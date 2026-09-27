"""LLM como juiz: nota de 1 a 5 por critério, para cada manual (complemento
da avaliação humana, não substituto).

Método: avaliação de resposta única (*single-answer grading*) de Zheng, L.
et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena". NeurIPS
2023 (Datasets and Benchmarks): o juiz recebe um texto por vez, os
critérios e a escala, e devolve nota e justificativa. Os critérios e as
definições são os mesmos entregues aos avaliadores humanos
(`avaliacao_humana.CRITERIOS`), para as notas serem comparáveis. Como em
G-Eval (Liu, Y. et al. "G-Eval: NLG Evaluation using GPT-4 with Better
Human Alignment". EMNLP 2023), o juiz recebe as definições dos critérios
explicitamente e é pedido a raciocinar antes de dar a nota.

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

Saída estruturada: `response_format` com JSON Schema. Fonte: Cohere,
"Structured Outputs" — https://docs.cohere.com/docs/structured-outputs
Ver docs/evaluation/01_estrutura.md, seção 8.

Uso:
    python -m src.evaluation.juiz_llm
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path

import cohere
from cohere.errors import TooManyRequestsError
from cohere.types import SystemChatMessageV2, UserChatMessageV2
from dotenv import load_dotenv

from src.common.schema import Artefato
from src.evaluation.avaliacao_humana import CRITERIOS, ESCALA, MANUAIS_PADRAO, anonimizar
from src.jira.extractor import parse_issues
from src.rag.indexer import artefato_para_texto

load_dotenv()

MODELO_JUIZ = "command-a-03-2025"
JUIZ_DIR = Path("data/evaluation/juiz_llm")

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Avaliação dos manuais por LLM como juiz.")
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--modelo", default=MODELO_JUIZ)
    parser.add_argument("--manual-humano", default=MANUAIS_PADRAO["manual"])
    args = parser.parse_args()

    with open(args.entrada, encoding="utf-8") as arquivo:
        artefatos = parse_issues(json.load(arquivo)["issues"])

    JUIZ_DIR.mkdir(parents=True, exist_ok=True)
    linhas = []
    for metodo, caminho in dict(MANUAIS_PADRAO, manual=args.manual_humano).items():
        if not Path(caminho).exists():
            print(f"Aviso: {caminho} não encontrado; {metodo} fica de fora.")
            continue
        manual = anonimizar(Path(caminho).read_text(encoding="utf-8"))
        while True:
            try:
                resultado = avaliar(manual, artefatos, args.modelo)
                break
            except TooManyRequestsError:
                print("  limite da API atingido; aguardando 60 s")
                time.sleep(60)
        (JUIZ_DIR / f"{metodo}.json").write_text(
            json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        linha = {"metodo": metodo, "modelo_juiz": args.modelo}
        linha.update({criterio: resultado[criterio]["nota"] for criterio in CRITERIOS})
        linha["afirmacoes_nao_sustentadas"] = len(resultado["afirmacoes_nao_sustentadas"])
        linhas.append(linha)
        print(linha)

    with open(JUIZ_DIR / "resultado.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


if __name__ == "__main__":
    main()
