# Referências ponto a ponto — Etapa 1 (Templating)

> Este documento é preenchido **incrementalmente**, arquivo por arquivo,
> conforme cada um for implementado. Cada entrada aponta o trecho exato
> (linhas), o que ele faz tecnicamente, o porquê teórico, e a fonte/
> referência correspondente — para você conferir uma a uma. O panorama
> geral (arquitetura, decisões antes de codar) está em `01_estrutura.md`.

## Status geral

| Arquivo | Status |
|---|---|
| `src/common/schema.py` | ✅ implementado |
| `src/jira/adf_parser.py` | ✅ implementado |
| `tests/test_adf_parser.py` | ✅ implementado (7/7 passando) |
| `src/jira/extractor.py` | ✅ implementado (validado com data/raw/data.json real) |
| `src/templating/generator.py` | ✅ implementado |
| `src/templating/templates/manual_template.md.j2` | ✅ implementado |

---

## `src/common/schema.py`

- **Linhas 9, 11**: `from __future__ import annotations` + `str | None`
  (linha 28) — sintaxe de union types do PEP 604, disponível nativamente a
  partir do Python 3.10; o `__future__` import a torna válida também se o
  arquivo rodar avaliado em modo string em versões um pouco mais antigas.
  Fonte: PEP 604 – Allow writing union types as `X | Y`
  (peps.python.org/pep-0604/).
- **Linhas 14–18 e 21–32**: duas `@dataclass` (`Subtarefa`, `Artefato`) —
  ver seção 3.1 de `01_estrutura.md`. Fonte: PEP 557 – Data Classes
  (peps.python.org/pep-0557/); docs.python.org/3/library/dataclasses.html.
- **Linhas 28–31**: `prioridade`, `responsavel`, `labels`, `subtarefas`
  como campos opcionais (`None`/lista vazia via `field(default_factory=list)`)
  — decisão tomada depois de inspecionar `data/raw/data.json`: nenhuma
  issue real do export tem esses campos preenchidos (nem sequer presentes),
  então eles não podem ser obrigatórios sob risco de o `extractor.py`
  quebrar em todas as issues. Ver seção 3.1 de `01_estrutura.md`.
- **Linha 30 (`field(default_factory=list)`)**: uso de `default_factory`
  em vez de `[]` direto como valor padrão — mutable default argument é um
  erro clássico e documentado em Python (todas as instâncias
  compartilhariam a mesma lista); `dataclasses` resolve isso exigindo
  `default_factory` para tipos mutáveis. Fonte: documentação oficial de
  `dataclasses`, seção "Mutable default values"
  (docs.python.org/3/library/dataclasses.html#mutable-default-values).

---

## `src/jira/adf_parser.py`

- **Linhas 14–25 (`_text_with_marks`)**: aplica marcação Markdown conforme
  o array `marks` de um nó `text` do ADF (`strong`→`**`, `em`→`*`,
  `code`→`` ` ``, `strike`→`~~`). Fonte da lista de marks do ADF:
  developer.atlassian.com/cloud/jira/platform/apis/document/marks/
  (referenciada em `01_estrutura.md`, item 6 da bibliografia).
- **Linhas 28–38 (`_inline_content_to_text`)** e **59–92
  (`_block_node_to_lines`)**: percurso recursivo da árvore ADF — cada nó é
  despachado pelo campo `type` (`paragraph`, `heading`, `blockquote`,
  `bulletList`/`orderedList`, `codeBlock`, `rule`); tipos desconhecidos
  apenas recursam em `content` (linhas 89–92), para não quebrar caso o
  Jira introduza um tipo de nó novo. Técnica: recursive tree traversal —
  Cormen et al. (2009), *Introduction to Algorithms*, cap. sobre árvores
  (item 7 da bibliografia de `01_estrutura.md`).
- **Linhas 41–47 (`_list_item_text`)** e **50–56 (`_list_items_to_lines`)**:
  cada `listItem` do ADF pode conter múltiplos parágrafos — a função
  concatena o texto de todos eles, e `_list_items_to_lines` decide o
  prefixo Markdown (`- ` ou `N. `) conforme a lista é `bulletList` ou
  `orderedList`, seguindo a sintaxe de listas do CommonMark (item 16 da
  bibliografia).
- **Linhas 95–104 (`adf_to_markdown`)**: função pública de entrada — dado
  o `dict` inteiro de `fields.description`, itera os blocos de
  `content` (nível "doc" da árvore, conforme
  developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
  e junta os blocos renderizados com linha em branco entre eles (parágrafo
  Markdown).
- **Linhas 107–138 (`_normalize_label` e `extract_bullet_items_after_label`)**:
  função auxiliar específica para o padrão User Story + Acceptance
  Criteria (Cohn, 2004 — item 17 da bibliografia): localiza, nos nós de
  primeiro nível do documento, um parágrafo cujo texto normalizado
  (sem `*`, sem `:`, case-insensitive via `casefold()` — método
  recomendado pela documentação do Python para comparação
  case-insensitive robusta com Unicode, ao contrário de `.lower()`;
  docs.python.org/3/library/stdtypes.html#str.casefold) bate com o rótulo
  procurado, e devolve os itens da lista logo em seguida.
- **Linhas 141–168 (`strip_section_after_label`)**: adicionada depois da
  primeira execução do pipeline completo, ao notar que a descrição
  renderizada repetia os critérios de aceitação (ver nota em
  `extractor.py` acima). Percorre os nós de primeiro nível do documento
  do mesmo jeito que `extract_bullet_items_after_label`, mas devolve uma
  cópia do documento **sem** o parágrafo do rótulo e sem a lista logo em
  seguida (linhas 160–166), preservando o restante do documento na
  mesma ordem (concatenação `top_level[:index] + top_level[restante:]`,
  técnica padrão de remoção de fatia em listas Python — documentação
  oficial de sequências, docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range).

---

## `tests/test_adf_parser.py`

- Usa `pytest` (pytest.org) como test runner — biblioteca padrão de fato
  para testes em Python, com sintaxe de `assert` simples em vez de
  `self.assertEqual` (como em `unittest`).
- `test_extract_bullet_items_after_label_estrutura_real_de_story` (linhas
  92–139) replica literalmente o trecho de ADF da issue real `SCRUM-21`
  (US-15 — Avaliação do restaurante) em `data/raw/data.json`, para
  garantir que o parser funciona no formato exato que o Jira devolveu,
  não só em exemplos sintéticos.
- Os demais casos (doc vazio/`None`, marks combinadas, `bulletList`,
  label ausente) cobrem os caminhos de decisão de `_block_node_to_lines`
  e `extract_bullet_items_after_label` isoladamente — prática de
  cobertura por caminho de decisão descrita em Myers, G. J., Sandler, C.,
  & Badgett, T. (2011). *The Art of Software Testing* (3rd ed.). Wiley.
- Configuração: `pytest.ini` (raiz do projeto) define `pythonpath = .`
  para que `from src.jira.adf_parser import ...` funcione sem precisar
  instalar o projeto como pacote — opção `pythonpath` documentada em
  docs.pytest.org/en/stable/reference/reference.html#confval-pythonpath
  (disponível desde o pytest 7.0).
- `test_strip_section_after_label_remove_paragrafo_e_lista_correspondentes`,
  `..._quando_label_nao_existe_mantem_doc_igual` e `..._com_doc_none`:
  adicionados junto com `strip_section_after_label` (ver nota de correção
  em `src/jira/adf_parser.py` acima); o primeiro caso verifica as duas
  metades da correção juntas — que `adf_to_markdown` do resultado não tem
  mais o parágrafo do rótulo, e que `extract_bullet_items_after_label` no
  documento **original** (não alterado por `strip_section_after_label`,
  que devolve uma cópia) ainda enxerga a lista normalmente. Suíte
  completa: 10/10 testes passando após a correção.

---

## `src/jira/extractor.py`

- **Linhas 19, 24–28 (`load_dotenv()` e `_get_env`)**: carrega `.env` e lê
  `JIRA_DOMAIN`/`JIRA_EMAIL`/`JIRA_API_TOKEN` de variáveis de ambiente, com
  erro explícito se alguma faltar. Prática de config via ambiente: The
  Twelve-Factor App, fator III (item 13 da bibliografia de
  `01_estrutura.md`). Biblioteca: `python-dotenv`
  (pypi.org/project/python-dotenv/).
- **Linha 40 (`url = f"https://{domain}/rest/api/3/search/jql"`)**: o
  endpoint usado é `/rest/api/3/search/jql`, não o clássico `/rest/api/3/search`
  do enunciado original do projeto. Motivo: inspecionando
  `data/raw/data.json`, a resposta real tem apenas o campo `isLast` no
  nível raiz — sem `startAt`/`maxResults`/`total` — o que é a assinatura
  do endpoint novo baseado em `nextPageToken`, e não do antigo baseado em
  offset. Fonte:
  developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get.
  (O endpoint clássico `/search` está sendo descontinuado pela Atlassian
  em favor deste.)
- **Linhas 45–51**: chamada HTTP com `requests.get(..., auth=(email,
  api_token))` — a tupla `(user, pass)` no parâmetro `auth` do `requests`
  já implementa HTTP Basic Auth (RFC 7617) automaticamente, codificando
  `email:token` em Base64 no cabeçalho `Authorization`. Fonte: Requests —
  Authentication (requests.readthedocs.io/en/latest/user/authentication/)
  e developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/.
  Paginação por `nextPageToken` até `payload["isLast"]` vir `true` (linhas
  48–51), conforme a mesma referência do endpoint acima.
- **Linha 46 (`response.raise_for_status()`)**: converte um HTTP 4xx/5xx
  em exceção Python imediatamente, em vez de deixar o erro passar
  silenciosamente adiante como JSON malformado — comportamento documentado
  em requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions.
- **Linhas 56–64, 67–87 (`_parse_subtarefas`, `parse_issue`)**: convertem
  uma issue crua da API para `Artefato`/`Subtarefa` (schema de
  `src/common/schema.py`), usando `.get(...)` com *default* para os campos
  ausentes neste dataset (`priority`, `assignee`, `labels`, `subtasks` —
  ver decisão registrada em `01_estrutura.md`, seção 3.1) e indexação
  direta (`fields["summary"]` etc.) para os campos que a API do Jira
  sempre devolve. Validado rodando contra as 32 issues reais de
  `data/raw/data.json` (6 Epic, 15 História, 7 Bug, 4 Request
  classificados corretamente).
- **Linhas 90–91 (`parse_issues`)**: função pública que aplica
  `parse_issue` a toda a lista — é o que `generator.py` (próxima etapa)
  vai consumir.

**Correção pós-primeira execução**: ao rodar o pipeline pela primeira vez
contra `data/raw/data.json`, o manual saiu com os critérios de aceitação
duplicados (uma vez dentro da descrição corrida, outra vez na lista
numerada de "Passo a passo") — porque `descricao` usava o ADF completo, e
`criterios_aceitacao` extraía a mesma lista separadamente. Corrigido
adicionando `strip_section_after_label` em `adf_parser.py` (linhas
141–168) e chamando-a em `extractor.py` (linha 73:
`descricao_sem_criterios_adf = strip_section_after_label(descricao_adf, CRITERIOS_ACEITACAO_LABEL)`,
usada na linha 80 em vez do ADF bruto). Coberto por
`test_strip_section_after_label_remove_paragrafo_e_lista_correspondentes`
em `tests/test_adf_parser.py`. Reexecutado depois da correção — conferido
manualmente que `## Funcionalidades` não repete mais os critérios.

---

## `src/templating/generator.py`

- **Linhas 25–35 (`TIPO_PARA_CATEGORIA`)**: dicionário de mapeamento
  tipo-do-Jira → categoria-do-template, centralizado em um único lugar
  (fácil de estender). Inclui `"história"`/`"historia"` → `"story"` e
  `"request"` → `"task"`, decisões tomadas por você ao confirmar a
  pergunta sobre como classificar o tipo "Request" deste dataset (não há
  tipo "Task" nele) — ver seção 3.4 de `01_estrutura.md`.
- **Linhas 38–54 (`classificar_por_tipo`)**: agrupa os `Artefato` em 5
  baldes (`epic`, `story`, `task`, `bug`, `outros`); tipos não mapeados
  caem em `"outros"` em vez de serem descartados — decisão de não perder
  dado silenciosamente, prática recomendada em pipelines de dados (ver
  também a seção "Outros Itens" do template, abaixo).
- **Linhas 57–70 (`gerar_manual`)**: monta um `jinja2.Environment` com
  `FileSystemLoader` apontando para `src/templating/templates/` e chama
  `template.render(**categorias)`, passando `epic`/`story`/`task`/`bug`/`outros`
  como variáveis de contexto do template. `trim_blocks=True` e
  `lstrip_blocks=True` evitam linhas em branco extras geradas pelas tags
  `{% %}` do Jinja2 — opções documentadas em
  jinja.palletsprojects.com/en/stable/api/#jinja2.Environment.
  `select_autoescape` fica desabilitado para `.j2` porque a saída é
  Markdown, não HTML (autoescape de HTML quebraria caracteres como `<`
  usados naturalmente em texto livre) — comportamento documentado na
  mesma página da API do Jinja2.
- **Linhas 73–94 (`main`)**: script de linha de comando (`argparse`,
  biblioteca padrão do Python — docs.python.org/3/library/argparse.html)
  que liga o pipeline inteiro: lê `data/raw/data.json`, chama
  `parse_issues` (extractor) e `gerar_manual` (este módulo), grava em
  `data/manuals_generated/templating/manual.md`. É o que roda com
  `python -m src.templating.generator`.

---

## `src/templating/templates/manual_template.md.j2`

- **Linhas 7–12, 15–35, 38–43**: um `{% for %}` por categoria
  (`epic`, `story`, `task`), na ordem Visão Geral → Funcionalidades →
  Tarefas Operacionais definida em `01_estrutura.md` (que por sua vez
  segue a ISO/IEC/IEEE 26514:2008 — bibliografia item 14). Sintaxe de
  template: jinja.palletsprojects.com/en/stable/templates/.
- **Linhas 20–34 (`{% if artefato.criterios_aceitacao %} ... {% elif
  artefato.subtarefas %} ... {% endif %}`)**: o "passo a passo" da seção
  Funcionalidades usa os critérios de aceitação quando existem (caso
  deste dataset — decisão da seção "Passo a passo" registrada nesta
  conversa e em `01_estrutura.md`, item 4.2) ou, alternativamente,
  subtarefas, para o template continuar funcionando também com um export
  do Jira que tenha subtarefas em vez de critérios de aceitação.
  `{% elif %}`, em vez de dois `{% if %}` separados, evita repetir o
  cabeçalho "**Passo a passo:**" duas vezes caso um artefato viesse a ter
  os dois campos preenchidos ao mesmo tempo.
- **Linhas 46–54 (tabela de Problemas Conhecidos)**: sintaxe de tabela
  Markdown com pipes (`| Chave | Título | Status |`). Essa sintaxe não
  faz parte do CommonMark núcleo — é uma extensão do GitHub Flavored
  Markdown (GFM). Fonte: GitHub. *GitHub Flavored Markdown Spec*, seção
  4.9 (Tables extension). https://github.github.com/gfm/#tables-extension-
- **Linhas 55–64 (seção "Outros Itens")**: só aparece se `outros` não
  estiver vazio (`{% if outros %}`), evitando uma seção vazia no manual
  quando todo artefato foi classificado — mas garantindo visibilidade
  caso apareça um tipo de issue não mapeado em `TIPO_PARA_CATEGORIA`.
