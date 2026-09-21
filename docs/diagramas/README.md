# Diagramas do TCC: o que cada um mostra e onde usar

Esta pasta guarda as 8 figuras dos métodos e do estudo, em PNG. O código de cada
uma (Mermaid, editável) está em `../diagramas.md`.

## Ordem sugerida no texto (Materiais e Métodos)

| Ordem | Arquivo | Nome interno | Onde entra no texto |
|---|---|---|---|
| 1 | `estudo_desenho.png` | Figura A | Abertura da seção: visão geral do estudo |
| 2 | `estudo_matriz.png` | Figura B | Logo depois: como os 4 métodos se diferenciam |
| 3 | `dados_composicao.png` | Figura D | Subseção de materiais: conjunto de dados |
| 4 | `fig1_templating.png` | Figura 1 | Método 1: templating puro |
| 5 | `fig2_rag.png` | Figura 2 | Método 2: LLM + RAG |
| 6 | `fig3_hibrido.png` | Figura 3 | Método 3: híbrido |
| 7 | `fig4_manual.png` | Figura 4 | Método 4: manual |
| 8 | `arquitetura_modulos.png` | Figura C | Subseção de implementação e ferramentas |

Os nomes A, B, C, D e 1 a 4 são só nomes internos. No TCC, renumere na ordem em
que as figuras aparecerem (Figura 1 a 8).

---

## As figuras

### `estudo_desenho.png` — desenho do estudo
- **Mostra:** os mesmos 32 artefatos do Jira entram nos 4 métodos, saem 4
  manuais, e os 4 vão para a comparação.
- **Use para:** explicar que é um estudo comparativo com a mesma entrada.
- **Atenção:** a caixa "Comparação dos 4 manuais" está tracejada e diz
  "critérios de avaliação: a definir". Atualize quando os critérios existirem.
- **Legenda sugerida:** "Desenho do estudo: os mesmos 32 artefatos do Jira
  alimentam quatro métodos de geração de manual."
- **Nota para a legenda ou o texto:** nos métodos 2 e 3 só a variante Cohere
  (Command R, temperatura 0,3) foi executada. A variante Claude está
  implementada, mas não foi executada.

### `estudo_matriz.png` — matriz de posicionamento
- **Mostra:** linhas = quem escreve o texto (regra, LLM, pessoa); colunas = quem
  decide a estrutura (template, LLM, pessoa). Cada método ocupa uma célula. As
  células vazias são combinações que o estudo não cobre.
- **Use para:** resumir a lógica da comparação em uma imagem. Complementa ou
  substitui a tabela "quem decide texto e estrutura".
- **Detalhe:** o híbrido tem borda azul grossa (estrutura do template) e
  preenchimento laranja (texto da LLM), para mostrar que ele mistura os dois.
- **Referência:** Reiter & Dale (2000), estágios de NLG.

### `dados_composicao.png` — composição do conjunto de dados
- **Mostra:** artefatos por tipo: 15 História, 7 Bug, 6 Epic, 4 Request (n = 32).
  Contagem conferida em `data/raw/data.json`.
- **Use para:** descrever os dados. Diga na legenda ou no texto que são fictícios.
- **Mapeamento útil para o texto:** no templating, História vira
  "Funcionalidades", Request vira "Tarefas Operacionais", Epic vira "Visão
  Geral" e Bug vira "Problemas Conhecidos".

### `fig1_templating.png` — método 1: templating puro
- **Mostra:** Jira → extração e parser ADF → `Artefato` → classificação por tipo
  → template Jinja2 → manual. Nenhuma etapa usa IA.
- **Legenda sugerida:** "Nenhuma etapa usa IA; a mesma entrada gera sempre a
  mesma saída."
- **Referências:** Reiter & Dale (2000); Gatt & Krahmer (2018).
- **Atenção:** esta figura ficou sem revisão visual depois de gerada. Abra o PNG
  antes de usar.

### `fig2_rag.png` — método 2: LLM + RAG
- **Mostra:** indexação (Embed v4 → Chroma), recuperação (4 consultas fixas,
  top-k = 6, remoção de duplicatas) e geração com Command R, com citações.
- **Legenda sugerida:** "A LLM decide texto e estrutura; a recuperação só
  seleciona quais artefatos entram no contexto."
- **Referências:** Lewis et al. (2020); documentação da Cohere (Embeddings e RAG).
- **Atenção:** só a variante Cohere foi executada. Por isso a figura não mostra o
  Claude neste método. Se quiser mostrá-lo, marque como "implementado, não
  executado".

### `fig3_hibrido.png` — método 3: híbrido
- **Mostra:** a estrutura fixa (moldura azul: classificação, seções, cabeçalhos,
  template) envolvendo a parte da LLM (caixas laranja: uma chamada por seção).
- **Legenda sugerida:** "Document planning fixo (moldura azul); microplanning e
  realization delegados à LLM (caixas laranja), uma chamada por seção."
- **Ponto importante para o texto:** a estrutura é decidida antes de qualquer
  chamada à LLM. O Jinja2 só monta o resultado no fim. A LLM escreve só o corpo de
  cada seção; o prompt proíbe criar cabeçalhos. Cada chamada recebe só os
  artefatos da sua categoria.
- **Referências:** Reiter & Dale (2000); Gatt & Krahmer (2018).

### `fig4_manual.png` — método 4: manual
- **Mostra:** leitura dos artefatos um a um → interpretação → escrita do manual em
  Markdown → revisão antes de salvar (ortografia e coerência). Processo 100%
  humano, sem ferramenta de geração.
- **Legenda sugerida:** "Leitura, interpretação, escrita e revisão feitas
  manualmente."
- **Atenção:** se a legenda comparar com o "fluxo clássico de um QA manual", essa
  frase precisa de fonte. Uma opção é Myers, Sandler & Badgett (2011), que já está
  nas referências do projeto. Ou tire a comparação.
- **Dado que falta:** o tempo gasto para escrever o manual. Vale registrar, porque
  é o único método em que ele não sai de uma execução automática.

### `arquitetura_modulos.png` — módulos do sistema
- **Mostra:** os módulos de `src/` (jira, common, templating, rag, hybrid), o
  Chroma local, as APIs de LLM e o que é reaproveitado entre etapas
  (`classificar_por_tipo` e `artefato_para_texto`, setas tracejadas).
- **Use para:** a subseção de implementação. Apoia o argumento de que a
  comparação é justa, já que as etapas compartilham o mesmo modelo de dados e a
  mesma classificação.
- **Nome na legenda:** é um diagrama de módulos inspirado no C4, não um C4
  estrito. Chame de "diagrama de módulos" ou "de componentes".
- **Referências:** modelo C4 (S. Brown, c4model.com); ISO/IEC/IEEE 42010.

---

## Convenção visual (igual em todas as figuras)

- **Cinza:** dado (entrada ou saída)
- **Azul:** etapa determinística (código ou regra, sem IA)
- **Laranja:** etapa com LLM
- **Verde:** etapa humana

Explique essa convenção uma vez, na primeira figura ou numa nota do texto.

## Pendências

1. Definir os critérios de avaliação e atualizar `estudo_desenho.png`.
2. Conferir nas fontes originais as referências de C4 e ISO 42010, que foram
   citadas de memória.
3. Abrir `fig1_templating.png` para uma revisão visual.
4. Decidir se a variante Claude aparece nas figuras 2 e 3 (hoje não aparece).

## Como regenerar as imagens

O código Mermaid de cada figura está em `../diagramas.md`. Para gerar de novo, de
graça e sem site:

```
npx @mermaid-js/mermaid-cli -i figura.mmd -o figura.png -b white -s 3
```

Troque `.png` por `.svg` para obter versão vetorial, melhor para impressão.
O arquivo `.mmd` deve ter só o conteúdo do bloco, sem as cercas de código.
