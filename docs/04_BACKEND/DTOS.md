# DTOs

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Data Transfer Objects  
**Camadas Relacionadas:** Presentation, Application, Domain e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e CQRS Light

---

# 1. Objetivo

Este documento define o padrão oficial de **Data Transfer Objects (DTOs)** do LifeOS.

Seu objetivo é estabelecer:

- quais tipos de DTOs existem;
- onde cada DTO deve ser criado;
- como dados devem atravessar fronteiras arquiteturais;
- como Commands, Queries, Results, Read Models e ViewModels devem ser organizados;
- como contratos públicos entre módulos devem ser definidos;
- como dados sensíveis devem ser protegidos;
- como o isolamento Multi-Tenant deve ser preservado;
- como DTOs devem ser versionados, mapeados e testados;
- quais práticas são obrigatórias e quais são proibidas.

Toda troca de dados entre camadas, módulos ou integrações deve utilizar contratos explícitos compatíveis com este documento.

---

# 2. Escopo

Este documento cobre:

- Input DTOs;
- Output DTOs;
- Commands;
- Queries;
- Results;
- Read Models;
- ViewModels;
- Public Contracts;
- Integration DTOs;
- Event DTOs;
- API DTOs;
- Export DTOs;
- Import DTOs;
- AI DTOs;
- DTOs de paginação;
- DTOs de erro;
- imutabilidade;
- serialização;
- versionamento;
- validação;
- segurança;
- Multi-Tenant;
- testes;
- anti-patterns;
- regras para agentes de IA.

Este documento complementa:

- `USE_CASES.md`;
- `MAPPERS.md`;
- `SERVICES.md`;
- `VALIDATORS.md`;
- `REPOSITORIES.md`;
- `UNIT_OF_WORK.md`;
- `02_ARCHITECTURE/HEXAGONAL.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`.

---

# 3. Definição

DTO é um objeto utilizado para transportar dados entre fronteiras.

Um DTO:

- não representa comportamento de domínio;
- não possui identidade própria;
- não controla ciclo de vida;
- não persiste a si mesmo;
- não conhece banco;
- não conhece interface;
- não executa regras de negócio;
- não acessa serviços externos.

Exemplo:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterWorkoutCommand:
    workout_type_id: str
    occurred_at: str
    duration_minutes: int | None
    perceived_effort: int | None
    notes: str | None
```

---

# 4. Princípio Central

Cada fronteira deve utilizar seu próprio contrato.

Fluxo oficial:

```text
Interface
    ↓
Request DTO
    ↓
Command / Query
    ↓
Use Case
    ↓
Result / Read Model
    ↓
ViewModel / Response DTO
    ↓
Interface
```

Nenhuma Entity deve atravessar diretamente uma fronteira externa.

---

# 5. Responsabilidades

Um DTO pode:

- transportar valores;
- agrupar parâmetros;
- representar entrada;
- representar saída;
- representar leitura;
- representar contrato público;
- representar payload de evento;
- representar dados de exportação;
- representar contexto para IA;
- representar paginação;
- representar erro estruturado.

Um DTO não pode:

- persistir dados;
- consultar Repository;
- calcular XP;
- alterar Entity;
- abrir transação;
- publicar evento;
- executar autorização;
- acessar `st.session_state`;
- importar SQLAlchemy;
- chamar Provider externo.

---

# 6. Tipos Oficiais de DTOs

O LifeOS reconhece as seguintes categorias:

```text
Command DTO
Query DTO
Result DTO
Read Model
ViewModel
Request DTO
Response DTO
Public Contract DTO
Integration DTO
Event DTO
Import DTO
Export DTO
AI DTO
Error DTO
Pagination DTO
```

Cada categoria possui responsabilidade própria.

---

# 7. Organização Física

Estrutura recomendada por módulo:

```text
module/
├── application/
│   ├── commands/
│   ├── queries/
│   ├── results/
│   ├── dto/
│   └── read_models/
├── presentation/
│   └── view_models/
├── public/
│   └── contracts.py
└── infrastructure/
    └── integrations/
        └── dto/
```

Interfaces externas:

```text
interfaces/
├── streamlit/
│   └── models/
└── api/
    └── dto/
```

---

# 8. Convenções de Nomenclatura

Nomes devem indicar claramente finalidade e direção.

Exemplos:

```text
RegisterWorkoutCommand
GetWorkoutHistoryQuery
RegisterWorkoutResult
WorkoutHistoryItem
DashboardReadModel
DashboardViewModel
RegisterUserRequest
RegisterUserResponse
CharacterSummaryContract
WorkoutRegisteredEventDto
WorkoutExportRow
WorkoutImportRow
WeeklyMentorContextDto
ValidationErrorDto
PageRequest
PageResult
```

Evitar:

```text
Data
Payload
Object
Model
GenericDto
CommonDto
UserData
ResponseData
```

sem contexto suficiente.

---

# 9. Imutabilidade

DTOs devem ser imutáveis sempre que possível.

Padrão:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterSummaryDto:
    character_id: str
    global_level: int
    total_experience: int
```

Benefícios:

- previsibilidade;
- segurança;
- ausência de efeitos colaterais;
- facilidade de testes;
- compatibilidade com eventos;
- consistência entre camadas.

---

# 10. Tipagem

DTOs devem possuir tipagem explícita.

Correto:

```python
@dataclass(frozen=True)
class SleepRecordResult:
    record_id: str
    record_date: date
    sleep_score: int | None
```

Evitar:

```python
dict[str, object]
```

como contrato principal.

`dict` pode ser utilizado apenas em metadados controlados e justificados.

---

# 11. Command DTOs

Commands representam intenção de alteração de estado.

Exemplos:

```text
RegisterUserCommand
RegisterWorkoutCommand
RegisterSleepCommand
CompleteHabitCommand
ResetPasswordCommand
GrantExperienceCommand
```

Commands devem:

- iniciar com verbo;
- ser imutáveis;
- conter somente dados de entrada;
- não possuir resultado;
- não possuir lógica;
- não importar infraestrutura.

---

# 12. Exemplo de Command

```python
@dataclass(frozen=True)
class RegisterSleepCommand:
    record_date: date
    sleep_duration_hours: Decimal | None
    hrv_ms: int | None
    resting_heart_rate_bpm: int | None
    deep_sleep_minutes: int | None
    rem_sleep_minutes: int | None
    sleep_score: int | None
```

O `user_id` pode ser obtido pelo `CurrentUserProvider`, evitando confiar em entrada externa.

---

# 13. Query DTOs

Queries representam intenção de leitura.

Exemplos:

```text
GetCharacterSheetQuery
GetWorkoutHistoryQuery
GetSleepHistoryQuery
SearchReadingInsightsQuery
GetDashboardSummaryQuery
```

Queries devem:

- ser somente leitura;
- conter filtros;
- conter paginação;
- conter ordenação;
- não alterar estado;
- não publicar eventos.

---

# 14. Exemplo de Query

```python
@dataclass(frozen=True)
class GetWorkoutHistoryQuery:
    start_date: date | None
    end_date: date | None
    workout_type_id: str | None
    page: int
    size: int
    sort_field: str
    sort_direction: str
```

Campos de ordenação devem ser validados contra uma allowlist.

---

# 15. Result DTOs

Results representam a saída de Command Use Cases.

Exemplos:

```text
RegisterUserResult
RegisterWorkoutResult
ResetPasswordResult
CompleteHabitResult
GrantExperienceResult
```

Results devem:

- indicar o resultado da operação;
- conter identificadores relevantes;
- conter dados necessários à próxima camada;
- não expor Entity;
- não expor ORM Model;
- não conter objetos técnicos.

---

# 16. Exemplo de Result

```python
@dataclass(frozen=True)
class RegisterWorkoutResult:
    workout_id: str
    granted_experience: int
    current_global_level: int
    unlocked_achievement_codes: tuple[str, ...]
```

---

# 17. Read Models

Read Models representam projeções otimizadas de leitura.

Exemplos:

```text
CharacterSheetReadModel
WorkoutHistoryReadModel
WeeklyAnalyticsReadModel
DashboardSummaryReadModel
```

Podem consolidar:

- múltiplas tabelas;
- agregações;
- joins;
- métricas;
- campos derivados.

Não possuem comportamento de domínio.

---

# 18. Exemplo de Read Model

```python
@dataclass(frozen=True)
class CharacterSheetReadModel:
    player_name: str
    sex: str | None
    height_cm: Decimal | None
    current_weight_kg: Decimal | None
    body_fat_percentage: Decimal | None
    muscle_mass_kg: Decimal | None
    vo2_max: Decimal | None
    global_level: int
    total_experience: int
    attributes: tuple["CharacterAttributeReadModel", ...]
```

---

# 19. ViewModels

ViewModels representam dados prontos para exibição.

Podem conter:

- textos formatados;
- labels;
- valores arredondados;
- percentuais formatados;
- dados para gráficos;
- mensagens;
- estados visuais.

Exemplo:

```python
@dataclass(frozen=True)
class CharacterSheetViewModel:
    player_name: str
    level_label: str
    total_experience_label: str
    body_fat_label: str
    radar_labels: tuple[str, ...]
    radar_values: tuple[int, ...]
```

ViewModels pertencem à Presentation.

---

# 20. Request DTOs

Request DTOs representam dados recebidos por uma interface externa.

Exemplos:

```text
RegisterUserRequest
LoginRequest
RegisterWorkoutRequest
ResetPasswordRequest
```

Podem refletir:

- formulário Streamlit;
- JSON de API;
- comando CLI;
- importação.

Devem ser convertidos em Command ou Query por Mapper ou Controller.

---

# 21. Response DTOs

Response DTOs representam contratos externos de resposta.

Exemplos:

```text
RegisterUserResponse
WorkoutHistoryResponse
CharacterSheetResponse
ValidationErrorResponse
```

Não devem expor estruturas internas da Application ou Domain.

---

# 22. Public Contract DTOs

Módulos comunicam-se por contratos públicos.

Localização:

```text
module/public/contracts.py
```

Exemplo:

```python
@dataclass(frozen=True)
class CharacterSummaryContract:
    character_id: str
    user_id: str
    global_level: int
    total_experience: int
```

Outros módulos não recebem `Character` Entity.

---

# 23. Integration DTOs

Integration DTOs representam dados enviados ou recebidos de sistemas externos.

Exemplos:

```text
EmailDeliveryRequestDto
ExternalCalendarEventDto
AIProviderRequestDto
AIProviderResponseDto
WebhookPayloadDto
```

Devem isolar o restante da aplicação do contrato externo.

---

# 24. Event DTOs

Eventos públicos devem utilizar payloads imutáveis e mínimos.

Exemplo:

```python
@dataclass(frozen=True)
class WorkoutRegisteredEventDto:
    event_id: str
    user_id: str
    workout_id: str
    occurred_at: datetime
```

Não transportar:

- Entity;
- Repository;
- Session;
- objeto Streamlit;
- ORM Model.

---

# 25. Import DTOs

Import DTOs representam linhas ou objetos recebidos por importação.

Exemplo:

```python
@dataclass(frozen=True)
class WorkoutImportRow:
    occurred_at: str
    workout_type_name: str
    duration_minutes: str | None
    perceived_effort: str | None
    notes: str | None
```

A conversão e validação devem ocorrer antes da criação da Entity.

---

# 26. Export DTOs

Export DTOs representam dados preparados para exportação.

Exemplo:

```python
@dataclass(frozen=True)
class WorkoutExportRow:
    occurred_at: str
    workout_type_name: str
    duration_minutes: int | None
    perceived_effort: int | None
    notes: str | None
```

O Exporter decide o formato final.

---

# 27. AI DTOs

AI DTOs devem conter somente o contexto mínimo necessário.

Exemplo:

```python
@dataclass(frozen=True)
class WeeklyMentorContextDto:
    user_alias: str
    period_start: date
    period_end: date
    workout_count: int
    average_sleep_score: Decimal | None
    completed_habits: int
    pages_read: int
    current_global_level: int
```

Devem evitar dados pessoais desnecessários.

---

# 28. Error DTOs

Erros devem ser estruturados.

Exemplo:

```python
@dataclass(frozen=True)
class ErrorDetailDto:
    code: str
    message: str
    field: str | None = None
```

Resposta agregada:

```python
@dataclass(frozen=True)
class ErrorResponseDto:
    correlation_id: str
    errors: tuple[ErrorDetailDto, ...]
```

---

# 29. Pagination DTOs

Padrão oficial:

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class PageRequest:
    page: int
    size: int


@dataclass(frozen=True)
class PageResult(Generic[T]):
    items: tuple[T, ...]
    page: int
    size: int
    total_items: int
    total_pages: int
```

---

# 30. Sort DTOs

Padrão:

```python
from dataclasses import dataclass
from enum import Enum


class SortDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True)
class SortDto:
    field: str
    direction: SortDirection
```

Campos válidos devem ser definidos por Query.

---

# 31. Filter DTOs

Filtros complexos devem ser agrupados.

Exemplo:

```python
@dataclass(frozen=True)
class WorkoutFilterDto:
    start_date: date | None = None
    end_date: date | None = None
    workout_type_id: str | None = None
    minimum_effort: int | None = None
```

Evitar assinaturas com muitos parâmetros soltos.

---

# 32. Date Range DTO

Quando não for Value Object de domínio, pode existir DTO de intervalo.

```python
@dataclass(frozen=True)
class DateRangeDto:
    start_date: date
    end_date: date
```

A validação deve garantir:

```text
start_date <= end_date
```

---

# 33. Identificadores

DTOs externos podem utilizar IDs como `str`.

Dentro da Application, podem utilizar Value Objects quando isso melhorar segurança de tipos.

Exemplo externo:

```python
user_id: str
```

Exemplo interno:

```python
user_id: UserId
```

A escolha deve respeitar a fronteira.

---

# 34. Datas e Horários

DTOs internos devem preferir:

```text
date
datetime
```

DTOs externos serializados podem utilizar ISO 8601.

Exemplo:

```text
2026-08-01T18:30:00Z
```

Conversão deve ser explícita por Mapper.

---

# 35. Decimal

Valores de precisão devem utilizar `Decimal`.

Exemplos:

- peso;
- percentual;
- massa muscular;
- distância;
- VO₂ máximo;
- métricas calculadas.

Evitar `float` em contratos que exigem precisão determinística.

---

# 36. Enums

DTOs internos podem usar Enums.

DTOs externos devem utilizar códigos estáveis.

Exemplo:

```text
ACTIVE
COMPLETED
PENDING
```

Não expor nomes dependentes de implementação.

---

# 37. Coleções

Coleções imutáveis devem preferir:

```text
tuple
```

Exemplo:

```python
attributes: tuple[CharacterAttributeDto, ...]
```

Listas podem ser utilizadas em contratos de serialização quando necessário.

---

# 38. Campos Opcionais

Campos opcionais devem ser explicitamente tipados.

Exemplo:

```python
vo2_max: Decimal | None
```

Não utilizar string vazia para representar ausência.

---

# 39. Defaults

Defaults devem ser simples e explícitos.

Exemplo:

```python
page: int = 1
size: int = 20
```

Defaults de negócio devem permanecer no Domain ou Policy.

---

# 40. Validação de DTOs

DTOs podem possuir validação estrutural mínima apenas quando necessária.

Preferência:

- Command Validator;
- Query Validator;
- Value Object;
- Domain;
- API schema validator.

Evitar lógica de negócio em `__post_init__` de DTOs.

---

# 41. DTOs e Mappers

Toda conversão entre DTO e outro modelo deve utilizar Mapper quando a transformação não for trivial ou quando cruzar camadas.

Exemplo:

```text
RegisterWorkoutRequest
    ↓
RegisterWorkoutRequestMapper
    ↓
RegisterWorkoutCommand
```

---

# 42. DTOs e Controllers

Controllers:

- recebem Request DTO;
- montam Command ou Query;
- executam Use Case;
- recebem Result;
- chamam Presenter;
- retornam ViewModel ou Response DTO.

Controllers não devem retornar Entity.

---

# 43. DTOs e Use Cases

Use Cases devem receber:

```text
Command
```

ou:

```text
Query
```

E retornar:

```text
Result
```

ou:

```text
Read Model
```

---

# 44. DTOs e Repositories

Aggregate Repositories retornam Entities.

Query Repositories podem retornar Read Models.

Repositories não devem retornar:

- Request DTO;
- Response DTO;
- ViewModel;
- objeto Streamlit;
- API schema.

---

# 45. DTOs e Domain

O Domain não deve depender de DTOs da Application ou Presentation.

Permitido:

```text
Application Mapper
    ↓
Domain Entity / Value Object
```

Proibido:

```text
Domain Entity
    ↓
RegisterWorkoutRequest
```

---

# 46. DTOs e Infrastructure

Infrastructure pode possuir DTOs próprios para integrações.

Exemplo:

```text
GeminiRequestDto
SmtpMessageDto
StorageObjectDto
```

Esses DTOs não devem vazar para Application.

---

# 47. Multi-Tenant

DTOs internos devem preservar `user_id` quando necessário para:

- ownership;
- persistência;
- eventos;
- auditoria;
- jobs;
- integrações internas.

DTOs públicos não devem expor `user_id` sem necessidade funcional.

---

# 48. Segurança

DTOs nunca devem expor:

- `password_hash`;
- token armazenado;
- segredo;
- chave privada;
- Session;
- detalhes internos de autenticação;
- notas sensíveis sem autorização.

---

# 49. Senhas

Request DTO pode conter senha temporariamente.

Exemplo:

```python
@dataclass(frozen=True)
class RegisterUserRequest:
    full_name: str
    email: str
    password: str
    password_confirmation: str
```

Esse DTO:

- não deve ser logado;
- não deve ser persistido;
- deve ter ciclo de vida curto;
- não deve ser retornado.

---

# 50. Tokens

Tokens brutos podem existir apenas em DTOs de entrega imediata ou entrada.

Nunca devem aparecer em:

- logs;
- auditoria;
- eventos públicos;
- exports;
- cache;
- histórico.

---

# 51. Dados Terapêuticos

DTOs de terapia devem aplicar minimização.

Exemplo de listagem:

```python
@dataclass(frozen=True)
class TherapySessionSummaryDto:
    session_id: str
    occurred_at: datetime
    therapist_name: str
    clarity_after_session: int | None
```

Notas completas devem possuir contrato separado e autorização explícita.

---

# 52. Dados de Saúde

DTOs devem diferenciar:

- resumo;
- detalhe;
- exportação;
- Analytics;
- AI context.

Não reutilizar um DTO amplo para todos os cenários.

---

# 53. Serialização JSON

DTOs externos devem ser serializáveis.

Conversões comuns:

```text
UUID → string
Decimal → string ou número controlado
datetime → ISO 8601
Enum → código
tuple → array
```

---

# 54. CSV e Excel

Export DTOs devem conter valores tabulares.

Evitar:

- objetos aninhados;
- Value Objects;
- listas complexas;
- Entities.

---

# 55. PDF

DTOs para PDF podem representar:

```text
ReportSectionDto
ReportTableDto
ReportMetricDto
```

O DTO organiza conteúdo.

O Exporter renderiza.

---

# 56. Versionamento

Contratos públicos devem ser versionados quando houver quebra de compatibilidade.

Exemplos:

```text
CharacterResponseV1
CharacterResponseV2
WorkoutRegisteredEventV1
```

DTOs internos podem evoluir de forma coordenada, mas mudanças devem manter documentação sincronizada.

---

# 57. Compatibilidade

Adicionar campo opcional tende a ser compatível.

Remover ou renomear campo tende a ser incompatível.

Alterar tipo é incompatível na maioria dos contratos externos.

Toda quebra exige:

- nova versão;
- migration de consumidor;
- ADR quando relevante;
- atualização de testes.

---

# 58. DTOs entre Módulos

Módulos devem utilizar apenas contratos públicos.

Permitido:

```python
from lifeos.modules.character.public.contracts import CharacterSummaryContract
```

Proibido:

```python
from lifeos.modules.character.application.dto import InternalCharacterDto
```

---

# 59. DTOs de Eventos

Event DTOs devem possuir:

```text
event_id
event_type
occurred_at
user_id quando aplicável
aggregate_id quando aplicável
version
```

Payload deve ser mínimo.

---

# 60. DTOs de Jobs

Jobs devem transportar:

- IDs;
- período;
- parâmetros;
- correlation ID;
- idempotency key.

Não transportar Aggregate completo.

---

# 61. DTOs de Cache

DTOs de cache devem ser:

- versionáveis;
- serializáveis;
- mínimos;
- descartáveis;
- livres de dados sensíveis desnecessários.

Cache não é fonte de verdade.

---

# 62. DTOs de Auditoria

Exemplo:

```python
@dataclass(frozen=True)
class AuditEntryDto:
    actor_user_id: str | None
    action: str
    entity_type: str | None
    entity_id: str | None
    occurred_at: datetime
    metadata: Mapping[str, object] | None
```

Metadata deve ser sanitizada.

---

# 63. DTOs de Configuração

Configurações devem utilizar objetos tipados.

Exemplo:

```python
@dataclass(frozen=True)
class PasswordResetSettingsDto:
    expiration_minutes: int
    maximum_attempts: int
```

Não espalhar `dict` de configuração.

---

# 64. DTOs de Feature Flags

Exemplo:

```python
@dataclass(frozen=True)
class FeatureFlagsDto:
    ai_mentor_enabled: bool
    exports_enabled: bool
    background_jobs_enabled: bool
```

Feature flags não substituem autorização.

---

# 65. DTOs de Analytics

Devem representar:

- séries temporais;
- métricas;
- correlações;
- tendências;
- períodos;
- confiança.

Exemplo:

```python
@dataclass(frozen=True)
class TimeSeriesPointDto:
    date: date
    value: Decimal | None
```

---

# 66. DTOs de Gamificação

Exemplos:

```text
ExperienceGrantResult
LevelProgressDto
AchievementSummaryDto
QuestProgressDto
CharacterAttributeDto
```

Devem utilizar códigos estáveis.

---

# 67. DTOs de Character

Separar:

```text
CharacterSummaryDto
CharacterDetailDto
CharacterSheetReadModel
CharacterSheetViewModel
```

Não criar um único DTO gigante.

---

# 68. DTOs de Authentication

Exemplos:

```text
RegisterUserCommand
AuthenticateUserCommand
AuthenticationResult
RequestPasswordResetCommand
ResetPasswordCommand
SessionSummaryDto
```

Nunca retornar `password_hash`.

---

# 69. DTOs de Workout

Exemplos:

```text
RegisterWorkoutCommand
UpdateWorkoutCommand
WorkoutSummaryDto
WorkoutHistoryItem
WorkoutStatisticsReadModel
WorkoutExportRow
```

---

# 70. DTOs de Health

Exemplos:

```text
RegisterSleepCommand
SleepRecordResult
WellbeingSummaryDto
BodyCompositionSummaryDto
HealthDashboardReadModel
```

---

# 71. DTOs de Reading

Exemplos:

```text
CreateBookCommand
RegisterReadingSessionCommand
BookSummaryDto
ReadingInsightDto
ReadingStatisticsReadModel
```

---

# 72. DTOs de Therapy

Exemplos:

```text
RegisterTherapistCommand
RegisterTherapySessionCommand
TherapySessionSummaryDto
TherapySessionDetailDto
```

Detalhe exige autorização específica.

---

# 73. DTOs de Habits

Exemplos:

```text
CreateHabitCommand
CompleteHabitCommand
HabitSummaryDto
HabitRecordDto
HabitStreakDto
```

---

# 74. DTOs de Reports

Exemplos:

```text
GenerateReportCommand
ReportExportResult
ReportStatusDto
ReportDownloadDto
```

`ReportDownloadDto` não deve expor path interno sem necessidade.

---

# 75. DTOs de AI Mentor

Exemplos:

```text
MentorContextDto
RecommendationDto
MissionSuggestionDto
CoachMessageDto
```

A resposta de IA deve ser validada antes de virar DTO público.

---

# 76. DTOs de Administração

Exemplos:

```text
UserAdministrationSummaryDto
AuditLogItemDto
SystemMetricDto
ConfigurationEntryDto
```

Exigem autorização administrativa.

---

# 77. Testes Unitários

DTOs devem ser testados quando possuírem:

- defaults;
- serialização;
- campos opcionais;
- generics;
- versionamento;
- validação estrutural.

Mappers associados devem possuir testes completos.

---

# 78. Testes de Contrato

Contratos públicos devem possuir testes que garantam:

- nomes de campos;
- tipos;
- obrigatoriedade;
- serialização;
- compatibilidade;
- versionamento;
- ausência de dados sensíveis.

---

# 79. Snapshot Tests

Podem ser utilizados para:

- JSON de API;
- payload de evento;
- export DTO;
- resposta de integração.

Snapshots não substituem testes semânticos.

---

# 80. Testes Multi-Tenant

Validar que:

- DTO de usuário A não contém dados de B;
- exports respeitam ownership;
- eventos preservam tenant;
- Read Models aplicam `user_id`;
- ViewModels não misturam contextos.

---

# 81. Testes de Segurança

Validar ausência de:

- senha;
- hash;
- token;
- segredo;
- notas privadas indevidas;
- path interno;
- configuração sensível;
- stack trace.

---

# 82. Performance

DTOs devem ser pequenos e adequados ao caso de uso.

Evitar:

- objetos gigantes;
- duplicação de payload;
- coleções sem limite;
- histórico completo;
- aninhamento excessivo;
- metadados desnecessários.

---

# 83. Anti-patterns

São proibidos:

## Entity como DTO

```python
return character
```

## ORM Model como DTO

```python
return CharacterModel
```

## DTO com comportamento de domínio

```python
class CharacterDto:
    def grant_experience(...):
        ...
```

## DTO com Repository

```python
class WorkoutDto:
    repository: WorkoutRepository
```

## DTO genérico

```python
GenericDataDto
```

## Dicionário como contrato principal

```python
return {"data": ...}
```

## DTO gigante universal

Um único `UserDto` para login, perfil, admin, export e IA.

## Exposição sensível

```python
password_hash: str
```

em resposta.

---

# 84. Como o Gemini deve Utilizar este Documento

Antes de criar um DTO, o agente deve responder:

1. Qual fronteira está sendo atravessada?
2. Qual é a origem?
3. Qual é o destino?
4. O DTO é Command, Query, Result, Read Model ou ViewModel?
5. Existe contrato equivalente?
6. O DTO contém apenas dados necessários?
7. Há dado sensível?
8. Há contexto Multi-Tenant?
9. O DTO precisa ser público?
10. O contrato precisa de versão?
11. Os tipos são explícitos?
12. A coleção precisa de paginação?
13. O DTO é imutável?
14. Existe Mapper?
15. Existem testes de contrato?
16. A documentação foi atualizada?

---

# 85. Checklist de Implementação

- [ ] Categoria do DTO identificada.
- [ ] Nome específico definido.
- [ ] Camada correta utilizada.
- [ ] Tipagem explícita.
- [ ] Imutabilidade aplicada.
- [ ] Campos mínimos.
- [ ] Sem comportamento de domínio.
- [ ] Sem dependência de infraestrutura.
- [ ] Sem Entity exposta.
- [ ] Sem ORM Model exposto.
- [ ] Dados sensíveis removidos.
- [ ] Multi-Tenant preservado.
- [ ] Datas padronizadas.
- [ ] Enums convertidos em códigos estáveis.
- [ ] Decimal avaliado.
- [ ] Paginação aplicada quando necessária.
- [ ] Mapper criado.
- [ ] Testes criados.
- [ ] Contrato versionado quando necessário.
- [ ] Documentação atualizada.

---

# 86. Critérios de Aceite

Este documento será considerado atendido quando:

- toda fronteira utilizar contratos explícitos;
- Commands e Queries estiverem separados;
- Results não expuserem Entities;
- Read Models forem usados em consultas complexas;
- ViewModels permanecerem na Presentation;
- módulos utilizarem apenas contratos públicos;
- dados sensíveis forem protegidos;
- Multi-Tenant estiver preservado;
- contratos externos forem versionáveis;
- testes garantirem estabilidade dos DTOs.

---

# 87. Definition of Done

Um DTO só estará concluído quando:

- [ ] Sua finalidade estiver clara.
- [ ] Sua categoria estiver correta.
- [ ] Sua localização estiver correta.
- [ ] Seus campos estiverem tipados.
- [ ] Sua imutabilidade estiver garantida.
- [ ] Nenhum dado desnecessário estiver presente.
- [ ] Nenhum dado sensível estiver exposto.
- [ ] O Mapper correspondente existir.
- [ ] Os testes passarem.
- [ ] A compatibilidade estiver avaliada.
- [ ] A documentação estiver sincronizada.

---

# 88. Declaração Final

DTOs são contratos de transporte, não modelos de domínio.

Eles existem para permitir que cada camada, módulo e integração do LifeOS evolua de forma independente, sem expor detalhes internos.

Todo DTO deve ser pequeno, explícito, imutável, seguro, fortemente tipado e adequado a uma única fronteira.

A qualidade dos contratos de dados determina a estabilidade da arquitetura, a segurança das integrações e a capacidade de evolução do LifeOS.
