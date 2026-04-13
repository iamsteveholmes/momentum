# Structural Integrity — Enumerator Findings (Iteration 2)

**Lens:** Structural Integrity
**Reviewer:** ENUMERATOR — systematic, section-by-section
**Skepticism:** Balanced (level 2) — benefit of the doubt on borderline cases
**Artifact stage:** Final
**Iteration:** 2 — post-fix-pass re-validation

## Summary

All priority fixes from iteration 1 landed correctly. The topic field unification is clean across all 9 files. Source-origin tags were applied in the Gemini file. The Harness Engineering disambiguation, EARS section, Blind Tester gap note, MIT NANDA replacement, and leaked editorial note removal are all confirmed. No critical or high findings remain from iteration 1.

Two low-severity residual issues and one new low-severity observation are recorded below. No regressions from the edits were found.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 3 |
| **Total** | **3** |

Files validated: 9
Dimensions: structural_validity, completeness, cross_reference_integrity, corpus_completeness

---

## Fix Verification (Iteration 1 Items)

### topic field unification (was STRUCTURAL-009, plus 8-file sed pass)
**CONFIRMED FIXED.** All 8 subagent files now carry:
`topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"`
This matches `gemini-deep-research-output.md` and scope.md exactly. No inconsistencies remain.

### Gemini: source-origin tags on high-stakes claims (was HIGH-002)
**CONFIRMED FIXED.** Tags present and appropriate:
- `[UNVERIFIED — no primary source URL provided]` on both "2026 Future of Software Development Retreat" references
- `[OFFICIAL — thoughtworks.com]` on AI/works™
- `[OFFICIAL — docs.aws.amazon.com]` on AWS "Zones of Intent" and AI-DLC (Follow-Up Q1)
- `[UNVERIFIED — no primary source URL provided]` on Anthropic skill-erosion research claim
- `[UNVERIFIED — no study citation provided]` on comprehension test statistic

### Gemini: Harness Engineering disambiguation (was CRITICAL-001)
**CONFIRMED FIXED.** Disambiguation blockquote present immediately after the Fowler/Böckeler section: "The term 'Harness Engineering' is also used independently by OpenAI for their agent-workflow operating model. These are distinct uses of the same phrase..."

### Gemini: AI-DLC Mob Contradiction (was CRITICAL-002)
**CONFIRMED FIXED.** The Mob Elaboration/Construction table is attributed solely to Thoughtworks 3-3-3. The AWS AI-DLC is accurately described as Inception/Construction/Operations with human Validators, explicitly distinguished from mob rituals.

### Gemini: Casey West date and characterization (was CRITICAL-003)
**CONFIRMED FIXED.** Both occurrences updated to "2025"; ADLC correctly characterized as a wrapper around SDLC, not a replacement or clean break.

### Gemini: Kinetic Enterprise hallucinated attribution (was CRITICAL-004)
**CONFIRMED FIXED.** `[UNVERIFIED]` blockquote replaces the Deloitte attribution. Deloitte trademark disambiguation included. Conceptual framing bullets retained with appropriate caveat.

### Gemini: EARS section added (was HIGH-004)
**CONFIRMED FIXED.** "EARS Notation and Spec-Driven Tooling" subsection present in the Specification-Completeness Problem section, describing EARS notation, Amazon Kiro IDE, and cross-referencing `research-acceptance-criteria-ai-literal.md`.

### Gemini: Blind Tester gap note (was HIGH-005)
**CONFIRMED FIXED.** "Known Implementation Gap" blockquote present after the Context Truncation / Inferential Sensors bullets in Follow-Up Q3, noting absence of a published open-source concrete pattern.

### research-spec-correct-value-zero.md: MIT NANDA claim (was CRITICAL-005)
**CONFIRMED FIXED.** The bare MIT Project NANDA sentence has been replaced with an `[UNVERIFIED]` blockquote explaining the figure could not be traced to a verifiable primary MIT publication and directing readers to the BCG "Widening AI Value Gap" report as the preferred alternative.

### research-acceptance-criteria-ai-literal.md: ATDD/BDD/Gherkin disambiguation (was HIGH)
**CONFIRMED FIXED.** Blockquote disambiguation note present before the "BDD and Gherkin: Partial Help, Real Risks" section, clearly distinguishing ATDD (test-first discipline), BDD (collaboration practice), and Gherkin (DSL).

### research-acceptance-criteria-ai-literal.md: arxiv tag inconsistency (was STRUCTURAL-006)
**CONFIRMED FIXED.** Both line 12 and line 14 now consistently use `[OFFICIAL — arxiv.org/html/2503.22625v1]`. The `[UNVERIFIED — synthesized]` contradiction is resolved.

### research-behavioral-validation-ai-agents.md: Anthropic Bloom flagged (was HIGH-006)
**CONFIRMED FIXED.** Body text tag changed to `[UNVERIFIED — "Bloom" as an Anthropic open-source behavioral evaluation tool could not be independently verified...]`. Sources section entry annotated `[UNVERIFIED — URL not independently verified; confirm before citing]`.

### research-thought-leader-frameworks-agile-ai.md: Forrester provenance (was HIGH-003)
**CONFIRMED FIXED.** Inline tag reads `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage; direct Forrester primary URL not verified]`. Sources section includes `[Forrester 2025 State of Agile — URL unverified; verify at forrester.com before citing as primary source] [UNVERIFIED]`.

### research-work-granularity-ai-speed.md: Forrester provenance (was HIGH-003)
**CONFIRMED CONSISTENT.** Body line already carried `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]` before the fix pass; remains consistent with the File 1 correction.

### research-ceremony-rhythm-alternatives.md: Harness Engineering disambiguation (was CRITICAL-001)
**CONFIRMED FIXED.** Disambiguation note present as first line after the "Harness Engineering: A Practitioner Model from OpenAI" section heading.

### research-ceremony-rhythm-alternatives.md: Leaked editorial note (was STRUCTURAL-004)
**CONFIRMED FIXED.** The `(**note: original publication is older than two years...**)` scaffolding text has been removed. The Shape Up section now reads cleanly: "...published by Ryan Singer in 2019, has attracted renewed attention in 2025-2026 as an AI-native-compatible framework..."

---

## Residual and New Findings

---

- id: STRUCTURAL-I2-001
- severity: low
- dimension: completeness
- location: `gemini-deep-research-output.md`:frontmatter
- description: The gemini file still lacks a `sub_question` field or equivalent coverage indicator in its frontmatter. STRUCTURAL-002 from iteration 1 flagged this as high; it was not addressed in the fix pass. The fix logs do not mention this finding. The gemini file covers all 8 sub-questions in a synthesized report, but this mapping is absent from the frontmatter, meaning a consumer reading only frontmatter metadata has no structured way to know which sub-questions this file addresses.
- evidence: Current frontmatter (lines 1–6):
  ```
  ---
  content_origin: gemini-deep-research
  date: 2026-04-13
  topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"
  method: claude-in-chrome
  ---
  ```
  No `sub_question` or `sub_questions` field present. Compare with any subagent file (e.g., `research-work-granularity-ai-speed.md` line 4) which includes `sub_question: "How have forward-thinking teams restructured work granularity..."`.
- suggestion: Add `sub_questions: all` to the gemini frontmatter, or `coverage: all-8-sub-questions`. Low severity because the file's H1 title and section headers make its scope self-evident to a human reader; only automated metadata consumers are affected.

---

- id: STRUCTURAL-I2-002
- severity: low
- dimension: completeness
- location: `gemini-deep-research-output.md`:Sources
- description: The Sources section remains at the domain-level citation format (e.g., `https://martinfowler.com (Fragments: February 18; 2025 archive)`) rather than article-level citations. STRUCTURAL-003 from iteration 1 flagged this as high, but it was not addressed in the fix pass. The fix logs do not mention this finding. Inline source citations from the three Follow-up sections are still not consolidated into the main Sources list. This is a carried-forward residual rather than a new issue; severity is downgraded from high to low under balanced skepticism because the inline source citations within each Follow-up section (e.g., `infoq.com/news/2026/02/ai-agile-manifesto-debate`, `sjwiggers.com/2026/02/28/...`) do provide a trail for key claims, and the file is clearly labeled as a gemini synthesis rather than subagent research.
- evidence: Sources section (lines 160–172) shows 12 entries of the form `- https://[domain] (parenthetical note)` with no article titles, authors, or direct article URLs. Follow-Up Q3 ends with `**Sources:** infoq.com/news/2026/02/ai-agile-manifesto-debate, sjwiggers.com/2026/02/28/ai-is-reshaping-software-development` — inline, not consolidated.
- suggestion: Expand the Sources section to list specific article titles and direct article URLs for at least the highest-stakes claims (Thoughtworks 3-3-3, AWS AI-DLC, Casey West ADLC, Fowler Harness Engineering). Consolidate inline Follow-up sources into the main list. Even partial expansion is useful for fact-checking.

---

- id: STRUCTURAL-I2-003
- severity: low
- dimension: corpus_completeness
- location: corpus-wide
- description: STRUCTURAL-012 (institutional Agile community coverage gap: SAFe, LeSS, Agile Alliance) and STRUCTURAL-013 (spec-volume side of cognitive load inversion) from iteration 1 were not addressed in the fix pass and are carried forward. Both are low-severity gaps that represent content expansion suggestions rather than errors. No regression; the scope coverage mapping remains intact (all 8 sub-questions have dedicated files). These are recorded here for tracking continuity rather than as new findings requiring immediate action.
- evidence: Corpus-wide search confirms SAFe (Scaled Agile Framework) is mentioned zero times across all 9 files. The Agile Alliance is mentioned zero times. LeSS is mentioned zero times. `research-cognitive-load-inversion.md` continues to address the code-review overload side of cognitive load inversion comprehensively but does not address AI-generated specification volume as a separate overload source — the word "specification" appears primarily as a solution (review specs instead of code), not as a second source of overload.
- suggestion: These are content-enrichment gaps, not errors. Consider adding a brief section to `research-cognitive-load-inversion.md` addressing AI-generated spec volume. Consider a SAFe/Agile Alliance addendum to `research-thought-leader-frameworks-agile-ai.md` if the corpus is used for enterprise-facing outputs.

---

## Corpus Completeness Check

Sub-question coverage mapping (post-fix-pass):

| Sub-question | Primary file | Status |
|---|---|---|
| 1 — Thought-leader frameworks (Thoughtworks, Fowler, Agile community) | research-thought-leader-frameworks-agile-ai.md | Covered. Institutional Agile gap (SAFe/LeSS) noted as low-severity in STRUCTURAL-I2-003 |
| 2 — Work granularity at AI speed | research-work-granularity-ai-speed.md | Fully covered |
| 3 — AC replacement for AI literal implementation | research-acceptance-criteria-ai-literal.md | Fully covered |
| 4 — Spec-correct, value-zero problem | research-spec-correct-value-zero.md | Fully covered |
| 5 — Feature as unit of user value | research-feature-unit-user-value.md | Fully covered |
| 6 — Behavioral validation and E2E testing | research-behavioral-validation-ai-agents.md | Fully covered |
| 7 — Cognitive load inversion | research-cognitive-load-inversion.md | Covered. Spec-volume gap noted in STRUCTURAL-I2-003 |
| 8 — Ceremony and rhythm alternatives | research-ceremony-rhythm-alternatives.md | Fully covered |

No sub-question is unaddressed. All 8 have primary dedicated files with substantial coverage.

---

## Structural Completeness Check

All 9 files confirmed to have:
- YAML frontmatter
- H1 title
- Summary or overview section
- Substantive body sections
- Synthesis or conclusions section
- Sources section

No required section is missing from any file.

---

## Cross-Reference Integrity

No inter-file cross-references found in the corpus (files do not link to each other by filename or section anchor, with the exception of the Gemini EARS section cross-reference to `research-acceptance-criteria-ai-literal.md`, which is accurate and appropriate). External source URL integrity issues carried from iteration 1 (STRUCTURAL-010, STRUCTURAL-011, STRUCTURAL-014) were not re-examined as URL resolution falls outside structural validation scope and was not targeted by the fix pass.
