# LIFEOS-LOGOS-001G — Cross-System Hardening Architecture / Scope

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001G-DEC-001`.

This document freezes the minimum reusable cross-system hardening foundation
for future LifeOS ↔ Logos integrations. It is an architecture and governance
boundary, not an implementation authorization. Reading → Logos remains a
verified bounded POC; productization remains unauthorized.

## Decision chronology

- `LIFEOS-LOGOS-001G`: **BLOCKED / HISTORICAL** because the Logos canonical
  baseline advanced.
- `LIFEOS-LOGOS-001G-R1`: **PASS** — foundation proposed against the updated
  baseline.
- `LIFEOS-LOGOS-001G-R1-A1`: **PASS** — dependency graph reconciled; minimum
  correlation precedes recovery.
- `LIFEOS-LOGOS-001G-DEC-001`: **APPROVED / FROZEN**.

No production readiness, productization, source change, migration, runtime,
or operational database change is authorized by this decision.

## Frozen foundation

The immediate `FOUNDATION_REQUIRED` capabilities are:

1. **HARD-001 — Workload Trust Contract**
2. **HARD-002 — Source / Namespace / Operation Authorization Boundary**
3. **HARD-003 — External Subject Ownership Lifecycle**
4. **HARD-005 — Minimum Cross-System Correlation Contract**
5. **HARD-004 — Bounded Delivery Recovery Policy**
6. **HARD-006 — Secret and Configuration Lifecycle Contract**

**HARD-007 — Deployment Boundary Contract** is deferred as
`PRODUCTIONIZATION_REQUIRED_LATER`.

## Corrected dependency graph

```text
HARD-001 — Workload Trust
    ↓
HARD-002 — Authorization Boundary
    ↓
HARD-003 — Subject Ownership
    ↓
HARD-005 — Minimum Correlation Contract
    ↓
HARD-004 — Bounded Recovery Policy

HARD-001
    ↓
HARD-006 — Secret / Configuration Lifecycle

HARD-001 + HARD-005 + HARD-006
    ↓
HARD-007 — Deployment Boundary (deferred)
```

HARD-005 and HARD-006 are independent branches after the trust foundation.
HARD-005 still depends on HARD-001, HARD-002, and HARD-003; it cannot bypass
authorization or subject ownership. HARD-004 depends on the resulting minimum
correlation contract.

Gate identifiers are not execution order. The frozen execution order is:

```text
001H → 001I → 001J → 001L → 001K
001H → 001M
001N remains deferred and depends on the relevant trust, correlation, and
secret/configuration architecture.
```

## Workload trust invariants

Production service calls must not depend on a human AppUser identity. A future
workload identity must be stable, distinct from a human, auditable, revocable,
rotatable, least-privilege, and bindable to allowed sources, namespaces, and
operations. Human password reuse and credentials embedded in source are
prohibited. The concrete mechanism is not selected; OIDC, OAuth client
credentials, mTLS, API keys, self-signed service JWTs, service-account
passwords, and cloud IAM remain alternatives for a later technical gate.

## Authorization boundary

Authentication alone is insufficient. An authenticated workload must be
authorized for the source, subject namespace, and operation. The initial LifeOS
policy is `source=lifeos`, `subject.namespace=lifeos`, and external progression
execution. Arbitrary source or namespace impersonation is prohibited.
Provisioning, execution, exact-read, and history permissions must be treated as
separate operations. The concrete Spring/security implementation is undecided.

## Subject ownership boundary

The existing subject mapping proves resolution, not external ownership. A
supported lifecycle must prevent namespace takeover, unauthorized external-ID
provisioning, unauthorized mapping use, and reassignment. Provisioning and use
must be attributable to an authorized workload or operator. Automatic bootstrap
is not authorized; the API and schema mechanism remain technical-plan topics.

## Minimum correlation and privacy boundary

HARD-005 freezes only the minimum contract needed to identify delivery,
attempt, downstream execution, and operator action before recovery:

Required fields:

- LifeOS delivery ID;
- `source` and `idempotencyKey`;
- configuration key and revision;
- attempt number;
- failure classification;
- downstream HTTP outcome;
- correlation/request ID.

Subject namespace/external ID is permitted only in access-controlled
telemetry/audit stores. It must not become unrestricted telemetry or a blind
metric label. Timestamps, latency, endpoint identity, and bounded diagnostic
reason are optional.

JWTs, bearer tokens, passwords, signing secrets, credential contents, and
unrestricted sensitive payload data are prohibited. High-cardinality/private
identifiers such as external IDs, idempotency keys, and delivery IDs require
controlled structured logs or audit stores rather than indiscriminate metric
labels. Distributed tracing, dashboards, and vendor selection are deferred.

## Recovery ownership and policy

LifeOS owns the durable delivery lifecycle: eligibility, attempts, retry budget,
next-attempt/disposition state, operator recovery entry point, terminal
disposition, and delivery-side audit. Logos owns durable execution truth,
execution idempotency, canonical fingerprint, conflict behavior, and persisted
outcome. Cross-system policy governs interpretation of Logos outcomes,
configuration/revision compatibility, correlation, and evidence required for
recovery.

LifeOS must not rewrite or delete Logos execution history, change an existing
idempotency identity, or silently reinterpret a historical delivery under a new
semantic contract.

Minimum recovery is **policy plus state model**, not an automatic scheduler.
The later design must include bounded retry budget, retry timing state,
explicit terminal/quarantine disposition, operator audit,
configuration/revision guard, and a concurrency-safe claim/lease or equivalent.
Terminal disposition is a LifeOS operational action requiring authorized
identity, reason, timestamp, previous state, selected disposition,
configuration/revision identity, and audit evidence. It does not delete
historical evidence.

Historical replay remains unauthorized.

## Secret and configuration lifecycle

HARD-006 requires external secret injection, no repository persistence, no
source-code credential, rotation without source modification, revocation or
expiry semantics, environment separation, credential identity auditability,
and controlled restart/reload behavior. No secret-management product or
deployment technology is selected.

## Attribute identity and durable outcomes

`Atributo.semanticKey` is integrated. `Conhecimento` remains the display/domain
attribute and `knowledge` the semantic catalog identity. Progression HTTP V1
continues to use UUID keys; `semanticKey` is additive nullable metadata.

New durable executions capture semantic identity at completion. Replay, exact
read, and history read the persisted snapshot. Legacy executions may expose a
null semantic key. No live catalog re-resolution during replay is a required
compatibility invariant. No further semantic-key implementation is part of
this immediate foundation.

## Idempotency compatibility

`source + idempotencyKey` remains the execution identity. The same identity and
fingerprint must return the persisted outcome without duplicate progression;
changed payloads must conflict without mutation. Recovery preserves the
original execution identity, and credential rotation must not alter it.

## Deferred scope

HARD-007 remains deferred until supported non-loopback/production-like
deployment. It must later address TLS outside trusted loopback,
environment-specific endpoints, bounded timeouts, readiness, failure
isolation, and credential injection.

Also deferred are distributed tracing, automated schedulers, queue/worker
infrastructure, advanced dead-letter transport, high-scale recovery,
production secret-manager selection, deployment topology, TLS certificate
implementation, and service discovery implementation.

Explicitly out of scope: Reading XP or configuration redesign, `Conhecimento`
changes, semantic-key HTTP V1 migration, frontend, WORK-001, Noema, Home
Assistant, multi-activity rollout, automatic historical replay, cloud-provider
selection, Kubernetes, service mesh, Kafka, RabbitMQ, and production deployment
implementation.

## Follow-up gates

- `001H` — Workload Identity / Trust Architecture — authorized next gate,
  read-only, not executed.
- `001I` — Source / Namespace / Operation Authorization — not authorized.
- `001J` — Subject Ownership Lifecycle — not authorized.
- `001K` — Delivery Recovery Architecture — not authorized.
- `001L` — Correlation / Observability Architecture — not authorized.
- `001M` — Secret / Configuration Lifecycle — not authorized.
- `001N` — Deployment Boundary Architecture — deferred and not authorized.

## Non-authorization

This freeze authorizes no source, test, migration, runtime, database,
progression, replay, recovery, observability, security, deployment, or
productization work. WORK-001 remains approved/frozen/deferred. The Reading →
Logos POC remains verified/closed, and its historical evidence is unchanged.
