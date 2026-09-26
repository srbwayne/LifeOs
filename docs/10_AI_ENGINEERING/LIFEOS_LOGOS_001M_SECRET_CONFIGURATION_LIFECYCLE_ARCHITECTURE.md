# LIFEOS-LOGOS-001M — HARD-006 Secret / Configuration Lifecycle Contract

Status: **APPROVED / FROZEN** by `LIFEOS-LOGOS-001M-DEC-001`.

Selected model: **OPTION B — BOUNDED WORKLOAD-KEY PROVIDER +
DEPLOYMENT-INJECTED SECRET MATERIAL/REFERENCE + STARTUP-IMMUTABLE LOADING**.

This is governance architecture only. Key generation, secret creation,
rotation, revocation, runtime authentication, deployment, database changes,
and configuration mutation remain **NOT AUTHORIZED**.

## Authority and current implementation state

HARD-001 remains the frozen ES256 workload assertion profile for stable
`WORKLOAD / lifeos`. HARD-002 grants remain attached to that stable principal,
not to a credential. HARD-003, HARD-004, and HARD-005 remain authoritative.

The canonical Logos reference is
`7a2b75aaa4413ab0e352c6f3d75d46f39ea16b74`. PR #41 provides a canonical V45
persistence foundation for workload principals, signing keys, trust audit,
and assertion replay. This means:

```text
HARD-001 architecture/profile = APPROVED / FROZEN
HARD-001 Logos persistence foundation = IMPLEMENTED / CANONICAL at V45
runtime workload authentication = NOT ESTABLISHED BY THIS GOVERNANCE GATE
```

No real workload principal, trusted key, `kid`, private key, or replay event
is seeded by this decision.

## Secret, identity, and configuration separation

The LifeOS private signing key is confidential secret material owned by LifeOS
and its authorized deployment boundary. It is never sent to Logos, committed
to Git, stored in business/delivery/attempt/correlation/audit records,
logged, printed, serialized into ordinary configuration dumps, or included in
ordinary application backups.

The public key is not confidential, but trust-registry integrity and its
association with a principal are security-critical. Logos may persist the
public key, `kid`, principal association, algorithm, fingerprint, lifecycle
state, and audit history.

```text
secret material != credential identity != trust metadata
business configuration != authentication credential
configuration revision != secret
```

Current LifeOS reality is environment-backed POC settings, including
`LIFEOS_LOGOS_BEARER_TOKEN`, base URL, Reading configuration key/revision,
timeout, and enablement. There is no implemented workload-key provider,
dynamic reload, or external secret-manager adapter. Current Logos
`LOGOS_JWT_SECRET` remains a separate human/AppUser credential.

## Workload-key provider boundary

Freeze a bounded integration-specific boundary equivalent to
`WorkloadSigningKeyProvider`. It supplies the active workload signing
credential to the assertion signer. It is not a universal secret-management
platform. Exact interface, reference syntax, and deployment mechanism are
technical-plan decisions.

Ordinary typed configuration should contain enablement, Logos endpoint, `kid`,
a signing-key reference/handle, timeout, and business configuration identity;
it should not broadly propagate raw private-key material.

The preferred source contract is deployment-injected secret material or a
controlled reference resolved by the provider at startup. No secret-manager
vendor is selected.

## Startup immutability and fail-fast behavior

The first implementation model is:

```text
startup load + validation + immutable process-lifetime credential
```

Dynamic reload and per-request provider lookup are deferred. Credential
changes become active through controlled process replacement/restart.

When explicitly enabled, fail closed/fast on missing or malformed PKCS#8 PEM,
missing `kid`, provider permission/unavailability, invalid endpoint/timeout,
or missing business configuration. Explicit enablement must never silently
fall back to NoOp.

Frozen protocol constants remain validated constants:

```text
alg = ES256
iss = urn:akume:workload-issuer:lifeos
aud = urn:akume:service:logos
```

Algorithm selection is not a free runtime setting.

## Credential identity and lifecycle

The workload private key uses ES256/EC P-256 and PKCS#8 PEM. `kid` is a
security-sensitive lookup selector, not secret material, and is never reused.
A revoked or retired `kid` cannot later identify different key material.

Conceptual states are:

```text
REGISTERED/PENDING → ACTIVE → RETIRING → REVOKED or RETIRED
```

The canonical V45 state mapping is implementation input for technical
planning; exact application enum names are not frozen here.

Rotation never changes:

```text
principalType = WORKLOAD
principalId   = lifeos
```

HARD-002 grants therefore remain unchanged. Whole-workload disablement or
revocation is separate from individual credential revocation and overrides
all keys.

## Planned rotation

The approved sequence is:

1. Generate K2 outside this gate and assign a never-used `kid`.
2. Register K2's public key in the Logos trust registry.
3. Activate K2 while K1 remains valid.
4. Deploy/restart every active LifeOS signer with K2.
5. Verify K2 authentication.
6. Confirm all active emitters have stopped issuing K1 assertions.
7. Retire/revoke K1 under normal policy.
8. Remove/destroy K1 private material from the active secret source.
9. Preserve only non-secret lifecycle/audit metadata.

New trust activation precedes new-key signing. All active emitters, including
future replicas/workers, must stop using K1 before normal retirement.
Overlap duration remains deferred.

## Emergency compromise and credential loss

Compromise prioritizes containment: revoke the affected Logos credential,
fail closed affected workload calls as necessary, create a replacement with a
new `kid`, register and activate trust, restart/reconfigure LifeOS, and resume
only after verification. No fallback to the compromised key, POC bearer,
human JWT, or shared secret is permitted.

If a key is lost without evidence of compromise, keep `WORKLOAD / lifeos` and
its grants, create a new credential with a new `kid`, and make the lost
credential non-active after replacement. `REVOKED` remains appropriate when
risk requires it; exact persisted mapping is deferred.

Ordinary application backups must not contain workload private keys. A
separate encrypted, access-controlled secret-specific backup may be considered
later.

## Environment and test isolation

Development, test, staging, and production must not normally reuse private
keys, `kid` values, trust registrations, bearer credentials, or database
passwords. Each environment owns independent trust material.

Tests use ephemeral/generated or clearly isolated credentials that cannot
authenticate against an operational trust registry. No key is generated by
this gate.

## Trust bootstrap and administration

The first LifeOS credential requires a controlled Logos administrative/bootstrap
action. Trust-on-first-use, LifeOS self-registration, assertion-supplied key
material, and assertion-supplied URL loading are prohibited.

Registration, activation, revocation, retirement, and whole-workload
disablement must be administrative, explicit, authorized, and audited.
`WORKLOAD / lifeos` cannot add its own trusted key merely because it is
authenticated.

## Fingerprints and audit

A public-key fingerprint is approved as controlled operator-verification and
audit metadata, not as an independent trust source. Canonical Logos V45
stores an SPKI SHA-256 fingerprint; future technical planning must reconcile
with that implementation. Exact encoding remains deferred.

Lifecycle audit must identify actor, principal, `kid`, fingerprint, algorithm,
state transitions, timestamps, reasons, replacement relationships, and
whole-workload status. Private keys and raw assertions never enter audit.

HARD-005 attempt evidence may record the `kid` used for an outbound attempt,
but never a private key, assertion, signature, Authorization header, or token.

## Logging and error boundary

Never log or expose private keys, raw assertions, Authorization headers, POC
bearer tokens, human JWT secrets, database passwords, signatures, or client
secrets. Controlled metadata such as `kid`, principal ID, fingerprint, and
bounded failure classifications may be used when access-controlled.

Secret-bearing objects must resist accidental `repr`, serialization, debug
dumps, exception interpolation, and structured logging. External errors must
not reveal secret values or matching behavior.

## POC bearer retirement

`LIFEOS_LOGOS_BEARER_TOKEN` is a current POC credential, not HARD-001
authentication. At a separately authorized cutover: verify workload
assertions, switch the workload route, disable the legacy bearer path, remove
the bearer from deployment sources, revoke/invalidate it where applicable,
remove obsolete configuration references, and record the cutover.

The selected default is atomic workload-authentication cutover, not prolonged
dual acceptance. Any temporary dual acceptance requires separate explicit,
time-bounded approval and must never provide fallback from an invalid workload
assertion to bearer or AppUser authentication.

## Human JWT and business configuration

`LOGOS_JWT_SECRET` remains on its independent human/AppUser lifecycle. HARD-006
does not alter human login semantics.

Reading configuration key/revision remains business configuration identity
under HARD-004/HARD-005. It is not secret material and credential rotation
must not change it. Base URL is controlled operational configuration; timeout
is controlled operational configuration. Neither changes business
idempotency or progression fingerprint semantics.

## Deployment boundary

HARD-006 defines guarantees, not technology. Any future deployment mechanism
must provide:

```text
secret excluded from Git
restricted access
controlled injection
environment isolation
safe restart/rollout
auditability
credential replacement capability
```

Vault, cloud secret managers, Kubernetes/Docker/systemd secrets, SOPS,
Ansible Vault, and other vendors/tools are not selected. HARD-007 may choose
technology compatible with this contract.

## Foundation governance completion

The reusable structural-hardening foundation is complete at the
architecture/governance level:

```text
HARD-001 / HARD-002 / HARD-003 / HARD-005 / HARD-004 / HARD-006
= APPROVED / FROZEN
```

This does not mean implementation, production readiness, deployment
readiness, or productization is complete. HARD-007 remains
`DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER`.

## Sequencing and deferrals

Future planning should reconcile canonical Logos V45 persistence with the
remaining HARD-001 runtime-authentication plan, then define the LifeOS
provider/signer, trust bootstrap, and separately authorized implementation
slices. This decision authorizes none of those activities.

Deferred details include interfaces, environment names, reference syntax,
paths/permissions, deployment mechanism, trust schema changes, migration
number, key-generation tooling, fingerprint encoding, overlap duration,
operator APIs, provider vendor, restart orchestration, and CI secret
injection.

## Status

```text
LIFEOS-LOGOS-001M-DEC-001 = APPROVED / FROZEN
HARD-006 = APPROVED / FROZEN
selected option = OPTION B — BOUNDED WORKLOAD-KEY PROVIDER
                 + DEPLOYMENT-INJECTED SECRET MATERIAL/REFERENCE
                 + STARTUP-IMMUTABLE LOADING
implementation = NOT AUTHORIZED
next gate = LIFEOS-LOGOS-HARDENING-TP-001
HARD-007 = DEFERRED
```
