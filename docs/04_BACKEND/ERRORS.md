# ERRORS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Erros e Exceções  
**Camadas Relacionadas:** Presentation, Application, Domain e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture

---

# 1. Objetivo

Este documento define o padrão oficial de erros e exceções do LifeOS.

Seu objetivo é estabelecer:

- como erros devem ser classificados;
- em qual camada cada erro deve existir;
- como exceções técnicas devem ser traduzidas;
- como erros de domínio devem ser representados;
- como a interface deve apresentar falhas;
- como códigos de erro devem ser padronizados;
- como dados sensíveis devem ser protegidos;
- como erros devem ser testados, registrados e auditados;
- como agentes de IA devem implementar novos fluxos de erro.

Toda falha previsível ou excepcional do LifeOS deverá seguir este documento.

---

# 2. Escopo

Este documento cobre:

- Domain Errors;
- Application Errors;
- Infrastructure Errors;
- Presentation Errors;
- Validation Errors;
- Authorization Errors;
- Authentication Errors;
- Multi-Tenant Errors;
- Persistence Errors;
- Integration Errors;
- Event Processing Errors;
- AI Provider Errors;
- códigos de erro;
- mensagens;
- tradução entre camadas;
- logging;
- auditoria;
- testes;
- anti-patterns;
- critérios de aceite;
- Definition of Done.

Este documento complementa:

- `VALIDATORS.md`;
- `USE_CASES.md`;
- `SERVICES.md`;
- `REPOSITORIES.md`;
- `UNIT_OF_WORK.md`;
- `DTOs.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`;
- `02_ARCHITECTURE/08_EVENTS.md`.

---

# 3. Princípio Central

Cada camada deve conhecer apenas erros compatíveis com sua responsabilidade.

Fluxo oficial:

```text
Infrastructure Error
        ↓
Application Error
        ↓
Presentation Error Model
        ↓
User Message
```

O Domain pode gerar erros próprios.

Esses erros devem ser preservados semanticamente e adaptados quando atravessarem fronteiras.

---

# 4. Classificação Oficial

O LifeOS reconhece as seguintes categorias:

```text
Domain Error
Application Error
Infrastructure Error
Presentation Error
Validation Error
Security Error
Integration Error
Event Error
```

Cada categoria deve possuir localização, semântica e tratamento próprios.

---

# 5. Domain Errors

Domain Errors representam violações de regras de negócio.

Exemplos:

```text
InvalidExperienceError
QuestAlreadyCompletedError
AchievementNotEligibleError
InvalidPercentageError
InvalidLevelError
HabitAlreadyCompletedError
CharacterAlreadyExistsError
```

Características:

- pertencem ao Domain;
- independem de framework;
- representam linguagem ubíqua;
- não expõem detalhes técnicos;
- podem ser testados sem infraestrutura.

---

# 6. Localização de Domain Errors

Estrutura:

```text
src/lifeos/modules/<module>/domain/exceptions/
```

Exemplo:

```text
src/lifeos/modules/game/domain/exceptions/
├── invalid_experience_error.py
├── quest_already_completed_error.py
└── achievement_not_eligible_error.py
```

---

# 7. Exemplo de Domain Error

```python
class InvalidExperienceError(Exception):
    code = "game.invalid_experience"

    def __init__(
        self,
        value: int,
    ) -> None:
        self.value = value
        super().__init__(
            "Experience value is invalid."
        )
```

A mensagem interna não precisa ser a mensagem final da interface.

---

# 8. Application Errors

Application Errors representam falhas de fluxo.

Exemplos:

```text
UserNotFoundError
WorkoutNotFoundError
OperationConflictError
PermissionDeniedError
AuthenticationRequiredError
ResourceOwnershipError
IdempotencyConflictError
```

Eles podem resultar de:

- recurso inexistente;
- precondição não atendida;
- falta de permissão;
- estado incompatível;
- falha de coordenação;
- conflito entre operações.

---

# 9. Localização de Application Errors

Estrutura:

```text
src/lifeos/modules/<module>/application/exceptions/
```

Exemplo:

```text
src/lifeos/modules/workout/application/exceptions/
├── workout_not_found_error.py
├── workout_access_denied_error.py
└── workout_operation_conflict_error.py
```

---

# 10. Infrastructure Errors

Infrastructure Errors representam falhas técnicas.

Exemplos:

```text
DatabaseUnavailableError
RepositoryPersistenceError
EmailDeliveryError
ExternalProviderUnavailableError
BackupStorageError
SerializationError
FileAccessError
```

Esses erros:

- pertencem à Infrastructure;
- podem encapsular exceções externas;
- não devem chegar diretamente à UI;
- devem ser traduzidos pela Application ou Adapter apropriado.

---

# 11. Localização de Infrastructure Errors

Estrutura compartilhada:

```text
src/lifeos/infrastructure/errors/
```

Ou específica:

```text
src/lifeos/modules/<module>/infrastructure/exceptions/
```

---

# 12. Presentation Errors

Presentation Errors representam falhas já adaptadas para exibição.

Exemplos:

```text
ValidationErrorViewModel
AuthenticationErrorViewModel
OperationFailedViewModel
NotFoundErrorViewModel
```

Eles não substituem erros internos.

São modelos de apresentação.

---

# 13. Validation Errors

Validation Errors representam entrada inválida.

Exemplo:

```python
@dataclass(frozen=True)
class ValidationErrorItem:
    field: str | None
    code: str
    message: str
```

Erro agregado:

```python
class CommandValidationError(Exception):
    def __init__(
        self,
        errors: tuple[ValidationErrorItem, ...],
    ) -> None:
        self.errors = errors
        super().__init__(
            "Command validation failed."
        )
```

---

# 14. Security Errors

Categoria oficial:

```text
AuthenticationRequiredError
InvalidCredentialsError
SessionExpiredError
SessionRevokedError
PermissionDeniedError
OwnershipViolationError
AccountBlockedError
InvalidTokenError
ExpiredTokenError
TokenAlreadyUsedError
```

Esses erros não devem revelar informação excessiva.

---

# 15. Authentication Error Safety

No login, mensagens devem evitar enumeração de usuários.

Preferir:

```text
E-mail ou senha inválidos.
```

Evitar:

```text
Usuário não existe.
```

ou:

```text
Senha incorreta.
```

---

# 16. Multi-Tenant Errors

Erros relacionados ao isolamento:

```text
ResourceOwnershipError
TenantAccessDeniedError
CrossTenantOperationError
```

A aplicação deve preferir resposta equivalente a recurso inexistente quando isso reduzir exposição.

Exemplo:

```text
Registro não encontrado.
```

em vez de:

```text
O registro pertence a outro usuário.
```

---

# 17. Persistence Errors

Exemplos técnicos:

```text
UniqueConstraintViolationError
ForeignKeyViolationError
OptimisticLockError
DatabaseLockedError
RepositoryReadError
RepositoryWriteError
```

Devem ser traduzidos para erros de aplicação.

Exemplo:

```text
IntegrityError
    ↓
EmailAlreadyRegisteredError
```

---

# 18. Integration Errors

Exemplos:

```text
EmailProviderUnavailableError
AIProviderTimeoutError
ExternalApiError
StorageUnavailableError
InvalidExternalResponseError
```

Devem conter contexto técnico mínimo e seguro.

---

# 19. Event Errors

Exemplos:

```text
EventPublicationError
EventHandlerError
EventDeserializationError
DeadEventError
DuplicateEventProcessingError
```

Devem preservar:

- `event_id`;
- tipo;
- handler;
- tentativas;
- correlation ID.

Nunca registrar payload sensível completo.

---

# 20. AI Provider Errors

Exemplos:

```text
AIProviderUnavailableError
AIProviderTimeoutError
AIResponseValidationError
AIQuotaExceededError
AIContentRejectedError
```

A interface deve apresentar mensagem segura e genérica quando necessário.

---

# 21. Hierarquia Base

Estrutura recomendada:

```python
class LifeOSError(Exception):
    code = "lifeos.error"


class DomainError(LifeOSError):
    code = "domain.error"


class ApplicationError(LifeOSError):
    code = "application.error"


class InfrastructureError(LifeOSError):
    code = "infrastructure.error"
```

Não criar hierarquia excessivamente profunda.

---

# 22. Código de Erro

Todo erro relevante deve possuir código estável.

Padrão:

```text
<module>.<category>.<error>
```

Exemplos:

```text
auth.validation.email_invalid
auth.security.invalid_credentials
workout.application.not_found
game.domain.invalid_experience
therapy.security.access_denied
infrastructure.database.unavailable
```

---

# 23. Regras para Códigos

Códigos devem:

- ser estáveis;
- usar lowercase;
- usar pontos;
- não depender de idioma;
- indicar módulo;
- indicar categoria;
- indicar problema.

Evitar:

```text
ERROR_01
GENERIC_ERROR
FAILURE
UNKNOWN
```

---

# 24. Mensagem Interna e Mensagem Externa

Mensagem interna:

- usada em logs;
- orientada a diagnóstico;
- sem dado sensível;
- pode ser técnica.

Mensagem externa:

- clara;
- amigável;
- localizada;
- segura;
- sem stack trace.

---

# 25. Estrutura Base de Erro

```python
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ErrorContext:
    code: str
    message: str
    field: str | None = None
    metadata: Mapping[str, object] | None = None
```

Metadata não deve conter dados sensíveis.

---

# 26. Tradução entre Camadas

Exemplo:

```text
SQLAlchemy IntegrityError
    ↓
UniqueConstraintViolationError
    ↓
EmailAlreadyRegisteredError
    ↓
ErrorResponseDto
    ↓
"E-mail já cadastrado."
```

Cada camada traduz apenas o que conhece.

---

# 27. Domain para Application

Domain Errors podem atravessar a Application quando sua semântica já for adequada.

Exemplo:

```text
QuestAlreadyCompletedError
```

Também podem ser traduzidos para um erro de caso de uso mais específico.

---

# 28. Infrastructure para Application

Infrastructure Errors sempre devem ser traduzidos.

Exemplo:

```python
try:
    repository.save(user)
except UniqueConstraintViolationError as exc:
    raise EmailAlreadyRegisteredError() from exc
```

---

# 29. Application para Presentation

Controller ou Presenter converte erro de aplicação em resposta visual.

Exemplo:

```python
class ErrorPresenter:
    def present(
        self,
        error: ApplicationError,
    ) -> ErrorViewModel:
        ...
```

---

# 30. Erros Esperados e Inesperados

Erros esperados:

- validação;
- not found;
- conflito;
- permissão;
- token expirado;
- regra de domínio.

Erros inesperados:

- bug;
- erro não mapeado;
- falha técnica desconhecida;
- corrupção de estado;
- exceção de biblioteca não traduzida.

Erros inesperados devem gerar:

- correlation ID;
- log completo seguro;
- mensagem genérica ao usuário.

---

# 31. Fallback Error

Mensagem padrão:

```text
Não foi possível concluir a operação.
```

O usuário pode receber um correlation ID.

Exemplo:

```text
Código de referência: 8f3b2a
```

---

# 32. Correlation ID

Toda operação relevante deve possuir correlation ID.

Esse identificador deve aparecer em:

- logs;
- erros inesperados;
- eventos;
- jobs;
- integrações;
- auditoria técnica.

---

# 33. Causas Encadeadas

Utilizar:

```python
raise ApplicationError() from exc
```

Isso preserva a causa para diagnóstico.

Nunca mostrar a cadeia completa ao usuário.

---

# 34. Stack Trace

Stack trace deve existir apenas em logs internos seguros.

Não retornar em:

- UI;
- API;
- export;
- evento público;
- e-mail;
- mensagem de usuário.

---

# 35. Logging

Erro esperado:

```text
INFO ou WARNING
```

Erro inesperado:

```text
ERROR
```

Falha crítica:

```text
CRITICAL
```

O nível deve refletir impacto, não apenas existência de exceção.

---

# 36. Dados Sensíveis em Logs

Nunca registrar:

- senha;
- hash;
- token;
- nota terapêutica;
- prompt completo;
- resposta completa de IA;
- biometria detalhada;
- dados pessoais desnecessários.

---

# 37. Auditoria

Erros de segurança e operações críticas podem gerar auditoria.

Exemplos:

- tentativas de login;
- token inválido;
- acesso negado;
- tentativa cross-tenant;
- alteração administrativa;
- restore falho;
- exportação negada.

---

# 38. Erros e Unit of Work

Qualquer erro dentro da transação deve causar rollback.

Fluxo:

```text
Exception
    ↓
Rollback
    ↓
Close Session
    ↓
Translate Error
```

Nenhum evento deve ser publicado após rollback.

---

# 39. Erros e Eventos

Falha de Handler deve:

- registrar evento;
- registrar handler;
- incrementar tentativas;
- aplicar retry quando elegível;
- mover para Dead Event quando necessário.

---

# 40. Retry Eligibility

Elegíveis:

- timeout;
- indisponibilidade temporária;
- lock transitório;
- falha de rede;
- erro 5xx externo.

Não elegíveis:

- regra de domínio;
- validação;
- permissão;
- token inválido;
- payload incompatível;
- conflito permanente.

---

# 41. Erros de Idempotência

Exemplos:

```text
DuplicateRequestError
DuplicateEventError
AlreadyProcessedError
```

Em alguns fluxos, duplicidade pode retornar sucesso idempotente em vez de erro.

Essa decisão pertence ao Use Case.

---

# 42. Erros de Concorrência

Exemplos:

```text
OptimisticLockError
ConcurrentModificationError
ResourceVersionConflictError
```

A interface pode orientar nova tentativa.

---

# 43. Erros de Configuração

Exemplos:

```text
MissingConfigurationError
InvalidConfigurationError
UnsupportedEnvironmentError
```

Configuração crítica inválida deve impedir startup.

---

# 44. Erros de Arquivo

Exemplos:

```text
FileNotFoundApplicationError
InvalidFileTypeError
FileTooLargeError
UnsafeFilePathError
ExportGenerationError
```

---

# 45. Erros de Backup

Exemplos:

```text
BackupCreationError
BackupIntegrityError
BackupRestoreError
BackupNotFoundError
```

Restore deve falhar de forma segura antes de substituir dados válidos.

---

# 46. Erros de Relatório

Exemplos:

```text
ReportGenerationError
UnsupportedReportFormatError
ReportExpiredError
ReportAccessDeniedError
```

---

# 47. Erros de Paginação

Exemplos:

```text
InvalidPageError
InvalidPageSizeError
InvalidSortFieldError
InvalidSortDirectionError
```

---

# 48. Erros de Datas

Exemplos:

```text
InvalidDateRangeError
FutureDateNotAllowedError
DateOutsideAllowedPeriodError
```

---

# 49. Erros de Authentication

Exemplos oficiais:

```text
EmailAlreadyRegisteredError
InvalidCredentialsError
AccountBlockedError
SessionExpiredError
SessionRevokedError
PasswordMismatchError
PasswordPolicyViolationError
PasswordResetTokenExpiredError
PasswordResetTokenAlreadyUsedError
```

---

# 50. Erros de Character

Exemplos:

```text
CharacterNotFoundError
CharacterAlreadyExistsError
InvalidCharacterLevelError
CharacterAttributeNotFoundError
CharacterStateConflictError
```

---

# 51. Erros de Workout

Exemplos:

```text
WorkoutNotFoundError
WorkoutTypeNotFoundError
InvalidWorkoutDurationError
InvalidPerceivedEffortError
WorkoutAccessDeniedError
```

---

# 52. Erros de Health

Exemplos:

```text
SleepRecordNotFoundError
InvalidSleepScoreError
InvalidHeartRateError
InvalidBodyCompositionError
HealthRecordAccessDeniedError
```

---

# 53. Erros de Reading

Exemplos:

```text
BookNotFoundError
ReadingSessionNotFoundError
InvalidPagesReadError
BookAlreadyFinishedError
ReadingAccessDeniedError
```

---

# 54. Erros de Therapy

Exemplos:

```text
TherapistNotFoundError
TherapySessionNotFoundError
InvalidClarityScoreError
TherapyAccessDeniedError
```

A mensagem não deve revelar existência de recurso de outro usuário.

---

# 55. Erros de Habits

Exemplos:

```text
HabitNotFoundError
HabitAlreadyCompletedError
InvalidHabitFrequencyError
InvalidHabitTargetError
HabitAccessDeniedError
```

---

# 56. Erros de Gamification

Exemplos:

```text
InvalidExperienceError
QuestNotFoundError
QuestAlreadyCompletedError
AchievementNotEligibleError
RewardAlreadyGrantedError
SkillNotUnlockedError
```

---

# 57. Erros de Analytics

Exemplos:

```text
InsufficientDataError
AnalyticsCalculationError
UnsupportedMetricError
AnalyticsPeriodInvalidError
```

---

# 58. Erros de AI Mentor

Exemplos:

```text
AIContextTooLargeError
AIProviderUnavailableError
AIResponseInvalidError
AIRecommendationGenerationError
AIConsentRequiredError
```

---

# 59. Erros de Administração

Exemplos:

```text
AdministrativePermissionRequiredError
ProtectedUserOperationError
SystemConfigurationConflictError
AuditLogAccessDeniedError
```

---

# 60. API Error Response

Modelo futuro:

```python
@dataclass(frozen=True)
class ApiErrorResponse:
    correlation_id: str
    code: str
    message: str
    field: str | None
```

Para múltiplos erros:

```python
@dataclass(frozen=True)
class ApiValidationErrorResponse:
    correlation_id: str
    errors: tuple[ErrorDetailDto, ...]
```

---

# 61. Status Semânticos

Mapeamento futuro sugerido:

```text
Validation → 400
Authentication → 401
Authorization → 403
Not Found → 404
Conflict → 409
Unprocessable Domain Rule → 422
Rate Limit → 429
Infrastructure Failure → 503
Unexpected Error → 500
```

A Presentation Streamlit deve usar a mesma semântica, mesmo sem HTTP.

---

# 62. Mensagens para Streamlit

Exemplo:

```python
if error.code == "auth.security.invalid_credentials":
    st.error("E-mail ou senha inválidos.")
```

Preferir Presenter ou catálogo de mensagens.

Evitar condicionais espalhadas pelas páginas.

---

# 63. Catálogo de Mensagens

Pode existir:

```text
src/lifeos/interfaces/streamlit/messages/error_messages.py
```

Mapeamento:

```python
ERROR_MESSAGES = {
    "auth.security.invalid_credentials":
        "E-mail ou senha inválidos.",
}
```

---

# 64. Internacionalização

Erros internos utilizam código.

A Presentation resolve mensagem por idioma.

Exemplo:

```text
code:
auth.security.invalid_credentials
```

Português:

```text
E-mail ou senha inválidos.
```

Inglês:

```text
Invalid email or password.
```

---

# 65. Testes Unitários

Todo erro deve ser testado quando possuir:

- contexto;
- código;
- metadata;
- tradução;
- regra de mapeamento;
- comportamento específico.

---

# 66. Testes de Tradução

Validar:

```text
Infrastructure Error
    ↓
Application Error
```

Exemplo:

```text
UniqueConstraintViolation
    ↓
EmailAlreadyRegisteredError
```

---

# 67. Testes de Presentation

Validar:

- mensagem correta;
- código correto;
- ausência de stack trace;
- ausência de dado sensível;
- correlation ID em erro inesperado.

---

# 68. Testes Multi-Tenant

Cenários:

```text
Acesso cross-tenant
    ↓
Mensagem segura
```

O teste deve garantir que não haja revelação de ownership.

---

# 69. Testes de Segurança

Validar:

- não enumeração de usuário;
- ausência de segredo;
- ausência de token;
- ausência de hash;
- ausência de payload privado;
- ausência de detalhe técnico.

---

# 70. Anti-patterns

São proibidos:

## Exceção genérica

```python
raise Exception("error")
```

## Mensagem técnica ao usuário

```text
sqlite3.IntegrityError
```

## Captura vazia

```python
except Exception:
    pass
```

## Catch-all silencioso

```python
except:
    return None
```

## Tradução incorreta

Converter toda falha em `ValidationError`.

## Stack trace na UI

## Dados sensíveis em mensagem

## Código instável

```text
ERROR_123
```

sem semântica.

## Erro criado na camada errada

Domain importando erro SQLAlchemy.

---

# 71. Como o Gemini deve Utilizar este Documento

Antes de criar ou tratar um erro, o agente deve responder:

1. Em qual camada ocorreu?
2. É erro de domínio, aplicação ou infraestrutura?
3. É esperado ou inesperado?
4. Qual código estável representa o erro?
5. Existe erro equivalente?
6. A mensagem externa é segura?
7. Há dados sensíveis?
8. É necessário correlation ID?
9. Deve gerar auditoria?
10. Deve causar rollback?
11. É elegível para retry?
12. Precisa ser traduzido?
13. Como será apresentado?
14. Existem testes?
15. A documentação foi atualizada?

---

# 72. Checklist de Implementação

- [ ] Categoria identificada.
- [ ] Camada correta.
- [ ] Código estável.
- [ ] Nome semântico.
- [ ] Mensagem interna segura.
- [ ] Mensagem externa definida.
- [ ] Tradução entre camadas implementada.
- [ ] Correlation ID avaliado.
- [ ] Logging seguro.
- [ ] Auditoria avaliada.
- [ ] Rollback avaliado.
- [ ] Retry avaliado.
- [ ] Multi-Tenant protegido.
- [ ] Testes unitários criados.
- [ ] Testes de tradução criados.
- [ ] Testes de segurança criados.
- [ ] Documentação atualizada.

---

# 73. Critérios de Aceite

Este documento será considerado atendido quando:

- erros estiverem classificados por camada;
- códigos forem estáveis;
- mensagens técnicas não chegarem ao usuário;
- erros de infraestrutura forem traduzidos;
- rollback ocorrer corretamente;
- retry for aplicado apenas quando apropriado;
- Multi-Tenant não for exposto;
- dados sensíveis forem protegidos;
- testes validarem tradução, segurança e apresentação;
- o tratamento permanecer consistente em todos os módulos.

---

# 74. Definition of Done

Um fluxo de erro só estará concluído quando:

- [ ] O erro estiver modelado.
- [ ] O código estiver definido.
- [ ] A camada estiver correta.
- [ ] A tradução estiver implementada.
- [ ] A mensagem externa estiver adequada.
- [ ] O log estiver seguro.
- [ ] O rollback estiver validado.
- [ ] A auditoria estiver avaliada.
- [ ] O retry estiver avaliado.
- [ ] Os testes passarem.
- [ ] A documentação estiver sincronizada.

---

# 75. Declaração Final

Erros fazem parte do contrato do LifeOS.

Eles devem ser tratados com a mesma disciplina aplicada aos fluxos de sucesso.

Cada erro deve possuir significado, camada, código, tradução, mensagem e estratégia de tratamento claros.

A arquitetura deve preservar segurança, rastreabilidade, testabilidade, isolamento Multi-Tenant e independência tecnológica mesmo quando uma operação falhar.
