# CHARTS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Gráficos  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Design System, UI Architecture, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial de gráficos do LifeOS.

Seu objetivo é padronizar toda representação visual de dados da plataforma, permitindo que informações complexas sejam compreendidas rapidamente pelo usuário.

Os gráficos deverão:

- facilitar análise;
- apresentar tendências;
- destacar evolução;
- apoiar decisões;
- complementar dashboards.

Os gráficos nunca substituem indicadores principais (KPIs).

---

# 2. Filosofia

O objetivo de um gráfico não é impressionar.

O objetivo é responder perguntas.

Todo gráfico deve permitir que o usuário compreenda rapidamente:

- o que mudou;
- como evoluiu;
- qual tendência existe;
- onde existe um problema;
- qual ação deve ser tomada.

A simplicidade deve prevalecer sobre efeitos visuais.

---

# 3. Princípios

Todo gráfico deverá seguir os seguintes princípios.

## Clareza

A mensagem deve ser compreendida em poucos segundos.

---

## Simplicidade

Eliminar elementos decorativos desnecessários.

---

## Consistência

Todos os gráficos utilizam o mesmo padrão visual.

---

## Comparabilidade

Os dados devem facilitar comparação.

---

## Legibilidade

Os elementos devem permanecer legíveis em qualquer resolução.

---

# 4. Arquitetura

Fluxo oficial:

```text
Use Case

↓

Response DTO

↓

Chart ViewModel

↓

Chart Component

↓

Render
```

O gráfico nunca consulta diretamente:

- banco;
- Repository;
- Services.

---

# 5. Estrutura Oficial

Todo gráfico deverá possuir estrutura semelhante.

```text
Title

↓

Subtitle

↓

Chart

↓

Legend

↓

Summary

↓

Actions
```

Cada seção possui responsabilidade específica.

---

# 6. Tipos de Gráficos

Tipos oficiais.

```text
Line Chart

Bar Chart

Area Chart

Pie Chart

Donut Chart

Radar Chart

Heatmap

Scatter Plot

Timeline

Progress Chart
```

Cada tipo possui finalidade específica.

---

# 7. Line Chart

Utilizado para evolução ao longo do tempo.

Exemplos:

- XP diário;
- peso corporal;
- horas de sono;
- páginas lidas;
- frequência de exercícios.

Nunca utilizar para comparação simples entre categorias.

---

# 8. Bar Chart

Utilizado para comparação entre categorias.

Exemplos:

- treinos por modalidade;
- livros por categoria;
- hábitos concluídos;
- sessões de terapia;
- metas atingidas.

As barras devem seguir ordenação lógica.

---

# 9. Area Chart

Utilizado para evolução acumulada.

Exemplos:

- XP acumulado;
- tempo total de leitura;
- quilômetros percorridos;
- horas estudadas.

A área reforça percepção de crescimento.

---

# 10. Pie Chart

Utilizado apenas para composição percentual.

Exemplos:

```text
Tempo

↓

Leitura

Treino

Sono

Lazer
```

Nunca utilizar Pie Charts para séries temporais.

Evitar utilizar quando existirem muitas categorias.

---

# 11. Donut Chart

Representa progresso.

Exemplos:

```text
Meta Semanal

75%
```

Outro exemplo:

```text
XP

68%
```

Ideal para metas individuais.

---

# 12. Radar Chart

Utilizado para múltiplos indicadores.

Exemplo:

```text
Inteligências Múltiplas

↓

Linguística

Lógica

Espacial

Musical

Corporal

Interpessoal

Intrapessoal

Naturalista
```

Permite identificar equilíbrio entre dimensões.

---

# 13. Heatmap

Representa intensidade.

Exemplos:

- hábitos por dia;
- frequência de treino;
- produtividade;
- leitura.

Inspirado no GitHub Contributions.

---

# 14. Scatter Plot

Representa correlação.

Exemplos:

```text
Sono

↓

Performance
```

Outro exemplo:

```text
Treino

↓

Humor
```

Utilizar apenas quando existir relação entre duas variáveis.

---

# 15. Timeline

Representa eventos cronológicos.

Exemplos:

- conquistas;
- evolução;
- sessões;
- marcos importantes.

A Timeline complementa os Dashboards.

---

# 16. Progress Charts

Representam evolução de metas.

Exemplos:

```text
Objetivo

↓

Progresso

↓

Conclusão
```

Devem utilizar indicadores simples e intuitivos.

---

# 17. Atualização

Os gráficos devem refletir sempre o estado mais recente.

Fluxo:

```text
Use Case

↓

Updated DTO

↓

Chart ViewModel

↓

Chart

↓

Render
```

Atualizar apenas os dados necessários.

---

# 18. Interatividade

Os gráficos poderão oferecer interações.

Exemplos:

- Tooltip;
- Zoom;
- Seleção;
- Drill Down;
- Hover;
- Destaque de série.

A interação nunca deve ocultar informações essenciais.

---

# 19. Responsividade

Os gráficos devem adaptar-se automaticamente.

Objetivos:

- preservar legibilidade;
- reorganizar legendas;
- reduzir elementos secundários;
- manter proporções.

Nunca comprometer a interpretação dos dados.

---

# 20. Princípios Arquiteturais

Todo gráfico do LifeOS deverá ser:

- orientado à informação;
- altamente legível;
- consistente;
- reutilizável;
- desacoplado;
- responsivo;
- compatível com o Design System;
- alinhado ao Theme;
- integrado aos Use Cases;
- independente da tecnologia utilizada.

Os gráficos representam um dos principais mecanismos de análise visual do LifeOS e devem transformar dados em conhecimento, permitindo que o usuário compreenda sua evolução e tome decisões de forma rápida, intuitiva e consistente em toda a plataforma.