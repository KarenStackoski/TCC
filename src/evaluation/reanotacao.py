"""Concordância intra-anotador da anotação de fidelidade.

Sem um segundo anotador, a consistência da anotação é medida reanotando
uma amostra das frases depois de um intervalo, sem olhar a primeira
anotação, e comparando as duas rodadas. Ver
docs/evaluation/02_guia_fidelidade.md, seção 7.

Duas etapas:

1. `sortear`: só roda com a primeira rodada completa (todas as frases com
   rótulo válido), para a amostra não poder influenciar a primeira
   anotação. Sorteia, em cada planilha, uma fração das frases a anotar
   (as pré-preenchidas como título ou navegação ficam de fora), com
   semente registrada, e grava planilhas novas com as mesmas colunas, mas
   sem rótulo, artefatos nem observação. Estratificar por método garante
   que cada manual entra na amostra na mesma proporção.
2. `concordancia`: compara os rótulos das duas rodadas nas frases
   sorteadas: concordância simples (%) e kappa de Cohen, por método e no
   total.

Fontes:
- Kappa: Cohen, J. "A Coefficient of Agreement for Nominal Scales".
  Educational and Psychological Measurement, v. 20, n. 1, 1960.
  κ = (p_o − p_e) / (1 − p_e), com p_o = concordância observada e
  p_e = concordância esperada ao acaso, pelas proporções marginais de
  cada rodada.
- Interpretação: Landis, J. R.; Koch, G. G. "The Measurement of Observer
  Agreement for Categorical Data". Biometrics, v. 33, n. 1, 1977
  (< 0 pobre; 0–0,20 leve; 0,21–0,40 razoável; 0,41–0,60 moderada;
  0,61–0,80 substancial; 0,81–1 quase perfeita).

Uso:
    python -m src.evaluation.reanotacao sortear --fracao 0.2 --semente 2026
    (esperar pelo menos uma semana; anotar data/evaluation/fidelidade/reanotacao/)
    python -m src.evaluation.reanotacao concordancia
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from src.evaluation.fidelidade import CAMPOS, FIDELIDADE_DIR, PRE_PREENCHIDO, ROTULOS

REANOTACAO_DIR = FIDELIDADE_DIR / "reanotacao"
INTERVALO_MINIMO_DIAS = 7


def _ler(planilha: Path) -> list[dict]:
    with open(planilha, newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def _rotulo(linha: dict) -> str:
    return (linha.get("rotulo") or "").strip().upper()


def _planilhas(diretorio: Path) -> list[Path]:
    return sorted(p for p in diretorio.glob("*.csv") if p.name != "resultado.csv")


def candidatas(linhas: list[dict]) -> list[dict]:
    """Frases que a pessoa anotou de fato (fora as pré-preenchidas)."""
    return [l for l in linhas if not (l.get("observacao") or "").startswith(PRE_PREENCHIDO)]


def sortear_ids(linhas: list[dict], fracao: float, semente: int) -> list[str]:
    """Ids sorteados entre as candidatas, arredondando para cima (pelo menos
    1 frase por manual), na ordem original do manual."""
    ids = [l["id"] for l in candidatas(linhas)]
    if not ids:
        return []
    quantidade = min(len(ids), math.ceil(fracao * len(ids)))
    sorteados = set(random.Random(semente).sample(ids, quantidade))
    return [i for i in ids if i in sorteados]


def sortear(fracao: float, semente: int, origem: Path = FIDELIDADE_DIR, destino: Path = REANOTACAO_DIR) -> dict:
    planilhas = _planilhas(origem)
    if not planilhas:
        raise FileNotFoundError(f"Nenhuma planilha de fidelidade em {origem}")
    for planilha in planilhas:
        incompletas = [l["id"] for l in _ler(planilha) if _rotulo(l) not in ROTULOS]
        if incompletas:
            raise ValueError(
                f"{planilha.name}: a primeira rodada ainda não terminou "
                f"(sem rótulo válido: {', '.join(incompletas[:10])}). Termine antes de sortear."
            )
    if destino.exists() and any(destino.glob("*.csv")):
        raise FileExistsError(f"{destino} já tem uma amostra; apague a pasta para sortear de novo.")

    destino.mkdir(parents=True, exist_ok=True)
    amostra = {}
    for planilha in planilhas:
        linhas = _ler(planilha)
        ids = sortear_ids(linhas, fracao, semente)
        por_id = {l["id"]: l for l in linhas}
        with open(destino / planilha.name, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
            escritor.writeheader()
            for i in ids:
                original = por_id[i]
                escritor.writerow(
                    {
                        "id": i,
                        "secao": original.get("secao", ""),
                        "frase": original["frase"],
                        "rotulo": "",
                        "artefatos": "",
                        "fonte_declarada": original.get("fonte_declarada", ""),
                        "observacao": "",
                    }
                )
        amostra[planilha.stem] = {"candidatas": len(candidatas(linhas)), "sorteadas": ids}

    hoje = date.today()
    registro = {
        "semente": semente,
        "fracao": fracao,
        "data_do_sorteio": hoje.isoformat(),
        "reanotar_a_partir_de": (hoje + timedelta(days=INTERVALO_MINIMO_DIAS)).isoformat(),
        "planilhas": amostra,
    }
    (destino / "amostra.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    return registro


def kappa_cohen(primeira: list[str], segunda: list[str]) -> float | None:
    """κ de Cohen (1960). None quando p_e = 1 (as duas rodadas usaram uma
    categoria só, e o kappa não é definido)."""
    if len(primeira) != len(segunda) or not primeira:
        raise ValueError("As duas rodadas precisam ter o mesmo número (> 0) de rótulos.")
    n = len(primeira)
    p_o = sum(a == b for a, b in zip(primeira, segunda)) / n
    marg_1, marg_2 = Counter(primeira), Counter(segunda)
    p_e = sum(marg_1[c] * marg_2[c] for c in marg_1) / (n * n)
    if p_e == 1:
        return None
    return (p_o - p_e) / (1 - p_e)


def interpretar(kappa: float | None) -> str:
    """Faixas de Landis e Koch (1977)."""
    if kappa is None:
        return "indefinido"
    if kappa < 0:
        return "pobre"
    for limite, nome in ((0.20, "leve"), (0.40, "razoável"), (0.60, "moderada"), (0.80, "substancial")):
        if kappa <= limite:
            return nome
    return "quase perfeita"


def _linha_resultado(metodo: str, pares: list[tuple[str, str]]) -> dict:
    primeira, segunda = [a for a, _ in pares], [b for _, b in pares]
    kappa = kappa_cohen(primeira, segunda)
    return {
        "metodo": metodo,
        "frases": len(pares),
        "concordancia_%": round(100 * sum(a == b for a, b in pares) / len(pares), 1),
        "kappa": round(kappa, 3) if kappa is not None else "",
        "interpretacao": interpretar(kappa),
        # Ex.: "S→P (2)" = 2 frases que eram S na primeira rodada e viraram P.
        "discordancias": "; ".join(
            f"{a}→{b} ({n})" for (a, b), n in sorted(Counter((a, b) for a, b in pares if a != b).items())
        ),
    }


def concordancia(origem: Path = FIDELIDADE_DIR, reanotacao: Path = REANOTACAO_DIR) -> list[dict]:
    resultados = []
    todos: list[tuple[str, str]] = []
    for planilha in _planilhas(reanotacao):
        primeira = {l["id"]: _rotulo(l) for l in _ler(origem / planilha.name)}
        segunda = _ler(planilha)
        invalidas = [l["id"] for l in segunda if _rotulo(l) not in ROTULOS]
        if invalidas:
            raise ValueError(f"reanotacao/{planilha.name}: sem rótulo válido: {', '.join(invalidas[:10])}")
        pares = [(primeira[l["id"]], _rotulo(l)) for l in segunda]
        if pares:
            resultados.append(_linha_resultado(planilha.stem, pares))
            todos += pares
    if not todos:
        raise FileNotFoundError(f"Nenhuma reanotação em {reanotacao}")
    resultados.append(_linha_resultado("todos", todos))
    return resultados


def main() -> None:
    parser = argparse.ArgumentParser(description="Concordância intra-anotador da fidelidade.")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_sortear = sub.add_parser("sortear")
    p_sortear.add_argument("--fracao", type=float, default=0.2)
    p_sortear.add_argument("--semente", type=int, default=2026)
    sub.add_parser("concordancia")
    args = parser.parse_args()

    if args.comando == "sortear":
        registro = sortear(args.fracao, args.semente)
        for metodo, item in registro["planilhas"].items():
            print(f"{metodo}: {len(item['sorteadas'])} de {item['candidatas']} frases")
        print(f"Planilhas em {REANOTACAO_DIR}. Não abra antes de {registro['reanotar_a_partir_de']}")
        print("e não consulte a primeira rodada enquanto reanota.")
        return

    resultados = concordancia()
    with open(REANOTACAO_DIR / "concordancia.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)
    for linha in resultados:
        print(linha)


if __name__ == "__main__":
    main()
