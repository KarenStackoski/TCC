"""Classificação dos artefatos por tipo e renderização do manual via Jinja2.

Fonte do motor de template: https://jinja.palletsprojects.com/
Estrutura das seções do manual: ISO/IEC/IEEE 26514:2008 — ver docs/templating/01_estrutura.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.common.schema import Artefato
from src.jira.extractor import parse_issues

TEMPLATE_DIR = Path(__file__).parent / "templates"
TEMPLATE_NOME = "manual_template.md.j2"

# Tipos do Jira mapeados para as quatro categorias fixas do template.
# "Request" -> "task" e "História" -> "story" são decisões específicas
# deste dataset (não existe tipo "Task" nele) — ver docs/templating/01_estrutura.md,
# seção 3.4.
TIPO_PARA_CATEGORIA: dict[str, str] = {
    "epic": "epic",
    "história": "story",
    "historia": "story",
    "story": "story",
    "user story": "story",
    "bug": "bug",
    "task": "task",
    "tarefa": "task",
    "request": "task",
}


def classificar_por_tipo(artefatos: list[Artefato]) -> dict[str, list[Artefato]]:
    """Agrupa os artefatos em epic/story/task/bug, conforme TIPO_PARA_CATEGORIA.

    Tipos não reconhecidos caem em "outros", para nenhum artefato ser
    descartado silenciosamente do manual.
    """
    categorias: dict[str, list[Artefato]] = {
        "epic": [],
        "story": [],
        "task": [],
        "bug": [],
        "outros": [],
    }
    for artefato in artefatos:
        categoria = TIPO_PARA_CATEGORIA.get(artefato.tipo.strip().casefold(), "outros")
        categorias[categoria].append(artefato)
    return categorias


def gerar_manual(
    artefatos: list[Artefato],
    template_dir: Path | str = TEMPLATE_DIR,
    template_nome: str = TEMPLATE_NOME,
) -> str:
    ambiente = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=select_autoescape(disabled_extensions=(".j2",), default=False),
    )
    template = ambiente.get_template(template_nome)
    categorias = classificar_por_tipo(artefatos)
    return template.render(**categorias)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera o manual (Etapa 1 — Templating puro) a partir de um export do Jira."
    )
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--saida", default="data/manuals_generated/templating/manual.md")
    args = parser.parse_args()

    with open(args.entrada, encoding="utf-8") as arquivo:
        bruto = json.load(arquivo)

    artefatos = parse_issues(bruto["issues"])
    manual = gerar_manual(artefatos)

    saida_path = Path(args.saida)
    saida_path.parent.mkdir(parents=True, exist_ok=True)
    saida_path.write_text(manual, encoding="utf-8")
    print(f"Manual gerado em {saida_path}")


if __name__ == "__main__":
    main()
