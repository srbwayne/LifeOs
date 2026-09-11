# THERAPY-003F — Therapy V1 Implementation Closeout

Status: **IMPLEMENTATION COMPLETE — OPERATIONAL ACTIVATION NOT YET AUTHORIZED**

Canonical implementation SHA: `100a8536f29ce7b756add6487f92d628c6af0ce6`

## Business authority

`TherapySession` is an owner-reported historical fact: it is not an appointment, clinical record, or therapist-authored medical record. `Therapist` is a separate reusable, owner-scoped reference. `private_note` is an optional owner-authored private reflection, not a clinical or medical note.

## Privacy matrix

| Concern | Therapy V1 |
|---|---|
| Activity existence | YES |
| External exposure | NO |
| Progression eligibility | NO |
| AI / Noema access | NO |

Activity existence is independent of external exposure, progression eligibility, and AI access.

## Final capabilities

Therapist supports create, get, list, deactivate, and reactivate. Therapist deletion and rename are not supported.

TherapySession supports create, detail, paginated history, private-note replacement, explicit-null clearing, whitespace-to-null clearing, and owner-authorized hard delete.

## Final API surface

Therapist routes are `POST /therapy/therapists`, `GET /therapy/therapists`, `GET /therapy/therapists/{therapist_id}`, `POST /therapy/therapists/{therapist_id}/deactivate`, and `POST /therapy/therapists/{therapist_id}/reactivate`.

TherapySession routes are:

- `POST /therapy/sessions` — 201
- `GET /therapy/sessions` — 200, paginated
- `GET /therapy/sessions/{session_id}` — 200
- `PATCH /therapy/sessions/{session_id}/private-note` — 200, `{id, private_note}`
- `DELETE /therapy/sessions/{session_id}` — 204 with an empty body

Ownership always comes from authentication. Malformed identifiers return 422. Well-formed missing and foreign identifiers return the same 404 contract. Inactive Therapists are rejected for new sessions. History never projects `private_note`.

## Domain and persistence boundaries

TherapySession structural fields (`owner_id`, `therapist_id`, `occurred_at`) are immutable; only `private_note` is mutable. Structural correction is delete plus create. Historical sessions remain readable after Therapist deactivation, and Therapist survives session deletion. Migration `0010` owns the Therapy V1 schema, including the composite owner/Therapist foreign key and restrictive ownership behavior.

## Privacy hardening

Sensitive command, DTO, request, and response representations omit note content from `repr`. The request-validation sanitizer removes invalid private-note input values from errors. Owner isolation and missing/foreign equivalence prevent disclosure. History queries and projections exclude `private_note`. No private note is sent to progression, Logos, Noema, or AI. Encryption-at-rest and backup erasure are not claimed.

## Non-capabilities and deferred items

Therapy V1 excludes appointments, scheduling, diagnosis, treatment records, clinical notes, note audit/version history, structured themes, AI/Noema ingestion, external exposure, Logos/progression, progression events/intents, Therapist deletion, soft delete, duration/start/end, and a generic Therapy event bus.

## Implementation provenance

- 003A — Domain Foundation — CLOSED
- 003B — Persistence Foundation — CLOSED
- 003C — Therapist Application/API — CLOSED
- 003D — TherapySession Core Application/API — CLOSED
- 003E — Sensitive Content Control — CLOSED (PR #68)
- 003F — closeout and isolated operational validation

The canonical final main is `100a8536f29ce7b756add6487f92d628c6af0ce6`. Earlier slice details remain in Git history and the merged PR records; no unsupported historical SHA claims are added here.

## Operational state

Canonical Git migration head: `0010`.

The operational LifeOS database intentionally remains at `0009`. Therapy operational cutover is **NOT AUTHORIZED / NOT EXECUTED**. Implementation completion does not activate the operational schema, and this closeout does not imply Therapy tables exist in the real database.

## Validation boundary and next gate

Migration validation in this slice uses only a newly created disposable database. The real database and operational runtime are not accessed. The next separate gate is **THERAPY OPERATIONAL ACTIVATION / CUTOVER**, which must independently authorize backup, integrity checks, migration 0009 to 0010, post-migration verification, runtime update, authenticated smoke testing, and rollback criteria.

No progression dispatch, Therapy events, Logos integration, or Noema/AI integration is included.
