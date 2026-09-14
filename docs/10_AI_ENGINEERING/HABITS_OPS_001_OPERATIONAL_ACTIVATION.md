# HABITS-OPS-001 — Habits V1 Operational Activation

**ACTIVE — OPERATIONAL CUTOVER COMPLETE / EVIDENCE RECONCILED**

Activation date: 2026-09-13
Canonical runtime source: `2599e5d104194b5401950b14b5b62c00457afc69`
Operational transition: `0010 -> 0011`
Final operational revision: `0011`

## Reconciled cutover evidence

Operational fact: the R2 operational migration and read-only activation smoke
succeeded. The live database is at revision `0011`, with clean integrity and
foreign-key checks. The `habits` and `habit_completions` tables are empty.

Procedural deviation: the newly required R2-specific pre-cutover backup
artifact was not retained, even though the R2 gate required it before
migration. No R2-specific backup is claimed to have existed.

Reconciliation evidence:

- Preserved backup A:
  `backups/lifeos-pre-habits-cutover-20260913-210947.db`
- Preserved backup B:
  `backups/lifeos-pre-habits-recutover-20260913-212103.db`
- Both backups have SHA-256
  `7621c7798e58e44a6f98d0f98c097f3581eae50447af89e110d9cd9bb43d011f`.
- Both backups independently verify at revision `0010`, with integrity check
  `ok`, zero foreign-key violations, absent Habits tables, and identical
  logical contents.
- A disposable clone of preserved revision `0010` successfully executed
  `alembic upgrade 0011`; the reconstructed revision, schema, integrity,
  foreign-key state, empty Habits tables, and all application-table logical
  digests matched the active operational database.
- A new post-activation safety backup was created during reconciliation:
  `backups/lifeos-post-habits-r2-reconciliation-20260913-215400.db`.
- Its SHA-256 is
  `206924553e09c7bbf48bfad2bb24dee4ad50c2633cc76f068047649a75d37fb9`.
- The post-activation backup verifies revision `0011`, integrity check `ok`,
  zero foreign-key violations, and matching application-table counts.

The authorized migration command was `alembic upgrade 0011`. No migration was
run against the operational database during R3. The operational database was
not modified by reconciliation or smoke testing.

## Activation Attempt History

1. HABITS-OPS-001 migrated `0010 -> 0011`, but authenticated smoke was
   unavailable; rollback restored `0010` cleanly.
2. HABITS-OPS-001R stopped before operational mutation because safe existing
   credentials were unavailable.
3. HABITS-OPS-001R2 used clone-only authentication; operational migration and
   smoke succeeded, but the required R2-specific new backup artifact was
   missing, so activation documentation was blocked.
4. HABITS-OPS-001R3 revalidated preserved `0010` evidence, reproduced the
   `0010 -> 0011` state on a disposable clone, proved logical equivalence,
   revalidated current read-only smoke, and created the post-activation
   `0011` safety backup.

## Runtime and smoke evidence

- Canonical runtime started successfully from the canonical source.
- `GET /` returned `200`.
- Unauthenticated Habits routes returned `401`.
- Authenticated `GET /habits` returned `200` with `[]`.
- Authenticated `GET /habits/checklist?record_date=2026-09-13` returned `200`
  with `[]`.
- Authenticated Books and Therapy read-only smoke returned `200`.
- No operational authentication/session write occurred.
- Users, sessions, password-reset state, Books/Reading, Therapy, Progression,
  and all other pre-existing application-table counts and logical digests
  remained unchanged.
- No Progression dispatch occurred.
- Temporary reconciliation/authentication clones and credential material were
  removed. Permanent backups were retained.

## Privacy and integration boundaries

| Boundary | State |
|---|---|
| Activity existence | YES |
| Owner-private data | YES |
| External exposure | NO |
| Progression eligibility | NO |
| Logos integration | NO |
| Noema / AI access | NO |
| Habit event dispatch | NO |

Habits activity existence does not imply progression eligibility, external
exposure, or Logos/Noema/AI access.

HAB-003 streak remains deferred. HAB-004 frequency remains deferred. HAB-005
statistics remains deferred.

## Relationship to implementation closeout

HABITS-010 recorded implementation completion before operational activation.
This record documents the later successful activation and evidence
reconciliation; it does not alter the historical meaning of HABITS-010.

## Operational state

Canonical Git migration head: `0011`
Final operational revision: `0011`
Operational cutover: `ACTIVE — COMPLETE`
Rollback: `NOT REQUIRED / NOT EXECUTED`

The activation is ratified from preserved earlier pre-cutover evidence,
deterministic disposable reconstruction/equivalence evidence, and the new
verified post-activation backup. No R2-specific pre-cutover backup is claimed
to exist.
