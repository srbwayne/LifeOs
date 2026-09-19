# LIFEOS-LOGOS-001 — Reading → Logos POC Integration Selection

Status: CURRENT GOVERNANCE / SOURCE RATIFICATION — DOCUMENTATION ONLY

## Current canonical state — source implementation ratified

`LIFEOS-LOGOS-001B — SOURCE IMPLEMENTATION: COMPLETE / CANONICAL`

Canonical source: `a4e9758a553ffd924303bd8e871183314642320f`

PR sequence: #94 merged, #95 closed/not merged/superseded, #96 merged, and #97
merged. Post-merge Quality Gates `35409223058` passed 3/3 on `main`.

The implemented adapter remains disabled by default. Runtime POC activation,
manual subject/configuration bootstrap, real HTTP, and historical replay have
not occurred.

When enabled, the adapter requires a positive pinned configuration revision and
uses the canonical Reading payload: `lifeos` subject identity, `lifeos` source,
`reading-session:<ReadingSessionId>` idempotency, and the `pages_read` fact.
Only HTTP 200 is success; unsupported 2xx responses are retryable.

The next gate is:

`LIFEOS-LOGOS-001C — CONTROLLED POC BOOTSTRAP / E2E VALIDATION`

This document does not authorize operational actions at that gate.

## Historical selection and architecture approval

`LIFEOS-LOGOS-001A-DEC-001 — APPROVED`

The Architecture / Technical Plan is APPROVED / FROZEN at:

`docs/10_AI_ENGINEERING/LIFEOS_LOGOS_001_ARCHITECTURE_TECHNICAL_PLAN.md`

The next authorized gate at that historical checkpoint was:

`LIFEOS-LOGOS-001B — SOURCE IMPLEMENTATION`

No runtime or end-to-end validation was authorized by that historical
publication. Source implementation was subsequently completed through PRs
#94, #96, and #97.

## Decision

The Product Owner selected the first bounded real LifeOS → Logos integration
before continuing WORK-001 architecture work. The selected activity is
`ReadingSession`. WORK-001 remains approved and frozen at Product Contract
level; it is temporarily deferred at its architecture gate, not cancelled or
rejected.

The next authorized gate at that historical checkpoint was:

`LIFEOS-LOGOS-001A — READING → LOGOS POC ARCHITECTURE / TECHNICAL PLAN`

LIFEOS-LOGOS-001G authorized no source, tests, migration, runtime, or
operational-database work.

## Evidence for the selected activity

Canonical LifeOS already contains:

- implemented `ReadingSession` with stable `ReadingSessionId` TSID identity;
- derived `pages_read` as the concrete approved progression fact;
- atomic persistence of a progression delivery intent with the ReadingSession;
- `progression_delivery_records` at Alembic `0011`;
- `ProgressionGateway`, `DurableProgressionGateway`, and
  `ProgressionDeliveryDispatcher`;
- explicit `dispatch_unresolved()` recovery;
- `NoOpProgressionGateway` as the current default downstream;
- no activated real Logos downstream.

The LifeOS-owned semantic occurrence for this pilot is:

`reading.session.completed`

Only `pages_read` is approved for the progression payload. Notes, book title,
author, reading insights, coverage, completion metadata, and facts from other
domains are excluded.

## Authority boundary

LifeOS owns the observed reading fact. Logos owns progression interpretation,
including XP, attribute distribution, stress, and skill-policy rules.

The Logos configuration key and required positive pinned revision are
integration configuration concerns, not ReadingSession domain facts.

The implemented adapter targets the supported Logos HTTP V1 execution resource:

```http
POST /api/internal/v1/progression/executions
```

The POC integration identity is:

```text
subject.namespace = lifeos
subject.externalId = canonical LifeOS UserId TSID
execution.source = lifeos
idempotencyKey = reading-session:<ReadingSessionId>
```

The idempotency value is transport/integration identity and must not be added
to the ReadingSession aggregate.

Before delivery, the intended LifeOS user must be linked in Logos through the
POC subject-provisioning endpoint:

```http
POST /api/internal/v1/progression/subject-identities
```

This is a one-time manual bootstrap for the POC, not automatic LifeOS-driven
provisioning.

## POC trust boundary

Logos is pre-production. The POC temporarily uses the current Logos AppUser
JWT mechanism. Dedicated service principals, OIDC, API keys, source
authorization, namespace authorization, cross-service read authorization, and
external identity ownership proof remain production-hardening debt.

The POC must not be described as production-ready authentication.

## Delivery and durability boundary

The implementation preserves the existing chain:

```text
CreateReadingSessionCommandHandler
    → DurableProgressionGateway
    → ProgressionDeliveryDispatcher
    → LogosProgressionGateway
    → Logos HTTP V1
```

The dispatcher remains responsible for `progression_delivery_records` status
transitions, attempt counts, failure classification, and delivery completion.
LifeOS delivery remains at-least-once. Logos execution idempotency provides
downstream duplicate protection; it does not make source delivery exactly-once.

The real downstream is not activated by this decision. Historical unresolved
delivery records must remain untouched. Startup must not automatically call
`dispatch_unresolved()`. The first pilot may attempt delivery for a new
ReadingSession; historical recovery requires a separate explicit review.

The existing terminal classification for HTTP 400 and 409 remains unchanged.
The implemented gateway classifies network failures, timeouts, 401, 403, 404,
429, and 5xx responses without changing dispatcher behavior.

## Implementation prerequisites to resolve at the next gate

The approved plan froze typed settings for enabled state, Logos base URL,
bearer token, Reading configuration key, required positive pinned revision, and
HTTP timeout. The implemented runtime uses `httpx==0.28.1`.

LifeOS Alembic remains `0011`; this pilot is expected to require no new
migration because `progression_delivery_records` already exists. Logos remains
at Flyway `V43`; no Logos migration is expected.

## References

- `docs/10_AI_ENGINEERING/ACTIVITY_INVENTORY_AND_PROGRESSION_READINESS.md`
- `docs/10_AI_ENGINEERING/READ_005_OPERATIONAL_CUTOVER.md`
- `docs/03_DATABASE/MIGRATIONS.md`
- `app/read/application/services/progression_delivery_dispatcher.py`
- `app/read/infrastructure/integrations/durable_progression_gateway.py`
- `app/read/infrastructure/integrations/noop_progression_gateway.py`

After the bounded pilot closes, initiative priority must be re-evaluated
explicitly before resuming WORK-001 architecture work.
