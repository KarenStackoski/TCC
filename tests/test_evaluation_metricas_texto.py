import pytest

from src.common.schema import Artefato
from src.evaluation import metricas_texto as mt


def _artefato(chave, titulo):
    return Artefato(chave=chave, titulo=titulo, tipo="História", status="Concluído", descricao="")


MANUAL_COM_CITACOES = (
    "# Manual\n\n## Pagamentos\n\nO app aceita Pix. O pagamento é seguro.\n\n---\n\n"
    "**Citações (Cohere Command R):**\n"
    '- "aceita Pix" — fonte(s): SCRUM-18\n'
)


def test_separar_citacoes_tira_rodape_e_regua():
    corpo, rodape = mt.separar_citacoes(MANUAL_COM_CITACOES)
    assert corpo.endswith("O pagamento é seguro.")
    assert rodape.startswith("**Citações")


def test_separar_citacoes_sem_rodape():
    assert mt.separar_citacoes("texto") == ("texto", "")


def test_limpar_markdown_tira_marcacao_e_fecha_titulos():
    limpo = mt.limpar_markdown("## Pagamentos\n\n- **Pix** e [cartão](http://x)\n| a | b |\n|---|---|")
    assert "#" not in limpo and "**" not in limpo and "http" not in limpo
    assert limpo.splitlines()[0] == "Pagamentos."
    assert "Pix e cartão." in limpo


def test_contar_silabas():
    assert mt.contar_silabas("restaurante") == 4
    assert mt.contar_silabas("pedido") == 3
    assert mt.contar_silabas("guarda-chuva") == 4
    assert mt.contar_silabas("PX") == 1  # sem vogal = 1


def test_flesch_segue_formula_de_martins_et_al():
    leg = mt.legibilidade("O pedido chegou. O app funciona.")
    assert leg.frases == 2
    assert leg.palavras == 6
    esperado = 248.835 - 1.015 * (leg.palavras / leg.frases) - 84.6 * (leg.silabas / leg.palavras)
    assert leg.flesch_pt == pytest.approx(esperado, abs=0.01)


def test_legibilidade_de_texto_vazio():
    assert mt.legibilidade("").flesch_pt == 0.0


def test_faixas_flesch():
    assert mt.faixa_flesch(80) == "muito fácil"
    assert mt.faixa_flesch(60) == "fácil"
    assert mt.faixa_flesch(30) == "difícil"
    assert mt.faixa_flesch(10) == "muito difícil"


def test_estrutura_conta_secoes_e_saltos_de_nivel():
    texto = "# T\n\n## A\n\n#### pulo\n\n## B\n\n### ok\n\n- item\n1. item\n| x |"
    est = mt.estrutura(texto)
    assert est.secoes_nivel2 == ["A", "B"]
    assert est.saltos_de_nivel == 1
    assert est.itens_de_lista == 2
    assert est.linhas_de_tabela == 1
    assert est.cabecalhos_por_nivel == {1: 1, 2: 2, 3: 1, 4: 1}


def test_artefatos_mencionados_por_chave_codigo_e_titulo():
    artefatos = [
        _artefato("SCRUM-18", "US-12 — Pagamento com Pix"),
        _artefato("SCRUM-15", "US-09 — Acompanhamento de status do pedido"),
        _artefato("SCRUM-21", "US-15 — Avaliação do restaurante"),
        _artefato("SCRUM-9", "US-03 — Redefinição de senha"),
    ]
    texto = "Veja SCRUM-18. A US-09 trata disso. Faça a avaliacao do restaurante. SCRUM-90 não conta."
    mencoes = mt.artefatos_mencionados(texto, artefatos)
    assert mencoes == {"SCRUM-18": "chave", "SCRUM-15": "codigo", "SCRUM-21": "titulo", "SCRUM-9": ""}
    assert mt.cobertura_explicita(texto, artefatos) == 0.75


def test_chave_nao_casa_prefixo_de_outra_chave():
    artefatos = [_artefato("SCRUM-1", "EP-01 — Autenticação e Cadastro")]
    assert mt.artefatos_mencionados("SCRUM-12", artefatos)["SCRUM-1"] == ""


def test_taxa_texto_citado():
    taxa = mt.taxa_texto_citado(MANUAL_COM_CITACOES)
    corpo, _ = mt.separar_citacoes(MANUAL_COM_CITACOES)
    nao_brancos = sum(1 for c in corpo if not c.isspace())
    assert taxa == pytest.approx(len("aceitaPix") / nao_brancos)


def test_taxa_texto_citado_sem_rodape_e_none():
    assert mt.taxa_texto_citado("# Manual sem citações") is None
