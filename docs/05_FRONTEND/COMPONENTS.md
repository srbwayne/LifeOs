# COMPONENTS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Componentes  
**Camadas Relacionadas:** Presentation  
**Arquiteturas Relacionadas:** Design System, UI Architecture, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial de componentes do LifeOS.

Seu objetivo é estabelecer um modelo único para construção, organização e reutilização de componentes da interface, garantindo:

- consistência visual;
- reutilização;
- baixo acoplamento;
- alta coesão;
- facilidade de manutenção;
- independência da tecnologia utilizada.

Todo componente visual deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

Todo componente deve representar uma única responsabilidade.

Um componente não é apenas um trecho reutilizável de interface.

Ele representa uma unidade arquitetural da camada de Presentation.

Componentes devem ser:

- pequenos;
- reutilizáveis;
- previsíveis;
- independentes;
- facilmente testáveis.

---

# 3. Princípios

Toda implementação deverá seguir os seguintes princípios.

## Single Responsibility

Cada componente resolve apenas um problema.

---

## Reutilização

O mesmo componente nunca deve ser implementado duas vezes.

---

## Composição

Interfaces complexas devem surgir da composição de componentes menores.

---

## Independência

Componentes nunca conhecem:

- banco;
- SQL;
- ORM;
- Repository;
- Entities.

---

## Imutabilidade

Sempre que possível, componentes devem ser tratados como funções puras da interface.

---

# 4. Arquitetura dos Componentes

Os componentes seguem uma hierarquia.

```text
Design Tokens

↓

Primitive Components

↓

Composite Components

↓

Business Components

↓

Pages
```

Cada nível depende apenas do imediatamente inferior.

---

# 5. Primitive Components

São os menores componentes reutilizáveis.

Exemplos:

```text
Button

Text

Input

Textarea

Checkbox

Radio

Switch

Avatar

Badge

Icon

Divider

Spinner

ProgressBar
```

Características:

- extremamente reutilizáveis;
- independentes do domínio;
- não conhecem DTOs;
- não possuem regras de negócio.

---

# 6. Composite Components

São construídos a partir dos Primitive Components.

Exemplos:

```text
Search Box

Search Bar

Toolbar

Pagination

Filter Panel

Modal Header

Dialog Footer

Navigation Item

Notification Item

Card Header
```

Esses componentes organizam elementos menores.

Ainda não conhecem regras de negócio.

---

# 7. Business Components

Representam componentes específicos do domínio do LifeOS.

Exemplos:

```text
Workout Card

Habit Card

Book Card

Quest Card

Achievement Card

Character Card

Weekly Progress

Mood Card

Health Summary

AI Insight Card
```

Esses componentes recebem apenas DTOs preparados pelos Use Cases.

Nunca acessam diretamente a camada Application.

---

# 8. Organização

Estrutura sugerida:

```text
components/

├── primitives/
│
├── composite/
│
├── business/
│
├── layouts/
│
├── dialogs/
│
├── navigation/
│
├── tables/
│
├── forms/
│
├── charts/
│
├── dashboard/
│
└── feedback/
```

Cada diretório representa um contexto funcional.

---

# 9. Responsabilidades

Cada tipo de componente possui responsabilidades específicas.

## Primitive

- renderização;
- aparência;
- estados visuais.

---

## Composite

- composição;
- layout interno;
- interação simples.

---

## Business

- apresentação de informações do domínio;
- exibição de DTOs;
- interação do usuário.

---

Nenhum componente implementa regras de negócio.

---

# 10. Fluxo Oficial

Todo componente segue o fluxo abaixo.

```text
DTO

↓

ViewModel

↓

Component

↓

Render

↓

Interaction

↓

Event

↓

Use Case
```

O componente nunca chama diretamente:

- Repository;
- Database;
- ORM;
- Services.

Toda comunicação ocorre através da camada Application.

---

# 11. Ciclo de Vida

Todo componente possui um ciclo de vida previsível.

```text
Create

↓

Initialize

↓

Render

↓

Update

↓

Dispose
```

Durante sua existência o componente pode:

- atualizar estado visual;
- responder eventos;
- solicitar dados através do ViewModel.

Nunca altera diretamente regras de negócio.

---

# 12. Propriedades (Props)

Toda comunicação entre componentes ocorre através de propriedades explícitas.

Exemplo:

```python
WorkoutCard(

    workout=workout,

    on_edit=...,

    on_delete=...
)
```

As propriedades devem ser:

- fortemente tipadas;
- imutáveis sempre que possível;
- documentadas.

Evitar objetos genéricos.

---

# 13. Eventos

Componentes nunca executam lógica.

Eles apenas disparam eventos.

Exemplo:

```text
Button Click

↓

Event

↓

Page

↓

Use Case
```

Eventos típicos:

- click;
- change;
- submit;
- cancel;
- retry;
- refresh.

---

# 14. Estado dos Componentes

Existem dois tipos de estado.

## Estado Local

Controla apenas comportamento visual.

Exemplos:

- expandido;
- selecionado;
- foco;
- aberto;
- fechado.

---

## Estado Global

Pertence ao módulo.

Exemplos:

- usuário;
- dashboard;
- personagem;
- progresso.

Esse estado nunca pertence ao componente.

---

# 15. Componentes Controlados

Sempre que possível, componentes devem ser controlados externamente.

Fluxo:

```text
Page

↓

State

↓

Component

↓

User Action

↓

Callback

↓

State Update
```

O componente não decide sozinho seu estado.

---

# 16. Composição

Interfaces complexas devem surgir pela composição.

Exemplo:

```text
Dashboard

↓

Progress Card

↓

XP Bar

↓

Level Badge

↓

Action Buttons
```

Cada componente permanece pequeno.

---

# 17. Reutilização

Antes de criar um novo componente deve ser verificado:

- já existe componente semelhante?
- pode ser parametrizado?
- pode ser estendido?
- pertence ao Design System?

Duplicação é proibida.

---

# 18. Componentes de Negócio

Cada módulo poderá possuir componentes próprios.

Exemplo:

```text
Workout/

Habit/

Reading/

Therapy/

Character/

AI/
```

Esses componentes continuam reutilizando:

- Primitive Components;
- Composite Components.

---

# 19. Testabilidade

Todo componente deve permitir testes.

Validar:

- renderização;
- propriedades;
- callbacks;
- estados;
- acessibilidade;
- comportamento visual.

A lógica permanece testada nos Use Cases.

---

# 20. Princípios Arquiteturais

Todo componente do LifeOS deverá ser:

- pequeno;
- reutilizável;
- desacoplado;
- previsível;
- fortemente tipado;
- independente da tecnologia;
- compatível com o Design System;
- alinhado ao Theme;
- facilmente testável;
- orientado à composição.

A arquitetura de componentes constitui a base da camada de Presentation e garante que toda a interface do LifeOS evolua de maneira consistente, escalável e sustentável ao longo do crescimento da plataforma.