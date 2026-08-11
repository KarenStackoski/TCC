"""Modelo de dados padronizado dos artefatos Jira.

Sem dependência de Jira/ADF/Jinja2 de propósito: `Artefato` e `Subtarefa`
são o contrato compartilhado entre as três etapas do TCC (templating, RAG
e híbrida). Quem converte JSON bruto do Jira para `Artefato` é
`src/jira/extractor.py`, não este módulo.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Subtarefa:
    chave: str
    titulo: str
    status: str


@dataclass
class Artefato:
    chave: str
    titulo: str
    tipo: str
    status: str
    descricao: str
    prioridade: str | None = None
    responsavel: str | None = None
    labels: list[str] = field(default_factory=list)
    subtarefas: list[Subtarefa] = field(default_factory=list)
    criterios_aceitacao: list[str] = field(default_factory=list)
