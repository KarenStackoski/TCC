"""LLM como juiz: nota de 1 a 5 por critério, para cada manual.

Método: avaliação de resposta única (*single-answer grading*) de Zheng, L.
et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena". NeurIPS
2023 (Datasets and Benchmarks): o juiz recebe um texto por vez, os
critérios e a escala, e devolve nota e justificativa. Os critérios e as
definições estão em `CRITERIOS`. Como em G-Eval (Liu, Y. et al. "G-Eval:
NLG Evaluation using GPT-4 with Better Human Alignment". EMNLP 2023), o
juiz recebe as definições dos critérios explicitamente e é pedido a
raciocinar antes de dar a nota.

Critérios: os mais usados em avaliação humana de NLG (van der Lee, C.;
Gatt, A.; van Miltenburg, E.; Krahmer, E. "Human evaluation of
automatically generated text: Current trends and best practice
guidelines". Computer Speech & Language, v. 67, 2021) e, para
"completude" e "utilidade", a finalidade de um manual de usuário
(ISO/IEC/IEEE 26514 — informação para usuários de software).

O juiz recebe também os 32 artefatos de origem, para poder julgar
"correcao" e listar afirmações sem apoio nos artefatos.

Vieses conhecidos, a registrar no TCC:
- autopreferência: LLMs tendem a dar nota maior a textos gerados por elas
  mesmas (Panickssery, A.; Bowman, S. R.; Feng, S. "LLM Evaluators
  Recognize and Favor Their Own Generations". NeurIPS 2024). O juiz
  padrão (Command A) é da mesma empresa do gerador (Command R), então o
  viés pode favorecer os métodos 2 e 3;
- verbosidade: preferência por textos mais longos (Zheng et al., 2023).
Por isso o manual vai anonimizado (sem rodapé de citações nem a linha que
identifica a etapa), com temperatura 0.

Com `--execucoes`, o juiz avalia cada um dos manuais salvos pelo benchmark
(10 por método automático), e não só um. RAG e híbrido variam muito entre
execuções (ver variacao.py), então a nota de um manual só não representa
o método. As 10 execuções do templating são idênticas: a variação das
notas delas mede o ruído do próprio juiz. Cada avaliação fica salva com o
SHA-256 do arquivo julgado; uma avaliação já feita do mesmo arquivo, com o
mesmo modelo, não é refeita (permite continuar depois de uma interrupção).

Saída estruturada: `response_format` com JSON Schema. Fonte: Cohere,
"Structured Outputs" — https://docs.cohere.com/docs/structured-outputs
Ver docs/evaluation/01_estrutura.md, seção 7.

Uso:
    python -m src.evaluation.juiz_llm               # 1 manual por método
    python -m src.evaluation.juiz_llm --execucoes   # todas as execuções
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
from pathlib import Path

import cohere
from cohere.errors import TooManyRequestsError
from cohere.types import SystemChatMessageV2, UserChatMessageV2
from dotenv import load_dotenv

from src.common.schema import Artefato
from src.evaluation.manuais import MANUAIS_PADRAO, anonimizar
from src.jira.extractor import parse_issues
from src.rag.indexer import artefato_para_texto

load_dotenv()

MODELO_JUIZ = "command-a-03-2025"
JUIZ_DIR = Path("data/evaluation/juiz_llm")
EXECUCOES_DIR = Path("data/evaluation/execucoes")
METODOS_AUTOMATICOS = ("templating", "rag", "hibrido")

CRITERIOS: dict[str, str] = {
    "clareza": "O texto é fácil de entender; as frases são claras e sem ambiguidade.",
    "coerencia": "As partes do manual se encadeiam de forma lógica; a organização faz sentido.",
    "completude": "O manual cobre as funcionalidades, tarefas e problemas que um usuário precisaria conhecer.",
    "correcao": "O texto está correto em gramática e ortografia e não contém informações que pareçam erradas.",
    "utilidade": "Com este manual, um usuário conseguiria usar o sistema.",
}
ESCALA = "1 = discordo totalmente, 2 = discordo, 3 = neutro, 4 = concordo, 5 = concordo totalmente"

SYSTEM_PROMPT = (
    "Você é um avaliador imparcial de manuais de usuário de software. Avalie "
    "o manual fornecido com base apenas nos critérios definidos e nos "
    "artefatos de origem. Não deixe o tamanho do texto influenciar a nota: "
    "um manual mais longo não é automaticamente melhor. Para cada critério, "
    "escreva primeiro uma justificativa curta e depois a nota."
)

ESQUEMA_RESPOSTA = {
    "type": "object",
    "properties": {
        **{
            criterio: {
                "type": "object",
                "properties": {
                    "justificativa": {"type": "string"},
                    "nota": {"type": "integer"},
                },
                "required": ["justificativa", "nota"],
            }
            for criterio in CRITERIOS
        },
        "afirmacoes_nao_sustentadas": {"type": "array", "items": {"type": "string"}},
    },
    "required": [*CRITERIOS, "afirmacoes_nao_sustentadas"],
}


def montar_prompt(manual: str, artefatos: list[Artefato]) -> str:
    """Função pura: artefatos primeiro, manual depois, instrução por último."""
    fontes = "\n\n".join(artefato_para_texto(a) for a in artefatos)
    criterios = "\n".join(f"- {nome}: {definicao}" for nome, definicao in CRITERIOS.items())
    return (
        f"<artefatos_de_origem>\n{fontes}\n</artefatos_de_origem>\n\n"
        f"<manual>\n{manual}\n</manual>\n\n"
        f"Avalie o manual acima em cada critério, com nota inteira de 1 a 5 ({ESCALA}).\n"
        f"Critérios:\n{criterios}\n\n"
        "Em `afirmacoes_nao_sustentadas`, liste (copiando o trecho) cada afirmação do "
        "manual que não é sustentada pelos artefatos de origem ou que os contradiz. "
        "Se não houver nenhuma, devolva uma lista vazia."
    )


def validar(resposta: dict) -> dict:
    for criterio in CRITERIOS:
        nota = resposta[criterio]["nota"]
        if not 1 <= nota <= 5:
            raise ValueError(f"Nota fora da escala em {criterio}: {nota}")
    return resposta


def avaliar(manual: str, artefatos: list[Artefato], modelo: str = MODELO_JUIZ) -> dict:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente COHERE_API_KEY não definida. Veja .env.example.")
    cliente = cohere.ClientV2(api_key=api_key)
    resposta = cliente.chat(
        model=modelo,
        messages=[
            SystemChatMessageV2(role="system", content=SYSTEM_PROMPT),
            UserChatMessageV2(role="user", content=montar_prompt(manual, artefatos)),
        ],
        response_format={"type": "json_object", "json_schema": ESQUEMA_RESPOSTA},
        temperature=0,
    )
    texto = "".join(bloco.text for bloco in resposta.message.content or [])
    return validar(json.loads(texto))


def avaliar_com_espera(manual: str, artefatos: list[Artefato], modelo: str) -> dict:
    """Plano Trial: em "429 Too Many Requests", espera 60 s e tenta de novo
    (Cohere, "Rate Limits")."""
    while True:
        try:
            return avaliar(manual, artefatos, modelo)
        except TooManyRequestsError:
            print("  limite da API atingido; aguardando 60 s")
            time.sleep(60)


def notas(resultado: dict) -> dict:
    linha = {criterio: resultado[criterio]["nota"] for criterio in CRITERIOS}
    linha["afirmacoes_nao_sustentadas"] = len(resultado["afirmacoes_nao_sustentadas"])
    return linha


def arquivos_das_execucoes(execucoes_dir: Path, manual_humano: str) -> list[tuple[str, int, Path]]:
    """(método, nº da execução, arquivo) de cada manual salvo pelo benchmark.
    O manual humano entra como execução única do método "manual"."""
    arquivos = []
    for metodo in METODOS_AUTOMATICOS:
        for caminho in sorted((execucoes_dir / metodo).glob("execucao_*.md")):
            arquivos.append((metodo, int(caminho.stem.split("_")[1]), caminho))
    if Path(manual_humano).exists():
        arquivos.append(("manual", 1, Path(manual_humano)))
    return arquivos


def _escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def julgar_manuais(manuais: dict[str, str], artefatos: list[Artefato], modelo: str) -> None:
    linhas = []
    for metodo, caminho in manuais.items():
        if not Path(caminho).exists():
            print(f"Aviso: {caminho} não encontrado; {metodo} fica de fora.")
            continue
        manual = anonimizar(Path(caminho).read_text(encoding="utf-8"))
        resultado = avaliar_com_espera(manual, artefatos, modelo)
        (JUIZ_DIR / f"{metodo}.json").write_text(
            json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        linha = {"metodo": metodo, "modelo_juiz": modelo, **notas(resultado)}
        linhas.append(linha)
        print(linha)
    _escrever_csv(JUIZ_DIR / "resultado.csv", linhas)


def julgar_execucoes(arquivos: list[tuple[str, int, Path]], artefatos: list[Artefato], modelo: str) -> None:
    """Uma avaliação por manual salvo. O CSV é regravado depois de cada uma,
    para uma falha no meio não perder o que já foi feito."""
    linhas = []
    for metodo, execucao, caminho in arquivos:
        sha256 = hashlib.sha256(caminho.read_bytes()).hexdigest()
        destino = JUIZ_DIR / "execucoes" / metodo / f"execucao_{execucao:02d}.json"
        salvo = json.loads(destino.read_text(encoding="utf-8")) if destino.exists() else None
        if salvo and salvo["sha256"] == sha256 and salvo["modelo_juiz"] == modelo:
            resultado = salvo["avaliacao"]
            print(f"{metodo} nº {execucao}: já avaliado, mantido")
        else:
            print(f"{metodo} nº {execucao}: avaliando")
            manual = anonimizar(caminho.read_text(encoding="utf-8"))
            resultado = avaliar_com_espera(manual, artefatos, modelo)
            destino.parent.mkdir(parents=True, exist_ok=True)
            registro = {"arquivo": caminho.as_posix(), "sha256": sha256, "modelo_juiz": modelo, "avaliacao": resultado}
            destino.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
        linhas.append(
            {"metodo": metodo, "execucao": execucao, "modelo_juiz": modelo, **notas(resultado), "arquivo": caminho.as_posix()}
        )
        _escrever_csv(JUIZ_DIR / "resultado_execucoes.csv", linhas)


def main() -> None:
    parser = argparse.ArgumentParser(description="Avaliação dos manuais por LLM como juiz.")
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--modelo", default=MODELO_JUIZ)
    parser.add_argument("--manual-humano", default=MANUAIS_PADRAO["manual"])
    parser.add_argument(
        "--execucoes",
        action="store_true",
        help=f"avalia cada manual salvo pelo benchmark em {EXECUCOES_DIR} (e o manual humano)",
    )
    args = parser.parse_args()

    with open(args.entrada, encoding="utf-8") as arquivo:
        artefatos = parse_issues(json.load(arquivo)["issues"])

    JUIZ_DIR.mkdir(parents=True, exist_ok=True)
    if args.execucoes:
        julgar_execucoes(arquivos_das_execucoes(EXECUCOES_DIR, args.manual_humano), artefatos, args.modelo)
    else:
        julgar_manuais(dict(MANUAIS_PADRAO, manual=args.manual_humano), artefatos, args.modelo)


if __name__ == "__main__":
    main()
