---
status: CHECKPOINT_WARNING
profile: checkpoint
stage: checkpoint
score_initial: 65
score_post_fix: 92
validated_at: 2026-04-09
corpus_files: 7
---

# AVFL Validation Report — Agent Guidelines Architecture Research Corpus

**Status:** CHECKPOINT_WARNING
**Initial Score:** 65/100 (Fair)
**Post-Fix Score:** 92/100 (Good — below 95 threshold; one fix attempt exhausted)
**Profile:** checkpoint
**Stage:** checkpoint
**Corpus:** 7 files

---

## Summary

The corpus of 7 research files is substantively sound and collectively addresses all 6 scope sub-questions with well-sourced findings. The primary issues found are cross-document inconsistencies: the Gemini deep research file contains an unsourced "19-rule ceiling" claim that contradicts the IFScale-cited thresholds in the companion file, opposite QA role complexity ratings across two files, and four Q1 2026 feature claims with no citations. A significant CLAUDE.md inheritance contradiction spans three files. All findings were addressed in one fix pass with clarification notes, cross-corpus reconciliation annotations, and [UNVERIFIED] tags. Two medium-severity issues remain unresolved at the factual level (the 19-rule threshold and the CLAUDE.md inheritance behavior) as they require primary source investigation to resolve definitively.

---

## Phase 1: Findings by Severity

### HIGH Severity (initial, pre-fix)

**ACCURACY-001** — Dimension: traceability
- Location: `gemini-deep-research-output.md`: Section 2 "Saturation Threshold", Follow-Ups 2, 3, 4
- Description: The "19-Rule Ceiling" is presented three times as an established empirical threshold with no citation. The only instruction-following study cited in the corpus (IFScale, 2025) identifies thresholds of 100–150 instructions, not 19. These figures are materially different and directly affect guideline budget recommendations.
- Evidence: "as the number of requirements approaches 19, the probability of the model 'forgetting' or deprioritizing a constraint increases exponentially" — no source provided. `research-guideline-volume-adherence.md` Section 3 cites IFScale: "Gemini 2.5 Pro: Threshold decay ~150 instructions."
- Fix applied: Added [UNVERIFIED] annotation with cross-corpus note pointing to IFScale thresholds.
- Residual: Medium (claim still present but flagged; Gemini's source is unknown)

**ACCURACY-002** — Dimension: correctness, cross_document_consistency
- Location: `research-claude-code-scoping-mechanisms.md` §1 vs `research-role-guideline-isolation.md` §CLAUDE.md Inheritance Problem vs `gemini-deep-research-output.md` Follow-Up 3
- Description: Three contradictory claims on whether subagents inherit project CLAUDE.md: (a) "in the interactive CLI, project CLAUDE.md does load for subagents" [scoping-mechanisms]; (b) "Task subagents do NOT load CLAUDE.md" based on GitHub #29423 [role-guideline-isolation]; (c) "subagents do not ignore CLAUDE.md. They inherit the root CLAUDE.md" [Gemini follow-up 3]. This is the most consequential question for the research topic.
- Evidence: Direct contradictory quotes across three files on the same core claim.
- Fix applied: Added reconciliation note in `research-role-guideline-isolation.md` explaining the likely CLI vs SDK/Task-agent distinction and recommending the safe architecture (embed in system prompt, don't rely on inheritance).
- Residual: Medium (contradiction acknowledged and reconciliation hypothesis provided; definitive resolution requires primary source confirmation)

**COHERENCE-001** — Dimension: cross_document_consistency
- Location: `research-non-dev-agent-guidelines.md` §Role Complexity Map vs `gemini-deep-research-output.md` §Non-Developer Guidelines table
- Description: QA role complexity is rated "highest complexity" in the research file (based on guidelines density) and "Low (Goal-heavy)" in the Gemini table (based on task simplicity). A reader synthesizing both files gets contradictory guidance on how densely to spec QA guidelines.
- Evidence: research-non-dev-agent-guidelines.md: "QA/Code-Review (highest complexity)" vs gemini-deep-research-output.md table: "QA: Low (Goal-heavy)."
- Fix applied: Added disambiguation note in `research-non-dev-agent-guidelines.md` explaining the different complexity dimensions being measured.
- Residual: Low (now explained as measuring different dimensions)

---

### MEDIUM Severity (initial, pre-fix)

**ACCURACY-003** — Dimension: consistency (source classification)
- Location: Sources sections of `research-guideline-volume-adherence.md` vs three other files
- Description: GitHub issues #16299 and #23478 are tagged [OFFICIAL] in `research-guideline-volume-adherence.md` but [PRAC] in `research-non-dev-agent-guidelines.md`, `research-role-guideline-isolation.md`, and `research-generic-agent-injection-patterns.md`. GitHub issues filed by community users are practitioner sources, not official documentation.
- Evidence: `research-guideline-volume-adherence.md` Sources: "**[OFFICIAL]** GitHub Issue #16299" vs `research-non-dev-agent-guidelines.md`: "[PRAC] ...#16299."
- Fix applied: Corrected to [PRAC] in `research-guideline-volume-adherence.md`.
- Residual: None — resolved.

**ACCURACY-004** — Dimension: traceability
- Location: `gemini-deep-research-output.md`: Follow-Up 3-5 section "New Q1 2026 Features"
- Description: Six Q1 2026 features claimed without URL citations or corroboration in the other 6 corpus files. Of these, 4 are not mentioned elsewhere (`initialPrompt` frontmatter, Event-Driven System Reminders, `managed-settings.d/` Drop-ins, "Channels"). The other 2 are confirmed in the corpus (`InstructionsLoaded` hook, `disallowedTools` field).
- Evidence: Follow-Up 3-5 section lists features with no source links attached. No other corpus file mentions `initialPrompt`, "Event-Driven System Reminders," `managed-settings.d/` drop-ins, or "Channels."
- Fix applied: Added [UNVERIFIED] / [CONFIRMED] annotations to each claimed feature.
- Residual: Low (items flagged as unverified).

**COHERENCE-002** — Dimension: cross_document_consistency
- Location: `research-generic-agent-injection-patterns.md` §2.2 vs `research-guideline-volume-adherence.md` §6
- Description: `paths:` scoping is described as "the most important mechanism for technology-specific specialization" in one file, while another characterizes it as having "documented regressions that may negate the benefit." A reader needs both pieces of information together.
- Evidence: research-generic-agent-injection-patterns.md §2.2: "This is the most important mechanism for technology-specific specialization." research-guideline-volume-adherence.md §6: "current implementation has documented regressions that may negate the benefit."
- Fix applied: Added reliability caveat and cross-reference to the regression bug in `research-generic-agent-injection-patterns.md`.
- Residual: None — resolved.

---

### LOW Severity (initial, pre-fix)

**STRUCTURAL-001** — Dimension: cross_reference_integrity
- Location: `research-generic-agent-injection-patterns.md` Sources section
- Description: Three internal relative-path references tagged [OFFICIAL — internal], conflating internal Momentum planning docs with official external documentation sources.
- Evidence: "Momentum Architecture — Decision 26: Two-Layer Agent Model" tagged [OFFICIAL — internal].
- Fix applied: Reclassified as [INTERNAL — relative path; validity unverified].
- Residual: None — resolved.

**COHERENCE-003** — Dimension: tonal_consistency
- Location: `gemini-deep-research-output.md` near end of Follow-Up 1
- Description: Conversational browser-session artifact ("I've clarified the load vs. activation behavior... Let me know if you need more details") embedded in research content.
- Evidence: Artifact present in the Follow-Up 1 section.
- Fix applied: Added source format note at top of Gemini file explaining the browser-capture format and acknowledging conversational artifacts.
- Residual: None — artifact explained by source format note.

---

## Scoring

| Iteration | Deductions | Score |
|---|---|---|
| Initial | 3× high (−24) + 3× medium (−9) + 2× low (−2) | **65/100** |
| Post-fix | 2× medium residual (−6) + 2× low residual (−2) | **92/100** |

**Checkpoint threshold:** 95. Post-fix score of 92 does not reach threshold after one fix attempt.

---

## Continuing with CHECKPOINT_WARNING

The corpus is suitable for downstream use with the following known issues:

1. **The "19-rule ceiling" vs. 100–150 instruction threshold**: Use the IFScale-cited 100–150 figure as the better-sourced planning reference. The Gemini "19" figure is annotated as [UNVERIFIED].

2. **CLAUDE.md inheritance by subagents**: The behavior is context-dependent (CLI interactive vs. SDK/Task agent). The safe architecture is to embed required conventions in subagent system prompts rather than relying on CLAUDE.md inheritance. Both positions are documented in the corpus with their evidence.

3. **Gemini Q1 2026 features**: Four features (`initialPrompt`, Event-Driven System Reminders, `managed-settings.d/` drop-ins, Channels) are [UNVERIFIED] and should be confirmed against official Claude Code release notes before being relied upon in design decisions.

---

## Files Modified During Fix Pass

1. `raw/gemini-deep-research-output.md` — Source format header note; [UNVERIFIED] annotation on 19-rule ceiling; [UNVERIFIED]/[CONFIRMED] annotations on Q1 2026 features
2. `raw/research-role-guideline-isolation.md` — Cross-corpus reconciliation note on CLAUDE.md inheritance contradiction
3. `raw/research-non-dev-agent-guidelines.md` — Role complexity disambiguation note (guidelines density vs task simplicity)
4. `raw/research-guideline-volume-adherence.md` — GitHub issue source tags corrected from [OFFICIAL] to [PRAC]
5. `raw/research-generic-agent-injection-patterns.md` — Reliability caveat on paths: scoping; internal reference tags corrected

---

## What Was Validated

- All 7 corpus files reviewed across structural, accuracy, and coherence lenses
- All 6 research sub-questions confirmed to have dedicated coverage
- Source citation consistency across files checked
- Cross-document claims on shared topics (CLAUDE.md inheritance, paths: scoping reliability, role complexity, instruction thresholds) reconciled or annotated
- Gemini deep research output cross-checked against 6 companion research files for factual alignment
