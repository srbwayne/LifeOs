# LIFEOS-LOGOS-001 — Reading → Logos POC Architecture / Technical Plan

Status: APPROVED / FROZEN / AMENDED
Amendment: `LIFEOS-LOGOS-001A-A1-DEC-001 — APPROVED`
Decision: `LIFEOS-LOGOS-001A-DEC-001 — APPROVED`
Baseline: `41e93cd5381e9497461943994dbfd0daed6dd7ae`
Source implementation: COMPLETE / CANONICAL
Canonical source: `a4e9758a553ffd924303bd8e871183314642320f`
Next gate: `LIFEOS-LOGOS-001C — CONTROLLED POC BOOTSTRAP / E2E VALIDATION`

This is the canonical Architecture / Technical Plan for the bounded Reading →
Logos POC. The source implementation is now canonical. This document does not
activate runtime, database access, subject bootstrap, or historical delivery
replay.

## 1. Purpose and frozen boundaries

```text
ReadingSession
  → durable LifeOS progression delivery
  → LogosProgressionGateway
  → Logos progression execution
```

The LifeOS semantic occurrence is `reading.session.completed` and the only
approved progression fact is `pages_read`. Notes, book metadata, insights,
coverage, BookCompletion metadata, and other capability facts are excluded.
LifeOS owns the observed reading fact; Logos owns progression interpretation,
XP, attributes, skills, stress, levels, and configuration rules.

The supported resource is:

```http
POST /api/internal/v1/progression/executions
```

Subject linking is a manual, one-time POC operation through:

```http
POST /api/internal/v1/progression/subject-identities
```

Integration identity is `namespace=lifeos`, the canonical LifeOS UserId TSID as
`externalId`, `source=lifeos`, and
`reading-session:<ReadingSessionId>` as idempotency key. The key is integration
metadata, not a ReadingSession domain field. Current Logos AppUser JWT
authentication is POC/pre-production only.

## 2. Architecture decisions

### 2.1 Existing delivery chain

Preserve:

```text
CreateReadingSessionCommandHandler
  → DurableProgressionGateway
  → ProgressionDeliveryDispatcher
  → ProgressionGateway
```

The downstream gateway becomes `LogosProgressionGateway` only when explicitly
enabled with valid configuration. Preserve the existing atomic
`ReadingSession + ProgressionDeliveryIntent` transaction, post-commit
dispatch, at-least-once delivery, and explicit `dispatch_unresolved()`
recovery. The dispatcher and delivery repository are not modified by this
plan.

### 2.2 Synchronous adapter

Use `LogosProgressionGateway` with synchronous `httpx.Client`. The existing
gateway, dispatcher, and handlers are synchronous; no `AsyncClient` or async
conversion is introduced. The adapter owns request construction, Bearer
authentication, finite timeout, supported response parsing, semantic error
classification, and safe logging. Tokens are never logged, committed, or
returned in application errors.

### 2.3 Typed configuration and wiring

`LogosProgressionSettings` is the typed infrastructure boundary for:

```text
LIFEOS_LOGOS_PROGRESSION_ENABLED
LIFEOS_LOGOS_BASE_URL
LIFEOS_LOGOS_BEARER_TOKEN
LIFEOS_LOGOS_READING_CONFIGURATION_KEY
LIFEOS_LOGOS_READING_CONFIGURATION_REVISION
LIFEOS_LOGOS_TIMEOUT_SECONDS
```

Disabled (`false`, the safe default) selects `NoOpProgressionGateway`.
Enabled (`true`) requires valid URL, nonblank bearer token, nonblank Reading
configuration key, and finite timeout greater than zero. Invalid or incomplete
enabled configuration fails fast; it never silently falls back to NoOp.
Revision is required when enabled, has no default, and must be an integer
greater than or equal to 1. The enabled adapter must never send `revision=null`.
Environment variables are read only by the configuration boundary.

`httpx==0.28.1` is promoted to `[project].dependencies`; its duplicate test
extra declaration is removed during implementation. `requirements.txt` stays
semantically synchronized and is not otherwise changed.

### 2.4 Failure semantics and recovery

Existing status, error, attempt-count, and last-attempt fields are sufficient;
no delivery schema change is planned. The adapter supplies stable
`ProgressionGatewayError` classifications without production dispatcher or
repository changes:

| Response/failure | Category | Recovery |
|---|---|---|
| HTTP 400 | TERMINAL (`http_status_400`) | excluded |
| HTTP 401 | RECOVERABLE_OPERATOR_ACTION | explicit recovery |
| HTTP 403 | RECOVERABLE_OPERATOR_ACTION | explicit recovery |
| HTTP 404 | RECOVERABLE_OPERATOR_ACTION | explicit recovery |
| HTTP 409 idempotency conflict | TERMINAL (`http_status_409`) | excluded |
| HTTP 409 configuration inactive | RECOVERABLE_OPERATOR_ACTION | explicit recovery |
| Unknown HTTP 409 | TERMINAL | excluded |
| HTTP 429 | RETRYABLE | explicit recovery |
| HTTP 5xx | RETRYABLE | explicit recovery |
| Network/DNS/connect failure | RETRYABLE | explicit recovery |
| Timeout | RETRYABLE | explicit recovery |

Recoverable operator-action failures are failed but nonterminal and remain
eligible for `dispatch_unresolved()` after remediation. There is no automatic
startup replay. Same source and key with the same fingerprint returns Logos
200 without a second mutation; a different fingerprint is a terminal conflict.
Source delivery remains at-least-once, never exactly-once.

### 2.5 Payload boundary

Map the supported Logos request to the subject, source, idempotency key,
configured progression key/revision, and one detail:

```text
factorKey = pages_read
value = ReadingSession.pages_read
```

The LifeOS semantic occurrence remains `reading.session.completed`; the
current Logos body has no independent occurrence-type field. Notes, book
metadata, Health facts, and unrelated capability facts do not cross the
boundary. No XP or progression rule is implemented in LifeOS.

### 2.6 Manual operations

Subject bootstrap is manual only. A same-owner repeated mapping is idempotent
(200); an ownership conflict is 409
`PROGRESSION_SUBJECT_IDENTITY_CONFLICT`. A later, separately authorized E2E
gate may link one user, configure progression, create one new ReadingSession,
verify one delivery record and one Logos execution, repeat the same identity
for idempotent 200, and verify `DELIVERED`. Historical unresolved records
remain untouched.

## 3. Technical Plan

### 3.1 Exact implementation allowlist

New production:

```text
app/read/infrastructure/integrations/logos_progression_gateway.py
app/read/infrastructure/integrations/logos_progression_settings.py
```

Modified production/configuration:

```text
app/read/dependencies.py
pyproject.toml
```

Documentation:

```text
docs/04_BACKEND/CONFIGURATION.md
```

Tests:

```text
tests/read/infrastructure/integrations/test_logos_progression_gateway.py
tests/read/infrastructure/integrations/test_logos_progression_settings.py
tests/read/application/test_read_dependencies.py
tests/read/application/test_progression_delivery_dispatcher.py
```

Exactly nine paths were authorized and are now the bounded implementation
allowlist. The production dispatcher,
`progression_delivery_repository.py`, `requirements.txt`, and migrations are
not in the allowlist.

### 3.2 Implementation result

1. Typed settings, disabled default, enabled fail-fast validation, runtime
   `httpx` dependency, and configuration documentation were implemented.
2. The synchronous gateway, supported request mapping, Bearer header, finite
   timeout, safe logging, and semantic failure classifications were implemented.
3. DI wiring preserves disabled → NoOp and valid enabled → Logos gateway;
   invalid enabled configuration fails fast.
4. Settings, gateway, payload, HTTP matrix, semantic 409, DI, secret-handling,
   and recovery-eligibility tests were implemented without changing dispatcher
   production code.
5. Manual subject/bootstrap and one-session E2E POC remain a separate runtime
   authorization gate.

### 3.3 Migration and database boundary

LifeOS remains at Alembic `0011`; Logos evidence remains at Flyway `V43`.
Neither repository requires a migration for this adapter because existing
`progression_delivery_records` provides durable Reading delivery. No
operational database access or historical backfill is part of this plan.

### 3.4 Test contract

Future tests cover settings disabled/enabled/invalid cases; complete payload
mapping; Bearer authentication; finite timeout; secret exclusion from
repr/log/error; network and timeout failures; HTTP 400, 401, 403, 404, 409
idempotency conflict, 409 configuration inactive, unknown 409, 429, and 5xx;
DI selection; and recovery eligibility versus terminal exclusion. Existing
dispatcher behavior is tested through its current interfaces, not changed for
this POC.

## 4. Deferred runtime and hardening

This publication does not start a runtime, make an HTTP call, provision a
subject, replay history, or activate the real downstream. It does not
authorize WORK-001 architecture or implementation. WORK-001 remains Product
Contract APPROVED / FROZEN, temporarily deferred at its Architecture gate,
with implementation unauthorized.

Production hardening remains outside the POC: service identity/OIDC or
equivalent, source and namespace authorization, external identity ownership
proof, token rotation, and cross-service authorization. After the POC closes,
initiative priority must be explicitly re-evaluated; WORK-001 does not resume
automatically.

## 5. Approval and next gate

`LIFEOS-LOGOS-001A-DEC-001 — APPROVED` freezes this Architecture / Technical
Plan. The next authorized gate is:

```text
LIFEOS-LOGOS-001C — CONTROLLED POC BOOTSTRAP / E2E VALIDATION
```

Runtime validation, subject/configuration bootstrap, and historical recovery
remain unauthorized until that gate is separately opened.

## 6. Amendment A1 — pinned configuration revision

`LIFEOS-LOGOS-001A-A1-DEC-001 — APPROVED` amends only configuration-revision
determinism. Logos includes `configuration.key` and `configuration.revision`
in the execution fingerprint. A null revision resolves through Logos' current
active version, so an unresolved delivery could change progression semantics
after a Logos activation change. That behavior is not acceptable for this
durable POC.

When `LIFEOS_LOGOS_PROGRESSION_ENABLED=true`,
`LIFEOS_LOGOS_READING_CONFIGURATION_REVISION` is required, has no default, and
must be a positive integer. Every enabled request includes the explicit key and
revision; `revision=null` is prohibited.

The configured key and revision must remain unchanged while any recoverable
delivery is unresolved: `PENDING` or `FAILED` with a nonterminal
classification. This operational invariant preserves deterministic retry
fingerprints without changing the delivery schema. A future unattended
rotation design may persist configuration selection in the delivery record;
that design is outside this POC.

The no-migration decision remains valid: LifeOS Alembic `0011`, Logos Flyway
`V43`, and no schema change. HTTP 200 is success without persisting the Logos
response; unsupported 2xx responses such as 201, 202, and 204 are retryable
unsupported statuses. HTTP 400 remains terminal; HTTP 409 with
`PROGRESSION_CONFIGURATION_NOT_ACTIVE` is recoverable operator action, while
an idempotency or unknown 409 remains terminal. Error bodies are inspected only
as needed for that semantic distinction and are never persisted wholesale.

For this bounded POC the gateway owns a context-managed synchronous
`httpx.Client` per `record(...)` call. No application-lifespan client or
`app_factory.py` change is required. The exact nine-path implementation
allowlist remains unchanged, and the source implementation is complete/canonical
at the SHA recorded above. Runtime POC actions remain outside this amendment.
