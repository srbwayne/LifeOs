# TASK-011 — LifeOS ↔ Logos Progression Contract Discovery

Status: `COMPLETE`
Implementation: `NOT STARTED`
Human decision required: `YES`

## 1. Baseline

- LifeOS branch: `docs/read-005-slice5-integration-reconciliation`
- HEAD: `d2d8dd4141b3ef0dd105e7064eebee6042004ae8`
- HEAD subject: `docs(read): reconcile slice 5 integration`
- Working tree: clean before this document
- Tests: `.venv-platform311\Scripts\python.exe -m pytest -q` — **502 passed**
- Logos checkpoint consulted: `89f6f6b4a433261b0c6a85941c91c1f4ae5aa2b2`

No production code, migration, database, dependency, or Logos file was changed.

## 2. Candidate inventory

The implemented LifeOS capabilities are `auth`, `character`, and `read`. No
implemented `workout`, `habit`, or study aggregate was found.

| Candidate | Source aggregate/event | Numeric facts available | Stable ID | Tenant/user link | Complexity | Recommendation |
|---|---|---|---|---|---|---|
| Reading session | `ReadingSession` / persisted reading session | `pages_read`, start/end pages, timestamps | `ReadingSessionId` (TSID) | `owner_id -> users.id` | Low | **Pilot** |
| Book completion | `BookCompletion` / persisted completion milestone | Binary completion, `completed_at` | `BookCompletionId` (TSID) | Derived through `book_id -> books.user_id` | Low, but no useful measure | Not first pilot |
| Character creation | `Character` / `CharacterCreated` | None suitable for progression valuation | `CharacterId`, `PlayerId` | `Player.user_id` | Low, no numeric fact | No |
| User registration | `User` / `UserRegistered` | None suitable for progression valuation | `UserId` (TSID) | User itself | Low, no activity fact | No |

Evidence: `app/read/domain/aggregates/reading_session.py`,
`app/read/infrastructure/persistence/models/reading_session_model.py`,
`app/read/application/commands/create_reading_session.py`,
`app/read/domain/aggregates/book_completion.py`,
`app/character/domain/events/character_created.py`, and
`app/auth/domain/events/user_registered.py`.

## 3. Selected pilot

**Candidate:** a recorded `ReadingSession`.

It is the smallest existing fact that combines a durable source record, a
stable source ID, and an unambiguous numeric value (`pages_read`). It does not
require Noema, hardware, a new aggregate, or a new LifeOS table. `BookCompletion`
is deliberately not selected: it is a useful milestone but supplies only a
boolean fact and is currently a derived/dedicated record rather than a numeric
activity measure.

### Source ownership

LifeOS owns the reading session and its pages/timestamps. Logos owns only the
progression valuation and resulting canonical progression state.

## 4. Source event identity

`ReadingSessionId` is a canonical TSID persisted as `reading_sessions.id`.
It is stable, non-empty, and generated at aggregate creation. It is suitable as
the future idempotency candidate for the integration.

There is currently no `ReadingSessionCreated` or equivalent domain event. The
current `CreateReadingSessionCommandHandler` persists the session and commits
it through `SqlAlchemyUnitOfWork`; the in-process event seam is not used for
reading sessions. Therefore the proposed source event is:

```text
reading_session_recorded
source event ID = ReadingSessionId
```

This is a contract proposal, not an implemented event. The next implementation
slice must decide whether to derive an integration intent after commit or add a
proper event seam within the approved READ workflow.

## 5. Subject identity

```text
namespace = lifeos
externalId = ReadingSession.owner_id / UserId
```

The source field is `reading_sessions.user_id`, which references `users.id`.
`UserId` is a canonical TSID string of length 26 (`app/shared/domain/identifiers/user_id.py`).
It is the stable technical user identity; email, username, token, session ID,
and display names are excluded.

The current database has user ownership but no `tenant_id` column in `users`,
`players`, `books`, or `reading_sessions`. The present schema therefore makes
`UserId` globally unique and safe for this pilot. The documented future
multi-tenant model still requires an explicit tenant/namespace decision before
multi-tenant deployment; do not silently change the external ID to
`tenantId:userId` in this task.

## 6. Configuration identity

Recommended key: `reading`.

This is a domain capability key rather than a LifeOS-specific or UUID-derived
key. It can remain reusable if another source later emits a reading fact.
The normal pilot request omits `revision`, so Logos resolves the current
configuration version. An explicit revision is reserved for controlled tests
and reproduction.

The Logos V2 boundary is:

```http
POST /api/internal/v2/progression/external/lifeos/{externalId}/evaluate
```

## 7. Fact mapping

| LifeOS field | Meaning | Logos `factorKey` | Transformation | Unit |
|---|---|---|---|---|
| `ReadingSession.pages_read` | Pages covered by the session, inclusive | `pages_read` | `int` converted to JSON number | pages |

The source calculation is `ReadingSession.pages_read`, implemented as
`end_page - start_page + 1`. No duration conversion is proposed because
timestamps are not currently the domain measure selected for this pilot.

LifeOS sends facts only. XP base, stress, distributions, cutoffs,
multipliers, and skill policy remain Logos-owned configuration.

## 8. Proposed request

For a session with 30 pages read:

```http
POST /api/internal/v2/progression/external/lifeos/0ujsszwN8NRYQQvj2bAP/evaluate
```

```json
{
  "configuration": {
    "key": "reading"
  },
  "details": [
    {
      "factorKey": "pages_read",
      "value": 30
    }
  ]
}
```

`revision` is omitted for normal operation. The caller does not provide
progression state or rules.

## 9. Response and canonical ownership

Logos returns the existing `result` and `profile` response shape. LifeOS may
use the immediate result for UX or operational observation, but must not store
`globalXp`, `level`, `stress`, attributes, or skills as an authoritative local
copy.

```text
LifeOS canonical fact: ReadingSession
Logos canonical progression state: ProgressionProfile/state in Logos
```

Any future LifeOS cache is derived and non-authoritative.

## 10. Delivery model alternatives

| Criterion | Sync Direct | Application Event | Durable Outbox |
|---|---:|---:|---:|
| Simplicity | High | Medium | Low |
| Preserves fact if Logos fails | Yes, if called after commit | Yes | Yes |
| Retry | Caller-managed | Not guaranteed by current in-memory bus | Durable |
| Idempotency needed | Yes | Yes | Yes |
| LifeOS impact | Small | Medium | Larger |
| Operational complexity | Low | Medium | High |
| Pilot suitability | High for manual proof | Medium | Low for first proof, high for production reliability |
| Future suitability | Limited | Limited while bus is in-memory | High |

### Recommendation

**Recommended pilot delivery:** synchronous call after the LifeOS transaction
has committed, behind an integration application boundary, with failure
reported separately from the already-persisted reading fact.

This is appropriate only for a bounded/manual pilot because it does not provide
durable retry. The production integration should evolve to a durable outbox or
equivalent delivery mechanism before relying on at-least-once cross-service
delivery. The existing `InMemoryEventBus` is explicitly best-effort and does
not provide the required guarantee.

## 11. Failure, duplicates, ordering, and concurrency

- Logos failure invalidates the LifeOS fact: **NO**. A completed reading session
  remains true in LifeOS even if valuation is unavailable.
- Duplicate risk: **REAL**. `ReadingSessionId` is the future `idempotencyKey`
  candidate; Logos does not yet provide integration idempotency.
- Ordering materially affects the result: **YES/PARTIALLY**. Logos updates a
  stateful profile, so out-of-order sessions can change the resulting state even
  when each individual pages value is independent.
- Concurrent same-subject events: **YES**. Multiple sessions can be recorded
  and delivered close together; serialization/optimistic concurrency remains a
  future integration concern.

## 12. Provisioning

For the first pilot:

- subject mapping: manual/bootstrap `lifeos:<UserId>` mapping in Logos;
- configuration: manual/bootstrap `reading` configuration in Logos.

Automatic mapping, email linking, onboarding APIs, and configuration authoring
are out of scope and remain prohibited for this slice.

## 13. Authentication and authorization

The Logos V2 endpoint currently inherits the existing authenticated boundary.
It is not a service-to-service contract yet.

Future runtime integration requires separate decisions for:

1. service-to-service authentication, without reusing a human login;
2. authorization for the LifeOS client to act on `namespace = lifeos`.

Authentication does not imply authorization, and the external subject is not
implicitly derived from the caller principal.

## 14. Conceptual end-to-end flow

```text
User records a reading session
↓
LifeOS persists ReadingSession and commits
↓
integration boundary derives reading_session_recorded intent
↓
map owner UserId → lifeos external subject
↓
map pages_read → ProgressionFact(pages_read)
↓
POST Logos V2 external progression
↓
Logos resolves current configuration key `reading`
↓
Logos resolves current global SkillPolicyVersion
↓
Logos evaluates and persists canonical progression state
↓
LifeOS observes the result; it does not duplicate canonical state
```

If Logos is unavailable, the persisted LifeOS fact remains valid. A future
durable delivery mechanism should retry the integration without rewriting the
source fact.

## 15. Contract freeze candidate — PROPOSED

```text
Source system: LifeOS
Source event: reading_session_recorded
Source event ID: ReadingSessionId (reading_sessions.id)
External subject namespace: lifeos
External subject ID: ReadingSession.owner_id / users.id (UserId TSID)
Configuration key: reading
Configuration revision mode: omitted for normal pilot; current version
Facts: pages_read -> factorKey pages_read, integer pages
Delivery model: synchronous after commit for bounded pilot
Failure semantics: Logos failure does not invalidate LifeOS fact
Canonical fact owner: LifeOS
Canonical progression owner: Logos
```

## 16. Logos and LifeOS changes

```text
Logos production changes required: NO
LifeOS production changes made: NO
Database changes made: NO
HTTP client added: NO
Retry/outbox/idempotency implemented: NO
Noema integration: NO
```

## 17. Recommended next implementation slice

After human approval, implement only:

1. a LifeOS integration adapter/application boundary;
2. a contract mapper for `ReadingSessionId`, `UserId`, `pages_read`, and
   configuration key `reading`;
3. a manually configured subject mapping and Logos configuration fixture;
4. contract/integration tests against the existing Logos V2 endpoint;
5. explicit logging/observation of delivery failure without changing the source
   fact.

Do not include outbox, retry, service accounts, namespace authorization,
automatic provisioning, or Noema in that first implementation slice unless a
separate decision authorizes them.

## 18. Remaining human decisions

1. Approve `ReadingSession` as the first pilot source fact.
2. Approve `reading_session_recorded` as the future integration event name and
   `ReadingSessionId` as its idempotency candidate.
3. Approve `lifeos` + `UserId` as the pilot subject identity, subject to a
   future explicit tenant identity decision.
4. Approve configuration key `reading`.
5. Approve synchronous-after-commit delivery for the bounded pilot, with the
   known non-durable failure semantics.
6. Define service-to-service authentication and namespace authorization before
   runtime deployment.

## 19. Git

This discovery adds documentation only. The document is intended to be
committed on the current LifeOS branch after review. No Logos working-tree
files are part of this task.

```text
TASK-011 DISCOVERY: COMPLETE
FIRST LIFEOS → LOGOS PILOT: IDENTIFIED
EXTERNAL SUBJECT CONTRACT: PROPOSED
EXTERNAL CONFIGURATION CONTRACT: PROPOSED
FACT MAPPING: PROPOSED
DELIVERY MODEL: PROPOSED
LOGOS PRODUCTION CHANGES: NONE
LIFEOS PRODUCTION CHANGES: NONE
HUMAN DECISION REQUIRED: YES
```
