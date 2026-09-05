# TASK-015 — LifeOS Durable Progression Delivery Discovery

Status: **DISCOVERY COMPLETE; IMPLEMENTATION NOT STARTED**

## Baseline

- Branch: `docs/read-005-slice5-integration-reconciliation`
- HEAD: `6ce367a0b2c5153f8e087bb97638563211c75e1d`
- Working tree: clean before this document; this file is the only task change.
- Tests: `507 passed` (`.venv-platform311`, Python 3.11).
- LifeOS Alembic head in the repository: `0008`.
- Next legitimate migration: `0009`.

The local validation database had been at `0007`; the existing historical `0008`
was applied during TASK-013V-R setup. No new migration is proposed here.

## 1. Current integration flow

Evidence: `app/read/application/commands/create_reading_session.py`,
`app/read/infrastructure/integrations/logos_progression_gateway.py`, and
`app/read/dependencies.py`.

```text
CreateReadingSessionCommandHandler
  -> save ReadingSession and completion
  -> uow.flush()
  -> uow.commit()
  -> build ReadingProgressionFact
  -> optional LogosProgressionGateway
  -> POST Logos V3
```

`ReadingProgressionFact` contains the session ID, `UserId` and `pages_read`.
The gateway maps those values to the fixed LifeOS V3 contract. Its result is
not persisted by LifeOS.

The handler deliberately ignores gateway failure after commit. This preserves
the fact but loses delivery when Logos is unavailable.

## 2. Event bus

Evidence: `app/shared/application/event_bus.py` and
`app/shared/infrastructure/unit_of_work.py`.

| Question | Finding |
|---|---|
| Durable? | **NO** |
| Usable as the outbox itself? | **NO** |
| Behavior | In-process synchronous handler calls |
| Transaction relation | `SqlAlchemyUnitOfWork.commit()` commits first, then publishes tracked domain events |
| Error behavior | Handler exceptions are printed and swallowed |
| ReadingSession integration | No ReadingSession domain event is currently emitted or registered |

The event bus can be an in-process notification after persistence, but cannot
be the recovery source after process termination or restart.

## 3. Unit of Work and atomic boundary

Evidence: `app/shared/infrastructure/unit_of_work.py`,
`app/read/application/commands/create_reading_session.py`, and migration
`migrations/versions/0008_create_book_completions_with_backfill.py`.

`SqlAlchemyUnitOfWork` owns one SQLAlchemy `Session`; `commit()` commits that
session and only then publishes in-memory events. The ReadingSession handler
currently inserts the session and optional completion, flushes, and commits.

The future delivery intent must be inserted through the same session before
`uow.commit()`. Therefore:

```text
ReadingSession + completion + durable delivery intent
  -> one SQL transaction
  -> commit
```

If the intent insert fails, the transaction must roll back. The current
post-commit gateway call must not be the place where the durable record is
created.

The proposed invariant is limited to newly integrated ReadingSessions:

```text
ReadingSession committed
iff
progression delivery intent committed
```

Legacy ReadingSessions remain outside that invariant.

## 4. Database and background execution

LifeOS uses SQLAlchemy models in `app/**/infrastructure/persistence/models`
and Alembic revisions `0001` through `0008`. The current ReadingSession table
stores immutable-at-application-boundary source facts (`id`, `user_id`, page
range, timestamps and notes); `ReadingSession.restore()` and the aggregate
have no update command for those facts.

No scheduler, worker, poller, queue, cron, `APScheduler`, background task or
startup dispatcher was found in `app` or `tests`. The FastAPI lifespan only
prints startup/shutdown messages (`app/app_factory.py`). A dispatcher is
therefore a future implementation concern, not an existing capability to
reuse.

## 5. Recommended ownership

**PROPOSED:** keep the first durable record in the `read` capability because
ReadingSession → Logos is the only proven durable integration today:

```text
app/read/application/ports/
app/read/infrastructure/persistence/
app/read/application/services/  (or equivalent orchestration boundary)
```

The record should represent a LifeOS integration delivery, not a generic
framework. A later second use case can justify extracting a shared delivery
component.

## 6. Recommended V1 record

The following is a proposed future table/aggregate; no schema is created in
TASK-015.

| Field | Decision | Reason |
|---|---|---|
| Technical `id` | **REQUIRED NOW** | Internal row identity, independent of source identity |
| `event_type` | **REQUIRED NOW** | Identifies `reading_session_recorded` without inspecting payload |
| `source` | **REQUIRED NOW** | Fixed `lifeos` scope and future source separation |
| `idempotency_key` | **REQUIRED NOW** | `ReadingSessionId`; must be immutable |
| `subject_namespace` | **REQUIRED NOW** | `lifeos` |
| `subject_external_id` | **REQUIRED NOW** | LifeOS `UserId` used by Logos |
| `configuration_key` | **REQUIRED NOW** | Current contract intent: `reading` |
| `requested_revision` | **REQUIRED NOW** | Nullable; distinguishes key-only from explicit revision intent |
| `pages_read` | **REQUIRED NOW** | Immutable source fact used to build the request |
| `status` | **REQUIRED NOW** | Delivery lifecycle |
| `attempt_count` | **REQUIRED NOW** | Local retry observability and scheduling |
| `created_at` | **REQUIRED NOW** | Ordering and operations |
| `last_attempt_at` | **USEFUL NOW** | Operations and retry diagnosis |
| `next_attempt_at` | **USEFUL NOW** | Bounded backoff scheduling |
| `delivered_at` | **USEFUL NOW** | Delivery audit |
| `last_error` | **USEFUL NOW** | Local diagnosis; redact secrets/payloads |
| Raw HTTP payload | **DEFER** | Couples storage to transport and is unnecessary for this fact |
| Bearer token | **UNNECESSARY / PROHIBITED** | Resolve credentials at delivery time |
| Logos response/profile | **DEFER** | Logos is canonical; not needed to retry the request |

Required uniqueness:

```text
UNIQUE(source, idempotency_key)
```

Historical rows are not backfilled with invented identities.

## 7. Persisted representation

**RECOMMENDED: FACTS.** Persist the immutable integration facts and request
intent, then construct the V3 payload at delivery time. The current domain
already exposes `ReadingProgressionFact`, and the gateway owns translation to
HTTP.

This keeps the outbox independent of JSON/header details while preserving the
values needed to reproduce the same request. If the contract mapping changes,
the event type/version or a migration can make that change explicit rather
than silently rewriting stored payloads.

## 8. Event identity and idempotency

The source identity is:

```text
source = lifeos
idempotencyKey = ReadingSessionId
```

A technical outbox `id` is still useful for database references, logs and
dispatcher bookkeeping. It must not replace the source identity, and retry
must never generate a new idempotency key.

## 9. Ordering and concurrency

### Same subject

**ORDER REQUIRED** for the first durable delivery design. Evidence from the
Logos progression model and TASK-013V-R shows that execution mutates current
profile state, levels, stress and skill-point side effects. Even if some XP
totals are additive, applying stateful events out of source order can change
intermediate transitions and future outcomes.

The outbox should retain source creation order (at minimum `created_at` plus a
stable technical ID) and a future dispatcher should serialize pending events
per `subject_external_id`. This is a requirement to address, not an
implementation in this task.

### Different subjects

They may be dispatched independently.

### Different ReadingSession IDs for one subject

Logos idempotency protects only duplicate identities. It does not protect two
distinct sessions from concurrent profile updates. A future dispatcher should
avoid concurrent delivery for one subject, while broader Logos optimistic
locking/concurrency remains a separate debt.

## 10. Delivery semantics

**AT-LEAST-ONCE delivery + Logos idempotent application.** Distributed
exactly-once is neither required nor achievable from the current two
transactions. The crash/retry protocol relies on the frozen Logos identity:

```text
(lifeos, ReadingSessionId) -> one logical Logos execution
```

## 11. Retry and status model

### Recommended V1 policy

Use a small bounded exponential backoff policy with no enterprise queue or
dead-letter subsystem. A retryable row remains eligible for later dispatch;
exact limits/timings require operational approval after the first dispatcher
exists. Manual retry must reuse the same identity and facts.

### Recommended states

```text
PENDING -> DELIVERED
PENDING -> FAILED
FAILED  -> DELIVERED
```

`PROCESSING` is **DEFERRED** for V1. A single local dispatcher can make one
attempt in a transaction and write the next state. If multiple workers or
long-running claims are introduced later, a lease/processing state becomes
necessary to recover abandoned claims.

## 12. Crash matrix

| Scenario | Expected result |
|---|---|
| A. ReadingSession saved, intent insert fails | One transaction rolls back both; no fact and no pending intent |
| B. Both committed, process crashes before HTTP | Pending intent remains recoverable on next dispatcher run |
| C. Logos commits, LifeOS crashes before marking delivered | Retry sends same identity; Logos returns the existing execution without a second mutation |
| D. HTTP timeout with unknown Logos outcome | Treat as retryable; Logos idempotency resolves whether it already committed |

## 13. Logos result classification

| Result | Classification | Rationale |
|---|---|---|
| 2xx | **DELIVERED** | Successful Logos acknowledgement |
| 400 | **TERMINAL / MANUAL REVIEW** | Invalid contract or source data; retry cannot correct it |
| 401 | **TERMINAL / MANUAL REVIEW** | Credential/configuration failure; refresh configuration first |
| 403 | **TERMINAL / MANUAL REVIEW** | Authorization failure; no blind retry loop |
| 404 subject | **TERMINAL / MANUAL REVIEW** | Provisioning is missing; retry only after correction |
| 404 configuration | **TERMINAL / MANUAL REVIEW** | Configuration provisioning is missing |
| 409 | **TERMINAL / MANUAL REVIEW** | Same identity with different request; indicates data corruption or mapping defect |
| 5xx | **RETRYABLE** | Remote transient failure |
| timeout/connection | **RETRYABLE** | Outcome is unknown; retry is required and safe |

An exact duplicate should normally be acknowledged by Logos as 2xx and is
therefore delivered, not treated as a conflict.

## 14. Authentication and namespace

Bearer credentials must be loaded from environment/configuration at dispatch
time. They must never be stored in the durable record, logs or payload facts.

The current pilot keeps `namespace=lifeos` and `externalId=UserId`. Source
authorization and multi-tenant identity validation are future concerns; the
outbox must not infer authorization from the persisted `source` field.

## 15. Configuration-version timing

This is the remaining **HUMAN DECISION REQUIRED** item.

The current LifeOS contract sends `configuration.key=reading` without a
revision. If delivery is delayed across a Logos rollout:

```text
ReadingSession committed
reading@2 is current
delivery delayed
reading@3 becomes current
delivery occurs
```

the current V3 semantics resolve `reading@3` at delivery time. Logos will then
freeze `reading@3`, but that is not the same as event-time configuration
selection.

| Option | Semantics | Assessment |
|---|---|---|
| A — key only | Delayed delivery uses current version at delivery time | Simplest and compatible with current pilot; configuration drift is explicit |
| B — freeze revision | Outbox stores an exact revision selected at event creation | Stronger event-time reproducibility, but LifeOS needs an approved way to know the revision without making commit depend on Logos |
| C — separate resolution record | A Logos-side reservation/selection records the version before delivery | More coupling and a new cross-service protocol; not justified by current evidence |

**PROPOSED pilot default: Option A**, explicitly named “current at delivery”.
It preserves the existing request and ownership boundaries. It must not be
used for replay of a completed Logos execution. If event-time configuration
semantics are required, human approval should select Option B and define the
version-resolution contract before implementation.

## 16. Payload immutability and replay

`ReadingSession` facts are immutable at the current application boundary:
there is a create/restore aggregate API and no update command for page facts.
The durable record must copy the source ID, user ID, `pages_read`, event type
and configuration intent at commit time; it must not re-read a mutable session
to build a retry.

Manual replay of a failed event means another delivery attempt of the same
record, preserving source, idempotency key, subject, facts and the approved
configuration-timing policy. It must not create a new source identity.

## 17. Observability and retention

Minimum useful operational visibility for a local/personal V1:

- count of pending/failed records;
- oldest pending record;
- attempt count, last attempt time and next attempt time;
- last sanitized error category/status;
- delivered timestamp.

No dashboard is required. Delivered records should be retained initially for
audit and duplicate diagnosis; a later retention policy may compact them only
after the Logos execution evidence and operational needs are understood.

## 18. Current gateway transition

**RECOMMENDED: Option B — durable intent plus immediate best-effort dispatch.**

```text
same LifeOS transaction:
  ReadingSession + delivery intent
commit
post-commit:
  attempt immediate Logos delivery
  mark DELIVERED or retryable/failed
```

This preserves the current user-visible latency and post-commit failure
isolation while making a process crash or network outage recoverable later.
Option A (replace the immediate call with only a worker) is safer for request
latency but requires the dispatcher before the feature is usable. A pure
post-commit direct call remains insufficient.

## 19. Future LifeOS schema impact

No schema was created in TASK-015. The next implementation would likely add a
new Alembic `0009` table owned by the reading/integration boundary, with a
unique `(source, idempotency_key)` constraint and indexes supporting status
plus `next_attempt_at` and subject ordering. Exact SQLAlchemy naming and JSON
usage require implementation review.

## 20. Risks

- duplicate delivery: mitigated by the immutable Logos execution identity;
- lost delivery: current direct call remains vulnerable until the outbox exists;
- stuck pending events: requires dispatcher visibility and bounded backoff;
- configuration drift: unresolved event-time versus delivery-time policy;
- subject ordering: distinct events are not protected by idempotency;
- token expiration/authorization: credentials are external and may fail;
- process crash: durable intent handles crashes after commit;
- conflicting 409: requires manual investigation, never blind retry;
- multi-tenant subject ambiguity: current `lifeos + UserId` is pilot-only.

## 21. Scope impact

- Logos changes: **NONE**; V3 idempotency is sufficient.
- Noema changes: **NONE**.
- Production changes in TASK-015: **NONE**.
- Migration created: **NONE**.

## 22. Decision gate

```text
TASK-015: COMPLETE

DURABLE DELIVERY NEED: CONFIRMED
OUTBOX BOUNDARY: DESIGNED
ATOMICITY: DESIGNED
DELIVERY SEMANTICS: AT-LEAST-ONCE
LOGOS IDEMPOTENCY: REUSED
CURRENT DIRECT CALL: TRANSITION DEFINED
CONFIGURATION VERSION TIMING: HUMAN DECISION REQUIRED
LOGOS CHANGE: NONE
NOEMA CHANGE: NONE
IMPLEMENTATION: BLOCKED FOR HUMAN DECISION
```

Human approval has frozen the event-time revision contract: the implementation
must persist `configurationKey = reading` and `configurationRevision = 2` when
the delivery event is created. Delayed delivery must continue to request
`reading@2`, even if a later revision becomes current.

The implementation remains authorized only after governance registration in
TASK-015G and is tracked as TASK-015I. It must preserve the V1 constraints:
facts rather than raw HTTP payload, same-transaction intent, at-least-once
delivery, per-subject order, and no persisted credentials.

Traceability:

```text
INT-001 — Durable Progression Delivery
↓
RF-INT-001 — Durable External Progression Delivery
↓
TASK-015 — LifeOS Durable Progression Delivery Discovery
↓
TASK-015I — Durable LifeOS → Logos Progression Delivery
```
