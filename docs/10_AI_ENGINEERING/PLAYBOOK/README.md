# Playbook

## 1. O que é o Playbook

O Playbook é a porta de entrada para os processos permanentes de engenharia do LifeOS. Ele existe para orientar pessoas e agentes de IA até o documento adequado em cada situação.

O Playbook não é fonte normativa, não substitui os documentos oficiais e não redefine suas regras. Sua função é coordenar a utilização da governança existente.

## 2. Princípios

- O Playbook coordena processos.
- Os documentos normativos continuam sendo as fontes de verdade.
- Cada documento possui responsabilidade única.
- A documentação deve evitar redundâncias.

## 3. Como utilizar o Playbook

```text
Leitor
  ↓
README
  ↓
Documento adequado
  ↓
Governança correspondente
```

O leitor inicia neste README, identifica o documento adequado à situação e consulta a governança correspondente quando houver uma regra normativa envolvida.

Em caso de conflito entre o Playbook e qualquer documento normativo do projeto, prevalece sempre o documento normativo.

## 4. Estrutura do Pacote

```text
PLAYBOOK/
├── README.md
├── ENGINEERING_PLAYBOOK.md
├── AI_AGENT_WORKFLOW.md
├── CHECKLISTS.md
└── INCIDENT_RESPONSE.md
```

## 5. Quando consultar cada documento

| Situação | Documento |
|---|---|
| Iniciar uma Sprint | [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md) |
| Atuar como agente de IA | [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md) |
| Validar uma etapa | [CHECKLISTS.md](CHECKLISTS.md) |
| Tratar uma interrupção do fluxo | [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) |

## 6. Relação com a Governança

```text
Governança
  ↓
Playbook
  ↓
Execução
```

O Playbook nunca substitui:

- [COMMIT_GUIDELINES.md](../COMMIT_GUIDELINES.md);
- [BRANCHING_STRATEGY.md](../BRANCHING_STRATEGY.md);
- [TESTING_POLICY.md](../TESTING_POLICY.md);
- [RELEASE_PROCESS.md](../RELEASE_PROCESS.md);
- [CODE_STYLE.md](../CODE_STYLE.md);
- [VERSIONING.md](../VERSIONING.md).

O Playbook apenas coordena a consulta e a aplicação dos documentos normativos.

## 7. Referências

### Referências Internas

- [ENGINEERING_PLAYBOOK.md](ENGINEERING_PLAYBOOK.md)
- [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md)
- [CHECKLISTS.md](CHECKLISTS.md)
- [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

### Documentação Normativa

As principais fontes normativas utilizadas pelo Playbook são:

- [DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md)
- [COMMIT_GUIDELINES.md](../COMMIT_GUIDELINES.md)
- [BRANCHING_STRATEGY.md](../BRANCHING_STRATEGY.md)
- [TESTING_POLICY.md](../TESTING_POLICY.md)
- [RELEASE_PROCESS.md](../RELEASE_PROCESS.md)
- [CODE_STYLE.md](../CODE_STYLE.md)
- [AI_DEVELOPMENT_POLICY.md](../AI_DEVELOPMENT_POLICY.md)
