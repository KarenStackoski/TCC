from src.common.schema import Artefato
from src.hybrid.section_backend import (
    SECTION_CONFIG,
    gerar_secao_claude,
    gerar_secao_cohere,
    montar_prompt_claude,
)


def test_section_config_cobre_as_cinco_categorias_de_classificar_por_tipo():
    # Mesmas chaves devolvidas por src.templating.generator.classificar_por_tipo,
    # para nenhuma categoria ficar sem seção/instrução no manual híbrido.
    assert set(SECTION_CONFIG.keys()) == {"epic", "story", "task", "bug", "outros"}
    for titulo, instrucao in SECTION_CONFIG.values():
        assert titulo
        assert instrucao


def test_gerar_secao_cohere_com_lista_vazia_nao_chama_api():
    texto, citacoes = gerar_secao_cohere("bug", [])
    assert texto == ""
    assert citacoes == []


def test_gerar_secao_claude_com_lista_vazia_nao_chama_api():
    assert gerar_secao_claude("bug", []) == ""


def test_montar_prompt_claude_usa_instrucao_da_categoria():
    artefato = Artefato(
        chave="SCRUM-1",
        titulo="Epic inicial",
        tipo="Epic",
        status="Aberto",
        descricao="Visão geral do projeto.",
    )
    _, instrucao_epic = SECTION_CONFIG["epic"]
    prompt = montar_prompt_claude("epic", [artefato])
    assert prompt.startswith("<documents>")
    assert '<document index="1">' in prompt
    assert "<source>SCRUM-1 — Epic inicial (Epic)</source>" in prompt
    assert prompt.rstrip().endswith(instrucao_epic)
    assert prompt.index("</documents>") < prompt.index(instrucao_epic)


def test_montar_prompt_claude_troca_instrucao_conforme_categoria():
    _, instrucao_bug = SECTION_CONFIG["bug"]
    prompt = montar_prompt_claude("bug", [])
    assert prompt == f"<documents>\n\n</documents>\n\n{instrucao_bug}"
