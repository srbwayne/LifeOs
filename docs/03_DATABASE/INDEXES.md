# INDEXES

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Estratégia Oficial de Indexação  
**Banco Inicial:** SQLite  
**Banco Futuro:** PostgreSQL  
**ORM:** SQLAlchemy

---

# 1. Objetivo

Este documento define a estratégia oficial de indexação do LifeOS.

Seu objetivo é estabelecer padrões para criação, manutenção e evolução dos índices utilizados pelo banco de dados, garantindo desempenho consistente durante o crescimento da plataforma.

Os índices são considerados parte da arquitetura de persistência e devem ser tratados como ativos arquiteturais, não apenas como otimizações pontuais.

Este documento deve orientar:

- criação de tabelas;
- migrations;
- consultas SQL;
- Repositories;
- Analytics;
- Dashboard;
- Event Store;
- futuras migrações para PostgreSQL.

---

# 2. Escopo

Este documento cobre:

- estratégia de indexação;
- tipos de índices;
- índices obrigatórios;
- índices compostos;
- índices Multi-Tenant;
- índices por módulo;
- índices para autenticação;
- índices para gamificação;
- índices para Analytics;
- índices para Event Store;
- índices para Auditoria;
- índices específicos do SQLite;
- índices específicos do PostgreSQL;
- boas práticas;
- anti-patterns;
- regras para agentes de IA.

Este documento complementa:

- `DATABASE.md`
- `ERD.md`
- `SCHEMA.md`
- `MIGRATIONS.md`

---

# 3. Filosofia de Indexação

O LifeOS adota uma estratégia de indexação baseada em uso real da aplicação.

Um índice não deve existir apenas porque uma coluna parece importante.

Todo índice deve possuir uma justificativa técnica.

Os objetivos principais são:

- acelerar consultas;
- reduzir leituras completas de tabela;
- preservar isolamento Multi-Tenant;
- manter consultas previsíveis;
- reduzir custo computacional;
- minimizar contenção de escrita.

Ao mesmo tempo, excesso de índices deve ser evitado.

Cada índice aumenta o custo de:

- INSERT;
- UPDATE;
- DELETE;
- VACUUM;
- BACKUP.

Portanto:

> Um índice só deve existir quando produzir benefício mensurável.

---

# 4. Estratégia Geral

A estratégia oficial do LifeOS segue cinco princípios.

---

## 4.1 Indexar consultas frequentes

Campos utilizados constantemente em filtros devem possuir índice.

Exemplos:

```sql
WHERE user_id = ?
```

```sql
WHERE occurred_at >= ?
```

```sql
WHERE email = ?
```

---

## 4.2 Priorizar consultas Multi-Tenant

Como toda operação operacional utiliza `user_id`, praticamente todas as tabelas deverão possuir índice sobre esse campo.

---

## 4.3 Priorizar índices compostos

Sempre que uma consulta utilizar dois ou mais campos com frequência, deve-se avaliar um índice composto.

Exemplo:

```sql
WHERE user_id = ?
AND occurred_at BETWEEN ...
```

Índice recomendado:

```text
(user_id, occurred_at)
```

---

## 4.4 Evitar índices redundantes

Não criar:

```text
(user_id)

(user_id, occurred_at)
```

caso o primeiro nunca seja utilizado isoladamente.

A necessidade deve ser comprovada.

---

## 4.5 Revisar continuamente

Os índices deverão ser revisados periodicamente com base em:

- plano de execução;
- tempo de resposta;
- volume de dados;
- crescimento do sistema;
- métricas de produção.

---

# 5. Tipos de Índices

O LifeOS utilizará diferentes categorias de índices.

---

## 5.1 Primary Key

Toda tabela deverá possuir chave primária.

Exemplo:

```sql
PRIMARY KEY(id)
```

Características:

- único;
- obrigatório;
- indexado automaticamente.

---

## 5.2 Unique Index

Utilizado para garantir unicidade.

Exemplo:

```sql
UNIQUE(email)
```

Outro exemplo:

```sql
UNIQUE(user_id, habit_id, record_date)
```

---

## 5.3 Foreign Key Index

Foreign Keys utilizadas em consultas frequentes deverão possuir índice.

Exemplo:

```text
user_id

character_id

quest_id

workout_type_id
```

Embora alguns bancos não criem automaticamente esses índices, eles deverão ser definidos explicitamente quando necessários.

---

## 5.4 Índice Simples

Indexa apenas uma coluna.

Exemplo:

```text
email
```

ou

```text
occurred_at
```

Utilizar quando consultas utilizam apenas um campo.

---

## 5.5 Índice Composto

Indexa múltiplas colunas.

Exemplo:

```text
(user_id, occurred_at)
```

É o tipo de índice mais importante do LifeOS.

---

## 5.6 Índice Parcial

Disponível em alguns bancos (como PostgreSQL).

Exemplo:

```sql
WHERE deleted_at IS NULL
```

Na versão SQLite inicial seu uso será avaliado caso a caso.

---

## 5.7 Índice Funcional

Utilizado quando a consulta depende de uma função.

Exemplo futuro:

```sql
LOWER(email)
```

Inicialmente não será utilizado.

---

## 5.8 Full Text Index

Reservado para:

- Insights;
- Livros;
- Notas Terapêuticas;
- IA.

Será considerado apenas em versões futuras.

---

# 6. Índices Obrigatórios

Independentemente do módulo, alguns índices são obrigatórios.

---

## 6.1 Chaves Primárias

Todas as tabelas:

```text
PRIMARY KEY(id)
```

---

## 6.2 User ID

Toda tabela operacional:

```text
INDEX(user_id)
```

---

## 6.3 Foreign Keys

Toda Foreign Key utilizada em filtros frequentes.

Exemplos:

```text
character_id

therapist_id

book_id

habit_id

workout_type_id
```

---

## 6.4 Datas

Campos utilizados em histórico:

```text
occurred_at

record_date

created_at
```

---

## 6.5 Campos Únicos

Sempre utilizar UNIQUE.

Exemplos:

```text
email

code

token_hash

event_id
```

---

## 6.6 Event Store

Campos mínimos:

```text
event_type

occurred_at

status
```

---

## 6.7 Auditoria

Campos mínimos:

```text
user_id

occurred_at

action
```

---

# 7. Índices por Módulo

Cada módulo possui necessidades específicas.

---

## Authentication

Principais consultas:

```sql
SELECT *

FROM users

WHERE email = ?
```

Índice:

```text
(email)
```

---

Tokens:

```sql
WHERE token_hash = ?
```

Índice:

```text
(token_hash)
```

---

Sessões:

```sql
WHERE session_token_hash = ?
```

Índice:

```text
(session_token_hash)
```

---

## Character

Consultas frequentes:

```sql
WHERE user_id = ?
```

Índice:

```text
(user_id)
```

---

Histórico:

```sql
WHERE character_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(character_id, occurred_at)
```

---

Atributos:

```sql
WHERE character_id = ?

AND attribute_code = ?
```

Índice:

```text
(character_id, attribute_code)
```

---

## Health

Sono:

```sql
WHERE user_id = ?

ORDER BY record_date DESC
```

Índice:

```text
(user_id, record_date)
```

Mesmo padrão para:

- Wellbeing;
- Body Composition.

---

## Workout

Consultas comuns:

```sql
WHERE user_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(user_id, occurred_at)
```

---

Filtro por modalidade:

```sql
WHERE user_id = ?

AND workout_type_id = ?
```

Índice:

```text
(user_id, workout_type_id)
```

---

## Reading

Sessões:

```sql
WHERE user_id = ?

ORDER BY record_date
```

Índice:

```text
(user_id, record_date)
```

---

Livro:

```sql
WHERE book_id = ?
```

Índice:

```text
(book_id)
```

---

## Therapy

Consultas:

```sql
WHERE therapist_id = ?
```

Índice:

```text
(therapist_id)
```

---

Histórico:

```sql
WHERE user_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(user_id, occurred_at)
```

---

## Habits

Busca por hábito:

```sql
WHERE user_id = ?

AND habit_id = ?
```

Índice:

```text
(user_id, habit_id)
```

---

Histórico:

```sql
WHERE user_id = ?

AND record_date = ?
```

Índice:

```text
(user_id, record_date)
```

---

## Gamification

XP:

```sql
WHERE character_id = ?

ORDER BY occurred_at
```

Índice:

```text
(character_id, occurred_at)
```

---

Achievements:

```sql
WHERE user_id = ?
```

Índice:

```text
(user_id)
```

---

Quest Progress:

```sql
WHERE user_id = ?

AND status = ?
```

Índice:

```text
(user_id, status)
```

---

# 8. Índices Multi-Tenant

O LifeOS é uma aplicação Multi-Tenant.

Por esse motivo:

```text
user_id
```

é a coluna mais importante do sistema.

---

## Regra Oficial

Sempre que possível, o primeiro campo do índice composto deverá ser:

```text
user_id
```

Exemplo:

```text
(user_id, occurred_at)
```

Não:

```text
(occurred_at, user_id)
```

---

## Motivo

As consultas sempre iniciam identificando o usuário.

Isso reduz drasticamente o conjunto de registros analisados.

---

## Exemplos

```sql
WHERE user_id = ?
```

```sql
WHERE user_id = ?

AND record_date >= ?
```

```sql
WHERE user_id = ?

AND status = ?
```

---

## Índices Compostos Oficiais

```text
(user_id, occurred_at)

(user_id, record_date)

(user_id, status)

(user_id, habit_id)

(user_id, workout_type_id)

(user_id, therapist_id)

(user_id, book_id)

(user_id, character_id)
```

---

# 9. Índices Compostos

Índices compostos deverão refletir exatamente os filtros utilizados pelas consultas.

---

## Exemplo Correto

Consulta:

```sql
WHERE user_id = ?

AND occurred_at >= ?

ORDER BY occurred_at DESC
```

Índice:

```text
(user_id, occurred_at)
```

---

## Outro Exemplo

Consulta:

```sql
WHERE user_id = ?

AND attribute_code = ?
```

Índice:

```text
(user_id, attribute_code)
```

---

## Ordem Importa

Índice:

```text
(user_id, occurred_at)
```

é diferente de:

```text
(occurred_at, user_id)
```

A ordem deve seguir a seletividade e o padrão real das consultas.

---

## Evitar

Criar índices compostos com muitas colunas.

Exemplo:

```text
(user_id,
status,
occurred_at,
created_at,
type,
level,
score)
```

Índices muito grandes:

- ocupam espaço;
- aumentam custo de escrita;
- raramente são utilizados integralmente.

---

# 10. Índices para Autenticação

A autenticação exige consultas rápidas e altamente seletivas.

---

## Users

Consulta principal:

```sql
SELECT *

FROM users

WHERE email = ?
```

Índice obrigatório:

```text
UNIQUE(email)
```

---

## Password Reset

Consulta:

```sql
WHERE token_hash = ?
```

Índice:

```text
UNIQUE(token_hash)
```

---

## Sessões

Consulta:

```sql
WHERE session_token_hash = ?
```

Índice:

```text
UNIQUE(session_token_hash)
```

---

## Usuários Ativos

Consulta futura:

```sql
WHERE status = 'ACTIVE'
```

Índice recomendado:

```text
(status)
```

apenas se comprovada necessidade.

---

## Login

Fluxo esperado:

```text
Email

↓

UNIQUE(email)

↓

User

↓

Hash Validation

↓

Session
```

O banco nunca deve realizar busca por senha.

A autenticação sempre ocorrerá através de:

1. busca do usuário por e-mail;
2. validação do hash na aplicação;
3. criação da sessão autenticada.

---

# 11. Índices para Character

O módulo Character concentra as consultas mais frequentes da aplicação.

Ele é responsável por alimentar:

- Dashboard;
- Gamificação;
- Analytics;
- AI Mentor;
- Character Sheet.

Por esse motivo, seus índices devem privilegiar consultas rápidas por usuário e por personagem.

---

## Tabela `characters`

Consultas principais:

```sql
SELECT *

FROM characters

WHERE user_id = ?
```

Índice obrigatório:

```text
UNIQUE(user_id)
```

---

Consulta por nível:

```sql
WHERE global_level >= ?
```

Índice recomendado apenas quando houver necessidade comprovada:

```text
(global_level)
```

---

Consulta por título ativo:

```sql
WHERE active_title_id = ?
```

Índice opcional:

```text
(active_title_id)
```

---

## Tabela `character_attributes`

Consulta principal:

```sql
WHERE character_id = ?

AND attribute_code = ?
```

Índice obrigatório:

```text
(character_id, attribute_code)
```

---

Consulta para Radar Chart:

```sql
WHERE character_id = ?
```

Índice:

```text
(character_id)
```

---

## Tabela `character_history`

Consultas:

```sql
WHERE character_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(character_id, occurred_at)
```

---

# 12. Índices para Workout

O módulo Workout possui grande volume histórico.

Os índices devem favorecer consultas temporais.

---

## Tabela `workout_records`

Consulta principal:

```sql
WHERE user_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(user_id, occurred_at)
```

---

Filtro por modalidade:

```sql
WHERE user_id = ?

AND workout_type_id = ?
```

Índice:

```text
(user_id, workout_type_id)
```

---

Filtro por período

```sql
WHERE user_id = ?

AND occurred_at BETWEEN ? AND ?
```

Índice:

```text
(user_id, occurred_at)
```

---

Consulta por frequência semanal

```sql
GROUP BY occurred_at
```

Não criar índice específico.

O índice temporal existente já atende.

---

# 13. Índices para Health

As métricas biológicas são consultadas quase sempre por período.

---

## Sleep Records

Consulta:

```sql
WHERE user_id = ?

ORDER BY record_date DESC
```

Índice:

```text
(user_id, record_date)
```

---

Consulta por intervalo

```sql
WHERE user_id = ?

AND record_date BETWEEN ? AND ?
```

Mesmo índice.

---

## Wellbeing Records

Índice:

```text
(user_id, record_date)
```

---

## Body Composition

Índice:

```text
(user_id, record_date)
```

---

## Evolução corporal

Consultas:

```sql
ORDER BY record_date
```

Já cobertas pelo índice composto.

---

# 14. Índices para Reading

READ-001 implementa somente a consulta da biblioteca pessoal por proprietário.

## Books

Consulta principal:

```sql
WHERE user_id = ?
ORDER BY id ASC
```

Índices implementados:

| Índice | Coluna | Finalidade |
|---|---|---|
| Primary Key de `books` | `id` | Identidade TSID e ordenação técnica determinística. |
| `ix_books_user_id` | `user_id` | Isolamento e consulta eficiente da biblioteca do usuário autenticado. |

Não existem índices para `title`, `isbn`, status, progresso ou timestamps em READ-001.

## Reading Sessions

READ-002 autoriza somente o registro de sessões; não existe caso de uso de consulta de sessões nesta Feature.

| Índice | Coluna | Finalidade |
|---|---|---|
| Primary Key de `reading_sessions` | `id` | Identidade TSID da sessão. |

Não existem índices secundários por `user_id`, `book_id`, `started_at` ou combinações dessas colunas. Índices para consultas futuras somente poderão ser introduzidos junto ao respectivo caso de uso autorizado.

---

# 15. Índices para Therapy

As sessões terapêuticas possuem histórico crescente.

---

## Therapy Sessions

Consulta principal

```sql
WHERE user_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(user_id, occurred_at)
```

---

Filtro por terapeuta

```sql
WHERE therapist_id = ?
```

Índice:

```text
(therapist_id)
```

---

Filtro composto

```sql
WHERE user_id = ?

AND therapist_id = ?
```

Índice recomendado:

```text
(user_id, therapist_id)
```

---

# 16. Índices para Habits

Os hábitos são consultados diariamente.

---

## Habits

Consulta:

```sql
WHERE user_id = ?

AND active = TRUE
```

Índice:

```text
(user_id, active)
```

---

## Habit Records

Consulta:

```sql
WHERE user_id = ?

AND habit_id = ?
```

Índice:

```text
(user_id, habit_id)
```

---

Consulta por data

```sql
WHERE user_id = ?

AND record_date = ?
```

Índice:

```text
(user_id, record_date)
```

---

Consulta histórica

```sql
WHERE habit_id = ?

ORDER BY record_date
```

Índice:

```text
(habit_id, record_date)
```

---

## Habit Streak

Consulta:

```sql
WHERE habit_id = ?
```

Índice:

```text
UNIQUE(habit_id)
```

---

# 17. Índices para Gamification

A gamificação utiliza consultas extremamente frequentes.

---

## Experience Transactions

Consulta:

```sql
WHERE character_id = ?

ORDER BY occurred_at
```

Índice:

```text
(character_id, occurred_at)
```

---

Consulta por atributo

```sql
WHERE character_id = ?

AND attribute_code = ?
```

Índice:

```text
(character_id, attribute_code)
```

---

Consulta por origem

```sql
WHERE source_type = ?
```

Índice opcional.

Criar apenas quando necessário.

---

## Quest Progress

Consulta:

```sql
WHERE user_id = ?

AND status = ?
```

Índice:

```text
(user_id, status)
```

---

## User Skills

Consulta:

```sql
WHERE user_id = ?
```

Índice:

```text
(user_id)
```

---

## User Achievements

Consulta:

```sql
WHERE user_id = ?

ORDER BY unlocked_at DESC
```

Índice:

```text
(user_id, unlocked_at)
```

---

## User Titles

Consulta:

```sql
WHERE user_id = ?
```

Índice:

```text
(user_id)
```

---

# 18. Índices para Analytics

Analytics trabalha quase exclusivamente com filtros temporais.

---

## Analytics Snapshots

Consulta:

```sql
WHERE user_id = ?

AND period_start >= ?
```

Índice:

```text
(user_id, period_start)
```

---

## Generated Insights

Consulta:

```sql
WHERE user_id = ?

ORDER BY generated_at DESC
```

Índice:

```text
(user_id, generated_at)
```

---

Filtro por tipo

```sql
WHERE user_id = ?

AND insight_type = ?
```

Índice:

```text
(user_id, insight_type)
```

---

## Dashboard Cache

Consulta

```sql
WHERE user_id = ?

AND cache_key = ?
```

Índice:

```text
UNIQUE(user_id, cache_key)
```

---

# 19. Índices para Event Store

O Event Store poderá crescer rapidamente.

Sua estratégia deve privilegiar rastreabilidade.

---

## Event Store

Consulta

```sql
WHERE event_type = ?
```

Índice:

```text
(event_type)
```

---

Consulta

```sql
WHERE user_id = ?
```

Índice:

```text
(user_id)
```

---

Consulta

```sql
WHERE aggregate_id = ?
```

Índice:

```text
(aggregate_id)
```

---

Consulta

```sql
WHERE status = ?
```

Índice:

```text
(status)
```

---

Consulta temporal

```sql
ORDER BY occurred_at DESC
```

Índice:

```text
(occurred_at)
```

---

Consulta composta

```sql
WHERE user_id = ?

AND occurred_at >= ?
```

Índice:

```text
(user_id, occurred_at)
```

---

## Processed Events

Consulta

```sql
WHERE event_id = ?

AND handler_name = ?
```

Índice:

```text
UNIQUE(event_id, handler_name)
```

---

# 20. Índices para Auditoria

Os logs de auditoria devem permitir investigação rápida.

---

## Audit Logs

Consulta principal

```sql
WHERE user_id = ?

ORDER BY occurred_at DESC
```

Índice:

```text
(user_id, occurred_at)
```

---

Consulta por ação

```sql
WHERE action = ?
```

Índice:

```text
(action)
```

---

Consulta por entidade

```sql
WHERE entity_type = ?

AND entity_id = ?
```

Índice:

```text
(entity_type, entity_id)
```

---

Consulta composta

```sql
WHERE user_id = ?

AND action = ?

AND occurred_at >= ?
```

Índice recomendado:

```text
(user_id, action, occurred_at)
```

---

## Estratégia para Auditoria

Como os logs tendem a crescer continuamente:

- evitar índices desnecessários;
- revisar periodicamente consultas mais utilizadas;
- arquivar registros antigos quando aplicável;
- manter índices focados em investigações operacionais.

Os índices de auditoria devem priorizar rastreabilidade, sem comprometer significativamente o desempenho das operações de escrita.

---

# 21. Índices para Exportação

O módulo de exportação deve permitir localizar rapidamente relatórios gerados, verificar seu estado e realizar limpeza automática de arquivos expirados.

---

## Report Exports

Consulta principal

```sql
WHERE user_id = ?

ORDER BY requested_at DESC
```

Índice:

```text
(user_id, requested_at)
```

---

Consulta por status

```sql
WHERE status = ?
```

Índice:

```text
(status)
```

---

Consulta para limpeza automática

```sql
WHERE expires_at < CURRENT_TIMESTAMP
```

Índice:

```text
(expires_at)
```

---

Consulta composta

```sql
WHERE user_id = ?

AND status = ?
```

Índice recomendado:

```text
(user_id, status)
```

---

# 22. Índices Temporários

Existem situações em que índices temporários podem melhorar processos específicos.

Exemplos:

- importação de grandes volumes;
- migração de dados;
- reconstrução de Analytics;
- geração massiva de relatórios.

---

## Regras

Índices temporários:

- devem possuir documentação;
- devem possuir prazo de remoção;
- nunca devem permanecer indefinidamente;
- devem ser removidos ao término da operação.

---

## Exemplo

```sql
CREATE INDEX idx_temp_import
ON workout_records(user_id, occurred_at);
```

Após a conclusão:

```sql
DROP INDEX idx_temp_import;
```

---

# 23. Estratégia para SQLite

Na primeira versão do LifeOS, SQLite será utilizado como mecanismo oficial de persistência.

Os índices devem respeitar as características do SQLite.

---

## Recomendações

- utilizar índices simples e compostos;
- evitar excesso de índices;
- manter transações curtas;
- utilizar WAL quando validado;
- revisar periodicamente o plano de execução.

---

## Limitações

SQLite possui:

- apenas um escritor por vez;
- menor paralelismo;
- limitações em índices avançados.

Essas limitações são aceitáveis para o volume esperado da primeira versão.

---

## Recomendações Operacionais

Executar periodicamente:

```sql
ANALYZE;
```

e

```sql
VACUUM;
```

quando apropriado.

---

# 24. Estratégia para PostgreSQL

A arquitetura foi planejada para permitir migração futura para PostgreSQL sem alteração do domínio.

---

## Recursos previstos

Quando a migração ocorrer, poderão ser utilizados:

- Partial Indexes;
- Expression Indexes;
- Covering Indexes;
- GIN Indexes;
- BRIN Indexes;
- Full Text Search;
- Materialized Views.

---

## Exemplo

```sql
CREATE INDEX idx_active_users

ON users(email)

WHERE deleted_at IS NULL;
```

---

## Full Text Search

Poderá ser utilizado para:

- Insights;
- Livros;
- Notas Terapêuticas;
- Missões;
- IA.

---

## GIN

Indicado para:

```text
JSONB

Arrays

Full Text Search
```

---

# 25. Índices Proibidos

Alguns índices não devem ser criados.

---

## Campos com baixa seletividade

Exemplo:

```text
BOOLEAN
```

```sql
(active)
```

na maioria dos casos não produz benefício.

---

## Campos raramente consultados

Evitar indexar:

```text
description

notes

summary

comments
```

---

## Índices duplicados

Errado:

```text
(user_id)

(user_id, occurred_at)
```

caso o primeiro nunca seja utilizado.

---

## Índices excessivamente grandes

Evitar:

```text
(user_id,
status,
occurred_at,
created_at,
type,
level,
score)
```

Índices muito extensos:

- ocupam memória;
- degradam escrita;
- raramente são utilizados integralmente.

---

## Indexar todas as colunas

É proibido.

Índices devem refletir consultas reais.

---

# 26. Estratégia de Evolução

A estratégia de indexação deve evoluir juntamente com o sistema.

Nunca assumir que um índice permanecerá ideal para sempre.

---

## Quando criar novos índices

Criar apenas quando:

- uma consulta tornar-se lenta;
- Analytics indicar gargalos;
- novos módulos forem adicionados;
- novos filtros surgirem;
- o plano de execução justificar.

---

## Quando remover índices

Remover quando:

- não forem utilizados;
- duplicarem outros índices;
- aumentarem significativamente o custo de escrita;
- perderem utilidade após mudanças de negócio.

---

## Processo Oficial

Toda alteração deverá:

1. medir a consulta atual;
2. analisar o plano de execução;
3. propor o índice;
4. validar o ganho;
5. criar migration;
6. atualizar este documento.

---

# 27. Como o Gemini deve utilizar este documento

Antes de criar um índice o agente deverá responder:

- A consulta realmente precisa de índice?
- Existe índice semelhante?
- O índice será utilizado frequentemente?
- A ordem das colunas está correta?
- Existe impacto na escrita?
- O índice respeita Multi-Tenant?
- O índice será compatível com PostgreSQL?
- A migration foi criada?
- O INDEXES.md foi atualizado?

Caso qualquer resposta seja negativa, a implementação deverá ser revisada.

---

# 28. Checklist de Implementação

Antes de adicionar um índice verificar:

- [ ] Existe justificativa técnica.
- [ ] A consulta foi identificada.
- [ ] O plano de execução foi analisado.
- [ ] O índice respeita Multi-Tenant.
- [ ] Não existe índice equivalente.
- [ ] A ordem das colunas foi validada.
- [ ] O impacto na escrita foi avaliado.
- [ ] Existe migration.
- [ ] Existem testes.
- [ ] A documentação foi atualizada.

---

# 29. Critérios de Aceite

Este documento será considerado atendido quando:

- todos os módulos possuírem estratégia de indexação;
- consultas críticas estiverem cobertas;
- índices Multi-Tenant estiverem definidos;
- índices compostos estiverem documentados;
- estratégias para SQLite e PostgreSQL estiverem descritas;
- anti-patterns estiverem documentados;
- regras para agentes de IA estiverem definidas.

---

# 30. Definition of Done

Uma alteração relacionada a índices será considerada concluída quando:

- [ ] O índice estiver tecnicamente justificado.
- [ ] A migration correspondente existir.
- [ ] O impacto na performance tiver sido avaliado.
- [ ] O índice respeitar o isolamento Multi-Tenant.
- [ ] Não houver duplicidade.
- [ ] O plano de execução demonstrar benefício.
- [ ] Os testes permanecerem aprovados.
- [ ] A documentação estiver sincronizada com o schema oficial.