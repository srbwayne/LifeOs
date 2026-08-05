# LAYOUT

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Layout  
**Camadas Relacionadas:** Presentation  
**Arquiteturas Relacionadas:** Design System, UI Architecture, Clean Architecture

---

# 1. Objetivo

Este documento define a arquitetura oficial de **Layout** do LifeOS.

Seu objetivo é estabelecer como toda a interface será organizada espacialmente, garantindo consistência, reutilização e uma excelente experiência do usuário.

O Layout define:

- organização da tela;
- posicionamento dos componentes;
- distribuição de espaços;
- hierarquia visual;
- comportamento responsivo;
- navegação visual;
- áreas funcionais.

O Layout não define cores, tipografia ou componentes individuais.

Esses aspectos pertencem ao Design System e ao Theme.

---

# 2. Filosofia

O Layout do LifeOS foi inspirado em:

- MMORPG HUD;
- IDEs modernas;
- Notion;
- Linear;
- GitHub;
- Jira;
- aplicações SaaS de alta produtividade.

A interface deve transmitir sensação de:

- organização;
- controle;
- foco;
- evolução;
- clareza.

O usuário nunca deve sentir que a tela está "lotada".

---

# 3. Princípios

Todo Layout deverá seguir os seguintes princípios.

## Hierarquia Visual

O usuário deve identificar rapidamente:

- onde está;
- o que é mais importante;
- quais ações pode executar.

---

## Consistência

Todas as páginas devem compartilhar a mesma estrutura.

---

## Escalabilidade

Novos módulos devem reutilizar o Layout existente.

---

## Flexibilidade

O conteúdo pode crescer sem quebrar a estrutura.

---

## Responsividade

A experiência deve permanecer consistente em diferentes resoluções.

---

# 4. Estrutura Geral

O Layout oficial será composto pelas seguintes áreas.

```text
Application

├── Sidebar
├── TopBar
├── Workspace
├── Right Panel (futuro)
├── Dialog Layer
├── Notification Layer
└── Overlay Layer
```

Cada área possui responsabilidades próprias.

---

# 5. Layout Principal

A estrutura padrão será:

```text
+------------------------------------------------------+
|                     TopBar                           |
+----------+-------------------------------------------+
|          |                                           |
| Sidebar  |             Workspace                     |
|          |                                           |
|          |                                           |
|          |                                           |
+----------+-------------------------------------------+
```

A Sidebar permanece fixa.

A TopBar permanece fixa.

O Workspace é a única área com rolagem principal.

---

# 6. Sidebar

A Sidebar representa a navegação principal.

Responsabilidades:

- módulos;
- navegação;
- perfil;
- progresso do personagem;
- acesso rápido;
- configurações.

Nunca deve conter:

- formulários;
- dashboards;
- tabelas;
- conteúdo principal.

A largura deve permanecer constante durante a navegação.

---

# 7. TopBar

A TopBar fornece informações globais da aplicação.

Elementos previstos:

- título da página;
- breadcrumb;
- busca global;
- notificações;
- perfil do usuário;
- seletor de organização (futuro);
- ações rápidas.

Fluxo:

```text
TopBar

↓

Contexto

↓

Ações
```

A TopBar nunca substitui a navegação principal.

---

# 8. Workspace

O Workspace representa a principal área útil da aplicação.

Toda funcionalidade do módulo é exibida aqui.

Exemplos:

- Dashboard;
- Workout;
- Habits;
- Reading;
- Therapy;
- AI Mentor;
- Reports.

Cada página controla apenas seu conteúdo interno.

O Workspace nunca altera a estrutura do Layout.

---

# 9. Grid System

Toda a interface utilizará um Grid consistente.

Estrutura conceitual:

```text
Container

↓

Grid

↓

Rows

↓

Columns

↓

Components
```

O Grid deve permitir:

- alinhamento consistente;
- espaçamento uniforme;
- expansão controlada;
- reutilização entre páginas.

Nenhum componente deve utilizar posicionamento absoluto sem necessidade.

---

# 10. Responsabilidades do Layout

O Layout possui apenas responsabilidades estruturais.

Ele organiza:

- Sidebar;
- TopBar;
- Workspace;
- Dialogs;
- Overlays;
- Notifications.

O Layout nunca:

- consulta APIs;
- executa Use Cases;
- realiza autenticação;
- implementa regras de negócio;
- manipula DTOs.

Sua única responsabilidade é organizar visualmente os componentes da interface.

Essa separação garante uma arquitetura limpa, reutilizável e preparada para a evolução futura do Frontend do LifeOS, independentemente da tecnologia utilizada.