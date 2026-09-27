# LifeOS ↔ Logos Hardening Foundation Technical Plan

## Status

```text
LIFEOS-LOGOS-HARDENING-TP-001-DEC-001 = APPROVED / FROZEN / AMENDED
LIFEOS-LOGOS-HARDENING-TP-001-DEC-001-A1 = APPROVED / FROZEN
Foundation Technical Plan = APPROVED / FROZEN
implementation = NOT AUTHORIZED
```

This document is a documentation-only implementation sequencing plan. It
does not authorize implementation, activation, bootstrap, deployment, or
operational mutation.

## Baselines and governance

The LifeOS planning baseline is `a3ba1b0d800de85b97499234b74b511ad8f0cdfe`.
The canonical remote Logos baseline is
`a1b8f936857d4b31fa39d592a63ed777524865f9`, with F1A, F1B, and F1C
canonical. The structural architecture foundation is frozen:

```text
HARD-001 / HARD-002 / HARD-003 / HARD-005 / HARD-004 / HARD-006
= ARCHITECTURE / GOVERNANCE FOUNDATION COMPLETE / FROZEN
```

Implementation remains partial. Productionization, deployment, HARD-007, and
WORK-001 remain deferred.

## Amendment A1

The original technical plan refined the remaining HARD-001 work into verifier,
replay, security integration, and trust administration. Before its
documentation canonicalization completed, Logos PR #43 became canonical and
consumed the F1C identifier for the signed workload assertion verifier.

Accordingly, this amendment reconciles the names with canonical reality:

```text
F1C = signed workload assertion verifier core (DONE)
F1D = durable replay consumption + authentication completion
F1E = Spring Security workload integration
F1F = trust administration
```

No dependency, security invariant, or activation boundary is weakened.

## Canonical slice map

| Slice | Owner | Status and invariant |
|---|---|---|
| F1A | Logos | V45 trust/replay persistence, IMPLEMENTED / CANONICAL |
| F1B | Logos | Trust domain/read adapter and P-256/SPKI validation, IMPLEMENTED / CANONICAL |
| F1C | Logos | Signed assertion verifier core, IMPLEMENTED / CANONICAL |
| F1D | Logos | Durable `issuer + jti` replay consumption and normalized authentication, PLANNED / NOT AUTHORIZED |
| F1E | Logos | Workload-only Spring Security integration, 401/503 boundary, no fallback, PLANNED / NOT AUTHORIZED |
| F1F | Logos | Administrative trust lifecycle capability, PLANNED / NOT AUTHORIZED |
| B1 | Logos | HARD-002 relational authorization persistence/domain, PLANNED / NOT AUTHORIZED |
| B2 | Logos | HARD-002 evaluator/enforcement, default deny, PLANNED / NOT AUTHORIZED |
| C1 | Logos | HARD-003 lifecycle/history persistence and legacy classification, PLANNED / NOT AUTHORIZED |
| C2 | Logos | HARD-003 enforcement and audited administration, PLANNED / NOT AUTHORIZED |
| D1 | LifeOS | HARD-005 durable delivery/attempt/correlation evidence, PLANNED / NOT AUTHORIZED |
| D2 | Logos | Additive correlation provenance/echo, PLANNED / NOT AUTHORIZED |
| E1 | LifeOS | Disabled-first workload key provider and assertion builder, PLANNED / NOT AUTHORIZED |
| E2 | LifeOS | Disabled-first workload-auth gateway integration, PLANNED / NOT AUTHORIZED |
| F | Cross-system | Explicit workload-authentication cutover, OPERATIONAL / NOT AUTHORIZED |
| G1 | LifeOS | HARD-004 bounded recovery implementation, PLANNED / NOT AUTHORIZED |
| G2 | Cross-system | Recovery activation and legacy disposition, OPERATIONAL / NOT AUTHORIZED |

F1A/F1B/F1C must not be re-planned as future work. F1C produces a
`VerifiedWorkloadAssertion`; it does not itself consume replay or establish an
authenticated workload principal.

## F1D — replay and authentication completion

F1D consumes the F1C output only after cryptographic, profile, lifecycle, and
principal-binding validation. It atomically and durably consumes replay identity
`issuer + jti`, commits that consumption independently of authorization and
progression transactions, fails closed when the replay store is unavailable,
and produces a normalized `WORKLOAD / lifeos` principal. Once consumed, a
downstream denial, rollback, or server failure must not unconsume it.

Expected content is a replay application port, PostgreSQL adapter, atomic
insert/consume result, independent transaction boundary, conflict semantics,
and authentication-completion service. V45 already supplies the replay table;
the expected migration is **NONE**. A schema defect requires a stop and a new
technical-plan review, not an unplanned V46/V47 migration.

Evidence must cover first/second consume, concurrent duplicate consume,
different issuer/jti behavior, rollback survival, database outage fail-closed,
and absence of in-memory or fallback authentication. F1D does not route real
traffic, integrate `SecurityConfig`, seed trust, or cut over LifeOS.

## F1E — workload security integration

F1E connects completed authentication to a workload-only Spring Security path.
AppUser and workload profiles are mutually exclusive. Invalid workload
assertions never fall back to AppUser JWT, POC bearer, or another mode.
External behavior is generic 401 for authentication failure and 503 when replay
store failure causes fail-closed authentication. Code canonicalization remains
distinct from real LifeOS traffic activation.

## F1F — trust administration

F1F provides explicit, authorized, audited capability for principal and
credential registration, activation, retirement, revocation, whole-workload
disablement, and trust audit. Implementing this capability is not the same as
registering a real LifeOS key; trust bootstrap remains a separate operation.

## B1/B2 — authorization

B1 persists separate principal, operation, source, and namespace constraints
with default deny. The frozen grant for `WORKLOAD / lifeos` and
`PROGRESSION_EXECUTE` is not inserted by B1. B2 evaluates all applicable
constraints after normalized authentication. No execution-read,
history-read, or subject-provisioning grant is introduced.

## C1/C2 — ownership

C1 adds lifecycle, provenance/verification state, proof/evidence reference,
history, disable/revoke, tombstone, transfer/correction, and legacy
classification without inventing proof or actors for existing non-native rows.
C2 enforces ACTIVE valid ownership, idempotent identical bindings, takeover
conflict, no silent overwrite, concurrency safety, and audited administration.
LifeOS receives no subject-provisioning grant.

## D1/D2 — correlation

D1 is the LifeOS-owned evidence foundation for stable `deliveryId`, monotonic
`attemptNumber`, unique `requestId`, original source/idempotency identity,
configuration key/revision, timestamps, outcomes, bounded errors, latency,
endpoint category, and future credential `kid`. Correlation never changes the
business fingerprint. D1 requires a new Alembic revision at implementation
time. D2 accepts additive correlation provenance/echo in Logos only where
appropriate and never changes progression identity or fingerprint; a migration
is conditional on its chosen persistence design.

## E1/E2 — disabled-first signer path

E1 defines the bounded signing-key provider, PKCS#8 P-256 loading, ES256
assertion construction, fresh jti, frozen issuer/audience, 60-second lifetime,
startup validation, and safe representations. E2 connects it to the gateway
while disabled. Both preserve the POC bearer path until an explicit cutover.
Each retry keeps deliveryId, source, idempotencyKey, and business facts while
creating a new attempt number, requestId, assertion, and jti. Tests use only
ephemeral isolated credentials.

## Operational boundaries

Bootstrap is three separate controlled operations:

```text
T1 TRUST: register/activate the real LifeOS public credential
T2 AUTHORIZATION: activate only PROGRESSION_EXECUTE for lifeos/lifeos
T3 OWNERSHIP: establish/verify required HARD-003 state
```

None is authorized by this plan. Cutover F is operational and requires F1D,
F1E, F1F as needed, B1/B2, C1/C2, D1/D2, E1/E2, trust/authorization/
ownership readiness, green cross-repository tests and CI, and no hidden
fallback. POC bearer retirement is part of that explicit cutover.

G1 implements bounded HARD-004 recovery only after durable D1 evidence and
security/revalidation foundations: maxAttempts, reservation before HTTP,
lease/expiry and stale-worker protection, lifecycle/disposition states,
timing, ambiguity, audit, and `RELEASE_SUCCESSORS`. G2 separately authorizes
legacy disposition or recovery activation. Neither permits automatic
redispatch, replay, backfill, or scheduler creation.

## Dependency DAG and parallelization

The serialized Logos critical path is:

```text
F1A → F1B → F1C → F1D → F1E → F1F → B1 → B2 → C1 → C2
```

D1 and E1 are safe parallel candidates after separate authorization when their
file allowlists and migrations do not overlap and all cross-system contracts
remain frozen. D2 follows the additive contract as needed; E2 follows E1.
F, G1, and G2 are cutover/activation boundaries, not automatic continuations.
Overlapping Logos work in workload security, `SecurityConfig`, progression or
subject controllers, and the Flyway directory must be serialized; only the
canonical remote main is evidence.

## Migration and ownership policy

No future migration number is reserved. Each implementation pre-flight reads
the then-current canonical head and uses the next available LifeOS Alembic or
Logos Flyway revision. A repository migration must leave that repository valid
independently; no cross-repository transaction is assumed.

```text
LifeOS provider/signer and delivery/recovery = LifeOS
trust, verification, replay, authorization, ownership, execution truth = Logos
correlation contract = cross-system
deployment technology = HARD-007
real bootstrap = controlled operations
```

## Compatibility, tests, and activation gates

Prefer additive, inactive-first commits: schema before activation, verifier
before routing, signer before cutover, and recovery schema before activation.
Tests must cover replay races/rollback, assertion negatives, strict profile
separation, authorization matrices, ownership lifecycle and concurrency,
correlation fingerprint regression, attempt/lease races, and cross-repository
HTTP contracts including 401, 403, 404, 409, 429, 5xx, and 503 replay-store
failure. No CI test uses operational secrets.

Implementation approval, merge, bootstrap, cutover, recovery activation, and
HARD-007 deployment approval are separate decisions. Historical deliveries are
evidence only and are not replayed or rewritten.

## First implementation candidate and next gate

The first primary candidate after this plan is canonical is:

```text
LOGOS-HARD-001-F1D
DURABLE ASSERTION REPLAY CONSUMPTION + AUTHENTICATION COMPLETION
```

This plan does not authorize it. The next gate is
`LOGOS-HARD-001-F1D-IA-001`, a read-only implementation authorization /
pre-flight review to verify the then-current Logos baseline, writer overlap,
V45 schema, F1C boundary, exact allowlist, independent transaction semantics,
normalized principal boundary, test evidence, and migration necessity.

```text
HARD-007 = DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER
WORK-001 = DEFERRED
implementation = NOT AUTHORIZED
```
