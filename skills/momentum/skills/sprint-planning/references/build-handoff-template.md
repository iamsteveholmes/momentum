# Build Handoff Template — Sprint Planning Step 8

**Implements:** Step 8 (Activate the sprint) of `sprint-planning/workflow.md` — the mandatory
build-bridge artifact written as the terminal action of activation.
**Consumed by:** the next `/momentum:conduct` session (or `momentum:sprint-dev`, if invoked
directly) — a fresh session with no memory of the planning session that produced this sprint.
**Governs:** `.claude/rules/handoff-conventions.md` (write location + `<topic>-<YYYY-MM-DD>.md`
naming).
**Lifecycle:** use-then-discard. The build session deletes this file once consumed — handoffs
are ephemeral, never preserved as history.

---

## 1. Filename

```
.momentum/handoffs/{{sprint_slug}}-build-handoff-{{handoff_date}}.md
```

`{{handoff_date}}` is the activation date (`YYYY-MM-DD`) — the same date `momentum-tools sprint
activate` stamps onto the sprint record's `started` field.

## 2. Exact skeleton

Fill every `{{placeholder}}`. Do not reorder, rename, or drop any of the four sections. The
opening notice is the file's literal first line, ahead of every section — not a preamble folded
into the first heading.

```
This is a use-then-discard build bridge for the next `/momentum:conduct` session. Delete this
file once the build session has consumed it — handoffs are ephemeral, not preserved as history.

# Build Handoff — {{sprint_slug}}

## Sprint Goal

{{goal}}

## Stories by Wave

### Wave {{n}}
- `{{story_slug}}`
- `{{story_slug}}`

## Contract / Spec Locations

- `{{story_slug}}`: `{{contract_path}}`
- `{{story_slug}}`: `{{contract_path}}`
- Coverage plan: `.momentum/sprints/{{sprint_slug}}/coverage-plan.md`

## Planning-Time Cautions

- {{caution}}
```

Repeat the `### Wave {{n}}` block once per wave in `{{waves}}`, lowest wave number first
(execution order), each listing its assigned story slugs as a bullet list. Repeat the
`Contract / Spec Locations` bullet once per story in `{{selected_stories}}`, then always end
that section with the coverage-plan line. Repeat the `Planning-Time Cautions` bullet once per
item in `{{cautions}}`.

## 3. Fallback wording (mandatory, verbatim — never blank, never omitted)

| Condition | Section body |
|---|---|
| `{{goal}}` is null/absent | `Sprint goal not captured at planning` |
| `{{cautions}}` is empty | `No planning-time cautions raised.` |

Both sections keep their heading even when using fallback wording — a section with no heading
at all is a missing section (producer/consumer mismatch), not an empty one.

## 4. Data sourcing (all already in scope at Step 8 — no new elicitation)

| Field | Source |
|---|---|
| `{{goal}}` | Active sprint record's `goal` field (`.momentum/sprints/index.json` → `active.goal`), read via a targeted query — not a whole-file Read |
| `{{waves}}` | Active sprint record's `waves` list (`active.waves`) — wave number → ordered story slugs |
| `{{contract_path}}` per story | `active.team.story_assignments[slug].contract.path`, just persisted in Step 8.B (equivalently `{{contract_metadata[story_slug].contract_path}}`, already in scope) |
| `{{cautions}}` | Union of: (a) coverage-plan.md's `## Known Guard Failures` section, if `{{guard_status}}` == `"accepted_with_failures"` (Step 3.5); (b) `{{avfl_result}}` == `"CHECKPOINT_WARNING"` findings the developer proceeded past (Step 6); (c) per-fork caveats from the developer's pasted plan-gate sign-off block, if `{{genuine_forks\|count}}` > 0 (Step 7). Empty list if none of these produced content. |

## 5. Example (fully rendered)

```
This is a use-then-discard build bridge for the next `/momentum:conduct` session. Delete this
file once the build session has consumed it — handoffs are ephemeral, not preserved as history.

# Build Handoff — sprint-2026-07-13

## Sprint Goal

The agent cohort goes live: the composition stack — Momentum's own KB, the manifesto producer,
and routing-table resolution — lands and is proven by the shipped E2E driver passing live
against the nornspun fixture with observed PASS output.

## Stories by Wave

### Wave 1
- `momentum-knowledge-base-buildout`
- `manifesto-builder-skill-generate-then-curate`

### Wave 2
- `rename-base-body-files-to-canonical-naming`

## Contract / Spec Locations

- `momentum-knowledge-base-buildout`: `.momentum/sprints/sprint-2026-07-13/specs/momentum-knowledge-base-buildout.eval.yaml`
- `manifesto-builder-skill-generate-then-curate`: `.momentum/sprints/sprint-2026-07-13/specs/manifesto-builder-skill-generate-then-curate.eval.yaml`
- `rename-base-body-files-to-canonical-naming`: `.momentum/sprints/sprint-2026-07-13/specs/rename-base-body-files-to-canonical-naming.eval.yaml`
- Coverage plan: `.momentum/sprints/sprint-2026-07-13/coverage-plan.md`

## Planning-Time Cautions

No planning-time cautions raised.
```
