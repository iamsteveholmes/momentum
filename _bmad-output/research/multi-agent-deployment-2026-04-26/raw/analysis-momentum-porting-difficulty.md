---
content_origin: claude-code-analysis
date: 2026-04-27
sub_question: "What's the actual difficulty of porting Momentum's Claude Code skills/rules/hooks/tools to OpenCode (and the other Tier-1 agents)? What gaps did the original synthesis under-cover?"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
authority: "supplemental analysis identifying gaps in the synthesis (multi-agent-deployment-final-2026-04-26.md). Some claims are inferences from existing verification reports; items flagged [INFERRED] need primary-source verification before refactor commits."
---

# Analysis: The Actual Difficulty of Porting Momentum to OpenCode (and the Other Tier-1 Agents)

The synthesis (§6, §10) concluded that adopting BMAD's verbatim-copy pattern + a Goose Recipe emitter would let Momentum reach ~38 destinations cheaply. The headline finding "OpenCode reads `.claude/skills/` natively" is technically true but **deceptively shallow**. The skill body lands on disk; the skill *instructions* reference Claude-Code-specific primitives that don't port. This document captures what the original research glossed and produces an honest difficulty estimate for a Momentum→OpenCode port (with notes on the other Tier-1 targets where applicable).

This is a corrective analysis, not new primary research. Items marked [VERIFIED] are confirmed against the Wave 2 verification corpus. Items marked [INFERRED] are reasonable analysis from the verified facts and the documented Momentum surface but need a focused verification pass before refactor commits.

---

## 1. What the synthesis covered vs. what it glossed

### Covered (the easy half)

- **File-path discovery.** Verified: OpenCode reads `.claude/skills/`, `.agents/skills/`, `.opencode/skills/`, plus user-config dirs. Discovery order is fixed: `~/.claude/skills/` → `~/.agents/skills/` → project-`.claude/skills/` → project-`.agents/skills/` → `.opencode/{skill,skills}/` → config-driven paths. ([verification-opencode.md][VERIFIED])
- **AGENTS.md handling.** Verified: precedence `AGENTS.md > CLAUDE.md > CONTEXT.md (deprecated)`, with `OPENCODE_DISABLE_CLAUDE_CODE_*` kill switches. First-match wins. ([verification-opencode.md][VERIFIED])
- **Plugin format.** Verified: `@opencode-ai/plugin` TypeScript SDK, `Plugin = (input, options?) => Promise<Hooks>` signature, 16 hook points, 35 bus events, kill-switch env vars. ([verification-opencode.md][VERIFIED])
- **Star count, version, canonical org.** All corrected by verification (anomalyco/opencode canonical, sst→anomalyco 301-redirect, v1.14.28, 150,109 stars). ([verification-opencode.md][VERIFIED])

### Glossed (the hard half)

The remaining sections of this document enumerate ten areas the synthesis treated lightly or not at all. Each is a real port-cost driver that the "drop SKILL.md and you're done" framing obscures.

---

## 2. Ten under-examined gaps

### 2.1 Tool name translation

**The gap.** Claude Code skills routinely invoke `Read`, `Bash`, `Edit`, `Glob`, `Grep`, `Write`, `Task`, `Agent`, `Skill`, `WebSearch`, `WebFetch`, `TodoWrite`, plus MCP-namespaced tools like `mcp__claude-in-chrome__*`. OpenCode's plugin SDK uses different names entirely.

**What we know.** Verification proved that **Gemini CLI** uses entirely different tool names (`read_file`, `run_shell_command`, `replace` (not `edit`!), `grep_search`, `glob`, `web_fetch`, `google_web_search`, `activate_skill`). The corresponding OpenCode tool name table was **never built** by any verification subagent. ([verification-goose-forgecode-gemini.md][VERIFIED for Gemini], [INFERRED for OpenCode])

**Concrete failure mode.** A Momentum skill body that contains `Use the Task tool to spawn a subagent...` silently confuses OpenCode because `Task` is not a tool there. The agent will improvise — possibly by trying a slash command or by giving up. **Skill bodies aren't pure prose; they're prose-with-embedded-tool-references**, and the references break across agents.

**What's needed.** A per-target tool name translation table built by reading each agent's tool registration source. For OpenCode: `packages/opencode/src/tool/*.ts`. For Codex: `codex-rs/protocol/src/tool/*.rs`. For Goose: `crates/goose/src/agents/extension_manager.rs`. **This work has not been done.**

**Port cost.** ~2-4 days per target to build the translation table. The skill bodies then need either (a) a build-time templating layer (`{{ tool.read }}` → `Read` for Claude, `read_file` for Gemini) or (b) per-target skill body variants (5× duplication). Adopting (a) is cheaper but introduces a templating dependency Momentum currently doesn't have.

### 2.2 Sub-agent / Task-tool semantics

**The gap.** Claude Code's `Task` and `Agent` tools spawn isolated sub-agents with parameters: `subagent_type`, `model`, `effort`, `run_in_background`, `isolation: worktree`, `team_name`, `mode: plan`. The synthesis treated this as a Claude-Code-specific feature without examining whether other agents have an equivalent.

**What we know.** OpenCode's plugin SDK exposes `experimental_workspace.register()` ([verification-opencode.md][VERIFIED]) which appears to be a workspace-spawning primitive but **was never characterized in detail**. We don't know:
- Does `register()` create an isolated session with its own tool access?
- Can the parent agent invoke a registered workspace as a tool?
- Does it support `run_in_background` semantics?
- Can the spawned workspace use a different model?

The other Tier-1 agents:
- **Codex CLI**: has the `codex-rs/agents/` crate but its semantics weren't verified for sub-agent spawning. Codex slash commands are a fixed enum (per `verification-codex-cli.md`) — there's no obvious user-spawn primitive.
- **Gemini CLI**: no documented sub-agent primitive in the verification report.
- **Goose**: `sub_recipes` are one level deep (per `verification-goose-recipes-integrations.md`). They're tool-shaped — parent agent invokes them as tools, child runs in isolated session via `run_subagent_task`. **This is the closest non-Claude analog to Task tool, and only Goose has it.**
- **Cline**: 9-event hook system but no documented sub-agent primitive ([verification-sq3-named-targets.md][VERIFIED]).

**Concrete failure mode.** Momentum's Impetus orchestrator pattern is `parent skill → spawn N specialist sub-skills via Task tool, collect their outputs, synthesize`. Without a Task-tool equivalent, this entire pattern doesn't work. The parent skill becomes a single-pass prompt that can't decompose into specialists. **Approximately every Momentum workflow that uses sub-agent fan-out** (sprint-planning, retro, AVFL, research, decision) is hook-anchored on this primitive.

**What's needed.** A focused verification probe: for each Tier-1 agent, identify the sub-agent spawning primitive (if any), document its parameter shape, and verify whether Momentum's Task-tool patterns can be expressed in it. Goose's `sub_recipes` is the most promising target.

**Port cost.** If the Task-tool pattern doesn't translate, Momentum's orchestrator skills need to be **reimplemented per target**, not just copied. The realistic options are:
1. **Sequential prompts** — parent skill becomes a long prompt that does all the work in one pass. Loses parallelism and isolation.
2. **Per-target plugin** — write a TypeScript plugin (OpenCode), Rust hook (Codex), Recipe sub_recipe (Goose) that exposes a "spawn" tool. Per-target effort: 1-2 weeks.
3. **External Momentum CLI** — Momentum becomes its own orchestrator, invoking the underlying agent as a worker. Biggest commitment but most portable. This is what BMAD-METHOD's CLI does for some workflows.

### 2.3 Plan mode

**The gap.** Claude Code's plan mode + `ExitPlanMode` tool is Claude-only. Momentum's `plan-audit` rule (active in this project's `.claude/rules/plan-audit.md`) intercepts `ExitPlanMode` to inject a Spec Impact analysis before plan acceptance.

**What we know.** No other Tier-1 agent has plan mode. Codex, Gemini, OpenCode, Goose, ForgeCode, Cline — none have a documented "plan mode" primitive ([VERIFIED] across all six verification reports — none mention plan mode).

**Concrete failure mode.** The plan-audit gate, the `momentum:plan-audit` skill, and any Momentum behavior that depends on plan-mode semantics simply does not run on non-Claude targets. There is no degradation path; the behavior is absent.

**Port cost.** Either (a) accept that plan-audit is Claude-Code-only and document this as a Tier-1 capability gap on every other target, or (b) reimplement the plan-audit logic as a wrapper that runs after every "design"-shaped skill output, outside the agent's control flow. Option (b) likely requires the external CLI orchestrator from §2.2.

### 2.4 The Skill tool semantics drift

**The gap.** Claude Code has a `Skill` tool with `disable-model-invocation`, `user-invocable: true`, `agent: Explore`, `context: fork` frontmatter fields. These control *how* a skill gets invoked. OpenCode reads SKILL.md files, but **the invocation contract is different**.

**What we know.** The synthesis's §5.3 enumerated 12 Claude-Code-only frontmatter fields silently dropped by other consumers ([verification-agents-md-skills-standards.md][VERIFIED]). What we **didn't** investigate is the behavioral consequence per target:

- For OpenCode: does it model-invoke skills based on frontmatter description match? User-invoke via slash command? Both? **Not verified.** [INFERRED]
- For Codex: skills are at `.codex/skills/` and `.agents/skills/` ([verification-codex-cli.md][VERIFIED]). Invocation contract not documented.
- For Goose: SKILL.md files are loaded as system context but **Goose treats them differently from Recipes** — skills are static behavior, Recipes are invocable workflows.

**Concrete failure mode.** A Momentum skill marked `disable-model-invocation: true` (intended to prevent the model from auto-invoking it during normal conversation) silently behaves as model-invocable on OpenCode, Codex, etc. — they ignore the field. **For skills with side effects** (deploy, send-message, irreversible), this is a security regression, not just a UX nit.

**What's needed.** Per-target verification of how each agent decides to invoke a skill, and explicit per-target classification of which Momentum skills are safe to model-invoke vs. user-invoke-only.

**Port cost.** ~1 week of audit work across the Momentum skill catalog. Plus possible refactor of side-effect-bearing skills to use a confirmation prompt rather than relying on `disable-model-invocation`.

### 2.5 Permission model translation

**The gap.** Three completely different permission abstractions across the Tier-1 targets, and the synthesis didn't address translation.

**What we know.**
- **Claude Code**: `settings.json` `permissions: {allow, deny, ask}` with regex matchers like `Bash(git *)`, `Read(/Users/steve/**)`, `mcp__claude-in-chrome__*`. ([CITED — docs.claude.com])
- **OpenCode**: TypeScript plugin defines a `permission.ask` event handler that runs in-process. Permission decisions are programmatic, not declarative. ([verification-opencode.md][VERIFIED])
- **Codex CLI**: TOML `[sandbox]` modes — `read-only`, `workspace-write`, `danger-full-access`. Coarse-grained, no per-tool patterns. ([verification-codex-cli.md][VERIFIED])
- **Goose**: no formal permission model documented. Per `verification-goose-forgecode-gemini.md`, MCP tools have a per-extension allow/deny but the schema is implicit.
- **Gemini CLI**: documented as part of `settings.json`, no detailed verification.
- **ForgeCode**: `permissions.yaml` with `policies × {allow|confirm|deny} × {read|write|command|url}` and `all`/`any`/`not` operators. ([verification-goose-forgecode-gemini.md][VERIFIED])

**Concrete failure mode.** Momentum's permission rules (e.g., the `fewer-permission-prompts` skill that adds `Bash(git status)` to allowlist) are **regex-shaped declarative rules** in `settings.json`. They can't be auto-translated to OpenCode's TypeScript event handler or Codex's coarse sandbox modes. A user installing Momentum on OpenCode either (a) gets no permission rules and is prompted for everything, or (b) requires a hand-written TypeScript plugin per Momentum permission rule.

**What's needed.** Per-target permission emit logic. For OpenCode: a TypeScript plugin generator that converts Claude regex patterns to permission.ask handler logic. For Codex: a settings.toml emitter that picks the closest sandbox mode and warns the user about loss of granularity. For ForgeCode: a permissions.yaml emitter.

**Port cost.** Building all three emitters is ~2-3 weeks. Or accept that permission rules are Claude-Code-only and ship a per-target manual-setup doc.

### 2.6 Hook payload/decision shape (the deep gap)

**The gap.** The synthesis said "Codex mirrors Claude Code's JSON shape" — true at the surface — but the actual blocking semantics differ subtly across agents that have hooks.

**What we know.**
- **Claude Code**: exit code 2 OR JSON `{"hookSpecificOutput": {"permissionDecision": "deny"}}`. Decision values: `allow|deny|ask|defer` (with `defer` added at v2.1.89). ([verification-claude-hooks.md][VERIFIED])
- **Codex CLI**: same JSON shape but **different valid decision values** — Codex shipped `defer` earlier than Claude per verification. ([verification-codex-cli.md][VERIFIED])
- **OpenCode**: hook errors thrown as TypeScript exceptions. No JSON wire shape. ([verification-opencode.md][VERIFIED])
- **Cline**: 9 events with their own schema. ([verification-sq3-named-targets.md][VERIFIED])
- **Gemini CLI**: 11 events with `Before/After` naming, `AfterModel` fires per chunk (unique). ([verification-goose-forgecode-gemini.md][VERIFIED])

**Concrete failure mode.** A Momentum hook config written for Claude Code's `permissionDecision: "deny"` can be mostly-translated to Codex but requires per-target rewriting beyond just renaming events. The translation isn't 1:1 because the *semantics of decision values* differ slightly.

**Port cost.** Per-target hook emit logic. For each of Codex/Cline/Gemini/OpenCode: 1-2 weeks per target to build and validate the translation. Plus the per-Momentum-hook decision tree: which translates cleanly, which loses fidelity, which is unportable.

### 2.7 Memory architecture

**The gap.** Three completely different memory paradigms, and Momentum's `auto-memory` rules are anchored on Claude Code's specific filesystem layout.

**What we know.**
- **Claude Code**: auto-memory at `~/.claude/projects/<project-slug>/memory/` (filesystem, per-project, model-curated, with MEMORY.md as the index). ([CITED — `~/.claude/rules/auto-memory`])
- **OpenCode**: persistent session threads (database-backed, viewable in TUI). ([INFERRED from verification-opencode.md plugin events including session.created])
- **Goose**: in-process session memory + `.goosehints` for cross-session context. ([verification-goose-forgecode-gemini.md][VERIFIED])
- **Codex**: session-scoped, no persistent memory documented.
- **Gemini, Cline**: not investigated.

**Concrete failure mode.** Momentum's auto-memory rules generate filesystem-anchored memory. The `MEMORY.md` index references typed memory files (user_*, feedback_*, project_*, reference_*). **Other agents don't read this layout.** A user who builds up memory in Claude Code and switches to OpenCode loses access to the entire memory store.

**What's needed.** A bridge layer that exports Claude Code's filesystem memory to a format the target agent consumes. For OpenCode: would need to inject memory content into AGENTS.md or a session-startup plugin hook. For Goose: into `.goosehints`. For Codex: into `AGENTS.md` (Codex reads it concatenated).

**Port cost.** ~2-3 weeks for a multi-target memory bridge, plus ongoing maintenance as each agent evolves its memory model.

### 2.8 Update mechanism end-to-end

**The gap.** Four entirely different update UX paths, never compared in the synthesis.

**What we know.**
- **Claude Code**: `/plugin marketplace update momentum` updates a git-cloned plugin marketplace. Per-user plugin install. ([CITED — Claude Code docs])
- **OpenCode**: `bun install` of npm package. Per-project install. ([verification-opencode.md][VERIFIED])
- **Codex CLI**: `git pull` of a repo's `.codex/` directory, or `cargo install`. No formal plugin distribution. ([verification-codex-cli.md][VERIFIED])
- **Goose**: fork-with-bundle "Custom Distros" (a Goose fork pre-loaded with recipes). No formal marketplace. ([verification-goose-recipes-integrations.md][VERIFIED])

**Concrete failure mode.** A user who installs Momentum across four agents has four different upgrade workflows to remember. There is no `momentum upgrade` that works against all of them.

**What's needed.** Either (a) accept per-target update flows and document them, or (b) build a Momentum CLI that abstracts the update step (`momentum upgrade --target=opencode` runs `bun install`, `--target=claude-code` runs the marketplace update, etc.).

**Port cost.** A unified Momentum CLI is ~2-3 weeks of work. Per-target docs alone are ~1 week.

### 2.9 Auth and credential propagation

**The gap.** Each agent has its own auth model. Momentum installs run as the user, not as a single-credential entity.

**What we know.**
- **Claude Code**: Anthropic API key OR login session. Stored in `~/.claude/`.
- **OpenCode**: Own auth model with `OPENCODE_DISABLE_CLAUDE_CODE_*` kill switches that explicitly *ignore* Claude Code's auth state. ([verification-opencode.md][VERIFIED])
- **Codex CLI**: OpenAI API key. Stored in `~/.codex/`.
- **Gemini CLI**: Google auth. Stored in `~/.gemini/` or via `gcloud auth`.
- **Goose, ForgeCode**: per-provider config.

**Concrete failure mode.** When Momentum's installer runs against a user with multiple agents installed, **does the user re-auth for each, or does the installer share auth?** The default answer is "no — the user re-auths per agent" which is a UX cost the synthesis didn't acknowledge.

**Port cost.** Probably accept the re-auth tax. Building unified auth is a much bigger commitment than Momentum should take on.

### 2.10 Output styles, status lines, progress indicators

**The gap.** Pure UI primitives don't port. Momentum's Impetus opens with ASCII art + nerdfont icons (per the user feedback memory `feedback_impetus_first_impression.md`); status-line + output-style are Claude-Code-only primitives.

**What we know.**
- **Claude Code**: `output-styles/`, `status-line` are first-class settings. Render in Claude's terminal UI.
- **OpenCode**: own TUI primitives. ([INFERRED — not verified])
- **Codex, Gemini, Goose, ForgeCode**: each has its own UI; none consume Claude's output-style/status-line files.

**Concrete failure mode.** Impetus' ASCII art + nerdfont icons may render correctly on OpenCode's TUI (both run in terminal) but **definitely don't honor status-line or output-style configs**. The user gets a visually different experience per agent.

**Port cost.** Either (a) accept per-target visual divergence and write to the lowest-common-denominator (plain Markdown headers, no ASCII art), or (b) per-target UI shimming. Honestly, option (a) is correct — Momentum's UI flair is nice-to-have, not load-bearing.

---

## 3. The honest difficulty estimate

Breaking Momentum's surface down by porting difficulty to OpenCode (the easiest non-Claude target):

| Momentum component | % of Momentum | Port difficulty | Why |
|---|---|---|---|
| Skill bodies that are pure instructional Markdown (no tool calls, no Task spawns, no plan mode) | ~10% | **Trivial** — true zero-translation | OpenCode reads `.claude/skills/` natively |
| Skill bodies referencing Claude tool names (`Read`, `Bash`, `Edit`, `Task`, `Skill`) | ~70% | **Medium** — requires translation layer | Tool name table per target + skill-body templating, OR per-target skill variants |
| Hooks (commit-checkpoint, plan-audit, scheduled-tasks-lock, auto-memory triggers) | ~20% | **Hard** — per-target reimplementation or drop | Each target has its own hook system shape; Goose/ForgeCode have none |
| CLI orchestrator behaviors (Impetus, sprint-planning, retro spawning sub-agents) | overlaps with hooks/tools | **Hard** — Task tool has no clean equivalent | Either reimplement per-target plugin OR external Momentum CLI |
| Permission rules (`Bash(git *)` allowlist, etc.) | small but security-critical | **Hard** — per-target emitter, semantics differ | Three different abstractions, no clean translation |
| Auto-memory architecture | small but UX-critical | **Medium** — requires bridge layer | Each agent has different memory model |
| UI flair (output-styles, status-line, ASCII art) | small | **Drop or accept divergence** | Lowest-common-denominator emit |

**Total realistic effort for a thorough Momentum→OpenCode port: 6-10 engineer-weeks** (not counting verification work).

**Per-additional-target tail: 1-3 weeks** depending on how many Tier-1 capabilities the target supports natively. Codex is closest (Claude-shaped hooks, similar AGENTS.md). Goose requires Recipe-emitter work (per §10 of synthesis). ForgeCode is highest-tail (no hooks, no marketplace, bespoke skill model).

**Total realistic effort to reach all 6 in-scope Tier-1 targets thoroughly: 12-25 engineer-weeks.**

The synthesis's "drop SKILL.md and you're done" framing accounts for **maybe 1 week of that**. The other 11-24 weeks are the per-target tail the synthesis under-quantified.

---

## 4. The actually-honest porting plan

A Momentum→multi-agent port is meaningfully bigger than "copy the SKILL.md tree." Realistic phases:

### Phase A — Skill body sweep (1-2 weeks)

Audit every Momentum skill body (`skills/momentum/skills/*/SKILL.md` and child workflow.md files) for:
- Claude-Code-specific tool names (`Task`, `Skill`, `Agent`, `TodoWrite`, MCP tool names)
- Plan mode references (`ExitPlanMode`)
- Frontmatter fields outside the open Agent Skills spec
- Side-effect-bearing operations (file writes, git commits, network calls)

Tag each skill as: **Tier 1 portable** / **Tier 2 needs-rewrite** / **Tier 3 unportable**. Output: a `momentum-skill-portability-audit.md` document.

### Phase B — Tool translation layer (2-4 weeks)

For each non-Claude target, build a **per-target tool name map** by reading the target's source code:

```
{
  "claude-code": { "read": "Read", "bash": "Bash", "edit": "Edit", "task": "Task", "skill": "Skill" },
  "opencode": { "read": "<verified-name>", "bash": "<verified-name>", ... },
  "codex": { "read": "<verified-name>", ... },
  "gemini": { "read": "read_file", "bash": "run_shell_command", "edit": "replace", "search": "google_web_search" },
  "goose": { "read": "<verified-name>", ... }
}
```

Then add a build step that templates skill bodies per target. Output: `tools/translate-skill.js` or similar.

### Phase C — Sub-agent fallback decision (uncertain — 2-6 weeks)

For skills that spawn Task agents, decide:

1. **Reimplement as OpenCode plugin tools** — write TypeScript that exposes `momentum-spawn-subagent` as a tool the OpenCode agent invokes. Per-target effort.
2. **Replace with sequential prompts** — parent skill becomes a long prompt that does all the work in one pass. Loses parallelism.
3. **External Momentum CLI** — Momentum becomes its own orchestrator; the underlying agent is a worker invoked via its own protocol (e.g., spawning `claude` or `opencode` subprocesses with carefully crafted prompts). Biggest commitment but most portable.

The right answer depends on how core sub-agent fan-out is to Momentum's identity. If it's the differentiator, option (3) becomes the architecture, not a port detail.

### Phase D — Hook fallback per target (1-2 weeks per Momentum hook × per target)

For each Momentum hook (commit-checkpoint, plan-audit, scheduled-tasks-lock, auto-memory triggers, etc.), produce a per-target translation matrix:

| Momentum hook | Claude Code | OpenCode | Codex | Cline | Gemini | Goose | ForgeCode |
|---|---|---|---|---|---|---|---|
| commit-checkpoint (PostToolUse on Edit/Write/Bash) | native | native (tool.execute.after) | native (PostToolUse) | native | native (AfterTool) | drop or pre-commit | drop |
| plan-audit (intercept ExitPlanMode) | native | drop | drop | drop | drop | drop | drop |
| scheduled-tasks-lock | filesystem-based, agent-agnostic | works | works | works | works | works | works |
| auto-memory triggers | UserPromptSubmit + SessionStart | drop | partial (SessionStart) | partial | partial | drop | drop |

The "drop" cells become Tier-1 capability gaps to document.

### Phase E — Update / auth / permission per target (1 week each)

The unglamorous integration work:
- Update flow: build target-specific upgrade commands.
- Auth: accept per-target re-auth tax, document it.
- Permissions: build per-target emitter for the high-value rules; drop the rest.

### Phase F — Validation pass (1-2 weeks)

For each target, install Momentum end-to-end and run the canonical workflows (`momentum:create-story`, `momentum:dev`, `momentum:retro`). Document what works, what degrades, what fails. This is Phase 7 of the AVFL pattern applied to the deployed product.

**Total honest effort: 12-25 engineer-weeks for thorough multi-target coverage.** A "Tier 1 only" cut (Claude Code + OpenCode + Codex) is closer to 6-10 engineer-weeks. A "skills only, no orchestrator" cut is the BMAD-pattern from §6 of the synthesis: 2-3 weeks.

---

## 5. Recommendations

### 5.1 What to do before any refactor commits

**Before** committing to multi-agent shape, run a focused verification probe answering these primary-source questions:

1. **OpenCode tool name table** — read `packages/opencode/src/tool/*.ts` and produce the canonical name map.
2. **OpenCode sub-agent primitive** — characterize `experimental_workspace.register()`. Can it spawn isolated agents?
3. **Codex skill invocation contract** — when does Codex auto-fire a SKILL.md vs. require user invocation?
4. **Goose Recipe sub_recipe parameter passing** — exact wire shape, parameter name resolution rules.
5. **The Momentum skill catalog audit** (Phase A above).

These five probes determine whether multi-agent Momentum is a 2-3 week BMAD-style verbatim-copy refactor (skill bodies are mostly portable, hooks accepted as Claude-Code-only), or a 12-25 week deep porting project (skill bodies need translation, sub-agent pattern needs reimplementation).

### 5.2 The architectural fork the synthesis didn't fully present

The "BMAD-pattern dual-emitter" recommendation from synthesis §10.5 is correct **for the skill-body emission layer**. It is silent on the orchestrator question.

There are really two Momentum architectures the user can pick between:

**Option 1: Momentum-as-skill-pack.** Momentum is a SKILL.md tree distributed to N agents via BMAD-pattern verbatim copy + Goose Recipe emitter. Sub-agent orchestration works on Claude Code natively; degrades to "agent reads skill, decides what to do next" on other targets. Practice rules and hooks are best-effort per target. **2-6 engineer-weeks. Reaches ~38 destinations.**

**Option 2: Momentum-as-orchestrator-CLI.** Momentum is its own CLI tool that drives any underlying agent (Claude Code, OpenCode, Codex) as a worker. Skills, workflows, hooks, sub-agent fan-out, plan-audit gates, auto-memory — all enforced by the Momentum CLI, with the underlying agent doing the LLM work. **6-12 engineer-weeks. Reaches all targets uniformly. Highest leverage, highest commitment.**

The synthesis recommended Option 1 implicitly. Option 2 is the architecture BMAD's CLI represents — and is what allows BMAD to scale to 42 platforms with consistent behavior. **Option 2 should be considered seriously before committing to Option 1.**

### 5.3 Documentation gap

The synthesis (§6) jumped from "extension contract per agent" to "concrete refactor sketch" without an intermediate "what doesn't translate" inventory. This document is that inventory. It should be:
- Linked from §6 of the synthesis as a port-difficulty addendum
- Used as input to the Phase A skill-catalog audit
- Updated as new verification probes resolve the [INFERRED] items

### 5.4 The "what we couldn't tell you" list

For honesty, here's what this analysis does NOT settle and would need a focused probe to answer:

1. **OpenCode `experimental_workspace.register()` semantics** — sub-agent fan-out feasibility hinges on this.
2. **Codex `.codex/skills/` invocation rules** — auto-invoke vs. user-invoke decision tree.
3. **Whether Goose's `sub_recipes` can be authored to match Momentum's parallel-fan-out pattern** — only one level deep, sequential-when-repeated flag is a strong constraint.
4. **Cline's hook payload shape** — 9 events documented but exact JSON not yet quoted.
5. **OpenCode permission.ask handler patterns** — concrete examples in the wild (not just SDK docs).
6. **Whether AGENTS.md v1.1 (issue #135) ships with frontmatter** — would simplify the Memorymd→AGENTS.md bridge.

Each of these is 1-3 days of focused primary-source verification. Recommend running them before Phase A of any port.

---

## Appendix: relationship to existing research artifacts

This analysis is supplemental to the synthesis at `final/multi-agent-deployment-final-2026-04-26.md`. It builds on:

- `verification-opencode.md` — primary OpenCode verification (file paths, plugin SDK, hook events)
- `verification-claude-hooks.md` — Claude Code hook contract (28 events at v2.1.119)
- `verification-codex-cli.md` — Codex CLI extension contract (6 hooks, sandbox modes)
- `verification-goose-forgecode-gemini.md` — Goose/ForgeCode/Gemini contracts
- `verification-agents-md-skills-standards.md` — open spec governance + 12 Claude-Code-only fields
- `verification-sq3-named-targets.md` — Aider/Continue/Cody/Roo/Cline architecture
- `verification-bmad-deep.md` — BMAD v6.5.0 architecture
- `verification-bmad-extra-platforms.md` — Tier-1 capabilities Momentum's targets lack
- `verification-goose-recipes-integrations.md` — Goose Recipes deep-dive

The [INFERRED] items in this analysis represent the gap between "what verification covered" and "what a refactor needs to know." Closing that gap is the next research step before any port begins.

---

*Authored 2026-04-27 by claude-code-analysis as a corrective addendum to the multi-agent-deployment synthesis. Identifies 10 under-examined porting concerns and provides an honest 12-25 engineer-week effort estimate for thorough multi-target Momentum coverage. Some claims marked [INFERRED] need primary-source verification before refactor commits.*
