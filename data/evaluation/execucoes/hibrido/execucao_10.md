# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

# Autenticação e Cadastro
A porta de entrada do app, que impacta diretamente a experiência inicial do usuário. Agrupa funcionalidades de acesso à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

# Catálogo de Restaurantes
Exibe, busca e filtra restaurantes e seus cardápios. Ajuda o usuário a encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

# Carrinho e Pedidos
Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É o núcleo do app, onde a conversão de interesse em compra acontece.

# Pagamentos
Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

# Rastreamento de Entrega
Permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

# Avaliações
Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Cadastro e Login

- **Cadastro com e-mail e senha**: os usuários novos podem criar uma conta no app, inserindo nome completo, e-mail e senha. O sistema valida o e-mail e a senha, e envia um e-mail de confirmação.
- **Login com Google**: os usuários podem acessar o app com sua conta Google, sem precisar criar uma senha. O fluxo OAuth funciona em iOS e Android.
- **Redefinição de senha**: os usuários podem redefinir sua senha por e-mail, recebendo um link de redefinição válido por 30 minutos. Após a redefinição, todas as sessões ativas são encerradas.

### Busca e Filtro de Restaurantes

- **Busca de restaurantes por nome**: os usuários podem buscar restaurantes pelo nome, com resultados exibidos em tempo real. O sistema retorna resultados em até 1 segundo, com debounce de 300ms para evitar requisições excessivas.
- **Filtro por categoria**: os usuários podem filtrar restaurantes por categoria de culinária, selecionando múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

### Visualização de Cardápio e Pedidos

- **Visualização do cardápio**: os usuários podem ver o cardápio completo de um restaurante, organizado por seções. Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados.
- **Adicionar itens ao carrinho**: os usuários podem adicionar itens ao carrinho, com opções de personalização e quantidade. O carrinho só pode conter itens de um único restaurante por vez.
- **Acompanhamento de status do pedido**: os usuários podem acompanhar o status do pedido em tempo real, com uma linha do tempo visual mostrando as etapas. O tempo estimado de entrega é exibido e atualizado dinamicamente.
- **Cancelamento de pedido**: os usuários podem cancelar o pedido antes que seja aceito pelo restaurante, informando o motivo do cancelamento. O estorno é processado automaticamente para o método de pagamento utilizado.

### Pagamento e Desconto

- **Pagamento com Pix**: os usuários podem pagar com Pix, gerando um QR Code válido por 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela após a confirmação.
- **Pagamento com cartão de crédito**: os usuários podem pagar com cartão de crédito, inserindo os dados do cartão em um formulário tokenizado. O sistema exibe as bandeiras aceitas e fornece feedback imediato de aprovação ou recusa.
- **Aplicar cupom de desconto**: os usuários podem aplicar um cupom de desconto no pedido, digitando o código em um campo dedicado. O sistema valida o cupom e exibe o desconto aplicado no resumo do pedido.

### Entrega e Avaliação

- **Notificação de saída para entrega**: os usuários recebem uma notificação push quando o pedido sai para entrega, com o nome do restaurante, tempo estimado de entrega e um link direto para a tela de rastreamento.
- **Rastreamento do entregador no mapa**: os usuários podem ver a localização do entregador em tempo real no mapa, com a posição atualizada a cada 10 segundos. O trajeto estimado é exibido no mapa e o tempo restante é recalculado dinamicamente.
- **Avaliação do restaurante**: após o pedido ser marcado como entregue, os usuários recebem uma notificação convidando-os a avaliar. Na tela de avaliação, podem atribuir de 1 a 5 estrelas e adicionar um comentário opcional. A média de avaliações do restaurante é atualizada em tempo real.

## Tarefas Operacionais

### Modo escuro

O app atualmente só suporta tema claro, mas a melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar último endereço de entrega automaticamente

Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido, mas a melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de erro sem conexão com internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente".

### Skeleton loading nas telas de lista

Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes)

Ao adicionar um item sem foto ao carrinho, o aplicativo trava e exibe uma tela branca. O problema ocorre porque o componente de imagem não trata URLs nulas.

### BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes)

Quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado.

### BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes)

Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.

### BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes)

As notificações push de mudança de status do pedido chegam com atraso de cerca de 5 minutos após a mudança real de status. Isso ocorre porque o job de envio de notificações roda em intervalos fixos de 5 minutos.

### BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes)

Ao tentar autenticar com o Google em dispositivos Android 10, o fluxo OAuth redireciona corretamente para a tela de seleção de conta, mas ao retornar ao app, exibe uma mensagem de falha na autenticação.

### BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes)

A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes)

Ao inserir um código de cupom inválido, a API retorna um erro 500 em vez de um erro 422 com mensagem adequada. O app exibe uma mensagem genérica de erro inesperado.


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "porta de entrada do app, que impacta diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "Agrupa funcionalidades de acesso à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "Exibe, busca e filtra restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "Ajuda o usuário a encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "núcleo do app, onde a conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "Permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "usuários novos" — fonte(s): SCRUM-7
- "criar uma conta no app" — fonte(s): SCRUM-7
- "inserindo nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "sistema valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "Login com Google" — fonte(s): SCRUM-8
- "usuários podem acessar o app com sua conta Google" — fonte(s): SCRUM-8
- "sem precisar criar uma senha." — fonte(s): SCRUM-8
- "fluxo OAuth funciona em iOS e Android." — fonte(s): SCRUM-8
- "Redefinição de senha" — fonte(s): SCRUM-9
- "usuários podem redefinir sua senha por e-mail" — fonte(s): SCRUM-9
- "link de redefinição válido por 30 minutos." — fonte(s): SCRUM-9
- "redefinição, todas as sessões ativas são encerradas." — fonte(s): SCRUM-9
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "usuários podem buscar restaurantes pelo nome" — fonte(s): SCRUM-10
- "resultados exibidos em tempo real." — fonte(s): SCRUM-10
- "sistema retorna resultados em até 1 segundo" — fonte(s): SCRUM-10
- "debounce de 300ms para evitar requisições excessivas." — fonte(s): SCRUM-10
- "Filtro por categoria" — fonte(s): SCRUM-11
- "usuários podem filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "selecionando múltiplas categorias simultaneamente." — fonte(s): SCRUM-11
- "filtro ativo é destacado visualmente e pode ser removido individualmente." — fonte(s): SCRUM-11
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "usuários podem ver o cardápio completo de um restaurante" — fonte(s): SCRUM-12
- "organizado por seções." — fonte(s): SCRUM-12
- "item exibe nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Itens indisponíveis aparecem como desabilitados." — fonte(s): SCRUM-12
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "usuários podem adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "opções de personalização e quantidade." — fonte(s): SCRUM-13
- "carrinho só pode conter itens de um único restaurante por vez." — fonte(s): SCRUM-13
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "usuários podem acompanhar o status do pedido em tempo real" — fonte(s): SCRUM-15
- "linha do tempo visual mostrando as etapas." — fonte(s): SCRUM-15
- "tempo estimado de entrega é exibido e atualizado dinamicamente." — fonte(s): SCRUM-15
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "usuários podem cancelar o pedido antes que seja aceito pelo restaurante" — fonte(s): SCRUM-16
- "informando o motivo do cancelamento." — fonte(s): SCRUM-16
- "estorno é processado automaticamente para o método de pagamento utilizado." — fonte(s): SCRUM-16
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "usuários podem pagar com Pix" — fonte(s): SCRUM-18
- "gerando um QR Code válido por 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela após a confirmação." — fonte(s): SCRUM-18
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "usuários podem pagar com cartão de crédito" — fonte(s): SCRUM-17
- "inserindo os dados do cartão em um formulário tokenizado." — fonte(s): SCRUM-17
- "sistema exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "feedback imediato de aprovação ou recusa." — fonte(s): SCRUM-17
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "usuários podem aplicar um cupom de desconto no pedido" — fonte(s): SCRUM-14
- "digitando o código em um campo dedicado." — fonte(s): SCRUM-14
- "sistema valida o cupom" — fonte(s): SCRUM-14
- "exibe o desconto aplicado no resumo do pedido." — fonte(s): SCRUM-14
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "usuários recebem uma notificação push quando o pedido sai para entrega" — fonte(s): SCRUM-20
- "nome do restaurante, tempo estimado de entrega e um link direto para a tela de rastreamento." — fonte(s): SCRUM-20
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "usuários podem ver a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "posição atualizada a cada 10 segundos." — fonte(s): SCRUM-19
- "trajeto estimado é exibido no mapa" — fonte(s): SCRUM-19
- "tempo restante é recalculado dinamicamente." — fonte(s): SCRUM-19
- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "pedido ser marcado como entregue" — fonte(s): SCRUM-21
- "usuários recebem uma notificação convidando-os a avaliar." — fonte(s): SCRUM-21
- "tela de avaliação" — fonte(s): SCRUM-21
- "atribuir de 1 a 5 estrelas e adicionar um comentário opcional." — fonte(s): SCRUM-21
- "média de avaliações do restaurante é atualizada em tempo real." — fonte(s): SCRUM-21

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "O app atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "melhoria consiste em implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido" — fonte(s): SCRUM-32
- "melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-01 — App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "(SCRUM-22, status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "Ao adicionar um item sem foto ao carrinho, o aplicativo trava e exibe uma tela branca." — fonte(s): SCRUM-22
- "O problema ocorre porque o componente de imagem não trata URLs nulas." — fonte(s): SCRUM-22
- "BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial" — fonte(s): SCRUM-23
- "(SCRUM-23, status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "Quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "BUG-03 — Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "(SCRUM-25, status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto." — fonte(s): SCRUM-25
- "BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "(SCRUM-26, status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "As notificações push de mudança de status do pedido chegam com atraso de cerca de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "Isso ocorre porque o job de envio de notificações roda em intervalos fixos de 5 minutos." — fonte(s): SCRUM-26
- "BUG-05 — Login com Google falha em Android 10" — fonte(s): SCRUM-27
- "(SCRUM-27, status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "Ao tentar autenticar com o Google em dispositivos Android 10, o fluxo OAuth redireciona corretamente para a tela de seleção de conta, mas ao retornar ao app, exibe uma mensagem de falha na autenticação." — fonte(s): SCRUM-27
- "BUG-06 — Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "(SCRUM-28, status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "BUG-07 — Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "(SCRUM-29, status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "Ao inserir um código de cupom inválido, a API retorna um erro 500 em vez de um erro 422 com mensagem adequada." — fonte(s): SCRUM-29
- "O app exibe uma mensagem genérica de erro inesperado." — fonte(s): SCRUM-29