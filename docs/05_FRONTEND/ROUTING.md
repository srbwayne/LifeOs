# ROUTING

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Roteamento  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Clean Architecture, DDD, Arquitetura Hexagonal, UI Architecture

---

# 1. Objetivo

Este documento define a arquitetura oficial de roteamento do LifeOS.

Seu objetivo é estabelecer como a navegação entre páginas será organizada, garantindo:

- consistência;
- previsibilidade;
- desacoplamento;
- segurança;
- escalabilidade;
- independência da tecnologia utilizada.

Embora a primeira versão utilize Streamlit, esta arquitetura deverá suportar futuras implementações em:

- React;
- Flutter Web;
- Vue;
- Angular;
- Desktop;
- Mobile.

---

# 2. Filosofia

O roteamento representa a estrutura de navegação da aplicação.

Sua função é:

- localizar páginas;
- preservar contexto;
- controlar acesso;
- organizar módulos.

O roteamento nunca implementa regras de negócio.

Ele apenas coordena a navegação.

---

# 3. Princípios

Toda estratégia de roteamento deverá seguir os seguintes princípios.

## Simplicidade

As rotas devem ser intuitivas.

---

## Consistência

Rotas semelhantes seguem padrões semelhantes.

---

## Desacoplamento

As páginas nunca conhecem a implementação do roteador.

---

## Segurança

Toda rota protegida exige autenticação e autorização.

---

## Escalabilidade

Novos módulos devem ser adicionados sem alterar a estrutura existente.

---

# 4. Arquitetura do Routing

Fluxo oficial:

```text
User

↓

Navigation Request

↓

Router

↓

Authentication

↓

Authorization

↓

Target Page

↓

Render
```

Toda navegação deve passar pelo Router.

---

# 5. Estrutura Oficial

A navegação será organizada por módulos.

```text
/

dashboard

/workouts

/habits

/reading

/therapy

/character

/ai

/reports

/settings

/profile

/admin
```

Cada módulo representa um contexto funcional.

---

# 6. Organização das Rotas

Cada módulo poderá possuir rotas internas.

Exemplo:

```text
/workouts

/workouts/new

/workouts/history

/workouts/calendar

/workouts/{id}
```

Outro exemplo:

```text
/books

/books/new

/books/{id}

/books/statistics
```

As rotas devem refletir o domínio.

---

# 7. Responsabilidades

O Router é responsável por:

- resolver rotas;
- localizar páginas;
- validar acesso;
- preservar contexto;
- controlar navegação.

O Router nunca:

- executa Use Cases;
- consulta banco;
- implementa regras de negócio;
- acessa Repositories.

---

# 8. Navegação Programática

A aplicação poderá navegar programaticamente.

Fluxo:

```text
User Action

↓

Router

↓

Target Route

↓

Page

↓

Render
```

Exemplo:

```text
Workout Saved

↓

Navigate

↓

Workout Details
```

A navegação sempre utiliza o Router.

---

# 9. Parâmetros de Rota

As rotas podem receber parâmetros.

Exemplos:

```text
/workouts/{id}

/books/{id}

/users/{id}
```

Os parâmetros representam identificadores.

Nunca devem conter regras de negócio.

---

# 10. Query Parameters

Filtros temporários devem utilizar Query Parameters.

Exemplos:

```text
/workouts?page=2

/books?status=READ

/habits?category=health

/reports?year=2026
```

Os parâmetros devem ser opcionais.

---

# 11. Rotas Públicas

Algumas páginas poderão ser acessadas sem autenticação.

Exemplos:

```text
/login

/register

/forgot-password

/reset-password
```

Essas rotas não possuem acesso ao restante da aplicação.

---

# 12. Rotas Protegidas

Toda funcionalidade principal deverá utilizar rotas protegidas.

Fluxo:

```text
Request

↓

Authentication

↓

Authorization

↓

Route

↓

Page
```

Usuários não autenticados devem ser redirecionados para Login.

---

# 13. Controle de Acesso

Antes da navegação deve ocorrer:

```text
Authentication

↓

Authorization

↓

Ownership

↓

Navigation
```

O roteador apenas inicia o processo.

As decisões pertencem ao Authorization Service.

---

# 14. Deep Linking

Toda página deverá suportar acesso direto.

Exemplos:

```text
/workouts/123

/books/54

/therapy/session/8
```

Ao abrir uma rota diretamente, a página deve reconstruir completamente seu estado.

---

# 15. Breadcrumb

O Router fornece as informações necessárias para o Breadcrumb.

Exemplo:

```text
Dashboard

↓

Workout

↓

History

↓

Workout Details
```

O Breadcrumb nunca deve ser montado manualmente por cada página.

---

# 16. Histórico de Navegação

O sistema deverá manter histórico da navegação.

Fluxo:

```text
Current Route

↓

Navigate

↓

History Stack

↓

Back

↓

Previous Route
```

Essa funcionalidade melhora a experiência do usuário.

---

# 17. Estados da Navegação

Durante uma navegação poderão existir os seguintes estados.

```text
Loading

Ready

Unauthorized

Forbidden

Not Found

Error
```

Cada estado deverá possuir interface própria.

---

# 18. Redirecionamentos

Algumas rotas poderão redirecionar automaticamente.

Exemplo:

```text
/

↓

Dashboard
```

Outro exemplo:

```text
/login

↓

Dashboard

(após autenticação)
```

Os redirecionamentos devem ser explícitos e documentados.

---

# 19. Estrutura Futura

A arquitetura deverá suportar futuras expansões.

Exemplos:

```text
Mobile Routes

Admin Routes

API Routes

Plugin Routes

Public Routes
```

Todos reutilizam a mesma arquitetura de roteamento.

---

# 20. Princípios Arquiteturais

Todo roteamento do LifeOS deverá ser:

- orientado por contexto;
- previsível;
- desacoplado;
- seguro;
- reutilizável;
- escalável;
- independente da tecnologia;
- compatível com a Clean Architecture;
- integrado ao sistema de autenticação e autorização;
- alinhado ao Design System.

A arquitetura de roteamento constitui a espinha dorsal da navegação do LifeOS, garantindo uma experiência consistente para o usuário, preservando o desacoplamento entre páginas e permitindo que a plataforma evolua de forma sustentável ao longo do tempo.