"""Comparação estatística entre os métodos, sobre as métricas medidas em
cada execução (tempo, tokens, métricas do texto, notas do juiz).

Protocolo de Arcuri, A.; Briand, L. "A practical guide for using
statistical tests to assess randomized algorithms in software
engineering". ICSE 2011: os métodos com LLM são aleatórios (cada execução
dá um resultado diferente), então a comparação é feita sobre várias
execuções, com um teste não paramétrico e um tamanho de efeito.

- Teste: U de Mann-Whitney, bilateral, para cada par de métodos. Não supõe
  distribuição normal (o tempo, por exemplo, tem cauda longa por causa da
  rede). Fonte: Mann, H. B.; Whitney, D. R. "On a Test of Whether One of
  Two Random Variables is Stochastically Larger than the Other". The
  Annals of Mathematical Statistics, v. 18, n. 1, 1947. Implementação:
  `scipy.stats.mannwhitneyu` (Virtanen, P. et al. "SciPy 1.0: Fundamental
  Algorithms for Scientific Computing in Python". Nature Methods, v. 17,
  2020). Se os dois grupos têm todos os valores iguais (ex.: nota 5 em
  todas as execuções dos dois), não há diferença a testar e p = 1.
- Tamanho do efeito: A12 de Vargha e Delaney, a probabilidade de uma
  execução do método A ter valor maior que uma do método B (empate conta
  meio). 0,5 = sem diferença. Faixas: |A12 − 0,5| < 0,06 desprezível;
  < 0,14 pequeno; < 0,21 médio; senão grande (limiares 0,56, 0,64 e 0,71).
  Fonte: Vargha, A.; Delaney, H. D. "A Critique and Improvement of the CL
  Common Language Effect Size Statistics of McGraw and Wong". Journal of
  Educational and Behavioral Statistics, v. 25, n. 2, 2000.
- Comparações múltiplas: cada métrica tem 3 comparações (um par por
  combinação de métodos), e o p de cada uma é ajustado pelo método de Holm
  dentro da métrica. Fonte: Holm, S. "A Simple Sequentially Rejective
  Multiple Test Procedure". Scandinavian Journal of Statistics, v. 6,
  n. 2, 1979.

Um método só entra no teste se tem pelo menos 2 execuções. O manual humano
(uma execução só) fica de fora dos testes e é descrito à parte.
Ver docs/evaluation/01_estrutura.md, seção 8.
"""

from __future__ import annotations

import math
from itertools import combinations

from scipy.stats import mannwhitneyu

ALFA = 0.05
MINIMO_EXECUCOES = 2


def a12(x: list[float], y: list[float]) -> float:
    """P(X > Y) + 0,5 · P(X = Y), contando todos os pares (Vargha e Delaney, 2000)."""
    maiores = sum(1 for a in x for b in y if a > b)
    empates = sum(1 for a in x for b in y if a == b)
    return (maiores + 0.5 * empates) / (len(x) * len(y))


def magnitude(valor_a12: float) -> str:
    distancia = abs(valor_a12 - 0.5)
    if distancia < 0.06:
        return "desprezível"
    if distancia < 0.14:
        return "pequeno"
    if distancia < 0.21:
        return "médio"
    return "grande"


def mann_whitney(x: list[float], y: list[float]) -> tuple[float, float]:
    """(U, p bilateral). Com todos os valores iguais nos dois grupos, o SciPy
    devolve p = NaN (variância zero); aí não há diferença: p = 1."""
    if len(set(x) | set(y)) == 1:
        return len(x) * len(y) / 2, 1.0
    resultado = mannwhitneyu(x, y, alternative="two-sided")
    return float(resultado.statistic), float(resultado.pvalue)


def holm(valores_p: list[float]) -> list[float]:
    """p ajustados pelo método de Holm (1979), na ordem de entrada."""
    m = len(valores_p)
    ordem = sorted(range(m), key=lambda i: valores_p[i])
    ajustados = [0.0] * m
    maior_ate_agora = 0.0
    for posicao, i in enumerate(ordem):
        maior_ate_agora = max(maior_ate_agora, (m - posicao) * valores_p[i])
        ajustados[i] = min(1.0, maior_ate_agora)
    return ajustados


def comparar(metrica: str, grupos: dict[str, list[float]]) -> list[dict]:
    """Uma linha por par de métodos com pelo menos MINIMO_EXECUCOES valores."""
    validos = {m: v for m, v in grupos.items() if len(v) >= MINIMO_EXECUCOES}
    linhas = []
    for a, b in combinations(validos, 2):
        u, p = mann_whitney(validos[a], validos[b])
        efeito = a12(validos[a], validos[b])
        linhas.append(
            {
                "metrica": metrica,
                "metodo_a": a,
                "metodo_b": b,
                "n_a": len(validos[a]),
                "n_b": len(validos[b]),
                "u": u,
                "p": p,
                "a12": round(efeito, 3),
                "efeito": magnitude(efeito),
            }
        )
    for linha, p_ajustado in zip(linhas, holm([linha["p"] for linha in linhas])):
        linha["p"] = round(linha["p"], 4)
        linha["p_holm"] = round(p_ajustado, 4)
        linha["diferenca_significativa"] = "sim" if p_ajustado < ALFA else "não"
    return linhas


def agrupar(linhas: list[dict], metrica: str) -> dict[str, list[float]]:
    """método -> valores da métrica, ignorando células vazias (ex.: texto
    citado não existe no templating)."""
    grupos: dict[str, list[float]] = {}
    for linha in linhas:
        valor = str(linha.get(metrica, "")).strip()
        if valor and not math.isnan(float(valor)):
            grupos.setdefault(linha["metodo"], []).append(float(valor))
    return grupos


def comparar_metricas(linhas: list[dict], metricas: list[str]) -> list[dict]:
    resultado = []
    for metrica in metricas:
        resultado += comparar(metrica, agrupar(linhas, metrica))
    return resultado
