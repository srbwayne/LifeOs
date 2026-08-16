# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | Sprint 08 |
| Iniciativa | Sprint 08 — Reading Statistics |
| Status | AUTORIZADA |
| Tipo | Funcional |
| Capability | READ |
| Feature | READ-007 — Estatísticas de Leitura |
| User Story | US-READ-007-001 |
| Requisito Funcional | RF-READ-007 |
| Product Specification | APROVADA / FROZEN |
| Implementação | NÃO INICIADA |
| Architecture Review | PENDING |
| Technical Plan | PENDING |
| Implementation Authorization | NO |

---

# Escopo Autorizado

- Sprint 08 contém exclusivamente READ-007, RF-READ-007 e US-READ-007-001.
- Estatísticas descritivas globais, all-time e owner-scoped do Player autenticado.
- Fontes funcionais: Book e ReadingSession.
- Persistência: derived on demand, sem novo estado estatístico.
- Consulta read-only por `GET /reading-statistics`, sem parâmetros.
- Resposta com exatamente `total_books`, `books_with_reading_sessions`, `total_reading_sessions`, `total_pages_read` e `average_pages_per_session`.
- `total_pages_read` usa `end_page - start_page + 1`; releituras e sobreposições contam novamente.
- `average_pages_per_session` usa duas casas decimais e ROUND_HALF_UP; zero sessões retorna `"0.00"`.
- Empty state retorna 200 com os cinco campos zerados.
- Status funcionais: 200 OK e 401 Unauthorized.
- Não há agrupamento, filtros, drill-down ou estatísticas por Book ou sessão.

---

# Estado das Entregas

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- READ-004: ENTREGUE.
- READ-006: ENTREGUE.
- READ-007: ESPECIFICAÇÃO FROZEN / IMPLEMENTAÇÃO NÃO INICIADA.
- RF-READ-001..004: ENTREGUES.
- RF-READ-005: NÃO ENTREGUE.
- RF-READ-006: ENTREGUE.
- RF-READ-007: ESPECIFICAÇÃO FROZEN / IMPLEMENTAÇÃO NÃO INICIADA.
- RF-READ-008..010: NÃO ENTREGUES.
- RF-READ-011: ENTREGUE.

> A numeração dos requisitos não implica ordem de entrega.

---

# Fora do Escopo

- READ-005, RF-READ-005, READ-008, RF-READ-009 e RF-READ-010;
- ReadingProgress e ReadingInsights como fontes ou resultados de READ-007;
- Insights, progresso, completion, Analytics, ANLT, AI, GAME, tendências, correlações, previsões ou scores;
- estatísticas por Book, por sessão, agrupamentos temporais, filtros ou drill-down;
- persistência de estatísticas, snapshots, cache persistido ou novo estado estatístico;
- versionamento isolado em `/api/v1`;
- implementação antes de Architecture Review e Technical Plan aprovados.

---

# Pendências Documentais Fora da Sprint

- READ-005: DIVERGÊNCIA PENDENTE / DEFERRED.
- RF-READ-005: PENDENTE / DEFERRED.
- READ-008: DEFERRED.
- RF-READ-009: ASSOCIAÇÃO PENDENTE / DEFERRED.
- RF-READ-010: RECONCILIAÇÃO PENDENTE / DEFERRED.
- `/api/v1`: PENDING NON-BLOCKING.

---

# Próximo Gate

ARCHITECTURE REVIEW + TECHNICAL PLAN — SPRINT 08 READ-007

Este gate somente poderá ocorrer após auditoria, publicação, PR, review,
merge e CI da main da formalização documental.
