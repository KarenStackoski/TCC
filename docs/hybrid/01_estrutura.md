# Etapa 3 — Híbrido (template + LLM por seção): estrutura e fundamentação teórica

> Documento de arquitetura da Etapa 3 do TCC. Escrito **antes** da implementação,
> como nas Etapas 1 e 2. O detalhamento técnico linha a linha fica em
> `02_referencias.md`, preenchido conforme cada arquivo é implementado.

## 1. Papel desta etapa na comparação do TCC

Retomando a tabela de `docs/templating/01_estrutura.md` e `docs/rag/01_estrutura.md`:

| Etapa | Quem decide o **texto** | Quem decide a **estrutura** |
|---|---|---|
| 1. Templating puro | ninguém (dados brutos formatados) | fixa, definida no template `.j2` |
| 2. RAG (Claude + Cohere) | a LLM | a LLM |
| 3. Híbrido | a LLM (reescreve/naturaliza) | fixa, definida no template `.j2` |

A Etapa 3 combina as duas anteriores: a **estrutura** volta a ser fixa (as
mesmas quatro categorias/seções da Etapa 1 — Visão Geral, Funcionalidades,
Tarefas Operacionais, Problemas Conhecidos — mais "Outros Itens" quando
aplicável), mas o **texto** de cada seção deixa de ser a concatenação
literal de `titulo`/`descricao` dos artefatos e passa a ser gerado por uma
LLM, uma chamada por seção (não uma chamada para o documento inteiro, como
na Etapa 2, nem zero chamadas, como na Etapa 1).

Essa divisão tem uma base teórica direta em Reiter, E., & Dale, R. (2000).
*Building Natural Language Generation Systems*, já citado em
`docs/templating/01_estrutura.md`: os autores separam a geração de
linguagem natural em três estágios — **document planning** (o que dizer e
em que ordem), **microplanning** (como estruturar frases/parágrafos) e
**realization** (o texto de superfície final). Na Etapa 1, os três estágios
são resolvidos deterministicamente pelo template. Na Etapa 2, os três são
delegados à LLM. Na Etapa 3, o **document planning fica fixo** (a
classificação por tipo e a ordem das seções, herdadas de
`src/templating/generator.py`), e **microplanning + realization são
delegados à LLM**, mas com escopo restrito a uma seção por vez — a LLM
nunca decide "o que vai em qual seção", só "como escrever, dentro da seção
que já foi decidida para ela". Gatt, A., & Krahmer, E. (2018) — já citado
nas Etapas 1 e 2 — também discute, na seção sobre arquiteturas de NLG,
pipelines que combinam estágios simbólicos/baseados em regra com estágios
neurais; a Etapa 3 é uma instância direta desse tipo de arquitetura híbrida
aplicada a um caso concreto.

## 2. Visão geral do pipeline

```
                    data/raw/data.json
                            │
             src/jira/extractor.py (reaproveitado sem alteração)
                            │
                     lista de Artefato
                            │
        src/templating/generator.py:classificar_por_tipo
        (reaproveitada sem alteração da Etapa 1 — MESMO
         agrupamento epic/story/task/bug/outros)
                            │
              dict[categoria, list[Artefato]]
                            │
        ┌───────────┬───────────┬───────────┬───────────┐
        ▼           ▼           ▼           ▼           ▼
      epic        story        task        bug        outros (se houver)
        │           │           │           │           │
   src/hybrid/section_backend.py — uma chamada de LLM por categoria,
   com instrução específica da seção (SECTION_CONFIG), documentos =
   só os artefatos daquela categoria (não o corpus inteiro)
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
   texto da     texto da     texto da     texto da    texto de
  Visão Geral  Funcionalid.  Tarefas Op.  Problemas    Outros
                                          Conhecidos    Itens
        └───────────┴───────────┴───────────┴───────────┘
                            │
        src/hybrid/templates/manual_hibrido.md.j2
        (estrutura fixa: cabeçalhos + ordem das seções;
         o corpo de cada seção é o texto já gerado acima)
                            │
                 manual_cohere.md / manual_claude.md
                    (data/manuals_generated/hybrid/)
```

`src/hybrid/generator.py` orquestra o pipeline acima, mesmo formato de CLI
(`argparse`, flag `--variante` repetível) de `src/rag/pipeline.py` (Etapa 2).

## 3. Decisões técnicas por módulo (com fonte)

### 3.1 Reaproveitamento de `classificar_por_tipo` (não duplicado)

A classificação por tipo (`epic`/`story`/`task`/`bug`/`outros`, com o
mapeamento `TIPO_PARA_CATEGORIA` já documentado em
`docs/templating/01_estrutura.md`, seção 3.4) é importada de
`src/templating/generator.py`, sem duplicação de lógica — mesmo princípio
de reaproveitamento já registrado em `docs/templating/01_estrutura.md`,
seção 5, para `schema.py`: a Etapa 3 usa exatamente a mesma definição de
"o que é uma Story vs. uma Task" que a Etapa 1, o que é necessário para a
comparação entre etapas fazer sentido (mesmo document planning nas duas).

### 3.2 `src/hybrid/section_backend.py` — geração de texto por seção

- **Granularidade da chamada — uma por seção, não uma por artefato nem uma
  para o documento inteiro**: decisão já registrada em
  `docs/rag/01_estrutura.md`, seção 4 ("Ligação com a Etapa 3"), ao term
  fim da Etapa 2. Uma chamada por artefato desperdiçaria a oportunidade da
  LLM de dar coesão ao texto entre artefatos da mesma seção (ex.: evitar
  repetir "esta funcionalidade permite..." em cada Story); uma chamada só
  para o documento inteiro (como a Etapa 2) devolveria a decisão de
  estrutura para a LLM, o que descaracterizaria a Etapa 3 como híbrida.
- **`SECTION_CONFIG`**: dicionário `categoria -> (titulo_secao, instrucao)`,
  mesmo padrão de dicionário de configuração centralizado já usado em
  `TIPO_PARA_CATEGORIA` (Etapa 1) e `QUERIES_PADRAO` (Etapa 2). A instrução
  é específica por categoria (ex.: a de `story` pede passo a passo a partir
  dos Critérios de Aceitação; a de `bug` pede que cada problema traga
  chave/título/status para rastreabilidade) — decisão de incluir também
  "Problemas Conhecidos" na reescrita por LLM (e não como tabela
  determinística, como na Etapa 1) confirmada com o usuário nesta sessão:
  abordagem uniforme entre as 4 categorias, mesmo tratamento para todas.
- **`SYSTEM_PROMPT_HIBRIDO` diferente do `SYSTEM_PROMPT` da Etapa 2**: a
  Etapa 2 instrui a LLM a decidir livremente títulos e ordem de seções
  (`docs/rag/02_referencias.md`, `cohere_backend.py`/`claude_backend.py`,
  `INSTRUCAO`); a Etapa 3 faz o oposto — instrui explicitamente a LLM a
  **não** incluir um cabeçalho de seção (o cabeçalho já vem do template
  `.j2`) e a escrever só o corpo daquela seção específica, usando somente
  os artefatos daquela categoria como contexto (não o corpus inteiro). É a
  operacionalização, no prompt, da linha "estrutura: fixa" da tabela da
  seção 1 — mesmo raciocínio de operacionalizar a tabela em texto de prompt
  já usado em `docs/rag/01_estrutura.md`, seção 3.3, para a linha
  "estrutura: a LLM" da Etapa 2.
- **Reaproveita `artefato_para_texto`** de `src/rag/indexer.py` (Etapa 2,
  sem alteração) para achatar cada artefato da categoria em texto — mesmo
  motivo de evitar divergência entre representações já registrado em
  `docs/rag/02_referencias.md` para `cohere_backend.py`.
- **Backend Cohere (`gerar_secao_cohere`)**: mesmo modelo (`command-r-08-2024`),
  mesmo uso do parâmetro `documents=` para geração fundamentada (*grounded*)
  com citações automáticas — só que os documentos passados são o
  subconjunto de artefatos da categoria, não o corpus inteiro recuperado.
  Fonte: Cohere. *Retrieval Augmented Generation (RAG)*.
  https://docs.cohere.com/docs/retrieval-augmented-generation-rag (já
  citada em `docs/rag/01_estrutura.md`).
- **Backend Claude (`gerar_secao_claude`)**: mesmo modelo
  (`claude-sonnet-5`) e mesmo formato de prompt com documentos em XML
  (`<documents>`/`<document>`/`<document_content>`) recomendado pela
  Anthropic, já usado em `src/rag/claude_backend.py` — fonte: Anthropic.
  *Claude prompting best practices — Long context prompting* (já citada em
  `docs/rag/01_estrutura.md`, seção 3.4). Implementado e testado nesta
  sessão, mas **não executado**, pela mesma decisão da Etapa 2: o usuário
  não quer gastar a API paga da Anthropic por enquanto (`docs/PROGRESSO.md`,
  Sessão 2). `gerar_manuais()` em `src/hybrid/generator.py` só chama a
  variante pedida, mesmo mecanismo do parâmetro `variantes` de
  `src/rag/pipeline.py`.

### 3.3 `src/hybrid/templates/manual_hibrido.md.j2` — estrutura fixa

- **Diferença em relação a `manual_template.md.j2` (Etapa 1)**: o template
  da Etapa 1 itera artefato por artefato dentro de cada seção
  (`{% for artefato in story %}`), imprimindo campos brutos. O template da
  Etapa 3 não itera artefatos — cada seção recebe uma única variável de
  texto já pronta (`{{ secoes.visao_geral }}` etc.), produzida por
  `section_backend.py`. A ordem e os cabeçalhos das seções (`## Visão
  Geral`, `## Funcionalidades`, `## Tarefas Operacionais`, `## Problemas
  Conhecidos`, `## Outros Itens` se houver) são idênticos aos da Etapa 1 —
  mesma fonte da estrutura de documentação de usuário: ISO/IEC/IEEE
  26514:2008 (já citada em `docs/templating/01_estrutura.md`, seção 3.5).
- **Motor de template**: Jinja2, mesma fonte já citada
  (jinja.palletsprojects.com) — reaproveitado por consistência mesmo não
  havendo laço (`for`) sobre artefatos nesta etapa, para manter o mesmo
  mecanismo de "estrutura definida fora do código Python" das outras
  etapas, em vez de concatenar strings diretamente em `generator.py`.

### 3.4 `src/hybrid/generator.py` — orquestração

- Mesmo formato de `src/rag/pipeline.py` (Etapa 2): `gerar_manuais(artefatos,
  variantes)` e `main()` com `argparse`, flag `--variante` repetível,
  gravando em `data/manuals_generated/hybrid/manual_<variante>.md`.
- Diferença: não há indexação nem recuperação (Chroma/embeddings) nesta
  etapa — como já previsto em `docs/rag/01_estrutura.md`, seção 4: "Não há
  geração de embeddings/recuperação na Etapa 3 (a estrutura já vem do
  template, não precisa ser 'descoberta' via retrieval)". `generator.py`
  chama `classificar_por_tipo` diretamente sobre a lista completa de
  artefatos, sem passar por `indexar`/`recuperar`.

## 4. Referências completas

Todas já citadas em `docs/templating/01_estrutura.md` e
`docs/rag/01_estrutura.md`; reunidas aqui pelas partes relevantes a esta
etapa:

1. Reiter, E., & Dale, R. (2000). *Building Natural Language Generation
   Systems*. Cambridge University Press.
2. Gatt, A., & Krahmer, E. (2018). Survey of the State of the Art in
   Natural Language Generation. *Journal of Artificial Intelligence
   Research*, 61, 65–170.
3. Cohere. *Retrieval Augmented Generation (RAG)*.
   https://docs.cohere.com/docs/retrieval-augmented-generation-rag
4. Cohere. *Models overview*. https://docs.cohere.com/docs/models
5. Anthropic. *Claude prompting best practices*.
   https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
6. Anthropic. *Models overview*.
   https://platform.claude.com/docs/en/models/overview
7. Pallets Projects. Jinja2 Documentation. https://jinja.palletsprojects.com/
8. ISO/IEC/IEEE 26514:2008. Systems and software engineering —
   Requirements for designers and developers of user documentation.
