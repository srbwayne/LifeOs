# HAB-003 — Technical Plan — Current Streak

| Field | Value |
|---|---|
| Feature | HAB-003 — Sequência (Streak) |
| Requirement | RF-HAB-005 — Controle de Streaks |
| Product Contract | APPROVED / FROZEN |
| Architecture | APPROVED / FROZEN |
| Technical Plan Decision | HAB-003-TP-DEC-001 — APPROVED |
| Technical Plan | APPROVED / FROZEN |
| Human Review | APPROVED |
| Decision Date | 2026-09-15 |
| Implementation at Technical Plan approval | NOT AUTHORIZED |
| Canonical decision baseline | `78bec6221ceabe4d345d2758e18cf08037b08b4c` |
| Alembic revision | `0011` |
| Technical Plan Amendment | HAB-003-TP-AMEND-DEC-001 — APPROVED |
| Amendment Date | 2026-09-16 |

This is the canonical durable form of `HAB-003-TP-001R2 — Final Technical
Plan`. It records the frozen engineering plan and does not authorize
implementation.

## 1. Product and architecture boundaries

HAB-003 calculates the current calendar-consecutive streak from existing
`HabitCompletion` facts. Evaluation uses an explicit civil date `D`: if `D` is
completed, the chain ends at `D`; otherwise, if `D-1` is completed, it ends at
`D-1`; otherwise the current streak is `0`. Facts after `D` are ignored.

An inactive Habit is not applicable and returns `None` at the application
boundary. Retroactive completion changes recalculate from facts.
`HabitCompletion` is the sole functional source of truth. No durable streak
state is introduced. HAB-004 frequency, HAB-005 statistics and longest streak,
GAME, XP, Progression, Logos, Noema/AI, Analytics, and event dispatch are
outside this plan.

The evaluation date is an explicit application-query input. No
`DateProvider`, `Clock`, `date.today()`, UTC-derived date, server-local date,
or implicit timezone inference is permitted.

## 2. Domain calculator

```text
app/habits/domain/services/__init__.py
app/habits/domain/services/current_habit_streak.py
```

```python
CurrentHabitStreakCalculator

def calculate(
    self,
    evaluation_date: date,
    completion_dates: Collection[date],
) -> int:
    ...
```

Caller ordering is not required. The calculator normalizes defensively,
collapses duplicates, ignores dates greater than `evaluation_date`, and is
pure. It uses `O(n)` time and `O(n)` auxiliary space, with no I/O, persistence,
clock, or date-provider dependency. Repository descending order is not a
calculator correctness precondition.

## 3. Application query and DTO

Query path:

```text
app/habits/application/queries/get_habit_streak.py
```

```python
@dataclass(frozen=True)
class GetHabitStreakQuery:
    owner_id: UserId
    habit_id: HabitId
    evaluation_date: date
```

Handler: `GetHabitStreakQueryHandler`.

Dependencies:

```text
IHabitRepository
IHabitCompletionReadRepository
CurrentHabitStreakCalculator
```

Operation order is fixed:

```text
1. owner-scoped Habit lookup
2. nonexistent/foreign -> HabitNotFoundError
3. inactive -> DTO(current_streak=None), no completion query
4. active -> exactly one completion-date projection
5. invoke calculator
6. return HabitStreakDTO
```

DTO path:

```text
app/habits/application/dtos/habit_streak_dto.py
```

```python
@dataclass(frozen=True)
class HabitStreakDTO:
    habit_id: str
    current_streak: int | None
    evaluation_date: date
```

`0` means applicable with no current chain. `None` means not applicable because
the Habit is inactive.

## 4. Completion read port and adapter

Port path:

```text
app/habits/application/ports/habit_completion_read_repository.py
```

```python
def list_record_dates_by_owner_and_habit_until(
    self,
    owner_id: UserId,
    habit_id: HabitId,
    evaluation_date: date,
) -> tuple[date, ...]:
    ...
```

Guarantees:

```text
user_id == owner_id
habit_id == habit_id
record_date <= evaluation_date
ORDER BY record_date DESC
```

The projection contains `record_date` only. Adapter path:

```text
app/habits/infrastructure/persistence/repositories/habit_completion_read_repository.py
```

The adapter uses the equivalent of:

```python
select(HabitCompletionModel.record_date).where(
    HabitCompletionModel.user_id == owner,
    HabitCompletionModel.habit_id == habit,
    HabitCompletionModel.record_date <= evaluation_date,
).order_by(HabitCompletionModel.record_date.desc())
```

An active request performs one owner-scoped Habit lookup and one completion-date
projection. An inactive request performs zero completion projections. N+1 is
forbidden.

## 5. HTTP, authentication, and response

Route:

```http
GET /habits/{habit_id}/streak?evaluation_date=YYYY-MM-DD
```

The endpoint receives:

```python
user_id: UserId = Depends(get_current_user_id)
```

The authenticated `user_id` becomes `owner_id`; owner identity cannot come from
the path, query, body, or arbitrary caller input. `evaluation_date` is required,
has no default, is a civil `date`, and is never derived from today.

HTTP behavior:

```text
Unauthenticated request -> 401
Malformed HabitId -> 422
Missing evaluation_date -> 422
Malformed evaluation_date -> 422
Nonexistent Habit -> 404
Foreign-owner Habit -> 404
Inactive Habit -> 200 / current_streak=null
```

Schema path:

```text
app/habits/presentation/api/fastapi/schemas.py
```

```python
class HabitStreakResponse(BaseModel):
    habit_id: str
    current_streak: int | None
    evaluation_date: date
```

Foreign and nonexistent Habits remain indistinguishable. The response echoes
the evaluation date and has no additional applicability field.

## 6. Dependencies and router

Dependency path:

```text
app/habits/dependencies.py
```

Provider: `get_get_habit_streak_handler`.

It depends on `get_habit_repository` and
`get_habit_completion_read_repository`, and constructs a stateless
`CurrentHabitStreakCalculator`. No global streak service, `Clock`, or
`DateProvider` is permitted.

Router path:

```text
app/habits/presentation/api/fastapi/routers.py
```

The endpoint uses the existing `_parse_habit_id`, the authenticated dependency,
the required `evaluation_date`, and the injected handler.

## 7. Database and migration boundary

Alembic revision remains `0011`. Existing schema evidence is:

```text
UNIQUE(user_id, habit_id, record_date)
ix_habit_completions_user_record_habit
(user_id, record_date, habit_id)
```

No new migration, migration `0012`, new V1 index, durable streak persistence,
or operational cutover is planned. Existing migrations may be validated only
against a dedicated disposable HAB-003 SQLite database with an explicitly set
`LIFEOS_DATABASE_URL`. Operational database access and operational `lifeos.db`
migration are forbidden.

## 8. Query-plan validation

Disposable validation data contains exactly 10,000 completion rows:

```text
U1: 9,500 rows (H1 target: 8,000; H2: 1,000; H3: 500)
U2/H4 foreign: 500 rows
H1: 7,998 dates < D, 1 date == D, 1 date > D
```

Query:

```sql
SELECT record_date
FROM habit_completions
WHERE user_id = ?
  AND habit_id = ?
  AND record_date <= ?
ORDER BY record_date DESC;
```

PASS requires `SEARCH` or equivalent indexed access and no avoidable
`SCAN habit_completions`. The existing unique auto-index or named index is
acceptable when it demonstrates that access. Failure is a hard stop requiring
an index decision gate; no index or migration remediation is automatic.

## 9. Implementation allowlist

Production — exactly nine paths:

```text
app/habits/domain/services/__init__.py
app/habits/domain/services/current_habit_streak.py
app/habits/application/dtos/habit_streak_dto.py
app/habits/application/queries/get_habit_streak.py
app/habits/application/ports/habit_completion_read_repository.py
app/habits/infrastructure/persistence/repositories/habit_completion_read_repository.py
app/habits/presentation/api/fastapi/schemas.py
app/habits/presentation/api/fastapi/routers.py
app/habits/dependencies.py
```

Tests — exactly five paths:

```text
tests/habits/domain/test_habit_streak.py
tests/habits/application/test_habit_streak_query.py
tests/habits/integration/test_habit_streak_read_repository.py
tests/habits/api/test_habit_api.py
tests/habits/application/test_read_queries.py
```

The legacy `tests/habits/application/test_read_queries.py` path is included
for compatibility because its `CompletionReadRepositoryFake` is passed to
`ListCompletionsQueryHandler` and structurally satisfies
`IHabitCompletionReadRepository`. When the Protocol gains
`list_record_dates_by_owner_and_habit_until(...)`, that fake must gain the
same method. The permitted change is compatibility-only: existing
ListCompletions tests and behavior are not rewritten, and dedicated HAB-003
application behavior remains in
`tests/habits/application/test_habit_streak_query.py`.

Production paths: 9. Test paths: 5. Total implementation paths: 14.
Migration, governance, and frontend paths: none. No fifteenth path is
authorized. Unrelated paths require a new review decision.

## 10. Test plan

Domain tests cover chains at `D`, `D-1`, and gaps; empty input; future facts;
unordered and duplicate dates; past and future evaluation dates; and purity.

Application tests cover owner scoping, active/inactive behavior, not-found
behavior, exact date forwarding, one active projection, and zero inactive
projections.

Integration tests cover owner/Habit isolation, `record_date <= D`, descending
ordering, date-only projection, and future-fact exclusion.

API tests cover unauthenticated `401`, authenticated success, zero streak,
inactive `200/null`, date echoing, missing/malformed dates, past/future dates,
malformed IDs, nonexistent Habits, and foreign Habits.

## 11. Validation and slicing

The future implementation gate runs focused HAB-003 tests, complete Habits
regression, `python -m pip check`, Ruff, Ruff format check, Mypy, application
import, full pytest, the DeprecationWarning gate, coverage, guarded disposable
Alembic `upgrade head`/`current`, deterministic query-plan validation, and
`git diff --check`.

The blocked `HAB-003-IA-001` local readiness evidence used CPython 3.13.5;
the rerun must use actual CPython 3.11.x. This is a pre-flight evidence gap,
not a Product Contract, Architecture, or implementation semantic change.
Its disposable Alembic validation, 10,000-row seed, and `EXPLAIN QUERY PLAN`
were not executed because the IA gate correctly stopped at the allowlist
blocker. `HAB-003-IA-001R` must complete that already-frozen validation and
cleanup before implementation authorization can be recommended.

The disposable Alembic sequence must create a non-existing dedicated database,
explicitly set `LIFEOS_DATABASE_URL` before both commands, refuse reuse or
overwrite, refuse `lifeos.db`, clean up the database, and unset the temporary
variable. No unqualified Alembic command is permitted.

At Technical Plan approval, this was one bounded implementation slice and
implementation was `NOT AUTHORIZED`; the next gate at that historical point was
`HAB-003-IA-001R — IMPLEMENTATION AUTHORIZATION / PRE-FLIGHT REVIEW RERUN`.

## 12. Implementation outcome

Human Implementation Authorization: `HAB-003-IA-DEC-001 — APPROVED`.

Implementation: CANONICAL.

Canonical SHA: `ca75af380e12515d1cdd1ebf74d29ca207cd9647`.

PR: `#86` (squash merge; parent
`83979a835d5fc7f8fa08cd9e3afef7119361c391`).

Canonical paths: 9 production + 5 tests = 14.

Migration: NONE. New index: NONE. Persisted streak: NO. Alembic: `0011`.

Main CI: `35171823950 — 3/3 SUCCESS`.

Implementation review identified and remediated representable civil-date lower
bound handling for `evaluation_date == date.min`, without changing the frozen
Product Contract or Architecture. Final implementation review classification:
BLOCKER 0, MAJOR 0, MINOR 0.

Source implementation is complete and canonical. Operational activation and
runtime verification are outside this Technical Plan implementation closure and
remain unverified.
