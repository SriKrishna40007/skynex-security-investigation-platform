# SKYNEX V1 — Master Test Plan (SAMPLE)

## 1. Scope

V1 release-blocking scope (fixed):

1. Terraform ingestion
2. Canonical resource model
3. Relationship discovery / semantics
4. Candidate detection / context / impact
5. Security traversal
6. Blast radius
7. Attack paths + semantic risk
8. Orchestrator
9. Public response / API contracts
10. IAM investigation
11. Authentication foundation
12. Investigation ownership / history / export / delete
13. Health contract
14. Legacy Terraform contract
15. V1 regression gate
16. API validation / security boundary
17. Secret / configuration hardening
18. Frontend / UI integration & production polish
19. SaaS login / session UX
20. Remediation engine
21. E2E release acceptance
22. Release documentation

## 2. Out of Scope (not release blockers for V1)

- MFA
- Device management
- Enterprise SSO
- Advanced Copilot
- Provider/rule expansion
- 3D graph visualization

Any defect found in these areas is logged (P3 by default) but does NOT block release.

## 3. Test Environments

| Environment | Purpose | Notes |
|---|---|---|
| Local Docker Compose | Full-stack functional + E2E testing | backend + frontend + Postgres |
| Backend-only test env | Unit/integration tests, pytest | SQLite or ephemeral Postgres |
| CI environment | Regression gate on every PR | Mirrors local Docker Compose |

## 4. Required Services

- PostgreSQL (persistence layer)
- Backend API (FastAPI/Uvicorn)
- Frontend dev/prod build server
- [Any auth/session service]

## 5. Required Configuration

- `.env` populated from `.env.example` with test-safe values (no production secrets)
- Test database isolated from any real data
- CORS configured to allow the local frontend origin only

## 6. Test Data Strategy

- All Terraform/IAM fixtures live under `tests/fixtures/v1/`
- Fixtures are deterministic — same input always produces the same expected output
- Expected results are derived independently (by hand/spec), never copied from
  implementation output
- Test users are created fresh per test run and torn down after

## 7. Test Execution Order

1. Environment setup + health check
2. Backend unit tests
3. Backend integration tests (DB-backed)
4. API acceptance tests (all endpoints, positive + negative)
5. Security test suite
6. Frontend unit/component tests
7. Multi-operation sequence tests
8. Data consistency tests
9. Failure injection tests
10. Live E2E acceptance walkthrough (manual/browser)
11. Stability/smoke pass
12. Release checklist sign-off

## 8. Test Categories

Code · API · Integration · Security · Database/Persistence · Frontend · Browser/E2E ·
Negative · Failure-injection · Multi-operation · Data-consistency · Regression ·
Release acceptance.

## 9. Severity Definitions

| Severity | Meaning |
|---|---|
| P0 | Catastrophic — security breach, data loss, release blocker |
| P1 | Major V1 functionality broken or security defect — release blocker |
| P2 | Important defect — release blocker unless explicitly accepted by release owner |
| P3 | Cosmetic / non-blocking |

## 10. Release-Blocking Rules

- Any P0 or P1 defect open at release time = automatic RELEASE = FAIL
- Any P2 defect requires an explicit, documented waiver from the release owner
- Any mandatory test left as NOT VERIFIED = RELEASE = NOT READY (never PASS by default)

## 11. Evidence Requirements

Every executed test must produce evidence: HTTP request/response logs, screenshots
for UI, database query output for persistence checks, and console logs for frontend
errors. Evidence is attached in `V1_TEST_EXECUTION_RECORD.md` or linked artifacts.

## 12. Exit Criteria

See `V1_RELEASE_GATE.md` for the full formal gate definition.
