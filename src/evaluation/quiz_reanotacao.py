"""Quiz da reanotação de fidelidade, para anotar as frases no navegador.

Duas etapas:

1. `gerar`: lê as planilhas de `data/evaluation/fidelidade/reanotacao/`,
   os artefatos de referência e as seções 3 e 4 do guia de anotação, e
   grava uma página HTML única (`quiz.html`, na mesma pasta) com tudo
   embutido. A página é publicada como artefato do claude.ai e guarda cada
   resposta no banco de dados do artefato, então o progresso é o mesmo no
   celular e no computador, e a anotação recomeça na primeira frase sem
   rótulo. Os rótulos da 1ª rodada não entram na página.
2. `importar`: lê as respostas exportadas do quiz (JSON) e preenche as
   colunas `rotulo`, `artefatos` e `observacao` das planilhas, que depois
   seguem para `python -m src.evaluation.reanotacao concordancia`.

Uso:
    python -m src.evaluation.quiz_reanotacao gerar
    python -m src.evaluation.quiz_reanotacao importar respostas.json
"""

import argparse
import csv
import json
import re
from pathlib import Path

from src.evaluation.fidelidade import CAMPOS, FIDELIDADE_DIR, ROTULOS
from src.evaluation.reanotacao import REANOTACAO_DIR, _ler, _planilhas

MODELO = Path(__file__).with_name("quiz_reanotacao.html")
REFERENCIA = FIDELIDADE_DIR / "artefatos_referencia.md"
GUIA = Path("docs/evaluation/02_guia_fidelidade.md")
SAIDA = REANOTACAO_DIR / "quiz.html"
# Ordem de apresentação: a mesma do README da reanotação
ORDEM = ["rag", "manual", "hibrido", "templating"]


def artefatos(referencia: Path = REFERENCIA) -> list[dict]:
    """Separa o arquivo de referência em um item por artefato (`## SCRUM-n — ...`)."""
    texto = referencia.read_text(encoding="utf-8")
    itens = []
    for bloco in re.split(r"^## ", texto, flags=re.M)[1:]:
        titulo, _, corpo = bloco.partition("\n")
        chave = titulo.split(" ", 1)[0]
        itens.append({"chave": chave, "titulo": titulo.strip(), "corpo": corpo.strip()})
    return itens


def secoes_guia(guia: Path = GUIA) -> str:
    """Seções 3 (Rótulos) e 4 (Regras de decisão) do guia, em Markdown."""
    texto = guia.read_text(encoding="utf-8")
    inicio = texto.index("## 3. Rótulos")
    fim = texto.index("## 5.")
    return texto[inicio:fim].strip()


def frases(diretorio: Path = REANOTACAO_DIR) -> list[dict]:
    planilhas = {p.stem: p for p in _planilhas(diretorio) if p.stem in ORDEM}
    itens = []
    for metodo in ORDEM:
        for linha in _ler(planilhas[metodo]):
            itens.append(
                {
                    "chave": f"{metodo}-{linha['id']}",
                    "metodo": metodo,
                    "id": linha["id"],
                    "secao": linha.get("secao", ""),
                    "frase": linha["frase"],
                    "fonte": [f.strip() for f in linha.get("fonte_declarada", "").split(",") if f.strip()],
                }
            )
    return itens


def gerar(saida: Path = SAIDA) -> int:
    dados = {"frases": frases(), "artefatos": artefatos(), "guia": secoes_guia()}
    # "</" escapado para o JSON não fechar o <script> da página
    embutido = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    pagina = MODELO.read_text(encoding="utf-8").replace("__DADOS__", embutido)
    saida.write_text(pagina, encoding="utf-8")
    return len(dados["frases"])


def importar(arquivo: Path, diretorio: Path = REANOTACAO_DIR) -> dict:
    """Preenche as planilhas com as respostas. Aceita a lista de respostas
    ou um objeto com a chave `respostas`."""
    bruto = json.loads(arquivo.read_text(encoding="utf-8"))
    respostas = {r["chave"]: r for r in (bruto["respostas"] if isinstance(bruto, dict) else bruto)}
    resumo = {}
    for planilha in _planilhas(diretorio):
        if planilha.stem not in ORDEM:
            continue
        linhas = _ler(planilha)
        faltando = []
        for linha in linhas:
            resposta = respostas.get(f"{planilha.stem}-{linha['id']}")
            rotulo = (resposta or {}).get("rotulo", "").strip().upper()
            if rotulo not in ROTULOS:
                faltando.append(linha["id"])
                continue
            linha["rotulo"] = rotulo
            linha["artefatos"] = resposta.get("artefatos", "").strip()
            linha["observacao"] = resposta.get("observacao", "").strip()
        with open(planilha, "w", newline="", encoding="utf-8-sig") as saida:
            escritor = csv.DictWriter(saida, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows({c: l.get(c, "") for c in CAMPOS} for l in linhas)
        resumo[planilha.stem] = {"total": len(linhas), "faltando": faltando}
    return resumo


def main() -> None:
    parser = argparse.ArgumentParser(description="Quiz da reanotação de fidelidade.")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("gerar")
    p_importar = sub.add_parser("importar")
    p_importar.add_argument("arquivo", type=Path)
    args = parser.parse_args()

    if args.comando == "gerar":
        total = gerar()
        print(f"{SAIDA} gerado com {total} frases.")
        return

    for metodo, item in importar(args.arquivo).items():
        anotadas = item["total"] - len(item["faltando"])
        aviso = f" (sem rótulo: {', '.join(item['faltando'])})" if item["faltando"] else ""
        print(f"{metodo}: {anotadas} de {item['total']} frases{aviso}")


if __name__ == "__main__":
    main()
