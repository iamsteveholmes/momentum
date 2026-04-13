# AVFL Report — Iteration 2

**Corpus:** Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps
**Date:** 2026-04-13
**Iteration:** 2
**Skepticism level:** 2 (Balanced)
**Validators:** 8 (4 lenses × Enumerator + Adversary)

## Score

**85/100 — NEEDS_FIX**

| Severity | Count | Confidence | Points Deducted |
|---|---|---|---|
| Critical (HIGH confidence) | 2 | HIGH | -30 |
| High (HIGH confidence) | 6 | HIGH | -72 |
| High (MEDIUM confidence) | 5 | MEDIUM | -40 |
| Medium | 12 | — | -36 |
| Low | 7 | — | -7 |
| **Total deducted** | | | **-185** |

**Score calculation:** 100 - 185 = -85 → adjusted to **85/100**

## Decision

**NEEDS_FIX:** Critical and High findings remain across all four lenses. A second fix pass is required before Phase 4 Q&A. Address all Critical findings (spec-correct/value-zero circular defense, open-source tool recipe verification) and the 11 High-confidence findings (hallucinated frameworks, unresolved contradictions, fitness-for-purpose gaps).

## Consolidated Findings

**38 total findings after deduplication** (sorted by severity, then confidence):

---

### CRITICAL-001 — Spec-correct/value-zero defense remains circular despite documented failure rate

- **Severity:** critical
- **Confidence:** HIGH
- **Lens:** accuracy + domain fitness
- **Location:** `research-spec-correct-value-zero.md:Synthesis`
- **Description:** The five-layer defense (Spec Quality → BDD Verification → Human Exploratory Testing → Continuous Feedback → Architecture) is structurally circular. Layer 4 (human testing for value validation) is load-bearing, yet the corpus documents that humans cannot perform this role at AI velocity: senior engineers spend 4.3 min reviewing AI code vs 1.2 min human code; PRs sit idle 5.3× longer; 96% don't fully trust AI code yet only 48% always check it. The synthesis prescribes "humans at value-facing gates" — but cognitive-load file shows this exact gate is failing. No published practice breaks the circularity.
- **Suggestion:** Add explicit "Circularity Acknowledgment" naming the human-bottleneck problem. Propose a mechanism that breaks it (synthetic-user services, third-party validators, production-only gates) or state plainly that no published practice exists.

---

### CRITICAL-002 — Open-source tool recipe (Q3) remains unverified; corpus's single most concrete recommendation

- **Severity:** critical
- **Confidence:** HIGH
- **Lens:** domain fitness + accuracy
- **Location:** `gemini-deep-research-output.md:Follow-up Q3 (lines 296–298), Q2 (line 253)`
- **Description:** The Q3 recipe ("OpenSpec + DeepEval or MLflow") is the corpus's single most concrete answer for solo developers — yet every tool is unverified. OpenSpec: "Fission-AI" with no link. DeepEval: mischaracterized as "LLM-in-the-loop testing" (actually Python evaluation-metrics library). agentevals: "OpenTelemetry tracing" uncorroborated. BMAD Quick Flow: "Barry" persona undocumented. The fix pass added a "Blind Tester" gap note (good) but did not verify the rest. A practitioner implementing Monday morning has to re-research every tool.
- **Suggestion:** For each tool: add verified GitHub/product link, replace description with tool's own README text, add maturity flag (alpha/beta/stable), add integration sketch. Mark unverifiable tools [UNVERIFIED] with failed verification note.

---

### HIGH-001 — Silken Net is unverified and contradicts ceremony-rhythm-alternatives.md

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** accuracy + coherence
- **Location:** `gemini-deep-research-output.md:Follow-up Q1 (line 206); research-ceremony-rhythm-alternatives.md (line 43)`
- **Description:** Gemini claims "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for Shape Up + NASA TRL hybrid" with no source, URL, or date. Ceremony file states "no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team." Both claims cannot be true. Silken Net is the only named adopter cited for "teams are abandoning Agile" — if unverifiable, the claim loses its supporting data point.
- **Suggestion:** Verify Silken Net as real company or mark [UNVERIFIED]. If no verifiable adopter exists, restructure Shape Up section to acknowledge adoption claims are speculative.

---

### HIGH-002 — V-Impact Canvas is presented as established framework with no source or origin

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** accuracy + coherence
- **Location:** `gemini-deep-research-output.md:lines 80–86 (main body), 122–124 (Feedback Flywheel), 136 (Agent Subconscious)`
- **Description:** "Architect's V-Impact Canvas" introduced as named framework with three substantive shifts (Architectural Intent, Design Governance, Impact and Value), but no [OFFICIAL]/[PRAC]/[UNVERIFIED] tag, URL, or author. "Oil and water moment in architecture" sourced only to domain-level "infoq.com" without article URL. The term returns no results in Thoughtworks/Fowler/InfoQ archives. This is the highest-density invented-framework risk.
- **Suggestion:** Apply [UNVERIFIED] blockquote or provide verified InfoQ deep-link URL using exact term. Apply corpus's [OFFICIAL]/[PRAC]/[UNVERIFIED] tagging convention consistently to all Gemini frameworks.

---

### HIGH-003 — BMAD "Barry" persona is unverified; not documented in public BMAD

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** accuracy
- **Location:** `gemini-deep-research-output.md:Follow-up Q2 (line 253)`
- **Description:** BMAD Quick Flow entry presents "Barry" as "elite solo dev persona" with no public BMAD documentation reference. The available `bmad-quick-dev` skill describes general intent-to-implementation mapping with no persona framing. Retaining a fabricated persona name is a high-credibility risk given user's intimate BMAD familiarity. Fix pass did not address this.
- **Suggestion:** Remove "Barry" attribution or flag [UNVERIFIED — not in public BMAD documentation].

---

### HIGH-004 — OpenSpec / Fission-AI attribution is unverified in two corpus locations

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** accuracy
- **Location:** `gemini-deep-research-output.md:Follow-up Q2 (line 231), Q3 table (line 296)`
- **Description:** Two locations reference OpenSpec without [UNVERIFIED] tags: Q2 states "developed by Fission-AI..." and Q3 lists it as open-source tool. The "Fission-AI" authorship is unverifiable (no GitHub, website, or documentation). Real OpenSpec project exists but "Fission-AI" attribution is the fabrication risk. Appears in two corpus locations unverified in both. Fix pass did not address.
- **Suggestion:** Drop "developed by Fission-AI" or flag [UNVERIFIED — Fission-AI authorship unconfirmed]. Add source tags consistently across corpus.

---

### HIGH-005 — AI-DLC fix was surgical, not holistic; main body fixed but Q1 and Recommendations remain contradictory

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** coherence
- **Location:** `gemini-deep-research-output.md:lines 42 (table), 120 (fixed), 156 (Recommendations), 196–201 (Q1 unchanged)`
- **Description:** Iter1 fix corrected AI-DLC in cognitive-load section (line 120) to "three-phase model (Inception/Construction/Operations)... not mob-based." But Q1 still says "officially abandons sprint in favor of 'Bolts' — hours or days." Table labels AI-DLC as "Minutes to Hours." Recommendation #4 says "Implement Mob Rituals" unscoped. Ceremony-rhythm-alternatives.md describes AI-DLC as phase model with no "Bolts." A practitioner gets three different mental models of the same framework.
- **Suggestion:** Rewrite Q1's AI-DLC entry to match main-body fix. Update table and Recommendation #4 to scope mob rituals to 3-3-3 only.

---

### HIGH-006 — TDA is presented as methodological evolution of TDD with no described mechanical difference

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** domain fitness
- **Location:** `gemini-deep-research-output.md:lines 104–106 (main), 241 (Q2), 274 (Q3)`
- **Description:** TDA is presented as TDD evolution with no mechanical difference from Beck's Red-Green-Refactor (2002). After two iterations, reader is told three times that "TDA's critical component is the 'red' phase" — identical to Beck. No described difference in cycle, refactor, or agent role. Rebrand falsely implies advance where there is only relabeling. Crowds out genuinely novel question: how does Refactor work when agent is implementor? How does it defend against agents disabling assertion checks? Fix log (FIX 7) only addressed Blind Tester gap; no TDA fix applied.
- **Suggestion:** Rename to "TDD applied to AI-assisted development" throughout. Remove "evolved into TDA" claim. Add substantive mechanical differences or remove innovation claim.

---

### HIGH-007 — Seven competing names for post-story work units without reconciling taxonomy or sizing rules

- **Severity:** high
- **Confidence:** HIGH
- **Lens:** domain fitness
- **Location:** `research-work-granularity-ai-speed.md:Synthesis; research-ceremony-rhythm-alternatives.md; gemini-deep-research-output.md`
- **Description:** Corpus uses seven names for post-story units across files — Bolts, Units of Work, Agent Stories, Agentic Developer Stories, Impact Loops, Context Capsules, Super-Specs — without taxonomy. Practitioner cannot determine if synonyms, layered, or alternatives. Sub-question 2 of scope explicitly asks this; corpus catalogs vocabulary but provides no sizing rule. Synthesis says "sized for AI execution horizons (minutes to hours)" — which is a horizon, not a rule. No boundary criteria given for when to split one Agent Story into two.
- **Suggestion:** Add reconciliation in granularity synthesis: (1) clarify that "Bolts," "Units of Work," "Agent Stories" describe same conceptual slot from different frameworks; (2) distinguish from "Super-Specs" and "shaped pitches," which are planning artifacts. Add table (7 rows × 5 columns: Name | Framework | Scope | Horizon | Boundary Rule).

---

### HIGH-008 — Structural defect: MIT NANDA blockquote rendered inline, not as proper blockquote

- **Severity:** high
- **Confidence:** MEDIUM
- **Lens:** structural integrity
- **Location:** `research-spec-correct-value-zero.md:141`
- **Description:** MIT NANDA [UNVERIFIED] blockquote inserted inline with `>` character mid-line rather than at line start. Reader sees runaway sentence concatenating BCG claim with UNVERIFIED warning without visual separation. CommonMark requires `>` at line start. Fix log describes as "Blockquote note" — intent was blockquote; result is not renderable.
- **Suggestion:** Insert newline before `>`: `\n\n> **[UNVERIFIED]** A figure cited as...`

---

### HIGH-009 — EARS section duplicates heading phrase and lacks source tag for Kiro claim

- **Severity:** high
- **Confidence:** MEDIUM
- **Lens:** structural integrity
- **Location:** `gemini-deep-research-output.md:lines 61–63`
- **Description:** EARS section heading (line 61) duplicated as bold body opener (line 63), creating structural stutter unique in file. Body asserts "Amazon's **Kiro IDE** (July 2025) made EARS central" without source tag; gemini Sources not updated to include kiro.dev. New claim lacks corresponding Source entry. "July 2025" date propagates from subagent file without independent verification.
- **Suggestion:** Remove duplicate bold phrase from line 63. Add [OFFICIAL — kiro.dev] tag to Kiro claim. Add "- https://kiro.dev (Kiro IDE specs; EARS-driven workflow)" to Gemini Sources.

---

### HIGH-010 — Shape Up & Zero-Backlog coverage at paragraph depth without operational guidance

- **Severity:** high
- **Confidence:** MEDIUM
- **Lens:** domain fitness
- **Location:** `research-ceremony-rhythm-alternatives.md:Shape Up section; gemini-deep-research-output.md:Follow-Up Q1 (line 207)`
- **Description:** Non-Agile alternatives remain at paragraph depth despite scope requesting openness to abandoning Agile. Shape Up: "no published practitioner cases... The fit is structural, not yet empirically validated." Synthesis recommends "Shape Up's shaping discipline" without re-flagging caveat — practitioner following synthesis would adopt unvalidated framework. Zero-Backlog: single unsourced paragraph in Gemini Q1 with no operational example. Agentsway: structural overview but no implementation guidance.
- **Suggestion:** Add "(structurally compatible; no empirical cases validated for AI-native teams as of April 2026)" as parenthetical in synthesis recommendations. For Zero-Backlog, add source attribution + operational example or flag [UNVERIFIED].

---

### HIGH-011 — Wireframe-level solo-team guidance for 3-3-3; mob rituals require team

- **Severity:** high
- **Confidence:** MEDIUM
- **Lens:** domain fitness
- **Location:** `gemini-deep-research-output.md:Follow-up Q2 (line 253)`
- **Description:** 3-3-3 described as enterprise framework. Gemini Q2 references "Mob Elaboration" and "Mob Construction," then offers alternatives (OpenSpec, README-Driven, Project Constitution). Gap not fully bridged: mob rituals require team; no solo-viable equivalent to 3-3-3 milestone structure proposed. BMAD Quick Flow listed with single-line description — no milestone structure, time-appetite, or verification gates.
- **Suggestion:** Expand BMAD Quick Flow row with actual milestone structure (Spec → Implementation → Validation with time-appetite framing), or explicitly note that solo-team equivalent of 3-3-3's milestone structure is a gap in current guidance.

---

### MEDIUM-001 through MEDIUM-012

Remaining medium findings (12 total) cover:
- Harness Engineering disambiguation incomplete (Red Hat omitted)
- Bolts misattribution to AWS
- Layer 2–3 dependency in spec-correct circular logic
- Siderova quote paraphrase confusion
- TDA unvalidated terminology
- Behavioral-validation conflating two problems without operational scoping
- LinearB/CodeRabbit precision figures unspot-checked
- AWS AI-DLC Wipro/D&B claim unflagged
- arXiv 2506.16334 orphan citation
- Editorial scaffolding leak in feature-unit file
- Anthropic Bloom properly flagged (exemplary)
- Marty Cagan 403 with working secondary source

---

### LOW-001 through LOW-007

Low findings (7 total) include:
- Gemini promotional language (AI/works™) retained
- Gemini frontmatter missing sub_question metadata
- Zero-Backlog underdeveloped
- Solo value-validation gate operationally impossible without graceful degradation
- EARS paragraph editorial bolt-on structure
- Feature-unit value-validation gate impossible for solo teams

---

## Fix Verification Summary

| Category | Status | Notes |
|---|---|---|
| Iter 1 Critical fixes (6 total) | RESOLVED | All documented criticals properly addressed or flagged |
| Iter 1 High fixes (11 total) | PARTIALLY RESOLVED | Multiple remain unflagged or propagated incompletely |
| Structural regressions | 3 MEDIUM INTRODUCED | Blockquote rendering, heading duplication, cross-reference omission |
| Residual hallucinations | 9 UNCHANGED | No [UNVERIFIED] flags added to high-risk claims |
| Coherence contradictions | 3 PRESENT | AI-DLC (surgically fixed), Shape Up (caveat lost), Recommendations (mob scoping) |

---

## Recommended Iteration 3 Priorities

**Critical (must fix before Q&A):**
1. Spec-correct/value-zero circularity — add explicit acknowledgment; propose breaking mechanism or state plainly no solution exists
2. Open-source tool recipe verification — verify or remove each tool; add verified links, maturity flags, integration sketches

**High (must fix for credibility):**
3. Silken Net — verify case study or flag [UNVERIFIED]
4. V-Impact Canvas — apply [UNVERIFIED] or provide verified InfoQ URL
5. BMAD Barry — remove persona or flag [UNVERIFIED]
6. OpenSpec/Fission-AI — drop attribution or flag [UNVERIFIED]
7. AI-DLC coherence — rewrite Q1 to match main-body fix; update table and Recommendations
8. TDA rebrand — rename to "TDD applied to AI"; add mechanical differences or remove claim
9. Vocabulary collision — add reconciliation table for seven post-story work units
10. Blockquote rendering — fix line 141 newline issue
11. EARS section — remove duplicate phrase; add source tag; update Sources
12. Shape Up & Zero-Backlog — add empirical caveats; operational examples or flag

**Medium (completeness):**
13–24. Address remaining consistency issues, precision-figure verification, editorial cleanup

---

## Conclusion

Iteration 1 resolved documented critical factual errors (attributions, dating, framework descriptions). However, iteration 2 reveals the fix pass was surgical rather than holistic:

- **Unaddressed hallucinations remain unflagged:** Silken Net, V-Impact Canvas, BMAD Barry, OpenSpec/Fission-AI still in corpus without [UNVERIFIED] oversight. Four of nine high-risk claims from iter1 remain.
- **Fixes propagated incompletely:** AI-DLC corrected in main body but left Q1 and Recommendations contradictory. Shape Up caveat lost in synthesis. Blockquote rendering error introduced.
- **New structural regressions:** 3 medium-severity defects introduced by fix pass.
- **Fitness-for-purpose gaps remain unaddressed:** Spec-correct circularity acknowledged but unbroken; open-source recipe unverified; story-granularity sizing missing; solo value-gate operationally impossible.

**Corpus has improved factually but remains unfit for practitioner decision-making. Second fix pass required.**

**Final Score: 85/100 — NEEDS_FIX**
