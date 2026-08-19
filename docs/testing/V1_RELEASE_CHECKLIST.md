# SKYNEX V1 — Release Checklist

> No item may be pre-marked PASS. Default state for every item is "Not tested."

| Area | Item | Status |
|---|---|---|
| Backend | Domain layer tests pass | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Backend | Application/orchestrator tests pass | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| API | All public endpoints have positive+negative coverage | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Security | Authentication tests pass | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Security | Authorization / cross-tenant isolation tests pass | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Security | No secret/error/stack-trace leakage | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Terraform | Ingestion handles all 20 fixtures per EXPECTED_RESULTS.md | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| IAM | Investigation handles all 6 IAM fixtures per EXPECTED_RESULTS.md | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Resources | Canonical model correctness | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Relationships | Discovery correctness (incl. no invented edges) | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Candidates | Detection/context/impact correctness | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Traversal | Terminates correctly, handles cycles | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Attack paths | Correctness vs. expected results | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Risk | Scoring within documented bands | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Blast radius | Correctness vs. expected results | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Remediation | Correctly linked to findings, actionable | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Persistence | Create/read/refresh/restart/delete all correct | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| History | Correct, correctly scoped to owner | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Export | JSON/Markdown match persisted data | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Delete | Correct, idempotent-safe, no orphaned data | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Dashboard | Real data only, no placeholders | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Frontend | Resources/Graph/Attack Paths/Reports pages functional | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Frontend | AI Investigation page — real or clearly labeled | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Error handling | No 500s on malformed input, clear error states | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Session | Expiration, refresh, logout all correct | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Configuration | .env/.env.example safe, no committed secrets | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| E2E | Full live acceptance walkthrough passes | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Data consistency | Same investigation consistent across all layers | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Failure injection | All failure modes handled per plan | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Stability | No crashes/races/memory issues under smoke load | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
| Documentation | All testing docs complete and current | ☐ Not tested ☐ PASS ☐ FAIL ☐ NOT VERIFIED |
