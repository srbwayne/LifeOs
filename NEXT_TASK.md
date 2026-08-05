# NEXT_TASK.md

> Documento oficial que define a única tarefa autorizada para implementação.

---

# Informações Gerais

| Campo | Valor |
|--------|--------|
| ID | SPR-002 |
| Sprint | Sprint 02 |
| Status | READY |
| Prioridade | Alta |
| Capability | CHAR |
| Responsável | AI Agent |
| Dependência | Sprint 01 ✅ |
| Início | A definir |
| Prazo | A definir |

---

# Objetivo

Expandir a **Capability Character** já existente, responsável pela identidade, pelo perfil e pela representação persistente do Player dentro da plataforma LifeOS.

Esta Sprint deverá preservar integralmente as estruturas criadas na Sprint 01 e evoluir apenas as consultas, a persistência e os eventos de criação pertencentes ao domínio Character.

---

# Capability

**CHAR**

---

# Features

- CHAR-001
- CHAR-002
- CHAR-003
- CHAR-004

---

# Requisitos Funcionais

- RF-CHAR-001
- RF-CHAR-002
- RF-CHAR-003
- RF-CHAR-004

---

# Escopo

Expandir somente:

- identidade do Character
- informações de perfil
- representação persistente do Character
- Persistência
- Repositórios
- consultas
- eventos de criação do Character
- APIs REST de consulta
- DTOs
- Queries
- novas migrations, somente se necessárias, sem alterar migrations existentes
- Testes Unitários
- Testes de Integração
- Testes Arquiteturais

---

# Fora do Escopo

Não implementar:

- Health
- Workout
- Reading
- Therapy
- Habits
- Game Engine
- XP
- Level
- Progressão
- Classes
- Skills
- Quests
- Rewards
- Attribute Evolution
- atributos evolutivos
- evolução
- balanceamento
- Dashboard
- Analytics
- Artificial Intelligence
- Reports
- Administration

---

# Dependências

Obrigatório utilizar a infraestrutura criada na Sprint 01:

- TSID
- UnitOfWork
- EventBus
- PasswordHasher
- Composition Root
- Shared Kernel
- CQRS
- Clean Architecture

Não duplicar componentes já existentes.

---

# Arquivos que poderão ser alterados

## Código

- app/character/**
- app/shared/** (apenas se necessário)

## Banco

- migrations/

## Testes

- tests/character/**

## Documentação

- DATABASE.md
- CHANGELOG.md
- PROJECT_STATUS.md
- TASK_HISTORY.md

---

# Critérios de Aceite

A Sprint será considerada concluída somente quando:

- RF-CHAR-001, RF-CHAR-002, RF-CHAR-003 e RF-CHAR-004 estiverem integralmente implementados.
- Todos os testes estiverem passando.
- Nenhum import quebrado.
- Nenhum warning relevante.
- Aplicação iniciar corretamente.
- Cobertura preservada ou aumentada.
- Documentação atualizada.
- Migrations executadas.
- Alembic atualizado.

---

# Evidências Obrigatórias

Ao finalizar apresentar obrigatoriamente:

## Banco

- Resultado do Alembic

## Testes

Resultado completo do:

```bash
python -m pytest -v
```

Cobertura:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

## Imports

Resultado da validação de imports.

## Aplicação

Resultado da execução:

```bash
python -m uvicorn app.main:app --reload
```

## APIs

Listagem das rotas criadas.

---

# Atualizações Obrigatórias

Ao finalizar atualizar:

- CHANGELOG.md
- PROJECT_STATUS.md
- TASK_HISTORY.md

---

# Restrições

Nunca:

- implementar funcionalidades de outras Capabilities;
- alterar arquitetura sem aprovação;
- alterar migrations já executadas;
- remover testes existentes;
- silenciar warnings ou erros.

---

# Definition of Done

Seguir integralmente:

- GEMINI.md
- AGENTS.md
- PRD.md
- CAPABILITY_MAP.md
- DATABASE.md
- ARCHITECTURE.md
- DEFINITION_OF_DONE.md

Nenhuma tarefa poderá ser considerada concluída sem atender integralmente todos os documentos acima.

---

# Próximo Passo

Após aprovação desta Sprint, uma nova versão deste arquivo será criada para a Sprint 03.
