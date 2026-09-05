# TASK-013 — LifeOS to Logos Controlled Reading Pilot

Status: implementation complete; controlled runtime execution pending pilot
environment provisioning.

## Runtime boundary

The `CreateReadingSessionCommandHandler` commits the canonical
`ReadingSession` through `SqlAlchemyUnitOfWork` first. Only after that commit
does it invoke the optional `ProgressionGateway`. The gateway is not called if
domain validation, persistence, or commit fails.

```text
Create ReadingSession
  -> commit LifeOS transaction
  -> map integration fact
  -> POST Logos V3
```

The gateway is disabled by default and is configured with:

```text
LOGOS_ENABLED=false
LOGOS_BASE_URL=<service base URL>
LOGOS_TIMEOUT=5
LOGOS_BEARER_TOKEN=<provided outside the repository>
```

`LOGOS_TIMEOUT` must be positive. No retry is performed.

## Mapping

| LifeOS | Logos |
|---|---|
| `ReadingSession.id` | `execution.idempotencyKey` |
| `ReadingSession.owner_id` / `UserId` | `{externalId}` |
| fixed source | `execution.source = lifeos` |
| fixed subject namespace | path namespace `lifeos` |
| `ReadingSession.pages_read` | `details[0].factorKey = pages_read` |
| fixed configuration | `configuration.key = reading` |

The request is sent to:

```http
POST /api/internal/v3/progression/external/lifeos/{UserId}/evaluate
```

Only the source event ID, user ID, and page count are sent. Notes, book data,
email, username, rules, and progression state are not sent.

## Failure semantics

Logos responses in the 2xx range are logged as successful delivery. HTTP
errors, timeouts, connection failures, missing configuration, and missing
credentials are returned as an unsuccessful delivery result and logged with
the session ID, user ID, and status/error type. Authorization tokens and
payload contents are not logged.

The LifeOS fact remains committed independently of every delivery failure.
The same session can be delivered again with the same `ReadingSession.id`; the
Logos V3 idempotency boundary is responsible for preventing a second
progression mutation.

## Provisioning prerequisites

Before the controlled pilot, provision manually in Logos:

```text
progression_subject_identity: namespace=lifeos, external_id=<UserId>
configuration key: reading
```

No automatic subject/configuration provisioning is part of this slice.

The current environment has no `LOGOS_BASE_URL` or `LOGOS_BEARER_TOKEN`
configured, so a cross-process manual delivery was not executed in this
workspace. Automated mapping, post-commit isolation, disabled integration, and
gateway request tests are covered.

## Deliberate limitations

This is a bounded synchronous-after-commit pilot adapter. It has no durable
outbox, retry scheduler, broker, service-to-service authentication redesign,
source authorization, namespace authorization, or automatic provisioning.
LifeOS remains the canonical owner of the reading fact; Logos remains the
canonical owner of progression state. Any future local cache of the Logos
response must be derived and non-authoritative.
