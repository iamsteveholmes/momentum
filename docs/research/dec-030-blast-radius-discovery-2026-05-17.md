# DEC-030 — Phase 0 Blast-Radius Discovery

**Date:** 2026-05-17
**Type:** Internal discovery (no spike story — per developer instruction, internal blast-radius discovery against our own artifacts does not require a spike story; findings committed so the work is durable)
**For:** `_bmad-output/planning-artifacts/decisions/dec-030-dag-dispatch-frozen-sprints-dual-format-2026-05-17.md`
**Method:** Four parallel discovery streams (fan-out, independent): (A) story blast radius, (B) decision/architecture reconciliation, (C) Gate 1 — dispatch host, (D) Gate 2 — how-vs-what adjudication.

> **Status of recommendations:** Streams A/B are discovered fact. Streams C/D produce **recommendations awaiting developer ratification** — they are not yet authoritative. DEC-030's Gates 1 and 2 remain formally open until ratified; this document supplies the resolved proposals.

---

## 1. Story Blast Radius (Stream A)

The execution-model change is systemic — no story touching sprint-dev, the epic/feature taxonomy, sprint-manager, dispatch, dependency management, or human-in-the-loop planning is unaffected.

### Existing stories affected (selected — the load-bearing set)

| Slug | Status | Why DEC-030 touches it |
|---|---|---|
| `momentum-sprint-dev` | ready-for-dev | D1: core loop is wave/barrier today; must become DAG-driven continuous dispatch |
| `sprint-manager-skill` | dropped | D2/D3: sole enforcer of the frozen-scope/subtract-only invariant + how-vs-what gate; epic/feature collapse |
| `epic-grooming` | done | D2: frozen-scope model obsoletes epic-as-accretion-container |
| `feature-grooming` | done | D2: epic+feature collapse makes parallel grooming redundant unless repositioned as value-discovery |
| `change-type-routing-in-sprint-dev` | backlog | D3: gates the how-vs-what boundary (Gate 2) |
| `feature-artifact-schema` | done | D2: features.json schema rework for the single closeable value-grouping |
| `feature-status-skill` / `feature-status-practice-path` | done | D4: Class-1 deterministic-projection dashboard surface |
| `intake-skill` / `consolidate-intake-invocation-and-fix-error` | done / backlog | D2: `discovered-from` birth model for work found mid-sprint |
| `sprint-scope-tracking` | backlog | D3: planned-vs-discovered accounting feeds the subtract-only invariant |
| `sprint-dev-fixture-parallel-spawning-for-independent-stories` | backlog | D1: parallelism becomes structural under DAG dispatch |
| `sprint-planning-fixture-gherkin-behavioral-generality` | backlog | D3: behavior/AC-level freeze depends on behavioral (not impl-coupled) specs |

(Stream A surfaced ~20 affected slugs total; the remainder are fixtures and phase-gate stories that follow from the above.)

### New stories implied

| Proposed title | Realizes | One-line scope |
|---|---|---|
| DAG dispatcher loop — continuous claim from beads ready-set | D1 | claim from `bd ready ∩ frozen-set`, spawn dev agents, unblock dependents, no wave barrier |
| sprint-manager frozen-scope enforcement — subtract-only + scope_guard | D3 | reject adds; adjudicate modify-vs-new-story at transition time |
| Epic+feature collapse to one closeable value-grouping | D2 | unify epic_slug/feature_slug → one M:N grouping w/ acceptance_condition + `discovered-from` |
| `discovered-from` lineage capture & navigation | D2 | born-separate discovered work; origin/closure navigation |
| Class-1 sprint/feature-status dashboard — deterministic projection | D4/D5 | zero-ambiguity human render; approval binds to render |
| Class-1 pre-sprint planning dashboard | D4/D5 | story-readiness, AC specs, AVFL-clean, team-composition before activation |
| Design-fidelity validator — DOM→skeleton + mismatch report | D6 | Class-2 decorrelated verification leg |
| DOM-skeleton extraction (breakpoint/state-sampled) | D6 | deterministic headless-browser snapshot, mechanical input to the validator |

---

## 2. Decision & Architecture Reconciliation (Stream B)

`architecture.md` uses inline **Decision N / AD-N** numbering. **No prior decision is fully superseded.**

**Amended:**
- **AD-25 (Teams Over Waves)** — tightened: runtime dependency ordering replaces wave assignment; wave fields become informational.
- **AD-36 (Sprint Lifecycle State Machine)** — asymmetric subtract-only freeze added as a hard invariant within the active state; pre-activation vetting becomes a hard gate.
- **AD-44 (Feature Artifact Layer)** — epic/feature taxonomy collapses from two orthogonal dimensions to one closeable grouping; `value_analysis`/`system_context`/`acceptance_conditions` fields survive.
- **AD-57 / DEC-028 (Beads spike)** — DEC-030 D1 is contingent on the beads verdict (DEC-030 Gate 3); `bd ready` is the dependency source if go, depends_on fallback if no-go.

**Composes-with:** DEC-005 (feature-first cycle — DEC-030 operates within it), DEC-006 (dual-audience legibility — D4 extends it with the integrity split + decorrelation), DEC-029 (its sequenced sprint-dev rewrite realizes DEC-030's planning-side model; D9/D10/D11 supply the pipeline & state-ledger abstraction).

**Unaffected:** DEC-004, DEC-012, DEC-017; AD-26, AD-29, AD-31, AD-34, AD-45, AD-51, AD-55.

---

## 3. Gate 1 — Dispatch Host (Stream C) — RECOMMENDATION

**Recommended: Option 1 — in-session orchestrator loop** (sprint-dev runs the poll-`bd ready`-and-spawn loop within one Claude Code session). Decisive reasons:

1. **Only Option 1 can both spawn agents and host the human gates.** Agent spawning is a session-bound `Agent` tool call — not a CLI entrypoint. This *disqualifies Option 3* (external process cannot spawn dev agents, run AVFL, or drive `<ask>` gates; it collapses back to "signal a session"). Option 2 (harness `/loop`/`ScheduleWakeup`) breaks DEC-030 D3/D5's blocking in-sprint human gates (AVFL stop-gate, fix-queue, Gherkin verification) — a re-entrant tick has no stable thread for multi-turn `<ask>`, and the pause/resume-with-human primitive doesn't exist.
2. **The loop already exists.** sprint-dev's Phase 2↔3 re-entry cycle, `spawn_registry` dedup, failure ask-gate, deferred worktree cleanup are present. D1 = delete the wave barrier + swap wave-gated graph re-eval for `bd ready --json --claim` on each completion. An edit, not a new substrate.
3. **The drift objection is neutralized in-tree.** Authoritative loop state is external and deterministic: `bd ready` recomputed every tick, status in `stories/index.json`, progress in mandated TaskCreate/TaskList, dedup anchored by atomic claim. Conversation carries flow, not truth — exactly why DEC-028/D1 wants the DAG in beads, not in the agent.
4. **Failure isolation is automatic.** A failed story's bead never becomes ready, so dependents stay unready in beads while the orchestrator keeps dispatching the rest of `bd ready`. That *is* D3's "blocked story drops, sprint continues" — beads enforces it; the orchestrator just keeps ticking.
5. **Stays inside Momentum's enforcement moat** — no out-of-moat harness feature as the central control surface, no parallel control plane outside sprint-manager.

**Accepted cost:** orchestrator-crash recovery is manual re-invoke — but degrades cleanly (idempotent atomic claim + existing session-resumption + external story/worktree state ⇒ no double-dispatch, no silent corruption).

**Residual risks to carry into Phase 1:**
- Long-sprint context budget unbounded → specify a per-iteration "re-sync from beads, discard narrative" step so compaction is non-destructive by design.
- Crash-restart idempotency asserted not proven (bead claimed but agent died pre-merge) → make the crash-restart path an explicit Gate 4 test case.
- `bd update` (bead close) ↔ story-status transition atomicity → define the authoritative system on conflict + reconcile step; specify the ledger abstraction so there is no hard beads dependency pre-spike (DEC-029 D11 / Gate 3).
- Concurrency degree unspecified → state a max-in-flight dev-agent cap (orchestrator-side throttle) to avoid unbounded fan-out.

---

## 4. Gate 2 — How-vs-What Adjudication (Stream D) — RECOMMENDATION

**Recommended policy: a deterministic `scope_guard` action at sprint-manager**, anchored on DEC-029 D2's hook-immutable frozen contract.

**Principle:** *A change is a "what" (new story) iff it changes the set of observable behaviors a black-box verifier checks against the frozen contract. It is a "how" (allowed perturbation) iff the frozen contract still verifies the edited story byte-identically.* The kernel is a hash/diff comparison, not a judgment call.

**Frozen-scope manifest** (sprint-manager-owned, captured at `sprint_activate` into `sprints/index.json`): per story `{ ac_hash, contract_hash, change_type, touches_root }`. Activation refuses if any member story lacks a frozen contract or is not validation-clean (DEC-030 D5 hard precondition).

**Decision rule (first match wins):**

| Edit class | Frozen contract still verifies as-is? | Verdict |
|---|---|---|
| Tasks / Dev-Notes / approach / internal structure only | Yes (byte-identical) | MODIFY — accept |
| AC wording tightened, same observable behavior | Yes | MODIFY — accept (may WARN per behavioral-generality guard) |
| AC behavior added/removed/altered | No — contract must be re-authored | NEW STORY — reject |
| `touches` expanded beyond frozen scope (directory granularity) | No | NEW STORY — reject |
| `change_type` changed | No — re-routes verification method | NEW STORY — reject |
| Story dropped | N/A — subtract always allowed | DROP — accept |

**Enforcement:** gate fires at two transitions — (1) `sprint_plan add` to an active sprint is unconditionally rejected ("add forbidden" arm, no adjudication); (2) any `status_transition` advancing/re-opening a member story runs `scope_guard` first, comparing recomputed AC hash / change_type / touches against the manifest. sprint-manager rejects the **transition**, never edits the story file (preserves its no-story-content-writes rule). Fail-closed: AC-hash change defaults to "scope-addition."

**Escalation (human, never agent):** sprint-manager is mechanical and never adjudicates ambiguity — it returns `success:false` + three remedies. The orchestrator escalates the AC diff (human-optimized projection, not raw hashes — DEC-030 D4/D5) to the developer, who chooses: (a) revert to behavior-equivalent wording → re-passes deterministically; (b) drop + `create-story` successor linked `discovered-from` → DAG re-entry; (c) explicit, logged, developer-attributed override (counted as a frozen-scope breach for retro / Gate 4).

**Net residual:** deterministic on 3 of 4 arms + the dominant AC arm; the one soft spot (synonymic AC rewrites / AC under-specification) is bounded by fail-closed defaults, developer escalation, and a retro planning-quality signal. No path admits a silent scope change into a certified sprint.

---

## 5. What Remains for Developer Ratification

1. **Gate 1:** ratify Option 1 (in-session orchestrator loop) — or direct otherwise.
2. **Gate 2:** ratify the `scope_guard` / frozen-manifest policy — or amend.
3. Gate 3 (DEC-028 beads verdict) and Gate 4 (real-sprint subtract-only validation) remain genuinely open by design — not resolvable in discovery.

On ratification, the new-story list (§1) is ready for `create-story`/sprint-planning; DEC-030's `architecture_decisions_affected` is updated (§2) and its Required-Discovery section closed.
