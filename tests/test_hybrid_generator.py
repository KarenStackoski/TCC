from cohere.types import Citation, DocumentSource

from src.hybrid.generator import _formatar_citacoes, gerar_manuais


def test_formatar_citacoes_sem_nenhuma_citacao():
    assert _formatar_citacoes({"epic": [], "story": []}) == ""


def test_formatar_citacoes_agrupa_por_titulo_da_secao():
    citacao = Citation(
        start=0,
        end=10,
        text="app trava",
        sources=[DocumentSource(id="SCRUM-7", document={})],
    )
    resultado = _formatar_citacoes({"bug": [citacao], "epic": []})
    assert "Citações (Cohere Command R)" in resultado
    assert "**Problemas Conhecidos:**" in resultado
    assert '"app trava" — fonte(s): SCRUM-7' in resultado


def test_gerar_manuais_com_lista_vazia_nao_chama_nenhuma_api():
    # Sem artefatos, nenhuma categoria tem conteúdo -> gerar_secao_cohere
    # devolve ("", []) sem chamar a API (ver test_hybrid_section_backend.py),
    # então isto roda sem COHERE_API_KEY/ANTHROPIC_API_KEY configuradas.
    manuais = gerar_manuais([], variantes=("cohere",))
    assert "cohere" in manuais
    manual = manuais["cohere"]
    assert "## Visão Geral" in manual
    assert "## Funcionalidades" in manual
    assert "## Tarefas Operacionais" in manual
    assert "## Problemas Conhecidos" in manual
    assert "## Outros Itens" not in manual
