# REPOSITORIES

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Repositories  
**Camadas Relacionadas:** Domain, Application e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal e Monólito Modular  
**Persistência Inicial:** SQLAlchemy + SQLite  
**Persistência Futura:** PostgreSQL

---

# 1. Objetivo

Este documento define o padrão oficial de Repositories do LifeOS.

Seu objetivo é estabelecer:

- o papel dos Repositories;
- onde seus contratos devem existir;
- onde suas implementações devem existir;
- como Aggregates devem ser persistidos;
- como o isolamento Multi-Tenant deve ser aplicado;
- como consultas, filtros, paginação e ordenação devem ser modelados;
- como SQLAlchemy deve ser isolado;
- como transações devem ser coordenadas;
- como Repositories devem ser testados;
- quais práticas são obrigatórias e quais são proibidas.

Toda implementação de persistência deverá seguir este documento.

---

# 2. Escopo

Este documento cobre:

- Repository Pattern;
- contratos de Repository;
- implementações concretas;
- Repositories de escrita;
- Repositories de leitura;
- CQRS Light;
- Aggregate Roots;
- Specifications;
- filtros;
- paginação;
- ordenação;
- consultas por período;
- consultas Multi-Tenant;
- Unit of Work;
- Persistence Mappers;
- tratamento de erros;
- performance;
- testes unitários;
- testes de contrato;
- testes de integração;
- regras para agentes de IA.

Este documento complementa:

- `DATABASE.md`;
- `ERD.md`;
- `SCHEMA.md`;
- `INDEXES.md`;
- `MIGRATIONS.md`;
- `02_ARCHITECTURE/02_CLEAN_ARCHITECTURE.md`;
- `02_ARCHITECTURE/03_DDD.md`;
- `02_ARCHITECTURE/HEXAGONAL.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`.

---

# 3. Definição

Repository é uma abstração responsável por fornecer acesso persistente aos Aggregates do domínio.

Ele deve oferecer ao restante da aplicação uma interface semelhante a uma coleção de objetos de domínio, ocultando:

- SQL;
- SQLAlchemy;
- Sessions;
- tabelas;
- joins;
- detalhes do banco;
- estratégias de cache;
- detalhes de persistência.

Exemplo conceitual:

```text
Application
    ↓
CharacterRepository
    ↓
SqlAlchemyCharacterRepository
    ↓
SQLite
```

---

# 4. Responsabilidade

Um Repository deve:

- localizar Aggregates;
- persistir Aggregates;
- atualizar Aggregates;
- remover logicamente quando aplicável;
- verificar existência;
- aplicar isolamento Multi-Tenant;
- executar consultas específicas do módulo;
- esconder detalhes de infraestrutura;
- participar da transação atual;
- retornar objetos adequados à camada consumidora.

Um Repository não deve:

- executar regras de negócio;
- calcular XP;
- validar progressão;
- iniciar casos de uso;
- montar componentes visuais;
- gerenciar sessão de usuário;
- enviar e-mails;
- gerar relatórios;
- realizar commit isolado;
- acessar módulos externos internamente.

---

# 5. Localização dos Contratos

Interfaces ou Protocols de Repository devem existir no Domain do módulo proprietário.

Estrutura:

```text
src/lifeos/modules/<module>/domain/repositories/
```

Exemplo:

```text
src/lifeos/modules/character/domain/repositories/
├── character_repository.py
└── character_history_repository.py
```

O Domain define o contrato.

A Infrastructure fornece a implementação.

---

# 6. Localização das Implementações

Implementações concretas devem existir na Infrastructure do módulo.

Estrutura:

```text
src/lifeos/modules/<module>/infrastructure/repositories/
```

Exemplo:

```text
src/lifeos/modules/character/infrastructure/repositories/
└── sqlalchemy_character_repository.py
```

---

# 7. Regra de Dependência

A direção oficial é:

```text
Infrastructure
    ↓
Domain Repository Contract
```

Nunca:

```text
Domain
    ↓
SQLAlchemy Repository
```

O Domain não pode importar implementações concretas.

A Application não pode instanciar implementações concretas.

A ligação ocorre no Composition Root.

---

# 8. Repository e Aggregate Root

Repositories devem trabalhar prioritariamente com Aggregate Roots.

Exemplo:

```text
CharacterRepository
```

persiste:

```text
Character Aggregate
```

Não criar Repository para cada tabela automaticamente.

Exemplo inadequado:

```text
CharacterAttributeRepository
```

quando `CharacterAttribute` for parte interna do Aggregate `Character`.

A existência de uma tabela não implica a existência de um Repository.

---

# 9. Critérios para Criar um Repository

Um Repository pode ser criado quando:

- existir Aggregate Root próprio;
- o objeto possuir ciclo de vida independente;
- houver necessidade de persistência isolada;
- o módulo for proprietário do dado;
- a abstração fizer sentido no domínio.

Não criar Repository para:

- Value Objects;
- DTOs;
- ViewModels;
- tabelas de junção internas sem comportamento;
- objetos derivados;
- cache temporário, salvo contrato técnico específico.

---

# 10. Contrato Básico

Exemplo oficial:

```python
from typing import Protocol

from lifeos.modules.character.domain.entities.character import Character
from lifeos.modules.character.domain.value_objects.character_id import CharacterId
from lifeos.modules.auth.domain.value_objects.user_id import UserId


class CharacterRepository(Protocol):
    def find_by_id(
        self,
        character_id: CharacterId,
        user_id: UserId,
    ) -> Character | None:
        ...

    def find_by_user_id(
        self,
        user_id: UserId,
    ) -> Character | None:
        ...

    def save(
        self,
        character: Character,
    ) -> None:
        ...

    def exists_for_user(
        self,
        user_id: UserId,
    ) -> bool:
        ...
```

---

# 11. Regras do Contrato

O contrato deve:

- usar tipos do domínio;
- usar identificadores explícitos;
- incluir `user_id` quando necessário;
- retornar Entity, Aggregate ou tipo de leitura;
- evitar tipos técnicos;
- evitar `dict` genérico;
- evitar `Any`;
- evitar Session;
- evitar SQLAlchemy Model;
- evitar `DataFrame`.

---

# 12. Nomenclatura

## Interface

```text
CharacterRepository
WorkoutRepository
BookRepository
HabitRepository
QuestRepository
```

## Implementação

```text
SqlAlchemyCharacterRepository
SqlAlchemyWorkoutRepository
SqlAlchemyBookRepository
```

## Arquivo

```text
character_repository.py
sqlalchemy_character_repository.py
```

Não utilizar prefixos artificiais:

```text
ICharacterRepository
CharacterRepositoryInterface
BaseCharacterDAO
```

---

# 13. Repository de Escrita

Repositories de escrita trabalham com Aggregates.

Operações comuns:

```text
save
find_by_id
exists
remove
```

Exemplo:

```python
class WorkoutRepository(Protocol):
    def find_by_id(
        self,
        workout_id: WorkoutId,
        user_id: UserId,
    ) -> Workout | None:
        ...

    def save(
        self,
        workout: Workout,
    ) -> None:
        ...

    def delete(
        self,
        workout: Workout,
    ) -> None:
        ...
```

---

# 14. Repository de Leitura

Consultas complexas podem utilizar interfaces específicas de leitura.

Exemplo:

```python
class CharacterSheetQueryRepository(Protocol):
    def get_character_sheet(
        self,
        user_id: UserId,
    ) -> CharacterSheetReadModel:
        ...
```

Esses Repositories:

- são somente leitura;
- podem retornar Read Models;
- podem executar joins;
- podem utilizar consultas otimizadas;
- não substituem Repositories de Aggregate;
- não retornam ORM Models.

---

# 15. CQRS Light

O LifeOS adota CQRS Light quando houver benefício real.

Separação:

```text
Command Side
    ↓
Aggregate Repository

Query Side
    ↓
Query Repository / Read Model
```

Exemplo:

```text
RegisterWorkoutUseCase
    ↓
WorkoutRepository
```

```text
GetWorkoutHistoryQuery
    ↓
WorkoutHistoryQueryRepository
```

---

# 16. Read Models

Read Models devem ser imutáveis.

Exemplo:

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkoutHistoryItem:
    workout_id: str
    workout_type_name: str
    occurred_at: datetime
    duration_minutes: int | None
    perceived_effort: int | None
```

Read Models:

- não possuem comportamento de domínio;
- não são persistidos como Entities;
- podem representar joins;
- podem ser específicos de tela ou relatório;
- devem permanecer independentes da UI.

---

# 17. Multi-Tenant

Toda consulta operacional deve aplicar isolamento por usuário.

Exemplo incorreto:

```python
def find_by_id(
    self,
    workout_id: WorkoutId,
) -> Workout | None:
    ...
```

Exemplo correto:

```python
def find_by_id(
    self,
    workout_id: WorkoutId,
    user_id: UserId,
) -> Workout | None:
    ...
```

---

# 18. Regra de Ownership

O Repository deve garantir que o dado retornado pertença ao usuário informado.

Exemplo:

```python
model = (
    self._session.query(WorkoutModel)
    .filter(
        WorkoutModel.id == str(workout_id),
        WorkoutModel.user_id == str(user_id),
        WorkoutModel.deleted_at.is_(None),
    )
    .one_or_none()
)
```

Nunca buscar por ID isoladamente em tabelas operacionais.

---

# 19. Identidade Autenticada

O `user_id` utilizado pelo Repository deve vir da Application Layer.

Fluxo:

```text
Session Adapter
    ↓
CurrentUserProvider
    ↓
Use Case
    ↓
Repository
```

Nunca obter `user_id` diretamente de:

- campo de formulário;
- query parameter não validado;
- variável global;
- cache compartilhado;
- estado interno do Repository.

---

# 20. Implementação SQLAlchemy

Exemplo:

```python
class SqlAlchemyCharacterRepository(CharacterRepository):
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def find_by_user_id(
        self,
        user_id: UserId,
    ) -> Character | None:
        model = (
            self._session.query(CharacterModel)
            .filter(CharacterModel.user_id == str(user_id))
            .one_or_none()
        )

        if model is None:
            return None

        return CharacterPersistenceMapper.to_domain(model)

    def save(
        self,
        character: Character,
    ) -> None:
        model = CharacterPersistenceMapper.to_model(character)
        self._session.merge(model)
```

---

# 21. Regra de Commit

Repositories não executam:

```python
self._session.commit()
```

Commit pertence ao Unit of Work.

O Repository pode:

- adicionar;
- atualizar;
- remover;
- executar `flush()` quando tecnicamente necessário e justificado.

---

# 22. Flush

`flush()` pode ser utilizado quando:

- o ID depende do banco;
- uma constraint precisa ser validada antes do fim;
- um relacionamento requer persistência intermediária;
- o Use Case precisa de dado gerado.

Como os IDs do LifeOS são gerados pela aplicação, o uso de `flush()` deve ser raro.

---

# 23. Rollback

Repositories não devem executar rollback por conta própria.

Rollback pertence ao Unit of Work.

Fluxo:

```text
Use Case
    ↓
Unit of Work
    ↓
Repository
    ↓
Exception
    ↓
Unit of Work Rollback
```

---

# 24. Persistence Mapper

Repositories concretos devem utilizar Persistence Mappers.

Exemplo:

```text
CharacterModel
    ↕
CharacterPersistenceMapper
    ↕
Character
```

O Repository não deve espalhar lógica de conversão.

---

# 25. Consulta por ID

Padrão:

```python
def find_by_id(
    self,
    aggregate_id: AggregateId,
    user_id: UserId,
) -> Aggregate | None:
    ...
```

A ausência deve retornar:

```text
None
```

O Use Case decide se isso representa erro.

---

# 26. Consulta Obrigatória

Quando o Repository oferecer método de consulta obrigatória, o nome deve ser explícito.

Exemplo:

```python
def get_by_id(
    self,
    aggregate_id: AggregateId,
    user_id: UserId,
) -> Aggregate:
    ...
```

Esse método pode lançar:

```text
AggregateNotFoundError
```

Não misturar semântica de `find` e `get`.

---

# 27. Convenção `find`, `get` e `exists`

```text
find_* → retorna objeto ou None
get_* → retorna objeto ou lança erro
exists_* → retorna bool
list_* → retorna coleção paginada ou sequência
count_* → retorna inteiro
```

---

# 28. Save

O método `save` deve funcionar para inclusão e atualização quando o ORM permitir.

Exemplo:

```python
def save(
    self,
    character: Character,
) -> None:
    ...
```

A regra de criação ou atualização pertence ao Aggregate e ao Use Case.

---

# 29. Delete

Excluir Aggregate deve utilizar método semanticamente adequado.

Possibilidades:

```text
delete
soft_delete
archive
deactivate
```

A escolha depende do domínio.

Não utilizar exclusão física por conveniência.

---

# 30. Soft Delete

Repositories devem omitir registros excluídos logicamente por padrão.

Exemplo:

```python
.filter(BookModel.deleted_at.is_(None))
```

Consultas administrativas explícitas podem incluir registros excluídos.

---

# 31. Filtros

Filtros complexos devem utilizar objetos explícitos.

Exemplo:

```python
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class WorkoutFilter:
    user_id: UserId
    start_date: date | None = None
    end_date: date | None = None
    workout_type_id: WorkoutTypeId | None = None
    minimum_effort: int | None = None
```

Evitar métodos com muitos parâmetros soltos.

---

# 32. Filtros Opcionais

O Repository concreto deve aplicar apenas filtros informados.

Exemplo:

```python
query = self._session.query(WorkoutModel).filter(
    WorkoutModel.user_id == str(filters.user_id)
)

if filters.start_date is not None:
    query = query.filter(
        WorkoutModel.occurred_at >= filters.start_date
    )

if filters.end_date is not None:
    query = query.filter(
        WorkoutModel.occurred_at <= filters.end_date
    )
```

---

# 33. Paginação

Listagens potencialmente grandes devem ser paginadas.

Contrato:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class PageRequest:
    page: int
    size: int


@dataclass(frozen=True)
class PageResult[T]:
    items: tuple[T, ...]
    page: int
    size: int
    total_items: int
    total_pages: int
```

---

# 34. Regras de Paginação

- página inicia em 1;
- tamanho deve possuir limite máximo;
- total deve ser calculado apenas quando necessário;
- ordenação deve ser determinística;
- parâmetros inválidos devem ser rejeitados;
- paginação deve respeitar Multi-Tenant.

---

# 35. Ordenação

Ordenação deve utilizar objeto explícito.

Exemplo:

```python
from dataclasses import dataclass
from enum import Enum


class SortDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True)
class Sort:
    field: str
    direction: SortDirection
```

Campos permitidos devem ser validados.

Nunca concatenar entrada livre em SQL.

---

# 36. Ordenação Determinística

Toda listagem deve possuir critério secundário.

Exemplo:

```text
occurred_at DESC, id DESC
```

Isso evita registros duplicados ou ausentes entre páginas.

---

# 37. Date Range

Consultas temporais devem utilizar Value Object ou filtro explícito.

Exemplo:

```python
@dataclass(frozen=True)
class DateRange:
    start: date
    end: date
```

Regra:

```text
start <= end
```

---

# 38. Specifications

Specifications podem representar critérios reutilizáveis do domínio.

Exemplo:

```text
ActiveHabitsSpecification
EligibleQuestsSpecification
CompletedBooksSpecification
```

O Repository pode traduzir uma Specification aprovada em consulta.

Não permitir Specification contendo SQLAlchemy diretamente no Domain.

---

# 39. Specification no Domain

Exemplo conceitual:

```python
class ActiveHabitSpecification:
    def is_satisfied_by(
        self,
        habit: Habit,
    ) -> bool:
        return habit.is_active
```

Para consultas persistentes complexas, utilizar filtros ou Query Repositories específicos.

---

# 40. Evitar Repository Genérico

Não criar um Repository genérico universal como:

```python
class BaseRepository[T]:
    def save(self, entity: T) -> None:
        ...
```

quando isso apagar a linguagem do domínio.

Preferir contratos específicos:

```text
CharacterRepository
WorkoutRepository
QuestRepository
```

Uma base técnica interna pode existir na Infrastructure, mas não deve se tornar API de domínio.

---

# 41. Base Repository Técnico

Pode existir internamente:

```python
class SqlAlchemyRepositoryBase:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
```

Essa base:

- não define operações genéricas de domínio;
- não é exposta à Application;
- não substitui contratos específicos;
- apenas reduz duplicação técnica segura.

---

# 42. Consultas Específicas

Métodos devem usar linguagem de domínio.

Correto:

```python
find_active_quests_for_user(...)
list_recent_workouts(...)
find_current_streak(...)
```

Evitar:

```python
find_by_field(...)
execute_query(...)
get_all(...)
```

---

# 43. `get_all`

`get_all()` é proibido em tabelas de crescimento contínuo.

Utilizar:

- paginação;
- filtro;
- período;
- limite explícito;
- consulta específica.

---

# 44. Contagem

Métodos de contagem devem ser específicos.

Exemplos:

```python
count_workouts_in_period(...)
count_completed_habits(...)
count_pages_read(...)
```

Não carregar registros para contar em memória.

---

# 45. Agregações

Agregações simples podem ocorrer em Query Repositories.

Exemplos:

- SUM;
- COUNT;
- AVG;
- MIN;
- MAX.

Regras de negócio derivadas devem permanecer no Domain ou Analytics.

---

# 46. Joins

Joins são permitidos em:

- Repositories concretos;
- Query Repositories;
- Infrastructure;
- Read Models.

Joins não devem vazar para o Domain.

---

# 47. N+1

Repositories devem evitar problema N+1.

Estratégias:

- eager loading controlado;
- `selectinload`;
- joins específicos;
- Read Models;
- consultas em lote.

Não carregar relações automaticamente sem necessidade.

---

# 48. Lazy Loading

Lazy loading deve ser evitado fora da transação.

Entities restauradas não devem depender de Session aberta para acessar dados.

O Aggregate deve ser reconstruído completamente dentro da fronteira necessária.

---

# 49. Consultas em Lote

Quando houver múltiplos IDs:

```python
def find_by_ids(
    self,
    ids: tuple[WorkoutId, ...],
    user_id: UserId,
) -> tuple[Workout, ...]:
    ...
```

Evitar executar uma consulta por item.

---

# 50. Cache

Repository não deve implementar cache de forma invisível sem contrato.

Se cache for necessário:

```text
CachedCharacterQueryRepository
```

ou Adapter decorador explícito.

O cache não pode comprometer isolamento Multi-Tenant.

---

# 51. Erros de Persistência

Erros técnicos devem ser traduzidos.

Exemplo:

```text
IntegrityError
    ↓
EmailAlreadyRegisteredPersistenceError
    ↓
Application Error
```

Não expor exceção SQLAlchemy diretamente para a UI.

---

# 52. Concorrência

Repositories devem considerar concorrência em operações críticas.

Exemplos:

- concessão de XP;
- atualização de Streak;
- conclusão de Quest;
- desbloqueio de Achievement;
- uso de token;
- criação única de Character.

Na versão SQLite, preservar transações curtas.

---

# 53. Idempotência

Operações dirigidas por evento devem verificar idempotência.

Exemplo:

```python
def exists_by_event_id(
    self,
    event_id: EventId,
) -> bool:
    ...
```

Uso:

```text
ExperienceTransaction
```

não deve ser criada duas vezes para o mesmo evento.

---

# 54. Repositories e Eventos

Repository não publica eventos.

O Aggregate registra eventos.

O Use Case ou Unit of Work coleta e publica após commit, conforme estratégia oficial.

Fluxo:

```text
Aggregate
    ↓
Domain Events
    ↓
Repository Save
    ↓
Commit
    ↓
Event Publisher
```

---

# 55. Repositories e Unit of Work

Os Repositories utilizados em um Use Case devem compartilhar a mesma Session da Unit of Work.

Exemplo:

```python
with unit_of_work as uow:
    user_repository = uow.users
    character_repository = uow.characters

    ...
    uow.commit()
```

ou via injeção coordenada pelo Composition Root.

---

# 56. Unit of Work com Repositories

Exemplo conceitual:

```python
class LifeOSUnitOfWork(Protocol):
    users: UserRepository
    characters: CharacterRepository
    workouts: WorkoutRepository

    def __enter__(self) -> "LifeOSUnitOfWork":
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
```

A forma final será detalhada em `UNIT_OF_WORK.md`.

---

# 57. Performance

Todo Repository deve considerar:

- índices;
- seleção de colunas;
- paginação;
- joins;
- N+1;
- filtros Multi-Tenant;
- plano de execução;
- volume esperado;
- custo de contagem;
- ordenação.

---

# 58. Consultas Lentas

Consultas lentas devem ser:

1. identificadas;
2. reproduzidas;
3. medidas;
4. analisadas;
5. otimizadas;
6. testadas;
7. documentadas.

Não criar índice sem analisar a consulta.

---

# 59. Read Repository do Dashboard

Dashboard deve utilizar Read Model consolidado.

Exemplo:

```python
class DashboardQueryRepository(Protocol):
    def get_summary(
        self,
        user_id: UserId,
        period: DateRange,
    ) -> DashboardSummaryReadModel:
        ...
```

Evitar executar dezenas de Repositories diretamente na página Streamlit.

---

# 60. Analytics Repositories

Analytics pode utilizar Repositories de leitura específicos.

Exemplos:

```text
SleepAnalyticsQueryRepository
WorkoutAnalyticsQueryRepository
ReadingAnalyticsQueryRepository
```

Eles podem retornar séries temporais e dados agregados.

Não devem retornar Plotly Figure.

---

# 61. Reports Repositories

Relatórios podem consumir Query Repositories.

Não duplicar consultas de negócio em exportadores.

Fluxo:

```text
Report Use Case
    ↓
Query Repository
    ↓
Export Adapter
```

---

# 62. Testes Unitários

Application deve ser testada com Repositories em memória.

Exemplo:

```python
class InMemoryCharacterRepository(CharacterRepository):
    def __init__(self) -> None:
        self._characters: dict[str, Character] = {}

    def find_by_user_id(
        self,
        user_id: UserId,
    ) -> Character | None:
        return self._characters.get(str(user_id))

    def save(
        self,
        character: Character,
    ) -> None:
        self._characters[str(character.user_id)] = character
```

---

# 63. Repositories em Memória

Devem respeitar o mesmo contrato e semântica da implementação real.

Não criar Fake simplificado que esconda comportamento importante.

Exemplos a preservar:

- unicidade;
- isolamento;
- ausência;
- ordenação;
- paginação;
- idempotência.

---

# 64. Testes de Contrato

Cada Repository deve possuir suíte de contrato reutilizável.

Exemplo:

```python
class CharacterRepositoryContract:
    def test_save_and_find_by_user_id(
        self,
        repository: CharacterRepository,
    ) -> None:
        ...

    def test_does_not_return_character_from_another_user(
        self,
        repository: CharacterRepository,
    ) -> None:
        ...
```

Implementações testadas:

```text
InMemoryCharacterRepository
SqlAlchemyCharacterRepository
FuturePostgresCharacterRepository
```

---

# 65. Testes de Integração

Devem validar:

- SQLAlchemy Models;
- Persistence Mappers;
- filtros;
- Multi-Tenant;
- Foreign Keys;
- constraints;
- ordenação;
- paginação;
- rollback;
- queries;
- soft delete;
- idempotência.

---

# 66. Teste Multi-Tenant Obrigatório

Todo Repository operacional deve possuir teste equivalente a:

```text
Dado usuário A e usuário B
Quando A busca seu registro
Então nenhum dado de B é retornado
```

Esse teste é obrigatório.

---

# 67. Teste de Ordenação

Toda listagem deve validar ordenação determinística.

Exemplo:

```text
occurred_at DESC
id DESC
```

---

# 68. Teste de Paginação

Validar:

- primeira página;
- última página;
- página vazia;
- limite máximo;
- total;
- ordenação;
- isolamento por usuário.

---

# 69. Teste de Soft Delete

Validar:

- registro excluído não aparece em consulta padrão;
- consulta administrativa pode localizar;
- ownership permanece protegido.

---

# 70. Estrutura de Arquivos

```text
module/
├── domain/
│   └── repositories/
│       └── <aggregate>_repository.py
├── application/
│   ├── queries/
│   ├── filters/
│   └── read_models/
└── infrastructure/
    ├── repositories/
    │   └── sqlalchemy_<aggregate>_repository.py
    ├── mappers/
    │   └── <aggregate>_persistence_mapper.py
    └── models/
        └── <aggregate>_model.py
```

---

# 71. Anti-patterns

São proibidos:

## Repository com regra de negócio

```python
def grant_experience(...):
    ...
```

## Repository com commit

```python
self._session.commit()
```

## Repository retornando ORM Model

```python
return CharacterModel
```

## Repository sem tenant

```python
filter(Model.id == id)
```

## Repository genérico de domínio

```python
BaseRepository[T]
```

como contrato universal.

## `get_all`

```python
def get_all(self) -> list[Entity]:
    ...
```

em tabelas crescentes.

## UI acessando Repository

```python
repository.find_by_id(...)
```

diretamente em página.

## SQL na Application

```python
session.execute(...)
```

dentro de Use Case.

---

# 72. Como o Gemini deve Utilizar este Documento

Antes de implementar um Repository, o agente deve verificar:

1. Qual Aggregate Root é proprietário?
2. O contrato pertence ao Domain?
3. A implementação pertence à Infrastructure?
4. O método utiliza linguagem do domínio?
5. O `user_id` está presente?
6. O retorno é Entity, Aggregate ou Read Model?
7. Existe Persistence Mapper?
8. Há commit indevido?
9. Existe consulta sem paginação?
10. A ordenação é determinística?
11. Há N+1?
12. Existe índice adequado?
13. A consulta acessa apenas o módulo proprietário?
14. Há necessidade de Query Repository separado?
15. Existem testes de contrato?
16. Existe teste Multi-Tenant?
17. A documentação foi atualizada?

---

# 73. Checklist de Implementação

- [ ] Aggregate Root identificado.
- [ ] Contrato criado no Domain.
- [ ] Implementação criada na Infrastructure.
- [ ] Nomenclatura oficial utilizada.
- [ ] Tipos de domínio utilizados.
- [ ] Multi-Tenant aplicado.
- [ ] Persistence Mapper utilizado.
- [ ] ORM Model não vazado.
- [ ] Nenhum commit no Repository.
- [ ] Filtros explícitos criados.
- [ ] Paginação aplicada quando necessária.
- [ ] Ordenação determinística definida.
- [ ] Índices avaliados.
- [ ] N+1 avaliado.
- [ ] Soft delete considerado.
- [ ] Tratamento de erro implementado.
- [ ] Repository em memória criado quando necessário.
- [ ] Teste de contrato criado.
- [ ] Teste de integração criado.
- [ ] Teste Multi-Tenant criado.
- [ ] Documentação atualizada.

---

# 74. Critérios de Aceite

Este documento será considerado atendido quando:

- todo Aggregate persistente possuir contrato adequado;
- implementações concretas permanecerem na Infrastructure;
- SQLAlchemy não vazar para Domain ou Application;
- Multi-Tenant estiver aplicado em todas as consultas;
- Repositories não executarem regras de negócio;
- commits forem controlados por Unit of Work;
- consultas grandes forem paginadas;
- Read Models forem utilizados quando apropriado;
- testes de contrato garantirem consistência;
- testes de integração validarem o comportamento real.

---

# 75. Definition of Done

Um Repository só estará concluído quando:

- [ ] O contrato estiver definido.
- [ ] A implementação concreta existir.
- [ ] O Mapper estiver implementado.
- [ ] O Model ORM estiver compatível.
- [ ] O filtro Multi-Tenant estiver aplicado.
- [ ] A transação estiver sob Unit of Work.
- [ ] A consulta estiver otimizada.
- [ ] A ordenação estiver definida.
- [ ] Os testes de contrato passarem.
- [ ] Os testes de integração passarem.
- [ ] O isolamento entre usuários estiver provado.
- [ ] A documentação estiver sincronizada.

---

# 76. Declaração Final

Repositories são fronteiras de persistência, não containers genéricos de acesso ao banco.

Eles existem para proteger o domínio dos detalhes técnicos e para oferecer operações coerentes com a linguagem do LifeOS.

Toda implementação deve preservar:

- encapsulamento;
- isolamento Multi-Tenant;
- semântica do domínio;
- controle transacional;
- testabilidade;
- independência de tecnologia;
- fronteiras modulares.

A persistência deve servir ao domínio sem contaminá-lo.
