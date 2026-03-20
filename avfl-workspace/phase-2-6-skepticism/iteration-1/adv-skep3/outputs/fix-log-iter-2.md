# Fix Log — Iteration 2

**Fixer role:** technical writer
**Input score:** 95/100 (PASS — borderline clean; fixes applied to resolve remaining issues)
**Findings addressed:** 3 (0 critical, 0 high, 1 medium, 2 low)
**Fix order:** severity-first (medium → low)

---

## STRUCTURAL-IT2-001 (medium) — Section reference number incorrect

**What changed:** Stage 4: "See Section 6 — Security Considerations for authentication and access control details" → "See Security Considerations for authentication and access control details."

**Why:** The fix in iteration 1 added Security Considerations as a new section between Operational Notes and Conclusions, making it the 5th top-level section. Stage 4's reference still called it "Section 6," which was now incorrect. Removing the section number makes the reference robust to future section additions or reordering. The section name alone is sufficient for navigation in a short document.

---

## ACCURACY-IT2-001 (low) — Unattributed benchmark claim

**What changed:** "Benchmarks show that streaming is 3× faster than batch processing for files under 10MB. For larger payloads, batch processing is preferred." → "In general, streaming outperforms batch processing for small files (under 10MB); for larger payloads, batch processing is preferred."

**Why:** The original phrasing ("Benchmarks show") implies specific cited evidence that is not present. The corrected phrasing frames this as a design principle (which is what it effectively is in the document context) rather than a measurement claim. The specific 3× figure is removed since no source is available to support it; the directional statement is retained and now stands on its own as a statement of design intent.

---

## COHERENCE-IT2-001 (low) — Security audit logs conflated with operational DLQ

**What changed:** Security Considerations — Audit logging bullet:
- Before: "Authentication failures and rejected events are logged to the dead-letter queue for operational review."
- After: "Authentication failures are logged to the security audit log. Malformed events are logged to the dead-letter queue for data quality review."

**Why:** Routing security events (authentication failures, 401) and data quality events (malformed events, 400) to the same dead-letter queue conflates two distinct operational concerns. Security teams monitor authentication failures for intrusion detection; data engineering teams monitor the DLQ for malformed event rates. Separating the two logging destinations makes each stream useful to its intended consumer without filtering noise. This also corrects an inconsistency with Stage 1, which already described the DLQ as the destination for malformed events only.
