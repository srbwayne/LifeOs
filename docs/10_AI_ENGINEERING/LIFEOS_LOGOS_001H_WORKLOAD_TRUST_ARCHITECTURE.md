# LIFEOS-LOGOS-001H — Workload Trust Architecture

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001H-DEC-001`.

This document records the human decision for workload authentication between
LifeOS and Logos. It defines trust semantics only. It authorizes no source
change, key generation, migration, runtime, or productization.

## Decision

The selected model is **Option D — asymmetric workload-signed assertion/JWT**.

- Principal type: `WORKLOAD`
- Initial principal identity: stable canonical LifeOS workload identity,
  `lifeos`
- LifeOS holds an externally provisioned asymmetric private key.
- Logos trusts the corresponding public key and constructs a workload
  principal after verification.
- A separate Identity Provider, OAuth authorization server, or mTLS layer is
  not required for the initial architecture.
- Human AppUser identity and password reuse for production service calls are
  prohibited.
- The opaque service-key fallback is not selected as a supported path.
- Replay control is required.

Implementation remains unauthorized. `LIFEOS-LOGOS-001I` is the only next
authorized gate.

## Workload principal

The authenticated principal must distinguish `WORKLOAD` from `HUMAN`/AppUser.
The conceptual metadata includes a stable principal ID, principal type,
authentication method, and verified credential/key identity. Exact DTO and
class names remain technical-plan decisions, and domain objects must not depend
on Spring Security.

The normalized handoff to HARD-002 is:

```text
principalType       = WORKLOAD
principalId         = stable LifeOS workload identity
authenticationMethod = ASYMMETRIC_SIGNED_ASSERTION
credentialIdentity  = verified key/credential ID
authenticationStatus = VERIFIED
```

HARD-002 must authorize from this normalized principal. It must not parse
private/public key material, revalidate raw credential semantics, or trust
caller-provided source/namespace claims merely because they occur in an
assertion.

## Assertion contract

LifeOS creates one short-lived signed assertion for each outbound authenticated
Logos request. Logos validates it directly; no Logos token-exchange or token
issuance endpoint is required by this architecture.

The assertion requires:

- trusted issuer identity representing the LifeOS workload;
- stable workload subject/principal identity;
- Logos-specific audience;
- issued-at and expiration times;
- unique assertion identity;
- credential/key identity;
- signature integrity.

These semantics correspond to issuer, subject, audience, issued-at,
expiration, unique token/assertion ID, and key ID. Exact standard claim and
header names are technical-plan scope. Authorization authority must not rest
solely in caller-controlled claims.

Replay control is mandatory. A short lifetime alone is insufficient. The
initial model is one assertion per outbound request, with a bounded replay
policy. The replay store/cache mechanism is deliberately undecided.

Logos must reject assertions with an untrusted issuer, wrong audience, invalid
signature, invalid lifetime, unknown/revoked key, or replayed assertion ID.
Clock-skew tolerance remains a technical-plan decision.

## Trust registry and administration

Logos requires a conceptual workload trust registry that resolves:

- workload principal;
- active public-key identities;
- key status and revocation;
- rotation state;
- audit history.

Multiple keys must be supported during controlled rotation. Storage is not
selected; it may be a database, external trust store, or another approved
persistent mechanism.

An authorized Logos-side trust administrator owns workload registration,
public-key registration, activation, rotation, and revocation. LifeOS must not
self-register arbitrary trusted keys. No current AppUser is automatically
granted this authority.

## Key rotation and revocation

Rotation preserves the workload principal ID:

1. Generate/provision a new LifeOS private key externally.
2. Register the new public key in Logos.
3. Allow old and new keys to coexist for a bounded overlap.
4. Switch LifeOS to the new private key.
5. Revoke or retire the old key.

Rotation must not change principal identity, source identity, namespace
identity, or progression idempotency identity. Individual-key revocation and
whole-workload revocation are required. Revoked credentials cause
authentication failure and do not delete historical evidence.

Exact overlap duration, storage, and automation remain technical-plan scope.

## Human authentication compatibility

The existing AppUser JWT path remains supported. Human and workload
authentication paths coexist and produce distinguishable principals. This
decision does not redesign human login or replace AppUser authentication.

## Boundary with authorization

001H answers **who authenticated**. 001I answers **what that principal may
claim or do**. The signed assertion authenticates `WORKLOAD / lifeos`; it does
not itself authorize `source=lifeos`, `namespace=lifeos`, progression
execution, subject provisioning, or read/history operations. Those bindings
belong to HARD-002.

## Local development and CI

Local and CI environments must exercise the same asymmetric trust semantics
with isolated non-production keys and identities. No runtime private key may
be committed. Test-only material may exist only under the repository security
policy and must not be reusable as production material. No key generation or
credential provisioning occurs in this gate.

## Compatibility

The architecture preserves:

- the existing Progression HTTP V1 payload;
- `subject.namespace` and `subject.externalId`;
- `execution.source` and `idempotencyKey`;
- explicit configuration key/revision and details;
- Reading revision 1 evidence;
- durable semantic snapshots;
- historical executions;
- progression idempotency semantics.

No POC rerun is required.

## Expected impact

Likely LifeOS areas are the Logos settings, gateway, dependency wiring,
credential/assertion provider abstraction, tests, and security documentation.
Likely Logos areas are security filter/provider composition, authenticated
principal abstraction, workload assertion verification, trust-registry adapter,
and security tests. The existing human JWT path must remain compatible.

No implementation allowlist is frozen by this decision.

LifeOS schema migration is not expected. Logos migration is possible or likely
if trust-registry and revocation metadata are persisted in the Logos database;
the storage mechanism remains undecided. Repository Flyway remains V44 and no
migration is authorized.

## HARD-006 relationship

This decision defines the credential properties required by trust architecture.
HARD-006/001M remains responsible for secret injection, storage, rotation
automation, revocation operations, environment separation, and controlled
reload/restart. No secret manager, key store, or deployment tool is selected.

## Next gate and non-authorization

The next authorized gate is:

`LIFEOS-LOGOS-001I — SOURCE / NAMESPACE / OPERATION AUTHORIZATION ARCHITECTURE`

It is read-only and not executed. 001J and later gates remain unauthorized.

This freeze authorizes no source, test, migration, runtime, database,
credential generation, progression, replay, service-identity implementation,
or productization work.
