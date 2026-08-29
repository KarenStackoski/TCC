"""Geração do manual via Cohere Command R — variante "Cohere puro" da Etapa 2.

Usa o modo nativo de RAG do Command R (parâmetro `documents` do endpoint
Chat v2): a geração fica fundamentada (*grounded*) nos documentos passados
e a resposta inclui citações automáticas (span de texto -> documento
fonte), sem implementação manual de citação.
Fonte: Cohere. "Retrieval Augmented Generation (RAG)".
https://docs.cohere.com/docs/retrieval-augmented-generation-rag
Modelo: Cohere. "Models overview". https://docs.cohere.com/docs/models
Ver docs/rag/01_estrutura.md, seção 3.3.
"""

from __future__ import annotations

import os

import cohere
from cohere.types import Citation, Document, SystemChatMessageV2, UserChatMessageV2
from dotenv import load_dotenv

from src.common.schema import Artefato
from src.rag.indexer import artefato_para_texto

load_dotenv()

CHAT_MODEL = "command-r-08-2024"
TEMPERATURE = 0.3

SYSTEM_PROMPT = (
    "Você é um redator técnico responsável por escrever manuais de usuário "
    "de software a partir de artefatos de gestão de projeto (Jira). Escreva "
    "em português do Brasil, em Markdown, de forma clara e organizada."
)

INSTRUCAO = (
    "Usando os documentos fornecidos (artefatos do Jira: epics, histórias de "
    "usuário, tarefas e bugs), escreva um manual de usuário completo do "
    "produto. Organize o documento em seções que façam sentido para quem vai "
    "usar o sistema — você decide a estrutura, os títulos das seções e a "
    "ordem. Não invente funcionalidades que não estejam nos documentos."
)


def _formatar_documentos(artefatos: list[Artefato]) -> list[Document]:
    return [
        Document(
            id=artefato.chave,
            data={
                "titulo": artefato.titulo,
                "tipo": artefato.tipo,
                "status": artefato.status,
                "texto": artefato_para_texto(artefato),
            },
        )
        for artefato in artefatos
    ]


def gerar_manual(artefatos_recuperados: list[Artefato]) -> tuple[str, list[Citation]]:
    """Devolve (texto_markdown, citações) — as citações já vêm prontas do
    Command R, sem pós-processamento nosso."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente COHERE_API_KEY não definida. Veja .env.example.")
    cliente = cohere.ClientV2(api_key=api_key)

    resposta = cliente.chat(
        model=CHAT_MODEL,
        messages=[
            SystemChatMessageV2(role="system", content=SYSTEM_PROMPT),
            UserChatMessageV2(role="user", content=INSTRUCAO),
        ],
        documents=_formatar_documentos(artefatos_recuperados),
        temperature=TEMPERATURE,
    )

    texto = "".join(bloco.text for bloco in resposta.message.content or [])
    citacoes = resposta.message.citations or []
    return texto, citacoes
