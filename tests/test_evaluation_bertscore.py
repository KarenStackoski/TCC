"""Confere que a implementação por janelas de src/evaluation/bertscore.py dá
o mesmo resultado que o pacote oficial `bert_score` quando o texto cabe numa
janela só. Precisa do modelo já baixado (~700 MB); sem ele, o teste é pulado."""

import pytest

from src.evaluation.bertscore import CAMADA, MODELO, Avaliador, pontuar_embeddings


@pytest.fixture(scope="module")
def avaliador():
    from transformers import AutoModel

    try:
        AutoModel.from_pretrained(MODELO, local_files_only=True)
    except OSError:
        pytest.skip(f"Modelo {MODELO} não está no cache local.")
    return Avaliador()


def test_igual_ao_bert_score_oficial_para_texto_curto(avaliador):
    from bert_score import score

    candidato = "O usuário pode acompanhar o pedido em tempo real pelo mapa."
    referencia = "A tela de rastreamento mostra a posição do entregador no mapa."
    p, r, f = score([candidato], [referencia], model_type=MODELO, num_layers=CAMADA, idf=False)
    nosso = pontuar_embeddings(avaliador.embeddings(candidato), avaliador.embeddings(referencia))
    assert nosso.precisao == pytest.approx(p.item(), abs=1e-4)
    assert nosso.revocacao == pytest.approx(r.item(), abs=1e-4)
    assert nosso.f1 == pytest.approx(f.item(), abs=1e-4)


def test_texto_longo_usa_varias_janelas(avaliador):
    longo = "O pedido saiu para entrega. " * 200  # bem mais que 512 tokens
    vetores = avaliador.embeddings(longo)
    n_tokens = len(avaliador.tokenizer(longo, add_special_tokens=False)["input_ids"])
    assert vetores.shape[0] == n_tokens
