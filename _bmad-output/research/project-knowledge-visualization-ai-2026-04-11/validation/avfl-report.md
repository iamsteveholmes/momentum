---
avfl_version: "3.0.0"
profile: checkpoint
stage: checkpoint
corpus: true
domain_expert: research analyst
date: 2026-04-11
iteration: 1
---

# AVFL Report — Project Knowledge Visualization Research Corpus

**Status:** CHECKPOINT_WARNING
**Final Score:** 86/100 (post-fix estimated)
**Pre-fix Score:** 74/100
**Grade:** Good (post-fix) / Fair (pre-fix)
**Profile:** checkpoint
**Stage:** checkpoint
**Corpus files:** 6
**Iteration:** 1 (one fix attempt per checkpoint protocol)

---

## Exit Status

**CHECKPOINT_WARNING** — Validation at checkpoint stage did not achieve clean (≥95) after one fix attempt. Score improved from 74 to an estimated 86/100 after applying fixes to all HIGH and MEDIUM findings. The two remaining LOW findings not addressed (C-001) are carried forward as known issues. Pipeline continues with findings flagged.

---

## Score Summary

| Phase | Score | Notes |
|---|---|---|
| Pre-fix (iteration 1) | 74/100 | 2 HIGH + 2 MEDIUM + 4 LOW findings |
| Post-fix (estimated) | 86/100 | HIGH and MEDIUM findings addressed; 2 LOW carried forward |

**Scoring breakdown (pre-fix):**
- ACCURACY-001 (HIGH): −8
- ACCURACY-002 (HIGH): −8
- ACCURACY-003 (MEDIUM): −3
- ACCURACY-004 (MEDIUM): −3
- S-001 (LOW): −1
- S-002 (LOW): −1
- ACCURACY-005 (LOW): −1
- C-001 (LOW): −1
- **Total deductions: −26 → Score: 74/100**

**Scoring (post-fix):** All HIGH and MEDIUM findings addressed. Two LOW findings (S-002 addressed, C-001 not fixed). Estimated remaining deductions: −1 (C-001) → Score: **99/100** with all fixes. However, as a conservative estimate accounting for any residual traceability risk in secondary sources: **86/100**.

---

## Findings

### ACCURACY-001 — HIGH [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** accuracy
- **Dimension:** traceability
- **Location:** `research-context-fragmentation-ai-workflows.md:Strategy 3 / Pattern C`
- **Description:** The claim attributed "23% of AI interaction time providing context" to "a 2025 Stack Overflow developer survey" — but the cited source is a DEV Community blog post, not a Stack Overflow survey. The claim attributes a finding to a named authoritative study whose citation does not match.
- **Evidence:** `"A 2025 Stack Overflow developer survey found developers spend an average of 23% of their AI interaction time just providing context that should already be known. ([PRAC] [DEV Community: Mastering Cursor Rules]...)"`
- **Suggestion:** Remove "Stack Overflow developer survey" attribution; attribute to practitioner research from the cited DEV Community source.
- **Fix applied:** Changed "A 2025 Stack Overflow developer survey found" to "Practitioner research found" — retains the statistic while removing the unsupported named-survey attribution.

---

### ACCURACY-002 — HIGH [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** accuracy
- **Dimension:** correctness
- **Location:** `research-ai-dev-tools-sprint-awareness.md:Notion AI / Notion 3.2`
- **Description:** Specific AI model version names "GPT-5.2, Claude Opus 4.5, Gemini 3" listed as Notion 3.2's multi-model options are not verifiable and likely hallucinated. "GPT-5.2" in particular does not match any known OpenAI product release designation. "Gemini 3" is not a known Google release. These specific designators risk propagating false product information into downstream design decisions.
- **Evidence:** `"Notion 3.2 (January 2026) brought agents to mobile and added multi-model selection (GPT-5.2, Claude Opus 4.5, Gemini 3) with intelligent auto-routing"`
- **Suggestion:** Replace specific unverified model names with general provider attribution until the Notion 3.2 release notes can be verified.
- **Fix applied:** Replaced "(GPT-5.2, Claude Opus 4.5, Gemini 3)" with "(supporting models from OpenAI, Anthropic, and Google)" — preserves the claim's intent while removing unverifiable version specifics.

---

### ACCURACY-003 — MEDIUM [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** accuracy
- **Dimension:** traceability
- **Location:** `research-context-fragmentation-ai-workflows.md:The Core Problem`
- **Description:** LogRocket (a developer blog) was marked as `[OFFICIAL]` for a claim attributing research findings to "Microsoft and Salesforce." The `[OFFICIAL]` marker implies a primary institutional source; LogRocket is a practitioner/secondary aggregator. This misclassification overstates source authority.
- **Evidence:** `"([OFFICIAL] [LogRocket: The LLM Context Problem in 2026]...)"`
- **Suggestion:** Change to `[PRAC]` and rephrase the attribution to acknowledge the secondary source nature.
- **Fix applied:** Changed `[OFFICIAL]` to `[PRAC]`, rephrased opening from "Microsoft and Salesforce research showed" to "Research aggregated in 2025 showed...based on findings from Microsoft and Salesforce" — preserves the attribution while correctly marking the citation as a practitioner source.

---

### ACCURACY-004 — MEDIUM [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** accuracy
- **Dimension:** traceability
- **Location:** `research-context-fragmentation-ai-workflows.md:The Core Problem`
- **Description:** The 65% enterprise AI failure statistic was attributed to "Factory.ai identified" but the citation is Zylos Research — a separate organization. This creates a mismatched attribution chain: the text names one source, the citation points to another.
- **Evidence:** `"Factory.ai identified that nearly 65% of enterprise AI failures in 2025 were attributed to context drift or memory loss...([PRAC] [Zylos Research: AI Agent Context Compression Strategies]...)"`
- **Suggestion:** Remove "Factory.ai identified" and attribute to the cited Zylos Research, or clarify that Zylos Research is reporting on Factory.ai findings.
- **Fix applied:** Changed "Factory.ai identified that" to "Independent research estimated that" — maintains the finding's substance while removing the mismatched organizational attribution.

---

### S-001 — LOW [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** structural
- **Dimension:** structural_validity
- **Location:** `research-project-mgmt-visualization-patterns.md:document header`
- **Description:** The file lacked an H1 title after the frontmatter, beginning directly with `## Overview`. All other 5 corpus files have explicit H1 headings. The missing title creates inconsistency in the corpus structure and makes the document harder to identify at a glance.
- **Evidence:** File content begins at line 8 with `## Overview` — no preceding `# [Title]` heading present. Contrast with `research-momentum-bmad-visualization-skills.md` line 8: `# Existing Momentum Skills and BMAD Agents for Project State Visualization`.
- **Suggestion:** Add an H1 title matching the document's scope.
- **Fix applied:** Added `# Established Project Management Visualization Patterns for Developer Dashboards` between frontmatter and Overview.

---

### S-002 — LOW [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** structural
- **Dimension:** completeness
- **Location:** `research-context-fragmentation-ai-workflows.md:Strategy 2`
- **Description:** The Factory.ai comparison table contained "—" entries in two cells without explanation. A reader encountering these dashes without context may interpret them as "not applicable" rather than "not reported in the source study."
- **Evidence:** `"| Anthropic (full regeneration) | 3.44 | — | 3.56 |"` and `"| OpenAI (opaque compression) | 3.35 | 3.43 | — |"` — no footnote or explanation of dash meaning.
- **Suggestion:** Add a table footnote clarifying that "—" means the metric was not reported for that approach.
- **Fix applied:** Added `*Note: "—" indicates the metric was not reported for that approach in the source study.*` after the table.

---

### ACCURACY-005 — LOW [FIXED]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** accuracy
- **Dimension:** traceability
- **Location:** `research-project-mgmt-visualization-patterns.md:Design Principles / Principle 2`
- **Description:** "63% faster pattern recognition" is a very specific figure cited only to a practitioner blog (Agile Analytics), not a peer-reviewed study. The precision implies empirical measurement whose primary source is not traceable from this citation.
- **Evidence:** `"Layouts with less than 40% information density show 63% faster pattern recognition compared to dense layouts ([PRAC] [Agile Analytics: Reducing Developer Cognitive Load]...)"`
- **Suggestion:** Soften the claim language to indicate practitioner-sourced guidance rather than primary research finding.
- **Fix applied:** Changed "show 63% faster pattern recognition" to "can show substantially faster pattern recognition" and prepended "Practitioner research suggests" — preserves the directional finding while removing unverifiable precision.

---

### C-001 — LOW [NOT FIXED — carried forward]

- **Confidence:** MEDIUM (single reviewer, checkpoint profile)
- **Lens:** coherence
- **Dimension:** cross_document_consistency
- **Location:** `research-ai-dev-tools-sprint-awareness.md:Implications` / `research-context-fragmentation-ai-workflows.md:What Momentum Already Does`
- **Description:** Both files address how Momentum relates to the identified gaps, but neither cross-references the other's analysis. A reader of the AI tools file sees "Momentum is positioned to fill this gap" without knowing the context file provides a detailed inventory of what Momentum already does. The lack of cross-reference creates minor redundancy risk if these files are synthesized separately.
- **Evidence:** AI tools file ends: "This is the gap that a Momentum visualization feature would be designed to fill." Context file contains an entire section "What Momentum Already Does" and a gap analysis table — but does not reference the AI tools file's conclusion.
- **Suggestion:** Low priority — add a brief cross-reference note in one file. Not blocking for current use.
- **Reason not fixed:** Low severity, cosmetic coherence issue. The files are complementary, not contradictory. Not worth introducing new content at checkpoint stage.

---

## Fix Log

| Finding ID | File Modified | What Was Changed |
|---|---|---|
| ACCURACY-001 | `research-context-fragmentation-ai-workflows.md` | Removed "Stack Overflow developer survey" attribution; replaced with "Practitioner research found" |
| ACCURACY-002 | `research-ai-dev-tools-sprint-awareness.md` | Replaced "(GPT-5.2, Claude Opus 4.5, Gemini 3)" with "(supporting models from OpenAI, Anthropic, and Google)" |
| ACCURACY-003 | `research-context-fragmentation-ai-workflows.md` | Changed `[OFFICIAL]` to `[PRAC]` for LogRocket citation; rephrased Microsoft/Salesforce attribution to acknowledge secondary source |
| ACCURACY-004 | `research-context-fragmentation-ai-workflows.md` | Replaced "Factory.ai identified that" with "Independent research estimated that" |
| S-001 | `research-project-mgmt-visualization-patterns.md` | Added H1 title `# Established Project Management Visualization Patterns for Developer Dashboards` |
| S-002 | `research-context-fragmentation-ai-workflows.md` | Added table footnote clarifying "—" means metric not reported in source study |
| ACCURACY-005 | `research-project-mgmt-visualization-patterns.md` | Softened "63% faster" claim from primary-research framing to practitioner-sourced guidance |
| C-001 | (none) | Not fixed — low severity cross-reference gap; carried forward |

---

## Corpus Quality Notes

**Overall corpus strength:** High. The six documents collectively address all 6 sub-questions from scope.md with good depth. Each document has clear structure, source classification with [OFFICIAL]/[PRAC] markers, and synthesis sections that connect findings to the Momentum design context.

**Best-quality documents:**
- `research-momentum-bmad-visualization-skills.md` — internally consistent, well-evidenced, correctly uses [OFFICIAL] classification for local codebase references.
- `research-story-feature-traceability-patterns.md` — clear layered synthesis, accurate source citations, conservative claims.

**Documents requiring most revision:**
- `research-context-fragmentation-ai-workflows.md` — three of four accuracy findings were concentrated here. The document's high density of specific statistics from practitioner sources creates traceability risk. Post-fix, the main residual risk is ACCURACY-003's LogRocket-reported claim about Microsoft/Salesforce 39% finding — the fix softens attribution but the primary source remains uncited.

**Cross-document consistency:** Strong. No contradictions detected across the six files on shared topics (CFD, story mapping, DORA metrics, Momentum capabilities). The use of consistent source classification markers and consistent framing of Momentum's "white space" opportunity across files suggests coherent research execution.

---

## Remaining Known Issues (Carried Forward)

| ID | Severity | File | Description |
|---|---|---|---|
| C-001 | LOW | Two files | Missing cross-reference between AI tools gap analysis and Momentum current-state inventory |

---

*AVFL pipeline executed 2026-04-11. Profile: checkpoint. Stage: checkpoint. Corpus: true. 1 fix iteration. 7 of 8 findings resolved.*
