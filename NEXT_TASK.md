# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | Sprint 04 |
| Iniciativa | Sprint 04 — Reading Sessions |
| Status | AUTORIZADA |
| Tipo | Funcional |
| Capability | READ |
| Feature | READ-002 — Reading Sessions |
| User Story | US-READ-002-001 |
| Requisito Funcional | RF-READ-003 |
| Implementação | AINDA NÃO INICIADA |
| Planejamento técnico | PENDENTE |

---

# Objetivo Autorizado

Permitir que o Player registre uma sessão de leitura referente a um livro existente em sua biblioteca.

---

# Princípio de Domínio

- `Book` representa o Asset permanente da biblioteca.
- `ReadingSession` representa um acontecimento real de leitura.
- Progress permanece futuro e será derivado das sessões.

---

# Dados Funcionais

São obrigatórios:

- book;
- start_page;
- end_page;
- started_at;
- ended_at.

É opcional:

- notes.

`pages_read` é calculado automaticamente por `end_page - start_page + 1` e não é informado pelo cliente.

---

# Regras Autorizadas

- O Book deve existir e pertencer ao usuário autenticado.
- Não é permitido registrar ReadingSession para Book pertencente a outro usuário.
- `start_page` deve ser maior ou igual a 1.
- `end_page` deve ser maior ou igual a `start_page` e não pode superar `total_pages` do Book.
- A sessão representa um único intervalo contínuo de páginas.
- `notes` é opcional.
- ReadingSession representa um fato histórico e não poderá ser editada nesta Feature.

---

# Fora do Escopo

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
- edição ou exclusão de ReadingSession;
- anexos;
- comentários sociais.

Qualquer expansão do escopo exige nova autorização explícita do Product Owner.

---

# Execução

A implementação ainda não foi iniciada. O planejamento técnico permanece pendente e deverá seguir o Engineering Playbook, a governança vigente e os required Quality Gates da `main`.

---

# Regra Final

Somente READ-002, RF-READ-003 e US-READ-002-001 estão autorizados para a Sprint 04 — Reading Sessions.

Nenhum RF posterior e nenhuma Sprint funcional adicional estão autorizados.