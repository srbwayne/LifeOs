# Engineering Playbook

## 1. Objetivo

O Engineering Playbook coordena o ciclo oficial de engenharia do LifeOS. Seu objetivo é integrar a utilização dos documentos especializados durante o processo de desenvolvimento.

Este documento não substitui documentos normativos, não cria novas políticas e não assume responsabilidades pertencentes a outras fontes oficiais. Ele apenas coordena sua utilização.

## 2. Princípios

- Processo acima de ferramentas.
- Governança acima de implementação.
- Autoridade baseada em papéis definidos pela governança.
- Documentos especializados possuem responsabilidade única.
- O Playbook coordena a utilização dos documentos especializados.
- Documentos normativos prevalecem sobre o Playbook.
- Rastreabilidade é obrigatória.
- Decisões devem ser verificáveis.

## 3. Escopo

O Engineering Playbook coordena:

- estados do processo;
- transições;
- Gates;
- integração entre documentos especializados;
- fluxo oficial.

O Engineering Playbook não coordena:

- commits;
- branches;
- testes;
- versionamento;
- revisão técnica;
- incidentes;
- agentes;
- arquitetura de software.

Cada tema permanece sob a responsabilidade do documento especializado correspondente.

## 4. Arquitetura do Processo

```text
                         Governança
                             ↓
                    Engineering Playbook
                             ↓
        ┌────────────────────┼────────────────────────┐
        ↓                    ↓                        ↓
AI Agent Workflow       Checklists            Incident Response
        └────────────────────┼────────────────────────┘
                             ↓
                   Execução da Engenharia
```

A governança define. O Engineering Playbook coordena. Os documentos especializados apoiam. A execução aplica.

## 5. Modelo de Estados

O processo oficial de engenharia é modelado como uma máquina de estados. Todo trabalho percorre estados bem definidos, que organizam sua evolução sem estabelecer regras próprias.

Cada estado possui obrigatoriamente:

- objetivo;
- critérios de entrada;
- execução;
- Gate;
- critérios de saída;
- próximo estado.

```text
Estado
  ↓
Critérios de Entrada
  ↓
Execução
  ↓
Gate
  ↓
Critérios de Saída
  ↓
Próximo Estado
```

Nenhum estado pode ser ignorado sem autorização da governança. Os estados utilizam documentos especializados e não criam regras próprias.

## 6. Gates

Gate é o mecanismo oficial que autoriza ou impede a transição entre estados.

Um Gate:

- valida critérios;
- consulta documentos especializados;
- registra evidências;
- permite ou bloqueia a transição.

```text
Estado Atual
  ↓
Gate
  ↓
Critérios atendidos?
  ├── Sim → Próximo Estado
  └── Não → Permanecer no Estado Atual
```

O Gate aplica os critérios definidos pela governança e pelos documentos normativos correspondentes. Ele não cria critérios próprios.

## 7. Transições

Toda transição ocorre entre dois estados válidos e representa uma mudança governada no processo oficial de engenharia.

Toda transição possui:

- estado de origem;
- Gate;
- decisão;
- estado de destino.

Uma transição nunca ocorre diretamente. Toda mudança entre estados é mediada por um Gate.

### Transição Autorizada

Os critérios do Gate foram atendidos.

```text
Estado A
  ↓
Gate
  ↓
Critérios atendidos
  ↓
Estado B
```

### Transição Bloqueada

Os critérios do Gate não foram atendidos.

```text
Estado A
  ↓
Gate
  ↓
Critérios não atendidos
  ↓
Permanece em Estado A
```

### Transição Suspensa

Existe um incidente de processo.

```text
Estado A
  ↓
Gate
  ↓
Incidente
  ↓
INCIDENT_RESPONSE.md
  ↓
Retorno ao estado apropriado
```

A transição permanece suspensa sob a referência de [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md).

### Transição Excepcional

A transição excepcional ocorre somente mediante autorização da governança.

- Não representa o fluxo normal.
- Deve ser registrada.
- Deve possuir justificativa.
- Permanece sujeita à governança.

Princípios das transições:

- toda transição possui origem;
- toda transição possui destino;
- nenhuma transição ignora um Gate;
- incidentes suspendem transições;
- exceções dependem da governança;
- documentos especializados executam as validações.

## 8. Integração com AI Agent Workflow

O [AI_AGENT_WORKFLOW.md](AI_AGENT_WORKFLOW.md) deve ser consultado quando o processo exigir definição ou confirmação de responsabilidades, papéis, autoridade ou colaboração entre participantes.

O Engineering Playbook coordena essa consulta sem assumir autoridade. Após a definição dos papéis, o processo retorna ao Engineering Playbook.

## 9. Integração com Checklists

O [CHECKLISTS.md](CHECKLISTS.md) deve ser utilizado quando o processo exigir validação de um estado, confirmação de critérios ou autorização para prosseguir.

O Engineering Playbook coordena essa validação sem executar suas verificações. Após a validação, o processo retorna ao Engineering Playbook.

## 10. Integração com Incident Response

O [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) deve ser acionado quando houver interrupção do fluxo, incidente processual ou suspensão de uma transição que exija retorno seguro.

O Engineering Playbook coordena o acionamento sem executar a resposta. Após o encerramento do incidente, o processo retorna ao Engineering Playbook.

```text
                 Engineering Playbook
                          │
                          ▼
                     Estado Atual
                          │
                          ▼
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    AI Agent          Checklists         Incident
    Workflow                              Response
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                 Engineering Playbook
                          │
                          ▼
                    Próximo Estado
```

O diagrama representa coordenação entre o Engineering Playbook e os documentos especializados, sem estabelecer dependência hierárquica.
