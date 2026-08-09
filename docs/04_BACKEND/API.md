# API

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Padrão Oficial de APIs  
**Camadas Relacionadas:** Presentation, Application e Infrastructure  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Monólito Modular e Event-Driven Architecture

---

# 1. Objetivo

Este documento define o padrão oficial para todas as APIs do LifeOS.

Seu objetivo é estabelecer uma especificação única para o desenvolvimento de interfaces HTTP, garantindo consistência, previsibilidade, segurança e evolução sustentável da plataforma.

Este documento define:

- arquitetura das APIs;
- organização dos endpoints;
- contratos públicos;
- DTOs;
- versionamento;
- autenticação;
- autorização;
- tratamento de erros;
- paginação;
- filtros;
- observabilidade;
- monitoramento;
- boas práticas;
- governança.

Embora a primeira versão do LifeOS utilize Streamlit como interface principal, toda a arquitetura será preparada para futura disponibilização de APIs REST.

---

# 2. Escopo

Este documento cobre:

- APIs REST;
- recursos;
- endpoints;
- Requests;
- Responses;
- DTOs;
- autenticação;
- autorização;
- versionamento;
- paginação;
- filtros;
- ordenação;
- busca;
- uploads;
- downloads;
- exportações;
- operações assíncronas;
- monitoramento;
- observabilidade;
- documentação OpenAPI;
- testes;
- governança.

Este documento complementa:

- `DTOs.md`;
- `ERRORS.md`;
- `AUTHORIZATION.md`;
- `SECURITY.md`;
- `docs/04_BACKEND/TRANSACTIONS.md`;
- `LOGGING.md`;
- `CONFIGURATION.md`;
- `USE_CASES.md`;
- `docs/02_ARCHITECTURE/08_EVENTS.md`.

---

# 3. Filosofia da API

Toda API do LifeOS deve seguir os seguintes princípios.

## API como Contrato

A API representa um contrato público entre consumidores e a plataforma.

Mudanças incompatíveis devem ser evitadas.

---

## Resource-Oriented

A API deve representar recursos do domínio.

Exemplos:

```text
Users

Characters

Workouts

Habits

Books

Therapy Sessions

Achievements
```

Nunca criar endpoints baseados apenas em ações técnicas.

---

## Consistência

Endpoints semelhantes devem seguir padrões semelhantes.

Exemplo:

```text
GET    /workouts

POST   /workouts

GET    /workouts/{id}

PUT    /workouts/{id}

DELETE /workouts/{id}
```

---

## Simplicidade

A API deve ser simples para consumir.

Evitar:

- parâmetros excessivos;
- respostas inconsistentes;
- múltiplos formatos para o mesmo recurso.

---

# 4. REST Principles

A API seguirá os princípios REST.

Características:

- Stateless;
- Resource-Oriented;
- Uniform Interface;
- HTTP Semantics;
- Cache Friendly;
- Layered System.

Cada requisição deve conter todas as informações necessárias para seu processamento.

O servidor não deve depender de estado mantido entre requisições.

---

# 5. Resource-Oriented Design

Todo endpoint deve representar um recurso de negócio.

Correto:

```text
/users

/workouts

/books

/habits

/characters

/quests
```

Evitar:

```text
/createWorkout

/getBooks

/updateCharacter
```

As operações devem ser representadas pelos métodos HTTP.

---

# 6. Versionamento

Toda API pública deve possuir versionamento explícito.

Padrão oficial:

```text
/api/v1
```

Exemplo:

```text
GET /api/v1/workouts
```

Futuras versões:

```text
/api/v2
```

Mudanças incompatíveis nunca devem ocorrer dentro da mesma versão.

## 6.1 Estado implementado — READ-001

A Reading Library está atualmente exposta sem prefixo de versão, conforme a aplicação FastAPI implantada:

### `POST /books`

- autenticação: obrigatória;
- status de sucesso: `201 Created`;
- ownership: derivado exclusivamente do `UserId` autenticado.

Request:

| Campo | Obrigatoriedade |
|---|---|
| `title` | Obrigatório |
| `author` | Obrigatório |
| `total_pages` | Obrigatório |
| `isbn` | Opcional |
| `publisher` | Opcional |
| `edition` | Opcional |
| `cover` | Opcional |
| `genre` | Opcional |
| `language` | Opcional |

A API não recebe `owner_id`, `user_id` ou `player_id` do cliente.

Response `BookResponse`:

- `id`;
- `title`;
- `author`;
- `total_pages`;
- `isbn`;
- `publisher`;
- `edition`;
- `cover`;
- `genre`;
- `language`.

O owner não integra o contrato público.

### `GET /books`

- autenticação: obrigatória;
- status de sucesso: `200 OK`;
- resposta: coleção dos livros pertencentes exclusivamente ao usuário autenticado;
- biblioteca vazia: `200 OK` com `[]`.

READ-001 não implementa filtros, busca, paginação, ordenação configurável, endpoint individual ou listagem global.

O Repository recebe obrigatoriamente o `UserId` autenticado e filtra a consulta por ownership.

> Divergência conhecida: estas rotas implantadas ainda não utilizam o prefixo normativo `/api/v1`. A decisão global de versionamento permanece pendente e não é alterada por READ-001.

---

# 7. Responsabilidades

Cada camada possui responsabilidades específicas.

## Presentation (API Layer)

Responsável por:

- receber requisições HTTP;
- validar formato;
- converter DTOs;
- chamar Use Cases;
- converter respostas.

---

## Application

Responsável por:

- executar Use Cases;
- autorização;
- orquestração;
- transações.

---

## Domain

Responsável por:

- regras de negócio;
- invariantes;
- Aggregates;
- Domain Events.

---

## Infrastructure

Responsável por:

- HTTP Server;
- serialização;
- autenticação;
- persistência;
- logging;
- monitoramento.

---

# 8. Arquitetura da API

Fluxo oficial:

```text
HTTP Request

↓

Controller

↓

Request DTO

↓

Use Case

↓

Application

↓

Domain

↓

Repository

↓

Response DTO

↓

HTTP Response
```

A API nunca acessa diretamente:

- Repository;
- ORM;
- Database;
- Entities.

Toda interação ocorre através dos Use Cases.

---

# 9. Convenções

Todas as APIs devem seguir convenções oficiais.

URLs:

```text
/workouts

/books

/users

/quests
```

Sempre utilizar:

- substantivos;
- plural;
- letras minúsculas;
- hífen quando necessário.

Nunca utilizar:

```text
/getUser

/CreateWorkout

/DeleteBook
```

JSON:

```json
{
  "id": "...",
  "name": "...",
  "created_at": "..."
}
```

Padrão:

- `snake_case` para propriedades JSON;
- URLs em minúsculas;
- identificadores imutáveis.

---

# 10. Fluxo Oficial da API

Toda requisição deverá seguir o fluxo abaixo.

```text
HTTP Request

↓

Authentication

↓

Authorization

↓

Request DTO

↓

Validation

↓

Use Case

↓

Application

↓

Domain

↓

Repository

↓

Commit

↓

Response DTO

↓

HTTP Response
```

Caso ocorra erro:

```text
HTTP Request

↓

Validation

↓

Exception

↓

Error Translator

↓

Standard Error Response
```

Nenhuma resposta da API deve expor:

- stack traces;
- exceções internas;
- SQL;
- detalhes da infraestrutura;
- informações sensíveis.

Toda API do LifeOS deve produzir contratos previsíveis, consistentes, seguros e independentes da implementação interna da plataforma, preservando o desacoplamento arquitetural e a evolução controlada do sistema.

---

# 11. Endpoints

Os Endpoints representam os pontos de entrada públicos da API.

Cada Endpoint deve corresponder a uma capacidade de negócio claramente definida.

Exemplo:

```text
GET    /api/v1/workouts

POST   /api/v1/workouts

GET    /api/v1/workouts/{id}

PUT    /api/v1/workouts/{id}

DELETE /api/v1/workouts/{id}
```

Um Endpoint nunca deve executar lógica de negócio diretamente.

Seu papel é:

- receber a requisição;
- validar o formato;
- construir o Request DTO;
- invocar o Use Case;
- converter a resposta.

---

# 12. HTTP Methods

Toda operação deve utilizar o método HTTP apropriado.

Padrão oficial:

```text
GET
```

Consultar recursos.

---

```text
POST
```

Criar recursos.

---

```text
PUT
```

Atualizar completamente um recurso.

---

```text
PATCH
```

Atualização parcial.

Utilizar apenas quando fizer sentido para o domínio.

---

```text
DELETE
```

Remover um recurso.

---

Nunca utilizar:

```text
GET
```

para operações que alteram estado.

---

# 13. Request DTOs

Toda entrada da API deve ser representada por um Request DTO.

Exemplo:

```python
CreateWorkoutRequest

UpdateWorkoutRequest

CompleteHabitRequest

CreateBookRequest
```

O Controller nunca deve receber Entities.

Fluxo:

```text
HTTP Request

↓

Request DTO

↓

Validation

↓

Use Case
```

Request DTOs pertencem à camada Presentation.

---

# 14. Response DTOs

Toda resposta da API deve utilizar Response DTOs.

Exemplo:

```python
WorkoutResponse

BookResponse

CharacterResponse

UserResponse
```

Nunca retornar:

- Entities;
- ORM Models;
- Aggregates.

Fluxo:

```text
Use Case

↓

Response DTO

↓

JSON
```

Os DTOs representam o contrato público da API.

---

# 15. Status Codes

A API deve utilizar códigos HTTP padronizados.

Operações bem-sucedidas:

```text
200 OK

201 Created

202 Accepted

204 No Content
```

Erros do cliente:

```text
400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Unprocessable Entity

429 Too Many Requests
```

Erros internos:

```text
500 Internal Server Error

503 Service Unavailable
```

Nunca utilizar:

```text
200 OK
```

para representar falhas.

---

# 16. Error Responses

Toda resposta de erro deve seguir um formato único.

Modelo oficial:

```json
{
    "error": {
        "code": "WORKOUT_NOT_FOUND",
        "message": "Workout não encontrado.",
        "correlation_id": "...",
        "timestamp": "..."
    }
}
```

Campos obrigatórios:

- code;
- message;
- correlation_id;
- timestamp.

Nunca retornar:

- stack trace;
- SQL;
- exceções internas.

---

# 17. Pagination

Endpoints que retornam coleções devem suportar paginação.

Parâmetros oficiais:

```text
page

size
```

Exemplo:

```text
GET /workouts?page=1&size=20
```

Resposta:

```json
{
    "items": [],
    "page": 1,
    "size": 20,
    "total_items": 320,
    "total_pages": 16
}
```

Paginação evita respostas excessivamente grandes.

---

# 18. Filtering

Filtros devem ser explícitos.

Exemplo:

```text
GET /workouts?type=RUNNING
```

Outro exemplo:

```text
GET /habits?active=true
```

Filtros devem:

- possuir documentação;
- possuir comportamento determinístico;
- ser opcionais;
- utilizar nomes consistentes.

Nunca utilizar filtros implícitos.

---

# 19. Sorting

Coleções devem permitir ordenação quando aplicável.

Parâmetros oficiais:

```text
sort

order
```

Exemplo:

```text
GET /workouts?sort=date&order=desc
```

Valores:

```text
asc

desc
```

Campos permitidos devem ser explicitamente definidos.

Nunca permitir ordenação arbitrária em qualquer coluna.

---

# 20. Searching

A API poderá suportar busca textual.

Parâmetro oficial:

```text
query
```

Exemplo:

```text
GET /workouts?query=running
```

Regras:

- busca opcional;
- independente da paginação;
- compatível com filtros;
- compatível com ordenação.

Fluxo:

```text
HTTP Request

↓

Validation

↓

Search Criteria

↓

Use Case

↓

Repository

↓

Paginated Response
```

A implementação da busca deve permanecer transparente ao consumidor da API, preservando o contrato público independentemente da estratégia utilizada internamente (SQLite, PostgreSQL ou mecanismos especializados de pesquisa).

---

# 21. Authentication

Toda API protegida deve exigir autenticação antes da execução de qualquer regra de negócio.

Fluxo oficial:

```text
HTTP Request

↓

Authentication

↓

Current User

↓

Authorization

↓

Use Case
```

A autenticação deve ser completamente transparente para os Use Cases.

Os Use Cases recebem apenas o usuário autenticado através do `CurrentUserProvider`.

A estratégia de autenticação (JWT, Session, OAuth, API Key, etc.) deve permanecer encapsulada na Infrastructure.

---

# 22. Authorization

Após a autenticação, toda operação protegida deve passar pelo processo de autorização.

Fluxo:

```text
Authentication

↓

Authorization Service

↓

Policy

↓

Use Case
```

Toda decisão de autorização segue o documento:

```text
AUTHORIZATION.md
```

O Controller nunca implementa regras de autorização.

---

# 23. Rate Limiting

Toda API pública deve suportar limitação de requisições.

Objetivos:

- evitar abuso;
- reduzir ataques;
- proteger infraestrutura;
- controlar consumo de recursos.

Exemplos:

```text
100 requests/minuto
```

ou

```text
1000 requests/hora
```

Quando o limite for excedido:

```http
429 Too Many Requests
```

O mecanismo de Rate Limiting pertence à Infrastructure.

---

# 24. Idempotência

Operações críticas devem suportar idempotência quando aplicável.

Exemplos:

- pagamentos;
- criação de recursos externos;
- importações;
- integrações;
- processamento de eventos.

Estratégia:

```text
Idempotency-Key

↓

Validation

↓

Already Processed?

↓

Yes

↓

Return Previous Result
```

Operações GET já são naturalmente idempotentes.

---

# 25. Upload

Toda operação de Upload deve utilizar endpoint específico.

Exemplo:

```text
POST /api/v1/uploads
```

Antes da persistência devem ocorrer:

- autenticação;
- autorização;
- validação;
- limite de tamanho;
- validação de extensão;
- validação de MIME Type.

Fluxo:

```text
Upload

↓

Validation

↓

Storage

↓

Response
```

Nunca confiar apenas na extensão do arquivo.

---

# 26. Download

Todo Download exige autorização.

Fluxo:

```text
Request

↓

Authentication

↓

Authorization

↓

Ownership

↓

Download
```

Nunca disponibilizar URLs públicas para recursos privados.

Exemplo:

```text
GET /api/v1/files/{id}
```

A autorização ocorre antes da recuperação do arquivo.

---

# 27. Export

Exportações representam operações potencialmente custosas.

Exemplo:

```text
POST /api/v1/workouts/export
```

A exportação deve validar:

- autenticação;
- autorização;
- Feature Flags;
- limites operacionais;
- formato solicitado.

Formatos previstos:

```text
CSV

Excel

PDF
```

Exportações extensas poderão ser executadas de forma assíncrona.

---

# 28. Import

Importações alteram estado da aplicação.

Fluxo:

```text
Upload

↓

Validation

↓

Authentication

↓

Authorization

↓

Import Use Case

↓

Commit
```

Antes da importação devem ser validados:

- formato;
- estrutura;
- consistência;
- ownership;
- limites.

Toda importação deve produzir auditoria.

---

# 29. Batch Operations

Operações em lote devem possuir endpoints específicos.

Exemplo:

```text
POST /api/v1/workouts/batch
```

ou

```text
POST /api/v1/workouts/import
```

Regras:

- limite máximo de itens;
- validação individual;
- resposta consolidada;
- auditoria;
- logging.

Sempre documentar claramente o comportamento em caso de falha parcial.

---

# 30. Async Operations

Operações longas podem ser executadas de forma assíncrona.

Exemplos:

- exportações;
- importações;
- geração de relatórios;
- processamento de IA;
- backups.

Fluxo:

```text
HTTP Request

↓

Validation

↓

Create Job

↓

202 Accepted

↓

Background Job

↓

Processing

↓

Completed
```

Resposta inicial:

```http
202 Accepted
```

Opcionalmente poderá ser retornado:

```json
{
    "job_id": "...",
    "status": "PENDING"
}
```

A API deve permitir acompanhamento do processamento através de endpoint específico, preservando consistência, rastreabilidade e desacoplamento entre a requisição original e a execução assíncrona.

---

# 31. OpenAPI

Toda API pública do LifeOS deve possuir documentação formal baseada na especificação **OpenAPI**.

Objetivos:

- documentar contratos;
- facilitar integração;
- permitir geração automática de clientes;
- servir como fonte oficial da API.

A especificação deve incluir:

- endpoints;
- parâmetros;
- DTOs;
- códigos HTTP;
- exemplos;
- autenticação;
- erros.

A documentação OpenAPI deve ser gerada automaticamente sempre que possível.

---

# 32. Swagger

A API deverá disponibilizar documentação interativa através do Swagger UI.

Exemplo:

```text
/api/docs
```

ou

```text
/swagger
```

A documentação deve permitir:

- consultar endpoints;
- visualizar DTOs;
- executar requisições de teste (quando permitido);
- visualizar exemplos;
- compreender autenticação.

Em produção, o acesso poderá ser protegido por autenticação ou restrito ao ambiente administrativo.

---

# 33. Versionamento Evolutivo

A evolução da API deve preservar compatibilidade.

Princípios:

- adicionar antes de remover;
- depreciar antes de eliminar;
- evitar breaking changes;
- manter contratos estáveis.

Exemplo:

```text
v1

↓

v1.1

↓

v1.2

↓

v2
```

Mudanças incompatíveis somente poderão ocorrer em uma nova versão principal.

---

# 34. Depreciação

Endpoints antigos devem seguir um processo formal de descontinuação.

Fluxo:

```text
Endpoint

↓

Deprecated

↓

Documentação Atualizada

↓

Período de Migração

↓

Remoção
```

A documentação deverá informar:

- data da depreciação;
- alternativa recomendada;
- previsão de remoção.

Endpoints depreciados continuam funcionando durante o período de transição.

---

# 35. Caching

Operações de leitura poderão utilizar mecanismos de cache quando apropriado.

Exemplos:

```text
GET /api/v1/books

GET /api/v1/achievements
```

Operações que alteram estado nunca devem ser armazenadas em cache.

A estratégia poderá utilizar:

- Cache-Control;
- ETag;
- Last-Modified.

A política de cache pertence à Infrastructure.

---

# 36. Compression

A API deverá suportar compressão de respostas quando apropriado.

Formatos previstos:

```text
gzip

brotli
```

Objetivos:

- reduzir tráfego;
- melhorar desempenho;
- diminuir tempo de resposta.

A compressão deve ser transparente para a Application.

---

# 37. Headers

A API utilizará cabeçalhos padronizados.

Exemplos:

```text
Authorization

Content-Type

Accept

Accept-Language

Correlation-ID

Idempotency-Key
```

Também poderão ser utilizados:

```text
If-None-Match

If-Modified-Since

X-Request-ID
```

Cabeçalhos personalizados devem ser documentados oficialmente.

---

# 38. Correlation ID

Toda requisição deverá possuir um Correlation ID.

Fluxo:

```text
HTTP Request

↓

Correlation ID

↓

Controller

↓

Use Case

↓

Repository

↓

Response
```

Caso o cliente não envie um identificador, a API deverá gerar um automaticamente.

O Correlation ID deverá estar presente:

- nos logs;
- nas auditorias;
- nas métricas;
- nas respostas de erro.

---

# 39. API Logging

Toda requisição relevante deverá produzir logs estruturados.

Registrar:

- método HTTP;
- endpoint;
- duração;
- usuário autenticado;
- status HTTP;
- Correlation ID;
- tamanho da resposta;
- falhas.

Nunca registrar:

- senha;
- tokens;
- API Keys;
- payloads sensíveis;
- dados médicos;
- notas terapêuticas.

O Logging segue integralmente o documento `LOGGING.md`.

---

# 40. API Monitoring

A API deverá fornecer informações para monitoramento operacional.

Indicadores sugeridos:

```text
Requests/Second

Average Latency

95th Percentile

Error Rate

Authentication Failures

Authorization Denied

Rate Limit Hits

Timeouts

Retries

Availability
```

Essas métricas deverão integrar-se à plataforma oficial de observabilidade do LifeOS.

A coleta de métricas deve permanecer desacoplada da lógica de negócio, permitindo evolução independente da infraestrutura e garantindo visibilidade completa sobre o comportamento da API em qualquer ambiente de execução.

---

# 41. Performance

A API do LifeOS deve ser projetada para oferecer baixa latência, previsibilidade e escalabilidade.

Objetivos:

- minimizar tempo de resposta;
- reduzir consumo de recursos;
- evitar consultas desnecessárias;
- permitir crescimento sustentável.

Boas práticas:

- paginação obrigatória;
- consultas otimizadas;
- índices apropriados;
- cache quando aplicável;
- compressão;
- processamento assíncrono para operações longas.

A camada de API nunca deve executar lógica que comprometa o desempenho da aplicação.

---

# 42. Segurança

Toda API deve seguir integralmente as diretrizes estabelecidas em:

- `SECURITY.md`;
- `AUTHORIZATION.md`;
- `CONFIGURATION.md`.

Toda requisição deve executar:

```text
Authentication

↓

Authorization

↓

Validation

↓

Use Case
```

Nunca permitir:

- acesso sem autenticação;
- bypass de autorização;
- exposição de informações internas;
- SQL Injection;
- Mass Assignment;
- enumeração de recursos.

A segurança deve ser aplicada antes da execução da regra de negócio.

---

# 43. Multi-Tenant

A API deve preservar completamente o isolamento entre usuários.

Fluxo:

```text
HTTP Request

↓

Authentication

↓

Current User

↓

Authorization

↓

Ownership

↓

Repository

↓

Response
```

Todo endpoint protegido deve garantir que:

- um usuário nunca visualize recursos de outro;
- um usuário nunca altere recursos de outro;
- um usuário nunca exclua recursos de outro.

O isolamento Multi-Tenant é obrigatório em todos os endpoints.

---

# 44. Observabilidade

Toda operação relevante da API deve contribuir para a observabilidade da plataforma.

Registrar:

- Correlation ID;
- duração;
- endpoint;
- usuário;
- status HTTP;
- exceções;
- retries;
- chamadas externas.

Fluxo:

```text
HTTP Request

↓

Logging

↓

Metrics

↓

Tracing

↓

Monitoring
```

Esses dados alimentam a plataforma oficial de observabilidade do LifeOS.

---

# 45. Testes

Toda API deve possuir testes automatizados.

Categorias mínimas:

- testes unitários;
- testes de integração;
- testes funcionais;
- testes de contrato;
- testes de autorização;
- testes Multi-Tenant;
- testes de segurança.

Cada endpoint deve possuir cenários de:

- sucesso;
- validação;
- erro;
- autorização negada;
- recurso inexistente.

---

# 46. Mock APIs

Durante desenvolvimento e testes poderão ser utilizadas implementações simuladas.

Exemplo:

```text
Fake API

↓

Request

↓

Mock Response
```

Os Mocks devem reproduzir:

- contratos;
- Status Codes;
- DTOs;
- erros;
- paginação.

Nunca alterar o contrato oficial apenas para facilitar testes.

---

# 47. Anti-patterns

São proibidos.

## Controllers com regra de negócio

```text
Controller

↓

Calcula XP

↓

Persiste Dados
```

---

## Retornar Entities

```text
Entity

↓

JSON
```

---

## SQL dentro do Controller

---

## Autorização no Controller

---

## DTO reutilizado como Entity

---

## Endpoint baseado em verbo

```text
/createWorkout

/updateBook

/deleteHabit
```

---

## Stack Trace na resposta

---

## HTTP 200 para erro

---

## Exposição de IDs internos sem necessidade

---

## Quebra de compatibilidade sem versionamento

Todos esses padrões violam a arquitetura oficial do LifeOS.

---

# 48. ADRs Relacionadas

Mudanças significativas na arquitetura da API deverão gerar uma **Architecture Decision Record (ADR)**.

Exemplos:

- mudança do padrão REST;
- adoção de GraphQL;
- adoção de gRPC;
- alteração do versionamento;
- mudança da estratégia de autenticação;
- alteração da paginação;
- mudança da estratégia de cache.

Cada ADR deverá conter:

- contexto;
- decisão;
- alternativas;
- consequências;
- impacto arquitetural.

---

# 49. Checklist Oficial

Antes da publicação de um endpoint verificar:

- [ ] Endpoint documentado.
- [ ] DTOs definidos.
- [ ] Validação implementada.
- [ ] Use Case reutilizado.
- [ ] Autenticação implementada.
- [ ] Autorização implementada.
- [ ] Ownership validado.
- [ ] Logging implementado.
- [ ] Correlation ID propagado.
- [ ] Auditoria quando necessária.
- [ ] Paginação implementada quando aplicável.
- [ ] Filtros documentados.
- [ ] Testes criados.
- [ ] OpenAPI atualizada.
- [ ] Documentação sincronizada.

Todos os novos endpoints devem cumprir integralmente este checklist.

---

# 50. Definition of Done

Um endpoint da API somente será considerado concluído quando:

- [ ] Contrato definido.
- [ ] Endpoint implementado.
- [ ] Request DTO criado.
- [ ] Response DTO criado.
- [ ] Use Case integrado.
- [ ] Autenticação implementada.
- [ ] Autorização implementada.
- [ ] Logging implementado.
- [ ] Monitoramento preparado.
- [ ] Tratamento de erros padronizado.
- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados.
- [ ] OpenAPI atualizada.
- [ ] Documentação sincronizada.

Nenhum endpoint poderá ser disponibilizado em produção sem atender integralmente aos critérios estabelecidos neste documento.

---

# 51. Integração com Clean Architecture

A camada de API faz parte exclusivamente da **Presentation Layer**.

Fluxo oficial:

```text
HTTP Request

↓

Controller

↓

Request DTO

↓

Use Case

↓

Domain

↓

Repository

↓

Response DTO

↓

HTTP Response
```

Responsabilidades da API:

- receber requisições;
- validar formato;
- autenticar;
- autorizar;
- converter DTOs;
- traduzir erros.

A API nunca deve:

- acessar diretamente o banco;
- manipular Entities;
- executar regras de negócio;
- publicar eventos diretamente;
- controlar transações.

Toda lógica permanece encapsulada nos Use Cases.

---

# 52. Integração com Domain-Driven Design (DDD)

A API representa apenas uma interface para o domínio.

Fluxo:

```text
API

↓

Application

↓

Aggregate

↓

Domain Events
```

O domínio permanece completamente isolado.

A API nunca conhece:

- Entities internas;
- Value Objects;
- Aggregates;
- Repositories;
- ORM.

Ela trabalha apenas com DTOs públicos.

Isso preserva a independência do domínio e evita acoplamento entre contrato HTTP e modelo interno.

---

# 53. Integração com Arquitetura Hexagonal

A API é um **Input Adapter** da Arquitetura Hexagonal.

Fluxo:

```text
HTTP Request

↓

REST Controller

↓

Input Port

↓

Use Case

↓

Output Ports

↓

Infrastructure
```

A API nunca depende diretamente de implementações concretas.

Toda comunicação ocorre através de:

- Use Cases;
- Ports;
- DTOs.

Essa separação permite reutilizar a mesma lógica para:

- Streamlit;
- API REST;
- CLI;
- Background Jobs;
- futuras integrações externas.

---

# 54. Integração com Eventos

Após a conclusão de um Use Case, eventos de domínio podem ser publicados.

Fluxo:

```text
HTTP Request

↓

Use Case

↓

Commit

↓

Publish Domain Events

↓

HTTP Response
```

A API nunca publica eventos diretamente.

Ela apenas inicia a execução do Use Case.

Os Event Handlers permanecem totalmente desacoplados da interface HTTP.

---

# 55. Convenções Oficiais

Toda API deverá seguir convenções consistentes.

### Controllers

```text
WorkoutController

BookController

HabitController

CharacterController

AchievementController
```

### DTOs

```text
CreateWorkoutRequest

WorkoutResponse

UpdateWorkoutRequest

CharacterResponse
```

### Rotas

```text
/api/v1/workouts

/api/v1/books

/api/v1/habits

/api/v1/characters
```

### Métodos

```text
GET

POST

PUT

PATCH

DELETE
```

A nomenclatura deve permanecer previsível em toda a plataforma.

---

# 56. Evolução Futura

A arquitetura da API foi projetada para evoluir sem comprometer os contratos existentes.

Evoluções previstas:

- OAuth 2.1;
- OpenID Connect;
- GraphQL Gateway;
- gRPC interno;
- WebSockets;
- Server-Sent Events (SSE);
- API para Mobile;
- API para Plugins;
- API Pública para terceiros;
- Webhooks;
- SDKs oficiais;
- Versionamento automático;
- OpenAPI Code Generation.

Toda evolução deverá preservar:

- compatibilidade;
- desacoplamento;
- estabilidade dos contratos.

---

# 57. Critérios de Aceite

Uma implementação de API será considerada aderente à arquitetura quando:

- utilizar Controllers finos;
- utilizar Request e Response DTOs;
- reutilizar Use Cases existentes;
- respeitar autenticação;
- respeitar autorização;
- seguir os padrões REST;
- possuir documentação OpenAPI;
- utilizar tratamento padronizado de erros;
- propagar Correlation ID;
- produzir Logging estruturado;
- possuir testes automatizados.

Todos esses critérios são obrigatórios.

---

# 58. Governança da API

Toda alteração na API deve seguir um processo de governança.

Fluxo oficial:

```text
Nova Necessidade

↓

Análise Arquitetural

↓

Definição do Contrato

↓

Revisão Técnica

↓

Implementação

↓

Testes

↓

Atualização da OpenAPI

↓

Publicação
```

Mudanças incompatíveis devem:

- gerar nova versão;
- atualizar documentação;
- comunicar consumidores;
- possuir período de transição.

A governança garante estabilidade para consumidores internos e externos.

---

# 59. Roadmap

A evolução planejada da API inclui:

### Curto Prazo

- API REST v1;
- OpenAPI 3;
- Swagger UI;
- autenticação;
- autorização;
- paginação;
- filtros;
- documentação completa.

### Médio Prazo

- Background Jobs;
- operações assíncronas;
- exportações;
- notificações;
- Webhooks;
- SDK oficial.

### Longo Prazo

- GraphQL;
- gRPC;
- APIs públicas;
- Marketplace;
- Plugins;
- integração com aplicações móveis;
- sincronização em tempo real.

Todas as evoluções devem permanecer compatíveis com os princípios arquiteturais definidos no LifeOS.

---

# 60. Declaração Final

A API do LifeOS constitui a interface oficial de comunicação entre consumidores externos e a plataforma.

Ela foi projetada para ser:

- orientada a recursos;
- consistente;
- segura;
- versionada;
- documentada;
- observável;
- desacoplada;
- extensível;
- independente da tecnologia utilizada.

Toda requisição deve seguir rigorosamente o fluxo arquitetural estabelecido:

```text
HTTP Request

↓

Authentication

↓

Authorization

↓

Validation

↓

Use Case

↓

Domain

↓

Repository

↓

Response DTO

↓

HTTP Response
```

A API nunca deve conter regras de negócio, acessar diretamente a infraestrutura ou expor detalhes internos da aplicação.

Este documento estabelece o padrão oficial para todas as interfaces HTTP do LifeOS, garantindo contratos estáveis, evolução controlada e alinhamento com os princípios de **Clean Architecture**, **DDD**, **Arquitetura Hexagonal**, **Monólito Modular** e **Event-Driven Architecture**, assegurando uma base sólida para o crescimento sustentável da plataforma.
