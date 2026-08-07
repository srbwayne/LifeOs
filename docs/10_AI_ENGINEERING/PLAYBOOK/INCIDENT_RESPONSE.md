# Incident Response

## 1. Objetivo

Este documento define a resposta aos incidentes que interrompem o processo oficial de engenharia do LifeOS. Seu escopo é exclusivamente processual e tem como finalidade restabelecer o fluxo definido pelo [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md).

## 2. Princípios

- Um incidente interrompe ou compromete o processo de engenharia.
- Todo incidente deve ser registrado.
- Todo incidente deve possuir um responsável.
- Todo incidente deve possuir uma classificação.
- Todo incidente deve terminar com o retorno seguro ao fluxo oficial.
- Documentos normativos prevalecem sobre este documento.

## 3. O que é um Incidente

Um incidente é uma condição identificada que interrompe, bloqueia ou compromete um estado do processo oficial de engenharia e exige tratamento autorizado antes da continuidade.

São exemplos de incidentes do processo:

- bloqueio de integração;
- conflito arquitetural;
- impedimento de merge;
- falha em Gate;
- perda de rastreabilidade;
- interrupção da Sprint.

Falhas técnicas isoladas somente constituem incidentes deste documento quando afetam o fluxo oficial. O tratamento da causa técnica permanece sob a documentação normativa correspondente.

## 4. Classificação dos Incidentes

### Classe A

Bloqueia totalmente o processo.

Exemplos:

- tarefa sem autorização válida;
- conflito de produto ou arquitetura que impeça a continuidade;
- perda de rastreabilidade essencial;
- interrupção integral da Sprint.

### Classe B

Bloqueia a integração.

Exemplos:

- Gate obrigatório não atendido;
- revisão obrigatória pendente;
- aprovação necessária indisponível;
- divergência que impeça o merge.

### Classe C

Não bloqueia o fluxo.

Exemplos:

- melhoria processual não bloqueante identificada;
- ajuste documental futuro devidamente registrado;
- risco residual aceito pelo responsável autorizado;
- oportunidade de atualização de checklist sem impacto na entrega atual.

## 5. Fluxo de Resposta

```text
Incidente
  ↓
Identificação
  ↓
Classificação
  ↓
Responsável
  ↓
Correção autorizada
  ↓
Validação
  ↓
Retorno ao ENGINEERING_PLAYBOOK
```

O fluxo representa os estados da resposta ao incidente. O tratamento somente avança sob a responsabilidade e a autorização definidas pela governança.

## 6. Escalonamento

| Tipo de incidente | Responsável pelo escalonamento |
|---|---|
| Produto ou prioridade | Product Owner |
| Arquitetura ou ADR | Arquiteto de Software |
| Implementação | Executor, com revisão técnica |
| Qualidade ou Gate | Revisor Técnico |
| Rastreabilidade ou conformidade | Auditor |
| Integração ou merge | Responsável autorizado pela governança |
| Release | Product Owner, com validação técnica |

O escalonamento utiliza papéis e preserva as autoridades definidas em [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md).

## 7. Critérios para Retorno ao Fluxo

O processo pode retornar ao fluxo oficial somente quando:

- [ ] Incidente resolvido.
- [ ] Evidências registradas.
- [ ] Validações concluídas.
- [ ] Checklist correspondente atendido em [CHECKLISTS.md](CHECKLISTS.md).
- [ ] Responsável autorizou o retorno.

O retorno deve ocorrer no estado aplicável do [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md).

## 8. Pós-Incidente

Após o incidente, verificar somente:

- necessidade de ADR;
- necessidade de atualização documental;
- necessidade de melhoria de processo;
- necessidade de atualização de checklist.

As necessidades identificadas permanecem sujeitas à autorização e aos documentos normativos aplicáveis.

## 9. Relação com a Governança

```text
Governança
  ↓
Playbook
  ↓
Incident Response
  ↓
Retorno ao ENGINEERING_PLAYBOOK
```

Este documento coordena a resposta processual e não substitui políticas, processos ou critérios normativos. Em caso de conflito, prevalece sempre o documento normativo.

## 10. Referências

### Referências do Playbook

- [README.md](README.md)
- [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md)
- [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md)
- [CHECKLISTS.md](CHECKLISTS.md)

### Documentação Normativa

- [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md)
- [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md)
- [TESTING_POLICY.md](../TESTING_POLICY.md)
- [CODE_REVIEW_CHECKLIST.md](../CODE_REVIEW_CHECKLIST.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [RELEASE_PROCESS.md](../RELEASE_PROCESS.md)
- [ADR_TEMPLATE.md](../ADR_TEMPLATE.md)
