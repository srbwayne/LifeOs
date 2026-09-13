# HABITS-010 — Habits V1 Implementation Closeout

Status: **IMPLEMENTATION COMPLETE — OPERATIONAL ACTIVATION NOT YET AUTHORIZED**

Canonical implementation SHA: `78f15a257b344f349903756aa6c5ab515cbcdd25`

## Business authority

Habits V1 implements HAB-001 and HAB-002 only. HAB-003 (streak), HAB-004
(frequency), and HAB-005 (statistics) remain deferred.

`Habit` is an owner-scoped reusable definition. `HabitCompletion` is an
owner-reported binary fact for an explicit civil date.

## Privacy and integration matrix

| Concern | Habits V1 |
|---|---|
| Activity existence | YES |
| Owner-private data | YES |
| External exposure | NO |
| Progression eligibility | NO |
| Logos integration | NO |
| Noema / AI access | NO |
| Habit event dispatch | NO |

Activity existence does not imply progression, external exposure, or
Noema/AI exposure.

## Final capabilities

`Habit` supports create, list, detail, deactivate, and reactivate. Rename,
delete, and soft delete are not supported in V1.

`HabitCompletion` supports mark, repeated idempotent mark, unmark correction,
and paginated history.

The checklist is a current-active-Habit projection for an explicit
`record_date`; `completed` is derived from completion-row presence.

## Final API surface

- `POST /habits` — 201
- `GET /habits` — 200
- `GET /habits/checklist` — 200, required `record_date`
- `GET /habits/{habit_id}` — 200
- `POST /habits/{habit_id}/deactivate` — 200
- `POST /habits/{habit_id}/reactivate` — 200
- `GET /habits/{habit_id}/completions` — 200, paginated
- `POST /habits/{habit_id}/completions` — 201 first / 200 repeat
- `DELETE /habits/{habit_id}/completions/{record_date}` — 204

Authentication is required for every route and ownership is derived from the
authenticated user. Malformed identifiers and dates return 422. Well-formed
missing and foreign resources preserve the same 404 contract.

## Business semantics

- Habit names are trimmed, blank names are rejected, case is preserved, and
  uniqueness is exact and case-sensitive per owner.
- There is no artificial business maximum length for names.
- Descriptions are optional, trimmed, and blank descriptions become `None`.
- New Habits are active; deactivate and reactivate are idempotent.
- Completion row existence represents the binary completed fact.
- `record_date` is an explicit civil DATE; historical and future dates are
  accepted without UTC or timezone derivation.
- The first mark returns 201; a repeated mark returns 200 with the same
  persisted completion.
- An inactive Habit with an existing completion remains idempotently markable
  with 200; an inactive Habit without a completion returns 409.
- Existing completions survive Habit deactivation and remain available in
  history.
- Checklist results use the CURRENT active Habit set, even for historical
  dates; an inactive historical Habit is excluded until reactivation.

## Domain and persistence boundaries

`Habit` and `HabitCompletion` are independent aggregate roots. Domain state
contains no technical timestamps. `completed` exists only in the checklist
read model and is not persisted.

Migration `0011` owns the Habits V1 schema, including the composite
owner/Habit foreign key and the unique completion business key
`(user_id, habit_id, record_date)`. Database uniqueness remains the
concurrency correctness boundary.

Slice 4 proved the deterministic two-session SQLite race for the tested
persistence model: both readers observe absence, both attempt insert/flush,
one wins, the loser rolls back before reloading the winner, both return the
same persisted ID, and one row remains. No `acquire_write_intent` application
dependency is required. This proof is not generalized beyond the tested
persistence model.

## Concurrency result

The canonical deterministic concurrency test passed once verbosely and ten
consecutive executions. Each execution proved two initial absent reads, two
flush attempts, one creation winner, one rollback recovery, winner reload
after rollback, one persisted row, and the same completion ID in both results.
No `OperationalError`, database-lock failure, or hanging worker was observed.

## Non-capabilities and deferred items

Habits V1 excludes streak, frequency, statistics, quantitative Habits,
targets, durations, units, categories/tags, schedules, timezone profiles,
reminders, notifications, rename, Habit deletion, soft delete,
progression/XP, Logos, Noema/AI, external dispatch, and Habit domain events.

## Implementation provenance

- HABITS-005 / Slice 1 — CLOSED — PR #73
- HABITS-006 / Slice 2 — CLOSED — PR #74
- HABITS-007 / Slice 3 — CLOSED — PR #75
- HABITS-008 / Slice 4 — CLOSED — PR #76
- HABITS-009 / Slice 5 — CLOSED — PR #77
- HABITS-010 / Slice 6 — closeout and isolated regression validation

The canonical implementation baseline before this documentation-only closeout
is `78f15a257b344f349903756aa6c5ab515cbcdd25`. Earlier slice details remain
in Git history and the merged PR records; no unsupported historical merge SHA
claims are added here.

## Operational state

Canonical Git migration head: `0011`.

The governed operational baseline before Habits activation remains `0010`.
Habits operational cutover is **NOT AUTHORIZED / NOT EXECUTED**.

The operational database was not accessed by this closeout. The closeout does
not claim that migration `0011` has been applied operationally.

## Validation evidence

All validation used the canonical implementation baseline and disposable test
databases where database access was required.

- Habits regression: 111 passed.
- Full pytest: 745 passed.
- Coverage: 99%, satisfying repository policy.
- Deterministic concurrency test: 10/10 passed.
- Ruff lint: PASS.
- Ruff format check: PASS.
- Mypy: PASS.
- Application import validation: PASS.
- DeprecationWarning rejection gate: PASS (745 passed).
- Disposable migration lifecycle `0011 -> 0010 -> 0011`: PASS.
- At revision 0010, both Habits tables were absent; at revision 0011, the
  schema and constraints were restored.
- `git diff --check`: PASS.

This closeout changes no production files, test files, migration files,
configuration, runtime, operational database, Progression, Logos, or
Noema/AI behavior.

## Next gate

The next separate gate is **HABITS V1 OPERATIONAL ACTIVATION / CUTOVER**.

If explicitly authorized, that future gate must independently define the
exact runtime source SHA, operational database identification, permanent
backup and verification/hash, pre-cutover `integrity_check` and
`foreign_key_check`, current migration verification, the expected `0010 ->
0011` transition, migration execution, post-migration integrity and schema
verification, preservation of pre-existing data/table counts where
appropriate, runtime update/start, authenticated Habits smoke testing,
existing-capability regression smoke testing, and rollback criteria.

None of those operational actions are executed or authorized by HABITS-010.
