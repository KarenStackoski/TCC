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
