# LIFEOS-LOGOS-001C-D1-DEC-001 — Reading POC Configuration Decision

Status: **APPROVED / FROZEN FOR FIRST DISPOSABLE POC**

## Decision boundary

This decision applies only to the first disposable LifeOS → Logos Reading
integration POC. It is not final production game balancing and does not define
the permanent Logos attribute taxonomy.

The baselines reviewed were:

- LifeOS `db608b3230e72f07acb496d5c1ad466b1b276810`;
- Logos `e2c9253fe0eaa89f7a20d0706bc6effbeee6fd1d`.

## Approved configuration

| Field | Value |
|---|---|
| logicalKey | `reading` |
| factor semanticKey | `pages_read` |
| factor name | `Pages Read` |
| factor unit | `pages` |
| factor type | `NUMERICO` |
| baseXp | `1` |
| baseStress | `0` |
| calculationMode | `FACT_VALUE` |
| multiplier | `1.0` |
| minCutoff | `null` |
| maxCutoff | `null` |
| distribution weight | `1.0` |
| stressRules | `[]` |
| attribute | `Learning` |
| attribute status | POC-PROVISIONAL / NOT PRODUCTION TAXONOMY |

The future disposable Logos database may create these objects. This document
does not create them.

## Product semantics

`pages_read` represents the quantity of pages completed in one ReadingSession.
For this POC, one page produces one global XP and one Learning attribute XP,
subject to the canonical Logos engine.

The current engine evaluates the matching FACT_VALUE rule as:

```text
baseXp × multiplier × distributionWeight × pages_read
= 1 × 1 × 1 × pages_read
```

With one distribution, the expected values are:

| pages_read | global XP | Learning XP | stress |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 5 | 5 | 5 | 0 |
| 10 | 10 | 10 | 0 |
| 30 | 30 | 30 | 0 |
| 100 | 100 | 100 | 0 |

The zero-stress result follows from mandatory `baseStress=0` and empty stress
rules. XP result conversion uses the canonical `Double.longValue()` truncation
behavior.

## Why FACT_VALUE

`FACT_VALUE` is selected because `pages_read` is the approved LifeOS fact and
its magnitude should affect progression. It exercises the real fact-value
engine path while remaining deterministic and explainable.

`FIXED` would transport `pages_read` while ignoring its magnitude. Cutoff-based
balancing is deferred because the current out-of-range engine behavior is not a
conventional clamp and would require additional product balance decisions.

## Provisional attribute boundary

`Learning` is a broad, Reading-compatible concept that can later accommodate
books, study, and knowledge-oriented activities. Its use here is provisional.
It may later be retained, renamed, split, or replaced without invalidating the
integration POC.

## Explicit exclusions

The `1 XP/page` rate does not establish production economy, daily caps,
anti-abuse rules, book difficulty, reading quality, time-based rewards,
page-normalization rules, genre multipliers, or long-term balance.

No concrete UUID, published revision, LifeOS UserId, ReadingSessionId, Logos
player ID, JWT, or configuration version is selected by this decision. The
future bootstrap creates the draft, publishes it, captures the actual positive
revision, activates that exact revision, and then pins it in LifeOS.

## Isolation and next gate

The future E1 uses a dedicated disposable LifeOS SQLite database at Alembic
`0011` and a dedicated disposable Logos PostgreSQL database at Flyway `V43`.
No operational database is used.

Runtime, HTTP, database mutation, factor/attribute/configuration creation,
subject provisioning, ReadingSession creation, and historical replay were not
executed by this decision.

The next gate is:

`LIFEOS-LOGOS-001C-E1 — CONTROLLED RUNTIME / E2E EXECUTION`

It remains unauthorized until this documentation publication is independently
reviewed and merged.
