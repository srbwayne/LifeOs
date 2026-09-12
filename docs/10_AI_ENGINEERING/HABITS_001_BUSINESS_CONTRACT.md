# HABITS V1 — Business Contract

**Status:** BUSINESS CONTRACT APPROVED — IMPLEMENTATION NOT AUTHORIZED

**Date:** 2026-09-12

**Canonical baseline:** `2d9dd73364bc92725ed4870c3b59616e44c2812f`

## Authority and scope

`docs/01_PRODUCT/FEATURE_CATALOG.md` is the authoritative Feature-ID registry:

- HAB-001 — Cadastro de hábitos
- HAB-002 — Checklist diário
- HAB-003 — Sequência (Streak)
- HAB-004 — Frequência
- HAB-005 — Estatísticas

Habits V1 includes HAB-001 and HAB-002. HAB-003..005 are deferred. No HAB-006 or later Feature ID is created by this contract.

This is an approved business decision, not a technical specification. No Habits API, schema, migration, production implementation or runtime activation is authorized. The next gate is **HABITS V1 TECHNICAL PLAN / ARCHITECTURE REVIEW**.

## HAB-001 — Habit definition and lifecycle

A Habit is an owner-scoped reusable definition with `id`, `owner_id`, mandatory `name`, optional `description`, `active`, and technical timestamps. Ownership is derived from authentication; `owner_id` is never client-controlled. Names are unique within one owner. A Habit is created active and may be deactivated or reactivated by its owner. Deactivation preserves historical completion facts. V1 does not support rename or delete.

V1 does not include frequency types, target or completed counts, quantities, durations, units, categories, tags, weekdays, date ranges, routines, complex schedules, reminders, notifications, `deleted_at`, or `attribute_code`.

## HAB-002 — Binary daily checklist

A `HabitCompletion` is a binary fact: the owner states that a Habit was completed for a civil date. Completion is represented by row existence, not by a `completed` boolean, count, quantity, duration or target. At most one completion exists for `(owner_id, habit_id, record_date)`.

The owner supplies an explicit `record_date` as a civil `DATE`; it is not derived from UTC. `created_at` is a technical UTC timestamp. No user timezone profile exists in V1, so the product does not infer a local date. Timezone ownership and future-date rules based on it are deferred.

The owner may mark a date, repeat marking is idempotent, and may unmark/remove a completion to correct a historical fact. An inactive Habit does not accept a new completion, while existing historical completions remain queryable. No synthetic missed-day rows are created.

HabitCompletion carries `owner_id` and must belong to the same owner as its Habit. Future technical design should enforce this relationship with an owner-safe constraint. Missing and foreign-owner resources are observationally equivalent; no ownership disclosure through 403 is intended.

## Privacy and integration boundaries

Habits are owner-private personal information by default.

| Boundary | V1 decision |
|---|---|
| Activity existence | YES |
| External exposure | NO |
| Progression eligibility | NO |
| Logos integration | NO |
| Noema / AI access | NO |
| Generic event bus | NO |
| Habits event dispatch | NO |

Activity existence does not imply external exposure, progression eligibility or AI access. LifeOS records Habit facts and does not calculate XP from HabitCompletion.

## Deferred scope

HAB-003 (Sequência/Streak), HAB-004 (Frequência) and HAB-005 (Estatísticas) are deferred, together with quantitative habits, targets, durations, routines, recurring schedules, timezone profiles, reminders, notifications, categories, tags, templates, social features, analytics integration, progression, XP, attribute mapping, Logos transport or adapters, Noema/AI access, and automatic external events.

The next decision gate is **HABITS V1 TECHNICAL PLAN / ARCHITECTURE REVIEW**. Until that gate authorizes implementation, there is no Habits source, migration or operational capability.
