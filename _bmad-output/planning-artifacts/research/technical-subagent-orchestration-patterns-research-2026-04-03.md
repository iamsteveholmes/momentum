---
stepsCompleted: [1, 2, 3, 4]
workflowType: 'research'
lastStep: 4
research_type: 'technical'
research_topic: 'Subagent Orchestration Patterns in Claude Code'
research_goals: 'Work decomposition, optimal agent count, agent type selection, foreground vs background, isolation, result aggregation, error handling'
user_name: 'Steve'
date: '2026-04-03'
web_research_enabled: true
source_verification: true
---

# Research Report: Subagent Orchestration Patterns in Claude Code

**Date:** 2026-04-03
**Author:** Steve
**Research Type:** Technical (web-verified, 2025-2026 sources)

---

## Research Overview

This report synthesizes findings on how to effectively orchestrate subagents in Claude Code for research and development tasks. It draws on Anthropic's official documentation, the C compiler case study (16 parallel agents, $20K, 100K lines of Rust), practitioner reports, GitHub issues, and community guides. Every factual claim from external sources is cited with its URL.

**Evidence quality notation:**
- `[OFFICIAL]` -- Anthropic documentation or engineering blog
- `[PRAC]` -- Practitioner consensus (blog, community guide)
- `[ISSUE]` -- GitHub issue with empirical data
- `[CASE]` -- Production case study

---

## 1. Work Decomposition Strategies

### 1.1 Decomposition by Domain (Strongest Pattern)

The most consistently successful decomposition strategy is **domain-based partitioning**, where each agent receives a non-overlapping area of responsibility. This pattern succeeds because agents don't write shared files, conflict probability is near zero, and synthesis is the only coordination point.

For research tasks specifically, this translates to **decomposition by subtopic** -- each agent investigates one distinct research question or knowledge domain. The C compiler project demonstrated this: when hundreds of independent failing tests existed, "each agent picks a different failing test to work on" and parallelization was trivial `[OFFICIAL]` ([Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)).

For code research, domain-based routing means spawning separate agents for frontend, backend, and database domains, "where each agent owns their domain" `[PRAC]` ([claudefa.st Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)).

### 1.2 Decomposition by Source Type

A variant useful for research: partition agents by the type of source they consult. One agent searches the web, another explores the codebase, a third reads specific documents. This works when the research question benefits from triangulation across source types.

### 1.3 Hierarchical Decomposition (Two-Level Delegation)

Addy Osmani's analysis recommends spawning "feature leads that spawn their own specialists" rather than a single orchestrator managing many agents. This reduces context fragmentation -- "the parent only coordinates with two feature leads, each managing their own team" `[PRAC]` ([The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)).

However, this pattern has a hard constraint in Claude Code: **subagents cannot spawn other subagents** `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)). The hierarchical pattern is only possible with Agent Teams (experimental), where teammates are full Claude Code sessions, not subagents.

### 1.4 Oracle-Based Decomposition (for Monolithic Tasks)

When a task cannot be trivially partitioned (e.g., all agents hit the same bug), the C compiler project solved this by introducing a "known-good oracle" -- GCC -- to generate ground truth, then decomposing around the oracle's outputs. The lesson: **when parallel agents converge on the same problem, restructure the task rather than adding more agents** `[OFFICIAL]` ([Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)).

### 1.5 Anti-Pattern: Decomposition Too Fine

"Launching 10 parallel agents for a simple feature wastes tokens and creates coordination overhead" `[PRAC]` ([claudefa.st Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)). Group related micro-tasks rather than creating one agent per atomic question.

---

## 2. Optimal Agent Count

### 2.1 The Sweet Spot: 3-5 Concurrent Agents

Multiple independent sources converge on this range:

- **Anthropic's official agent teams docs:** "Start with 3-5 teammates for most workflows. Scale up only when work genuinely benefits from simultaneous teammates. Three focused teammates often outperform five scattered ones." `[OFFICIAL]` ([Claude Code Agent Teams](https://claudefa.st/blog/guide/agents/agent-teams), citing official docs)
- **Addy Osmani:** "Three to five teammates is the sweet spot. Token costs scale linearly, and three focused teammates consistently outperform five scattered ones." `[PRAC]` ([The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/))
- **Subscription tier constraints:** On Pro plans, comfortable throughput for 2-3 concurrent instances. On Max, 4-5. "The practical ceiling is 5-7 concurrent agents on a laptop before rate limits, merge conflicts, and review bottleneck eat the gains." `[PRAC]` ([How to run Claude Code in parallel](https://ona.com/stories/parallelize-claude-code))

### 2.2 Scaling Beyond 5: Diminishing Returns

- **Token cost:** A 3-teammate team uses roughly 3-4x the tokens of a single session doing the same work sequentially `[PRAC]` ([claudefa.st Agent Teams Guide](https://claudefa.st/blog/guide/agents/agent-teams)). Multi-agent workflows use 4-7x more tokens than single-agent sessions `[PRAC]` ([ksred Claude Code Agents](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)).
- **Up to ~10:** Coordination and token overhead creates diminishing returns `[PRAC]` ([claudefa.st](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)).
- **16 agents (C compiler):** Worked only because tasks were perfectly independent (different failing tests). When the task became monolithic (Linux kernel compilation), 16 agents were "no help because each was stuck solving the same task" `[OFFICIAL]` ([Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)).

### 2.3 System Stability Limits: 20+ Agents

- **GitHub Issue #15487:** On a 2vCPU/4GB RAM VPS, 24 parallel subagent processes spawned within 2 minutes caused a 17.3x disk I/O spike and 5.6x CPU increase, requiring a hard reboot `[ISSUE]` ([GitHub #15487](https://github.com/anthropics/claude-code/issues/15487)).
- **Mac mini M4 Pro (24GB RAM):** Complete system freeze from memory exhaustion with 20+ agents `[ISSUE]` ([same issue](https://github.com/anthropics/claude-code/issues/15487)).
- **No built-in throttling:** There is no `maxParallelAgents` setting. A feature request was auto-closed without response `[ISSUE]` ([GitHub #15487](https://github.com/anthropics/claude-code/issues/15487)).

### 2.4 Practical Guidelines by Task Weight

Observed limits from practitioner data `[ISSUE]` ([GitHub #15487](https://github.com/anthropics/claude-code/issues/15487)):
- ~5-6 agents: light tasks (file ops, git, search)
- ~3-4 agents: medium tasks (builds, linting, research with web search)
- ~2 agents: heavy tasks (large file processing, complex reasoning)

### 2.5 The Human Review Constraint

"Don't run more agents than you can meaningfully review" `[PRAC]` ([The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)). For research, this means the synthesizing agent (or human) must be able to actually process and verify all parallel outputs. Beyond 5-6 research agents, the synthesis step itself becomes the bottleneck.

---

## 3. Agent Type Selection

### 3.1 Built-in Agent Types

Claude Code ships with several built-in subagent types `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)):

| Type | Model | Tools | Use Case |
|---|---|---|---|
| **Explore** | Haiku | Read-only (Glob, Grep, Read) | Fast codebase search, file discovery |
| **Plan** | Inherits parent | Read-only | Architecture planning, context gathering in plan mode |
| **General-purpose** | Inherits parent | All tools | Complex multi-step tasks, code changes |
| **Bash** | Inherits parent | Terminal commands | Shell operations in separate context |

### 3.2 Explore Agent: When and How

The Explore agent runs on Haiku at ~80% lower cost than Sonnet/Opus `[PRAC]` ([Claude Code Agents guide](https://claude-world.com/articles/agents-guide/)). It specifies a thoroughness level `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)):

- **Quick:** Targeted lookups -- find a specific file, check if a function exists. Minimal tool calls.
- **Medium:** Balanced exploration -- understand how a feature works across a few files. Moderate tool calls.
- **Very thorough:** Comprehensive analysis -- map an entire system, search across multiple locations and naming conventions. Many tool calls.

**When to use Explore for research:**
- Codebase mapping before implementation
- Finding all references to a pattern, API, or convention
- Understanding feature boundaries across files
- Any read-only investigation where frontier reasoning is not required

**When NOT to use Explore:**
- When the task requires complex reasoning to interpret findings across files
- When the task requires code modification after research
- When web search or external tool access is needed (Explore has no web tools)

### 3.3 General-Purpose Agent: When to Use

Use general-purpose when the research task requires `[PRAC]` ([Claude Code Agents guide](https://claudelab.net/en/articles/claude-code/claude-code-agent-guide)):
- Both exploration AND modification
- Complex reasoning to interpret results
- Multiple dependent steps
- Web search or external data sources
- Writing findings to files

### 3.4 Plan Agent: Architecture Research

The Plan agent activates during plan mode. When Claude needs to understand the codebase before presenting a plan, it delegates research to the Plan subagent `[PRAC]` ([producttalk.org Claude Code Features](https://www.producttalk.org/how-to-use-claude-code-features/)). This is useful for architectural research where the goal is understanding structure, not making changes.

### 3.5 Cost Optimization via Model Routing

Set `CLAUDE_CODE_SUBAGENT_MODEL` to run lighter models on subagents while maintaining the main session on Opus. "This cuts costs significantly without sacrificing quality on well-scoped sub-agent work" `[PRAC]` ([claudefa.st Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)). For research subagents that primarily search and read, Haiku or Sonnet is often sufficient. Reserve Opus for the synthesis/aggregation step.

---

## 4. Foreground vs Background Agents

### 4.1 Execution Modes

Claude Code subagents can run in three modes `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)):

1. **Foreground (blocking):** Main conversation waits for subagent to complete. Permission prompts pass through to the user. Use when the result is needed before proceeding.
2. **Background (non-blocking):** Main conversation continues while subagent works. User is notified on completion. Press `Ctrl+B` to move a foreground agent to background mid-execution. Monitor with `/tasks`.
3. **Always-background:** Set `background: true` in agent frontmatter to always run as background task.

### 4.2 When to Use Each for Research

**Foreground** -- when the research result is a prerequisite for the next step:
- Investigating a codebase pattern before deciding on an implementation approach
- Checking whether a dependency exists before proposing architecture
- Any research where the answer determines the next action

**Background** -- when research can proceed independently:
- Web research and documentation lookups
- Codebase exploration and analysis that will be reviewed later
- Security audits and performance profiling
- Multiple parallel research threads that will be synthesized after all complete

**Best pattern for multi-topic research:** Launch all research agents as background tasks, continue with any work that doesn't depend on their results, then synthesize when all complete. "Background agents batch permissions upfront" unlike foreground agents which prompt interactively `[PRAC]` ([claudefa.st Async Workflows](https://claudefa.st/blog/guide/agents/async-workflows)).

### 4.3 The Permission Pre-Approval Pattern

Background agents cannot interrupt for permission prompts. Before launching, Claude Code prompts for all tool permissions the subagent will need upfront `[PRAC]` ([claudefa.st Async Workflows](https://claudefa.st/blog/guide/agents/async-workflows)). For research agents that only read, this is trivial -- read-only tools rarely need permission. For agents that write results to files, ensure write permissions are granted before backgrounding.

---

## 5. Agent Isolation

### 5.1 Worktree Isolation Mechanism

Setting `isolation: worktree` in agent frontmatter gives each subagent its own git worktree -- a separate working copy that shares git history but has its own file tree `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)). Worktrees are automatically cleaned up when the subagent finishes without changes `[PRAC]` ([claudefa.st Worktree Guide](https://claudefa.st/blog/guide/development/worktree-guide)).

### 5.2 When Worktree Isolation Helps Research

**Useful when:**
- Multiple agents need to write research artifacts to the same directory
- Research agents run code (tests, benchmarks, build commands) that modify local state
- Agents explore different git branches or historical states
- Protection against one agent's file writes corrupting another's workspace

**Not useful when:**
- Research is read-only (Explore agents, web search only)
- All agents write to distinct, non-overlapping files
- Research doesn't involve running code that modifies local state

### 5.3 The Merge Challenge

Worktree isolation creates branches that must be merged. For research tasks that only produce reports, this is trivial -- merge the report files. For implementation tasks with overlapping file edits, merge conflicts are expected and require careful review `[PRAC]` ([dandoescode.com Parallel Vibe Coding](https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees)).

### 5.4 Context Isolation (Without Worktrees)

Even without worktrees, subagents provide **context isolation** -- the primary benefit for research. Verbose exploration output stays in the subagent's 200K context window; only a summary returns to the main conversation. This is the "subagent-as-context-fence" pattern `[PRAC]` ([claudefa.st Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)). For pure research tasks, context isolation is usually sufficient without worktree isolation.

---

## 6. Result Aggregation

### 6.1 Inline Return (Default)

The parent receives the subagent's final message verbatim as the Agent tool result. Intermediate tool calls and results stay inside the subagent; only the final message returns `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)).

**Advantages:**
- Zero file I/O overhead
- Immediate availability in parent context
- Natural language summary, easy to synthesize

**Disadvantages:**
- Consumes parent context window -- running many agents that return detailed results fills the main context fast
- No persistent record unless parent writes it
- Large inline returns may be summarized/truncated by the parent

### 6.2 File-Based Aggregation

Instruct subagents to write structured output (JSON, Markdown) to specific files. Parent reads files to aggregate.

**Advantages:**
- Persistent -- survives context compaction and session interruption
- Can handle arbitrarily large outputs without consuming parent context
- Structured data (JSON) enables programmatic aggregation
- Multiple agents can write to separate files without conflict

**Disadvantages:**
- File I/O overhead
- Requires coordination on file naming and location
- Parent must read files (additional tool calls)

**Recommended pattern:** "Spin off multiple read-only analysis agents in parallel and aggregate their JSON outputs in the main thread" `[PRAC]` ([pubnub.com Best Practices](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)).

### 6.3 Hybrid Strategy (Recommended for Research)

For research orchestration, the optimal pattern combines both approaches:

1. **Each research subagent** writes detailed findings to a file (e.g., `/tmp/research-{topic}.md`) AND returns a brief summary inline
2. **The parent** receives summaries immediately for quick synthesis
3. **For deep synthesis**, the parent reads the detailed files
4. This preserves parent context (short summaries) while retaining detail (files)

### 6.4 Agent Teams: Shared Task List

Agent Teams use a shared task list at `~/.claude/tasks/{team-name}/` with file-locking for claim races. Teammates self-claim tasks, and automatic unblocking occurs when dependencies complete. A reviewer teammate can validate each task completion before the lead sees it `[PRAC]` ([The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)).

---

## 7. Error Handling and Retries

### 7.1 Current State: Limited Diagnostic Context

When a subagent fails, the orchestrator receives the subagent's working transcript (all tool calls and results up to the crash point) but **no structured metadata** distinguishing "completed successfully" from "crashed mid-execution." There is no formal checklist to verify coverage `[ISSUE]` ([GitHub #25818](https://github.com/anthropics/claude-code/issues/25818)).

### 7.2 Common Failure Modes

1. **Token budget exceeded:** Subagent hits context window limit mid-task. The transcript is incomplete but the orchestrator may not realize it `[ISSUE]` ([GitHub #25818](https://github.com/anthropics/claude-code/issues/25818)).
2. **Max turns reached:** Subagent hits `maxTurns` limit before completing. Partial results exist but may be incomplete.
3. **Tool error:** A specific tool call fails (permission denied, file not found). May cascade if the agent doesn't recover.
4. **Internal crash:** `classifyHandoffIfNeeded is not defined` and similar internal errors `[ISSUE]` ([GitHub #25818](https://github.com/anthropics/claude-code/issues/25818)).

### 7.3 Problematic Recovery Patterns

Two anti-patterns are well-documented `[ISSUE]` ([GitHub #25818](https://github.com/anthropics/claude-code/issues/25818)):

1. **Blind resubmission:** Orchestrator re-dispatches identical task to a new subagent. New agent hits the same failure. Cycle repeats, burning parent context on each attempt.
2. **Confident fabrication:** Orchestrator announces the agent encountered an issue but proceeds to answer by inferring/hallucinating what the subagent would have found. Results presented with false confidence are indistinguishable from verified findings.

### 7.4 Best Practices for Error Recovery

Based on community patterns and the GitHub issue discussion:

- **Token budget exceeded:** Do NOT retry. Report partial results, suggest narrower follow-up queries `[ISSUE]` ([GitHub #25818](https://github.com/anthropics/claude-code/issues/25818)).
- **Internal crash:** Retry once. If second failure, report to user `[ISSUE]` ([same issue](https://github.com/anthropics/claude-code/issues/25818)).
- **Max turns reached:** Return partial results. Ask user whether to continue with a follow-up agent.
- **Tool error:** Diagnose which tool failed. Fix precondition before retrying.
- **Never fabricate:** If a subagent returned no results, say so. Inferring/hallucinating is worse than returning nothing.

### 7.5 Defensive Patterns

- **Set `maxTurns` explicitly:** Prevents runaway subagents. "Every teammate gets a hard MAX_ITERATIONS=8" with forced reflection prompts `[PRAC]` ([The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)).
- **Kill criteria:** "If an agent becomes stuck for 3+ iterations on the same error, kill and reassign to a fresh agent" `[PRAC]` ([same source](https://addyosmani.com/blog/code-agent-orchestra/)).
- **Token budgets as hard stops:** e.g., "Frontend 180k tokens, Backend 280k tokens" `[PRAC]` ([same source](https://addyosmani.com/blog/code-agent-orchestra/)).
- **Validation hooks:** `TaskCompleted` hook runs lint and tests, preventing progression if validation fails `[PRAC]` ([same source](https://addyosmani.com/blog/code-agent-orchestra/)).
- **Structured output requirements:** Instruct subagents to produce checklists of what they covered. This enables the parent to verify coverage even from a crashed transcript.

### 7.6 Circuit Breaker Pattern

For production SDK usage, the circuit breaker pattern is recommended: CLOSED (normal operation) -> OPEN (failures exceed threshold, requests fail fast) -> HALF_OPEN (testing if service recovered). Exponential backoff with jitter (1s, 2s, 4s, 8s, 16s, with +/-25% jitter) prevents thundering herd problems `[PRAC]` ([claudelab.net Self-Healing Agents](https://claudelab.net/en/articles/api-sdk/claude-api-self-healing-agent-production-patterns)).

---

## 8. Research-Specific Orchestration Recommendations

Synthesizing all findings, here are recommendations specifically for research task orchestration:

### 8.1 Decomposition

- **Decompose by subtopic**, not by depth level or source type. Each agent gets one research question.
- **3-5 parallel research agents** is the sweet spot. More than 5 creates synthesis overhead that exceeds the parallelism gains.
- **Scope each agent narrowly.** A well-scoped agent with 3-5 search queries outperforms a broad agent trying to cover everything.

### 8.2 Agent Configuration

- **Use Explore (Haiku) for codebase research** -- fast, cheap, read-only.
- **Use general-purpose (Sonnet) for web research** -- needs WebSearch, WebFetch tools.
- **Reserve Opus for synthesis** -- the parent or a dedicated synthesis agent that reads all results and produces the final report.
- **Set `maxTurns` to 15-20** for research agents. Research rarely needs more turns, and unbounded agents waste tokens.

### 8.3 Execution

- **Launch all research agents as background tasks.** Use `/tasks` to monitor.
- **No worktree isolation needed** for pure research (read-only + file writes to distinct paths).
- **Instruct agents to write findings to files AND return a summary.** Hybrid aggregation preserves parent context while retaining detail.

### 8.4 Synthesis

- **Wait for all agents to complete** before synthesizing. Partial synthesis leads to rework.
- **Read the detail files, not just the summaries.** Summaries lose nuance; synthesis quality depends on the synthesizer seeing primary data.
- **Cross-reference findings across agents.** Conflicting findings between agents are high-value signals -- investigate rather than arbitrarily choosing one.

---

## 9. Gaps and Limitations

### 9.1 Missing from Official Documentation

- **No official guidance on optimal agent count for research tasks.** The 3-5 recommendation comes from implementation/coding contexts. Research may have different characteristics (lower per-agent cost, higher synthesis cost).
- **No documentation on Explore thoroughness level internals.** What "quick" vs "medium" vs "very thorough" actually means in terms of tool calls, token budget, or search strategy is not specified.
- **No official error recovery guidance for subagents.** The structured failure payload proposed in GitHub #25818 does not exist. Error handling is entirely ad hoc.
- **No built-in result aggregation patterns.** File-based vs inline return is left to the user with no framework support.

### 9.2 Architectural Constraints

- **No subagent nesting.** Subagents cannot spawn other subagents, eliminating hierarchical decomposition for non-Agent Teams workflows `[OFFICIAL]` ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)).
- **No `maxParallelAgents` setting.** Unbounded spawning remains a system stability risk. The feature request was closed without response `[ISSUE]` ([GitHub #15487](https://github.com/anthropics/claude-code/issues/15487)).
- **No structured failure metadata.** The orchestrator cannot distinguish successful completion from mid-execution crash `[ISSUE]` ([GitHub #25818](https://github.com/anthropics/claude-code/issues/25818)).
- **Agent Teams are experimental.** The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` flag is required. Resumption (`/resume`, `/rewind`) does not restore teammates.

### 9.3 Evidence Gaps

- **No controlled studies** comparing decomposition strategies (by subtopic vs by source type vs by depth) for research quality.
- **No benchmarks** for research agent count vs output quality. The 3-5 recommendation is based on coding task efficiency, not research thoroughness.
- **Token cost data is approximate.** "3-4x tokens for 3 agents" is a rough practitioner estimate, not a controlled measurement.
- **No data on Explore agent quality by thoroughness level.** Whether "very thorough" actually finds more than "medium" at what cost ratio is undocumented.
- **The C compiler case study (16 agents, $20K) is the only large-scale first-party case study.** Generalizability to research tasks is uncertain -- the task had perfectly independent subtasks (failing tests) which is atypical for research.

### 9.4 Open Questions

1. **Does research quality degrade with agent count?** More agents produce more findings, but does synthesis quality drop when the parent must integrate 8+ agent reports?
2. **What is the optimal balance between agent count and agent depth?** Is it better to run 3 thorough agents (20 turns each) or 6 quick agents (8 turns each) for the same token budget?
3. **How should conflicting findings from parallel agents be resolved?** No documented pattern exists for adjudicating disagreements between research agents.
4. **Does model routing (Haiku for search, Opus for synthesis) actually improve research quality?** Or does running everything on Opus produce better results despite the cost?

---

## Sources

- [Create custom subagents -- Anthropic Official Docs](https://code.claude.com/docs/en/sub-agents)
- [Building a C compiler with a team of parallel Claudes -- Anthropic Engineering](https://www.anthropic.com/engineering/building-c-compiler)
- [The Code Agent Orchestra -- Addy Osmani](https://addyosmani.com/blog/code-agent-orchestra/)
- [Claude Code Sub-Agents: Parallel vs Sequential Patterns -- claudefa.st](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)
- [Claude Code Agent Teams: Setup & Usage Guide -- claudefa.st](https://claudefa.st/blog/guide/agents/agent-teams)
- [Claude Code Async: Background Agents & Parallel Tasks -- claudefa.st](https://claudefa.st/blog/guide/agents/async-workflows)
- [Claude Code Worktrees: Run Parallel Sessions Without Conflicts -- claudefa.st](https://claudefa.st/blog/guide/development/worktree-guide)
- [GitHub Issue #15487: maxParallelAgents Feature Request](https://github.com/anthropics/claude-code/issues/15487)
- [GitHub Issue #25818: Orchestrator Lacks Diagnostic Context on Subagent Failure](https://github.com/anthropics/claude-code/issues/25818)
- [Best practices for Claude Code subagents -- PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Claude Code Subagents and Main-Agent Coordination -- Rick Hightower / Medium](https://medium.com/@richardhightower/claude-code-subagents-and-main-agent-coordination-a-complete-guide-to-ai-agent-delegation-patterns-a4f88ae8f46c)
- [Mastering Claude Code's Agent Features -- Claude Lab](https://claudelab.net/en/articles/claude-code/claude-code-agent-guide)
- [Claude Code Agents & Subagents: What They Actually Unlock -- ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)
- [Building Self-Healing AI Agents -- Claude Lab](https://claudelab.net/en/articles/api-sdk/claude-api-self-healing-agent-production-patterns)
- [How to run Claude Code in parallel -- Ona](https://ona.com/stories/parallelize-claude-code)
- [Parallel Vibe Coding with Git Worktrees -- Dan Does Code](https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees)
- [How to Use Claude Code Features -- ProductTalk](https://www.producttalk.org/how-to-use-claude-code-features/)
- [Claude Code Agents: Complete Guide -- ClaudeWorld](https://claude-world.com/articles/agents-guide/)
