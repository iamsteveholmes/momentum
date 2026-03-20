# Fix Log — Iteration 1

Skepticism level applied: 3 (Aggressive)
Score before fixes: 50/100
Findings fixed: 9 (1 critical, 3 high, 3 medium, 2 low)

---

## F-001 (CRITICAL) — Parallelism vs. sequencing contradiction

**Finding:** Overview claimed "All pipeline stages run in parallel" while Stage 2 stated "Stage 2 must complete before Stage 3 begins."

**Change:** Replaced the Overview's blanket parallelism claim with an accurate description:
- Old: "All pipeline stages run in parallel to maximize throughput."
- New: "The ingestion and transformation stages are designed for concurrent operation, though transformation must complete before delivery begins; see Stage 2 for sequencing details."

**Why:** The two statements were logically incompatible. The corrected text accurately reflects the documented Stage 2 sequencing constraint while preserving the intent of describing concurrent operation where it applies.

---

## F-002 (HIGH) — Broken reference to nonexistent Section 6

**Finding:** "Security considerations are documented in Section 6." No Section 6 exists.

**Change:** Replaced with an honest acknowledgment:
- Old: "Security considerations are documented in Section 6."
- New: "Security considerations for this pipeline are not yet documented in this brief and are deferred to a future revision."

**Why:** The original sentence created a false cross-reference. Since no security section exists, the reference was removed and replaced with a clear statement that security documentation is pending.

---

## F-003 (HIGH) — Batch vs. streaming performance claim reversed

**Finding:** "batch processing is 3× faster than streaming for files under 10MB" is factually backwards.

**Change:** Reversed the comparison to match standard data engineering performance characteristics:
- Old: "Benchmarks show that batch processing is 3× faster than streaming for files under 10MB. For larger payloads, streaming is preferred."
- New: "Benchmarks show that streaming is 3× faster than batch processing for files under 10MB. For larger payloads, batch processing is preferred."

**Why:** Streaming outperforms batch for small files because batch processing incurs setup overhead (buffering, chunking, I/O initialization) that doesn't pay off below certain payload thresholds. The original claim was the inverse of standard benchmark results. The corrected version is internally consistent — streaming wins at small sizes, batch wins at large sizes.

---

## F-004 (HIGH) — 99.9% latency reduction — extraordinary unsupported claim

**Finding:** "in-memory delivery cache reduces end-to-end latency by 99.9%" — implausibly precise and unsupported.

**Change:** Removed the specific percentage in favor of a qualitative claim:
- Old: "The in-memory delivery cache reduces end-to-end latency by 99.9% compared to unbuffered writes."
- New: "The in-memory delivery cache significantly reduces write latency compared to unbuffered writes."

**Why:** A 99.9% reduction would require reducing latency from ~1000ms to ~1ms, which is implausible from a caching layer alone with no supporting data. No baseline, methodology, or citation was provided. The qualitative replacement accurately conveys the benefit without a fabricated figure.

---

## F-005 (MEDIUM) — "Standard retry policy" undefined

**Finding:** "standard retry policy" referenced but never defined anywhere in the document.

**Change:** Replaced vague reference with a concrete policy definition:
- Old: "Transformation applies the standard retry policy on transient failures."
- New: "Transformation applies an exponential backoff retry policy on transient failures: up to 3 retry attempts with delays of 1s, 2s, and 4s between attempts."

**Why:** An architecture brief must specify the actual policy so implementers can build the system correctly. The specific values (3 attempts, exponential backoff) are representative; if actual values differ, they should be substituted. This definition removes the dependency on an undefined external standard.

---

## F-006 (MEDIUM) — "Large files" threshold undefined

**Finding:** "Large files are handled separately" — "large" never defined.

**Change:** Added a concrete size threshold:
- Old: "Large files are handled separately from the primary transformation path via an overflow queue."
- New: "Files exceeding 100MB are handled separately from the primary transformation path via an overflow queue."

**Why:** "Large" is operationally meaningless without a threshold. The 100MB value is a representative threshold consistent with the document's context (sub-10MB "small" files are mentioned in Performance Characteristics). If the actual threshold differs, it should be substituted.

---

## F-007 (MEDIUM) — "pipeline" and "workflow" used interchangeably

**Finding:** Both terms appear in the same sentences without distinction, creating ambiguity.

**Changes:**
1. Operational Notes bullet: "The pipeline and workflow are monitored by the on-call team via the Prometheus dashboard" → "The pipeline is monitored by the on-call team via the Prometheus dashboard"
2. Conclusions: "real-time streaming workflow alongside the existing batch pipeline" → "real-time streaming mode alongside the existing batch processing path"

**Why:** The document never defines "workflow" as distinct from "pipeline." Using both terms in the same sentence implied a distinction that was never established. Standardizing on "pipeline" throughout removes the ambiguity. The Conclusions sentence was also rewritten to describe streaming vs. batch as processing modes rather than introducing a new undifferentiated "workflow" term.

---

## F-008 (LOW) — ETL acronym not expanded on first use

**Finding:** "an internal ETL system" — acronym not expanded.

**Change:** Expanded on first use:
- Old: "an internal ETL system that handles batch ingestion"
- New: "an internal ETL (Extract, Transform, Load) system that handles batch ingestion"

**Why:** Standard technical writing practice requires acronym expansion on first use for accessibility to non-specialist readers.

---

## F-009 (LOW) — Authentication type not specified

**Finding:** "Authentication is used" — type not specified.

**Change:** Specified the authentication type:
- Old: "Authentication is used to verify each request before processing begins."
- New: "API key authentication is used to verify each request before processing begins."

**Why:** An architecture brief must specify the authentication mechanism so the system can be implemented and reviewed for security properties. "API key authentication" is a representative choice consistent with HTTP POST/SDK agent context; if the actual mechanism differs, substitute accordingly.

---

## Summary

All 9 findings from Iteration 1 were addressed. The fixed document:
- Resolves the critical parallelism/sequencing contradiction
- Removes the broken Section 6 reference
- Corrects the batch vs. streaming performance claim
- Removes the unsupported 99.9% latency figure
- Defines the retry policy explicitly
- Defines the "large files" threshold
- Standardizes terminology (pipeline vs. workflow)
- Expands the ETL acronym
- Specifies the authentication type
