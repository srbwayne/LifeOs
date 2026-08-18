# ADR-0042

## Título

READ-005 — Book Completion Milestone

## Status

Accepted

## Data

2026-08-17

---

# Contexto

READ-005 — Livros Concluídos possui Product Specification APPROVED / FROZEN.
`ReadingProgress.completed` continua sendo o estado atual derivado da cobertura
das ReadingSessions. READ-005, porém, precisa representar um fato histórico,
único, imutável, consultável e owner-scoped, com `completed_at`, atomicamente
relacionado à sessão disparadora e disponível como fonte para futuras integrações.

# Problema

Persistir completion no Book confundiria item de biblioteca, cobertura atual e
milestone histórico. Uma solução somente baseada em eventos não oferece fonte
durável de consulta no estado atual do LifeOS. A arquitetura precisa preservar
atomicidade, unicidade, idempotência, isolamento por Player e reconstrução de
Books já completos antes de READ-005.

# Alternativas Consideradas

## Option A — Fields on Book

Adicionar semanticamente `completed` e `completed_at` ao Aggregate Book. É
simples para consulta, mas acopla o histórico ao catálogo e altera a fronteira
de Book.

## Option B — Dedicated Completion Record

Persistir um registro dedicado owner-scoped por Player + Book. Mantém
`ReadingProgress` derivado, representa o milestone histórico diretamente e
permite unicidade e consultas próprias.

## Option C — Event-only / Event-derived

Representar completion somente por ocorrência/evento. O EventBus atual é
in-memory, não durável e não é fonte suficiente para identificação ou histórico.

## Option D — Dedicated Completion Record + post-commit occurrence

Persistir o milestone como fonte durável e disponibilizar uma ocorrência após o
commit. Esta opção preserva a integridade transacional sem exigir Outbox ou
mensageria distribuída em READ-005 V1.

# Decisão

- READ-005 utilizará o conceito persistido dedicado **BookCompletion**.
- BookCompletion representa o fato histórico, único e imutável de que um Player
  concluiu um Book.
- BookCompletion será separado de Book e de ReadingProgress.
- Book não receberá semanticamente `completed` ou `completed_at` como estratégia
  de READ-005.
- ReadingProgress.completed permanecerá derivado e não persistido.
- A ReadingSession disparadora e BookCompletion participarão do mesmo Unit of
  Work e do mesmo commit.
- Após considerar a nova ReadingSession, a cobertura será recalculada pelos
  serviços puros existentes. A ausência de BookCompletion permite criar o
  primeiro milestone; sua presença impede duplicação.
- Haverá serialização lógica de escrita por Book durante criação da sessão,
  avaliação de cobertura e materialização de completion.
- A unicidade Player + Book deverá ser protegida também no banco.
- `completed_at` será persistido semanticamente como o `ended_at` da sessão que
  provoca a primeira completion, em UTC/timezone-aware.
- READ-005 terá read model/query dedicada para identidade do Book concluído e
  `completed_at`, sem alterar inicialmente GET /books, READ-006 ou READ-007.
- A persistência dedicada exigirá migration conceitualmente posterior à 0007,
  esperada como 0008, incluindo integridade, unicidade, índices e backfill.
- Books já com 100% de cobertura deverão ser reconhecidos. O backfill ordenará
  ReadingSessions por `ended_at` crescente e usará o primeiro timestamp em que
  a união cumulativa atingir 100%. Empates mantêm o mesmo timestamp; eventual
  desempate por ID é detalhe do Technical Plan.
- Se BookCompletion já existir, sessão retroativa não altera completion nem
  `completed_at`. Se não existir, sessão retroativa que atingir 100% poderá
  criar o milestone com seu próprio `ended_at`.
- Alterações posteriores de `total_pages` não causam reversão automática.
- BookCompletion persistido será a fonte durável de verdade. O InMemoryEventBus
  poderá ser um integration seam inicial, mas não garante entrega durável.
- Outbox, broker e consumidor GAME não são necessários em READ-005 V1.
- RF-READ-009 permanece ASSOCIATION PENDING / DEFERRED.
- READ-003, READ-004, READ-006 e READ-007 permanecem inalterados.

# Consequências

## Positivas

- separação clara entre cobertura atual e fato histórico;
- histórico estável e consultável;
- unicidade e idempotência explícitas;
- isolamento por Player;
- baixo acoplamento com Book;
- compatibilidade com DDD, Clean Architecture e CQRS simples;
- preservação do contrato de READ-006;
- evolução futura de integração sem tornar o evento a fonte de verdade.

## Negativas e trade-offs

- nova persistência e migration;
- repository/read model adicionais;
- write flow mais complexo;
- serialização lógica por Book;
- custo de recalcular cobertura;
- backfill obrigatório;
- necessidade de testes de concorrência e integração;
- EventBus atual não oferece durabilidade externa.

# Impactos

Capabilities afetadas: READ.
Features afetadas: READ-005 — Livros Concluídos.
RFs afetados: RF-READ-005 — Conclusão de Livro.
Migration necessária: Sim, conceitualmente 0008; não criada neste ADR.
Breaking Change: Não no contrato existente de READ-003/004/006/007.
GAME: nenhuma implementação; RF-READ-009 permanece deferred.

# Referências

- `NEXT_TASK.md`
- `docs/01_PRODUCT/PRD.md`
- `docs/01_PRODUCT/USE_CASES/READ/EPIC-READ.md`
- `docs/02_ARCHITECTURE/09_DECISION_LOG.md`
- `app/read/domain/services/reading_coverage_calculator.py`
- `app/read/domain/services/reading_progress_calculator.py`
- `app/shared/infrastructure/unit_of_work.py`

## Technical Plan Deferred

Este ADR não congela nome de tabela ou coluna, SQL type, ORM mapping,
repository signatures, locking primitive, retry algorithm, DDL, nomes de
índices, ação de FK, API/path/método HTTP, DTO, paginação, ordenação, classe ou
payload de evento, Outbox ou broker. Esses itens pertencem ao Technical Plan.
