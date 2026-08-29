"""Recuperação (retrieval) via busca semântica no Chroma.

Cada query representa uma pergunta típica de quem lê um manual de usuário —
a Etapa 2 gera um documento inteiro, não responde a uma pergunta livre de
usuário, então as queries guiam o que entra no contexto, não como ele é
apresentado (isso continua a cargo da LLM de geração). Ver
docs/rag/01_estrutura.md, seção 3.2, inclusive a ressalva metodológica
sobre o efeito de filtragem ser menor num corpus de só 32 artefatos.
Fonte da técnica de RAG: Lewis, P., et al. (2020). "Retrieval-Augmented
Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020.
"""

from __future__ import annotations

import os

import cohere
from dotenv import load_dotenv

from src.common.schema import Artefato

load_dotenv()

EMBED_MODEL = "embed-v4.0"
TOP_K_POR_QUERY = 6

QUERIES_PADRAO = [
    "Visão geral do produto: quais são os principais objetivos e iniciativas (epics)?",
    "Quais funcionalidades estão disponíveis para o usuário final e como usá-las?",
    "Quais tarefas operacionais ou configurações administrativas o sistema oferece?",
    "Quais problemas, bugs ou limitações conhecidas existem no sistema?",
]


def _get_cohere_client() -> cohere.ClientV2:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente COHERE_API_KEY não definida. Veja .env.example.")
    return cohere.ClientV2(api_key=api_key)


def _deduplicar_por_chave(
    chaves_por_query: list[list[str]], artefatos_por_chave: dict[str, Artefato]
) -> list[Artefato]:
    """Preserva só a primeira ocorrência de cada chave, na ordem em que foi
    recuperada (uma query anterior "ganha" de uma posterior)."""
    chaves_vistas: set[str] = set()
    recuperados: list[Artefato] = []
    for chaves in chaves_por_query:
        for chave in chaves:
            if chave not in chaves_vistas:
                chaves_vistas.add(chave)
                recuperados.append(artefatos_por_chave[chave])
    return recuperados


def recuperar(
    collection,
    artefatos_por_chave: dict[str, Artefato],
    queries: list[str] = QUERIES_PADRAO,
    top_k: int = TOP_K_POR_QUERY,
) -> list[Artefato]:
    """Roda uma busca por similaridade para cada query e devolve os Artefato
    originais recuperados (não o texto achatado guardado no Chroma),
    deduplicados por chave."""
    cliente_cohere = _get_cohere_client()
    resposta = cliente_cohere.embed(
        model=EMBED_MODEL,
        input_type="search_query",
        texts=queries,
        embedding_types=["float"],
    )

    chaves_por_query = []
    for vetor_query in resposta.embeddings.float_:
        resultado = collection.query(query_embeddings=[vetor_query], n_results=top_k)
        chaves_por_query.append(resultado["ids"][0])

    return _deduplicar_por_chave(chaves_por_query, artefatos_por_chave)
