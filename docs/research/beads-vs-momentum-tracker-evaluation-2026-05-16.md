---
title: "Beads vs. Momentum — Tracker & Persistent-Memory Engine Evaluation"
date: 2026-05-16
type: research-evaluation
status: draft-for-decision
sources:
  - https://gastownhall.github.io/beads/ (v1.0.4)
  - .momentum/ state model + skills/momentum/ (sprint-manager, sprint-dev, intake, create-story, epic/feature-grooming, retro)
---

# Beads vs. Momentum — Tracker & Persistent-Memory Engine Evaluation

## BLUF

Beads (`bd`) is a **superior substrate** for the layers Momentum currently hand-builds: the
work-item store, the typed dependency graph, the dependency-aware ready queue, multi-agent
claim/lease primitives, and compaction-resilient memory. It is **not** a replacement for
Momentum — it has no quality practice (AVFL, reviewers, retro audit, distill) and, critically,
no enforcement model. Beads is advisory; Momentum's moat is *enforced* workflow fidelity.

**Recommendation: adopt beads underneath Momentum as the state/dependency/memory engine; keep
Momentum's enforced orchestration and quality practice on top; keep story spec prose in the git
tree. Do it as a one-sprint dual-write spike, not a big-bang migration.** The epic/feature
consolidation the user anticipated is real but less lossy than feared — features survive as
relate-linked epic-beads, not as a deleted concept.

This is a "build-on" decision, not a "build-vs-buy" one.

---

## 1. Correct the mental model: beads is now Dolt-powered

Older beads was git-tracked JSONL + a SQLite cache. **v1.0.4 is Dolt-powered** — a
version-controlled, MySQL-compatible database. This materially changes the evaluation:

- Issue data lives in a Dolt DB under `.beads/` (embedded by default; `dolt sql-server` for
  multi-writer). It is **gitignored**.
- Sync is **not** git-of-the-data. Dolt rides the *same git remote* but under a separate ref
  namespace `refs/dolt/data`, via `bd dolt push` / `bd dolt pull`. Your code and your issue
  history share a remote but live in different ref trees.
- This buys per-issue history, `bd show --as-of <commit>` time travel, merge-driver-assisted
  concurrent edits, and graceful compaction — but it moves tracker state **out of your git
  working tree** and adds a real binary/DB infrastructure dependency to a project whose
  CLAUDE.md currently says "markdown and bash, no compiled code."

That trade — richer data engine vs. state leaving the reviewable git tree — is the spine of
this whole evaluation.

---

## 2. Side-by-side

| Axis | Momentum today | Beads v1.0.4 | Edge |
|---|---|---|---|
| **Work-item store** | `stories/index.json` (one ~146 KB file, 311 stories, single sole-writer skill) + per-story `.md` in git tree | Dolt DB; hash IDs; rich fields (`description/design/acceptance/notes/context/spec_id/external_ref/metadata/estimate/due/defer`); `bd query` + `bd sql` | **Beads** for scale, query, concurrency; **Momentum** for in-tree reviewable spec |
| **State machine** | Domain FSM `backlog→ready-for-dev→in-progress→review→verify→done`, terminal `done/dropped/closed-incomplete`, **enforced** by sprint-manager with `--force` override | `status` driven by categories `active/wip/done/frozen`; custom statuses; **no enforced FSM** | **Momentum** — enforced domain lifecycle is the point |
| **Dependencies** | per-story `depends_on[]` + sprint `waves[]`; graph rebuilt ad hoc in sprint-dev Phases 1–3 | 10 typed kinds (`blocks/parent-child/discovered-from/relates-to/supersedes/validates/...`); transitive blocker-aware `bd ready`; atomic `--claim`; cycle detection; `--explain` | **Beads** — decisively |
| **Epic / Feature** | `epic_slug` (1:N, `epics.md`) **and** `feature_slug` (M:N orthogonal, `features.json`) — two taxonomies | `epic` type + `parent-child` tree (dotted IDs) + labels + metadata + `relates-to` + `bd query` | **Beads** for epics; features must be remodeled (see §3) |
| **Persistent memory** | `handoffs/`, `intake-queue.jsonl`, decision docs, `memory/` dir, Impetus orientation | `bd remember/recall/forget`, `bd kv`, `bd prime` SessionStart re-injection, Dolt history, `discovered-from` | **Beads** — purpose-built for compaction amnesia |
| **Multi-agent concurrency** | fan-out spawns, orchestrator-controlled, **no claim/lease**, sole-writer index is a serialization point | hash IDs (collision-free concurrent create), atomic `--claim`, `pin/hook` lease, file `reserve`, `lock`, `merge-slot`, `swarm` | **Beads** — decisively |
| **Orchestration + quality** | sprint-planning/sprint-dev/AVFL/code-reviewer/qa/e2e/architecture-guard/retro DuckDB audit/distill/upstream-fix | formulas/molecules/gates/wisps DAG engine; **no quality practice at all** | Different layers — not either/or |
| **Audit / history** | `git log` over JSON (coarse whole-index diffs) + retro transcript audit | per-issue Dolt history, `--as-of` time travel, `bd audit` → `interactions.jsonl` (SFT/RL) | **Beads** for issue history; Momentum's transcript audit is orthogonal, stays |
| **Storage / infra** | markdown + bash, JSON in git tree, normal git remote, zero infra | Dolt binary + versioned SQL DB + `refs/dolt/data` + optional Dolt server | **Momentum** — far simpler |
| **Enforcement model** | Skills are sole writers; transitions validated; approval-SHA gates; workflow-fidelity rules | Advisory: `bd prime` injects protocol, agent *voluntarily* calls CLI; no CLAUDE.md gate, no FSM enforcement | **Momentum** — this is the moat |

---

## 3. The epic/feature consolidation question (answered specifically)

The user's premise — "we'd have to consolidate epic/feature into 'epics' the beads way" — is
**correct for epics and softer than feared for features.**

- **Epics → strictly better in beads.** `epic_slug` is a string field that epic-grooming
  polices for orphans. Beads gives a real graph: `epic` type, `--parent` children with dotted
  IDs (`bd-a3f8.1`), `bd epic status`, `bd epic close-eligible`, label inheritance. This is an
  upgrade, not a compromise.
- **Features do not have to be deleted.** Momentum's feature is an M:N value bundle with its
  own `value_analysis`, `system_context`, `acceptance_condition` — that does not fit
  `parent-child` (a story has one parent). Two viable models in beads:
  1. `feature:<slug>` **label** on member stories → fast `bd list --label feature:x` /
     `bd query` views. Cheap; loses feature-level prose.
  2. Feature as its own **epic-type bead** with `relates-to` edges to member stories →
     preserves `value_analysis`/`system_context` in the bead body, keeps M:N, stays
     queryable, non-blocking. Recommended — it keeps `features.json` semantics inside beads.
- **What genuinely doesn't survive:** feature-grooming's 6-signal holistic scan
  (MERGE/SPLIT/DEDUP/NEW/RETIRE/UPDATE) and feature-status/canvas rendering must be **rebuilt
  against `bd query`/`bd sql`** instead of parsing `features.json`. Features also stop being a
  separately *enforced* taxonomy and become a view — defensible simplification, but a real
  semantic change to acknowledge.

Net: consolidation is feasible and partly an upgrade. Budget the rebuild of feature-grooming,
feature-status, and the canvas data layer.

---

## 4. What you gain, lose, and keep regardless

**Gain**
- `bd ready` + atomic `--claim` replaces the bespoke dependency graph in sprint-dev Phases
  1–3. This is the single biggest win — a battle-tested, richer version of logic Momentum
  reimplements and must keep correct by hand.
- `discovered-from` collapses the intake-queue triage hop: discovered work is created *in the
  graph*, linked to its origin, and resurfaces via `bd ready` — instead of an append-only
  JSONL someone must later triage into stories.
- `bd remember`/`bd prime` is a designed answer to compaction amnesia; Momentum's handoffs/
  + memory/ + Impetus orientation is more bespoke and not auto-injected at compaction.
- Real concurrency safety (hash IDs, claim/lease, file reservations, merge-slot) for fan-out
  subagents — Momentum currently has none; the sole-writer index is a serialization point.
- `bd query`/`bd sql` + per-issue history make canvas/feature-status/retro analytics far
  cheaper than parsing a 146 KB JSON and diffing whole-index git history.

**Lose**
- Story spec prose moving into a gitignored Dolt DB removes it from PR review, the git diff,
  and the working tree. **Mitigation: keep `.momentum/stories/*.md` as the spec of record,
  link via `bd` `--spec-id`/`--external-ref`. Do not move spec prose into Dolt.** Beads tracks
  the *work item*; the markdown stays the *contract*.
- Zero-infra simplicity. Dolt is a binary + versioned SQL DB, with operational sharp edges the
  docs themselves flag (phantom DBs, orphan `sql-server` processes / `bd dolt killall`, CGO
  requirement for federation).
- A second sync channel (`bd dolt push`) that **collides with the global git-discipline
  rules** (push-needs-approval, conventional commits). `bd prime` injects "ALWAYS
  `bd dolt push` at session end" — exactly the autonomy Momentum's rules withhold.
  `no-git-ops`/`--stealth` mode mitigates but is more custom config to own.
- The enforcement gap: beads will not stop an agent making an invalid transition or skipping a
  gate. Momentum's state-machine validation and approval-SHA gate must be **kept and layered
  on top** — sprint-manager becomes a thin enforcing wrapper over `bd`, not retired.

**Keep regardless (beads touches none of this)**
- The entire quality practice: AVFL, code-reviewer, qa-reviewer, e2e-validator,
  architecture-guard, upstream-fix.
- Retro's DuckDB transcript audit, the distill flywheel, decision documents.
- Gherkin specs, change-type classification, EDD/TDD injection, the approval-SHA gate.
- Workflow-fidelity enforcement via skills/rules. Beads is the substrate; Momentum remains the
  practice.

---

## 5. Maturity & risk

- Single-vendor, v1.0.x, GitHub-Pages docs. The gate system's **phased rollout** (human=P1,
  timer=P2, GitHub=P3, cross-rig bead=P4) signals the advanced coordination surface is newer
  and less battle-tested than the issue/dep core.
- A copy-paste **JSON error in the documented Claude Code hook snippet** (duplicate
  `"SessionStart"` key) — minor, but a docs-quality signal.
- The integration is **advisory by design** — "protocol by injection," no CLAUDE.md gate, no
  guarantee the agent uses `bd`. This is philosophically opposite to Momentum's enforced
  fidelity; adopting beads does not import enforcement, it presumes Momentum supplies it.
- Dolt is a real dependency with a real ops surface. Treat the Dolt remote's backup/restore as
  a first-class concern, not an afterthought (your tracker history now lives there).

---

## 6. Recommendation — phased, not big-bang

**Verdict: Beads is the right engine for the tracker/dependency/memory layers; Momentum stays
the orchestration/quality/enforcement layer. Adopt, layered, via a spike.**

**Spike (one upcoming sprint, dual-write):**
1. Rewrite `sprint-manager` to dual-write: keep `index.json` authoritative, mirror every
   story/sprint/transition into beads (`bd create/update/dep add`, epics as `--parent`,
   features as relate-linked epic-beads).
2. Drive sprint-dev's dependency selection off `bd ready --json` instead of the hand-built
   wave/`depends_on` graph. Keep waves as a fallback.
3. Route discovered work through `bd create --deps discovered-from:<origin>` instead of the
   intake-queue append, for that sprint only.
4. Wire `bd prime` via SessionStart hook with a `.beads/PRIME.md` override carrying Momentum's
   protocol; set `no-git-ops`/`--stealth` so beads never injects `bd dolt push` against the
   git-discipline rules — Momentum owns sync.
5. Keep `.momentum/stories/*.md` in the git tree; link via `--spec-id`.

**Decision criteria after the spike:**
- Did `bd ready` + `--claim` measurably simplify sprint-dev Phases 1–3 and remove
  hand-maintained graph logic?
- Did `discovered-from` eliminate intake-queue triage toil without losing items?
- Was Dolt sync manageable alongside the git-discipline rules, or a constant friction?
- Did losing in-tree story metadata (now in Dolt) hurt review/audit, or did `--spec-id`
  linkage hold?

If 3 of 4 are positive → flip beads to authoritative, retire `index.json`, rebuild
feature-grooming/feature-status/canvas over `bd query`. If not → keep the JSON model; the
spike still yields a better dependency engine for sprint-dev regardless.

**Do not** adopt the molecules/formulas/gates DAG engine in the same move. It overlaps
sprint-planning/sprint-dev and is the least mature surface. Evaluate it separately, later, only
if the substrate adoption succeeds.

---

## 7. One-line answer to the question asked

> Is beads a *superior tracker and persistent-memory engine* than what Momentum has?

For the **tracker and memory engine layers specifically — yes, clearly.** For Momentum as a
whole — no, because Momentum's value is enforced practice and quality, which beads does not
provide and does not claim to. The right outcome is beads *under* Momentum, proven by a
one-sprint dual-write spike, with story specs kept in the git tree and the epic/feature model
consolidated as described in §3.
