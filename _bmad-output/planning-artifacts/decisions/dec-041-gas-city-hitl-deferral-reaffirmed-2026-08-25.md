---
id: DEC-041
title: Gas City HITL Evaluation — Deferral Reaffirmed, Notification as Hard HITL Requirement, Stop-Before-Push
date: '2026-08-25'
status: decided
source_research:
  - path: docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/final/gas-city-hitl-cycle-orchestration-final-2026-08-21.md
    type: research-synthesis
    date: '2026-08-25'
  - path: docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/raw/practitioner-notes.md
    type: developer-conversation
    date: '2026-08-25'
prior_decisions_reviewed:
  - DEC-028 (Beads dual-write spike — Dolt migration go/no-go, still open)
  - DEC-032 (Gas City as dispatcher — superseded by DEC-035)
  - DEC-035 (Conduct execution engine — Gas City deferred with revisit clause)
architecture_decisions_affected:
  - DEC-035 — REAFFIRMED: the deferral stands; neither revisit trigger (out-of-session goal, multi-Conductor goal) has fired. Capability existing ≠ goal appearing.
  - DEC-028 — UNTOUCHED: the go/no-go remains open and independently decidable; the research adds only that Gas City adoption, if it ever happens, carries a scoped city-local bd/Dolt requirement for the gate primitive.
---

# DEC-041: Gas City HITL Evaluation — Deferral Reaffirmed, Notification as Hard HITL Requirement, Stop-Before-Push

## Summary

A heavy-profile research engagement (8 subagents + Gemini triangulation + hands-on gc 1.4.1
testing on this machine, hardened by four adversarial validation rounds) evaluated whether Gas
City can orchestrate Momentum's full triage→planning→conduct→retro cycle with human gates at
the developer's approval points. The gate-blocking mechanics proved out empirically, but no
shipped release notifies the developer that a gate is waiting, the post-fan-out barrier the
results gate needs has no proven construction upstream, and the adoption cost floor is 4–7+
weeks. The developer ratified four decisions at the 2026-08-25 decision gate: the DEC-035
deferral stands; rich notification + bidirectional developer interaction is a hard requirement
for any HITL orchestration (making the silent-gate gap the disqualifying one); any future
unattended cycle terminates before push; and the four residual empirical unknowns ship as
recorded pre-adoption checks.

---

## Decisions

### D1: DEC-035's Gas City Deferral — REAFFIRMED

**Research recommended:** Score the corpus against DEC-035 D2's revisit clause ("revisit only
if/when an out-of-session or multi-Conductor goal appears"). Verdict: neither trigger has
fired — every corpus fact is about Gas City's capability, not Momentum's goals; the
multi-Conductor evidence actively weakened the case (single-dispatcher-by-design; the one
exclusion primitive failed in the field with its fix unmerged; multi-city broken on Apple
Silicon).

**Decision:** Reaffirmed. The deferral stands. The corpus files as the evidentiary baseline
for any future revisit.

**Rationale:** Capability existing is not a goal appearing. The developer does not currently
want unattended out-of-session cycles; and were the goal to appear, the silent-gate and
barrier gaps mean the first unattended cycle would strand silently at exactly its
highest-stakes moments.

### D2: Rich Notification + Bidirectional Developer Interaction Is a Hard HITL Requirement — ADOPTED

**Research recommended:** The corpus found Gas City's gate primitive blocks correctly but
"tells nobody" in every tagged release (notify/renudge orders are main/edge-only; the one
shipped watcher deliberately excludes human gates; formula-cooked gates persist
`await_type: null` so even the unreleased reflexes would skip them).

**Decision:** Adopted as a standing requirement, elevating the finding: any HITL orchestration
Momentum runs — with or without Gas City — must provide rich notification and genuinely
bidirectional back-and-forth with the developer. A gate that blocks silently fails the
requirement even where the blocking mechanics are proven. Any future Gas City revisit must
prove the notification + verdict-return layer FIRST, not last.

**Rationale:** Developer, verbatim in substance: "It needs better notifications. It's crucial
we have back and forth and visibility with me (the HITL)." Momentum's in-session gates
(plan gate, results gate surfaces) already meet this bar; an out-of-session design must match
it, not lower it.

### D3: Any Future Unattended Cycle Terminates Before Push — ADOPTED

**Research recommended:** The corpus surfaced a fifth HITL point the four named gates don't
cover: git-discipline requires developer approval for every push, and version-on-release
requires a bump+push at sprint close — so an autonomous cycle must either stop before push,
carry a fifth push-approval gate, or relax the rule.

**Decision:** Adopted: stop before push. A future unattended cycle ends at "merged locally,
ready to push"; push remains a manual, approval-gated session action. No fifth gate, no
git-discipline change.

**Rationale:** Simplest resolution; no new gate machinery; the push-approval rule stays intact.

### D4: Residual Empirical Unknowns Ship as Recorded Pre-Adoption Checks — ADOPTED

**Research recommended:** Four unknowns survived all validation, honestly marked open:
(1) whether bd v1.2.2 carries the CAS write flags (settling command `bd 1.2.2 update --help`
never run — bears on DEC-028's multi-agent-safety row); (2) whether the unreleased notify
orders fire against a properly-typed human gate (inferred from source, never run); (3) the
drain+check barrier's failed-close semantics (completion-assertion guard prescribed, untested);
(4) multi-hour Claude session survival under gc timeouts.

**Decision:** Adopted: ship the research with these recorded as open items. They become
mandatory pre-adoption checks the moment D1's deferral is ever lifted. No probe round now.

**Rationale:** None of the four changes today's verdict; closing them buys nothing while the
deferral stands.

---

## Decision Gates

| Gate | Condition | Action |
|---|---|---|
| Revisit trigger | Developer states an out-of-session or multi-Conductor goal (per DEC-035 D2) | New decision required; adoption pre-flight runs in order: notification/verdict-return layer proven first (D2), then the four D4 probes, then barrier construction, then cost re-estimate (floors: 15–25d rewrite + 5.5–9d glue for first gate type, city standup uncosted) |
