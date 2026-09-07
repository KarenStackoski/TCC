"""Geração de texto por seção — motor da Etapa 3 (Híbrido).

Ao contrário da Etapa 2 (`src/rag/cohere_backend.py`, `src/rag/claude_backend.py`),
onde a LLM decide livremente estrutura e conteúdo do manual inteiro, aqui a
estrutura já está decidida (as categorias fixas de `src/templating/generator.py`)
e cada chamada de LLM escreve só o corpo de UMA seção, a partir dos artefatos
já classificados naquela categoria. Ver docs/hybrid/01_estrutura.md, seção 3.2,
para a justificativa completa (Reiter & Dale, 2000 — document planning fixo,
microplanning/realization delegados à LLM por seção).

Fonte do backend Cohere (grounded generation + citações via `documents=`):
https://docs.cohere.com/docs/retrieval-augmented-generation-rag
Fonte do backend Claude (documentos em XML, conteúdo antes da instrução):
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
"""

from __future__ import annotations

import os

import anthropic
import cohere
from cohere.types import Citation, Document, SystemChatMessageV2, UserChatMessageV2
from dotenv import load_dotenv

from src.common.schema import Artefato
from src.rag.indexer import artefato_para_texto

load_dotenv()

COHERE_CHAT_MODEL = "command-r-08-2024"
CLAUDE_CHAT_MODEL = "claude-sonnet-5"
CLAUDE_MAX_TOKENS = 4096
TEMPERATURE = 0.3

SYSTEM_PROMPT_HIBRIDO = (
    "Você é um redator técnico responsável por reescrever, em prosa clara e "
    "natural, UMA seção específica de um manual de usuário de software, a "
    "partir de artefatos de gestão de projeto (Jira) já classificados nessa "
    "seção. Escreva em português do Brasil, em Markdown. Escreva apenas o "
    "corpo da seção: não inclua um cabeçalho (ex.: não escreva '## "
    "Funcionalidades'), pois o cabeçalho já é definido pela estrutura fixa "
    "do documento. Não invente fatos que não estejam nos documentos "
    "fornecidos. Seja conciso: no máximo 2 a 3 frases por artefato, sem "
    "repetir o mesmo fato de formas diferentes — o modelo tem um limite "
    "rígido de tokens de saída (Cohere, Chat API reference — max_tokens: "
    "https://docs.cohere.com/reference/chat) e a seção precisa cobrir TODOS "
    "os artefatos fornecidos dentro desse limite. Se for usar subtítulos "
    "dentro da seção (por exemplo, um por artefato ou por grupo de "
    "artefatos), use nível 3 (`###`) ou mais profundo — nunca nível 2 "
    "(`##`), que é o nível já usado pelo cabeçalho fixo da seção."
)

# categoria (de src.templating.generator.classificar_por_tipo) -> (título da
# seção no manual final, instrução específica da LLM para essa seção).
# Ordem = ordem das seções no manual, mesma ordem de manual_template.md.j2
# (Etapa 1) — ver docs/hybrid/01_estrutura.md, seção 3.3.
SECTION_CONFIG: dict[str, tuple[str, str]] = {
    "epic": (
        "Visão Geral",
        "Usando os Epics abaixo (os grandes temas/módulos do produto), "
        "escreva a seção 'Visão Geral' do manual: uma apresentação do "
        "produto e do que ele oferece, sem entrar em passo a passo. "
        "Baseie-se só nos documentos fornecidos.",
    ),
    "story": (
        "Funcionalidades",
        "Usando as Histórias de Usuário abaixo, escreva a seção "
        "'Funcionalidades' do manual: para cada uma, um parágrafo curto "
        "descrevendo o que a funcionalidade permite fazer e os passos "
        "principais para usá-la, resumindo os Critérios de Aceitação (ou "
        "as Subtarefas, quando não houver critérios) em vez de listar cada "
        "um por extenso. Baseie-se só nos documentos fornecidos.",
    ),
    "task": (
        "Tarefas Operacionais",
        "Usando os itens abaixo, escreva a seção 'Tarefas Operacionais' do "
        "manual, explicando o que cada um envolve e como ele afeta o uso do "
        "produto. Baseie-se só nos documentos fornecidos.",
    ),
    "bug": (
        "Problemas Conhecidos",
        "Usando os bugs abaixo, escreva a seção 'Problemas Conhecidos' do "
        "manual em prosa corrida (não use tabela). Para cada problema, "
        "mencione claramente a chave do Jira, o título e o status atual, "
        "para que o leitor consiga rastrear o item na ferramenta de gestão. "
        "Baseie-se só nos documentos fornecidos.",
    ),
    "outros": (
        "Outros Itens",
        "Usando os itens abaixo (artefatos que não se encaixam nas "
        "categorias principais do manual), escreva uma seção breve 'Outros "
        "Itens' descrevendo cada um. Baseie-se só nos documentos "
        "fornecidos.",
    ),
}


def _formatar_documentos_cohere(artefatos: list[Artefato]) -> list[Document]:
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


def gerar_secao_cohere(categoria: str, artefatos: list[Artefato]) -> tuple[str, list[Citation]]:
    """Gera o texto (e citações) de UMA seção via Cohere Command R, a partir
    só dos artefatos daquela categoria. Devolve ("", []) se a categoria não
    tiver artefatos (seção fica vazia, sem chamar a API)."""
    if not artefatos:
        return "", []

    _, instrucao = SECTION_CONFIG[categoria]
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente COHERE_API_KEY não definida. Veja .env.example.")
    cliente = cohere.ClientV2(api_key=api_key)

    resposta = cliente.chat(
        model=COHERE_CHAT_MODEL,
        messages=[
            SystemChatMessageV2(role="system", content=SYSTEM_PROMPT_HIBRIDO),
            UserChatMessageV2(role="user", content=instrucao),
        ],
        documents=_formatar_documentos_cohere(artefatos),
        temperature=TEMPERATURE,
    )

    texto = "".join(bloco.text for bloco in resposta.message.content or [])
    citacoes = resposta.message.citations or []
    return texto, citacoes


def _montar_documento_xml_claude(indice: int, artefato: Artefato) -> str:
    fonte = f"{artefato.chave} — {artefato.titulo} ({artefato.tipo})"
    return (
        f'<document index="{indice}">\n'
        f"<source>{fonte}</source>\n"
        f"<document_content>\n{artefato_para_texto(artefato)}\n</document_content>\n"
        f"</document>"
    )


def montar_prompt_claude(categoria: str, artefatos: list[Artefato]) -> str:
    """Monta o prompt da seção para o Claude — documentos primeiro, instrução
    por último (mesma fonte de src/rag/claude_backend.py). Função pura, sem
    chamada de API, para ser testável isoladamente."""
    _, instrucao = SECTION_CONFIG[categoria]
    documentos_xml = "\n".join(
        _montar_documento_xml_claude(indice, artefato)
        for indice, artefato in enumerate(artefatos, start=1)
    )
    return f"<documents>\n{documentos_xml}\n</documents>\n\n{instrucao}"


def gerar_secao_claude(categoria: str, artefatos: list[Artefato]) -> str:
    """Gera o texto de UMA seção via Claude (Messages API). Implementado e
    testado (função pura `montar_prompt_claude`), mas não executado nesta
    sessão — decisão de não usar a API paga da Anthropic por enquanto (mesma
    decisão da Etapa 2, ver docs/PROGRESSO.md)."""
    if not artefatos:
        return ""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Variável de ambiente ANTHROPIC_API_KEY não definida. Veja .env.example.")
    cliente = anthropic.Anthropic(api_key=api_key)

    resposta = cliente.messages.create(
        model=CLAUDE_CHAT_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        temperature=TEMPERATURE,
        system=SYSTEM_PROMPT_HIBRIDO,
        messages=[{"role": "user", "content": montar_prompt_claude(categoria, artefatos)}],
    )

    return "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
