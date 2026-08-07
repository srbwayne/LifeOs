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
