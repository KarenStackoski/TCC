# Manual do usuário

## Sumário

<!-- Classificado conforme a ordem com que o usuário vai utilizar cada funcionalidade -->

- [Autenticação e Cadastro](#autenticacao-e-cadastro)
- [Catálogo de Restaurantes](#catalogo-de-restaurantes)
- [Carrinho e Pedidos](#carrinho-e-pedidos)
- [Pagamentos](#pagamentos)
- [Rastreamento de Entrega](#rastreamento-de-entrega)
- [Avaliações](#avaliacoes)

## Autenticação e Cadastro

Para **realizar o cadastro**, o usuário deve acessar a tela de cadastro e preencher os campos de nome completo, e-mail e senha. O sistema valida se o e-mail já está cadastrado, se a senha atende aos requisitos mínimos (mínimo 8 caracteres, uma letra maiúscula e um número) e envia um e-mail de confirmação. Somente após confirmar o e-mail o cadastro é ativado.

Para **realizar login**, o usuário deve clicar em "Entrar com Google", assim ele será redirecionado para o fluxo de autenticação OAuth do Google. Após autenticação bem-sucedida, se for o primeiro acesso, uma conta é criada automaticamente com os dados do perfil Google (nome e foto). Se já tiver conta vinculada, o usuário é autenticado diretamente.

**Particularidades:**

- É possível utilizar a autenticação por OAuth em iOS e Android;
- Ao realizar o primeiro acesso, a conta é criada automaticamente sem etapas extras;
- O login é válido por 30 dias. Após esse perído é necessário autenticar novamente com a mesma conta;
- Em caso de falha na autenticação, o app exibe uma mensagem de erro.

Para **redefinir a senha**, o usuário deve clicar em "Esqueci minha senha" na tela de login, informar seu e-mail e receber um link de redefinição. O link é válido por 30 minutos e redireciona para uma tela onde o usuário define uma nova senha. Após redefinição, todas as sessões ativas são encerradas por segurança.

## Catálogo de Restaurantes

O **catálogo de resturantes** mostra as opções de estabelecimentos que o cliente pode fazer seus pedidos. É possível **filtrar** os restaurantes, para facilitar a busca. Na tela principal, o usuário acessa o campo de busca e digita o nome (parcial ou completo) do restaurante. O sistema retorna os resultados. Os resultados exibem **nome**, **foto**, **avaliação** e **tempo estimado de entrega**.

Também é possível filtrar por **categorias** utilizando os chips. Na tela principal, o usuário visualiza **chips horizontais** com as categorias disponíveis (Pizza, Sushi, Hambúrguer, Brasileira, Árabe, Sobremesas, etc.). Ao selecionar uma categoria, a lista de restaurantes é filtrada automaticamente. É possível selecionar múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

Ao **selecionar** um restaurante, o usuário acessa a página de detalhes com **banner**, **informações do estabelecimento** (horário, avaliação, tempo e taxa de entrega) e o cardápio é organizado por **seções** (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe **nome**, **foto**, **descrição curta** e **preço**. Itens indisponíveis aparecem como desabilitados com label "Indisponível".

## Carrinho e Pedidos

Para adicionar um produto ao carrinho, basta o usuário clicar em um item do cardápio e serão exibidos a foto ampliada, descrição completa, opções de personalização (ex: ponto da carne, retirar ingredientes) e quantidade. Ao confirmar, o item é adicionado ao carrinho e um indicador flutuante com o total aparece na tela. O carrinho só pode conter itens de um único restaurante por vez, caso o usuário tente adicionar de outro, um alerta pergunta se deseja limpar o carrinho.

Na tela de checkout, o usuário digita o código do cupom em um campo dedicado e clica em "Aplicar". O sistema valida o cupom (existência, validade, valor mínimo de pedido, uso por usuário) e exibe o desconto aplicado no resumo do pedido. Caso inválido, uma mensagem específica informa o motivo (expirado, já utilizado, valor mínimo não atingido).

Após confirmar o pedido, o usuário acessa uma tela de acompanhamento com linha do tempo visual mostrando as etapas: **Pedido Recebido** → **Confirmado pelo Restaurante** → **Em Preparo** → **Saiu para Entrega** → **Entregue**. Cada etapa é atualizada via WebSocket em tempo real. O tempo estimado de entrega é exibido e atualizado dinamicamente.

Na tela de acompanhamento, enquanto o pedido estiver no status "Pedido Recebido" (aguardando confirmação do restaurante), um botão "Cancelar Pedido" é exibido. Ao clicar, o usuário informa o motivo do cancelamento (campo obrigatório com opções pré-definidas) e confirma. O estorno é processado automaticamente para o método de pagamento utilizado em até 5 dias úteis.

## Pagamentos

É possível realizar o pagamento com dois métodos diferentes: Cartão de crédito e PIX.

**Cartão de crédito:** Na tela de checkout, o usuário seleciona "Cartão de Crédito" e insere os dados do cartão (número, nome, validade, CVV) em um formulário tokenizado via gateway de pagamento. O sistema exibe as bandeiras aceitas (Visa, Mastercard, Elo, Amex). Após confirmação, o pagamento é processado e o resultado (aprovado/recusado) é exibido imediatamente.

**PIX:** O usuário seleciona Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O app monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário. Se o QR Code expirar, o usuário pode gerar um novo.

## Rastreamento de Entrega

Após o pedido entrar no status "Saiu para Entrega", a tela de acompanhamento exibe um mapa com a posição atual do entregador (ícone de moto), a localização do restaurante e o endereço de entrega. A posição do entregador é atualizada a cada 10 segundos. O trajeto estimado é desenhado no mapa e o tempo restante é recalculado dinamicamente.

Quando o status do pedido muda para "Saiu para Entrega", o sistema dispara automaticamente uma notificação para o usuário com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento. A notificação deve ser enviada mesmo com o app em segundo plano ou fechado.

## Avaliações

Após o pedido ser marcado como entregue, o usuário recebe uma notificação convidando-o a avaliar. Na tela de avaliação, o usuário atribui de 1 a 5 estrelas para o restaurante e pode adicionar um comentário opcional de até 300 caracteres. A avaliação é vinculada ao pedido específico e cada pedido permite apenas uma avaliação. A média de avaliações do restaurante é atualizada em tempo real.