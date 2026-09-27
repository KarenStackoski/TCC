"""BERTScore de cada manual em relação ao manual humano (método 4).

Fórmula (Zhang, T.; Kishore, V.; Wu, F.; Weinberger, K. Q.; Artzi, Y.
"BERTScore: Evaluating Text Generation with BERT". ICLR, 2020, seção 3):
cada token do candidato é casado com o token mais parecido da referência
(similaridade de cosseno entre embeddings contextuais), e vice-versa:
    P = média, sobre os tokens do candidato, da maior similaridade na referência
    R = média, sobre os tokens da referência, da maior similaridade no candidato
    F = 2PR / (P + R)

Por que não chamar `bert_score.score()` direto: o BERT aceita no máximo 512
tokens por entrada, e a biblioteca trunca o texto em silêncio
(`truncation=True` em `bert_score.utils.sent_encode`). Os manuais têm
milhares de tokens, então só o começo seria comparado. Aqui o texto é
dividido em janelas de até 510 tokens, cada janela passa pelo modelo, e os
embeddings de todas as janelas são concatenados antes do casamento guloso.
A fórmula é a mesma; muda só que cada token vê o contexto da sua janela,
não do documento inteiro. Para textos curtos (uma janela só) o resultado
é igual ao de `bert_score.score()` — verificado em
tests/test_evaluation_bertscore.py.

Modelo e camada: os mesmos padrões do pacote bert_score para textos que
não estão em inglês — `bert-base-multilingual-cased` (Devlin et al., 2019)
e a camada 9 (`bert_score.utils.model2layers`), escolhida pelos autores
por correlacionar melhor com julgamento humano. Sem ponderação por IDF e
sem reescalonamento por linha de base (não há linha de base publicada
para português no pacote), então os valores absolutos ficam comprimidos
perto do topo da escala: compare os métodos entre si, não com um limiar.

Ressalva de validade: usar o manual humano como referência mede
semelhança com ele, não qualidade absoluta; favorece o método que escreve
de forma parecida com a autora. Ver docs/evaluation/01_estrutura.md, seção 5.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from bert_score.utils import model2layers
from transformers import AutoModel, AutoTokenizer

from src.evaluation.metricas_texto import limpar_markdown

MODELO = "bert-base-multilingual-cased"
CAMADA = model2layers[MODELO]
TOKENS_POR_JANELA = 510  # 512 menos [CLS] e [SEP]


@dataclass
class BertScore:
    precisao: float
    revocacao: float
    f1: float


def pontuar_embeddings(candidato: torch.Tensor, referencia: torch.Tensor) -> BertScore:
    """Casamento guloso de Zhang et al. (2020), sobre embeddings já
    normalizados (uma linha por token). Separado para ser testável sem
    baixar o modelo."""
    similaridade = candidato @ referencia.T
    precisao = similaridade.max(dim=1).values.mean().item()
    revocacao = similaridade.max(dim=0).values.mean().item()
    f1 = 2 * precisao * revocacao / (precisao + revocacao) if precisao + revocacao else 0.0
    return BertScore(round(precisao, 4), round(revocacao, 4), round(f1, 4))


class Avaliador:
    def __init__(self, modelo: str = MODELO, camada: int = CAMADA) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(modelo)
        self.modelo = AutoModel.from_pretrained(modelo)
        self.modelo.eval()
        self.camada = camada

    @torch.no_grad()
    def embeddings(self, texto: str) -> torch.Tensor:
        ids = self.tokenizer(texto, add_special_tokens=False)["input_ids"]
        partes = []
        for inicio in range(0, len(ids), TOKENS_POR_JANELA):
            janela = ids[inicio : inicio + TOKENS_POR_JANELA]
            entrada = torch.tensor(
                [[self.tokenizer.cls_token_id, *janela, self.tokenizer.sep_token_id]]
            )
            saida = self.modelo(entrada, output_hidden_states=True)
            # hidden_states[0] é a camada de embeddings; hidden_states[k] é a
            # saída da k-ésima camada. Tira [CLS] e [SEP], que o bert_score
            # também exclui (peso zero em `get_idf_dict`).
            partes.append(saida.hidden_states[self.camada][0, 1:-1])
        vetores = torch.cat(partes)
        return vetores / vetores.norm(dim=-1, keepdim=True)

    def pontuar(self, candidato_md: str, referencia_md: str) -> BertScore:
        return pontuar_embeddings(
            self.embeddings(limpar_markdown(candidato_md)),
            self.embeddings(limpar_markdown(referencia_md)),
        )
