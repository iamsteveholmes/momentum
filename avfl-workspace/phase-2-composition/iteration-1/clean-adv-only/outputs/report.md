# AVFL Validation Report
## Variant: avfl-3lens-adv-only (Phase 2 Thoroughness Benchmark)

---

## Run Parameters

| Parameter | Value |
|---|---|
| domain_expert | technical writer |
| task_context | API developer guide for the Momentum Analytics API |
| profile | full |
| output_to_validate | `avfl-workspace/fixtures/api-guide-clean.md` |
| source_material | none |
| reviewer_composition | 3 Adversary agents (1 per lens, no Enumerator, no dual-review cross-check) |
| max_iterations | 4 |
| pass_threshold | 95 |

---

## Final Status

**CLEAN**

Output passed validation with score **99/100** after **2 iterations**.

---

## Score Per Iteration

| Iteration | Score | Result | Action |
|---|---|---|---|
| 1 (initial validation) | 67 | FAIL | proceed to fix |
| 2 (post-fix re-validation) | 99 | CLEAN | exit |

---

## Pipeline Summary

### Phase-by-Phase Overview

**Iteration 1 — Phase 1 (Validate):**
Three Adversary reviewers launched in parallel — one per active lens (Structural Integrity, Factual Accuracy, Coherence & Craft). Adversary framing: read holistically and skeptically, follow hunches, verify with evidence before reporting. All confidence values default to MEDIUM (no dual-review cross-check).

Raw output: 11 candidate findings across 3 lenses before consolidation.

**Iteration 1 — Phase 2 (Consolidate):**
Merged all 11 findings. Deduplication: STRUCTURAL-001 and ACCURACY-003 addressed the same "All tiers" phrasing — merged into a single finding (ACCURACY-003, logical_soundness framing kept as the stronger frame). Evidence verification: ACCURACY-001 (mk_live_ prefix implies test keys) was discarded — the claim could not be confirmed without source material, per conservative flagging rules. Final consolidated list: 9 findings (2 high, 5 medium, 2 low). Score: 100 − 16 − 15 − 2 = **67**.

**Iteration 1 — Phase 3 (Evaluate):**
67 < 95. Iteration 1 < 4. Decision: proceed to fix.

**Iteration 1 — Phase 4 (Fix):**
Technical writer applied fixes in severity order. All 9 findings resolved. Fixed document produced.

**Iteration 2 — Phase 1 (Validate):**
Three Adversary reviewers re-ran against the fixed document. One new low-severity finding identified (COHERENCE-005: `avg_score` response field description lacks range specification, while sibling field `clean_rate` explicitly documents its range).

**Iteration 2 — Phase 2 (Consolidate):**
Single finding: COHERENCE-005, low severity. Score: 100 − 1 = **99**.

**Iteration 2 — Phase 3 (Evaluate):**
99 ≥ 95. Decision: **CLEAN — exit**.

---

## All Findings — Iteration 1

All findings carry **MEDIUM** confidence (Adversary-only configuration, no dual-review cross-check).

---

### High Severity

---

**STRUCTURAL-004**
- **Severity:** high
- **Dimension:** structural_validity
- **Location:** Authentication section — HTTP code example
- **Description:** The base URL in the authentication example uses `api.momentum.example.com`. Per RFC 2606, `.example.com` is a reserved documentation domain — it is not a real hostname. No production base URL is defined anywhere in the document. Developers cannot make a real API call from this guide.
- **Evidence:** Authentication section, HTTP code example: `Host: api.momentum.example.com` — `.example.com` is explicitly reserved for use in documentation examples and does not resolve to a real server.
- **Suggestion:** Define the production base URL explicitly (e.g., "Base URL: `https://api.momentum.io`") in the Authentication section or as a prerequisite. If the example domain must remain, add a callout noting it is illustrative and directing developers to their account dashboard for the actual URL.
- **Fix applied:** Added a "Base URL" block in the Authentication section with a note to replace the example domain with the hostname from the account dashboard.

---

**ACCURACY-002**
- **Severity:** high
- **Dimension:** correctness
- **Location:** Authentication section; Prerequisites section
- **Description:** The guide instructs developers to include the API key in the `X-Momentum-Key` header but makes no requirement to use HTTPS. Transmitting API keys over unencrypted HTTP is a security vulnerability; all production API documentation requires HTTPS. The absence of this statement could mislead developers into making plaintext API calls.
- **Evidence:** Authentication section: "All requests must include your API key in the `X-Momentum-Key` header." — no transport security requirement. Prerequisites section: "HTTP client capable of sending JSON requests" — no HTTPS mention.
- **Suggestion:** State explicitly that all requests must use HTTPS. Add HTTPS to the Prerequisites or Authentication opening.
- **Fix applied:** Authentication section updated to read "All requests must use HTTPS and include your API key..." Prerequisites updated to mention HTTPS.

---

### Medium Severity

---

**ACCURACY-003** *(merged from ACCURACY-003 + STRUCTURAL-001)*
- **Severity:** medium
- **Dimension:** logical_soundness
- **Location:** Rate Limits section
- **Description:** The phrase "All tiers: 100 requests/hour" introduces a logical inconsistency — "All tiers" implies multiple tiers exist, but no tiers are defined anywhere in the document. If one rate limit applies to all accounts, the phrasing is wrong. If multiple tiers exist with different limits, the section is incomplete. Either way, the statement is self-undermining.
- **Evidence:** Rate Limits section, full text: "All tiers: 100 requests/hour." No tier names, tier definitions, or per-tier differentiation appear anywhere else in the document.
- **Suggestion:** If a single rate limit applies universally, rephrase to "All accounts: 100 requests/hour" or "100 requests per hour, per API key." If multiple tiers exist, document them.
- **Fix applied:** Changed "All tiers:" to "All accounts:".

---

**STRUCTURAL-002**
- **Severity:** medium
- **Dimension:** cross_reference_integrity
- **Location:** Rate Limits section; Error Response Format section
- **Description:** The Rate Limits section describes a `Retry-After` HTTP response header on 429 responses. The Error Response Format section shows a `retry_after` field in the JSON body of error responses. These are described in two separate sections with no cross-reference or explanation of their relationship. A developer cannot tell whether both are present on a 429 response, or whether they should read the header vs. the body field.
- **Evidence:** Rate Limits section: "a `Retry-After` header indicating seconds until the limit resets." Error Response Format section: `"retry_after": 1823` in the JSON error body — no prose connecting these two mentions or explaining both exist simultaneously.
- **Suggestion:** Update the Rate Limits section to state that 429 responses include both a `Retry-After` HTTP response header and a `retry_after` field in the JSON body, both representing seconds to wait.
- **Fix applied:** Rate Limits section updated to explicitly document both the header and the JSON body field.

---

**COHERENCE-001**
- **Severity:** medium
- **Dimension:** consistency
- **Location:** Both endpoint sections — Response subsections
- **Description:** Both endpoints provide parameter documentation in full tables (Name/Type/Required/Description), but neither endpoint documents its response fields. Developers see a raw JSON example but cannot look up field types, ranges, or semantics. This is an asymmetry within the guide's own documentation standard.
- **Evidence:** GET /v2/metrics: full "Parameters" table with 3 rows (Name, Type, Required, Description) — no response field table. GET /v2/validations/{id}: "Path parameters" documented — no response field table. Both responses are represented only by code blocks.
- **Suggestion:** Add response field tables to both endpoints. At minimum document field names, types, and one-line descriptions. For enum fields (e.g., `status`), list all valid values.
- **Fix applied:** Response field tables added to both endpoints.

---

**COHERENCE-002**
- **Severity:** medium
- **Dimension:** completeness
- **Location:** GET /v2/validations/{id} — Response section
- **Description:** The `status` field in the validation response example shows `"CLEAN"` as its value. This is an enumerated field with multiple defined values, but no other valid values are documented. A developer cannot write a complete status-handling implementation from this guide — they do not know what other statuses to expect.
- **Evidence:** Response example: `"status": "CLEAN"` — single value shown. The AVFL framework defines at minimum: `CLEAN`, `GATE_FAILED`, `MAX_ITERATIONS_REACHED`, `CHECKPOINT_WARNING`. None of these are listed in the guide.
- **Suggestion:** Document all valid `status` values in a response field table or inline enumeration.
- **Fix applied:** Response field table for GET /v2/validations/{id} includes `status` with all four enum values.

---

**COHERENCE-003**
- **Severity:** medium
- **Dimension:** cross_reference_integrity
- **Location:** Per-endpoint error tables; Error Response Format section
- **Description:** Each endpoint has an error code table listing HTTP status codes and brief meanings. A separate "Error Response Format" section near the end of the document defines the JSON body structure for error responses. These two pieces of information are structurally disconnected — no prose links them. A developer reading only the endpoint error tables has no idea what the error response body looks like.
- **Evidence:** GET /v2/metrics error table (listing codes 400, 401, 429) and GET /v2/validations/{id} error table (listing 401, 404) — neither contains any reference to the Error Response Format section at the bottom of the document.
- **Suggestion:** Add a line above or below each endpoint error table: "See [Error Response Format](#error-response-format) for the JSON body structure."
- **Fix applied:** Cross-reference note added to both endpoint error tables.

---

### Low Severity

---

**STRUCTURAL-003**
- **Severity:** low
- **Dimension:** completeness
- **Location:** Overview
- **Description:** The Overview states "This guide covers... available endpoints" — phrasing that implies complete coverage of the API's endpoint surface. The guide documents 2 endpoints. There is no indication of how many total endpoints exist, whether this guide is partial, or what is not covered. This overstates the guide's scope.
- **Evidence:** Overview: "This guide covers authentication, available endpoints, request/response formats, and error handling." No endpoint count or completeness caveat appears anywhere.
- **Suggestion:** Replace "available endpoints" with "the endpoints listed below" to make scope honest without requiring enumeration of unlisted endpoints.
- **Fix applied:** Overview updated to "the endpoints listed below."

---

**COHERENCE-004**
- **Severity:** low
- **Dimension:** clarity
- **Location:** GET /v2/metrics — Parameters table, `workflow` row
- **Description:** The `workflow` parameter is described as "Filter by workflow name" with no specification of what happens when the provided name does not match any existing workflow. Industry practice is split between returning 200 with empty results and returning 400 — the absence of documentation leaves developers uncertain.
- **Evidence:** Parameters table, `workflow` row, Description column: "Filter by workflow name." No behavior note for no-match case. The endpoint's error table documents 400 only for "Invalid date range," not for unrecognized workflow names.
- **Suggestion:** Append behavior note: "Returns empty results (200) if the workflow name does not match any workflow."
- **Fix applied:** Parameter description updated to include no-match behavior.

---

## Findings Summary — Iteration 1

| Severity | Count |
|---|---|
| critical | 0 |
| high | 2 |
| medium | 5 |
| low | 2 |
| **total** | **9** |

**Raw findings before consolidation:** 11
**Duplicates removed:** 1 (STRUCTURAL-001 merged into ACCURACY-003 — both addressed the "All tiers" phrasing; logical_soundness framing kept)
**False positives discarded:** 1 (ACCURACY-001 — `mk_live_` prefix implying test key environment; could not be confirmed without source material; discarded per conservative flagging)

---

## Scoring Calculation — Iteration 1

| Component | Value |
|---|---|
| Starting score | 100 |
| High findings (2 × −8) | −16 |
| Medium findings (5 × −3) | −15 |
| Low findings (2 × −1) | −2 |
| **Total deductions** | **−33** |
| **Final score** | **67** |

Grade: Fair (50–70) — notable issues, fix required.

---

## Fix Log — Iteration 1

All 9 findings resolved in severity order:

| Finding ID | Severity | What Changed |
|---|---|---|
| STRUCTURAL-004 | high | Added "Base URL" block in Authentication section with note to replace example domain with account dashboard hostname |
| ACCURACY-002 | high | Added "All requests must use HTTPS" to Authentication section; added HTTPS mention to Prerequisites |
| ACCURACY-003 | medium | Changed "All tiers: 100 requests/hour" to "All accounts: 100 requests/hour" |
| STRUCTURAL-002 | medium | Rate Limits updated to state both `Retry-After` HTTP header and `retry_after` JSON body field are present on 429 responses |
| COHERENCE-001 | medium | Added response field tables to GET /v2/metrics and GET /v2/validations/{id} |
| COHERENCE-002 | medium | Response field table for GET /v2/validations/{id} documents all four `status` enum values: CLEAN, GATE_FAILED, MAX_ITERATIONS_REACHED, CHECKPOINT_WARNING |
| COHERENCE-003 | medium | Added "See Error Response Format" cross-reference note to both endpoint error tables |
| STRUCTURAL-003 | low | Overview changed from "available endpoints" to "the endpoints listed below" |
| COHERENCE-004 | low | `workflow` parameter description updated to specify 200 with empty results on no-match |

---

## Iteration 2 — Findings

One new finding identified in re-validation of the fixed document:

---

**COHERENCE-005** *(post-fix, iteration 2)*
- **Severity:** low
- **Dimension:** consistency
- **Location:** GET /v2/metrics — Response Fields table, `avg_score` row
- **Description:** The response field table added in the fix pass describes `clean_rate` with an explicit range notation "(0–1)" but describes `avg_score` without a range. The example value `91.3` implies a 0–100 scale, but the description ("Average validation score across all runs") does not confirm this. This is inconsistent with the documentation style used for `clean_rate` in the same table.
- **Evidence:** Response Fields table: `clean_rate` — "float (0–1) | Fraction of validations that achieved CLEAN status"; `avg_score` — "float | Average validation score across all runs" — no range specified.
- **Suggestion:** Update `avg_score` description to include range: "float (0–100) | Average validation score across all runs."
- **Status:** NOT FIXED (score remained ≥ 95; pipeline exited CLEAN before fix phase was triggered)

---

## Scoring Calculation — Iteration 2

| Component | Value |
|---|---|
| Starting score | 100 |
| Low findings (1 × −1) | −1 |
| **Final score** | **99** |

Grade: Clean (≥95) — passes threshold.

---

## Iteration History

| Iteration | Phase | Findings | Score | Decision |
|---|---|---|---|---|
| 1 | Validate | 11 raw (9 after dedup/discard) | — | — |
| 1 | Consolidate | 9 final | 67 | FAIL |
| 1 | Fix | 9 resolved | — | loop |
| 2 | Validate | 1 new (COHERENCE-005) | — | — |
| 2 | Consolidate | 1 final | 99 | CLEAN — exit |

---

## Benchmark Notes (Phase 2 Composition — Adversary-Only)

**Variant:** adv-only — 3 Adversary reviewers (1 per lens), no Enumerator, no dual-review cross-check. All findings MEDIUM confidence by default.

**Fixture:** `api-guide-clean.md` — a realistic, well-drafted API guide with genuine issues. Not a pristine document; not a seeded-errors document.

**What the adversary composition found:**
- 2 high-severity issues: missing HTTPS requirement (security gap), undefined production base URL (developer-blocking)
- 5 medium-severity issues: 3 coherence/consistency gaps (response field documentation, status enum values, cross-reference disconnection), 1 logical inconsistency (tier phrasing), 1 cross-reference integrity gap (Retry-After header vs. body)
- 2 low-severity issues: scope overclaim in Overview, underdocumented filter behavior

**False positive rate:** 1 of 11 raw findings discarded (9%). The discarded finding (ACCURACY-001: `mk_live_` prefix implying test keys) was an adversarial hunch that did not meet the evidence threshold — correctly filtered.

**Efficiency:** CLEAN in 2 iterations. Iteration 1 score 67 reflects genuine, substantive issues across all three lenses. Iteration 2 score 99 reflects a thorough fix pass with one residual low-severity documentation style gap.

**Adversary framing effectiveness:** The holistic, hunch-driven approach found issues that a checklist reviewer might miss — notably the ACCURACY-002 HTTPS omission (a security issue invisible in a structural enumeration) and STRUCTURAL-002 (the disconnect between two descriptions of the same retry mechanism in separate sections). The framing proved productive without generating false positives.
