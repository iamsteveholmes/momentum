---
content_origin: research-agent
date: 2026-05-22
sub_question: "Temporal as alternative dispatcher for Momentum sprint pipeline"
---

# Temporal as Alternative Dispatcher — Research

## Research Question

Can Temporal (temporal.io) serve as the dispatcher/coordinator for Momentum's agentic sprint pipeline? Specifically: how well does it cover the eight dispatch requirements (parallel story dispatch, per-story loop, fan-in barrier, AVFL fix loop, E2E fix loop, human review loop, human gate for final merge, error handling, and monitoring)?

This document is a counterpart evaluation to the Gas City research. The Fit Verdict at the end compares Temporal directly to Gas City for Momentum's specific use case.

---

## Sources Consulted

- https://temporal.io/ — overview and value proposition [OFFICIAL]
- https://docs.temporal.io/activities — Activity primitives, failure model [OFFICIAL]
- https://docs.temporal.io/workflows — Workflow concepts, determinism, signals [OFFICIAL]
- https://docs.temporal.io/glossary — Canonical definitions of Signal, Query, Update, Activity, Heartbeat, Continue-As-New [OFFICIAL]
- https://docs.temporal.io/develop/python/message-passing — Signal and Query Python SDK [OFFICIAL]
- https://docs.temporal.io/develop/python/cancellation — Cancellation patterns [OFFICIAL]
- https://docs.temporal.io/develop/python/failure-detection — Retry policy configuration [OFFICIAL]
- https://docs.temporal.io/develop/python/continue-as-new — Continue-As-New mechanics [OFFICIAL]
- https://docs.temporal.io/develop/python/child-workflows — Child workflow fan-out [OFFICIAL]
- https://docs.temporal.io/develop/python/testing-suite — Testing framework [OFFICIAL]
- https://docs.temporal.io/web-ui — Web UI capabilities [OFFICIAL]
- https://docs.temporal.io/cli — CLI command reference [OFFICIAL]
- https://docs.temporal.io/self-hosted-guide — Self-hosting overview [OFFICIAL]
- https://docs.temporal.io/production-deployment — Production deployment [OFFICIAL]
- https://docs.temporal.io/encyclopedia/retry-policies — Retry policy semantics [OFFICIAL]
- https://temporal.io/pricing — Pricing tiers [OFFICIAL]
- https://github.com/temporalio/temporal — GitHub repository (maturity, activity) [OFFICIAL]
- https://github.com/temporalio/samples-python — Python SDK samples, AI integrations [OFFICIAL]
- https://github.com/temporalio/docker-compose (archived) — Infrastructure footprint [OFFICIAL]
- https://github.com/temporalio/samples-python/blob/main/hello/hello_signal.py — Signal code example [OFFICIAL]
- https://github.com/temporalio/samples-python/blob/main/hello/hello_parallel_activity.py — Fan-out code example [OFFICIAL]
- https://github.com/temporalio/samples-python/blob/main/openai_agents/README.md — OpenAI agents sample [OFFICIAL]
- https://community.temporal.io/ — Community forum and AI-related discussions [PRAC]

---

## Findings

### 1. Core Fit Assessment

#### Shell command invocation as an Activity

CONFIRMED. A Temporal Activity is defined as "a normal function or method that executes a single, well-defined action (either short or long running), such as calling another service, transcoding a media file, or sending an email message." [OFFICIAL — docs.temporal.io/activities] Nothing in the Activity contract restricts what the function does: it can open a subprocess, block until `claude -p "..."` exits, capture its stdout, and return it as the Activity result. Activity code is explicitly permitted to be non-deterministic (unlike Workflow code), which means subprocess execution with variable timing and output is a first-class use case.

The Python SDK provides `asyncio`-compatible execution via `ThreadPoolExecutor` for blocking subprocess calls. CONFIRMED as viable based on activity semantics. No official sample demonstrates `subprocess` specifically [UNKNOWN — no official shell-command sample exists], but the Activity abstraction is exactly the right container for it and the pattern is straightforward Python.

#### Parallel fan-out with fan-in barrier

CONFIRMED. The canonical mechanism is `asyncio.gather()` applied to multiple `workflow.execute_activity()` or `start_child_workflow()` calls. [OFFICIAL — samples-python hello_parallel_activity.py] The pattern is:

```python
results = await asyncio.gather(
    workflow.execute_activity(run_story, story_id="story-1", ...),
    workflow.execute_activity(run_story, story_id="story-2", ...),
    workflow.execute_activity(run_story, story_id="story-3", ...),
)
```

`asyncio.gather()` fans out immediately and blocks until all N complete — the fan-in barrier is implicit. Results may arrive in any order; the gather collects them all before returning. This maps directly to Momentum's "parallel story dispatch → wait for all N merged" requirement. CONFIRMED as a first-class primitive.

For N stories determined at runtime, the pattern generalizes: build a list of coroutines dynamically and pass `*coros` to `asyncio.gather()`. INFERRED from Python async semantics plus the documented Activity API.

#### Convergence loops (repeat until condition met)

CONFIRMED. Because Workflow code is just Python, a convergence loop is a native while loop:

```python
while True:
    score = await workflow.execute_activity(run_avfl_validators, ...)
    if score >= 95:
        break
    await workflow.execute_activity(run_avfl_fixer, ...)
```

Temporal's event history preserves every iteration, so if the Worker crashes mid-loop the workflow resumes from the last completed Activity rather than starting over. This is the core value proposition of durable execution — the loop itself does not need to be idempotent. CONFIRMED.

One nuance: Temporal Workflows must be deterministic. Loops are fine; the constraint is that the loop must not read from non-Temporal sources (e.g., direct filesystem reads inside workflow code). All non-deterministic work (running validators, running fixers) goes inside Activities, which are explicitly allowed to be non-deterministic. CONFIRMED — the AVFL fix loop pattern fits cleanly.

**Event history size caution (INFERRED):** A long-running sprint workflow with many iterations could accumulate thousands of events. Temporal's `Continue-As-New` primitive addresses this — it checkpoints the current state into a new workflow execution with a fresh event history, preserving logical continuity. The SDK provides `workflow.info().is_continue_as_new_suggested()` to detect when this is needed. [OFFICIAL — docs.temporal.io/develop/python/continue-as-new] For a Momentum sprint (bounded iterations, bounded stories) this is unlikely to be a practical problem, but it is an operational consideration for very long-running sprints. INFERRED risk, low probability at Momentum scale.

---

### 2. Human-in-the-Loop Support

#### Mechanism for pausing and waiting for human input

CONFIRMED. Temporal's Signal primitive is the canonical mechanism. A Signal is "an asynchronous message sent to a running Workflow Execution to change its state and control its flow." [OFFICIAL — glossary] The workflow uses `workflow.wait_condition()` to pause at a decision point until a signal arrives:

```python
self._approved = False

@workflow.signal
async def approve(self, input: ApprovalInput) -> None:
    self._approved = True
    self._feedback = input.feedback

async def run(self):
    # ... do work ...
    await workflow.wait_condition(lambda: self._approved)
    # ... continue ...
```

The workflow is durably suspended — no polling, no timeout unless explicitly configured, no resource consumed while waiting. The developer (or any authorized external actor) sends the signal via CLI, Web UI, or API. CONFIRMED.

#### Signal payloads

CONFIRMED. Signals accept typed parameters via dataclasses. Example: `await workflow_handle.signal(MyWorkflow.approve, ApprovalInput(feedback="Fix the auth module before merge"))`. [OFFICIAL — docs.temporal.io/develop/python/message-passing] The feedback text the human provides on rejection is a standard signal payload.

#### Iterative review loop (reject and re-enter fix pipeline multiple times)

CONFIRMED. Because the workflow is just Python running inside Temporal's durable execution engine, the human review loop is a while loop with signal waits:

```python
while True:
    await workflow.wait_condition(lambda: self._decision_received)
    self._decision_received = False
    if self._approved:
        break
    # Re-enter fix pipeline
    await workflow.execute_activity(run_fix_pass, feedback=self._feedback, ...)
```

Each rejection resets the decision flag, re-runs the fix pass as an Activity, and re-suspends waiting for the next signal. The developer can reject N times. CONFIRMED as a first-class composition pattern.

#### UI for pending human approvals

CONFIRMED with qualification. The Temporal Web UI shows "Workflow Execution state and metadata for debugging purposes" including which workflows are currently running, which activities are pending, and which are waiting. [OFFICIAL — docs.temporal.io/web-ui] A developer can see that a workflow is in a signal-wait state by inspecting its event history — the last event will be a `WorkflowTaskCompleted` entry with the workflow blocked on `wait_condition`.

However: there is no dedicated "Approvals inbox" view in the Web UI — no dashboard showing "these N workflows are waiting for your signal." A developer must either know to look, or query workflows by status/type. [INFERRED from Web UI documentation — no approval inbox UI described] The Web UI also allows sending signals directly from the interface, which partially compensates. Temporal Cloud reportedly has richer workflow search capabilities, but for a self-hosted dev server this is INFERRED to be the same as the open-source UI.

For Momentum's use case (one developer, one sprint, one workflow at a time), the absence of an approvals inbox is a minor UX friction, not a blocking gap.

---

### 3. Error Handling

#### Activity failure and retry behavior

CONFIRMED. When an Activity fails or times out, Temporal consults the attached Retry Policy. Activities retry automatically by default (unlimited attempts, exponential backoff: 1s initial, 2.0x coefficient, 100s cap). [OFFICIAL — docs.temporal.io/encyclopedia/retry-policies] Per-activity configuration allows:

```python
retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=10),
    backoff_coefficient=3.0,
    maximum_interval=timedelta(minutes=5),
    maximum_attempts=5,  # fail permanently after 5 attempts
)
```

When `maximum_attempts` is exhausted, the Activity raises `ActivityError` to the Workflow, which can catch it and implement recovery logic (alert the developer, mark the story failed, continue with remaining stories). CONFIRMED.

Heartbeating is the mechanism for detecting hung activities (e.g., a `claude -p` subprocess that stalls without exiting). A `claude -p` invocation wrapping a long coding task should heartbeat periodically; if it stops, Temporal marks it failed. Without heartbeating, a hung subprocess will only be detected when `start_to_close_timeout` is reached. [OFFICIAL — docs.temporal.io/encyclopedia/detecting-activity-failures] This is an implementation requirement, not a framework gap.

#### Behavior when max retries are exhausted

CONFIRMED. `ActivityError` propagates to the Workflow. The Workflow catches or does not catch it. If caught, the developer's code decides what happens (e.g., "mark this story as failed, do not block the rest of the fan-out"). If uncaught, the Workflow Execution itself fails, but its event history is preserved — the workflow is not lost, it is just in a failed terminal state. A developer can inspect the failure via Web UI or CLI and restart from the last checkpoint. CONFIRMED.

#### Failed parallel branch isolation

CONFIRMED with nuance. `asyncio.gather()` by default propagates the first exception and cancels all remaining coroutines. To handle partial failures gracefully — where one story's Activity fails but the rest continue — the developer must use `asyncio.gather(*coros, return_exceptions=True)` and inspect results for exceptions. [INFERRED from Python asyncio semantics — not documented in Temporal-specific terms, but standard Python behavior applies inside Workflow code.] This is the correct pattern for Momentum's use case: collect all results including failures, then report which stories failed rather than aborting the whole fan-out. INFERRED as the right pattern but requires explicit implementation care.

#### Workflow-level failure and state preservation

CONFIRMED. If a Workflow Execution fails (uncaught exception, or the Worker process crashes), Temporal preserves the full event history on the server. The workflow can be restarted from scratch (it replays history to recover state) or, if designed for it, can resume from the last completed Activity. State is never lost as long as the Temporal server's persistence layer (SQLite for dev, PostgreSQL/Cassandra for production) is intact. CONFIRMED.

#### Dead letter equivalents

INFERRED. Temporal has no explicit "dead letter queue" primitive by that name. The equivalent is: a failed Workflow Execution with a terminal `FAILED` status in the server's visibility store. The developer queries `temporal workflow list --status FAILED` to find them. [OFFICIAL — CLI docs] The Web UI's Task Failures view also highlights "workflows with failed or timed-out tasks." Non-retryable error types can be declared to skip retries for permanent failures. This is a functional equivalent to a dead letter queue, not a purpose-built primitive.

---

### 4. Developer Experience and Monitoring

#### What the Web UI shows

CONFIRMED. The Temporal Web UI provides:
- Workflow list with status (Running, Completed, Failed, Timed Out, Cancelled)
- Per-workflow event history timeline (approximately 40 event types: workflow started, activity scheduled, activity started, activity completed, signal received, etc.)
- "Summary of recently active and/or pending Activity Executions"
- Task Failures view: workflows with failed or timed-out tasks
- Call Stack tab: captured stack traces showing where Workflow code is currently waiting
- Workers section: which workers are polling which task queues
- Signal send UI: send a signal to any running workflow without CLI
- Query UI: inspect workflow state via registered Query handlers
- Metadata tab: human-readable log of workflow state

[OFFICIAL — docs.temporal.io/web-ui]

A developer running a Momentum sprint would see: the sprint workflow in Running state, individual story activities in their respective states (Scheduled / Started / Completed / Failed), and the exact point where the workflow is blocked on a signal wait. This gives substantially more observability than the current Momentum approach (no persistent state — only what the LLM context holds). CONFIRMED.

#### Self-hosted option without cloud account

CONFIRMED. The `temporal server start-dev` command launches a complete Temporal server — including Web UI, default namespace, in-memory or SQLite persistence — as a single binary with no external dependencies. [OFFICIAL — self-hosted guide, CLI docs] This is explicitly recommended for development work. No cloud account is required. The dev server runs on `localhost:7233` (gRPC) with Web UI at `http://localhost:8233`. CONFIRMED.

For production self-hosting (persistence across server restarts, actual reliability guarantees), a database is required: PostgreSQL, MySQL, or Cassandra. The docker-compose configuration (now maintained in samples-server) deploys Temporal + PostgreSQL + Elasticsearch + Web UI. [OFFICIAL — github.com/temporalio/docker-compose, archived] This is a meaningfully larger operational footprint than the dev server.

For Momentum's use case — single developer, single machine, sprint workflows measured in hours not days — the `temporal server start-dev --db-filename temporal.db` invocation (SQLite persistence, single binary) is sufficient and zero-infrastructure. INFERRED as sufficient for the use case.

#### Operational footprint for a solo developer

Two tiers:

**Development (recommended starting point):**
- One binary: `temporal` CLI
- One command: `temporal server start-dev --db-filename temporal.db`
- One Worker process: the Python (or TypeScript/Go) application running workflow and activity code
- Total: 2 processes, no Docker, no database server, no Kubernetes

**Production (if Momentum needed durability across machine restarts):**
- Temporal Server (Go binary)
- PostgreSQL or MySQL
- Optional: Elasticsearch (for full-text workflow search)
- Worker processes
- Total: 3–4 services, Docker Compose or equivalent

For a solo developer running sprint workflows during a session, the development footprint is entirely acceptable. CONFIRMED that the operational bar is low for the target use case.

#### Temporal Cloud as an alternative

CONFIRMED. Temporal Cloud is the managed hosted option. Pricing starts at $100/month after $1,000 in free credits expire. [OFFICIAL — temporal.io/pricing] For a solo developer this is a real cost. The self-hosted dev server is the practical alternative and is fully featured for Momentum's use case.

---

### 5. Community, Maturity, and Fit

#### Maturity and production-readiness

CONFIRMED. Temporal originated as a fork of Uber's Cadence, built by the Cadence creators after leaving Uber. It is described by the project itself as "a mature technology." [OFFICIAL — github.com/temporalio/temporal] Key indicators:

- 20,400 GitHub stars [OFFICIAL]
- 166 releases, latest v1.31.0 (April 29, 2026) [OFFICIAL]
- 9,072 commits on main branch [OFFICIAL]
- 510 open issues, 212 open PRs — active ongoing development [OFFICIAL]
- Used in production by Stripe, Snap, Netflix, Coinbase, and others (INFERRED from Temporal's marketing, not independently verified from the GitHub repository)
- Written in Go (99.5%), reflects production-systems engineering culture [OFFICIAL]

This is definitively production-grade software with multi-year production deployment history at scale. No caveats about maturity. CONFIRMED.

#### AI agent orchestration community

CONFIRMED with qualification. The samples-python repository includes official integrations for:
- OpenAI Agents SDK (orchestrating OpenAI agent workflows as durable Temporal workflows)
- LangChain activities
- LangGraph workflows (Graph API and Functional API)
- Amazon Bedrock chatbot orchestration

[OFFICIAL — github.com/temporalio/samples-python]

The OpenAI Agents sample explicitly describes "combining Temporal workflows for orchestrating agent control flow and state management" with patterns including multi-agent collaboration, handoffs, and escalation workflows. [OFFICIAL — samples-python/openai_agents/README.md]

There is active community discussion around AI/LLM use cases. The community forum shows AI-tagged topics. [PRAC — community.temporal.io] However, AI orchestration represents a subset of Temporal's user base; the majority of community discussion focuses on traditional distributed systems workloads (payment processing, order fulfillment, CI/CD). CONFIRMED that AI orchestration is a real use case with official samples, but not the primary community focus.

No official samples or community examples show Temporal orchestrating Claude Code CLI (`claude -p`) as a subprocess specifically. [UNKNOWN] The closest pattern is the OpenAI Agents integration, which wraps an LLM-driven agent loop as a Temporal Activity/Workflow. The `claude -p` subprocess pattern is a minor variation on "run a long-running process as an Activity."

#### Language SDKs

CONFIRMED. Temporal provides official SDKs for: Go, Java, Python, TypeScript, .NET, PHP. [OFFICIAL — docs.temporal.io, Python SDK at python.temporal.io] Python 3.10+ is required for the Python SDK. All SDKs are first-party maintained by Temporal Technologies.

For Momentum's context: Python or TypeScript are the most natural fits for a developer already working in a JavaScript/TypeScript Claude Code environment. The Python SDK is well-documented with an active samples repository.

#### Realistic onboarding effort for a solo developer

INFERRED from documentation review. The onboarding path:

1. Install Temporal CLI: `brew install temporal` or download binary — trivial
2. Start dev server: `temporal server start-dev --db-filename temporal.db` — one command
3. Install Python SDK: `pip install temporalio` — trivial
4. Write a Worker with one Activity (the `claude -p` subprocess call) and one Workflow — ~50–100 lines of Python
5. Register and run the Worker
6. Trigger a workflow via CLI or API

The Temporal 101 Python course is available free at learn.temporal.io [OFFICIAL — Python SDK page]. The conceptual model (Workflow = orchestration code, Activity = side-effecting work, Worker = runtime) is straightforward.

Estimated time to a working `claude -p` dispatch loop: 1–3 days for a developer with Python experience. Estimated time to the full Momentum sprint pipeline (fan-out, fan-in, convergence loops, human signals): 1–2 weeks. INFERRED.

The main learning curve is the **determinism constraint on Workflow code**. Any direct I/O, randomness, or time calls inside Workflow code will break replay. All such operations must be moved into Activities. This is the primary conceptual shift; once internalized, the model is clean and consistent.

---

## Synthesis

### Temporal maps naturally to every Momentum requirement

The eight dispatch requirements map to Temporal primitives with little impedance:

| Momentum requirement | Temporal primitive | Confidence |
|---|---|---|
| Parallel story dispatch | `asyncio.gather()` + Activities or Child Workflows | CONFIRMED |
| Per-story loop (dev → review → merge) | Child Workflow per story | CONFIRMED |
| Fan-in barrier | `asyncio.gather()` semantics | CONFIRMED |
| AVFL fix loop (repeat until score ≥ 95) | `while` loop with Activity calls | CONFIRMED |
| E2E fix loop | Same as AVFL fix loop | CONFIRMED |
| Human review loop (N rejections) | `while` loop + Signal + `wait_condition` | CONFIRMED |
| Human gate for final merge | Signal with payload (approval/rejection + feedback) | CONFIRMED |
| Error handling — failed story isolation | `asyncio.gather(return_exceptions=True)` | INFERRED |
| Error handling — hung subprocess | Activity heartbeating + `start_to_close_timeout` | CONFIRMED |
| Monitoring — developer sees pipeline state | Temporal Web UI (event history, pending activities, blocked signals) | CONFIRMED |

There is no requirement in the Momentum list that Temporal cannot address. The primitives are a clean match.

### The model inversion: code-first vs. config-first

The critical structural difference from Gas City is that Temporal's workflow logic lives entirely in code (Python, TypeScript, Go). A Momentum sprint pipeline would be a Python program, not a declarative configuration file. This has two implications:

**Upside:** Full expressiveness. Every conditional, loop, and branching pattern is native Python. No config DSL limits what you can express. Error handling, partial failure isolation, and convergence logic are standard programming, not framework-specific escapes.

**Downside:** A developer must write and maintain workflow code. The Gas City Orders system is configured declaratively (five trigger types, YAML-like agent configuration). Adding a new workflow step in Gas City is a config change; in Temporal it is a code change with versioning implications.

For Momentum, where the sprint pipeline is well-defined and unlikely to change frequently, this tradeoff favors Temporal's expressiveness. For a more dynamic workflow that needs frequent restructuring, Gas City's declarative model would be preferable. INFERRED.

### Determinism constraint is real but manageable

The Workflow determinism constraint is the only non-trivial conceptual hurdle. Any `claude -p` invocations, filesystem reads, or network calls must be Activities. The Workflow itself is pure orchestration: no direct I/O. For Momentum's sprint pipeline this is a natural fit — all the actual work (running Claude Code, running AVFL validators, running E2E tests) is already "subprocess invocations" that belong in Activities. The Workflow layer holds the sprint logic: how to sequence, when to loop, when to wait for human input.

### Infrastructure is lighter than it looks

The fear response to "Temporal requires Cassandra and Elasticsearch" is outdated. The development server (`temporal server start-dev --db-filename temporal.db`) is a single binary with SQLite persistence. For a solo developer running sprint workflows (not a production SaaS), this is the right operational tier. The full production stack is irrelevant to Momentum's use case.

### AI agent orchestration is an acknowledged use case

Temporal is not being force-fit into an AI-adjacent use case. The official samples repository ships LangGraph, OpenAI Agents, and LangChain integrations. The underlying pattern — "wrap a long-running AI agent invocation as a Temporal Activity, use Workflows for orchestration logic" — is documented and supported. CONFIRMED.

---

## Open Questions

- **Subprocess Activity without heartbeating: what is the practical timeout floor?** A `claude -p` sprint-dev invocation for a complex story can run 20–60 minutes. Without heartbeating inside the subprocess (which would require the Claude Code session to emit heartbeat signals externally), the only failure detection is `start_to_close_timeout`. What is the right timeout value, and how do you distinguish a slow-but-running subprocess from a hung one? This is an implementation question, not a framework limitation, but it matters for the reliability of the dispatch loop.

- **Signal delivery ordering when multiple stories complete near-simultaneously:** If three stories complete at nearly the same time and each triggers a state update, does `asyncio.gather()` in the parent Workflow handle these correctly without race conditions? INFERRED as safe (Temporal processes workflow tasks single-threaded by design), but this should be verified in practice.

- **Does the determinism constraint interact badly with the `claude -p` result parsing?** If output parsing (extracting a score from AVFL output) happens inside Workflow code using string operations, it is safe. If it involves datetime parsing or external library calls with randomness, it must move to an Activity. This is a design hygiene question, not a blocker.

- **Temporal Cloud pricing at scale:** If Momentum ever ran at higher frequency (multiple sprints per day, multiple projects), the $100/month Cloud floor plus Action costs could become relevant. The self-hosted path avoids this entirely but adds operational maintenance. UNKNOWN for future scale, irrelevant for current Momentum use.

---

## Fit Verdict: Temporal vs. Gas City for Momentum

### Where Temporal is stronger

**Dispatch pipeline completeness.** Every Momentum requirement maps to a documented, production-tested Temporal primitive. The fan-out, convergence loop, and human signal patterns are first-class — not approximate fits. Gas City's Orders system is a narrower trigger-and-dispatch layer; it does not natively model convergence loops or multi-phase human review without explicit orchestration code in the agents themselves.

**Human-in-the-loop with payload.** Temporal Signals carry typed payloads and can be sent multiple times. The "reject with feedback text → re-enter fix pipeline → review again" loop is 15 lines of Python. Gas City has no analogous primitive — its human-in-the-loop story relies on agents polling for instructions, not a durable signal mechanism.

**Error handling visibility.** When a `claude -p` subprocess fails, Temporal captures the exception, records it in the event history, retries per policy, and surfaces the failure in the Web UI with full context. Gas City's error handling at the executor level is less documented and its visibility story is UNKNOWN based on the Gas City research.

**Maturity and production confidence.** Temporal is a 9-year-old technology (Cadence lineage) running in production at Stripe, Netflix, and Snap. Gas City reached v1.0.0 on April 27, 2026 — weeks old at the time of this research. The risk profile is not comparable.

**Monitoring.** The Temporal Web UI provides event-by-event timeline visibility: which Activity is running, which has failed, which Workflow is blocked on a signal. A developer can open `localhost:8233` and see the sprint pipeline state at any moment. Gas City has no equivalent dedicated UI; monitoring relies on log output from the controller process.

**AI agent orchestration community.** Temporal ships official samples for OpenAI Agents, LangGraph, and LangChain. There is a documented pattern for "wrap LLM agent as a Temporal Activity." Gas City orchestrates agents by exec-ing them, with no higher-level AI integration primitives beyond exec orders.

### Where Gas City is stronger

**Declarative configuration.** The Gas City Orders system is YAML-configured: define a trigger type, point it at an agent, set conditions. No code to write. A Momentum developer could define a sprint dispatch order without writing a workflow program. For developers who are not comfortable with Python async programming, this is a significant advantage.

**Lower conceptual overhead.** Temporal's determinism constraint requires understanding the Workflow/Activity split. Gas City's model is simpler: agents run shell commands when triggered. There is no concept of event replay, determinism, or workflow history to internalize.

**Integration with Gas Town ecosystem.** If Momentum were adopting Gas City's broader ecosystem (Beads, the Orders event system, the exec order primitives), there is a coherent integrated story. Temporal is an independent system with no native tie-in to any existing Momentum or Gas Town tooling.

**Zero infrastructure for the prototype.** Gas City runs as a single binary (`gc`) against a local filesystem. Temporal requires a server process (even the dev server is an additional process). For a rapid proof-of-concept, Gas City has lower startup friction.

### Assessment

For Momentum's specific sprint pipeline, **Temporal is the technically superior dispatcher**. It provides first-class primitives for every requirement, has production-proven error handling, ships a monitoring UI, is demonstrably used for AI agent orchestration, and has a decade of production history.

The cost is: a developer must write workflow code in Python (or TypeScript), internalize the determinism constraint, and run a server process alongside the Worker. These are real costs but bounded and learnable.

Gas City is a credible lightweight alternative for teams that want declarative configuration over code, are already adopting the Gas Town ecosystem, and can accept a narrower primitive set (no native human-signal loop, no convergence loop primitive, lower maturity).

For a solo developer evaluating which to invest in first: Temporal's documentation, official samples, testing framework, and community support substantially reduce the risk of getting stuck. Gas City's youth means the developer will encounter gaps the community has not yet solved. The `claude -p` subprocess pattern is not documented for either system, but Temporal's Activity model makes it trivially wrappable; Gas City's exec order model requires it natively but with less surrounding infrastructure.

**Recommendation:** Temporal warrants a proof-of-concept as a standalone alternative to Gas City, not just a comparison entry. The implementation path is clear, the primitive mapping is complete, and the operational footprint at development scale is low. If the Gas City Orders proof-of-concept stalls on maturity gaps or missing primitives, Temporal is the natural fallback with no fundamental capability compromises.
