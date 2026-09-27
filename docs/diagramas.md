# Diagramas dos 4 métodos (para uso no TCC)

> Como usar: copie o bloco ```mermaid de cada diagrama em https://mermaid.live,
> ajuste se quiser e exporte como PNG/SVG. Todos seguem a mesma convenção
> visual, para o leitor comparar os métodos lado a lado:
>
> - **Cinza** = dado (entrada/saída)
> - **Azul** = etapa determinística (código/regra, sem IA)
> - **Laranja** = etapa com LLM
> - **Verde** = etapa humana
>
> Entrada e saída são idênticas nos 4 métodos (mesmos 32 artefatos do Jira
> → um manual em Markdown). O que muda é o que fica no meio.

## Convenção de estilos (colar no fim de cada diagrama)

```
classDef dado fill:#eeeeee,stroke:#666,color:#000;
classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
classDef humano fill:#dcfce7,stroke:#16a34a,color:#000;
```

---

## Figura 1 — Templating puro (Jinja2)

O que mostrar: pipeline 100% determinístico. Legenda sugerida: "Nenhuma
etapa usa IA; mesma entrada gera sempre a mesma saída."

```mermaid
flowchart TB
    A["Artefatos do Jira<br/>(32 issues, JSON)"]:::dado
    B["Extração e parsing<br/>API REST + parser ADF"]:::regra
    C["Modelo padronizado<br/>Artefato (dataclass)"]:::dado
    D["Classificação por tipo<br/>Epic / Story / Request / Bug"]:::regra
    E["Template Jinja2<br/>estrutura fixa, campos brutos"]:::regra
    F["Manual em Markdown"]:::dado

    A --> B --> C --> D --> E --> F

    classDef dado fill:#eeeeee,stroke:#666,color:#000;
    classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
    classDef humano fill:#dcfce7,stroke:#16a34a,color:#000;
```

Quem decide o texto: ninguém (dados formatados). Estrutura: fixa (template).

---

## Figura 2 — LLM + RAG

O que mostrar: duas fases (indexação e recuperação) e depois a geração livre.
Legenda sugerida: "A LLM decide texto e estrutura; a recuperação só
seleciona quais artefatos entram no contexto."

```mermaid
block-beta
    columns 13
    L1["Indexação"]:2 A["Artefatos do Jira<br/>(32 issues, modelo Artefato)"]:3 space C["Embeddings dos artefatos<br/>Cohere Embed v4<br/>(search_document)"]:3 space D[("Banco vetorial<br/>Chroma")]:3
    space:13
    L2["Recuperação"]:2 Q["4 consultas fixas<br/>visão geral, funcionalidades,<br/>tarefas, problemas"]:3 space E["Embedding da consulta<br/>(search_query)"]:3 space F["Busca por similaridade<br/>top-k = 6 por consulta<br/>+ remoção de duplicatas"]:3
    space:13
    L3["Geração"]:2 I["Manual em Markdown<br/>estrutura livre<br/>+ citações por artefato"]:3 space H["Geração com LLM<br/>Cohere Command R<br/>(documents + citações)"]:3 space G["Artefatos recuperados<br/>(subconjunto)"]:3

    A --> C
    C --> D
    D --> F
    Q --> E
    E --> F
    F --> G
    G --> H
    H --> I

    classDef rotulo fill:#ffffff,stroke:#ffffff,color:#333,font-weight:bold;
    classDef dado fill:#eeeeee,stroke:#666,color:#000;
    classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
    class L1,L2,L3 rotulo
    class A,D,G,I dado
    class Q,F regra
    class C,E,H llm
```

Quem decide o texto: a LLM. Estrutura: a LLM.

> Decisão sua: o código também tem a variante Claude (Messages API) no lugar
> do Command R, mas ela **não foi executada**. Se for mostrar, desenhe como
> caixa tracejada ("H2 — Claude, implementado, não executado") ou deixe só
> na descrição da figura.

---

## Figura 3 — Híbrido (template + LLM por seção)

O que mostrar: a estrutura vem do template, a LLM só escreve o corpo de cada
seção. Legenda sugerida: "Document planning fixo (moldura azul); microplanning e
realization delegados à LLM (caixas laranja), uma chamada por seção."

```mermaid
flowchart TB
    A["Artefatos do Jira<br/>(32 issues)"]:::dado
    B["Modelo padronizado<br/>Artefato"]:::dado

    subgraph EST["Estrutura fixa: seções, ordem e cabeçalhos definidos antes da LLM#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;"]
        direction TB
        C["Classificação por tipo<br/>(mesma da Figura 1)"]:::regra

        subgraph SEC["LLM: uma chamada por seção#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;"]
            direction LR
            S1["Visão Geral<br/>(Epics)"]:::llm
            S2["Funcionalidades<br/>(Stories)"]:::llm
            S3["Tarefas Operacionais<br/>(Requests)"]:::llm
            S4["Problemas Conhecidos<br/>(Bugs)"]:::llm
        end

        T["Montagem no template Jinja2<br/>(cabeçalhos e ordem fixos)"]:::regra
    end

    F["Manual em Markdown"]:::dado

    A --> B --> C
    C --> S1 & S2 & S3 & S4
    S1 & S2 & S3 & S4 --> T
    T --> F

    style EST fill:#eff6ff,stroke:#2563eb,stroke-width:2px
    style SEC fill:#ffffff,stroke:#ea580c,stroke-dasharray:4 4

    classDef dado fill:#eeeeee,stroke:#666,color:#000;
    classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
    classDef humano fill:#dcfce7,stroke:#16a34a,color:#000;
```

Quem decide o texto: a LLM. Estrutura: fixa (template). Sem embeddings nem
recuperação. A LLM escreve só o corpo de cada seção (o prompt proíbe criar
cabeçalhos). Cada chamada recebe só os artefatos da sua categoria, não o
corpus inteiro (dizer isso na legenda da figura).

---

## Figura 4 — Manual (humana)

O que mostrar: mesmo insumo, processo inteiramente humano, sem nenhuma etapa
automatizada. Legenda sugerida: "Leitura, interpretação, escrita e revisão
feitas manualmente, como no fluxo clássico de um QA manual."

```mermaid
%%{init: {"flowchart": {"subGraphTitleMargin": {"top": 0, "bottom": 45}}}}%%
flowchart TB
    A["Artefatos do Jira<br/>(32 issues)"]:::dado

    subgraph HUM["Processo 100% humano,<br/>sem ferramenta de geração#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;#160;"]
        direction TB
        B["Leitura dos artefatos<br/>um a um"]:::humano
        C["Interpretação<br/>do conteúdo de cada artefato"]:::humano
        D["Escrita do manual<br/>em Markdown"]:::humano
        E["Revisão antes de salvar<br/>ortografia e coerência"]:::humano
    end

    F["Manual em Markdown"]:::dado

    A --> B --> C --> D --> E --> F

    style HUM fill:#f0fdf4,stroke:#16a34a,stroke-width:2px

    classDef dado fill:#eeeeee,stroke:#666,color:#000;
    classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
    classDef humano fill:#dcfce7,stroke:#16a34a,color:#000;
```

Quem decide o texto: a pessoa. Estrutura: a pessoa.

---

## Figuras adicionais para Materiais e Métodos

Ordem sugerida no texto: A (desenho do estudo) → B (matriz) → D (dados) →
Figuras 1 a 4 (um método por figura) → C (módulos). Detalhes em
`docs/diagramas/README.md`. Arquivos em
`docs/diagramas/`.

### Figura A — Desenho do estudo (`estudo_desenho.png`)

Mostra que os 4 métodos partem da mesma entrada e chegam a 4 manuais que serão
comparados. **A caixa "Comparação" está tracejada de propósito**: os critérios de
avaliação ainda não estão definidos no projeto — substitua pelo que você usar.
Legenda sugerida: "Desenho do estudo: os mesmos 32 artefatos do Jira alimentam
quatro métodos de geração de manual."

Notas para a legenda: nos métodos 2 e 3 só a variante Cohere (Command R,
temperatura 0,3) foi executada; a variante Claude está implementada, mas não
foi executada.

```mermaid
flowchart LR
    A["Artefatos do Jira<br/>32 issues<br/>(mesma entrada nos 4 métodos)"]:::dado

    subgraph MET["Quatro métodos de geração do manual"]
        direction TB
        M1["1. Templating puro<br/>Jinja2, sem IA"]:::regra
        M2["2. LLM + RAG<br/>Embed v4 + Chroma + Command R<br/>(LLM decide texto e estrutura)"]:::llm
        M3["3. Híbrido<br/>template fixo + Command R por seção<br/>(LLM escreve, template estrutura)"]:::hibrido
        M4["4. Manual<br/>leitura, escrita e revisão<br/>por uma pessoa"]:::humano
    end

    O1["Manual 1<br/>(Markdown)"]:::dado
    O2["Manual 2<br/>(Markdown)"]:::dado
    O3["Manual 3<br/>(Markdown)"]:::dado
    O4["Manual 4<br/>(Markdown)"]:::dado

    C["Comparação dos 4 manuais<br/>(critérios de avaliação: a definir)"]:::pendente

    A --> M1 --> O1
    A --> M2 --> O2
    A --> M3 --> O3
    A --> M4 --> O4
    O1 & O2 & O3 & O4 --> C

    style MET fill:#fafafa,stroke:#999,stroke-dasharray:4 4

    classDef dado fill:#eeeeee,stroke:#666,color:#000;
    classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
    classDef hibrido fill:#ffedd5,stroke:#2563eb,stroke-width:3px,color:#000;
    classDef humano fill:#dcfce7,stroke:#16a34a,color:#000;
    classDef pendente fill:#ffffff,stroke:#666,stroke-dasharray:4 4,color:#000;
```

### Figura B — Matriz de posicionamento dos métodos (`estudo_matriz.png`)

Posiciona cada método por quem escreve o texto (linhas) e quem decide a
estrutura (colunas). As células vazias são combinações que o estudo não cobre.
O híbrido tem borda azul grossa (estrutura do template) com preenchimento
laranja (texto da LLM), para ficar visível que ele mistura os dois.
Referência para a legenda: Reiter & Dale (2000), estágios de NLG.

```mermaid
block-beta
    columns 4
    corner["Texto ↓ / Estrutura →"]:1 h1["Estrutura fixa<br/>(template)"]:1 h2["Estrutura livre<br/>(decidida pela LLM)"]:1 h3["Estrutura<br/>(decidida por pessoa)"]:1
    r1["Texto: regra<br/>(dados brutos)"]:1 A["1. Templating puro"]:1 e1[" "]:1 e2[" "]:1
    r2["Texto: LLM"]:1 B["3. Híbrido"]:1 C["2. LLM + RAG"]:1 e3[" "]:1
    r3["Texto: pessoa"]:1 e4[" "]:1 e5[" "]:1 D["4. Manual"]:1

    classDef eixo fill:#eeeeee,stroke:#666,color:#000;
    classDef regra fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef llm fill:#ffedd5,stroke:#ea580c,color:#000;
    classDef hibrido fill:#ffedd5,stroke:#2563eb,stroke-width:3px,color:#000;
    classDef humano fill:#dcfce7,stroke:#16a34a,color:#000;
    classDef vazio fill:#ffffff,stroke:#cccccc,color:#ffffff;
    class corner,h1,h2,h3,r1,r2,r3 eixo
    class A regra
    class B hibrido
    class C llm
    class D humano
    class e1,e2,e3,e4,e5 vazio
```

### Figura C — Módulos do sistema (`arquitetura_modulos.png`)

Diagrama de módulos/componentes **inspirado no C4** (não é um diagrama C4
estrito: os módulos são pacotes Python de uma só aplicação, não contêineres
implantáveis). Dependências extraídas dos `import` reais em `src/`. As setas
tracejadas mostram reaproveitamento de código entre etapas
(`classificar_por_tipo` e `artefato_para_texto`). Chroma é local, em
`.chroma/rag`.

```mermaid
flowchart LR
    JIRA["Jira Cloud<br/>export em<br/>data/raw/data.json"]:::ext

    subgraph SIS["Sistema em Python"]
        subgraph COMUM["Módulos compartilhados"]
            direction TB
            JM["src/jira<br/>extractor + adf_parser<br/>(parse_issues)"]:::mod
            SCH["src/common<br/>schema.py<br/>(Artefato)"]:::mod
            JM --> SCH
        end

        RAG["src/rag<br/>indexer, retriever,<br/>backends, pipeline"]:::mod
        HYB["src/hybrid<br/>generator + section_backend<br/>+ template Jinja2"]:::mod
        TPL["src/templating<br/>generator<br/>+ template Jinja2"]:::mod
        CHROMA[("Chroma<br/>banco vetorial local")]:::mod
    end

    LLMAPI["APIs de LLM<br/>Cohere: Embed v4 e Command R (executado)<br/>Anthropic: Claude (implementado, não executado)"]:::ext

    JIRA --> COMUM
    COMUM --> RAG
    COMUM --> HYB
    COMUM --> TPL

    HYB -. "reusa artefato_para_texto" .-> RAG
    HYB -. "reusa classificar_por_tipo" .-> TPL

    RAG --> CHROMA
    RAG --> LLMAPI
    HYB --> LLMAPI

    style SIS fill:#fafafa,stroke:#666,stroke-width:2px
    style COMUM fill:#eff6ff,stroke:#2563eb

    classDef mod fill:#dbeafe,stroke:#2563eb,color:#000;
    classDef ext fill:#eeeeee,stroke:#666,color:#000;
```

### Figura D — Composição do conjunto de dados (`dados_composicao.png`)

Contagem por tipo conferida direto em `data/raw/data.json`: 15 História, 7 Bug,
6 Epic e 4 Request (total 32). Para a legenda: os dados são fictícios; no
método de templating, História vira "Funcionalidades", Request vira "Tarefas
Operacionais", Epic vira "Visão Geral" e Bug vira "Problemas Conhecidos".
Uma série só, por isso sem legenda de cores; os valores estão rotulados nas
barras.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"xyChart": {"plotColorPalette": "#2a78d6"}}, "xyChart": {"showDataLabel": true, "titleFontSize": 30, "xAxis": {"labelFontSize": 24, "titleFontSize": 24}, "yAxis": {"labelFontSize": 24, "titleFontSize": 24}}}}%%
xychart-beta horizontal
    title "Artefatos por tipo (n = 32)"
    x-axis ["História", "Bug", "Epic", "Request"]
    y-axis "Quantidade de artefatos" 0 --> 16
    bar [15, 7, 6, 4]
```

### Referências sugeridas para as legendas das figuras adicionais

Estas referências vêm de memória e **precisam ser conferidas nas fontes originais antes
de entrar no TCC**.

| Figura | Referência |
|---|---|
| A, B | Reiter & Dale (2000); Gatt & Krahmer (2018), já nos docs de cada etapa |
| C | Modelo C4 (S. Brown, c4model.com); ISO/IEC/IEEE 42010 (descrição de arquitetura) |
| D | Sem referência de método; cite a origem dos dados (`data/raw/data.json`) |

### Como regenerar os PNGs (gratuito, local)

```
npx @mermaid-js/mermaid-cli -i figura.mmd -o figura.png -b white -s 3
```

Troque `.png` por `.svg` para vetorial. O bloco mermaid de cada figura vai num
arquivo `.mmd` (só o conteúdo, sem as cercas de código).

---

## Sugestão de legendas com fonte (o TCC exige referência para cada método)

Todas já constam nos documentos de cada etapa:

| Figura | Referência para citar na legenda |
|---|---|
| 1 | Reiter & Dale (2000); Gatt & Krahmer (2018) — abordagem *template-based* de NLG |
| 2 | Lewis et al. (2020) — RAG; Cohere (Embeddings e RAG, docs oficiais) |
| 3 | Reiter & Dale (2000) — estágios de NLG; Gatt & Krahmer (2018) — arquiteturas híbridas |
| 4 | Sem referência de código; se quiser embasar a estrutura do manual: ISO/IEC/IEEE 26514:2008 |

## Extra opcional: quadro-resumo (pode virar uma Figura 5 ou tabela)

| Método | Texto | Estrutura | Usa LLM | Usa recuperação |
|---|---|---|---|---|
| Templating | dados brutos | fixa | não | não |
| LLM + RAG | LLM | LLM | sim | sim |
| Híbrido | LLM | fixa | sim | não |
| Manual | humana | humana | não | não |
