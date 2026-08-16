# EPIC-READ — Reading

## Código

READ

## Objetivo

Gerenciar toda a jornada de leitura do Player dentro do LifeOS.

A Capability Reading é responsável pelo registro, acompanhamento e evolução das atividades de leitura, permitindo que o Character desenvolva conhecimento de forma contínua através das regras oficiais da Game Engine.

---

## Responsabilidades

A Capability Reading é responsável por:

- Cadastro de Livros;
- Biblioteca Pessoal;
- Registro de Leitura;
- Sessões de Leitura;
- Controle de Progresso;
- Livros Concluídos;
- Histórico de Leitura;
- Estatísticas de Leitura;
- Evolução Intelectual.

---

## Features

- READ-001 — Biblioteca de Livros;
- READ-002 — Cadastro de Livro;
- READ-003 — Sessão de Leitura;
- READ-004 — Insights;
- READ-005 — Livros Concluídos;
- READ-006 — Histórico de Leitura;
- READ-007 — Estatísticas de Leitura;
- READ-008 — Evolução Intelectual.

---

## READ-007 — Estatísticas de Leitura

- **Objetivo:** permitir ao Player autenticado consultar estatísticas descritivas consolidadas da própria atividade de leitura.
- **Escopo V1:** global por Player, all-time, owner-scoped, sem agrupamento, filtro ou drill-down.
- **Fontes:** exclusivamente Book e ReadingSession.
- **Persistência:** derivada sob demanda; nenhum estado estatístico é persistido.
- **Contrato:** `GET /reading-statistics`, sem parâmetros, com 200 e 401 como estados funcionais.
- **Resposta:** exatamente `total_books`, `books_with_reading_sessions`, `total_reading_sessions`, `total_pages_read` e `average_pages_per_session`.
- **Semântica:** páginas são calculadas por `end_page - start_page + 1`; releituras e sobreposições contam novamente; média com duas casas decimais e ROUND_HALF_UP; zero sessões retorna `"0.00"`.
- **Fronteiras:** não retorna Progress, Insights, evolução intelectual, Analytics, ANLT, tendências, correlações, predições, scores ou completion.

## Pendências Documentais

### Sprint 07 — Reading History

- READ-006 permanece Histórico de Leitura.
- Sprint 07 inclui exclusivamente RF-READ-006.
- V1 global e all-time do Player autenticado, baseada em ReadingSessions.
- Contrato read-only, paginado por page/size, ordenado por started_at DESC e id DESC e exposto por GET /reading-sessions.
- Itens: id, book_id, book_title, start_page, end_page, pages_read, started_at, ended_at e notes.
- RF-READ-010 não integra a Sprint 07; reconciliação pendente.
- Implementação não iniciada; planejamento técnico pendente.

### Pendências anteriores preservadas

A correção direta de READ-004 para Insights torna esta Feature convergente com o Feature Catalog, o PRD e a Sprint 06. Permanecem fora do escopo deste saneamento:

- RF-READ-005 — Conclusão de Livro associado a READ-005;
- divergência de READ-005 entre Pesquisa no Feature Catalog e Livros Concluídos neste EPIC;
- READ-005 permanece divergente e READ-007 é formalizada na Sprint 08;
- READ-008 ausente no Feature Catalog;
- RF-READ-009 associado a READ-003.
- RF-READ-010 fora da Sprint 07, com reconciliação pendente.
- divergência global /api/v1 PENDING NON-BLOCKING.

---

## Dependências

- AUTH;
- CHAR;
- GAME.

Authentication garante a identidade do Player.

Character representa a evolução do usuário.

Game Engine aplica as regras oficiais de experiência, progressão e desenvolvimento relacionadas às atividades de leitura.

---

## Consumidores

A Capability Reading disponibiliza informações para:

- Character;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

---

## Regras Gerais

Reading deverá garantir que:

- toda atividade de leitura pertença ao Player autenticado;
- o progresso dos livros seja preservado;
- cada sessão de leitura seja registrada no histórico;
- livros concluídos permaneçam disponíveis para consulta;
- a evolução do Character seja calculada exclusivamente pela Game Engine;
- Analytics e Inteligência Artificial possam utilizar os dados registrados para geração de indicadores e recomendações.

---

## Fluxo Simplificado

```text
Player

↓

Início da leitura

↓

Registro da sessão

↓

Atualização do progresso

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

A Capability Reading integra-se principalmente com:

- Character;
- Dashboard;
- Analytics;
- AI Mentor;
- AI Coaching;
- Reports.

Esses módulos utilizam as informações de leitura para acompanhar a evolução intelectual do Player e produzir indicadores, análises e recomendações personalizadas.

---

## Critérios de Aceite da Capability

A Capability Reading será considerada completa quando:

- todas as Features READ estiverem implementadas;
- livros puderem ser cadastrados;
- sessões de leitura puderem ser registradas;
- o progresso dos livros for atualizado corretamente;
- o histórico de leitura estiver disponível para consulta;
- a Game Engine processar corretamente a evolução do Character;
- Analytics e Inteligência Artificial consumirem corretamente os dados produzidos por Reading;
- todas as regras permanecerem compatíveis com a arquitetura oficial do LifeOS.
