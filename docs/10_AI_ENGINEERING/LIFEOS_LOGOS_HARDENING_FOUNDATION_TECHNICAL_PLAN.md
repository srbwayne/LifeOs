# LifeOS ↔ Logos Hardening Foundation Technical Plan

## Status

```text
LIFEOS-LOGOS-HARDENING-TP-001-DEC-001 = APPROVED / FROZEN / CANONICAL / AMENDED
LIFEOS-LOGOS-HARDENING-TP-001-DEC-001-A1 = APPROVED / FROZEN
LIFEOS-LOGOS-HARDENING-TP-001-A4 = HISTORICAL F1E DORMANT FOUNDATION + RESIDUAL F1E-R2 DECISION
LIFEOS-LOGOS-HARDENING-TP-001-A5 = HISTORICAL CANONICAL F1F ADVANCEMENT / SEQUENCING DEVIATION
LIFEOS-LOGOS-HARDENING-TP-001-A6 = HISTORICAL F1E-R2 CLOSURE + F1F SEQUENCING RECONCILIATION
LIFEOS-LOGOS-HARDENING-TP-001-A7 = HISTORICAL F1E-R2 CLOSURE CORRECTION + RESIDUAL HUMAN-AUTH GAP RESTORED
LIFEOS-LOGOS-HARDENING-TP-001-A8 = CURRENT CANONICAL B1 ADVANCEMENT + F1E-R2 RESIDUAL CLOSURE STILL OPEN
Foundation Technical Plan = APPROVED / FROZEN / CANONICAL / RECONCILED
implementation overall = PARTIAL
F1A-F1D = IMPLEMENTED / CANONICAL
F1E PR #45 foundation = IMPLEMENTED / CANONICAL / DORMANT
F1E overall = PARTIAL / NOT CLOSED
F1E-R2 = IMPLEMENTED / CANONICAL / DEFAULT-OFF / RESIDUAL GAP OPEN
F1F = IMPLEMENTED / CANONICAL / DORMANT TRUST ADMINISTRATION CAPABILITY
```

This document is a documentation-only implementation sequencing plan. It
does not itself authorize additional implementation or operational activation,
bootstrap, deployment, or mutation.

## Baselines and governance

The A7 current-state correction used LifeOS canonical
`4fea64478b1053c724b56d234d66fbc8d671dc1b`; A8 uses LifeOS canonical
`47a8d4a8eb12714fccb75c3f4d6591617f6ef1f2`. The A7 Logos reference was
`d475838e529e32a81074094f291f45892076e9f5`; current A8 Logos canonical is
`001fa70108d6640e85f01be643d71177935fb40c`, with PR #48's B1 foundation
present alongside F1A–F1F. The structural architecture
foundation is frozen:

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

## A2 — canonical F1D implementation-state reconciliation

After this plan was merged, Logos PR #44 advanced F1D canonically before the
planned `LOGOS-HARD-001-F1D-IA-001` pre-flight gate ran. This is recorded as a
**GOVERNANCE SEQUENCING DEVIATION**. It is not an architecture conflict,
security-model rejection, or plan invalidation. The deviation is reconciled as
canonical external reality; it does not claim that F1D-IA-001 occurred and
does not grant retroactive LifeOS authorization. No revert or reimplementation
is requested.

```text
LIFEOS-LOGOS-HARDENING-TP-001 = COMPLETE
DEC-001 = APPROVED / FROZEN / CANONICAL / AMENDED
A1 = APPROVED / FROZEN / CANONICAL
A2 = IMPLEMENTATION-STATE RECONCILIATION / CANONICAL F1D ADVANCEMENT
implementation overall = PARTIAL
```

PR #44 (`LOGOS-HARD-001-F1D — Add atomic replay protection and authenticated
principal`) is canonical at `c095fbb2ce0643b8622bbf0bf24bc62b2177157e`. It
adds replay storage/guard and authentication completion, but does not add
SecurityConfig integration, route activation, progression changes, HARD-002
authorization, or trust bootstrap.

## A3 — current-state correction after canonical A2 publication

This section is the historical A3 checkpoint. Its references to PR #45 being
open, in review, or non-canonical describe that checkpoint only and are
superseded by A4 below.

A2 remains the historical canonical reconciliation of F1D. Two later facts
make parts of its current-state summary stale: F1E subsequently received direct
Logos-side implementation authorization and is now under review in PR #45; and
canonical Logos already had scheduling infrastructure, so F1D replay-cleanup
scheduling eligibility can be established from the canonical tree. This
correction does not rewrite A2's historical checkpoint.

F1E implementation was directly authorized in the Logos execution workflow
and is currently under review in PR #45. The separately planned
`LOGOS-HARD-001-F1E-IA-001` was not executed under that identifier and is not
retroactively claimed. This is governance sequencing reconciliation only; it
is not an architecture conflict, security-model rejection, retroactive IA
completion, or merge authorization. PR #45 remains non-canonical until
independent review, explicit merge authorization, merge, and post-merge push CI
verification.

The canonical Logos reference remains
`c095fbb2ce0643b8622bbf0bf24bc62b2177157e`; observed PR #45 HEAD
`d8440954a06412f8bce04e2435e6c51a5f236b27` is review evidence only. Current
implementation state is partial: F1A–F1D are implemented/canonical; F1E is
authorized/in review/not canonical; F1F, B1, B2, C1, and C2 remain unauthorized.
Bootstrap, cutover, productization, productionization, and recovery remain
unauthorized. HARD-007 remains deferred and WORK-001 remains deferred.

## A4 — current F1E canonical dormant foundation and residual decision

A3 remains the historical F1E review checkpoint and is not rewritten. After
A3, Logos PR #45 merged canonically at
`760e9fda55dc2543c42594ebe2ad2edf6ce0b450` with successful post-merge CI.
This A4 reconciliation records the current state:

```text
LIFEOS-LOGOS-HARDENING-TP-001-A4 =
F1E CANONICAL DORMANT FOUNDATION + RESIDUAL F1E-R2 DECISION

LOGOS-HARD-001-F1E-R1-DEC-001 = APPROVED / FROZEN
PR #45 = IMPLEMENTED / CANONICAL / DORMANT SPRING SECURITY WORKLOAD ADAPTER FOUNDATION
F1E = PARTIAL IMPLEMENTATION / CANONICAL DORMANT FOUNDATION / NOT CLOSED
F1E-R2 = PLANNED / NOT AUTHORIZED
```

The human F1E-R1 decision occurred after PR #45 implementation and merge. It
is authoritative for the remaining target, not retroactive authorization for
PR #45. PR #45 provides the request/principal tokens, F1D provider adapter,
bounded Bearer parser, generic 401/503 responder, and dormancy evidence, but
does not wire production `SecurityConfig`, the exact workload POST matcher,
default-off activation, exclusive chain ownership, the pre-B2 `denyAll`
barrier, or production integration behavior.

The residual slice is:

```text
LOGOS-HARD-001-F1E-R2
WIRE AND COMPLETE DORMANT WORKLOAD SPRING SECURITY PROFILE
WITHOUT ACTIVATING REAL WORKLOAD TRAFFIC
```

Its frozen boundary is a conditional higher-priority workload chain for exact
`POST /api/internal/v1/progression/executions`, default-disabled through the
conceptual `logos.security.workload.http.enabled` setting. When enabled, the
matched request is exclusively owned by the workload chain; authentication
only produces identity, and before B2 the chain uses `denyAll`, returns 403,
and never invokes the controller. Authentication failures return generic 401;
replay/trust infrastructure failures return generic 503. GET execution,
history, and subject provisioning remain outside the workload profile.

R2 may modify exactly `SecurityConfig.java` and
`JwtAuthenticationFilter.java`, and may add exactly the approved workload
integration test plus modify the existing progression security test. No
migration or dependency change is expected. Human filter servlet
auto-registration must be explicitly disabled, and its hardening is limited
to expected JWT credential failures; it must not gain workload responsibilities.
Trust/authorization/ownership bootstrap, cutover, bearer retirement, F1F,
recovery, HARD-007, and WORK-001 remain outside this decision.

## A5 — canonical F1F dormant trust administration advancement

A4 is preserved as the historical/current checkpoint before the later Logos
advancement. Logos PR #46 subsequently advanced from
`760e9fda55dc2543c42594ebe2ad2edf6ce0b450` to
`0d03fe34c522df2e0ca12a2681d7e81e50c62654`. PR #46 is canonical and provides
dormant trust-administration capability. F1F advanced before F1E-R2 closure;
this is a **GOVERNANCE SEQUENCING DEVIATION**, not an architecture conflict,
security-model rejection, A4 invalidation, retroactive authorization, or F1E-R2
completion. No prior F1F implementation-authorization gate is claimed, and no
revert or reimplementation is requested.

```text
LIFEOS-LOGOS-HARDENING-TP-001-A5 =
CANONICAL F1F DORMANT TRUST ADMINISTRATION ADVANCEMENT

LOGOS-HARD-001-F1F = IMPLEMENTED / CANONICAL / DORMANT TRUST ADMINISTRATION CAPABILITY
F1E = PARTIAL / NOT CLOSED
F1E-R2 = PLANNED / NOT AUTHORIZED
F1F sequencing = ADVANCED BEFORE F1E-R2 CLOSURE / GOVERNANCE SEQUENCING DEVIATION
retroactive F1F authorization = NONE
```

Canonical F1F provides internal application/storage capability for workload
principal and credential registration, principal lifecycle transitions,
credential lifecycle transitions, and transactional trust audit events. Its
canonical tests cover idempotent identical registration, issuer/principal and
kid/fingerprint conflict rejection, invalid lifecycle transitions, and
rejection of credential activation for revoked principals. It is not a public
HTTP administration API, deployment tooling, secret manager, private-key
handler, authorization registry, ownership implementation, or workload HTTP
cutover. Real trust bootstrap and real LifeOS registration remain unexecuted.

## A6 — canonical F1E-R2 closure and F1F sequencing reconciliation

A5 is preserved as the historical checkpoint that recorded F1F becoming
canonical before F1E-R2 closure. After A5, Logos PR #47 merged as a squash:

```text
PR #47 reviewed HEAD = b7ed2da2bca5401157190246d1c59282c83b4fdf
canonical parent = 0d03fe34c522df2e0ca12a2681d7e81e50c62654
canonical Logos main = d475838e529e32a81074094f291f45892076e9f5
post-merge push CI = 36369044090 / SUCCESS
canonical suite = 378 tests / 0 failures / 0 errors / 0 skipped
Flyway = V45
```

PR #47 completes F1E-R2 with a conditional workload Spring Security chain for
exact `POST /api/internal/v1/progression/executions`. The property
`logos.security.workload.http.enabled` is absent from production configuration;
the conditional chain is default-disabled. When enabled in an isolated
context, the workload chain is order 1 and the human chain is order 2. The
profiles are isolated, the human `JwtAuthenticationFilter` is not servlet
auto-registered and remains installed inside the human chain, and the workload
chain has a dedicated workload-only manager. Before B2 its authorization rule
is `denyAll`: a valid first-use workload assertion authenticates and consumes
replay, then receives 403 without controller invocation; replaying that
assertion receives 401. Caller authentication failures map to 401 and
authentication infrastructure failures to 503. Operational workload
activation remains NOT ACTIVE.

The F1F sequencing fact is retained: F1F advanced canonically before F1E-R2
closure. This remains a GOVERNANCE SEQUENCING DEVIATION, not an architecture or
security-model conflict, invalid F1F implementation, rollback requirement, or
retroactive authorization. With both slices now canonical, the dependency
ordering is satisfied in implementation state. F1E overall is
IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF; F1F remains
IMPLEMENTED / CANONICAL / DORMANT. HARD-001's implementation foundation is
complete/canonical but operationally NOT ACTIVATED. No real LifeOS credential,
private key, trust bootstrap, workload assertion emission, POC bearer
retirement, or cutover is established by this reconciliation.

The canonical implementation foundation does not establish an operational
`WORKLOAD / lifeos` trust registration, signing key, authorization grant, or
route activation. The future HARD-002 policy target remains architecture-only:
principal `WORKLOAD / lifeos`, operation `PROGRESSION_EXECUTE`, source `lifeos`,
namespace `lifeos`, default DENY, with no read or subject-provisioning grant.
No grant is inserted by this reconciliation.

At the A6 checkpoint, the then-current remaining Logos path was
`B1 → B2 → C1 → C2`. Its next gate was
`LOGOS-HARD-002-B1-TP-001` — Authorization Registry Persistence / Domain
Technical Preflight, a READ-ONLY preflight. A6 did not authorize B1
implementation. A7 later superseded that path for its CURRENT state; A8 now
supersedes A7 for CURRENT state.

## Historical A7 — F1E-R2 closure correction and residual human-auth gap restoration

This current-state correction is based on canonical LifeOS PR #118 merge
`4fea64478b1053c724b56d234d66fbc8d671dc1b`
(`docs(governance): reconcile F1E-R2 closure and F1F sequencing`, 2 changed
files) and canonical Logos `d475838e529e32a81074094f291f45892076e9f5`. A6 is
preserved historically: it
declared F1E-R2/F1E closed and recorded B1 as the next path. No Logos code
change followed PR #47, so the implementation evidence used for that closure
conclusion still contains the residual AppUser lookup gap. A7 supersedes A6
only for CURRENT state. It does not roll back PR #118, reject PR #47, or claim
retroactive R2 authorization / IA approval. PR #118 was documentation-only;
no Logos code change followed PR #47.

Canonical PR #47 remains `IMPLEMENTED / CANONICAL / DEFAULT-OFF`. The current
classification is:

```text
LIFEOS-LOGOS-HARDENING-TP-001-A7 =
F1E-R2 CLOSURE CORRECTION + RESIDUAL HUMAN-AUTH GAP RESTORED

F1E foundation = IMPLEMENTED / CANONICAL / DORMANT
F1E-R2 = IMPLEMENTED / CANONICAL / DEFAULT-OFF / RESIDUAL GAP OPEN
F1E = PARTIAL / NOT CLOSED
F1F = IMPLEMENTED / CANONICAL / DORMANT
```

At canonical Logos baseline `d475838e529e32a81074094f291f45892076e9f5`,
`JwtAuthenticationFilter` catches `JwtException` around JWT subject extraction
and token validation, but calls
`userDetailsService.loadUserByUsername(userEmail)` outside those catches.
Canonical `UserDetailsServiceImpl.loadUserByUsername(...)` throws
`UsernameNotFoundException` when the AppUser repository has no matching user.
Therefore a validly structured human JWT whose subject has no AppUser may let
that expected lookup exception escape `JwtAuthenticationFilter`. This is the
proven gap; no external HTTP status such as 500 is asserted.

The completed R2 pre-flight identified the expected filter catch set as
`JwtException` plus `UsernameNotFoundException`. PR #47 implements only the
`JwtException` portion, so its implementation evidence and the pre-flight
target are not fully aligned. The residual is classified `MAJOR — R2 CLOSURE
GAP`. No Logos code change followed PR #47.

The A7 governance classification is `GOVERNANCE / CURRENT-STATE CORRECTION`,
not a PR #118 revert, PR #47 rejection, architecture conflict, or
security-model rejection. A6 remains a historical canonical checkpoint;
A2–A6 are not erased. The F1F sequencing deviation remains historical fact.

Canonical F1E-R2 behaviors remain accepted: conditional workload chain for
exact `POST /api/internal/v1/progression/executions`; workload `@Order(1)` and
AppUser `@Order(2)` chains; default/missing activation false; chain-local
workload filter and workload-only `ProviderManager`; disabled servlet
registration of the human `JwtAuthenticationFilter`; pre-B2 `denyAll`; valid
first workload assertion receives 403 after replay consumption; replay and
invalid workload authentication receive 401; authentication infrastructure
failure receives 503; controller is not invoked before B2; GET execution,
history GET, and subject provisioning remain outside the workload profile.
The residual human AppUser lookup gap does not invalidate these capabilities.

`SecurityConfig` R2 wiring remains `IMPLEMENTED / CANONICAL`, with no residual
SecurityConfig gap identified. No `SecurityConfig.java` change is indicated.
The deferred provider minor remains: an unexpected
`WorkloadAuthenticationProvider` `RuntimeException` is translated to
`AuthenticationServiceException` and returns 503; it is
`MINOR / FAIL-CLOSED / DEFERRED` and is outside immediate R2 closure.

The A7 serialized path at that historical checkpoint was:

```text
F1E-R2 residual closure → B1 → B2 → C1 → C2
```

At the A7 checkpoint, `LOGOS-HARD-002-B1` was planned / not authorized and
was sequenced after F1E closure. A8 records its subsequent canonical
advancement as a governance sequencing deviation. The next gate at A7 was
`LOGOS-HARD-001-F1E-R2-CLOSE-IA-001`, a READ-ONLY RESIDUAL CLOSURE PRE-FLIGHT /
IMPLEMENTATION AUTHORIZATION REVIEW. Its then-current review hypothesis was a
possible `JwtAuthenticationFilter.java` change to catch the expected
`UsernameNotFoundException` and continue unauthenticated, with a regression
test for a valid human JWT whose subject has no AppUser in
`ProgressionExecutionSecurityPostgresTest.java`. This was a hypothesis only;
A7 authorized no source or test implementation. `SecurityConfig`, workload
adapters, migration, dependencies, and runtime activation remain unchanged.

Current boundaries remain:

```text
migration = NONE
dependency changes = NONE
runtime configuration changes = NONE
logos.security.workload.http.enabled = absent / default false
real workload HTTP activation = NOT AUTHORIZED
T1 trust bootstrap = NOT AUTHORIZED
T2 authorization bootstrap = NOT AUTHORIZED
T3 ownership readiness = NOT AUTHORIZED
LifeOS workload assertion cutover = NOT AUTHORIZED
POC bearer retirement = NOT AUTHORIZED
B1 = PLANNED / NOT AUTHORIZED
HARD-007 = DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER
WORK-001 = DEFERRED
```

## A8 — canonical B1 advancement before F1E residual closure

A7 is preserved as the historical current-state checkpoint before canonical
B1 advancement. After A7, Logos PR #48 merged canonically:

```text
PR #48 = LOGOS-HARD-002-B1 — Add workload authorization registry foundation
base = d475838e529e32a81074094f291f45892076e9f5
head = fd6b8152f994928d55d22d550c347e54454971e3
merge = 001fa70108d6640e85f01be643d71177935fb40c
parent = d475838e529e32a81074094f291f45892076e9f5
tree = 1e56086e00a4bbf23a0649329b268d8cf49adbea
commit = feat(authorization): add relational workload grant registry (#48)
files = 18
stats = +665 / -4
post-merge push CI = 36496654683 / SUCCESS
Flyway = V46
```

PR #48 canonically implements `LOGOS-HARD-002-B1` as the relational
authorization registry persistence/domain foundation. It adds
`V46__Create_Authorization_Grant_Registry.sql` and the
`authorization_grant` table with `principal_type`, `principal_id`, `operation`,
`source`, `namespace`, and `created_at`. Supported operations are
`PROGRESSION_EXECUTE`, `PROGRESSION_EXECUTION_READ`,
`PROGRESSION_HISTORY_READ`, and `SUBJECT_PROVISION`; the migration enforces the
operation-specific source/namespace applicability constraints.

The grant principal has a foreign key to
`workload_principal(principal_type, principal_id)` with `ON DELETE RESTRICT`.
Semantic uniqueness is enforced by:

```text
UNIQUE NULLS NOT DISTINCT
(principal_type, principal_id, operation, source, namespace)
```

Canonical domain concepts are `AuthorizationPrincipal`,
`AuthorizationOperation`, `AuthorizationSource`, `AuthorizationNamespace`, and
`AuthorizationGrant`; the domain rejects dimensions inconsistent with the
operation. `AuthorizationGrantStore` and `JdbcAuthorizationGrantStore`
provide `insertIfAbsent(...)` and `findExact(...)`. An identical duplicate
insert returns `ALREADY_EXISTS`; exact semantic lookup is supported.

V46 is explicitly an empty authorization registry foundation. No grant is
seeded or inferred from trust, progression, or subject records. Authorization
bootstrap has not occurred; no `WORKLOAD/lifeos`
`PROGRESSION_EXECUTE` grant is inserted. Do not reserve V47; the F1E-R2
residual closure requires no migration.

PR #48 does not implement B2 authorization evaluation or enforcement, does
not create Spring authorities from stored grants, and does not change route
authorization. The pre-B2 workload chain continues to use `denyAll`. The B1
integration test inserts/finds a test grant and still receives 403 after a
valid workload assertion, without invoking the controller. Grant presence is
not enforcement. B2 remains `PLANNED / NOT AUTHORIZED`.

B1 advanced canonically before the F1E-R2 residual closure was complete. This
is a `GOVERNANCE SEQUENCING DEVIATION`; no retroactive B1 authorization is
claimed. PR #48 is canonical fact, not an architecture conflict,
security-model rejection, or reason to revert the PR or remove V46. A7's
then-current statement `B1 = PLANNED / NOT AUTHORIZED` remains historical.

The F1E-R2 residual gap remains `UsernameNotFoundException` at the AppUser
lookup boundary inside `JwtAuthenticationFilter`. Current states remain:

```text
F1E-R2 = IMPLEMENTED / CANONICAL / DEFAULT-OFF / RESIDUAL GAP OPEN
F1E = PARTIAL / NOT CLOSED
F1F = IMPLEMENTED / CANONICAL / DORMANT
B1 = IMPLEMENTED / CANONICAL / RELATIONAL AUTHORIZATION REGISTRY FOUNDATION
B2 = PLANNED / NOT AUTHORIZED
```

The approved/frozen decision
`LOGOS-HARD-001-F1E-R2-CLOSE-IA-001-DEC-001` remains valid against
`001fa70108d6640e85f01be643d71177935fb40c` because both approved closure
paths are byte-identical at the A7 and current Logos baselines:

```text
src/main/java/com/josecjuniors/logossrv/config/jwt/JwtAuthenticationFilter.java
= 246e05367286c53ef024f5b62d80829698d32461

src/test/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionSecurityPostgresTest.java
= 992898982d93bd5635501dbf4d78395ca37935fe
```

PR #48 did not modify either approved closure path or `SecurityConfig.java`.
It did modify `WorkloadSpringSecurityIntegrationPostgresTest.java` to exercise
grant persistence while the pre-B2 `denyAll` barrier remains; that is not the
approved closure test path. Therefore the previous 1-production + 1-existing-
test closure decision remains valid and no re-preflight is required. This A8
documentation gate does not perform the implementation.

The current serialized path is:

```text
F1E-R2 residual closure → B2 → C1 → C2
```

B1 is removed from the future implementation queue. B2 remains blocked until
the F1E-R2 fix is implemented, independently reviewed, merged canonically,
post-merge CI succeeds, and F1E is formally reconciled as closed.

After A8 becomes canonical, the next gate is
`LOGOS-HARD-001-F1E-R2-CLOSE-IMPL-001-R2`, an implementation retry under the
existing approved decision, using a fresh physically independent Logos clone.
The exact implementation scope remains one production path and one existing
test path. This A8 documentation reconciliation does not authorize that work.

Current boundaries remain:

```text
V46 = B1 authorization registry foundation
V47 = NOT RESERVED
F1E-R2 residual closure migration = NONE
dependency changes = NONE
runtime configuration changes = NONE
workload HTTP activation = NOT AUTHORIZED
authorization grant bootstrap = NOT EXECUTED
T1 trust bootstrap = NOT AUTHORIZED
T2 authorization bootstrap = NOT AUTHORIZED
T3 ownership readiness = NOT AUTHORIZED
LifeOS workload-auth cutover = NOT AUTHORIZED
POC bearer retirement = NOT AUTHORIZED
B2 = PLANNED / NOT AUTHORIZED
HARD-007 = DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER
WORK-001 = DEFERRED
```

## Canonical slice map

| Slice | Owner | Status and invariant |
|---|---|---|
| F1A | Logos | V45 trust/replay persistence, IMPLEMENTED / CANONICAL |
| F1B | Logos | Trust domain/read adapter and P-256/SPKI validation, IMPLEMENTED / CANONICAL |
| F1C | Logos | Signed assertion verifier core, IMPLEMENTED / CANONICAL |
| F1D | Logos | Durable `issuer + jti` replay consumption and normalized authentication, IMPLEMENTED / CANONICAL |
| F1E | Logos | Spring Security workload adapter foundation, IMPLEMENTED / CANONICAL / DORMANT; overall F1E PARTIAL / NOT CLOSED |
| F1E-R2 | Logos | Exact workload chain wiring, IMPLEMENTED / CANONICAL / DEFAULT-OFF / RESIDUAL GAP OPEN (`UsernameNotFoundException` handling) |
| F1F | Logos | Administrative trust lifecycle capability, IMPLEMENTED / CANONICAL / DORMANT |
| B1 | Logos | HARD-002 relational authorization registry persistence/domain foundation, IMPLEMENTED / CANONICAL; no grants seeded; no evaluator/enforcement |
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

F1A/F1B/F1C/F1D must not be re-planned as future work. F1C produces a
`VerifiedWorkloadAssertion`; F1D consumes replay and establishes the
authenticated workload principal.

## Canonical F1D evidence

F1D consumes replay identity `issuer + jti` using the V45 replay table with
database-backed `INSERT ... ON CONFLICT (issuer, jti) DO NOTHING` semantics:
an inserted row is first use and a conflict is replay. The replay guard uses
an independent `REQUIRES_NEW` transaction, so replay consumption survives an
outer rollback and is never restored after later authorization, business, or
server failure. Concurrent identical assertions permit at most one
authentication completion. Invalid F1C assertions do not invoke replay
consumption. Replay-store failure fails closed without an authenticated
principal; HTTP 503 translation remains F1E scope.

F1D transforms `VerifiedWorkloadAssertion` into an `AuthenticatedPrincipal`
only after successful consumption:

```text
principalType = WORKLOAD
principalId = lifeos
authenticationMethod = ASYMMETRIC_SIGNED_ASSERTION
credentialIdentity = verified kid
authenticationStatus = VERIFIED
```

PR #44 added no Flyway migration; F1D migration remains **NONE**. Its replay
cleanup support deletes rows only when `expires_at < now - acceptedClockSkew`.
Canonical Logos already had `@EnableScheduling` in `LogosSrvApplication`;
PR #44 did not need to introduce it. `WorkloadAssertionReplayCleanupScheduler`
is a Spring-wired `@Component`, limited to `@Profile("!test")`, and its
`@ConditionalOnProperty` defaults to enabled when
`logos.security.workload.replay-cleanup.enabled` is absent. Thus it is
eligible/active at application-context level in a normal non-test context
unless explicitly disabled. This does not prove that any deployed instance
actually executed a cleanup cycle. Replay cleanup is HARD-001 authentication
state housekeeping and is distinct from the unauthorized HARD-004 delivery
recovery scheduler.

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

Canonical capabilities include `F1A → F1B → F1C → F1D → F1E` with default-off
F1E-R2 wiring, canonical dormant F1F trust administration, and B1's relational
authorization registry foundation. F1E-R2 still has an open closure gap, so the
current serialized remaining Logos path is:

```text
F1E-R2 residual closure → B2 → C1 → C2
```

B1 is already canonical and has been removed from the future implementation
queue.

D1 and E1 are safe parallel candidates after separate authorization when their
file allowlists and migrations do not overlap and all cross-system contracts
remain frozen. D2 follows the additive contract as needed; E2 follows E1.
F, G1, and G2 are cutover/activation boundaries, not automatic continuations.
Overlapping Logos work in workload security, `SecurityConfig`, progression or
subject controllers, and the Flyway directory must be serialized; only the
canonical remote main is evidence.

## Migration and ownership policy

Logos V46 is canonical for the B1 authorization registry foundation. V47 is
not reserved. The F1E-R2 residual closure requires no migration. Each future
implementation pre-flight reads the then-current canonical head and uses the
next available LifeOS Alembic or Logos Flyway revision. A repository migration
must leave that repository valid independently; no cross-repository transaction
is assumed.

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

## Current next Logos action — A8

The next gate is:

```text
LOGOS-HARD-001-F1E-R2-CLOSE-IMPL-001-R2
IMPLEMENTATION RETRY UNDER THE EXISTING APPROVED / FROZEN DECISION
```

This A8 documentation reconciliation does not implement the residual fix.
Closure implementation is the next gate only after A8 is canonical, using a
fresh physically independent Logos clone and the already approved/frozen 1+1
scope. This A8 gate does not begin that implementation.

```text
HARD-007 = DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER
WORK-001 = DEFERRED
implementation overall = PARTIAL
F1A-F1D = IMPLEMENTED / CANONICAL
F1E = PARTIAL / NOT CLOSED
F1E-R2 = IMPLEMENTED / CANONICAL / DEFAULT-OFF / RESIDUAL GAP OPEN
F1F = IMPLEMENTED / CANONICAL / DORMANT
B1 = IMPLEMENTED / CANONICAL / RELATIONAL AUTHORIZATION REGISTRY FOUNDATION
B2/C1/C2 = PLANNED / NOT AUTHORIZED
real trust bootstrap = NOT EXECUTED
authorization grant bootstrap = NOT EXECUTED
workload HTTP operational activation = NOT ACTIVE
cutover/productionization = NOT AUTHORIZED
remaining path = F1E-R2 residual closure → B2 → C1 → C2
next gate = LOGOS-HARD-001-F1E-R2-CLOSE-IMPL-001-R2 / IMPLEMENTATION RETRY UNDER THE EXISTING APPROVED / FROZEN DECISION
this plan itself = DOES NOT AUTHORIZE ADDITIONAL IMPLEMENTATION OR OPERATIONAL ACTIVATION
```
