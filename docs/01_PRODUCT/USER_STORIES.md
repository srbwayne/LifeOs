## US-READ-007-001 — Consultar Estatísticas de Leitura

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-007-001 |
| Capability | READ |
| Feature | READ-007 — Estatísticas de Leitura |
| Requisito Funcional | RF-READ-007 |
| Status | Entregue — Sprint 08 concluída |

### Persona

Player autenticado.

### Necessidade

Consultar estatísticas descritivas consolidadas da própria atividade de leitura.

### Valor

Acompanhar quantitativamente a utilização da biblioteca e o histórico de leitura.

### User Story

Como Player autenticado,
quero consultar estatísticas consolidadas da minha atividade de leitura,
para acompanhar quantitativamente minha utilização da biblioteca e meu histórico de leitura.

### Pré-condições

- O Player está autenticado.
- Books e ReadingSessions podem existir ou não; o estado vazio é válido.

### Regras de negócio

- As estatísticas são globais, all-time e exclusivamente owner-scoped.
- O cliente não fornece owner_id, user_id ou identificador equivalente.
- As únicas fontes são Book e ReadingSession.
- A resposta possui exatamente os cinco campos V1.
- `total_books` conta Books do Player.
- `books_with_reading_sessions` conta Books distintos com ao menos uma sessão do mesmo Player.
- `total_reading_sessions` conta todas as sessões do Player.
- `total_pages_read` soma `end_page - start_page + 1` de cada sessão.
- Releituras e intervalos sobrepostos contam novamente; páginas não são deduplicadas.
- `average_pages_per_session` é a divisão do total de páginas pelo total de sessões; sem sessões, é `"0.00"`.
- A média é representada como decimal string com exatamente duas casas e ROUND_HALF_UP.
- O resultado é derivado on demand e não é persistido.
- READ-007 não retorna nem recalcula Progress, Insights, Analytics, ANLT, evolução intelectual, tendências, correlações, predições, scores ou completion.

### Cenários

#### Cenário 1 — Player sem Books e sem sessões

**Dado** que o Player está autenticado e não possui Books nem ReadingSessions
**Quando** consultar `/reading-statistics`
**Então** o sistema deverá retornar 200 com os cinco campos zerados e `average_pages_per_session` igual a `"0.00"`.

#### Cenário 2 — Books sem sessões

**Dado** que o Player possui Books e nenhuma ReadingSession
**Quando** consultar as estatísticas
**Então** `total_books` deverá refletir os Books, os demais totais deverão ser zero e a média deverá ser `"0.00"`.

#### Cenário 3 — Uma sessão

**Dado** que existe uma ReadingSession de 1 a 10
**Quando** consultar as estatísticas
**Então** `total_reading_sessions` deverá ser 1, `total_pages_read` 10 e a média `"10.00"`.

#### Cenário 4 — Múltiplas sessões do mesmo Book

**Dado** que o mesmo Book possui múltiplas ReadingSessions
**Quando** consultar as estatísticas
**Então** o Book deverá contar uma vez em `books_with_reading_sessions` e todas as sessões deverão contar no total.

#### Cenário 5 — Sessões de vários Books

**Dado** que existem sessões pertencentes a vários Books do Player
**Quando** consultar as estatísticas
**Então** Books distintos e todas as sessões deverão ser contabilizados conforme suas definições.

#### Cenário 6 — Releitura ou intervalo sobreposto

**Dado** que existem sessões 1..10 e 5..10
**Quando** consultar as estatísticas
**Então** `total_pages_read` deverá ser 16, sem deduplicação.

#### Cenário 7 — Média fracionária

**Dado** que a divisão entre páginas totais e sessões produz fração
**Quando** consultar as estatísticas
**Então** a média deverá ser serializada com exatamente duas casas e ROUND_HALF_UP.

#### Cenário 8 — Isolamento de ownership

**Dado** que existem dados de Players diferentes
**Quando** o Player autenticado consultar as estatísticas
**Então** somente seus Books e ReadingSessions deverão entrar nos cálculos.

#### Cenário 9 — Requisição não autenticada

**Dado** que a requisição não possui autenticação válida
**Quando** consultar `/reading-statistics`
**Então** o sistema deverá retornar 401.

#### Cenário 10 — Resposta sem outras métricas

**Dado** que a consulta autenticada foi realizada
**Quando** o sistema retornar os indicadores
**Então** a resposta não deverá conter campos de Progress, Insights ou ANLT.

### Critérios de aceite

- `GET /reading-statistics` é global, all-time e owner-scoped.
- A resposta 200 possui exatamente os cinco campos V1.
- Os cálculos são determinísticos e usam somente Book e ReadingSession.
- Empty state retorna 200.
- Releituras e sobreposições contam novamente.
- Média e serialização seguem duas casas e ROUND_HALF_UP.
- Não existem filtros ou parâmetros temporais.
- Requisição sem autenticação retorna 401.
- Não existe persistência estatística.
- Não são retornadas métricas de Progress, Insights ou ANLT.

### Fora do escopo

- READ-003 Progress, READ-004 Insights, READ-008 Evolução Intelectual, ANLT e GAME.
- Estatísticas por Book, sessão ou período, agrupamentos, filtros, drill-down, tendências, correlações, predições, scores e completion.
- Novo estado estatístico persistido, migration, snapshot, cache persistido ou `/api/v1`.

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

## US-READ-004-001 — Consultar Insights de Leitura

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-004-001 |
| Capability | READ |
| Feature | READ-004 — Insights |
| Requisito Funcional | RF-READ-011 |
| Status | Entregue — Sprint 06 concluída |

### Persona

Player autenticado.

### Necessidade

Compreender o estado atual de leitura de um Book por meio de observações claras derivadas dos registros existentes.

### Valor

Tornar a cobertura do Book explicável sem progresso manual, AI ou análise cross-capability.

### User Story

Como Player autenticado,
quero consultar Insights determinísticos sobre a cobertura atual de um livro da minha biblioteca,
para compreender páginas restantes, lacunas e a relação entre página alcançada e cobertura integral.

### Pré-condições

- O Player está autenticado.
- O Book existe e pertence à biblioteca do Player autenticado.
- As ReadingSessions consideradas são válidas, pertencem ao mesmo Book e ao Player autenticado.

### Regras de negócio

- **RN-01:** Insights são derivados exclusivamente de Book, ReadingSessions e ReadingProgress.
- **RN-02:** Nenhum Insight é persistido.
- **RN-03:** Sobreposição e releitura não duplicam páginas na cobertura.
- **RN-04:** Book sem ReadingSessions produz resultado válido.
- **RN-05:** Lacunas são intervalos inclusivos dentro de `1..total_pages`.
- **RN-06:** `highest_page_reached` não representa posição atual.
- **RN-07:** Alcançar a última página não implica cobertura integral.
- **RN-08:** Cobertura integral utiliza somente `ReadingProgress.completed`.
- **RN-09:** Nenhum Insight recomenda ações.
- **RN-10:** Nenhum Insight altera Book, ReadingSession, Character ou GAME.
- **RN-11:** Book inexistente e Book pertencente a outro owner permanecem indistinguíveis publicamente.
- **RN-12:** A V1 é exclusivamente por Book e all-time.

### Insights da V1

#### Cobertura restante

Informa quanto do Book ainda não possui cobertura registrada a partir de `total_pages`, `unique_pages_read` e `percentage`. Releitura não altera o resultado e o Insight não é persistido.

#### Lacunas de cobertura

Informa os intervalos inclusivos do Book ainda sem cobertura, calculados como complemento da união das ReadingSessions dentro de `1..total_pages`. Overlaps e releituras não duplicam cobertura. As lacunas não representam `current_page`, `next_page` ou recomendação.

#### Última página alcançada com lacunas

É aplicável quando `highest_page_reached == total_pages` e `completed == false`, explicando que alcançar a página final não significa cobertura integral. Não recomenda ações e não é persistido.

#### Cobertura integral confirmada

Utiliza somente `ReadingProgress.completed == true` para explicar que todas as páginas possuem cobertura registrada. Não marca o Book como concluído, não persiste status, não gera evento e não antecipa RF-READ-005.

### Cenários

#### Cenário 1 — Book sem ReadingSessions

**Dado** um Book do Player sem ReadingSessions
**Quando** o Player consultar seus Insights
**Então** a cobertura restante será igual a `total_pages`
**E** haverá uma única lacuna inclusiva de `1..total_pages`
**E** o Insight de última página alcançada com lacunas não será aplicável
**E** a cobertura integral será falsa.

#### Cenário 2 — Sessões sobrepostas

**Dado** que as ReadingSessions possuem intervalos sobrepostos
**Quando** os Insights forem calculados
**Então** cada página será considerada apenas uma vez na cobertura.

#### Cenário 3 — Sessões não contíguas

**Dado** que existem intervalos válidos não contíguos
**Quando** os Insights forem calculados
**Então** as lacunas inclusivas entre os intervalos serão explicitadas.

#### Cenário 4 — Última página alcançada sem cobertura integral

**Dado** que `highest_page_reached` é igual a `total_pages`
**E** `completed` é falso
**Quando** os Insights forem consultados
**Então** o sistema informará que existem lacunas
**E** não recomendará uma ação.

#### Cenário 5 — Cobertura integral

**Dado** que todas as páginas possuem cobertura registrada
**Quando** os Insights forem consultados
**Então** a cobertura integral será confirmada
**E** nenhuma conclusão será persistida no Book.

#### Cenário 6 — Book inexistente ou pertencente a outro usuário

**Dado** um Book inexistente ou pertencente a outro usuário
**Quando** o Player solicitar seus Insights
**Então** nenhum Insight será exposto
**E** os dois casos permanecerão indistinguíveis publicamente.

### Critérios de aceite

- Os quatro Insights oficiais são calculados exclusivamente para um Book.
- O período considerado é all-time.
- Os resultados são determinísticos, explicáveis e reproduzíveis.
- Nenhum Insight é persistido.
- Book sem sessões produz resultado válido.
- Cobertura restante e lacunas são calculadas corretamente.
- Sobreposição e releitura não duplicam páginas.
- Alcançar a última página não implica cobertura integral.
- Cobertura integral utiliza somente `ReadingProgress.completed`.
- Nenhum resultado recomenda ações ou usa AI, Analytics ou GAME.
- Nenhum resultado altera Book, ReadingSession ou Character.
- Ownership e indistinguibilidade pública são preservados.

### Fora do escopo

- visão consolidada da biblioteca;
- períodos, dia, semana, mês ou intervalo informado;
- comparação de períodos;
- duração total, duração média ou sessão mais longa;
- frequência ou tendências;
- volume bruto de releitura;
- análise de notes, análise semântica ou sumarização;
- LLM, AI, recomendações ou coaching;
- Analytics, KPIs, scores ou correlações;
- GAME, XP, Level, Skills, Attributes, Rewards ou eventos;
- Streaks ou Achievements;
- Pesquisa;
- Histórico completo ou paginação de ReadingSessions;
- conclusão persistida de Book ou evento de conclusão;
- RF-READ-005;
- RF-READ-006..010;
- alteração de Book ou ReadingSession.

### Rastreabilidade

```text
US-READ-004-001
↓
READ-004 — Insights
↓
RF-READ-011
↓
Sprint 06
```

Esta User Story foi entregue com a conclusão da Sprint 06.

## US-READ-005-001 — Reconhecer Livros Concluídos

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-005-001 |
| Capability | READ |
| Feature | READ-005 — Livros Concluídos |
| Requisito Funcional | RF-READ-005 — Conclusão de Livro |
| Status | Product Specification APPROVED / Implementation NOT AUTHORIZED |

### Persona

Player autenticado.

### Necessidade

Ter um Book reconhecido automaticamente como concluído quando sua atividade de leitura cobrir todas as páginas e conseguir identificar essa conclusão na própria jornada de leitura.

### Valor

Registrar de forma objetiva, estável e historicamente significativa os Books efetivamente concluídos pelo Player sem depender de marcação manual.

### User Story

Como Player autenticado,
quero que um livro seja reconhecido automaticamente como concluído quando minhas ReadingSessions cobrirem todas as suas páginas e que essa conclusão permaneça identificável na minha jornada,
para registrar de forma estável os livros que concluí.

### Pré-condições

- O Player está autenticado.
- O Book pertence ao Player.
- O Book possui `total_pages` válido e positivo.
- A ReadingSession considerada é válida e pertence ao mesmo Player e Book.

### Regras de negócio

- **RN-01:** O cálculo é owner-scoped.
- **RN-02:** A conclusão é automática.
- **RN-03:** 100% de cobertura de páginas únicas é obrigatória.
- **RN-04:** Lacunas impedem conclusão.
- **RN-05:** `highest_page_reached` sozinho não conclui.
- **RN-06:** Overlaps e releituras não duplicam cobertura.
- **RN-07:** A primeira transição para cobertura integral gera o milestone.
- **RN-08:** Existe um único milestone por Player + Book.
- **RN-09:** Não existe conclusão manual ou antecipada.
- **RN-10:** `completed_at` funcional equivale ao `ended_at` da ReadingSession que provoca a primeira transição.
- **RN-11:** Releituras posteriores não alteram conclusão nem `completed_at`.
- **RN-12:** Não existe reversão automática.
- **RN-13:** O Book permanece disponível.
- **RN-14:** Novas ReadingSessions são permitidas após conclusão.
- **RN-15:** Books concluídos devem ser identificáveis pelo Player.
- **RN-16:** A conclusão deve ser historicamente representável.
- **RN-17:** A ocorrência deve ser disponibilizável externamente.
- **RN-18:** READ é autoridade sobre o fato de conclusão.
- **RN-19:** Efeitos GAME não pertencem a esta User Story.
- **RN-20:** Dados de outros Players não participam nem são expostos.

### Cenários

#### Cenário 1 — Cobertura incompleta

**Dado** um Book com lacunas
**Quando** atividade válida for registrada
**Então** nenhum milestone ocorre.

#### Cenário 2 — Última lacuna coberta

**Dado** que a nova ReadingSession cobre a última lacuna
**Quando** a cobertura atinge 100%
**Então** a conclusão ocorre automaticamente.

#### Cenário 3 — Última página com lacunas

**Dado** que a última página foi alcançada, mas há lacunas
**Quando** o progresso for avaliado
**Então** o Book permanece incompleto.

#### Cenário 4 — Releitura após conclusão

**Dado** um Book concluído
**Quando** nova atividade for registrada
**Então** o milestone não se repete e `completed_at` não muda.

#### Cenário 5 — Book disponível

**Dado** um Book concluído
**Quando** o Player consultar a biblioteca ou registrar atividade
**Então** o Book permanece disponível.

#### Cenário 6 — Isolamento de Player

**Dado** atividade pertencente a outro Player
**Quando** a conclusão for avaliada
**Então** ela não participa do cálculo nem é exposta.

#### Cenário 7 — Ocorrência externa

**Dado** que o primeiro milestone ocorreu
**Quando** consumidores autorizados forem considerados
**Então** a ocorrência funcional pode ser disponibilizada sem definir mecanismo ou efeito GAME.

### Critérios de aceite

- A conclusão ocorre automaticamente apenas com 100% de cobertura única.
- Não há conclusão manual, antecipada ou múltipla.
- O milestone é único e historicamente estável.
- `completed_at` usa o `ended_at` da sessão que provoca a primeira transição.
- Releituras não criam novo milestone nem alteram `completed_at`.
- O Book permanece disponível e aceita novas ReadingSessions.
- O Player distingue Books concluídos de incompletos dentro do próprio ownership.
- A conclusão é representável na jornada histórica.
- A ocorrência externa é requisito conceitual, sem mecanismo definido.
- Não há semântica de XP, GAME ou Character.

### Fora do escopo

- conclusão manual;
- conclusão antecipada;
- undo/reopen;
- múltiplas conclusões;
- Pesquisa;
- READ-008;
- RF-READ-009;
- RF-READ-010;
- XP e comportamento GAME;
- ANLT, AI e DASH;
- desenho de API/HTTP;
- `/api/v1`;
- arquitetura;
- mecanismo de persistência;
- transporte de eventos.

### Rastreabilidade

```text
US-READ-005-001
↓
READ-005 — Livros Concluídos
↓
RF-READ-005 — Conclusão de Livro
↓
PD-READ-005
↓
Product Specification APPROVED / FROZEN
```

Implementation NOT AUTHORIZED.

Sprint 09 NOT AUTHORIZED.
## US-READ-006-001 — Consultar Histórico de Leitura

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-006-001 |
| Capability | READ |
| Feature | READ-006 — Histórico |
| Requisito Funcional | RF-READ-006 |
| Status | Entregue — Sprint 07 concluída |

### Persona

Player autenticado.

### Necessidade

Consultar cronologicamente as ReadingSessions já registradas em seu histórico pessoal de leitura.

### Valor

Permitir acesso ao histórico completo de atividades de leitura sem transformá-lo em Analytics, Progress ou jornada consolidada.

### User Story

Como Player autenticado,
quero consultar meu histórico de sessões de leitura,
para revisar cronologicamente as atividades de leitura que registrei.

### Pré-condições

- O Player está autenticado.
- As ReadingSessions retornadas pertencem ao Player autenticado.

### Regras de negócio

- **RN-01:** O histórico é formado exclusivamente por ReadingSessions pertencentes ao Player autenticado.
- **RN-02:** A consulta é global ao Player e não é restrita a um Book.
- **RN-03:** O período da V1 é all-time.
- **RN-04:** As sessões são ordenadas por started_at DESC e id DESC.
- **RN-05:** A consulta é paginada por page e size.
- **RN-06:** page inicia em 1.
- **RN-07:** size possui default 20 e máximo 100.
- **RN-08:** Cada item possui exatamente id, book_id, book_title, start_page, end_page, pages_read, started_at, ended_at e notes.
- **RN-09:** notes é apenas exposto como valor original opcional, sem análise semântica.
- **RN-10:** owner_id não é exposto.
- **RN-11:** Histórico vazio é resultado válido e retorna 200 com coleção vazia.
- **RN-12:** A V1 não possui filtros funcionais.
- **RN-13:** A consulta não altera ReadingSession ou Book.
- **RN-14:** READ-006 não inclui RF-READ-010.
- **RN-15:** A consulta não produz Progress, Insights, Analytics, AI ou GAME.
- **RN-16:** Somente sessões do Player autenticado podem ser retornadas.

### Contrato do item

| Campo | Definição |
|---|---|
| id | Identificador da ReadingSession. |
| book_id | Identificador do Book associado. |
| book_title | Título atual do Book associado à ReadingSession retornada, pertencente ao mesmo contexto autorizado do Player autenticado; integra somente o read model e não é snapshot nem dado persistido na sessão. |
| start_page | Página inicial da sessão. |
| end_page | Página final da sessão. |
| pages_read | Valor derivado de end_page - start_page + 1. |
| started_at | Timestamp funcional de início. |
| ended_at | Timestamp funcional de término. |
| notes | Valor original opcional da sessão. |

Não são expostos owner, timestamps técnicos, duração, Progress, Insights, conclusão, recomendações ou dados GAME.

### Paginação e ordenação

- page: default 1 e mínimo 1.
- size: default 20, mínimo 1 e máximo 100.
- Response: items, page, size, total_items e total_pages.
- total_items representa o total de ReadingSessions owner-scoped do Player autenticado antes do recorte da página atual, independentemente da quantidade de items retornados nessa página.
- total_pages = ceil(total_items / size); sem itens, total_pages é 0.
- Ordenação: started_at DESC e, em empate, id DESC.

### HTTP

- GET /reading-sessions, com autenticação obrigatória.
- Sem path parameters e sem filtros funcionais.
- 200 OK: histórico retornado, inclusive vazio.
- 401 Unauthorized: autenticação ausente ou inválida.
- 422 Unprocessable Entity: paginação inválida.
- 403 e 404 não integram esta consulta global.

### Cenários

#### Cenário 1 — Histórico vazio

**Dado** um Player autenticado sem ReadingSessions
**Quando** consultar GET /reading-sessions
**Então** receberá 200
**E** items será vazio
**E** total_items e total_pages serão 0.

#### Cenário 2 — Histórico com múltiplos livros

**Dado** ReadingSessions de Books diferentes
**Quando** consultar o histórico
**Então** elas poderão aparecer na mesma coleção
**E** cada item incluirá book_id e book_title.

#### Cenário 3 — Ordenação

**Dado** sessões com diferentes started_at
**Quando** consultar o histórico
**Então** a mais recente aparecerá primeiro
**E** empates serão ordenados por id DESC.

#### Cenário 4 — Paginação

**Dado** mais registros que size
**Quando** consultar uma página
**Então** somente seus itens serão retornados
**E** os metadados serão coerentes.

#### Cenário 5 — Notes

**Dado** sessão com notes
**Então** o valor será retornado sem transformação
**E**, quando ausente, notes será null.

#### Cenário 6 — Ownership

**Dado** ReadingSessions de outro Player
**Quando** o Player autenticado consultar seu histórico
**Então** nenhum dado alheio será retornado.

#### Cenário 7 — Paginação inválida

**Dado** page < 1, size < 1 ou size > 100
**Quando** consultar o histórico
**Então** receberá 422.

#### Cenário 8 — Não autenticado

**Dado** um cliente não autenticado
**Quando** consultar o histórico
**Então** receberá 401.

### Critérios de aceite

- Consulta global, all-time e owner-scoped, usando ReadingSessions como fonte.
- Somente RF-READ-006 integra a Sprint 07.
- Nenhum owner é exposto.
- Nove campos exatos por item, incluindo book_title e notes nullable sem análise.
- Ordenação started_at DESC e id DESC.
- Paginação page/size, defaults 1 e 20, size máximo 100; total_items conta todas as ReadingSessions owner-scoped antes do recorte da página e os metadados permanecem coerentes.
- Histórico vazio retorna 200 com coleção vazia.
- Não existem filtros funcionais.
- GET /reading-sessions suporta 200, 401 e 422.
- Nenhuma escrita, alteração de Book/ReadingSession ou evento novo.
- RF-READ-010 e /api/v1 permanecem fora do escopo.
- Nenhum Analytics, AI ou GAME.

### Fora do escopo

- READ-005, RF-READ-005 e RF-READ-010;
- READ-007, READ-008 e RF-READ-009;
- Progress ou Insights agregados;
- filtros, busca ou janela temporal configurável;
- Analytics, KPIs, AI, LLM, recomendações, GAME, XP, Achievements ou Streaks;
- conclusão persistida de Book;
- edição ou exclusão de ReadingSession;
- /api/v1.

### Rastreabilidade

    US-READ-006-001
    ↓
    READ-006 — Histórico
    ↓
    RF-READ-006
    ↓
    Sprint 07

Esta User Story foi entregue com a conclusão da Sprint 07.
