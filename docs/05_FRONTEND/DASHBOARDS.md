# DASHBOARDS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Dashboards  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Design System, UI Architecture, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial dos Dashboards do LifeOS.

Seu objetivo é estabelecer padrões para apresentação de informações estratégicas, operacionais e analíticas, proporcionando uma visão clara da evolução do usuário e do funcionamento da plataforma.

Os Dashboards deverão:

- apresentar indicadores;
- facilitar tomada de decisão;
- incentivar o engajamento;
- destacar progresso;
- reduzir carga cognitiva.

Todo Dashboard deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

O Dashboard representa o centro de comando do LifeOS.

Ele não deve apenas mostrar dados.

Ele deve responder continuamente:

- Como estou hoje?
- Estou evoluindo?
- O que merece minha atenção?
- Qual é meu próximo objetivo?

A interface deve motivar o usuário sem gerar sobrecarga de informações.

---

# 3. Princípios

Todo Dashboard deverá seguir os seguintes princípios.

## Clareza

Os indicadores mais importantes devem aparecer primeiro.

---

## Hierarquia

Toda informação deve possuir prioridade visual.

---

## Objetividade

Mostrar apenas informações relevantes.

---

## Ação

Sempre que possível um indicador deve permitir navegar para sua origem.

---

## Atualização

As informações devem refletir o estado mais recente disponível.

---

# 4. Arquitetura

Fluxo oficial:

```text
Use Case

↓

Response DTO

↓

Dashboard ViewModel

↓

Widgets

↓

Layout

↓

Render
```

O Dashboard nunca consulta diretamente:

- banco;
- repositories;
- serviços externos.

---

# 5. Estrutura Oficial

Todo Dashboard deverá seguir uma organização semelhante.

```text
Header

↓

KPIs

↓

Progress

↓

Widgets

↓

Charts

↓

Lists

↓

Recommendations
```

Cada seção possui responsabilidade específica.

---

# 6. Dashboard Principal

O Dashboard inicial representa a visão geral do LifeOS.

Elementos previstos:

- Status do personagem;
- XP;
- Nível;
- Evolução semanal;
- Hábitos;
- Treinos;
- Leitura;
- Terapia;
- IA;
- Próximos objetivos.

Essa página representa a Home da aplicação.

---

# 7. Dashboards por Módulo

Cada módulo poderá possuir Dashboard próprio.

Exemplos:

```text
Workout Dashboard

Habit Dashboard

Reading Dashboard

Therapy Dashboard

Character Dashboard

AI Dashboard
```

Todos seguem a mesma arquitetura visual.

---

# 8. KPIs

Os principais indicadores deverão aparecer no topo.

Exemplos:

```text
XP Total

Nível Atual

Sequência de Hábitos

Livros Lidos

Treinos na Semana

Dias Consecutivos

Tempo de Leitura
```

Os KPIs devem ser simples e facilmente compreendidos.

---

# 9. Widgets

Os Dashboards serão compostos por Widgets reutilizáveis.

Exemplos:

```text
XP Widget

Goal Widget

Workout Widget

Habit Widget

Mood Widget

AI Insight Widget

Weekly Summary

Calendar Widget
```

Cada Widget possui responsabilidade única.

---

# 10. Cards

Cards representam agrupamentos visuais de informações.

Exemplos:

```text
Workout Card

Reading Card

Habit Card

Quest Card

Achievement Card
```

Todos devem seguir o Design System oficial.

---

# 11. Progressão

A evolução do usuário deve ser constantemente apresentada.

Exemplos:

```text
XP

↓

Nível

↓

Próximo Nível
```

Outro exemplo:

```text
Meta

↓

65%

↓

Progresso
```

Toda progressão deve ser facilmente identificável.

---

# 12. Indicadores

Os indicadores devem responder rapidamente ao estado atual do usuário.

Exemplos:

- hábitos concluídos;
- treinos pendentes;
- livros em andamento;
- sessões realizadas;
- metas concluídas.

Sempre utilizar representação visual consistente.

---

# 13. Gráficos

Os gráficos complementam os KPIs.

Nunca substituem indicadores principais.

Exemplos:

```text
Linha

Barra

Área

Radar

Pizza

Heatmap
```

Cada gráfico deve possuir objetivo claro.

---

# 14. Resumo Semanal

Todo Dashboard deverá apresentar um resumo da semana.

Exemplo:

```text
Treinos

Leitura

Hábitos

Humor

XP

Missões
```

Esse resumo aproxima o usuário da sua evolução contínua.

---

# 15. Recomendações

Os Dashboards poderão apresentar recomendações.

Exemplos:

```text
Continue sua leitura.

↓

Registrar treino.

↓

Dormir mais cedo.

↓

Revisar metas.
```

As recomendações podem ser produzidas pela IA.

---

# 16. Alertas

Alertas importantes devem aparecer em área específica.

Exemplos:

- hábito esquecido;
- treino atrasado;
- backup pendente;
- sessão não realizada.

Alertas não devem competir visualmente com KPIs.

---

# 17. Navegação

Todo Widget poderá servir como ponto de entrada.

Fluxo:

```text
Widget

↓

Click

↓

Module

↓

Details
```

O Dashboard atua como central de navegação da aplicação.

---

# 18. Personalização

O usuário poderá personalizar seu Dashboard.

Exemplos futuros:

- ordem dos Widgets;
- Widgets favoritos;
- ocultar seções;
- tamanho dos Cards;
- tema visual.

A personalização nunca altera o Design System.

---

# 19. Atualização

Os Dashboards deverão ser atualizados após mudanças relevantes.

Fluxo:

```text
Use Case

↓

DTO Atualizado

↓

ViewModel

↓

Widgets

↓

Render
```

Evitar recarregamentos completos quando apenas um Widget precisar ser atualizado.

---

# 20. Princípios Arquiteturais

Todo Dashboard do LifeOS deverá ser:

- orientado por indicadores;
- altamente visual;
- reutilizável;
- desacoplado;
- responsivo;
- compatível com o Design System;
- alinhado ao Theme;
- composto por Widgets reutilizáveis;
- integrado aos Use Cases;
- independente da tecnologia utilizada.

Os Dashboards constituem o principal ponto de acompanhamento da evolução do usuário dentro do LifeOS e devem transformar dados em informações claras, acionáveis e motivadoras, fortalecendo a experiência de uso e a proposta da plataforma como um sistema operacional para desenvolvimento pessoal.