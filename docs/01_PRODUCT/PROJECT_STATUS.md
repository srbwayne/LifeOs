# Project Status

## Sprint 04 — Reading Sessions - 2026-08-09

**Status:** AUTORIZADA — implementação ainda não iniciada
**Capability:** READ
**Feature:** READ-002 — Reading Sessions
**User Story:** US-READ-002-001
**Requisito Funcional:** RF-READ-003

### Objetivo autorizado

Permitir que o Player registre uma sessão de leitura referente a um Book existente em sua biblioteca.

### Estado

- READ-002 selecionada pelo Product Owner.
- Planejamento técnico pendente.
- Nenhuma implementação iniciada nesta etapa.
- RF-READ-004+ permanecem fora do escopo.
## Sprint 03 — Reading Library - 2026-08-09

**Status:** ✅ Concluída
**Capability:** READ
**Feature:** READ-001 — Cadastro de livros e consulta da biblioteca
**User Story:** US-READ-001-001
**Requisitos Funcionais:** RF-READ-001 e RF-READ-002

### Entregas

- Capability READ criada com `Book` como Aggregate Root.
- Biblioteca pessoal persistente com ownership por `UserId` e isolamento entre usuários.
- Cadastro autenticado por `POST /books`.
- Consulta autenticada por `GET /books`.
- Migration `0004` integrada como head.
- Documentação técnica READ sincronizada com a implementação.
- CI da `main` aprovado após o merge do PR #7.

### Estado funcional

- READ-001: ENTREGUE.
- RF-READ-001: ENTREGUE.
- RF-READ-002: ENTREGUE.
- RF-READ-003+: NÃO ENTREGUES.
- Sprint 04 — Reading Sessions autorizada posteriormente pelo Product Owner.

### Pendência

- Divergência global de versionamento entre `/books` e `/api/v1`: PENDENTE — NÃO BLOQUEANTE.

## SPR-2.1 — Consolidação de Governança - 2026-08-08

**Status:** ✅ Concluída
**Autorização funcional:** Nenhuma

### Estado consolidado

- Baseline de governança e políticas de engenharia consolidadas.
- Arquitetura e isolamento entre Capabilities validados.
- Ruff e Mypy adotados como ferramentas oficiais.
- Playbook Permanente de Engenharia integrado com AI Agent Workflow, Checklists e Incident Response.
- GitHub Actions ativo com Python 3.10 validado em runner real.
- Quality Gates automatizados e três required status checks ativos na `main`.
- Branch protection preservada.
- Nenhuma Sprint funcional subsequente autorizada.

## Sprint 02 — Character - 2026-08-04

**Versão Atual:** 0.2.0
**Status:** Sprint 02 ✅ Concluída

### Resumo

A Sprint 02 expandiu a Capability Character preservando a criação atômica de User, Player e Character entregue na Sprint 01. Foram implementadas identidade tipada, representação persistente, evento de criação e consultas autenticadas somente leitura do Character e das informações de perfil.

As relações `User 1:1 Player` e `Player 1:1 Character` permanecem protegidas pelo domínio e pelas constraints existentes no banco. Nenhuma migration adicional foi necessária.

### Features concluídas

- CHAR-001: criação automática e única do Character.
- CHAR-002: identidade associada à representação persistente existente.
- CHAR-003: consulta autenticada do perfil do Character.
- CHAR-004: consulta autenticada das informações persistidas de perfil.

### Validação

- Ambiente virtual limpo instalado por `requirements.txt`.
- Migrations executadas até `0003 (head)` em banco novo.
- Baseline do banco local legado sincronizado com `0003` após confirmação de schema e `integrity_check: ok`.
- Suíte completa: 19 testes aprovados.
- Suíte com `DeprecationWarning` tratado como erro: 19 testes aprovados.
- Cobertura total: 96%.
- Importação individual de 69 módulos: nenhuma falha.
- Uvicorn com reload: startup concluído sem warnings.
- Endpoints Character: somente `GET /character` e `GET /character/profile`.
- Regressão da Sprint 01 preservada.

### Pendência documental conhecida

O arquivo `docs/01_PRODUCT/USE_CASES/CHAR/EPIC-CHAR.md` ainda atribui XP, Level, Progressão e Skills à Capability Character. Conforme decisão de produto, essa inconsistência não integra a Sprint 02 e deverá ser tratada em auditoria documental futura. Nenhum desses conceitos foi implementado.

## Auditoria de correção - 2026-08-04

A declaração original da Sprint 01 foi reauditada. A correção validou um ambiente
virtual limpo, instalação por `requirements.txt`, migrations até a revisão
`0003`, importação de todos os módulos, suíte completa e inicialização real do
Uvicorn. Os endpoints AUTH-001 a AUTH-005 e os fluxos de sessão já existentes
foram exercitados por testes E2E.

**Versão auditada:** 0.1.0
**Status da Sprint 01:** ✅ Concluída

## Resumo

A Sprint 01 foi concluída com sucesso, entregando a fundação arquitetural e a Capability de Autenticação completa. O sistema agora suporta o ciclo de vida de um usuário, desde o cadastro (incluindo a criação atômica de Player e Character) até o gerenciamento seguro de sessão e recuperação de conta. Todos os requisitos funcionais da Sprint foram implementados e validados por uma suíte de testes automatizados. A qualidade do código e a robustez da arquitetura foram validadas e corrigidas.

## Features Concluídas
- AUTH-001: Cadastro de usuário
- AUTH-002: Login
- AUTH-003: Logout
- AUTH-004: Recuperação de senha
- AUTH-005: Redefinição de senha

## Saúde do Projeto
- **Cobertura de Testes:** Alta para os fluxos implementados.
- **Débito Técnico:** Baixo.
- **Documentação:** Atualizada.
