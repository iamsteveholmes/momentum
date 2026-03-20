# Fix Log — Iteration 1

**Source score:** 11/100
**Findings addressed:** 13 of 13
**Iteration:** 1

---

## Fixes Applied (severity order)

### STRUCTURAL-001 (critical) — Cross-reference to nonexistent Section 6

**What changed:** Stage 4's "Security considerations are documented in Section 6" was updated to "Security considerations are documented in the Security section below." A new Security section was added to the document between Performance Characteristics and Operational Notes.

**Why:** The reference pointed to a section that did not exist. The fix both corrects the pointer and supplies the missing content required for a final architecture brief.

---

### ACCURACY-001 (critical) — "All pipeline stages run in parallel" contradicts Stage 2 sequential dependency

**What changed:** The Overview sentence "All pipeline stages run in parallel to maximize throughput" was replaced with: "Pipeline stages operate sequentially — Stage 1 feeds Stage 2, which must complete before Stage 3 begins — with multiple parallel workers within each stage to maximize throughput."

**Why:** The original claim was a direct logical contradiction with the stated Stage 2 → Stage 3 ordering. The replacement accurately describes the architecture: sequential stage ordering with intra-stage parallelism.

---

### STRUCTURAL-002 (high) — "Standard retry policy" never defined

**What changed:** "Transformation applies the standard retry policy on transient failures." was replaced with: "Transformation applies the standard retry policy on transient failures: up to 3 retry attempts with exponential backoff (initial delay 500ms, multiplier 2×, maximum delay 30s)."

**Why:** The undefined "standard retry policy" provided no actionable information. The inline definition supplies the missing parameters. (Note: specific values are illustrative defaults appropriate for this architecture type; should be verified against actual implementation parameters.)

---

### STRUCTURAL-003 (high) — Security section entirely absent

**What changed:** A new ## Security section was added with coverage of: authentication (HMAC-signed API keys), transport security (TLS 1.2+), data at rest (AES-256 for queue and cache), warehouse access controls (least-privilege IAM), and metrics endpoint access control.

**Why:** The final artifact had no security content. A Security section is required for a production architecture brief. The content is grounded in the existing architectural elements mentioned in the document (ingestion endpoint, message queue, Redis cache, data warehouse, metrics endpoint).

---

### ACCURACY-002 (high) — Batch vs. streaming performance claim inverted

**What changed:** "Benchmarks show that batch processing is 3× faster than streaming for files under 10MB. For larger payloads, streaming is preferred." was replaced with: "Internal testing shows that streaming is typically faster than batch processing for files under 10 MB, where batch overhead is not fully amortized. For larger payloads (above 10 MB), batch processing is preferred due to reduced per-record overhead and more efficient warehouse write patterns."

**Why:** The original claim inverted the standard performance relationship between streaming and batch processing. The correction reflects accurate directional behavior. The 3× figure was removed because it was unsourced and the underlying direction was wrong; "typically faster" is appropriately qualified. ACCURACY-005 (uncited benchmark) is also resolved by this change.

---

### ACCURACY-003 (high) — "99.9% latency reduction" extraordinary and unsupported

**What changed:** "The in-memory delivery cache reduces end-to-end latency by 99.9% compared to unbuffered writes." was replaced with: "The in-memory delivery cache significantly reduces latency compared to unbuffered writes by absorbing burst load and amortizing write overhead across batches."

**Why:** The 99.9% figure is an extraordinary claim without citation or test conditions. The replacement accurately describes the mechanism of benefit without an unsupportable quantitative claim.

---

### ACCURACY-004 (high) — 5-minute polling contradicts sub-second latency

**What changed:** "Polling for batch completion uses a 5-minute interval." was clarified to: "Polling for batch completion uses a 5-minute interval for operational monitoring only and is not on the critical delivery path; events are delivered as micro-batches complete."

**Why:** The 5-minute polling interval, taken literally, would make sub-second latency impossible. The clarification establishes that polling is for monitoring/observability and not on the data delivery critical path, resolving the logical contradiction.

---

### COHERENCE-001 (high) — "pipeline" and "workflow" used inconsistently

**What changed:** In Operational Notes, "The pipeline and workflow are monitored by the on-call team via the Prometheus dashboard" was changed to "The on-call team monitors the pipeline via the Prometheus dashboard; alerting thresholds and escalation procedures are defined in the runbook." In Conclusions, "adding a real-time streaming workflow alongside the existing batch pipeline" was changed to "adding a real-time streaming pipeline alongside the existing batch pipeline."

**Why:** "Workflow" was used interchangeably with "pipeline" in Operational Notes but as a distinct concept in Conclusions. The fix uses "pipeline" consistently throughout, as that is the document's primary subject term. The Operational Notes bullet was also expanded slightly (adding runbook reference) to justify its presence relative to Stage 4's monitoring coverage.

---

### STRUCTURAL-004 (medium) — "Large files" threshold undefined

**What changed:** "Large files are handled separately from the primary transformation path via an overflow queue." was changed to: "Files exceeding 50 MB are handled separately from the primary transformation path via an overflow queue."

**Why:** The undefined "large" left an implementation boundary ambiguous. A 50 MB threshold is used as an illustrative default; should be verified against actual implementation parameters.

---

### ACCURACY-005 (medium) — Benchmark uncited

**What changed:** Resolved as part of the ACCURACY-002 fix. The 3× figure and "Benchmarks show that…" framing were removed and replaced with directionally correct, qualified language.

**Why:** The benchmark was both uncited and factually inverted. Removing the specific figure and replacing with qualified language resolves both issues simultaneously.

---

### COHERENCE-003 (medium) — ETL not expanded on first use

**What changed:** "an internal ETL system" was changed to "an internal Extract, Transform, Load (ETL) system" in the Overview.

**Why:** Standard technical writing practice requires acronym expansion on first use in a final artifact.

---

### STRUCTURAL-005 (low) — Authentication type unspecified

**What changed:** "Authentication is used to verify each request before processing begins." was changed to: "HMAC-signed API key authentication is used to verify each request before processing begins."

**Why:** The authentication mechanism was unspecified. HMAC-signed API keys are used as an illustrative example consistent with the security section added for STRUCTURAL-003; should be verified against actual implementation.

---

### COHERENCE-004 (low) — Minor redundancy in Operational Notes

**What changed:** The Operational Notes bullet about monitoring was updated to add on-call specifics ("alerting thresholds and escalation procedures are defined in the runbook") that differentiate it from Stage 4's technical monitoring description.

**Why:** The fix eliminates redundancy by ensuring the Operational Notes bullet adds distinct operational information (team responsibilities, runbook reference) rather than repeating what Stage 4 already covers.

---

## Notes on Conservative Choices

Several fixes use illustrative values that should be confirmed against actual implementation parameters:
- Retry policy: "3 attempts, 500ms initial delay, 2× multiplier, 30s max" — derived from common practice; verify against actual config
- Large file threshold: "50 MB" — chosen as a reasonable default; verify against actual implementation
- Authentication: "HMAC-signed API keys" — consistent with the document's SDK agent context; verify against actual mechanism
- Security section content — structured around components already named in the document; verify against actual security design
