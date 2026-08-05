# Definition of Done (DoD)

> Documento oficial que define os critérios mínimos para considerar qualquer atividade concluída no projeto LifeOS.

Versão: 1.0

---

# 1. Objetivo

A Definition of Done (DoD) estabelece o padrão mínimo de qualidade para todas as entregas do LifeOS.

Nenhuma funcionalidade, correção, refatoração ou melhoria poderá ser considerada concluída sem atender integralmente aos critérios definidos neste documento.

A DoD garante:

- qualidade consistente;
- previsibilidade das entregas;
- redução de débito técnico;
- preservação da arquitetura;
- rastreabilidade;
- documentação atualizada.

---

# 2. Escopo

Esta Definition of Done aplica-se a:

- novas funcionalidades;
- correções de bugs;
- refatorações;
- melhorias;
- integrações;
- migrações;
- alterações de banco;
- documentação;
- testes.

---

# 3. Fluxo Oficial

Toda entrega deverá seguir obrigatoriamente o fluxo abaixo.

```text
Requisito

↓

Planejamento

↓

Implementação

↓

Testes

↓

Validação

↓

Documentação

↓

Revisão

↓

Entrega
```

Nenhuma etapa poderá ser ignorada.

---

# 4. Critérios Gerais

Uma tarefa somente poderá ser considerada concluída quando:

- implementar completamente o escopo solicitado;
- respeitar a arquitetura oficial;
- possuir testes;
- atualizar documentação quando necessário;
- não introduzir regressões;
- preservar a qualidade do projeto.

---

# 5. Checklist de Desenvolvimento

Antes de concluir uma tarefa confirme:

- [ ] Todos os requisitos foram implementados.
- [ ] Não existem funcionalidades parcialmente concluídas.
- [ ] Não existem TODOs.
- [ ] Não existem FIXMEs.
- [ ] Não existem códigos comentados.
- [ ] Não existem trechos temporários.

---

# 6. Checklist de Arquitetura

Verifique:

- [ ] Clean Architecture preservada.
- [ ] SOLID respeitado.
- [ ] DDD respeitado.
- [ ] Dependências corretas.
- [ ] Nenhuma violação da Regra de Dependência.
- [ ] Sem acoplamento indevido.
- [ ] Sem duplicação de responsabilidades.

---

# 7. Checklist da Game Engine

Quando aplicável:

- [ ] Nenhuma Capability altera diretamente o Character.
- [ ] Toda evolução ocorre pela Game Engine.
- [ ] Eventos publicados corretamente.
- [ ] Eventos consumidos corretamente.
- [ ] Regras de evolução preservadas.
- [ ] Auditoria registrada.

---

# 8. Checklist de Banco de Dados

Quando aplicável:

- [ ] Migration criada.
- [ ] Migration testada.
- [ ] Schema atualizado.
- [ ] Índices avaliados.
- [ ] Integridade referencial preservada.
- [ ] Compatibilidade mantida.

---

# 9. Checklist de Backend

Verifique:

- [ ] APIs implementadas.
- [ ] Validações concluídas.
- [ ] Tratamento de erros implementado.
- [ ] Logs adicionados.
- [ ] Eventos publicados.
- [ ] DTOs atualizados.
- [ ] Mappers atualizados.

---

# 10. Checklist de Frontend

Quando aplicável:

- [ ] Interface implementada.
- [ ] Navegação funcionando.
- [ ] Feedback visual adequado.
- [ ] Estados de carregamento.
- [ ] Estados de erro.
- [ ] Responsividade preservada.

---

# 11. Checklist de Inteligência Artificial

Quando aplicável:

- [ ] Recomendações explicáveis.
- [ ] Contexto atualizado.
- [ ] Nenhuma alteração direta no Character.
- [ ] Fontes rastreáveis.
- [ ] Prompts documentados.

---

# 12. Checklist de Analytics

Quando aplicável:

- [ ] Indicadores corretos.
- [ ] Métricas consistentes.
- [ ] Correlações reproduzíveis.
- [ ] Insights documentados.

---

# 13. Checklist de Segurança

Verifique:

- [ ] Autenticação validada.
- [ ] Autorização validada.
- [ ] Dados sensíveis protegidos.
- [ ] Nenhuma credencial exposta.
- [ ] Validação de entrada implementada.

---

# 14. Checklist Multi-Tenant

Quando aplicável:

- [ ] Isolamento preservado.
- [ ] Consultas filtradas por Tenant.
- [ ] Nenhum vazamento de dados.
- [ ] Testes de isolamento executados.

---

# 15. Checklist de Performance

Verifique:

- [ ] Sem consultas desnecessárias.
- [ ] Paginação quando aplicável.
- [ ] Processamento otimizado.
- [ ] Sem loops redundantes.
- [ ] Sem gargalos conhecidos.

---

# 16. Checklist de Testes

Toda entrega deverá possuir:

- [ ] Testes unitários.
- [ ] Testes de integração.
- [ ] Testes arquiteturais (quando aplicável).
- [ ] Testes End-to-End (quando aplicável).

Além disso:

- [ ] Todos os testes executados.
- [ ] Nenhum teste falhou.
- [ ] Cobertura preservada ou aumentada.

---

# 17. Checklist de Documentação

Verifique:

- [ ] PRD atualizado quando necessário.
- [ ] Feature Catalog atualizado.
- [ ] Architecture atualizada.
- [ ] Database atualizado.
- [ ] CHANGELOG atualizado.
- [ ] Comentários relevantes adicionados.

---

# 18. Checklist de Revisão

Antes da entrega:

- [ ] Código revisado.
- [ ] Padrões respeitados.
- [ ] Nomenclatura consistente.
- [ ] Sem código duplicado.
- [ ] Sem dependências desnecessárias.

---

# 19. Critérios para NÃO Considerar uma Tarefa Concluída

Uma tarefa permanece aberta quando:

- existe código incompleto;
- existem testes falhando;
- existe documentação desatualizada;
- existem TODOs;
- existe débito técnico não registrado;
- existe violação arquitetural;
- existe requisito parcialmente implementado.

---

# 20. Responsabilidades

## Desenvolvedor

Responsável por:

- implementação;
- testes;
- documentação;
- qualidade.

---

## Revisor

Responsável por:

- validar arquitetura;
- validar padrões;
- validar testes;
- aprovar a entrega.

---

## Agente de IA

Responsável por:

- seguir o GEMINI.md;
- respeitar esta Definition of Done;
- nunca considerar uma tarefa concluída sem atender todos os critérios;
- interromper a implementação caso algum requisito obrigatório não possa ser atendido.

---

# 21. Resultado Esperado

Ao finalizar qualquer tarefa, o projeto deverá estar:

- mais organizado;
- mais documentado;
- mais testado;
- mais seguro;
- mais consistente;
- mais próximo da visão definida no Product Vision.

A qualidade do projeto sempre terá prioridade sobre a velocidade de entrega.