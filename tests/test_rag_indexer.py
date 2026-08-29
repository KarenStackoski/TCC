from src.common.schema import Artefato, Subtarefa
from src.rag.indexer import artefato_para_texto


def test_artefato_para_texto_com_criterios_aceitacao():
    artefato = Artefato(
        chave="SCRUM-21",
        titulo="Avaliação do restaurante",
        tipo="História",
        status="Concluído",
        descricao="Como usuário, quero avaliar o restaurante para dar feedback.",
        criterios_aceitacao=["Nota de 1 a 5 estrelas", "Comentário opcional"],
    )
    texto = artefato_para_texto(artefato)
    assert "SCRUM-21 — Avaliação do restaurante (História, status: Concluído)" in texto
    assert "Como usuário, quero avaliar o restaurante para dar feedback." in texto
    assert "Critérios de aceitação:" in texto
    assert "- Nota de 1 a 5 estrelas" in texto
    assert "- Comentário opcional" in texto
    assert "Subtarefas:" not in texto


def test_artefato_para_texto_com_subtarefas_quando_nao_ha_criterios():
    artefato = Artefato(
        chave="SCRUM-5",
        titulo="Configurar ambiente",
        tipo="Task",
        status="Em andamento",
        descricao="Preparar infraestrutura inicial.",
        subtarefas=[Subtarefa(chave="SCRUM-6", titulo="Criar repositório", status="Concluído")],
    )
    texto = artefato_para_texto(artefato)
    assert "Subtarefas:" in texto
    assert "- Criar repositório (Concluído)" in texto
    assert "Critérios de aceitação:" not in texto


def test_artefato_para_texto_sem_criterios_nem_subtarefas():
    artefato = Artefato(
        chave="SCRUM-1",
        titulo="Epic inicial",
        tipo="Epic",
        status="Aberto",
        descricao="Visão geral do projeto.",
    )
    texto = artefato_para_texto(artefato)
    assert texto == "SCRUM-1 — Epic inicial (Epic, status: Aberto)\n\nVisão geral do projeto."
