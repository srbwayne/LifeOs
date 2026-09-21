# LIFEOS-LOGOS-001F — Post-POC Priority Decision

Status: APPROVED / OPTION C SELECTED

## Decision

`LIFEOS-LOGOS-001F-DEC-001` records the human post-POC priority decision:

```text
APPROVED — OPTION C SELECTED:
REUSABLE STRUCTURAL HARDENING BEFORE PRODUCTIZATION DECISION
```

The first bounded LifeOS → Logos Reading POC remains
`VERIFIED / CLOSED AS A BOUNDED POC`. This decision does not promote the
integration to a supported production capability.

The decision does not select Options A, B, or D. It does not authorize another
initiative, and it does not automatically resume WORK-001.

## Context

The POC created one retained LifeOS Book, ReadingSession, and delivered
progression record. Logos recorded one execution for `reading` revision `1`,
with `pages_read = 3`, global XP `3`, Conhecimento XP `3`, and stress `0`.
An identical downstream resubmit returned HTTP 200 without duplicate
progression. Full evidence remains in the canonical POC closure documents.

The POC is closed. Historical unresolved deliveries remain outside its scope,
and no historical replay was authorized.

## Reusable hardening direction

Option C seeks a minimum reusable cross-system hardening foundation before a
later decision on Reading → Logos productization. Candidate areas are:

- service-to-service identity and authentication;
- source and namespace authorization;
- external identity ownership and the cross-service trust boundary;
- operational recovery policy and unresolved delivery handling;
- observability and correlation;
- secret lifecycle;
- deployment and configuration boundaries.

These are candidates for architectural analysis only. This document does not
freeze an implementation, select OIDC, service principals, API keys, topology,
or any other solution.

## Attribute identity state

The Logos source foundation for `Atributo.semanticKey` is already integrated.
`Conhecimento` remains the Reading display/domain attribute and `knowledge` is
its selected semantic catalog identity. Progression HTTP V1 intentionally
preserves UUID-based attribute compatibility. The repository migration head is
V44, while operational V44 deployment was not reverified by this decision.

Remaining semantic-identity questions include operational rollout, catalog data
assignment, consumer compatibility governance, and future HTTP semantic-key
evolution. They are not resolved here.

## WORK-001 and historical deliveries

WORK-001 remains:

```text
PRODUCT CONTRACT APPROVED / FROZEN
TEMPORARILY DEFERRED AT ARCHITECTURE GATE
IMPLEMENTATION NOT AUTHORIZED
```

If later resumed, its next gate is
`WORK-001-ARCH-001 — ARCHITECTURE REVIEW`. It is not resumed by this decision.

The following historical deliveries remain unchanged and excluded:

```text
0RH9P86RHH41F — PENDING / attempts 0
0RH9CJ0QW56TE — FAILED / attempts 3 / http_status_404
0RHZMAPV7C31Y — PENDING / attempts 0
```

Historical replay and `dispatch_unresolved()` remain unauthorized.

## Next gate

The only authorized next gate is:

```text
LIFEOS-LOGOS-001G — CROSS-SYSTEM HARDENING ARCHITECTURE / SCOPE FREEZE
```

It is a read-only architecture/scope review. Its purpose is to define the
minimum coherent reusable hardening foundation, ownership boundaries,
dependencies, logical ordering, productionization blockers, optional
improvements, conceptual allowlists, and later gates.

`001G` is authorized but not executed by this document.

## Explicit non-authorization

This decision authorizes no runtime, database mutation, migration, progression,
replay, source implementation, test implementation, security implementation,
OIDC, service identity, observability, deployment, WORK-001 work, or Reading →
Logos productization.
