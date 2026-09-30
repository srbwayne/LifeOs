# NEXT_TASK.md

## Current Authoritative State — LIFEOS-LOGOS-001 POC Verified / Closed

| Field | Value |
|---|---|
| Repository/closure publication | `25322af61d81c3fc95253d4f2ce3c3e50b97e5f7` |
| Canonical source implementation | `a4e9758a553ffd924303bd8e871183314642320f` |
| Repository Alembic | `0011` |
| Operational DB documented revision | `0011` |
| Selected initiative | `LIFEOS-LOGOS-001 — Reading → Logos POC Integration` |
| Initiative state | `VERIFIED / CLOSED` |
| Architecture decision | `LIFEOS-LOGOS-001A-DEC-001 — APPROVED` |
| Architecture amendment | `LIFEOS-LOGOS-001A-A1-DEC-001 — APPROVED` |
| Architecture | APPROVED / FROZEN / AMENDED |
| Technical Plan | APPROVED / FROZEN / AMENDED |
| Source implementation | IMPLEMENTED / CANONICAL / CLOSED |
| Runtime POC | EXECUTED / VERIFIED / CLOSED |
| Real E2E | ESTABLISHED FOR THE BOUNDED POC |
| Original `LIFEOS-LOGOS-001D` | HISTORICAL HARD STOP AFTER MUTATION POINT / LOCAL VERIFIER DEFECT |
| `LIFEOS-LOGOS-001D-RECOVERY-001` | PASS |
| Historical replay | NOT EXECUTED |
| Productionization | NOT AUTHORIZED |
| WORK-001 | PRODUCT CONTRACT APPROVED / FROZEN / TEMPORARILY DEFERRED AT ARCHITECTURE GATE / IMPLEMENTATION NOT AUTHORIZED |
| Post-POC priority decision | APPROVED — OPTION C |
| Selected direction | REUSABLE STRUCTURAL HARDENING BEFORE PRODUCTIZATION DECISION |
| Current decision state | OPTION C SELECTED; HARDENING ARCHITECTURE APPROVED / FROZEN |
| Hardening architecture | APPROVED / FROZEN / AMENDED BY `LIFEOS-LOGOS-001G-R1-A1` |
| Immediate foundation | HARD-001 / HARD-002 / HARD-003 / HARD-005 / HARD-004 / HARD-006 |
| Deployment boundary | HARD-007 DEFERRED / PRODUCTIONIZATION_REQUIRED_LATER |
| HARD-001 | APPROVED / FROZEN |
| Workload trust model | ASYMMETRIC WORKLOAD-SIGNED ASSERTION |
| Workload principal | WORKLOAD / lifeos |
| External IdP | NOT REQUIRED |
| Human AppUser for service authentication | PROHIBITED |
| Opaque service-key fallback | NOT SELECTED |
| Replay control | REQUIRED |
| HARD-002 | APPROVED / FROZEN |
| Authorization model | LOGOS-MANAGED RELATIONAL AUTHORIZATION REGISTRY |
| Initial workload authorization | `WORKLOAD / lifeos`: `PROGRESSION_EXECUTE` only; `source=lifeos`; `namespace=lifeos` |
| Authorization default | DENY |
| LifeOS read grants | NOT GRANTED |
| LifeOS subject provisioning grant | NOT GRANTED |
| HARD-003 | APPROVED / FROZEN |
| HARD-003 ownership model | STATEFUL OWNERSHIP LIFECYCLE / IMMUTABLE-BY-DEFAULT |
| External-subject ownership lifecycle | APPROVED / FROZEN — `LIFEOS-LOGOS-001J-DEC-001` |
| HARD-005 | APPROVED / FROZEN |
| Correlation model | OPTION B — STABLE DELIVERY-ROOT PLUS PER-ATTEMPT REQUEST IDENTITY |
| Correlation root | LifeOS Delivery ID |
| Business execution identity | `source + idempotencyKey` |
| Attempt identity | `attemptNumber + requestId` |
| LifeOS read grants | NOT GRANTED |
| HARD-004 | APPROVED / FROZEN |
| HARD-004 policy | POLICY B — EXPLICIT BOUNDED RECOVERY LIFECYCLE |
| Retry budget | `maxAttempts` / finite / numeric value deferred |
| Recovery claim | LEASE WITH EXPIRY + STALE-WORKER PROTECTION |
| Attempt reservation | BEFORE HTTP |
| Configuration retry | STRICT ORIGINAL KEY + REVISION |
| Same-owner ordering | BLOCK BY DEFAULT / EXPLICIT RELEASE |
| Historical replay | NOT AUTHORIZED |
| Scheduler | NOT AUTHORIZED |
| Implementation | NOT AUTHORIZED |
| HARD-006 | APPROVED / FROZEN |
| HARD-006 model | OPTION B — BOUNDED WORKLOAD-KEY PROVIDER + DEPLOYMENT-INJECTED SECRET MATERIAL/REFERENCE + STARTUP-IMMUTABLE LOADING |
| Private-key owner | LifeOS / authorized deployment boundary |
| `kid` | NEVER REUSED |
| Rotation | NEW TRUST BEFORE NEW SIGNING; OLD ISSUANCE STOPS BEFORE NORMAL RETIREMENT |
| Multi-instance retirement | ALL ACTIVE EMITTERS OFF OLD KEY BEFORE NORMAL REVOCATION |
| Compromise | IMMEDIATE REVOCATION / FAIL CLOSED / NO FALLBACK |
| Credential loss | NEW CREDENTIAL / SAME WORKLOAD PRINCIPAL; OLD CREDENTIAL NON-ACTIVE AFTER REPLACEMENT |
| Private-key ordinary backup | NO |
| Trust bootstrap | LOGOS ADMINISTRATIVE / NO TOFU / NO SELF-REGISTRATION |
| POC bearer | RETIRE AT WORKLOAD CUTOVER / NO HIDDEN FALLBACK |
| Secret technology | DEFERRED |
| HARD-007 | DEFERRED |
| Hardening foundation architecture | COMPLETE / FROZEN |
| Foundation Technical Plan | APPROVED / FROZEN / CANONICAL / RECONCILED |
| Technical Plan decision | `LIFEOS-LOGOS-HARDENING-TP-001-DEC-001` — APPROVED |
| Technical Plan amendment | `LIFEOS-LOGOS-HARDENING-TP-001-DEC-001-A1` — APPROVED |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A2` — CANONICAL F1D ADVANCEMENT |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A3` — F1E REVIEW + REPLAY CLEANUP SCHEDULING |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A4` — F1E CANONICAL DORMANT FOUNDATION + RESIDUAL R2 DECISION |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A5` — CANONICAL F1F DORMANT TRUST ADMINISTRATION ADVANCEMENT |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A6` — F1E-R2 CLOSURE + F1F SEQUENCING RECONCILIATION AS RECORDED AT A6 |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A7` — F1E-R2 CLOSURE CORRECTION + RESIDUAL HUMAN-AUTH GAP RESTORED |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A8` — CANONICAL B1 ADVANCEMENT + CANONICAL F1E-R2 RESIDUAL CLOSURE |
| Historical canonical decision checkpoint | `LIFEOS-LOGOS-HARDENING-TP-001-A9` — B2 DESIGN APPROVED / FROZEN; IMPLEMENTATION NOT AUTHORIZED AT THAT CHECKPOINT |
| Historical canonical checkpoint | `LIFEOS-LOGOS-HARDENING-TP-001-A10` — CANONICAL / CURRENT R2 TECHNICAL AUTHORITY |
| Historical reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A11` — CANONICAL CHECKPOINT; CURRENT CONCLUSIONS SUPERSEDED BY A12 |
| Current reconciliation | `LIFEOS-LOGOS-HARDENING-TP-001-A12` — B2 SEQUENCING-DEVIATION / R2 FORWARD-ALIGNMENT RECONCILIATION |
| LifeOS canonical baseline for A8 | `47a8d4a8eb12714fccb75c3f4d6591617f6ef1f2` |
| LifeOS A9 input baseline | `3f4cf47531c7a1e00167919eef612b08958da8a8` |
| LifeOS A9 canonical merge | `579328182034f4059fd7a7701f4ea0b223db96f1` |
| LifeOS A9 canonical CI | `36507368056` — push / completed / SUCCESS; 811 tests / 98.54% coverage; all three required jobs SUCCESS |
| LifeOS A10 input baseline | `579328182034f4059fd7a7701f4ea0b223db96f1` |
| LifeOS A11 input baseline | `80e40c8fd3531e68135926c1e60afd3f73377b3d` |
| LifeOS canonical A11 merge | `24b2ab6cc62ea25c9f98b03d54f28b1d8658e67a` |
| LifeOS A12 input baseline | `24b2ab6cc62ea25c9f98b03d54f28b1d8658e67a` |
| LifeOS PR #123 canonical merge | `80e40c8fd3531e68135926c1e60afd3f73377b3d` — merged after canonical Logos B2 |
| LifeOS post-A10 CI | `36641497128` — push / completed / SUCCESS; all three required jobs SUCCESS |
| Logos B2 canonical SHA | `096fc1a5124358997771d1bb0b0db291a2d81935` — parent `bc13dce086c865d1db4a4811b764fdc2bdd155d7`; tree `07c5f93b60a520bc768ee58e1c9d2a10ae8afd80` |
| Logos PR #50 | MERGED / CANONICAL — B2 implementation |
| Logos B2 post-merge CI | `36639505288` — push / completed / SUCCESS; 404 tests / 0 failures / 0 errors / 0 skips |
| PR #121 | MERGED — `docs(governance): correct canonical A8 metadata`; base `c2418867008b3e3b6c289446de7ae8f5b175b0d2`; head `267b12432558f8fcf63dc24fa593cf393468fe21`; merge `3f4cf47531c7a1e00167919eef612b08958da8a8`; 1 commit / 2 documentation files / +8 / -33 |
| PR #117 | CLOSED / NOT MERGED / SUPERSEDED / DO NOT MERGE |
| PR #118 | MERGED — `docs(governance): reconcile F1E-R2 closure and F1F sequencing` / `4fea64478b1053c724b56d234d66fbc8d671dc1b` / 2 files / HISTORICAL A6 CHECKPOINT; its premature F1E closure was superseded by A7 gap correction and later closed by canonical PR #49 |
| Logos pre-B2 / F1E-R2 canonical baseline | `bc13dce086c865d1db4a4811b764fdc2bdd155d7` |
| Logos canonical migration | V46 — B1 authorization registry foundation |
| PR #48 | MERGED — `LOGOS-HARD-002-B1 — Add workload authorization registry foundation` / `d475838e529e32a81074094f291f45892076e9f5` → `001fa70108d6640e85f01be643d71177935fb40c` / 1 commit / 18 files / +665 / -4 |
| PR #49 | MERGED — `LOGOS-HARD-001-F1E-R2 — Close unknown human subject authentication gap` / `001fa70108d6640e85f01be643d71177935fb40c` → `bc13dce086c865d1db4a4811b764fdc2bdd155d7` / 1 commit / 2 files / +40 / -1 |
| B1 | IMPLEMENTED / CANONICAL / RELATIONAL AUTHORIZATION REGISTRY FOUNDATION |
| B1 sequencing | ADVANCED BEFORE F1E-R2 RESIDUAL CLOSURE / GOVERNANCE SEQUENCING DEVIATION / NO RETROACTIVE AUTHORIZATION |
| Authorization grants seeded | NONE — `WORKLOAD/lifeos` / `PROGRESSION_EXECUTE` grant NOT INSERTED |
| B2 preflight | `LOGOS-HARD-002-B2-TP-001` — PRE-FLIGHT COMPLETE |
| A9 B2 decision | `LOGOS-HARD-002-B2-TP-001-DEC-001` — APPROVED / FROZEN; HISTORICAL CANONICAL DECISION CHECKPOINT |
| B2 implementation authorization at PR #50 merge | NOT PRESENT; no retroactive authorization |
| B2 current status | CANONICAL A9 IMPLEMENTATION PRESENT / DEFAULT-OFF / R2 FORWARD ALIGNMENT OPEN |
| B2 canonical scope | 11 paths — 7 production + 4 tests |
| A10/R2 technical authority | CURRENT / APPROVED / FROZEN |
| A11 current conclusions | HISTORICAL / SUPERSEDED BY A12 |
| B2 sequencing deviation | YES — IMPLEMENTATION ADVANCED BEFORE EXPLICIT AUTHORIZATION |
| Authorization bypass / rollback | NO / NO |
| Grant bootstrap / workload activation | NOT EXECUTED / NOT AUTHORIZED |
| Logos F1A | IMPLEMENTED / CANONICAL |
| Logos F1B | IMPLEMENTED / CANONICAL |
| Logos F1C | IMPLEMENTED / CANONICAL — SIGNED WORKLOAD ASSERTION VERIFIER CORE |
| Logos F1D | IMPLEMENTED / CANONICAL — REPLAY + AUTHENTICATION COMPLETION |
| F1D governance sequencing | IMPLEMENTED BEFORE PLANNED IA GATE; RECONCILED AS CANONICAL EXTERNAL FACT; NO RETROACTIVE AUTHORIZATION CLAIM |
| Logos F1E foundation (PR #45) | IMPLEMENTED / CANONICAL / DORMANT |
| F1E overall | IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF |
| F1E decision | `LOGOS-HARD-001-F1E-R1-DEC-001` — APPROVED / FROZEN |
| F1E-R2 (PR #47 + PR #49) | IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF — PR #49 closes `UsernameNotFoundException` handling in `JwtAuthenticationFilter` |
| Workload security behavior | Exact conditional POST chain with `authenticated()`; current PR #50 uses historical manual B2 evaluation; default-off; R2 alignment open |
| Logos F1F | IMPLEMENTED / CANONICAL / DORMANT TRUST ADMINISTRATION CAPABILITY |
| F1F sequencing | ADVANCED BEFORE F1E-R2 CLOSURE / GOVERNANCE SEQUENCING DEVIATION / NO RETROACTIVE AUTHORIZATION CLAIM |
| Remaining primary Logos path | B2-R2 FORWARD ALIGNMENT → C1 → C2 |
| Parallel LifeOS candidates | D1 / E1 |
| Operational bootstrap | T1 TRUST / T2 AUTHORIZATION / T3 OWNERSHIP READINESS |
| Authentication cutover | SEPARATE / NOT AUTHORIZED |
| Recovery implementation | SEPARATE / NOT AUTHORIZED |
| Recovery activation | SEPARATE / NOT AUTHORIZED |
| Migration numbering | NEXT AVAILABLE AT IMPLEMENTATION TIME |
| Implementation | PARTIAL — HARD-001 foundation F1A–F1F CANONICAL; operational activation remains separate and inactive |
| F1E-R2 source allowlist | 2 exact paths |
| F1E-R2 test allowlist | 2 exact paths |
| F1E-R2 migration | NONE |
| F1E-R2 dependencies | NONE |
| Current next Logos gate | `LOGOS-HARD-002-B2-R2-RECOVERY-IMPL-001` — BOUNDED FORWARD-CORRECTION IMPLEMENTATION AUTHORIZATION / EXCLUSIVE-WRITER PREFLIGHT |

## Historical Logos Hardening Reconciliation — A9

> **Historical canonical checkpoint.** A9 remains valid and preserved as the
> checkpoint where B2 implementation was NOT AUTHORIZED, the approved design
> was frozen, no B2 code or real grant existed, and workload activation had not
> occurred. Logos PR #50 later implemented that frozen design canonically, but
> implementation authorization was not present when PR #50 merged. This is a
> sequencing deviation, not retroactive authorization. A9 remains valid and was
> not invalidated or rolled back; A12 reconciles current external state.

A9 historically canonicalized the approved and frozen decision
`LOGOS-HARD-002-B2-TP-001-DEC-001`. A8 remains the historical canonical
checkpoint. PR #121 is a canonical A8 metadata / housekeeping correction and
does not invalidate A8, B1, F1E closure, the completed B2 pre-flight, or its
frozen human decision. PR #117 is CLOSED / NOT MERGED / SUPERSEDED / DO NOT
MERGE.

At LifeOS baseline `3f4cf47531c7a1e00167919eef612b08958da8a8`, with canonical
Logos baseline `bc13dce086c865d1db4a4811b764fdc2bdd155d7`, the frozen state is:

```text
LIFEOS-LOGOS-HARDENING-TP-001-A9 =
B2 TECHNICAL DECISION APPROVED / FROZEN /
IMPLEMENTATION NOT AUTHORIZED

LOGOS-HARD-002-B2-TP-001 = PRE-FLIGHT COMPLETE
LOGOS-HARD-002-B2-TP-001-DEC-001 = APPROVED / FROZEN
B2 design = APPROVED / FROZEN
B2 implementation = NOT AUTHORIZED
```

The approved design uses a generic, read-only, Spring Security-independent
evaluator backed by `AuthorizationGrantStore.findExact(...)`, with an
`ALLOW` / `DENY` decision. Enforcement in this slice is limited to
`PROGRESSION_EXECUTE`; workload reads, history, and subject provisioning are
not enabled. The evaluator maps only
`AuthenticatedPrincipal.principalType` and `principalId`, requires
`AuthenticationStatus.VERIFIED` before lookup, and has no grant mutation
capability. Credential identity/`kid`, assertion `jti`, and authentication
method are not authorization dimensions.

Authorization requires an exact match across principal type, principal ID,
operation, and all applicable dimensions. No wildcard, prefix, fallback,
implicit global, trust-derived, role-derived, or partial-dimension grant is
allowed. Missing grant and dimension mismatch deny. For execute, source comes
from normalized `request.execution.source`; namespace comes from normalized
`request.subject.namespace`. External ID, idempotency key, configuration,
details, `kid`, and `jti` are excluded from the grant key.

The frozen request sequence is:

```text
deserialize request
→ validate envelope and required source/namespace presence
→ normalize ProgressionExecutionIdentity
→ normalize ExternalSubjectReference
→ construct AuthorizationSource
→ construct AuthorizationNamespace
→ evaluate authorization
→ ALLOW only: call progression execution use case
```

Null, malformed, or invalid source/namespace returns 400 Bad Request. A valid
normalized request without an exact grant returns generic 403 Forbidden.
Enforcement is explicit at the `ProgressionExecutionController` /
web-application boundary after deserialization and normalization, before
`ExecuteIdempotentExternalSubjectProgressionUseCase.execute(...)`. Filter
body parsing, `@PreAuthorize` request-body authorization, and Spring authority
synthesis are rejected for this slice. Use typed MVC principal injection via
`@AuthenticationPrincipal AuthenticatedPrincipal` or a compile-equivalent
explicit argument; do not use static `SecurityContextHolder` lookup without
implementation evidence that explicit injection is infeasible.

For the exact conditional workload POST chain, the only authorized rule
transition is `denyAll()` to `authenticated()`; never `permitAll()`.
Workload token authorities remain empty. Authentication remains distinct from
registry authorization.

The default-deny invariant is: authenticated workload + valid normalized
request + no exact grant gives 403, never calls the execution use case, and
causes no durable progression, XP, subject, or configuration mutation. The
exact grant `WORKLOAD / lifeos / PROGRESSION_EXECUTE / source=lifeos /
namespace=lifeos` allows continuation to the existing use case. No canonical
grant is seeded.

Replay order remains authentication → durable replay `jti` consumption →
authorization. A denied first-use assertion remains consumed; retry returns
401. Replay state is never released after denial. The controller may enter
for validation, normalization, and authorization, but business execution must
not begin before ALLOW.

Known authorization-registry availability failures fail closed as generic 503.
Persisted-row/domain reconstruction corruption fails closed as generic 500 and
must not fall through to the global IllegalArgumentException-to-400 mapping.
Use narrow typed translations only: no broad RuntimeException catch. The B1
query/schema stay unchanged; the JDBC adapter may narrowly translate recognized
availability failures and row reconstruction corruption into typed application
exceptions. Denial, availability, and corruption responses must not reveal
grant dimensions, principal ID, grant presence, SQL, database details, `kid`,
or trust details.

Human execution/history GETs, subject provisioning, public authentication,
and human JWT behavior remain unchanged. C1 and C2 remain PLANNED / NOT
AUTHORIZED; B2 does not establish ownership. V46 remains current; no B2
migration or V47 reservation, dependency, runtime configuration, or grant
bootstrap is authorized. Workload HTTP remains absent/default false. T1/T2/T3
bootstrap, workload cutover, and POC bearer retirement remain NOT AUTHORIZED.
HARD-007 remains deferred / productionization required later; WORK-001 remains
deferred. B2 remains dormant until separately authorized operational actions.

The frozen B2 production allowlist is exactly seven paths:

ADD:
- `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluator.java`
- `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationRegistryUnavailableException.java`
- `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationRegistryCorruptedException.java`

MODIFY:
- `src/main/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionController.java`
- `src/main/java/com/josecjuniors/logossrv/config/SecurityConfig.java`
- `src/main/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStore.java`
- `src/main/java/com/josecjuniors/logossrv/adapters/in/web/exception/GlobalExceptionHandler.java`

The frozen test allowlist is exactly four paths:

ADD:
- `src/test/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluatorTest.java`

MODIFY:
- `src/test/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionControllerTest.java`
- `src/test/java/com/josecjuniors/logossrv/config/security/workload/WorkloadSpringSecurityIntegrationPostgresTest.java`
- `src/test/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStorePostgresTest.java`

No eighth production or fifth test path is authorized without human review. Tests cover exact allow, absent grant and each constructible mismatch, normalized controller dimensions, generic denial and use-case non-invocation, allow-path preservation, invalid dimensions, no-grant/wrong-dimension/exact-grant workload requests, replay preservation, existing authentication failures, human-route isolation, and narrowly translated adapter failures. Wrong principal type is currently unconstructible because the canonical enum only contains WORKLOAD; do not expand it solely for a test. Non-VERIFIED is likewise currently unreachable with the one-value status enum.

The decision accepts the 45 pre-flight recommendations subject to these explicit
frozen details. A9 does not itself authorize implementation. After A9 is merged,
canonical, and post-merge CI is green, the next gate is
`LOGOS-HARD-002-B2-IMPL-001` — BOUNDED IMPLEMENTATION AUTHORIZATION /
EXCLUSIVE-WRITER PRE-FLIGHT. That gate may consider only the frozen seven
production and four test paths.

## Historical Logos Hardening Reconciliation — A8

`LIFEOS-LOGOS-HARDENING-TP-001-A8` reconciles canonical Logos PR #48 and
PR #49. A7 remains the historical gap-open checkpoint. A8 records the current
canonical state and the advancement sequence:

```text
d475838e529e32a81074094f291f45892076e9f5
→ 001fa70108d6640e85f01be643d71177935fb40c (PR #48 / B1)
→ bc13dce086c865d1db4a4811b764fdc2bdd155d7 (PR #49 / F1E-R2 closure)
```

PR #48 establishes B1 as the canonical relational authorization registry
foundation, including Flyway V46, operation/dimension applicability, semantic
uniqueness, `insertIfAbsent(...)`, and `findExact(...)`. The registry remains an
empty foundation: no grants were seeded, no `WORKLOAD/lifeos` grant was
inserted, and no authorization bootstrap occurred. B1 does not implement B2
evaluation or enforcement; grant presence is not authorization enforcement.

B1 advanced before F1E-R2 residual closure. This remains a GOVERNANCE
SEQUENCING DEVIATION with no retroactive B1 authorization. PR #48 and V46 are
canonical facts; no rollback is requested.

PR #49 is canonical and closes the F1E-R2 missing-human-subject gap. Its merge
commit is `bc13dce086c865d1db4a4811b764fdc2bdd155d7`, parent
`001fa70108d6640e85f01be643d71177935fb40c`, with tree
`5f81e369238a73fd4be5b2d0c1155eb0be3e61e3`. It modifies exactly
`JwtAuthenticationFilter.java` and the existing
`ProgressionExecutionSecurityPostgresTest.java` regression file. The filter
catches only `UsernameNotFoundException` around AppUser lookup, continues the
chain unauthenticated, and retains existing `JwtException` handling. No broad
`RuntimeException`, `Exception`, or `AuthenticationException` catch was added.
PR #49's pull-request CI run `36499176463` and post-merge push CI run
`36499878899` both completed successfully with the required `test` job green.

The canonical regression
`validHumanBearerForUnknownSubjectRemainsUnauthenticated` creates a valid JWT
for a unique synthetic subject, verifies that subject is absent from
`app_user` before the request and remains absent afterward, and asserts 403 on
the protected GET. The test uses `JdbcTemplate` count queries instead of the
pre-flight's suggested `AppUserRepository.findByEmail(...)`; this is an
INFORMATIONAL / ACCEPTABLE IMPLEMENTATION VARIANCE that proves the same absence
invariant within the approved existing test path.

Current slice states are:

```text
F1E foundation = IMPLEMENTED / CANONICAL / DORMANT
F1E-R2 = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1E = IMPLEMENTED / CANONICAL / CLOSED / DEFAULT-OFF
F1F = IMPLEMENTED / CANONICAL / DORMANT
B1 = IMPLEMENTED / CANONICAL / RELATIONAL AUTHORIZATION REGISTRY FOUNDATION
B2 = PLANNED / NOT AUTHORIZED
HARD-001 implementation foundation = COMPLETE / CANONICAL / NOT OPERATIONALLY ACTIVATED
```

PR #49 changes no `SecurityConfig.java` or workload security component. It
adds no migration, dependency, or runtime configuration change. Flyway V46
remains current; V47 is not reserved. Workload HTTP remains default-off and
NOT AUTHORIZED for activation. T1/T2/T3 bootstrap, cutover, and POC bearer
retirement remain NOT AUTHORIZED. HARD-007 remains deferred /
productionization required later; WORK-001 remains deferred.

The B1-before-F1E-R2-closure order is historical sequencing deviation. Both
prerequisites now exist canonically, but B2 requires its own authorization.
The remaining path is:

```text
B2 → C1 → C2
```

After A8 becomes canonical, the next gate is
`LOGOS-HARD-002-B2-TP-001` — Authorization Evaluator / Enforcement Technical
Preflight, a READ-ONLY TECHNICAL PREFLIGHT / IMPLEMENTATION AUTHORIZATION
REVIEW. It does not authorize B2 implementation.

## Historical Logos Hardening Reconciliation — A7

`LIFEOS-LOGOS-HARDENING-TP-001-A7` is the current-state correction at LifeOS
canonical baseline `4fea64478b1053c724b56d234d66fbc8d671dc1b`. A6 and canonical
PR #118 remain historical evidence: PR #118 recorded F1E as closed and B1 as
next, but that current-state conclusion is superseded by A7. No Logos code
change followed PR #47, and the canonical implementation still has the
residual AppUser lookup failure described below. This correction does not
revert PR #118 or reject PR #47, and it does not claim retroactive IA approval.

PR #47 remains `IMPLEMENTED / CANONICAL / DEFAULT-OFF`. F1E-R2 is
`IMPLEMENTED / CANONICAL / DEFAULT-OFF / RESIDUAL GAP OPEN`; F1E is
`PARTIAL / NOT CLOSED`. At the canonical Logos reference
`d475838e529e32a81074094f291f45892076e9f5`, `JwtAuthenticationFilter` catches
`JwtException` while extracting and validating a JWT, but calls
`userDetailsService.loadUserByUsername(userEmail)` outside that handling.
`UserDetailsServiceImpl.loadUserByUsername(...)` throws
`UsernameNotFoundException` when no AppUser exists for the JWT subject. Thus a
validly structured human JWT whose subject has no AppUser may let that expected
lookup exception escape the filter. No external HTTP status is asserted.

The completed R2 pre-flight identified the expected filter catch set as
`JwtException` plus `UsernameNotFoundException`; PR #47 implements only the
first part. The next gate is
`LOGOS-HARD-001-F1E-R2-CLOSE-IA-001`, a read-only residual closure pre-flight /
implementation authorization review. A possible production change to
`JwtAuthenticationFilter.java` and regression test in
`ProgressionExecutionSecurityPostgresTest.java` are review hypotheses only;
A7 authorizes neither implementation.

SecurityConfig R2 wiring remains canonical with no residual SecurityConfig gap
identified. The provider's unexpected `RuntimeException` to
`AuthenticationServiceException` to 503 behavior remains a deferred minor,
fail-closed item. F1F remains implemented/canonical/dormant, and its sequencing
deviation remains recorded. The then-current A7 path was F1E-R2 residual
closure → B1 → B2 → C1 → C2; B1 was then planned and not authorized.
Migration, dependency, and
runtime configuration changes remain none. Workload HTTP activation, T1/T2/T3
bootstrap, LifeOS cutover, and POC bearer retirement remain unauthorized.
HARD-007 remains deferred / productionization required later, and WORK-001
remains deferred.

The first bounded LifeOS → Logos Reading POC is verified and closed. The
retained evidence is `Book = 0RNXGW86RWC70`, `ReadingSession =
0RNXGW8J67V68`, and `Delivery = 0RNXGW8JCPZ17 / DELIVERED`; Logos recorded
one execution, global XP `3`, Conhecimento XP `3`, stress `0`, and an
identical resubmit returned HTTP 200 without duplication. Full evidence is in
`docs/10_AI_ENGINEERING/LIFEOS_LOGOS_001_POC_CLOSURE.md`.

`LIFEOS-LOGOS-001F-DEC-001` recorded the human decision:

```text
APPROVED — OPTION C SELECTED:
REUSABLE STRUCTURAL HARDENING BEFORE PRODUCTIZATION DECISION
```

Reading → Logos remains `VERIFIED / CLOSED AS A BOUNDED POC` and
productionization remains unauthorized. WORK-001 remains approved/frozen and
temporarily deferred. No other initiative is selected automatically.

The human decision `LIFEOS-LOGOS-001F-DEC-001` approved Option C: a minimum
reusable cross-system hardening foundation before any productization decision.
The architecture is approved/frozen and amended by
`LIFEOS-LOGOS-001G-R1-A1`, which places minimum correlation before bounded
recovery. The immediate foundation is HARD-001 Workload Trust, HARD-002 Source
/ Namespace / Operation Authorization, HARD-003 External Subject Ownership,
HARD-005 Minimum Cross-System Correlation, HARD-004 Bounded Delivery Recovery,
and HARD-006 Secret / Configuration Lifecycle. HARD-007 Deployment Boundary is
deferred as `PRODUCTIONIZATION_REQUIRED_LATER`.

Hardening implementation is partial overall because HARD-002, HARD-003 and
other foundation work remain unimplemented. Logos PR #45 is canonical as the
dormant F1E Spring Security adapter foundation, PR #47 is canonical as the
F1E-R2 default-off chain wiring, and PR #46 is canonical as dormant F1F trust
administration. Under current A8 state F1E is IMPLEMENTED / CANONICAL / CLOSED /
DEFAULT-OFF because canonical PR #49 closes the expected AppUser lookup
failure in the human JWT filter. F1F advanced before F1E-R2 closure; this remains a governance
sequencing deviation, with no rollback. The current remaining Logos path is
B2 → C1 → C2. B1 advanced before F1E-R2 closure as
a governance sequencing deviation, without retroactive authorization or
rollback. This does not
authorize bootstrap, cutover, productization, deployment, recovery, historical
replay, or WORK-001 resumption. Remaining unapproved slices remain
unauthorized. This plan does not itself authorize additional implementation or
operational activation.

F1E-R2 wires a conditional workload chain for exactly
`POST /api/internal/v1/progression/executions` behind
`logos.security.workload.http.enabled`, absent/default-disabled in production
configuration. Before B2 the chain uses `denyAll`: authenticated first use
returns 403 after durable replay consumption, replay returns 401, and
authentication infrastructure failure returns 503. This code capability is
not operational activation. No real `WORKLOAD / lifeos` trust bootstrap,
signing credential, or HARD-002 grant is established here; the frozen initial
policy remains architecture-only.

`LIFEOS-LOGOS-001H-DEC-001` approved and froze the asymmetric workload-signed
assertion trust model. LifeOS authenticates as the distinct `WORKLOAD / lifeos`
principal; an external IdP is not required now, human AppUser service
authentication is prohibited, and replay control is required. No keys or
credentials were generated, and implementation remains unauthorized.

`LIFEOS-LOGOS-001I-DEC-001` approved and froze HARD-002 as a
Logos-managed relational authorization registry. The stable authorization
identity is `principalType + principalId`, initially `WORKLOAD / lifeos`.
The initial policy grants only `PROGRESSION_EXECUTE` with `source=lifeos` and
`subject.namespace=lifeos`; default deny applies, and neither read nor subject
provisioning authority is granted. `LIFEOS-LOGOS-001J-DEC-001` then approved
and froze HARD-003 as a stateful ownership lifecycle with immutable-by-default
bindings, controlled transfer/correction, disable/revoke support, and no
ordinary hard delete. Ownership proof, lifecycle persistence, and
implementation remain unselected and unauthorized. `LIFEOS-LOGOS-001L-DEC-001`
then approved and froze HARD-005 as Option B: the LifeOS Delivery ID is the
correlation root, while each attempt has a monotonic attempt number and a new
request ID. Business execution identity remains `source + idempotencyKey`;
correlation metadata does not change idempotency. The next authorized
governance gate is `LIFEOS-LOGOS-001K — HARD-004 BOUNDED DELIVERY RECOVERY
POLICY`. `LIFEOS-LOGOS-001K-DEC-001` then approved and froze Policy B: an
explicit bounded recovery lifecycle with total `maxAttempts` semantics,
lease-based claims, pre-network attempt reservation, strict original
configuration, conservative ambiguous-outcome handling, and default
same-owner blocking with explicit successor release. The numeric budget and
implementation details remain deferred and unauthorized. `LIFEOS-LOGOS-001M-
DEC-001` now approves and freezes Option B: a bounded workload-key provider,
deployment-injected secret material/reference, startup-immutable loading,
controlled rotation, and no hidden bearer fallback. The structural hardening
foundation is complete at the architecture/governance level only. The next
authorized gate is `LIFEOS-LOGOS-HARDENING-TP-001 — FOUNDATION TECHNICAL /
IMPLEMENTATION SEQUENCING REVIEW`.

At the A7 checkpoint, the canonical Logos reference was
`d475838e529e32a81074094f291f45892076e9f5`. PR #41 provides the canonical V45
workload trust/replay persistence foundation, PR #44 provides canonical F1D
replay consumption/authentication completion, PR #45 provides the canonical
dormant F1E adapter foundation, PR #46 provides canonical dormant F1F trust
administration, and PR #47 provides canonical F1E-R2 default-off security-chain
wiring. HARD-001's implementation foundation is complete/canonical, but
runtime route activation, trust seeding, real credentials, LifeOS signing, and
authorization remain unestablished by this governance state.

Productization, WORK-001 resumption, remaining unapproved security/service-
identity slices, recovery implementation, historical replay, observability,
deployment, runtime activation, progression authorization, new migrations,
and redispatch mechanisms remain unauthorized. F1A–F1F, including closed,
default-off F1E-R2, are canonical; current F1E is IMPLEMENTED / CANONICAL /
CLOSED / DEFAULT-OFF. Real trust bootstrap and cutover remain unauthorized and
unexecuted. At this earlier checkpoint, the planned Logos path was B2 → C1 → C2; A11 later recorded the external PR #50 fact, and A12 reconciles the current state below.

Post-A1 HTTP contract hardening =
`a4e9758a553ffd924303bd8e871183314642320f`.
Supported successful Logos execution response = HTTP 200.

`LIFEOS-LOGOS-HARDENING-TP-001-DEC-001` is approved/frozen and amended by
`LIFEOS-LOGOS-HARDENING-TP-001-DEC-001-A1`; A2 through A7 remain historical
checkpoints, with A8 the current reconciliation. A3 records the checkpoint at
which PR #45 was still open/in review/not canonical, and the planned
`LOGOS-HARD-001-F1E-IA-001` was not executed under that identifier and is not
retroactively claimed. A5 records F1F becoming canonical before F1E-R2
closure. A6 records PR #45, PR #46, and PR #47 as canonical and documents its
then-current F1E closure conclusion and B1-first path; A7 corrected that
conclusion for its current state while preserving A6 historically. A8 records
canonical PR #48/B1 advancement and PR #49/F1E-R2 closure, superseding A7 for
current state. B1 advanced before F1E-R2 residual closure as a governance
sequencing deviation; no retroactive B1 authorization is claimed. The F1F
sequencing deviation remains historical fact, not rollback grounds or
retroactive authorization.
D1 and E1 remain parallel LifeOS candidates subject to separate authorization.
T1/T2/T3 bootstrap, authentication cutover, recovery implementation, and
recovery activation remain separate and unauthorized. Migration numbers are
not reserved. Canonical Logos already has `@EnableScheduling`; F1D's
`WorkloadAssertionReplayCleanupScheduler` is Spring-wired under `@Profile("!test")`
and enabled by default unless
`logos.security.workload.replay-cleanup.enabled=false`. This establishes
application-context scheduling eligibility, not that a deployed instance ran
a cleanup cycle. Replay cleanup is HARD-001 housekeeping, distinct from
HARD-004 delivery recovery, which remains unimplemented and unauthorized. The
current next Logos gate, after A8 canonicalization, is
`LOGOS-HARD-002-B2-TP-001` — Authorization Evaluator / Enforcement Technical
Preflight, READ-ONLY TECHNICAL PREFLIGHT / IMPLEMENTATION AUTHORIZATION
REVIEW. B2 implementation remains unauthorized pending its own gate.

---

## Historical Governance State — LIFEOS-LOGOS-001 Architecture / Technical Plan Approved

| Field | Value |
|---|---|
| Decision baseline reviewed | `5ddf709f52f18840e8a76a166e89354b0e748c37` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Selected initiative | `LIFEOS-LOGOS-001 — Reading → Logos POC Integration` |
| Selection | `APPROVED` |
| Architecture / Technical Plan decision | `LIFEOS-LOGOS-001A-DEC-001 — APPROVED` |
| Architecture | APPROVED / FROZEN |
| Technical Plan | APPROVED / FROZEN |
| Source implementation at this checkpoint | NOT YET STARTED |
| Runtime POC | NOT AUTHORIZED |
| Historical replay | NOT AUTHORIZED |
| WORK-001 | PRODUCT CONTRACT APPROVED / FROZEN / TEMPORARILY DEFERRED AT ARCHITECTURE GATE / IMPLEMENTATION NOT AUTHORIZED |
| Next gate at this checkpoint | `LIFEOS-LOGOS-001B — SOURCE IMPLEMENTATION` |

Canonical plan: `docs/10_AI_ENGINEERING/LIFEOS_LOGOS_001_ARCHITECTURE_TECHNICAL_PLAN.md`.
Architecture / Technical Plan: APPROVED / FROZEN / AMENDED
Amendment: `LIFEOS-LOGOS-001A-A1-DEC-001 — APPROVED`
Source implementation at this checkpoint: NOT YET STARTED / NOT CANONICAL
Next gate at this checkpoint: `LIFEOS-LOGOS-001B — SOURCE IMPLEMENTATION`

At this historical checkpoint, no source implementation, dependency change,
migration, runtime POC, subject bootstrap, historical replay, or WORK-001
resumption was authorized.

---


## Historical Governance State — LIFEOS-LOGOS-001 Integration Selection

| Field | Value |
|---|---|
| Decision baseline reviewed | `3121e7667d289e91c4b707e41ab9dae1e5399cb4` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Selected initiative | `LIFEOS-LOGOS-001 — Reading → Logos POC Integration` |
| Product Owner decision | `APPROVED` |
| Activity | `ReadingSession` |
| Downstream | `Logos Progression HTTP V1` |
| WORK-001 | PRODUCT CONTRACT APPROVED / FROZEN / TEMPORARILY DEFERRED AT ARCHITECTURE GATE / IMPLEMENTATION NOT AUTHORIZED |
| Next authorized gate | `LIFEOS-LOGOS-001A — READING → LOGOS POC ARCHITECTURE / TECHNICAL PLAN` |

The Product Owner selected the first bounded real LifeOS → Logos integration
before continuing WORK-001 architecture work. WORK-001 remains approved at
Product Contract level and is temporarily deferred at its architecture gate,
not cancelled or rejected. After the bounded pilot closes, initiative priority
must be re-evaluated explicitly.

### Historical Next Authorized Gate

`LIFEOS-LOGOS-001A — READING → LOGOS POC ARCHITECTURE / TECHNICAL PLAN`

Type: READ-ONLY ARCHITECTURE / TECHNICAL PLAN.

Purpose: freeze the HTTP adapter, payload mapping, typed settings, dependency
wiring, failure classification, test strategy, manual bootstrap, manual
end-to-end validation, and file allowlist. No implementation is authorized by
LIFEOS-LOGOS-001G.

---

## Historical Governance State — WORK-001 Product Contract Approved (preserved)

| Field | Value |
|---|---|
| Decision baseline reviewed | `6b44108ee58bd2d9bf990875c1f2b12b22146a55` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Selected initiative | `WORK-001` |
| Selection decision | `LIFEOS-PRIORITY-002-DEC-001 — APPROVED` |
| Product Contract decision | `WORK-001-PC-DEC-001 — APPROVED` |
| WORK-001 | PRODUCT CONTRACT APPROVED / FROZEN / ARCHITECTURE NOT YET APPROVED / TECHNICAL PLAN NOT YET APPROVED / IMPLEMENTATION NOT AUTHORIZED |
| WORK-001 identity | RESOLVED — Registro de Treino |
| Next authorized gate | `WORK-001-ARCH-001 — ARCHITECTURE REVIEW` |

This historical state records the prior WORK-001 gate. It is preserved for
traceability; the current selection and next authorized gate are recorded
above.

---

## Historical Governance State — WORK-001 Selected (preserved)

| Field | Value |
|---|---|
| Decision baseline reviewed | `e7a37fc186cc3ec2dd35e5076b2f78c7b3787b2b` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| HAB-001 | IMPLEMENTED / ACTIVE |
| HAB-002 | IMPLEMENTED / ACTIVE |
| HAB-003 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| WORK-001 | SELECTED / PRODUCT CONTRACT NOT YET FROZEN / IMPLEMENTATION NOT AUTHORIZED |
| WORK-001 identity | UNRESOLVED / CONFLICTING |
| Selection decision | `LIFEOS-PRIORITY-002-DEC-001 — APPROVED: WORK-001` |
| Current selected initiative | `WORK-001` |
| Next authorized gate | `WORK-001 PRODUCT CONTRACT REVIEW` |

No WORK implementation is authorized. This selection authorizes only a
read-only Product Contract / semantic review. It does not authorize
Architecture, Technical Plan, source, tests, migration, runtime, operational
DB, Game, Health, or frontend work.

### Next Authorized Gate

`WORK-001 PRODUCT CONTRACT REVIEW`

Type: READ-ONLY PRODUCT CONTRACT / SEMANTIC REVIEW.

Purpose: reconcile WORK-001 identity and freeze the smallest coherent Workout
product contract before Architecture. The identity question remains open:
the Feature Catalog says `Cadastro de modalidades`, while the PRD and Workout
Epic say `Registro de Treino`.

---

## Current Authoritative State — HAB-003 Source Implementation Canonical

| Field | Value |
|---|---|
| Decision baseline reviewed | `e47af64907488a07697ef248041612d9ad4ac13c` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Therapy V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| Habits V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| HAB-001 | IMPLEMENTED / ACTIVE |
| HAB-002 | IMPLEMENTED / ACTIVE |
| HAB-003 | PRODUCT CONTRACT APPROVED / FROZEN / ARCHITECTURE APPROVED / FROZEN / TECHNICAL PLAN APPROVED / FROZEN / SOURCE IMPLEMENTED / CANONICAL / OPERATIONALLY VERIFIED / ACTIVE / CLOSED |
| Technical Plan Decision | `HAB-003-TP-DEC-001 — APPROVED` |
| Technical Plan Amendment | `HAB-003-TP-AMEND-DEC-001 — APPROVED` |
| Canonical implementation | `ca75af380e12515d1cdd1ebf74d29ca207cd9647` |
| Implementation PR | `#86` |
| Operational activation document | `docs/10_AI_ENGINEERING/HAB_003_OPERATIONAL_ACTIVATION.md` |
| Operational mutation during HAB-003 activation | NONE |
| Main CI | `35171823950 — 3/3 SUCCESS` |
| HAB-004 | DEFERRED |
| HAB-005 | DEFERRED |
| Progression for Habits | NOT ELIGIBLE / UNCHANGED |
| Logos for Habits | NOT INTEGRATED |
| Noema/AI for Habits | NOT INTEGRATED |
| Habit event dispatch | NO |
| Current selected initiative | NONE |
| Next authorized gate | `LIFEOS NEXT INITIATIVE SELECTION — PRODUCT / ARCHITECTURE PRIORITIZATION REVIEW` |

HAB-003 source implementation is canonical and operationally verified. HAB-003 is OPERATIONALLY ACTIVE / CLOSED. No next feature implementation is authorized. HAB-004 and HAB-005 remain DEFERRED.

### Next Authorized Gate

`LIFEOS NEXT INITIATIVE SELECTION — PRODUCT / ARCHITECTURE PRIORITIZATION REVIEW`

Type: READ-ONLY GOVERNANCE / PRIORITIZATION REVIEW.

Purpose: re-evaluate the canonical backlog after HAB-003 closure and select the next bounded LifeOS initiative. No next feature implementation is authorized.

---

## Historical Governance State — Superseded (Technical Plan Approval)

| Field | Value |
|---|---|
| Decision baseline reviewed | `78bec6221ceabe4d345d2758e18cf08037b08b4c` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Therapy V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| Habits V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| HAB-001 | IMPLEMENTED / ACTIVE |
| HAB-002 | IMPLEMENTED / ACTIVE |
| HAB-003 | PRODUCT CONTRACT APPROVED / FROZEN / ARCHITECTURE APPROVED / FROZEN / TECHNICAL PLAN APPROVED / FROZEN / IMPLEMENTATION NOT AUTHORIZED |
| Technical Plan Decision | `HAB-003-TP-DEC-001 — APPROVED` |
| Technical Plan Document | `docs/10_AI_ENGINEERING/HAB_003_TECHNICAL_PLAN.md` |
| Technical Plan Amendment | `HAB-003-TP-AMEND-DEC-001 — APPROVED` |
| Production implementation paths | 9 |
| Test implementation paths | 5 |
| Total implementation paths | 14 |
| HAB-004 | DEFERRED |
| HAB-005 | DEFERRED |
| Progression for Habits | NOT ELIGIBLE / UNCHANGED |
| Logos for Habits | NOT INTEGRATED |
| Noema/AI for Habits | NOT INTEGRATED |
| Habit event dispatch | NO |
| Current selected initiative | HAB-003 — Sequência (Streak) |
| Next authorized gate | `HAB-003-IA-001R — IMPLEMENTATION AUTHORIZATION / PRE-FLIGHT REVIEW RERUN` |

Implementation remains NOT AUTHORIZED. HAB-004 and HAB-005 remain DEFERRED;
Progression, Logos, Noema/AI, and event dispatch remain unchanged and excluded.

### Next Authorized Gate

`HAB-003-IA-001R — IMPLEMENTATION AUTHORIZATION / PRE-FLIGHT REVIEW RERUN`

Type: READ-ONLY IMPLEMENTATION AUTHORIZATION / PRE-FLIGHT REVIEW.

Purpose: re-run implementation readiness against the amended 14-path allowlist,
using CPython 3.11.x and completing the disposable query-plan validation before
a separate human implementation decision.

The IA gate does not authorize implementation by itself.

---

## Historical Governance State — Superseded

> Documento oficial que define a única tarefa autorizada para execução.

---

# Current Authoritative State — HAB-003 Architecture Approved

| Field | Value |
|---|---|
| Decision baseline reviewed | `68e18225043344217fd1bcd1c27561a3f210bbae` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Therapy V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| Habits V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| HAB-001 | IMPLEMENTED / ACTIVE |
| HAB-002 | IMPLEMENTED / ACTIVE |
| HAB-003 | PRODUCT CONTRACT APPROVED / FROZEN / ARCHITECTURE APPROVED / FROZEN / TECHNICAL PLAN NOT YET APPROVED / IMPLEMENTATION NOT AUTHORIZED |
| HAB-004 | DEFERRED |
| HAB-005 | DEFERRED |
| Progression for Habits | NOT ELIGIBLE / UNCHANGED |
| Logos for Habits | NOT INTEGRATED |
| Noema/AI for Habits | NOT INTEGRATED |
| Habit event dispatch | NO |
| Current selected initiative | HAB-003 — Sequência (Streak) |
| Next authorized gate | HAB-003-TP-001 — TECHNICAL PLAN / IMPLEMENTATION SLICING REVIEW |

## Next Authorized Gate

`HAB-003-TP-001 — TECHNICAL PLAN / IMPLEMENTATION SLICING REVIEW`

Type: READ-ONLY TECHNICAL PLAN / IMPLEMENTATION PLANNING

Purpose: produce the exact implementation plan for the already-frozen HAB-003
product contract and architecture.

Authorized:

- exact source/test file inventory and symbols to add or modify;
- exact repository projection signature/query and pure calculator contract;
- application query/DTO design and dependency-injection wiring plan;
- exact HTTP route, method, schema, explicit `evaluation_date` transport and inactive-Habit representation;
- error mapping, test matrix, SQL/query-plan validation strategy, implementation slicing and allowlist proposal.

Not authorized:

- source modification or architecture/API implementation;
- production code, tests, migrations, runtime or operational DB access;
- HAB-003 implementation or HAB-004/HAB-005 work;
- Progression, XP, GAME, Logos, Noema/AI, Analytics or event dispatch integration.

The approved architecture requires `evaluation_date` as an explicit application
query input and forbids a CivilDateProvider, clock abstraction, `date.today()`,
UTC-derived date, server-local date, or implicit timezone inference. If the
Technical Plan cannot define an explicit transport without inventing product
semantics, it must stop with a product-gap report. A later explicit human
decision remains required before implementation.

## Historical Governance State — Superseded

The following section is retained for historical context only.

# Estado Atual — Pós-Ativação Habits V1

| Campo | Valor |
|---|---|
| Canonical main baseline | `7743df8cb5c9df601e8266d545181d88caa1fa7` |
| Repository Alembic | `0011` |
| Operational DB | `0011` |
| Therapy V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| THERAPY-OPS-001 | CLOSED |
| Habits V1 | IMPLEMENTED / OPERATIONALLY ACTIVE / CLOSED |
| HAB-001 | IMPLEMENTED / ACTIVE |
| HAB-002 | IMPLEMENTED / ACTIVE |
| HAB-003 | DEFERRED |
| HAB-004 | DEFERRED |
| HAB-005 | DEFERRED |
| HABITS-OPS-001 | CLOSED |
| HABITS-OPS-001R3 | PASS / EVIDENCE RECONCILED |
| HABITS-OPS-001M | COMPLETE |
| Progression for Habits | NOT ELIGIBLE / UNCHANGED |
| Logos for Habits | NOT INTEGRATED |
| Noema/AI for Habits | NOT INTEGRATED |
| Habit event dispatch | NO |
| Current selected initiative | NONE |
| Next authorized gate | LIFEOS NEXT INITIATIVE SELECTION — PRODUCT / ARCHITECTURE PRIORITIZATION REVIEW |

## Next Authorized Gate

`LIFEOS NEXT INITIATIVE SELECTION — PRODUCT / ARCHITECTURE PRIORITIZATION REVIEW`

Type: READ-ONLY GOVERNANCE / PRIORITIZATION REVIEW

Purpose: evaluate the canonical product backlog and implemented capabilities to
recommend the next bounded LifeOS initiative. This gate may analyze candidates
but must not implement them.

Authorized:

- repository and document inspection;
- backlog/status reconciliation;
- comparison of candidate initiatives;
- architectural dependency analysis;
- recommendation of the next bounded initiative.

Not authorized:

- production code changes;
- migration creation or execution;
- operational DB access;
- runtime mutation;
- HAB-003, HAB-004, or HAB-005 implementation;
- Progression, Logos, or Noema/AI integration;
- new API or frontend implementation.

A later explicit human decision remains required before implementation.

The historical READ closure and planning records below are preserved as historical context.

The planning state below is retained as historical context. Where it conflicts
with this closure section, this section is authoritative for current
operational status.

# Historical Planning State — Superseded

| Campo | Valor |
|---|---|
| ID | LIFEOS-COORDINATED-DATABASE-CUTOVER-0007-0009-RUNTIME-ACTIVATION-REVIEW |
| Iniciativa | LifeOS progression integration governance |
| Status | ARCHITECTURE / OPERATIONAL REVIEW ONLY |
| Tipo | Read-only coordinated cutover and runtime activation review |
| Capability | READ |
| Feature | READ-005 — Livros Concluídos |
| Requisito Funcional | RF-READ-005 — Conclusão de Livro |
| User Story | US-READ-005-001 |
| Product Decision | PD-READ-005 — APPROVED |
| Product Identity | FROZEN |
| Completion Model | AUTOMATIC COMPLETION MILESTONE |
| Completion Semantics | APPROVED / FROZEN |
| Product Specification | APPROVED / FROZEN |
| Product Clarification | PRE-EXISTING COMPLETION / BACKFILL APPROVED |
| Architecture Review | APPROVED |
| Architecture Decision | ADR-0042 — ACCEPTED |
| Architecture | APPROVED / FROZEN |
| Technical Plan | APPROVED / FROZEN |
| Technical Plan Document | docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md |
| Human Technical Review | APPROVED |
| Implementation Authorization Review | PASS |
| Human Implementation Authorization | APPROVED |
| Implementation Program | READ-005 SOURCE IMPLEMENTATION COMPLETE |
| Sprint 09 | READ-005 SOURCE CLOSURE COMPLETE |
| Current Executable Unit | READ-ONLY ARCHITECTURE / OPERATIONAL REVIEW |
| Slice 1 Status | INTEGRATED / FINALIZED |
| Pre-Slice-2 Remediation Status | FINALIZED |
| Slice 2 Status | INTEGRATED / FINALIZED |
| Slice 3 Status | INTEGRATED / FINALIZED |
| Slice 4 Status | INTEGRATED / FINALIZED / MAIN CI PYTHON 3.11 3/3 SUCCESS / RUNTIME ACTIVATION BLOCKED PENDING COORDINATED CUTOVER |
| Slice 5 Status | INTEGRATED / FINALIZED / MAIN CI PYTHON 3.11 3/3 SUCCESS |
| Slice 5 PR | #53 — MERGED |
| Slice 5 Reviewed Source Head | `1e1e7697284a281e460562a9ed13a111ad36ddbc` |
| Slice 5 Integrated Main | `38b8cff8436474e07a2761b3adee9938341ea3a4` |
| Slice 5 Main CI | `33826496903` — 3/3 SUCCESS |
| Slice 5 Validation | CPython 3.11.16 / 502 tests / 502 warning-gate PASS / 98.18% coverage |
| Slice 6 Status | MIGRATION 0008 + BACKFILL IMPLEMENTATION INTEGRATED / REAL-DATA APPLICATION NOT EXECUTED / COORDINATED CUTOVER NOT EXECUTED |
| Slice 7 Status | INTEGRATED / FINALIZED |
| Slice 8 Status | FULL REGRESSION + GOVERNANCE CLOSURE COMPLETE |
| Slice 7 PR | #55 — MERGED |
| Slice 7 Reviewed Source Head | `ba07b3b362813629240f5e9164820a0092c3fec0` |
| Slice 7 Integrated Implementation | `f2c5fc23b9abdaf254541521b7d5df23490f0d38` |
| Slice 7 Integrated Remediation / Main | `7f1b5745194b72801d02a9cbfa63bdc60fc3e459` |
| Slice 7 Main CI | `33937874975` — 3/3 SUCCESS |
| Slice 7 Validation | CPython 3.11.16 / 513 tests / 513 warning-gate PASS / 98.28% coverage |
| Migration 0008 | CODE INTEGRATED / REAL DATABASE NOT APPLIED |
| Migration 0009 | CODE INTEGRATED / REAL DATABASE NOT APPLIED |
| Alembic | Repository: 0009 (head); real `lifeos.db`: 0007 |
| Migration 0008 Real Execution | NO |
| Migration 0009 Real Execution | NO |
| Coordinated Cutover | NO |
| Slice 4 Runtime Activation | NO |
| Slice 5 Deployment | NO |
| Slice 7 Deployment | NO |
| TASK-015 Durable Delivery / Recovery | INTEGRATED / AT-LEAST-ONCE / EXPLICIT RECOVERY ENTRY POINT |
| Progression Downstream | `NoOpProgressionGateway` remains the default |
| TASK-015 Main | `1e3b1c72e19fa1e0b34a668ad636d79f75bd91e3` |
| TASK-015 Main CI | `34034023199` — 3/3 SUCCESS |
| READ-005 Source Implementation | COMPLETE |
| READ-005 Production Deployment | NOT EXECUTED |
| Slice 4 PR | #46 — MERGED |
| Slice 4 Reviewed Source Head | `3f23cdb4f991a0c8381801378b2b0f70267f7d97` |
| Slice 4 Integrated Main | `8201cb9d6e3f79241808c01fe913b232c730188f` |
| Slice 4 Main CI | `33705415321` — 3/3 SUCCESS |
| Slice 4 Validation | CPython 3.11.16 / 483 tests / 483 warning-gate PASS / 98.11% coverage |
| Current Integrated Python Platform | >=3.11 |
| Current Required Branch Checks | Static quality (Python 3.11); Tests and coverage (Python 3.11); Alembic migration (Python 3.11) |
| Python 3.11 Platform Transition | INTEGRATED / FINALIZED |
| Platform PR | #49 — MERGED |
| Platform Main | `f62d4798560cf36025cee021b34c5fb10462cff3` |
| Platform Main CI | `33697509650` — 3/3 SUCCESS |
| Platform Baseline | 465 tests / 98.16% coverage |

## Limite atual de autorização

Python >=3.11 está integrado em `main` pelo PR #49, e a proteção da branch exige
`Static quality (Python 3.11)`, `Tests and coverage (Python 3.11)` e
`Alembic migration (Python 3.11)`.

**AUTHORIZED NOW:** READ-ONLY ARCHITECTURE / OPERATIONAL REVIEW OF THE COORDINATED CUTOVER.

**NOT YET AUTHORIZED:**

- aplicar Migration 0008 a dados reais;
- aplicar Migration 0009 a dados reais;
- executar o cutover coordenado;
- ativar o runtime READ/PROGRESSION;
- deploy do runtime atual;
- ativar Logos, scheduler, worker ou downstream real;
- implementar qualquer nova funcionalidade.

**NEXT DECISION GATE:** `LIFEOS COORDINATED DATABASE CUTOVER 0007 → 0009 + READ/PROGRESSION RUNTIME ACTIVATION — ARCHITECTURE / OPERATIONAL REVIEW`.

Esse gate é somente para análise e planejamento operacional e requer nova decisão
humana antes de qualquer execução. A sequência obrigatória a revisar é
`0007 → 0008 → 0009 → compatible runtime activation`; o backfill histórico da
0008 deve ocorrer com exclusão de escrita em ReadingSession, conforme o requisito
de cutover coordenado do READ-005.

O source de entrega durável TASK-015 está integrado no repositório, mas a
Migration 0008 e a Migration 0009 reais, o cutover, o deployment e a ativação de
runtime permanecem não executados. `dispatch_unresolved()` existe como entrada
explícita de recuperação, mas não é invocado automaticamente. A semântica de
entrega é at-least-once; não há garantia exactly-once.

BookCompletion persistido permanece a fonte durável de verdade. A ocorrência
BookCompleted permanece um seam best-effort in-process. O `NoOpProgressionGateway`
permanece o downstream padrão. Logos continua separado; nenhum contrato HTTP,
auth ou configuração externa foi integrado. Scheduler, worker, Outbox, broker,
Kafka, RabbitMQ, GAME e Noema permanecem fora do escopo desta revisão.

**CURRENT-STATE CONTRADICTIONS:** 0

## Especificação aprovada

- A conclusão ocorre automaticamente na primeira cobertura integral das páginas.
- Cobertura significa páginas únicas cobertas pela união das ReadingSessions.
- Não existe ação manual nem conclusão antecipada.
- O milestone é único por Player + Book e historicamente estável.
- `completed_at` é informação funcional obrigatória, derivada semanticamente do `ended_at` da sessão que provoca a primeira transição.
- Releituras posteriores não alteram a conclusão nem `completed_at`.
- O Book permanece disponível e pode receber novas ReadingSessions.
- Books concluídos devem ser identificáveis pelo Player e historicamente representáveis.
- A ocorrência funcional deve ser disponibilizável externamente; o mecanismo é decisão de arquitetura.
- Efeitos GAME estão fora do escopo e RF-READ-009 permanece deferred.

## Decisão arquitetural aprovada

- BookCompletion dedicado e imutável.
- ReadingProgress continua derivado.
- Book continua sem completion state.
- Session + Completion são atômicos no mesmo UoW e commit.
- Unicidade obrigatória por Player + Book.
- Single logical writer por Book.
- completed_at é persistido semanticamente a partir do ended_at da sessão disparadora.
- Read model dedicado para completion.
- Migration necessária, conceitualmente 0008.
- Backfill dos Books já completos, com reconstrução histórica por ended_at crescente.
- BookCompletion persistido é a fonte durável de verdade.
- Transporte externo durável fica deferred.
- GAME permanece fora do escopo.

## Entregas Existentes

- READ-001: ENTREGUE.
- READ-002: ENTREGUE.
- READ-003: ENTREGUE.
- READ-004: ENTREGUE.
- READ-006: ENTREGUE.
- READ-007: ENTREGUE.
- RF-READ-001..004: ENTREGUES.
- RF-READ-006: ENTREGUE.
- RF-READ-007: ENTREGUE.
- RF-READ-011: ENTREGUE.

## Implementation Authorization

- Human Implementation Authorization Decision: APPROVED (2026-08-18).
- Implementation Program: AUTHORIZED.
- Sprint 09: AUTHORIZED at program level.
- Slice 1 completed implementation, publication, final review and integration.
- PR #31: MERGED via Rebase and Merge.
- Main after Slice 1 integration: `700d7e9e6c66fb4716323c22ef5c4b3693c8d3de`.
- Main CI run `32212825644`: SUCCESS.
- Slice 2 Architectural / Implementation Authorization Review: PASS.
- Human Slice 2 Authorization: APPROVED (2026-08-19).
- Slice 2 Implementation Pre-Flight was BLOCKED by the pre-existing AUTH/CHARACTER SQLite FK write-order defect.
- PRE-SLICE-2 Remediation Pre-Flight: PASS; Human Technical Review: APPROVED.
- PRE-SLICE-2 Remediation: IMPLEMENTED, REVIEWED, MERGED, and FINALIZED through PR #34.
- Slice 2 prerequisite: RESOLVED.
- Slice 2 Implementation Pre-Flight: PASS; Human Technical Review: APPROVED.
- Slice 2 implementation is authorized only through the frozen two-file allowlist below.
- Slices 3..8 remain NOT EXECUTABLE / GATED.
- Sprint 09 authorization is not blanket permission to implement all slices in one branch or PR.

### PRE-SLICE-2 REMEDIATION CLOSURE — AUTH/CHARACTER SQLITE FK WRITE ORDER

Root cause: disconnected AUTH/CHARACTER ORM persistence ordering under immediate
SQLite foreign-key enforcement.

Resolution:

User save
→ UoW flush
→ Player save
→ UoW flush
→ Character save
→ one final commit

PR: #34 — MERGED.
Main: `f1a1af321a85576d1c8d7cba22cc8adf47167258`.
Main CI: `32433670497` — 3/3 SUCCESS.
Local finalization: PASS.
Tests: 440 passed.
Global process-local SQLite FK diagnostic: 440 passed.
`foreign_key_check`: [].

The prerequisite is RESOLVED.

### SLICE 2 - SQLITE INTEGRITY FOUNDATION — CLOSED / INTEGRATED / FINALIZED

Goal: establish the frozen SQLite foreign-key integrity foundation at shared
Engine/connection infrastructure level.

Frozen implementation mechanism:

- SQLAlchemy Engine-class `connect` listener registered in
  `app/shared/infrastructure/database.py` before runtime Engine creation;
- SQLite guard: `isinstance(dbapi_connection, sqlite3.Connection)`;
- SQLite connections execute `PRAGMA foreign_keys = ON`; non-SQLite connections are no-op;
- the listener does not commit, rollback, change transaction mode, isolation level, or use
  `Connection.autocommit`.

Frozen implementation allowlist:

1. `app/shared/infrastructure/database.py` — centralized SQLite-gated Engine listener only.
2. `tests/shared/infrastructure/test_database.py` — new behavioral infrastructure tests only.

Required tests and invariants:

- fresh and multiple direct SQLite Engine connections report `foreign_keys == 1`;
- invalid FK writes fail, valid FK writes succeed, and `foreign_key_check` is clean;
- Alembic online SQLite connection is covered; non-SQLite callback path executes no PRAGMA;
- runtime, current direct test Engines, and Alembic online Engines are covered;
- repositories remain unaware of PRAGMA policy and the complete suite remains green.

Accepted risks:

- shared database infrastructure must be imported before directly created Engines establish
  connections; all current runtime, test, and Alembic paths satisfy this ordering;
- existing scoped test FK listeners may remain; they are redundant and idempotent;
- the guard intentionally supports only the configured built-in `sqlite3` / pysqlite driver.

Permitted scope when Slice 2 executes:

- Engine-level SQLite connection enforcement;
- `PRAGMA foreign_keys = ON`;
- runtime SQLite connection coverage;
- test SQLite connection coverage;
- Alembic online SQLite connection coverage;
- verification that `PRAGMA foreign_keys == 1`;
- verification that invalid foreign-key writes are rejected;
- verification of clean SQLite foreign-key integrity where appropriate;
- unchanged behavior for non-SQLite databases;
- infrastructure-level tests required by this slice.

Slice 2 must not include BookCompletion ORM models, persistence mappers or repositories;
the `book_completions` table, UNIQUE(book_id), completion indexes, migration 0008 or
backfill; BEGIN IMMEDIATE, retry or ReadingSession + Completion transaction integration;
completion detection orchestration; API, GET /book-completions, BookCompleted, EventBus
changes, GAME or any work from Slices 3..8.

Slice 2 closure evidence:

- PR #37: MERGED.
- Canonical main: `432fbbe415e54a2d3d3fb81d972e52133e9f8977`.
- Main CI `32439884304`: 3/3 SUCCESS.
- Local integration finalization: PASS; infrastructure tests: 5 passed;
  AUTH/CHARACTER regression: 4 passed; full suite: 445 passed.
- Coverage: 98.13%; Alembic: 0007 (head); migration 0008: NOT CREATED.
- Runtime SQLite `foreign_keys == 1`; runtime and existing database
  `foreign_key_check`: []. Alembic online SQLite enforcement: confirmed.

Slice 2 is CLOSED / INTEGRATED / FINALIZED.

### SLICE 3 — COMPLETION PERSISTENCE — CLOSED / INTEGRATED / FINALIZED

Slice 3 implementation pre-flight: PASS. Human Technical Review: APPROVED.
Implementation Authorization Review: APPROVED. PR #40 is MERGED; authorized head
`00bc7b4f38e52358970b600f6a5c6064bc38a63a` was integrated into canonical main
`5674df21fcd40fb3e1c29bf3e4d0c303248ec5a0` (parent
`8803474ab748f96cc2fac10704d20b3303789674`). Main CI `32611356740`: 3/3 SUCCESS.
Local integration finalization: PASS.

Frozen domain and ownership contract:

- BookCompletion remains a dedicated immutable Aggregate Root with `id`,
  `book_id`, and `completed_at`; it has no `owner_id`, `user_id`, or `updated_at`.
  Book, ReadingProgress, and the domain aggregate remain unchanged.
- Domain ownership is derived through `BookCompletion.book_id → Book.id → Book.owner_id`.
  The persistence owner-safe lookup derives through
  `BookCompletionModel.book_id → BookModel.id → BookModel.user_id`. The table
  must not persist an owner/user identifier. Wrong-owner lookup returns `None`.
- The repository port is `IBookCompletionRepository`, with exactly
  `save(completion)` and `get_by_book_and_owner(book_id, owner_id)`. The latter
  joins `BookCompletionModel` to `BookModel`, filters completion `book_id` and
  `BookModel.user_id`, and returns `BookCompletion | None`.

Frozen ORM, mapper, and repository contract:

- New `BookCompletionModel` maps `book_completions`: `id` String(26) primary key;
  required and unique `book_id` String(26); required `completed_at`
  DateTime(timezone=True); persistence-only technical `created_at` DateTime with
  the established Python-side `datetime.datetime.now` default. It has no
  relationship, owner/user field, `updated_at`, or cascade.
- `book_id` uses `ForeignKey("books.id", ondelete="RESTRICT")`; one single-column
  uniqueness mechanism (`mapped_column(..., unique=True)`) and no redundant
  standalone non-unique book index. The required composite metadata index is
  `Index("ix_book_completions_completed_at_book_id", "completed_at", "book_id")`.
- `BookCompletionMapper` maps IDs with `to_persistence()` / `from_value()`.
  On load it must call existing `canonicalize_utc_datetime(model.completed_at)`
  before `BookCompletion.restore()`. SQLite may return a naive datetime; the
  domain invariant must not be weakened.
- `SqlAlchemyBookCompletionRepository` receives a Session, uses
  `session.add(BookCompletionMapper.to_persistence(completion))`, and does not
  commit, flush, merge, upsert, replace, update, or execute PRAGMA. The caller/UoW
  owns commit and flush; duplicate Book completion is a database uniqueness error.

Frozen implementation allowlist — exactly six new files; a seventh file requires
human review and STOP:

1. `app/read/domain/ports/book_completion_repository.py`
2. `app/read/infrastructure/persistence/models/book_completion_model.py`
3. `app/read/infrastructure/persistence/mappers/book_completion_mapper.py`
4. `app/read/infrastructure/persistence/repositories/book_completion_repository.py`
5. `tests/read/integration/test_book_completion_mapper.py`
6. `tests/read/integration/test_book_completion_repository.py`

Tests must use disposable SQLite plus explicit model import and
`Base.metadata.create_all/drop_all`, not migration 0008. They cover mapper ID and
UTC round trips; SQLite-naive restoration; save/rollback; owner isolation;
uniqueness; valid/invalid FK; `foreign_keys == 1`; `foreign_key_check == []`;
created_at; composite index; RESTRICT deletion rollback; and no merge/upsert.

Migration 0008, Alembic model-import registration, production schema deployment,
backfill, downgrade/re-upgrade remain Slice 6 only. `migrations/env.py` remains
unchanged. Slice 2 Engine-level SQLite enforcement is mandatory and unchanged;
new repositories must rely on it without a listener or PRAGMA.

Accepted risk — MINOR: SQLite strips timezone information from
`DateTime(timezone=True)` round trips. Mandatory mitigation is mapper use of the
existing UTC canonicalizer before domain restoration. Accepted information
boundary: Alembic explicitly imports models, and BookCompletion registration is
owned by Slice 6.

Slice 3 validation and closure evidence:

- exact integrated scope: the six frozen port/model/mapper/repository/test files;
  no existing Slice 3 file changed and no unexpected file was added;
- mapper tests: 5 passed; repository tests: 9 passed; architecture: 12 passed;
  full and DeprecationWarning-as-error suites: 459 passed; coverage: 98.16%;
  Alembic: 0007 (head);
- runtime SQLite `foreign_keys == 1` and `foreign_key_check == []`; existing
  `lifeos.db` remains Alembic 0007 with clean `foreign_key_check` and no
  `book_completions` deployment; migration 0008 remains absent.

Slice 3 is CLOSED / INTEGRATED / FINALIZED. Its frozen persistence contract above
is preserved as completed evidence. No Slice 4+ implementation was introduced.

### SLICE 4 — TRANSACTIONAL WRITE AND CONCURRENCY — IMPLEMENTED / PUBLISHED / MERGE BLOCKED

Slice 4 Implementation Authorization is APPROVED. The implementation, local final
review, atomicity evidence remediation, and final remediated commit review all
passed. The six-file authorized implementation is complete at commit
`151a519291a785f86856c685880f441b8b3bc510` and is published in PR #46, which
remains OPEN / DRAFT.

PR CI `33457790140` failed on the current integrated Python 3.10 platform: its
stdlib `sqlite3` does not expose the public numeric SQLite error-code API required
by the frozen `SQLITE_BUSY` classifier. This is a PLATFORM PREREQUISITE, not a
change to the frozen retry semantics. Slice 4 merge is blocked pending a separately
reviewed, implemented, and integrated Python >=3.11 platform transition.

Human Technical Decision: APPROVED — OPTION B. The future LifeOS platform is
Python >=3.11; the transition implementation is AUTHORIZED / NOT STARTED. The
current integrated platform and required
branch checks remain Python 3.10. Runtime activation remains separately forbidden
until Migration 0008 has been applied and fully backfilled under the coordinated
cutover below.

### COORDINATED MIGRATION 0008 + SLICE 4 RUNTIME CUTOVER — FROZEN

Semantic slice identities and BookCompletion semantics are preserved. Execution
and deployment order are amended: Migration 0008 + Backfill and Slice 4 remain
separate implementation/review scopes, but they are not independent deployment
units.

For every writable environment, the required sequence is:

1. create and verify a backup;
2. exclude ReadingSession write traffic and stop old writable application instances;
3. validate pre-migration database integrity;
4. apply Migration 0008, containing Completion schema, constraints, indexes, and
   complete historical backfill;
5. validate Alembic revision, schema, FK integrity, uniqueness, and historical
   backfill invariants;
6. start only the Slice 4-capable runtime and verify health;
7. re-enable ReadingSession write traffic.

No ReadingSession write may occur from the start of historical backfill until the
Slice 4-capable runtime is active. The following are invalid: migration/backfill
with an old writable ReadingSession runtime, and schema-only activation followed
by later historical backfill. Neither runtime schema fallback nor completion
timestamp rewriting is permitted.

Migration 0008 remains one cohesive schema + full-backfill migration. Its code is
integrated at repository Alembic head 0008; real-data application remains pending
the coordinated cutover. Do not split the backfill into 0009 and do not add
provenance state.

The retry policy frozen for the completed Slice 4 implementation remains: two total
write-intent acquisition attempts, fixed 50 ms delay, no jitter, and retry only
for `OperationalError` wrapping `sqlite3.OperationalError` with
`sqlite_errorcode == SQLITE_BUSY` before relevant reads, writes, tracking, flush,
or commit. Never retry after acquisition, `SQLITE_LOCKED`, IntegrityError, domain
or owner failure, flush, commit, ambiguous commit, publication, or unknown error.

`SqlAlchemyUnitOfWork.rollback()` not clearing `_tracked_aggregates` remains INFO:
no remediation is required while retry stays acquisition-only before tracking.

### MIGRATION 0008 + BACKFILL — INITIAL PREFLIGHT BLOCKERS RESOLVED / RESUME AUTHORIZED

The initial strictly read-only Migration 0008 + Backfill pre-flight completed
and was BLOCKED by two governance issues: documentation described a canonical
26-character TSID although pinned `tsidpy==1.1.5` produces and validates the
canonical 13-character representation; and schema 0007 permits historical
owner-consistent page intervals outside a Book's current total_pages.

Human data-integrity remediation is APPROVED. Canonical TSID representation is
defined behaviorally by the pinned dependency's round-trip, not by a length;
`VARCHAR(26)` remains unchanged persistence capacity. No domain, value object,
model, existing ID, or dependency change is authorized or required.

For each owner-consistent source row, backfill must validate page bounds against
the current Book and a readable, deterministically orderable ended_at. Any
unrepresentable source history aborts 0008 before DDL; no clamp, truncation,
silent exclusion, rewrite, deletion, repair, or synthetic historical total_pages
is permitted. Owner-mismatched sessions remain excluded from coverage and do not
independently block migration. FK integrity violations remain independent
blockers.

SQLite partial-DDL risk is accepted only under the already frozen backup,
traffic-exclusion, failed-start, post-migration verification, and coordinated
cutover controls. All source validation, full candidate computation,
migration-local TSID generation/validation, and explicit technical created_at
selection must complete before the first 0008 DDL.

At the blocked pre-flight stage, the conditional three-file candidate was not
yet authorized and only the Migration 0008 + Backfill pre-flight resume was
executable. That historical state was subsequently superseded by the approved
Implementation Authorization Review, implementation, final review, and PR #44
integration.

### MIGRATION 0008 CODE INTEGRATION FINALIZED

- PR #44 merged authorized head `dd4a1b1069b342febf0bdec4d271ffb1e833ecf1`
  through Rebase and Merge into canonical main
  `93c385670be8490662cb7f96e05016be7a60aed5`.
- Main CI `33028326214`: 3/3 SUCCESS. Local finalization: PASS; 465 tests and
  98.16% coverage. Repository Alembic head is 0008.
- Real `lifeos.db` intentionally remains revision 0007 without
  `book_completions`; no real-data migration or coordinated cutover has run.
- Migration 0008 code integration is finalized. At that integration checkpoint,
  Slice 4 implementation had not started and its Implementation Authorization
  Review was next. That historical state was superseded by the approved Slice 4
  implementation, final review, publication in draft PR #46, and discovery of the
  Python 3.11 platform prerequisite.

### Deferred slices

3. Completion Persistence — INTEGRATED / FINALIZED.
4. Transactional Write + Concurrency — IMPLEMENTED / DRAFT PR #46 / MERGE BLOCKED PENDING PYTHON 3.11 PLATFORM TRANSITION / RUNTIME ACTIVATION BLOCKED PENDING COORDINATED CUTOVER.
5. Dedicated Read Model / API.
6. Migration 0008 + Backfill — CODE INTEGRATED / REAL-DATA APPLICATION NOT EXECUTED / COORDINATED CUTOVER NOT EXECUTED.
7. Best-Effort Event Seam.
8. Full Regression + Governance.

## Pendências

- READ-005: SLICE 1 INTEGRATED / PRE-SLICE-2 REMEDIATION FINALIZED / SLICE 2 FINALIZED / SLICE 3 FINALIZED / SLICE 4 IMPLEMENTED AND PUBLISHED IN DRAFT PR #46 / SLICE 6 CODE INTEGRATED.
- RF-READ-005: Slice 4 merge is blocked pending the Python 3.11 platform transition; runtime activation remains blocked pending coordinated cutover.
- US-READ-005-001: only the Python 3.11 Platform Transition Implementation is executable.
- Python platform: current integrated platform and required checks remain 3.10; future >=3.11 transition is human-approved and AUTHORIZED / NOT STARTED.
- Migration 0008: CODE INTEGRATED; real local database NOT APPLIED.
- Alembic: repository 0008 (head); real `lifeos.db` 0007.
- READ-008: DEFERRED.
- RF-READ-009: ASSOCIAÇÃO PENDENTE / DEFERRED.
- RF-READ-010: RECONCILIAÇÃO PENDENTE / DEFERRED.
- `/api/v1`: PENDING NON-BLOCKING.
- Pesquisa: OUTSIDE READ-005 / NO FEATURE AUTHORIZED.

## Architecture Boundary

This amendment preserves ADR-0042 and BookCompletion semantics while clarifying
the pinned TSID representation and source-history safety conditions. At this
amendment's historical stage, authorization was limited to the read-only
Migration 0008 + Backfill implementation pre-flight resume. That state was
superseded by Migration 0008 code integration and the completed, reviewed Slice 4
implementation now published in draft PR #46. The current executable authority is
the Python 3.11 Platform Transition Implementation. Slice 4
merge remains blocked pending that platform transition; runtime activation remains
blocked pending coordinated cutover; Slices 5, 7, and 8 remain gated.

Architecture Decision ADR-0042 está aceita e congelada. The amended Technical
Plan is approved and frozen at docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md.

## Próximo Gate

PYTHON 3.11 PLATFORM TRANSITION IMPLEMENTATION

ONLY THE PYTHON 3.11 PLATFORM TRANSITION IMPLEMENTATION IS AUTHORIZED.

DO NOT MODIFY PR #46, APPLY MIGRATION 0008 TO REAL DATA, EXECUTE THE COORDINATED CUTOVER, OR EXPAND THE PYTHON 3.11 PLATFORM IMPLEMENTATION BEYOND THE FROZEN SIX-FILE ALLOWLIST.

SPRINT 09 AUTHORIZATION IS PROGRAM-LEVEL AUTHORIZATION, NOT BLANKET PERMISSION.

## A10 and A11 historical checkpoints; current A12 reconciliation

A10 became canonical in PR #123 at `80e40c8fd3531e68135926c1e60afd3f73377b3d`
on `2026-09-29T22:46:05Z`. Its R2 technical design remains the current,
approved and frozen authority. Its statement that B2 had not been implemented
became stale when canonical Logos PR #50 merged earlier, at
`2026-09-29T22:25:40Z`. PR #50 preceded A10; at that merge, A9 was canonical
and implementation was explicitly NOT AUTHORIZED. The classification is a
GOVERNANCE SEQUENCING DEVIATION: B2 implementation advanced before its explicit
authorization gate. No retroactive authorization is claimed.

A11 is a HISTORICAL CANONICAL RECONCILIATION CHECKPOINT. Its external facts
about PR #50, its canonical SHA, CI, test count, default-off posture, and lack
of repository bootstrap or activation remain preserved. A11's current-state
conclusions that B2 was complete, A10/R2 was superseded, and C1 was next are
SUPERSEDED BY A12. A11 remains in canonical history and is not rewritten.

### Current A12 reconciliation

`LIFEOS-LOGOS-HARDENING-TP-001-A12` is the current reconciliation. PR #50 is a
canonical external implementation fact and reflects the historical A9 design.
No authorization bypass was found; automatic rollback is not required. The
current state is:

```text
A9 = HISTORICAL / CANONICAL B2 DECISION CHECKPOINT
A10 = CANONICAL / CURRENT R2 TECHNICAL AUTHORITY
A11 = HISTORICAL CANONICAL RECONCILIATION / CURRENT CONCLUSIONS SUPERSEDED BY A12
A12 = CURRENT B2 SEQUENCING-DEVIATION / R2 FORWARD-ALIGNMENT RECONCILIATION
PR #50 implementation authorization at merge = NOT PRESENT
sequencing deviation = YES
B2 = CANONICAL A9 IMPLEMENTATION PRESENT / DEFAULT-OFF / R2 FORWARD ALIGNMENT OPEN
R2 authority = LOGOS-HARD-002-B2-TP-001-R2 / APPROVED / FROZEN
recovery preflight = LOGOS-HARD-002-B2-R2-RECOVERY-IA-001 / COMPLETE / READ-ONLY
recovery recommendation = READY_FOR_FORWARD_R2_CORRECTION
recovery path universe = 19 semantic paths maximum
C1 = NOT AUTHORIZED
current path = B2-R2 FORWARD ALIGNMENT → C1 → C2
next gate = LOGOS-HARD-002-B2-R2-RECOVERY-IMPL-001
```

Canonical Logos PR #50 (`LOGOS-HARD-002-B2 — Enforce workload authorization
grants`) merged at `096fc1a5124358997771d1bb0b0db291a2d81935`, parent
`bc13dce086c865d1db4a4811b764fdc2bdd155d7`, tree
`07c5f93b60a520bc768ee58e1c9d2a10ae8afd80`. It changed 11 paths (7 production
and 4 tests). Pre-merge CI `36637456809` and post-merge CI `36639505288` passed;
post-merge coverage included 404 tests, with zero failures, errors, or skips.

### Current canonical Logos implementation facts

The implementation is the historical A9 shape. Enforcement is manual inside
`ProgressionExecutionController.create(...)`; the controller target begins
before a DENY, though the business use case is not called on denial. The core
result is `AuthorizationEvaluator.AuthorizationDecision`. Missing, null, or
invalid authorization dimensions return 400. `AuthorizationRegistryCorruptedException`
is present, and `AuthorizationRegistryUnavailableException` remains in its old
application package. The method-security advisor, `AuthorizeProgressionExecute`,
`ProgressionExecuteAuthorizationManager`, `WorkloadAuthorizationMethodSecurityConfig`,
and `AuthorizationVerdict` are absent. The workload request rule is
`authenticated()` and the workload profile is default-off. These are current
code facts, not the R2 target architecture.

Security review found no authorization bypass. No real grant seed, production
activation configuration, or migration beyond V46 is present in the repository.
Automatic rollback is NO; forward correction is suitable. No external database
state is inferred.

### Current R2 target and open alignment

A10/R2 remains the technical authority: E3-B custom method security after MVC
body binding and before controller target execution. The Spring-independent
`AuthorizationEvaluator` returns `AuthorizationVerdict` (`ALLOW` / `DENY`).
`AuthorizeProgressionExecute` marks only `create(...)`;
`ProgressionExecuteAuthorizationManager` bridges the bound request to the
core evaluator, and `WorkloadAuthorizationMethodSecurityConfig` owns the
method-security wiring. The public pointcut is
`AnnotationMatchingPointcut.forMethodAnnotation(AuthorizeProgressionExecute.class)`;
`AuthorizationMethodPointcuts`, `@PreAuthorize`, SpEL, and `@P` are not used.
The evaluator input is `AuthenticatedPrincipal`, operation, and optional source
and namespace; it defensively requires WORKLOAD / VERIFIED and allows only an
exact grant. Stable identity is `principalType + principalId`; no credential
identity, `kid`, wildcard, prefix, cache, role-derived authority, or trust-derived
grant is used. The manager requires authenticated `WorkloadPrincipalAuthenticationToken`
with an `AuthenticatedPrincipal`, reads the bound request arguments, and maps
`AuthorizationVerdict.ALLOW` to Spring allow and DENY to Spring deny. It catches
only expected `IllegalArgumentException` while constructing authorization
dimensions; the bounded registry-unavailable exception propagates for 503.

The infrastructure advisor is `progressionExecuteAuthorizationAdvisor`, with
`ROLE_INFRASTRUCTURE`, conditional on
`logos.security.workload.http.enabled=true` and `matchIfMissing=false`. When
the property is absent or false, the workload chain and advisor are absent,
the marker is inert, and the human chain is unchanged. When enabled, only the
exact workload POST matcher applies and request authorization is
`authenticated()`.

Open forward behavioral alignment: malformed JSON remains 400; a
 deserializable request with missing authorization dimensions or invalid source
or namespace grammar must return 403; valid authorization dimensions followed
by ALLOW and invalid business fields may return 400. Malformed/unparseable JSON
remains 400. Only POST `/api/internal/v1/progression/executions` is in the
workload chain; GET execution, GET history, and subject provisioning stay on the
human chain. Open architectural
alignment: DENY must occur before the controller target body, with the business
use case not invoked. Open registry alignment: move the bounded
`AuthorizationRegistryUnavailableException` to
`core/security/authorization/application/exception`, translate only
`DataAccessException` in `findExact`, and do not include a corruption-specific
B2 exception in the current target. No-row remains ordinary DENY.

PR #50's 404 green tests validate the historical implementation but do not
prove the R2 advisor enabled/default-off states, manager token/principal
validation, null dimensions and invalid grammar returning 403, controller
target non-invocation on DENY, valid-auth registry outage returning 503 with
replay consumed and retry 401, or mocked `JdbcTemplate` DataAccessException
translation. These remain open R2 evidence.

### Frozen forward recovery universe

The maximum semantic universe is 19 paths: the 15 current R2 target paths
below plus four A9 cleanup paths. No twentieth path is authorized without new
human review.

R2 target (15):
1. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluator.java`
2. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationVerdict.java`
3. `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/exception/AuthorizationRegistryUnavailableException.java`
4. `src/main/java/com/josecjuniors/logossrv/config/security/authorization/AuthorizeProgressionExecute.java`
5. `src/main/java/com/josecjuniors/logossrv/config/security/authorization/ProgressionExecuteAuthorizationManager.java`
6. `src/main/java/com/josecjuniors/logossrv/config/security/authorization/WorkloadAuthorizationMethodSecurityConfig.java`
7. `src/main/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionController.java`
8. `src/main/java/com/josecjuniors/logossrv/config/SecurityConfig.java`
9. `src/main/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStore.java`
10. `src/main/java/com/josecjuniors/logossrv/adapters/in/web/exception/GlobalExceptionHandler.java`
11. `src/test/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationEvaluatorTest.java`
12. `src/test/java/com/josecjuniors/logossrv/config/security/authorization/ProgressionExecuteAuthorizationManagerTest.java`
13. `src/test/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStoreTest.java`
14. `src/test/java/com/josecjuniors/logossrv/config/security/workload/WorkloadSpringSecurityIntegrationPostgresTest.java`
15. `src/test/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionSecurityPostgresTest.java`

A9 cleanup (4):
16. Delete `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationRegistryCorruptedException.java`.
17. Remove old path `src/main/java/com/josecjuniors/logossrv/core/security/authorization/application/AuthorizationRegistryUnavailableException.java` (relocated to target path #3).
18. Remove only PR #50 B2-specific changes from `src/test/java/com/josecjuniors/logossrv/adapters/in/web/progression/api/ProgressionExecutionControllerTest.java`.
19. Remove only PR #50 B2-specific changes from `src/test/java/com/josecjuniors/logossrv/adapters/out/security/authorization/JdbcAuthorizationGrantStorePostgresTest.java`.

Flyway remains V46; no migration is part of this recovery, V47 is not
reserved, and `pom.xml` remains unchanged. No real grant is inserted; T1/T2/T3
are not executed; operational workload activation is not active by repository
configuration. The next gate is
`LOGOS-HARD-002-B2-R2-RECOVERY-IMPL-001` — BOUNDED FORWARD-CORRECTION
IMPLEMENTATION AUTHORIZATION / EXCLUSIVE-WRITER PREFLIGHT. This gate is not
executed here. C1 remains NOT AUTHORIZED.
