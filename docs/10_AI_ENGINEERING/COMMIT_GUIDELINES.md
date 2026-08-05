# COMMIT_GUIDELINES.md

> Padrão oficial de criação, organização e rastreabilidade dos commits do projeto LifeOS.

Versão: 1.0
Status: Ativo
Aplicação: Obrigatória para desenvolvedores humanos e agentes de Inteligência Artificial

---

# 1. Objetivo

Este documento define o padrão oficial para mensagens, conteúdo e organização dos commits do LifeOS.

Todo commit deverá ser:

- claro;
- atômico;
- rastreável;
- reversível;
- relacionado a uma única responsabilidade;
- compatível com o histórico arquitetural e funcional do projeto.

Os commits fazem parte da documentação técnica do LifeOS.

O histórico Git deverá permitir compreender:

- o que foi alterado;
- por que foi alterado;
- qual Capability foi afetada;
- qual Sprint autorizou a alteração;
- qual Feature originou a mudança;
- qual Requisito Funcional foi atendido;
- qual decisão arquitetural justificou a implementação;
- quais testes validam o comportamento.

---

# 2. Escopo

Estas diretrizes aplicam-se a:

- novas funcionalidades;
- correções de bugs;
- refatorações;
- alterações arquiteturais;
- testes;
- documentação;
- migrations;
- dependências;
- segurança;
- performance;
- automações;
- infraestrutura;
- configuração;
- reversões.

Nenhuma alteração versionada está dispensada deste padrão.

---

# 3. Princípios Fundamentais

## 3.1. Um commit representa uma responsabilidade

Cada commit deverá possuir um propósito único e claramente identificável.

Exemplo correto:

```text
feat(character): add authenticated character query
```

Exemplo incorreto:

```text
feat: add character query, update docs, refactor auth and fix database
```

---

## 3.2. Um commit deve ser compreensível isoladamente

A mensagem deverá explicar suficientemente a alteração sem exigir a leitura completa do diff.

---

## 3.3. Um commit deve ser reversível

Sempre que possível, um commit deverá poder ser revertido sem remover alterações não relacionadas.

---

## 3.4. Um commit deve manter o projeto válido

Após cada commit:

- o projeto deverá instalar;
- os imports deverão funcionar;
- os testes relacionados deverão passar;
- a arquitetura deverá permanecer válida;
- o código não deverá permanecer propositalmente quebrado.

Commits intermediários quebrados não deverão ser enviados para branches compartilhadas.

---

## 3.5. Evidência prevalece sobre declaração

Não é permitido afirmar na mensagem que algo foi validado sem executar a validação correspondente.

---

## 3.6. Rastreabilidade é obrigatória

Toda alteração funcional deverá estar vinculada a uma Sprint, Feature ou Requisito Funcional.

Toda alteração arquitetural deverá estar vinculada a um ADR, quando aplicável.

---

# 4. Formato Oficial

A mensagem de commit seguirá o formato:

```text
<tipo>(<escopo>): <resumo>

<corpo opcional>

Sprint: <SPR-XXX>
Capability: <CAPABILITY>
Feature: <FEATURE-ID>
RF: <RF-ID>
ADR: <ADR-ID>
Tests: <comandos ou resumo>
```

Nem todos os metadados são obrigatórios em todos os commits.

O cabeçalho é sempre obrigatório.

---

# 5. Estrutura do Cabeçalho

```text
<tipo>(<escopo>): <resumo>
```

Exemplo:

```text
feat(character): add read-only character profile query
```

---

# 6. Tipos Permitidos

## `feat`

Nova funcionalidade ou novo comportamento funcional.

```text
feat(auth): add refresh token rotation
```

---

## `fix`

Correção de comportamento incorreto.

```text
fix(character): enforce authenticated ownership filter
```

---

## `refactor`

Alteração interna sem mudança intencional de comportamento externo.

```text
refactor(shared): move UserId to shared kernel
```

---

## `test`

Criação, atualização ou correção de testes.

```text
test(character): add cross-user isolation coverage
```

---

## `docs`

Alterações exclusivamente documentais.

```text
docs(product): align Character and Game capability boundaries
```

---

## `perf`

Melhoria de performance sem mudança funcional relevante.

```text
perf(character): reduce repository query round trips
```

---

## `build`

Alterações no processo de build, empacotamento ou dependências.

```text
build(dependencies): add pytest-cov
```

---

## `ci`

Alterações relacionadas à integração contínua.

```text
ci(github): add test workflow
```

---

## `style`

Alterações de formatação sem impacto funcional.

```text
style(auth): normalize import ordering
```

---

## `chore`

Atividades de manutenção que não se enquadram nos demais tipos.

```text
chore(project): remove obsolete local artifacts
```

---

## `security`

Correções ou melhorias diretamente relacionadas à segurança.

```text
security(auth): revoke sessions after password reset
```

---

## `revert`

Reversão explícita de um commit anterior.

```text
revert(character): revert profile projection change
```

---

# 7. Tipos Proibidos

Não utilizar tipos genéricos ou sem significado técnico.

Exemplos proibidos:

```text
update
change
changes
adjust
adjustment
improvement
new
commit
misc
temp
final
work
wip
```

Também são proibidas mensagens como:

```text
fix
update files
ajustes
melhorias
alterações
funcionando
versão final
commit final
teste
novo código
```

---

# 8. Escopos Oficiais

O escopo identifica a área principal impactada.

## Capabilities

```text
auth
character
health
workout
reading
therapy
habits
game
dashboard
analytics
ai
reports
admin
```

## Escopos transversais

```text
shared
database
migrations
dependencies
architecture
product
tests
docs
ci
project
security
```

## Regras

O escopo deverá:

- ser escrito em minúsculas;
- representar a principal responsabilidade alterada;
- evitar nomes de arquivos;
- evitar nomes genéricos como `core`, salvo quando oficialmente definido.

Exemplo correto:

```text
fix(auth): reject reused refresh token
```

Exemplo incorreto:

```text
fix(token_service.py): fix token
```

---

# 9. Resumo do Commit

O resumo deverá:

- utilizar verbo no imperativo;
- começar com letra minúscula;
- não terminar com ponto;
- ser objetivo;
- explicar o resultado da alteração;
- possuir, preferencialmente, até 72 caracteres.

Exemplos:

```text
feat(character): expose authenticated profile query
```

```text
fix(auth): prevent refresh token reuse
```

```text
refactor(shared): centralize user identifier
```

Evitar:

```text
feat(character): profile
```

```text
fix(auth): bug fix
```

```text
refactor: several improvements
```

---

# 10. Corpo do Commit

O corpo é recomendado quando a alteração não for evidente pelo cabeçalho.

Ele deverá explicar:

- o contexto;
- o problema;
- a solução adotada;
- os impactos;
- eventuais restrições;
- decisões relevantes.

Exemplo:

```text
refactor(shared): centralize user identifier

Move UserId from AUTH internals to the Shared Kernel so other
capabilities can reference the authenticated user without creating
cross-capability domain dependencies.

No database schema or HTTP contract was changed.
```

---

# 11. Rodapé de Rastreabilidade

## Sprint

Obrigatório para alterações realizadas dentro de uma Sprint.

```text
Sprint: SPR-002
```

---

## Capability

Obrigatório para alterações funcionais ou de domínio.

```text
Capability: CHAR
```

---

## Feature

Obrigatório quando a alteração estiver vinculada a uma Feature.

```text
Feature: CHAR-002
```

Múltiplas Features deverão ser evitadas no mesmo commit.

Quando inevitável:

```text
Feature: CHAR-002, CHAR-003
```

---

## Requisito Funcional

Obrigatório quando a alteração implementar ou corrigir um RF.

```text
RF: RF-CHAR-002
```

Quando não aplicável:

```text
RF: N/A
```

---

## ADR

Obrigatório para alterações orientadas por decisão arquitetural formal.

```text
ADR: ADR-001
```

Quando não existir ADR:

```text
ADR: N/A
```

---

## Testes

Informar a validação executada quando relevante.

```text
Tests: python -m pytest tests/character -v
```

ou:

```text
Tests: 8 passed
```

Não informar testes que não foram realmente executados.

---

# 12. Exemplos Oficiais

## Nova funcionalidade

```text
feat(character): add current character query

Implement the authenticated query used to retrieve the Character
associated with the current user.

Sprint: SPR-002
Capability: CHAR
Feature: CHAR-002
RF: RF-CHAR-002
ADR: ADR-002
Tests: python -m pytest tests/character -v
```

---

## Correção de bug

```text
fix(auth): reject revoked refresh sessions

Prevent revoked sessions from generating new access tokens and update
the session validation flow.

Sprint: SPR-001
Capability: AUTH
Feature: AUTH-003
RF: RF-AUTH-003
ADR: N/A
Tests: python -m pytest tests/auth -v
```

---

## Refatoração arquitetural

```text
refactor(shared): move UserId to shared kernel

Remove the direct dependency from CHAR Domain to AUTH Domain by
centralizing the cross-capability identifier in the Shared Kernel.

Sprint: SPR-002
Capability: SHARED
Feature: N/A
RF: N/A
ADR: ADR-001
Tests: python -m pytest -v
```

---

## Testes

```text
test(character): add capability isolation architecture rule

Add an architecture test that rejects direct imports between the
domain layers of different capabilities.

Sprint: SPR-002
Capability: CHAR
Feature: N/A
RF: N/A
ADR: ADR-001
Tests: python -m pytest tests/architecture -v
```

---

## Documentação

```text
docs(product): move XP ownership to Game capability

Align Feature Catalog, PRD and Capability Map with the official
boundary between Character and Game Engine.

Sprint: SPR-002
Capability: GAME
Feature: GAME-001
RF: RF-GAME-006
ADR: ADR-002
Tests: N/A
```

---

## Dependências

```text
build(dependencies): add coverage tooling

Declare pytest-cov in requirements.txt and pyproject.toml and validate
the installation in a clean environment.

Sprint: SPR-002
Capability: SHARED
Feature: N/A
RF: N/A
ADR: N/A
Tests: python -m pip check
```

---

## Migration

```text
feat(migrations): create health records table

Add the new health persistence structure without modifying previously
applied migrations.

Sprint: SPR-003
Capability: HEALTH
Feature: HEALTH-001
RF: RF-HEALTH-001
ADR: N/A
Tests: python -m alembic upgrade head
```

---

## Segurança

```text
security(auth): hash password reset tokens

Persist only token hashes and prevent tokens from being reused after
successful password reset.

Sprint: SPR-001
Capability: AUTH
Feature: AUTH-005
RF: RF-AUTH-005
ADR: N/A
Tests: python -m pytest tests/auth -v
```

---

# 13. Commits Atômicos

Um commit atômico representa uma única alteração lógica.

## Correto

```text
feat(character): add CharacterId value object
```

```text
feat(character): add current character query
```

```text
test(character): add query handler tests
```

```text
docs(project): update Sprint 02 status
```

## Incorreto

```text
feat(character): implement entire Sprint 02
```

Esse commit mistura domínio, aplicação, infraestrutura, API, testes e documentação.

---

# 14. Separação Recomendada por Responsabilidade

Uma funcionalidade poderá ser dividida em commits como:

```text
feat(character): add CharacterId value object
```

```text
feat(character): evolve Character aggregate
```

```text
feat(character): add repository query contract
```

```text
feat(character): implement SQLAlchemy character query
```

```text
feat(character): expose character profile endpoint
```

```text
test(character): cover character profile flow
```

```text
docs(project): record Sprint 02 delivery
```

Essa divisão facilita:

- revisão;
- rollback;
- auditoria;
- investigação de regressões;
- compreensão histórica.

---

# 15. Tamanho dos Commits

Não existe limite fixo de linhas.

O tamanho é determinado pela responsabilidade.

Um commit está grande demais quando:

- possui mais de um objetivo;
- exige múltiplos verbos no resumo;
- mistura refatoração e funcionalidade;
- mistura correção e nova Feature;
- mistura Capabilities independentes;
- não pode ser revertido isoladamente;
- exige uma mensagem excessivamente genérica.

---

# 16. Estado do Projeto em Cada Commit

Antes de criar um commit, o agente deverá confirmar:

- [ ] O código compila ou importa corretamente.
- [ ] Os testes relacionados foram executados.
- [ ] Nenhum teste anteriormente aprovado foi quebrado.
- [ ] Nenhuma dependência necessária ficou ausente.
- [ ] Nenhum segredo foi incluído.
- [ ] Nenhum arquivo local foi incluído indevidamente.
- [ ] A arquitetura permanece válida.
- [ ] A mensagem segue este documento.

---

# 17. Relação entre Código e Testes

A preferência oficial é:

```text
Implementação pequena
↓
Testes correspondentes
↓
Commit validado
```

Quando o teste fizer parte inseparável da alteração, código e teste poderão estar no mesmo commit.

Exemplo:

```text
fix(auth): prevent token reuse
```

Incluindo:

- correção;
- teste de regressão.

Quando os testes representarem uma entrega independente ou ampla, utilizar commit separado:

```text
test(auth): expand refresh token regression coverage
```

---

# 18. Relação entre Código e Documentação

Documentação funcional ou arquitetural significativa deverá, preferencialmente, possuir commit próprio.

Exemplo:

```text
docs(architecture): record shared UserId decision
```

Atualizações operacionais diretamente relacionadas à entrega poderão ocorrer no commit final da Sprint:

```text
docs(project): close Sprint 02
```

---

# 19. Relação entre Código e Migrations

Migrations deverão ser criadas em commits identificáveis.

Quando a migration for inseparável da implementação:

```text
feat(health): persist sleep records
```

Quando for relevante isoladamente:

```text
feat(migrations): create sleep records table
```

É proibido:

- alterar migrations já aplicadas;
- esconder alterações de schema em commits genéricos;
- criar migrations sem validar upgrade;
- criar migrations sem downgrade quando tecnicamente possível.

---

# 20. Commits de Correção após Revisão

Quando uma revisão técnica identificar um problema, o commit deverá explicar a origem da correção.

Exemplo:

```text
fix(character): remove cross-capability domain dependency

Move UserId to the Shared Kernel after architecture review identified
a direct dependency from CHAR Domain to AUTH Domain.

Sprint: SPR-002
Capability: CHAR
Feature: N/A
RF: N/A
ADR: ADR-001
Tests: python -m pytest -v
```

Não utilizar:

```text
fix review
```

ou:

```text
address comments
```

---

# 21. Breaking Changes

Mudanças incompatíveis deverão utilizar `!` no cabeçalho:

```text
feat(auth)!: replace session token contract
```

E incluir:

```text
BREAKING CHANGE: refresh responses no longer return the previous token format.
```

Breaking Changes exigem:

- aprovação arquitetural;
- documentação;
- migration ou estratégia de compatibilidade;
- atualização de versão MAJOR quando aplicável;
- testes de regressão.

---

# 22. Reversões

Reversões deverão identificar o commit revertido.

```text
revert(character): revert profile projection optimization

Reverts: abc1234

Reason: the optimized query broke tenant isolation.
```

Nunca apagar o histórico para esconder uma decisão incorreta.

---

# 23. Commits Temporários

Commits como estes não deverão ser enviados à branch compartilhada:

```text
wip
temp
debug
trying
almost done
```

Durante trabalho local, poderão existir provisoriamente, mas deverão ser reorganizados antes do push por meio de:

- squash;
- fixup;
- rebase interativo;
- recriação organizada dos commits.

---

# 24. Commits Gerados por Agentes de IA

Todo agente deverá:

1. Ler este documento antes de criar commits.
2. Exibir previamente os commits planejados.
3. Informar quais arquivos entrarão em cada commit.
4. Executar as validações correspondentes.
5. Criar commits apenas após validação real.
6. Não agrupar toda a Sprint em um único commit.
7. Não alterar histórico remoto sem autorização.
8. Não usar `--force` sem aprovação explícita.
9. Não declarar commit criado sem apresentar seu SHA.
10. Não fazer push de segredos ou artefatos locais.

---

# 25. Plano de Commits

Antes de implementar uma tarefa relevante, o agente deverá apresentar um plano semelhante a:

```text
Commit 1
refactor(shared): move UserId to shared kernel

Arquivos:
- app/shared/domain/identifiers/user_id.py
- app/auth/domain/value_objects/user_id.py
- app/character/domain/aggregates/player.py

Validação:
- python -m pytest tests/auth tests/character -v
```

```text
Commit 2
test(architecture): prevent cross-capability domain imports

Arquivos:
- tests/architecture/test_dependency_rules.py

Validação:
- python -m pytest tests/architecture -v
```

```text
Commit 3
fix(character): use timezone-aware timestamps

Arquivos:
- app/character/domain/aggregates/player.py
- app/character/domain/aggregates/character.py
- tests/character/domain/

Validação:
- python -m pytest tests/character -v
```

---

# 26. Ordem Recomendada Durante uma Sprint

```text
Planejamento
↓
Fundação ou contratos
↓
Domínio
↓
Application
↓
Infrastructure
↓
Presentation
↓
Testes
↓
Documentação
↓
Encerramento
```

A ordem poderá variar quando houver justificativa técnica.

---

# 27. Proibições

É proibido:

- criar um único commit para toda a Sprint;
- usar mensagens vagas;
- misturar Capabilities sem justificativa;
- esconder falhas conhecidas;
- criar commits sem testes quando testes forem aplicáveis;
- registrar evidências não executadas;
- incluir arquivos `.env`;
- incluir tokens;
- incluir senhas;
- incluir bancos locais;
- incluir ambientes virtuais;
- modificar migrations aplicadas;
- reescrever histórico remoto sem autorização;
- executar `git push --force` sem autorização explícita;
- criar commits diretamente em branches protegidas quando a estratégia exigir branch específica.

---

# 28. Checklist Antes do Commit

- [ ] A alteração possui uma única responsabilidade.
- [ ] O tipo está correto.
- [ ] O escopo está correto.
- [ ] O resumo é claro.
- [ ] A Sprint foi informada quando aplicável.
- [ ] A Capability foi informada quando aplicável.
- [ ] A Feature foi informada quando aplicável.
- [ ] O RF foi informado quando aplicável.
- [ ] O ADR foi informado quando aplicável.
- [ ] Os testes foram realmente executados.
- [ ] O projeto permanece válido.
- [ ] Nenhum segredo será versionado.
- [ ] Nenhum arquivo local será versionado.
- [ ] O diff foi revisado.
- [ ] O commit pode ser revertido isoladamente.

---

# 29. Checklist Depois do Commit

- [ ] O SHA foi registrado.
- [ ] A mensagem foi conferida.
- [ ] Os arquivos esperados estão no commit.
- [ ] Nenhum arquivo indevido foi incluído.
- [ ] O repositório está no estado esperado.
- [ ] Os testes permanecem aprovados.
- [ ] O próximo incremento está claramente definido.

---

# 30. Formato do Relatório de Commit

O agente deverá apresentar:

```text
Commit:
<sha>

Mensagem:
<mensagem completa>

Arquivos:
- arquivo 1
- arquivo 2

Validações:
- comando
- resultado

Rastreabilidade:
Sprint:
Capability:
Feature:
RF:
ADR:
```

---

# 31. Exemplo de Histórico Ideal

```text
refactor(shared): move UserId to shared kernel
test(architecture): prevent cross-capability domain imports
fix(character): use timezone-aware timestamps
feat(character): add current character query
test(character): add authenticated query coverage
docs(project): close Sprint 02
```

Esse histórico demonstra claramente:

- arquitetura;
- correção;
- funcionalidade;
- testes;
- documentação.

---

# 32. Exemplo de Histórico Inadequado

```text
initial commit
updates
fix
adjustments
final version
more fixes
working now
```

Esse histórico não fornece rastreabilidade, contexto ou segurança para manutenção.

---

# 33. Conformidade

O descumprimento destas diretrizes deverá ser tratado como problema de governança.

Commits fora do padrão poderão ser:

- rejeitados durante revisão;
- reorganizados antes do merge;
- corrigidos por rebase quando ainda não publicados;
- acompanhados por commit corretivo quando já publicados.

---

# 34. Responsabilidades

## Desenvolvedor humano

Responsável por:

- estruturar commits;
- validar o diff;
- garantir a veracidade das evidências;
- preservar o histórico.

## Agente de IA

Responsável por:

- propor o plano de commits;
- seguir o padrão;
- apresentar validações reais;
- informar os SHAs;
- não alterar histórico sem autorização.

## Revisor técnico

Responsável por:

- avaliar atomicidade;
- validar rastreabilidade;
- identificar mistura de responsabilidades;
- aprovar ou solicitar reorganização.

---

# 35. Regra Final

Todo commit do LifeOS deverá responder claramente:

```text
O que mudou?

Por que mudou?

Onde mudou?

Qual requisito autorizou?

Qual decisão arquitetural sustentou?

Como foi validado?
```

Se a mensagem não permitir responder a essas perguntas, o commit não está pronto.