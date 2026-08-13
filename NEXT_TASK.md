# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | Sprint 06 |
| Iniciativa | Sprint 06 — Reading Insights |
| Status | AUTORIZADA |
| Tipo | Funcional |
| Capability | READ |
| Feature | READ-004 — Insights |
| User Story | US-READ-004-001 |
| Requisito Funcional | RF-READ-011 |
| Implementação | NÃO INICIADA |
| Planejamento técnico | PENDENTE |

---

# Escopo Autorizado

- Quatro Insights determinísticos sobre a cobertura atual de um único Book:
  - cobertura restante;
  - lacunas de cobertura;
  - última página alcançada com lacunas;
  - cobertura integral confirmada.
- Escopo exclusivamente por Book e all-time.
- Dados derivados de Book, ReadingSessions e ReadingProgress.
- Operação read-only, sem persistência de Insights.

---

# Estado das Entregas

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- READ-004: AUTORIZADA.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003: ENTREGUE.
- RF-READ-004: ENTREGUE.
- RF-READ-005..010: NÃO ENTREGUES.
- RF-READ-011: AUTORIZADO.

---

# Fora do Escopo

- visão consolidada da biblioteca;
- períodos, comparações, duração, frequência ou tendências;
- volume bruto de releitura;
- análise de notes, AI, LLM, recomendações ou coaching;
- Analytics, KPIs, scores ou correlações;
- GAME, XP, Level, Skills, Attributes, Rewards ou eventos;
- Pesquisa ou Histórico completo;
- conclusão persistida de Book ou evento de conclusão;
- RF-READ-005..010;
- alteração de Book ou ReadingSession.

---

# Pendências Documentais Fora da Sprint

- RF-READ-005 — Conclusão de Livro permanece associado a READ-005.
- READ-005 permanece divergente entre Pesquisa e Livros Concluídos no EPIC-READ.
- READ-007 e READ-008 permanecem ausentes no Feature Catalog.
- RF-READ-009 permanece associado a READ-003.

---

# Pendência

A divergência global de versionamento entre `/books` e `/api/v1` permanece PENDENTE — NÃO BLOQUEANTE.
