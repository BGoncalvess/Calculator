# Autor
- Bruno Gonçalves

# Trello Clone em Python com Flet

Este projeto é um clone do Trello desenvolvido em Python, utilizando a biblioteca Flet para criar uma interface gráfica. A aplicação permite aos utilizadores gerir projetos, organizar tarefas e identificar facilmente quais destas requerem maior atenção. 

Uma das principais inovações é a introdução de colunas personalizáveis dentro dos quadros, adicionando uma camada extra à hierarquia: 

**Quadro → Colunas → Listas → Cartões → Etiquetas**

Esta alteração aumentou a complexidade da aplicação, especialmente na gestão do drag and drop entre colunas, impactando funcionalidades como a remoção de etiquetas, edição de títulos e gestão de etiquetas entre outros.

Este README tem como objetivo descrever o projeto, fornecer instruções claras de configuração para que o utilizador possa executar a aplicação e visualizar as funcionalidades implementadas, incluindo as inovações introduzidas.

---

## Tecnologias Utilizadas

- **Python 3.12**: Linguagem principal do projeto.
- **Flet**: Biblioteca para construção de interfaces gráficas, possibilitando a execução da aplicação em diferentes sistemas operativos.

## Instalação e Configuração

### Pré-requisitos

- Python 3.12.
- Bibliotecas necessárias: `flet`, `itertools`, `typing`.

### Passos para Instalação

1. Clone o repositório:

```bash
git clone https://github.com/BGoncalvess/MobileComputing.git
```

2. Navegue até o diretório do projeto:

```bash
cd MobileComputing/Board
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
ou
uv sync
```

4. Execute a aplicação:

```bash
py src/main.py
```

---

## Funcionalidades Básicas

- **Quadros**: Permitem criar múltiplos quadros para organizar diferentes projetos.
- **Colunas**: Podem ser criadas conforme necessário, com opção de alterar o nome ou eliminá-las após a criação.
- **Listas**: Cada quadro pode conter várias listas, representando etapas ou categorias.
- **Cartões**: Os utilizadores podem adicionar cartões às listas para representar tarefas específicas.
- **Etiquetas**: Podem ser adicionadas aos cartões. Ao clicar numa etiqueta, é possível editá-la ou eliminá-la. O botão "Manage Labels" permite filtrar por lista ou etiqueta.
- **Arrastar e Soltar**: Suporte a drag and drop para mover listas entre colunas e cartões entre listas.
- **Edição e Remoção**: Quadros, colunas, listas, cartões e etiquetas podem ser editados ou eliminados conforme necessário.

---

## Funcionalidades Inovadoras

### Gestão de Etiquetas com Cores

#### Motivo da Inclusão
A gestão de etiquetas com cores foi implementada para proporcionar uma forma visual e intuitiva de categorizar e priorizar tarefas. Inspirada em ferramentas como Trello e Jira, esta funcionalidade permite aos utilizadores identificar rapidamente o tipo, estado ou urgência de um cartão sem precisar de ler todo o seu conteúdo.

#### Descrição Detalhada
- **Adição de Etiquetas**: Cada cartão pode ter múltiplas etiquetas. Ao clicar em "Add Label", o utilizador insere um texto e escolhe uma cor a partir de uma paleta já predefinida.
- **Edição e Remoção**: As etiquetas podem ser editadas (alterando texto ou cor) ou eliminadas ao clicar sobre elas, abrindo um diálogo de opções.
- **Visualização**: As etiquetas são exibidas no cartão com a cor escolhida, numa linha horizontal que suporta várias etiquetas, com texto truncado para manter a interface limpa.
- **Persistência**: As etiquetas e suas cores são armazenadas no estado da aplicação através da classe `InMemoryStore`, garantindo consistência entre colunas e listas.

### Colunas Personalizáveis nos Quadros

#### Motivo da Inclusão
A introdução de colunas personalizáveis foi motivada pela necessidade de oferecer uma estrutura mais flexível, sendo esta inspirada em ferramentas como Jira e Trello já referido anteriormente, esta funcionalidade permite organizar listas em colunas verticais dentro de um quadro.

#### Descrição Detalhada
- **Criação de Colunas**: O botão "Add Column", no topo do quadro, permite criar uma nova coluna com nome e cor personalizados.
- **Gestão de Listas por Coluna**: As listas podem ser atribuídas a colunas específicas durante a criação ou movidas manualmente.
- **Edição e Remoção**: As colunas podem ser editadas (alterando o nome) ou eliminadas (removendo todas as listas associadas) através de botões dedicados no final de cada coluna.
- **Interface Dinâmica**: As colunas ajustam-se à largura do ecrã, com suporte a scroll para listas extensas.

### Dark Mode

#### Motivo da Inclusão
O Dark Mode foi adicionado para melhorar a acessibilidade e a preferencia do utilizador.

#### Descrição Detalhada
- **Alternância de Tema:** O Dark Mode muda o esquema de cores da aplicação para tons escuros, substituindo o fundo claro por um fundo escuro e ajustando as cores de textos e elementos para manter a legibilidade.
- **Implementação:** É ativado por um botão de alternância no menu de opções, atualizando a interface em tempo real.

#### Instruções de Utilização
- Abra a aplicação e encontre o menu de opções (ícone com três pontos).
- Clique em "Enable Dark Mode" para ativar o tema escuro.
- Para voltar ao tema claro, selecione "Disable Dark Mode" no mesmo menu.

#### Valor Acrescentado
- Estética ou preferencia do utilizador, não irá afetar a aplicação.

---

## Estrutura do Projeto

- **`main.py`**: Principal ponto de entrada da aplicação.
- **`app_layout.py`**: Define o layout da interface da aplicação.
- **`board.py`**: Gere a lógica dos quadros e colunas.
- **`board_list.py`**: Gere as listas dentro dos quadros.
- **`item.py`**: Gere os cartões e etiquetas.
- **`data_store.py`**: Interface para armazenamento de dados.
- **`memory_store.py`**: Implementação em memória durante a execução.
- **`user.py`**: Gere informações dos utilizadores.
- **`sidebar.py`**: Gere a barra lateral de navegação.
- **`column_manager.py`**: Gere a criação e gestão de colunas.

---

## Conclusão
A adição de colunas personalizáveis introduziu maior complexidade, especialmente na gestão do drag and drop, exigindo métodos robustos para atualizar a interface e garantir a consistência dos dados. Isso impactou operações como eliminação de etiquetas, edição de títulos e gestão de etiquetas, que se tornaram mais delicadas devido à navegação entre múltiplas camadas. 

Apesar dos desafios, estas funcionalidades aumentam a flexibilidade da aplicação, assemelhando-se a ferramentas como Trello e Jira, e permitem uma organização mais detalhada.

---

## Tabela Resumo de Impactos

| Funcionalidade         | Impacto da Adição de Colunas | Desafios |
|------------------------|-----------------------------|----------------------|
| Drag and Drop entre Colunas | Aumentou a complexidade ao mover listas e cartões | Gestão locais para fazer "drop", feedback visual, Os diversos prints espalhados pela aplicação demonstram um pouco da frustração |
| Eliminar Etiquetas     | Dificultou a localização de cartões | Navegação hierárquica, atualizações de UI |
| Editar Títulos        | Mais camadas para navegar, gestão de estado complexa | Propagação de eventos, consistência de dados |
| Gerir Etiquetas       | Pesquisa mais avançada, sendo possivel procurar por Listas ou Etiquetas | Não consegui gerir num só lugar todas as etiquetas e cores. |

## Melhorias e Evolução Futura

A aplicação, embora funcional, apresenta alguns aspetos para evolução tanto em termos de desempenho como na incorporação de novas funcionalidades. Abaixo, detalho áreas de melhoria e propostas para versões futuras.

### Áreas de Melhoria

#### Código da Aplicação
- **Redundância**: Há partes do código repetidos, que poderiam ser consolidados em métodos reutilizáveis para aumentar a legibilidade e facilitar a manutenção, ou, centralizar as mesmas num ficheiro `utils.py`.
- **Desempenho**: A estrutura apresentada (quadros → colunas → listas → cartões) pode gerar atrasos em interfaces densas, especialmente durante operações de *drag and drop*. Otimizar a gestão de atualizações da UI e reduzir chamadas desnecessárias à *store* seria benéfico.

#### Usabilidade
- **Estado Atual**: Todas as funcionalidades básicas e inovadoras estão operacionais, permitindo uma experiência consistente. Contudo, a complexidade introduzida pelas colunas personalizáveis pode exigir ajustes na interface para garantir maior intuitividade, como realçar alvos de *drop* com mais clareza.

### Funcionalidades Futuras
Para enriquecer a aplicação numa próxima versão, proponho as seguintes adições:

- **Login de Utilizadores**: Implementar autenticação para suportar múltiplos utilizadores, permitindo que cada um aceda aos seus quadros personalizados. Isso poderia integrar um sistema de registo e *login*, armazenando as credenciais na *store*.
- **Persistência de Estado**: Adicionar a capacidade de guardar o estado atual (quadros, colunas, listas, cartões e etiquetas) num ficheiro local ou numa base de dados, restaurando-o ao reabrir a aplicação.
- **Datas de Término**: Associar prazos a listas ou a cartões, exibindo-os na interface para melhor gestão do tempo. Por exemplo, um campo de data poderia ser adicionado ao criar/editar um cartão.
- **Notificações de Prazos**: Implementar alertas visuais (ex., mudança de cor) ou sons para notificar o utilizador quando o prazo (*deadline*) de uma tarefa estiver próximo, como 24 horas antes do término.
- **Avisos para a Equipa**: Permitir o envio de mensagens ou avisos visíveis a todos os membros pertençentes a um quadro, como um painel de notas.

### Benefícios Esperados
Essas melhorias tornariam a aplicação mais eficiente e viável para o uso diário.