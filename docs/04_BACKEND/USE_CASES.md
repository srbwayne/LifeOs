# USE_CASES

## READ-006 — ListReadingHistory

ListReadingHistoryQuery contains owner_id, page, and size.
ListReadingHistoryQueryHandler obtains total_items, translates page/size to
offset/limit, retrieves the projected page, and calculates total_pages. It is
read-only and uses no Unit of Work, EventBus, save, or commit.

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Use Cases  
**Camadas Relacionadas:** Presentation, Application, Domain e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal e Monólito Modular

---

# 1. Objetivo

Este documento define o padrão oficial para implementação de **Use Cases** no LifeOS.

Os Use Cases representam a camada **Application** da arquitetura e constituem a principal forma de execução das regras de negócio pelo sistema.

Seu objetivo é estabelecer:

- responsabilidades dos Use Cases;
- organização da camada Application;
- padrão de implementação;
- interação entre módulos;
- controle transacional;
- integração com Domain;
- utilização de Repositories;
- utilização de Domain Services;
- publicação de eventos;
- isolamento Multi-Tenant;
- tratamento de erros;
- testabilidade;
- padronização para desenvolvimento humano e por agentes de IA.

Todo novo fluxo funcional do sistema deverá ser implementado como um Use Case seguindo este documento.

---

# 2. Papel dos Use Cases na Clean Architecture

Na arquitetura oficial do LifeOS, os Use Cases pertencem exclusivamente à **Application Layer**.

Eles representam as ações que um usuário ou sistema pode executar.

Fluxo arquitetural:

```text
Presentation
        │
        ▼
Controller
        │
        ▼
Use Case
        │
 ┌──────┴──────────┐
 ▼                 ▼
Domain        Repositories
        │
        ▼
Infrastructure
```

O Use Case atua como orquestrador da execução.

Ele conecta:

- Interface do usuário;
- Domínio;
- Persistência;
- Eventos;
- Serviços externos.

Sem conhecer detalhes tecnológicos.

---

# 3. Princípios

Todo Use Case deve obedecer aos seguintes princípios.

## 3.1 Responsabilidade Única

Cada Use Case representa exatamente **uma intenção do usuário**.

Exemplos:

```text
RegisterWorkoutUseCase

RegisterSleepUseCase

CompleteHabitUseCase

ResetPasswordUseCase

CreateCharacterUseCase
```

Nunca representar múltiplas funcionalidades distintas.

---

## 3.2 Independência Tecnológica

Um Use Case nunca depende diretamente de:

- Streamlit;
- SQLAlchemy;
- SQLite;
- PostgreSQL;
- HTTP;
- SMTP;
- Gemini;
- OpenAI;
- Plotly.

Ele depende apenas de contratos definidos pela arquitetura.

---

## 3.3 Linguagem Ubíqua

O nome do Use Case deve refletir a linguagem do domínio.

Correto:

```text
GrantExperienceUseCase
```

Evitar:

```text
ProcessDataUseCase

MainUseCase

UserOperationUseCase
```

---

## 3.4 Orquestração

O Use Case coordena objetos.

Ele não concentra regras de negócio.

As regras pertencem ao Domain.

---

## 3.5 Testabilidade

Todo Use Case deve ser facilmente testável utilizando:

- Repositories em memória;
- Fakes;
- Mocks apenas quando necessário;
- Unit of Work fake;
- Clock fake;
- Event Publisher fake.

---

# 4. Responsabilidades

Um Use Case pode:

- receber um comando;
- validar pré-condições de aplicação;
- abrir transação;
- carregar Aggregates;
- chamar Domain Services;
- chamar Entities;
- persistir alterações;
- publicar eventos;
- retornar resultado.

Ele representa um fluxo completo da aplicação.

---

## Exemplo

```text
Registrar treino

↓

Carregar Character

↓

Calcular XP

↓

Atualizar atributos

↓

Persistir treino

↓

Persistir Character

↓

Publicar evento

↓

Retornar resultado
```

---

## Outro exemplo

```text
Cadastrar usuário

↓

Validar e-mail

↓

Criar User

↓

Criar Character

↓

Criar Preferências

↓

Persistir

↓

Criar Sessão

↓

Retornar Login
```

---

# 5. O que um Use Case pode fazer

Um Use Case pode:

## Coordenar múltiplos módulos

Exemplo:

```text
Auth

↓

Character

↓

Gamification
```

---

## Utilizar múltiplos Repositories

Exemplo:

```text
UserRepository

CharacterRepository

PreferencesRepository
```

---

## Utilizar Domain Services

Exemplo:

```text
ExperienceCalculationService

LevelProgressionService

RecoveryScoreService
```

---

## Utilizar Policies

Exemplo:

```text
ExperiencePolicy

PasswordPolicy

RewardPolicy
```

---

## Utilizar Specifications

Exemplo:

```text
EligibleForLevelUpSpecification
```

---

## Publicar eventos

Exemplo:

```text
WorkoutRegistered

ExperienceGranted

CharacterLeveledUp
```

---

## Controlar Unit of Work

Exemplo:

```python
with self._unit_of_work:
    ...
    self._unit_of_work.commit()
```

---

## Retornar DTO

Nunca retornar Entity diretamente para a interface.

---

# 6. O que um Use Case NÃO pode fazer

É proibido ao Use Case:

## Conhecer Streamlit

Errado:

```python
import streamlit as st
```

---

## Conhecer SQLAlchemy

Errado:

```python
Session()
```

---

## Executar SQL

Errado:

```python
SELECT *
```

---

## Conhecer tabelas

Errado:

```python
WorkoutModel
```

---

## Montar gráficos

Errado:

```python
plotly.graph_objects
```

---

## Enviar e-mail diretamente

Utilizar:

```text
EmailSender
```

---

## Fazer hash diretamente

Utilizar:

```text
PasswordHasher
```

---

## Criar conexão HTTP

Utilizar Ports.

---

## Criar Providers concretos

Errado:

```python
GeminiProvider()
```

Correto:

```python
AIProvider
```

---

## Conter regra de negócio pesada

Essa responsabilidade pertence:

- Entity;
- Aggregate;
- Domain Service;
- Policy;
- Specification.

---

# 7. Fluxo Oficial de Execução

Todo Use Case deve seguir o mesmo fluxo arquitetural.

```text
Controller

↓

Request DTO

↓

Use Case

↓

Validações

↓

Repositories

↓

Domain

↓

Repositories

↓

Commit

↓

Publish Events

↓

Response DTO
```

---

Fluxo completo:

```text
Presentation

↓

Controller

↓

Input DTO

↓

Use Case

↓

Load Aggregates

↓

Domain Services

↓

Entities

↓

Repositories

↓

Commit

↓

Event Publisher

↓

Output DTO

↓

Presenter

↓

UI
```

---

Essa sequência é obrigatória.

---

# 8. Estrutura Oficial de Diretórios

Cada módulo possui sua própria camada Application.

Estrutura:

```text
module/

application/

├── use_cases/

├── dto/

├── commands/

├── queries/

├── services/

├── mappers/

├── exceptions/

└── validators/
```

---

Exemplo:

```text
modules/

workout/

application/

use_cases/

├── register_workout_use_case.py

├── delete_workout_use_case.py

├── update_workout_use_case.py

└── get_workout_history_use_case.py
```

---

Outro exemplo:

```text
modules/

auth/

application/

use_cases/

register_user_use_case.py

login_use_case.py

reset_password_use_case.py
```

---

# 9. Convenções de Nomenclatura

Todos os nomes devem iniciar com verbo.

Correto:

```text
CreateCharacterUseCase

RegisterWorkoutUseCase

ReadDashboardUseCase

GenerateWeeklySummaryUseCase

UnlockAchievementUseCase

GrantExperienceUseCase
```

---

Evitar:

```text
CharacterUseCase

WorkoutManager

MainUseCase

GeneralUseCase

LifeOSUseCase
```

---

Arquivo:

```text
register_workout_use_case.py
```

Classe:

```python
RegisterWorkoutUseCase
```

---

# 10. Template Oficial de Use Case

Todo novo Use Case deverá seguir o template oficial.

```python
class RegisterWorkoutUseCase:

    def __init__(
        self,
        workout_repository: WorkoutRepository,
        character_repository: CharacterRepository,
        experience_service: ExperienceCalculationService,
        unit_of_work: UnitOfWork,
        event_publisher: EventPublisher,
    ) -> None:

        self._workout_repository = workout_repository
        self._character_repository = character_repository
        self._experience_service = experience_service
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher

    def execute(
        self,
        command: RegisterWorkoutCommand,
    ) -> RegisterWorkoutResult:

        with self._unit_of_work:

            character = self._character_repository.get_by_user_id(
                command.user_id
            )

            workout = Workout.create(command)

            xp = self._experience_service.calculate_for_workout(
                workout
            )

            character.grant_experience(xp)

            self._workout_repository.save(workout)

            self._character_repository.save(character)

            self._unit_of_work.commit()

            self._event_publisher.publish(
                character.collect_domain_events()
            )

        return RegisterWorkoutResult.success(
            workout_id=workout.id,
            experience=xp,
            new_level=character.global_level,
        )
```

### Características obrigatórias

- responsabilidade única;
- dependências por construtor;
- contratos ao invés de implementações;
- uso de DTOs;
- Unit of Work;
- Repositories;
- Domain Services;
- publicação de eventos após commit;
- retorno imutável;
- nenhuma dependência tecnológica da UI ou banco.

Este template será o padrão oficial para todos os Use Cases do LifeOS.

---

# 11. Input Models (Commands)

Todo Use Case deve receber um **Input Model** explícito.

O Input Model representa a intenção do usuário, encapsulando todos os dados necessários para execução do caso de uso.

Não é permitido receber parâmetros soltos.

Correto:

```python
@dataclass(frozen=True)
class RegisterWorkoutCommand:
    user_id: UserId
    workout_type_id: WorkoutTypeId
    occurred_at: datetime
    duration_minutes: int
    perceived_effort: int
    notes: str | None
```

Errado:

```python
def execute(
    user_id,
    workout_type,
    duration,
    effort,
    notes,
):
```

---

## Características obrigatórias

Todo Command deve:

- ser imutável (`frozen=True`);
- possuir tipos explícitos;
- utilizar Value Objects quando disponíveis;
- representar apenas dados de entrada;
- não possuir comportamento.

---

## Organização

```text
application/

commands/

├── register_workout_command.py
├── create_character_command.py
├── register_sleep_command.py
└── complete_habit_command.py
```

---

# 12. Output Models (Results)

Todo Use Case deve retornar um **Result Model**.

Nunca retornar:

- Entity;
- Aggregate;
- ORM Model;
- dicionário genérico;
- tupla.

Correto:

```python
@dataclass(frozen=True)
class RegisterWorkoutResult:
    workout_id: WorkoutId
    granted_experience: int
    new_level: int
    unlocked_achievements: tuple[str, ...]
```

---

## Benefícios

- desacoplamento;
- estabilidade da API;
- independência da UI;
- facilidade de testes;
- evolução controlada.

---

## Organização

```text
application/

results/

├── register_workout_result.py
├── login_result.py
├── dashboard_result.py
└── create_character_result.py
```

---

# 13. Controllers

Controllers representam a fronteira entre a interface e a camada Application.

São responsáveis por:

- receber dados da interface;
- validar formato básico;
- montar Commands;
- executar Use Cases;
- encaminhar Result ao Presenter.

Fluxo:

```text
UI

↓

Controller

↓

Command

↓

Use Case

↓

Result

↓

Presenter
```

---

O Controller nunca deve:

- acessar banco;
- executar SQL;
- calcular regras;
- manipular ORM;
- alterar Entities.

---

Exemplo:

```python
class RegisterWorkoutController:

    def execute(
        self,
        request: WorkoutRequest,
    ) -> WorkoutResponse:

        command = RegisterWorkoutCommand(
            ...
        )

        result = self._use_case.execute(command)

        return self._presenter.present(result)
```

---

# 14. Presenters

O Presenter transforma o Result em um formato adequado para a interface.

Responsabilidades:

- adaptar dados;
- formatar respostas;
- esconder detalhes internos;
- preparar View Models.

Nunca executar regra de negócio.

---

Fluxo:

```text
Use Case

↓

Result

↓

Presenter

↓

ViewModel

↓

UI
```

---

Exemplo:

```python
class DashboardPresenter:

    def present(
        self,
        result: DashboardResult,
    ) -> DashboardViewModel:

        ...
```

---

# 15. DTOs

DTOs representam objetos de transporte entre camadas.

Existem três categorias oficiais:

```text
Command DTO

Result DTO

View DTO
```

---

DTOs devem ser:

- imutáveis;
- simples;
- serializáveis;
- independentes do banco.

Nunca conter:

- comportamento;
- lógica;
- validações complexas.

---

Exemplo:

```python
@dataclass(frozen=True)
class LoginResult:
    user_name: str
    session_token: str
```

---

# 16. Current User

Todo Use Case operacional deve conhecer o usuário autenticado.

O acesso ocorre por abstração.

```python
class CurrentUserProvider(Protocol):

    def get_current_user_id(
        self,
    ) -> UserId:
        ...
```

---

Fluxo:

```text
Session

↓

CurrentUserProvider

↓

Use Case
```

---

O Use Case nunca deve acessar:

```python
st.session_state
```

ou qualquer mecanismo da interface.

---

# 17. Unit of Work

Todo Use Case que altera estado deve utilizar Unit of Work.

Fluxo:

```python
with self._unit_of_work:

    ...

    self._unit_of_work.commit()
```

---

Responsabilidades:

- abrir transação;
- coordenar Repositories;
- realizar commit;
- executar rollback;
- controlar consistência.

---

O Use Case nunca deve chamar:

```python
session.commit()
```

---

# 18. Repositories

Use Cases acessam persistência exclusivamente por Repository.

Nunca por:

- SQL;
- Session;
- ORM;
- DataFrame;
- Cursor.

Exemplo:

```python
character = self._character_repository.get_by_user_id(
    command.user_id
)
```

---

O Use Case pode utilizar múltiplos Repositories.

Exemplo:

```text
CharacterRepository

WorkoutRepository

AchievementRepository
```

Todos compartilhando a mesma Unit of Work.

---

# 19. Domain Services

Quando uma regra envolver múltiplos objetos do domínio, o Use Case deve delegar para um Domain Service.

Exemplo:

```python
xp = self._experience_service.calculate_for_workout(
    workout
)
```

O Use Case coordena.

O Domain Service calcula.

---

Nunca mover regras complexas para o próprio Use Case.

---

# 20. Policies

Quando uma regra for configurável, ela deve ser encapsulada em uma Policy.

Exemplo:

```text
ExperiencePolicy

RewardPolicy

PasswordPolicy

RecoveryPolicy
```

Fluxo:

```text
Use Case

↓

Domain Service

↓

Policy
```

---

Exemplo:

```python
xp = self._experience_service.calculate(
    workout,
    self._experience_policy,
)
```

---

Benefícios:

- regras configuráveis;
- testes simplificados;
- substituição de estratégias;
- desacoplamento;
- reutilização.

Os Use Cases nunca devem conter valores mágicos ou fórmulas diretamente no código quando essas regras pertencerem a uma Policy.

---

# 21. Specifications

Specifications representam regras booleanas reutilizáveis do domínio.

Seu objetivo é encapsular critérios de elegibilidade, validações complexas e regras de decisão que podem ser reutilizadas por diversos Use Cases e Domain Services.

Exemplos:

```text
EligibleForLevelUpSpecification

QuestCompletedSpecification

AchievementUnlockedSpecification

CanResetPasswordSpecification

WorkoutEligibleForXPRewardSpecification
```

---

## Fluxo

```text
Use Case

↓

Specification

↓

true / false
```

---

## Exemplo

```python
if not self._eligible_for_level_up.is_satisfied_by(
    character
):
    raise CharacterNotEligibleForLevelUpError()
```

---

## Benefícios

- reutilização;
- isolamento de regras;
- código legível;
- facilidade de testes;
- eliminação de condicionais duplicadas.

Use Cases nunca devem conter regras booleanas complexas quando uma Specification puder representá-las.

---

# 22. Domain Events

Todo Use Case deve respeitar a estratégia oficial de Domain Events.

O Use Case não cria eventos manualmente.

Quem cria eventos são:

- Entities;
- Aggregates;
- Domain Services.

O Use Case apenas coleta e publica.

---

Fluxo:

```text
Entity

↓

Domain Event

↓

Use Case

↓

Event Publisher
```

---

Exemplo:

```python
character.grant_experience(xp)

events = character.collect_domain_events()
```

---

Eventos devem representar fatos já ocorridos.

Exemplos:

```text
WorkoutRegistered

ExperienceGranted

CharacterLeveledUp

AchievementUnlocked

HabitCompleted
```

---

# 23. Publicação de Eventos

A publicação ocorre somente após sucesso da transação.

Fluxo obrigatório:

```text
Use Case

↓

Repositories

↓

Commit

↓

Publish Events
```

Nunca:

```text
Publish

↓

Commit
```

---

Exemplo:

```python
with self._unit_of_work:

    ...

    self._unit_of_work.commit()

self._event_publisher.publish(events)
```

---

Benefícios:

- consistência;
- ausência de eventos fantasmas;
- integridade entre módulos;
- preparação para Outbox Pattern.

---

# 24. Idempotência

Todo Use Case acionado por:

- eventos;
- filas;
- webhooks;
- sincronizações;
- jobs;

deve ser idempotente.

---

Exemplo:

```text
GrantExperienceFromWorkoutUseCase
```

não pode conceder XP duas vezes para o mesmo treino.

---

Estratégias:

- EventId;
- RequestId;
- Idempotency Key;
- Unique Constraint;
- Event Store.

---

Um mesmo comando executado repetidamente deve produzir o mesmo estado final.

---

# 25. Multi-Tenant

Todo Use Case operacional deve preservar isolamento entre usuários.

Fluxo:

```text
Current User

↓

Use Case

↓

Repositories

↓

WHERE user_id = current_user
```

---

Jamais confiar em:

```text
user_id enviado pela interface
```

O usuário autenticado deve ser obtido pelo contexto da aplicação.

---

Todo acesso a dados deve respeitar:

```text
Ownership

Tenant Isolation

Authorization
```

---

# 26. Tratamento de Erros

Use Cases devem lançar erros de aplicação.

Não lançar:

```text
IntegrityError

OperationalError

SQLAlchemyError

SMTPException
```

Esses erros pertencem à infraestrutura.

---

Exemplos corretos:

```text
WorkoutNotFoundError

CharacterNotFoundError

EmailAlreadyRegisteredError

PermissionDeniedError

QuestAlreadyCompletedError
```

---

Fluxo:

```text
Infrastructure Exception

↓

Application Exception

↓

Controller

↓

UI
```

---

# 27. Validação

Existem três níveis oficiais de validação.

---

## Validação de Interface

Formato.

Exemplo:

- campo obrigatório;
- e-mail válido;
- número inteiro.

---

## Validação de Aplicação

Fluxo.

Exemplo:

```text
Usuário autenticado?

Permissão?

Treino existente?
```

---

## Validação de Domínio

Regras do negócio.

Exemplo:

```text
Pode subir de nível?

Pode concluir Quest?

Pode ganhar XP?
```

---

Cada validação deve ocorrer na camada correta.

---

# 28. Logging

Use Cases podem registrar logs técnicos.

Permitido:

```text
Início

Fim

Tempo

Falha

Identificador da operação
```

---

Nunca registrar:

- senha;
- token;
- código de redefinição;
- notas terapêuticas;
- dados médicos completos;
- prompts privados da IA.

---

Exemplo:

```text
INFO

RegisterWorkoutUseCase started

User: xxxxx

CorrelationId: yyyy
```

---

# 29. Segurança

Todo Use Case deve assumir que a interface é potencialmente maliciosa.

Deve validar:

- autenticação;
- autorização;
- ownership;
- permissões;
- escopo;
- tenant.

---

Jamais confiar em:

- parâmetros ocultos;
- IDs enviados pelo cliente;
- dados da sessão manipuláveis;
- campos calculados pelo frontend.

---

Fluxo:

```text
Authenticate

↓

Authorize

↓

Validate Ownership

↓

Execute
```

---

# 30. Performance

Todo Use Case deve considerar desempenho como requisito arquitetural.

Boas práticas:

- evitar N+1;
- evitar consultas repetidas;
- utilizar paginação;
- utilizar Read Models;
- evitar carregar histórico completo;
- minimizar tempo de transação;
- publicar eventos após commit;
- utilizar Queries específicas quando necessário.

---

Evitar:

```text
for item:

↓

Repository.find()
```

Preferir:

```text
Repository.find_by_ids()
```

---

Antes de otimizar, medir.

A otimização deve ser baseada em evidências e manter a clareza arquitetural.

Um Use Case deve ser simples, previsível, testável e eficiente, sem sacrificar a legibilidade ou as regras de negócio.

---

# 31. Sincronia

Os Use Cases síncronos representam operações cujo resultado é necessário imediatamente para a continuidade da interação do usuário.

O usuário aguarda a conclusão da execução antes de prosseguir.

São utilizados quando:

- o resultado precisa ser exibido imediatamente;
- a consistência deve ser imediata;
- a operação faz parte da mesma transação;
- uma falha deve impedir a continuidade do fluxo.

---

## Exemplos

```text
Login

↓

Cadastro de Usuário

↓

Registrar Treino

↓

Registrar Sono

↓

Atualizar Perfil

↓

Alterar Senha
```

---

Fluxo:

```text
Controller

↓

Use Case

↓

Repositories

↓

Commit

↓

Return Result
```

---

Características:

- resposta imediata;
- transação única;
- consistência forte;
- execução previsível;
- menor complexidade operacional.

---

# 32. Assincronia

Use Cases assíncronos representam operações que não precisam finalizar antes da resposta ao usuário.

Devem ser utilizados quando:

- processamento for pesado;
- envolver IA;
- gerar relatórios;
- enviar notificações;
- recalcular indicadores;
- integrar serviços externos.

---

Exemplos

```text
Gerar relatório PDF

↓

Gerar recomendações com IA

↓

Enviar e-mail

↓

Recalcular Analytics

↓

Gerar Snapshot do Dashboard
```

---

Fluxo

```text
Use Case

↓

Commit

↓

Domain Event

↓

Event Handler

↓

Background Job

↓

Resultado
```

---

Benefícios

- menor tempo de resposta;
- melhor escalabilidade;
- menor tempo de transação;
- desacoplamento.

---

A consistência eventual deve ser aceita apenas quando não comprometer regras críticas do domínio.

---

# 33. Transactions

Todo Use Case que modifica estado deve executar dentro de uma transação.

Fluxo oficial:

```text
Open Transaction

↓

Load Aggregates

↓

Business Rules

↓

Persist

↓

Commit

↓

Publish Events
```

---

A transação deve conter apenas o necessário.

Evitar:

- chamadas HTTP;
- IA;
- SMTP;
- exportações;
- processamento pesado.

---

Exemplo

```python
with self._unit_of_work:

    ...

    self._unit_of_work.commit()
```

---

Nunca utilizar múltiplas transações independentes para uma única operação de negócio.

---

# 34. Rollback

Sempre que ocorrer uma falha durante a execução do Use Case, a transação deve ser revertida integralmente.

Fluxo:

```text
Use Case

↓

Erro

↓

Rollback

↓

Retorno da exceção
```

---

O rollback deve garantir que:

- nenhuma alteração parcial permaneça;
- nenhum evento seja publicado;
- nenhum Aggregate fique inconsistente.

---

O Use Case nunca deve executar:

```python
session.rollback()
```

Essa responsabilidade pertence à Unit of Work.

---

# 35. Retry

Retries não pertencem ao domínio.

Quando necessários, devem ocorrer apenas para operações técnicas.

Exemplos:

```text
SMTP

↓

API Externa

↓

Storage

↓

Provider IA
```

---

Nunca realizar retry em:

- cálculo de XP;
- subida de nível;
- criação de Character;
- conclusão de Quest.

---

Caso exista retry, ele deve ser:

- limitado;
- configurável;
- registrado em log;
- idempotente.

---

# 36. Timeout

Todo acesso externo deve possuir timeout configurado.

Exemplos:

```text
Gemini

OpenAI

SMTP

Webhook

REST API
```

---

Nunca deixar chamadas externas aguardando indefinidamente.

---

Fluxo recomendado:

```text
Use Case

↓

Provider

↓

Timeout

↓

Erro controlado
```

---

Timeouts devem ser tratados como exceções técnicas.

---

# 37. Facades

Cada módulo poderá disponibilizar uma Facade pública para comunicação entre módulos.

Fluxo:

```text
Module A

↓

Facade

↓

Module B
```

---

Exemplo

```python
class CharacterModuleFacade:

    def grant_experience(
        self,
        request: GrantExperienceRequest,
    ) -> GrantExperienceResult:
        ...
```

---

A Facade representa a API pública do módulo.

Ela nunca expõe:

- Repositories;
- ORM;
- SQL;
- Entities internas.

---

Benefícios

- baixo acoplamento;
- encapsulamento;
- evolução independente;
- contratos claros.

---

# 38. Integração entre Módulos

Os módulos do LifeOS comunicam-se exclusivamente através de:

- Facades;
- Events;
- Ports.

Nunca diretamente por:

- Repository;
- SQL;
- ORM;
- acesso ao banco.

---

Fluxo permitido

```text
Workout

↓

Game Facade

↓

Character
```

---

Fluxo proibido

```text
Workout

↓

CharacterRepository

↓

Tabela Character
```

---

Essa regra preserva a independência dos módulos.

---

# 39. AI Services

Use Cases nunca devem depender diretamente de uma implementação específica de IA.

Dependência correta:

```text
AIProvider
```

Implementações possíveis:

```text
GeminiAIProvider

OpenAIProvider

LocalLLMProvider
```

---

Exemplo

```python
class GenerateWeeklyMentorSummaryUseCase:

    def __init__(
        self,
        ai_provider: AIProvider,
    ):
        ...
```

---

O Use Case não conhece:

- SDK;
- API REST;
- autenticação;
- modelo utilizado.

---

A IA é apenas uma implementação da porta.

---

# 40. Analytics

Use Cases responsáveis por Analytics devem coordenar cálculos, nunca implementá-los diretamente.

Fluxo:

```text
Use Case

↓

Analytics Service

↓

Repositories

↓

Result DTO
```

---

Exemplo

```text
GenerateHealthInsightsUseCase

↓

HealthAnalyticsService

↓

DashboardResult
```

---

Analytics deve produzir:

- indicadores;
- métricas;
- tendências;
- correlações;
- previsões estatísticas.

Nunca:

- gráficos;
- componentes Streamlit;
- figuras Plotly;
- elementos HTML.

A responsabilidade da visualização pertence exclusivamente à camada de Presentation.

---

# 41. Character Use Cases

O módulo **Character** é responsável pela identidade RPG do usuário dentro do LifeOS.

Todos os Use Cases deste módulo devem manipular exclusivamente o Aggregate **Character** e seus componentes internos.

---

## Responsabilidades

São responsabilidades do módulo Character:

- criação do personagem;
- atualização dos atributos base;
- progressão de nível;
- cálculo do estado atual;
- gerenciamento de estatísticas;
- gerenciamento da ficha do personagem;
- histórico de evolução.

---

## Exemplos

```text
CreateCharacterUseCase

GetCharacterSheetUseCase

UpdateCharacterProfileUseCase

GrantAttributePointsUseCase

RecalculateCharacterStatsUseCase
```

---

O módulo Character não deve conhecer:

- Treinos;
- Leituras;
- Hábitos;
- Terapias.

Esses módulos comunicam-se através de Facades ou Domain Events.

---

# 42. Authentication Use Cases

O módulo Authentication controla todo o ciclo de vida da autenticação.

Responsabilidades:

- cadastro;
- login;
- logout;
- recuperação de senha;
- redefinição de senha;
- renovação de sessão;
- verificação de autenticação.

---

## Exemplos

```text
RegisterUserUseCase

AuthenticateUserUseCase

LogoutUserUseCase

RequestPasswordResetUseCase

ResetPasswordUseCase

RefreshSessionUseCase
```

---

Todo Use Case de autenticação deve utilizar apenas abstrações:

```text
PasswordHasher

EmailSender

TokenGenerator

CurrentUserProvider
```

Nunca implementações concretas.

---

# 43. Workout Use Cases

O módulo Workout representa todas as atividades físicas registradas pelo usuário.

Responsabilidades:

- registrar treino;
- editar treino;
- excluir treino;
- consultar histórico;
- consultar estatísticas;
- sincronizar métricas.

---

## Exemplos

```text
RegisterWorkoutUseCase

UpdateWorkoutUseCase

DeleteWorkoutUseCase

GetWorkoutHistoryUseCase

GetWorkoutStatisticsUseCase
```

---

Ao registrar um treino, o Use Case pode:

- persistir Workout;
- conceder XP;
- atualizar Character;
- publicar eventos.

Nunca calcular XP diretamente.

---

# 44. Health Use Cases

O módulo Health concentra registros fisiológicos e biométricos.

Responsabilidades:

- registrar sono;
- registrar peso;
- registrar gordura corporal;
- registrar VO₂;
- registrar recuperação;
- atualizar indicadores.

---

## Exemplos

```text
RegisterSleepUseCase

RegisterBodyCompositionUseCase

RegisterRecoveryMetricsUseCase

UpdateBiometricsUseCase

GetHealthDashboardUseCase
```

---

As fórmulas de saúde pertencem aos Domain Services.

O Use Case apenas coordena.

---

# 45. Reading Use Cases

O módulo Reading controla toda evolução intelectual baseada em leitura.

Responsabilidades:

- cadastrar livros;
- registrar leitura;
- concluir livro;
- registrar páginas;
- consultar histórico.

---

## Exemplos

```text
RegisterReadingSessionUseCase

FinishBookUseCase

CreateBookUseCase

GetReadingHistoryUseCase

GetReadingStatisticsUseCase
```

---

Ao concluir um livro:

- registrar progresso;
- atualizar Character;
- conceder XP;
- verificar Achievements.

---

# 46. Therapy Use Cases

O módulo Therapy registra sessões terapêuticas e evolução emocional.

Responsabilidades:

- registrar sessão;
- registrar insights;
- consultar histórico;
- acompanhar evolução.

---

## Exemplos

```text
RegisterTherapySessionUseCase

RegisterInsightUseCase

GetTherapyHistoryUseCase

GenerateTherapySummaryUseCase
```

---

As informações terapêuticas são consideradas dados sensíveis.

Todos os Use Cases deste módulo devem respeitar regras específicas de privacidade.

---

# 47. Habits Use Cases

O módulo Habits controla hábitos recorrentes do usuário.

Responsabilidades:

- cadastrar hábito;
- concluir hábito;
- calcular sequência (Streak);
- acompanhar frequência;
- gerar indicadores.

---

## Exemplos

```text
CreateHabitUseCase

CompleteHabitUseCase

ArchiveHabitUseCase

GetHabitDashboardUseCase

CalculateHabitStreakUseCase
```

---

Ao concluir um hábito:

- registrar execução;
- atualizar sequência;
- conceder XP;
- verificar Quests;
- publicar eventos.

---

# 48. Gamification Use Cases

O módulo Game é responsável pelo sistema de progressão do LifeOS.

Responsabilidades:

- conceder XP;
- desbloquear conquistas;
- subir de nível;
- atualizar atributos;
- concluir Quests;
- gerar recompensas.

---

## Exemplos

```text
GrantExperienceUseCase

EvaluateAchievementsUseCase

UnlockAchievementUseCase

CompleteQuestUseCase

GenerateDailyMissionUseCase

LevelUpCharacterUseCase
```

---

O módulo Game nunca deve conhecer detalhes da interface.

Toda comunicação ocorre através de:

- Facades;
- Domain Events;
- Repositories.

---

# 49. Reports Use Cases

O módulo Reports centraliza geração de relatórios e exportações.

Responsabilidades:

- gerar PDF;
- gerar CSV;
- gerar Excel;
- exportar Dashboard;
- exportar Analytics.

---

## Exemplos

```text
GenerateDashboardReportUseCase

ExportWorkoutHistoryUseCase

ExportReadingHistoryUseCase

ExportHealthDataUseCase

GenerateWeeklySummaryReportUseCase
```

---

Os Use Cases de relatório nunca devem gerar arquivos diretamente.

Eles delegam para:

```text
ReportExporter

PdfExporter

CsvExporter

ExcelExporter
```

---

# 50. Administração Use Cases

O módulo Administration reúne funcionalidades administrativas da plataforma.

Responsabilidades:

- gerenciamento de usuários;
- auditoria;
- configurações globais;
- manutenção;
- monitoramento;
- métricas operacionais.

---

## Exemplos

```text
ListUsersUseCase

DeactivateUserUseCase

UnlockUserUseCase

GetAuditLogUseCase

GetSystemMetricsUseCase

UpdateSystemConfigurationUseCase
```

---

Esses Use Cases possuem regras adicionais:

- autenticação obrigatória;
- autorização obrigatória;
- verificação de permissões;
- registro de auditoria;
- rastreabilidade completa.

Nenhum Use Case administrativo pode ser reutilizado pela interface comum do usuário final.

---

# 51. Query Use Cases

Query Use Cases representam operações exclusivamente de leitura.

Seu objetivo é recuperar informações para a interface sem modificar o estado do sistema.

Características:

- não alteram dados;
- não executam regras de negócio de escrita;
- não geram eventos;
- não iniciam transações de escrita;
- podem utilizar Read Models especializados.

---

## Exemplos

```text
GetDashboardUseCase

GetCharacterSheetUseCase

GetWorkoutHistoryUseCase

GetReadingStatisticsUseCase

GetAnalyticsSummaryUseCase
```

---

Fluxo:

```text
Controller

↓

Query Use Case

↓

Query Repository

↓

Read Model

↓

Presenter

↓

UI
```

---

Query Use Cases devem priorizar desempenho, utilizando consultas otimizadas e modelos específicos de leitura.

---

# 52. Command Use Cases

Command Use Cases representam operações que modificam o estado do sistema.

Características:

- criam registros;
- atualizam registros;
- removem registros;
- publicam eventos;
- executam regras de domínio;
- utilizam Unit of Work.

---

## Exemplos

```text
RegisterWorkoutUseCase

CreateCharacterUseCase

CompleteHabitUseCase

GrantExperienceUseCase

ResetPasswordUseCase
```

---

Fluxo:

```text
Controller

↓

Command

↓

Use Case

↓

Domain

↓

Repositories

↓

Commit

↓

Publish Events

↓

Result
```

---

Todo Command Use Case deve ser transacional.

---

# 53. CQRS Light

O LifeOS adota oficialmente **CQRS Light**.

Existe separação lógica entre:

```text
Commands
```

e

```text
Queries
```

Porém:

- utilizam o mesmo banco de dados;
- compartilham o mesmo domínio;
- compartilham a mesma infraestrutura.

---

Estrutura:

```text
application/

commands/

queries/

use_cases/
```

---

Benefícios:

- melhor organização;
- consultas otimizadas;
- código mais legível;
- escalabilidade futura;
- facilidade para evolução para CQRS completo.

---

# 54. Testes Unitários

Todo Use Case deve possuir testes unitários.

Os testes devem validar:

- fluxo principal;
- regras de aplicação;
- erros esperados;
- chamadas aos serviços;
- integração com Domain.

---

Dependências utilizadas:

- InMemory Repository;
- Fake Unit of Work;
- Fake Event Publisher;
- Fake Clock;
- Fake Provider.

---

Nunca depender de:

- banco real;
- Streamlit;
- SMTP;
- IA;
- arquivos.

---

Exemplo:

```python
def test_register_workout():
    ...
```

---

# 55. Testes de Integração

Testes de integração validam a comunicação entre componentes reais.

Devem validar:

- SQLAlchemy;
- banco;
- mapeamentos;
- persistência;
- transações;
- Unit of Work;
- Events;
- Repositories.

---

Exemplos

```text
RegisterWorkoutUseCaseIntegrationTest

RegisterUserUseCaseIntegrationTest

GenerateDashboardUseCaseIntegrationTest
```

---

Esses testes utilizam infraestrutura real controlada.

---

# 56. Testes Multi-Tenant

Todo Use Case operacional deve possuir teste específico de isolamento entre usuários.

Exemplo:

```text
Usuário A cria treino

↓

Usuário B consulta histórico

↓

Treino não aparece
```

---

Casos obrigatórios:

- leitura;
- atualização;
- exclusão;
- exportação;
- analytics.

---

O isolamento entre usuários é um requisito arquitetural obrigatório.

---

# 57. Testes de Contrato

Use Cases que dependem de Ports devem possuir testes de contrato.

Exemplos:

```text
AIProvider

EmailSender

PasswordHasher

TokenGenerator
```

---

Todas as implementações devem obedecer exatamente ao mesmo contrato.

Exemplo:

```text
GeminiAIProvider

OpenAIProvider

LocalLLMProvider
```

---

O comportamento deve permanecer consistente independentemente da implementação.

---

# 58. Testes de Segurança

Os testes devem validar:

- autenticação;
- autorização;
- ownership;
- Multi-Tenant;
- acesso negado;
- sessão expirada;
- token inválido;
- permissões administrativas.

---

Também devem validar tentativas de:

- acesso cruzado;
- manipulação de IDs;
- replay;
- elevação de privilégio.

---

Nenhum Use Case crítico deve ser considerado concluído sem testes de segurança.

---

# 59. Anti-patterns

São proibidos.

---

## Use Case Gigante

```text
1000 linhas
```

---

## SQL dentro do Use Case

```python
SELECT ...
```

---

## ORM dentro do Use Case

```python
WorkoutModel
```

---

## Streamlit dentro do Use Case

```python
st.button(...)
```

---

## Regra de domínio dentro do Use Case

```python
xp = duration * 8
```

---

## Instanciar infraestrutura

```python
GeminiProvider()
```

---

## Commit manual

```python
session.commit()
```

---

## Retornar Entity para UI

```python
return Character
```

---

## Usar dicionários genéricos

```python
return {
    ...
}
```

---

Todos esses padrões são proibidos pela arquitetura oficial.

---

# 60. Como o Gemini deve Utilizar este Documento

Antes de gerar qualquer Use Case, o agente deve responder:

1. Qual é a intenção do usuário?
2. Esse fluxo pertence à Application?
3. Existe um Aggregate responsável?
4. Existe Domain Service?
5. Existe Policy?
6. Existe Specification?
7. Existe Repository?
8. Existe Unit of Work?
9. Existe Event?
10. Existe Multi-Tenant?
11. O retorno será um Result?
12. Há testes necessários?
13. Existe Facade pública?
14. Há integração entre módulos?
15. A documentação continua consistente?

Somente após responder essas perguntas o código poderá ser gerado.

---

# 61. Checklist de Implementação

Antes de considerar um Use Case concluído:

- [ ] Responsabilidade única.
- [ ] Nome correto.
- [ ] Command criado.
- [ ] Result criado.
- [ ] DTOs definidos.
- [ ] Repository utilizado.
- [ ] Domain Service utilizado quando necessário.
- [ ] Policy utilizada quando necessária.
- [ ] Specification utilizada quando necessária.
- [ ] Unit of Work aplicada.
- [ ] Eventos publicados após commit.
- [ ] Multi-Tenant garantido.
- [ ] Tratamento de erros implementado.
- [ ] Testes unitários criados.
- [ ] Testes de integração criados.
- [ ] Testes de segurança criados.
- [ ] Documentação atualizada.

---

# 62. Critérios de Aceite

Um Use Case será considerado aceito quando:

- representar uma única intenção do usuário;
- respeitar a Clean Architecture;
- utilizar apenas contratos;
- preservar isolamento Multi-Tenant;
- não depender de infraestrutura concreta;
- publicar eventos corretamente;
- utilizar Unit of Work;
- possuir testes automatizados;
- retornar DTO imutável;
- possuir documentação correspondente.

---

# 63. Definition of Done

Um Use Case somente será considerado concluído quando:

- [ ] Implementação concluída.
- [ ] Revisão arquitetural aprovada.
- [ ] Revisão de código aprovada.
- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados.
- [ ] Testes de segurança aprovados.
- [ ] Cobertura mínima atingida.
- [ ] Multi-Tenant validado.
- [ ] Eventos validados.
- [ ] Performance analisada.
- [ ] Logs revisados.
- [ ] Documentação sincronizada.

Nenhum Use Case deve entrar em produção sem atender integralmente à Definition of Done.

---

# 64. Declaração Final

Os Use Cases constituem a espinha dorsal da camada **Application** do LifeOS.

Eles representam todas as capacidades do sistema e definem como o domínio é utilizado para atender às intenções dos usuários.

Todo Use Case deve ser:

- pequeno;
- coeso;
- previsível;
- testável;
- desacoplado;
- orientado ao domínio;
- independente de tecnologia;
- seguro;
- transacional quando necessário;
- compatível com Multi-Tenant.

Ao seguir este documento, garante-se que toda a camada de aplicação permaneça consistente, escalável e preparada para evolução contínua, permitindo que desenvolvedores e agentes de IA implementem novas funcionalidades mantendo o mesmo padrão arquitetural do LifeOS.
