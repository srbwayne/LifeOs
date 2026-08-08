# AI Agent Workflow

## 1. Objetivo

Este documento organiza a colaboração entre participantes humanos e agentes de Inteligência Artificial durante o ciclo de desenvolvimento do LifeOS. Ele define papéis, responsabilidades, limites de atuação, autoridade, escalonamento e resolução de conflitos sem depender de ferramentas específicas.

O documento não substitui políticas ou processos oficiais e não concede autoridade autônoma aos agentes. Cada participante atua apenas dentro das responsabilidades atribuídas pela governança.

## 2. Princípios

- Papéis são independentes das pessoas ou ferramentas que os desempenham.
- Agentes não possuem autoridade própria.
- Decisões devem ser rastreáveis até o papel autorizado e a governança aplicável.
- Nenhum agente altera produto ou arquitetura sem autorização.
- Evidências verificáveis prevalecem sobre declarações de execução.
- Conflitos devem ser interrompidos e escalados ao papel competente.
- Documentos normativos prevalecem sobre o Playbook.
- A troca de ferramenta não altera o processo, as responsabilidades ou a autoridade.

## 3. Papéis

O papel determina a responsabilidade e a autoridade no processo, independentemente da identidade da pessoa ou da ferramenta que o desempenha. Um participante poderá assumir mais de um papel quando a governança permitir, preservando os limites de cada atuação.

### Product Owner

Responsável pela direção do produto, prioridades, escopo funcional e autorização das tarefas.

### Arquiteto de Software

Responsável pelas decisões arquiteturais, fronteiras, padrões e aprovação de alterações estruturais.

### Executor

Responsável pela implementação autorizada, validações, commits, evidências e preparação da entrega.

### Revisor Técnico

Responsável por revisar código, documentação, arquitetura, testes, riscos e aderência aos critérios oficiais.

### Auditor

Responsável por verificar rastreabilidade, evidências, conformidade e consistência entre documentos, código e execução.

## 4. Responsabilidades

### Product Owner

- Pode definir direção, prioridades e escopo funcional.
- Deve autorizar tarefas e resolver decisões de produto.
- Não pode decidir sozinho alterações arquiteturais ou declarar validações técnicas sem evidências.

### Arquiteto de Software

- Pode definir e aprovar decisões, fronteiras e restrições arquiteturais.
- Deve avaliar impactos estruturais e registrar as decisões aplicáveis.
- Não pode alterar unilateralmente a direção ou o escopo funcional do produto.

### Executor

- Pode planejar e executar o trabalho expressamente autorizado dentro das restrições vigentes.
- Deve validar o estado real, preservar a arquitetura, produzir evidências e preparar a entrega para revisão.
- Não pode decidir sozinho conflitos de produto, arquitetura ou outras matérias reservadas pela governança.

### Revisor Técnico

- Pode emitir parecer técnico, solicitar correções e verificar a aderência aos critérios oficiais.
- Deve revisar riscos, evidências, código, documentação, arquitetura e validações pertinentes.
- Não pode ampliar escopo, redefinir produto ou substituir a autoridade do responsável pela decisão.

### Auditor

- Pode examinar rastreabilidade, conformidade e consistência do processo.
- Deve registrar achados com evidências e encaminhar não conformidades ao papel competente.
- Não pode corrigir ou reinterpretar silenciosamente decisões já aprovadas.

As responsabilidades detalhadas de participação e execução permanecem nos documentos normativos referenciados por este workflow.

## 5. Matriz de Autoridade

| Assunto | Decide | Executa | Revisa | Aprova |
|---|---|---|---|---|
| Visão e prioridade de produto | Product Owner | Product Owner | Arquiteto de Software e Revisor Técnico | Product Owner |
| Escopo da Sprint | Product Owner | Executor | Arquiteto de Software e Revisor Técnico | Product Owner |
| Requisitos funcionais | Product Owner | Executor | Arquiteto de Software e Revisor Técnico | Product Owner |
| Arquitetura | Arquiteto de Software | Executor | Revisor Técnico e Auditor | Arquiteto de Software |
| ADRs | Arquiteto de Software | Executor | Revisor Técnico e Auditor | Arquiteto de Software |
| Implementação | Executor, dentro do escopo autorizado | Executor | Revisor Técnico | Revisor Técnico ou responsável exigido pela natureza da alteração |
| Documentação técnica | Responsável pelo tema | Executor | Revisor Técnico e Auditor | Responsável pelo tema |
| Testes | Revisor Técnico, conforme a governança | Executor | Revisor Técnico | Revisor Técnico |
| Commits | Executor, conforme a governança | Executor | Revisor Técnico | Responsável pela integração |
| Pull Request | Executor, conforme a tarefa autorizada | Executor | Revisor Técnico | Responsável pela integração |
| Merge | Responsável autorizado pela governança | Executor autorizado | Revisor Técnico | Responsável autorizado pela governança |
| Versionamento | Product Owner, com avaliação técnica | Executor | Revisor Técnico | Product Owner |
| Release | Product Owner, com validação técnica | Executor autorizado | Revisor Técnico e Auditor | Product Owner |
| Tratamento de incidentes | Responsável pelo tema do incidente | Executor autorizado | Revisor Técnico e Auditor | Responsável pelo tema do incidente |

A matriz atribui autoridade aos papéis definidos pela governança. O uso de um agente para desempenhar um papel não transfere autoridade à ferramenta.

## 6. Fluxo de Colaboração

```text
Product Owner
  ↓
Tarefa autorizada
  ↓
Arquiteto de Software
  ↓
Direção e restrições arquiteturais
  ↓
Executor
  ↓
Plano e implementação
  ↓
Revisor Técnico
  ↓
Parecer e correções
  ↓
Responsável pela aprovação
  ↓
Integração ou retorno para ajustes
```

O fluxo representa somente a colaboração e a transferência de responsabilidade entre papéis. O ciclo completo de engenharia permanece no [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md).

## 7. Escalonamento de Decisões

| Tipo de decisão | Escalonar para |
|---|---|
| Produto | Product Owner |
| Arquitetura | Arquiteto de Software |
| Implementação | Executor, com revisão técnica |
| Qualidade | Revisor Técnico |
| Conflito documental | Arquiteto de Software e Product Owner, conforme o tema |
| Segurança crítica | Arquiteto de Software e responsável autorizado |
| Release | Product Owner, com validação técnica |

O Executor não resolve autonomamente conflitos de produto ou arquitetura. Quando uma decisão ultrapassar sua responsabilidade, o trabalho afetado deverá aguardar a manifestação do papel competente.

## 8. Resolução de Conflitos

1. Identificar o conflito.
2. Registrar as evidências disponíveis.
3. Classificar o tipo de decisão.
4. Interromper a atividade afetada.
5. Escalar ao papel competente.
6. Registrar a decisão tomada.
7. Atualizar o plano autorizado.
8. Retomar o fluxo.

Não existe prioridade entre agentes. Sugestões não substituem decisões, e autoridade não é definida pela ferramenta. O responsável pelo tema decide, e nenhuma implementação prossegue enquanto houver conflito bloqueante aberto.

## 9. Substituição de Agentes

Ferramentas e participantes que desempenham papéis operacionais são substituíveis quando a governança permitir. Os papéis, seus limites e sua autoridade permanecem inalterados durante a substituição.

O novo agente ou participante deverá receber o contexto necessário, preservar a rastreabilidade do trabalho anterior e respeitar as decisões aprovadas. Nenhuma decisão poderá ser reinterpretada silenciosamente em razão da troca.

| Papel | Implementação possível | Substituível |
|---|---|---|
| Executor | Agente ou humano autorizado | Sim |
| Revisor Técnico | Agente ou humano autorizado | Sim |
| Auditor | Agente ou humano autorizado | Sim |
| Arquiteto de Software | Responsável designado | Conforme a governança |
| Product Owner | Responsável pelo produto | Conforme a governança |

## 10. Continuidade e Transferência de Contexto

A continuidade do trabalho exige uma transferência de contexto suficiente para que o próximo participante compreenda o estado real e os limites da atuação. Quando aplicável, a transferência deverá incluir:

- tarefa autorizada;
- estado atual;
- branch;
- commits;
- Pull Request;
- documentos consultados;
- decisões aprovadas;
- testes executados;
- pendências;
- bloqueios;
- próxima ação permitida.

O novo participante deverá validar o estado real antes de prosseguir. A transferência de contexto não concede novas permissões nem modifica decisões existentes.

## 11. Relação com a Governança

Este documento não substitui [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md), [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md), [CONTRIBUTING.md](../CONTRIBUTING.md), [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md), [AGENTS.md](../../../AGENTS.md) ou instruções locais aplicáveis. Ele define apenas a colaboração entre papéis durante o processo de engenharia.

Em caso de conflito entre este documento e qualquer documento normativo do projeto, prevalece sempre o documento normativo. A governança determina a autoridade; o Playbook apenas coordena sua aplicação no fluxo de colaboração.

## 12. Referências

### Referências do Playbook

- [README.md](README.md)
- [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md)
- [CHECKLISTS.md](CHECKLISTS.md)
- [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

### Documentação Normativa

- [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md)
- [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [DEFINITION_OF_DONE.md](../DEFINITION_OF_DONE.md)
- [CODE_REVIEW_CHECKLIST.md](../CODE_REVIEW_CHECKLIST.md)
- [AGENTS.md](../../../AGENTS.md)
- [GEMINI.md](../../../GEMINI.md)
- [GEMINI_AGENT.md](../GEMINI_AGENT.md)
