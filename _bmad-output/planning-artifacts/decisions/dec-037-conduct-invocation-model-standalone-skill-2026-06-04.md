---
id: DEC-037
title: Conduct Invocation Model — Standalone /momentum:conduct Skill, Coexisting with sprint-dev (resolves spec §13 Q6)
date: '2026-06-04'
status: decided
source_research:
  - path: .momentum/handoffs/sprint-2026-06-02-conduct-core-hitl-report.html
    type: end-gate-report
    date: '2026-06-04'
  - path: "(conduct-runnability multi-lens discovery, 2026-06-04)"
    type: discovery
    date: '2026-06-04'
prior_decisions_reviewed:
  - DEC-035 (Conduct Execution Engine — conduct adopted; in-session; ships as the engine, sprint-dev sequencing)
  - DEC-036 (Conduct HITL Calibration — stakes-and-timing escalation)
architecture_decisions_affected:
  - "Resolves spec §13 Open Question 6 (Conductor as a separate skill vs. sprint-dev's top-level session)."
  - "Reconciles spec §10/§12 — the redesign's 'replace the build phase inside sprint-dev/workflow.md' is reframed as the eventual ADOPTION step, not the initial integration. conduct ships as a standalone skill first; sprint-dev's wave loop is retired at adoption."
---

# DEC-037: Conduct Invocation Model — Standalone /momentum:conduct Skill, Coexisting with sprint-dev

## Summary

The conduct core-build sprint (`sprint-2026-06-02-conduct-core`) shipped the Conductor as a **standalone skill**
(`skills/momentum/skills/conductor/`), but spec §10/§12 describe the redesign as *replacing the build phase inside
`sprint-dev/workflow.md`*. The built artifact and the spec's stated integration point disagreed — spec §13 Q6
flagged exactly this fork, and the conduct-runnability discovery found it gates every downstream invocation
decision (the command file, the caller/discovery route, and — subtly — who may legitimately run `git push`).

**Decision: Option A — conduct is a standalone `/momentum:conduct` skill that coexists with `sprint-dev`.** A thin
command invokes the existing conductor skill as the top-level session; `sprint-dev` remains the live builder,
unchanged, until conduct is proven runnable end-to-end; `sprint-dev` is retired later as a distinct adoption step.

## Decision

### D1: Conduct is invoked as a standalone `/momentum:conduct` skill, coexisting with sprint-dev — ADOPTED

The built standalone `conductor` skill is kept. A new `/momentum:conduct` command invokes it **as the top-level
session**. `sprint-dev` is not rewritten now; the two builders coexist during the transition. Retiring sprint-dev's
wave loop is a separate, later adoption step (the `conduct-adoption-retire-sprint-dev` backlog item).

**Rationale:**
- **Matches what's built.** The artifact is already a standalone skill; Option A is the lower-delta, lower-risk path.
- **Matches the developer's stated intent** — a distinct, discoverable `/momentum:conduct` command.
- **Lowest risk.** It does not rewrite the working `sprint-dev` in place; the current builder keeps working while
  conduct is completed and proven.
- **Resolves the git-push / orchestrator-purity concern.** Orchestrator-purity forbids *spawned / subagent* skills
  from mutating git. A directly-invoked `/momentum:conduct` runs the conductor **as the top-level session**, which
  legitimately owns commits, merges, and the approve-time `git push`. So a standalone skill is sound on this axis.
- **Aligns with DEC-035's sequencing** — conduct ships as the engine; sprint-dev retirement is downstream, not a
  prerequisite to a first runnable conduct.

### Option considered and rejected

**Option B — rewrite `sprint-dev/workflow.md` to BE the Conductor (fold the standalone skill in).** Matches spec
§10/§12 literally and yields a single builder with the existing `/momentum:sprint-dev` entry + Impetus dispatch
already wired. **Rejected because:** it rewrites the *working* builder in place (high risk before conduct is
proven), provides no distinct `/momentum:conduct` command (the developer's stated intent) without adding an alias,
and makes the just-built standalone conductor skill redundant. Its one real advantage — matching the spec's stated
integration point and avoiding two coexisting builders — is preserved by deferring it to the adoption step.

## Reconciliation with the spec and DEC-035

| Spec / prior statement | DEC-037 reconciliation |
|---|---|
| spec §10/§12: "replace the build phase inside `sprint-dev/workflow.md`" | Reframed as the **adoption** step (`conduct-adoption-retire-sprint-dev`), performed *after* conduct is runnable and proven — not the initial integration. |
| spec §13 Q6: separate skill vs. sprint-dev session | **Resolved: separate skill** (standalone `/momentum:conduct`), top-level-session invoked. |
| DEC-035: ship conduct as the engine; sprint-dev retires later | Honored directly — coexist now, retire at adoption. |

## Implications / sequencing (updates the runnability roadmap)

- `conduct-entry-point-command` — build a `/momentum:conduct` command (resolve the `conduct` vs `conductor` name)
  that invokes the standalone skill as the top-level session.
- `conduct-register-skill-and-refresh-cache` — confirm user-invocable frontmatter + marketplace refresh so the
  skill registers.
- `conduct-wire-caller-and-discovery` — **narrowed by this decision**: surface `/momentum:conduct` (e.g. via
  Impetus) and ensure it dispatches to `conductor/workflow.md`. **Do NOT rewrite `sprint-dev`** as part of making
  conduct runnable — sprint-dev coexists untouched.
- `conduct-adoption-retire-sprint-dev` (eventual) — once conduct is proven, make it the default and retire
  sprint-dev's wave loop (this is where spec §10/§12's "replace inside sprint-dev" is finally honored).

## Decision Gates

- **The coexistence is temporary by design.** If two builders drift or cause confusion before adoption, accelerate
  the adoption step rather than maintaining both indefinitely.
- **The git-push soundness depends on `/momentum:conduct` running as the top-level session.** If a future change
  ever makes conduct a *spawned* skill, the push authority must be re-examined (a subagent must not push).
