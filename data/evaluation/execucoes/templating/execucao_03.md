# Manual do Usuário

_Documento gerado automaticamente — Etapa 1 do TCC: Templating puro (Jinja2), sem geração de texto por IA._

## Visão Geral

### EP-06 — Avaliações

Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

### EP-05 — Rastreamento de Entrega

Funcionalidades que permitem ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

### EP-04 — Pagamentos

Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

### EP-03 — Carrinho e Pedidos

Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É o núcleo do app, onde a conversão de interesse em compra acontece.

### EP-02 — Catálogo de Restaurantes

Engloba a exibição, busca e filtragem de restaurantes e seus cardápios. O usuário precisa encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

### EP-01 — Autenticação e Cadastro

Agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil. É a porta de entrada do app e impacta diretamente a experiência inicial do usuário.

## Funcionalidades

### US-15 — Avaliação do restaurante

> *Como usuário, quero avaliar o restaurante após receber meu pedido para compartilhar minha experiência com outros usuários.*

**Descrição:** Após o pedido ser marcado como entregue, o usuário recebe uma notificação convidando-o a avaliar. Na tela de avaliação, o usuário atribui de 1 a 5 estrelas para o restaurante e pode adicionar um comentário opcional de até 300 caracteres. A avaliação é vinculada ao pedido específico e cada pedido permite apenas uma avaliação. A média de avaliações do restaurante é atualizada em tempo real.

**Passo a passo:**

1. Avaliação disponível por até 7 dias após entrega
2. Comentário opcional com limite de 300 caracteres
3. Apenas uma avaliação por pedido
4. Média do restaurante atualizada imediatamente após envio

### US-14 — Notificação de saída para entrega

> *Como usuário, quero receber uma notificação push quando meu pedido sair para entrega para me preparar para recebê-lo.*

**Descrição:** Quando o status do pedido muda para "Saiu para Entrega", o sistema dispara automaticamente uma notificação push para o dispositivo do usuário com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento. A notificação deve ser enviada mesmo com o app em segundo plano ou fechado.

**Passo a passo:**

1. Notificação enviada em até 5 segundos após mudança de status
2. Funciona com app em segundo plano e fechado
3. Toque na notificação abre diretamente a tela de rastreamento
4. Usuário pode desativar notificações nas configurações do app

### US-13 — Rastreamento do entregador no mapa

> *Como usuário, quero ver a localização do entregador em tempo real no mapa para saber quando meu pedido vai chegar.*

**Descrição:** Após o pedido entrar no status "Saiu para Entrega", a tela de acompanhamento exibe um mapa com a posição atual do entregador (ícone de moto), a localização do restaurante e o endereço de entrega. A posição do entregador é atualizada a cada 10 segundos via WebSocket. O trajeto estimado é desenhado no mapa e o tempo restante é recalculado dinamicamente.

**Passo a passo:**

1. Posição do entregador atualizada a cada 10 segundos
2. Trajeto estimado exibido no mapa
3. Tempo restante recalculado a cada atualização de posição
4. Mapa centralizando automaticamente na posição do entregador

### US-12 — Pagamento com Pix

> *Como usuário, quero pagar com Pix para finalizar o pedido de forma instantânea sem usar cartão.*

**Descrição:** O usuário seleciona Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O app monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário. Se o QR Code expirar, o usuário pode gerar um novo.

**Passo a passo:**

1. QR Code válido por 10 minutos com contador regressivo visível
2. Código Pix copia-e-cola disponível como alternativa ao QR Code
3. Detecção automática do pagamento em até 5 segundos após confirmação
4. Opção de gerar novo QR Code após expiração

### US-11 — Pagamento com cartão de crédito

> *Como usuário, quero pagar meu pedido com cartão de crédito para finalizar a compra de forma segura.*

**Descrição:** Na tela de checkout, o usuário seleciona "Cartão de Crédito" e insere os dados do cartão (número, nome, validade, CVV) em um formulário tokenizado via gateway de pagamento. O sistema exibe as bandeiras aceitas (Visa, Mastercard, Elo, Amex). Após confirmação, o pagamento é processado e o resultado (aprovado/recusado) é exibido imediatamente.

**Passo a passo:**

1. Dados do cartão nunca armazenados no backend da aplicação (tokenização)
2. Feedback imediato de aprovação ou recusa
3. Mensagem de erro amigável em caso de recusa
4. Compatível com 3DS quando exigido pela operadora

### US-10 — Cancelamento de pedido

> *Como usuário, quero cancelar meu pedido antes que ele seja aceito pelo restaurante para não ser cobrado por um pedido indesejado.*

**Descrição:** Na tela de acompanhamento, enquanto o pedido estiver no status "Pedido Recebido" (aguardando confirmação do restaurante), um botão "Cancelar Pedido" é exibido. Ao clicar, o usuário informa o motivo do cancelamento (campo obrigatório com opções pré-definidas) e confirma. O estorno é processado automaticamente para o método de pagamento utilizado em até 5 dias úteis.

**Passo a passo:**

1. Cancelamento disponível apenas no status "Pedido Recebido"
2. Motivo do cancelamento obrigatório
3. Estorno automático iniciado imediatamente
4. E-mail de confirmação de cancelamento enviado ao usuário

### US-09 — Acompanhamento de status do pedido

> *Como usuário, quero acompanhar o status do meu pedido em tempo real para saber em que etapa ele está.*

**Descrição:** Após confirmar o pedido, o usuário acessa uma tela de acompanhamento com linha do tempo visual mostrando as etapas: Pedido Recebido → Confirmado pelo Restaurante → Em Preparo → Saiu para Entrega → Entregue. Cada etapa é atualizada via WebSocket em tempo real. O tempo estimado de entrega é exibido e atualizado dinamicamente.

**Passo a passo:**

1. Atualização via WebSocket sem necessidade de recarregar a tela
2. Tempo estimado atualizado a cada mudança de status
3. Notificação push em cada mudança de status
4. Histórico de horários de cada etapa visível

### US-08 — Aplicar cupom de desconto

> *Como usuário, quero aplicar um cupom de desconto no meu pedido para pagar menos na entrega ou nos itens.*

**Descrição:** Na tela de checkout, o usuário digita o código do cupom em um campo dedicado e clica em "Aplicar". O sistema valida o cupom (existência, validade, valor mínimo de pedido, uso por usuário) e exibe o desconto aplicado no resumo do pedido. Caso inválido, uma mensagem específica informa o motivo (expirado, já utilizado, valor mínimo não atingido).

**Passo a passo:**

1. Validação em tempo real ao clicar em "Aplicar"
2. Mensagem de erro específica por tipo de falha
3. Desconto exibido de forma destacada no resumo
4. Apenas um cupom por pedido

### US-07 — Adicionar itens ao carrinho

> *Como usuário, quero adicionar itens ao carrinho para montar meu pedido antes de finalizar a compra.*

**Descrição:** O usuário clica em um item do cardápio e uma bottom sheet é exibida com a foto ampliada, descrição completa, opções de personalização (ex: ponto da carne, retirar ingredientes) e quantidade. Ao confirmar, o item é adicionado ao carrinho e um indicador flutuante com o total aparece na tela. O carrinho só pode conter itens de um único restaurante por vez — caso o usuário tente adicionar de outro, um alerta pergunta se deseja limpar o carrinho.

**Passo a passo:**

1. Bottom sheet com opções de personalização quando aplicável
2. Alerta ao tentar misturar itens de restaurantes diferentes
3. Indicador de carrinho atualizado em tempo real
4. Quantidade mínima de 1 e máxima de 20 por item

### US-06 — Visualização do cardápio

> *Como usuário, quero ver o cardápio completo de um restaurante para escolher o que vou pedir.*

**Descrição:** Ao clicar em um restaurante, o usuário acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados com label "Indisponível".

**Passo a passo:**

1. Cardápio organizado em seções com navegação por âncora
2. Itens indisponíveis exibidos mas não clicáveis
3. Foto de cada item (fallback para imagem padrão se não houver)
4. Informações do restaurante sempre visíveis no topo

### US-05 — Filtro por categoria

> *Como usuário, quero filtrar restaurantes por categoria de culinária para encontrar o tipo de comida que desejo.*

**Descrição:** Na tela principal, o usuário visualiza chips horizontais com as categorias disponíveis (Pizza, Sushi, Hambúrguer, Brasileira, Árabe, Sobremesas, etc.). Ao selecionar uma categoria, a lista de restaurantes é filtrada automaticamente. É possível selecionar múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

**Passo a passo:**

1. Seleção múltipla de categorias permitida
2. Filtro combinável com busca por nome
3. Filtro persiste ao rolar a lista
4. Botão "Limpar filtros" visível quando algum filtro estiver ativo

### US-04 — Busca de restaurantes por nome

> *Como usuário, quero buscar restaurantes pelo nome para encontrar rapidamente um estabelecimento específico.*

**Descrição:** Na tela principal, o usuário acessa o campo de busca e digita o nome (parcial ou completo) do restaurante. O sistema retorna resultados em tempo real com debounce de 300ms para evitar requisições excessivas. Os resultados exibem nome, foto, avaliação e tempo estimado de entrega. Caso nenhum resultado seja encontrado, exibe mensagem amigável com sugestões.

**Passo a passo:**

1. Busca insensível a maiúsculas/minúsculas e acentos
2. Debounce de 300ms implementado
3. Resultados exibidos em até 1 segundo
4. Mensagem de "nenhum resultado" com sugestões alternativas

### US-03 — Redefinição de senha

> *Como usuário, quero redefinir minha senha por e-mail caso eu esqueça minha senha atual.*

**Descrição:** O usuário clica em "Esqueci minha senha" na tela de login, informa seu e-mail e recebe um link de redefinição. O link é válido por 30 minutos e redireciona para uma tela onde o usuário define uma nova senha. Após redefinição, todas as sessões ativas são encerradas por segurança.

**Passo a passo:**

1. Link de redefinição expira em 30 minutos
2. Após uso do link, ele não pode ser reutilizado
3. Todas as sessões ativas encerradas após troca de senha
4. Confirmação visual de sucesso após redefinição

### US-02 — Login com Google

> *Como usuário, quero fazer login com minha conta Google para acessar o app sem precisar criar uma senha.*

**Descrição:** Na tela de login, o usuário clica em "Entrar com Google" e é redirecionado para o fluxo de autenticação OAuth do Google. Após autenticação bem-sucedida, se for o primeiro acesso, uma conta é criada automaticamente com os dados do perfil Google (nome e foto). Se já tiver conta vinculada, o usuário é autenticado diretamente.

**Passo a passo:**

1. Fluxo OAuth deve funcionar em iOS e Android
2. Em primeiro acesso, conta criada automaticamente sem etapas extras
3. Token de sessão válido por 30 dias
4. Em caso de falha na autenticação, exibir mensagem de erro adequada

### US-01 — Cadastro com e-mail e senha

> *Como usuário novo, quero me cadastrar com e-mail e senha para criar minha conta no app.*

**Descrição:** O usuário acessa a tela de cadastro e preenche nome completo, e-mail e senha. O sistema valida se o e-mail já está cadastrado, se a senha atende aos requisitos mínimos (mínimo 8 caracteres, uma letra maiúscula e um número) e envia um e-mail de confirmação. Somente após confirmar o e-mail o cadastro é ativado.

**Passo a passo:**

1. Campo de e-mail deve validar formato correto
2. Senha deve exibir indicador de força
3. Exibir mensagem de erro clara se o e-mail já estiver em uso
4. E-mail de confirmação enviado em até 1 minuto

## Tarefas Operacionais

### IMP-04 — Modo escuro

**Descrição:** O app atualmente só suporta tema claro. A melhoria consiste em implementar suporte a modo escuro seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app. Todos os componentes, telas e modais devem ser adaptados para garantir contraste e legibilidade adequados.

### IMP-03 — Salvar último endereço de entrega automaticamente

**Descrição:** Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar. Endereços frequentes podem ser salvos como favoritos ("Casa", "Trabalho") acessíveis diretamente na tela de entrega.

### IMP-02 — Mensagem de erro sem conexão com internet

**Descrição:** Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente via listener de rede e exibir uma tela amigável com ícone, mensagem clara ("Sem conexão com a internet") e botão "Tentar novamente", sem aguardar o timeout da requisição.

### IMP-01 — Skeleton loading nas telas de lista

**Descrição:** Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual. Baseado em padrão amplamente utilizado por apps como iFood e Rappi.

## Problemas Conhecidos

| Chave | Título | Status |
| --- | --- | --- |
| SCRUM-29 | BUG-07 — Cupom inválido retorna erro 500 | Tarefas pendentes |
| SCRUM-28 | BUG-06 — Tela de rastreamento não atualiza posição automaticamente | Tarefas pendentes |
| SCRUM-27 | BUG-05 — Login com Google falha em Android 10 | Tarefas pendentes |
| SCRUM-26 | BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos | Tarefas pendentes |
| SCRUM-25 | BUG-03 — Valor do frete somando em dobro no resumo do pedido | Tarefas pendentes |
| SCRUM-23 | BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial | Tarefas pendentes |
| SCRUM-22 | BUG-01 — App trava ao adicionar item sem foto ao carrinho | Tarefas pendentes |
