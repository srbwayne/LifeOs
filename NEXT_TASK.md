# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | READ-005-S09-SLICE-03-PREFLIGHT |
| Iniciativa | READ-005 — Livros Concluídos |
| Status | IMPLEMENTATION PRE-FLIGHT AUTHORIZED — SLICE 3 |
| Tipo | Implementation Pre-Flight |
| Capability | READ |
| Feature | READ-005 — Livros Concluídos |
| Requisito Funcional | RF-READ-005 — Conclusão de Livro |
| User Story | US-READ-005-001 |
| Product Decision | PD-READ-005 — APPROVED |
| Product Identity | FROZEN |
| Completion Model | AUTOMATIC COMPLETION MILESTONE |
| Completion Semantics | APPROVED / FROZEN |
| Product Specification | APPROVED / FROZEN |
| Product Clarification | PRE-EXISTING COMPLETION / BACKFILL APPROVED |
| Architecture Review | APPROVED |
| Architecture Decision | ADR-0042 — ACCEPTED |
| Architecture | APPROVED / FROZEN |
| Technical Plan | APPROVED / FROZEN |
| Technical Plan Document | docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md |
| Human Technical Review | APPROVED |
| Implementation Authorization Review | PASS |
| Human Implementation Authorization | APPROVED |
| Implementation Program | AUTHORIZED |
| Sprint 09 | AUTHORIZED |
| Current Executable Unit | SLICE 3 IMPLEMENTATION PRE-FLIGHT — READ-005 COMPLETION PERSISTENCE |
| Slice 1 Status | INTEGRATED |
| Pre-Slice-2 Remediation Status | FINALIZED |
| Slice 2 Status | INTEGRATED / FINALIZED |
| Slice 3 Status | IMPLEMENTATION PRE-FLIGHT AUTHORIZED / IMPLEMENTATION NOT STARTED |
| Slices 4..8 | NOT EXECUTABLE / GATED |
| Migration 0008 | NOT CREATED |
| Alembic | 0007 (head) |

## Especificação aprovada

- A conclusão ocorre automaticamente na primeira cobertura integral das páginas.
- Cobertura significa páginas únicas cobertas pela união das ReadingSessions.
- Não existe ação manual nem conclusão antecipada.
- O milestone é único por Player + Book e historicamente estável.
- `completed_at` é informação funcional obrigatória, derivada semanticamente do `ended_at` da sessão que provoca a primeira transição.
- Releituras posteriores não alteram a conclusão nem `completed_at`.
- O Book permanece disponível e pode receber novas ReadingSessions.
- Books concluídos devem ser identificáveis pelo Player e historicamente representáveis.
- A ocorrência funcional deve ser disponibilizável externamente; o mecanismo é decisão de arquitetura.
- Efeitos GAME estão fora do escopo e RF-READ-009 permanece deferred.

## Decisão arquitetural aprovada

- BookCompletion dedicado e imutável.
- ReadingProgress continua derivado.
- Book continua sem completion state.
- Session + Completion são atômicos no mesmo UoW e commit.
- Unicidade obrigatória por Player + Book.
- Single logical writer por Book.
- completed_at é persistido semanticamente a partir do ended_at da sessão disparadora.
- Read model dedicado para completion.
- Migration necessária, conceitualmente 0008.
- Backfill dos Books já completos, com reconstrução histórica por ended_at crescente.
- BookCompletion persistido é a fonte durável de verdade.
- Transporte externo durável fica deferred.
- GAME permanece fora do escopo.

## Entregas Existentes

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- READ-004: ENTREGUE.
- READ-006: ENTREGUE.
- READ-007: ENTREGUE.
- RF-READ-001..004: ENTREGUES.
- RF-READ-006: ENTREGUE.
- RF-READ-007: ENTREGUE.
- RF-READ-011: ENTREGUE.

## Implementation Authorization

- Human Implementation Authorization Decision: APPROVED (2026-08-18).
- Implementation Program: AUTHORIZED.
- Sprint 09: AUTHORIZED at program level.
- Slice 1 completed implementation, publication, final review and integration.
- PR #31: MERGED via Rebase and Merge.
- Main after Slice 1 integration: `700d7e9e6c66fb4716323c22ef5c4b3693c8d3de`.
- Main CI run `32212825644`: SUCCESS.
- Slice 2 Architectural / Implementation Authorization Review: PASS.
- Human Slice 2 Authorization: APPROVED (2026-08-19).
- Slice 2 Implementation Pre-Flight was BLOCKED by the pre-existing AUTH/CHARACTER SQLite FK write-order defect.
- PRE-SLICE-2 Remediation Pre-Flight: PASS; Human Technical Review: APPROVED.
- PRE-SLICE-2 Remediation: IMPLEMENTED, REVIEWED, MERGED, and FINALIZED through PR #34.
- Slice 2 prerequisite: RESOLVED.
- Slice 2 Implementation Pre-Flight: PASS; Human Technical Review: APPROVED.
- Slice 2 implementation is authorized only through the frozen two-file allowlist below.
- Slices 3..8 remain NOT EXECUTABLE / GATED.
- Sprint 09 authorization is not blanket permission to implement all slices in one branch or PR.

### PRE-SLICE-2 REMEDIATION CLOSURE — AUTH/CHARACTER SQLITE FK WRITE ORDER

Root cause: disconnected AUTH/CHARACTER ORM persistence ordering under immediate
SQLite foreign-key enforcement.

Resolution:

User save
→ UoW flush
→ Player save
→ UoW flush
→ Character save
→ one final commit

PR: #34 — MERGED.
Main: `f1a1af321a85576d1c8d7cba22cc8adf47167258`.
Main CI: `32433670497` — 3/3 SUCCESS.
Local finalization: PASS.
Tests: 440 passed.
Global process-local SQLite FK diagnostic: 440 passed.
`foreign_key_check`: [].

The prerequisite is RESOLVED.

### SLICE 2 - SQLITE INTEGRITY FOUNDATION — CLOSED / INTEGRATED / FINALIZED

Goal: establish the frozen SQLite foreign-key integrity foundation at shared
Engine/connection infrastructure level.

Frozen implementation mechanism:

- SQLAlchemy Engine-class `connect` listener registered in
  `app/shared/infrastructure/database.py` before runtime Engine creation;
- SQLite guard: `isinstance(dbapi_connection, sqlite3.Connection)`;
- SQLite connections execute `PRAGMA foreign_keys = ON`; non-SQLite connections are no-op;
- the listener does not commit, rollback, change transaction mode, isolation level, or use
  `Connection.autocommit`.

Frozen implementation allowlist:

1. `app/shared/infrastructure/database.py` — centralized SQLite-gated Engine listener only.
2. `tests/shared/infrastructure/test_database.py` — new behavioral infrastructure tests only.

Required tests and invariants:

- fresh and multiple direct SQLite Engine connections report `foreign_keys == 1`;
- invalid FK writes fail, valid FK writes succeed, and `foreign_key_check` is clean;
- Alembic online SQLite connection is covered; non-SQLite callback path executes no PRAGMA;
- runtime, current direct test Engines, and Alembic online Engines are covered;
- repositories remain unaware of PRAGMA policy and the complete suite remains green.

Accepted risks:

- shared database infrastructure must be imported before directly created Engines establish
  connections; all current runtime, test, and Alembic paths satisfy this ordering;
- existing scoped test FK listeners may remain; they are redundant and idempotent;
- the guard intentionally supports only the configured built-in `sqlite3` / pysqlite driver.

Permitted scope when Slice 2 executes:

- Engine-level SQLite connection enforcement;
- `PRAGMA foreign_keys = ON`;
- runtime SQLite connection coverage;
- test SQLite connection coverage;
- Alembic online SQLite connection coverage;
- verification that `PRAGMA foreign_keys == 1`;
- verification that invalid foreign-key writes are rejected;
- verification of clean SQLite foreign-key integrity where appropriate;
- unchanged behavior for non-SQLite databases;
- infrastructure-level tests required by this slice.

Slice 2 must not include BookCompletion ORM models, persistence mappers or repositories;
the `book_completions` table, UNIQUE(book_id), completion indexes, migration 0008 or
backfill; BEGIN IMMEDIATE, retry or ReadingSession + Completion transaction integration;
completion detection orchestration; API, GET /book-completions, BookCompleted, EventBus
changes, GAME or any work from Slices 3..8.

Slice 2 closure evidence:

- PR #37: MERGED.
- Canonical main: `432fbbe415e54a2d3d3fb81d972e52133e9f8977`.
- Main CI `32439884304`: 3/3 SUCCESS.
- Local integration finalization: PASS; infrastructure tests: 5 passed;
  AUTH/CHARACTER regression: 4 passed; full suite: 445 passed.
- Coverage: 98.13%; Alembic: 0007 (head); migration 0008: NOT CREATED.
- Runtime SQLite `foreign_keys == 1`; runtime and existing database
  `foreign_key_check`: []. Alembic online SQLite enforcement: confirmed.

Slice 2 is CLOSED / INTEGRATED / FINALIZED.

### SLICE 3 — COMPLETION PERSISTENCE — IMPLEMENTATION PRE-FLIGHT

Goal: perform a strictly read-only implementation pre-flight for the persistence
foundation of BookCompletion. The pre-flight must inspect the current repository
and determine the smallest valid implementation slice consistent with the frozen
READ-005 Technical Plan. It must not implement anything.

Frozen persistence context to preserve:

- BookCompletion is a dedicated immutable Aggregate Root with `id`, `book_id`
  and `completed_at`; it has no `owner_id`, `user_id` or `updated_at`.
- Ownership is derived through `BookCompletion.book_id → Book.id → Book.owner_id`.
- The planned `book_completions` persistence has `id`, `book_id`, `completed_at`
  and technical `created_at`; it requires UNIQUE(book_id), a book FK using
  RESTRICT / NO ACTION, and `(completed_at, book_id)` indexing.
- Migration 0008 belongs exclusively to Slice 6 and must not be created during
  this pre-flight or future Slice 3 implementation.
- Slice 2 SQLite enforcement is a finalized prerequisite: repositories must not
  execute PRAGMA and the listener must not be duplicated or modified absent a
  new blocker requiring human review.

Authorized read-only investigation:

- BookCompletion domain aggregate and identifier; READ persistence structure;
  BookModel; ReadingSessionModel; mappers; repository ports and SQLAlchemy
  implementations; owner-scoped query patterns; Base/metadata registration;
  persistence exports; dependency wiring only when registration requires it;
  relevant unit/integration and architecture tests; SQLite FK foundation;
  Alembic model-import behavior; ADR-0042; Technical Plan; and this task.
- Determine exact ORM model, mapper, repository contract and owner-safe
  `get_by_book_and_owner(book_id, owner_id)` semantics (or the exact established
  equivalent), metadata uniqueness/FK/index representations, UTC-aware
  `completed_at`, technical `created_at`, current datetime normalization, and
  the mapper/repository/owner-isolation/constraint/timezone test plan.
- Propose the exact smallest implementation allowlist and identify any file
  outside it that would be required.

Slice 3 may plan only BookCompletion ORM persistence, mapper, write repository,
owner-safe lookup, metadata constraints, and focused persistence tests. It must
exclude Slice 4 orchestration, completion detection, BEGIN IMMEDIATE, retries,
concurrency and atomic command integration; Slice 5 read model/API; Slice 6
migration/backfill; Slice 7 BookCompleted/EventBus work; and Slice 8 final
regression/governance. GAME, Noema, Outbox, brokers, RabbitMQ, Kafka and all
Slices 4..8 remain gated.

Implementation is NOT AUTHORIZED. This checkpoint authorizes only the read-only
Slice 3 implementation pre-flight; human review is required after it.

### Deferred slices

3. Completion Persistence.
4. Transactional Write + Concurrency.
5. Dedicated Read Model / API.
6. Migration 0008 + Backfill.
7. Best-Effort Event Seam.
8. Full Regression + Governance.

## Pendências

- READ-005: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION FINALIZED / SLICE 2 FINALIZED / SLICE 3 PRE-FLIGHT AUTHORIZED.
- RF-READ-005: SLICE 1 INTEGRATED / SLICE 2 FINALIZED / SLICE 3 IMPLEMENTATION NOT STARTED.
- US-READ-005-001: SLICE 1 INTEGRATED / SLICE 2 FINALIZED / SLICE 3 IMPLEMENTATION NOT STARTED.
- Migration 0008: NOT CREATED.
- Alembic: 0007 (head).
- READ-008: DEFERRED.
- RF-READ-009: ASSOCIAÇÃO PENDENTE / DEFERRED.
- RF-READ-010: RECONCILIAÇÃO PENDENTE / DEFERRED.
- `/api/v1`: PENDING NON-BLOCKING.
- Pesquisa: OUTSIDE READ-005 / NO FEATURE AUTHORIZED.

## Architecture Boundary

Architecture Decision ADR-0042 está aceita e congelada. O Technical Plan está
aprovado e congelado em docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md.
A autorização humana atual é limitada ao IMPLEMENTATION PRE-FLIGHT read-only da
Slice 3; a implementação da Slice 3 e as Slices 4..8 permanecem gated.

## Próximo Gate

SLICE 3 IMPLEMENTATION PRE-FLIGHT — READ-005 COMPLETION PERSISTENCE

ONLY THE SLICE 3 READ-ONLY IMPLEMENTATION PRE-FLIGHT IS AUTHORIZED.

DO NOT IMPLEMENT SLICE 3.

SPRINT 09 AUTHORIZATION IS PROGRAM-LEVEL AUTHORIZATION, NOT BLANKET PERMISSION.
