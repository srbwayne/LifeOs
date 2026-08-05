# Capability Map

> Documento oficial de organização das Capabilities do LifeOS.

Versão: 1.0

---

# 1. Objetivo

Este documento define o mapa oficial de Capabilities do LifeOS.

Uma Capability representa uma unidade funcional de alto nível responsável por um domínio específico do negócio.

Cada Capability possui:

- responsabilidades bem definidas;
- fronteiras arquiteturais;
- regras de negócio próprias;
- eventos consumidos;
- eventos produzidos;
- integração com outras Capabilities.

Este documento é a principal referência para organização funcional do sistema.

---

# 2. O que é uma Capability?

Uma Capability representa uma capacidade de negócio da plataforma.

Ela não representa uma tela.

Ela não representa uma API.

Ela não representa uma tabela.

Ela representa um conjunto coeso de responsabilidades relacionadas a um único domínio.

Cada Capability deverá possuir:

- responsabilidade única;
- baixo acoplamento;
- alta coesão;
- autonomia funcional;
- comunicação baseada em eventos.

---

# 3. Princípios

Toda Capability deverá seguir os princípios abaixo.

## Single Responsibility

Uma Capability deve possuir apenas uma responsabilidade principal.

---

## Ownership

Cada dado deverá possuir um único proprietário.

Não poderá existir duplicação de responsabilidade.

---

## Comunicação

As Capabilities deverão comunicar-se preferencialmente através de eventos.

Dependências diretas deverão ser evitadas.

---

## Independência

Cada Capability deverá evoluir de forma independente.

---

## Testabilidade

Cada Capability deverá possuir testes próprios.

---

## Rastreabilidade

Toda Capability deverá estar vinculada a:

- Product Vision
- Feature Catalog
- PRD
- Código
- Testes

---

# 4. Capability Map

```text
                           +----------------------+
                           |   Authentication     |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |      Character       |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |     Game Engine      |
                           +----------+-----------+
                                      |
          +---------------------------+---------------------------+
          |                           |                           |
          v                           v                           v
     +---------+                +-----------+              +------------+
     | Health  |                | Workout   |              |  Habits    |
     +---------+                +-----------+              +------------+
          |                           |                           |
          +---------------------------+---------------------------+
                                      |
                                      v
                           +----------------------+
                           |      Analytics       |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           | Artificial Intelligence |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |      Dashboard       |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |       Reports        |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |   Administration     |
                           +----------------------+
```

---

# 5. Capabilities Oficiais

Atualmente o LifeOS possui as seguintes Capabilities.

| Código | Capability | Responsabilidade |
|---------|------------|------------------|
| AUTH | Authentication | Identidade, autenticação e autorização |
| CHAR | Character | Representação do Player |
| HEALTH | Health | Saúde física e fisiológica |
| WORK | Workout | Treinos físicos |
| READ | Reading | Leitura |
| THER | Therapy | Terapia |
| HAB | Habits | Hábitos |
| GAME | Game Engine | Evolução do Character |
| DASH | Dashboard | Visualização consolidada |
| ANLT | Analytics | Indicadores e métricas |
| AI | Artificial Intelligence | Recomendações inteligentes |
| REPORT | Reports | Relatórios |
| ADMIN | Administration | Administração da plataforma |

---

# 6. Responsabilidades das Capabilities

## AUTH

Responsável por:

- autenticação;
- autorização;
- sessões;
- credenciais;
- recuperação de senha.

Não poderá:

- alterar Character;
- conceder XP;
- executar regras da Game Engine.

---

## CHAR

Responsável por:

- identidade do Character;
- perfil do Character;
- representação persistente do Character;
- consultas de identidade e perfil.

Não poderá:

- calcular ou administrar XP;
- calcular ou administrar Level;
- administrar atributos evolutivos;
- administrar Skills, Classes, Quests ou Rewards;
- calcular progressão ou evolução;
- executar regras de balanceamento.

---

## HEALTH

Responsável por registrar:

- sono;
- peso;
- frequência cardíaca;
- VFC;
- indicadores fisiológicos.

Produz eventos.

Não altera o Character.

---

## WORK

Responsável por:

- musculação;
- corrida;
- pilates;
- exercícios.

Produz eventos.

Não altera XP.

---

## READ

Responsável pelo acompanhamento de leitura.

Produz eventos.

---

## THER

Responsável pelo registro das sessões terapêuticas.

Produz eventos.

---

## HAB

Responsável pelos hábitos.

Produz eventos.

---

## GAME

Responsável por toda evolução e por todo balanceamento do Character.

É a única Capability autorizada a alterar:

- XP;
- Level;
- Attributes;
- Skills;
- Classes;
- Rewards;
- Inventário;
- Progressão;
- Evolução;
- Balanceamento.

---

## DASH

Responsável apenas pela apresentação consolidada.

Nunca altera dados.

---

## ANLT

Responsável por:

- indicadores;
- métricas;
- tendências;
- correlações;
- insights.

Nunca altera dados.

---

## AI

Responsável por:

- recomendações;
- coaching;
- mentoria;
- planejamento.

Nunca altera dados.

---

## REPORT

Responsável por consolidar informações para exportação.

Nunca altera dados.

---

## ADMIN

Responsável por:

- usuários;
- configurações;
- auditoria;
- monitoramento;
- administração.

Nunca participa da evolução do Character.

---

# 7. Fluxo Oficial de Evolução

Nenhuma Capability poderá alterar diretamente o Character.

O fluxo oficial é:

```text
Capability

↓

Evento de Domínio

↓

Game Engine

↓

Validação

↓

Aplicação das Regras

↓

Atualização do Character

↓

Persistência

↓

Eventos
```

---

# 8. Fluxo Oficial de Dados

```text
Health

Workout

Reading

Therapy

Habits

↓

Eventos

↓

Game Engine

↓

Character

↓

Analytics

↓

Artificial Intelligence

↓

Dashboard

↓

Reports
```

---

# 9. Ownership

Cada Capability possui propriedade exclusiva sobre seus dados.

| Capability | Dono dos Dados |
|------------|----------------|
| AUTH | Usuários e autenticação |
| CHAR | Character |
| HEALTH | Indicadores de saúde |
| WORK | Treinos |
| READ | Leituras |
| THER | Sessões |
| HAB | Hábitos |
| GAME | Evolução |
| ANLT | Indicadores |
| AI | Recomendações |
| DASH | Nenhum (consulta) |
| REPORT | Nenhum (consulta) |
| ADMIN | Configurações |

Nenhuma Capability poderá modificar dados pertencentes a outra Capability sem utilizar os mecanismos oficiais da arquitetura.

---

# 10. Anti-Patterns

São proibidos:

- lógica de Game Engine em outras Capabilities;
- consultas cruzadas sem necessidade;
- acesso direto ao banco entre módulos;
- duplicação de regras de negócio;
- dependências circulares;
- acoplamento entre interfaces.

---

# 11. Roadmap

Novas Capabilities somente poderão ser adicionadas quando:

- existir necessidade de negócio;
- houver responsabilidade claramente definida;
- não existir sobreposição com Capabilities existentes;
- a arquitetura permanecer desacoplada.

Toda nova Capability deverá possuir:

- Features;
- Requisitos Funcionais;
- Modelo de Dados;
- APIs;
- Testes;
- Documentação.
