"""Benchmark de tempo e tokens dos métodos automáticos (Etapas 1, 2 e 3).

Roda cada método N vezes sobre a mesma entrada, cronometra cada execução com
`time.perf_counter()` e separa o tempo gasto em cada fase (indexação,
recuperação, geração pela API; o restante é processamento local: Chroma,
Jinja2, montagem do texto). Cada saída é guardada, para a análise de
variação entre execuções (`src/evaluation/variacao.py`).

Por que repetir: uma medição só não é confiável quando há ruído (rede,
latência da API, carga do servidor); o recomendado é repetir e reportar uma
medida central com a sua dispersão. Fonte: Georges, A.; Buytaert, D.;
Eeckhout, L. "Statistically Rigorous Java Performance Evaluation". OOPSLA,
2007. Usa-se a mediana (robusta a valores extremos) e o intervalo mín.–máx.
Ver docs/evaluation/01_estrutura.md, seção 2.

O tempo do método 4 (manual, humano) não sai daqui: é cronometrado à mão e
registrado em data/evaluation/tempo_manual.csv (ver o mesmo documento).

Uso:
    python -m src.evaluation.benchmark --repeticoes 5
    python -m src.evaluation.benchmark --metodo templating --repeticoes 30
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import time
from datetime import datetime
from pathlib import Path

import httpx
from cohere.errors import TooManyRequestsError

from src.common.schema import Artefato
from src.evaluation.medicao import RegistroChamadas
from src.hybrid import generator as hybrid_generator
from src.jira.extractor import parse_issues
from src.rag import pipeline as rag_pipeline
from src.templating import generator as templating_generator

SAIDA_DIR = Path("data/evaluation")
METODOS = ("templating", "rag", "hibrido")

# Limite do plano Trial da Cohere para o endpoint de chat: 20 chamadas/min.
# Fonte: Cohere, "Rate Limits" — https://docs.cohere.com/docs/rate-limits
ESPERA_LIMITE_S = 60
# Mais que isso seguido indica a cota mensal do Trial (1.000 chamadas), não
# o limite por minuto — mesma fonte.
MAX_TENTATIVAS = 3

# Tempo máximo de espera por resposta do SDK da Cohere: 300 s (padrão do
# cliente, `timeout` em cohere.ClientV2). Uma execução em que alguma
# chamada passa disso não termina, então não tem tempo medido: é
# registrada em falhas.csv e refeita. O TCC deve relatar quantas houve.
ERROS_DE_REDE = (httpx.TimeoutException, httpx.NetworkError)

CAMPOS_CSV = [
    "metodo",
    "execucao",
    "inicio",
    "arquivo",
    "sha256",
    "tempo_total_s",
    "tempo_indexacao_s",
    "tempo_recuperacao_s",
    "tempo_geracao_s",
    "tempo_local_s",
    "chamadas_api",
    "tokens_entrada",
    "tokens_saida",
    "caracteres_saida",
]


def _gerar(metodo: str, artefatos: list[Artefato]) -> str:
    """Chama exatamente a mesma função que a CLI de cada etapa usa. Os
    módulos são importados no topo do arquivo, antes de qualquer medição:
    importar dentro desta função faria a 1ª execução de cada método pagar o
    tempo de importação (chromadb, cohere...) e as outras não."""
    if metodo == "templating":
        return templating_generator.gerar_manual(artefatos)
    if metodo == "rag":
        return rag_pipeline.gerar_manuais(artefatos, variantes=("cohere",))["cohere"]
    if metodo == "hibrido":
        return hybrid_generator.gerar_manuais(artefatos, variantes=("cohere",))["cohere"]
    raise ValueError(f"Método desconhecido: {metodo}")


def medir_execucao(metodo: str, artefatos: list[Artefato]) -> tuple[dict, str]:
    """Uma execução cronometrada. Devolve (linha do CSV, texto gerado)."""
    data_hora = datetime.now().astimezone().isoformat(timespec="seconds")
    with RegistroChamadas() as registro:
        inicio = time.perf_counter()
        texto = _gerar(metodo, artefatos)
        total = time.perf_counter() - inicio

    fases = registro.tempo_por_fase()
    entrada, saida = registro.total_tokens()
    linha = {
        "metodo": metodo,
        "inicio": data_hora,
        # SHA-256 do texto salvo: permite provar depois que o arquivo da
        # execução não foi alterado (FIPS 180-4; módulo hashlib do Python).
        "sha256": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
        "tempo_total_s": round(total, 4),
        "tempo_indexacao_s": round(fases["indexacao"], 4),
        "tempo_recuperacao_s": round(fases["recuperacao"], 4),
        "tempo_geracao_s": round(fases["geracao"], 4),
        "tempo_local_s": round(total - sum(fases.values()), 4),
        "chamadas_api": len(registro.chamadas),
        "tokens_entrada": entrada,
        "tokens_saida": saida,
        "caracteres_saida": len(texto),
    }
    return linha, texto


def _escrever_csv(caminho: Path, linhas: list[dict], campos: list[str]) -> None:
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)


def _registrar_falha(saida_dir: Path, metodo: str, execucao: int, erro: str) -> None:
    caminho = saida_dir / "falhas.csv"
    novo = not caminho.exists()
    with open(caminho, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        if novo:
            escritor.writerow(["metodo", "execucao", "data_hora", "erro"])
        agora = datetime.now().astimezone().isoformat(timespec="seconds")
        escritor.writerow([metodo, execucao, agora, erro])


def resumir(linhas: list[dict]) -> list[dict]:
    """Mediana, mín., máx. e desvio-padrão do tempo total por método."""
    resumo = []
    for metodo in dict.fromkeys(l["metodo"] for l in linhas):
        tempos = [float(l["tempo_total_s"]) for l in linhas if l["metodo"] == metodo]
        tokens = [int(l["tokens_entrada"]) + int(l["tokens_saida"]) for l in linhas if l["metodo"] == metodo]
        resumo.append(
            {
                "metodo": metodo,
                "execucoes": len(tempos),
                "mediana_s": round(statistics.median(tempos), 4),
                "min_s": round(min(tempos), 4),
                "max_s": round(max(tempos), 4),
                "desvio_padrao_s": round(statistics.stdev(tempos), 4) if len(tempos) > 1 else 0.0,
                "mediana_tokens": statistics.median(tokens),
            }
        )
    return resumo


def main() -> None:
    parser = argparse.ArgumentParser(description="Mede tempo e tokens de cada método de geração.")
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--metodo", choices=METODOS, action="append", dest="metodos")
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--pausa", type=float, default=3.0, help="Segundos entre execuções (limite da API).")
    parser.add_argument("--saida-dir", default=str(SAIDA_DIR))
    parser.add_argument(
        "--a-partir-de",
        type=int,
        default=1,
        help="Continua uma medição interrompida: mantém as execuções anteriores a este número.",
    )
    args = parser.parse_args()
    metodos = tuple(args.metodos) if args.metodos else METODOS

    with open(args.entrada, encoding="utf-8") as arquivo:
        artefatos = parse_issues(json.load(arquivo)["issues"])

    saida_dir = Path(args.saida_dir)
    saida_dir.mkdir(parents=True, exist_ok=True)
    csv_path = saida_dir / "tempos.csv"
    # Métodos não rodados agora mantêm as linhas de uma execução anterior,
    # para dar para medir um método de cada vez sem perder os outros.
    anteriores: list[dict] = []
    if csv_path.exists():
        with open(csv_path, newline="", encoding="utf-8") as arquivo:
            anteriores = [
                l
                for l in csv.DictReader(arquivo)
                if l["metodo"] not in metodos or int(l["execucao"]) < args.a_partir_de
            ]

    linhas: list[dict] = []
    for metodo in metodos:
        exec_dir = saida_dir / "execucoes" / metodo
        exec_dir.mkdir(parents=True, exist_ok=True)
        for execucao in range(args.a_partir_de, args.repeticoes + 1):
            for tentativa in range(1, MAX_TENTATIVAS + 1):
                try:
                    linha, texto = medir_execucao(metodo, artefatos)
                    break
                except ERROS_DE_REDE as erro:
                    _registrar_falha(saida_dir, metodo, execucao, f"{type(erro).__name__}: {erro}")
                    print(f"  falha de rede ({type(erro).__name__}); execução descartada e refeita")
                    time.sleep(args.pausa)
                except TooManyRequestsError:
                    # A execução interrompida é descartada inteira e refeita
                    # do zero, para a espera não contaminar o tempo medido.
                    if tentativa == MAX_TENTATIVAS:
                        # Provavelmente a cota mensal (1.000 chamadas) acabou.
                        raise SystemExit("Limite da API da Cohere persistente; parando. Resultados parciais em tempos.csv.")
                    print(f"  limite da API atingido; aguardando {ESPERA_LIMITE_S} s e refazendo")
                    time.sleep(ESPERA_LIMITE_S)
            else:
                raise SystemExit(f"{metodo} #{execucao} falhou {MAX_TENTATIVAS} vezes seguidas; parando. Veja falhas.csv.")
            arquivo_md = exec_dir / f"execucao_{execucao:02d}.md"
            # newline="\n": sem isso, o Windows grava \r\n e o SHA-256 do
            # arquivo deixaria de bater com o registrado no CSV.
            arquivo_md.write_text(texto, encoding="utf-8", newline="\n")
            linha["execucao"] = execucao
            linha["arquivo"] = arquivo_md.as_posix()
            linhas.append(linha)
            # Grava a cada execução: se algo falhar no meio, o que já foi
            # medido não se perde.
            _escrever_csv(csv_path, anteriores + linhas, CAMPOS_CSV)
            print(f"{metodo} #{execucao}: {linha['tempo_total_s']} s")
            if metodo != "templating" and args.pausa:
                time.sleep(args.pausa)

    resumo = resumir(anteriores + linhas)
    _escrever_csv(saida_dir / "tempos_resumo.csv", resumo, list(resumo[0]))
    for item in resumo:
        print(item)
    print(f"Resultados em {saida_dir / 'tempos.csv'} e {saida_dir / 'tempos_resumo.csv'}")


if __name__ == "__main__":
    main()
