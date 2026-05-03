---
content_origin: web-research
date: 2026-05-02
topic: "TeamCreate Real-World Usage Patterns"
sub_question: "Decision framework and benchmarks: TeamCreate vs fan-out"
---

# Decision Framework and Benchmarks: TeamCreate vs Fan-Out

## Summary

The core decision criterion is **whether parallel workers need to communicate with each other during execution**. If yes, use agent teams (TeamCreate + SendMessage). If no, use fan-out subagents. This rule, stated explicitly in Anthropic's official Claude Code docs, is corroborated by academic research and practitioner reports — though the actual picture is more nuanced because agent teams carry significant overhead, known bugs in the experimental feature, and production failure modes that make the theoretical value harder to capture in practice.

---

## 1. The Official Anthropic Distinction

From the [official Claude Code agent teams docs](https://code.claude.com/docs/en/agent-teams):

| Dimension | Subagents (fan-out) | Agent Teams (TeamCreate) |
|---|---|---|
| Context | Own context window; results return to caller | Own context window; fully independent |
| Communication | Report results to main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| Token cost | Lower: results summarized back to main context | Higher: each teammate is a separate Claude instance |

The docs identify agent teams as most effective for:
- **Research and review** — multiple teammates investigate different aspects simultaneously, then share and challenge findings
- **New modules or features** — teammates each own a separate piece without file conflicts
- **Debugging with competing hypotheses** — teammates test different theories in parallel and converge faster
- **Cross-layer coordination** — changes spanning frontend, backend, and tests

Agent teams are explicitly not recommended for: sequential tasks, same-file edits, or work with many dependencies. For those, a single session or subagents are more effective.

The docs also state: "Agent teams use approximately **7x more tokens** than standard sessions when teammates run in plan mode."

Recommended team size: 3–5 teammates. Beyond 4–5 active agents, coordination overhead and file conflict risk grow faster than productivity gains.

---

## 2. Practitioner Decision Frameworks

### 2a. The Core Heuristic

The most cited practitioner heuristic (appearing across [Charles Jones](https://charlesjones.dev/blog/claude-code-agent-teams-vs-subagents-parallel-development), [LaoZhang AI](https://blog.laozhang.ai/en/posts/claude-code-agent-teams), [knightli.com](https://www.knightli.com/en/2026/04/22/claude-code-subagents-vs-agent-teams/), and [MindStudio](https://www.mindstudio.ai/blog/claude-code-agent-teams-vs-sub-agents)):

> **"If you can describe each worker's task without referencing other workers, use subagents."**

### 2b. Full Decision Tree

**Choose fan-out subagents when:**
- Tasks decompose into truly independent units (research across sources, tests for separate components)
- Output is "bring me the result" — no peer deliberation needed
- Pipeline is short (3 or fewer stages)
- Sequential reasoning dominates (each step depends on full prior context)
- Budget is primary constraint
- Full auditability required (single orchestrator trace)
- Task decomposition is dynamic or unpredictable mid-execution

**Choose agent teams (TeamCreate) when:**
- Workers need to share findings, challenge each other's hypotheses, or negotiate interfaces
- Parallel tracks must agree on contracts before or during implementation (e.g., frontend/backend API shape)
- Adversarial/debate structure is the mechanism (competing theories for debugging)
- Cross-cutting concerns require ongoing coordination (not just a handoff at the end)
- Work spans 10+ semi-independent tasks where orchestrator context accumulation would become prohibitive

**Choose a single session when:**
- Tasks are sequential
- Work involves repeated edits to the same file
- Task complexity is low enough that multi-agent coordination overhead exceeds benefit
- Baseline single-agent performance already exceeds ~45% accuracy (see Section 4)

### 2c. The OAuth Case Study (Charles Jones)

Agent teams completed an OAuth implementation feature in roughly **half the wall-clock time** of a subagent workflow. The key efficiency gain: "the frontend and backend matched on the first pass" through direct communication, eliminating typical handoff debugging loops. This is a concrete case where peer messaging provided measurable value over fan-out.

### 2d. Context Accumulation Token Dynamics

[MindStudio](https://www.mindstudio.ai/blog/claude-code-agent-teams-vs-sub-agents) identifies a counterintuitive token cost scenario where fan-out is actually *more expensive* than teams at scale:

- In fan-out, the orchestrator accumulates all subagent outputs into its own context. With 10 subagents producing 2,000 tokens each, the orchestrator holds 20,000+ tokens of accumulated state — paid on every subsequent message.
- In agent teams, no single agent accumulates the full context. Each agent loads only the task it's working on.
- **For large pipelines (10+ agents producing substantial output), agent teams estimated as 3–5x cheaper in token costs** than fan-out due to this accumulation effect.
- **For small pipelines (2–4 agents)**: negligible difference.
- **For medium pipelines (5–10 agents)**: orchestrator can hit 30–50k tokens by synthesis — real cost impact.

This reversal of the token cost intuition depends on pipeline size and output volume. The "7x more expensive" figure from Anthropic's docs applies when comparing plan-mode agent team costs to a single standard session, not comparing teams to equivalent fan-out orchestrator patterns at scale.

---

## 3. Real-World Cost Analysis (Verified Scenarios)

From [LaoZhang AI blog](https://blog.laozhang.ai/en/posts/claude-code-agent-teams) using Opus 4.6 lead + Sonnet 4.5 teammates:

| Scenario | Single Session | Agent Team | Multiplier | Notes |
|---|---|---|---|---|
| Parallel code review (3 reviewers, 30 min) | ~$2.00 | ~$4.50 | 2.25x | Simultaneous lenses |
| Full-stack feature (frontend + backend + tests, 2h) | $8–15 | ~$20 | 2.5–3x | Compresses 4–6 sequential hours → 90 min |
| Complex debugging (3 investigators, 1h) | ~$10 | ~$13 | 1.3x | Significant wall-clock compression |

**Anthropic's own internal validation**: Built an entire C compiler using 16 agent teams across ~2,000 sessions, producing 100,000 lines of Rust. Total cost: ~$20,000 (approximately 2 billion input tokens and 140 million output tokens).

Enterprise teams report subagent costs running 300–500% higher than expected due to parallel context windows — a reminder that "cheaper fan-out" assumptions need empirical validation per workflow.

---

## 4. Academic and Research Benchmarks

### 4a. Google Research: Scaling Agent Systems (arXiv:2512.08296)

Source: [Towards a Science of Scaling Agent Systems](https://arxiv.org/html/2512.08296v1)

This is the most rigorous quantitative study found. Key findings:

**Performance by task type:**
- Finance (parallelizable): Centralized coordination +80.9% over single-agent; decentralized +74.5%
- Planning (sequential): All multi-agent variants degraded by **39–70%**. Centralized dropped to -50.4%.
- Web navigation: Decentralized +9.2%; centralized essentially flat (+0.2%)
- Tool-heavy workflows: Independent agents amplify errors **17.2x**; centralized contains this to **4.4x**

**Critical threshold (quantitative):**
> "Tasks where single-agent performance already exceeds 45% accuracy experience negative returns from additional agents" (β = -0.408, p < 0.001)

This means multi-agent coordination is wasteful — not just neutral — when the task is already tractable for a single agent.

**Predictive model** achieves 87% accuracy identifying optimal architecture using just two measurable properties: task decomposability and tool count (R² = 0.513).

**Architecture selection rules from the model:**
- Planning tasks (≤4 tools, PSA ≈ 0.57): single-agent
- Analysis tasks (~5 tools, PSA ≈ 0.35): centralized (error control via orchestrator)
- Tool-heavy tasks (16 tools, PSA ≈ 0.63): decentralized despite 263% overhead, due to parallelization benefits

**Error amplification note**: Independent (fully decentralized peer-to-peer without orchestrator validation) systems amplify errors 17.2x. This is the "pure mesh" failure mode. Centralized hub-and-spoke contains this to 4.4x. Agent teams in Claude Code are a hybrid — peers communicate, but the lead still coordinates — which likely falls between these extremes.

### 4b. Financial Document Processing Benchmark (arXiv:2603.22651)

Source: [Benchmarking Multi-Agent LLM Architectures](https://arxiv.org/html/2603.22651) — 10,000 SEC filings

| Architecture | F1 Score | Cost/Doc | Latency (median) |
|---|---|---|---|
| Sequential | 0.903 | $0.187 | 38.7s |
| Parallel (fan-out) | 0.914 | $0.221 | 21.3s |
| Hierarchical | 0.929 | $0.261 | 46.2s |
| Reflexive (peer-to-peer loops) | 0.943 | $0.430 | 74.1s |

**Key finding**: Hierarchical achieves 98.5% of reflexive F1 at 60.7% of the cost. Peer-to-peer (reflexive) is highest quality but 2.3x more expensive per document.

**At scale (100K docs/day)**: Reflexive F1 degrades sharply (-0.072 from baseline). Sequential degrades least (-0.017). Peer-to-peer architectures do not scale as cleanly as hierarchical ones.

**Practical recommendation**: Hierarchical fan-out for production volume. Peer-to-peer only for low-volume, accuracy-critical workloads.

### 4c. Multi-Agent vs Single LLM Orchestration (arXiv:2509.23537)

Source: [Beyond the Strongest LLM](https://arxiv.org/abs/2509.23537)

Multi-turn orchestration between multiple LLM agents "matches or exceeds the strongest single model and consistently outperforms the others" across GPQA-Diamond, IFEval, and MuSR benchmarks. However:
- Authorship visibility (agents knowing who proposed what) increased self-voting and tied outcomes
- Vote visibility amplified herding — faster convergence but sometimes premature consensus
- Current coordination mechanisms haven't reached their quality ceiling

### 4d. Anthropic Multi-Agent Research System

Source: [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)

Anthropic's own production system uses **fan-out** (not peer teams):
- Lead: Claude Opus 4 (orchestrator)
- Workers: Claude Sonnet 4 subagents (parallel investigators)
- Pattern: orchestrator spawns → subagents investigate independently → results synthesized

Performance: Multi-agent (Opus lead + Sonnet subagents) outperformed single-agent Opus by **90.2%** on internal research evaluations. Parallel tool calling reduced research time by **up to 90%** for complex queries.

**Token cost**: approximately **15x more tokens** than standard chat interactions.

This is significant: Anthropic's own flagship multi-agent system chose fan-out over peer teams for production research tasks.

### 4e. Coordination Overhead Scaling

From [Multi-Agent Collaboration Mechanisms survey](https://arxiv.org/html/2501.06322v1):
- Coordination overhead grows **superlinearly** with agent count: O(n^1.4 to n^2.1)
- 68% of published multi-agent systems lack efficiency reporting
- Graph-based protocols (peer-to-peer) achieve best task performance but similar token usage to star (hub-and-spoke) protocols — the "peer" benefit is quality, not cost

---

## 5. Production Failure Modes of Agent Teams (Claude Code Specific)

These are bugs and limitations of the current experimental Claude Code implementation that narrow the practical applicability of TeamCreate:

### 5a. SendMessage Not Available in Subagents (Issue #48160)

Source: [GitHub issue #48160](https://github.com/anthropics/claude-code/issues/48160)

Subagents spawned under `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` cannot originate `SendMessage` calls. The tool is asymmetric: the parent can send to named agents, but spawned agents cannot send back. This defeats the core peer-to-peer premise of agent teams. The workaround (parent manually relays messages) doubles cost and wall-clock time. Status: **closed as duplicate** — unfixed as of the report date.

### 5b. Cold-Start Messaging Failure (Issue #28075)

Source: [GitHub issue #28075](https://github.com/anthropics/claude-code/issues/28075)

The idle-nudge system (3 nudges → agent goes dormant) does not distinguish "waiting for a peer message" from "nothing to do." Agents time out and go dormant before messages from peers arrive. Controlled experiments showed:

| Model | Cold-Start Delay | Result |
|---|---|---|
| Opus 200K | ~32s | Timed out, ACK arrived after dormancy |
| Sonnet 1M | ~9s delivery; 42s of checking | Timed out despite message waiting since second 14 |
| Haiku 4.5 | Fastest model = fastest timeout (~8s) | |

Warm-state messaging is reliable (0–13s per hop). The problem is exclusively getting both agents warm simultaneously. A "lead keepalive" workaround (periodic nudges every ~10s) works but wastes tokens. Status: **closed as not planned**.

### 5c. SDK/Headless Incompatibility (Issue #1124)

Source: [claude-code-action issue #1124](https://github.com/anthropics/claude-code-action/issues/1124)

Agent teams do not work in headless/SDK mode or the VS Code extension. The session lifecycle model requires interactive terminal sessions. Any automated pipeline (CI/CD, GitHub Actions) cannot use TeamCreate.

### 5d. No Session Resumption

`/resume` and `/rewind` do not restore in-process teammates. After resuming a session, the lead may attempt to message teammates that no longer exist. Long-running team workflows cannot be interrupted and resumed.

### 5e. Broadcast Doesn't Scale

From [Feature request #30140](https://github.com/anthropics/claude-code/issues/30140): Current SendMessage is push-based and ephemeral with no persistence or ordering guarantees. With 8+ agents, broadcast becomes chaotic — N agents × M messages arrive out of order. Practical cap on useful team sizes is approximately 3–5 agents.

---

## 6. What Production Teams Have Learned ("What Survived" — 2026)

Source: [Multi-Agent in Production in 2026](https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1)

**Hub-and-spoke orchestration** (fan-out) emerged as the dominant production winner. Anthropic Research's 90.2% gain over single-agent using lead + 3–5 parallel subagents is a widely replicated result.

**Peer collaboration teams** — the "romantic vision" — largely failed in open form. Surviving implementations use hidden selectors, phase gates, or final arbiters — essentially *bounded collaboration within supervisor architectures* rather than true mesh systems.

**Three foundational failure studies cited:**
1. MIT: Adding relay stages without new signals collapsed accuracy from 90.7% to 22.5% across five stages. "Without new exogenous signals, multi-agent DAGs are dominated by centralized decision-makers."
2. "From Spark to Fire" cascade study: Hub injection produced 100% system-wide failure vs. 9.7% from leaf-node failures.
3. Google 2026 scaling study: Multi-agent degraded sequential planning by 39–70%; independent agents amplified errors 17.2x vs. 4.4x for centralized.

**Five production rules that survived:**
1. Start with a single strong agent
2. Specialists must contribute genuinely new information (not just route)
3. Budget for approximately 15x token consumption vs. single-agent
4. Match topology to task shape, not organizational structure
5. Bound collaboration with protocols and observability mechanisms

---

## 7. Architecture Pattern Taxonomy (2026)

Source: [Agent Architecture Patterns: 2026 Taxonomy Guide](https://www.digitalapplied.com/blog/agent-architecture-patterns-taxonomy-2026)

The five primary patterns, ranked by coordination complexity:

1. **Pipeline** — sequential stage-based. Lowest overhead, best for well-defined workflows.
2. **Orchestrator-Worker (fan-out)** — centralized control, parallel workers. Dominant production pattern.
3. **Hierarchical** — tree-structured delegation. Best cost-accuracy tradeoff for volume.
4. **Swarm** — emergent decentralized coordination. High theoretical scalability, N² connection growth.
5. **Mesh (peer-to-peer)** — direct agent-to-agent communication. Best for tightly coupled small teams.

TeamCreate in Claude Code implements a **hybrid**: a centralized lead with peer messaging capability among teammates. This is architecturally between Orchestrator-Worker and Mesh. The practical result is it pays coordination overhead of Mesh without reliable delivery (due to the bugs in Section 5).

---

## 8. Synthesized Decision Framework

### Primary Gate

```
Do your parallel workers need to communicate with each other?
├── No → Fan-out subagents
│        └── Can each worker's task be described without referencing other workers?
│            ├── Yes → Subagents (clean fan-out)
│            └── No → Rethink decomposition; sequential may be better
└── Yes → Consider agent teams
          └── Is single-agent baseline performance already above ~45%?
              ├── Yes → Multi-agent likely adds no value; stick with single agent
              └── No → Agent teams may be warranted
```

### Secondary Gate (Task Shape)

| Task Shape | Recommendation |
|---|---|
| Parallelizable, independent (research, review, test generation) | Fan-out subagents |
| Sequential reasoning (planning, dependency chains) | Single agent |
| High tool density (≥10 tools) | Decentralized agents, but monitor error amplification |
| Low volume, accuracy-critical, small team ≤5 | Agent teams viable if peer debate is the mechanism |
| High volume (10K+ iterations), cost-sensitive | Hierarchical fan-out; avoid peer teams |
| CI/CD or SDK pipeline | Fan-out only; TeamCreate is incompatible |

### Quantitative Thresholds

- **Agent count**: Start with 3. Beyond 5, coordination overhead compounds faster than gains.
- **Tasks per agent**: 5–6 keeps agents productive without excessive context switching.
- **Token budget**: Plan for 3–7x a single session (lower end for parallel review; higher for plan-mode teams).
- **Baseline accuracy**: If single agent already exceeds ~45% on the task, multi-agent coordination is net-negative.
- **Pipeline length**: At 10+ semi-independent tasks, fan-out orchestrator context accumulation becomes expensive; teams may be more token-efficient.

---

## 9. Gaps and Caveats

1. **No published head-to-head benchmark specifically comparing TeamCreate vs fan-out for identical tasks in Claude Code.** All data is either architectural analysis, external research on analogous patterns, or practitioner case studies.

2. **Agent teams are experimental** (as of Claude Code v2.1.32+). The feature flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` signals this is not production-ready. The known bugs (Sections 5a–5e) materially limit what peer communication can deliver in practice.

3. **Anthropic's own production system (Section 4d) chose fan-out**, not peer teams, for their flagship multi-agent research workload. This is the strongest practitioner signal available.

4. **Token cost comparisons are pipeline-specific.** The "7x more expensive" claim (plan mode team vs single session) and the "3–5x cheaper" claim (teams vs fan-out at scale) are both valid in different scenarios. Neither is universally true.

5. **Quality improvement from peer debate** (the "competing hypotheses" use case) is the most credible unique value proposition for agent teams. The OAuth case study and code review scenarios are the strongest documented examples. No controlled experiments on this specific mechanism exist yet.

---

## Sources

- [Anthropic: Claude Code Agent Teams Docs](https://code.claude.com/docs/en/agent-teams)
- [Anthropic: Manage Costs Effectively](https://code.claude.com/docs/en/costs)
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic: When to Use Multi-Agent Systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
- [Charles Jones: Agent Teams vs Subagents — When They Beat Each Other](https://charlesjones.dev/blog/claude-code-agent-teams-vs-subagents-parallel-development)
- [LaoZhang AI: Claude Code Agent Teams Practical Guide 2026](https://blog.laozhang.ai/en/posts/claude-code-agent-teams)
- [MindStudio: Agent Teams vs Sub-Agents](https://www.mindstudio.ai/blog/claude-code-agent-teams-vs-sub-agents)
- [knightli.com: Claude Code Subagents vs Agent Teams 2026](https://www.knightli.com/en/2026/04/22/claude-code-subagents-vs-agent-teams/)
- [Medium: Sub-agent vs Agent Team in 60 Seconds](https://medium.com/data-science-collective/sub-agent-vs-agent-team-in-claude-code-pick-the-right-pattern-in-60-seconds-e856e5b4e5cc)
- [Medium: Multi-Agent in Production in 2026 — What Actually Survived](https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1)
- [arXiv:2512.08296 — Towards a Science of Scaling Agent Systems (Google Research)](https://arxiv.org/html/2512.08296v1)
- [arXiv:2603.22651 — Benchmarking Multi-Agent LLM Architectures for Financial Document Processing](https://arxiv.org/html/2603.22651)
- [arXiv:2509.23537 — Beyond the Strongest LLM: Multi-Turn Multi-Agent Orchestration vs Single LLMs](https://arxiv.org/abs/2509.23537)
- [arXiv:2501.06322 — Multi-Agent Collaboration Mechanisms: A Survey of LLMs](https://arxiv.org/abs/2501.06322)
- [GitHub Issue #48160 — Spawned Subagents Cannot Originate SendMessage](https://github.com/anthropics/claude-code/issues/48160)
- [GitHub Issue #28075 — No "Waiting for Peer Message" State in Agent Teams](https://github.com/anthropics/claude-code/issues/28075)
- [GitHub Issue #1124 — Agent Teams Unusable in claude-code-action (SDK)](https://github.com/anthropics/claude-code-action/issues/1124)
- [Agent Architecture Patterns: 2026 Taxonomy Guide](https://www.digitalapplied.com/blog/agent-architecture-patterns-taxonomy-2026)
- [MindStudio: Claude Code Parallel Agents Coordination](https://www.mindstudio.ai/blog/claude-code-agent-teams-parallel-agents)
- [Galileo: Architectures for Multi-Agent Systems](https://galileo.ai/blog/architectures-for-multi-agent-systems)
