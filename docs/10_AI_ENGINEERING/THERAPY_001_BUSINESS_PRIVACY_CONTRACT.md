# THERAPY-001 Business and Privacy Contract

Status: **BUSINESS REVIEW APPROVED — DOCUMENTATION ONLY**

Date: 2026-09-08

This document is a business and privacy refinement for the planned Therapy
capability. It does not authorize implementation, database changes, event
delivery, progression, external exposure, AI access or runtime work.

## 1. Scope and authority

LifeOS owns observed activity facts. Logos owns progression interpretation.
Noema is outside this contract.

The following decisions remain independent:

```text
activity exists
!= external exposure allowed
!= progression eligible
!= AI access allowed
```

Therapy must not calculate or own XP, attribute XP, stress, multipliers,
levels, skills, progression configuration or configuration revisions.

### Existing evidence versus proposed decisions

The canonical repository contains planning references to Therapy, Therapist,
TherapySession, TherapyRegistered/TherapySessionRecorded events, agenda,
history, observations and statistics. The PRD also says that Therapy does not
calculate progression directly and that sensitive data must respect privacy
settings. The DDD, ERD and schema documents describe planned entities and
fields. No Therapy implementation, model, repository, command or API exists
under `app`.

Those planning references are evidence, not approved implementation
requirements. This document records the approved bounded business/privacy
contract for Therapy V1. `OPEN` means that LifeOS has not established a safe
answer for the deferred technical detail.

## 2. Business meaning

### Proposed decision: one TherapySession

A `TherapySession` represents a LifeOS record that an authenticated owner
reports a real therapeutic session occurred with one owner-associated
therapist at a stated time.

It is:

- a personal activity record of an occurrence reported by the owner;
- an owner-scoped historical fact;
- optionally accompanied by private user-authored notes or reflections.

It is not, by this contract:

- a clinical or medical record system;
- a therapist's professional record;
- a diagnosis, treatment plan or clinical measurement;
- a scheduled appointment;
- an automatic signal that progression or external sharing is allowed.

The distinction between a real-world appointment and the LifeOS record is
important: LifeOS stores the owner's record of the occurrence, not an
independent verification of what happened in the consultation.

Follow-up actions are not included in the V1 TherapySession contract. They may
be private notes for now or a future independent capability, but must not be
silently converted into Tasks or Goals.

## 3. Aggregate and identity proposal

### TherapySession

Proposed aggregate root: `TherapySession`.

The session owns the observed occurrence facts and its private content. A
future implementation should not expose internal entities through direct
cross-aggregate access.

### Therapist

Proposed model: `Therapist` is an owner-scoped reference entity separate from
the `TherapySession` aggregate. It may be referenced by many sessions. The ERD
relationship alone is not treated as proof of this proposal; the reason is
that a therapist is a reusable owner-managed reference, while a session is a
historical occurrence.

Both records must be owner-scoped:

- `Therapist.user_id` identifies the authenticated LifeOS owner;
- `TherapySession.user_id` identifies the same owner;
- a session may reference a therapist only when both owners match;
- cross-owner references are forbidden, including through guessed IDs.

### Candidate identifiers

`TherapySessionId` and `TherapistId` should follow the current LifeOS canonical
identifier convention used by implemented aggregates, currently TSID-style
opaque identifiers. Exact value-object names, generation rules and external
mapping are OPEN until implementation is authorized.

No cross-system or Logos identifier is proposed.

## 4. Lifecycle proposal

The current evidence does not require a draft workflow for a historical
session. The conservative V1 proposal is that creating a TherapySession means
the owner is recording that the session already occurred, analogous to the
current ReadingSession historical-fact model.

| Lifecycle concept | V1 proposal | Status |
|---|---|---|
| CREATED / DRAFT | Do not create a draft TherapySession. A future appointment/draft belongs to a separate scheduling concept. | NOT REQUIRED IN V1 |
| FINALIZED / COMPLETED | Successful creation is the stable historical occurrence; no extra finalized state is required. | FROZEN V1 DECISION |
| CORRECTED | Correction is a business operation/recording policy, not a status value yet. | OPEN |
| CANCELLED | A session that did not occur should not be created as a TherapySession. Appointment cancellation is outside this aggregate. | PROPOSED OUT OF SCOPE |
| DELETED / HIDDEN | Do not hard-delete by default. Product retention and privacy behavior require approval. | OPEN |

The exact persisted state model is therefore intentionally not frozen. Adding
`DRAFT`, `COMPLETED`, `CANCELLED` or version states requires evidence that the
historical-fact model is insufficient.

## 5. Time semantics

Minimum V1 business fact: `occurred_at`, representing the instant at which the
reported session occurred.

Proposed rules:

- store and compare the instant with explicit UTC semantics;
- accept a user-local time only with an explicit timezone interpretation before
  normalization;
- do not add duration merely to support progression or analytics;
- `started_at`, `ended_at` and `duration` are not V1 fields;
- technical `created_at` and `updated_at`, if later implemented, are audit
  metadata and not the therapeutic occurrence time.

## 6. Therapist semantics

The minimum useful V1 reference proposal is:

| Field | Classification | V1 proposal |
|---|---|---|
| `name` | Owner-entered reference data | REQUIRED for a usable reference; not a verified professional identity |
| `active` | Owner-managed reference lifecycle metadata | ALLOWED reference metadata; not a session fact |
| `specialty_or_focus` | Descriptive/professional metadata | DEFERRED; no clinical or professional profiling is required in V1 |

Credentials, license data, contact details, diagnosis, treatment specialization
and other professional profiling are unnecessary for THERAPY-001 V1 and are
not proposed.

## 7. Session content and privacy

Private content is not progression payload and is not externally exposed by
default.

| Information | V1 status | Fact type | Sensitivity | Mutable? | External exposure by default |
|---|---|---|---|---|---|
| Owner identity | YES as access/ownership context | Structural private | STRUCTURAL PRIVATE | No semantic reassignment | NO |
| Therapist reference/name | Reference required for the session | Structural/reference fact | STRUCTURAL PRIVATE | Correction policy OPEN | NO |
| `occurred_at` | YES if the session record is retained | Objective occurrence fact | STRUCTURAL PRIVATE | Correction policy OPEN | NO |
| Private reflection / note | YES, one optional user-authored free-text field; implementation-neutral naming | Personal reflection written by the LifeOS owner, not a clinical or medical note | HIGHLY SENSITIVE FREE TEXT | May remain editable under future policy | NO |
| Themes | DEFERRED | User-authored interpretation | HIGHLY SENSITIVE FREE TEXT | DEFERRED | NO |
| Structured reflections | DEFERRED | Subjective reflection | HIGHLY SENSITIVE FREE TEXT | DEFERRED | NO |
| Follow-up actions | DEFERRED | Private action/context | SENSITIVE or HIGHLY SENSITIVE | DEFERRED | NO |
| `clarity_after_session` | DEFERRED FROM V1 | Potential user self-report | DERIVED / SUBJECTIVE | DEFERRED | NO |

Owning a field in LifeOS does not authorize sending it to Logos, analytics,
Noema or any other consumer. Any future exposure requires a separate
allowlist, purpose, consent/privacy and product decision.

## 8. `clarity_after_session`

The field appears in planning/schema material, but its presence is not enough
to make it an approved domain requirement. It is **DEFERRED FROM V1**.

If retained, its only acceptable initial meaning would be an optional,
owner-reported self-assessment captured after the session. It must not be
described as a clinical measurement, therapist assessment or objective outcome.
If reconsidered later, the scale, timing, labels, missing-value semantics and
correction policy require a separate decision. The planned `0..10` constraint
is evidence of an old schema proposal, not an approved V1 contract.

It is not approved for external exposure or progression.

## 9. Follow-up actions

Follow-up actions are OUT OF THERAPY-001 scope.

For this contract they may remain private free-form notes, but a structured
action list should be a separately authorized future capability/entity. No
Tasks or Goals model is introduced here, and no automatic reminders or
completion semantics are proposed.

## 10. Finalization and immutability

The structural occurrence facts should become historically stable when the
owner records the occurred session:

- owner;
- therapist reference;
- occurrence time.

Private user-authored notes should not be forced into the same immutability
rule. A future implementation may allow the one optional private reflection /
note to remain editable under an explicit privacy and audit policy while
preserving the occurrence fact. Whether edits are versioned, timestamped or
simply replace content is OPEN.

No progression-triggered immutability is proposed. Progression eligibility is
independent and is explicitly NO for Therapy V1.

## 11. Correction semantics

Before any future externalization, owner-authorized correction of structural
information may be supported. Correction must distinguish the type of mistake:

| Case | Proposed business meaning |
|---|---|
| Wrong date/time | Correct the owner-reported structural fact before any external use; audit/version semantics are OPEN |
| Wrong therapist | Correct the owner-scoped reference before any external use; ownership must be revalidated |
| Accidental duplicate | Identify and resolve as a duplicate without silently merging private content; exact policy is OPEN |
| Private notes | Allow correction under a privacy policy without changing the historical occurrence by default |

If a future externalized Therapy occurrence exists, it requires a separately
approved correction contract. Distributed compensation or retraction is not
designed by THERAPY-001.

## 12. Cancellation semantics

If `TherapySession` means only an occurred historical fact, a session that did
not occur should never be created as a TherapySession. Cancellation belongs to
a future appointment/scheduling model, if one is authorized.

Whether LifeOS needs such a scheduling capability is OPEN and outside this
contract. It must not be conflated with the historical session aggregate.

## 13. Delete and retention semantics

Current LifeOS product evidence does not establish legal or regulatory
retention obligations. **NOT ESTABLISHED BY CURRENT LIFEOS PRODUCT CONTRACT.**

The product requirement frozen here is that sensitive Therapy content remains
under explicit owner control. The exact storage mechanism is OPEN.

Hard delete, soft delete and archive are deferred to the THERAPY-002
architecture decision. Until then:

- do not hard-delete historical TherapySession data as routine cleanup;
- prefer a hide/archive or soft-delete policy if removal from ordinary views is
  required;
- preserve enough audit information to avoid accidental recreation or exposure;
- define owner-controlled deletion and retention only after privacy/product
  review establishes the required behavior.

The proposal is a product safety recommendation, not a claim of legal duty.

## 14. Privacy classification

| Data class | Classification | Default handling |
|---|---|---|
| Owner identity and ownership links | STRUCTURAL PRIVATE | Access-control context only; no external sharing by default |
| Therapist identity/name | STRUCTURAL PRIVATE | Owner-scoped reference; no external sharing by default |
| Session timestamp | STRUCTURAL PRIVATE | Retain only for the owner's history unless separately approved |
| Session notes, themes and reflections | HIGHLY SENSITIVE FREE TEXT | Private by default; no Logos, Noema, analytics or AI access by default |
| `clarity_after_session` | DERIVED / SUBJECTIVE | Treat as private self-report; not clinical and not externally exposed by default |
| Future follow-up information | SENSITIVE / OPEN | Outside V1; no structured exposure or automation |

## 15. Progression eligibility

`PROGRESSION_ELIGIBLE: NO — THERAPY V1.`

This does not prohibit future participation. Enabling progression requires a
future explicit business/architecture gate. No Therapy progression facts exist
in V1.

No Therapy occurrence type, progression fact, Logos configuration, XP,
attribute XP, stress, level, skill, multiplier or revision is frozen here.

## 16. External exposure

`EXTERNAL_EXPOSURE_ALLOWED: NO — THERAPY V1.`

No Therapy fact is approved for Logos or another external consumer in V1. A
future proposal would need a separate decision for each candidate fact,
including purpose limitation, consent/privacy review, allowlisting and
redaction. Private free text is excluded.

Proposed occurrence type: **NONE**. No Logos occurrence type exists for Therapy
V1.

Facts proposed for external exposure: **NONE**.

## 17. Logos boundary

This contract authorizes no Logos adapter, delivery, gateway change, durable
intent, dispatch, XP semantic or downstream integration. The current
LifeOS/Logos boundary remains the one established for the mature Reading
reference, but Therapy has no progression payload or occurrence contract.

## 18. Noema boundary

No Noema integration or cognitive-ingestion contract is proposed. Therapy
content must not be assumed available to Noema. Any future use would require a
separate explicit privacy, consent, purpose and data-minimization boundary.

## 19. Open business questions

- What future appointment capability, if any, should represent scheduling?
- What exact technical storage mechanism will implement owner-controlled
  deletion or hiding?
- What future correction/version policy applies if external exposure is later
  approved?
- Are notes/reflections editable after the occurrence becomes historically
  stable, and what audit evidence is required?
- What explicit consent and purpose boundaries would be required for any future
  AI use?

## 20. Frozen V1 business decisions

1. Treat TherapySession as an owner-reported historical occurrence, not an
   appointment, scheduling record, clinical record, therapist-authored medical
   record, progression transaction or task.
2. Use TherapySession as the aggregate root and Therapist as a reusable
   owner-scoped reference.
3. Require owner matching for every Therapist/TherapySession relationship.
4. Use only normalized UTC `occurred_at` as the V1 functional time fact.
5. Require exactly one optional private owner-authored reflection/note field;
   themes, structured reflections and follow-up actions are deferred.
6. Defer `clarity_after_session` from V1; if reconsidered, it is a private
   user self-report and not a clinical measurement.
7. Set progression eligibility to NO for Therapy V1.
8. Set external exposure to NO for Therapy V1.
9. Keep owner-controlled deletion/retention storage, future scheduling,
   post-exposure correction and any future external contract outside this task.

## 21. Independent decision matrix

| Question | Therapy V1 |
|---|---|
| Activity exists | YES |
| External exposure allowed | NO |
| Progression eligible | NO |
| AI / Noema access allowed | NO |

## 22. Explicitly deferred items

- all production Therapy code, migrations, tests and APIs;
- event publication or durable progression intents;
- Logos adapter, HTTP/auth/configuration integration and occurrence delivery;
- Noema access, embeddings, summaries or cognitive ingestion;
- XP, skill, stress, level and rule semantics;
- scheduling/appointments, reminders and follow-up task management;
- hard-delete, retention enforcement and legal/compliance claims;
- any Therapy occurrence type or external payload.

## 23. Implementation readiness

**THERAPY-001: BUSINESS CONTRACT FROZEN**

**THERAPY V1: NOT YET IMPLEMENTATION-READY**

Next required gate: **THERAPY-002 — V1 TECHNICAL PLAN**.

That gate is not designed by this document. It must not be interpreted as
authorization for production changes, migrations, progression, external
exposure, Logos or Noema integration.
