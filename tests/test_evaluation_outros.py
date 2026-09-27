"""Testes das partes determinísticas dos módulos de avaliação — sem chamar
API nem baixar modelo."""

import csv
from types import SimpleNamespace

import cohere
import pytest
import torch

from src.common.schema import Artefato
from src.evaluation import avaliacao_humana as ah
from src.evaluation import fidelidade
from src.evaluation.benchmark import resumir
from src.evaluation.bertscore import pontuar_embeddings
from src.evaluation.juiz_llm import montar_prompt, validar
from src.evaluation.medicao import RegistroChamadas
from src.evaluation.variacao import similaridade, variacao

# --- medicao -----------------------------------------------------------------


def test_registro_chamadas_classifica_fases_e_soma_tokens(monkeypatch):
    def chat_falso(self, **kwargs):
        billed = SimpleNamespace(input_tokens=100, output_tokens=40)
        return SimpleNamespace(usage=SimpleNamespace(billed_units=billed))

    def embed_falso(self, **kwargs):
        return SimpleNamespace(meta=SimpleNamespace(billed_units=SimpleNamespace(input_tokens=7)))

    monkeypatch.setattr(cohere.ClientV2, "chat", chat_falso)
    monkeypatch.setattr(cohere.ClientV2, "embed", embed_falso)
    with RegistroChamadas() as registro:
        # O cliente é criado dentro do bloco, como nos backends reais (ver
        # docstring de RegistroChamadas).
        cliente = cohere.ClientV2(api_key="teste")
        cliente.embed(input_type="search_document", texts=["a"])
        cliente.embed(input_type="search_query", texts=["b"])
        cliente.chat(model="x", messages=[])

    assert [c.fase for c in registro.chamadas] == ["indexacao", "recuperacao", "geracao"]
    assert registro.total_tokens() == (114, 40)  # 7 + 7 (embeds) + 100 (chat)
    assert set(registro.tempo_por_fase()) == {"indexacao", "recuperacao", "geracao"}
    # Ao sair do bloco, os métodos originais voltam.
    assert cohere.ClientV2.chat is chat_falso
    assert cohere.ClientV2.embed is embed_falso


def test_resumir_calcula_mediana_e_extremos():
    linhas = [
        {"metodo": "rag", "tempo_total_s": t, "tokens_entrada": 10, "tokens_saida": 5}
        for t in (3.0, 1.0, 2.0)
    ]
    (item,) = resumir(linhas)
    assert item["mediana_s"] == 2.0
    assert (item["min_s"], item["max_s"]) == (1.0, 3.0)
    assert item["desvio_padrao_s"] == 1.0
    assert item["mediana_tokens"] == 15


# --- variacao ----------------------------------------------------------------


def test_variacao_de_textos_identicos():
    v = variacao(["## A\n\ntexto igual"] * 3)
    assert v.textos_distintos == 1
    assert v.estruturas_distintas == 1
    assert v.similaridade_minima == 1.0


def test_variacao_detecta_estrutura_diferente():
    v = variacao(["## A\n\num dois", "## B\n\num dois"])
    assert v.estruturas_distintas == 2
    assert v.textos_distintos == 2


def test_similaridade_ignora_rodape_de_citacoes():
    base = "## A\n\ntexto"
    com_rodape = base + '\n\n---\n\n**Citações (Cohere Command R):**\n- "texto" — fonte(s): SCRUM-1'
    assert similaridade(base, com_rodape) == 1.0


def test_variacao_exige_duas_execucoes():
    with pytest.raises(ValueError):
        variacao(["so uma"])


# --- bertscore ---------------------------------------------------------------


def test_pontuar_embeddings_textos_iguais_da_1():
    e = torch.nn.functional.normalize(torch.randn(5, 8), dim=-1)
    assert pontuar_embeddings(e, e).f1 == pytest.approx(1.0, abs=1e-4)


def test_pontuar_embeddings_precisao_e_revocacao():
    # candidato: 2 tokens; referência: 1 token igual ao primeiro candidato.
    c = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    r = torch.tensor([[1.0, 0.0]])
    bs = pontuar_embeddings(c, r)
    assert bs.precisao == 0.5  # (1 + 0) / 2
    assert bs.revocacao == 1.0
    assert bs.f1 == pytest.approx(2 * 0.5 / 1.5, abs=1e-4)


# --- avaliacao humana --------------------------------------------------------


def test_anonimizar_tira_rodape_e_linha_da_etapa():
    texto = (
        "# Manual\n\n_Documento gerado automaticamente — Etapa 1 do TCC._\n\n## A\n\nx"
        '\n\n---\n\n**Citações (Cohere Command R):**\n- "x" — fonte(s): SCRUM-1'
    )
    anonimo = ah.anonimizar(texto)
    assert "Etapa 1" not in anonimo
    assert "Citações" not in anonimo
    assert anonimo == "# Manual\n\n## A\n\nx\n"


def test_sortear_letras_e_reprodutivel():
    metodos = ["hibrido", "manual", "rag", "templating"]
    assert ah.sortear_letras(metodos, 7) == ah.sortear_letras(metodos, 7)
    assert sorted(ah.sortear_letras(metodos, 7).values()) == metodos


def test_preparar_e_analisar(tmp_path):
    manuais = {}
    for metodo in ("rag", "templating"):
        caminho = tmp_path / f"{metodo}.md"
        caminho.write_text(f"# {metodo}", encoding="utf-8")
        manuais[metodo] = str(caminho)
    manuais["manual"] = str(tmp_path / "nao_existe.md")

    gabarito = ah.preparar(manuais, semente=1, saida_dir=tmp_path / "av")
    assert sorted(gabarito.values()) == ["rag", "templating"]
    assert (tmp_path / "av" / "manuais" / "manual_A.md").exists()

    criterios = list(ah.CRITERIOS)
    for avaliador, notas in (("ana", {"A": 5, "B": 2}), ("bia", {"A": 4, "B": 2})):
        with open(tmp_path / "av" / "respostas" / f"{avaliador}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["avaliador", "manual", *criterios, "comentario"])
            for letra, nota in notas.items():
                w.writerow([avaliador, letra, *[nota] * len(criterios), ""])

    resumo, concordancia = ah.analisar(tmp_path / "av")
    por_letra = {linha["manual"]: linha for linha in resumo}
    assert por_letra["A"]["clareza_media"] == 4.5
    assert por_letra["B"]["clareza_mediana"] == 2.0
    assert concordancia["avaliadores"] == 2
    assert -1.0 <= concordancia["alfa_krippendorff_ordinal"] <= 1.0


def test_alfa_com_concordancia_perfeita_e_1():
    respostas = [
        {"avaliador": a, "manual": m, "clareza": n}
        for a in ("x", "y")
        for m, n in (("A", "1"), ("B", "3"), ("C", "5"))
    ]
    assert ah.alfa_ordinal(respostas, ["clareza"]) == pytest.approx(1.0)


def test_alfa_com_um_avaliador_e_none():
    assert ah.alfa_ordinal([{"avaliador": "x", "manual": "A", "clareza": "3"}], ["clareza"]) is None


# --- fidelidade --------------------------------------------------------------


def test_analisar_planilha_de_fidelidade():
    linhas = [
        {"id": "1", "rotulo": "S", "artefatos": "SCRUM-1, SCRUM-2"},
        {"id": "2", "rotulo": "n", "artefatos": ""},
        {"id": "3", "rotulo": "P", "artefatos": "SCRUM-2"},
        {"id": "4", "rotulo": "-", "artefatos": ""},
    ]
    r = fidelidade.analisar_planilha(linhas, total_artefatos=4)
    assert r["frases_verificaveis"] == 3
    assert r["sustentadas_%"] == pytest.approx(33.3)
    assert r["nao_sustentadas_%"] == pytest.approx(33.3)
    assert r["artefatos_cobertos"] == 2
    assert r["cobertura_conteudo_%"] == 50.0


def test_analisar_planilha_recusa_rotulo_vazio():
    with pytest.raises(ValueError):
        fidelidade.analisar_planilha([{"id": "1", "rotulo": "", "artefatos": ""}], 1)


def test_preparar_fidelidade_nao_sobrescreve_anotacao(tmp_path):
    manual = tmp_path / "m.md"
    manual.write_text("## A\n\nPrimeira frase. Segunda frase.", encoding="utf-8")
    contagem = fidelidade.preparar({"rag": str(manual)}, saida_dir=tmp_path / "f")
    assert contagem == {"rag": 3}  # título "A." + duas frases
    planilha = tmp_path / "f" / "rag.csv"
    planilha.write_text("anotado", encoding="utf-8")
    fidelidade.preparar({"rag": str(manual)}, saida_dir=tmp_path / "f")
    assert planilha.read_text(encoding="utf-8") == "anotado"


# --- juiz LLM ----------------------------------------------------------------


def test_montar_prompt_do_juiz_inclui_fontes_manual_e_criterios():
    artefato = Artefato(chave="SCRUM-1", titulo="EP-01 — Login", tipo="Epic", status="Feito", descricao="Entrar.")
    prompt = montar_prompt("# Manual", [artefato])
    assert prompt.index("<artefatos_de_origem>") < prompt.index("<manual>")
    assert "SCRUM-1" in prompt
    for criterio in ah.CRITERIOS:
        assert criterio in prompt


def test_validar_recusa_nota_fora_da_escala():
    resposta = {c: {"justificativa": "", "nota": 3} for c in ah.CRITERIOS}
    resposta["afirmacoes_nao_sustentadas"] = []
    assert validar(resposta) is resposta
    resposta["clareza"]["nota"] = 7
    with pytest.raises(ValueError):
        validar(resposta)
