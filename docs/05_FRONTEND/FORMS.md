# FORMS

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Formulários  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** UI Architecture, Design System, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial de formulários do LifeOS.

Seu objetivo é padronizar toda entrada de dados da plataforma, garantindo:

- consistência visual;
- validação uniforme;
- excelente experiência do usuário;
- reutilização;
- acessibilidade;
- independência da tecnologia.

Todo formulário deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

O formulário é o principal ponto de interação entre o usuário e a aplicação.

Seu objetivo não é apenas coletar informações.

Ele deve:

- orientar;
- reduzir erros;
- minimizar esforço;
- fornecer feedback imediato;
- transmitir confiança.

O usuário nunca deve sentir dúvida sobre o que precisa preencher.

---

# 3. Princípios

Todo formulário deverá seguir os seguintes princípios.

## Simplicidade

Solicitar apenas as informações necessárias.

---

## Clareza

Cada campo deve possuir propósito evidente.

---

## Consistência

Campos semelhantes devem possuir o mesmo comportamento.

---

## Feedback

Toda interação deve produzir resposta imediata.

---

## Prevenção de Erros

Evitar que o usuário cometa erros sempre que possível.

---

## Acessibilidade

Todos os campos devem ser utilizáveis por qualquer usuário.

---

# 4. Arquitetura dos Formulários

Fluxo oficial:

```text
User

↓

Form

↓

Validation

↓

Request DTO

↓

Use Case

↓

Response DTO

↓

Feedback
```

O formulário nunca executa regras de negócio.

---

# 5. Estrutura Oficial

Todo formulário deverá seguir a estrutura abaixo.

```text
Header

↓

Description

↓

Fields

↓

Validation

↓

Actions

↓

Feedback
```

Essa estrutura deve permanecer consistente em toda a plataforma.

---

# 6. Organização

Estrutura sugerida:

```text
forms/

├── authentication/
├── workout/
├── habits/
├── reading/
├── therapy/
├── ai/
├── profile/
├── settings/
└── administration/
```

Cada formulário pertence a um único contexto funcional.

---

# 7. Campos

Os formulários deverão utilizar apenas componentes oficiais do Design System.

Exemplos:

```text
Text Input

Number Input

Email Input

Password Input

Search Input

Date Picker

Time Picker

Checkbox

Radio

Switch

Textarea

Select

Multi Select

Slider
```

Nunca criar componentes próprios sem necessidade.

---

# 8. Organização dos Campos

Os campos devem ser agrupados logicamente.

Exemplo:

```text
Dados Pessoais

↓

Nome

Email

Telefone
```

Outro exemplo:

```text
Treino

↓

Tipo

Data

Duração

Observações
```

A organização deve reduzir a carga cognitiva.

---

# 9. Labels

Todo campo deve possuir Label.

Exemplo:

```text
Nome do Livro
```

Evitar:

```text
Nome
```

quando o contexto não for suficiente.

Os Labels devem ser:

- objetivos;
- consistentes;
- autoexplicativos.

---

# 10. Placeholders

Placeholders são opcionais.

Eles devem servir apenas como exemplo.

Correto:

```text
Ex.: Clean Architecture
```

Errado:

```text
Digite aqui...
```

O Placeholder nunca substitui o Label.

---

# 11. Campos Obrigatórios

Campos obrigatórios devem ser claramente identificados.

Exemplo:

```text
Nome *
```

ou

```text
● Obrigatório
```

Nunca depender exclusivamente da cor para indicar obrigatoriedade.

---

# 12. Valores Padrão

Sempre que possível fornecer valores padrão.

Exemplo:

```text
Hoje

↓

Data Atual
```

Outro exemplo:

```text
Duração

↓

30 minutos
```

Valores padrão reduzem esforço do usuário.

---

# 13. Validação

Existem dois níveis de validação.

## Validação Visual

Executada imediatamente.

Exemplos:

- formato;
- comprimento;
- máscara;
- obrigatoriedade.

---

## Validação de Negócio

Executada pelo Use Case.

Exemplos:

- duplicidade;
- conflitos;
- regras do domínio.

O Frontend nunca implementa regras de negócio.

---

# 14. Máscaras

Campos específicos devem utilizar máscaras.

Exemplos:

```text
Telefone

CPF

CEP

Data

Hora

Moeda

Percentual
```

As máscaras auxiliam a entrada de dados, mas não substituem a validação.

---

# 15. Estados dos Campos

Todo campo deverá suportar estados padronizados.

```text
Enabled

Disabled

Read Only

Focused

Hovered

Filled

Empty

Error

Success
```

Os estados devem seguir o Theme oficial.

---

# 16. Estados do Formulário

Todo formulário deverá suportar estados próprios.

```text
Idle

Loading

Validating

Submitting

Success

Error
```

O usuário deve compreender claramente o estado atual da operação.

---

# 17. Botões

Todo formulário deverá possuir ações padronizadas.

Exemplos:

```text
Salvar

Cancelar

Excluir

Atualizar

Voltar
```

O botão principal deve possuir maior destaque visual.

---

# 18. Feedback

Após o envio do formulário deverá existir feedback imediato.

Exemplos:

```text
✔ Dados salvos.

⚠ Campo obrigatório.

❌ Erro ao salvar.

ℹ Alterações descartadas.
```

Nunca deixar o usuário sem resposta após uma ação.

---

# 19. Comunicação com Use Cases

Fluxo oficial:

```text
User

↓

Form

↓

Validation

↓

Request DTO

↓

Use Case

↓

Response DTO

↓

Feedback
```

O formulário nunca:

- acessa banco;
- chama Repository;
- executa SQL;
- altera Entities.

Toda lógica permanece encapsulada na camada Application.

---

# 20. Princípios Arquiteturais

Todo formulário do LifeOS deverá ser:

- simples;
- consistente;
- acessível;
- reutilizável;
- desacoplado;
- fortemente tipado;
- orientado por DTOs;
- compatível com o Design System;
- alinhado ao Theme;
- independente da tecnologia utilizada.

Os formulários representam o principal mecanismo de entrada de dados da plataforma e devem proporcionar uma experiência previsível, segura e eficiente, mantendo a lógica de negócio isolada nos Use Cases e preservando a arquitetura oficial do LifeOS.