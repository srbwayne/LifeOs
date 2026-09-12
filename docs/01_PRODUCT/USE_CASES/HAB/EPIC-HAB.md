# EPIC-HAB — Habits

## Código

HAB

## Objetivo

Gerenciar os hábitos do Player dentro do LifeOS.

A Capability Habits é responsável por registrar definições de hábitos e fatos binários de conclusão do Player. No V1, é owner-private e limitada a HAB-001 (Cadastro de hábitos) e HAB-002 (Checklist diário). HAB-003..005 permanecem DEFERRED; não há integração atual com Game/Logos, Analytics ou AI/Noema.

---

## Responsabilidades

A Capability Habits é responsável por:

- Cadastro de Hábitos;
- Checklist diário e histórico de HabitCompletion (HAB-002);
- Frequência (HAB-004) — DEFERRED;
- Sequência/Streak (HAB-003) — DEFERRED;
- Estatísticas (HAB-005) — DEFERRED;
- Rotinas e evolução — conceitos futuros DEFERRED.

---

## Features

- HAB-001 — Cadastro de Hábitos;
- HAB-002 — Checklist diário
- HAB-003 — Sequência (Streak)
- HAB-004 — Frequência
- HAB-005 — Estatísticas

V1 = HAB-001 + HAB-002. HAB-003..005 = DEFERRED.

---

## Dependências

- AUTH;
- persistência owner-scoped do LifeOS.

CHAR, GAME, Analytics e AI/Noema são dependências futuras, não ativadas no V1.

Authentication garante a identidade do Player. O V1 registra fatos no LifeOS; não calcula evolução nem envia dados à Game Engine.

---

## Consumidores

A Capability Habits disponibiliza dados ao próprio proprietário e às telas internas autorizadas do LifeOS. Exposição externa, Logos, Noema/AI e Analytics permanecem DEFERRED.

---

## Regras Gerais

Habits deverá garantir que:

- cada hábito pertença exclusivamente ao Player autenticado;
- cada Habit pertença exclusivamente ao proprietário autenticado;
- HabitCompletion seja um fato binário único por proprietário, hábito e data civil;
- a repetição da marcação seja idempotente e a remoção permita correção histórica;
- desativação preserve fatos históricos e impeça novas conclusões;
- não haja despacho de eventos, progressão, Logos ou Noema/AI no V1.

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

No V1, a Capability Habits não integra Game/Logos, Progression, Analytics ou AI/Noema e não despacha eventos externos. Integrações futuras permanecem uma possibilidade arquitetural DEFERRED.

---

## Critérios de Aceite da Capability

A Capability Habits será considerada completa quando:

- HAB-001 e HAB-002 forem implementados conforme autorização futura;
- hábitos puderem ser cadastrados, desativados e reativados;
- fatos binários puderem ser marcados, consultados e corrigidos por data civil;
- o histórico permanecer owner-scoped;
- HAB-003..005 forem tratados como escopo separado e DEFERRED;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.
