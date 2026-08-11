# Etapa 1 — Templating puro (Jinja2): estrutura e fundamentação teórica

> Documento de arquitetura da Etapa 1 do TCC. Escrito **antes** da implementação,
> para alinhar o que será construído e por quê. O detalhamento técnico linha a
> linha (o que cada trecho de código faz e sua referência) fica em
> `02_referencias.md`, preenchido conforme cada arquivo é implementado.

## 1. Papel desta etapa na comparação do TCC

O TCC compara três formas de gerar o mesmo manual de usuário a partir dos
mesmos artefatos do Jira:

| Etapa | Quem decide o **texto** | Quem decide a **estrutura** |
|---|---|---|
| 1. Templating puro | ninguém (dados brutos formatados) | fixa, definida no template `.j2` |
| 2. RAG (Claude + Cohere) | a LLM | a LLM |
| 3. Híbrido | a LLM (reescreve/naturaliza) | fixa, definida no template `.j2` |

A Etapa 1 é a **baseline determinística**: mesma entrada sempre produz a
mesma saída, sem geração de linguagem natural livre. Isso é o que a
literatura de Geração de Linguagem Natural (NLG) chama de abordagem
*template-based*, em oposição a abordagens *corpus-based / neural* (que é
o que a Etapa 2 usa). Ter essa baseline é o que permite medir, nas etapas
seguintes, o que a IA de fato agrega (naturalidade, coesão) e o que
eventualmente perde (precisão, previsibilidade) — essa distinção é descrita
formalmente em:

- Reiter, E., & Dale, R. (2000). *Building Natural Language Generation
  Systems*. Cambridge University Press. (referência clássica que separa
  arquiteturas de NLG em estágios de *document planning*, *microplanning*
  e *realization* — o que fazemos aqui é essencialmente document
  planning + realization via template, sem microplanning linguístico)
- Gatt, A., & Krahmer, E. (2018). "Survey of the State of the Art in
  Natural Language Generation: Core tasks, applications and evaluation."
  *Journal of Artificial Intelligence Research*, 61, 65–170. (survey
  recente e amplamente citado que contrasta métodos baseados em regras/
  template com métodos neurais — é a referência mais direta para
  justificar por que comparar as três abordagens no TCC faz sentido
  metodologicamente)

## 2. Visão geral do pipeline

```
Jira Cloud REST API v3
        │  GET /rest/api/3/search   (Basic Auth: email + API token)
        ▼
┌───────────────────────────┐
│ src/jira/extractor.py     │  1) fetch_issues(): busca as issues brutas
│                            │     (JSON) via requests
│  usa adf_parser +          │  2) parse_issues(): converte cada issue no
│  common/schema             │     formato de Artefato (dataclass definida
└──────────────┬─────────────┘     em common/schema.py), chamando
               │                    adf_parser para o campo "description"
               ▼
     lista de Artefato (chave, título, tipo, status, descrição em
     texto/Markdown, critérios de aceitação, prioridade, responsável,
     labels, subtarefas — os últimos quatro opcionais, dependendo do
     que a API devolveu)
               ▼
┌───────────────────────────────────┐
│ src/templating/generator.py       │  1) classifica os Artefatos por tipo
└──────────────┬─────────────────────┘   (Epic / Story / Task / Bug)
               │                       2) monta o contexto (dict) para o Jinja2
               ▼
┌─────────────────────────────────────────────┐
│ src/templating/templates/manual_template.md.j2 │  renderiza o Markdown final
└──────────────┬─────────────────────────────────┘
               ▼
     data/manuals_generated/templating/manual.md
```

Esse mesmo `schema.py` será reaproveitado, sem alteração de contrato, pelas
Etapas 2 (RAG) e 3 (Híbrida) — é o ponto de integração entre as três
abordagens, garantindo que elas partam exatamente dos mesmos dados.

## 3. Decisões técnicas por módulo (com fonte)

### 3.1 `src/common/schema.py` — modelo de dados padronizado

- **O quê**: `dataclasses` representando o Artefato (e sua eventual
  Subtarefa), **sem nenhuma dependência do Jira** — apenas os campos
  normalizados. Quem sabe converter JSON do Jira para `Artefato` é o
  `extractor.py` (seção 3.3), não o `schema.py`.
- **Técnica**: `dataclasses` da biblioteca padrão do Python.
- **Fonte**: PEP 557 – Data Classes (peps.python.org/pep-0557/) e
  documentação oficial (docs.python.org/3/library/dataclasses.html).
- **Por quê**: separar o *modelo de dados* da *apresentação* é o mesmo
  princípio do padrão arquitetural Model–View–Controller, descrito
  originalmente em Krasner, G. E., & Pope, S. T. (1988). "A Description
  of the Model-View-Controller User Interface Paradigm in the Smalltalk-80
  System." *Journal of Object-Oriented Programming*. Aqui, `schema.py` é o
  Model; `manual_template.md.j2` é a View; `generator.py` é o Controller
  que os conecta. Mantendo o Model livre de qualquer detalhe do Jira, ele
  pode ser populado por qualquer fonte (inclusive, futuramente, por outro
  sistema de rastreamento de issues) sem alterar `generator.py` nem os
  módulos de RAG/Híbrido.
- **Campos opcionais**: o export real usado neste projeto (`data/raw/data.json`)
  não traz `priority`, `assignee`, `labels` nem `subtasks` em nenhuma issue
  — só `summary`, `issuetype`, `description` e `status`. Esses quatro campos
  ficam como opcionais (`None`/lista vazia) no `Artefato`, tanto para não
  quebrar com este dataset quanto para o schema continuar genérico o
  suficiente para exports que os tragam.

### 3.2 `src/jira/adf_parser.py` — parser do Atlassian Document Format

- **O quê**: função recursiva que percorre a árvore do campo `description`
  e produz texto plano/Markdown simples.
- **Técnica**: percurso recursivo em árvore (recursive tree traversal),
  necessário porque o ADF é uma estrutura de nós aninhados (`doc` →
  `content[]` → nós como `paragraph`, `text`, `bulletList`, `orderedList`,
  `heading`, etc.), não uma lista plana.
- **Fonte da estrutura de dados**: Atlassian Document Format — structure
  (developer.atlassian.com/cloud/jira/platform/apis/document/structure/).
- **Fonte da técnica de percurso**: percurso em árvore é um algoritmo
  clássico de estruturas de dados, formalizado em Cormen, T. H., Leiserson,
  C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms*
  (3rd ed.). MIT Press — capítulo sobre árvores e recursão.
- **Extração de critérios de aceitação**: as Stories deste dataset não têm
  subtarefas — em vez disso, seguem o formato clássico de User Story
  ("Como usuário, quero..., para...") descrito em Cohn, M. (2004). *User
  Stories Applied: For Agile Software Development*. Addison-Wesley,
  seguido de uma lista de Critérios de Aceitação. Por isso, além da função
  genérica de conversão ADF → Markdown, `adf_parser.py` expõe uma função
  auxiliar que localiza a lista (`bulletList`) imediatamente após o
  parágrafo em negrito "Critérios de aceitação" e a devolve como lista de
  strings — usada pelo `extractor.py` para popular
  `Artefato.criterios_aceitacao`, que a Etapa 1 usa como o "passo a passo"
  da seção de Funcionalidades (na ausência de subtarefas).

### 3.3 `src/jira/extractor.py` — extração via API REST do Jira

- **O quê**: `fetch_issues()` consulta `GET /rest/api/3/search` com
  autenticação básica e devolve as issues em JSON bruto; `parse_issues()`
  converte essa lista de JSON em `list[Artefato]`, chamando
  `adf_parser.adf_to_markdown` (e a extração de critérios de aceitação)
  para o campo `description` de cada issue.
- **Fonte do endpoint**: Jira Cloud REST API v3 — `GET /rest/api/3/search/jql`
  (developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get),
  o endpoint atual de busca por JQL com paginação via `nextPageToken`
  (o antigo `/rest/api/3/search`, baseado em `startAt`, está em
  descontinuação pela Atlassian). Confirmado inspecionando o formato real
  de `data/raw/data.json`, que só tem o campo `isLast` no nível raiz.
- **Fonte da autenticação**: Basic Auth for REST APIs — uso de e-mail +
  API Token (developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/).
  Você já validou esse fluxo no Postman, então a implementação vai espelhar
  exatamente essa mesma chamada.
- **Biblioteca HTTP**: `requests` (requests.readthedocs.io) — biblioteca
  padrão de fato para chamadas HTTP em Python.
- **Segredos via `.env`**: e-mail, domínio e token nunca ficam hardcoded
  no código, seguindo a prática de configuração via variáveis de ambiente
  descrita em "The Twelve-Factor App", fator III — Config
  (12factor.net/config), metodologia amplamente adotada na indústria para
  separar configuração de código.

### 3.4 `src/templating/generator.py` — classificação e renderização

- **O quê**:
  1. classifica os Artefatos por tipo, usando o campo
     `fields.issuetype.name` (vocabulário controlado do próprio Jira —
     Epic / Story / Task / Bug — documentado em
     developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/);
  2. monta o contexto (dicionário Python) que alimenta o template;
  3. renderiza usando a API `Environment` / `render()` do Jinja2.
- **Mapeamento de tipos deste dataset**: o export usado não tem o tipo
  "Task"/"Tarefa" previsto originalmente para a seção "Tarefas
  Operacionais" — em vez disso tem o tipo "Request" (pedidos de melhoria
  de design, ex. "IMP-04 — Modo escuro"). `generator.py` mapeia
  `Request → Tarefas Operacionais`, mantendo as quatro seções do template
  inalteradas; e `História → Story` (nome em português do mesmo conceito
  de User Story). Esse mapeamento fica centralizado em um dicionário
  único em `generator.py`, para ficar fácil de estender caso apareçam
  outros nomes de tipo em exports futuros.
- **Fonte do motor de template**: Jinja2, mantido pelo Pallets Projects
  (jinja.palletsprojects.com/) — motor de templates para Python que separa
  explicitamente lógica de apresentação de lógica de aplicação, mesmo
  princípio de separação citado na seção 3.1.

### 3.5 `src/templating/templates/manual_template.md.j2` — estrutura do manual

- **O quê**: template com estrutura fixa, com quatro seções: Visão Geral
  (Epics), Funcionalidades (Stories, com passo a passo derivado das
  subtarefas), Tarefas Operacionais (Tasks) e uma tabela de Problemas
  Conhecidos (Bugs).
- **Fonte da estrutura de documentação de usuário**: essas quatro seções
  seguem o padrão internacional para documentação de usuário de software:
  ISO/IEC/IEEE 26514:2008 — *Systems and software engineering —
  Requirements for designers and developers of user documentation*, que
  recomenda separar visão geral do produto, descrição de funcionalidades
  (orientada a tarefas do usuário) e informação de suporte/known issues.
  Como referência complementar de escrita técnica orientada a tarefas:
  Hargis, G. et al. (2004). *Developing Quality Technical Information: A
  Handbook for Writers and Editors* (2nd ed.). IBM Press — amplamente
  citado em redação técnica de software, reforça a lógica de "uma seção
  por tarefa do usuário" usada para transformar Subtasks em passo a passo.
- **Formato de saída**: Markdown, seguindo a especificação CommonMark
  (spec.commonmark.org) — formato de texto plano, versionável em Git,
  portátil (renderiza no GitHub, VS Code, etc.), escolha adequada para um
  pipeline reprodutível de TCC.

## 4. Contratos previstos (sem código ainda)

Só para situar o que cada arquivo vai expor — a assinatura pode mudar
levemente na implementação, mas a responsabilidade de cada peça é esta:

- `schema.py`: dataclasses `Artefato` e `Subtarefa` — sem lógica, sem
  import do Jira, só estrutura.
- `adf_parser.py`: `adf_to_markdown(adf_doc: dict) -> str` (conversão
  genérica) e `extract_bullet_items_after_label(adf_doc: dict, label: str)
  -> list[str]` (auxiliar para critérios de aceitação) — funções puras,
  sem efeitos colaterais, fáceis de testar isoladamente (por isso os
  testes começam por elas).
- `extractor.py`: `fetch_issues(jql: str | None = None) -> list[dict]`
  (chamada HTTP) e `parse_issues(issues: list[dict]) -> list[Artefato]`
  (conversão para o schema comum, usando `adf_parser`).
- `generator.py`: `classificar_por_tipo(artefatos: list[Artefato]) -> dict`
  e `gerar_manual(artefatos: list[Artefato], template_path: str) -> str`.

## 5. Ligação com as próximas etapas

`schema.py` é o único artefato desta etapa que será **importado** (não
duplicado) pelos módulos `src/rag/` e `src/hybrid/` mais adiante — por
isso ele precisa ficar livre de qualquer detalhe específico de Jinja2 ou
de prompt de LLM. O que muda entre as três etapas é só o que acontece
depois do schema: `generator.py` (template) vs. um `chain.py`/`prompt.py`
equivalente na Etapa 2 vs. a combinação dos dois na Etapa 3.

## 6. Referências completas

1. Reiter, E., & Dale, R. (2000). *Building Natural Language Generation
   Systems*. Cambridge University Press.
2. Gatt, A., & Krahmer, E. (2018). Survey of the State of the Art in
   Natural Language Generation. *Journal of Artificial Intelligence
   Research*, 61, 65–170.
3. Krasner, G. E., & Pope, S. T. (1988). A Description of the
   Model-View-Controller User Interface Paradigm in the Smalltalk-80
   System. *Journal of Object-Oriented Programming*.
4. Python Software Foundation. PEP 557 – Data Classes.
   https://peps.python.org/pep-0557/
5. Python Software Foundation. `dataclasses` — Data Classes (docs).
   https://docs.python.org/3/library/dataclasses.html
6. Atlassian. Atlassian Document Format — structure.
   https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
7. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
   *Introduction to Algorithms* (3rd ed.). MIT Press.
8. Atlassian. Jira Cloud REST API v3 — Issue search (`GET /rest/api/3/search/jql`).
   https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get
9. Atlassian. Basic auth for REST APIs.
   https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
10. Atlassian. Jira Cloud REST API v3 — Issue types.
    https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/
11. Pallets Projects. Jinja2 Documentation. https://jinja.palletsprojects.com/
12. Requests project. Requests: HTTP for Humans. https://requests.readthedocs.io/
13. Wiggins, A. (2011). The Twelve-Factor App — III. Config.
    https://12factor.net/config
14. ISO/IEC/IEEE 26514:2008. Systems and software engineering —
    Requirements for designers and developers of user documentation.
15. Hargis, G., Carey, M., Hernandez, A. K., Hughes, P., Longo, D.,
    Rouiller, S., & Wilde, E. (2004). *Developing Quality Technical
    Information: A Handbook for Writers and Editors* (2nd ed.). IBM Press.
16. CommonMark. CommonMark Spec. https://spec.commonmark.org/
17. Cohn, M. (2004). *User Stories Applied: For Agile Software
    Development*. Addison-Wesley.
18. Python Software Foundation. PEP 604 – Allow writing union types as
    `X | Y`. https://peps.python.org/pep-0604/
19. Atlassian. Atlassian Document Format — marks.
    https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/
20. Myers, G. J., Sandler, C., & Badgett, T. (2011). *The Art of Software
    Testing* (3rd ed.). Wiley.
21. pytest documentation. `pythonpath` configuration option.
    https://docs.pytest.org/en/stable/reference/reference.html#confval-pythonpath
22. Python Software Foundation. `str.casefold()` — string methods.
    https://docs.python.org/3/library/stdtypes.html#str.casefold
23. GitHub. *GitHub Flavored Markdown Spec* — Tables extension.
    https://github.github.com/gfm/#tables-extension-
24. Python Software Foundation. `argparse` — Parser for command-line
    options. https://docs.python.org/3/library/argparse.html
