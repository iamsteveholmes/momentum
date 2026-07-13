---
title: Base-body collapse rollback
story_key: base-body-collapse-rollback
status: ready-for-dev
epic_slug: momentum-agent-role-contracts
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
priority: high
change_type:
  - script-code
  - skill-instruction
  - agent-definition
  - specification
verification_method_advisory: bash
depends_on: []
touches:
  - skills/momentum/agents/dev-frontend.md
  - skills/momentum/agents/dev-build.md
  - skills/momentum/agents/dev-skills.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/build-guidelines/workflow.md
  - skills/momentum/references/sprint-tracking-schema.md
  - skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md
  - skills/momentum/agents/evals/eval-large-file-guidance-present.md
  - skills/momentum/skills/dev/evals/eval-no-commit-instruction-in-any-variant.md
  - skills/momentum/agents/evals/eval-agent-resolve-defaults-fallback.md
  - skills/momentum/agents/evals/eval-agent-resolve-project-entry-match.md
---

# Base-body collapse rollback

## Story

As a developer,
I want the plugin to ship only one `dev` base body (removing the pre-shipped `dev-frontend`, `dev-build`, and `dev-skills` specialist bodies) and to retire the `specialist-classify` mapping that resolves to them,
so that routing-table resolution (`momentum-tools agent resolve` against `momentum/agents.json`) becomes the single specialist spawn path and projects are not locked into Momentum's taxonomy guesses.

## Description

The plugin currently ships three pre-shipped dev specialist base bodies — `skills/momentum/agents/dev-frontend.md`, `dev-build.md`, and `dev-skills.md` — and a deterministic `momentum-tools specialist-classify` command that maps a story's `touches`/`change_type` to one of those specialists. This is a **second specialist spawn path** that duplicates and competes with the Gen-2 routing-table model (Decision 55 / DEC-023), under which composed specialists live per-project at `.claude/guidelines/agents/{role}-{domain}.md` and are resolved through `momentum/agents.json` by `momentum-tools agent resolve`.

This story collapses the two paths into one. It removes the three pre-shipped specialist bodies, retires the `specialist-classify → pre-shipped body` resolution, and updates every skill, workflow, reference doc, and eval fixture that still resolves those files — so that **`momentum-tools agent resolve` against `agents.json` is the ONLY specialist spawn path**. The generic `dev` base body (`skills/momentum/agents/dev.md`) survives as the single dev role contract; project-specific specialists remain available exclusively through composed `project` entries in `agents.json`.

This is step (2) of the four-step sequence recorded in architecture.md Decision 55 (ARCH-3): (1) architect-guard base body ships, **(2) this story removes the legacy specialist bodies**, (3) the `architecture-decision-26-update-for-base-body-collapse` sibling records the collapse in architecture.md, then (4) constitution-builder and agent-builder follow.

**Scope boundary (sibling coherence):** This story owns the file removals, the `specialist-classify` retirement, and all skill/workflow/reference/eval reference updates. It does **NOT** edit `architecture.md` — every architecture.md edit (Decision 26 canonical-lookup paragraph, the three Repository Structure listings, and the ARCH-3 note in Decision 55) is owned by the `architecture-decision-26-update-for-base-body-collapse` sibling. It does **NOT** rename or touch `qa-reviewer.md` / `e2e-validator.md` — those belong to the `rename-base-body-files-to-canonical-naming` sibling. The specialist-body reference set (dev-frontend / dev-build / dev-skills) and the naming-sibling's reference set (qa-reviewer / e2e-validator) are disjoint.

## Acceptance Criteria

1. The three pre-shipped specialist base-body files — `skills/momentum/agents/dev-frontend.md`, `skills/momentum/agents/dev-build.md`, and `skills/momentum/agents/dev-skills.md` — no longer exist in the plugin.
2. Exactly one `dev` base body remains: `skills/momentum/agents/dev.md`. `agents.json` `defaults.dev` resolves to it, and no pre-shipped specialist `dev-*` base body remains under `skills/momentum/agents/`.
3. `momentum-tools specialist-classify` no longer resolves any `touches`/`change_type` input to `dev-skills`, `dev-build`, or `dev-frontend`. The `change_type → pre-shipped-specialist-body` mapping (`SPECIALIST_PATTERNS`, `_match_specialist`, `cmd_specialist_classify` in `momentum-tools.py`) is retired, and `test-momentum-tools.py` reflects the retirement (no test asserts a `dev-skills`/`dev-build`/`dev-frontend` classification result).
4. The `sprint-planning` and `quick-fix` workflows no longer contain a `touches → dev-skills/dev-build/dev-frontend` specialist classification table. Team/specialist selection in both workflows resolves through `momentum-tools agent resolve` against `agents.json`.
5. Every remaining reference to a removed specialist body in skill/workflow/reference files is updated or removed. Specifically reconciled: `sprint-dev/workflow.md` (line ~267 composed-slug note), `conductor/workflow.md` (line ~560 `{{dev_agent}}` example list), `build-guidelines/workflow.md` (line ~299 example), `references/sprint-tracking-schema.md` (line ~112 `specialist` field enum), and `sprint-planning/references/plan-gate-renderer.md` (line ~202 example). No skill or workflow resolves a `skills/momentum/agents/` path for `dev-skills.md`, `dev-build.md`, or `dev-frontend.md`.
6. Eval fixtures that hard-reference the removed files are reconciled: `agents/evals/eval-large-file-guidance-present.md` and `skills/dev/evals/eval-no-commit-instruction-in-any-variant.md` no longer enumerate the deleted files; `agents/evals/eval-agent-resolve-defaults-fallback.md` and `eval-agent-resolve-project-entry-match.md` use a surviving base body or a composed `.claude/guidelines/agents/` path instead of the now-dead `skills/momentum/agents/dev-build.md` fixture path.
7. `momentum-tools agent resolve` (against `agents.json`) is the sole specialist spawn path: a repo-wide search finds no hard-coded resolution to a pre-shipped dev specialist body anywhere outside `agents.json` `project` (composed) entries.

## Tasks / Subtasks

- [ ] **Remove the pre-shipped specialist bodies** (AC1, AC2)
  - [ ] Delete `skills/momentum/agents/dev-frontend.md`, `dev-build.md`, `dev-skills.md`
  - [ ] Confirm `skills/momentum/agents/dev.md` remains and `agents.json` `defaults.dev` still points to it
- [ ] **Retire `specialist-classify` resolution to pre-shipped bodies** (AC3)
  - [ ] In `skills/momentum/scripts/momentum-tools.py`, remove or repoint `SPECIALIST_PATTERNS`, `_match_specialist`, and `cmd_specialist_classify` so no input resolves to `dev-skills`/`dev-build`/`dev-frontend`; update the CLI usage/help text (line ~20, ~3004-3007)
  - [ ] Update `skills/momentum/scripts/test-momentum-tools.py` — remove/replace tests asserting specialist classification results
- [ ] **Collapse the specialist classification tables in sprint-planning and quick-fix** (AC4)
  - [ ] `sprint-planning/workflow.md` — remove the `touches → dev-skills/dev-build/dev-frontend` table (lines ~781-783) and the "coarse specialist value" notes (~845, ~853); route via `momentum-tools agent resolve`
  - [ ] `quick-fix/workflow.md` — remove the specialist table (lines ~204-206), the filename-derivation step (~214), the `agent_file` example (~313), and any `specialist-classify` invocation; route via `momentum-tools agent resolve`
- [ ] **Reconcile remaining skill/workflow/reference references** (AC5)
  - [ ] `sprint-dev/workflow.md` (~267), `conductor/workflow.md` (~560), `build-guidelines/workflow.md` (~299), `references/sprint-tracking-schema.md` `specialist` enum (~112), `sprint-planning/references/plan-gate-renderer.md` (~202)
- [ ] **Reconcile eval fixtures** (AC6)
  - [ ] Hard fixtures: `eval-large-file-guidance-present.md`, `eval-no-commit-instruction-in-any-variant.md`, `eval-agent-resolve-defaults-fallback.md`, `eval-agent-resolve-project-entry-match.md`
  - [ ] Audit conceptual mentions (composed-slug / spawn-registry-key examples) in `eval-touches-resolves-composed-slug-not-dev.md`, `eval-dedup-guard-blocks-duplicate.md`, `eval-dedup-guard-allows-new-stories.md`, `eval-retro-phase5-routes-all-findings-to-stubs.md`; update any that name a now-deleted `.md` file, keep those that correctly use `dev-skills` as a *composed* project slug
- [ ] **Verify single spawn path** (AC7)
  - [ ] Repo-wide grep confirms no residual hard-coded resolution to a pre-shipped `dev-*` specialist body outside `agents.json` `project` entries

## Dev Notes

### Decision Authority

- **Decision 55 / DEC-023 (Agent Routing Table, architecture.md ~line 3010):** `momentum-tools agent resolve` against `agents.json` is the canonical specialist-resolution mechanism. The ARCH-3 note explicitly sequences this story as step (2) and names the removal scope ("REMOVE the pre-shipped dev-frontend/dev-build/dev-skills specialist bodies, collapsing specialist resolution to the routing-table alone"). The resolver was already hardened (sprint-2026-06-02) with dead-role cleanup + `Path.exists()` validation, so a stale routing entry pointing at a deleted body is pruned/hard-failed rather than silently emitting an unspawnable path — this removal is safe against the resolver.
- **Decision 56 / DEC-026 (Agent Builder pipeline):** composed specialists live at `.claude/guidelines/agents/{role}-{domain}.md`, written by agent-builder into `agents.json` `project`. The `project` block is where "dev-skills"-style specialists legitimately survive **as composed slugs**, not as pre-shipped plugin files.
- **DEC-020 (Universal Agent Role Taxonomy):** the `dev` role is one of the nine universal base bodies; specialization is a composition concern, not a pre-shipped-file concern.

### Current State of Affected Files

- `skills/momentum/agents/` ships nine base-body files today: `analyst.md`, `dev.md`, `dev-build.md`, `dev-frontend.md`, `dev-skills.md`, `e2e-validator.md`, `qa-reviewer.md`, `researcher.md`, `ux.md` — that is six role bodies plus the three `dev-*` specialist bodies this story removes. The three `dev-*` specialist files are the removal targets; `dev.md` is the surviving dev body (six role bodies remain after collapse).
- `momentum/agents.json` `defaults` keys: `ux`, `analyst`, `researcher`, `dev`, `qa-reviewer`, `e2e-validator`. It does **not** list the specialist bodies today, so **`agents.json` itself needs no edit** for this story — the specialist bodies were only ever reachable via `specialist-classify` and hard-coded workflow tables, which is exactly what this story removes.
- `momentum-tools.py`: `specialist-classify` implemented at ~lines 1901-1964 (`SPECIALIST_PATTERNS`, `_match_specialist`, `cmd_specialist_classify`), registered at ~3004-3007, documented at ~line 20.
- Reference footprint (current, grepped fresh — references have grown since capture): see the Reference Audit under `### References`.

### Architecture Compliance

- After this story, the only specialist spawn path is `momentum-tools agent resolve --role <role> --touches <paths>` → `agents.json` (`project` first, then `defaults`). No workflow may re-introduce a `touches → specialist-body` lookup table.
- Editing `workflow.md`, `SKILL.md`, and agent-definition files falls under the `dev-skills` rule: follow `skills/momentum/references/agent-skill-development-guide.md` (authoritative frontmatter/structure conventions; 500-line limit).
- **Do not** edit `architecture.md` in this story — those edits are the `architecture-decision-26-update-for-base-body-collapse` sibling's ACs. Leaving them for the sibling keeps each observable architecture-doc change owned by exactly one story.

### Testing Requirements

Primary verification method (advisory): **bash** — the highest-precedence change type present is `script-code` (the `momentum-tools.py` retirement).

- Run `momentum-tools specialist-classify --touches "skills/foo/SKILL.md"` (and Gradle/Compose paths) and confirm it no longer returns `dev-skills`/`dev-build`/`dev-frontend`.
- Run `momentum-tools agent resolve --role dev --touches <paths>` and confirm it resolves via `agents.json` (composed `project` entry when present, else `defaults.dev`).
- Run `test-momentum-tools.py` — green, with specialist-classification assertions removed/updated.
- Whichever `cmd_specialist_classify` branch is chosen, verify it: if **repointed**, run the command and confirm it no longer returns `dev-skills`/`dev-build`/`dev-frontend`; if **removed**, confirm `specialist-classify` is absent from `momentum-tools --help` and that invoking it errors (unknown subcommand). The dev commits to exactly one branch and the self-check matches it.
- Repo-wide grep gate (AC7): `grep -rn -E "dev-frontend|dev-build|dev-skills" skills/momentum` returns only legitimate composed-slug/example usages, no resolution of a deleted plugin file.

### Implementation Guide

- **script-code (`momentum-tools.py`, tests):** TDD delegation — update `test-momentum-tools.py` first to encode the retired behavior, then modify the implementation until green.
- **skill-instruction (workflow.md edits):** EDD — after each workflow edit, re-read the surrounding block to confirm the routing instruction now names `momentum-tools agent resolve` and no orphan table row or `{{dev_agent}}` example references a removed body.
- **agent-definition (file removals):** deletion + reference sweep; the observable check is absence of the files and absence of any resolution to them.
- **specification (schema/reference/eval docs):** direct authoring with cross-reference verification; the `specialist` enum in `sprint-tracking-schema.md` must no longer offer `dev-skills`/`dev-build`/`dev-frontend`.
- A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Read the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done; do not read the verifier body beyond sections referenced by `how_dev_self_checks`.

### Project Structure Notes

- Base bodies: `skills/momentum/agents/*.md` (plugin-shipped role contracts). Composed specialists: `.claude/guidelines/agents/{role}-{domain}.md` (per-project, written by agent-builder). This story enforces that specialization happens only at the composed layer.
- The `dev-skills` **token** legitimately survives in two forms after this story: (a) as a composed project slug in `agents.json` `project` (e.g. a project's `dev/skills` domain), and (b) as the `.claude/rules/dev-skills.md` rule name. Neither is a pre-shipped base body; do not delete these.

### References

- **Sibling — `rename-base-body-files-to-canonical-naming`:** operates on the *surviving* base bodies (`qa-reviewer.md`, `e2e-validator.md`) after this collapse; depends on this story. Disjoint reference set (never touches `dev-*` specialist bodies).
- **Sibling — `architecture-decision-26-update-for-base-body-collapse`:** owns ALL `architecture.md` edits recording this collapse (Decision 26 canonical-lookup paragraph ~line 2169; Repository Structure listings ~lines 345-347, 1230-1232, 2304-2306; ARCH-3 note ~line 3012); depends on this story.
- **Reference Audit (grepped 2026-07-13) — Tier A, hard references that break on removal:**
  - `skills/momentum/scripts/momentum-tools.py` (~20, ~1901-1964, ~3004-3007) and `test-momentum-tools.py`
  - `skills/momentum/skills/sprint-planning/workflow.md` (~781-783, ~845, ~853)
  - `skills/momentum/skills/quick-fix/workflow.md` (~204-206, ~214, ~313, `specialist-classify` invocation)
  - `skills/momentum/skills/sprint-dev/workflow.md` (~267)
  - `skills/momentum/skills/conductor/workflow.md` (~560)
  - `skills/momentum/skills/build-guidelines/workflow.md` (~299)
  - `skills/momentum/references/sprint-tracking-schema.md` (~112, `specialist` enum)
  - `skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md` (~202)
  - `skills/momentum/agents/evals/eval-large-file-guidance-present.md` (~26-28, ~70-72)
  - `skills/momentum/skills/dev/evals/eval-no-commit-instruction-in-any-variant.md` (~5)
  - `skills/momentum/agents/evals/eval-agent-resolve-defaults-fallback.md` (~34) and `eval-agent-resolve-project-entry-match.md` (~33, ~56, ~79)
- **Reference Audit — Tier B, conceptual mentions (audit, keep legitimate composed-slug usages):** `skills/momentum/skills/build-guidelines/evals/eval-touches-resolves-composed-slug-not-dev.md` (~18), `skills/momentum/skills/sprint-dev/evals/eval-dedup-guard-blocks-duplicate.md`, `eval-dedup-guard-allows-new-stories.md`, `skills/momentum/skills/retro/evals/eval-retro-phase5-routes-all-findings-to-stubs.md` (~16).
- **Architecture:** `_bmad-output/planning-artifacts/architecture.md` Decision 55 / DEC-023 (~line 3010, ARCH-3 sequencing), Decision 56 / DEC-026 (composed-specialist layer).
- Epic context: `momentum-agent-role-contracts` (from _bmad-output/planning-artifacts/epics.json)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
