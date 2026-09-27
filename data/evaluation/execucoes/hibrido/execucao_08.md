# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

# Autenticação e Cadastro
O EP-01 agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

# Catálogo de Restaurantes
O EP-02 abrange a exibição, busca e filtragem de restaurantes e seus cardápios. O usuário pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

# Carrinho e Pedidos
O EP-03 cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É o núcleo do app, onde a conversão de interesse em compra acontece.

# Pagamentos
O EP-04 é responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

# Rastreamento de Entrega
O EP-05 oferece funcionalidades que permitem ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

# Avaliações
O EP-06 permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Avaliação do restaurante
Após o pedido ser entregue, o usuário pode avaliar o restaurante com uma nota de 1 a 5 estrelas e adicionar um comentário opcional. A média de avaliações do restaurante é atualizada em tempo real.

### Notificação de saída para entrega
O sistema envia uma notificação push ao usuário quando o pedido sai para entrega, com informações como o nome do restaurante, tempo estimado e um link para a tela de rastreamento.

### Rastreamento do entregador no mapa
Quando o pedido está em trânsito, o usuário pode ver a localização do entregador em tempo real no mapa, junto com o restaurante e o endereço de entrega.

### Pagamento com Pix
O usuário pode selecionar Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O app monitora o pagamento e avança automaticamente para a próxima tela após a confirmação.

### Pagamento com cartão de crédito
Na tela de checkout, o usuário seleciona cartão de crédito e insere os dados do cartão em um formulário seguro. O sistema exibe as bandeiras aceitas e processa o pagamento, mostrando o resultado imediatamente.

### Cancelamento de pedido
Enquanto o pedido estiver no status "Pedido Recebido", o usuário pode cancelá-lo informando o motivo. O estorno é processado automaticamente e um e-mail de confirmação é enviado.

### Acompanhamento de status do pedido
Após confirmar o pedido, o usuário pode acompanhar seu status em tempo real, com uma linha do tempo visualizando as etapas e o tempo estimado de entrega.

### Aplicar cupom de desconto
Na tela de checkout, o usuário pode aplicar um cupom de desconto, que é validado em tempo real. O desconto aplicado é exibido de forma destacada no resumo do pedido.

### Adicionar itens ao carrinho
O usuário pode adicionar itens ao carrinho, visualizando uma bottom sheet com opções de personalização e quantidade. O carrinho só pode conter itens de um único restaurante por vez.

### Visualização do cardápio
Ao clicar em um restaurante, o usuário acessa a página de detalhes com o cardápio organizado por seções, exibindo nome, foto, descrição e preço de cada item.

### Filtro por categoria
Na tela principal, o usuário pode filtrar restaurantes por categoria de culinária, selecionando múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente.

### Busca de restaurantes por nome
O usuário pode buscar restaurantes pelo nome na tela principal, com resultados em tempo real e debounce de 300ms para evitar requisições excessivas.

### Redefinição de senha
Caso esqueça a senha, o usuário pode clicar em "Esqueci minha senha" e receber um link de redefinição por e-mail, válido por 30 minutos. Após a redefinição, todas as sessões ativas são encerradas.

### Login com Google
O usuário pode fazer login com sua conta Google, sendo redirecionado para o fluxo de autenticação OAuth. Em primeiro acesso, uma conta é criada automaticamente com os dados do perfil Google.

### Cadastro com e-mail e senha
O usuário novo pode se cadastrar com e-mail e senha, validando o formato do e-mail e a força da senha. Um e-mail de confirmação é enviado em até 1 minuto.

## Tarefas Operacionais

### Modo escuro

O app atualmente só suporta tema claro, mas a melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar último endereço de entrega automaticamente

Atualmente, o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de erro sem conexão com internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente".

### Skeleton loading nas telas de lista

Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes)

O aplicativo trava ao tentar adicionar um item sem imagem ao carrinho. O problema ocorre porque o componente de imagem não trata URLs nulas.

### BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes)

O filtro de categoria não é resetado ao voltar para a tela inicial, exibindo todos os restaurantes sem filtro aplicado.

### BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes)

A taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.

### BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes)

As notificações push de mudança de status do pedido chegam com atraso de cerca de 5 minutos após a mudança real de status.

### BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes)

Ao tentar autenticar com Google em dispositivos Android 10, o fluxo OAuth redireciona corretamente, mas ao retornar ao app exibe uma mensagem de falha na autenticação.

### BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes)

A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos.

### BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes)

Ao inserir um código de cupom inválido, a API retorna um erro HTTP 500 em vez de um HTTP 422 com mensagem de erro adequada. O app exibe uma mensagem genérica de erro.


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "EP-01" — fonte(s): SCRUM-1
- "agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma" — fonte(s): SCRUM-1
- "criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "EP-02" — fonte(s): SCRUM-2
- "exibição, busca e filtragem de restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir" — fonte(s): SCRUM-2
- "informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "EP-03" — fonte(s): SCRUM-3
- "cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "núcleo do app" — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "EP-04" — fonte(s): SCRUM-4
- "responsável por todas as formas de pagamento disponíveis na plataforma" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "EP-05" — fonte(s): SCRUM-5
- "funcionalidades que permitem ao usuário acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "EP-06" — fonte(s): SCRUM-6
- "usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Após o pedido ser entregue" — fonte(s): SCRUM-21
- "avaliar o restaurante com uma nota de 1 a 5 estrelas" — fonte(s): SCRUM-21
- "adicionar um comentário opcional." — fonte(s): SCRUM-21
- "A média de avaliações do restaurante é atualizada em tempo real." — fonte(s): SCRUM-21
- "envia uma notificação push ao usuário quando o pedido sai para entrega" — fonte(s): SCRUM-20
- "o nome do restaurante, tempo estimado e um link para a tela de rastreamento." — fonte(s): SCRUM-20
- "ver a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "o restaurante e o endereço de entrega." — fonte(s): SCRUM-19
- "selecionar Pix como método de pagamento" — fonte(s): SCRUM-18
- "um QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "monitora o pagamento e avança automaticamente para a próxima tela após a confirmação." — fonte(s): SCRUM-18
- "tela de checkout" — fonte(s): SCRUM-17
- "seleciona cartão de crédito e insere os dados do cartão em um formulário seguro." — fonte(s): SCRUM-17
- "exibe as bandeiras aceitas e processa o pagamento" — fonte(s): SCRUM-17
- "o resultado imediatamente." — fonte(s): SCRUM-17
- ""Pedido Recebido"" — fonte(s): SCRUM-16
- "cancelá-lo informando o motivo." — fonte(s): SCRUM-16
- "estorno é processado automaticamente" — fonte(s): SCRUM-16
- "um e-mail de confirmação é enviado." — fonte(s): SCRUM-16
- "confirmar o pedido" — fonte(s): SCRUM-15
- "acompanhar seu status em tempo real" — fonte(s): SCRUM-15
- "linha do tempo visualizando as etapas e o tempo estimado de entrega." — fonte(s): SCRUM-15
- "tela de checkout" — fonte(s): SCRUM-14
- "aplicar um cupom de desconto" — fonte(s): SCRUM-14
- "validado em tempo real." — fonte(s): SCRUM-14
- "desconto aplicado é exibido de forma destacada no resumo do pedido." — fonte(s): SCRUM-14
- "adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "bottom sheet com opções de personalização e quantidade." — fonte(s): SCRUM-13
- "carrinho só pode conter itens de um único restaurante por vez." — fonte(s): SCRUM-13
- "clicar em um restaurante" — fonte(s): SCRUM-12
- "página de detalhes com o cardápio organizado por seções" — fonte(s): SCRUM-12
- "nome, foto, descrição e preço de cada item." — fonte(s): SCRUM-12
- "tela principal" — fonte(s): SCRUM-11
- "filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "selecionando múltiplas categorias simultaneamente." — fonte(s): SCRUM-11
- "filtro ativo é destacado visualmente." — fonte(s): SCRUM-11
- "buscar restaurantes pelo nome na tela principal" — fonte(s): SCRUM-10
- "resultados em tempo real" — fonte(s): SCRUM-10
- "debounce de 300ms" — fonte(s): SCRUM-10
- "evitar requisições excessivas." — fonte(s): SCRUM-10
- "esqueça a senha" — fonte(s): SCRUM-9
- "clicar em "Esqueci minha senha"" — fonte(s): SCRUM-9
- "receber um link de redefinição por e-mail" — fonte(s): SCRUM-9
- "válido por 30 minutos." — fonte(s): SCRUM-9
- "redefinição, todas as sessões ativas são encerradas." — fonte(s): SCRUM-9
- "fazer login com sua conta Google" — fonte(s): SCRUM-8
- "redirecionado para o fluxo de autenticação OAuth." — fonte(s): SCRUM-8
- "primeiro acesso, uma conta é criada automaticamente com os dados do perfil Google." — fonte(s): SCRUM-8
- "se cadastrar com e-mail e senha" — fonte(s): SCRUM-7
- "validando o formato do e-mail e a força da senha." — fonte(s): SCRUM-7
- "e-mail de confirmação é enviado em até 1 minuto." — fonte(s): SCRUM-7

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "O app atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "melhoria consiste em implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema" — fonte(s): SCRUM-33
- "opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "Atualmente, o usuário precisa digitar o endereço de entrega em cada novo pedido." — fonte(s): SCRUM-32
- "melhoria consiste em salvar automaticamente o último endereço utilizado" — fonte(s): SCRUM-32
- "pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente" — fonte(s): SCRUM-31
- "exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-01 — App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "(SCRUM-22, status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "aplicativo trava" — fonte(s): SCRUM-22
- "tentar adicionar um item sem imagem ao carrinho." — fonte(s): SCRUM-22
- "problema ocorre porque o componente de imagem não trata URLs nulas." — fonte(s): SCRUM-22
- "BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial" — fonte(s): SCRUM-23
- "(SCRUM-23, status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "filtro de categoria não é resetado ao voltar para a tela inicial" — fonte(s): SCRUM-23
- "exibindo todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "BUG-03 — Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "(SCRUM-25, status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "taxa de entrega é exibida corretamente" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total incorreto." — fonte(s): SCRUM-25
- "BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "(SCRUM-26, status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido chegam com atraso de cerca de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "BUG-05 — Login com Google falha em Android 10" — fonte(s): SCRUM-27
- "(SCRUM-27, status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "tentar autenticar com Google em dispositivos Android 10" — fonte(s): SCRUM-27
- "fluxo OAuth redireciona corretamente" — fonte(s): SCRUM-27
- "ao retornar ao app exibe uma mensagem de falha na autenticação." — fonte(s): SCRUM-27
- "BUG-06 — Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "(SCRUM-28, status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "BUG-07 — Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "(SCRUM-29, status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "inserir um código de cupom inválido" — fonte(s): SCRUM-29
- "API retorna um erro HTTP 500 em vez de um HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "app exibe uma mensagem genérica de erro." — fonte(s): SCRUM-29