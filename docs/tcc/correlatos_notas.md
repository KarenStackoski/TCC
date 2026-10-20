# Trabalhos correlatos — o que foi conferido (2026-10-19)

Apoio para `correlatos_relacao.tex`. Tudo o que o quadro e os parágrafos
afirmam sobre cada trabalho foi tirado das fontes abaixo, e não da
introdução.

## O que cada fonte diz

| Chave | Fonte consultada | Fatos usados |
|---|---|---|
| `yang2025` | arXiv 2504.08725v3 (ACL 2025) | Código Python: funções, métodos e classes. Agentes Reader, Searcher, Writer, Verifier e Orchestrator. Métricas: completude, utilidade (LLM como juiz, GPT-4o) e veracidade. 9 repositórios, 366 componentes. Veracidade de 95,74% na melhor configuração (DA-GPT, Tabela 3). Sem avaliação humana. |
| `jakupov2026` | Microsoft Tech Community e cópia do texto | Atualiza a documentação do código a cada pull request, com GitHub Actions. Vários agentes, GPT-4, Semantic Kernel e AutoGen. Fonte fraca: blog, sem métricas. |
| `medeiros2024` | PDF do CBA 2024, DOI 10.20906/CBA2024/4635 | Manual do VW Taos 2023. GPT-4 Turbo, LangChain, Milvus, FastAPI, Faster Whisper. Entrada por texto, áudio e imagem. 2 perguntas de teste. ROUGE-L, METEOR, BERTScore e tempo de resposta. |
| `perkusich2026` | arXiv 2602.08192 e página do XP 2026 | Questionário com 70 profissionais. 78% relatam ganho de produtividade, 81% saídas "quase corretas", 59% alucinações. |
| `gurgul2026` | arXiv 2603.16975 | Revisão da literatura e questionário com 65 desenvolvedores. Mais de 70% relatam que a IA ao menos reduziu à metade o tempo em tarefas repetitivas e de documentação. |

## Ajustes na introdução

1. **DocAgent (`yang2025`):** "95,74% de veracidade na geração de
   documentação técnica" está certo, mas o número vale para a melhor
   configuração e para documentação de componentes de código Python. Uma
   observação: na leitura automática do artigo, as contagens da Tabela 3
   pareciam não bater com a porcentagem. Se for destacar o número, confira
   a tabela no PDF.
2. **Medeiros et al. (`medeiros2024`):** a introdução diz que eles
   "validam o RAG como mecanismo eficaz de checagem de fatos". O artigo é
   um estudo de caso com 2 perguntas sobre um manual. Algo mais fiel
   seria: "demonstram, em estudo de caso, a viabilidade de RAG para
   simplificar consultas a manuais técnicos".
3. **"treinar a LLM com RAG"** (objetivos): o RAG não treina o modelo. Ele
   recupera os artefatos e os passa ao modelo junto com a pergunta.
4. **Opinião de profissionais e entrevistas com usuários** (objetivos e
   metodologia da introdução): saíram do estudo em 2026-10-18. Ajuste o
   texto ou mova esses itens para trabalhos futuros.
5. **"identificar, pela primeira vez"**: é uma afirmação forte para uma
   banca. "Contribuir para identificar" é mais seguro.

## Correções no .bib

- `yang2025`: o campo `journal` diz arXiv:2502.19411, mas o artigo é
  2504.08725 (o mesmo da `url`). Foi publicado na ACL 2025. Sugestão:
  ```bibtex
  @inproceedings{yang2025,
    author    = {Yang, Dayu and Simoulin, Antoine and Qian, Xin and Liu, Xiaoyi and Cao, Yuwei and Teng, Zhaopu and Yang, Grey},
    title     = {{DocAgent}: A Multi-Agent System for Automated Code Documentation Generation},
    booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)},
    year      = {2025},
    url       = {https://arxiv.org/abs/2504.08725},
    note      = {Acesso em: 19 out. 2026}
  }
  ```
  Antes de usar o `booktitle`, confira na ACL Anthology se o artigo saiu
  na trilha principal ou na de demonstrações. A página do arXiv só diz
  "ACL 2025".
- `perkusich2026`: o campo `journal = {INF/PUC-Rio}` está errado. É um
  capítulo da Springer, apresentado no XP 2026 (São Paulo); a `url` está
  certa. Use `@inproceedings` com `booktitle` = anais do XP 2026 e
  confira o volume da série na página da Springer (exige login).
- `medeiros2024`: acrescente `doi = {10.20906/CBA2024/4635}` e os demais
  autores (Hilton Machado, Gisliany Alves, Luís Tavares, Marianne Silva).
  Evento: XXV Congresso Brasileiro de Automática, 15 a 18 out. 2024. A
  `url` mudou para `https://ojs.sba.org.br/index.php/cba/article/view/4635`.
- `jakupov2026`: o post da Microsoft não mostrou a data nem os autores na
  consulta. O ano 2026 provavelmente está errado, porque o projeto é
  anterior. Abra o post e confira data e autoria.
- `Hou2023`: a `url` aponta para outro artigo (2507.13334). A correta é
  `https://arxiv.org/abs/2308.10620`.
- Nova entrada, citada no último parágrafo do `.tex`:
  ```bibtex
  @inproceedings{Maynez2020,
    author    = {Maynez, Joshua and Narayan, Shashi and Bohnet, Bernd and McDonald, Ryan},
    title     = {On Faithfulness and Factuality in Abstractive Summarization},
    booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
    pages     = {1906--1919},
    year      = {2020},
    doi       = {10.18653/v1/2020.acl-main.173}
  }
  ```

## Fontes

- DocAgent: https://arxiv.org/abs/2504.08725
- DocAider: https://techcommunity.microsoft.com/blog/educatordeveloperblog/docaider-automated-documentation-maintenance-for-open-source-github-repositories/4245588
- Medeiros et al.: https://ojs.sba.org.br/index.php/cba/article/view/4635
- Perkusich et al.: https://arxiv.org/abs/2602.08192 e https://conf.researchr.org/details/xp-2026/xp-2026-papers/2/Adoption-of-Large-Language-Models-in-Scrum-Management-Insights-from-Brazilian-Practi
- Gurgul et al.: https://arxiv.org/abs/2603.16975
