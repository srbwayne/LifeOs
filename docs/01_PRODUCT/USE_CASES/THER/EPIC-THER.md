# EPIC-THER — Therapy

## Código

THER

## Objetivo

Gerenciar o acompanhamento terapêutico do Player dentro do LifeOS.

A Capability Therapy é responsável pelo registro, organização e acompanhamento das sessões terapêuticas, permitindo que o Player acompanhe sua evolução emocional e comportamental ao longo do tempo, preservando a privacidade das informações registradas.

---

## Responsabilidades

A Capability Therapy é responsável por:

- Cadastro de terapeutas;
- Registro de sessões;
- Agenda de sessões;
- Histórico terapêutico;
- Registro de observações;
- Registro de evolução;
- Estatísticas de acompanhamento;
- Evolução do bem-estar emocional.

---

## Features

- THER-001 — Cadastro de Terapeuta;
- THER-002 — Registro de Sessão;
- THER-003 — Agenda de Sessões;
- THER-004 — Histórico Terapêutico;
- THER-005 — Registro de Observações;
- THER-006 — Evolução Terapêutica;
- THER-007 — Estatísticas;
- THER-008 — Acompanhamento Contínuo.

---

## Dependências

- AUTH;
- CHAR;
- GAME.

Authentication garante a identidade do Player.

Character representa a evolução do usuário.

Game Engine aplica as regras oficiais relacionadas à progressão decorrente das atividades terapêuticas.

---

## Consumidores

A Capability Therapy disponibiliza informações para:

- Character;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

---

## Regras Gerais

Therapy deverá garantir que:

- todas as sessões pertençam exclusivamente ao Player autenticado;
- o histórico terapêutico permaneça preservado;
- registros anteriores nunca sejam sobrescritos;
- informações sensíveis respeitem as configurações de privacidade do usuário;
- Analytics e Inteligência Artificial utilizem apenas dados autorizados;
- a evolução do Character seja calculada exclusivamente pelas regras oficiais da Game Engine.

---

## Fluxo Simplificado

```text
Player

↓

Registro da sessão

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

A Capability Therapy integra-se principalmente com:

- Character;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

Esses módulos utilizam as informações registradas para acompanhar a evolução do Player e fornecer análises e recomendações contextualizadas, sempre respeitando as permissões de acesso definidas pelo usuário.

---

## Critérios de Aceite da Capability

A Capability Therapy será considerada completa quando:

- todas as Features THER estiverem implementadas;
- sessões terapêuticas puderem ser registradas;
- o histórico estiver disponível para consulta;
- os registros respeitarem as configurações de privacidade;
- a Game Engine processar corretamente a evolução do Character;
- Analytics e Inteligência Artificial consumirem corretamente os dados autorizados;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.