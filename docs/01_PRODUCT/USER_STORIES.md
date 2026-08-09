# User Stories

## US-READ-001-001 — Cadastro de livros e consulta da biblioteca pessoal

### Identificação

| Campo | Valor |
|---|---|
| User Story | US-READ-001-001 |
| Capability | READ |
| Feature | READ-001 — Cadastro de livros |
| Requisitos Funcionais | RF-READ-001 e RF-READ-002 |
| Status | Aprovada — Sprint 03 autorizada |

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
