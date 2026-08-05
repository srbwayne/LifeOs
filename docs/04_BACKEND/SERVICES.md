# SERVICES

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Services  
**Camadas Relacionadas:** Domain, Application e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal e Monólito Modular

---

# 1. Objetivo

Este documento define o padrão oficial de Services do LifeOS.

Seu objetivo é estabelecer:

- o papel de cada tipo de Service;
- onde cada Service deve existir;
- quais responsabilidades pertencem a cada camada;
- como regras de negócio devem ser organizadas;
- como múltiplos módulos devem ser coordenados;
- como integrações externas devem ser isoladas;
- como Services devem ser nomeados, testados e versionados;
- como evitar Services genéricos, gigantes ou acoplados.

Toda implementação que utilize o sufixo `Service` deverá respeitar este documento.

---

# 2. Escopo

Este documento cobre:

- Domain Services;
- Application Services;
- Infrastructure Services;
- Services de consulta;
- Services de coordenação;
- Services de integração;
- Services de segurança;
- Services de Analytics;
- Services de Gamificação;
- Services de IA;
- dependências permitidas;
- tratamento de erros;
- transações;
- eventos;
- Multi-Tenant;
- testes;
- anti-patterns;
- regras para agentes de IA.

Este documento complementa:

- `REPOSITORIES.md`;
- `DATABASE.md`;
- `docs/02_ARCHITECTURE/02_CLEAN_ARCHITECTURE.md`;
- `docs/02_ARCHITECTURE/03_DDD.md`;
- `docs/02_ARCHITECTURE/05_MODULAR_MONOLITH.md`;
- `docs/02_ARCHITECTURE/04_HEXAGONAL.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`;
- `02_ARCHITECTURE/08_EVENTS.md`.

---

# 3. Princípio Central

Service não é um recipiente genérico para qualquer código.

Todo Service deve possuir:

- responsabilidade específica;
- camada definida;
- linguagem de domínio;
- dependências explícitas;
- fronteira clara;
- testes correspondentes.

Antes de criar um Service, deve-se verificar se a responsabilidade pertence a:

- Entity;
- Value Object;
- Aggregate;
- Use Case;
- Policy;
- Specification;
- Repository;
- Adapter;
- Presenter.

Se pertencer a algum desses elementos, não deve ser movida para um Service apenas por conveniência.

---

# 4. Tipos Oficiais de Services

O LifeOS reconhece três categorias principais:

```text
Domain Service
Application Service
Infrastructure Service
```

Também poderão existir Services especializados de leitura ou coordenação, desde que pertençam claramente a uma dessas categorias.

---

# 5. Domain Service

Domain Service representa uma regra de negócio que:

- não pertence naturalmente a uma única Entity;
- envolve múltiplos objetos do domínio;
- permanece independente de tecnologia;
- utiliza linguagem ubíqua;
- pode ser testada sem banco ou interface.

Exemplos:

```text
CharacterEvolutionService
ExperienceCalculationService
QuestCompletionService
RecoveryScoreService
AchievementEligibilityService
StreakCalculationService
```

---

# 6. Localização de Domain Services

Estrutura:

```text
src/lifeos/modules/<module>/domain/services/
```

Exemplo:

```text
src/lifeos/modules/game/domain/services/
├── experience_calculation_service.py
├── quest_completion_service.py
└── achievement_eligibility_service.py
```

---

# 7. Exemplo de Domain Service

```python
class ExperienceCalculationService:
    def calculate_for_workout(
        self,
        duration_minutes: int,
        perceived_effort: int,
        policy: ExperiencePolicy,
    ) -> ExperiencePoints:
        base = policy.base_experience_for_workout(
            duration_minutes=duration_minutes,
        )

        multiplier = policy.effort_multiplier(
            perceived_effort=perceived_effort,
        )

        return ExperiencePoints(
            value=round(base * multiplier),
        )
```

Esse Service:

- não conhece Repository;
- não conhece SQLAlchemy;
- não conhece Streamlit;
- não conhece sessão;
- não executa commit.

---

# 8. Quando Usar Domain Service

Utilizar quando:

- a regra envolve mais de uma Entity;
- a regra não pertence claramente a um Aggregate;
- a regra representa conceito de negócio;
- a regra precisa ser reutilizada;
- a regra deve permanecer independente de infraestrutura.

Não utilizar para:

- coordenação de caso de uso;
- acesso ao banco;
- envio de e-mail;
- logging;
- transformação visual;
- chamadas HTTP.

---

# 9. Application Service

Application Service coordena fluxos de aplicação.

Pode:

- chamar Use Cases;
- coordenar múltiplos módulos;
- iniciar transações;
- utilizar Repositories por contrato;
- publicar eventos;
- aplicar autorização;
- compor resultados;
- chamar Ports;
- retornar DTOs.

Não deve:

- conter regra de negócio central;
- depender de Streamlit;
- depender de SQLAlchemy;
- acessar Models ORM;
- conhecer detalhes de infraestrutura.

---

# 10. Localização de Application Services

Estrutura:

```text
src/lifeos/modules/<module>/application/services/
```

Exemplo:

```text
src/lifeos/modules/auth/application/services/
├── account_initialization_service.py
└── authentication_application_service.py
```

---

# 11. Exemplo de Application Service

```python
class AccountInitializationService:
    def __init__(
        self,
        user_repository: UserRepository,
        character_facade: CharacterModuleFacade,
        preference_repository: UserPreferenceRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._user_repository = user_repository
        self._character_facade = character_facade
        self._preference_repository = preference_repository
        self._unit_of_work = unit_of_work

    def initialize(
        self,
        user: User,
    ) -> AccountInitializationResult:
        with self._unit_of_work:
            self._user_repository.save(user)

            character = self._character_facade.create_initial_character(
                user_id=str(user.id),
                player_name=user.full_name,
            )

            preferences = UserPreferences.create_default(
                user_id=user.id,
            )

            self._preference_repository.save(preferences)
            self._unit_of_work.commit()

        return AccountInitializationResult(
            user_id=str(user.id),
            character_id=character.character_id,
        )
```

---

# 12. Use Case e Application Service

Use Case representa uma funcionalidade específica.

Application Service pode coordenar operações reutilizadas por múltiplos Use Cases.

Exemplo:

```text
RegisterUserUseCase
    ↓
AccountInitializationService
```

Outro exemplo:

```text
GenerateWeeklySummaryUseCase
    ↓
AnalyticsCompositionService
```

Não criar Application Service apenas para delegar uma única chamada sem acrescentar coordenação.

---

# 13. Infrastructure Service

Infrastructure Service implementa capacidades técnicas.

Exemplos:

```text
SmtpEmailService
BcryptPasswordService
LocalBackupService
GeminiAIService
SqlAlchemyTransactionService
FileExportService
AuditLogService
```

Preferência de nomenclatura:

```text
EmailSender
PasswordHasher
BackupStorage
AIProvider
```

quando a abstração for um Port.

A implementação concreta pode utilizar sufixo técnico:

```text
SmtpEmailSender
BcryptPasswordHasher
LocalBackupStorage
GeminiAIProvider
```

---

# 14. Localização de Infrastructure Services

Estrutura compartilhada:

```text
src/lifeos/infrastructure/
```

Ou específica do módulo:

```text
src/lifeos/modules/<module>/infrastructure/services/
```

A escolha depende da propriedade da integração.

---

# 15. Exemplo de Infrastructure Service

```python
class SmtpEmailSender(EmailSender):
    def __init__(
        self,
        configuration: EmailConfiguration,
    ) -> None:
        self._configuration = configuration

    def send_password_reset(
        self,
        recipient: str,
        reset_token: str,
        expires_in_minutes: int,
    ) -> None:
        ...
```

---

# 16. Regra de Dependência

```text
Presentation
    ↓
Application Service
    ↓
Domain Service
```

Infrastructure implementa Ports utilizados por Application.

Proibido:

```text
Domain Service
    ↓
Infrastructure Service
```

Proibido:

```text
Application Service
    ↓
SqlAlchemy concrete service
```

A implementação concreta deve ser injetada por Port.

---

# 17. Services e Entidades

A regra deve permanecer na Entity quando:

- altera apenas seu próprio estado;
- protege sua própria invariante;
- representa comportamento natural do objeto.

Exemplo:

```python
character.grant_experience(amount)
```

Não mover para:

```python
CharacterService.grant_experience(character, amount)
```

quando a própria Entity pode proteger a regra.

---

# 18. Services e Value Objects

Validações de valor pertencem ao Value Object.

Exemplo:

```python
Email.create(raw_email)
ExperiencePoints(value)
Percentage(value)
```

Não criar:

```text
EmailValidationService
PercentageValidationService
```

sem necessidade real.

---

# 19. Services e Policies

Quando a regra for variável, configurável ou substituível, utilizar Policy.

Exemplo:

```text
ExperiencePolicy
RewardPolicy
StreakPolicy
PasswordPolicy
```

O Service pode utilizar a Policy, mas não deve ocultá-la.

---

# 20. Services e Specifications

Specifications representam critérios booleanos reutilizáveis.

Exemplo:

```text
EligibleForLevelUpSpecification
QuestCompletedSpecification
AchievementUnlockedSpecification
```

Um Service pode coordenar Specifications, mas não deve duplicar suas condições.

---

# 21. Services e Repositories

Domain Services devem evitar Repository quando possível.

Application Services podem depender de Repository Interfaces.

Infrastructure Services podem utilizar mecanismos técnicos.

Exemplo permitido:

```python
class CharacterApplicationService:
    def __init__(
        self,
        repository: CharacterRepository,
    ) -> None:
        self._repository = repository
```

Exemplo proibido:

```python
class CharacterEvolutionService:
    def __init__(
        self,
        repository: SqlAlchemyCharacterRepository,
    ) -> None:
        ...
```

---

# 22. Services e Unit of Work

Application Services podem controlar Unit of Work quando coordenam fluxo transacional.

Exemplo:

```python
with self._unit_of_work:
    ...
    self._unit_of_work.commit()
```

Domain Services nunca controlam transação.

Infrastructure Services não devem decidir fronteira transacional de negócio.

---

# 23. Services e Eventos

Domain Services podem produzir Domain Events por meio de Entities ou resultado explícito.

Application Services podem:

- coletar eventos;
- publicar após commit;
- coordenar handlers;
- emitir Application Events.

Infrastructure Services não devem decidir quais eventos de negócio existem.

---

# 24. Exemplo de Resultado com Evento

```python
@dataclass(frozen=True)
class ExperienceGrantResult:
    previous_level: int
    current_level: int
    granted_experience: int
    events: tuple[DomainEvent, ...]
```

---

# 25. Services e Multi-Tenant

Todo Application Service operacional deve receber ou obter `user_id`.

Esse identificador deve:

- vir do contexto autenticado;
- ser propagado aos Repositories;
- ser usado nos contratos públicos;
- ser validado em integrações entre módulos.

Nunca confiar em `user_id` fornecido livremente pela interface.

---

# 26. Current User Context

A Application pode utilizar:

```python
class CurrentUserProvider(Protocol):
    def get_current_user_id(self) -> UserId:
        ...
```

O Adapter concreto pode usar sessão Streamlit.

O Service não conhece Streamlit.

---

# 27. Services Síncronos

Utilizar fluxo síncrono quando:

- o resultado é necessário imediatamente;
- a operação faz parte da mesma transação;
- o usuário depende da resposta;
- a falha deve interromper o caso de uso.

Exemplo:

```text
RegisterUser
→ create Character
→ create Preferences
→ start Session
```

---

# 28. Services Assíncronos

Utilizar eventos ou jobs quando:

- a resposta imediata não é necessária;
- o processamento é pesado;
- múltiplos consumidores precisam reagir;
- consistência eventual é aceitável.

Exemplos:

```text
Generate Analytics Snapshot
Generate AI Recommendation
Export Report
Send Notification
Rebuild Dashboard Cache
```

---

# 29. Services de Consulta

Services de consulta podem compor múltiplos Read Models.

Exemplo:

```python
class DashboardCompositionService:
    def __init__(
        self,
        character_query: CharacterQueryRepository,
        health_query: HealthQueryRepository,
        workout_query: WorkoutQueryRepository,
        gamification_query: GamificationQueryRepository,
    ) -> None:
        ...
```

Esse Service:

- não altera estado;
- não executa regra de domínio;
- retorna DTO ou Read Model;
- pode coordenar múltiplas consultas.

---

# 30. Services de Analytics

Services de Analytics devem:

- receber dados estruturados;
- aplicar cálculos documentados;
- retornar resultados independentes da UI;
- não gerar gráficos diretamente;
- não acessar Streamlit;
- não misturar recomendação de IA com cálculo estatístico.

Exemplos:

```text
CorrelationAnalysisService
TrendAnalysisService
KpiCalculationService
HealthScoreService
```

---

# 31. Services de Gamificação

Exemplos:

```text
ExperienceCalculationService
LevelProgressionService
QuestEvaluationService
AchievementEvaluationService
RewardGrantService
StreakEvaluationService
```

Esses Services devem permanecer no módulo `game`, salvo responsabilidade específica de Character.

---

# 32. Services de Character

Exemplos:

```text
CharacterEvolutionService
AttributeProgressionService
CharacterInitializationService
```

O módulo Character é proprietário de:

- estado do Character;
- níveis;
- atributos;
- histórico de evolução.

O módulo Game é proprietário de:

- regras de XP;
- Quests;
- Rewards;
- Achievements;
- Skills.

---

# 33. Services de Authentication

Exemplos:

```text
AuthenticationService
PasswordResetService
SessionManagementService
AccountInitializationService
```

Abstrações técnicas:

```text
PasswordHasher
TokenGenerator
EmailSender
CurrentUserProvider
```

---

# 34. Services de Health

Exemplos:

```text
RecoveryScoreService
SleepQualityService
BodyCompositionAnalysisService
WellbeingEvaluationService
```

Esses Services não podem emitir diagnóstico médico.

Devem produzir indicadores internos do produto.

---

# 35. Services de Workout

Exemplos:

```text
WorkoutRegistrationService
WorkoutFrequencyService
WorkoutProgressService
```

O registro básico tende a ser um Use Case.

Criar Service apenas quando houver coordenação ou regra reutilizável.

---

# 36. Services de Reading

Exemplos:

```text
ReadingProgressService
BookCompletionService
ReadingInsightService
```

---

# 37. Services de Therapy

Exemplos:

```text
TherapySessionService
ClarityProgressService
```

Notas terapêuticas são dados sensíveis.

Services devem evitar logs com seu conteúdo.

---

# 38. Services de Habits

Exemplos:

```text
HabitCompletionService
StreakCalculationService
HabitFrequencyService
```

---

# 39. Services de AI Mentor

A Application deve depender de:

```text
AIProvider
```

Exemplos de Application Services:

```text
RecommendationGenerationService
WeeklyMentorSummaryService
MissionSuggestionService
```

Implementações concretas:

```text
GeminiAIProvider
OpenAIProvider
LocalLLMProvider
```

---

# 40. Services de Reports

Exemplos:

```text
ReportGenerationService
ExportOrchestrationService
BackupReportService
```

Exportadores concretos devem ser Adapters:

```text
CsvExporter
ExcelExporter
PdfExporter
```

---

# 41. Services de Segurança

Exemplos de Ports:

```text
PasswordHasher
TokenGenerator
EncryptionService
PermissionEvaluator
```

Implementações concretas:

```text
BcryptPasswordHasher
SecureTokenGenerator
AesEncryptionService
```

---

# 42. Services de Auditoria

Auditoria deve ser tratada por Port ou Service técnico.

Exemplo:

```python
class AuditLogger(Protocol):
    def record(
        self,
        entry: AuditEntry,
    ) -> None:
        ...
```

Não espalhar gravação de auditoria diretamente em todas as classes.

---

# 43. Nomenclatura

Nomes devem comunicar responsabilidade.

Correto:

```text
ExperienceCalculationService
AccountInitializationService
DashboardCompositionService
PasswordResetService
```

Evitar:

```text
GeneralService
CommonService
UtilsService
ManagerService
LifeOSService
DataService
HelperService
```

---

# 44. Sufixo `Service`

O sufixo deve ser utilizado somente quando a classe realmente representa um Service.

Não utilizar em:

- Entity;
- Repository;
- Use Case;
- Adapter;
- Mapper;
- Presenter;
- Validator;
- Factory;
- Policy;
- Specification.

---

# 45. Tamanho

Um Service deve ser pequeno e coeso.

Sinais de problema:

- dezenas de métodos não relacionados;
- dependência de muitos módulos;
- mais de uma responsabilidade;
- nome genérico;
- muitos Repositories;
- muitas condições;
- mistura de leitura e escrita;
- mistura de infraestrutura e domínio.

---

# 46. Quantidade de Dependências

Um Service com muitas dependências deve ser revisado.

Referência prática:

```text
1 a 5 dependências: normal
6 a 8 dependências: revisar
mais de 8: provável problema de design
```

Isso não é regra absoluta, mas é sinal arquitetural.

---

# 47. Coesão

Todos os métodos de um Service devem contribuir para o mesmo objetivo.

Exemplo coeso:

```text
PasswordResetService
├── request_reset
├── validate_token
└── reset_password
```

Exemplo não coeso:

```text
UserService
├── login
├── generate_report
├── grant_xp
├── send_email
└── calculate_sleep
```

---

# 48. Stateless

Services devem ser stateless sempre que possível.

Permitido manter:

- dependências;
- configuração imutável;
- Policies;
- Ports.

Evitar manter:

- usuário atual;
- Session;
- resultados temporários;
- cache local implícito;
- estado mutável entre chamadas.

---

# 49. Imutabilidade

DTOs e resultados de Services devem ser imutáveis quando possível.

Exemplo:

```python
@dataclass(frozen=True)
class PasswordResetResult:
    user_id: str
    token_expires_at: datetime
```

---

# 50. Tratamento de Erros

Services devem lançar erros coerentes com sua camada.

## Domain Service

```text
InvalidExperienceError
QuestAlreadyCompletedError
```

## Application Service

```text
UserNotFoundError
PermissionDeniedError
OperationConflictError
```

## Infrastructure Service

```text
EmailDeliveryError
ExternalProviderUnavailableError
BackupStorageError
```

Erros técnicos devem ser traduzidos antes de chegar à interface.

---

# 51. Logging

Domain Services não devem depender de logger.

Application Services podem registrar:

- início de operação crítica;
- conclusão;
- falha;
- contexto técnico sem dados sensíveis.

Infrastructure Services podem registrar detalhes técnicos.

Nunca registrar:

- senha;
- token;
- notas terapêuticas;
- payload completo de saúde;
- dados pessoais desnecessários.

---

# 52. Configuração

Services não devem ler variáveis de ambiente diretamente.

Configuração deve ser injetada.

Exemplo:

```python
class PasswordResetService:
    def __init__(
        self,
        expiration_minutes: int,
    ) -> None:
        self._expiration_minutes = expiration_minutes
```

---

# 53. Dependency Injection

Services devem receber dependências por construtor.

Exemplo:

```python
class RecommendationGenerationService:
    def __init__(
        self,
        ai_provider: AIProvider,
        analytics_query: AnalyticsQueryRepository,
        clock: Clock,
    ) -> None:
        ...
```

Proibido:

```python
self._provider = GeminiAIProvider()
```

dentro do Service.

---

# 54. Composition Root

Services concretos devem ser compostos em:

```text
src/lifeos/bootstrap/container.py
```

ou Factories de bootstrap aprovadas.

---

# 55. Facades

Um módulo pode expor Facade pública.

Exemplo:

```python
class GameModuleFacade:
    def grant_experience(
        self,
        request: ExperienceGrantRequest,
    ) -> ExperienceGrantResult:
        ...
```

A Facade:

- representa API pública;
- delega para Application Services ou Use Cases;
- não expõe internals;
- não contém lógica de infraestrutura.

---

# 56. Services e Facades

Facade não substitui todos os Services.

Fluxo:

```text
Module Facade
    ↓
Application Service / Use Case
    ↓
Domain
```

---

# 57. Services e Controllers

Controllers podem chamar:

- Use Cases;
- Application Services;
- Facades públicas.

Controllers não devem chamar Domain Services diretamente.

---

# 58. Services e UI

Streamlit nunca chama Infrastructure Service diretamente.

Fluxo correto:

```text
Streamlit Page
    ↓
Controller
    ↓
Use Case / Application Service
    ↓
Port
    ↓
Infrastructure Service
```

---

# 59. Services e Reutilização

Reutilização deve ocorrer quando existe responsabilidade realmente compartilhada.

Não extrair Service apenas para evitar duas linhas duplicadas.

A abstração deve representar conceito real.

---

# 60. Services e Idempotência

Services acionados por eventos devem ser idempotentes.

Exemplo:

```text
GrantExperienceFromWorkoutService
```

deve impedir processamento duplicado por `event_id`.

---

# 61. Services e Retry

Retry pertence a infraestrutura ou coordenação de aplicação.

Não implementar loops de retry dentro de Domain Service.

---

# 62. Services e Cache

Cache deve ser Adapter ou Decorator explícito.

Exemplo:

```text
CachedDashboardCompositionService
```

ou:

```text
DashboardCache
```

Nunca esconder cache mutável dentro de Service sem contrato.

---

# 63. Services e Performance

Application Services devem evitar:

- múltiplas consultas redundantes;
- N+1;
- carregamento completo de histórico;
- cálculos pesados dentro de transação;
- chamadas externas durante locks prolongados.

---

# 64. Services e Transações Externas

Chamadas externas devem preferencialmente ocorrer após commit.

Exemplo:

```text
Persistir token
→ Commit
→ Enviar e-mail
```

Quando a entrega externa for essencial, utilizar estratégia de evento ou Outbox.

---

# 65. Testes de Domain Service

Devem ser unitários e sem infraestrutura.

Exemplo:

```python
def test_calculates_workout_experience() -> None:
    service = ExperienceCalculationService()
    policy = FixedExperiencePolicy()

    result = service.calculate_for_workout(
        duration_minutes=60,
        perceived_effort=8,
        policy=policy,
    )

    assert result.value == 120
```

---

# 66. Testes de Application Service

Devem utilizar:

- Repositories em memória;
- Fakes;
- FixedClock;
- FakeUnitOfWork;
- FakeEventPublisher;
- FakeProvider.

---

# 67. Testes de Infrastructure Service

Devem validar:

- integração real;
- timeout;
- erro;
- configuração;
- serialização;
- retry;
- segurança;
- contrato.

Exemplos:

```text
SmtpEmailSenderIntegrationTest
BcryptPasswordHasherContract
LocalBackupStorageIntegrationTest
```

---

# 68. Testes de Contrato

Ports com múltiplas implementações devem possuir testes de contrato.

Exemplo:

```text
AIProviderContract
├── GeminiAIProvider
├── OpenAIProvider
└── LocalLLMProvider
```

---

# 69. Teste Multi-Tenant

Todo Application Service operacional deve possuir teste que prove:

```text
Usuário A não acessa nem altera dados de Usuário B.
```

---

# 70. Teste Transacional

Services transacionais devem validar:

- commit em sucesso;
- rollback em falha;
- ausência de estado parcial;
- eventos publicados somente no momento correto.

---

# 71. Estrutura de Arquivos

```text
module/
├── domain/
│   └── services/
├── application/
│   └── services/
└── infrastructure/
    └── services/
```

Quando a integração for compartilhada:

```text
src/lifeos/infrastructure/<capability>/
```

---

# 72. Anti-patterns

São proibidos:

## Service Genérico

```text
UserService
DataService
CommonService
```

com responsabilidades amplas.

## Service como DAO

```python
class CharacterService:
    def find_all_from_database(self):
        ...
```

## Domain Service com SQLAlchemy

```python
class XPService:
    def __init__(self, session: Session):
        ...
```

## Application Service com Streamlit

```python
import streamlit as st
```

## Infrastructure Service com regra de domínio

```python
class SmtpEmailSender:
    def calculate_user_level(...):
        ...
```

## Service Locator

```python
service = Container.get("service")
```

dentro do domínio.

## Service gigante

Classe responsável por autenticação, Character, Analytics e Reports.

---

# 73. Como o Gemini deve Utilizar este Documento

Antes de criar um Service, o agente deve responder:

1. A responsabilidade pertence a uma Entity?
2. Pertence a um Value Object?
3. Pertence a um Use Case?
4. Pertence a uma Policy?
5. Pertence a um Repository?
6. Qual tipo de Service é?
7. Em qual camada deve existir?
8. Quais dependências são permitidas?
9. Existe regra Multi-Tenant?
10. Existe transação?
11. Existe evento?
12. A classe está coesa?
13. O nome comunica a responsabilidade?
14. Há risco de Service gigante?
15. Existem testes adequados?
16. A documentação foi atualizada?

---

# 74. Checklist de Implementação

- [ ] Tipo de Service identificado.
- [ ] Responsabilidade única definida.
- [ ] Nome específico escolhido.
- [ ] Camada correta utilizada.
- [ ] Dependências permitidas.
- [ ] Injeção por construtor.
- [ ] Multi-Tenant aplicado.
- [ ] Transação definida quando necessária.
- [ ] Eventos avaliados.
- [ ] Repositories usados apenas por contrato.
- [ ] Nenhum framework no Domain.
- [ ] Nenhum SQL na Application.
- [ ] Nenhuma regra de negócio na Infrastructure.
- [ ] Erros traduzidos corretamente.
- [ ] Logging sem dados sensíveis.
- [ ] Testes unitários criados.
- [ ] Testes de contrato criados quando necessários.
- [ ] Testes Multi-Tenant criados.
- [ ] Documentação atualizada.

---

# 75. Critérios de Aceite

Este documento será considerado atendido quando:

- todos os Services possuírem categoria clara;
- Domain Services permanecerem independentes;
- Application Services coordenarem fluxos sem conter regra central;
- Infrastructure Services implementarem Ports;
- Services genéricos forem evitados;
- Multi-Tenant for preservado;
- transações forem controladas corretamente;
- eventos forem utilizados de forma coerente;
- testes cobrirem comportamento e contratos;
- dependências respeitarem a arquitetura oficial.

---

# 76. Definition of Done

Um Service só estará concluído quando:

- [ ] Sua responsabilidade estiver clara.
- [ ] Sua camada estiver correta.
- [ ] As dependências estiverem explícitas.
- [ ] O contrato estiver definido quando necessário.
- [ ] A implementação estiver desacoplada.
- [ ] Multi-Tenant estiver protegido.
- [ ] Erros estiverem tratados.
- [ ] Eventos estiverem coordenados corretamente.
- [ ] Testes unitários passarem.
- [ ] Testes de integração ou contrato passarem quando aplicável.
- [ ] A documentação estiver sincronizada.

---

# 77. Declaração Final

Services existem para representar regras ou coordenações que não pertencem naturalmente a outros elementos da arquitetura.

Eles não devem ser usados como destino padrão para qualquer lógica.

Todo Service deve ser pequeno, específico, testável, coerente com sua camada e alinhado à linguagem do LifeOS.

A clareza da responsabilidade deve prevalecer sobre a conveniência de concentrar código.
