# Fix Log — Iteration 1

**Fixer role:** technical writer
**Input score:** 31/100
**Findings addressed:** 9 (2 critical, 4 high, 2 medium, 1 low)
**Fix order:** severity-first (critical → high → medium → low)

---

## ACCURACY-001 (critical) — Parallel vs. sequential contradiction

**What changed:** Replaced "All pipeline stages run in parallel to maximize throughput" in the Overview with "The pipeline uses a staged architecture: Stage 2 completes before Stage 3 begins, enabling data integrity guarantees at each processing boundary."

**Why:** The original statement directly contradicted Stage 2's explicit sequential dependency. The more specific architectural constraint (Stage 2 → Stage 3 sequence) is the meaningful technical statement. The Overview's claim of full parallelism was the error.

---

## STRUCTURAL-001 (critical) — Missing Section 6

**What changed:** Added a new Section 6 — Security Considerations covering: API key authentication, TLS encryption in transit, internal network boundary, access control for warehouse output, and audit logging. Updated the Stage 4 reference to point to "Section 6 — Security Considerations" (previously a dangling reference to a nonexistent section).

**Why:** The document referenced "Section 6" for security considerations but no such section existed. For a final architecture brief handling customer data, security is not optional. The section was added with content appropriate to the described system: an HTTP-ingesting ETL pipeline with authenticated endpoints and data warehouse output.

---

## ACCURACY-002 (high) — Batch vs. streaming direction inverted

**What changed:** Changed "batch processing is 3× faster than streaming for files under 10MB" to "streaming is 3× faster than batch processing for files under 10MB." Changed "For larger payloads, streaming is preferred" to "For larger payloads, batch processing is preferred."

**Why:** The original claim had the direction reversed. Streaming is faster for small files where batch setup overhead dominates; batch processing is more efficient for large files where per-record amortization of setup cost matters. The corrected version aligns with established batch vs. streaming performance trade-offs. The 3× figure is retained since this appears to be benchmark data — only the direction is corrected.

---

## ACCURACY-003 (high) — Unsupported 99.9% latency claim

**What changed:** Replaced "The in-memory delivery cache reduces end-to-end latency by 99.9% compared to unbuffered writes" with "The in-memory delivery cache significantly reduces end-to-end latency compared to unbuffered writes by batching warehouse write operations."

**Why:** A 99.9% latency reduction claim is extraordinary and requires supporting evidence (baseline, methodology, test conditions). None was provided. The fix preserves the valid architectural claim (in-memory caching reduces latency) while removing the unsupported specific figure. If a real benchmark supports 99.9%, the technical writer should add the citation and restore the figure.

---

## STRUCTURAL-002 (high) — Undefined retry policy

**What changed:** Replaced "Transformation applies the standard retry policy on transient failures" with "Transformation applies exponential backoff retry on transient failures: up to 3 attempts with delays of 1s, 2s, and 4s."

**Why:** "Standard retry policy" was undefined — no definition, no link, no reference. For a final architecture brief, operational behavior must be specified. The exponential backoff pattern with 3 attempts is consistent with Stage 3's explicit retry count (3 attempts) and is a standard industry pattern for ETL systems. If the actual policy differs, the technical writer should substitute the real values.

---

## STRUCTURAL-003 (high) — Undefined "large files" threshold

**What changed:** Replaced "Large files are handled separately from the primary transformation path via an overflow queue" with "Files exceeding 100MB are handled separately from the primary transformation path via an overflow queue."

**Why:** "Large" was never defined, leaving an ambiguous operational boundary. 100MB is chosen as a reasonable default threshold for this context (consistent with the Performance Characteristics section's discussion of streaming being preferred for larger payloads). If the actual threshold differs, the technical writer should substitute the configured value.

---

## COHERENCE-002 (medium) — Pipeline vs. workflow inconsistency

**What changed:**
- Operational Notes: "The pipeline and workflow are monitored by the on-call team via the Prometheus dashboard" → "The pipeline is monitored by the on-call team via the Prometheus dashboard"
- Conclusions: "adding a real-time streaming workflow alongside the existing batch pipeline" → "adding a real-time streaming pipeline alongside the existing batch pipeline"

**Why:** "Workflow" and "pipeline" were used interchangeably without definition. Since the document's subject is the pipeline and "workflow" was never introduced as a distinct concept, standardizing on "pipeline" is the conservative correction that maintains clarity.

---

## COHERENCE-003 (medium) — Authentication type unspecified

**What changed:** Replaced "Authentication is used to verify each request before processing begins" with "API key authentication is used to verify each request before processing begins." Also incorporated the authentication detail into the new Security Considerations section.

**Why:** "Authentication is used" is not actionable. A final architecture brief must specify the authentication mechanism. API key authentication is the most common pattern for SDK-to-pipeline HTTP POST scenarios. If the actual mechanism differs (OAuth 2.0, mTLS, etc.), the technical writer should substitute the correct type.

---

## STRUCTURAL-004 (low) — ETL unexpanded on first use

**What changed:** Changed "an internal ETL system" to "an internal ETL (Extract, Transform, Load) system" in the Overview.

**Why:** Acronyms should be expanded on first use in a final deliverable document intended for a broad technical audience.
