# Reanotação da fidelidade — o que fazer

## O que é

A 1ª rodada da anotação de fidelidade (as 296 frases em
`data/evaluation/fidelidade/*.csv`) foi feita pelo Claude. Aqui você anota
de novo uma amostra dessas frases, **sem ver os rótulos do Claude**. Depois
o script compara as duas anotações.

**Para que serve:** mostrar que a anotação da IA é confiável. Se você,
seguindo o mesmo guia, chega aos mesmos rótulos na maioria das frases, a
1ª rodada pode ser usada no TCC. Se discordar muito, ela não pode ser
usada como está.

## O que tem nesta pasta

| Arquivo | Conteúdo |
|---|---|
| `rag.csv` | 6 frases |
| `manual.csv` | 11 frases |
| `hibrido.csv` | 10 frases |
| `templating.csv` | 34 frases |
| `amostra.json` | registro do sorteio (semente 2026, 20% de cada manual, 2026-10-19) |

Total: 61 frases, sorteadas ao acaso. A data `reanotar_a_partir_de` do
`amostra.json` pode ser ignorada: a espera de 7 dias só vale quando a
mesma pessoa faz as duas rodadas.

## Passo a passo

1. **Não abra** as planilhas da 1ª rodada (`data/evaluation/fidelidade/rag.csv`
   etc., a pasta de cima) até terminar. Se abrir, os rótulos do Claude
   influenciam os seus e a comparação perde o valor.
2. Releia as seções 3 e 4 do guia: `docs/evaluation/02_guia_fidelidade.md`.
3. Abra cada CSV **desta pasta** e preencha a coluna `rotulo` de cada
   frase, consultando `data/evaluation/fidelidade/artefatos_referencia.md`:
   - `S`: tudo o que a frase diz está nos artefatos (mesmo com outras palavras);
   - `P`: só uma parte está, ou uma parte contradiz algum artefato;
   - `N`: o conteúdo principal não está nos artefatos ou os contradiz;
   - `-`: não há o que verificar (título, transição, rótulo como "Passo a passo:").

   As colunas `artefatos` e `observacao` são opcionais. Na dúvida entre
   dois rótulos, escolha o mais severo e escreva "dúvida" em `observacao`.
4. Salve como **CSV UTF-8**, com o mesmo nome e as mesmas colunas. No Excel
   em português, importe por **Dados > De Texto/CSV**, com o delimitador
   **vírgula**, ou use o LibreOffice.
5. Na raiz do projeto, rode:
   ```
   python -m src.evaluation.reanotacao concordancia
   python -m src.evaluation.relatorio
   ```

Tempo estimado: de 30 a 40 minutos. As frases do templating são cópia
direta dos artefatos e vão rápido.

## Como ler o resultado

Sai em `concordancia.csv` (nesta pasta) e numa seção nova do
`data/evaluation/resultados.md`:

- **concordancia_%:** em quantas frases você e o Claude deram o mesmo rótulo.
- **kappa:** kappa de Cohen, a concordância descontando a que aconteceria
  por acaso. Faixas de Landis e Koch (1977): até 0,20 leve; até 0,40
  razoável; até 0,60 moderada; até 0,80 substancial; acima de 0,80 quase
  perfeita.
- **discordancias:** onde vocês divergiram. `S→P (2)` = 2 frases em que o
  Claude marcou `S` e você marcou `P`. O primeiro rótulo é o da 1ª rodada.

Ressalvas para o texto do TCC:
- Se quase todas as frases de um método tiverem o mesmo rótulo (o
  templating deve ser quase só `S`), o kappa desse método fica instável
  ou "indefinido". Nesse caso, dê mais peso à % de concordância e ao
  kappa total.
- Concordância não é o mesmo que correção: vocês dois podem errar do
  mesmo jeito. Comente no texto as frases em que discordaram.

## Depois

Agora sim pode abrir a 1ª rodada. Revise as frases em que discordaram e
decida o rótulo final. Se mudar algum rótulo da 1ª rodada, registre a
mudança (o que mudou e por quê) e rode de novo
`python -m src.evaluation.fidelidade analisar` e
`python -m src.evaluation.relatorio`.
