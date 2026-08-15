# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | Sprint 07 |
| Iniciativa | Sprint 07 — Reading History |
| Status | CONCLUÍDA |
| Tipo | Funcional |
| Capability | READ |
| Feature | READ-006 — Histórico |
| User Story | US-READ-006-001 |
| Requisito Funcional | RF-READ-006 |
| Especificação funcional | APROVADA / FROZEN |
| Implementação | INTEGRADA |
| Planejamento técnico | APROVADO |
| CI | APROVADO |

---

# Escopo Autorizado

- Histórico global e all-time do Player autenticado, formado por suas ReadingSessions.
- Consulta read-only por `GET /reading-sessions`.
- Paginação por `page` e `size`, defaults 1 e 20, com `size` máximo 100.
- Ordenação por `started_at DESC` e `id DESC`.
- Itens com exatamente `id`, `book_id`, `book_title`, `start_page`, `end_page`, `pages_read`, `started_at`, `ended_at` e `notes`.
- Histórico vazio retorna 200 com coleção vazia; nenhum filtro funcional integra a V1.

---

# Estado das Entregas

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- READ-004: ENTREGUE.
- READ-006: ENTREGUE.
- RF-READ-001..004: ENTREGUES.
- RF-READ-005: NÃO ENTREGUE.
- RF-READ-006: ENTREGUE.
- RF-READ-007..010: NÃO ENTREGUES.
- RF-READ-011: ENTREGUE.

> A numeração dos requisitos não implica ordem de entrega.

---

# Fora do Escopo

- RF-READ-010 — Jornada Consolidada;
- READ-005, RF-READ-005, READ-007, READ-008 e RF-READ-009;
- Progress ou Insights agregados;
- filtros, busca, Analytics, AI, GAME ou conclusão persistida;
- edição ou exclusão de ReadingSession;
- versionamento isolado em `/api/v1`;
- implementação antes da aprovação do planejamento técnico.

---

# Pendências Documentais Fora da Sprint

- READ-005: DIVERGÊNCIA PENDENTE.
- RF-READ-005: PENDENTE.
- READ-007: AUSENTE NO FEATURE CATALOG.
- READ-008: AUSENTE NO FEATURE CATALOG.
- RF-READ-009: ASSOCIAÇÃO PENDENTE.
- RF-READ-010: FORA DA SPRINT 07 — RECONCILIAÇÃO PENDENTE.
- `/api/v1`: PENDING NON-BLOCKING.

---

# Próximo Gate

PRODUCT DECISION — NEXT SCOPE

NENHUMA NOVA SPRINT AUTORIZADA. Nenhuma nova Feature ou RF está autorizada
automaticamente; READ-005, READ-007, READ-008 e os demais escopos permanecem
dependentes de decisão explícita de Produto.
