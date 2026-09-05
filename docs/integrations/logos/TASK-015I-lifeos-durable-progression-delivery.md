# TASK-015I — Durable LifeOS → Logos Progression Delivery

Status: **IMPLEMENTED LOCALLY; CONTROLLED LOGOS E2E PENDING**

## Boundary

`READ` persists the canonical `ReadingSession`. The same LifeOS transaction
also persists a `progression_delivery_records` row owned by the reading
integration boundary. Logos remains the owner of canonical XP, level, stress,
attribute and skill progression.

The record stores facts rather than raw HTTP JSON:

```text
ReadingSessionId / reading_session_id
source = lifeos
idempotency_key = ReadingSessionId
subject_namespace = lifeos
subject_external_id = UserId
configuration_key = reading
configuration_revision = 2
pages_read
status, attempt_count, timestamps and bounded last_error
```

`(source, idempotency_key)` is unique. The record also has a restricted,
unique foreign key to `reading_sessions.id`, so a delivery intent cannot exist
without its source fact.

## Transaction and immediate delivery

The creation flow is:

```text
create ReadingSession
create completion when required
flush source fact
create delivery intent
flush delivery intent
commit once
best-effort dispatch after commit
```

If the intent cannot be persisted, the transaction rolls back. A Logos failure
after commit changes only the delivery record; it cannot roll back the
ReadingSession. The immediate dispatcher marks successful delivery as
`DELIVERED` and unresolved responses as `FAILED` while retaining the record.

The explicit `ProgressionDeliveryDispatcher.dispatch_unresolved()` method is
the recovery boundary for a later controlled invocation. It processes records
in subject/creation order and blocks a newer event for a subject when an older
one remains unresolved. Other subjects are not blocked.

## Configuration determinism

The configuration key and revision are captured from LifeOS runtime settings at
event creation. Dispatch reconstructs the Logos V3 request from those stored
facts; it does not resolve current configuration and does not read mutable
ReadingSession state. Delayed delivery therefore continues to request
`reading@2`.

## Failure classification

```text
200                 DELIVERED
400                 FAILED; no automatic retry
401 / 403           FAILED; operational correction then recovery
404                 FAILED; provisioning correction then recovery
409                 FAILED; manual review, no automatic retry
5xx / timeout      FAILED; retryable
```

Bearer tokens are read from `LOGOS_BEARER_TOKEN` at dispatch time and are never
stored in the delivery record. When `LOGOS_ENABLED=false`, the existing
disabled behavior is preserved: the ReadingSession succeeds without an
external delivery intent or HTTP call.

## Schema

Alembic migration `0009_create_progression_delivery_records.py` adds the
delivery table without changing migrations `0001`–`0008`. Delivered records are
retained for operational evidence. No LifeOS canonical progression state is
stored.

## Traceability

```text
INT-001 — Durable Progression Delivery
↓
RF-INT-001 — Durable External Progression Delivery
↓
US-INT-001-001
↓
TASK-015 — discovery/design
↓
TASK-015I — implementation
```

## Known limitations

- Recovery is an explicit service invocation; no scheduler, worker, outbox
  broker or external queue is introduced.
- Service-to-service authentication and source/namespace authorization remain
  operational debts.
- General concurrency control for different events of the same subject remains
  outside this slice; duplicate execution identity is protected by the Logos
  contract and database uniqueness.
