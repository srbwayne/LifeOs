# Changelog

## [Unreleased]

### Added
- Consolidada a baseline de governança e estabelecidas as políticas oficiais de engenharia.
- Adotados Ruff e Mypy como ferramentas oficiais de qualidade.
- Integrado o Playbook Permanente de Engenharia com AI Agent Workflow, Checklists e Incident Response.
- Ativado o GitHub Actions com execução real em Python 3.10 e Quality Gates automatizados.
- Adicionada a Reading Library pessoal com cadastro de livros e consulta autenticada da biblioteca do usuário.

### Changed
- Validado o isolamento entre Capabilities e centralizada a identidade transversal no Shared Kernel.
- Configurados três required status checks na proteção da `main`, preservando as demais regras de branch protection.
- Integrada a migration `0004` para persistência de `books` com ownership por `UserId`.
- Sincronizada a documentação técnica da Capability READ com a implementação de READ-001.

## [0.2.0] - 2026-08-04

### Added
- Implementadas as consultas autenticadas `GET /character` e `GET /character/profile` para RF-CHAR-002, RF-CHAR-003 e RF-CHAR-004.
- Adicionados Value Objects de identidade e perfil para `Player` e `Character`.
- Adicionado o evento de domínio `CharacterCreated`, publicado somente após o commit da criação atômica prevista no RF-CHAR-001.
- Adicionados DTOs, Queries, repositories e mappers de leitura com isolamento pelo usuário autenticado.
- Adicionados testes unitários, de integração, E2E e arquiteturais da Capability Character.
- Adicionada a dependência de teste `pytest-cov==6.1.1` para a validação oficial de cobertura.

### Changed
- Fortalecidas as invariantes `User 1:1 Player` e `Player 1:1 Character` sem alteração do schema existente.
- Centralizado o provider de sessão no Shared Kernel para reutilização pelos Composition Roots AUTH e CHAR.
- Sincronizado o baseline Alembic do banco local legado com a revisão `0003`, após validação de integridade e compatibilidade do schema existente.

### Notes
- Nenhuma migration foi criada: as constraints e tabelas da revisão `0002` já atendem integralmente ao escopo da Sprint 02.
- Nenhum endpoint ou Command de alteração de perfil foi implementado.
- As inconsistências conhecidas de `EPIC-CHAR.md` sobre XP, Level, Progressão e Skills permanecem reservadas para auditoria documental futura.

## [0.1.1] - 2026-08-04

### Fixed
- Corrigida a geração de TSID para a API suportada por `tsidpy`.
- Corrigido o Unit of Work para compartilhar a mesma sessão dos repositórios.
- Restaurada a infraestrutura executável do Alembic.
- Fixadas versões compatíveis de todas as dependências diretas.
- Eliminadas colisões de refresh token com a inclusão de `jti`.
- Concluído o envio de recuperação de senha por adapter SMTP, sem expor tokens em logs.
- Substituídas exceções genéricas por erros de domínio e respostas HTTP apropriadas.
- Isolados os bancos de teste e ampliado o fluxo E2E para todos os endpoints AUTH da Sprint 01.

## [0.1.0] - 2024-05-23

### Added
- **Capability: Authentication (AUTH)**
  - Implementado fluxo completo de autenticação:
    - Cadastro de Usuário (RF-AUTH-001)
    - Login com JWT (Access e Refresh Tokens) (RF-AUTH-002)
    - Logout invalidando sessão (RF-AUTH-003)
    - Recuperação de Senha (RF-AUTH-004)
    - Redefinição de Senha (RF-AUTH-005)
- **Capability: Character (CHAR)**
  - Implementada criação atômica de `Player` e `Character` durante o registro do usuário.
- **Architecture:**
  - Estabelecida a fundação arquitetural do projeto com estrutura de diretórios revisada.
  - Introduzido diretório `shared` para código comum.
  - Implementado padrão CQRS simples (Commands/Handlers).
  - Implementado `EventBus` em memória e `UnitOfWork` para gerenciamento de transações e eventos.
  - Oficializado o uso de **TSID** como padrão de identificadores.
  - Criada a estrutura de persistência com SQLAlchemy e Alembic.
  - Implementado o `Composition Root` e injeção de dependências com FastAPI.
  - Adotado o `lifespan` do FastAPI para o ciclo de vida da aplicação.

### Fixed
- Garantida a criação atômica de User, Player e Character em uma única transação.
- Corrigido o fluxo de publicação de eventos para ocorrer apenas após o commit bem-sucedido.
- Centralizada a configuração do banco de dados em `app/shared/infrastructure/database.py`.
- Removido o uso do decorador obsoleto `@app.on_event("startup")`.
- Corrigidos e limpos os imports e as dependências do projeto.
