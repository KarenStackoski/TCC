# Manual do Usuário

## Autenticação e Cadastro

A primeira etapa de acesso à plataforma envolve a criação de uma conta, login e recuperação de senha, além do gerenciamento de perfil. É a porta de entrada do aplicativo e impacta diretamente a experiência inicial do usuário.

## Catálogo de Restaurantes

O catálogo de restaurantes permite a exibição, busca e filtragem de estabelecimentos e seus cardápios. O usuário pode encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

## Carrinho e Pedidos

O carrinho e pedidos cobrem todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É o núcleo do aplicativo, onde a conversão de interesse em compra acontece.

## Pagamentos

A área de pagamentos oferece diversas formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

## Rastreamento de Entrega

O rastreamento de entrega permite ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

## Avaliações

Após a conclusão do pedido, o usuário pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma.

## Visualização do Cardápio

Ao clicar em um restaurante, o usuário acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados com a etiqueta "Indisponível".

## Pagamento com Pix

O usuário pode selecionar Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O aplicativo monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário. Se o QR Code expirar, o usuário pode gerar um novo.

## Modo Escuro

O aplicativo atualmente só suporta tema claro. A melhoria consiste em implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do aplicativo. Todos os componentes, telas e modais devem ser adaptados para garantir contraste e legibilidade adequados.

## Bugs e Melhorias

- **Cupom inválido retorna erro 500**: Ao inserir um código de cupom que não existe no sistema, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada. O aplicativo exibe a mensagem genérica "Erro inesperado. Tente novamente." O backend não está tratando o caso de cupom não encontrado antes de tentar acessar seus atributos, causando NullPointerException.
- **App trava ao adicionar item sem foto ao carrinho**: Ao tentar adicionar ao carrinho um item do cardápio que não possui imagem cadastrada, o aplicativo para de responder e exibe tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada. Reproduzível em 100% dos casos no Android. No iOS o comportamento é diferente — exibe ícone quebrado mas não trava.
- **Valor do frete somando em dobro no resumo do pedido**: Na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega" mas também está sendo somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto. O valor cobrado no pagamento é o correto — o problema é apenas na exibição do resumo.
- **Mensagem de erro sem conexão com internet**: Quando o usuário abre o aplicativo sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente via listener de rede e exibir uma tela amigável com ícone, mensagem clara ("Sem conexão com a internet") e botão "Tentar novamente", sem aguardar o timeout da requisição.
- **Tela de rastreamento não atualiza posição automaticamente**: A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. A conexão WebSocket está sendo encerrada por inatividade e o aplicativo não implementa reconexão automática. O usuário precisa fechar e reabrir a tela para ver a posição atualizada.
- **Notificação de pedido chegando com atraso de ~5 minutos**: As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status. A causa identificada é um job de envio de notificações que roda em intervalo fixo de 5 minutos em vez de ser disparado por evento. Impacta a percepção de tempo real do acompanhamento.

---

**Citações (Cohere Command R):**

- "Autenticação e Cadastro" — fonte(s): SCRUM-1
- "criação de uma conta, login e recuperação de senha, além do gerenciamento de perfil." — fonte(s): SCRUM-1
- "porta de entrada do aplicativo e impacta diretamente a experiência inicial do usuário." — fonte(s): SCRUM-1
- "Catálogo de Restaurantes" — fonte(s): SCRUM-2
- "exibição, busca e filtragem de estabelecimentos e seus cardápios." — fonte(s): SCRUM-2
- "encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações." — fonte(s): SCRUM-2
- "Carrinho e Pedidos" — fonte(s): SCRUM-3
- "todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido." — fonte(s): SCRUM-3
- "núcleo do aplicativo, onde a conversão de interesse em compra acontece." — fonte(s): SCRUM-3
- "Pagamentos" — fonte(s): SCRUM-4
- "diversas formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra." — fonte(s): SCRUM-4
- "Rastreamento de Entrega" — fonte(s): SCRUM-5
- "acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta." — fonte(s): SCRUM-5
- "Avaliações" — fonte(s): SCRUM-6
- "conclusão do pedido, o usuário pode expressar sua experiência com o restaurante e o entregador, gerando dados de qualidade para a plataforma." — fonte(s): SCRUM-6
- "Visualização do Cardápio" — fonte(s): SCRUM-12
- "página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas)" — fonte(s): SCRUM-12
- "nome, foto, descrição curta e preço." — fonte(s): SCRUM-12
- "indisponíveis aparecem como desabilitados com a etiqueta "Indisponível"" — fonte(s): SCRUM-12
- "Pagamento com Pix" — fonte(s): SCRUM-18
- "selecionar Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos." — fonte(s): SCRUM-18
- "dados do beneficiário são exibidos." — fonte(s): SCRUM-18
- "monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário." — fonte(s): SCRUM-18
- "QR Code expirar, o usuário pode gerar um novo." — fonte(s): SCRUM-18
- "Modo Escuro" — fonte(s): SCRUM-33
- "suporta tema claro." — fonte(s): SCRUM-33
- "implementar suporte a modo escuro, seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do aplicativo." — fonte(s): SCRUM-33
- "componentes, telas e modais devem ser adaptados para garantir contraste e legibilidade adequados." — fonte(s): SCRUM-33
- "Cupom inválido retorna erro 500" — fonte(s): SCRUM-29
- "código de cupom que não existe no sistema, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada." — fonte(s): SCRUM-29
- "mensagem genérica "Erro inesperado. Tente novamente."" — fonte(s): SCRUM-29
- "backend não está tratando o caso de cupom não encontrado antes de tentar acessar seus atributos, causando NullPointerException." — fonte(s): SCRUM-29
- "App trava ao adicionar item sem foto ao carrinho" — fonte(s): SCRUM-22
- "adicionar ao carrinho um item do cardápio que não possui imagem cadastrada, o aplicativo para de responder e exibe tela branca." — fonte(s): SCRUM-22
- "componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada." — fonte(s): SCRUM-22
- "Reproduzível em 100% dos casos no Android." — fonte(s): SCRUM-22
- "iOS o comportamento é diferente — exibe ícone quebrado mas não trava." — fonte(s): SCRUM-22
- "Valor do frete somando em dobro no resumo do pedido" — fonte(s): SCRUM-25
- "tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega" mas também está sendo somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto." — fonte(s): SCRUM-25
- "valor cobrado no pagamento é o correto — o problema é apenas na exibição do resumo." — fonte(s): SCRUM-25
- "Mensagem de erro sem conexão com internet" — fonte(s): SCRUM-31
- "abre o aplicativo sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera." — fonte(s): SCRUM-31
- "detectar a ausência de conexão imediatamente via listener de rede e exibir uma tela amigável com ícone, mensagem clara ("Sem conexão com a internet") e botão "Tentar novamente", sem aguardar o timeout da requisição." — fonte(s): SCRUM-31
- "Tela de rastreamento não atualiza posição automaticamente" — fonte(s): SCRUM-28
- "posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos." — fonte(s): SCRUM-28
- "conexão WebSocket está sendo encerrada por inatividade e o aplicativo não implementa reconexão automática." — fonte(s): SCRUM-28
- "fechar e reabrir a tela para ver a posição atualizada." — fonte(s): SCRUM-28
- "Notificação de pedido chegando com atraso de ~5 minutos" — fonte(s): SCRUM-26
- "notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status." — fonte(s): SCRUM-26
- "job de envio de notificações que roda em intervalo fixo de 5 minutos em vez de ser disparado por evento." — fonte(s): SCRUM-26
- "percepção de tempo real do acompanhamento." — fonte(s): SCRUM-26