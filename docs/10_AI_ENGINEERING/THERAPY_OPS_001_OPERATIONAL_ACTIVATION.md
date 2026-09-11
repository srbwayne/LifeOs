# THERAPY-OPS-001 — Therapy V1 Operational Activation

Status: **ACTIVE — OPERATIONAL CUTOVER COMPLETE**

Activation date: `2026-09-11`

Canonical runtime source: `99cd44e02464e4d09da4b3db4303384c1118b465`

Operational Alembic transition: `0009 -> 0010`

Final operational revision: `0010`

## Cutover evidence

- Pre-cutover `integrity_check`: `ok`
- Pre-cutover `foreign_key_check`: 0 rows
- Therapy tables were absent before migration
- Permanent verified backup was created
- Migration command: `alembic upgrade 0010`
- Post-migration `integrity_check`: `ok`
- Post-migration `foreign_key_check`: 0 rows
- `therapists` schema: PASS
- `therapy_sessions` schema: PASS
- Both Therapy tables were initially empty
- All pre-existing table counts were unchanged
- Progression records were unchanged
- No progression dispatch occurred
- Canonical runtime started successfully
- `GET /` returned 200
- Unauthenticated Therapy routes returned 401
- Owner-scoped read-only Therapy smoke returned 200
- Existing `GET /books` smoke returned 200
- Rollback was not executed

## Backup and rollback evidence

Permanent backup:

`C:\Users\ojnaa\Documents\pessoal\projeto rpg\LifeOS\backups\lifeos-pre-therapy-cutover-20260911-193250.db`

Backup SHA-256: `a31c7088c00ebf41bbbd9a0fdcc603305cec3c673cd974942a89299aa0db7366`

Rollback worktree SHA: `a1692f0c95aa124e4def51f601b7d6ec7aa3800b`

## Relationship to THERAPY-003F

THERAPY-003F recorded Therapy V1 implementation completion before operational activation. THERAPY-OPS-001 records the later successful operational activation and does not alter the historical meaning of the 003F closeout.

## Current Therapy V1 boundaries

Operational activation does not change the frozen boundaries:

| Boundary | State |
|---|---|
| Activity existence | YES |
| External exposure | NO |
| Progression eligibility | NO |
| Logos integration | NO |
| Noema / AI access | NO |
| Private note | Owner-private |
| Therapy event dispatch | NO |

## Scope record

This record makes no production-code, test, migration, configuration, database, runtime-restart, progression, Logos, or Noema/AI changes.
