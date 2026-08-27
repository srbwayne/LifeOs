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
Implementation at Technical Plan approval: NOT AUTHORIZED
Sprint 09 at Technical Plan approval: NOT AUTHORIZED

Current execution state is governed by `NEXT_TASK.md` and subsequent approved
governance. Migration 0008 code is integrated; Slice 4 implementation remains
subject to its separate Implementation Authorization Review; runtime activation
remains coupled to the coordinated cutover.

## 1. Domain

Book permanece sem completion state. ReadingProgress permanece derivado e não persistido. BookCompletion é um Aggregate Root dedicado e imutável.

Estado de BookCompletion:

- id: BookCompletionId;
- book_id: BookId;
- completed_at: datetime.

Não possui owner_id nem updated_at. BookCompletionId segue a representação de string
TSID canônica produzida e validada pela dependência `tsidpy` fixada. Em
`tsidpy==1.1.5`, essa representação canônica possui 13 caracteres; a
canonicalidade é comportamental (`TSID.from_string(value).to_string() == value`).
`VARCHAR(26)` é capacidade de persistência/compatibilidade e não define o
comprimento semântico do TSID. completed_at é o ended_at da ReadingSession
disparadora, normalizado como UTC-aware. Equality é por BookCompletionId. Não
existe update, reopen ou automatic revoke.

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

Os campos `id` e `book_id` permanecem `VARCHAR(26)` como capacidade de
armazenamento; isso não impõe representação TSID semântica de 26 caracteres.

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

Runtime activation of Slice 4 requires a verified Migration 0008 schema and
completed historical backfill. Migration/backfill and Slice 4 activation must use
a coordinated cutover: no ReadingSession writes may occur from the start of the
backfill snapshot until only the Slice 4-capable runtime is active. A migrated
schema with the old writable ReadingSession path, and a schema-only Slice 4
activation followed by later backfill, are forbidden deployment states.

The SQLite V1 retry policy is frozen as two total write-intent acquisition
attempts: the initial attempt and at most one retry after a fixed 50 ms delay,
without jitter. Retry is allowed only before relevant reads, writes, aggregate
tracking, flush, or commit, when `OperationalError` wraps
`sqlite3.OperationalError` with `sqlite_errorcode == SQLITE_BUSY`. It never
applies after successful acquisition, to `SQLITE_LOCKED`, IntegrityError, domain
or owner failures, flush, commit, ambiguous commit, publication, or unknown
errors.

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

Migration 0008 remains one cohesive Completion migration: table, integrity,
uniqueness, indexes, and complete historical backfill. It must not be split into
a schema-only revision plus a later backfill.

Execution status: Migration 0008 code is implemented and integrated at repository
head 0008. At Technical Plan approval time it was not yet created; real-data
application remains pending the coordinated cutover, and real local `lifeos.db`
intentionally remains revision 0007.

Para cada Book, ReadingSessions owner-consistent são ordenadas por ended_at ASC, id ASC; intervalos são unidos cumulativamente; o primeiro timestamp que alcança 100% cria exatamente uma Completion. Books incompletos ou sem sessões não recebem row. Empates preservam o mesmo timestamp.

IDs de backfill usam diretamente a dependência `tsidpy` já fixada, sem importar
`app.shared.domain.tsid.new_tsid`, BookCompletionId ou outro código de aplicação
mutável. A canonicalidade segue a representação fornecida pela dependência fixada;
em `tsidpy==1.1.5`, ela possui 13 caracteres e cabe em `VARCHAR(26)`.

Antes do primeiro DDL de 0008, a migration deve validar toda a fonte
owner-consistent e calcular o conjunto completo de candidatos. Cada intervalo
considerado deve obedecer a `start_page >= 1`, `end_page >= start_page`,
`start_page <= books.total_pages` e `end_page <= books.total_pages`; `ended_at`
deve ser legível e deterministamente ordenável. História owner-consistent que não
for representável contra o total_pages atual aborta a migration antes de qualquer
DDL. Não é permitido clamp, truncamento, exclusão, reescrita, reparo automático
ou inferência de total_pages histórico. Sessões com owner divergente continuam
excluídas da fonte de backfill e, isoladamente, não bloqueiam a migration.

Após validar e calcular candidatos, a migration gera e valida todos os TSIDs e
define explicitamente `created_at` técnico; somente então pode criar a tabela,
índice e inserir as linhas preparadas. Violações de `foreign_key_check` continuam
blockers independentes. Como SQLite/Alembic não oferece garantia suficiente de
DDL transacional neste ambiente, backup, exclusão de tráfego, failed-start,
verificação pós-migration e cutover coordenado permanecem obrigatórios.

Downgrade remove apenas a persistência de Completion e não modifica Books ou
ReadingSessions. Re-upgrade precisa preservar book_ids completos, completed_at,
contagem e semântica de unicidade/ownership; IDs de Completion podem ser
regenerados após o downgrade destrutivo.

Sessão retroativa com Completion existente nunca altera completed_at; sem Completion, pode criar o milestone usando seu próprio ended_at. Alteração posterior de total_pages não revoga o milestone.

Before a real-data Migration 0008, create and verify a backup, exclude
ReadingSession writes, stop old writable application instances, and validate
`foreign_key_check`. After migration/backfill, validate Alembic revision, schema,
constraints, indexes, FK integrity, uniqueness, and historical backfill results.
The application must not start if these validations fail. Old writable instances
remain stopped until the Slice 4-capable runtime is healthy; downgrade requires a
compatible application rollback and traffic exclusion.

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

Slice numbering is a semantic implementation and review decomposition, not an
unconditional independent deployment order. Slice 6 Migration 0008 + Backfill is
a deployment prerequisite for Slice 4 runtime activation. Slice 6 and Slice 4
may use separate branches, PRs, and reviews, but their final writable-runtime
activation is coupled.

## 12. Boundaries and Authorization

Este documento formaliza o plano técnico aprovado; não cria código, migration, schema aplicado ou comportamento runtime. A aprovação não autoriza implementação nem Sprint 09.

Independent Slice 4 activation on schema 0007 is forbidden. Independent writable
deployment of Migration 0008/backfill while the old ReadingSession path accepts
writes is forbidden. Schema-only activation followed by later historical backfill
is forbidden. The coupled cutover requires an explicit readiness review; this
amendment did not authorize Migration 0008 implementation or Slice 4
implementation. Migration 0008 code is now integrated; Slice 4 implementation
still requires its separate Implementation Authorization Review, and runtime
activation still requires the coordinated cutover.

Technical Plan: APPROVED / FROZEN.

At Technical Plan approval:

- Implementation: NOT AUTHORIZED.
- Sprint 09: NOT AUTHORIZED.

Current execution authorization is governed by `NEXT_TASK.md` and subsequent
approved governance. Migration 0008 code is INTEGRATED. Slice 4 implementation
is NOT YET AUTHORIZED; Slice 4 runtime activation is BLOCKED PENDING COORDINATED
CUTOVER.
