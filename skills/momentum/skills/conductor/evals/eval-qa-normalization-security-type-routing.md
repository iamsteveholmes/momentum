# Eval: QA Normalization — security-auth-isolation Stakes Routes to type: security

## Given

The Conductor's stage-2 pipeline has received a qa-reviewer report for story `implement-role-permissions` containing two findings with different stakes classes:

```
### Findings

- **AC:** AC-2
  **Verdict:** MISSING
  **stakes_class:** security-auth-isolation
  **Location:** src/permissions/rbac.kt:30
  **Summary:** Admin-only endpoint accessible to regular users
  **Detail:** AC-2 requires role-based access control on /api/admin/*. No authorization check exists. Expected: 403 for non-admin roles.
  **Evidence:** curl -H "Authorization: Bearer user_token" /api/admin/users → HTTP 200 (should be 403)

- **AC:** AC-4
  **Verdict:** BLOCKED
  **stakes_class:** high-blast-radius-architecture
  **Location:** unspecified
  **Summary:** Permission schema migration not applied
  **Detail:** AC-4 requires the permissions table to exist. The migration file is present but was not run. Expected: permissions table in schema.
  **Evidence:** psql -c "\dt permissions" → "Did not find any relation"
```

## The Conductor Should

Produce two canonical finding records where the `type` field is assigned deterministically from `stakes_class`:

1. **AC-2 finding:** `type: security` because `stakes_class` is `security-auth-isolation`. Severity is `major` (from verdict MISSING, independent of stakes_class).

2. **AC-4 finding:** `type: spec-compliance` because `stakes_class` is `high-blast-radius-architecture` (not `security-auth-isolation`). Severity is `critical` (from verdict BLOCKED, independent of stakes_class).

The type assignment rule is: `security` if and only if `stakes_class == security-auth-isolation`; all other stakes classes (including `high-blast-radius-architecture`, `irreversible-destructive`, and `routine`) produce `type: spec-compliance`. This is total and deterministic — no prose inference is needed for `type` on qa-reviewer findings.
