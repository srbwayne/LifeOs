# LIFEOS-LOGOS-001L — Minimum Cross-System Correlation Contract

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001L-DEC-001`.

This is a governance and architecture record only. It authorizes no source,
HTTP, schema, migration, logging, metrics, tracing, recovery, credential,
runtime, replay, deployment, or productization work.

## Selected model

The selected model is **Option B — stable delivery-root correlation plus
per-attempt request identity**.

The contract correlates a LifeOS durable delivery, each outbound attempt, the
HTTP exchange, and the corresponding Logos durable execution without changing
the progression business identity.

## Identity taxonomy

The business execution identity is:

```text
source + idempotencyKey
```

For the bounded Reading integration:

```text
source = lifeos
idempotencyKey = reading-session:<ReadingSessionId>
```

This identity is stable across retries and remains the basis of Logos
idempotency. It is distinct from:

```text
deliveryId != idempotencyKey
requestId != idempotencyKey
attemptNumber != idempotencyKey
```

The durable LifeOS Delivery ID is the canonical correlation root. No second
root UUID representing the same delivery lifecycle is selected.

Each attempt is conceptually identified by:

```text
deliveryId + attemptNumber + requestId
```

`attemptNumber` is the monotonic LifeOS delivery sequence. `requestId` is new
for every concrete outbound HTTP invocation. Neither is the Logos internal
execution attempt count.

## Responsibility boundaries

```text
authentication != authorization
authorization != ownership
correlation != authentication
correlation != authorization
correlation != ownership
correlation != business idempotency
```

HARD-001 authenticates `WORKLOAD / lifeos`; HARD-002 authorizes operations,
source, and namespace; HARD-003 governs external-subject ownership; HARD-005
provides operational linkage and evidence only.

## HTTP propagation and echo

Correlation metadata crosses LifeOS to Logos through additive HTTP headers.
Headers convey sufficient information for:

```text
delivery ID / correlation root
attempt number
request ID
```

The business body remains responsible for subject, execution identity,
configuration, and progression facts. Exact header names and request-ID format
are technical-plan decisions. Correlation fields do not participate in the
canonical progression fingerprint.

Logos should echo the delivery/correlation root and request ID through additive
response metadata when the request reaches Logos. Echo is diagnostic evidence,
not proof of authorization or mutation, and cannot exist when the connection,
timeout, or network fails before a response is available. Exact response header
names remain unselected.

## Durable evidence

LifeOS is the canonical owner of the complete outbound attempt history. Future
implementation must preserve, per attempt, at least:

```text
delivery ID
attempt number
request ID
source and idempotencyKey
requested configuration key and revision
attempt start and completion timestamps, or equivalent
endpoint category
HTTP status when a response exists
normalized outcome/failure classification
bounded Logos error code when safely available
bounded diagnostic reason
latency / elapsed duration
```

The current single `attempt_count` and `last_error` fields are not the final
HARD-005 evidence model. Exact persistence schema is unselected.

The requested configuration key and revision must remain durably knowable so a
later recovery cannot silently reinterpret a delivery using current settings.
Raw response bodies are not required and unrestricted payload persistence is
not authorized.

Logos remains the owner of canonical progression execution truth. A future
Logos implementation should persist the stable LifeOS delivery ID/correlation
root as provenance, without making it part of business execution identity.
Logos is not required by this decision to create a separate execution for each
retry. Any inbound-attempt audit is separate from
`progression_external_execution` and remains technical-plan scope.

The Logos internal execution UUID remains useful internal/operator evidence,
but LifeOS is not required to receive or persist it in the initial contract.
The canonical lookup identity remains `source + idempotencyKey`.

## Ambiguous outcomes and read authority

The contract recognizes timeout after possible downstream commit, lost
responses, persistence failure after HTTP success, and process failure between
the response and LifeOS state update. Correlation makes these cases diagnosable
but does not prove whether Logos committed.

HARD-005 grants no read authority. In particular, LifeOS retains no grants for:

```text
PROGRESSION_EXECUTION_READ
PROGRESSION_HISTORY_READ
```

Future operator-controlled exact read, narrow reconciliation, or an explicitly
approved workload read grant are separate decisions. An idempotent POST retry
may recover a stored original outcome in some cases, but is not a general read
capability.

Future HARD-004 operator actions must be attributable to delivery ID, business
execution identity, relevant attempt/request identity, configuration key and
revision, authorized operator principal, timestamp, and reason/action. No
operator API is selected here.

## Privacy and cardinality

Low-sensitivity operational fields include source, attempt number, HTTP status
or status class, failure classification, outcome category, and endpoint
category.

Controlled high-cardinality fields include delivery ID, idempotency key,
correlation root, request ID, and Logos execution UUID. Subject namespace and
external ID are private subject identifiers. Workload principal and key
identity are controlled security metadata.

JWT/assertion contents, bearer tokens, private keys, signing secrets, passwords,
client secrets, credential contents, raw unrestricted payloads, and unrestricted
response bodies are never telemetry fields.

Ordinary metric labels must not contain delivery ID, idempotency key,
correlation/request IDs, subject external ID, or Logos execution UUID. Metrics
may use bounded dimensions such as source, operation, endpoint category,
failure classification, outcome category, and HTTP status class. Configuration
keys require separate bounded-cardinality approval.

Future structured diagnostic events may contain controlled correlation fields,
status, outcome, bounded reason, latency, and timestamps. Subject identifiers
require stricter access control. Exact log schemas remain unselected.

Distributed tracing is deferred. Correlation semantics work without
OpenTelemetry, traceparent, a tracing vendor, or a hosted tracing service.

## Existing state and approved direction

### Exists today

LifeOS has delivery ID, ReadingSession ID, owner ID, delivery status,
`attempt_count`, `last_error`, attempt timestamps, and delivered timestamp. It
derives source and idempotency key in the outbound payload.

Logos has durable execution UUID, source/idempotency identity, request
fingerprint, request/response snapshots, subject identity, configuration
references, processing status, internal attempt count, and timestamps.

### Missing today

The systems lack cross-system correlation metadata, per-attempt request IDs,
durable LifeOS attempt history, durable HTTP outcome evidence, durable LifeOS
configuration binding, delivery-ID propagation to Logos, Logos correlation-root
provenance, and authoritative LifeOS downstream read permission.

### Deferred

The following remain technical-plan or later decision scope:

```text
exact schema and migrations
header names and request-ID format
response metadata contract tests
logging schema and metric names
tracing implementation
Logos inbound-attempt audit schema
operator/reconciliation API
new HARD-002 read grant
Logos UUID exposure
```

## Compatibility and inherited constraints

Additive request and response headers are the intended HTTP V1-compatible
direction. The progression business body, `source + idempotencyKey`, request
fingerprint, and idempotent retry semantics remain unchanged.

HARD-004 must preserve delivery ID as correlation root, unchanged business
idempotency, per-attempt request identity, durable attempt evidence,
configuration identity, privacy/cardinality limits, and execute-only workload
authority unless separately amended.

HARD-006 remains separate; this decision does not select secret management,
key generation, rotation, injection, or reload behavior.

## Governance state

```text
LIFEOS-LOGOS-001L-DEC-001 = APPROVED / FROZEN
HARD-005 = APPROVED / FROZEN
selected option = OPTION B — STABLE DELIVERY-ROOT PLUS PER-ATTEMPT REQUEST IDENTITY
implementation = NOT AUTHORIZED
next governance gate = LIFEOS-LOGOS-001K — HARD-004 BOUNDED DELIVERY RECOVERY POLICY
```

The canonical Logos governance baseline referenced by this decision is
`b5a0a12933a04cfce29b97bb6080076edb963470`; its advancement from
`d3b9bd3aebceac1bc56799eaeffa314ec341c380` was documentation-only governance
canonicalization. Logos is not modified by this LifeOS decision.
