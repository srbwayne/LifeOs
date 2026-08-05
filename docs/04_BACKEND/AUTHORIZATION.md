# AUTHORIZATION

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Autorização  
**Camadas Relacionadas:** Domain, Application, Infrastructure e Presentation  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture

---

# 1. Objetivo

Este documento define o padrão oficial de **Autorização** do LifeOS.

Seu objetivo é estabelecer como o sistema determina se um usuário autenticado possui permissão para executar determinada ação sobre um recurso.

Este documento define:

- modelo oficial de autorização;
- responsabilidades de cada camada;
- ownership de recursos;
- isolamento Multi-Tenant;
- RBAC (Role-Based Access Control);
- permissões;
- políticas de acesso;
- autorização entre módulos;
- autorização por Use Case;
- autorização administrativa;
- auditoria;
- testes;
- boas práticas;
- anti-patterns.

Este documento **não trata de autenticação**.

Autenticação será definida em **SECURITY.md**.

---

# 2. Escopo

Este documento cobre:

- autorização;
- ownership;
- papéis (Roles);
- permissões;
- políticas;
- autorização baseada em recursos;
- autorização baseada em contexto;
- autorização Multi-Tenant;
- autorização administrativa;
- autorização entre módulos;
- autorização para APIs futuras;
- autorização para Streamlit;
- autorização para Jobs;
- autorização para IA;
- auditoria;
- testes;
- anti-patterns;
- critérios de aceite;
- Definition of Done.

Este documento complementa:

- `SECURITY.md`;
- `USE_CASES.md`;
- `VALIDATORS.md`;
- `SERVICES.md`;
- `REPOSITORIES.md`;
- `docs/04_BACKEND/UNIT_OF_WORK.md`;
- `ERRORS.md`;
- `DTOs.md`;
- `docs/02_ARCHITECTURE/03_DDD.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`.

---

# 3. Princípios Fundamentais

A autorização do LifeOS segue os seguintes princípios.

## Menor Privilégio

Todo usuário deve possuir apenas as permissões estritamente necessárias.

Nunca conceder acesso amplo por conveniência.

---

## Negação por Padrão

Toda operação é considerada proibida até que exista uma regra explícita permitindo sua execução.

Fluxo:

```text
Request

↓

Existe permissão?

↓

Não

↓

Acesso negado
```

---

## Ownership

O proprietário de um recurso possui direitos especiais sobre esse recurso.

Exemplo:

```text
Workout

↓

owner_user_id
```

Somente o proprietário pode:

- visualizar;
- alterar;
- excluir;
- exportar;
- compartilhar (quando suportado).

---

## Isolamento Multi-Tenant

Nenhum usuário pode acessar recursos pertencentes a outro usuário.

Essa é uma regra obrigatória da arquitetura.

---

## Defesa em Profundidade

A autorização não deve existir apenas na interface.

Ela deve ser aplicada em:

- Use Cases;
- Policies;
- Repositories;
- APIs futuras;
- Jobs;
- Eventos;
- Integrações.

---

# 4. Modelo Oficial

O LifeOS utiliza um modelo híbrido composto por:

- Ownership;
- RBAC;
- Policies;
- Contexto;
- Regras de Domínio.

Fluxo:

```text
Usuário autenticado

↓

Role

↓

Permissões

↓

Ownership

↓

Policy

↓

Use Case

↓

Recurso
```

Nenhuma dessas etapas substitui a outra.

Todas podem participar da decisão.

---

# 5. Ownership

Ownership é a principal regra de autorização do LifeOS.

Cada recurso persistido pertence exatamente a um usuário.

Exemplos:

```text
Workout

↓

user_id
```

```text
Book

↓

user_id
```

```text
Habit

↓

user_id
```

```text
Therapy Session

↓

user_id
```

---

Todo Repository deve preservar esse vínculo.

Nunca deve existir recurso órfão.

---

# 6. Roles (Papéis)

O sistema reconhece papéis funcionais.

Versão inicial:

```text
USER

ADMIN
```

Futuramente poderão existir:

```text
SUPPORT

MODERATOR

AUDITOR

SYSTEM
```

Papéis representam responsabilidades gerais.

Eles não substituem ownership.

---

# 7. Permissões

Permissões representam ações específicas.

Exemplos:

```text
user.read

user.update

user.delete

workout.create

workout.read

workout.update

workout.delete

habit.complete

book.create

therapy.read

therapy.update

admin.users.read

admin.audit.read
```

Cada permissão deve possuir significado único e estável.

---

# 8. Policies

Policies encapsulam regras de autorização mais complexas.

Exemplo:

```text
User pode editar treino?

↓

WorkoutPolicy

↓

True ou False
```

Outro exemplo:

```text
Pode excluir livro?

↓

BookPolicy

↓

True ou False
```

Policies pertencem à camada Application.

Elas não conhecem Streamlit nem SQLAlchemy.

---

# 9. Responsabilidades das Camadas

## Presentation

Responsável por:

- ocultar funcionalidades indisponíveis;
- desabilitar botões;
- apresentar mensagens de acesso negado.

Nunca deve ser a única camada de proteção.

---

## Application

Responsável por:

- executar autorização;
- chamar Policies;
- validar permissões;
- validar ownership;
- interromper execução quando necessário.

---

## Domain

Responsável apenas por regras de negócio.

O domínio não deve conhecer usuários autenticados nem papéis administrativos.

---

## Infrastructure

Responsável por:

- recuperar identidade autenticada;
- recuperar permissões;
- integrar provedores externos;
- aplicar filtros técnicos quando necessário.

---

# 10. Fluxo Oficial de Autorização

Toda operação protegida deverá seguir o fluxo abaixo.

```text
Usuário autenticado

↓

Receber Request

↓

Criar Command

↓

Use Case

↓

Authorization Service

↓

Policy

↓

Ownership

↓

Permissão concedida?

↓

SIM
    ↓
Executa regra de negócio

↓

Persistência

↓

Commit

↓

Resposta
```

Caso a autorização falhe:

```text
Usuário autenticado

↓

Use Case

↓

Authorization Service

↓

Permissão negada

↓

AuthorizationError

↓

Presenter

↓

Mensagem amigável ao usuário
```

Nenhuma alteração de estado deve ocorrer quando a autorização for negada.

A autorização deve sempre acontecer **antes** da execução das regras de negócio e antes da persistência de qualquer alteração.

---

# 11. Authorization Service

Toda decisão de autorização deve ser centralizada em um componente específico.

Nome oficial:

```text
AuthorizationService
```

Sua responsabilidade é determinar se um usuário autenticado pode executar determinada ação.

O Authorization Service pode utilizar:

- Policies;
- Roles;
- Permissões;
- Ownership;
- Contexto da operação;
- Feature Flags;
- Configurações.

Ele nunca deve:

- executar regras de negócio;
- persistir dados;
- acessar Streamlit;
- abrir transações.

---

Exemplo:

```python
class AuthorizationService(Protocol):

    def authorize(
        self,
        context: AuthorizationContext,
    ) -> None:
        ...
```

Caso a autorização falhe, uma exceção apropriada deve ser lançada.

---

# 12. Authorization Context

Toda autorização deve ser baseada em um contexto explícito.

Exemplo:

```python
@dataclass(frozen=True)
class AuthorizationContext:

    current_user: CurrentUser

    action: str

    resource_type: str

    resource_owner_id: str | None

    metadata: Mapping[str, object] | None = None
```

O contexto concentra todas as informações necessárias para tomada de decisão.

Isso evita parâmetros espalhados pela aplicação.

---

# 13. Resource Authorization

A autorização deve ocorrer sobre um recurso específico.

Exemplos:

```text
Workout

Book

Habit

Character

Quest

Achievement

Therapy Session

Report

Dashboard
```

Cada recurso deve possuir regras próprias.

Fluxo:

```text
Current User

↓

Resource

↓

Authorization Service

↓

Allowed?
```

---

# 14. Ownership Validation

Ownership é a principal forma de autorização do LifeOS.

Fluxo:

```text
Current User

↓

Resource.user_id

↓

Equals?

↓

Yes

↓

Access Granted
```

Caso contrário:

```text
Access Denied
```

---

Exemplo:

```python
if workout.user_id != current_user.id:
    raise ResourceOwnershipError()
```

Essa validação deve ocorrer antes da execução das regras de domínio.

---

# 15. Authorization Policies

Policies encapsulam regras complexas.

Exemplos:

```text
WorkoutPolicy

CharacterPolicy

BookPolicy

HabitPolicy

TherapyPolicy

ReportPolicy
```

Cada Policy responde apenas perguntas de autorização.

Exemplo:

```python
class WorkoutPolicy:

    def can_update(
        self,
        user: CurrentUser,
        workout: Workout,
    ) -> bool:
        ...
```

Policies nunca executam persistência.

---

# 16. Policy Composition

Policies podem ser compostas.

Exemplo:

```text
WorkoutPolicy

↓

OwnershipPolicy

↓

RolePolicy

↓

PermissionPolicy

↓

Result
```

Cada Policy continua pequena e especializada.

Evitar grandes classes contendo centenas de regras.

---

# 17. Role-Based Authorization (RBAC)

Além do ownership, o sistema utiliza papéis.

Versão inicial:

```text
USER

ADMIN
```

Fluxo:

```text
Current User

↓

Role

↓

Permission

↓

Action
```

Roles representam permissões gerais.

Não substituem ownership.

---

# 18. Permission-Based Authorization

Permissões representam ações específicas.

Exemplos:

```text
workout.create

workout.read

workout.update

workout.delete

book.create

book.update

therapy.read

admin.audit.read
```

A verificação deve ocorrer através do Authorization Service.

Exemplo:

```python
authorization_service.require(
    "workout.update"
)
```

---

# 19. Role × Permission

Roles agrupam permissões.

Exemplo:

```text
ADMIN

↓

workout.read

workout.update

user.read

user.update

audit.read
```

Enquanto:

```text
USER
```

possui apenas permissões relacionadas aos próprios recursos.

Sempre que possível, o sistema deve validar permissões e não comparar Roles diretamente.

Isso facilita futuras expansões.

---

# 20. Regra Oficial de Decisão

Toda autorização deve seguir a seguinte ordem lógica:

```text
Usuário autenticado?

↓

Recurso existe?

↓

Ownership válido?

↓

Role permite?

↓

Permissão permite?

↓

Policy permite?

↓

Ação autorizada
```

Caso qualquer etapa falhe:

```text
AuthorizationError
```

Nenhuma regra de negócio deve ser executada antes da conclusão desse fluxo.

Essa sequência torna o processo de autorização previsível, auditável e consistente em todos os módulos do LifeOS.

---

# 21. Context-Based Authorization

Nem toda autorização pode ser resolvida apenas por Roles ou Ownership.

Algumas decisões dependem do contexto atual da operação.

Exemplos:

- horário;
- Feature Flags;
- assinatura do usuário;
- estado do recurso;
- ambiente (desenvolvimento, homologação, produção);
- configuração da organização;
- status do usuário.

Exemplo:

```text
Usuário é proprietário

↓

Recurso está arquivado

↓

Pode editar?

↓

Não
```

Nesse caso, o Ownership continua válido, mas o contexto impede a operação.

---

# 22. Attribute-Based Authorization (ABAC)

O LifeOS também suporta autorização baseada em atributos (ABAC).

Os atributos podem pertencer ao:

- usuário;
- recurso;
- ambiente;
- operação.

Exemplo:

```text
User.plan = PREMIUM

↓

AI Mentor

↓

Permitido
```

Outro exemplo:

```text
Workout.status = LOCKED

↓

Update

↓

Negado
```

ABAC complementa RBAC.

Nunca substitui Ownership.

---

# 23. Multi-Tenant Authorization

O isolamento Multi-Tenant é obrigatório.

Todo recurso deve pertencer exatamente a um usuário.

Fluxo:

```text
Current User

↓

Repository

↓

user_id

↓

Filtro obrigatório

↓

Resultado
```

A autorização deve ocorrer em dois níveis:

- lógico (Authorization Service);
- persistência (Repository).

Assim, mesmo uma falha em uma camada não compromete o isolamento.

---

# 24. Authorization entre Módulos

Um módulo nunca deve acessar diretamente regras internas de autorização de outro módulo.

Fluxo correto:

```text
Module A

↓

Public Facade

↓

Authorization Service

↓

Module B
```

Nunca:

```text
Module A

↓

Module B Repository

↓

Bypass Authorization
```

Toda comunicação entre módulos deve respeitar contratos públicos.

---

# 25. Authorization por Use Case

Cada Use Case de escrita deve definir explicitamente quais permissões exige.

Exemplo:

```text
RegisterWorkoutUseCase

↓

workout.create
```

Outro exemplo:

```text
DeleteWorkoutUseCase

↓

workout.delete
```

A autorização deve ocorrer antes da execução da lógica do caso de uso.

---

# 26. Authorization por Resource

Cada Aggregate possui sua própria política.

Exemplo:

```text
Workout

↓

WorkoutPolicy
```

```text
Book

↓

BookPolicy
```

```text
Character

↓

CharacterPolicy
```

Essa separação evita classes gigantes de autorização.

Cada recurso conhece apenas suas próprias regras.

---

# 27. Authorization por Operação

As operações padrão são:

```text
CREATE

READ

UPDATE

DELETE

EXPORT

IMPORT

RESTORE

SHARE

ARCHIVE
```

Cada uma pode possuir regras diferentes.

Exemplo:

```text
Workout

READ → proprietário

UPDATE → proprietário

DELETE → proprietário

EXPORT → proprietário
```

---

# 28. Authorization para Recursos Compartilhados

No futuro poderão existir recursos compartilhados.

Exemplo:

```text
Projeto

↓

Usuário A

Usuário B

Usuário C
```

Nesse cenário, a autorização deixa de depender apenas de ownership.

Será baseada em:

- papel dentro do recurso;
- permissões específicas;
- políticas.

A implementação deve permanecer compatível com esse cenário futuro.

---

# 29. Authorization para Recursos Administrativos

Recursos administrativos exigem permissão explícita.

Exemplos:

```text
Audit Logs

System Metrics

Configuration

User Administration

Feature Flags

Backup

Restore
```

Ownership não é suficiente.

Esses recursos exigem:

```text
ADMIN

+

Permissão específica
```

Exemplo:

```text
admin.audit.read
```

---

# 30. Ordem Oficial da Autorização

Toda operação protegida deverá seguir exatamente esta sequência:

```text
Usuário autenticado

↓

Resolver Current User

↓

Carregar Resource

↓

Validar Multi-Tenant

↓

Validar Ownership

↓

Validar Role

↓

Validar Permissão

↓

Executar Policies

↓

Validar Contexto

↓

Autorizado?

↓

SIM

↓

Executar Use Case

↓

Persistir

↓

Commit
```

Caso qualquer etapa falhe:

```text
AuthorizationError

↓

Rollback (se necessário)

↓

Presenter

↓

Mensagem amigável
```

Essa ordem é obrigatória para todos os módulos do LifeOS e garante uma autorização consistente, previsível, segura e alinhada à arquitetura oficial do projeto.

---

# 31. Authorization em Command Use Cases

Todo **Command Use Case** deve validar autorização antes de executar qualquer alteração de estado.

Fluxo oficial:

```text
Request
    ↓
Command
    ↓
Use Case
    ↓
Authorization Service
    ↓
Autorizado?
    ↓
SIM
    ↓
Executa regra de negócio
    ↓
Persistência
```

Nunca alterar estado antes da autorização.

---

Exemplo:

```python
class RegisterWorkoutUseCase:

    def execute(
        self,
        command: RegisterWorkoutCommand,
    ) -> RegisterWorkoutResult:

        self._authorization_service.require(
            permission="workout.create",
            current_user=self._current_user,
        )

        ...
```

---

# 32. Authorization em Query Use Cases

Consultas também exigem autorização.

Nem toda informação pode ser visualizada por qualquer usuário.

Exemplo:

```text
GetWorkoutHistoryQuery

↓

Authorization

↓

Repository
```

Mesmo operações de leitura devem validar:

- ownership;
- permissões;
- contexto.

---

# 33. Authorization em Repositories

Repositories nunca substituem o Authorization Service.

Porém, devem reforçar o isolamento Multi-Tenant.

Exemplo:

```python
SELECT *

FROM workout

WHERE id = :id

AND user_id = :current_user
```

Assim, mesmo que uma autorização seja esquecida, o Repository continua impedindo acesso indevido.

---

# 34. Authorization em Domain Services

Domain Services não executam autorização.

Eles assumem que o chamador já validou o acesso.

Errado:

```python
class ExperienceService:

    def grant(...):

        if current_user.role != "ADMIN":
            ...
```

Correto:

```text
Use Case

↓

Authorization

↓

ExperienceService
```

O Domain permanece independente de usuários autenticados.

---

# 35. Authorization em Application Services

Application Services podem reutilizar Authorization Service.

Exemplo:

```text
Use Case

↓

Application Service

↓

Authorization Service

↓

Operation
```

Quando um Service representa uma operação reutilizável, ele pode proteger seu próprio contrato.

---

# 36. Authorization em Background Jobs

Jobs executam sem interface.

Mesmo assim, autorização continua existindo.

Exemplo:

```text
Job

↓

Load User

↓

Authorization Context

↓

Operation
```

Jobs nunca devem assumir privilégios administrativos automaticamente.

Sempre utilizar um contexto explícito.

---

# 37. Authorization em Event Handlers

Handlers devem validar autorização quando modificarem recursos protegidos.

Fluxo:

```text
Event

↓

Handler

↓

Authorization

↓

Persistência
```

Caso o evento já tenha sido produzido por um fluxo autorizado, essa validação pode ser simplificada.

Mesmo assim, ownership deve permanecer preservado.

---

# 38. Authorization para AI

Toda chamada envolvendo IA deve respeitar autorização.

Exemplos:

```text
Mentor AI

↓

Somente dados do usuário atual
```

Nunca enviar para IA:

- dados de outro usuário;
- notas privadas não autorizadas;
- informações administrativas;
- registros internos.

A autorização deve ocorrer antes da montagem do contexto enviado ao Provider.

---

# 39. Authorization para Exportações

Exportações seguem exatamente as mesmas regras dos recursos originais.

Exemplo:

```text
Workout Export

↓

Ownership

↓

Export permitido
```

O fato de ser uma exportação não concede acesso adicional.

O usuário só pode exportar recursos que já poderia visualizar.

---

# 40. Authorization para Importações

Importações também exigem autorização.

Fluxo:

```text
Upload

↓

Authorization

↓

Validation

↓

Import

↓

Persistência
```

Antes de importar:

- validar permissão;
- validar ownership do destino;
- validar limites do usuário;
- validar Feature Flags quando aplicável.

Nenhuma importação deve criar ou alterar recursos fora do escopo autorizado do usuário autenticado.

---

# 41. Authorization para Administração

Operações administrativas exigem um nível adicional de autorização.

Ownership não é suficiente.

Exemplos:

```text
Gerenciar usuários

Gerenciar Feature Flags

Consultar Auditoria

Executar Backup

Executar Restore

Alterar Configurações Globais

Gerenciar Roles

Gerenciar Permissões
```

Todas essas operações exigem:

```text
Role ADMIN

+

Permissão específica
```

Exemplo:

```text
admin.users.manage
```

---

# 42. Privilégios Administrativos

Mesmo administradores devem obedecer ao princípio do menor privilégio.

Exemplo:

```text
ADMIN

↓

Pode acessar Auditoria

↓

Não necessariamente pode alterar configurações críticas
```

As permissões administrativas devem ser independentes.

Exemplo:

```text
admin.audit.read

admin.configuration.update

admin.backup.execute

admin.restore.execute

admin.users.manage
```

Nunca utilizar apenas:

```text
role == ADMIN
```

como regra única.

---

# 43. Feature Flags

Feature Flags também participam da autorização.

Exemplo:

```text
AI Mentor

↓

Feature habilitada?

↓

Não

↓

Acesso negado
```

Outro exemplo:

```text
Exportação PDF

↓

Feature habilitada

↓

Permissão

↓

Executa
```

Feature Flags não substituem autorização.

São uma camada adicional.

---

# 44. Authorization para APIs Futuras

A futura API REST deverá utilizar exatamente o mesmo mecanismo de autorização.

Fluxo:

```text
HTTP Request

↓

Authentication

↓

Authorization Service

↓

Use Case

↓

Response
```

Nunca implementar autorização duplicada apenas para a API.

A mesma regra deve servir para:

- Streamlit;
- API;
- CLI;
- Background Jobs.

---

# 45. Authorization para Streamlit

A interface Streamlit deve apenas refletir o resultado da autorização.

Pode:

- ocultar menus;
- ocultar páginas;
- desabilitar botões;
- ocultar ações.

Nunca confiar apenas nisso.

Exemplo:

```python
if permissions.can_create_workout:
    st.button(...)
```

Mesmo ocultando o botão, o Use Case continua obrigado a validar autorização.

---

# 46. Authorization para Dashboards

Dashboards podem combinar informações de diversos módulos.

A autorização deve ser aplicada em cada fonte de dados.

Fluxo:

```text
Dashboard

↓

Workout

↓

Health

↓

Reading

↓

Habits

↓

Therapy
```

Cada consulta deve respeitar:

- ownership;
- tenant;
- permissões.

Nunca montar Dashboard utilizando dados de outro usuário.

---

# 47. Authorization para Relatórios

Relatórios seguem exatamente a autorização do recurso original.

Exemplo:

```text
Workout Report

↓

Workout Authorization

↓

Generate Report
```

O relatório nunca pode conter:

- registros não autorizados;
- informações administrativas;
- dados de terceiros.

---

# 48. Authorization para Auditoria

Auditoria é um recurso altamente sensível.

Exemplo:

```text
Audit Logs

↓

ADMIN

+

admin.audit.read
```

Além disso:

- acessos devem ser registrados;
- filtros devem respeitar tenant;
- exportações devem ser auditadas.

---

# 49. Authorization para Configurações

Configurações são divididas em categorias.

Exemplos:

```text
User Settings

↓

Ownership
```

```text
System Settings

↓

ADMIN
```

```text
Game Settings

↓

Permissão específica
```

Nem toda configuração pertence ao administrador.

Configurações pessoais continuam pertencendo ao usuário.

---

# 50. Fluxo Oficial para Operações Administrativas

Toda operação administrativa deverá seguir o seguinte fluxo:

```text
Usuário autenticado

↓

Role

↓

Permissão administrativa

↓

Feature Flag (quando existir)

↓

Policy

↓

Authorization Service

↓

Executa operação

↓

Auditoria

↓

Resposta
```

Toda operação administrativa deve gerar registro de auditoria contendo, no mínimo:

- usuário responsável;
- operação executada;
- data e hora;
- recurso afetado;
- resultado da operação;
- correlation ID.

Operações administrativas nunca devem ignorar as regras gerais de autorização definidas neste documento.

# 51. Authorization para Segurança

A autorização complementa a autenticação.

Enquanto a autenticação responde:

```text
Quem é o usuário?
```

A autorização responde:

```text
O que esse usuário pode fazer?
```

Toda operação protegida deve ocorrer na seguinte ordem:

```text
Authenticate

↓

Authorize

↓

Execute
```

Nunca inverter essa sequência.

---

# 52. Authorization e Sessões

A autorização sempre deve utilizar a sessão autenticada atual.

Exemplo:

```text
Session

↓

Current User

↓

Authorization Context

↓

Use Case
```

Jamais confiar em:

- user_id enviado pelo cliente;
- parâmetros ocultos;
- cookies manipuláveis;
- dados provenientes da interface.

O usuário autenticado deve ser resolvido pela infraestrutura.

---

# 53. Authorization e Cache

Permissões podem ser armazenadas em cache quando necessário.

Entretanto:

- mudanças de permissões devem invalidar o cache;
- mudanças de Role devem invalidar o cache;
- revogação de acesso deve produzir efeito imediato.

Fluxo:

```text
Permission Changed

↓

Invalidate Cache

↓

Next Authorization

↓

Reload Permissions
```

Nunca utilizar cache permanente para autorização.

---

# 54. Authorization e Performance

O sistema deve minimizar consultas repetidas de autorização.

Boas práticas:

- cache controlado;
- carregamento único do usuário;
- carregamento único das permissões;
- Policies pequenas;
- verificações determinísticas.

Evitar:

```text
100 consultas

↓

100 verificações iguais
```

A autorização deve permanecer rápida sem comprometer segurança.

---

# 55. Authorization em Repositories

Repositories reforçam isolamento.

Exemplo:

```sql
SELECT *

FROM workouts

WHERE id = :id

AND user_id = :current_user
```

Mesmo que uma autorização seja esquecida na Application, o Repository continua protegendo os dados.

Essa proteção é considerada uma segunda camada de defesa.

---

# 56. Authorization e Queries

Toda Query protegida deve validar acesso antes da leitura.

Fluxo:

```text
Query

↓

Authorization

↓

Repository

↓

Read Model
```

Consultas nunca devem retornar dados para posterior filtragem por autorização.

Correto:

```text
Autoriza

↓

Consulta
```

Errado:

```text
Consulta tudo

↓

Filtra depois
```

---

# 57. Authorization e Erros

Falhas de autorização devem produzir erros específicos.

Exemplos:

```text
PermissionDeniedError

OwnershipViolationError

TenantAccessDeniedError

AuthorizationError
```

Nunca lançar:

```python
Exception()
```

ou

```python
RuntimeError()
```

para representar autorização.

Esses erros devem seguir o padrão definido em `ERRORS.md`.

---

# 58. Authorization e Logging

Toda falha relevante de autorização deve ser registrada.

Registrar:

- usuário;
- recurso;
- ação;
- data;
- correlation ID;
- motivo da negação.

Nunca registrar:

- senha;
- token;
- segredo;
- payload completo;
- dados terapêuticos;
- informações médicas.

O log deve permitir auditoria sem expor informações sensíveis.

---

# 59. Authorization e Auditoria

Algumas operações exigem auditoria obrigatória.

Exemplos:

```text
Acesso administrativo

Mudança de Role

Mudança de Permissão

Tentativa de acesso negado

Alteração de Configuração

Execução de Backup

Execução de Restore
```

Cada registro deve conter, no mínimo:

- usuário;
- ação;
- recurso;
- resultado;
- timestamp;
- correlation ID.

---

# 60. Princípios Arquiteturais

Toda implementação de autorização do LifeOS deve obedecer aos seguintes princípios:

- autorização centralizada;
- Ownership obrigatório;
- isolamento Multi-Tenant;
- menor privilégio;
- negação por padrão;
- responsabilidade única;
- independência tecnológica;
- autorização antes da regra de negócio;
- autorização antes da persistência;
- autorização testável;
- autorização auditável;
- autorização desacoplada da interface.

Esses princípios são obrigatórios para todos os módulos do LifeOS e devem permanecer válidos independentemente da tecnologia utilizada pela aplicação.

---

# 61. Testes Unitários

Toda regra de autorização deve possuir testes unitários.

Os testes devem validar:

- permissões concedidas;
- permissões negadas;
- ownership;
- Roles;
- Policies;
- contexto;
- Feature Flags;
- Multi-Tenant.

---

Exemplo:

```text
Dado

Usuário proprietário

Quando

Atualiza Workout

Então

Permissão concedida
```

Outro exemplo:

```text
Dado

Usuário diferente

Quando

Atualiza Workout

Então

OwnershipViolationError
```

A autorização deve ser testada independentemente da interface.

---

# 62. Testes de Integração

Os testes de integração devem validar o fluxo completo.

Exemplo:

```text
Request

↓

Authentication

↓

Authorization

↓

Use Case

↓

Repository

↓

Database
```

Os cenários devem incluir:

- sucesso;
- acesso negado;
- recurso inexistente;
- recurso pertencente a outro usuário;
- administrador;
- usuário comum.

---

# 63. Testes Multi-Tenant

O isolamento entre usuários é obrigatório.

Os testes devem garantir que:

- usuário A nunca visualize dados de B;
- usuário A nunca altere dados de B;
- usuário A nunca exclua dados de B;
- exportações respeitem ownership;
- relatórios respeitem ownership;
- IA utilize apenas dados do usuário autenticado.

Exemplo:

```text
User A

↓

Workout B

↓

Access Denied
```

---

# 64. Testes de Segurança

Devem validar:

- ausência de bypass;
- ausência de escalonamento de privilégio;
- validação correta de permissões;
- proteção administrativa;
- proteção Multi-Tenant;
- proteção de recursos compartilhados.

Também devem validar ataques comuns:

```text
Troca de user_id

Troca de resource_id

Enumeração de IDs

Manipulação de parâmetros

Escalonamento de Role
```

Todos devem resultar em acesso negado.

---

# 65. Observabilidade

Toda autorização relevante deve ser observável.

Registrar:

- início;
- resultado;
- duração;
- Policy utilizada;
- Permission utilizada;
- Resource;
- Correlation ID.

Não registrar:

- senha;
- tokens;
- prompts;
- notas terapêuticas;
- dados médicos.

A observabilidade deve auxiliar diagnóstico sem comprometer privacidade.

---

# 66. Métricas

O sistema poderá registrar métricas futuras.

Exemplos:

```text
authorization_total

authorization_denied

authorization_allowed

authorization_latency

policy_execution_time

ownership_checks

permission_checks

admin_operations
```

Essas métricas auxiliam:

- performance;
- auditoria;
- segurança;
- capacidade.

---

# 67. Anti-patterns

São proibidos.

## Autorização apenas na Interface

```text
Ocultar botão

↓

Sem validação no Use Case
```

---

## Verificar apenas Role

```python
if role == "ADMIN":
```

sem validar permissões.

---

## Ignorar Ownership

Permitir alteração apenas porque o usuário possui Role.

---

## Repository sem filtro de usuário

```sql
SELECT *

FROM workout

WHERE id = ?
```

---

## Permitir acesso por ID informado pelo cliente

```python
user_id=request.user_id
```

---

## Hardcode de Permissões

```python
if permission == "123":
```

---

## Policies gigantes

Uma única classe contendo centenas de regras.

---

## Duplicação de Regras

Mesmo código repetido em vários Use Cases.

---

Todos esses padrões violam a arquitetura oficial.

---

# 68. Como o Gemini deve Utilizar este Documento

Antes de implementar qualquer autorização, o agente deve responder:

1. Quem é o usuário autenticado?
2. Qual recurso será acessado?
3. O recurso possui proprietário?
4. Ownership foi validado?
5. Existe Role necessária?
6. Existe permissão necessária?
7. Existe Policy específica?
8. Existe Feature Flag?
9. Existe regra Multi-Tenant?
10. O Repository filtra corretamente?
11. Existe auditoria?
12. Existem testes?
13. Há risco de escalonamento?
14. Existe documentação correspondente?
15. A autorização ocorre antes da regra de negócio?

Somente após responder essas perguntas o código poderá ser implementado.

---

# 69. Checklist de Implementação

- [ ] Usuário autenticado identificado.
- [ ] Authorization Service utilizado.
- [ ] Ownership validado.
- [ ] Role validada.
- [ ] Permissão validada.
- [ ] Policy implementada.
- [ ] Multi-Tenant protegido.
- [ ] Repository filtrando por usuário.
- [ ] Nenhum bypass possível.
- [ ] Auditoria avaliada.
- [ ] Logging seguro.
- [ ] Feature Flags avaliadas.
- [ ] Testes unitários criados.
- [ ] Testes de integração criados.
- [ ] Testes Multi-Tenant criados.
- [ ] Testes de segurança criados.
- [ ] Documentação atualizada.

---

# 70. Critérios de Aceite, Definition of Done e Declaração Final

## Critérios de Aceite

Este documento será considerado atendido quando:

- toda operação protegida utilizar Authorization Service;
- ownership for obrigatório para recursos do usuário;
- RBAC estiver implementado por permissões;
- Policies encapsularem regras complexas;
- isolamento Multi-Tenant for garantido;
- administradores utilizarem permissões específicas;
- nenhuma regra depender apenas da interface;
- auditoria estiver prevista para operações críticas;
- testes cobrirem cenários positivos e negativos;
- a arquitetura permanecer independente da tecnologia utilizada.

---

## Definition of Done

Uma funcionalidade protegida por autorização somente será considerada concluída quando:

- [ ] A autenticação estiver resolvida.
- [ ] A autorização ocorrer antes do Use Case.
- [ ] Ownership estiver validado.
- [ ] Permissões estiverem verificadas.
- [ ] Policies estiverem implementadas.
- [ ] Repositories reforçarem o isolamento.
- [ ] Multi-Tenant estiver preservado.
- [ ] Auditoria estiver implementada quando necessária.
- [ ] Logs estiverem seguros.
- [ ] Testes passarem.
- [ ] Documentação estiver sincronizada.

---

## Declaração Final

A autorização do LifeOS é baseada em uma arquitetura híbrida composta por **Ownership**, **RBAC**, **Policies** e **isolamento Multi-Tenant**.

Nenhuma camada isoladamente é responsável pela segurança da aplicação.

A proteção dos recursos deve ser construída em profundidade, garantindo que todas as operações sejam autorizadas de forma consistente, auditável, testável e independente da tecnologia utilizada.

Toda decisão de autorização deve ocorrer antes da execução das regras de negócio, preservando a integridade dos dados, a privacidade dos usuários e a evolução sustentável da arquitetura do LifeOS.

---

# 71. Roadmap Evolutivo

A arquitetura de autorização do LifeOS foi projetada para suportar crescimento contínuo sem necessidade de reescrita das regras existentes.

Evoluções previstas:

- RBAC completo;
- ABAC (Attribute-Based Access Control);
- PAP/PDP (Policy Administration Point / Policy Decision Point);
- políticas configuráveis;
- autorização baseada em organização;
- compartilhamento de recursos;
- grupos de usuários;
- equipes;
- permissões delegadas;
- permissões temporárias;
- auditoria avançada;
- consentimento granular;
- integração com OAuth/OpenID Connect;
- autorização para plugins;
- autorização para Marketplace.

Todas essas evoluções deverão manter compatibilidade com este documento.

---

# 72. Integração com Clean Architecture

A autorização deve respeitar integralmente as dependências da Clean Architecture.

Fluxo oficial:

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

A autorização ocorre na **Application Layer**.

O Domain:

- não conhece usuário autenticado;
- não conhece sessão;
- não conhece permissões;
- não conhece Roles.

A Infrastructure apenas fornece informações necessárias para que a Application tome a decisão.

---

# 73. Integração com DDD

A autorização não faz parte do modelo de domínio.

Ela representa uma preocupação da camada de aplicação.

Entretanto, o domínio continua protegendo seus próprios invariantes.

Exemplo:

```text
Authorization

↓

Grant XP

↓

Character.grant_experience()
```

Mesmo autorizado, o domínio continua validando:

- limites;
- regras;
- consistência;
- invariantes.

Autorização nunca substitui regras de negócio.

---

# 74. Integração com Arquitetura Hexagonal

A autorização deve permanecer desacoplada das tecnologias externas.

Fluxo:

```text
Interface

↓

Input Adapter

↓

Application

↓

Authorization Service

↓

Domain
```

A implementação concreta do usuário autenticado deve ser obtida por um **Port**.

Exemplo:

```text
CurrentUserProvider
```

Assim, Streamlit, API REST, CLI e Jobs reutilizam exatamente a mesma lógica.

---

# 75. Integração com Eventos

Eventos de domínio não carregam permissões.

A autorização deve ocorrer **antes** da geração do evento.

Fluxo:

```text
Authorization

↓

Use Case

↓

Domain Event

↓

Commit

↓

Publish
```

Event Handlers devem validar autorização apenas quando iniciarem novas operações protegidas.

Nunca confiar que um evento externo já foi autorizado.

---

# 76. Integração com IA

Toda integração com IA deve obedecer às regras de autorização.

Antes de montar o contexto enviado ao modelo:

```text
Authorization

↓

Ownership

↓

Sanitização

↓

Prompt Context

↓

AI Provider
```

Nunca enviar:

- dados de outro usuário;
- informações administrativas;
- tokens;
- notas privadas;
- dados protegidos sem autorização.

A autorização precede qualquer processamento por IA.

---

# 77. Convenções Oficiais

Todo componente relacionado à autorização deve seguir a nomenclatura oficial.

Exemplos:

```text
AuthorizationService

AuthorizationContext

AuthorizationPolicy

WorkoutPolicy

BookPolicy

HabitPolicy

Permission

Role

CurrentUser

CurrentUserProvider

AuthorizationError

PermissionDeniedError

OwnershipViolationError
```

Evitar nomes genéricos como:

```text
SecurityManager

AccessUtil

PermissionHelper

CommonAuthorization
```

A nomenclatura deve refletir claramente a responsabilidade do componente.

---

# 78. Referências Arquiteturais

Este documento está alinhado com:

- Clean Architecture;
- Domain-Driven Design (DDD);
- Arquitetura Hexagonal;
- SOLID;
- CQRS Light;
- Event-Driven Architecture;
- Modular Monolith.

Também complementa diretamente:

- `SECURITY.md`;
- `ERRORS.md`;
- `USE_CASES.md`;
- `SERVICES.md`;
- `REPOSITORIES.md`;
- `docs/04_BACKEND/UNIT_OF_WORK.md`;
- `docs/04_BACKEND/TRANSACTIONS.md`;
- `DTOs.md`;
- `VALIDATORS.md`;
- `08_EVENTS.md`.

Todos esses documentos devem permanecer consistentes entre si.

---

# 79. ADRs Relacionadas

Qualquer alteração estrutural na estratégia de autorização deverá gerar uma **Architecture Decision Record (ADR)**.

Exemplos:

- adoção de novo modelo RBAC;
- migração para ABAC;
- autorização baseada em organizações;
- introdução de permissões delegadas;
- compartilhamento de recursos;
- alteração do fluxo de autorização;
- mudança de provedor de identidade.

Toda decisão arquitetural relevante deve permanecer documentada para preservar o histórico técnico do projeto.

---

# 80. Encerramento

A autorização do LifeOS constitui uma das camadas fundamentais da arquitetura da plataforma.

Ela foi projetada para ser:

- centralizada;
- previsível;
- desacoplada;
- testável;
- auditável;
- extensível;
- independente da tecnologia utilizada.

A combinação de:

- Ownership;
- RBAC;
- Policies;
- Contexto;
- Multi-Tenant;
- Auditoria;
- Defesa em Profundidade;

garante que todas as operações do sistema sejam executadas de maneira segura e consistente.

Este documento estabelece o padrão oficial que deverá ser seguido por todos os módulos, serviços, interfaces e agentes de IA envolvidos no desenvolvimento do LifeOS, assegurando uma base sólida para evolução futura sem comprometer segurança, manutenibilidade ou coerência arquitetural.
