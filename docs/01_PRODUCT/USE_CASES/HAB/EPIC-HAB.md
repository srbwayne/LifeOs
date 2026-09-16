# EPIC-HAB — Habits

## Current HAB-003 Governance

HAB-003 — Sequência (Streak) is a post-V1 initiative with Product Contract,
Architecture, and Technical Plan APPROVED / FROZEN under
`HAB-003-TP-DEC-001` dated 2026-09-15. The canonical Technical Plan is
`docs/10_AI_ENGINEERING/HAB_003_TECHNICAL_PLAN.md`.

Implementation remains NOT AUTHORIZED. The next gate is
`HAB-003-IA-001 — IMPLEMENTATION AUTHORIZATION / PRE-FLIGHT REVIEW`.

HABITS V1 remains HAB-001 + HAB-002 — CLOSED. HAB-004 and HAB-005 remain
DEFERRED, with no Game, Logos, Analytics, or AI/Noema integration.

---

## Código

HAB

## Objetivo

Gerenciar os hábitos do Player dentro do LifeOS.

A Capability Habits é responsável por registrar definições de hábitos, fatos binários de conclusão e a leitura derivada de Streak do Player. Habits V1 permanece CLOSED como HAB-001 (Cadastro de hábitos) e HAB-002 (Checklist diário). HAB-003 é uma iniciativa pós-V1 selecionada, com contrato de produto e arquitetura aprovados/frozen, mas implementação não autorizada. HAB-004 e HAB-005 permanecem DEFERRED; não há integração atual com Game/Logos, Analytics ou AI/Noema.

---

## Responsabilidades

A Capability Habits é responsável por:

- Cadastro de Hábitos;
- Checklist diário e histórico de HabitCompletion (HAB-002);
- Sequência/Streak derivada de fatos HabitCompletion (HAB-003) — PRODUCT CONTRACT / ARCHITECTURE APPROVED, IMPLEMENTATION NOT AUTHORIZED;
- Frequência (HAB-004) — DEFERRED;
- Estatísticas (HAB-005) — DEFERRED;
- Rotinas e evolução — conceitos futuros DEFERRED.

---

## Features

- HAB-001 — Cadastro de Hábitos;
- HAB-002 — Checklist diário
- HAB-003 — Sequência (Streak)
- HAB-004 — Frequência
- HAB-005 — Estatísticas

Habits V1 = HAB-001 + HAB-002 — CLOSED. HAB-003 é iniciativa pós-V1 selecionada; HAB-004 e HAB-005 = DEFERRED.

---

## Dependências

- AUTH;
- persistência owner-scoped do LifeOS.

CHAR, GAME, Analytics e AI/Noema não são dependências de HAB-003. HAB-004 (Frequência) e HAB-005 (Estatísticas) permanecem features DEFERRED e não participam da arquitetura do HAB-003.

Authentication garante a identidade do Player. O V1 registra fatos no LifeOS; não calcula evolução nem envia dados à Game Engine.

---

## Consumidores

A Capability Habits disponibiliza dados ao próprio proprietário e às telas internas autorizadas do LifeOS. O Streak permanece owner-private e derivado de HabitCompletion; exposição externa, Logos, Noema/AI e Analytics permanecem não integrados.

---

## Regras Gerais

Habits deverá garantir que:

- cada Habit pertença exclusivamente ao proprietário autenticado;
- HabitCompletion seja um fato binário único por proprietário, hábito e data civil;
- a repetição da marcação seja idempotente e a remoção permita correção histórica;
- desativação preserve fatos históricos e impeça novas conclusões;
- não haja despacho de eventos, progressão, Logos ou Noema/AI no V1.
- HAB-003 use somente uma data civil de avaliação explicitamente fornecida à aplicação;
- HAB-003 permaneça calendar-consecutive, sem frequência, longest streak ou estado durável de Streak.

---

## Fluxo Simplificado

```text
Player autenticado

↓

Cadastro do Habit (HAB-001)

↓

Marcação explícita de record_date (HAB-002)

↓

Validação owner-scoped

↓

Persistência do fato binário / consulta do histórico
```

---

## Integração com a Plataforma

Habits não integra Game/XP/Logos, Progression, Analytics ou AI/Noema e não despacha eventos. HAB-003 permanece dentro da Capability HAB, sem dependência dessas integrações.

---

## Critérios de Aceite da Capability

A Capability Habits será considerada completa quando:

- HAB-001 e HAB-002 forem implementados conforme autorização futura;
- hábitos puderem ser cadastrados, desativados e reativados;
- fatos binários puderem ser marcados, consultados e corrigidos por data civil;
- o histórico permanecer owner-scoped;
- HAB-003 seja tratado como iniciativa pós-V1 separada, com implementação ainda não autorizada;
- HAB-004 e HAB-005 permaneçam DEFERRED;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.
