---
content_origin: claude-code-subagent
date: 2026-05-18
sub_question: "Can Hermes Kanban + worker lanes map onto Momentum's sprint/epic/story/wave + beads graph + intake-queue — fit, mismatches, source-of-truth?"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
---

# Hermes Kanban ↔ Momentum: Structural Fit, Impedance Mismatches, and Source-of-Truth Ownership

## BLUF / Verdict

The two models are **semantically close at the work-item layer and structurally incompatible at the ownership layer.** Hermes Kanban's task/link/run/comment/event model maps cleanly, almost field-for-field, onto Momentum's story/dependency/attempt/handoff concepts — close enough that a *projection* is trivial. But both systems are designed as **the authoritative writer of task lifecycle state**, and Momentum has *already* committed beads as its **designated future** tracker/dependency substrate under an enforcing sprint-manager (DEC-028; currently in dual-write spike; `index.json` is still authoritative until spike gates pass — see `beads-vs-momentum-tracker-evaluation-2026-05-16`, `beads-dual-write-spike-findings-2026-05-16`). Putting Hermes Kanban *also* in an authoritative position creates a **three-way split-brain** (Momentum `index.json` ⇄ beads Dolt DB ⇄ Hermes `kanban.db`), each with its own claim semantics and its own dispatcher promoting `todo→ready`. The only safe topology is a **one-way, read-only projection**: beads (the **designated future** system of record per DEC-028; post-spike target state) → a Hermes Kanban *view*, with Hermes owning *nothing* in the work graph and Momentum/beads owning everything. Bidirectional sync is not safe and should be rejected. A Claude-native dispatcher reading `bd ready` directly (per `claude-code-background-dispatcher-2026-05-17` §6 + Beads addendum) dominates Hermes-as-delegate on every axis that matters for the local-only, cost-sensitive, Claude-skill-centric constraint set.

> **Current state (2026-05-18):** `index.json` is authoritative, beads is best-effort shadow. The split-brain analysis applies in both current and post-spike states, but with different severity. This document reasons primarily about the post-spike target state.

---

## H2 1. Two Lifecycle Models Side by Side

Both systems are work-queue state machines with a dependency-promotion engine. The vocabularies are near-isomorphic.

**Hermes Kanban status enum** [OFFICIAL — kanban data-model doc, fetched 2026-05-18; corroborates `hermes-kanban-discovery-2026-05-17` §3]: `triage | todo | ready | running | blocked | done | archived`. Promotion: `triage → todo` (via specify/decompose) → `ready` (when *all* parents `done`) → `running` (atomic claim) → `done | blocked | archived` (terminal). The dispatcher loop (default 60 s tick) reclaims stale claims, detects crashed PIDs, promotes ready tasks, atomically claims, spawns the assigned profile.

**Momentum story FSM** [PRAC — `.momentum/stories/index.json` distinct statuses + `sprint-manager/workflow.md:84-90`, inspected 2026-05-18]: ordered states `backlog → ready-for-dev → in-progress → review → verify → done`; terminal `done | dropped | closed-incomplete`. Transitions are **enforced** by the sole-writer sprint-manager: only adjacent-forward transitions are legal, backward/non-adjacent illegal without `force: true`. Dependency ordering is computed by sprint-dev from per-story `depends_on[]` plus the sprint's `waves[]` array (`sprint-2026-05-16` has `waves: [{wave:1,stories:[...]},{wave:2,...}]`, inspected 2026-05-18).

**Momentum beads layer** [PRAC — `beads-vs-momentum-tracker-evaluation-2026-05-16` §2; `.beads/issues.jsonl` inspected 2026-05-18]: beads adds the *real* dependency graph — 10 typed edge kinds (`blocks`, `parent-child`, `discovered-from`, `relates-to`, `supersedes`, `validates`, …), transitive-blocker-aware `bd ready`, atomic `bd ready --claim`, cycle detection. Beads status categories `active/wip/done/frozen` are mapped *from* Momentum's FSM by sprint-manager (`workflow.md:31-40`), confirming beads is downstream of the enforced FSM, not the FSM itself.

### Mapping Table — Concept ↔ Concept

| Hermes Kanban | Momentum equivalent | Fit |
|---|---|---|
| Board (`kanban.db`, per-project) | A Momentum project / `.momentum/` + `.beads/` root | **Clean** — 1 board ≈ 1 repo |
| Task (row: title, body, assignee, status) | Story (`stories/index.json` entry + `stories/{slug}.md` spec) + its bead | **Clean (work item)** — but Momentum splits work item (bead/index entry) from contract (spec `.md` in git tree); Hermes has no in-tree spec concept |
| Status enum (7 states) | Story FSM (6 ordered + 3 terminal) → beads `active/wip/done/frozen` | **Semantic mismatch** — Hermes has no `review`/`verify` (Momentum's quality gates); Hermes `triage` ≈ Momentum `backlog`+intake-queue stub |
| `task_links` (parent→child, single kind) | beads typed edges (10 kinds) + sprint `waves[]` + story `depends_on[]` | **Impedance** — Hermes links are *untyped* parent→child; beads is a *typed DAG*. Lossy downcast (see §3) |
| `task_runs` (one row per attempt) | Re-spawn / quick-fix; AVFL findings; git history (no first-class run table) | **Hermes richer** — attempt history is first-class in Hermes, bespoke in Momentum |
| Comment (durable thread) | Story spec prose + AVFL findings + handoff docs (`.momentum/handoffs/`) | **Partial** — Hermes comment thread ≈ Momentum's distributed handoff/finding artifacts |
| `kanban_complete(summary, metadata)` | Story spec + commit history + AVFL pass record | **Partial** — structured per-run handoff vs spec-driven contract |
| Workspace (`scratch`/`dir:`/`worktree`) | Sprint-dev git worktree under `.worktrees/<id>/` | **Clean** — both use git worktrees for code |
| Dispatcher (60 s tick, in-gateway) | sprint-dev orchestrator + (proposed) Claude-native daemon | **Conflict** — see §4, two dispatchers cannot co-promote one graph |
| Tenant (soft namespace) | epic_slug / feature_slug (M:N value bundle) | **Weak** — Hermes tenant is a flat filter; Momentum epic/feature is a taxonomy with prose |
| Worker lane (assignee → process) | `momentum:dev*` spawned subagent per story | **Impedance** — Hermes lane = OS process w/ Hermes profile; Momentum worker = Claude Code subagent (not a Hermes profile) — see §5 |
| `task_events` append-only log | `intake-queue.jsonl` + git log + beads `events` table | **Partial overlap** — Hermes events are lifecycle telemetry; intake-queue is discovered-work, not lifecycle |
| Sprint / wave | *(no Hermes equivalent)* | **No mapping** — Hermes board is continuous; Momentum sprint is a frozen-scope batch — the deepest mismatch (see §3) |
| Epic (membership/grouping) | `epic_slug` 1:N + beads `epic` type + `parent-child` | **Partial** — Hermes has parent→child trees but no first-class epic concept; beads does |
| Feature (M:N value bundle) | `feature_slug` + `features.json` | **No mapping** — Hermes has no orthogonal M:N grouping |

The table's shape is the finding: every **execution-mechanics** concept maps cleanly (board, task, workspace, run, comment). Every **planning-governance** concept (sprint, wave, epic, feature, the enforced FSM, the in-tree spec contract) has *no clean Hermes counterpart* — because Hermes Kanban is deliberately a thin coordination primitive whose explicit non-goals are "auto-assignment, budgets, governance gates, org-chart views remain user-space" [OFFICIAL — `hermes-kanban-discovery-2026-05-17` §12]. Momentum's value *is* those governance gates.

---

## H2 2. Where It Fits Cleanly

Three areas are genuine isomorphisms worth stating, because they are what makes a *projection* (not a sync) attractive:

1. **Worktree execution model.** Hermes `workspace: worktree` (git worktree under `.worktrees/<id>/`) is the same primitive sprint-dev already uses [OFFICIAL kanban doc; `hermes-kanban-discovery-2026-05-17` §3]. A code task's physical execution surface is identical in both.

2. **Attempt history.** Hermes `task_runs` (one row per attempt, prior-attempt outcomes injected into the retrying worker's context) is *strictly richer* than Momentum's current re-spawn/quick-fix model, which `beads-vs-momentum-tracker-evaluation-2026-05-16` §2 explicitly scores as "less structured attempt history." This is a concept Momentum could borrow regardless of any Hermes integration (already flagged in `hermes-kanban-discovery-2026-05-17` §13 idea 1).

3. **Structured handoff.** Hermes `kanban_complete(summary, metadata={changed_files, verification, residual_risk})` is a machine-readable downstream contract. Momentum's equivalent is spec-driven + AVFL findings — different mechanism, same intent. The *shape* is compatible enough that a projection can populate a Hermes card's handoff fields from a bead's metadata + the story's AVFL record without semantic loss in that direction.

These clean fits matter for exactly one thing: they make a **read-only beads→Hermes-board view** low-friction to build. They do **not** argue for letting Hermes own anything.

---

## H2 3. The Impedance Mismatches

Four mismatches are structural, not cosmetic. Each one independently breaks a naive bidirectional mapping.

### 3.1 Typed DAG vs. untyped parent→child links

Beads' core value is a **typed dependency graph**: `blocks` (hard, transitive, gates `bd ready`), `discovered-from` (provenance, non-blocking), `relates-to` (soft), `parent-child` (epic tree), `supersedes`, `validates` [PRAC — `beads-vs-momentum-tracker-evaluation-2026-05-16` §2; `.beads/issues.jsonl` shows a live `discovered-from` edge, inspected 2026-05-18]. Hermes `task_links` is a **single untyped parent→child relation** whose only semantic is "dispatcher promotes child `todo→ready` when all parents `done`" [OFFICIAL kanban doc, 2026-05-18]. Projecting beads → Hermes collapses 10 edge types into 1, discarding `discovered-from` provenance and `relates-to`/`supersedes`/`validates` semantics — a **lossy downcast**. Projecting Hermes → beads is *worse*: you'd have to *infer* edge type from nothing, producing semantically wrong `blocks` edges that would corrupt `bd ready`. This alone makes beads→Hermes a defensible one-way view and Hermes→beads unsafe.

### 3.2 Frozen-scope sprint vs. continuous board

This is the deepest mismatch. A Momentum **sprint is a frozen-scope batch**: sprint-planning selects a story set, locks it (`sprints/index.json` `active.locked: true`, per-story approval SHAs gating the contract — observed in `planning.approvals[]`, inspected 2026-05-18), and sprint-dev drains *that frozen set* in dependency-ordered `waves[]`. Hermes Kanban is the **opposite by design**: a continuous board where `kanban_create` can add work at any time and the dispatcher promotes the ready frontier *continuously* with no batch boundary, no freeze, no approval gate [OFFICIAL — `hermes-kanban-discovery-2026-05-17` §1, §6 Story 2 "create all, walk away"]. There is **no Hermes concept that maps to a sprint or a wave.** A Hermes board faithfully representing Momentum state would either (a) show the frozen sprint set as just-more-cards, erasing the freeze invariant that the approval-SHA gate enforces, or (b) require a synthetic "sprint" tenant/label that Hermes's dispatcher would ignore for promotion — meaning Hermes's continuous promotion engine would try to promote `ready` stories *outside the current sprint's frozen scope*. The sprint freeze is a Momentum enforcement primitive; Hermes has no hook to honor it.

### 3.3 Enforced FSM vs. advisory lifecycle

Momentum's FSM is **enforced**: sprint-manager is the sole writer of `index.json`, rejects non-adjacent/backward transitions without `force`, and is the moat per `beads-vs-momentum-tracker-evaluation-2026-05-16` §2 ("enforced domain lifecycle is the point"; beads itself is scored "no enforced FSM"). Hermes Kanban's lifecycle is **advisory and openly writable** — "every handoff is a row anyone (agent or human) can read and write" [OFFICIAL kanban doc, 2026-05-18]; the dashboard drag-drop does a *direct status write* through `kanban_db`. If Hermes can write status, Momentum's FSM enforcement is bypassed exactly the way `beads-vs-momentum-tracker-evaluation-2026-05-16` §4 warns about beads ("beads will not stop an agent making an invalid transition … must be kept and layered on top"). Hermes is *more* permissive than beads here (it has a GUI drag-drop write path), so it's a *larger* enforcement hole, not a smaller one.

### 3.4 In-tree spec contract vs. SQLite body

Momentum deliberately keeps story spec prose as `.momentum/stories/{slug}.md` **in the git working tree** so it appears in PR review and `git diff`; beads tracks only the work item and links via `--spec-id` (DEC-028 mitigation; `beads-dual-write-spike-findings-2026-05-16` Gate 4). Hermes stores the task `body` *in `kanban.db` SQLite* with no in-tree-spec concept. A Hermes-authoritative model would pull the contract out of the reviewable git tree — the *exact* regression `beads-vs-momentum-tracker-evaluation-2026-05-16` §4 ("Lose") spent a paragraph guarding against. A read-only projection avoids this (the spec stays in git; Hermes shows a pointer/summary); a bidirectional sync re-introduces it.

---

## H2 4. Source-of-Truth: The Three-Way Split-Brain

This is the decisive section. Momentum has **already designated its system of record**.

- Today (DEC-028 dual-write spike): `index.json` is authoritative, beads is a best-effort mirror (sprint-manager writes index "first — authoritative", then `bd update`, logging beads failures without aborting — `sprint-manager/workflow.md:93-94`).
- Post-spike (if gates pass): beads becomes authoritative, `index.json` retires (`beads-vs-momentum-tracker-evaluation-2026-05-16` §6 decision rule). **(post-spike target state)**

Either way there is exactly **one** SoT, and a single sole-writer (sprint-manager) enforcing the FSM on top of it. Hermes Kanban is **also architected to be the SoT of task lifecycle** — its own docs are explicit: "Hermes Kanban owns lifecycle truth … worker lanes execute but never own that truth" [OFFICIAL — kanban-worker-lanes doc, fetched 2026-05-18]. Two systems each asserting "I own lifecycle truth" is the definition of split-brain. Concretely, the failure modes if both are authoritative:

1. **Dual dispatcher promotion race.** Hermes's 60 s dispatcher promotes `todo→ready` and *atomically claims + spawns* when parents are `done`. Momentum's sprint-dev (and the proposed Claude-native daemon, `claude-code-background-dispatcher-2026-05-17` §6) does its own `bd ready --claim`. Two independent claim engines over the same logical work graph → the same story claimed and executed twice, or claimed in Hermes but invisible to sprint-dev's wave ordering. `beads-vs-momentum-tracker-evaluation-2026-05-16` already flags "duplicate story assignments (atomic claim not working)" as a *no-go trigger* for a single claim engine; adding a second, independent one (Hermes's) makes the race structurally certain, not merely possible.

2. **FSM bypass.** A Hermes dashboard drag-drop or `hermes kanban complete` writes `done` directly into `kanban.db`. If that syncs back, it skips Momentum's `review`/`verify` gates and the approval-SHA contract — invalid transition, no `force`, no AVFL. (§3.3.)

3. **Edge-type corruption.** Hermes→beads sync must invent edge types it doesn't have (§3.1), poisoning `bd ready`'s transitive blocker logic — the single most load-bearing query in the whole stack.

4. **Spec drift.** Hermes body edited in SQLite vs. `.momentum/stories/{slug}.md` in git → two contradictory contracts, the reviewable one not authoritative (§3.4).

5. **Sync-channel collision.** Hermes board lives in `~/.hermes/kanban.db` (single-host SQLite, no multi-host primitive [OFFICIAL §12]); beads lives in Dolt under `refs/dolt/data` with `bd dolt push`. A bidirectional bridge is a *third* sync channel on top of git + Dolt — and `beads-vs-momentum-tracker-evaluation-2026-05-16` §4 already documents the beads/git-discipline sync collision as a real friction. Adding Hermes makes it three-way.

**Who owns the SoT and what breaks if both do:** Momentum (via beads under the enforcing sprint-manager) owns it. If Hermes also owns it, the FSM enforcement moat (Momentum's entire stated value per `beads-vs-momentum-tracker-evaluation-2026-05-16` §6) is voided, `bd ready` is corrupted, and stories execute twice. There is no configuration that makes two authoritative dispatchers over one dependency graph safe.

---

## H2 5. The Worker-Lane Mismatch (Why "Hermes as delegate" is harder than it looks)

Even setting SoT aside, the *execution* bridge is not turnkey. A Hermes worker lane must supply [OFFICIAL — kanban-worker-lanes doc, fetched 2026-05-18; `hermes-kanban-discovery-2026-05-17` §5]: (1) an assignee string matching a **Hermes profile** (or a registered non-spawnable id), (2) a spawn mechanism — default is `hermes -p <assignee> chat -q <prompt>` — and (3) a lifecycle terminator (`kanban_complete`/`kanban_block`/crash). Momentum's workers are **Claude Code subagents running SKILL.md workflows** (`momentum:dev`, AVFL, sprint-dev) — *not* Hermes profiles. The docs are explicit that wiring a non-Hermes CLI (Claude Code/Codex/OpenCode) is **"not yet a paved path"** and requires per-integration design work: wrapping the Claude exit into `kanban_complete`/`kanban_block`, mapping workspace conventions onto `HERMES_KANBAN_WORKSPACE`, auth, per-CLI policy [OFFICIAL — kanban-worker-lanes doc, 2026-05-18; historical refs issue #19931, closed-not-merged Codex PR #19924 per `hermes-kanban-discovery-2026-05-17` §5.3]. So "Hermes dispatches Claude Code" is net-new, unsupported integration work, and the dispatched *work* is Momentum SKILL.md / AVFL / fan-out — which a non-Claude runtime can't execute anyway (`claude-code-background-dispatcher-2026-05-17` "Momentum-specific catch"). Hermes-as-delegate buys a dispatcher Momentum would have to hand-wire to Claude Code, to drive a board that duplicates beads.

Contrast: a **Claude-native dispatcher** reading `bd ready --claim` directly, woken by the beads `.beads/hooks/on_update` exec hook, needs *zero* new integration — it's the architecture `claude-code-background-dispatcher-2026-05-17` §6 + Beads addendum already recommends, runs on the existing local stack, fires Momentum skills natively, and keeps beads as the single SoT.

---

## H2 6. Safest Integration Topology

A one-way projection is dramatically safer than any sync, and the asymmetry is provable from §3:

- **beads → Hermes board (read-only view): safe-ish.** Generate a Hermes board (or any kanban GUI) as a *projection* of `bd query`/`bd list --json`: each bead → a card, beads status → a column, `blocks` edges → parent→child links (drop the other 9 edge types or render as annotations), AVFL/handoff metadata → the card's read-only handoff panel. Hermes's dispatcher is **disabled** (no `hermes gateway`/daemon against this DB; `kanban.db` is regenerated, never written by Hermes tooling). Loss is bounded and one-directional: you lose typed-edge fidelity *in the view only*; the authoritative graph in beads is untouched. This delivers Hermes Kanban's genuine wins (the dashboard, run-history drawer, the durable-comment UX) as an *observability surface* without ceding ownership.

- **Hermes → beads, or bidirectional: unsafe — reject.** Requires inventing edge types (§3.1 → corrupts `bd ready`), bypasses the enforced FSM (§3.3), pulls the spec contract out of git (§3.4), introduces a second claim/promotion engine (§4.1), and adds a third sync channel (§4.5). Every one of these is independently a no-go trigger by the criteria in `beads-vs-momentum-tracker-evaluation-2026-05-16` §6 / `beads-dual-write-spike-findings-2026-05-16` no-go list.

Recommended topology if a Hermes board view is desired at all:

```
Momentum sprint-planning / sprint-manager  →  enforces FSM, sole writer
        │  (writes)
        ▼
   beads (Dolt)  =  THE single system of record (DEC-028)
        │  bd query --json   (read-only, scheduled or on bd hook)
        ▼
   projector script  →  regenerates a Hermes/kanban GUI DB  (Hermes dispatcher OFF)
        ▼
   read-only board view  (humans watch; no write-back path exists)

   Execution stays Claude-native:
   .beads/hooks/on_update → local wake → Claude-native daemon → bd ready --claim
        → momentum:dev / AVFL / sprint-dev  (no Hermes lane, no Hermes profile)
```

**Verdict on fit:** Hermes Kanban is an excellent *conceptual analog* and a viable *read-only visualization* of Momentum's beads graph, but a poor *authoritative co-owner*. The structural fit is high at the execution-mechanics layer and absent at the planning-governance and ownership layers. For the stated constraints (local-only, cost-sensitive, Claude-skill-centric), **Hermes-as-delegate is the wrong topology**: it adds an unsupported CLI-lane integration, a single-host SQLite SoT that competes with beads, and a second dispatcher over one graph — to deliver a board a read-only projector can produce with none of that risk. A **Claude-native dispatcher over beads** (per `claude-code-background-dispatcher-2026-05-17`) is the dominant choice; Hermes Kanban's role, if any, is a downstream read-only mirror — never a writer, never the dispatcher, never a SoT.

---

## Sources

**Prior-art research docs (cited by name):**
- `/Users/steve/projects/momentum/docs/research/hermes-kanban-discovery-2026-05-17.md` — Hermes Kanban facts (data model §3, worker lanes §5, scope boundaries §12, Momentum-relevance §13).
- `/Users/steve/projects/momentum/docs/research/beads-vs-momentum-tracker-evaluation-2026-05-16.md` — Momentum beads model, typed edges, enforced FSM as moat, SoT decision (§2, §4, §6).
- `/Users/steve/projects/momentum/docs/research/beads-dual-write-spike-findings-2026-05-16.md` — DEC-028 dual-write status, no-go triggers, `--spec-id` Gate 4.
- `/Users/steve/projects/momentum/docs/research/claude-code-background-dispatcher-2026-05-17.md` — recommended Claude-native daemon architecture (§6), beads-as-event-source addendum, Momentum-specific catch, cost levers.

**Hermes official docs (fetched/verified 2026-05-18) [OFFICIAL]:**
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban — status enum, task_links promotion, task_runs, dispatcher, single-host constraint, event vocabulary.
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes — three-part lane contract, Hermes profile spawn, "Kanban owns lifecycle truth," external CLI lanes not a paved path.
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial — referenced via prior-art discovery (four tutorial stories, §6 of discovery doc).

**Momentum state inspected directly (2026-05-18) [PRAC]:**
- `.momentum/stories/index.json` — story statuses (`backlog/ready-for-dev/done/dropped/closed-incomplete`), `depends_on[]`, `epic_slug`.
- `.momentum/sprints/index.json` — `waves[]` structure, `active.locked`, per-story `approvals[]` SHA gate.
- `.momentum/intake-queue.jsonl` — discovered-work event log shape.
- `.beads/issues.jsonl` — live `discovered-from` edge, epic/task issue types.
- `skills/momentum/skills/sprint-manager/workflow.md` — enforced FSM transition rules (lines 84-90), Momentum→beads status mapping (31-40), index-first-authoritative dual-write (93-94).
