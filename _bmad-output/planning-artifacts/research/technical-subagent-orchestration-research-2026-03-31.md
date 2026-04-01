---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/planning-artifacts/research/technical-subagent-orchestration-research-2026-03-30.md
workflowType: 'research'
lastStep: 4
research_type: 'technical'
research_topic: 'LLM agent orchestration patterns: comprehensive benchmark-anchored survey 2025-2026'
research_goals: 'Document all major orchestration patterns beyond DAG and Swarms; explain DAG and Swarm failure modes with empirical evidence; survey benchmark results (SWE-bench, GAIA, AgentBench, WebArena, OSWorld, HumanEval); identify recommended patterns as of early 2026; provide scale limits, token cost, and citations for each pattern'
user_name: 'Steve'
date: '2026-03-31'
web_research_enabled: true
source_verification: true
---

# Research Report: LLM Agent Orchestration Patterns — Comprehensive Survey 2025-2026

**Date:** 2026-03-31
**Author:** Steve
**Research Type:** Technical (web-verified, 2025-2026 sources)
**Predecessor document:** `technical-subagent-orchestration-research-2026-03-30.md` (covers Wave/Parallel-Batch, DAG, Hierarchical, Mesh, Blackboard, Reactive, Framework Verdicts, Claude Code native capabilities, wshobson/agents analysis)

---

## Research Scope

**Research Topic:** LLM agent orchestration patterns: comprehensive benchmark-anchored survey 2025-2026

**Research Goals:**
1. Document orchestration patterns beyond DAG and Swarms: hierarchical, sequential pipelines/chains, router/dispatcher, reflection/self-critique loops, plan-and-execute, ReAct, LATS, actor-critic, blackboard/shared-memory, event-driven/pub-sub
2. Explain DAG failure modes with specificity
3. Explain Swarm failure modes with empirical evidence
4. Survey benchmark results: SWE-bench, GAIA, AgentBench, HumanEval, WebArena, OSWorld
5. Identify recommended patterns as of early 2026

**Scope:** Per-pattern treatment with structural description, strengths, failure modes, scale limits, token/cost overhead, source URL and date. Peer-reviewed evidence distinguished from community/practitioner consensus.

**Research Methodology:** Parallel web searches with direct URL fetches of primary sources. Peer-reviewed papers (arXiv, ICML, NeurIPS, ICLR) distinguished from practitioner blogs.

**Scope Confirmed:** 2026-03-31

---

## Research Overview

This document extends and deepens the 2026-03-30 research with a pattern-by-pattern treatment anchored to 2025-2026 benchmark data. It covers 11 distinct orchestration patterns, the empirical case against DAGs and Swarms, and the current state of major agent benchmarks. Sources include peer-reviewed papers from ICML 2024, arXiv 2025-2026, Nature journals, and practitioner evidence from production deployments.

**Notation for evidence quality:**
- `[PEER]` — Peer-reviewed (arXiv, ICML, NeurIPS, ICLR, Nature)
- `[PRAC]` — Practitioner consensus / community (blog, framework docs, benchmarking blog)
- `[PROD]` — Production case study / enterprise report

---

## Part 1: Pattern Catalog

### Pattern 1: Sequential Pipeline / Chain

**Structure:** Fixed linear sequence of agents. Each agent receives the previous agent's output as input and passes its own output forward. No branching, no loops, no concurrent execution.

**Typical shape:** Parser Agent → Extractor Agent → Summarizer Agent → Formatter Agent

**Strengths:**
- Simplest to implement and debug — deterministic execution order, full traceability
- Lowest orchestration overhead of all multi-agent patterns
- Each agent has a bounded, focused context
- State flows predictably through shared session state (output_key pattern)
- Google ADK recommendation: "your go-to architecture for data processing pipelines" `[PRAC]`

**Failure modes:**
- Error compounding: a mistake in step N propagates uncorrected to step N+1 through the entire chain
- Context accumulation: with cumulative context threading (each agent sees all prior outputs), late-chain agents face context window pressure
- No adaptation: cannot revise earlier decisions based on later discoveries
- Sequential throughput ceiling: total latency = sum of all agent latencies, no parallelism
- Cross-table reference failures: 28.4% of errors in sequential extraction pipelines arise from cross-document reference resolution failures `[PEER]`

**Quantitative data (financial document extraction, 10,000 SEC filings, Claude 3.5 Sonnet):**
- F1: 0.903
- Document accuracy: 64.8%
- Cost: $0.187/document
- Latency (p50): 38.7 seconds
- Scales best at high document volume; most resilient pattern at >25K docs/day `[PEER]`

**Scale limits:**
- Degrades with chain length beyond ~5 agents due to error compounding
- No hard concurrency ceiling (it's sequential), but total latency grows linearly with chain length
- Context accumulation pattern fails before ~8 agents without explicit summarization

**Token overhead:** Lowest of all multi-agent patterns — only one agent active at a time. With cumulative context, input tokens grow O(n) with chain length.

**Source:** [Benchmarking Multi-Agent LLM Architectures](https://arxiv.org/html/2603.22651) — March 2026 arXiv `[PEER]`; [Google ADK Patterns Guide](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — 2025 `[PRAC]`

---

### Pattern 2: Parallel Fan-Out / Fan-In

**Structure:** An orchestrator dispatches N independent subtasks simultaneously to N subagents. All N subagents execute concurrently. A synthesizer agent (or the orchestrator itself) aggregates results when all N complete. This is the "wave" pattern from the 2026-03-30 research.

**Typical shape:** Orchestrator → [Agent A, Agent B, Agent C] → Synthesizer

**Strengths:**
- Clean context isolation: each subagent receives only tokens relevant to its subtask — avoids the self-conditioning degradation of single-context chains
- Latency = max(subagent latencies), not sum — major throughput advantage over sequential
- Natural fit for independent parallel analyses (multi-perspective review, concurrent web search, parallel code review)
- Anthropic's production Research feature uses exactly this model: 3–5 subagents per wave `[PRAC]`
- Google ADK recommendation: "useful to reduce latency or gain diverse perspectives" `[PRAC]`

**Failure modes:**
- Straggler problem: slowest member of the wave sets pace for the entire fan-in
- Synthesis bottleneck: aggregating many large outputs at a single synthesis node can overflow context window
- Race conditions on shared state: subagents writing to the same keys require mutex/unique-key discipline
- Token redundancy: parallel branches re-process overlapping context, leading to redundant input token consumption
- Coordination overhead: reconciling contradictory parallel outputs requires a non-trivial synthesis step

**Quantitative data (financial document extraction):**
- F1: 0.914
- Document accuracy: 67.2%
- Cost: $0.221/document (+18% vs sequential)
- Latency (p50): 21.3 seconds (45% faster than sequential)
- Least token-efficient pattern (2.43% token efficiency ratio) due to overlapping context windows `[PEER]`

**Scale limits:**
- Anthropic's Claude Code: ~10 concurrent operations hard cap
- Context synthesis degrades beyond ~8 parallel agents without summarization at agent level
- Error amplification becomes significant beyond 5 agents: 5-agent sequences degrade to 77% reliability if each agent has 95% success rate (compounding) `[PRAC]`

**Token overhead:** ~4× chat per subagent. Agent Teams configuration: ~15× chat total. Parallel redundancy adds ~18% token cost versus sequential baseline. `[PRAC]`

**Source:** [Benchmarking Multi-Agent LLM Architectures](https://arxiv.org/html/2603.22651) — March 2026 `[PEER]`; [Anthropic Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) `[PRAC]`

---

### Pattern 3: Hierarchical Orchestration

**Structure:** Agents organized in a tree. Top-level strategic orchestrator → mid-level domain supervisors → leaf workers. Each level holds only the context appropriate to its scope. Delegation flows top-down; results bubble up via summarization.

**Typical shape:**
```
Strategic Orchestrator
├── Domain Supervisor A → Worker A1, Worker A2
└── Domain Supervisor B → Worker B1, Worker B2
```

**Strengths:**
- Scales to 20+ agent problems that would overflow any single context window
- Domain context encapsulation: supervisors hold specialized context without burdening the strategic layer
- Google ADK recommendation for tasks "too big for one agent context window" `[PRAC]`
- Hierarchical supervisor-worker achieves 98.5% of reflexive F1 at 60.7% of cost in production — the best cost-accuracy tradeoff for moderate-scale (10K-50K docs/day) deployments `[PEER]`

**Quantitative data (financial document extraction):**
- F1: 0.929
- Document accuracy: 71.8%
- Cost: $0.261/document
- Latency (p50): 46.2 seconds
- Optimized variant (semantic caching + model routing): F1 0.924 at $0.148/doc — 89% of reflexive gains at 1.15× sequential baseline cost `[PEER]`

**Failure modes:**
- Information loss through summarization at level boundaries — the critical failure mode for hierarchical systems
- Latency tax: minimum ~6 seconds overhead per 3-level hierarchy before any worker starts (2s per LLM call per level)
- Debugging requires distributed tracing across levels
- Hard limit in Claude Code: no nested teams — maximum depth is lead + teammates; truly deep hierarchies require custom implementation

**Scale limits:**
- 3-level hierarchies are practical; 4+ levels introduce sufficient latency and information loss to undermine the value
- Scales effectively to ~20-50 agents when levels are cleanly separated by domain boundary
- Claude Code native maximum: lead + 1 level of teammates; no nested subagents from teammates `[PRAC]`

**Token overhead:** ~2.78% token efficiency ratio (same as reflexive), achieved through targeted extraction. Total token count is moderate (one model call per level per task). `[PEER]`

**Source:** [Benchmarking Multi-Agent LLM Architectures](https://arxiv.org/html/2603.22651) — March 2026 `[PEER]`; [Google ADK Patterns Guide](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) `[PRAC]`

---

### Pattern 4: Router / Dispatcher

**Structure:** A central lightweight agent (often a smaller/cheaper model) analyzes incoming intent and routes the request to the appropriate specialist agent. The dispatcher does not execute tasks — it classifies and delegates.

**Typical shape:** Request → Dispatcher (intent classification) → [Specialist A | Specialist B | Specialist C]

**Routing approaches (in order of sophistication):**
1. Rule-based: keyword matching, regex, hardcoded logic
2. ML classifier: fine-tuned classification model on intent categories
3. LLM-as-router: LLM reads sub-agent descriptions and selects the best match (AutoFlow in Google ADK)
4. Semantic router: embedding similarity between query and agent capability descriptions

**Strengths:**
- Isolates complexity: each specialist maintains deep domain focus without competing contexts
- Cost optimization: router can be a cheap small model; only expensive models handle actual domain work
- Enables specialization at scale: 16+ specialists behind a single routing layer (wshobson/agents uses exactly this)
- Model Context Protocol (MCP) servers extending routing with standardized agent capability description `[PRAC]`
- Google ADK `AutoFlow` mechanism uses LLM-driven delegation based on sub-agent `description` fields `[PRAC]`

**Failure modes:**
- Single point of failure: router misclassification sends task to wrong specialist; no automatic recovery
- Ambiguous intents: queries spanning multiple domains require either query decomposition or fallback handling
- Circular routing risk: if LLMs are routers, they can create cycles in what should be acyclic dispatching
- Cold-start: new specialists must be explicitly registered; zero-shot routing to unknown agents fails

**Scale limits:**
- LLM-based router degrades with very large specialist catalogs (>20 specialists) — retrieval augmentation needed
- No inherent concurrency ceiling; router itself is stateless so scales horizontally
- Routing accuracy drops with semantic overlap between specialist descriptions

**Token overhead:** Router adds one LLM call (~500-1000 tokens) per request. Total overhead minimal (<5% of specialist execution cost). `[PRAC]`

**Source:** [AWS Prescriptive Guidance: Routing Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/routing-dynamic-dispatch-patterns.html) `[PRAC]`; [Google ADK Developer Guide](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) `[PRAC]`; [Patronus AI: Agent Routing Best Practices](https://www.patronus.ai/ai-agent-development/ai-agent-routing) `[PRAC]`

---

### Pattern 5: ReAct (Reasoning + Acting)

**Structure:** Interleaved Thought → Action → Observation cycles. The agent thinks out loud (chain-of-thought), chooses a tool call (action), observes the result, then repeats. Proposed by Yao et al. (2022), now the dominant single-agent loop architecture.

**Typical shape (one cycle):**
```
Thought: I need to find the population of France
Action: search("France population 2024")
Observation: France population is approximately 68 million
Thought: Now I can answer the question
```

**Strengths:**
- Transparency: reasoning trace is auditable and explainable — critical for regulated industries
- Adaptive: each observation informs the next thought; highly responsive to unexpected tool results
- Fault recovery: simple retry logic outperforms more complex architectures under stress
- Well-studied: most empirically validated single-agent architecture; extensive production tooling
- ReAct achieves 2.5% higher reliability than Reflexion under production stress conditions `[PEER]`
- 80.9% fault recovery rate vs 67.3% for Reflexion `[PEER]`

**Failure modes:**
- Long-horizon degradation: ReAct agents struggle beyond ~5 sequential reasoning steps; compounding errors in thought chain
- Latency: each cycle requires one full LLM call; multi-step tasks are slow
- Tool dependency: quality bounded by tool reliability; poor tools corrupt the observation stream
- Context growth: each Thought/Action/Observation triplet grows the context window
- Rate limiting is the largest single source of degradation — 2.5% below mixed baseline under rate-limit injection `[PEER]`
- Self-conditioning errors compound from ~step 2 onwards (arXiv 2509.09677 documents 39% multi-turn degradation) `[PEER]`

**Benchmark results:**
- Gradientsys (ReAct orchestration for multi-agent scheduling): 24.1% on GAIA vs 15.0% baseline — 60% relative improvement `[PEER]`
- HotPotQA baseline performance: ~44% exact match (single ReAct agent)
- ReAct baseline on Gaia2: 48.3% overall (ERL improves this to 56.1%) `[PEER]`

**Scale limits:**
- ReAct is fundamentally single-agent; multi-agent extensions (Gradientsys, LangGraph) layer orchestration on top
- Single ReAct loop degrades beyond ~10 tool calls per session without memory augmentation
- Multi-turn degradation becomes significant at ~2-3 reasoning steps per chain-of-thought

**Token overhead:** Medium — 2,000-3,000 tokens per task; 3-5 API calls `[PRAC]`

**Cost (GPT-4):** $0.06-0.09 per task `[PRAC]`

**Source:** [ReliabilityBench arXiv 2601.06112](https://arxiv.org/html/2601.06112v1) — 2026 `[PEER]`; [Gradientsys arXiv 2507.06520](https://arxiv.org/abs/2507.06520) `[PEER]`; [Dev.to ReAct vs Plan-and-Execute](https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9) `[PRAC]`

---

### Pattern 6: Plan-and-Execute

**Structure:** Explicit separation of planning (high-reasoning model) from execution (lighter/faster model). The planner generates a complete multi-step plan upfront; the executor carries out steps sequentially; a re-planner can revise the plan based on execution results.

**Typical shape:**
```
[Planner: o3/Claude] → structured task DAG
[Executor: Llama 70B / fast model] → executes each step
[Re-planner: triggered on failure/surprise] → revises remaining plan
```

**Strengths:**
- Forces explicit "think through all steps" reasoning — improves long-horizon task quality
- Cost optimization: small fast models handle execution; expensive model only invoked for (re)planning
- 92% task completion rate with 3.6× speedup over sequential ReAct execution `[PRAC]`
- Superior for multi-step tasks: 92% completion accuracy vs 85% for ReAct `[PRAC]`
- Clean separation of concerns enables different safety/validation policies per phase
- Secure Plan-then-Execute implementations (arXiv 2509.08646) have formal security analysis `[PEER]`

**Failure modes:**
- Brittle to unexpected mid-execution results: if the world changes between planning and execution, the plan is stale
- Replanning overhead: every plan revision adds a full planner LLM call
- Planner hallucination: a bad plan fails the entire task; no step-by-step course correction during execution
- Higher implementation complexity than ReAct
- Front-loaded cost: planner call is expensive even for simple tasks that would have been cheap in ReAct

**Scale limits:**
- Planner context grows with plan complexity — very complex plans (>20 steps) exceed planner context
- Re-planner calls multiply for dynamic tasks; degenerate case approaches ReAct cost
- Works well up to ~15-step plans with a capable replanner; degrades beyond that

**Token overhead:** Higher than ReAct — 3,000-4,500 tokens per task; 5-8 API calls `[PRAC]`

**Cost (GPT-4):** $0.09-0.14 per task — roughly 1.6× ReAct `[PRAC]`

**Source:** [Dev.to ReAct vs Plan-and-Execute](https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9) `[PRAC]`; [arXiv 2509.08646 Secure Plan-then-Execute](https://arxiv.org/abs/2509.08646) `[PEER]`; [n1n.ai 5 Patterns 2026](https://explore.n1n.ai/blog/5-ai-agent-design-patterns-master-2026-2026-03-21) `[PRAC]`

---

### Pattern 7: Reflection / Self-Critique Loop

**Structure:** A multi-phase cycle: Generate → Critique → Refine. The same agent (or a separate critic agent) reviews its own output, identifies weaknesses, and produces a revised version. Iterations continue until a quality threshold is met or a loop limit is reached.

**Two major variants:**

**7a. Single-agent Reflexion (Shinn et al., 2023):** Agent reflects on its own failures and stores verbal reflections as episodic memory for future attempts. No separate critic model.

**7b. Generator-Critic (multi-agent):** Separate generator and critic agents. Critic provides adversarial feedback; generator revises. Google ADK calls this the "Generator and Critic Pattern."

**Strengths:**
- Measurable accuracy gains on code generation:
  - HumanEval: 80% → 91% with reflection (11-point gain) `[PRAC]`
  - With external verification: accuracy gains can exceed 30 percentage points `[PRAC]`
  - MAR (Multi-Agent Reflexion): HumanEval pass@1 76.4 → 82.6 (+6.2 points); HotPotQA 44 → 47 EM (+3 points) `[PEER]`
- Highest F1 of all patterns in financial extraction (0.943) `[PEER]`
- Highest document accuracy (75.8%) across all patterns tested `[PEER]`
- Google ADK uses `LoopAgent` with `condition_key` and `exit_condition` primitives `[PRAC]`

**Failure modes:**
- Oscillation: reflexive architecture's dominant failure is oscillating between ambiguous interpretations (39.3% of errors) — the agent can't escape local optima `[PEER]`
- Confirmation bias: single-agent Reflexion uses the same model for action, evaluation, and reflection — "repeated reasoning errors" and "limited corrective feedback" `[PEER]`
- Latency: highest latency of all patterns (74.1s p50 vs 38.7s sequential) `[PEER]`
- Cost: highest absolute cost ($0.430/doc — 2.3× sequential) `[PEER]`
- Scale ceiling: degrades beyond 25K docs/day due to queuing-induced timeout truncation `[PEER]`
- Complexity amplification under stress: Reflexion shows 10% degradation under fault injection vs 7.5% for simpler ReAct — "architectural complexity introduces vulnerabilities" `[PEER]`
- Loop termination: without explicit max_iterations, agents can cycle indefinitely

**Scale limits:**
- Best at low-medium volume (<25K operations/day) — degrades at scale due to queuing
- 3 iterations is the empirically identified sweet spot; >3 iterations shows diminishing returns
- Generator-Critic: n-squared messaging overhead if N critics are used; keep critic count ≤ 3

**Token overhead:** Highest of all patterns. 2.78% token efficiency ratio — same as hierarchical but total token count is much higher due to iteration. `[PEER]`

**Source:** [Benchmarking Multi-Agent LLM Architectures](https://arxiv.org/html/2603.22651) `[PEER]`; [MAR arXiv 2512.20845](https://arxiv.org/html/2512.20845) `[PEER]`; [ReliabilityBench arXiv 2601.06112](https://arxiv.org/html/2601.06112v1) `[PEER]`; [Google ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) `[PRAC]`; [Reflexion arXiv 2303.11366](https://arxiv.org/pdf/2303.11366) `[PEER]`

---

### Pattern 8: LATS (Language Agent Tree Search)

**Structure:** Integrates Monte Carlo Tree Search (MCTS) into LLM agent execution. The agent maintains a search tree of possible action sequences. At each node, it can: (a) expand by generating new child actions, (b) simulate by executing a partial trajectory, (c) backpropagate by updating node values based on reflection on outcomes. Self-reflection mechanisms generate natural language evaluations of partial trajectories to guide search.

**Paper:** Zhou et al., ICML 2024 — "Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models"

**Strengths:**
- Unifies reasoning, acting, and planning in a single framework
- HumanEval pass@1: 94.4% with GPT-4 — among the highest ever reported on that benchmark at time of publication `[PEER]`
- HotPotQA: 75.9 average score with GPT-3.5 `[PEER]`
- Outperforms ReAct, CoT, and RAP on decision-making tasks across programming, QA, web navigation, and mathematical reasoning `[PEER]`
- Can recover from failed paths by backtracking through the search tree — unlike linear ReAct or plan-and-execute

**Failure modes:**
- Extremely high token cost: MCTS exploration of a search tree requires many LLM calls per decision; latency and cost are the primary barriers to production deployment
- Implementation complexity: requires custom MCTS infrastructure; not available natively in any major framework
- Tree explosion: without good value function estimates, the search tree grows exponentially
- Scaling to more capable base models reduces the relative advantage — frontier models may not need tree search for simpler tasks

**Scale limits:**
- Practical for tasks with well-defined terminal states (code passes tests; answer is correct)
- Does not scale to open-ended creative tasks where "better" is not objectively measurable
- Token cost scales with tree depth × branching factor; deep trees (depth >5, branching >3) become prohibitively expensive

**Token overhead:** Very high — MCTS exploration multiplies ReAct token cost by the branching factor and depth. For a depth-3, branching-3 tree: ~27× a single ReAct call. `[PEER estimated]`

**Source:** [LATS arXiv 2310.04406 / ICML 2024](https://arxiv.org/abs/2310.04406) `[PEER]`; [LATS GitHub](https://github.com/lapisrocks/LanguageAgentTreeSearch) `[PEER]`

---

### Pattern 9: Actor-Critic

**Structure:** Two-role separation: an Actor agent proposes solutions/actions; a Critic agent analyzes them, identifies errors, and generates targeted feedback; the Actor revises. The Critic's role is adversarial — it is explicitly incentivized to find faults.

**Structural distinction from Reflection (Pattern 7):**
- Reflection: same agent (or generic critic) reviews output
- Actor-Critic: two agents with fixed and distinct roles; Critic is domain-specialized and adversarial
- Actor-Critic can use RL to train the orchestrator's agent-sequencing policy

**2025 variant — Critique-Guided Improvement (CGI):** Two-player framework; actor explores an environment; critic generates detailed natural language feedback promoting more robust strategy exploration. `[PEER]`

**Puppeteer variant (2025):** Centralized orchestrator trained via RL to dynamically direct agents based on evolving task state. Achieves adaptive agent sequencing without hardcoded policies. `[PEER]`

**Strengths:**
- Adversarial critique breaks confirmation bias in single-agent reflection
- Role specialization: critic can be fine-tuned for a specific quality dimension (security, performance, correctness)
- Demonstrated gains on multi-hop reasoning and code generation tasks
- 3-lens AVFL variant in Momentum (Enumerator + Adversary per lens) is an actor-critic instantiation

**Failure modes:**
- Sycophancy risk: if the Actor and Critic are the same model, critic feedback degrades into agreement
- Token cost: each revision cycle is two full LLM calls (actor + critic) plus any tool use
- Loop termination: without a stop condition, Actor-Critic cycles can run indefinitely
- Critic miscalibration: an overly aggressive critic generates unhelpful nitpicking; overly lenient critic provides no value

**Scale limits:**
- 2-3 agent pairs is the practical ceiling for unaugmented Actor-Critic; additional critics beyond 3 show diminishing returns
- RL-trained orchestrators (puppeteer) require training data — not zero-shot deployable

**Token overhead:** ~2× ReAct per cycle (actor + critic calls). Multiple cycles multiply this. `[PRAC estimated]`

**Source:** [Actor-Critic for LLM Decision-Making arXiv 2311.13884](https://arxiv.org/html/2311.13884v3) `[PEER]`; [CGI arXiv 2503.16024](https://arxiv.org/html/2503.16024v2) `[PEER]`; [Multi-Agent Evolving Orchestration arXiv 2505.19591](https://arxiv.org/abs/2505.19591) `[PEER]`

---

### Pattern 10: Blackboard / Shared-Memory

**Structure:** A shared global state structure (the "blackboard") that all agents can read and write. Specialist agents monitor the blackboard and autonomously volunteer contributions when they have relevant capability. A control unit (arbiter) selects which agent acts next based on current blackboard state. No central orchestrator dictates assignments — agents self-select based on board content.

**Key components:**
- Public blackboard space: shared communication visible to all agents
- Private spaces: agent-pair discussion areas (in advanced implementations)
- Control unit: monitors board state, selects next contributor
- Specialist agents: heterogeneous agents that monitor and contribute opportunistically

**Strengths:**
- 13-57% relative improvement in end-to-end success over best baselines including RAG and master-slave frameworks `[PEER]`
- Up to 9% relative gain in data discovery F1 over orchestrator-worker baselines `[PEER]`
- Token efficiency: single shared blackboard reduces per-agent prompt lengths vs. point-to-point messaging `[PEER]`
- LbMAS with two LLMs outperforms average of a single LLM while spending fewer tokens `[PEER]`
- Competitive MMLU: 85.35%; ARC-Challenge: 93.43%; GSM8K: 94.46% `[PEER]`
- Outperforms Chain-of-Thought by 4.33% average; static multi-agent by 5.02% `[PEER]`
- Handles heterogeneous, evolving agent capabilities without upfront workflow specification
- Particularly powerful for large data science problems with unknown solution paths

**Failure modes:**
- Write conflicts: multiple agents simultaneously updating shared state require locking/arbitration
- Arbiter as bottleneck: control unit becomes a single point of failure
- Staleness: agents may act on stale board state if reads and writes are not properly ordered
- Debugging complexity: non-deterministic agent participation makes trace replay difficult
- Scaling: blackboard read throughput becomes a bottleneck with many concurrent agents

**Scale limits:**
- Practical for 5-15 agents in current implementations
- LbMAS uses "relatively few predefined agent types" — broader agent pools need additional arbitration sophistication `[PEER]`
- Blackboard read contention becomes significant beyond ~10 concurrent readers

**Token overhead:** Lower than naive multi-agent because shared context replaces per-agent context duplication. AFlow (autonomous alternative) requires 16.7M tokens for MATH; LbMAS achieves comparable results at 4.7M tokens — 72% token reduction. `[PEER]`

**Source:** [LbMAS arXiv 2510.01285](https://arxiv.org/abs/2510.01285) `[PEER]`; [Exploring LLM Multi-Agent Blackboard arXiv 2507.01701](https://arxiv.org/abs/2507.01701) `[PEER]`

---

### Pattern 11: Event-Driven / Pub-Sub

**Structure:** Agents operate as reactive components subscribing to event streams. When an event of interest arrives, an agent activates, processes it, and emits new events. Backend is an append-only event log (Kafka, RabbitMQ, Redis Streams). Agents are temporally decoupled — no synchronous call/response.

**Infrastructure stack in production:**
- Message broker: Apache Kafka, RabbitMQ, Redis Streams (sub-millisecond pub/sub latency)
- Event sourcing: append-only log enables event replay for debugging
- Service discovery: distributed config stores (etcd, Consul) for dynamic agent registration
- Frameworks: AutoGen + Kafka for CEP pipelines; Knative Eventing for serverless agent triggers

**Strengths:**
- Temporal decoupling: producer agents never wait for consumer agents — emit and proceed
- Scalability: consumer agents scale independently via partition assignment
- Resilience: event replay enables deterministic failure recovery
- Real-time responsiveness: sub-millisecond message routing (Redis Streams)
- Loose coupling: adding new agents requires only subscribing to existing topics, not modifying producers
- Enables integration with existing event-driven infrastructure without re-architecting data flows

**Failure modes:**
- Infrastructure complexity: requires separate message broker deployment and operations
- Event ordering: out-of-order event delivery corrupts stateful agent behavior without careful sequence numbering
- Exactly-once semantics: difficult to guarantee; duplicate event processing requires idempotent agents
- Observability gap: distributed async execution is significantly harder to debug than synchronous patterns
- Context fragmentation: each event-triggered activation is stateless by default; state reconstruction from event log is expensive

**Scale limits:**
- Scales essentially horizontally (add consumer partitions, add agents) — highest ceiling of all patterns
- Agent state management becomes the binding constraint at scale, not message throughput
- Kafka supports millions of events/sec; LLM inference throughput is the practical bottleneck

**Token overhead:** Minimal per-event overhead; each agent activation is a fresh bounded context. Total token cost depends on activation frequency, not agent count. No cross-agent context sharing means no redundant token consumption. `[PRAC]`

**Source:** [Redis AI Agent Orchestration](https://redis.io/blog/ai-agent-orchestration/) `[PRAC]`; [Boundary ML: Event-Driven Agentic Loops](https://boundaryml.com/podcast/2025-11-05-event-driven-agents) `[PRAC]`; [Knative Event-Driven Agents](https://knative.dev/blog/articles/knative-eventing-eda-agents/) `[PRAC]`; [LLM CEP Pipeline arXiv 2501.00906](https://arxiv.org/html/2501.00906v1) `[PEER]`

---

## Part 2: Why DAGs Fail for LLM Agents

> Note: the 2026-03-30 research covers this in depth. This section adds specificity and additional sources.

### The Core Structural Problem

A DAG (Directed Acyclic Graph) assumes that a complete, correct dependency graph can be specified upfront and executed without modification. Four properties of LLMs make this assumption fail:

**1. No working memory independent of context window `[PEER]`**
LLMs have no internal state separate from their context window. Research (arXiv 2505.10571) confirms: performance on working-memory tasks correlates with context window size, not genuine internal state. GPT-4o's smaller variant failed all 200 working-memory trials. The implication: LLMs cannot hold the mental model required to reliably plan and commit to a full dependency graph upfront — the graph planning itself degrades as the planned graph grows.

**2. Step-wise greedy reasoning policy `[PEER]`**
LLMs are formally equivalent to step-wise greedy policy generators. arXiv 2601.22311 formally proves that step-wise greedy policies "achieve arbitrarily poor long-horizon performance" even when optimal actions exist. A DAG plan requires the planner to propagate downstream value backward to earlier decisions — exactly what greedy reasoners cannot do.

**3. Context window degradation at ~2-3 steps `[PEER]`**
arXiv 2509.09677 documents a 39% average multi-turn performance drop across all frontier LLMs. The planning horizon limit is not a prompt engineering problem — it is structural. DAG generation for even moderately complex graphs (10+ nodes) puts the LLM well past its reliable planning horizon.

**4. Acyclicity prevents feedback loops `[STRUCTURAL]`**
DAGs are acyclic by definition. Any retry, critic cycle, or self-improvement pass requires cyclic structure. Multi-agent systems that require quality iteration (the majority of non-trivial production tasks) cannot be represented in a DAG without violating the acyclic constraint. When LLMs act as DAG routers, "acyclic graphs can become cyclic, which brings challenges that don't exist in traditional directed acyclic workflows." `[PRAC]`

### Specific DAG Failure Modes

| Failure Mode | Description | Source |
|---|---|---|
| Upfront commitment brittleness | Planning error at node 1 propagates through entire graph; no mid-execution correction | `[PEER]` |
| JSON output requirement | DAG nodes must produce structured outputs for dependency passing; streaming and unstructured text incompatible | `[PRAC]` |
| Fan-in context overflow | Synthesis nodes receiving outputs from many parallel branches overflow context | `[PEER]` |
| Working memory exhaustion | LLM cannot maintain awareness of graph state across many nodes | `[PEER]` |
| Cycle prohibition | Cannot represent self-improvement loops, retries, or critic cycles | `[STRUCTURAL]` |
| Cognitive horizon limit | Full upfront graph generation fails at planning horizons LLMs cannot sustain | `[PEER]` |

### When DAG Is the Right Answer

DAG is most powerful at the infrastructure/serving layer — where a deterministic engine (not an LLM) handles scheduling and LLMs are the computation nodes, not the schedulers:

- **LLMCompiler (ICML 2024):** deterministic DAG executor, LLMs as nodes → 1.8× latency speedup, 3.37× cost reduction on HotpotQA `[PEER]`
- **Flash-Searcher (2025):** DAG-based parallel web search → 35% step reduction, ~65% execution time reduction, 82.5% on GAIA `[PEER]`

The winning architecture: **LLM planner → emit structured dependency specification → deterministic engine executes the DAG**. Never ask an LLM to both generate and execute the full DAG within a single context.

---

## Part 3: Why Swarms Fail

> Note: the 2026-03-30 research covers the headline statistics (Galileo 60%→25%, TheAgentCompany 30.3%). This section adds empirical depth and additional failure mechanisms.

### Definition Problem

"Swarm" in LLM context has no consistent definition. In robotics/biology, swarms exhibit emergent coordination from local rules without central control. In LLM frameworks (OpenAI Swarm, CrewAI, AutoGPT), "swarm" means one of:
- A supervisor routing to subagents (1990s workflow engine with LLM nodes)
- A collection of agents without explicit coordination (pure chaos)
- A peer-to-peer network of agents communicating directly

True emergent swarm behavior — coordination arising from local interactions without centralized scripting — has been demonstrated only in constrained research settings with heavy prompt scaffolding. `[PRAC]`

### Empirical Evidence Against Swarm Reliability

**Error amplification (Google DeepMind, Dec 2025):**
180 configurations × 5 agent architectures × 3 LLM families. Finding: unstructured multi-agent networks amplify errors **17.2× compared to single-agent baselines**. Multi-agent systems degrade sequential tasks by 39-70%. `[PRAC/PROD]`

**Reliability multiplication (mathematical):**
If each agent has a 95% success rate:
- 2 sequential agents: 90.25% system reliability
- 3 agents: 85.7%
- 5 agents: 77.4%
- 10 agents: 59.9%

No swarm framework provides automatic error correction at handoff boundaries. `[PRAC]`

**Production failure rate:**
40% of multi-agent pilots fail within six months of production deployment. Gartner (2025): over 40% of agentic AI projects will be canceled by end of 2027. `[PROD]`

**Real-task ceiling:**
Claude Sonnet 4 with OpenHands: 7.5% on ACE-Bench (end-to-end feature development) vs 70.4% on SWE-Bench (isolated bug fixes) — **10× performance drop** when moving from isolated tasks to integrated real-world work. `[PRAC]`

**Enterprise scaling:**
78% AI adoption reported, but fewer than 10% of enterprises successfully scale multi-agent systems. `[PROD]` (McKinsey 2025)

### The Coordination Overhead Problem

Peer-to-peer swarms introduce N² communication overhead. For N=10 agents: 90 potential communication pairs. Each coordination message is an LLM call. The coordination cost overwhelms the computational value of the distributed work.

**Concrete production failure modes:**
- **Context state management:** A financial services firm lost $2M in duplicate processing due to poor agent state management `[PROD]`
- **Customer-facing handoffs:** An e-commerce platform saw 40% cart abandonment when swarm agent transitions confused customers `[PROD]`
- **Over-engineering:** A major retailer spent 18 months building a perfect swarm system that was obsolete on launch `[PROD]`

### What Ships as "Swarm" Is Actually Supervisor-Worker

Production deployments labeled as "swarm" architectures consistently show, on inspection, a supervisor routing to subagents — exactly the orchestrator-worker (wave) pattern. Pure peer-to-peer swarm coordination without a central orchestrator is not reliably deployable with current LLMs. The winning production pattern is hybrid: **high-level orchestrator for strategic coordination + local mesh for tactical execution** within bounded subsets. `[PROD]`

---

## Part 4: Benchmark Survey 2025-2026

### SWE-bench (Software Engineering Tasks)

**What it measures:** Real GitHub issues across open-source Python repositories. Success = agent correctly resolves the issue with a valid patch.

**Current top scores (SWE-bench Verified, early 2026):**

| System | % Resolved | Architecture | Cost/instance |
|---|---|---|---|
| Claude 4.5 Opus (high reasoning) | 76.8% | Single agent | $0.75 |
| Gemini 3 Flash (high reasoning) | 75.8% | Single agent | $0.36 |
| MiniMax M2.5 (high reasoning) | ~75%+ | Single agent | $0.07 |
| Anthropic submission | 73.20% | Multi-agent pipeline | N/A |
| ByteDance (prior top) | 75.2% | Multi-agent | N/A |

**Architecture observations:**
- No single workflow dominates; high-performing systems blend retrieval, orchestration, and self-critique
- Three dominant approaches: (1) agentless/fixed pipelines, (2) SWE-Agent-style emergent multi-turn, (3) hybrid ensembling/LLM-as-judge
- Industry (small + large public companies) accounts for majority of top submissions; academic and solo-developer efforts remain competitive but less prevalent at top ranks
- IBM iSWE-Agent: #1 and #2 on Multi-SWE-Bench Java category (33% and 31% of Java issues resolved) `[PEER]`

**Key finding:** Current frontier single-agent systems match or exceed most multi-agent pipelines on SWE-bench. Complexity does not automatically improve scores.

**Source:** [SWE-bench Leaderboard](https://www.swebench.com/) — live; [Dissecting SWE-Bench Leaderboards arXiv 2506.17208](https://arxiv.org/html/2506.17208v2) `[PEER]`; [Epoch AI SWE-bench Verified](https://epoch.ai/benchmarks/swe-bench-verified) `[PRAC]`

---

### GAIA (General AI Assistants)

**What it measures:** 450 questions requiring multi-modal reasoning, web browsing, tool use, and multi-step reasoning. 3 difficulty levels. Designed to be easy for humans, hard for AI.

**Current scores (GAIA test set, early 2026):**

| System | Overall Score | Notes |
|---|---|---|
| H2O.ai h2oGPTe Agent | 75% | First to achieve "C grade" on GAIA test set |
| Flash-Searcher (DAG web search) | 82.5% | Level 1/2 only; specialized web search agent |
| Gradientsys (ReAct orchestration) | 24.1% | Multi-agent scheduler baseline comparison |
| Gradientsys baseline | 15.0% | Reference point |

**Gaia2 (dynamic/async environments, 2025 release):**

| System | Pass@1 | Notes |
|---|---|---|
| GPT-5 (high) | 42% | Strongest overall; fails on time-sensitive tasks |
| Claude-4 Sonnet | Lower | Trades accuracy/speed for cost |
| Kimi-K2 | 21% | Top open-source |
| ERL (Experiential Reflective Learning) | 56.1% | +7.8% over ReAct baseline |

**Architecture finding:** ERL's memory-augmented ReAct (heuristic pool with relevance scoring) outperforms Reflexion and AutoGuide on Gaia2, suggesting that persistent external memory for strategy patterns matters more than in-context reflection. `[PEER]`

**Source:** [GAIA HuggingFace Leaderboard](https://huggingface.co/spaces/gaia-benchmark/leaderboard) — live; [H2O.ai GAIA result](https://h2o.ai/blog/2025/h2o-ai-tops-the-general-ai-assistant-test/) `[PRAC]`; [ERL arXiv 2603.24639](https://arxiv.org/html/2603.24639) `[PEER]`

---

### AgentBench (Multi-Environment Agent Evaluation)

**What it measures:** 8 diverse environments: OS, database, knowledge graph, digital card game, lateral thinking puzzle, house-holding, web shopping, web browsing.

**Key finding:** Analysis of 1,642 multi-agent system execution traces found **41-86.7% failure rates** on state-of-the-art open-source systems. This is the widest failure-rate range published on a multi-environment benchmark. `[PEER]`

**Architecture finding:** Agents fail hardest on tasks requiring coordinated state across multiple environments. Single-environment specialists outperform generalist agents significantly.

**Source:** [AgentBench arXiv 2308.03688 / ICLR 2024](https://arxiv.org/abs/2308.03688) `[PEER]`; recent trace analysis cited in sequential pattern research `[PEER]`

---

### HumanEval (Code Generation)

**What it measures:** 164 programming problems. pass@k metric: probability of generating a correct solution within k attempts.

**Key architecture scores:**

| System | pass@1 | Notes |
|---|---|---|
| LATS + GPT-4 | 94.4% | ICML 2024; MCTS-based tree search `[PEER]` |
| Reflection + verification | ~91% | Single-agent with self-critique (from 80%) `[PRAC]` |
| MAR (Multi-Agent Reflexion) | 82.6% | Multi-agent Reflexion (+6.2 vs baseline 76.4) `[PEER]` |
| Standard ReAct baseline | ~76-80% | Frontier model dependent |

**Architecture finding:** LATS's 94.4% is exceptional but requires enormous token cost (MCTS exploration). For production code generation, reflection loops with external verification offer the best accuracy/cost tradeoff. `[PEER]`

**Source:** [LATS arXiv 2310.04406 / ICML 2024](https://arxiv.org/abs/2310.04406) `[PEER]`; [MAR arXiv 2512.20845](https://arxiv.org/html/2512.20845) `[PEER]`

---

### WebArena (Web Navigation)

**What it measures:** Realistic web automation tasks across e-commerce, social forum, software development, content management. Fully self-contained reproducible environments.

**Current scores:**
- Gemini 2.5 Pro: **54.8%** — current top performance on WebArena `[PRAC]`
- WebChoreArena extension (2025): introduces 532 tasks emphasizing massive memory and cross-page reasoning; current best agents score significantly lower than on base WebArena

**Architecture finding:** Cross-page, long-horizon web tasks (WebChoreArena) expose severe failure modes in current ReAct agents. Multi-step web tasks requiring state across 10+ page visits are effectively unsolved. `[PRAC]`

**Source:** [WebArena site](https://webarena.dev/) — live; [o-mega.ai agent benchmarks 2025-2026](https://o-mega.ai/articles/the-2025-2026-guide-to-ai-computer-use-benchmarks-and-top-ai-agents) `[PRAC]`

---

### OSWorld (Computer Use / GUI Agents)

**What it measures:** 369 computer tasks in real desktop environments: web apps, native apps, file I/O, multi-app workflows. Multimodal (screen observation + action generation).

**Current scores:**

| System | Success Rate | Notes |
|---|---|---|
| OSAgent | 76.26% (274/360) | Surpasses ~72% human baseline |
| Claude Opus 4.6 | 72.7% | Anthropic; highest model-only score |
| Agent S2 + Claude 3.7 | 34.5% | Prior state-of-the-art (Feb 2025) |
| Claude 3.7 solo | 28% | 100-step limit |
| ARPO (RL-based) | 29.9% | End-to-end RL via Group Relative Policy Optimization |
| Agent S + GPT-4o | 20.58% | Experience-augmented hierarchical planning |

**Architecture finding:** OSAgent's self-verification loop (continuously checks and corrects its own actions in real time) drives the 76.26% top score. This is actor-critic at the tool-use level. Experience-augmented hierarchical planning (Agent S) outperforms flat ReAct significantly (20.58% vs ~15% baseline). `[PRAC]`

**Source:** [OSWorld Leaderboard](https://llm-stats.com/benchmarks/osworld) — live; [OSWorld site](https://os-world.github.io/) `[PEER]`; [o-mega.ai 2025-2026 computer-use guide](https://o-mega.ai/articles/the-2025-2026-guide-to-ai-computer-use-benchmarks-and-top-ai-agents) `[PRAC]`

---

## Part 5: Recommended Patterns as of Early 2026

### Synthesis: What the Evidence Shows

The empirical literature converges on several consistent findings:

**1. Hierarchical supervisor-worker is the production workhorse.** It achieves the best cost-accuracy tradeoff across the widest range of task types (98.5% of reflexive F1 at 60.7% of cost). It is the dominant pattern in the top SWE-bench submissions. `[PEER]`

**2. Reflexive/self-critique loops are best for accuracy-critical low-volume tasks.** Highest F1 and accuracy scores, but highest cost and worst scalability. Use for legal, compliance, financial reporting — not for high-throughput pipelines. `[PEER]`

**3. Sequential pipelines are underrated for well-defined deterministic workflows.** Lowest cost, most debuggable, most resilient at scale. The right first choice before adding orchestration complexity. `[PEER/PRAC]`

**4. ReAct is the right base for interactive/adaptive single-agent tasks.** More reliable under stress than Reflexion (2.5% higher, 80.9% vs 67.3% fault recovery). Better fault tolerance through simpler retry logic. `[PEER]`

**5. Plan-and-Execute beats ReAct for long-horizon structured tasks.** 92% vs 85% completion, 3.6× speedup. Use when the task decomposition is knowable upfront. `[PRAC]`

**6. LATS for accuracy-critical, token-budget-unconstrained tasks.** 94.4% HumanEval pass@1 — the ceiling for code generation accuracy. Reserved for tasks where correctness is worth the MCTS token overhead. `[PEER]`

**7. Blackboard for heterogeneous, evolving-capability problems.** 13-57% improvement over strong baselines. Best for data science, research synthesis, and problems where the right agent combination is not known at design time. `[PEER]`

**8. Event-driven for real-time, always-on, loosely coupled systems.** Horizontal scale ceiling exceeds all synchronous patterns. Required for high-throughput monitoring, streaming data pipelines, and integration with existing event infrastructure. `[PRAC]`

**9. Code-based orchestration beats LLM-driven orchestration for predictability.** "Code-based orchestration makes tasks more deterministic and predictable in terms of speed, cost and performance compared to LLM-driven approaches." Start with code-based flow; introduce LLM routing only where classification is genuinely needed. `[PRAC]`

**10. Avoid full swarm (pure peer-to-peer without central coordination).** 17.2× error amplification, 40% production failure rate, <10% enterprise scaling success. What ships as "swarm" in production is supervisor-worker with marketing rebranding. `[PRAC/PROD]`

### Pattern Selection Decision Tree (2026)

```
Is the task well-decomposed into known sequential steps?
  YES → Sequential Pipeline (lowest cost, most debuggable)
  NO → continue

Is latency the primary constraint?
  YES → Parallel Fan-Out (wave orchestration)
  NO → continue

Is accuracy the primary constraint (low volume, high stakes)?
  YES → Reflexive Self-Correcting Loop (or LATS for code)
  NO → continue

Does the task require adaptive decision-making with tool use?
  YES + short horizon → ReAct
  YES + long horizon → Plan-and-Execute

Does the task span multiple domains with distinct specialist expertise?
  YES → Hierarchical Orchestration (or Router/Dispatcher for intake)
  NO → continue

Are agent capabilities heterogeneous and not fully known at design time?
  YES → Blackboard Architecture
  NO → continue

Does the task require real-time response to external events?
  YES → Event-Driven / Pub-Sub
  NO → default to Sequential or Parallel Fan-Out
```

### Framework Recommendations (Early 2026)

| Framework | Pattern | Verdict |
|---|---|---|
| **LangGraph** | DAG + cycles | Most technically rigorous; production-grade state management; API instability is a real tax |
| **OpenAI Agents SDK** (Mar 2025) | Handoff-based | Clean handoff primitives; built-in guardrails and tracing; best for explicit delegation chains |
| **Google ADK** (Apr 2025) | Hierarchical + patterns | Native A2A protocol for cross-framework agent communication; tight Vertex AI integration |
| **Microsoft Agent Framework** (late 2025) | Graph-based + AutoGen | Enterprise features; Magnetic One pattern; graph-based workflows with checkpointing |
| **PydanticAI** | Single-agent / simple handoffs | Fastest of tested frameworks; type-safe; best for constrained, well-defined pipelines |
| **CrewAI** | Role-based waves | Intuitive for structured delegation; poor debugging story; loop/cost risks require manual guardrails |
| **LLMCompiler** | DAG (deterministic executor) | Best when dependency graph is static and known — not LLM-generated |

**Avoid:** AutoGPT (production anti-pattern), BabyAGI (proof-of-concept only), pure swarm architectures without central coordination.

---

## Summary Table: All Patterns at a Glance

| Pattern | Best For | Scale Limit | Token Overhead | Peer-Reviewed Evidence? |
|---|---|---|---|---|
| Sequential Pipeline | Deterministic multi-step workflows | ~5 agents before compounding | Lowest | Yes — arXiv 2603.22651 |
| Parallel Fan-Out | Independent parallel analysis, latency reduction | ~10 concurrent (Claude Code hard cap) | 4× chat per subagent | Yes — arXiv 2603.22651 |
| Hierarchical | 20+ agent, multi-domain, context overflow | 3-4 levels practical | Moderate; targeted extraction | Yes — arXiv 2603.22651 |
| Router/Dispatcher | Multi-specialist intake, intent routing | ~20 specialists before routing degrades | Minimal (+1 LLM call) | No (practitioner consensus) |
| ReAct | Interactive adaptive single-agent | ~10 tool calls per session | Medium (2K-3K tokens/task) | Yes — arXiv 2601.06112, 2507.06520 |
| Plan-and-Execute | Long-horizon structured tasks | ~15 plan steps | Higher than ReAct (3K-4.5K) | Partial — practitioner + arXiv 2509.08646 |
| Reflection/Self-Critique | Accuracy-critical, low volume | <25K ops/day | Highest absolute | Yes — arXiv 2603.22651, 2512.20845 |
| LATS | Code gen, QA — accuracy ceiling | Depth ×3, branching ×3 | Very high (MCTS multiplier) | Yes — arXiv 2310.04406 ICML 2024 |
| Actor-Critic | Adversarial quality validation | 2-3 critic pairs | ~2× ReAct per cycle | Yes — arXiv 2311.13884, 2503.16024 |
| Blackboard | Heterogeneous evolving agents, data science | ~10-15 agents (arbiter bottleneck) | Lower than naive multi-agent | Yes — arXiv 2510.01285, 2507.01701 |
| Event-Driven | Real-time, always-on, external event integration | Horizontal (LLM inference is binding) | Minimal per-event | Partial — arXiv 2501.00906 + PRAC |

---

*Research completed: 2026-03-31 | Methodology: Parallel web search + direct URL fetch of primary sources. Peer-reviewed evidence (arXiv, ICML, NeurIPS, Nature) distinguished from practitioner/community evidence throughout.*

*Predecessor document with Wave, Mesh, Framework Verdicts, and Claude Code capability details: `_bmad-output/planning-artifacts/research/technical-subagent-orchestration-research-2026-03-30.md`*
