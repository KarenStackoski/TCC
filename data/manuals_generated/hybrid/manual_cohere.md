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

### Cadastro e Login

- **Cadastro com e-mail e senha**: os usuários novos podem criar uma conta no app, inserindo nome completo, e-mail e senha. O sistema valida o e-mail e a senha, e envia um e-mail de confirmação.
- **Login com Google**: os usuários podem acessar o app usando sua conta Google, sem precisar criar uma senha. O fluxo OAuth funciona em iOS e Android.
- **Redefinição de senha**: os usuários podem redefinir sua senha por e-mail, recebendo um link de redefinição válido por 30 minutos. Após a redefinição, todas as sessões ativas são encerradas.

### Busca e Filtro

- **Busca de restaurantes por nome**: os usuários podem buscar restaurantes pelo nome, com resultados exibidos em tempo real. O sistema retorna nome, foto, avaliação e tempo estimado de entrega.
- **Filtro por categoria**: os usuários podem filtrar restaurantes por categoria de culinária, selecionando múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

### Visualização e Montagem do Pedido

- **Visualização do cardápio**: os usuários podem ver o cardápio completo de um restaurante, organizado por seções, com foto, descrição curta e preço de cada item.
- **Adicionar itens ao carrinho**: os usuários podem clicar em um item do cardápio e adicioná-lo ao carrinho, com opções de personalização e quantidade. O carrinho só pode conter itens de um único restaurante por vez.
- **Aplicar cupom de desconto**: os usuários podem digitar o código do cupom e aplicá-lo ao pedido, com validação em tempo real e desconto exibido de forma destacada.

### Acompanhamento e Pagamento

- **Acompanhamento de status do pedido**: os usuários podem acessar uma tela de acompanhamento com linha do tempo visual, mostrando as etapas do pedido em tempo real.
- **Pagamento com cartão de crédito**: os usuários podem selecionar "Cartão de Crédito" e inserir os dados do cartão em um formulário tokenizado, com feedback imediato de aprovação ou recusa.
- **Pagamento com Pix**: os usuários podem selecionar Pix como método de pagamento, com um QR Code válido por 10 minutos e monitoramento em tempo real do pagamento.

### Entrega e Avaliação

- **Cancelamento de pedido**: os usuários podem cancelar seu pedido enquanto estiver no status "Pedido Recebido", informando o motivo do cancelamento e recebendo um e-mail de confirmação.
- **Notificação de saída para entrega**: os usuários recebem uma notificação push quando seu pedido sai para entrega, com o nome do restaurante, tempo estimado e link para a tela de rastreamento.
- **Rastreamento do entregador no mapa**: os usuários podem ver a localização do entregador em tempo real no mapa, com o trajeto estimado e o tempo restante recalculados dinamicamente.
- **Avaliação do restaurante**: após o pedido ser marcado como entregue, os usuários recebem uma notificação convidando-os a avaliar, atribuindo de 1 a 5 estrelas e adicionando um comentário opcional.

## Tarefas Operacionais

### Modo escuro

Atualmente, o aplicativo só suporta tema claro. A implementação do modo escuro seguirá as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

### Salvar último endereço de entrega automaticamente

O usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar.

### Mensagem de erro sem conexão com internet

Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente".

### Skeleton loading nas telas de lista

Ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual.

## Problemas Conhecidos

### BUG-01 — App trava ao adicionar item sem foto ao carrinho (SCRUM-22, status: Tarefas pendentes)

O aplicativo para de responder e exibe uma tela branca ao tentar adicionar um item sem imagem ao carrinho. O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada.

### BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (SCRUM-23, status: Tarefas pendentes)

Quando o usuário seleciona uma categoria e volta para a tela inicial, o filtro permanece ativo visualmente, mas a lista exibe todos os restaurantes sem filtro aplicado.

### BUG-03 — Valor do frete somando em dobro no resumo do pedido (SCRUM-25, status: Tarefas pendentes)

Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.

### BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (SCRUM-26, status: Tarefas pendentes)

As notificações push de mudança de status do pedido chegam com um atraso médio de 5 minutos após a mudança real de status. Isso ocorre porque o job de envio de notificações roda em um intervalo fixo de 5 minutos, em vez de ser disparado por evento.

### BUG-05 — Login com Google falha em Android 10 (SCRUM-27, status: Tarefas pendentes)

Ao tentar autenticar com o Google em dispositivos Android 10, o fluxo OAuth redireciona corretamente para a tela de seleção de conta, mas ao retornar ao app, exibe uma mensagem de falha na autenticação sem mais detalhes.

### BUG-06 — Tela de rastreamento não atualiza posição automaticamente (SCRUM-28, status: Tarefas pendentes)

A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.

### BUG-07 — Cupom inválido retorna erro 500 (SCRUM-29, status: Tarefas pendentes)

Ao inserir um código de cupom inválido, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada. O app exibe uma mensagem genérica de erro.


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
- "acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "EP-06" — fonte(s): SCRUM-6
- "expresse sua experiência com o restaurante e o entregador após a conclusão do pedido" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6

**Funcionalidades:**

- "Cadastro e Login" — fonte(s): SCRUM-7
- "Cadastro com e-mail e senha" — fonte(s): SCRUM-7
- "usuários novos podem criar uma conta no app" — fonte(s): SCRUM-7
- "inserindo nome completo, e-mail e senha." — fonte(s): SCRUM-7
- "sistema valida o e-mail e a senha" — fonte(s): SCRUM-7
- "envia um e-mail de confirmação." — fonte(s): SCRUM-7
- "Login com Google" — fonte(s): SCRUM-8
- "usuários podem acessar o app usando sua conta Google" — fonte(s): SCRUM-8
- "sem precisar criar uma senha." — fonte(s): SCRUM-8
- "fluxo OAuth funciona em iOS e Android." — fonte(s): SCRUM-8
- "Redefinição de senha" — fonte(s): SCRUM-9
- "usuários podem redefinir sua senha por e-mail" — fonte(s): SCRUM-9
- "link de redefinição válido por 30 minutos." — fonte(s): SCRUM-9
- "redefinição, todas as sessões ativas são encerradas." — fonte(s): SCRUM-9
- "Busca e Filtro" — fonte(s): SCRUM-11, SCRUM-10
- "Busca de restaurantes por nome" — fonte(s): SCRUM-10
- "usuários podem buscar restaurantes pelo nome" — fonte(s): SCRUM-10
- "resultados exibidos em tempo real." — fonte(s): SCRUM-10
- "sistema retorna nome, foto, avaliação e tempo estimado de entrega." — fonte(s): SCRUM-10
- "Filtro por categoria" — fonte(s): SCRUM-11
- "usuários podem filtrar restaurantes por categoria de culinária" — fonte(s): SCRUM-11
- "selecionando múltiplas categorias simultaneamente." — fonte(s): SCRUM-11
- "filtro ativo é destacado visualmente e pode ser removido individualmente." — fonte(s): SCRUM-11
- "Visualização e Montagem do Pedido" — fonte(s): SCRUM-13, SCRUM-12
- "Visualização do cardápio" — fonte(s): SCRUM-12
- "usuários podem ver o cardápio completo de um restaurante" — fonte(s): SCRUM-12
- "organizado por seções" — fonte(s): SCRUM-12
- "foto, descrição curta e preço de cada item." — fonte(s): SCRUM-12
- "Adicionar itens ao carrinho" — fonte(s): SCRUM-13
- "usuários podem clicar em um item do cardápio e adicioná-lo ao carrinho" — fonte(s): SCRUM-13
- "opções de personalização e quantidade." — fonte(s): SCRUM-13
- "carrinho só pode conter itens de um único restaurante por vez." — fonte(s): SCRUM-13
- "Aplicar cupom de desconto" — fonte(s): SCRUM-14
- "usuários podem digitar o código do cupom e aplicá-lo ao pedido" — fonte(s): SCRUM-14
- "validação em tempo real" — fonte(s): SCRUM-14
- "desconto exibido de forma destacada." — fonte(s): SCRUM-14
- "Acompanhamento e Pagamento" — fonte(s): SCRUM-18, SCRUM-17, SCRUM-15
- "Acompanhamento de status do pedido" — fonte(s): SCRUM-15
- "usuários podem acessar uma tela de acompanhamento com linha do tempo visual" — fonte(s): SCRUM-15
- "etapas do pedido em tempo real." — fonte(s): SCRUM-15
- "Pagamento com cartão de crédito" — fonte(s): SCRUM-17
- "usuários podem selecionar "Cartão de Crédito"" — fonte(s): SCRUM-17
- "inserir os dados do cartão em um formulário tokenizado" — fonte(s): SCRUM-17
- "feedback imediato de aprovação ou recusa." — fonte(s): SCRUM-17
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "usuários podem selecionar Pix como método de pagamento" — fonte(s): SCRUM-18
- "QR Code válido por 10 minutos" — fonte(s): SCRUM-18
- "monitoramento em tempo real do pagamento." — fonte(s): SCRUM-18
- "Entrega e Avaliação" — fonte(s): SCRUM-21, SCRUM-20, SCRUM-19, SCRUM-16
- "Cancelamento de pedido" — fonte(s): SCRUM-16
- "usuários podem cancelar seu pedido enquanto estiver no status "Pedido Recebido"" — fonte(s): SCRUM-16
- "informando o motivo do cancelamento e recebendo um e-mail de confirmação." — fonte(s): SCRUM-16
- "Notificação de saída para entrega" — fonte(s): SCRUM-20
- "usuários recebem uma notificação push quando seu pedido sai para entrega" — fonte(s): SCRUM-20
- "nome do restaurante, tempo estimado e link para a tela de rastreamento." — fonte(s): SCRUM-20
- "Rastreamento do entregador no mapa" — fonte(s): SCRUM-19
- "usuários podem ver a localização do entregador em tempo real no mapa" — fonte(s): SCRUM-19
- "trajeto estimado e o tempo restante recalculados dinamicamente." — fonte(s): SCRUM-19
- "Avaliação do restaurante" — fonte(s): SCRUM-21
- "pedido ser marcado como entregue" — fonte(s): SCRUM-21
- "usuários recebem uma notificação convidando-os a avaliar" — fonte(s): SCRUM-21
- "atribuindo de 1 a 5 estrelas e adicionando um comentário opcional." — fonte(s): SCRUM-21

**Tarefas Operacionais:**

- "Modo escuro" — fonte(s): SCRUM-33
- "Atualmente, o aplicativo só suporta tema claro." — fonte(s): SCRUM-33
- "A implementação do modo escuro seguirá as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Salvar último endereço de entrega automaticamente" — fonte(s): SCRUM-32
- "O usuário precisa digitar o endereço de entrega em cada novo pedido." — fonte(s): SCRUM-32
- "A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar." — fonte(s): SCRUM-32
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com ícone, mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "Skeleton loading nas telas de lista" — fonte(s): SCRUM-30
- "Ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados." — fonte(s): SCRUM-30
- "A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais)" — fonte(s): SCRUM-30
- "reduzindo a percepção de tempo de carregamento e melhorando a experiência visual." — fonte(s): SCRUM-30

**Problemas Conhecidos:**

- "BUG-01 — App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "(SCRUM-22, status: Tarefas pendentes)" — fonte(s): SCRUM-22
- "O aplicativo para de responder e exibe uma tela branca" — fonte(s): SCRUM-22
- "tentar adicionar um item sem imagem ao carrinho." — fonte(s): SCRUM-22
- "O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada." — fonte(s): SCRUM-22
- "BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial" — fonte(s): SCRUM-23
- "(SCRUM-23, status: Tarefas pendentes)" — fonte(s): SCRUM-23
- "o usuário seleciona uma categoria e volta para a tela inicial" — fonte(s): SCRUM-23
- "o filtro permanece ativo visualmente" — fonte(s): SCRUM-23
- "a lista exibe todos os restaurantes sem filtro aplicado." — fonte(s): SCRUM-23
- "BUG-03 — Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "(SCRUM-25, status: Tarefas pendentes)" — fonte(s): SCRUM-25
- "tela de checkout" — fonte(s): SCRUM-25
- "a taxa de entrega é exibida corretamente" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total incorreto." — fonte(s): SCRUM-25
- "BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "(SCRUM-26, status: Tarefas pendentes)" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido chegam com um atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "o job de envio de notificações roda em um intervalo fixo de 5 minutos, em vez de ser disparado por evento." — fonte(s): SCRUM-26
- "BUG-05 — Login com Google falha em Android 10" — fonte(s): SCRUM-27
- "(SCRUM-27, status: Tarefas pendentes)" — fonte(s): SCRUM-27
- "tentar autenticar com o Google em dispositivos Android 10" — fonte(s): SCRUM-27
- "o fluxo OAuth redireciona corretamente para a tela de seleção de conta" — fonte(s): SCRUM-27
- "ao retornar ao app, exibe uma mensagem de falha na autenticação sem mais detalhes." — fonte(s): SCRUM-27
- "BUG-06 — Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "(SCRUM-28, status: Tarefas pendentes)" — fonte(s): SCRUM-28
- "A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "O usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "BUG-07 — Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "(SCRUM-29, status: Tarefas pendentes)" — fonte(s): SCRUM-29
- "inserir um código de cupom inválido" — fonte(s): SCRUM-29
- "a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "O app exibe uma mensagem genérica de erro." — fonte(s): SCRUM-29