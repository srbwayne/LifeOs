# CLEAN ARCHITECTURE

## LifeOS

**Versão:** 1.0

**Status:** Documento Oficial

**Arquitetura Base:** Clean Architecture adaptada ao LifeOS

---

# Objetivo

Este documento define a arquitetura oficial do LifeOS baseada nos princípios da Clean Architecture.

Seu objetivo é estabelecer como o software será organizado, quais responsabilidades pertencem a cada camada e quais dependências são permitidas.

Toda implementação deverá respeitar as regras definidas neste documento.

---

# Motivação

O LifeOS foi concebido como uma plataforma de longa duração.

Ao longo de sua evolução serão adicionados novos módulos, novas interfaces e novas tecnologias.

Para evitar que essas mudanças impactem as regras de negócio, a arquitetura deve isolar o domínio das demais camadas.

A Clean Architecture foi escolhida porque permite:

- independência da interface;
- independência do banco de dados;
- facilidade de testes;
- baixo acoplamento;
- alta coesão;
- evolução incremental.

---

# Objetivos Arquiteturais

A arquitetura do LifeOS possui os seguintes objetivos:

- proteger o domínio;
- desacoplar tecnologias;
- facilitar manutenção;
- permitir evolução contínua;
- permitir testes independentes;
- facilitar substituição de frameworks.

---

# Visão Geral

```
                Presentation

                      │

                      ▼

                Application

                      │

                      ▼

                  Domain

                      │

                      ▼

              Infrastructure

                      │

                      ▼

                 Persistence
```

Toda dependência aponta para o centro da arquitetura.

---

# Camadas

O LifeOS é organizado em cinco camadas principais.

| Camada | Responsabilidade |
|----------|------------------|
| Presentation | Interface com o usuário |
| Application | Casos de uso |
| Domain | Regras de negócio |
| Infrastructure | Recursos externos |
| Persistence | Armazenamento |

---

# Presentation Layer

## Objetivo

Receber entradas do usuário e apresentar resultados.

---

## Responsabilidades

- páginas Streamlit;
- componentes;
- navegação;
- formulários;
- validação visual;
- mensagens ao usuário.

---

## Não é permitido

- regras de negócio;
- acesso direto ao banco;
- SQL;
- cálculos de domínio;
- lógica de XP;
- lógica de Analytics.

---

## Pode utilizar

- DTOs
- Use Cases
- ViewModels

Nunca Entities diretamente.

---

# Application Layer

## Objetivo

Executar os Casos de Uso do sistema.

Esta camada coordena a execução das funcionalidades.

---

## Contém

- Use Cases
- Commands
- Queries
- DTOs
- Application Services
- Mappers

---

## Responsabilidades

- coordenar operações;
- validar fluxo;
- iniciar transações;
- chamar o domínio;
- retornar resultados.

---

## Não contém

- SQL
- Interface
- Componentes Streamlit

---

# Domain Layer

## Objetivo

Representar o conhecimento do negócio.

Esta é a camada mais importante do sistema.

---

## Contém

- Entities
- Value Objects
- Domain Services
- Aggregates
- Policies
- Specifications
- Domain Events
- Repository Interfaces

---

## Responsabilidades

- regras de negócio;
- cálculos;
- validações;
- políticas;
- comportamento do Character;
- comportamento da Gamificação.

---

## Nunca depende de

- Streamlit
- SQLAlchemy
- SQLite
- Banco
- Frameworks
- APIs

O domínio deve ser completamente independente.

---

# Infrastructure Layer

## Objetivo

Implementar recursos externos.

---

## Contém

- SQLAlchemy
- Logger
- Configuração
- Email
- Cache
- Backup
- APIs externas

---

## Responsabilidades

Implementar interfaces definidas pelo domínio.

Exemplo:

Domain

```
UserRepository
```

Infrastructure

```
SqlAlchemyUserRepository
```

---

# Persistence Layer

## Objetivo

Persistir informações.

---

## Responsabilidades

- SQLite
- PostgreSQL (futuro)
- Migrações
- Conexões

A persistência nunca contém regras de negócio.

---

# Regra Fundamental

Toda dependência aponta para dentro.

Nunca para fora.

```
Presentation

↓

Application

↓

Domain

↑

Infrastructure

↑

Persistence
```

---

# Fluxo Oficial

```mermaid
flowchart TD

UI

-->

UseCase

-->

Domain

-->

Repository Interface

-->

Repository SQLAlchemy

-->

Database
```

---

# Inversão de Dependência

O domínio define contratos.

A infraestrutura implementa esses contratos.

Exemplo

```
Domain

UserRepository

↓

Infrastructure

SqlAlchemyUserRepository
```

Nunca o contrário.

---

# Regras de Dependência

## Presentation

Pode depender de

- Application

Não pode depender de

- Infrastructure
- Persistence

---

## Application

Pode depender de

- Domain

Não pode depender de

- Streamlit
- SQLAlchemy

---

## Domain

Não depende de nenhuma camada.

É completamente isolado.

---

## Infrastructure

Pode depender de

- Domain

Nunca da Presentation.

---

## Persistence

Pode depender apenas da Infrastructure.

---

# Use Cases

Todo comportamento do sistema deverá ser iniciado por um Use Case.

Exemplos:

RegisterUserUseCase

RegisterWorkoutUseCase

RegisterSleepUseCase

CalculateXPUseCase

GenerateDashboardUseCase

---

# Entities

Entities representam conceitos do domínio.

Exemplos:

Player

Character

Workout

Book

Sleep

Habit

TherapySession

---

# Value Objects

Representam conceitos imutáveis.

Exemplos:

Email

Password

XP

Level

Weight

Height

HeartRate

---

# Domain Services

Responsáveis por regras que envolvem múltiplas entidades.

Exemplos:

GamificationService

AnalyticsService

CharacterEvolutionService

---

# Repository Pattern

Todo acesso ao banco deverá ocorrer através de Repositories.

Nunca utilizar SQL diretamente nas regras de negócio.

---

# Eventos

A comunicação entre módulos deverá utilizar Domain Events sempre que possível.

Exemplos:

UserCreated

WorkoutRegistered

XPGranted

LevelUp

AchievementUnlocked

---

# Testabilidade

Cada camada poderá ser testada isoladamente.

Tipos de testes:

- Unitários
- Integração
- Arquitetura
- Contrato

---

# Evolução

Novas tecnologias poderão substituir:

- Streamlit
- SQLAlchemy
- SQLite

Sem necessidade de alterar:

- Entities
- Regras
- Casos de Uso

---

# Boas Práticas

Sempre:

✔ Criar Use Cases.

✔ Manter regras no domínio.

✔ Utilizar DTOs.

✔ Utilizar Repository Pattern.

✔ Utilizar Dependency Injection quando necessário.

✔ Escrever testes.

---

# Anti-patterns

Nunca:

✘ SQL na interface.

✘ Regras de negócio em páginas Streamlit.

✘ Entity acessando banco.

✘ Repository contendo regras de negócio.

✘ Service contendo SQL.

✘ Interface chamando Infrastructure diretamente.

---

# Como um Agente de IA deve utilizar este documento

Antes de implementar qualquer funcionalidade, o agente deve:

1. Identificar a Capability correspondente.
2. Identificar o Caso de Uso relacionado.
3. Criar o Use Case na camada Application.
4. Implementar ou reutilizar Entities no Domain.
5. Utilizar apenas interfaces de Repository.
6. Implementar persistência na Infrastructure.
7. Expor a funcionalidade na Presentation.
8. Criar testes.
9. Atualizar a documentação.

Qualquer implementação que viole estas regras deverá ser considerada incorreta.

---

# Critérios de Aceite

Este documento será considerado concluído quando:

- Todas as camadas estiverem claramente definidas.
- As regras de dependência estiverem documentadas.
- Os papéis de cada camada estiverem descritos.
- Os fluxos estiverem representados.
- As boas práticas e anti-patterns estiverem definidos.

---

# Referências

- Robert C. Martin — Clean Architecture
- Domain-Driven Design — Eric Evans
- Clean Code — Robert C. Martin
- The Pragmatic Programmer