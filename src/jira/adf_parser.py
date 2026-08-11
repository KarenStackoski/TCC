"""Parser do Atlassian Document Format (ADF).

O campo `description` das issues do Jira Cloud vem como uma árvore JSON
(ADF), não como texto puro. Este módulo converte essa árvore em texto
Markdown por percurso recursivo dos nós, seguindo a estrutura documentada
em https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/.
"""

from __future__ import annotations

_LIST_NODE_TYPES = ("bulletList", "orderedList")


def _text_with_marks(node: dict) -> str:
    text = node.get("text", "")
    mark_types = {mark.get("type") for mark in node.get("marks", []) or []}
    if "code" in mark_types:
        text = f"`{text}`"
    if "strong" in mark_types:
        text = f"**{text}**"
    if "em" in mark_types:
        text = f"*{text}*"
    if "strike" in mark_types:
        text = f"~~{text}~~"
    return text


def _inline_content_to_text(nodes: list[dict]) -> str:
    parts = []
    for node in nodes:
        node_type = node.get("type")
        if node_type == "text":
            parts.append(_text_with_marks(node))
        elif node_type == "hardBreak":
            parts.append("\n")
        else:
            parts.append(_inline_content_to_text(node.get("content", []) or []))
    return "".join(parts)


def _list_item_text(list_item: dict) -> str:
    paragraphs = [
        _inline_content_to_text(child.get("content", []) or [])
        for child in list_item.get("content", []) or []
        if child.get("type") == "paragraph"
    ]
    return " ".join(part.strip() for part in paragraphs if part.strip())


def _list_items_to_lines(list_node: dict, ordered: bool) -> list[str]:
    lines = []
    for index, item in enumerate(list_node.get("content", []) or [], start=1):
        item_text = _list_item_text(item)
        prefix = f"{index}. " if ordered else "- "
        lines.append(f"{prefix}{item_text}")
    return lines


def _block_node_to_lines(node: dict) -> list[str]:
    node_type = node.get("type")

    if node_type == "paragraph":
        return [_inline_content_to_text(node.get("content", []) or [])]

    if node_type == "heading":
        level = node.get("attrs", {}).get("level", 1)
        text = _inline_content_to_text(node.get("content", []) or [])
        return [f"{'#' * level} {text}"]

    if node_type == "blockquote":
        inner_lines = []
        for child in node.get("content", []) or []:
            inner_lines.extend(_block_node_to_lines(child))
        return [f"> {line}" for line in inner_lines]

    if node_type == "bulletList":
        return _list_items_to_lines(node, ordered=False)

    if node_type == "orderedList":
        return _list_items_to_lines(node, ordered=True)

    if node_type == "codeBlock":
        text = _inline_content_to_text(node.get("content", []) or [])
        return [f"```\n{text}\n```"]

    if node_type == "rule":
        return ["---"]

    lines = []
    for child in node.get("content", []) or []:
        lines.extend(_block_node_to_lines(child))
    return lines


def adf_to_markdown(adf_doc: dict | None) -> str:
    """Converte um documento ADF completo (`fields.description`) em Markdown."""
    if not adf_doc:
        return ""
    blocks = []
    for node in adf_doc.get("content", []) or []:
        lines = _block_node_to_lines(node)
        if lines:
            blocks.append("\n".join(lines))
    return "\n\n".join(blocks).strip()


def _normalize_label(text: str) -> str:
    return text.strip().strip("*").rstrip(":").strip().casefold()


def extract_bullet_items_after_label(adf_doc: dict | None, label: str) -> list[str]:
    """Devolve os itens da lista (bullet/ordered) que vem logo após um
    parágrafo cujo texto bate com `label` (ex.: "Critérios de aceitação").

    Usado para artefatos que seguem o padrão User Story + Acceptance
    Criteria (Cohn, 2004) em vez de subtarefas — ver docs/templating/01_estrutura.md.
    """
    if not adf_doc:
        return []
    normalized_label = _normalize_label(label)
    top_level = adf_doc.get("content", []) or []
    for index, node in enumerate(top_level):
        if node.get("type") != "paragraph":
            continue
        paragraph_text = _inline_content_to_text(node.get("content", []) or [])
        if _normalize_label(paragraph_text) != normalized_label:
            continue
        if index + 1 >= len(top_level):
            return []
        next_node = top_level[index + 1]
        if next_node.get("type") not in _LIST_NODE_TYPES:
            return []
        return [
            _list_item_text(item)
            for item in next_node.get("content", []) or []
            if _list_item_text(item)
        ]
    return []


def strip_section_after_label(adf_doc: dict | None, label: str) -> dict | None:
    """Remove, no nível superior do documento, o parágrafo `label` e a
    lista logo em seguida (se houver).

    Complementa `extract_bullet_items_after_label`: o chamador extrai os
    itens para um campo próprio (`Artefato.criterios_aceitacao`) e usa
    esta função para tirar a mesma seção do texto corrido da descrição,
    evitando que a lista apareça duplicada no manual final.
    """
    if not adf_doc:
        return adf_doc
    normalized_label = _normalize_label(label)
    top_level = adf_doc.get("content", []) or []
    for index, node in enumerate(top_level):
        if node.get("type") != "paragraph":
            continue
        paragraph_text = _inline_content_to_text(node.get("content", []) or [])
        if _normalize_label(paragraph_text) != normalized_label:
            continue
        restante_apos_label = index + 1
        if (
            restante_apos_label < len(top_level)
            and top_level[restante_apos_label].get("type") in _LIST_NODE_TYPES
        ):
            restante_apos_label += 1
        novo_content = top_level[:index] + top_level[restante_apos_label:]
        return {**adf_doc, "content": novo_content}
    return adf_doc
