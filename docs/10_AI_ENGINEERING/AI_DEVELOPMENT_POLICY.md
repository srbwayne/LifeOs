# AI_DEVELOPMENT_POLICY.md

> Política oficial para utilização de Inteligência Artificial no desenvolvimento do projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os agentes de Inteligência Artificial utilizados no desenvolvimento do projeto.

---

# 1. Objetivo

Este documento define a política oficial para utilização de agentes de Inteligência Artificial durante o desenvolvimento do **LifeOS**.

Seu objetivo é estabelecer padrões de comportamento, responsabilidades e limitações para garantir que toda contribuição produzida por IA mantenha o mesmo nível de qualidade exigido dos desenvolvedores humanos.

Esta política aplica-se independentemente do modelo ou fornecedor da Inteligência Artificial.

---

# 2. Escopo

Esta política aplica-se a qualquer agente utilizado durante o ciclo de desenvolvimento do LifeOS.

Inclui:

- geração de código;
- revisão técnica;
- documentação;
- testes;
- refatoração;
- arquitetura;
- análise de requisitos;
- automação;
- suporte ao desenvolvimento.

Também se aplica a:

- Codex;
- Gemini;
- OpenCode;
- ChatGPT;
- Claude;
- Cursor;
- outros agentes autorizados.

---

# 3. Documentos Relacionados

Esta política complementa os seguintes documentos oficiais:

- CONTRIBUTING.md
- DEVELOPMENT_WORKFLOW.md
- CODE_STYLE.md
- TESTING_POLICY.md
- SECURITY_POLICY.md
- DEPENDENCY_POLICY.md
- CODE_REVIEW_CHECKLIST.md
- RELEASE_PROCESS.md
- DEFINITION_OF_DONE.md

As decisões arquiteturais aprovadas em ADRs possuem prioridade sobre esta política.

---

# 4. Princípios

Toda Inteligência Artificial utilizada no projeto deverá respeitar os princípios abaixo.

---

## 4.1. Arquitetura em Primeiro Lugar

A IA deverá preservar integralmente a arquitetura oficial do projeto.

Nenhuma sugestão poderá violar:

- Clean Architecture;
- Domain-Driven Design;
- CQRS;
- Event-Driven Architecture;
- isolamento entre Capabilities.

---

## 4.2. Escopo Controlado

A IA deverá implementar apenas o escopo explicitamente autorizado.

Não deverá:

- adicionar funcionalidades;
- alterar requisitos;
- modificar comportamento;
- antecipar Sprints futuras.

---

## 4.3. Rastreabilidade

Toda alteração produzida por IA deverá possuir rastreabilidade.

Deverá ser possível identificar:

- Sprint;
- Capability;
- Feature;
- Requisito Funcional;
- documentação relacionada.

---

## 4.4. Evidências

Nenhuma implementação poderá ser declarada concluída sem evidências reais de execução.

Os testes deverão seguir integralmente a política definida em **TESTING_POLICY.md**.

---

## 4.5. Transparência

A IA deverá informar claramente:

- limitações;
- dependências;
- bloqueios;
- conflitos documentais;
- requisitos ausentes.

Não deverá assumir decisões de produto por conta própria.

---

## 4.6. Consistência

Toda contribuição deverá permanecer consistente com:

- arquitetura;
- documentação;
- decisões anteriores;
- padrões oficiais do projeto.

---

# 5. Papéis da Inteligência Artificial

Os agentes poderão assumir diferentes papéis durante o desenvolvimento.

Exemplos:

- Desenvolvedor;
- Revisor Técnico;
- Arquiteto de Software;
- Auditor Técnico;
- Documentador;
- Analista de Requisitos.

O papel deverá ser definido explicitamente antes do início da atividade.

---

# 6. Responsabilidades

Todo agente deverá:

- respeitar esta política;
- preservar a arquitetura;
- seguir os documentos oficiais;
- manter rastreabilidade;
- produzir código limpo;
- executar apenas atividades autorizadas;
- atualizar documentação quando solicitado.

O agente nunca deverá assumir responsabilidades não autorizadas.

---

# 7. Limitações

Os agentes não possuem autonomia para:

- alterar requisitos;
- alterar o escopo da Sprint;
- modificar ADRs;
- criar novas Capabilities;
- alterar a arquitetura oficial;
- publicar Releases;
- criar Tags Git;
- modificar versões do projeto;
- decidir prioridades de produto.

Essas decisões pertencem exclusivamente ao responsável pelo projeto.

---

# 8. Processo de Trabalho

Toda atividade executada por IA deverá seguir obrigatoriamente o fluxo oficial definido em:

- DEVELOPMENT_WORKFLOW.md
- CONTRIBUTING.md
- MASTER_EXECUTION_PLAN.md

Esta política não substitui esses documentos.

Ela define apenas como os agentes deverão se comportar durante sua execução.

---

# 9. Planejamento da Implementação

Toda implementação realizada por um agente de Inteligência Artificial deverá partir de um planejamento previamente aprovado.

A IA não deverá iniciar alterações diretamente no código sem compreender o escopo autorizado.

---

## 9.1. Leitura Obrigatória

Antes de iniciar qualquer atividade, o agente deverá consultar os documentos aplicáveis ao escopo da tarefa.

No mínimo:

- PRD;
- FEATURE_CATALOG;
- CAPABILITY_MAP;
- NEXT_TASK;
- documentação da Capability envolvida.

Quando aplicável, também deverão ser consultados:

- ADRs;
- documentação arquitetural;
- documentação técnica específica.

---

## 9.2. Validação do Escopo

O agente deverá confirmar:

- Sprint ativa;
- Capability;
- Feature;
- Requisitos Funcionais;
- critérios de aceite;
- dependências.

Caso exista qualquer inconsistência documental, a implementação deverá ser interrompida até decisão explícita do responsável pelo projeto.

---

# 10. Desenvolvimento

Durante a implementação, o agente deverá seguir rigorosamente a arquitetura oficial do LifeOS.

---

## Regras

O agente deverá:

- implementar apenas o escopo autorizado;
- preservar a arquitetura;
- manter compatibilidade com os documentos oficiais;
- reutilizar componentes existentes sempre que possível;
- evitar duplicação de código.

---

## Proibições

O agente não deverá:

- criar funcionalidades não solicitadas;
- modificar comportamento existente sem autorização;
- alterar contratos públicos sem aprovação;
- criar soluções paralelas para problemas já resolvidos pela arquitetura.

---

# 11. Atualização da Documentação

Sempre que solicitado, o agente deverá atualizar a documentação correspondente à implementação realizada.

---

## Documentos

Dependendo da alteração, poderão ser atualizados:

- CHANGELOG.md;
- PROJECT_STATUS.md;
- TASK_HISTORY.md;
- NEXT_TASK.md;
- PRD.md;
- FEATURE_CATALOG.md;
- CAPABILITY_MAP.md;
- documentação técnica da Capability.

---

## Consistência

A documentação deverá refletir exatamente o comportamento implementado.

O agente não deverá registrar funcionalidades inexistentes.

---

# 12. Geração de Código

Todo código produzido pela IA deverá obedecer integralmente às políticas oficiais do projeto.

Especialmente:

- CODE_STYLE.md;
- DEPENDENCY_POLICY.md;
- SECURITY_POLICY.md.

---

## Requisitos

O código deverá:

- compilar corretamente;
- possuir tipagem adequada;
- respeitar a arquitetura;
- possuir baixo acoplamento;
- possuir alta coesão.

---

## Reutilização

Antes de criar novos componentes, o agente deverá verificar se já existe solução equivalente na arquitetura oficial.

Evitar duplicação de:

- Services;
- Repositories;
- DTOs;
- Value Objects;
- Domain Events;
- componentes compartilhados.

---

# 13. Testes

Todo código produzido deverá ser validado conforme a política oficial de testes.

O agente deverá seguir integralmente:

**TESTING_POLICY.md**

---

## Obrigatório

Quando aplicável, executar:

- testes unitários;
- testes de integração;
- testes End-to-End;
- testes arquiteturais.

---

## Evidências

O agente somente poderá declarar uma implementação concluída após apresentar evidências reais da execução dos testes.

Declarações sem validação não serão aceitas.

---

# 14. Revisão Técnica

Antes de considerar uma tarefa concluída, o próprio agente deverá revisar sua implementação.

---

## Verificar

- arquitetura;
- dependências;
- nomenclatura;
- organização do código;
- documentação;
- testes.

---

## Objetivo

Identificar e corrigir problemas antes da revisão técnica formal.

---

# 15. Comunicação

Toda comunicação produzida pelo agente deverá ser objetiva, técnica e rastreável.

---

## O agente deverá informar

- o que foi implementado;
- quais arquivos foram alterados;
- quais testes foram executados;
- quais documentos foram atualizados;
- quais limitações permanecem.

---

## O agente não deverá

- exagerar resultados;
- ocultar falhas;
- declarar sucesso sem evidências;
- afirmar execuções que não ocorreram.

---

# 16. Entrega

A entrega produzida pela IA deverá conter todas as informações necessárias para validação.

---

## A entrega deverá incluir

- resumo da implementação;
- arquivos criados;
- arquivos alterados;
- documentação atualizada;
- testes executados;
- evidências produzidas;
- pendências existentes, quando houver.

---

## Definition of Done

A IA somente poderá declarar uma Sprint concluída quando todos os critérios definidos em **DEFINITION_OF_DONE.md** tiverem sido integralmente atendidos.

---

# 17. Contribuições de Inteligência Artificial

Toda contribuição produzida por Inteligência Artificial deverá seguir exatamente o mesmo padrão de qualidade exigido para contribuições humanas.

Não existirão exceções para código gerado por IA.

---

## 17.1. Equivalência

Todo código produzido por IA deverá atender aos mesmos requisitos de:

- arquitetura;
- testes;
- documentação;
- revisão técnica;
- rastreabilidade.

A origem da implementação não altera os critérios de aprovação.

---

## 17.2. Responsabilidade

A utilização de IA não transfere a responsabilidade pela qualidade da entrega.

Toda implementação deverá ser revisada antes de sua aprovação.

---

# 18. Decisões Arquiteturais

Os agentes de Inteligência Artificial deverão respeitar integralmente a arquitetura oficial do LifeOS.

---

## Obrigatório

Os agentes deverão seguir:

- Clean Architecture;
- Domain-Driven Design;
- CQRS;
- Event-Driven Architecture;
- arquitetura oficial das Capabilities;
- ADRs aprovadas.

---

## Proibido

Os agentes não deverão:

- alterar fronteiras arquiteturais;
- modificar dependências entre camadas;
- criar novos padrões arquiteturais;
- substituir tecnologias oficiais;
- ignorar decisões previamente aprovadas.

Qualquer alteração estrutural dependerá de autorização explícita.

---

# 19. Resolução de Conflitos

Quando o agente identificar conflitos entre documentos oficiais, o desenvolvimento deverá ser interrompido.

---

## Exemplos

Conflitos entre:

- PRD;
- Feature Catalog;
- Capability Map;
- ADRs;
- NEXT_TASK;
- documentação técnica.

---

## Procedimento

O agente deverá:

1. identificar o conflito;
2. apresentar as evidências;
3. interromper a implementação;
4. aguardar decisão oficial.

O agente não deverá assumir qual documento está correto.

---

# 20. Escopo da Sprint

Cada Sprint representa um limite rígido para a atuação da Inteligência Artificial.

---

## Regras

O agente deverá implementar apenas:

- Features autorizadas;
- Requisitos Funcionais autorizados;
- documentação relacionada;
- testes correspondentes.

---

## Proibido

O agente não deverá:

- antecipar funcionalidades;
- iniciar outra Sprint;
- implementar requisitos futuros;
- alterar o roadmap.

O planejamento do produto pertence exclusivamente ao responsável pelo projeto.

---

# 21. Uso de Ferramentas

Os agentes deverão utilizar apenas as ferramentas autorizadas durante a execução das atividades.

---

## Exemplos

Quando aplicável:

- Git;
- Python;
- Alembic;
- Pytest;
- Uvicorn;
- ferramentas oficiais de desenvolvimento.

---

## Regras

As ferramentas deverão ser utilizadas apenas para os fins autorizados.

O agente deverá respeitar as políticas definidas pelo projeto para cada ferramenta.

---

# 22. Evidências de Execução

Toda execução realizada pelo agente deverá possuir evidências objetivas.

---

## Exemplos

Quando aplicável:

- saída do pytest;
- cobertura de testes;
- resultado do pip check;
- migrations executadas;
- inicialização da aplicação;
- validação dos endpoints;
- arquivos modificados.

---

## Declarações

O agente não deverá afirmar que executou comandos que não foram efetivamente executados.

Toda afirmação deverá estar respaldada por evidências.

---

# 23. Segurança

Os agentes deverão seguir integralmente a política oficial de segurança do projeto.

Esta política complementa:

**SECURITY_POLICY.md**

---

## Obrigatório

Os agentes deverão:

- proteger informações confidenciais;
- preservar mecanismos de autenticação;
- respeitar controles de autorização;
- evitar exposição de dados sensíveis;
- seguir as políticas de armazenamento de credenciais.

---

## Proibido

Os agentes não deverão:

- inserir credenciais no código;
- registrar segredos em logs;
- remover validações de segurança;
- criar mecanismos inseguros para facilitar o desenvolvimento.

---

# 24. Qualidade da Entrega

Toda entrega produzida pela Inteligência Artificial deverá atender integralmente aos padrões oficiais do projeto.

---

## Critérios

A entrega deverá possuir:

- arquitetura preservada;
- documentação consistente;
- testes aprovados;
- rastreabilidade completa;
- evidências da execução.

---

## Aprovação

A implementação somente poderá ser considerada concluída quando atender simultaneamente:

- CONTRIBUTING.md;
- TESTING_POLICY.md;
- CODE_STYLE.md;
- SECURITY_POLICY.md;
- DEFINITION_OF_DONE.md.

Nenhuma exceção será admitida para código produzido por Inteligência Artificial.

---

# 25. Checklist para Agentes de Inteligência Artificial

Antes de declarar qualquer atividade concluída, o agente deverá verificar integralmente os itens abaixo.

---

## Planejamento

- [ ] Sprint confirmada.
- [ ] Capability confirmada.
- [ ] Feature confirmada.
- [ ] Requisitos Funcionais identificados.
- [ ] Escopo validado.

---

## Implementação

- [ ] Arquitetura preservada.
- [ ] Escopo respeitado.
- [ ] Nenhuma funcionalidade extra implementada.
- [ ] Nenhuma alteração arquitetural não autorizada.

---

## Código

- [ ] Código compilando.
- [ ] Imports válidos.
- [ ] Dependências corretas.
- [ ] Sem código morto.
- [ ] Sem TODOs críticos.
- [ ] Sem FIXMEs críticos.

---

## Testes

- [ ] Testes executados conforme TESTING_POLICY.md.
- [ ] Cobertura dentro da meta.
- [ ] Nenhuma regressão identificada.
- [ ] Evidências registradas.

---

## Documentação

- [ ] Documentação atualizada quando aplicável.
- [ ] Rastreabilidade preservada.
- [ ] Relatório técnico consistente.

---

## Entrega

- [ ] Resumo da implementação.
- [ ] Arquivos criados.
- [ ] Arquivos alterados.
- [ ] Testes executados.
- [ ] Pendências informadas.

---

# 26. Não Conformidades

As situações abaixo impedem a aprovação de uma entrega produzida por Inteligência Artificial.

---

## Escopo

- implementação fora da Sprint;
- alteração de requisitos;
- inclusão de funcionalidades não autorizadas;
- antecipação de Features futuras.

---

## Arquitetura

- violação da Clean Architecture;
- quebra das regras de dependência;
- acoplamento entre Capabilities;
- alteração estrutural sem aprovação.

---

## Código

- erros de compilação;
- imports inválidos;
- dependências quebradas;
- código incompleto;
- inconsistência com os padrões oficiais.

---

## Testes

- ausência de evidências;
- testes falhando;
- cobertura abaixo da meta;
- regressões conhecidas.

---

## Documentação

- documentação inconsistente;
- rastreabilidade incompleta;
- documentação desatualizada.

Enquanto existir qualquer não conformidade crítica, a implementação não poderá ser considerada concluída.

---

# 27. Auditoria

Toda contribuição produzida por Inteligência Artificial deverá permitir auditoria completa.

---

## Informações mínimas

Sempre que aplicável, deverá ser possível identificar:

- Sprint;
- Capability;
- Feature;
- Requisitos Funcionais;
- arquivos modificados;
- documentação atualizada;
- testes executados;
- evidências produzidas;
- limitações identificadas.

---

## Transparência

A auditoria deverá permitir verificar exatamente:

- o que foi solicitado;
- o que foi implementado;
- o que permaneceu pendente;
- quais decisões dependeram de aprovação humana.

---

# 28. Melhoria Contínua

Os agentes deverão evoluir continuamente sua forma de trabalhar dentro do projeto.

Essa evolução deverá ocorrer sem alterar a arquitetura ou os padrões oficiais previamente aprovados.

---

## Objetivos

Os agentes deverão buscar continuamente:

- maior qualidade do código;
- menor complexidade;
- melhor legibilidade;
- maior reutilização;
- maior consistência documental;
- redução de retrabalho.

---

## Restrições

Melhorias espontâneas não poderão:

- alterar requisitos;
- modificar comportamento;
- introduzir novas tecnologias;
- mudar padrões oficiais;
- substituir decisões arquiteturais.

Toda melhoria estrutural deverá passar pelo processo formal de aprovação.

---

# 29. Convivência entre Agentes

O LifeOS poderá utilizar diferentes agentes de Inteligência Artificial durante seu ciclo de desenvolvimento.

Todos deverão atuar de forma complementar e seguir exatamente os mesmos padrões de engenharia.

---

## Regras

Independentemente do fornecedor ou modelo utilizado, todos os agentes deverão:

- respeitar a arquitetura oficial;
- seguir os documentos de governança;
- preservar a rastreabilidade;
- manter compatibilidade entre suas entregas.

Nenhum agente deverá assumir que possui prioridade sobre outro.

As decisões oficiais do projeto sempre prevalecerão sobre sugestões individuais dos agentes.

---

# 30. Regra Final

A Inteligência Artificial é uma ferramenta de apoio ao desenvolvimento do LifeOS.

Ela acelera a implementação, auxilia na revisão técnica e aumenta a produtividade, mas não substitui as decisões de arquitetura, produto ou engenharia.

Toda contribuição produzida por IA deverá:

- respeitar integralmente a arquitetura oficial do projeto;
- seguir todas as políticas de governança;
- manter a rastreabilidade completa;
- produzir evidências reais de execução;
- preservar a qualidade do software;
- atuar estritamente dentro do escopo autorizado.

O sucesso de uma entrega não será medido pela quantidade de código gerado, mas pela conformidade com a arquitetura, pelas evidências apresentadas e pela capacidade de evoluir o projeto de forma segura, consistente e sustentável.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial para utilização de Inteligência Artificial no desenvolvimento do projeto LifeOS. |