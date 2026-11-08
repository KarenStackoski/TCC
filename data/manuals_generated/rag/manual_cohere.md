# Manual do Usuário

## Autenticação e Cadastro
O acesso à plataforma é feito através da criação de uma conta, login e recuperação de senha. O gerenciamento de perfil também está incluído nesta funcionalidade.

## Catálogo de Restaurantes
Aqui, o usuário pode visualizar, buscar e filtrar restaurantes e seus cardápios. As informações sobre tempo de entrega, taxa de frete e avaliações estão disponíveis para ajudar o usuário a encontrar o que deseja pedir.

## Carrinho e Pedidos
Esta seção cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É onde a conversão de interesse em compra acontece.

## Pagamentos
A plataforma oferece diversas formas de pagamento, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

## Rastreamento de Entrega
O usuário pode acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

## Avaliações
Após a conclusão do pedido, o usuário pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Visualização do Cardápio
Ao clicar em um restaurante, o usuário acessa a página de detalhes com informações do estabelecimento, como horário, avaliação, tempo e taxa de entrega. O cardápio é organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas), com nome, foto, descrição curta e preço de cada item. Itens indisponíveis aparecem como desabilitados com a label "Indisponível".

## Pagamento com Pix
O usuário pode selecionar Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O app monitora o pagamento em tempo real e avança automaticamente para a próxima tela após a confirmação. Se o QR Code expirar, o usuário pode gerar um novo.

## Modo Escuro
O app atualmente só suporta tema claro, mas está prevista a implementação de suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS). A detecção automática da preferência do sistema e a opção manual de alternar nas configurações do app serão disponibilizadas.

## Bugs e Melhorias
- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom inválido, a API retorna um erro interno em vez de uma mensagem de erro adequada. O app exibe uma mensagem genérica e o backend não trata o caso de cupom não encontrado.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar um item sem imagem cadastrada, o aplicativo para de responder e exibe uma tela branca. Este problema ocorre devido a uma exceção não tratada.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente, mas também é somada erroneamente no campo "Subtotal dos itens", resultando em um total incorreto. O valor cobrado no pagamento é o correto, mas a exibição do resumo precisa ser corrigida.
- **Mensagem de erro sem conexão com internet**: Quando o app é aberto sem conexão com a internet, é exibida uma mensagem técnica de timeout. A melhoria consiste em detectar imediatamente a ausência de conexão e exibir uma tela amigável com uma mensagem clara e um botão para tentar novamente.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso de ~5 minutos**: As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status. Este atraso impacta a percepção de tempo real do acompanhamento.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "criação de uma conta, login e recuperação de senha." — fonte(s): SCRUM-1
- "gerenciamento de perfil" — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "visualizar, buscar e filtrar restaurantes e seus cardápios." — fonte(s): SCRUM-2
- "tempo de entrega, taxa de frete e avaliações" — fonte(s): SCRUM-2
- "encontrar o que deseja pedir." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
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
- "página de detalhes com informações do estabelecimento" — fonte(s): SCRUM-12
- "horário, avaliação, tempo e taxa de entrega." — fonte(s): SCRUM-12
- "cardápio é organizado por seções" — fonte(s): SCRUM-12
- "(Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço de cada item." — fonte(s): SCRUM-12
- "Itens indisponíveis aparecem como desabilitados com a label "Indisponível"" — fonte(s): SCRUM-12
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "selecionar Pix como método de pagamento" — fonte(s): SCRUM-18
- "QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "valor e os dados do beneficiário são exibidos." — fonte(s): SCRUM-18
- "app monitora o pagamento em tempo real" — fonte(s): SCRUM-18
- "avança automaticamente para a próxima tela após a confirmação." — fonte(s): SCRUM-18
- "QR Code expirar, o usuário pode gerar um novo." — fonte(s): SCRUM-18
- "Modo Escuro" — fonte(s): SCRUM-33
- "atualmente só suporta tema claro" — fonte(s): SCRUM-33
- "implementação de suporte a modo escuro" — fonte(s): SCRUM-33
- "diretrizes de design do sistema operacional (Android e iOS)" — fonte(s): SCRUM-33
- "detecção automática da preferência do sistema" — fonte(s): SCRUM-33
- "opção manual de alternar nas configurações do app" — fonte(s): SCRUM-33
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "código de cupom inválido" — fonte(s): SCRUM-29
- "API retorna um erro interno" — fonte(s): SCRUM-29
- "mensagem de erro adequada." — fonte(s): SCRUM-29
- "mensagem genérica" — fonte(s): SCRUM-29
- "backend não trata o caso de cupom não encontrado." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "adicionar um item sem imagem cadastrada" — fonte(s): SCRUM-22
- "aplicativo para de responder" — fonte(s): SCRUM-22
- "tela branca." — fonte(s): SCRUM-22
- "exceção não tratada." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout" — fonte(s): SCRUM-25
- "taxa de entrega é exibida corretamente" — fonte(s): SCRUM-25
- "somada erroneamente no campo "Subtotal dos itens"" — fonte(s): SCRUM-25
- "total incorreto." — fonte(s): SCRUM-25
- "valor cobrado no pagamento é o correto" — fonte(s): SCRUM-25
- "exibição do resumo precisa ser corrigida." — fonte(s): SCRUM-25
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "aberto sem conexão com a internet" — fonte(s): SCRUM-31
- "mensagem técnica de timeout." — fonte(s): SCRUM-31
- "detectar imediatamente a ausência de conexão" — fonte(s): SCRUM-31
- "tela amigável com uma mensagem clara e um botão para tentar novamente." — fonte(s): SCRUM-31
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente" — fonte(s): SCRUM-28
- "tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido" — fonte(s): SCRUM-26
- "atraso médio de 5 minutos" — fonte(s): SCRUM-26
- "mudança real de status." — fonte(s): SCRUM-26
- "impacta a percepção de tempo real do acompanhamento." — fonte(s): SCRUM-26