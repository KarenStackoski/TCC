from src.common.schema import Artefato
from src.rag.claude_backend import INSTRUCAO, montar_prompt


def test_montar_prompt_com_doc_unico():
    artefato = Artefato(
        chave="SCRUM-1",
        titulo="Epic inicial",
        tipo="Epic",
        status="Aberto",
        descricao="Visão geral do projeto.",
    )
    prompt = montar_prompt([artefato])
    assert prompt.startswith("<documents>")
    assert '<document index="1">' in prompt
    assert "<source>SCRUM-1 — Epic inicial (Epic)</source>" in prompt
    assert "Visão geral do projeto." in prompt
    assert prompt.rstrip().endswith(INSTRUCAO)
    # documentos vêm antes da instrução, não depois
    assert prompt.index("</documents>") < prompt.index(INSTRUCAO)


def test_montar_prompt_numera_documentos_em_ordem():
    artefatos = [
        Artefato(chave=f"A-{i}", titulo=f"Título {i}", tipo="Story", status="Aberto", descricao="")
        for i in range(1, 4)
    ]
    prompt = montar_prompt(artefatos)
    assert '<document index="1">' in prompt
    assert '<document index="2">' in prompt
    assert '<document index="3">' in prompt
    assert prompt.index('index="1"') < prompt.index('index="2"') < prompt.index('index="3"')


def test_montar_prompt_com_lista_vazia():
    prompt = montar_prompt([])
    assert prompt == f"<documents>\n\n</documents>\n\n{INSTRUCAO}"
