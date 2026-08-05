# UNIT OF WORK

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Unit of Work  
**Camadas Relacionadas:** Application e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture  
**Persistência Inicial:** SQLAlchemy + SQLite  
**Persistência Futura:** PostgreSQL

---

# 1. Objetivo

Este documento define o padrão oficial de **Unit of Work** do LifeOS.

Seu objetivo é estabelecer:

- como transações devem ser abertas;
- como Repositories devem compartilhar a mesma sessão;
- como commit e rollback devem ocorrer;
- como eventos devem ser publicados após persistência bem-sucedida;
- como operações envolvendo múltiplos Aggregates devem manter consistência;
- como falhas devem ser tratadas;
- como testes devem simular a fronteira transacional;
- como a implementação deve permanecer independente de SQLAlchemy;
- como o isolamento Multi-Tenant deve ser preservado.

Toda operação que altera estado persistente deverá seguir este documento.

---

# 2. Escopo

Este documento cobre:

- definição de Unit of Work;
- fronteira transacional;
- ciclo de vida;
- commit;
- rollback;
- flush;
- Repositories;
- SQLAlchemy Session;
- eventos;
- idempotência;
- consistência entre módulos;
- transações síncronas;
- operações assíncronas;
- tratamento de erros;
- testes;
- anti-patterns;
- regras para agentes de IA;
- critérios de aceite;
- Definition of Done.

Este documento complementa:

- `REPOSITORIES.md`;
- `SERVICES.md`;
- `USE_CASES.md`;
- `VALIDATORS.md`;
- `DATABASE.md`;
- `MIGRATIONS.md`;
- `02_ARCHITECTURE/08_EVENTS.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`.

---

# 3. Definição

Unit of Work é o componente responsável por controlar uma unidade transacional completa.

Ela agrupa:

- uma sessão de persistência;
- um ou mais Repositories;
- alterações realizadas durante um caso de uso;
- commit;
- rollback;
- coleta de eventos;
- encerramento de recursos.

Fluxo conceitual:

```text
Use Case
    ↓
Unit of Work
    ↓
Repositories
    ↓
Session
    ↓
Database
```

---

# 4. Princípio Fundamental

Uma intenção de negócio deve possuir uma fronteira transacional clara.

Exemplo:

```text
Registrar treino
    ↓
Criar Workout
    ↓
Atualizar Character
    ↓
Registrar XP
    ↓
Commit único
```

Se qualquer etapa falhar:

```text
Rollback completo
```

Nenhum estado parcial deve permanecer.

---

# 5. Responsabilidades

A Unit of Work deve:

- abrir a transação;
- criar ou receber a sessão;
- fornecer Repositories ligados à mesma sessão;
- controlar commit;
- controlar rollback;
- encerrar a sessão;
- coletar eventos quando aplicável;
- publicar eventos no momento correto;
- impedir commit após falha;
- preservar consistência.

A Unit of Work não deve:

- executar regras de negócio;
- validar domínio;
- montar DTOs;
- conhecer Streamlit;
- conhecer Controllers;
- executar lógica de autorização;
- gerar relatórios;
- chamar IA diretamente.

---

# 6. Localização do Contrato

O contrato da Unit of Work deve existir na Application Layer ou Shared Application Kernel.

Estrutura recomendada:

```text
src/lifeos/shared/application/unit_of_work.py
```

ou, quando específica:

```text
src/lifeos/modules/<module>/application/ports/unit_of_work.py
```

A implementação concreta deve existir na Infrastructure.

---

# 7. Localização da Implementação

Estrutura:

```text
src/lifeos/infrastructure/database/unit_of_work.py
```

Implementação:

```text
SqlAlchemyUnitOfWork
```

---

# 8. Contrato Oficial

```python
from typing import Protocol


class UnitOfWork(Protocol):
    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
```

---

# 9. Contrato com Repositories

Quando a Unit of Work expõe Repositories:

```python
class LifeOSUnitOfWork(Protocol):
    users: UserRepository
    characters: CharacterRepository
    workouts: WorkoutRepository
    experience_transactions: ExperienceTransactionRepository

    def __enter__(self) -> "LifeOSUnitOfWork":
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
```

Essa abordagem garante que todos compartilhem a mesma sessão.

---

# 10. Implementação SQLAlchemy

Exemplo conceitual:

```python
class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: SqlAlchemySessionFactory,
    ) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory.create()

        self.users = SqlAlchemyUserRepository(self._session)
        self.characters = SqlAlchemyCharacterRepository(self._session)
        self.workouts = SqlAlchemyWorkoutRepository(self._session)

        return self

    def commit(self) -> None:
        if self._session is None:
            raise RuntimeError("Unit of Work is not active.")

        self._session.commit()

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        if self._session is None:
            return

        try:
            if exc_type is not None:
                self._session.rollback()
        finally:
            self._session.close()
            self._session = None
```

---

# 11. Ciclo de Vida

Fluxo oficial:

```text
Create Unit of Work
    ↓
Enter Context
    ↓
Open Session
    ↓
Create Repositories
    ↓
Execute Use Case
    ↓
Commit or Rollback
    ↓
Close Session
```

---

# 12. Uso em Command Use Case

```python
class RegisterWorkoutUseCase:
    def __init__(
        self,
        unit_of_work: LifeOSUnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    def execute(
        self,
        command: RegisterWorkoutCommand,
    ) -> RegisterWorkoutResult:
        with self._unit_of_work as uow:
            workout = Workout.create(
                user_id=command.user_id,
                workout_type_id=command.workout_type_id,
                occurred_at=command.occurred_at,
            )

            uow.workouts.save(workout)
            uow.commit()

        return RegisterWorkoutResult(
            workout_id=str(workout.id),
        )
```

---

# 13. Fronteira Transacional

A fronteira deve corresponder à intenção do usuário.

Exemplos:

```text
RegisterUserUseCase
RegisterWorkoutUseCase
CompleteHabitUseCase
GrantExperienceUseCase
ResetPasswordUseCase
```

Cada um deve possuir uma unidade transacional própria.

---

# 14. Commit

Commit deve ocorrer apenas quando:

- todas as validações passaram;
- todas as regras foram executadas;
- todos os Aggregates estão consistentes;
- todas as persistências foram preparadas;
- nenhuma exceção foi lançada.

Exemplo:

```python
uow.commit()
```

Commit não deve ocorrer:

- dentro de Repository;
- dentro de Domain Service;
- dentro de Entity;
- dentro de Controller;
- dentro de página Streamlit.

---

# 15. Rollback

Rollback deve ocorrer quando:

- uma exceção for lançada;
- uma validação crítica falhar;
- uma constraint for violada;
- a persistência falhar;
- um Aggregate não puder ser salvo;
- uma operação transacional for cancelada.

O rollback deve ser automático no `__exit__` quando houver exceção.

---

# 16. Rollback Explícito

Rollback explícito pode ser utilizado quando:

- a operação é cancelada sem exceção;
- a aplicação decide abortar;
- uma falha controlada exige reversão;
- o fluxo precisa encerrar antes do retorno.

Exemplo:

```python
uow.rollback()
```

Seu uso deve ser raro.

---

# 17. Regra de Não Commit

A ausência de `commit()` deve resultar em descarte das alterações ao sair do contexto.

Exemplo:

```python
with uow:
    uow.workouts.save(workout)
    # sem commit
```

Resultado esperado:

```text
Nenhuma alteração persistida
```

---

# 18. Flush

`flush()` envia alterações para o banco sem concluir a transação.

Pode ser necessário para:

- validar constraint antes do commit;
- obter valor gerado pelo banco;
- sincronizar relações;
- detectar conflito antecipadamente.

Como os IDs do LifeOS são gerados pela aplicação, `flush()` deve ser excepcional.

---

# 19. Interface de Flush

Caso necessário:

```python
class UnitOfWork(Protocol):
    def flush(self) -> None:
        ...
```

Nunca utilizar `Session.flush()` diretamente na Application.

---

# 20. Repositories Compartilhados

Todos os Repositories usados na mesma operação devem compartilhar a mesma sessão.

Correto:

```text
UserRepository
CharacterRepository
PreferencesRepository
    ↓
Same Session
```

Incorreto:

```text
Cada Repository cria sua própria Session
```

---

# 21. Repositories e Unit of Work

Duas estratégias são permitidas.

## Estratégia A — Repositories expostos pela Unit of Work

```python
with uow:
    user = uow.users.find_by_email(...)
```

## Estratégia B — Repositories injetados com Session coordenada

```python
with uow:
    self._user_repository.save(user)
```

A estratégia escolhida deve ser consistente no projeto.

A recomendação oficial é a Estratégia A para operações transacionais complexas.

---

# 22. Unit of Work por Módulo

Cada módulo pode possuir Unit of Work própria quando:

- possui persistência isolada;
- não compartilha transação com outros módulos;
- a fronteira modular exige isolamento;
- existe clara propriedade transacional.

Exemplo:

```text
AuthUnitOfWork
GameUnitOfWork
AnalyticsUnitOfWork
```

---

# 23. Unit of Work Compartilhada

Pode existir uma Unit of Work compartilhada no monólito modular quando:

- múltiplos módulos usam o mesmo banco;
- a operação exige atomicidade;
- os Repositories precisam da mesma Session;
- os módulos permanecem desacoplados por contratos.

Essa decisão deve ser registrada em ADR quando consolidada.

---

# 24. Transações entre Módulos

Transações entre módulos devem ser evitadas quando possível.

Preferência:

```text
Módulo A commit
    ↓
Evento
    ↓
Módulo B processa
```

Quando atomicidade imediata for obrigatória, utilizar Application Service ou Orchestrator com contrato público.

---

# 25. Exemplo entre Auth e Character

Cadastro inicial pode exigir:

```text
Criar User
Criar Character
Criar Preferences
```

Se todas as tabelas pertencem ao mesmo banco e a consistência é obrigatória:

```text
Uma transação
```

Se futuramente os módulos forem separados:

```text
Saga / Process Manager
```

---

# 26. Unit of Work e Domain Events

Aggregates podem registrar eventos internamente.

Exemplo:

```python
character.grant_experience(amount)

events = character.collect_domain_events()
```

A Unit of Work pode coletar esses eventos antes ou após persistência, mas a publicação deve respeitar o commit.

---

# 27. Ordem Oficial dos Eventos

Fluxo recomendado:

```text
Execute Domain
    ↓
Collect Events
    ↓
Persist Aggregates
    ↓
Commit
    ↓
Publish Events
```

Nunca publicar antes do commit.

---

# 28. Evento após Commit

Exemplo:

```python
events = character.collect_domain_events()

with uow:
    uow.characters.save(character)
    uow.commit()

event_publisher.publish_all(events)
```

---

# 29. Falha na Publicação de Evento

Se o commit ocorreu e a publicação falhou:

```text
Banco confirmado
Evento não entregue
```

Isso exige estratégia de confiabilidade.

Soluções possíveis:

- Event Store;
- Outbox Pattern;
- retry;
- status pendente;
- Dead Event.

---

# 30. Outbox Pattern

O Outbox Pattern deve ser adotado quando houver necessidade de garantir atomicidade entre:

- persistência;
- publicação de eventos;
- integrações externas.

Fluxo:

```text
Transaction
├── Persist Aggregate
└── Persist Outbox Event
    ↓
Commit
    ↓
Background Publisher
```

---

# 31. Escopo Inicial de Eventos

Na versão inicial, o LifeOS pode utilizar:

```text
InMemory Event Bus
```

com persistência operacional no `event_store` quando necessário.

Evolução futura:

```text
Transactional Outbox
```

---

# 32. Idempotência

Unit of Work deve colaborar com idempotência.

Exemplo:

```text
event_id UNIQUE
```

Antes de criar transação de XP:

```python
if uow.experience_transactions.exists_by_event_id(event_id):
    return AlreadyProcessedResult()
```

---

# 33. Concorrência

Operações críticas:

- XP;
- Level Up;
- Streak;
- Quest;
- Achievement;
- token de reset;
- sessão;
- Character único.

A Unit of Work deve manter transações curtas.

---

# 34. Optimistic Locking

Pode ser adotado futuramente usando:

```text
version
```

Exemplo:

```text
characters.version
```

A atualização deve verificar a versão anterior.

---

# 35. Pessimistic Locking

Deve ser evitado no SQLite.

No PostgreSQL futuro, poderá ser utilizado apenas em operações críticas e justificadas.

---

# 36. Unit of Work e SQLite

Regras:

- transações curtas;
- evitar chamadas externas dentro da transação;
- evitar cálculos pesados;
- evitar grandes lotes;
- utilizar WAL quando validado;
- tratar `database is locked`.

---

# 37. Unit of Work e PostgreSQL

Futuramente poderá utilizar:

- níveis de isolamento;
- savepoints;
- locks;
- retries controlados;
- transações distribuídas apenas se inevitável.

---

# 38. Níveis de Isolamento

A versão inicial deve utilizar o padrão seguro do banco e ORM.

Mudanças de nível exigem:

- medição;
- justificativa;
- teste;
- ADR;
- análise de concorrência.

---

# 39. Savepoints

Savepoints podem ser utilizados em operações avançadas.

Exemplo:

```text
Transação principal
    ↓
Savepoint
    ↓
Operação opcional
```

Não utilizar como substituto para bom design.

---

# 40. Chamadas Externas

Não executar dentro da transação:

- envio de e-mail;
- chamada Gemini;
- chamada OpenAI;
- upload;
- geração PDF;
- API externa;
- processamento demorado.

Fluxo correto:

```text
Persist
    ↓
Commit
    ↓
Call External Service
```

ou evento assíncrono.

---

# 41. Transações e E-mail

Recuperação de senha:

```text
Gerar token
    ↓
Persistir hash
    ↓
Commit
    ↓
Enviar e-mail
```

Se o e-mail falhar:

- token permanece válido;
- erro é registrado;
- retry pode ser realizado;
- não recriar token sem necessidade.

---

# 42. Transações e IA

Fluxo recomendado:

```text
Persistir solicitação
    ↓
Commit
    ↓
Chamar AI Provider
    ↓
Persistir resposta em nova transação
```

Nunca manter transação aberta durante geração de IA.

---

# 43. Transações e Relatórios

Fluxo:

```text
Criar report_export com status PENDING
    ↓
Commit
    ↓
Gerar arquivo
    ↓
Atualizar status em nova transação
```

---

# 44. Tratamento de Exceções

A Unit of Work deve traduzir falhas técnicas quando necessário.

Exemplos:

```text
IntegrityError
OperationalError
DatabaseError
```

Essas exceções não devem chegar diretamente à UI.

---

# 45. Exceções no `__exit__`

O `__exit__` deve:

1. detectar exceção;
2. executar rollback;
3. fechar sessão;
4. não ocultar a exceção por padrão.

Retornar `False` ou `None` para propagar.

---

# 46. Estado da Unit of Work

A Unit of Work deve possuir estado interno controlado.

Estados conceituais:

```text
NEW
ACTIVE
COMMITTED
ROLLED_BACK
CLOSED
```

Chamadas inválidas devem falhar explicitamente.

---

# 47. Commit Duplo

É proibido executar commit duas vezes na mesma Unit of Work.

Exemplo de erro:

```text
commit()
commit()
```

A implementação pode proteger essa condição.

---

# 48. Uso após Fechamento

Após sair do contexto:

```python
with uow:
    ...

uow.commit()
```

deve falhar.

---

# 49. Nesting

Unit of Work aninhada deve ser evitada.

Incorreto:

```python
with uow_a:
    with uow_b:
        ...
```

Se ambas usam o mesmo banco, isso pode quebrar atomicidade.

---

# 50. Propagação Transacional

Application Services chamados dentro de um Use Case devem reutilizar a transação atual.

Eles não devem abrir nova Unit of Work sem necessidade.

---

# 51. Orquestração

O componente de mais alto nível deve controlar a transação.

Exemplo:

```text
RegisterUserUseCase
    ↓
AccountInitializationService
```

O Use Case controla a Unit of Work.

O Service reutiliza Repositories disponíveis.

---

# 52. Query Use Cases

Queries somente leitura não precisam de Unit of Work de escrita.

Podem utilizar:

- Query Repository;
- sessão de leitura;
- contexto read-only;
- conexão otimizada.

---

# 53. Read-Only Unit of Work

Pode existir:

```python
class ReadOnlyUnitOfWork(Protocol):
    def __enter__(self) -> "ReadOnlyUnitOfWork":
        ...

    def __exit__(...):
        ...
```

Sem `commit()`.

---

# 54. Testes Unitários

Use Cases devem utilizar Fake Unit of Work.

Exemplo:

```python
class FakeUnitOfWork:
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        if exc_type is not None:
            self.rollback()
```

---

# 55. Teste de Commit

Cenário:

```text
Dado fluxo válido
Quando Use Case termina
Então commit foi realizado
```

---

# 56. Teste de Rollback

Cenário:

```text
Dado erro durante persistência
Quando Use Case falha
Então rollback foi realizado
E nenhum estado parcial permanece
```

---

# 57. Teste de Evento

Cenário:

```text
Dado commit bem-sucedido
Quando Use Case termina
Então eventos são publicados
```

Cenário negativo:

```text
Dado rollback
Então eventos não são publicados
```

---

# 58. Testes de Integração

Devem validar:

- mesma Session;
- commit real;
- rollback real;
- Foreign Keys;
- constraints;
- visibilidade das alterações;
- fechamento de sessão;
- eventos;
- falha de banco.

---

# 59. Teste Multi-Tenant

A Unit of Work não substitui validação Multi-Tenant.

Os testes devem garantir:

- Repositories recebem `user_id`;
- nenhuma operação cruza tenant;
- rollback não afeta transações de outro usuário;
- eventos preservam `user_id`.

---

# 60. Observabilidade

Registrar:

- início;
- commit;
- rollback;
- duração;
- correlation ID;
- tipo de operação;
- erro técnico.

Não registrar dados sensíveis.

---

# 61. Métricas

Métricas futuras:

- duração média;
- taxa de rollback;
- taxa de erro;
- transações longas;
- bloqueios;
- deadlocks;
- commits por módulo.

---

# 62. Configuração

Unit of Work não deve ler ambiente diretamente.

Deve receber:

- Session Factory;
- Event Publisher;
- opções técnicas;
- timeout, quando aplicável.

---

# 63. Composition Root

A implementação deve ser criada no Bootstrap.

Exemplo:

```python
def build_unit_of_work() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(
        session_factory=build_session_factory(),
    )
```

---

# 64. Anti-patterns

São proibidos:

## Commit em Repository

```python
self._session.commit()
```

## Session em Use Case

```python
class UseCase:
    def __init__(self, session: Session):
        ...
```

## Uma Session por Repository

Cada Repository cria conexão própria.

## Transação na UI

```python
with session:
```

em Streamlit.

## Chamada externa dentro da transação

```text
Open Transaction
→ Call AI
→ Commit
```

## Evento antes do commit

```text
Publish
→ Commit
```

## Unit of Work gigante

Uma UoW expondo todos os módulos sem necessidade e criando forte acoplamento.

## Nesting improvisado

Várias UoWs independentes no mesmo fluxo.

---

# 65. Como o Gemini deve Utilizar este Documento

Antes de implementar uma operação transacional, o agente deve responder:

1. Qual é a intenção de negócio?
2. Qual é a fronteira transacional?
3. Quais Repositories participam?
4. Eles compartilham a mesma Session?
5. Quem controla o commit?
6. O rollback é automático?
7. Existem chamadas externas?
8. Elas ocorrem após commit?
9. Existem Domain Events?
10. Quando serão publicados?
11. Há necessidade de Outbox?
12. A operação é idempotente?
13. Há risco de concorrência?
14. Há isolamento Multi-Tenant?
15. Existem testes de commit e rollback?
16. A documentação está atualizada?

---

# 66. Checklist de Implementação

- [ ] Fronteira transacional definida.
- [ ] Contrato da Unit of Work utilizado.
- [ ] Implementação concreta na Infrastructure.
- [ ] Repositories compartilham Session.
- [ ] Commit fora dos Repositories.
- [ ] Rollback automático.
- [ ] Session fechada.
- [ ] Chamadas externas fora da transação.
- [ ] Eventos coletados.
- [ ] Eventos publicados após commit.
- [ ] Idempotência avaliada.
- [ ] Concorrência avaliada.
- [ ] Multi-Tenant preservado.
- [ ] Teste de commit criado.
- [ ] Teste de rollback criado.
- [ ] Teste de evento criado.
- [ ] Teste de integração criado.
- [ ] Logging seguro.
- [ ] Documentação atualizada.

---

# 67. Critérios de Aceite

Este documento será considerado atendido quando:

- toda escrita possuir fronteira transacional clara;
- Repositories compartilharem a mesma sessão;
- commit e rollback forem centralizados;
- SQLAlchemy permanecer na Infrastructure;
- eventos forem publicados após commit;
- chamadas externas não prolongarem transações;
- falhas não deixarem estado parcial;
- testes provarem commit, rollback e eventos;
- Multi-Tenant permanecer protegido;
- a implementação puder migrar de SQLite para PostgreSQL sem alterar Use Cases.

---

# 68. Definition of Done

Uma operação transacional só estará concluída quando:

- [ ] A Unit of Work estiver integrada.
- [ ] O commit estiver no ponto correto.
- [ ] O rollback estiver validado.
- [ ] Nenhum Repository executar commit.
- [ ] Nenhuma camada externa acessar Session.
- [ ] Os eventos estiverem confiáveis.
- [ ] Chamadas externas ocorrerem fora da transação.
- [ ] Idempotência estiver avaliada.
- [ ] Multi-Tenant estiver testado.
- [ ] Testes unitários passarem.
- [ ] Testes de integração passarem.
- [ ] A documentação estiver sincronizada.

---

# 69. Declaração Final

A Unit of Work define a fronteira de consistência das operações do LifeOS.

Ela existe para garantir que uma intenção de negócio seja persistida por completo ou não seja persistida.

Commit, rollback, Repositories, Session e eventos devem permanecer coordenados por uma única fronteira transacional.

Toda implementação deve priorizar consistência, simplicidade, testabilidade, isolamento Multi-Tenant e independência tecnológica.
