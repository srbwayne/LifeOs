# THERAPY-002 V1 Technical Plan

Status: **ARCHITECTURE REVIEW APPROVED — DOCUMENTATION ONLY**

Date: 2026-09-08

This plan translates the frozen THERAPY-001 business/privacy contract into a
minimum implementation architecture. It authorizes no production change,
migration, test change, runtime action, progression, external exposure, Logos
integration or Noema integration.

## 1. Authority and frozen business decisions

The authoritative business contract is:

`docs/10_AI_ENGINEERING/THERAPY_001_BUSINESS_PRIVACY_CONTRACT.md`

This plan does not reopen it. Decisions below are labeled as technical
proposals, open questions or deferred work.

Frozen Therapy V1 facts:

- `TherapySession` is an owner-reported historical occurrence that already
  happened;
- `TherapySession` is the aggregate root;
- `Therapist` is a separate reusable owner-scoped reference;
- both are owned by the authenticated LifeOS User;
- cross-owner references are forbidden;
- there is no draft, appointment, scheduling or cancellation state;
- the only functional time field is UTC `occurred_at`;
- Therapist V1 requires `name`; `active` is allowed metadata;
- `specialty_or_focus` is not V1;
- there is exactly one optional private owner-authored reflection/note;
- themes, structured reflections, follow-up actions, clarity, duration,
  `started_at` and `ended_at` are not V1;
- `PROGRESSION_ELIGIBLE = NO` and
  `EXTERNAL_EXPOSURE_ALLOWED = NO` for Therapy V1;
- AI/Noema access is NO;
- no event delivery, progression intent, Logos occurrence or downstream call
  exists in this plan.

## 2. Repository evidence

The canonical `main` baseline is `b0bddb8609e85b39e9cebfc58c415770e6950bb8`.
The repository Alembic head is revision `0009`, with `0009` depending on
`0008`.

Patterns inspected include:

- `app/read/domain`, `application`, `infrastructure` and `presentation`;
- `app/auth`, `app/shared`, `app/app_factory.py` and `app/composition_root.py`;
- `migrations/env.py` and revisions `0001` through `0009`;
- repository ports and SQLAlchemy repositories;
- `SqlAlchemyUnitOfWork`, `get_db`, FastAPI dependencies and routers;
- TSID value objects and `UserId`;
- Reading repository/API pagination and owner-safe lookup behavior;
- domain, application, integration and E2E test patterns.

No `app/therapy` implementation exists. The planning documents describe
Therapy entities and older fields, but those fields are not copied into V1
without the THERAPY-001 decision.

## 3. Proposed package structure

Align the new capability with the existing capability layering:

```text
app/therapy/
├── __init__.py
├── dependencies.py
├── domain/
│   ├── __init__.py
│   ├── aggregates/
│   │   ├── therapist.py
│   │   └── therapy_session.py
│   ├── errors/therapy_errors.py
│   ├── ports/
│   │   ├── therapist_repository.py
│   │   └── therapy_session_repository.py
│   └── value_objects/
│       ├── therapist_id.py
│       └── therapy_session_id.py
├── application/
│   ├── commands/
│   │   ├── create_therapist.py
│   │   ├── activate_therapist.py
│   │   ├── deactivate_therapist.py
│   │   ├── create_therapy_session.py
│   │   ├── update_private_note.py
│   │   └── delete_therapy_session.py
│   ├── dtos/
│   │   ├── therapist_dto.py
│   │   └── therapy_session_dto.py
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── therapist_read_repository.py
│   │   └── therapy_session_read_repository.py
│   └── queries/
│       ├── get_therapist.py
│       ├── list_therapists.py
│       ├── get_therapy_session.py
│       └── list_therapy_sessions.py
├── infrastructure/
│   └── persistence/
│       ├── mappers/
│       │   ├── therapist_mapper.py
│       │   └── therapy_session_mapper.py
│       ├── models/
│       │   ├── therapist_model.py
│       │   └── therapy_session_model.py
│       └── repositories/
│           ├── therapist_repository.py
│           ├── therapist_read_repository.py
│           ├── therapy_session_repository.py
│           └── therapy_session_read_repository.py
└── presentation/
    └── api/fastapi/
        ├── routers.py
        └── schemas.py
```

No Therapy event module, progression adapter, Noema adapter or generic
repository abstraction is proposed.

## 4. Domain model: Therapist

### Frozen architecture decision

`Therapist` is an Aggregate Root with independent identity, lifecycle,
repository and application use cases. It is a reusable owner-scoped reference
and is not embedded in the TherapySession aggregate or treated as a cross-user
directory.

```text
Therapist
- id: TherapistId
- owner_id: UserId
- name: normalized non-empty string
- active: bool
```

Rules:

- `name` is trimmed and must not be blank;
- maximum length is 150 characters, matching the established Therapy planning
  schema convention and preventing unbounded reference values;
- `active` defaults to `true`;
- duplicate names are allowed for one owner because a display name is not a
  trustworthy identity and the business contract did not forbid duplicates;
- no `specialty_or_focus`, credentials, license, phone, email or clinical
  profile is present in V1;
Therapist is not deleted by the V1 API. Deactivation is the V1 lifecycle
operation for making the reference unavailable to new sessions. TherapySession
is also a separate Aggregate Root and references Therapist only by
`TherapistId`; no cross-aggregate object navigation is required.

## 5. Domain model: TherapySession

```text
TherapySession
- id: TherapySessionId
- owner_id: UserId
- therapist_id: TherapistId
- occurred_at: timezone-aware UTC datetime
- private_note: optional normalized private owner-authored text
```

`private_note` is the implementation-neutral name for the one optional field.
Its business meaning is personal reflection/private note written by the owner.
It must not be described or surfaced as a clinical note, therapist note,
medical note, diagnosis or treatment record.

Invariants:

- owner, therapist and occurrence time are required;
- `occurred_at` must be timezone-aware and normalized to UTC;
- a future `occurred_at` is rejected by the domain/application boundary using
  an injected current UTC instant; this preserves the historical-occurrence
  meaning;
- `private_note` must be a string or null, is trimmed, and blank input becomes
  null;
- `PRIVATE_NOTE_MAX_LENGTH = 10_000` is validated at both the
  presentation/request boundary and domain construction/mutation boundary;
  this is an operational payload bound, not a progression or clinical rule;
- structural occurrence fields are immutable after creation;
- no status field is added;
- no domain event is emitted by Therapy V1.

The aggregate factory creates a new `TherapySessionId`; restoration validates
the value-object types and preserves persisted values.

## 6. Identifier decision

`TherapistId` and `TherapySessionId` are frozen as TSID-style opaque IDs,
consistent with `UserId`, `ReadingSessionId` and the repository's current
`new_tsid()` convention.

For each ID:

- value-object location: `app/therapy/domain/value_objects/`;
- generation: the aggregate factory calls the `new()` class method;
- parsing: `from_value()` validates canonical TSID representation;
- serialization: `to_persistence()` returns the 26-character string;
- persistence: `String(26)` primary/foreign-key columns;
- API: IDs are serialized as opaque strings;
- no UUID and no external-system identifier is introduced.

## 7. Ownership enforcement

Ownership is enforced at every layer:

1. The authenticated `UserId` is derived from the bearer token.
2. The API never accepts `user_id` as writable request data.
3. `get_by_id_and_owner(id, owner_id)` is the only single-resource lookup
   contract exposed to application code.
4. Creating a session first loads the Therapist through the authenticated
   owner's scope.
5. The application verifies the therapist owner matches the command owner.
6. The database composite relationship also enforces the pair.

Foreign-owner IDs are intentionally indistinguishable from missing IDs:
repositories return `None`, application handlers raise the existing-style
not-found error, and the API returns `404` without revealing existence.

## 8. Repository ports

Minimum ports:

```python
class ITherapistRepository(Protocol):
    def save(self, therapist: Therapist) -> None: ...
    def get_by_id_and_owner(
        self, therapist_id: TherapistId, owner_id: UserId
    ) -> Therapist | None: ...

class ITherapySessionRepository(Protocol):
    def save(self, session: TherapySession) -> None: ...
    def get_by_id_and_owner(
        self, session_id: TherapySessionId, owner_id: UserId
    ) -> TherapySession | None: ...
    def delete(self, session: TherapySession) -> None: ...
```

Read ports are separate projection contracts under
`app/therapy/application/ports/` and do not mutate aggregates:

```python
class ITherapistReadRepository(Protocol):
    def list_by_owner(self, owner_id: UserId) -> tuple[TherapistDTO, ...]: ...

class ITherapySessionReadRepository(Protocol):
    def get_by_id_and_owner(
        self, session_id: TherapySessionId, owner_id: UserId
    ) -> TherapySessionDetailDTO | None: ...
    def count_by_owner(self, owner_id: UserId) -> int: ...
    def list_page_by_owner(
        self, owner_id: UserId, offset: int, limit: int
    ) -> tuple[TherapySessionHistoryItemDTO, ...]: ...
```

History uses the established `page`/`size` application query shape, with
`page >= 1`, `1 <= size <= 100`, and stable order `occurred_at DESC, id DESC`.
The history projection excludes `private_note`. Deleted sessions are absent
from all read projections because V1 chooses hard delete.

## 9. Application use cases

### Therapist

- `CreateTherapist`;
- `ListTherapists`;
- `GetTherapist`;
- `DeactivateTherapist`;
- `ActivateTherapist`.

Activation changes only the owner-scoped reference's `active` flag. No session
history is modified.

### TherapySession

- `CreateTherapySession`;
- `GetTherapySession`;
- `ListTherapySessions`;
- `UpdatePrivateNote`;
- `DeleteTherapySession`.

No structural edit command is included. Note update accepts a new optional note
or null, and remains owner-scoped. Delete is an explicit owner-authorized hard
delete; no bulk cleanup or cascade is provided.

## 10. Correction and edit policy

### Frozen architecture decision

- structural fields (`owner_id`, `therapist_id`, `occurred_at`) are immutable
  after creation;
- the private note may be provided during creation and, after creation, may be
  replaced or cleared through `UpdatePrivateNote`;
- no event sourcing, revision history or distributed compensation is added;
- duplicate correction is a separate owner-authorized delete/create decision,
  not an implicit merge;
- if future externalization is ever approved, correction requires a new
  explicit contract and is not implemented here.

This preserves the historical occurrence while allowing the owner to correct
private text. No event sourcing, revision table or audit-history table is part
of V1. `PRIVATE NOTE AUDIT TRAIL: NO — THERAPY V1`; future audit/version
semantics are deferred.

## 11. Delete and retention decision

### Frozen architecture decision: owner-authorized hard delete

V1 hard-deletes a single owner-scoped TherapySession and its private note. No
`deleted_at`, archive state or lifecycle state machine is added.

Consequences:

- deleted sessions disappear from owner history and all repository/API reads;
- the private note is removed with the row;
- there is no product audit trail for the deleted occurrence;
- a future identical session can be recorded again, so the API must not claim
  duplicate prevention beyond the owner's explicit action;
- Therapist references are not deleted as a side effect;
- future AI, progression or external consumers have no V1 deletion event to
  reconcile because none are integrated;
- hard delete removes the canonical database row;
- V1 does not promise erasure from historical backups because backup-purge
  semantics are not established;
- hard delete remains a product choice, not a legal-retention claim.

Therapist deletion is not a V1 API operation. If introduced later, referenced
Therapists must be `RESTRICT`ed rather than cascading into historical sessions.
Long-term privacy/retention review is deferred. No legal retention claim is
made.

## 12. Therapist deactivation

New Therapist records use `active = true`. `active = false` means
unavailable for new TherapySession selection by that owner. It does not delete,
hide or invalidate historical TherapySession references.

Creating a new session with an inactive Therapist is rejected with a domain
conflict. Reading historical sessions continues to return the inactive
Therapist reference. Reactivation is owner-scoped and restores selection for
future sessions.

## 13. Persistence schema

Migration `0010` should contain only these two tables:

```text
therapists
- id VARCHAR(26) NOT NULL PRIMARY KEY
- user_id VARCHAR(26) NOT NULL
- name VARCHAR(150) NOT NULL
- active BOOLEAN NOT NULL DEFAULT TRUE
- created_at DATETIME NOT NULL
- updated_at DATETIME NOT NULL

therapy_sessions
- id VARCHAR(26) NOT NULL PRIMARY KEY
- user_id VARCHAR(26) NOT NULL
- therapist_id VARCHAR(26) NOT NULL
- occurred_at DATETIME NOT NULL
- private_note TEXT NULL
- created_at DATETIME NOT NULL
- updated_at DATETIME NOT NULL
```

Constraints and indexes:

- `therapists.user_id -> users.id ON DELETE RESTRICT`;
- `UNIQUE(therapists.user_id, therapists.id)` to support the composite
  ownership foreign key;
- `therapy_sessions.user_id -> users.id ON DELETE RESTRICT`;
- composite `therapy_sessions(user_id, therapist_id) ->
  therapists(user_id, id) ON DELETE RESTRICT`;
- `ix_therapists_user_active_name` on `(user_id, active, name, id)`;
- `ix_therapy_sessions_user_occurred_id` on
  `(user_id, occurred_at, id)`;
- `ix_therapy_sessions_user_therapist` on `(user_id, therapist_id)`;
- no unique `(user_id, name)` constraint;
- no `specialty_or_focus`, `clarity_after_session`, appointment, AI or
  progression column.

The SQLAlchemy definitions must be explicit, equivalent to:

```python
UniqueConstraint("user_id", "id", name="uq_therapists_user_id_id")
ForeignKeyConstraint(
    ["user_id", "therapist_id"],
    ["therapists.user_id", "therapists.id"],
    ondelete="RESTRICT",
    name="fk_therapy_sessions_owner_therapist",
)
```

The individual User foreign keys must also be explicit `ForeignKey` or
`ForeignKeyConstraint` definitions with `ondelete="RESTRICT"`.

SQLAlchemy models must import into the shared `Base.metadata`, and migrations
must register all model imports in `migrations/env.py` as current migrations
do.

## 14. Foreign-key and delete behavior

Defense in depth is required:

- application owner-safe lookup prevents cross-owner use;
- composite database FK prevents a mismatched owner pair even if application
  code is bypassed;
- SQLite foreign keys remain enabled through the existing engine hook;
- all User and Therapist references use `RESTRICT`;
- deleting a TherapySession never deletes its Therapist;
- no Therapist deletion is exposed in V1;
- deactivation preserves all historical references.

## 15. Private-text safeguards

`private_note` is highly sensitive free text. The implementation must:

- never log its body;
- exclude it from exception messages;
- exclude it from metrics, tracing attributes and analytics payloads;
- exclude it from progression intents and any Logos payload;
- exclude it from AI/Noema payloads;
- not index it for search;
- return it only to the authenticated owner through owner-scoped endpoints;
- avoid echoing it in validation errors;
- apply the 10,000-character request bound.

Current LifeOS has no established encryption-at-rest mechanism for this field.
No bespoke cryptography is introduced here. Encryption-at-rest is a future
security/privacy decision.

## 16. API surface

Use the existing FastAPI router/dependency style and derive ownership from
`get_current_user_id`.

### Therapists

```text
POST   /therapy/therapists
GET    /therapy/therapists
GET    /therapy/therapists/{therapist_id}
POST   /therapy/therapists/{therapist_id}/deactivate
POST   /therapy/therapists/{therapist_id}/activate
```

Create request: `name` only. V1 responses contain `id`, `name` and `active`;
`created_at` and `updated_at` remain persistence-only columns and are not
exposed without a separately justified use case. No `user_id` input is
accepted.

### Therapy sessions

```text
POST   /therapy/sessions
GET    /therapy/sessions?page=1&size=20
GET    /therapy/sessions/{session_id}
PATCH  /therapy/sessions/{session_id}/private-note
DELETE /therapy/sessions/{session_id}
```

Create request: `therapist_id`, `occurred_at`, and optional `private_note`.
The create response may contain the private note for the authenticated owner.
It does not contain `user_id` as a writable field.

The paginated history response contains only structural navigation data:
session ID, Therapist reference/safe display data and normalized UTC
`occurred_at`. It MUST NOT contain `private_note`.

The detail response may contain `private_note` only for the authenticated
owner. The private-note update response may also contain the updated note for
that owner. There is no bulk note export or search endpoint.

Status proposal:

- `201` create;
- `200` reads, activation/deactivation and note update;
- `204` hard delete;
- `401` missing/invalid authentication;
- `404` well-formed but missing or foreign-owner IDs without existence
  disclosure;
- `409` inactive Therapist on session creation;
- `422` malformed or non-canonical TSID, blank/oversized name/note or invalid
  datetime.

A well-formed but missing or foreign-owner TherapistId/TherapySessionId uses
the indistinguishable `404` path; it is never reported as `422`.

## 17. Transaction boundary

`CreateTherapySession` executes:

1. resolve the authenticated owner;
2. load Therapist with `get_by_id_and_owner`;
3. reject missing/foreign or inactive Therapist;
4. construct TherapySession with normalized UTC time and private note;
5. save through `ITherapySessionRepository`;
6. commit through `SqlAlchemyUnitOfWork`.

There is no downstream call, event publication, progression intent, gateway,
dispatcher, Logos call or Noema call. Therapist creation, activation,
deactivation, note update and deletion each use their own owner-scoped UoW
transaction.

## 18. Migration strategy

Current repository head: `0009`.

### Frozen architecture decision

The next migration number is `0010`, depending on `0009`. It contains only
Therapy V1 persistence described in this plan. It must not contain:

- `clarity_after_session`;
- `specialty_or_focus`;
- appointment/scheduling tables;
- AI/Noema fields;
- progression or occurrence fields;
- unrelated repair or backfill behavior.

The migration must be validated only against disposable databases during its
implementation slice. No real database migration is authorized by this plan.

## 19. Test strategy

### Domain

- valid Therapist creation and name normalization;
- blank/oversized names;
- active default and state transitions;
- valid TherapySession creation;
- missing owner/therapist rejection;
- naive or invalid datetime rejection;
- future `occurred_at` rejection using a controlled clock;
- UTC normalization;
- blank/oversized private note handling;
- structural immutability;
- no status or deferred field in the model.

### Application

- create/list/get Therapist owner scope;
- activate/deactivate behavior;
- inactive Therapist rejected for new sessions;
- create session with same-owner Therapist;
- cross-owner Therapist rejection without disclosure;
- paginated history ordering and filtering;
- private-note update and clear;
- owner-authorized hard delete;
- no progression intent or event interaction.

### Infrastructure/integration

- Therapist and TherapySession round trips;
- shared metadata imports and mapper behavior;
- composite owner FK rejection;
- User and Therapist `RESTRICT` behavior;
- inactive reference preserving historical sessions;
- session hard delete removing private text;
- disposable migration `0009 -> 0010` upgrade validation.

### Presentation/privacy

- authentication required for every endpoint;
- foreign-owner IDs return the same `404` contract as missing IDs;
- request validation and status codes;
- private note returned only to its authenticated owner;
- private note absent from logs, errors, metrics and traces;
- no dispatcher, Logos gateway, progression intent or Noema access is invoked.

Deferred capabilities must not receive tests in this slice: appointments,
themes, structured reflections, follow-up actions, clarity, progression,
external exposure, AI/Noema and clinical data.

## 20. Documentation reconciliation list

Do not edit these documents in THERAPY-002. Reconcile them after the
implementation contract is accepted:

- `docs/01_PRODUCT/PRD.md`: old Game Engine/event and agenda wording, including
  automatic event assumptions;
- `docs/01_PRODUCT/CAPABILITY_MAP.md`: Therapy “produces events” wording;
- `docs/02_ARCHITECTURE/03_DDD.md`: event naming and aggregate wording;
- `docs/02_ARCHITECTURE/08_EVENTS.md`: `TherapyRegistered` and
  `TherapySessionRecordedEvent` entries;
- `docs/03_DATABASE/ERD.md` and `docs/03_DATABASE/SCHEMA.md`: stale UUID,
  `specialty_or_focus`, `clarity_after_session`, `deleted_at` and legacy
  uniqueness assumptions;
- `docs/03_DATABASE/INDEXES.md`: planned indexes must match the approved
  `0010` schema;
- `docs/00_FOUNDATION/GLOSSARY.md`: add only terms implemented and approved;
- backend API/DTO/service/authorization planning documents: reconcile old
  agenda, clinical, event and Game Engine coupling claims.

These are documentation conflicts or historical planning differences, not
implementation authorization.

## 21. Implementation slicing and gates

### THERAPY-003A — Domain Foundation

Implement both IDs, Therapist Aggregate, TherapySession Aggregate, errors,
ports and domain tests only.

Gate: invariants, UTC normalization, note normalization, future-time policy,
no deferred fields and no events all pass.

### THERAPY-003B — Persistence Foundation

Implement migration `0010`, both SQLAlchemy models, mappers, write/read
repositories, composite ownership FK and persistence/integration/migration
tests.

Gate: owner isolation, composite FK, `RESTRICT`, schema constraints,
round-trip and disposable migration tests pass.

### THERAPY-003C — Therapist Application/API

Implement create, get, list, deactivate and reactivate.

Gate: owner-safe API behavior, active selection behavior and validation pass.

### THERAPY-003D — TherapySession Core Application/API

Implement create, detail and paginated history with private-note minimization.

Gate: API 401/404/409/422 behavior, owner non-disclosure and transaction
boundaries pass.

### THERAPY-003E — Sensitive Content Control

Implement private-note update/clear, owner-authorized hard delete and privacy
regression tests.

Gate: no note leakage, no cascading Therapist deletion, deletion behavior and
read-after-delete pass.

### THERAPY-003F — Documentation Reconciliation / Operational Validation

Reconcile approved planning documents, run disposable migration validation and
quality gates, and perform a separate operational review.

Gate: exact documentation scope, migration evidence and full required quality
checks pass. No Logos, Noema, progression or real migration is included.

## 22. Technical open questions

No unresolved technical question blocks THERAPY-003A through THERAPY-003E.
Future matters are deferred:

- audit/history mechanism for private-note edits;
- future replacement of the hard-delete policy;
- encryption-at-rest;
- privacy/security review before any future external consumer;
- documentation reconciliation governance.

## 23. Deferred

- production code, tests and migration creation;
- clinical, medical or therapist-authored records;
- scheduling, appointments and cancellation;
- themes, structured reflections and follow-up actions;
- `clarity_after_session`, duration, `started_at`, `ended_at`;
- external exposure, progression and any occurrence type;
- Logos, Noema, AI, analytics and search indexing;
- encryption-at-rest design;
- legal or regulatory retention claims.

## 24. Implementation readiness

**THERAPY-002: ARCHITECTURE PLAN FROZEN PENDING PUBLICATION**

**THERAPY V1: IMPLEMENTATION-READY AFTER THERAPY-002 PUBLICATION/MERGE**

Next implementation gate: **THERAPY-003A — DOMAIN FOUNDATION**.

This document still does not create `0010`, modify the database, or authorize
implementation before its publication/merge gate.
