# CODE_REVIEW_CHECKLIST.md

> Checklist oficial de revisão técnica e arquitetural do projeto LifeOS.

Versão: 1.0
Status: Ativo
Aplicação: Obrigatória para desenvolvedores humanos, agentes de IA e revisores técnicos

---

# 1. Objetivo

Este documento define os critérios obrigatórios para revisão de código no LifeOS.

Toda alteração deverá ser avaliada antes de ser considerada pronta para merge, release ou encerramento de Sprint.

A revisão deverá verificar:

- aderência ao escopo autorizado;
- conformidade com a arquitetura;
- integridade do domínio;
- qualidade do código;
- segurança;
- persistência;
- testes;
- performance;
- dependências;
- documentação;
- rastreabilidade;
- governança Git.

A aprovação não poderá ser baseada apenas no relato do desenvolvedor ou agente.

Toda conclusão deverá ser sustentada por:

- leitura do código;
- análise do diff;
- evidências reais de execução;
- resultados de testes;
- verificação da documentação;
- confirmação da Definition of Done.

---

# 2. Aplicação

Este checklist aplica-se a:

- novas funcionalidades;
- correções de bugs;
- refatorações;
- alterações arquiteturais;
- migrations;
- integrações;
- APIs;
- segurança;
- dependências;
- documentação;
- testes;
- automações;
- infraestrutura;
- alterações de configuração.

---

# 3. Papéis

## Desenvolvedor ou agente executor

Responsável por:

- realizar a autoauditoria;
- executar os testes;
- apresentar evidências;
- revisar o próprio diff;
- corrigir problemas antes da entrega;
- preencher o checklist aplicável.

---

## Revisor técnico

Responsável por:

- validar o escopo;
- revisar arquitetura;
- verificar regras de domínio;
- confirmar evidências;
- identificar riscos;
- aprovar, reprovar ou solicitar correções.

---

## Arquiteto de Software

Responsável por:

- avaliar mudanças estruturais;
- proteger as fronteiras entre Capabilities;
- aprovar decisões arquiteturais;
- exigir ADR quando necessário;
- impedir antecipação de responsabilidades futuras.

---

# 4. Resultado da Revisão

A revisão deverá produzir um dos seguintes resultados:

| Resultado | Significado |
|---|---|
| ✅ Aprovado | A alteração atende integralmente aos critérios aplicáveis |
| ⚠️ Aprovado com ressalvas | Existem pontos não bloqueantes devidamente registrados |
| 🔄 Correções obrigatórias | Existem pendências que impedem a aprovação |
| ⛔ Reprovado | A alteração viola escopo, arquitetura, segurança ou requisitos |
| 🛑 Bloqueado | Existe conflito documental ou decisão de produto pendente |

Uma Sprint não poderá ser encerrada com resultado:

- 🔄 Correções obrigatórias;
- ⛔ Reprovado;
- 🛑 Bloqueado.

---

# 5. Gate 1 — Escopo e autorização

Antes de revisar o código, confirmar:

- [ ] Existe `NEXT_TASK.md` válido na raiz.
- [ ] A tarefa está autorizada.
- [ ] A Sprint está identificada.
- [ ] A Capability está identificada.
- [ ] As Features estão identificadas.
- [ ] Os RFs estão identificados.
- [ ] O escopo está claramente definido.
- [ ] O fora do escopo está claramente definido.
- [ ] Nenhuma funcionalidade externa foi implementada.
- [ ] Nenhuma decisão de produto foi tomada sem autorização.
- [ ] Nenhum RF foi considerado concluído parcialmente.
- [ ] Não existem conflitos não resolvidos entre PRD, Feature Catalog e NEXT_TASK.

## Reprovar imediatamente quando

- houver funcionalidade sem Feature ou RF;
- houver implementação fora do escopo;
- houver antecipação de outra Capability;
- houver requisito parcialmente implementado declarado como concluído;
- houver decisão de produto inventada.

---

# 6. Gate 2 — Rastreabilidade

Verificar:

- [ ] Toda alteração funcional possui Capability.
- [ ] Toda alteração funcional possui Feature correspondente.
- [ ] Toda alteração funcional possui RF correspondente.
- [ ] Alterações arquiteturais possuem ADR, quando aplicável.
- [ ] Os testes podem ser associados ao comportamento implementado.
- [ ] Os commits informam Sprint, Capability, Feature, RF e ADR quando aplicável.
- [ ] O CHANGELOG registra a alteração.
- [ ] PROJECT_STATUS reflete o estado real.
- [ ] TASK_HISTORY registra a entrega.
- [ ] Nenhuma referência documental ficou órfã.

Fluxo esperado:

```text
Product Vision
↓
Capability
↓
Feature
↓
Requisito Funcional
↓
Código
↓
Teste
↓
Commit
↓
Release
```

---

# 7. Gate 3 — Arquitetura

## Clean Architecture

- [ ] Domain não depende de Application.
- [ ] Domain não depende de Infrastructure.
- [ ] Domain não depende de Presentation.
- [ ] Application não depende de Infrastructure.
- [ ] Application não depende de Presentation.
- [ ] Presentation não acessa diretamente o banco.
- [ ] Infrastructure implementa Ports definidos pelas camadas internas.
- [ ] O Composition Root concentra a montagem das dependências.
- [ ] Frameworks permanecem nas camadas externas.
- [ ] Entidades de domínio não conhecem FastAPI, SQLAlchemy ou Pydantic.

---

## Fronteiras entre Capabilities

- [ ] Uma Capability não importa internals de outra.
- [ ] Domain de uma Capability não importa Domain de outra.
- [ ] Comunicação transversal utiliza Shared Kernel, contratos públicos ou eventos.
- [ ] Não existem dependências circulares.
- [ ] Ownership dos dados está preservado.
- [ ] Nenhuma Capability escreve diretamente em dados pertencentes a outra.
- [ ] A Game Engine continua sendo a única autoridade de progressão.
- [ ] Analytics permanece consultiva.
- [ ] AI permanece consultiva.
- [ ] Dashboard permanece consultivo.
- [ ] Reports permanece consultivo.

Exemplo proibido:

```text
app.character.domain
↓
app.auth.domain
```

Exemplo permitido:

```text
app.character.domain
↓
app.shared.domain
```

---

## Shared Kernel

- [ ] Contém apenas conceitos realmente transversais.
- [ ] Não contém regras específicas de uma Capability.
- [ ] Não se tornou um diretório genérico para qualquer código reutilizável.
- [ ] Identificadores compartilhados possuem ownership claro.
- [ ] Alterações no Shared Kernel foram avaliadas pelo Arquiteto.
- [ ] Existe teste de regressão para Capabilities afetadas.

---

## CQRS

- [ ] Commands representam operações de escrita.
- [ ] Queries representam operações de leitura.
- [ ] Queries não alteram estado.
- [ ] Commands não retornam modelos ORM.
- [ ] Handlers possuem responsabilidade clara.
- [ ] Não existe infraestrutura genérica desnecessária.
- [ ] O padrão não foi aplicado de forma artificial a operações triviais.

---

## Event-Driven Architecture

- [ ] Eventos representam fatos ocorridos.
- [ ] Eventos são publicados após a persistência válida.
- [ ] Eventos não são utilizados para garantir pós-condições atômicas sem estratégia de consistência.
- [ ] O nome do evento representa o estado realmente concluído.
- [ ] Eventos não carregam dados sensíveis.
- [ ] Handlers são idempotentes quando necessário.
- [ ] A limitação do Event Bus em memória está respeitada.
- [ ] Outbox é considerada quando houver necessidade de entrega garantida.

---

## Unit of Work

- [ ] Repositórios da mesma transação compartilham a mesma sessão.
- [ ] Repositórios não executam `commit()`.
- [ ] O commit é controlado pela Application.
- [ ] O rollback é executado em caso de falha.
- [ ] Eventos são coletados e despachados na ordem oficial.
- [ ] A transação não fica aberta além do necessário.
- [ ] Testes validam atomicidade e rollback.

---

# 8. Gate 4 — Domain-Driven Design

## Aggregates

- [ ] O Aggregate possui responsabilidade clara.
- [ ] As invariantes são protegidas dentro do domínio.
- [ ] O Aggregate não está anêmico.
- [ ] O Aggregate não concentra responsabilidades externas.
- [ ] Alterações de estado passam por métodos de negócio.
- [ ] O Aggregate não recebe objetos de infraestrutura.
- [ ] O Aggregate não depende de serviços concretos.
- [ ] A fronteira transacional está correta.

---

## Entities

- [ ] Possuem identidade própria quando necessário.
- [ ] A identidade é imutável.
- [ ] A igualdade respeita a identidade.
- [ ] Não são criadas Entities sem comportamento ou necessidade real.
- [ ] Não duplicam dados de outros Aggregates.

---

## Value Objects

- [ ] São imutáveis.
- [ ] Validam suas próprias invariantes.
- [ ] Possuem nomes de domínio.
- [ ] Não aceitam estado inválido.
- [ ] Não representam apenas um wrapper sem valor semântico.
- [ ] Cada Value Object relevante está em arquivo próprio.
- [ ] Erros de validação utilizam Domain Errors adequados.

---

## Domain Services e Ports

- [ ] Existem somente quando a lógica não pertence naturalmente a uma Entity ou Aggregate.
- [ ] Interfaces possuem responsabilidade única.
- [ ] Nomes representam contratos claros.
- [ ] Implementações concretas permanecem na Infrastructure.
- [ ] O domínio não recebe dependências desnecessárias.
- [ ] Serviços anêmicos ou genéricos foram evitados.

---

## Domain Errors

- [ ] Erros representam linguagem do domínio.
- [ ] Não são lançadas exceções genéricas para regras de negócio.
- [ ] Erros não expõem detalhes internos.
- [ ] A Presentation traduz erros para respostas adequadas.
- [ ] Não existe captura genérica que silencie falhas reais.

---

# 9. Gate 5 — Regras específicas da Game Engine

Quando a alteração envolver ou tocar o Character:

- [ ] Nenhuma Capability externa calcula XP.
- [ ] Nenhuma Capability externa altera Level.
- [ ] Nenhuma Capability externa evolui Attributes.
- [ ] Nenhuma Capability externa desbloqueia Skills.
- [ ] Nenhuma Capability externa atribui Classes.
- [ ] Nenhuma Capability externa concede Rewards.
- [ ] Nenhuma Capability externa altera Progression.
- [ ] Toda evolução passa pela Game Engine.
- [ ] Character permanece representação persistente e identidade.
- [ ] Consultas de XP e Level apontam para GAME.
- [ ] Nenhuma regra futura foi antecipada sem RF.

---

# 10. Gate 6 — Application Layer

- [ ] Use Cases ou Handlers refletem o requisito funcional.
- [ ] A orquestração está na Application.
- [ ] A Application não contém regra de domínio que deveria estar no Aggregate.
- [ ] A Application não conhece SQLAlchemy.
- [ ] A Application não conhece FastAPI.
- [ ] DTOs não expõem Entities.
- [ ] DTOs não expõem ORM Models.
- [ ] Commands e Queries são validados adequadamente.
- [ ] As dependências são injetadas.
- [ ] O Unit of Work é utilizado corretamente.
- [ ] O contexto autenticado não vem de parâmetros manipuláveis pelo cliente.
- [ ] Casos de uso não realizam commits diretamente em repositories.

---

# 11. Gate 7 — Infrastructure

- [ ] Repositories implementam Ports oficiais.
- [ ] Mappers separam Domain de ORM.
- [ ] ORM Models não contêm regras de negócio.
- [ ] Repositories não retornam ORM Models para Application.
- [ ] Queries aplicam isolamento por usuário ou tenant.
- [ ] Não existe SQL duplicado sem necessidade.
- [ ] Adaptadores externos possuem timeout.
- [ ] Falhas de integrações são tratadas.
- [ ] Segredos são obtidos por configuração segura.
- [ ] Não existem credenciais hardcoded.
- [ ] Infraestrutura não altera invariantes do domínio.

---

# 12. Gate 8 — API e Presentation

- [ ] Endpoint corresponde a RF autorizado.
- [ ] Método HTTP está semanticamente correto.
- [ ] Status HTTP está correto.
- [ ] Schemas de entrada e saída estão separados.
- [ ] Não existem modelos ORM na API.
- [ ] Autenticação é obrigatória quando aplicável.
- [ ] Autorização é validada.
- [ ] O contexto do usuário vem do token ou sessão.
- [ ] O cliente não fornece `user_id` para acessar dados próprios.
- [ ] Erros de domínio são traduzidos adequadamente.
- [ ] Não são expostos stack traces.
- [ ] Não são expostos detalhes sensíveis.
- [ ] OpenAPI foi validado.
- [ ] Endpoints fora do escopo não foram criados.
- [ ] Endpoints de escrita inexistentes retornam 405 quando aplicável.
- [ ] Paginação existe em coleções potencialmente grandes.
- [ ] Rotas possuem nomes e prefixos consistentes.

---

# 13. Gate 9 — Banco de Dados

## Schema

- [ ] Cada tabela possui owner definido.
- [ ] PK utiliza o padrão oficial TSID.
- [ ] FKs estão corretas.
- [ ] Constraints `UNIQUE` foram avaliadas.
- [ ] Constraints `NOT NULL` foram avaliadas.
- [ ] Índices foram avaliados.
- [ ] Relacionamentos 1:1 estão protegidos.
- [ ] Relacionamentos 1:N estão corretamente modelados.
- [ ] Não há duplicação de dados sem justificativa.
- [ ] Campos sensíveis estão protegidos.
- [ ] Timestamps seguem padrão UTC.

---

## Migrations

- [ ] Migration nova foi criada quando necessária.
- [ ] Nenhuma migration aplicada foi alterada.
- [ ] Upgrade foi executado em banco vazio.
- [ ] Upgrade foi executado a partir da versão anterior.
- [ ] Downgrade foi testado quando aplicável.
- [ ] Migration possui nome claro.
- [ ] Migration não utiliza `create_all()`.
- [ ] Alembic está em `head`.
- [ ] Schema resultante foi inspecionado.
- [ ] `integrity_check` foi executado quando aplicável.
- [ ] Dados existentes foram preservados.
- [ ] Estratégia de backfill foi definida quando necessária.

---

## Unit of Work e transações

- [ ] Todas as persistências obrigatórias participam da mesma transação.
- [ ] Não existem commits parciais indevidos.
- [ ] Falha intermediária provoca rollback.
- [ ] Eventos são publicados somente no momento correto.
- [ ] O repositório não cria sessões independentes dentro da mesma operação.

---

# 14. Gate 10 — Segurança

## Autenticação

- [ ] Senhas nunca são persistidas em texto puro.
- [ ] PasswordHasher utiliza algoritmo aprovado.
- [ ] Tokens não são registrados em logs.
- [ ] Tokens persistidos são armazenados como hash.
- [ ] Sessões expiradas são rejeitadas.
- [ ] Sessões revogadas são rejeitadas.
- [ ] Refresh token reutilizado é rejeitado.
- [ ] Logout revoga a sessão.
- [ ] Reset de senha invalida o token.
- [ ] Respostas não revelam existência de e-mail indevidamente.

---

## Autorização

- [ ] Toda operação protegida valida identidade.
- [ ] Toda operação protegida valida ownership.
- [ ] O acesso cruzado entre usuários é bloqueado.
- [ ] O acesso cruzado entre tenants é bloqueado.
- [ ] Falha de ownership não revela dados de terceiros.
- [ ] Permissões administrativas são verificadas.

---

## Dados sensíveis

- [ ] Nenhuma senha aparece no diff.
- [ ] Nenhum token aparece no diff.
- [ ] Nenhuma API key aparece no diff.
- [ ] Nenhuma credencial aparece em arquivo de configuração.
- [ ] `.env` está ignorado.
- [ ] Logs não contêm dados sensíveis.
- [ ] Mensagens de erro não expõem internals.
- [ ] Dados pessoais têm finalidade definida.

---

## Entrada e saída

- [ ] Entradas são validadas.
- [ ] Limites de tamanho foram definidos.
- [ ] Strings são normalizadas quando necessário.
- [ ] Não existe interpolação insegura de SQL.
- [ ] Conteúdo retornado foi minimizado.
- [ ] Dados internos não são expostos sem necessidade.

---

# 15. Gate 11 — Multi-Tenant e isolamento

- [ ] Toda consulta operacional inclui contexto do usuário ou tenant.
- [ ] O tenant não é confiado diretamente ao payload do cliente.
- [ ] Repositories aplicam o filtro obrigatório.
- [ ] Testes cobrem acesso cruzado.
- [ ] Erros não revelam existência de recursos de outro tenant.
- [ ] Cache, eventos e logs preservam o isolamento.
- [ ] Jobs e tarefas agendadas recebem contexto explícito.
- [ ] Não existe consulta global em fluxo de usuário comum.

---

# 16. Gate 12 — Dependências

- [ ] Todo import externo possui dependência declarada.
- [ ] `requirements.txt` foi atualizado.
- [ ] `pyproject.toml` foi atualizado quando aplicável.
- [ ] As versões estão compatíveis.
- [ ] Dependências não utilizadas foram removidas.
- [ ] Não existem bibliotecas duplicadas para a mesma finalidade.
- [ ] `python -m pip check` foi executado.
- [ ] O projeto instala em ambiente limpo.
- [ ] Dependências transitivas críticas foram avaliadas.
- [ ] Licença e manutenção da biblioteca foram consideradas.
- [ ] Nenhuma dependência foi adicionada sem necessidade real.

---

# 17. Gate 13 — Qualidade de código

- [ ] Nomes expressam intenção.
- [ ] Métodos possuem responsabilidade única.
- [ ] Classes não acumulam responsabilidades.
- [ ] Não existem números mágicos.
- [ ] Não existe duplicação relevante.
- [ ] Não existe código morto.
- [ ] Não existem comentários obsoletos.
- [ ] Não existem TODOs ou FIXMEs não registrados.
- [ ] Não existem blocos comentados.
- [ ] Funções complexas foram simplificadas.
- [ ] Condições complexas foram nomeadas.
- [ ] Erros não são silenciosamente ignorados.
- [ ] Tipos estão claros.
- [ ] Imports estão organizados.
- [ ] O código segue as convenções do projeto.
- [ ] O código está no diretório correto.
- [ ] Arquivos genéricos excessivamente grandes foram evitados.

---

# 18. Gate 14 — Tempo e datas

- [ ] Timestamps utilizam UTC.
- [ ] Datetimes possuem timezone.
- [ ] Não existe `datetime.now()` sem timezone no domínio.
- [ ] Regras temporais são testáveis.
- [ ] Clock injetável foi considerado quando necessário.
- [ ] Expirações são comparadas usando a mesma referência temporal.
- [ ] Serialização mantém timezone.
- [ ] Banco e aplicação usam convenção consistente.

---

# 19. Gate 15 — Performance

- [ ] Não existem consultas N+1.
- [ ] Não existem consultas repetidas desnecessariamente.
- [ ] Índices suportam os filtros principais.
- [ ] Coleções grandes utilizam paginação.
- [ ] Operações pesadas não bloqueiam a interface.
- [ ] Não existe carregamento excessivo de Aggregates.
- [ ] Queries de leitura retornam apenas os campos necessários.
- [ ] Serialização desnecessária foi evitada.
- [ ] Cache não foi introduzido prematuramente.
- [ ] Otimizações possuem evidência ou justificativa.

---

# 20. Gate 16 — Observabilidade

- [ ] Operações críticas possuem logs adequados.
- [ ] Logs não contêm dados sensíveis.
- [ ] Logs possuem contexto suficiente.
- [ ] Erros inesperados são registrados.
- [ ] Eventos de segurança são observáveis.
- [ ] Não existem `print()` em código de produção.
- [ ] Correlation ID foi considerado em fluxos distribuídos.
- [ ] Métricas foram consideradas para operações críticas.
- [ ] Falhas de integração podem ser diagnosticadas.

---

# 21. Gate 17 — Testes

## Unitários

- [ ] Regras de domínio possuem testes.
- [ ] Invariantes possuem testes.
- [ ] Value Objects possuem testes.
- [ ] Domain Errors possuem testes.
- [ ] Handlers possuem testes.
- [ ] Casos negativos foram cobertos.
- [ ] Testes não dependem de banco real.
- [ ] Testes são determinísticos.
- [ ] Testes não dependem de horário real quando evitável.

---

## Integração

- [ ] Repositories possuem testes.
- [ ] Mappers possuem testes.
- [ ] Constraints do banco foram testadas.
- [ ] Unit of Work foi testado.
- [ ] Rollback foi testado.
- [ ] Isolamento multi-tenant foi testado.
- [ ] Migrations foram testadas.
- [ ] Integrações externas utilizam adapters ou fakes controlados.

---

## E2E

- [ ] O fluxo principal foi validado.
- [ ] Autenticação foi validada.
- [ ] Autorização foi validada.
- [ ] Cenários negativos foram validados.
- [ ] Regressões das Sprints anteriores foram validadas.
- [ ] O banco de teste está isolado.
- [ ] Nenhum teste altera o banco local de desenvolvimento.

---

## Arquiteturais

- [ ] Domain não importa camadas externas.
- [ ] Application não importa Infrastructure.
- [ ] Application não importa Presentation.
- [ ] Capabilities não importam internals umas das outras.
- [ ] Shared Kernel não depende de Capabilities.
- [ ] Presentation não acessa SQLAlchemy.
- [ ] Repositories não executam commit.
- [ ] Regras específicas da Game Engine não existem fora de GAME.

---

## Evidências obrigatórias

- [ ] `python -m pytest -v`
- [ ] `python -W error::DeprecationWarning -m pytest -v`
- [ ] `python -m pytest --cov=app --cov-report=term-missing`
- [ ] Resultado real apresentado.
- [ ] Nenhuma falha omitida.
- [ ] Nenhum teste crítico foi ignorado.
- [ ] Cobertura não diminuiu sem justificativa.

---

# 22. Gate 18 — Cobertura

- [ ] Cobertura total foi apresentada.
- [ ] Domain atende à meta mínima oficial.
- [ ] Linhas críticas possuem cobertura.
- [ ] Branches de erro possuem cobertura.
- [ ] Cobertura não foi inflada por testes sem assertividade.
- [ ] Arquivos com baixa cobertura foram analisados.
- [ ] Quedas de cobertura foram justificadas.
- [ ] Cobertura foi executada no mesmo código entregue.

Meta atual:

```text
Domain: mínimo de 90%
Projeto: preservar ou aumentar
```

---

# 23. Gate 19 — Inicialização e execução

- [ ] A aplicação inicia.
- [ ] Não existe `ImportError`.
- [ ] Não existe `ModuleNotFoundError`.
- [ ] Não existe `DeprecationWarning`.
- [ ] O startup conclui.
- [ ] O shutdown conclui corretamente.
- [ ] `/docs` responde.
- [ ] `/openapi.json` responde.
- [ ] As rotas esperadas estão registradas.
- [ ] Rotas proibidas não foram adicionadas.
- [ ] Configuração não depende de artefato local oculto.
- [ ] A porta utilizada foi registrada.
- [ ] Processos externos não foram interrompidos indevidamente.

Comando mínimo:

```bash
python -m uvicorn app.main:app --reload
```

---

# 24. Gate 20 — Documentação

- [ ] PRD foi atualizado quando houve mudança funcional.
- [ ] Feature Catalog foi atualizado quando necessário.
- [ ] Capability Map permanece consistente.
- [ ] Database foi atualizado quando houve mudança persistente.
- [ ] Arquitetura foi atualizada quando houve mudança estrutural.
- [ ] ADR foi criado quando necessário.
- [ ] CHANGELOG foi atualizado.
- [ ] PROJECT_STATUS foi atualizado.
- [ ] TASK_HISTORY foi atualizado.
- [ ] NEXT_TASK permaneceu consistente.
- [ ] README foi atualizado quando necessário.
- [ ] Documentos não foram duplicados.
- [ ] Não foi criado documento sem necessidade real.
- [ ] Referências e caminhos estão corretos.
- [ ] Nenhuma informação comprovadamente falsa foi registrada.

---

# 25. Gate 21 — Commits

- [ ] O plano de commits foi apresentado.
- [ ] Os commits são atômicos.
- [ ] As mensagens seguem `COMMIT_GUIDELINES.md`.
- [ ] O tipo está correto.
- [ ] O escopo está correto.
- [ ] Sprint está informada.
- [ ] Capability está informada.
- [ ] Feature e RF estão informados quando aplicáveis.
- [ ] ADR está informado quando aplicável.
- [ ] Testes declarados foram executados.
- [ ] SHAs foram apresentados.
- [ ] Nenhum segredo foi versionado.
- [ ] Nenhum ambiente virtual foi versionado.
- [ ] Nenhum banco local foi versionado.
- [ ] Nenhum commit gigante reúne toda a Sprint.
- [ ] Não houve `push --force` sem autorização.

---

# 26. Gate 22 — Branch e integração

- [ ] A branch está de acordo com `BRANCH_STRATEGY.md`.
- [ ] A branch possui nome adequado.
- [ ] A branch partiu da base correta.
- [ ] Não existem alterações não relacionadas.
- [ ] O merge não introduz conflitos não resolvidos.
- [ ] A branch de destino está atualizada.
- [ ] O histórico está compreensível.
- [ ] O merge respeita a estratégia oficial.
- [ ] A branch pode ser removida após integração.
- [ ] Nenhuma branch protegida recebeu alteração direta indevida.

---

# 27. Gate 23 — Versionamento

- [ ] A mudança está classificada corretamente.
- [ ] PATCH, MINOR ou MAJOR foi definido conforme `VERSIONING.md`.
- [ ] Breaking Changes foram identificadas.
- [ ] A versão foi atualizada quando aplicável.
- [ ] O CHANGELOG está coerente com a versão.
- [ ] Tags não foram criadas prematuramente.
- [ ] A release representa código validado.
- [ ] Migrações e contratos estão compatíveis com a versão.

---

# 28. Gate 24 — Autoauditoria do agente

Antes da entrega, o agente deverá responder:

- [ ] Implementei somente o escopo autorizado?
- [ ] Introduzi responsabilidade de outra Capability?
- [ ] Criei alguma regra não documentada?
- [ ] Tomei alguma decisão de produto?
- [ ] Criei alguma abstração prematura?
- [ ] Dupliquei algum componente existente?
- [ ] Adicionei alguma dependência desnecessária?
- [ ] Deixei algum requisito parcial?
- [ ] Executei realmente todos os comandos relatados?
- [ ] Atualizei os documentos obrigatórios?
- [ ] Os commits estão atômicos?
- [ ] O projeto está melhor do que antes?

Qualquer resposta negativa deverá ser explicada.

---

# 29. Problemas bloqueantes

A revisão deverá ser interrompida quando existir:

- conflito entre documentos oficiais;
- requisito sem Feature;
- Feature sem Capability;
- mudança arquitetural sem aprovação;
- dependência cruzada entre domínios;
- falha de segurança;
- vazamento multi-tenant;
- migration aplicada alterada;
- testes falhando;
- aplicação que não inicia;
- import quebrado;
- dependência ausente;
- funcionalidade incompleta;
- evidência apenas conceitual;
- segredo versionado;
- escopo extrapolado;
- decisão de produto tomada pelo agente.

---

# 30. Problemas não bloqueantes

Podem ser registrados como ressalva:

- melhoria de nomenclatura sem impacto;
- oportunidade de refatoração futura;
- ampliação de cobertura já acima da meta;
- otimização sem gargalo comprovado;
- documentação complementar;
- melhoria de observabilidade não crítica;
- extração futura de abstração ainda prematura.

Toda ressalva deverá possuir:

- descrição;
- impacto;
- prioridade;
- momento recomendado para correção.

---

# 31. Formato do relatório de revisão

```md
# Relatório de Revisão Técnica

## Identificação

- Sprint:
- Capability:
- Branch:
- Commit inicial:
- Commit final:
- Revisor:
- Data:

## Resultado

- Status:
- Decisão:

## Escopo

- Autorizado:
- Implementado:
- Fora do escopo identificado:

## Pontos aprovados

- ...

## Problemas bloqueantes

- ...

## Ressalvas

- ...

## Arquitetura

- ...

## Domínio

- ...

## Banco

- ...

## Segurança

- ...

## Testes

- Comando:
- Resultado:
- Cobertura:

## Execução

- Startup:
- Rotas:
- Imports:
- Warnings:

## Commits

- SHA:
- Mensagem:
- Conformidade:

## Documentação

- ...

## Definition of Done

- Atendida:
- Pendências:

## Decisão final

- Aprovado
- Aprovado com ressalvas
- Correções obrigatórias
- Reprovado
- Bloqueado
```

---

# 32. Checklist resumido de aprovação

## Produto e escopo

- [ ] Escopo autorizado.
- [ ] RFs completos.
- [ ] Nenhuma funcionalidade extra.

## Arquitetura

- [ ] Clean Architecture.
- [ ] Capabilities isoladas.
- [ ] Shared Kernel correto.
- [ ] Sem acoplamento cruzado.

## Domínio

- [ ] Invariantes protegidas.
- [ ] Value Objects válidos.
- [ ] Domain Errors claros.
- [ ] Sem regras externas.

## Banco

- [ ] Migrations corretas.
- [ ] Transações corretas.
- [ ] Constraints corretas.
- [ ] Alembic em head.

## Segurança

- [ ] Autenticação.
- [ ] Autorização.
- [ ] Multi-tenant.
- [ ] Dados sensíveis protegidos.

## Testes

- [ ] Unitários.
- [ ] Integração.
- [ ] E2E.
- [ ] Arquiteturais.
- [ ] Cobertura.
- [ ] Regressão.

## Execução

- [ ] Imports.
- [ ] Startup.
- [ ] Rotas.
- [ ] Sem depreciações.

## Governança

- [ ] Documentação.
- [ ] Commits.
- [ ] Branch.
- [ ] Versionamento.
- [ ] DoD.

---

# 33. Regra final

Nenhuma alteração do LifeOS poderá ser aprovada apenas porque:

- o código parece correto;
- os testes “deveriam passar”;
- o agente declarou sucesso;
- a aplicação funcionou em um cenário isolado;
- a cobertura está alta.

A aprovação exige a combinação de:

```text
Escopo correto
+
Arquitetura preservada
+
Domínio consistente
+
Segurança validada
+
Testes reais
+
Execução real
+
Documentação atualizada
+
Commits rastreáveis
+
Definition of Done atendida
```

Se qualquer elemento obrigatório estiver ausente, a alteração não estará pronta para aprovação.