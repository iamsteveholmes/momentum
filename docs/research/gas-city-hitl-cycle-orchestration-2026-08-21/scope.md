---
topic: "Gas City HITL gates and cycle orchestration for Momentum"
goals: "Assess whether Gas City can orchestrate Momentum's full triage→planning→conduct→retro cycle with human-in-the-loop gates at decision points; validate [steps.gate] behavior hands-on against current releases; determine what adoption would force on the open DEC-028 beads Dolt go/no-go; produce the evidentiary basis for exercising DEC-035's revisit clause."
profile: heavy
date: 2026-08-21
sub_questions:
  - "Gate mechanics hands-on: install gc, author a minimal v2 formula with a [steps.gate] step, and empirically verify the gate bead blocks downstream steps and manual closure releases the graph"
  - "Human-verdict patterns: check-loops/[template.check] with human-recorded verdicts in bead metadata — supported conventions in gascity-packs, converge manual gates, approve/iterate/reject semantics"
  - "Notification and watcher layer: gate-bead bead.created events to human notification — what exists today (dashboard, gc events --follow, mail) and what Momentum would need to build"
  - "Cycle orchestration fit: formulas + orders chaining triage→planning→conduct→retro via exec steps running claude -p /momentum:* — harness recipes for Claude Code as the agent runtime (premise refuted — CRIT-005; see research-cycle-orchestration-fit.md §1)"
  - "Maturity and open bugs: O3 status; wedge bugs #2131/#2168, barrier race #2311, container-gate gap #3451; release cadence and v1→v2 breaking changes since May 2026"
  - "Beads coupling and DEC-028 implications: what Gas City requires of beads (Dolt vs GC_BEADS=file in current releases); what adoption forces on the open Dolt migration go/no-go"
  - "HITL alternative patterns: assignee-to-human steps, mail-to-human, converge gates — which fits Momentum's plan gate vs results gate vs mid-story tooling gates (human-facing tools like nornspun/chorgi)"
  - "Production evidence: who runs human-gated formulas in the wild; maintainer guidance on HITL today"
  - "DEC-035 revisit-clause scoring: out-of-session and multi-Conductor triggers — assembled evidence and verdict (added post-AVFL to close the MAJ-012 coverage gap; goal #4)"
  - "Live verification probes: GC_BEADS=file, FileStore metadata durability, gate persistence on file store, dashboard port, deps.env BD pin — settling AVFL-flagged contradictions (added during the AVFL fix pass to settle CRIT-004/MAJ-007/MAJ-008 with live gc 1.4.1 evidence)"
---

# Research Scope: Gas City HITL gates and cycle orchestration for Momentum

**Date:** 2026-08-21
**Profile:** heavy
**Goals:** Assess whether Gas City can orchestrate Momentum's full triage→planning→conduct→retro cycle with human-in-the-loop gates at decision points; validate [steps.gate] behavior hands-on against current releases; determine what adoption would force on the open DEC-028 beads Dolt go/no-go; produce the evidentiary basis for exercising DEC-035's revisit clause.

## Sub-Questions

1. Gate mechanics hands-on: install gc, author a minimal v2 formula with a [steps.gate] step, and empirically verify the gate bead blocks downstream steps and manual closure releases the graph
2. Human-verdict patterns: check-loops/[template.check] with human-recorded verdicts in bead metadata — supported conventions in gascity-packs, converge manual gates, approve/iterate/reject semantics
3. Notification and watcher layer: gate-bead bead.created events to human notification — what exists today (dashboard, gc events --follow, mail) and what Momentum would need to build
4. Cycle orchestration fit: formulas + orders chaining triage→planning→conduct→retro via exec steps running claude -p /momentum:* — harness recipes for Claude Code as the agent runtime (premise refuted — CRIT-005; see `research-cycle-orchestration-fit.md` §1)
5. Maturity and open bugs: O3 status; wedge bugs #2131/#2168, barrier race #2311, container-gate gap #3451; release cadence and v1→v2 breaking changes since May 2026
6. Beads coupling and DEC-028 implications: what Gas City requires of beads (Dolt vs GC_BEADS=file in current releases); what adoption forces on the open Dolt migration go/no-go
7. HITL alternative patterns: assignee-to-human steps, mail-to-human, converge gates — which fits Momentum's plan gate vs results gate vs mid-story tooling gates (human-facing tools like nornspun/chorgi)
8. Production evidence: who runs human-gated formulas in the wild; maintainer guidance on HITL today
9. DEC-035 revisit-clause scoring: out-of-session and multi-Conductor triggers — assembled evidence and verdict (`raw/research-dec035-revisit-triggers.md`, added 2026-08-24 to close the coverage gap flagged by AVFL finding MAJ-012 — the original 8 sub-questions covered the out-of-session trigger only incidentally and the multi-Conductor trigger not at all)
10. Live verification probes: GC_BEADS=file, FileStore metadata durability, gate persistence on file store, dashboard port, deps.env BD pin — settling AVFL-flagged contradictions (`raw/research-verification-probes.md`, added 2026-08-24 during the AVFL fix pass to settle CRIT-004/MAJ-007/MAJ-008 with live gc 1.4.1 evidence)

## Evidence notation note (added during AVFL fix pass — STRUCTURAL-A-005)

This corpus uses a fourth evidence tag beyond the standard three (`[OFFICIAL]` docs/source-grounded, `[PRAC]` practitioner-sourced, `[UNVERIFIED]` inference): **`[EMPIRICAL]`** — a claim established by first-hand reproduction (a command actually run, a probe actually executed, a file actually fetched and inspected during this research), as opposed to `[OFFICIAL]`'s reliance on documentation or source-code text describing intended behavior without confirming it was exercised. `[EMPIRICAL]` carries the **highest trust for behavioral claims** in this corpus — it is evidence that something was observed to actually happen, not merely documented to be intended. This tag is used extensively across all 10 raw research files (including `research-verification-probes.md`) but was not defined anywhere in the corpus prior to this note. **Process note for the practice:** the underlying `momentum:research` skill's evidence-tag template does not define a fourth tag either; this is a corpus-local fix, not a skill fix. A skill-level template update (adding `[EMPIRICAL]` as a first-class tag alongside `[OFFICIAL]`/`[PRAC]`/`[UNVERIFIED]`) should be routed through Momentum's `momentum:upstream-fix` process separately — recorded in `validation/fix-log-iter1.md` rather than applied here.

### Correction markers and finding IDs (added during AVFL fix pass — COHERENCE3-A-009)

Alongside the evidence tags, the raw research files carry a second, structurally different kind of inline annotation: **correction markers**. They look like evidence tags but are not — they are edit provenance, recording that a passage was changed after adversarial validation and why.

- **Form.** A bracketed, usually bolded lead-in such as `**[Corrected during AVFL fix pass — CRIT-004]**`, `**[Scoped per ACCURACY2-A-001]**`, `**[Reworded during AVFL fix pass — ACCURACY2-A-010]**`, or a trailing `*Correction history: …*` note. A marker always names the finding ID that prompted the edit.
- **What a marker means.** The text it introduces is the **current, corrected** claim. A marker is never a warning that the surrounding text is wrong; where a superseded claim is quoted for the record, it is named explicitly as retracted (pattern: *"the pre-X framing is retracted and is superseded by the text that follows"*).
- **Reading order.** From iteration 3 onward the convention is **conclusion first, correction history trailing** — the settled claim leads the passage, and the edit provenance is compressed into a short closing note. Passages that still lead with a marker predate that convention.
- **Finding-ID grammar.** `<LENS><ITER>-<ROLE>-<NNN>` — lens is `ACCURACY` / `COHERENCE` / `DOMAIN` / `STRUCTURAL`; the iteration digit is present from iteration 2 onward and absent on iteration-1 IDs; role is `A` (adversary) or `E` (enumerator). So `ACCURACY3-A-002` is accuracy lens, iteration 3, adversary, finding 2; `DOMAIN-A-011` is a first-iteration domain-adversary finding. Severity-prefixed IDs (`CRIT-004`, `MAJ-011`, `MIN-006`, `LOW-001`) are the consolidator's post-dedup numbering for that iteration.
- **Where the IDs resolve.** Per-lens findings live in `validation/findings/` (iteration 1), `validation/findings-iter2/`, and `validation/findings-iter3/`. Consolidated, deduplicated findings live in `validation/avfl-consolidated.md`, `avfl-consolidated-iter2.md`, and `avfl-consolidated-iter3.md`; fix records live in `validation/fix-log-iter1.md`, `fix-log-iter2.md`, and `fix-log-iter3.md`. **`MERGED-*` IDs are iteration-2 cross-lens merge identifiers and resolve only in `validation/avfl-consolidated-iter2.md`** (with their fixes recorded in `fix-log-iter2.md`) — they do not appear in any per-lens findings file, which is why `MERGED-002` cannot be found by grepping `validation/findings*/`.

- DEC-032 (2026-05-22): adopted Gas City as dispatcher; superseded by DEC-035
- DEC-035 (2026-05-30): conduct adopted as execution engine; Gas City deferred with revisit clause = "out-of-session or multi-Conductor goal appears"
- DEC-028 (2026-05-16): beads dual-write spike; Dolt migration go/no-go flagged ready 2026-06-18, still open
