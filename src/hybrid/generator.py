"""Orquestração da Etapa 3 (Híbrido): reaproveita a classificação por tipo
da Etapa 1 (estrutura fixa) e gera o texto de cada seção via LLM, uma
chamada por seção. Mesmo formato de CLI de src/rag/pipeline.py (Etapa 2).
Ver docs/hybrid/01_estrutura.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cohere.types import Citation
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.common.schema import Artefato
from src.hybrid.section_backend import SECTION_CONFIG, gerar_secao_claude, gerar_secao_cohere
from src.jira.extractor import parse_issues
from src.templating.generator import classificar_por_tipo

TEMPLATE_DIR = Path(__file__).parent / "templates"
TEMPLATE_NOME = "manual_hibrido.md.j2"

VARIANTES_DISPONIVEIS = ("cohere", "claude")

# Ordem das seções no manual final — mesma ordem de manual_template.md.j2 (Etapa 1).
ORDEM_CATEGORIAS = ("epic", "story", "task", "bug", "outros")


def _formatar_citacoes(citacoes_por_categoria: dict[str, list[Citation]]) -> str:
    linhas = []
    for categoria, citacoes in citacoes_por_categoria.items():
        if not citacoes:
            continue
        titulo_secao, _ = SECTION_CONFIG[categoria]
        linhas.append(f"\n**{titulo_secao}:**\n")
        for citacao in citacoes:
            fontes = ", ".join(fonte.id for fonte in citacao.sources or [])
            linhas.append(f'- "{citacao.text}" — fonte(s): {fontes}')
    if not linhas:
        return ""
    return "\n\n---\n\n**Citações (Cohere Command R):**\n" + "\n".join(linhas)


def _renderizar(secoes: dict[str, str]) -> str:
    ambiente = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=select_autoescape(disabled_extensions=(".j2",), default=False),
    )
    template = ambiente.get_template(TEMPLATE_NOME)
    return template.render(secoes=secoes)


def gerar_manuais(
    artefatos: list[Artefato], variantes: tuple[str, ...] = VARIANTES_DISPONIVEIS
) -> dict[str, str]:
    """Gera só as variantes pedidas em `variantes` — mesmo mecanismo de
    src/rag/pipeline.py.gerar_manuais (Etapa 2), pela mesma razão: a
    variante `claude` depende de ANTHROPIC_API_KEY paga, não configurada por
    padrão neste projeto."""
    categorias = classificar_por_tipo(artefatos)

    manuais: dict[str, str] = {}

    if "cohere" in variantes:
        secoes_cohere: dict[str, str] = {}
        citacoes_por_categoria: dict[str, list[Citation]] = {}
        for categoria in ORDEM_CATEGORIAS:
            texto, citacoes = gerar_secao_cohere(categoria, categorias[categoria])
            secoes_cohere[categoria] = texto
            citacoes_por_categoria[categoria] = citacoes
        manuais["cohere"] = _renderizar(secoes_cohere) + _formatar_citacoes(citacoes_por_categoria)

    if "claude" in variantes:
        secoes_claude = {
            categoria: gerar_secao_claude(categoria, categorias[categoria])
            for categoria in ORDEM_CATEGORIAS
        }
        manuais["claude"] = _renderizar(secoes_claude)

    return manuais


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera os manuais (Etapa 3 — Híbrido) a partir de um export do Jira."
    )
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--saida-dir", default="data/manuals_generated/hybrid")
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
