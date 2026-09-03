# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | READ-005-S09-SLICE4-INTEGRATION-AUTHORIZATION-REVIEW |
| Iniciativa | READ-005 — Livros Concluídos |
| Status | INTEGRATION AUTHORIZATION REVIEW PENDING / EXECUTABLE |
| Tipo | Slice 4 Python 3.11 Rebase + Remediation Authorization Review |
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
| Current Executable Unit | PR #46 READY + INTEGRATION AUTHORIZATION REVIEW |
| Slice 1 Status | INTEGRATED |
| Pre-Slice-2 Remediation Status | FINALIZED |
| Slice 2 Status | INTEGRATED / FINALIZED |
| Slice 3 Status | INTEGRATED / FINALIZED |
| Slice 4 Status | IMPLEMENTED / REBASED ON PYTHON 3.11 MAIN / PYTHON 3.11 REMEDIATED / LOCAL FINAL REVIEW PASS / PUBLISHED IN DRAFT PR #46 / PR CI PYTHON 3.11 3/3 SUCCESS / REMOTE FINAL REVIEW PASS / MERGE BLOCKED PENDING INTEGRATION AUTHORIZATION / RUNTIME ACTIVATION BLOCKED PENDING COORDINATED CUTOVER |
| Slice 5 Status | GATED |
| Slice 6 Status | MIGRATION 0008 + BACKFILL IMPLEMENTATION INTEGRATED / REAL-DATA APPLICATION NOT EXECUTED / COORDINATED CUTOVER NOT EXECUTED |
| Slice 7 Status | GATED |
| Slice 8 Status | GATED |
| Migration 0008 | CODE INTEGRATED / REAL LOCAL DATABASE NOT APPLIED |
| Alembic | Repository: 0008 (head); real `lifeos.db`: 0007 |
| Slice 4 PR | #46 — OPEN / DRAFT |
| Slice 4 PR Head | `3f23cdb4f991a0c8381801378b2b0f70267f7d97` |
| Slice 4 PR CI | `33701876559` — 3/3 SUCCESS |
| Slice 4 PR Topology | ahead 1 / behind 0 relative to `main` |
| Slice 4 Remote Final Review | PASS |
| Slice 4 Validation | Python >=3.11 / 483 tests / 98.11% coverage |
| Current Integrated Python Platform | >=3.11 |
| Current Required Branch Checks | Static quality (Python 3.11); Tests and coverage (Python 3.11); Alembic migration (Python 3.11) |
| Python 3.11 Platform Transition | INTEGRATED / FINALIZED |
| Platform PR | #49 — MERGED |
| Platform Main | `f62d4798560cf36025cee021b34c5fb10462cff3` |
| Platform Main CI | `33697509650` — 3/3 SUCCESS |
| Platform Baseline | 465 tests / 98.16% coverage |

## Limite atual de autorização

Python >=3.11 está integrado em `main` pelo PR #49, e a proteção da branch exige
`Static quality (Python 3.11)`, `Tests and coverage (Python 3.11)` e
`Alembic migration (Python 3.11)`.

**AUTHORIZED NOW:** PR #46 READY + INTEGRATION AUTHORIZATION REVIEW.

**NOT YET AUTHORIZED:**

- marcar PR #46 Ready;
- merge PR #46.

- aplicar Migration 0008 a dados reais;
- executar o cutover coordenado;
- ativar o runtime Slice 4.

O CI Python 3.10 `33457790140` permanece apenas como evidência histórica. PR #46
foi rebased, remediado e validado em Python 3.11; Ready e integração aguardam
autorização explícita.

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

### SLICE 3 — COMPLETION PERSISTENCE — CLOSED / INTEGRATED / FINALIZED

Slice 3 implementation pre-flight: PASS. Human Technical Review: APPROVED.
Implementation Authorization Review: APPROVED. PR #40 is MERGED; authorized head
`00bc7b4f38e52358970b600f6a5c6064bc38a63a` was integrated into canonical main
`5674df21fcd40fb3e1c29bf3e4d0c303248ec5a0` (parent
`8803474ab748f96cc2fac10704d20b3303789674`). Main CI `32611356740`: 3/3 SUCCESS.
Local integration finalization: PASS.

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

Slice 3 validation and closure evidence:

- exact integrated scope: the six frozen port/model/mapper/repository/test files;
  no existing Slice 3 file changed and no unexpected file was added;
- mapper tests: 5 passed; repository tests: 9 passed; architecture: 12 passed;
  full and DeprecationWarning-as-error suites: 459 passed; coverage: 98.16%;
  Alembic: 0007 (head);
- runtime SQLite `foreign_keys == 1` and `foreign_key_check == []`; existing
  `lifeos.db` remains Alembic 0007 with clean `foreign_key_check` and no
  `book_completions` deployment; migration 0008 remains absent.

Slice 3 is CLOSED / INTEGRATED / FINALIZED. Its frozen persistence contract above
is preserved as completed evidence. No Slice 4+ implementation was introduced.

### SLICE 4 — TRANSACTIONAL WRITE AND CONCURRENCY — IMPLEMENTED / PUBLISHED / MERGE BLOCKED

Slice 4 Implementation Authorization is APPROVED. The implementation, local final
review, atomicity evidence remediation, and final remediated commit review all
passed. The six-file authorized implementation is complete at commit
`151a519291a785f86856c685880f441b8b3bc510` and is published in PR #46, which
remains OPEN / DRAFT.

PR CI `33457790140` failed on the current integrated Python 3.10 platform: its
stdlib `sqlite3` does not expose the public numeric SQLite error-code API required
by the frozen `SQLITE_BUSY` classifier. This is a PLATFORM PREREQUISITE, not a
change to the frozen retry semantics. Slice 4 merge is blocked pending a separately
reviewed, implemented, and integrated Python >=3.11 platform transition.

Human Technical Decision: APPROVED — OPTION B. The future LifeOS platform is
Python >=3.11; the transition implementation is AUTHORIZED / NOT STARTED. The
current integrated platform and required
branch checks remain Python 3.10. Runtime activation remains separately forbidden
until Migration 0008 has been applied and fully backfilled under the coordinated
cutover below.

### COORDINATED MIGRATION 0008 + SLICE 4 RUNTIME CUTOVER — FROZEN

Semantic slice identities and BookCompletion semantics are preserved. Execution
and deployment order are amended: Migration 0008 + Backfill and Slice 4 remain
separate implementation/review scopes, but they are not independent deployment
units.

For every writable environment, the required sequence is:

1. create and verify a backup;
2. exclude ReadingSession write traffic and stop old writable application instances;
3. validate pre-migration database integrity;
4. apply Migration 0008, containing Completion schema, constraints, indexes, and
   complete historical backfill;
5. validate Alembic revision, schema, FK integrity, uniqueness, and historical
   backfill invariants;
6. start only the Slice 4-capable runtime and verify health;
7. re-enable ReadingSession write traffic.

No ReadingSession write may occur from the start of historical backfill until the
Slice 4-capable runtime is active. The following are invalid: migration/backfill
with an old writable ReadingSession runtime, and schema-only activation followed
by later historical backfill. Neither runtime schema fallback nor completion
timestamp rewriting is permitted.

Migration 0008 remains one cohesive schema + full-backfill migration. Its code is
integrated at repository Alembic head 0008; real-data application remains pending
the coordinated cutover. Do not split the backfill into 0009 and do not add
provenance state.

The retry policy frozen for the completed Slice 4 implementation remains: two total
write-intent acquisition attempts, fixed 50 ms delay, no jitter, and retry only
for `OperationalError` wrapping `sqlite3.OperationalError` with
`sqlite_errorcode == SQLITE_BUSY` before relevant reads, writes, tracking, flush,
or commit. Never retry after acquisition, `SQLITE_LOCKED`, IntegrityError, domain
or owner failure, flush, commit, ambiguous commit, publication, or unknown error.

`SqlAlchemyUnitOfWork.rollback()` not clearing `_tracked_aggregates` remains INFO:
no remediation is required while retry stays acquisition-only before tracking.

### MIGRATION 0008 + BACKFILL — INITIAL PREFLIGHT BLOCKERS RESOLVED / RESUME AUTHORIZED

The initial strictly read-only Migration 0008 + Backfill pre-flight completed
and was BLOCKED by two governance issues: documentation described a canonical
26-character TSID although pinned `tsidpy==1.1.5` produces and validates the
canonical 13-character representation; and schema 0007 permits historical
owner-consistent page intervals outside a Book's current total_pages.

Human data-integrity remediation is APPROVED. Canonical TSID representation is
defined behaviorally by the pinned dependency's round-trip, not by a length;
`VARCHAR(26)` remains unchanged persistence capacity. No domain, value object,
model, existing ID, or dependency change is authorized or required.

For each owner-consistent source row, backfill must validate page bounds against
the current Book and a readable, deterministically orderable ended_at. Any
unrepresentable source history aborts 0008 before DDL; no clamp, truncation,
silent exclusion, rewrite, deletion, repair, or synthetic historical total_pages
is permitted. Owner-mismatched sessions remain excluded from coverage and do not
independently block migration. FK integrity violations remain independent
blockers.

SQLite partial-DDL risk is accepted only under the already frozen backup,
traffic-exclusion, failed-start, post-migration verification, and coordinated
cutover controls. All source validation, full candidate computation,
migration-local TSID generation/validation, and explicit technical created_at
selection must complete before the first 0008 DDL.

At the blocked pre-flight stage, the conditional three-file candidate was not
yet authorized and only the Migration 0008 + Backfill pre-flight resume was
executable. That historical state was subsequently superseded by the approved
Implementation Authorization Review, implementation, final review, and PR #44
integration.

### MIGRATION 0008 CODE INTEGRATION FINALIZED

- PR #44 merged authorized head `dd4a1b1069b342febf0bdec4d271ffb1e833ecf1`
  through Rebase and Merge into canonical main
  `93c385670be8490662cb7f96e05016be7a60aed5`.
- Main CI `33028326214`: 3/3 SUCCESS. Local finalization: PASS; 465 tests and
  98.16% coverage. Repository Alembic head is 0008.
- Real `lifeos.db` intentionally remains revision 0007 without
  `book_completions`; no real-data migration or coordinated cutover has run.
- Migration 0008 code integration is finalized. At that integration checkpoint,
  Slice 4 implementation had not started and its Implementation Authorization
  Review was next. That historical state was superseded by the approved Slice 4
  implementation, final review, publication in draft PR #46, and discovery of the
  Python 3.11 platform prerequisite.

### Deferred slices

3. Completion Persistence — INTEGRATED / FINALIZED.
4. Transactional Write + Concurrency — IMPLEMENTED / DRAFT PR #46 / MERGE BLOCKED PENDING PYTHON 3.11 PLATFORM TRANSITION / RUNTIME ACTIVATION BLOCKED PENDING COORDINATED CUTOVER.
5. Dedicated Read Model / API.
6. Migration 0008 + Backfill — CODE INTEGRATED / REAL-DATA APPLICATION NOT EXECUTED / COORDINATED CUTOVER NOT EXECUTED.
7. Best-Effort Event Seam.
8. Full Regression + Governance.

## Pendências

- READ-005: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION FINALIZED / SLICE 2 FINALIZED / SLICE 3 FINALIZED / SLICE 4 IMPLEMENTED AND PUBLISHED IN DRAFT PR #46 / SLICE 6 CODE INTEGRATED.
- RF-READ-005: Slice 4 merge is blocked pending the Python 3.11 platform transition; runtime activation remains blocked pending coordinated cutover.
- US-READ-005-001: only the Python 3.11 Platform Transition Implementation is executable.
- Python platform: current integrated platform and required checks remain 3.10; future >=3.11 transition is human-approved and AUTHORIZED / NOT STARTED.
- Migration 0008: CODE INTEGRATED; real local database NOT APPLIED.
- Alembic: repository 0008 (head); real `lifeos.db` 0007.
- READ-008: DEFERRED.
- RF-READ-009: ASSOCIAÇÃO PENDENTE / DEFERRED.
- RF-READ-010: RECONCILIAÇÃO PENDENTE / DEFERRED.
- `/api/v1`: PENDING NON-BLOCKING.
- Pesquisa: OUTSIDE READ-005 / NO FEATURE AUTHORIZED.

## Architecture Boundary

This amendment preserves ADR-0042 and BookCompletion semantics while clarifying
the pinned TSID representation and source-history safety conditions. At this
amendment's historical stage, authorization was limited to the read-only
Migration 0008 + Backfill implementation pre-flight resume. That state was
superseded by Migration 0008 code integration and the completed, reviewed Slice 4
implementation now published in draft PR #46. The current executable authority is
the Python 3.11 Platform Transition Implementation. Slice 4
merge remains blocked pending that platform transition; runtime activation remains
blocked pending coordinated cutover; Slices 5, 7, and 8 remain gated.

Architecture Decision ADR-0042 está aceita e congelada. The amended Technical
Plan is approved and frozen at docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md.

## Próximo Gate

PYTHON 3.11 PLATFORM TRANSITION IMPLEMENTATION

ONLY THE PYTHON 3.11 PLATFORM TRANSITION IMPLEMENTATION IS AUTHORIZED.

DO NOT MODIFY PR #46, APPLY MIGRATION 0008 TO REAL DATA, EXECUTE THE COORDINATED CUTOVER, OR EXPAND THE PYTHON 3.11 PLATFORM IMPLEMENTATION BEYOND THE FROZEN SIX-FILE ALLOWLIST.

SPRINT 09 AUTHORIZATION IS PROGRAM-LEVEL AUTHORIZATION, NOT BLANKET PERMISSION.
