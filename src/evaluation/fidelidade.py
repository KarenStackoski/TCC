"""Fidelidade às fontes (alucinação) e cobertura de conteúdo, por anotação.

Não existe métrica automática confiável para "esta frase é sustentada pelos
artefatos?" em português sem usar outra LLM como juiz, e o juiz traz vieses
próprios (ver src/evaluation/juiz_llm.py). Por isso a medida principal é
anotada por uma pessoa, frase a frase, como na avaliação humana de
fidelidade de Maynez, J.; Narayan, S.; Bohnet, B.; McDonald, R. "On
Faithfulness and Factuality in Abstractive Summarization". ACL, 2020.

Rótulos por frase (definição de alucinação de Ji, Z. et al. "Survey of
Hallucination in Natural Language Generation". ACM Computing Surveys,
v. 55, n. 12, 2023):
  S = sustentada: o conteúdo está nos artefatos;
  P = parcialmente sustentada: parte está nos artefatos, parte não;
  N = não sustentada (alucinação): o conteúdo não está nos artefatos ou
      os contradiz.
  - = não se aplica (frase sem conteúdo verificável, ex.: "Bem-vindo ao manual").

Na mesma planilha, a coluna `artefatos` recebe as chaves (SCRUM-N) de onde
veio o conteúdo da frase; a cobertura de conteúdo é a proporção dos 32
artefatos que aparecem em alguma frase. É a mesma ideia de cobertura
(recall de conteúdo) usada na avaliação de sumarização.
Ver docs/evaluation/01_estrutura.md, seção 4.

Uso:
    python -m src.evaluation.fidelidade preparar
    (anotar as planilhas em data/evaluation/fidelidade/)
    python -m src.evaluation.fidelidade analisar
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from src.evaluation.avaliacao_humana import MANUAIS_PADRAO
from src.evaluation.metricas_texto import dividir_frases, limpar_markdown
from src.jira.extractor import parse_issues

FIDELIDADE_DIR = Path("data/evaluation/fidelidade")
ROTULOS = {"S", "P", "N", "-"}
CAMPOS = ["id", "frase", "rotulo", "artefatos", "observacao"]


def preparar(manuais: dict[str, str], saida_dir: Path = FIDELIDADE_DIR) -> dict[str, int]:
    """Uma planilha por método, uma frase por linha. Não sobrescreve uma
    planilha que já exista (para não apagar anotação feita)."""
    saida_dir.mkdir(parents=True, exist_ok=True)
    contagem: dict[str, int] = {}
    for metodo, caminho in manuais.items():
        if not Path(caminho).exists():
            print(f"Aviso: {caminho} não encontrado; {metodo} fica de fora.")
            continue
        destino = saida_dir / f"{metodo}.csv"
        if destino.exists():
            print(f"{destino} já existe; mantido sem alteração.")
            continue
        frases = dividir_frases(limpar_markdown(Path(caminho).read_text(encoding="utf-8")))
        with open(destino, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(CAMPOS)
            for indice, frase in enumerate(frases, start=1):
                escritor.writerow([indice, frase, "", "", ""])
        contagem[metodo] = len(frases)
    return contagem


def _chaves(celula: str) -> set[str]:
    return set(re.findall(r"SCRUM-\d+", celula or ""))


def analisar_planilha(linhas: list[dict], total_artefatos: int) -> dict:
    rotulos = [l["rotulo"].strip().upper() for l in linhas]
    invalidos = [l["id"] for l, r in zip(linhas, rotulos) if r not in ROTULOS]
    if invalidos:
        raise ValueError(f"Frases sem rótulo válido (S/P/N/-): {', '.join(invalidos[:10])}")
    verificaveis = [r for r in rotulos if r != "-"]
    n = len(verificaveis)
    cobertos = set().union(*(_chaves(l["artefatos"]) for l in linhas)) if linhas else set()
    return {
        "frases": len(rotulos),
        "frases_verificaveis": n,
        "sustentadas_%": round(100 * verificaveis.count("S") / n, 1) if n else 0.0,
        "parciais_%": round(100 * verificaveis.count("P") / n, 1) if n else 0.0,
        "nao_sustentadas_%": round(100 * verificaveis.count("N") / n, 1) if n else 0.0,
        "artefatos_cobertos": len(cobertos),
        "cobertura_conteudo_%": round(100 * len(cobertos) / total_artefatos, 1) if total_artefatos else 0.0,
    }


def analisar(entrada_json: str, saida_dir: Path = FIDELIDADE_DIR) -> list[dict]:
    with open(entrada_json, encoding="utf-8") as arquivo:
        total = len(parse_issues(json.load(arquivo)["issues"]))
    resultados = []
    for planilha in sorted(saida_dir.glob("*.csv")):
        if planilha.name == "resultado.csv":
            continue
        with open(planilha, newline="", encoding="utf-8-sig") as arquivo:
            linhas = list(csv.DictReader(arquivo))
        resultados.append({"metodo": planilha.stem, **analisar_planilha(linhas, total)})
    return resultados


def main() -> None:
    parser = argparse.ArgumentParser(description="Planilhas de fidelidade e cobertura.")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_preparar = sub.add_parser("preparar")
    p_preparar.add_argument("--manual-humano", default=MANUAIS_PADRAO["manual"])
    p_analisar = sub.add_parser("analisar")
    p_analisar.add_argument("--entrada", default="data/raw/data.json")
    args = parser.parse_args()

    if args.comando == "preparar":
        contagem = preparar(dict(MANUAIS_PADRAO, manual=args.manual_humano))
        for metodo, n in contagem.items():
            print(f"{metodo}: {n} frases para anotar em {FIDELIDADE_DIR / (metodo + '.csv')}")
        return

    resultados = analisar(args.entrada)
    with open(FIDELIDADE_DIR / "resultado.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)
    for linha in resultados:
        print(linha)


if __name__ == "__main__":
    main()
