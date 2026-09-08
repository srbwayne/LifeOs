# LifeOS Activity Inventory and Progression Readiness

Status: **BUSINESS REVIEW REQUIRED — DOCUMENTATION ONLY**

Date: 2026-09-08

This inventory records the current LifeOS activity evidence and the maturity of
possible future activity sources for progression. It does not implement a new
capability, occurrence type, adapter, transport or progression rule.

## Authority boundary

LifeOS owns observed activity facts. Logos owns the interpretation of those
facts for progression.

LifeOS may own `occurrence.type` as a semantic description of an observed
occurrence. Logos owns the mapping from that type to progression configuration.
Therefore this inventory does not freeze a Logos configuration key, skill
policy, revision, XP value, attribute XP value, stress effect, level effect,
multiplier or rule revision as LifeOS activity data.

Progression eligibility is opt-in per activity capability. The existence of a
LifeOS activity does not automatically make it progression-eligible or safe to
expose externally. For sensitive capabilities such as Therapy and Sleep, the
following are separate decisions: whether the activity exists, whether any
facts may cross the integration boundary, and whether the capability is
progression-eligible.

The current canonical runtime is the source baseline for this audit:

- main: `5e7605c28869a7095cca2d50bdcbf10df41da768`;
- current implemented activity capability: Reading;
- current progression boundary: durable delivery intent plus a
  `ProgressionGateway` port;
- default downstream: `NoOpProgressionGateway`;
- current real downstream integration: not activated.

## Maturity summary

| Activity or candidate | Classification | Evidence | Progression readiness |
|---|---|---|---|
| `ReadingSession` | MATURE | Implemented aggregate, persistence, command, APIs and durable delivery boundary | Baseline-ready for business review; occurrence contract still needs explicit product/architecture freeze |
| `TherapySession` | NEW | PRD, DDD, ERD and planned events only; no `app` implementation | Not ready; business refinement required |
| `WorkoutRecord` / `Workout` | NEW | PRD, DDD, ERD and planned events only; no `app` implementation | Not ready; activity lifecycle and facts require refinement |
| `HabitRecord` / `Habit` | NEW | PRD, DDD, ERD and planned events only; no `app` implementation | Not ready; completion and recurrence semantics require refinement |
| `SleepRecord` | NEW | Health DDD and ERD planning only; no `app` implementation | Not ready; health/privacy and finalization semantics require refinement |
| Study / learning | NEW | Product-level learning references only; no authoritative capability/entity found | No contract; do not model yet |
| Tasks / goals | NEW | No authoritative activity capability/entity found in the inspected sources | No contract; do not model yet |
| `Book`, `ReadingProgress`, `BookCompletion`, reading insights/statistics | NOT PROGRESSION RELEVANT as independent activities | Library entity, derived read models, milestone or analysis outputs | Must not be mistaken for independent activity occurrences |

No activity is classified REFINE as a separate implemented capability. The
ReadingSession progression boundary has refinement questions, but the underlying
activity itself is mature.

## Inventory contract

The fields below are the required review vocabulary. `OPEN` means that the
repository does not define a safe answer yet; it is not a permission to infer
one during implementation.

## 1. ReadingSession — MATURE reference activity

### Business meaning

An authenticated user's historical reading fact for one owned Book and one
page interval. ReadingSession is a concrete aggregate with its own stable
identity; ReadingProgress and reading insights are derived from recorded
sessions.

### Current contract

| Field | Current evidence / decision |
|---|---|
| Current status | MATURE; implemented in `app/read` |
| Aggregate / entity | `ReadingSession`, associated with `Book` |
| Activity ID | `ReadingSessionId`, canonical TSID; logical occurrence identity |
| Owner identity | `UserId` / persisted `reading_sessions.user_id` |
| Lifecycle | Created as a historical fact with required `started_at` and `ended_at`; no public edit or delete flow is implemented |
| Time model | Functional UTC `started_at` and `ended_at`; technical `created_at` and `updated_at` |
| Objective facts | owner, book, start page, end page, start/end timestamps |
| Quantitative facts | `pages_read = end_page - start_page + 1`; coverage is separately derived from the union of session intervals |
| Metadata | Nullable `notes`; it is not a progression fact and must not be forwarded by default |
| Progression eligible | OPT-IN: YES for this first concrete reference activity; eligibility is capability-specific, not automatic |
| Occurrence type | `reading.session.completed` as the LifeOS-owned semantic type proposed for this reference contract |
| Facts that may be exposed to progression | V1: `pages_read`; occurrence identity and ownership are envelope/context facts; notes and derived insights are excluded |
| Idempotency source ID | `ReadingSession.id`; the durable delivery record is unique per ReadingSession |
| Edit before finalization | No separate finalization state exists; creation records the completed historical interval. Whether a draft/pre-finalization state is needed is OPEN |
| Edit after finalization | No public edit behavior exists; correction policy is OPEN |
| Edit after progression | No edit behavior exists; compensating occurrence or correction semantics are OPEN |
| Cancellation semantics | No cancellation state or operation is defined; OPEN |
| Delete after progression | No public delete flow; retention and deletion policy are OPEN |
| Integration failure semantics | Durable intent is persisted atomically with the committed ReadingSession. Delivery is independent and at-least-once; `PENDING`, retryable `FAILED`, terminal `FAILED` and `DELIVERED` are supported. Recovery is explicit through `dispatch_unresolved()` and is not automatic |
| Privacy / sensitivity | Notes may contain personal content; do not expose them to progression. Reading facts are owner-scoped |
| Open business questions | Whether `reading.session.completed` becomes a formal typed field; finalization/correction policy; whether later corrections require compensating occurrences; retention; exact occurrence envelope |

### Current progression boundary

The current application creates a durable progression intent in the same write
transaction as the ReadingSession. The post-commit gateway boundary carries an
occurrence with owner, ReadingSession identity and `pages_read`. The default
`NoOpProgressionGateway` performs no downstream action; the durable intent still
exists. A durable gateway can route the occurrence to the explicit dispatcher.

The current delivery contract is at-least-once. Same-owner ordering is enforced
by unresolved predecessor checks; terminal `http_status_400` and
`http_status_409` failures do not block newer records, while retryable or
pending predecessors do. These delivery mechanics do not make Logos
configuration part of the LifeOS activity contract.

The V1 progression fact for this inventory is only:

```text
occurrence.type = reading.session.completed
occurrence.source_id = ReadingSession.id
facts.pages_read = ReadingSession.pages_read
```

The type is a proposed LifeOS-owned semantic contract for business review. It
does not assert that the current Python occurrence object already contains a
`type` field.

## 2. TherapySession — NEW refinement placeholder

### Evidence

Therapy is present in the product PRD (`RF-THER`), DDD bounded-context notes,
planned `Therapist` / `TherapySession` entities and the ERD. No Therapy module,
model, repository, command or API was found under `app`.

### Inventory

| Field | Current answer |
|---|---|
| Business meaning | Planned registration of a therapeutic session associated with a therapist |
| Current status | NEW; planned only, not implemented |
| Aggregate / entity | Planned `TherapySession`; exact aggregate boundary OPEN |
| Activity ID | Planned `therapy_sessions.id`; representation and source identity OPEN |
| Owner identity | Planned `user_id`; ownership rules OPEN |
| Lifecycle | Registration is described; finalization, correction and cancellation are OPEN |
| Time model | Planned `occurred_at`; timezone and session interval semantics OPEN |
| Objective facts | Therapist relationship and occurrence time are suggested by planning documents |
| Quantitative facts | Planned `clarity_after_session` appears in ERD; whether it is an activity fact and whether it is sensitive are OPEN |
| Metadata | `session_notes` is planned and potentially highly sensitive |
| Progression eligible | OPEN; no automatic eligibility is authorized, and any future exposure requires a separate privacy decision |
| Occurrence type | OPEN; do not freeze one yet |
| Facts that may be exposed to progression | NONE approved; private notes, themes and reflections must not be assumed payload |
| Idempotency source ID | Planned session ID is a candidate; OPEN until lifecycle is defined |
| Edit before finalization | OPEN |
| Edit after finalization | OPEN |
| Edit after progression | OPEN; correction/compensation semantics required |
| Cancellation semantics | OPEN |
| Delete after progression | OPEN; retention and legal/privacy requirements required |
| Integration failure semantics | OPEN; no delivery boundary exists |
| Privacy / sensitivity | High sensitivity. Therapy notes, themes, reflections and private textual content are excluded by default |
| Open business questions | What constitutes one session; finalization; corrections; cancellation; deletion; follow-up actions; progression eligibility; minimal non-sensitive fact crossing the boundary |

Therapy is the recommended next business-refinement candidate because its
privacy and finalization questions materially constrain any future occurrence
contract. This recommendation authorizes refinement only, not implementation.

## 3. Workout / WorkoutRecord — NEW

### Evidence

Workout appears in the PRD, DDD bounded-context design, planned events and ERD
tables `workout_types` and `workout_records`. No Workout implementation was
found under `app`.

| Field | Current answer |
|---|---|
| Business meaning | Planned registration of physical activities |
| Current status | NEW; planned only |
| Aggregate / entity | Planned `Workout`, `Exercise`, `WorkoutType` / `WorkoutRecord`; exact aggregate OPEN |
| Activity ID | Planned `workout_records.id`; representation OPEN |
| Owner identity | Planned `user_id`; ownership OPEN |
| Lifecycle | Registration and possible completion are described; finalization/correction OPEN |
| Time model | Planned `occurred_at`; duration and timezone semantics OPEN |
| Objective facts | Workout type and occurrence time are planned |
| Quantitative facts | Planned duration, heart rate, perceived effort, calories and distance; authoritative subset OPEN |
| Metadata | Planned `notes`; sensitivity and exposure policy OPEN |
| Progression eligible | OPEN; activity existence does not imply external exposure or progression eligibility |
| Occurrence type | OPEN |
| Facts that may be exposed to progression | NONE approved; no XP or configuration fact belongs here |
| Idempotency source ID | Planned workout record ID, subject to lifecycle decision |
| Edit/cancel/delete semantics | OPEN before and after finalization/progression |
| Integration failure semantics | OPEN; no delivery boundary exists |
| Privacy / sensitivity | Health and biometric measurements may be sensitive |
| Open business questions | What completes a workout; correction policy; imported data; minimal stable facts; privacy and retention |

## 4. Habits / HabitRecord — NEW

### Evidence

Habits appears in the PRD, DDD bounded-context design, planned
`Habit`/`HabitRecord`/`HabitStreak` entities and planned completion/broken events.
No Habits implementation was found under `app`.

| Field | Current answer |
|---|---|
| Business meaning | Planned recurring habit definition and dated execution record |
| Current status | NEW; planned only |
| Aggregate / entity | Planned `Habit`, `HabitRecord`, `HabitStreak`; activity candidate is the record, not the definition |
| Activity ID | Planned `habit_records.id`; representation OPEN |
| Owner identity | Planned `user_id` |
| Lifecycle | Habit definition, daily record and streak are distinct concepts; finalization semantics OPEN |
| Time model | Planned `record_date`; timezone and late-entry rules OPEN |
| Objective facts | Habit identity, date and completion state |
| Quantitative facts | Planned target and `completed_count`; recurrence semantics OPEN |
| Metadata | Name, description and planned attribute code; exposure policy OPEN |
| Progression eligible | OPEN; a streak is not automatically an occurrence |
| Occurrence type | OPEN |
| Facts that may be exposed to progression | NONE approved |
| Idempotency source ID | Candidate `HabitRecord.id` or `(user, habit, record_date)` uniqueness; OPEN |
| Edit/cancel/delete semantics | OPEN, especially late corrections and broken streaks |
| Integration failure semantics | OPEN; no delivery boundary exists |
| Privacy / sensitivity | Habit names/descriptions may disclose health or personal routines |
| Open business questions | What is final; whether repeated corrections emit occurrences; streak semantics; deletion; minimal non-sensitive fact |

## 5. SleepRecord — NEW

### Evidence

Sleep is described under the planned Health context and ERD `sleep_records`
schema. No Health or Sleep implementation was found under `app`.

The planned fields include date, duration, HRV, resting heart rate, sleep
stages and sleep score. These are health-sensitive facts, not progression
payload by default.

| Field | Current answer |
|---|---|
| Business meaning | Planned daily health/sleep record |
| Current status | NEW; planned only |
| Aggregate / entity | Planned `SleepRecord`; aggregate boundary OPEN |
| Activity ID | Planned record ID; representation OPEN |
| Owner identity | Planned `user_id` |
| Lifecycle / time model | Daily `record_date`, with technical timestamps; finalization and corrections OPEN |
| Objective facts | Record date and selected measurements |
| Quantitative facts | Duration, HRV, heart rate, sleep stages, score; authoritative subset OPEN |
| Metadata | No approved progression metadata |
| Progression eligible | OPEN |
| Occurrence type | OPEN |
| Facts that may be exposed to progression | NONE approved |
| Idempotency source ID | Candidate record ID or unique `(user_id, record_date)`; OPEN |
| Edit/cancel/delete semantics | OPEN |
| Integration failure semantics | OPEN; no delivery boundary exists |
| Privacy / sensitivity | High health sensitivity; raw measurements must not cross the progression boundary by assumption |
| Open business questions | Whether any derived non-sensitive summary may be exposed; correction and retention; consent; source/import provenance |

## 6. Study / learning, tasks and goals — NEW only if separately authorized

The inspected repository contains product-level references to learning,
productivity and goals, but no authoritative bounded context, aggregate,
entity, persistence model, command or API for Study, Task or Goal. They are
therefore not current LifeOS activity contracts.

If a future initiative selects one of them, it must first define its own
activity facts, owner, lifecycle, finalization and privacy boundary. No
occurrence type, idempotency source or progression fact is proposed here.

## 7. Not independent progression activities

`Book` is a library entity, not an activity occurrence. `ReadingProgress`,
reading statistics and reading insights are derived/read-model outputs.
`BookCompletion` is a durable milestone generated from coverage; it is not the
same activity as the ReadingSession that produced it. None should be treated as
an additional progression activity without a separate business decision.

## Progression readiness conclusions

1. `ReadingSession` is the only mature concrete activity reference.
2. Its stable occurrence identity is `ReadingSession.id`.
3. The proposed LifeOS-owned occurrence type is
   `reading.session.completed`.
4. The only V1 progression fact approved by this inventory is `pages_read`.
5. Logos configuration mapping remains Logos-owned and is intentionally absent.
6. Durable intent persistence, at-least-once delivery, explicit recovery and
   the default NoOp downstream are existing boundaries, not new behavior in
   this document.
7. Therapy is the recommended next business-refinement capability, with
   privacy and finalization as the first decisions.
8. No future activity is ready for implementation or progression integration
   solely because it appears in planning documents.

## Architectural risks

- confusing activity facts with progression interpretation;
- freezing a Logos configuration key in LifeOS;
- using mutable or derived read-model state as an occurrence identity;
- unclear finalization/correction semantics causing duplicate or compensating
  occurrences;
- assuming all planned schemas are implemented;
- treating at-least-once delivery as exactly-once;
- coupling private or health-sensitive content to progression payloads.

## Privacy risks

Therapy content, habit descriptions, workout notes and health measurements may
be sensitive. No private textual content, therapy themes, reflections, notes or
raw health measurements are approved for progression exposure by this
inventory. Any future boundary requires explicit data minimization, ownership,
consent, retention and correction decisions.

## Review boundary

This document is a business/governance inventory only. It creates no code,
migration, event publisher, adapter, Logos contract, scheduler, worker or
automatic recovery behavior. A future implementation requires a separately
approved capability scope and a reviewed occurrence contract.
