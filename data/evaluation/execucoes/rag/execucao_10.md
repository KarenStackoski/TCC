# Manual do Usuário

## Autenticação e Cadastro

O acesso à plataforma é feito por meio de autenticação e cadastro. Ao criar uma conta, você pode fazer login e gerenciar seu perfil. A autenticação é a porta de entrada do aplicativo e impacta diretamente a experiência inicial do usuário.

## Catálogo de Restaurantes

O catálogo de restaurantes permite que você visualize, busque e filtre estabelecimentos e seus cardápios. Você pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

## Carrinho e Pedidos

O carrinho e pedidos é o núcleo do aplicativo, onde você pode adicionar itens ao carrinho, confirmar e acompanhar seu pedido. É aqui que a conversão de interesse em compra acontece.

## Pagamentos

O aplicativo oferece diversas formas de pagamento, garantindo segurança, praticidade e variedade de métodos para finalizar sua compra. Você pode pagar com cartão ou Pix, por exemplo.

## Rastreamento de Entrega

O rastreamento de entrega permite que você acompanhe em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

## Avaliações

Após a conclusão do pedido, você pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Visualização do Cardápio

Ao clicar em um restaurante, você acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados com a etiqueta "Indisponível".

## Pagamento com Pix

Para pagar com Pix, você seleciona essa opção como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O aplicativo monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação sua. Se o QR Code expirar, você pode gerar um novo.

## Modo Escuro

O aplicativo atualmente só suporta tema claro, mas está em desenvolvimento a implementação do modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS). O modo escuro será adaptado para garantir contraste e legibilidade adequados.

## Bugs e Melhorias

- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom que não existe no sistema, a API retorna um erro interno em vez de uma mensagem de erro adequada. O aplicativo exibe uma mensagem genérica e não trata o caso de cupom não encontrado.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar um item do cardápio sem imagem cadastrada, o aplicativo para de responder e exibe uma tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto. O valor cobrado no pagamento é o correto, mas a exibição do resumo precisa ser corrigida.
- **Mensagem de erro sem conexão com internet**: Quando o aplicativo é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão para tentar novamente.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso de ~5 minutos**: As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status. O job de envio de notificações roda em intervalo fixo de 5 minutos, em vez de ser disparado por evento.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "autenticação e cadastro." — fonte(s): SCRUM-1
- "criar uma conta, você pode fazer login e gerenciar seu perfil." — fonte(s): SCRUM-1
- "autenticação é a porta de entrada do aplicativo" — fonte(s): SCRUM-1
- "impacta diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "visualize, busque e filtre estabelecimentos e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "núcleo do aplicativo" — fonte(s): SCRUM-3
- "adicionar itens ao carrinho, confirmar e acompanhar seu pedido." — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "diversas formas de pagamento" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos para finalizar sua compra." — fonte(s): SCRUM-4
- "cartão ou Pix" — fonte(s): SCRUM-18
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhe em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido, você pode expressar sua experiência com o restaurante e o entregador" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Visualização do Cardápio" — fonte(s): SCRUM-12
- "página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "indisponíveis aparecem como desabilitados com a etiqueta "Indisponível"" — fonte(s): SCRUM-12
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "seleciona essa opção como método de pagamento e um QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "valor e os dados do beneficiário são exibidos." — fonte(s): SCRUM-18
- "monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação sua." — fonte(s): SCRUM-18
- "QR Code expirar, você pode gerar um novo." — fonte(s): SCRUM-18
- "Modo Escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "implementação do modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "adaptado para garantir contraste e legibilidade adequados." — fonte(s): SCRUM-33
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "código de cupom que não existe no sistema, a API retorna um erro interno em vez de uma mensagem de erro adequada." — fonte(s): SCRUM-29
- "exibe uma mensagem genérica e não trata o caso de cupom não encontrado." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "adicionar um item do cardápio sem imagem cadastrada, o aplicativo para de responder e exibe uma tela branca." — fonte(s): SCRUM-22
- "componente de imagem não trata o caso de URL nula." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto." — fonte(s): SCRUM-25
- "valor cobrado no pagamento é o correto, mas a exibição do resumo precisa ser corrigida." — fonte(s): SCRUM-25
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão para tentar novamente." — fonte(s): SCRUM-31
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "job de envio de notificações roda em intervalo fixo de 5 minutos, em vez de ser disparado por evento." — fonte(s): SCRUM-26