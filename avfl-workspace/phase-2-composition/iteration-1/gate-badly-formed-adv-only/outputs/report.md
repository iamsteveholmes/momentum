# AVFL Validation Report

**Variant:** avfl-3lens-adv-only
**Profile:** gate
**Lens:** Structural Integrity (Adversary framing)
**Domain Expert:** technical writer
**Task Context:** API integration specification document
**Source Material:** none
**Fix Loop Attempted:** no

---

## Status: GATE_FAILED

**Score:** 28/100
**Threshold:** 95
**Grade:** Failing — major rework needed

Structural validation failed. The document cannot proceed in a pipeline until these issues are resolved.

---

## Findings Summary

| Severity | Count |
|---|---|
| critical | 3 |
| high | 3 |
| medium | 1 |
| low | 0 |
| **total** | **7** |

---

## Findings

### STRUCTURAL-001
- **Severity:** critical
- **Dimension:** cross_reference_integrity
- **Location:** Endpoints section — POST /sync description
- **Description:** The document contains a dangling reference to a section that does not exist. "See Section 5 for error codes and handling procedures." The document has exactly four sections: Overview, Authentication, Endpoints, Rate Limits. There is no Section 5.
- **Evidence:** "See Section 5 for error codes and handling procedures." — The document ends at Rate Limits with no Section 5 present.
- **Suggestion:** Either add Section 5 (Error Codes and Handling) with full error code definitions and handling procedures, or remove the reference and include the error documentation inline with the endpoint.

---

### STRUCTURAL-002
- **Severity:** critical
- **Dimension:** completeness
- **Location:** Endpoints section — POST /sync
- **Description:** The POST /sync endpoint entry is missing all contract-defining content required for an integration specification: request body schema (required fields, types, constraints), response schema (shape of the returned job ID object, types), and HTTP status codes (success and error cases). An API integration spec without request/response contracts is not implementable.
- **Evidence:** The entire POST /sync entry reads: "Initiates a data synchronization job. Returns a job ID for polling. See Section 5 for error codes and handling procedures." No parameters, no request body, no response body, no status codes are documented.
- **Suggestion:** Document at minimum: request body (required/optional fields with types and constraints), success response (200/202 shape with job ID field type), and error response codes with meanings.

---

### STRUCTURAL-003
- **Severity:** critical
- **Dimension:** structural_validity
- **Location:** Entire document
- **Description:** No base URL is defined anywhere in the document. An integration specification must tell the integrator where to send requests. Without a base URL, the endpoint listing (POST /sync) cannot be used — the integrator has no host to call.
- **Evidence:** The document contains no URL, hostname, environment specification, or base path anywhere in its 18 lines.
- **Suggestion:** Add a Base URL or Environments section specifying at minimum the production endpoint (e.g., `https://api.datasync.example.com/v1`), and ideally staging/sandbox environments as well.

---

### STRUCTURAL-004
- **Severity:** high
- **Dimension:** completeness
- **Location:** Authentication section
- **Description:** The authentication section states only that a Bearer token must be included in the Authorization header. It provides no information about how to obtain the token, the token format or length, token expiry, refresh behavior, or permission scopes. This is insufficient for an integrator to implement authentication.
- **Evidence:** "All requests must include a Bearer token in the Authorization header." — The section ends here. No token acquisition flow, no token format, no expiry, no scopes.
- **Suggestion:** Add token acquisition instructions (e.g., OAuth2 client credentials flow, API key issuance), token lifetime and refresh guidance, and any required permission scopes for the documented endpoints.

---

### STRUCTURAL-005
- **Severity:** high
- **Dimension:** completeness
- **Location:** Rate Limits section
- **Description:** Only the "Standard tier" is documented (100 requests/hour). The use of "Standard tier" implies other tiers exist, but they are not specified. Additionally, no burst limit, retry-after behavior, or rate limit response headers are documented — all of which are required for correct integration.
- **Evidence:** "Standard tier: 100 requests/hour." — This is the entirety of the Rate Limits section. No other tiers, no burst limits, no HTTP header behavior, no 429 response guidance.
- **Suggestion:** Document all tiers, burst limits, the 429 response format, the Retry-After header behavior, and guidance on how integrators should handle rate limit errors.

---

### STRUCTURAL-006
- **Severity:** high
- **Dimension:** structural_validity
- **Location:** Entire document
- **Description:** No API version is specified anywhere. Integration specifications must identify the API version to which the documented contract applies. Without versioning, integrators cannot determine whether the spec is current, cannot manage upgrades, and cannot handle breaking changes.
- **Evidence:** No version number, version header, URL path version segment, or versioning policy appears anywhere in the document.
- **Suggestion:** Add explicit API version (e.g., "v1" in the base URL or a dedicated Versioning section), and document the versioning policy (e.g., breaking changes increment the major version).

---

### STRUCTURAL-007
- **Severity:** medium
- **Dimension:** completeness
- **Location:** Endpoints section
- **Description:** Only one endpoint (POST /sync) is documented. The endpoint description states it "returns a job ID for polling," which implies a polling endpoint exists to check job status — but no such endpoint is documented. A DataSync API integration spec with a single endpoint and an unreferenced polling mechanism is almost certainly incomplete.
- **Evidence:** "Returns a job ID for polling." — No GET /sync/{jobId} or equivalent status endpoint appears in the Endpoints section.
- **Suggestion:** Document the polling/status endpoint (e.g., GET /jobs/{jobId}) with its response schema, status field values (pending, running, complete, failed), and any other endpoints that comprise the complete API surface.

---

## Scoring Calculation

| Finding | Severity | Points |
|---|---|---|
| STRUCTURAL-001 | critical | -15 |
| STRUCTURAL-002 | critical | -15 |
| STRUCTURAL-003 | critical | -15 |
| STRUCTURAL-004 | high | -8 |
| STRUCTURAL-005 | high | -8 |
| STRUCTURAL-006 | high | -8 |
| STRUCTURAL-007 | medium | -3 |
| **Final Score** | | **28/100** |

Starting score: 100. Deductions: -72. Final: 28.

---

## Pipeline Decision

**GATE_FAILED.** Score 28 is below the gate threshold of 95. The document is structurally unusable as an API integration specification: three critical deficiencies (broken cross-reference, absent endpoint contracts, missing base URL) make it impossible for an integrator to implement against this spec. No fix loop was attempted (gate profile does not permit fix attempts). The document must be substantially rewritten before re-entry into the pipeline.
