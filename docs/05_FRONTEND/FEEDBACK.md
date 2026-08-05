# FEEDBACK

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Arquitetura de Feedback ao Usuário  
**Camadas Relacionadas:** Presentation, Application  
**Arquiteturas Relacionadas:** Design System, UI Architecture, Clean Architecture, Arquitetura Hexagonal

---

# 1. Objetivo

Este documento define a arquitetura oficial de **Feedback ao Usuário** do LifeOS.

Seu objetivo é padronizar toda comunicação da aplicação com o usuário durante sua interação com o sistema, garantindo:

- clareza;
- previsibilidade;
- consistência;
- acessibilidade;
- excelente experiência de uso.

Todo feedback visual deverá seguir obrigatoriamente este documento.

---

# 2. Filosofia

O usuário nunca deve ficar em dúvida sobre o que aconteceu.

Toda ação executada deve produzir uma resposta clara.

O sistema deve comunicar:

- sucesso;
- erro;
- progresso;
- carregamento;
- confirmação;
- alerta;
- informação.

O silêncio da interface é considerado um problema de usabilidade.

---

# 3. Princípios

Todo feedback deverá seguir os seguintes princípios.

## Imediatismo

Responder imediatamente após a ação.

---

## Clareza

Explicar o que aconteceu.

---

## Objetividade

Mensagens curtas e compreensíveis.

---

## Consistência

A mesma situação gera sempre o mesmo tipo de feedback.

---

## Não Intrusivo

O feedback não deve interromper o fluxo do usuário sem necessidade.

---

# 4. Arquitetura do Feedback

Fluxo oficial:

```text
User Action

↓

Use Case

↓

Result

↓

Feedback

↓

Render
```

A camada de Feedback apenas apresenta o resultado da operação.

Nunca executa lógica de negócio.

---

# 5. Tipos de Feedback

Existem seis categorias oficiais.

```text
Success

Information

Warning

Error

Loading

Confirmation
```

Cada categoria possui identidade visual própria.

---

# 6. Feedback de Sucesso

Utilizado quando uma operação foi concluída corretamente.

Exemplos:

```text
Treino registrado com sucesso.

Livro atualizado.

Meta concluída.

Perfil salvo.
```

O usuário deve compreender imediatamente que a ação foi concluída.

---

# 7. Feedback Informativo

Comunica acontecimentos sem exigir ação imediata.

Exemplos:

```text
Sincronização concluída.

Nova atualização disponível.

Relatório gerado.

Backup realizado.
```

Esse feedback não representa erro nem sucesso operacional.

---

# 8. Feedback de Alerta

Utilizado quando o usuário deve prestar atenção.

Exemplos:

```text
Você está próximo do limite diário.

Sessão expirará em breve.

Pouco espaço disponível.
```

O alerta não impede a continuidade da operação.

---

# 9. Feedback de Erro

Representa falhas.

Exemplos:

```text
Erro ao salvar.

Falha na conexão.

Arquivo inválido.

Operação não permitida.
```

Mensagens de erro nunca devem expor:

- SQL;
- Stack Trace;
- Exceptions;
- detalhes internos.

---

# 10. Feedback de Carregamento

Operações que levam tempo devem informar seu progresso.

Exemplos:

```text
Carregando...

Processando...

Exportando...

Importando...

Sincronizando...
```

Sempre apresentar indicador visual durante operações demoradas.

---

# 11. Feedback de Confirmação

Operações destrutivas devem solicitar confirmação.

Exemplos:

```text
Excluir treino?

Excluir livro?

Restaurar backup?

Cancelar alterações?
```

O usuário deve compreender claramente as consequências da ação.

---

# 12. Toast Notifications

Mensagens rápidas devem utilizar Toasts.

Exemplos:

```text
✔ Salvo com sucesso.

⚠ Alterações pendentes.

ℹ Atualização disponível.
```

Características:

- temporárias;
- não bloqueantes;
- discretas;
- consistentes.

---

# 13. Snackbars

Snackbars apresentam informações rápidas com possibilidade de ação.

Exemplo:

```text
Treino excluído.

[Desfazer]
```

Devem desaparecer automaticamente após alguns segundos.

---

# 14. Dialogs

Dialogs são utilizados quando uma decisão do usuário é necessária.

Exemplos:

```text
Excluir

Cancelar

Salvar

Confirmar
```

Dialogs interrompem temporariamente o fluxo da interface.

Devem ser utilizados apenas quando indispensáveis.

---

# 15. Loading States

Toda operação longa deve possuir um estado visual.

Exemplos:

```text
Loading Spinner

Progress Bar

Skeleton Screen

Loading Card
```

Nunca apresentar telas vazias durante carregamentos.

---

# 16. Skeleton Loading

Sempre que possível utilizar Skeletons.

Exemplo:

```text
██████████

██████

████████████
```

Benefícios:

- reduz percepção de espera;
- mantém estabilidade visual;
- melhora experiência.

Skeletons substituem Spinners em listas e dashboards.

---

# 17. Progress Feedback

Operações demoradas devem informar progresso.

Exemplo:

```text
Importando...

45%
```

Outro exemplo:

```text
Backup

↓

3 de 10 arquivos
```

Sempre informar progresso quando possível.

---

# 18. Empty States

Quando não houver dados disponíveis, utilizar Empty States.

Exemplos:

```text
Nenhum treino registrado.

Comece criando seu primeiro treino.
```

Outro exemplo:

```text
Nenhum livro encontrado.
```

O Empty State deve incentivar a próxima ação do usuário.

---

# 19. Error States

Quando ocorrer falha na página:

```text
Erro ao carregar informações.

[Tentar novamente]
```

Sempre oferecer:

- contexto;
- ação de recuperação;
- linguagem amigável.

Nunca deixar a interface sem possibilidade de recuperação.

---

# 20. Princípios Arquiteturais

Todo feedback do LifeOS deverá ser:

- imediato;
- consistente;
- acessível;
- contextual;
- reutilizável;
- desacoplado;
- compatível com o Design System;
- alinhado ao Theme;
- independente da tecnologia utilizada;
- orientado à experiência do usuário.

A arquitetura de Feedback garante que toda interação com o LifeOS produza respostas claras, previsíveis e úteis, reduzindo a carga cognitiva, aumentando a confiança do usuário e fortalecendo a identidade visual e funcional da plataforma.