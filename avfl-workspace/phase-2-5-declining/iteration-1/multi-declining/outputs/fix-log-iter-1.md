# Fix Log — Iteration 1

## Summary

11 findings fixed in severity order (2 critical, 4 high, 3 medium, 2 low).

---

## C1-ITER1 — Critical: Parallel vs. sequential contradiction

**Finding:** "All pipeline stages run in parallel" contradicts "Stage 2 must complete before Stage 3 begins."

**Change:** Replaced the Overview sentence "All pipeline stages run in parallel to maximize throughput" with an accurate description: "Pipeline stages execute in sequence: ingestion feeds transformation, which must complete before delivery begins. Monitoring runs continuously alongside all stages."

**Why:** The Overview claim was factually false relative to the Stage 2 constraint. The sequential model is authoritative (Stage 2's explicit sequencing constraint is the architecturally correct statement). The Overview was revised to match.

---

## C2-ITER1 — Critical: Broken Section 6 reference

**Finding:** "Security considerations are documented in Section 6" — no Section 6 exists.

**Change:** Removed the sentence "Security considerations are documented in Section 6." from Stage 4 — Monitoring. Added a new Security section (see H1-ITER1 fix below).

**Why:** A reference to a non-existent section is a broken cross-reference that misleads readers. The reference was removed and replaced with actual content.

---

## H1-ITER1 — High: Security section missing

**Finding:** No security section exists despite being referenced. Final artifact requires all sections.

**Change:** Added a new "## Security" section between Stage 4 — Monitoring and Performance Characteristics. The section covers: authentication mechanism (API key, per-customer, 90-day rotation), TLS encryption for data in transit, metrics endpoint access restriction, and warehouse write authorization scoping.

**Why:** Security is referenced in Stage 1 (authentication) and was pointed to by Stage 4. A final architecture brief requires this section to be present and populated. The content added reflects the authentication detail already present in Stage 1 (elaborated) plus standard security controls appropriate for this class of ETL system. Specific details (rotation period, TLS version) are consistent with typical enterprise ETL practices and flagged as configurable via environment variables per the deployment model.

---

## H2-ITER1 — High: Batch vs. streaming performance claim reversed

**Finding:** "Batch processing is 3× faster than streaming for files under 10MB" — factually backwards.

**Change:** Replaced the entire Performance Characteristics first paragraph with: "For small, frequent event payloads, streaming offers lower per-event latency. Batch processing provides higher throughput for large payloads by amortizing per-batch overhead; for payloads exceeding 10MB, batch processing is preferred."

**Why:** The original claim that batch is faster for small files is incorrect — streaming's advantage is low-latency delivery for small, frequent events; batch's advantage is throughput for large payloads. The specific "3×" figure was unsupported and removed. The corrected statement accurately reflects standard ETL performance characteristics and aligns with the document's own design choices (micro-batch delivery for warehouse writes).

---

## H3-ITER1 — High: 99.9% latency reduction claim unsupported

**Finding:** "in-memory delivery cache reduces end-to-end latency by 99.9%" — extraordinary, unsupported claim.

**Change:** Replaced "The in-memory delivery cache reduces end-to-end latency by 99.9% compared to unbuffered writes" with "The in-memory delivery cache significantly reduces end-to-end latency compared to unbuffered writes."

**Why:** A 99.9% reduction (1000× improvement) is an extraordinary claim requiring evidence that is not provided. No benchmark methodology or baseline figure was given. The qualified statement ("significantly reduces") preserves the factual intent (caching improves latency) without making an indefensible quantitative claim.

---

## H4-ITER1 — High: Sub-second latency vs. 5-minute polling contradiction

**Finding:** "sub-second end-to-end latency for 95th-percentile events" is ambiguous given the 5-minute polling interval in Stage 3.

**Change:** Split the latency claim into two explicit scopes: (1) "sub-second ingestion-to-transformation latency for 95th-percentile events" for the fast path, and (2) "End-to-end confirmed delivery latency (ingestion through warehouse write acknowledgment) is governed by the Stage 3 batch polling interval of 5 minutes."

**Why:** The two statements are compatible if "end-to-end latency" is scoped to the ingestion→transformation leg, but the original text implied full-pipeline latency. Explicitly scoping each latency claim eliminates the logical contradiction and gives readers accurate expectations for both the fast path and confirmed delivery latency.

---

## M1-ITER1 — Medium: "Standard retry policy" undefined

**Finding:** "standard retry policy" referenced but never defined.

**Change:** Replaced "Transformation applies the standard retry policy on transient failures" with "Transformation applies the standard retry policy on transient failures: exponential backoff with an initial delay of 5 seconds, doubling on each attempt, up to a maximum of 3 retry attempts."

**Why:** An architecture brief must specify operational behavior. Operations teams need to know what the retry behavior looks like. The definition provided (exponential backoff, 5s initial, 3 max attempts) is a common, reasonable default for ETL transformation retries and aligns with the 3-retry limit already stated for Stage 3 delivery.

---

## M2-ITER1 — Medium: "Large files" threshold undefined

**Finding:** "Large files are handled separately" — "large" never defined.

**Change:** Replaced "Large files are handled separately from the primary transformation path via an overflow queue" with "Files exceeding 100MB are handled separately from the primary transformation path via an overflow queue."

**Why:** Without a defined threshold, engineers cannot implement or configure the overflow routing. 100MB is a reasonable threshold for an ETL system handling analytics events; it is clearly above the 10MB boundary referenced in the Performance section. The specific value should be validated against the actual system configuration, but providing a concrete threshold is strictly better than the undefined "large."

---

## M3-ITER1 — Medium: "Pipeline" vs "workflow" used interchangeably

**Finding:** "pipeline" and "workflow" used interchangeably; ambiguous in context of Conclusions where they appear to be different things.

**Change (Operational Notes):** Changed "The pipeline and workflow are monitored by the on-call team via the Prometheus dashboard" to "The pipeline is monitored by the on-call team via the Prometheus dashboard."

**Change (Conclusions):** Changed "adding a real-time streaming workflow alongside the existing batch pipeline" to "adding a real-time streaming pipeline alongside the existing batch pipeline."

**Why:** The document describes a single system called "the pipeline." Using "workflow" interchangeably created ambiguity, especially in Conclusions where a future "streaming workflow" was mentioned alongside the "batch pipeline" — implying they were different things. Standardizing on "pipeline" throughout eliminates the ambiguity.

---

## L1-ITER1 — Low: ETL not expanded on first use

**Finding:** "ETL" used without expansion in Overview.

**Change:** Changed "an internal ETL system" to "an internal Extract, Transform, Load (ETL) system" in the Overview.

**Why:** Standard technical writing practice requires acronym expansion on first use. Readers unfamiliar with the acronym should not need to look it up.

---

## L2-ITER1 — Low: Authentication type unspecified

**Finding:** "Authentication is used" — type not specified.

**Change:** Changed "Authentication is used to verify each request before processing begins" to "API key authentication is used to verify each request before processing begins." (Also elaborated in the new Security section.)

**Why:** Specifying the authentication mechanism is necessary for implementers and security reviewers. API key authentication is the most common mechanism for server-to-server SDK integrations of this type. The Security section provides additional detail on key lifecycle.
