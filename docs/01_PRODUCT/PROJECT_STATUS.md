# Project Status

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
