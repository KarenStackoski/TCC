# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

### Autenticação e Cadastro
O EP-01 abrange todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

### Catálogo de Restaurantes
O EP-02 permite a exibição, busca e filtragem de restaurantes e seus cardápios, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

### Carrinho e Pedidos
O EP-03 cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido, sendo o núcleo do app onde a conversão de interesse em compra acontece.

### Pagamentos
O EP-04 é responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

### Rastreamento de Entrega
O EP-05 oferece funcionalidades que permitem ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

### Avaliações
O EP-06 permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Login e Cadastro

- O usuário pode fazer login com sua conta Google ou criar uma conta com e-mail e senha.
- O cadastro exige nome completo, e-mail e senha, com validação de formato e requisitos mínimos.
- O login com Google usa o fluxo OAuth e cria uma conta automaticamente no primeiro acesso.

### Pagamentos

- O usuário pode pagar com cartão de crédito, inserindo os dados em um formulário seguro.
- O pagamento com Pix gera um QR Code válido por 10 minutos, com opção de código copia-e-cola.

### Acompanhamento de Pedidos

- O usuário pode acompanhar o status do pedido em tempo real, com notificações push e linha do tempo visual.
- O rastreamento do entregador no mapa mostra a posição atual, o trajeto estimado e o tempo restante.

### Avaliação e Cancelamento

- O usuário pode avaliar o restaurante após a entrega, atribuindo de 1 a 5 estrelas e adicionando um comentário.
- O cancelamento de pedido é possível antes da confirmação pelo restaurante, com estorno automático.

### Cupons e Carrinho

- O usuário pode aplicar um cupom de desconto, com validação em tempo real e exibição destacada.
- O carrinho permite adicionar itens, com opções de personalização e alerta para misturar restaurantes.

### Busca e Filtro

- O usuário pode buscar restaurantes por nome, com resultados em tempo real e sugestões amigáveis.
- O filtro por categoria permite selecionar múltiplas categorias e combina com busca por nome.

### Visualização de Cardápio

- O usuário pode visualizar o cardápio completo de um restaurante, organizado por seções.
- Cada item exibe nome, foto, descrição e preço, com indicação de indisponibilidade.

## Tarefas Operacionais

### Modo escuro

O app atualmente só suporta tema claro, mas a melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar último endereço de entrega automaticamente

Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido, mas a melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar. Endereços frequentes podem ser salvos como favoritos ("Casa", "Trabalho") acessíveis diretamente na tela de entrega.

### Mensagem de erro sem conexão com internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente via listener de rede e exibir uma tela amigável com ícone, mensagem clara ("Sem conexão com a internet") e botão "Tentar novamente", sem aguardar o timeout da requisição.

### Skeleton loading nas telas de lista

Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### Problemas com o Cupom

BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes): ao inserir um código de cupom inválido, a API retorna um erro 500 em vez de um erro 422 com mensagem adequada. O app exibe uma mensagem genérica de erro.

### Problemas de Rastreamento

BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes): a posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### Problemas de Autenticação

BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes): ao tentar autenticar com Google em dispositivos Android 10, o app exibe uma mensagem de erro sem detalhes. Suspeita-se de incompatibilidade com o Custom Tab usado no redirecionamento.

### Problemas de Notificação

BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes): as notificações push de mudança de status do pedido estão chegando com atraso de 5 minutos após a mudança real de status. O job de envio de notificações roda em intervalo fixo de 5 minutos em vez de ser disparado por evento.

### Problemas de Checkout

BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes): na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto.

### Problemas de Filtro

BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes): quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado.

### Problemas de Estabilidade

BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes): ao tentar adicionar um item sem foto ao carrinho, o aplicativo para de responder e exibe uma tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula.


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "EP-01" — fonte(s): SCRUM-1
- "todas as funcionalidades relacionadas ao acesso do usuário à plataforma" — fonte(s): SCRUM-1
- "criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "EP-02" — fonte(s): SCRUM-2
- "exibição, busca e filtragem de restaurantes e seus cardápios" — fonte(s): SCRUM-2
- "informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "EP-03" — fonte(s): SCRUM-3
- "todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido" — fonte(s): SCRUM-3
- "núcleo do app onde a conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "EP-04" — fonte(s): SCRUM-4
- "todas as formas de pagamento disponíveis na plataforma" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "EP-05" — fonte(s): SCRUM-5
- "usuário acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "EP-06" — fonte(s): SCRUM-6
- "usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Login e Cadastro" — fonte(s): SCRUM-8, SCRUM-7
- "fazer login com sua conta Google" — fonte(s): SCRUM-8
- "criar uma conta com e-mail e senha." — fonte(s): SCRUM-7
- "cadastro exige nome completo, e-mail e senha" — fonte(s): SCRUM-7
- "validação de formato e requisitos mínimos." — fonte(s): SCRUM-7
- "login com Google usa o fluxo OAuth" — fonte(s): SCRUM-8
- "cria uma conta automaticamente no primeiro acesso." — fonte(s): SCRUM-8
- "Pagamentos" — fonte(s): SCRUM-18, SCRUM-17
- "pagar com cartão de crédito" — fonte(s): SCRUM-17
- "inserindo os dados em um formulário seguro." — fonte(s): SCRUM-17
- "pagamento com Pix gera um QR Code válido por 10 minutos" — fonte(s): SCRUM-18
- "opção de código copia-e-cola." — fonte(s): SCRUM-18
- "Acompanhamento de Pedidos" — fonte(s): SCRUM-15
- "acompanhar o status do pedido em tempo real" — fonte(s): SCRUM-15
- "notificações push" — fonte(s): SCRUM-15
- "linha do tempo visual." — fonte(s): SCRUM-15
- "rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "posição atual" — fonte(s): SCRUM-19
- "trajeto estimado" — fonte(s): SCRUM-19
- "tempo restante." — fonte(s): SCRUM-19
- "Avaliação e Cancelamento" — fonte(s): SCRUM-21, SCRUM-16
- "avaliar o restaurante após a entrega" — fonte(s): SCRUM-21
- "atribuindo de 1 a 5 estrelas" — fonte(s): SCRUM-21
- "adicionando um comentário." — fonte(s): SCRUM-21
- "cancelamento de pedido é possível antes da confirmação pelo restaurante" — fonte(s): SCRUM-16
- "estorno automático." — fonte(s): SCRUM-16
- "Cupons e Carrinho" — fonte(s): SCRUM-14, SCRUM-13
- "aplicar um cupom de desconto" — fonte(s): SCRUM-14
- "validação em tempo real" — fonte(s): SCRUM-14
- "exibição destacada." — fonte(s): SCRUM-14
- "carrinho permite adicionar itens" — fonte(s): SCRUM-13
- "opções de personalização" — fonte(s): SCRUM-13
- "alerta para misturar restaurantes." — fonte(s): SCRUM-13
- "Busca e Filtro" — fonte(s): SCRUM-11, SCRUM-10
- "buscar restaurantes por nome" — fonte(s): SCRUM-10
- "resultados em tempo real" — fonte(s): SCRUM-10
- "sugestões amigáveis." — fonte(s): SCRUM-10
- "filtro por categoria permite selecionar múltiplas categorias" — fonte(s): SCRUM-11
- "combina com busca por nome." — fonte(s): SCRUM-11
- "Visualização de Cardápio" — fonte(s): SCRUM-12
- "visualizar o cardápio completo de um restaurante" — fonte(s): SCRUM-12
- "organizado por seções." — fonte(s): SCRUM-12
- "nome, foto, descrição e preço" — fonte(s): SCRUM-12
- "indicação de indisponibilidade." — fonte(s): SCRUM-12

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "O app atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "melhoria consiste em implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido" — fonte(s): SCRUM-32
- "melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Endereços frequentes podem ser salvos como favoritos ("Casa", "Trabalho") acessíveis diretamente na tela de entrega." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente via listener de rede e exibir uma tela amigável com ícone, mensagem clara ("Sem conexão com a internet") e botão "Tentar novamente", sem aguardar o timeout da requisição." — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "ao inserir um código de cupom inválido, a API retorna um erro 500 em vez de um erro 422 com mensagem adequada. O app exibe uma mensagem genérica de erro." — fonte(s): SCRUM-29
- "BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "a posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "ao tentar autenticar com Google em dispositivos Android 10, o app exibe uma mensagem de erro sem detalhes. Suspeita-se de incompatibilidade com o Custom Tab usado no redirecionamento." — fonte(s): SCRUM-27
- "BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "as notificações push de mudança de status do pedido estão chegando com atraso de 5 minutos após a mudança real de status. O job de envio de notificações roda em intervalo fixo de 5 minutos em vez de ser disparado por evento." — fonte(s): SCRUM-26
- "BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto." — fonte(s): SCRUM-25
- "BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "ao tentar adicionar um item sem foto ao carrinho, o aplicativo para de responder e exibe uma tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula." — fonte(s): SCRUM-22