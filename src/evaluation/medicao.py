"""Registro de tempo e tokens de cada chamada à API da Cohere durante uma
execução de um método de geração.

Em vez de alterar os backends das Etapas 2 e 3 para devolverem tempo e uso
de tokens (o que mudaria as assinaturas já testadas e documentadas), este
módulo envolve temporariamente `cohere.ClientV2.chat` e `cohere.ClientV2.embed`
enquanto a execução roda, e restaura os métodos originais ao sair. O código
de geração medido é exatamente o mesmo que roda fora do benchmark.

Relógio: `time.perf_counter()`, o relógio monotônico de maior resolução
disponível, indicado pela documentação oficial do Python para medir
intervalos curtos — https://docs.python.org/3/library/time.html#time.perf_counter

Tokens: a resposta do Chat v2 traz `usage.billed_units` (input_tokens,
output_tokens) e a do Embed traz `meta.billed_units` (input_tokens).
Fonte: Cohere, "Chat API reference" — https://docs.cohere.com/reference/chat
e "Embed API reference" — https://docs.cohere.com/reference/embed
Ver docs/evaluation/01_estrutura.md, seção 2.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import cohere


@dataclass
class ChamadaAPI:
    """Uma chamada à API. `fase` é deduzida do tipo da chamada: embed com
    input_type="search_document" = indexação; embed com "search_query" =
    recuperação; chat = geração."""

    fase: str
    duracao_s: float
    tokens_entrada: int = 0
    tokens_saida: int = 0


def _fase_do_embed(kwargs: dict) -> str:
    return "indexacao" if kwargs.get("input_type") == "search_document" else "recuperacao"


def _tokens(billed_units) -> tuple[int, int]:
    if billed_units is None:
        return 0, 0
    entrada = int(billed_units.input_tokens or 0)
    saida = int(getattr(billed_units, "output_tokens", None) or 0)
    return entrada, saida


@dataclass
class RegistroChamadas:
    """Context manager: enquanto ativo, toda chamada a `ClientV2.chat` e
    `ClientV2.embed` é cronometrada e tem os tokens anotados em `chamadas`.

    Só vale para clientes criados dentro do bloco: o construtor do SDK
    (`cohere.client.validate_args`) copia o método `chat` da classe para a
    instância no momento da criação. Todos os backends deste projeto criam
    o cliente dentro da própria função de geração, então isso é atendido."""

    chamadas: list[ChamadaAPI] = field(default_factory=list)

    def __enter__(self) -> "RegistroChamadas":
        self._chat_original = cohere.ClientV2.chat
        self._embed_original = cohere.ClientV2.embed
        registro = self

        def chat(cliente, *args, **kwargs):
            inicio = time.perf_counter()
            resposta = registro._chat_original(cliente, *args, **kwargs)
            duracao = time.perf_counter() - inicio
            usage = getattr(resposta, "usage", None)
            entrada, saida = _tokens(getattr(usage, "billed_units", None))
            registro.chamadas.append(ChamadaAPI("geracao", duracao, entrada, saida))
            return resposta

        def embed(cliente, *args, **kwargs):
            inicio = time.perf_counter()
            resposta = registro._embed_original(cliente, *args, **kwargs)
            duracao = time.perf_counter() - inicio
            meta = getattr(resposta, "meta", None)
            entrada, _ = _tokens(getattr(meta, "billed_units", None))
            registro.chamadas.append(ChamadaAPI(_fase_do_embed(kwargs), duracao, entrada, 0))
            return resposta

        cohere.ClientV2.chat = chat
        cohere.ClientV2.embed = embed
        return self

    def __exit__(self, *exc) -> None:
        cohere.ClientV2.chat = self._chat_original
        cohere.ClientV2.embed = self._embed_original

    def tempo_por_fase(self) -> dict[str, float]:
        tempos = {"indexacao": 0.0, "recuperacao": 0.0, "geracao": 0.0}
        for chamada in self.chamadas:
            tempos[chamada.fase] += chamada.duracao_s
        return tempos

    def total_tokens(self) -> tuple[int, int]:
        entrada = sum(c.tokens_entrada for c in self.chamadas)
        saida = sum(c.tokens_saida for c in self.chamadas)
        return entrada, saida
