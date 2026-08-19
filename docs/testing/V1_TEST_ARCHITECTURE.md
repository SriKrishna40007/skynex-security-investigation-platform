# SKYNEX V1 — Test Architecture (TEMPLATE — requires repo inspection to finalize)

> **Status: SAMPLE / PLACEHOLDER.** This document has NOT been derived from the actual
> SKYNEX repository. Every bracketed `[ ]` item below must be filled in from real code
> inspection before this document is considered valid. Do not treat any statement here
> as a fact about SKYNEX until verified against the repo.

## 1. Purpose

This document describes the actual test architecture of SKYNEX V1, derived from
inspection of the codebase (backend, frontend, tests, configuration). It is the
foundation every other testing document in this package builds on.

## 2. Repository Map (fill in from real repo)

| Area | Path | Framework / Tooling | Notes |
|---|---|---|---|
| Backend app | `backend/` | [FastAPI version] | [ ] |
| Domain models | `backend/[domain]/` | [ ] | [ ] |
| Application services | `backend/[application]/` | [ ] | [ ] |
| Orchestrator | `backend/[orchestrator]/` | [ ] | [ ] |
| Engines (traversal, blast radius, attack path, risk) | `backend/[engines]/` | [ ] | [ ] |
| ORM models | `backend/[models]/` | [ ] | [ ] |
| API routers | `backend/[api]/` | [ ] | [ ] |
| Alembic migrations | `alembic/` | [ ] | [ ] |
| Frontend app | `frontend/` | [React version, Vite/CRA/Next] | [ ] |
| Frontend API clients | `frontend/src/[api]/` | [ ] | [ ] |
| Frontend repositories | `frontend/src/[repositories]/` | [ ] | [ ] |
| Frontend pages/routes | `frontend/src/[pages]/` | [ ] | [ ] |
| Existing backend tests | `backend/tests/` or `tests/` | [pytest?] | [ ] |
| Existing frontend tests | `frontend/[tests dir]` | [vitest/jest?] | [ ] |

## 3. Backend Endpoint Inventory (fill in from real repo)

| Method | Path | Auth Required | Purpose | Existing Test? |
|---|---|---|---|---|
| POST | `/api/v1/investigations` | [ ] | Create investigation | [ ] |
| GET | `/api/v1/investigations/{id}` | [ ] | Read investigation | [ ] |
| GET | `/api/v1/investigations` | [ ] | List/history | [ ] |
| DELETE | `/api/v1/investigations/{id}` | [ ] | Delete investigation | [ ] |
| GET | `/api/v1/investigations/{id}/export` | [ ] | Export | [ ] |
| POST | `/api/v1/auth/login` | N/A | Login | [ ] |
| POST | `/api/v1/auth/logout` | [ ] | Logout | [ ] |
| GET | `/health` | No | Health contract | [ ] |
| ... | ... | ... | ... | ... |

*(Replace with the actual route table — grep `@router.` / `@app.` decorators across the backend.)*

## 4. Frontend Route Inventory (fill in from real repo)

| Route | Page Component | Auth Guarded? | Data Source |
|---|---|---|---|
| `/login` | [ ] | No | [ ] |
| `/dashboard` | [ ] | Yes | [ ] |
| `/investigations/new` | [ ] | Yes | [ ] |
| `/investigations/:id` | [ ] | Yes | [ ] |
| `/investigations/:id/resources` | [ ] | Yes | [ ] |
| `/investigations/:id/graph` | [ ] | Yes | [ ] |
| `/investigations/:id/attack-paths` | [ ] | Yes | [ ] |
| `/investigations/:id/reports` | [ ] | Yes | [ ] |
| ... | ... | ... | ... |

## 5. V1 Workflow Inventory

| Workflow | Entry Point | Backend Path | Persistence Touched |
|---|---|---|---|
| Terraform ingestion → canonical model | [ ] | [ ] | [ ] |
| Relationship discovery | [ ] | [ ] | [ ] |
| Candidate detection/context/impact | [ ] | [ ] | [ ] |
| Security traversal | [ ] | [ ] | [ ] |
| Blast radius | [ ] | [ ] | [ ] |
| Attack path + risk | [ ] | [ ] | [ ] |
| IAM investigation | [ ] | [ ] | [ ] |
| Remediation engine | [ ] | [ ] | [ ] |
| Export (JSON/Markdown) | [ ] | [ ] | [ ] |
| Auth (login/session) | [ ] | [ ] | [ ] |

## 6. Existing Automated Test Inventory

| Suite | Location | Count | Framework | Coverage Area |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] |

*(Run `pytest --collect-only` and the frontend test runner's list/dry-run mode to populate this table with real counts.)*

## 7. External / Environment Dependencies

| Dependency | Required For | Local Substitute |
|---|---|---|
| PostgreSQL | Persistence | Docker container / test DB |
| [Auth provider, if any] | Login | [ ] |
| [ ] | [ ] | [ ] |

## 8. Known Gaps / Placeholder Markers Found in Source

| File | Line | Marker | Classification (TODO/mock/dead code) |
|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] |

*(Populate via `grep -rn "TODO\|FIXME\|Coming Soon\|mock\|placeholder" backend/ frontend/`.)*

## 9. Frontend/Backend Contract Boundaries

Document each place where a frontend type must exactly match a backend response
schema (Pydantic model ↔ TypeScript interface). Any mismatch here is a release-blocking
data-consistency defect.

| Backend Schema | Frontend Type | Verified Match? |
|---|---|---|
| [ ] | [ ] | [ ] |

---
**Next step:** re-run this document generation against the real repository (upload the
codebase or a GitHub URL) so every `[ ]` above is replaced with verified facts.
