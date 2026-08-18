## Architecture Decision READ-005 — 2026-08-17

**Human Decision:** APPROVED
**ADR:** ADR-0042 — Accepted
**Feature:** READ-005 — Livros Concluídos
**Architecture:** APPROVED / FROZEN

### Decisões congeladas

- BookCompletion dedicado, separado de Book e ReadingProgress.
- ReadingSession + BookCompletion atômicos no mesmo UoW e commit.
- Single logical writer por Book e unicidade Player + Book.
- `completed_at` persistido semanticamente a partir do `ended_at` disparador.
- Read model dedicado; READ-006 e READ-007 permanecem inalterados.
- Migration conceitualmente 0008 e backfill obrigatório.
- Backfill por `ended_at` crescente; sessões retroativas seguem as regras aprovadas.
- BookCompletion persistido é a fonte durável de verdade.
- Transporte externo durável deferred; GAME fora do escopo.

**Product Clarification:** pre-existing completions + deterministic backfill approved.
**Technical Plan:** PENDING
**Implementation:** NOT AUTHORIZED
**Sprint 09:** NOT AUTHORIZED
**Next Gate:** TECHNICAL PLAN — READ-005 LIVROS CONCLUÍDOS

## Product Specification READ-005 — 2026-08-16

**Status:** APPROVED / FROZEN
**Capability:** READ
**Feature:** READ-005 — Livros Concluídos
**RF:** RF-READ-005 — Conclusão de Livro
**US:** US-READ-005-001
**Product Decision:** PD-READ-005 — APPROVED

### Contrato aprovado

- Completion Model: AUTOMATIC COMPLETION MILESTONE.
- A primeira cobertura integral de páginas únicas produz a conclusão automaticamente.
- Overlaps e releituras não duplicam cobertura; lacunas impedem conclusão.
- Não existe conclusão manual ou antecipada.
- O milestone é único por Player + Book e historicamente estável.
- `completed_at` é informação funcional e corresponde ao `ended_at` da sessão que provoca a primeira transição.
- Releituras posteriores não alteram conclusão nem `completed_at`.
- O Book permanece disponível e Books concluídos devem ser identificáveis pelo Player.
- A conclusão deve ser historicamente representável e sua ocorrência disponibilizável externamente.
- Efeitos GAME estão fora do escopo; RF-READ-009 permanece deferred.

**Product Identity:** FROZEN
**Product Specification:** FROZEN
**Architecture Review:** APPROVED / FROZEN
**Technical Plan:** NOT AUTHORIZED
**Implementation:** NOT AUTHORIZED
**Sprint 09:** NOT AUTHORIZED
**Next Gate:** ARCHITECTURE REVIEW — READ-005 LIVROS CONCLUÍDOS
## Product Decision PD-READ-005 — 2026-08-16

**Status:** APPROVED
**Capability:** READ
**Feature:** READ-005 — Livros Concluídos
**RF:** RF-READ-005 — Conclusão de Livro

### Decisão

- READ-005 é canonicamente Livros Concluídos.
- A entrada “Pesquisa” no Feature Catalog era divergência documental e foi
  substituída.
- Pesquisa não possui Feature ID, RF ou User Story autorizado por esta decisão.
- Completion semantics permanecem pendentes de Product Specification.
- READ-008, RF-READ-009 e RF-READ-010 permanecem deferred.

### Estado

- Sprint 09: NOT AUTHORIZED.
- Next Gate: PRODUCT SPECIFICATION — READ-005 LIVROS CONCLUÍDOS.

## Sprint 08 — Reading Statistics - 2026-08-16

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-007 — Estatísticas de Leitura
**User Story:** US-READ-007-001
**Requisito Funcional:** RF-READ-007

### Entregas

- READ-007 integrada na `main` por `GET /reading-statistics`.
- Consulta global por Player autenticado, all-time e owner-scoped.
- Estatísticas derivadas on demand de Book + ReadingSession.
- Exatamente cinco estatísticas entregues.
- `total_pages_read` preserva gross activity: releituras e sobreposições contam novamente.
- `average_pages_per_session` usa Decimal, ROUND_HALF_UP e string HTTP com duas casas.
- Owner isolation preservado.
- SQL executa dois SELECTs fixos, sem N+1.
- Nenhum estado estatístico persistido.
- Nenhuma migration criada.

### Integração e validação

- PR #23 integrado por Rebase and Merge em `2026-08-16T18:58:18Z`.
- Main funcional: `9aa77f461fbbaded2f26d5c46a201674adcf686d`.
- Commits funcionais na main:
  - `7dce4eb6d849168a93d657d8151d11f66f5b8d37` — `feat(read): implement reading statistics read model`;
  - `9aa77f461fbbaded2f26d5c46a201674adcf686d` — `feat(read): expose reading statistics API`.
- CI da main: run `31966168701` — SUCCESS.
- Validação: 407 testes aprovados, cobertura 97,95% e Alembic `0007 (head)`.
- Branch `feature/read-007-reading-statistics` removida local e remotamente.

### Estado

- Sprint 08: CONCLUÍDA.
- READ-007: ENTREGUE.
- RF-READ-007: ENTREGUE.
- US-READ-007-001: ENTREGUE.
- Implementação: INTEGRADA.
- Product Specification: FROZEN.
- Architecture: APPROVED.
- Technical Plan: APPROVED / FROZEN.
- CI: APROVADO.
- Migration: NONE.
- Próxima Sprint: NENHUMA AUTORIZADA.
## Sprint 08 — Reading Statistics - 2026-08-15

**Status:** AUTORIZADA — PRODUCT SPEC APPROVED / FROZEN
**Capability:** READ
**Feature:** READ-007 — Estatísticas de Leitura
**RF:** RF-READ-007
**US:** US-READ-007-001

### Decisão e contrato

- Product Owner aprovou READ-007 e o contrato V1.
- Product Contract: FROZEN.
- Estatísticas globais, all-time, owner-scoped e derivadas on demand.
- Fontes exclusivas: Book e ReadingSession.
- `GET /reading-statistics`, sem parâmetros, com cinco campos exatos.
- `total_pages_read` é volume bruto; releituras e sobreposições contam novamente.
- `average_pages_per_session` usa duas casas decimais e ROUND_HALF_UP.
- Empty state retorna 200; requisição sem autenticação retorna 401.

### Estado

- Implementação: NOT STARTED.
- Architecture Review: PENDING.
- Technical Plan: PENDING.
- Implementation Authorization: NO.
- Sprint 07 permanece concluída.
- Outros itens READ permanecem deferidos para reconciliação posterior.

# Project Status

## Sprint 08 — Reading Statistics — Implementation Authorization - 2026-08-16

**Product Specification:** INTEGRATED / FROZEN
**Architecture Review:** APPROVED
**Technical Plan:** APPROVED / FROZEN
**Migration:** NOT REQUIRED
**Alembic target:** 0007
**Implementation Readiness:** READY
**Implementation Authorization:** YES — HUMAN DECISION
**Implementation:** NOT STARTED
**Next:** FUNCTIONAL IMPLEMENTATION

READ-007 remains a derived, owner-scoped CQRS read model with no domain
changes, no persisted statistics state, no UoW/events, and two fixed SQL
SELECTs. Implementation must follow the frozen Technical Plan and allowlist.


## Sprint 07 — Reading History - 2026-08-15

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-006 — Histórico
**User Story:** US-READ-006-001
**Requisito Funcional:** RF-READ-006

### Entregas

- READ-006 integrada na `main` por `GET /reading-sessions`.
- Histórico global, all-time, owner-scoped e read-only, com paginação `page`/`size`.
- Ordenação determinística por `started_at DESC, id DESC`.
- `book_title` atual obtido pelo read model dedicado, sem novo Aggregate e sem N+1.
- Semântica UTC preservada.
- Migration `0007` e índice `ix_reading_sessions_user_started_id` integrados.
- Índice `ix_reading_sessions_user_book` preservado.

### Integração e validação

- PR #19 integrado por Rebase and Merge em `2026-08-15T13:54:11Z`.
- Main funcional: `54b024cc24b491aaa28ad2b97b0230f82a101cc8`.
- CI da `main`: run `31888455360` — SUCCESS.
- Validação: 390 testes aprovados, cobertura de 97,87% e Alembic `0007 (head)`.
- Branch `feature/read-006-reading-history` removida local e remotamente.

### Estado

- Sprint 07: CONCLUÍDA.
- READ-006: ENTREGUE.
- RF-READ-006: ENTREGUE.
- US-READ-006-001: ENTREGUE.
- Implementação: INTEGRADA.
- Product Spec: FROZEN.
- Planejamento técnico: APROVADO.
- CI: APROVADO.
- Próxima Sprint: NENHUMA AUTORIZADA.

## Implementação local da Sprint 07: Reading History - 2026-08-15

**Status:** IMPLEMENTAÇÃO FUNCIONAL CONCLUÍDA LOCALMENTE — AGUARDANDO AUDITORIA, PUBLICAÇÃO E INTEGRAÇÃO
**Feature:** READ-006 — Histórico
**RF:** RF-READ-006
**US:** US-READ-006-001

- Product Spec: FROZEN.
- Planejamento técnico: APROVADO.
- GET /reading-sessions implementado localmente como query owner-scoped,
  all-time, paginada e read-only.
- Read-side port dedicado, projection join sem N+1, UTC preservado e migration
  0007 com índice (user_id, started_at, id).
- RF-READ-010 permanece OUT OF SCOPE.
- Nenhuma publicação, PR, integração na main ou CI da main ocorreu.
- Sprint 07, READ-006 e RF-READ-006 permanecem NÃO ENTREGUES.

## Sprint 07 — Reading History - 2026-08-14

**Status:** ESPECIFICAÇÃO FUNCIONAL APROVADA — AGUARDANDO PLANEJAMENTO TÉCNICO
**Capability:** READ
**Feature:** READ-006 — Histórico
**User Story:** US-READ-006-001
**Requisito Funcional:** RF-READ-006

### Autorização

- Product Owner selecionou READ-006 e exclusivamente RF-READ-006.
- Specification freeze concluído.
- Histórico global, all-time, owner-scoped e read-only, baseado em ReadingSessions.
- Nove campos aprovados, incluindo book_title e notes original.
- GET /reading-sessions, paginação page/size e ordenação started_at DESC, id DESC.
- Histórico vazio retorna 200 OK; não existem filtros funcionais.
- RF-READ-010 está fora da Sprint 07.
- Implementação não iniciada e planejamento técnico pendente.
- Sprint 06 permanece concluída; nenhuma alteração funcional ocorreu.

### Pendências preservadas

- READ-005: DIVERGÊNCIA PENDENTE.
- RF-READ-005: PENDENTE.
- READ-007 e READ-008: AUSENTES NO FEATURE CATALOG.
- RF-READ-009: ASSOCIAÇÃO PENDENTE.
- RF-READ-010: FORA DA SPRINT 07 — RECONCILIAÇÃO PENDENTE.
- /api/v1: PENDING NON-BLOCKING.

## Sprint 06 — Reading Insights - 2026-08-14

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-004 — Insights
**User Story:** US-READ-004-001
**Requisito Funcional:** RF-READ-011

### Entregas

- READ-004 integrada na `main`.
- Quatro Insights entregues: cobertura restante, lacunas de cobertura, última página alcançada com lacunas e cobertura integral confirmada.
- Consulta exclusivamente por Book e all-time.
- Coverage intervalar compartilhada por READ-003 e READ-004, com `ReadingProgress` preservado como fonte da semântica de progresso.
- Resultados determinísticos, derivados e read-only, sem persistência ou eventos.
- `GET /books/{book_id}/insights` integrado com ownership preservado pelo usuário autenticado.
- Infrastructure e Repository Ports permaneceram inalterados.
- Nenhuma migration foi criada; Alembic permanece em `0006 (head)`.
- PR #16 integrado por Rebase and Merge em `2026-08-14T03:19:44Z`.
- CI da `main` aprovado após o merge no run `31766473176`.
- Validação final: 368 testes aprovados e cobertura total de 97,76%.
- Documentação técnica sincronizada.

### Estado

- Sprint 05: CONCLUÍDA.
- Sprint 06: CONCLUÍDA.
- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- READ-004: ENTREGUE.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003: ENTREGUE.
- RF-READ-004: ENTREGUE.
- RF-READ-005..010: NÃO ENTREGUES.
- RF-READ-011: ENTREGUE.
- Implementação: INTEGRADA.
- Planejamento técnico: APROVADO.
- CI: APROVADO.
- Próxima Sprint: NENHUMA AUTORIZADA.

### Pendências fora da Sprint

- RF-READ-005 — Conclusão de Livro associado a READ-005: PENDENTE.
- READ-005 divergente entre Pesquisa e Livros Concluídos no EPIC-READ: DIVERGÊNCIA PENDENTE.
- READ-007: AUSENTE NO FEATURE CATALOG.
- READ-008: AUSENTE NO FEATURE CATALOG.
- RF-READ-009 associado a READ-003: ASSOCIAÇÃO PENDENTE.
- Divergência global de versionamento entre `/books` e `/api/v1`: PENDENTE — NÃO BLOQUEANTE.
## Sprint 05 — Reading Progress - 2026-08-10

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-003 — Reading Progress
**User Story:** US-READ-003-001
**Requisito Funcional:** RF-READ-004

### Entregas

- READ-003 integrada na `main`.
- `ReadingProgress` derivado das ReadingSessions por cobertura de páginas únicas.
- Sobreposições e releituras tratadas sem dupla contagem.
- `highest_page_reached` mantido como informação, sem representar posição atual.
- Percentual derivado e conclusão determinada somente por cobertura integral.
- Nenhum estado de progresso persistido.
- Consulta autenticada integrada por `GET /books/{book_id}/progress`.
- Ownership preservado pelo usuário autenticado.
- Migration `0006` e índice `ix_reading_sessions_user_book` integrados.
- Documentação técnica sincronizada.
- PR #13 integrado por Rebase and Merge.
- CI da `main` aprovado após o merge.

### Estado funcional

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003: ENTREGUE.
- RF-READ-004: ENTREGUE.
- RF-READ-005+: NÃO ENTREGUES.
- Próxima Sprint: NENHUMA AUTORIZADA.

### Pendência

- Divergência global de versionamento entre `/books` e `/api/v1`: PENDENTE — NÃO BLOQUEANTE.

## Sprint 04 — Reading Sessions - 2026-08-09

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-002 — Reading Sessions
**User Story:** US-READ-002-001
**Requisito Funcional:** RF-READ-003

### Entregas

- READ-002 integrada com `ReadingSession` como Aggregate Root.
- `ReadingSessionId` e `PageNumber` implementados.
- Persistência de `reading_sessions` integrada pela migration `0005`.
- Ownership por `UserId` e isolamento entre usuários preservados.
- Registro autenticado por `POST /books/{book_id}/reading-sessions`.
- `pages_read` calculado como valor derivado e não persistido.
- Timestamps funcionais normalizados para UTC.
- Documentação técnica sincronizada com a implementação.
- CI da `main` aprovado após o merge do PR #10.

### Estado funcional

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003: ENTREGUE.
- RF-READ-004+: NÃO ENTREGUES.
- Próxima Sprint: NENHUMA AUTORIZADA.

### Pendência

- Divergência global de versionamento entre `/books` e `/api/v1`: PENDENTE — NÃO BLOQUEANTE.
## Sprint 03 — Reading Library - 2026-08-09

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-001 — Cadastro de livros e consulta da biblioteca
**User Story:** US-READ-001-001
**Requisitos Funcionais:** RF-READ-001 e RF-READ-002

### Entregas

- Capability READ criada com `Book` como Aggregate Root.
- Biblioteca pessoal persistente com ownership por `UserId` e isolamento entre usuários.
- Cadastro autenticado por `POST /books`.
- Consulta autenticada por `GET /books`.
- Migration `0004` integrada como head.
- Documentação técnica READ sincronizada com a implementação.
- CI da `main` aprovado após o merge do PR #7.

### Estado funcional

- READ-001: ENTREGUE.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003+: NÃO ENTREGUES.
- Sprint 04 — Reading Sessions autorizada posteriormente pelo Product Owner.

### Pendência

- Divergência global de versionamento entre `/books` e `/api/v1`: PENDENTE — NÃO BLOQUEANTE.

## SPR-2.1 — Consolidação de Governança - 2026-08-08

**Status:** ✅ Concluída
**Autorização funcional:** Nenhuma

### Estado consolidado

- Baseline de governança e políticas de engenharia consolidadas.
- Arquitetura e isolamento entre Capabilities validados.
- Ruff e Mypy adotados como ferramentas oficiais.
- Playbook Permanente de Engenharia integrado com AI Agent Workflow, Checklists e Incident Response.
- GitHub Actions ativo com Python 3.10 validado em runner real.
- Quality Gates automatizados e três required status checks ativos na `main`.
- Branch protection preservada.
- Nenhuma Sprint funcional subsequente autorizada.

## Sprint 02 — Character - 2026-08-04

**Versão Atual:** 0.2.0
**Status:** Sprint 02 ✅ Concluída

### Resumo

A Sprint 02 expandiu a Capability Character preservando a criação atômica de User, Player e Character entregue na Sprint 01. Foram implementadas identidade tipada, representação persistente, evento de criação e consultas autenticadas somente leitura do Character e das informações de perfil.

As relações `User 1:1 Player` e `Player 1:1 Character` permanecem protegidas pelo domínio e pelas constraints existentes no banco. Nenhuma migration adicional foi necessária.

### Features concluídas

- CHAR-001: criação automática e única do Character.
- CHAR-002: identidade associada à representação persistente existente.
- CHAR-003: consulta autenticada do perfil do Character.
- CHAR-004: consulta autenticada das informações persistidas de perfil.

### Validação

- Ambiente virtual limpo instalado por `requirements.txt`.
- Migrations executadas até `0003 (head)` em banco novo.
- Baseline do banco local legado sincronizado com `0003` após confirmação de schema e `integrity_check: ok`.
- Suíte completa: 19 testes aprovados.
- Suíte com `DeprecationWarning` tratado como erro: 19 testes aprovados.
- Cobertura total: 96%.
- Importação individual de 69 módulos: nenhuma falha.
- Uvicorn com reload: startup concluído sem warnings.
- Endpoints Character: somente `GET /character` e `GET /character/profile`.
- Regressão da Sprint 01 preservada.

### Pendência documental conhecida

O arquivo `docs/01_PRODUCT/USE_CASES/CHAR/EPIC-CHAR.md` ainda atribui XP, Level, Progressão e Skills à Capability Character. Conforme decisão de produto, essa inconsistência não integra a Sprint 02 e deverá ser tratada em auditoria documental futura. Nenhum desses conceitos foi implementado.

## Auditoria de correção - 2026-08-04

A declaração original da Sprint 01 foi reauditada. A correção validou um ambiente
virtual limpo, instalação por `requirements.txt`, migrations até a revisão
`0003`, importação de todos os módulos, suíte completa e inicialização real do
Uvicorn. Os endpoints AUTH-001 a AUTH-005 e os fluxos de sessão já existentes
foram exercitados por testes E2E.

**Versão auditada:** 0.1.0
**Status da Sprint 01:** ✅ Concluída

## Resumo

A Sprint 01 foi concluída com sucesso, entregando a fundação arquitetural e a Capability de Autenticação completa. O sistema agora suporta o ciclo de vida de um usuário, desde o cadastro (incluindo a criação atômica de Player e Character) até o gerenciamento seguro de sessão e recuperação de conta. Todos os requisitos funcionais da Sprint foram implementados e validados por uma suíte de testes automatizados. A qualidade do código e a robustez da arquitetura foram validadas e corrigidas.

## Features Concluídas
- AUTH-001: Cadastro de usuário
- AUTH-002: Login
- AUTH-003: Logout
- AUTH-004: Recuperação de senha
- AUTH-005: Redefinição de senha

## Saúde do Projeto
- **Cobertura de Testes:** Alta para os fluxos implementados.
- **Débito Técnico:** Baixo.
- **Documentação:** Atualizada.
