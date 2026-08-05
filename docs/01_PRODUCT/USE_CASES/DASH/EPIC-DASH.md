# EPIC-DASH — Dashboard

## Código

DASH

## Objetivo

Centralizar a visualização das informações mais relevantes do LifeOS, permitindo que o Player acompanhe a evolução do seu Character, seus objetivos, indicadores e atividades por meio de uma interface unificada.

O Dashboard representa o principal ponto de interação do usuário com a plataforma.

---

## Responsabilidades

A Capability Dashboard é responsável por:

- Dashboard Principal;
- Character Overview;
- Status do Character;
- Indicadores Gerais;
- Objetivos Ativos;
- Progresso Diário;
- Progresso Semanal;
- Progresso Sazonal;
- Resumo de Atividades;
- Atalhos para funcionalidades da plataforma.

---

## Features

- DASH-001 — Dashboard Principal;
- DASH-002 — Character Overview;
- DASH-003 — Status do Character;
- DASH-004 — Indicadores Gerais;
- DASH-005 — Objetivos Ativos;
- DASH-006 — Resumo Diário;
- DASH-007 — Resumo Semanal;
- DASH-008 — Resumo Sazonal;
- DASH-009 — Atividades Recentes;
- DASH-010 — Atalhos Rápidos.

---

## Dependências

- AUTH;
- CHAR;
- GAME;
- HEALTH;
- WORK;
- READ;
- THER;
- HAB;
- ANLT;
- AI.

O Dashboard consolida informações produzidas pelas demais Capabilities.

Ele não implementa regras de negócio.

---

## Consumidores

O principal consumidor desta Capability é:

- Player.

Outras Capabilities poderão utilizar componentes do Dashboard para apresentação de informações.

---

## Regras Gerais

A Capability Dashboard deverá garantir que:

- todas as informações apresentadas pertençam ao Player autenticado;
- os dados exibidos representem o estado atual da plataforma;
- o Character seja o elemento central da interface;
- os indicadores sejam provenientes do Analytics;
- a evolução apresentada seja produzida pela Game Engine;
- recomendações sejam fornecidas pela camada de Inteligência Artificial;
- a interface permaneça consistente entre todos os módulos.

---

## Fluxo Simplificado

```text
Player

↓

Dashboard

↓

Character

↓

Game Engine

↓

Analytics

↓

AI

↓

Visualização Consolidada
```

---

## Integração com a Plataforma

A Capability Dashboard integra informações provenientes de:

- Authentication;
- Character;
- Health;
- Workout;
- Reading;
- Therapy;
- Habits;
- Game Engine;
- Analytics;
- Artificial Intelligence;
- Reports.

O Dashboard não produz informações.

Sua responsabilidade é consolidar e apresentar os dados produzidos pelos demais módulos da plataforma.

---

## Critérios de Aceite da Capability

A Capability Dashboard será considerada completa quando:

- todas as Features DASH estiverem implementadas;
- o Character Overview estiver funcional;
- os indicadores forem apresentados corretamente;
- os objetivos ativos forem exibidos;
- os resumos diário, semanal e sazonal estiverem disponíveis;
- as informações estiverem sincronizadas com as demais Capabilities;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.