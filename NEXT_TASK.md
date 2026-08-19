# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | READ-005-S09-SLICE-01 |
| Iniciativa | READ-005 — Livros Concluídos |
| Status | IMPLEMENTATION AUTHORIZED - SLICE 1 READY |
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
| Current Executable Slice | SLICE 1 - DOMAIN FOUNDATION |
| Slice 1 Status | AUTHORIZED / NOT STARTED |
| Slices 2..8 | NOT YET EXECUTABLE / INDIVIDUALLY GATED |

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
- ONLY SLICE 1 IS AUTHORIZED FOR EXECUTION.
- Slices 2..8 remain NOT YET EXECUTABLE / INDIVIDUALLY GATED.
- Do not start Slice 2 until Slice 1 has completed its implementation, review and integration gates.
- Sprint 09 authorization is not blanket permission to implement all slices in one branch or PR.

### SLICE 1 - DOMAIN FOUNDATION

Goal: introduce the pure READ domain foundation for BookCompletion.

Permitted scope when Slice 1 executes:

- BookCompletionId using the TSID project convention;
- dedicated immutable BookCompletion Aggregate Root/domain milestone;
- state limited to id, book_id and completed_at;
- domain invariants, creation factory, restore path if required by project patterns;
- equality by BookCompletionId;
- domain-only tests.

Slice 1 must not include owner_id, created_at as functional domain state, updated_at,
manual completion, reopen, revocation, persistence, repository, ORM, migration, API,
SQLite listener, BEGIN IMMEDIATE integration or event integration.

### Deferred slices

2. SQLite Integrity Foundation.
3. Completion Persistence.
4. Transactional Write + Concurrency.
5. Dedicated Read Model / API.
6. Migration 0008 + Backfill.
7. Best-Effort Event Seam.
8. Full Regression + Governance.

## Pendências

- READ-005: IMPLEMENTATION AUTHORIZED / NOT STARTED.
- RF-READ-005: IMPLEMENTATION AUTHORIZED / NOT STARTED.
- US-READ-005-001: IMPLEMENTATION AUTHORIZED / NOT STARTED.
- READ-008: DEFERRED.
- RF-READ-009: ASSOCIAÇÃO PENDENTE / DEFERRED.
- RF-READ-010: RECONCILIAÇÃO PENDENTE / DEFERRED.
- `/api/v1`: PENDING NON-BLOCKING.
- Pesquisa: OUTSIDE READ-005 / NO FEATURE AUTHORIZED.

## Architecture Boundary

Architecture Decision ADR-0042 está aceita e congelada. O Technical Plan está
aprovado e congelado em docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md.
A autorização humana é limitada à Slice 1; as demais slices permanecem individualmente gated.

## Próximo Gate

SLICE 1 IMPLEMENTATION PRE-FLIGHT - READ-005 DOMAIN FOUNDATION

ONLY SLICE 1 IS AUTHORIZED FOR EXECUTION.

DO NOT START SLICE 2 UNTIL SLICE 1 HAS COMPLETED ITS OWN IMPLEMENTATION / REVIEW / INTEGRATION GATES.

SPRINT 09 AUTHORIZATION IS PROGRAM-LEVEL AUTHORIZATION, NOT BLANKET PERMISSION.
