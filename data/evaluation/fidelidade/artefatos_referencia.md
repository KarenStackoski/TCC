# Artefatos de origem (data/raw/data.json)

## SCRUM-1 — EP-01 — Autenticação e Cadastro

SCRUM-1 — EP-01 — Autenticação e Cadastro (Epic, status: Tarefas pendentes)

Agrupa todas as funcionalidades relacionadas ao acesso do usuário à plataforma, incluindo criação de conta, login, recuperação de senha e gerenciamento de perfil. É a porta de entrada do app e impacta diretamente a experiência inicial do usuário.

## SCRUM-2 — EP-02 — Catálogo de Restaurantes

SCRUM-2 — EP-02 — Catálogo de Restaurantes (Epic, status: Tarefas pendentes)

Engloba a exibição, busca e filtragem de restaurantes e seus cardápios. O usuário precisa encontrar facilmente o que deseja pedir, com informações claras sobre tempo de entrega, taxa de frete e avaliações.

## SCRUM-3 — EP-03 — Carrinho e Pedidos

SCRUM-3 — EP-03 — Carrinho e Pedidos (Epic, status: Tarefas pendentes)

Cobre todo o fluxo desde a adição de itens ao carrinho até a confirmação e acompanhamento do pedido. É o núcleo do app, onde a conversão de interesse em compra acontece.

## SCRUM-4 — EP-04 — Pagamentos

SCRUM-4 — EP-04 — Pagamentos (Epic, status: Tarefas pendentes)

Responsável por todas as formas de pagamento disponíveis na plataforma, garantindo segurança, praticidade e variedade de métodos para o usuário finalizar a compra.

## SCRUM-5 — EP-05 — Rastreamento de Entrega

SCRUM-5 — EP-05 — Rastreamento de Entrega (Epic, status: Tarefas pendentes)

Funcionalidades que permitem ao usuário acompanhar em tempo real onde está o seu pedido, desde a saída do restaurante até a chegada na porta.

## SCRUM-6 — EP-06 — Avaliações

SCRUM-6 — EP-06 — Avaliações (Epic, status: Tarefas pendentes)

Permite que o usuário expresse sua experiência com o restaurante e o entregador após a conclusão do pedido, gerando dados de qualidade para a plataforma.

## SCRUM-7 — US-01 — Cadastro com e-mail e senha

SCRUM-7 — US-01 — Cadastro com e-mail e senha (História, status: Tarefas pendentes)

> *Como usuário novo, quero me cadastrar com e-mail e senha para criar minha conta no app.*

**Descrição:** O usuário acessa a tela de cadastro e preenche nome completo, e-mail e senha. O sistema valida se o e-mail já está cadastrado, se a senha atende aos requisitos mínimos (mínimo 8 caracteres, uma letra maiúscula e um número) e envia um e-mail de confirmação. Somente após confirmar o e-mail o cadastro é ativado.

Critérios de aceitação:
- Campo de e-mail deve validar formato correto
- Senha deve exibir indicador de força
- Exibir mensagem de erro clara se o e-mail já estiver em uso
- E-mail de confirmação enviado em até 1 minuto

## SCRUM-8 — US-02 — Login com Google

SCRUM-8 — US-02 — Login com Google (História, status: Tarefas pendentes)

> *Como usuário, quero fazer login com minha conta Google para acessar o app sem precisar criar uma senha.*

**Descrição:** Na tela de login, o usuário clica em "Entrar com Google" e é redirecionado para o fluxo de autenticação OAuth do Google. Após autenticação bem-sucedida, se for o primeiro acesso, uma conta é criada automaticamente com os dados do perfil Google (nome e foto). Se já tiver conta vinculada, o usuário é autenticado diretamente.

Critérios de aceitação:
- Fluxo OAuth deve funcionar em iOS e Android
- Em primeiro acesso, conta criada automaticamente sem etapas extras
- Token de sessão válido por 30 dias
- Em caso de falha na autenticação, exibir mensagem de erro adequada

## SCRUM-9 — US-03 — Redefinição de senha

SCRUM-9 — US-03 — Redefinição de senha (História, status: Tarefas pendentes)

> *Como usuário, quero redefinir minha senha por e-mail caso eu esqueça minha senha atual.*

**Descrição:** O usuário clica em "Esqueci minha senha" na tela de login, informa seu e-mail e recebe um link de redefinição. O link é válido por 30 minutos e redireciona para uma tela onde o usuário define uma nova senha. Após redefinição, todas as sessões ativas são encerradas por segurança.

Critérios de aceitação:
- Link de redefinição expira em 30 minutos
- Após uso do link, ele não pode ser reutilizado
- Todas as sessões ativas encerradas após troca de senha
- Confirmação visual de sucesso após redefinição

## SCRUM-10 — US-04 — Busca de restaurantes por nome

SCRUM-10 — US-04 — Busca de restaurantes por nome (História, status: Tarefas pendentes)

> *Como usuário, quero buscar restaurantes pelo nome para encontrar rapidamente um estabelecimento específico.*

**Descrição:** Na tela principal, o usuário acessa o campo de busca e digita o nome (parcial ou completo) do restaurante. O sistema retorna resultados em tempo real com debounce de 300ms para evitar requisições excessivas. Os resultados exibem nome, foto, avaliação e tempo estimado de entrega. Caso nenhum resultado seja encontrado, exibe mensagem amigável com sugestões.

Critérios de aceitação:
- Busca insensível a maiúsculas/minúsculas e acentos
- Debounce de 300ms implementado
- Resultados exibidos em até 1 segundo
- Mensagem de "nenhum resultado" com sugestões alternativas

## SCRUM-11 — US-05 — Filtro por categoria

SCRUM-11 — US-05 — Filtro por categoria (História, status: Tarefas pendentes)

> *Como usuário, quero filtrar restaurantes por categoria de culinária para encontrar o tipo de comida que desejo.*

**Descrição:** Na tela principal, o usuário visualiza chips horizontais com as categorias disponíveis (Pizza, Sushi, Hambúrguer, Brasileira, Árabe, Sobremesas, etc.). Ao selecionar uma categoria, a lista de restaurantes é filtrada automaticamente. É possível selecionar múltiplas categorias simultaneamente. O filtro ativo é destacado visualmente e pode ser removido individualmente.

Critérios de aceitação:
- Seleção múltipla de categorias permitida
- Filtro combinável com busca por nome
- Filtro persiste ao rolar a lista
- Botão "Limpar filtros" visível quando algum filtro estiver ativo

## SCRUM-12 — US-06 — Visualização do cardápio

SCRUM-12 — US-06 — Visualização do cardápio (História, status: Tarefas pendentes)

> *Como usuário, quero ver o cardápio completo de um restaurante para escolher o que vou pedir.*

**Descrição:** Ao clicar em um restaurante, o usuário acessa a página de detalhes com banner, informações do estabelecimento (horário, avaliação, tempo e taxa de entrega) e o cardápio organizado por seções (Entradas, Pratos Principais, Bebidas, Sobremesas). Cada item exibe nome, foto, descrição curta e preço. Itens indisponíveis aparecem como desabilitados com label "Indisponível".

Critérios de aceitação:
- Cardápio organizado em seções com navegação por âncora
- Itens indisponíveis exibidos mas não clicáveis
- Foto de cada item (fallback para imagem padrão se não houver)
- Informações do restaurante sempre visíveis no topo

## SCRUM-13 — US-07 — Adicionar itens ao carrinho

SCRUM-13 — US-07 — Adicionar itens ao carrinho (História, status: Tarefas pendentes)

> *Como usuário, quero adicionar itens ao carrinho para montar meu pedido antes de finalizar a compra.*

**Descrição:** O usuário clica em um item do cardápio e uma bottom sheet é exibida com a foto ampliada, descrição completa, opções de personalização (ex: ponto da carne, retirar ingredientes) e quantidade. Ao confirmar, o item é adicionado ao carrinho e um indicador flutuante com o total aparece na tela. O carrinho só pode conter itens de um único restaurante por vez — caso o usuário tente adicionar de outro, um alerta pergunta se deseja limpar o carrinho.

Critérios de aceitação:
- Bottom sheet com opções de personalização quando aplicável
- Alerta ao tentar misturar itens de restaurantes diferentes
- Indicador de carrinho atualizado em tempo real
- Quantidade mínima de 1 e máxima de 20 por item

## SCRUM-14 — US-08 — Aplicar cupom de desconto

SCRUM-14 — US-08 — Aplicar cupom de desconto (História, status: Tarefas pendentes)

> *Como usuário, quero aplicar um cupom de desconto no meu pedido para pagar menos na entrega ou nos itens.*

**Descrição:** Na tela de checkout, o usuário digita o código do cupom em um campo dedicado e clica em "Aplicar". O sistema valida o cupom (existência, validade, valor mínimo de pedido, uso por usuário) e exibe o desconto aplicado no resumo do pedido. Caso inválido, uma mensagem específica informa o motivo (expirado, já utilizado, valor mínimo não atingido).

Critérios de aceitação:
- Validação em tempo real ao clicar em "Aplicar"
- Mensagem de erro específica por tipo de falha
- Desconto exibido de forma destacada no resumo
- Apenas um cupom por pedido

## SCRUM-15 — US-09 — Acompanhamento de status do pedido

SCRUM-15 — US-09 — Acompanhamento de status do pedido (História, status: Tarefas pendentes)

> *Como usuário, quero acompanhar o status do meu pedido em tempo real para saber em que etapa ele está.*

**Descrição:** Após confirmar o pedido, o usuário acessa uma tela de acompanhamento com linha do tempo visual mostrando as etapas: Pedido Recebido → Confirmado pelo Restaurante → Em Preparo → Saiu para Entrega → Entregue. Cada etapa é atualizada via WebSocket em tempo real. O tempo estimado de entrega é exibido e atualizado dinamicamente.

Critérios de aceitação:
- Atualização via WebSocket sem necessidade de recarregar a tela
- Tempo estimado atualizado a cada mudança de status
- Notificação push em cada mudança de status
- Histórico de horários de cada etapa visível

## SCRUM-16 — US-10 — Cancelamento de pedido

SCRUM-16 — US-10 — Cancelamento de pedido (História, status: Tarefas pendentes)

> *Como usuário, quero cancelar meu pedido antes que ele seja aceito pelo restaurante para não ser cobrado por um pedido indesejado.*

**Descrição:** Na tela de acompanhamento, enquanto o pedido estiver no status "Pedido Recebido" (aguardando confirmação do restaurante), um botão "Cancelar Pedido" é exibido. Ao clicar, o usuário informa o motivo do cancelamento (campo obrigatório com opções pré-definidas) e confirma. O estorno é processado automaticamente para o método de pagamento utilizado em até 5 dias úteis.

Critérios de aceitação:
- Cancelamento disponível apenas no status "Pedido Recebido"
- Motivo do cancelamento obrigatório
- Estorno automático iniciado imediatamente
- E-mail de confirmação de cancelamento enviado ao usuário

## SCRUM-17 — US-11 — Pagamento com cartão de crédito

SCRUM-17 — US-11 — Pagamento com cartão de crédito (História, status: Tarefas pendentes)

> *Como usuário, quero pagar meu pedido com cartão de crédito para finalizar a compra de forma segura.*

**Descrição:** Na tela de checkout, o usuário seleciona "Cartão de Crédito" e insere os dados do cartão (número, nome, validade, CVV) em um formulário tokenizado via gateway de pagamento. O sistema exibe as bandeiras aceitas (Visa, Mastercard, Elo, Amex). Após confirmação, o pagamento é processado e o resultado (aprovado/recusado) é exibido imediatamente.

Critérios de aceitação:
- Dados do cartão nunca armazenados no backend da aplicação (tokenização)
- Feedback imediato de aprovação ou recusa
- Mensagem de erro amigável em caso de recusa
- Compatível com 3DS quando exigido pela operadora

## SCRUM-18 — US-12 — Pagamento com Pix

SCRUM-18 — US-12 — Pagamento com Pix (História, status: Tarefas pendentes)

> *Como usuário, quero pagar com Pix para finalizar o pedido de forma instantânea sem usar cartão.*

**Descrição:** O usuário seleciona Pix como método de pagamento e um QR Code é gerado com validade de 10 minutos. O valor e os dados do beneficiário são exibidos. O app monitora o pagamento em tempo real e, ao detectar a confirmação, avança automaticamente para a próxima tela sem necessidade de ação do usuário. Se o QR Code expirar, o usuário pode gerar um novo.

Critérios de aceitação:
- QR Code válido por 10 minutos com contador regressivo visível
- Código Pix copia-e-cola disponível como alternativa ao QR Code
- Detecção automática do pagamento em até 5 segundos após confirmação
- Opção de gerar novo QR Code após expiração

## SCRUM-19 — US-13 — Rastreamento do entregador no mapa

SCRUM-19 — US-13 — Rastreamento do entregador no mapa (História, status: Tarefas pendentes)

> *Como usuário, quero ver a localização do entregador em tempo real no mapa para saber quando meu pedido vai chegar.*

**Descrição:** Após o pedido entrar no status "Saiu para Entrega", a tela de acompanhamento exibe um mapa com a posição atual do entregador (ícone de moto), a localização do restaurante e o endereço de entrega. A posição do entregador é atualizada a cada 10 segundos via WebSocket. O trajeto estimado é desenhado no mapa e o tempo restante é recalculado dinamicamente.

Critérios de aceitação:
- Posição do entregador atualizada a cada 10 segundos
- Trajeto estimado exibido no mapa
- Tempo restante recalculado a cada atualização de posição
- Mapa centralizando automaticamente na posição do entregador

## SCRUM-20 — US-14 — Notificação de saída para entrega

SCRUM-20 — US-14 — Notificação de saída para entrega (História, status: Tarefas pendentes)

> *Como usuário, quero receber uma notificação push quando meu pedido sair para entrega para me preparar para recebê-lo.*

**Descrição:** Quando o status do pedido muda para "Saiu para Entrega", o sistema dispara automaticamente uma notificação push para o dispositivo do usuário com o nome do restaurante, o tempo estimado de entrega e um link direto para a tela de rastreamento. A notificação deve ser enviada mesmo com o app em segundo plano ou fechado.

Critérios de aceitação:
- Notificação enviada em até 5 segundos após mudança de status
- Funciona com app em segundo plano e fechado
- Toque na notificação abre diretamente a tela de rastreamento
- Usuário pode desativar notificações nas configurações do app

## SCRUM-21 — US-15 — Avaliação do restaurante

SCRUM-21 — US-15 — Avaliação do restaurante (História, status: Tarefas pendentes)

> *Como usuário, quero avaliar o restaurante após receber meu pedido para compartilhar minha experiência com outros usuários.*

**Descrição:** Após o pedido ser marcado como entregue, o usuário recebe uma notificação convidando-o a avaliar. Na tela de avaliação, o usuário atribui de 1 a 5 estrelas para o restaurante e pode adicionar um comentário opcional de até 300 caracteres. A avaliação é vinculada ao pedido específico e cada pedido permite apenas uma avaliação. A média de avaliações do restaurante é atualizada em tempo real.

Critérios de aceitação:
- Avaliação disponível por até 7 dias após entrega
- Comentário opcional com limite de 300 caracteres
- Apenas uma avaliação por pedido
- Média do restaurante atualizada imediatamente após envio

## SCRUM-22 — BUG-01 — App trava ao adicionar item sem foto ao carrinho

SCRUM-22 — BUG-01 — App trava ao adicionar item sem foto ao carrinho (Bug, status: Tarefas pendentes)

**Descrição:** Ao tentar adicionar ao carrinho um item do cardápio que não possui imagem cadastrada, o aplicativo para de responder e exibe tela branca. O problema ocorre porque o componente de imagem não trata o caso de URL nula, lançando uma exceção não tratada. Reproduzível em 100% dos casos no Android. No iOS o comportamento é diferente — exibe ícone quebrado mas não trava. **Severidade:** Alta **Passos para reproduzir:** 1) Acessar restaurante "Lanchonete do Zé"; 2) Tentar adicionar o item "Suco de Caju"; 3) App trava.

## SCRUM-23 — BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial

SCRUM-23 — BUG-02 — Filtro de categoria não reseta ao voltar para tela inicial (Bug, status: Tarefas pendentes)

**Descrição:** Quando o usuário seleciona uma categoria (ex: Pizza), navega para um restaurante e volta para a tela inicial, o filtro permanece ativo visualmente mas a lista exibe todos os restaurantes sem filtro aplicado. Há inconsistência entre o estado visual do chip e o estado real da filtragem. **Severidade:** Média **Passos para reproduzir:** 1) Selecionar categoria "Pizza"; 2) Abrir qualquer restaurante; 3) Voltar com o botão de back; 4) Chip aparece selecionado mas lista não está filtrada.

## SCRUM-25 — BUG-03 — Valor do frete somando em dobro no resumo do pedido

SCRUM-25 — BUG-03 — Valor do frete somando em dobro no resumo do pedido (Bug, status: Tarefas pendentes)

**Descrição:** Na tela de checkout, a taxa de entrega é exibida corretamente no campo "Entrega" mas também está sendo somada erroneamente no campo "Subtotal dos itens", fazendo o total ficar incorreto. O valor cobrado no pagamento é o correto — o problema é apenas na exibição do resumo. **Severidade:** Alta (impacto na confiança do usuário mesmo sem impacto financeiro real) **Passos para reproduzir:** 1) Adicionar qualquer item ao carrinho; 2) Avançar para checkout; 3) Observar que subtotal + frete + frete = total exibido.

## SCRUM-26 — BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos

SCRUM-26 — BUG-04 — Notificação de pedido chegando com atraso de ~5 minutos (Bug, status: Tarefas pendentes)

**Descrição:** As notificações push de mudança de status do pedido estão chegando com atraso médio de 5 minutos após a mudança real de status. A causa identificada é um job de envio de notificações que roda em intervalo fixo de 5 minutos em vez de ser disparado por evento. Impacta a percepção de tempo real do acompanhamento. **Severidade:** Média **Ambiente:** Produção. Não reproduzível em desenvolvimento pois o job tem intervalo diferente.

## SCRUM-27 — BUG-05 — Login com Google falha em Android 10

SCRUM-27 — BUG-05 — Login com Google falha em Android 10 (Bug, status: Tarefas pendentes)

**Descrição:** Ao tentar autenticar com Google em dispositivos Android 10 (API 29), o fluxo OAuth redireciona corretamente para a tela de seleção de conta Google, mas ao retornar ao app exibe a mensagem "Falha na autenticação. Tente novamente." sem mais detalhes. Versões Android 11+ funcionam normalmente. Suspeita-se de incompatibilidade com o Custom Tab usado no redirecionamento. **Severidade:** Alta **Dispositivos afetados:** Samsung Galaxy A30, Motorola Moto G7 (ambos Android 10).

## SCRUM-28 — BUG-06 — Tela de rastreamento não atualiza posição automaticamente

SCRUM-28 — BUG-06 — Tela de rastreamento não atualiza posição automaticamente (Bug, status: Tarefas pendentes)

**Descrição:** A posição do entregador no mapa não é atualizada automaticamente após a tela ficar aberta por mais de 2 minutos. A conexão WebSocket está sendo encerrada por inatividade e o app não implementa reconexão automática. O usuário precisa fechar e reabrir a tela para ver a posição atualizada. **Severidade:** Alta (funcionalidade core de rastreamento comprometida) **Passos para reproduzir:** 1) Abrir tela de rastreamento com pedido em andamento; 2) Aguardar 2 minutos sem interagir; 3) Posição do entregador congela no mapa.

## SCRUM-29 — BUG-07 — Cupom inválido retorna erro 500

SCRUM-29 — BUG-07 — Cupom inválido retorna erro 500 (Bug, status: Tarefas pendentes)

**Descrição:** Ao inserir um código de cupom que não existe no sistema, a API retorna HTTP 500 (Internal Server Error) em vez de HTTP 422 com mensagem de erro adequada. O app exibe a mensagem genérica "Erro inesperado. Tente novamente." O backend não está tratando o caso de cupom não encontrado antes de tentar acessar seus atributos, causando NullPointerException. **Severidade:** Média **Endpoint afetado:** `POST /coupons/validate`

## SCRUM-30 — IMP-01 — Skeleton loading nas telas de lista

SCRUM-30 — IMP-01 — Skeleton loading nas telas de lista (Request, status: Tarefas pendentes)

**Descrição:** Atualmente, ao carregar a lista de restaurantes ou o cardápio, a tela exibe um spinner centralizado enquanto os dados são buscados. A melhoria consiste em substituir esse spinner por skeleton screens (placeholders animados no formato dos cards reais), reduzindo a percepção de tempo de carregamento e melhorando a experiência visual. Baseado em padrão amplamente utilizado por apps como iFood e Rappi.

## SCRUM-31 — IMP-02 — Mensagem de erro sem conexão com internet

SCRUM-31 — IMP-02 — Mensagem de erro sem conexão com internet (Request, status: Tarefas pendentes)

**Descrição:** Quando o usuário abre o app sem conexão com a internet, é exibida uma mensagem técnica de timeout após vários segundos de espera. A melhoria consiste em detectar a ausência de conexão imediatamente via listener de rede e exibir uma tela amigável com ícone, mensagem clara ("Sem conexão com a internet") e botão "Tentar novamente", sem aguardar o timeout da requisição.

## SCRUM-32 — IMP-03 — Salvar último endereço de entrega automaticamente

SCRUM-32 — IMP-03 — Salvar último endereço de entrega automaticamente (Request, status: Tarefas pendentes)

**Descrição:** Hoje o usuário precisa digitar o endereço de entrega em cada novo pedido. A melhoria consiste em salvar automaticamente o último endereço utilizado e pré-preencher o campo no próximo checkout, com opção de alterar. Endereços frequentes podem ser salvos como favoritos ("Casa", "Trabalho") acessíveis diretamente na tela de entrega.

## SCRUM-33 — IMP-04 — Modo escuro

SCRUM-33 — IMP-04 — Modo escuro (Request, status: Tarefas pendentes)

**Descrição:** O app atualmente só suporta tema claro. A melhoria consiste em implementar suporte a modo escuro seguindo as diretrizes de design do sistema operacional (Android e iOS), com detecção automática da preferência do sistema e opção manual de alternar nas configurações do app. Todos os componentes, telas e modais devem ser adaptados para garantir contraste e legibilidade adequados.
