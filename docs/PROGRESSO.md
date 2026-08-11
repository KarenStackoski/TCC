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
