"""Avaliação humana cega dos manuais, com concordância entre avaliadores.

Duas etapas:

1. `preparar`: copia cada manual para um nome neutro (manual_A.md,
   manual_B.md, ...) em ordem sorteada, tira o rodapé de citações e a linha
   que identifica a etapa (que revelariam o método), grava o gabarito
   (letra -> método) à parte e gera o formulário que cada avaliador preenche.
   O avaliador não sabe qual método gerou cada manual (avaliação cega).
2. `analisar`: lê os formulários preenchidos, desfaz o sorteio pelo
   gabarito e calcula média e mediana por método e critério, e a
   concordância entre avaliadores (alfa de Krippendorff, nível ordinal).

Fontes:
- Protocolo (critérios explícitos, escala Likert, avaliação cega, mais de
  um avaliador, reportar concordância): van der Lee, C.; Gatt, A.; van
  Miltenburg, E.; Krahmer, E. "Human evaluation of automatically generated
  text: Current trends and best practice guidelines". Computer Speech &
  Language, v. 67, 2021.
- Alfa de Krippendorff: Krippendorff, K. "Content Analysis: An Introduction
  to Its Methodology". 2. ed. Sage, 2004 (cap. 11). Implementação: pacote
  `krippendorff` (Castro, S., https://github.com/pln-fing-udelar/fast-krippendorff).
- Escala ordinal para Likert: os valores têm ordem, mas a distância entre
  eles não é garantidamente igual — Krippendorff (2004), métrica ordinal.
Ver docs/evaluation/01_estrutura.md, seção 7.

Uso:
    python -m src.evaluation.avaliacao_humana preparar --semente 2026
    python -m src.evaluation.avaliacao_humana analisar
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import statistics
import string
from pathlib import Path

import krippendorff

from src.evaluation.metricas_texto import separar_citacoes

AVALIACAO_DIR = Path("data/evaluation/avaliacao_humana")

MANUAIS_PADRAO = {
    "templating": "data/manuals_generated/templating/manual.md",
    "rag": "data/manuals_generated/rag/manual_cohere.md",
    "hibrido": "data/manuals_generated/hybrid/manual_cohere.md",
    "manual": "data/manuals_generated/manual/manual.md",
}

# Critérios e definições entregues ao avaliador. Baseados nos critérios de
# qualidade mais usados em avaliação humana de NLG (van der Lee et al.,
# 2021) e, para "completude" e "utilidade", na finalidade de um manual de
# usuário (ISO/IEC/IEEE 26514 — informação para usuários de software).
CRITERIOS: dict[str, str] = {
    "clareza": "O texto é fácil de entender; as frases são claras e sem ambiguidade.",
    "coerencia": "As partes do manual se encadeiam de forma lógica; a organização faz sentido.",
    "completude": "O manual cobre as funcionalidades, tarefas e problemas que um usuário precisaria conhecer.",
    "correcao": "O texto está correto em gramática e ortografia e não contém informações que pareçam erradas.",
    "utilidade": "Com este manual, um usuário conseguiria usar o sistema.",
}
ESCALA = "1 = discordo totalmente, 2 = discordo, 3 = neutro, 4 = concordo, 5 = concordo totalmente"

# Linha que a Etapa 1 escreve no topo do manual e que identificaria o método.
_LINHA_IDENTIFICADORA = re.compile(r"^_Documento gerado automaticamente.*_\s*$", re.MULTILINE)


def anonimizar(texto: str) -> str:
    corpo, _ = separar_citacoes(texto)
    corpo = _LINHA_IDENTIFICADORA.sub("", corpo)
    return re.sub(r"\n{3,}", "\n\n", corpo).strip() + "\n"


def sortear_letras(metodos: list[str], semente: int) -> dict[str, str]:
    """letra -> método, em ordem aleatória reprodutível pela semente."""
    embaralhados = list(metodos)
    random.Random(semente).shuffle(embaralhados)
    return dict(zip(string.ascii_uppercase, embaralhados))


def preparar(manuais: dict[str, str], semente: int, saida_dir: Path = AVALIACAO_DIR) -> dict[str, str]:
    existentes = {m: p for m, p in manuais.items() if Path(p).exists()}
    faltando = sorted(set(manuais) - set(existentes))
    if faltando:
        print(f"Aviso: manuais não encontrados e deixados de fora: {', '.join(faltando)}")

    gabarito = sortear_letras(sorted(existentes), semente)
    (saida_dir / "manuais").mkdir(parents=True, exist_ok=True)
    for letra, metodo in gabarito.items():
        texto = Path(existentes[metodo]).read_text(encoding="utf-8")
        (saida_dir / "manuais" / f"manual_{letra}.md").write_text(anonimizar(texto), encoding="utf-8")

    (saida_dir / "gabarito.json").write_text(
        json.dumps({"semente": semente, "letras": gabarito}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with open(saida_dir / "formulario_modelo.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["avaliador", "manual", *CRITERIOS, "comentario"])
        for letra in gabarito:
            escritor.writerow(["", letra, *[""] * len(CRITERIOS), ""])

    instrucoes = [
        "# Instruções para o avaliador",
        "",
        "Leia cada manual da pasta `manuais/` e dê uma nota de 1 a 5 para cada critério.",
        f"Escala: {ESCALA}.",
        "",
        "Preencha uma cópia de `formulario_modelo.csv` com o seu nome na coluna `avaliador`",
        "e salve em `respostas/<seu_nome>.csv`. Avalie cada manual de forma independente;",
        "não converse com outros avaliadores antes de terminar.",
        "",
        "## Critérios",
        "",
        *[f"- **{nome}**: {definicao}" for nome, definicao in CRITERIOS.items()],
        "",
    ]
    (saida_dir / "INSTRUCOES.md").write_text("\n".join(instrucoes), encoding="utf-8")
    (saida_dir / "respostas").mkdir(exist_ok=True)
    return gabarito


def ler_respostas(respostas_dir: Path) -> list[dict]:
    linhas = []
    for arquivo_csv in sorted(respostas_dir.glob("*.csv")):
        with open(arquivo_csv, newline="", encoding="utf-8-sig") as arquivo:
            for linha in csv.DictReader(arquivo):
                if not linha.get("avaliador"):
                    linha["avaliador"] = arquivo_csv.stem
                linhas.append(linha)
    return linhas


def alfa_ordinal(respostas: list[dict], criterios: list[str]) -> float | None:
    """Alfa de Krippendorff (ordinal). Unidades = pares (manual, critério);
    avaliadores = linhas da matriz. Com poucas unidades (ex.: 4 manuais por
    critério), o alfa de um critério isolado é instável, por isso a unidade
    é o par manual×critério. None se houver menos de 2 avaliadores."""
    avaliadores = sorted({r["avaliador"] for r in respostas})
    if len(avaliadores) < 2:
        return None
    unidades = sorted({(r["manual"], c) for r in respostas for c in criterios})
    notas = {(r["avaliador"], r["manual"], c): r.get(c, "") for r in respostas for c in criterios}
    matriz = [
        [float(notas[(a, m, c)]) if notas.get((a, m, c), "").strip() else float("nan") for (m, c) in unidades]
        for a in avaliadores
    ]
    return float(krippendorff.alpha(reliability_data=matriz, level_of_measurement="ordinal"))


def analisar(saida_dir: Path = AVALIACAO_DIR) -> tuple[list[dict], dict]:
    gabarito = json.loads((saida_dir / "gabarito.json").read_text(encoding="utf-8"))["letras"]
    respostas = ler_respostas(saida_dir / "respostas")
    if not respostas:
        raise FileNotFoundError(f"Nenhum formulário preenchido em {saida_dir / 'respostas'}")

    criterios = list(CRITERIOS)
    resumo = []
    for letra, metodo in gabarito.items():
        linha = {"metodo": metodo, "manual": letra}
        for criterio in criterios:
            notas = [float(r[criterio]) for r in respostas if r["manual"] == letra and r.get(criterio, "").strip()]
            linha[f"{criterio}_media"] = round(statistics.mean(notas), 2) if notas else ""
            linha[f"{criterio}_mediana"] = statistics.median(notas) if notas else ""
        resumo.append(linha)

    concordancia = {
        "avaliadores": len({r["avaliador"] for r in respostas}),
        "alfa_krippendorff_ordinal": alfa_ordinal(respostas, criterios),
    }
    return resumo, concordancia


def main() -> None:
    parser = argparse.ArgumentParser(description="Avaliação humana cega dos manuais.")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_preparar = sub.add_parser("preparar")
    p_preparar.add_argument("--semente", type=int, default=2026)
    p_preparar.add_argument("--manual-humano", default=MANUAIS_PADRAO["manual"])
    sub.add_parser("analisar")
    args = parser.parse_args()

    if args.comando == "preparar":
        manuais = dict(MANUAIS_PADRAO, manual=args.manual_humano)
        gabarito = preparar(manuais, args.semente)
        print(f"{len(gabarito)} manuais anonimizados em {AVALIACAO_DIR / 'manuais'}")
        print(f"Gabarito em {AVALIACAO_DIR / 'gabarito.json'} — não mostre aos avaliadores.")
        return

    resumo, concordancia = analisar()
    with open(AVALIACAO_DIR / "resultado.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resumo[0]))
        escritor.writeheader()
        escritor.writerows(resumo)
    (AVALIACAO_DIR / "concordancia.json").write_text(json.dumps(concordancia, indent=2), encoding="utf-8")
    for linha in resumo:
        print(linha)
    print(concordancia)


if __name__ == "__main__":
    main()
