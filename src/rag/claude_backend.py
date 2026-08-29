"""Geração do manual via Claude (Messages API) — variante "Cohere + Claude" da Etapa 2.

Ao contrário do Command R (src/rag/cohere_backend.py), a API Messages da
Anthropic não tem um parâmetro nativo de `documents`/citação — os artefatos
recuperados são formatados manualmente no prompt, seguindo a recomendação
oficial da Anthropic para prompts com múltiplos documentos: conteúdo longo
no topo do prompt, instrução no final, cada documento envolvido em tags
`<document>`/`<document_content>`/`<source>` dentro de `<documents>`.
Fonte: Anthropic. "Claude prompting best practices — Long context prompting".
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
Modelo: Anthropic. "Models overview". https://platform.claude.com/docs/en/models/overview
Ver docs/rag/01_estrutura.md, seção 3.4.
"""

from __future__ import annotations

import os

import anthropic
from dotenv import load_dotenv

from src.common.schema import Artefato
from src.rag.indexer import artefato_para_texto

load_dotenv()

CHAT_MODEL = "claude-sonnet-5"
MAX_TOKENS = 8192
TEMPERATURE = 0.3

SYSTEM_PROMPT = (
    "Você é um redator técnico responsável por escrever manuais de usuário "
    "de software a partir de artefatos de gestão de projeto (Jira). Escreva "
    "em português do Brasil, em Markdown, de forma clara e organizada."
)

INSTRUCAO = (
    "Usando os documentos acima (artefatos do Jira: epics, histórias de "
    "usuário, tarefas e bugs), escreva um manual de usuário completo do "
    "produto. Organize o documento em seções que façam sentido para quem vai "
    "usar o sistema — você decide a estrutura, os títulos das seções e a "
    "ordem. Não invente funcionalidades que não estejam nos documentos."
)


def _montar_documento_xml(indice: int, artefato: Artefato) -> str:
    fonte = f"{artefato.chave} — {artefato.titulo} ({artefato.tipo})"
    return (
        f'<document index="{indice}">\n'
        f"<source>{fonte}</source>\n"
        f"<document_content>\n{artefato_para_texto(artefato)}\n</document_content>\n"
        f"</document>"
    )


def montar_prompt(artefatos_recuperados: list[Artefato]) -> str:
    """Monta o prompt completo — documentos primeiro, instrução por último
    (ver fonte no docstring do módulo). Função pura, sem chamada de API,
    para poder ser testada isoladamente."""
    documentos_xml = "\n".join(
        _montar_documento_xml(indice, artefato)
        for indice, artefato in enumerate(artefatos_recuperados, start=1)
    )
    return f"<documents>\n{documentos_xml}\n</documents>\n\n{INSTRUCAO}"


def gerar_manual(artefatos_recuperados: list[Artefato]) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente ANTHROPIC_API_KEY não definida. Veja .env.example.")
    cliente = anthropic.Anthropic(api_key=api_key)

    resposta = cliente.messages.create(
        model=CHAT_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": montar_prompt(artefatos_recuperados)}],
    )

    return "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
