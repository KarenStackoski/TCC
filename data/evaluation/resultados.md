# Resultados da avaliação

Gerado por `python -m src.evaluation.relatorio` em 2026-10-19T19:50:42-03:00.
Métodos e fontes de cada métrica: `docs/evaluation/01_estrutura.md`.

Manuais avaliados nas seções de métricas automáticas, fidelidade e juiz (1 manual por método):
- templating: `data/manuals_generated/templating/manual.md`
- rag: `data/manuals_generated/rag/manual_cohere.md`
- hibrido: `data/manuals_generated/hybrid/manual_cohere.md`
- manual: `data/manuals_generated/manual/manual.md`

## Tempo de geração — resumo (s)

Mediana, mínimo, máximo e desvio-padrão do tempo total de cada execução.

| metodo | execucoes | mediana_s | min_s | max_s | desvio_padrao_s | mediana_tokens |
|---|---|---|---|---|---|---|
| templating | 10 | 0.0051 | 0.0048 | 0.0064 | 0.0005 | 0.0 |
| rag | 10 | 123.7699 | 88.732 | 240.9057 | 42.6953 | 8512.5 |
| hibrido | 10 | 197.363 | 169.9763 | 271.2465 | 34.1356 | 8786.0 |

## Tempo e métricas de cada manual gerado

Cada linha é um manual salvo em `data/evaluation/execucoes/`. `integridade` = o SHA-256 do arquivo hoje é igual ao registrado quando ele foi gerado.

| metodo | execucao | inicio | tempo_total_s | tempo_geracao_s | tokens_entrada | tokens_saida | palavras | flesch_pt | secoes_nivel2 | cobertura_explicita_% | texto_citado_% | arquivo | sha256 | integridade |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| templating | 1 | 2026-09-27T18:34:00-03:00 | 0.0064 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_01.md | a92b9c2fe67de2e4… | ok |
| templating | 2 | 2026-09-27T18:34:00-03:00 | 0.0052 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_02.md | a92b9c2fe67de2e4… | ok |
| templating | 3 | 2026-09-27T18:34:00-03:00 | 0.0052 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_03.md | a92b9c2fe67de2e4… | ok |
| templating | 4 | 2026-09-27T18:34:00-03:00 | 0.005 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_04.md | a92b9c2fe67de2e4… | ok |
| templating | 5 | 2026-09-27T18:34:00-03:00 | 0.0051 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_05.md | a92b9c2fe67de2e4… | ok |
| templating | 6 | 2026-09-27T18:34:00-03:00 | 0.0051 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_06.md | a92b9c2fe67de2e4… | ok |
| templating | 7 | 2026-09-27T18:34:00-03:00 | 0.0049 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_07.md | a92b9c2fe67de2e4… | ok |
| templating | 8 | 2026-09-27T18:34:00-03:00 | 0.005 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_08.md | a92b9c2fe67de2e4… | ok |
| templating | 9 | 2026-09-27T18:34:00-03:00 | 0.0049 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_09.md | a92b9c2fe67de2e4… | ok |
| templating | 10 | 2026-09-27T18:34:00-03:00 | 0.0048 | 0.0 | 0 | 0 | 2229 | 38.93 | 4 | 100.0 |  | data/evaluation/execucoes/templating/execucao_10.md | a92b9c2fe67de2e4… | ok |
| rag | 1 | 2026-09-27T18:34:00-03:00 | 113.7942 | 111.1252 | 7605 | 719 | 498 | 40.14 | 8 | 46.9 | 83.0 | data/evaluation/execucoes/rag/execucao_01.md | 581458f10e4387d8… | ok |
| rag | 2 | 2026-09-27T18:35:57-03:00 | 88.732 | 84.4666 | 7605 | 555 | 392 | 38.47 | 7 | 43.8 | 89.5 | data/evaluation/execucoes/rag/execucao_02.md | f1f66c1b6450278b… | ok |
| rag | 3 | 2026-09-27T18:37:29-03:00 | 124.9841 | 121.3844 | 7605 | 836 | 591 | 39.16 | 10 | 50.0 | 81.8 | data/evaluation/execucoes/rag/execucao_03.md | d30bce2d0ba5284e… | ok |
| rag | 4 | 2026-09-27T18:39:37-03:00 | 124.2687 | 120.3547 | 7605 | 1075 | 757 | 37.36 | 10 | 46.9 | 86.3 | data/evaluation/execucoes/rag/execucao_04.md | e157de47299532ab… | ok |
| rag | 5 | 2026-09-27T18:41:44-03:00 | 104.1381 | 101.5073 | 7605 | 877 | 611 | 38.15 | 8 | 50.0 | 90.0 | data/evaluation/execucoes/rag/execucao_05.md | ddd2a2c8dd318230… | ok |
| rag | 6 | 2026-09-27T18:43:31-03:00 | 140.3283 | 136.9926 | 7605 | 955 | 662 | 36.58 | 10 | 46.9 | 89.9 | data/evaluation/execucoes/rag/execucao_06.md | d390e38ddc25782c… | ok |
| rag | 7 | 2026-09-27T18:45:55-03:00 | 132.0102 | 129.0704 | 7605 | 1022 | 728 | 42.76 | 10 | 46.9 | 89.2 | data/evaluation/execucoes/rag/execucao_07.md | eb4887a36b552d37… | ok |
| rag | 8 | 2026-09-27T18:48:10-03:00 | 240.9057 | 237.4763 | 7605 | 902 | 616 | 31.45 | 8 | 50.0 | 79.1 | data/evaluation/execucoes/rag/execucao_08.md | 21035d17e364db22… | ok |
| rag | 9 | 2026-09-27T18:52:14-03:00 | 123.2712 | 119.8461 | 7605 | 1028 | 727 | 42.64 | 10 | 46.9 | 88.6 | data/evaluation/execucoes/rag/execucao_09.md | 87c593248ce92798… | ok |
| rag | 10 | 2026-09-27T18:54:20-03:00 | 94.2919 | 90.9701 | 7605 | 913 | 643 | 40.38 | 10 | 50.0 | 83.0 | data/evaluation/execucoes/rag/execucao_10.md | 65362bb55cd30cf6… | ok |
| hibrido | 1 | 2026-09-27T18:55:57-03:00 | 271.2465 | 268.3899 | 6962 | 1821 | 1213 | 38.51 | 4 | 100.0 | 85.1 | data/evaluation/execucoes/hibrido/execucao_01.md | 5d57b4cca96fab55… | ok |
| hibrido | 2 | 2026-09-27T19:00:32-03:00 | 186.078 | 183.2569 | 6962 | 1923 | 1267 | 37.13 | 4 | 100.0 | 66.0 | data/evaluation/execucoes/hibrido/execucao_02.md | 7ce6017b7b65c7f4… | ok |
| hibrido | 3 | 2026-09-27T19:03:41-03:00 | 237.9663 | 235.0049 | 6962 | 1765 | 1180 | 41.38 | 4 | 100.0 | 87.4 | data/evaluation/execucoes/hibrido/execucao_03.md | 90564344a76c29da… | ok |
| hibrido | 4 | 2026-09-27T19:07:42-03:00 | 169.9763 | 167.0021 | 6962 | 1524 | 1008 | 38.75 | 4 | 93.8 | 86.5 | data/evaluation/execucoes/hibrido/execucao_04.md | b9fb6e61926cf1c7… | ok |
| hibrido | 5 | 2026-09-27T19:10:35-03:00 | 214.9941 | 212.0201 | 6962 | 2064 | 1362 | 41.16 | 4 | 100.0 | 89.1 | data/evaluation/execucoes/hibrido/execucao_05.md | 744e957c21bfdfa5… | ok |
| hibrido | 6 | 2026-09-27T19:21:40-03:00 | 184.8373 | 182.4366 | 6962 | 1836 | 1204 | 38.95 | 4 | 100.0 | 85.1 | data/evaluation/execucoes/hibrido/execucao_06.md | dc29ffa078c50621… | ok |
| hibrido | 7 | 2026-09-27T19:24:48-03:00 | 198.2784 | 195.4649 | 6962 | 1863 | 1234 | 38.41 | 4 | 100.0 | 83.9 | data/evaluation/execucoes/hibrido/execucao_07.md | 50e3e25bb6f48447… | ok |
| hibrido | 8 | 2026-09-27T19:28:09-03:00 | 258.7349 | 255.8986 | 6962 | 1730 | 1157 | 40.91 | 4 | 100.0 | 81.3 | data/evaluation/execucoes/hibrido/execucao_08.md | c05183fd182a59d3… | ok |
| hibrido | 9 | 2026-09-27T19:32:31-03:00 | 189.2259 | 186.6513 | 6962 | 1750 | 1151 | 41.97 | 4 | 100.0 | 81.8 | data/evaluation/execucoes/hibrido/execucao_09.md | 0a6f99448bab5298… | ok |
| hibrido | 10 | 2026-09-27T19:35:43-03:00 | 196.4477 | 193.6118 | 6962 | 1827 | 1216 | 37.49 | 4 | 100.0 | 91.0 | data/evaluation/execucoes/hibrido/execucao_10.md | 2cd1090ee6aa58ac… | ok |

## Execuções que falharam (descartadas e refeitas)

Uma execução em que alguma chamada à API passou do tempo limite do SDK (300 s) não termina e não tem tempo medido; ela foi refeita com o mesmo número.

| metodo | execucao | data_hora | erro |
|---|---|---|---|
| hibrido | 6 | 2026-09-27 (hora não registrada; falha anterior ao registro automático) | ReadTimeout: The read operation timed out (chamada de chat passou de 300 s) |

## Tempo do método manual (min)

| etapa | minutos | cronometro |
|---|---|---|
| total | 21.86 | 21:51.56 |

## Métricas automáticas

BERTScore em relação ao manual humano (sem reescalonamento). Cobertura explícita = artefatos citados por chave, código ou título.

| metodo | palavras | frases | palavras_por_frase | silabas_por_palavra | flesch_pt | faixa_flesch | secoes_nivel2 | cabecalhos | saltos_de_nivel | itens_de_lista | cobertura_explicita_% | texto_citado_% | bertscore_p | bertscore_r | bertscore_f1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| templating | 2229 | 197 | 11.31 | 2.345 | 38.93 | difícil | 4 | 30 | 0 | 60 | 100.0 |  | 0.7936 | 0.8859 | 0.8372 |
| rag | 600 | 41 | 14.63 | 2.268 | 42.08 | difícil | 10 | 11 | 0 | 6 | 46.9 | 78.0 | 0.803 | 0.7844 | 0.7936 |
| hibrido | 1159 | 74 | 15.66 | 2.309 | 37.61 | difícil | 4 | 27 | 0 | 15 | 100.0 | 89.2 | 0.7851 | 0.8174 | 0.8009 |
| manual | 966 | 68 | 14.21 | 2.359 | 34.83 | difícil | 7 | 8 | 0 | 10 | 18.8 |  |  |  |  |

## Variação entre execuções

| metodo | execucoes | textos_distintos | estruturas_distintas | similaridade_media | similaridade_minima |
|---|---|---|---|---|---|
| hibrido | 10 | 10 | 1 | 0.5333 | 0.3588 |
| rag | 10 | 10 | 4 | 0.6102 | 0.2829 |
| templating | 10 | 1 | 1 | 1.0 | 1.0 |

## Fidelidade e cobertura de conteúdo (anotação)

| metodo | frases | frases_verificaveis | sustentadas_% | parciais_% | nao_sustentadas_% | artefatos_cobertos | cobertura_conteudo_% |
|---|---|---|---|---|---|---|---|
| hibrido | 74 | 46 | 100.0 | 0.0 | 0.0 | 32 | 100.0 |
| manual | 68 | 53 | 98.1 | 1.9 | 0.0 | 16 | 50.0 |
| rag | 41 | 30 | 100.0 | 0.0 | 0.0 | 15 | 46.9 |
| templating | 197 | 150 | 100.0 | 0.0 | 0.0 | 32 | 100.0 |

## LLM como juiz (1 a 5)

| metodo | modelo_juiz | clareza | coerencia | completude | correcao | utilidade | afirmacoes_nao_sustentadas |
|---|---|---|---|---|---|---|---|
| templating | command-a-03-2025 | 5 | 5 | 4 | 5 | 5 | 0 |
| rag | command-a-03-2025 | 4 | 4 | 3 | 4 | 3 | 1 |
| hibrido | command-a-03-2025 | 5 | 5 | 4 | 5 | 5 | 2 |

## LLM como juiz sobre todas as execuções (1 a 5)

Mediana (mínimo–máximo) das notas dadas a cada manual salvo pelo benchmark. As execuções do templating são idênticas: a faixa delas é o ruído do próprio juiz.

| metodo | execucoes | clareza | coerencia | completude | correcao | utilidade | afirmacoes_nao_sustentadas |
|---|---|---|---|---|---|---|---|
| templating | 10 | 5 (5–5) | 5 (5–5) | 4 (4–4) | 5 (5–5) | 5 (4–5) | 0 (0–2) |
| rag | 10 | 4 (3–5) | 4 (3–5) | 3 (2–4) | 4.5 (4–5) | 3 (2–4) | 2 (0–7) |
| hibrido | 10 | 5 (4–5) | 5 (3–5) | 4 (3–4) | 5 (5–5) | 4 (3–5) | 2 (0–10) |
| manual | 1 | 5 (5–5) | 5 (5–5) | 4 (4–4) | 5 (5–5) | 5 (5–5) | 3 (3–3) |

## Comparação estatística entre os métodos

U de Mann-Whitney bilateral sobre os valores de cada execução; p ajustado por Holm dentro de cada métrica; A12 = P(execução de A > execução de B). O manual humano (1 execução) fica de fora.

| metrica | metodo_a | metodo_b | n_a | n_b | u | p | a12 | efeito | p_holm | diferenca_significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| tempo_total_s | templating | rag | 10 | 10 | 0.0 | 0.0002 | 0.0 | grande | 0.0005 | sim |
| tempo_total_s | templating | hibrido | 10 | 10 | 0.0 | 0.0002 | 0.0 | grande | 0.0005 | sim |
| tempo_total_s | rag | hibrido | 10 | 10 | 8.0 | 0.0017 | 0.08 | grande | 0.0017 | sim |
| tokens_total | templating | rag | 10 | 10 | 0.0 | 0.0001 | 0.0 | grande | 0.0002 | sim |
| tokens_total | templating | hibrido | 10 | 10 | 0.0 | 0.0001 | 0.0 | grande | 0.0002 | sim |
| tokens_total | rag | hibrido | 10 | 10 | 6.0 | 0.001 | 0.06 | grande | 0.001 | sim |
| palavras | templating | rag | 10 | 10 | 100.0 | 0.0001 | 1.0 | grande | 0.0002 | sim |
| palavras | templating | hibrido | 10 | 10 | 100.0 | 0.0001 | 1.0 | grande | 0.0002 | sim |
| palavras | rag | hibrido | 10 | 10 | 0.0 | 0.0002 | 0.0 | grande | 0.0002 | sim |
| flesch_pt | templating | rag | 10 | 10 | 50.0 | 1.0 | 0.5 | desprezível | 1.0 | não |
| flesch_pt | templating | hibrido | 10 | 10 | 50.0 | 1.0 | 0.5 | desprezível | 1.0 | não |
| flesch_pt | rag | hibrido | 10 | 10 | 44.0 | 0.6776 | 0.44 | pequeno | 1.0 | não |
| cobertura_explicita_% | templating | rag | 10 | 10 | 100.0 | 0.0001 | 1.0 | grande | 0.0002 | sim |
| cobertura_explicita_% | templating | hibrido | 10 | 10 | 55.0 | 0.3681 | 0.55 | desprezível | 0.3681 | não |
| cobertura_explicita_% | rag | hibrido | 10 | 10 | 0.0 | 0.0001 | 0.0 | grande | 0.0002 | sim |
| texto_citado_% | rag | hibrido | 10 | 10 | 59.5 | 0.4958 | 0.595 | pequeno | 0.4958 | não |
| clareza | templating | rag | 10 | 10 | 95.0 | 0.0002 | 0.95 | grande | 0.0005 | sim |
| clareza | templating | hibrido | 10 | 10 | 65.0 | 0.0767 | 0.65 | médio | 0.0767 | não |
| clareza | rag | hibrido | 10 | 10 | 17.0 | 0.0064 | 0.17 | grande | 0.0128 | sim |
| coerencia | templating | rag | 10 | 10 | 95.0 | 0.0002 | 0.95 | grande | 0.0006 | sim |
| coerencia | templating | hibrido | 10 | 10 | 65.0 | 0.0776 | 0.65 | médio | 0.0776 | não |
| coerencia | rag | hibrido | 10 | 10 | 23.0 | 0.0331 | 0.23 | grande | 0.0663 | não |
| completude | templating | rag | 10 | 10 | 95.0 | 0.0002 | 0.95 | grande | 0.0005 | sim |
| completude | templating | hibrido | 10 | 10 | 65.0 | 0.0767 | 0.65 | médio | 0.0767 | não |
| completude | rag | hibrido | 10 | 10 | 17.0 | 0.0064 | 0.17 | grande | 0.0128 | sim |
| correcao | templating | rag | 10 | 10 | 75.0 | 0.0137 | 0.75 | grande | 0.041 | sim |
| correcao | templating | hibrido | 10 | 10 | 50.0 | 1.0 | 0.5 | desprezível | 1.0 | não |
| correcao | rag | hibrido | 10 | 10 | 25.0 | 0.0137 | 0.25 | grande | 0.041 | sim |
| utilidade | templating | rag | 10 | 10 | 99.0 | 0.0001 | 0.99 | grande | 0.0003 | sim |
| utilidade | templating | hibrido | 10 | 10 | 71.0 | 0.0722 | 0.71 | médio | 0.0722 | não |
| utilidade | rag | hibrido | 10 | 10 | 7.0 | 0.0007 | 0.07 | grande | 0.0014 | sim |
| afirmacoes_nao_sustentadas | templating | rag | 10 | 10 | 8.5 | 0.0008 | 0.085 | grande | 0.0025 | sim |
| afirmacoes_nao_sustentadas | templating | hibrido | 10 | 10 | 13.0 | 0.0023 | 0.13 | grande | 0.0046 | sim |
| afirmacoes_nao_sustentadas | rag | hibrido | 10 | 10 | 53.0 | 0.8448 | 0.53 | desprezível | 0.8448 | não |
