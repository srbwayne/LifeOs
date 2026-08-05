# CONFIGURATION

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Configuração  
**Camadas Relacionadas:** Presentation, Application, Domain e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture

---

# 1. Objetivo

Este documento define o padrão oficial de **Configuração** do LifeOS.

Seu objetivo é estabelecer como toda configuração da plataforma deve ser organizada, carregada, validada e disponibilizada para os diferentes módulos da aplicação.

Este documento define:

- organização das configurações;
- carregamento de configurações;
- tipagem forte;
- validação;
- gerenciamento de ambientes;
- gerenciamento de secrets;
- Feature Flags;
- configurações por módulo;
- configurações por infraestrutura;
- ciclo de vida das configurações.

Toda configuração do sistema deverá seguir obrigatoriamente este documento.

---

# 2. Escopo

Este documento cobre:

- Configuration Management;
- Environment Variables;
- Settings Objects;
- Secrets;
- Config Providers;
- Feature Flags;
- Configuração por ambiente;
- Configuração de banco;
- Configuração de IA;
- Configuração de Storage;
- Configuração de autenticação;
- Configuração de segurança;
- Configuração de módulos;
- Configuração de Logging;
- Configuração de monitoramento;
- Configuração de Jobs;
- Configuração de integrações;
- Testes;
- Anti-patterns;
- Boas práticas.

Este documento complementa:

- `SECURITY.md`;
- `DATABASE.md`;
- `docs/04_BACKEND/TRANSACTIONS.md`;
- `SERVICES.md`;
- `USE_CASES.md`;
- `docs/02_ARCHITECTURE/08_EVENTS.md`;
- artefato futuro proposto: DEPENDENCY_INJECTION.md;
- artefato futuro proposto: OBSERVABILITY.md.

---

# 3. Filosofia de Configuração

Toda configuração do LifeOS deve seguir os seguintes princípios.

## Configuration as Code

A estrutura das configurações faz parte da arquitetura da aplicação.

Ela deve ser:

- versionável;
- tipada;
- documentada;
- testável.

---

## Single Source of Truth

Cada configuração deve possuir apenas uma origem oficial.

Exemplo:

```text
DATABASE_URL
```

Nunca deve existir:

```text
database_url

database.connection

db.url

connection_string
```

representando o mesmo conceito.

---

## Forte Tipagem

Configurações nunca devem ser manipuladas como strings espalhadas pelo sistema.

Sempre utilizar objetos tipados.

---

## Fail Fast

Configurações inválidas devem impedir a inicialização da aplicação.

Nunca iniciar parcialmente.

---

## Segurança

Secrets nunca fazem parte da configuração pública.

---

# 4. Configuration as Code

As configurações devem ser representadas por classes específicas.

Exemplo:

```python
DatabaseSettings

AuthenticationSettings

AISettings

StorageSettings

LoggingSettings
```

Nunca utilizar:

```python
config["database"]
```

espalhado pela aplicação.

A configuração deve possuir estrutura explícita.

---

# 5. Responsabilidades

Cada camada possui responsabilidades diferentes.

## Presentation

Consome configurações relacionadas à interface.

Exemplos:

- tema;
- idioma;
- paginação;
- layout.

---

## Application

Consome configurações relacionadas à lógica.

Exemplos:

- limites;
- Feature Flags;
- políticas;
- retries.

---

## Domain

O domínio deve permanecer independente de configuração.

Ele não deve conhecer:

- arquivos;
- variáveis de ambiente;
- providers;
- secrets.

---

## Infrastructure

Responsável por:

- carregar configuração;
- validar;
- fornecer objetos tipados;
- integração com providers externos.

---

# 6. Hierarquia de Configuração

A resolução das configurações deverá seguir uma ordem única.

Prioridade:

```text
Runtime Override

↓

Environment Variables

↓

Secrets

↓

Configuration File

↓

Default Values
```

Cada configuração deve possuir apenas um valor final.

Nunca combinar múltiplas fontes de forma imprevisível.

---

# 7. Ambientes

O LifeOS deverá suportar ambientes distintos.

Oficialmente:

```text
Development

Testing

Homologation

Production
```

Cada ambiente possui:

- banco;
- logging;
- Feature Flags;
- integrações;
- monitoramento;
- credenciais.

Nunca compartilhar configurações críticas entre ambientes.

---

# 8. Estrutura de Arquivos

Estrutura recomendada:

```text
config/

├── settings.py
├── environment.py
├── providers.py
├── validators.py
├── defaults.py
├── feature_flags.py
├── logging.py
├── security.py
└── ai.py
```

Separação por responsabilidade.

Nunca criar um único arquivo gigantesco de configuração.

---

# 9. Convenções

Toda configuração deve seguir convenções oficiais.

Classes:

```text
DatabaseSettings

AISettings

EmailSettings

StorageSettings

LoggingSettings

SecuritySettings
```

Providers:

```text
ConfigurationProvider

EnvironmentProvider

SecretProvider
```

Variáveis:

```text
DATABASE_URL

SMTP_HOST

OPENAI_API_KEY

SQLITE_PATH

APP_ENV
```

Evitar nomes genéricos:

```text
config

settings

value

option

parameter
```

---

# 10. Fluxo Oficial de Configuração

Toda configuração deverá seguir o seguinte fluxo:

```text
Application Startup

↓

Environment Provider

↓

Secret Provider

↓

Configuration Loader

↓

Validation

↓

Typed Settings

↓

Dependency Injection

↓

Application
```

Caso qualquer configuração obrigatória esteja ausente ou inválida:

```text
Startup

↓

Configuration Validation

↓

Failure

↓

Application Abort
```

A aplicação nunca deve iniciar com configurações inconsistentes, incompletas ou inseguras.

---

# 11. Environment Variables

As configurações do LifeOS devem ser obtidas prioritariamente através de **Environment Variables**.

Elas representam a principal forma de parametrizar a aplicação entre diferentes ambientes.

Exemplos:

```text
APP_ENV

DATABASE_URL

SQLITE_PATH

SMTP_HOST

SMTP_PORT

SMTP_USERNAME

SMTP_PASSWORD

OPENAI_API_KEY

GEMINI_API_KEY

LOG_LEVEL
```

As variáveis de ambiente nunca devem ser acessadas diretamente fora da camada de configuração.

Fluxo:

```text
Environment

↓

Configuration Provider

↓

Typed Settings
```

---

# 12. Secrets

Secrets representam informações altamente sensíveis.

Exemplos:

- senhas;
- API Keys;
- Encryption Keys;
- JWT Secret;
- SMTP Password;
- Tokens de integração;
- OAuth Client Secret.

Nunca armazenar Secrets:

- no código-fonte;
- em arquivos versionados;
- em documentação pública;
- em logs;
- em mensagens de erro.

Todo Secret deve ser obtido através do **Secret Provider**.

---

# 13. Configuration Providers

Toda configuração deve ser carregada por Providers específicos.

Exemplo:

```text
EnvironmentProvider

↓

SecretProvider

↓

ConfigurationProvider

↓

Settings
```

Responsabilidades:

- carregar configurações;
- resolver prioridades;
- validar valores;
- construir objetos tipados.

Nenhum módulo deve acessar diretamente variáveis de ambiente.

---

# 14. Settings Objects

As configurações devem ser agrupadas em objetos específicos.

Exemplos:

```python
DatabaseSettings

SecuritySettings

AuthenticationSettings

EmailSettings

AISettings

StorageSettings

LoggingSettings
```

Cada classe representa um único contexto.

Nunca criar uma classe contendo todas as configurações do sistema.

---

# 15. Typed Configuration

Todas as configurações devem possuir tipagem explícita.

Exemplo:

```python
@dataclass(frozen=True)
class DatabaseSettings:

    database_url: str

    pool_size: int

    timeout_seconds: int

    echo_sql: bool
```

Evitar:

```python
dict[str, str]
```

como estrutura principal.

A tipagem reduz erros e facilita manutenção.

---

# 16. Default Values

Algumas configurações podem possuir valores padrão.

Exemplo:

```python
page_size = 20

log_level = "INFO"

session_timeout_minutes = 60
```

Esses valores devem existir apenas na camada de configuração.

Nunca espalhar constantes pelo código.

Valores relacionados ao negócio pertencem ao Domain ou às Policies.

---

# 17. Validation

Toda configuração deve ser validada durante a inicialização.

Exemplos:

```text
DATABASE_URL obrigatória

SMTP_PORT > 0

LOG_LEVEL válido

APP_ENV conhecido

Session Timeout > 0
```

Caso qualquer validação falhe:

```text
Startup

↓

Validation Error

↓

Abort Initialization
```

Nunca iniciar parcialmente.

---

# 18. Fail Fast

O LifeOS adota o princípio **Fail Fast** para configurações.

Se uma configuração obrigatória estiver ausente:

```text
Missing DATABASE_URL
```

Resultado:

```text
Application Startup

↓

Failure

↓

Abort
```

Não utilizar valores fictícios para mascarar erros.

Problemas de configuração devem ser identificados imediatamente.

---

# 19. Configuration Loading

O carregamento das configurações ocorre apenas uma vez durante a inicialização.

Fluxo oficial:

```text
Application Startup

↓

Environment Provider

↓

Secret Provider

↓

Configuration Loader

↓

Validation

↓

Typed Settings

↓

Dependency Injection
```

Após esse processo, os módulos utilizam apenas objetos tipados.

Nenhuma camada deve continuar consultando variáveis de ambiente diretamente.

---

# 20. Configuration Lifecycle

O ciclo de vida das configurações segue o seguinte padrão:

```text
Read

↓

Validate

↓

Instantiate

↓

Inject

↓

Use

↓

Dispose (Application Shutdown)
```

As configurações são consideradas **imutáveis** durante a execução da aplicação.

Caso uma configuração precise ser alterada:

- atualizar a origem oficial;
- reinicializar a aplicação (quando necessário);
- reconstruir os objetos de configuração.

Essa abordagem garante previsibilidade, consistência e evita comportamentos inesperados causados por alterações dinâmicas de configuração.

---

# 21. Database Configuration

Toda configuração relacionada ao banco de dados deve estar centralizada em um único objeto.

Exemplo:

```python
@dataclass(frozen=True)
class DatabaseSettings:

    database_url: str

    echo_sql: bool

    connection_timeout: int

    pool_size: int

    max_overflow: int
```

A Application nunca deve conhecer:

- connection string;
- credenciais;
- parâmetros de conexão.

Essas informações pertencem exclusivamente à Infrastructure.

---

# 22. AI Configuration

Toda integração com Inteligência Artificial deve possuir configuração própria.

Exemplo:

```python
@dataclass(frozen=True)
class AISettings:

    provider: str

    model: str

    temperature: float

    max_tokens: int

    timeout_seconds: int
```

Outras configurações possíveis:

- contexto máximo;
- limite diário;
- Feature Flag;
- retry policy;
- custo máximo por requisição.

Nenhum módulo deve conhecer diretamente API Keys.

---

# 23. Email Configuration

Toda configuração relacionada ao envio de e-mails deve permanecer isolada.

Exemplo:

```python
@dataclass(frozen=True)
class EmailSettings:

    smtp_host: str

    smtp_port: int

    smtp_username: str

    smtp_password: str

    use_tls: bool
```

O restante da aplicação conhece apenas:

```text
EmailProvider
```

Nunca detalhes do SMTP.

---

# 24. Storage Configuration

Toda configuração de armazenamento deve utilizar abstração.

Exemplo:

```python
@dataclass(frozen=True)
class StorageSettings:

    provider: str

    bucket_name: str

    root_path: str

    max_upload_size_mb: int
```

Implementações futuras:

```text
Local Storage

Amazon S3

Azure Blob

Google Cloud Storage
```

A Application permanece independente do provedor.

---

# 25. Logging Configuration

Toda configuração de Logging deve estar centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class LoggingSettings:

    level: str

    json_logs: bool

    file_logging: bool

    console_logging: bool
```

Também podem existir:

- retenção;
- rotação;
- formatação;
- destino.

Nunca configurar Logging espalhado pelos módulos.

---

# 26. Security Configuration

As configurações de segurança devem permanecer agrupadas.

Exemplo:

```python
@dataclass(frozen=True)
class SecuritySettings:

    password_min_length: int

    session_timeout_minutes: int

    maximum_login_attempts: int

    enable_rate_limit: bool
```

Também podem existir:

- política de senha;
- tempo de expiração;
- algoritmo de hash;
- Feature Flags de segurança.

---

# 27. Authentication Configuration

As configurações de autenticação devem possuir objeto próprio.

Exemplo:

```python
@dataclass(frozen=True)
class AuthenticationSettings:

    remember_me_enabled: bool

    session_timeout_minutes: int

    password_reset_expiration_minutes: int

    maximum_sessions_per_user: int
```

Essas configurações não pertencem ao módulo de autorização.

---

# 28. Authorization Configuration

As configurações de autorização devem permanecer independentes.

Exemplo:

```python
@dataclass(frozen=True)
class AuthorizationSettings:

    enable_admin_panel: bool

    enable_audit_access: bool

    enable_cross_module_permissions: bool
```

Essas configurações apenas habilitam funcionalidades.

A decisão de autorização continua pertencendo ao:

```text
AuthorizationService
```

---

# 29. Feature Flags

As Feature Flags devem possuir estrutura própria.

Exemplo:

```python
@dataclass(frozen=True)
class FeatureFlags:

    ai_mentor_enabled: bool

    exports_enabled: bool

    therapy_enabled: bool

    analytics_enabled: bool

    achievements_enabled: bool
```

Regras:

- valores fortemente tipados;
- centralização;
- documentação;
- independência dos módulos.

Nunca espalhar:

```python
if FEATURE_X:
```

por todo o código.

---

# 30. Monitoring Configuration

Toda configuração de monitoramento deve permanecer centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class MonitoringSettings:

    metrics_enabled: bool

    tracing_enabled: bool

    audit_enabled: bool

    performance_monitoring: bool
```

Também podem existir:

- intervalo de coleta;
- exportadores;
- retenção;
- nível de detalhamento.

A configuração de monitoramento nunca deve depender diretamente da lógica de negócio, garantindo que a observabilidade possa evoluir independentemente dos módulos funcionais do LifeOS.

---

# 31. Streamlit Configuration

Toda configuração específica do Streamlit deve permanecer isolada da lógica de negócio.

Exemplo:

```python
@dataclass(frozen=True)
class StreamlitSettings:

    page_title: str

    page_icon: str

    layout: str

    sidebar_state: str

    show_debug_information: bool
```

Outras configurações possíveis:

- idioma padrão;
- tema;
- largura da página;
- cache;
- timeout da sessão.

O restante da aplicação nunca deve depender diretamente de componentes do Streamlit.

---

# 32. SQLAlchemy Configuration

Toda configuração do SQLAlchemy deve ser centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class SqlAlchemySettings:

    echo: bool

    future: bool

    pool_pre_ping: bool

    expire_on_commit: bool
```

Responsabilidades:

- criação da Engine;
- Session Factory;
- configuração do Pool;
- configuração de Logging SQL;
- configuração de Timeouts.

A Application nunca deve conhecer esses detalhes.

---

# 33. SQLite Configuration

A configuração específica do SQLite deve permanecer separada da configuração geral do banco.

Exemplo:

```python
@dataclass(frozen=True)
class SQLiteSettings:

    database_path: str

    busy_timeout_ms: int

    enable_wal: bool

    foreign_keys_enabled: bool
```

Configurações futuras:

- cache_size;
- synchronous;
- journal_mode;
- temp_store.

Essas opções pertencem exclusivamente à Infrastructure.

---

# 34. PostgreSQL Configuration

A futura migração para PostgreSQL deverá utilizar configuração própria.

Exemplo:

```python
@dataclass(frozen=True)
class PostgreSQLSettings:

    host: str

    port: int

    database: str

    username: str

    password: str

    ssl_enabled: bool
```

Também poderão existir:

- pool_size;
- max_connections;
- statement_timeout;
- lock_timeout;
- application_name.

Nenhum módulo deve depender dessas informações.

---

# 35. Background Jobs Configuration

Jobs assíncronos devem possuir configuração independente.

Exemplo:

```python
@dataclass(frozen=True)
class BackgroundJobSettings:

    enabled: bool

    worker_count: int

    retry_attempts: int

    retry_delay_seconds: int
```

Também podem existir:

- fila padrão;
- prioridade;
- timeout;
- limite de concorrência.

A configuração deve permanecer desacoplada do Job.

---

# 36. Cache Configuration

Toda configuração relacionada ao cache deve permanecer centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class CacheSettings:

    enabled: bool

    ttl_seconds: int

    maximum_entries: int

    provider: str
```

Implementações futuras:

```text
Memory Cache

Redis

Distributed Cache
```

A lógica da aplicação nunca deve conhecer detalhes do provedor.

---

# 37. Export Configuration

Exportações devem possuir configuração específica.

Exemplo:

```python
@dataclass(frozen=True)
class ExportSettings:

    export_directory: str

    maximum_file_size_mb: int

    default_format: str

    retention_days: int
```

Também podem existir:

- compressão;
- assinatura digital;
- criptografia;
- limite diário.

Cada formato (CSV, Excel, PDF) reutiliza essa configuração.

---

# 38. Upload Configuration

Uploads devem ser configuráveis.

Exemplo:

```python
@dataclass(frozen=True)
class UploadSettings:

    maximum_file_size_mb: int

    allowed_extensions: tuple[str, ...]

    temporary_directory: str

    virus_scan_enabled: bool
```

As validações continuam pertencendo à camada de Application.

A configuração apenas define limites.

---

# 39. Backup Configuration

Toda configuração de Backup deve permanecer agrupada.

Exemplo:

```python
@dataclass(frozen=True)
class BackupSettings:

    backup_directory: str

    compression_enabled: bool

    encryption_enabled: bool

    retention_days: int

    automatic_backup_enabled: bool
```

Também podem existir:

- horário;
- frequência;
- destino;
- política de retenção.

---

# 40. Restore Configuration

A operação de Restore também deve possuir configuração própria.

Exemplo:

```python
@dataclass(frozen=True)
class RestoreSettings:

    confirmation_required: bool

    verify_integrity: bool

    create_backup_before_restore: bool

    audit_enabled: bool
```

Fluxo oficial:

```text
Restore Request

↓

Restore Settings

↓

Validation

↓

Integrity Verification

↓

Authorization

↓

Execution

↓

Audit
```

Toda configuração de Restore deve priorizar segurança e rastreabilidade, garantindo que nenhuma restauração seja executada sem validação, autorização e registro adequado de auditoria.


Todas as configurações utilizadas pelo LifeOS devem ser fortemente tipadas, centralizadas, documentadas e injetadas através da camada de infraestrutura, preservando a independência do domínio e garantindo previsibilidade em todos os ambientes de execução.

---

# 41. Multi-Tenant Configuration

Toda configuração relacionada ao isolamento Multi-Tenant deve permanecer centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class MultiTenantSettings:

    enabled: bool

    enforce_ownership: bool

    strict_isolation: bool

    audit_cross_tenant_attempts: bool
```

Regras:

- isolamento habilitado por padrão;
- ownership obrigatório;
- auditoria de tentativas inválidas;
- validação em todos os módulos.

Nenhum módulo deve desabilitar essas configurações individualmente.

---

# 42. Module Configuration

Cada módulo pode possuir configurações próprias.

Exemplo:

```python
WorkoutSettings

HabitSettings

ReadingSettings

TherapySettings

AISettings

CharacterSettings
```

Cada módulo conhece apenas suas próprias configurações.

Nunca criar dependências entre configurações de módulos distintos.

---

# 43. Dependency Injection Configuration

Toda configuração da Injeção de Dependências deve permanecer concentrada na camada Infrastructure.

Exemplo:

```text
Application Startup

↓

Configuration Provider

↓

Container

↓

Service Registration

↓

Dependency Resolution
```

Os módulos nunca devem registrar dependências manualmente.

Toda configuração do container deve ser centralizada.

---

# 44. Plugin Configuration

A arquitetura deve permitir futuras extensões através de plugins.

Exemplo:

```python
@dataclass(frozen=True)
class PluginSettings:

    plugins_enabled: bool

    plugin_directory: str

    automatic_discovery: bool
```

No futuro poderão existir:

```text
AI Plugins

Visualization Plugins

Export Plugins

Notification Plugins
```

A configuração permanece independente da implementação.

---

# 45. External Providers Configuration

Integrações externas devem possuir configuração própria.

Exemplos:

```text
Gemini

OpenAI

SMTP

Storage

OAuth

Analytics
```

Modelo sugerido:

```python
ProviderSettings
```

Cada Provider deve conhecer apenas:

- endpoint;
- timeout;
- retries;
- autenticação;
- limites.

Nunca espalhar essas configurações pelos serviços.

---

# 46. API Configuration

A futura API REST deverá possuir configuração dedicada.

Exemplo:

```python
@dataclass(frozen=True)
class ApiSettings:

    enabled: bool

    host: str

    port: int

    cors_enabled: bool

    request_timeout_seconds: int
```

Também poderão existir:

- versionamento;
- compressão;
- paginação padrão;
- limite de payload.

---

# 47. Event Configuration

Toda configuração relacionada aos eventos deve permanecer centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class EventSettings:

    event_logging: bool

    publish_after_commit: bool

    retry_attempts: int

    dead_letter_enabled: bool
```

Essas configurações não pertencem aos Event Handlers.

Elas fazem parte da infraestrutura de eventos.

---

# 48. Scheduler Configuration

Processos agendados devem possuir configuração própria.

Exemplo:

```python
@dataclass(frozen=True)
class SchedulerSettings:

    enabled: bool

    timezone: str

    maximum_parallel_jobs: int

    retry_attempts: int
```

Também podem existir:

- intervalos;
- prioridades;
- horários;
- políticas de execução.

---

# 49. Retry Policies

As políticas de Retry devem permanecer configuráveis.

Exemplo:

```python
@dataclass(frozen=True)
class RetrySettings:

    maximum_attempts: int

    initial_delay_seconds: int

    exponential_backoff: bool

    maximum_delay_seconds: int
```

Aplicações possíveis:

- chamadas externas;
- IA;
- SMTP;
- Storage;
- APIs;
- banco de dados quando apropriado.

O Domain nunca implementa Retry.

---

# 50. Timeout Configuration

Todos os timeouts relevantes devem possuir configuração explícita.

Exemplo:

```python
@dataclass(frozen=True)
class TimeoutSettings:

    database_timeout_seconds: int

    ai_timeout_seconds: int

    smtp_timeout_seconds: int

    storage_timeout_seconds: int

    api_timeout_seconds: int
```

Princípios:

- nenhum timeout implícito;
- valores documentados;
- configuração centralizada;
- comportamento consistente entre ambientes.

Toda operação dependente de infraestrutura deve utilizar timeouts configuráveis, garantindo previsibilidade, resiliência e facilidade de manutenção ao longo da evolução do LifeOS.

---

# 51. Performance Configuration

As configurações relacionadas ao desempenho da aplicação devem permanecer centralizadas.

Exemplo:

```python
@dataclass(frozen=True)
class PerformanceSettings:

    lazy_loading_enabled: bool

    query_batch_size: int

    maximum_parallel_tasks: int

    preload_reference_data: bool
```

Essas configurações devem permitir otimizações sem alterar regras de negócio.

A camada de domínio nunca deve depender de parâmetros de performance.

---

# 52. Limits Configuration

Todo limite operacional deve ser configurável.

Exemplos:

- tamanho máximo de upload;
- quantidade máxima de registros exportados;
- número máximo de sessões;
- quantidade máxima de notificações;
- limite diário de chamadas para IA.

Exemplo:

```python
@dataclass(frozen=True)
class LimitsSettings:

    maximum_upload_size_mb: int

    maximum_export_rows: int

    maximum_active_sessions: int

    maximum_ai_requests_per_day: int
```

Nunca utilizar valores mágicos espalhados pelo código.

---

# 53. Quotas Configuration

Recursos sujeitos a consumo devem utilizar cotas configuráveis.

Exemplos:

```text
AI Requests

Storage

Exports

Uploads

Notifications
```

Exemplo:

```python
@dataclass(frozen=True)
class QuotaSettings:

    ai_requests_per_day: int

    storage_limit_mb: int

    exports_per_day: int
```

As cotas podem variar conforme o plano do usuário em versões futuras.

---

# 54. Rate Limiting Configuration

Toda limitação de requisições deve ser configurável.

Exemplo:

```python
@dataclass(frozen=True)
class RateLimitSettings:

    enabled: bool

    requests_per_minute: int

    burst_limit: int

    lockout_minutes: int
```

Aplicações:

- Login;
- Password Reset;
- IA;
- API;
- Upload;
- Exportação.

O algoritmo utilizado deve permanecer transparente para os módulos.

---

# 55. Observability Configuration

Toda configuração relacionada à observabilidade deve permanecer centralizada.

Exemplo:

```python
@dataclass(frozen=True)
class ObservabilitySettings:

    tracing_enabled: bool

    metrics_enabled: bool

    correlation_id_enabled: bool

    structured_logging: bool
```

Essas configurações controlam apenas a infraestrutura de observabilidade.

A lógica de negócio permanece independente.

---

# 56. Metrics Configuration

A coleta de métricas deve ser configurável.

Exemplo:

```python
@dataclass(frozen=True)
class MetricsSettings:

    enabled: bool

    export_interval_seconds: int

    retention_days: int
```

Métricas futuras:

- performance;
- autenticação;
- autorização;
- IA;
- banco;
- eventos;
- exportações.

---

# 57. Audit Configuration

Toda auditoria deve possuir configuração própria.

Exemplo:

```python
@dataclass(frozen=True)
class AuditSettings:

    enabled: bool

    retention_days: int

    record_login_events: bool

    record_admin_operations: bool
```

A configuração define quais eventos devem ser persistidos.

A implementação continua pertencendo ao módulo de auditoria.

---

# 58. Configuration Versioning

Toda configuração oficial deve possuir controle de versão.

Objetivos:

- rastreabilidade;
- compatibilidade;
- migração segura;
- rollback.

Exemplo:

```text
Configuration Schema

↓

Version 1

↓

Version 2

↓

Migration
```

Mudanças incompatíveis devem ser documentadas através de ADRs.

---

# 59. Configuration Migration

Sempre que uma configuração for alterada de forma incompatível, deve existir uma estratégia de migração.

Fluxo:

```text
Old Configuration

↓

Migration

↓

Validation

↓

New Configuration
```

Regras:

- nunca perder configurações válidas;
- validar antes da aplicação;
- registrar alterações relevantes.

---

# 60. Compatibility Policy

Toda evolução da configuração deve preservar compatibilidade sempre que possível.

Princípios:

- adicionar antes de remover;
- depreciar antes de eliminar;
- documentar mudanças;
- manter nomes consistentes;
- evitar mudanças desnecessárias.

Quando uma quebra de compatibilidade for inevitável, ela deverá:

- ser registrada em ADR;
- ser documentada no CHANGELOG;
- possuir plano de migração;
- ser validada por testes automatizados.

Essas diretrizes garantem que a evolução da configuração do LifeOS ocorra de forma previsível, segura e alinhada com a arquitetura oficial da plataforma.

---

# 61. Testes de Configuração

Toda configuração do LifeOS deve possuir testes automatizados.

Os testes devem validar:

- carregamento correto;
- tipagem;
- valores padrão;
- variáveis obrigatórias;
- validações;
- compatibilidade entre ambientes.

Exemplo:

```text
Environment

↓

Configuration Loader

↓

Validation

↓

Typed Settings
```

Os testes devem garantir que nenhuma configuração inválida seja aceita.

---

# 62. Testes de Configuração por Ambiente

Cada ambiente oficial deve possuir testes próprios.

Ambientes:

```text
Development

Testing

Homologation

Production
```

Os testes devem validar:

- carregamento correto;
- variáveis obrigatórias;
- Secrets;
- Feature Flags;
- Providers;
- integrações.

Nenhum ambiente deve iniciar utilizando configurações destinadas a outro ambiente.

---

# 63. Mock Configuration

Os testes automatizados devem utilizar configurações específicas.

Exemplo:

```python
TestSettings

FakeDatabaseSettings

FakeAISettings

FakeEmailSettings
```

Essas configurações permitem:

- isolamento;
- repetibilidade;
- previsibilidade;
- independência de infraestrutura.

Nunca utilizar configurações reais durante testes automatizados.

---

# 64. Anti-patterns

São proibidos.

## Leitura direta de Environment Variables

Errado:

```python
import os

database = os.getenv("DATABASE_URL")
```

Fora da camada de configuração.

---

## Configuração espalhada

```python
timeout = 30

...

timeout = 60
```

---

## Strings mágicas

```python
os.getenv("database")
```

---

## Secrets no código

```python
API_KEY = "abc123"
```

---

## Configuração mutável

```python
settings.timeout = 999
```

Durante a execução da aplicação.

---

## Configuração global compartilhada

```python
GLOBAL_CONFIG = {}
```

---

## Configuração duplicada

Mesmo parâmetro definido em múltiplos locais.

---

## Falta de validação

Inicializar a aplicação sem validar configurações obrigatórias.

Todos esses padrões violam a arquitetura oficial do LifeOS.

---

# 65. Configuration Security

As configurações fazem parte da superfície de segurança da aplicação.

Boas práticas:

- Secrets fora do código;
- Environment Variables protegidas;
- objetos imutáveis;
- validação obrigatória;
- criptografia quando necessário;
- auditoria de alterações.

Nunca registrar em logs:

- senhas;
- API Keys;
- tokens;
- secrets;
- chaves criptográficas.

---

# 66. ADRs Relacionadas

Toda alteração significativa na estratégia de configuração deverá gerar uma **Architecture Decision Record (ADR)**.

Exemplos:

- adoção de novo Configuration Provider;
- alteração da hierarquia de configuração;
- mudança da estratégia de Secrets;
- adoção de novo provedor de Storage;
- migração de banco;
- alteração de Feature Flags.

Cada decisão deve possuir:

- contexto;
- motivação;
- decisão;
- consequências;
- alternativas consideradas.

---

# 67. Convenções Oficiais

Toda configuração deve seguir uma nomenclatura consistente.

Classes:

```text
DatabaseSettings

AISettings

SecuritySettings

AuthenticationSettings

LoggingSettings

StorageSettings

FeatureFlags
```

Providers:

```text
ConfigurationProvider

EnvironmentProvider

SecretProvider
```

Arquivos:

```text
settings.py

providers.py

validators.py

defaults.py
```

Variáveis:

```text
DATABASE_URL

APP_ENV

SMTP_HOST

OPENAI_API_KEY
```

Evitar abreviações e nomes genéricos.

---

# 68. Checklist Oficial

Antes da implementação de uma nova configuração verificar:

- [ ] Configuração tipada.
- [ ] Classe específica criada.
- [ ] Validação implementada.
- [ ] Valor padrão definido quando aplicável.
- [ ] Secret separado da configuração pública.
- [ ] Environment Variable documentada.
- [ ] Dependency Injection atualizada.
- [ ] Testes criados.
- [ ] Documentação atualizada.
- [ ] ADR criada quando necessário.

Esse checklist deve ser seguido por todos os módulos do LifeOS.

---

# 69. Definition of Done

Uma configuração somente será considerada concluída quando:

- [ ] Estrutura criada.
- [ ] Tipagem definida.
- [ ] Validação implementada.
- [ ] Defaults definidos.
- [ ] Secrets protegidos.
- [ ] Providers atualizados.
- [ ] Dependency Injection atualizada.
- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados.
- [ ] Documentação sincronizada.

Nenhuma configuração deve ser considerada concluída sem atender a todos esses critérios.

---

# 70. Declaração Final

A estratégia de configuração do LifeOS foi projetada para ser:

- centralizada;
- fortemente tipada;
- segura;
- imutável;
- validável;
- testável;
- extensível;
- independente da tecnologia utilizada.

Toda configuração da plataforma deve possuir uma única origem oficial, ser carregada pela camada de infraestrutura, validada durante a inicialização da aplicação e disponibilizada aos módulos por meio de objetos tipados e injeção de dependências.

Esse padrão garante previsibilidade, segurança, facilidade de manutenção e evolução sustentável da arquitetura do LifeOS ao longo de todo o seu ciclo de vida.
