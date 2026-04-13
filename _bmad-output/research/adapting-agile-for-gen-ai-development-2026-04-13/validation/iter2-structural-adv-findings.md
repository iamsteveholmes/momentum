# Structural Integrity — Adversary Findings (Iteration 2)

**Lens:** Structural Integrity
**Reviewer framing:** Adversary (pattern-aware, holistic)
**Corpus:** 9 files (1 gemini-deep-research output + 8 claude-code-subagent research files)
**Stage:** Iter 2 re-validation after fix pass
**Skepticism level:** 2 (Balanced)

## Summary by severity

- critical: 0
- high: 0
- medium: 3
- low: 2
- Total: 5

## Iter 1 findings — disposition

| Iter 1 ID | Status after fix pass | Notes |
|---|---|---|
| STRUCTURAL-001 (topic field divergence) | RESOLVED | All 8 subagent files now carry the scope.md topic verbatim; gemini already matched. |
| STRUCTURAL-002 (gemini lacks source-origin tags) | PARTIALLY RESOLVED | Tags added to 7 high-stakes claims (Retreat, AI/works, Zones of Intent, AI-DLC, Anthropic skill-erosion, comprehension stat, EARS section). Bulk of body still untagged but specifically targeted high-risk claims now carry provenance — acceptable given fix-log scope. Not re-raised. |
| STRUCTURAL-003 (Forrester provenance contradiction) | RESOLVED | Both files now use `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage; direct Forrester primary URL not verified]`; thought-leader file added an `[UNVERIFIED]` Source entry. Consistent across the corpus. |
| STRUCTURAL-004 (arXiv 2506.16334 cited but not in Sources) | UNRESOLVED | See ITER2-STRUCTURAL-001 below. Not addressed by any fix log. |
| STRUCTURAL-005 (orphan SciTePress source) | UNRESOLVED | Still appears in Sources list line 188 of `research-acceptance-criteria-ai-literal.md` with no body citation. Out of scope of fix logs. |
| STRUCTURAL-006 (orphan arxiv 2512.20798 source) | UNRESOLVED | Still on line 185 of same file with no body citation. Out of scope of fix logs. |
| STRUCTURAL-007 (gemini frontmatter missing scope marker) | UNRESOLVED | No fix attempted; pre-existing structural ambiguity. |
| STRUCTURAL-008 (Shape Up "fit" claims untagged in ceremony file) | UNRESOLVED | Lines 34–40 of `research-ceremony-rhythm-alternatives.md` remain declarative without `[UNVERIFIED]` tags. The empirical-incompleteness admission at line 43 still trails the unhedged claims. |
| STRUCTURAL-009 (no synthesis artifact unifying three goal-gaps) | UNRESOLVED | No new synthesis file. Out of scope of iter 1 fix passes. |
| STRUCTURAL-010 (Red Hat April 2026 article plausibility) | NOT VERIFIED | URL not externally checked; citation remains as-is. Acceptable per benefit-of-doubt. |
| STRUCTURAL-011 (arxiv version-suffix inconsistency) | UNRESOLVED | Cosmetic; out of fix-log scope. |
| STRUCTURAL-012 (back-to-back PRAC/UNVERIFIED tags in one paragraph) | UNRESOLVED | Line 71 of ceremony file unchanged. |
| STRUCTURAL-013 (sub_question quoting drift in spec-correct file) | UNRESOLVED | Line 4 of `research-spec-correct-value-zero.md` still drops the inner single-quotes around 'spec-correct, value-zero'. |

## Did the fixes introduce new structural problems?

Yes — three new structural defects were introduced by the fix-pass edits, and two pre-existing patterns surfaced more clearly under iter-2 re-read. Per skepticism level 2, only those with concrete evidence are filed. Findings below.

---

## Findings

### ITER2-STRUCTURAL-001

- id: ITER2-STRUCTURAL-001
- severity: medium
- dimension: structural_validity
- location: `research-spec-correct-value-zero.md:141`
- description: The new MIT NANDA `[UNVERIFIED]` blockquote was inserted **inline mid-paragraph** rather than as a properly-formatted blockquote line. The `>` character appears mid-line after `[OFFICIAL, bcg.com]`, so it will not render as a blockquote in any markdown renderer. The reader sees a runaway sentence concatenating BCG's claim with the UNVERIFIED warning without visual separation.
- evidence: Line 141 reads in full: `**Treating spec completion as done:** The BCG Widening AI Value Gap report (September 2025) notes that despite tens of billions invested in generative AI, organizations still struggle to connect AI output to measurable business outcomes. [OFFICIAL, bcg.com] > **[UNVERIFIED]** A figure cited as "MIT Project NANDA — 95% of corporate AI projects show no measurable return" appears in secondary sources but could not be traced to a verifiable primary MIT publication. The BCG "Widening AI Value Gap" report (cited above) provides well-sourced evidence for the same point and is preferred.` The `>` is in word-position, not at line start. CommonMark requires `>` at the beginning of a line (after optional leading whitespace) to begin a blockquote. The fix log (`fix-log-spec-correct.md`) describes this as a "Blockquote `[UNVERIFIED]` note" — the intent was a blockquote; the result is not.
- suggestion: Insert a newline before the `>` so the blockquote begins on its own line. Replace the inline `> **[UNVERIFIED]**...` with a paragraph break followed by `\n\n> **[UNVERIFIED]** A figure cited as ...`.

### ITER2-STRUCTURAL-002

- id: ITER2-STRUCTURAL-002
- severity: medium
- dimension: structural_validity
- location: `gemini-deep-research-output.md:61–63`
- description: The new EARS section duplicates its heading. Line 61 is `### EARS Notation and Spec-Driven Tooling` (H3 heading) and line 63's body opens with `**EARS Notation and Spec-Driven Tooling:**` (bold prefix repeating the same phrase). Either the bold opener or the heading is redundant — together they create a structural stutter that no other section in the file exhibits.
- evidence: Lines 61–63 verbatim: `### EARS Notation and Spec-Driven Tooling` then blank then `**EARS Notation and Spec-Driven Tooling:** The subagent research identifies EARS notation...`. Compare to the immediately preceding section `### The Move to 'Super-Specs' and Intent Design` (line 57) whose body opens directly with narrative — no bold-phrase repetition. Compare to `### Encoding Team Standards as Infrastructure` (line 65) — same convention, no doubled phrase. The EARS block is the only `###` section in the file with a duplicated bold phrase opener.
- suggestion: Remove the `**EARS Notation and Spec-Driven Tooling:**` bold prefix from line 63; the H3 heading already announces the topic. Resulting body line begins: `The subagent research identifies EARS notation...`

### ITER2-STRUCTURAL-003

- id: ITER2-STRUCTURAL-003
- severity: medium
- dimension: cross_reference_integrity
- location: `gemini-deep-research-output.md` Sources section (lines 160–173) vs. new EARS body content (line 63)
- description: The newly-added EARS section cites "Amazon's **Kiro IDE** (July 2025)" and points to the subagent file `research-acceptance-criteria-ai-literal.md` for full coverage, but the gemini file's own Sources section was not updated to include any Kiro / kiro.dev URL. The new content thus introduces a body claim (Kiro IDE made EARS central; July 2025 launch date) without a corresponding Source entry within the same file. This regresses the file's already-weak source-coverage and is a fresh cross-reference defect introduced by the fix pass itself.
- evidence: Body line 63 contains the claim with attribution language ("Amazon's **Kiro IDE** (July 2025) made EARS central to its spec-driven workflow"). Sources section (lines 160–173) lists 12 entries; none reference `kiro.dev`, `kiro`, EARS, or Amazon Kiro. Cross-file pointer to `research-acceptance-criteria-ai-literal.md` is provided, but the convention in the corpus is for each file's body claims to be sourced within that file's own Sources list (every subagent file follows this).
- suggestion: Add at minimum `- https://kiro.dev (Kiro IDE specs documentation; EARS-driven workflow)` to gemini Sources, or rephrase line 63 to soften the standalone factual claim ("As documented in `research-acceptance-criteria-ai-literal.md`, Amazon's Kiro IDE...") and explicitly acknowledge in-file that the source is borrowed.

### ITER2-STRUCTURAL-004

- id: ITER2-STRUCTURAL-004
- severity: low
- dimension: cross_reference_integrity
- location: `research-ceremony-rhythm-alternatives.md:201` and Sources section (lines 223–253)
- description: Carry-over of iter 1 STRUCTURAL-004 — the in-text reference `(arXiv, 2506.16334)` for Lean Startup + AI is still present in the body, and the Sources section still does not contain that arxiv ID. No fix pass addressed it. Re-filing at lower severity for explicit iter-2 visibility because the fix-log evidence shows it was not in any fix list.
- evidence: Line 201: `Lean Startup methodology has been studied in combination with AI (arXiv, 2506.16334) but the research focuses on product validation cycles`. Grep across Sources (lines 223–253) for `2506.16334` returns 0 matches. None of the three fix logs (`fix-log-gemini.md`, `fix-log-spec-correct.md`, `fix-log-subagent-files.md`) reference 2506.16334.
- suggestion: Either add `- [arXiv 2506.16334: Lean Startup + AI study]` to the Sources list with a verified URL, or remove the body citation and replace with `[UNVERIFIED]` framing. The current state is identical to iter 1.

### ITER2-STRUCTURAL-005

- id: ITER2-STRUCTURAL-005
- severity: low
- dimension: structural_validity
- location: `research-acceptance-criteria-ai-literal.md:86`
- description: The newly-added ATDD/BDD/Gherkin disambiguation note is correctly formatted as a blockquote, but its content describes ATDD as `Acceptance Test-Driven Development`. Several paragraphs later (line 96), the file refers to "Paul Duvall's ATDD-for-AI framework" — and the Source entry on line 179 is `ATDD-Driven AI Development`. The disambiguation note does not specify whether "ATDD" elsewhere in the file is being used in this canonical sense or in Duvall's usage — these may diverge. No new structural break, but the note's added scope creates a new opportunity for inconsistency that previously didn't exist; without explicit cross-reference the disambiguation may not transfer to the rest of the file's usage.
- evidence: Line 86: `> **Note:** ATDD (Acceptance Test-Driven Development), BDD (Behavior-Driven Development), and Gherkin are related but distinct: ATDD is a test-first discipline; BDD is a collaboration practice for defining behavior in shared language; Gherkin is the DSL (Domain Specific Language) used to write BDD scenarios.` Line 96: `Paul Duvall's ATDD-for-AI framework addresses this by making acceptance tests the **primary specification mechanism**`. Line 179 Sources: `ATDD-Driven AI Development: How Prompting and Tests Steer the Code — Paul Duvall`. The disambiguation note doesn't bridge to whether Duvall's usage matches the canonical definition.
- suggestion: Optional — add a sentence to the note: "Where this file references specific frameworks (e.g., 'ATDD-for-AI'), the framework's own usage applies; the canonical definitions above are baseline." Acceptable to leave unchanged given low severity and benefit-of-doubt.

---

## Re-examination pass

Per skepticism-level-2 protocol, I confirmed:

- All 9 files retain valid frontmatter, title, body, and Sources section after the fix pass.
- The topic-field correction (iter 1 STRUCTURAL-001) landed cleanly across all 8 subagent files with no quoting or formatting damage to surrounding frontmatter fields.
- The gemini file's added disambiguation blockquote (Harness Engineering) is properly formatted as a blockquote (line 32, leading `>`) and renders as intended — that fix landed cleanly.
- The gemini file's new Casey West / AI-DLC / Kinetic Enterprise edits did not orphan headings, break section nesting, or leave dangling section markers. Heading hierarchy is preserved.
- The Anthropic Bloom `[UNVERIFIED]` change in `research-behavioral-validation-ai-agents.md` (line 85 body, line 167 Sources) landed cleanly and is structurally well-formed.
- The new Blind Tester "Known Implementation Gap" blockquote (gemini line 288) is properly formatted with leading `>` and renders correctly.
- The MIT NANDA fix in `research-spec-correct-value-zero.md` (line 141) did NOT land cleanly — see ITER2-STRUCTURAL-001 above. The intended blockquote is structurally inert.
- The new EARS section in gemini introduced a duplicated bold-prefix-after-H3 pattern not seen elsewhere — see ITER2-STRUCTURAL-002.
- The new EARS section cites Kiro IDE without updating the gemini file's Sources list — see ITER2-STRUCTURAL-003.
- iter 1 carry-overs (STRUCTURAL-004, -005, -006, -011, -012, -013) were not in any fix-log scope; one is re-raised at lower severity because it's directly cross-referenced by the new gemini EARS section's tooling family (arxiv references). The remaining are not re-raised — they're known and out of fix-pass scope.

The fix pass substantially improved corpus integrity: all critical/high iter-1 issues are resolved or partially resolved with documented disposition. The defects introduced are all medium-or-lower and confined to formatting (blockquote rendering, heading duplication) plus one cross-reference omission tied to the new EARS additions.
