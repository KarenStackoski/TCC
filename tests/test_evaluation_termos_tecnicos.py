from src.evaluation.termos_tecnicos import carregar_glossario, medir

GLOSSARIO = {"api": "estrito", "skeleton": "estrito", "skeleton loading": "estrito", "status": "amplo"}


def test_conta_por_100_palavras_nos_dois_niveis():
    v = medir("A API mudou o status do pedido hoje de manhã.", GLOSSARIO)
    assert v.palavras == 10
    assert v.ocorrencias_estrito == 1
    assert v.ocorrencias_amplo == 2
    assert v.termos_estrito_100p == 10.0
    assert v.termos_amplo_100p == 20.0


def test_termo_composto_conta_uma_vez_e_nao_casa_parte_de_palavra():
    v = medir("Skeleton loading aparece. A rapidez e a terapia não contam.", GLOSSARIO)
    assert v.por_termo == {"skeleton loading": 1}


def test_proporcao_de_frases_e_codigos_internos():
    v = medir("A API caiu. O pedido chegou. Ver SCRUM-12 e US-15.", GLOSSARIO)
    assert v.frases_com_termo_estrito_pct == 33.3
    assert v.ocorrencias_estrito == 1
    assert v.codigos_100p > 0


def test_ignora_rodape_de_citacoes():
    texto = 'O pedido chegou.\n\n---\n\n**Citações (Cohere Command R):**\n\n- "API" — fonte(s): SCRUM-1\n'
    assert medir(texto, GLOSSARIO).ocorrencias_estrito == 0


def test_glossario_do_projeto_so_tem_niveis_validos():
    assert set(carregar_glossario().values()) == {"estrito", "amplo"}
