# Etapa 2 — RAG (Retrieval-Augmented Generation): estrutura e fundamentação teórica

> Documento de arquitetura da Etapa 2 do TCC. Escrito **antes** da implementação,
> como na Etapa 1. O detalhamento técnico linha a linha fica em
> `02_referencias.md`, preenchido conforme cada arquivo é implementado.

## 1. Papel desta etapa na comparação do TCC

Retomando a tabela de `docs/templating/01_estrutura.md`:

| Etapa | Quem decide o **texto** | Quem decide a **estrutura** |
|---|---|---|
| 1. Templating puro | ninguém (dados brutos formatados) | fixa, definida no template `.j2` |
| 2. RAG (Claude + Cohere) | a LLM | a LLM |
| 3. Híbrido | a LLM (reescreve/naturaliza) | fixa, definida no template `.j2` |

Na Etapa 2, tanto o texto quanto a estrutura do manual são decididos pela
LLM geradora — o papel do pipeline é só selecionar (recuperar) os artefatos
relevantes e entregá-los como contexto, sem impor um template. É a
abordagem *corpus-based/neural* de NLG, em oposição à *template-based* da
Etapa 1 (Gatt & Krahmer, 2018 — já citado em `docs/templating/01_estrutura.md`).

### 1.1 Duas variantes, mesma recuperação

Combinando o que já existe no projeto (`.env.example` já reservava
`COHERE_API_KEY` e `ANTHROPIC_API_KEY`) com a decisão tomada nesta sessão,
a Etapa 2 gera **dois manuais**, não um, isolando a variável "qual LLM
escreve o texto":

| Variante | Indexação + recuperação | Geração |
|---|---|---|
| `cohere` | Cohere Embed v4 + Chroma | Cohere Command R (grounded generation nativa, com citações) |
| `claude` | Cohere Embed v4 + Chroma (idêntica) | Claude (Messages API, Anthropic) |

Motivo de manter a recuperação idêntica nas duas variantes: se ela também
mudasse, uma eventual diferença entre os dois manuais não poderia ser
atribuída com confiança à LLM de geração — poderia ser efeito da
recuperação. Mantendo a recuperação fixa, a única variável entre as duas
saídas é o modelo generativo, o que é o comportamento correto de um
experimento controlado (variar um fator por vez).

### 1.2 Por que "Cohere" e "Claude" (e não, por exemplo, "Claude" para tudo)

A Anthropic **não oferece endpoint de embeddings** na API do Claude — a
documentação oficial recomenda explicitamente um provedor terceiro
(Voyage AI) para isso. Fonte: Anthropic. *Embeddings*.
https://platform.claude.com/docs/en/build-with-claude/embeddings — confirmado
nesta sessão. Ou seja: usar Claude em algum ponto do pipeline de RAG
implica que a etapa de embedding/recuperação **tem que** vir de outro
provedor — não é uma escolha de estilo, é uma restrição da própria API.

A Cohere, por sua vez, oferece o pacote completo desenhado para RAG:

- **Embed v4** — embeddings multilíngues (100+ idiomas, incluindo
  português), até 1536 dimensões. Fonte: Cohere. *Embeddings*.
  https://docs.cohere.com/docs/embeddings
- **Command R** — modelo de chat com suporte nativo a RAG: aceita um
  parâmetro `documents` e devolve citações automáticas (span de texto →
  documento-fonte), sem precisar implementar isso manualmente. Fonte:
  Cohere. *Retrieval Augmented Generation (RAG)*.
  https://docs.cohere.com/docs/retrieval-augmented-generation-rag

Isso justifica tecnicamente por que "Claude + Cohere" é uma combinação
natural para RAG: a Cohere cobre a parte que o Claude estruturalmente não
faz (embeddings), e a variante `cohere` usa o próprio Command R também
para gerar — permitindo comparar geração 100% Cohere vs. recuperação
Cohere + geração Claude.

## 2. Visão geral do pipeline

```
                    data/raw/data.json
                            │
                 src/jira/extractor.py (reaproveitado da Etapa 1, sem alteração)
                            │
                     lista de Artefato
                            │
              ┌─────────────┴─────────────┐
              ▼                           │
┌───────────────────────────┐             │
│ src/rag/indexer.py        │             │  artefatos_por_chave
│  achata cada Artefato em   │             │  (dict chave -> Artefato,
│  texto (artefato_para_     │             │   guardado à parte para a
│  texto) e embute via       │             │   geração usar os campos
│  Cohere Embed v4           │             │   estruturados originais,
│  (input_type=search_       │             │   não o texto achatado)
│  document); grava no       │             │
│  Chroma (persistido em     │             │
│  .chroma/rag/)             │             │
└──────────────┬──────────────┘             │
               ▼                           │
┌────────────────────────────────┐         │
│ src/rag/retriever.py           │◄────────┘
│  4 queries fixas (perguntas    │
│  típicas de leitor de manual)  │
│  embutidas com input_type=     │
│  search_query; busca por       │
│  similaridade no Chroma        │
│  (top-k por query);            │
│  deduplica por chave           │
└──────────────┬───────────────────┘
               ▼
     lista de Artefato recuperados (subconjunto do total)
               │
     ┌─────────┴──────────┐
     ▼                    ▼
┌─────────────────┐  ┌──────────────────┐
│ cohere_backend.py│  │ claude_backend.py│
│ Command R,       │  │ Messages API,    │
│ documents=[...]  │  │ documentos em    │
│ (grounded        │  │ XML no prompt    │
│  generation)     │  │ (Anthropic docs) │
└────────┬─────────┘  └────────┬─────────┘
         ▼                     ▼
 manual_cohere.md       manual_claude.md
     (data/manuals_generated/rag/)
```

`src/rag/pipeline.py` orquestra as duas colunas finais a partir do mesmo
`artefatos` e da mesma recuperação — ver `src/templating/generator.py` na
Etapa 1 para o precedente de um `main()` de CLI equivalente.

## 3. Decisões técnicas por módulo (com fonte)

### 3.1 `src/rag/indexer.py` — unidade de indexação e embeddings

- **Granularidade**: um chunk = um Artefato inteiro (chave + título + tipo +
  status + descrição + critérios de aceitação/subtarefas concatenados).
  Diferente de RAG sobre texto longo (onde chunking por tamanho de janela é
  necessário — Lewis et al., 2020), aqui os "documentos" de origem já são
  registros estruturados curtos e semanticamente coesos (um artefato do
  Jira raramente passa de poucos parágrafos), então fatiar um artefato ao
  meio destruiria contexto sem necessidade real de caber em limite de
  tokens. Fonte da técnica de RAG em si: Lewis, P., Perez, E., Piktus, A.,
  et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive
  NLP Tasks." *Advances in Neural Information Processing Systems (NeurIPS)*,
  33, 9459–9474.
- **Modelo de embedding**: Cohere `embed-v4.0`, com `input_type=
  "search_document"` para os textos indexados (distinto de `"search_query"`
  usado em `retriever.py` — a Cohere otimiza o vetor de forma diferente
  conforme o papel do texto, documento vs. consulta). Fonte: Cohere.
  *Embeddings*. https://docs.cohere.com/docs/embeddings
- **Banco vetorial**: Chroma, `PersistentClient` gravando em `.chroma/rag/`
  (diretório já presente no `.gitignore` do projeto — dado derivado,
  regenerável a partir de `data/raw/data.json`, não versionado, ao
  contrário de `data/raw/data.json` em si). Fonte: Chroma. *Chroma
  Documentation*. https://docs.trychroma.com/
- **`artefatos_por_chave` fica fora do Chroma**: o Chroma guarda o texto
  achatado (para casar com o vetor de embedding) e metadados simples
  (chave/título/tipo/status), mas quem gera o manual final usa o `Artefato`
  original (com `criterios_aceitacao`/`subtarefas` como listas estruturadas,
  não texto solto) — por isso `retriever.py` recebe também um
  `dict[str, Artefato]` para resolver os IDs devolvidos pela busca de volta
  para os objetos originais. Evita reconstruir/parsear a estrutura a partir
  do texto achatado.

### 3.2 `src/rag/retriever.py` — recuperação por similaridade

- **Queries fixas, não uma pergunta livre de usuário**: como a Etapa 2 gera
  um documento inteiro (não responde a uma pergunta ad hoc), a recuperação
  usa um conjunto pequeno de queries que representam os tipos de pergunta
  que um leitor de manual normalmente tem — visão geral do produto,
  funcionalidades disponíveis, tarefas operacionais, problemas conhecidos.
  Isso mantém a recuperação real (nem toda query traz os mesmos top-k) sem
  impor a estrutura de seções da Etapa 1 — a LLM de geração ainda decide
  livremente como organizar e nomear as seções do manual final; as queries
  só guiam **o que** entra no contexto, não **como** ele é apresentado.
- **Limite metodológico, registrado explicitamente**: o dataset tem só 32
  artefatos curtos. Com `top_k=6` por query e 4 queries, é esperado que boa
  parte do corpus acabe recuperada de qualquer forma (sobreposição entre
  queries). Isso é diferente do cenário em que RAG mostra seu valor mais
  claro — corpus grande, onde a maior parte do conteúdo é irrelevante para
  uma consulta específica e o retrieval filtra agressivamente. Aqui a
  arquitetura de RAG é implementada de forma real (embedding + busca por
  similaridade + top-k, não um "dump" do dataset inteiro), mas o efeito
  prático de filtragem é menor — ponto relevante para a análise/discussão
  do TCC, não um defeito de implementação.
- **`input_type="search_query"`**: mesmo modelo `embed-v4.0`, mas com o
  tipo de input trocado para otimizar o vetor da consulta (em vez do vetor
  de documento) — mesma fonte da seção 3.1.
- **Deduplicação por chave**: um artefato pode ser o mais similar a mais de
  uma query (ex.: uma Story bem escrita pode aparecer tanto na busca de
  "funcionalidades" quanto na de "visão geral"); a lista final preserva
  só a primeira ocorrência de cada chave, na ordem em que foi recuperada.

### 3.3 `src/rag/cohere_backend.py` — geração via Cohere Command R

- **Modelo**: `command-r-08-2024` — versão "Live" atual da família Command R
  no Chat endpoint v2 (128k de contexto), suficiente para os poucos
  artefatos recuperados deste dataset; `command-r-plus-08-2024` fica
  disponível como alternativa mais cara/potente, não necessária aqui.
  Fonte: Cohere. *Models overview*. https://docs.cohere.com/docs/models
- **`documents=[...]`**: cada Artefato recuperado vira um `cohere.types.
  Document(id=chave, data={...})`; o Command R usa esses documentos para
  fundamentar (*ground*) a geração e devolve `message.citations` — lista de
  citações com posição no texto (`start`/`end`) e a(s) fonte(s)
  (`sources`) — prontas, sem implementação manual de citação. Fonte:
  Cohere. *Retrieval Augmented Generation (RAG)*.
  https://docs.cohere.com/docs/retrieval-augmented-generation-rag
- **`temperature=0.3`**: valor baixo (não zero) para reduzir a variância
  entre execuções — relevante porque o TCC compara saídas entre etapas, e
  execuções muito diferentes a cada rodada dificultariam essa comparação.
  Fonte do parâmetro: Cohere. *Chat API reference — temperature*.
  https://docs.cohere.com/reference/chat

### 3.4 `src/rag/claude_backend.py` — geração via Claude

- **Modelo**: `claude-sonnet-5` — "melhor combinação de velocidade e
  inteligência" da linha atual (vs. Opus 5, mais caro, voltado a tarefas
  agenticas complexas; e Haiku 4.5, mais barato/rápido mas com corte de
  conhecimento mais antigo) — adequado ao custo/qualidade de gerar um
  manual a partir de ~20-30 artefatos curtos. Fonte: Anthropic. *Models
  overview*. https://platform.claude.com/docs/en/models/overview
- **Sem parâmetro nativo de `documents`/citação**: ao contrário do Command
  R, a API Messages do Claude não tem um parâmetro dedicado para RAG — os
  documentos recuperados são formatados manualmente dentro do prompt.
  Diferença real de produto entre os dois provedores, registrada aqui
  porque explica por que o código dos dois backends não é simétrico.
- **Formato do prompt — documentos no topo, instrução no final, em XML**:
  segue a recomendação oficial da Anthropic para prompts com múltiplos
  documentos: colocar o conteúdo longo antes da instrução (relatado como
  melhoria de até 30% na qualidade da resposta em testes deles) e envolver
  cada documento em tags `<document index="n"><source>...</source>
  <document_content>...</document_content></document>` dentro de um
  `<documents>` — Fonte: Anthropic. *Claude prompting best practices —
  Long context prompting*.
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- **Papel do sistema (`system`)**: uma frase definindo o papel ("redator
  técnico") no `system prompt`, seguindo a mesma recomendação da página
  acima ("Give Claude a role").
- **`temperature=0.3`**: mesmo raciocínio da seção 3.3, aplicado à API do
  Claude. Fonte do parâmetro: Anthropic. *Messages API reference —
  temperature*. https://platform.claude.com/docs/en/api/messages

### 3.5 `src/rag/pipeline.py` — orquestração

- **O quê**: `main()` lê `data/raw/data.json`, chama `parse_issues`
  (reaproveitado sem alteração do `src/jira/extractor.py` da Etapa 1 — é
  o ponto de integração entre etapas descrito em
  `docs/templating/01_estrutura.md`, seção 5), indexa, recupera, gera as
  duas variantes e grava `data/manuals_generated/rag/manual_cohere.md` e
  `manual_claude.md`. Mesma forma de CLI (`argparse`) usada em
  `src/templating/generator.py`.

## 4. Ligação com a Etapa 3 (Híbrida)

A Etapa 3 reaproveita a estrutura fixa da Etapa 1 (`manual_template.md.j2`)
mas usa uma LLM para reescrever/naturalizar o texto de cada seção — o que
significa que ela também pode reaproveitar `src/rag/claude_backend.py` (ou
`cohere_backend.py`) como "motor de geração de texto por seção", chamado
uma vez por seção do template em vez de uma vez para o documento inteiro.
Não há geração de embeddings/recuperação na Etapa 3 (a estrutura já vem do
template, não precisa ser "descoberta" via retrieval).

## 5. Referências completas

1. Lewis, P., Perez, E., Piktus, A., et al. (2020). Retrieval-Augmented
   Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural
   Information Processing Systems (NeurIPS)*, 33, 9459–9474.
2. Gatt, A., & Krahmer, E. (2018). Survey of the State of the Art in
   Natural Language Generation. *Journal of Artificial Intelligence
   Research*, 61, 65–170. (já citado em `docs/templating/01_estrutura.md`)
3. Anthropic. *Embeddings*.
   https://platform.claude.com/docs/en/build-with-claude/embeddings
4. Cohere. *Embeddings*. https://docs.cohere.com/docs/embeddings
5. Cohere. *Retrieval Augmented Generation (RAG)*.
   https://docs.cohere.com/docs/retrieval-augmented-generation-rag
6. Cohere. *Models overview*. https://docs.cohere.com/docs/models
7. Cohere. *Chat API reference*. https://docs.cohere.com/reference/chat
8. Chroma. *Chroma Documentation*. https://docs.trychroma.com/
9. Anthropic. *Models overview*.
   https://platform.claude.com/docs/en/models/overview
10. Anthropic. *Claude prompting best practices*.
    https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
11. Anthropic. *Messages API reference*.
    https://platform.claude.com/docs/en/api/messages
12. Cohere Inc. `cohere` Python SDK (v7). https://github.com/cohere-ai/cohere-python
13. Anthropic. `anthropic` Python SDK. https://github.com/anthropics/anthropic-sdk-python
