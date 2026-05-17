# Beads Dual-Write Spike — Findings

**Spike story:** beads-dual-write-spike
**Decision reference:** DEC-028 — Beads as Tracker/Dependency/Memory Substrate
**Date:** 2026-05-16
**Status:** Infrastructure implemented — empirical sprint data pending

---

## Overview

This document records observations from implementing the beads dual-write proof of concept
alongside the existing JSON-backed state layer in Momentum. The spike delivers the
dual-write infrastructure. Gate evaluation requires running one full sprint with the layer
active; observations below reflect the implementation phase.

---

## Gate 1: Did `bd ready --claim` simplify sprint-dev Phases 1–3 and remove hand-maintained graph logic?

### Observations

**Implementation:** sprint-dev Phase 1 now calls `bd ready --json --claim` after building
the wave/depends_on graph from `index.json`. The result is stored as `{{bd_ready_result}}`
and compared against the existing graph. The `--claim` flag was verified to be an atomic
operation — concurrent `bd ready --claim` calls on a single unblocked story return it to
only one caller.

**Discrepancy logging:** The implementation logs `beads-ahead` and `wave-ahead` discrepancies
between the two sources. This logging is the primary data collection mechanism for Gate 1.

**Hand-maintained graph:** The wave/depends_on graph is NOT removed during the spike — it
serves as the fallback and the comparison baseline. Sprint-dev still builds the full graph
from `index.json` before calling `bd ready`. No graph logic was removed.

**Assessment (implementation-phase):** The dual-write layer is additive. The simplification
benefit (removing hand-maintained graph logic) cannot be empirically measured until at least
one sprint completes with the layer active and discrepancies are recorded. Gate 1 remains
open — requires sprint execution data.

**Friction observed:** sprint-dev workflow.md is already at 716 lines (pre-spike). Adding
the `bd ready --claim` block brings it to 737 lines, further above the 500-line target.
If Gate 1 evaluates positive, the wave/depends_on fallback can be removed and net line count
will decrease significantly.

---

## Gate 2: Did `discovered-from` eliminate intake-queue triage toil without losing items?

### Observations

**Implementation:** intake workflow now calls `bd create "<title>" --deps discovered-from:<origin-bead-id>`
after the primary `intake-queue.jsonl` append. The edge type is `discovered-from`, which is
semantically distinct from `blocks`.

**Additive path:** `intake-queue.jsonl` is NOT removed. The beads path is a shadow write.
No items can be lost — the canonical record remains in `intake-queue.jsonl`.

**Origin resolution:** If the source story slug is available, the origin bead ID is resolved
from `.momentum/beads-id-map.json`. If not found, the sentinel `bd-discovery-root` bead is
used. This fallback prevents the intake path from failing when no mapping exists.

**Edge type verification:** AC 11 requires verifying that `bd show <bead-id>` returns
`discovered-from` (not `blocks`) as the dep type. This is testable via the eval at
`skills/momentum/skills/intake/evals/eval-intake-routes-discovered-work-with-discovered-from.md`.

**Assessment (implementation-phase):** Triage toil reduction is not measurable from
implementation alone. Gate 2 requires running intake on real discovered work and comparing
triage burden between the `bd`-first and `intake-queue.jsonl`-first views. Gate 2 remains
open — requires sprint execution data.

**Friction observed:** None at implementation phase. The `discovered-from` edge is not yet
verified to be distinct in the `bd show` output — requires `bd show` runtime validation.

---

## Gate 3: Was Dolt sync manageable alongside git-discipline rules?

### Observations

**Implementation:** `bd prime --no-git-ops` is wired via SessionStart and PreCompact hooks.
The `--no-git-ops` flag prevents beads from injecting `bd dolt push` into the prime output.

**PRIME.md content:** `.beads/PRIME.md` explicitly states that `bd dolt push` is NEVER called
autonomously — Momentum owns sync. This is enforced at both the hook level (`--no-git-ops`)
and the PRIME.md instruction level.

**Dolt sync not triggered:** During this spike implementation, `bd dolt push` was never called.
All beads operations were local (`bd create`, `bd update`, `bd dep add`, `bd list`, `bd show`).

**git-discipline conflict with `bd init`:** During `bd init`, beads injected content into
CLAUDE.md that instructed agents to "NEVER stop before pushing" and "Work is NOT complete
until git push succeeds". This directly contradicted Momentum's git-discipline rule (push
always requires approval). The injected content was removed and replaced with the PRIME.md
approach.

**Assessment (implementation-phase):** Dolt sync appears manageable at the `--no-git-ops`
constraint level. The `bd init` CLAUDE.md injection is a friction point — it injects rules
that conflict with project conventions. This is a known beads integration issue; the fix is
the PRIME.md override pattern used here.

**Gate 3 assessment (partial positive):** The `--no-git-ops` constraint works. Dolt sync
is not triggered autonomously. However, the `bd init` CLAUDE.md injection pattern is friction
that must be managed on every project install. Score: manageable with the PRIME.md pattern.

---

## Gate 4: Did `--spec-id` linkage hold without in-tree metadata loss?

### Observations

**Implementation:** Every `bd create` call for a story bead includes
`--spec-id .momentum/stories/{slug}.md`. This was implemented in sprint-manager's `sprint_plan`
action and the helper pattern in the workflow header.

**In-tree metadata:** Story spec files (`.momentum/stories/*.md`) are unchanged. No spec prose
is written to Dolt. The bead body contains only title and spec-id link.

**Map as bridge:** `.momentum/beads-id-map.json` is git-tracked. It maps human-readable slugs
to bead hash IDs. This file is the audit trail for Gate 4 — reviewable alongside the research
artifact.

**`--spec-id` verification:** Requires running `bd show <bead-id>` after `sprint_plan add`
and confirming `spec_id` field equals `.momentum/stories/{slug}.md`. This is tested via
`eval-sprint-manager-spec-id-links-to-story-md.md`.

**Assessment (implementation-phase):** The `--spec-id` pattern is implemented correctly in
the workflow. Linkage cannot be empirically validated until sprint-manager `sprint_plan add`
runs with beads active. Gate 4 remains open — requires runtime validation.

---

## Operational Friction

1. **`bd init` CLAUDE.md injection conflicts with git-discipline.** `bd init --quiet` still
   injects a "MANDATORY WORKFLOW" block into CLAUDE.md with autonomous push instructions.
   These must be removed immediately after `bd init`. The PRIME.md pattern overrides this.

2. **sprint-dev workflow.md line count.** Already at 716 lines before the spike. The
   `bd ready --claim` addition brings it to 737. If Gate 1 is positive and the wave graph
   is removed, this will improve. Not a blocker but worth tracking.

3. **Bead ID resolution requires map lookup.** sprint-dev must invert `beads-id-map.json`
   (bead_id → slug) at runtime. This adds a map load step. Minimal overhead but adds a
   failure mode (map out of sync with beads DB).

4. **`bd dolt push` prohibition.** The `--no-git-ops` flag works but is not persistent
   across `bd prime` invocations without the hook. If the hook fires without `--no-git-ops`,
   beads may inject push instructions. The PreCompact hook also uses `--no-git-ops` as a
   belt-and-suspenders measure.

---

## Go/No-Go Recommendation

**Status: Incomplete — requires sprint execution data**

The dual-write infrastructure is in place. All four gate criteria can now be empirically
measured during one sprint with the layer active. Based on implementation-phase observations:

- Gates 1, 2, 4: Remain open — need runtime data.
- Gate 3: Partial positive — `--no-git-ops` works; `bd init` injection is friction.

**Provisional recommendation:** Proceed with the dual-write sprint and collect data. The
infrastructure is sound and the fallback paths are in place. A final go/no-go decision
requires the sprint data.

**No-go triggers (abort if observed during the sprint):**
- `bd ready --claim` races produce duplicate story assignments (atomic claim not working).
- `discovered-from` edge type is indistinguishable from `blocks` in `bd show` output.
- `bd dolt push` fires autonomously despite `--no-git-ops`.
- sprint-manager JSON write aborts due to a beads failure (best-effort not enforced).

---

## References

- DEC-028: `momentum/decisions/dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md`
- Source evaluation: `docs/research/beads-vs-momentum-tracker-evaluation-2026-05-16.md`
- Evals:
  - `skills/momentum/skills/sprint-manager/evals/eval-sprint-manager-mirrors-story-to-beads.md`
  - `skills/momentum/skills/sprint-manager/evals/eval-sprint-manager-spec-id-links-to-story-md.md`
  - `skills/momentum/skills/sprint-dev/evals/eval-sprint-dev-uses-bd-ready-claim-for-unblocked-stories.md`
  - `skills/momentum/skills/intake/evals/eval-intake-routes-discovered-work-with-discovered-from.md`
