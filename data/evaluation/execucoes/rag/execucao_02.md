# Manual do Usuário

## Autenticação e Cadastro
A autenticação e o cadastro são a porta de entrada do aplicativo. Aqui, você pode criar uma conta, fazer login, recuperar sua senha e gerenciar seu perfil.

## Catálogo de Restaurantes
O catálogo de restaurantes permite que você visualize, busque e filtre restaurantes e seus cardápios. Você pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

## Carrinho e Pedidos
O carrinho e os pedidos são o núcleo do aplicativo, onde a conversão de interesse em compra acontece. Você pode adicionar itens ao carrinho, confirmar e acompanhar seu pedido.

## Pagamentos
A área de pagamentos oferece diversas formas de pagamento seguras, práticas e variadas para que você finalize sua compra.

## Rastreamento de Entrega
O rastreamento de entrega permite que você acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na sua porta.

## Avaliações
Após a conclusão do pedido, você pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Bugs e Melhorias
- **Cupom inválido retorna erro 500**: ao inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada.
- **App trava ao adicionar item sem foto ao carrinho**: ao tentar adicionar um item sem imagem ao carrinho, o aplicativo para de responder e exibe uma tela branca.
- **Valor do frete somando em dobro no resumo do pedido**: na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.
- **Tela de rastreamento não atualiza posição automaticamente**: a posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos.
- **Notificação de pedido chegando com atraso de ~5 minutos**: as notificações push de mudança de status do pedido chegam com atraso de aproximadamente 5 minutos após a mudança real de status.
- **Modo escuro**: o aplicativo atualmente só suporta tema claro, mas está previsto o suporte ao modo escuro, seguindo as diretrizes de design do sistema operacional.
- **Mensagem de erro sem conexão com internet**: quando o aplicativo é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "autenticação e o cadastro" — fonte(s): SCRUM-1
- "porta de entrada do aplicativo." — fonte(s): SCRUM-1
- "criar uma conta, fazer login, recuperar sua senha e gerenciar seu perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "catálogo de restaurantes" — fonte(s): SCRUM-2
- "visualize, busque e filtre restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "carrinho e os pedidos" — fonte(s): SCRUM-3
- "núcleo do aplicativo" — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "adicionar itens ao carrinho, confirmar e acompanhar seu pedido." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "pagamentos" — fonte(s): SCRUM-4
- "diversas formas de pagamento seguras, práticas e variadas" — fonte(s): SCRUM-4
- "finalize sua compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "rastreamento de entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na sua porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido" — fonte(s): SCRUM-6
- "expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "tentar adicionar um item sem imagem ao carrinho, o aplicativo para de responder e exibe uma tela branca." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto." — fonte(s): SCRUM-25
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido chegam com atraso de aproximadamente 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "Modo escuro" — fonte(s): SCRUM-33
- "aplicativo atualmente só suporta tema claro, mas está previsto o suporte ao modo escuro, seguindo as diretrizes de design do sistema operacional." — fonte(s): SCRUM-33
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "aplicativo é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara." — fonte(s): SCRUM-31