# MIGRATIONS

## 0007 — Reading History Index

Revision 0007, based on 0006, creates only
ix_reading_sessions_user_started_id on
reading_sessions(user_id, started_at, id). Downgrade removes only this index.
No table, column, or constraint is added.

## READ-005 — Coordinated Completion Cutover

Current Alembic head is `0007_add_reading_sessions_user_history_index`.
Migration 0008 is planned but NOT CREATED. It owns the complete READ-005
Completion schema, constraints, indexes, and historical backfill; Alembic remains
the sole schema owner.

Migration/backfill and Slice 4 transactional-write activation are one controlled
operational cutover, although they remain separate implementation and review
scopes. Before the backfill begins, create and verify a backup, exclude
ReadingSession writes, and stop old writable application instances. Validate
integrity before and after migration/backfill, then start only the Slice 4-capable
runtime before re-enabling writes.

It is forbidden to use runtime `create_all()`, table-existence fallback, or a
writable old ReadingSession runtime during this cutover. A schema-only runtime
activation followed by historical backfill is also forbidden.

For planned Migration 0008, migration-local IDs follow the canonical string
representation of pinned `tsidpy==1.1.5` (currently 13 characters); `VARCHAR(26)`
remains storage capacity. Before its first DDL, the migration must validate and
precompute all owner-consistent backfill candidates. An owner-consistent interval
outside the current Book page boundary, or a required unreadable/non-orderable
timestamp, aborts before DDL: no clamp, truncation, rewrite, deletion, or
automatic repair is allowed. Owner-mismatched sessions are excluded from
backfill, not repaired, and do not independently block it. Backup, traffic
exclusion, and pre/post integrity checks remain mandatory.

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Estratégia Oficial de Migrações de Banco de Dados  
**Banco Inicial:** SQLite  
**Banco Futuro:** PostgreSQL  
**Ferramenta Oficial:** Alembic  
**ORM:** SQLAlchemy

---

# 1. Objetivo

Este documento define a estratégia oficial de migrações do banco de dados do LifeOS.

Seu objetivo é garantir que toda alteração estrutural no schema seja:

- versionada;
- rastreável;
- reproduzível;
- testável;
- revisável;
- segura;
- compatível com ambientes existentes;
- alinhada à arquitetura oficial do projeto.

Nenhuma alteração de schema poderá ser considerada concluída sem uma migration correspondente.

---

# 2. Escopo

Este documento cobre:

- ferramenta oficial de migração;
- estrutura de diretórios;
- convenções de nomenclatura;
- criação de migrations;
- upgrade;
- downgrade;
- versionamento;
- migrations de dados;
- migrations destrutivas;
- compatibilidade entre SQLite e PostgreSQL;
- testes;
- rollback;
- backup;
- observabilidade;
- regras para agentes de IA;
- critérios de aceite;
- Definition of Done.

Este documento complementa:

- `DATABASE.md`;
- `ERD.md`;
- `SCHEMA.md`;
- `INDEXES.md`.

---

# 3. Princípios

Toda migration deve obedecer aos seguintes princípios:

1. Toda alteração de schema deve ser versionada.
2. Toda migration deve possuir objetivo único.
3. Toda migration deve ser pequena.
4. Toda migration deve ser determinística.
5. Toda migration deve ser revisável.
6. Toda migration deve preservar dados sempre que possível.
7. Toda migration deve considerar rollback.
8. Toda migration deve ser testada antes de uso real.
9. Toda migration deve respeitar Multi-Tenant.
10. Toda migration deve manter compatibilidade com o domínio.
11. Toda migration destrutiva exige justificativa explícita.
12. Toda migration relevante deve atualizar a documentação.

---

# 4. Ferramenta Oficial

A ferramenta oficial será:

```text
Alembic
```

Alembic será utilizado para:

- criar tabelas;
- alterar tabelas;
- criar colunas;
- remover colunas;
- criar Foreign Keys;
- criar Constraints;
- criar índices;
- alterar tipos;
- versionar dados de referência;
- executar migrations de dados;
- controlar upgrade e downgrade.

---

# 5. Estrutura Oficial

```text
migrations/
├── env.py
├── script.py.mako
├── README.md
└── versions/
    ├── 0001_create_users.py
    ├── 0002_create_characters.py
    ├── 0003_create_health_tables.py
    ├── 0004_create_workout_tables.py
    └── ...
```

Configuração na raiz:

```text
alembic.ini
```

---

# 6. Convenção de Nomenclatura

Formato oficial:

```text
NNNN_descricao_curta.py
```

Exemplos:

```text
0001_create_users.py
0002_create_characters.py
0003_create_character_attributes.py
0004_create_sleep_records.py
0005_add_user_id_indexes.py
0006_add_password_reset_tokens.py
```

Regras:

- prefixo numérico sequencial;
- nome em `snake_case`;
- descrição curta;
- verbo explícito;
- sem nomes genéricos;
- sem reutilização de números.

---

# 7. Identificador da Revision

Cada migration deve possuir:

```python
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None
```

Exemplo seguinte:

```python
revision = "0002"
down_revision = "0001"
```

A sequência deve permanecer linear na fase inicial.

Branches de migration devem ser evitadas.

---

# 8. Modelo Oficial

```python
from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )


def downgrade() -> None:
    op.drop_table("users")
```

---

# 9. Regra de Uma Responsabilidade

Cada migration deve representar uma alteração coesa.

Correto:

```text
0005_create_workout_records.py
```

Incorreto:

```text
0005_create_workout_records_add_indexes_fix_users_add_quests.py
```

Quando houver mudanças independentes, criar migrations separadas.

---

# 10. Estado Atual das Migrations

A cadeia aplicada permanece linear:

```text
0001_create_users_table
↓
0002_create_players_and_characters_tables
↓
0003_create_auth_tables
↓
0004_create_books_table
↓
0005_create_reading_sessions_table
↓
0006_add_reading_sessions_user_book_index
↓
0007_add_reading_sessions_user_history_index (head)
```

A migration `0004_create_books_table.py` permanece inalterada e mantém a tabela `books`, sua Foreign Key de ownership, a constraint de `total_pages` e o índice `ix_books_user_id`.

A migration `0005_create_reading_sessions_table.py` possui:

- revision `0005`;
- down revision `0004`;
- criação da tabela `reading_sessions`;
- Primary Key TSID em `id`;
- Foreign Keys obrigatórias de `user_id` para `users.id` e de `book_id` para `books.id`;
- constraints `start_page >= 1`, `end_page >= start_page` e `ended_at >= started_at`;
- timestamps funcionais e técnicos;
- nenhuma coluna `pages_read`;
- nenhum índice secundário.

O downgrade de `0005` remove a tabela `reading_sessions` e os objetos criados com ela.

A migration `0006_add_reading_sessions_user_book_index.py` possui:

- revision `0006`;
- down revision `0005`;
- finalidade: adicionar o índice owner/book de `reading_sessions`;
- upgrade: cria `ix_reading_sessions_user_book` na tabela `reading_sessions`, nas colunas `(user_id, book_id)`, com `unique=False`;
- downgrade: remove exclusivamente `ix_reading_sessions_user_book` da tabela `reading_sessions`.

A migration `0006` não cria tabela, não cria coluna, não altera dados, não persiste progresso e não modifica migrations anteriores. Após READ-003, `0006` was the then-current head; the current Alembic head is `0007`.

As migrations `0001`, `0002`, `0003` e `0004` permanecem inalteradas.

---
# 11. Autogenerate

Alembic `autogenerate` poderá ser utilizado como apoio.

Comando:

```bash
alembic revision --autogenerate -m "create users"
```

Entretanto:

> Toda migration gerada automaticamente deve ser revisada manualmente.

O agente ou desenvolvedor deve conferir:

- nomes de Constraints;
- tipos;
- nullable;
- Foreign Keys;
- índices;
- ordem das operações;
- compatibilidade com SQLite;
- downgrade;
- dados existentes.

Autogenerate nunca substitui revisão técnica.

---

# 12. Upgrade

Comando oficial:

```bash
alembic upgrade head
```

O upgrade deve:

- executar migrations pendentes;
- respeitar a ordem;
- falhar de forma explícita;
- não ignorar erros;
- não deixar estado parcialmente aplicado.

---

# 13. Downgrade

Comando:

```bash
alembic downgrade -1
```

ou:

```bash
alembic downgrade <revision>
```

Toda migration deve possuir downgrade quando tecnicamente viável.

Quando downgrade seguro não for possível, o motivo deve estar documentado no arquivo da migration.

---

# 14. Migrations Irreversíveis

Uma migration poderá ser irreversível apenas quando:

- houver perda inevitável de dados;
- a reversão for tecnicamente insegura;
- existir justificativa;
- existir backup;
- houver aprovação explícita.

Exemplo:

```python
def downgrade() -> None:
    raise RuntimeError(
        "Irreversible migration: historical data was normalized."
    )
```

---

# 15. Migrations de Dados

Migrations de dados alteram conteúdo existente.

Exemplos:

- preencher `user_id`;
- converter códigos;
- migrar status;
- criar atributos padrão;
- normalizar valores;
- copiar dados para nova tabela.

Devem ser:

- determinísticas;
- idempotentes quando possível;
- transacionais;
- testadas com dados reais simulados;
- separadas de migrations estruturais quando o risco for elevado.

---

# 16. Separação entre Schema e Dados

Preferência oficial:

```text
Migration A → cria estrutura
Migration B → migra dados
Migration C → aplica constraint final
```

Exemplo:

```text
0040_add_attribute_code_nullable
0041_backfill_attribute_code
0042_make_attribute_code_not_null
```

Essa estratégia reduz risco.

---

# 17. Adição de Coluna Obrigatória

Não adicionar diretamente coluna `NOT NULL` em tabela com dados existentes sem valor padrão seguro.

Fluxo recomendado:

1. adicionar coluna nullable;
2. preencher dados;
3. validar dados;
4. alterar para `NOT NULL`.

---

# 18. Remoção de Coluna

Antes de remover uma coluna:

1. confirmar ausência de uso;
2. atualizar código;
3. atualizar documentação;
4. realizar backup;
5. migrar dados relevantes;
6. criar migration específica;
7. avaliar downgrade.

Remoção direta sem análise é proibida.

---

# 19. Renomeação de Coluna

Renomeações devem preservar dados.

Exemplo:

```python
op.alter_column(
    "users",
    "name",
    new_column_name="full_name",
)
```

Quando SQLite não suportar diretamente a operação, utilizar batch mode.

---

# 20. Batch Mode no SQLite

SQLite possui limitações para alterações estruturais.

Alembic deve utilizar:

```python
with op.batch_alter_table("users") as batch_op:
    batch_op.add_column(
        sa.Column("status", sa.String(length=30), nullable=True)
    )
```

Batch mode será obrigatório quando a operação exigir recriação segura da tabela.

---

# 21. Foreign Keys no SQLite

Foreign Keys devem ser habilitadas:

```sql
PRAGMA foreign_keys = ON;
```

Toda migration que cria relacionamento deve:

- definir a FK;
- definir política de exclusão;
- avaliar índice;
- testar integridade.

---

# 22. Constraints

Toda Constraint deve possuir nome explícito.

Exemplos:

```text
pk_users
fk_characters_user_id_users
uq_users_email
ck_characters_total_experience_non_negative
ix_workout_records_user_id_occurred_at
```

Evitar nomes gerados automaticamente.

---

# 23. Convenção de Nomes de Constraints

```text
pk_<table>
fk_<table>_<column>_<referenced_table>
uq_<table>_<column_or_columns>
ck_<table>_<rule>
ix_<table>_<column_or_columns>
```

Exemplos:

```text
pk_users
fk_characters_user_id_users
uq_character_attributes_character_id_attribute_code
ck_sleep_records_sleep_score_range
ix_workout_records_user_id_occurred_at
```

---

# 24. Criação de Índices

Índices devem ser criados via migration.

Exemplo:

```python
op.create_index(
    "ix_workout_records_user_id_occurred_at",
    "workout_records",
    ["user_id", "occurred_at"],
)
```

Toda criação deve estar alinhada ao `INDEXES.md`.

---

# 25. Remoção de Índices

Exemplo:

```python
op.drop_index(
    "ix_workout_records_user_id_occurred_at",
    table_name="workout_records",
)
```

Antes de remover:

- analisar plano de execução;
- confirmar redundância;
- medir impacto;
- atualizar documentação.

---

# 26. Compatibilidade SQLite e PostgreSQL

Migrations devem evitar recursos exclusivos de um banco quando houver alternativa portátil.

Evitar no início:

- tipos proprietários;
- funções específicas;
- índices exclusivos;
- SQL não portátil;
- triggers dependentes do banco.

Quando necessário, isolar por dialect e documentar.

---

# 27. Tipos Portáveis

Preferir:

```text
String
Integer
Numeric
Boolean
Date
DateTime
Text
```

Evitar:

```text
JSONB
ARRAY
UUID nativo
ENUM nativo
```

na fase inicial, salvo decisão arquitetural formal.

---

# 28. ENUMs

Preferência inicial:

```text
VARCHAR + validação no Domain
```

ou:

```text
VARCHAR + CHECK
```

Isso facilita compatibilidade entre SQLite e PostgreSQL.

---

# 29. JSON

Na fase inicial, campos JSON serão persistidos como:

```text
TEXT
```

com serialização controlada.

Futuramente, PostgreSQL poderá utilizar `JSONB`.

Essa mudança exigirá migration específica.

---

# 30. Transações

Migrations devem executar dentro de transação quando suportado.

Falhas devem resultar em rollback.

Operações grandes devem ser planejadas para evitar:

- locks longos;
- consumo excessivo de memória;
- transações gigantes;
- indisponibilidade prolongada.

---

# 31. Backup Antes de Migration

Antes de aplicar migrations em ambiente com dados reais:

1. criar backup;
2. validar integridade;
3. registrar versão atual;
4. executar migration;
5. validar schema;
6. validar dados;
7. manter backup até confirmação.

---

# 32. Verificação Pré-Migration

Antes de aplicar:

```bash
alembic current
alembic history
alembic heads
```

Verificar:

- revisão atual;
- existência de múltiplos heads;
- ordem;
- pendências;
- branch inesperada.

---

# 33. Verificação Pós-Migration

Após aplicar:

```bash
alembic current
```

Também validar:

- tabelas;
- colunas;
- constraints;
- índices;
- dados;
- integridade;
- execução da aplicação.

---

# 34. Multiple Heads

Multiple heads são proibidos na fase inicial.

Caso ocorram:

- interromper aplicação;
- investigar causa;
- criar merge revision;
- revisar processo.

Não aplicar migrations divergentes sem resolução.

---

# 35. Baseline

Instalações novas devem executar:

```bash
alembic upgrade head
```

Não utilizar dumps manuais como baseline oficial.

O histórico de migrations é a fonte de verdade estrutural.

---

# 36. `create_all()`

`Base.metadata.create_all()` poderá ser usado apenas:

- em testes isolados;
- em protótipos descartáveis;
- em bootstrap de teste.

Não poderá substituir Alembic em ambientes persistentes.

---

# 37. Seed Inicial

Dados de referência poderão ser inseridos por migration ou script versionado.

Exemplos:

- atributos oficiais;
- Skills padrão;
- Achievements iniciais;
- títulos;
- tipos de exercício padrão.

Seeds devem ser idempotentes.

---

# 38. Migrations e Multi-Tenant

Toda nova tabela operacional deve possuir `user_id` quando aplicável.

A migration deve avaliar:

- FK para `users`;
- índice;
- UNIQUE composta;
- backfill;
- ownership;
- impacto em dados existentes.

---

# 39. Migrations Destrutivas

São consideradas destrutivas:

- drop table;
- drop column;
- alteração incompatível de tipo;
- redução de tamanho;
- remoção de constraint necessária;
- sobrescrita de dados;
- exclusão em massa.

Exigem:

- justificativa;
- backup;
- teste;
- plano de rollback;
- atualização documental;
- aprovação.

---

# 40. Alteração de Tipo

Fluxo seguro:

1. criar nova coluna;
2. converter dados;
3. validar;
4. alterar leitura do código;
5. remover coluna antiga em migration posterior.

Evitar cast destrutivo direto.

---

# 41. Grandes Volumes

Para migrations com grande volume:

- processar em lotes;
- evitar carregar tudo em memória;
- registrar progresso;
- permitir reexecução;
- reduzir tempo de lock;
- testar com volume representativo.

---

# 42. Observabilidade

Toda execução deve registrar:

- revision inicial;
- revision final;
- duração;
- resultado;
- erro;
- ambiente;
- backup associado.

Nunca registrar dados sensíveis.

---

# 43. Testes de Migration

Toda migration relevante deve possuir teste de integração.

Cenários:

- banco vazio → upgrade;
- banco anterior → upgrade;
- upgrade → downgrade;
- dados existentes preservados;
- constraints aplicadas;
- índices criados;
- Multi-Tenant preservado.

---

# 44. Teste de Upgrade Completo

Deve existir teste que:

1. cria banco vazio;
2. executa todas as migrations;
3. valida `head`;
4. inspeciona tabelas;
5. valida schema final.

---

# 45. Teste de Downgrade

Quando suportado:

1. aplica migration;
2. insere dados de teste;
3. executa downgrade;
4. valida estado anterior;
5. verifica perda esperada ou inexistente.

---

# 46. Teste com Dados Legados

Migrations de dados devem possuir fixtures que representem versões anteriores.

Exemplo:

```text
tests/fixtures/migrations/0039_before_attribute_backfill.sql
```

---

# 47. Scripts Oficiais

```text
scripts/
├── migrate.py
├── migration_status.py
├── validate_migrations.py
└── backup_before_migration.py
```

Scripts devem chamar Alembic oficialmente.

Não duplicar lógica de migration.

---

# 48. Comandos Oficiais

Criar migration:

```bash
alembic revision -m "create users"
```

Criar automaticamente:

```bash
alembic revision --autogenerate -m "create users"
```

Aplicar:

```bash
alembic upgrade head
```

Reverter uma:

```bash
alembic downgrade -1
```

Ver histórico:

```bash
alembic history
```

Ver atual:

```bash
alembic current
```

---

# 49. Revisão de Migration

Toda revisão deve conferir:

- nome;
- revision;
- down_revision;
- upgrade;
- downgrade;
- constraints;
- índices;
- tipos;
- nullable;
- Foreign Keys;
- defaults;
- compatibilidade;
- risco de perda;
- teste;
- documentação.

---

# 50. Server Default

Defaults estruturais devem ser definidos com cuidado.

Exemplo:

```python
sa.Column(
    "active",
    sa.Boolean(),
    nullable=False,
    server_default=sa.true(),
)
```

Após backfill, avaliar remover `server_default` quando ele for apenas temporário.

---

# 51. Application Default vs Server Default

Application Default:

- definido pelo domínio ou aplicação;
- principal mecanismo para regras de negócio.

Server Default:

- proteção estrutural;
- apoio à migration;
- compatibilidade com inserções externas controladas.

Não duplicar regras complexas no banco.

---

# 52. Timestamps

Migrations devem criar:

```text
created_at
updated_at
```

com tipos consistentes.

A aplicação continuará responsável por gerar valores via `Clock`.

---

# 53. Dados Sensíveis

Migrations nunca devem:

- registrar senha;
- copiar token bruto;
- expor notas terapêuticas;
- imprimir dados biométricos;
- incluir dados pessoais no nome da migration;
- persistir segredos.

---

# 54. Migrations de Segurança

Exemplos:

- aumentar tamanho de hash;
- substituir token bruto por hash;
- adicionar auditoria;
- adicionar revogação de sessão;
- criptografar campos.

Devem possuir atenção especial a compatibilidade e rollback.

---

# 55. Limpeza de Dados

Limpeza massiva deve ser separada da migration estrutural quando possível.

Preferir:

```text
Migration → prepara schema
Script controlado → limpa dados
Migration → aplica constraint
```

---

# 56. Documentação Obrigatória

Toda migration deve atualizar, quando aplicável:

- `ERD.md`;
- `SCHEMA.md`;
- `INDEXES.md`;
- `DATABASE.md`;
- ADR;
- changelog;
- documentação do módulo.

---

# 57. Changelog

Mudanças de banco relevantes devem aparecer no changelog.

Exemplo:

```text
Added:
- characters table
- unique character per user
- character attributes indexes
```

---

# 58. Ambiente de Desenvolvimento

Ao atualizar a branch:

```bash
alembic upgrade head
```

deve ser executado antes de iniciar a aplicação.

O startup pode verificar revisão, mas não deve aplicar migration automaticamente sem política explícita.

---

# 59. Ambiente de Teste

Cada suíte deve criar banco isolado e aplicar migrations do zero.

Não reutilizar banco de desenvolvimento.

---

# 60. Ambiente de Produção Futuro

Fluxo:

1. colocar aplicação em modo controlado;
2. backup;
3. validar versão;
4. aplicar migration;
5. executar smoke tests;
6. iniciar aplicação;
7. monitorar.

---

# 61. Rollback Operacional

Rollback de aplicação e rollback de banco são decisões separadas.

Nem toda reversão de código exige downgrade.

Antes de downgrade, avaliar compatibilidade do código anterior com o schema atual.

---

# 62. Forward-Only Strategy

Para ambientes futuros críticos, poderá ser adotada estratégia preferencialmente forward-only.

Nesse modelo:

- corrigir com nova migration;
- evitar downgrade destrutivo;
- manter compatibilidade gradual;
- usar expand-and-contract.

---

# 63. Expand and Contract

Estratégia recomendada para mudanças complexas:

## Expand

- adicionar nova estrutura;
- manter antiga;
- suportar ambas.

## Migrate

- copiar dados;
- alterar código;
- validar.

## Contract

- remover estrutura antiga em release posterior.

---

# 64. Exemplo Expand and Contract

Renomear `name` para `full_name`:

```text
Migration 1:
add full_name nullable

Application:
write name and full_name

Migration 2:
backfill full_name

Application:
read full_name

Migration 3:
make full_name not null

Migration 4:
drop name
```

---

# 65. Anti-patterns

São proibidos:

## Alteração manual

```sql
ALTER TABLE ...
```

executada fora de migration versionada.

## Migration gigante

Misturar dezenas de alterações independentes.

## Sem downgrade

Omitir downgrade sem justificativa.

## Uso cego de autogenerate

Aplicar código gerado sem revisão.

## Dados sensíveis

Imprimir ou migrar informações privadas sem proteção.

## Drop imediato

Remover coluna utilizada pela versão atual.

## Migration no startup

Aplicar automaticamente sem controle.

## `create_all()` como migration

Usar ORM para modificar schema persistente.

---

# 66. Como o Gemini deve utilizar este documento

Antes de criar ou alterar uma migration, o agente deve verificar:

1. Qual Feature ou requisito motivou a mudança?
2. O ERD foi atualizado?
3. O SCHEMA foi atualizado?
4. A alteração é estrutural ou de dados?
5. A migration pode ser pequena?
6. Existe risco de perda?
7. O downgrade é viável?
8. SQLite suporta a operação?
9. É necessário batch mode?
10. O `user_id` foi considerado?
11. Índices foram avaliados?
12. Constraints têm nome?
13. Dados existentes serão preservados?
14. Há testes?
15. Há necessidade de backup?
16. A documentação foi sincronizada?

---

# 67. Checklist de Implementação

- [ ] Feature relacionada identificada.
- [ ] Revision definida.
- [ ] `down_revision` correta.
- [ ] Nome oficial aplicado.
- [ ] `upgrade()` implementado.
- [ ] `downgrade()` implementado ou justificado.
- [ ] Constraints nomeadas.
- [ ] Índices criados corretamente.
- [ ] Multi-Tenant avaliado.
- [ ] Compatibilidade SQLite validada.
- [ ] Compatibilidade PostgreSQL avaliada.
- [ ] Dados existentes preservados.
- [ ] Backup previsto.
- [ ] Testes criados.
- [ ] ERD atualizado.
- [ ] SCHEMA atualizado.
- [ ] INDEXES atualizado.
- [ ] Changelog atualizado.

---

# 68. Critérios de Aceite

Este documento será considerado atendido quando:

- Alembic for a ferramenta única de evolução de schema;
- toda mudança possuir migration;
- migrations forem pequenas e rastreáveis;
- upgrade e downgrade forem definidos;
- alterações destrutivas forem controladas;
- SQLite e PostgreSQL forem considerados;
- Multi-Tenant for preservado;
- testes validarem histórico e schema final;
- documentação permanecer sincronizada.

---

# 69. Definition of Done

Uma migration só estará concluída quando:

- [ ] O objetivo estiver claro.
- [ ] O código estiver revisado.
- [ ] O upgrade funcionar em banco vazio e existente.
- [ ] O downgrade estiver validado ou documentado.
- [ ] Não houver perda não planejada.
- [ ] Constraints e índices estiverem corretos.
- [ ] Multi-Tenant estiver protegido.
- [ ] Testes passarem.
- [ ] Backup e rollback forem avaliados.
- [ ] Documentação estiver atualizada.
- [ ] O schema final corresponder ao ERD oficial.

---

# 70. Declaração Final

As migrations representam a história evolutiva do banco de dados do LifeOS.

Elas não são arquivos auxiliares nem scripts descartáveis.

Cada migration deve preservar contexto, segurança, rastreabilidade e compatibilidade.

O schema deve evoluir de forma intencional, controlada e reproduzível, sem depender de alterações manuais ou conhecimento implícito.
