# PAGES

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Páginas  
**Camadas Relacionadas:** Presentation  
**Arquiteturas Relacionadas:** UI Architecture, Design System, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial das páginas do LifeOS.

Uma **Page** representa o maior elemento funcional da camada de apresentação e corresponde a um contexto completo de interação do usuário.

Seu objetivo é:

- organizar componentes;
- iniciar casos de uso;
- apresentar informações;
- controlar estados visuais;
- manter a navegação consistente.

As Pages nunca implementam regras de negócio.

---

# 2. Filosofia

Cada página representa uma experiência completa.

Ela deve responder apenas uma pergunta:

> **"Qual tarefa o usuário deseja realizar neste momento?"**

Exemplos:

- visualizar Dashboard;
- registrar treino;
- acompanhar leitura;
- consultar progresso;
- conversar com a IA.

Uma página nunca deve tentar resolver vários problemas simultaneamente.

---

# 3. Princípios

Toda Page deverá seguir os seguintes princípios.

## Responsabilidade Única

Cada página representa apenas um contexto funcional.

---

## Baixo Acoplamento

A página conhece apenas:

- ViewModels;
- DTOs;
- Components;
- Use Cases.

---

## Alta Coesão

Todos os elementos da página possuem o mesmo objetivo.

---

## Reutilização

As páginas reutilizam componentes existentes.

Nunca implementam componentes próprios quando já houver equivalente.

---

## Independência

Uma página nunca depende diretamente de outra página.

A comunicação ocorre exclusivamente através da navegação.

---

# 4. Arquitetura das Pages

Fluxo oficial:

```text
User

↓

Page

↓

Layout

↓

Business Components

↓

ViewModel

↓

Use Case

↓

DTO

↓

Render
```

A Page coordena o fluxo da interface.

Ela nunca executa regras de negócio.

---

# 5. Estrutura Oficial

Cada página deverá possuir estrutura semelhante.

```text
Page

├── Header

├── Toolbar

├── Filters

├── Content

├── Floating Actions

├── Dialogs

└── Feedback Area
```

Essa estrutura favorece consistência entre módulos.

---

# 6. Organização das Pages

Estrutura sugerida:

```text
pages/

├── dashboard/
├── character/
├── workout/
├── habits/
├── reading/
├── therapy/
├── ai/
├── reports/
├── settings/
├── profile/
└── administration/
```

Cada diretório representa um módulo da aplicação.

---

# 7. Header

Toda página deverá possuir um Header.

O Header apresenta:

- título;
- descrição;
- breadcrumb;
- ações rápidas;
- indicadores relevantes.

Exemplo:

```text
Workout

Registrar e acompanhar seus treinos
```

O Header contextualiza a tela.

---

# 8. Toolbar

A Toolbar concentra ações relacionadas à página.

Exemplos:

```text
Novo

Editar

Excluir

Exportar

Atualizar

Pesquisar
```

A Toolbar nunca contém informações de negócio.

Seu papel é apenas disponibilizar ações.

---

# 9. Área de Conteúdo

O Content representa a principal área útil da página.

Pode conter:

- Cards;
- Tabelas;
- Dashboards;
- Gráficos;
- Formulários;
- Listas;
- Calendários;
- Widgets.

Todo conteúdo deve respeitar o Layout oficial.

---

# 10. Responsabilidades

Uma Page é responsável por:

- organizar componentes;
- controlar estados visuais;
- iniciar navegação;
- iniciar Use Cases;
- apresentar DTOs;
- responder eventos do usuário.

Uma Page nunca:

- consulta banco;
- acessa Repository;
- executa SQL;
- calcula regras de negócio;
- altera Aggregates.

---

# 11. ViewModel

Toda página deverá possuir um ViewModel próprio.

Exemplo:

```text
WorkoutPage

↓

WorkoutViewModel

↓

WorkoutDTO
```

Responsabilidades do ViewModel:

- preparar dados;
- organizar informações;
- adaptar DTOs;
- facilitar renderização.

Nunca executar regras de negócio.

---

# 12. Estados da Página

Toda página deverá suportar estados bem definidos.

```text
Loading

Ready

Empty

Error

Unauthorized

Not Found
```

Cada estado possui interface específica.

Nunca apresentar telas parcialmente renderizadas.

---

# 13. Ciclo de Vida

Fluxo oficial:

```text
Open Page

↓

Initialize

↓

Load Data

↓

Render

↓

Interaction

↓

Refresh

↓

Dispose
```

A inicialização deve ser rápida.

Carregamentos demorados devem utilizar Loading States.

---

# 14. Navegação

As Pages nunca navegam diretamente entre si.

Fluxo:

```text
User Action

↓

Navigation Service

↓

Target Page
```

Isso mantém baixo acoplamento entre módulos.

---

# 15. Comunicação com Use Cases

Toda interação relevante ocorre através de Use Cases.

Fluxo:

```text
Button

↓

Page

↓

Use Case

↓

DTO

↓

Page
```

A Page nunca conhece Services internos.

---

# 16. Atualização da Interface

Após um Use Case concluir:

```text
Use Case

↓

Updated DTO

↓

ViewModel

↓

Components

↓

Render
```

Sempre atualizar a interface utilizando novos DTOs.

Nunca modificar diretamente o estado interno de Components complexos.

---

# 17. Dialogs

Dialogs pertencem ao contexto da Page.

Exemplos:

- confirmação;
- exclusão;
- edição;
- detalhes;
- seleção.

Fluxo:

```text
Page

↓

Dialog

↓

Use Case

↓

Close
```

Dialogs nunca substituem páginas completas.

---

# 18. Feedback

Toda ação deve produzir feedback visual.

Exemplos:

```text
Loading

Success

Warning

Error

Information
```

A resposta deve ocorrer imediatamente após a interação do usuário.

---

# 19. Organização Futura

Cada módulo poderá evoluir para múltiplas páginas.

Exemplo:

```text
Workout

├── Dashboard

├── History

├── Calendar

├── Statistics

├── Goals

└── Details
```

Todas reutilizam o mesmo conjunto de componentes.

---

# 20. Princípios Arquiteturais

Toda Page do LifeOS deverá ser:

- orientada a contexto;
- altamente coesa;
- desacoplada;
- reutilizável;
- previsível;
- compatível com o Design System;
- alinhada ao Theme;
- composta por Components reutilizáveis;
- integrada aos Use Cases;
- independente da tecnologia utilizada.

As Pages representam a principal unidade funcional da camada de Presentation e devem servir como ponto de orquestração da experiência do usuário, mantendo a lógica de negócio encapsulada nas camadas inferiores e garantindo uma interface consistente, escalável e sustentável para toda a plataforma LifeOS.