---
id: DEC-012
title: Retire `.momentum/sprints/{slug}.json` Per-Sprint State File
date: '2026-04-30'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-04-30'
prior_decisions_reviewed:
  - DEC-011 D3 (State Source Paths Under `.momentum/` — clarified for canvas reads only; this DEC explicitly retires the per-sprint file at the state-model level)
stories_affected:
  - fix-per-sprint-json-contract-drift
  - impetus-momentum-state-migration
---

# DEC-012: Retire `.momentum/sprints/{slug}.json` Per-Sprint State File

## Summary

A two-source-of-truth contract drift surfaced during dispatch of `sprint-2026-04-27`: the spec stack (two skill workflows and three sections of `architecture.md`) continued to describe a per-sprint JSON state file at `.momentum/sprints/{slug}.json`, while the implementation (`momentum-tools.py`) has never written this file — it has only ever written the holistic `sprints/index.json`. DEC-011 D3 narrowed what the canvas reads to the holistic index, but stopped short of formally retiring the per-sprint file pattern at the underlying state-model level. This decision closes that gap: the per-slug JSON file is formally retired across the entire spec stack, and `sprints/index.json` (with its `active`, `planning`, `completed[]`, `quickfixes[]` sections) is the canonical sprint state source going forward. Per-sprint **subdirectories** (`{slug}/specs/`, `{slug}/sprint-summary.md`, retro artifacts, audit-extracts) remain — only the per-slug **JSON file** is retired.

---

## Decisions

### D1: Retire the `.momentum/sprints/{slug}.json` Per-Sprint State File — ADOPTED

**Developer framing:** During dispatch of `sprint-2026-04-27`, sprint-dev/workflow.md halted in Phase 1 attempting to read `sprints/{sprint_slug}.json` — a file that does not exist on disk and has never existed. Investigation against `momentum-tools.py` (the sole declared writer) confirmed that the cmd_sprint_activate, cmd_sprint_complete, and planning paths only ever read and write `sprints/index.json`. The per-sprint file has lived in the spec stack only, never in code. Two parallel descriptions of sprint state (a per-sprint file and a holistic index) would invite drift even if the per-sprint file were implemented; one canonical source eliminates that risk by construction.

**Decision:** Retire the `.momentum/sprints/{slug}.json` per-sprint state file pattern. The holistic `sprints/index.json` — with its `active`, `planning`, `completed[]`, and `quickfixes[]` sections — is the canonical sprint state source. All readers (skill workflows, the canvas, future tooling) read from `sprints/index.json`. The sole writer remains `momentum-tools sprint`. Per-sprint **subdirectories** (`{slug}/specs/`, `{slug}/sprint-summary.md`, `{slug}/retro-transcript-audit.md`, `{slug}/audit-extracts/`) are explicitly preserved — only the per-slug **JSON file** is retired.

**Rationale:**

- The implementation has lived without a per-sprint file for the entire project history with no missing capability. The active sprint can be fully described from the `active` block alone.
- The holistic `active` block already carries every field the per-sprint file was designed to hold (slug, locked, started, status, stories, team.story_assignments, waves, approvals). There is no field on the per-sprint file design that is not already present on the active block.
- Two sources of truth for sprint state would invite drift; a single source eliminates it by construction. Even a correctly-implemented per-sprint file would impose dual-write coordination cost on every sprint mutation.
- Adding a per-sprint writer now would require schema design, migration of existing sprint data (none exists), dual-write protection logic, and downstream skill updates — all to introduce a redundancy.
- DEC-011 D3 implicitly assumed this state model when it pinned the canvas to `sprints/index.json` for sprint state. DEC-012 makes the assumption explicit at the state-model level so the next contributor cannot re-introduce the per-sprint pattern without contradicting an ADOPTED decision.

---

## Status

**ADOPTED — Steve Holmes, 2026-04-30**

Supersedes: none — clarifies a state-model question DEC-011 D3 left ambiguous (D3 specified canvas-read scope only).

---

## Consequences

- **`skills/momentum/skills/sprint-dev/workflow.md`** must read sprint state from `sprints/index.json` `active` block; derive primary ordering from `active.waves` and per-story `depends_on` from `stories/index.json`. No reference to or read of `sprints/{slug}.json` remains.
- **`skills/momentum/skills/sprint-manager/workflow.md`** must drop the three obsolete steps that instructed writes to the per-sprint file (`sprint_activate` step 8, `sprint_complete` step 6, `sprint_plan` step 7). The remaining steps in each procedure exactly match what `momentum-tools.py` already does.
- **`_bmad-output/planning-artifacts/architecture.md`** drops per-sprint file references from three sections: the Read/Write Authority table, the Protection Boundaries list, and the Sprint Tracking Schema folder description. A new `editHistory:` entry records the retirement.
- **File-protection hooks** no longer need to protect a path that never exists — the protection boundary entry for `.momentum/sprints/{slug}.json` is removed.
- **Future tooling** (canvas, future writers, future readers) treats `sprints/index.json` as the single canonical sprint state source. The `active` block is the authoritative description of the in-flight sprint.

---

## Cross-references

- **DEC-011 D3** (`dec-011-project-canvas-implementation-foundations-2026-04-24.md`) — pinned the canvas to read from holistic `sprints/index.json`. DEC-012 makes the per-sprint-file retirement explicit at the state-model level, beyond canvas-read scope. DEC-011 D3 is clarified, not superseded.
- **Story `fix-per-sprint-json-contract-drift`** — implements this decision across `architecture.md` and the two affected `workflow.md` files. The story is the enacting artifact for DEC-012.
- **Story `impetus-momentum-state-migration`** (Wave 1 of `sprint-2026-04-27`) — relocates state from `_bmad-output/implementation-artifacts/...` to `.momentum/...`. The relocation honors DEC-012: no per-sprint JSON file appears in the new location either. The `active` block shape and the `index.json` filename are preserved by the migration, so DEC-012 survives intact.

---

## Implementation Impact

The four touches that enact DEC-012 (story `fix-per-sprint-json-contract-drift`):

1. **This decision document** — `_bmad-output/planning-artifacts/decisions/dec-012-retire-per-sprint-state-file-2026-04-30.md` (created).
2. **`_bmad-output/planning-artifacts/architecture.md`** — three sections updated (Read/Write Authority table ~line 1320, Protection Boundaries list ~line 1347, Sprint Tracking Schema ~line 1526) plus a new `editHistory:` entry dated 2026-04-30.
3. **`skills/momentum/skills/sprint-dev/workflow.md`** — Phase 1 read step rewritten against `sprints/index.json` `active` block; ordering derived from `active.waves` + per-story `depends_on` from `stories/index.json`.
4. **`skills/momentum/skills/sprint-manager/workflow.md`** — three obsolete per-sprint-write steps deleted (`sprint_activate` step 8, `sprint_complete` step 6, `sprint_plan` step 7); inline DEC-012 reference added near the top.

A grep for `dec-012` (case-insensitive) across the four enacting artifacts must return at least one match in each, ensuring the decision trail is discoverable from any of them.
