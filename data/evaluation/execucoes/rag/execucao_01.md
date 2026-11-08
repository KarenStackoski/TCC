# Manual do Usuário

## Autenticação e Cadastro

A autenticação e o cadastro são a porta de entrada do aplicativo. Aqui, o usuário pode criar uma conta, fazer login, recuperar senha e gerenciar seu perfil.

## Catálogo de Restaurantes

O catálogo de restaurantes permite que o usuário visualize, busque e filtre restaurantes e seus cardápios. As informações incluem horário, avaliação, tempo e taxa de entrega. O cardápio é organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas), com nome, foto, descrição curta e preço de cada item. Itens indisponíveis são exibidos como desabilitados com a label "Indisponível".

## Carrinho e Pedidos

O carrinho e os pedidos cobrem todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É o núcleo do aplicativo, onde a conversão de interesse em compra acontece.

## Pagamentos

A área de pagamentos oferece segurança, praticidade e variedade de métodos para o usuário finalizar a compra. O usuário pode pagar com Pix, gerando um QR Code válido por 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela após a confirmação.

## Rastreamento de Entrega

O rastreamento de entrega permite que o usuário acompanhe em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

## Avaliações

Após a conclusão do pedido, o usuário pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Modo Escuro

O aplicativo atualmente só suporta tema claro. A melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

## Bugs e Melhorias

- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada. O app exibe uma mensagem genérica.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar um item sem imagem ao carrinho, o aplicativo trava e exibe uma tela branca. O problema ocorre devido a uma exceção não tratada.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.
- **Mensagem de erro sem conexão com internet**: Quando o usuário abre o app sem conexão, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso de ~5 minutos**: As notificações push de mudança de status do pedido chegam com atraso de aproximadamente 5 minutos após a mudança real de status.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "autenticação e o cadastro" — fonte(s): SCRUM-1
- "porta de entrada do aplicativo." — fonte(s): SCRUM-1
- "criar uma conta, fazer login, recuperar senha e gerenciar seu perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "catálogo de restaurantes" — fonte(s): SCRUM-2
- "visualize, busque e filtre restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "horário, avaliação, tempo e taxa de entrega." — fonte(s): SCRUM-12
- "cardápio é organizado por seções" — fonte(s): SCRUM-12
- "(Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço de cada item." — fonte(s): SCRUM-12
- "Itens indisponíveis são exibidos como desabilitados com a label "Indisponível"" — fonte(s): SCRUM-12
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "carrinho e os pedidos" — fonte(s): SCRUM-3
- "todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "núcleo do aplicativo" — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "pagamentos" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "pagar com Pix" — fonte(s): SCRUM-18
- "QR Code válido por 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real e avança automaticamente para a próxima tela após a confirmação." — fonte(s): SCRUM-18
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "rastreamento de entrega" — fonte(s): SCRUM-5
- "acompanhe em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido" — fonte(s): SCRUM-6
- "expressar sua experiência com o restaurante e o entregador" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Modo Escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro." — fonte(s): SCRUM-33
- "implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "código de cupom inválido" — fonte(s): SCRUM-29
- "API retorna um erro interno em vez de uma mensagem de erro adequada." — fonte(s): SCRUM-29
- "mensagem genérica." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "adicionar um item sem imagem ao carrinho" — fonte(s): SCRUM-22
- "aplicativo trava e exibe uma tela branca." — fonte(s): SCRUM-22
- "exceção não tratada." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout" — fonte(s): SCRUM-25
- "taxa de entrega é exibida corretamente no campo "Entrega"" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total incorreto." — fonte(s): SCRUM-25
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "abre o app sem conexão" — fonte(s): SCRUM-31
- "mensagem técnica de timeout." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara." — fonte(s): SCRUM-31
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido chegam com atraso de aproximadamente 5 minutos após a mudança real de status." — fonte(s): SCRUM-26