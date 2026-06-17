# Re-entry — Agent Cohort / Manifesto Thread

**Date:** 2026-06-17
**Purpose:** Pick-up point for a fresh session (the prior session ended on a terminal issue).
This is an *open* re-entry, not a task list — get your bearings from the linked artifacts, then
explore the threads below **with the developer**. Do not map out a sprint unprompted.

---

We're picking up an in-flight thread on Momentum's agent cohort. The developer wants to think it
through together, not be handed a plan.

## Where things stand — read these first, then discuss

- **DEC-038** — `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`
  Manifesto = a **stable per-agent "diagnostic table"** (observable symptom → exact `wiki-query`);
  **per-project, multi-KB**; agents are **project-scoped**. Includes a phased plan + two gates.
- **Recovery brief** (how we got to DEC-038) — `.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md`
- **The recovered prototype** the design is based on — `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`
  (verbatim nornspun `cmp-dev.md`; ~35 worked symptom→`wiki-query` entries across 9 tech areas)
- **The two June-14 audits this started from** —
  `.momentum/handoffs/conduct-subskills-audit-2026-06-14.html` and
  `.momentum/handoffs/agent-cohort-audit-2026-06-14.html`
- **Two fresh backlog stubs** — `momentum-knowledge-base-buildout`,
  `manifesto-builder-skill-generate-then-curate` (epic: `momentum-agent-composition-pipeline`)

## The bigger picture

The developer chose **"Path A"** — build out the agent cohort for real (realize DEC-020–027). The
idea is that the **conduct sub-skill fixes** (the `finding_id` contract bug + the ledger idempotency
cluster — **not yet storied**) ride in the **same sprint** as the cohort work. The verified keystone
is `build-agents` (the missing orchestrator, a.k.a. the `build-guidelines-skill` stub): until it
exists, the routing table stays empty and `agent resolve` only ever returns generic `dev`.

## Open threads — explore, don't resolve

- Whether the manifesto should be **hand-authored or generated-then-curate** (DEC-038 Gate G2).
- Whether **"SM" is actually a real spawnable role** (or should be dropped from DEC-020 scope).
- What **standing up Momentum's own KB** really involves.
- Whether the old **May-16 story stubs need a refresh** (`momentum:refine`) before any of this.
- And honestly — **where it makes the most sense to start.**

## How to begin

Get your bearings from the docs above, then **talk it through with the developer** and see where it
goes. Don't prescribe a sprint plan; follow the developer's lead.

---

### State as of session change (all committed; pushed where noted)
- `DEC-038` + registry — committed & **pushed** (`5a44397`).
- Recovery brief + exemplar — committed & **pushed** (`1bdf4e8`).
- Two intake stubs + index/ledger/beads — committed **locally** (`47de4fb`, *not pushed*).
- `nornspun-client/.claude/agents/cmp-dev.md` — committed & **pushed** (`29f1a25`) so the prototype is safe.
- Next natural step (when the developer is ready): planning for the agent-cohort sprint, keystone-first.
