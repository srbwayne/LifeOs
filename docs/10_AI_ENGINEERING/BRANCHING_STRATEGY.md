# BRANCHING_STRATEGY.md

> Política oficial de estratégia de branches do projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os desenvolvedores e agentes de Inteligência Artificial.

---

# 1. Objetivo

Este documento define a estratégia oficial de utilização de branches no repositório do **LifeOS**.

Seu objetivo é garantir que o histórico do projeto permaneça:

- organizado;
- previsível;
- rastreável;
- auditável;
- compatível com a arquitetura do sistema.

A estratégia de branches deverá permitir que múltiplos desenvolvedores e agentes de IA trabalhem simultaneamente sem comprometer a estabilidade da aplicação.

---

# 2. Escopo

Esta política aplica-se a:

- desenvolvedores;
- Tech Leads;
- Arquitetos de Software;
- revisores técnicos;
- agentes de Inteligência Artificial;
- pipelines de CI/CD;
- todo o repositório oficial do LifeOS.

Todos os commits deverão seguir esta estratégia.

---

# 3. Documentos Relacionados

Esta política complementa os seguintes documentos:

- COMMIT_GUIDELINES.md
- VERSIONING.md
- DEFINITION_OF_DONE.md
- DEVELOPMENT_WORKFLOW.md
- CODE_REVIEW_CHECKLIST.md
- DEPENDENCY_POLICY.md

Nenhuma regra deste documento substitui os documentos acima.

---

# 4. Princípios

A estratégia de branches do LifeOS baseia-se nos seguintes princípios.

## 4.1. Branches Curtas

Toda branch deverá possuir vida curta.

Branches muito longas aumentam:

- conflitos;
- retrabalho;
- divergências;
- dificuldade de revisão.

Sempre que possível, uma branch deverá representar apenas uma entrega.

---

## 4.2. Commits Atômicos

Cada commit deverá representar apenas uma alteração lógica.

Não é permitido misturar:

- novas funcionalidades;
- correções;
- documentação;
- refatorações;
- alterações de dependências;

no mesmo commit sem justificativa.

As regras completas encontram-se em **COMMIT_GUIDELINES.md**.

---

## 4.3. Histórico Limpo

O histórico do Git deverá ser legível.

Ao analisar a linha do tempo do projeto deve ser possível identificar:

- Sprint;
- Capability;
- Feature;
- RF;
- ADR;
- motivo de cada alteração.

---

## 4.4. Main Sempre Estável

A branch **main** deverá permanecer estável durante todo o ciclo de desenvolvimento.

Ela nunca deverá conter:

- código incompleto;
- funcionalidades parcialmente implementadas;
- testes quebrados;
- migrations inválidas;
- documentação inconsistente.

---

## 4.5. Integração Contínua

Toda alteração deverá ser integrada continuamente.

Evitar branches que permaneçam semanas sem sincronização.

Sempre que necessário, realizar:

- atualização da branch;
- resolução de conflitos;
- execução dos testes.

---

## 4.6. Revisão Obrigatória

Nenhuma alteração significativa deverá chegar à branch principal sem revisão técnica.

A revisão deverá seguir o documento:

**CODE_REVIEW_CHECKLIST.md**

---

# 5. Estratégia Oficial

O LifeOS adota oficialmente uma estratégia baseada no **GitHub Flow**, adaptada para projetos com arquitetura modular e desenvolvimento assistido por Inteligência Artificial.

Essa estratégia foi escolhida por proporcionar:

- simplicidade;
- baixo custo operacional;
- integração contínua;
- facilidade de automação;
- histórico limpo.

Não será utilizado o Git Flow tradicional.

---

# 6. Branch Principal

A branch principal do projeto será:

```text
main
```

A branch **main** representa a versão oficial do projeto.

Estado transitório: o repositório ainda utiliza `master`. A migração real para
`main` está aprovada para a Fase 3; até sua execução, esta política mantém
`main` como nome normativo futuro sem alterar a configuração atual.

Ela deverá refletir sempre um estado:

- compilável;
- testado;
- documentado;
- rastreável.

---

## Regras

É proibido:

- desenvolver diretamente na main;
- realizar commits locais diretamente na main;
- utilizar force push;
- ignorar revisão técnica;
- publicar código experimental.

Toda alteração deverá chegar à main através do fluxo oficial.

---

# 7. Tipos Oficiais de Branch

O LifeOS adota os seguintes tipos de branches.

| Prefixo | Finalidade |
|----------|------------|
| feature/ | Novas funcionalidades |
| bugfix/ | Correções de defeitos |
| hotfix/ | Correções críticas em produção |
| refactor/ | Refatorações |
| docs/ | Documentação |
| test/ | Testes |
| build/ | Build e dependências |
| infra/ | Infraestrutura |
| security/ | Segurança |
| perf/ | Performance |
| spike/ | Estudos e protótipos |
| release/ | Preparação de Releases |

Somente esses prefixos deverão ser utilizados.

---

# 8. Convenção de Nomenclatura

Toda branch deverá seguir o formato:

```text
tipo/nome-curto
```

## Exemplos

### Feature

```text
feature/auth-login
feature/auth-refresh-token
feature/character-profile
feature/game-xp-engine
feature/workout-tracker
```

### Bugfix

```text
bugfix/auth-token
bugfix/password-reset
bugfix/character-query
```

### Hotfix

```text
hotfix/jwt-expiration
hotfix/security-password-reset
```

### Refactor

```text
refactor/auth-service
refactor/shared-kernel
refactor/game-engine
```

### Documentação

```text
docs/versioning
docs/prd
docs/rf-game
docs/code-review
```

### Testes

```text
test/auth
test/character
test/game
```

### Build

```text
build/dependencies
build/python312
build/pytest
```

### Infraestrutura

```text
infra/docker
infra/github-actions
infra/nginx
```

### Segurança

```text
security/jwt
security/authorization
security/password-policy
```

### Performance

```text
perf/database
perf/query-optimization
perf/cache
```

### Spike

```text
spike/event-sourcing
spike/langgraph
spike/openai-agents
```

### Release

```text
release/0.4.0
release/1.0.0
```

---

## Nomes Proibidos

É proibido criar branches com nomes genéricos ou sem significado.

Exemplos:

```text
teste
teste2
nova
branch
correcao
joao
maria
temp
tmp
backup
```

Toda branch deverá permitir identificar claramente seu propósito.

---

# 9. Fluxo Oficial de Desenvolvimento

Toda alteração deverá seguir o fluxo oficial de desenvolvimento definido para o LifeOS.

O objetivo é garantir:

- histórico limpo;
- integração contínua;
- revisões técnicas consistentes;
- rastreabilidade completa;
- estabilidade da branch principal.

## Fluxo Oficial

1. Atualizar a branch `main`.
2. Criar uma nova branch a partir da `main`.
3. Implementar a alteração.
4. Executar os testes obrigatórios.
5. Atualizar a documentação quando necessário.
6. Criar commits seguindo o padrão oficial.
7. Atualizar a branch com a `main`, caso necessário.
8. Abrir Pull Request.
9. Executar Code Review.
10. Aprovar a alteração.
11. Realizar Merge.
12. Remover a branch.

Nenhuma etapa deverá ser ignorada.

---

# 10. Criação de Branches

Toda nova branch deverá ser criada a partir da versão mais recente da `main`.

## Procedimento

1. Atualizar a branch principal.
2. Garantir que a `main` esteja sincronizada.
3. Criar a nova branch.
4. Confirmar o nome conforme esta política.

Exemplo:

```bash
git checkout main
git pull origin main
git checkout -b feature/auth-login
```

É proibido criar branches a partir de outras branches de Feature, salvo autorização explícita do Arquiteto de Software.

---

# 11. Atualização de Branches

Branches deverão permanecer sincronizadas com a `main`.

Atualizações frequentes reduzem:

- conflitos;
- retrabalho;
- regressões;
- problemas de integração.

Sempre que uma branch permanecer aberta por período prolongado, deverá ser atualizada.

## Estratégia recomendada

Utilizar Rebase para manter o histórico linear.

Exemplo:

```bash
git fetch origin
git rebase origin/main
```

Caso ocorram conflitos, eles deverão ser resolvidos antes da continuação do desenvolvimento.

---

# 12. Merge

Toda integração com a `main` deverá ocorrer através de Pull Request.

Não será permitido merge direto.

## Estratégias Permitidas

### Rebase and Merge

Estratégia padrão quando os commits estiverem atômicos e conformes com
`docs/10_AI_ENGINEERING/COMMIT_GUIDELINES.md`. Esses commits deverão ser
preservados no histórico.

Resultado:

- histórico limpo;
- commits atômicos preservados.

### Squash Merge

Permitido somente quando existirem commits temporários, intermediários ou não
conformes que não devam permanecer no histórico.

## Estratégia Proibida

Não utilizar Merge Commit automático sem justificativa.

Esse tipo de merge tende a poluir o histórico do projeto.

---

# 13. Rebase

O Rebase é a estratégia preferencial para atualização de branches.

Benefícios:

- histórico linear;
- menor quantidade de Merge Commits;
- revisão mais simples;
- rastreabilidade facilitada.

## Quando utilizar

Antes da abertura do Pull Request.

Sempre que houver alterações relevantes na `main`.

Antes do Merge final.

## Quando evitar

Nunca realizar Rebase sobre branches já compartilhadas quando isso puder impactar outros desenvolvedores sem alinhamento prévio.

---

# 14. Proteção da Branch Main

A branch `main` deverá possuir proteção obrigatória.

## Não será permitido

- Push direto.
- Force Push.
- Exclusão da branch.
- Merge sem Pull Request.
- Merge sem revisão.
- Merge com testes obrigatórios falhando.
- Merge com conflitos não resolvidos.

## Obrigatório

- Pull Request aprovado.
- Testes aprovados.
- Revisão técnica concluída.
- Documentação atualizada quando aplicável.

A branch `main` representa o estado oficial do projeto.

---

# 15. Pull Requests

Todo código deverá ser integrado através de Pull Request.

O Pull Request deverá possuir:

- objetivo claro;
- escopo limitado;
- descrição completa;
- referência à Sprint;
- referência à Capability;
- referência à Feature;
- referência aos RFs;
- referência aos ADRs quando aplicável.

## Estrutura recomendada

### Objetivo

Descrição resumida da alteração.

### Escopo

O que foi implementado.

### Testes Executados

Lista dos testes realizados.

### Documentação

Arquivos atualizados.

### Checklist

Confirmação dos critérios obrigatórios.

---

# 16. Relação entre Branches e Capabilities

Sempre que possível, uma branch deverá estar associada a uma única Capability.

## Exemplos

### Authentication

```text
feature/auth-login
feature/auth-register
feature/auth-refresh-token
```

### Character

```text
feature/character-profile
feature/character-query
```

### Health

```text
feature/health-records
```

### Workout

```text
feature/workout-session
```

### Reading

```text
feature/reading-books
```

### Therapy

```text
feature/therapy-sessions
```

### Habits

```text
feature/habit-tracking
```

### Game Engine

```text
feature/game-level-engine
feature/game-xp-engine
feature/game-achievements
```

Uma branch não deverá misturar alterações pertencentes a múltiplas Capabilities, salvo quando a mudança for transversal e previamente aprovada.

---

# 17. Branches por Sprint

Em situações específicas, poderá ser criada uma branch para representar uma Sprint completa.

Essa abordagem deverá ser utilizada apenas quando houver necessidade de coordenação entre múltiplas Features antes da integração com a `main`.

## Objetivos

- consolidar entregas da Sprint;
- facilitar homologação;
- organizar validações integradas.

## Convenção

```text
sprint/<numero>-<descricao>
```

## Exemplos

```text
sprint/03-health
sprint/08-game-engine
```

Após a conclusão da Sprint, a branch deverá ser removida.

---

# 18. Branches por Requisito Funcional

Quando um Requisito Funcional possuir grande complexidade ou demandar vários dias de implementação, poderá ser criada uma branch específica.

## Convenção

```text
feature/rf-<identificador>
```

## Exemplos

```text
feature/rf-auth-001
feature/rf-char-003
feature/rf-game-021
```

Essa estratégia melhora a rastreabilidade entre:

- branch;
- commits;
- Pull Request;
- Feature;
- RF;
- testes.

---

# 19. Branches Experimentais

Branches experimentais destinam-se exclusivamente a estudos, provas de conceito e avaliações técnicas.

Seu conteúdo não deverá ser considerado código de produção.

## Convenção

```text
spike/<descricao>
```

## Exemplos

```text
spike/event-sourcing
spike/langgraph
spike/openai-agents
spike/vector-search
```

## Regras

Branches experimentais:

- não deverão gerar Releases;
- não deverão ser integradas diretamente à `main`;
- deverão possuir documentação técnica quando produzirem conclusões relevantes.

Caso uma prova de conceito seja aprovada, uma nova branch de Feature deverá ser criada.

---

# 20. Branches de Documentação

Alterações exclusivamente documentais deverão ocorrer em branches específicas.

## Convenção

```text
docs/<descricao>
```

## Exemplos

```text
docs/prd
docs/versioning
docs/branching-strategy
docs/game-engine
docs/rf-admin
```

## Escopo

Essas branches destinam-se a:

- documentação;
- ADRs;
- PRD;
- RFs;
- guias técnicos;
- documentação arquitetural.

Não deverão conter alterações funcionais.

---

# 21. Branches de Refatoração

Refatorações deverão ocorrer em branches próprias.

## Convenção

```text
refactor/<descricao>
```

## Exemplos

```text
refactor/auth-service
refactor/shared-kernel
refactor/game-engine
refactor/repositories
```

## Objetivos

Essas branches destinam-se a:

- melhoria estrutural;
- simplificação de código;
- redução de dívida técnica;
- melhoria arquitetural.

Não deverão alterar comportamento funcional sem aprovação prévia.

---

# 22. Branches de Infraestrutura

Alterações relacionadas ao ambiente de execução deverão utilizar branches específicas.

## Convenção

```text
infra/<descricao>
```

## Exemplos

```text
infra/docker
infra/nginx
infra/github-actions
infra/devcontainer
infra/database
```

## Escopo

Incluem:

- Docker;
- CI/CD;
- GitHub Actions;
- configuração de servidores;
- ambientes de desenvolvimento;
- infraestrutura de banco de dados.

---

# 23. Branches de Segurança

Alterações relacionadas à segurança deverão ocorrer em branches dedicadas.

## Convenção

```text
security/<descricao>
```

## Exemplos

```text
security/jwt
security/password-policy
security/authorization
security/oauth
```

## Escopo

Incluem:

- autenticação;
- autorização;
- criptografia;
- políticas de senha;
- vulnerabilidades;
- auditoria de segurança.

Alterações dessa categoria deverão passar por revisão técnica obrigatória.

---

# 24. Branches de Performance

Melhorias de desempenho deverão utilizar branches específicas.

## Convenção

```text
perf/<descricao>
```

## Exemplos

```text
perf/database
perf/cache
perf/query-optimization
perf/indexes
```

## Escopo

Incluem:

- otimização de consultas;
- cache;
- índices;
- redução de consumo de memória;
- redução de tempo de resposta;
- otimização de algoritmos.

Toda melhoria de performance deverá ser acompanhada por evidências mensuráveis, como benchmarks ou métricas comparativas.

---

# 25. Branches Proibidas

Para manter a organização do repositório, alguns padrões de nomenclatura são proibidos.

## Não utilizar

```text
teste
teste2
novo
branch
temp
tmp
backup
joao
maria
dev
codigo
```

Também não deverão ser utilizados:

- nomes genéricos;
- nomes pessoais;
- datas como identificador principal;
- descrições ambíguas;
- abreviações sem significado.

## Regras

Toda branch deverá:

- possuir um prefixo oficial;
- descrever claramente seu objetivo;
- possuir rastreabilidade com a alteração realizada.

---

# 26. Fluxo para Agentes de Inteligência Artificial

Os agentes de Inteligência Artificial deverão seguir exatamente o mesmo fluxo aplicado aos desenvolvedores.

Nenhum agente poderá realizar alterações diretamente na branch principal.

## Fluxo Oficial

1. Atualizar a branch `main`.
2. Criar uma nova branch.
3. Implementar a alteração.
4. Executar todos os testes obrigatórios.
5. Atualizar a documentação.
6. Produzir evidências da execução.
7. Criar commits seguindo `COMMIT_GUIDELINES.md`.
8. Abrir Pull Request.
9. Aguardar revisão técnica.
10. Realizar Merge somente após aprovação.

## Regras

Os agentes deverão:

- respeitar a arquitetura oficial;
- respeitar os limites entre Capabilities;
- não modificar documentação sem autorização;
- não alterar requisitos funcionais;
- não criar migrations desnecessárias;
- não alterar versões automaticamente;
- não criar Tags Git.

Toda alteração produzida por IA deverá ser auditável.

---

# 27. Checklist para Merge

Antes da aprovação de um Pull Request, todos os itens abaixo deverão estar concluídos.

## Código

- [ ] Compila corretamente.
- [ ] Sem erros de importação.
- [ ] Sem TODOs críticos.
- [ ] Sem FIXME críticos.
- [ ] Sem código morto.

---

## Arquitetura

- [ ] Clean Architecture preservada.
- [ ] DDD preservado.
- [ ] Dependências respeitam `DEPENDENCY_POLICY.md`.
- [ ] Nenhuma violação arquitetural.

---

## Banco de Dados

- [ ] Migrations criadas quando necessárias.
- [ ] Migrations testadas.
- [ ] Schema consistente.

---

## Testes

- [ ] Testes unitários.
- [ ] Testes de integração.
- [ ] Testes E2E.
- [ ] Testes arquiteturais.
- [ ] Cobertura dentro da meta.

---

## Documentação

- [ ] CHANGELOG atualizado.
- [ ] PROJECT_STATUS atualizado.
- [ ] TASK_HISTORY atualizado.
- [ ] Documentação da Sprint atualizada.
- [ ] ADR criada quando necessária.

---

## Revisão

- [ ] Code Review aprovado.
- [ ] Nenhuma não conformidade bloqueante.
- [ ] Pull Request aprovado.

---

# 28. Não Conformidades

Um Merge deverá ser bloqueado quando qualquer uma das situações abaixo ocorrer.

## Código

- erros de compilação;
- imports inválidos;
- dependências quebradas;
- código incompleto.

---

## Arquitetura

- violação da Clean Architecture;
- violação das regras de dependência;
- quebra entre Capabilities;
- ausência de ADR obrigatória.

---

## Banco

- migrations inconsistentes;
- alterações sem migration;
- perda de rastreabilidade.

---

## Testes

- testes falhando;
- cobertura abaixo da meta;
- regressões identificadas.

---

## Documentação

- documentação desatualizada;
- CHANGELOG inconsistente;
- PROJECT_STATUS desatualizado;
- TASK_HISTORY desatualizado.

Enquanto existir qualquer não conformidade bloqueante, o Pull Request não poderá ser aprovado.

---

# 29. Auditoria

Toda branch deverá permitir auditoria completa.

A qualquer momento deverá ser possível identificar:

- quem criou a branch;
- quando foi criada;
- qual Sprint representa;
- qual Capability foi alterada;
- quais Features foram implementadas;
- quais RFs foram atendidos;
- quais ADRs foram utilizados;
- quais testes foram executados;
- quais migrations foram criadas;
- quais documentos foram alterados.

Toda alteração deverá possuir rastreabilidade entre:

- Branch;
- Commits;
- Pull Request;
- Sprint;
- Capability;
- Feature;
- Requisito Funcional;
- Testes;
- Release.

---

# 30. Regra Final

A estratégia de branches do LifeOS existe para preservar:

- qualidade;
- organização;
- previsibilidade;
- rastreabilidade;
- estabilidade;
- colaboração.

Nenhuma branch deverá existir sem um objetivo claramente definido.

Toda branch deverá representar uma unidade lógica de trabalho, possuir escopo limitado e permanecer aberta pelo menor tempo possível.

A branch `main` deverá representar continuamente a versão oficial do projeto, mantendo-se compilável, testada, documentada e pronta para evoluir de forma segura.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial de estratégia de branches do LifeOS. |
