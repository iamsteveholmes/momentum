---
content_origin: research-agent
date: 2026-05-22
sub_question: "Survey of orchestration alternatives to Gas City for Momentum dispatcher"
---

# Orchestration Alternatives Survey — Dispatcher for Momentum

## Research Question

What orchestration tools beyond Gas City, Temporal, LangGraph, and GitHub Actions could serve as the dispatcher layer for Momentum's sprint pipeline? Do any deserve a full evaluation? And what is the simplest possible approach — Beads alone with shell scripts and a filesystem watcher — compared to Gas City?

## Sources Consulted

- https://microsoft.github.io/autogen/stable/ — AutoGen architecture overview
- https://github.com/microsoft/autogen — AutoGen maturity signals (58k stars, maintenance mode notice)
- https://docs.crewai.com/introduction — CrewAI architecture
- https://github.com/crewAIInc/crewAI — CrewAI maturity (52k stars, v1.14.5, 192 releases)
- https://github.com/openai/swarm — OpenAI Swarm status (deprecated, replaced by Agents SDK)
- https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/ — Magentic-One architecture
- https://huggingface.co/docs/smolagents/en/index — SmolAgents primitives
- https://rivet.ironcladapp.com/ — Rivet visual AI editor
- https://docs.agentops.ai/v1/introduction — AgentOps observability
- https://agentstack.sh/ — AgentStack scaffolding
- https://docs.agentstack.sh/ — AgentStack documentation
- https://www.inngest.com/docs/ — Inngest architecture and primitives
- https://www.inngest.com/docs/self-hosting — Inngest self-hosting requirements
- https://www.inngest.com/docs/features/inngest-functions/steps-and-workflows/step-parallelism (via inngest.com/docs) — Inngest parallelism model (fan-out via Promise.all, fan-in via waitForEvent)
- https://github.com/inngest/inngest — Inngest maturity (5.4k stars, v1.21.0, 246 releases)
- https://docs.prefect.io/v3/get-started/index — Prefect architecture
- https://docs.prefect.io/v3/develop/task-runners — Prefect parallel task runners
- https://docs.prefect.io/v3/develop/inputs — Prefect human-in-the-loop primitives
- https://github.com/PrefectHQ/prefect — Prefect maturity (22.4k stars, v3.7.1, 823 releases)
- https://docs.dagster.io/getting-started — Dagster architecture
- https://airflow.apache.org/docs/apache-airflow/stable/index.html — Airflow architecture
- https://dagger.io/ — Dagger overview
- https://docs.dagger.io/ — Dagger core primitives
- https://docs.dagger.io/quickstart/ — Dagger execution model (container-centric)
- https://docs.dagger.io/api/llm/ — Dagger LLM integration
- https://docs.dagger.io/cookbook — Dagger execution patterns (container-native, not host subprocesses)
- https://github.com/dagger/dagger — Dagger maturity (15.9k stars, v0.20.8, 871 releases)
- https://buildkite.com/docs/pipelines/getting-started — Buildkite architecture
- https://buildkite.com/docs/pipelines/controlling-concurrency — Buildkite concurrency/fan-out
- https://buildkite.com/docs/pipelines/block-step — Buildkite human approval (block steps)
- https://buildkite.com/pricing — Buildkite pricing (SaaS-required)
- https://modal.com/docs/guide — Modal architecture (cloud-only)
- https://github.com/watchexec/watchexec — watchexec filesystem watcher
- https://eradman.com/entrproject/ — entr filesystem watcher and limitations
- Prior Momentum research corpus:
  - docs/research/claude-code-background-dispatcher-2026-05-17.md — prior dispatcher research establishing the Claude-native baseline
  - docs/research/hermes-claude-dispatcher-momentum-2026-05-18-final.md — Hermes evaluation and state-ownership split-brain finding
  - docs/research/gas-town-dispatcher-2026-05-20/final/gas-town-dispatcher-final-2026-05-20.md — Gas City evaluation establishing the comparison baseline
  - docs/research/beads-vs-momentum-tracker-evaluation-2026-05-16.md — Beads architecture and role

---

## Findings

### Momentum's Dispatcher Requirements (Evaluation Frame)

Confirmed from prior research and scope.md (CONFIRMED): The dispatcher needs to:
1. Launch parallel `claude -p` shell subprocesses on separate git worktrees
2. Coordinate per-story pipelines (dev → review → merge)
3. Wait for all stories before corpus-level validation (fan-in barrier)
4. Run convergence fix loops (validate → fix → re-validate, N times)
5. Surface human review with iterative feedback and re-execution
6. Gate merge to main on explicit human approval
7. Fail loudly — no silent hangs
8. Provide pipeline state visibility

The work unit is a `claude -p "..."` shell subprocess. The dispatcher coordinates; it does not itself do agentic work. This distinction eliminates most of the tools surveyed below before analysis even begins.

---

## AI-Specific Frameworks

### AutoGen (Microsoft)

AutoGen is Microsoft's multi-agent conversation framework, now structured in four layers: Core (event-driven agent primitives), AgentChat (high-level multi-agent teams), Studio (no-code UI), and Extensions. It supports GraphFlow, Swarm-style handoffs, and SelectorGroupChat as team coordination patterns. It has 58k GitHub stars and a large contributor base.

The architectural mismatch with Momentum is complete. AutoGen's design centers on **LLM-to-LLM conversation** — agents send messages to each other and an orchestrating LLM decides what happens next. Momentum's dispatcher is not an LLM; it is a deterministic scheduler that invokes `claude -p` as opaque subprocesses and tracks their exit codes and output. AutoGen has no concept of "spawn a shell command and wait for it to finish before proceeding." Its code execution support (DockerCommandLineCodeExecutor) is about giving an LLM the ability to run code it generates — not about scheduling external agent processes.

Additional disqualifiers: AutoGen is **in maintenance mode** as of 2025 — Microsoft's own README states no new features and recommends "new projects" use the Microsoft Agent Framework instead. The succession path is uncertain. Even if it were actively maintained, using it here would mean wrapping `claude -p` calls inside AutoGen agent tool calls, producing a framework-on-top-of-framework stack with no benefit over plain Python subprocess management.

**Fit verdict: Poor. Wrong abstraction layer, wrong design center, maintenance mode.**

---

### CrewAI

CrewAI is a role-based multi-agent framework with 52k stars and active production use (v1.14.5 as of May 2026). Its two-tier model — Flows (state management, event-driven orchestration) + Crews (agent collaboration teams) — is genuinely capable for production multi-agent pipelines with human-in-the-loop support, callbacks, and guardrails on tasks.

The mismatch is the same as AutoGen but less severe: CrewAI is built for **LLM-based agents** that it instantiates, manages, and routes. `claude -p` is a black-box subprocess, not a CrewAI agent. Wrapping it as a CrewAI "tool" is technically possible but converts a lightweight dispatcher problem into a framework integration project. CrewAI would add a Python service layer, its own state model, and its own agent concept — all of which would sit parallel to Beads without an integration path. The prior corpus found this same split-brain problem in the Hermes evaluation and concluded it was a decisive disqualifier.

CrewAI's strongest relevant capability is its Flows system, which supports conditional branching, state persistence, and parallel execution — patterns genuinely useful for the sprint pipeline. But these capabilities are available more cheaply through Prefect, Inngest, or plain Python asyncio, without importing a framework that insists on owning agents.

**Fit verdict: Poor. LLM-agent-centric, state split-brain risk, overkill for subprocess coordination.**

---

### OpenAI Swarm

Swarm is **deprecated**. OpenAI's own repository states it is "replaced by the OpenAI Agents SDK" and no longer maintained. It was explicitly described as "educational" and not for production use. Nothing further to evaluate.

**Fit verdict: Eliminated. Deprecated.**

---

### Magentic-One (Microsoft)

Magentic-One is a Microsoft Research system built on AutoGen with five hardwired agent roles (Orchestrator, WebSurfer, FileSurfer, Coder, ComputerTerminal). It is a **research project**, not a framework for building custom pipelines. Its agent roster is fixed; its design presupposes an orchestrating LLM doing planning via nested task and progress ledgers.

Nothing in Magentic-One applies to Momentum's dispatcher need. It is a complete system for autonomous research/web tasks, not an orchestration primitive. Using it would mean importing Microsoft's opinionated agent topology for a sprint dispatch problem it was not designed to solve.

**Fit verdict: Not applicable. Research system, not an orchestration primitive.**

---

### SmolAgents (HuggingFace)

SmolAgents is a lightweight Python library (~1,000 lines of core logic) for building code-writing agents (CodeAgent) and tool-calling agents (ToolCallingAgent). It supports multi-agent systems, MCP server tool consumption, sandboxed code execution (via Modal, E2B, Docker), and multi-model backends. It is genuinely elegant for its stated purpose.

Its stated purpose is writing agents that generate and execute code. It is not a scheduler or dispatcher. It has no concept of fan-out across subprocesses, wait-for-all barriers, human approval gates, or pipeline state visibility. The "multi-agent system" support means one SmolAgent can call another SmolAgent — it does not mean "launch N parallel shell subprocesses and collect their results." SmolAgents is a tool for building Claude-equivalent behavior cheaply, not for scheduling Claude.

**Fit verdict: Not applicable. Agent authoring library, not a scheduler.**

---

### Rivet

Rivet is a visual AI workflow editor — a graph-based LLM chain builder with a desktop GUI where you wire up nodes representing prompts, tools, and logic. Workflows are stored as YAML and can be executed programmatically via an API. It is production-used at Ironclad.

Rivet is a prompt-chain design tool. It has no subprocess invocation model, no parallelism semantics for launching N Claude processes simultaneously, no human approval gate, and no pipeline state dashboard. Using it would require drawing a graph in a GUI for every sprint — a manual, not automated, approach. It solves a different problem (iterating on LLM prompts visually) and has no relevance to the dispatcher question.

**Fit verdict: Not applicable. Visual prompt design tool, not a dispatcher.**

---

### AgentStack

AgentStack describes itself as "create-next-app for Agents" — a CLI scaffolding tool that bootstraps agent projects with pre-built tools and code generation utilities. It is not a runtime framework, not a scheduler, and not an orchestration layer. It generates boilerplate for starting an agent project.

**Fit verdict: Not applicable. Scaffolding tool, not a dispatcher.**

---

### AgentOps

AgentOps is an **observability and monitoring platform** for AI agents — not a framework or orchestrator. It provides session tracking, LLM call visualization, timing breakdowns, and dashboard views of agent executions. It requires two lines of code to integrate and is compatible with multiple frameworks.

AgentOps is relevant only as a potential monitoring layer on top of whatever dispatcher Momentum builds — it does not compete with the dispatcher role itself. The "Monitoring" requirement in the dispatcher spec (requirement #8) is where AgentOps would apply: it could provide visibility into `claude -p` session behavior if integrated. But it does not schedule, coordinate, fan-out, or handle failures.

**Fit verdict: Not applicable as a dispatcher. Potentially relevant as an observability layer.**

---

## General Workflow / Pipeline Engines

### Inngest

Inngest is an event-driven durable execution platform. Its core model: functions are triggered by events, composed of discrete steps, and each step is individually retried on failure. It supports TypeScript, Python, and Go. Its parallelism model is explicit and capable: `Promise.all([step.run(...), step.run(...)])` in TypeScript and `ctx.group.parallel(...)` in Python execute steps concurrently with a fan-in at the await boundary. Fan-out across separate functions is handled by triggering events. The Dev Server provides full local execution with production parity — no cloud required for development. Self-hosting requires running a single binary (in-memory Redis + SQLite by default).

For Momentum's requirements, Inngest is the **most technically capable** of the general-purpose pipeline tools surveyed. It natively handles:
- Fan-out: `step.run` calls in parallel
- Fan-in barrier: `Promise.all` / `ctx.group.parallel`
- Fix loops: while-loop inside a function with `step.run` on each iteration (each iteration is checkpointed)
- Human approval: `waitForEvent` with a timeout — pause the function until a named event arrives (e.g., `sprint/approved`)
- Error handling: per-step retries, function-level error handlers
- Monitoring: built-in Dev Server dashboard showing function runs, step execution, events

Subprocess invocation is straightforward: a step runs arbitrary code, including `subprocess.run(["claude", "-p", ...])` in Python or `execSync("claude -p ...")` in TypeScript. The subprocess output becomes the step's return value, and if it fails the step retries.

The weaknesses for Momentum are: (1) Inngest is not local-first in the production sense — you either use Inngest Cloud (SaaS) or run the self-hosted binary, which is a real infrastructure component (not just a library); (2) the Server Side Public License (delayed Apache 2.0) creates a soft lock-in concern; (3) it requires standing up a web server endpoint that the Inngest runner calls back into, which is an architectural imposition for a local-machine sprint tool; (4) a solo developer running sprints locally would need to run the Inngest Dev Server as a sidecar process.

This is manageable but heavier than Gas City's `gc` binary. The critical question is whether Inngest's more mature durable-execution semantics (Temporal-style checkpointing, per-step retries) justify that overhead for Momentum's use case. For a sprint pipeline that runs perhaps once a week and whose "steps" are 5–40 minute Claude sessions, the durability guarantees are valuable but not obviously worth the infrastructure cost compared to a simpler approach.

**Fit verdict: Credible. Technically capable across all 8 requirements. Infrastructure overhead is real but manageable. Deserves consideration in shortlist.**

---

### Prefect

Prefect is a Python workflow orchestration framework with 22.4k stars, 823 releases, and production adoption at Fortune 50 companies. It uses `@flow` and `@task` decorators on plain Python functions. Parallelism is first-class: `TaskRunner` choices include `ThreadPoolTaskRunner` (concurrent threads), `ProcessPoolTaskRunner` (true parallel subprocesses), `DaskTaskRunner`, and `RayTaskRunner`. Fan-out is `task.submit()`; fan-in is automatic when a future is consumed by a downstream task, or explicit via `.wait()`.

Human-in-the-loop is a documented first-class feature: `pause_flow_run(wait_for_input=...)` halts execution and presents a typed form in the Prefect UI; `suspend_flow_run` is the same but also cleans up compute resources. This is the strongest HITL primitive of any tool surveyed here. Prefect can run fully locally — `prefect server start` runs at `localhost:4200` with a full monitoring dashboard, no cloud required.

For Momentum's requirements, Prefect maps well:
- Parallel story dispatch: `ProcessPoolTaskRunner` or `task.submit()` for each story
- Per-story convergence: sequential tasks within a story's sub-flow
- Fan-in barrier: `wait()` on all story futures before AVFL
- Fix loops: `while not validated: task.submit(fix); validate()` inside a flow
- Human approval gate: `pause_flow_run(wait_for_input=ApprovalRequest)` — human types approval in UI
- Error handling: `@task(retries=3)` decorator; flows can catch exceptions
- Monitoring: built-in Prefect dashboard at localhost:4200

Subprocess invocation is trivial: `subprocess.run(["claude", "-p", ...])` inside a task body. The `ProcessPoolTaskRunner` can run these in true parallel across multiple CPU cores.

The weaknesses: (1) Prefect is data-pipeline-oriented and brings that mental model — concepts like "deployments," "workers," and "work pools" assume recurring batch jobs, not ad-hoc sprint runs; (2) the local server requires a running Prefect server process as a sidecar; (3) human approval requires the Prefect UI to be open in a browser for the reviewer; (4) Prefect's state model is its own — it does not integrate with Beads and would be a parallel source of pipeline truth.

The data-pipeline framing is not a disqualifier but does mean some impedance mismatch when modeling a sprint (not a recurring schedule, not a data ETL). That said, Prefect 3.x explicitly moved toward event-driven flows and supports ad-hoc invocation. It is meaningfully more production-mature and observable than Gas City, but it is also substantially heavier to adopt for a solo developer's local sprint tool.

**Fit verdict: Credible. Technically capable, best HITL primitives of any tool surveyed, strong monitoring. Data-pipeline bias and server-as-sidecar are real adoption costs. Deserves inclusion in shortlist alongside Inngest.**

---

### Dagster

Dagster is a data orchestration platform centered on the **asset** abstraction — you define data assets and their dependencies, and Dagster manages materialization. It is production-grade for data engineering but is explicitly positioned as a data orchestrator, not a general workflow engine.

Dagster's asset model is fundamentally misaligned with Momentum's sprint pipeline. Stories are not data assets. The `sprint/story-A/dev` stage does not "materialize" an asset that `sprint/story-A/review` depends on in the Dagster sense. Forcing that mapping would produce a deeply awkward model. Dagster also requires Dagster Cloud or a self-hosted Dagster server — it is not a lightweight library.

**Fit verdict: Poor. Wrong abstraction (asset-centric data pipeline). Not applicable to sprint orchestration.**

---

### Apache Airflow

Airflow is the oldest and most mature batch workflow scheduler: DAG-based, Python-defined, with a web UI, massive operator ecosystem, and a BashOperator that can run arbitrary shell commands. It has been running production data pipelines for a decade.

Airflow is the wrong tool for Momentum's use case for several reasons. First, it is **schedule-first** — DAGs run on cron-like schedules, and running a DAG ad-hoc feels like an afterthought. Second, Airflow's architecture assumes multiple services (webserver, scheduler, workers, metadata DB, broker) — running it locally for a solo sprint tool is a significant operational burden. Third, Airflow has **no human-in-the-loop primitive** — there is no built-in "pause for human approval" step; practitioners work around this with sensors that poll external state. Fourth, Airflow's DAG model is static — the graph must be defined before execution, which clashes with Momentum's dynamic sprint (number of stories, which ones need fix loops, is determined at runtime).

Airflow's BashOperator could technically invoke `claude -p`, and its DAG model could be extended for sprint shapes. But the setup overhead, missing HITL, and static-DAG constraint make it a poor fit compared to even Prefect, let alone Gas City.

**Fit verdict: Poor. Enterprise batch scheduler, wrong operational model, no HITL primitive, static DAG conflicts with dynamic sprint shape.**

---

### Dagger

Dagger is a programmable software delivery platform — think "CI/CD pipelines as code" with containerized execution. It runs locally or in CI, provides Go/Python/TypeScript/PHP/Java SDKs, and has strong caching (content-addressed, cross-run). It recently added an `LLM` type as a first-class primitive, allowing LLM agent calls to be wired into pipelines alongside container steps.

For Momentum's use case, Dagger has a critical structural mismatch: its execution model is **container-centric**. `WithExec()` runs commands inside containers; the pipeline API chains container operations. Running `claude -p` as a host-native subprocess is not the intended use pattern — Dagger would want to run Claude inside a container, which introduces isolation complexity (Claude Code's filesystem tools, git operations, worktree management all require host-level access that containers complicate).

The LLM primitive is interesting but operates at a different level than what Momentum needs: it lets a Dagger pipeline invoke an LLM to make decisions within the pipeline, not to schedule external Claude sessions. Dagger also has no human approval gate primitive. The "block until human approves" pattern is absent from its model.

That said, Dagger's parallelism and local execution capabilities are genuinely strong, and the caching layer is a differentiator for deterministic steps (though LLM calls and `claude -p` sessions are non-deterministic, so caching would mostly apply to infrastructure setup steps). Dagger is v0.20.8 — actively developed but pre-1.0 in versioning.

**Fit verdict: Poor for this specific use case. Container-centric execution model conflicts with host-native `claude -p` subprocesses. No HITL primitive. Interesting for future exploration if Momentum adds containerized agent sandboxing.**

---

## Other Relevant Tools

### Buildkite

Buildkite is a CI/CD platform with a distributed agent architecture. Pipelines are YAML-defined and run on Buildkite-hosted or self-hosted agents. It has strong parallelism (the `parallelism` attribute), wait steps for fan-in, and block steps for human approval (pause until a team member clicks "Unblock" in the UI or via API).

Buildkite is disqualified on two grounds. First, it **requires the Buildkite SaaS platform** for coordination — self-hosted agents still phone home to Buildkite Cloud for job dispatch and pipeline management. There is no fully self-hosted option without a Buildkite account. For a local-first sprint tool, a mandatory cloud dependency is unacceptable. Second, Buildkite's mental model is CI/CD — pipelines are triggered by git events, run in isolated build environments, and produce build artifacts. The sprint pipeline is not a CI pipeline; it is a coordination protocol for long-running interactive agent sessions.

The block step human approval is the closest to Momentum's requirement of any tool's native primitive — but it requires the Buildkite UI (cloud-hosted) to surface it.

**Fit verdict: Poor. Cloud-dependency is a hard disqualifier. CI/CD mental model is wrong for sprint orchestration.**

---

### Modal

Modal is a cloud-first serverless compute platform — functions run in Modal's cloud infrastructure, with GPU access, auto-scaling, and batch processing. It is **cloud-only** with no local execution mode.

For a local-first, offline-capable sprint pipeline, Modal is immediately disqualified. Every `claude -p` invocation would run in Modal's cloud, not on the local machine with local git worktrees and local Claude Code sessions. The entire architecture depends on local state (git worktrees, `.claude/` configs, local story files).

**Fit verdict: Eliminated. Cloud-only, incompatible with local-first requirement.**

---

### Watchexec / entr / fswatch (Filesystem Watchers)

These are discussed under the "Simplest Path" section below, as they are components of the Beads-alone baseline rather than dispatcher alternatives.

---

## Synthesis

The survey divides cleanly into three groups:

**Group 1 — Wrong abstraction layer (most tools):** AutoGen, CrewAI, SmolAgents, Magentic-One, OpenAI Swarm, Rivet, AgentStack, AgentOps. These tools build, manage, or observe LLM agents — they are not schedulers of external processes. Wrapping `claude -p` in any of them would mean importing a large framework to solve a problem that framework was not designed for. The result would be the same state split-brain that disqualified Hermes: two authoritative lifecycle owners, no clean integration with Beads.

**Group 2 — Wrong deployment model:** Airflow, Dagster (data-pipeline-centric and service-heavy), Buildkite (cloud-required), Modal (cloud-only). These are production-grade tools that solve real problems — none of which are Momentum's problems in the deployment context that matters (solo dev, local machine, local git).

**Group 3 — Credible fits:** Inngest and Prefect. Both are general-purpose Python/TypeScript workflow engines that can schedule arbitrary shell subprocesses, support fan-out/fan-in, have human-in-the-loop primitives, provide local monitoring dashboards, and run without mandatory cloud. Dagger is a borderline case — technically strong but container-centric in a way that conflicts with host-native Claude sessions.

**Cross-cutting tension:** The closer a tool gets to meeting Momentum's requirements, the more it resembles "a running sidecar service plus a web UI." Inngest and Prefect both require a local server process (Inngest Dev Server or Prefect server at localhost:4200). Gas City requires a `gc` binary process. The Claude-native baseline (from the prior dispatcher research) requires a long-lived Agent SDK daemon. There is no zero-infrastructure option among the capable tools — the question is which infrastructure is most appropriate.

**What Inngest has over Gas City:** Durable execution with per-step checkpointing (if a step fails after 30 minutes, you restart from that step, not the beginning). Production-grade retry semantics. A polished monitoring UI. First-class TypeScript/Python ergonomics. These are real advantages for a production sprint pipeline.

**What Gas City has over Inngest:** Native understanding of the Gas Town / Beads ecosystem (designed to work with Beads). Simpler operational model (single `gc` binary vs. Inngest server + app server + function definitions). Closer alignment with the Claude Code native tool call model. An exec-order primitive that is exactly "run a shell command when a condition is met."

**What Prefect has over both:** The strongest human-in-the-loop primitive of any tool surveyed — `pause_flow_run` with typed input forms in a UI is production-grade and well-documented. The ProcessPoolTaskRunner provides true parallel subprocess execution with no framework wrapping needed. It is the most mature and most widely used of the credible tools.

---

## Shortlist

Of all tools surveyed, two deserve full evaluation equivalent to the Temporal/LangGraph/GitHub Actions assessments:

**1. Prefect** — Most technically complete fit for Momentum's requirements. Native subprocess parallelism (ProcessPoolTaskRunner), strong HITL (`pause_flow_run`), self-hosted local server, active maintenance (v3.7.1, weekly releases), and production pedigree. Primary risk: data-pipeline mental model creates impedance mismatch; local server is a real operational dependency.

**2. Inngest** — Second-strongest fit. Durable execution with per-step checkpointing, native fan-out/fan-in via parallel steps, event-driven human gates (`waitForEvent`), local Dev Server with dashboard. Primary risk: Server Side Public License (soft lock-in); callback-based architecture requires standing up an HTTP endpoint that Inngest calls back into; less mature than Prefect (5.4k stars vs. 22.4k).

**Not shortlisted but worth watching:** Dagger — interesting because it is actively integrating LLM agents as first-class primitives (the `LLM` type), is local-first, and has strong caching. Its container-centric execution model currently conflicts with host-native Claude sessions. If Momentum ever moves toward containerized agent sandboxing, Dagger becomes a stronger candidate.

---

## Simplest Path: Beads Alone with Shell Scripts and a Filesystem Watcher

### What It Would Look Like

The Beads-alone approach uses Beads as the story state store and a minimal shell wrapper — triggered by a filesystem watcher — as the dispatcher. The architecture is:

1. **State store:** Beads (or `index.json` without Beads) tracks story status: `todo → ready → in_progress → review → merged`.
2. **Trigger mechanism:** `watchexec` (or `entr`) watches a queue file (e.g., `intake-queue.jsonl` or a Beads cursor). When the file changes (a story enters `ready` state), the watcher fires a shell script.
3. **Dispatcher script:** A bash script (`dispatch.sh`) reads the queue, finds stories in `ready` state, and for each launches `claude -p "..."` as a background subprocess in a git worktree. It writes the PID to a tracking file.
4. **Convergence:** The script polls subprocess exit codes. On success, it updates story state to `merged` and fires the next stage. On failure, it retries up to N times (a simple counter in a file).
5. **Fan-in barrier:** After all story PIDs have exited, the script fires the AVFL corpus pass.
6. **Human gate:** The script writes a `PENDING_APPROVAL` sentinel file and blocks (or exits). The developer reads the output, types a command to approve or reject, which removes the sentinel and re-runs the final push step.
7. **Monitoring:** `tail -f dispatch.log` plus the Beads dashboard (if using Beads) or a simple `jq` query on `index.json`.

### What It Costs

- **Implementation time:** 1–2 days for a working prototype; 1–2 weeks for robust error handling and the full pipeline shape.
- **Infrastructure:** Zero. No server processes, no databases beyond what Beads already uses, no network dependencies.
- **Operational overhead:** Zero marginal overhead — it is just shell scripts and a watcher, both of which are already running on the developer's machine.
- **Maintenance:** High per-feature cost. Every new requirement (fan-in logic, retry counting, AVFL integration, human gate UX) requires custom shell code.

### What It Lacks Compared to Gas City

| Capability | Beads+Shell | Gas City |
|---|---|---|
| Durable execution (crash recovery) | No — if the dispatcher script dies, all state is lost | Partial — Gas City can restart from Beads state |
| Per-step checkpointing | No — restart means re-running from the beginning | No (same limitation) |
| Human approval UI | Terminal stdin + sentinel file | Not documented — likely same |
| Monitoring dashboard | None native (tail logs) | None documented (CLI only) |
| Convergence loop logic | Custom per loop | Exec orders with condition triggers |
| Parallelism management | `&` + PID tracking in shell | Worker pool with configurable concurrency |
| Error surfacing | Exit codes + log parsing | Exec order failure callbacks |
| Integration with Beads | Direct (reads/writes same files) | Designed (native) |

### Honest Assessment

The Beads-alone approach is viable for a small sprint (2–3 stories) where the developer is watching the terminal. It becomes fragile as sprint size grows, as fix loops add nesting, and as the need for reliable fan-in semantics grows. The prior dispatcher research (docs/research/claude-code-background-dispatcher-2026-05-17.md) concluded exactly this: the shell+watcher pattern works but the "12 second per-process spawn cost, PID management, and self-trigger loop guards" compound into maintenance burden at scale. CONFIRMED from prior corpus.

The key insight from that prior research is: **the shell dispatcher is not "no dispatcher" — it is "a dispatcher you build yourself."** Every capability in Gas City's exec-order system, Prefect's task runner, or Inngest's durable functions could be hand-coded in bash. The question is whether the maintenance cost of that custom code exceeds the adoption cost of a purpose-built tool.

For a proof of concept or a 2-story sprint, Beads+shell is the right choice — it eliminates all adoption risk and produces a working pipeline faster. For a 6–8 story sprint with AVFL loops, E2E validation, human review cycles, and fix passes, the custom dispatcher grows to the point where it becomes the main engineering burden of the sprint toolchain. At that scale, Gas City's exec-order model or Prefect's task-runner approach saves net effort.

**The specific gap where Beads+shell fails hardest:** the fix loop. A convergence loop that runs `validate → fix → re-validate` up to N times, where each step is a 10–30 minute Claude session, requires tracking loop state across subprocess exits. In shell, this is a while loop with a counter file and careful exit-code handling. It works — but when it fails (and it will: a subprocess hangs, a filesystem event is missed, the watcher process itself crashes), debugging it requires reading raw process tables and log files. Gas City's condition trigger, or Prefect's retry decorator, fails loudly and tells you exactly which step failed and why.

**Recommendation on Simplest Path:** Use Beads+shell for the first sprint after Beads adoption (DEC-028 dual-write is not yet resolved, so this is the right scope anyway). Instrument it deliberately — capture what breaks, what requires manual intervention, and which pipeline steps need the most iteration. Use that data to make a grounded decision between Gas City, Prefect, and the Beads+shell approach for the long term. Do not prematurely adopt a heavier tool when the simpler approach will generate the operational evidence needed to choose well.

---

## Open Questions

- **Prefect HITL UX in practice:** Prefect's `pause_flow_run` with typed input forms sounds compelling on paper, but what does the developer experience actually look like for a solo developer approving a sprint merge? Does the Prefect UI make this easier than reading a terminal + typing a command? Warrants a 1-hour hands-on evaluation.

- **Inngest callback architecture fit:** Inngest requires an HTTP endpoint that its runner calls back into to execute function steps. For a local sprint pipeline, this means the Momentum dispatcher must be a running web server on the developer's machine. How does this interact with the developer starting/stopping sessions? Is the callback model a fundamental impedance mismatch for an interactive, session-scoped tool?

- **Prefect vs. Gas City decision point:** The prior Gas City evaluation recommends a 3–4 week proof of concept. If that PoC is authorized, what would a 1-week Prefect parallel spike look like? The comparison data would be: (a) how much code do you write for the sprint pipeline shape? (b) how natural is the `claude -p` subprocess integration? (c) what breaks first in a real sprint?

- **Dagger LLM primitive trajectory:** Dagger's `LLM` type and `Env` primitive suggest the team is moving toward first-class agentic pipeline support. If they add host-native (non-containerized) subprocess coordination, Dagger becomes a much stronger candidate. Worth monitoring their roadmap.

- **Watchexec vs. Gas City exec orders for the simple case:** For a 2-story sprint, is a watchexec-triggered shell script materially worse than a Gas City exec-order trigger? The answer is probably no for small sprints and yes for large ones — but the crossover threshold is unknown without empirical data.
