# Progresso do TCC — log de sessões

> Log de retomada de contexto entre sessões de trabalho. Cada entrada
> resume o que foi feito, decisões tomadas (e por quê) e o que falta.
> Detalhe técnico completo da Etapa 1 fica em `docs/templating/01_estrutura.md`
> (arquitetura) e `docs/templating/02_referencias.md` (linha a linha, com
> fontes).

## Sessão 1 — 2026-08-10 — Etapa 1 (Templating puro) concluída

### Contexto do projeto
TCC compara três abordagens para gerar manuais de usuário a partir de
artefatos do Jira: (1) Templating puro (Jinja2), (2) RAG com Claude +
Cohere command-r, (3) Híbrido. Etapa 1 é a baseline determinística, sem
IA. Toda técnica usada no código precisa ter fonte/referência válida —
isso é levado a sério nesse projeto (é TCC).

### O que existe no repositório agora

```
src/common/schema.py                          # Artefato, Subtarefa (dataclasses puras)
src/jira/adf_parser.py                        # adf_to_markdown, extract_bullet_items_after_label, strip_section_after_label
src/jira/extractor.py                         # fetch_issues (API), parse_issue/parse_issues (JSON -> Artefato)
src/templating/generator.py                   # classificar_por_tipo, gerar_manual, main() (CLI)
src/templating/templates/manual_template.md.j2
tests/test_adf_parser.py                      # 10 testes, todos passando
data/raw/data.json                            # export real (fictício) do Jira, já usado para validar tudo
data/manuals_generated/templating/manual.md   # saída gerada e conferida manualmente
docs/templating/01_estrutura.md               # arquitetura da Etapa 1, com fontes
docs/templating/02_referencias.md             # referência linha a linha de cada arquivo
requirements.txt, .env.example, pytest.ini
```

Pipeline roda ponta a ponta com `python -m src.templating.generator`
(lê `data/raw/data.json`, escreve `data/manuals_generated/templating/manual.md`).
O `.gitignore` **não** ignora `data/raw/` — os dados são fictícios, o
usuário pediu explicitamente para versionar.

### Decisões tomadas nesta sessão (confirmadas com o usuário, não presumidas)

1. **Sem subtarefas neste dataset** → o "passo a passo" da seção
   Funcionalidades usa os **Critérios de Aceitação** das Stories em vez
   de subtarefas (fonte: Cohn, 2004, *User Stories Applied*). O template
   também sabe usar subtarefas via `{% elif artefato.subtarefas %}` caso
   um export futuro as tenha — as duas fontes nunca aparecem juntas no
   mesmo artefato.
2. **Tipo "Request" (não existe tipo "Task" neste dataset)** → mapeado
   para a seção "Tarefas Operacionais" em `TIPO_PARA_CATEGORIA`
   (`src/templating/generator.py`). "História" (nome em PT-BR) mapeado
   para "Story".
3. **Campos ausentes no export real** (`priority`, `assignee`, `labels`,
   `subtasks` não aparecem em nenhuma issue) → viraram opcionais em
   `Artefato`, não obrigatórios.
4. **Endpoint do Jira**: o export real só tem `isLast` no nível raiz (sem
   `startAt`/`total`), o que indica o endpoint novo
   `GET /rest/api/3/search/jql` (paginação por `nextPageToken`), não o
   clássico `/rest/api/3/search`. `extractor.py` foi implementado contra
   esse endpoint.
5. **Segredos do Jira**: usuário já tem a API validada no Postman
   (Basic Auth e-mail + token); `extractor.py` espera `JIRA_DOMAIN`,
   `JIRA_EMAIL`, `JIRA_API_TOKEN` em `.env` (ver `.env.example`).

### Bug encontrado e corrigido nesta sessão
Primeira geração do manual duplicava os critérios de aceitação (uma vez
dentro da descrição corrida, outra vez como lista numerada "Passo a
passo"). Corrigido adicionando `strip_section_after_label()` em
`adf_parser.py`, usada em `extractor.py` para gerar a descrição sem
repetir a seção já extraída separadamente. 3 testes novos cobrindo isso.
Manual regenerado e conferido — sem duplicação.

### Estado final da Etapa 1
- 10/10 testes passando (`pytest`).
- Manual gerado a partir de dados reais (32 artefatos: 6 Epic, 15 Story,
  7 Bug, 4 Request) sem erros nem duplicação.
- Nada commitado ainda (usuário não pediu commit nesta sessão) — só
  arquivos criados/staged no working tree.

### Para a próxima sessão
- Etapa 1 está funcionalmente pronta; ainda não revisada a fundo pelo
  usuário (ele disse que ia conferir `docs/templating/02_referencias.md`
  ponto a ponto — pode trazer correções/perguntas na próxima sessão).
- Próximo passo natural: Etapa 2 (RAG com Claude + Cohere command-r),
  reaproveitando `src/common/schema.py` e `src/jira/extractor.py` sem
  alteração — é o ponto de integração entre as etapas.
- Nenhuma chave de API (Cohere/Anthropic) configurada ainda — `.env.example`
  já tem os placeholders (`COHERE_API_KEY`, `ANTHROPIC_API_KEY`).

## Sessão 2 — 2026-08-29 — Etapa 2 (RAG) implementada, aguardando execução ponta a ponta

### Decisões tomadas nesta sessão (confirmadas com o usuário, não presumidas)

1. **Duas variantes de geração, mesma recuperação**: a Etapa 2 passou a
   gerar **dois manuais** (`manual_cohere.md` e `manual_claude.md`), não
   um — o usuário pediu explicitamente "um só com a Cohere... e um que
   combine o RAG da Cohere e a geração do Claude". As duas variantes usam
   exatamente os mesmos artefatos recuperados (mesma indexação/busca);
   só o modelo que escreve o texto final muda. Isso isola a variável
   "qual LLM gera o texto" como um experimento controlado — ver
   `docs/rag/01_estrutura.md`, seção 1.1.
2. **Cohere faz embeddings, Claude não tem endpoint de embeddings**: a
   Anthropic não oferece embeddings na API do Claude (confirmado na
   documentação oficial, recomenda Voyage AI como parceira) — por isso a
   recuperação usa Cohere Embed v4 nas duas variantes, e só a geração
   muda entre Command R (Cohere) e Messages API (Claude). Não é uma
   escolha de estilo, é uma restrição real da API — ver seção 1.2 do
   documento de arquitetura.
3. **Sem LangChain**: decisão do usuário ("pode seguir sem langchain"),
   depois de eu explicar o tradeoff — chamadas diretas aos SDKs oficiais
   (`cohere`, `chromadb`, `anthropic`) em vez de abstrações de framework,
   pelo mesmo motivo de citabilidade linha a linha que guiou a Etapa 1.
   `langchain`/`langchain-core` continuam instalados no venv mas não são
   mais importados por nenhum módulo.
4. **Granularidade de indexação**: um chunk = um Artefato inteiro (não
   chunking por tamanho) — decidido e documentado (não uma pergunta
   explícita respondida pelo usuário desta vez, mas com justificativa
   clara registrada em `docs/rag/01_estrutura.md`, seção 3.1, para revisão
   posterior, como algumas decisões da Etapa 1).
5. **4 queries fixas para recuperação** (visão geral/epics, funcionalidades,
   tarefas operacionais, problemas conhecidos), `top_k=6` por query,
   deduplicado por chave — ver seção 3.2 do documento de arquitetura,
   incluindo a ressalva registrada de que, com só 32 artefatos curtos, o
   efeito de filtragem do retrieval é menor do que num corpus grande
   (ponto para a análise/discussão do TCC, não um defeito).

### O que existe no repositório agora (além do que já existia na Etapa 1)

```
src/rag/indexer.py                      # artefato_para_texto, indexar (Cohere Embed v4 + Chroma)
src/rag/retriever.py                    # 4 queries fixas, recuperar, _deduplicar_por_chave
src/rag/cohere_backend.py               # geração via Command R (grounded generation + citações)
src/rag/claude_backend.py               # geração via Claude Messages API (documentos em XML)
src/rag/pipeline.py                     # main() (CLI), orquestra indexação+recuperação+2 gerações
tests/test_rag_indexer.py               # 3 testes
tests/test_rag_retriever.py             # 3 testes
tests/test_rag_cohere_backend.py        # 2 testes
tests/test_rag_claude_backend.py        # 3 testes
tests/test_rag_pipeline.py              # 2 testes
docs/rag/01_estrutura.md                # arquitetura da Etapa 2, com fontes
docs/rag/02_referencias.md              # referência linha a linha de cada arquivo
```

`requirements.txt` atualizado: `anthropic==1.2.0` adicionado e instalado no
venv (não estava instalado antes desta sessão); comentário adicionado
explicando que `langchain`/`langchain-core` ficam sem uso.

Suíte de testes completa: **23/23 passando** (10 da Etapa 1 + 13 novos —
só as funções puras/determinísticas de cada módulo têm teste automatizado;
as que chamam Cohere/Claude/Chroma de verdade (`indexar`, `recuperar`,
`gerar_manual` dos dois backends) não têm mock, ver justificativa em
`docs/rag/02_referencias.md`, seção final).

`.env` criado a partir de `.env.example`; usuário preencheu `COHERE_API_KEY`
real com uma chave Trial (gratuita) gerada em dashboard.cohere.com/api-keys
(arquivo gitignorado, nunca versionado).

### Decisão adicional desta sessão: só a variante Cohere por enquanto

O usuário decidiu não usar `ANTHROPIC_API_KEY` por ora — a API do Claude
teria custo adicional além do que ele já paga. `gerar_manuais()` em
`src/rag/pipeline.py` ganhou um parâmetro `variantes` (e a CLI uma flag
`--variante`, repetível) para gerar só a variante pedida, em vez de sempre
tentar as duas — sem isso, o pipeline quebraria tentando usar uma
`ANTHROPIC_API_KEY` vazia mesmo pedindo só Cohere. O código da variante
`claude` continua no repositório, testado e documentado, pronto para rodar
quando/se o usuário decidir usar a chave paga.

### Estado final da Etapa 2 nesta sessão

- Código e documentação completos e testados (parte determinística):
  23/23 testes passando.
- **Executada ponta a ponta com sucesso** (`python -m src.rag.pipeline
  --variante cohere`), gerando `data/manuals_generated/rag/manual_cohere.md`
  a partir de `data/raw/data.json` real (32 artefatos). Resultado:
  - Manual coerente, em Markdown, com 12 seções — nenhuma repete o
    esquema fixo de 4 categorias da Etapa 1 (Visão Geral/Funcionalidades/
    Tarefas/Bugs); a LLM decidiu livremente a estrutura, como previsto na
    seção 1 de `docs/rag/01_estrutura.md`.
  - Citações automáticas do Command R presentes e coerentes — cada
    afirmação do texto aponta pra uma chave real do Jira (`SCRUM-1` a
    `SCRUM-33`), sem indício de alucinação a olho nu.
  - Recuperação filtrou de fato: só ~15 dos 32 artefatos foram citados no
    manual final, não o dataset inteiro — evidência de que o retrieval por
    similaridade está discriminando, e não só "despejando tudo" (a
    ressalva metodológica da seção 3.2 de `01_estrutura.md` previa um
    efeito de filtragem menor num corpus pequeno; na prática saiu
    ~47% do corpus, um filtro real ainda que não agressivo).
  - Ainda falta revisão de conteúdo linha a linha pelo usuário (mesmo
    processo de conferência manual da Etapa 1) — a validação acima foi
    técnica (estrutura, citações, ausência de erro), não uma revisão
    completa do texto gerado.
- Variante `claude` implementada e testada, mas **não executada** (decisão
  do usuário de não gastar na API paga por enquanto).

### Para a próxima sessão

- Revisar o conteúdo de `manual_cohere.md` linha a linha (mesmo processo
  da Etapa 1) e registrar aqui qualquer correção/observação.
- Se/quando o usuário decidir usar a API paga da Anthropic: preencher
  `ANTHROPIC_API_KEY` no `.env` e rodar
  `python -m src.rag.pipeline --variante claude` (não precisa reindexar
  nem gerar a variante Cohere de novo — os artefatos recuperados são os
  mesmos, ver `docs/rag/01_estrutura.md`, seção 1.1).
- Próximo passo depois disso: Etapa 3 (Híbrido) — reaproveita
  `manual_template.md.j2` da Etapa 1 e usa `claude_backend`/`cohere_backend`
  como "motor de reescrita" por seção, em vez de gerar o documento inteiro
  livre (ver `docs/rag/01_estrutura.md`, seção 4).

## Sessão 3 — 2026-09-07 — Etapa 3 (Híbrido) implementada e executada

### Decisões tomadas nesta sessão (confirmadas com o usuário, não presumidas)

1. **Todas as 4 seções reescritas por LLM, incluindo "Problemas Conhecidos"**
   — o usuário escolheu abordagem uniforme entre as 4 categorias em vez de
   manter a tabela de bugs determinística como na Etapa 1 (opção também
   oferecida). Cada bug ainda traz chave/título/status no texto gerado,
   para não perder rastreabilidade.
2. **Só variante Cohere executada** — mesma decisão da Etapa 2 (sem
   `ANTHROPIC_API_KEY` paga); `gerar_secao_claude`/`montar_prompt_claude`
   implementados e testados (parte pura), mas não executados.
3. **Uma chamada de LLM por seção (categoria), não por artefato nem para o
   documento inteiro** — decisão já registrada ao fim da Etapa 2
   (`docs/rag/01_estrutura.md`, seção 4), confirmada e implementada nesta
   sessão em `src/hybrid/section_backend.py`.

### O que existe no repositório agora (além do que já existia nas Etapas 1–2)

```
src/hybrid/section_backend.py                 # SECTION_CONFIG, gerar_secao_cohere, gerar_secao_claude
src/hybrid/templates/manual_hibrido.md.j2      # estrutura fixa, corpo de cada seção = 1 variável
src/hybrid/generator.py                        # gerar_manuais, main() (CLI)
tests/test_hybrid_section_backend.py           # 5 testes
tests/test_hybrid_generator.py                 # 3 testes
docs/hybrid/01_estrutura.md                    # arquitetura da Etapa 3, com fontes
docs/hybrid/02_referencias.md                  # referência linha a linha, incluindo os bugs abaixo
```

Suíte de testes completa: **31/31 passando** (23 das Etapas 1–2 + 8 novos).

### Bugs encontrados e corrigidos na primeira execução ponta a ponta

1. **Truncamento por `MAX_TOKENS`**: a seção "Funcionalidades" (15
   Histórias de Usuário) foi cortada no meio de uma frase, com uma tag de
   citação bruta e incompleta vazando no texto (`<co: 1>...`). Diagnóstico
   isolado confirmou `finish_reason == "MAX_TOKENS"` e
   `output_tokens == 4096` — o teto de saída do próprio modelo
   `command-r-08-2024` (não configurável para cima via `max_tokens`,
   confirmado na documentação oficial da Cohere). A mesma documentação
   confirma que citações inline (`<co: N>`) não são o formato normal de
   resposta — a tag vazada era um artefato do corte abrupto. Corrigido
   pedindo concisão explícita no prompt (2–3 frases por artefato); a seção
   passou a completar em ~2600 tokens de saída, sem cortes.
2. **Subtítulos da LLM no mesmo nível do cabeçalho fixo**: a LLM usava
   `##` (mesmo nível de `## Funcionalidades`) para subtítulos internos,
   quebrando a hierarquia do documento. Corrigido instruindo
   explicitamente nível `###` ou mais profundo para subtítulos internos.

Ambos os bugs só apareciam na execução real (não nos testes automatizados,
que cobrem só as funções puras) — mesma limitação metodológica já
registrada para a Etapa 2. Detalhamento completo em
`docs/hybrid/02_referencias.md`.

### Estado final da Etapa 3 nesta sessão

- Código e documentação completos e testados (parte determinística):
  31/31 testes passando.
- **Executada ponta a ponta com sucesso** (`python -m src.hybrid.generator
  --variante cohere`), gerando `data/manuals_generated/hybrid/manual_cohere.md`
  a partir de `data/raw/data.json` real (32 artefatos), após as duas
  correções acima: sem truncamento, sem tags soltas, hierarquia de
  cabeçalhos correta (`###` para subtítulos internos), citações do Command
  R presentes por seção e agrupadas no rodapé do documento.
- Variante `claude` implementada e testada, mas não executada (mesma
  decisão da Etapa 2).
- Ainda falta revisão de conteúdo linha a linha pelo usuário (mesmo
  processo de conferência manual das Etapas 1 e 2).

### Para a próxima sessão

- Revisar o conteúdo de `manual_cohere.md` (Etapa 3) linha a linha.
- Com as três etapas implementadas (Templating, RAG, Híbrido), o próximo
  passo natural do TCC é a análise/discussão comparativa entre os três
  manuais gerados a partir do mesmo `data/raw/data.json` — não há mais
  etapa de implementação prevista além da variante `claude` (Etapas 2 e 3),
  pendente de decisão do usuário sobre a API paga da Anthropic.

## Sessão 4 — 2026-09-27 — Etapa 4 (Avaliação) implementada

### O que foi feito

- Figuras dos métodos (`docs/diagramas/fig1` a `fig4`) refeitas para caber
  na largura da página do TCC: fig1, fig3 e fig4 na vertical; fig2 em grade
  de 3 linhas (Indexação, Recuperação, Geração). O Mermaid atualizado está em
  `docs/diagramas.md`. No LaTeX, usar `width=\linewidth` em vez de `scale`
  (com `scale=0.2`, 2352 px viram ~16,6 cm, mais que os 16 cm de texto da ABNT).
- Módulo `src/evaluation/` com todas as métricas combinadas com o usuário.
  Arquitetura, fontes e comandos em `docs/evaluation/01_estrutura.md`:
  - `benchmark.py` + `medicao.py`: tempo (mediana de N execuções, por fase)
    e tokens; salva cada execução para a análise de variação;
  - `metricas_texto.py`: Flesch-PT, estrutura, cobertura explícita, % de
    texto citado;
  - `bertscore.py`: BERTScore por janelas (sem o truncamento em 512 tokens
    do pacote), idêntico ao `bert_score` oficial para textos curtos;
  - `variacao.py`: reprodutibilidade entre execuções;
  - `fidelidade.py`: planilhas de anotação frase a frase (S/P/N/-) e cobertura
    de conteúdo;
  - `avaliacao_humana.py`: pacote cego (manual_A..D), formulário, médias e
    alfa de Krippendorff ordinal;
  - `juiz_llm.py`: LLM como juiz (Command A, JSON Schema), com os vieses
    documentados;
  - `relatorio.py`: junta tudo em `data/evaluation/resultados.md`.
- Novas dependências: `bert-score` (traz torch e transformers), `pyphen` e
  `krippendorff`.
- Testes: 63 passando (31 anteriores + 32 novos). Dois deles precisam do
  modelo BERT no cache e são pulados sem ele.

### Pendências

- O manual humano (método 4) ainda não está no repositório. Caminho
  esperado: `data/manuals_generated/manual/manual.md`. Sem ele, não há
  BERTScore e o método 4 fica fora das planilhas.
- O tempo do método 4 vai em `data/evaluation/tempo_manual.csv` (à mão).
- Rodar o benchmark definitivo (5 repetições), anotar as planilhas de
  fidelidade, recrutar pelo menos 2 avaliadores e rodar o juiz.
- Conferir nas fontes originais as referências da Etapa 4 (escritas de memória).

### Medição definitiva (2026-09-27, 18:34–19:39)

- 10 execuções de cada método automático, salvas uma a uma em
  `data/evaluation/execucoes/<metodo>/execucao_NN.md`, com data/hora e
  SHA-256 em `data/evaluation/tempos.csv` (todas com integridade "ok").
- Mediana do tempo total: templating 0,0051 s; RAG 123,8 s (88,7–240,9);
  híbrido 197,4 s (170,0–271,2). Quase todo o tempo é a espera pela API.
- 1 falha de rede (híbrido nº 6, ReadTimeout > 300 s), registrada em
  `data/evaluation/falhas.csv` e refeita.
- Juiz LLM rodado sobre os manuais de `data/manuals_generated/`.
- Consumo: cerca de 90 chamadas à Cohere no total da sessão (limite Trial:
  1.000/mês).
- Relatório consolidado: `data/evaluation/resultados.md`.
