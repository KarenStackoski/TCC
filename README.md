# Geração de manuais de usuário a partir de artefatos ágeis

Código e dados do TCC **"Análise comparativa de métodos de geração de texto na
automação de manuais de usuário"** (Karen Bialescki Stackoski, Ciência da
Computação, UNESC).

O projeto gera um manual de usuário a partir de 32 artefatos de um projeto no
Jira (épicos, histórias, bugs e melhorias) por quatro métodos, e compara os
resultados:

| Método | Quem define a estrutura | Quem escreve o texto | Código |
|---|---|---|---|
| Templating | template Jinja2 | os próprios dados | `src/templating/` |
| RAG | LLM (Cohere Command R) | LLM | `src/rag/` |
| Híbrido | template Jinja2 | LLM, uma chamada por seção | `src/hybrid/` |
| Manual | a autora | a autora | `data/manuals_generated/manual/manual.md` |

**Os dados do Jira já estão no repositório** (`data/raw/data.json`). Não é
preciso ter acesso ao Jira nem configurar as credenciais dele: basta rodar os
comandos abaixo.

---

## Sumário

1. [O que já está no repositório](#1-o-que-já-está-no-repositório)
2. [Preparar o ambiente](#2-preparar-o-ambiente)
3. [Caminho A: refazer os números a partir dos dados salvos (sem API)](#3-caminho-a-refazer-os-números-a-partir-dos-dados-salvos-sem-api)
4. [Caminho B: gerar os manuais de novo (com API)](#4-caminho-b-gerar-os-manuais-de-novo-com-api)
5. [Onde está cada número do TCC](#5-onde-está-cada-número-do-tcc)
6. [O que não sai de um comando](#6-o-que-não-sai-de-um-comando)
7. [Estrutura do repositório](#7-estrutura-do-repositório)

---

## 1. O que já está no repositório

Tudo o que foi usado para chegar aos resultados está versionado:

| Pasta ou arquivo | Conteúdo |
|---|---|
| `data/raw/data.json` | Retorno da API REST do Jira com os 32 artefatos (entrada de todos os métodos) |
| `data/manuals_generated/` | Os 4 manuais avaliados na fidelidade, no BERTScore e na LLM avaliadora (um por método) |
| `data/evaluation/execucoes/` | Os 10 manuais de cada método automatizado gerados no benchmark |
| `data/evaluation/tempos.csv` | Tempo e tokens de cada execução, com o SHA-256 de cada manual |
| `data/evaluation/tempo_manual.csv` | Tempo cronometrado da redação manual |
| `data/evaluation/fidelidade/` | Anotação frase a frase da fidelidade (1ª rodada) e a reanotação da autora |
| `data/evaluation/juiz_llm/` | Notas da LLM avaliadora para cada manual |
| `data/evaluation/termos_tecnicos/glossario.csv` | Glossário de termos técnicos |
| `data/evaluation/resultados.md` | Relatório com todos os números |

Por isso há dois caminhos:

- **Caminho A (recomendado):** recalcula todas as métricas e testes
  estatísticos a partir dos manuais e das anotações salvos. Não precisa de
  chave de API e chega exatamente aos números do TCC.
- **Caminho B:** gera os manuais de novo, chamando a API da Cohere. Os métodos
  com LLM não são determinísticos e o tempo depende da rede, então os textos e
  os tempos serão outros. Serve para conferir que o código funciona e que os
  resultados ficam na mesma ordem de grandeza. Só o templating gera um texto
  idêntico ao salvo.

---

## 2. Preparar o ambiente

Testado no Windows 11 com **Python 3.14.3**. Os comandos usam a sintaxe do
PowerShell. No Linux ou no macOS, troque `.\venv\Scripts\Activate.ps1` por
`source venv/bin/activate`.

Todos os comandos devem ser rodados **na raiz do repositório** (a pasta deste
README), porque os caminhos dos arquivos são relativos a ela.

```powershell
# 1. Criar e ativar o ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar as dependências (inclui PyTorch, por causa do BERTScore; pode demorar)
pip install -r requirements.txt

# 3. Rodar os testes automatizados
python -m pytest
```

O resultado esperado dos testes é `78 passed`. Os testes não chamam nenhuma
API.

### Chave da API (só para o caminho B e para a LLM avaliadora)

Copie o arquivo de exemplo e preencha **apenas** `COHERE_API_KEY`:

```powershell
Copy-Item .env.example .env
```

A chave gratuita (*trial*) da Cohere é criada em
<https://dashboard.cohere.com/api-keys>. Ela é suficiente para este projeto,
mas tem limite de chamadas por minuto e por mês. As variáveis `JIRA_*`
**não são necessárias**, porque o retorno do Jira já está em
`data/raw/data.json`. `ANTHROPIC_API_KEY` também não é necessária, porque a
variante com Claude foi implementada, mas não foi usada no estudo.

---

## 3. Caminho A: refazer os números a partir dos dados salvos (sem API)

Rode os comandos nesta ordem. Nenhum deles precisa de chave de API, e nenhum
altera os manuais ou as anotações: eles só recalculam as tabelas.

```powershell
# 1. Fidelidade e cobertura, a partir das planilhas anotadas
python -m src.evaluation.fidelidade analisar

# 2. Concordância entre a 1ª rodada da anotação e a reanotação da autora (kappa)
python -m src.evaluation.reanotacao concordancia

# 3. Vocabulário técnico em todas as execuções, com os testes estatísticos
python -m src.evaluation.termos_tecnicos

# 4. Relatório consolidado: tempo, legibilidade, BERTScore, variação entre
#    execuções, notas da LLM avaliadora e testes de Mann-Whitney com ajuste de Holm
python -m src.evaluation.relatorio

# 5. Figura do tempo de cada execução (Apêndice A do TCC)
python -m src.evaluation.grafico_tempo
```

O que cada comando faz:

| Comando | Lê | Grava |
|---|---|---|
| `fidelidade analisar` | `data/evaluation/fidelidade/{templating,rag,hibrido,manual}.csv` | `data/evaluation/fidelidade/resultado.csv` |
| `reanotacao concordancia` | as mesmas planilhas e `data/evaluation/fidelidade/reanotacao/*.csv` | `data/evaluation/fidelidade/reanotacao/concordancia.csv` |
| `termos_tecnicos` | `data/evaluation/execucoes/`, o manual humano e o glossário | `data/evaluation/termos_tecnicos/*.csv` |
| `relatorio` | os manuais, `tempos.csv`, `tempo_manual.csv` e as notas da LLM avaliadora | `metricas_automaticas.csv`, `variacao.csv`, `execucoes_individuais.csv`, `estatistica.csv` e `resultados.md`, em `data/evaluation/` |
| `grafico_tempo` | `data/evaluation/tempos.csv` | `data/evaluation/fig5_tempo_execucoes.png` |

**Na primeira vez**, o `relatorio` baixa o modelo `bert-base-multilingual-cased`
(cerca de 700 MB) para calcular o BERTScore. Para pular essa métrica, use
`python -m src.evaluation.relatorio --sem-bertscore`. Nesse caso, as colunas do
BERTScore ficam vazias e o `metricas_automaticas.csv` deixa de bater com o do
TCC. Para restaurar o original, use `git checkout -- data/evaluation/`.

**Como conferir:** depois dos cinco comandos, `git status` não deve mostrar
mudanças nos CSVs. No `data/evaluation/resultados.md`, só a data de geração
muda. A coluna `integridade` da tabela "Tempo e métricas de cada manual
gerado" confere o SHA-256 de cada manual salvo com o registrado no momento em
que ele foi gerado. Ela deve mostrar `ok` em todas as linhas.

---

## 4. Caminho B: gerar os manuais de novo (com API)

Precisa do `.env` com `COHERE_API_KEY` (seção 2).

> **Atenção:** os comandos com as opções padrão **sobrescrevem** os manuais e
> as medições que foram usados no TCC. Para não perder os originais, use
> sempre uma pasta de saída separada, como nos exemplos abaixo. Se algo for
> sobrescrito por engano, recupere com `git checkout -- data/`.

### 4.1 Gerar um manual por método

```powershell
# Templating (não usa API; leva cerca de 5 ms)
python -m src.templating.generator --saida saida_banca/templating/manual.md

# RAG com Cohere: indexa os artefatos (Embed v4 + Chroma), recupera e gera com o Command R
python -m src.rag.pipeline --variante cohere --saida-dir saida_banca/rag

# Híbrido com Cohere: template Jinja2 + uma chamada ao Command R por seção
python -m src.hybrid.generator --variante cohere --saida-dir saida_banca/hybrid
```

Use sempre `--variante cohere`. Sem essa opção, os scripts tentam gerar também
a variante com Claude, que exige uma chave paga da Anthropic e não fez parte
do estudo.

O templating é determinístico, ou seja, gera sempre o mesmo texto. Para
conferir que ele é idêntico ao manual salvo, ignorando a diferença de fim de
linha do Windows:

```powershell
python -c "a=open('saida_banca/templating/manual.md','rb').read().replace(b'\r\n',b'\n'); b=open('data/evaluation/execucoes/templating/execucao_01.md','rb').read(); print('idêntico' if a==b else 'diferente')"
```

### 4.2 Benchmark de tempo (10 execuções por método)

Este foi o comando usado no TCC, aqui com uma pasta de saída separada:

```powershell
python -m src.evaluation.benchmark --repeticoes 10 --saida-dir saida_banca/benchmark
```

- Roda o templating, o RAG e o híbrido 10 vezes cada, sobre a mesma entrada.
  Cada execução é cronometrada com `time.perf_counter()`.
- Grava `tempos.csv` (cada execução), `tempos_resumo.csv` (mediana, mínimo,
  máximo e desvio-padrão) e os 30 manuais em `execucoes/`.
- Leva cerca de **1 hora**, porque o RAG leva cerca de 2 minutos por execução
  e o híbrido, cerca de 3. Entre as execuções há uma pausa de 3 s para
  respeitar o limite da API (opção `--pausa`).
- Para rodar um método só, use `--metodo rag` (a opção pode ser repetida).
  Para continuar uma medição interrompida, use `--a-partir-de N`.
- Se a cota da API acabar, o script para e mantém o que já foi medido.

Os tempos vão ser diferentes dos do TCC, porque dependem da rede e da carga
do servidor da Cohere. O que deve se repetir é a ordem de grandeza: o
templating leva milissegundos, o RAG cerca de 2 minutos e o híbrido cerca de
3 minutos, mais lento que o RAG. Outros dois resultados também devem se
repetir: o RAG muda a estrutura de seções entre as execuções e deixa artefatos
de fora, e o híbrido mantém sempre a estrutura do template.

### 4.3 LLM avaliadora (Cohere Command A)

```powershell
python -m src.evaluation.juiz_llm --execucoes
```

O script dá notas de 1 a 5 (clareza, coerência, completude, correção e
utilidade) a cada manual de `data/evaluation/execucoes/` e ao manual humano.
Uma avaliação que já existe para o mesmo arquivo, com o mesmo modelo, não é
refeita. Como as notas usadas no TCC já estão em
`data/evaluation/juiz_llm/execucoes/`, o comando só reaproveita essas notas.
Para pedir as notas de novo à API, apague essa pasta antes, o que gasta cerca
de 31 chamadas. Sem `--execucoes`, o script avalia só um manual por método,
os de `data/manuals_generated/`.

---

## 5. Onde está cada número do TCC

| Resultado no TCC | Arquivo | Comando que gera |
|---|---|---|
| Tempo (5 ms; 123,8 s; 197,4 s) e estabilidade (textos e estruturas distintos) | `data/evaluation/tempos_resumo.csv`, `variacao.csv` | `benchmark` (medição); `relatorio` (variação) |
| Tempo da redação manual (21,9 min) | `data/evaluation/tempo_manual.csv` | cronometrado à mão (seção 6) |
| Frases sustentadas e cobertura (100%, 46,9%, 50%) | `data/evaluation/fidelidade/resultado.csv` | `fidelidade analisar` |
| Concordância da reanotação (93,4%, κ = 0,641) | `data/evaluation/fidelidade/reanotacao/concordancia.csv` | `reanotacao concordancia` |
| Flesch, BERTScore e palavras | `data/evaluation/metricas_automaticas.csv` | `relatorio` |
| Vocabulário técnico | `data/evaluation/termos_tecnicos/resultado.csv` e `estatistica.csv` | `termos_tecnicos` |
| Notas da LLM avaliadora | `data/evaluation/juiz_llm/resultado_execucoes.csv` | `juiz_llm --execucoes` |
| Testes de Mann-Whitney, A12 e Holm (Apêndice A) | `data/evaluation/estatistica.csv` | `relatorio` |
| Figura do tempo de cada execução | `data/evaluation/fig5_tempo_execucoes.png` | `grafico_tempo` |

---

## 6. O que não sai de um comando

Três partes do estudo foram feitas à mão. Os registros delas estão no
repositório para conferência.

- **Manual humano** (`data/manuals_generated/manual/manual.md`): escrito pela
  autora a partir dos mesmos artefatos, com o tempo cronometrado e registrado
  em `data/evaluation/tempo_manual.csv`.
- **Anotação de fidelidade** (`data/evaluation/fidelidade/*.csv`): cada frase
  dos 4 manuais recebeu um rótulo: `S` (sustentada), `P` (parcial), `N` (não
  sustentada) ou `-` (sem conteúdo verificável). A coluna `artefatos` traz as
  chaves dos artefatos que sustentam a frase. A 1ª rodada foi feita por uma
  LLM, seguindo o guia `docs/evaluation/02_guia_fidelidade.md`. Para conferir
  um rótulo, compare a frase com `data/evaluation/fidelidade/artefatos_referencia.md`.
- **Reanotação** (`data/evaluation/fidelidade/reanotacao/`): a autora
  reanotou, sem ver a 1ª rodada, 20% das frases, sorteadas com semente fixa
  (`amostra.json`). O sorteio foi feito com
  `python -m src.evaluation.reanotacao sortear --fracao 0.2 --semente 2026`,
  que se recusa a rodar se a pasta já tiver planilhas. A anotação foi feita
  numa página gerada por `python -m src.evaluation.quiz_reanotacao gerar`, e
  as respostas voltaram às planilhas com
  `python -m src.evaluation.quiz_reanotacao importar respostas.json`.

O arquivo `data/raw/data.json` foi obtido da API REST do Jira Cloud com
`src/jira/extractor.py` (função `fetch_issues`, com paginação por
`nextPageToken`). Esse passo exige as variáveis `JIRA_*` e acesso ao projeto,
por isso o retorno já vem salvo no repositório.

---

## 7. Estrutura do repositório

```
data/
  raw/data.json            retorno do Jira (entrada)
  manuals_generated/       um manual por método (os avaliados)
  evaluation/              medições, anotações e resultados
docs/
  evaluation/              métricas, fontes e guia de anotação
  templating/, rag/, hybrid/
                           arquitetura e referências de cada método
src/
  common/schema.py         modelo padronizado dos artefatos
  jira/                    extração (API REST) e conversão ADF → Markdown
  templating/              método 1
  rag/                     método 2 (Cohere Embed v4 + Chroma + Command R)
  hybrid/                  método 3 (template + LLM por seção)
  evaluation/              benchmark, métricas, estatística e relatório
tests/                     testes automatizados (pytest)
```

As decisões de implementação e as fontes de cada técnica estão em
`docs/<método>/01_estrutura.md` e `02_referencias.md`. As métricas de
avaliação estão descritas em `docs/evaluation/01_estrutura.md`.
