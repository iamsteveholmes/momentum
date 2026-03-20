# Fix Log — Iteration 1

**Source document:** fixture/research-summary-seeded.md
**Score before fixes:** 78/100
**Findings addressed:** 6 (2 high, 1 medium, 3 low)

---

## ACCURACY-001 (HIGH) — Meta-Judge factual error

**What changed:** Rewrote the first paragraph of Key Findings > Multi-Agent Review Performance.

**Before:**
> Meta-Judge (2025) found that using 3 independent reviewers outperformed a single-agent approach by 15% absolute accuracy, with optimal performance achieved at the 3-reviewer configuration. Teams should therefore target at least 3 reviewers per validation pass to maximize accuracy gains.

**After:**
> Meta-Judge (2025) found that using 2 independent reviewers with majority voting outperformed a single-agent approach by approximately 8–12% absolute accuracy (77.26% vs. 68.89%), with optimal performance achieved at the 2-reviewer configuration. Adding a third reviewer decreased performance, suggesting that framing diversity — not raw reviewer count — is the key driver of accuracy gains.

**Why:** The original stated 3 reviewers and 15% gain — both incorrect per source data. Actual: 2 reviewers, ~8.4% absolute gain (77.26 − 68.89), with 3rd agent decreasing performance. The prescriptive recommendation ("Teams should therefore target at least 3 reviewers") was also removed from the Findings section (prescriptions belong in Methodology/Conclusions, and the underlying claim was wrong).

---

## COHERENCE-001 (HIGH) — Threshold contradiction

**What changed:** Updated Executive Summary threshold from 90 to 95.

**Before:**
> a validation threshold of 90 out of 100 providing the optimal balance between quality requirements and iteration cost.

**After:**
> a validation threshold of 95 out of 100 providing the optimal balance between quality requirements and iteration cost.

**Why:** Executive Summary said 90; Methodology said 95. The Methodology section is the authoritative specification of the threshold. Updated Executive Summary to match.

---

## STRUCTURAL-001 (MEDIUM) — Missing References section

**What changed:** Added a References section at the end of the document.

**Added:**
```
## References
- Meta-Judge (2025): Study on multi-agent majority voting evaluation...
- PoLL (2024): Panel of LLM Evaluators study...
- Huang et al. (2023): Error propagation analysis...
- ASCoT (2025): Agentic step-level evaluation study...
```

**Why:** Final research summary with four cited studies and specific quantitative claims had no bibliography. Added identifiable reference entries for each cited study.

---

## ACCURACY-002 (LOW) — PRM precision loss

**What changed:** Restored lower-bound qualifier in Staged Validation Efficiency paragraph.

**Before:**
> step-level feedback is 8% more accurate

**After:**
> step-level feedback is more than 8% more accurate

**Why:** Source finding is ">8%" (a lower bound). The document dropped the qualifier, converting a lower bound to a precise claim.

---

## COHERENCE-002 (LOW) — Prescription in Key Findings

**What changed:** Removed the prescriptive sentence from Key Findings (addressed as part of the ACCURACY-001 fix — the sentence "Teams should therefore target at least 3 reviewers per validation pass" was removed when rewriting the paragraph).

**Why:** Actionable prescriptions belong in Methodology or Conclusions, not Key Findings. The sentence was also factually wrong and is not needed after the factual correction.

---

## COHERENCE-003 (LOW) — PoLL misleading framing

**What changed:** Updated the PoLL paragraph to frame the finding around diverse reviewer configurations rather than raw reviewer count.

**Before:**
> The PoLL (2024) study corroborated these findings using panel evaluations across multiple benchmarks, consistently showing that more reviewers produces better outcomes.

**After:**
> The PoLL (2024) study corroborated these findings using panel evaluations across multiple benchmarks, consistently showing that diverse reviewer configurations outperform single-model evaluation when reviewers apply different cognitive framings.

**Why:** "More reviewers produces better outcomes" implies raw count drives quality and contradicts the Conclusions section's emphasis on framing diversity. Reframed to match the document's own Conclusions.

---

## Summary

| Finding | Severity | Status |
|---|---|---|
| ACCURACY-001 | High | Fixed — corrected reviewer count (3→2) and accuracy gain (15%→~8–12%), removed wrong prescription |
| COHERENCE-001 | High | Fixed — aligned threshold (90→95) in Executive Summary |
| STRUCTURAL-001 | Medium | Fixed — added References section |
| ACCURACY-002 | Low | Fixed — restored ">8%" lower-bound qualifier |
| COHERENCE-002 | Low | Fixed — removed prescription from Key Findings (done as part of ACCURACY-001) |
| COHERENCE-003 | Low | Fixed — reframed PoLL finding around framing diversity |
