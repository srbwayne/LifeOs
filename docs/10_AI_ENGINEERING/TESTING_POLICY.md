# TESTING_POLICY.md

> Política oficial de testes do projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os desenvolvedores e agentes de Inteligência Artificial.

---

# 1. Objetivo

Este documento define a política oficial de testes do projeto **LifeOS**.

Seu objetivo é garantir que todo código desenvolvido seja validado de forma consistente, reproduzível e automatizada antes de ser integrado ao projeto.

Os testes fazem parte da arquitetura do sistema e representam um dos principais mecanismos para garantir:

- qualidade;
- estabilidade;
- segurança;
- rastreabilidade;
- evolução sustentável;
- redução de regressões.

Nenhuma funcionalidade será considerada concluída sem a execução dos testes definidos nesta política.

---

# 2. Escopo

Esta política aplica-se a todo o projeto LifeOS.

Inclui:

- Domain;
- Application;
- Infrastructure;
- Presentation;
- Shared Kernel;
- APIs;
- banco de dados;
- migrations;
- integrações;
- scripts de automação.

Também se aplica ao código produzido por:

- desenvolvedores;
- Codex;
- Gemini;
- OpenCode;
- outros agentes de Inteligência Artificial.

---

# 3. Documentos Relacionados

Esta política complementa os seguintes documentos:

- DEFINITION_OF_DONE.md
- CODE_STYLE.md
- CODE_REVIEW_CHECKLIST.md
- RELEASE_PROCESS.md
- DEVELOPMENT_WORKFLOW.md
- VERSIONING.md
- DEPENDENCY_POLICY.md

Todos deverão ser considerados durante o processo de validação.

Em caso de conflito, prevalecerão:

1. ADRs aprovadas;
2. arquitetura oficial;
3. esta política.

---

# 4. Princípios

A estratégia de testes do LifeOS baseia-se nos princípios abaixo.

---

## 4.1. Testes fazem parte do produto

Testes não são documentação auxiliar.

Eles fazem parte do software.

Uma funcionalidade sem testes automatizados não será considerada concluída.

---

## 4.2. Automação

Todo teste deverá ser automatizado sempre que tecnicamente possível.

Testes manuais deverão existir apenas quando:

- houver limitação técnica;
- envolverem validação visual;
- dependerem de recursos externos não automatizáveis.

---

## 4.3. Determinismo

Todo teste deverá produzir sempre o mesmo resultado.

Os testes não deverão depender de:

- horário atual;
- ordem de execução;
- internet;
- estado do ambiente;
- banco persistente compartilhado.

---

## 4.4. Independência

Cada teste deverá poder ser executado isoladamente.

Um teste não deverá depender:

- da execução anterior;
- de outro teste;
- da ordem da suíte.

---

## 4.5. Velocidade

Os testes deverão ser rápidos.

Sempre que possível:

- utilizar banco temporário;
- evitar chamadas externas;
- evitar esperas desnecessárias;
- utilizar fixtures reutilizáveis.

---

## 4.6. Regressão

Todo defeito corrigido deverá gerar um novo teste.

Esse teste garantirá que o problema não volte a ocorrer futuramente.

---

## 4.7. Evidência

Nenhuma Sprint poderá ser considerada concluída sem evidências reais da execução dos testes.

Essas evidências deverão ser registradas no relatório técnico da Sprint.

---

# 5. Pirâmide de Testes

O LifeOS adota oficialmente a Pirâmide de Testes.

A maior parte da suíte deverá ser composta por testes rápidos e isolados.

## Ordem de prioridade

1. Testes Unitários
2. Testes de Integração
3. Testes End-to-End
4. Testes Arquiteturais

---

## Testes Unitários

Objetivo:

Validar regras de negócio isoladamente.

Exemplos:

- Value Objects;
- Aggregates;
- Domain Services;
- Commands;
- Queries.

---

## Testes de Integração

Objetivo:

Validar integração entre componentes.

Exemplos:

- Repositories;
- Unit of Work;
- SQLAlchemy;
- Event Bus;
- Alembic.

---

## Testes End-to-End

Objetivo:

Validar fluxos completos da aplicação.

Exemplos:

- registro;
- login;
- refresh token;
- consulta de Character;
- recuperação de senha.

---

## Testes Arquiteturais

Objetivo:

Garantir que a arquitetura oficial permaneça preservada.

Exemplos:

- regras de dependência;
- isolamento entre Capabilities;
- ausência de imports proibidos;
- fronteiras da Clean Architecture.

---

# 6. Ferramentas Oficiais

As ferramentas oficiais para testes são:

| Ferramenta | Finalidade |
|------------|------------|
| pytest | Execução da suíte |
| pytest-cov | Cobertura |
| FastAPI TestClient | Testes HTTP |
| HTTPX | Cliente HTTP |
| SQLite | Banco temporário |
| Alembic | Validação de migrations |

Novas ferramentas deverão ser aprovadas pelo Arquiteto de Software antes de sua adoção.

---

## Execução da suíte

Execução completa:

```bash
python -m pytest -v
```

---

## Cobertura

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

## Warnings

```bash
python -W error::DeprecationWarning -m pytest -v
```

Todos esses comandos deverão permanecer funcionais durante toda a evolução do projeto.

---

# 7. Organização dos Testes

A estrutura dos testes deverá espelhar a estrutura da aplicação.

Exemplo:

```text
tests/
├── architecture/
├── auth/
│   ├── application/
│   ├── domain/
│   ├── integration/
│   └── e2e/
├── character/
├── health/
├── workout/
├── reading/
├── therapy/
├── habits/
├── game/
└── shared/
```

Cada Capability deverá possuir sua própria suíte.

Não deverão existir testes compartilhados entre Capabilities sem justificativa arquitetural.

---

# 8. Convenções

Os testes deverão seguir uma convenção única de nomenclatura.

---

## Arquivos

Formato:

```text
test_<componente>.py
```

Exemplos:

- test_user.py
- test_character.py
- test_auth_flow.py
- test_character_repository.py

---

## Funções

Formato:

```text
test_<comportamento>()
```

Exemplos:

- test_register_user_successfully()
- test_login_returns_access_token()
- test_character_creation_raises_event()
- test_refresh_token_is_revoked()

Os nomes deverão descrever claramente o comportamento esperado.

---

## Organização

Cada teste deverá possuir:

1. preparação do cenário;
2. execução da ação;
3. validação do resultado.

Sempre que possível, utilizar o padrão **Arrange → Act → Assert**.

A estrutura deverá permanecer consistente em toda a suíte de testes.

---

# 9. Testes Unitários

Os testes unitários representam a base da estratégia de testes do LifeOS.

Seu objetivo é validar regras de negócio de forma isolada, rápida e determinística.

Toda regra de domínio deverá possuir cobertura por testes unitários.

---

## 9.1. Objetivos

Os testes unitários deverão validar:

- Value Objects;
- Aggregates;
- Domain Services;
- Domain Events;
- Domain Errors;
- Commands;
- Queries;
- validações de domínio;
- invariantes;
- regras de negócio.

---

## 9.2. Características

Os testes unitários deverão:

- executar rapidamente;
- ser independentes;
- não acessar banco de dados;
- não acessar APIs externas;
- não depender da infraestrutura;
- não compartilhar estado.

---

## 9.3. Exemplos

Exemplos de testes unitários:

- criação de User;
- criação de Character;
- validação de Email;
- validação de PlayerName;
- geração de Domain Events;
- cálculo de regras de negócio.

---

# 10. Testes de Integração

Os testes de integração validam a comunicação entre componentes da aplicação.

Seu objetivo é garantir que as implementações concretas estejam funcionando corretamente.

---

## 10.1. Objetivos

Validar:

- SQLAlchemy;
- Repositories;
- Unit of Work;
- Event Bus;
- PasswordHasher;
- JWT Provider;
- Alembic;
- integrações entre camadas.

---

## 10.2. Banco de Dados

Sempre que possível, utilizar banco temporário.

Os testes não deverão utilizar banco persistente compartilhado.

Cada teste deverá iniciar com ambiente limpo.

---

## 10.3. Repositories

Todo Repository deverá possuir testes para:

- persistência;
- recuperação;
- atualização;
- exclusão quando aplicável;
- tratamento de erros.

---

# 11. Testes End-to-End

Os testes End-to-End validam fluxos completos da aplicação.

Seu objetivo é garantir que o sistema funcione corretamente sob a perspectiva do usuário.

---

## 11.1. Fluxos Obrigatórios

Cada Capability deverá possuir testes E2E para seus principais casos de uso.

Exemplos:

### AUTH

- registro;
- login;
- refresh token;
- logout;
- recuperação de senha.

---

### CHARACTER

- consulta do Character;
- consulta do perfil.

---

### HEALTH

- criação de registro;
- consulta;
- histórico.

---

### GAME

- geração de XP;
- evolução de nível;
- conquistas;
- recompensas.

---

## 11.2. APIs

Os testes deverão validar:

- códigos HTTP;
- payloads;
- autenticação;
- autorização;
- validações;
- tratamento de erros.

---

# 12. Testes Arquiteturais

Os testes arquiteturais garantem que a arquitetura oficial permaneça preservada.

Eles representam um dos principais mecanismos de proteção do projeto.

---

## 12.1. Objetivos

Validar:

- Clean Architecture;
- DDD;
- CQRS;
- isolamento entre Capabilities;
- regras de dependência;
- Shared Kernel.

---

## 12.2. Exemplos

Verificar que:

- Domain não depende de Infrastructure;
- Domain não depende de Presentation;
- Application não depende de Presentation;
- Infrastructure implementa apenas Ports;
- Capabilities permanecem isoladas.

---

## 12.3. Obrigatoriedade

Toda nova Capability deverá possuir testes arquiteturais quando houver novas regras de dependência.

---

# 13. Testes de Repositories

Repositories representam uma das principais integrações da aplicação.

Todos deverão possuir testes específicos.

---

## Validar

- persistência;
- recuperação;
- filtros;
- consultas;
- paginação;
- tratamento de entidades inexistentes.

---

## Não validar

Repositories não deverão conter regras de negócio.

Essas regras pertencem ao domínio.

---

# 14. Testes de Domain Events

Todo Domain Event deverá possuir testes.

---

## Validar

- geração do evento;
- conteúdo do evento;
- momento da publicação;
- processamento pelo Event Bus.

---

## Ordem obrigatória

Validar que:

1. Aggregate gera o evento.
2. Repository persiste o Aggregate.
3. Unit of Work realiza o commit.
4. Event Bus publica o evento.

Essa ordem deverá permanecer consistente durante toda a evolução do projeto.

---

# 15. Testes de CQRS

Commands e Queries deverão possuir testes independentes.

---

## Commands

Validar:

- regras de escrita;
- alterações de estado;
- geração de eventos;
- tratamento de erros.

---

## Queries

Validar:

- consultas;
- DTOs;
- isolamento por usuário;
- filtros;
- paginação quando aplicável.

Queries nunca deverão alterar estado.

---

# 16. Cobertura de Código

A cobertura de código é um indicador de qualidade, mas não substitui testes bem escritos.

---

## Meta Oficial

Como meta mínima do projeto:

| Tipo | Cobertura |
|------|----------:|
| Projeto | ≥ 90% |
| Domain | ≥ 95% |
| Aggregates | 100% recomendado |
| Value Objects | 100% recomendado |

---

## Execução

Executar:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

## Interpretação

Cobertura elevada não garante qualidade.

Os testes deverão validar comportamento e regras de negócio, não apenas executar linhas de código.

---

# 17. Banco de Dados

Os testes que envolvem persistência deverão utilizar um ambiente controlado e reproduzível.

O objetivo é garantir que a validação do banco de dados seja confiável, isolada e independente do ambiente do desenvolvedor.

---

## 17.1. Banco Temporário

Sempre que possível, utilizar banco temporário durante os testes.

Não utilizar banco de desenvolvimento compartilhado.

Cada execução deverá iniciar com um estado limpo.

---

## 17.2. Migrations

Toda migration criada deverá ser validada.

Executar obrigatoriamente:

```bash
python -m alembic upgrade head
```

Validar a versão atual:

```bash
python -m alembic current
```

Quando houver suporte a rollback:

```bash
python -m alembic downgrade -1
python -m alembic upgrade head
```

O banco deverá permanecer consistente após essas operações.

---

## 17.3. Integridade

Sempre validar:

- integridade referencial;
- constraints;
- índices;
- unicidade;
- chaves estrangeiras;
- versionamento do Alembic.

Não deverão existir migrations quebradas.

---

# 18. Fixtures

As Fixtures deverão padronizar a criação dos cenários utilizados pelos testes.

Seu objetivo é reduzir duplicação e aumentar a legibilidade.

---

## Regras

As Fixtures deverão ser:

- reutilizáveis;
- pequenas;
- independentes;
- previsíveis.

Cada Fixture deverá possuir apenas uma responsabilidade.

---

## Organização

As Fixtures deverão permanecer organizadas por Capability.

Exemplo:

```text
tests/
├── auth/
│   └── fixtures.py
├── character/
│   └── fixtures.py
├── game/
│   └── fixtures.py
└── shared/
    └── fixtures.py
```

---

## Evitar

Não criar Fixtures gigantescas contendo dezenas de objetos.

Preferir composição de Fixtures menores.

---

# 19. Mocks

Mocks deverão ser utilizados apenas quando houver necessidade de isolar dependências externas.

Não utilizar Mocks para substituir regras de negócio.

---

## Casos permitidos

Utilizar Mocks para:

- SMTP;
- APIs externas;
- serviços HTTP;
- Redis;
- serviços de terceiros;
- provedores de autenticação.

---

## Casos proibidos

Não utilizar Mocks para:

- Aggregates;
- Value Objects;
- Domain Services;
- regras de negócio.

Esses componentes deverão ser testados utilizando implementações reais.

---

## Objetivo

Mocks deverão reduzir dependências externas, nunca esconder defeitos da implementação.

---

# 20. Dados de Teste

Os dados utilizados pelos testes deverão ser representativos e previsíveis.

Evitar dados aleatórios quando não forem necessários.

---

## Utilizar

Exemplos consistentes:

- e-mails válidos;
- nomes reais;
- identificadores determinísticos;
- datas controladas.

---

## Evitar

Não utilizar:

- valores aleatórios;
- horários do sistema;
- identificadores imprevisíveis;
- dependência de serviços externos.

Quando necessário, controlar a aleatoriedade utilizando sementes fixas.

---

# 21. Testes de Performance

Testes de performance não substituem testes funcionais.

Seu objetivo é identificar degradações de desempenho.

---

## Exemplos

Validar:

- tempo de resposta;
- consumo de memória;
- consultas SQL;
- utilização de índices;
- operações em lote.

---

## Regras

Os resultados deverão ser mensuráveis.

Toda otimização deverá ser baseada em evidências e não em percepção.

---

# 22. Testes de Regressão

Todo defeito corrigido deverá gerar um teste de regressão.

Esse teste deverá permanecer permanentemente na suíte.

---

## Objetivos

Garantir que:

- o problema foi realmente corrigido;
- a falha não volte a ocorrer;
- futuras alterações não reintroduzam o defeito.

---

## Identificação

Sempre que possível, documentar a origem da regressão.

Exemplo:

```python
# Regressão corrigida na Sprint 03 (RF-AUTH-007)
```

Quando existir uma Issue ou ADR relacionada, incluir a referência correspondente.

---

# 23. Testes Obrigatórios por Capability

Toda Capability deverá possuir uma suíte mínima de testes.

---

## Domain

Obrigatórios:

- Aggregates;
- Value Objects;
- Domain Events;
- Domain Errors;
- Domain Services.

---

## Application

Obrigatórios:

- Commands;
- Queries;
- Handlers;
- DTOs quando possuírem comportamento.

---

## Infrastructure

Obrigatórios:

- Repositories;
- Mappers;
- Unit of Work;
- Event Bus;
- integrações.

---

## Presentation

Obrigatórios:

- endpoints;
- autenticação;
- autorização;
- validações HTTP;
- códigos de resposta.

---

## End-to-End

Toda Capability deverá possuir ao menos um fluxo completo validado.

---

# 24. Testes para Agentes de Inteligência Artificial

Os agentes de Inteligência Artificial deverão executar exatamente os mesmos testes exigidos dos desenvolvedores.

Não será permitido declarar uma Sprint concluída sem evidências reais de execução.

---

## Execuções obrigatórias

Antes da conclusão da Sprint, deverão ser executados:

```bash
python -m pytest -v
```

---

```bash
python -W error::DeprecationWarning -m pytest -v
```

---

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

```bash
python -m pip check
```

---

Quando houver alterações estruturais:

```bash
python -m alembic upgrade head
```

---

Quando houver APIs:

- inicializar o Uvicorn;
- validar `/docs`;
- validar `/openapi.json`;
- validar os endpoints alterados.

---

Os agentes deverão apresentar evidências reais da execução desses comandos.

Não serão aceitas declarações de sucesso sem a respectiva validação.

---

# 25. Gates de Qualidade

Antes que qualquer implementação seja considerada concluída, todos os Gates de Qualidade deverão ser aprovados.

Esses gates representam os critérios mínimos para garantir que o software atende aos padrões técnicos definidos pelo LifeOS.

---

## 25.1. Gate de Compilação

A aplicação deverá:

- iniciar corretamente;
- possuir todos os imports válidos;
- não apresentar erros de sintaxe;
- não possuir dependências quebradas.

Sempre que aplicável, executar:

```bash
python -m pip check
```

Resultado esperado:

```text
No broken requirements found.
```

---

## 25.2. Gate de Banco de Dados

Quando houver alterações estruturais, deverão ser validados:

- migrations;
- versionamento do Alembic;
- integridade do schema;
- constraints;
- índices.

Executar:

```bash
python -m alembic upgrade head
```

---

## 25.3. Gate de Testes

Todos os testes obrigatórios deverão ser aprovados.

Inclui:

- testes unitários;
- testes de integração;
- testes End-to-End;
- testes arquiteturais.

Executar:

```bash
python -m pytest -v
```

---

## 25.4. Gate de Cobertura

A cobertura deverá atender às metas oficiais do projeto.

Executar:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

## 25.5. Gate de Warnings

A suíte deverá ser executada tratando warnings de depreciação como erro.

Executar:

```bash
python -W error::DeprecationWarning -m pytest -v
```

Nenhum `DeprecationWarning` deverá permanecer.

---

## 25.6. Gate da Aplicação

Quando houver alteração na API, deverá ser validado:

- inicialização do Uvicorn;
- documentação OpenAPI;
- endpoint `/docs`;
- endpoint `/openapi.json`;
- rotas alteradas.

---

# 26. Checklist de Testes

Antes da conclusão de qualquer Sprint, verificar:

## Código

- [ ] Compila corretamente.
- [ ] Sem erros de importação.
- [ ] Sem dependências quebradas.

---

## Banco

- [ ] Migrations executadas.
- [ ] Schema consistente.
- [ ] Alembic sincronizado.

---

## Testes

- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados.
- [ ] Testes End-to-End aprovados.
- [ ] Testes arquiteturais aprovados.

---

## Cobertura

- [ ] Cobertura dentro da meta.
- [ ] Nenhuma regressão detectada.

---

## API

- [ ] Uvicorn iniciado.
- [ ] `/docs` disponível.
- [ ] `/openapi.json` disponível.
- [ ] Endpoints principais validados.

---

## Documentação

- [ ] Evidências registradas.
- [ ] Relatório técnico atualizado.
- [ ] CHANGELOG atualizado quando aplicável.

---

# 27. Não Conformidades

Os itens abaixo impedem a aprovação da Sprint.

---

## Código

- erro de compilação;
- import inválido;
- dependência quebrada;
- erro de sintaxe.

---

## Banco

- migration inválida;
- schema inconsistente;
- falha no upgrade.

---

## Testes

- qualquer teste falhando;
- cobertura abaixo da meta;
- regressão conhecida.

---

## Arquitetura

- violação da Clean Architecture;
- quebra das regras de dependência;
- acoplamento entre Capabilities.

---

## Documentação

- documentação inconsistente;
- evidências ausentes;
- rastreabilidade incompleta.

Enquanto existir qualquer não conformidade bloqueante, a implementação não poderá ser considerada concluída.

---

# 28. Auditoria

Toda Sprint deverá produzir evidências suficientes para permitir auditoria completa.

Deverá ser possível identificar:

- Sprint;
- Capability;
- Feature;
- Requisitos Funcionais implementados;
- testes executados;
- cobertura obtida;
- migrations executadas;
- versão do banco;
- versão da aplicação;
- evidências da execução;
- data da validação.

As evidências deverão ser reais e reproduzíveis.

---

## Evidências mínimas

Sempre que aplicável, registrar:

- resultado do `pytest`;
- cobertura;
- `pip check`;
- validação do Alembic;
- inicialização do Uvicorn;
- validação dos endpoints principais;
- quantidade de testes executados.

---

# 29. Métricas

As métricas de testes deverão ser acompanhadas continuamente.

---

## Indicadores mínimos

- percentual de cobertura;
- número de testes;
- tempo total da suíte;
- regressões encontradas;
- defeitos corrigidos;
- testes adicionados;
- migrations validadas.

---

## Objetivos

As métricas deverão apoiar:

- melhoria contínua;
- redução de regressões;
- estabilidade das Releases;
- evolução da qualidade do projeto.

Não deverão ser utilizadas como único critério de qualidade.

---

# 30. Regra Final

No LifeOS, testes são parte integrante do produto.

Nenhuma funcionalidade será considerada concluída apenas porque o código foi implementado.

Uma implementação somente será considerada pronta quando:

- todos os testes obrigatórios forem aprovados;
- a arquitetura permanecer íntegra;
- a cobertura atender às metas estabelecidas;
- não existirem regressões conhecidas;
- as evidências de execução forem registradas;
- os critérios da **Definition of Done** forem integralmente atendidos.

A qualidade do software sempre terá prioridade sobre a velocidade de entrega.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial de testes do projeto LifeOS. |