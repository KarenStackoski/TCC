from src.jira.adf_parser import (
    adf_to_markdown,
    extract_bullet_items_after_label,
    strip_section_after_label,
)


def test_adf_to_markdown_com_doc_vazio_ou_none():
    assert adf_to_markdown(None) == ""
    assert adf_to_markdown({"type": "doc", "version": 1, "content": []}) == ""


def test_adf_to_markdown_paragrafo_com_marks_strong_e_texto_simples():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Descrição:", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": " app trava sem internet."},
                ],
            }
        ],
    }
    assert adf_to_markdown(doc) == "**Descrição:** app trava sem internet."


def test_adf_to_markdown_com_em_e_code_marks():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "endpoint afetado ", "marks": []},
                    {
                        "type": "text",
                        "text": "POST /coupons/validate",
                        "marks": [{"type": "code"}],
                    },
                ],
            },
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Como usuário, quero pagar com Pix.",
                                "marks": [{"type": "em"}],
                            }
                        ],
                    }
                ],
            },
        ],
    }
    resultado = adf_to_markdown(doc)
    assert "`POST /coupons/validate`" in resultado
    assert "> *Como usuário, quero pagar com Pix.*" in resultado


def test_adf_to_markdown_bullet_list_vira_lista_markdown():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Item 1"}]}
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Item 2"}]}
                        ],
                    },
                ],
            }
        ],
    }
    assert adf_to_markdown(doc) == "- Item 1\n- Item 2"


def test_extract_bullet_items_after_label_estrutura_real_de_story():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Critérios de aceitação:",
                        "marks": [{"type": "strong"}],
                    }
                ],
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Avaliação disponível por até 7 dias após entrega",
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Apenas uma avaliação por pedido",
                                    }
                                ],
                            }
                        ],
                    },
                ],
            },
        ],
    }
    assert extract_bullet_items_after_label(doc, "Critérios de aceitação") == [
        "Avaliação disponível por até 7 dias após entrega",
        "Apenas uma avaliação por pedido",
    ]


def test_extract_bullet_items_after_label_quando_label_nao_existe():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Descrição sem critérios."}],
            }
        ],
    }
    assert extract_bullet_items_after_label(doc, "Critérios de aceitação") == []


def test_extract_bullet_items_after_label_com_doc_none():
    assert extract_bullet_items_after_label(None, "Critérios de aceitação") == []


def test_strip_section_after_label_remove_paragrafo_e_lista_correspondentes():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Descrição da história."}],
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Critérios de aceitação:",
                        "marks": [{"type": "strong"}],
                    }
                ],
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": "Critério 1"}],
                            }
                        ],
                    }
                ],
            },
        ],
    }
    resultado = strip_section_after_label(doc, "Critérios de aceitação")
    assert adf_to_markdown(resultado) == "Descrição da história."
    assert extract_bullet_items_after_label(doc, "Critérios de aceitação") == ["Critério 1"]


def test_strip_section_after_label_quando_label_nao_existe_mantem_doc_igual():
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Descrição sem critérios."}],
            }
        ],
    }
    assert strip_section_after_label(doc, "Critérios de aceitação") == doc


def test_strip_section_after_label_com_doc_none():
    assert strip_section_after_label(None, "Critérios de aceitação") is None
