from src.common.schema import Artefato
from src.rag.retriever import _deduplicar_por_chave


def _artefato(chave: str) -> Artefato:
    return Artefato(chave=chave, titulo=f"Título {chave}", tipo="Story", status="Aberto", descricao="")


def test_deduplicar_por_chave_preserva_primeira_ocorrencia_na_ordem():
    artefatos_por_chave = {chave: _artefato(chave) for chave in ["A-1", "A-2", "A-3"]}
    chaves_por_query = [
        ["A-1", "A-2"],
        ["A-2", "A-3"],
    ]
    resultado = _deduplicar_por_chave(chaves_por_query, artefatos_por_chave)
    assert [artefato.chave for artefato in resultado] == ["A-1", "A-2", "A-3"]


def test_deduplicar_por_chave_sem_sobreposicao():
    artefatos_por_chave = {chave: _artefato(chave) for chave in ["A-1", "A-2"]}
    chaves_por_query = [["A-1"], ["A-2"]]
    resultado = _deduplicar_por_chave(chaves_por_query, artefatos_por_chave)
    assert [artefato.chave for artefato in resultado] == ["A-1", "A-2"]


def test_deduplicar_por_chave_com_listas_vazias():
    assert _deduplicar_por_chave([], {}) == []
    assert _deduplicar_por_chave([[], []], {}) == []
