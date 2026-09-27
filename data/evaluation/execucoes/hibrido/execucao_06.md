# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

# Autenticação e Cadastro
A porta de entrada do app, que impacta diretamente a experiência inicial do usuário. Inclui criação de conta, login, recuperação de senha e gerenciamento de perfil.

# Catálogo de Restaurantes
Exibe, busca e filtra restaurantes e seus cardápios. O usuário pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

# Carrinho e Pedidos
O núcleo do app, onde a conversão de interesse em compra acontece. Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido.

# Pagamentos
Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

# Rastreamento de Entrega
Permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

# Avaliações
Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Cadastro e Login

- **Cadastro com e-mail e senha**: os usuários novos podem criar uma conta no app, preenchendo nome completo, e-mail e senha. O sistema valida o e-mail e a senha, e envia um e-mail de confirmação.
- **Login com Google**: os usuários podem acessar o app com sua conta Google, sem precisar criar uma senha. O fluxo OAuth funciona em iOS e Android.
- **Redefinição de senha**: os usuários podem redefinir sua senha por e-mail, caso a esqueçam. O link de redefinição é válido por 30 minutos e todas as sessões ativas são encerradas após a troca de senha.

### Busca e Filtro

- **Busca de restaurantes por nome**: os usuários podem buscar restaurantes pelo nome, com resultados exibidos em tempo real. O sistema retorna resultados com debounce de 300ms para evitar requisições excessivas.
- **Filtro por categoria**: os usuários podem filtrar restaurantes por categoria de culinária, selecionando múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

### Visualização e Montagem do Pedido

- **Visualização do cardápio**: os usuários podem ver o cardápio completo de um restaurante, organizado por seções. Cada item exibe nome, foto, descrição curta e preço.
- **Adicionar itens ao carrinho**: os usuários podem adicionar itens ao carrinho, clicando em um item do cardápio e confirmando. O carrinho só pode conter itens de um único restaurante por vez.
- **Aplicar cupom de desconto**: os usuários podem aplicar um cupom de desconto no pedido, digitando o código em um campo dedicado e clicando em "Aplicar". O sistema valida o cupom e exibe o desconto aplicado.

### Acompanhamento e Pagamento

- **Acompanhamento de status do pedido**: os usuários podem acompanhar o status do pedido em tempo real, com uma linha do tempo visual mostrando as etapas. O tempo estimado de entrega é exibido e atualizado dinamicamente.
- **Pagamento com Pix**: os usuários podem pagar com Pix, selecionando-o como método de pagamento e gerando um QR Code válido por 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela.
- **Pagamento com cartão de crédito**: os usuários podem pagar com cartão de crédito, inserindo os dados do cartão em um formulário tokenizado. O sistema exibe as bandeiras aceitas e processa o pagamento, exibindo o resultado imediatamente.

### Entrega e Avaliação

- **Cancelamento de pedido**: os usuários podem cancelar o pedido antes que seja aceito pelo restaurante, informando o motivo do cancelamento. O estorno é processado automaticamente para o método de pagamento utilizado.
- **Notificação de saída para entrega**: os usuários recebem uma notificação push quando o pedido sai para entrega, com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento.
- **Rastreamento do entregador no mapa**: os usuários podem ver a localização do entregador em tempo real no mapa, após o pedido entrar no status "Saiu para Entrega". A posição do entregador é atualizada a cada 10 segundos.
- **Avaliação do restaurante**: os usuários podem avaliar o restaurante após receber o pedido, atribuindo de 1 a 5 estrelas e adicionando um comentário opcional. A média de avaliações do restaurante é atualizada em tempo real.

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

### Problemas com a tela de rastreamento

- SCRUM-28, BUG-06, "Tela de rastreamento não atualiza posição automaticamente" (status: Tarefas pendentes): a posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### Problemas com o login

- SCRUM-27, BUG-05, "Login com Google falha em Android 10" (status: Tarefas pendentes): ao tentar autenticar com Google em dispositivos Android 10, o app exibe a mensagem "Falha na autenticação. Tente novamente." sem mais detalhes.

### Problemas com notificações

- SCRUM-26, BUG-04, "Notificação de pedido chegando com atraso de ~5 minutos" (status: Tarefas pendentes): as notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status.

### Problemas com o checkout

- SCRUM-25, BUG-03, "Valor do frete somando em dobro no resumo do pedido" (status: Tarefas pendentes): na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também está sendo somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto.

### Problemas com filtros

- SCRUM-23, BUG-02, "Filtro de categoria não reseta ao voltar para tela inicial" (status: Tarefas pendentes): quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado.

### Problemas com itens sem foto

- SCRUM-22, BUG-01, "App trava ao adicionar item sem foto ao carrinho" (status: Tarefas pendentes): ao tentar adicionar ao carrinho um item do cardápio que não possui imagem cadastrada, o aplicativo para de responder e exibe tela branca.

### Problemas com cupons

- SCRUM-29, BUG-07, "Cupom inválido retorna erro 500" (status: Tarefas pendentes): ao inserir um código de cupom que não existe no sistema, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada. O app exibe a mensagem genérica "Erro inesperado. Tente novamente."


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "porta de entrada do app" — fonte(s): SCRUM-1
- "impacta diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "Exibe, busca e filtra restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "núcleo do app" — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "todas as formas de pagamento disponíveis na plataforma" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "usuários novos" — fonte(s): SCRUM-7
- "criar uma conta no app" — fonte(s): SCRUM-7
- "preenchendo nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "sistema valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "Login com Google" — fonte(s): SCRUM-8
- "usuários podem acessar o app com sua conta Google" — fonte(s): SCRUM-8
- "sem precisar criar uma senha." — fonte(s): SCRUM-8
- "fluxo OAuth funciona em iOS e Android." — fonte(s): SCRUM-8
- "Redefinição de senha" — fonte(s): SCRUM-9
- "usuários podem redefinir sua senha por e-mail" — fonte(s): SCRUM-9
- "caso a esqueçam." — fonte(s): SCRUM-9
- "link de redefinição é válido por 30 minutos" — fonte(s): SCRUM-9
- "todas as sessões ativas são encerradas após a troca de senha." — fonte(s): SCRUM-9
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "usuários podem buscar restaurantes pelo nome" — fonte(s): SCRUM-10
- "resultados exibidos em tempo real." — fonte(s): SCRUM-10
- "sistema retorna resultados com debounce de 300ms para evitar requisições excessivas." — fonte(s): SCRUM-10
- "Filtro por categoria" — fonte(s): SCRUM-11
- "usuários podem filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "selecionando múltiplas categorias simultaneamente." — fonte(s): SCRUM-11
- "filtro ativo é destacado visualmente" — fonte(s): SCRUM-11
- "pode ser removido individualmente." — fonte(s): SCRUM-11
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "usuários podem ver o cardápio completo de um restaurante" — fonte(s): SCRUM-12
- "organizado por seções." — fonte(s): SCRUM-12
- "item exibe nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "usuários podem adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "clicando em um item do cardápio e confirmando." — fonte(s): SCRUM-13
- "carrinho só pode conter itens de um único restaurante por vez." — fonte(s): SCRUM-13
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "usuários podem aplicar um cupom de desconto no pedido" — fonte(s): SCRUM-14
- "digitando o código em um campo dedicado e clicando em "Aplicar"" — fonte(s): SCRUM-14
- "sistema valida o cupom" — fonte(s): SCRUM-14
- "exibe o desconto aplicado." — fonte(s): SCRUM-14
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "usuários podem acompanhar o status do pedido em tempo real" — fonte(s): SCRUM-15
- "uma linha do tempo visual mostrando as etapas." — fonte(s): SCRUM-15
- "tempo estimado de entrega é exibido e atualizado dinamicamente." — fonte(s): SCRUM-15
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "usuários podem pagar com Pix" — fonte(s): SCRUM-18
- "selecionando-o como método de pagamento" — fonte(s): SCRUM-18
- "gerando um QR Code válido por 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela." — fonte(s): SCRUM-18
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "usuários podem pagar com cartão de crédito" — fonte(s): SCRUM-17
- "inserindo os dados do cartão em um formulário tokenizado." — fonte(s): SCRUM-17
- "sistema exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "processa o pagamento" — fonte(s): SCRUM-17
- "exibindo o resultado imediatamente." — fonte(s): SCRUM-17
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "usuários podem cancelar o pedido antes que seja aceito pelo restaurante" — fonte(s): SCRUM-16
- "informando o motivo do cancelamento." — fonte(s): SCRUM-16
- "estorno é processado automaticamente para o método de pagamento utilizado." — fonte(s): SCRUM-16
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "usuários recebem uma notificação push quando o pedido sai para entrega" — fonte(s): SCRUM-20
- "o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento." — fonte(s): SCRUM-20
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "usuários podem ver a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "o pedido entrar no status "Saiu para Entrega"" — fonte(s): SCRUM-19
- "posição do entregador é atualizada a cada 10 segundos." — fonte(s): SCRUM-19
- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "usuários podem avaliar o restaurante após receber o pedido" — fonte(s): SCRUM-21
- "atribuindo de 1 a 5 estrelas e adicionando um comentário opcional." — fonte(s): SCRUM-21
- "média de avaliações do restaurante é atualizada em tempo real." — fonte(s): SCRUM-21

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema" — fonte(s): SCRUM-33
- "opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "usuário precisa digitar o endereço de entrega em cada novo pedido." — fonte(s): SCRUM-32
- "salvar automaticamente o último endereço utilizado" — fonte(s): SCRUM-32
- "pré-preencher o campo no próximo checkout" — fonte(s): SCRUM-32
- "opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "usuário abre o app sem conexão com a internet" — fonte(s): SCRUM-31
- "mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente" — fonte(s): SCRUM-31
- "tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "carregar a lista de restaurantes ou o cardápio" — fonte(s): SCRUM-30
- "spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento" — fonte(s): SCRUM-30
- "melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "SCRUM-28" — fonte(s): SCRUM-28
- "BUG-06" — fonte(s): SCRUM-28
- ""Tela de rastreamento não atualiza posição automaticamente"" — fonte(s): SCRUM-28
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "SCRUM-27" — fonte(s): SCRUM-27
- "BUG-05" — fonte(s): SCRUM-27
- ""Login com Google falha em Android 10"" — fonte(s): SCRUM-27
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "ao tentar autenticar com Google em dispositivos Android 10" — fonte(s): SCRUM-27
- "o app exibe a mensagem "Falha na autenticação. Tente novamente."" — fonte(s): SCRUM-27
- "sem mais detalhes." — fonte(s): SCRUM-27
- "SCRUM-26" — fonte(s): SCRUM-26
- "BUG-04" — fonte(s): SCRUM-26
- ""Notificação de pedido chegando com atraso de ~5 minutos"" — fonte(s): SCRUM-26
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "as notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "SCRUM-25" — fonte(s): SCRUM-25
- "BUG-03" — fonte(s): SCRUM-25
- ""Valor do frete somando em dobro no resumo do pedido"" — fonte(s): SCRUM-25
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega"" — fonte(s): SCRUM-25
- "também está sendo somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "fazendo o total ficar incorreto." — fonte(s): SCRUM-25
- "SCRUM-23" — fonte(s): SCRUM-23
- "BUG-02" — fonte(s): SCRUM-23
- ""Filtro de categoria não reseta ao voltar para tela inicial"" — fonte(s): SCRUM-23
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "quando o usuário seleciona uma categoria e volta para a tela inicial" — fonte(s): SCRUM-23
- "o filtro permanece ativo visualmente" — fonte(s): SCRUM-23
- "a lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "SCRUM-22" — fonte(s): SCRUM-22
- "BUG-01" — fonte(s): SCRUM-22
- ""App trava ao adicionar item sem foto ao carrinho"" — fonte(s): SCRUM-22
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "ao tentar adicionar ao carrinho um item do cardápio que não possui imagem cadastrada" — fonte(s): SCRUM-22
- "o aplicativo para de responder e exibe tela branca." — fonte(s): SCRUM-22
- "SCRUM-29" — fonte(s): SCRUM-29
- "BUG-07" — fonte(s): SCRUM-29
- ""Cupom inválido retorna erro 500"" — fonte(s): SCRUM-29
- "(status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "ao inserir um código de cupom que não existe no sistema" — fonte(s): SCRUM-29
- "a API retorna HTTP 500 (Internal Server Error)" — fonte(s): SCRUM-29
- "em vez de HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "O app exibe a mensagem genérica "Erro inesperado. Tente novamente."" — fonte(s): SCRUM-29