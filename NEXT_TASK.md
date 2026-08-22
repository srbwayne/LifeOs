# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | READ-005-S09-SLICE-03 |
| Iniciativa | READ-005 — Livros Concluídos |
| Status | IMPLEMENTATION AUTHORIZED — SLICE 3 READY |
| Tipo | Implementation |
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
| Current Executable Unit | SLICE 3 IMPLEMENTATION — READ-005 COMPLETION PERSISTENCE |
| Slice 1 Status | INTEGRATED |
| Pre-Slice-2 Remediation Status | FINALIZED |
| Slice 2 Status | INTEGRATED / FINALIZED |
| Slice 3 Status | IMPLEMENTATION AUTHORIZED / IMPLEMENTATION NOT STARTED |
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

### SLICE 3 — COMPLETION PERSISTENCE — IMPLEMENTATION AUTHORIZED

The strictly read-only Slice 3 implementation pre-flight: PASS. Human Technical
Review: APPROVED. Implementation Authorization Review: APPROVED. Slice 3 is the
only implementation unit now authorized; implementation has not started.

Frozen domain and ownership contract:

- BookCompletion remains a dedicated immutable Aggregate Root with `id`,
  `book_id`, and `completed_at`; it has no `owner_id`, `user_id`, or `updated_at`.
  Book, ReadingProgress, and the domain aggregate remain unchanged.
- Domain ownership is derived through `BookCompletion.book_id → Book.id → Book.owner_id`.
  The persistence owner-safe lookup derives through
  `BookCompletionModel.book_id → BookModel.id → BookModel.user_id`. The table
  must not persist an owner/user identifier. Wrong-owner lookup returns `None`.
- The repository port is `IBookCompletionRepository`, with exactly
  `save(completion)` and `get_by_book_and_owner(book_id, owner_id)`. The latter
  joins `BookCompletionModel` to `BookModel`, filters completion `book_id` and
  `BookModel.user_id`, and returns `BookCompletion | None`.

Frozen ORM, mapper, and repository contract:

- New `BookCompletionModel` maps `book_completions`: `id` String(26) primary key;
  required and unique `book_id` String(26); required `completed_at`
  DateTime(timezone=True); persistence-only technical `created_at` DateTime with
  the established Python-side `datetime.datetime.now` default. It has no
  relationship, owner/user field, `updated_at`, or cascade.
- `book_id` uses `ForeignKey("books.id", ondelete="RESTRICT")`; one single-column
  uniqueness mechanism (`mapped_column(..., unique=True)`) and no redundant
  standalone non-unique book index. The required composite metadata index is
  `Index("ix_book_completions_completed_at_book_id", "completed_at", "book_id")`.
- `BookCompletionMapper` maps IDs with `to_persistence()` / `from_value()`.
  On load it must call existing `canonicalize_utc_datetime(model.completed_at)`
  before `BookCompletion.restore()`. SQLite may return a naive datetime; the
  domain invariant must not be weakened.
- `SqlAlchemyBookCompletionRepository` receives a Session, uses
  `session.add(BookCompletionMapper.to_persistence(completion))`, and does not
  commit, flush, merge, upsert, replace, update, or execute PRAGMA. The caller/UoW
  owns commit and flush; duplicate Book completion is a database uniqueness error.

Frozen implementation allowlist — exactly six new files; a seventh file requires
human review and STOP:

1. `app/read/domain/ports/book_completion_repository.py`
2. `app/read/infrastructure/persistence/models/book_completion_model.py`
3. `app/read/infrastructure/persistence/mappers/book_completion_mapper.py`
4. `app/read/infrastructure/persistence/repositories/book_completion_repository.py`
5. `tests/read/integration/test_book_completion_mapper.py`
6. `tests/read/integration/test_book_completion_repository.py`

Tests must use disposable SQLite plus explicit model import and
`Base.metadata.create_all/drop_all`, not migration 0008. They cover mapper ID and
UTC round trips; SQLite-naive restoration; save/rollback; owner isolation;
uniqueness; valid/invalid FK; `foreign_keys == 1`; `foreign_key_check == []`;
created_at; composite index; RESTRICT deletion rollback; and no merge/upsert.

Migration 0008, Alembic model-import registration, production schema deployment,
backfill, downgrade/re-upgrade remain Slice 6 only. `migrations/env.py` remains
unchanged. Slice 2 Engine-level SQLite enforcement is mandatory and unchanged;
new repositories must rely on it without a listener or PRAGMA.

Accepted risk — MINOR: SQLite strips timezone information from
`DateTime(timezone=True)` round trips. Mandatory mitigation is mapper use of the
existing UTC canonicalizer before domain restoration. Accepted information
boundary: Alembic explicitly imports models, and BookCompletion registration is
owned by Slice 6.

Slice 3 excludes all Slice 4 orchestration, detection, BEGIN IMMEDIATE, retries,
concurrency, locks, and atomic ReadingSession flow; Slice 5 API/read model,
pagination, count/list methods, and DTOs; Slice 6 migration work; Slice 7 events
and EventBus; Slice 8 final closure; GAME, Noema, Outbox, RabbitMQ, Kafka, and
broker work. Slices 4..8 remain gated.

### Deferred slices

3. Completion Persistence.
4. Transactional Write + Concurrency.
5. Dedicated Read Model / API.
6. Migration 0008 + Backfill.
7. Best-Effort Event Seam.
8. Full Regression + Governance.

## Pendências

- READ-005: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION FINALIZED / SLICE 2 FINALIZED / SLICE 3 IMPLEMENTATION AUTHORIZED.
- RF-READ-005: SLICE 1 INTEGRATED / SLICE 2 FINALIZED / SLICE 3 IMPLEMENTATION AUTHORIZED / NOT STARTED.
- US-READ-005-001: SLICE 1 INTEGRATED / SLICE 2 FINALIZED / SLICE 3 IMPLEMENTATION AUTHORIZED / NOT STARTED.
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
A autorização humana atual é limitada à implementação congelada de seis arquivos
da Slice 3; as Slices 4..8 permanecem gated.

## Próximo Gate

SLICE 3 IMPLEMENTATION — READ-005 COMPLETION PERSISTENCE

ONLY THE FROZEN SIX-FILE SLICE 3 IMPLEMENTATION IS AUTHORIZED.

DO NOT START SLICE 4 OR IMPLEMENT OUTSIDE THE ALLOWLIST.

SPRINT 09 AUTHORIZATION IS PROGRAM-LEVEL AUTHORIZATION, NOT BLANKET PERMISSION.
