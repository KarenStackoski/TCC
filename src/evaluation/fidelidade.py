"""Fidelidade às fontes (alucinação) e cobertura de conteúdo, por anotação.

Não existe métrica automática confiável para "esta frase é sustentada pelos
artefatos?" em português sem usar outra LLM como juiz, e o juiz traz vieses
próprios (ver src/evaluation/juiz_llm.py). Por isso a medida principal é
anotada por uma pessoa, frase a frase, como na avaliação humana de
fidelidade de Maynez, J.; Narayan, S.; Bohnet, B.; McDonald, R. "On
Faithfulness and Factuality in Abstractive Summarization". ACL, 2020.

Rótulos por frase (definição de alucinação de Ji, Z. et al. "Survey of
Hallucination in Natural Language Generation". ACM Computing Surveys,
v. 55, n. 12, 2023):
  S = sustentada: o conteúdo está nos artefatos;
  P = parcialmente sustentada: parte está nos artefatos, parte não;
  N = não sustentada (alucinação): o conteúdo não está nos artefatos ou
      os contradiz.
  - = não se aplica (frase sem conteúdo verificável, ex.: "Bem-vindo ao manual").

Na mesma planilha, a coluna `artefatos` recebe as chaves (SCRUM-N) de onde
veio o conteúdo da frase; a cobertura de conteúdo é a proporção dos 32
artefatos que aparecem em alguma frase. É a mesma ideia de cobertura
(recall de conteúdo) usada na avaliação de sumarização.
Ver docs/evaluation/01_estrutura.md, seção 4.

Uso:
    python -m src.evaluation.fidelidade preparar
    (anotar as planilhas em data/evaluation/fidelidade/)
    python -m src.evaluation.fidelidade analisar
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from bisect import bisect_right
from pathlib import Path

from src.common.schema import Artefato
from src.evaluation.manuais import MANUAIS_PADRAO
from src.evaluation.metricas_texto import (
    artefatos_mencionados,
    citacoes,
    corpo_visivel,
    dividir_frases_com_posicao,
    limpar_linha,
)
from src.jira.extractor import parse_issues
from src.rag.indexer import artefato_para_texto

FIDELIDADE_DIR = Path("data/evaluation/fidelidade")
ROTULOS = {"S", "P", "N", "-"}
CAMPOS = ["id", "secao", "frase", "rotulo", "artefatos", "fonte_declarada", "observacao"]
PRE_PREENCHIDO = "pré-preenchido"

_CABECALHO = re.compile(r"^(#{1,6})\s+(.*)$")
# Linhas sem conteúdo verificável: item de lista que é só um link (sumário)
# e a linha que a Etapa 1/3 escreve no topo do manual.
_SO_LINK = re.compile(r"^[-*+]\s+\[[^\]]*\]\([^)]*\)$")
_LINHA_ETAPA = re.compile(r"^_Documento gerado automaticamente.*_$")


def frases_para_anotar(texto: str, artefatos: list[Artefato]) -> list[dict]:
    """As mesmas frases que `dividir_frases(limpar_markdown(texto))`, cada uma
    com a seção onde está, o rótulo "-" já preenchido quando ela é título,
    item de sumário ou a linha de identificação da etapa, e a
    `fonte_declarada`: os artefatos que a própria frase menciona (chave,
    código ou nome, como na cobertura explícita), os que o título da seção
    dela menciona por chave ou código, e as fontes que o Command R declarou
    para trechos dela. É só uma pista para a anotação, não um rótulo."""
    linhas = corpo_visivel(texto).splitlines()
    limpas: list[str] = []
    meta: list[dict] = []
    caminho: dict[int, str] = {}
    for linha in linhas:
        crua = linha.strip()
        cabecalho = _CABECALHO.match(crua)
        secao = " > ".join(caminho[n] for n in sorted(caminho) if n > 1)
        if cabecalho:
            nivel = len(cabecalho.group(1))
            caminho = {n: t for n, t in caminho.items() if n < nivel}
            caminho[nivel] = limpar_linha(cabecalho.group(2)).rstrip(".")
        limpa = limpar_linha(linha)
        if limpa is None:
            continue
        limpas.append(limpa)
        meta.append(
            {
                "secao": secao,
                "titulo_da_secao": caminho[max(caminho)] if caminho and not cabecalho else "",
                "nao_verificavel": bool(cabecalho or _SO_LINK.match(crua) or _LINHA_ETAPA.match(crua)),
            }
        )

    inicios, posicao = [], 0
    for limpa in limpas:
        inicios.append(posicao)
        posicao += len(limpa) + 1
    trechos_citados = citacoes(texto)

    saida = []
    for frase, inicio in dividir_frases_com_posicao("\n".join(limpas)):
        m = meta[bisect_right(inicios, inicio) - 1]
        na_frase = artefatos_mencionados(frase, artefatos)
        no_titulo = artefatos_mencionados(m["titulo_da_secao"], artefatos)
        fontes = {chave for chave, forma in na_frase.items() if forma}
        # Do título da seção, só chave ou código: o nome sozinho ("Pagamentos")
        # é o de um épico e apontaria o épico para todas as frases da seção.
        fontes |= {chave for chave, forma in no_titulo.items() if forma in ("chave", "codigo")}
        fontes |= {chave for trecho, chaves in trechos_citados if trecho in frase for chave in chaves}
        saida.append(
            {
                "secao": m["secao"],
                "frase": frase,
                "rotulo": "-" if m["nao_verificavel"] else "",
                "fonte_declarada": ", ".join(sorted(fontes, key=lambda c: int(c.split("-")[1]))),
                "observacao": f"{PRE_PREENCHIDO}: título ou navegação" if m["nao_verificavel"] else "",
            }
        )
    return saida


def _tem_anotacao(planilha: Path) -> bool:
    """Alguma célula de anotação preenchida pela pessoa (o pré-preenchimento
    automático não conta)."""
    with open(planilha, newline="", encoding="utf-8-sig") as arquivo:
        for linha in csv.DictReader(arquivo):
            if (linha.get("observacao") or "").startswith(PRE_PREENCHIDO):
                continue
            if any((linha.get(c) or "").strip() for c in ("rotulo", "artefatos", "observacao")):
                return True
    return False


def escrever_referencia(artefatos: list[Artefato], destino: Path) -> None:
    """Os 32 artefatos por extenso, para consultar durante a anotação."""
    ordenados = sorted(artefatos, key=lambda a: int(a.chave.split("-")[1]))
    partes = ["# Artefatos de origem (data/raw/data.json)", ""]
    for artefato in ordenados:
        partes += [f"## {artefato.chave} — {artefato.titulo}", "", artefato_para_texto(artefato), ""]
    destino.write_text("\n".join(partes), encoding="utf-8")


def preparar(manuais: dict[str, str], artefatos: list[Artefato], saida_dir: Path = FIDELIDADE_DIR) -> dict[str, int]:
    """Uma planilha por método, uma frase por linha, mais a referência dos
    artefatos. Não sobrescreve uma planilha que já tenha anotação. O CSV é
    gravado em UTF-8 com BOM para o Excel reconhecer os acentos."""
    saida_dir.mkdir(parents=True, exist_ok=True)
    escrever_referencia(artefatos, saida_dir / "artefatos_referencia.md")
    contagem: dict[str, int] = {}
    for metodo, caminho in manuais.items():
        if not Path(caminho).exists():
            print(f"Aviso: {caminho} não encontrado; {metodo} fica de fora.")
            continue
        destino = saida_dir / f"{metodo}.csv"
        if destino.exists() and _tem_anotacao(destino):
            print(f"{destino} já tem anotação; mantido sem alteração.")
            continue
        frases = frases_para_anotar(Path(caminho).read_text(encoding="utf-8"), artefatos)
        with open(destino, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
            escritor.writeheader()
            for indice, frase in enumerate(frases, start=1):
                escritor.writerow({"id": indice, "artefatos": "", **frase})
        contagem[metodo] = len(frases)
    return contagem


def _chaves(celula: str) -> set[str]:
    return set(re.findall(r"SCRUM-\d+", celula or ""))


def analisar_planilha(linhas: list[dict], total_artefatos: int) -> dict:
    rotulos = [l["rotulo"].strip().upper() for l in linhas]
    invalidos = [l["id"] for l, r in zip(linhas, rotulos) if r not in ROTULOS]
    if invalidos:
        raise ValueError(f"Frases sem rótulo válido (S/P/N/-): {', '.join(invalidos[:10])}")
    verificaveis = [r for r in rotulos if r != "-"]
    n = len(verificaveis)
    cobertos = set().union(*(_chaves(l["artefatos"]) for l in linhas)) if linhas else set()
    return {
        "frases": len(rotulos),
        "frases_verificaveis": n,
        "sustentadas_%": round(100 * verificaveis.count("S") / n, 1) if n else 0.0,
        "parciais_%": round(100 * verificaveis.count("P") / n, 1) if n else 0.0,
        "nao_sustentadas_%": round(100 * verificaveis.count("N") / n, 1) if n else 0.0,
        "artefatos_cobertos": len(cobertos),
        "cobertura_conteudo_%": round(100 * len(cobertos) / total_artefatos, 1) if total_artefatos else 0.0,
    }


def analisar(entrada_json: str, saida_dir: Path = FIDELIDADE_DIR) -> list[dict]:
    with open(entrada_json, encoding="utf-8") as arquivo:
        total = len(parse_issues(json.load(arquivo)["issues"]))
    resultados = []
    for planilha in sorted(saida_dir.glob("*.csv")):
        if planilha.name == "resultado.csv":
            continue
        with open(planilha, newline="", encoding="utf-8-sig") as arquivo:
            linhas = list(csv.DictReader(arquivo))
        resultados.append({"metodo": planilha.stem, **analisar_planilha(linhas, total)})
    return resultados


def main() -> None:
    parser = argparse.ArgumentParser(description="Planilhas de fidelidade e cobertura.")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_preparar = sub.add_parser("preparar")
    p_preparar.add_argument("--manual-humano", default=MANUAIS_PADRAO["manual"])
    p_preparar.add_argument("--entrada", default="data/raw/data.json")
    p_analisar = sub.add_parser("analisar")
    p_analisar.add_argument("--entrada", default="data/raw/data.json")
    args = parser.parse_args()

    if args.comando == "preparar":
        with open(args.entrada, encoding="utf-8") as arquivo:
            artefatos = parse_issues(json.load(arquivo)["issues"])
        contagem = preparar(dict(MANUAIS_PADRAO, manual=args.manual_humano), artefatos)
        for metodo, n in contagem.items():
            print(f"{metodo}: {n} frases para anotar em {FIDELIDADE_DIR / (metodo + '.csv')}")
        return

    resultados = analisar(args.entrada)
    with open(FIDELIDADE_DIR / "resultado.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)
    for linha in resultados:
        print(linha)


if __name__ == "__main__":
    main()
