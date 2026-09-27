# Etapa 4 — Avaliação dos manuais: métricas, fontes e como rodar

Este documento explica o que cada métrica mede, por que foi escolhida, de
onde vem (fonte) e qual script a calcula. O código fica em `src/evaluation/`
e os resultados em `data/evaluation/`.

> **Aviso sobre as referências:** as referências acadêmicas abaixo foram
> escritas de memória (autores, título, local e ano). Confira cada uma na
> fonte original antes de citar no TCC, principalmente as marcadas com (*).

## 1. Visão geral

A qualidade de um manual não cabe numa métrica só. Cada aspecto é medido
por uma métrica diferente, e cada métrica tem limitações próprias. Usar
várias métricas que se complementam é a recomendação da literatura de
avaliação de geração de texto (Gatt e Krahmer, 2018; van der Lee et al., 2021).

| Aspecto | Métrica | Tipo | Script |
|---|---|---|---|
| Custo de geração | tempo (mediana de N execuções), tokens | automática | `benchmark.py` |
| Fidelidade às fontes | % de frases sustentadas / não sustentadas | anotação humana | `fidelidade.py` |
| Cobertura de conteúdo | % dos 32 artefatos presentes | anotação humana | `fidelidade.py` |
| Cobertura explícita | % dos artefatos citados por chave, código ou título | automática | `metricas_texto.py` |
| Rastreabilidade | % do texto coberto por citações do Command R | automática | `metricas_texto.py` |
| Legibilidade | Flesch adaptado ao português | automática | `metricas_texto.py` |
| Estrutura | seções, cabeçalhos, saltos de nível, listas | automática | `metricas_texto.py` |
| Semelhança com o manual humano | BERTScore (P, R, F1) | automática | `bertscore.py` |
| Reprodutibilidade | similaridade e estrutura entre execuções | automática | `variacao.py` |
| Qualidade percebida | notas de 1 a 5 em 5 critérios, alfa de Krippendorff | avaliação humana cega | `avaliacao_humana.py` |
| Qualidade (complemento) | as mesmas notas, dadas por uma LLM | LLM como juiz | `juiz_llm.py` |

O manual humano (método 4) deve estar em `data/manuals_generated/manual/manual.md`
(ou informe outro caminho com `--manual-humano`). Sem ele, os scripts
rodam para os outros três métodos, e o BERTScore não é calculado.

## 2. Tempo e tokens (`benchmark.py`, `medicao.py`)

- **Relógio:** `time.perf_counter()`, monotônico e de maior resolução.
  Fonte: documentação do Python, módulo `time`.
- **Repetições:** cada método roda N vezes sobre a mesma entrada. A medição
  do TCC usou N = 10: é o suficiente para a mediana ser estável e cabe com
  folga no limite gratuito da Cohere (cerca de 70 das 1.000 chamadas do mês).
  O relatório traz mediana, mínimo, máximo e desvio-padrão. A latência de
  rede e da API varia de uma execução para outra (no teste, a mesma geração
  RAG levou de 80 s a 239 s), então uma medição só não se sustenta. Fonte:
  Georges, Buytaert e Eeckhout, "Statistically Rigorous Java Performance
  Evaluation", OOPSLA 2007. A mediana foi escolhida por ser robusta a
  valores extremos (uma execução lenta por causa da rede não distorce o
  resultado).
- **Sem custo de inicialização:** os módulos de cada etapa são importados
  antes de qualquer medição. Se fossem importados na primeira chamada, só a
  execução nº 1 pagaria o tempo de importação (no templating, 0,034 s contra
  0,005 s das outras). Esse efeito de inicialização contra regime
  permanente também é discutido por Georges et al. (2007).
- **Prova de cada execução:** cada manual gerado fica salvo em
  `data/evaluation/execucoes/<metodo>/execucao_NN.md`, com a data e hora de
  início e o hash SHA-256 do arquivo registrados em `tempos.csv`. O
  relatório recalcula o hash e marca `integridade = ok` quando o arquivo
  continua igual ao que foi gerado e medido. Fontes: NIST FIPS 180-4
  (Secure Hash Standard); documentação do Python, módulo `hashlib`. O CSV é
  gravado depois de cada execução, então uma falha no meio não perde o que
  já foi medido.
- **Falhas de rede:** o SDK da Cohere desiste de uma chamada depois de
  300 s (tempo limite padrão do cliente). Uma execução assim não termina e
  não tem tempo medido: ela é registrada em `data/evaluation/falhas.csv` e
  refeita com o mesmo número. Na medição do TCC, isso aconteceu uma vez (na
  execução 6 do híbrido). O texto deve relatar isso, porque a mediana foi
  calculada só sobre as execuções que terminaram, ou seja, ela subestima
  um pouco os casos mais lentos. `--a-partir-de N` continua uma medição
  interrompida sem refazer as execuções já válidas.
- **Fases:** o tempo de cada chamada à API é separado por tipo. Embed de
  documentos = indexação; embed de consultas = recuperação; chat =
  geração. O restante (`tempo_local_s`) é processamento local: Chroma,
  Jinja2 e montagem do texto.
- **Como a medição é feita:** `RegistroChamadas` envolve temporariamente
  `cohere.ClientV2.chat` e `embed` durante a execução. O código de geração
  medido é o mesmo das Etapas 1 a 3, sem nenhuma alteração.
- **Tokens:** vêm de `usage.billed_units` (chat) e de `meta.billed_units`
  (embed), que é o que a Cohere cobra. Fonte: Cohere, Chat API reference e
  Embed API reference.
- **Limite do plano Trial da Cohere:** se a API responder "429 Too Many
  Requests", a execução interrompida é descartada e refeita do zero depois
  de 60 s. Assim, a espera não entra no tempo medido. Fonte: Cohere,
  "Rate Limits".
- **Método manual:** o tempo é cronometrado à mão e registrado em
  `data/evaluation/tempo_manual.csv` (etapas: leitura, escrita, revisão).
  Não é diretamente comparável com o tempo de máquina, e isso deve ser
  dito no texto.
- **Ressalva:** a indexação roda em toda execução do RAG (como na CLI da
  Etapa 2). Num uso real ela seria feita uma vez só. Por isso ela aparece
  separada, para dar para comparar com e sem ela.

## 3. Legibilidade e estrutura (`metricas_texto.py`)

- **Índice de Flesch adaptado ao português brasileiro:**
  `248,835 − 1,015 × (palavras/frase) − 84,6 × (sílabas/palavra)`.
  Faixas: 75–100 muito fácil; 50–75 fácil; 25–50 difícil; 0–25 muito
  difícil. Fonte (*): Martins, Ghiraldelo, Nunes e Oliveira Jr.,
  "Readability formulas applied to textbooks in Brazilian Portuguese",
  Notas do ICMSC-USP, Série Computação, n. 28, 1996.
- **Sílabas:** pontos de hifenização do Pyphen com os padrões pt_BR do
  LibreOffice, mais 1. Em português, a translineação segue a divisão
  silábica (Acordo Ortográfico de 1990, Base XX). Limitação conhecida:
  alguns hiatos não são separados (ex.: "usu-á-rio" conta 3 sílabas em vez
  de 4). O erro é pequeno e igual para todos os métodos, então não afeta a
  comparação entre eles.
- **Texto analisado:** só a prosa. A marcação Markdown e o rodapé de
  citações saem, e títulos sem ponto final contam como frase própria.
- **Estrutura:** contagem de cabeçalhos por nível, seções de nível 2,
  itens de lista, linhas de tabela e "saltos de nível" (ex.: `##` seguido
  de `####`), que quebram a hierarquia. Fonte: W3C, WCAG 2.2, técnica
  G141, "Organizing a page using headings".

## 4. Fidelidade e cobertura (`fidelidade.py`, `metricas_texto.py`)

- **Fidelidade (anotação humana):** cada frase do manual recebe um rótulo:
  S (sustentada pelos artefatos), P (parcialmente), N (não sustentada, ou
  seja, alucinação) ou `-` (sem conteúdo verificável). Na mesma linha vão
  as chaves dos artefatos de onde a frase veio. Fontes: Maynez et al., "On
  Faithfulness and Factuality in Abstractive Summarization", ACL 2020
  (anotação humana de fidelidade); Ji et al., "Survey of Hallucination in
  Natural Language Generation", ACM Computing Surveys, 2023 (definição de
  alucinação).
- **Cobertura de conteúdo (anotação):** a proporção dos 32 artefatos que
  aparecem em alguma frase anotada.
- **Cobertura explícita (automática):** a proporção dos artefatos citados
  por chave (SCRUM-12), código (US-06) ou nome do título. É só um apoio:
  um texto pode tratar de um artefato sem citá-lo.
- **Texto citado (automático, métodos 2 e 3):** a proporção dos caracteres
  do corpo cobertos por algum trecho que o Command R citou. Mede
  rastreabilidade (quanto do texto aponta para uma fonte), não correção.
  Fonte: Cohere, "Retrieval Augmented Generation (RAG)".
- **Recomendação:** se possível, uma segunda pessoa anota uma parte das
  frases, para medir a concordância da anotação (van der Lee et al., 2021).

## 5. BERTScore (`bertscore.py`)

- **Fórmula:** a de Zhang et al., "BERTScore: Evaluating Text Generation
  with BERT", ICLR 2020. É o casamento guloso por similaridade de cosseno
  entre embeddings contextuais, com P, R e F1.
- **Modelo e camada:** os padrões do pacote `bert_score` para textos fora
  do inglês: `bert-base-multilingual-cased`, camada 9.
- **Por que não chamar `bert_score.score()` direto:** o BERT aceita 512
  tokens por vez, e a biblioteca corta o resto sem avisar. Aqui o texto é
  dividido em janelas de 510 tokens, e o casamento é feito sobre todos os
  tokens. Para um texto que cabe numa janela, o resultado é idêntico ao
  do pacote oficial (testado em `tests/test_evaluation_bertscore.py`).
- **Referência:** o manual humano.
- **Ressalvas para o texto do TCC:**
  1. O BERTScore mede semelhança com o manual humano, não qualidade
     absoluta. Ele favorece o método que escreve de forma parecida com a
     autora.
  2. Os valores não foram reescalonados (o pacote não tem linha de base
     para o português), então ficam comprimidos perto do topo da escala.
     Compare os métodos entre si, não com um limiar.
- **Por que não BLEU/ROUGE:** BLEU não tem validade demonstrada para
  avaliar geração de texto fora da tradução automática. Fonte: Reiter, "A
  Structured Review of the Validity of BLEU", Computational Linguistics,
  2018.

## 6. Variação entre execuções (`variacao.py`)

- Compara, par a par, os manuais salvos pelo benchmark em
  `data/evaluation/execucoes/<metodo>/`.
- **Similaridade:** `difflib.SequenceMatcher.ratio()` sobre as palavras
  (2·M/T). Fontes: documentação do Python, módulo `difflib`; Ratcliff e
  Metzener, "Pattern Matching: The Gestalt Approach", Dr. Dobb's Journal,
  1988 (*).
- **Estrutura:** quantas listas diferentes de seções de nível 2
  apareceram. O esperado é 1 no templating e no híbrido (estrutura fixa) e
  mais de 1 no RAG (a LLM decide a estrutura).
- O templating deve ter similaridade 1,0 e 1 texto distinto. Isso
  confirma a legenda da Figura 1 ("a mesma entrada gera sempre a mesma saída").

## 7. Avaliação humana cega (`avaliacao_humana.py`)

- **Critérios:** clareza, coerência, completude, correção e utilidade,
  numa escala Likert de 1 a 5, com as definições em `CRITERIOS`. Eles se
  baseiam nos critérios mais usados em avaliação humana de NLG (van der
  Lee et al., "Human evaluation of automatically generated text: Current
  trends and best practice guidelines", Computer Speech & Language, 2021)
  e na finalidade de um manual de usuário (ISO/IEC/IEEE 26514).
- **Cegamento:** os manuais viram `manual_A.md` a `manual_D.md`, em ordem
  sorteada (semente registrada em `gabarito.json`). O rodapé de citações e
  a linha "Documento gerado automaticamente — Etapa 1" saem.
  - Limitação: a estrutura (as 4 seções fixas) e o estilo ainda podem
    denunciar o método. Isso deve ser registrado no texto.
- **Avaliadores:** pelo menos 2, avaliando de forma independente. Um
  formulário por avaliador vai em `respostas/<nome>.csv`.
- **Concordância:** alfa de Krippendorff no nível ordinal, adequado para
  Likert, porque as notas têm ordem mas a distância entre elas não é
  garantidamente igual. A unidade é o par (manual, critério), já que 4
  manuais por critério seriam poucos para um alfa estável. Fontes:
  Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 2.
  ed., Sage, 2004; pacote `krippendorff` (Castro).
  - Interpretação usual (Krippendorff, 2004): α ≥ 0,800 é confiável;
    0,667 ≤ α < 0,800 permite só conclusões provisórias.

## 8. LLM como juiz (`juiz_llm.py`)

- **Método:** avaliação de resposta única de Zheng et al., "Judging
  LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023. Os
  critérios são dados explicitamente, e o juiz justifica antes de dar a
  nota, como em Liu et al., "G-Eval", EMNLP 2023. Os critérios e as
  definições são os mesmos da avaliação humana.
- **Configuração:** juiz `command-a-03-2025` com temperatura 0 e saída em
  JSON Schema (Cohere, "Structured Outputs"). O juiz recebe os 32
  artefatos, para julgar a correção e listar afirmações sem apoio.
- **Vieses, a registrar no TCC:**
  1. Autopreferência: o juiz é da mesma empresa do gerador (Command R) e
     pode favorecer os métodos 2 e 3. Fonte: Panickssery, Bowman e Feng,
     "LLM Evaluators Recognize and Favor Their Own Generations", NeurIPS 2024.
  2. Verbosidade: tendência a preferir textos mais longos (Zheng et al., 2023).
- É um complemento. O resultado principal de qualidade é a avaliação humana.

## 9. Como rodar (ordem sugerida)

```
# 1. Tempo e tokens (cria também as execuções usadas na variação)
python -m src.evaluation.benchmark --repeticoes 10   # já rodado em 2026-09-27

# 2. Registrar à mão o tempo do método manual
#    data/evaluation/tempo_manual.csv  (etapa,minutos)

# 3. Fidelidade: gera as planilhas; anotar; depois analisar
python -m src.evaluation.fidelidade preparar
python -m src.evaluation.fidelidade analisar

# 4. Avaliação humana: gera o pacote cego; avaliadores preenchem; analisar
python -m src.evaluation.avaliacao_humana preparar --semente 2026
python -m src.evaluation.avaliacao_humana analisar

# 5. LLM como juiz (4 chamadas à API)
python -m src.evaluation.juiz_llm

# 6. Relatório consolidado (métricas automáticas + tudo que já existir)
python -m src.evaluation.relatorio
```

Consumo do plano Trial da Cohere com 10 repetições: RAG = 3 chamadas por
execução (2 de embed, 1 de chat); híbrido = 4 chamadas de chat por execução;
juiz = 1 chamada por manual. Total: cerca de 75 chamadas, bem abaixo do
limite de 1.000 por mês. Uma chave Trial nunca gera cobrança: se o limite
acabar, a API só passa a recusar as chamadas (Cohere, "Rate Limits").
