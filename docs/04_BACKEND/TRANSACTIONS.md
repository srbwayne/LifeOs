# TRANSACTIONS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de Transações  
**Camadas Relacionadas:** Application e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture  
**Persistência Inicial:** SQLAlchemy + SQLite  
**Persistência Futura:** PostgreSQL

---

# 1. Objetivo

Este documento define o padrão oficial de transações do LifeOS.

Seu objetivo é estabelecer:

- como fronteiras transacionais devem ser definidas;
- quais operações exigem atomicidade;
- como commit e rollback devem funcionar;
- como múltiplos Repositories devem participar da mesma transação;
- como módulos devem colaborar sem romper isolamento arquitetural;
- como eventos devem ser coordenados com persistência;
- como chamadas externas devem ser separadas da transação;
- como consistência imediata e eventual devem ser tratadas;
- como concorrência, idempotência e retry devem ser avaliados;
- como testes devem provar o comportamento transacional.

Toda operação que altera estado persistente deve seguir este documento.

---

# 2. Escopo

Este documento cobre:

- definição de transação;
- atomicidade;
- consistência;
- isolamento;
- durabilidade;
- fronteira transacional;
- Unit of Work;
- commit;
- rollback;
- flush;
- savepoints;
- transações entre módulos;
- transações com eventos;
- consistência imediata;
- consistência eventual;
- idempotência;
- concorrência;
- optimistic locking;
- retries;
- timeouts;
- chamadas externas;
- Outbox Pattern;
- transações de leitura;
- testes;
- observabilidade;
- anti-patterns;
- regras para agentes de IA.

Este documento complementa:

- `docs/04_BACKEND/UNIT_OF_WORK.md`;
- `REPOSITORIES.md`;
- `USE_CASES.md`;
- `SERVICES.md`;
- `ERRORS.md`;
- `DATABASE.md`;
- `MIGRATIONS.md`;
- `02_ARCHITECTURE/08_EVENTS.md`;
- `02_ARCHITECTURE/07_DEPENDENCY_RULES.md`.

---

# 3. Definição

Transação é uma unidade lógica de trabalho que deve ser concluída integralmente ou revertida integralmente.

Exemplo:

```text
Registrar treino
    ↓
Persistir treino
    ↓
Conceder XP
    ↓
Atualizar Character
    ↓
Registrar transação de XP
```

Essas etapas representam uma única intenção de negócio.

Se qualquer etapa falhar:

```text
Rollback completo
```

---

# 4. Propriedades ACID

O LifeOS adota as propriedades ACID como referência.

## Atomicidade

Tudo ocorre ou nada ocorre.

## Consistência

O estado final respeita invariantes.

## Isolamento

Uma transação não deve observar estado parcial de outra.

## Durabilidade

Após commit, os dados devem permanecer persistidos.

---

# 5. Princípio Fundamental

A fronteira transacional deve corresponder à intenção do usuário ou do sistema.

Exemplos:

```text
RegisterUserUseCase
RegisterWorkoutUseCase
CompleteHabitUseCase
ResetPasswordUseCase
GrantExperienceUseCase
```

Cada Use Case de escrita deve possuir uma fronteira transacional clara.

---

# 6. Responsabilidade da Application Layer

A Application Layer define:

- início da transação;
- fim da transação;
- quais Repositories participam;
- quando commit deve ocorrer;
- quando rollback deve ocorrer;
- quando eventos podem ser publicados;
- quais operações externas devem acontecer depois.

A Application não conhece SQLAlchemy diretamente.

---

# 7. Responsabilidade da Infrastructure Layer

A Infrastructure implementa:

- Session;
- conexão;
- commit;
- rollback;
- flush;
- locks;
- savepoints;
- tratamento técnico;
- tradução de erros;
- integração com o banco.

---

# 8. Responsabilidade do Domain

O Domain:

- protege invariantes;
- altera estado;
- produz eventos;
- valida regras;
- permanece independente da transação técnica.

O Domain não executa:

```python
commit()
rollback()
flush()
```

---

# 9. Fronteira Transacional

A fronteira deve começar antes da primeira alteração persistente e terminar após a última alteração necessária ao caso de uso.

Fluxo:

```text
Open Transaction
    ↓
Load Aggregates
    ↓
Execute Domain Rules
    ↓
Persist Changes
    ↓
Commit
```

---

# 10. Tamanho da Transação

Transações devem ser curtas.

Evitar dentro da transação:

- IA;
- e-mail;
- chamadas HTTP;
- geração de arquivos;
- relatórios pesados;
- espera humana;
- processamento em lote extenso;
- sleeps;
- retries longos.

---

# 11. Unit of Work

Toda transação de escrita deve ser coordenada por Unit of Work.

Exemplo:

```python
with self._unit_of_work as uow:
    ...
    uow.commit()
```

A Unit of Work controla:

- Session;
- Repositories;
- commit;
- rollback;
- encerramento.

---

# 12. Commit

Commit deve ocorrer somente quando:

- validações passaram;
- regras de domínio foram concluídas;
- Aggregates estão consistentes;
- persistência foi preparada;
- não há exceções pendentes.

Exemplo:

```python
uow.commit()
```

---

# 13. Rollback

Rollback deve ocorrer quando:

- uma exceção é lançada;
- uma validação crítica falha;
- o banco rejeita persistência;
- o fluxo é cancelado;
- ocorre conflito;
- um Aggregate não pode ser salvo.

---

# 14. Rollback Automático

A Unit of Work deve executar rollback automático ao sair do contexto com exceção.

Exemplo:

```python
with uow:
    ...
    raise OperationConflictError()
```

Resultado:

```text
Rollback
Close Session
Propagate Error
```

---

# 15. Rollback Explícito

Pode ser utilizado quando o fluxo precisa abortar sem lançar exceção imediatamente.

Exemplo:

```python
uow.rollback()
```

Esse uso deve ser raro e explícito.

---

# 16. Commit Único

Uma operação deve preferir um único commit.

Evitar:

```text
Save User
Commit
Save Character
Commit
Save Preferences
Commit
```

Preferir:

```text
Save User
Save Character
Save Preferences
Commit
```

---

# 17. Proibição de Commit em Repository

Repositories não podem executar commit.

Incorreto:

```python
def save(self, entity):
    self._session.add(model)
    self._session.commit()
```

Correto:

```python
def save(self, entity):
    self._session.add(model)
```

---

# 18. Proibição de Commit em Domain Service

Domain Service não controla transação.

Incorreto:

```python
class ExperienceService:
    def grant(...):
        session.commit()
```

---

# 19. Proibição de Commit em Controller

Controller não deve acessar Session nem Unit of Work diretamente.

Fluxo correto:

```text
Controller
    ↓
Use Case
    ↓
Unit of Work
```

---

# 20. Flush

Flush sincroniza alterações com o banco sem encerrar a transação.

Pode ser utilizado para:

- validar constraint antecipadamente;
- obter valor gerado;
- materializar relações;
- detectar conflito.

No LifeOS, seu uso deve ser excepcional.

---

# 21. Savepoints

Savepoints podem ser utilizados para suboperações controladas.

Exemplo:

```text
Transaction
    ↓
Savepoint
    ↓
Optional Operation
```

Não usar savepoint para esconder design transacional ruim.

---

# 22. Transações Síncronas

Use quando:

- resultado é necessário imediatamente;
- consistência forte é obrigatória;
- usuário aguarda resposta;
- múltiplas alterações pertencem à mesma intenção.

Exemplos:

```text
RegisterUser
RegisterWorkout
ResetPassword
CompleteHabit
```

---

# 23. Transações Assíncronas

Processos assíncronos devem utilizar transações próprias por etapa.

Exemplo:

```text
Create Report Request
    ↓
Commit
    ↓
Background Job
    ↓
Generate File
    ↓
Commit Result
```

---

# 24. Consistência Imediata

Utilizar quando o estado precisa estar disponível imediatamente.

Exemplos:

- login;
- mudança de senha;
- criação de Character;
- concessão de XP;
- conclusão de Quest;
- atualização de sessão.

---

# 25. Consistência Eventual

Utilizar quando o consumidor pode reagir depois.

Exemplos:

- Analytics;
- AI Mentor;
- notificações;
- cache;
- relatórios;
- dashboard derivado.

---

# 26. Transações entre Módulos

Transações entre módulos devem ser evitadas quando possível.

Preferência:

```text
Módulo A commit
    ↓
Evento
    ↓
Módulo B processa
```

Quando atomicidade imediata for obrigatória, utilizar Application Orchestrator.

---

# 27. Orquestração entre Módulos

Exemplo:

```text
RegisterUserUseCase
    ↓
Auth Repository
    ↓
Character Public Facade
    ↓
Preferences Repository
    ↓
Commit
```

A orquestração deve ocorrer na Application Layer.

---

# 28. Regra de Fronteira Modular

Um módulo não acessa Repository interno de outro módulo.

Permitido:

```text
Module Facade
Public Contract
Event
```

Proibido:

```text
Module A
    ↓
Module B Repository
```

---

# 29. Transação de Cadastro

Fluxo recomendado:

```text
Validate Email
    ↓
Create User
    ↓
Create Character
    ↓
Create Preferences
    ↓
Persist All
    ↓
Commit
```

---

# 30. Transação de Treino

Fluxo recomendado:

```text
Load Character
    ↓
Create Workout
    ↓
Calculate XP
    ↓
Grant XP
    ↓
Persist Workout
    ↓
Persist Character
    ↓
Persist Experience Transaction
    ↓
Commit
```

---

# 31. Transação de Hábito

```text
Load Habit
    ↓
Validate Completion
    ↓
Create Habit Record
    ↓
Update Streak
    ↓
Grant XP
    ↓
Commit
```

---

# 32. Transação de Password Reset

```text
Validate Token
    ↓
Hash New Password
    ↓
Update User
    ↓
Invalidate Token
    ↓
Revoke Sessions if Required
    ↓
Commit
```

---

# 33. Transação de Quest

```text
Load Quest Progress
    ↓
Validate Completion
    ↓
Complete Quest
    ↓
Grant Reward
    ↓
Grant XP
    ↓
Commit
```

---

# 34. Transação de Achievement

```text
Evaluate Criteria
    ↓
Check Existing Unlock
    ↓
Create User Achievement
    ↓
Grant Reward
    ↓
Commit
```

---

# 35. Transação de Terapia

```text
Validate Therapist Ownership
    ↓
Create Therapy Session
    ↓
Persist Sensitive Notes
    ↓
Commit
```

Dados sensíveis não devem aparecer em logs.

---

# 36. Transação de Exportação

```text
Create Report Export PENDING
    ↓
Commit
    ↓
Generate File Outside Transaction
    ↓
Update Status COMPLETED
    ↓
Commit
```

---

# 37. Transação de IA

```text
Create AI Request
    ↓
Commit
    ↓
Call Provider
    ↓
Validate Response
    ↓
Persist Recommendation
    ↓
Commit
```

Nunca manter transação aberta durante a chamada ao Provider.

---

# 38. Chamadas Externas

Chamadas externas devem acontecer fora da transação principal.

Exemplos:

- SMTP;
- Gemini;
- OpenAI;
- Storage;
- APIs externas;
- webhooks.

---

# 39. Exceção para Chamada Externa

Somente quando a regra exigir confirmação externa antes da persistência.

Mesmo assim, preferir:

```text
Prepare
    ↓
Call External
    ↓
Open Transaction
    ↓
Persist Confirmed Result
```

---

# 40. Eventos e Transações

Domain Events devem ser coletados durante a execução.

A publicação ocorre após commit.

Fluxo:

```text
Execute Domain
    ↓
Collect Events
    ↓
Persist
    ↓
Commit
    ↓
Publish
```

---

# 41. Evento Fantasma

Evento publicado antes do commit pode gerar estado inexistente.

Exemplo proibido:

```text
Publish WorkoutRegistered
    ↓
Database Commit Fails
```

Esse cenário é proibido.

---

# 42. Falha após Commit

Se o commit ocorrer e a publicação falhar, existe divergência.

Soluções:

- retry;
- Event Store;
- status pendente;
- Outbox Pattern;
- Dead Event.

---

# 43. Outbox Pattern

Quando confiabilidade for obrigatória:

```text
Transaction
├── Persist Aggregate
└── Persist Outbox Event
    ↓
Commit
    ↓
Publisher Worker
```

---

# 44. Idempotência

Transações acionadas por evento ou job devem ser idempotentes.

Estratégias:

- `event_id`;
- `request_id`;
- idempotency key;
- UNIQUE constraint;
- processed_events;
- ledger.

---

# 45. Exemplo de Idempotência

```python
if uow.processed_events.exists(
    event_id=event_id,
    handler_name=handler_name,
):
    return AlreadyProcessedResult()
```

---

# 46. Concorrência

Operações críticas:

- XP;
- Level Up;
- Streak;
- Quest;
- Achievement;
- reset token;
- sessão;
- Character único;
- saldo de pontos.

---

# 47. Optimistic Locking

Pode ser implementado com coluna:

```text
version
```

Fluxo:

```text
Read version 3
    ↓
Update WHERE version = 3
    ↓
Set version = 4
```

Se nenhuma linha for atualizada:

```text
ConcurrentModificationError
```

---

# 48. Pessimistic Locking

Deve ser evitado no SQLite.

No PostgreSQL futuro, utilizar apenas em casos justificados.

---

# 49. Retries Transacionais

Retry pode ser aplicado em falhas transitórias.

Exemplos:

- deadlock;
- lock temporário;
- serialization failure;
- timeout de banco;
- `database is locked`.

---

# 50. Regras de Retry

Retry deve ser:

- limitado;
- idempotente;
- configurável;
- observável;
- aplicado fora do Domain;
- seguro para repetição.

---

# 51. Erros Não Elegíveis para Retry

Não repetir automaticamente:

- validação;
- permissão;
- ownership;
- regra de domínio;
- token inválido;
- conflito permanente;
- dados inconsistentes.

---

# 52. Timeout Transacional

Transações longas devem possuir limite operacional.

O timeout deve ser configurado na Infrastructure.

---

# 53. SQLite

Regras específicas:

- manter transações curtas;
- evitar escrita concorrente;
- utilizar WAL quando validado;
- configurar `busy_timeout`;
- evitar grandes lotes;
- tratar lock transitório.

---

# 54. PostgreSQL

Futuramente poderá utilizar:

- níveis de isolamento;
- optimistic locking;
- row locks;
- savepoints;
- retries de serialization failure;
- advisory locks em casos específicos.

---

# 55. Níveis de Isolamento

Mudança de nível exige:

- justificativa;
- medição;
- testes;
- ADR;
- análise de impacto.

Não alterar por conveniência.

---

# 56. Read Transactions

Queries podem utilizar contexto read-only.

Exemplo:

```text
ReadOnlyUnitOfWork
```

Sem commit.

---

# 57. Snapshot de Leitura

Consultas compostas devem buscar consistência adequada ao caso.

Para Dashboard, uma visão ligeiramente defasada pode ser aceitável.

Para segurança e autenticação, não.

---

# 58. Transações em Lote

Processos em lote devem:

- dividir em chunks;
- evitar transação gigante;
- registrar progresso;
- permitir retomada;
- preservar idempotência;
- controlar memória.

---

# 59. Exemplo em Lote

```text
Import 10.000 records
    ↓
Process 500
    ↓
Commit
    ↓
Process next 500
```

---

# 60. Compensação

Quando não for possível rollback distribuído, utilizar compensação.

Exemplo:

```text
External File Created
    ↓
Database Save Fails
    ↓
Delete File
```

---

# 61. Saga

Futuramente, processos distribuídos podem utilizar Saga.

Exemplo:

```text
Create Account
    ↓
Create Character
    ↓
Provision Cloud Resource
```

Cada etapa possui compensação.

---

# 62. Estado Parcial

Estado parcial é proibido em operações atômicas.

Exemplo incorreto:

```text
Workout persisted
Character not updated
XP not recorded
```

---

# 63. Integridade

A transação deve preservar:

- Aggregate invariants;
- Foreign Keys;
- UNIQUE constraints;
- ledger;
- ownership;
- Multi-Tenant;
- idempotência.

---

# 64. Multi-Tenant

Toda operação deve utilizar `user_id` autenticado.

A transação não substitui filtro Multi-Tenant.

Repositories continuam obrigados a filtrar por tenant.

---

# 65. Ownership

Relações entre registros devem pertencer ao mesmo usuário.

Exemplo:

```text
workout_record.user_id
=
workout_type.user_id
```

Essa regra deve ser validada antes do commit.

---

# 66. Erros Transacionais

Exemplos:

```text
TransactionCommitError
TransactionRollbackError
ConcurrentModificationError
DatabaseLockedError
TransactionTimeoutError
```

Devem ser traduzidos antes da Presentation.

---

# 67. Falha de Rollback

Falha de rollback é crítica.

Deve gerar:

- log ERROR ou CRITICAL;
- correlation ID;
- fechamento forçado;
- descarte da Session;
- alerta operacional.

---

# 68. Falha de Commit

Falha de commit deve:

1. tentar rollback;
2. fechar Session;
3. traduzir erro;
4. não publicar eventos;
5. registrar contexto seguro.

---

# 69. Observabilidade

Registrar:

- início;
- fim;
- commit;
- rollback;
- duração;
- operação;
- módulo;
- correlation ID;
- erro;
- tentativa de retry.

---

# 70. Métricas

Métricas futuras:

```text
transaction_duration
transaction_commit_count
transaction_rollback_count
transaction_retry_count
transaction_timeout_count
database_lock_count
```

---

# 71. Logging Seguro

Não registrar:

- senha;
- token;
- notas terapêuticas;
- payload completo;
- dados de saúde detalhados;
- prompt completo de IA.

---

# 72. Testes Unitários

Use Cases devem ser testados com Fake Unit of Work.

Validar:

- commit;
- rollback;
- ordem;
- ausência de commit;
- publicação de eventos;
- idempotência.

---

# 73. Teste de Commit

```text
Dado fluxo válido
Quando Use Case termina
Então commit ocorre uma vez
```

---

# 74. Teste de Rollback

```text
Dado erro após primeira persistência
Quando Use Case falha
Então rollback ocorre
E nenhum estado parcial permanece
```

---

# 75. Teste de Evento

```text
Dado commit bem-sucedido
Então evento é publicado
```

```text
Dado rollback
Então evento não é publicado
```

---

# 76. Teste de Concorrência

Validar:

- conflito de versão;
- duas conclusões simultâneas;
- XP duplicada;
- token usado duas vezes;
- Achievement duplicado.

---

# 77. Teste de Idempotência

Executar o mesmo comando ou evento duas vezes.

Resultado esperado:

```text
Mesmo estado final
Sem duplicação
```

---

# 78. Testes de Integração

Devem validar:

- commit real;
- rollback real;
- constraints;
- Session compartilhada;
- lock;
- event store;
- Outbox quando implementado;
- SQLite real de teste.

---

# 79. Teste Multi-Tenant

Cenários:

- usuário A altera apenas seus dados;
- usuário B não observa estado parcial;
- relacionamento cross-tenant falha;
- rollback preserva isolamento.

---

# 80. Teste de Chamada Externa

Validar que a chamada externa ocorre depois do commit.

Exemplo:

```text
Commit
    ↓
EmailSender
```

---

# 81. Anti-patterns

São proibidos:

## Commit por Repository

## Múltiplos commits na mesma intenção

## Session criada em cada Repository

## Chamada de IA dentro da transação

## Evento antes do commit

## Retry de regra de domínio

## Transação em Controller

## Transação em Streamlit

## Transação gigante em lote

## Uso de lock sem justificativa

## Catch silencioso de erro transacional

---

# 82. Como o Gemini deve Utilizar este Documento

Antes de implementar uma transação, o agente deve responder:

1. Qual é a intenção de negócio?
2. Qual é a fronteira transacional?
3. Quais Aggregates participam?
4. Quais Repositories participam?
5. Eles compartilham Session?
6. Quantos commits existem?
7. O rollback é automático?
8. Existem chamadas externas?
9. Elas ocorrem fora da transação?
10. Existem eventos?
11. Eles são publicados após commit?
12. Há necessidade de Outbox?
13. A operação é idempotente?
14. Há risco de concorrência?
15. Há retry?
16. É elegível?
17. Multi-Tenant está protegido?
18. Existem testes?

---

# 83. Checklist de Implementação

- [ ] Intenção de negócio definida.
- [ ] Fronteira transacional definida.
- [ ] Unit of Work utilizada.
- [ ] Repositories compartilham Session.
- [ ] Commit único.
- [ ] Rollback automático.
- [ ] Nenhum commit em Repository.
- [ ] Nenhuma Session na Application.
- [ ] Chamadas externas fora da transação.
- [ ] Eventos após commit.
- [ ] Idempotência avaliada.
- [ ] Concorrência avaliada.
- [ ] Retry avaliado.
- [ ] Timeout avaliado.
- [ ] Multi-Tenant validado.
- [ ] Ownership validado.
- [ ] Testes de commit criados.
- [ ] Testes de rollback criados.
- [ ] Testes de idempotência criados.
- [ ] Testes de integração criados.
- [ ] Documentação atualizada.

---

# 84. Critérios de Aceite

Este documento será considerado atendido quando:

- toda operação de escrita possuir fronteira transacional clara;
- commit e rollback forem centralizados;
- Repositories compartilharem a mesma Session;
- eventos forem publicados após commit;
- chamadas externas ocorrerem fora da transação;
- falhas não deixarem estado parcial;
- idempotência estiver protegida;
- concorrência for tratada em operações críticas;
- Multi-Tenant estiver preservado;
- testes provarem comportamento transacional.

---

# 85. Definition of Done

Uma transação só estará concluída quando:

- [ ] Sua fronteira estiver documentada.
- [ ] O commit estiver correto.
- [ ] O rollback estiver correto.
- [ ] A Session estiver isolada.
- [ ] Nenhum estado parcial permanecer.
- [ ] Os eventos estiverem confiáveis.
- [ ] As chamadas externas estiverem separadas.
- [ ] A idempotência estiver validada.
- [ ] A concorrência estiver avaliada.
- [ ] Os testes passarem.
- [ ] A documentação estiver sincronizada.

---

# 86. Declaração Final

Transações existem para proteger a consistência das intenções de negócio do LifeOS.

Elas devem ser curtas, explícitas, testáveis e alinhadas à fronteira dos Use Cases.

Commit, rollback, eventos, Repositories, concorrência e idempotência devem ser coordenados de forma previsível.

Toda operação deve terminar em um estado integralmente válido ou não produzir alteração persistente alguma.
