"""Junta os resultados de todas as métricas num relatório (Markdown + CSV).

Calcula agora as métricas automáticas (legibilidade, estrutura, cobertura
explícita, taxa de texto citado, BERTScore) e a variação entre execuções, e
acrescenta os resultados que dependem de etapas separadas, quando já
existem: tempos (benchmark.py), tempo do método manual
(data/evaluation/tempo_manual.csv, preenchido à mão), fidelidade
(fidelidade.py), avaliação humana (avaliacao_humana.py) e juiz LLM
(juiz_llm.py). Ver docs/evaluation/01_estrutura.md.

Uso:
    python -m src.evaluation.relatorio
    python -m src.evaluation.relatorio --sem-bertscore
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

from src.evaluation import metricas_texto as mt
from src.evaluation.avaliacao_humana import MANUAIS_PADRAO
from src.evaluation.variacao import variacao_do_diretorio
from src.jira.extractor import parse_issues

AVALIACAO_DIR = Path("data/evaluation")


def metricas_automaticas(manuais: dict[str, str], artefatos, com_bertscore: bool) -> list[dict]:
    textos = {m: Path(p).read_text(encoding="utf-8") for m, p in manuais.items() if Path(p).exists()}
    avaliador = None
    if com_bertscore and "manual" in textos:
        from src.evaluation.bertscore import Avaliador

        avaliador = Avaliador()

    linhas = []
    for metodo, texto in textos.items():
        leg = mt.legibilidade(texto)
        est = mt.estrutura(texto)
        citado = mt.taxa_texto_citado(texto)
        linha = {
            "metodo": metodo,
            "palavras": leg.palavras,
            "frases": leg.frases,
            "palavras_por_frase": leg.palavras_por_frase,
            "silabas_por_palavra": leg.silabas_por_palavra,
            "flesch_pt": leg.flesch_pt,
            "faixa_flesch": mt.faixa_flesch(leg.flesch_pt),
            "secoes_nivel2": len(est.secoes_nivel2),
            "cabecalhos": sum(est.cabecalhos_por_nivel.values()),
            "saltos_de_nivel": est.saltos_de_nivel,
            "itens_de_lista": est.itens_de_lista,
            "cobertura_explicita_%": round(100 * mt.cobertura_explicita(texto, artefatos), 1),
            "texto_citado_%": round(100 * citado, 1) if citado is not None else "",
        }
        if avaliador and metodo != "manual":
            bs = avaliador.pontuar(texto, textos["manual"])
            linha.update({"bertscore_p": bs.precisao, "bertscore_r": bs.revocacao, "bertscore_f1": bs.f1})
        linhas.append(linha)
    return linhas


def execucoes_individuais(tempos: list[dict], artefatos) -> list[dict]:
    """Uma linha por manual gerado no benchmark: tempo, tokens, métricas do
    texto e a conferência do SHA-256 (o arquivo salvo ainda é o mesmo que
    foi gerado e medido?)."""
    linhas = []
    for t in tempos:
        caminho = Path(t["arquivo"])
        if not caminho.exists():
            integro = "arquivo ausente"
            texto = ""
        else:
            texto = caminho.read_text(encoding="utf-8")
            integro = "ok" if hashlib.sha256(caminho.read_bytes()).hexdigest() == t["sha256"] else "ALTERADO"
        leg = mt.legibilidade(texto)
        citado = mt.taxa_texto_citado(texto)
        linhas.append(
            {
                "metodo": t["metodo"],
                "execucao": t["execucao"],
                "inicio": t["inicio"],
                "tempo_total_s": t["tempo_total_s"],
                "tempo_geracao_s": t["tempo_geracao_s"],
                "tokens_entrada": t["tokens_entrada"],
                "tokens_saida": t["tokens_saida"],
                "palavras": leg.palavras,
                "flesch_pt": leg.flesch_pt,
                "secoes_nivel2": len(mt.estrutura(texto).secoes_nivel2),
                "cobertura_explicita_%": round(100 * mt.cobertura_explicita(texto, artefatos), 1),
                "texto_citado_%": round(100 * citado, 1) if citado is not None else "",
                "arquivo": caminho.as_posix(),
                "sha256": t["sha256"][:16] + "…",
                "integridade": integro,
            }
        )
    return linhas


def variacoes(execucoes_dir: Path) -> list[dict]:
    linhas = []
    for diretorio in sorted(p for p in execucoes_dir.glob("*") if p.is_dir()):
        if len(list(diretorio.glob("execucao_*.md"))) < 2:
            continue
        v = variacao_do_diretorio(diretorio)
        linhas.append({"metodo": diretorio.name, **vars(v)})
    return linhas


def _ler_csv(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def _tabela_md(titulo: str, linhas: list[dict], nota: str = "") -> list[str]:
    if not linhas:
        return [f"## {titulo}", "", "_Ainda sem dados._", ""]
    colunas = list(linhas[0])
    saida = [f"## {titulo}", ""]
    if nota:
        saida += [nota, ""]
    saida.append("| " + " | ".join(colunas) + " |")
    saida.append("|" + "---|" * len(colunas))
    for linha in linhas:
        saida.append("| " + " | ".join(str(linha.get(c, "")) for c in colunas) + " |")
    return saida + [""]


def _escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    if not linhas:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def main() -> None:
    parser = argparse.ArgumentParser(description="Relatório consolidado da avaliação.")
    parser.add_argument("--entrada", default="data/raw/data.json")
    parser.add_argument("--manual-humano", default=MANUAIS_PADRAO["manual"])
    parser.add_argument("--sem-bertscore", action="store_true")
    args = parser.parse_args()

    with open(args.entrada, encoding="utf-8") as arquivo:
        artefatos = parse_issues(json.load(arquivo)["issues"])
    manuais = dict(MANUAIS_PADRAO, manual=args.manual_humano)

    AVALIACAO_DIR.mkdir(parents=True, exist_ok=True)
    automaticas = metricas_automaticas(manuais, artefatos, not args.sem_bertscore)
    var = variacoes(AVALIACAO_DIR / "execucoes")
    _escrever_csv(AVALIACAO_DIR / "metricas_automaticas.csv", automaticas)
    _escrever_csv(AVALIACAO_DIR / "variacao.csv", var)

    concordancia_path = AVALIACAO_DIR / "avaliacao_humana" / "concordancia.json"
    concordancia = json.loads(concordancia_path.read_text(encoding="utf-8")) if concordancia_path.exists() else None

    individuais = execucoes_individuais(_ler_csv(AVALIACAO_DIR / "tempos.csv"), artefatos)
    _escrever_csv(AVALIACAO_DIR / "execucoes_individuais.csv", individuais)

    agora = datetime.now().astimezone().isoformat(timespec="seconds")
    md = [
        "# Resultados da avaliação",
        "",
        f"Gerado por `python -m src.evaluation.relatorio` em {agora}.",
        "Métodos e fontes de cada métrica: `docs/evaluation/01_estrutura.md`.",
        "",
        "Manuais avaliados nas seções de métricas automáticas, fidelidade, avaliação humana e juiz:",
        *[f"- {m}: `{p}`" + ("" if Path(p).exists() else " (ainda não existe)") for m, p in manuais.items()],
        "",
    ]
    md += _tabela_md(
        "Tempo de geração — resumo (s)",
        _ler_csv(AVALIACAO_DIR / "tempos_resumo.csv"),
        "Mediana, mínimo, máximo e desvio-padrão do tempo total de cada execução.",
    )
    md += _tabela_md(
        "Tempo e métricas de cada manual gerado",
        individuais,
        "Cada linha é um manual salvo em `data/evaluation/execucoes/`. `integridade` = o "
        "SHA-256 do arquivo hoje é igual ao registrado quando ele foi gerado.",
    )
    falhas = _ler_csv(AVALIACAO_DIR / "falhas.csv")
    if falhas:
        md += _tabela_md(
            "Execuções que falharam (descartadas e refeitas)",
            falhas,
            "Uma execução em que alguma chamada à API passou do tempo limite do SDK "
            "(300 s) não termina e não tem tempo medido; ela foi refeita com o mesmo número.",
        )
    md += _tabela_md("Tempo do método manual (min)", _ler_csv(AVALIACAO_DIR / "tempo_manual.csv"))
    md += _tabela_md(
        "Métricas automáticas",
        automaticas,
        "BERTScore em relação ao manual humano (sem reescalonamento). "
        "Cobertura explícita = artefatos citados por chave, código ou título.",
    )
    md += _tabela_md("Variação entre execuções", var)
    md += _tabela_md("Fidelidade e cobertura de conteúdo (anotação)", _ler_csv(AVALIACAO_DIR / "fidelidade" / "resultado.csv"))
    md += _tabela_md("Avaliação humana (1 a 5)", _ler_csv(AVALIACAO_DIR / "avaliacao_humana" / "resultado.csv"))
    if concordancia:
        md += [f"Concordância: {concordancia}", ""]
    md += _tabela_md("LLM como juiz (1 a 5)", _ler_csv(AVALIACAO_DIR / "juiz_llm" / "resultado.csv"))

    (AVALIACAO_DIR / "resultados.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Relatório em {AVALIACAO_DIR / 'resultados.md'}")


if __name__ == "__main__":
    main()
