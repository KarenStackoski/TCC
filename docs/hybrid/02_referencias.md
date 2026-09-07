# Referências ponto a ponto — Etapa 3 (Híbrido)

> Preenchido no mesmo formato de `docs/templating/02_referencias.md` e
> `docs/rag/02_referencias.md`. O panorama geral (arquitetura, decisões
> antes de codar) está em `01_estrutura.md`.

## Status geral

| Arquivo | Status |
|---|---|
| `src/hybrid/section_backend.py` | ✅ implementado |
| `src/hybrid/templates/manual_hibrido.md.j2` | ✅ implementado |
| `src/hybrid/generator.py` | ✅ implementado |
| `tests/test_hybrid_section_backend.py` | ✅ implementado (5/5 passando) |
| `tests/test_hybrid_generator.py` | ✅ implementado (3/3 passando) |
| Execução ponta a ponta (variante `cohere`) contra `data/raw/data.json` | ✅ executada com sucesso, após duas correções (ver seção "Bugs encontrados e corrigidos" abaixo) |
| Variante `claude` | implementada e coberta por teste puro (`montar_prompt_claude`), **não executada** — mesma decisão da Etapa 2 (sem `ANTHROPIC_API_KEY` paga configurada) |

---

## `src/hybrid/section_backend.py`

- **Linhas 31–34 (constantes de modelo)**: `COHERE_CHAT_MODEL`/`CLAUDE_CHAT_MODEL`
  idênticos aos usados em `src/rag/cohere_backend.py`/`claude_backend.py`
  (Etapa 2) — mesma justificativa de escolha de modelo, já registrada em
  `docs/rag/01_estrutura.md`, seções 3.3 e 3.4. `CLAUDE_MAX_TOKENS = 4096`
  reaproveita o valor já usado em `claude_backend.py` (`MAX_TOKENS`).
- **Linhas 36–47 (`SYSTEM_PROMPT_HIBRIDO`)**: diferente do `SYSTEM_PROMPT`
  da Etapa 2 — instrui a LLM a **não** decidir estrutura (nem cabeçalho de
  seção, nem subtítulos no mesmo nível do cabeçalho fixo) e a escrever
  apenas o corpo de uma seção específica. Ver justificativa completa em
  `docs/hybrid/01_estrutura.md`, seção 3.2.
- **Linhas 58–97 (`SECTION_CONFIG`)**: dicionário `categoria -> (título,
  instrução)`, mesmo padrão de configuração centralizada de
  `TIPO_PARA_CATEGORIA` (Etapa 1) e `QUERIES_PADRAO` (Etapa 2). As chaves
  são exatamente as cinco categorias devolvidas por
  `src.templating.generator.classificar_por_tipo` (`epic`, `story`, `task`,
  `bug`, `outros`) — verificado por
  `test_section_config_cobre_as_cinco_categorias_de_classificar_por_tipo`.
- **Linhas 99–112 (`_formatar_documentos_cohere`)**: idêntica em estrutura
  a `_formatar_documentos` de `src/rag/cohere_backend.py` (Etapa 2, não
  reaproveitada por ser função privada do outro módulo — duplicação
  pequena e intencional, mesmo padrão de `cohere_backend.py` e
  `claude_backend.py` já não compartilharem `SYSTEM_PROMPT` entre si na
  Etapa 2).
- **Linhas 114–139 (`gerar_secao_cohere`)**: chama `cliente.chat(...)` com
  `documents=` só com os artefatos da categoria (não o corpus inteiro) —
  fonte: Cohere. *Retrieval Augmented Generation (RAG)*.
  https://docs.cohere.com/docs/retrieval-augmented-generation-rag (já
  citada na Etapa 2). Linha 118: devolve `("", [])` sem chamar a API
  quando `artefatos` está vazio (ex.: dataset sem bugs) — evita erro e
  evita gastar chamada de API por uma seção vazia; testado em
  `test_gerar_secao_cohere_com_lista_vazia_nao_chama_api`.
- **Linhas 142–150 (`_montar_documento_xml_claude`)** e **152–162
  (`montar_prompt_claude`)**: mesma estrutura de
  `src/rag/claude_backend.py` (`_montar_documento_xml`/`montar_prompt`),
  parametrizada pela instrução da categoria em vez da instrução fixa da
  Etapa 2. Fonte: Anthropic. *Claude prompting best practices — Long
  context prompting* (já citada na Etapa 2). Testado em
  `test_montar_prompt_claude_usa_instrucao_da_categoria` e
  `test_montar_prompt_claude_troca_instrucao_conforme_categoria`.
- **Linhas 164–184 (`gerar_secao_claude`)**: mesma estrutura de
  `claude_backend.gerar_manual` (Etapa 2), parametrizada por categoria.
  Implementada e testada (a parte pura, `montar_prompt_claude`), **não
  executada** nesta sessão — decisão já registrada de não usar
  `ANTHROPIC_API_KEY` paga por enquanto (`docs/PROGRESSO.md`, Sessão 2).

### Bugs encontrados e corrigidos nesta sessão

1. **Truncamento da seção "Funcionalidades" (`MAX_TOKENS`)**: a primeira
   execução ponta a ponta gerou `manual_cohere.md` com a seção
   "Funcionalidades" cortada no meio de uma frase, terminando com uma tag
   de citação bruta e incompleta (`<co: 1>Quando o status do pedido mudar
   para "Sai`). Diagnóstico (script isolado chamando só a seção `story`,
   15 artefatos): `resposta.finish_reason == "MAX_TOKENS"`,
   `usage.tokens.output_tokens == 4096`. Confirmado com a documentação
   oficial (Cohere, *Chat API reference*,
   https://docs.cohere.com/reference/chat) que **4096 é o teto de saída do
   próprio modelo** `command-r-08-2024` (não um valor configurável para
   cima via `max_tokens`) — logo a correção não podia ser "aumentar o
   limite", só reduzir o texto necessário para caber nele. A mesma
   documentação confirma que o Command R **não** embute citações inline
   (`<co: N>...</co>`) na resposta em condições normais — elas só existem
   como resposta estruturada em `message.citations`; a tag bruta observada
   era um artefato do corte abrupto no meio da resolução interna da
   citação, não um formato esperado da API. **Correção**: `SYSTEM_PROMPT_HIBRIDO`
   (linhas 36–47) e a instrução de `story` em `SECTION_CONFIG` (linhas
   64–71) passaram a pedir explicitamente concisão (2–3 frases por
   artefato, resumindo Critérios de Aceitação em vez de listá-los por
   extenso). Reexecutado isoladamente após a correção: `finish_reason ==
   "COMPLETE"`, 2634 tokens de saída (bem abaixo do teto), sem tags soltas.
2. **Subtítulos da LLM no mesmo nível do cabeçalho fixo da seção**: a
   mesma primeira execução mostrou a LLM usando `##` (nível 2, mesmo nível
   de `## Funcionalidades`/`## Tarefas Operacionais`) para subtítulos
   internos por artefato/grupo de artefatos — quebra a hierarquia de
   cabeçalhos do documento (CommonMark, https://spec.commonmark.org/, já
   citada na Etapa 1) e destoa do padrão da Etapa 1
   (`manual_template.md.j2` usa `###` para cada artefato dentro de uma
   seção `##`). **Correção**: instrução explícita adicionada a
   `SYSTEM_PROMPT_HIBRIDO` (linhas 44–47) pedindo nível 3 (`###`) ou mais
   profundo para qualquer subtítulo interno. Reverificado isoladamente
   (categoria `task`, 4 artefatos): saída usa `###` corretamente.
   Suíte de testes (31/31) roda sem custo de API antes/depois dessas
   correções — os dois bugs só apareciam na execução real contra a API,
   não nas funções puras testadas (mesma limitação já registrada em
   `docs/rag/02_referencias.md` para `indexar`/`recuperar`/`gerar_manual`).

---

## `src/hybrid/templates/manual_hibrido.md.j2`

- Mesmos cabeçalhos e mesma ordem de seções de `manual_template.md.j2`
  (Etapa 1): Visão Geral, Funcionalidades, Tarefas Operacionais, Problemas
  Conhecidos, Outros Itens (condicional, só se não vazio — mesmo
  `{% if secoes.outros %}` que `{% if outros %}` da Etapa 1). Diferença:
  não há `{% for %}` sobre artefatos — cada seção recebe uma única
  variável de texto (`{{ secoes.epic }}` etc.), já gerada por
  `section_backend.py`. Ver `docs/hybrid/01_estrutura.md`, seção 3.3.

---

## `src/hybrid/generator.py`

- **Linhas 22–31 (`VARIANTES_DISPONIVEIS`, `ORDEM_CATEGORIAS`)**: mesmo
  mecanismo de `src/rag/pipeline.py` (Etapa 2) para `VARIANTES_DISPONIVEIS`;
  `ORDEM_CATEGORIAS` fixa a ordem de renderização das seções, igual à
  ordem de `manual_template.md.j2`.
- **Linhas 34–44 (`_formatar_citacoes`)**: adaptação de
  `src.rag.pipeline._formatar_citacoes` (Etapa 2) para agrupar citações por
  seção (título da seção como sub-cabeçalho), já que agora há uma lista de
  citações por categoria, não uma lista única para o documento inteiro.
  Testada em `tests/test_hybrid_generator.py`.
- **Linhas 47–55 (`_renderizar`)**: mesmas opções de `Environment`
  (`trim_blocks`, `lstrip_blocks`, `select_autoescape` desabilitado para
  `.j2`) de `src/templating/generator.gerar_manual` (Etapa 1) — mesma
  fonte (jinja.palletsprojects.com).
- **Linhas 58–83 (`gerar_manuais`)**: reaproveita
  `classificar_por_tipo` de `src/templating/generator.py` (Etapa 1, sem
  alteração — ver `docs/hybrid/01_estrutura.md`, seção 3.1) em vez de
  `indexar`/`recuperar` (Etapa 2): não há embeddings nem recuperação nesta
  etapa, como já previsto em `docs/rag/01_estrutura.md`, seção 4. Para
  cada categoria em `ORDEM_CATEGORIAS`, chama `gerar_secao_cohere`
  (ou `gerar_secao_claude`) uma vez — a "uma chamada por seção" da
  arquitetura. Testada com lista de artefatos vazia (nenhuma chamada de
  API) em `test_gerar_manuais_com_lista_vazia_nao_chama_nenhuma_api`.
- **Linhas 86–110 (`main`)**: mesmo formato de CLI (`argparse`, flag
  `--variante` repetível) de `src/rag/pipeline.py` (Etapa 2), gravando em
  `data/manuals_generated/hybrid/manual_<variante>.md`.

---

## `tests/test_hybrid_section_backend.py`, `tests/test_hybrid_generator.py`

- Mesmo estilo das outras etapas: `pytest` puro, `assert` simples, cobrindo
  só as funções determinísticas (`SECTION_CONFIG`, `montar_prompt_claude`,
  `_formatar_citacoes`, o caminho de lista vazia de `gerar_secao_cohere`/
  `gerar_secao_claude`/`gerar_manuais`) — mesma filosofia de Myers, Sandler
  & Badgett (2011), já citada nas Etapas 1 e 2. As funções que chamam a API
  real (`gerar_secao_cohere`/`gerar_secao_claude` com artefatos não vazios)
  não têm teste automatizado — cobertas pela execução ponta a ponta
  (incluindo os dois bugs encontrados e corrigidos acima), mesma decisão
  já registrada para a Etapa 2.
- Suíte completa do projeto após a Etapa 3: **31/31 testes passando**
  (23 das Etapas 1–2 + 8 novos).

---

## Execução ponta a ponta

`python -m src.hybrid.generator --variante cohere` contra
`data/raw/data.json` real (32 artefatos: 6 Epic, 15 História, 7 Bug, 4
Request) → `data/manuals_generated/hybrid/manual_cohere.md`. Resultado
final (após as duas correções acima):

- 4 seções fixas (`## Visão Geral`, `## Funcionalidades`, `## Tarefas
  Operacionais`, `## Problemas Conhecidos`), nenhuma seção "Outros Itens"
  (dataset não tem artefatos fora das 4 categorias mapeadas).
- Sem truncamento (`finish_reason == "COMPLETE"` em todas as 4 chamadas) e
  sem tags de citação soltas no texto.
- Hierarquia de cabeçalhos correta: subtítulos internos em `###`, nunca no
  mesmo nível do cabeçalho fixo da seção.
- Citações do Command R presentes por seção, agrupadas no rodapé do
  documento por `_formatar_citacoes`, cada uma apontando para uma chave
  real do Jira (ex.: `SCRUM-22` para o BUG-01).
- Ainda falta revisão de conteúdo linha a linha pelo usuário (mesmo
  processo de conferência manual das Etapas 1 e 2).
