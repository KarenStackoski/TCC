# Onde paramos (atualizado em 2026-10-19)

Resumo do que foi feito na sessão de 19/10, do que falta, e das mudanças e
dos cuidados para o texto do TCC. Para retomar, peça ao Claude: **"me
relembre onde paramos"**.

---

## 1. O que já está feito

- **Medições:** tempo, tokens, métricas de texto, BERTScore, variação,
  juiz LLM e estatística (Mann-Whitney, A12 e Holm), todas em
  `data/evaluation/resultados.md`.
- **Fidelidade, 1ª rodada:** feita pelo Claude (Opus 5.5) nas 296 frases.
  - Frases sustentadas: templating, RAG e híbrido 100%; manual humano 98,1%
    (1 frase `P`, id 18).
  - Cobertura de conteúdo: templating e híbrido 100%; manual humano 50%;
    RAG 46,9%.
- **Amostra da reanotação sorteada:** 61 frases em
  `data/evaluation/fidelidade/reanotacao/`, com um README próprio.
- **Referências da Etapa 4 conferidas:** seção 11 de
  `docs/evaluation/01_estrutura.md`.
- **Correlatos lidos nas fontes:** DocAgent, DocAider, Medeiros, Perkusich e
  Gurgul. Notas em `docs/tcc/correlatos_notas.md`.
- **Atenção: ainda não houve commit** desta sessão. As planilhas anotadas, os
  docs, os READMEs e a pasta `reanotacao/` estão só na cópia local.

---

## 2. O que falta fazer (em ordem)

1. [ ] **Commit** do trabalho de 19/10 (pedir ao Claude ou fazer à mão).
2. [ ] **Reanotar as 61 frases**: siga
   `data/evaluation/fidelidade/reanotacao/README.md`. Não abra as planilhas
   da 1ª rodada antes de terminar. Leva de 30 a 40 min. Depois rode:
   ```
   python -m src.evaluation.reanotacao concordancia
   python -m src.evaluation.relatorio
   ```
3. [ ] Revisar as frases em que você e o Claude discordaram e decidir o
   rótulo final.
4. [ ] Ajustar a **introdução** (seção 3 abaixo).
5. [ ] Corrigir o **.bib** (seção 4).
6. [ ] Escrever **Resultados e Discussão** relacionando com os correlatos
   (seção 5).
7. [ ] Escrever as **ameaças à validade** (seção 6).
8. [ ] Conferir as pendências de referência (seção 7).
9. [ ] Decidir se `docs/tcc/correlatos_relacao.tex` fica. É um quadro
   comparativo feito antes de entender o pedido; não era o que você queria.
   Use ou apague.

---

## 3. Mudanças na introdução

| Trecho atual | Problema | Sugestão |
|---|---|---|
| "pretende-se **treinar** a LLM com RAG e artefatos" | O RAG não treina o modelo; recupera os artefatos e os passa no prompt. | "fundamentar as respostas da LLM nos artefatos de DevOps por meio de RAG" |
| "comparar os quatro métodos [...] quanto a qualidade, tempo, complexidade e **opinião de profissionais**" | A pesquisa com pessoas saiu do estudo em 18/10. | "[...] quanto a tempo de geração, fidelidade às fontes, cobertura, legibilidade, estrutura e estabilidade entre execuções" |
| "será coletada a percepção de profissionais [...] além de **entrevistas com usuários** sem experiência" | Não foi feito. | Retirar, ou mover para **trabalhos futuros** |
| "artefatos **reais** [...] extraídos de uma plataforma de DevOps" | Os 32 artefatos parecem de um projeto montado para o estudo ("Lanchonete do Zé", todos em "Tarefas pendentes"). | Se forem fictícios: "artefatos de um projeto construído para o estudo, no formato real do Jira". Se forem reais, explique de onde vieram. |
| Medeiros et al. "**validam** o RAG como mecanismo eficaz de checagem de fatos" | É um estudo de caso com 2 perguntas sobre 1 manual, avaliado só por semelhança textual. | "demonstram, em estudo de caso, a viabilidade de RAG para simplificar consultas a manuais técnicos" |
| "identificar, **pela primeira vez**, qual combinação [...] produz documentação de **maior qualidade**" | Afirmação forte, e "qualidade para o usuário" não foi medida. | "contribuir para identificar qual combinação [...] oferece melhor equilíbrio entre fidelidade, cobertura e custo de tempo" |
| DocAgent "atinge 95,74% de veracidade na geração de documentação técnica" | Está certo, mas vale só para a melhor configuração e para componentes de código Python. | Acrescentar "na melhor configuração, ao documentar funções e classes Python". Antes de destacar o número, confira a Tabela 3 no PDF. |

**Regra geral:** o estudo **não mede qualidade para o usuário**. Ele mede se
o texto é fiel às fontes, se está completo, quanto custa gerar e se é
estável. As conclusões não podem passar disso.

---

## 4. Correções no .bib

- `yang2025`: o `journal` diz arXiv:2502.19411; o correto é 2504.08725.
  Saiu na ACL 2025 (confira se foi na trilha principal ou na de demos). A
  entrada pronta está em `docs/tcc/correlatos_notas.md`.
- `perkusich2026`: o `journal = {INF/PUC-Rio}` está errado. É um capítulo
  da Springer do XP 2026 (São Paulo); arXiv 2602.08192.
- `medeiros2024`: acrescentar `doi = {10.20906/CBA2024/4635}`, os autores
  que faltam (Machado, Alves, Tavares, M. Silva) e a URL nova
  (`ojs.sba.org.br/index.php/cba/article/view/4635`).
- `jakupov2026`: o ano 2026 provavelmente está errado. Abra o post da
  Microsoft e confira data e autores.
- `Hou2023`: a `url` aponta para outro artigo. A correta é
  `https://arxiv.org/abs/2308.10620`.
- Novas entradas, se forem citadas no texto: `Maynez2020` (está em
  `correlatos_notas.md`) e as da seção 11 de
  `docs/evaluation/01_estrutura.md` (Mann-Whitney, Holm, Vargha-Delaney,
  Arcuri-Briand, Cohen, Landis-Koch, Martins 1996, Zhang/BERTScore etc.).

---

## 5. Como relacionar seus resultados com os correlatos

**Como cada um avaliou:**

| Trabalho | Como avaliou | O que concluiu |
|---|---|---|
| Medeiros et al. (2024) | 1 manual (VW Taos), 2 perguntas. ROUGE-L, METEOR, BERTScore, WMD contra respostas de referência; tempo médio da API | BERTScore F1 de 0,91 e 0,88; geração em 6,70 s em média, variando com a API da OpenAI. Chamam as respostas de "confiáveis" só pela semelhança. |
| DocAgent (Yang et al., 2025) | 366 componentes de 9 repositórios Python. Completude, utilidade (GPT-4o como juiz) e veracidade (entidades citadas existem no código). Sem avaliação humana. | Veracidade de 95,74% contra 61,10% do GPT sozinho. A ablação mostra que o contexto estruturado importa. |
| Perkusich et al. (2026) | Questionário com 70 profissionais; porcentagens | 78% ganho de produtividade; 81% saídas "quase corretas"; 59% alucinações |
| Gurgul et al. (2026) | Revisão da literatura e questionário com 65 desenvolvedores | Mais de 70%: a IA reduziu ao menos à metade o tempo de documentação |

**Pontos de diálogo (um parágrafo depois de cada métrica nos Resultados):**

1. **Tempo.** Manual humano 21,9 min; RAG 123,8 s (cerca de 91% menos);
   híbrido 197,4 s (cerca de 85% menos); templating 0,005 s.
   - Confirma o "reduz à metade" de Gurgul, só que **medido** (10 execuções
     e teste estatístico) e não relatado em questionário.
   - Mesma explicação do Medeiros para a variação: quase todo o tempo é
     espera pela API.
   - Limites: o tempo humano é uma medição só, feita pela autora, e o
     tempo de revisar os textos gerados não foi medido.
2. **BERTScore.** O RAG teve o menor BERTScore (0,79) e a menor cobertura
   (46,9%), mas 100% das frases sustentadas: ele **omitiu, não inventou**.
   A avaliação por semelhança do Medeiros não distingue errado de
   incompleto, e isso justifica a sua anotação de fidelidade e cobertura.
   Os valores não se comparam diretamente (respostas curtas × manual
   inteiro, BERT inglês × multilíngue).
3. **Fidelidade × DocAgent.** Nos dois estudos, a fonte estruturada evita
   invenção: lá o contexto levou a veracidade de 61% para 96%; aqui, o RAG
   e o template levaram a quase 100% de frases sustentadas. O template
   ainda elevou a cobertura de 46,9% (RAG) para 100% (híbrido), o que é
   paralelo à ablação deles. Diferença de método: a veracidade deles é
   automática; a sua é anotada frase a frase, com erro intrínseco e
   extrínseco.
4. **Juiz LLM.** Mesma limitação do DocAgent (sem validação humana). Você
   tem uma evidência a mais: o juiz apontou de 2 a 10 "afirmações não
   sustentadas" onde a anotação não achou nenhuma, e um caso do manual
   humano se contradiz. O juiz sozinho não mede correção.
5. **"Quase corretas" (Perkusich).** Aqui o risco das LLMs apareceu como
   **omissão e instabilidade**, não como invenção: o RAG teve 4 estruturas
   diferentes em 10 execuções (similaridade mínima de 0,28) e o híbrido 10
   textos diferentes. O template resolve a parte estrutural.

**Frase-síntese para a conclusão:** os métodos com LLM não inventaram
conteúdo, mas omitiram e variaram entre execuções; o template corrigiu a
cobertura e a estrutura, e o híbrido combinou cobertura total com texto
reescrito, a um custo de tempo de cerca de 3 minutos.

*Os pontos 2, 3 e 5 dependem da fidelidade: confirme os números depois da
reanotação.*

---

## 6. Validade da pesquisa: pontos de atenção

**O desenho é válido.** Em vários pontos é mais rigoroso que os correlatos:
mais repetições, estatística, comparação entre 4 métodos sobre a mesma
entrada, fidelidade frase a frase e rastreabilidade por SHA-256. O DocAgent
(ACL 2025) usa o mesmo desenho, com métricas automáticas e LLM como juiz,
sem pessoas, e serve de precedente.

**O que declarar nas ameaças à validade:**

- **Construto:** não há avaliação com usuários, então nada mede se o manual
  ajuda quem o usa. As conclusões ficam em fidelidade, cobertura, custo e
  estabilidade.
- **Fidelidade com efeito teto:** cerca de 100% em todos os métodos (os
  artefatos são curtos e limpos, e o templating copia a fonte). A métrica
  não separa os métodos; a cobertura e a variação separam. Diga isso, em
  vez de apresentar a fidelidade como vitória de todos.
- **Anotação por LLM:** a 1ª rodada foi feita pelo Claude. O kappa da sua
  reanotação é o que valida isso, então não feche o texto sem ele.
- **Viés da autora:** você escreveu o manual humano, que também é a
  referência do BERTScore, e é anotadora. Já está em `01_estrutura.md`,
  seção 9.
- **Externa:** um único projeto (32 artefatos, possivelmente fictício) e um
  único provedor (Cohere). Não generaliza.
- **Conclusão:** n = 10 por método (limite da API gratuita), 1 manual
  anotado por método e 1 medição do tempo humano (trate como estimativa).

---

## 7. Referências ainda a conferir

- Vargha e Delaney (2000): os limiares do A12 (0,56 / 0,64 / 0,71) só foram
  vistos em fontes secundárias, porque o artigo é pago.
- Ji et al. (2023): confirmar o número de artigo (248) na ACM Digital
  Library.
- DocAgent: conferir a Tabela 3 no PDF, onde as contagens pareciam não
  bater com os 95,74%.
- DocAider: data e autores do post.

---

## 8. Arquivos úteis

| Arquivo | Conteúdo |
|---|---|
| `data/evaluation/resultados.md` | todos os números |
| `data/evaluation/fidelidade/reanotacao/README.md` | passo a passo da reanotação |
| `docs/evaluation/01_estrutura.md` | métricas, fontes, ameaças à validade, referências conferidas (seção 11) |
| `docs/evaluation/02_guia_fidelidade.md` | regras de anotação |
| `docs/tcc/correlatos_notas.md` | fatos conferidos de cada correlato e entradas do .bib |
| `docs/PROGRESSO.md` | histórico das sessões |
