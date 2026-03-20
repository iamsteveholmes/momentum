# AVFL Gate Validation Report

## Summary

| Field | Value |
|---|---|
| Status | **GATE_FAILED** |
| Score | **51 / 100** |
| Grade | Poor — significant problems |
| Profile | gate |
| Lens Active | Structural Integrity (structural_validity, completeness, cross_reference_integrity) |
| Agents | 1 (gate profile — single agent, no dual review) |
| Fix Loop Attempted | No — gate profile does not trigger a fix loop |
| Document | `avfl-workspace/fixtures/tech-spec-badly-formed.md` |
| Task Context | API integration specification document |
| Domain Expert | Technical writer |
| Source Material | None provided |

---

## Score Calculation

| Step | Adjustment | Running Score |
|---|---|---|
| Starting score | — | 100 |
| STRUCTURAL-001 (critical) | -15 | 85 |
| STRUCTURAL-002 (critical) | -15 | 70 |
| STRUCTURAL-003 (high) | -8 | 62 |
| STRUCTURAL-004 (high) | -8 | 54 |
| STRUCTURAL-005 (medium) | -3 | 51 |
| **Final score** | | **51** |

Pass threshold: 95. Score 51 < 95 → **GATE_FAILED**.

---

## Findings

### STRUCTURAL-001
- **Severity:** critical
- **Dimension:** cross_reference_integrity
- **Location:** Section "Endpoints" → POST /sync description
- **Description:** The POST /sync endpoint description references "Section 5" for error codes and handling procedures, but Section 5 does not exist anywhere in the document. This is a dangling cross-reference pointing to non-existent content.
- **Evidence:** "See Section 5 for error codes and handling procedures." — the document contains only four sections (Overview, Authentication, Endpoints, Rate Limits) and no Section 5.
- **Suggestion:** Either add Section 5 with error codes and handling content, or replace the reference with inline error information or a correctly numbered section reference.

---

### STRUCTURAL-002
- **Severity:** critical
- **Dimension:** completeness
- **Location:** Section "Endpoints"
- **Description:** The spec documents only one endpoint (POST /sync) and states it "returns a job ID for polling," but no polling endpoint is documented. An integration spec for an async API must document how the client retrieves job status. Without the polling endpoint, the spec is non-functional — an implementer cannot complete the integration.
- **Evidence:** "Initiates a data synchronization job. Returns a job ID for polling." — no corresponding GET or status endpoint appears anywhere in the document.
- **Suggestion:** Document the job status/polling endpoint (e.g., GET /sync/{job_id}) with its request parameters, response schema, and terminal states.

---

### STRUCTURAL-003
- **Severity:** high
- **Dimension:** structural_validity
- **Location:** Section "Endpoints" → POST /sync
- **Description:** The POST /sync endpoint entry is missing all required structural elements for an API endpoint specification: request body schema (fields, types, required/optional), response schema (fields, types), HTTP status codes, and error codes. The entry contains only a one-sentence description, which does not meet the minimum structural requirements for an API integration spec.
- **Evidence:** The entire POST /sync documentation consists of: "Initiates a data synchronization job. Returns a job ID for polling." No schema, no status codes, no parameters are present.
- **Suggestion:** Add request body schema (with field names, types, and required flags), response schema (including the job_id field type and format), successful status code (e.g., 202 Accepted), and any endpoint-specific error codes.

---

### STRUCTURAL-004
- **Severity:** high
- **Dimension:** completeness
- **Location:** Section "Authentication"
- **Description:** The Authentication section states that requests must include a Bearer token in the Authorization header but does not document how to obtain the token, the token format or structure, token expiry duration, or how to refresh an expired token. These are required elements of an authentication section in any API integration specification.
- **Evidence:** "All requests must include a Bearer token in the Authorization header." — this is the entire authentication section. No token acquisition, expiry, or refresh information is present.
- **Suggestion:** Add: (1) how to obtain credentials/token (e.g., OAuth flow, API key exchange endpoint), (2) token format or any required claims, (3) token lifetime/expiry, (4) refresh procedure or re-authentication instructions.

---

### STRUCTURAL-005
- **Severity:** medium
- **Dimension:** completeness
- **Location:** Section "Rate Limits"
- **Description:** The Rate Limits section mentions only the "Standard tier" at 100 requests/hour, but does not document: what HTTP response is returned when the limit is exceeded (e.g., 429 Too Many Requests), the Retry-After header behavior, any other tiers, or burst/concurrency limits. An integration spec must include enough information for implementers to handle rate-limit responses.
- **Evidence:** "Standard tier: 100 requests/hour." — this is the complete rate limits section. No response code, retry guidance, or additional tier information is present.
- **Suggestion:** Add the HTTP status code returned on limit violation, Retry-After header details, any other tiers (enterprise, free), and recommended backoff/retry strategy.

---

## Findings Summary

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 2 |
| Medium | 1 |
| Low | 0 |
| **Total** | **5** |

---

## Pipeline Execution Notes

- **Profile:** gate — 1 agent, structural lens only, no dual review, no fix loop.
- **Fix loop attempted:** No. Gate profile halts on failure and reports. Fix loop is not triggered regardless of score.
- **Dual review:** Not applicable (gate profile disables dual review; single agent used).
- **Source material:** None provided. Cross-reference findings were derived from internal document analysis only.
- **Verdict:** GATE_FAILED. The document must be corrected before it can proceed through the pipeline. Minimum required fixes: resolve the dangling Section 5 reference (STRUCTURAL-001) and document the polling endpoint (STRUCTURAL-002).
