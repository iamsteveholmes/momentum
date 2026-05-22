---
title: Remove momentum:distill Skill
story_key: remove-momentum-distill
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
priority: high
change_type:
  - skill-instruction
  - config-structure
verification_method:
  - EDD eval (skill-instruction tasks — retro, triage, impetus)
  - inspection (config-structure tasks — plugin.json, settings.local.json)
harness_profile: default
depends_on: []
touches:
  - skills/momentum/skills/distill/
  - skills/momentum/.claude-plugin/plugin.json
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/triage/workflow.md
  - skills/momentum/skills/triage/SKILL.md
  - skills/momentum/skills/triage/evals/eval-triage-classifies-six-classes.md
  - skills/momentum/skills/impetus/references/dispatch.md
  - skills/momentum/skills/impetus/references/partner.md
  - skills/momentum/skills/feature-status/evals/eval-practice-path-topology-shows-handoffs.md
  - .claude/settings.local.json
---

# Remove momentum:distill Skill

Status: ready-for-dev

## Story

As the Momentum practice operator,
I want `momentum:distill` removed entirely from the plugin and all call sites cleaned up,
so that the two-lane model (ordinary sprint stories built with skill-creator / agent-builder / constitution-builder, or momentum:quick-fix when urgent) is the sole path for applying practice fixes, and no dead skill route creates confusion or blocks forward progress.

## Description

**Decision class.** DEC-031 D6 — Legibility-Before-Automation, Canvas Gate Surface, Pipeline Restructure, Dispatcher Sequencing. Decision document: `_bmad-output/planning-artifacts/decisions/dec-031-legibility-before-automation-canvas-gate-surface-2026-05-20.md`.

**What is being removed.** `momentum:distill` is a skill that was designed to immediately apply a session learning or retro Tier 1 finding to the appropriate rule, reference, or skill prompt. It was invoked from retro Phase 5 (Tier 1 routing) and from `momentum:triage` (DISTILL class delegation). DEC-031 D6 retires it: practice fixes (skills, rules, hooks, agents) are now ordinary sprint stories built with skill-creator / agent-builder / constitution-builder, or momentum:quick-fix when urgent. Distill is redundant with that two-lane model and has been blocking forward progress with heavy human intervention for un-deduped output.

**Scope of changes:**

1. **Delete `skills/momentum/skills/distill/`** — the entire directory including SKILL.md, workflow.md, and the `evals/` subdirectory (3 eval files).

2. **Update `skills/momentum/.claude-plugin/plugin.json`** — there is no distill skill registration entry in plugin.json (the file contains only name, version, description, author). The only real work here is bumping the version from 0.22.0 → 0.23.0 per version-on-release rule.

3. **Remove distill invocation from `skills/momentum/skills/retro/workflow.md` Phase 5** — Phase 5 (lines 488–601) has substantial distill-specific logic: Tier classification, `{{distill_candidates}}`, inline `momentum:distill` spawn, `{{distilled_dispositions}}`, output referencing distill counts. Remove this routing entirely. All findings route to stub creation (the existing Tier 2 path). Phase 5's step goal should be simplified to "Propose and approve story stubs from audit findings". Phase 5.5 (handoff to intake-queue) has a minor reference at line 629 ("Findings already routed to distill (Phase 5 Tier 1) — those are applied or staged") — remove that note. Phase 5.5 line 646 contains "either stubbed or distilled" — remove "or distilled", leaving only "stubbed".

4. **Clean up distill references in `skills/momentum/skills/triage/`** — `triage/SKILL.md` description mentions `distill`. `triage/workflow.md` has 9 distill references at lines 9, 23, 36, 149, 211, 216, 217, 272, 273: the DISTILL class in the six-class table, delegation logic, result tracking. Remove DISTILL as a routing class — triage now routes: ARTIFACT → `momentum:intake`, DECISION → `momentum:decision`, queue → intake-queue append. Remove DISTILL entirely.

5. **Clean up distill references in impetus references** — `dispatch.md` line 29 routes "Apply a retro finding to rules, skills, or refs" to `momentum:distill`. Replace with the two-lane alternative (quick-fix or sprint story). `partner.md` line 32 mentions distill as an option for quality concerns — remove it (leave avfl and upstream-fix).

6. **Clean up other skill references** — `feature-status/evals/eval-practice-path-topology-shows-handoffs.md` line 35 lists distill in the practice path topology. Remove the distill entry.

7. **Clean up `.claude/settings.local.json`** — line contains `"Skill(momentum:distill)"` in allowed tools. Remove this entry.

8. **Bump plugin.json version** — bump from 0.22.0 to 0.23.0 (minor bump — behavioral change: skill removal).

**Out of scope:**
- `skills/momentum/skills/avfl/references/framework.json` — contains a "distill" profile entry (lines 403–416). This is an AVFL validation profile named "distill" (used for lightweight post-change discovery passes). It is NOT a reference to `momentum:distill` skill — it is an independent profile name. Preserve this.
- `.momentum/sprints/*/` retro-transcript-audit.md and sprint-summary.md files — these are historical artifacts that mention distill in past tense. Do not edit historical sprint records.
- `docs/research/` and docs references — research documents are historical. Do not edit.
- `_bmad-output/planning-artifacts/` decision documents — historical. Do not edit.
- `.claude/skills/bmad-*/` — these are BMAD framework skills, not momentum plugin. References to "distill" there are within the BMAD distillator skill context, not momentum:distill. Do not edit.
- MEMORY.md files under `~/.claude/projects/` — memory entries mentioning distill work are historical context, not live routing. Do not edit.

## Acceptance Criteria

1. **`skills/momentum/skills/distill/` does not exist.** After this story, `ls skills/momentum/skills/distill/` returns a "not found" error. All files within — SKILL.md, workflow.md, evals/eval-discovery-before-write.md, evals/eval-three-path-routing.md, evals/eval-tier-classification.md — are deleted.

2. **`skills/momentum/.claude-plugin/plugin.json` version field reads `"0.23.0"` and file is valid JSON.** The version is bumped from 0.22.0 to 0.23.0. The file parses without error (`python3 -c "import json; json.load(open('skills/momentum/.claude-plugin/plugin.json'))"` exits 0). Note: plugin.json contains no distill skill registration entry — none existed before implementation.

3. **`skills/momentum/skills/retro/workflow.md` Phase 5 contains no distill references.** Grep for `distill` in retro/workflow.md returns zero matches. Phase 5 step goal is updated (no "route Tier 1 findings to distill" language). All priority action items route to stub creation. The Tier 1 / Tier 2 classification block, `{{distill_candidates}}`, distill invocation, and `{{distilled_dispositions}}` are removed. Phase 5 output summary no longer references "Distilled" count. Phase 5.5 note about "findings already routed to distill" is removed. Phase 5.5 line 646 no longer contains "or distilled". The retro workflow is still structurally valid XML (`<workflow>`, `<step>` tags well-formed) after the edit.

4. **`skills/momentum/skills/triage/workflow.md` contains no distill references.** Grep for `distill` in triage/workflow.md returns zero matches. The DISTILL class is removed from the six-class routing table. Triage routes: ARTIFACT → intake, DECISION → decision, queue → intake-queue append. DISTILL class handling (spawn, result tracking, output count) removed. Triage workflow is still structurally valid and routes the remaining classes.

5. **`skills/momentum/skills/triage/SKILL.md` description no longer mentions distill.** The description field is updated (≤150 characters) and does not reference "distill".

6. **`skills/momentum/skills/impetus/references/dispatch.md` no longer routes to momentum:distill.** The row "Apply a retro finding to rules, skills, or refs → `momentum:distill`" is replaced with appropriate two-lane guidance (e.g., route to quick-fix for urgent, sprint story for non-urgent).

7. **`skills/momentum/skills/impetus/references/partner.md` no longer mentions momentum:distill.** The quality concern entry no longer lists `momentum:distill` as an option.

8. **`skills/momentum/skills/feature-status/evals/eval-practice-path-topology-shows-handoffs.md` no longer lists distill in the practice path.** The "distill — Practice artifact distillation" entry is removed from the topology list.

9. **`.claude/settings.local.json` no longer contains `Skill(momentum:distill)` in allowed tools.** The entry is removed. The JSON file remains valid (parses without error).

10. **`skills/momentum/skills/triage/evals/eval-triage-classifies-six-classes.md` is updated to reflect five classes.** The eval no longer expects a DISTILL class in triage output.

11. **A grep for `momentum:distill` across the entire `skills/momentum/` directory returns zero matches.** Use: `grep -rn "momentum:distill" skills/momentum/`. Zero results.

12. **A grep for `momentum:distill` across `skills/momentum/` and `.claude/settings.local.json` returns zero matches.** No live invocation reference remains.

13. **`plugin.json` is valid JSON.** After edits, `python3 -c "import json; json.load(open('skills/momentum/.claude-plugin/plugin.json'))"` exits 0.

14. **Two behavioral evals written in `skills/momentum/skills/retro/evals/` confirm Phase 5 routes all findings to stubs.** Both evals confirm the absence of distill invocation paths in retro Phase 5.

15. **Three behavioral evals written for triage and impetus confirm the two-lane routing model.** Two evals in `skills/momentum/skills/triage/evals/` confirm triage routes five classes and never delegates to momentum:distill. One eval in `skills/momentum/skills/impetus/evals/` confirms dispatch routes urgent practice fixes to momentum:quick-fix and non-urgent to sprint story creation — no momentum:distill routing exists.

## Tasks / Subtasks

- [ ] **Task 1 — Delete `skills/momentum/skills/distill/` directory** (AC: 1, 11, 12)
  - [ ] Subtask 1.1: Verify the directory contents: SKILL.md, workflow.md, evals/eval-discovery-before-write.md, evals/eval-three-path-routing.md, evals/eval-tier-classification.md
  - [ ] Subtask 1.2: Delete the entire `skills/momentum/skills/distill/` directory tree
  - [ ] Subtask 1.3: Confirm directory no longer exists

- [ ] **Task 2 — Update `skills/momentum/.claude-plugin/plugin.json`** (AC: 2, 13) — `config-structure`
  - [ ] Subtask 2.1: Read plugin.json to confirm its structure (name, version, description, author — no skill registration list exists)
  - [ ] Subtask 2.2: Bump version from `"0.22.0"` to `"0.23.0"` (minor bump per version-on-release rule)
  - [ ] Subtask 2.3: Validate JSON parses without error
  - [ ] Subtask 2.4: Write updated plugin.json

- [ ] **Task 3 — Remove distill logic from `skills/momentum/skills/retro/workflow.md` Phase 5** (AC: 3, 11, 12) — `skill-instruction`
  - [ ] Subtask 3.1: Write 2 behavioral evals in `skills/momentum/skills/retro/evals/` before modifying (EDD protocol):
    - `eval-retro-phase5-routes-all-findings-to-stubs.md`: Given a retro Phase 5 with priority action items, all items should route to stub creation — no items should be classified as Tier 1 for distill routing
    - `eval-retro-phase5-no-distill-invocation.md`: Given any retro Phase 5 execution, the skill should never invoke `momentum:distill` or reference `{{distill_candidates}}`
  - [ ] Subtask 3.2: Read retro/workflow.md lines 484–601 (Phase 5) to understand full scope of distill logic
  - [ ] Subtask 3.3: Rewrite Phase 5 step goal: remove "route Tier 1 findings to distill" from the goal attribute
  - [ ] Subtask 3.4: Remove the Tier 1 / Tier 2 classification note block (lines ~500–511)
  - [ ] Subtask 3.5: Remove the `{{distill_candidates}}` / `{{stub_candidates}}` classification action (lines ~513–523)
  - [ ] Subtask 3.6: Remove the `<check if="distill_candidates is not empty">` block entirely (lines ~525–547)
  - [ ] Subtask 3.7: Simplify the `<check if="stub_candidates is not empty">` to use plain `{{action_items}}` — all priority items route to stubs
  - [ ] Subtask 3.8: Remove distill count from Phase 5 completion output (line ~597): `Distilled: {{distill_candidates | length}} | ...`
  - [ ] Subtask 3.9: In Phase 5.5 (line ~629), remove the note "Findings already routed to distill (Phase 5 Tier 1) — those are applied or staged"
  - [ ] Subtask 3.10: In Phase 5.5 (line 646), remove "or distilled" from "either stubbed or distilled" — leave only "stubbed"
  - [ ] Subtask 3.11: Verify retro/workflow.md XML is well-formed after edits (all `<step>` tags closed, no dangling template vars)
  - [ ] Subtask 3.12: Grep retro/workflow.md for "distill" — confirm zero matches

- [ ] **Task 4 — Remove distill from `skills/momentum/skills/triage/`** (AC: 4, 5, 10, 11, 12) — `skill-instruction`
  - [ ] Subtask 4.0: Write 2 behavioral evals in `skills/momentum/skills/triage/evals/` before modifying triage files (EDD protocol):
    - `eval-triage-routes-five-classes.md`: Given a set of observations, all route to ARTIFACT / DECISION / queue — no DISTILL class exists in triage output
    - `eval-triage-no-distill-delegation.md`: Given any triage execution, triage never spawns momentum:distill
  - [ ] Subtask 4.1: Read triage/SKILL.md description field; rewrite to remove "distill" reference (≤150 chars)
  - [ ] Subtask 4.2: Read triage/workflow.md; identify all 9 distill references at lines 9, 23, 36, 149, 211, 216, 217, 272, 273
  - [ ] Subtask 4.3: Remove DISTILL from the six-class routing table (now five classes)
  - [ ] Subtask 4.4: Remove DISTILL delegation logic (spawn momentum:distill per item, parallel spawns, wait for completion)
  - [ ] Subtask 4.5: Remove `{{distill_results}}` / `{{distill_count}}` tracking and output references
  - [ ] Subtask 4.6: Update triage/evals/eval-triage-classifies-six-classes.md to reflect five classes (DISTILL removed)
  - [ ] Subtask 4.7: Grep triage/ for "distill" — confirm zero matches

- [ ] **Task 5 — Clean up impetus references** (AC: 6, 7, 11, 12) — `skill-instruction`
  - [ ] Subtask 5.0: Write 1 behavioral eval in `skills/momentum/skills/impetus/evals/` (create directory if needed) before modifying impetus files (EDD protocol):
    - `eval-impetus-dispatch-two-lane-routing.md`: Given a developer intent to apply a practice fix, urgent fixes route to momentum:quick-fix and non-urgent to sprint story creation — no momentum:distill routing exists
  - [ ] Subtask 5.1: Read impetus/references/dispatch.md; replace the `momentum:distill` routing row with two-lane guidance (quick-fix for urgent practice fixes, sprint story for non-urgent)
  - [ ] Subtask 5.2: Read impetus/references/partner.md; remove `momentum:distill` from the quality concern entry (preserve avfl and upstream-fix references)
  - [ ] Subtask 5.3: Grep both files for "distill" — confirm zero matches

- [ ] **Task 6 — Clean up other references** (AC: 8, 9, 11, 12)
  - [ ] Subtask 6.1: Edit `skills/momentum/skills/feature-status/evals/eval-practice-path-topology-shows-handoffs.md` — remove the "distill — Practice artifact distillation" entry from the topology list
  - [ ] Subtask 6.2: Edit `.claude/settings.local.json` — remove `"Skill(momentum:distill)"` from the allowed tools list; validate JSON parses
  - [ ] Subtask 6.3: Grep `skills/momentum/` for "momentum:distill" — confirm zero matches
  - [ ] Subtask 6.4: Run broad grep for "distill" across `skills/momentum/skills/` (excluding `avfl/references/framework.json` which has a legitimate "distill" profile name) — review any remaining matches to confirm they are the AVFL profile, not momentum:distill references

- [ ] **Task 7 — Final validation** (AC: all)
  - [ ] Subtask 7.1: Run `grep -rn "momentum:distill" skills/momentum/` — confirm zero matches
  - [ ] Subtask 7.2: Run `python3 -c "import json; json.load(open('skills/momentum/.claude-plugin/plugin.json'))"` — confirm exits 0
  - [ ] Subtask 7.3: Confirm plugin.json version is 0.23.0
  - [ ] Subtask 7.4: Run EDD evals on retro Phase 5 (from Task 3 evals) — confirm both pass
  - [ ] Subtask 7.5: Run EDD evals on triage (from Task 4 evals) and impetus (from Task 5 eval) — confirm all three pass
  - [ ] Subtask 7.6: Document results in Dev Agent Record

## Dev Notes

### Decision Authority

This story enacts DEC-031 D6. The decision document is at:
`_bmad-output/planning-artifacts/decisions/dec-031-legibility-before-automation-canvas-gate-surface-2026-05-20.md`

The key rationale: distill is redundant with the two-lane model (skill-creator / agent-builder / constitution-builder for sprint stories; momentum:quick-fix for urgent changes). It has been blocking forward progress with heavy human intervention for un-deduped output.

### Current State of Affected Files

**`skills/momentum/skills/distill/SKILL.md`:**
- `name: distill`, `description: Practice artifact distillation — immediately applies a session learning or retro Tier 1 finding to the appropriate rule, reference, or skill prompt. Invoked directly or from retro Phase 5.`
- model: claude-sonnet-4-6, effort: medium
- Body delegates to ./workflow.md

**`skills/momentum/.claude-plugin/plugin.json`:**
- Current version: `"0.22.0"`
- Structure: name, version, description, author only — no skill registration list or distill entry exists
- Target version after bump: `"0.23.0"`

**`skills/momentum/skills/retro/workflow.md`:**
- Total: 835 lines
- Phase 5 (lines 484–601): distill-specific logic spans ~60 lines including Tier 1 classification note, distill_candidates extraction, momentum:distill invocation, distilled_dispositions tracking, and distill count in output summary
- Phase 5.5 (line 629): one-line note about findings "already routed to distill"
- Phase 5.5 (line 646): "either stubbed or distilled" — remove "or distilled", leave "stubbed"
- Preserve: Phase 5 stub creation path (Tier 2 logic, lines 549–582), Phase 5 output for approved/rejected stubs, Phase 5.5 handoff logic, all other phases

**`skills/momentum/skills/triage/workflow.md`:**
- DISTILL appears in exactly 9 references at lines: 9, 23, 36, 149, 211, 216, 217, 272, 273
- Preserve: ARTIFACT, DECISION, and queue routing classes; all non-DISTILL logic

**`skills/momentum/skills/triage/SKILL.md`:**
- Current description: `"Batch-classify observations into six classes, enrich ARTIFACTs, batch-approve, then delegate to intake/distill/decision or queue."`
- New description should reflect five classes and omit distill

**`skills/momentum/skills/impetus/references/dispatch.md`:**
- Line 29: `| Apply a retro finding to rules, skills, or refs | \`momentum:distill\` |`
- Replace with: urgent → `momentum:quick-fix`, non-urgent → create a sprint story via `momentum:create-story`

**`skills/momentum/skills/impetus/references/partner.md`:**
- Line 32: mentions `momentum:distill` as option for quality concerns alongside avfl and upstream-fix
- Remove momentum:distill from that line; preserve avfl and upstream-fix

**`.claude/settings.local.json`:**
- Contains `"Skill(momentum:distill)"` in an allowed tools array
- Remove this one entry; preserve all others; ensure the JSON array remains valid (no trailing comma issues)

### What NOT to Change

- `skills/momentum/skills/avfl/references/framework.json` — the `"distill"` key here (line ~403) is the AVFL profile name "distill" for lightweight post-change discovery passes. This is NOT a reference to the momentum:distill skill. Preserve it.
- Historical sprint records in `.momentum/sprints/*/` — retro-transcript-audit.md, sprint-summary.md. These are historical, not routing instructions.
- `docs/research/` and `_bmad-output/planning-artifacts/decisions/` — historical artifacts.
- `.claude/skills/bmad-distillator/` and `.claude/skills/bmad-*/` — BMAD framework skills referencing their own "distill" concepts. Not the same as momentum:distill.
- MEMORY.md files under `~/.claude/projects/` — historical memory, not routing.
- `~/.claude/plugins/marketplaces/momentum/` — marketplace mirror. Changes land there via `plugin marketplace update`, not direct edits.

### Architecture Compliance

- **Version-on-release rule** (`.claude/rules/version-on-release.md`): A behavioral change (skill removal) triggers a minor version bump. 0.22.0 → 0.23.0.
- **Two-lane replacement model** (DEC-031 D6): After removal, the canonical paths for practice fixes are: (1) sprint story with skill-creator / agent-builder / constitution-builder for new skills/agents, (2) `momentum:quick-fix` for urgent single-story fixes. No distill-equivalent shortcut replaces it.
- **Triage routing after removal**: Triage handles five classes (was six). DISTILL class is eliminated. Tier 1 retro findings that would have gone to distill now go to stub creation, to be picked up as sprint stories.

### Testing Requirements

- EDD (Eval-Driven Development) applies to all skill-instruction tasks (retro/workflow.md, triage/workflow.md, impetus references, feature-status eval).
- Write 2 behavioral evals for retro Phase 5 BEFORE modifying the workflow (Task 3 Subtask 3.1).
- Write 2 behavioral evals for triage BEFORE modifying triage files (Task 4 Subtask 4.0).
- Write 1 behavioral eval for impetus BEFORE modifying impetus references (Task 5 Subtask 5.0).
- No evals required for config-structure tasks (plugin.json, settings.local.json) — direct implementation + JSON validation is sufficient.
- The distill skill itself is deleted, so no evals are written for it.

### Project Context Reference

- `_bmad-output/planning-artifacts/decisions/dec-031-legibility-before-automation-canvas-gate-surface-2026-05-20.md` — authoritative decision document for DEC-031 D6
- `skills/momentum/.claude-plugin/plugin.json` — skill registration and version
- `skills/momentum/skills/retro/workflow.md` — Phase 5 distill routing to remove
- `skills/momentum/skills/triage/workflow.md` and SKILL.md — DISTILL class to remove
- `skills/momentum/skills/impetus/references/dispatch.md` — routing table to update
- `skills/momentum/skills/impetus/references/partner.md` — quality concern routing to update

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List

---

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1 → deletion (no evals needed — file removal is deterministic)
- Task 2 → config-structure (direct implementation + JSON validation)
- Tasks 3, 4, 5 → skill-instruction (EDD applies — write evals before modifying)
- Task 6 → mixed: skill-instruction (eval file update) + config-structure (settings.local.json) + skill-instruction (feature-status eval)
- Task 7 → cross-cutting close-out

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write behavioral evals (see Task 3 Subtask 3.1, Task 4 Subtask 4.0, Task 5 Subtask 5.0 for specific eval files):
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md files per the task subtasks

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — applies to triage/SKILL.md update
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23) — preserve existing
- Skill names use `momentum:` namespace prefix (NFR12) — N/A (no new skills)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2 behavioral evals written in `skills/momentum/skills/retro/evals/`
- [ ] 2 behavioral evals written in `skills/momentum/skills/triage/evals/`
- [ ] 1 behavioral eval written in `skills/momentum/skills/impetus/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] triage/SKILL.md description ≤150 characters confirmed
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config change** per the story's acceptance criteria
2. **Verify by inspection:**
   - plugin.json: must parse without error (`python3 -c "import json; json.load(open('skills/momentum/.claude-plugin/plugin.json'))"`)
   - settings.local.json: must parse without error
   - Version field: must read exactly `"0.23.0"`
3. **Document** what was created in the Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] All JSON files parse without error (validated with python3)
- [ ] plugin.json version field reads "0.23.0"
- [ ] No `Skill(momentum:distill)` in settings.local.json allowed tools
- [ ] Changes documented in Dev Agent Record

---

### Gherkin Specs Reminder (Decision 30 — Black-Box Separation)

If Gherkin specs exist for this sprint at `.momentum/sprints/{sprint-slug}/specs/`, they are **off-limits to the dev agent**. The dev agent implements against the plain-English Acceptance Criteria in this story file only — never against `.feature` files.
