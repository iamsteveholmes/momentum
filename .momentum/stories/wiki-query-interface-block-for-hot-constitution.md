---
title: Wiki-Query Interface Block for Hot Constitution
story_key: wiki-query-interface-block-for-hot-constitution
status: ready-for-dev
priority: medium
epic_slug: momentum-agent-composition-pipeline
feature_slug: 
story_type: feature
depends_on: []
touches:
  - skills/momentum/skills/constitution-builder/SKILL.md
change_type:
  - specification
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Wiki-Query Interface Block for Hot Constitution

## Story

As a developer,
I want the hot constitution (Tier 1) to include a canonical wiki-query interface block documenting both invocation modes with exact agent syntax, multi-KB selection (DEC-038), and prescriptive trigger scenarios,
so that every agent always knows when and how to query the cold KB without relying on memory or inference.

## Description

The hot constitution is Tier 1 context — it is always loaded for every agent in every session (DEC-001 D1, DEC-008). A wiki-query interface block placed here guarantees that cold-KB query behavior is universally available and consistently applied across all agents, rather than wired per-workflow.

The block must document both wiki-query modes with the exact agent syntax:
- **Normal mode:** `wiki-query [question]` — tiered retrieval (index scan → section grep → full page read), returns cited answers with `[[wikilinks]]`
- **Fast / index-only mode:** `wiki-query quick answer: [question]` — index-only, no page bodies opened; cheaper and faster for factual lookups. Also triggered by the prefix variants `just scan:`, `don't read the pages:`, and `fast lookup:`

The block must also include **prescriptive trigger language** — not permissive "if you need" phrasing, but specific named scenarios where a KB lookup is required before proceeding. The goal is deterministic agent behavior: agents do not decide whether to query, they follow a trigger list (DEC-015 D3).

DEC-018 D2 established this block as Tier 1 (hot constitution) content rather than per-workflow injection. DEC-038 D2 extends the wiki-query interface to support **multiple, per-project KBs**: Momentum agents are project-scoped and draw on Momentum's own KB, distinct from nornspun's. The interface block must therefore make KB selection explicit when more than one KB is available, rather than assuming a single global vault.

This is DEC-018 Phase 2. Phase 1 established the wiki-skills architecture; Phase 2 ensures agents actually use it via Tier 1 hot-context injection.

**Ownership boundary (DEC-038 D1):** This story defines the *interface block* — the shared, project-wide documentation of how to invoke wiki-query and the named scenarios that trigger it. It does NOT define the per-agent **diagnostic table** (observable symptom → exact `wiki-query` lookup), which is owned at the manifesto/agent-builder layer and is per-role×domain. A shared symptom→query routing table is meaningless for a `pm` vs an `architect`; the shared interface block carries only the invocation contract and cross-cutting trigger scenarios, not per-agent routing entries. Keep this consistent with sibling story `constitutionmd-generation-acceptance-criteria` (which asserts the shared constitution contains no per-agent routing) and `constitution-builder-write-mode-parameterization` (which reconciles `constitution-builder`'s current project-shared `## Quick Routing` ownership against the per-agent model).

**Current generator:** Today the only place the wiki-query interface material is authored is `skills/momentum/skills/constitution-builder/SKILL.md` (its "Routing Entry Format (DEC-018)" guidance and Phase 6 routing-entry generation). The standalone hot constitution file (`.claude/guidelines/constitution.md`) and its `build-guidelines` orchestrator do not exist yet (both are backlog). So this story lands the canonical block specification AND updates `constitution-builder` to emit that block (both modes, multi-KB selection, prescriptive triggers) when generating the standalone hot constitution — leaving a single authoritative source the future `build-guidelines` orchestrator can consume.

## Acceptance Criteria

1. The canonical wiki-query interface block is specified as authoritative content for the hot constitution (Tier 1) and is emitted by `constitution-builder/SKILL.md` when it generates the standalone hot constitution. (DEC-018 D2)

2. The block documents **normal mode** with exact syntax `wiki-query [question]`, and states its behavior: tiered retrieval (index scan → section grep → full page read as needed) returning cited answers with `[[wikilinks]]`. (DEC-018 D2)

3. The block documents **fast / index-only mode** with exact syntax `wiki-query quick answer: [question]`, states its behavior (answers from page summaries and index.md only — no page bodies opened; cheaper, good for factual lookups), and lists ALL trigger prefixes: `quick answer:`, `just scan:`, `don't read the pages:`, `fast lookup:`. (DEC-018 D2)

4. The block includes **prescriptive trigger language**: specific named scenarios where a KB lookup is required before proceeding, each written as an imperative naming the exact moment and an exact query string (e.g., "before selecting a test pattern for a new library, run `wiki-query [specific question]`"). No scenario uses permissive "if you need" / "consult the KB if needed" phrasing. (DEC-015 D3)

5. The block accounts for **multiple, per-project KBs** (DEC-038 D2): when more than one KB is available, the syntax and trigger guidance make KB selection explicit (project-scoped KB selection), rather than assuming a single global vault. When exactly one KB is configured, the block degrades to the single-KB form without requiring explicit selection.

6. The block carries ONLY the shared invocation contract and cross-cutting trigger scenarios — it contains NO per-agent diagnostic-table / symptom→query routing entries (those are owned at the manifesto/agent-builder layer per DEC-038 D1). (Consistency check with `constitutionmd-generation-acceptance-criteria` and `constitution-builder-write-mode-parameterization`.)

7. The block is positioned in the constitution such that it is part of always-loaded Tier 1 hot context for every agent that receives the constitution (not behind a conditional or per-workflow wiring). (DEC-018 D2, DEC-001 D1)

8. `constitution-builder/SKILL.md`'s existing "Routing Entry Format (DEC-018)" guidance is reconciled with this block: the two-mode invocation contract and multi-KB selection are described once, authoritatively, and existing references to wiki-query syntax in the skill remain consistent with the canonical block (no contradictory or stale single-KB-only syntax).

9. Invoking `constitution-builder` to (re)generate a constitution produces output that contains the canonical block satisfying ACs 2–7. (Verification: `skill-invoke` — observe the generated constitution material.)

10. Existing sibling stories remain consistent with this addition: `nornspun-agent-constitution-wiki-query-block` consumes the SAME canonical block verbatim, and `constitutionmd-generation-acceptance-criteria` ACs do not conflict with the block's placement or content.

## Tasks / Subtasks

- [ ] **Task 1 — Specify the canonical wiki-query interface block** (AC 1, 2, 3, 4, 5, 6, 7)
  - [ ] Author the canonical block text: both modes with exact syntax, behavior descriptions, and the full trigger-prefix list (`quick answer:`, `just scan:`, `don't read the pages:`, `fast lookup:`).
  - [ ] Write the prescriptive trigger section as imperatives naming exact moments + exact query strings; remove/forbid permissive phrasing.
  - [ ] Add multi-KB selection guidance (DEC-038 D2): explicit project-scoped KB selection when >1 KB is configured; single-KB degrade path.
  - [ ] State the ownership boundary inline: the block holds the invocation contract + cross-cutting triggers only; per-agent symptom→query diagnostic table is excluded (DEC-038 D1).

- [ ] **Task 2 — Emit the canonical block from `constitution-builder/SKILL.md`** (AC 1, 8, 9)
  - [ ] Update `constitution-builder/SKILL.md` so that, when generating the standalone hot constitution, it emits the canonical wiki-query interface block from Task 1 as part of always-loaded Tier 1 content.
  - [ ] Reconcile the existing "Routing Entry Format (DEC-018)" guidance and Phase 6 wiki-query references so the two-mode contract + multi-KB selection are described once and consistently (no stale single-KB-only syntax).

- [ ] **Task 3 — Verify generation via skill invocation** (AC 9)
  - [ ] Invoke `constitution-builder` and confirm the generated constitution contains the canonical block satisfying ACs 2–7 (both modes present with exact syntax, all trigger prefixes, prescriptive triggers, multi-KB selection, no per-agent routing).

- [ ] **Task 4 — Cross-story consistency check** (AC 6, 10)
  - [ ] Confirm `nornspun-agent-constitution-wiki-query-block` references the SAME canonical block (verbatim, not a variant).
  - [ ] Confirm no conflict with `constitutionmd-generation-acceptance-criteria` (shared constitution carries no per-agent routing) or `constitution-builder-write-mode-parameterization`.

## Dev Notes

### Decision Authority

- **DEC-018** (`dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`) — D2 adopts `wiki-query` as the standard Tier 3 cold-KB interface and places its interface specification in the hot constitution (Tier 1), with both modes and exact agent syntax. This story is DEC-018 **Phase 2** ("Constitution update — add wiki-query interface block (both modes, exact syntax) to constitution.md").
- **DEC-038** (`dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`) — D2 extends the wiki-query interface to support **multiple, per-project KBs** and project-scoped agents (multi-KB support requirement on the wiki-query interface, "DEC-018 extended"). D1 fixes the ownership boundary: per-agent **routing/diagnostic table** lives at the manifesto/agent-builder layer, NOT the shared constitution — so the constitution's wiki-query block carries the invocation contract + cross-cutting triggers only.
- **DEC-015 D3** — KB trigger language in the constitution must be **prescriptive, not permissive** (named scenarios with exact query strings; no "consult the KB if needed").
- **DEC-001 D1 / DEC-008** — three-tier model; Tier 1 hot constitution is always loaded by every agent. DEC-018 updates DEC-001 D3 (Tier 3 access mechanism is now `wiki-query`, not manual `grep index.md + read`).

### Current State of Affected Files

- `skills/momentum/skills/constitution-builder/SKILL.md` (exists, ~248 lines) — today the ONLY generator that authors wiki-query interface material.
  - Has a "**Routing Entry Format (DEC-018)**" section documenting `wiki-query [question]` and `wiki-query quick answer: [question]` for routing entries.
  - Phase 6 ("Generate Routing Entries") emits per-concept symptom→`wiki-query` entries into a `## Quick Routing` section of a target SKILL.md.
  - **Tension to resolve (DEC-038 D1):** this skill currently produces a project-*shared* `## Quick Routing` table; DEC-038 says per-agent routing belongs at the manifesto layer. This story does NOT re-home that routing (that is `constitution-builder-write-mode-parameterization`'s job) — it focuses on the **interface block** (invocation contract + cross-cutting triggers + multi-KB selection) that the standalone hot constitution must contain. Keep the skill's wiki-query *syntax* references consistent with the canonical block; coordinate the routing-ownership reconciliation with the sibling story.
  - **What must be preserved:** the existing Permissions / Standing Rules / Quick Routing architecture, the Permission Pattern Syntax section, and the two-mode wiki-query syntax already documented. This story refines/canonicalizes the wiki-query interface description and adds multi-KB selection — it does not delete the existing routing machinery.
- `.claude/guidelines/constitution.md` — **does not exist yet.** The standalone hot constitution file and its `build-guidelines` orchestrator (`build-guidelines-skill` story) are backlog. There is no separate constitution template to edit; the authoritative source for the block is `constitution-builder`. When `build-guidelines` later lands, it consumes this canonical block from `constitution-builder` — do not author a second, divergent copy.

### Architecture Compliance

- Three-tier architecture (DEC-001 / DEC-008): Tier 1 = hot constitution (always loaded), Tier 2 = composed agent file (base body + constitution + manifesto), Tier 3 = cold KB accessed via `wiki-query`. This story strictly targets Tier 1 shared content.
- Ownership boundary (DEC-038 D1): shared constitution = project identity/values/constraints/glossary + the wiki-query **interface** block; per-agent diagnostic table = manifesto layer. Do not introduce per-agent symptom→query entries into the shared block.
- Prescriptive triggers (DEC-015 D3): every trigger names the exact moment and an exact query string.

### Testing Requirements

- **Verification method (advisory): `skill-invoke`** (from `change_type: skill-instruction`; `specification` is subsumed per the routing standard). Drive verification by invoking `constitution-builder` to (re)generate constitution output and observing that the canonical block is emitted and satisfies ACs 2–7.
- For the `skill-instruction` task, EDD applies: write 2–3 behavioral evals under `skills/momentum/skills/constitution-builder/evals/` asserting the generated constitution contains both modes (exact syntax), all four trigger prefixes, prescriptive (non-permissive) triggers, and multi-KB selection — then run them.
- For the `specification` portion (canonical block definition), AVFL validates the block against the upstream decisions (DEC-018 D2, DEC-038 D2, DEC-015 D3) — `document-review`-style cross-reference, no automated driver.
- A static assertion is acceptable as a guard: the emitted block must NOT contain permissive phrasing ("if you need", "consult the KB if needed") and must NOT contain per-agent symptom→query routing rows.

### Project Context Reference

- This story is part of the **momentum-agent-composition-pipeline** epic — the pipeline that produces project-conditioned agent prompts (base body + Tier 1 constitution + Tier 2 manifesto). The epic's value analysis explicitly calls out: "the wiki-query interface block needs to land in the hot constitution."
- Sibling stories in this epic: `constitutionmd-generation-acceptance-criteria` (constitution.md ACs — asserts no per-agent routing in the shared constitution), `constitution-builder-write-mode-parameterization` (reconciles `## Quick Routing` ownership vs. per-agent model), `build-guidelines-skill` (the future orchestrator that generates the standalone constitution), and `nornspun-agent-constitution-wiki-query-block` (consumes the identical canonical block for the nornspun constitution).

### References

- Source decision: `_bmad-output/planning-artifacts/decisions/dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md` (D2 — wiki-query in hot constitution; Phase 2)
- Extending decision: `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` (D2 — multi-KB; D1 — ownership boundary)
- Prescriptive triggers: DEC-015 D3 (folded into `constitutionmd-generation-acceptance-criteria`)
- Generator skill: `skills/momentum/skills/constitution-builder/SKILL.md`
- Related story: `.momentum/stories/build-guidelines-skill.md`
- Related story: `.momentum/stories/constitutionmd-generation-acceptance-criteria.md`
- Related story: `.momentum/stories/constitution-builder-write-mode-parameterization.md`
- Related story: `.momentum/stories/nornspun-agent-constitution-wiki-query-block.md`
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → specification (direct authoring with cross-reference verification — the canonical block definition)
- Task 2 → skill-instruction (EDD — `constitution-builder/SKILL.md` must emit the block)
- Task 3 → skill-instruction (EDD verification via skill invocation)
- Task 4 → specification (cross-story consistency)

A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/wiki-query-interface-block-for-hot-constitution.{ext}`. Before signaling done, read the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Do NOT read the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing changes to the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/constitution-builder/evals/` (the `evals/` dir already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-constitution-emits-wiki-query-block-both-modes.md`, `eval-triggers-are-prescriptive-not-permissive.md`, `eval-multi-kb-selection-explicit.md`).
   - Format each eval as: "Given [the skill is invoked to generate a hot constitution for a project with N KBs], the skill should [emit a wiki-query block containing both modes with exact syntax / all four trigger prefixes / prescriptive imperative triggers / explicit KB selection when N>1 / no per-agent symptom→query rows]."
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Modify `skills/momentum/skills/constitution-builder/SKILL.md` to emit the canonical block (Task 1 content) and reconcile the existing "Routing Entry Format (DEC-018)" wiki-query syntax references.

**Then verify:**
3. Run evals: for each eval file, spawn a subagent (Agent tool). Give it the eval's scenario as its task and load the skill (SKILL.md contents as context, or invoke via Agent Skills name if installed). Observe whether the generated constitution material matches the expected outcome.
4. All evals match → tasks complete. Any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to developer if still failing).

**NFR compliance — mandatory for the skill-instruction task:**
- `constitution-builder` SKILL.md `description` field must remain ≤150 characters (NFR1) — count precisely after edits.
- `model:` and `effort:` frontmatter fields must remain present (model routing per FR23).
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3). Current body is ~248 lines — adding the canonical block guidance should not breach the budget, but verify; move the verbatim block template to `references/` if it does.
- Skill name keeps the `momentum:` namespace prefix (NFR12).

**Additional DoD items for the skill-instruction task:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/constitution-builder/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] `constitution-builder` SKILL.md description ≤150 characters confirmed (count the actual characters after edits)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow to `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented SKILL.md against story ACs)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

The canonical block definition (Task 1) and the cross-story consistency pass (Task 4) are validated by AVFL against their upstream sources (DEC-018 D2, DEC-038 D1/D2, DEC-015 D3) — not by tests or evals. Write directly and verify by inspection:

1. **Author the canonical block** per the ACs — both modes, exact syntax, full trigger-prefix list, prescriptive triggers, multi-KB selection, ownership boundary.
2. **Verify cross-references:** every decision id, story slug, and section name referenced must resolve correctly. Confirm the block's two-mode syntax matches DEC-018 D2 verbatim and the multi-KB language matches DEC-038 D2.
3. **Verify format compliance:** the block follows the constitution's section conventions and is placed as always-loaded Tier 1 content.
4. **Verify consistency:** `nornspun-agent-constitution-wiki-query-block` uses the same canonical block; no conflict with `constitutionmd-generation-acceptance-criteria` or `constitution-builder-write-mode-parameterization`.
5. **Document** what was written in the Dev Agent Record.

**Additional DoD items for the specification tasks:**
- [ ] All cross-references to decisions, stories, and sections resolve correctly
- [ ] Two-mode syntax matches DEC-018 D2; multi-KB language matches DEC-038 D2; triggers are prescriptive per DEC-015 D3
- [ ] No per-agent symptom→query routing in the shared block (DEC-038 D1 boundary holds)
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
