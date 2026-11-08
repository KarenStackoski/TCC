"""Figura do tempo de cada execução do RAG e do híbrido (artigo do TCC).

Lê data/evaluation/tempos.csv (gerado por `src/evaluation/benchmark.py`) e
desenha um gráfico de pontos: cada ponto é uma execução e o traço vertical
é a mediana do método. O templating (cerca de 5 ms) fica de fora, porque
não aparece na mesma escala; o valor dele é dado no texto.

Gráfico com matplotlib (`Axes.scatter`, `Axes.vlines`) —
https://matplotlib.org/stable/api/axes_api.html. Pontos com transparência e
deslocamento vertical pequeno e fixo, para que valores próximos não se
sobreponham (gráfico de pontos "jittered"; Cleveland, W. S. "The Elements
of Graphing Data". Hobart Press, 1994). Ver docs/evaluation/01_estrutura.md,
seção 2.

Uso: python -m src.evaluation.grafico_tempo
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ENTRADA = Path("data/evaluation/tempos.csv")
SAIDA = Path("data/evaluation/fig5_tempo_execucoes.png")
METODOS = (("rag", "RAG"), ("hibrido", "Híbrido"))
COR = "#2a78d6"
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#5f5e5a"
# Deslocamentos fixos (não aleatórios), para a figura sair igual a cada execução.
DESLOCAMENTOS = (-0.12, 0.08, -0.04, 0.12, -0.08, 0.04, 0.0, -0.10, 0.10, -0.02)


def ler_tempos(caminho: Path = ENTRADA) -> dict[str, list[float]]:
    tempos: dict[str, list[float]] = {}
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            tempos.setdefault(linha["metodo"], []).append(float(linha["tempo_total_s"]))
    return tempos


def desenhar(tempos: dict[str, list[float]], saida: Path = SAIDA) -> Path:
    plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
    figura, eixo = plt.subplots(figsize=(6.3, 2.4), dpi=300)

    for posicao, (metodo, rotulo) in enumerate(METODOS):
        valores = tempos[metodo]
        ys = [posicao + DESLOCAMENTOS[i % len(DESLOCAMENTOS)] for i in range(len(valores))]
        eixo.scatter(valores, ys, s=28, color=COR, alpha=0.75, edgecolors="white", linewidths=0.8, zorder=3)
        mediana = statistics.median(valores)
        eixo.vlines(mediana, posicao - 0.28, posicao + 0.28, color=TINTA, linewidth=2, zorder=4)
        eixo.annotate(
            f"mediana {mediana:.1f} s".replace(".", ","),
            (mediana, posicao + 0.30),
            ha="center",
            va="bottom",
            fontsize=8,
            color=TINTA,
        )

    eixo.set_yticks(range(len(METODOS)), [rotulo for _, rotulo in METODOS], fontsize=9, color=TINTA)
    eixo.set_ylim(-0.6, len(METODOS) - 0.25)
    eixo.set_xlim(0, 300)
    eixo.set_xlabel("Tempo total da execução (s)", fontsize=9, color=TINTA_SECUNDARIA)
    eixo.tick_params(axis="x", labelsize=8, colors=TINTA_SECUNDARIA)
    eixo.tick_params(axis="y", length=0)
    eixo.grid(axis="x", color="#e2e1dc", linewidth=0.6, zorder=0)
    for lado in ("top", "right", "left"):
        eixo.spines[lado].set_visible(False)
    eixo.spines["bottom"].set_color("#c9c8c2")

    figura.tight_layout()
    saida.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(saida, bbox_inches="tight")
    plt.close(figura)
    return saida


def main() -> None:
    print(f"Figura salva em {desenhar(ler_tempos())}")


if __name__ == "__main__":
    main()
