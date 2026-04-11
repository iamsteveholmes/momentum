---
sub_question: practitioner-qa
date: 2026-04-10
status: complete
---

# Practitioner Q&A Notes

Three questions surfaced by AVFL checkpoint validation. Answers captured from practitioner (Steve) on 2026-04-10.

---

## Q1 — Scope: Böckeler's harness-engineering.html

**Question:** Should synthesis treat Böckeler's "Harness Engineering for Coding Agent Users" (martinfowler.com) as in-scope or out-of-scope for this comparison?

**Answer:** In-scope for mentioning as future research but not the primary focus. The scope of this comparison is particular to the flywheel concept. Böckeler's article should be noted as adjacent/relevant but not counted as part of the Fowler series for gap analysis.

**Synthesis instruction:** Reference Böckeler's article where it adds context, but frame it explicitly as a supplementary source outside the core comparison. Flag it as a candidate for a follow-on research pass focused on harness engineering.

---

## Q2 — Authoritative flywheel numbering

**Question:** Which is more authoritative — product brief (#4 of 7, "Evaluation Flywheel") or practice-overview (#7 of 8, "Practice compounds")?

**Answer:** Practitioner was uncertain; deferred to git log analysis.

**Git evidence:**
- Product brief (`_bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md`) — committed 2026-03-16, planning artifact
- Practice-overview (`skills/momentum/references/practice-overview.md`) — last updated 2026-04-04, live canonical reference in the installed plugin

**Recommendation (accepted):** Practice-overview is authoritative. It is:
1. More recent by 3 weeks
2. The live installed reference (not a planning artifact)
3. More evolved framing: "Practice compounds" broadens "Evaluation Flywheel" to systemic cross-story improvement

**Synthesis instruction:** Use practice-overview framing — principle #7 of 8, "Practice compounds." Acknowledge the earlier "Evaluation Flywheel" name from the product brief as the historical precursor with a narrower defect-tracing focus.

---

## Q3 — Gemini/Yegge contamination

**Question:** Should synthesis use Gemini's Yegge Momentum analysis as contrast context, or discard it?

**Answer:** Out of scope. Discard entirely.

**Follow-up instruction:** If a follow-on Gemini research pass is warranted, re-run with a prompt that explicitly points Gemini to our Momentum repository URL so it analyzes the correct project.

**Synthesis instruction:** Do not reference Steve Yegge's Momentum, NTM, Beads, PageRank, or Thompson sampling in the synthesis. Note in the synthesis frontmatter that Gemini output was quarantined due to incorrect subject identification.
