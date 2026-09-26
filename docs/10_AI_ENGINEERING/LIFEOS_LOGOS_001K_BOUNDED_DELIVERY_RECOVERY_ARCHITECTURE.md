# LIFEOS-LOGOS-001K — Bounded Delivery Recovery Policy

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001K-DEC-001`.

This is a governance and architecture record only. It authorizes no recovery,
source, schema, migration, scheduler, database, runtime, replay, deployment,
credential, or productization work.

## Selected policy

The selected policy is **Policy B — Explicit bounded recovery lifecycle**.
LifeOS owns the durable delivery lifecycle, retry eligibility, attempt history,
retry budget and timing, operator state, and terminal/quarantine disposition.
Logos owns canonical progression execution truth, execution idempotency,
fingerprint and conflict semantics. Neither system rewrites the other's
historical truth.

## Identity invariants

Normal retry preserves:

```text
source
idempotencyKey
subject
requested configuration key/revision
progression details
```

For Reading:

```text
source = lifeos
idempotencyKey = reading-session:<ReadingSessionId>
```

The Delivery ID remains the correlation root. Every retry receives a new
`attemptNumber`, new `requestId`, fresh workload assertion, and fresh `jti`.
Business idempotency identity never changes.

## Recovery lifecycle

The conceptual lifecycle is equivalent to:

```text
PENDING
RETRY_WAIT
IN_PROGRESS
OPERATOR_ACTION_REQUIRED
DELIVERED
QUARANTINED
TERMINAL
```

Exact persisted names and whether state/disposition are separate remain
technical-plan decisions. The existing `FAILED` state is insufficient because
it conflates retryable failures, operator action, terminal rejection,
ambiguous outcomes, and exhausted budget.

## Retry budget and timing

The canonical budget semantic is:

```text
maxAttempts = total durably reserved delivery attempts,
including the initial attempt
```

Every reserved attempt counts, including success, transport failure, timeout,
HTTP rejection, rate limiting, and server failure. The numeric value is finite,
bounded, auditable, and deferred to the technical plan or controlled runtime
configuration. `maxRetries` is not the canonical term.

Automatic retries use bounded exponential backoff. A valid bounded HTTP 429
`Retry-After` may be honored, but cannot create unbounded scheduling. Exact
delays, multiplier, cap, jitter, and Retry-After limits remain unselected.
`nextAttemptAt` or equivalent timing semantics are required for retryable
deliveries. Operator-action states have no automatic timer by default.

When attempts reach `maxAttempts`, automatic recovery stops and the delivery
becomes quarantined/operator-action-required. There is no silent budget reset
or infinite redispatch. A normal `RETRY_NOW` does not bypass the budget; any
override requires a separate authorized, reasoned, audited administrative
action.

No scheduler, cron, worker, queue consumer, or background service is selected
or authorized. This policy defines eligibility and state, not invocation
infrastructure.

## Failure policy

Network failures and HTTP 5xx are retryable with the same business identity.
HTTP 429 is rate-limited and consumes an attempt. HTTP 401, 403, prerequisite
404, and inactive configuration are operator-action classifications and do not
loop automatically. Confirmed HTTP 400 business rejection is terminal.

A confirmed fingerprint conflict for the same `source + idempotencyKey` is not
repaired by changing request fields; it requires operator or reconciliation
handling.

`AMBIGUOUS_OUTCOME` applies when LifeOS cannot prove whether Logos committed,
including timeout, lost response, post-commit persistence failure, process
crash after transmission, or an orphaned reserved attempt. Under the current
execute-only authorization, the initial strategy is a bounded same-identity
POST retry. It is not a general downstream read capability.

## Strict configuration guard

Normal retry uses the exact original configuration key and revision associated
with the delivery. Recovery must not read a newer environment setting and
silently reinterpret an old delivery. Missing, inactive, or unavailable
original configuration becomes operator action. Configuration supersession is
not a normal retry and requires a separate explicit decision.

## Ownership, authorization, and authentication revalidation

Before every new outbound attempt, current HARD-003 ownership and HARD-002
source/namespace/operation authorization must be valid. Disabled, revoked,
transferred-incompatibly, tombstoned, or otherwise invalid ownership prevents
new progression use. Revoked authorization likewise prevents the request.

Each retry must satisfy HARD-001 with a fresh signed assertion and `jti`.
Previous permission or assertion validity is never reused as current
authorization.

## Lease and claim policy

Recovery uses an atomic lease with expiry, conceptually including lease owner,
acquisition time, and expiry time. A database lock held across the HTTP request
is explicitly not selected.

Lease expiry may make a delivery eligible again after a worker crash, but a
stale worker must not overwrite a newer attempt or disposition. Completion must
use a CAS, version, lease token, or equivalent stale-worker guard. Exact fields,
tokens, and duration remain technical-plan decisions.

## Attempt reservation boundary

Attempt evidence is durably reserved before HTTP:

```text
TX1:
  acquire lease
  reserve counted attempt
  assign attemptNumber and requestId
  freeze business/configuration evidence
  commit

NETWORK:
  send request

TX2:
  record outcome
  transition delivery/disposition
  release or complete lease
  commit
```

If TX1 does not commit, no attempt exists. If TX1 commits but no final outcome
is recorded, the attempt counts toward `maxAttempts` and is conservatively
ambiguous after lease expiry unless stronger evidence proves otherwise.

## Terminal, quarantine, and operator actions

`TERMINAL` means normal retry cannot make the business action succeed.
`QUARANTINED` means automatic processing is stopped pending human or
reconciliation action. Administrative abandon is an auditable non-retry
disposition; it does not delete evidence.

Conceptual actions include:

```text
RETRY_NOW
RESUME
QUARANTINE
MARK_TERMINAL
ABANDON
RECONCILE_DOWNSTREAM
RELEASE_SUCCESSORS
```

`SUPERSEDE_CONFIGURATION` is not a normal recovery action. Every action must
eventually record actor, delivery, business identity, prior/new state or
disposition, timestamp, reason, attempt reference when applicable,
configuration identity, and correlation root.

## Same-owner ordering

Older deliveries block newer same-owner deliveries by default, including
`RETRY_WAIT`, `OPERATOR_ACTION_REQUIRED`, `QUARANTINED`, and `TERMINAL` states.
This conservative default prevents silent causal bypass.

`RELEASE_SUCCESSORS` is an explicit operator action that only releases later
deliveries. It does not mark the old delivery delivered, erase its disposition,
retry it, change business identity, or rewrite attempt history. Release is
authorized, reasoned, timestamped, and auditable.

## Historical and existing-record boundaries

HARD-004 covers recovery of an existing durable delivery only. It does not
authorize historical replay, backfill, creation of missing old deliveries,
source-event recreation, or bulk redispatch.

Existing `PENDING` and `FAILED` rows must not be treated as if they already have
attempt history, request IDs, configuration provenance, leases, or operator
decisions. Migration and backward-compatibility treatment remain future work.

Historical attempt evidence is immutable. Later policy or classification changes
may affect future eligibility only through explicit auditable state/disposition
changes; they must not rewrite what happened.

## Observability and dependency boundaries

HARD-005 privacy and cardinality rules remain in force. Recovery metrics may use
bounded state/category dimensions, but not delivery ID, idempotency key, request
ID, or subject external ID. No observability implementation is authorized.

HARD-004 depends architecturally on future HARD-005 evidence availability, but
that dependency is not implementation authorization. HARD-006 remains separate
and no secret manager, key storage, injection, or rotation design is selected.

## Technical-plan deferrals

The following remain unselected:

```text
exact state/disposition names
tables, columns, and attempt/audit schema
migration number
claim SQL and lease token/version mechanism
lease duration
numeric maxAttempts
backoff, jitter, and Retry-After values
request-ID generation format
operator API and admin UI
scheduler, worker, and queue technology
exact transaction APIs
```

## Governance state

```text
LIFEOS-LOGOS-001K-DEC-001 = APPROVED / FROZEN
HARD-004 = APPROVED / FROZEN
selected policy = POLICY B — EXPLICIT BOUNDED RECOVERY LIFECYCLE
implementation = NOT AUTHORIZED
next governance gate = LIFEOS-LOGOS-001M — HARD-006 SECRET / CONFIGURATION LIFECYCLE CONTRACT
```

The external Logos governance reference for this decision is
`e3fb855ddbcfae2e148ec39b42a06604cedf6699`. Logos is not modified by this
LifeOS decision.
