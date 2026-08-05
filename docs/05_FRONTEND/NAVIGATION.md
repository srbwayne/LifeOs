# NAVIGATION

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Navegação  
**Camadas Relacionadas:** Presentation  
**Arquiteturas Relacionadas:** UI Architecture, Design System, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial de navegação do LifeOS.

Seu objetivo é estabelecer como os usuários percorrem a aplicação, garantindo uma experiência consistente, intuitiva e escalável.

A navegação deverá:

- reduzir a carga cognitiva;
- minimizar a quantidade de cliques;
- manter o contexto do usuário;
- facilitar descoberta de funcionalidades;
- permanecer consistente em todos os módulos.

Toda navegação do sistema deverá seguir as diretrizes deste documento.

---

# 2. Filosofia

O LifeOS deve se comportar como um sistema operacional pessoal.

O usuário nunca deve sentir que está "trocando de sistema" ao navegar.

A navegação deve transmitir:

- continuidade;
- previsibilidade;
- fluidez;
- foco;
- organização.

A troca entre módulos deve parecer instantânea.

---

# 3. Princípios

Toda navegação deverá seguir os seguintes princípios.

## Consistência

O mesmo caminho sempre leva ao mesmo resultado.

---

## Contexto

O usuário deve saber continuamente:

- onde está;
- como chegou ali;
- para onde pode ir.

---

## Descoberta

Novas funcionalidades devem ser facilmente encontradas.

---

## Eficiência

As ações mais frequentes devem exigir o menor número possível de interações.

---

## Escalabilidade

Novos módulos devem ser adicionados sem alterar a estrutura principal de navegação.

---

# 4. Arquitetura da Navegação

A navegação é organizada em níveis.

```text
Application

↓

Module

↓

Page

↓

Section

↓

Component
```

Cada nível representa um contexto específico.

A navegação nunca deve "pular" níveis de forma inesperada.

---

# 5. Estrutura Principal

A navegação principal será realizada através da Sidebar.

Estrutura:

```text
Dashboard

Character

Workout

Habits

Reading

Therapy

AI Mentor

Reports

Settings

Administration
```

Cada item representa um módulo da aplicação.

Não devem existir menus duplicados.

---

# 6. Sidebar

A Sidebar é o principal mecanismo de navegação.

Responsabilidades:

- acesso aos módulos;
- identificação visual do módulo atual;
- acesso rápido;
- agrupamento lógico.

Cada item deverá possuir:

- ícone;
- título;
- estado ativo;
- tooltip (quando necessário).

O estado ativo deve permanecer claramente identificado.

---

# 7. Top Navigation

A TopBar complementa a Sidebar.

Ela apresenta:

- título da página;
- breadcrumb;
- pesquisa global;
- notificações;
- perfil;
- ações rápidas.

A TopBar não substitui a navegação principal.

Ela complementa o contexto da página atual.

---

# 8. Breadcrumb

Todas as páginas internas deverão apresentar Breadcrumb.

Exemplo:

```text
Dashboard

↓

Workout

↓

Treino de Corrida

↓

Detalhes
```

Outro exemplo:

```text
Settings

↓

Notifications

↓

Email Preferences
```

O Breadcrumb permite retornar rapidamente aos níveis superiores.

---

# 9. Navegação Hierárquica

A estrutura segue hierarquia clara.

```text
Application

↓

Module

↓

Page

↓

Section

↓

Dialog
```

Exemplo:

```text
Workout

↓

Weekly Plan

↓

Workout Details

↓

Edit Dialog
```

Cada nível possui apenas um responsável.

---

# 10. Fluxo Oficial de Navegação

Toda navegação deverá seguir o fluxo abaixo.

```text
User Action

↓

Navigation Event

↓

Route Resolution

↓

Page Loading

↓

Use Case

↓

DTO

↓

Render

↓

Ready
```

Caso ocorra erro:

```text
Navigation

↓

Page Resolution

↓

Failure

↓

Error Page

↓

Retry
```

A navegação nunca deve:

- perder o contexto do usuário;
- gerar telas em branco;
- apresentar estados inconsistentes;
- interromper o fluxo da aplicação.

Toda transição entre páginas deve preservar a consistência visual, a previsibilidade da interface e a identidade arquitetural do LifeOS.

---

# 11. Organização dos Módulos

Os módulos deverão seguir uma ordem lógica baseada na jornada do usuário.

Estrutura sugerida:

```text
Home

↓

Dashboard

↓

Character

↓

Habits

↓

Workout

↓

Reading

↓

Therapy

↓

AI Mentor

↓

Reports

↓

Settings
```

Módulos administrativos permanecem separados da experiência principal.

---

# 12. Navegação Contextual

Cada módulo poderá oferecer navegação interna própria.

Exemplo:

```text
Workout

↓

Today's Workout

↓

History

↓

Statistics

↓

Goals
```

Essa navegação não altera a Sidebar.

Ela permanece restrita ao contexto do módulo.

---

# 13. Navegação por Cartões

Os Dashboards utilizarão Cards como pontos de entrada para funcionalidades.

Exemplo:

```text
Workout Card

↓

Click

↓

Workout Dashboard
```

Outro exemplo:

```text
Reading Progress

↓

Click

↓

Books Module
```

Os Cards devem complementar a navegação, nunca substituí-la.

---

# 14. Pesquisa Global

A aplicação deverá oferecer uma pesquisa global.

A pesquisa poderá localizar:

- páginas;
- hábitos;
- livros;
- treinos;
- metas;
- quests;
- configurações.

Fluxo:

```text
Search

↓

Suggestions

↓

Selection

↓

Navigation
```

Os resultados devem respeitar autenticação e autorização.

---

# 15. Quick Actions

A interface deverá oferecer atalhos para ações frequentes.

Exemplos:

```text
Novo Hábito

Novo Treino

Novo Livro

Nova Sessão

Nova Meta
```

Essas ações poderão estar disponíveis:

- na TopBar;
- em FABs (quando aplicável);
- no Dashboard.

---

# 16. Deep Links

A arquitetura deverá permitir acesso direto às páginas.

Exemplos:

```text
/workouts

/workouts/{id}

/books/{id}

/habits/{id}
```

Cada rota deve restaurar completamente o estado necessário da página.

---

# 17. Estados da Navegação

Toda navegação poderá apresentar estados distintos.

```text
Loading

Ready

Empty

Error

Unauthorized

Not Found
```

Cada estado deve possuir interface própria e consistente com o Design System.

---

# 18. Navegação por Notificações

Notificações poderão direcionar o usuário para páginas específicas.

Fluxo:

```text
Notification

↓

Click

↓

Navigate

↓

Target Page
```

Exemplo:

```text
Meta concluída

↓

Character

↓

Achievement Details
```

---

# 19. Navegação Assistida por IA

O AI Mentor poderá sugerir navegação contextual.

Exemplos:

```text
Você não treina há 5 dias.

↓

Abrir Workout
```

```text
Seu livro está parado há duas semanas.

↓

Abrir Reading
```

A IA apenas sugere.

A navegação continua sob controle do usuário.

---

# 20. Princípios Arquiteturais

Toda navegação do LifeOS deverá obedecer aos seguintes princípios:

- previsível;
- consistente;
- contextual;
- acessível;
- desacoplada da lógica de negócio;
- independente da tecnologia;
- reutilizável;
- escalável;
- orientada ao usuário;
- alinhada ao Design System.

A navegação constitui um dos pilares da experiência do LifeOS e deverá evoluir preservando sempre a simplicidade, a clareza e a sensação de continuidade entre todos os módulos da plataforma.