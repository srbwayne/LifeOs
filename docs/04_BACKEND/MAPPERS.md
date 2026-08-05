# MAPPERS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Mappers  
**Camadas Relacionadas:** Presentation, Application, Domain e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture

---

# 1. Objetivo

Este documento define o padrão oficial para implementação de **Mappers** no LifeOS.

Seu objetivo é estabelecer como objetos são convertidos entre as diversas camadas da arquitetura sem gerar acoplamento entre elas.

Os Mappers garantem que cada camada trabalhe exclusivamente com seus próprios modelos, preservando:

- independência tecnológica;
- isolamento do domínio;
- separação de responsabilidades;
- baixo acoplamento;
- alta coesão;
- facilidade de evolução;
- facilidade de testes.

Toda conversão entre objetos pertencentes a camadas diferentes deverá ser realizada por um Mapper.

---

# 2. Escopo

Este documento cobre:

- Mappers de Domain;
- Mappers de Application;
- Mappers de Infrastructure;
- Mappers de Presentation;
- conversão entre DTOs;
- conversão entre Entities e ORM;
- conversão entre Commands;
- conversão entre Results;
- conversão entre ViewModels;
- conversão entre Read Models;
- conversão entre Events;
- serialização;
- desserialização;
- tratamento de Value Objects;
- coleções;
- objetos aninhados;
- segurança;
- Multi-Tenant;
- testes;
- anti-patterns;
- regras para agentes de IA.

Este documento complementa:

- `USE_CASES.md`;
- `SERVICES.md`;
- `REPOSITORIES.md`;
- `docs/04_BACKEND/UNIT_OF_WORK.md`;
- `VALIDATORS.md`;
- `DATABASE.md`;
- `SCHEMA.md`;
- `docs/02_ARCHITECTURE/02_CLEAN_ARCHITECTURE.md`;
- `docs/02_ARCHITECTURE/03_DDD.md`;
- `docs/02_ARCHITECTURE/04_HEXAGONAL.md`.

---

# 3. Princípios

Os Mappers do LifeOS devem seguir os seguintes princípios.

## 3.1 Separação de Camadas

Cada camada possui seus próprios modelos.

Nenhuma camada deve conhecer diretamente os modelos internos de outra.

Fluxo:

```text
Presentation
        ↓
Application
        ↓
Domain
        ↓
Infrastructure
```

A conversão entre essas camadas ocorre exclusivamente através de Mappers.

---

## 3.2 Conversão Explícita

Toda conversão deve ser explícita.

Nunca depender de:

- reflexão;
- conversão automática;
- serialização implícita;
- bibliotecas mágicas.

O código deve demonstrar claramente como cada campo é convertido.

---

## 3.3 Independência Tecnológica

Mappers não devem depender de:

- Streamlit;
- SQLAlchemy;
- SQLite;
- PostgreSQL;
- Plotly;
- APIs externas.

Eles trabalham apenas com objetos.

---

## 3.4 Determinismo

O mesmo objeto de entrada deve sempre produzir o mesmo objeto de saída.

Mappers nunca devem:

- consultar banco;
- acessar sessão;
- modificar estado global;
- gerar identificadores;
- executar regras de negócio.

---

## 3.5 Imutabilidade

Sempre que possível:

- objetos de entrada são imutáveis;
- objetos de saída são imutáveis;
- Mappers não modificam o objeto recebido.

A conversão produz uma nova instância.

---

# 4. O que é um Mapper

Mapper é um componente responsável exclusivamente pela conversão entre representações diferentes de um mesmo conceito.

Exemplo:

```text
RegisterWorkoutCommand

↓

Workout Entity
```

Outro exemplo:

```text
Workout Entity

↓

WorkoutResult
```

Outro exemplo:

```text
Workout Entity

↓

WorkoutModel (ORM)
```

O Mapper não executa nenhuma regra de domínio.

Sua única responsabilidade é transformar objetos.

---

## Exemplos

```text
UserMapper

CharacterMapper

WorkoutMapper

HealthMapper

DashboardMapper

ExperienceMapper
```

---

# 5. Responsabilidades

Um Mapper pode:

- copiar propriedades;
- converter tipos;
- converter Value Objects;
- converter listas;
- converter coleções;
- montar DTOs;
- montar ViewModels;
- montar ORM Models;
- montar Read Models;
- converter identificadores;
- converter datas;
- converter enums;
- converter estruturas aninhadas.

---

O Mapper nunca deve:

- persistir objetos;
- consultar banco;
- validar regras de negócio;
- abrir transações;
- publicar eventos;
- chamar IA;
- enviar e-mails;
- executar cálculos de domínio.

---

# 6. O que NÃO é responsabilidade do Mapper

As seguintes responsabilidades pertencem a outros componentes.

## Entity

- proteger invariantes;
- alterar estado.

---

## Domain Service

- calcular regras.

---

## Use Case

- coordenar fluxo.

---

## Repository

- persistir dados.

---

## Validator

- validar entrada.

---

## Policy

- definir regras configuráveis.

---

## Specification

- responder critérios booleanos.

---

## Presenter

- preparar dados para interface.

---

O Mapper apenas converte estruturas.

---

# 7. Tipos Oficiais de Mappers

O LifeOS reconhece oficialmente os seguintes tipos.

## Domain Mapper

Conversão entre objetos do domínio.

Exemplo:

```text
CharacterSnapshot

↓

Character
```

---

## Application Mapper

Conversão entre:

```text
Command

↓

Entity
```

ou

```text
Entity

↓

Result
```

---

## Infrastructure Mapper

Conversão entre:

```text
Entity

↓

ORM Model
```

e

```text
ORM Model

↓

Entity
```

---

## Presentation Mapper

Conversão entre:

```text
Result

↓

ViewModel
```

---

## Integration Mapper

Conversão entre:

```text
Entity

↓

API DTO
```

ou

```text
Webhook

↓

Command
```

---

# 8. Organização de Pastas

Estrutura oficial.

## Domain

```text
domain/

mappers/
```

---

## Application

```text
application/

mappers/
```

---

## Infrastructure

```text
infrastructure/

mappers/
```

---

## Presentation

```text
presentation/

mappers/
```

---

Exemplo:

```text
modules/

workout/

application/

mappers/

register_workout_mapper.py
```

Outro exemplo:

```text
modules/

character/

infrastructure/

mappers/

character_orm_mapper.py
```

---

Cada módulo deve possuir apenas os Mappers necessários.

---

# 9. Convenções de Nomenclatura

Os nomes devem comunicar claramente:

- origem;
- destino;
- responsabilidade.

Exemplos corretos:

```text
RegisterWorkoutCommandMapper

WorkoutResultMapper

CharacterOrmMapper

UserDtoMapper

DashboardViewModelMapper

ExperienceEventMapper
```

---

Evitar:

```text
Mapper

DataMapper

CommonMapper

GenericMapper

UtilsMapper

HelperMapper
```

---

Arquivos:

```text
character_orm_mapper.py

register_workout_command_mapper.py

dashboard_view_model_mapper.py
```

---

Classes:

```python
CharacterOrmMapper

RegisterWorkoutCommandMapper

DashboardViewModelMapper
```

---

# 10. Contrato Base

Todo Mapper deve possuir uma interface simples, previsível e fortemente tipada.

Exemplo:

```python
from typing import Protocol, TypeVar

Source = TypeVar("Source")
Target = TypeVar("Target")


class Mapper(Protocol[Source, Target]):

    def map(
        self,
        source: Source,
    ) -> Target:
        ...
```

---

Quando houver conversão bidirecional:

```python
class BidirectionalMapper(
    Protocol[Source, Target]
):

    def to_domain(
        self,
        source: Source,
    ) -> Target:
        ...

    def from_domain(
        self,
        source: Target,
    ) -> Source:
        ...
```

---

Características obrigatórias:

- responsabilidade única;
- tipagem explícita;
- sem efeitos colaterais;
- sem acesso a banco;
- sem regras de negócio;
- sem dependência de framework;
- determinístico;
- facilmente testável.

Este contrato será o padrão oficial para todos os Mappers implementados no LifeOS.

---

# 11. Command → Entity

A conversão de **Command** para **Entity** representa uma das principais responsabilidades da camada Application.

O Command contém a intenção do usuário.

A Entity representa o conceito de domínio.

Fluxo:

```text
Controller

↓

RegisterWorkoutCommand

↓

RegisterWorkoutCommandMapper

↓

Workout Entity
```

---

## Responsabilidades

O Mapper deve:

- copiar propriedades;
- converter Value Objects;
- converter enums;
- converter identificadores;
- converter datas;
- inicializar coleções vazias quando necessário.

---

## Exemplo

```python
class RegisterWorkoutCommandMapper:

    def map(
        self,
        command: RegisterWorkoutCommand,
    ) -> Workout:

        return Workout.create(
            id=WorkoutId.generate(),
            user_id=command.user_id,
            workout_type=command.workout_type,
            occurred_at=command.occurred_at,
            duration_minutes=command.duration_minutes,
            perceived_effort=command.perceived_effort,
        )
```

---

O Mapper não deve:

- salvar a Entity;
- validar regras de negócio;
- calcular XP;
- consultar banco.

---

# 12. Entity → Result

Após a execução do Use Case, a Entity nunca deve ser retornada diretamente.

O retorno oficial é um **Result**.

Fluxo:

```text
Workout Entity

↓

WorkoutResultMapper

↓

RegisterWorkoutResult
```

---

## Exemplo

```python
class WorkoutResultMapper:

    def map(
        self,
        workout: Workout,
    ) -> RegisterWorkoutResult:

        return RegisterWorkoutResult(
            workout_id=str(workout.id),
            created_at=workout.created_at,
        )
```

---

Benefícios:

- desacoplamento;
- estabilidade da API;
- independência da UI;
- proteção do domínio.

---

# 13. Entity → DTO

DTOs representam contratos públicos.

Uma Entity nunca deve atravessar a fronteira da camada.

Fluxo:

```text
Entity

↓

DTO Mapper

↓

DTO
```

---

Exemplo:

```python
Character

↓

CharacterDto
```

---

Exemplo de Mapper:

```python
class CharacterDtoMapper:

    def map(
        self,
        character: Character,
    ) -> CharacterDto:

        return CharacterDto(
            id=str(character.id),
            level=character.level,
            total_experience=character.total_experience,
        )
```

---

DTOs devem conter apenas os dados necessários.

---

# 14. DTO → Entity

Em integrações ou importações, pode ser necessário converter um DTO em Entity.

Fluxo:

```text
DTO

↓

Mapper

↓

Entity
```

---

Exemplo:

```python
class CharacterImportMapper:

    def map(
        self,
        dto: CharacterImportDto,
    ) -> Character:

        return Character.restore(
            ...
        )
```

---

Essa conversão nunca deve:

- persistir;
- validar regras de negócio;
- abrir transação.

---

# 15. ORM → Entity

Esse é o Mapper mais importante da Infrastructure.

Fluxo:

```text
SQLAlchemy Model

↓

Orm Mapper

↓

Domain Entity
```

---

Exemplo:

```python
class CharacterOrmMapper:

    def to_domain(
        self,
        model: CharacterModel,
    ) -> Character:

        return Character.restore(
            id=CharacterId(model.id),
            level=model.level,
            total_experience=model.total_experience,
        )
```

---

A Entity não deve conhecer SQLAlchemy.

---

# 16. Entity → ORM

Persistência ocorre através da conversão para o modelo ORM.

Fluxo:

```text
Entity

↓

Orm Mapper

↓

SQLAlchemy Model
```

---

Exemplo:

```python
class CharacterOrmMapper:

    def from_domain(
        self,
        character: Character,
    ) -> CharacterModel:

        return CharacterModel(
            id=str(character.id),
            level=character.level,
            total_experience=character.total_experience,
        )
```

---

Esse Mapper pertence exclusivamente à Infrastructure.

---

# 17. Aggregate Mapping

Aggregates devem ser convertidos preservando sua consistência.

Exemplo:

```text
Character

├── Attributes

├── Statistics

└── Achievements
```

↓

```text
CharacterDto
```

---

O Mapper deve manter:

- relações;
- composição;
- hierarquia;
- identidade.

Nunca reconstruir parcialmente um Aggregate sem justificativa.

---

# 18. Value Objects

Value Objects devem ser convertidos explicitamente.

Exemplo:

```python
Email

↓

String
```

ou

```python
String

↓

Email
```

---

Exemplo:

```python
email=str(user.email)
```

ou

```python
Email.create(dto.email)
```

---

Nunca transformar um Value Object em tipos primitivos espalhados pela aplicação sem necessidade.

---

# 19. Collections

Coleções devem ser convertidas preservando ordem e tipo.

Exemplo:

```python
return [
    self._mapper.map(item)
    for item in entities
]
```

---

Quando possível:

```python
tuple(
    self._mapper.map(item)
    for item in entities
)
```

para manter imutabilidade.

---

Nunca modificar a coleção original.

---

# 20. Null Handling

Mappers devem tratar valores opcionais explicitamente.

Correto:

```python
nickname=(
    dto.nickname
    if dto.nickname
    else None
)
```

---

Para coleções:

```python
items = source.items or []
```

---

Nunca assumir que um valor opcional sempre estará presente.

Toda conversão envolvendo campos opcionais deve ser explícita, previsível e segura, evitando exceções inesperadas durante o mapeamento.

---

# 21. Query Models

Os **Query Models** representam objetos especializados para operações de leitura.

Seu objetivo é otimizar consultas sem expor diretamente o modelo de domínio.

Fluxo:

```text
Query Repository

↓

Query Model

↓

Query Mapper

↓

Read Model
```

---

## Características

Query Models:

- não possuem comportamento;
- representam apenas leitura;
- podem conter joins;
- podem conter campos calculados;
- não substituem Entities.

---

## Exemplo

```python
class CharacterDashboardQueryModel:

    user_id: str

    player_name: str

    level: int

    total_experience: int

    body_fat: Decimal

    muscle_mass: Decimal
```

---

Os Query Models pertencem à camada Infrastructure.

---

# 22. Read Models

Read Models representam estruturas prontas para consumo pela camada Application.

Eles podem consolidar dados provenientes de múltiplas tabelas.

Fluxo:

```text
Query Model

↓

ReadModelMapper

↓

DashboardReadModel
```

---

Exemplo:

```python
@dataclass(frozen=True)
class DashboardReadModel:

    player_name: str

    global_level: int

    current_hp: int

    total_experience: int

    body_fat_percentage: Decimal
```

---

Read Models:

- não executam regras;
- não possuem identidade de domínio;
- são imutáveis;
- existem apenas para leitura.

---

# 23. ViewModels

ViewModels representam exatamente aquilo que será consumido pela interface.

Fluxo:

```text
Result

↓

ViewModel Mapper

↓

DashboardViewModel
```

---

Exemplo:

```python
class DashboardViewModel:

    player_name: str

    level_text: str

    experience_text: str

    radar_chart_data: list[int]
```

---

O ViewModel pode conter:

- textos formatados;
- valores arredondados;
- dados preparados para gráficos;
- propriedades específicas da interface.

---

Nunca utilizar ViewModel dentro do domínio.

---

# 24. API DTOs

Os API DTOs representam contratos públicos da futura API REST.

Fluxo:

```text
Result

↓

ApiDtoMapper

↓

JSON Response
```

---

Exemplo:

```python
class CharacterResponseDto:

    id: str

    player_name: str

    level: int

    total_experience: int
```

---

Esses DTOs devem permanecer estáveis.

Alterações incompatíveis exigem versionamento da API.

---

# 25. Events

Eventos também precisam de Mappers.

Fluxo:

```text
Domain Event

↓

Event Mapper

↓

Integration Event
```

---

Exemplo:

```python
class CharacterLevelUpEventMapper:

    def map(
        self,
        event: CharacterLeveledUp,
    ) -> CharacterLevelUpIntegrationEvent:

        ...
```

---

O Event Mapper pode:

- converter IDs;
- serializar datas;
- transformar Value Objects;
- montar payloads.

---

Nunca publicar Entities diretamente.

---

# 26. AI Models

Os modelos utilizados pela IA não devem conhecer o domínio.

Fluxo:

```text
Domain Entity

↓

AI Mapper

↓

Prompt Context
```

---

Exemplo:

```python
class WeeklySummaryPrompt:

    player_name: str

    workouts: list[str]

    sleep_average: float

    books_completed: int
```

---

O AI Mapper deve:

- anonimizar dados quando necessário;
- remover campos desnecessários;
- limitar contexto;
- proteger informações sensíveis.

---

# 27. Export Models

Exportações utilizam modelos próprios.

Fluxo:

```text
Entity

↓

Export Mapper

↓

CsvRow
```

ou

```text
↓

ExcelRow

↓

PdfSection
```

---

Exemplo:

```python
class WorkoutExportRow:

    occurred_at: date

    workout_name: str

    duration: int

    experience: int
```

---

Nunca reutilizar DTOs públicos para exportação.

---

# 28. Import Models

Importações devem utilizar objetos próprios.

Fluxo:

```text
CSV

↓

Import DTO

↓

Import Mapper

↓

Entity
```

---

Exemplo:

```python
WorkoutImportDto
```

↓

```python
Workout
```

---

O Import Mapper deve:

- converter tipos;
- normalizar dados;
- criar Value Objects.

A validação permanece responsabilidade dos Validators e do Domain.

---

# 29. Snapshot Models

Snapshots representam uma fotografia imutável do estado de um Aggregate em determinado momento.

São úteis para:

- auditoria;
- histórico;
- analytics;
- machine learning;
- backups;
- replay de eventos.

---

Exemplo:

```python
CharacterSnapshot
```

↓

```python
CharacterSnapshotMapper
```

↓

```python
CharacterSnapshotModel
```

---

Snapshots nunca substituem o Aggregate original.

---

# 30. Versionamento

Quando um contrato evoluir de forma incompatível, deve ser criada uma nova versão do Mapper.

Exemplo:

```text
CharacterDtoMapperV1

CharacterDtoMapperV2
```

ou

```text
CharacterResponseV1

CharacterResponseV2
```

---

Nunca modificar silenciosamente um contrato já utilizado por:

- API;
- exportação;
- integração;
- IA;
- eventos.

O versionamento preserva compatibilidade, facilita migrações graduais e reduz riscos de quebra entre módulos e consumidores externos.

---

# 31. Composição de Mappers

Em muitos cenários, um único Mapper não é suficiente para realizar toda a conversão.

Nesses casos, deve-se utilizar **composição**, nunca duplicação de código.

Fluxo:

```text
CharacterMapper
        │
        ├── AttributeMapper
        ├── StatisticsMapper
        ├── SkillMapper
        └── AchievementMapper
```

---

## Exemplo

```python
class CharacterMapper:

    def __init__(
        self,
        attribute_mapper: AttributeMapper,
        statistics_mapper: StatisticsMapper,
        achievement_mapper: AchievementMapper,
    ) -> None:
        ...
```

---

Cada Mapper continua responsável apenas pelo seu próprio objeto.

Essa abordagem favorece:

- baixo acoplamento;
- alta coesão;
- reutilização;
- facilidade de testes.

---

# 32. Nested Mapping

Objetos compostos devem ser convertidos através de seus próprios Mappers.

Exemplo:

```text
Character

├── Attributes
├── Statistics
├── Equipment
└── ActiveQuests
```

Cada objeto interno deve possuir seu Mapper específico.

---

Fluxo:

```text
CharacterMapper

↓

AttributeMapper

↓

StatisticsMapper

↓

QuestMapper
```

---

Nunca realizar toda a conversão manualmente em uma única classe.

---

# 33. Circular References

Mappers nunca devem gerar referências circulares.

Exemplo incorreto:

```text
Character

↓

Workout

↓

Character

↓

Workout

↓

...
```

---

Para evitar isso:

- utilizar DTOs específicos;
- utilizar identificadores;
- utilizar referências resumidas;
- utilizar Read Models.

---

Exemplo correto:

```text
WorkoutDto

↓

character_id
```

ao invés de:

```text
WorkoutDto

↓

CharacterDto

↓

WorkoutDto

↓

...
```

---

# 34. Lazy Loading

Mappers nunca devem depender de Lazy Loading implícito.

Errado:

```python
character.workouts
```

quando isso dispara consulta automática.

---

O Repository deve carregar previamente os dados necessários.

Fluxo correto:

```text
Repository

↓

Aggregate completo

↓

Mapper
```

---

O Mapper nunca deve provocar acesso ao banco.

---

# 35. Performance

Mappers devem ser extremamente leves.

Boas práticas:

- evitar reflexão;
- evitar serialização intermediária;
- evitar JSON temporário;
- evitar cópias desnecessárias;
- evitar consultas;
- evitar processamento pesado.

---

Exemplo correto:

```python
return CharacterDto(
    id=str(character.id),
    level=character.level,
)
```

---

Evitar:

```python
json.loads(
    json.dumps(...)
)
```

---

# 36. Imutabilidade

Sempre que possível, os objetos produzidos pelos Mappers devem ser imutáveis.

Exemplo:

```python
@dataclass(frozen=True)
class WorkoutResult:
    ...
```

---

O Mapper nunca deve modificar o objeto recebido.

Errado:

```python
entity.name = entity.name.upper()
```

Correto:

```python
return UserDto(
    name=entity.name.upper()
)
```

---

A transformação ocorre apenas no objeto de destino.

---

# 37. Multi-Tenant

Os Mappers devem preservar informações de isolamento entre usuários.

Exemplo:

```text
user_id

organization_id

tenant_id
```

---

Esses identificadores nunca devem ser removidos durante conversões internas quando forem necessários para manter o contexto da operação.

---

Ao gerar objetos públicos:

- remover informações internas quando apropriado;
- nunca expor dados de outro tenant;
- preservar ownership.

---

# 38. Segurança

Mappers também possuem responsabilidade sobre exposição de dados.

Nunca converter automaticamente:

- senha;
- hash;
- tokens;
- refresh tokens;
- códigos temporários;
- segredos;
- chaves privadas.

---

Exemplo incorreto:

```python
UserDto(
    password_hash=model.password_hash
)
```

---

Exemplo correto:

```python
UserDto(
    id=str(user.id),
    name=user.full_name,
    email=user.email.value,
)
```

---

# 39. Dados Sensíveis

Informações sensíveis devem possuir tratamento explícito.

Exemplos:

```text
Notas terapêuticas

Biometria

Dados médicos

Prompt da IA

Logs privados

Tokens

Sessões

Histórico clínico
```

---

O Mapper deve aplicar o princípio do **mínimo privilégio**.

Converter apenas o que é realmente necessário para o destino.

---

Quando necessário:

```text
Domain

↓

Sanitized DTO

↓

Interface
```

---

Nunca expor informações internas sem necessidade funcional.

---

# 40. Auditoria

Quando objetos forem destinados ao módulo de auditoria, o Mapper deve produzir um modelo específico.

Fluxo:

```text
Entity

↓

AuditMapper

↓

AuditEntry
```

---

Exemplo:

```python
class AuditEntry:

    entity_name: str

    entity_id: str

    operation: str

    occurred_at: datetime

    actor_id: str

    changes: dict[str, object]
```

---

O Audit Mapper deve:

- registrar apenas informações relevantes;
- preservar rastreabilidade;
- remover dados sensíveis;
- padronizar datas;
- produzir registros imutáveis.

A auditoria nunca deve depender diretamente das Entities do domínio, garantindo independência entre o histórico operacional e a evolução do modelo de negócio.

---

# 41. SQLAlchemy

A conversão entre o domínio e o banco de dados ocorre exclusivamente através dos **ORM Mappers**.

Fluxo:

```text
Domain Entity

↓

Orm Mapper

↓

SQLAlchemy Model

↓

Database
```

Fluxo inverso:

```text
Database

↓

SQLAlchemy Model

↓

Orm Mapper

↓

Domain Entity
```

---

## Responsabilidades

O ORM Mapper deve:

- converter tipos primitivos;
- converter Value Objects;
- converter Enums;
- converter coleções;
- converter relações;
- preservar identidade;
- reconstruir corretamente o Aggregate.

---

Nunca permitir que:

- Entities importem SQLAlchemy;
- Aggregates conheçam Models ORM;
- Domain dependa de Session.

---

Exemplo:

```python
CharacterOrmMapper

↓

CharacterModel
```

---

# 42. Streamlit

A camada Presentation utiliza ViewModels próprios.

Fluxo:

```text
Use Case

↓

Result

↓

ViewModel Mapper

↓

Streamlit Page
```

---

Nunca passar Entities diretamente para componentes Streamlit.

Errado:

```python
st.write(character)
```

Correto:

```python
view_model = mapper.map(result)

render(view_model)
```

---

O Mapper prepara:

- textos;
- ícones;
- labels;
- indicadores;
- tabelas;
- gráficos;
- cards.

---

A interface nunca deve depender da estrutura interna do domínio.

---

# 43. JSON

JSON representa um formato de transporte.

Nunca deve substituir DTOs.

Fluxo:

```text
Entity

↓

DTO

↓

JSON Mapper

↓

JSON
```

---

Exemplo:

```python
{
    "id": "...",
    "level": 15,
    "experience": 4120
}
```

---

O Mapper deve:

- serializar datas;
- serializar UUIDs;
- serializar Enums;
- serializar Decimal;
- remover objetos complexos.

---

Nunca serializar Entities diretamente.

---

# 44. CSV

CSV utiliza modelos próprios.

Fluxo:

```text
Entity

↓

Export Mapper

↓

CSV Row

↓

CSV File
```

---

Exemplo:

```python
WorkoutCsvRow

date

type

duration

experience
```

---

O Mapper deve:

- converter datas;
- converter números;
- normalizar separadores;
- remover objetos complexos.

---

Nunca exportar o Aggregate inteiro.

---

# 45. Excel

Excel segue a mesma estratégia do CSV.

Fluxo:

```text
Entity

↓

Excel Mapper

↓

Worksheet Row
```

---

Exemplo:

```python
CharacterExcelRow

Level

Experience

Body Fat

VO₂ Max
```

---

O Mapper deve produzir dados prontos para planilhas.

Não deve:

- criar workbook;
- aplicar estilos;
- gerar gráficos.

Essas responsabilidades pertencem ao Exporter.

---

# 46. PDF

PDF utiliza modelos específicos.

Fluxo:

```text
Entity

↓

Report Mapper

↓

PdfSection

↓

PdfExporter
```

---

Exemplo:

```python
CharacterSummarySection
```

---

O Mapper organiza:

- títulos;
- textos;
- indicadores;
- tabelas;
- listas.

Nunca desenha diretamente o PDF.

---

# 47. APIs

Toda API utiliza DTOs públicos.

Fluxo:

```text
Request JSON

↓

Request DTO

↓

Mapper

↓

Command

↓

Use Case

↓

Result

↓

Mapper

↓

Response DTO

↓

JSON
```

---

Nunca:

```text
JSON

↓

Entity
```

diretamente.

---

O Mapper protege o domínio de mudanças na API.

---

# 48. AI Providers

Os Providers de IA nunca devem conhecer o domínio.

Fluxo:

```text
Domain

↓

AI Mapper

↓

Prompt Context

↓

Provider

↓

Response

↓

AI Response Mapper

↓

Recommendation DTO
```

---

O AI Mapper deve:

- reduzir contexto;
- anonimizar dados;
- limitar tamanho;
- remover informações sensíveis;
- estruturar prompts.

---

O domínio permanece totalmente desacoplado do modelo de IA utilizado.

---

# 49. Background Jobs

Jobs assíncronos utilizam seus próprios modelos.

Fluxo:

```text
Domain Event

↓

Job Mapper

↓

Job Payload

↓

Worker
```

---

Exemplo:

```python
GenerateWeeklySummaryJob
```

↓

```python
GenerateWeeklySummaryPayload
```

---

O Payload deve conter apenas:

- IDs;
- parâmetros;
- contexto mínimo.

Nunca transportar Aggregates completos.

---

# 50. Cache

Objetos destinados ao cache devem possuir modelos próprios.

Fluxo:

```text
Entity

↓

Cache Mapper

↓

Cache Model

↓

Redis / Memory
```

---

Exemplo:

```python
DashboardCacheModel
```

---

O Cache Mapper deve:

- serializar objetos;
- reduzir tamanho;
- remover informações sensíveis;
- manter compatibilidade de versão.

Nunca armazenar diretamente Entities ou Aggregates completos no cache.

O cache deve ser tratado como uma representação otimizada e descartável dos dados, nunca como fonte oficial de verdade.

---

# 51. Testes Unitários

Todo Mapper deve possuir testes unitários independentes.

Os testes devem validar:

- conversão completa;
- conversão parcial;
- objetos nulos;
- coleções vazias;
- Value Objects;
- Enums;
- datas;
- campos opcionais;
- objetos aninhados.

---

Exemplo:

```python
def test_character_mapper():
    character = CharacterFactory.create()

    dto = CharacterDtoMapper().map(character)

    assert dto.id == str(character.id)
    assert dto.level == character.level
```

---

Os testes nunca devem depender de:

- banco;
- SQLAlchemy;
- Streamlit;
- APIs externas.

---

# 52. Testes de Contrato

Quando existir uma interface de Mapper, todas as implementações devem respeitar exatamente o mesmo contrato.

Exemplo:

```text
CharacterMapper

↓

CharacterDtoMapper

CharacterJsonMapper

CharacterExportMapper
```

Todos devem produzir resultados coerentes para o mesmo objeto de entrada.

---

Os testes devem validar:

- assinatura;
- comportamento;
- tipos;
- nulidade;
- exceções.

---

# 53. Testes de Integração

Os testes de integração validam a interação entre Mappers e Infrastructure.

Devem validar:

- ORM Mapping;
- SQLAlchemy;
- persistência;
- reconstrução de Aggregates;
- serialização;
- desserialização.

---

Exemplo:

```text
Entity

↓

ORM Mapper

↓

Database

↓

ORM Mapper

↓

Entity
```

O objeto reconstruído deve permanecer consistente.

---

# 54. Testes de Performance

Mappers são executados milhares de vezes durante o ciclo de vida da aplicação.

Devem ser eficientes.

Os testes podem medir:

- tempo médio;
- consumo de memória;
- alocações;
- conversão em lote.

---

Evitar:

- serializações desnecessárias;
- reflexão;
- cópias excessivas.

---

# 55. Builders

Builders podem ser utilizados para facilitar criação de objetos complexos antes do mapeamento.

Exemplo:

```python
CharacterBuilder()\
    .with_level(15)\
    .with_total_experience(4200)\
    .build()
```

---

Builders auxiliam principalmente:

- testes;
- importações;
- fixtures;
- seeds.

Não substituem os Mappers.

---

# 56. Factories

Factories são responsáveis por criar objetos.

Mappers apenas convertem.

Fluxo correto:

```text
Factory

↓

Entity

↓

Mapper

↓

DTO
```

---

Nunca utilizar um Mapper para criar regras de construção do domínio.

Exemplo incorreto:

```python
mapper.map(command)
```

criando lógica complexa de inicialização.

Essa responsabilidade pertence às Factories ou às próprias Entities.

---

# 57. Anti-patterns

São proibidos.

---

## Mapper Genérico

```python
class GenericMapper:
    ...
```

---

## Mapper com SQL

```python
SELECT ...
```

---

## Mapper com Repository

```python
repository.find(...)
```

---

## Mapper com regra de negócio

```python
xp = duration * 8
```

---

## Mapper modificando Entity

```python
entity.level += 1
```

---

## Mapper chamando IA

```python
GeminiProvider()
```

---

## Mapper persistindo dados

```python
session.commit()
```

---

## Mapper utilizando Streamlit

```python
st.metric(...)
```

---

Todos esses padrões violam a arquitetura oficial.

---

# 58. Exemplos Oficiais

## Command → Entity

```text
RegisterWorkoutCommand

↓

Workout
```

---

## Entity → Result

```text
Workout

↓

RegisterWorkoutResult
```

---

## Entity → ORM

```text
Character

↓

CharacterModel
```

---

## ORM → Entity

```text
CharacterModel

↓

Character
```

---

## Entity → ViewModel

```text
DashboardResult

↓

DashboardViewModel
```

---

## Entity → Export

```text
Workout

↓

WorkoutCsvRow
```

---

## Domain Event → Integration Event

```text
CharacterLeveledUp

↓

CharacterLevelUpIntegrationEvent
```

---

Esses fluxos representam os padrões oficiais do LifeOS.

---

# 59. Como o Gemini deve Utilizar este Documento

Antes de criar qualquer Mapper, o agente deve responder:

1. Qual é a origem?
2. Qual é o destino?
3. As camadas são diferentes?
4. Existe Mapper reutilizável?
5. Existem Value Objects?
6. Existem coleções?
7. Existem objetos aninhados?
8. Existem dados sensíveis?
9. Existe contexto Multi-Tenant?
10. Existe necessidade de anonimização?
11. Existe serialização?
12. Existe versão do contrato?
13. Há testes?
14. O Mapper está livre de regras de negócio?
15. O Mapper está livre de dependências tecnológicas?

Somente após essas respostas o código poderá ser gerado.

---

# 60. Checklist de Implementação

- [ ] Origem definida.
- [ ] Destino definido.
- [ ] Responsabilidade única.
- [ ] Conversão explícita.
- [ ] Sem regras de negócio.
- [ ] Sem acesso a banco.
- [ ] Sem acesso à UI.
- [ ] Sem acesso à IA.
- [ ] Value Objects tratados.
- [ ] Enums tratados.
- [ ] Datas convertidas.
- [ ] Objetos opcionais tratados.
- [ ] Coleções convertidas.
- [ ] Multi-Tenant preservado.
- [ ] Dados sensíveis protegidos.
- [ ] Testes unitários criados.
- [ ] Documentação atualizada.

---

# 61. Critérios de Aceite

Um Mapper será considerado aceito quando:

- converter corretamente todos os campos;
- preservar identidade;
- não executar regras de negócio;
- não depender de infraestrutura;
- não modificar o objeto de origem;
- possuir testes automatizados;
- respeitar a arquitetura em camadas;
- preservar isolamento Multi-Tenant;
- proteger informações sensíveis.

---

# 62. Definition of Done

Um Mapper somente será considerado concluído quando:

- [ ] Conversão implementada.
- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados quando aplicável.
- [ ] Objetos imutáveis preservados.
- [ ] Sem efeitos colaterais.
- [ ] Sem dependências indevidas.
- [ ] Performance revisada.
- [ ] Documentação sincronizada.

---

# 63. Roadmap Evolutivo

Evoluções previstas:

- geração automática de Mappers;
- validação automática de contratos;
- geração de documentação a partir dos Mappers;
- suporte a versionamento automático;
- integração com Event Sourcing;
- otimizações para processamento em lote;
- suporte a novos formatos de exportação;
- integração com novos Providers de IA.

Toda evolução deverá manter compatibilidade com este documento.

---

# 64. Convenções Oficiais

Os Mappers do LifeOS devem seguir obrigatoriamente:

- responsabilidade única;
- uma origem;
- um destino;
- métodos pequenos;
- conversão explícita;
- tipagem forte;
- nomenclatura consistente;
- sem efeitos colaterais;
- independência tecnológica;
- alta testabilidade.

---

# 65. Glossário

**Mapper**  
Componente responsável pela conversão entre representações de um mesmo conceito.

**DTO**  
Objeto de transporte entre camadas.

**ViewModel**  
Objeto preparado para consumo da interface.

**Read Model**  
Objeto otimizado para consultas.

**ORM Model**  
Representação persistente utilizada pela camada Infrastructure.

**Value Object**  
Objeto imutável que representa um conceito do domínio.

**Aggregate**  
Conjunto consistente de Entities controlado por uma Aggregate Root.

---

# 66. Referências Arquiteturais

Este documento está alinhado com:

- Clean Architecture;
- Domain-Driven Design (DDD);
- Arquitetura Hexagonal;
- SOLID;
- CQRS Light;
- Event-Driven Architecture;
- Modular Monolith.

Também complementa:

- `USE_CASES.md`;
- `DTOs.md`;
- `REPOSITORIES.md`;
- `SERVICES.md`;
- `docs/04_BACKEND/UNIT_OF_WORK.md`;
- `VALIDATORS.md`.

---

# 67. ADRs Relacionadas

Toda alteração significativa no padrão de Mappers deverá ser registrada através de uma **Architecture Decision Record (ADR)**.

Exemplos:

- adoção de geração automática de Mappers;
- mudança de estratégia de serialização;
- introdução de novos formatos de exportação;
- alteração do contrato base.

O objetivo é preservar o histórico das decisões arquiteturais.

---

# 68. Padrões Obrigatórios

Todo Mapper do LifeOS deve obedecer às seguintes regras:

- converter apenas entre duas representações;
- nunca acessar banco de dados;
- nunca conhecer a interface;
- nunca executar regras de domínio;
- nunca persistir dados;
- nunca publicar eventos;
- nunca modificar o objeto de origem;
- produzir sempre um objeto válido para a camada de destino.

Essas regras são obrigatórias para todo o projeto.

---

# 69. Declaração Final

Os Mappers representam a fronteira entre as camadas do LifeOS.

Sua função é garantir que cada camada permaneça isolada, independente e evolutiva, permitindo que tecnologias sejam substituídas sem impacto no domínio.

Ao seguir este documento, o projeto mantém uma arquitetura limpa, previsível e altamente testável, preparada para crescimento contínuo e geração de código assistida por IA.

---

# 70. Anexos

## Anexo A — Fluxo Geral

```text
Presentation
      ↓
Command
      ↓
Mapper
      ↓
Entity
      ↓
Use Case
      ↓
Result
      ↓
Mapper
      ↓
ViewModel
      ↓
Interface
```

---

## Anexo B — Fluxo ORM

```text
Entity
      ↓
Orm Mapper
      ↓
SQLAlchemy Model
      ↓
Database
      ↓
SQLAlchemy Model
      ↓
Orm Mapper
      ↓
Entity
```

---

## Anexo C — Fluxo de Integração

```text
Domain Event
      ↓
Event Mapper
      ↓
Integration Event
      ↓
External System
```

Esses anexos representam os fluxos oficiais de mapeamento adotados pelo LifeOS e devem servir como referência para desenvolvedores e agentes de IA durante a implementação.
