# FOLDER_STRUCTURE

## LifeOS

**Versão:** 1.0

**Status:** Documento Oficial

**Documento:** Estrutura Física do Repositório

---

# 1. Objetivo

Este documento define a estrutura oficial de diretórios e arquivos do código-fonte do **LifeOS**.

Seu propósito é garantir que:

- cada artefato seja criado no local correto;
- todos os módulos utilizem a mesma organização;
- desenvolvedores e agentes de IA encontrem rapidamente o código;
- as fronteiras definidas pela Clean Architecture e pelo Monólito Modular sejam preservadas;
- o projeto cresça sem perder consistência estrutural.

A estrutura definida neste documento é **obrigatória** para novas implementações.

---

# 2. Escopo

Este documento especifica:

- estrutura da raiz do repositório;
- organização do código-fonte;
- organização interna dos módulos;
- localização de Entities, Value Objects, Use Cases e Repositories;
- localização das interfaces Streamlit;
- localização de configurações e serviços compartilhados;
- estrutura de testes;
- estrutura de documentação;
- convenções para criação de arquivos e diretórios.

Este documento **não define**:

- regras de negócio;
- modelos de banco de dados;
- detalhes visuais.

---

# 3. Princípios Estruturais

A estrutura do projeto deverá refletir diretamente a arquitetura oficial.

Os princípios obrigatórios são:

- Organização principal por módulo de negócio.
- Cada módulo implementa sua própria Clean Architecture.
- O domínio permanece isolado de frameworks.
- A interface Streamlit não contém regras de negócio.
- Implementações de infraestrutura não ficam no domínio.
- Testes acompanham as mesmas fronteiras dos módulos.
- Código compartilhado deve ser mínimo e tecnicamente neutro.
- Nenhum módulo acessa diretamente arquivos internos de outro módulo.
- Cada arquivo deve possuir uma responsabilidade principal.
- A estrutura deve permitir novas interfaces sem alterar o domínio.

---

# 4. Estrutura Geral do Repositório

```text
lifeos/
├── src/
│   └── lifeos/
│       ├── modules/
│       ├── interfaces/
│       ├── infrastructure/
│       ├── shared/
│       ├── bootstrap/
│       └── __init__.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── architecture/
│   ├── end_to_end/
│   ├── fixtures/
│   └── conftest.py
│
├── docs/
│   ├── 00_FOUNDATION/
│   ├── 01_PRODUCT/
│   ├── 02_ARCHITECTURE/
│   ├── 03_DATABASE/
│   ├── 04_BACKEND/
│   ├── 05_FRONTEND/
│   ├── 06_GAME_ENGINE/
│   ├── 07_ANALYTICS/
│   ├── 08_AI/
│   ├── 09_TESTS/
│   ├── 10_AI_ENGINEERING/
│   └── 99_REFERENCE/
│
├── assets/
│   ├── images/
│   ├── icons/
│   ├── fonts/
│   └── styles/
│
├── data/
│   ├── database/
│   ├── exports/
│   └── backups/
│
├── logs/
│   └── .gitkeep
│
├── scripts/
│   ├── initialize_database.py
│   ├── seed_database.py
│   ├── create_backup.py
│   └── validate_architecture.py
│
├── migrations/
│
├── .env.example
├── .gitignore
├── app.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 5. Diretório `src`

O diretório **src** contém exclusivamente o código-fonte da aplicação.

```text
src/
└── lifeos/
```

A utilização do layout **src** evita imports acidentais a partir da raiz do repositório e melhora a confiabilidade dos testes e do empacotamento.

O pacote principal será:

```text
lifeos
```

---

# 6. Estrutura Principal do Pacote `lifeos`

```text
src/lifeos/
├── modules/
├── interfaces/
├── infrastructure/
├── shared/
├── bootstrap/
└── __init__.py
```

## Responsabilidades

| Diretório | Responsabilidade |
|-----------|------------------|
| `modules` | Módulos de negócio e suas camadas internas |
| `interfaces` | Pontos de entrada externos da aplicação |
| `infrastructure` | Recursos técnicos compartilhados |
| `shared` | Kernel mínimo compartilhado |
| `bootstrap` | Inicialização e composição da aplicação |

---

# 7. Diretório `modules`

O diretório **modules** contém os módulos funcionais oficiais do LifeOS.

```text
src/lifeos/modules/
├── auth/
├── character/
├── health/
├── workout/
├── reading/
├── therapy/
├── habits/
├── game/
├── dashboard/
├── analytics/
├── ai/
├── reports/
└── admin/
```

Cada diretório representa um **Bounded Context** ou módulo funcional definido na documentação oficial.

---

# 8. Estrutura Interna Padrão de um Módulo

Todos os módulos devem seguir a mesma estrutura-base.

```text
module_name/
├── application/
│   ├── commands/
│   ├── queries/
│   ├── use_cases/
│   ├── dto/
│   ├── mappers/
│   ├── services/
│   └── ports/
│
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── aggregates/
│   ├── repositories/
│   ├── services/
│   ├── events/
│   ├── policies/
│   ├── specifications/
│   ├── factories/
│   └── exceptions/
│
├── infrastructure/
│   ├── persistence/
│   ├── repositories/
│   ├── models/
│   ├── mappers/
│   └── adapters/
│
├── presentation/
│   ├── controllers/
│   ├── view_models/
│   └── presenters/
│
├── public/
│   ├── facade.py
│   ├── contracts.py
│   └── events.py
│
└── __init__.py
```

> Diretórios vazios não precisam ser criados antecipadamente. Eles devem ser adicionados quando existir um artefato real correspondente.

---

# 9. Camada `application`

```text
application/
├── commands/
├── queries/
├── use_cases/
├── dto/
├── mappers/
├── services/
└── ports/
```

---

## 9.1 `commands`

Contém objetos que representam intenção de alteração de estado.

### Exemplos

```text
register_user_command.py
register_workout_command.py
grant_experience_command.py
complete_quest_command.py
```

### Exemplo

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterWorkoutCommand:
    user_id: str
    workout_type_id: str
    occurred_at: str
    average_heart_rate: int | None
    perceived_effort: int
```

**Commands** devem ser imutáveis sempre que possível.

---

## 9.2 `queries`

Contém objetos e handlers responsáveis por leitura.

### Exemplos

```text
get_character_sheet_query.py
list_workouts_query.py
get_dashboard_summary_query.py
search_reading_notes_query.py
```

Queries **não devem alterar** o estado do domínio.

---

## 9.3 `use_cases`

Contém os casos de uso executáveis.

### Exemplos

```text
register_user.py
authenticate_user.py
register_sleep.py
register_workout.py
complete_habit.py
calculate_global_level.py
```

Cada arquivo deve representar um caso de uso principal.

### Exemplo

```python
class RegisterWorkoutUseCase:

    def execute(
        self,
        command: RegisterWorkoutCommand
    ) -> RegisterWorkoutResult:
        ...
```

---

## 9.4 `dto`

Contém objetos de transporte entre camadas.

### Exemplos

```text
user_dto.py
character_sheet_dto.py
workout_dto.py
dashboard_dto.py
```

DTOs:

- não possuem regras de negócio;
- não representam tabelas;
- não substituem Entities;
- podem ser específicos de entrada ou saída.

Convenção recomendada:

```text
register_workout_input.py
register_workout_output.py
```

---

## 9.5 `mappers`

Converte objetos entre fronteiras.

### Exemplos

```text
character_dto_mapper.py
workout_dto_mapper.py
dashboard_mapper.py
```

Conversões permitidas:

- Entity → DTO
- DTO → Command
- Query Result → ViewModel

Mappers **não contêm regras de negócio**.

---

## 9.6 `services`

Contém serviços de aplicação que coordenam múltiplos casos de uso ou integrações.

### Exemplos

```text
account_initialization_service.py
character_progression_application_service.py
dashboard_composition_service.py
```

Não deve duplicar regras que pertencem ao domínio.

---

## 9.7 `ports`

Define contratos necessários para serviços externos.

### Exemplos

```text
email_sender.py
password_hasher.py
token_generator.py
clock.py
transaction_manager.py
```

### Exemplo

```python
from typing import Protocol


class PasswordHasher(Protocol):

    def hash(self, raw_password: str) -> str:
        ...

    def verify(
        self,
        raw_password: str,
        hashed_password: str
    ) -> bool:
        ...
```

As implementações ficam em **infrastructure**.

---

# 10. Camada `domain`

```text
domain/
├── entities/
├── value_objects/
├── aggregates/
├── repositories/
├── services/
├── events/
├── policies/
├── specifications/
├── factories/
└── exceptions/
```

Esta camada **não pode importar**:

- Streamlit
- SQLAlchemy
- SQLite
- Plotly
- pandas
- qualquer framework externo de infraestrutura

---

## 10.1 `entities`

Contém as **Entities** do domínio.

### Exemplos

```text
user.py
character.py
workout.py
book.py
habit.py
quest.py
```

As Entities possuem:

- identidade;
- comportamento;
- invariantes;
- ciclo de vida.

### Exemplo

```python
class Character:

    def grant_experience(
        self,
        amount: ExperiencePoints
    ) -> None:
        ...
```

---

## 10.2 `value_objects`

Contém objetos imutáveis comparados por valor.

### Exemplos

```text
email.py
experience_points.py
level.py
weight.py
height.py
percentage.py
heart_rate.py
date_range.py
```

### Exemplo

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperiencePoints:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(
                "Experience points cannot be negative."
            )
```

---

## 10.3 `aggregates`

Contém **Aggregate Roots** e estruturas internas de agregação quando a separação for necessária.

### Exemplos

```text
character_aggregate.py
user_account_aggregate.py
quest_aggregate.py
```

Não é obrigatório duplicar uma Entity em **entities** e **aggregates**.

Quando uma Entity for a própria **Aggregate Root**, ela deverá possuir uma única definição.

---

## 10.4 `repositories`

Contém somente interfaces ou protocolos de persistência.

### Exemplos

```text
user_repository.py
character_repository.py
workout_repository.py
quest_repository.py
```

### Exemplo

```python
from typing import Protocol


class CharacterRepository(Protocol):

    def find_by_user_id(
        self,
        user_id: str
    ) -> Character | None:
        ...

    def save(
        self,
        character: Character
    ) -> None:
        ...
```

Nenhuma implementação concreta pertence a esta pasta.

---

## 10.5 `services`

Contém **Domain Services**.

### Exemplos

```text
experience_calculation_service.py
character_evolution_service.py
quest_completion_service.py
recovery_score_service.py
```

Devem representar regras de negócio que não pertencem naturalmente a uma única Entity.

---

## 10.6 `events`

Contém eventos internos do domínio.

### Exemplos

```text
user_registered.py
workout_registered.py
experience_granted.py
level_increased.py
achievement_unlocked.py
```

Os eventos devem ser nomeados no passado, pois representam fatos ocorridos.

---

## 10.7 `policies`

Contém regras variáveis ou estratégias de negócio.

### Exemplos

```text
experience_policy.py
streak_policy.py
reward_policy.py
password_policy.py
```

As **Policies** permitem substituir regras sem alterar as Entities principais.

---

## 10.8 `specifications`

Contém regras booleanas reutilizáveis.

### Exemplos

```text
eligible_for_level_up.py
quest_completion_specification.py
achievement_unlock_specification.py
```

---

## 10.9 `factories`

Contém criação complexa de objetos do domínio.

### Exemplos

```text
character_factory.py
quest_factory.py
achievement_factory.py
```

As **Factories** devem assegurar a criação de objetos válidos.

---

## 10.10 `exceptions`

Contém exceções específicas do domínio.

### Exemplos

```text
invalid_experience_error.py
quest_already_completed_error.py
email_already_registered_error.py
```

Exceções técnicas de banco ou rede não pertencem a esta pasta.

---

# 11. Camada `infrastructure` do Módulo

```text
infrastructure/
├── persistence/
├── repositories/
├── models/
├── mappers/
└── adapters/
```

---

## 11.1 `persistence`

Contém configurações ou objetos de persistência específicos do módulo.

### Exemplos

```text
tables.py
unit_of_work.py
database_queries.py
```

SQL textual só pode existir aqui quando não for possível utilizar adequadamente o ORM e deve ser explicitamente justificado.

---

## 11.2 `repositories`

Contém implementações concretas dos contratos de domínio.

### Exemplos

```text
sqlalchemy_user_repository.py
sqlalchemy_character_repository.py
sqlalchemy_workout_repository.py
```

Convenção obrigatória:

```text
<technology>_<aggregate>_repository.py
```

---

## 11.3 `models`

Contém modelos do ORM.

### Exemplos

```text
user_model.py
character_model.py
workout_model.py
```

Os modelos do SQLAlchemy:

- não são Entities de domínio;
- não devem possuir regras de negócio.

---

## 11.4 `mappers`

Converte modelos de persistência e objetos do domínio.

### Exemplos

```text
user_persistence_mapper.py
character_persistence_mapper.py
workout_persistence_mapper.py
```

Fluxo permitido:

```text
SQLAlchemy Model ↔ Domain Entity
```

---

## 11.5 `adapters`

Implementa os **Ports** definidos em `domain/ports` para Repositories de
Aggregates ou em `application/ports` para orquestração e integrações de casos de
uso. Adapters concretos permanecem na Infrastructure.

### Exemplos

```text
bcrypt_password_hasher.py
smtp_email_sender.py
secure_token_generator.py
system_clock.py
```

---

# 12. Camada `presentation` do Módulo

```text
presentation/
├── controllers/
├── view_models/
└── presenters/
```

Essa camada adapta entradas e saídas sem depender de uma tecnologia visual específica.

---

## 12.1 `controllers`

Recebem solicitações da interface e chamam os Use Cases.

### Exemplos

```text
register_user_controller.py
register_workout_controller.py
character_sheet_controller.py
```

Os Controllers:

- validam o formato da entrada;
- constroem Commands ou Queries;
- executam Use Cases;
- convertem erros para respostas apropriadas.

Não contêm regras de domínio.

---

## 12.2 `view_models`

Contêm dados preparados para exibição.

### Exemplos

```text
character_sheet_view_model.py
workout_history_view_model.py
dashboard_view_model.py
```

Os ViewModels podem conter formatação de apresentação, mas não cálculos de negócio.

---

## 12.3 `presenters`

Convertem resultados dos casos de uso em formatos adequados para a interface.

### Exemplos

```text
character_sheet_presenter.py
validation_error_presenter.py
```

---

# 13. Diretório `public`

```text
public/
├── facade.py
├── contracts.py
└── events.py
```

Este diretório define a superfície pública do módulo.

Outros módulos só podem utilizar elementos expostos por **public**.

---

## 13.1 `facade.py`

Expõe operações síncronas oficiais do módulo.

### Exemplo

```python
class CharacterModuleFacade:

    def get_character_summary(
        self,
        user_id: str
    ) -> CharacterSummary:
        ...

    def grant_experience(
        self,
        command: GrantExperienceCommand
    ) -> None:
        ...
```

---

## 13.2 `contracts.py`

Contém contratos públicos e objetos de integração.

### Exemplos

```text
CharacterSummary
ExperienceGrantRequest
UserIdentity
WorkoutSummary
```

Os contratos públicos não devem expor Entities internas.

---

## 13.3 `events.py`

Expõe eventos públicos que outros módulos podem consumir.

### Exemplos

```text
CharacterCreatedEvent
WorkoutRegisteredEvent
LevelIncreasedEvent
```

Os eventos públicos devem ser estáveis e versionáveis.

---

# 14. Interfaces da Aplicação

As interfaces ficam fora dos módulos de negócio.

```text
src/lifeos/interfaces/
├── streamlit/
├── api/
└── cli/
```

Na versão inicial, somente **streamlit** será implementado.

---

# 15. Estrutura da Interface Streamlit

```text
src/lifeos/interfaces/streamlit/
├── app.py
├── navigation/
├── pages/
├── components/
├── layouts/
├── state/
├── themes/
├── forms/
├── presenters/
└── assets/
```

---

## 15.1 `navigation`

Contém roteamento e proteção de páginas.

### Exemplos

```text
router.py
route_guard.py
menu_builder.py
```

---

## 15.2 `pages`

Contém páginas Streamlit.

### Exemplos

```text
login_page.py
register_page.py
character_dashboard_page.py
sleep_page.py
workout_page.py
reading_page.py
therapy_page.py
habits_page.py
reports_page.py
```

As páginas devem apenas:

- renderizar;
- coletar entrada;
- chamar Controllers;
- apresentar resultados.

---

## 15.3 `components`

Contém componentes reutilizáveis.

### Exemplos

```text
character_card.py
experience_bar.py
attribute_radar.py
metric_card.py
quest_card.py
achievement_badge.py
```

---

## 15.4 `layouts`

Contém estruturas visuais compartilhadas.

### Exemplos

```text
authenticated_layout.py
public_layout.py
character_sheet_layout.py
```

---

## 15.5 `state`

Contém gerenciamento de sessão da interface.

### Exemplos

```text
session_state.py
authentication_state.py
navigation_state.py
```

A sessão do Streamlit não substitui o modelo de autenticação do domínio.

---

## 15.6 `themes`

Contém configuração de tema e estilos visuais.

### Exemplos

```text
theme.py
classic_rpg_theme.py
css_loader.py
```

---

## 15.7 `forms`

Contém componentes de formulário reutilizáveis.

### Exemplos

```text
login_form.py
register_user_form.py
workout_form.py
sleep_form.py
```

---

# 16. Infraestrutura Compartilhada

```text
src/lifeos/infrastructure/
├── database/
├── configuration/
├── logging/
├── security/
├── email/
├── backup/
├── events/
├── cache/
└── observability/
```

Este diretório contém recursos técnicos compartilhados por mais de um módulo.

---

## 16.1 `database`

```text
database/
├── engine.py
├── session_factory.py
├── transaction_manager.py
├── metadata.py
├── migrations.py
└── health_check.py
```

---

## 16.2 `configuration`

```text
configuration/
├── settings.py
├── environment.py
└── paths.py
```

---

## 16.3 `logging`

```text
logging/
├── logger_factory.py
├── log_config.py
└── audit_logger.py
```

---

## 16.4 `security`

```text
security/
├── password_hasher.py
├── token_service.py
└── encryption_service.py
```

---

## 16.5 `email`

```text
email/
├── smtp_email_sender.py
├── templates/
└── email_config.py
```

---

## 16.6 `backup`

```text
backup/
├── backup_service.py
├── restore_service.py
└── retention_policy.py
```

---

## 16.7 `events`

```text
events/
├── event_bus.py
├── event_handler.py
└── event_registry.py
```

---

# 17. Shared Kernel

```text
src/lifeos/shared/
├── domain/
├── application/
├── types/
├── errors/
├── constants/
└── utilities/
```

O **Shared Kernel** deve permanecer mínimo.

## Conteúdo permitido

- identificadores genéricos;
- base de Domain Event;
- tipo Result;
- paginação;
- erros genéricos;
- relógio abstrato;
- utilitários sem regra de negócio.

## Conteúdo proibido

- regras de XP;
- regras de Character;
- regras de saúde;
- Entities compartilhadas;
- Use Cases;
- lógica específica de módulos.

> Quando um elemento for usado por apenas um módulo, deverá permanecer nesse módulo.

---

# 18. Bootstrap e Composition Root

```text
src/lifeos/bootstrap/
├── application.py
├── container.py
├── module_registry.py
├── event_handlers.py
└── startup.py
```

O bootstrap é responsável por:

- criar dependências;
- configurar banco;
- registrar Repositories;
- registrar Use Cases;
- configurar Event Bus;
- inicializar módulos;
- iniciar a interface.

O arquivo **container.py** será o **Composition Root oficial**.

Nenhum módulo deverá criar diretamente suas dependências concretas.

---

# 19. Arquivo de Entrada

Na raiz do projeto:

```text
app.py
```

Responsabilidade exclusiva:

- carregar configuração;
- inicializar o bootstrap;
- iniciar a interface Streamlit.

### Exemplo

```python
from lifeos.bootstrap.startup import start_streamlit_application


if __name__ == "__main__":
    start_streamlit_application()
```

O arquivo não deve conter:

- regras de negócio;
- consultas;
- composição complexa de interface.

---

# 20. Estrutura de Testes

```text
tests/
├── unit/
│   ├── modules/
│   ├── shared/
│   └── infrastructure/
│
├── integration/
│   ├── modules/
│   ├── database/
│   └── events/
│
├── architecture/
│   ├── test_dependency_rules.py
│   ├── test_module_boundaries.py
│   └── test_domain_independence.py
│
├── end_to_end/
│   ├── test_registration_flow.py
│   ├── test_authentication_flow.py
│   └── test_workout_progression_flow.py
│
├── fixtures/
└── conftest.py
```

---

## 20.1 Testes Unitários

Devem espelhar a organização dos módulos.

### Exemplo

```text
tests/unit/modules/character/domain/
tests/unit/modules/character/application/
```

---

## 20.2 Testes de Integração

Validam:

- Repositories;
- banco de dados;
- transações;
- Event Bus;
- integrações técnicas.

---

## 20.3 Testes Arquiteturais

Garantem automaticamente:

- domínio sem import de framework;
- UI sem acesso direto ao banco;
- módulos sem dependências proibidas;
- ausência de importações circulares.

---

## 20.4 Testes End-to-End

Validam fluxos completos do produto.

Devem ser reservados para jornadas críticas.

---

# 21. Diretório de Dados

```text
data/
├── database/
│   └── database.db
├── exports/
└── backups/
```

Arquivos gerados durante a execução não devem ficar dentro de **src**.

---

# 22. Diretório de Assets

```text
assets/
├── images/
├── icons/
├── fonts/
└── styles/
```

Arquivos de referência da documentação devem permanecer em:

```text
docs/99_REFERENCE/
```

Assets da aplicação devem permanecer em:

```text
assets/
```

---

# 23. Diretório de Logs

```text
logs/
└── application.log
```

Os logs não devem ser versionados.

O diretório pode conter um arquivo:

```text
.gitkeep
```

---

# 24. Diretório de Scripts

```text
scripts/
├── initialize_database.py
├── seed_database.py
├── create_backup.py
├── restore_backup.py
├── validate_architecture.py
└── run_quality_checks.py
```

Os scripts não devem duplicar regras de negócio.

Eles devem chamar serviços ou componentes oficiais da aplicação.

---

# 25. Migrations

```text
migrations/
├── versions/
├── env.py
└── README.md
```

Toda alteração de schema deve possuir uma migration versionada.

O código da aplicação não deve executar alterações improvisadas no schema.

---

# 26. Exemplo Completo do Módulo Character

```text
src/lifeos/modules/character/
├── application/
│   ├── commands/
│   │   └── grant_experience_command.py
│   ├── queries/
│   │   └── get_character_sheet_query.py
│   ├── use_cases/
│   │   ├── create_character.py
│   │   ├── grant_experience.py
│   │   └── get_character_sheet.py
│   ├── dto/
│   │   ├── character_dto.py
│   │   └── character_sheet_dto.py
│   ├── mappers/
│   │   └── character_dto_mapper.py
│   ├── services/
│   │   └── character_application_service.py
│   └── ports/
│       └── transaction_manager.py
│
├── domain/
│   ├── entities/
│   │   ├── character.py
│   │   └── attribute.py
│   ├── value_objects/
│   │   ├── experience_points.py
│   │   └── level.py
│   ├── repositories/
│   │   └── character_repository.py
│   ├── services/
│   │   └── character_evolution_service.py
│   ├── events/
│   │   ├── character_created.py
│   │   ├── experience_granted.py
│   │   └── level_increased.py
│   ├── policies/
│   │   └── level_progression_policy.py
│   ├── specifications/
│   │   └── eligible_for_level_up.py
│   ├── factories/
│   │   └── character_factory.py
│   └── exceptions/
│       └── invalid_experience_error.py
│
├── infrastructure/
│   ├── models/
│   │   ├── character_model.py
│   │   └── attribute_model.py
│   ├── repositories/
│   │   └── sqlalchemy_character_repository.py
│   ├── mappers/
│   │   └── character_persistence_mapper.py
│   └── adapters/
│
├── presentation/
│   ├── controllers/
│   │   └── character_sheet_controller.py
│   ├── view_models/
│   │   └── character_sheet_view_model.py
│   └── presenters/
│       └── character_sheet_presenter.py
│
├── public/
│   ├── facade.py
│   ├── contracts.py
│   └── events.py
│
└── __init__.py
```

---

# 27. Convenções de Nomenclatura

## Diretórios e Arquivos

Utilizar **snake_case**.

### Exemplos

```text
character_sheet.py
register_workout.py
experience_calculation_service.py
```

---

## Classes

Utilizar **PascalCase**.

### Exemplos

```text
RegisterWorkoutUseCase
CharacterRepository
ExperiencePoints
```

---

## Funções e Métodos

Utilizar **snake_case**.

### Exemplos

```python
register_workout()
grant_experience()
find_by_user_id()
```

---

## Constantes

Utilizar **UPPER_SNAKE_CASE**.

### Exemplo

```python
MAX_PASSWORD_ATTEMPTS = 5
DEFAULT_BACKUP_RETENTION_DAYS = 30
```

---

## Interfaces e Protocolos

Não utilizar prefixos artificiais como:

```text
IRepository
```

Utilizar nomes de domínio:

```text
CharacterRepository
PasswordHasher
EmailSender
```

A implementação deve indicar a tecnologia utilizada.

### Exemplos

```text
SqlAlchemyCharacterRepository
BcryptPasswordHasher
SmtpEmailSender
```

---

# 28. Regras para Arquivos

Cada arquivo deve:

- possuir uma responsabilidade principal;
- conter classes fortemente relacionadas;
- evitar funções genéricas sem contexto;
- evitar dependências indiretas desnecessárias;
- possuir nome representativo;
- ser pequeno o suficiente para compreensão direta.

## Evitar arquivos genéricos como:

```text
helpers.py
utils.py
common.py
manager.py
misc.py
```

Quando realmente necessário, o nome deve indicar claramente o propósito.

---

# 29. Imports Permitidos

## Dentro de um módulo

```text
presentation → application
application  → domain
infrastructure → domain
public → application/contracts públicos
```

## Imports proibidos

```text
domain → infrastructure
domain → presentation
application → Streamlit
presentation → SQLAlchemy
module A → internals de module B
```

Essas regras serão detalhadas em **DEPENDENCY_RULES.md**.

---

# 30. Exposição entre Módulos

Um módulo nunca deverá importar diretamente:

```python
lifeos.modules.character.domain.entities.character
```

a partir de outro módulo.

## Acesso permitido

```python
lifeos.modules.character.public.facade
lifeos.modules.character.public.contracts
lifeos.modules.character.public.events
```

---

# 31. Critérios para Criar um Novo Diretório

Um novo diretório só deve ser criado quando:

- possuir responsabilidade clara;
- agrupar pelo menos dois artefatos relacionados ou possuir previsão concreta de expansão;
- estiver alinhado às camadas existentes;
- não duplicar uma categoria já existente.

Não criar pastas apenas para aparentar organização.

---

# 32. Critérios para Criar um Novo Módulo

Um novo módulo exige:

- Capability definida;
- Feature IDs;
- requisitos no PRD;
- Bounded Context identificável;
- regras próprias;
- dados próprios ou comportamento próprio;
- contratos públicos definidos;
- registro arquitetural quando necessário.

---

# 33. Como o Gemini deve utilizar este documento

Antes de criar ou mover qualquer arquivo, o agente deve:

1. identificar a Capability;
2. identificar o módulo;
3. identificar a camada;
4. identificar o tipo de artefato;
5. localizar o diretório oficial;
6. verificar se já existe artefato equivalente;
7. respeitar a API pública dos módulos;
8. criar ou atualizar os testes correspondentes.

O agente não deve inventar novos diretórios quando existir um local oficial adequado.

Ao concluir uma alteração deverá listar:

- arquivos criados;
- arquivos modificados;
- arquivos removidos;
- justificativa da localização de cada artefato.

---

# 34. Anti-patterns Estruturais

São proibidos:

```text
pages/
    database.py

streamlit/
    xp_calculator.py

domain/
    sqlalchemy_models.py

shared/
    gamification_service.py

modules/workout/
    imports internos de modules/health/
```

Também são proibidos:

- diretório **services** global contendo serviços de todos os módulos;
- diretório **models** global misturando domínio e ORM;
- diretório **repositories** global;
- páginas Streamlit na raiz;
- regras de negócio em scripts;
- arquivos de banco dentro da interface;
- Entities compartilhadas entre Bounded Contexts.

---

# 35. Diagrama Estrutural

> **A ser definido em versão posterior da documentação.**

---

# 36. Critérios de Aceite

Este documento será considerado atendido quando:

- a raiz do projeto seguir a estrutura oficial;
- todos os módulos estiverem dentro de `src/lifeos/modules`;
- todos os módulos respeitarem a estrutura interna padrão;
- as interfaces estiverem desacopladas dos módulos de negócio;
- os modelos SQLAlchemy estiverem separados das Entities;
- os contratos públicos forem utilizados na comunicação entre módulos;
- os testes refletirem as fronteiras da arquitetura;
- imports proibidos forem detectados por testes arquiteturais;
- nenhum código de negócio depender diretamente do Streamlit;
- nenhum módulo acessar diretamente os detalhes internos de outro.

---

# 37. Definition of Done Estrutural

Uma implementação somente poderá ser considerada estruturalmente concluída quando:

- Os arquivos estiverem nos diretórios corretos.
- A nomenclatura estiver padronizada.
- Não existirem imports proibidos.
- A API pública dos módulos estiver preservada.
- Os testes correspondentes estiverem organizados corretamente.
- Não existir regra de negócio fora do Domain ou Application.
- Não existir código de infraestrutura no Domain.
- A documentação relacionada estiver atualizada.

---

# 38. Declaração Final

A estrutura física do **LifeOS** deve representar com clareza sua arquitetura lógica.

A localização de um arquivo deve comunicar:

- a qual módulo ele pertence;
- qual camada representa;
- qual responsabilidade possui;
- quais dependências pode utilizar.

Qualquer estrutura que esconda essas informações ou enfraqueça as fronteiras modulares deverá ser considerada incompatível com a arquitetura oficial do **LifeOS**.
