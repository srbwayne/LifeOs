# SCHEMA

## READ-006 — Reading Sessions Index Inventory

The reading_sessions table preserves ix_reading_sessions_user_book(user_id,
book_id) and adds ix_reading_sessions_user_started_id(user_id, started_at, id).
READ-006 adds no table or column; book_title and pages_read remain query
projection values rather than persisted ReadingSession state.

## LifeOS

**Versão:** 1.0  
**Status:** Documento Oficial  
**Documento:** Especificação Oficial do Schema Relacional  
**Banco Inicial:** SQLite  
**Banco Futuro:** PostgreSQL  
**ORM:** SQLAlchemy  
**Migrações:** Alembic

---

# 1. Objetivo

Este documento define o schema relacional oficial do LifeOS.

Seu objetivo é especificar:

- tabelas;
- colunas;
- tipos de dados;
- chaves primárias;
- chaves estrangeiras;
- constraints;
- índices esperados;
- regras Multi-Tenant;
- defaults;
- nulabilidade;
- convenções de auditoria;
- relações entre módulos;
- compatibilidade com SQLite e PostgreSQL.

Este documento é a referência oficial para:

- Models SQLAlchemy;
- migrations Alembic;
- Repositories;
- testes de integração;
- validações de persistência;
- revisão de mudanças estruturais;
- implementação por agentes de IA.

---

# 2. Relação com os Demais Documentos

Este documento deve permanecer consistente com:

- `DATABASE.md`;
- `ERD.md`;
- `INDEXES.md`;
- `MIGRATIONS.md`;
- `docs/02_ARCHITECTURE/03_DDD.md`;
- `docs/02_ARCHITECTURE/05_MODULAR_MONOLITH.md`;
- `01_PRODUCT/FEATURE_CATALOG.md`;
- `01_PRODUCT/PRD.md`.

Em caso de divergência:

1. o PRD define a necessidade funcional;
2. o DDD define o significado do domínio;
3. o ERD define os relacionamentos;
4. este documento define a estrutura persistente;
5. migrations materializam a evolução do schema.

---

# 3. Princípios do Schema

O schema deve obedecer aos seguintes princípios:

1. Toda tabela possui uma responsabilidade clara.
2. Toda tabela operacional pertence a um módulo.
3. Toda tabela operacional deve possuir `user_id` quando aplicável.
4. Toda chave primária utiliza UUID v4.
5. Toda Foreign Key deve possuir nome explícito.
6. Toda Constraint deve possuir nome explícito.
7. Toda coluna deve possuir tipo compatível com SQLite e PostgreSQL.
8. Toda tabela relevante deve possuir auditoria temporal.
9. Toda alteração deve possuir migration.
10. Toda consulta operacional deve preservar isolamento Multi-Tenant.
11. Models ORM não substituem Entities de domínio.
12. O schema deve evitar duplicação semântica.

---

# 4. Convenções Gerais

## 4.1 Tabelas

- nomes em inglês;
- `snake_case`;
- plural;
- sem prefixos técnicos desnecessários.

Exemplos:

```text
users
characters
sleep_records
workout_records
experience_transactions
```

---

## 4.2 Colunas

- nomes em inglês;
- `snake_case`;
- semanticamente explícitos;
- sem abreviações ambíguas.

Exemplos:

```text
created_at
updated_at
occurred_at
total_experience
body_fat_percentage
```

---

## 4.3 Primary Keys

Padrão:

```text
id VARCHAR(36) PRIMARY KEY
```

O valor deve ser gerado pela aplicação.

---

## 4.4 Foreign Keys

Padrão:

```text
<entity>_id VARCHAR(36) NOT NULL
```

Exemplos:

```text
user_id
character_id
workout_type_id
therapist_id
```

---

## 4.5 Timestamps

Padrão:

```text
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
```

Quando aplicável:

```text
deleted_at DATETIME NULL
occurred_at DATETIME NOT NULL
expires_at DATETIME NULL
```

Todos os timestamps devem ser armazenados em UTC.

---

# 5. Tipos de Dados Oficiais

| Conceito | Tipo SQL portátil |
|---|---|
| UUID | `VARCHAR(36)` |
| Texto curto | `VARCHAR(n)` |
| Texto longo | `TEXT` |
| Inteiro | `INTEGER` |
| Decimal | `NUMERIC(p,s)` |
| Data | `DATE` |
| Data e hora | `DATETIME` |
| Booleano | `BOOLEAN` |
| JSON inicial | `TEXT` |
| Hash | `VARCHAR(255)` |
| Código | `VARCHAR(100)` |

---

# 6. Módulo Authentication

## 6.1 Tabela `users`

```sql
CREATE TABLE users (
    id VARCHAR(36) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    sex VARCHAR(20),
    height_cm NUMERIC(6,2),
    status VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME,

    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT ck_users_height_positive
        CHECK (height_cm IS NULL OR height_cm > 0)
);
```

Regras:

- `email` é globalmente único;
- `status` deve utilizar códigos definidos pela aplicação;
- `password_hash` nunca contém senha em texto puro;
- `deleted_at` representa exclusão lógica.

Valores iniciais de `status`:

```text
ACTIVE
INACTIVE
BLOCKED
PENDING
DELETED
```

---

## 6.2 Tabela `user_preferences`

```sql
CREATE TABLE user_preferences (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    theme VARCHAR(50) NOT NULL,
    language VARCHAR(10) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    email_notifications_enabled BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_user_preferences PRIMARY KEY (id),
    CONSTRAINT fk_user_preferences_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_user_preferences_user_id UNIQUE (user_id)
);
```

---

## 6.3 Tabela `user_sessions`

```sql
CREATE TABLE user_sessions (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    session_token_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    expires_at DATETIME NOT NULL,
    revoked_at DATETIME,
    last_activity_at DATETIME,

    CONSTRAINT pk_user_sessions PRIMARY KEY (id),
    CONSTRAINT fk_user_sessions_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_user_sessions_token_hash
        UNIQUE (session_token_hash)
);
```

---

## 6.4 Tabela `password_reset_tokens`

```sql
CREATE TABLE password_reset_tokens (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    used_at DATETIME,
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_password_reset_tokens PRIMARY KEY (id),
    CONSTRAINT fk_password_reset_tokens_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_password_reset_tokens_token_hash
        UNIQUE (token_hash)
);
```

---

# 7. Módulo Character

## 7.1 Tabela `characters`

```sql
CREATE TABLE characters (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    avatar_path VARCHAR(500),
    global_level INTEGER NOT NULL,
    total_experience INTEGER NOT NULL,
    class_code VARCHAR(50),
    guild_name VARCHAR(100),
    active_title_id VARCHAR(36),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_characters PRIMARY KEY (id),
    CONSTRAINT fk_characters_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_characters_user_id UNIQUE (user_id),
    CONSTRAINT ck_characters_global_level_min
        CHECK (global_level >= 1),
    CONSTRAINT ck_characters_total_experience_non_negative
        CHECK (total_experience >= 0)
);
```

---

## 7.2 Tabela `character_attributes`

```sql
CREATE TABLE character_attributes (
    id VARCHAR(36) NOT NULL,
    character_id VARCHAR(36) NOT NULL,
    attribute_code VARCHAR(10) NOT NULL,
    attribute_name VARCHAR(100) NOT NULL,
    level INTEGER NOT NULL,
    current_experience INTEGER NOT NULL,
    total_experience INTEGER NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_character_attributes PRIMARY KEY (id),
    CONSTRAINT fk_character_attributes_character_id_characters
        FOREIGN KEY (character_id) REFERENCES characters(id),
    CONSTRAINT uq_character_attributes_character_code
        UNIQUE (character_id, attribute_code),
    CONSTRAINT ck_character_attributes_level_min
        CHECK (level >= 1),
    CONSTRAINT ck_character_attributes_current_experience_non_negative
        CHECK (current_experience >= 0),
    CONSTRAINT ck_character_attributes_total_experience_non_negative
        CHECK (total_experience >= 0)
);
```

Códigos oficiais:

```text
COR
LIN
TRA
TER
LOG
MUS
ESP
NAT
```

---

## 7.3 Tabela `character_history`

```sql
CREATE TABLE character_history (
    id VARCHAR(36) NOT NULL,
    character_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    previous_value_json TEXT,
    new_value_json TEXT,
    occurred_at DATETIME NOT NULL,

    CONSTRAINT pk_character_history PRIMARY KEY (id),
    CONSTRAINT fk_character_history_character_id_characters
        FOREIGN KEY (character_id) REFERENCES characters(id),
    CONSTRAINT fk_character_history_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

# 8. Módulo Health

## 8.1 Tabela `sleep_records`

```sql
CREATE TABLE sleep_records (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    record_date DATE NOT NULL,
    sleep_duration_hours NUMERIC(4,2),
    hrv_ms INTEGER,
    resting_heart_rate_bpm INTEGER,
    deep_sleep_minutes INTEGER,
    rem_sleep_minutes INTEGER,
    sleep_score INTEGER,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_sleep_records PRIMARY KEY (id),
    CONSTRAINT fk_sleep_records_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_sleep_records_user_date
        UNIQUE (user_id, record_date),
    CONSTRAINT ck_sleep_records_duration_non_negative
        CHECK (
            sleep_duration_hours IS NULL
            OR sleep_duration_hours >= 0
        ),
    CONSTRAINT ck_sleep_records_sleep_score_range
        CHECK (
            sleep_score IS NULL
            OR sleep_score BETWEEN 0 AND 10
        ),
    CONSTRAINT ck_sleep_records_hrv_non_negative
        CHECK (hrv_ms IS NULL OR hrv_ms >= 0),
    CONSTRAINT ck_sleep_records_resting_hr_positive
        CHECK (
            resting_heart_rate_bpm IS NULL
            OR resting_heart_rate_bpm > 0
        )
);
```

---

## 8.2 Tabela `wellbeing_records`

```sql
CREATE TABLE wellbeing_records (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    record_date DATE NOT NULL,
    mental_clarity INTEGER,
    fatigue_level INTEGER,
    concentration INTEGER,
    screen_time_minutes INTEGER,
    caffeine_mg INTEGER,
    energy_level INTEGER,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_wellbeing_records PRIMARY KEY (id),
    CONSTRAINT fk_wellbeing_records_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_wellbeing_records_user_date
        UNIQUE (user_id, record_date),
    CONSTRAINT ck_wellbeing_records_mental_clarity_range
        CHECK (
            mental_clarity IS NULL
            OR mental_clarity BETWEEN 0 AND 10
        ),
    CONSTRAINT ck_wellbeing_records_fatigue_range
        CHECK (
            fatigue_level IS NULL
            OR fatigue_level BETWEEN 0 AND 10
        ),
    CONSTRAINT ck_wellbeing_records_concentration_range
        CHECK (
            concentration IS NULL
            OR concentration BETWEEN 0 AND 10
        ),
    CONSTRAINT ck_wellbeing_records_energy_range
        CHECK (
            energy_level IS NULL
            OR energy_level BETWEEN 0 AND 10
        ),
    CONSTRAINT ck_wellbeing_records_screen_time_non_negative
        CHECK (
            screen_time_minutes IS NULL
            OR screen_time_minutes >= 0
        ),
    CONSTRAINT ck_wellbeing_records_caffeine_non_negative
        CHECK (
            caffeine_mg IS NULL
            OR caffeine_mg >= 0
        )
);
```

---

## 8.3 Tabela `body_composition_records`

```sql
CREATE TABLE body_composition_records (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    record_date DATE NOT NULL,
    weight_kg NUMERIC(6,2),
    body_fat_percentage NUMERIC(5,2),
    muscle_mass_kg NUMERIC(6,2),
    skeletal_muscle_mass_kg NUMERIC(6,2),
    lean_mass_kg NUMERIC(6,2),
    vo2_max NUMERIC(6,2),
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_body_composition_records PRIMARY KEY (id),
    CONSTRAINT fk_body_composition_records_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT ck_body_composition_weight_positive
        CHECK (weight_kg IS NULL OR weight_kg > 0),
    CONSTRAINT ck_body_composition_fat_range
        CHECK (
            body_fat_percentage IS NULL
            OR body_fat_percentage BETWEEN 0 AND 100
        ),
    CONSTRAINT ck_body_composition_muscle_non_negative
        CHECK (
            muscle_mass_kg IS NULL
            OR muscle_mass_kg >= 0
        ),
    CONSTRAINT ck_body_composition_skeletal_non_negative
        CHECK (
            skeletal_muscle_mass_kg IS NULL
            OR skeletal_muscle_mass_kg >= 0
        ),
    CONSTRAINT ck_body_composition_lean_non_negative
        CHECK (
            lean_mass_kg IS NULL
            OR lean_mass_kg >= 0
        ),
    CONSTRAINT ck_body_composition_vo2_positive
        CHECK (vo2_max IS NULL OR vo2_max > 0)
);
```

---

# 9. Módulo Workout

## 9.1 Tabela `workout_types`

```sql
CREATE TABLE workout_types (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    active BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_workout_types PRIMARY KEY (id),
    CONSTRAINT fk_workout_types_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_workout_types_user_name
        UNIQUE (user_id, name)
);
```

---

## 9.2 Tabela `workout_records`

```sql
CREATE TABLE workout_records (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    workout_type_id VARCHAR(36) NOT NULL,
    occurred_at DATETIME NOT NULL,
    duration_minutes INTEGER,
    average_heart_rate_bpm INTEGER,
    perceived_effort INTEGER,
    calories_burned INTEGER,
    distance_km NUMERIC(8,2),
    notes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_workout_records PRIMARY KEY (id),
    CONSTRAINT fk_workout_records_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_workout_records_type_id_workout_types
        FOREIGN KEY (workout_type_id) REFERENCES workout_types(id),
    CONSTRAINT ck_workout_records_duration_non_negative
        CHECK (
            duration_minutes IS NULL
            OR duration_minutes >= 0
        ),
    CONSTRAINT ck_workout_records_hr_positive
        CHECK (
            average_heart_rate_bpm IS NULL
            OR average_heart_rate_bpm > 0
        ),
    CONSTRAINT ck_workout_records_effort_range
        CHECK (
            perceived_effort IS NULL
            OR perceived_effort BETWEEN 0 AND 10
        ),
    CONSTRAINT ck_workout_records_calories_non_negative
        CHECK (
            calories_burned IS NULL
            OR calories_burned >= 0
        ),
    CONSTRAINT ck_workout_records_distance_non_negative
        CHECK (
            distance_km IS NULL
            OR distance_km >= 0
        )
);
```

---

# 10. Módulo Reading

## 10.1 Tabela `books`

```sql
CREATE TABLE books (
    id VARCHAR(26) NOT NULL,
    user_id VARCHAR(26) NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    total_pages INTEGER NOT NULL,
    isbn VARCHAR,
    publisher VARCHAR,
    edition VARCHAR,
    cover VARCHAR,
    genre VARCHAR,
    language VARCHAR,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_books PRIMARY KEY (id),
    CONSTRAINT fk_books_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT ck_books_total_pages_positive
        CHECK (total_pages > 0)
);

CREATE INDEX ix_books_user_id
ON books(user_id);
```

Regras:

- `id` persiste o TSID de `BookId` em sua representação canônica;
- `user_id` é obrigatório e referencia `users.id`;
- `title`, `author` e `total_pages` são obrigatórios;
- `isbn`, `publisher`, `edition`, `cover`, `genre` e `language` são opcionais e nullable;
- `created_at` e `updated_at` são timestamps técnicos de persistência e não pertencem ao Aggregate `Book`;
- não existem campos de status, progresso, sessão de leitura ou exclusão lógica em READ-001.

---

## 10.2 Tabela `reading_sessions`

```sql
CREATE TABLE reading_sessions (
    id VARCHAR(26) NOT NULL,
    user_id VARCHAR(26) NOT NULL,
    book_id VARCHAR(26) NOT NULL,
    start_page INTEGER NOT NULL,
    end_page INTEGER NOT NULL,
    started_at DATETIME NOT NULL,
    ended_at DATETIME NOT NULL,
    notes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_reading_sessions PRIMARY KEY (id),
    CONSTRAINT fk_reading_sessions_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_reading_sessions_book_id_books
        FOREIGN KEY (book_id) REFERENCES books(id),
    CONSTRAINT ck_reading_sessions_start_page_positive
        CHECK (start_page >= 1),
    CONSTRAINT ck_reading_sessions_end_page_not_before_start
        CHECK (end_page >= start_page),
    CONSTRAINT ck_reading_sessions_end_not_before_start_time
        CHECK (ended_at >= started_at)
);
```

Regras:

- `id` persiste o TSID de `ReadingSessionId` em sua representação canônica;
- `user_id` e `book_id` são obrigatórios e referenciam, respectivamente, `users.id` e `books.id`;
- `started_at` e `ended_at` são timestamps funcionais timezone-aware, normalizados para UTC pelo Domain;
- `notes` é opcional e nullable;
- `created_at` e `updated_at` são timestamps técnicos de persistência e não pertencem ao Aggregate;
- `pages_read` não é coluna: o valor é derivado no Domain/Application por `end_page - start_page + 1`;
- não existem índices secundários para `reading_sessions` em READ-002.

---
## 10.3 Planejamento futuro — `reading_insights`

> Esta tabela não está implementada e não integra o schema vigente de READ-001.

```sql
CREATE TABLE reading_insights (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    reading_session_id VARCHAR(36) NOT NULL,
    content TEXT NOT NULL,
    keywords TEXT,
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_reading_insights PRIMARY KEY (id),
    CONSTRAINT fk_reading_insights_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_reading_insights_session_id_reading_sessions
        FOREIGN KEY (reading_session_id)
        REFERENCES reading_sessions(id)
);
```

---

# 11. Módulo Therapy

## 11.1 Tabela `therapists`

```sql
CREATE TABLE therapists (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    specialty_or_focus VARCHAR(255),
    active BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME,

    CONSTRAINT pk_therapists PRIMARY KEY (id),
    CONSTRAINT fk_therapists_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_therapists_user_name
        UNIQUE (user_id, name)
);
```

---

## 11.2 Tabela `therapy_sessions`

```sql
CREATE TABLE therapy_sessions (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    therapist_id VARCHAR(36) NOT NULL,
    occurred_at DATETIME NOT NULL,
    session_notes TEXT,
    clarity_after_session INTEGER,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_therapy_sessions PRIMARY KEY (id),
    CONSTRAINT fk_therapy_sessions_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_therapy_sessions_therapist_id_therapists
        FOREIGN KEY (therapist_id) REFERENCES therapists(id),
    CONSTRAINT ck_therapy_sessions_clarity_range
        CHECK (
            clarity_after_session IS NULL
            OR clarity_after_session BETWEEN 0 AND 10
        )
);
```

---

# 12. Módulo Habits

## 12.1 Tabela `habits`

```sql
CREATE TABLE habits (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    frequency_type VARCHAR(30) NOT NULL,
    target_count INTEGER NOT NULL,
    attribute_code VARCHAR(10),
    active BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME,

    CONSTRAINT pk_habits PRIMARY KEY (id),
    CONSTRAINT fk_habits_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_habits_user_name
        UNIQUE (user_id, name),
    CONSTRAINT ck_habits_target_count_positive
        CHECK (target_count > 0)
);
```

---

## 12.2 Tabela `habit_records`

```sql
CREATE TABLE habit_records (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    habit_id VARCHAR(36) NOT NULL,
    record_date DATE NOT NULL,
    completed BOOLEAN NOT NULL,
    completed_count INTEGER NOT NULL,
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_habit_records PRIMARY KEY (id),
    CONSTRAINT fk_habit_records_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_habit_records_habit_id_habits
        FOREIGN KEY (habit_id) REFERENCES habits(id),
    CONSTRAINT uq_habit_records_user_habit_date
        UNIQUE (user_id, habit_id, record_date),
    CONSTRAINT ck_habit_records_completed_count_non_negative
        CHECK (completed_count >= 0)
);
```

---

## 12.3 Tabela `habit_streaks`

```sql
CREATE TABLE habit_streaks (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    habit_id VARCHAR(36) NOT NULL,
    current_streak INTEGER NOT NULL,
    longest_streak INTEGER NOT NULL,
    last_completed_date DATE,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_habit_streaks PRIMARY KEY (id),
    CONSTRAINT fk_habit_streaks_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_habit_streaks_habit_id_habits
        FOREIGN KEY (habit_id) REFERENCES habits(id),
    CONSTRAINT uq_habit_streaks_habit_id
        UNIQUE (habit_id),
    CONSTRAINT ck_habit_streaks_current_non_negative
        CHECK (current_streak >= 0),
    CONSTRAINT ck_habit_streaks_longest_non_negative
        CHECK (longest_streak >= 0)
);
```

---

# 13. Módulo Gamification

## 13.1 Tabela `experience_transactions`

```sql
CREATE TABLE experience_transactions (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    character_id VARCHAR(36) NOT NULL,
    attribute_code VARCHAR(10) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_id VARCHAR(36),
    amount INTEGER NOT NULL,
    description VARCHAR(255),
    event_id VARCHAR(36),
    occurred_at DATETIME NOT NULL,
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_experience_transactions PRIMARY KEY (id),
    CONSTRAINT fk_experience_transactions_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_experience_transactions_character_id_characters
        FOREIGN KEY (character_id) REFERENCES characters(id),
    CONSTRAINT uq_experience_transactions_event_id
        UNIQUE (event_id)
);
```

Regra:

- `event_id` pode ser nulo;
- quando preenchido, deve garantir idempotência.

---

## 13.2 Tabela `skills`

```sql
CREATE TABLE skills (
    id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    attribute_code VARCHAR(10) NOT NULL,
    active BOOLEAN NOT NULL,

    CONSTRAINT pk_skills PRIMARY KEY (id),
    CONSTRAINT uq_skills_code UNIQUE (code)
);
```

---

## 13.3 Tabela `user_skills`

```sql
CREATE TABLE user_skills (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    skill_id VARCHAR(36) NOT NULL,
    level INTEGER NOT NULL,
    total_experience INTEGER NOT NULL,
    unlocked_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_user_skills PRIMARY KEY (id),
    CONSTRAINT fk_user_skills_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_user_skills_skill_id_skills
        FOREIGN KEY (skill_id) REFERENCES skills(id),
    CONSTRAINT uq_user_skills_user_skill
        UNIQUE (user_id, skill_id),
    CONSTRAINT ck_user_skills_level_min
        CHECK (level >= 1),
    CONSTRAINT ck_user_skills_experience_non_negative
        CHECK (total_experience >= 0)
);
```

---

## 13.4 Tabela `quests`

```sql
CREATE TABLE quests (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36),
    code VARCHAR(100),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    quest_type VARCHAR(30) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_value NUMERIC(10,2) NOT NULL,
    reward_experience INTEGER NOT NULL,
    starts_at DATETIME,
    ends_at DATETIME,
    active BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_quests PRIMARY KEY (id),
    CONSTRAINT uq_quests_code UNIQUE (code),
    CONSTRAINT fk_quests_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT ck_quests_target_value_positive
        CHECK (target_value > 0),
    CONSTRAINT ck_quests_reward_experience_non_negative
        CHECK (reward_experience >= 0)
);
```

---

## 13.5 Tabela `quest_progress`

```sql
CREATE TABLE quest_progress (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    quest_id VARCHAR(36) NOT NULL,
    current_value NUMERIC(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    started_at DATETIME,
    completed_at DATETIME,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_quest_progress PRIMARY KEY (id),
    CONSTRAINT fk_quest_progress_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_quest_progress_quest_id_quests
        FOREIGN KEY (quest_id) REFERENCES quests(id),
    CONSTRAINT uq_quest_progress_user_quest
        UNIQUE (user_id, quest_id),
    CONSTRAINT ck_quest_progress_current_non_negative
        CHECK (current_value >= 0)
);
```

---

## 13.6 Tabela `achievements`

```sql
CREATE TABLE achievements (
    id VARCHAR(36) NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    rarity VARCHAR(30),
    badge_path VARCHAR(500),
    active BOOLEAN NOT NULL,

    CONSTRAINT pk_achievements PRIMARY KEY (id),
    CONSTRAINT uq_achievements_code UNIQUE (code)
);
```

---

## 13.7 Tabela `user_achievements`

```sql
CREATE TABLE user_achievements (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    achievement_id VARCHAR(36) NOT NULL,
    unlocked_at DATETIME NOT NULL,
    source_event_id VARCHAR(36),

    CONSTRAINT pk_user_achievements PRIMARY KEY (id),
    CONSTRAINT fk_user_achievements_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_user_achievements_achievement_id_achievements
        FOREIGN KEY (achievement_id) REFERENCES achievements(id),
    CONSTRAINT uq_user_achievements_user_achievement
        UNIQUE (user_id, achievement_id)
);
```

---

## 13.8 Tabela `titles`

```sql
CREATE TABLE titles (
    id VARCHAR(36) NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    minimum_level INTEGER,
    active BOOLEAN NOT NULL,

    CONSTRAINT pk_titles PRIMARY KEY (id),
    CONSTRAINT uq_titles_code UNIQUE (code),
    CONSTRAINT ck_titles_minimum_level
        CHECK (
            minimum_level IS NULL
            OR minimum_level >= 1
        )
);
```

---

## 13.9 Tabela `user_titles`

```sql
CREATE TABLE user_titles (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    title_id VARCHAR(36) NOT NULL,
    unlocked_at DATETIME NOT NULL,
    active BOOLEAN NOT NULL,

    CONSTRAINT pk_user_titles PRIMARY KEY (id),
    CONSTRAINT fk_user_titles_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_user_titles_title_id_titles
        FOREIGN KEY (title_id) REFERENCES titles(id),
    CONSTRAINT uq_user_titles_user_title
        UNIQUE (user_id, title_id)
);
```

---

# 14. Módulo Analytics

## 14.1 Tabela `analytics_snapshots`

```sql
CREATE TABLE analytics_snapshots (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    snapshot_type VARCHAR(50) NOT NULL,
    payload_json TEXT NOT NULL,
    generated_at DATETIME NOT NULL,

    CONSTRAINT pk_analytics_snapshots PRIMARY KEY (id),
    CONSTRAINT fk_analytics_snapshots_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT ck_analytics_snapshots_period
        CHECK (period_end >= period_start)
);
```

---

## 14.2 Tabela `generated_insights`

```sql
CREATE TABLE generated_insights (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    insight_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    confidence_score NUMERIC(5,2),
    source_period_start DATE,
    source_period_end DATE,
    generated_at DATETIME NOT NULL,
    dismissed_at DATETIME,

    CONSTRAINT pk_generated_insights PRIMARY KEY (id),
    CONSTRAINT fk_generated_insights_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT ck_generated_insights_confidence_range
        CHECK (
            confidence_score IS NULL
            OR confidence_score BETWEEN 0 AND 100
        ),
    CONSTRAINT ck_generated_insights_period
        CHECK (
            source_period_end IS NULL
            OR source_period_start IS NULL
            OR source_period_end >= source_period_start
        )
);
```

---

## 14.3 Tabela `dashboard_cache`

```sql
CREATE TABLE dashboard_cache (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    cache_key VARCHAR(150) NOT NULL,
    payload_json TEXT NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME NOT NULL,

    CONSTRAINT pk_dashboard_cache PRIMARY KEY (id),
    CONSTRAINT fk_dashboard_cache_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_dashboard_cache_user_key
        UNIQUE (user_id, cache_key)
);
```

---

# 15. Módulo Reports

## 15.1 Tabela `report_exports`

```sql
CREATE TABLE report_exports (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    status VARCHAR(30) NOT NULL,
    requested_at DATETIME NOT NULL,
    completed_at DATETIME,
    expires_at DATETIME,

    CONSTRAINT pk_report_exports PRIMARY KEY (id),
    CONSTRAINT fk_report_exports_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

# 16. Módulo Administration

## 16.1 Tabela `audit_logs`

```sql
CREATE TABLE audit_logs (
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id VARCHAR(36),
    metadata_json TEXT,
    occurred_at DATETIME NOT NULL,

    CONSTRAINT pk_audit_logs PRIMARY KEY (id),
    CONSTRAINT fk_audit_logs_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 16.2 Tabela `event_store`

```sql
CREATE TABLE event_store (
    id VARCHAR(36) NOT NULL,
    event_type VARCHAR(150) NOT NULL,
    aggregate_type VARCHAR(100),
    aggregate_id VARCHAR(36),
    user_id VARCHAR(36),
    payload_json TEXT NOT NULL,
    occurred_at DATETIME NOT NULL,
    published_at DATETIME,
    status VARCHAR(30) NOT NULL,
    attempts INTEGER NOT NULL,
    error_message TEXT,

    CONSTRAINT pk_event_store PRIMARY KEY (id),
    CONSTRAINT fk_event_store_user_id_users
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT ck_event_store_attempts_non_negative
        CHECK (attempts >= 0)
);
```

---

## 16.3 Tabela `processed_events`

```sql
CREATE TABLE processed_events (
    id VARCHAR(36) NOT NULL,
    event_id VARCHAR(36) NOT NULL,
    handler_name VARCHAR(255) NOT NULL,
    processed_at DATETIME NOT NULL,
    status VARCHAR(30) NOT NULL,
    error_message TEXT,

    CONSTRAINT pk_processed_events PRIMARY KEY (id),
    CONSTRAINT fk_processed_events_event_id_event_store
        FOREIGN KEY (event_id) REFERENCES event_store(id),
    CONSTRAINT uq_processed_events_event_handler
        UNIQUE (event_id, handler_name)
);
```

---

## 16.4 Tabela `application_settings`

```sql
CREATE TABLE application_settings (
    id VARCHAR(36) NOT NULL,
    setting_key VARCHAR(150) NOT NULL,
    setting_value TEXT,
    value_type VARCHAR(30) NOT NULL,
    updated_at DATETIME NOT NULL,

    CONSTRAINT pk_application_settings PRIMARY KEY (id),
    CONSTRAINT uq_application_settings_key
        UNIQUE (setting_key)
);
```

---

# 17. Índices Oficiais

Os índices abaixo devem ser criados por migrations específicas e permanecer alinhados ao `INDEXES.md`.

```sql
CREATE INDEX ix_user_sessions_user_id
ON user_sessions(user_id);

CREATE INDEX ix_password_reset_tokens_user_id
ON password_reset_tokens(user_id);

CREATE INDEX ix_character_history_character_id_occurred_at
ON character_history(character_id, occurred_at);

CREATE INDEX ix_sleep_records_user_id_record_date
ON sleep_records(user_id, record_date);

CREATE INDEX ix_wellbeing_records_user_id_record_date
ON wellbeing_records(user_id, record_date);

CREATE INDEX ix_body_composition_user_id_record_date
ON body_composition_records(user_id, record_date);

CREATE INDEX ix_workout_records_user_id_occurred_at
ON workout_records(user_id, occurred_at);

CREATE INDEX ix_workout_records_user_id_type_id
ON workout_records(user_id, workout_type_id);

CREATE INDEX ix_therapy_sessions_user_id_occurred_at
ON therapy_sessions(user_id, occurred_at);

CREATE INDEX ix_therapy_sessions_user_id_therapist_id
ON therapy_sessions(user_id, therapist_id);

CREATE INDEX ix_habit_records_user_id_record_date
ON habit_records(user_id, record_date);

CREATE INDEX ix_habit_records_habit_id_record_date
ON habit_records(habit_id, record_date);

CREATE INDEX ix_experience_transactions_character_id_occurred_at
ON experience_transactions(character_id, occurred_at);

CREATE INDEX ix_experience_transactions_character_id_attribute_code
ON experience_transactions(character_id, attribute_code);

CREATE INDEX ix_quest_progress_user_id_status
ON quest_progress(user_id, status);

CREATE INDEX ix_user_achievements_user_id_unlocked_at
ON user_achievements(user_id, unlocked_at);

CREATE INDEX ix_analytics_snapshots_user_id_period_start
ON analytics_snapshots(user_id, period_start);

CREATE INDEX ix_generated_insights_user_id_generated_at
ON generated_insights(user_id, generated_at);

CREATE INDEX ix_event_store_user_id_occurred_at
ON event_store(user_id, occurred_at);

CREATE INDEX ix_event_store_event_type
ON event_store(event_type);

CREATE INDEX ix_event_store_status
ON event_store(status);

CREATE INDEX ix_audit_logs_user_id_occurred_at
ON audit_logs(user_id, occurred_at);

CREATE INDEX ix_audit_logs_entity_type_entity_id
ON audit_logs(entity_type, entity_id);

CREATE INDEX ix_report_exports_user_id_requested_at
ON report_exports(user_id, requested_at);
```

---

# 18. Regras Multi-Tenant

Toda operação deve garantir que entidades relacionadas pertençam ao mesmo usuário.

Exemplo:

```text
workout_records.user_id
```

deve corresponder ao:

```text
workout_types.user_id
```

Essa regra deve ser validada pela Application e pelo Repository.

O banco, isoladamente, não cobre todos os casos de ownership com Foreign Keys simples.

---

# 19. Regras de Nulabilidade

Uma coluna deve ser `NOT NULL` quando:

- fizer parte da identidade funcional;
- for necessária para reconstruir o Aggregate;
- representar dado obrigatório do caso de uso;
- possuir valor sempre conhecido.

Uma coluna deve permitir `NULL` quando:

- o dado for opcional;
- depender de processamento futuro;
- possuir significado real de ausência;
- ainda não estiver disponível.

Nunca utilizar `NULL` para representar string vazia, zero ou falso.

---

# 20. Defaults

Defaults de negócio devem preferencialmente ser definidos no Domain.

Defaults técnicos podem existir no banco.

Exemplos permitidos:

```text
active = true
attempts = 0
global_level = 1
total_experience = 0
```

A migration deve avaliar se o `server_default` é permanente ou temporário.

---

# 21. Regras de Soft Delete

Tabelas com `deleted_at`:

- `users`;
- `books`;
- `therapists`;
- `habits`.

Outras tabelas poderão adotar soft delete mediante requisito.

Consultas normais devem filtrar:

```sql
deleted_at IS NULL
```

---

# 22. Regras de Cascade

Preferência:

```text
ON DELETE RESTRICT
```

para dados históricos.

Pode ser utilizado:

```text
ON DELETE CASCADE
```

apenas em estruturas internas sem valor próprio, como:

- sessões revogáveis;
- tokens;
- cache;
- preferências;
- dados temporários.

---

# 23. Ordem de Criação do Schema

A ordem oficial deve respeitar dependências:

```text
1. users
2. user_preferences
3. user_sessions
4. password_reset_tokens
5. characters
6. character_attributes
7. character_history
8. workout_types
9. books
10. therapists
11. habits
12. skills
13. quests
14. achievements
15. titles
16. sleep_records
17. wellbeing_records
18. body_composition_records
19. workout_records
20. reading_sessions
21. reading_insights (futuro)
22. therapy_sessions
23. habit_records
24. habit_streaks
25. experience_transactions
26. user_skills
27. quest_progress
28. user_achievements
29. user_titles
30. analytics_snapshots
31. generated_insights
32. dashboard_cache
33. report_exports
34. audit_logs
35. event_store
36. processed_events
37. application_settings
```

---

# 24. SQLAlchemy Models

Cada tabela deve possuir Model próprio na Infrastructure.

Exemplo:

```text
modules/character/infrastructure/models/character_model.py
```

Exemplo conceitual:

```python
class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    global_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    total_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
```

---

# 25. Naming Convention SQLAlchemy

O `MetaData` deve utilizar convenção oficial:

```python
NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": (
        "fk_%(table_name)s_%(column_0_N_name)s_"
        "%(referred_table_name)s"
    ),
    "pk": "pk_%(table_name)s",
}
```

Isso garante nomes determinísticos em migrations.

---

# 26. Compatibilidade SQLite

O schema deve considerar:

- Foreign Keys habilitadas;
- batch mode em alterações;
- `BOOLEAN` persistido conforme dialect;
- `DATETIME` tratado pelo ORM;
- JSON armazenado como `TEXT`;
- UUID armazenado como `VARCHAR(36)`;
- ausência de ENUM nativo;
- ausência de JSONB;
- ausência de ARRAY.

---

# 27. Compatibilidade PostgreSQL

A migração futura poderá introduzir:

- UUID nativo;
- JSONB;
- índices parciais;
- Full Text Search;
- constraints mais avançadas;
- materialized views;
- tipos específicos.

Essas mudanças devem permanecer na Infrastructure e migrations.

---

# 28. Testes do Schema

Os testes devem validar:

- criação integral do banco;
- Foreign Keys;
- UNIQUE;
- CHECK;
- nullable;
- defaults;
- índices;
- Multi-Tenant;
- rollback;
- downgrade;
- compatibilidade com migrations.

---

# 29. Teste de Integridade

Exemplos de cenários obrigatórios:

```text
Não permitir dois usuários com mesmo e-mail.
Não permitir dois Characters para o mesmo usuário.
Não permitir dois registros de sono no mesmo dia para o mesmo usuário.
Não permitir XP negativa quando a regra não autorizar.
Não permitir pontuação fora de 0 a 10.
Não permitir Relationship inválido.
```

---

# 30. Como o Gemini deve Utilizar este Documento

Antes de criar ou alterar Model, tabela ou migration, o agente deve verificar:

1. A tabela já está definida?
2. A coluna já existe?
3. O nome segue a convenção?
4. O tipo é portátil?
5. A nulabilidade está correta?
6. O campo exige `user_id`?
7. A Foreign Key está nomeada?
8. A Constraint está nomeada?
9. Há índice necessário?
10. A mudança está no ERD?
11. A migration foi criada?
12. O Repository e Mapper serão atualizados?
13. Os testes foram previstos?
14. A mudança preserva SQLite e PostgreSQL?
15. A documentação está sincronizada?

---

# 31. Checklist de Implementação

- [ ] Tabela vinculada ao módulo correto.
- [ ] Nome oficial aplicado.
- [ ] Primary Key definida.
- [ ] Foreign Keys definidas.
- [ ] `user_id` aplicado quando necessário.
- [ ] Constraints nomeadas.
- [ ] Índices avaliados.
- [ ] Nulabilidade revisada.
- [ ] Tipos portáveis utilizados.
- [ ] Soft delete avaliado.
- [ ] Cascade avaliado.
- [ ] Migration criada.
- [ ] Model SQLAlchemy criado.
- [ ] Persistence Mapper criado.
- [ ] Repository atualizado.
- [ ] Testes de integração criados.
- [ ] ERD atualizado.
- [ ] INDEXES atualizado.
- [ ] MIGRATIONS atualizado.
- [ ] Documentação sincronizada.

---

# 32. Critérios de Aceite

Este documento será considerado atendido quando:

- todas as tabelas iniciais estiverem especificadas;
- todas as colunas possuírem tipo e nulabilidade;
- todas as PKs e FKs estiverem documentadas;
- todas as Constraints críticas estiverem definidas;
- os índices principais estiverem listados;
- o isolamento Multi-Tenant estiver refletido;
- o schema for compatível com SQLAlchemy e SQLite;
- a evolução para PostgreSQL permanecer viável;
- os Models puderem ser implementados sem ambiguidade.

---

# 33. Definition of Done

Uma alteração de schema só estará concluída quando:

- [ ] O schema estiver atualizado.
- [ ] O ERD estiver atualizado.
- [ ] A migration existir.
- [ ] O Model ORM estiver atualizado.
- [ ] O Mapper estiver atualizado.
- [ ] O Repository estiver atualizado.
- [ ] Constraints e índices estiverem corretos.
- [ ] Multi-Tenant estiver protegido.
- [ ] Testes passarem.
- [ ] A documentação estiver sincronizada.

---

# 34. Declaração Final

O schema do LifeOS deve representar a persistência de forma clara, previsível e rastreável.

Ele não define o comportamento do domínio, mas deve proteger sua integridade estrutural.

Toda tabela, coluna, Constraint e índice deve existir por uma razão explícita e documentada.

A evolução do schema deve permanecer controlada por migrations, alinhada ao ERD e compatível com a arquitetura modular e Multi-Tenant da plataforma.
