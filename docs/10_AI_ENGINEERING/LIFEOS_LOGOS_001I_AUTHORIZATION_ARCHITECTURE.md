# LIFEOS-LOGOS-001I — Source / Namespace / Operation Authorization Architecture

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001I-DEC-001`.

This document canonizes the human decision for HARD-002. It is an architecture
and governance record only; it authorizes no implementation, migration, runtime
change, credential activity, progression, replay, recovery, or productization.

## Decision

The selected model is **Option A — Logos-managed relational authorization
registry**.

Logos owns persistent authorization policy. LifeOS cannot register itself,
grant itself source, namespace, or operation authority, or otherwise elevate
its policy. The administration mechanism is deliberately not selected here.

## Stable authorization principal

Authorization policy identity is exactly:

```text
principalType + principalId
```

The initial workload policy subject is:

```text
principalType = WORKLOAD
principalId   = lifeos
```

`credentialIdentity`, key IDs, individual keys, and an assertion/JWT instance
are not authorization identity. Credential rotation retains the same workload
principal and therefore the same authorization identity.

## Authorization decision

```text
authorize(
    normalizedAuthenticatedPrincipal,
    operation,
    requestedSource?,
    requestedNamespace?
) -> ALLOW | DENY
```

HARD-002 consumes the normalized principal produced by HARD-001. It must not
parse assertions, verify signatures, parse keys, authenticate again, or treat a
caller-provided source or namespace as proof of authority.

## Grant dimensions and default deny

Operation, source, and namespace grants are conceptually independent. Every
dimension applicable to an operation must allow the request; no grant implies
another grant. The registry is **default deny**.

Absence of an applicable grant denies unknown workloads, unauthorized source,
namespace, or operation, a disabled principal, and a revoked grant.
Authentication failure remains HARD-001 territory; authorization denial belongs
to HARD-002. HTTP error representation remains a later technical-plan decision.

## Initial LifeOS authorization

The complete initial workload grant is:

```text
principal: WORKLOAD / lifeos
operation: PROGRESSION_EXECUTE
source:    lifeos
namespace: lifeos
```

Thus `WORKLOAD / lifeos` may execute progression only when both requested
`source` and subject namespace equal `lifeos`.

The following are explicitly **not granted**:

```text
PROGRESSION_EXECUTION_READ
PROGRESSION_HISTORY_READ
SUBJECT_IDENTITY_PROVISION
```

Execution authority does not imply a read or provisioning grant. Source
authority does not imply namespace authority, and vice versa.

## Human AppUser boundary

The existing human AppUser JWT authentication path is preserved and is not
redesigned by this decision. `SUBJECT_IDENTITY_PROVISION` is recognized as a
distinct authorization-sensitive operation; its current human behavior is not a
new broad authorization grant.

## HARD-001 separation

```text
HARD-001 trust         = may this credential authenticate as this workload?
HARD-002 authorization = what may that authenticated principal do?
```

The trust registry and authorization registry have separate responsibilities.
No shared persistence model is selected by this decision.

## HARD-003 handoff

HARD-002 authorizes an operation, source, and namespace. It does not establish
ownership of `(namespace, externalId)`.

`HARD-003 / LIFEOS-LOGOS-001J` must decide creation, claim, linking, ownership
proof, takeover prevention, use after provisioning, reassignment, deactivation,
deletion, and audit lifecycle.

## Persistence boundary

The selected registry must conceptually support stable principal identity,
principal enable/disable state, operation/source/namespace grants, grant
activation or revocation, and audit-relevant policy history. Exact schema,
tables, entities, repositories, DDL, migrations, seed data, and administration
workflow remain unselected and unauthorized.

## Compatibility invariants

```text
credential identity != workload principal
workload principal != execution source
execution source != subject namespace
subject namespace != subject externalId
authentication != authorization
authorization != business idempotency
authorization != assertion replay protection
```

The existing execution business identity remains `source + idempotencyKey`.
This decision preserves Progression HTTP V1 payload and business semantics,
historical executions, and semantic snapshots.

## Next gate and non-authorization

The next authorized gate is:

`LIFEOS-LOGOS-001J — EXTERNAL SUBJECT OWNERSHIP LIFECYCLE`

HARD-002 is approved and frozen, but implementation remains unauthorized.
001J and later gates have not been executed. This decision authorizes no source
or test change, migration, database operation, runtime progression, key or
credential work, replay, recovery, deployment, or productization.
