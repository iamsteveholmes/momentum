---
content_origin: research-agent
date: 2026-05-22
sub_question: "Gas City convergence loops, human review loop patterns, barrier/join primitives, pipeline observability"
---

# Gas City Convergence Patterns — Discovery Report

## Research Question

Does Gas City have built-in convergence loop constructs suitable for modeling automated fix loops and iterative human review? What barrier/join primitives exist for fan-out synchronization? How observable is a multi-order pipeline?

## Sources Consulted

- `https://github.com/gastownhall/gascity` — top-level repository structure [OFFICIAL]
- `https://github.com/gastownhall/gascity/tree/main/internal/convergence` — full package file listing [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/handler.go` — 9-step loop algorithm [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/gate.go` — gate result structures [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/manual.go` — approve handler [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/hybrid.go` — hybrid gate logic [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/retry.go` — retry handler [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/create.go` — creation parameters [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/metadata.go` — bead metadata schema [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/events.go` — event types and payloads [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/evaluate.go` — evaluation step [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/artifact.go` — artifact directory management [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/template.go` — template context variables [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/capture.go` — subprocess output capture [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/formula.go` — formula validation [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/orders.md` — order types and triggers [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/dispatch.md` — dispatch/fan-out [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/nine-concepts.md` — core concepts [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/formulas.md` — formula architecture [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/event-bus.md` — event types and filters [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/life-of-a-molecule.md` — molecule lifecycle [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/glossary.md` — term definitions [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/engdocs/architecture/event-query.md` — event query layer [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/orders/order.go` — Order struct [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/orders/triggers.go` — trigger evaluation [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/orders/runtime_helpers.go` — order helpers [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/cmd/gc/cmd_converge.go` — gc converge CLI [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/cmd/gc/cmd_citystatus.go` — gc citystatus CLI [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/cmd/gc/cmd_dashboard.go` — gc dashboard CLI [OFFICIAL]
- `https://github.com/gastownhall/gascity/tree/main/internal/beads` — beads package structure [OFFICIAL]
- `https://docs.gascityhall.com/` — docs site navigation [OFFICIAL]
- `https://docs.gascityhall.com/reference/cli` — full CLI reference [OFFICIAL]
- `https://github.com/gastownhall/gascity-packs/tree/main/pr-pipeline` — pr-pipeline pack [OFFICIAL]
- `https://github.com/gastownhall/gascity-packs/tree/main/pr-review` — pr-review pack [OFFICIAL]
- `https://github.com/gastownhall/gascity-packs/tree/main/flywheel` — flywheel pack [OFFICIAL]
- `https://github.com/gastownhall/gascity/blob/main/internal/convergence/stop_test.go` — stop behavior [OFFICIAL]
- `https://github.com/gastownhall/gascity/tree/main/examples/lifecycle` — lifecycle example [OFFICIAL]

---

## Findings

### 1. Convergence Loop Constructs

**Gas City has a native, first-class convergence loop primitive.** CONFIRMED.

The `internal/convergence/` package is a dedicated subsystem — not a pattern built from orders. The package contains 20+ source files covering creation, evaluation, gating, retry, artifact management, event emission, and termination. The loop is instantiated via `gc converge create` and operates as follows:

**Core loop algorithm (from `handler.go`, 9 steps):**

1. Guard: confirm root bead is not already terminated.
2. Dedup: monotonic iteration tracking prevents replay.
3. Derive iteration: count closed child wisps with convergence keys.
4. Speculative pour: create the next wisp *before* gate evaluation (crash-safe).
5. Gate evaluation: run condition/hybrid/manual logic.
6. Persist outcome: store gate result for replay fidelity.
7. Determine continuation vs. terminal.
8. Emit `convergence.iteration` event.
9. Commit with dedup marker.

**Loop continues automatically** unless the gate outcome triggers a terminal state. There is no separate "re-trigger" step required — the handler fires on each `wisp_closed` event.

**Terminal states (from `handler.go` and `stop_test.go`):**

| State | Trigger |
|---|---|
| `approved` | Gate passed (`ActionApproved`) |
| `no_convergence` | Max iterations reached or timeout with `terminate` action |
| `waiting_manual` | Manual gate mode: loop suspends, awaits `gc converge approve` or `gc converge iterate` |
| `stopped` | Operator calls `gc converge stop` |

**This is NOT implemented as chained condition-triggered orders.** It is a native bounded-iteration construct. CONFIRMED.

**Iteration count is template-accessible.** The `TemplateContext` struct injects: `BeadID`, `WispID`, `Iteration` (1-based), `ArtifactDir`, `Formula`, `RetrySource`, and `Var.*` (custom variables). An agent prompt in iteration N knows it is iteration N and has access to per-iteration artifact directories. CONFIRMED.

**Gate modes (from `gate.go`, `manual.go`, `hybrid.go`):**

- **`manual`**: Loop suspends to `waiting_manual` after each iteration. Human explicitly calls `gc converge approve` or `gc converge iterate`.
- **`condition`**: Shell script evaluated. Exit 0 = pass. Non-zero = fail, loop continues.
- **`hybrid`**: Condition script evaluated with agent verdict injected as `$GC_AGENT_VERDICT`. Falls back to manual if no condition is configured.

**Timeout action variants (from `gate.go`):**

- `iterate` (default): treat timeout as continue
- `retry`: up to 3 retries
- `manual`: fall back to human
- `terminate`: end loop as `no_convergence`

**Formula-level configuration:** A formula must set `convergence = true`. It must not use reserved step names. The evaluate step uses a prompt that must call `bd meta set convergence.agent_verdict <value>` — the agent writes its own verdict into bead metadata, which the gate then reads. CONFIRMED.

**Retry a terminated loop:** `gc converge retry` recreates a new convergence bead from a terminated one (copies formula, vars, gate config). A loop terminated as `approved` cannot be retried — only failed or stopped loops can. CONFIRMED.

---

### 2. Human Review Loop — Gate Mechanics and Feedback

**The `waiting_manual` state IS the human gate.** CONFIRMED.

When a convergence loop reaches `waiting_manual`, it suspends. Two operator commands are available:

- `gc converge approve <beadID>` — terminates the loop with `terminal_reason=approved`. Emits `convergence.terminated` (TierCritical) then `convergence.manual_approve` (TierBestEffort). Actor is recorded as `"operator:<username>"`.
- `gc converge iterate <beadID>` — forces the next iteration cycle. Emits `convergence.manual_iterate` (TierRecoverable). The loop resumes and runs the formula again.

**There is no `bd gate reject` or `bd gate feedback` command.** CONFIRMED ABSENT.

The `ApproveHandler` signature accepts only `(ctx, beadID, username, "")` — the empty string parameter has no payload function. No feedback text field exists in the approval flow. No `reject` subcommand exists under `gc converge`. CONFIRMED.

**The intended rejection workaround:** Use `gc converge iterate` instead of approve when the human wants fixes. The loop runs another iteration. However, the human has no in-system channel to communicate *what* to fix. CONFIRMED as gap.

**Can feedback be conveyed as payload?** Indirectly, via the artifact directory and bead metadata. The `ArtifactDir` is per-iteration and accessible to formula prompts. A human operator could write a `feedback.txt` into the artifact dir for iteration N before calling `gc converge iterate`, and the formula prompt for iteration N+1 could read it. However, this is NOT a documented pattern — no official mechanism exists for human-written feedback injection. INFERRED as possible workaround; [UNVERIFIED] as supported practice.

**The `convergence.waiting_manual` event** (TierRecoverable) fires whenever the loop enters waiting_manual state. Its payload includes: rig, iteration, wisp ID, agent verdict, gate result, waiting reason, and duration. A downstream system could subscribe to this event to notify humans. CONFIRMED as mechanism; [UNVERIFIED] whether the Momentum orchestrator currently does this.

**Can a gate carry human feedback as payload to the next stage?** Not natively. The metadata field `convergence.agent_verdict` is agent-written, not human-written. The `Var.*` template variables are set at creation time and cannot be updated mid-loop via any documented CLI. CONFIRMED as gap.

---

### 3. Pipeline Synchronization — Barrier / Join Primitives

**There is no native barrier or join primitive in Gas City.** CONFIRMED ABSENT.

A search across `internal/beads/`, `internal/orders/`, `internal/session/`, `internal/convergence/`, and the architecture docs found zero barrier/join constructs. The CLI reference (`gc barrier`, `gc join`) does not exist. The dispatch architecture describes serial fan-out only: "Container expansion is serial. When expanding a convoy, each child is slung sequentially." CONFIRMED.

**Fan-out exists; fan-in does not.** CONFIRMED.

The order system can fire N orders independently (event trigger, cron, condition). But there is no primitive to "wait until all N complete before firing order N+1."

**Documented community workarounds for fan-out → fan-in:**

No official documentation describes a fan-in pattern. The only confirmed approach derivable from available primitives is a counter-based workaround:

1. Each parallel exec order writes a flag file (e.g., `.gc/done/story-N`) on completion.
2. A condition-triggered order polls: `test $(ls .gc/done/ | wc -l) -ge N && exit 0 || exit 1`.
3. When the count reaches N, the condition passes and the downstream order fires.

This is INFERRED from the condition trigger semantics ("fires when exit code is 0") and exec order behavior. [UNVERIFIED] as an actual community practice — no documentation, blog post, or example was found confirming this pattern is used.

**Alternative approach (bead-based):** Because beads are queryable, an exec order could run `bd query --label=story-complete --status=closed --count` and compare against expected N. This avoids file system dependency. INFERRED from bead query primitives. [UNVERIFIED].

**The `pr-pipeline` pack** uses sequential stages (not parallel fan-in): planning → blast-radius → self-review → gate → ship. Each stage is a separate formula; pipeline proceeds linearly. This is not a fan-out pattern. CONFIRMED.

---

### 4. Pipeline Observability

**Observability is per-primitive, not pipeline-wide.** INFERRED.

Gas City does not have a pipeline-level view showing Order A → Order B → Order C with current state. The following per-primitive views exist:

| Command | What it shows |
|---|---|
| `gc order list` | All orders with trigger type |
| `gc order history` | Execution history (fired/completed/failed) per order |
| `gc order check` | Which orders are due right now |
| `gc converge list` | Active convergence loops (filterable by state/rig) |
| `gc converge status <id>` | Single loop: iteration count, gate mode, active wisp state |
| `gc events` | Raw event stream (JSON Lines), filterable by type, actor, sequence |
| `gc dashboard` | Supervisor-level: city state, agents running/suspended, rigs |

**`gc citystatus` does NOT show order history or convergence loops.** It shows controller state, agent running/suspended status, rigs, and summary counts only. CONFIRMED.

**`gc dashboard`** operates in supervisor mode (all cities) or city mode (all agents). It does not render a pipeline diagram. The dashboard renders city configuration and runtime state, not order execution history or convergence loop state. INFERRED (dashboard implementation not directly readable, but scope described in cmd_dashboard.go is supervisor/city-level only).

**`gc events` is the closest thing to a pipeline audit log.** Events are append-only, monotonically sequenced, and filterable by `Type`, `Actor`, `Since`, `AfterSeq`. Convergence events (`convergence.created`, `convergence.iteration`, `convergence.terminated`, `convergence.waiting_manual`) and order events (`order.fired`, `order.completed`, `order.failed`) are all emitted into this bus. A pipeline trace can be reconstructed from the event stream post-hoc. CONFIRMED.

**Pipeline view requires external tooling.** There is no `gc pipeline status` or equivalent. Practitioners monitoring a multi-order pipeline must query each order and loop independently or tail `gc events`. CONFIRMED.

---

### 5. Community Pipeline Examples

**No community examples of multi-loop pipelines were found.** CONFIRMED ABSENT.

Searches across `gastownhall` org repos, `gascity-packs`, and docs turned up no examples, blog posts, or third-party repos showing fix loops, human review loops with re-entry, or parallel fan-out with synchronization.

The closest real-world pattern found is the **`pr-pipeline` pack** (official, in `gascity-packs`), which implements:
- Four sequential formula stages (planning, blast-radius, self-review, ship)
- A human gate (`bd close <step-id>`) as a manual block before push
- An iterative self-review inner loop via convergence (the `mol-pr-ship` stage: "iterate self-review until clean")

This pack demonstrates nested convergence: a convergence loop *within* a pipeline stage. It does NOT demonstrate cross-stage looping (e.g., "if stage 4 fails, loop back to stage 2"). CONFIRMED.

**The `flywheel` pack** is an agent-enhancement stack (MCP mail, memory, bug scanning) — not a convergence loop pattern. Name is misleading relative to this research question. CONFIRMED.

---

## Synthesis

### What Gas City provides

Gas City's convergence primitive is mature and purpose-built. It handles the **AVFL fix loop** and **E2E fix loop** cases directly:

```
gc converge create \
  --formula avfl-fix \
  --target avfl-agent \
  --gate condition \
  --gate-condition ./scripts/check-score.sh \
  --max-iterations 10 \
  --var threshold=95
```

The gate condition script reads score output and exits 0 when >= 95. The loop runs the formula, evaluates the condition, and continues automatically until pass or max-iterations. This is exactly what both fix loops need, and it works without any custom scaffolding.

### What Gas City does NOT provide

Three gaps matter for the Momentum sprint pipeline:

**Gap 1: Human feedback injection.** `gc converge iterate` resumes the loop but carries no feedback text. The human has no in-system channel to say "here is what needs fixing." This is the most significant gap for the human review loop. Gas City's design assumes the formula prompt itself determines what to do next (e.g., reading a bead meta field the agent set, or reading the artifact from the prior iteration). A human "rejection with notes" has no native home.

**Gap 2: No barrier/join primitive.** Running N story validators in parallel and proceeding only when all N pass requires custom fan-in scaffolding — either flag files or bead count queries. This must be built by the sprint pipeline, not provided by Gas City.

**Gap 3: No pipeline-level observability.** There is no single view of "here is the current state of sprint pipeline steps A through E." Operators must query each order and convergence loop independently or parse the raw event stream.

### Key architectural insight

The convergence loop and the order system are **independent primitives** in Gas City. An order can dispatch a convergence loop as its formula action. But a convergence loop does not natively trigger an order on completion — it only emits events. To chain: "convergence loop completes → next order fires," an event-triggered order must subscribe to `convergence.terminated` events. This is theoretically possible (the order `On` field accepts any event type string), but no documentation confirms `convergence.terminated` as a valid subscription target, and no examples demonstrate it. [UNVERIFIED].

---

## Open Questions

1. **Can an order's event trigger subscribe to `convergence.terminated` events?** The `On` field accepts arbitrary event type strings, and `convergence.terminated` is a confirmed event type — but no documentation or example confirms this pairing is tested or supported. This is the critical chaining question for the Momentum pipeline.

2. **What is the recommended pattern for human feedback injection?** If `gc converge iterate` is the rejection mechanism, how do practitioners convey reviewer notes to the next iteration? Is the artifact directory convention documented anywhere in Gas Town community channels?

3. **How does the `pr-pipeline` pack's inner convergence loop in `mol-pr-ship` terminate and hand control back to the outer pipeline stage?** Understanding this would reveal the intended chaining pattern for nested loops.

4. **Is there an undocumented `bd gate reject` or `gc converge reject` command?** Only `approve`, `iterate`, and `stop` were confirmed. The presence of the empty string parameter in `ApproveHandler` is suspicious and may indicate a reserved slot.

5. **For the fan-in problem: does Gas City's beads query layer support counting closed beads by label efficiently enough to use as a condition trigger without N-second polling overhead?** The condition trigger blocks the dispatch loop during execution; if the query is slow, all other orders stall.

---

## Pattern Recommendation

**For the Momentum sprint pipeline human-review-as-a-loop, the most practical Gas City model is:**

### Three-convergence-loop design with bead-mediated feedback

```
[AVFL Fix Loop]          [E2E Fix Loop]          [Human Review Loop]
gc converge create       gc converge create       gc converge create
  --formula avfl-fix       --formula e2e-fix        --formula apply-feedback
  --gate condition         --gate condition          --gate manual
  --gate-condition         --gate-condition          --max-iterations N
    ./score-check.sh         ./e2e-clean.sh
  --max-iterations 10      --max-iterations 10
```

**Human review loop mechanics:**

1. After E2E loop terminates (`approved`), an event-triggered order fires the human-review convergence loop.
2. The formula runs a "present for review" step (generates a summary report, creates a notification bead or sends a message).
3. Gate mode is `manual` — loop suspends to `waiting_manual`.
4. Human reviews. If satisfied: `gc converge approve <id>` — sprint proceeds.
5. If human wants fixes: the human writes feedback into a bead (via `bd meta set feedback.notes "..."` on the review bead, or into the artifact dir for the current iteration), then calls `gc converge iterate <id>`.
6. The next iteration's formula reads the feedback from the artifact dir or a bead query and generates fix tasks.
7. A nested AVFL/E2E fix loop runs against those fix tasks (either as a new convergence loop or as exec orders).
8. When fix loops complete, the formula's next step re-presents for review → loop suspends again.
9. Repeat until `gc converge approve`.

**Tradeoffs of this design:**

- Feedback injection via artifact dir or bead meta is a workaround, not a native feature. It requires the formula prompt to know where to look.
- `gc converge iterate` does not atomically carry the feedback — there is a gap between "human writes feedback" and "human calls iterate" where the loop could be accidentally advanced without feedback present.
- The nesting of fix loops inside a human review loop's iteration is not a native Gas City concept — it requires the formula itself to orchestrate the fix loop (either by calling `gc converge create` as a shell step, or by the formula's steps being themselves a multi-step fix sequence).

**Alternative simpler design (if feedback fidelity is not critical):**

Use a single manual-gate convergence loop where each iteration is the full sprint pipeline (AVFL + E2E + review prep). Human approves or iterates. The formula handles all sub-work in its steps. This avoids nested loop coordination but loses granularity — every human rejection re-runs everything, including already-passing validators.

**The recommended design for Momentum** is the three-loop model, with the human-review loop's formula using `ArtifactDir` for feedback files. The sprint pipeline orchestrator should write a `human-feedback-required.md` template into the artifact dir at loop creation time, and document the convention that human reviewers fill in that file before calling `gc converge iterate`. This keeps the pattern legible without requiring Gas City to add a feedback payload feature.

The barrier/fan-in problem (waiting for N parallel validators) should be solved with a bead count condition: a single condition-triggered order queries `bd list --label=avfl-pass --status=closed` and proceeds when count equals expected N. This keeps the solution within Gas City primitives without external flag files.
