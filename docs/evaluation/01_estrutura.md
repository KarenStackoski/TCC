# Etapa 4 — Avaliação dos manuais: métricas, fontes e como rodar

Este documento explica o que cada métrica mede, por que foi escolhida, de
onde vem (fonte) e qual script a calcula. O código fica em `src/evaluation/`
e os resultados em `data/evaluation/`.

> **Referências:** as referências acadêmicas abaixo foram conferidas em
> 2026-10-19 (seção 11 traz volume, páginas e DOI de cada uma). As de
> documentação técnica (Python, Cohere, W3C, NIST) são páginas vivas e não
> foram reconferidas.

## 1. Visão geral

A qualidade de um manual não cabe numa métrica só. Cada aspecto é medido
por uma métrica diferente, e cada métrica tem limitações próprias. Usar
várias métricas que se complementam é a recomendação da literatura de
avaliação de geração de texto (Gatt e Krahmer, 2018; van der Lee et al., 2021).

| Aspecto | Métrica | Tipo | Script |
|---|---|---|---|
| Custo de geração | tempo (mediana de N execuções), tokens | automática | `benchmark.py` |
| Fidelidade às fontes | % de frases sustentadas / não sustentadas | anotação (LLM + amostra humana) | `fidelidade.py` |
| Cobertura de conteúdo | % dos 32 artefatos presentes | anotação (LLM + amostra humana) | `fidelidade.py` |
| Cobertura explícita | % dos artefatos citados por chave, código ou título | automática | `metricas_texto.py` |
| Rastreabilidade | % do texto coberto por citações do Command R | automática | `metricas_texto.py` |
| Legibilidade | Flesch adaptado ao português | automática | `metricas_texto.py` |
| Estrutura | seções, cabeçalhos, saltos de nível, listas | automática | `metricas_texto.py` |
| Semelhança com o manual humano | BERTScore (P, R, F1) | automática | `bertscore.py` |
| Reprodutibilidade | similaridade e estrutura entre execuções | automática | `variacao.py` |
| Qualidade (aproximação) | notas de 1 a 5 em 5 critérios, em cada execução | LLM como juiz | `juiz_llm.py` |
| Diferença entre métodos | Mann-Whitney U, A12 de Vargha-Delaney, ajuste de Holm | estatística | `estatistica.py` |

**Escopo: só métricas técnicas.** O estudo não tem avaliação com usuários
(nem avaliação humana cega por terceiros, nem teste de uso). A primeira rodada
da anotação de fidelidade (seção 4) foi feita pelo Claude (Opus 5.5) e
uma amostra de 20% é reanotada pela autora. O que isso deixa de fora está na
seção 9.

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
  `data/evaluation/tempo_manual.csv`: 21 min 51,56 s, cronometrado em
  2026-10-18. Só o total foi medido; as etapas de leitura, escrita e
  revisão não foram separadas.
  Não é diretamente comparável com o tempo de máquina, e isso deve ser
  dito no texto.
- **Ressalva:** a indexação roda em toda execução do RAG (como na CLI da
  Etapa 2). Num uso real ela seria feita uma vez só. Por isso ela aparece
  separada, para dar para comparar com e sem ela.

## 3. Legibilidade e estrutura (`metricas_texto.py`)

- **Índice de Flesch adaptado ao português brasileiro:**
  `248,835 − 1,015 × (palavras/frase) − 84,6 × (sílabas/palavra)`.
  Faixas: 75–100 muito fácil; 50–75 fácil; 25–50 difícil; 0–25 muito
  difícil. Fonte: Martins, Ghiraldelo, Nunes e Oliveira Jr.,
  "Readability formulas applied to textbooks in Brazilian Portuguese",
  Notas do ICMSC-USP, Série Computação, n. 28, 1996.
- **Sílabas:** pontos de hifenização do Pyphen com os padrões pt_BR do
  LibreOffice, mais 1. Em português, a translineação segue a divisão
  silábica (Acordo Ortográfico de 1990, Base XX). Limitação conhecida:
  alguns hiatos não são separados (ex.: "usu-á-rio" conta 3 sílabas em vez
  de 4). O erro é pequeno e igual para todos os métodos, então não afeta a
  comparação entre eles.
- **Texto analisado:** só a prosa. A marcação Markdown, os comentários
  HTML (`<!-- … -->`, que o leitor não vê) e o rodapé de citações saem, e
  títulos sem ponto final contam como frase própria.
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
- **Regras de anotação:** em `02_guia_fidelidade.md`: rótulos, regras de
  decisão (status dos artefatos, melhorias, bugs, números), o tipo de erro
  (intrínseco ou extrínseco) e a pista `fonte_declarada` das planilhas.
- **Quem anotou:** a primeira rodada completa (296 frases, 2026-10-19)
  foi feita pelo Claude (modelo Opus 5.5, `claude-opus-5-5`), seguindo o
  guia com as regras de decisão sugeridas nele. A autora reanota, às
  cegas, uma amostra sorteada de 20% (61 frases).
- **Concordância:** a reanotação da autora contra a primeira rodada dá a
  concordância **entre anotadores** (LLM × pessoa), pelo kappa de Cohen
  (`reanotacao.py`; guia, seção 8). Isso também valida o uso da LLM como
  anotadora: se o kappa for baixo, a primeira rodada não pode ser usada
  como está.

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
  1988.
- **Estrutura:** quantas listas diferentes de seções de nível 2
  apareceram. O esperado é 1 no templating e no híbrido (estrutura fixa) e
  mais de 1 no RAG (a LLM decide a estrutura).
- O templating deve ter similaridade 1,0 e 1 texto distinto. Isso
  confirma a legenda da Figura 1 ("a mesma entrada gera sempre a mesma saída").

## 7. LLM como juiz (`juiz_llm.py`)

- **Método:** avaliação de resposta única de Zheng et al., "Judging
  LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023. Os
  critérios são dados explicitamente, e o juiz justifica antes de dar a
  nota, como em Liu et al., "G-Eval", EMNLP 2023.
- **Critérios:** clareza, coerência, completude, correção e utilidade,
  numa escala de 1 a 5, com as definições em `CRITERIOS`. Eles se baseiam
  nos critérios mais usados em avaliação humana de NLG (van der Lee et
  al., "Human evaluation of automatically generated text: Current trends
  and best practice guidelines", Computer Speech & Language, 2021) e na
  finalidade de um manual de usuário (ISO/IEC/IEEE 26514).
- **Configuração:** juiz `command-a-03-2025` com temperatura 0 e saída em
  JSON Schema (Cohere, "Structured Outputs"). O juiz recebe os 32
  artefatos, para julgar a correção e listar afirmações sem apoio. O
  manual vai anonimizado: o rodapé de citações e a linha "Documento gerado
  automaticamente — Etapa 1" saem (`manuais.anonimizar`).
- **Todas as execuções (`--execucoes`):** o juiz avalia cada manual salvo
  pelo benchmark (10 por método automático) e o manual humano, e não só
  um manual por método. RAG e híbrido mudam muito de uma execução para
  outra (seção 6), então a nota de um manual só não representa o método.
  O resultado é uma distribuição de notas por método, que entra nos
  testes da seção 8. Cada avaliação fica em
  `data/evaluation/juiz_llm/execucoes/<metodo>/execucao_NN.json`, com o
  SHA-256 do arquivo julgado; o resumo fica em `resultado_execucoes.csv`.
- **Ruído do juiz:** as 10 execuções do templating são o mesmo texto (seção
  6). Se as notas delas variam, essa variação é do juiz, mesmo com
  temperatura 0. Ela serve de linha de base: uma diferença entre métodos
  menor que esse ruído não deve ser interpretada.
- **Vieses, a registrar no TCC:**
  1. Autopreferência: o juiz é da mesma empresa do gerador (Command R) e
     pode favorecer os métodos 2 e 3. Fonte: Panickssery, Bowman e Feng,
     "LLM Evaluators Recognize and Favor Their Own Generations", NeurIPS 2024.
  2. Verbosidade: tendência a preferir textos mais longos (Zheng et al., 2023).
  3. Sem validação contra notas humanas: como o estudo não tem avaliação
     com usuários, não se sabe quanto as notas do juiz concordam com as de
     uma pessoa. Elas são uma aproximação da qualidade, não uma medida
     dela. A medida principal de correção é a anotação de fidelidade
     (seção 4).

## 8. Comparação estatística entre os métodos (`estatistica.py`)

- **Por quê:** RAG e híbrido são aleatórios (cada execução dá um texto
  diferente). Comparar duas medianas não diz se a diferença é maior que a
  variação natural entre execuções. Protocolo: Arcuri e Briand, "A
  practical guide for using statistical tests to assess randomized
  algorithms in software engineering", ICSE 2011, que recomendam um teste
  não paramétrico e um tamanho de efeito sobre várias execuções.
- **Dados:** os valores de cada execução. Do benchmark: tempo total, tokens
  (entrada + saída), palavras, Flesch, cobertura explícita e texto
  citado. Do juiz com `--execucoes`: as 5 notas e o número de afirmações
  não sustentadas.
- **Teste:** U de Mann-Whitney bilateral, para cada par de métodos. Não
  supõe distribuição normal (o tempo, por exemplo, tem cauda longa por
  causa da rede). Fontes: Mann e Whitney, "On a Test of Whether One of Two
  Random Variables is Stochastically Larger than the Other", The Annals of
  Mathematical Statistics, 1947; implementação `scipy.stats.mannwhitneyu`
  (Virtanen et al., "SciPy 1.0", Nature Methods, 2020). Quando os dois
  grupos têm todos os valores iguais (ex.: nota 5 em todas as execuções),
  não há diferença a testar, e p = 1.
- **Tamanho do efeito:** A12 de Vargha e Delaney, a probabilidade de uma
  execução do método A ter valor maior que uma do método B (empate conta
  meio; 0,5 = sem diferença). Faixas: |A12 − 0,5| < 0,06 desprezível;
  < 0,14 pequeno; < 0,21 médio; acima disso, grande. Fonte: Vargha e
  Delaney, "A Critique and Improvement of the CL Common Language Effect
  Size Statistics of McGraw and Wong", Journal of Educational and
  Behavioral Statistics, 2000. Com n = 10, o p diz se a diferença existe;
  o A12 diz se ela importa.
- **Comparações múltiplas:** cada métrica tem 3 comparações (templating ×
  RAG, templating × híbrido, RAG × híbrido). O p é ajustado pelo método de
  Holm dentro de cada métrica, com α = 0,05. Fonte: Holm, "A Simple
  Sequentially Rejective Multiple Test Procedure", Scandinavian Journal of
  Statistics, 1979.
- **Manual humano:** é uma execução só, então fica de fora dos testes. Os
  valores dele são descritos ao lado dos outros, sem teste.
- **Ressalva:** as comparações com o templating, nas métricas do texto,
  são triviais. O templating tem variância zero, então qualquer variação
  do outro método já o separa. O que importa nesses casos é o A12 e o
  sentido da diferença.
- Resultado em `data/evaluation/estatistica.csv` e na seção "Comparação
  estatística entre os métodos" de `resultados.md`.

## 9. Ameaças à validade (escopo sem usuários)

O estudo usa só métricas técnicas. Isso deve aparecer no texto do TCC,
seguindo a classificação de Wohlin et al., *Experimentation in Software
Engineering*, Springer, 2012 (validade de construto, interna, externa e
de conclusão):

- **Construto:** nenhuma métrica mede diretamente se um usuário consegue
  usar o sistema com o manual. Flesch, estrutura e cobertura são
  aproximações. A utilidade do juiz é a opinião de uma LLM, e essa
  opinião não foi validada contra a de pessoas. O BERTScore mede
  semelhança com o manual da autora, não qualidade.
- **Interna:** a primeira rodada da fidelidade foi anotada por uma LLM
  (Claude), que pode ser leniente com textos gerados por outra LLM; só
  20% das frases têm anotação humana (a da autora, que também escreveu o
  manual humano e não está cega para o método). O juiz pode favorecer os textos
  da Cohere (seção 7).
- **Externa:** há um único projeto de entrada (os 32 artefatos de
  `data/raw/data.json`) e um único provedor de LLM. Os resultados não se
  generalizam para outros projetos ou modelos sem nova medição.
- **Conclusão:** n = 10 execuções por método, e a anotação de fidelidade é
  sobre 1 manual por método.
- **Trabalho futuro:** avaliação com usuários (avaliação humana cega com
  concordância entre avaliadores, ou teste de uso com tarefas), seguindo
  van der Lee et al. (2021).

## 10. Como rodar (ordem sugerida)

```
# 1. Tempo e tokens (cria também as execuções usadas na variação)
python -m src.evaluation.benchmark --repeticoes 10   # já rodado em 2026-09-27

# 2. Registrar à mão o tempo do método manual
#    data/evaluation/tempo_manual.csv  (etapa,minutos,cronometro) — já preenchido

# 3. Fidelidade: gera as planilhas; anotar; depois analisar
python -m src.evaluation.fidelidade preparar
python -m src.evaluation.fidelidade analisar
#    Reanotação (concordância LLM × autora): sortear só com a 1ª rodada
#    completa; a autora reanota sem abrir a 1ª rodada (guia, seção 8)
#    Sorteio já feito em 2026-10-19 (semente 2026, 61 frases)
python -m src.evaluation.reanotacao sortear --fracao 0.2 --semente 2026
python -m src.evaluation.reanotacao concordancia

# 4. LLM como juiz
python -m src.evaluation.juiz_llm               # 1 manual por método (4 chamadas)
python -m src.evaluation.juiz_llm --execucoes   # cada execução (31 chamadas)

# 5. Relatório consolidado (métricas automáticas, testes estatísticos e
#    tudo que já existir)
python -m src.evaluation.relatorio
```

Consumo do plano Trial da Cohere com 10 repetições: RAG = 3 chamadas por
execução (2 de embed, 1 de chat); híbrido = 4 chamadas de chat por execução;
juiz = 1 chamada por manual (4 no modo simples, 31 com `--execucoes`).
Total: cerca de 105 chamadas, bem abaixo do limite de 1.000 por mês. O
`--execucoes` não refaz uma avaliação já salva do mesmo arquivo; quando o
manual humano entrar, só ele é avaliado. Uma chave Trial nunca gera
cobrança: se o limite acabar, a API só passa a recusar as chamadas
(Cohere, "Rate Limits").

## 11. Referências conferidas (2026-10-19)

Conferidas no registro do editor, no repositório institucional ou em
indexadores (ACL Anthology, Project Euclid, JSTOR, OpenReview, NeurIPS
Proceedings).

- Arcuri, A.; Briand, L. A practical guide for using statistical tests to
  assess randomized algorithms in software engineering. ICSE 2011.
  DOI 10.1145/1985793.1985795.
- Cohen, J. A Coefficient of Agreement for Nominal Scales. Educational and
  Psychological Measurement, v. 20, n. 1, p. 37–46, 1960.
  DOI 10.1177/001316446002000104.
- Gatt, A.; Krahmer, E. Survey of the State of the Art in Natural Language
  Generation: Core Tasks, Applications and Evaluation. Journal of
  Artificial Intelligence Research, v. 61, p. 65–170, 2018.
  DOI 10.1613/jair.5477. (O arXiv indica v. 60, 2017; cite a versão do JAIR.)
- Georges, A.; Buytaert, D.; Eeckhout, L. Statistically Rigorous Java
  Performance Evaluation. OOPSLA 2007, p. 57–76.
- Holm, S. A Simple Sequentially Rejective Multiple Test Procedure.
  Scandinavian Journal of Statistics, v. 6, n. 2, p. 65–70, 1979.
- Ji, Z. et al. Survey of Hallucination in Natural Language Generation.
  ACM Computing Surveys, v. 55, n. 12, art. 248, 2023. (Volume e número de
  artigo vistos só em indexador; confira o DOI na ACM Digital Library.)
- Landis, J. R.; Koch, G. G. The Measurement of Observer Agreement for
  Categorical Data. Biometrics, v. 33, n. 1, p. 159–174, 1977.
  DOI 10.2307/2529310.
- Liu, Y. et al. G-Eval: NLG Evaluation using GPT-4 with Better Human
  Alignment. EMNLP 2023, p. 2511–2522.
- Mann, H. B.; Whitney, D. R. On a Test of Whether One of Two Random
  Variables is Stochastically Larger than the Other. The Annals of
  Mathematical Statistics, v. 18, n. 1, p. 50–60, 1947.
  DOI 10.1214/aoms/1177730491.
- Martins, T. B. F.; Ghiraldelo, C. M.; Nunes, M. G. V.; Oliveira Jr.,
  O. N. Readability formulas applied to textbooks in Brazilian Portuguese.
  Notas do ICMSC, Série Computação, n. 28. São Carlos: ICMSC-USP, jun. 1996.
  ISSN 0103-2577. Conferido no PDF do Repositório da USP (item 000906089):
  o relatório usa a fórmula original de Flesch (206,835 − 84,6 × sílabas/
  palavra − 1,015 × palavras/frase) e soma 42 pontos aos textos em
  português (p. 6), o que dá a constante 248,835 do código; as faixas
  (75–100, 50–75, 25–50, < 25) estão nas p. 3–4 e 7.
- Maynez, J.; Narayan, S.; Bohnet, B.; McDonald, R. On Faithfulness and
  Factuality in Abstractive Summarization. ACL 2020, p. 1906–1919.
  DOI 10.18653/v1/2020.acl-main.173.
- Panickssery, A.; Bowman, S. R.; Feng, S. LLM Evaluators Recognize and
  Favor Their Own Generations. NeurIPS 2024. DOI 10.52202/079017-2197.
- Ratcliff, J. W.; Metzener, D. E. Pattern Matching: The Gestalt Approach.
  Dr. Dobb's Journal, n. 46, jul. 1988. (O algoritmo é de Ratcliff e
  Obershelp, 1983; o artigo que o publicou é de Ratcliff e Metzener.)
- Reiter, E. A Structured Review of the Validity of BLEU. Computational
  Linguistics, v. 44, n. 3, p. 393–401, 2018. DOI 10.1162/coli_a_00322.
- van der Lee, C.; Gatt, A.; van Miltenburg, E.; Krahmer, E. Human
  evaluation of automatically generated text: Current trends and best
  practice guidelines. Computer Speech & Language, v. 67, art. 101151,
  2021.
- Vargha, A.; Delaney, H. D. A Critique and Improvement of the CL Common
  Language Effect Size Statistics of McGraw and Wong. Journal of
  Educational and Behavioral Statistics, v. 25, n. 2, p. 101–132, 2000.
  DOI 10.3102/10769986025002101. (Os limiares 0,56 / 0,64 / 0,71 foram
  vistos só em fontes secundárias; o artigo é pago. Confira na p. do
  artigo antes de citar os limiares.)
- Virtanen, P. et al. SciPy 1.0: fundamental algorithms for scientific
  computing in Python. Nature Methods, v. 17, n. 3, p. 261–272, 2020.
  DOI 10.1038/s41592-019-0686-2.
- Wohlin, C.; Runeson, P.; Höst, M.; Ohlsson, M. C.; Regnell, B.;
  Wesslén, A. Experimentation in Software Engineering. Berlin: Springer,
  2012. (Os quatro tipos de validade são os do livro; a página do editor
  não foi aberta.)
- Zhang, T.; Kishore, V.; Wu, F.; Weinberger, K. Q.; Artzi, Y. BERTScore:
  Evaluating Text Generation with BERT. ICLR 2020.
  https://openreview.net/forum?id=SkeHuCVFDr.
- Zheng, L. et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.
  NeurIPS 2023, Datasets and Benchmarks Track.
