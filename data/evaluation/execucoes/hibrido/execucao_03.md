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
O EP-05 permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

# Avaliações
O EP-06 permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Avaliação do restaurante

Após o pedido ser entregue, o usuário pode avaliar o restaurante com notas de 1 a 5 estrelas e adicionar um comentário opcional. A média de avaliações é atualizada em tempo real.

### Notificação de saída para entrega

O sistema envia uma notificação push ao usuário quando o pedido sai para entrega, com informações como o nome do restaurante, tempo estimado e um link para rastreamento.

### Rastreamento do entregador no mapa

O usuário pode acompanhar a localização do entregador em tempo real no mapa, com atualizações a cada 10 segundos. O trajeto estimado é exibido e o tempo restante é recalculado dinamicamente.

### Pagamento com Pix

O usuário seleciona Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela após a confirmação.

### Pagamento com cartão de crédito

Na tela de checkout, o usuário seleciona cartão de crédito e insere os dados do cartão em um formulário seguro. O sistema exibe as bandeiras aceitas e processa o pagamento, exibindo o resultado imediatamente.

### Cancelamento de pedido

Enquanto o pedido estiver no status "Pedido Recebido", o usuário pode cancelá-lo informando o motivo e confirmando. O estorno é processado automaticamente e um e-mail de confirmação é enviado.

### Acompanhamento de status do pedido

Após confirmar o pedido, o usuário pode acompanhar seu status em tempo real, com atualizações via WebSocket e notificações push em cada mudança.

### Aplicar cupom de desconto

O usuário digita o código do cupom na tela de checkout e o sistema valida sua existência, validade e valor mínimo. O desconto é exibido no resumo do pedido.

### Adicionar itens ao carrinho

O usuário clica em um item do cardápio e uma bottom sheet é exibida com opções de personalização. Ao confirmar, o item é adicionado ao carrinho e um indicador flutuante mostra o total.

### Visualização do cardápio

Ao clicar em um restaurante, o usuário acessa sua página de detalhes com informações e o cardápio organizado por seções. Itens indisponíveis são exibidos como desabilitados.

### Filtro por categoria

Na tela principal, o usuário visualiza categorias disponíveis e pode selecionar múltiplas simultaneamente. O filtro é destacado visualmente e pode ser removido individualmente.

### Busca de restaurantes por nome

O usuário acessa o campo de busca e digita o nome do restaurante. O sistema retorna resultados em tempo real com debounce de 300ms e exibe nome, foto, avaliação e tempo de entrega.

### Redefinição de senha

O usuário clica em "Esqueci minha senha", informa seu e-mail e recebe um link de redefinição válido por 30 minutos. Após redefinição, todas as sessões ativas são encerradas.

### Login com Google

O usuário clica em "Entrar com Google" e é redirecionado para o fluxo de autenticação OAuth. Após autenticação bem-sucedida, uma conta é criada automaticamente ou o usuário é autenticado diretamente.

### Cadastro com e-mail e senha

O usuário acessa a tela de cadastro e preenche nome completo, e-mail e senha. O sistema valida o e-mail e a senha e envia um e-mail de confirmação. O cadastro é ativado após a confirmação.

## Tarefas Operacionais

### Modo Escuro

O app atualmente só suporta tema claro, mas a melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar Último Endereço de Entrega Automaticamente

Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de Erro sem Conexão com Internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente".

### Skeleton Loading nas Telas de Lista

Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### Problemas com severidade alta

- BUG-01 (SCRUM-22): o app trava ao adicionar um item sem foto ao carrinho. O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada.
- BUG-04 (SCRUM-25): o valor do frete é somado em dobro no resumo do pedido. A taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto.
- BUG-06 (SCRUM-28): a tela de rastreamento não atualiza a posição do entregador automaticamente após a tela ficar aberta por mais de 2 minutos. A conexão WebSocket é encerrada por inatividade e o app não implementa reconexão automática.
- BUG-05 (SCRUM-27): o login com Google falha em dispositivos Android 10 (API 29). O fluxo OAuth redireciona corretamente para a tela de seleção de conta Google, mas ao retornar ao app exibe a mensagem "Falha na autenticação. Tente novamente." sem mais detalhes.

### Problemas com severidade média

- BUG-07 (SCRUM-29): um cupom inválido retorna erro 500. Ao inserir um código de cupom que não existe no sistema, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada.
- BUG-03 (SCRUM-26): a notificação de pedido chega com atraso de aproximadamente 5 minutos. As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status.
- BUG-02 (SCRUM-23): o filtro de categoria não reseta ao voltar para a tela inicial. Quando o usuário seleciona uma categoria, navega para um restaurante e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado.


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
- "acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "EP-06" — fonte(s): SCRUM-6
- "expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "Após o pedido ser entregue" — fonte(s): SCRUM-21
- "avaliar o restaurante com notas de 1 a 5 estrelas" — fonte(s): SCRUM-21
- "adicionar um comentário opcional." — fonte(s): SCRUM-21
- "A média de avaliações é atualizada em tempo real." — fonte(s): SCRUM-21
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "envia uma notificação push ao usuário quando o pedido sai para entrega" — fonte(s): SCRUM-20
- "o nome do restaurante, tempo estimado e um link para rastreamento." — fonte(s): SCRUM-20
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "acompanhar a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "atualizações a cada 10 segundos." — fonte(s): SCRUM-19
- "O trajeto estimado é exibido e o tempo restante é recalculado dinamicamente." — fonte(s): SCRUM-19
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "seleciona Pix como método de pagamento" — fonte(s): SCRUM-18
- "um QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "O app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela após a confirmação." — fonte(s): SCRUM-18
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "Na tela de checkout" — fonte(s): SCRUM-17
- "seleciona cartão de crédito e insere os dados do cartão em um formulário seguro." — fonte(s): SCRUM-17
- "exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "processa o pagamento" — fonte(s): SCRUM-17
- "exibindo o resultado imediatamente." — fonte(s): SCRUM-17
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "Enquanto o pedido estiver no status "Pedido Recebido"" — fonte(s): SCRUM-16
- "cancelá-lo informando o motivo e confirmando." — fonte(s): SCRUM-16
- "O estorno é processado automaticamente" — fonte(s): SCRUM-16
- "um e-mail de confirmação é enviado." — fonte(s): SCRUM-16
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "Após confirmar o pedido" — fonte(s): SCRUM-15
- "acompanhar seu status em tempo real" — fonte(s): SCRUM-15
- "atualizações via WebSocket" — fonte(s): SCRUM-15
- "notificações push em cada mudança." — fonte(s): SCRUM-15
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "digita o código do cupom na tela de checkout" — fonte(s): SCRUM-14
- "valida sua existência, validade e valor mínimo." — fonte(s): SCRUM-14
- "O desconto é exibido no resumo do pedido." — fonte(s): SCRUM-14
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "clica em um item do cardápio" — fonte(s): SCRUM-13
- "uma bottom sheet é exibida com opções de personalização." — fonte(s): SCRUM-13
- "Ao confirmar, o item é adicionado ao carrinho" — fonte(s): SCRUM-13
- "um indicador flutuante mostra o total." — fonte(s): SCRUM-13
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "Ao clicar em um restaurante" — fonte(s): SCRUM-12
- "acessa sua página de detalhes com informações e o cardápio organizado por seções." — fonte(s): SCRUM-12
- "Itens indisponíveis são exibidos como desabilitados." — fonte(s): SCRUM-12
- "Filtro por categoria" — fonte(s): SCRUM-11
- "Na tela principal" — fonte(s): SCRUM-11
- "visualiza categorias disponíveis" — fonte(s): SCRUM-11
- "selecionar múltiplas simultaneamente." — fonte(s): SCRUM-11
- "O filtro é destacado visualmente e pode ser removido individualmente." — fonte(s): SCRUM-11
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "acessa o campo de busca e digita o nome do restaurante." — fonte(s): SCRUM-10
- "retorna resultados em tempo real com debounce de 300ms" — fonte(s): SCRUM-10
- "exibe nome, foto, avaliação e tempo de entrega." — fonte(s): SCRUM-10
- "Redefinição de senha" — fonte(s): SCRUM-9
- "clica em "Esqueci minha senha"" — fonte(s): SCRUM-9
- "informa seu e-mail e recebe um link de redefinição válido por 30 minutos." — fonte(s): SCRUM-9
- "Após redefinição, todas as sessões ativas são encerradas." — fonte(s): SCRUM-9
- "Login com Google" — fonte(s): SCRUM-8
- "clica em "Entrar com Google"" — fonte(s): SCRUM-8
- "redirecionado para o fluxo de autenticação OAuth." — fonte(s): SCRUM-8
- "Após autenticação bem-sucedida, uma conta é criada automaticamente ou o usuário é autenticado diretamente." — fonte(s): SCRUM-8
- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "acessa a tela de cadastro e preenche nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "O cadastro é ativado após a confirmação." — fonte(s): SCRUM-7

**Tarefas Operacionais:**

- "Modo Escuro" — fonte(s): SCRUM-33
- "O app atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "melhoria consiste em implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar Último Endereço de Entrega Automaticamente" — fonte(s): SCRUM-32
- "Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido." — fonte(s): SCRUM-32
- "melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de Erro sem Conexão com Internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton Loading nas Telas de Lista" — fonte(s): SCRUM-30
- "Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-01 (SCRUM-22)" — fonte(s): SCRUM-22
- "app trava" — fonte(s): SCRUM-22
- "adicionar um item sem foto ao carrinho." — fonte(s): SCRUM-22
- "componente de imagem não trata o caso de URL nula" — fonte(s): SCRUM-22
- "lançando uma exceção não tratada." — fonte(s): SCRUM-22
- "BUG-04 (SCRUM-25)" — fonte(s): SCRUM-25
- "valor do frete é somado em dobro no resumo do pedido." — fonte(s): SCRUM-25
- "taxa de entrega é exibida corretamente no campo "Entrega"" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total ficar incorreto." — fonte(s): SCRUM-25
- "BUG-06 (SCRUM-28)" — fonte(s): SCRUM-28
- "tela de rastreamento não atualiza a posição do entregador automaticamente" — fonte(s): SCRUM-28
- "tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "conexão WebSocket é encerrada por inatividade" — fonte(s): SCRUM-28
- "app não implementa reconexão automática." — fonte(s): SCRUM-28
- "BUG-05 (SCRUM-27)" — fonte(s): SCRUM-27
- "login com Google falha em dispositivos Android 10 (API 29)" — fonte(s): SCRUM-27
- "fluxo OAuth redireciona corretamente para a tela de seleção de conta Google" — fonte(s): SCRUM-27
- "retornar ao app exibe a mensagem "Falha na autenticação. Tente novamente."" — fonte(s): SCRUM-27
- "BUG-07 (SCRUM-29)" — fonte(s): SCRUM-29
- "cupom inválido retorna erro 500." — fonte(s): SCRUM-29
- "inserir um código de cupom que não existe no sistema" — fonte(s): SCRUM-29
- "API retorna HTTP 500 (Internal Server Error)" — fonte(s): SCRUM-29
- "HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "BUG-03 (SCRUM-26)" — fonte(s): SCRUM-26
- "notificação de pedido chega com atraso de aproximadamente 5 minutos." — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "BUG-02 (SCRUM-23)" — fonte(s): SCRUM-23
- "filtro de categoria não reseta ao voltar para a tela inicial." — fonte(s): SCRUM-23
- "usuário seleciona uma categoria, navega para um restaurante e volta para a tela inicial" — fonte(s): SCRUM-23
- "filtro permanece ativo visualmente" — fonte(s): SCRUM-23
- "lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23