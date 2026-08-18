# READ-005 — Technical Plan — Livros Concluídos

Feature: READ-005 — Livros Concluídos
RF: RF-READ-005 — Conclusão de Livro
US: US-READ-005-001
Product Decision: PD-READ-005 — APPROVED
Product Specification: APPROVED / FROZEN
Architecture: ADR-0042 — ACCEPTED / FROZEN
Technical Plan: APPROVED / FROZEN
Human Review: APPROVED
Date: 2026-08-17
Implementation: NOT AUTHORIZED
Sprint 09: NOT AUTHORIZED

## 1. Domain

Book permanece sem completion state. ReadingProgress permanece derivado e não persistido. BookCompletion é um Aggregate Root dedicado e imutável.

Estado de BookCompletion:

- id: BookCompletionId;
- book_id: BookId;
- completed_at: datetime.

Não possui owner_id nem updated_at. BookCompletionId segue a convenção TSID canônica de 26 caracteres. completed_at é o ended_at da ReadingSession disparadora, normalizado como UTC-aware. Equality é por BookCompletionId. Não existe update, reopen ou automatic revoke.

## 2. Ownership

Option B está aprovada. Ownership é derivado por:

```text
BookCompletion.book_id → Book.id → Book.owner_id
```

Book possui identidade global e exatamente um owner. Completion não persiste owner redundante.

O write repository possui semântica owner-safe equivalente a save(completion) e get_by_book_and_owner(book_id, owner_id). A leitura oferece count_by_owner(owner_id) e list_page_by_owner(owner_id, offset, limit). Todas as consultas fazem JOIN com Book e filtram o owner autenticado. Não há owner fornecido pelo cliente.

## 3. Persistence

Tabela: book_completions.

| Column | Type | Null | Constraint |
|---|---|---:|---|
| id | VARCHAR(26) | no | primary key |
| book_id | VARCHAR(26) | no | foreign key to books.id |
| completed_at | DateTime(timezone=True) | no | functional timestamp |
| created_at | DateTime | no | technical timestamp |

UNIQUE(book_id) garante um milestone por Player + Book, pois cada Book possui owner único. A FK usa RESTRICT / NO ACTION; CASCADE não é permitido. Índices: unique book_id e (completed_at, book_id). Não há user_id, owner_id ou updated_at.

## 4. SQLite Integrity

Toda conexão SQLite usada pelo runtime, testes ou Alembic deve executar PRAGMA foreign_keys = ON por listener de conexão no shared infrastructure/database.py ou mecanismo equivalente aplicado ao Engine-level. Bancos não-SQLite permanecem inalterados; repositories não executam PRAGMA.

PRAGMA foreign_keys deve retornar 1. PRAGMA foreign_key_check é obrigatório antes e depois da migration, em upgrade de banco existente e em validação downgrade/re-upgrade. Qualquer violation é BLOCKER de implementação ou migration; não há reparo ou deleção automática.

## 5. Transaction and Concurrency

Fluxo congelado:

```text
enter UoW
→ BEGIN IMMEDIATE
→ Book owner-scoped
→ existing Completion owner-safe
→ existing ReadingSessions owner-scoped
→ create new ReadingSession
→ calculate(existing_sessions + new_session)
→ save ReadingSession
→ optionally save BookCompletion
→ track occurrence
→ flush
→ commit once
→ post-commit best-effort publication
```

autoflush=False permanece. O calculator recebe explicitamente a sessão nova; flush não é necessário para calcular cobertura e ocorre somente após preparar a persistência.

ReadingSession e Completion são atômicos no mesmo UoW, transação e commit. SQLite V1 usa BEGIN IMMEDIATE, serializando a escrita antes das leituras relevantes. Esse custo é aceito para o deployment atual.

Retries são limitados a falhas transitórias de aquisição de lock antes do commit, com rollback completo e repetição da operação inteira. Resultado de commit ambíguo não recebe retry automático, pois o comando atual não possui idempotency key.

## 6. Completion Detection

Reutilizar ReadingCoverageCalculator e ReadingProgressCalculator.calculate_from_coverage:

- coverage incompleta: nenhum Completion;
- coverage completa com Completion existente: no-op;
- coverage completa sem Completion: criar exatamente uma Completion.

União de intervalos, deduplicação de overlap/releitura, lacunas e a fronteira de READ-003 permanecem inalteradas. Command Handler não chama Query Handler.

## 7. Event Semantics

BookCompletion persistido é a fonte durável de verdade e a consulta dedicada é a superfície funcional durável. BookCompleted é somente ocorrência best-effort in-process, com payload mínimo completion_id, book_id e completed_at.

O comportamento atual de READ, com InMemoryEventBus por UoW, é preservado. Não há promessa de entrega durável, cross-process ou subscriber guarantee. Outbox, broker, RabbitMQ, Kafka, GAME e Noema não fazem parte deste plano.

## 8. Read Model and API

Endpoint dedicado: GET /book-completions, autenticado e owner-scoped.

Paginação: page=1, size=20, máximo 100. Ordenação: completed_at DESC, book_id DESC. Item mínimo: book_id, book_title, completed_at. Resposta paginada: items, page, size, total_items, total_pages.

São esperados dois SELECTs: count e page query com JOIN Book/Completion. N+1 é proibido. GET /books, /reading-sessions, /reading-statistics, READ-003, READ-004, READ-006 e READ-007 permanecem inalterados. /api/v1 continua PENDING NON-BLOCKING.

## 9. Migration 0008 and Backfill

Migration conceitual 0008 cria tabela, integridade, unicidade, índices e backfill. Ela não é criada neste gate.

Para cada Book, ReadingSessions owner-consistent são ordenadas por ended_at ASC, id ASC; intervalos são unidos cumulativamente; o primeiro timestamp que alcança 100% cria exatamente uma Completion. Books incompletos ou sem sessões não recebem row. Empates preservam o mesmo timestamp.

IDs de backfill usam a dependência TSID já fixada, sem importar código de aplicação mutável. Downgrade remove apenas a persistência de Completion e não modifica Books ou ReadingSessions.

Sessão retroativa com Completion existente nunca altera completed_at; sem Completion, pode criar o milestone usando seu próprio ended_at. Alteração posterior de total_pages não revoga o milestone.

## 10. Test Plan

Cobertura obrigatória:

- domínio: criação, TSID, timestamp, invariantes, imutabilidade e igualdade;
- aplicação: cobertura incompleta/completa, gaps, overlaps, rereads, retroatividade e isolamento;
- atomicidade: falha de sessão ou Completion sem estado parcial;
- concorrência: gaps finais simultâneos, lock e retry;
- SQLite: foreign_keys == 1, FK inválida rejeitada e foreign_key_check vazio;
- persistência: mapper, unique, FK, RESTRICT e timezone;
- migration: fresh/existing DB, backfill, ties, downgrade e re-upgrade;
- API: auth, owner scope, paginação, ordenação, empty result e ausência de N+1;
- regressão integral de AUTH, CHARACTER, READ e testes arquiteturais.

## 11. Implementation Slices

1. Domain foundation.
2. SQLite integrity foundation.
3. Completion persistence.
4. Transactional write and concurrency.
5. Dedicated read model and API.
6. Migration 0008 and backfill.
7. Best-effort event seam.
8. Full regression and governance.

Cada slice deve preservar atomicidade, owner isolation, unicidade, derivação de ReadingProgress, fronteiras READ-003/004/006/007 e ausência de efeitos GAME.

## 12. Boundaries and Authorization

Este documento formaliza o plano técnico aprovado; não cria código, migration, schema aplicado ou comportamento runtime. A aprovação não autoriza implementação nem Sprint 09.

Technical Plan: APPROVED / FROZEN.
Implementation: NOT AUTHORIZED.
Sprint 09: NOT AUTHORIZED.