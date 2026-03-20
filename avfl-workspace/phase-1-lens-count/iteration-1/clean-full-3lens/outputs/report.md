# AVFL Validation Report — API Integration Guide

## Run Metadata
- **Skill:** avfl-3lens (3-lens benchmark variant)
- **Profile:** full
- **Domain expert:** technical writer
- **Task context:** API integration guide
- **Document:** `/Users/steve/projects/momentum/avfl-workspace/fixtures/api-guide-clean.md`
- **Source material:** none
- **Date:** 2026-03-20

---

## Final Status: CLEAN

| Metric | Value |
|--------|-------|
| Final status | CLEAN |
| Final score | 97/100 |
| Iterations | 2 |
| Total findings (iteration 1) | 7 |
| Findings fixed | 7 |
| Findings remaining | 3 (all low — did not trigger another fix loop; score ≥ 95) |
| False positives removed | 0 |
| Duplicates removed | 2 (1 per iteration) |

---

## Score Per Iteration

| Iteration | Score | Status |
|-----------|-------|--------|
| 1 | 83/100 | FAIL — proceed to fix |
| 2 | 97/100 | CLEAN — exit |

---

## Iteration 1: Findings Detail

7 findings after consolidation, 1 duplicate removed (STRUCTURAL-004 merged into COHERENCE-002).

| ID | Severity | Lens | Dimension | Location | Description | Evidence | Confidence |
|----|----------|------|-----------|----------|-------------|----------|------------|
| STRUCTURAL-001 | medium | structural | completeness | GET /v2/validations/{id} — Errors table | The 429 rate limit error is absent from this endpoint's error table, even though Rate Limits states the limit applies globally | Endpoint error table lists only 401 and 404. GET /v2/metrics includes 429. Rate Limits: "All tiers: 100 requests/hour" — no endpoint exclusion. | MEDIUM |
| STRUCTURAL-002 | medium | structural | completeness | Both endpoint Response sections | Response field descriptions absent — only raw JSON examples provided; no documentation of what each response field means | `"clean_rate": 0.84` appears with no description. `"duration_ms": 14200` has no description. Neither endpoint has a field description table. | MEDIUM |
| STRUCTURAL-003 | medium | structural | completeness | Error Response Format + endpoint error tables | Machine-readable error code strings (the `error.code` field) documented only by example for RATE_LIMIT_EXCEEDED; developers cannot know code strings for 401, 404, or 400 responses | Error Response Format shows `"code": "RATE_LIMIT_EXCEEDED"` but endpoint error tables provide only HTTP status codes and plain text meanings. No code strings for AUTH_INVALID, NOT_FOUND, INVALID_DATE_RANGE, etc. | MEDIUM |
| ACCURACY-001 | medium | accuracy | logical_soundness | Rate Limits section | The phrase "All tiers" implies multiple service tiers exist but provides no information distinguishing them; a developer on a paid tier would reasonably expect higher limits | "All tiers: 100 requests/hour." — "tiers" implies differentiation; stating all tiers share one limit without defining what tiers exist creates a logical gap. | MEDIUM |
| COHERENCE-002 | medium | coherence | consistency | Error Response Format section | The generic error format example includes a `retry_after` field, implying it is present in all error responses; it is semantically applicable only to 429 rate limit errors | Error Response Format JSON: `{ "error": { "code": "...", "message": "...", "retry_after": 1823 } }` — the template implies `retry_after` is a standard field on all error objects. | MEDIUM |
| COHERENCE-001 | low | coherence | clarity | GET /v2/metrics — Response (200 OK) | `clean_rate` field value `0.84` is undocumented — unclear whether this is a proportion (0.0–1.0) or a percentage (0–100) | `"clean_rate": 0.84` appears with no field description. A value of 0.84 is ambiguous without knowing the scale. | MEDIUM |
| COHERENCE-003 | low | coherence | clarity | Authentication section | Authentication request example shows only GET /v2/metrics, which could imply the header is scoped to that endpoint rather than all requests | "All requests must include your API key in the `X-Momentum-Key` header" is clear prose, but the code example beneath it shows only one of two documented endpoints. | MEDIUM |

**Score breakdown:** 100 − 3(med) − 3(med) − 3(med) − 3(med) − 3(med) − 1(low) − 1(low) = **83**

**Fixes applied (technical writer, iteration 1):**
- STRUCTURAL-001: Added 429/RATE_LIMIT_EXCEEDED to GET /v2/validations/{id} error table.
- STRUCTURAL-002: Added response field description tables to both endpoints.
- STRUCTURAL-003: Added `error.code` column to all endpoint error tables with code strings (INVALID_DATE_RANGE, AUTH_INVALID, RATE_LIMIT_EXCEEDED, NOT_FOUND).
- ACCURACY-001: Replaced "All tiers: 100 requests/hour" with "100 requests per hour" — removed misleading tier language.
- COHERENCE-002: Added clarification note to Error Response Format section; added a second example showing a non-429 error without the `retry_after` field.
- COHERENCE-001: Documented `clean_rate` as "number (0.0–1.0), proportion of validation runs that achieved a clean score (≥95)" in new response field table.
- COHERENCE-003: Strengthened authentication section prose to "All requests to all endpoints must include your API key..."

---

## Iteration 2: Findings Detail

3 findings after consolidation (1 duplicate removed — COHERENCE-I2-001 merged into STRUCTURAL-I2-001).

| ID | Severity | Lens | Dimension | Location | Description | Evidence | Confidence |
|----|----------|------|-----------|----------|-------------|----------|------------|
| STRUCTURAL-I2-001 | low | structural | completeness | GET /v2/validations/{id} — Response fields: status | The `status` field description gives only partial enumeration via "e.g., CLEAN, MAX_ITERATIONS_REACHED" — developers cannot write exhaustive case handling without the complete list | `"status": "string — Final status of the validation run (e.g., CLEAN, MAX_ITERATIONS_REACHED)"` — "e.g." explicitly signals partial list. | HIGH (both Structural-Enumerator and Coherence-Adversary found it) |
| STRUCTURAL-I2-002 | low | structural | completeness | GET /v2/metrics — Error table | Error table implies a single error.code per HTTP status code without stating whether this is exhaustive; APIs often have multiple error codes per HTTP status | `| 400 | INVALID_DATE_RANGE | Invalid date range |` — single code listed for 400, no exhaustiveness indicator. | MEDIUM |
| ACCURACY-I2-001 | low | accuracy | consistency | Error Response Format — NOT_FOUND example vs. /v2/validations/{id} error table | NOT_FOUND error message in JSON example has trailing period; the same meaning in the endpoint error table does not | Error table: `Validation run not found` (no period). Error example: `"message": "Validation run not found."` (with period). | MEDIUM |

**Score breakdown:** 100 − 1(low) − 1(low) − 1(low) = **97**

Score ≥ 95. **Exit condition: CLEAN.**

These 3 remaining low-severity findings were not fixed (score already at 97; further iteration not required). They are documented for optional follow-up.

---

## False Positives Removed

**Total false positives removed across all iterations: 0**

No findings were discarded for lack of evidence or reviewer hallucination. All MEDIUM-confidence findings were investigated against the document and retained with supporting evidence.

**Duplicates removed:**
- Iteration 1: STRUCTURAL-004 (structural/validity — Retry-After header vs. retry_after body ambiguity) merged into COHERENCE-002 (consistency — retry_after implied always-present in generic error format). COHERENCE-002 was more specific and actionable.
- Iteration 2: COHERENCE-I2-001 (coherence/completeness — status field incomplete enumeration) merged into STRUCTURAL-I2-001 (same finding, structural framing). STRUCTURAL-I2-001 elevated to HIGH confidence due to agreement across two reviewers.

---

## Summary

The input document (`api-guide-clean.md`) was a well-structured but incomplete API integration guide. Its primary weaknesses were:

1. Missing error coverage for rate limiting on one endpoint
2. Absent response field documentation (raw JSON only, no field descriptions)
3. Undocumented machine-readable error code strings
4. Misleading "All tiers" rate limit phrasing
5. Ambiguous generic error format implying `retry_after` is always present

All 5 medium-severity issues were resolved in iteration 1. The fixed document passed iteration 2 with a score of 97/100. Three low-severity issues remain (status value enumeration incomplete, 400 error code exhaustiveness unstated, minor punctuation inconsistency in error message example) but do not affect the CLEAN determination.
