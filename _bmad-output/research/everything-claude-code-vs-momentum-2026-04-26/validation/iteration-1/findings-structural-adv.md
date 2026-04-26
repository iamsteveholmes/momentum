# AVFL Structural Integrity Findings — Adversary Reviewer

**Lens:** Structural Integrity | **Framing:** Adversary | **Skepticism:** 3 (aggressive) | **Stage:** final | **Corpus:** true (9 files) | **Domain expert:** research analyst

Holistic, pattern-aware scan across all 9 corpus files. Findings are limited to the Structural Integrity lens dimensions: `structural_validity`, `completeness`, `cross_reference_integrity`, and the corpus-only `corpus_completeness`. Cross-document numerical inconsistencies and tonal/voice issues belong to Coherence & Craft and are not flagged here even when adjacent.

---

## STRUCTURAL-001

- **severity:** medium
- **dimension:** structural_validity
- **location:** `research-philosophy.md:top` and `research-portability.md:top`
- **description:** Two research files omit the level-1 (H1) document title that all other research files use as their first heading after the YAML frontmatter. Every other `research-*.md` in the corpus opens with a single `# {Title}` immediately after the closing `---` of frontmatter. `research-philosophy.md` and `research-portability.md` jump directly from frontmatter to `## Inline Summary` with no H1.
- **evidence:**
  - `research-philosophy.md` line 7 closes frontmatter, line 9 begins `## Inline Summary` — no H1 between.
  - `research-portability.md` line 7 closes frontmatter, line 9 begins `## Inline Summary` — no H1 between.
  - Compare: `research-architecture-capabilities.md:8` = `# Architecture & Capabilities of ...`; `research-ecc-superior.md:8` = `# ECC vs Momentum — Where ECC Leads`; `research-feature-parallels.md:8` = `# Feature Parallels — ...`; `research-integration-assessment.md:8` = `# Integration Assessment — ...`; `research-maturity-community.md:8` = `# Maturity & Community Signals: ...`; `research-momentum-superior.md:8` = `# Where Momentum is Superior to ECC ...`.
- **suggestion:** Add H1 titles consistent with the pattern: in `research-philosophy.md`, insert `# Design Philosophy Comparison — ECC vs Momentum`; in `research-portability.md`, insert `# Portability Across Agentic CLIs — ECC vs Momentum`. Place each immediately after frontmatter and before `## Inline Summary`.

## STRUCTURAL-002

- **severity:** medium
- **dimension:** structural_validity
- **location:** `gemini-deep-research-output.md:end-of-file`
- **description:** The Gemini file is the only corpus file lacking a `## Sources` section. All eight `research-*.md` subagent files end with `## Sources`. The Gemini file ends with `## Follow-Up #3 — Directory structure verification (skipped)` and contains no sources block, breaking the corpus's documented closing-section convention.
- **evidence:**
  - `grep -c "^## Sources"` returns 1 for each of the eight `research-*.md` files; returns 0 for `gemini-deep-research-output.md`.
  - Final heading in `gemini-deep-research-output.md` is `## Follow-Up #3 — Directory structure verification (skipped)`.
  - Frontmatter declares `source_url: https://gemini.google.com/app/86668a7bd7fdd717` but no Sources section enumerates the inline citations Gemini produced (Gemini cites forgecode.dev, github.com/tailcallhq/forgecode, github.com/sst/opencode, github.com/mark-hingston/opencode-workflows, github.com/maximhq/bifrost throughout the prose with no consolidated list).
- **suggestion:** Add a `## Sources` section to `gemini-deep-research-output.md` listing the Gemini chat URL plus the URLs Gemini cited inline. If Gemini's output didn't provide a consolidated source list, add a top-of-file note explicitly stating "Sources: see frontmatter `source_url` and inline mentions; Gemini's output did not provide a consolidated source list."

## STRUCTURAL-003

- **severity:** high
- **dimension:** structural_validity
- **location:** `gemini-deep-research-output.md:top`
- **description:** The Gemini file is included as a corpus document but contains no top-level structural signal that its body has been disputed/superseded by the eight subagent files. The "Orchestrator note" admitting Gemini sidestepped verification is buried mid-document at the end of `## Follow-Up #1`. A downstream consumer reading only this file would treat its body claims (140K stars, 113 contributors, 1,282 tests, AgentShield bundled inside ECC, Anthropic x Forum Ventures hackathon, claude-mem at 89K stars, "qflow MCP server" with 7-state machine, ECC ships TypeScript/Jest tests, "14 MCP integrations") as authoritative. The structural framing fails to signal that the document's role in the corpus is "disputed raw input," not "research finding."
- **evidence:**
  - Body lines 11–383 make confident factual claims with no annotation of dispute. E.g., line 11 "over 140,000 GitHub stars and 21,000 forks" (actual is 167,488 / 25,969 per `research-architecture-capabilities.md` lines 41–44); line 79 "currently boasting 113 contributors and over 768 commits" (actual 159 / ~1,465 per `research-maturity-community.md` lines 83–84, 139); line 60 "Proprietary security scanning engine with over 1,282 automated tests" in a table row attributing AgentShield to ECC's `tools/agentshield/` directory — `research-integration-assessment.md` lines 28–30 explicitly verifies "AgentShield is **not** part of ECC — it is a sibling project at `affaan-m/agentshield`"; line 75 "winner of the Anthropic x Forum Ventures hackathon in late 2025" — `research-maturity-community.md` lines 270–271 corrects: "Cerebral Valley × Anthropic ... Feb 10–16, 2026. Forum Ventures was not the partner."
  - The only correction signal is line 424: `**Orchestrator note:** Gemini did NOT verify the ECC numbers in this follow-up. ... This strongly suggests the original ECC numbers may be hallucinated. Subagents in Phase 2 must verify against the live GitHub repo.` — placed inside Follow-Up #1, ~424 lines into the file, not at file top.
  - Frontmatter (lines 1–7) declares `content_origin: gemini-deep-research` but does not flag disputed status with a `disputed: true` field or equivalent.
- **suggestion:** Add a prominent top-of-file callout immediately after frontmatter, before the H1, e.g.:
  > **STATUS — DISPUTED INPUT:** This file is the raw Gemini Deep Research output preserved for triangulation. Subagent files in this corpus verified its claims against the live `affaan-m/everything-claude-code` repo and found multiple factual inaccuracies (star/contributor/commit/test counts, hackathon sponsor, AgentShield attribution, claude-mem star count, qflow integration, language stack). Treat the body as a starting hypothesis; defer to the subagent files (`research-architecture-capabilities.md`, `research-maturity-community.md`, `research-feature-parallels.md`, `research-integration-assessment.md`) for verified claims.

  Alternatively, add `disputed: true` to frontmatter and document the convention in `scope.md` or a corpus README.

## STRUCTURAL-004

- **severity:** low
- **dimension:** structural_validity
- **location:** `raw/` directory listing — `gemini-prompt.md`
- **description:** The `raw/` directory contains 10 files, not 9. The corpus task and validation parameters specify 9 corpus files. The 10th file, `gemini-prompt.md`, is the prompt sent to Gemini — structurally a different artifact (input prompt, not research output) — but its co-location in `raw/` creates ambiguity about what is and isn't part of the corpus. There is no manifest in the research directory naming canonical corpus members.
- **evidence:**
  - `ls _bmad-output/research/everything-claude-code-vs-momentum-2026-04-26/raw/` returns 10 entries.
  - Validation parameters explicitly enumerate 9 corpus files (numbered 1–9 in the task spec).
  - `gemini-prompt.md` has no YAML frontmatter and no `## Sources` section, structurally distinguishing it from corpus members.
- **suggestion:** Either move `gemini-prompt.md` to a sibling directory (e.g., `raw/inputs/`) so `raw/` contains only research outputs, or add a small `raw/README.md` enumerating which files are corpus members and which are reference/staging.

## STRUCTURAL-005

- **severity:** low
- **dimension:** completeness
- **location:** `gemini-deep-research-output.md:Follow-Up #3`
- **description:** "Follow-Up #3 — Directory structure verification (skipped)" announces the question, names the disposition, but provides no content. Per the `final` stage rule, "All required sections must be present and complete." The cross-reference is real (the subagent file does cover this), but the section as authored leaves a `## Follow-Up #3` heading whose body is a single sentence of meta-commentary rather than directory data.
- **evidence:** `gemini-deep-research-output.md` "## Follow-Up #3" section contains only a Question and Disposition sentence; no directory listing.
- **suggestion:** Either remove the `## Follow-Up #3` heading entirely and fold the disposition into the end of `## Follow-Up #2`, or convert the disposition into an explicit cross-reference: `See **research-architecture-capabilities.md → "Directory Layout (Top Level)"** for the verified directory structure.`

---

## Re-examination notes (skepticism 3 — Adversary)

Re-examined Adversary hunches before reporting. Cleared on:

- **`corpus_completeness` — all 8 sub-questions covered.** SQ1→architecture-capabilities, SQ2→maturity-community, SQ3→feature-parallels, SQ4→ecc-superior, SQ5→momentum-superior, SQ6→portability, SQ7→philosophy, SQ8→integration-assessment. No sub-question shallow or tangential. Clean.
- **`cross_reference_integrity` — Momentum decisions cited.** Verified Decision 26, 30, 35, 3d are real in `skills/momentum/skills/architecture-guard/SKILL.md`. Clean.
- **`cross_reference_integrity` — Momentum file paths.** Spot-verified: `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/specs/triage-skill.feature` exists; `skills/momentum/references/gherkin-template.md` exists; `skills/momentum/skills/avfl/SKILL.md` exists; `skills/momentum/.claude-plugin/plugin.json` confirms `version: 0.17.0`. Clean.
- **`cross_reference_integrity` — Apache-2.0 claim.** Verified `LICENSE` exists and `README.md:398` confirms Apache-2.0. Clean.
- **`structural_validity` — frontmatter consistency.** All 8 `research-*.md` use identical schema. Clean.

**Out of lens scope (noted, not flagged for this lens):** cross-document numerical inconsistencies (Momentum skill count 25/26, ECC star count 167,487/167,488, MCP server count 14/17/20/24+, ECC agent count 30/38/47/48, etc.) — these belong to Coherence & Craft (`cross_document_consistency`), not Structural Integrity.

---

## Summary

5 findings: 1 high (STRUCTURAL-003 — Gemini file lacks disputed-status header at top), 2 medium (STRUCTURAL-001 two files missing H1 titles, STRUCTURAL-002 Gemini file missing `## Sources`), 2 low (STRUCTURAL-004 raw/ contains a non-corpus prompt file with no manifest, STRUCTURAL-005 stub Follow-Up #3 heading with no content). Sub-question coverage is complete; cross-references spot-checked clean; per-research-file frontmatter is consistent.
