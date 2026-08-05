# VERSIONING.md

> Política oficial de versionamento do projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os desenvolvedores e agentes de Inteligência Artificial.

---

# 1. Objetivo

Este documento define a política oficial de versionamento do projeto **LifeOS**.

Seu objetivo é garantir que toda evolução do sistema seja:

- previsível;
- rastreável;
- reproduzível;
- compatível com a arquitetura;
- alinhada ao Product Roadmap;
- integrada ao processo de desenvolvimento.

O versionamento deverá permitir identificar exatamente:

- o estado do produto;
- as funcionalidades disponíveis;
- os requisitos implementados;
- os riscos conhecidos;
- as mudanças incompatíveis;
- a relação entre código, documentação e banco de dados.

---

# 2. Escopo

Esta política aplica-se a todos os artefatos do LifeOS, incluindo:

- código-fonte;
- APIs;
- banco de dados;
- migrations;
- documentação;
- Capabilities;
- Features;
- Requisitos Funcionais;
- agentes de IA;
- pipelines de integração contínua;
- releases.

---

# 3. Princípios

O versionamento do LifeOS deverá seguir os seguintes princípios.

## 3.1. Rastreabilidade

Toda versão deverá ser rastreável até:

- Sprint;
- Capability;
- Feature;
- Requisito Funcional;
- ADR;
- Commits;
- Pull Request;
- Release.

---

## 3.2. Reprodutibilidade

Qualquer versão publicada deverá poder ser reconstruída utilizando apenas:

- código da tag correspondente;
- migrations oficiais;
- documentação oficial;
- arquivos de dependências.

---

## 3.3. Imutabilidade

Uma versão publicada nunca deverá ser modificada.

Caso seja necessário corrigir uma release, uma nova versão deverá ser criada.

---

## 3.4. Compatibilidade

Mudanças incompatíveis deverão ser:

- documentadas;
- aprovadas;
- registradas em ADR;
- destacadas no CHANGELOG.

---

## 3.5. Simplicidade

O processo de versionamento deverá permanecer simples, previsível e fácil de automatizar.

---

# 4. Semantic Versioning

O LifeOS adota oficialmente o padrão **Semantic Versioning (SemVer)**.

Formato:

**MAJOR.MINOR.PATCH**

Exemplo:

| Componente | Valor |
|------------|------:|
| MAJOR | 1 |
| MINOR | 4 |
| PATCH | 2 |

Versão resultante:

**1.4.2**

---

# 5. Significado das Versões

## 5.1. MAJOR

Incrementar quando ocorrer:

- Breaking Change;
- alteração incompatível de API;
- alteração incompatível de banco;
- alteração incompatível entre Capabilities;
- mudança arquitetural incompatível;
- remoção de contratos públicos.

### Exemplos

| Antes | Depois |
|--------|---------|
| 1.4.2 | 2.0.0 |
| 2.1.5 | 3.0.0 |

---

## 5.2. MINOR

Incrementar quando ocorrer:

- nova Capability;
- nova Feature;
- novo RF;
- novos endpoints compatíveis;
- novos casos de uso;
- novas integrações.

### Exemplos

| Antes | Depois |
|--------|---------|
| 0.2.1 | 0.3.0 |
| 1.8.4 | 1.9.0 |

---

## 5.3. PATCH

Incrementar quando ocorrer:

- correção de bugs;
- refatorações;
- melhorias internas;
- atualização compatível de dependências;
- melhoria de testes;
- documentação;
- otimizações.

### Exemplos

| Antes | Depois |
|--------|---------|
| 0.3.0 | 0.3.1 |
| 2.7.5 | 2.7.6 |

---

# 6. Estratégia do LifeOS

Enquanto o projeto estiver em desenvolvimento, será utilizado:

| Fase | Versão |
|------|---------|
| Fundação | 0.1.x |
| MVP | 0.x.y |
| Primeira versão estável | 1.0.0 |

Durante a fase **0.x**, ainda poderão ocorrer mudanças estruturais relevantes.

Entretanto, toda mudança incompatível deverá continuar sendo documentada e aprovada.

---

# 7. Estratégia por Sprint

As versões deverão acompanhar a evolução funcional do produto.

| Sprint | Conteúdo | Versão sugerida |
|---------|----------|-----------------|
| Fundação | Estrutura inicial | 0.1.0 |
| Sprint 01 | Authentication | 0.2.0 |
| Sprint 02 | Character | 0.3.0 |
| Sprint 2.1 | Engineering Governance | 0.3.1 (planejada, não publicada) |
| Sprint 03 | Health | 0.4.0 |
| Sprint 04 | Workout | 0.5.0 |
| Sprint 05 | Reading | 0.6.0 |
| Sprint 06 | Habits | 0.7.0 |
| Sprint 07 | Therapy | 0.8.0 |
| Sprint 08 | Game Engine | 0.9.0 |
| Release MVP | Plataforma estável | 1.0.0 |

A numeração poderá ser ajustada conforme decisão arquitetural, desde que documentada.

---

# 8. Pré-Releases

Antes de uma versão estável poderão existir versões intermediárias.

## Alpha

Utilizada quando:

- desenvolvimento ainda está em andamento;
- APIs podem mudar;
- funcionalidades estão incompletas.

Exemplo:

**0.4.0-alpha.1**

---

## Beta

Utilizada quando:

- funcionalidades foram concluídas;
- testes adicionais são necessários;
- ajustes finais ainda podem ocorrer.

Exemplo:

**0.4.0-beta.1**

---

## Release Candidate (RC)

Utilizada quando:

- todas as funcionalidades estão implementadas;
- todos os testes passaram;
- apenas validações finais permanecem.

Exemplo:

**0.4.0-rc.1**

---

# 9. Build Metadata

Quando necessário, poderá ser utilizado Build Metadata.

Formato:

**MAJOR.MINOR.PATCH+BUILD**

Exemplos:

- 0.3.1+20260805
- 1.0.0+build17
- 1.2.4+ci452

O Build Metadata não altera a precedência da versão.

Serve apenas para identificação interna.

---

# 10. Fonte Oficial da Versão

A versão oficial do LifeOS deverá existir em apenas um local.

O arquivo oficial é `pyproject.toml`. O estado documental aprovado atual é
0.3.0; a versão 0.3.1 está planejada somente após a conclusão integral da Sprint
2.1 e ainda não foi publicada. A divergência técnica atualmente presente no
`pyproject.toml` será tratada em fase posterior.

O trecho abaixo é apenas um exemplo estrutural; o valor exibido não declara uma
versão publicada:

```toml
[project]
name = "lifeos"
version = "0.3.1"
```

Arquivo:

```text
pyproject.toml
```

Outros arquivos poderão exibir a versão, mas não deverão ser considerados fonte oficial.

Sempre que a versão for alterada deverão ser atualizados, quando aplicável:

- CHANGELOG.md;
- PROJECT_STATUS.md;
- documentação de Release;
- Tag Git;
- Release GitHub;
- pipeline de CI/CD.

---

---

# 11. Versionamento da API

Enquanto a API estiver em evolução e não houver necessidade de múltiplas versões simultâneas, os endpoints não deverão conter versão na URL.

## Estrutura atual

```text
/auth/login
/auth/logout
/auth/register
/character
/character/profile
```

## Quando utilizar versionamento de API

O versionamento da API somente deverá ser adotado quando ocorrer:

- Breaking Change pública;
- necessidade de manter múltiplas versões simultaneamente;
- clientes externos dependentes da API;
- contratos incompatíveis entre versões.

Exemplo:

```text
/api/v1/auth/login
/api/v2/auth/login
```

A adoção de versionamento de API exigirá um ADR específico.

---

# 12. Versionamento do Banco de Dados

O banco de dados será versionado através do Alembic.

Cada alteração estrutural deverá possuir uma migration própria.

Exemplo:

| Migration | Descrição |
|------------|-----------|
| 0001 | Users |
| 0002 | Players e Characters |
| 0003 | Sessions e Password Reset |

A versão da aplicação e a versão do banco são independentes.

Exemplo:

| Componente | Versão |
|------------|---------|
| Aplicação | 0.3.1 |
| Alembic | 0003 |

Toda Release deverá informar:

- migration mínima suportada;
- migration atual;
- necessidade de upgrade;
- possíveis migrações de dados.

---

# 13. Versionamento da Documentação

A documentação faz parte do produto.

Sempre que houver alteração relevante deverá ser atualizada.

Documentos estruturais deverão possuir cabeçalho contendo:

- versão;
- status;
- responsável;
- aplicação.

Exemplo:

```md
**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
```

Não é obrigatório incrementar a versão de um documento para pequenas correções ortográficas.

Entretanto, alterações arquiteturais deverão atualizar a versão documental.

---

# 14. Tags Git

Toda Release oficial deverá possuir uma Tag Git.

Formato:

```text
vMAJOR.MINOR.PATCH
```

Exemplos:

- v0.3.1
- v0.4.0
- v1.0.0

Pré-Releases:

- v0.4.0-alpha.1
- v0.4.0-beta.1
- v0.4.0-rc.1

---

# 15. Regras para Criação de Tags

Uma Tag somente poderá ser criada quando todos os critérios abaixo forem atendidos.

## Código

- aplicação compila;
- imports válidos;
- sem erros de lint bloqueantes;
- sem TODOs críticos.

## Banco

- migrations validadas;
- banco atualizado;
- downgrade testado quando aplicável.

## Testes

- testes unitários aprovados;
- testes de integração aprovados;
- testes E2E aprovados;
- testes arquiteturais aprovados.

## Qualidade

- cobertura dentro da meta;
- sem DeprecationWarning bloqueante;
- sem vulnerabilidades conhecidas de alto risco.

## Documentação

- CHANGELOG atualizado;
- PROJECT_STATUS atualizado;
- TASK_HISTORY atualizado;
- documentação da Sprint atualizada;
- NEXT_TASK atualizado.

Somente após essas validações a Tag poderá ser criada.

---

# 16. Imutabilidade das Releases

Uma Release publicada é imutável.

É proibido:

- alterar uma Tag existente;
- substituir código de uma Release;
- modificar artefatos publicados.

Caso seja necessária uma correção, deverá ser criada uma nova versão.

Exemplo:

| Versão incorreta | Nova versão |
|------------------|-------------|
| 0.3.1 | 0.3.2 |

Nunca reutilizar uma versão já publicada.

---

# 17. Releases no GitHub

Cada Release deverá conter, no mínimo:

- número da versão;
- data;
- resumo executivo;
- Capabilities entregues;
- Features entregues;
- RFs implementados;
- ADRs relevantes;
- migrations;
- alterações de dependências;
- Breaking Changes;
- limitações conhecidas;
- instruções de atualização.

---

# 18. CHANGELOG

Toda versão deverá possuir uma entrada correspondente no arquivo:

```text
CHANGELOG.md
```

Estrutura recomendada:

```md
# [0.3.1]

## Added

-

## Changed

-

## Fixed

-

## Removed

-

## Security

-
```

As informações deverão refletir exatamente o que foi entregue.

---

# 19. Releases Funcionais

Uma Release Funcional deverá conter, obrigatoriamente:

- pelo menos uma Feature concluída;
- todos os RFs relacionados implementados;
- testes aprovados;
- documentação atualizada;
- rastreabilidade completa.

Normalmente uma Release Funcional incrementa a versão MINOR.

Exemplo:

| Antes | Depois |
|--------|---------|
| 0.3.1 | 0.4.0 |

---

# 20. Releases Técnicas

Uma Release Técnica poderá conter:

- melhorias arquiteturais;
- refatorações;
- melhorias de desempenho;
- atualização de dependências;
- melhorias na CI/CD;
- governança;
- documentação;
- observabilidade;
- ferramentas internas.

Releases Técnicas normalmente incrementam PATCH.

Exemplo:

| Antes | Depois |
|--------|---------|
| 0.3.0 | 0.3.1 |

Caso uma alteração técnica provoque incompatibilidade pública, deverá seguir as regras de Breaking Change.

---

---

# 21. Hotfix

Um **Hotfix** é uma correção emergencial aplicada sobre uma versão já publicada.

Seu objetivo é corrigir problemas críticos sem introduzir novas funcionalidades.

## Quando utilizar

Um Hotfix deverá ser utilizado quando ocorrer:

- falha crítica em produção;
- vulnerabilidade de segurança;
- corrupção de dados;
- indisponibilidade da aplicação;
- erro que impeça o uso do sistema.

## Regras

Todo Hotfix deverá:

- possuir escopo mínimo;
- incluir teste de regressão;
- atualizar o CHANGELOG;
- gerar uma nova versão;
- passar por revisão técnica.

Exemplo:

| Antes | Depois |
|--------|---------|
| 0.3.1 | 0.3.2 |

---

# 22. Release Candidate

Uma **Release Candidate (RC)** representa uma versão considerada pronta para produção, aguardando apenas validações finais.

## Critérios

Uma Release Candidate deverá atender aos seguintes critérios:

- todas as funcionalidades previstas foram implementadas;
- todos os testes passaram;
- documentação concluída;
- cobertura dentro da meta;
- migrations validadas;
- revisão arquitetural concluída.

Exemplo:

| Etapa | Versão |
|--------|---------|
| Alpha | 0.4.0-alpha.1 |
| Beta | 0.4.0-beta.1 |
| RC | 0.4.0-rc.1 |
| Release | 0.4.0 |

---

# 23. Critérios para a Versão 1.0.0

A versão **1.0.0** representa a primeira versão oficialmente estável do LifeOS.

Ela somente poderá ser publicada quando todos os critérios abaixo forem atendidos.

## Produto

- MVP completo;
- funcionalidades essenciais concluídas;
- fluxos críticos funcionando.

## Arquitetura

- Clean Architecture preservada;
- DDD preservado;
- CQRS aplicado onde previsto;
- Event Bus operacional;
- Unit of Work validado.

## Banco de Dados

- migrations estáveis;
- schema consolidado;
- rollback validado quando aplicável.

## Qualidade

- cobertura dentro da meta;
- testes automatizados aprovados;
- sem bugs críticos conhecidos.

## Documentação

- PRD atualizado;
- Feature Catalog atualizado;
- CHANGELOG atualizado;
- PROJECT_STATUS atualizado;
- TASK_HISTORY atualizado;
- documentação arquitetural revisada.

---

# 24. Alterações Documentais

Alterações exclusivamente documentais normalmente não geram nova versão funcional.

Quando fizerem parte de uma Release, deverão incrementar apenas **PATCH**.

Exemplos:

- correção de documentação;
- melhoria de diagramas;
- atualização de exemplos;
- melhoria de governança.

Exemplo:

| Antes | Depois |
|--------|---------|
| 0.3.0 | 0.3.1 |

---

# 25. Alterações de Dependências

Atualizações de dependências deverão seguir a política definida em **DEPENDENCY_POLICY.md**.

## Atualização compatível

Incremento recomendado:

**PATCH**

Exemplos:

- atualização de biblioteca;
- correção de vulnerabilidade compatível;
- melhoria de ferramenta de desenvolvimento.

---

## Nova dependência

Incremento recomendado:

**MINOR**, quando fizer parte de uma nova funcionalidade.

---

## Alteração incompatível

Caso uma atualização provoque incompatibilidade pública, deverá ser tratada como Breaking Change.

---

# 26. Alterações de Schema

Toda alteração estrutural do banco deverá possuir migration própria.

## Alterações compatíveis

Exemplos:

- nova tabela;
- nova coluna opcional;
- novo índice;
- nova constraint compatível.

Normalmente acompanham incremento **MINOR**.

---

## Alterações incompatíveis

Exemplos:

- remoção de coluna;
- alteração de tipo incompatível;
- alteração de chave primária;
- alteração obrigatória de dados.

Essas alterações deverão possuir:

- ADR;
- plano de migração;
- plano de rollback;
- documentação;
- atualização do CHANGELOG.

---

# 27. Alterações de API

## Alterações compatíveis

Exemplos:

- novo endpoint;
- novo parâmetro opcional;
- novo campo opcional;
- novo filtro.

Normalmente incrementam **MINOR**.

---

## Alterações incompatíveis

Exemplos:

- remoção de endpoint;
- alteração obrigatória de payload;
- alteração de autenticação;
- alteração de contrato.

Essas alterações deverão ser classificadas como Breaking Change.

---

# 28. Compatibilidade durante a fase 0.x

Mesmo durante a fase **0.x**, mudanças incompatíveis não deverão ocorrer sem controle.

Toda alteração incompatível deverá:

- ser documentada;
- possuir ADR;
- atualizar o CHANGELOG;
- ser aprovada pelo Arquiteto de Software;
- possuir plano de migração.

A fase 0.x não elimina a necessidade de disciplina arquitetural.

---

# 29. Planejamento de Versão

Ao concluir uma Sprint, deverá ser elaborado um relatório de versão contendo:

| Campo | Descrição |
|--------|-----------|
| Versão atual | Versão existente |
| Versão proposta | Nova versão |
| Tipo | MAJOR, MINOR ou PATCH |
| Justificativa | Motivo da alteração |
| Capabilities | Capabilities afetadas |
| Features | Features entregues |
| RFs | Requisitos implementados |
| ADRs | ADRs relacionados |
| Migrations | Alterações de banco |
| Dependências | Bibliotecas alteradas |

A versão somente poderá ser alterada após aprovação.

---

# 30. Commit de Release

Toda preparação de versão deverá utilizar um commit específico.

## Formato

```text
chore(release): prepare version X.Y.Z
```

Exemplo:

```text
chore(release): prepare version 0.3.1
```

O commit deverá ocorrer somente após:

- validação completa dos testes;
- atualização da documentação;
- atualização do CHANGELOG;
- atualização do PROJECT_STATUS;
- atualização do TASK_HISTORY;
- validação da Definition of Done;
- aprovação da revisão técnica.

Nenhuma nova funcionalidade deverá ser adicionada após o commit de preparação da Release.

---

# 31. Criação de Tags

A criação de uma Tag oficial deverá ocorrer somente após a conclusão da Release.

## Pré-requisitos

Antes da criação da Tag, deverão ser validados:

- aplicação iniciando corretamente;
- migrations atualizadas;
- testes unitários aprovados;
- testes de integração aprovados;
- testes E2E aprovados;
- testes arquiteturais aprovados;
- cobertura dentro da meta;
- documentação atualizada;
- CHANGELOG atualizado;
- PROJECT_STATUS atualizado;
- TASK_HISTORY atualizado;
- revisão técnica concluída.

## Procedimento

Após a aprovação da Release:

1. Atualizar a versão oficial do projeto.
2. Criar o commit de Release.
3. Criar a Tag correspondente.
4. Publicar a Release.
5. Atualizar o roadmap quando necessário.

---

# 32. Rollback de Release

Caso uma Release apresente problemas críticos após sua publicação, deverá ser executado um processo formal de rollback.

## Objetivos

O rollback deverá:

- minimizar indisponibilidade;
- preservar integridade dos dados;
- manter rastreabilidade;
- evitar perda de histórico.

## Regras

Nunca remover uma Tag publicada.

Caso seja necessária uma correção:

1. Registrar o problema.
2. Corrigir a causa.
3. Executar todos os testes.
4. Publicar uma nova versão.

Exemplo:

| Versão | Situação |
|----------|----------|
| 0.3.1 | Release problemática |
| 0.3.2 | Correção oficial |

---

# 33. Matriz de Versionamento

| Alteração | Incremento recomendado |
|------------|------------------------|
| Correção documental | PATCH |
| Correção de bug | PATCH |
| Refatoração | PATCH |
| Atualização compatível de dependência | PATCH |
| Governança | PATCH |
| Nova Feature | MINOR |
| Novo RF | MINOR |
| Nova Capability | MINOR |
| Novo endpoint compatível | MINOR |
| Nova integração | MINOR |
| Breaking Change | MAJOR |
| Alteração incompatível de API | MAJOR |
| Alteração incompatível de banco | MAJOR |
| Remoção de contrato público | MAJOR |

---

# 34. Responsabilidades

## Product Owner

Responsável por:

- aprovar o escopo da Release;
- aprovar funcionalidades;
- definir prioridades.

---

## Desenvolvedor

Responsável por:

- implementar as alterações;
- executar os testes;
- atualizar a documentação;
- preparar a Release.

---

## Agente de Inteligência Artificial

Responsável por:

- seguir esta política;
- não alterar versões sem autorização;
- produzir evidências;
- atualizar documentação quando solicitado;
- validar requisitos antes da Release.

---

## Arquiteto de Software

Responsável por:

- aprovar alterações arquiteturais;
- avaliar Breaking Changes;
- revisar ADRs;
- validar compatibilidade entre Capabilities.

---

## Revisor Técnico

Responsável por:

- revisar código;
- validar documentação;
- conferir rastreabilidade;
- aprovar ou reprovar a Release.

---

# 35. Checklist de Release

Antes da publicação de qualquer versão, todos os itens abaixo deverão estar concluídos.

## Código

- [ ] Compila corretamente.
- [ ] Sem erros de importação.
- [ ] Sem TODOs críticos.
- [ ] Sem FIXME críticos.

---

## Banco de Dados

- [ ] Migrations criadas.
- [ ] Upgrade validado.
- [ ] Downgrade validado quando aplicável.

---

## Testes

- [ ] Testes unitários.
- [ ] Testes de integração.
- [ ] Testes E2E.
- [ ] Testes arquiteturais.
- [ ] Cobertura dentro da meta.

---

## Qualidade

- [ ] Sem DeprecationWarning.
- [ ] Sem vulnerabilidades críticas.
- [ ] Dependências validadas.
- [ ] Ambiente limpo validado.

---

## Documentação

- [ ] CHANGELOG atualizado.
- [ ] PROJECT_STATUS atualizado.
- [ ] TASK_HISTORY atualizado.
- [ ] NEXT_TASK atualizado.
- [ ] Documentação da Sprint atualizada.

---

## Governança

- [ ] Revisão técnica aprovada.
- [ ] Definition of Done atendida.
- [ ] Evidências registradas.

---

# 36. Checklist de Breaking Change

Sempre que houver uma Breaking Change, deverão ser atendidos os seguintes requisitos.

- [ ] ADR criado.
- [ ] Justificativa documentada.
- [ ] Impacto identificado.
- [ ] API revisada.
- [ ] Banco revisado.
- [ ] Plano de migração elaborado.
- [ ] Plano de rollback elaborado.
- [ ] Testes de regressão criados.
- [ ] CHANGELOG atualizado.
- [ ] Nova versão aprovada.

Nenhuma Breaking Change poderá ser publicada sem aprovação do Arquiteto de Software.

---

# 37. Relatório de Versão

Cada Release deverá possuir um relatório resumindo a entrega.

## Estrutura

| Campo | Conteúdo |
|--------|----------|
| Versão atual | |
| Nova versão | |
| Tipo | MAJOR / MINOR / PATCH |
| Sprint | |
| Capabilities | |
| Features | |
| RFs | |
| ADRs | |
| Migrations | |
| Dependências | |
| Cobertura | |
| Testes executados | |
| Evidências | |
| Responsável | |
| Data | |

Este relatório poderá integrar a documentação da Release.

---

# 38. Auditoria

Toda Release deverá ser auditável.

A auditoria deverá permitir responder:

- Qual versão foi publicada?
- Quando foi publicada?
- Quem aprovou?
- Quais RFs foram entregues?
- Quais Features foram implementadas?
- Quais ADRs foram utilizados?
- Quais migrations foram executadas?
- Quais testes foram executados?
- Quais evidências foram produzidas?

Toda resposta deverá possuir rastreabilidade documental.

---

# 39. Não Conformidades

Uma Release deverá ser bloqueada quando ocorrer qualquer uma das situações abaixo.

## Código

- erros de compilação;
- erros de importação;
- dependências inválidas.

## Banco

- migrations inválidas;
- inconsistência estrutural.

## Testes

- falha em qualquer teste obrigatório;
- cobertura inferior à meta.

## Arquitetura

- violação da Clean Architecture;
- violação das regras de dependência;
- ausência de ADR obrigatória.

## Documentação

- CHANGELOG desatualizado;
- PROJECT_STATUS desatualizado;
- TASK_HISTORY desatualizado;
- documentação inconsistente.

Enquanto houver qualquer não conformidade bloqueante, a Release não poderá ser publicada.

---

# 40. Regra Final

Toda versão publicada do LifeOS deverá representar um estado:

- reproduzível;
- documentado;
- testado;
- rastreável;
- auditável;
- aprovado;
- estável para seu propósito.

Uma versão não existe apenas para numerar o software.

Ela representa um marco oficial da evolução do projeto e deverá refletir, com fidelidade, a qualidade, a arquitetura e a maturidade do LifeOS.

---

# Histórico de Versões

| Versão | Data | Descrição |
|----------|------|-----------|
| 1.0 | A definir | Criação da política oficial de versionamento do LifeOS. |
