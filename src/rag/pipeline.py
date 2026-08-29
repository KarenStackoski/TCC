"""Orquestração da Etapa 2 (RAG): indexação, recuperação e as duas variantes
de geração (Cohere Command R e Claude). Mesmo formato de CLI de
src/templating/generator.py (Etapa 1) — ver docs/rag/01_estrutura.md,
seção 3.5.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cohere.types import Citation

from src.common.schema import Artefato
from src.jira.extractor import parse_issues
from src.rag import claude_backend, cohere_backend
from src.rag.indexer import indexar
from src.rag.retriever import recuperar


def _formatar_citacoes(citacoes: list[Citation]) -> str:
    if not citacoes:
        return ""
    linhas = ["\n\n---\n\n**Citações (Cohere Command R):**\n"]
    for citacao in citacoes:
        fontes = ", ".join(fonte.id for fonte in citacao.sources or [])
        linhas.append(f'- "{citacao.text}" — fonte(s): {fontes}')
    return "\n".join(linhas)


VARIANTES_DISPONIVEIS = ("cohere", "claude")


def gerar_manuais(
    artefatos: list[Artefato], variantes: tuple[str, ...] = VARIANTES_DISPONIVEIS
) -> dict[str, str]:
    """Gera só as variantes pedidas em `variantes` — útil para rodar apenas
    `cohere` quando ainda não há `ANTHROPIC_API_KEY` configurada (a variante
    `claude` depende de uma chave paga da Anthropic, a `cohere` não)."""
    artefatos_por_chave = {artefato.chave: artefato for artefato in artefatos}
    collection = indexar(artefatos)
    recuperados = recuperar(collection, artefatos_por_chave)

    manuais: dict[str, str] = {}
    if "cohere" in variantes:
        texto_cohere, citacoes = cohere_backend.gerar_manual(recuperados)
        manuais["cohere"] = texto_cohere + _formatar_citacoes(citacoes)
    if "claude" in variantes:
        manuais["claude"] = claude_backend.gerar_manual(recuperados)
    return manuais


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera os manuais (Etapa 2 — RAG) a partir de um export do Jira."
    )
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--saida-dir", default="data/manuals_generated/rag")
    parser.add_argument(
        "--variante",
        choices=VARIANTES_DISPONIVEIS,
        action="append",
        dest="variantes",
        help="Repita a flag para gerar mais de uma variante (padrão: todas).",
    )
    args = parser.parse_args()
    variantes = tuple(args.variantes) if args.variantes else VARIANTES_DISPONIVEIS

    with open(args.entrada, encoding="utf-8") as arquivo:
        bruto = json.load(arquivo)

    artefatos = parse_issues(bruto["issues"])
    manuais = gerar_manuais(artefatos, variantes)

    saida_dir = Path(args.saida_dir)
    saida_dir.mkdir(parents=True, exist_ok=True)
    for variante, texto in manuais.items():
        caminho = saida_dir / f"manual_{variante}.md"
        caminho.write_text(texto, encoding="utf-8")
        print(f"Manual ({variante}) gerado em {caminho}")


if __name__ == "__main__":
    main()
