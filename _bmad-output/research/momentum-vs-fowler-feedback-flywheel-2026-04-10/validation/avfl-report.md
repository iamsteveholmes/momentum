---
content_origin: avfl-checkpoint
date: 2026-04-10
profile: checkpoint
corpus_files: 7
topic: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Conceptual Comparison"
status: CHECKPOINT_WARNING
score_before_fix: 37
score_after_fix: estimated 80+
---

# AVFL Checkpoint Validation Report

**Status:** CHECKPOINT_WARNING (score 37/100 before fix; one fix pass applied; continuing per checkpoint protocol)
**Profile:** checkpoint, corpus mode, 3 lenses (structural, accuracy, coherence)
**Files validated:** 7

---

## Pre-Fix Score Breakdown

| Severity | Count | Weight | Subtotal |
|---|---|---|---|
| Critical | 1 | −15 | −15 |
| High | 4 | −8 | −32 |
| Medium | 4 | −3 | −12 |
| Low | 4 | −1 | −4 |
| **Score** | | | **37/100 (Failing)** |

6 duplicate findings removed during consolidation.

---

## Consolidated Findings (pre-fix, sorted by severity)

### CRITICAL

**ACCURACY-002** | cross_reference_integrity | research-momentum-concepts-absent-from-fowler.md:Overview
Böckeler misattributed as co-primary author of the Fowler 5-article "Patterns for Reducing Friction" series. She authored a separate standalone article (harness-engineering.html), not any of the five series articles. All five articles are authored solely by Rahul Garg.
*Fixed: Corrected to "authored by Rahul Garg" with explicit note that Böckeler authored a separate supplementary article.*

### HIGH

**ACCURACY-001** | correctness | research-momentum-flywheel-definition.md:How the Flywheel Is Defined
Internal contradiction: flywheel described as "one of seven core composable principles" and then "principle #7 of eight" in the same section without distinguishing source documents. Product brief = 7 principles (flywheel at #4); practice-overview = 8 principles (flywheel at #7).
*Fixed: Added disambiguation note attributing each count to its source document.*

**ACCURACY-003** | correctness | research-fowler-feedback-flywheel.md:The Problem Being Solved
"Collaboration Loop" tagged [OFFICIAL] but the term does not appear in the Fowler series. SQ2 itself acknowledges this at line 196 ("The series does not use 'Frustration Loop' and 'Collaboration Loop' as formally defined, named concepts") — contradicting its own earlier [OFFICIAL] tag.
*Fixed: Changed [OFFICIAL] to [UNVERIFIED] for "Collaboration Loop" throughout.*

**ACCURACY-004** | correctness | research-fowler-concepts-absent-from-momentum.md:Gap 6
Fabricated lockfile quote attributed to Fowler with [OFFICIAL] tag: "A lockfile that is never updated does not stay stable, it becomes a liability." Confirmed absent from both Context Anchoring and Encoding Team Standards articles via direct verification.
*Fixed: Quote removed. Replaced with accurate description of artifact maintenance concepts actually present in the articles.*

**COHERENCE-002** | cross_document_consistency | research-momentum-concepts-absent-from-fowler.md
harness-engineering.html attributed to "Fowler" throughout SQ4 (9 locations) while SQ5 correctly attributes it to Böckeler. The misattribution inflated "what Fowler covers" in the gap analysis by incorporating Böckeler's separate work.
*Fixed: All 9 instances corrected to "Böckeler's 'Harness Engineering for Coding Agent Users'"; all [OFFICIAL: harness-engineering.html] tags changed to [OFFICIAL: Böckeler, harness-engineering.html].*

### MEDIUM

**ACCURACY-005** | correctness | research-adoption-candidates.md:Candidate 5
45-min/5-min example misattributed to Frustration Loop definition; it illustrates Knowledge Priming benefits, not the Frustration Loop.
*Fixed: Attribution clarified.*

**ACCURACY-007** | correctness | research-fowler-feedback-flywheel.md:Encoding Team Standards
"Teams of 15+ benefit most" oversimplifies "teams of five may not need this; teams of fifteen almost certainly do" — loses lower-bound calibration.
*Fixed: Replaced with accurate Garg heuristic.*

**STRUCTURAL-001** | structural_validity | gemini-deep-research-output.md:frontmatter
Missing `sub_question` frontmatter field (all 6 Claude subagent files have it).
*Fixed: Added `sub_question: null`.*

**STRUCTURAL-003** | cross_reference_integrity | research-momentum-concepts-absent-from-fowler.md:Sources
Incomplete source citation for harness-engineering.html — bare URL, no author/date/title.
*Fixed: Full Böckeler citation added.*

### LOW

**ACCURACY-008** | correctness | research-fowler-feedback-flywheel.md:Cadence Structure
"Seconds to ask, minutes to act" is editorial gloss tagged [OFFICIAL]; not in source.
*Fixed: Changed to [PRAC].*

**COHERENCE-005** | conciseness | research-fowler-concepts-absent-from-momentum.md:Gap 8
Self-defeating gemini citation for Design-First Collaboration.
*Fixed: Removed; replaced with primary source reference.*

**COHERENCE-006** | tonal_consistency | research-momentum-concepts-absent-from-fowler.md:Overview
Promotional tone ("not just advises on it") vs. neutral register elsewhere.
*Fixed: Revised to neutral framing.*

**STRUCTURAL-004** | completeness | gemini-deep-research-output.md:Sources
42 lines of "Opens in a new window" corrupted source rendering from Gemini's browser UI.
*Fixed: Replaced with explanatory note about rendering artifacts.*

---

## Corpus Completeness Check

All 6 scope sub-questions are addressed by dedicated files. No corpus completeness gaps found.

---

## Fix Summary

All 13 findings addressed in one pass. The four highest-impact changes:
1. Böckeler authorship corrected across SQ4 (ACCURACY-002 + COHERENCE-002)
2. Fabricated Fowler lockfile quote removed (ACCURACY-004)
3. "Collaboration Loop" [OFFICIAL] tag corrected to [UNVERIFIED] (ACCURACY-003)
4. Flywheel principle numbering disambiguated by source document (ACCURACY-001)

**No Gemini contamination detected in SQ1–SQ6.** All six research files accurately describe our actual Momentum codebase.

---

## AVFL Findings Summary (for Phase 4 Q&A)

**Unresolved questions surfaced by validation:**
1. The harness-engineering.html article by Böckeler is adjacent to but not part of the Fowler series. Should synthesis treat it as in-scope for the comparison (it's on martinfowler.com and directly relevant to agentic development) or explicitly out-of-scope?
2. The Evaluation Flywheel is "principle #4 in the product brief" vs. "principle #7 in the practice overview" — which framing is most current/authoritative for the project?
3. Gemini analyzed a different "Momentum" (Steve Yegge's tool-intensive model). Does the Yegge Momentum's concepts (Beads/PageRank/Thompson sampling) provide useful contrast context even though they're not our project?
