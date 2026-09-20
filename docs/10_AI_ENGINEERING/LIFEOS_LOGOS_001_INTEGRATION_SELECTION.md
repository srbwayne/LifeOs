# LIFEOS-LOGOS-001 — Reading → Logos POC Integration Selection

Status: CURRENT GOVERNANCE / POC VERIFIED / CLOSED — DOCUMENTATION ONLY

## Current canonical initiative state

`LIFEOS-LOGOS-001 — VERIFIED / CLOSED`

The first bounded real Reading → Logos POC was executed and subsequently
verified by `LIFEOS-LOGOS-001D-RECOVERY-001`. The canonical closure evidence is
`docs/10_AI_ENGINEERING/LIFEOS_LOGOS_001_POC_CLOSURE.md`.

The retained operational evidence proves one LifeOS `ReadingSession` produced
one delivered progression execution in Logos, with global XP `+3`,
`Conhecimento` XP `+3`, stress delta `0`, and an identical downstream
resubmit returning HTTP 200 without a duplicate execution or progression
application. Historical unresolved deliveries were not replayed.

## Current canonical state — source implementation closed

`LIFEOS-LOGOS-001B — IMPLEMENTED / CANONICAL / A1-CONFORMANT / CLOSED`

Canonical source: `a4e9758a553ffd924303bd8e871183314642320f`

Closure publication: `25322af61d81c3fc95253d4f2ce3c3e50b97e5f7`

PR #94 introduced the source, PR #95 was closed/not merged/superseded, PR #96
applied pinned-revision remediation, PR #97 completed final HTTP/revision
boundary conformance, and PR #98 published this closure state.

At this historical source-closure checkpoint, the implemented adapter remained
disabled by default and runtime POC activation, manual bootstrap, real HTTP,
and historical replay had not occurred. That checkpoint is preserved here for
traceability; it is not the current initiative state.

`LIFEOS-LOGOS-001C-DEC-001` subsequently froze and approved the bounded runtime
decision. The runtime execution and recovery verification are documented in
the canonical POC closure document referenced above.

## Historical selection and architecture approval

`LIFEOS-LOGOS-001A-DEC-001 — APPROVED`

The Architecture / Technical Plan is APPROVED / FROZEN at:

`docs/10_AI_ENGINEERING/LIFEOS_LOGOS_001_ARCHITECTURE_TECHNICAL_PLAN.md`

The next authorized gate at that historical checkpoint was:

`LIFEOS-LOGOS-001B — SOURCE IMPLEMENTATION`

No runtime or end-to-end validation was authorized by that historical
publication. Source implementation was subsequently completed and closed.

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

At the historical decision-freeze checkpoint, the real downstream had not yet
been activated. The completed POC preserved the boundary: historical unresolved
delivery records remained untouched, startup did not call
`dispatch_unresolved()`, and only the newly created ReadingSession delivery was
allowed to execute.

The existing terminal classification for HTTP 400 and 409 remains unchanged.
The implemented gateway classifies network failures, timeouts, 401, 403, 404,
429, and 5xx responses without changing dispatcher behavior. Only HTTP 200 is
success; unsupported 2xx responses are retryable unsupported statuses.

## Historical pre-execution prerequisites

The approved plan froze typed settings for enabled state, Logos base URL,
bearer token, Reading configuration key, required positive pinned revision, and
HTTP timeout. The implemented runtime uses `httpx==0.28.1`.

LifeOS Alembic remained `0011`; the pilot required no new migration because
`progression_delivery_records` already existed. Logos remained at Flyway
`V43`; no Logos migration was required. These were pre-execution constraints,
not an outstanding current gate.

## References

- `docs/10_AI_ENGINEERING/ACTIVITY_INVENTORY_AND_PROGRESSION_READINESS.md`
- `docs/10_AI_ENGINEERING/READ_005_OPERATIONAL_CUTOVER.md`
- `docs/03_DATABASE/MIGRATIONS.md`
- `app/read/application/services/progression_delivery_dispatcher.py`
- `app/read/infrastructure/integrations/durable_progression_gateway.py`
- `app/read/infrastructure/integrations/noop_progression_gateway.py`

The POC is now closed. Initiative priority must be re-evaluated explicitly
before any productionization work or resumption of WORK-001 architecture.
