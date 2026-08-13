# DDD

# Domain-Driven Design

## LifeOS

**Versão:** 1.0

**Status:** Documento Oficial

**Padrão Arquitetural:** Domain-Driven Design (DDD)

---

# Objetivo

Este documento define como os princípios de Domain-Driven Design (DDD) são aplicados no LifeOS.

Seu objetivo é garantir que a arquitetura permaneça orientada ao domínio, preservando as regras de negócio independentes de tecnologias, interfaces e mecanismos de persistência.

Toda implementação deve respeitar as definições apresentadas neste documento.

---

# Motivação

O LifeOS é um produto de longo prazo.

Seu domínio tende a crescer continuamente com novos módulos, integrações e motores especializados.

Sem uma modelagem orientada ao domínio, o conhecimento do negócio tende a ficar espalhado entre telas, serviços e consultas SQL.

O DDD permite centralizar esse conhecimento em um modelo consistente, reutilizável e de fácil evolução.

---

# Objetivos

O modelo de domínio do LifeOS deve:

- representar fielmente o negócio;
- utilizar uma linguagem única;
- minimizar duplicação de regras;
- facilitar manutenção;
- facilitar testes;
- permitir evolução incremental.

---

# Linguagem Ubíqua

Todos os membros da equipe e agentes de IA deverão utilizar exatamente a linguagem definida em:

```
00_FOUNDATION/GLOSSARY.md
```

Não devem existir sinônimos para conceitos do domínio.

Exemplos:

✔ Character

✔ Player

✔ Quest

✔ Achievement

✔ Skill

✔ XP

✔ Attribute

✘ Usuário RPG

✘ Avatar XP

✘ Perfil Gamer

Esses termos não fazem parte da linguagem oficial.

---

# Estratégia de Modelagem

O LifeOS será organizado em Bounded Contexts.

Cada contexto representa um domínio de negócio independente.

---

# Bounded Contexts

```
Authentication

Character

Health

Workout

Reading

Therapy

Habits

Gamification

Analytics

AI Mentor

Reporting

Administration
```

Cada contexto possui:

- entidades próprias;
- regras próprias;
- serviços próprios;
- eventos próprios;
- persistência própria.

---

# Context Map

```text
                       LifeOS

                           │

    ┌───────────────┬───────────────┬───────────────┐

    │               │               │

 Character      Health        Workout

    │               │               │

    ├───────────────┴───────────────┤

                    │

             Gamification

                    │

            Analytics Engine

                    │

               AI Mentor
```

---

# Bounded Context — Authentication

## Responsabilidade

Gerenciar identidade.

---

## Entidades

User

Session

PasswordReset

---

## Value Objects

Email

PasswordHash

UserId

---

## Eventos

UserRegistered

UserLoggedIn

PasswordChanged

---

# Bounded Context — Character

## Responsabilidade

Representar a evolução do Player.

---

## Entidades

Character

Attribute

Title

Guild

Class

---

## Value Objects

Level

XP

CharacterId

---

## Eventos

CharacterCreated

XPGranted

LevelUp

TitleUnlocked

---

# Bounded Context — Health

## Responsabilidade

Registrar indicadores biológicos.

---

## Entidades

SleepRecord

BodyComposition

HeartRate

Recovery

---

## Eventos

SleepRegistered

RecoveryCalculated

---

# Bounded Context — Workout

## Responsabilidade

Registrar atividades físicas.

---

## Entidades

Workout

Exercise

WorkoutType

---

## Eventos

WorkoutRegistered

WorkoutCompleted

---

# Bounded Context — Reading

## Responsabilidade

Gerenciar livros da biblioteca pessoal e registrar acontecimentos históricos de leitura do usuário autenticado.

---

## Aggregate Roots

- `Book`: representa o item permanente da biblioteca e não controla sessões.
- `ReadingSession`: representa um fato histórico de leitura e referencia o livro por `BookId`.

`ReadingSession` possui identidade própria, não oferece mutabilidade pública para edição em READ-002 e calcula `pages_read` pelo intervalo inclusivo entre `start_page` e `end_page`.

---

## Value Objects

- `BookId`;
- `TotalPages`;
- `ReadingSessionId`, com representação TSID;
- `PageNumber`, inteiro imutável maior ou igual a 1.

Não existe `PageRange` Value Object. A consistência entre página inicial e final pertence ao Aggregate `ReadingSession`.

`UserId` é o contrato transversal de ownership reutilizado por READ e permanece no Shared Kernel.

---

## Repository Ports

- `IBookRepository`: inclui lookup obrigatório por `BookId` e `UserId` para preservar ownership;
- `IReadingSessionRepository`: além de `save(session)`, expõe em READ-003 a ampliação mínima owner-scoped:

```python
list_by_book_and_owner(
    book_id: BookId,
    owner_id: UserId,
) -> tuple[ReadingSession, ...]
```

O ownership faz parte do próprio contrato do Port. Não existe método de listagem por Book sem o owner.

## READ-003 — Reading Progress

`ReadingProgress` não é Aggregate Root nem Entity: não possui identidade, não é persistido e representa um resultado de domínio derivado e imutável. Seus campos são:

- `book_id`;
- `total_pages`;
- `unique_pages_read`;
- `highest_page_reached`;
- `percentage`;
- `completed`.

`ReadingProgressCalculator` é um Domain Service puro, stateless e determinístico. Não depende de Repository, banco ou autenticação, não produz efeitos colaterais e não publica Domain Events.

O algoritmo:

1. extrai os intervalos inclusivos `start_page..end_page` das ReadingSessions;
2. ordena por `start_page` e `end_page`;
3. funde intervalos sobrepostos;
4. funde intervalos adjacentes;
5. soma `end - start + 1` para obter `unique_pages_read`;
6. obtém `highest_page_reached` pelo maior `end_page` ou `None` quando não há sessões;
7. calcula o percentual;
8. determina a conclusão.

O tempo total é `O(n log n)` devido à ordenação, a consolidação é `O(n)` e a memória auxiliar é `O(n)`. O algoritmo não expande intervalos página por página.

Sobreposições não duplicam páginas, releituras não aumentam o progresso e a ordem das ReadingSessions não altera o resultado. `highest_page_reached` é apenas a maior página alcançada historicamente e não representa posição atual.

O Domain calcula `percentage` com `Decimal`, precisão de duas casas e `ROUND_HALF_UP`. A conclusão obedece exclusivamente a `completed = unique_pages_read == total_pages`; alcançar isoladamente a última página não conclui o Book.

READ-003 não adiciona `progress`, `pages_read`, `percentage`, `completed` ou `highest_page_reached` ao `Book`. O progresso não é armazenado no Book. `ReadingSession` não sofreu alteração funcional: a Feature apenas utiliza os fatos históricos já registrados pelas sessões.

O fluxo de consulta da Application é:

```text
GetReadingProgressQuery
        ↓
GetReadingProgressQueryHandler
        ↓
Book owner-scoped
        ↓
ReadingSessions owner-scoped
        ↓
ReadingProgressCalculator
        ↓
ReadingProgressDTO
```

Trata-se de uma Query: não utiliza Unit of Work, não executa `commit` nem `save`. O Handler reutiliza `BookNotFoundError`, mantendo Book inexistente e Book pertencente a outro owner indistinguíveis.

---

## Eventos

READ-001, READ-002 e READ-003 não publicam Domain Events. Em particular, o cálculo de Reading Progress não cria evento algum.

---
# Bounded Context — Therapy

## Responsabilidade

Registrar sessões terapêuticas.

---

## Entidades

Therapist

TherapySession

---

## Eventos

TherapyRegistered

---

# Bounded Context — Habits

## Responsabilidade

Registrar hábitos.

---

## Entidades

Habit

HabitRecord

HabitStreak

---

## Eventos

HabitCompleted

HabitBroken

---

# Bounded Context — Gamification

## Responsabilidade

Transformar ações em evolução.

---

## Entidades

Quest

Achievement

Reward

Skill

ExperienceTransaction

---

## Eventos

QuestCompleted

AchievementUnlocked

RewardGranted

---

# Bounded Context — Analytics

## Responsabilidade

Gerar indicadores.

---

## Entidades

KPI

Trend

Correlation

Insight

---

## Eventos

InsightGenerated

---

# Bounded Context — AI Mentor

## Responsabilidade

Interpretar dados.

---

## Entidades

Recommendation

MissionSuggestion

CoachMessage

---

## Eventos

RecommendationGenerated

---

# Aggregate Roots

O LifeOS utilizará Aggregate Roots para proteger consistência.

Aggregates oficiais:

```
User

Character

Workout

Book

ReadingSession

Habit

Quest

TherapySession

SleepRecord
```

Todo acesso deverá ocorrer através da Aggregate Root.

Nunca acessar entidades internas diretamente.

---

# Entidades

Uma Entity possui identidade própria.

Exemplos:

```
Character

Workout

Book

ReadingSession

Habit
```

Características:

- identidade permanente;
- ciclo de vida;
- comportamento;
- regras.

---

# Value Objects

São objetos imutáveis.

Exemplos:

```
Email

XP

Level

Weight

Height

HeartRate

Percentage

DateRange
```

Características:

- imutáveis;
- sem identidade;
- comparados por valor.

---

# Domain Services

Existem regras que não pertencem a uma única entidade.

Essas regras deverão ser implementadas em Domain Services.

Exemplos:

```
GamificationService

CharacterEvolutionService

AnalyticsService

HealthScoreService

RecommendationService
```

---

# Repository Interfaces

Cada Aggregate Root possuirá uma interface de Repository.

Exemplo:

```
CharacterRepository

WorkoutRepository

BookRepository

ReadingSessionRepository

HabitRepository
```

As implementações pertencem à Infrastructure.

---

# Domain Events

Eventos representam acontecimentos importantes do domínio.

Exemplos:

```
UserRegistered

WorkoutCompleted

SleepRegistered

XPGranted

LevelUp

AchievementUnlocked
```

Eventos devem ser utilizados para reduzir acoplamento entre módulos.

---

# Invariantes

Cada Aggregate deverá proteger suas próprias invariantes.

Exemplos:

Character

- XP nunca negativa.

Workout

- Data obrigatória.

Habit

- Frequência válida.

User

- Email único.

---

# Fábricas (Factories)

Objetos complexos deverão utilizar Factories.

Exemplos:

```
CharacterFactory

QuestFactory

AchievementFactory
```

---

# Specifications

Regras reutilizáveis deverão utilizar Specification Pattern.

Exemplos:

```
EligibleForLevelUpSpecification

QuestCompletedSpecification

AchievementUnlockedSpecification
```

---

# Policies

Políticas representam regras variáveis.

Exemplos:

```
XPPolicy

RewardPolicy

DifficultyPolicy

StreakPolicy
```

---

# Anti-patterns

Nunca:

✘ Colocar regras na interface.

✘ Colocar SQL nas Entities.

✘ Criar Entities anêmicas.

✘ Duplicar regras em Services.

✘ Misturar múltiplos domínios na mesma Entity.

---

# Fluxo de Desenvolvimento

Sempre implementar nesta ordem:

```
Domínio

↓

Entity

↓

Value Object

↓

Domain Service

↓

Repository Interface

↓

Use Case

↓

Infrastructure

↓

Presentation
```

---

# Como um Agente de IA deve utilizar este documento

Antes de implementar qualquer funcionalidade:

1. Identificar o Bounded Context.

2. Identificar o Aggregate Root.

3. Identificar as Entities envolvidas.

4. Verificar Value Objects existentes.

5. Criar Domain Events necessários.

6. Criar Repository Interfaces.

7. Somente então implementar o Use Case.

Qualquer implementação que viole essa sequência deverá ser considerada incorreta.

---

# Critérios de Aceite

Este documento será considerado concluído quando:

- Todos os Bounded Contexts estiverem definidos.
- Todos os Aggregates estiverem identificados.
- Todas as Entities principais estiverem documentadas.
- Todos os Value Objects principais estiverem documentados.
- O fluxo oficial de modelagem estiver estabelecido.

---

# Referências

- Eric Evans — Domain-Driven Design
- Vaughn Vernon — Implementing Domain-Driven Design
- Martin Fowler — Patterns of Enterprise Application Architecture
- Robert C. Martin — Clean Architecture
