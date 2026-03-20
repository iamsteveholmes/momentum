# AVFL 2-Lens Validation Report

## Run Summary

| Field | Value |
|---|---|
| Status | **CLEAN** |
| Final Score | **100 / 100** |
| Iterations | **2** |
| Total Findings (consolidated) | **5** |
| Findings Fixed | **5** |
| False Positives Removed | **0** |
| Duplicates Removed | **0** |
| Profile | full |
| Active Lenses | Structural Integrity, Factual Accuracy |
| Domain Expert | technical writer |
| Task Context | API integration guide |
| Source Material | none |
| Document | avfl-workspace/fixtures/api-guide-clean.md |

---

## Score Per Iteration

| Iteration | Score | Decision |
|---|---|---|
| 1 (initial) | 89 | FAIL — 3 medium + 2 low findings → proceed to fix |
| 2 (post-fix) | 100 | PASS — CLEAN |

---

## Iteration 1 — Consolidated Findings

5 findings consolidated from 4 validators (2 lenses × 2 reviewers). All findings had MEDIUM confidence (one reviewer each). Zero false positives removed after investigation — all findings were substantiated by evidence. Zero duplicates removed (findings were distinct despite some overlap in the error response section).

### Finding Detail

---

**STRUCTURAL-ADV-001**

| Field | Value |
|---|---|
| Severity | medium |
| Dimension | completeness |
| Confidence | MEDIUM (structural adversary only) |
| Location | Error Response Format section |

Description: The error response JSON example is specific to a 429 rate-limit error (it includes `retry_after: 1823`) but is labeled as the universal error format for all errors. A 400 or 404 error would not have a meaningful `retry_after` field. The schema conflates a rate-limit-specific field with the general error structure, misleading API consumers about the shape of non-429 error responses.

Evidence: The "Error Response Format" section heading states "All errors use this structure:" followed by a single JSON example containing `"retry_after": 1823`. No note distinguishes this as a 429-specific field or marks it optional.

Fix applied: Added a generic error example (using `INVALID_DATE_RANGE`) as the primary "all errors" example. Added a separate 429-specific example with `retry_after`, explicitly labeled as applying only to rate limit errors.

---

**STRUCTURAL-002**

| Field | Value |
|---|---|
| Severity | medium |
| Dimension | cross_reference_integrity |
| Confidence | MEDIUM (structural enumerator only) |
| Location | Rate Limits section vs. Error Response Format section |

Description: The Rate Limits section states retry timing is communicated via a `Retry-After` HTTP response header. The Error Response Format section includes `retry_after` as a field in the response body. These are two different mechanisms (header vs. body field), but the guide never acknowledges that both exist or explains their relationship.

Evidence: Rate Limits: "Exceeded requests return HTTP 429 with a `Retry-After` header indicating seconds until the limit resets." Error Response Format JSON: `"retry_after": 1823` — a body field with the same semantic meaning, referenced without any connection to the header.

Fix applied: Rewrote the Rate Limits section to explicitly state: "The time until the rate limit resets is indicated both in the `Retry-After` response header (in seconds) and in the `retry_after` field of the error response body."

---

**ACCURACY-ADV-001**

| Field | Value |
|---|---|
| Severity | medium |
| Dimension | completeness |
| Confidence | MEDIUM (accuracy adversary only) |
| Location | Authentication section |

Description: The guide does not state that HTTPS is required. The HTTP example shows bare `HTTP/1.1` without specifying TLS. For an API that uses key-based authentication, transmitting the API key over unencrypted HTTP would expose credentials. The guide's silence on transport security could mislead implementers into using HTTP.

Evidence: Authentication section: "GET /v2/metrics HTTP/1.1 / Host: api.momentum.example.com / X-Momentum-Key: mk_live_abc123xyz" — no mention of HTTPS, TLS, or transport security anywhere in the guide.

Fix applied: Added to the Authentication section: "All requests must use HTTPS and include your API key in the `X-Momentum-Key` header. Sending your API key over an unencrypted HTTP connection is a security risk."

---

**STRUCTURAL-001**

| Field | Value |
|---|---|
| Severity | low |
| Dimension | completeness |
| Confidence | MEDIUM (structural enumerator only) |
| Location | GET /v2/metrics — Parameters table, `workflow` parameter |

Description: The `workflow` filter parameter description provides only "Filter by workflow name" with no indication of format, matching behavior (exact vs. partial), or example value.

Evidence: "| workflow | string | No | Filter by workflow name |" — no example, no format guidance.

Fix applied: Updated description to: "Filter by workflow name (exact match, e.g. `"avfl-2lens"`)"

---

**STRUCTURAL-ADV-002**

| Field | Value |
|---|---|
| Severity | low |
| Dimension | structural_validity |
| Confidence | MEDIUM (structural adversary only) |
| Location | Rate Limits section |

Description: "All tiers: 100 requests/hour" implies multiple service tiers exist but provides only a single rate limit value, creating ambiguity about whether tiers are differentiated elsewhere in the product.

Evidence: "All tiers: 100 requests/hour." — The phrase "all tiers" implies multiple tiers exist, but no tier differentiation is described anywhere in the guide.

Fix applied: Rewritten as "Rate limit: 100 requests/hour." removing the ambiguous multi-tier implication.

---

## Iteration 2 — Post-Fix Validation

All 4 validators (Structural Enumerator, Structural Adversary, Accuracy Enumerator, Accuracy Adversary) returned NO FINDINGS against the fixed document.

Score: 100 / 100. Status: CLEAN.

---

## False Positives Removed

**0 false positives removed.**

All 5 MEDIUM-confidence findings were substantiated by concrete textual evidence upon consolidator investigation. No findings were discarded.

---

## Final Status

**CLEAN — 100/100 after 2 iterations.**

The API integration guide passed full 2-lens validation (Structural Integrity + Factual Accuracy) after one fix pass. Five issues were identified and resolved: three medium-severity (missing HTTPS requirement, ambiguous error response schema, unexplained Retry-After header/body duality) and two low-severity (underspecified workflow parameter, ambiguous tier language in rate limits). The fixed document is production-ready under the 2-lens configuration.
