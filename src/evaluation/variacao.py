"""Variação entre execuções do mesmo método (reprodutibilidade).

Compara, par a par, os manuais que `src/evaluation/benchmark.py` salvou em
data/evaluation/execucoes/<metodo>/. Um método determinístico (templating)
deve dar sempre o mesmo texto; os métodos com LLM, não.

Similaridade: `difflib.SequenceMatcher.ratio()` sobre a sequência de
palavras (2·M/T, onde M = elementos em comum e T = total), da biblioteca
padrão do Python — https://docs.python.org/3/library/difflib.html —
baseado no algoritmo de Ratcliff, J. W.; Metzener, D. E. "Pattern
Matching: The Gestalt Approach". Dr. Dobb's Journal, 1988.
A estrutura (lista de seções de nível 2) é comparada à parte, porque é
justamente o que o template fixa e a LLM do RAG decide livremente.
Ver docs/evaluation/01_estrutura.md, seção 6.
"""

from __future__ import annotations

import itertools
import statistics
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from src.evaluation.metricas_texto import estrutura, separar_citacoes


def similaridade(texto_a: str, texto_b: str) -> float:
    corpo_a, _ = separar_citacoes(texto_a)
    corpo_b, _ = separar_citacoes(texto_b)
    # autojunk=False: com o padrão, palavras muito frequentes (> 1% do texto)
    # são ignoradas no casamento, o que distorce a razão em textos longos.
    return SequenceMatcher(None, corpo_a.split(), corpo_b.split(), autojunk=False).ratio()


@dataclass
class Variacao:
    execucoes: int
    textos_distintos: int
    estruturas_distintas: int
    similaridade_media: float
    similaridade_minima: float


def variacao(textos: list[str]) -> Variacao:
    if len(textos) < 2:
        raise ValueError("São necessárias ao menos 2 execuções para medir variação.")
    razoes = [similaridade(a, b) for a, b in itertools.combinations(textos, 2)]
    estruturas = {tuple(estrutura(t).secoes_nivel2) for t in textos}
    return Variacao(
        execucoes=len(textos),
        textos_distintos=len(set(textos)),
        estruturas_distintas=len(estruturas),
        similaridade_media=round(statistics.mean(razoes), 4),
        similaridade_minima=round(min(razoes), 4),
    )


def variacao_do_diretorio(diretorio: Path | str) -> Variacao:
    arquivos = sorted(Path(diretorio).glob("execucao_*.md"))
    return variacao([a.read_text(encoding="utf-8") for a in arquivos])
