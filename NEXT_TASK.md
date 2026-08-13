# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | Sprint 05 |
| Iniciativa | Sprint 05 — Reading Progress |
| Status | AUTORIZADA |
| Tipo | Funcional |
| Capability | READ |
| Feature | READ-003 — Reading Progress |
| User Story | US-READ-003-001 |
| Requisito Funcional | RF-READ-004 |
| Implementação | CONCLUÍDA LOCALMENTE |
| Integração | PENDENTE |
| PR | AINDA NÃO ABERTO |

---

# Escopo Autorizado

- READ-003 — Reading Progress.
- RF-READ-004 — consulta do progresso atual de leitura.
- O progresso será derivado exclusivamente das ReadingSessions existentes do Book.
- Nenhum estado de progresso será persistido no Book nesta Feature.

---

# Estado das Entregas

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: IMPLEMENTADA LOCALMENTE, AGUARDANDO AUDITORIA, PR E INTEGRAÇÃO.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003: ENTREGUE.
- RF-READ-004: AUTORIZADO.
- RF-READ-005+: FORA DO ESCOPO.

---

# Próximos Gates

1. Auditoria pré-PR.
2. Push.
3. PR.
4. CI.
5. Review.
6. Merge.
7. Fechamento da Sprint.

READ-003 continua sendo a única Feature funcional ativa. Nenhuma Sprint posterior está autorizada.

---

# Pendência

A divergência global de versionamento entre `/books` e `/api/v1` permanece PENDENTE — NÃO BLOQUEANTE.
