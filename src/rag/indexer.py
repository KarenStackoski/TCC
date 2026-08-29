"""Indexação dos Artefatos no Chroma via embeddings da Cohere.

Fonte do modelo de embedding: Cohere Embed v4 (multilíngue, PT-BR
suportado) — https://docs.cohere.com/docs/embeddings
Fonte do banco vetorial: Chroma — https://docs.trychroma.com/
Ver docs/rag/01_estrutura.md, seção 3.1, para a justificativa de indexar
cada Artefato inteiro como um único chunk (sem fatiamento por tamanho).
"""

from __future__ import annotations

import os
from pathlib import Path

import chromadb
import cohere
from dotenv import load_dotenv

from src.common.schema import Artefato

load_dotenv()

EMBED_MODEL = "embed-v4.0"
COLLECTION_NAME = "artefatos_jira"
CHROMA_PERSIST_DIR = Path(".chroma/rag")


def _get_cohere_client() -> cohere.ClientV2:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente COHERE_API_KEY não definida. Veja .env.example.")
    return cohere.ClientV2(api_key=api_key)


def artefato_para_texto(artefato: Artefato) -> str:
    """Achata um Artefato num único texto — a unidade de indexação/recuperação
    é o artefato inteiro, não um chunk menor (ver docs/rag/01_estrutura.md,
    seção 3.1)."""
    partes = [
        f"{artefato.chave} — {artefato.titulo} ({artefato.tipo}, status: {artefato.status})",
        artefato.descricao,
    ]
    if artefato.criterios_aceitacao:
        criterios = "\n".join(f"- {item}" for item in artefato.criterios_aceitacao)
        partes.append(f"Critérios de aceitação:\n{criterios}")
    elif artefato.subtarefas:
        subtarefas = "\n".join(f"- {s.titulo} ({s.status})" for s in artefato.subtarefas)
        partes.append(f"Subtarefas:\n{subtarefas}")
    return "\n\n".join(parte for parte in partes if parte)


def indexar(artefatos: list[Artefato], persist_dir: Path | str = CHROMA_PERSIST_DIR):
    """Embute cada Artefato (Cohere Embed v4, input_type=search_document) e
    grava (upsert) no Chroma. Devolve a collection já populada."""
    cliente_cohere = _get_cohere_client()
    cliente_chroma = chromadb.PersistentClient(path=str(persist_dir))
    collection = cliente_chroma.get_or_create_collection(COLLECTION_NAME)

    textos = [artefato_para_texto(artefato) for artefato in artefatos]
    resposta = cliente_cohere.embed(
        model=EMBED_MODEL,
        input_type="search_document",
        texts=textos,
        embedding_types=["float"],
    )

    collection.upsert(
        ids=[artefato.chave for artefato in artefatos],
        embeddings=resposta.embeddings.float_,
        documents=textos,
        metadatas=[
            {
                "chave": artefato.chave,
                "titulo": artefato.titulo,
                "tipo": artefato.tipo,
                "status": artefato.status,
            }
            for artefato in artefatos
        ],
    )
    return collection
