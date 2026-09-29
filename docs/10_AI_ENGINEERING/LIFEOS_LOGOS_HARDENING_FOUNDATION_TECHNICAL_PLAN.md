# LifeOS ↔ Logos Hardening Foundation Technical Plan

## Status

```text
LIFEOS-LOGOS-HARDENING-TP-001-DEC-001 = APPROVED / FROZEN / CANONICAL / AMENDED
LIFEOS-LOGOS-HARDENING-TP-001-DEC-001-A1 = APPROVED / FROZEN
LIFEOS-LOGOS-HARDENING-TP-001-A4 = HISTORICAL F1E DORMANT FOUNDATION + RESIDUAL F1E-R2 DECISION
LIFEOS-LOGOS-HARDENING-TP-001-A5 = HISTORICAL CANONICAL F1F ADVANCEMENT / SEQUENCING DEVIATION
LIFEOS-LOGOS-HARDENING-TP-001-A6 = HISTORICAL F1E-R2 CLOSURE + F1F SEQUENCING RECONCILIATION
LIFEOS-LOGOS-HARDENING-TP-001-A7 = HISTORICAL F1E-R2 CLOSURE CORRECTION + RESIDUAL HUMAN-AUTH GAP RESTORED
LIFEOS-LOGOS-HARDENING-TP-001-A8 = HISTORICAL CANONICAL B1 ADVANCEMENT + CANONICAL F1E-R2 RESIDUAL CLOSURE
LIFEOS-LOGOS-HARDENING-TP-001-A9 = HISTORICAL CANONICAL CHECKPOINT; B2 DESIGN SUPERSEDED FOR CURRENT IMPLEMENTATION DESIGN
LIFEOS-LOGOS-HARDENING-TP-001-A10 = CURRENT B2 R2 TECHNICAL DECISION APPROVED / FROZEN / IMPLEMENTATION NOT AUTHORIZED
Foundation Technical Plan = APPROVED / FROZEN / CANONICAL / RECONCILED
implementation overall = PARTIAL
F1A-F1D = IMPLEMENTED / CANONICAL
F1E PR #45 foundation = IMPLEMENTED / CANONICAL / DORMANT
F1E overall = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1E-R2 = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1F = IMPLEMENTED / CANONICAL / DORMANT TRUST ADMINISTRATION CAPABILITY
```

This document is a documentation-only implementation sequencing plan. It
does not itself authorize additional implementation or operational activation,
bootstrap, deployment, or mutation.

## Baselines and governance

The A7 current-state correction used LifeOS canonical
`4fea64478b1053c724b56d234d66fbc8d671dc1b`; A8 used LifeOS canonical
`47a8d4a8eb12714fccb75c3f4d6591617f6ef1f2`; A9 uses LifeOS canonical
`3f4cf47531c7a1e00167919eef612b08958da8a8` after PR #121's canonical A8
metadata correction. Its merge subject is `docs(governance): correct canonical
A8 metadata (#121)`, parent `c2418867008b3e3b6c289446de7ae8f5b175b0d2`,
tree `84fcb2fd287fa109bdc800454ce759aa210120bb`, and scope is the two
canonical governance documents (+8 / -33). The required current LifeOS push
run `36504632848` completed successfully for this head with Static quality,
Tests and coverage, and Alembic migration all green. PR #121 is housekeeping
and does not invalidate A8, B1, F1E closure, the B2 pre-flight, or its frozen
decision. PR #117 is CLOSED / NOT MERGED / SUPERSEDED / DO NOT MERGE. The A7
Logos reference was
`d475838e529e32a81074094f291f45892076e9f5`; PR #48 advanced Logos to
`001fa70108d6640e85f01be643d71177935fb40c` with canonical B1, and PR #49
advanced it to the A8 baseline
`bc13dce086c865d1db4a4811b764fdc2bdd155d7` with canonical F1E-R2 closure. The structural architecture
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

## Historical A8 — canonical B1 advancement and F1E-R2 residual closure

A7 remains the historical gap-open checkpoint. A8 reconciles the canonical
advancement chronology: PR #48 made B1 canonical, then PR #49 closed the F1E-R2
residual gap. The Logos baseline sequence is:

```text
d475838e529e32a81074094f291f45892076e9f5
→ 001fa70108d6640e85f01be643d71177935fb40c (PR #48 / B1)
→ bc13dce086c865d1db4a4811b764fdc2bdd155d7 (PR #49 / F1E-R2 closure)
```

PR #48 canonically implements `LOGOS-HARD-002-B1` as the relational
authorization registry foundation through V46. The registry and domain/store
capabilities remain as documented above: applicable principal/operation/source/
namespace dimensions, semantic uniqueness, `insertIfAbsent(...)`, and
`findExact(...)`. The registry is empty; no grant was seeded, no
`WORKLOAD/lifeos` grant was inserted, and authorization bootstrap did not
occur. B1 is not B2: no authorization evaluator or enforcement was introduced,
and grant presence does not grant request permission.

B1 advanced before F1E-R2 residual closure. This is a GOVERNANCE SEQUENCING
DEVIATION; no retroactive B1 authorization is claimed. PR #48 and V46 remain
canonical; no rollback is requested.

PR #49 merged as:

```text
PR #49 = LOGOS-HARD-001-F1E-R2 — Close unknown human subject authentication gap
base = 001fa70108d6640e85f01be643d71177935fb40c
head = 6d8daede87ddaa821f9914ed24aaf196a37dce9c
merge = bc13dce086c865d1db4a4811b764fdc2bdd155d7
parent = 001fa70108d6640e85f01be643d71177935fb40c
tree = 5f81e369238a73fd4be5b2d0c1155eb0be3e61e3
commit = fix(security): keep unknown human JWT subject unauthenticated (#49)
files = 2 / +40 / -1
PR CI = 36499176463 / pull_request / SUCCESS / test SUCCESS
post-merge CI = 36499878899 / push / SUCCESS / test SUCCESS
```

Its exact files are `JwtAuthenticationFilter.java` and the existing
`ProgressionExecutionSecurityPostgresTest.java`. At AppUser lookup the filter
catches only `UsernameNotFoundException`, continues the filter chain
unauthenticated, and returns. Existing `JwtException` behavior remains. It
adds no broad `RuntimeException`, `Exception`, or `AuthenticationException`
catch. No `SecurityConfig` or workload security component changed.

The canonical regression
`validHumanBearerForUnknownSubjectRemainsUnauthenticated` uses a unique
synthetic subject and a generated valid human JWT; it verifies the subject is
absent from `app_user` before and after the protected GET and expects 403. The
test uses `JdbcTemplate` count queries rather than the pre-flight suggestion
`AppUserRepository.findByEmail(...)`. This is INFORMATIONAL / ACCEPTABLE
IMPLEMENTATION VARIANCE: it establishes the same missing-user invariant in the
approved existing integration test file without changing production scope.

The residual defect is CLOSED IN CANONICAL LOGOS. Current states are:

```text
F1E foundation = IMPLEMENTED / CANONICAL / DORMANT
F1E-R2 = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1E = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1F = IMPLEMENTED / CANONICAL / DORMANT
B1 = IMPLEMENTED / CANONICAL / RELATIONAL AUTHORIZATION REGISTRY FOUNDATION
B2 = PLANNED / NOT AUTHORIZED
HARD-001 implementation foundation = COMPLETE / CANONICAL / NOT OPERATIONALLY ACTIVATED
```

The B1-before-F1E-R2-closure ordering remains a historical sequencing
deviation. Both prerequisites now exist canonically; B2 still needs its own
authorization gate. The current remaining path is:

```text
B2 → C1 → C2
```

After A8 becomes canonical, the next gate is
`LOGOS-HARD-002-B2-TP-001` — Authorization Evaluator / Enforcement Technical
Preflight, a READ-ONLY TECHNICAL PREFLIGHT / IMPLEMENTATION AUTHORIZATION
REVIEW. It does not authorize implementation. Its future review will define
default-deny authorization through the B1 registry; no grant is inserted by
this A8 reconciliation.

The `WorkloadAuthenticationProvider` unexpected `RuntimeException` mapping to
`AuthenticationServiceException` / 503 remains MINOR / FAIL-CLOSED / DEFERRED;
it does not reopen F1E closure.

Current boundaries remain:

```text
Flyway current = V46
V47 = NOT RESERVED
authorization grants seeded = NONE
authorization bootstrap = NOT EXECUTED
workload HTTP activation = NOT AUTHORIZED / default false
T1 trust bootstrap = NOT AUTHORIZED
T2 authorization bootstrap = NOT AUTHORIZED
T3 ownership readiness = NOT AUTHORIZED
LifeOS workload-auth cutover = NOT AUTHORIZED
POC bearer retirement = NOT AUTHORIZED
HARD-007 = DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER
WORK-001 = DEFERRED
```

## Historical A9 — B2 technical decision approved / frozen; implementation not authorized

> A9 remains valid historical canonical governance. It records that B2
> implementation was NOT AUTHORIZED, the earlier technical decision was
> frozen, no B2 code or real grant existed, and workload activation had not
> occurred. Its design and 7-production / 4-test allowlist are SUPERSEDED FOR
> CURRENT IMPLEMENTATION DESIGN by A10 / R1-R2. This is post-A9 technical
> refinement, not A9 or B1 invalidation, rollback, incident, implementation
> drift, or runtime defect. No code was implemented under A9; no rollback is
> required. The historical detail below is deliberately retained.

A9 records the frozen human decision
`LOGOS-HARD-002-B2-TP-001-DEC-001 = APPROVED / FROZEN`. The B2 technical
pre-flight is complete and its design is approved/frozen; B2 implementation
remains NOT AUTHORIZED. A8 is preserved as the historical canonical
reconciliation of B1 and F1E-R2. PR #121 is a canonical A8 metadata /
housekeeping correction only. PR #117 is CLOSED / NOT MERGED / SUPERSEDED /
DO NOT MERGE. The current LifeOS baseline is
`3f4cf47531c7a1e00167919eef612b08958da8a8`; canonical Logos remains
`bc13dce086c865d1db4a4811b764fdc2bdd155d7`.

The approved B2 design is a generic, read-only, Spring Security-agnostic
authorization evaluator backed by `AuthorizationGrantStore.findExact(...)`.
Its decision is `ALLOW` or `DENY`; it has no grant mutation capability.
Enforcement in this slice is limited to `PROGRESSION_EXECUTE`. It does not
authorize workload enforcement for execution reads, history reads, or subject
provisioning.

The conceptual evaluator API is:

```java
AuthorizationDecision evaluate(
    AuthenticatedPrincipal principal,
    AuthorizationOperation operation,
    Optional<AuthorizationSource> source,
    Optional<AuthorizationNamespace> namespace)
```

Prefer `AuthorizationDecision` nested in `AuthorizationEvaluator` unless
implementation evidence requires otherwise. Authorization identity uses only
`AuthenticatedPrincipal.principalType` and `principalId`. Require
`AuthenticationStatus.VERIFIED` before lookup; a non-VERIFIED principal
denies without lookup. Credential identity/`kid`, assertion `jti`, and
authentication method are not grant dimensions.

Authorization requires exact equality across principal type, principal ID,
operation, and every applicable source/namespace dimension. Missing grant,
wrong principal ID, wrong operation, wrong source, or wrong namespace denies.
There are no wildcards, prefixes, fallback or implicit global grants,
trust-derived grants, roles, or partial-dimension matches. The current
`PrincipalType` enum contains only WORKLOAD; do not expand it merely to
manufacture a wrong-type test. Non-VERIFIED is presently unreachable because
the status enum contains only VERIFIED.

For `PROGRESSION_EXECUTE`, derive source from normalized
`request.execution.source` and namespace from normalized
`request.subject.namespace`. Do not include external ID, idempotency key,
configuration, details, `kid`, or `jti` in the authorization key.

Frozen request processing order:

```text
deserialize request
→ validate envelope
→ validate required source/namespace presence
→ normalize ProgressionExecutionIdentity
→ normalize ExternalSubjectReference
→ construct AuthorizationSource
→ construct AuthorizationNamespace
→ evaluate authorization
→ ALLOW only: call progression execution use case
```

Null, malformed, or invalid source/namespace returns 400 Bad Request; explicitly
avoid an unmapped null failure. A valid normalized request without an exact
grant returns generic 403 Forbidden.

Enforce explicitly at the `ProgressionExecutionController` /
web-application boundary after deserialization, validation, and normalization,
before `ExecuteIdempotentExternalSubjectProgressionUseCase.execute(...)`.
Servlet-filter body parsing, `@PreAuthorize` request-body expressions, and
Spring authority synthesis are rejected. Prefer
`@AuthenticationPrincipal AuthenticatedPrincipal` or equivalent explicit,
typed MVC injection; avoid static `SecurityContextHolder` lookup unless
implementation evidence proves explicit injection infeasible.

For the exact conditional workload POST chain, replace only
`denyAll()` with `authenticated()`; do not use `permitAll()`. The workload
authentication token retains empty authorities. Authentication and
authorization remain separate.

Default-deny invariant:

```text
authenticated workload + valid normalized request + no exact grant
→ 403
→ execution use case NEVER CALLED
→ no durable progression / XP / subject / configuration mutation
```

The exact grant `WORKLOAD / lifeos / PROGRESSION_EXECUTE / source=lifeos /
namespace=lifeos` allows continuation to the existing progression use case.
No canonical grant is seeded by B2.

Preserve `authentication → replay jti consumption → authorization`. A denied
first-use assertion remains consumed; retry of the same assertion returns 401.
Never release replay consumption after authorization denial. Controller entry
for validation, normalization, and authorization is permitted; business
execution and durable mutation must not begin before ALLOW.

Known authorization-registry availability failures (recognized connection,
resource, or transient persistence availability errors) fail closed with a
generic 503 Service Unavailable. Do not broadly translate RuntimeException.
Persisted authorization row/domain reconstruction corruption fails closed with
generic 500 Internal Server Error and must not be misclassified by the global
IllegalArgumentException-to-400 handler. The B1 query and schema remain
unchanged; the JDBC adapter may narrowly translate recognized availability
failures and row reconstruction corruption into typed authorization application
exceptions. These responses must not expose grant dimensions, principal IDs,
grant existence, SQL/database details, `kid`, or trust details.

Human execution/history GETs, subject provisioning, public authentication,
and human JWT semantics remain unchanged. C1 and C2 remain PLANNED / NOT
AUTHORIZED; B2 authorization is not ownership. Flyway remains V46, no B2
migration or V47 reservation is authorized, and there are no dependency or
runtime configuration changes. Workload activation remains absent/default
false. T1/T2/T3 bootstrap, workload cutover, and POC bearer retirement remain
NOT AUTHORIZED. HARD-007 remains deferred / productionization required later;
WORK-001 remains deferred.

The frozen implementation candidate is exactly seven production paths.

ADD:
1. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluator.java`
2. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationRegistryUnavailableException.java`
3. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationRegistryCorruptedException.java`

MODIFY:
4. `src/main/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionController.java`
5. `src/main/java/com/josecjuniors/logossrv/config/SecurityConfig.java`
6. `src/main/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStore.java`
7. `src/main/java/com/josecjuniors/logossrv/adapters/in/web/exception/GlobalExceptionHandler.java`

The frozen test candidate is exactly four paths.

ADD:
1. `src/test/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluatorTest.java`

MODIFY:
2. `src/test/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionControllerTest.java`
3. `src/test/java/com/josecjuniors/logossrv/config/security/workload/WorkloadSpringSecurityIntegrationPostgresTest.java`
4. `src/test/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStorePostgresTest.java`

A required eighth production path or fifth test path requires human review; the
allowlists must not be silently expanded. Evaluator tests cover exact allow,
missing grant, and every constructible principal/operation/source/namespace
mismatch. Controller tests prove normalized dimensions reach the evaluator,
DENY returns generic 403 without the execution use case, ALLOW preserves the
existing normalized call, and invalid/null dimensions return 400 before lookup.
Workload integration tests cover no grant, wrong-source and wrong-namespace
grants, exact-grant allow, replay consumption and retry, existing missing/
malformed/human assertion behavior, authentication infrastructure 503, and
human-route isolation. Store integration tests cover the narrow typed adapter
failure translation without duplicating the already canonical B1 exact-match
persistence matrix. Tests may create ephemeral grants and must clean them; no
runtime/bootstrap grant is inserted.

The decision accepts the completed pre-flight recommendations subject to the
explicit frozen boundaries above. A9 does not authorize implementation. After
A9 is merged, canonical, and post-merge LifeOS CI is green, the next gate is
`LOGOS-HARD-002-B2-IMPL-001` — BOUNDED IMPLEMENTATION AUTHORIZATION /
EXCLUSIVE-WRITER PRE-FLIGHT. It may implement only these seven production and
four test paths. The remaining path is:

```text
B2 → C1 → C2
```

## A10 — current B2 R2 technical design; implementation not authorized

`LIFEOS-LOGOS-HARDENING-TP-001-A10` is the current documentation-only
reconciliation. A9 remains historical canonical state; its B2 design is
SUPERSEDED FOR CURRENT IMPLEMENTATION DESIGN. The current technical authority
is executed read-only gate `LOGOS-HARD-002-B2-TP-001-R2`, APPROVED / FROZEN.
A10 does not invent DEC-002. B2 implementation remains NOT AUTHORIZED.

A9 remains the valid checkpoint where implementation was not authorized, its
earlier design was frozen, no B2 code or real grant existed, and workload
activation had not occurred. PR #122 merged at
`579328182034f4059fd7a7701f4ea0b223db96f1`; post-merge run `36507368056`
succeeded with all required jobs, 811 tests, and 98.54% coverage. This
refinement is not A9/B1 invalidation, rollback, incident, implementation drift,
or runtime defect. No code was implemented under A9; no rollback is required.
The historical A9 decision and its 7-production / 4-test allowlist remain
above as evidence and are not current implementation authority.

### Current architecture and enforcement

Authentication remains assertion verification → replay consumption →
`WorkloadPrincipalAuthenticationToken` → `AuthenticatedPrincipal`.
Authorization identity uses only `principalType + principalId`, operation,
and applicable source/namespace. The Spring-independent
`AuthorizationEvaluator` receives principal, operation, and optional source
and namespace and returns `AuthorizationVerdict` (`ALLOW` / `DENY`). It
requires WORKLOAD and VERIFIED. Exact grant allows; absent or wrong principal,
operation, source, or namespace denies. No wildcard, prefix, fallback,
role/trust-derived grant, cache, or mutation. No `kid`, credential identity,
`jti`, or authentication method as policy identity. Supported operations are
`PROGRESSION_EXECUTE`, `PROGRESSION_EXECUTION_READ`,
`PROGRESSION_HISTORY_READ`, and `SUBJECT_PROVISION`; initial enforcement is
`PROGRESSION_EXECUTE` only.

Enforcement is E3-B custom method security after MVC body binding and before
the controller target. Marker
`com.josecjuniors.logossrv.config.security.authorization.AuthorizeProgressionExecute`
applies only to `ProgressionExecutionController.create(...)`. The bridge
`ProgressionExecuteAuthorizationManager implements
AuthorizationManager<MethodInvocation>` reads the bound request from method
arguments and requires authenticated workload-token and
`AuthenticatedPrincipal` types. It derives operation, source, and namespace
from that request. No manual controller authorization, `@PreAuthorize`, SpEL,
`@P`, servlet body parsing/wrapping, or authority synthesis.

The public pointcut is Spring Framework 6.1.10
`AnnotationMatchingPointcut.forMethodAnnotation(AuthorizeProgressionExecute.class)`.
Spring Security 6.3.1 `AuthorizationMethodPointcuts` is package-private and
must not be imported or called. The named bean
`progressionExecuteAuthorizationAdvisor` is an
`AuthorizationManagerBeforeMethodInterceptor` advisor with
`BeanDefinition.ROLE_INFRASTRUCTURE`. Configure
`@EnableMethodSecurity(prePostEnabled = false)`; `securedEnabled` and
`jsr250Enabled` stay false.

C1 is selected: condition the advisor bean on
`logos.security.workload.http.enabled=true` with `matchIfMissing=false`.
When absent/false, workload chain and advisor are absent, the method marker is
inert, and existing human-chain behavior is unchanged. Enabled workload
routing preserves exact `POST /api/internal/v1/progression/executions` and
changes only `denyAll()` to `authenticated()`; never `permitAll()`. GET
execution/history and subject provisioning remain on the human chain.
Production stays default-off; no operational activation.

Malformed JSON is 400. Missing authorization dimensions and invalid source or
namespace grammar are 403 before controller target invocation; only expected
`IllegalArgumentException` during authorization-dimension construction is
converted to DENY. With valid dimensions and ALLOW, invalid business fields
such as missing configuration/details remain 400. Ordinary denial is 403 and
invokes neither controller target nor use case. A no-grant first assertion is
replay-consumed and receives 403; the same assertion retries as 401 without
evaluator re-entry.

Only bounded Spring `DataAccessException` from
`JdbcAuthorizationGrantStore.findExact(...)` translates to
`AuthorizationRegistryUnavailableException`; no row is ordinary DENY. The
bounded exception maps to generic 503 body
`{"error":"Authorization service temporarily unavailable"}`. No broad
runtime catch. Registry outage after valid workload authentication consumes
replay, returns 503 without business invocation, and retry returns 401.
`AuthorizationRegistryCorruptedException` is historical A9 detail and is not
part of current R2. The exact ephemeral test grant
`WORKLOAD/lifeos/PROGRESSION_EXECUTE/source=lifeos/namespace=lifeos` permits a
fresh valid request to return 200 and call the use case once; no real grant is
inserted.

### Current R2 implementation allowlist — exactly 15 paths

This is future implementation scope only; A10 does not authorize implementation.

New production (6):
1. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluator.java`
2. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationVerdict.java`
3. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/exception/AuthorizationRegistryUnavailableException.java`
4. `src/main/java/com/josecjuniors/logossrv/config/security/authorization/AuthorizeProgressionExecute.java`
5. `src/main/java/com/josecjuniors/logossrv/config/security/authorization/ProgressionExecuteAuthorizationManager.java`
6. `src/main/java/com/josecjuniors/logossrv/config/security/authorization/WorkloadAuthorizationMethodSecurityConfig.java`

Existing production modified (4):
1. `src/main/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionController.java`
2. `src/main/java/com/josecjuniors/logossrv/config/SecurityConfig.java`
3. `src/main/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStore.java`
4. `src/main/java/com/josecjuniors/logossrv/adapters/in/web/exception/GlobalExceptionHandler.java`

New tests (3):
1. `src/test/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluatorTest.java`
2. `src/test/java/com/josecjuniors/logossrv/config/security/authorization/ProgressionExecuteAuthorizationManagerTest.java`
3. `src/test/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStoreTest.java`

Existing tests modified (2):
1. `src/test/java/com/josecjuniors/logossrv/config/security/workload/WorkloadSpringSecurityIntegrationPostgresTest.java`
2. `src/test/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionSecurityPostgresTest.java`

Migration: NONE. Dependency: NONE. No sixteenth path without separate human
review. `JdbcAuthorizationGrantStorePostgresTest.java` remains unchanged; the
new mocked-`JdbcTemplate` unit test tests DataAccessException translation and
canonical PostgreSQL store tests retain real exact-query semantics. Default-off
regression retains `SecurityFilterChain` count one and asserts the named
advisor absent. Enabled-context regression proves advisor active, no-grant and
wrong-dimension 403, exact-grant ALLOW/200, one business invocation, replay,
and outage. No human POST fixture is required for this gate.

B1 and V46 remain canonical and unchanged. No port/schema change, migration,
dependency, real grant, bootstrap, T2, activation, cutover, or productionization
is included. Next gate remains `LOGOS-HARD-002-B2-IMPL-001` — BOUNDED
IMPLEMENTATION AUTHORIZATION / EXCLUSIVE-WRITER PRE-FLIGHT; it may authorize
only this 15-path allowlist. The path remains B2 → C1 → C2.

## Canonical slice map

| Slice | Owner | Status and invariant |
|---|---|---|
| F1A | Logos | V45 trust/replay persistence, IMPLEMENTED / CANONICAL |
| F1B | Logos | Trust domain/read adapter and P-256/SPKI validation, IMPLEMENTED / CANONICAL |
| F1C | Logos | Signed assertion verifier core, IMPLEMENTED / CANONICAL |
| F1D | Logos | Durable `issuer + jti` replay consumption and normalized authentication, IMPLEMENTED / CANONICAL |
| F1E | Logos | Spring Security workload adapter, IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF |
| F1E-R2 | Logos | Exact workload chain wiring, IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF; PR #49 closes missing AppUser subject handling |
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

Canonical capabilities include `F1A → F1B → F1C → F1D → F1E` with closed,
default-off F1E-R2 wiring, canonical dormant F1F trust administration, and
B1's relational authorization registry foundation. The current serialized
remaining Logos path is:

```text
B2 → C1 → C2
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

## Current next Logos action — A10

The next gate after A10 canonicalization is:

```text
LOGOS-HARD-002-B2-IMPL-001
BOUNDED IMPLEMENTATION AUTHORIZATION / EXCLUSIVE-WRITER PRE-FLIGHT
```

The read-only R2 technical gate is complete and
`LOGOS-HARD-002-B2-TP-001-R2` is APPROVED / FROZEN. Historical A9
`LOGOS-HARD-002-B2-TP-001-DEC-001` is superseded for current implementation
design, not removed from A9 history. B2 implementation remains NOT AUTHORIZED
until that next gate and its separate authorization.

```text
HARD-007 = DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER
WORK-001 = DEFERRED
implementation overall = PARTIAL
F1A-F1D = IMPLEMENTED / CANONICAL
F1E = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1E-R2 = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1F = IMPLEMENTED / CANONICAL / DORMANT
B1 = IMPLEMENTED / CANONICAL / RELATIONAL AUTHORIZATION REGISTRY FOUNDATION
B2/C1/C2 = PLANNED / NOT AUTHORIZED
real trust bootstrap = NOT EXECUTED
authorization grant bootstrap = NOT EXECUTED
workload HTTP operational activation = NOT ACTIVE
cutover/productionization = NOT AUTHORIZED
remaining path = B2 → C1 → C2
B2 preflight = COMPLETE / R2 TECHNICAL DECISION APPROVED / FROZEN
A9 B2 design = HISTORICAL / SUPERSEDED FOR CURRENT IMPLEMENTATION DESIGN
A10 = CURRENT / R2 TECHNICAL DECISION APPROVED / FROZEN
current B2 technical authority = LOGOS-HARD-002-B2-TP-001-R2
current B2 allowlist = 15 paths
B2 implementation = NOT AUTHORIZED
next gate = LOGOS-HARD-002-B2-IMPL-001 / BOUNDED IMPLEMENTATION AUTHORIZATION / EXCLUSIVE-WRITER PRE-FLIGHT
this plan itself = DOES NOT AUTHORIZE ADDITIONAL IMPLEMENTATION OR OPERATIONAL ACTIVATION
```
