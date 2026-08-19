#!/usr/bin/env bash
set -u

# SKYNEX V1 — Claude ZIP / Production-Readiness Acceptance Runner
# Run from Git Bash. This script DOES NOT modify application code or DB schema.
#
# Usage:
#   chmod +x scripts/claude_v1_acceptance.sh
#   ./scripts/claude_v1_acceptance.sh
#
# Optional:
#   BASE_URL=http://127.0.0.1:8000 ./scripts/claude_v1_acceptance.sh
#
# It creates:
#   artifacts/claude-v1-acceptance-<timestamp>.log
#
# IMPORTANT:
# - A PASS means the observed behavior matches the explicit expectation encoded here.
# - A FAIL is a release blocker candidate, not permission to change EXPECTED_RESULTS.md.
# - Review every FAIL before release.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/backend" 2>/dev/null || cd "$ROOT"

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
API="${BASE_URL}/api/v1"
FIXTURES="${FIXTURES:-$PWD/tests/fixtures/v1}"
STAMP="$(date +%Y%m%d-%H%M%S)"
ARTIFACT_DIR="${ARTIFACT_DIR:-$PWD/../artifacts}"
mkdir -p "$ARTIFACT_DIR"
LOG="$ARTIFACT_DIR/claude-v1-acceptance-${STAMP}.log"
TMP_DIR="$ARTIFACT_DIR/.claude-v1-tmp-${STAMP}"
mkdir -p "$TMP_DIR"
RESP_JSON="$TMP_DIR/response.json"
BODY_TXT="$TMP_DIR/body.txt"
export RESP_JSON BODY_TXT
HEADERS_TXT="$TMP_DIR/headers.txt"

PASS=0
FAIL=0
WARN=0
TOTAL=0

log() {
  printf '%s\n' "$*" | tee -a "$LOG"
}

run() {
  "$@" 2>&1 | tee -a "$LOG"
  return "${PIPESTATUS[0]}"
}

pass() { PASS=$((PASS+1)); TOTAL=$((TOTAL+1)); log "PASS | $*"; }
fail() { FAIL=$((FAIL+1)); TOTAL=$((TOTAL+1)); log "FAIL | $*"; }
warn() { WARN=$((WARN+1)); log "WARN | $*"; }

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

log "============================================================"
log "SKYNEX V1 — CLAUDE ZIP / LIVE ACCEPTANCE"
log "Started: $(date)"
log "Base URL: $BASE_URL"
log "Fixtures: $FIXTURES"
log "Log: $LOG"
log "============================================================"

# ------------------------------------------------------------
# 0. Repository/build baseline
# ------------------------------------------------------------
log ""
log "========== 0. BUILD BASELINE =========="

if git diff --check >>"$LOG" 2>&1; then
  pass "git diff --check"
else
  fail "git diff --check reports whitespace/errors"
fi

if uv run pytest -q >>"$LOG" 2>&1; then
  pass "backend regression suite"
else
  fail "backend regression suite"
fi

if (cd "$ROOT/frontend" && npm test -- --run >>"$LOG" 2>&1); then
  pass "frontend tests"
else
  fail "frontend tests"
fi

if (cd "$ROOT/frontend" && npm run lint >>"$LOG" 2>&1); then
  pass "frontend lint"
else
  fail "frontend lint"
fi

if (cd "$ROOT/frontend" && npm run build >>"$LOG" 2>&1); then
  pass "frontend production build"
else
  fail "frontend production build"
fi

# ------------------------------------------------------------
# 1. Environment
# ------------------------------------------------------------
log ""
log "========== 1. ENVIRONMENT =========="

if curl -fsS "$API/health" > "$RESP_JSON" 2>"$BODY_TXT"; then
  cat "$RESP_JSON" | tee -a "$LOG"
  if grep -q '"status"[[:space:]]*:[[:space:]]*"healthy"' "$RESP_JSON"; then
    pass "health endpoint"
  else
    fail "health endpoint returned unexpected body"
  fi
else
  fail "health endpoint unreachable"
fi

if curl -fsS "$BASE_URL/openapi.json" > "$RESP_JSON" 2>/dev/null; then
  ROUTES="$(python -c 'import json; print(len(json.load(open(__import__("os").environ["RESP_JSON"]))["paths"]))')"
  log "OpenAPI routes=$ROUTES"
  [ "$ROUTES" -ge 1 ] && pass "OpenAPI reachable" || fail "OpenAPI route inventory empty"
else
  fail "OpenAPI unreachable"
fi

# ------------------------------------------------------------
# 2. Login / auth foundation
# ------------------------------------------------------------
log ""
log "========== 2. AUTH FOUNDATION =========="

TEST_EMAIL="${SKYNEX_TEST_EMAIL:-v1-verification-tester@gmail.com}"
TEST_PASSWORD="${SKYNEX_TEST_PASSWORD:-V1Verification123!}"

LOGIN_RESPONSE="$(curl -fsS \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}" \
  "$API/auth/login" 2>/dev/null || true)"

if [ -n "$LOGIN_RESPONSE" ]; then
  ACCESS_TOKEN="$(printf '%s' "$LOGIN_RESPONSE" | python -c 'import json,sys; print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null || true)"
else
  ACCESS_TOKEN=""
fi

if [ -n "$ACCESS_TOKEN" ]; then
  pass "login returns access token"
else
  fail "login did not return access token"
fi

if [ -n "$ACCESS_TOKEN" ]; then
  if curl -fsS -H "Authorization: Bearer $ACCESS_TOKEN" "$API/auth/me" >"$RESP_JSON" 2>/dev/null; then
    cat "$RESP_JSON" | tee -a "$LOG"
    pass "authenticated /me"
  else
    fail "authenticated /me"
  fi
fi

# Wrong password must not issue a token.
BAD_LOGIN_CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
  -X POST -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"definitely-wrong-password\"}" \
  "$API/auth/login")"
cat "$BODY_TXT" | tee -a "$LOG"
[ "$BAD_LOGIN_CODE" = "401" ] && pass "wrong-password returns 401" || fail "wrong-password returned HTTP $BAD_LOGIN_CODE"

# ------------------------------------------------------------
# 3. Terraform live acceptance — all 20 fixtures
# ------------------------------------------------------------
log ""
log "========== 3. TERRAFORM — 20 FIXTURES =========="

if [ ! -d "$FIXTURES" ]; then
  fail "fixture directory missing: $FIXTURES"
else
  for i in $(seq -w 1 20); do
    f="$(find "$FIXTURES" -maxdepth 1 -type f -name "${i}_*.tf" | head -1)"
    if [ -z "$f" ]; then
      warn "fixture ${i}_*.tf not found"
      continue
    fi

    name="$(basename "$f")"
    log ""
    log "----- TF $i: $name -----"

    # Expected negative/edge behavior.
    case "$i" in
      10)
        CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
          -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
          -F "terraform_file=@$f" \
          -F "source=aws_instance.public_server" \
          -F "target=aws_s3_bucket.sensitive_data" \
          "$API/investigations/terraform")"
        cat "$BODY_TXT" | tee -a "$LOG"
        if [ "$CODE" -ge 400 ] && [ "$CODE" -lt 500 ]; then
          pass "$name rejects malformed Terraform with 4xx"
        else
          fail "$name expected 4xx validation error, got HTTP $CODE"
        fi
        ;;
      13)
        CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
          -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
          -F "terraform_file=@$f" \
          -F "source=aws_instance.dup_source" \
          -F "target=aws_s3_bucket.dup_bucket" \
          "$API/investigations/terraform")"
        cat "$BODY_TXT" | tee -a "$LOG"
        # Explicitly acceptable: 4xx rejection OR a documented single/deduplicated resource result.
        if [ "$CODE" -ge 400 ] && [ "$CODE" -lt 500 ]; then
          pass "$name rejects duplicate resource address"
        elif [ "$CODE" = "200" ] && python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
rs=d.get("resources",[])
ids=[r.get("id") for r in rs]
raise SystemExit(0 if len(ids)==len(set(ids)) else 1)
' 2>/dev/null; then
          pass "$name explicitly deduplicates duplicate resource addresses"
        else
          fail "$name silently accepts duplicate resource addresses"
        fi
        ;;
      1|2|3|4|5|6|7|8|9|11|12|14|15|16|17|18|19|20)
        CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
          -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
          -F "terraform_file=@$f" \
          -F "source=aws_instance.public_server" \
          -F "target=aws_s3_bucket.sensitive_data" \
          "$API/investigations/terraform")"
        cat "$BODY_TXT" | tee -a "$LOG"

        if [ "$CODE" != "200" ] && [ "$CODE" != "201" ]; then
          fail "$name expected successful ingestion, got HTTP $CODE"
          continue
        fi

        # Minimum independently-derived structural checks.
        EXPECTED_RESOURCES=""
        case "$i" in
          01) EXPECTED_RESOURCES=1 ;;
          02) EXPECTED_RESOURCES=4 ;;
          03) EXPECTED_RESOURCES=4 ;;
          04) EXPECTED_RESOURCES=6 ;;
          05) EXPECTED_RESOURCES=5 ;;
          06) EXPECTED_RESOURCES=2 ;;
          07) EXPECTED_RESOURCES=1 ;;
          08) EXPECTED_RESOURCES=1 ;;
          09) EXPECTED_RESOURCES=2 ;;
          11) EXPECTED_RESOURCES=0 ;;
          12) EXPECTED_RESOURCES=0 ;;
          14) EXPECTED_RESOURCES=3 ;;
          15) EXPECTED_RESOURCES=4 ;;
          16) EXPECTED_RESOURCES=10 ;;
          17) EXPECTED_RESOURCES=1 ;;
          18) EXPECTED_RESOURCES=3 ;;
          19) EXPECTED_RESOURCES=2 ;;
          20) EXPECTED_RESOURCES=13 ;;
        esac

        if [ -n "$EXPECTED_RESOURCES" ]; then
          ACTUAL="$(python -c 'import json; print(len(json.load(open(__import__("os").environ["BODY_TXT"])).get("resources",[])))' 2>/dev/null || echo -1)"
          if [ "$ACTUAL" = "$EXPECTED_RESOURCES" ]; then
            pass "$name resource count=$EXPECTED_RESOURCES"
          else
            fail "$name resource count expected=$EXPECTED_RESOURCES actual=$ACTUAL"
          fi
        else
          pass "$name ingestion HTTP contract"
        fi

        # Special semantic assertions from EXPECTED_RESULTS.md.
        case "$i" in
          03)
            if grep -q 'aws_instance.app_server' "$BODY_TXT" && grep -q 'aws_iam_role.app_role' "$BODY_TXT"; then
              pass "$name contains expected relationship resources"
            else
              warn "$name could not verify relationship semantics from public response"
            fi
            ;;
          04)
            if python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
ap=d.get("attack_path_analysis") or {}
ca=d.get("candidates") or []
ok=(len(ca)>=2 and (ap.get("exists") is True or len(d.get("attack_path",[]))>0))
raise SystemExit(0 if ok else 1)
' 2>/dev/null; then
              pass "$name exposes attack-path/candidate evidence"
            else
              fail "$name expected attack-path/candidate evidence"
            fi
            ;;
          05)
            if python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
b=d.get("blast_radius_analysis") or {}
n=b.get("affected_resource_count",0)
raise SystemExit(0 if n==3 else 1)
' 2>/dev/null; then
              pass "$name blast radius affected_resource_count=3"
            else
              fail "$name blast radius expected exactly 3 affected resources"
            fi
            ;;
          06)
            if python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
ok=len(d.get("candidates",[]))>=1 or len(d.get("reasoning",{}).get("findings",[]))>=1
raise SystemExit(0 if ok else 1)
' 2>/dev/null; then
              pass "$name public bucket finding/candidate present"
            else
              fail "$name expected high-risk public bucket finding"
            fi
            ;;
          07)
            if python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
ok=len(d.get("candidates",[]))>=1
raise SystemExit(0 if ok else 1)
' 2>/dev/null; then
              pass "$name public 8080 candidate present"
            else
              fail "$name expected medium-risk candidate"
            fi
            ;;
          08|09)
            if python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
score=d.get("risk_score",0)
cand=len(d.get("candidates",[]))
raise SystemExit(0 if score <= 30 and cand == 0 else 1)
' 2>/dev/null; then
              pass "$name remains low/no-finding"
            else
              warn "$name risk/candidate fields differ from expected low-risk baseline"
            fi
            ;;
          15)
            # If the request returned, bounded execution/cycle termination is already evidenced.
            pass "$name completed without timeout/stack overflow"
            ;;
          17)
            if grep -qi 'remedi' "$BODY_TXT"; then
              pass "$name remediation evidence present"
            else
              fail "$name expected remediation evidence"
            fi
            ;;
          18)
            if grep -q 'aws_lambda_function' "$BODY_TXT" && grep -q 'aws_s3_bucket' "$BODY_TXT"; then
              pass "$name cross-resource resources present"
            else
              fail "$name expected lambda/bucket resources"
            fi
            ;;
          20)
            pass "$name completed large-environment smoke case"
            ;;
        esac
        ;;
    esac
  done
fi

# ------------------------------------------------------------
# 4. IAM — all 6 fixtures
# ------------------------------------------------------------
log ""
log "========== 4. IAM — 6 FIXTURES =========="

for name in iam_minimal.json iam_least_privilege.json iam_overprivileged.json iam_complex.json iam_empty.json iam_invalid.json; do
  f="$FIXTURES/$name"
  log ""
  log "----- IAM: $name -----"

  if [ ! -f "$f" ]; then
    fail "$name fixture missing"
    continue
  fi

  CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
    -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
    -F "policy=@$f" \
    "$API/scan/iam")"
  cat "$BODY_TXT" | tee -a "$LOG"

  case "$name" in
    iam_minimal.json|iam_least_privilege.json)
      if [ "$CODE" = "200" ] && python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
raise SystemExit(0 if d.get("findings")==0 and d.get("overall_risk_score",0)==0 else 1)
' 2>/dev/null; then
        pass "$name least-privilege baseline"
      else
        fail "$name expected 200 with zero findings"
      fi
      ;;
    iam_overprivileged.json)
      if [ "$CODE" = "200" ] && python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
raise SystemExit(0 if d.get("findings",0)>=2 and d.get("overall_risk_score",0)>=80 else 1)
' 2>/dev/null; then
        pass "$name detects severe overprivilege"
      else
        fail "$name expected >=2 findings and high risk"
      fi
      ;;
    iam_complex.json)
      if [ "$CODE" = "200" ] && python -c '
import json
d=json.load(open(__import__("os").environ["BODY_TXT"]))
raise SystemExit(0 if d.get("findings",0)>=1 else 1)
' 2>/dev/null; then
        pass "$name identifies complex-policy findings"
      else
        fail "$name expected findings"
      fi
      ;;
    iam_empty.json|iam_invalid.json)
      if [ "$CODE" -ge 400 ] && [ "$CODE" -lt 500 ]; then
        pass "$name rejects invalid/empty policy with 4xx"
      else
        fail "$name expected 4xx validation error, got HTTP $CODE"
      fi
      ;;
  esac
done

# ------------------------------------------------------------
# 5. API security boundary
# ------------------------------------------------------------
log ""
log "========== 5. API SECURITY BOUNDARY =========="

NOAUTH_CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
  -X POST \
  -F "terraform_file=@$FIXTURES/01_minimal_valid.tf" \
  -F "source=aws_instance.public_server" \
  -F "target=aws_s3_bucket.sensitive_data" \
  "$API/investigations/terraform")"
cat "$BODY_TXT" | tee -a "$LOG"
[ "$NOAUTH_CODE" = "401" ] && pass "Terraform investigation requires authentication" || fail "Terraform investigation no-auth expected 401, got $NOAUTH_CODE"

BADTOKEN_CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
  -X POST -H "Authorization: Bearer definitely-invalid-token" \
  -F "terraform_file=@$FIXTURES/01_minimal_valid.tf" \
  -F "source=aws_instance.public_server" \
  -F "target=aws_s3_bucket.sensitive_data" \
  "$API/investigations/terraform")"
cat "$BODY_TXT" | tee -a "$LOG"
[ "$BADTOKEN_CODE" = "401" ] && pass "invalid token rejected" || fail "invalid token expected 401, got $BADTOKEN_CODE"

# ------------------------------------------------------------
# 6. History / persistence / export / delete
# ------------------------------------------------------------
log ""
log "========== 6. PERSISTENCE / HISTORY / EXPORT / DELETE =========="

CREATE_CODE="$(curl -sS -o "$RESP_JSON" -w '%{http_code}' \
  -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "terraform_file=@$FIXTURES/01_minimal_valid.tf" \
  -F "source=aws_s3_bucket.minimal_bucket" \
  -F "target=aws_s3_bucket.minimal_bucket" \
  "$API/investigations/terraform")"
cat "$RESP_JSON" | tee -a "$LOG"
INV_ID="$(python -c 'import json; print(json.load(open(__import__("os").environ["RESP_JSON"])).get("id",""))' 2>/dev/null || true)"

if [ "$CREATE_CODE" = "200" ] || [ "$CREATE_CODE" = "201" ]; then
  pass "persisted investigation create"
else
  fail "persisted investigation create HTTP $CREATE_CODE"
fi

if [ -n "$INV_ID" ]; then
  READ_CODE="$(curl -sS -o "$RESP_JSON" -w '%{http_code}' \
    -H "Authorization: Bearer $ACCESS_TOKEN" "$API/investigations/$INV_ID")"
  cat "$RESP_JSON" | tee -a "$LOG"
  [ "$READ_CODE" = "200" ] && pass "investigation read-after-create" || fail "investigation read-after-create HTTP $READ_CODE"

  HIST_CODE="$(curl -sS -o "$RESP_JSON" -w '%{http_code}' \
    -H "Authorization: Bearer $ACCESS_TOKEN" "$API/investigations?size=100")"
  cat "$RESP_JSON" | tee -a "$LOG"
  if [ "$HIST_CODE" = "200" ] && grep -q "$INV_ID" "$RESP_JSON"; then
    pass "investigation appears in owner history"
  else
    fail "investigation missing from owner history"
  fi

  EXPORT_CODE="$(curl -sS -o "$RESP_JSON" -w '%{http_code}' \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    "$API/investigations/$INV_ID/export?format=json")"
  cat "$RESP_JSON" | tee -a "$LOG"
  [ "$EXPORT_CODE" = "200" ] && pass "JSON export" || fail "JSON export HTTP $EXPORT_CODE"

  DELETE_CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
    -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
    "$API/investigations/$INV_ID")"
  cat "$BODY_TXT" | tee -a "$LOG"
  if [ "$DELETE_CODE" = "204" ] || [ "$DELETE_CODE" = "200" ]; then
    pass "investigation delete"
  else
    fail "investigation delete HTTP $DELETE_CODE"
  fi

  GET_DELETED_CODE="$(curl -sS -o "$BODY_TXT" -w '%{http_code}' \
    -H "Authorization: Bearer $ACCESS_TOKEN" "$API/investigations/$INV_ID")"
  cat "$BODY_TXT" | tee -a "$LOG"
  [ "$GET_DELETED_CODE" = "404" ] && pass "deleted investigation returns 404" || fail "deleted investigation expected 404, got $GET_DELETED_CODE"
fi

# ------------------------------------------------------------
# 7. Final report
# ------------------------------------------------------------
log ""
log "============================================================"
log "FINAL RESULT"
log "============================================================"
log "PASS=$PASS"
log "FAIL=$FAIL"
log "WARN=$WARN"
log "TOTAL_ASSERTIONS=$TOTAL"
log "Evidence log: $LOG"
log ""

if [ "$FAIL" -eq 0 ]; then
  log "GATE CANDIDATE: PASS"
  log "Review WARN items and the browser/manual E2E journey before release."
  exit 0
else
  log "GATE CANDIDATE: FAIL"
  log "Do NOT release V1 until every release-blocking FAIL is resolved or explicitly waived."
  exit 1
fi
