# SKYNEX V1 — Live Acceptance Plan (Real-Time Execution Document)

> Execute this with the backend and frontend actually running. Fill in "Actual" and
> "Result" columns live, as you go — do not pre-fill or batch-fill afterward from memory.

**Tester:** ______________  **Date:** ______________  **Build/commit:** ______________

**Environment:** [ ] Local Docker Compose  [ ] Local dev servers  [ ] Staging

---

| # | Step | Action | Expected UI | Expected API | Expected Data | Actual | Result | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | Start backend | `[real command from V1_TEST_COMMANDS.md]` | N/A | Health endpoint reachable | N/A | | ☐P ☐F | terminal log |
| 2 | Start frontend | `[real command]` | Dev server boots, no build errors | N/A | N/A | | ☐P ☐F | terminal log |
| 3 | Open browser | Navigate to app URL | Login page renders, no console errors | N/A | N/A | | ☐P ☐F | screenshot |
| 4 | Register/login | Enter valid test credentials | Redirect to dashboard | POST /auth/login → 200 | Session/token stored | | ☐P ☐F | network tab |
| 5 | Verify session | Refresh page | Still authenticated | N/A | Token/cookie persists | | ☐P ☐F | screenshot |
| 6 | Dashboard | Land on dashboard | Real counts/data shown, no placeholders | GET dashboard data → 200 | Matches DB state | | ☐P ☐F | screenshot |
| 7 | Create investigation | Click "New Investigation" | Upload form renders | N/A | N/A | | ☐P ☐F | screenshot |
| 8 | Upload real Terraform | Upload `16_complex_environment.tf` | Upload accepted, processing indicator shown | POST /investigations → 200/201 | Investigation ID returned | | ☐P ☐F | network tab |
| 9 | Wait for actual result | Wait for processing to complete | Loading state resolves to results, no infinite spinner | GET status → completed | N/A | | ☐P ☐F | screenshot + timing |
| 10 | Verify findings | Inspect findings list | Findings match EXPECTED_RESULTS.md for fixture 16 | GET findings → 200 | IDs/severities match | | ☐P ☐F | screenshot + JSON diff |
| 11 | Verify resources | Open Resources page | All 9 expected resources listed | GET resources → 200 | Resource IDs match canonical model | | ☐P ☐F | screenshot |
| 12 | Verify relationships | Open Graph page | Expected edges rendered (SG chain, instance→profile→role) | GET relationships → 200 | Edge count/direction correct | | ☐P ☐F | screenshot |
| 13 | Verify candidates | Inspect candidate list | High-risk candidate (app_role wildcard s3) flagged | GET candidates → 200 | Context/impact fields populated | | ☐P ☐F | screenshot |
| 14 | Verify candidate context | Open candidate detail | Context matches source HCL | N/A | N/A | | ☐P ☐F | screenshot |
| 15 | Verify candidate impact | Open candidate detail | Impact description references correct downstream resources | N/A | N/A | | ☐P ☐F | screenshot |
| 16 | Verify attack path | Open Attack Paths page | Path matches EXPECTED_RESULTS.md (web_sg → app_server → app_role → app_policy → app_data) | GET attack-paths → 200 | Node sequence correct | | ☐P ☐F | screenshot |
| 17 | Verify blast radius | Inspect blast radius view | Correct resource set shown | GET blast-radius → 200 | Set matches expected | | ☐P ☐F | screenshot |
| 18 | Verify risk | Inspect risk score | Score/severity in documented band | N/A | N/A | | ☐P ☐F | screenshot |
| 19 | Verify remediation | Open remediation panel | Remediation references correct finding ID, actionable text | GET remediation → 200 | Finding ID linkage correct | | ☐P ☐F | screenshot |
| 20 | Refresh | Browser refresh mid-workspace | All data reloads identically, no loss | Re-fetch → 200 | Identical to pre-refresh | | ☐P ☐F | screenshot before/after |
| 21 | Verify persistence | Close and reopen investigation | Same data as before | GET investigation → 200 | Matches step 10-19 exactly | | ☐P ☐F | screenshot |
| 22 | Resources page | Navigate directly via URL | Loads correctly, no dead state | N/A | N/A | | ☐P ☐F | screenshot |
| 23 | Graph page | Navigate directly via URL | Renders correctly | N/A | N/A | | ☐P ☐F | screenshot |
| 24 | Attack Paths page | Navigate directly via URL | Renders correctly | N/A | N/A | | ☐P ☐F | screenshot |
| 25 | AI Investigation page | Open page | Real functionality or clearly labeled not-yet-available; no fake/mock output presented as real | N/A | N/A | | ☐P ☐F | screenshot |
| 26 | Reports | Open reports view | Reflects actual investigation | N/A | N/A | | ☐P ☐F | screenshot |
| 27 | Export | Trigger export (JSON) | File downloads, content matches investigation | GET export → 200 | Diff against persisted data = 0 | | ☐P ☐F | file diff |
| 28 | History | Open investigation history | This investigation appears, correctly attributed | GET history → 200 | Matches DB | | ☐P ☐F | screenshot |
| 29 | Delete | Delete this investigation | Confirmation shown, then removed from UI | DELETE → 200/204 | Row removed/soft-deleted in DB | | ☐P ☐F | screenshot + DB check |
| 30 | Refresh | Browser refresh | Investigation stays gone | GET history → no longer lists it | N/A | | ☐P ☐F | screenshot |
| 31 | Verify deletion | Attempt direct GET by old ID | 404, not a stale cached view | GET /investigations/{id} → 404 | N/A | | ☐P ☐F | network tab |
| 32 | Logout | Click logout | Redirect to login, session cleared | POST /auth/logout → 200 | Token invalidated | | ☐P ☐F | screenshot |
| 33 | Attempt protected access | Navigate to dashboard URL directly while logged out | Redirected to login, no data flash | GET protected route → 401 | N/A | | ☐P ☐F | screenshot + network tab |

**Overall E2E result:** ☐ PASS  ☐ FAIL  ☐ NOT COMPLETE

**Notes / anomalies observed during execution:**
_______________________________________________________________
