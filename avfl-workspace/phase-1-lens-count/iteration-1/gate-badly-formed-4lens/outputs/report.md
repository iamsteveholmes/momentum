# AVFL Gate Validation Report

## Status: GATE_FAILED

**Score:** 33/100
**Grade:** Failing
**Profile:** gate
**Pipeline stage:** input validation
**Fix loop attempted:** No (gate profile does not include a fix loop)

---

## Parameters

| Parameter | Value |
|---|---|
| domain_expert | technical writer |
| task_context | API integration specification document |
| profile | gate |
| output_to_validate | `avfl-workspace/fixtures/tech-spec-badly-formed.md` |
| source_material | none |
| lenses active | structural (1 agent) |

---

## Scoring Breakdown

| Severity | Count | Weight | Subtotal |
|---|---|---|---|
| critical | 3 | −15 each | −45 |
| high | 2 | −8 each | −16 |
| medium | 2 | −3 each | −6 |
| low | 0 | −1 each | 0 |
| **Total deductions** | | | **−67** |
| **Final score** | | | **33/100** |

---

## Findings

### STRUCTURAL-001
- **Severity:** critical
- **Dimension:** cross_reference_integrity
- **Location:** `## Endpoints / ### POST /sync`
- **Description:** The document references "Section 5" for error codes and handling procedures, but no Section 5 exists. The document contains exactly four sections: Overview, Authentication, Endpoints, and Rate Limits. This cross-reference is unresolvable and points to content that is entirely absent.
- **Evidence:** "See Section 5 for error codes and handling procedures." — the document has no Section 5 by any numbering or heading; the four present sections carry no section numbers and none covers error codes.
- **Suggestion:** Add a dedicated error codes section covering HTTP status codes returned by each endpoint, error response body schema, and handling guidance. Update the reference to point to the actual section heading.

---

### STRUCTURAL-002
- **Severity:** critical
- **Dimension:** completeness
- **Location:** `## Endpoints / ### POST /sync`
- **Description:** The only documented endpoint provides a single descriptive sentence with no technical contract. An API integration spec requires, at minimum: request method and path (present), request body schema or parameters, response body schema, HTTP status codes for success and error cases, and example payloads. None of these are present.
- **Evidence:** "Initiates a data synchronization job. Returns a job ID for polling." — this is the complete content under `### POST /sync`. No request schema, response schema, status codes, or examples appear anywhere under this heading.
- **Suggestion:** Expand the endpoint section to include: request body schema (required and optional fields with types), success response schema (including the job ID field name and type), applicable HTTP status codes, and at minimum one request/response example.

---

### STRUCTURAL-003
- **Severity:** critical
- **Dimension:** completeness
- **Location:** `## Endpoints`
- **Description:** The POST /sync endpoint states it returns a job ID "for polling," implying a polling mechanism exists. No polling endpoint is documented anywhere in the specification. An integrator cannot implement the polling workflow without knowing the endpoint path, method, parameters, and response format.
- **Evidence:** "Returns a job ID for polling." — the document contains only one endpoint (`### POST /sync`). No GET endpoint for polling job status appears under `## Endpoints` or anywhere else in the document.
- **Suggestion:** Document the polling endpoint (e.g., `GET /sync/{jobId}`) including path parameters, response schema showing job status values, terminal states, and recommended polling interval or guidance.

---

### STRUCTURAL-004
- **Severity:** high
- **Dimension:** completeness
- **Location:** `## Authentication`
- **Description:** The Authentication section contains a single sentence that identifies the mechanism (Bearer token) but provides no actionable integration detail: there is no explanation of how to obtain a token, the token format, token lifetime/expiry behavior, what happens on an invalid/expired token, or an example Authorization header.
- **Evidence:** "All requests must include a Bearer token in the Authorization header." — this is the complete content of the `## Authentication` section. No further detail appears.
- **Suggestion:** Expand to cover: how to obtain a Bearer token (endpoint, credential requirements), expected token format, token lifetime and refresh behavior, the HTTP 401 response returned on authentication failure, and an example Authorization header value.

---

### STRUCTURAL-005
- **Severity:** high
- **Dimension:** completeness
- **Location:** Document level
- **Description:** The document contains no base URL, API host, or server URL. Without a base URL, an integrator cannot form any HTTP request. This is a required structural element of any integration specification.
- **Evidence:** No base URL, host, server URL, or environment URL (e.g., `https://api.example.com/v1`) appears anywhere in the document across all four sections.
- **Suggestion:** Add a base URL at the top of the document or in a dedicated Connection / Base URL section. Include environment variants (production, staging) if applicable.

---

### STRUCTURAL-006
- **Severity:** medium
- **Dimension:** completeness
- **Location:** `## Rate Limits`
- **Description:** The Rate Limits section states the standard tier limit but omits the behavior when the limit is exceeded: no HTTP status code (429), no response body for rate limit errors, no retry-after header documentation, and no retry/backoff guidance. The existence of a "Standard tier" label also implies other tiers exist but they are not documented.
- **Evidence:** "Standard tier: 100 requests/hour." — this is the complete content of the `## Rate Limits` section.
- **Suggestion:** Add: HTTP 429 response details, Retry-After header behavior, recommended backoff strategy, and documentation of any other rate limit tiers.

---

### STRUCTURAL-007
- **Severity:** medium
- **Dimension:** structural_validity
- **Location:** Document level
- **Description:** The document contains no versioning information — no API version, document version, or date. For an integration specification, API version is required structural metadata because integrators must know which API version a spec describes, and breaking changes between versions require version identification.
- **Evidence:** No version field, API version string, document revision date, or changelog appears anywhere in the document's four sections or header.
- **Suggestion:** Add API version (e.g., `v1`) to the document header or Overview section, and include a document version or last-updated date.

---

## Validation Summary

The document is structurally insufficient to serve as an integration specification. Three critical findings drive the gate failure:

1. A broken internal cross-reference (Section 5 does not exist) indicates the document is incomplete relative to its own stated content plan.
2. The only documented endpoint lacks any technical contract — no request/response schemas, no status codes, no examples.
3. A core workflow (polling) is referenced but entirely undocumented.

**Cannot proceed until these findings are resolved.**
