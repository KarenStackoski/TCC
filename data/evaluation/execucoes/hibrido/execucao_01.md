# Manual do Usuário

_Documento gerado automaticamente — Etapa 3 do TCC: Híbrido (estrutura fixa por template, texto de cada seção reescrito por LLM)._

## Visão Geral

# Autenticação e Cadastro
A porta de entrada do app, que impacta diretamente a experiência inicial do usuário. Agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil.

# Catálogo de Restaurantes
Engloba a exibição, busca e filtragem de restaurantes e seus cardápios. O usuário precisa encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

# Carrinho e Pedidos
É o núcleo do app, onde a conversão de interesse em compra acontece. Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido.

# Pagamentos
Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

# Rastreamento de Entrega
Permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

# Avaliações
Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## Funcionalidades

### Cadastro e login

- **Cadastro com e-mail e senha**: os usuários novos podem criar uma conta no app, preenchendo nome completo, e-mail e senha. O sistema valida o e-mail e a senha, e envia um e-mail de confirmação.
- **Login com Google**: os usuários podem acessar o app com sua conta Google, sem precisar criar uma senha. O fluxo OAuth funciona em iOS e Android.
- **Redefinição de senha**: os usuários podem redefinir sua senha por e-mail, clicando em "Esqueci minha senha" na tela de login. O link de redefinição é válido por 30 minutos.

### Busca e filtros

- **Busca de restaurantes por nome**: os usuários podem buscar restaurantes pelo nome, acessando o campo de busca na tela principal. O sistema retorna resultados em tempo real, com debounce de 300ms.
- **Filtro por categoria**: os usuários podem filtrar restaurantes por categoria de culinária, visualizando chips horizontais com as categorias disponíveis. É possível selecionar múltiplas categorias simultaneamente.

### Visualização e montagem do pedido

- **Visualização do cardápio**: os usuários podem ver o cardápio completo de um restaurante, organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço.
- **Adicionar itens ao carrinho**: os usuários podem clicar em um item do cardápio e adicioná-lo ao carrinho, com opções de personalização e quantidade. O carrinho só pode conter itens de um único restaurante por vez.
- **Aplicar cupom de desconto**: os usuários podem digitar o código do cupom na tela de checkout e aplicar o desconto no pedido. O sistema valida o cupom e exibe o desconto aplicado.

### Pagamento e cancelamento

- **Pagamento com Pix**: os usuários podem selecionar Pix como método de pagamento, e um QR Code é gerado com validade de 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela.
- **Pagamento com cartão de crédito**: os usuários podem selecionar "Cartão de Crédito" na tela de checkout e inserir os dados do cartão em um formulário tokenizado. O sistema exibe as bandeiras aceitas e processa o pagamento, exibindo o resultado imediatamente.
- **Cancelamento de pedido**: os usuários podem cancelar seu pedido na tela de acompanhamento, enquanto estiver no status "Pedido Recebido". É necessário informar o motivo do cancelamento e o estorno é processado automaticamente.

### Acompanhamento e avaliação

- **Acompanhamento de status do pedido**: os usuários podem acessar uma tela de acompanhamento com uma linha do tempo visual, mostrando as etapas do pedido em tempo real. O tempo estimado de entrega é exibido e atualizado dinamicamente.
- **Rastreamento do entregador no mapa**: os usuários podem ver a localização do entregador em tempo real no mapa, após o pedido entrar no status "Saiu para Entrega". A posição do entregador é atualizada a cada 10 segundos.
- **Notificação de saída para entrega**: os usuários recebem uma notificação push quando seu pedido sai para entrega, com o nome do restaurante, o tempo estimado e um link direto para a tela de rastreamento.
- **Avaliação do restaurante**: após o pedido ser marcado como entregue, os usuários recebem uma notificação convidando-os a avaliar. Na tela de avaliação, podem atribuir de 1 a 5 estrelas e adicionar um comentário opcional.

## Tarefas Operacionais

### Modo escuro
O app atualmente só suporta tema claro, mas a melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar último endereço de entrega automaticamente
Atualmente, o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de erro sem conexão com internet
Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão "Tentar novamente".

### Skeleton loading nas telas de lista
Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes)

Ao adicionar um item sem foto ao carrinho, o aplicativo trava e exibe uma tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada.

### BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes)

Quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado.

### BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes)

Na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.

### BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes)

As notificações push de mudança de status do pedido estão chegando com atraso de aproximadamente 5 minutos após a mudança real de status.

### BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes)

Ao tentar autenticar com Google em dispositivos Android 10, o fluxo OAuth redireciona corretamente para a tela de seleção de conta Google, mas ao retornar ao app exibe uma mensagem de erro sem mais detalhes.

### BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes)

A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes)

Ao inserir um código de cupom inválido, a API retorna um erro HTTP 500 em vez de um erro HTTP 422 com mensagem adequada. O app exibe uma mensagem genérica de erro.


---

**Citações (Cohere Command R):**

**Visão Geral:**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "porta de entrada do app" — fonte(s): SCRUM-1
- "impacta diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "Agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma" — fonte(s): SCRUM-1
- "criação de conta, login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "Engloba a exibição, busca e filtragem de restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "precisa encontrar facilmente o que deseja pedir" — fonte(s): SCRUM-2
- "informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "núcleo do app" — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "Responsável por todas as formas de pagamento disponíveis na plataforma" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "Permite ao usuário acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "usuários novos" — fonte(s): SCRUM-7
- "criar uma conta no app" — fonte(s): SCRUM-7
- "preenchendo nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "sistema valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "Login com Google" — fonte(s): SCRUM-8
- "acessar o app com sua conta Google" — fonte(s): SCRUM-8
- "sem precisar criar uma senha." — fonte(s): SCRUM-8
- "fluxo OAuth funciona em iOS e Android." — fonte(s): SCRUM-8
- "Redefinição de senha" — fonte(s): SCRUM-9
- "redefinir sua senha por e-mail" — fonte(s): SCRUM-9
- ""Esqueci minha senha" na tela de login." — fonte(s): SCRUM-9
- "link de redefinição é válido por 30 minutos." — fonte(s): SCRUM-9
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "buscar restaurantes pelo nome" — fonte(s): SCRUM-10
- "acessando o campo de busca na tela principal." — fonte(s): SCRUM-10
- "sistema retorna resultados em tempo real" — fonte(s): SCRUM-10
- "debounce de 300ms." — fonte(s): SCRUM-10
- "Filtro por categoria" — fonte(s): SCRUM-11
- "filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "visualizando chips horizontais com as categorias disponíveis." — fonte(s): SCRUM-11
- "possível selecionar múltiplas categorias simultaneamente." — fonte(s): SCRUM-11
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "ver o cardápio completo de um restaurante" — fonte(s): SCRUM-12
- "organizado por seções" — fonte(s): SCRUM-12
- "(Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "item exibe nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "clicar em um item do cardápio e adicioná-lo ao carrinho" — fonte(s): SCRUM-13
- "opções de personalização e quantidade." — fonte(s): SCRUM-13
- "carrinho só pode conter itens de um único restaurante por vez." — fonte(s): SCRUM-13
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "digitar o código do cupom na tela de checkout" — fonte(s): SCRUM-14
- "aplicar o desconto no pedido." — fonte(s): SCRUM-14
- "sistema valida o cupom" — fonte(s): SCRUM-14
- "exibe o desconto aplicado." — fonte(s): SCRUM-14
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "selecionar Pix como método de pagamento" — fonte(s): SCRUM-18
- "um QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela." — fonte(s): SCRUM-18
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "selecionar "Cartão de Crédito" na tela de checkout" — fonte(s): SCRUM-17
- "inserir os dados do cartão em um formulário tokenizado." — fonte(s): SCRUM-17
- "sistema exibe as bandeiras aceitas" — fonte(s): SCRUM-17
- "processa o pagamento" — fonte(s): SCRUM-17
- "exibindo o resultado imediatamente." — fonte(s): SCRUM-17
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "cancelar seu pedido na tela de acompanhamento" — fonte(s): SCRUM-16
- "estiver no status "Pedido Recebido"" — fonte(s): SCRUM-16
- "necessário informar o motivo do cancelamento" — fonte(s): SCRUM-16
- "estorno é processado automaticamente." — fonte(s): SCRUM-16
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "acessar uma tela de acompanhamento" — fonte(s): SCRUM-15
- "linha do tempo visual" — fonte(s): SCRUM-15
- "as etapas do pedido em tempo real." — fonte(s): SCRUM-15
- "tempo estimado de entrega é exibido e atualizado dinamicamente." — fonte(s): SCRUM-15
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "ver a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "o pedido entrar no status "Saiu para Entrega"" — fonte(s): SCRUM-19
- "posição do entregador é atualizada a cada 10 segundos." — fonte(s): SCRUM-19
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "recebem uma notificação push" — fonte(s): SCRUM-20
- "seu pedido sai para entrega" — fonte(s): SCRUM-20
- "o nome do restaurante, o tempo estimado e um link direto para a tela de rastreamento." — fonte(s): SCRUM-20
- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "o pedido ser marcado como entregue" — fonte(s): SCRUM-21
- "recebem uma notificação convidando-os a avaliar." — fonte(s): SCRUM-21
- "tela de avaliação" — fonte(s): SCRUM-21
- "atribuir de 1 a 5 estrelas e adicionar um comentário opcional." — fonte(s): SCRUM-21

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
- "tela amigável" — fonte(s): SCRUM-31
- "mensagem clara" — fonte(s): SCRUM-31
- "botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "carregar a lista de restaurantes ou o cardápio" — fonte(s): SCRUM-30
- "spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "substituir esse spinner por skeleton screens" — fonte(s): SCRUM-30
- "(placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento" — fonte(s): SCRUM-30
- "melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-01 — App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "(SCRUM-22, status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "Ao adicionar um item sem foto ao carrinho, o aplicativo trava e exibe uma tela branca." — fonte(s): SCRUM-22
- "O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada." — fonte(s): SCRUM-22
- "BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial" — fonte(s): SCRUM-23
- "(SCRUM-23, status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "Quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "BUG-03 — Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "(SCRUM-25, status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "Na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto." — fonte(s): SCRUM-25
- "BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "(SCRUM-26, status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "As notificações push de mudança de status do pedido estão chegando com atraso de aproximadamente 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "BUG-05 — Login com Google falha em Android 10" — fonte(s): SCRUM-27
- "(SCRUM-27, status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "Ao tentar autenticar com Google em dispositivos Android 10, o fluxo OAuth redireciona corretamente para a tela de seleção de conta Google, mas ao retornar ao app exibe uma mensagem de erro sem mais detalhes." — fonte(s): SCRUM-27
- "BUG-06 — Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "(SCRUM-28, status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "BUG-07 — Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "(SCRUM-29, status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "Ao inserir um código de cupom inválido, a API retorna um erro HTTP 500 em vez de um erro HTTP 422 com mensagem adequada. O app exibe uma mensagem genérica de erro." — fonte(s): SCRUM-29