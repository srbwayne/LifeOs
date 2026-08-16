# FEATURE_CATALOG

## LifeOS
### Catálogo Oficial de Funcionalidades

**Versão:** 1.0

**Status:** Documento Oficial

---

# Objetivo

Este documento define todas as funcionalidades oficiais do LifeOS.

Cada funcionalidade possui um identificador único (Feature ID).

Esse identificador deverá ser utilizado em:

- PRD
- User Stories
- Sprints
- Casos de Uso
- Testes
- Commits
- Pull Requests
- Changelog
- Roadmap
- Documentação Técnica

Nenhuma funcionalidade deve ser implementada sem possuir um Feature ID.

---

# Estrutura do Feature ID

Formato:

AAA-999

Exemplos

AUTH-001

CHAR-003

WORK-014

GAME-021

ANLT-008

---

# AUTH — Authentication

Responsável pela autenticação e gestão de usuários.

| ID | Feature |
|----|----------|
| AUTH-001 | Cadastro de usuário |
| AUTH-002 | Login |
| AUTH-003 | Logout |
| AUTH-004 | Recuperação de senha |
| AUTH-005 | Redefinição de senha |
| AUTH-006 | Alteração de senha |
| AUTH-007 | Sessão autenticada |
| AUTH-008 | Multi-Tenant |
| AUTH-009 | Perfil do usuário |
| AUTH-010 | Configurações da conta |

---

# CHAR — Character

Responsável pela representação do Player.

| ID | Feature |
|----|----------|
| CHAR-001 | Character Sheet |
| CHAR-002 | Avatar |
| CHAR-003 | Perfil do Character |
| CHAR-004 | Informações de perfil |
| CHAR-007 | Títulos |
| CHAR-008 | Guilda |
| CHAR-009 | Classe |
| CHAR-010 | Histórico de evolução |

---

# HEALTH — Saúde

| ID | Feature |
|----|----------|
| HEALTH-001 | Registro de Sono |
| HEALTH-002 | Registro de VFC |
| HEALTH-003 | Registro de Frequência Cardíaca |
| HEALTH-004 | Registro de Energia |
| HEALTH-005 | Recuperação |
| HEALTH-006 | Bioimpedância |
| HEALTH-007 | Histórico |
| HEALTH-008 | Evolução corporal |

---

# WORK — Exercícios

| ID | Feature |
|----|----------|
| WORK-001 | Cadastro de modalidades |
| WORK-002 | Registro de treino |
| WORK-003 | Histórico |
| WORK-004 | Frequência semanal |
| WORK-005 | Evolução |
| WORK-006 | Estatísticas |
| WORK-007 | FC Média |
| WORK-008 | Esforço percebido |

---

# READ — Leitura

| ID | Feature |
|----|----------|
| READ-001 | Cadastro de livros |
| READ-002 | Registro de leitura |
| READ-003 | Progresso |
| READ-004 | Insights |
| READ-005 | Pesquisa |
| READ-006 | Histórico |
| READ-007 | Estatísticas de Leitura |

---

# THER — Terapia

| ID | Feature |
|----|----------|
| THER-001 | Cadastro de terapeutas |
| THER-002 | Sessões |
| THER-003 | Evolução |
| THER-004 | Clareza mental |
| THER-005 | Histórico |

---

# HAB — Hábitos

| ID | Feature |
|----|----------|
| HAB-001 | Cadastro de hábitos |
| HAB-002 | Checklist diário |
| HAB-003 | Sequência (Streak) |
| HAB-004 | Frequência |
| HAB-005 | Estatísticas |

---

# GAME — Gamificação

| ID | Feature |
|----|----------|
| GAME-001 | XP Engine |
| GAME-002 | Level Engine |
| GAME-003 | Sistema de Atributos |
| GAME-004 | Skills |
| GAME-005 | Quests |
| GAME-006 | Daily Quests |
| GAME-007 | Weekly Quests |
| GAME-008 | Monthly Quests |
| GAME-009 | Achievements |
| GAME-010 | Badges |
| GAME-011 | Rewards |
| GAME-012 | Ranking |
| GAME-013 | Progressão |
| GAME-014 | Curva de XP |
| GAME-015 | Sistema de Classes |
| GAME-016 | Guildas |
| GAME-017 | Títulos |
| GAME-018 | Especializações |

## Rastreabilidade de Features absorvidas

| Feature anterior | Feature oficial | Motivo |
|------------------|-----------------|--------|
| CHAR-005 — Barra de XP | GAME-001 — XP Engine | XP é responsabilidade exclusiva da Capability GAME. |
| CHAR-006 — Nível Global | GAME-002 — Level Engine | Level é responsabilidade exclusiva da Capability GAME. |

---

# DASH — Dashboard

| ID | Feature |
|----|----------|
| DASH-001 | Character Sheet |
| DASH-002 | Radar de atributos |
| DASH-003 | KPIs |
| DASH-004 | Timeline |
| DASH-005 | Cards |
| DASH-006 | Evolução semanal |
| DASH-007 | Evolução mensal |
| DASH-008 | Atividades recentes |

---

# ANLT — Analytics

| ID | Feature |
|----|----------|
| ANLT-001 | KPIs |
| ANLT-002 | Correlações |
| ANLT-003 | Tendências |
| ANLT-004 | Comparativos |
| ANLT-005 | Insights |
| ANLT-006 | Score Geral |
| ANLT-007 | Indicadores |
| ANLT-008 | Previsões |

---

# AI — Inteligência Artificial

| ID | Feature |
|----|----------|
| AI-001 | Mentor |
| AI-002 | Recomendações |
| AI-003 | Missões inteligentes |
| AI-004 | Resumo semanal |
| AI-005 | Resumo mensal |
| AI-006 | Alertas |
| AI-007 | Coaching |
| AI-008 | Explicações |
| AI-009 | Análise comportamental |

---

# REPORT — Relatórios

| ID | Feature |
|----|----------|
| REPORT-001 | CSV |
| REPORT-002 | Excel |
| REPORT-003 | PDF |
| REPORT-004 | Relatório consolidado |

---

# ADMIN

| ID | Feature |
|----|----------|
| ADMIN-001 | Configurações |
| ADMIN-002 | Preferências |
| ADMIN-003 | Logs |
| ADMIN-004 | Auditoria |
| BACKUP-001 | Backup automático |
| BACKUP-002 | Backup manual |
| BACKUP-003 | Restore |

> `BACKUP-001`, `BACKUP-002` e `BACKUP-003` são identificadores legados preservados para rastreabilidade. As três Features pertencem à Capability `ADMIN`.

---

# Convenções

Toda nova funcionalidade deverá:

- possuir Feature ID;
- pertencer a uma categoria existente;
- ser documentada no PRD;
- possuir User Story;
- possuir Critérios de Aceite;
- possuir testes;
- ser rastreável durante todo o ciclo de desenvolvimento.

---

# Fluxo Oficial

```
Feature Catalog

↓

PRD

↓

User Story

↓

Sprint

↓

Implementação

↓

Testes

↓

Release
```

---

# Exemplo de Uso

Feature:

GAME-005

↓

User Story

US-GAME-005-001

↓

Sprint

SPRINT-07

↓

Commit

feat(game): GAME-005 - Implement Quest Engine

↓

Teste

TEST-GAME-005

↓

Release

v1.0
