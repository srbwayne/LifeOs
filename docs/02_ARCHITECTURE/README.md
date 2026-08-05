# Arquitetura do LifeOS

## README

**Versão:** 1.0

**Status:** Documento Oficial

---

# Objetivo

Esta pasta contém toda a documentação arquitetural oficial do LifeOS.

Seu objetivo é definir como o sistema é organizado internamente, quais princípios arquiteturais devem ser seguidos e como cada camada do software deve interagir.

Os documentos desta pasta são a referência oficial para decisões técnicas relacionadas à implementação.

---

# Escopo

A documentação arquitetural descreve:

- Estrutura geral da aplicação
- Organização em camadas
- Organização dos módulos
- Dependências entre componentes
- Comunicação entre módulos
- Regras arquiteturais
- Decisões de projeto
- Evolução futura da arquitetura

Não descreve regras de negócio específicas. Essas informações pertencem ao domínio do produto e estão documentadas no PRD e nos documentos da pasta `01_PRODUCT`.

---

# Objetivos Arquiteturais

A arquitetura do LifeOS foi projetada para atender aos seguintes objetivos:

- Separação clara de responsabilidades
- Alta coesão
- Baixo acoplamento
- Facilidade de manutenção
- Facilidade de testes
- Evolução incremental
- Independência de tecnologia
- Reutilização de componentes
- Escalabilidade funcional

---

# Princípios Arquiteturais

Toda implementação deverá respeitar os seguintes princípios:

- O domínio nunca depende da interface.
- A interface nunca contém regras de negócio.
- Toda persistência é realizada através de Repositories.
- Toda regra de negócio pertence ao domínio ou à camada de Application.
- Toda comunicação entre módulos deve respeitar as regras de dependência.
- Tecnologias são substituíveis sem alterar o domínio.

---

# Padrões Arquiteturais Adotados

O LifeOS adota a combinação dos seguintes padrões:

- Clean Architecture
- Domain-Driven Design (DDD)
- Modular Monolith
- Repository Pattern
- Service Layer
- Dependency Injection (quando aplicável)
- CQRS Light (Use Cases separados por comandos e consultas quando fizer sentido)
- Domain Events

Cada padrão será detalhado em documentos específicos desta pasta.

---

# Organização da Documentação

A documentação arquitetural está organizada na seguinte ordem:

## 1. 01_OVERVIEW.md

Apresenta uma visão geral da arquitetura do LifeOS, seus módulos e a relação entre eles.

---

## 2. 02_CLEAN_ARCHITECTURE.md

Define as camadas do sistema, responsabilidades e regras de dependência.

---

## 3. 03_DDD.md

Descreve o modelo de domínio, entidades, agregados, serviços de domínio e linguagem ubíqua.

---

## 4. 05_MODULAR_MONOLITH.md

Explica a estratégia de organização modular adotada pelo projeto e como novos módulos devem ser incorporados.

---

## 5. 06_FOLDER_STRUCTURE.md

Documenta a estrutura oficial de diretórios do projeto e a responsabilidade de cada pasta.

---

## 6. 07_DEPENDENCY_RULES.md

Define quais módulos podem depender de outros e quais dependências são proibidas.

---

## 7. 08_EVENTS.md

Documenta a estratégia de eventos do domínio, comunicação entre módulos e desacoplamento.

---

## 8. 09_DECISION_LOG.md

Registra decisões arquiteturais importantes tomadas durante a evolução do projeto.

---

# Fluxo de Leitura

Todo desenvolvedor ou agente de IA deve seguir a seguinte ordem antes de iniciar qualquer implementação:

1. MANIFESTO.md
2. PRINCIPLES.md
3. GLOSSARY.md
4. PRODUCT_VISION.md
5. FEATURE_CATALOG.md
6. PRD.md
7. OVERVIEW.md
8. Demais documentos da arquitetura
9. Documentação técnica correspondente

Essa sequência garante que decisões técnicas estejam sempre alinhadas aos objetivos do produto.

---

# Como Utilizar Esta Documentação

Antes de implementar uma funcionalidade:

1. Identificar a Capability correspondente.
2. Consultar o PRD e os requisitos relacionados.
3. Ler os documentos arquiteturais necessários.
4. Verificar impactos em outros módulos.
5. Implementar respeitando as regras de dependência.
6. Atualizar documentação quando necessário.

---

# Regras para Agentes de IA

Todo agente de IA deverá:

- Ler a documentação arquitetural antes de gerar código.
- Nunca criar novas camadas sem justificativa documentada.
- Nunca violar as regras de dependência.
- Nunca inserir regras de negócio na interface.
- Nunca acessar diretamente a infraestrutura a partir da interface.
- Atualizar a documentação quando uma decisão arquitetural for alterada.

---

# Relação com os Demais Documentos

A arquitetura depende dos documentos da pasta `00_FOUNDATION` e `01_PRODUCT`.

As pastas `03_DATABASE`, `04_BACKEND`, `05_FRONTEND`, `06_GAME_ENGINE`, `07_ANALYTICS`, `08_AI` e `09_TESTS` deverão seguir obrigatoriamente as diretrizes definidas nesta pasta.

---

# Estrutura da Pasta

```
02_ARCHITECTURE/

README.md

OVERVIEW.md

docs/02_ARCHITECTURE/02_CLEAN_ARCHITECTURE.md

docs/02_ARCHITECTURE/03_DDD.md

docs/02_ARCHITECTURE/05_MODULAR_MONOLITH.md

docs/02_ARCHITECTURE/06_FOLDER_STRUCTURE.md

DEPENDENCY_RULES.md

docs/02_ARCHITECTURE/08_EVENTS.md

ADR.md
```

---

# Critérios de Aceite

A documentação arquitetural será considerada completa quando:

- Todos os documentos desta pasta estiverem concluídos.
- As regras de arquitetura estiverem claramente definidas.
- Os diagramas arquiteturais estiverem atualizados.
- As decisões arquiteturais estiverem registradas.
- A arquitetura puder ser compreendida sem necessidade de consultar o código-fonte.

---

# Declaração Final

A arquitetura do LifeOS representa a fundação técnica da plataforma.

Ela existe para garantir que o sistema possa evoluir continuamente sem comprometer sua qualidade, organização e capacidade de manutenção.

Toda implementação futura deverá respeitar os princípios e diretrizes definidos nesta documentação.
