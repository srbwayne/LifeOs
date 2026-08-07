# Checklists

## 1. Objetivo

Este documento valida a passagem entre estados do processo oficial de engenharia. Ele não ensina procedimentos nem estabelece regras próprias.

## 2. Princípios

- Checklist valida.
- Checklist não explica.
- Checklists validam estados, não tarefas.
- Documentos normativos permanecem como fontes de verdade.
- Nenhum item de checklist cria regra nova.
- Toda validação possui um documento de referência.

## 3. Como utilizar os Checklists

Utilize o checklist correspondente ao estado atual e confirme suas condições antes da transição:

```text
Estado
  ↓
Checklist
  ↓
Validação
  ↓
Próximo Estado
```

Quando um item não estiver atendido, a transição permanece pendente conforme o documento normativo referenciado.

## 4. Checklists por Estado

### Planejamento

- [ ] Tarefa autorizada em [NEXT_TASK.md](../../../NEXT_TASK.md).
- [ ] Escopo aprovado conforme [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md).
- [ ] Requisitos e rastreabilidade identificados conforme [CONTRIBUTING.md](../CONTRIBUTING.md).
- [ ] Impacto arquitetural classificado conforme [docs/02_ARCHITECTURE/](../../02_ARCHITECTURE/).
- [ ] Plano compatível com [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md).

### Implementação

- [ ] Escopo implementado sem ampliação da tarefa autorizada conforme [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md).
- [ ] Arquitetura preservada conforme [docs/02_ARCHITECTURE/](../../02_ARCHITECTURE/).
- [ ] Código aderente a [CODE_STYLE.md](../CODE_STYLE.md).
- [ ] Dependências aderentes a [DEPENDENCY_POLICY.md](../DEPENDENCY_POLICY.md).
- [ ] Evidências de execução disponíveis conforme [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md).

### Revisão

- [ ] Revisão técnica concluída conforme [CODE_REVIEW_CHECKLIST.md](../CODE_REVIEW_CHECKLIST.md).
- [ ] Testes executados conforme [TESTING_POLICY.md](../TESTING_POLICY.md).
- [ ] Critérios de conclusão verificados conforme [DEFINITION_OF_DONE.md](../DEFINITION_OF_DONE.md).
- [ ] Rastreabilidade revisada conforme [CONTRIBUTING.md](../CONTRIBUTING.md).
- [ ] Pendências e riscos registrados conforme [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md).

### Integração

- [ ] Commits conformes a [COMMIT_GUIDELINES.md](../COMMIT_GUIDELINES.md).
- [ ] Branch e estratégia de integração conformes a [BRANCHING_STRATEGY.md](../BRANCHING_STRATEGY.md).
- [ ] Revisões e aprovações exigidas concluídas conforme [CONTRIBUTING.md](../CONTRIBUTING.md).
- [ ] Evidências finais disponíveis conforme [TESTING_POLICY.md](../TESTING_POLICY.md).
- [ ] Integração autorizada conforme [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md).

### Encerramento

- [ ] Definition of Done atendida conforme [DEFINITION_OF_DONE.md](../DEFINITION_OF_DONE.md).
- [ ] Registros operacionais atualizados conforme [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md).
- [ ] Rastreabilidade da entrega preservada conforme [CONTRIBUTING.md](../CONTRIBUTING.md).
- [ ] Versionamento validado conforme [VERSIONING.md](../VERSIONING.md).
- [ ] Encerramento ou Release autorizado conforme [RELEASE_PROCESS.md](../RELEASE_PROCESS.md).

## 5. Checklists Especiais

### Mudança Arquitetural

- [ ] Impacto arquitetural identificado conforme [docs/02_ARCHITECTURE/](../../02_ARCHITECTURE/).
- [ ] Decisão arquitetural registrada ou referenciada conforme [ADR_TEMPLATE.md](../ADR_TEMPLATE.md).
- [ ] Aprovação arquitetural disponível conforme [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md).
- [ ] Testes arquiteturais validados conforme [TESTING_POLICY.md](../TESTING_POLICY.md).

### Mudança de Banco

- [ ] Alteração autorizada conforme [DATABASE.md](../../03_DATABASE/DATABASE.md).
- [ ] Compatibilidade e integridade validadas conforme [DATABASE.md](../../03_DATABASE/DATABASE.md).
- [ ] Evidências de migration disponíveis conforme [TESTING_POLICY.md](../TESTING_POLICY.md).
- [ ] Revisão técnica concluída conforme [CODE_REVIEW_CHECKLIST.md](../CODE_REVIEW_CHECKLIST.md).

### Hotfix

- [ ] Classificação de Hotfix confirmada conforme [BRANCHING_STRATEGY.md](../BRANCHING_STRATEGY.md).
- [ ] Escopo restrito à correção autorizada conforme [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md).
- [ ] Regressão validada conforme [TESTING_POLICY.md](../TESTING_POLICY.md).
- [ ] Critérios de entrega atendidos conforme [RELEASE_PROCESS.md](../RELEASE_PROCESS.md).

### Incidente

- [ ] Incidente registrado conforme [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md).
- [ ] Responsável e severidade identificados conforme [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md).
- [ ] Evidências preservadas conforme [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md).
- [ ] Estado de continuidade validado conforme [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md).

## 6. Relação com a Governança

```text
Governança
  ↓
Playbook
  ↓
Checklists
  ↓
Execução
```

Os checklists apenas verificam condições definidas pela governança. Eles não substituem políticas, processos ou qualquer outro documento normativo. Em caso de conflito, prevalece sempre o documento normativo.

## 7. Referências

### Referências do Playbook

- [README.md](README.md)
- [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md)
- [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md)
- [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

### Documentação Normativa

- [TESTING_POLICY.md](../TESTING_POLICY.md)
- [CODE_REVIEW_CHECKLIST.md](../CODE_REVIEW_CHECKLIST.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [COMMIT_GUIDELINES.md](../COMMIT_GUIDELINES.md)
- [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md)
- [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md)
