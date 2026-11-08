# Manual do Usuário

## Autenticação e Cadastro

O acesso à plataforma é feito por meio de autenticação e cadastro de usuário. Ao criar uma conta, você terá acesso a todas as funcionalidades do aplicativo, incluindo login, recuperação de senha e gerenciamento de perfil.

## Catálogo de Restaurantes

O aplicativo oferece um catálogo de restaurantes, permitindo que você encontre facilmente o que deseja pedir. Ao clicar em um restaurante, você acessa a página de detalhes com informações como horário, avaliação, tempo e taxa de entrega. O cardápio é organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas), com nome, foto, descrição curta e preço de cada item. Itens indisponíveis aparecem como desabilitados com a label "Indisponível".

## Carrinho e Pedidos

O carrinho e os pedidos são o núcleo do aplicativo, onde você pode adicionar itens, confirmar e acompanhar seu pedido. O fluxo é simples e intuitivo, convertendo seu interesse em compra.

## Pagamentos

O aplicativo oferece diversas formas de pagamento, garantindo segurança, praticidade e variedade de métodos. Você pode selecionar o método de pagamento Pix, gerando um QR Code válido por 10 minutos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela após a confirmação.

## Rastreamento de Entrega

Você pode acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta. O aplicativo utiliza um mapa para mostrar a posição do entregador, mas é necessário fechar e reabrir a tela para ver a posição atualizada após 2 minutos de inatividade.

## Avaliações

Após a conclusão do pedido, você pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Bugs e Melhorias

- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada. O aplicativo exibe uma mensagem genérica e não trata o caso corretamente.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar um item sem imagem cadastrada, o aplicativo trava e exibe uma tela branca. O problema ocorre devido a uma exceção não tratada.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após 2 minutos de inatividade. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso de ~5 minutos**: As notificações push de mudança de status do pedido chegam com atraso de aproximadamente 5 minutos após a mudança real de status.
- **Melhoria: Modo escuro**: O aplicativo atualmente só suporta tema claro. A melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional, com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app.
- **Melhoria: Mensagem de erro sem conexão com internet**: Quando o aplicativo é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar a ausência de conexão imediatamente e exibir uma tela amigável com mensagem clara e botão "Tentar novamente".

## Dicas e Sugestões

- Certifique-se de ter uma conexão estável com a internet para evitar problemas de timeout e atrasos nas notificações.
- Ao adicionar itens ao carrinho, verifique se todos possuem imagens cadastradas para evitar travamentos.
- Fique atento à exibição do resumo do pedido, garantindo que o valor do frete esteja correto.
- Para acompanhar a posição do entregador em tempo real, lembre-se de atualizar a tela após 2 minutos de inatividade.
- Expresse sua opinião sobre os restaurantes e entregadores, contribuindo para a melhoria da plataforma.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "autenticação e cadastro de usuário." — fonte(s): SCRUM-1
- "criar uma conta" — fonte(s): SCRUM-1
- "todas as funcionalidades do aplicativo" — fonte(s): SCRUM-1
- "login, recuperação de senha e gerenciamento de perfil." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "catálogo de restaurantes" — fonte(s): SCRUM-2
- "encontre facilmente o que deseja pedir." — fonte(s): SCRUM-2
- "clicar em um restaurante" — fonte(s): SCRUM-12
- "página de detalhes" — fonte(s): SCRUM-12
- "informações como horário, avaliação, tempo e taxa de entrega." — fonte(s): SCRUM-12
- "cardápio é organizado por seções" — fonte(s): SCRUM-12
- "(Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço de cada item." — fonte(s): SCRUM-12
- "Itens indisponíveis aparecem como desabilitados com a label "Indisponível"" — fonte(s): SCRUM-12
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "carrinho e os pedidos são o núcleo do aplicativo" — fonte(s): SCRUM-3
- "adicionar itens, confirmar e acompanhar seu pedido." — fonte(s): SCRUM-3
- "fluxo é simples e intuitivo" — fonte(s): SCRUM-3
- "convertendo seu interesse em compra." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "diversas formas de pagamento" — fonte(s): SCRUM-4
- "segurança, praticidade e variedade de métodos." — fonte(s): SCRUM-4
- "selecionar o método de pagamento Pix" — fonte(s): SCRUM-18
- "QR Code válido por 10 minutos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela após a confirmação." — fonte(s): SCRUM-18
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido" — fonte(s): SCRUM-5
- "a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "mapa para mostrar a posição do entregador" — fonte(s): SCRUM-5
- "fechar e reabrir a tela para ver a posição atualizada após 2 minutos de inatividade." — fonte(s): SCRUM-28
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido" — fonte(s): SCRUM-6
- "expressar sua experiência com o restaurante e o entregador" — fonte(s): SCRUM-6
- "dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "inserir um código de cupom inválido" — fonte(s): SCRUM-29
- "API retorna um erro interno em vez de uma mensagem de erro adequada." — fonte(s): SCRUM-29
- "mensagem genérica" — fonte(s): SCRUM-29
- "não trata o caso corretamente." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "tentar adicionar um item sem imagem cadastrada" — fonte(s): SCRUM-22
- "aplicativo trava e exibe uma tela branca." — fonte(s): SCRUM-22
- "exceção não tratada." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout" — fonte(s): SCRUM-25
- "taxa de entrega é exibida corretamente" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total incorreto." — fonte(s): SCRUM-25
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após 2 minutos de inatividade." — fonte(s): SCRUM-28
- "fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido chegam com atraso de aproximadamente 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "Melhoria: Modo escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro." — fonte(s): SCRUM-33
- "implementar suporte a modo escuro" — fonte(s): SCRUM-33
- "diretrizes de design do sistema operacional" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema e opção manual de alternar nas configurações do app." — fonte(s): SCRUM-33
- "Melhoria: Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "aplicativo é aberto sem conexão com a internet" — fonte(s): SCRUM-31
- "mensagem técnica de timeout." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente" — fonte(s): SCRUM-31
- "tela amigável com mensagem clara e botão "Tentar novamente"" — fonte(s): SCRUM-31
- "conexão estável com a internet" — fonte(s): SCRUM-26
- "problemas de timeout e atrasos nas notificações." — fonte(s): SCRUM-26
- "adicionar itens ao carrinho" — fonte(s): SCRUM-22
- "todos possuem imagens cadastradas" — fonte(s): SCRUM-22
- "travamentos." — fonte(s): SCRUM-22
- "exibição do resumo do pedido" — fonte(s): SCRUM-25
- "valor do frete esteja correto." — fonte(s): SCRUM-25
- "acompanhar a posição do entregador em tempo real" — fonte(s): SCRUM-28
- "atualizar a tela após 2 minutos de inatividade." — fonte(s): SCRUM-28
- "restaurantes e entregadores" — fonte(s): SCRUM-6
- "melhoria da plataforma." — fonte(s): SCRUM-6