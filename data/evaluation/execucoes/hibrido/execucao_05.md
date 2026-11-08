# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

# Autenticação e Cadastro
A porta de entrada do app, impactando diretamente a experiência inicial do usuário. Agrupa funcionalidades de acesso à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

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

### Avaliação do restaurante

Após receber seu pedido, você pode avaliar o restaurante, atribuindo de 1 a 5 estrelas e adicionando um comentário opcional. A avaliação é vinculada ao pedido e a média do restaurante é atualizada em tempo real.

### Notificação de saída para entrega

Quando seu pedido sai para entrega, você recebe uma notificação push com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento. A notificação é enviada mesmo com o app em segundo plano ou fechado.

### Rastreamento do entregador no mapa

Após o pedido sair para entrega, você pode acompanhar a localização do entregador em tempo real no mapa, junto com a posição do restaurante e o endereço de entrega. A posição do entregador é atualizada a cada 10 segundos e o trajeto estimado é exibido no mapa.

### Pagamento com Pix

Para finalizar o pedido instantaneamente, você pode pagar com Pix. Um QR Code é gerado com validade de 10 minutos e o pagamento é monitorado em tempo real. Se o QR Code expirar, você pode gerar um novo.

### Pagamento com cartão de crédito

Na tela de checkout, você seleciona "Cartão de Crédito" e insere os dados do cartão em um formulário tokenizado. O sistema exibe as bandeiras aceitas e, após confirmação, processa o pagamento, exibindo imediatamente o resultado (aprovado ou recusado).

### Cancelamento de pedido

Enquanto o pedido estiver no status "Pedido Recebido", você pode cancelá-lo informando o motivo (campo obrigatório com opções pré-definidas). O estorno é processado automaticamente para o método de pagamento utilizado em até 5 dias úteis e um e-mail de confirmação é enviado.

### Acompanhamento de status do pedido

Após confirmar o pedido, você pode acompanhar seu status em tempo real, visualizando as etapas: Pedido Recebido, Confirmado pelo Restaurante, Em Preparo, Saiu para Entrega e Entregue. Cada etapa é atualizada via WebSocket e o tempo estimado de entrega é exibido e atualizado dinamicamente.

### Aplicar cupom de desconto

Na tela de checkout, você digita o código do cupom e clica em "Aplicar". O sistema valida o cupom e exibe o desconto aplicado no resumo do pedido. Se o cupom for inválido, uma mensagem específica informa o motivo.

### Adicionar itens ao carrinho

Para montar seu pedido, você clica em um item do cardápio e uma bottom sheet é exibida com opções de personalização e quantidade. Ao confirmar, o item é adicionado ao carrinho e um indicador flutuante com o total aparece na tela.

### Visualização do cardápio

Ao clicar em um restaurante, você acessa a página de detalhes com o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço, e os indisponíveis aparecem como desabilitados.

### Filtro por categoria

Na tela principal, você visualiza chips horizontais com as categorias disponíveis. Ao selecionar uma ou mais categorias, a lista de restaurantes é filtrada automaticamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

### Busca de restaurantes por nome

Na tela principal, você acessa o campo de busca e digita o nome (parcial ou completo) do restaurante. O sistema retorna resultados em tempo real com debounce de 300ms para evitar requisições excessivas.

### Redefinição de senha

Se você esquecer sua senha, pode clicar em "Esqueci minha senha" na tela de login, informar seu e-mail e receber um link de redefinição válido por 30 minutos. Após redefinição, todas as sessões ativas são encerradas por segurança.

### Login com Google

Para acessar o app sem precisar criar uma senha, você pode clicar em "Entrar com Google" na tela de login e ser redirecionado para o fluxo de autenticação OAuth do Google. Após autenticação bem-sucedida, se for o primeiro acesso, uma conta é criada automaticamente com seus dados do perfil Google.

### Cadastro com e-mail e senha

Se você é um usuário novo, pode acessar a tela de cadastro e preencher nome completo, e-mail e senha. O sistema valida se o e-mail já está cadastrado e se a senha atende aos requisitos mínimos. Somente após confirmar o e-mail o cadastro é ativado.

## Tarefas Operacionais

### Modo Escuro

O app atualmente só suporta tema claro, mas a implementação do modo escuro seguirá as diretrizes de design do sistema operacional, com detecção automática da preferência do sistema e opção manual de alternar nas configurações.

### Salvar Último Endereço de Entrega Automaticamente

O usuário precisa digitar o endereço de entrega em cada novo pedido, mas a melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de Erro sem Conexão com Internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente".

### Skeleton Loading nas Telas de Lista

Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes)

O aplicativo trava ao adicionar um item sem foto ao carrinho, exibindo uma tela branca. Isso ocorre porque o componente de imagem não trata URLs nulas, lançando uma exceção não tratada.

### BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes)

O filtro de categoria não é resetado ao voltar para a tela inicial, exibindo todos os restaurantes sem filtro aplicado. Há uma inconsistência entre o estado visual do chip e o estado real da filtragem.

### BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes)

O valor do frete é somado em dobro no resumo do pedido, mas o valor cobrado no pagamento é o correto. O problema está apenas na exibição do resumo.

### BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes)

As notificações push de mudança de status do pedido chegam com atraso de cerca de 5 minutos após a mudança real de status. Isso ocorre porque o job de envio de notificações roda em intervalo fixo de 5 minutos, em vez de ser disparado por evento.

### BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes)

O login com Google falha em dispositivos Android 10 (API 29). O fluxo OAuth redireciona corretamente para a tela de seleção de conta Google, mas ao retornar ao app exibe uma mensagem de erro sem detalhes.

### BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes)

A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes)

Ao inserir um código de cupom inválido, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada. O app exibe uma mensagem genérica de erro.


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "A porta de entrada do app, impactando diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "Agrupa funcionalidades de acesso à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "Exibe, busca e filtra restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "O usuário pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "O núcleo do app, onde a conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "Permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Após receber seu pedido" — fonte(s): SCRUM-21
- "avaliar o restaurante" — fonte(s): SCRUM-21
- "atribuindo de 1 a 5 estrelas" — fonte(s): SCRUM-21
- "adicionando um comentário opcional." — fonte(s): SCRUM-21
- "A avaliação é vinculada ao pedido" — fonte(s): SCRUM-21
- "a média do restaurante é atualizada em tempo real." — fonte(s): SCRUM-21
- "Quando seu pedido sai para entrega" — fonte(s): SCRUM-20
- "recebe uma notificação push" — fonte(s): SCRUM-20
- "o nome do restaurante" — fonte(s): SCRUM-20
- "o tempo estimado de entrega" — fonte(s): SCRUM-20
- "um link direto para a tela de rastreamento." — fonte(s): SCRUM-20
- "A notificação é enviada mesmo com o app em segundo plano ou fechado." — fonte(s): SCRUM-20
- "Após o pedido sair para entrega" — fonte(s): SCRUM-19
- "acompanhar a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "a posição do restaurante e o endereço de entrega." — fonte(s): SCRUM-19
- "A posição do entregador é atualizada a cada 10 segundos" — fonte(s): SCRUM-19
- "o trajeto estimado é exibido no mapa." — fonte(s): SCRUM-19
- "finalizar o pedido instantaneamente" — fonte(s): SCRUM-18
- "pagar com Pix." — fonte(s): SCRUM-18
- "Um QR Code é gerado com validade de 10 minutos" — fonte(s): SCRUM-18
- "o pagamento é monitorado em tempo real." — fonte(s): SCRUM-18
- "Se o QR Code expirar, você pode gerar um novo." — fonte(s): SCRUM-18
- "Na tela de checkout" — fonte(s): SCRUM-17
- "seleciona "Cartão de Crédito"" — fonte(s): SCRUM-17
- "insere os dados do cartão em um formulário tokenizado." — fonte(s): SCRUM-17
- "O sistema exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "após confirmação" — fonte(s): SCRUM-17
- "processa o pagamento" — fonte(s): SCRUM-17
- "exibindo imediatamente o resultado (aprovado ou recusado)" — fonte(s): SCRUM-17
- "Enquanto o pedido estiver no status "Pedido Recebido"" — fonte(s): SCRUM-16
- "cancelá-lo" — fonte(s): SCRUM-16
- "informando o motivo (campo obrigatório com opções pré-definidas)" — fonte(s): SCRUM-16
- "O estorno é processado automaticamente para o método de pagamento utilizado em até 5 dias úteis" — fonte(s): SCRUM-16
- "um e-mail de confirmação é enviado." — fonte(s): SCRUM-16
- "Após confirmar o pedido" — fonte(s): SCRUM-15
- "acompanhar seu status em tempo real" — fonte(s): SCRUM-15
- "visualizando as etapas: Pedido Recebido, Confirmado pelo Restaurante, Em Preparo, Saiu para Entrega e Entregue." — fonte(s): SCRUM-15
- "Cada etapa é atualizada via WebSocket" — fonte(s): SCRUM-15
- "o tempo estimado de entrega é exibido e atualizado dinamicamente." — fonte(s): SCRUM-15
- "Na tela de checkout" — fonte(s): SCRUM-14
- "digita o código do cupom e clica em "Aplicar"" — fonte(s): SCRUM-14
- "O sistema valida o cupom" — fonte(s): SCRUM-14
- "exibe o desconto aplicado no resumo do pedido." — fonte(s): SCRUM-14
- "Se o cupom for inválido, uma mensagem específica informa o motivo." — fonte(s): SCRUM-14
- "montar seu pedido" — fonte(s): SCRUM-13
- "clica em um item do cardápio" — fonte(s): SCRUM-13
- "uma bottom sheet é exibida com opções de personalização e quantidade." — fonte(s): SCRUM-13
- "Ao confirmar, o item é adicionado ao carrinho" — fonte(s): SCRUM-13
- "um indicador flutuante com o total aparece na tela." — fonte(s): SCRUM-13
- "Ao clicar em um restaurante" — fonte(s): SCRUM-12
- "acessa a página de detalhes com o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "Cada item exibe nome, foto, descrição curta e preço" — fonte(s): SCRUM-12
- "os indisponíveis aparecem como desabilitados." — fonte(s): SCRUM-12
- "Na tela principal" — fonte(s): SCRUM-11
- "visualiza chips horizontais com as categorias disponíveis." — fonte(s): SCRUM-11
- "Ao selecionar uma ou mais categorias, a lista de restaurantes é filtrada automaticamente." — fonte(s): SCRUM-11
- "O filtro ativo é destacado visualmente e pode ser removido individualmente." — fonte(s): SCRUM-11
- "Na tela principal" — fonte(s): SCRUM-10
- "acessa o campo de busca e digita o nome (parcial ou completo) do restaurante." — fonte(s): SCRUM-10
- "O sistema retorna resultados em tempo real com debounce de 300ms para evitar requisições excessivas." — fonte(s): SCRUM-10
- "Se você esquecer sua senha" — fonte(s): SCRUM-9
- "clicar em "Esqueci minha senha" na tela de login" — fonte(s): SCRUM-9
- "informar seu e-mail e receber um link de redefinição válido por 30 minutos." — fonte(s): SCRUM-9
- "Após redefinição, todas as sessões ativas são encerradas por segurança." — fonte(s): SCRUM-9
- "acessar o app sem precisar criar uma senha" — fonte(s): SCRUM-8
- "clicar em "Entrar com Google" na tela de login" — fonte(s): SCRUM-8
- "redirecionado para o fluxo de autenticação OAuth do Google." — fonte(s): SCRUM-8
- "Após autenticação bem-sucedida, se for o primeiro acesso, uma conta é criada automaticamente com seus dados do perfil Google." — fonte(s): SCRUM-8
- "Se você é um usuário novo" — fonte(s): SCRUM-7
- "acessar a tela de cadastro e preencher nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "O sistema valida se o e-mail já está cadastrado e se a senha atende aos requisitos mínimos." — fonte(s): SCRUM-7
- "Somente após confirmar o e-mail o cadastro é ativado." — fonte(s): SCRUM-7

**Tarefas Operacionais:**

- "Modo Escuro" — fonte(s): SCRUM-33
- "O app atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "implementação do modo escuro seguirá as diretrizes de design do sistema operacional" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações." — fonte(s): SCRUM-33
- "Salvar Último Endereço de Entrega Automaticamente" — fonte(s): SCRUM-32
- "O usuário precisa digitar o endereço de entrega em cada novo pedido" — fonte(s): SCRUM-32
- "melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de Erro sem Conexão com Internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton Loading nas Telas de Lista" — fonte(s): SCRUM-30
- "Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado." — fonte(s): SCRUM-30
- "melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-01 — App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "(SCRUM-22, status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "O aplicativo trava ao adicionar um item sem foto ao carrinho, exibindo uma tela branca." — fonte(s): SCRUM-22
- "Isso ocorre porque o componente de imagem não trata URLs nulas, lançando uma exceção não tratada." — fonte(s): SCRUM-22
- "BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial" — fonte(s): SCRUM-23
- "(SCRUM-23, status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "O filtro de categoria não é resetado ao voltar para a tela inicial, exibindo todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "Há uma inconsistência entre o estado visual do chip e o estado real da filtragem." — fonte(s): SCRUM-23
- "BUG-03 — Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "(SCRUM-25, status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "O valor do frete é somado em dobro no resumo do pedido, mas o valor cobrado no pagamento é o correto." — fonte(s): SCRUM-25
- "O problema está apenas na exibição do resumo." — fonte(s): SCRUM-25
- "BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "(SCRUM-26, status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "As notificações push de mudança de status do pedido chegam com atraso de cerca de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "Isso ocorre porque o job de envio de notificações roda em intervalo fixo de 5 minutos, em vez de ser disparado por evento." — fonte(s): SCRUM-26
- "BUG-05 — Login com Google falha em Android 10" — fonte(s): SCRUM-27
- "(SCRUM-27, status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "O login com Google falha em dispositivos Android 10 (API 29)" — fonte(s): SCRUM-27
- "O fluxo OAuth redireciona corretamente para a tela de seleção de conta Google, mas ao retornar ao app exibe uma mensagem de erro sem detalhes." — fonte(s): SCRUM-27
- "BUG-06 — Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "(SCRUM-28, status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "BUG-07 — Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "(SCRUM-29, status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "Ao inserir um código de cupom inválido, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "O app exibe uma mensagem genérica de erro." — fonte(s): SCRUM-29