"""Vocabulário técnico dos manuais: o Flesch mede o tamanho das frases e das
palavras, mas não reconhece jargão, e o público dos manuais é leigo.

- Termos técnicos: ocorrências, por 100 palavras, dos termos de um glossário
  (data/evaluation/termos_tecnicos/glossario.csv). O critério de inclusão vem
  da 2ª heurística de Nielsen, usar palavras familiares ao usuário, "rather
  than internal jargon". Fonte: Nielsen, J. "Enhancing the explanatory power
  of usability heuristics". Proc. ACM CHI'94, p. 152-158, 1994.
  "estrito" = vocabulário de programação; "amplo" = estrito + termos
  limítrofes, que parte dos usuários conhece. Os dois níveis existem para
  mostrar se a conclusão depende da fronteira do glossário.
- Códigos internos: SCRUM-12, US-15, BUG-07, EP-01 e IMP-04, contados à parte,
  porque são identificadores do processo, e não vocabulário.
- Palavras raras: proporção de palavras abaixo de um limiar de frequência
  na língua geral, como no De-Jargonizer. Fonte: Rakedzon, T. et al.
  "Automatic jargon identifier for scientists engaging with the public and
  science communication educators". PLOS ONE, v. 12, n. 8, e0181742, 2017. Lá,
  jargão aparece menos de 50 vezes em 90 milhões de palavras; aqui esse limiar
  foi convertido para a escala Zipf do wordfreq: log10(50/90e6 × 1e9) = 2,74.
  Fonte: Speer, R. "rspeer/wordfreq: v3.0". Zenodo, 2022,
  https://doi.org/10.5281/zenodo.7199437. Serve de conferência independente do
  glossário, mas é ruidosa: flexões comuns como "cardápios" também são raras.

Os métodos com várias execuções são comparados como em estatistica.py.
Ver docs/evaluation/01_estrutura.md, seção 3.

Uso:
    python -m src.evaluation.termos_tecnicos
"""

from __future__ import annotations

import csv
import re
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from wordfreq import zipf_frequency

from src.evaluation import metricas_texto as mt
from src.evaluation.estatistica import comparar_metricas
from src.evaluation.manuais import MANUAIS_PADRAO, anonimizar

SAIDA_DIR = Path("data/evaluation/termos_tecnicos")
EXECUCOES_DIR = Path("data/evaluation/execucoes")
LIMIAR_ZIPF_RARA = 2.74
METRICAS = ["termos_estrito_100p", "termos_amplo_100p", "frases_com_termo_estrito_%", "codigos_100p", "palavras_raras_%"]

_CODIGO_INTERNO = re.compile(r"\b(?:SCRUM|US|BUG|EP|IMP)-\d+\b")


@dataclass
class Vocabulario:
    palavras: int
    ocorrencias_estrito: int
    ocorrencias_amplo: int
    termos_estrito_100p: float
    termos_amplo_100p: float
    frases_com_termo_estrito_pct: float
    codigos_100p: float
    palavras_raras_pct: float
    por_termo: Counter


def carregar_glossario(caminho: Path = SAIDA_DIR / "glossario.csv") -> dict[str, str]:
    """termo -> nível."""
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        return {linha["termo"]: linha["nivel"] for linha in csv.DictReader(arquivo)}


def _padrao(termos: list[str]) -> re.Pattern:
    """Do mais longo para o mais curto, para "skeleton loading" contar uma vez
    só, e sem casar com parte de palavra hifenizada."""
    ordenados = sorted(termos, key=len, reverse=True)
    return re.compile(r"(?<![\w-])(?:" + "|".join(map(re.escape, ordenados)) + r")(?![\w-])", re.IGNORECASE)


def medir(texto_markdown: str, glossario: dict[str, str]) -> Vocabulario:
    limpo = mt.limpar_markdown(anonimizar(texto_markdown))
    lista = mt.palavras(limpo)
    total = len(lista) or 1
    padrao = _padrao(list(glossario))
    por_termo = Counter(m.group(0).lower() for m in padrao.finditer(limpo))
    estrito = sum(n for termo, n in por_termo.items() if glossario[termo] == "estrito")
    amplo = sum(por_termo.values())
    termos_estritos = [termo for termo, nivel in glossario.items() if nivel == "estrito"]
    padrao_estrito = _padrao(termos_estritos)
    frases = mt.dividir_frases(limpo)
    com_termo = sum(1 for frase in frases if padrao_estrito.search(frase))
    raras = sum(1 for p in lista if zipf_frequency(p, "pt") < LIMIAR_ZIPF_RARA)
    return Vocabulario(
        palavras=len(lista),
        ocorrencias_estrito=estrito,
        ocorrencias_amplo=amplo,
        termos_estrito_100p=round(100 * estrito / total, 2),
        termos_amplo_100p=round(100 * amplo / total, 2),
        frases_com_termo_estrito_pct=round(100 * com_termo / (len(frases) or 1), 1),
        codigos_100p=round(100 * len(_CODIGO_INTERNO.findall(limpo)) / total, 2),
        palavras_raras_pct=round(100 * raras / total, 2),
        por_termo=por_termo,
    )


def _linha(metodo: str, execucao: str, v: Vocabulario) -> dict:
    return {
        "metodo": metodo,
        "execucao": execucao,
        "palavras": v.palavras,
        "ocorrencias_estrito": v.ocorrencias_estrito,
        "ocorrencias_amplo": v.ocorrencias_amplo,
        "termos_estrito_100p": v.termos_estrito_100p,
        "termos_amplo_100p": v.termos_amplo_100p,
        "frases_com_termo_estrito_%": v.frases_com_termo_estrito_pct,
        "codigos_100p": v.codigos_100p,
        "palavras_raras_%": v.palavras_raras_pct,
    }


def resumir(linhas: list[dict]) -> list[dict]:
    """Por método: mediana (mín–máx) de cada métrica nas execuções."""
    resumo = []
    for metodo in dict.fromkeys(linha["metodo"] for linha in linhas):
        valores_metodo = [linha for linha in linhas if linha["metodo"] == metodo]
        item = {"metodo": metodo, "execucoes": len(valores_metodo)}
        for metrica in METRICAS:
            valores = [float(linha[metrica]) for linha in valores_metodo]
            item[metrica] = f"{statistics.median(valores):g} ({min(valores):g}–{max(valores):g})"
        resumo.append(item)
    return resumo


def _escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def main() -> None:
    glossario = carregar_glossario()
    linhas = []
    por_termo: dict[str, Counter] = {}
    arquivos = [(m, p.stem, p) for m in ("templating", "rag", "hibrido") for p in sorted((EXECUCOES_DIR / m).glob("execucao_*.md"))]
    arquivos.append(("manual", "execucao_01", Path(MANUAIS_PADRAO["manual"])))
    for metodo, execucao, caminho in arquivos:
        v = medir(caminho.read_text(encoding="utf-8"), glossario)
        linhas.append(_linha(metodo, execucao, v))
        por_termo.setdefault(metodo, Counter()).update(v.por_termo)

    _escrever_csv(SAIDA_DIR / "execucoes.csv", linhas)
    _escrever_csv(SAIDA_DIR / "resultado.csv", resumir(linhas))
    _escrever_csv(SAIDA_DIR / "estatistica.csv", comparar_metricas(linhas, METRICAS))
    metodos = list(por_termo)
    usados = sorted({t for c in por_termo.values() for t in c}, key=lambda t: (glossario[t], t))
    _escrever_csv(
        SAIDA_DIR / "por_termo.csv",
        [{"termo": t, "nivel": glossario[t], **{m: por_termo[m][t] for m in metodos}} for t in usados],
    )
    print(f"Resultados em {SAIDA_DIR}")


if __name__ == "__main__":
    main()
