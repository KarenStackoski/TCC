"""Métricas automáticas calculadas sobre o texto de um manual (Markdown).

Todas são funções puras (sem API, sem modelo), para serem testáveis e
reprodutíveis. Ver docs/evaluation/01_estrutura.md, seções 3 a 5, para a
justificativa e as fontes de cada métrica:

- Legibilidade: Índice de Flesch adaptado ao português brasileiro por
  Martins, T. B. F.; Ghiraldelo, C. M.; Nunes, M. G. V.; Oliveira Jr., O. N.
  "Readability formulas applied to textbooks in Brazilian Portuguese".
  Notas do ICMSC-USP, Série Computação, n. 28, 1996.
  Fórmula: 248,835 − 1,015 × (palavras/frase) − 84,6 × (sílabas/palavra).
- Sílabas: hifenização do Pyphen com os padrões pt_BR do LibreOffice. Em
  português, a translineação segue a divisão silábica (Acordo Ortográfico
  da Língua Portuguesa, 1990, Base XX), então os pontos de hifenização
  aproximam os limites de sílaba. https://pyphen.org/
- Cobertura: proporção dos artefatos de entrada mencionados no manual.
- Taxa de texto citado: proporção do texto coberta por citações do Command
  R. Fonte do formato das citações: Cohere, "Retrieval Augmented Generation
  (RAG)" — https://docs.cohere.com/docs/retrieval-augmented-generation-rag
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

import pyphen

from src.common.schema import Artefato

# Rodapé de citações que os métodos 2 e 3 acrescentam ao fim do manual
# (src/rag/pipeline.py e src/hybrid/generator.py, `_formatar_citacoes`).
MARCADOR_CITACOES = "**Citações (Cohere Command R):**"
_LINHA_CITACAO = re.compile(r'^- "(?P<texto>.*)" — fonte\(s\): (?P<fontes>.*)$', re.MULTILINE)

_hifenizador = pyphen.Pyphen(lang="pt_BR", left=1, right=1)
_PALAVRA = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)*")
_FIM_DE_FRASE = re.compile(r"(?<=[.!?…])\s+|\n{2,}")
_VOGAIS = set("aeiouáéíóúâêôãõàü")


def separar_citacoes(texto: str) -> tuple[str, str]:
    """(corpo, rodapé de citações). Sem rodapé, devolve (texto, "")."""
    posicao = texto.find(MARCADOR_CITACOES)
    if posicao == -1:
        return texto, ""
    corpo = texto[:posicao].rstrip()
    if corpo.endswith("---"):
        corpo = corpo[:-3].rstrip()
    return corpo, texto[posicao:]


def limpar_markdown(texto: str) -> str:
    """Tira a marcação Markdown e o rodapé de citações, deixando só a prosa
    que o leitor lê — é sobre ela que legibilidade e BERTScore se aplicam."""
    corpo, _ = separar_citacoes(texto)
    linhas = []
    for linha in corpo.splitlines():
        linha = linha.strip()
        if re.fullmatch(r"[-*_|: ]{3,}", linha):  # régua horizontal ou separador de tabela
            continue
        linha = re.sub(r"^#{1,6}\s*", "", linha)  # cabeçalhos
        linha = re.sub(r"^>\s*", "", linha)  # citação em bloco
        linha = re.sub(r"^([-*+]|\d+[.)])\s+", "", linha)  # itens de lista
        linha = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", linha)  # links e imagens
        linha = re.sub(r"`([^`]*)`", r"\1", linha)
        linha = re.sub(r"(\*\*|__|\*|_)(.+?)\1", r"\2", linha)  # ênfase
        linha = linha.replace("|", " ")
        # Título/cabeçalho sem pontuação final vira frase própria.
        if linha and linha[-1] not in ".!?:;…":
            linha += "."
        linhas.append(linha)
    return "\n".join(linhas).strip()


def dividir_frases(texto_limpo: str) -> list[str]:
    frases = [f.strip() for f in _FIM_DE_FRASE.split(texto_limpo)]
    return [f for f in frases if _PALAVRA.search(f)]


def palavras(texto: str) -> list[str]:
    return _PALAVRA.findall(texto)


def contar_silabas(palavra: str) -> int:
    """Nº de sílabas = pontos de hifenização + 1. Palavras sem vogal
    (siglas como "API", "PIX" soletradas) contam como 1."""
    minuscula = palavra.lower()
    if not any(c in _VOGAIS for c in minuscula):
        return 1
    return sum(len(_hifenizador.positions(parte)) + 1 for parte in minuscula.split("-") if parte)


@dataclass
class Legibilidade:
    palavras: int
    frases: int
    silabas: int
    palavras_por_frase: float
    silabas_por_palavra: float
    flesch_pt: float


def legibilidade(texto_markdown: str) -> Legibilidade:
    limpo = limpar_markdown(texto_markdown)
    frases = dividir_frases(limpo)
    lista = palavras(limpo)
    if not frases or not lista:
        return Legibilidade(0, 0, 0, 0.0, 0.0, 0.0)
    silabas = sum(contar_silabas(p) for p in lista)
    asl = len(lista) / len(frases)
    asw = silabas / len(lista)
    return Legibilidade(
        palavras=len(lista),
        frases=len(frases),
        silabas=silabas,
        palavras_por_frase=round(asl, 2),
        silabas_por_palavra=round(asw, 3),
        flesch_pt=round(248.835 - 1.015 * asl - 84.6 * asw, 2),
    )


def faixa_flesch(indice: float) -> str:
    """Faixas de interpretação de Martins et al. (1996)."""
    if indice >= 75:
        return "muito fácil"
    if indice >= 50:
        return "fácil"
    if indice >= 25:
        return "difícil"
    return "muito difícil"


@dataclass
class Estrutura:
    cabecalhos_por_nivel: dict[int, int]
    secoes_nivel2: list[str]
    saltos_de_nivel: int
    itens_de_lista: int
    linhas_de_tabela: int


def estrutura(texto_markdown: str) -> Estrutura:
    """Conta cabeçalhos, listas e tabelas. `saltos_de_nivel` = quantas vezes
    um cabeçalho desce mais de um nível de uma vez (ex.: ## seguido de ####),
    o que quebra a hierarquia do documento (WCAG 2.2, técnica G141,
    "Organizing a page using headings" — https://www.w3.org/WAI/WCAG22/Techniques/general/G141)."""
    corpo, _ = separar_citacoes(texto_markdown)
    por_nivel: dict[int, int] = {}
    secoes: list[str] = []
    saltos = 0
    nivel_anterior = 0
    itens = 0
    tabela = 0
    for linha in corpo.splitlines():
        cabecalho = re.match(r"^(#{1,6})\s+(.*)", linha)
        if cabecalho:
            nivel = len(cabecalho.group(1))
            por_nivel[nivel] = por_nivel.get(nivel, 0) + 1
            if nivel == 2:
                secoes.append(cabecalho.group(2).strip())
            if nivel_anterior and nivel > nivel_anterior + 1:
                saltos += 1
            nivel_anterior = nivel
        elif re.match(r"^\s*([-*+]|\d+[.)])\s+", linha):
            itens += 1
        elif linha.strip().startswith("|"):
            tabela += 1
    return Estrutura(dict(sorted(por_nivel.items())), secoes, saltos, itens, tabela)


def _normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", sem_acento.casefold()).strip()


def _partes_do_titulo(titulo: str) -> tuple[str, str]:
    """"US-15 — Avaliação do restaurante" -> ("us-15", "avaliacao do restaurante")."""
    codigo, _, nome = titulo.partition("—")
    if not nome:
        return "", _normalizar(titulo)
    return _normalizar(codigo), _normalizar(nome)


def artefatos_mencionados(texto_markdown: str, artefatos: list[Artefato]) -> dict[str, str]:
    """Para cada artefato, como ele aparece no manual: "chave" (SCRUM-12),
    "codigo" (US-06), "titulo" (nome do título) ou "" (não aparece).

    É uma medida de menção explícita, não de cobertura de conteúdo: um
    manual pode tratar de um artefato sem citar a chave nem o título (o
    que é comum no manual humano e no RAG). Por isso a cobertura de
    conteúdo é anotada à mão na planilha de fidelidade
    (src/evaluation/fidelidade.py) e esta função serve como apoio."""
    texto_normalizado = _normalizar(texto_markdown)
    resultado: dict[str, str] = {}
    for artefato in artefatos:
        codigo, nome = _partes_do_titulo(artefato.titulo)
        if re.search(rf"\b{re.escape(artefato.chave)}\b", texto_markdown):
            resultado[artefato.chave] = "chave"
        elif codigo and re.search(rf"\b{re.escape(codigo)}\b", texto_normalizado):
            resultado[artefato.chave] = "codigo"
        elif nome and nome in texto_normalizado:
            resultado[artefato.chave] = "titulo"
        else:
            resultado[artefato.chave] = ""
    return resultado


def cobertura_explicita(texto_markdown: str, artefatos: list[Artefato]) -> float:
    if not artefatos:
        return 0.0
    mencoes = artefatos_mencionados(texto_markdown, artefatos)
    return sum(1 for forma in mencoes.values() if forma) / len(artefatos)


def taxa_texto_citado(texto_markdown: str) -> float | None:
    """Proporção dos caracteres do corpo cobertos por algum trecho citado
    pelo Command R. None quando o manual não tem rodapé de citações
    (métodos 1 e 4), para não confundir "sem citações" com "0%"."""
    corpo, rodape = separar_citacoes(texto_markdown)
    if not rodape:
        return None
    coberto = [False] * len(corpo)
    for citacao in _LINHA_CITACAO.finditer(rodape):
        trecho = citacao.group("texto")
        inicio = corpo.find(trecho)
        while inicio != -1:
            for i in range(inicio, inicio + len(trecho)):
                coberto[i] = True
            inicio = corpo.find(trecho, inicio + 1)
    caracteres_texto = [i for i, c in enumerate(corpo) if not c.isspace()]
    if not caracteres_texto:
        return 0.0
    return sum(1 for i in caracteres_texto if coberto[i]) / len(caracteres_texto)
