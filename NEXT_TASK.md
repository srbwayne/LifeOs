# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | Sprint 03 |
| Iniciativa | Sprint 03 — Reading Library |
| Status | AUTORIZADA |
| Tipo | Funcional |
| Capability | READ |
| Feature | READ-001 — Cadastro de livros e consulta da biblioteca |
| User Story | US-READ-001-001 |
| Requisitos Funcionais | RF-READ-001 e RF-READ-002 |

---

# Objetivo Autorizado

Permitir que o Player autenticado cadastre livros em sua biblioteca pessoal e consulte exclusivamente os livros associados ao próprio Player.

---

# Dados Funcionais

São obrigatórios:

- título;
- autor;
- quantidade total de páginas.

São opcionais:

- ISBN;
- editora;
- edição;
- capa;
- gênero;
- idioma.

Os campos opcionais podem ser informados, não influenciam regras de negócio nesta Sprint e sua ausência não bloqueia o cadastro.

---

# Comportamentos Autorizados

- Cada livro pertence a um único Player.
- Um Player não pode consultar livros de outro Player.
- A consulta de uma biblioteca vazia é válida e retorna uma coleção vazia.
- Nesta Sprint, biblioteca organizada significa pertencimento correto ao Player autenticado, retorno consistente da coleção e disponibilidade dos livros cadastrados para consulta.

---

# Fora do Escopo

- RF-READ-003 ou qualquer RF posterior;
- filtros;
- busca;
- paginação;
- ordenação configurável;
- sessões de leitura;
- progresso;
- páginas lidas;
- tempo de leitura;
- XP;
- GAME;
- Analytics;
- Dashboard;
- AI.

Qualquer expansão do escopo exige nova autorização explícita do Product Owner.

---

# Execução

A implementação deverá seguir o Engineering Playbook, a governança vigente e os required Quality Gates da `main`.

A autorização desta Sprint não define schema, ORM, endpoints, migrations ou outras decisões técnicas, que pertencem ao planejamento técnico autorizado posteriormente.

---

# Regra Final

Somente READ-001, RF-READ-001, RF-READ-002 e US-READ-001-001 estão autorizados para a Sprint 03 — Reading Library.
