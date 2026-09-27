# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

### Autenticação e Cadastro
O EP-01 abrange todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

### Catálogo de Restaurantes
O EP-02 permite que o usuário encontre facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

### Carrinho e Pedidos
O EP-03 cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido, sendo o núcleo do app.

### Pagamentos
O EP-04 garante segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

### Rastreamento de Entrega
O EP-05 permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

### Avaliações
O EP-06 permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Cadastro e Login

- **Cadastro com e-mail e senha**: os usuários novos podem se cadastrar informando nome completo, e-mail e senha. O sistema valida o e-mail e a senha, e envia um e-mail de confirmação.
- **Login com Google**: os usuários podem fazer login com sua conta Google, sem precisar criar uma senha. O fluxo OAuth funciona em iOS e Android.
- **Redefinição de senha**: se esquecerem a senha, os usuários podem clicar em "Esqueci minha senha", informar seu e-mail e receber um link de redefinição, válido por 30 minutos.

### Busca e Filtro

- **Busca de restaurantes por nome**: os usuários podem buscar restaurantes pelo nome, parcial ou completo, e o sistema retorna resultados em tempo real com debounce de 300ms.
- **Filtro por categoria**: os usuários podem filtrar restaurantes por categoria de culinária, selecionando múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

### Visualização e Montagem do Pedido

- **Visualização do cardápio**: ao clicar em um restaurante, os usuários acessam a página de detalhes com banner, informações do estabelecimento e o cardápio organizado por seções. Cada item exibe nome, foto, descrição curta e preço.
- **Adicionar itens ao carrinho**: os usuários clicam em um item do cardápio e uma bottom sheet é exibida com opções de personalização. Ao confirmar, o item é adicionado ao carrinho e um indicador flutuante com o total aparece na tela.
- **Aplicar cupom de desconto**: na tela de checkout, os usuários digitam o código do cupom e clicam em "Aplicar". O sistema valida o cupom e exibe o desconto aplicado no resumo do pedido.

### Pagamento e Cancelamento

- **Pagamento com cartão de crédito**: na tela de checkout, os usuários selecionam "Cartão de Crédito" e inserem os dados do cartão em um formulário tokenizado. O sistema exibe as bandeiras aceitas e, após confirmação, processa o pagamento, exibindo o resultado imediatamente.
- **Pagamento com Pix**: os usuários selecionam Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O app monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela.
- **Cancelamento de pedido**: enquanto o pedido estiver no status "Pedido Recebido", os usuários podem clicar em "Cancelar Pedido", informar o motivo e confirmar. O estorno é processado automaticamente para o método de pagamento utilizado.

### Acompanhamento e Avaliação

- **Acompanhamento de status do pedido**: após confirmar o pedido, os usuários acessam uma tela de acompanhamento com linha do tempo visual mostrando as etapas. Cada etapa é atualizada via WebSocket em tempo real.
- **Rastreamento do entregador no mapa**: após o pedido entrar no status "Saiu para Entrega", a tela de acompanhamento exibe um mapa com a posição atual do entregador, a localização do restaurante e o endereço de entrega.
- **Notificação de saída para entrega**: quando o status do pedido muda para "Saiu para Entrega", o sistema dispara uma notificação push para o dispositivo do usuário com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento.
- **Avaliação do restaurante**: após o pedido ser marcado como entregue, os usuários recebem uma notificação convidando-os a avaliar. Na tela de avaliação, atribuem de 1 a 5 estrelas e podem adicionar um comentário opcional.

## Tarefas Operacionais

### Modo escuro
O app atualmente só suporta tema claro, mas a implementação do modo escuro seguirá as diretrizes de design do sistema operacional, com detecção automática da preferência do sistema e opção manual de alternar nas configurações.

### Salvar último endereço de entrega automaticamente
Atualmente, o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de erro sem conexão com internet
Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão "Tentar novamente".

### Skeleton loading nas telas de lista
Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### Problemas com a tela de rastreamento

- BUG-06 (SCRUM-28, tarefas pendentes): a posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### Problemas com o login

- BUG-05 (SCRUM-27, tarefas pendentes): o login com Google falha em dispositivos Android 10 (API 29). Ao retornar ao app, exibe a mensagem "Falha na autenticação. Tente novamente." sem mais detalhes.

### Problemas com notificações

- BUG-04 (SCRUM-26, tarefas pendentes): as notificações push de mudança de status do pedido chegam com atraso médio de 5 minutos após a mudança real de status. Isso impacta a percepção de tempo real do acompanhamento.

### Problemas com o checkout

- BUG-03 (SCRUM-25, tarefas pendentes): o valor do frete é somado em dobro no resumo do pedido, mas o valor cobrado no pagamento é o correto. O problema é apenas na exibição do resumo.

### Problemas com filtros

- BUG-02 (SCRUM-23, tarefas pendentes): ao voltar para a tela inicial, o filtro de categoria não reseta, mas a lista exibe todos os restaurantes sem filtro aplicado. Há inconsistência entre o estado visual do chip e o estado real da filtragem.

### Problemas com itens sem foto

- BUG-01 (SCRUM-22, tarefas pendentes): ao adicionar um item sem foto ao carrinho, o aplicativo trava e exibe uma tela branca. No iOS, o comportamento é diferente: exibe um ícone quebrado, mas não trava.

### Problemas com cupons

- BUG-07 (SCRUM-29, tarefas pendentes): ao inserir um código de cupom inválido, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada. O app exibe a mensagem genérica "Erro inesperado. Tente novamente."


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "EP-01" — fonte(s): SCRUM-1
- "todas as funcionalidades relacionadas ao acesso do usuário à plataforma" — fonte(s): SCRUM-1
- "criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "EP-02" — fonte(s): SCRUM-2
- "encontre facilmente o que deseja pedir" — fonte(s): SCRUM-2
- "informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "EP-03" — fonte(s): SCRUM-3
- "todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido" — fonte(s): SCRUM-3
- "o núcleo do app." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "EP-04" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "EP-05" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "EP-06" — fonte(s): SCRUM-6
- "expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "novos" — fonte(s): SCRUM-7
- "cadastrar" — fonte(s): SCRUM-7
- "nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "sistema valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "Login com Google" — fonte(s): SCRUM-8
- "fazer login com sua conta Google" — fonte(s): SCRUM-8
- "sem precisar criar uma senha." — fonte(s): SCRUM-8
- "fluxo OAuth funciona em iOS e Android." — fonte(s): SCRUM-8
- "Redefinição de senha" — fonte(s): SCRUM-9
- "esquecerem a senha" — fonte(s): SCRUM-9
- "clicar em "Esqueci minha senha"" — fonte(s): SCRUM-9
- "informar seu e-mail" — fonte(s): SCRUM-9
- "receber um link de redefinição" — fonte(s): SCRUM-9
- "válido por 30 minutos." — fonte(s): SCRUM-9
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "buscar restaurantes pelo nome" — fonte(s): SCRUM-10
- "parcial ou completo" — fonte(s): SCRUM-10
- "sistema retorna resultados em tempo real com debounce de 300ms." — fonte(s): SCRUM-10
- "Filtro por categoria" — fonte(s): SCRUM-11
- "filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "selecionando múltiplas categorias simultaneamente." — fonte(s): SCRUM-11
- "filtro ativo é destacado visualmente" — fonte(s): SCRUM-11
- "pode ser removido individualmente." — fonte(s): SCRUM-11
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "clicar em um restaurante" — fonte(s): SCRUM-12
- "acessam a página de detalhes" — fonte(s): SCRUM-12
- "banner, informações do estabelecimento e o cardápio organizado por seções." — fonte(s): SCRUM-12
- "item exibe nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "clicam em um item do cardápio" — fonte(s): SCRUM-13
- "bottom sheet é exibida com opções de personalização." — fonte(s): SCRUM-13
- "confirmar" — fonte(s): SCRUM-13
- "item é adicionado ao carrinho" — fonte(s): SCRUM-13
- "indicador flutuante com o total aparece na tela." — fonte(s): SCRUM-13
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "tela de checkout" — fonte(s): SCRUM-14
- "digitam o código do cupom" — fonte(s): SCRUM-14
- "clicam em "Aplicar"" — fonte(s): SCRUM-14
- "sistema valida o cupom" — fonte(s): SCRUM-14
- "exibe o desconto aplicado no resumo do pedido." — fonte(s): SCRUM-14
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "tela de checkout" — fonte(s): SCRUM-17
- "selecionam "Cartão de Crédito"" — fonte(s): SCRUM-17
- "inserem os dados do cartão em um formulário tokenizado." — fonte(s): SCRUM-17
- "sistema exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "após confirmação" — fonte(s): SCRUM-17
- "processa o pagamento" — fonte(s): SCRUM-17
- "exibindo o resultado imediatamente." — fonte(s): SCRUM-17
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "selecionam Pix como método de pagamento" — fonte(s): SCRUM-18
- "QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "ao detectar a confirmação" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela." — fonte(s): SCRUM-18
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "pedido estiver no status "Pedido Recebido"" — fonte(s): SCRUM-16
- "clicar em "Cancelar Pedido"" — fonte(s): SCRUM-16
- "informar o motivo e confirmar." — fonte(s): SCRUM-16
- "estorno é processado automaticamente para o método de pagamento utilizado." — fonte(s): SCRUM-16
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "confirmar o pedido" — fonte(s): SCRUM-15
- "acessam uma tela de acompanhamento" — fonte(s): SCRUM-15
- "linha do tempo visual mostrando as etapas." — fonte(s): SCRUM-15
- "etapa é atualizada via WebSocket em tempo real." — fonte(s): SCRUM-15
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "pedido entrar no status "Saiu para Entrega"" — fonte(s): SCRUM-19
- "tela de acompanhamento exibe um mapa" — fonte(s): SCRUM-19
- "posição atual do entregador" — fonte(s): SCRUM-19
- "localização do restaurante e o endereço de entrega." — fonte(s): SCRUM-19
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "status do pedido muda para "Saiu para Entrega"" — fonte(s): SCRUM-20
- "sistema dispara uma notificação push para o dispositivo do usuário" — fonte(s): SCRUM-20
- "nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento." — fonte(s): SCRUM-20
- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "pedido ser marcado como entregue" — fonte(s): SCRUM-21
- "recebem uma notificação convidando-os a avaliar." — fonte(s): SCRUM-21
- "tela de avaliação" — fonte(s): SCRUM-21
- "atribuem de 1 a 5 estrelas" — fonte(s): SCRUM-21
- "adicionar um comentário opcional." — fonte(s): SCRUM-21

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "implementação do modo escuro seguirá as diretrizes de design do sistema operacional" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "usuário precisa digitar o endereço de entrega em cada novo pedido." — fonte(s): SCRUM-32
- "salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado." — fonte(s): SCRUM-30
- "substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-06 (SCRUM-28, tarefas pendentes)" — fonte(s): SCRUM-28
- "a posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "BUG-05 (SCRUM-27, tarefas pendentes)" — fonte(s): SCRUM-27
- "o login com Google falha em dispositivos Android 10 (API 29)" — fonte(s): SCRUM-27
- "Ao retornar ao app, exibe a mensagem "Falha na autenticação. Tente novamente." sem mais detalhes." — fonte(s): SCRUM-27
- "BUG-04 (SCRUM-26, tarefas pendentes)" — fonte(s): SCRUM-26
- "as notificações push de mudança de status do pedido chegam com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "Isso impacta a percepção de tempo real do acompanhamento." — fonte(s): SCRUM-26
- "BUG-03 (SCRUM-25, tarefas pendentes)" — fonte(s): SCRUM-25
- "o valor do frete é somado em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "mas o valor cobrado no pagamento é o correto." — fonte(s): SCRUM-25
- "O problema é apenas na exibição do resumo." — fonte(s): SCRUM-25
- "BUG-02 (SCRUM-23, tarefas pendentes)" — fonte(s): SCRUM-23
- "ao voltar para a tela inicial, o filtro de categoria não reseta" — fonte(s): SCRUM-23
- "mas a lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "Há inconsistência entre o estado visual do chip e o estado real da filtragem." — fonte(s): SCRUM-23
- "BUG-01 (SCRUM-22, tarefas pendentes)" — fonte(s): SCRUM-22
- "ao adicionar um item sem foto ao carrinho, o aplicativo trava e exibe uma tela branca." — fonte(s): SCRUM-22
- "No iOS, o comportamento é diferente: exibe um ícone quebrado, mas não trava." — fonte(s): SCRUM-22
- "BUG-07 (SCRUM-29, tarefas pendentes)" — fonte(s): SCRUM-29
- "ao inserir um código de cupom inválido, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "O app exibe a mensagem genérica "Erro inesperado. Tente novamente."" — fonte(s): SCRUM-29