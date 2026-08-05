# EPIC-HAB — Habits

## Código

HAB

## Objetivo

Gerenciar os hábitos do Player dentro do LifeOS.

A Capability Habits é responsável por registrar, acompanhar e incentivar a execução contínua de hábitos, promovendo consistência ao longo do tempo e contribuindo para a evolução do Character por meio das regras oficiais da Game Engine.

---

## Responsabilidades

A Capability Habits é responsável por:

- Cadastro de Hábitos;
- Organização de Rotinas;
- Execução de Hábitos;
- Controle de Frequência;
- Controle de Streaks;
- Histórico de Execuções;
- Estatísticas de Consistência;
- Acompanhamento da Evolução.

---

## Features

- HAB-001 — Cadastro de Hábitos;
- HAB-002 — Rotinas;
- HAB-003 — Registro de Execução;
- HAB-004 — Frequência;
- HAB-005 — Streaks;
- HAB-006 — Histórico;
- HAB-007 — Estatísticas;
- HAB-008 — Evolução dos Hábitos.

---

## Dependências

- AUTH;
- CHAR;
- GAME.

Authentication garante a identidade do Player.

Character representa quem evolui.

Game Engine aplica as regras oficiais de experiência, progressão, missões, recompensas e demais mecanismos relacionados aos hábitos.

---

## Consumidores

A Capability Habits disponibiliza informações para:

- Character;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

---

## Regras Gerais

Habits deverá garantir que:

- cada hábito pertença exclusivamente ao Player autenticado;
- toda execução seja registrada no histórico;
- o histórico nunca seja sobrescrito;
- a frequência seja calculada automaticamente;
- os Streaks sejam calculados pelas regras oficiais da Game Engine;
- a experiência obtida seja processada exclusivamente pela Game Engine;
- Analytics e Inteligência Artificial possam utilizar os dados registrados para produção de indicadores e recomendações.

---

## Fluxo Simplificado

```text
Player

↓

Execução do hábito

↓

Validação

↓

Persistência

↓

Game Engine

↓

Atualização do Character

↓

Analytics

↓

IA

↓

Dashboard
```

---

## Integração com a Plataforma

A Capability Habits integra-se principalmente com:

- Character;
- Game Engine;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

Os hábitos representam uma das principais fontes de evolução contínua do Character, alimentando os mecanismos de Progression, Experience, Streaks, Quests, Missions e Rewards definidos pela Game Engine.

---

## Critérios de Aceite da Capability

A Capability Habits será considerada completa quando:

- todas as Features HAB estiverem implementadas;
- hábitos puderem ser cadastrados e organizados;
- execuções puderem ser registradas;
- o histórico permanecer disponível para consulta;
- os Streaks forem calculados corretamente;
- a Game Engine processar corretamente a evolução do Character;
- Analytics e Inteligência Artificial consumirem corretamente os dados produzidos por Habits;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.