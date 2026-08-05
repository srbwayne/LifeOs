# VALIDATORS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Validação  
**Camadas Relacionadas:** Presentation, Application, Domain e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal e Monólito Modular

---

# 1. Objetivo

Este documento define o padrão oficial de validação do LifeOS.

Seu objetivo é estabelecer:

- onde cada tipo de validação deve ocorrer;
- quais validações pertencem à interface;
- quais validações pertencem à Application Layer;
- quais validações pertencem ao Domain;
- quais validações pertencem à Infrastructure;
- como erros de validação devem ser representados;
- como evitar duplicação de regras;
- como preservar consistência Multi-Tenant;
- como Validators devem ser nomeados, organizados e testados.

Toda validação implementada no LifeOS deverá respeitar este documento.

---

# 2. Escopo

Este documento cobre:

- validações de formato;
- validações de entrada;
- validações de aplicação;
- invariantes de domínio;
- validações de autorização;
- validações Multi-Tenant;
- validações de persistência;
- Validators;
- Specifications;
- Policies;
- Value Objects;
- tratamento de erros;
- mensagens;
- internacionalização;
- testes;
- anti-patterns;
- regras para agentes de IA.

Este documento complementa:

- `USE_CASES.md`;
- `SERVICES.md`;
- `REPOSITORIES.md`;
- `DATABASE.md`;
- `02_ARCHITECTURE/02_CLEAN_ARCHITECTURE.md`;
- `02_ARCHITECTURE/03_DDD.md`;
- `02_ARCHITECTURE/HEXAGONAL.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`.

---

# 3. Princípio Central

Validação não é uma responsabilidade única.

Ela ocorre em camadas diferentes porque cada camada protege uma fronteira diferente.

Fluxo oficial:

```text
Presentation Validation
        ↓
Application Validation
        ↓
Domain Validation
        ↓
Infrastructure Validation
```

Cada camada deve validar apenas aquilo que lhe pertence.

---

# 4. Tipos Oficiais de Validação

O LifeOS reconhece quatro categorias principais:

```text
Presentation Validation
Application Validation
Domain Validation
Infrastructure Validation
```

Também existem validações transversais de segurança, autorização e isolamento Multi-Tenant.

---

# 5. Presentation Validation

A Presentation valida formato e usabilidade da entrada.

Responsabilidades:

- campo obrigatório visual;
- tipo esperado;
- conversão simples;
- limite de caracteres;
- valor numérico;
- formato de data;
- formato básico de e-mail;
- feedback imediato;
- mensagens de interface.

Exemplos:

```text
Campo Nome não preenchido
Data em formato inválido
Valor não numérico
Senha e confirmação visualmente diferentes
```

A Presentation não decide regra de negócio.

---

# 6. Application Validation

A Application valida pré-condições do fluxo.

Responsabilidades:

- usuário autenticado;
- autorização;
- existência de recurso;
- ownership;
- estado atual compatível;
- conflito de operação;
- idempotência;
- dependências disponíveis;
- escopo Multi-Tenant.

Exemplos:

```text
Usuário existe?
Character existe?
Treino pertence ao usuário?
Quest já foi concluída?
Token ainda é válido?
```

---

# 7. Domain Validation

O Domain protege invariantes e regras de negócio.

Responsabilidades:

- XP não negativa;
- nível mínimo;
- percentual válido;
- esforço entre 0 e 10;
- Character não pode possuir estado inválido;
- Quest não pode ser concluída duas vezes;
- Achievement não pode ser desbloqueado sem critério;
- Value Object deve nascer válido.

Exemplos:

```text
ExperiencePoints(value >= 0)
Percentage(0 <= value <= 100)
Level(value >= 1)
Email(normalizado e válido)
```

---

# 8. Infrastructure Validation

A Infrastructure valida integridade técnica.

Responsabilidades:

- conexão disponível;
- payload serializável;
- resposta externa válida;
- arquivo acessível;
- hash compatível;
- schema persistente;
- configuração obrigatória;
- tipo de banco suportado;
- constraint técnica.

Exemplos:

```text
SMTP configurado
Resposta da API contém campo esperado
Arquivo de backup existe
Migration aplicada
```

---

# 9. Regra de Não Duplicação

A mesma regra não deve ser implementada integralmente em várias camadas.

Exemplo:

```text
Domain:
Percentage deve estar entre 0 e 100
```

A Presentation pode impedir visualmente valores inválidos, mas o Domain continua sendo a fonte de verdade.

A validação visual não substitui a invariante do domínio.

---

# 10. Fonte de Verdade

A prioridade oficial é:

```text
Domain Invariant
    ↓
Application Precondition
    ↓
Presentation Feedback
    ↓
Infrastructure Constraint
```

Em caso de divergência, o Domain prevalece para regras de negócio.

---

# 11. Validators

Validator é um componente responsável por validar entrada ou condição específica quando a validação não pertence naturalmente a um Value Object, Entity, Policy ou Specification.

Exemplos:

```text
RegisterUserCommandValidator
RegisterWorkoutCommandValidator
PasswordResetRequestValidator
DateRangeValidator
PaginationValidator
```

---

# 12. Quando Criar um Validator

Criar Validator quando:

- múltiplos campos precisam ser validados juntos;
- a validação pertence à Application;
- a regra é de formato ou fluxo;
- a mesma validação será reutilizada;
- o Command precisa ser validado antes do Use Case;
- a validação não representa uma invariante de Entity.

Não criar Validator quando:

- a regra pertence ao Value Object;
- a regra pertence à Entity;
- a regra é uma Policy;
- a regra é uma Specification;
- a regra pertence ao Repository;
- a regra é apenas formatação visual.

---

# 13. Localização dos Validators

Estrutura oficial:

```text
src/lifeos/modules/<module>/application/validators/
```

Exemplo:

```text
src/lifeos/modules/auth/application/validators/
├── register_user_command_validator.py
├── login_command_validator.py
└── reset_password_command_validator.py
```

Validators visuais reutilizáveis podem existir em:

```text
src/lifeos/interfaces/streamlit/forms/validators/
```

Eles não substituem Validators da Application.

---

# 14. Contrato de Validator

Exemplo:

```python
from typing import Protocol, TypeVar

T = TypeVar("T")


class Validator(Protocol[T]):
    def validate(
        self,
        value: T,
    ) -> None:
        ...
```

A validação pode lançar erro específico.

---

# 15. Exemplo de Command Validator

```python
class RegisterUserCommandValidator:
    def validate(
        self,
        command: RegisterUserCommand,
    ) -> None:
        errors: list[ValidationErrorItem] = []

        if not command.full_name.strip():
            errors.append(
                ValidationErrorItem(
                    field="full_name",
                    code="required",
                    message="Nome é obrigatório.",
                )
            )

        if command.password != command.password_confirmation:
            errors.append(
                ValidationErrorItem(
                    field="password_confirmation",
                    code="password_mismatch",
                    message="As senhas devem ser iguais.",
                )
            )

        if errors:
            raise CommandValidationError(errors)
```

---

# 16. Resultado de Validação

O padrão oficial utiliza erros estruturados.

```python
from dataclasses import dataclass


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
        super().__init__("Command validation failed.")
```

---

# 17. Fail Fast e Erros Agregados

Existem dois modos possíveis.

## Fail Fast

Interrompe no primeiro erro.

Indicado para:

- invariantes de domínio;
- segurança;
- autorização;
- ownership;
- estado inválido crítico.

## Erros Agregados

Retorna múltiplos erros.

Indicado para:

- formulários;
- Commands;
- filtros;
- dados de entrada.

---

# 18. Value Objects

Value Objects devem validar a si mesmos.

Exemplo:

```python
@dataclass(frozen=True)
class Percentage:
    value: Decimal

    def __post_init__(self) -> None:
        if self.value < 0 or self.value > 100:
            raise InvalidPercentageError()
```

Não depender de Validator externo para garantir validade permanente.

---

# 19. Entities

Entities devem proteger suas invariantes.

Exemplo:

```python
class Character:
    def grant_experience(
        self,
        amount: ExperiencePoints,
    ) -> None:
        if amount.value <= 0:
            raise InvalidExperienceGrantError()

        self._total_experience += amount
```

A Entity não deve aceitar transição inválida.

---

# 20. Aggregates

Aggregate Root deve validar consistência interna.

Exemplos:

- Character controla seus atributos;
- Quest controla progresso e conclusão;
- Habit controla frequência e estado;
- User controla status e credenciais associadas.

Entidades internas não devem ser alteradas sem passar pela Aggregate Root.

---

# 21. Specifications

Specifications devem representar regras booleanas reutilizáveis.

Exemplo:

```python
class EligibleForLevelUpSpecification:
    def is_satisfied_by(
        self,
        character: Character,
    ) -> bool:
        ...
```

Use Specifications para critérios de elegibilidade.

Não usar Validator genérico quando a semântica for uma Specification de domínio.

---

# 22. Policies

Policies representam regras variáveis.

Exemplos:

```text
PasswordPolicy
ExperiencePolicy
RewardPolicy
StreakPolicy
```

Validator pode utilizar Policy.

Exemplo:

```python
class RegisterUserCommandValidator:
    def __init__(
        self,
        password_policy: PasswordPolicy,
    ) -> None:
        self._password_policy = password_policy
```

---

# 23. Validação de Commands

Todo Command deve ser validado antes da execução principal.

Fluxo:

```text
Controller
    ↓
Command
    ↓
Command Validator
    ↓
Use Case
```

Alternativamente, o Use Case pode iniciar chamando o Validator.

A estratégia deve permanecer consistente em todo o projeto.

---

# 24. Validação de Queries

Queries devem validar:

- paginação;
- ordenação;
- intervalo de datas;
- filtros;
- limites;
- campos permitidos.

Exemplo:

```python
class WorkoutHistoryQueryValidator:
    def validate(
        self,
        query: WorkoutHistoryQuery,
    ) -> None:
        ...
```

---

# 25. Validação de Paginação

Regras oficiais:

```text
page >= 1
1 <= size <= 100
```

Exemplo:

```python
class PaginationValidator:
    def validate(
        self,
        page: int,
        size: int,
    ) -> None:
        if page < 1:
            raise InvalidPageError()

        if size < 1 or size > 100:
            raise InvalidPageSizeError()
```

---

# 26. Validação de Ordenação

Campos de ordenação devem ser permitidos explicitamente.

Exemplo:

```python
ALLOWED_FIELDS = {
    "occurred_at",
    "created_at",
    "name",
}
```

Nunca aceitar livremente nomes de coluna vindos da interface.

---

# 27. Validação de Intervalo de Datas

Regras:

```text
start_date <= end_date
```

Opcionalmente:

```text
intervalo máximo permitido
```

Exemplo:

```python
if start_date > end_date:
    raise InvalidDateRangeError()
```

---

# 28. Validação Multi-Tenant

A validação Multi-Tenant deve ocorrer na Application e no Repository.

Application:

- valida identidade;
- valida ownership;
- propaga `user_id`.

Repository:

- filtra por `user_id`;
- nunca retorna dado de outro usuário.

---

# 29. Ownership Validator

Pode existir quando a regra for reutilizada.

Exemplo:

```python
class OwnershipValidator:
    def ensure_owned_by(
        self,
        resource_user_id: UserId,
        current_user_id: UserId,
    ) -> None:
        if resource_user_id != current_user_id:
            raise PermissionDeniedError()
```

Não substituir filtro Multi-Tenant do Repository.

---

# 30. Autorização

Autorização deve validar:

- role;
- permission;
- ownership;
- escopo;
- estado da conta.

Exemplo:

```python
class PermissionEvaluator(Protocol):
    def ensure_allowed(
        self,
        actor: UserIdentity,
        action: Permission,
    ) -> None:
        ...
```

---

# 31. Validação de Senha

A senha deve ser validada por `PasswordPolicy`.

Possíveis critérios:

- tamanho mínimo;
- tamanho máximo;
- complexidade;
- senha comum;
- igualdade com confirmação;
- reutilização futura;
- bloqueio de senha vazada, quando disponível.

A senha nunca deve aparecer em logs ou mensagens técnicas.

---

# 32. Validação de E-mail

O e-mail deve ser representado por Value Object.

Responsabilidades:

- normalização;
- trim;
- lowercase;
- formato;
- tamanho.

Unicidade pertence ao fluxo de Application e persistência.

---

# 33. Validação de Token

Tokens devem validar:

- existência;
- hash;
- expiração;
- uso anterior;
- escopo;
- usuário;
- revogação.

Exemplo:

```text
Token válido
Token expirado
Token já utilizado
Token revogado
Token não encontrado
```

---

# 34. Validação de Sessão

A sessão deve validar:

- token;
- expiração;
- revogação;
- usuário ativo;
- última atividade;
- escopo.

A interface não deve considerar apenas a presença de `user_id` no estado visual como autenticação suficiente.

---

# 35. Validação de Dados de Saúde

Regras devem ser conservadoras.

Exemplos:

```text
sleep_score: 0 a 10
body_fat_percentage: 0 a 100
heart_rate: positivo
sleep_duration: não negativa
```

O sistema não deve emitir diagnóstico.

Valores extremos podem gerar aviso, mas não devem ser interpretados clinicamente sem requisito explícito.

---

# 36. Validação de Treino

Exemplos:

```text
duration_minutes >= 0
perceived_effort entre 0 e 10
distance_km >= 0
average_heart_rate_bpm > 0
```

A combinação de campos pode variar por modalidade.

Essa regra pode pertencer a Policy de modalidade.

---

# 37. Validação de Leitura

Exemplos:

```text
pages_read > 0
pages_read não ultrapassa limite plausível quando total conhecido
finished_at >= started_at
```

O domínio decide quando um livro pode ser concluído.

---

# 38. Validação de Terapia

Exemplos:

```text
clarity_after_session entre 0 e 10
therapist pertence ao usuário
session_date obrigatória
```

Notas terapêuticas são sensíveis.

Validators não devem registrar conteúdo.

---

# 39. Validação de Hábitos

Exemplos:

```text
target_count > 0
frequency_type válido
completed_count >= 0
record_date válida
```

A conclusão deve respeitar o estado do hábito.

---

# 40. Validação de Gamificação

Exemplos:

```text
XP válida
Quest ativa
Quest não concluída
Achievement elegível
Reward ainda não concedida
```

Essas regras pertencem ao Domain e Specifications.

---

# 41. Validação de IA

Antes de enviar dados a um Provider:

- remover dados desnecessários;
- minimizar informações pessoais;
- validar tamanho do contexto;
- validar prompt;
- validar limites;
- validar consentimento quando necessário;
- validar disponibilidade do Provider.

Depois da resposta:

- validar estrutura;
- validar campos esperados;
- validar tamanho;
- filtrar conteúdo inválido;
- não tratar resposta como verdade absoluta.

---

# 42. Validação de Arquivos

Para uploads e exports:

- extensão;
- MIME type;
- tamanho;
- nome seguro;
- path permitido;
- integridade;
- conteúdo esperado;
- ausência de path traversal.

---

# 43. Validação de Configuração

Na inicialização, validar:

- banco configurado;
- diretórios acessíveis;
- e-mail configurado quando habilitado;
- provedor de IA configurado quando habilitado;
- chaves presentes;
- ambiente reconhecido;
- timezone padrão;
- políticas válidas.

Falha crítica deve impedir startup.

---

# 44. Validação na Infrastructure

A Infrastructure deve traduzir erros técnicos.

Exemplo:

```text
IntegrityError
    ↓
EmailAlreadyRegisteredPersistenceError
```

Ela não deve gerar erro de regra de negócio sem tradução apropriada.

---

# 45. Constraints de Banco

O banco deve reforçar invariantes estáveis.

Exemplos:

```text
UNIQUE(email)
CHECK(score BETWEEN 0 AND 10)
CHECK(total_experience >= 0)
```

Constraints não substituem Domain Validation.

---

# 46. Mensagens de Erro

Mensagens devem ser:

- claras;
- objetivas;
- seguras;
- sem detalhes técnicos;
- sem dados sensíveis;
- adequadas ao usuário.

Exemplo:

```text
E-mail já cadastrado.
```

Evitar:

```text
UNIQUE constraint failed: users.email
```

---

# 47. Códigos de Erro

Toda validação deve possuir código estável.

Exemplos:

```text
required
invalid_format
not_found
permission_denied
ownership_violation
password_mismatch
token_expired
invalid_date_range
invalid_score
```

A mensagem pode mudar.

O código deve permanecer estável.

---

# 48. Estrutura de Erro

Exemplo:

```python
@dataclass(frozen=True)
class ApplicationErrorDetail:
    code: str
    message: str
    field: str | None = None
    metadata: Mapping[str, object] | None = None
```

Não incluir dados sensíveis em `metadata`.

---

# 49. Internacionalização

Mensagens podem futuramente ser traduzidas.

Por isso:

- código do erro é estável;
- mensagem é camada de apresentação;
- Domain Error não deve depender de idioma;
- Presenter pode resolver mensagem localizada.

---

# 50. Logging de Validação

Pode registrar:

- código;
- operação;
- correlation ID;
- user ID mascarado;
- tipo de recurso.

Não registrar:

- senha;
- token;
- conteúdo terapêutico;
- payload completo;
- dados biométricos detalhados;
- prompt completo de IA.

---

# 51. Performance

Validators devem ser eficientes.

Evitar:

- múltiplas consultas para a mesma validação;
- consultas duplicadas;
- validações pesadas em loops;
- acesso externo durante validação simples;
- carregar Aggregate completo quando `exists` resolve.

---

# 52. Validação e Repositories

Use métodos específicos:

```text
exists_by_email
exists_for_user
find_by_id
```

Evitar carregar registros apenas para validar existência quando isso não for necessário.

---

# 53. Validação Assíncrona

Validações dependentes de recursos externos podem ser assíncronas quando o fluxo permitir.

Exemplos:

- reputação de e-mail;
- validação de integração;
- verificação de provider;
- análise pesada de arquivo.

Regras críticas do domínio não devem depender exclusivamente de validação assíncrona tardia.

---

# 54. Fail Safe

Em segurança, na dúvida, negar.

Exemplos:

```text
Usuário não identificado → negar
Permissão desconhecida → negar
Tenant inconsistente → negar
Token ambíguo → negar
```

---

# 55. Testes Unitários

Todo Validator deve possuir testes para:

- entrada válida;
- cada erro individual;
- múltiplos erros;
- limites;
- valores nulos;
- valores extremos;
- códigos de erro.

---

# 56. Testes de Domain Validation

Devem validar:

- Entity rejeita estado inválido;
- Value Object rejeita valor inválido;
- Aggregate protege invariante;
- Policy aplica regra correta;
- Specification retorna resultado esperado.

---

# 57. Testes de Application Validation

Devem validar:

- recurso inexistente;
- ownership;
- usuário inativo;
- operação conflitante;
- idempotência;
- autorização;
- Multi-Tenant.

---

# 58. Testes de Infrastructure Validation

Devem validar:

- constraint;
- serialização;
- configuração;
- resposta externa inválida;
- arquivo inválido;
- falha técnica traduzida.

---

# 59. Testes Multi-Tenant

Cenários obrigatórios:

```text
Usuário A não lê dado de B
Usuário A não altera dado de B
Usuário A não exclui dado de B
Usuário A não exporta dado de B
Usuário A não usa ID de B em relacionamento
```

---

# 60. Anti-patterns

São proibidos:

## Validação apenas na UI

```text
Slider limita 0 a 10
```

sem proteção no Domain.

## Validator genérico gigante

```text
GlobalValidator
CommonValidator
DataValidator
```

## Regra de negócio em Controller

```python
if xp > 100:
    ...
```

## SQL em Validator

```python
session.query(...)
```

na Application.

## Duplicação

Mesma fórmula validada em três locais diferentes.

## Retorno booleano sem contexto

```python
False
```

sem código ou erro estruturado.

## Exposição técnica

```text
IntegrityError
```

mostrado ao usuário.

## Validação depois do commit

Persistir estado antes de validar regra crítica.

---

# 61. Como o Gemini deve Utilizar este Documento

Antes de criar uma validação, o agente deve responder:

1. Qual camada é responsável?
2. É formato, fluxo, domínio ou infraestrutura?
3. A regra pertence a Value Object?
4. A regra pertence a Entity?
5. A regra pertence a Policy?
6. A regra pertence a Specification?
7. É necessário um Validator?
8. Existe duplicação?
9. Há impacto Multi-Tenant?
10. Há autorização?
11. O erro possui código?
12. A mensagem é segura?
13. Há dados sensíveis?
14. A validação exige consulta?
15. A constraint de banco também é necessária?
16. Existem testes?

---

# 62. Checklist de Implementação

- [ ] Camada correta identificada.
- [ ] Regra não duplicada.
- [ ] Value Object avaliado.
- [ ] Entity avaliada.
- [ ] Policy avaliada.
- [ ] Specification avaliada.
- [ ] Validator criado apenas quando necessário.
- [ ] Código de erro definido.
- [ ] Mensagem segura.
- [ ] Multi-Tenant validado.
- [ ] Ownership validado.
- [ ] Autorização validada.
- [ ] Dados sensíveis protegidos.
- [ ] Constraints avaliadas.
- [ ] Testes unitários criados.
- [ ] Testes de integração criados quando necessários.
- [ ] Documentação atualizada.

---

# 63. Critérios de Aceite

Este documento será considerado atendido quando:

- cada validação estiver na camada correta;
- invariantes permanecerem no Domain;
- pré-condições permanecerem na Application;
- formato permanecer na Presentation;
- integridade técnica permanecer na Infrastructure;
- erros forem estruturados;
- Multi-Tenant for protegido;
- mensagens não expuserem detalhes técnicos;
- Validators forem pequenos e específicos;
- testes cobrirem limites e falhas.

---

# 64. Definition of Done

Uma validação só estará concluída quando:

- [ ] A responsabilidade estiver clara.
- [ ] A camada estiver correta.
- [ ] A regra estiver centralizada.
- [ ] O erro possuir código estável.
- [ ] A mensagem for apropriada.
- [ ] Multi-Tenant estiver protegido.
- [ ] Segurança estiver avaliada.
- [ ] Constraints estiverem alinhadas.
- [ ] Testes passarem.
- [ ] A documentação estiver sincronizada.

---

# 65. Declaração Final

A validação no LifeOS deve proteger cada fronteira sem duplicar responsabilidades.

A interface melhora a experiência.

A Application protege o fluxo.

O Domain protege o negócio.

A Infrastructure protege a integração técnica.

A qualidade da validação depende de colocar cada regra no local correto, com erros claros, testes adequados e proteção permanente do isolamento Multi-Tenant.
