# HABITS-001 ? Habits V1 Business Contract

Status: **BUSINESS CONTRACT APPROVED ? IMPLEMENTATION NOT AUTHORIZED**

Date: `2026-09-12`

Canonical baseline: `2d9dd73364bc92725ed4870c3b59616e44c2812f`

Feature-ID authority: `docs/01_PRODUCT/FEATURE_CATALOG.md`

This is a business contract, not a technical specification. Where older planning documents conflict with this approved contract, this document is the current Habits V1 business decision after reconciliation.

## V1 scope

V1 includes **HAB-001 ? Cadastro de h?bitos** and **HAB-002 ? Checklist di?rio**. HAB-003 ? Sequ?ncia (Streak), HAB-004 ? Frequ?ncia, and HAB-005 ? Estat?sticas are deferred. No HAB-006 or later Feature IDs are created.

## HAB-001 ? Habit definition

A Habit is an owner-scoped reusable definition with `id`, `owner_id`, mandatory `name`, optional `description`, `active`, and technical timestamps. The owner is derived from authentication. The name is unique within one owner. A Habit is active when created; its owner may deactivate and reactivate it. Deactivation preserves historical completion facts. V1 has no rename or delete.

Frequency types, target/completed counts, quantities, durations, units, attribute mapping, categories, tags, weekdays, start/end dates, routines, schedules, reminders, notifications, and `attribute_code` are excluded. `attribute_code` is not reserved as an unused field.

## HAB-002 ? Binary daily checklist

`HabitCompletion` is a binary completion fact: its existence means the owner states that the Habit was completed for the selected civil date. At most one fact exists for `(owner_id, habit_id, record_date)`. Repeating a mark is idempotent. The owner may remove a completion to correct an historical record; correction is unmark plus mark on the correct date. No completed boolean, quantity, duration, target, or synthetic missed-day row exists.

An inactive Habit does not accept a new completion. Existing historical completions remain queryable after deactivation. HabitCompletion carries `owner_id`, and future technical design must enforce that it matches the Habit owner, preferably through an owner-safe composite constraint. Missing and foreign-owner resources are observationally equivalent to API clients.

## Civil-date semantics

`record_date` is an explicit civil `DATE` supplied by the client. It is not derived from a UTC datetime. `created_at` is a technical UTC timestamp. No per-user timezone exists yet, so owner-local date derivation and future-date rules based on timezone are deferred until timezone ownership exists.

## Mutability and privacy

Habit supports create, read, list, deactivate, and reactivate only. HabitCompletion supports mark/create, idempotent repeat, and unmark/remove. Habit data is owner-private personal information. Activity existence is YES; external exposure, progression eligibility, Logos integration, Noema/AI access, generic event-bus dispatch, and Habits event dispatch are NO. LifeOS records Habit facts and does not calculate XP from HabitCompletion.

## Deferred scope

Deferred items include streaks, frequency, statistics, quantitative habits, routines, recurring schedules, reminders, notifications, categories, tags, templates, social features, progression, XP, attribute mapping, Logos transport, Noema/AI, analytics integration, and automatic external events.

No migration, API, schema, production implementation, event, or integration is authorized by this document.

Next gate: **HABITS V1 TECHNICAL PLAN / ARCHITECTURE REVIEW**.
