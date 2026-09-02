# DECISION LOG

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Registro de Decisões Arquiteturais (ADR Index)

---

# 1. Objetivo

Este documento registra todas as decisões arquiteturais relevantes tomadas durante o desenvolvimento do LifeOS.

Seu propósito é preservar o contexto técnico das decisões, evitando que elas sejam perdidas ao longo da evolução do projeto.

Cada decisão registrada deverá possuir motivação, alternativas consideradas, justificativa, consequências e status.

Este documento representa a memória arquitetural oficial do projeto.

---

# 2. Objetivos do Decision Log

O Decision Log existe para:

- registrar decisões permanentes;
- documentar justificativas técnicas;
- evitar rediscussões recorrentes;
- facilitar onboarding;
- auxiliar agentes de IA;
- manter coerência arquitetural;
- preservar histórico técnico.

---

# 3. Quando Registrar uma Decisão

Uma decisão deve ser registrada quando alterar ou definir aspectos relevantes da arquitetura.

Exemplos:

- adoção de um novo padrão arquitetural;
- substituição de tecnologia;
- mudança estrutural;
- definição de convenções;
- criação de módulos;
- alteração de estratégia de persistência;
- mudança na política de eventos;
- alteração do modelo de autenticação;
- decisões que impactem vários módulos.

Não registrar decisões temporárias ou experimentais.

---

# 4. Estrutura Oficial de um ADR

Todo ADR deverá seguir o mesmo formato.

```text
ADR-XXXX

Título

Status

Data

Contexto

Problema

Alternativas

Decisão

Consequências

Impactos

Referências
```

---

# 5. Status Permitidos

Cada ADR deverá possuir exatamente um status.

## Proposed

A decisão está em discussão.

---

## Accepted

A decisão foi aprovada.

---

## Superseded

A decisão foi substituída por outra.

Sempre deverá informar qual ADR a substituiu.

---

## Deprecated

A decisão deixou de ser utilizada.

---

## Rejected

A proposta foi descartada.

---

# 6. Organização Física

Todos os ADRs deverão ficar em:

```text
docs/

02_ARCHITECTURE/

decisions/
```

Estrutura:

```text
decisions/

ADR-0001-clean-architecture.md

ADR-0002-ddd.md

ADR-0003-modular-monolith.md

ADR-0004-hexagonal.md

ADR-0005-sqlalchemy.md

ADR-0006-streamlit.md
```

Nunca criar ADRs fora desta pasta.

---

# 7. Convenção de Nomenclatura

Padrão obrigatório:

```text
ADR-XXXX-nome-da-decisao.md
```

Exemplos:

```text
ADR-0001-clean-architecture.md

ADR-0002-domain-driven-design.md

ADR-0003-modular-monolith.md

ADR-0004-event-driven-architecture.md

ADR-0005-multi-tenant.md
```

A numeração nunca deve ser reutilizada.

---

# 8. Índice Oficial de ADRs

Os ADRs serão numerados sequencialmente.

## Fundação

| ADR | Título | Status |
|------|---------|--------|
| ADR-0001 | Clean Architecture | Accepted |
| ADR-0002 | Domain-Driven Design | Accepted |
| ADR-0003 | Modular Monolith | Accepted |
| ADR-0004 | Hexagonal Architecture | Accepted |
| ADR-0005 | Event-Driven Architecture | Accepted |

---

## Interface

| ADR | Título | Status |
|------|---------|--------|
| ADR-0010 | Streamlit como Interface Inicial | Accepted |
| ADR-0011 | Dashboard MMORPG | Accepted |

---

## Persistência

| ADR | Título | Status |
|------|---------|--------|
| ADR-0020 | SQLAlchemy como ORM Oficial | Accepted |
| ADR-0021 | SQLite como Banco Inicial | Accepted |
| ADR-0022 | Migrações com Alembic | Accepted |

---

## Segurança

| ADR | Título | Status |
|------|---------|--------|
| ADR-0030 | Autenticação Multi-Tenant | Accepted |
| ADR-0031 | Hash de Senhas com bcrypt | Accepted |

---

## IA

| ADR | Título | Status |
|------|---------|--------|
| ADR-0040 | Arquitetura para AI Mentor | Proposed |
| ADR-0041 | Abstração de Provedores de IA | Accepted |

---

## Reading

| ADR | Título | Status |
|------|---------|--------|
| ADR-0042 | READ-005 — Book Completion Milestone | Accepted |

---

## Plataforma

| ADR | Título | Status |
|------|---------|--------|
| ADR-0043 | Python 3.11 — Minimum Platform Runtime | Accepted |

---

# 9. Template Oficial de ADR

```markdown
# ADR-000X

## Título

Status

Accepted

Data

YYYY-MM-DD

---

# Contexto

Descrever o cenário.

---

# Problema

Qual problema motivou esta decisão?

---

# Alternativas Consideradas

Alternativa 1

Alternativa 2

Alternativa 3

---

# Decisão

Descrever claramente a decisão tomada.

---

# Consequências

Positivas

Negativas

Trade-offs

---

# Impactos

Quais módulos são afetados?

---

# Referências

Links

Livros

Documentação
```

---

# 10. Como o Gemini deve utilizar este documento

Antes de alterar qualquer decisão arquitetural, o agente deverá:

1. Verificar se já existe um ADR relacionado.
2. Confirmar se a alteração é compatível com os ADRs aceitos.
3. Caso a decisão seja nova, criar um novo ADR.
4. Nunca modificar um ADR Accepted sem criar outro ADR que o substitua.
5. Atualizar o índice oficial de decisões.

Os ADRs representam a verdade arquitetural do projeto e devem prevalecer sobre implementações pontuais.
