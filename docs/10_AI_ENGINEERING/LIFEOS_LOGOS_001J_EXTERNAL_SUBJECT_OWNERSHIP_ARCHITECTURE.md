# LIFEOS-LOGOS-001J — External Subject Ownership Lifecycle Architecture

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001J-DEC-001`.

This is a governance and architecture record only. It authorizes no source,
schema, migration, credential, runtime, progression, replay, recovery,
deployment, or productization work.

## Decision

The selected model is **Option B — Stateful ownership lifecycle with
immutable-by-default bindings**. An external reference is the pair
`(namespace, externalId)` and its relationship to an internal Logos subject is
an ownership relationship, not an authentication or authorization result.
Normal callers cannot silently change an established valid binding; transfer or
correction requires an explicit controlled lifecycle action.

## Responsibility boundaries

```text
authentication != authorization
authorization != ownership
ownership != execution identity
ownership != assertion replay protection
ownership != business idempotency
```

HARD-001 answers who authenticated. HARD-002 answers what that principal may
do for an operation, source, and namespace. HARD-003 answers whether a specific
`(namespace, externalId)` is validly linked to a specific Logos subject and
what lifecycle governs that link. A valid workload assertion or namespace grant
is not ownership proof.

## Creation and proof

Conceptual creation paths include an authorized Logos operator, a human
self-link supported by valid external ownership evidence, or a workload flow
that has a separate `SUBJECT_IDENTITY_PROVISION` grant. `PROGRESSION_EXECUTE`
never implies provisioning authority. The current `WORKLOAD / lifeos` policy
has no subject-provisioning grant.

Authentication, source authorization, and namespace authorization alone do not
prove control of an external identity. Evidence must be Logos-verifiable and
specific to both the external reference and target subject. The exact proof
protocol is intentionally unselected; challenge formats, OAuth/OIDC pairing,
provider callbacks, and API exchanges are not frozen here.

## Lifecycle semantics

The lifecycle supports semantics equivalent to:

```text
UNMAPPED -> ACTIVE -> DISABLED -> TOMBSTONED
                    -> TRANSFERRED / REASSIGNED (controlled history)
```

Exact persisted state names remain a technical-plan decision.

For an ACTIVE mapping, the same reference and same target are an idempotent
success. A different target is a conflict: normal flows must never silently
overwrite, delete and recreate, automatically transfer, or apply last-write-
wins ownership.

Reassignment is not normal provisioning. It requires a controlled
administrative transfer/correction workflow with an explicit actor, reason,
old subject, new subject, effective time, and audit history. A disabled mapping
cannot authorize new progression/use, while historical evidence remains valid.
Ordinary hard deletion is not selected; tombstone or equivalent preservation
must prevent silent external-ID reclaim and preserve provenance.

## Use after valid linking

The selected initial rule is:

```text
ACTIVE validly-established mapping
+ HARD-002 operation/source/namespace authorization
= sufficient condition for progression use
```

No per-mapping workload delegation is introduced, and this decision grants no
new HARD-002 operation.

## Human, native, and legacy boundaries

Historical AppUser self-provisioning is POC/legacy behavior, not production
ownership proof. Future human self-linking requires valid external evidence;
human JWT authentication does not prove control of an external LifeOS, Noema,
or other identity.

`logos-native` remains Logos-owned. External workloads and humans must not claim
or transfer native identities. Existing non-native mappings may lack provenance;
the architecture must not retroactively assert their proof source, creating
actor, or verified status. They may later be classified as `LEGACY`, `UNKNOWN`,
or operator-reviewed by an explicit technical decision. The bounded LifeOS POC
mapping remains historical evidence and is not automatically production-
verified ownership.

## History, audit, and concurrency

Ownership changes must not rewrite durable progression history. Executions retain
their stored subject namespace, external ID, execution identity, timestamps,
and semantic snapshots.

A future persistence model must preserve mapping/version identity, action, actor
or normalized principal where applicable, effective time, previous and new
subjects where applicable, reason, and proof/evidence reference where applicable.
Exact tables and event schemas are unselected.

Concurrent same-reference/same-target claims must be idempotent; concurrent
different-target claims must produce one valid outcome and a conflict;
transfer/correction must not create inconsistent ownership; and disable versus
execution must have an atomic ordering that prevents invalid new use. Locking or
versioning mechanisms remain technical-plan decisions.

## Persistence boundary

This decision does not select table or column names, entities, Flyway versions,
`verification_status`, challenge tables, token formats, proof/history schemas,
lock implementations, APIs, DTOs, or administrative UX.

## Experimental evidence

Logos PR #38 explored subject-link verification and was closed without merge
during governance reconciliation. Its successful CI and branch remain
engineering evidence only. The following are not frozen by this decision:

```text
challenge-based linking
INTEGRATION_VERIFIED
UNVERIFIED
verified_by_client_id
V45
challenge persistence
specific migration strategy
specific legacy quarantine behavior
specific concurrency design
```

PR #36 introduced trust/authorization semantics inconsistent with frozen
HARD-001/HARD-002; PR #37 canonically reverted that implementation. HARD-003
does not promote either experiment into canonical implementation.

## Governance state

```text
LIFEOS-LOGOS-001J-DEC-001 = APPROVED / FROZEN
HARD-003 = APPROVED / FROZEN
implementation = NOT AUTHORIZED
next governance gate = LIFEOS-LOGOS-001L / HARD-005
```

HARD-005 (minimum cross-system correlation) precedes HARD-004. No
implementation gate is opened by this canonicalization.
