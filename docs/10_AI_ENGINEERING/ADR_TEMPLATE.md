# ADR_TEMPLATE.md

> Registro oficial das decisões arquiteturais do projeto LifeOS.

Versão: 1.0
Status: Ativo
Responsável: Software Architect
Aplicação: Obrigatória para desenvolvedores humanos e agentes de Inteligência Artificial

---

# 1. Objetivo

Este documento registra as decisões arquiteturais relevantes do LifeOS utilizando o padrão **Architecture Decision Record — ADR**.

Cada ADR documenta:

- o contexto da decisão;
- o problema arquitetural;
- as alternativas avaliadas;
- a decisão adotada;
- as consequências;
- os impactos sobre o sistema;
- as Capabilities afetadas;
- as Features e os Requisitos Funcionais relacionados;
- os documentos e componentes impactados.

Os ADRs fazem parte da fonte oficial de verdade do LifeOS.

Uma decisão registrada não deverá ser alterada silenciosamente.

Caso uma decisão precise ser modificada, um novo ADR deverá ser criado para substituir formalmente o anterior.

---

# 2. Estados de um ADR

| Estado | Significado |
|---|---|
| Proposed | Decisão proposta, ainda não aprovada |
| Accepted | Decisão aprovada e vigente |
| Deprecated | Decisão não recomendada para novas implementações |
| Superseded | Decisão substituída por outro ADR |
| Rejected | Decisão avaliada e rejeitada |

---

# 3. Níveis de impacto

| Impacto | Significado |
|---|---|
| Critical | Afeta toda a plataforma ou o núcleo arquitetural |
| High | Afeta múltiplas Capabilities ou componentes estruturais |
| Medium | Afeta uma Capability ou fluxo relevante |
| Low | Afeta uma decisão localizada e facilmente reversível |

---

# 4. Regras

Todo ADR deverá:

- possuir identificador único;
- possuir título claro;
- registrar a data da decisão;
- registrar seu estado;
- identificar o contexto;
- explicar a decisão;
- documentar consequências positivas e negativas;
- informar se existe Breaking Change;
- informar se exige migration;
- registrar os documentos afetados;
- registrar commits relacionados quando disponíveis.

É proibido:

- apagar ADRs antigos;
- alterar silenciosamente uma decisão aceita;
- reutilizar um identificador;
- modificar o significado histórico de um ADR;
- declarar uma decisão arquitetural sem aprovação.

---

# 5. Índice de Decisões

| ADR | Título | Estado | Impacto |
|---|---|---|---|
| ADR-001 | TSID como identificador oficial | Accepted | High |
| ADR-002 | Clean Architecture como arquitetura obrigatória | Accepted | Critical |
| ADR-003 | Domain-Driven Design como padrão de modelagem | Accepted | Critical |
| ADR-004 | CQRS simples na Application Layer | Accepted | High |
| ADR-005 | Composition Root centralizado | Accepted | High |
| ADR-006 | Shared Kernel restrito a conceitos transversais | Accepted | High |
| ADR-007 | Game Engine como única autoridade de progressão | Accepted | Critical |
| ADR-008 | Character limitado à identidade e perfil persistente | Accepted | Critical |
| ADR-009 | Publicação de eventos após commit bem-sucedido | Accepted | High |

---

# ADR-001 — TSID como identificador oficial

## Estado

Accepted

## Data

2026-08-04

## Impacto

High

## Origem

Revisão arquitetural da Sprint 01.

## Contexto

O LifeOS necessita de identificadores únicos para:

- Users;
- Players;
- Characters;
- sessões;
- eventos;
- entidades das futuras Capabilities.

A documentação inicial mencionava UUID como estratégia de identificação.

Durante a revisão da fundação, foi decidido adotar identificadores temporalmente ordenáveis para melhorar:

- ordenação natural;
- comportamento de índices;
- localidade de inserção;
- rastreabilidade temporal;
- consistência entre todas as Capabilities.

## Problema

UUIDs aleatórios podem provocar maior fragmentação de índices e não oferecem ordenação temporal natural.

O projeto também precisava estabelecer um único padrão de identificação antes da criação das demais Capabilities.

## Alternativas consideradas

### UUID aleatório

Vantagens:

- suporte amplo;
- implementação simples;
- bibliotecas maduras.

Desvantagens:

- ausência de ordenação temporal;
- inserções menos localizadas em índices;
- maior dificuldade para inspeção cronológica.

### Identificador inteiro sequencial

Vantagens:

- simples;
- compacto;
- eficiente para índices.

Desvantagens:

- dependência direta do banco;
- previsibilidade;
- menor autonomia para geração distribuída;
- exposição da quantidade de registros.

### TSID

Vantagens:

- ordenação temporal;
- geração independente do banco;
- eficiência de índices;
- unicidade;
- compatibilidade com arquitetura modular.

Desvantagens:

- necessidade de biblioteca ou implementação específica;
- exigência de padronização de conversão e persistência.

## Decisão

O LifeOS utilizará **TSID — Time-Sorted Unique Identifier** como padrão oficial para identificadores de entidades e Aggregates.

O Shared Kernel será responsável por fornecer:

- geração de TSID;
- representação oficial;
- conversão;
- validação;
- serialização quando necessário.

As Capabilities poderão criar Value Objects específicos:

```text
UserId
PlayerId
CharacterId
SessionId
```

Todos baseados no padrão TSID.

## Consequências positivas

- identificadores temporalmente ordenáveis;
- melhor comportamento em índices;
- geração independente do banco;
- padrão único em toda a plataforma;
- maior facilidade para ordenação cronológica.

## Consequências negativas

- dependência de uma implementação de TSID;
- necessidade de testes de compatibilidade;
- necessidade de conversões explícitas entre domínio, ORM e API.

## Regras derivadas

- novas entidades não poderão utilizar UUID sem novo ADR;
- identificadores não poderão ser gerados diretamente pelo banco;
- identificadores de domínio deverão ser imutáveis;
- ORM Models deverão preservar o valor integral do TSID;
- APIs não deverão expor detalhes internos da biblioteca utilizada.

## Capabilities afetadas

- AUTH
- CHAR
- Todas as futuras Capabilities

## Features afetadas

- AUTH-001
- CHAR-001
- Todas as Features que criem entidades persistentes

## RFs afetados

- RF-AUTH-001
- RF-CHAR-001
- Requisitos futuros que criem entidades

## Migration necessária

Sim, para novas tabelas.

As migrations existentes deverão preservar os identificadores já implementados.

## Breaking Change

Não, considerando o estado inicial do projeto.

## Documentos afetados

- `docs/03_DATABASE/DATABASE.md`
- `docs/02_ARCHITECTURE/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/DEFINITION_OF_DONE.md`

## Código relacionado

```text
app/shared/domain/tsid.py
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-002 — Clean Architecture como arquitetura obrigatória

## Estado

Accepted

## Data

2026-08-04

## Impacto

Critical

## Origem

Definição arquitetural inicial do LifeOS.

## Contexto

O LifeOS será composto por múltiplas Capabilities com regras de negócio independentes.

O projeto precisa permitir que:

- o domínio evolua sem depender de frameworks;
- a persistência possa ser substituída;
- APIs sejam adaptadores;
- testes de domínio sejam rápidos;
- a Game Engine permaneça protegida;
- as Capabilities mantenham fronteiras claras.

## Problema

Uma arquitetura baseada diretamente em frameworks poderia causar:

- domínio dependente do FastAPI;
- regras de negócio acopladas ao SQLAlchemy;
- baixa testabilidade;
- dificuldade de manutenção;
- dependências circulares;
- mistura entre aplicação e infraestrutura.

## Alternativas consideradas

### Arquitetura baseada em framework

Vantagens:

- implementação inicial rápida;
- menor quantidade de abstrações.

Desvantagens:

- alto acoplamento;
- domínio contaminado;
- dificuldade de substituição;
- baixa independência das regras de negócio.

### Arquitetura em camadas tradicional

Vantagens:

- organização conhecida;
- separação parcial das responsabilidades.

Desvantagens:

- risco de dependências apontando para infraestrutura;
- domínio frequentemente anêmico;
- serviços excessivamente acoplados.

### Clean Architecture

Vantagens:

- domínio independente;
- dependências direcionadas para dentro;
- testabilidade;
- substituição de adapters;
- proteção das regras de negócio.

Desvantagens:

- maior disciplina;
- mais contratos;
- maior custo inicial de estruturação.

## Decisão

O LifeOS seguirá obrigatoriamente a **Clean Architecture**.

A organização principal de cada Capability será:

```text
domain/
application/
infrastructure/
presentation/
```

A regra de dependência será:

```text
Presentation
    ↓
Application
    ↓
Domain
```

A Infrastructure implementará Ports definidos pelas camadas internas.

## Regras de dependência

### Domain

Pode depender apenas de:

- linguagem;
- biblioteca padrão;
- Shared Kernel autorizado.

Não pode depender de:

- Application;
- Infrastructure;
- Presentation;
- FastAPI;
- SQLAlchemy;
- Pydantic.

### Application

Pode depender de:

- Domain;
- Ports;
- Shared Application autorizado.

Não pode depender de:

- Infrastructure;
- Presentation;
- FastAPI;
- SQLAlchemy ORM Models.

### Infrastructure

Pode depender das camadas internas para implementar contratos.

### Presentation

Pode depender da Application para executar casos de uso.

Não poderá acessar diretamente:

- banco;
- SQLAlchemy repositories;
- ORM Models.

## Consequências positivas

- isolamento das regras de negócio;
- alta testabilidade;
- possibilidade de substituir frameworks;
- melhor manutenção;
- fronteiras explícitas;
- redução de acoplamento.

## Consequências negativas

- necessidade de mais arquivos;
- necessidade de Ports e Adapters;
- maior rigor durante revisão;
- risco de abstrações excessivas se aplicada sem critério.

## Capabilities afetadas

Todas.

## Features afetadas

Todas.

## RFs afetados

Todos.

## Migration necessária

Não.

## Breaking Change

Não.

## Documentos afetados

- `docs/02_ARCHITECTURE/`
- `GEMINI.md`
- `AGENTS.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/<capability>/domain/
app/<capability>/application/
app/<capability>/infrastructure/
app/<capability>/presentation/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-003 — Domain-Driven Design como padrão de modelagem

## Estado

Accepted

## Data

2026-08-04

## Impacto

Critical

## Origem

Definição arquitetural inicial.

## Contexto

O LifeOS possui domínios complexos, incluindo:

- autenticação;
- identidade do Character;
- saúde;
- treinos;
- hábitos;
- leitura;
- terapia;
- progressão;
- Game Engine;
- Analytics;
- Inteligência Artificial.

Esses conceitos possuem linguagem e regras próprias.

## Problema

Uma modelagem puramente orientada a tabelas ou CRUD poderia gerar:

- entidades anêmicas;
- regras espalhadas;
- baixa expressividade;
- lógica duplicada;
- dificuldade de proteger invariantes;
- dependência da estrutura do banco.

## Alternativas consideradas

### Modelo CRUD anêmico

Vantagens:

- simples para operações básicas;
- menor custo inicial.

Desvantagens:

- regras fora das entidades;
- serviços grandes;
- dificuldade de preservar invariantes;
- baixo alinhamento com o negócio.

### Active Record

Vantagens:

- produtividade inicial;
- persistência integrada ao objeto.

Desvantagens:

- domínio acoplado ao ORM;
- quebra da independência arquitetural;
- baixa separação entre modelo e banco.

### Domain-Driven Design

Vantagens:

- linguagem de negócio explícita;
- Aggregates;
- Entities;
- Value Objects;
- Domain Events;
- invariantes protegidas.

Desvantagens:

- maior complexidade conceitual;
- exige disciplina;
- risco de modelagem excessiva em operações triviais.

## Decisão

O LifeOS utilizará **Domain-Driven Design** como padrão principal de modelagem de negócio.

Serão utilizados quando aplicáveis:

- Bounded Contexts representados pelas Capabilities;
- Aggregates;
- Aggregate Roots;
- Entities;
- Value Objects;
- Domain Events;
- Domain Errors;
- Repository Ports;
- Domain Services.

## Regras derivadas

- regras de negócio deverão residir no domínio;
- Aggregates deverão proteger suas invariantes;
- Value Objects deverão ser imutáveis;
- Domain Errors deverão utilizar linguagem do negócio;
- ORM Models não serão entidades de domínio;
- Persistence Mappers deverão separar domínio e banco;
- conceitos sem comportamento ou necessidade real não deverão ser modelados prematuramente.

## Consequências positivas

- linguagem clara;
- domínio expressivo;
- invariantes protegidas;
- menor duplicação;
- rastreabilidade funcional;
- maior alinhamento com o PRD.

## Consequências negativas

- mais classes e arquivos;
- necessidade de conhecimento de DDD;
- custo de modelagem;
- risco de overengineering se aplicado sem necessidade.

## Capabilities afetadas

Todas as Capabilities com regras de negócio.

## Features afetadas

Todas as Features funcionais.

## RFs afetados

Todos os RFs de domínio.

## Migration necessária

Não diretamente.

## Breaking Change

Não.

## Documentos afetados

- `docs/02_ARCHITECTURE/03_DDD.md`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/<capability>/domain/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-004 — CQRS simples na Application Layer

## Estado

Accepted

## Data

2026-08-04

## Impacto

High

## Origem

Revisão arquitetural da Sprint 01.

## Contexto

O LifeOS possui operações com comportamentos distintos:

- Commands alteram estado;
- Queries recuperam informações;
- consultas não devem carregar Aggregates desnecessariamente;
- fluxos de escrita precisam respeitar Unit of Work;
- APIs de leitura podem utilizar DTOs específicos.

## Problema

Misturar leitura e escrita no mesmo serviço poderia provocar:

- classes com múltiplas responsabilidades;
- consultas dependentes de Aggregates completos;
- dificuldade de otimização;
- contratos pouco claros;
- risco de Queries alterarem estado.

## Alternativas consideradas

### Application Services genéricos

Vantagens:

- menos classes;
- implementação simples.

Desvantagens:

- responsabilidades misturadas;
- tendência a serviços grandes;
- rastreabilidade reduzida.

### CQRS com buses e infraestrutura completa

Vantagens:

- alto desacoplamento;
- extensibilidade;
- pipelines.

Desvantagens:

- complexidade prematura;
- excesso de abstrações;
- menor clareza no estágio atual.

### CQRS simples

Vantagens:

- Commands e Queries explícitos;
- separação de responsabilidades;
- estrutura simples;
- possibilidade de evolução futura.

Desvantagens:

- maior quantidade de handlers;
- necessidade de disciplina de nomenclatura.

## Decisão

O LifeOS adotará **CQRS simples** na Application Layer.

A estrutura poderá conter:

```text
application/
├── commands/
├── queries/
└── dtos/
```

Cada arquivo poderá conter:

- Command ou Query;
- Handler correspondente;
- contratos específicos.

Não será criado inicialmente:

- Command Bus genérico;
- Query Bus genérico;
- pipeline complexo;
- mediador externo sem necessidade comprovada.

## Regras derivadas

### Commands

- podem alterar estado;
- devem utilizar Unit of Work quando transacionais;
- podem gerar Domain Events;
- não retornam ORM Models.

### Queries

- são somente leitura;
- não alteram estado;
- não publicam eventos;
- retornam DTOs;
- podem utilizar modelos de leitura otimizados.

## Consequências positivas

- responsabilidade explícita;
- melhor testabilidade;
- consultas independentes;
- facilidade de evolução;
- rastreabilidade por caso de uso.

## Consequências negativas

- maior quantidade de arquivos;
- possível duplicação de estruturas simples;
- risco de aplicação mecânica em operações triviais.

## Capabilities afetadas

Todas as Capabilities com casos de uso.

## Features afetadas

Features de leitura e escrita.

## RFs afetados

Todos os RFs executados pela Application Layer.

## Migration necessária

Não.

## Breaking Change

Não.

## Documentos afetados

- `docs/02_ARCHITECTURE/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/<capability>/application/commands/
app/<capability>/application/queries/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-005 — Composition Root centralizado

## Estado

Accepted

## Data

2026-08-04

## Impacto

High

## Origem

Revisão arquitetural da Sprint 01.

## Contexto

O LifeOS utiliza:

- Repository Ports;
- Unit of Work;
- Event Bus;
- PasswordHasher;
- adapters externos;
- handlers;
- dependências de infraestrutura.

Esses componentes precisam ser conectados sem contaminar Domain e Application com implementações concretas.

## Problema

Instanciar dependências diretamente dentro de handlers ou endpoints provocaria:

- alto acoplamento;
- dificuldade de testes;
- duplicação;
- dependência de infraestrutura;
- configuração espalhada.

## Alternativas consideradas

### Instanciação direta

Vantagens:

- simples;
- menos configuração inicial.

Desvantagens:

- acoplamento;
- dificuldade de substituição;
- baixa testabilidade.

### Container de injeção de dependências externo

Vantagens:

- automação;
- resolução dinâmica;
- recursos avançados.

Desvantagens:

- dependência adicional;
- maior complexidade;
- comportamento implícito.

### Composition Root explícito

Vantagens:

- wiring visível;
- controle;
- baixa dependência;
- fácil inspeção;
- testabilidade.

Desvantagens:

- configuração manual;
- possível crescimento do arquivo principal.

## Decisão

O LifeOS utilizará um **Composition Root centralizado e explícito**.

A montagem principal ocorrerá em:

```text
app/main.py
```

ou em factories invocadas por ele:

```text
app/app_factory.py
app/<capability>/dependencies.py
```

## Responsabilidades

O Composition Root poderá:

- criar engine e sessions;
- instanciar repositories;
- criar Unit of Work;
- configurar Event Bus;
- registrar handlers;
- injetar adapters;
- montar routers;
- criar a aplicação FastAPI.

Não poderá:

- conter regras de negócio;
- executar lógica de domínio;
- substituir handlers;
- acessar dados diretamente.

## Consequências positivas

- dependências explícitas;
- testabilidade;
- facilidade de substituição;
- baixa dependência de frameworks de DI;
- melhor rastreabilidade.

## Consequências negativas

- configuração manual;
- risco de arquivo excessivamente grande;
- necessidade de modularização por Capability.

## Capabilities afetadas

Todas.

## Features afetadas

Todas as Features que dependam de infraestrutura.

## RFs afetados

Todos os casos de uso integrados.

## Migration necessária

Não.

## Breaking Change

Não.

## Documentos afetados

- `docs/02_ARCHITECTURE/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/main.py
app/app_factory.py
app/<capability>/dependencies.py
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-006 — Shared Kernel restrito a conceitos transversais

## Estado

Accepted

## Data

2026-08-04

## Impacto

High

## Origem

Revisão arquitetural das Sprints 01 e 02.

## Contexto

Múltiplas Capabilities precisam compartilhar alguns conceitos fundamentais:

- AggregateRoot;
- DomainEvent;
- DomainError;
- ValueObject;
- TSID;
- UserId transversal;
- Unit of Work;
- Event Bus;
- Clock futuro.

Ao mesmo tempo, um diretório compartilhado excessivo pode se tornar um acoplamento central.

## Problema

Sem Shared Kernel, conceitos básicos seriam duplicados.

Com um Shared Kernel sem limites, regras específicas de Capabilities poderiam ser movidas para um diretório genérico, destruindo as fronteiras do sistema.

## Alternativas consideradas

### Duplicação por Capability

Vantagens:

- independência máxima;
- sem dependência compartilhada.

Desvantagens:

- código duplicado;
- comportamentos inconsistentes;
- manutenção repetitiva.

### Shared genérico

Vantagens:

- reutilização simples;
- menos arquivos duplicados.

Desvantagens:

- acoplamento;
- ownership indefinido;
- risco de se tornar depósito de código.

### Shared Kernel restrito

Vantagens:

- compartilhamento controlado;
- conceitos fundamentais únicos;
- menor duplicação;
- fronteiras preservadas.

Desvantagens:

- exige revisão arquitetural;
- mudanças podem afetar várias Capabilities.

## Decisão

O LifeOS utilizará um **Shared Kernel pequeno e controlado**.

Estrutura base:

```text
app/shared/
├── domain/
├── application/
└── infrastructure/
```

## Permitido no Shared Kernel

- abstrações fundamentais;
- identificadores realmente transversais;
- tipos técnicos padronizados;
- contratos utilizados por múltiplas Capabilities;
- infraestrutura transversal aprovada.

## Proibido no Shared Kernel

- regras específicas de AUTH;
- regras específicas de CHAR;
- regras da Game Engine;
- DTOs de uma única Capability;
- repositories específicos;
- Models ORM específicos;
- utilitários sem ownership;
- código movido apenas para evitar pensar sobre fronteiras.

## Critérios para inclusão

Um componente somente poderá entrar no Shared Kernel quando:

- for utilizado por múltiplas Capabilities;
- representar conceito transversal;
- não possuir ownership exclusivo;
- sua inclusão for aprovada arquiteturalmente;
- houver testes de regressão.

## Consequências positivas

- redução de duplicação;
- padronização;
- tipos transversais consistentes;
- menor acoplamento entre Capabilities.

## Consequências negativas

- impacto amplo em alterações;
- necessidade de governança;
- risco de crescimento indevido.

## Capabilities afetadas

Todas.

## Features afetadas

Todas as Features que utilizem conceitos compartilhados.

## RFs afetados

Indiretamente todos.

## Migration necessária

Não diretamente.

## Breaking Change

Pode ser, dependendo da alteração.

## Documentos afetados

- `docs/02_ARCHITECTURE/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/shared/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-007 — Game Engine como única autoridade de progressão

## Estado

Accepted

## Data

2026-08-04

## Impacto

Critical

## Origem

Product Vision, Capability Map e revisão documental da Sprint 02.

## Contexto

O LifeOS transforma atividades reais em progressão gamificada.

Diversas Capabilities produzem informações:

- HEALTH;
- WORKOUT;
- READING;
- THERAPY;
- HABITS.

Essas atividades podem influenciar:

- XP;
- Level;
- Attributes;
- Skills;
- Classes;
- Quests;
- Rewards;
- Progression;
- Balanceamento.

## Problema

Se cada Capability calcular sua própria progressão, o sistema teria:

- regras duplicadas;
- inconsistência;
- acoplamento;
- dificuldade de balanceamento;
- resultados imprevisíveis;
- impossibilidade de auditoria central.

## Alternativas consideradas

### Cada Capability calcula sua evolução

Vantagens:

- autonomia local;
- implementação direta.

Desvantagens:

- regras duplicadas;
- evolução inconsistente;
- alto acoplamento;
- balanceamento impossível.

### Character calcula sua própria evolução

Vantagens:

- estado e comportamento centralizados.

Desvantagens:

- Aggregate excessivamente grande;
- mistura identidade e Game Engine;
- acoplamento com todas as Capabilities.

### Game Engine centraliza progressão

Vantagens:

- única fonte de verdade;
- regras auditáveis;
- balanceamento central;
- evolução determinística;
- separação de responsabilidades.

Desvantagens:

- maior importância do módulo GAME;
- necessidade de eventos e integração;
- complexidade concentrada.

## Decisão

A Capability **GAME** será a única autoridade responsável por:

- conceder XP;
- calcular XP;
- calcular Level;
- alterar Level;
- evoluir Attributes;
- gerenciar Skills;
- gerenciar Classes;
- gerenciar Progression;
- conceder Rewards;
- processar Quests;
- gerenciar balanceamento.

As demais Capabilities apenas:

- registram dados;
- validam seu próprio domínio;
- publicam eventos oficiais.

## Fluxo oficial

```text
Capability de origem
↓
Domain Event
↓
Game Engine
↓
Validação das regras
↓
Atualização da progressão
↓
Persistência
↓
Novos eventos
```

## Regras derivadas

- WORKOUT não concede XP;
- HEALTH não altera atributos;
- READING não aumenta Level;
- HABITS não concede Rewards diretamente;
- CHAR não calcula progressão;
- Dashboard apenas consulta;
- Analytics apenas interpreta;
- AI apenas recomenda.

## Consequências positivas

- consistência;
- balanceamento central;
- auditabilidade;
- regras únicas;
- separação clara.

## Consequências negativas

- GAME será uma Capability complexa;
- eventos deverão ser bem definidos;
- indisponibilidade da Game Engine poderá atrasar processamento;
- testes de balanceamento serão críticos.

## Capabilities afetadas

- GAME
- CHAR
- HEALTH
- WORKOUT
- READING
- THERAPY
- HABITS
- DASH
- ANLT
- AI
- REPORT

## Features afetadas

- GAME-001
- GAME-002
- todas as Features de progressão

## RFs afetados

- RF-GAME-001 a RF-GAME-070
- RF-CHAR relacionados à consulta
- RFs produtores de eventos

## Migration necessária

Futuramente, para persistência da Game Engine.

## Breaking Change

Sim, caso outra Capability já implemente progressão.

## Documentos afetados

- `docs/01_PRODUCT/CAPABILITY_MAP.md`
- `docs/01_PRODUCT/FEATURE_CATALOG.md`
- `docs/01_PRODUCT/PRD.md`
- `docs/02_ARCHITECTURE/`
- `GEMINI.md`

## Código relacionado

```text
app/game/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-008 — Character limitado à identidade e ao perfil persistente

## Estado

Accepted

## Data

2026-08-04

## Impacto

Critical

## Origem

Revisão arquitetural e documental da Sprint 02.

## Contexto

A Capability CHAR inicialmente possuía referências a:

- XP;
- Level;
- Attributes;
- Skills;
- Classes;
- Títulos;
- Guildas;
- evolução.

Esses conceitos conflitam com o ownership da Game Engine.

A Sprint 02 precisava definir claramente o limite de Character.

## Problema

Permitir que Character gerencie identidade e progressão produziria:

- Aggregate excessivamente grande;
- sobreposição com GAME;
- regras duplicadas;
- dependência das demais Capabilities;
- dificuldade de evolução modular.

## Alternativas consideradas

### Character completo com progressão

Vantagens:

- visão centralizada;
- menos consultas entre módulos.

Desvantagens:

- domínio excessivamente grande;
- sobreposição com GAME;
- acoplamento elevado.

### Character como projeção de GAME

Vantagens:

- leitura simplificada.

Desvantagens:

- perda de autonomia da identidade;
- criação dependente da Game Engine;
- mistura de ownership.

### Character como identidade e perfil persistente

Vantagens:

- responsabilidade clara;
- domínio pequeno;
- separação de progressão;
- criação independente;
- consultas simples.

Desvantagens:

- telas completas precisarão agregar dados de GAME;
- consultas poderão exigir composição entre Capabilities.

## Decisão

A Capability **CHAR** será responsável exclusivamente por:

- Player;
- identidade do Character;
- vínculo User → Player → Character;
- perfil persistente;
- representação básica;
- consultas de identidade e perfil;
- eventos de criação.

CHAR não será responsável por:

- XP;
- Level;
- atributos evolutivos;
- Skills;
- Classes;
- Quests;
- Rewards;
- Progression;
- evolução;
- balanceamento.

## Estado atual autorizado

```text
User
↓
Player
↓
Character
```

Relacionamentos:

- um User possui exatamente um Player;
- um Player possui exatamente um Character.

## APIs autorizadas na Sprint 02

```text
GET /character
GET /character/profile
```

Não existem, sem RF específico:

```text
PUT /character
PATCH /character
PATCH /character/profile
```

## Consequências positivas

- fronteira clara;
- Aggregate simples;
- menor acoplamento;
- progressão protegida;
- consultas seguras.

## Consequências negativas

- composição necessária para telas gamificadas;
- informações de GAME não estarão diretamente no Aggregate Character;
- perfil editável exigirá Feature e RF futuros.

## Capabilities afetadas

- CHAR
- AUTH
- GAME
- DASH
- REPORT

## Features afetadas

- CHAR-001
- CHAR-002
- CHAR-003
- CHAR-004
- GAME-001
- GAME-002

## RFs afetados

- RF-CHAR-001
- RF-CHAR-002
- RF-CHAR-003
- RF-CHAR-004
- RF-GAME-006
- RF-GAME-007

## Migration necessária

Não para a decisão base.

## Breaking Change

Não no estado atual.

## Documentos afetados

- `docs/01_PRODUCT/CAPABILITY_MAP.md`
- `docs/01_PRODUCT/FEATURE_CATALOG.md`
- `docs/01_PRODUCT/PRD.md`
- `NEXT_TASK.md`

## Código relacionado

```text
app/character/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-009 — Publicação de eventos após commit bem-sucedido

## Estado

Accepted

## Data

2026-08-04

## Impacto

High

## Origem

Revisão arquitetural da Sprint 01.

## Contexto

Aggregates do LifeOS geram Domain Events para comunicar fatos relevantes.

Exemplos:

- UserRegistered;
- PlayerCreated;
- CharacterCreated;
- eventos futuros de saúde e treino.

A publicação precisa respeitar o estado persistido.

## Problema

Publicar um evento antes do commit pode comunicar um fato que será revertido.

Publicar após o commit usando Event Bus em memória pode perder o evento caso a aplicação falhe entre o commit e o dispatch.

## Alternativas consideradas

### Publicar antes do commit

Vantagens:

- handlers executados dentro do fluxo;
- possibilidade de rollback conjunto em memória.

Desvantagens:

- consumidores podem observar estado não persistido;
- evento pode representar fato revertido;
- integrações externas não participam da transação.

### Publicar após commit com Event Bus em memória

Vantagens:

- evento representa estado persistido;
- implementação simples;
- adequada à fase inicial.

Desvantagens:

- garantia `at-most-once`;
- possível perda após o commit;
- sem persistência do evento.

### Outbox Pattern

Vantagens:

- consistência entre banco e evento;
- entrega recuperável;
- suporte a `at-least-once`.

Desvantagens:

- maior complexidade;
- tabela adicional;
- worker;
- idempotência obrigatória.

## Decisão

Na fase inicial, os Domain Events serão:

1. gerados pelos Aggregates;
2. armazenados internamente;
3. coletados pelo Unit of Work;
4. publicados somente após commit bem-sucedido;
5. despachados pelo Event Bus em memória.

## Ordem oficial

```text
Command Handler
↓
Alteração dos Aggregates
↓
Repository save
↓
Unit of Work commit
↓
Coleta dos Domain Events
↓
Event Bus dispatch
↓
Event Handlers
```

## Limitação aceita

O Event Bus em memória oferece, inicialmente, semântica aproximada de:

```text
at-most-once
```

Uma falha entre commit e publicação poderá causar perda do evento.

Essa limitação é aceita apenas enquanto os eventos não forem críticos para garantir pós-condições obrigatórias.

## Regra crítica

Eventos não poderão ser utilizados para garantir uma pós-condição atômica obrigatória.

Exemplo:

A criação de User, Player e Character não poderá depender de:

```text
commit do User
↓
UserRegistered
↓
criação posterior de Player e Character
```

Quando as três entidades forem obrigatórias, deverão participar da mesma transação.

## Quando adotar Outbox

Um novo ADR deverá avaliar Outbox quando existir:

- mensageria externa;
- eventos críticos;
- integração entre serviços;
- necessidade de retry;
- garantia `at-least-once`;
- recuperação de eventos perdidos.

## Consequências positivas

- eventos representam fatos persistidos;
- fluxo simples;
- desacoplamento;
- compatibilidade com futura mensageria.

## Consequências negativas

- possibilidade de perda;
- ausência de retry;
- handlers síncronos;
- necessidade futura de evolução.

## Capabilities afetadas

Todas as produtoras ou consumidoras de eventos.

## Features afetadas

Features orientadas a eventos.

## RFs afetados

- RF-AUTH-001
- RF-CHAR-001
- requisitos futuros produtores de eventos

## Migration necessária

Não na implementação em memória.

Será necessária para Outbox futura.

## Breaking Change

Não.

## Documentos afetados

- `docs/02_ARCHITECTURE/08_EVENTS.md`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/shared/application/event_bus.py
app/shared/infrastructure/event_bus.py
app/shared/application/unit_of_work.py
app/shared/infrastructure/unit_of_work.py
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# Próximos ADRs previstos

Os próximos registros deverão contemplar:

| ADR | Título previsto |
|---|---|
| ADR-010 | Unit of Work como autoridade transacional |
| ADR-011 | Criação atômica de User, Player e Character |
| ADR-012 | Proibição de dependências entre internals de Capabilities |
| ADR-013 | UserId como identidade transversal no Shared Kernel |
| ADR-014 | FastAPI como adapter HTTP inicial |
| ADR-015 | SQLAlchemy e Alembic como persistência inicial |

---

# ADR-010 — Unit of Work como autoridade transacional

## Estado

Accepted

## Data

2026-08-04

## Impacto

Critical

## Origem

Revisão arquitetural da Sprint 01.

## Contexto

Os casos de uso do LifeOS podem envolver múltiplas operações persistentes dentro de uma única ação de negócio.

Exemplos:

- criação de User, Player e Character;
- criação de sessão autenticada;
- atualização de Aggregate e persistência de eventos;
- operações futuras envolvendo Game Engine;
- alterações coordenadas entre múltiplos Repositories.

Essas operações precisam ser executadas de forma atômica.

## Problema

Permitir que cada Repository controle sua própria transação pode causar:

- commits parciais;
- estado inconsistente;
- impossibilidade de rollback completo;
- múltiplas sessões na mesma operação;
- publicação de eventos antes da conclusão da persistência;
- dificuldade de testar atomicidade.

## Alternativas consideradas

### Commit dentro de cada Repository

Vantagens:

- implementação simples;
- Repository aparentemente autônomo.

Desvantagens:

- ausência de atomicidade entre Repositories;
- commits parciais;
- transações fragmentadas;
- impossibilidade de coordenar múltiplos Aggregates.

### Controle transacional no endpoint

Vantagens:

- fluxo visível;
- menor quantidade de abstrações.

Desvantagens:

- Presentation conhece persistência;
- violação da Clean Architecture;
- duplicação de controle transacional;
- baixa testabilidade.

### Unit of Work

Vantagens:

- transação coordenada;
- múltiplos Repositories compartilhando sessão;
- commit e rollback centralizados;
- integração com Domain Events;
- melhor testabilidade.

Desvantagens:

- abstração adicional;
- necessidade de disciplina;
- maior cuidado com o ciclo de vida da sessão.

## Decisão

O LifeOS utilizará o padrão **Unit of Work** como autoridade transacional da Application Layer.

Toda operação que altere estado deverá utilizar uma única instância de Unit of Work por caso de uso transacional.

## Responsabilidades

O Unit of Work deverá:

- controlar o início e o encerramento da transação;
- fornecer ou coordenar Repositories ligados à mesma sessão;
- executar commit;
- executar rollback em caso de falha;
- coletar Domain Events dos Aggregates processados;
- despachar eventos no momento definido pelo ADR-009;
- liberar recursos ao final da operação.

## Regras derivadas

- Repositories não poderão executar `commit()`;
- Repositories não poderão criar sessões independentes dentro da mesma operação;
- o Command Handler deverá controlar o ciclo transacional;
- falhas intermediárias deverão provocar rollback integral;
- consultas somente leitura não deverão abrir transações de escrita sem necessidade;
- eventos não poderão ser despachados antes do commit bem-sucedido;
- uma instância de Unit of Work não deverá ser reutilizada entre requisições distintas.

## Fluxo oficial

```text
Command Handler
↓
Abrir Unit of Work
↓
Executar regras de aplicação e domínio
↓
Persistir Aggregates
↓
Commit
↓
Publicar eventos
↓
Encerrar Unit of Work
```

Em caso de erro:

```text
Erro
↓
Rollback
↓
Descartar eventos não publicados
↓
Propagar erro apropriado
```

## Consequências positivas

- atomicidade;
- consistência;
- rollback centralizado;
- menor acoplamento;
- melhor suporte a múltiplos Repositories;
- integração controlada com eventos.

## Consequências negativas

- maior complexidade estrutural;
- necessidade de garantir sessão compartilhada;
- risco de transações longas;
- necessidade de testes específicos.

## Capabilities afetadas

Todas as Capabilities com operações de escrita.

## Features afetadas

Todas as Features transacionais.

## RFs afetados

- RF-AUTH-001
- RF-AUTH-002
- RF-AUTH-003
- RF-AUTH-004
- RF-AUTH-005
- RF-CHAR-001
- requisitos futuros de escrita

## Migration necessária

Não.

## Breaking Change

Sim, caso algum Repository controle commit diretamente.

## Documentos afetados

- `docs/02_ARCHITECTURE/`
- `docs/03_DATABASE/TRANSACTIONS.md`
- `docs/03_DATABASE/UNIT_OF_WORK.md`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/shared/application/unit_of_work.py
app/shared/infrastructure/unit_of_work.py
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-011 — Criação atômica de User, Player e Character

## Estado

Accepted

## Data

2026-08-04

## Impacto

Critical

## Origem

Revisão bloqueante do planejamento da Sprint 01.

## Contexto

O RF-AUTH-001 define que o cadastro inicial deverá resultar em:

- User criado;
- Player criado;
- Character criado.

As três pós-condições fazem parte de um único fluxo funcional.

Inicialmente foi considerada a criação do User seguida da publicação de um evento para criação posterior de Player e Character.

## Problema

O fluxo orientado exclusivamente a evento permitiria:

```text
User criado
Player ausente
Character ausente
```

caso o commit do User fosse concluído e o Event Handler falhasse.

Como o Event Bus inicial possui semântica `at-most-once`, ele não poderia garantir as pós-condições obrigatórias do cadastro.

## Alternativas consideradas

### Criar User e publicar evento

Vantagens:

- baixo acoplamento;
- fluxo simples;
- comunicação orientada a eventos.

Desvantagens:

- falta de atomicidade;
- possibilidade de cadastro parcial;
- evento pode ser perdido;
- RF-AUTH-001 poderia terminar incompleto.

### Criar as entidades em transações separadas

Vantagens:

- menor coordenação;
- autonomia dos módulos.

Desvantagens:

- estado parcial;
- necessidade de compensação;
- maior complexidade;
- difícil recuperação.

### Criar User, Player e Character na mesma transação

Vantagens:

- atomicidade;
- atendimento integral ao requisito;
- rollback completo;
- estado sempre consistente.

Desvantagens:

- necessidade de orquestração entre Capabilities;
- maior coordenação na Application Layer;
- dependência de contratos públicos.

## Decisão

A criação inicial de:

```text
User
Player
Character
```

deverá ocorrer em uma única transação controlada pelo Unit of Work.

O cadastro somente será considerado concluído quando as três entidades estiverem persistidas.

## Fluxo oficial

```text
RegisterUserCommandHandler
↓
Validar e-mail
↓
Gerar HashedPassword
↓
Criar User
↓
Criar Player
↓
Criar Character
↓
Persistir os três
↓
Commit único
↓
Publicar eventos
↓
Retornar sucesso
```

## Integração entre Capabilities

AUTH não deverá implementar regras internas de CHAR.

A orquestração deverá utilizar:

- Port público;
- factory;
- contrato estável;
- Repositories coordenados pelo mesmo Unit of Work.

As regras de criação de Player e Character permanecem pertencentes a CHAR.

## Eventos

Eventos como:

- UserRegistered;
- PlayerCreated;
- CharacterCreated;

somente poderão representar fatos persistidos com sucesso.

O evento `UserRegistered` não será utilizado para garantir a criação de Player e Character.

## Regras derivadas

- falha na criação do Player deverá reverter User;
- falha na criação do Character deverá reverter User e Player;
- falha no commit deverá impedir publicação de eventos;
- o endpoint não poderá retornar `201 Created` com cadastro parcial;
- repetição do fluxo deverá respeitar idempotência e constraints únicas;
- relacionamentos 1:1 deverão ser protegidos pelo domínio e pelo banco.

## Consequências positivas

- consistência;
- cumprimento integral do RF;
- rollback completo;
- menor necessidade de compensação;
- previsibilidade do estado inicial.

## Consequências negativas

- maior acoplamento de orquestração;
- transação envolvendo mais de uma Capability;
- necessidade de Ports e contratos bem definidos;
- futura separação em serviços exigirá padrão diferente, como Saga.

## Capabilities afetadas

- AUTH
- CHAR
- SHARED

## Features afetadas

- AUTH-001
- CHAR-001

## RFs afetados

- RF-AUTH-001
- RF-CHAR-001

## Migration necessária

Sim, para as tabelas iniciais.

As migrations já existentes deverão ser preservadas.

## Breaking Change

Sim, caso o fluxo anterior criasse somente User.

## Documentos afetados

- `docs/01_PRODUCT/PRD.md`
- `docs/01_PRODUCT/CAPABILITY_MAP.md`
- `docs/02_ARCHITECTURE/`
- `docs/03_DATABASE/DATABASE.md`
- `NEXT_TASK.md`

## Código relacionado

```text
app/auth/application/commands/register_user.py
app/auth/application/ports/character_factory.py
app/character/application/factories/character_factory.py
app/shared/application/unit_of_work.py
```

## Commits relacionados

A registrar.

## Supersedes

A proposta inicial de criação reativa de Player e Character após `UserRegistered`.

---

# ADR-012 — Proibição de dependências entre internals de Capabilities

## Estado

Accepted

## Data

2026-08-05

## Impacto

Critical

## Origem

Revisão arquitetural da Sprint 02.

## Contexto

O LifeOS é organizado como Monólito Modular, no qual cada Capability representa uma fronteira funcional e arquitetural.

Durante a revisão da Sprint 02, foi identificado que:

```text
app.character.domain
```

importava diretamente:

```text
app.auth.domain
```

para utilizar `UserId`.

Esse tipo de dependência cria acoplamento entre os internals de duas Capabilities.

## Problema

Permitir imports diretos entre internals pode causar:

- dependências circulares;
- perda de autonomia;
- mudanças em cascata;
- fronteiras frágeis;
- dificuldade de futura extração;
- compartilhamento indevido de regras;
- domínio contaminado por decisões externas.

## Alternativas consideradas

### Permitir imports diretos entre domínios

Vantagens:

- reutilização simples;
- menor número de contratos.

Desvantagens:

- acoplamento forte;
- fronteiras enfraquecidas;
- dependências não controladas.

### Duplicar conceitos em cada Capability

Vantagens:

- independência total;
- nenhuma dependência direta.

Desvantagens:

- duplicação;
- possíveis incompatibilidades;
- conversões frequentes.

### Utilizar Shared Kernel ou contratos públicos

Vantagens:

- dependência explícita;
- conceitos transversais compartilhados;
- fronteiras preservadas;
- maior facilidade de evolução.

Desvantagens:

- necessidade de governança;
- mais contratos;
- Shared Kernel precisa permanecer pequeno.

## Decisão

É proibido que uma Capability importe diretamente os internals de outra Capability.

Exemplos proibidos:

```text
app.character.domain
→ app.auth.domain
```

```text
app.workout.application
→ app.game.infrastructure
```

```text
app.health.domain
→ app.character.domain
```

## Formas permitidas de integração

### Shared Kernel

Para conceitos realmente transversais:

```text
app.character.domain
→ app.shared.domain
```

### Contratos públicos

Quando uma Capability expõe um contrato estável:

```text
app.auth.application
→ contrato público de CHAR
```

### Domain Events

Para comunicação desacoplada entre fatos ocorridos.

### APIs ou mensageria

Em futuras separações físicas.

## Regras derivadas

- internals não são APIs públicas;
- estruturas internas poderão mudar sem compatibilidade externa;
- nenhuma Capability poderá acessar ORM Models de outra;
- nenhuma Capability poderá acessar Repository concreto de outra;
- nenhuma Capability poderá alterar diretamente tabelas pertencentes a outra;
- contratos compartilhados deverão possuir ownership claro;
- testes arquiteturais deverão validar essas regras.

## Exceções

Uma exceção somente poderá ser criada por novo ADR.

A exceção deverá informar:

- motivo;
- duração;
- Capabilities afetadas;
- plano de remoção;
- riscos.

## Testes arquiteturais obrigatórios

Deverão existir testes que impeçam:

```text
app.<capability>.domain
→ app.<outra-capability>.domain
```

e dependências semelhantes entre camadas internas.

## Consequências positivas

- baixo acoplamento;
- modularidade;
- maior autonomia;
- melhor testabilidade;
- preparação para futura distribuição;
- redução de dependências circulares.

## Consequências negativas

- necessidade de Ports;
- possível duplicação controlada;
- mais esforço de integração;
- necessidade de revisão do Shared Kernel.

## Capabilities afetadas

Todas.

## Features afetadas

Todas as Features que envolvam integração entre Capabilities.

## RFs afetados

Todos os RFs transversais.

## Migration necessária

Não.

## Breaking Change

Pode ser, quando código existente depender diretamente de outra Capability.

## Documentos afetados

- `docs/01_PRODUCT/CAPABILITY_MAP.md`
- `docs/02_ARCHITECTURE/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/
tests/architecture/test_dependency_rules.py
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-013 — UserId como identidade transversal no Shared Kernel

## Estado

Accepted

## Data

2026-08-05

## Impacto

High

## Origem

Revisão arquitetural da Sprint 02.

## Contexto

Diversas Capabilities precisam referenciar o usuário autenticado.

Exemplos:

- AUTH cria e autentica o User;
- CHAR vincula Player ao User;
- HEALTH armazenará registros do usuário;
- WORKOUT registrará treinos;
- READING associará leituras;
- THERAPY e HABITS precisarão de ownership;
- consultas deverão aplicar isolamento.

Inicialmente, `UserId` foi definido dentro do domínio AUTH.

## Problema

Quando CHAR importou `UserId` diretamente de AUTH, foi criada uma dependência proibida:

```text
CHAR Domain
→ AUTH Domain
```

Ao mesmo tempo, duplicar um identificador incompatível em cada Capability poderia causar conversões e inconsistências.

## Alternativas consideradas

### Manter UserId em AUTH

Vantagens:

- ownership aparentemente claro;
- implementação já existente.

Desvantagens:

- outras Capabilities dependem de AUTH internals;
- viola ADR-012;
- acoplamento transversal.

### Criar identificadores diferentes em cada Capability

Exemplos:

```text
OwnerUserId
HealthUserId
WorkoutUserId
```

Vantagens:

- independência;
- nenhuma dependência direta.

Desvantagens:

- duplicação;
- conversões;
- possível inconsistência semântica;
- maior complexidade para identidade autenticada comum.

### Mover UserId para Shared Kernel

Vantagens:

- identidade única;
- dependência transversal autorizada;
- menor duplicação;
- integração simplificada;
- isolamento consistente.

Desvantagens:

- Shared Kernel ganha conceito de negócio transversal;
- alterações impactam múltiplas Capabilities;
- exige governança.

## Decisão

`UserId` será uma identidade transversal oficial localizada em:

```text
app/shared/domain/identifiers/user_id.py
```

AUTH e as demais Capabilities utilizarão o mesmo Value Object compartilhado.

## Responsabilidades

O `UserId` deverá:

- encapsular TSID;
- ser imutável;
- validar sua representação;
- fornecer igualdade por valor;
- permitir conversão segura para persistência e API;
- não conter regras específicas de AUTH.

## Regras derivadas

- nenhuma Capability deverá definir outro `UserId` concorrente;
- `UserId` não representará credenciais;
- AUTH continuará sendo owner da conta de usuário;
- Shared Kernel será owner apenas da representação transversal da identidade;
- mudanças no contrato exigirão revisão ampla;
- ORM Models persistirão o valor TSID, não o objeto diretamente.

## Consequências positivas

- remoção da dependência CHAR → AUTH;
- identidade consistente;
- isolamento multi-tenant padronizado;
- menor duplicação;
- integração futura simplificada.

## Consequências negativas

- impacto amplo em mudanças;
- aumento da responsabilidade do Shared Kernel;
- necessidade de testes de regressão em várias Capabilities.

## Capabilities afetadas

- AUTH
- CHAR
- HEALTH
- WORKOUT
- READING
- THERAPY
- HABITS
- GAME
- DASH
- ANLT
- AI
- REPORT
- ADMIN

## Features afetadas

Todas as Features associadas a dados de usuário.

## RFs afetados

- RF-AUTH-001
- RF-CHAR-001
- RF-CHAR-002
- RF-CHAR-003
- RF-CHAR-004
- requisitos futuros autenticados

## Migration necessária

Não.

O valor persistido permanece inalterado.

## Breaking Change

Somente no código interno.

## Documentos afetados

- `docs/02_ARCHITECTURE/`
- `docs/03_DATABASE/DATABASE.md`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/shared/domain/identifiers/user_id.py
app/auth/
app/character/
```

## Commits relacionados

A registrar.

## Supersedes

O ownership anterior de `UserId` dentro dos internals de AUTH.

---

# ADR-014 — FastAPI como adapter HTTP inicial

## Estado

Accepted

## Data

2026-08-04

## Impacto

Medium

## Origem

Definição técnica da Sprint 01.

## Contexto

O LifeOS necessita de uma interface HTTP para:

- autenticação;
- consultas do Character;
- futuras APIs das Capabilities;
- documentação OpenAPI;
- integração com interfaces gráficas.

A arquitetura exige que o framework HTTP permaneça fora do domínio e da aplicação.

## Problema

Era necessário selecionar um framework que permitisse:

- APIs REST;
- validação de schemas;
- documentação automática;
- injeção de dependências;
- testes;
- execução assíncrona quando aplicável;
- integração simples com Python.

## Alternativas consideradas

### Flask

Vantagens:

- simples;
- maduro;
- flexível.

Desvantagens:

- maior configuração manual;
- validação e OpenAPI não integrados nativamente.

### Django REST Framework

Vantagens:

- ecossistema completo;
- autenticação e administração maduras.

Desvantagens:

- framework mais intrusivo;
- ORM acoplado;
- maior peso;
- menor alinhamento com a estrutura atual.

### FastAPI

Vantagens:

- tipagem;
- Pydantic;
- OpenAPI automático;
- alta produtividade;
- boa testabilidade;
- suporte assíncrono.

Desvantagens:

- risco de lógica em endpoints;
- dependência de Pydantic;
- mudanças frequentes no ecossistema.

## Decisão

O LifeOS utilizará **FastAPI** como adapter HTTP inicial.

O framework ficará exclusivamente na camada:

```text
presentation/api/fastapi/
```

## Responsabilidades permitidas

A Presentation poderá:

- receber requests;
- validar schemas básicos;
- extrair autenticação;
- invocar Commands e Queries;
- traduzir erros;
- retornar responses;
- expor OpenAPI.

## Responsabilidades proibidas

FastAPI não poderá:

- executar regras de domínio;
- acessar SQLAlchemy diretamente;
- realizar commits;
- calcular progressão;
- alterar Aggregates sem Application Layer;
- expor ORM Models.

## Lifespan

A inicialização deverá utilizar o mecanismo oficial de `lifespan`.

É proibido utilizar APIs depreciadas como:

```python
@app.on_event("startup")
```

quando houver substituição oficial.

## Consequências positivas

- produtividade;
- documentação automática;
- tipagem;
- integração com testes;
- schemas claros.

## Consequências negativas

- dependência de framework;
- necessidade de acompanhar depreciações;
- risco de endpoints acumularem lógica;
- necessidade de separar schemas e DTOs.

## Capabilities afetadas

Todas as Capabilities com APIs HTTP.

## Features afetadas

Features expostas externamente.

## RFs afetados

RFs com endpoints.

## Migration necessária

Não.

## Breaking Change

Não.

## Documentos afetados

- `docs/04_BACKEND/API.md`
- `docs/05_FRONTEND/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/main.py
app/app_factory.py
app/<capability>/presentation/api/fastapi/
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# ADR-015 — SQLAlchemy e Alembic como persistência inicial

## Estado

Accepted

## Data

2026-08-04

## Impacto

High

## Origem

Fundação técnica da Sprint 01.

## Contexto

O LifeOS necessita de persistência relacional para:

- usuários;
- sessões;
- Player;
- Character;
- dados das futuras Capabilities;
- integridade referencial;
- migrations;
- transações.

O domínio deverá permanecer independente da tecnologia de persistência.

## Problema

Era necessário selecionar uma solução que fornecesse:

- ORM;
- controle explícito de sessão;
- transações;
- mapeamento relacional;
- integração com SQLite e bancos futuros;
- migrations versionadas;
- boa compatibilidade com Python.

## Alternativas consideradas

### SQL manual

Vantagens:

- controle total;
- menor abstração;
- performance previsível.

Desvantagens:

- maior quantidade de código;
- mapeamento manual;
- risco de inconsistências;
- menor produtividade.

### Django ORM

Vantagens:

- maduro;
- migrations integradas;
- API produtiva.

Desvantagens:

- dependência do Django;
- modelo Active Record;
- menor alinhamento com Clean Architecture.

### SQLAlchemy com Alembic

Vantagens:

- ORM maduro;
- controle explícito;
- Data Mapper;
- sessões e transações;
- suporte a múltiplos bancos;
- Alembic para migrations.

Desvantagens:

- curva de aprendizado;
- configuração mais detalhada;
- necessidade de mappers;
- risco de sessão mal gerenciada.

## Decisão

O LifeOS utilizará:

```text
SQLAlchemy
```

como tecnologia inicial de persistência relacional e:

```text
Alembic
```

como ferramenta oficial de migrations.

## Separação obrigatória

O domínio utilizará:

- Aggregates;
- Entities;
- Value Objects;
- Repository Ports.

A Infrastructure utilizará:

- ORM Models;
- SQLAlchemy Repositories;
- Persistence Mappers;
- SQLAlchemy Unit of Work.

## Regras de ORM

- ORM Models não são Entities de domínio;
- ORM Models não conterão regras de negócio;
- Repositories converterão ORM ↔ Domain;
- Application não receberá ORM Models;
- Presentation não importará SQLAlchemy;
- sessions serão controladas pelo Unit of Work.

## Regras de migrations

- toda alteração de schema utilizará Alembic;
- migrations aplicadas não poderão ser alteradas;
- novas alterações exigem nova revisão;
- `upgrade()` deverá ser implementado;
- `downgrade()` deverá existir quando tecnicamente possível;
- `create_all()` não substituirá migrations;
- Alembic deverá permanecer em `head`;
- upgrades deverão ser testados em banco novo e banco existente.

## Banco inicial

SQLite poderá ser utilizado inicialmente para:

- desenvolvimento;
- testes;
- execução local.

A arquitetura deverá permitir adoção futura de PostgreSQL sem alterar Domain ou Application.

## Consequências positivas

- persistência desacoplada;
- migrations versionadas;
- transações explícitas;
- suporte a diferentes bancos;
- boa integração com Unit of Work.

## Consequências negativas

- necessidade de mappers;
- maior quantidade de código;
- risco de inconsistência entre Domain e ORM;
- SQLite possui limitações em relação a bancos de produção.

## Capabilities afetadas

Todas as Capabilities persistentes.

## Features afetadas

Todas as Features com armazenamento.

## RFs afetados

Todos os RFs persistentes.

## Migration necessária

Sim, conforme cada Feature.

## Breaking Change

Não.

## Documentos afetados

- `docs/03_DATABASE/`
- `docs/04_BACKEND/`
- `GEMINI.md`
- `docs/10_AI_ENGINEERING/DEFINITION_OF_DONE.md`
- `docs/10_AI_ENGINEERING/CODE_REVIEW_CHECKLIST.md`

## Código relacionado

```text
app/shared/infrastructure/database.py
app/shared/infrastructure/unit_of_work.py
app/<capability>/infrastructure/persistence/
migrations/
alembic.ini
```

## Commits relacionados

A registrar.

## Supersedes

Nenhum.

---

# Índice Atualizado de Decisões

| ADR | Título | Estado | Impacto |
|---|---|---|---|
| ADR-001 | TSID como identificador oficial | Accepted | High |
| ADR-002 | Clean Architecture como arquitetura obrigatória | Accepted | Critical |
| ADR-003 | Domain-Driven Design como padrão de modelagem | Accepted | Critical |
| ADR-004 | CQRS simples na Application Layer | Accepted | High |
| ADR-005 | Composition Root centralizado | Accepted | High |
| ADR-006 | Shared Kernel restrito a conceitos transversais | Accepted | High |
| ADR-007 | Game Engine como única autoridade de progressão | Accepted | Critical |
| ADR-008 | Character limitado à identidade e ao perfil persistente | Accepted | Critical |
| ADR-009 | Publicação de eventos após commit bem-sucedido | Accepted | High |
| ADR-010 | Unit of Work como autoridade transacional | Accepted | Critical |
| ADR-011 | Criação atômica de User, Player e Character | Accepted | Critical |
| ADR-012 | Proibição de dependências entre internals de Capabilities | Accepted | Critical |
| ADR-013 | UserId como identidade transversal no Shared Kernel | Accepted | High |
| ADR-014 | FastAPI como adapter HTTP inicial | Accepted | Medium |
| ADR-015 | SQLAlchemy e Alembic como persistência inicial | Accepted | High |

---

# Modelo Oficial para Novos ADRs

```md
# ADR-XXX — Título da decisão

## Estado

Proposed | Accepted | Deprecated | Superseded | Rejected

## Data

YYYY-MM-DD

## Impacto

Critical | High | Medium | Low

## Origem

Origem da decisão.

## Contexto

Contexto da decisão.

## Problema

Problema arquitetural.

## Alternativas consideradas

### Alternativa A

Vantagens:

- ...

Desvantagens:

- ...

### Alternativa B

Vantagens:

- ...

Desvantagens:

- ...

## Decisão

Decisão aprovada.

## Regras derivadas

- ...

## Consequências positivas

- ...

## Consequências negativas

- ...

## Capabilities afetadas

- ...

## Features afetadas

- ...

## RFs afetados

- ...

## Migration necessária

Sim | Não

## Breaking Change

Sim | Não

## Documentos afetados

- ...

## Código relacionado

- ...

## Commits relacionados

- ...

## Supersedes

Nenhum ou ADR anterior.
```