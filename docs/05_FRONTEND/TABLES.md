# TABLES

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Tabelas  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Design System, UI Architecture, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial das tabelas do LifeOS.

Seu objetivo é estabelecer um padrão único para apresentação de dados tabulares, garantindo:

- consistência visual;
- alta legibilidade;
- excelente experiência do usuário;
- reutilização;
- escalabilidade;
- independência da tecnologia.

Toda tabela utilizada na plataforma deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

As tabelas existem para facilitar análise de dados.

Elas devem responder rapidamente às perguntas:

- O que existe?
- O que mudou?
- O que merece atenção?
- Como localizar uma informação?

A tabela nunca deve ser utilizada quando outra visualização for mais adequada.

---

# 3. Princípios

Toda tabela deverá seguir os seguintes princípios.

## Clareza

Cada coluna possui propósito claro.

---

## Simplicidade

Mostrar apenas informações relevantes.

---

## Consistência

Todas as tabelas utilizam o mesmo padrão visual.

---

## Escalabilidade

A estrutura suporta milhares de registros.

---

## Acessibilidade

Toda informação deve permanecer legível.

---

# 4. Arquitetura

Fluxo oficial:

```text
Use Case

↓

Response DTO

↓

Table ViewModel

↓

Table Component

↓

Render
```

A tabela nunca consulta diretamente:

- banco;
- Repository;
- ORM.

---

# 5. Estrutura Oficial

Toda tabela deverá possuir a seguinte estrutura.

```text
Toolbar

↓

Filters

↓

Table

↓

Pagination

↓

Summary
```

Cada seção possui responsabilidade específica.

---

# 6. Cabeçalho

O cabeçalho apresenta:

- título;
- descrição;
- quantidade de registros;
- ações rápidas.

Exemplo:

```text
Treinos

245 registros
```

---

# 7. Colunas

Cada coluna representa um único atributo.

Exemplo:

```text
Data

Tipo

Duração

Status

XP

Ações
```

Nunca agrupar informações distintas na mesma coluna.

---

# 8. Linhas

Cada linha representa um único registro.

Exemplo:

```text
Workout

↓

Uma linha
```

O usuário deve compreender imediatamente qual objeto está sendo exibido.

---

# 9. Toolbar

A Toolbar concentra ações relacionadas à tabela.

Exemplos:

```text
Novo

Exportar

Atualizar

Pesquisar

Filtros
```

Nunca inserir ações específicas de uma linha na Toolbar.

---

# 10. Paginação

Toda tabela deverá suportar paginação.

Padrão:

```text
10

20

50

100 registros
```

Também apresentar:

- página atual;
- total de páginas;
- quantidade de registros.

---

# 11. Ordenação

As colunas poderão permitir ordenação.

Exemplo:

```text
Data ↑

Nome ↓

XP ↑
```

A ordenação deve ser:

- previsível;
- consistente;
- documentada.

---

# 12. Filtros

Filtros reduzem a quantidade de registros exibidos.

Exemplos:

```text
Status

Categoria

Data

Tipo

Usuário
```

Os filtros pertencem ao contexto da tabela.

---

# 13. Pesquisa

Toda tabela poderá oferecer pesquisa textual.

Fluxo:

```text
Search

↓

ViewModel

↓

DTO

↓

Table
```

A pesquisa deve funcionar em conjunto com:

- filtros;
- ordenação;
- paginação.

---

# 14. Seleção

As tabelas poderão permitir seleção.

Tipos:

```text
Seleção única

Seleção múltipla
```

As ações em lote devem utilizar essa seleção.

---

# 15. Ações por Linha

Cada linha poderá apresentar ações.

Exemplos:

```text
Visualizar

Editar

Excluir

Duplicar
```

As ações devem aparecer de forma consistente em todas as tabelas.

---

# 16. Estados da Tabela

Toda tabela deverá suportar estados oficiais.

```text
Loading

Ready

Empty

Error

Filtered

No Results
```

Cada estado possui representação visual específica.

---

# 17. Empty State

Quando não houver registros:

```text
Nenhum treino encontrado.

↓

Criar primeiro treino.
```

O Empty State deve incentivar a próxima ação do usuário.

---

# 18. Responsividade

Em resoluções menores:

- ocultar colunas secundárias;
- reorganizar informações;
- priorizar leitura;
- manter ações acessíveis.

Nunca reduzir a legibilidade.

---

# 19. Atualização

Após alterações:

```text
Use Case

↓

Updated DTO

↓

Table ViewModel

↓

Render
```

Sempre atualizar apenas os registros necessários.

Evitar recarregamentos completos da página.

---

# 20. Princípios Arquiteturais

Toda tabela do LifeOS deverá ser:

- altamente legível;
- consistente;
- reutilizável;
- desacoplada;
- paginável;
- filtrável;
- ordenável;
- compatível com o Design System;
- alinhada ao Theme;
- independente da tecnologia utilizada.

As tabelas representam o principal mecanismo de visualização de dados estruturados do LifeOS e devem proporcionar uma experiência eficiente para consulta, análise e gerenciamento de informações, preservando a simplicidade da interface e o desacoplamento entre apresentação e lógica de negócio.