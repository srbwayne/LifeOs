# VALIDATION

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Validação da Interface  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, Design System

---

# 1. Objetivo

Este documento define a arquitetura oficial de validação da camada de Frontend do LifeOS.

Seu objetivo é padronizar todas as validações realizadas durante a interação do usuário, proporcionando:

- melhor experiência de uso;
- prevenção de erros;
- feedback imediato;
- consistência entre módulos;
- separação clara entre validação visual e regras de negócio.

Toda validação da interface deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

A validação existe para ajudar o usuário.

Ela não deve:

- impedir desnecessariamente o fluxo;
- gerar mensagens confusas;
- substituir regras de negócio.

Seu papel é reduzir erros antes do envio dos dados.

A decisão final sempre pertence à camada Application.

---

# 3. Princípios

Toda validação deverá seguir os seguintes princípios.

## Feedback Imediato

O usuário deve receber retorno o mais cedo possível.

---

## Clareza

Toda mensagem deve explicar:

- o problema;
- onde ocorreu;
- como corrigir.

---

## Consistência

A mesma regra deve produzir sempre a mesma mensagem.

---

## Não Duplicação

Uma regra de negócio nunca deve existir apenas no Frontend.

---

## Segurança

Toda validação realizada na interface deverá ser repetida no Backend quando aplicável.

---

# 4. Arquitetura da Validação

Fluxo oficial:

```text
User

↓

Form

↓

UI Validation

↓

Request DTO

↓

Use Case

↓

Business Validation

↓

Response
```

A UI realiza apenas validações de apresentação.

As regras de negócio permanecem na Application.

---

# 5. Tipos de Validação

Existem dois tipos oficiais.

## Validação Visual

Executada imediatamente.

Exemplos:

- obrigatório;
- formato;
- tamanho;
- máscara;
- caracteres permitidos.

---

## Validação de Negócio

Executada pelos Use Cases.

Exemplos:

- e-mail já utilizado;
- meta duplicada;
- limite diário excedido;
- violação de regras do domínio.

---

# 6. Responsabilidades

## Frontend

Responsável por:

- validar entrada;
- melhorar UX;
- orientar o usuário;
- reduzir erros simples.

---

## Application

Responsável por:

- validar regras de negócio;
- validar invariantes;
- validar autorização;
- validar consistência.

---

## Domain

Responsável pelas regras fundamentais do negócio.

---

# 7. Fluxo Oficial

Toda submissão deverá seguir o fluxo abaixo.

```text
Input

↓

UI Validation

↓

Valid

↓

Submit

↓

Use Case

↓

Business Validation

↓

Success
```

Caso ocorra erro:

```text
Input

↓

Validation

↓

Error Message

↓

Correction

↓

Retry
```

---

# 8. Validação em Tempo Real

Sempre que apropriado, a validação deverá ocorrer durante a digitação.

Exemplos:

- e-mail;
- senha;
- CPF;
- telefone;
- URL;
- número.

Evitar validar regras pesadas em tempo real.

---

# 9. Campos Obrigatórios

Campos obrigatórios devem ser identificados antes do envio.

Exemplo:

```text
Nome *
```

Ao perder o foco:

```text
Nome é obrigatório.
```

Nunca permitir que o usuário descubra campos obrigatórios apenas após enviar o formulário.

---

# 10. Mensagens de Validação

Toda mensagem deverá ser:

- objetiva;
- amigável;
- específica;
- acionável.

Correto:

```text
Informe um endereço de e-mail válido.
```

Errado:

```text
Erro.

Campo inválido.

Falha.
```

As mensagens devem orientar claramente o usuário sobre como corrigir o problema.

---

# 11. Validação de Formato

Campos com formato conhecido devem ser validados na interface.

Exemplos:

```text
E-mail

Telefone

CPF

CEP

Data

Hora

URL

UUID
```

A validação deve ocorrer antes do envio do formulário.

---

# 12. Validação de Comprimento

Campos textuais devem possuir limites claros.

Exemplo:

```text
Nome

mínimo: 3

máximo: 100
```

Sempre apresentar feedback quando o limite for ultrapassado.

---

# 13. Validação Numérica

Campos numéricos devem validar:

- mínimo;
- máximo;
- intervalo permitido;
- número inteiro;
- número decimal.

Exemplo:

```text
Duração

1 — 600 minutos
```

---

# 14. Validação de Datas

Datas devem respeitar regras básicas de consistência.

Exemplos:

- data válida;
- data futura quando permitido;
- data inicial menor que data final.

As regras específicas do domínio permanecem no Use Case.

---

# 15. Validação de Seleção

Campos do tipo:

- Select;
- MultiSelect;
- Radio;
- Checkbox.

Devem impedir estados inconsistentes.

Exemplo:

```text
Nenhuma opção selecionada

↓

Campo obrigatório
```

---

# 16. Validação de Upload

Uploads devem validar:

- extensão;
- MIME Type;
- tamanho;
- quantidade de arquivos.

Nunca confiar apenas na extensão do arquivo.

---

# 17. Feedback Visual

Toda validação deve possuir retorno visual.

Estados oficiais:

```text
Normal

Focused

Success

Warning

Error

Disabled
```

Todos os estados devem seguir o Theme oficial.

---

# 18. Validação Assíncrona

Algumas validações exigem comunicação com a Application.

Exemplos:

- e-mail existente;
- nome já utilizado;
- código promocional;
- disponibilidade de recurso.

Fluxo:

```text
Input

↓

Request

↓

Validation

↓

Response

↓

Feedback
```

O usuário deve visualizar um indicador de carregamento durante a operação.

---

# 19. Integração com Use Cases

Após a validação visual:

```text
Form

↓

Request DTO

↓

Use Case

↓

Business Validation

↓

Response DTO

↓

Feedback
```

A interface apenas apresenta o resultado.

Nunca implementa regras de domínio.

---

# 20. Princípios Arquiteturais

Toda validação do LifeOS deverá ser:

- previsível;
- consistente;
- reutilizável;
- desacoplada;
- acessível;
- orientada à experiência do usuário;
- compatível com o Design System;
- alinhada ao Theme;
- integrada aos Use Cases;
- independente da tecnologia utilizada.

A arquitetura de validação garante uma experiência fluida para o usuário, reduz erros durante a entrada de dados e preserva a separação de responsabilidades entre a camada de Presentation e as regras de negócio da plataforma.