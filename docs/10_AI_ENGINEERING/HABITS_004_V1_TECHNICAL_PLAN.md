# HABITS-004 — Habits V1 Technical Plan

**Status:** TECHNICAL PLAN APPROVED — IMPLEMENTATION NOT AUTHORIZED

**Date:** 2026-09-12

**Canonical baseline:** `c49667388d2c0328e4017f8c9739cabaafa0dad0`

This plan freezes the technical shape for HAB-001 and HAB-002. It authorizes no source change, migration creation, migration execution, database access, runtime change, progression, Logos integration, or Noema/AI integration.

## 1. Architecture and aggregates

Use independent aggregate roots (Option B): `Habit` and `HabitCompletion`. Completion history is unbounded, daily writes must not load a Habit history, completion correction has an independent lifecycle, and future streak/frequency/statistics queries can read completion facts directly. A command validates owner and Habit membership in one transaction; the Habit aggregate does not contain a collection of completions.

`Habit` contains `HabitId`, `UserId owner_id`, normalized `name`, optional normalized `description`, and `active`. `created_at` and `updated_at` are persistence timestamps, not aggregate business state. It is created active and supports deactivate/reactivate only. Rename, hard delete, and soft delete are outside V1.

`HabitCompletion` contains `HabitCompletionId`, `UserId owner_id`, `HabitId habit_id`, and explicit civil `record_date`. `created_at` is a persistence technical timestamp, not aggregate business state. It is binary by row existence. There are no persisted completed, quantity, duration, target, timezone, streak, frequency, or statistics fields.

## 2. Normalization and identity

Habit names are trimmed, blank names are rejected, case is preserved, and exact stored-string uniqueness is enforced per owner. No case-insensitive rule is introduced. The database unique constraint is authoritative; an application lookup may provide a friendly conflict before the database check.

Descriptions accept `str | None`, are trimmed, and normalize blank text to `None`, following existing optional-string behavior. No business length limit is invented. Persistence uses nullable `Text`.

`HabitCompletionId` is a typed TSID surrogate primary key, matching existing LifeOS identifiers. The business key remains unique on `(user_id, habit_id, record_date)`.

## 3. Persistence design for migration 0011

### `habits`

| Column | Shape |
|---|---|
| `id` | `VARCHAR(26) NOT NULL`, primary key |
| `user_id` | `VARCHAR(26) NOT NULL`, FK `users.id`, `ON DELETE RESTRICT` |
| `name` | `TEXT NOT NULL`; no business length limit or length validation |
| `description` | `TEXT NULL` |
| `active` | Boolean, `NOT NULL` |
| `created_at` | technical `DATETIME NOT NULL` |
| `updated_at` | technical `DATETIME NOT NULL` |

Constraints are primary key `(id)`, unique `(user_id, id)` for owner-safe child references, and unique `(user_id, name)` for exact owner/name uniqueness. No active-filter index is created. `GET /habits` returns active and inactive definitions ordered by `name ASC, id ASC`; the unique owner/name key supplies the principal owner/name index.

### `habit_completions`

| Column | Shape |
|---|---|
| `id` | `VARCHAR(26) NOT NULL`, primary key |
| `user_id` | `VARCHAR(26) NOT NULL`, FK `users.id`, `ON DELETE RESTRICT` |
| `habit_id` | `VARCHAR(26) NOT NULL` |
| `record_date` | SQL `DATE NOT NULL` |
| `created_at` | technical `DATETIME NOT NULL` |

Add composite FK `(user_id, habit_id) -> habits(user_id, id)` with `ON DELETE RESTRICT` and unique `(user_id, habit_id, record_date)`. Add `(user_id, record_date, habit_id)` for checklist lookup. The unique business key already supports owner+Habit+date history access; no redundant index is added. History ordering is `record_date DESC, id DESC`; if query plans later demonstrate a separate ordering index is needed, that is an infrastructure review, not a speculative 0011 index.

There is no backfill. Downgrade drops completion indexes, drops `habit_completions`, drops Habit indexes, then drops `habits`, respecting FK dependency order. Migration tests use only disposable databases.

## 4. Mark completion algorithm and concurrency

The correctness boundary is the database unique key `(user_id, habit_id, record_date)`, not the timing of an application pre-check. Canonical infrastructure contains concrete `SqlAlchemyUnitOfWork.acquire_write_intent()` behavior that issues `BEGIN IMMEDIATE` for SQLite, while `IUnitOfWork` does not expose that method. Habits handlers must not downcast or couple to the concrete UoW merely to call it. Slice 4 must establish whether ordinary uniqueness plus conflict recovery is sufficient; exposing write intent through an application abstraction would require a separate reviewed decision. No new locking primitive is introduced. The command executes in this order:

1. Resolve the Habit by exact owner and `habit_id`.
2. Treat missing and foreign resources as the same not-found result.
3. Query an existing completion for owner, Habit, and `record_date`.
4. If it exists, return it idempotently with HTTP `200`, even when the Habit is now inactive.
5. If it does not exist, check `Habit.active`.
6. If inactive, raise `InactiveHabitError` mapped to `409`.
7. If active, attempt the insert.
8. Return the new completion with HTTP `201`.
9. If a uniqueness race occurs, detect the SQLAlchemy uniqueness failure, rollback the failed transaction or use an explicitly reviewed savepoint, then reload the winner through a valid transaction/session and return it with HTTP `200`. A failed flush/commit leaves the transaction unusable until recovery; querying immediately without rollback is invalid.

The first and repeated responses use the same completion representation. The existing SQLite write-intent capability is concrete infrastructure only and is not part of the application protocol. If Habits later needs to reuse it, that must be proven by infrastructure tests and exposed through an explicitly reviewed application abstraction. Unique-constraint enforcement plus conflict recovery is mandatory.

## 5. Unmark and transactions

Use `POST /habits/{habit_id}/completions` with body `{ "record_date": "YYYY-MM-DD" }`. The response is `HabitCompletionResponse` with `id`, `habit_id`, and `record_date`; it does not expose `owner_id` or require `created_at`. First persistence returns `201`; an existing completion, concurrent winner resolution, or inactive Habit with an existing completion returns `200`; inactive without an existing completion returns `409`; malformed Habit ID or date returns `422`; missing/foreign Habit returns `404`.

Use `DELETE /habits/{habit_id}/completions/{record_date}` for correction. An existing owner-scoped completion is removed and returns `204`; an absent or foreign completion returns `404`. Repeating the delete after success returns `404`. This is correction semantics, without an audit row or soft delete.

Each write command—Habit creation, deactivate, reactivate, mark, and unmark—uses one local transaction through the existing `SqlAlchemyUnitOfWork`/SQLAlchemy session pattern. `IUnitOfWork` remains the application protocol and does not expose `acquire_write_intent`; no handler may downcast to the concrete UoW. No external calls, domain events, progression writes, Logos calls, or Noema calls occur.

## 6. Habit API

```text
POST   /habits                         -> 201
GET    /habits                         -> 200 (active and inactive, name ASC, id ASC)
GET    /habits/{habit_id}              -> 200
POST   /habits/{habit_id}/deactivate   -> 200
POST   /habits/{habit_id}/reactivate   -> 200
POST   /habits/{habit_id}/completions  -> 201 first / 200 repeat or race
DELETE /habits/{habit_id}/completions/{record_date} -> 204 / 404 repeat
```

Ownership is derived exclusively from authentication. No PATCH rename and no Habit DELETE exist. Malformed TSIDs map to `422`; missing and foreign resources are indistinguishable `404`; duplicate owner/name maps to `409`; unauthenticated requests map to `401`.

## 7. Checklist API

```text
GET /habits/checklist?record_date=YYYY-MM-DD -> 200
```

The static `/checklist` route is registered before `/{habit_id}`. It returns the owner’s **current active Habit set** projected against the explicitly supplied civil `record_date`. Each item contains at least Habit ID, name, description, and completion state derived from completion-row existence. A read-model `completed` boolean is permitted, but is never persisted in the domain or database.

V1 does not retain active-period history. A checklist for an old date therefore means current active Habits projected against that date; it does not reconstruct which Habits were active on that historical date. Historical completions for inactive Habits remain available from completion history.

## 8. Completion history API

```text
GET /habits/{habit_id}/completions?page=1&size=20 -> 200
```

The endpoint is owner-scoped. A missing or foreign Habit returns `404`; an existing owner Habit with zero completions returns `200` with an empty page. It uses `page >= 1`, `1 <= size <= 100`, defaults page `1` and size `20`, and returns current stored completion facts only. Ordering is `record_date DESC, id DESC`. There is no date-range filter, aggregate statistic, audit history, or analytics output in V1.

Any structurally valid civil `DATE` is accepted. No UTC-derived owner date, server-timezone future-date rejection, or timezone rule is introduced.

## 9. Narrow repository ports

The application ports remain focused and HTTP-neutral:

```text
IHabitRepository:
  save(habit)
  get_by_id_and_owner(habit_id, owner_id)
  get_by_owner_and_name(owner_id, name)

IHabitCompletionRepository:
  save(completion)
  get_by_owner_habit_date(owner_id, habit_id, record_date)
  delete(completion)

IHabitReadRepository:
  list_by_owner(owner_id)
  get_checklist_by_owner_and_record_date(owner_id, record_date)

IHabitCompletionReadRepository:
  list_by_owner_and_habit(owner_id, habit_id, page, size)
```

Checklist and history use projection-oriented read repositories where useful. No generic repository base is introduced.

## 10. Errors and composition

Use `InvalidHabitNameError` → `422`, `HabitNotFoundError` → `404`, `HabitAlreadyExistsError` (or the existing conflict equivalent) → `409`, `InactiveHabitError` → `409`, and `HabitCompletionNotFoundError` → `404` where required by the unmark/history application contract. Foreign-owner and absent resources share the same observable not-found path.

Future integration points are the new `app/habits/` module and `app/app_factory.py` for router and exception registration. `app/composition_root.py` remains UNCHANGED; Habits follows the Therapy module-local `dependencies.py` composition pattern and consumes the existing `get_current_user_id`. These files are not modified by this plan.

## 11. Migration and test strategy

The conceptual migration is `0011_create_habits_v1_schema.py`, revision `0011`, down revision `0010`, with the two tables and constraints above. It is not created or executed by this plan.

Tests must cover domain normalization/lifecycle/identity; application ownership, duplicate names, lifecycle, first/repeated mark, inactive-new and inactive-existing behavior, unmark and transaction boundaries; persistence TSID/DATE round trips, unique keys, owner-safe FK, RESTRICT, ordering and removal isolation; API authentication, malformed IDs, owner isolation, lifecycle, checklist, `201` first mark, `200` repeated mark, `204` unmark, repeated-delete `404`, and history pagination; and disposable migration upgrade/schema/downgrade checks.

Concurrency tests must use two real database sessions attempting the same owner/Habit/date. They must prove exactly one row, one creation result, and one response resolving to the same persisted completion. Correctness may not depend on pre-check timing.

## 12. Implementation slicing (not authorized)

1. Domain, typed IDs, errors, ports, and domain tests.
2. Migration 0011, persistence models/mappers/repositories, and persistence tests.
3. HAB-001 create/list/get/deactivate/reactivate and tests.
4. HAB-002 mark/unmark, database-backed idempotency, concurrency and API tests.
5. Checklist projection and completion history with pagination/order.
6. Full regression and governance closeout.

Migration belongs with persistence in Slice 2. No slice is authorized by this document.

## 13. File plan

```text
app/habits/__init__.py                                      NEW
app/habits/dependencies.py                                  NEW
app/habits/domain/aggregates/habit.py                       NEW
app/habits/domain/aggregates/habit_completion.py            NEW
app/habits/domain/errors/habit_errors.py                    NEW
app/habits/domain/ports/habit_repository.py                 NEW
app/habits/domain/ports/habit_completion_repository.py      NEW
app/habits/domain/value_objects/habit_id.py                 NEW
app/habits/domain/value_objects/habit_completion_id.py      NEW
app/habits/application/commands/create_habit.py             NEW
app/habits/application/commands/deactivate_habit.py         NEW
app/habits/application/commands/reactivate_habit.py         NEW
app/habits/application/commands/mark_completion.py          NEW
app/habits/application/commands/unmark_completion.py        NEW
app/habits/application/queries/list_habits.py               NEW
app/habits/application/queries/get_habit.py                 NEW
app/habits/application/queries/get_checklist.py             NEW
app/habits/application/queries/list_completions.py          NEW
app/habits/application/dtos/habit_dto.py                    NEW
app/habits/application/dtos/habit_completion_dto.py         NEW
app/habits/application/ports/habit_read_repository.py       NEW
app/habits/application/ports/habit_completion_read_repository.py NEW
app/habits/infrastructure/persistence/models/habit_model.py NEW
app/habits/infrastructure/persistence/models/habit_completion_model.py NEW
app/habits/infrastructure/persistence/mappers/habit_mapper.py NEW
app/habits/infrastructure/persistence/mappers/habit_completion_mapper.py NEW
app/habits/infrastructure/persistence/repositories/habit_repository.py NEW
app/habits/infrastructure/persistence/repositories/habit_completion_repository.py NEW
app/habits/presentation/api/fastapi/routers.py              NEW
app/habits/presentation/api/fastapi/schemas.py              NEW
tests/habits/domain/...                                     NEW
tests/habits/application/...                                NEW
tests/habits/integration/...                                NEW
tests/habits/api/...                                        NEW
migrations/versions/0011_create_habits_v1_schema.py         NEW
app/app_factory.py                                          MODIFIED
app/composition_root.py                                     UNCHANGED
```

No file in this plan is created now.

## 14. Non-goals and authorization boundary

This plan introduces no progression intent, `ProgressionGateway`, Logos, Noema, AI, domain events, generic event bus, scheduler, worker, streak, frequency computation, statistics, quantitative habits, timezone profile, reminders, notifications, rename, Habit delete, soft delete, external dispatch, or analytics integration.

**Implementation remains NOT AUTHORIZED. Migration 0011 remains NOT CREATED / NOT AUTHORIZED.**
