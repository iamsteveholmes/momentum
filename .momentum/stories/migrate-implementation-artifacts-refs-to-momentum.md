---
title: Migrate implementation-artifacts path references to .momentum/
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-invocable.md
  - skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-loads-sprint-summary-when-available.md
  - skills/momentum/skills/distill/evals/eval-tier-classification.md
  - skills/momentum/skills/triage/evals/eval-triage-delegates-not-writes.md
  - skills/momentum/skills/intake/evals/eval-intake-captures-context.md
  - skills/momentum/skills/retro/evals/eval-produces-sprint-summary-at-retro-close.md
  - skills/momentum/skills/plan-audit/evals/eval-substantive-spec-audit.md
  - skills/momentum/skills/refine/evals/eval-refine-reprioritization.md
  - skills/momentum/skills/refine/evals/eval-refine-assessment-decision-review.md
  - skills/momentum/skills/feature-breakdown/workflow.md
  - skills/momentum/skills/feature-grooming/evals/eval-refine-detects-unmapped-stories.md
  - skills/momentum/scripts/update-story-status.sh
change_type: skill-instruction
---

# Migrate implementation-artifacts path references to .momentum/

## Goal

Replace every stale `_bmad-output/implementation-artifacts/` path reference in skill files, evals,
workflows, and scripts with the correct `.momentum/` path. These references cause evals to test
against wrong paths and scripts to break in consumer projects.

## Story

As a Momentum skill consumer,
I want all skill evals, workflows, and scripts to reference `.momentum/` for stories and sprints,
so that the skills behave correctly after the path migration that moved implementation artifacts
from `_bmad-output/implementation-artifacts/` to `.momentum/`.

## Description

Multiple skill files, evals, workflows, and scripts still reference `_bmad-output/implementation-artifacts/`
— the old path for stories and sprints that has since moved to `.momentum/`. This causes incorrect
behavior in consumer projects: evals test against the wrong paths, workflows read from the wrong
locations, and scripts break.

`orient.md` is already correct in source (uses `.momentum/` paths) but cached plugin versions
(0.17.x, 0.18.0) in consumer projects may still show the old path — this is resolved by publishing
the fix.

**Critical scoping rule:** `_bmad-output/planning-artifacts/` references are intentional and must
NOT be changed. PRD, architecture, epics, features, assessments, and decisions still live in
`_bmad-output/planning-artifacts/` in consumer projects.

**Special case — impetus eval:** `skills/momentum/skills/impetus/evals/eval-impetus-reads-momentum-state.md`
uses `_bmad-output/implementation-artifacts/` references intentionally — the eval tests that Impetus
does NOT fall back to those paths. Those occurrences are anti-pattern examples and must NOT be changed.

## Acceptance Criteria

1. **Zero remaining stale references:** Exhaustive grep of all skill files, evals, workflow.md
   files, agent definitions, scripts, and reference docs shows zero occurrences of
   `_bmad-output/implementation-artifacts/` outside of files that intentionally document the
   old path as a rejected anti-pattern (the impetus eval).
2. **Planning artifacts untouched:** All `_bmad-output/planning-artifacts/` references are
   untouched — a grep confirming 0 changes to planning-artifacts paths is required.
3. **orient.md verified correct:** `skills/momentum/skills/impetus/references/orient.md`
   contains only `.momentum/` paths (already fixed in source — verify not re-introduced).
4. **Plugin patch version bumped:** `skills/momentum/.claude-plugin/plugin.json` version is
   incremented (patch) and committed after all fixes are applied.

## Dev Notes

### What exists today

**Current path mapping:**
- Old path (wrong): `_bmad-output/implementation-artifacts/`
- Correct path: `.momentum/`

**orient.md is already correct.** Reading it confirms `.momentum/sprints/index.json` and
`.momentum/stories/index.json` with the explicit statement "There is no fallback to
`_bmad-output/implementation-artifacts/`."

**update-story-status.sh is deprecated.** The script has a deprecation header noting it will be
replaced by `momentum-sprint-manager`. However it still has a live reference on line 44 that
points to `sprint-status.yaml` under the old path. Fix the path even in the deprecated script —
consumers may still invoke it.

**Current plugin version:** `0.18.0` in `skills/momentum/.claude-plugin/plugin.json`. After
all fixes, bump to `0.18.1`.

### Exhaustive file list (verified by grep)

**Files requiring path replacement:**

| File | Lines with old path | Replacement |
|------|--------------------|-|
| `skills/momentum/scripts/update-story-status.sh` | 44 | `$PROJECT_DIR/.momentum/sprint-status.yaml` |
| `skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-invocable.md` | 8 | `.momentum/stories/index.json` |
| `skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-loads-sprint-summary-when-available.md` | 8, 15, 19, 41, 44 | `.momentum/sprints/...` and `.momentum/stories/...` |
| `skills/momentum/skills/distill/evals/eval-tier-classification.md` | 36 | `.momentum/stories/` |
| `skills/momentum/skills/triage/evals/eval-triage-delegates-not-writes.md` | 39-40 | `.momentum/stories/...` |
| `skills/momentum/skills/intake/evals/eval-intake-captures-context.md` | 46 | `.momentum/stories/<slug>.md` |
| `skills/momentum/skills/retro/evals/eval-produces-sprint-summary-at-retro-close.md` | 26, 38 | `.momentum/sprints/sprint-2026-03-01/sprint-summary.md` |
| `skills/momentum/skills/plan-audit/evals/eval-substantive-spec-audit.md` | 57, 74 | `.momentum/` prefix |
| `skills/momentum/skills/refine/evals/eval-refine-reprioritization.md` | 6, 29 | `.momentum/sprints/...` |
| `skills/momentum/skills/refine/evals/eval-refine-assessment-decision-review.md` | 19 | `.momentum/stories/index.json` |
| `skills/momentum/skills/feature-breakdown/workflow.md` | 20 | `.momentum/` (loaded from config key — see note below) |
| `skills/momentum/skills/feature-grooming/evals/eval-refine-detects-unmapped-stories.md` | 3 | `.momentum/stories/index.json` |

**Files that must NOT be changed:**
- `skills/momentum/skills/impetus/evals/eval-impetus-reads-momentum-state.md` — uses old path as
  a rejected anti-pattern test assertion. Do not modify.
- `skills/momentum/skills/impetus/references/orient.md` — already correct.
- Any file under `_bmad-output/planning-artifacts/` — different domain, not affected.

### feature-breakdown/workflow.md note

The workflow.md Initialization block reads both `planning_artifacts` and `implementation_artifacts`
from `_bmad/bmm/config.yaml`. The `implementation_artifacts` config key itself still points to
`_bmad-output/implementation-artifacts/` in the config file. However, the **comment** in the
workflow reads `- implementation_artifacts — path to _bmad-output/implementation-artifacts/` — this
inline comment is the stale reference to fix. Change the comment to reflect the new path:
`- implementation_artifacts — path to .momentum/` (or better: remove the inline path hint
entirely, since the workflow loads this from config at runtime and should not hardcode the path
in comments).

**However:** The `_bmad/bmm/config.yaml` `implementation_artifacts` key also needs to be
consistent. Check whether the config still points to `_bmad-output/implementation-artifacts/`
or `.momentum/`. The skills load this key dynamically — if the config is wrong, fixing comments
alone won't help. Read the config before editing the workflow.

### Replacement pattern

All replacements follow a simple substitution:
```
_bmad-output/implementation-artifacts/ → .momentum/
```

Paths underneath that prefix (e.g., `stories/index.json`, `sprints/sprint-2026-03-01/sprint-summary.md`)
remain unchanged. Only the prefix changes.

### Verification step

After all edits, run:
```bash
grep -rn "_bmad-output/implementation-artifacts" skills/momentum/ | \
  grep -v "eval-impetus-reads-momentum-state"
```

Expected result: zero output lines. Any remaining line is a missed edit.

Confirm planning artifacts are untouched:
```bash
grep -rn "_bmad-output/planning-artifacts" skills/momentum/ | wc -l
```

Compare to pre-edit count to confirm no reduction.

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks → `skill-instruction` (editing SKILL.md-adjacent instruction files: evals, workflow.md, scripts within skills/)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

These are edits to existing skill instruction files (evals, workflow.md, scripts). EDD applies:

**Before editing:**
1. Read each target file in full to understand current content and surrounding context.
2. Confirm you are NOT changing `_bmad-output/planning-artifacts/` references — those are in scope
   for a different domain and must remain untouched.
3. Confirm you are NOT editing `eval-impetus-reads-momentum-state.md` — its old-path references are
   intentional (anti-pattern assertions).

**Implement:**
4. Apply the `_bmad-output/implementation-artifacts/` → `.momentum/` substitution in each file.
5. For `feature-breakdown/workflow.md`: update the inline comment on line 20 to remove the
   hardcoded old path. Do not change the config key load — that happens at runtime.
6. For `update-story-status.sh`: update the `SPRINT_STATUS` variable path on line 44.
7. For `plugin.json`: bump `version` from `0.18.0` to `0.18.1`.

**Verify:**
8. Run the grep verification commands from Dev Notes above.
9. Confirm zero remaining stale references (excluding the intentional anti-pattern eval).
10. Confirm planning-artifacts count is unchanged.

**NFR compliance notes:**
- These are edits to existing files — no new SKILL.md files created. SKILL.md description/model/effort
  constraints do not apply.
- No new eval files required (these ARE the eval files being corrected).

**Additional DoD items for this story:**
- [ ] Grep verification: zero remaining `_bmad-output/implementation-artifacts/` refs in skills/
  (excluding eval-impetus-reads-momentum-state.md)
- [ ] Grep verification: `_bmad-output/planning-artifacts/` count unchanged (no accidental changes)
- [ ] orient.md confirmed correct (read the file — verify `.momentum/` paths only)
- [ ] plugin.json version bumped to 0.18.1 and committed
- [ ] feature-grooming eval (not in original user-provided list) confirmed fixed

## File List

**Modify** (path prefix fix `_bmad-output/implementation-artifacts/` → `.momentum/`):
- `skills/momentum/scripts/update-story-status.sh` — line 44 SPRINT_STATUS path
- `skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-invocable.md` — line 8
- `skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-loads-sprint-summary-when-available.md` — lines 8, 15, 19, 41, 44
- `skills/momentum/skills/distill/evals/eval-tier-classification.md` — line 36
- `skills/momentum/skills/triage/evals/eval-triage-delegates-not-writes.md` — lines 39-40
- `skills/momentum/skills/intake/evals/eval-intake-captures-context.md` — line 46
- `skills/momentum/skills/retro/evals/eval-produces-sprint-summary-at-retro-close.md` — lines 26, 38
- `skills/momentum/skills/plan-audit/evals/eval-substantive-spec-audit.md` — lines 57, 74
- `skills/momentum/skills/refine/evals/eval-refine-reprioritization.md` — lines 6, 29
- `skills/momentum/skills/refine/evals/eval-refine-assessment-decision-review.md` — line 19
- `skills/momentum/skills/feature-breakdown/workflow.md` — line 20 comment
- `skills/momentum/skills/feature-grooming/evals/eval-refine-detects-unmapped-stories.md` — line 3

**Modify** (version bump):
- `skills/momentum/.claude-plugin/plugin.json` — bump `0.18.0` → `0.18.1`

**Read-only verification** (do not modify):
- `skills/momentum/skills/impetus/references/orient.md` — verify already correct
- `skills/momentum/skills/impetus/evals/eval-impetus-reads-momentum-state.md` — verify NOT changed

## Dev Agent Record

Status: ready-for-dev
