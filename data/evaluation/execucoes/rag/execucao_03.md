# Manual do Usuário

## Autenticação e Cadastro

A primeira etapa de acesso à plataforma envolve a criação de uma conta, login e gerenciamento de perfil. É a porta de entrada do aplicativo e impacta diretamente a experiência inicial do usuário.

## Catálogo de Restaurantes

Esta seção permite a exibição, busca e filtragem de restaurantes e seus cardápios. O usuário pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

## Carrinho e Pedidos

Aqui, o usuário pode adicionar itens ao carrinho, confirmar e acompanhar o pedido. É o núcleo do aplicativo, onde a conversão de interesse em compra acontece.

## Pagamentos

A plataforma oferece diversas formas de pagamento, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

## Rastreamento de Entrega

O usuário pode acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

## Avaliações

Após a conclusão do pedido, o usuário pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Visualização do Cardápio

Ao clicar em um restaurante, o usuário acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados com a etiqueta "Indisponível".

## Pagamento com Pix

O usuário pode selecionar Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O aplicativo monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário. Se o QR Code expirar, o usuário pode gerar um novo.

## Modo Escuro

O aplicativo atualmente só suporta tema claro. A melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.

## Bugs e Melhorias

- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom que não existe no sistema, a API retorna um erro interno em vez de uma mensagem de erro adequada. O aplicativo exibe uma mensagem genérica e o backend não trata o caso corretamente.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar um item sem imagem ao carrinho, o aplicativo para de responder e exibe uma tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto.
- **Mensagem de erro sem conexão com internet**: Quando o usuário abre o aplicativo sem conexão, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão para tentar novamente.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso**: As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status. Impacta a percepção de tempo real do acompanhamento.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "criação de uma conta, login e gerenciamento de perfil." — fonte(s): SCRUM-1
- "porta de entrada do aplicativo" — fonte(s): SCRUM-1
- "impacta diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "exibição, busca e filtragem de restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "adicionar itens ao carrinho, confirmar e acompanhar o pedido." — fonte(s): SCRUM-3
- "núcleo do aplicativo" — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "diversas formas de pagamento" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos" — fonte(s): SCRUM-4
- "finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido" — fonte(s): SCRUM-6
- "expressar sua experiência com o restaurante e o entregador" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Visualização do Cardápio" — fonte(s): SCRUM-12
- "página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega)" — fonte(s): SCRUM-12
- "cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Itens indisponíveis aparecem como desabilitados com a etiqueta "Indisponível"" — fonte(s): SCRUM-12
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "selecionar Pix como método de pagamento" — fonte(s): SCRUM-18
- "QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "valor e os dados do beneficiário são exibidos." — fonte(s): SCRUM-18
- "monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário." — fonte(s): SCRUM-18
- "QR Code expirar, o usuário pode gerar um novo." — fonte(s): SCRUM-18
- "Modo Escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro." — fonte(s): SCRUM-33
- "implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "inserir um código de cupom que não existe no sistema" — fonte(s): SCRUM-29
- "API retorna um erro interno em vez de uma mensagem de erro adequada." — fonte(s): SCRUM-29
- "mensagem genérica" — fonte(s): SCRUM-29
- "backend não trata o caso corretamente." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "tentar adicionar um item sem imagem ao carrinho" — fonte(s): SCRUM-22
- "para de responder e exibe uma tela branca." — fonte(s): SCRUM-22
- "componente de imagem não trata o caso de URL nula." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout, a taxa de entrega é exibida corretamente" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total ficar incorreto." — fonte(s): SCRUM-25
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "abre o aplicativo sem conexão" — fonte(s): SCRUM-31
- "mensagem técnica de timeout." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão para tentar novamente." — fonte(s): SCRUM-31
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente" — fonte(s): SCRUM-28
- "tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "percepção de tempo real do acompanhamento." — fonte(s): SCRUM-26