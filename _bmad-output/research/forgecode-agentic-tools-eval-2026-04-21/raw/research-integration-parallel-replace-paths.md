---
content_origin: claude-code-subagent
date: 2026-04-21
sub_question: "For ForgeCode and the strongest peers, describe three concrete pathways: (a) plug in as a specialist co-processor alongside Claude Code (cheap model routing, parallel review, sandboxed sub-agent); (b) run Momentum-equivalent practice in parallel on the tool (as once imagined for Cursor); (c) migrate parts or all of Momentum onto it. What does each look like in practice, and what are the tradeoffs?"
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

# Integration, Parallel-Track, and Migration Pathways

This brief evaluates four candidate tools against Momentum's Claude-Code-centric practice: **ForgeCode** (antinomyhq/forgecode), **OpenCode** (sst/opencode), **Goose** (block/goose), and **Aider** as the wildcard. For each tool, three pathways are considered: (a) specialist co-processor alongside Claude Code, (b) parallel Momentum-equivalent practice on the tool, (c) partial or full migration.

Evidence tags: [OFFICIAL] = vendor docs/repos; [PRAC] = practitioner/community write-ups; [UNVERIFIED] = inference or unsourced claim.

## Decision Matrix

| Tool        | (a) Co-Processor | (b) Parallel Track | (c) Migration | One-line justification |
|-------------|------------------|--------------------|---------------|-----------------------|
| **ForgeCode** | Viable            | Viable              | Risky          | YAML-front-matter custom agents and MCP are strong; harness is still centralized around .forge/, no rich hook lifecycle like Claude's — migration forfeits Momentum hooks. [OFFICIAL] |
| **OpenCode** | Recommended        | Recommended          | Viable         | Reads `.claude/skills/*/SKILL.md` and `CLAUDE.md` as fallbacks — skill portability is near-free. 25+ lifecycle hooks + JS/TS plugins cover Momentum's hook needs. [OFFICIAL] |
| **Goose**    | Recommended        | Viable               | Risky          | Sub-agents + sub-recipes are a natural co-processor pattern; YAML recipes don't map cleanly onto Momentum's workflow.md skills; runtime is Rust, extensions via MCP only. [OFFICIAL] |
| **Aider**    | Recommended (narrow) | Not Recommended    | Not Recommended | Excellent architect/editor split for cheap bulk edits; no skill/agent/hook primitives — would require rebuilding the entire practice scaffold. [PRAC] |

---

## Preamble: What Momentum Actually Needs

Before judging pathways, pin down what Momentum's primitives require from a host:

1. **File-authoritative rules** — plain markdown in a conventional directory, auto-loaded into context.
2. **Skills with workflows** — `SKILL.md` + sibling `workflow.md` + templates; skills discover and invoke each other.
3. **Hooks** — PreToolUse / PostToolUse / Stop / SessionStart shell commands the harness runs automatically.
4. **Agent definitions** — subagents with isolated context, custom prompts, tool whitelists, and model selection.
5. **Sub-agent spawning from skills** — the orchestrator can fan out N parallel workers.
6. **Plan mode / read-only mode** — AVFL and sprint-status need a non-mutating lane.
7. **External process control** — CMUX panes, DuckDB audits, git worktrees.

Claude Code provides all seven. [OFFICIAL — https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/sub-agents] Any alternative must provide (1)–(5) at minimum to host Momentum; (6)–(7) can be polyfilled with shell.

---

## ForgeCode

ForgeCode (antinomyhq/forgecode) is a terminal coding harness that supports 300+ models via OpenRouter and ships a built-in 3-agent architecture (Muse plans, Forge executes, Sage researches). [OFFICIAL — https://github.com/antinomyhq/forgecode] As of April 2026 it holds the #1 spot on Terminal-Bench 2.0 at 81.8%. [PRAC — Hightower, Medium, Apr 2026]

### (a) Specialist co-processor

**Integration shape.** Expose ForgeCode through a thin MCP server or a bash tool invoked via Claude Code's PreToolUse/PostToolUse hook. Because ForgeCode has a non-interactive mode (`forge -p "<prompt>"`), it can be called as a subprocess from a Momentum skill — e.g. the `momentum:dev` skill could shell out to ForgeCode for a bulk-edit sub-task.

- **Momentum primitive it rides on:** `agent_definition` (a new `forgecode-bulk-editor` subagent that wraps the ForgeCode CLI) or a skill step that shells out.
- **Cost/latency benefit:** ForgeCode routes through OpenRouter with no markup [OFFICIAL — forgecode.dev/blog graduating-from-early-access], so Momentum can route bulk refactors to DeepSeek-V3 or Qwen-Coder at 5–10x lower $/token than Sonnet. [UNVERIFIED cost; model availability OFFICIAL per OpenRouter.]
- **Parallel review lane.** Because ForgeCode's harness is distinct from Claude Code, running ForgeCode on the same diff is genuinely adversarial — different prompt, different model, different tool call patterns. This gives Momentum's AVFL a second architecture to catch blind spots Claude shares with its own critics.
- **Failure modes.** (1) No structured output contract — parsing ForgeCode's natural-language response into AVFL findings needs a post-processor. (2) ForgeCode writes to disk; running it in parallel on the same worktree is unsafe. Must sandbox in a sibling worktree. (3) Its indexing (`:sync`) sends file content to `api.forgecode.dev` by default [OFFICIAL — docs] — a data-egress concern for private code.

**Verdict: Viable.** Narrow, well-scoped sub-tasks (bulk refactor, read-only audit) are a fit. Not recommended as a general parallel reviewer until the egress knob is fully understood.

### (b) Parallel Momentum-equivalent practice

ForgeCode provides most of the structural primitives Momentum relies on:

- **Custom agents** are markdown + YAML frontmatter in `.forge/agents/` (project) or `~/forge/agents/` (global). Frontmatter declares `id`, `tools`, `model`, `provider`, `temperature`, plus Handlebars templating via `user_prompt`. [OFFICIAL — forgecode.dev/docs/creating-agents]
- **Agent-as-tool delegation.** If an agent has a `description`, other agents can invoke it as a tool — this is ForgeCode's equivalent of subagent spawning.
- **MCP** is first-class; `mcp_*` glob in tool lists auto-pulls new servers.
- **No hook lifecycle** equivalent to Claude's PreToolUse/PostToolUse was found in the docs. This is the principal gap for Momentum.

**Minimum viable port.** `create-story`, `sprint-planning`, and `intake` are essentially markdown-generating skills that invoke subagents and write files; they would port with mechanical changes:
- Replace `.claude/skills/momentum/` with `.forge/agents/momentum-*.md`
- Rewrite skill `workflow.md` as system-prompt content inside the agent file
- Use `user_prompt` Handlebars to inject current date and context variables

**What requires rewriting.** Anything that depends on hooks — the `plan-audit` rule that fires before `ExitPlanMode`, the post-commit checkpoint hook, and the `cmux`/PostToolUse integrations — has no direct ForgeCode equivalent as of April 2026. These would need to move inside the agent's system prompt (brittle) or a wrapper script outside ForgeCode.

**Tradeoff.** You keep BMAD + CMUX. You lose ~30% of Momentum's enforcement surface (the hooks), which is precisely the layer that makes the practice file-authoritative rather than advisory.

**Verdict: Viable.** Good for a proof-of-concept where ForgeCode handles a limited slice (e.g. only `intake` + `create-story`).

### (c) Migration

**Clean migrations.** Skills that are pure subagent-spawn-and-compose (research, intake, distill) map to ForgeCode custom agents with minor edits.

**Hard blocks.** (1) No hook layer — Momentum's enforcement model (e.g. plan-audit, autonomous commit, architecture-guard PostToolUse drift detection) disintegrates. (2) TeamCreate/agent-to-agent SendMessage is a Claude Code feature [OFFICIAL — released Feb 2026 with Opus 4.6] that has no ForgeCode analog; Momentum's retro auditor team and sprint review team patterns cannot be rebuilt without polling loops. (3) No slash commands — Impetus's session-orientation UX collapses.

**What we'd gain.** Native OpenRouter = cheap models for everything, not just subagents. Harness-level benchmark leadership [PRAC]. Lighter cognitive load if the team is already OpenRouter-fluent.

**Effort estimate.** Full migration: **2–4 months**, largely spent reimplementing hooks as wrapper scripts and rebuilding the retro/AVFL team coordination patterns. Partial migration (e.g. only the "executor" layer): **2–3 weeks**.

**Verdict: Risky.** Hook loss and lack of team-coordination primitives are structural, not cosmetic.

---

## OpenCode (sst/opencode)

OpenCode is the Claude-Code-compatible open source coding agent. It explicitly reads `.claude/skills/*/SKILL.md`, `CLAUDE.md`, and related Claude conventions as fallbacks. [OFFICIAL — opencode.ai/docs/skills, opencode.ai/docs/rules]

### (a) Specialist co-processor

**Integration shape.** OpenCode has an HTTP API and a CLI with non-interactive invocation. A Momentum skill can shell out to OpenCode for read-only exploration on a cheap model (Haiku/DeepSeek/Qwen) and parse results. Alternatively, expose OpenCode as an MCP server to Claude Code.

- **Momentum primitive:** agent definition wrapping the OpenCode CLI, or an MCP tool. Because OpenCode has a built-in `plan` mode (read-only) [OFFICIAL — opencode.ai/docs/agents], it is naturally suited as the "read-only audit" lane.
- **Parallel review.** OpenCode reads the same `.claude/skills/` and `CLAUDE.md` Claude does, so a parallel review agent using OpenCode sees **the same rules** without porting — this is a nearly unique property among the peers.
- **Cost/latency benefit.** OpenCode natively supports per-agent model selection — a co-processor configured with `model: openrouter/deepseek-v3` costs a fraction of Sonnet and Claude Code's main agent can keep running Opus.
- **Failure modes.** OpenCode's forks (sst/opencode, anomalyco/opencode, opencode-ai/opencode) have diverged; picking the right fork matters. The TypeScript plugin system is the right abstraction but the ecosystem is young (<2 years).

**Verdict: Recommended.** Lowest-friction co-processor among the peers; rules and skills are already shared ground.

### (b) Parallel Momentum-equivalent practice

OpenCode's primitive coverage is the closest match to Claude Code:

| Momentum primitive       | OpenCode support                           | Notes |
|--------------------------|---------------------------------------------|-------|
| File-authoritative rules | `AGENTS.md` + `CLAUDE.md` fallback          | Direct. [OFFICIAL] |
| Skills                   | `SKILL.md` with shared format               | Near-identical. [OFFICIAL] |
| Hooks                    | 25+ lifecycle events via JS/TS plugins      | Different language, same concept. [OFFICIAL — opencode.ai/docs/plugins] |
| Agents                   | `.md` + YAML frontmatter, primary/sub mode  | Direct analog. [OFFICIAL] |
| Subagent spawning        | `@mention` + HTTP API                       | Direct. [OFFICIAL] |
| Plan mode                | Built-in read-only `plan` agent             | Direct. [OFFICIAL] |
| Model routing            | Per-agent model field, OpenRouter native    | Better than Claude Code's env-var approach. [PRAC] |

**Minimum viable port.** Effectively zero for skills and rules — they load from the existing paths. The port work is:
- **Hooks rewrite**: shell-based Momentum hooks (e.g. checkpoint-commit) become JS/TS plugin functions that subscribe to `tool.execute.after` and shell out via Bun's `$`. The practitioner evidence is that a 12-agent migration was done in a single day. [PRAC — Hightower gist]
- **Commands**: Claude's slash commands become OpenCode commands (separate format but mechanical).

**What stays same.** `CLAUDE.md`, every `SKILL.md`, every `workflow.md`, every rules file, every agent definition in `.claude/agents/`.

**Tradeoff.** You operate two harnesses against the same repo with the same rules. Split model bills: Claude Code on Anthropic direct, OpenCode on OpenRouter. Duplicate context of memory — both will read `CLAUDE.md` and both will load memory. Cognitive tax of "which tool am I in?" is real.

**Verdict: Recommended.** This is the single highest-leverage experiment. Minimal loss, direct skill reuse, independent model-cost curve.

### (c) Migration

**Clean migrations.** Skills, rules, agent definitions, CLAUDE.md — these move by flipping the harness.

**Moderate work.** Hooks become plugins. The Momentum hook set is small (<20 hooks from inspection of the repo structure), and each is short shell — translation is mechanical.

**What doesn't migrate.** (1) Claude's TeamCreate + SendMessage is the single hardest loss — Momentum's retro auditor team and sprint review team presume iterative inter-agent messaging. OpenCode's subagents are still fundamentally fan-out/collect. (2) Claude's `Task` and `Agent` tool semantics for subagent-can't-spawn-subagent are enforced; OpenCode is looser and needs explicit guardrails.

**What we'd gain.** (1) OpenRouter-native routing drops per-token cost 3–10x on routine work. [PRAC — Roo Code / Kilo Code + OpenRouter writeups] (2) The plugin API (JS/TS + Bun shell) is strictly more ergonomic than Claude's shell-command hooks for anything more than a one-liner. (3) Apache-2 license eliminates vendor-exit risk.

**Effort estimate.** Full migration: **3–6 weeks** (primarily the retro/sprint-review team coordination rewrite and hook port). Partial migration (let Impetus remain on Claude Code, run dev-wave on OpenCode): **1 week**.

**Verdict: Viable — the only viable full-migration target of the four.** The gating question is whether we can replace TeamCreate-style inter-agent dialogue with a polling pattern without losing quality.

---

## Goose (block/goose)

Goose is Block's Rust-based agent with an MCP-native extension model. As of April 2026 it has ~29K stars, 368 contributors, Apache-2 license, and 70+ documented MCP extensions. [OFFICIAL — github.com/block/goose; PRAC — Effloow review]

### (a) Specialist co-processor

**Integration shape.** Goose has a CLI with non-interactive invocation (`goose run --recipe <name>`). Momentum can invoke a Goose recipe as a specialist — e.g. database schema migration, changelog generation — tasks the community already has battle-tested recipes for. [PRAC — PulseMCP building-agents-with-goose]

- **Momentum primitive:** `agent_definition` that shells out to `goose run`, or an MCP server wrapping Goose.
- **Cost/latency.** Goose supports any LLM, including local models via Ollama — uniquely suited for running bulk work on a local GPU with zero API cost. [OFFICIAL]
- **Parallel review.** Goose's adversary-reviewer built-in is a useful second opinion lane; its prompt-injection detection is mature. [OFFICIAL]
- **Failure modes.** (1) Goose recipes are coarse-grained; invoking one for a Momentum subtask means carrying whatever recipe-wide extensions it declares. (2) Goose runs its own MCP extension stack, separate from Claude's — stacking both means 2x MCP subprocess overhead. (3) Recipe YAML differs from Claude skill YAML; no direct shared-format benefit like OpenCode.

**Verdict: Recommended (as a recipe-library specialist).** For discrete repeatable workflows (migrations, scaffolds) that the community has already codified, Goose recipes are drop-in. Not competitive with OpenCode for general-purpose co-processing because nothing is shared.

### (b) Parallel Momentum-equivalent practice

| Momentum primitive    | Goose support                                  | Notes |
|-----------------------|------------------------------------------------|-------|
| File-authoritative rules | `AGENTS.md` (core)                           | Present. [OFFICIAL] |
| Skills                | Recipes (YAML), Claude-Skill bridge discussed  | Structural mismatch — recipes are end-to-end workflows, not composable skills. [OFFICIAL — discussion #6202] |
| Hooks                 | No PreToolUse/PostToolUse hook lifecycle found | Primary gap. |
| Agents                | Sub-agents (experimental) + sub-recipes        | Two overlapping concepts, both experimental. [OFFICIAL — Block blog 2025-09-26] |
| Subagent spawning     | Native, parallel                                | Direct. [OFFICIAL] |
| Plan mode             | No first-class read-only agent                 | Polyfill required. |
| Model routing         | Any LLM, including local                        | Strongest of the four. [OFFICIAL] |

**Minimum viable port.** Goose recipes would host Momentum's "single shot" workflows (intake, distill, sprint-status). Anything requiring iterative fan-out + file-authoritative gating (sprint-dev, AVFL) hits the hook gap.

A **unified-tooling** RFC exists — Block is actively designing a bridge so recipes, subrecipes, Claude Skills, and Claude Subagents can interop. [OFFICIAL — github.com/block/goose/discussions/6202] If that lands, Goose's parallel-track viability improves materially.

**What requires rewriting.** (1) Every SKILL.md becomes a recipe YAML or an inverse bridge. (2) Hooks become recipe pre/post shell steps (less general than Claude hooks). (3) BMAD skills relied on by Momentum would all need bridges.

**Verdict: Viable but expensive.** Makes sense if Momentum wanted a local-model-first posture (zero egress, sovereign operation).

### (c) Migration

**Clean migrations.** Research, intake, distill: each is a self-contained recipe.

**Hard blocks.** (1) No hook lifecycle = losing the practice enforcement spine. (2) Recipe model is workflow-centric, not skill-centric — Momentum's "skills discover and compose other skills" pattern doesn't translate. (3) Rust runtime means any hook extension = Rust or a child-process hop.

**What we'd gain.** (1) Truly free local operation via Ollama/llama.cpp. (2) Strongest MCP ecosystem (3000+ servers). (3) Block's engineering team is demonstrably responsive [PRAC — 368 contributors].

**Effort estimate.** Full migration: **4–8 months** (waiting for unified-tooling RFC + rebuilding hooks as external scripts). Partial migration (use Goose as the local-model-first executor): **2–4 weeks**.

**Verdict: Risky.** The gap between recipe-YAML and Momentum's skill/workflow/hook trinity is wider than it looks. Revisit if the unified-tooling RFC ships.

---

## Aider (Wildcard)

Aider pioneered architect-mode and has the cleanest git workflow of the four (auto-commit per change). [PRAC — sanj.dev, effloow.com comparisons] It's a scalpel, not an operating system.

### (a) Specialist co-processor

**Integration shape.** Shell out to `aider --message "<prompt>" --yes <files>` from a Momentum skill when the task is "apply this specific change to these specific files". Aider's architect mode (plan with one model, apply with another) is battle-tested for cheap-model bulk editing.

- **Momentum primitive:** Agent definition `aider-bulk-editor` that wraps the CLI. Or a new skill `bulk-refactor` that invokes Aider directly.
- **Cost benefit.** Aider's architect pattern means you can plan with Opus (expensive, good) and apply with Haiku/DeepSeek (cheap, mechanical) — very close to Claude Code's Haiku-subagent pattern but with explicit architect/editor split. [PRAC — morphllm]
- **Parallel review.** Aider itself doesn't review; but pointing Aider at Claude Code's diff with a "critic" prompt is a cheap parallel-review lane.
- **Failure modes.** (1) Aider edits files directly — must run in a sibling worktree for safety. (2) No subagent system, no hooks, no skills — you're treating it as a unix tool, not a harness.

**Verdict: Recommended (narrow).** Specifically for bulk-edit + auto-commit scenarios where structure (hooks, skills) is overhead. A single `momentum:bulk-refactor` skill that wraps Aider would be high value.

### (b) Parallel Momentum-equivalent practice

Aider provides **none** of Momentum's structural primitives: no skills, no hooks, no agent definitions, no subagent spawning, no plan mode separation. You could store prompts in files and invoke them manually, but that's not Momentum — it's Aider with markdown notes.

**Verdict: Not Recommended.** Wrong tool for the job.

### (c) Migration

Same answer as (b) — you'd be rebuilding the practice scaffolding from scratch on a tool that doesn't want to host it.

**Verdict: Not Recommended.**

---

## Cross-Cutting Observations

### Shared-format tailwind

OpenCode's choice to honor `.claude/skills/*/SKILL.md` and `CLAUDE.md` has created a de facto portability layer. [OFFICIAL — opencode.ai/docs/skills] Block's unified-tooling RFC [OFFICIAL — discussion #6202] would extend this to Goose. The practical implication for Momentum: **keep authoring under `.claude/skills/` and `CLAUDE.md` regardless of host**, because this is the widest-compatible surface as of April 2026.

### The TeamCreate gap

Among the four, only Claude Code has a first-class inter-agent messaging primitive (`TeamCreate` + `SendMessage`, released Feb 2026). [OFFICIAL — claude.com/blog/subagents-in-claude-code] Momentum uses this in retro audits and sprint review. Any migration must either (a) wait for parity, (b) downgrade to polling/fan-out only, or (c) accept that "dialogue during execution" is a Claude-Code-only capability.

### Hooks are the sticky layer

Every non-Claude host has a weaker hook story. OpenCode comes closest with 25+ lifecycle events in JS/TS plugins. [OFFICIAL] ForgeCode has no found hook lifecycle. Goose has recipe-level pre/post but not operation-level hooks. Aider has none. Since Momentum's "file-authoritative enforcement" character comes from hooks, hook parity is the decisive test for full migration.

### Model-routing economics

All four peers route natively through OpenRouter; Claude Code does so only via third-party projects like claude-auto-router or CLAUDE_CODE_SUBAGENT_MODEL env vars. [PRAC — github.com/bijumailbox/claude-auto-router] If Momentum's cost driver becomes "volume of bulk edits on commodity tasks", co-processor mode (any of the four) wins on $/task vs. pure Claude-Code.

### Date caveats

Benchmark claims (Terminal-Bench 2.0) and unified-tooling RFCs are dated 2026-03 through 2026-04 [PRAC, OFFICIAL]. Agent Teams (Claude Code) released 2026-02-05. [OFFICIAL — per subagent-routing search] Most referenced docs are within the 2-year window, with the oldest useful signal being the 2025-09-26 Goose subagent-vs-subrecipe blog post. No source older than 2 years is load-bearing in this analysis.

---

## Recommendation

The lowest-risk, highest-signal next experiment is **OpenCode as a parallel track (pathway b)** — specifically, run one Momentum workflow (candidate: `create-story` or `research`) on OpenCode using the existing `.claude/skills/` directory, and compare outputs. This test:
- Costs <1 week of effort because skills are shared-format;
- Produces a direct comparison between Anthropic-direct Claude Code and OpenRouter-brokered OpenCode on the identical practice;
- De-risks the question of whether Momentum can live off Claude Code without committing to full migration.

**Co-processor quick win (pathway a):** wire ForgeCode or Aider behind a single new skill — `momentum:bulk-refactor` — for scenarios where the work is mechanical, parallelizable, and cost-sensitive. This does not touch Momentum's core practice; it adds a new capability.

**Avoid in 2026-Q2:** full migration to any peer. The TeamCreate gap and hook-lifecycle gap across non-Claude hosts is too costly to paper over right now. Revisit after (i) Block's unified-tooling RFC ships, or (ii) OpenCode grows an inter-agent messaging primitive.

---

## Sources

- ForgeCode GitHub — https://github.com/antinomyhq/forgecode [OFFICIAL]
- ForgeCode creating-agents docs — https://forgecode.dev/docs/creating-agents/ [OFFICIAL]
- ForgeCode operating-agents docs — https://forgecode.dev/docs/operating-agents/ [OFFICIAL]
- ForgeCode pricing blog — https://forgecode.dev/blog/graduating-from-early-access-new-pricing-tiers-available/ [OFFICIAL]
- Hightower, "ForgeCode: The Multi-Agent Coding Harness Dominating Terminal-Bench 2.0", Medium, Apr 2026 — https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4 [PRAC]
- OpenCode docs: Plugins — https://opencode.ai/docs/plugins/ [OFFICIAL]
- OpenCode docs: Agents — https://opencode.ai/docs/agents/ [OFFICIAL]
- OpenCode docs: Skills — https://opencode.ai/docs/skills/ [OFFICIAL]
- OpenCode docs: Rules — https://opencode.ai/docs/rules/ [OFFICIAL]
- OpenCode docs: Config — https://opencode.ai/docs/config/ [OFFICIAL]
- Hightower gist, "Claude Code Agents to OpenCode Agents" — https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0 [PRAC]
- OpenCode vs Claude Code, DataCamp, 2026 — https://www.datacamp.com/blog/opencode-vs-claude-code [PRAC]
- Morph, OpenCode vs Claude Code, 2026 — https://www.morphllm.com/comparisons/opencode-vs-claude-code [PRAC]
- Goose GitHub — https://github.com/block/goose [OFFICIAL]
- Goose docs — https://goose-docs.ai/ [OFFICIAL]
- Goose recipes docs — https://block.github.io/goose/docs/guides/recipes/ [OFFICIAL]
- Goose subagents docs — https://goose-docs.ai/docs/guides/subagents/ [OFFICIAL]
- Block, "How to Choose Between Subagents and Subrecipes" 2025-09-26 — https://block.github.io/goose/blog/2025/09/26/subagents-vs-subrecipes/ [OFFICIAL]
- Unified-tooling RFC — https://github.com/block/goose/discussions/6202 [OFFICIAL]
- Effloow, Goose review 2026 — https://effloow.com/articles/goose-open-source-ai-agent-review-2026 [PRAC]
- PulseMCP, Building Agents with Goose (Part IV) — https://www.pulsemcp.com/building-agents-with-goose/part-4-configure-your-agent-with-goose-recipes [PRAC]
- Claude Code Hooks reference — https://code.claude.com/docs/en/hooks [OFFICIAL]
- Claude Code Subagents docs — https://code.claude.com/docs/en/sub-agents [OFFICIAL]
- Claude Code Skills docs — https://code.claude.com/docs/en/skills [OFFICIAL]
- Claude Code MCP docs — https://code.claude.com/docs/en/mcp [OFFICIAL]
- Anthropic subagents blog — https://claude.com/blog/subagents-in-claude-code [OFFICIAL]
- claude-auto-router (bijumailbox) — https://github.com/bijumailbox/claude-auto-router [PRAC]
- Roo Code + OpenRouter, Medium, Mar 2026 — https://medium.com/@priyan.prabhu/low-cost-coding-agent-in-vs-code-roo-code-openrouter-4b8e92a1bf68 [PRAC]
- Aider vs OpenCode vs Claude Code, sanj.dev — https://sanj.dev/post/comparing-ai-cli-coding-assistants [PRAC]
- Terminal AI Coding Agents Compared 2026, Effloow — https://effloow.com/articles/terminal-ai-coding-agents-compared-claude-code-gemini-cli-2026 [PRAC]
- Morph, "9 Parallel AI Agents That Review My Code" — https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents [PRAC]
- MCP Tool Search announcement (Anthropic, Jan 2026) — referenced in https://code.claude.com/docs/en/mcp [OFFICIAL]
