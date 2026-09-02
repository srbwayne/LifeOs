# ADR-0043

## Título

Python 3.11 — Minimum Platform Runtime

## Status

Accepted

## Data

2026-09-01

---

## Contexto

LifeOS was officially Python >=3.10. READ-005 Slice 4 introduced a frozen
SQLite concurrency requirement: retry eligibility must distinguish SQLITE_BUSY
numerically from other SQLite failures. Python 3.10 stdlib sqlite3 does not
expose the public `sqlite_errorcode` / `sqlite_errorname` API required by that
contract. Python 3.11 provides it. Genuine CPython 3.11.9 / SQLite 3.45.1
contention was proven with SQLITE_BUSY = 5, SQLITE_LOCKED = 6, and a
`BEGIN IMMEDIATE` contention exception exposing code 5 and name SQLITE_BUSY.

## Problema

Keeping Python 3.10 would require weakening numeric classification, relying on
error strings, or introducing an alternate SQLite driver. These outcomes are
incompatible with the approved contract or add unnecessary infrastructure.

## Alternativas Consideradas

### Option A — Keep Python 3.10 + stdlib sqlite3

Rejected: the public runtime API cannot satisfy the numeric error-code
requirement.

### Option B — Raise minimum platform to Python 3.11

Accepted: provides the required public sqlite3 error-code API without a new
dependency.

### Option C — Alternate SQLite driver

Rejected: adds infrastructure and dependency complexity solely to preserve
Python 3.10.

### Option D — Message/string classification

Rejected: violates numeric classification and is sensitive to message text.

## Decisão

- LifeOS minimum supported Python becomes `>=3.11`; Python 3.10 support is dropped.
- Minimum CI interpreter is Python 3.11; Ruff target is `py311`; Mypy target is `3.11`.
- Existing dependency pins remain unchanged and stdlib sqlite3 remains the driver.
- Numeric sqlite3 error-code classification remains required.
- SQLITE_BUSY remains the only retryable acquisition result; SQLITE_LOCKED remains non-retryable.
- String/message matching remains forbidden.
- Slice 4 retry semantics are unchanged by this ADR.
- No schema change, Migration 0008 execution, or Slice 4 runtime activation is authorized by this ADR.

## Consequências

### Positivas

- Public supported sqlite3 numeric error API.
- No additional database driver.
- Simpler Slice 4 implementation and explicit runtime/tooling contract.
- Removal of incompatible Python 3.10 support burden.

### Negativas e trade-offs

- Developer environments must move to Python >=3.11.
- Python 3.10 users can no longer install supported LifeOS versions.
- CI required-context names must change.
- Branch protection requires an explicitly controlled human transition.
- PR #46 must be rebased/remediated after platform integration.
- Ruff remains targeted at `py311`. That target exposes `UP017` for existing
  `datetime.timezone.utc` usage; the rule is explicitly ignored for this
  transition because it is Python 3.11 style modernization, not runtime
  compatibility. Existing datetime usage is not rewritten here; a dedicated
  future modernization may remove the exception.

## Impactos

- Platform: project-wide minimum Python runtime.
- CI: three quality jobs move from Python 3.10 to Python 3.11.
- Tooling: Ruff py311 and Mypy 3.11.
- Dependencies: no pin changes required.
- Application/domain: no semantic change.
- Database schema: none; Migration 0008 is not applied by this decision.
- PR #46 remains separate and is handled only after platform integration.
- Branch protection changes require a later explicit human action.

## Referências

- `NEXT_TASK.md`
- `pyproject.toml`
- `.github/workflows/quality.yml`
- `docs/10_AI_ENGINEERING/CODE_STYLE.md`
- `docs/10_AI_ENGINEERING/TESTING_POLICY.md`
- `docs/02_ARCHITECTURE/09_DECISION_LOG.md`
- `docs/10_AI_ENGINEERING/READ_005_TECHNICAL_PLAN.md`
- Python 3.11 sqlite3 documentation
- SQLite result-code documentation
- PR #46
- CI run `33457790140`
