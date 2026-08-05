# INTERNATIONALIZATION

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Internacionalização (i18n) e Localização (l10n)  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Clean Architecture, Design System, UI Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial de Internacionalização (i18n) e Localização (l10n) do LifeOS.

Seu objetivo é permitir que a plataforma seja utilizada em diferentes idiomas e regiões sem alterações na lógica da aplicação.

A arquitetura deve suportar:

- múltiplos idiomas;
- diferentes formatos regionais;
- expansão futura;
- consistência textual;
- adaptação cultural.

Toda funcionalidade deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

A internacionalização não consiste apenas em traduzir textos.

Ela garante que toda a experiência da aplicação possa ser adaptada para diferentes culturas mantendo:

- usabilidade;
- consistência;
- identidade visual;
- comportamento funcional.

O idioma nunca deve alterar regras de negócio.

---

# 3. Princípios

Toda implementação deverá seguir os seguintes princípios.

## Separação

Textos nunca devem estar fixos no código.

---

## Consistência

A mesma chave representa sempre o mesmo significado.

---

## Escalabilidade

Novos idiomas devem ser adicionados sem alterar a arquitetura.

---

## Reutilização

Mensagens iguais reutilizam a mesma chave.

---

## Independência

A lógica da aplicação nunca depende do idioma.

---

# 4. Arquitetura

Fluxo oficial:

```text
Current Locale

↓

Translation Service

↓

Localized Resources

↓

UI Components

↓

Render
```

A interface nunca contém textos fixos.

---

# 5. Idioma Padrão

O idioma oficial inicial da plataforma será:

```text
Português (Brasil)

pt-BR
```

Os demais idiomas serão adicionados posteriormente.

---

# 6. Idiomas Suportados

Arquitetura preparada para:

```text
pt-BR

en-US

es-ES

fr-FR

de-DE

it-IT

ja-JP

zh-CN
```

Novos idiomas poderão ser adicionados sem impacto arquitetural.

---

# 7. Organização

Estrutura sugerida:

```text
i18n/

├── pt_BR.json
├── en_US.json
├── es_ES.json
├── fr_FR.json
├── de_DE.json
├── ja_JP.json
├── zh_CN.json
└── locale.py
```

Cada idioma possui seu próprio arquivo.

---

# 8. Chaves de Tradução

As traduções devem utilizar chaves hierárquicas.

Exemplo:

```text
dashboard.title

dashboard.subtitle

workout.new

workout.delete

book.status.read

settings.language
```

Nunca utilizar frases completas como identificadores.

---

# 9. Uso na Interface

Sempre utilizar o mecanismo oficial de tradução.

Exemplo conceitual:

```text
t("dashboard.title")
```

Nunca escrever diretamente:

```text
Dashboard
```

Toda interface deve utilizar recursos traduzíveis.

---

# 10. Textos

Todos os textos da interface deverão ser externalizados.

Exemplos:

- botões;
- menus;
- mensagens;
- títulos;
- descrições;
- placeholders;
- tooltips;
- notificações.

Nenhum texto fixo deve permanecer nos componentes.

---

# 11. Formatação de Datas

As datas devem respeitar o idioma atual.

Exemplos:

```text
31/12/2026

(pt-BR)
```

```text
12/31/2026

(en-US)
```

A lógica de armazenamento permanece independente da apresentação.

---

# 12. Formatação de Horários

Os horários devem seguir a convenção regional.

Exemplos:

```text
23:45
```

```text
11:45 PM
```

A escolha depende do Locale.

---

# 13. Formatação Numérica

Números devem respeitar a localização.

Exemplo:

```text
1.234,56

(pt-BR)
```

```text
1,234.56

(en-US)
```

Toda formatação deve ocorrer na camada de apresentação.

---

# 14. Formatação Monetária

Valores monetários devem utilizar o padrão regional.

Exemplos:

```text
R$ 1.250,00
```

```text
US$ 1,250.00
```

A moeda utilizada depende do contexto da aplicação.

---

# 15. Fuso Horário

Toda exibição de data e hora deve considerar o fuso horário do usuário.

Fluxo:

```text
UTC

↓

Timezone

↓

Localized Date

↓

Render
```

Internamente recomenda-se armazenar datas em UTC.

---

# 16. Pluralização

Mensagens devem suportar singular e plural.

Exemplo:

```text
1 treino

2 treinos
```

Outro exemplo:

```text
1 livro

5 livros
```

Nunca construir pluralização manualmente na interface.

---

# 17. Idioma do Usuário

O idioma poderá ser definido por:

- preferência do usuário;
- configuração da organização;
- idioma do navegador;
- configuração da aplicação.

A preferência do usuário possui prioridade.

---

# 18. Mudança de Idioma

O usuário poderá alterar o idioma sem reiniciar a aplicação.

Fluxo:

```text
Settings

↓

Language

↓

Reload Resources

↓

Render
```

A mudança não deve afetar o estado da aplicação.

---

# 19. Evolução

A arquitetura deverá permitir futuras extensões.

Exemplos:

- idiomas adicionais;
- dialetos regionais;
- formatos personalizados;
- temas culturais;
- localização automática.

Toda expansão deve reutilizar a arquitetura existente.

---

# 20. Princípios Arquiteturais

Toda internacionalização do LifeOS deverá ser:

- desacoplada da lógica de negócio;
- orientada por recursos externos;
- reutilizável;
- consistente;
- escalável;
- compatível com o Design System;
- alinhada ao Theme;
- independente da tecnologia utilizada;
- preparada para múltiplos idiomas;
- preparada para múltiplas localidades.

A arquitetura de Internacionalização garante que o LifeOS possa evoluir para um produto global, oferecendo uma experiência natural para usuários de diferentes idiomas e culturas, sem comprometer a arquitetura da plataforma nem a consistência da interface.