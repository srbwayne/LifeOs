# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para execução.

---

# Estado Atual

| Campo | Valor |
|---|---|
| ID | READ-005-PRODUCT-SPEC |
| Iniciativa | READ-005 — Livros Concluídos |
| Status | PRODUCT SPECIFICATION APPROVED / FROZEN |
| Tipo | Produto / Documental |
| Capability | READ |
| Feature | READ-005 — Livros Concluídos |
| Requisito Funcional | RF-READ-005 — Conclusão de Livro |
| User Story | US-READ-005-001 |
| Product Decision | PD-READ-005 — APPROVED |
| Product Identity | FROZEN |
| Completion Model | AUTOMATIC COMPLETION MILESTONE |
| Completion Semantics | APPROVED / FROZEN |
| Product Specification | APPROVED / FROZEN |
| Architecture Review | PENDING |
| Technical Plan | NOT AUTHORIZED |
| Implementation Authorization | NO |
| Sprint 09 | NOT AUTHORIZED |

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

## Pendências

- READ-005: PRODUCT SPECIFICATION APPROVED / NOT DELIVERED.
- RF-READ-005: PRODUCT SPECIFICATION APPROVED / NOT DELIVERED.
- US-READ-005-001: APPROVED / NOT DELIVERED.
- READ-008: DEFERRED.
- RF-READ-009: ASSOCIAÇÃO PENDENTE / DEFERRED.
- RF-READ-010: RECONCILIAÇÃO PENDENTE / DEFERRED.
- `/api/v1`: PENDING NON-BLOCKING.
- Pesquisa: OUTSIDE READ-005 / NO FEATURE AUTHORIZED.

## Product Specification Boundary

Product Specification de READ-005 está aprovada e congelada. Persistência,
representação técnica, endpoint, HTTP, eventos, arquitetura e Technical Plan
permanecem decisões futuras de Architecture Review. Isto não autoriza
Implementation nem Sprint 09.

## Próximo Gate

ARCHITECTURE REVIEW — READ-005 LIVROS CONCLUÍDOS

THIS DOES NOT AUTHORIZE SPRINT 09.