# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | READ-005-S09-PRE-SLICE-02-REMEDIATION-01 |
| Iniciativa | READ-005 — Livros Concluídos |
| Status | IMPLEMENTATION AUTHORIZED — PREREQUISITE REMEDIATION READY |
| Tipo | Prerequisite Remediation |
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
| Current Executable Unit | PRE-SLICE-2 REMEDIATION — AUTH/CHARACTER SQLITE FK WRITE ORDER |
| Slice 1 Status | INTEGRATED |
| Slice 2 Status | AUTHORIZED / BLOCKED BY PREREQUISITE / IMPLEMENTATION NOT STARTED |
| Slices 3..8 | NOT EXECUTABLE / GATED |

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
- Slice 2 Implementation Pre-Flight: BLOCKED by the pre-existing AUTH/CHARACTER SQLite FK write-order defect.
- PRE-SLICE-2 Remediation Pre-Flight: PASS; Human Technical Review: APPROVED.
- ONLY THE PRE-SLICE-2 AUTH/CHARACTER FK REMEDIATION IS AUTHORIZED FOR EXECUTION.
- Slice 2 remains authorized at program/slice level and blocked until the prerequisite is integrated and validated.
- Slices 3..8 remain NOT EXECUTABLE / GATED.
- Sprint 09 authorization is not blanket permission to implement all slices in one branch or PR.

### PRE-SLICE-2 REMEDIATION — AUTH/CHARACTER SQLITE FK WRITE ORDER

Goal: correct existing AUTH/CHARACTER persistence ordering so registration is valid
under immediate SQLite foreign-key enforcement.

Frozen remediation flow:

User save
→ UoW flush
→ Player save
→ UoW flush
→ Character save
→ one final commit

Authorized future remediation scope:

- expose explicit `flush()` through shared `IUnitOfWork`;
- implement `flush()` as SQLAlchemy `Session.flush()` only;
- flush User before initial Player/Character provisioning;
- flush Player before Character persistence;
- ensure CharacterFactory receives the same request-scoped UoW;
- add focused tests for FK-enabled registration, rollback semantics, one final commit,
  post-commit event publication, duplicate-user behavior, and the full suite under FK enforcement.

Authorized future implementation allowlist:

- `app/shared/application/unit_of_work.py`;
- `app/shared/infrastructure/unit_of_work.py`;
- `app/auth/application/commands/register_user.py`;
- `app/character/application/factories/character_factory.py`;
- `app/composition_root.py`;
- `tests/auth/integration/test_registration_flow.py`.

No other implementation file is authorized automatically. Repository-local flush,
repository/mapper/model changes, ORM relationships, schema changes, migrations, FK disabling,
deferred constraints, global autoflush changes, SQLite PRAGMA logic in AUTH/CHARACTER,
EventBus redesign, and READ production changes are not authorized.

### SLICE 2 - SQLITE INTEGRITY FOUNDATION

Goal: establish the frozen SQLite foreign-key integrity foundation at shared
Engine/connection infrastructure level.

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

Slice 2 is not executable during this prerequisite remediation. It must return to
IMPLEMENTATION PRE-FLIGHT after remediation integration; do not implement Engine listeners,
SQLite connection listeners, `PRAGMA foreign_keys` enforcement, or shared infrastructure tests
in this remediation.

### Deferred slices

3. Completion Persistence.
4. Transactional Write + Concurrency.
5. Dedicated Read Model / API.
6. Migration 0008 + Backfill.
7. Best-Effort Event Seam.
8. Full Regression + Governance.

## Pendências

- READ-005: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION AUTHORIZED / SLICE 2 BLOCKED BY PREREQUISITE.
- RF-READ-005: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION AUTHORIZED / SLICE 2 IMPLEMENTATION NOT STARTED.
- US-READ-005-001: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION AUTHORIZED / SLICE 2 IMPLEMENTATION NOT STARTED.
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
A autorização humana atual é limitada ao pré-requisito de remediação AUTH/CHARACTER;
Slice 2 permanece bloqueada por esse pré-requisito e as Slices 3..8 permanecem gated.

## Próximo Gate

PRE-SLICE-2 REMEDIATION IMPLEMENTATION — AUTH/CHARACTER SQLITE FK WRITE ORDER

ONLY THE PRE-SLICE-2 REMEDIATION IS AUTHORIZED FOR EXECUTION.

DO NOT START SLICE 3.

SPRINT 09 AUTHORIZATION IS PROGRAM-LEVEL AUTHORIZATION, NOT BLANKET PERMISSION.
