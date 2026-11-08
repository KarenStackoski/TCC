"""Caminhos dos quatro manuais comparados e a anonimização usada antes de
entregá-los ao juiz LLM.

Ver docs/evaluation/01_estrutura.md.
"""

from __future__ import annotations

import re

from src.evaluation.metricas_texto import separar_citacoes

MANUAIS_PADRAO = {
    "templating": "data/manuals_generated/templating/manual.md",
    "rag": "data/manuals_generated/rag/manual_cohere.md",
    "hibrido": "data/manuals_generated/hybrid/manual_cohere.md",
    "manual": "data/manuals_generated/manual/manual.md",
}

# Linha que a Etapa 1 escreve no topo do manual e que identificaria o método.
_LINHA_IDENTIFICADORA = re.compile(r"^_Documento gerado automaticamente.*_\s*$", re.MULTILINE)


def anonimizar(texto: str) -> str:
    """Tira o rodapé de citações e a linha que identifica a etapa, que
    revelariam o método ao juiz."""
    corpo, _ = separar_citacoes(texto)
    corpo = _LINHA_IDENTIFICADORA.sub("", corpo)
    return re.sub(r"\n{3,}", "\n\n", corpo).strip() + "\n"
