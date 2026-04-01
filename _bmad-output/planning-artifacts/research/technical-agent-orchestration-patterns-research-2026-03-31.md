---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ["docs/research/LLM Agent Orchestration Patterns Research.md"]
workflowType: 'research'
lastStep: 4
research_type: 'technical'
research_topic: 'agent orchestration patterns for LLM multi-agent systems'
research_goals: 'Survey orchestration patterns beyond DAG and Swarms, understand empirical evidence for what works, identify platform-specific constraints for Claude Code vs Cursor, survey the framework landscape, produce clear recommendations for and against specific patterns — current state March 2026'
user_name: 'Steve'
date: '2026-03-31'
web_research_enabled: true
source_verification: true
---

# Research Report: Agent Orchestration Patterns for LLM Multi-Agent Systems (Claude Code & Cursor) — March 2026

**Date:** 2026-03-31
**Research Type:** Technical (Multi-Agent Research Team)

---

## Technical Research Scope Confirmation

**Research Topic:** Agent Orchestration Patterns for LLM Multi-Agent Systems (Claude Code & Cursor)
**Research Goals:** Survey orchestration patterns beyond DAG and Swarms; understand empirical evidence for what works; identify platform-specific constraints for Claude Code vs Cursor; produce clear recommendations for and against — current state March 2026.

**Technical Research Scope:**

- Architecture Analysis — orchestration patterns (hierarchical, sequential, router, reflection, plan-and-execute, ReAct, LATS, actor-critic, blackboard, event-driven)
- Implementation Approaches — what patterns work within Claude Code and Cursor natively; failure modes; scale limits
- Platform Constraints — Claude Code native capabilities vs. Cursor native capabilities; where they diverge
- Performance Considerations — token overhead, reliability, benchmark evidence
- Recommendations — explicit FOR and AGAINST lists, conditional guidance, platform-specific caveats

**Out of Scope:** Python library selection or external orchestration frameworks, unless found to be genuinely the only viable path for a specific pattern.

**Research Methodology:**

- Live web search with rigorous source verification
- Community consensus vs. peer-reviewed evidence clearly distinguished
- Confidence levels flagged where evidence is thin or conflicting
- All claims targeted at March 2026 currency

**Scope Confirmed:** 2026-03-31

## Research Overview

**Status:** Gemini primary research integrated; follow-up responses received and incorporated; AVFL pass 1 complete.

**Sources:** 4 parallel research subagents (web search, official docs, practitioner reports, peer-reviewed papers); Gemini Deep Research integrated.

**Research Date:** March 31, 2026

**Methodology:**
- Live web search with source verification
- Peer-reviewed evidence distinguished from practitioner consensus
- Platform-specific claims verified against official documentation
- Confidence levels applied where evidence conflicts

---

## Part 1: The Pattern Landscape

### 1.1 Why DAGs Fail for LLM Orchestration

DAG-based orchestration originated in deterministic workflow automation (Apache Airflow, Luigi, Prefect). The core assumption — that steps are predictable, stateless, and composable — breaks down with LLMs.

**Four root causes of DAG failure with LLMs:**

1. **No working memory separate from context window.** LLMs have no persistent state between DAG nodes beyond what is explicitly passed. Context continuity is an illusion — each node re-reads a serialized artifact.
2. **Greedy step-wise reasoning.** DAG execution cannot propagate downstream value backward. A node that makes a locally reasonable decision cannot know it forecloses better paths downstream.
3. **39–70% multi-turn performance degradation on strictly sequential tasks** (DeepMind, arXiv 2512.08296 — multi-agent coordination fragments reasoning chains; degradation scales with hop count). Each hop introduces context truncation, prompt reinterpretation, and drift.
4. **Acyclicity prohibits feedback loops.** Retry, self-correction, and reflection are structurally impossible in a pure DAG — the graph cannot revisit a node.

**The one context where DAGs work:** When a deterministic engine executes the DAG and LLMs are only the compute nodes (not the coordinators), DAG delivers genuine efficiency gains. LLMCompiler (ICML 2024) achieved 1.8–3.74× efficiency gains this way. Flash-Searcher reached 82.5% on GAIA using this approach. The lesson: DAGs as execution scaffolding for LLM tasks = valid. DAGs as the orchestration model = not valid.

_Source: arXiv 2512.08296 (Google, 180-config study); LLMCompiler ICML 2024; practitioner consensus 2025–2026._
_Confidence: HIGH (peer-reviewed + practitioner convergence)_

---

### 1.2 Why Swarms Fail for LLM Orchestration

Swarms — peer-to-peer agent networks with emergent coordination, no central authority — are theoretically appealing and empirically disastrous.

**The numbers:**
- **17.2× error amplification** from flat "bag-of-agents" topologies vs. single-agent baseline (Google DeepMind, 180-configuration study, arXiv 2512.08296)
- **Reliability multiplication failure:** 5 agents at 95% individual reliability each = 77% system reliability. At 10 agents, 60%. Swarms don't add reliability — they multiply fragility.
- **Gartner (June 2025) projects more than 40% of enterprise agentic AI projects will be canceled by end of 2027** — attributed primarily to compute costs, unpredictable latency, and state management complexity (not model capability)
- **10× performance drop** from isolated task benchmarks (SWE-bench 70.4% — single-agent baseline; cf. §3.1 for orchestrated 80.9%) to integrated real-world multi-agent work (ACE-Bench 7.5%)
- **<10% enterprise scaling success rate** for swarm-style architectures

**Why the OpenAI Swarms library is an outlier:** It is a teaching tool and framework demo, not a production pattern recommendation. The name has unfortunately anchored the term "swarm" as a legitimate orchestration pattern in public discourse.

**When swarms show any promise:** Massive parallelism of genuinely independent, identical tasks (e.g., 1,000 document classifications in parallel). Even here, a supervisor-coordinated wave pattern outperforms on cost and error rate.

_Source: arXiv 2512.08296; The New Stack 2025; ACE-Bench evaluation 2025–2026._
_Confidence: HIGH (peer-reviewed)_

---

### 1.3 The 11 Orchestration Patterns

Evidence codes: `[PEER]` = peer-reviewed paper; `[PRAC]` = practitioner consensus/production report.

---

#### Pattern 1: Sequential Pipeline
**Structure:** Agent A → Agent B → Agent C. Linear handoff with explicit context passing at each boundary.

**Strengths:** Predictable, debuggable, lowest coordination overhead, best cost resilience at high volume. F1 0.903 on financial document processing at >25K docs/day, $0.187/doc. `[PEER arXiv 2603.25620]` (PICon multi-agent framework, financial document processing benchmark.)

**Failure modes:** Cannot parallelize; latency scales linearly with chain length; a single weak step poisons all downstream outputs.

**Scale limits:** Unlimited in theory. Practical degradation after ~6 sequential hops due to context drift.

**Token overhead:** 1× baseline (lowest of all patterns).

**Best for:** Deterministic pipelines, data transformation, document processing, code generation → test → fix loops.

**Platform notes:** Supported natively in both Claude Code and Cursor. Claude Code: skill-to-skill handoff via `claude -p`. Cursor: sequential Agent passes.

---

#### Pattern 2: Parallel Fan-Out (Wave)
**Structure:** Orchestrator decomposes task → dispatches N independent subtasks simultaneously → waits for all → synthesizes results.

**Strengths:** 45% latency reduction vs. sequential for parallelizable tasks. F1 0.914. Synchronous wave execution — parallel agents dispatched in batches, waiting for each batch to complete before proceeding — is the practitioner-preferred pattern for reliable orchestration. `[PRAC]` The Google DeepMind study independently validates batch coordination over unstructured parallel dispatch. `[PEER arXiv 2512.08296]`

**Failure modes:** Synthesis ("reduce") step is the hardest part and most failure-prone. Agents must write to distinct output files — shared mutable state causes silent corruption. Results arrive at different times, requiring a reconciliation agent.

**Scale limits:** 3–5 concurrent agents (practical sweet spot across both Claude Code and Cursor). Beyond 7, reasoning capacity per agent becomes too thin. Beyond ~12 (Claude Code), system resource exhaustion risk.

**Token overhead:** 4× chat baseline.

**Best for:** Research tasks with distinct domains, parallel implementation of independent features, competitive hypothesis testing.

**Platform notes:** Claude Code: `isolation: worktree` with parallel subagents. Cursor: parallel worktree agents (8 concurrent, Cursor 2.0). See §2 for scale limits.

---

#### Pattern 3: Hierarchical Supervisor-Worker
**Structure:** Orchestrator agent decomposes task → spawns specialist worker agents → workers report back → orchestrator synthesizes.

**Strengths:** Best production cost-accuracy tradeoff. Achieves 98.5% of the accuracy achieved by the Reflection/Self-Critique pattern (Pattern 7, F1 0.943) — hereafter 'reflexive baseline' (Pattern 7 in this report; distinct from Reflexion, the Shinn et al. 2023 language-feedback technique) — at 60.7% of cost. `[PEER arXiv 2603.22651]` Centralized coordination reduces error amplification from 17.2× (flat) to 4.4×. `[PEER arXiv 2512.08296]`

**Failure modes:** Orchestrator is a single point of failure. Orchestrator context saturates as worker results accumulate — the orchestrator must actively compress. No nesting supported natively in Claude Code or Cursor (subagents cannot spawn subagents).

**Scale limits:** 3–5 workers is the validated sweet spot. Beyond 7 workers, orchestrator context management becomes the bottleneck.

**Token overhead:** 3–4× chat baseline (scales with worker count).

**Best for:** Complex multi-domain tasks, research synthesis, large refactors with independent modules.

**Platform notes:** Claude Code supports this via Agent Teams (experimental) or parent/subagent delegation. Cursor supports one level of delegation (coordinator → subagents) but subagents cannot further delegate.

**Platform constraint:** Both Claude Code and Cursor limit this to ONE level of delegation (subagents cannot spawn subagents). For tasks requiring deeper decomposition: flatten into a sequential series of hierarchical stages, or use Plan-and-Execute where the planner handles intermediate coordination that would otherwise require nesting.

---

#### Pattern 4: Router / Dispatcher
**Structure:** A classifier/router agent receives input → selects the appropriate specialist agent → routes the task.

**Strengths:** One LLM call overhead for routing. Scales to ~20 specialist agents. Google ADK AutoFlow uses this pattern. Isolates specialist context — each expert only sees relevant input. `[PRAC]`

**Failure modes:** Router errors are silent and hard to detect. Ambiguous inputs route to the wrong specialist. No feedback from specialist to improve routing.

**Scale limits:** Router itself is effectively unlimited. Specialist pool can be large; practical limit is documentation/maintenance.

**Token overhead:** 1.5–2× baseline.

**Best for:** Tasks with clearly distinct subtypes (code vs. docs vs. research); customer support routing; modular skill dispatch.

**Platform notes:** Natively implementable in both platforms as a supervisor subagent that routes tasks. Claude Code: orchestrator-as-main-agent pattern. Cursor: Background Agent routing.

---

#### Pattern 5: ReAct (Reasoning + Acting)
**Structure:** Single agent loops: [Reason] → [Act (tool call)] → [Observe result] → [Reason] → repeat until done.

**Strengths:** 2.5% higher reliability than Reflexion (Shinn et al. 2023, a specific language feedback loop method, distinct from Pattern 7 Reflection/Self-Critique) under stress. 80.9% fault recovery rate. Adaptive — responds to observations, not pre-planned steps. `[PEER arXiv 2601.06112]`

**Failure modes:** Can loop indefinitely without progress (requires hard `maxTurns` limit). Context window fills with observation history. Prone to "getting stuck" on failed tool calls.

**Scale limits:** Single-agent pattern — scale by running multiple ReAct agents as workers under a hierarchical coordinator.

**Token overhead:** 2–3× baseline (loops multiply tokens).

**Best for:** Interactive tasks requiring tool use and adaptation (web research, code debugging, API integration).

**Platform notes:** Both Claude Code and Cursor support ReAct natively — it is the default execution loop for any agent using tool calls. Requires explicit `maxTurns` limit in Claude Code subagent frontmatter to prevent infinite loops.

---

#### Pattern 6: Plan-and-Execute
**Structure:** Planner agent produces a structured plan → separate Executor agent(s) carry out steps.

**Strengths:** 92% task completion vs. 85% for ReAct. 3.6× speedup over sequential ReAct. Plan is auditable and correctable before execution begins. `[PEER]` Wang et al. (2023); consistently replicated in financial and data processing pipelines `[PEER arXiv 2603.22651]`

**Failure modes:** Plan quality gates everything — a bad plan produces bad execution. Plans go stale when real-world conditions change mid-execution. Planner and executor may disagree on implicit assumptions.

**Scale limits:** Planner is single-agent; executors can be parallelized (becomes hybrid with fan-out).

**Token overhead:** 2–4× baseline.

**Best for:** Long-horizon structured work (story implementation, multi-step migrations, complex refactors).

**Platform notes:** Claude Code's `momentum-dev` skill uses this pattern. Cursor's Plan Mode (`Shift+Tab`) implements the planner half.

---

#### Pattern 7: Reflection / Self-Critique
**Structure:** Generator agent produces output → Critic agent evaluates → Generator revises → repeat until quality threshold or max iterations.

**Strengths:** Highest F1 in cross-pattern comparison (0.943); separate SEC filing configuration from same study achieves F1 0.985. Cross-pattern comparison: Hierarchical reaches F1 ≈0.929 (98.5% of Reflection's cross-pattern F1 of 0.943). Breaks implementation bias — fresh context re-reading catches errors the generator missed. `[PEER arXiv 2603.22651]`

**Failure modes:** Highest cost ($0.430/doc). Degrades above ~25K operations/day. Critic and generator can enter agreement loops without genuine improvement. Hard to know when to stop.

**Scale limits:** 2–3 iteration cycles; beyond that, marginal improvement rarely justifies cost.

**Token overhead:** 5–8× baseline.

**Best for:** Accuracy-critical, low-volume work: code review, document validation, security analysis.

**Platform notes:** Writer/Reviewer separation in Claude Code (separate sessions to avoid implementation bias) is this pattern in practice.

---

#### Pattern 8: LATS (Language Agent Tree Search)
**Structure:** MCTS-style tree search over agent action space. Agent generates multiple candidate actions → evaluates each → expands the most promising → backtracks on failure.

**Strengths:** 92.7% HumanEval pass@1 (GPT-4, ICML 2024) — ceiling performance on coding benchmarks (source: Gemini Deep Research; subagent research found 94.4% in alternate configuration). Systematic exploration prevents local optima. `[PEER ICML 2024]`

**Failure modes:** Very high token cost (MCTS exploration is multiplicative). Impractical for time-sensitive tasks. Requires a reliable value function to evaluate candidate steps.

**Scale limits:** Practical only for bounded problem spaces. Unbounded LATS is financially prohibitive.

**Token overhead:** 10–20× baseline.

**Best for:** Maximum-accuracy coding tasks where cost is not constrained. Not suited for IDE daily use.

**Platform notes:** Not natively supported by either Claude Code or Cursor — LATS requires MCTS scaffolding not available in standard agent hooks. Consider Plan-and-Execute (Pattern 6) as an alternative for code generation tasks.

---

#### Pattern 9: Actor-Critic
**Structure:** Actor agent proposes actions; Critic agent evaluates and challenges; Actor revises under critique.

**Strengths:** Adversarial critique breaks confirmation bias. Statistically more reliable than single-agent output for complex reasoning. `[PEER arXiv 2603.22651; Shinn et al. 2023 (Reflexion)]`

**Failure modes:** ~2× token cost per cycle vs. ReAct. Critics can be sycophantic (agree with actor). Requires careful critic prompt design to maintain genuine adversarialism.

**Token overhead:** 4–6× baseline.

**Best for:** High-stakes decisions, architecture planning, security analysis, anywhere bias in a single agent is a concern.

**Platform notes:** Implement as two-session Writer/Reviewer separation in Claude Code (avoids implementation bias from same-context review). Cursor: use two-pass protocol (generate pass then fresh verify pass).

---

#### Pattern 10: Blackboard / Shared Memory
**Structure:** Agents read from and write to a shared knowledge structure (the "blackboard"). No direct agent-to-agent communication — all coordination is mediated through shared state.

**Strengths:** 13–57% improvement over strong baselines. 72% token reduction vs. AFlow (automated agent workflow). Handles heterogeneous agents with unknown capabilities well. `[PEER arXiv 2510.01285]`

**Failure modes:** Write conflicts if not carefully managed (unique write keys required). Shared state becomes incoherent if agents overwrite each other's contributions.

**Scale limits:** File-system-based blackboard (each agent writes distinct files) scales well. In-memory shared state does not.

**Token overhead:** 2–3× baseline.

**Best for:** Teams of heterogeneous specialists contributing to a shared artifact (documentation, architecture design, research synthesis).

**Platform notes:** Claude Code's filesystem is effectively a blackboard. Skills like `momentum-dev` use this implicitly when agents write to distinct output files.

---

#### Pattern 11: Event-Driven / Pub-Sub
**Structure:** Agents subscribe to event streams. Events trigger agent activation. Agents publish results as new events.

**Strengths:** Horizontal scale ceiling. Sub-millisecond dispatch with Redis Streams. Inference latency (not orchestration) becomes the bottleneck at scale. `[PRAC/PEER]`

**Failure modes:** Debugging is hard — causal chains are non-linear. Event storms can cascade. Requires infrastructure (message broker) beyond what Claude Code / Cursor natively provide.

**Scale limits:** Infrastructure-bound, not agent-bound.

**Token overhead:** 1–2× baseline (low coordination overhead).

**Best for:** Real-time integration (CI/CD triggers, monitoring, Slack/Linear automations). Cursor's Automations feature implements a limited version of this pattern.

**Platform notes:** Cursor Automations (GitHub, Slack, Linear, PagerDuty triggers) implement a limited version of this pattern. Claude Code hooks (`PreToolUse`, `PostToolUse`) provide tool-level event triggers. Full pub-sub requires external infrastructure (Redis Streams, Kafka) beyond either platform's native capability.

---

## Part 2: Platform Capabilities and Constraints

### 2.1 Claude Code — Native Orchestration

**Agent primitives:**

| Primitive | Status | Key Properties |
|---|---|---|
| Subagents (`.claude/agents/`) | Stable | Isolated 200K context (standard subagents); 1M token context for Agent Teams (Opus 4.6); `isolation: worktree` available; no nesting |
| Agent Teams | Experimental | Lead + teammates; shared task list; async mailbox; no session resume |
| Git Worktree Isolation | Stable | `--worktree` flag; auto-cleaned if no changes; `/batch` skill uses this |
| Hooks (stable) | Stable | `PreToolUse`, `PostToolUse` — standard hook events |
| Hooks (experimental) | Experimental (Agent Teams) | `SubagentStart`, `SubagentStop`, `TeammateIdle` — verify against current docs; Agent Teams feature |
| Skills / SKILL.md | Stable | Context injection; not subagents; callable as tools |

**Concurrent agent limits:**

| Workload | Safe Concurrent Count |
|---|---|
| Light (file ops, git) | 5–6 |
| Medium (builds, linting) | 3–4 |
| Heavy (large file processing) | 2 |
| Official documented cap | 10 (with queuing) |
| Practical degradation threshold | ~10–12 |
| System instability risk | ~20+ |

_Note: Anthropic closed a feature request for `maxParallelAgents` without response (March 2026)._

**What works in Claude Code:**
- Hierarchical coordinator → specialist subagents (one level only — no nesting)
- Fan-out via CLI loop (`claude -p` in bash) for 1,000+ file batch operations
- Worktree-isolated parallel implementation (prevents file-write conflicts)
- Sequential chaining (pipeline) via skill-to-skill handoff
- Writer/Reviewer separation (distinct sessions — avoids implementation bias)
- Agent Teams for multi-domain research synthesis
- Competitive hypothesis testing (multiple agents with opposing theories)

**What fails or degrades in Claude Code:**
- Recursive nesting (subagents spawning subagents) — explicitly unsupported
- Same-file concurrent edits in standard subagent mode (no file-level locking; use worktree isolation). Agent Teams uses strict file-locking, which prevents corruption but causes lock-contention when multiple teammates edit the same file.
- Spawning 20+ agents (no throttling; system instability documented)
- Context window saturation: degradation begins at ~60% utilization; "lost in the middle" measurable below 50%
- Session resumption with Agent Teams (`/resume` doesn't restore teammates)
- Agent Teams on non-tmux terminals (VS Code integrated terminal, Windows Terminal, Ghostty not supported for split panes)
- Bloated CLAUDE.md / skill files (keep under 2,000–3,000 tokens; bloat causes attention dilution)

_Sources: code.claude.com/docs/en/sub-agents; code.claude.com/docs/en/agent-teams; GitHub Issue #15487 (Dec 2025); Shipyard.build; Zach Wills; Addy Osmani._

---

### 2.2 Cursor — Native Orchestration

**Agent primitives:**

| Primitive | Status | Key Properties |
|---|---|---|
| Agent Mode | Stable | Full autonomous coding, tool use, terminal exec |
| Background / Cloud Agents | Stable (Pro+) | Isolated Ubuntu VMs; triggered by Automations |
| Parallel Agents (Worktrees) | Stable | Git worktree isolation; no LSP in worktrees |
| Subagents (`.cursor/agents/`) | Stable | Isolated context windows; cannot spawn subagents |
| Hooks (`.cursor/hooks.json`) | Stable | Autonomous iteration loops until success criteria |
| Automations | Stable | Event-driven triggers: cron, GitHub, Slack, Linear, PagerDuty |
| Plan Mode | Stable (buggy) | `Shift+Tab`; known bug: agents stuck in plan mode waste tokens |

**Concurrent agent limits:**

| Limit Type | Value |
|---|---|
| Parallel agents (Cursor 2.0, Oct 2025) | **8 worktree cap (Cursor 2.0, Oct 2025); ~4 practical on laptop hardware (LSP/thermal limits)** |
| Workspace worktree hard cap | 20 (oldest auto-removed) |
| Practical thermal limit (laptops) | ~4 |
| MCP tools per workspace | 40 (hard cap) |

**What works in Cursor:**
- Parallel fan-out (worktrees) for independent tasks on separate branches
- One level of hierarchical delegation (coordinator → subagents)
- Two-pass protocol (generate then verify in separate passes with fresh context)
- Autonomous loops via `hooks.json` (iterate until tests pass)
- Event-driven Automations (Background Agents triggered by external events)
- Best-of-N model comparison (same prompt → multiple models simultaneously)
- Real-time visual diff review at each agent step

**What fails or degrades in Cursor:**
- Recursive multi-agent pipelines (subagents cannot spawn subagents — architectural constraint)
- Cross-agent context sharing (isolated context windows; no direct communication channel)
- LSP/linting inside worktrees (no LSP support in parallel agent worktrees)
- Programmatic orchestration (Cursor is UI-first; no CLI scripting of agent lifecycle)
- CI/CD integration (possible via Automations webhooks but IDE-first architecture)
- Plan mode reliability (confirmed bug: agents stuck in plan mode waste context)
- Context window: advertised 200K, practical 70K–120K after internal truncation

_Sources: cursor.com/docs/configuration/worktrees; cursor.com/blog/2-0; cursor.com/blog/agent-best-practices; forum.cursor.com/t/better-multi-agent-orchestration/151730; vibecoding.app/blog/cursor-problems-2026._

---

### 2.3 Cross-Platform Comparison

| Dimension | Claude Code | Cursor |
|---|---|---|
| **Architecture model** | Distributed systems (programmatic) | Interactive development (UI-mediated) |
| **Max concurrent agents** | ~10 safe / ~20 instability threshold | 8 parallel (20 worktree cap) |
| **Subagent nesting** | Not supported | Not supported |
| **Cross-agent communication** | File-based (filesystem as blackboard) | File-based only (no direct channels) |
| **Context sharing** | Configurable context passing | Isolated — no parent context access |
| **Worktree isolation** | `isolation: worktree` in frontmatter | Native (all parallel agents in worktrees) |
| **LSP in parallel agents** | Full toolchain available | No LSP in worktrees |
| **Programmatic orchestration** | Full (scripts, CI, hooks, SDK) | Limited (Automations webhooks only) |
| **CI/CD integration** | Native CLI | IDE-first; webhook bridge required |
| **MCP tool limit** | No documented hard cap | 40-tool hard cap |
| **Event-driven triggers** | Hooks (tool-level events) | Automations (GitHub, Slack, Linear, cron) |
| **Visual diff review** | No | Yes (IDE-native) |
| **Plan mode** | EnterPlanMode skill | Shift+Tab (buggy) |
| **Session resumption** | Partial (no teammate restore) | Limited |
| **Best-of-N comparison** | Manual | Native (same prompt → multiple models) |

**Patterns exclusive to Claude Code:**
- Fully autonomous multi-step pipelines (CLI-scriptable `claude -p` chaining)
- CI/CD-triggered parallel agent batches
- Programmatic orchestration via Agent SDK
- Multi-directory cross-repo access (`--add-dir`)
- Per-subagent MCP configuration
- Agent Teams (experimental multi-agent coordination)

**Patterns exclusive to Cursor:**
- Real-time visual diff review at each agent step
- Best-of-N model comparison with visual side-by-side
- BugBot PR automation (35% autofix merge rate)
- Event-driven Automations (Linear, Slack, PagerDuty triggers)
- IDE-integrated plan mode

**Patterns that work in both:**
- Parallel fan-out for independent tasks (worktrees in Cursor; isolation: worktree + subagents in Claude Code)
- MCP tool integration
- Rules / context files
- Sequential pipeline (skill chaining)
- Hooks for autonomous iteration loops
- Hierarchical delegation (one level only)
- Blackboard via filesystem (distinct output files per agent)

---

## Part 3: Empirical Evidence

### 3.1 Key Benchmark Results (March 2026)

| Benchmark | Best Result | System | Notes |
|---|---|---|---|
| SWE-bench Verified | 80.9% | Claude Code (Opus 4.5 via Tier 1 local orchestration) | Orchestrated Claude Code — scaffolding adds ~17 points vs. same model in competing harness. (Opus 4.5 is the version used in this benchmark; Agent Teams now runs on Opus 4.6 — sequential model releases; benchmark predates 4.6 availability.) |
| SWE-bench Verified | 75.8% | Gemini 3 Flash | — |
| HumanEval pass@1 | 92.7% | LATS (GPT-4) | Very high token cost; alt. config: 94.4% |
| GAIA | 75% | H2O.ai | Multi-agent research pipeline |
| WebArena | 54.8% | Gemini 2.5 Pro | Cross-page long-horizon: effectively unsolved |
| OSWorld | 60.76% | CoAct (computer-use + coding) | Actor-Critic combining visual actions with coding verification |
| AgentBench | 41–86.7% failure | SOTA open-source | High failure rates even at frontier |
| Financial docs (SEC filings) | F1 0.985 (reflection, SEC filing config) | arXiv 2603.22651 | Highest F1 in study; Hierarchical achieves F1 ≈0.929 at 60.7% of Reflection's cost |

**Critical finding:** The 80.9% SWE-bench result is an *orchestrated* result — the same model scores ~17 points lower in competing agent harnesses. Orchestration quality matters more than raw model capability. The correct takeaway: prove your orchestration adds value before scaling to many agents, not that single-agent equals multi-agent.

### 3.2 Google's 180-Configuration Study (arXiv 2512.08296)

The most comprehensive empirical study of multi-agent orchestration patterns to date. Key findings:

- Multi-agent with centralized coordination **outperforms flat topologies by 3.9×** on decomposable tasks (17.2× error rate drops to 4.4× with a coordinator)
- Multi-agent **degrades by 39–70%** on sequential planning tasks
- A 20-parameter model predicts optimal architecture for **87% of unseen configurations**
- **17.2× error amplification** from flat topologies vs. **4.4× with centralized coordination**
- Hierarchical supervisor-worker achieves best cost-accuracy Pareto position

### 3.3 MAST Taxonomy (Cemri et al. 2025, ICLR 2025)

Cemri et al. 2025. Two datasets: 150 traces used to derive and validate 14 failure modes; 1,642 traces (MAST-Data) used to calculate failure rate distributions. Same taxonomy, different analysis corpora. Documented failure modes in 3 categories:

1. **Specification/design flaws** — ambiguous task decomposition, unclear agent boundaries
2. **Inter-agent misalignment** — context drift, assumption mismatch between agents
3. **Task verification failures** — no ground truth, inability to detect silent errors

"Silent drift" — errors that compound invisibly across agent hops — is the most dangerous production failure mode. Structural solutions (hard boundaries, reconciliation agents, verification steps) substantially outperform prompt-level mitigations, which address symptoms rather than root causes.

### 3.4 Anthropic Internal Production Findings

- Dynamic agent scaling: 1–4 agents for simple tasks, 10+ for complex research (community-extrapolated from Anthropic's 'Building effective agents' guide; not formally published as internal benchmarks) `[PRAC]`
- Wave execution (synchronous parallel batches) chosen over async DAGs for reliability (community-extrapolated from Anthropic's 'Building effective agents' guide; not formally published as internal benchmarks) `[PRAC]`
- 90.2% performance improvement over single-agent Opus 4 for complex research tasks `[CONF — Anthropic blog, June 2025; not independently verified against primary sources]`
- Token cost reality: 3.2–4.2× (Agent Teams, per Claude Code telemetry) vs. chat baseline
- **Model quality upgrade beats doubling token budget** — better model > more agents
- External memory for orchestrator state persistence is mandatory at scale

---

## Part 4: Recommendations

**When to escalate from single-agent to multi-agent:** A task is a candidate when it meets at least two of: (1) requires distinct domain expertise that cannot fit in one context window; (2) contains parallelizable subtasks with no shared state; (3) single-agent attempts fail due to context saturation, not reasoning quality; (4) requires adversarial verification (security, compliance, accuracy-critical work). If failure is due to reasoning quality, upgrade the model before adding agents.

### 4.1 Recommend FOR

**✅ Hierarchical Supervisor-Worker**
Best production workhorse. Centralized coordination, best cost-accuracy tradeoff (98.5% of reflexive F1 at 60.7% cost). Use when: complex multi-domain tasks, 3–5 distinct specializations needed. Caveat: orchestrator context management is the failure point — budget aggressively for synthesis.

**✅ Sequential Pipeline**
Use as the default starting point. Lowest overhead, most debuggable, best cost at scale. Only add complexity when sequential provably insufficient.

**✅ Parallel Fan-Out / Wave (with reconciliation agent)**
45% latency reduction for genuinely parallelizable tasks. MUST include: (1) worktree isolation to prevent file conflicts, (2) distinct output files per agent, (3) dedicated reconciliation/synthesis step. Limit to 3–5 concurrent agents.

**✅ Plan-and-Execute**
92% task completion rate. Ideal for long-horizon work where the plan is auditable before execution. Use Cursor's Plan Mode or Claude Code's EnterPlanMode skill for the planner half. (Note: Cursor Plan Mode has a known token-waste bug in some configurations — see §2.2. Prefer `claude -p` for the planner if reproducible in your environment.)

**✅ Reflection / Self-Critique (Writer + Reviewer)**
Highest accuracy when cost is not the constraint. Implement as two separate sessions (not same agent reviewing own output) to avoid implementation bias. Hard limit: 2–3 critique cycles max.

**✅ ReAct**
Best for adaptive tool-use tasks. Requires `maxTurns` hard limit. Good fit for interactive debugging, web research, API integration tasks.

**✅ Blackboard via Filesystem**
Both platforms support this natively — agents write to distinct output files, orchestrator synthesizes. Low overhead (72% token reduction vs. workflow alternatives). Use unique write keys (filename per agent) to prevent conflicts.

**✅ Router/Dispatcher**
Excellent for modular skill dispatch. One routing call overhead. Scale to ~20 specialists. Both platforms support this pattern.

---

### 4.2 Recommend AGAINST

**❌ Pure Swarm (Peer-to-Peer, No Coordinator)**
17.2× error amplification. Gartner projects >40% of enterprise agentic AI projects canceled by 2027 (primarily compute costs and state management complexity). Reliability degrades multiplicatively with agent count. No exceptions for coordinated multi-domain tasks in production. Narrow exception: massive parallelism of genuinely independent, stateless, identical tasks (e.g., bulk document classification) — even here, a supervisor-coordinated wave pattern is safer.

**❌ DAG as Orchestration Model**
Works for deterministic pipelines with LLMs as compute nodes. Fails when LLMs are the coordinators. Prohibits feedback loops, retry, and adaptation. Use Sequential Pipeline instead.

**❌ Recursive Nesting (Subagents Spawning Subagents)**
Blocked by both Claude Code and Cursor (correctly). The math: 3 levels × 3 spawns each = 27 agents; at 4× token overhead per delegation level, 3 levels = ~64× token cost. Don't architect around this.

**❌ Starting with Multi-Agent Before Proving Single-Agent Insufficient**
The 80.9% SWE-bench result is an orchestrated result — the same model scores ~17 points lower in competing harnesses. Orchestration quality matters more than agent count. Multi-agent complexity is only justified for genuinely decomposable tasks. Prove your orchestration adds value before scaling. If failure is due to reasoning quality, upgrade the model before adding agents.

**❌ Unbounded Concurrent Agents (20+ in Claude Code)**
No throttling mechanism. Documented system instability (hard reboots, memory exhaustion). Anthropic declined to add `maxParallelAgents`. Cap manually at 10 maximum, 3–5 ideally.

**❌ Bag-of-Agents (Flat, No Hierarchy)**
17.2× error amplification vs. 4.4× with centralized coordination. Always add a coordinator even for simple parallel tasks.

**❌ AutoGPT / BabyAGI Patterns**
Both represent unbounded autonomous recursion. Community verdict as of 2026: useful for demos, dangerous in production. Neither has produced reliable production deployments.

**❌ Skipping the Reconciliation Layer**
Inter-agent handoffs without explicit reconciliation are the #1 source of silent drift. Every boundary between agents needs a verification/reconciliation step — either a dedicated agent or an explicit checkpoint.

**❌ Prompt Engineering as Error Control**
MAST taxonomy research (Cemri et al. 2025) shows structural architectural solutions substantially outperform prompt-level mitigations — hard boundaries, verification agents, and explicit iteration limits address root causes; prompting treats symptoms.

---

### 4.3 Conditional Recommendations

**LATS / Tree Search:** Use when maximum accuracy is the goal and token cost is unconstrained. Not for daily IDE workflows. Not suitable for real-time tasks.

**Actor-Critic:** Use for high-stakes decisions where single-agent bias is a concern (architecture, security). Overkill for routine coding tasks.

**Event-Driven / Pub-Sub:** Valid for Cursor Automations (GitHub, Slack, Linear triggers). Requires infrastructure beyond native Claude Code/Cursor for full pub-sub. Limit to external event integration use cases.

**Agent Teams (Claude Code experimental):** Valid for multi-domain research synthesis. Not production-stable — no session resume, one team per lead session, tmux/iTerm2 required for split panes. Watch for GA release.

**Managed Handoffs (OpenAI Agents SDK pattern):** Agents explicitly declare authorized handoff targets; boundary context is scrubbed between agents; `input_filter` prevents prompt injection propagation. **Condition:** Currently native only to OpenAI Agents SDK. Cannot be replicated natively in Claude Code (Agent Teams uses shared task list, not boundary-enforced handoffs) or Cursor. If handoff security is a requirement, consider this an external framework dependency.

---

## Part 5: Platform-Specific Guidance

### If you are primarily in Claude Code

- **Pattern ceiling:** Hierarchical (one level), fan-out with worktrees, sequential pipeline, plan-and-execute, reflection loop.
- **Hard limits to build around:** No nesting; cap at 5 concurrent for medium tasks; keep skill files under 3K tokens; proactively compact after each subtask.
- **Best orchestration architecture:** Orchestrator agent (reads task, decomposes, dispatches) → specialist subagents (worktree-isolated, write to distinct output files) → synthesis step (orchestrator or dedicated reconciliation subagent).
- **Context management is the job:** External memory for orchestrator state. Auto-compaction at ~95%. Subagent delegation specifically to keep main context lean.

### If you are primarily in Cursor

- **Pattern ceiling:** Fan-out (8 parallel, worktrees), one-level hierarchy, two-pass (generate/verify), plan-then-execute, event-driven Automations.
- **Hard limits to build around:** No subagent nesting; no LSP in worktrees; 40 MCP tool cap; 70–120K practical context (not 200K); plan mode bug risk. For cloud-scale concurrency (hundreds/thousands of agents), see Cursor Glass (cloud tier, §7.2.E) — requires Pro+ and usage-based billing.
- **Best orchestration architecture:** Parallel worktrees for independent tasks; subagent delegation for distinct specializations; hooks for autonomous iteration loops; Automations for external event triggers.
- **Leverage what Cursor does uniquely:** Visual diff review, best-of-N model comparison, Automations (Linear/Slack/GitHub integration).

### If you are working across both

- **Design for the lowest common denominator:** No nesting, file-system-based coordination, 4–5 concurrent agents max (safe on both platforms).
- **Platform-specific patterns are additive:** Use Cursor Automations for external event triggers; use Claude Code CLI for programmatic batch operations.
- **The architectural difference is fundamental:** Claude Code is a distributed systems tool. Cursor is an interactive development tool. Don't try to make Cursor behave like Claude Code for programmatic orchestration — it isn't designed for it.

---

## Part 6: Emerging Patterns and Watchlist (2025–2026)

**Watch Now (active adoption imminent):**
- **Context Engineering as discipline** (coined Karpathy/Lütke, mid-2025): Treating context window management as a first-class engineering concern, not prompt afterthought.
- **MCP + A2A emerging protocol stack:** MCP (Anthropic, Nov 2024) + A2A (Google, Apr 2025) — emerging agent-to-agent communication standards gaining cross-vendor adoption; Linux Foundation hosting interoperability discussions. Watch for Claude Code and Cursor native adoption.

**Watch Later (research/early stage):**
- **RL-trained conductor orchestration:** Orchestrators trained via reinforcement learning to route and coordinate. Not yet production-accessible.
- **Zettelkasten-style agent memory** (A-MEM, arXiv 2502.12110): Structured memory graph for agents — better than naive context window stuffing.
- **ACH (Analysis of Competing Hypotheses) pattern:** Multiple agents assigned explicitly opposing theories; surviving theory is more reliable. Emerging practitioner pattern.
- **Semantic revert:** Logical work unit rollback (undo a conceptual change, not just a git commit). Emerging tooling concept.
- **Multi-provider model routing:** 3–7 models per enterprise deployment, routed by task type. Platform support pending.

**Note on MAD (Multi-Agent Debate):** Production-ready for deterministic tasks (MASQRAD boosts coding benchmark accuracy from 80% to 91% `[PEER]`); risky for safety/alignment tasks without adversarial agent diversity safeguards.

---

## Sources

**Peer-Reviewed:**
- arXiv 2512.08296 — Google DeepMind, 180-configuration multi-agent study; 39–70% degradation on sequential tasks; 17.2× error amplification in flat topologies; 4-agent coordination saturation threshold
- arXiv 2603.22651 — Kulkarni & Kulkarni, "Benchmarking Multi-Agent LLM Architectures for Financial Document Processing" — F1 0.943 (Reflection), $0.187/doc (Sequential), $0.430/doc (Reflection), 98.5%/60.7% hierarchical cost-accuracy
- arXiv 2603.25620 — PICon multi-agent framework for financial document processing; F1 0.903 on sequential pipeline configuration
- arXiv 2601.06112 — "ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions" — ReAct 2.5% higher reliability than Reflexion; 80.9% fault recovery rate (Table 8)
- arXiv 2510.01285 — Blackboard pattern evaluation
- arXiv 2502.12110 — A-MEM Zettelkasten agent memory
- LLMCompiler, ICML 2024 — DAG efficiency with deterministic execution
- LATS, ICML 2024 — Language Agent Tree Search; 92.7% HumanEval pass@1 (GPT-4); alt. configuration 94.4%
- MAST taxonomy (Cemri et al. 2025), ICLR 2025 — 14 failure modes; 150 traces (derivation dataset); 1,642 traces (MAST-Data, failure rate distribution)
- Wang et al. (2023) — Plan-and-Execute framework; 92% task completion vs. 85% for ReAct; 3.6× speedup [cited in Pattern 6; full arXiv citation pending verification]
- Shinn et al. (2023) — Reflexion; language-feedback self-refinement loop; distinct from Pattern 7 Reflection/Self-Critique pattern [cited in Pattern 5; full arXiv citation pending verification]
- Flash-Searcher — 82.5% GAIA benchmark using DAG-as-scaffold execution [PEER/PRAC — source: subagent research March 2026; full citation pending verification]

**Official Documentation:**
- code.claude.com/docs/en/sub-agents
- code.claude.com/docs/en/agent-teams
- platform.claude.com/docs/en/agent-sdk/overview
- cursor.com/docs/configuration/worktrees
- cursor.com/blog/2-0 (Cursor 2.0 announcement, Oct 2025)
- cursor.com/blog/agent-best-practices
- docs.cursor.com/context/model-context-protocol

**Practitioner Reports:**
- GitHub Issue #15487 (Claude Code concurrent agent limits, Dec 2025)
- forum.cursor.com/t/better-multi-agent-orchestration/151730
- Shipyard.build — Multi-agent orchestration for Claude Code in 2026
- Addy Osmani — The Code Agent Orchestra
- Zach Wills — How to Use Claude Code Subagents to Parallelize Development
- Gartner, June 2025 (reported via The New Stack) — >40% of enterprise agentic AI projects projected to be canceled by end of 2027 (compute costs, latency, state management)
- Anthropic engineering blog, "How we built our multi-agent research system," June 2025 — 90.2% improvement claim [CONF — not in Gemini source; unverified]
- builder.io/blog/cursor-vs-claude-code
- qodo.ai/blog/claude-code-vs-cursor
- vibecoding.app/blog/cursor-problems-2026

---

## Part 7: Gemini Deep Research Integration

_Source: "Agent Orchestration Patterns for LLM-Based Multi-Agent Systems: A 2026 State-of-the-Field Analysis" — Gemini Deep Research, March 2026._

This section records findings from Gemini Deep Research that confirm, extend, or materially differ from the parallel research above. Conflicts and additions are called out explicitly.

---

### 7.1 Confirmations and Convergence

The following findings from our subagent research are independently confirmed by Gemini:

- **DAG anti-pattern confirmed** with additional mechanism: "state space explosion and context flooding" — static DAGs cannot dynamically optimize context windows, dumping entire graph history into every subsequent node, causing attention degradation and hallucinations.
- **Swarm anti-pattern confirmed** with an important provenance note: OpenAI explicitly deprecated the original "Swarm" repository (March 2025), labeling it "educational only," and replaced it with the Agents SDK using a strictly controlled **Handoff** pattern with deterministic, bounded routing.
- **Hierarchical supervisor-worker** confirmed as the production workhorse. DeepMind 180-config study cited consistently (arXiv 2512.08296).
- **17.2× error amplification** from flat topologies confirmed.
- **ReAct** confirmed as the universal leaf-node execution pattern. "ReAct becomes a fatal anti-pattern if used as the primary orchestration method for a massive system."
- **LATS at 92.7% HumanEval pass@1** (Gemini figure) vs. 94.4% (our subagent). Minor variance — both confirm LATS as ceiling-performance for code but cost-prohibitive for daily use.

---

### 7.2 New Findings from Gemini Not in Subagent Research

#### A. Coordination Tax — Quantified

Gemini provides a precise number our subagents did not surface:

> A task requiring 10,000 tokens for a single agent may consume 35,000 tokens when distributed across a 4-agent hierarchical setup — a **3.5× cost multiplier** dedicated purely to coordination overhead before any ReAct retry or Actor-Critic cycles.

DeepMind's saturation data: coordination gains **plateau sharply at 4 concurrent agents**. Beyond 4, the Coordination Tax consumes marginal utility from additional agents.

_Implication: The "3–5 concurrent agents" sweet spot our research identified is correct. The DeepMind data suggests 4 is the specific optimization peak._

#### B. Pipeline Reliability Mathematics — Explicit

The compound reliability calculation Gemini surfaces is critical for architectural decisions:

| Pipeline Steps | 99% individual reliability | 95% individual reliability |
|---|---|---|
| 5 steps | 95.1% | 77.4% |
| 10 steps | 90.4% | **59.9%** |
| 20 steps | 81.8% | **35.8%** |

**Interpretation:** Any pipeline longer than ~5 steps with agents that are less than 99% reliable will fail more often than it succeeds. This mathematically mandates Actor-Critic validation nodes at intermediate steps for long pipelines.

#### C. Claude Code Memory Leak — Bug #1042

Gemini surfaces a specific documented defect: background agents in **ruvnet/claude-flow** (a community orchestration project built on Claude Code) fail to terminate properly, consuming up to **650MB RAM per idle agent**. This is the proximate cause of the 10–12 agent practical limit — it is a memory leak, not a design ceiling. A fix would raise the practical concurrency ceiling above the current 10-12 agent practical limit.

_Source: ruvnet/claude-flow GitHub Issue #1042 (github.com/ruvnet/claude-flow/issues/1042). Note: this is a community project, not Anthropic's official Claude Code repository._

#### D. Claude Code File-Locking Bottleneck

In Claude Code Agent Teams, strict file-locking causes lock-contention when agents are assigned interdependent, single-file edits. A 10-agent team can degrade to the effective throughput of a single agent while agents wait for file access. Mitigation: worktree isolation ensures each agent works on a distinct branch, eliminating lock contention.

#### E. Cursor's Dual-Tier Architecture — Clarification

Gemini provides important nuance on Cursor that our Cursor subagent partially missed:

**Tier 1 (Local):** The ~4 concurrent agents limit is accurate for local IDE agents — constrained by LSP responsiveness and local hardware.

**Tier 2/3 (Cloud — "Cursor Glass"):** Via Background Agents and the Cursor Glass cloud control plane, concurrency scales to **hundreds or thousands** of agents running in isolated cloud VMs. Gemini cites a Cursor benchmark: 36-hour autonomous run building a web browser using thousands of cloud agents.

_Practical implication: The "4 agents" limit is a local IDE constraint. Cloud-scaled Cursor is a fundamentally different operational model — but it requires Pro+ and usage-based billing, and the cloud VM environment is not the same as local Claude Code._

**Cursor's key innovation over Claude Code:** Cursor uses **Optimistic Concurrency Control** `[CONF — source: Cursor 2.0 launch blog; OCC behavior not confirmed in official Cursor engineering documentation]` — agents read freely, but writes fail and retry semantically if underlying code changed during execution. Claude Code uses **strict file-locking** (Agent Teams). Both prevent conflicts; Cursor's approach eliminates the lock-contention throughput bottleneck at the cost of requiring semantic retry logic.

#### F. MAST Taxonomy — Full Dataset

Our subagent research cited 150 traces used to derive and validate the 14 failure modes. The same study (Cemri et al. 2025) also uses MAST-Data (1,642 production traces) to calculate failure rate distributions. These are two datasets from one study, not two separate studies. Failure category breakdown:

| Category | % of Failures |
|---|---|
| System Design Issues (step repetition, history loss, infinite loops) | 44.2% |
| Inter-Agent Misalignment (information withholding, ignoring peer input) | 32.3% |
| Task Verification (premature termination, incomplete verification) | 23.5% |

The 44.2% figure for system design issues is striking — nearly half of all failures are architectural, not model quality problems.

#### G. Multi-Agent Debate (MAD) — New Pattern

Not covered in our subagent research. MAD is an emerging test-time scaling technique: diverse agents propose solutions and aggressively critique each other iteratively. Important nuance:

- **MAD helps:** Highly deterministic, difficult mathematical/logical problems.
- **MAD hurts:** Safety, compliance, and alignment tasks. Collaborative refinement can be manipulated into generating sophisticated jailbreaks. Requires rigorously diverse and adversarially aligned agent pools.

_Confidence: MEDIUM — early 2026 research, not yet production-validated._

#### H. Tool-Use vs. Orchestration — Formal Distinction

Gemini formalizes a distinction our research treated informally:

> **Tool-use** = a single model calling functions (APIs, databases, calculators) within one context window. **Orchestration** = managing lifecycle, state, and context transfers between distinct LLM inference loops with separate system prompts, memory boundaries, and potentially different foundation models.

Anti-pattern: calling a single agent with 50 tools a "50-agent system." Forces a single model to juggle dozens of schemas, causing instruction-following degradation and catastrophic tool-selection hallucinations.

#### I. Framework Landscape — Additions

Gemini adds framework detail not in our subagent research:

| Framework | Pattern | Key Differentiator |
|---|---|---|
| LangGraph v1.0 GA | Dynamic State Machine | Enterprise standard; time-travel debugging; durable checkpointing |
| Mastra v1.0 Beta | Task DAG / Code-first | TypeScript-first; native Next.js/Vercel AI SDK v5 integration |
| ControlFlow (Prefect 3.0) | Task-Centric / Hybrid | Bridges traditional data pipelines with LLM nodes; native observability |
| OpenAI Agents SDK | Managed Handoffs | Replaced Swarm; strict boundary enforcement; end-to-end tracing |
| Microsoft AutoGen | Actor Model | Forking into community AG2 + Azure-native; high overhead |

_Note: These are external Python/TypeScript frameworks — out of scope for the Claude Code / Cursor focus of this report unless a specific pattern requires external scaffolding._

---

### 7.3 Findings That Conflict or Require Reconciliation

_Note: Pre-correction values shown in this table for traceability — body text uses corrected figures._

| Claim | Our Research (pre-correction) | Gemini | Resolution |
|---|---|---|---|
| SWE-bench Verified | 76.8% (subagent research) | 80.9% (Gemini source) | Resolved: 80.9% is correct and orchestrated; 76.8% was a subagent error. Central thesis corrected accordingly. |
| Cursor concurrent agents | 8 (Cursor 2.0, Oct 2025) | ~4 local, hundreds via cloud | Both correct — different tiers. 8 is the parallel worktree cap locally; cloud is separate |
| LATS HumanEval pass@1 | 94.4% | 92.7% | Minor variance across test configurations; both confirm LATS as ceiling pattern |
| MASFT/MAST traces | 150 (derivation dataset) | 1,642 (MAST-Data) | Same study (Cemri et al. 2025) — two datasets, one taxonomy. Presented as unified study. |
| Coordination plateau | 3–5 agents (sweet spot) | 4 agents (DeepMind saturation) | Consistent — DeepMind's 4 is the mathematical peak; 3–5 is the safe operating range |

---

### 7.4 Gemini Follow-Up Integration

Gemini follow-up responses received and integrated. Key corrections applied:
- SWE-bench figure corrected from 76.8% to 80.9% (orchestrated result)
- MASFT and MAST unified as one study (Cemri et al. 2025) with two datasets
- "40% fail" attribution corrected to Gartner June 2025 (not The New Stack)
- Token cost 15× (agent teams) removed as unverified; replaced with 3.2–4.2×
- Wave execution and dynamic scaling downgraded from Anthropic official to community extrapolation [PRAC]
- F1 0.903 attribution corrected from arXiv 2603.22651 to arXiv 2603.25620 (PICon framework)
- LATS HumanEval updated to 92.7% (Gemini-verified) as primary figure

---

## Part 8: AVFL Validation Notes

AVFL pass 1 complete. Score: -100/100 (51 findings). Fixer pass in progress. Re-validation pending at skepticism 2.

**Summary of findings addressed:**
- 1 Critical (frontmatter)
- 13 High (central thesis, MASFT/MAST, SWE-bench, attribution errors, platform constraints)
- 22 Medium (sourcing, platform notes, terminology, decision frameworks)
- 15 Low (title, math, labels, source entries)

---

_**Status:** Gemini primary research integrated. Follow-up responses received and incorporated. AVFL pass 1 complete. Fixer pass applied._
