"""Testes das partes determinísticas dos módulos de avaliação — sem chamar
API nem baixar modelo."""

import csv
from types import SimpleNamespace

import cohere
import pytest
import torch

from src.common.schema import Artefato
from src.evaluation import estatistica, fidelidade, reanotacao
from src.evaluation.benchmark import resumir
from src.evaluation.bertscore import pontuar_embeddings
from src.evaluation.juiz_llm import CRITERIOS, arquivos_das_execucoes, montar_prompt, validar
from src.evaluation.manuais import anonimizar
from src.evaluation.medicao import RegistroChamadas
from src.evaluation.relatorio import dados_por_execucao, resumo_juiz
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


# --- manuais ------------------------------------------------------------------


def test_anonimizar_tira_rodape_e_linha_da_etapa():
    texto = (
        "# Manual\n\n_Documento gerado automaticamente — Etapa 1 do TCC._\n\n## A\n\nx"
        '\n\n---\n\n**Citações (Cohere Command R):**\n- "x" — fonte(s): SCRUM-1'
    )
    anonimo = anonimizar(texto)
    assert "Etapa 1" not in anonimo
    assert "Citações" not in anonimo
    assert anonimo == "# Manual\n\n## A\n\nx\n"


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


ARTEFATOS_FIDELIDADE = [
    Artefato(chave="SCRUM-4", titulo="EP-04 — Pagamentos", tipo="Epic", status="Feito", descricao="Pagar."),
    Artefato(chave="SCRUM-18", titulo="US-12 — Pagamento com Pix", tipo="História", status="Feito", descricao="Pix."),
    Artefato(chave="SCRUM-26", titulo="BUG-04 — Atraso", tipo="Bug", status="Feito", descricao="Atraso."),
]


def _ler_planilha(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def test_preparar_fidelidade_nao_sobrescreve_anotacao(tmp_path):
    manual = tmp_path / "m.md"
    manual.write_text("## A\n\nPrimeira frase. Segunda frase.", encoding="utf-8")
    contagem = fidelidade.preparar({"rag": str(manual)}, ARTEFATOS_FIDELIDADE, saida_dir=tmp_path / "f")
    assert contagem == {"rag": 3}  # título "A." + duas frases
    assert (tmp_path / "f" / "artefatos_referencia.md").read_text(encoding="utf-8").count("## SCRUM-") == 3
    planilha = tmp_path / "f" / "rag.csv"
    # Só o pré-preenchimento: pode ser refeita.
    assert fidelidade.preparar({"rag": str(manual)}, ARTEFATOS_FIDELIDADE, saida_dir=tmp_path / "f") == {"rag": 3}
    linhas = _ler_planilha(planilha)
    linhas[1]["rotulo"] = "S"
    with open(planilha, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=fidelidade.CAMPOS)
        escritor.writeheader()
        escritor.writerows(linhas)
    assert fidelidade.preparar({"rag": str(manual)}, ARTEFATOS_FIDELIDADE, saida_dir=tmp_path / "f") == {}
    assert _ler_planilha(planilha)[1]["rotulo"] == "S"


def test_frases_para_anotar_secao_titulos_e_fontes():
    texto = (
        "# Manual\n\n_Documento gerado automaticamente — Etapa 3 do TCC._\n\n"
        "- [Pagamentos](#pagamentos)\n\n"
        "## Pagamentos\n\n### US-12 — Pagamento com Pix\n\n"
        "O QR Code vale 10 minutos. Há atraso nas notificações.\n\n"
        "<!-- nota da autora -->\n\n"
        "---\n\n**Citações (Cohere Command R):**\n"
        '- "atraso nas notificações" — fonte(s): SCRUM-26'
    )
    frases = fidelidade.frases_para_anotar(texto, ARTEFATOS_FIDELIDADE)
    assert [f["frase"] for f in frases] == [
        "Manual.",
        "Documento gerado automaticamente — Etapa 3 do TCC.",
        "Pagamentos.",
        "Pagamentos.",
        "US-12 — Pagamento com Pix.",
        "O QR Code vale 10 minutos.",
        "Há atraso nas notificações.",
    ]
    assert [f["rotulo"] for f in frases] == ["-"] * 5 + ["", ""]
    assert frases[4]["secao"] == "Pagamentos"
    assert frases[5]["secao"] == "Pagamentos > US-12 — Pagamento com Pix"
    # Pelo título da seção mais interna ("US-12 — Pagamento com Pix").
    assert frases[5]["fonte_declarada"] == "SCRUM-18"
    # Pela citação do Command R + o título da seção.
    assert frases[6]["fonte_declarada"] == "SCRUM-18, SCRUM-26"


# --- juiz LLM ----------------------------------------------------------------


def test_montar_prompt_do_juiz_inclui_fontes_manual_e_criterios():
    artefato = Artefato(chave="SCRUM-1", titulo="EP-01 — Login", tipo="Epic", status="Feito", descricao="Entrar.")
    prompt = montar_prompt("# Manual", [artefato])
    assert prompt.index("<artefatos_de_origem>") < prompt.index("<manual>")
    assert "SCRUM-1" in prompt
    for criterio in CRITERIOS:
        assert criterio in prompt


def test_validar_recusa_nota_fora_da_escala():
    resposta = {c: {"justificativa": "", "nota": 3} for c in CRITERIOS}
    resposta["afirmacoes_nao_sustentadas"] = []
    assert validar(resposta) is resposta
    resposta["clareza"]["nota"] = 7
    with pytest.raises(ValueError):
        validar(resposta)


def test_arquivos_das_execucoes_inclui_manual_humano(tmp_path):
    for metodo in ("rag", "templating"):
        (tmp_path / metodo).mkdir()
        for n in (2, 1):
            (tmp_path / metodo / f"execucao_{n:02d}.md").write_text("x", encoding="utf-8")
    humano = tmp_path / "manual.md"
    humano.write_text("x", encoding="utf-8")
    arquivos = arquivos_das_execucoes(tmp_path, str(humano))
    assert [(m, n) for m, n, _ in arquivos] == [
        ("templating", 1), ("templating", 2), ("rag", 1), ("rag", 2), ("manual", 1)
    ]
    assert len(arquivos_das_execucoes(tmp_path, str(tmp_path / "nao_existe.md"))) == 4


# --- estatistica -------------------------------------------------------------


def test_a12_e_magnitude():
    assert estatistica.a12([2, 3], [1, 1]) == 1.0
    assert estatistica.a12([1, 1], [1, 1]) == 0.5
    assert estatistica.a12([1, 2], [2, 3]) == pytest.approx(0.125)  # 1 empate em 4 pares
    assert estatistica.magnitude(0.53) == "desprezível"
    assert estatistica.magnitude(0.60) == "pequeno"
    assert estatistica.magnitude(0.36) == "médio"
    assert estatistica.magnitude(0.0) == "grande"


def test_mann_whitney_grupos_constantes_e_iguais_da_p_1():
    assert estatistica.mann_whitney([5.0] * 10, [5.0] * 10) == (50.0, 1.0)


def test_mann_whitney_separacao_total():
    # Sem empates, n = 3 x 3: p exato bilateral = 2 / C(6, 3) = 0,1.
    u, p = estatistica.mann_whitney([1, 2, 3], [4, 5, 6])
    assert u == 0.0
    assert p == pytest.approx(0.1)


def test_holm():
    # Ordenados: 0,01·3 = 0,03; 0,02·2 = 0,04; 0,04·1 = 0,04 (monotônico).
    assert estatistica.holm([0.04, 0.01, 0.02]) == pytest.approx([0.04, 0.03, 0.04])
    assert estatistica.holm([0.5, 0.9]) == [1.0, 1.0]


def test_comparar_metricas_ignora_vazios_e_metodo_com_uma_execucao():
    linhas = (
        [{"metodo": "templating", "t": "0.005", "citado": ""} for _ in range(10)]
        + [{"metodo": "rag", "t": str(100 + i), "citado": "80"} for i in range(10)]
        + [{"metodo": "hibrido", "t": str(200 + i), "citado": "90"} for i in range(10)]
        + [{"metodo": "manual", "t": "9999", "citado": ""}]
    )
    resultado = estatistica.comparar_metricas(linhas, ["t", "citado"])
    pares_t = [(r["metodo_a"], r["metodo_b"]) for r in resultado if r["metrica"] == "t"]
    assert pares_t == [("templating", "rag"), ("templating", "hibrido"), ("rag", "hibrido")]
    assert all(r["diferenca_significativa"] == "sim" and r["efeito"] == "grande" for r in resultado)
    (citado,) = [r for r in resultado if r["metrica"] == "citado"]
    assert (citado["metodo_a"], citado["metodo_b"], citado["a12"]) == ("rag", "hibrido", 0.0)


# --- relatorio ----------------------------------------------------------------


def test_dados_por_execucao_junta_benchmark_e_juiz():
    individuais = [
        {"metodo": "rag", "execucao": "1", "tempo_total_s": "100", "tokens_entrada": "7", "tokens_saida": "3",
         "palavras": 10, "flesch_pt": 40, "cobertura_explicita_%": 50, "texto_citado_%": 80}
    ]
    notas = {c: "4" for c in CRITERIOS} | {"afirmacoes_nao_sustentadas": "1"}
    juiz = [{"metodo": "rag", "execucao": "1", **notas}, {"metodo": "manual", "execucao": "1", **notas}]
    dados = dados_por_execucao(individuais, juiz)
    assert dados[0]["tokens_total"] == 10
    assert dados[0]["clareza"] == "4"
    assert dados[1] == {"metodo": "manual", **notas}


def test_resumo_juiz_mediana_e_faixa():
    linhas = [
        {"metodo": "rag", **{c: str(n) for c in CRITERIOS}, "afirmacoes_nao_sustentadas": "0"} for n in (3, 4, 5)
    ]
    (item,) = resumo_juiz(linhas)
    assert item["execucoes"] == 3
    assert item["clareza"] == "4 (3–5)"


# --- reanotacao --------------------------------------------------------------


def test_kappa_cohen_exemplo_classico():
    # 50 itens: 20 sim/sim, 5 sim/não, 10 não/sim, 15 não/não.
    # p_o = 0,7; p_e = 0,5·0,6 + 0,5·0,4 = 0,5; κ = 0,4.
    primeira = ["S"] * 25 + ["N"] * 25
    segunda = ["S"] * 20 + ["N"] * 5 + ["S"] * 10 + ["N"] * 15
    assert reanotacao.kappa_cohen(primeira, segunda) == pytest.approx(0.4)
    assert reanotacao.interpretar(0.4) == "razoável"
    assert reanotacao.kappa_cohen(["S"] * 3, ["S"] * 3) is None
    assert reanotacao.interpretar(None) == "indefinido"


def _gravar(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=fidelidade.CAMPOS)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({c: linha.get(c, "") for c in fidelidade.CAMPOS})


def test_sortear_exige_primeira_rodada_completa_e_ignora_pre_preenchidas(tmp_path):
    origem = tmp_path / "f"
    origem.mkdir()
    linhas = [{"id": "1", "frase": "Título.", "rotulo": "-", "observacao": "pré-preenchido: título ou navegação"}]
    linhas += [{"id": str(i), "frase": f"Frase {i}.", "rotulo": ""} for i in range(2, 12)]
    _gravar(origem / "rag.csv", linhas)
    with pytest.raises(ValueError):
        reanotacao.sortear(0.2, 1, origem, origem / "re")

    for linha in linhas[1:]:
        linha["rotulo"] = "S"
    _gravar(origem / "rag.csv", linhas)
    registro = reanotacao.sortear(0.2, 1, origem, origem / "re")
    sorteadas = registro["planilhas"]["rag"]["sorteadas"]
    assert registro["planilhas"]["rag"]["candidatas"] == 10
    assert len(sorteadas) == 2 and "1" not in sorteadas
    assert sorteadas == reanotacao.sortear_ids(linhas, 0.2, 1)  # reprodutível pela semente
    nova = _ler_planilha(origem / "re" / "rag.csv")
    assert [l["id"] for l in nova] == sorteadas
    assert all(l["rotulo"] == "" for l in nova)  # a primeira rodada não vai junto
    with pytest.raises(FileExistsError):
        reanotacao.sortear(0.2, 1, origem, origem / "re")


def test_concordancia_entre_rodadas(tmp_path):
    origem = tmp_path / "f"
    origem.mkdir()
    _gravar(origem / "rag.csv", [{"id": str(i), "rotulo": r} for i, r in enumerate("SSNP", start=1)])
    (origem / "re").mkdir()
    _gravar(origem / "re" / "rag.csv", [{"id": "1", "rotulo": "s"}, {"id": "3", "rotulo": "N"}, {"id": "4", "rotulo": "N"}])
    rag, todos = reanotacao.concordancia(origem, origem / "re")
    assert rag["frases"] == 3
    assert rag["concordancia_%"] == pytest.approx(66.7)
    assert rag["discordancias"] == "P→N (1)"
    assert todos["metodo"] == "todos"
