# CONTRIBUTING.md

> Guia oficial de contribuição para o projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os desenvolvedores e agentes de Inteligência Artificial.

---

# 1. Objetivo

Este documento define o processo oficial de contribuição para o projeto **LifeOS**.

Seu objetivo é garantir que toda contribuição seja realizada de forma:

- consistente;
- rastreável;
- segura;
- documentada;
- testada;
- alinhada à arquitetura oficial;
- compatível com as políticas de engenharia do projeto.

Toda alteração realizada no LifeOS deverá seguir este processo, independentemente do seu tamanho ou complexidade.

---

# 2. Escopo

Esta política aplica-se a todas as contribuições realizadas no projeto.

Inclui:

- implementação de novas funcionalidades;
- correção de defeitos;
- refatorações;
- melhorias de desempenho;
- alterações arquiteturais;
- documentação;
- testes;
- infraestrutura;
- pipelines de CI/CD;
- automações.

Também se aplica às contribuições produzidas por:

- desenvolvedores;
- Tech Leads;
- Arquitetos de Software;
- revisores técnicos;
- Codex;
- Gemini;
- OpenCode;
- outros agentes de Inteligência Artificial.

---

# 3. Documentos Relacionados

Toda contribuição deverá respeitar os seguintes documentos oficiais:

- DEVELOPMENT_WORKFLOW.md
- MASTER_EXECUTION_PLAN.md
- DEFINITION_OF_DONE.md
- CODE_STYLE.md
- TESTING_POLICY.md
- CODE_REVIEW_CHECKLIST.md
- BRANCHING_STRATEGY.md
- COMMIT_GUIDELINES.md
- RELEASE_PROCESS.md
- VERSIONING.md
- DEPENDENCY_POLICY.md

As decisões arquiteturais aprovadas em ADRs possuem prioridade sobre este documento.

---

# 4. Princípios

Toda contribuição deverá seguir os princípios abaixo.

---

## 4.1. Qualidade

A qualidade do software possui prioridade sobre a velocidade de entrega.

Nenhuma funcionalidade deverá ser integrada sem atender aos critérios definidos pelo projeto.

---

## 4.2. Rastreabilidade

Toda alteração deverá possuir rastreabilidade completa.

Deverá ser possível identificar:

- Sprint;
- Capability;
- Feature;
- Requisito Funcional;
- Branch;
- Commits;
- Pull Request;
- testes executados.

---

## 4.3. Arquitetura

Toda contribuição deverá preservar:

- Clean Architecture;
- Domain-Driven Design;
- CQRS;
- Event-Driven Architecture;
- regras de dependência;
- isolamento entre Capabilities.

Nenhuma alteração poderá violar a arquitetura oficial.

---

## 4.4. Testabilidade

Toda funcionalidade deverá ser acompanhada pelos testes apropriados.

O código não será considerado concluído sem validação automatizada.

---

## 4.5. Documentação

A documentação faz parte da entrega.

Sempre que uma alteração impactar comportamento, arquitetura ou processo, a documentação correspondente deverá ser atualizada.

---

## 4.6. Evolução Contínua

Toda contribuição deverá melhorar ou manter a qualidade do projeto.

Não serão aceitas alterações que aumentem:

- dívida técnica;
- acoplamento;
- duplicação;
- complexidade desnecessária.

---

# 5. Quem Pode Contribuir

Podem contribuir para o LifeOS:

- desenvolvedores autorizados;
- Tech Leads;
- Arquitetos de Software;
- revisores técnicos;
- agentes de Inteligência Artificial autorizados.

Toda contribuição deverá seguir rigorosamente este documento.

---

## Agentes de Inteligência Artificial

Os agentes de IA deverão seguir exatamente o mesmo processo exigido dos desenvolvedores humanos.

Nenhum agente possui permissão para ignorar políticas de engenharia ou arquitetura.

---

# 6. Papéis e Responsabilidades

O processo de contribuição envolve diferentes responsabilidades.

---

## Product Owner

Responsável por:

- aprovar o escopo;
- priorizar funcionalidades;
- aprovar requisitos.

---

## Desenvolvedor

Responsável por:

- implementar a solução;
- executar os testes;
- atualizar a documentação;
- produzir evidências da execução.

---

## Arquiteto de Software

Responsável por:

- validar decisões arquiteturais;
- aprovar mudanças estruturais;
- revisar ADRs;
- garantir a evolução sustentável da arquitetura.

---

## Revisor Técnico

Responsável por:

- revisar código;
- validar testes;
- verificar conformidade com os padrões do projeto;
- aprovar ou reprovar a contribuição.

---

## Agente de Inteligência Artificial

Responsável por:

- implementar apenas o escopo autorizado;
- seguir todas as políticas oficiais;
- produzir evidências reais de execução;
- não alterar requisitos sem autorização;
- não modificar arquitetura sem aprovação formal.

---

# 7. Fluxo Geral de Contribuição

Toda contribuição deverá seguir obrigatoriamente o fluxo abaixo.

1. Selecionar a tarefa autorizada.
2. Atualizar a branch `main`.
3. Criar uma nova branch.
4. Implementar a alteração.
5. Executar os testes obrigatórios.
6. Atualizar a documentação.
7. Criar commits conforme o padrão oficial.
8. Abrir Pull Request.
9. Realizar Code Review.
10. Corrigir eventuais não conformidades.
11. Aprovar o Pull Request.
12. Realizar o Merge.
13. Atualizar o status do projeto.

Nenhuma etapa poderá ser omitida.

---

# 8. Preparação do Ambiente

Antes de iniciar qualquer contribuição, o ambiente deverá estar preparado e validado.

---

## Ambiente Python

Utilizar exclusivamente o ambiente virtual oficial do projeto.

Exemplo:

```bash
python -m venv .venv
```

Ativação:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Instalação das Dependências

Instalar todas as dependências oficiais:

```bash
pip install -r requirements.txt
```

---

## Validação

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

Quando aplicável, sincronizar o banco utilizando:

```bash
python -m alembic upgrade head
```

---

## Verificação Inicial

Antes de iniciar qualquer implementação, confirmar:

- ambiente virtual ativo;
- dependências instaladas;
- migrations sincronizadas;
- projeto compilando;
- testes executando corretamente.

Somente após essa validação o desenvolvimento poderá ser iniciado.

---

# 9. Escolha da Tarefa

Toda contribuição deverá iniciar a partir de uma tarefa oficialmente autorizada.

A implementação deverá possuir rastreabilidade com o planejamento do projeto.

A origem da tarefa poderá ser:

- Sprint ativa;
- Capability;
- Feature;
- Requisito Funcional (RF);
- Bug;
- Hotfix;
- Refatoração;
- ADR aprovada.

Não será permitido iniciar implementações sem autorização explícita.

---

## 9.1. Escopo

Antes de iniciar o desenvolvimento, confirmar:

- Sprint correspondente;
- Capability responsável;
- Feature envolvida;
- Requisitos Funcionais;
- critérios de aceite;
- documentação relacionada.

Caso exista conflito documental, a implementação deverá ser interrompida até a definição oficial.

---

# 10. Criação da Branch

Toda contribuição deverá ocorrer em uma branch específica.

A criação deverá seguir integralmente o documento:

**BRANCHING_STRATEGY.md**

---

## Procedimento

Atualizar a branch principal:

```bash
git checkout main
git pull origin main
```

Criar a nova branch:

```bash
git checkout -b feature/auth-register
```

---

## Regras

A branch deverá:

- possuir escopo único;
- representar apenas uma unidade lógica de trabalho;
- utilizar nomenclatura oficial;
- permanecer aberta pelo menor tempo possível.

Não será permitido desenvolver diretamente na branch `main`.

---

# 11. Desenvolvimento

O desenvolvimento deverá seguir integralmente a arquitetura oficial do LifeOS.

Durante a implementação deverão ser respeitados:

- Clean Architecture;
- Domain-Driven Design;
- CQRS;
- Event-Driven Architecture;
- regras de dependência;
- isolamento entre Capabilities.

---

## Responsabilidades

Toda implementação deverá:

- atender ao escopo autorizado;
- preservar a arquitetura;
- manter a rastreabilidade;
- produzir código limpo;
- manter compatibilidade com a documentação.

Não implementar funcionalidades fora do escopo da Sprint.

---

# 12. Atualização da Documentação

A documentação deverá evoluir juntamente com o código.

Sempre que aplicável, atualizar:

- CHANGELOG.md;
- PROJECT_STATUS.md;
- TASK_HISTORY.md;
- NEXT_TASK.md;
- PRD.md;
- FEATURE_CATALOG.md;
- CAPABILITY_MAP.md;
- ADRs.

---

## Regras

A documentação deverá refletir exatamente o comportamento implementado.

Não registrar funcionalidades inexistentes.

Não omitir alterações arquiteturais.

---

# 13. Commits

Os commits deverão seguir obrigatoriamente o padrão definido em:

**COMMIT_GUIDELINES.md**

---

## Regras

Cada commit deverá:

- representar uma alteração lógica;
- compilar corretamente;
- preservar o histórico;
- possuir mensagem padronizada.

Evitar commits contendo alterações não relacionadas.

---

## Antes do Commit

Confirmar:

- código compilando;
- testes locais aprovados;
- documentação atualizada;
- arquivos temporários removidos.

---

# 14. Testes Obrigatórios

Toda contribuição deverá ser validada antes da abertura do Pull Request.

A política oficial encontra-se em:

**TESTING_POLICY.md**

---

## Execuções obrigatórias

Executar:

```bash
python -m pytest -v
```

---

Cobertura:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

Warnings:

```bash
python -W error::DeprecationWarning -m pytest -v
```

---

Dependências:

```bash
python -m pip check
```

---

Banco de Dados

Quando houver alterações estruturais:

```bash
python -m alembic upgrade head
```

---

## API

Quando houver alterações na aplicação:

- iniciar o Uvicorn;
- validar `/docs`;
- validar `/openapi.json`;
- validar os endpoints modificados.

Toda execução deverá gerar evidências reais.

---

# 15. Revisão Local

Antes da abertura do Pull Request, o próprio autor deverá realizar uma revisão completa da implementação.

Essa revisão tem como objetivo identificar problemas antes da revisão técnica formal.

---

## Verificar

- arquitetura;
- organização do código;
- imports;
- nomenclatura;
- documentação;
- testes;
- cobertura;
- migrations;
- dependências.

Corrigir todas as não conformidades identificadas.

---

## Checklist

Confirmar:

- código limpo;
- ausência de TODOs críticos;
- ausência de FIXMEs críticos;
- ausência de código morto;
- ausência de warnings.

---

# 16. Preparação do Pull Request

Somente após todas as validações o Pull Request poderá ser preparado.

---

## Confirmar

- branch atualizada;
- commits organizados;
- documentação sincronizada;
- testes aprovados;
- evidências registradas.

---

## O Pull Request deverá conter

- objetivo da alteração;
- Sprint;
- Capability;
- Feature;
- Requisitos Funcionais;
- ADRs relacionadas;
- testes executados;
- documentação alterada;
- evidências da validação.

Nenhum Pull Request deverá ser aberto antes da conclusão dessas atividades.

---

# 17. Pull Request

Toda contribuição deverá ser integrada ao projeto através de um Pull Request.

O Pull Request representa o ponto oficial de revisão técnica antes da integração com a branch principal.

Toda alteração deverá possuir um Pull Request correspondente.

---

## 17.1. Conteúdo Obrigatório

O Pull Request deverá conter, no mínimo:

- objetivo da alteração;
- Sprint;
- Capability;
- Feature;
- Requisitos Funcionais;
- documentação alterada;
- ADRs relacionadas, quando aplicável;
- testes executados;
- evidências produzidas.

---

## 17.2. Escopo

Cada Pull Request deverá possuir um único objetivo.

Não misturar:

- novas funcionalidades;
- refatorações;
- correções;
- documentação;
- infraestrutura.

Quando houver objetivos distintos, criar Pull Requests independentes.

---

## 17.3. Evidências

Sempre que aplicável, anexar:

- resultado do pytest;
- cobertura;
- pip check;
- Alembic;
- inicialização da aplicação;
- validação dos endpoints.

As evidências deverão ser reais.

---

# 18. Code Review

Todo Pull Request deverá passar por revisão técnica.

A revisão seguirá obrigatoriamente o documento:

**CODE_REVIEW_CHECKLIST.md**

---

## Objetivos

Verificar:

- arquitetura;
- qualidade do código;
- testes;
- documentação;
- rastreabilidade;
- aderência aos padrões do projeto.

---

## Critérios

O revisor deverá confirmar:

- código legível;
- responsabilidades bem definidas;
- ausência de duplicação;
- conformidade arquitetural;
- testes suficientes.

---

## Resultado

A revisão poderá resultar em:

- Aprovado;
- Aprovado com ressalvas;
- Reprovado.

Enquanto existir reprovação, o Merge permanecerá bloqueado.

---

# 19. Correções Solicitadas

Quando a revisão identificar problemas, o autor deverá corrigir todas as não conformidades antes da aprovação.

---

## Exemplos

- arquitetura incorreta;
- testes insuficientes;
- documentação incompleta;
- nomenclatura inadequada;
- violações de dependência;
- regressões.

---

## Regras

As correções deverão ocorrer na mesma branch do Pull Request.

Após cada correção, os testes obrigatórios deverão ser executados novamente.

---

# 20. Critérios de Aprovação

Uma contribuição somente poderá ser aprovada quando atender integralmente aos critérios abaixo.

---

## Código

- compila corretamente;
- imports válidos;
- sem código morto;
- sem conflitos.

---

## Arquitetura

- Clean Architecture preservada;
- DDD preservado;
- CQRS preservado;
- fronteiras entre Capabilities respeitadas.

---

## Banco

- migrations válidas;
- schema consistente;
- Alembic sincronizado.

---

## Testes

- testes unitários aprovados;
- testes de integração aprovados;
- testes End-to-End aprovados;
- testes arquiteturais aprovados;
- cobertura dentro da meta.

---

## Documentação

- documentação atualizada;
- CHANGELOG atualizado;
- PROJECT_STATUS atualizado;
- TASK_HISTORY atualizado;
- NEXT_TASK atualizado, quando aplicável.

---

# 21. Merge

O Merge somente poderá ocorrer após aprovação formal.

A estratégia deverá seguir:

**BRANCHING_STRATEGY.md**

---

## Regras

Antes do Merge, confirmar:

- Pull Request aprovado;
- testes aprovados;
- documentação atualizada;
- branch sincronizada;
- ausência de conflitos.

---

## Estratégias Permitidas

Preferencialmente:

- Squash Merge;
- Rebase and Merge.

A estratégia deverá manter o histórico limpo e rastreável.

---

# 22. Atualização Pós-Merge

Após o Merge, deverão ser realizadas as atividades finais.

---

## Atualizar

Quando aplicável:

- CHANGELOG.md;
- PROJECT_STATUS.md;
- TASK_HISTORY.md;
- NEXT_TASK.md;
- documentação da Sprint;
- roadmap do projeto.

---

## Branch

Após confirmação do Merge:

- remover a branch local;
- remover a branch remota.

Exemplo:

```bash
git branch -d feature/character-profile
```

```bash
git push origin --delete feature/character-profile
```

---

# 23. Contribuições de Agentes de Inteligência Artificial

Os agentes de IA deverão seguir exatamente o mesmo fluxo aplicado aos desenvolvedores.

Não existem exceções.

---

## Obrigatório

Os agentes deverão:

- respeitar a arquitetura;
- respeitar os documentos oficiais;
- executar testes;
- produzir evidências;
- atualizar documentação quando solicitado;
- seguir o padrão de commits.

---

## Proibido

Os agentes não deverão:

- alterar requisitos;
- alterar arquitetura sem autorização;
- ignorar falhas de testes;
- criar Tags Git;
- publicar Releases;
- modificar versões automaticamente.

Toda contribuição produzida por IA deverá ser revisada antes do Merge.

---

# 24. Não Conformidades

As situações abaixo impedem a aprovação da contribuição.

---

## Código

- erro de compilação;
- import inválido;
- dependência quebrada;
- código incompleto.

---

## Arquitetura

- violação da Clean Architecture;
- quebra das regras de dependência;
- acoplamento indevido entre Capabilities.

---

## Banco

- migration inválida;
- schema inconsistente;
- falha de atualização.

---

## Testes

- qualquer teste falhando;
- cobertura abaixo da meta;
- regressão conhecida.

---

## Documentação

- documentação desatualizada;
- CHANGELOG inconsistente;
- PROJECT_STATUS desatualizado;
- TASK_HISTORY desatualizado;
- NEXT_TASK inconsistente.

Enquanto qualquer não conformidade permanecer aberta, o Pull Request não poderá ser aprovado.

---

# 25. Checklist de Contribuição

Antes de solicitar a aprovação de uma contribuição, o autor deverá confirmar que todos os itens abaixo foram concluídos.

---

## Planejamento

- [ ] Tarefa oficialmente autorizada.
- [ ] Sprint identificada.
- [ ] Capability identificada.
- [ ] Feature identificada.
- [ ] Requisitos Funcionais identificados.

---

## Desenvolvimento

- [ ] Implementação concluída.
- [ ] Arquitetura preservada.
- [ ] Código organizado.
- [ ] Padrões do projeto respeitados.

---

## Banco de Dados

- [ ] Migrations criadas quando necessárias.
- [ ] Alembic sincronizado.
- [ ] Schema validado.

---

## Testes

- [ ] Testes unitários aprovados.
- [ ] Testes de integração aprovados.
- [ ] Testes End-to-End aprovados.
- [ ] Testes arquiteturais aprovados.
- [ ] Cobertura dentro da meta.
- [ ] Nenhum `DeprecationWarning`.

---

## Documentação

- [ ] CHANGELOG atualizado.
- [ ] PROJECT_STATUS atualizado.
- [ ] TASK_HISTORY atualizado.
- [ ] NEXT_TASK atualizado quando aplicável.
- [ ] Documentação técnica atualizada.

---

## Pull Request

- [ ] Evidências anexadas.
- [ ] Checklist preenchido.
- [ ] Pronto para revisão técnica.

---

# 26. Comunicação

Toda comunicação relacionada ao desenvolvimento deverá ser clara, objetiva e rastreável.

---

## Commits

Os commits deverão seguir obrigatoriamente:

**COMMIT_GUIDELINES.md**

---

## Pull Requests

A descrição deverá informar:

- objetivo;
- escopo;
- Sprint;
- Capability;
- Feature;
- Requisitos Funcionais;
- testes executados;
- documentação alterada.

---

## Revisões

As observações realizadas durante o Code Review deverão ser:

- objetivas;
- técnicas;
- respeitosas;
- fundamentadas.

Discussões arquiteturais deverão ser registradas em ADR quando resultarem em decisões permanentes.

---

# 27. Auditoria

Toda contribuição deverá permitir auditoria completa.

Deverá ser possível identificar:

- autor;
- data;
- Sprint;
- Capability;
- Feature;
- Requisitos Funcionais;
- Branch;
- Commits;
- Pull Request;
- testes executados;
- cobertura obtida;
- documentação alterada.

---

## Evidências

Sempre que aplicável, registrar:

- resultado do `pytest`;
- cobertura de testes;
- `pip check`;
- execução das migrations;
- inicialização da aplicação;
- validação dos endpoints;
- evidências do ambiente utilizado.

Nenhuma contribuição deverá depender exclusivamente de declarações textuais sem validação.

---

# 28. Boas Práticas

Toda contribuição deverá seguir as boas práticas adotadas pelo LifeOS.

---

## Código

- escrever código simples;
- utilizar nomes claros;
- manter baixo acoplamento;
- favorecer alta coesão;
- remover código não utilizado.

---

## Arquitetura

- respeitar as fronteiras entre Capabilities;
- preservar a Clean Architecture;
- utilizar Ports e Adapters corretamente;
- manter regras de negócio no domínio.

---

## Testes

- adicionar testes para novas funcionalidades;
- criar testes de regressão para defeitos corrigidos;
- manter a suíte rápida e determinística.

---

## Documentação

- atualizar documentos sempre que necessário;
- manter rastreabilidade;
- evitar documentação desatualizada.

---

## Colaboração

- manter escopo reduzido por Pull Request;
- comunicar decisões relevantes;
- revisar cuidadosamente antes do Merge.

---

# 29. Fluxo Resumido

O processo oficial de contribuição deverá seguir a sequência abaixo.

1. Selecionar a tarefa autorizada.
2. Atualizar a branch `main`.
3. Criar uma nova branch.
4. Implementar a alteração.
5. Executar todos os testes obrigatórios.
6. Atualizar a documentação.
7. Criar commits conforme o padrão oficial.
8. Abrir Pull Request.
9. Realizar Code Review.
10. Corrigir não conformidades.
11. Aprovar o Pull Request.
12. Realizar o Merge.
13. Atualizar a documentação pós-Merge.
14. Remover a branch utilizada.

Esse fluxo deverá ser seguido por todos os colaboradores e agentes de Inteligência Artificial.

---

# 30. Regra Final

Contribuir para o LifeOS significa preservar a qualidade do projeto em todos os seus aspectos.

Cada contribuição deverá:

- resolver um problema claramente definido;
- manter a arquitetura íntegra;
- preservar a rastreabilidade;
- possuir testes automatizados;
- atualizar a documentação quando necessário;
- produzir evidências reais da validação realizada.

Nenhuma contribuição será considerada concluída apenas porque o código foi escrito.

Ela somente estará concluída quando atender integralmente:

- à arquitetura oficial;
- às políticas de engenharia;
- aos critérios da Definition of Done;
- às regras de testes;
- às regras de revisão;
- às regras de Release.

A qualidade do projeto sempre terá prioridade sobre a velocidade de desenvolvimento.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial de contribuição do projeto LifeOS. |