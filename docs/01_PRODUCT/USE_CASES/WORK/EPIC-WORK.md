# EPIC-WORK — Workout

## Código

WORK

## Objetivo

Gerenciar todas as atividades físicas realizadas pelo Player dentro do LifeOS.

A Capability Workout é responsável pelo registro, acompanhamento e evolução dos treinamentos físicos, permitindo que o Character evolua de forma consistente através das regras oficiais da Game Engine.

---

## Responsabilidades

A Capability Workout é responsável por:

- Registro de Treinos;
- Corrida;
- Musculação;
- Pilates;
- Exercícios Personalizados;
- Histórico de Treinos;
- Volume de Treinamento;
- Frequência de Treinos;
- Evolução Física.

---

## Features

- WORK-001 — Registro de Treino;
- WORK-002 — Corrida;
- WORK-003 — Musculação;
- WORK-004 — Pilates;
- WORK-005 — Exercícios Personalizados;
- WORK-006 — Histórico de Treinos;
- WORK-007 — Estatísticas de Treino;
- WORK-008 — Evolução Física.

---

## Contrato de Produto WORK-001

WORK-001 registra um Workout concluído, owner-private, do Player autenticado.
O registro exige modalidade reconhecida e instante de início/ocorrência com
offset UTC explícito. Entradas históricas são permitidas e ocorrências futuras
são rejeitadas. Planejamento, estado em andamento, cancelamento, correção,
exclusão e gerenciamento de modalidades não pertencem ao primeiro escopo.

Um Workout pode atravessar uma fronteira de dia civil. Sua data civil segue a
data civil local representada pelo instante explícito de início. WORK-001 não
exige uma data de registro separada nem um instante explícito de término.

Workout não calcula XP nem altera Character. O fato persistido deve ficar
disponível para a Game Engine, mas o consumo da Game não é requisito síncrono
para registrar o Workout. Health é relacionamento contextual/futuro e não
dependência síncrona. Histórico completo é WORK-006.

---

## Dependências

- AUTH;
- CHAR;
- GAME (consumidor de progressão; não pré-requisito síncrono);
- HEALTH (relacionamento contextual/futuro; não pré-requisito síncrono).

Authentication garante a identidade do Player.

Character representa a evolução do usuário.

Game Engine aplica as regras oficiais de progressão.

Health fornece informações relacionadas ao estado fisiológico do Player.

---

## Consumidores

A Capability Workout disponibiliza informações para:

- Character;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

---

## Regras Gerais

Workout deverá garantir que:

- todo treino pertença ao Player autenticado;
- nenhum treino seja perdido após seu registro;
- o histórico permaneça íntegro;
- toda evolução seja baseada em atividades registradas;
- a Game Engine seja responsável pelo cálculo de experiência e progressão;
- os dados possam ser utilizados pelos módulos analíticos e pelos sistemas de Inteligência Artificial.

---

## Fluxo Simplificado

```text
Player

↓

Registro do treino

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

A Capability Workout integra-se principalmente com:

- Character;
- Health;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

Esses módulos utilizam os dados dos treinamentos para acompanhar a evolução do Player e produzir indicadores, análises e recomendações.

---

## Critérios de Aceite da Capability

A Capability Workout será considerada completa quando:

- todas as Features WORK estiverem implementadas;
- os diferentes tipos de treino puderem ser registrados;
- o histórico estiver disponível para consulta;
- a Game Engine processar corretamente a evolução do Character;
- Analytics utilizar os dados dos treinamentos;
- a Inteligência Artificial utilizar essas informações em recomendações contextualizadas;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.

Esses critérios descrevem a visão de completude da Capability Workout. Não
transformam Analytics, AI, Game consumption ou o histórico completo em
requisitos do primeiro slice de WORK-001.
