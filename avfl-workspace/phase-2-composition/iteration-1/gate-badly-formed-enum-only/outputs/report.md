# AVFL Validation Report

**Variant:** avfl-3lens-enum-only
**Profile:** gate
**Domain Expert:** technical writer
**Task Context:** API integration specification document
**Source Material:** none
**Fixture:** tech-spec-badly-formed.md
**Date:** 2026-03-20

---

## Result

**Status:** GATE_FAILED
**Score:** 48 / 100
**Grade:** Failing — major rework needed
**Fix Loop Attempted:** no (gate profile does not fix)

---

## Score Breakdown

| Severity | Count | Points Each | Subtotal |
|---|---|---|---|
| critical | 2 | -15 | -30 |
| high | 2 | -8 | -16 |
| medium | 2 | -3 | -6 |
| low | 0 | -1 | 0 |
| **Total deducted** | | | **-52** |

Starting score 100 − 52 = **48**

---

## Findings

### STRUCTURAL-001

- **Severity:** critical
- **Dimension:** cross_reference_integrity
- **Location:** `POST /sync` section
- **Description:** The document contains a cross-reference to "Section 5" that does not exist. The document has four sections (Overview, Authentication, Endpoints, Rate Limits) and no Section 5 is present anywhere.
- **Evidence:** `"See Section 5 for error codes and handling procedures."` — no Section 5 exists in the document.
- **Suggestion:** Either add the missing Section 5 (Error Codes and Handling) or remove the dangling reference and document error handling inline within the endpoint.
- **Confidence:** MEDIUM (single Enumerator, no dual-review)

---

### STRUCTURAL-002

- **Severity:** critical
- **Dimension:** completeness
- **Location:** Document-level (entire document)
- **Description:** Error codes and handling documentation is entirely absent from the document. This is mandatory content for an API integration specification — integrators cannot handle API errors without it. The only mention of error handling is the dangling reference to the nonexistent Section 5.
- **Evidence:** The complete document contains no error code table, no HTTP error status documentation, no error response schema, and no error handling procedures. The sole reference is: `"See Section 5 for error codes and handling procedures."` which resolves to nothing.
- **Suggestion:** Add an Error Codes section documenting all expected HTTP status codes, error response body schema, and handling guidance for each error condition.
- **Confidence:** MEDIUM (single Enumerator, no dual-review)

---

### STRUCTURAL-003

- **Severity:** high
- **Dimension:** completeness
- **Location:** `POST /sync` section
- **Description:** The only documented endpoint is missing its request body schema and response schema. A one-sentence prose description is not sufficient specification for integration. No field names, types, required/optional designations, or format examples are provided.
- **Evidence:** Entire endpoint documentation reads: `"Initiates a data synchronization job. Returns a job ID for polling."` — no request parameters, no request body fields, no response body fields, no types.
- **Suggestion:** Document request body schema (field names, types, required/optional, constraints) and response schema (fields, types, example) for `POST /sync`.
- **Confidence:** MEDIUM (single Enumerator, no dual-review)

---

### STRUCTURAL-004

- **Severity:** high
- **Dimension:** completeness
- **Location:** `Endpoints` section
- **Description:** The spec states that `POST /sync` returns a job ID "for polling," implying a polling endpoint exists. That polling endpoint is never documented. An integrator cannot use the API without knowing how to poll for job status.
- **Evidence:** `"Returns a job ID for polling."` — no GET endpoint for job status retrieval is documented anywhere in the Endpoints section or elsewhere in the document.
- **Suggestion:** Add documentation for the polling endpoint (e.g., `GET /sync/{jobId}` or equivalent), including its path, response schema, and terminal job states.
- **Confidence:** MEDIUM (single Enumerator, no dual-review)

---

### STRUCTURAL-005

- **Severity:** medium
- **Dimension:** completeness
- **Location:** `Authentication` section
- **Description:** The authentication section provides only a single sentence with insufficient detail for integration. Token acquisition, token expiry/refresh, and a concrete header format example are all absent.
- **Evidence:** Complete authentication section text: `"All requests must include a Bearer token in the Authorization header."` — no token acquisition path, no expiry duration, no refresh procedure, no header format example (e.g., `Authorization: Bearer <token>`).
- **Suggestion:** Expand to include: how to obtain a Bearer token, token lifetime and refresh behavior, and a concrete header format example.
- **Confidence:** MEDIUM (single Enumerator, no dual-review)

---

### STRUCTURAL-006

- **Severity:** medium
- **Dimension:** completeness
- **Location:** `Rate Limits` section
- **Description:** Rate limits documentation omits the HTTP response behavior when a limit is exceeded, retry guidance, and any information about burst limits or multiple tiers beyond "Standard tier."
- **Evidence:** Complete rate limits section text: `"Standard tier: 100 requests/hour."` — no HTTP 429 status documentation, no `Retry-After` header guidance, no burst limit, no behavior on exceeded limit.
- **Suggestion:** Add: HTTP status code returned on rate limit exceeded (typically 429), `Retry-After` header behavior if applicable, burst limit if any, and guidance on retry strategy.
- **Confidence:** MEDIUM (single Enumerator, no dual-review)

---

## Pipeline Summary

| Phase | Result |
|---|---|
| Validate | 1 agent (Enumerator), Structural Integrity lens — 6 findings |
| Consolidate | No duplicates removed. No findings discarded (all have evidence). Score: 48/100 |
| Evaluate | GATE_FAILED (48 < 95 threshold) |
| Fix Loop | Not attempted (gate profile: no fix loop) |

---

## Lens Coverage

| Lens | Status | Active |
|---|---|---|
| Structural Integrity | Executed (gate profile) | yes |
| Factual Accuracy | Not run (gate profile — structural only) | no |
| Coherence & Craft | Not run (gate profile — structural only) | no |
| Domain Fitness | Inactive in this variant | no |

---

## Reviewer Composition

| Role | Count | Confidence Tagging |
|---|---|---|
| Enumerator | 1 | MEDIUM (no dual-review) |
| Adversary | 0 | not active in this variant |

---

## Interpretation

The document fails the structural gate comprehensively. Two critical issues — a dangling cross-reference to a nonexistent section and the complete absence of error handling documentation — alone would be sufficient to fail the gate. Four additional findings (two high, two medium) indicate the document is substantially incomplete as an API integration specification. The document is a skeletal outline, not a usable specification.

The gate halt is appropriate. This document should not advance through the pipeline until missing sections are written and the broken cross-reference is resolved.
