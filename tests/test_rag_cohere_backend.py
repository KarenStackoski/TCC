from src.common.schema import Artefato
from src.rag.cohere_backend import _formatar_documentos


def test_formatar_documentos_usa_chave_como_id_e_inclui_metadados():
    artefato = Artefato(
        chave="SCRUM-21",
        titulo="Avaliação do restaurante",
        tipo="História",
        status="Concluído",
        descricao="Como usuário, quero avaliar o restaurante.",
    )
    documentos = _formatar_documentos([artefato])
    assert len(documentos) == 1
    documento = documentos[0]
    assert documento.id == "SCRUM-21"
    assert documento.data["titulo"] == "Avaliação do restaurante"
    assert documento.data["tipo"] == "História"
    assert documento.data["status"] == "Concluído"
    assert "Como usuário, quero avaliar o restaurante." in documento.data["texto"]


def test_formatar_documentos_com_lista_vazia():
    assert _formatar_documentos([]) == []
