# Referências ponto a ponto — Etapa 2 (RAG)

> Preenchido incrementalmente, arquivo por arquivo, no mesmo formato de
> `docs/templating/02_referencias.md`. O panorama geral (arquitetura,
> decisões antes de codar) está em `01_estrutura.md`.

## Status geral

| Arquivo | Status |
|---|---|
| `src/rag/indexer.py` | ✅ implementado |
| `src/rag/retriever.py` | ✅ implementado |
| `src/rag/cohere_backend.py` | ✅ implementado |
| `src/rag/claude_backend.py` | ✅ implementado |
| `src/rag/pipeline.py` | ✅ implementado |
| `tests/test_rag_indexer.py` | ✅ implementado (3/3 passando) |
| `tests/test_rag_retriever.py` | ✅ implementado (3/3 passando) |
| `tests/test_rag_claude_backend.py` | ✅ implementado (3/3 passando) |
| `tests/test_rag_cohere_backend.py` | ✅ implementado (2/2 passando) |
| `tests/test_rag_pipeline.py` | ✅ implementado (2/2 passando) |
| Execução ponta a ponta contra `data/raw/data.json` | ⬜ pendente (precisa de `COHERE_API_KEY`/`ANTHROPIC_API_KEY` reais no `.env`) |

---

## `src/rag/indexer.py`

- **Linhas 23–25 (`EMBED_MODEL`, `COLLECTION_NAME`, `CHROMA_PERSIST_DIR`)**:
  constantes de configuração no topo do módulo, mesmo padrão de
  `TIPO_PARA_CATEGORIA` em `src/templating/generator.py` (Etapa 1) — fácil
  de achar/alterar sem procurar dentro de funções.
- **Linhas 28–32 (`_get_cohere_client`)**: lê `COHERE_API_KEY` do ambiente
  com erro explícito se faltar — mesmo padrão de `_get_env` em
  `src/jira/extractor.py` (Etapa 1), aplicando a mesma prática de config
  via variável de ambiente (The Twelve-Factor App, fator III — já citado
  em `docs/templating/01_estrutura.md`, item 13 da bibliografia).
- **Linhas 35–49 (`artefato_para_texto`)**: função pura que achata um
  `Artefato` (schema reaproveitado de `src/common/schema.py`, sem
  alteração — o ponto de integração entre as três etapas, conforme
  `docs/templating/01_estrutura.md`, seção 5) num texto único. Usa
  `criterios_aceitacao` quando existe, senão `subtarefas` — mesmo
  `if`/`elif` (não dois `if`) que `manual_template.md.j2` usa na Etapa 1,
  para não repetir cabeçalho caso os dois campos venham preenchidos.
  Coberta por `tests/test_rag_indexer.py` (3 casos: com critérios, com
  subtarefas, sem nenhum dos dois).
- **Linhas 52–81 (`indexar`)**: 
  - linha 56: `chromadb.PersistentClient(path=...)` grava em disco (não em
    memória), para o índice sobreviver entre execuções do pipeline — API
    documentada em https://docs.trychroma.com/docs/run-chroma/persistent-client
  - linhas 60–65: `cliente_cohere.embed(model="embed-v4.0", input_type=
    "search_document", texts=textos, embedding_types=["float"])` — um
    único request para todos os artefatos de uma vez (a Cohere aceita uma
    lista de textos por chamada), em vez de um request por artefato.
    `input_type="search_document"` é o valor correto para textos que serão
    *buscados* (em oposição a `"search_query"`, usado em
    `retriever.py`) — Cohere. *Embeddings — input_type*.
    https://docs.cohere.com/docs/embeddings
  - linha 69: `resposta.embeddings.float_` — o SDK da Cohere (v7) devolve
    embeddings agrupados por tipo (`float_`, `int8`, `binary`, etc.) dentro
    de `EmbedByTypeResponseEmbeddings`; o sufixo `_` existe porque `float`
    é palavra reservada em Python. Confirmado inspecionando
    `cohere.types.embed_by_type_response_embeddings.
    EmbedByTypeResponseEmbeddings` na versão instalada (`cohere==7.0.5`).
  - linhas 67–80: `collection.upsert(...)` grava IDs (a própria chave do
    Jira, ex. `SCRUM-21`), os vetores, o texto achatado (`documents=`, na
    nomenclatura do Chroma — não confundir com `Document` da Cohere) e
    metadados simples para exibição. `upsert` em vez de `add` porque
    reexecutar o pipeline sobre o mesmo dataset deve atualizar os
    registros existentes, não duplicá-los nem falhar por ID repetido —
    comportamento documentado em
    https://docs.trychroma.com/docs/collections/manage-collections#adding-data-to-a-collection.

---

## `src/rag/retriever.py`

- **Linhas 24–32 (`EMBED_MODEL`, `TOP_K_POR_QUERY`, `QUERIES_PADRAO`)**:
  as quatro queries fixas — decisão registrada em
  `docs/rag/01_estrutura.md`, seção 3.2, junto com a ressalva
  metodológica sobre o efeito de filtragem ser limitado num corpus de 32
  artefatos.
- **Linhas 42–54 (`_deduplicar_por_chave`)**: função pura (recebe/devolve
  só estruturas de dados, sem chamar API) — separada de `recuperar` de
  propósito, para poder ser testada sem precisar de um Chroma real nem de
  chave de API (`tests/test_rag_retriever.py`, 3 casos). Preserva a
  primeira ocorrência de cada chave, técnica padrão de deduplicação
  preservando ordem com um `set` auxiliar de chaves já vistas.
- **Linhas 57–79 (`recuperar`)**:
  - linhas 67–72: embute as queries com `input_type="search_query"` —
    mesma fonte da seção sobre `indexer.py` acima; o contraste
    `search_document` vs. `search_query` é a própria razão de existir do
    parâmetro `input_type` na API da Cohere.
  - linhas 74–77: `collection.query(query_embeddings=[vetor_query],
    n_results=top_k)` roda uma busca por similaridade de cosseno por vez
    (uma chamada por vetor de query, dentro do loop) — a API do Chroma
    aceita múltiplos `query_embeddings` na mesma chamada, mas aqui optei
    por uma chamada por query para poder atribuir facilmente cada
    resultado à sua query de origem antes de deduplicar. `resultado["ids"]
    [0]`: o Chroma sempre devolve uma lista de resultados por query
    embutida (mesmo com uma só), daí o índice `[0]`. Fonte:
    https://docs.trychroma.com/docs/querying-collections/query-and-get

---

## `src/rag/cohere_backend.py`

- **Linha 26 (`CHAT_MODEL = "command-r-08-2024"`)**: versão "Live" atual
  da família Command R no Chat endpoint v2 — confirmado em Cohere.
  *Models overview*. https://docs.cohere.com/docs/models (as versões
  anteriores `command-r-03-2024`/`command-r-plus-04-2024` estão
  descontinuadas desde 15/set/2025).
- **Linha 27 (`TEMPERATURE = 0.3`)**: valor baixo, não zero — reduz
  variância entre execuções sem tornar a saída completamente
  determinística/repetitiva; parâmetro documentado em Cohere. *Chat API
  reference*. https://docs.cohere.com/reference/chat. Ver justificativa
  completa em `docs/rag/01_estrutura.md`, seção 3.3.
- **Linhas 29–41 (`SYSTEM_PROMPT`, `INSTRUCAO`)**: papel + instrução de
  geração livre — a Etapa 2 explicitamente não define estrutura de seções
  (ao contrário do `manual_template.md.j2` da Etapa 1); a frase "você
  decide a estrutura" (linha 39) é o que operacionaliza, no prompt, a
  linha da tabela da seção 1 de `01_estrutura.md` ("quem decide a
  estrutura: a LLM").
- **Linhas 44–56 (`_formatar_documentos`)**: converte cada `Artefato`
  recuperado num `cohere.types.Document(id=..., data={...})` — o
  formato de `data` como dicionário (em vez de string simples) é uma das
  três formas aceitas pelo parâmetro `documents` do Chat v2, e foi
  escolhida porque preserva os metadados (`titulo`, `tipo`, `status`)
  separados do texto corrido, o que ajuda o modelo e as citações geradas a
  se referirem a um documento de forma mais estruturada. Fonte: Cohere.
  *Retrieval Augmented Generation (RAG) — documents*.
  https://docs.cohere.com/docs/retrieval-augmented-generation-rag. Testada
  isoladamente em `tests/test_rag_cohere_backend.py` (sem chamar a API).
  Reaproveita `artefato_para_texto` de `indexer.py` (linha 22, import) em
  vez de duplicar a lógica de achatamento — mesmo texto que foi indexado é
  o texto passado para geração, evitando divergência entre o que foi
  buscado e o que foi mostrado ao modelo.
- **Linhas 59–79 (`gerar_manual`)**:
  - linhas 67–75: `cliente.chat(model=..., messages=[...], documents=...,
    temperature=...)` — API v2 (`cohere.ClientV2`), mensagens tipadas
    (`SystemChatMessageV2`, `UserChatMessageV2`) em vez de dicts soltos,
    conforme o SDK instalado (`cohere==7.0.5`) exige/aceita.
  - linha 77: a resposta vem como uma lista de blocos de conteúdo
    (`message.content`), cada um com `.text` — junta todos os blocos numa
    string; na prática, para um chat sem *tool use*, normalmente há um
    único bloco de texto, mas o formato da API já prevê múltiplos blocos
    (mesma lógica de `resposta.content` da API do Claude, ver
    `claude_backend.py` abaixo).
  - linha 78: `message.citations` — lista de `Citation` (posição no
    texto + documentos-fonte) devolvida pronta pela Cohere quando
    `documents` é passado; usada por `pipeline.py` para anexar as fontes
    ao final do manual gerado. Fonte: mesma da seção 3.3 acima.

---

## `src/rag/claude_backend.py`

- **Linha 27 (`CHAT_MODEL = "claude-sonnet-5"`)**: "melhor combinação de
  velocidade e inteligência" da linha atual — Anthropic. *Models
  overview*. https://platform.claude.com/docs/en/models/overview.
  Escolhido em vez de Opus 5 (mais caro, para tarefas agênticas
  complexas) ou Haiku 4.5 (mais barato, mas corte de conhecimento mais
  antigo) porque gerar um manual a partir de ~20–30 artefatos curtos não
  exige o topo de linha, mas se beneficia de mais qualidade de escrita do
  que o modelo mais rápido/barato ofereceria.
- **Linhas 46–53 (`_montar_documento_xml`)**: um documento por vez, no
  formato `<document index="n"><source>...</source><document_content>...
  </document_content></document>` — estrutura exata recomendada pela
  Anthropic para múltiplos documentos em um prompt. Fonte: Anthropic.
  *Claude prompting best practices — Long context prompting*.
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  (seção "Structure document content and metadata with XML tags").
- **Linhas 56–64 (`montar_prompt`)**: função pura (não chama a API) — os
  documentos vêm **antes** da instrução (linha 64: `f"{documentos}...
  {INSTRUCAO}"`, instrução por último), seguindo a mesma fonte acima:
  "Put longform data at the top… queries at the end can improve response
  quality by up to 30 percent in tests, especially with complex,
  multidocument inputs." Separada de `gerar_manual` de propósito para ser
  testável sem API (`tests/test_rag_claude_backend.py`, 3 casos,
  incluindo a ordem relativa de `</documents>` e da instrução).
- **Linhas 67–81 (`gerar_manual`)**:
  - linhas 73–79: `cliente.messages.create(model=..., max_tokens=8192,
    temperature=0.3, system=SYSTEM_PROMPT, messages=[{"role": "user",
    "content": montar_prompt(...)}])` — API Messages padrão da Anthropic;
    `system` como parâmetro separado (não uma mensagem `role="system"`
    dentro de `messages`, diferença real de formato entre a API da
    Anthropic e a da Cohere v2) — Anthropic. *Messages API reference*.
    https://platform.claude.com/docs/en/api/messages.
  - linha 81: a resposta vem em `resposta.content`, lista de blocos com
    `.type` (`"text"`, ou `"tool_use"` se houvesse *tool calling*, que não
    é o caso aqui) — filtra só os blocos de texto e concatena, mesmo
    princípio de "resposta em blocos" da Cohere (ver `cohere_backend.py`
    acima), documentado em Anthropic. *Messages API — content blocks*.
    https://platform.claude.com/docs/en/api/messages.

---

## `src/rag/pipeline.py`

- **Linhas 22–29 (`_formatar_citacoes`)**: função pura que transforma a
  lista de `Citation` da Cohere (só disponível na variante `cohere`, já
  que a API do Claude não tem citação nativa — ver seção 3.4 de
  `01_estrutura.md`) num bloco Markdown legível, anexado ao final do
  `manual_cohere.md`. `fonte.id` vem de `DocumentSource.id`, que é a
  própria chave do Jira (`Document(id=artefato.chave, ...)` em
  `cohere_backend.py`), então a citação aponta direto para o artefato de
  origem sem precisar de uma tabela de lookup à parte. Testada em
  `tests/test_rag_pipeline.py` (com e sem citações).
- **Linhas 32–51 (`VARIANTES_DISPONIVEIS`, `gerar_manuais`)**: orquestra
  indexação → recuperação → geração, reaproveitando o mesmo `recuperados`
  para as variantes pedidas — é o que garante, na prática, a "recuperação
  idêntica nas duas variantes" descrita em `01_estrutura.md`, seção 1.1
  (variar só a LLM de geração, não a recuperação). O parâmetro `variantes`
  (linhas 35–36, default = as duas) foi adicionado depois da primeira
  versão desta função, quando o usuário decidiu rodar só a variante
  `cohere` por enquanto — a `claude` depende de uma chave paga da
  Anthropic além do que ele já assina, enquanto a `cohere` roda no plano
  trial gratuito (limites confirmados na sessão anterior). Sem esse
  parâmetro, `gerar_manuais` chamaria os dois backends incondicionalmente
  e quebraria com `ANTHROPIC_API_KEY` ausente mesmo pedindo só Cohere.
- **Linhas 54–81 (`main`)**: mesmo formato de CLI (`argparse`) de
  `src/templating/generator.py` (Etapa 1) — lê `data/raw/data.json`,
  chama `parse_issues` (reaproveitado sem alteração do `extractor.py` da
  Etapa 1) e grava os manuais gerados em arquivos separados
  (`manual_cohere.md` e/ou `manual_claude.md`) dentro de
  `data/manuals_generated/rag/` (diretório já coberto pelo `.gitignore`
  existente do projeto, mesma política da Etapa 1 — saída gerada não é
  versionada, só o `data/raw/data.json` de entrada). Linhas 60–66: flag
  `--variante` repetível (`action="append"`, padrão de `argparse` para
  aceitar a mesma opção várias vezes — docs.python.org/3/library/argparse.html#action),
  ex. `python -m src.rag.pipeline --variante cohere`; sem a flag, gera
  todas as variantes de `VARIANTES_DISPONIVEIS`.

---

## `tests/test_rag_*.py`

- Mesmo estilo de `tests/test_adf_parser.py` (Etapa 1): `pytest` puro,
  `assert` simples, um arquivo de teste por módulo.
- Cobrem só as funções **puras** de cada módulo (sem chamar Cohere/Claude/
  Chroma de verdade) — `artefato_para_texto`, `_deduplicar_por_chave`,
  `montar_prompt`, `_formatar_documentos`, `_formatar_citacoes` — mesma
  filosofia de separar lógica testável (determinística) de efeitos
  colaterais (chamada de rede) descrita em Myers, G. J., Sandler, C., &
  Badgett, T. (2011). *The Art of Software Testing* (3rd ed.). Wiley. (já
  citado em `docs/templating/01_estrutura.md`, item 20). As funções que
  chamam API real (`indexar`, `recuperar`, `gerar_manual` dos dois
  backends) não têm teste automatizado nesta sessão — cobertas pela
  execução ponta a ponta (ver Status geral, linha pendente) em vez de
  mock, para a Etapa 2 ser validada contra o comportamento real das APIs,
  não contra um dublê.
- `tests/test_rag_pipeline.py` constrói `Citation`/`DocumentSource` do
  SDK da Cohere diretamente (`cohere.types`) em vez de dicts, porque são
  modelos Pydantic — confirmado inspecionando `cohere.types.Citation.
  model_fields` e `cohere.types.DocumentSource.model_fields` na versão
  instalada (`cohere==7.0.5`).
- Suíte completa do projeto após a Etapa 2: 23/23 testes passando
  (10 da Etapa 1 + 13 novos).
