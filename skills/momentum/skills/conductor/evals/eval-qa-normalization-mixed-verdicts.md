# Eval: QA Normalization — Mixed Verdicts Map to Complete Canonical Records

## Given

The Conductor's stage-2 pipeline has received a qa-reviewer report for story `fix-auth-token-refresh` containing three findings:

```
### Findings

- **AC:** AC-1
  **Verdict:** BLOCKED
  **stakes_class:** routine
  **Location:** src/auth/token.kt:42
  **Summary:** Token refresh endpoint unreachable — test environment has no auth service running
  **Detail:** The refresh endpoint could not be exercised because the auth service did not start. Expected: graceful 401 with error body when refresh token is expired.
  **Evidence:** docker-compose up auth-service → connection refused on port 8080; test execution aborted before first request

- **AC:** AC-3
  **Verdict:** MISSING
  **stakes_class:** security-auth-isolation
  **Location:** src/auth/session.kt:88
  **Summary:** Session invalidation not implemented
  **Detail:** AC-3 requires that expired sessions are invalidated server-side. No invalidation logic exists. Expected: session store deletes expired entries on refresh.
  **Evidence:** grep -r "invalidate" src/auth/ returns no matches

- **AC:** AC-5
  **Verdict:** PARTIAL
  **stakes_class:** routine
  **Location:** src/auth/login.kt:15
  **Summary:** Login rate limiting uses wrong window
  **Detail:** Rate limit window is 60s but AC-5 specifies 300s. The feature exists but the parameter is wrong.
  **Evidence:** RateLimiter(windowMs = 60000) in login.kt:15; AC-5 says "5-minute window"
```

## The Conductor Should

Apply the stage-2 normalization action and produce three canonical finding records with every base field populated:

1. **BLOCKED finding (AC-1):** `severity: critical`, `type: spec-compliance`, `source: "qa-reviewer"`, `story_slug: "fix-auth-token-refresh"`, `legitimate: true`, `suggested_fix: null`, `verdict: "BLOCKED"`, `stakes_class: "routine"`, `ac_id: "AC-1"`, plus location/summary/detail/evidence carried through from the producer.

2. **MISSING finding (AC-3):** `severity: major`, `type: security` (because `stakes_class` is `security-auth-isolation`), `source: "qa-reviewer"`, `story_slug: "fix-auth-token-refresh"`, `legitimate: true`, `suggested_fix: null`, `verdict: "MISSING"`, `stakes_class: "security-auth-isolation"`, `ac_id: "AC-3"`, plus location/summary/detail/evidence carried through.

3. **PARTIAL finding (AC-5):** `severity: minor`, `type: spec-compliance`, `source: "qa-reviewer"`, `story_slug: "fix-auth-token-refresh"`, `legitimate: true`, `suggested_fix: null`, `verdict: "PARTIAL"`, `stakes_class: "routine"`, `ac_id: "AC-5"`, plus location/summary/detail/evidence carried through.

No base field on any record is left blank, null (except `suggested_fix`), or deferred to inference. Fixer-assigned fields (`disposition`, `dismissal_rationale`, `timing_tier`) are intentionally absent — normalization does not set them. The severity mapping is deterministic from the verdict alone and does not consult `stakes_class`. The `type` field is `security` only for the finding whose `stakes_class` is `security-auth-isolation`; the other two are `spec-compliance`.
