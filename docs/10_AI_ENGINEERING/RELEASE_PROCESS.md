# RELEASE_PROCESS.md

> Política oficial do processo de Release do projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os desenvolvedores e agentes de Inteligência Artificial.

---

# 1. Objetivo

Este documento define o processo oficial de Release do projeto **LifeOS**.

Seu objetivo é garantir que toda Release publicada seja:

- estável;
- reproduzível;
- rastreável;
- auditável;
- documentada;
- validada;
- compatível com a arquitetura oficial do projeto.

Uma Release representa um marco oficial da evolução do LifeOS e somente poderá ser publicada após atender a todos os critérios definidos neste documento.

---

# 2. Escopo

Esta política aplica-se a:

- desenvolvedores;
- Tech Leads;
- Arquitetos de Software;
- revisores técnicos;
- agentes de Inteligência Artificial;
- pipelines de CI/CD;
- todas as Capabilities do LifeOS.

Também se aplica às publicações realizadas em:

- GitHub;
- artefatos de distribuição;
- documentação oficial;
- ambientes de homologação;
- ambientes de produção.

---

# 3. Documentos Relacionados

Este documento complementa os seguintes documentos oficiais:

- VERSIONING.md
- BRANCHING_STRATEGY.md
- COMMIT_GUIDELINES.md
- CODE_REVIEW_CHECKLIST.md
- DEFINITION_OF_DONE.md
- DEPENDENCY_POLICY.md
- DEVELOPMENT_WORKFLOW.md
- MASTER_EXECUTION_PLAN.md

As regras aqui descritas não substituem os documentos acima, devendo ser utilizadas em conjunto.

---

# 4. Princípios

O processo de Release do LifeOS baseia-se nos seguintes princípios.

## 4.1. Estabilidade

Uma Release deverá representar um estado estável do sistema.

Não deverão existir:

- funcionalidades incompletas;
- código experimental;
- testes obrigatórios falhando;
- migrations inválidas.

---

## 4.2. Reprodutibilidade

Qualquer Release deverá poder ser reconstruída utilizando apenas:

- código da Tag correspondente;
- migrations oficiais;
- documentação oficial;
- arquivos de dependências.

---

## 4.3. Rastreabilidade

Toda Release deverá possuir rastreabilidade completa.

Deverá ser possível identificar:

- Sprint;
- Capability;
- Feature;
- Requisito Funcional;
- ADR;
- Pull Request;
- Commits;
- Testes executados.

---

## 4.4. Evidências

Nenhuma Release poderá ser aprovada sem evidências reais.

As evidências deverão demonstrar:

- compilação;
- execução;
- testes;
- cobertura;
- migrations;
- integridade do banco;
- atualização documental.

---

## 4.5. Imutabilidade

Após publicada, uma Release torna-se imutável.

Caso seja necessária uma correção, uma nova versão deverá ser criada.

Não será permitido:

- alterar Tags existentes;
- substituir artefatos publicados;
- modificar retrospectivamente uma Release.

---

# 5. Tipos de Release

O LifeOS adota os seguintes tipos oficiais de Release.

## 5.1. Release Funcional

Entrega novas funcionalidades ao produto.

Exemplos:

- nova Capability;
- nova Feature;
- novos RFs;
- novos endpoints.

Normalmente incrementa a versão **MINOR**.

---

## 5.2. Release Técnica

Entrega melhorias internas sem alteração funcional significativa.

Exemplos:

- refatorações;
- governança;
- arquitetura;
- melhorias de desempenho;
- atualização de ferramentas.

Normalmente incrementa a versão **PATCH**.

---

## 5.3. Hotfix

Corrige um problema crítico em uma versão publicada.

Exemplos:

- falhas críticas;
- vulnerabilidades;
- erros em produção.

Sempre deverá gerar uma nova versão.

---

## 5.4. Release de Segurança

Destinada exclusivamente à correção de vulnerabilidades.

Pode ocorrer independentemente do planejamento das Sprints.

Deverá seguir fluxo prioritário.

---

## 5.5. Release Major

Representa mudanças incompatíveis.

Exemplos:

- Breaking Changes;
- alterações incompatíveis de API;
- mudanças incompatíveis de banco;
- alterações de contratos públicos.

Esse tipo de Release exige aprovação arquitetural formal.

---

# 6. Papéis e Responsabilidades

O processo de Release envolve diferentes responsabilidades.

## Product Owner

Responsável por:

- aprovar o escopo da Release;
- validar funcionalidades entregues;
- autorizar publicação funcional.

---

## Desenvolvedor

Responsável por:

- concluir a implementação;
- executar os testes;
- atualizar a documentação;
- preparar a Release.

---

## Agente de Inteligência Artificial

Responsável por:

- seguir esta política;
- produzir evidências reais;
- atualizar documentação quando solicitado;
- não publicar Releases sem autorização explícita.

---

## Arquiteto de Software

Responsável por:

- aprovar alterações arquiteturais;
- validar Breaking Changes;
- revisar ADRs;
- aprovar decisões técnicas críticas.

---

## Revisor Técnico

Responsável por:

- revisar código;
- validar testes;
- revisar documentação;
- aprovar ou reprovar a Release.

---

# 7. Critérios para Iniciar uma Release

Uma Release somente poderá ser iniciada quando todos os critérios abaixo forem atendidos.

## Desenvolvimento

- Sprint concluída;
- escopo aprovado;
- Features concluídas;
- RFs implementados.

---

## Código

- código compilando;
- imports válidos;
- sem erros críticos;
- sem conflitos pendentes.

---

## Banco de Dados

- migrations concluídas;
- schema consistente;
- banco atualizado.

---

## Testes

- testes unitários aprovados;
- testes de integração aprovados;
- testes E2E aprovados;
- testes arquiteturais aprovados.

---

## Documentação

- CHANGELOG atualizado;
- PROJECT_STATUS atualizado;
- TASK_HISTORY atualizado;
- NEXT_TASK atualizado;
- documentação da Sprint revisada.

Caso qualquer um desses critérios não seja atendido, a Release deverá permanecer bloqueada.

---

# 8. Fluxo Geral do Processo

Toda Release deverá seguir o fluxo oficial abaixo.

1. Concluir a implementação da Sprint.
2. Executar todos os testes obrigatórios.
3. Validar o banco de dados.
4. Validar dependências.
5. Atualizar a documentação.
6. Executar Code Review.
7. Corrigir não conformidades.
8. Atualizar a versão oficial.
9. Preparar o commit de Release.
10. Criar a Tag correspondente.
11. Publicar a Release.
12. Atualizar o roadmap e os indicadores do projeto.

Nenhuma etapa poderá ser ignorada.

---

# 9. Preparação da Release

A preparação da Release inicia após a conclusão da Sprint e antecede qualquer atividade de publicação.

Seu objetivo é garantir que todos os artefatos necessários estejam consistentes antes da criação da versão oficial.

## Objetivos

Durante esta etapa deverão ser verificados:

- escopo da Sprint;
- código-fonte;
- banco de dados;
- documentação;
- testes;
- versionamento;
- dependências.

Nenhuma atividade de publicação deverá ser iniciada antes da conclusão desta etapa.

---

# 10. Validação do Código

Todo código deverá ser validado antes da preparação da Release.

## Critérios

O código deverá:

- compilar corretamente;
- iniciar sem erros;
- não possuir conflitos de merge;
- respeitar a Clean Architecture;
- respeitar as regras de dependência;
- possuir rastreabilidade com os requisitos implementados.

## Também deverá ser verificado

- ausência de código comentado desnecessário;
- ausência de TODOs críticos;
- ausência de FIXMEs críticos;
- ausência de código morto;
- ausência de imports não utilizados.

Caso qualquer item falhe, a Release deverá permanecer bloqueada.

---

# 11. Validação do Banco de Dados

Toda alteração estrutural deverá ser validada antes da Release.

## Migrations

Deverão ser verificadas:

- ordem correta das migrations;
- integridade do schema;
- consistência entre código e banco;
- versionamento Alembic.

## Validações obrigatórias

Quando aplicável, executar:

```bash
python -m alembic upgrade head
```

Verificar a versão atual:

```bash
python -m alembic current
```

Caso exista estratégia de rollback:

```bash
python -m alembic downgrade -1
```

Em seguida:

```bash
python -m alembic upgrade head
```

O banco deverá permanecer consistente após essas operações.

---

# 12. Validação das Dependências

As dependências deverão seguir integralmente a política definida em:

**DEPENDENCY_POLICY.md**

## Validações obrigatórias

Verificar se todas as dependências estão instaladas corretamente:

```bash
python -m pip check
```

Confirmar que:

- não existem conflitos;
- não existem versões incompatíveis;
- não existem dependências quebradas.

Sempre que possível, a validação deverá ocorrer também em ambiente limpo.

---

# 13. Execução dos Testes

Antes da publicação da Release, todos os testes obrigatórios deverão ser executados.

## Testes Unitários

```bash
python -m pytest tests
```

---

## Testes completos

```bash
python -m pytest -v
```

---

## Cobertura

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

## Deprecation Warnings

```bash
python -W error::DeprecationWarning -m pytest -v
```

---

## Critérios

A Release somente poderá prosseguir quando:

- todos os testes forem aprovados;
- não existirem falhas;
- não existirem erros de importação;
- não existirem warnings bloqueantes.

---

# 14. Revisão Técnica

Após a validação dos testes, deverá ocorrer a revisão técnica.

A revisão seguirá obrigatoriamente o documento:

**CODE_REVIEW_CHECKLIST.md**

## Objetivos

Confirmar que:

- arquitetura foi preservada;
- código está consistente;
- documentação está atualizada;
- padrões do projeto foram respeitados;
- requisitos foram implementados corretamente.

## Resultado

A revisão poderá resultar em:

- Aprovado;
- Aprovado com ressalvas;
- Reprovado.

Uma Release reprovada não poderá prosseguir.

---

# 15. Atualização da Documentação

Toda Release deverá manter a documentação sincronizada com o estado do projeto.

## Documentos obrigatórios

Antes da publicação deverão ser atualizados, quando aplicável:

- CHANGELOG.md;
- PROJECT_STATUS.md;
- TASK_HISTORY.md;
- NEXT_TASK.md;
- PRD.md;
- FEATURE_CATALOG.md;
- CAPABILITY_MAP.md;
- documentação da Sprint;
- ADRs relacionados.

A documentação deverá refletir exatamente o que foi implementado.

---

# 16. Preparação da Versão

Após todas as validações, deverá ser preparada a nova versão do projeto.

## Atividades

Atualizar:

- versão oficial do projeto;
- CHANGELOG;
- documentação de Release;
- referência da Sprint;
- histórico do projeto.

## Conferências

Antes de prosseguir, confirmar:

- versão anterior;
- nova versão;
- tipo da Release;
- compatibilidade com VERSIONING.md.

Nenhuma versão deverá ser alterada sem aprovação conforme a política oficial de versionamento.

---

# 17. Criação da Tag

Após a aprovação da Release, deverá ser criada a Tag oficial correspondente.

A Tag representa o marco definitivo da versão publicada.

## Convenção

Toda Tag deverá seguir o padrão definido em **VERSIONING.md**.

Formato:

```text
vMAJOR.MINOR.PATCH
```

## Exemplos

```text
v0.3.1
v0.4.0
v1.0.0
```

Para Pré-Releases:

```text
v0.4.0-alpha.1
v0.4.0-beta.1
v0.4.0-rc.1
```

## Procedimento

Criar a Tag:

```bash
git tag -a v0.3.1 -m "Release v0.3.1"
```

Publicar:

```bash
git push origin v0.3.1
```

Nenhuma Tag poderá ser alterada após sua publicação.

---

# 18. Publicação da Release

Após a criação da Tag, deverá ser publicada a Release oficial.

A publicação deverá conter todas as informações necessárias para reconstrução da entrega.

## Informações obrigatórias

- versão;
- data;
- Sprint;
- Capabilities entregues;
- Features implementadas;
- Requisitos Funcionais;
- ADRs relacionados;
- migrations;
- alterações de dependências;
- Breaking Changes (quando existirem);
- limitações conhecidas.

## Artefatos

Quando aplicável, deverão ser publicados:

- código-fonte;
- documentação;
- Release Notes;
- imagem Docker;
- artefatos de distribuição.

Toda Release deverá possuir rastreabilidade completa.

---

# 19. Evidências Obrigatórias

Nenhuma Release poderá ser aprovada sem evidências reais de execução.

## Ambiente

Registrar:

- versão do Python;
- sistema operacional;
- ambiente virtual;
- versão das dependências.

---

## Dependências

Executar:

```bash
python -m pip check
```

Resultado esperado:

```text
No broken requirements found.
```

---

## Banco de Dados

Executar:

```bash
python -m alembic upgrade head
```

Validar:

```bash
python -m alembic current
```

Registrar:

- versão Alembic;
- migrations executadas;
- schema final.

---

## Testes

Executar:

```bash
python -m pytest -v
```

Cobertura:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Warnings:

```bash
python -W error::DeprecationWarning -m pytest -v
```

---

## Aplicação

Validar inicialização.

Exemplo:

```bash
uvicorn app.main:app --reload
```

Confirmar:

- aplicação iniciou;
- rotas registradas;
- OpenAPI disponível;
- documentação acessível.

---

## Evidências adicionais

Sempre que possível registrar:

- cobertura;
- tempo de execução;
- quantidade de testes;
- quantidade de módulos importados;
- resultado da validação HTTP.

---

# 20. Hotfix

Um Hotfix representa uma correção emergencial aplicada sobre uma versão publicada.

## Objetivos

Corrigir:

- falhas críticas;
- vulnerabilidades;
- indisponibilidade;
- corrupção de dados;
- regressões críticas.

## Fluxo

1. Criar branch `hotfix/`.
2. Implementar a correção.
3. Executar testes.
4. Atualizar documentação.
5. Criar nova versão.
6. Criar nova Tag.
7. Publicar Release.

## Exemplo

| Versão | Nova versão |
|---------|-------------|
| 0.3.1 | 0.3.2 |

Nenhum Hotfix deverá modificar uma Tag existente.

---

# 21. Rollback

Caso uma Release apresente problemas críticos, poderá ser necessário realizar rollback.

## Objetivos

- restaurar estabilidade;
- preservar integridade dos dados;
- minimizar indisponibilidade.

## Regras

O rollback deverá possuir:

- justificativa;
- evidências;
- registro no CHANGELOG;
- atualização do PROJECT_STATUS.

## Importante

Rollback não significa apagar histórico.

Toda ação deverá permanecer auditável.

---

# 22. Auditoria

Toda Release deverá permitir auditoria completa.

A qualquer momento deverá ser possível responder:

- Qual versão foi publicada?
- Quando foi publicada?
- Quem aprovou?
- Qual Sprint originou a Release?
- Quais Capabilities foram entregues?
- Quais Features foram implementadas?
- Quais RFs foram concluídos?
- Quais ADRs foram utilizados?
- Quais migrations foram executadas?
- Quais testes foram executados?
- Quais evidências foram produzidas?

Nenhuma Release deverá perder sua rastreabilidade.

---

# 23. Não Conformidades

A publicação da Release deverá ser bloqueada sempre que existir qualquer não conformidade crítica.

## Código

- erros de compilação;
- erros de importação;
- código incompleto;
- conflitos pendentes.

---

## Banco

- migrations inválidas;
- schema inconsistente;
- falha de upgrade.

---

## Testes

- falha em testes obrigatórios;
- cobertura abaixo da meta;
- regressões identificadas.

---

## Arquitetura

- violação da Clean Architecture;
- violação das regras de dependência;
- ausência de ADR obrigatória.

---

## Documentação

- CHANGELOG desatualizado;
- PROJECT_STATUS desatualizado;
- TASK_HISTORY desatualizado;
- NEXT_TASK desatualizado;
- documentação inconsistente.

Enquanto qualquer item permanecer pendente, a Release deverá continuar bloqueada.

---

# 24. Critérios de Bloqueio

Uma Release não poderá ser publicada quando ocorrer qualquer uma das situações abaixo.

- Sprint não concluída.
- RFs obrigatórios incompletos.
- Testes falhando.
- Cobertura abaixo da meta definida pelo projeto.
- Migrations não validadas.
- Banco inconsistente.
- Dependências quebradas.
- Vulnerabilidades críticas conhecidas.
- Revisão técnica reprovada.
- Definition of Done não atendida.
- Evidências ausentes.
- Documentação oficial desatualizada.

Somente após a resolução de todas as pendências a Release poderá prosseguir para publicação.

---

# 25. Checklist de Release

Antes da publicação de qualquer Release, todos os itens abaixo deverão ser concluídos.

## Planejamento

- [ ] Sprint concluída.
- [ ] Escopo aprovado.
- [ ] Features implementadas.
- [ ] Requisitos Funcionais concluídos.
- [ ] ADRs atualizadas quando necessário.

---

## Código

- [ ] Aplicação compila corretamente.
- [ ] Sem erros de importação.
- [ ] Sem conflitos de merge.
- [ ] Sem TODOs críticos.
- [ ] Sem FIXMEs críticos.
- [ ] Sem código morto.

---

## Arquitetura

- [ ] Clean Architecture preservada.
- [ ] DDD preservado.
- [ ] CQRS respeitado.
- [ ] Unit of Work validado.
- [ ] Event Bus validado.
- [ ] Composition Root atualizado quando necessário.

---

## Banco de Dados

- [ ] Migrations criadas.
- [ ] Upgrade validado.
- [ ] Downgrade validado quando aplicável.
- [ ] Integridade do banco confirmada.
- [ ] Alembic sincronizado.

---

## Dependências

- [ ] `requirements.txt` atualizado.
- [ ] `pyproject.toml` atualizado.
- [ ] `pip check` executado.
- [ ] Nenhuma dependência quebrada.

---

## Testes

- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados.
- [ ] Testes E2E aprovados.
- [ ] Testes arquiteturais aprovados.
- [ ] Cobertura dentro da meta.
- [ ] Nenhum `DeprecationWarning`.

---

## Aplicação

- [ ] Uvicorn iniciado com sucesso.
- [ ] OpenAPI acessível.
- [ ] `/docs` disponível.
- [ ] Rotas registradas corretamente.
- [ ] Endpoints principais validados.

---

## Documentação

- [ ] CHANGELOG atualizado.
- [ ] PROJECT_STATUS atualizado.
- [ ] TASK_HISTORY atualizado.
- [ ] NEXT_TASK atualizado.
- [ ] Documentação da Sprint atualizada.
- [ ] PRD atualizado quando aplicável.
- [ ] FEATURE_CATALOG atualizado quando aplicável.
- [ ] CAPABILITY_MAP atualizado quando aplicável.

---

## Governança

- [ ] Versionamento atualizado.
- [ ] Code Review aprovado.
- [ ] Definition of Done atendida.
- [ ] Evidências registradas.
- [ ] Release aprovada.

---

# 26. Checklist de Hotfix

Toda correção emergencial deverá seguir este checklist.

## Correção

- [ ] Problema reproduzido.
- [ ] Causa identificada.
- [ ] Correção implementada.

---

## Testes

- [ ] Teste de regressão criado.
- [ ] Fluxo impactado validado.
- [ ] Nenhuma regressão detectada.

---

## Banco

- [ ] Migrations validadas quando aplicável.
- [ ] Integridade confirmada.

---

## Documentação

- [ ] CHANGELOG atualizado.
- [ ] PROJECT_STATUS atualizado.
- [ ] TASK_HISTORY atualizado.

---

## Publicação

- [ ] Nova versão criada.
- [ ] Nova Tag publicada.
- [ ] Release publicada.

---

# 27. Checklist de Rollback

Caso seja necessário reverter uma Release, deverão ser executadas as seguintes atividades.

## Análise

- [ ] Problema confirmado.
- [ ] Impacto identificado.
- [ ] Aprovação obtida.

---

## Execução

- [ ] Plano de rollback executado.
- [ ] Banco validado.
- [ ] Aplicação iniciada.
- [ ] Testes críticos executados.

---

## Pós-Rollback

- [ ] Evidências registradas.
- [ ] CHANGELOG atualizado.
- [ ] PROJECT_STATUS atualizado.
- [ ] Nova Release planejada.

---

# 28. Fluxo para Agentes de Inteligência Artificial

Os agentes de Inteligência Artificial deverão seguir rigorosamente o processo oficial de Release.

## Responsabilidades

Os agentes deverão:

- implementar apenas o escopo autorizado;
- preservar a arquitetura oficial;
- produzir evidências reais;
- atualizar a documentação solicitada;
- executar os testes obrigatórios;
- respeitar a política de versionamento.

## Restrições

Os agentes não deverão:

- publicar Releases sem autorização;
- criar Tags Git sem autorização;
- alterar versões automaticamente;
- ignorar falhas de testes;
- modificar documentação fora do escopo autorizado.

Toda alteração realizada por IA deverá ser revisada antes da publicação.

---

# 29. Métricas de Qualidade

Toda Release deverá possuir indicadores mínimos de qualidade.

## Código

- compilação sem erros;
- imports válidos;
- ausência de código morto.

---

## Testes

- 100% dos testes obrigatórios aprovados;
- cobertura conforme meta definida;
- nenhuma regressão conhecida.

---

## Banco de Dados

- migrations consistentes;
- integridade validada;
- versionamento sincronizado.

---

## Documentação

- documentação sincronizada com o código;
- rastreabilidade completa;
- evidências registradas.

---

## Arquitetura

- nenhuma violação da Clean Architecture;
- nenhuma violação da política de dependências;
- nenhuma violação das fronteiras entre Capabilities.

Essas métricas deverão servir como indicadores mínimos para aprovação da Release.

---

# 30. Regra Final

Uma Release do LifeOS representa um marco oficial da evolução do produto.

Ela deverá refletir um estado:

- estável;
- reproduzível;
- documentado;
- testado;
- auditável;
- rastreável;
- aprovado.

Nenhuma Release deverá ser publicada apenas porque uma Sprint foi concluída.

A publicação somente ocorrerá quando todos os critérios técnicos, arquiteturais, documentais e de qualidade definidos neste documento forem integralmente atendidos.

A qualidade da Release sempre terá prioridade sobre a velocidade de entrega.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial do processo de Release do LifeOS. |