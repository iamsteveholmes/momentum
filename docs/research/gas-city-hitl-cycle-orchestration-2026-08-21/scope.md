---
topic: "Gas City HITL gates and cycle orchestration for Momentum"
goals: "Assess whether Gas City can orchestrate Momentum's full triage→planning→conduct→retro cycle with human-in-the-loop gates at decision points; validate [steps.gate] behavior hands-on against current releases; determine what adoption would force on the open DEC-028 beads Dolt go/no-go; produce the evidentiary basis for exercising DEC-035's revisit clause."
profile: heavy
date: 2026-08-21
sub_questions:
  - "Gate mechanics hands-on: install gc, author a minimal v2 formula with a [steps.gate] step, and empirically verify the gate bead blocks downstream steps and manual closure releases the graph"
  - "Human-verdict patterns: check-loops/[template.check] with human-recorded verdicts in bead metadata — supported conventions in gascity-packs, converge manual gates, approve/iterate/reject semantics"
  - "Notification and watcher layer: gate-bead bead.created events to human notification — what exists today (dashboard, gc events --follow, mail) and what Momentum would need to build"
  - "Cycle orchestration fit: formulas + orders chaining triage→planning→conduct→retro via exec steps running claude -p /momentum:* — harness recipes for Claude Code as the agent runtime"
  - "Maturity and open bugs: O3 status; wedge bugs #2131/#2168, barrier race #2311, container-gate gap #3451; release cadence and v1→v2 breaking changes since May 2026"
  - "Beads coupling and DEC-028 implications: what Gas City requires of beads (Dolt vs GC_BEADS=file in current releases); what adoption forces on the open Dolt migration go/no-go"
  - "HITL alternative patterns: assignee-to-human steps, mail-to-human, converge gates — which fits Momentum's plan gate vs results gate vs mid-story tooling gates (human-facing tools like nornspun/chorgi)"
  - "Production evidence: who runs human-gated formulas in the wild; maintainer guidance on HITL today"
---

# Research Scope: Gas City HITL gates and cycle orchestration for Momentum

**Date:** 2026-08-21
**Profile:** heavy
**Goals:** Assess whether Gas City can orchestrate Momentum's full triage→planning→conduct→retro cycle with human-in-the-loop gates at decision points; validate [steps.gate] behavior hands-on against current releases; determine what adoption would force on the open DEC-028 beads Dolt go/no-go; produce the evidentiary basis for exercising DEC-035's revisit clause.

## Sub-Questions

1. Gate mechanics hands-on: install gc, author a minimal v2 formula with a [steps.gate] step, and empirically verify the gate bead blocks downstream steps and manual closure releases the graph
2. Human-verdict patterns: check-loops/[template.check] with human-recorded verdicts in bead metadata — supported conventions in gascity-packs, converge manual gates, approve/iterate/reject semantics
3. Notification and watcher layer: gate-bead bead.created events to human notification — what exists today (dashboard, gc events --follow, mail) and what Momentum would need to build
4. Cycle orchestration fit: formulas + orders chaining triage→planning→conduct→retro via exec steps running claude -p /momentum:* — harness recipes for Claude Code as the agent runtime
5. Maturity and open bugs: O3 status; wedge bugs #2131/#2168, barrier race #2311, container-gate gap #3451; release cadence and v1→v2 breaking changes since May 2026
6. Beads coupling and DEC-028 implications: what Gas City requires of beads (Dolt vs GC_BEADS=file in current releases); what adoption forces on the open Dolt migration go/no-go
7. HITL alternative patterns: assignee-to-human steps, mail-to-human, converge gates — which fits Momentum's plan gate vs results gate vs mid-story tooling gates (human-facing tools like nornspun/chorgi)
8. Production evidence: who runs human-gated formulas in the wild; maintainer guidance on HITL today

## Prior Decisions (context for synthesis)

- DEC-032 (2026-05-22): adopted Gas City as dispatcher; superseded by DEC-035
- DEC-035 (2026-05-30): conduct adopted as execution engine; Gas City deferred with revisit clause = "out-of-session or multi-Conductor goal appears"
- DEC-028 (2026-05-16): beads dual-write spike; Dolt migration go/no-go flagged ready 2026-06-18, still open
