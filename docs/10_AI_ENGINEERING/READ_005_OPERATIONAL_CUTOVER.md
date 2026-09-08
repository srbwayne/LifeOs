# READ-005 / TASK-015 Real Operational Cutover Closure

Date: 2026-09-07

Status: **CLOSED — REAL LOCAL OPERATIONAL HISTORY VERIFIED**

This document records the observed local operational history. It does not
authorize a new migration, recovery dispatch, downstream integration, or
feature initiative.

## 1. Observed database history

The originally planned coordinated migration path was not the state found in
the real local database. On inspection, the database already reported:

- `alembic_version = 0009`;
- BookCompletion/runtime-related history inconsistent with the previous
  assumption that the real database was still at `0007`;
- exactly two pre-existing foreign-key violations: one `sessions` row and one
  `players` row, both referencing the same missing user;
- `progression_delivery_records` in a noncanonical/intermediate schema.

**PROVENANCE OF THE NONCANONICAL 0009 STATE: UNDETERMINED.**

No old branch, process or actor is attributed by this record. The observed
state is not described as a normal Alembic `0007 -> 0008 -> 0009` upgrade.

## 2. Preservation reconciliation

The approved preservation decision retained the surviving aggregate and
reconstructed the missing principal using the same identifier:

- missing user: `0RH21M9HZQE5Q`;
- player preserved: `0RH21M9JKE9KT`;
- character preserved: `0RH21M9JXDEY4`;
- historical session preserved: `0RH21M9WSQKSB`.

The approved search did not recover a trustworthy historical source for the
missing user. A synthetic recovery identity was therefore created with:

- email: `recovered.0rh21m9hzqe5q@lifeos.invalid`;
- password material generated only in memory and stored only as a canonical
  Argon2 hash;
- plaintext never persisted or logged;
- recovery-derived `created_at`: `2026-09-04 23:37:18.612522`;
- repair timestamp: `2026-09-07T23:01:37.961239Z`.

The creation timestamp is explicitly recovery-derived and is not claimed to be
the original historical user creation timestamp. The historical session was
preserved and revoked so reconstruction could not reactivate old authentication
state.

## 3. Progression schema reconciliation

The real progression table was an intermediate/noncanonical 0009-era shape
containing legacy-only fields:

- `source`;
- `idempotency_key`;
- `subject_namespace`;
- `subject_external_id`;
- `configuration_key`;
- `configuration_revision`.

During the approved preservation transaction it was rebuilt in place to the
exact canonical Migration 0009 model. The following canonical values were
preserved:

- `id`;
- `reading_session_id`;
- `pages_read`;
- `status`;
- `attempt_count`;
- `last_error`;
- `created_at`;
- `last_attempt_at`;
- `delivered_at`.

The following values were derived:

- `owner_id` from the referenced `ReadingSession`;
- `updated_at = last_attempt_at` when present, otherwise `created_at`.

No Migration 0010 was created, and Migration 0009 was not edited. The
`alembic_version` value remained `0009`. No historical progression row was
dropped: the original eight rows remained eight, with status distribution
`DELIVERED 6 / FAILED 1 / PENDING 1` and attempt total `12`.

## 4. Backup evidence

Both backups remain retained outside Git as operational audit/recovery evidence.

### Pre-preservation repair

- file: `lifeos-pre-preservation-repair-20260907-230137.db`;
- SHA-256: `3edaa80f15cd0ea3bce123cca95b53b92838eee44d5b8f094efc473510aff48e`;
- purpose: pre-repair historical/noncanonical state evidence.

### Post-repair / pre-first-write-canary

- file: `lifeos-post-repair-pre-canary-20260907-231728.db`;
- SHA-256: `83bebc4565ccfd0eafdc3c3285a5c1a70a7f95ad1980cc310868d80c59871564`;
- purpose: canonical repaired state immediately before the first accepted
  canonical business write.

Neither backup is tracked in Git.

## 5. Preservation repair validation

The successful repair validation established:

- revision `0009`;
- `integrity_check = ok`;
- empty `foreign_key_check`;
- recovered user readable through the current mapping;
- player and character preserved;
- historical session revoked;
- progression ORM read passed;
- unresolved count after repair: `2`;
- no dispatcher executed;
- no runtime active during repair.

The validated immediate pre-repair execution baseline was SHA-256
`085c82f442e7233358a30ef213fc32bc786dfbda3d0da3f2dff242947a0573c4`.
The post-repair SHA-256 was
`800c6994c5c0375b4897ce5aa84bd59a84fb532a963a8c24710a3999b4efe6f2`.
These are reported as time-specific evidence; no cause is inferred for
differences from older forensic SHA values.

## 6. Read-only runtime activation

**CANONICAL RUNTIME READ-ONLY ACTIVATION: PASS**

Evidence:

- canonical code SHA: `a1692f0c95aa124e4def51f601b7d6ec7aa3800b`;
- real database explicitly targeted through an absolute read-only SQLite URI;
- `mode=ro` and the write-rejection probe passed;
- `GET /` returned `200`;
- startup performed no migration and no automatic progression recovery;
- database SHA remained `800c6994c5c0375b4897ce5aa84bd59a84fb532a963a8c24710a3999b4efe6f2`;
- unresolved count remained `2`;
- runtime shut down cleanly after this gate.

## 7. First canonical write canary

### Initial attempt

The first attempt was blocked before persistence. The isolated one-shot harness
had not loaded the full ORM composition, leaving `users` absent from shared
`Base.metadata` and causing `NoReferencedTableError`.

This was a harness-composition error, not a real database or schema defect. The
handler was invoked once, no flush or commit persisted, no retry was performed
inside that attempt, and the database SHA remained unchanged.

### Corrected attempt

**FIRST CANONICAL WRITE CANARY: PASS**

The full production ORM composition was loaded through `app.main` before the
single handler invocation.

- owner: `0RH970TKHWF6W`;
- book: `0RH9AX0A66WXG`;
- page: `1`;
- ReadingSession: `0RHZMAPTVBZ12`;
- progression delivery: `0RHZMAPV7C31Y`.

Results:

- ReadingSessions `8 -> 9`;
- progression records `8 -> 9`;
- new delivery `PENDING`, attempt count `0`, with no error or delivery
  timestamps;
- previous eight deliveries unchanged;
- statuses `DELIVERED 6 / FAILED 1 / PENDING 2`;
- attempt total `12`;
- unresolved `2 -> 3`;
- coverage remained `37` pages;
- BookCompletion remained absent;
- integrity check passed;
- foreign-key check was empty.

Post-canary SHA-256:
`900c3a6edb2b812371232333e186bd8e10ceeaa987d15dd37afc5c7a6b5b3a97`.

The canary row is intentionally retained as accepted canonical operational
history.

## 8. Writable runtime activation

**WRITABLE CANONICAL RUNTIME ACTIVATION: PASS — LIFEOS OPERATIONAL**

Activation-time evidence:

- source SHA: `a1692f0c95aa124e4def51f601b7d6ec7aa3800b`;
- writable real database URL explicitly targeted the absolute real database;
- exactly one intended Uvicorn runtime tree;
- server PID: `63660` at activation time;
- listener: `127.0.0.1:18082`;
- `GET /` returned `200`;
- `GET /openapi.json` returned `200`;
- no migration attempt;
- no automatic progression dispatch;
- ReadingSessions remained `9`;
- progression records remained `9`;
- statuses remained `6 / 1 / 2`;
- attempts remained `12`;
- unresolved remained `3`;
- canary delivery remained `PENDING / 0`;
- database SHA remained `900c3a6edb2b812371232333e186bd8e10ceeaa987d15dd37afc5c7a6b5b3a97`.

The PID is activation-time evidence, not a permanent process identifier.

## 9. Current operational contract

- LifeOS is operational locally.
- The canonical runtime source is the main lineage at
  `a1692f0c95aa124e4def51f601b7d6ec7aa3800b`.
- The real database canonical schema revision is `0009`.
- `NoOpProgressionGateway` remains the default downstream.
- Durable intents are persisted even while the downstream is NoOp.
- Startup performs no automatic dispatch or recovery.
- `dispatch_unresolved()` remains an explicit recovery entry point only.
- Unresolved records at closure: `3`.
- The three unresolved records are not dispatched as part of this closure.
- Logos is not integrated as a real downstream.
- Scheduler and worker remain absent.
- At-least-once delivery remains the intended model; exactly-once is not
  promised.

The accepted first canonical write establishes a **FIX-FORWARD** policy. The
pre-canary backup is not a routine rollback target.

## 10. Local governance preservation evidence

The historical dirty worktree was audited. Obsolete pre-canonical subject-based
implementation and tests were not transplanted because canonical main already
contains the current ordering and retry semantics.

The following are local preservation evidence only:

- `archive/read-005-slice5-precanonical-66428c8` ->
  `66428c8bd45acc8d2160bfdcc1100ae145c41723`;
- `salvage/read-005-slice5-durable-delivery-audit`;
- salvage commit `edc0d258ce7a0608c5009f6783ea10e9de454507`;
- original repository worktree returned cleanly to `main` at
  `a1692f0c95aa124e4def51f601b7d6ec7aa3800b`.

No archive or salvage branch was pushed during reconciliation.

## 11. Closure boundary

This document closes the verified local operational cutover history. It does
not authorize dispatch of unresolved records, Logos adapter/configuration/auth
or HTTP integration, scheduler/worker activation, automatic recovery, a new
migration, new product functionality, cleanup of the accepted canary, or
backup restoration.
