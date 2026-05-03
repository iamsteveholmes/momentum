---
title: "TeamCreate Real-World Usage Patterns — Research Report"
date: 2026-05-02
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/research-official-docs-and-sdk.md
    relationship: synthesized_from
  - path: raw/research-real-world-examples.md
    relationship: synthesized_from
  - path: raw/research-decision-framework-and-benchmarks.md
    relationship: synthesized_from
  - path: raw/research-community-sentiment.md
    relationship: synthesized_from
  - path: raw/gemini-output.md
    relationship: synthesized_from
---

# TeamCreate Real-World Usage Patterns — Research Report

## Executive Summary

TeamCreate is an experimental Claude Code feature (shipped with Opus 4.6 on 2026-02-05) that lets a lead session spawn independent teammate sessions which can message each other peer-to-peer via SendMessage. The capability is real, the architecture is sound on paper, and the official guidance is sensible: use teams when workers must communicate during execution, fan-out when they don't.

**The honest verdict from the public record: TeamCreate is currently over-promised and under-delivered for most workflows.** Production examples of true multi-turn agent-to-agent dialogue are nearly absent. The flagship case study most often cited as a TeamCreate validation (Anthropic's C compiler) did not actually use TeamCreate — coordination was git-lock files. Multiple confirmed bugs (subagents can't originate SendMessage, recipient names aren't validated, state wipes on restart, headless/SDK mode is non-functional, permission requests crash the lead) materially limit what peer messaging can deliver in practice. Token costs run 3–7x a single session. The dominant production winner across multi-agent surveys remains hub-and-spoke fan-out, including Anthropic's own flagship multi-agent research system.

**Recommendation for Momentum:** Stay with fan-out as the default. Reserve TeamCreate as a deliberate, opt-in pattern only for the narrow case where workers genuinely need iterative back-and-forth — and only in interactive CLI mode, never in automation. The existing Momentum global rule (`spawning-patterns.md`) already encodes this correctly. Do not adopt TeamCreate for current Momentum workflows; revisit after the feature exits experimental status and the SDK/headless path works.

---

## 1. Official Documented Use Cases: Teams vs Fan-Out

### What Anthropic actually says

The official agent teams docs (https://code.claude.com/docs/en/agent-teams) are clear and reasonable. The decision rule is one sentence:

> "Use subagents when you need quick, focused workers that report back. Use agent teams when teammates need to share findings, challenge each other, and coordinate on their own."

The documented capability matrix (confirmed):

| Aspect | Subagents (fan-out) | Agent Teams |
|--------|---------------------|-------------|
| Context | Own window; results return to caller | Own window; fully independent |
| Communication | Report back to main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only result matters | Complex work requiring discussion/collaboration |
| Token cost | Lower: results summarized back | Higher: each teammate is separate Claude instance |

Anthropic identifies four official use cases for teams: research and review across multiple aspects in parallel, new modules where teammates each own separate files, debugging with competing hypotheses (the "scientific debate" pattern), and cross-layer coordination spanning frontend/backend/tests.

The docs explicitly warn against teams for: sequential tasks, same-file edits, dependency-heavy work. The docs also state that teams use "approximately 7x more tokens than standard sessions when teammates run in plan mode" and recommend 3–5 teammates as a soft cap.

### Architecture, in one paragraph

The team lead is the original session. Teammates are independent Claude Code processes with their own context windows, spawned via the Agent tool with a `team_name` parameter. Coordination state lives on disk: `~/.claude/teams/{team-name}/config.json`, a shared task list at `~/.claude/tasks/{team-name}/`, and inbox JSON files at `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`. SendMessage appends to a recipient's inbox. A 2–4 second polling heartbeat picks up messages. There is no message broker, no IPC, no database — JSON files on disk are the entire coordination layer (confirmed via reverse-engineering, Issue #27555 surfaces the inbox-file mechanism). This is simple and durable, and also the source of most failure modes.

### Key tool-availability quirk (confirmed, Issue #32723)

The tool matrix is asymmetric and undocumented:

| Context | TeamCreate | SendMessage | Agent (spawn) |
|---------|------------|-------------|---------------|
| Standalone subagent | YES | YES | NO |
| Teammate inside team | NO | YES | NO |
| Team lead (main session) | YES | YES | YES |

A standalone subagent can call `TeamCreate` — but cannot populate the team. A teammate can receive messages but, in current builds, often cannot originate them (Issue #48160). This means the architecture is more hub-and-spoke than peer mesh in practice, regardless of intent.

---

## 2. Real-World Examples: Multi-Turn Agent Communication

This is where the marketing diverges sharply from the public record.

### The C compiler is not a TeamCreate example (confirmed)

The most commonly cited "TeamCreate proof point" is Anthropic's C compiler project (Nicholas Carlini, Safeguards team, ~2,000 sessions, 100K lines of Rust, ~$20K, 2 weeks). Reading the actual engineering blog post and repo (https://www.anthropic.com/engineering/building-c-compiler, https://github.com/anthropics/claudes-c-compiler) confirms:

- 16 Claude Opus 4.6 agents ran in parallel Docker containers against a shared git repo
- **Coordination was git-based lock files**, not SendMessage or TeamCreate
- Carlini explicitly chose **not** to use a central coordinator
- The blog states: "I haven't yet implemented any other method for communication between agents"
- The repo README describes itself as a code-generation showcase: 100% of code written by Opus 4.6

This is a parallel-agents-via-shared-git example. Any secondary source (including Gemini's triangulation output) that claims this validated TeamCreate is wrong. The Anthropic engineering blog itself does not call it a TeamCreate example.

### What the GitHub repo ecosystem actually demonstrates

| Repo | Claims | Demonstrated multi-turn P2P? |
|------|--------|------------------------------|
| `aws-samples/sample-claude-code-agent-team` | Three specialists coordinated by a fullstack agent via shared tasks and direct messaging | No. Architecture is sequential handoffs (plan → parallel build → review → loop). No SendMessage code visible. |
| `cs50victor/claude-code-teams-mcp` | Reverse-engineered protocol exposed as a generic MCP server | No working multi-turn dialogue examples. Inbox mechanism understood; peer dialogue not demonstrated. |
| `777genius/claude_agent_teams_ui` | Kanban UI; "agents talk to each other," "native real-time mailbox" | No code samples; whether this is true P2P or UI-mediated hub-and-spoke is undetermined. |
| `wshobson/agents` | 80-plugin, 185-agent collection with 7 team presets | No. Sequential handoffs, plugin composition, not TeamCreate. |
| `barkain/claude-code-workflow-orchestration` | Multi-step workflow plugin with parallel agents | Not assessed in detail; no multi-turn SendMessage evidence found. |

**Honest summary: zero public repos surfaced in this research demonstrate working multi-turn peer-to-peer agent dialogue via SendMessage.** Several describe the intent. None show transcripts or code that prove it.

### What the blog-post ecosystem reveals when you read carefully

- **alexop.dev "From Tasks to Swarms":** the much-cited QA-swarm example shows 5 agents working in parallel isolation (pages, posts, links, SEO, accessibility), each reporting back to the lead. This is hub-and-spoke, not peer mesh. The article claims teammates can ask each other for help but provides no code demonstrating it.
- **Isaac Kargar (Medium):** the only `SendMessage` shown in actual logs is a `shutdown_request` (a control message, not content collaboration). The lead uses `Bash sleep` and file polling rather than receiving autonomous inter-agent messages.
- **heeki.medium.com:** quotes Anthropic docs as evidence; provides no transcripts. Acknowledges teammates "get stuck and the team lead loses track of them."
- **kieranklaassen Gist:** describes a Teammate skill with a dotted line labeled "can message" between teammates. Operational guidance routes through the lead's inbox. Direct agent-to-agent exchange is unimplemented.

### The Gemini hallucinations (flagged explicitly)

The Gemini Thinking triangulation output cited two specific projects as evidence of production TeamCreate usage:

- **MOAI-ADK (Modu-AI):** described as an open-source ADK using TeamCreate for a TDD Quality Gate. **Hallucinated.** No results in any web search. Discard this claim.
- **+1GSD (Get Shit Done):** described as a project-management layer using TeamCreate for cross-repo merges. **Hallucinated.** No results in any web search. Discard this claim.

The Gemini output also mischaracterized the C compiler as a "Coordinator-Janitor" pattern with `sendMessage` alerts, which contradicts the actual Anthropic blog post. This is a Gemini fabrication. The C compiler used git-lock coordination only.

The remaining Gemini claims (the "Permission Deadlock," context fragmentation, orphaned processes, lack of tool isolation) are corroborated by other sources and are credible. Use them with that caveat.

### Vikrant Jain's "Taskbox" — community workaround

The most credible alternative pattern in the community: SQLite-in-WAL-mode as a coordination layer with a thin Python CLI wrapper. Multiple Claude Code agents share a task queue via poll-and-claim. No daemon, no server. This is closer to the C compiler's git-lock approach than to SendMessage. It exists because TeamCreate's mailbox model isn't reliable enough to depend on. https://vikrantjain.hashnode.dev/distributed-claude-code-agents-across-machines

### Bottom line on real-world examples

The capability matrix is honest:

| Capability | Documented | Demonstrated publicly | Confirmed working |
|---|---|---|---|
| Lead spawns teammates | Yes | Yes | Yes (CLI mode) |
| Lead sends to teammates | Yes | Yes (control messages) | Yes |
| Shared task list | Yes | Yes | Yes |
| Teammate replies to lead | Yes | Partially | Partially (bug #48160) |
| True peer-to-peer teammate↔teammate | Yes (docs) | **No real examples found** | Unclear/buggy |
| Multi-turn dialogue (back-and-forth) | Yes (docs) | **No real examples found** | Not confirmed |
| SDK/headless mode | No (docs warn) | Not found | **No (bug #1124)** |

---

## 3. Failure Modes, Limitations, and Gotchas

This section consolidates confirmed bugs and limitations across the research. Each item references the GitHub issue where available.

### Critical reliability bugs

**Issue #48160 — Spawned subagents cannot originate SendMessage (closed as duplicate, unfixed).** Subagents can receive messages but `ToolSearch("select:SendMessage")` returns no match in subagent context. In one tested case, a parent could send to four subagents but three of four could not reciprocate. The peer-to-peer architecture degrades to one-way broadcast. *This single bug undermines the entire stated value proposition of teams over fan-out.*

**Issue #25135 — SendMessage silently succeeds when recipient name doesn't match (open).** `SendMessage` returns `{success: true}` even when no agent polls the named inbox. `validateInput()` only checks for empty strings, not actual team membership. Messages written to orphaned inbox files are silently lost. Workaround: always use `recipient: "team-lead"` explicitly; manually monitor inbox files.

**Issue #28075 — Cold-start messaging failure (closed as not planned).** The idle-nudge system (3 nudges → dormancy) doesn't distinguish "waiting for a peer message" from "nothing to do." Teammates time out before peer messages arrive. Measured cold-start delays: Opus 200K ~32s (timed out), Sonnet 1M ~9s delivery + 42s checking (timed out), Haiku 4.5 ~8s (fastest model = fastest timeout). Warm-state messaging is reliable (0–13s). Workaround: lead keepalive nudges every ~10s, which wastes tokens.

**Issue #1124 (claude-code-action) — Agent Teams entirely unusable in SDK/headless mode.** The lead produces `end_turn` immediately after spawning teammates because the SDK session lifecycle has no keepalive. Teammates spawn as separate processes that return "agent is running, will receive messages via mailbox" — but the session exits (typically after 10–11 turns) before they complete. A "watcher" subagent workaround is blocked by auto-enrollment: any agent spawned while a team is active is auto-enrolled as a teammate. **No working workaround. The feature is non-functional in CI/CD, GitHub Actions, or any automation pipeline.**

**Issue #34614 — Silent process exit (Claude Code v2.1.76+).** Teammate processes silently exit immediately after spawn. tmux pane opens; process exits with no error output.

**Issue #42391 — Command split at ~255 bytes during teammate spawn.** Internal buffering in Claude Code's tmux integration splits launch commands of 400–500 chars. First fragment fails; second runs as standalone. Parent falsely reports "Spawned successfully." Workaround: wrap send-keys through a temp script.

### State and lifecycle limitations

**Issue #33764 — State wiped on session restart.** No `/resume` for in-process teammates. Long-running team workflows cannot be interrupted and resumed. This is acknowledged in the builder.io blog as a near-disqualifier: "Session dies, team is gone."

**Issue #32730 — Orphaned teams block future creation.** When a subagent calls `TeamCreate`, the config persists after the subagent ends. Subsequent `TeamCreate` for the same name returns `"Already leading team"`. Manual deletion of `~/.claude/teams/{name}/` is the only fix.

**Issue #36670 — Teammates don't inherit 1M context variant.** Teammates inherit the model ID but resolve to claude-opus-4-6 (200K) rather than claude-opus-4-6[1m] (1M). Real capability gap on large codebases.

**Issue #48889 — Spawn fails after `brew upgrade`.** Hardcoded Caskroom path captured at spawn time; symlink not used. Restart required after upgrade.

### UI and crash bugs

**Issue #49303 — Stack overflow on teammate permission request.** Team lead Claude Code v2.1.111 crashes in the permission-explainer component (cli.js:477). Regression vs. older Opus 4.6.

**Issue #49865 — Team leader crashes ("getAppState is not a function") on teammate tool permission request.** Permission prompt never surfaces. Leader is dead. Combined with #49303, **any teammate that needs tool permissions can crash the entire team.**

**Issue #27555 — Teammate messages render with `⏺ Human:` prefix.** Teammate-originated messages are visually indistinguishable from user input. UI bug, not architectural — but confirms the routing mechanism is JSON inbox files, not a live message bus.

### Architectural constraints

- One team per session. Cannot manage multiple teams concurrently.
- No nested teams. Teammates can't spawn their own teams.
- Model config not inherited (must specify model explicitly).
- File conflicts: parallel edits overwrite each other. Must partition files by teammate.
- Teammates inherit the lead's full permission set — no read-only-researcher vs. full-access-implementer separation.
- Broadcast doesn't scale: SendMessage is push-based, ephemeral, no persistence or ordering. With 8+ agents, broadcasts arrive out of order. Practical cap is 3–5 agents (Issue #30140).

### Cost and token gotchas

- 3-agent team: ~3–4x tokens vs. single session.
- Plan-mode teams: ~7x tokens vs. single session (Anthropic's own number).
- Anthropic's flagship multi-agent research system: ~15x tokens.
- One documented worst case: a `/typescript-checks` invocation with 49 subagents for 2.5 hours, estimated $8K–$15K.
- A financial-services team: $47K over three days from 23 unattended agents.
- alexop.dev measured 4x multiplier on a 3-agent team: 200K solo → 800K team.

### What this list collectively means

The current TeamCreate implementation has fundamental reliability problems at every layer: spawn (#42391, #34614, #48889), runtime (#48160, #25135, #28075), state (#33764, #32730), permission (#49303, #49865), automation (#1124), and capability inheritance (#36670). Several are closed as duplicate or not-planned, signaling Anthropic is aware but not actively patching. The April 23, 2026 Claude Code postmortem confirmed broader quality regression in March–April 2026, which amplified community skepticism about features that compound failure surfaces.

---

## 4. Decision Framework: When Teams Add Value Over Fan-Out

### The primary heuristic (community consensus)

Across Charles Jones, LaoZhang AI, knightli.com, and MindStudio, the same one-line rule appears:

> **"If you can describe each worker's task without referencing other workers, use subagents."**

This is the same gate Momentum's existing `spawning-patterns.md` rule applies. The agreement is striking and useful.

### Decision tree

```
Do parallel workers need to communicate during execution?
├── No → Fan-out subagents
│        └── Can each worker's task be described without referencing other workers?
│            ├── Yes → Subagents (clean fan-out)
│            └── No → Rethink decomposition; sequential may be better
└── Yes → Consider agent teams
          └── Is single-agent baseline performance already above ~45% accuracy?
              ├── Yes → Multi-agent likely adds no value; stick with single agent
              └── No → Agent teams may be warranted (if interactive CLI mode)
```

### Secondary gate by task shape

| Task shape | Recommendation |
|---|---|
| Parallelizable, independent (research, review, test gen) | Fan-out subagents |
| Sequential reasoning (planning, dependency chains) | Single agent |
| High tool density (≥10 tools) | Decentralized agents, monitor error amplification |
| Low volume, accuracy-critical, ≤5 agents, peer debate is the mechanism | Teams viable |
| High volume (10K+ iterations), cost-sensitive | Hierarchical fan-out; avoid teams |
| CI/CD / SDK pipeline | Fan-out only (teams are non-functional) |

### Quantitative thresholds (from research)

- **Agent count:** start with 3, soft cap at 5. Coordination overhead grows superlinearly (O(n^1.4 to n^2.1) per the multi-agent collaboration survey).
- **Baseline accuracy:** if a single agent already exceeds ~45% on the task, multi-agent is *net-negative* (Google scaling study, β = -0.408, p < 0.001).
- **Pipeline length:** at 10+ semi-independent tasks, fan-out orchestrator context accumulation becomes expensive; teams may be more token-efficient *only at this scale*.
- **Token budget:** plan for 3–7x a single session.

### Signals that teams genuinely add value

The OAuth case study from Charles Jones is the cleanest documented win: agent teams cut wall-clock time roughly in half on an OAuth feature. The mechanism: "frontend and backend matched on the first pass" via direct messaging, eliminating handoff debugging loops. This is a real, specific value prop — but it requires (a) two parallel workstreams that genuinely need to negotiate an interface and (b) interactive CLI mode where SendMessage actually works.

The "scientific debate" / competing-hypotheses use case is the most credible unique value claim for teams. *No public reproduction of this pattern in working form was found.* It remains a documented intent, not a proven mechanism.

### Counter-signals (when "communication" is a mirage)

Many tasks that *seem* to need agent communication actually don't:

- "Frontend and backend agents need to agree on API shape" → spec the API up front in a single planning session, then fan out.
- "The reviewer needs to ask the implementer questions" → run them sequentially, not in parallel.
- "Agents need to share findings" → synthesize at the end via the orchestrator.

The alexop.dev pattern is robust: **plan first in plan mode (cheap), hand the plan to a team or fan-out for parallel execution.** Most coordination collapses out at the planning stage.

---

## 5. Benchmarks: TeamCreate vs Fan-Out Performance

**No published head-to-head benchmark specifically comparing TeamCreate vs fan-out for identical tasks in Claude Code exists in the public record.** Every benchmark cited is either architectural analysis, external research on analogous patterns, or practitioner anecdote.

The closest data points:

### Anthropic's own production system chose fan-out (strongest signal)

Anthropic's flagship multi-agent research system (https://www.anthropic.com/engineering/multi-agent-research-system) uses **fan-out**:

- Lead: Claude Opus 4 (orchestrator)
- Workers: Claude Sonnet 4 subagents (parallel investigators, no peer messaging)
- Pattern: orchestrator spawns → subagents investigate independently → results synthesized
- Performance: **+90.2%** over single-agent Opus on internal research evals
- Latency: parallel tool calling reduced research time by **up to 90%** for complex queries
- Cost: ~15x tokens vs. standard chat

When Anthropic itself shipped a flagship multi-agent system for research (the canonical "teams" use case), they chose fan-out, not peer teams. This is the most damning signal for TeamCreate as a default pattern.

### The OAuth case study (Charles Jones)

Agent teams completed an OAuth feature in roughly **half the wall-clock time** of a subagent workflow. Frontend/backend matched on first pass via direct messaging. **N=1**, single-author report, no controlled methodology. Useful as existence proof, not as a benchmark.

### LaoZhang AI cost scenarios (Opus 4.6 lead + Sonnet 4.5 teammates)

| Scenario | Single session | Agent team | Multiplier |
|---|---|---|---|
| Parallel code review (3 reviewers, 30 min) | ~$2.00 | ~$4.50 | 2.25x |
| Full-stack feature (FE+BE+tests, 2h) | $8–15 | ~$20 | 2.5–3x |
| Complex debugging (3 investigators, 1h) | ~$10 | ~$13 | 1.3x |

Wall-clock compression is real (full-stack: 4–6h sequential → 90 min). Token cost premium is consistent.

### Google Research scaling study (arXiv:2512.08296)

Most rigorous quantitative study found:

- Finance (parallelizable): centralized +80.9%, decentralized +74.5%
- Planning (sequential): all multi-agent variants degraded **39–70%**
- Web navigation: decentralized +9.2%, centralized +0.2%
- Tool-heavy: independent agents amplify errors **17.2x**; centralized contains to **4.4x**
- **Critical threshold: tasks where single-agent already exceeds 45% accuracy experience negative returns from additional agents** (β = -0.408, p < 0.001)

### Financial document benchmark (arXiv:2603.22651, 10K SEC filings)

| Architecture | F1 | Cost/doc | Latency |
|---|---|---|---|
| Sequential | 0.903 | $0.187 | 38.7s |
| Parallel (fan-out) | 0.914 | $0.221 | 21.3s |
| Hierarchical | 0.929 | $0.261 | 46.2s |
| Reflexive (peer-to-peer) | 0.943 | $0.430 | 74.1s |

Hierarchical achieves 98.5% of reflexive F1 at 60.7% of the cost. Peer-to-peer is highest quality but 2.3x more expensive per doc and degrades at scale (-0.072 F1 at 100K docs/day vs. -0.017 for sequential). **Hierarchical fan-out is the practical optimum.**

### Multi-agent vs. single LLM (arXiv:2509.23537)

Multi-turn orchestration matches or exceeds the strongest single model and consistently outperforms others on GPQA-Diamond, IFEval, MuSR — but vote-visibility amplifies herding and premature consensus. Coordination mechanisms haven't reached their ceiling.

### MindStudio's token-cost reversal at scale

A counterintuitive scenario: in fan-out, the orchestrator accumulates all subagent outputs. With 10 subagents at 2K tokens each, orchestrator carries 20K+ tokens per subsequent message.

- **Small pipelines (2–4 agents):** negligible difference.
- **Medium (5–10 agents):** orchestrator hits 30–50K tokens by synthesis — real cost.
- **Large (10+ agents, substantial output):** **agent teams estimated 3–5x cheaper** in token costs because no single agent accumulates full state.

This is an estimated reversal, not a measured one. Cite cautiously. It applies only at pipeline sizes Momentum doesn't currently run.

### Synthesis

The benchmark evidence supports a strong default for fan-out (specifically hub-and-spoke / hierarchical) and a narrow niche for peer-to-peer (low-volume, accuracy-critical, ≤5 agents, peer debate is the mechanism). Anthropic's own production multi-agent system corroborates this. There is no benchmark anywhere proving teams beat fan-out on the same Claude Code task.

---

## 6. Community Sentiment: Honest Developer Perspectives

### Where the signal lives

- **GitHub issues** — most reliable, developers debugging real failures.
- **Hacker News** thread #46902368 (Agent Teams announcement) — best structured discussion, multi-perspective.
- **Substack** (getpushtoprod, theexcitedengineer) — practitioners writing longer-form lessons.
- **Medium** — mixed; some genuine practitioner posts, many SEO guides.

Notably absent: Reddit (r/ClaudeAI and r/LocalLLaMA returned zero results for "agent teams" or "TeamCreate"), Discord (no public indexed threads), X/Twitter (not surfaced).

### The dominant practitioner take: "you probably don't need agent teams"

The clearest blog statement is from builder.io: "Claude agent teams are pointless for most things." Practical ceiling 3–5 teammates. No `/resume`. Efficiency paradox: 3–4x more tokens for gains that materialize only in narrow scenarios. Most development tasks don't fit those scenarios.

The alexop.dev assessment (most technically grounded): measured 4x token multiplier on a 3-agent team. "More agents = more tokens = more cost." Best workflow: plan in plan mode first (cheap), then hand to a team for parallel execution (expensive but fast). Teams that go in wrong directions burn 500K+ tokens; a 10K-token planning phase prevents this.

The @itsHabib Medium post (real production usage): large undifferentiated teams ("FE, BE, infra, SRE all in one") failed with excessive coordination overhead and conflicting assumptions. Two agents with narrow scope consistently outperformed larger teams. Strict compartmentalization (narrow roles, dedicated output ownership, templates preventing deviation) was the only path to success. Infrastructure domain agents struggled most.

### The 30-tips compendium (Substack, John Kim) — concrete gotchas from real usage

- File conflict disasters when agents work on identical files; requires clean domain separation.
- Context isolation: teammates don't inherit the orchestrator's conversation history; important context must be embedded in task descriptions.
- Orchestrator goes rogue: "Sometimes the leader will just start implementing stuff instead of delegating." Cannot be left unattended.
- tmux works; iTerm integration is flaky.
- Confirmed experimental as of March 2026.

### Hacker News voices

**Skeptics:**
- "$200/month is a used car payment" (dangus) — pricing trajectory criticism.
- "I absolutely cannot trust Claude code to independently work on large tasks" (ottah) — teams amplify an existing reliability problem.
- Week-long debugging cycle where agents failed at ffmpeg, streaming formats, basic architecture — agents burning tokens on wrong approaches without correction (RollAHardSix).
- Token usage "insane" relative to effectiveness (gbnwl).

**Cautious optimists:**
- "With an agent swarm I'm limited by my idea and review capabilities" (MarkMarine) — review bandwidth is the real constraint.
- Built a complex media pipeline "in a few days when it otherwise would have taken 1–2 months" (frankc) — ROI positive on the right shape of work.
- Adversarial pattern (one agent implements, another critiques) is recommended (aqme28) — and has been independently rediscovered by multiple developers.

**Most structural:** doctoboggan — agent teams target corporations, not individual developers. The token economics only work on engineering team budgets. *This single observation explains a lot of the disconnect between marketing and individual-developer adoption.*

### "Multi-Agent in Production in 2026 — What Actually Survived" (Medium)

Hub-and-spoke fan-out emerged as the dominant production winner. Peer-collaboration teams — the "romantic vision" — largely failed in open form. Surviving multi-agent implementations use hidden selectors, phase gates, or final arbiters: *bounded collaboration within supervisor architectures*, not true mesh systems.

Three failure studies cited:
1. MIT: adding relay stages without new signals collapsed accuracy from 90.7% to 22.5% across five stages.
2. "From Spark to Fire" cascade study: hub injection produced 100% system-wide failure vs. 9.7% from leaf-node failures.
3. Google 2026: multi-agent degraded sequential planning by 39–70%; independent agents amplified errors 17.2x vs. 4.4x for centralized.

Five surviving production rules:
1. Start with a single strong agent.
2. Specialists must contribute genuinely new information (not just route).
3. Budget for ~15x token consumption vs. single-agent.
4. Match topology to task shape, not organizational structure.
5. Bound collaboration with protocols and observability mechanisms.

### Has anyone abandoned TeamCreate?

Not as an explicit reversal in any sourced post. The pattern observed: developers who tried teams with large undifferentiated rosters scaled back to smaller focused teams or reverted to subagents. The SDK/headless limitation is an *effective* abandonment for CI/CD use cases — there's no path forward. The general framing across multiple sources: "agent teams for specific collaboration scenarios, subagents for everything else."

### Honest summary of community sentiment

TeamCreate is a genuinely novel architectural primitive that works *when conditions are narrow*: tasks require true peer coordination, teams are small (2–5), domain separation is clean, token budget is not a concern, workflow runs in interactive CLI (not headless/SDK). Outside those conditions — which is most workflows — practitioners report agent teams add cost and fragility without proportional benefit. The feature is not "never works." It's "requires expert knowledge of failure modes, costs significantly more, has fundamental incompatibilities with automation."

---

## Cross-Cutting Themes

Several patterns repeat across all four research streams:

**1. The marketing-reality gap is large.** The official docs describe a peer-mesh architecture. The implementation behaves as constrained hub-and-spoke. Subagents can't originate SendMessage in many configurations. The most-cited proof point (C compiler) doesn't actually use the feature. No public repo demonstrates working multi-turn peer dialogue.

**2. Fan-out wins on the evidence.** Anthropic's own production multi-agent system uses fan-out. The financial-document benchmark shows hierarchical fan-out at 98.5% of peer F1 for 60.7% of the cost. The Google scaling study shows centralized coordination contains errors 4x better than independent peers. "What Survived 2026" identifies hub-and-spoke as the production winner.

**3. The single-agent baseline matters more than people admit.** The 45%-accuracy threshold from Google Research is the most important quantitative finding in this corpus. If a single agent already handles the task tractably, multi-agent coordination is *net-negative*, not neutral. Most Momentum workflow steps probably exceed this threshold.

**4. Token costs are higher than the docs suggest.** The "7x in plan mode" official number is a floor, not a ceiling. Real-world reports: 3–4x at 3 agents, 15x for Anthropic's own research system, $8K–$15K for one ill-bounded run, $47K over three days for unattended teams.

**5. Headless/SDK incompatibility is structural.** Issue #1124 means TeamCreate cannot be used in CI/CD, GitHub Actions, or any non-interactive automation. This is not a bug to be patched soon — the session lifecycle model is incompatible.

**6. The community has independently converged on similar workarounds.** Plan-first-then-fan-out (alexop.dev), adversarial pairs (aqme28), shared SQLite/git task queues (Vikrant Jain's Taskbox, the C compiler). All of these are *avoidance strategies* for TeamCreate, not implementations of it.

**7. The "competing hypotheses" use case is the only credible unique value claim — and it has no public proof.** Every other documented use case (research, modules, cross-layer) can be done with fan-out plus a final synthesis pass.

---

## Recommendations for Momentum

Momentum already has a clean global rule (`~/.claude/rules/spawning-patterns.md`) that codifies the right gate:

> **"Can each agent complete its work without talking to any other agent?"**
> - Yes → Fan-out (individual Agent spawns)
> - No → TeamCreate

The rule is correct in principle. The research suggests how to refine it in practice.

### 1. Keep fan-out as the default. Do not migrate existing workflows to TeamCreate.

The current Momentum workflows that use parallel agents (sprint-dev wave, AVFL validators, research queries, dev wave per-story spawning) are textbook fan-out cases. Each agent's task can be described without referencing other agents. Results return to the orchestrator. There is no peer dialogue requirement. Migrating any of these to TeamCreate would add 3–7x token cost, add failure modes (cold-start timeout, recipient validation, permission crashes, headless incompatibility), and gain nothing measurable.

### 2. Add explicit "do not adopt" guidance for current Momentum workflows.

Update `spawning-patterns.md` to add a third gate after the existing decision rule:

> **"Even if peer dialogue seems valuable, is the task already tractable with a single agent + fan-out + synthesis pass? If yes, do not use TeamCreate."**

Most "agents need to talk" instincts dissolve when the work is decomposed properly. The OAuth-style case (interface negotiation between truly parallel workstreams) is rare in Momentum; spec-then-fan-out usually replaces it.

### 3. If TeamCreate is ever used, gate it explicitly on these preconditions.

A skill that genuinely needs teams must satisfy *all* of:

- Interactive CLI mode only (never SDK, headless, hooks, scheduled, or CI).
- ≤5 teammates.
- Clean file partitioning (no same-file edits).
- Workflow can survive `/resume` not working (i.e., short enough to run in one session).
- Single-agent baseline below ~45% on the task.
- Mechanism is genuinely peer dialogue (debate, hypothesis testing, interface negotiation), not parallel execution.
- Developer is present to handle permission requests (which can crash the lead, Issues #49303 and #49865).

If any precondition fails, default to fan-out.

### 4. Document the SDK/headless incompatibility prominently.

Many Momentum workflows are designed to run headlessly or under SDK conditions (hooks, scheduled tasks, automated retros, AVFL passes). These cannot use TeamCreate at all. This is not a tunable knob — it's a structural incompatibility. Surface this in the rule.

### 5. Treat "competing hypotheses" debugging as a future spike, not a current pattern.

The scientific-debate pattern is the strongest unique value prop for teams. No public implementation works yet. If Momentum ever wants this capability — for example, in `momentum:assessment` or a future debugging skill — treat it as a research spike with a working proof-of-concept first, not a workflow adoption. Validate that Issues #48160 and #28075 are fixed before committing.

### 6. Encode the 45% baseline rule.

Add a quantitative gate to `spawning-patterns.md`: "If a single Claude Opus session already handles the task at usable quality, multi-agent coordination is net-negative. Don't multi-agent for the optics." This is the single most actionable finding from the Google Research scaling study.

### 7. For existing fan-out workflows, validate the orchestrator-context-accumulation cost.

The MindStudio finding — that fan-out becomes more expensive than teams at 10+ agents because the orchestrator accumulates all outputs — is plausible but unmeasured for Momentum's specific workflows. Sprint-dev waves with many stories may approach this. Worth a one-time measurement: capture orchestrator token usage at synthesis time across a representative sprint. If it exceeds 30K–50K, consider intermediate compaction or a hierarchical pattern (lead → sub-orchestrators → workers), not teams.

### 8. Capture hub-and-spoke patterns as the default architecture.

The "What Survived 2026" framing — *bounded collaboration within supervisor architectures* — fits Momentum's existing design. Sprint-dev's flow (dispatcher → parallel dev workers → AVFL → merge) is exactly hub-and-spoke. Retro's flow (transcript audit → auditor team → findings synthesis) is also hub-and-spoke. Don't break these for TeamCreate.

### 9. Write off the Gemini-cited examples.

If anyone (including a future research run) cites MOAI-ADK or +1GSD as TeamCreate validation, they're propagating Gemini hallucinations. The C compiler is also not a TeamCreate example. Calibrate any future research that proposes adopting teams against these honest baselines.

---

## Known Limitations of This Research

- **No published head-to-head benchmark of TeamCreate vs fan-out exists.** All comparisons are inferred from analogous studies, practitioner reports, or architectural reasoning.
- **The agent teams feature is moving fast.** Several issues cited may be fixed by the time this report is read. Verify Issues #48160, #28075, and #1124 status before changing recommendations based on them.
- **Reddit and Discord signal is missing.** Search returned no results in r/ClaudeAI or r/LocalLLaMA, and Discord threads aren't publicly indexed. This may be a gap in coverage rather than absence of discussion.
- **N=1 case studies dominate.** The OAuth case (Charles Jones), the @itsHabib production usage, and the alexop.dev measurements are all single-author reports with no controlled methodology.
- **Gemini Thinking output contained two confirmed hallucinations** (MOAI-ADK, +1GSD) and one mischaracterization (the C compiler). Other Gemini claims were corroborated by independent sources but should not be trusted unless independently verified.
- **The Anthropic April 23, 2026 Claude Code postmortem** acknowledged broader quality regression in March–April 2026 that may have temporarily worsened TeamCreate's apparent reliability. Future re-evaluation should account for this.
- **Token cost figures vary widely** across sources (3x, 4x, 7x, 15x). They depend on team size, mode (plan vs. execute), and task shape. Treat them as ranges, not point estimates.
- **No data on Momentum-specific workflows.** All recommendations are extrapolations from general multi-agent research and Claude Code-specific anecdote. Empirical validation on a Momentum workflow would improve confidence.

---

## Sources

### Official documentation
- Claude Code Agent Teams docs: https://code.claude.com/docs/en/agent-teams
- Manage costs effectively: https://code.claude.com/docs/en/costs
- Anthropic: How We Built Our Multi-Agent Research System: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic: When to use multi-agent systems: https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
- Anthropic: Building a C compiler with Claude: https://www.anthropic.com/engineering/building-c-compiler
- Anthropic: April 23, 2026 postmortem: https://www.anthropic.com/engineering/april-23-postmortem
- C compiler repo: https://github.com/anthropics/claudes-c-compiler
- TechCrunch Opus 4.6 announcement: https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/

### GitHub issues — confirmed bugs and limitations
- #48160 Spawned subagents cannot originate SendMessage: https://github.com/anthropics/claude-code/issues/48160
- #25135 SendMessage silently succeeds for invalid recipients: https://github.com/anthropics/claude-code/issues/25135
- #27555 Teammate messages render with `Human:` prefix: https://github.com/anthropics/claude-code/issues/27555
- #28075 Cold-start messaging failure: https://github.com/anthropics/claude-code/issues/28075
- #30140 Broadcast scaling and persistence: https://github.com/anthropics/claude-code/issues/30140
- #32723 Tool availability matrix: https://github.com/anthropics/claude-code/issues/32723
- #32730 Orphaned teams block creation: https://github.com/anthropics/claude-code/issues/32730
- #33764 State wiped on restart: https://github.com/anthropics/claude-code/issues/33764
- #34614 Silent process exit: https://github.com/anthropics/claude-code/issues/34614
- #36670 Teammates don't inherit 1M context: https://github.com/anthropics/claude-code/issues/36670
- #40270 Agent tool with team_name fails: https://github.com/anthropics/claude-code/issues/40270
- #42391 Command split at ~255 bytes: https://github.com/anthropics/claude-code/issues/42391
- #48889 Spawn fails after brew upgrade: https://github.com/anthropics/claude-code/issues/48889
- #49303 Stack overflow on permission request: https://github.com/anthropics/claude-code/issues/49303
- #49865 Lead crashes on teammate permission: https://github.com/anthropics/claude-code/issues/49865
- #577 SDK SendMessage broken: https://github.com/anthropics/claude-code/issues/577
- claude-code-action #1124 SDK/headless unusable: https://github.com/anthropics/claude-code-action/issues/1124

### Repos surveyed
- aws-samples/sample-claude-code-agent-team: https://github.com/aws-samples/sample-claude-code-agent-team
- cs50victor/claude-code-teams-mcp: https://github.com/cs50victor/claude-code-teams-mcp
- 777genius/claude_agent_teams_ui: https://github.com/777genius/claude_agent_teams_ui
- wshobson/agents: https://github.com/wshobson/agents
- barkain/claude-code-workflow-orchestration: https://github.com/barkain/claude-code-workflow-orchestration

### Practitioner posts
- Charles Jones — Agent Teams vs Subagents: https://charlesjones.dev/blog/claude-code-agent-teams-vs-subagents-parallel-development
- LaoZhang AI practical guide: https://blog.laozhang.ai/en/posts/claude-code-agent-teams
- MindStudio — Agent Teams vs Sub-Agents: https://www.mindstudio.ai/blog/claude-code-agent-teams-vs-sub-agents
- knightli.com Subagents vs Agent Teams 2026: https://www.knightli.com/en/2026/04/22/claude-code-subagents-vs-agent-teams/
- alexop.dev From Tasks to Swarms: https://alexop.dev/posts/from-tasks-to-swarms-agent-teams-in-claude-code/
- Isaac Kargar Medium: https://kargarisaac.medium.com/agent-teams-with-claude-code-and-claude-agent-sdk-e7de4e0cb03e
- heeki.medium.com: https://heeki.medium.com/collaborating-with-agents-teams-in-claude-code-f64a465f3c11
- builder.io You Probably Don't Need Agent Teams: https://www.builder.io/blog/claude-agent-teams-explained-what-it-is-and-how-to-actually-use-it
- John Kim Substack 30 Tips: https://getpushtoprod.substack.com/p/30-tips-for-claude-code-agent-teams
- @itsHabib Trying Out Claude Code Teams: https://medium.com/@itsHabib/trying-out-claude-code-teams-e4c2a0eaf72f
- Multi-Agent in Production 2026 — What Survived: https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1
- Vikrant Jain Taskbox: https://vikrantjain.hashnode.dev/distributed-claude-code-agents-across-machines
- kieranklaassen Swarm Skill Gist: https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea
- claudecodecamp internals: https://www.claudecodecamp.com/p/claude-code-agent-teams-how-they-work-under-the-hood
- LeadDev trust crisis: https://leaddev.com/ai/how-anthropics-silence-fueled-a-claude-code-trust-crisis

### Hacker News threads
- Agent Teams announcement (#46902368): https://news.ycombinator.com/item?id=46902368
- Is Claude Code getting worse (#47936579): https://news.ycombinator.com/item?id=47936579
- Claude Code unusable for complex tasks (#47660925): https://news.ycombinator.com/item?id=47660925

### Academic and research papers
- arXiv:2512.08296 Towards a Science of Scaling Agent Systems (Google Research): https://arxiv.org/html/2512.08296v1
- arXiv:2603.22651 Benchmarking Multi-Agent LLM Architectures: https://arxiv.org/html/2603.22651
- arXiv:2509.23537 Beyond the Strongest LLM: https://arxiv.org/abs/2509.23537
- arXiv:2501.06322 Multi-Agent Collaboration Mechanisms Survey: https://arxiv.org/abs/2501.06322
- InfoQ C compiler analysis: https://www.infoq.com/news/2026/02/claude-built-c-compiler/

### Architecture references
- Agent Architecture Patterns 2026 Taxonomy: https://www.digitalapplied.com/blog/agent-architecture-patterns-taxonomy-2026
- Galileo: Architectures for Multi-Agent Systems: https://galileo.ai/blog/architectures-for-multi-agent-systems
- MindStudio Parallel Agents Coordination: https://www.mindstudio.ai/blog/claude-code-agent-teams-parallel-agents)
