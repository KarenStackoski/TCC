# Guia de anotação de fidelidade

Este guia é o manual de codificação da anotação de fidelidade (seção 4 de
`01_estrutura.md`). Ele existe para que as quatro planilhas sejam anotadas
com os mesmos critérios. Leia tudo antes de começar. Decida as regras
marcadas com **[decisão]** antes da primeira frase e não mude no meio.
Se precisar mudar, reanote o que já fez.

Registrar as regras de anotação junto com o resultado é uma das boas
práticas de van der Lee et al. (2021). A distinção entre alucinação
intrínseca e extrínseca é de Maynez et al. (2020) e Ji et al. (2023).

## 1. Arquivos

| Arquivo | Para quê |
|---|---|
| `data/evaluation/fidelidade/templating.csv` | 197 frases (166 a anotar) |
| `data/evaluation/fidelidade/rag.csv` | 41 frases (30 a anotar) |
| `data/evaluation/fidelidade/hibrido.csv` | 74 frases (46 a anotar) |
| `data/evaluation/fidelidade/manual.csv` | 68 frases (54 a anotar) |
| `data/evaluation/fidelidade/artefatos_referencia.md` | os 32 artefatos por extenso, para consultar |

As frases são exatamente as mesmas que as métricas de texto usam. Se você
abrir no Excel em português e tudo aparecer numa coluna só, use **Dados >
De Texto/CSV** com o delimitador **vírgula**, ou abra no LibreOffice. Salve
de volta como **CSV UTF-8**, com o mesmo nome e as mesmas colunas.

## 2. Colunas

| Coluna | Quem preenche | Conteúdo |
|---|---|---|
| `id` | já vem | número da frase; não mude |
| `secao` | já vem | onde a frase está no manual, para dar contexto |
| `frase` | já vem | o texto a julgar; não edite |
| `rotulo` | **você** | `S`, `P`, `N` ou `-` (seção 3) |
| `artefatos` | **você** | as chaves que sustentam a frase: `SCRUM-18, SCRUM-26` |
| `fonte_declarada` | já vem | pista: a fonte que o próprio texto declara (seção 5) |
| `observacao` | **você** | para `N` e `P`: `intrinseca` ou `extrinseca`, e um comentário curto |

Os títulos, os itens de sumário e a linha "Documento gerado
automaticamente…" já vêm com `-` e com a observação "pré-preenchido".
Confira esses rótulos e troque algum se ele estiver errado. Enquanto só
houver pré-preenchimento, `python -m src.evaluation.fidelidade preparar`
pode refazer a planilha. Depois da primeira anotação sua, ele não mexe
mais nela.

## 3. Rótulos

Julgue cada frase **só pelos 32 artefatos**. O que você sabe sobre apps de
delivery, ou o que "parece óbvio", não conta.

- **S, sustentada:** tudo o que a frase afirma está nos artefatos, mesmo
  que com outras palavras. Resumir ou reordenar não tira o S.
- **P, parcialmente sustentada:** uma parte está nos artefatos e outra
  parte não está ou contradiz algo. Exemplo: "o QR Code vale 10 minutos e
  pode ser pago com cartão" (só a primeira parte tem apoio).
- **N, não sustentada:** o conteúdo principal da frase não está nos
  artefatos ou os contradiz.
- **`-`, sem conteúdo verificável:** títulos, transições ("Nesta seção você
  verá…"), saudações, instruções de leitura do próprio manual.

Para `N` e `P`, escreva em `observacao` o tipo do erro:
- `intrinseca`: **contradiz** um artefato (número errado, regra invertida).
  Em `artefatos`, coloque a chave contradita.
- `extrinseca`: **acrescenta** algo que não está em nenhum artefato, mesmo
  que seja plausível ou verdadeiro no mundo real. Deixe `artefatos` vazio
  para a parte sem apoio.

## 4. Regras de decisão

1. **Status dos artefatos [decisão].** Os 32 artefatos estão todos em
   "Tarefas pendentes". Regra sugerida: tratar o conjunto como a
   especificação do sistema. Uma frase que descreve uma história ou épico
   como funcionalidade existente é `S`. Sem essa regra, quase tudo seria
   `N`, e a métrica não diferenciaria os métodos.
2. **Melhorias, IMP-01 a IMP-04 (SCRUM-30 a 33) [decisão].** Elas
   descrevem o estado atual ("o app atualmente só suporta tema claro") e
   uma mudança proposta. Regra sugerida:
   - a frase apresenta a melhoria como planejada ou futura → `S`;
   - a frase diz que o app **já tem** a melhoria → `P` com `intrinseca`
     (o conteúdo existe, mas contradiz o "atualmente" do artefato);
   - a frase descreve o estado atual ("o app só tem tema claro") → `S`.
3. **Bugs, BUG-01 a BUG-07.**
   - a frase apresenta o bug como problema conhecido → `S`;
   - a frase descreve o comportamento correto que o bug quebra, e esse
     comportamento está numa história (ex.: a posição do entregador é
     atualizada, US-13) → `S`, com a chave da história. Anote o conflito em
     `observacao` ("contradito por BUG-06");
   - a frase diz que o bug foi corrigido ou não existe → `N`, `intrinseca`.
4. **Números, prazos e limites** (30 minutos, 8 caracteres, 300
   caracteres, 10 segundos): um número diferente do artefato é erro
   `intrinseca`. A frase fica `N` se o número é o conteúdo principal dela e
   `P` se é um detalhe entre outros corretos.
5. **Detalhes de interface que não estão nos artefatos** (nome de botão,
   ícone, "toque em Confirmar", "nas configurações do app"): `extrinseca`.
   A frase fica `P` se o resto dela tem apoio, ou `N` se for só isso.
6. **Generalizações.** "O app aceita várias formas de pagamento" é `S` se o
   EP-04 e as histórias de pagamento sustentam. "Todas as formas de
   pagamento" também é `S`, porque o EP-04 diz isso. Uma generalização que
   vai além dos artefatos ("pagamento em qualquer moeda") é `extrinseca`.
7. **Duas ideias numa frase.** Às vezes o divisor junta dois itens de lista
   numa frase só. Julgue a frase inteira: tudo com apoio → `S`; uma parte
   sem apoio → `P`.
8. **Na dúvida entre dois rótulos,** escolha o mais severo (`S` × `P` → `P`;
   `P` × `N` → `N`) e escreva "dúvida" em `observacao`. Isso permite contar
   depois quantas frases foram decididas assim.

## 5. A coluna `artefatos` e a pista `fonte_declarada`

- Em `artefatos`, coloque **todas** as chaves que sustentam a frase,
  preferindo a mais específica: a história (US) em vez do épico (EP),
  quando a frase trata de um detalhe da história. A cobertura de conteúdo
  é calculada a partir desta coluna. Se você puser só o épico, a
  cobertura das histórias fica subestimada.
- `fonte_declarada` traz o que o texto declara como fonte. São três
  casos: a chave ou o código citado na frase ou no título da seção
  (`US-12 — …`), o nome de um artefato citado na frase, e as fontes que o
  Command R declarou nas citações (RAG e híbrido). É **só uma pista**:
  - nos métodos 2 e 3, a citação é a afirmação do próprio modelo. Conferir
    se ela está certa é justamente o que a anotação mede. Não copie sem
    verificar no `artefatos_referencia.md`;
  - no templating, a pista é quase sempre a história da seção, e
    costuma estar certa;
  - no manual humano, quase não há pista, porque o texto não cita códigos.
- Risco a registrar no TCC: a pista pode ancorar a anotação, ou seja,
  levar a aceitar a fonte sugerida sem procurar outra. Ela existe para
  reduzir o tempo de busca. A decisão de `rotulo` e `artefatos` continua
  sendo sua.

## 6. Como proceder

1. Leia o `artefatos_referencia.md` inteiro uma vez antes de começar.
2. Anote um método por sessão, na ordem **rag → manual → hibrido →
   templating**. Os dois textos mais livres vêm primeiro, enquanto as
   regras ainda estão frescas. O templating, que copia os artefatos,
   fica por último e é rápido.
3. Tempo estimado: cerca de 300 frases a anotar. A 20–40 s por frase, são
   2 a 3 horas no total. Registre o tempo gasto, se quiser relatá-lo.
4. Ao terminar, rode `python -m src.evaluation.fidelidade analisar` e
   depois `python -m src.evaluation.relatorio`.

## 7. Quem anotou e limitações a declarar no TCC

**Primeira rodada (2026-10-19):** feita pelo Claude (modelo Opus 5.5,
`claude-opus-5-5`), a pedido da autora, com este guia. Decisões adotadas:
as regras sugeridas nas regras 1 e 2 da seção 4. Resultado: só uma frase
fora de `S` (manual humano, id 18: `P`, extrínseca, "dúvida"). Além do
pré-preenchido, ficaram com `-` os rótulos do template ("Passo a passo:"),
o cabeçalho da tabela de bugs do templating e "Particularidades:" do
manual humano. As frases que descrevem um comportamento quebrado por um
bug levam a observação "contradito por BUG-0X" (regra 3).

- **A primeira rodada é de uma LLM.** Ela pode ser leniente com textos
  gerados por outra LLM. A amostra reanotada pela autora (seção 8) mede
  isso.
- **A autora também escreveu o manual humano e o estudo.** Ela sabe qual
  método gerou cada texto, então a reanotação não é cega quanto ao método.
- A pista `fonte_declarada` pode ancorar a anotação (seção 5).
- A anotação cobre 1 manual por método, e não as 10 execuções.

## 8. Reanotação (concordância entre anotadores)

A primeira rodada foi feita pelo Claude (seção 7). A autora anota de novo
uma amostra das frases, sem olhar a primeira rodada, e as duas são
comparadas. Como a autora não fez a primeira rodada, não há memória dela
a esquecer: **o intervalo de 7 dias do passo 3 não se aplica**, e a data
`reanotar_a_partir_de` do `amostra.json` pode ser ignorada. A regra que
continua valendo é não abrir as planilhas da primeira rodada antes de
terminar a reanotação.

O sorteio foi feito em 2026-10-19 (semente 2026): hibrido 10, manual 11,
rag 6, templating 34 frases (61 no total).

1. **Termine a primeira rodada** das quatro planilhas. O sorteio se recusa
   a rodar antes disso. Assim, você não sabe quais frases vão ser
   reanotadas enquanto faz a primeira anotação, e não dá para caprichar
   mais nelas.
2. **Sorteie a amostra:**
   ```
   python -m src.evaluation.reanotacao sortear --fracao 0.2 --semente 2026
   ```
   - São 20% das frases que você anotou em cada manual, arredondando
     para cima. As pré-preenchidas ficam de fora. A amostra é
     estratificada por método, ou seja, cada manual contribui na mesma
     proporção.
   - Cria `data/evaluation/fidelidade/reanotacao/<metodo>.csv`, com as
     frases na ordem do manual e sem rótulo, e o `amostra.json`, com a
     semente, os ids sorteados e a data a partir da qual reanotar.
   - Com cerca de 300 frases anotadas, a amostra fica com cerca de 60.
3. **Espere pelo menos 7 dias** (a data está no `amostra.json`). Não abra
   as planilhas da reanotação antes disso.
4. **Reanote** só `rotulo` (e, se quiser, `artefatos` e `observacao`)
   seguindo este mesmo guia, **sem abrir a primeira rodada**.
5. **Calcule a concordância:**
   ```
   python -m src.evaluation.reanotacao concordancia
   python -m src.evaluation.relatorio
   ```
   O resultado sai em `reanotacao/concordancia.csv` e numa seção própria
   do `resultados.md`: concordância simples (%), kappa de Cohen e as
   discordâncias por tipo (ex.: `S→P (2)`), por método e no total.

**Kappa de Cohen:** κ = (p_o − p_e) / (1 − p_e). p_o é a concordância
observada e p_e é a concordância esperada ao acaso, calculada pelas
proporções de cada rótulo nas duas rodadas. Fonte: Cohen, J. "A
Coefficient of Agreement for Nominal Scales". Educational and
Psychological Measurement, v. 20, n. 1, 1960. Faixas de interpretação:
< 0 pobre; 0–0,20 leve; 0,21–0,40 razoável; 0,41–0,60 moderada;
0,61–0,80 substancial; 0,81–1 quase perfeita. Fonte: Landis, J. R.;
Koch, G. G. "The Measurement of Observer Agreement for Categorical Data".
Biometrics, v. 33, n. 1, 1977.

**Ressalvas para o texto:**
- O kappa mede a concordância entre a LLM e a autora, não a
  **correção**: os dois podem errar do mesmo jeito. As frases em que
  discordarem devem ser discutidas no texto.
- Se um método tiver quase todas as frases com o mesmo rótulo (o
  templating deve ter quase só `S`), o kappa dele fica instável ou
  indefinido: com p_e perto de 1, qualquer discordância derruba o kappa.
  Nesse caso, reporte a concordância simples ao lado e dê mais peso ao
  kappa total.
- Se o kappa sair baixo, olhe as discordâncias. Por exemplo, muitas `S→P`
  podem indicar que a regra de "detalhe de interface" (seção 4, regra 5)
  ficou ambígua.
