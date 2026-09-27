# Manual do Usuário

## Autenticação e Cadastro

O acesso à plataforma é feito por meio de autenticação e cadastro. Você pode criar uma conta, fazer login, recuperar sua senha e gerenciar seu perfil. É a porta de entrada do aplicativo e impacta diretamente a sua experiência inicial.

## Catálogo de Restaurantes

Aqui você pode explorar e pesquisar restaurantes e seus cardápios. Encontre facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

### Visualização do Cardápio

Ao clicar em um restaurante, você acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados com a etiqueta "Indisponível".

## Carrinho e Pedidos

Esta é a área central do aplicativo, onde você pode adicionar itens ao carrinho, confirmar seu pedido e acompanhar o processo. É aqui que a conversão de interesse em compra acontece.

## Pagamentos

O aplicativo oferece diversas formas de pagamento, garantindo segurança, praticidade e variedade de métodos para você finalizar sua compra.

### Pagamento com Pix

Você pode selecionar o Pix como método de pagamento e um QR Code será gerado com validade de 10 minutos. O valor e os dados do beneficiário serão exibidos. O aplicativo monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação sua. Se o QR Code expirar, você pode gerar um novo.

## Rastreamento de Entrega

Você pode acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na sua porta.

## Avaliações

Após a conclusão do pedido, você pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Modo Escuro

O aplicativo atualmente só suporta tema claro, mas em breve será implementado o suporte ao modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS). A preferência do sistema será detectada automaticamente e você também terá a opção de alternar manualmente nas configurações do aplicativo.

## Bugs e Melhorias

- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada. O aplicativo exibe uma mensagem genérica e não trata o caso de cupom não encontrado.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar um item sem imagem ao carrinho, o aplicativo para de responder e exibe uma tela branca. Este problema ocorre devido a uma exceção não tratada.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto. O valor cobrado no pagamento é o correto, mas a exibição do resumo precisa ser corrigida.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso de ~5 minutos**: As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status. Isso impacta a percepção de tempo real do acompanhamento.
- **Mensagem de erro sem conexão com internet**: Quando o aplicativo é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão "Tentar novamente".

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "autenticação e cadastro." — fonte(s): SCRUM-1
- "criar uma conta, fazer login, recuperar sua senha e gerenciar seu perfil." — fonte(s): SCRUM-1
- "porta de entrada do aplicativo" — fonte(s): SCRUM-1
- "impacta diretamente a sua experiência inicial." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "explorar e pesquisar restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Visualização do Cardápio" — fonte(s): SCRUM-12
- "clicar em um restaurante, você acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "Itens indisponíveis aparecem como desabilitados com a etiqueta "Indisponível"" — fonte(s): SCRUM-12
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "adicionar itens ao carrinho, confirmar seu pedido e acompanhar o processo." — fonte(s): SCRUM-3
- "conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "diversas formas de pagamento, garantindo segurança, praticidade e variedade de métodos para você finalizar sua compra." — fonte(s): SCRUM-4
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "selecionar o Pix como método de pagamento e um QR Code será gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "valor e os dados do beneficiário serão exibidos." — fonte(s): SCRUM-18
- "aplicativo monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação sua." — fonte(s): SCRUM-18
- "QR Code expirar, você pode gerar um novo." — fonte(s): SCRUM-18
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na sua porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido, você pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Modo Escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "implementado o suporte ao modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "preferência do sistema será detectada automaticamente e você também terá a opção de alternar manualmente nas configurações do aplicativo." — fonte(s): SCRUM-33
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada." — fonte(s): SCRUM-29
- "aplicativo exibe uma mensagem genérica e não trata o caso de cupom não encontrado." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "tentar adicionar um item sem imagem ao carrinho, o aplicativo para de responder e exibe uma tela branca." — fonte(s): SCRUM-22
- "problema ocorre devido a uma exceção não tratada." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega", mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto." — fonte(s): SCRUM-25
- "valor cobrado no pagamento é o correto, mas a exibição do resumo precisa ser corrigida." — fonte(s): SCRUM-25
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "usuário precisa fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "impacta a percepção de tempo real do acompanhamento." — fonte(s): SCRUM-26
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "aplicativo é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout." — fonte(s): SCRUM-31
- "melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com uma mensagem clara e um botão "Tentar novamente"" — fonte(s): SCRUM-31