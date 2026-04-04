# AVFL Invocation Guide for momentum-dev

Reference this file in Step 7 to determine how to run AVFL on the story's complete changeset.

## What AVFL Validates

AVFL validates the **entire story changeset** — not a single "primary artifact." Every file added, modified, or deleted by the story is part of the validation input. This holistic approach catches problems that per-file validation misses:

- Extraneous files that shouldn't have been changed
- Files that should have been deleted or modified but weren't
- Cross-file inconsistencies (e.g., code that doesn't match the spec it implements)
- Changes that are unnecessary for fulfilling the acceptance criteria
- Incomplete implementations where some ACs are only partially addressed

The story file itself is included in the diff (status updates, Dev Agent Record, File List, Change Log), so AVFL can cross-reference the story's own records against the actual changes.

## Capturing the Changeset

Every momentum-dev story runs in an isolated git worktree on branch `story/{{story_key}}`, branched from `{{target_branch}}`. After bmad-dev-story completes and the workflow exits the worktree, capture the complete changeset:

```
git diff {{target_branch}}...story/{{story_key}}
```

This shows all additions, modifications, and deletions across every commit on the story branch — regardless of how many intermediate commits bmad-dev-story made.

## Profile Selection

| Story characteristics | Profile | Rationale |
|---|---|---|
| Most stories (code, specs, mixed, skills, rules, docs) | `checkpoint` | 2–3 lenses, one fix attempt — good quality signal without 8-agent cost |
| Config/structure-only stories (only JSON, YAML, directory changes) | `gate` | Structural pass/fail — fields present, types correct |

**How to determine config-only:** If every file path in the diff is a `.json`, `.yaml`, `.yml`, `.toml`, or version file, and no substantive prose or code was added, use `gate`. If any code, skill instructions, rules, or documentation appear in the diff, use `checkpoint`.

**Why `checkpoint` not `full`?** Skills get dogfooded on real stories; code gets tested; specs get reviewed. `checkpoint` gives structural and coherence quality signal without the 8-agent cost of `full`. Reserve `full` for final deliverables, high-stakes content, or anything published without further review.

## Domain Expert Selection

Infer `domain_expert` from the story's context and the dominant type of change:

| Dominant change type | domain_expert |
|---|---|
| Skill instructions (SKILL.md, workflow.md, agent definitions) | `"skill author"` |
| Code and scripts (.sh, .py, .ts, .js, .go, etc.) | `"software engineer"` |
| Specifications and documentation (PRD, architecture, stories, README) | `"technical writer"` |
| Rules and hooks (.claude/rules/, hook configs) | `"practice engineer"` |
| Configuration (JSON, YAML, version files) | `"project engineer"` |
| Mixed — no clear dominant type | `"software engineer"` |

When in doubt, use `"software engineer"` — it is the broadest applicable role.

## Parameter Template

One unified template for all stories:

```
domain_expert: [inferred from story context — see table above]
task_context: "Story {{story_key}} — [brief description from story title]"
output_to_validate: [full git diff output from: git diff {{target_branch}}...story/{{story_key}}]
source_material: [the Acceptance Criteria section from {{story_file}}]
profile: [checkpoint or gate — see Profile Selection above]
stage: final
```

**Why acceptance criteria as source_material?** AVFL's Factual Accuracy lens checks whether the produced changes deliver what they were supposed to deliver. The ACs define "supposed to deliver."

**Why the full diff as output_to_validate?** The diff captures everything — additions, deletions, modifications across all file types. AVFL can assess completeness (did the changes fulfill all ACs?), correctness (are the changes right?), and scope (are there extraneous changes?).

## Presenting AVFL Findings

Always synthesize AVFL output before presenting to the user. Never dump raw JSON.

**Format:**
```
AVFL [checkpoint|gate] — [CLEAN | CHECKPOINT_WARNING | GATE_FAILED]
[If CHECKPOINT_WARNING or GATE_FAILED:]
  ! [critical finding summary — one line]
  · [medium finding summary — one line]
  [etc.]
```

**Severity key:** `!` = critical or high, `·` = medium or low
