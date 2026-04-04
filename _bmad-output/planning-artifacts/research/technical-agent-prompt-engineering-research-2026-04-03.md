# Technical Research: Prompt Engineering for Research Subagents in Claude Code

**Date:** 2026-04-03
**Status:** Complete
**Scope:** Best practices for prompting, briefing, and scoping research subagents spawned via the Claude Code Agent tool

---

## 1. Effective Agent Briefing Patterns

The Claude Code documentation advises treating subagent prompts like a briefing for "a smart colleague who just walked into the room." In practice, this means the prompt string passed to the Agent tool is the **only channel** from parent to subagent --- the subagent receives no conversation history, no prior tool results, nothing except its system prompt plus your prompt string and basic environment details like the working directory ([Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents)).

Anthropic's own multi-agent research system learned this the hard way. They started by allowing the lead agent to give simple, short instructions like "research the semiconductor shortage," but found these instructions "often were vague enough that subagents misinterpreted the task or performed the exact same searches as other agents." In one case, "one subagent explored the 2021 automotive chip crisis while 2 others duplicated work investigating current 2025 supply chains, without an effective division of labor" ([Anthropic Engineering: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)).

**What a good briefing includes:**

- **Objective:** What specific question the subagent should answer, stated explicitly.
- **Output format:** What the result should look like (structured findings, file path to write, inline summary).
- **Tool and source guidance:** Which tools to prefer, what sources to consult.
- **Task boundaries:** What is in scope and what is explicitly out of scope.
- **Prior context:** What has already been tried, ruled out, or discovered, so the subagent does not duplicate work.

The PubNub best-practices guide distills this to: "Give each subagent one clear goal, input, output, and handoff rule. Keep descriptions action-oriented" --- for example, "Use after a spec exists; produce an ADR and guardrails" rather than a vague "Reviews architecture" ([PubNub: Best Practices for Claude Code Sub-Agents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)).

**Good vs. bad prompt examples:**

| Quality | Prompt |
|---------|--------|
| Bad | "Research agent logging approaches" |
| Good | "Investigate structured logging libraries for TypeScript serverless environments. Compare pino, winston, and console-based approaches on: cold start impact, structured JSON output, log level filtering, and Lambda compatibility. We've already ruled out bunyan (unmaintained). Return a comparison table and a recommendation with rationale." |

The bad prompt is a terse command that gives no scope, no exclusions, no output format, and no boundaries. The good prompt explains what, why, what has been ruled out, and what form the answer should take.

## 2. Context Provision: The Goldilocks Problem

Anthropic's context engineering guide frames this as finding "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Every token competes for model attention, and research shows that "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases" --- a phenomenon called context rot ([Anthropic Engineering: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Too little context** produces shallow, generic results. The subagent lacks the judgment to make domain-appropriate decisions and falls back to surface-level web knowledge.

**Too much context** degrades performance. One practitioner observed that "by the time you hit two-thirds capacity, response quality degrades noticeably, not because the model is worse, but because the context is full of noise" ([ksred: Claude Code Agents & Subagents](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)).

**Practical guidelines:**

1. **Include what you have already tried or ruled out.** This prevents the single most common failure mode: the subagent duplicating work the parent has already done. Anthropic's research system specifically solved duplication by giving each subagent distinct, non-overlapping search boundaries.

2. **Include file paths, error messages, or architectural decisions** the subagent needs. These are concrete, low-token, high-signal items.

3. **Do not dump entire conversation history.** The subagent gets its own 200K-token context window. Let it do its own exploration rather than pre-loading it with stale intermediate results.

4. **Use progressive disclosure.** Anthropic recommends agents "maintain lightweight identifiers (file paths, stored queries, web links) and use these references to dynamically load data into context at runtime using tools" rather than pre-loading everything upfront.

5. **Describe the "why" behind the research.** A subagent that understands the motivation can make better judgment calls about relevance than one that only knows the literal question.

## 3. Output Format Instructions

Whether a subagent should write files or return inline depends on the task:

| Scenario | Recommendation |
|----------|---------------|
| Research findings that feed into further reasoning | Return inline to parent |
| Artifacts with independent value (specs, reports, config) | Write to a file |
| Structured data for comparison | Specify table/JSON format explicitly |
| Exploratory findings | Narrative inline with key takeaways highlighted |

The PubNub guide recommends explicit "Definition of Done" checklists per agent role: the PM agent produces "acceptance criteria + clarifying questions," the architect produces "ADR + guardrails," the implementer produces "code + passing tests + summary." When the DoD is missing, "stop and fix" ([PubNub: Best Practices](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)).

Anthropic's context engineering guide recommends **structured guidance over narrative instruction**: use "explicit sections and clear delineation (XML tags, Markdown headers)" and provide "structured examples showing expected format rather than describing it narratively" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

A key architectural benefit of subagents is context isolation: "All the intermediate noise stays inside the subagent's context and never touches the parent's conversation" ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)). This means the parent only receives the final distilled output, regardless of how many files the subagent read or how many searches it ran.

## 4. Task Scoping: Narrow vs. Broad

Anthropic's research system embeds explicit scaling rules based on query complexity:

- **Simple fact-finding:** 1 agent, 3--10 tool calls
- **Direct comparisons:** 2--4 subagents, 10--15 calls each
- **Complex research:** 10+ subagents with "clearly divided responsibilities"

The purpose is to "help the lead agent allocate resources efficiently and prevent overinvestment in simple queries" ([Anthropic: Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system)).

**Risks of over-specification:** The agent follows instructions too literally, missing relevant adjacent information. Anthropic's context engineering guide warns against "hardcoding complex, brittle logic in prompts to elicit exact agentic behavior" because this "creates fragility and increases maintenance complexity over time." The recommendation is to write prompts that are "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Risks of under-specification:** The agent goes off track, duplicates work, or produces generic results. This was Anthropic's primary finding when building their research system --- vague instructions caused subagents to "misinterpret the task or perform the exact same searches as other agents."

**The sweet spot:** Give the subagent a clear objective and explicit boundaries, but leave the method flexible. Specify *what* to find and *what to exclude*, but let the agent decide *how* to search.

## 5. Agent Type Matching

Claude Code provides three built-in subagent types with different capabilities:

### Explore Agent
- **Model:** Haiku (fast, cheap)
- **Tools:** Read-only (no Write, no Edit)
- **Purpose:** File discovery, code search, codebase exploration
- **Context:** Starts fresh (does not inherit parent context)
- **Thoroughness:** Accepts `quick`, `medium`, or `very thorough` levels
- **Best for:** Bounded codebase questions where speed matters and write access is unnecessary

### Plan Agent
- **Model:** Inherits from main conversation
- **Tools:** Read-only (no Write, no Edit)
- **Purpose:** Codebase research for architectural planning
- **Context:** Inherits full parent context
- **Best for:** Understanding codebase structure before proposing changes

### General-Purpose Agent
- **Model:** Inherits from main conversation
- **Tools:** All tools (read, write, edit, bash, MCP)
- **Context:** Inherits full parent context
- **Best for:** Complex multi-step tasks requiring both exploration and modification

([Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents))

**Practical guidance:** One practitioner recommends using "2-3 focused information-gathering agents running in parallel, with the main session synthesising their outputs" for research tasks ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)). For research specifically, the Explore agent is often sufficient --- it runs on Haiku for speed and cost savings, and the read-only constraint prevents accidental modifications.

However, the Explore agent's summaries are lossy. One practitioner warns to "have Claude read relevant files itself" after an Explore pass returns pointers, because "summaries compress information lossy" ([Sankalp: Guide to Claude Code 2.0](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/)).

For research tasks that need web access, file creation, or multi-step reasoning, the general-purpose agent is required. Custom subagents can also be created with specific tool sets --- for example, a research agent with Read, Grep, Glob, Bash, and WebSearch but no Write or Edit.

## 6. Iterative Refinement

### Continuing Existing Agents (SendMessage)

Claude Code supports resuming subagents via the `SendMessage` tool, available when agent teams are enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Resumed subagents "retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh" ([Claude Code Docs](https://code.claude.com/docs/en/sub-agents)).

### When to Continue vs. Spawn New

| Situation | Action |
|-----------|--------|
| Initial results are partial but on track | Continue via SendMessage with specific follow-up questions |
| Initial results missed the point entirely | Spawn a new agent with a better-scoped prompt |
| Need to explore a different facet | Spawn a new agent --- fresh context avoids cross-contamination |
| Results need validation or adversarial review | Spawn a separate reviewer agent |

### Iterative Prompt Refinement

Anthropic discovered that "Claude 4 models can be excellent prompt engineers." When shown "a prompt and a failure mode, they are able to diagnose why the agent is failing and suggest improvements." They built a tool-testing agent that "attempts to use the tool and then rewrites the tool description to avoid failures," achieving "a 40% decrease in task completion time for future agents using the new description" ([Anthropic: Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system)).

A practical loop for iterative refinement: the main agent sends results to a reviewer subagent, which provides feedback, and the main agent feeds that feedback back to the implementing agent "until the reviewer is satisfied" ([Rick Hightower: Claude Code Subagents Guide](https://medium.com/@richardhightower/claude-code-subagents-and-main-agent-coordination-a-complete-guide-to-ai-agent-delegation-patterns-a4f88ae8f46c)).

## 7. Meta-Prompting Patterns

Meta-prompting changes the model's role from performer to conductor: "instead of doing the work directly, it plans and orchestrates how the work gets done" ([Prompting Guide: Meta Prompting](https://www.promptingguide.ai/techniques/meta-prompting)).

**Key meta-prompting patterns for research subagents:**

1. **"Explain what you are trying to accomplish and why."** This forces the subagent to establish purpose before diving into execution, preventing the common failure mode of jumping to conclusions without adequate grounding.

2. **"Describe what you have already learned."** Encourages the agent to synthesize intermediate findings, which improves coherence and surfaces gaps in reasoning.

3. **"Give enough context for judgment calls."** When the subagent encounters ambiguity, it needs domain context to resolve it. Without this, it defaults to the most generic interpretation.

4. **Scaling rules.** Anthropic embeds explicit effort calibration: simple queries get minimal tool calls, complex queries get deep investigation. Without this, agents either "scour the web endlessly for nonexistent sources" or under-invest in queries that need depth.

5. **Hypothesis tracking.** For research tasks, prompting the agent to "develop several competing hypotheses, track confidence levels, regularly self-critique approach and plan" improves depth and prevents premature convergence on the first plausible answer.

6. **Source verification.** Explicitly instructing agents to verify sources prevents hallucinated citations --- a common failure mode in research tasks.

Anthropic's context engineering guide recommends the **minimal information approach**: "Start with the minimal set of information that fully outlines your expected behavior. This doesn't mean brevity --- agents still need sufficient upfront information to adhere to desired behavior. Test with the best available model first, then add clarity based on observed failures" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

## 8. Common Prompt Anti-Patterns

### Terse Command-Style Prompts
Short, imperative prompts like "research X" or "find Y" produce shallow results because the agent has no boundaries, no exclusions, no output format, and no prior context. Anthropic's research system documented this as their primary early failure mode.

### Over-Spawning
"Claude Opus has a known tendency to over-spawn subagents" --- Anthropic's own documentation flags that Opus "will delegate to agents in situations where a direct approach would be faster and cheaper" ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)). Anthropic's research system found early versions creating "50 subagents for simple queries" ([Anthropic: Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system)).

### Context Gatekeeping
Creating specialized subagents can backfire by "gatekeeping context --- if you make a specialized subagent, you have hidden context from the main agent, which can no longer reason holistically about changes" ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)).

### Tool Bloat
Designing "bloated tool sets that cover too much functionality or lead to ambiguous decision points" is an anti-pattern. The test: "if humans can't definitively choose which tool applies, agents can't either" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### Excessive Edge-Case Enumeration
Attempting to "articulate every possible rule the LLM should follow for a particular task" by listing exhaustive edge cases degrades performance. Use "diverse, canonical examples that effectively portray the expected behavior" instead --- "for LLMs, examples are the pictures worth a thousand words" ([Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### Lazy Delegation
The coordinator must synthesize findings before delegating further work. "Based on your findings, do X" without actually reviewing those findings creates a delegation chain where no agent takes responsibility for quality ([Rick Hightower](https://medium.com/@richardhightower/claude-code-subagents-and-main-agent-coordination-a-complete-guide-to-ai-agent-delegation-patterns-a4f88ae8f46c)).

### Skipping the Explore-Then-Read Pattern
Using Explore subagents to find files but not reading the files afterward. Explore returns summaries, and "summaries compress information lossy." The main agent should read the actual files the Explore agent identified ([Sankalp](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/)).

### Endless Searching
Without explicit effort bounds, agents "scour the web endlessly for nonexistent sources." Embed scaling rules that cap tool calls based on task complexity ([Anthropic: Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system)).

## 9. Gaps and Limitations

### Limited First-Party Guidance
Anthropic's official documentation on the Agent tool prompt parameter is surprisingly thin. The docs describe the mechanical API (parameters, frontmatter fields, tool restrictions) but provide few examples of well-crafted prompt strings for different task types. Most practical guidance comes from community blog posts and practitioner reports rather than official sources.

### No Formal Prompt Templates
There is no published library of validated prompt templates for common subagent tasks (research, code review, refactoring, testing). The community-maintained repositories like [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) and [claude-code-prompts](https://github.com/repowise-dev/claude-code-prompts) are independently authored and not validated by Anthropic.

### Agent Teams Are Experimental
The `SendMessage` continuation mechanism requires an experimental flag (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). This means iterative refinement patterns involving agent-to-agent communication are not yet stable or generally available.

### Subagents Cannot Spawn Subagents
This architectural constraint prevents recursive decomposition patterns. If a research task naturally requires multi-level decomposition, the orchestrator must handle all delegation directly, which can strain the orchestrator's context.

### No Shared Memory Between Subagents
Subagents in the same session cannot share findings directly. Each subagent returns its output to the parent, which must manually relay relevant context to other subagents. This creates a bottleneck at the coordinator level and can lead to the coordinator becoming a context dump.

### Reliability of Auto-Delegation
Multiple sources report that Claude's automatic delegation to custom subagents based on description matching is unreliable. Claude "frequently handles tasks in the main session rather than delegating to a defined agent, even when the agent is explicitly relevant and its description matches the task" ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)). Workarounds include adding "use PROACTIVELY" or "MUST BE USED" to description fields.

### Cost and Rate Limits
Running parallel subagents on paid plans can hit rate limits quickly. One practitioner reports that "running five agents simultaneously on the Pro plan is a reliable way to hit rate limits in under twenty minutes" ([ksred](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)). This constrains parallelism strategies in practice.

### Research-Specific Gaps
There is minimal published guidance on prompting research agents specifically (as opposed to coding agents). Anthropic's multi-agent research system paper is the closest, but it describes a custom-built system, not patterns for the Agent tool directly. The translation from their system's architecture to Claude Code's Agent tool is left as an exercise for the reader.

---

## Sources

- [Claude Code Docs: Create Custom Subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic Engineering: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic Engineering: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [PubNub: Best Practices for Claude Code Sub-Agents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [PubNub: Best Practices Part II — From Prompts to Pipelines](https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/)
- [ksred: Claude Code Agents & Subagents: What They Actually Unlock](https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/)
- [Sankalp: A Guide to Claude Code 2.0](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/)
- [Rick Hightower: Claude Code Subagents and Main-Agent Coordination (Medium)](https://medium.com/@richardhightower/claude-code-subagents-and-main-agent-coordination-a-complete-guide-to-ai-agent-delegation-patterns-a4f88ae8f46c)
- [Piebald-AI: Claude Code System Prompts (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts)
- [claudefa.st: Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)
- [alexop.dev: Claude Code Customization Guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/)
- [Prompting Guide: Meta Prompting](https://www.promptingguide.ai/techniques/meta-prompting)
- [Prompting Guide: LLM Agents](https://www.promptingguide.ai/research/llm-agents)
- [morphllm: Agent Engineering](https://www.morphllm.com/agent-engineering)
- [Anthropic: Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [DEV Community: The Task Tool — Claude Code's Agent Orchestration System](https://dev.to/bhaidar/the-task-tool-claude-codes-agent-orchestration-system-4bf2)
- [Anthropic Courses: Introduction to Subagents](https://anthropic.skilljar.com/introduction-to-subagents)
