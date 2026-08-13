# User Stories

## US-READ-001-001 — Cadastro de livros e consulta da biblioteca pessoal

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-001-001 |
| Capability | READ |
| Feature | READ-001 — Cadastro de livros |
| Requisitos Funcionais | RF-READ-001 e RF-READ-002 |
| Status | Entregue — Sprint 03 concluída |

### Persona

Player autenticado.

### Necessidade

Registrar livros em sua biblioteca pessoal e consultar exclusivamente os livros pertencentes à sua própria biblioteca.

### Valor

Manter uma biblioteca pessoal organizada e disponível para consulta.

### User Story

Como Player autenticado,
quero registrar livros em minha biblioteca pessoal e consultar os livros que cadastrei,
para manter minha biblioteca organizada e disponível para consulta.

### Pré-condições

- O usuário está autenticado.

### Dados funcionais

| Campo | Obrigatoriedade | Observação |
|---|---|---|
| Título | Obrigatório | Sua ausência impede o cadastro. |
| Autor | Obrigatório | Sua ausência impede o cadastro. |
| Quantidade total de páginas | Obrigatório | Sua ausência impede o cadastro. |
| ISBN | Opcional | Sua ausência não impede o cadastro ou a consulta. |
| Editora | Opcional | Sua ausência não impede o cadastro ou a consulta. |
| Edição | Opcional | Sua ausência não impede o cadastro ou a consulta. |
| Capa | Opcional | Sua ausência não impede o cadastro ou a consulta. |
| Gênero | Opcional | Sua ausência não impede o cadastro ou a consulta. |
| Idioma | Opcional | Sua ausência não impede o cadastro ou a consulta. |

Os campos opcionais podem ser informados e persistidos. Eles não participam de regras de negócio específicas nesta User Story, exceto pela validade estrutural básica quando aplicável.

### Regras de negócio

- Todo livro cadastrado deve pertencer ao Player autenticado.
- Título, autor e quantidade total de páginas são obrigatórios.
- A ausência de qualquer campo opcional não impede o cadastro ou a consulta.
- A consulta deve retornar exclusivamente a coleção de livros do Player autenticado.
- A consulta de uma biblioteca sem livros é válida e deve retornar uma coleção vazia.
- Uma biblioteca vazia não constitui erro.
- Nenhum livro pertencente a outro Player pode ser apresentado.
- Nesta User Story, uma biblioteca organizada para consulta significa pertencimento correto ao Player autenticado, retorno consistente da coleção e disponibilidade dos livros cadastrados para consulta.

### Cenários

#### Cenário 1 — Cadastrar livro com os dados obrigatórios

**Dado** que o Player está autenticado
**E** informou título, autor e quantidade total de páginas
**Quando** solicitar o cadastro do livro
**Então** o sistema deverá validar as informações
**E** cadastrar o livro na biblioteca pessoal
**E** associar o livro ao Player autenticado
**E** manter o livro disponível para consulta.

#### Cenário 2 — Cadastrar livro sem campos opcionais

**Dado** que o Player está autenticado
**E** informou todos os dados obrigatórios
**E** não informou um ou mais campos opcionais
**Quando** solicitar o cadastro do livro
**Então** a ausência dos campos opcionais não deverá impedir o cadastro.

#### Cenário 3 — Impedir cadastro sem dado obrigatório

**Dado** que o Player está autenticado
**E** não informou título, autor ou quantidade total de páginas
**Quando** solicitar o cadastro do livro
**Então** o livro não deverá ser cadastrado.

#### Cenário 4 — Consultar biblioteca com livros

**Dado** que o Player está autenticado
**E** possui livros cadastrados em sua biblioteca
**Quando** consultar sua biblioteca pessoal
**Então** o sistema deverá retornar a coleção de livros pertencente ao Player autenticado
**E** os livros cadastrados deverão permanecer disponíveis para consulta.

#### Cenário 5 — Consultar biblioteca vazia

**Dado** que o Player está autenticado
**E** não possui livros cadastrados
**Quando** consultar sua biblioteca pessoal
**Então** o sistema deverá retornar uma coleção vazia
**E** a consulta não deverá ser tratada como erro.

#### Cenário 6 — Preservar isolamento entre Players

**Dado** que existem livros pertencentes a Players diferentes
**Quando** o Player autenticado consultar sua biblioteca pessoal
**Então** o sistema deverá retornar somente os livros pertencentes a esse Player
**E** não deverá apresentar livros de outro Player.

### Critérios de aceite

- O Player autenticado consegue cadastrar um livro ao informar título, autor e quantidade total de páginas.
- O livro cadastrado fica associado ao Player autenticado.
- O livro permanece disponível na biblioteca pessoal para consulta.
- Campos opcionais podem ser informados e persistidos.
- A ausência de campos opcionais não impede o cadastro ou a consulta.
- A consulta retorna exclusivamente os livros pertencentes ao Player autenticado.
- A consulta sem livros retorna uma coleção vazia e não constitui erro.
- Livros pertencentes a outro Player nunca são apresentados.
- A coleção retornada é consistente com os livros cadastrados na biblioteca do Player autenticado.

### Fora do escopo

- RF-READ-003 ou posteriores;
- sessões de leitura;
- páginas lidas;
- progresso percentual;
- tempo de leitura;
- metas;
- streaks;
- filtros;
- busca;
- paginação;
- ordenação configurável;
- agrupamento;
- favoritos;
- status avançados;
- XP;
- Level;
- eventos para GAME;
- Skills;
- achievements;
- badges;
- recomendações;
- Analytics;
- Dashboard;
- integração externa com catálogos de livros;
- consulta externa por ISBN;
- upload de capa;
- funcionalidades sociais;
- compartilhamento.

Uma eventual ordenação técnica determinística pertence à especificação técnica e não constitui requisito funcional desta User Story.

### Rastreabilidade

```text
US-READ-001-001
↓
READ-001
↓
RF-READ-001
↓
RF-READ-002
```

Esta User Story especifica uma candidata funcional. Ela não autoriza o início da Sprint 03 nem qualquer implementação.
## US-READ-002-001 — Registro de sessão de leitura

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-002-001 |
| Capability | READ |
| Feature | READ-002 — Reading Sessions |
| Requisito Funcional | RF-READ-003 |
| Status | Entregue — Sprint 04 concluída |

### Persona

Player autenticado.

### Necessidade

Registrar uma sessão de leitura referente a um livro existente em sua própria biblioteca.

### Valor

Manter um histórico fiel das leituras e das reflexões realizadas em cada sessão.

### User Story

Como Player,
quero registrar uma sessão de leitura de um livro da minha biblioteca,
para manter um histórico fiel das minhas leituras e das reflexões realizadas em cada sessão.

### Pré-condições

- O Player está autenticado.
- O Book existe na biblioteca do Player autenticado.

### Dados funcionais

| Campo | Obrigatoriedade | Observação |
|---|---|---|
| book | Obrigatório | Identifica o Book existente ao qual a sessão pertence. |
| start_page | Obrigatório | Primeira página do intervalo contínuo lido. |
| end_page | Obrigatório | Última página do intervalo contínuo lido. |
| started_at | Obrigatório | Momento de início da sessão. |
| ended_at | Obrigatório | Momento de encerramento da sessão. |
| notes | Opcional | Observações, aprendizados, percepções ou reflexões da sessão. |
| pages_read | Calculado | Não é informado pelo cliente; corresponde a `end_page - start_page + 1`. |

### Princípio de domínio

- Book representa o Asset permanente da biblioteca.
- ReadingSession representa um acontecimento real de leitura.
- Progress permanece futuro e será derivado das sessões.

### Regras de negócio

- **RN-01:** O Book deve existir.
- **RN-02:** O Book deve pertencer ao usuário autenticado.
- **RN-03:** Não é permitido registrar ReadingSession para Book pertencente a outro usuário.
- **RN-04:** `start_page` deve ser maior ou igual a 1.
- **RN-05:** `end_page` deve ser maior ou igual a `start_page`.
- **RN-06:** `end_page` não pode ser maior que `total_pages` do Book.
- **RN-07:** A sessão representa um único intervalo contínuo de páginas.
- **RN-08:** `notes` é opcional.
- **RN-09:** `pages_read` é calculado automaticamente por `end_page - start_page + 1`.
- **RN-10:** ReadingSession representa um fato histórico e não poderá ser editada nesta Feature.

### Cenários

#### Cenário 1 — Registrar sessão válida

**Dado** que o Player está autenticado
**E** selecionou um Book existente em sua biblioteca
**E** informou um intervalo válido e os horários da sessão
**Quando** solicitar o registro
**Então** a ReadingSession deverá ser registrada para o Book selecionado
**E** deverá compor seu histórico de leitura.

#### Cenário 2 — Impedir sessão para Book inexistente

**Dado** que o Player está autenticado
**E** informou um Book inexistente
**Quando** solicitar o registro da sessão
**Então** a ReadingSession não deverá ser registrada.

#### Cenário 3 — Impedir sessão para Book de outro usuário

**Dado** que o Book pertence a outro usuário
**Quando** o Player autenticado solicitar o registro da sessão
**Então** a ReadingSession não deverá ser registrada
**E** o isolamento entre usuários deverá ser preservado.

#### Cenário 4 — Impedir intervalo invertido

**Dado** que `start_page` é maior que `end_page`
**Quando** o Player solicitar o registro
**Então** a ReadingSession não deverá ser registrada.

#### Cenário 5 — Impedir página final além do Book

**Dado** que `end_page` é maior que `total_pages` do Book
**Quando** o Player solicitar o registro
**Então** a ReadingSession não deverá ser registrada.

#### Cenário 6 — Registrar sessão com notes

**Dado** que os dados obrigatórios são válidos
**E** o Player informou `notes`
**Quando** solicitar o registro
**Então** a ReadingSession deverá ser registrada com as observações da sessão.

#### Cenário 7 — Registrar sessão sem notes

**Dado** que os dados obrigatórios são válidos
**E** o Player não informou `notes`
**Quando** solicitar o registro
**Então** a ausência de `notes` não deverá impedir o registro.

#### Cenário 8 — Registrar leitura de uma única página

**Dado** que `start_page` e `end_page` são iguais a 150
**Quando** a sessão for registrada
**Então** `pages_read` deverá ser igual a 1.

#### Cenário 9 — Calcular intervalo com várias páginas

**Dado** que `start_page` é igual a 80
**E** `end_page` é igual a 92
**Quando** a sessão for registrada
**Então** `pages_read` deverá ser igual a 13.

### Critérios de aceite

- Uma sessão válida é registrada para um Book existente da biblioteca do Player autenticado.
- Uma sessão não é registrada quando o Book não existe.
- Uma sessão não é registrada quando o Book pertence a outro usuário.
- Uma sessão não é registrada quando `start_page` é maior que `end_page`.
- Uma sessão não é registrada quando `end_page` supera `total_pages` do Book.
- Uma sessão válida pode ser registrada com `notes`.
- Uma sessão válida pode ser registrada sem `notes`.
- Um intervalo de uma única página produz `pages_read` igual a 1.
- Um intervalo de 80 a 92 produz `pages_read` igual a 13.
- `pages_read` é sempre calculado pelo sistema e nunca informado pelo cliente.

### Fora do escopo

- RF-READ-004 ou posteriores;
- ReadingProgress;
- percentual concluído;
- última página lida;
- Book concluído;
- tempo acumulado;
- velocidade média;
- streak;
- XP;
- Domain Events para GAME;
- GAME;
- Analytics;
- Dashboard;
- AI;
- edição de ReadingSession;
- exclusão de ReadingSession;
- anexos;
- comentários sociais.

### Rastreabilidade

```text
US-READ-002-001
↓
READ-002
↓
RF-READ-003
```

Esta User Story foi entregue com a conclusão da Sprint 04.

## US-READ-003-001 — Consultar progresso de leitura

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-003-001 |
| Capability | READ |
| Feature | READ-003 — Reading Progress |
| Requisito Funcional | RF-READ-004 |
| Status | Entregue — Sprint 05 concluída |

### Persona

Player autenticado.

### Objetivo

Como Player,
quero consultar o progresso atual de leitura de um livro da minha biblioteca,
para saber quanto do livro já li sem depender de um estado de progresso manualmente mantido.

### Pré-condições

- O Player está autenticado.
- O Book existe e pertence à biblioteca do Player autenticado.
- As ReadingSessions consideradas são intervalos válidos já registrados para o Book.

### Semântica oficial

- O progresso é derivado exclusivamente das ReadingSessions existentes do Book.
- Nenhum estado de progresso é persistido no Book.
- Cada página coberta é contada uma única vez, inclusive em sessões sobrepostas ou releituras.
- A ordem cronológica ou de registro das sessões não altera o resultado.
- A maior página alcançada corresponde ao maior `end_page` entre as sessões e é apenas informativa.
- O percentual representa a cobertura real: `(unique_pages_read / total_pages) * 100`.
- O Book está concluído somente quando todas as suas páginas estiverem cobertas por pelo menos uma ReadingSession.

### Dados derivados

| Campo | Definição |
|---|---|
| unique_pages_read | Quantidade de páginas distintas cobertas pelas ReadingSessions. |
| percentage | Percentual de cobertura real das páginas do Book; nunca superior a 100%. |
| highest_page_reached | Maior `end_page` entre as ReadingSessions; inexistente quando não existem sessões. |
| completed | Verdadeiro somente quando todas as páginas do Book estiverem cobertas. |

### Regras de negócio

- **RN-01:** O Book deve pertencer ao Player autenticado.
- **RN-02:** Books de outros usuários não podem ter seu progresso consultado.
- **RN-03:** O owner não é exposto no contrato público.
- **RN-04:** Sem sessões, `unique_pages_read` é 0, `percentage` é 0%, `highest_page_reached` é inexistente e `completed` é falso.
- **RN-05:** Sessões sobrepostas ou repetidas não contam a mesma página mais de uma vez.
- **RN-06:** Sessões não contíguas contribuem apenas com suas páginas efetivamente cobertas.
- **RN-07:** A maior página alcançada não implica que as páginas anteriores tenham sido lidas.
- **RN-08:** A ordem das sessões não altera o resultado.
- **RN-09:** O percentual é calculado por `(unique_pages_read / total_pages) * 100` e não excede 100%.
- **RN-10:** Conclusão exige cobertura de todas as páginas do Book.

### Cenários

#### Cenário 1 — Book sem sessões

**Dado** um Book sem ReadingSessions
**Quando** o Player consultar seu progresso
**Então** as páginas únicas lidas serão 0
**E** o percentual será 0%
**E** não haverá maior página alcançada
**E** o Book não estará concluído.

#### Cenário 2 — Sessões sobrepostas

**Dado** uma sessão de 1 a 20
**E** outra sessão de 15 a 30
**Quando** o progresso for consultado
**Então** as páginas únicas lidas serão 30, e não 36.

#### Cenário 3 — Sessões não contíguas

**Dado** um Book de 100 páginas
**E** sessões de 1 a 20, de 15 a 30 e de 50 a 60
**Quando** o progresso for consultado
**Então** as páginas únicas lidas serão 41
**E** o percentual será 41%
**E** a maior página alcançada será 60
**E** o Book não estará concluído.

#### Cenário 4 — Alcançar a última página sem concluir

**Dado** um Book de 100 páginas
**E** uma sessão de 90 a 100
**Quando** o progresso for consultado
**Então** a maior página alcançada será 100
**E** o Book não estará concluído.

#### Cenário 5 — Releitura

**Dado** uma sessão de 1 a 10
**E** outra sessão de 1 a 10
**Quando** o progresso for consultado
**Então** as páginas únicas lidas serão 10.

#### Cenário 6 — Ordem das sessões

**Dado** o mesmo conjunto de intervalos válidos registrado em ordens diferentes
**Quando** o progresso for consultado
**Então** o resultado será o mesmo.

#### Cenário 7 — Conclusão

**Dado** que as ReadingSessions cobrem todas as páginas do Book ao menos uma vez
**Quando** o progresso for consultado
**Então** o Book estará concluído.

### Critérios de aceite

- O progresso é calculado exclusivamente a partir das ReadingSessions do Book.
- Nenhum estado de progresso é persistido no Book.
- Sobreposições e releituras contam cada página uma única vez.
- Sessões não contíguas produzem cobertura equivalente à união de seus intervalos.
- A ordem das sessões não altera o resultado.
- A maior página alcançada é informativa e não representa sozinha o progresso.
- O percentual representa a cobertura real e nunca excede 100%.
- A conclusão exige cobertura de todas as páginas do Book.
- O progresso somente pode ser consultado pelo owner autenticado, sem exposição do owner.

### Fora do escopo

- persistência de páginas lidas, percentual, última página ou conclusão no Book;
- edição ou exclusão de ReadingSession;
- XP;
- GAME;
- Achievements;
- Streaks;
- Analytics;
- Dashboard;
- AI;
- recomendações;
- metas;
- estatísticas de releitura;
- histórico analítico;
- RF-READ-005 ou posteriores.

### Rastreabilidade

```text
US-READ-003-001
↓
READ-003
↓
RF-READ-004
↓
Sprint 05
```

Esta User Story foi entregue com a conclusão da Sprint 05.
