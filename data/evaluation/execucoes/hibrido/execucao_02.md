# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

### Autenticação e Cadastro
A funcionalidade de Autenticação e Cadastro é a porta de entrada do aplicativo, impactando diretamente a experiência inicial do usuário. Ela agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

### Catálogo de Restaurantes
O Catálogo de Restaurantes abrange a exibição, busca e filtragem de restaurantes e seus cardápios. O usuário pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

### Carrinho e Pedidos
O Carrinho e Pedidos é o núcleo do aplicativo, cobrindo todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É onde a conversão de interesse em compra acontece.

### Pagamentos
A funcionalidade de Pagamentos é responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

### Rastreamento de Entrega
O Rastreamento de Entrega permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

### Avaliações
As Avaliações permitem que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Cadastro e Login

- **Cadastro com e-mail e senha**: os usuários novos podem se cadastrar com e-mail e senha, preenchendo nome completo, e-mail e senha. O sistema valida o e-mail e a senha, e envia um e-mail de confirmação.
- **Login com Google**: os usuários podem fazer login com sua conta Google, sendo redirecionados para o fluxo de autenticação OAuth do Google. Após a autenticação, uma conta é criada automaticamente com os dados do perfil Google.
- **Redefinição de senha**: os usuários podem redefinir sua senha por e-mail, clicando em "Esqueci minha senha" na tela de login, informando seu e-mail e recebendo um link de redefinição.

### Busca e Filtro

- **Busca de restaurantes por nome**: os usuários podem buscar restaurantes pelo nome, acessando o campo de busca e digitando o nome (parcial ou completo) do restaurante. O sistema retorna resultados em tempo real com debounce de 300ms.
- **Filtro por categoria**: os usuários podem filtrar restaurantes por categoria de culinária, visualizando chips horizontais com as categorias disponíveis. Ao selecionar uma categoria, a lista de restaurantes é filtrada automaticamente.

### Visualização e Adição de Itens

- **Visualização do cardápio**: os usuários podem ver o cardápio completo de um restaurante, acessando a página de detalhes com banner, informações do estabelecimento e o cardápio organizado por seções. Cada item exibe nome, foto, descrição curta e preço.
- **Adicionar itens ao carrinho**: os usuários podem adicionar itens ao carrinho, clicando em um item do cardápio e confirmando. O item é adicionado ao carrinho e um indicador flutuante com o total aparece na tela.

### Pagamento e Cancelamento

- **Pagamento com Pix**: os usuários podem pagar com Pix, selecionando Pix como método de pagamento e gerando um QR Code com validade de 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela.
- **Pagamento com cartão de crédito**: os usuários podem pagar com cartão de crédito, selecionando "Cartão de Crédito" e inserindo os dados do cartão em um formulário tokenizado. O sistema exibe as bandeiras aceitas e processa o pagamento, exibindo o resultado imediatamente.
- **Cancelamento de pedido**: os usuários podem cancelar seu pedido antes que ele seja aceito pelo restaurante, acessando a tela de acompanhamento e clicando em "Cancelar Pedido". O estorno é processado automaticamente para o método de pagamento utilizado.

### Acompanhamento e Avaliação

- **Acompanhamento de status do pedido**: os usuários podem acompanhar o status do seu pedido em tempo real, acessando uma tela de acompanhamento com linha do tempo visual mostrando as etapas. Cada etapa é atualizada via WebSocket em tempo real.
- **Rastreamento do entregador no mapa**: os usuários podem ver a localização do entregador em tempo real no mapa, após o pedido entrar no status "Saiu para Entrega". A posição do entregador é atualizada a cada 10 segundos via WebSocket.
- **Notificação de saída para entrega**: os usuários recebem uma notificação push quando seu pedido sai para entrega, com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento.
- **Avaliação do restaurante**: os usuários podem avaliar o restaurante após receber seu pedido, atribuindo de 1 a 5 estrelas e adicionando um comentário opcional de até 300 caracteres. A média de avaliações do restaurante é atualizada em tempo real.

### Cupom de Desconto

- **Aplicar cupom de desconto**: os usuários podem aplicar um cupom de desconto no seu pedido, digitando o código do cupom em um campo dedicado e clicando em "Aplicar". O sistema valida o cupom e exibe o desconto aplicado no resumo do pedido.

## Tarefas Operacionais

### Modo escuro

O app atualmente só suporta tema claro, mas a melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar último endereço de entrega automaticamente

Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de erro sem conexão com internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente", sem aguardar o timeout da requisição.

### Skeleton loading nas telas de lista

Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22)

Status: Tarefas pendentes. O app trava ao tentar adicionar um item sem imagem ao carrinho, exibindo uma tela branca. O problema ocorre porque o componente de imagem não trata URLs nulas.

### BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23)

Status: Tarefas pendentes. O filtro de categoria não é resetado ao voltar para a tela inicial, exibindo todos os restaurantes sem filtro aplicado.

### BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25)

Status: Tarefas pendentes. O valor do frete é somado em dobro no resumo do pedido, impactando a confiança do usuário, embora o valor cobrado no pagamento seja o correto.

### BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26)

Status: Tarefas pendentes. As notificações push de mudança de status do pedido chegam com atraso de 5 minutos, impactando a percepção de tempo real do acompanhamento.

### BUG-05 — Login com Google falha em Android 10 (SCRUM-27)

Status: Tarefas pendentes. O login com Google falha em dispositivos Android 10, exibindo a mensagem "Falha na autenticação. Tente novamente." sem mais detalhes.

### BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28)

Status: Tarefas pendentes. A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos, comprometendo a funcionalidade core de rastreamento.

### BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29)

Status: Tarefas pendentes. Ao inserir um código de cupom inválido, a API retorna HTTP 500 em vez de HTTP 422 com mensagem de erro adequada. O app exibe a mensagem genérica "Erro inesperado. Tente novamente."


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "porta de entrada do aplicativo" — fonte(s): SCRUM-1
- "impactando diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma" — fonte(s): SCRUM-1
- "criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "exibição, busca e filtragem de restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir" — fonte(s): SCRUM-2
- "informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "núcleo do aplicativo" — fonte(s): SCRUM-3
- "todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "responsável por todas as formas de pagamento disponíveis na plataforma" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "usuários novos" — fonte(s): SCRUM-7
- "cadastrar com e-mail e senha" — fonte(s): SCRUM-7
- "preenchendo nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "sistema valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "Login com Google" — fonte(s): SCRUM-8
- "fazer login com sua conta Google" — fonte(s): SCRUM-8
- "redirecionados para o fluxo de autenticação OAuth do Google." — fonte(s): SCRUM-8
- "autenticação" — fonte(s): SCRUM-8
- "uma conta é criada automaticamente com os dados do perfil Google." — fonte(s): SCRUM-8
- "Redefinição de senha" — fonte(s): SCRUM-9
- "redefinir sua senha por e-mail" — fonte(s): SCRUM-9
- ""Esqueci minha senha"" — fonte(s): SCRUM-9
- "tela de login" — fonte(s): SCRUM-9
- "informando seu e-mail" — fonte(s): SCRUM-9
- "recebendo um link de redefinição." — fonte(s): SCRUM-9
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "buscar restaurantes pelo nome" — fonte(s): SCRUM-10
- "acessando o campo de busca" — fonte(s): SCRUM-10
- "digitando o nome (parcial ou completo) do restaurante." — fonte(s): SCRUM-10
- "sistema retorna resultados em tempo real" — fonte(s): SCRUM-10
- "debounce de 300ms." — fonte(s): SCRUM-10
- "Filtro por categoria" — fonte(s): SCRUM-11
- "filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "visualizando chips horizontais com as categorias disponíveis." — fonte(s): SCRUM-11
- "selecionar uma categoria" — fonte(s): SCRUM-11
- "lista de restaurantes é filtrada automaticamente." — fonte(s): SCRUM-11
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "ver o cardápio completo de um restaurante" — fonte(s): SCRUM-12
- "acessando a página de detalhes" — fonte(s): SCRUM-12
- "banner, informações do estabelecimento e o cardápio organizado por seções." — fonte(s): SCRUM-12
- "Cada item exibe nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "clicando em um item do cardápio" — fonte(s): SCRUM-13
- "confirmando." — fonte(s): SCRUM-13
- "item é adicionado ao carrinho" — fonte(s): SCRUM-13
- "um indicador flutuante com o total aparece na tela." — fonte(s): SCRUM-13
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "pagar com Pix" — fonte(s): SCRUM-18
- "selecionando Pix como método de pagamento" — fonte(s): SCRUM-18
- "gerando um QR Code com validade de 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela." — fonte(s): SCRUM-18
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "pagar com cartão de crédito" — fonte(s): SCRUM-17
- "selecionando "Cartão de Crédito"" — fonte(s): SCRUM-17
- "inserindo os dados do cartão em um formulário tokenizado." — fonte(s): SCRUM-17
- "sistema exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "processa o pagamento" — fonte(s): SCRUM-17
- "exibindo o resultado imediatamente." — fonte(s): SCRUM-17
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "cancelar seu pedido" — fonte(s): SCRUM-16
- "ele seja aceito pelo restaurante" — fonte(s): SCRUM-16
- "acessando a tela de acompanhamento" — fonte(s): SCRUM-16
- "clicando em "Cancelar Pedido"" — fonte(s): SCRUM-16
- "estorno é processado automaticamente" — fonte(s): SCRUM-16
- "método de pagamento utilizado." — fonte(s): SCRUM-16
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "acompanhar o status do seu pedido em tempo real" — fonte(s): SCRUM-15
- "acessando uma tela de acompanhamento" — fonte(s): SCRUM-15
- "linha do tempo visual mostrando as etapas." — fonte(s): SCRUM-15
- "etapa é atualizada via WebSocket em tempo real." — fonte(s): SCRUM-15
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "ver a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "pedido entrar no status "Saiu para Entrega"" — fonte(s): SCRUM-19
- "posição do entregador é atualizada a cada 10 segundos via WebSocket." — fonte(s): SCRUM-19
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "recebem uma notificação push" — fonte(s): SCRUM-20
- "seu pedido sai para entrega" — fonte(s): SCRUM-20
- "nome do restaurante" — fonte(s): SCRUM-20
- "tempo estimado de entrega" — fonte(s): SCRUM-20
- "link direto para a tela de rastreamento." — fonte(s): SCRUM-20
- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "avaliar o restaurante após receber seu pedido" — fonte(s): SCRUM-21
- "atribuindo de 1 a 5 estrelas" — fonte(s): SCRUM-21
- "adicionando um comentário opcional de até 300 caracteres." — fonte(s): SCRUM-21
- "média de avaliações do restaurante é atualizada em tempo real." — fonte(s): SCRUM-21
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "aplicar um cupom de desconto no seu pedido" — fonte(s): SCRUM-14
- "digitando o código do cupom em um campo dedicado" — fonte(s): SCRUM-14
- "clicando em "Aplicar"" — fonte(s): SCRUM-14
- "sistema valida o cupom" — fonte(s): SCRUM-14
- "exibe o desconto aplicado no resumo do pedido." — fonte(s): SCRUM-14

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "O app atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "melhoria consiste em implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema" — fonte(s): SCRUM-33
- "opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido." — fonte(s): SCRUM-32
- "melhoria consiste em salvar automaticamente o último endereço utilizado" — fonte(s): SCRUM-32
- "pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente" — fonte(s): SCRUM-31
- "exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "sem aguardar o timeout da requisição." — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30