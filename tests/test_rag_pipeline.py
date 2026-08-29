from cohere.types import Citation, DocumentSource

from src.rag.pipeline import _formatar_citacoes


def test_formatar_citacoes_com_lista_vazia():
    assert _formatar_citacoes([]) == ""


def test_formatar_citacoes_lista_texto_e_fontes():
    citacao = Citation(
        start=0,
        end=10,
        text="app trava",
        sources=[DocumentSource(id="SCRUM-7", document={})],
    )
    resultado = _formatar_citacoes([citacao])
    assert "Citações (Cohere Command R)" in resultado
    assert '"app trava" — fonte(s): SCRUM-7' in resultado
