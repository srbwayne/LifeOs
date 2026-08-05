# EPIC-CHAR — Character

## Código

CHAR

## Objetivo

Representar digitalmente a evolução do Player ao longo de toda a sua jornada no LifeOS.

O Character é a entidade central da plataforma e consolida todas as informações relacionadas à progressão, atributos, estatísticas, conquistas e desenvolvimento do usuário.

Toda ação registrada pelo Player impacta, direta ou indiretamente, a evolução do seu Character.

---

## Responsabilidades

A Capability Character é responsável por:

- Criação automática do Character;
- Character Sheet;
- Avatar;
- Perfil do Character;
- Atributos;
- Estatísticas;
- Inteligências Múltiplas;
- Experiência (XP);
- Nível Global;
- Progressão;
- Skills;
- Classes;
- Perks;
- Títulos;
- Badges;
- Histórico de evolução;
- Visualização do estado atual do Character.

---

## Features

- CHAR-001 — Character Sheet;
- CHAR-002 — Avatar;
- CHAR-003 — Perfil do Character;
- CHAR-004 — Atributos;
- CHAR-005 — Barra de XP;
- CHAR-006 — Nível Global;
- CHAR-007 — Títulos;
- CHAR-008 — Guilda;
- CHAR-009 — Classe;
- CHAR-010 — Histórico de evolução.

---

## Dependências

- AUTH;
- GAME.

Authentication garante a identidade do Player.

Gamification fornece as regras responsáveis pela evolução do Character.

---

## Consumidores

A Capability Character disponibiliza informações para:

- Dashboard;
- Health;
- Workout;
- Reading;
- Therapy;
- Habits;
- Analytics;
- Artificial Intelligence;
- Reports;
- Notifications.

Praticamente toda a plataforma utiliza informações do Character.

---

## Regras Gerais

Character deverá garantir que:

- cada Player possua exatamente um Character;
- o Character represente toda a evolução do usuário;
- atributos sejam atualizados apenas pelas regras oficiais da Game Engine;
- experiência seja calculada exclusivamente pelo sistema de Progression;
- níveis sejam derivados da experiência acumulada;
- Skills, Classes, Perks, Badges e Títulos respeitem os critérios definidos pela Game Engine;
- todo histórico de evolução permaneça rastreável;
- o estado atual do Character reflita todas as ações registradas pelo Player.

---

## Fluxo Simplificado

```text
Player

↓

Registro de atividade

↓

Game Engine

↓

Atualização do Character

↓

Progressão

↓

Dashboard

↓

Analytics

↓

IA
```

---

## Integração com a Game Engine

O Character atua como principal consumidor das regras da Game Engine.

Entre os componentes integrados estão:

- Experience;
- Leveling;
- Progression;
- Attributes;
- Stats;
- Skills;
- Classes;
- Perks;
- Achievements;
- Rewards;
- Titles;
- Badges.

A evolução do Character ocorre exclusivamente através dessas regras.

---

## Critérios de Aceite da Capability

A Capability Character será considerada completa quando:

- todas as Features CHAR estiverem implementadas;
- cada Player possuir exatamente um Character;
- Character Sheet estiver funcional;
- sistema de atributos estiver operacional;
- experiência e progressão estiverem integradas à Game Engine;
- histórico de evolução estiver disponível;
- Dashboard, Analytics e IA consumirem corretamente as informações do Character;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.