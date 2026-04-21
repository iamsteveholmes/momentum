---
content_origin: claude-code-subagent
date: 2026-04-21
sub_question: "Which of these tools support Momentum's core primitives — file-authoritative rules, skills/agents as first-class citizens, hooks, and deterministic workflows — well enough that a Momentum-equivalent practice could live on them, and which would require heavy glue?"
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

# Momentum Practice Surface — Can Other Tools Host Momentum?

## Scope and framing

Momentum is a practice layer composed of four primitives layered on Claude Code: (1) file-authoritative rules auto-loaded from `.claude/rules/*.md` and nested `CLAUDE.md`, (2) skills as first-class SKILL.md + workflow.md directories invoked by the Skill tool, (3) shell-command hooks wired into lifecycle events in `settings.json`, and (4) deterministic workflows with numbered steps, `<check>` conditionals, `<action>` directives, `<critical>` invariants, and a workflow-fidelity rule that treats each step as binding. A fifth supporting primitive is the spawnable subagent — markdown files with frontmatter that become independent work contexts via the Agent tool.

This research evaluates whether nine other agentic coding tools — ForgeCode, Goose AI, OpenCode/sst, Qwen Code, Kilo Code, Aider, Cline, Roo Code, Continue.dev, plus Codex CLI — could host a Momentum-equivalent practice, and where the structural gaps live.

## Classification summary

The table below classifies each tool against each primitive. `Native` means first-class, idiomatic support. `Glue` means achievable but requires custom config, shell wrappers, or convention. `Missing` means no equivalent exists today.

| Tool | File-authoritative rules | Skills/agents first-class | Hooks | Deterministic workflows |
|---|---|---|---|---|
| **Claude Code (baseline)** | Native | Native | Native | Native (via skill workflow.md) |
| **Qwen Code** | Native (AGENTS.md) | Native (SKILL.md + subagents) | Native (13 events) | Glue (skills carry workflows, no DSL) |
| **OpenCode (sst)** | Native (AGENTS.md + CLAUDE.md) | Native (SKILL.md + agents) | Native (~25 plugin events, TS/JS) | Glue (skills + agent prompts) |
| **Codex CLI** | Native (AGENTS.md chain) | Glue (slash commands + subagents, skills via SKILL.md community) | Native (experimental: 5+ events) | Glue |
| **Kilo Code** | Native (nested AGENTS.md) | Glue (agents/modes, custom modes) | Missing | Glue (workflows feature nascent) |
| **Cline** | Native (.clinerules/, AGENTS.md) | Glue (workflows as slash commands, no subagents in the spawn sense) | Native (6 events, v3.36+) | Glue (workflow markdown files) |
| **Roo Code** | Native (AGENTS.md + .roo/rules) | Glue (custom modes per-task, no spawn API) | Missing (GitHub issues open) | Glue (mode orchestration via boomerang) |
| **Goose AI** | Glue (AGENTS.md supported in repo; no nested loading documented) | Glue (recipes = workflow+skill hybrid, subrecipes exist) | Missing (no lifecycle hook API; MCP only) | Native (recipes YAML w/ Jinja + subrecipes) |
| **ForgeCode** | Native (AGENTS.md, layered load) | Glue (custom agents + custom commands, no SKILL.md) | Missing | Glue (agent prompts + custom commands) |
| **Continue.dev** | Glue (.continue/rules, no AGENTS.md yet) | Missing (agents = profiles, not spawnable skills) | Missing | Missing |
| **Aider** | Glue (CONVENTIONS.md, manual load) | Missing | Missing (git hooks only) | Missing |

Two clusters emerge: a "high-fidelity Momentum host" cluster (Qwen Code, OpenCode, Codex CLI) where all four primitives are native or near-native, and a "partial host" cluster (Kilo, Cline, Roo, Goose, ForgeCode) where at least two primitives are missing or heavily glue-dependent. Aider and Continue.dev sit below the practice threshold.

## Per-tool analysis

### Qwen Code — highest fidelity clone [PRAC]

Qwen Code is effectively a Claude Code fork at the primitive level. AGENTS.md loads as a system prompt injection [OFFICIAL: qwen-code/AGENTS.md]. Subagents are first-class: markdown files with YAML frontmatter, spawnable, with their own prompts, tools, and models [OFFICIAL: qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/]. Skills follow the SKILL.md convention exactly — required `name` and `description` frontmatter, discoverable from `~/.qwen/skills/`, `.qwen/skills/`, and extensions, model-invoked by description match, or user-invoked via `/skills <name>` [OFFICIAL: qwenlm.github.io/qwen-code-docs/en/users/features/skills/].

Hooks are the most striking parity point. Qwen Code supports 13 lifecycle events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PostCompact`, `Notification` [OFFICIAL: QwenLM/qwen-code docs/users/features/hooks.md]. Handler types include command (shell), HTTP, and internal function. Configuration lives in `.qwen/settings.json` with matcher regex, sequential flag, timeout — nearly identical schema to Claude Code's hook config.

The one true gap is deterministic workflow DSL. Qwen has no equivalent of Claude's `<check>`/`<action>`/`<critical>` step tags or a workflow-fidelity rule. Skills carry workflow text, and the model is instructed to follow steps, but there is no explicit step DSL or fidelity enforcement.

**Momentum portability verdict:** Migrating Momentum to Qwen Code would require ~0 primitive-level glue. Rules, skills, subagents, and hooks all port directly. Workflows port as markdown text inside SKILL.md — you lose the `<check>`/`<action>` structure as first-class syntax but retain the content. The workflow-fidelity rule could be ported as a user-level AGENTS.md rule directing the model to treat numbered steps as binding.

### OpenCode (sst) — closest competitor by plugin surface [PRAC]

OpenCode loads AGENTS.md with a well-documented cascade: local traversal up from cwd, then `~/.config/opencode/AGENTS.md` global, then falls back to `~/.claude/CLAUDE.md` for Claude Code compatibility [OFFICIAL: opencode.ai/docs/rules/]. The "first matching file wins in each category" rule is flat rather than nested — you cannot stack nested CLAUDE.md files the way Claude Code does, though OpenCode's `opencode.json` has an `instructions` field that accepts glob patterns (`packages/*/AGENTS.md`) to simulate monorepo context.

Agents are markdown + frontmatter files in `.opencode/agents/` or `~/.config/opencode/agents/`, with a primary/subagent split. Primary agents auto-invoke subagents based on descriptions, or users trigger via `@` mentions [OFFICIAL: opencode.ai/docs/agents/]. Skills are separately modeled from agents: SKILL.md files in `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/`, discovered via a native `skill` tool, with a frontmatter schema nearly identical to Anthropic's (`name`, `description`, plus optional `license`, `compatibility`, `metadata`) [OFFICIAL: opencode.ai/docs/skills/]. The explicit reading of both `.opencode/` and `.claude/` paths means Anthropic skills are drop-in.

The hook system is actually broader than Claude Code. Plugins are TypeScript/JavaScript modules (not shell scripts) that export functions returning a hooks object. Documented events span ~25 types organized by category: `session.*` (created, compacted, idle, error), `tool.execute.before` / `tool.execute.after`, `file.edited`, `permission.asked`, `message.part.updated`, `tui.prompt.append`, `shell.env`, plus experimental `session.compacting` [OFFICIAL: opencode.ai/docs/plugins/]. The TS/JS contract gives far richer in-process control than Claude's shell-out model, at the cost of requiring a Node runtime.

Deterministic workflows are not natively supported as a DSL. Workflows are expressed as agent prompts or skill instructions — free-form markdown. No `<check>`/`<action>` parser.

**Portability:** High. Rules port directly. Skills port directly (OpenCode reads `.claude/skills/` paths). Hooks port with a rewrite from shell to TS — every Momentum shell hook must become a TS plugin function. Workflows port as skill content.

### Codex CLI — strong chain-loading rules, decent hooks, weakest skill story [PRAC]

Codex CLI's AGENTS.md chain is powerful: it builds an instruction chain at session start, reading `~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md` at the home level, then layers project-specific AGENTS.md [OFFICIAL: developers.openai.com/codex/guides/agents-md]. The layered precedence is explicit and well-documented.

Hooks are experimental and must be enabled via a feature flag (`codex_hooks = true`), configured in `hooks.json` at `~/.codex/` or `.codex/`. Documented events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` [PRAC: openai/codex GitHub issues, community release trackers]. Community hook runners (`hatayama/codex-hooks`) explicitly reuse Claude Code hooks settings, indicating schema proximity. Caveats: as of GitHub issue #16732, hooks only fire reliably for the Bash tool, not the ApplyPatchHandler — a PostToolUse code-quality gate on file edits is not yet production-safe.

Skills and subagents exist but are less mature. Codex ships 40+ built-in slash commands but the public docs do not formally cover custom slash command authoring; the catalog of built-ins is deeper than OpenCode's. Subagent support is referenced via `/agent` and the community SKILL.md convention has been adopted broadly — per the 2026 agent-skills.io specification, Codex is listed as one of 11+ SKILL.md-compatible tools [UNVERIFIED: rywalker.com/research/agentic-skills-frameworks].

Deterministic workflows: no native DSL; would be expressed as skill instructions.

**Portability:** Medium-high. Rules port well (AGENTS.md chain is more powerful than Claude's CLAUDE.md nesting in some respects). Hooks port with caveats on tool coverage. Skills port as SKILL.md. Workflows are free-form.

### Kilo Code — nested AGENTS.md, no hooks [OFFICIAL]

Kilo Code has an unusually strong rules story: nested AGENTS.md files are explicitly supported, with subdirectory files taking precedence over root for conflicting instructions — this is the closest match to Claude Code's nested CLAUDE.md behavior documented in any competitor [OFFICIAL: kilo.ai/docs/customize/agents-md]. Rules load in priority order: agent-specific prompts → project `kilo.jsonc` → AGENTS.md → global `kilo.jsonc` → skills.

Modes (renamed to Agents in April 2026) are customizable behavioral profiles defined as markdown + YAML frontmatter with configurable tool permissions (read, edit, bash, glob, grep, etc.) [OFFICIAL: kilo.ai/docs/customize/custom-modes]. This is closer to Roo's mode system than Claude's spawnable subagents — modes switch the current agent's behavior rather than spawning a new context.

Hooks: not documented. Workflows: referenced as a new feature but without implementation details as of April 2026.

**Portability:** Medium. Rules port directly (best-in-class nested loading). Skills need adaptation (modes are not skills). Hooks are missing entirely — every hook-driven automation in Momentum would need to become an external process (git hook, file watcher) or be abandoned.

### Cline — only competitor with a Claude-parity hook system [OFFICIAL]

Cline v3.36 ships six lifecycle hooks: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `TaskStart`, `TaskResume`, `TaskCancel` [OFFICIAL: cline.bot/blog/cline-v3-36-hooks]. Hooks live in `~/Documents/Cline/Rules/Hooks/` or `.clinerules/hooks/`, receive JSON via stdin, and return JSON with `cancel` and `contextModification` fields. Platform support is macOS/Linux only — Windows developers are blocked. The context-modification payload is interesting: unlike Claude's hook output which is largely additive to transcript/stdout, Cline's `contextModification` explicitly injects text into the next API request.

Rules live in `.clinerules/` at project root, with YAML frontmatter supporting `paths` (glob array) for conditional activation [OFFICIAL: docs.cline.bot/customization/cline-rules]. Workflows are a separate concept: markdown files in `.clinerules/workflows/` invoked via `/workflow-name.md`, wrapped in `explicit_instructions` tags. This is a clean separation Momentum lacks — Cline explicitly distinguishes always-on rules (token-expensive) from on-demand workflows (token-cheap). [TRANSFERABLE]

Subagents: Cline does not spawn independent subagent contexts in the Claude Code sense. Multi-agent work is done via task orchestration within a single Cline task tree.

**Portability:** Medium-high for rules/hooks, low for subagents. Workflows could port as Cline workflow files, but Momentum's pattern of skills spawning subagent teams (e.g., retro auditor team, AVFL lens agents) has no direct equivalent.

### Roo Code — modes over subagents [OFFICIAL]

Roo Code supports the AGENTS.md standard [OFFICIAL: RooCodeInc/Roo-Code issue #5966] and also loads `.roo/rules-{modeSlug}/` directories recursively for mode-scoped instructions [OFFICIAL: docs.roocode.com/features/custom-instructions]. The per-mode rule scoping is a nice variant of path-scoped loading.

Custom modes define role definitions, tool permissions, and custom instructions per mode. Mode switching (boomerang mode, hierarchical teams) is the Roo equivalent of agent spawn, but it lacks the "independent context" semantics of Claude subagents — modes share the top-level conversation state.

Hooks: no native system. Open issues (#11504, #12025) request prompt-based and event-based hook commands. Momentum's auto-commit reminder and auto-rename hooks would need to be implemented as external daemons or shell wrappers.

**Portability:** Low-medium. Rules port. Modes replace subagents but with semantic drift. Hooks are missing. Workflows are free-form.

### Goose AI — workflow-native but hook-poor [OFFICIAL]

Goose is the one tool where deterministic workflows are arguably more powerful than Claude Code's. Recipes are YAML files with fields: `version`, `title`, `description`, `instructions`, `prompt`, `extensions`, `activities`, `settings`, `parameters`, `response`, `retry`, and `sub_recipes` [OFFICIAL: block.github.io/goose/docs/guides/recipes/recipe-reference/]. Instructions support Jinja2 templating for conditional logic. Sub-recipes accept mapped parameters from the parent — this is a native deterministic workflow composition model [PRAC: dev.to/nickytonline/advent-of-ai-day-15-goose-sub-recipes].

A Momentum sprint-planning workflow with parallel sub-skills (create-story per-story, spawn via fan-out) maps cleanly onto Goose recipes with sub_recipes — cleaner than Claude Code's "skill invokes Agent tool" pattern.

However, Goose has weaker rule and hook stories. AGENTS.md is supported but no nested loading is documented, so Momentum's per-directory `.claude/rules/` pattern needs flattening. There is no lifecycle hook API — extensibility is entirely MCP-based. MCP gives you tool capabilities but not event hooks on the agent loop. Auto-commit reminders, stop hooks, user-prompt-submit injection — none have equivalents.

Subagents are supported [PRAC: gist/mootrichard] but through recipes-as-subagents rather than a separate Agent tool.

**Portability:** Workflows port extremely well (often with improvements). Rules port as flat AGENTS.md. Hooks are missing. Skills-as-skills need rewriting as recipes.

### ForgeCode — custom agents + AGENTS.md, no hooks, no skills [OFFICIAL]

ForgeCode loads AGENTS.md from three locations in priority: `~/forge` base path, git root, cwd [OFFICIAL: forgecode.dev/docs/custom-rules/]. Custom agents live in `.forge/agents/` or `~/forge/agents/` as `.md` files with YAML frontmatter (id, title, description, model, tools, custom_rules, max_turns, reasoning) [OFFICIAL: forgecode.dev/docs/agent-definition-guide/]. Custom commands (`.forge/commands/`) provide shortcuts via `:commandname` syntax and can also be inlined in `forge.yaml`. Tool filtering supports glob patterns like `mcp_*`.

Agents use Handlebars templates for dynamic prompt content — similar in spirit to Jinja but less commonly associated with deterministic workflows. No SKILL.md convention. No documented hook API. No explicit workflow DSL.

**Portability:** Low-medium. Rules port. Subagents via custom agents port with rewrites. Skills don't exist as a first-class concept. Hooks are missing.

### Continue.dev — rules-only [OFFICIAL]

Continue has `.continue/rules/` with rich frontmatter (`name`, `globs`, `regex`, `description`, `alwaysApply`) and path-scoped activation via globs [OFFICIAL: docs.continue.dev/customize/deep-dives/rules]. This rule schema is arguably more sophisticated than Claude Code's. AGENTS.md support is an open GitHub issue (#6716) — not yet native.

Agents in Continue are bundled profiles (model + rules + tools), not spawnable subagent contexts. There is no SKILL.md system, no lifecycle hooks, no workflow DSL. Custom slash commands exist for prompt templates but without step semantics.

**Portability:** Low. Only rules port cleanly, and even those need frontmatter rewrites.

### Aider — conventions-based, not a practice host [OFFICIAL]

Aider treats conventions as read-only files loaded via `/read CONVENTIONS.md` or `.aider.conf.yml` `read:` list [OFFICIAL: aider.chat/docs/usage/conventions.html]. No auto-load, no nested loading, no frontmatter, no skills, no subagents, no hooks (beyond git hooks which are outside Aider itself), no workflow DSL. Aider is a pair-programming chat tool, not a practice surface. It would require wholesale re-architecture to host Momentum.

## Transferable primitives worth importing to Momentum

Several competitors have features that Claude Code lacks and that Momentum could borrow.

**Cline's workflow/rule split.** Cline's explicit distinction between always-on rules (persistent system context, token cost on every message) and on-demand workflows (invoked by slash command, token cost only when triggered) is a clean design [OFFICIAL: cline.ghost.io/stop-adding-rules-when-you-need-workflows/]. Momentum currently loads all rules via CLAUDE.md injection whether they apply or not. A lazy-load pattern — mark rules as `trigger: on-demand` and surface them via a skill or slash command — would reduce context bloat for rules like avfl-post-merge-strategy that only matter during retro.

**Goose recipe sub_recipes with mapped parameters.** Goose's `sub_recipes: [{name, path, values: {param: {{parent_param}}}}]` is a cleaner workflow composition primitive than "skill spawns subagent via Agent tool and prompt-templates inputs." A recipe-like DSL would let Momentum workflows declare their composition graph explicitly, enabling static analysis (dependency checks, orphan detection) that is currently done by convention.

**OpenCode's rich plugin event surface.** OpenCode's ~25 documented plugin events (including `session.compacted`, `file.watcher.updated`, `permission.asked`, `message.part.updated`) offer hooks into states that Claude Code does not expose. Notably, `session.compacted` with an `experimental.session.compacting` hook that fires before summarization and can inject domain context would let Momentum preserve sprint state across compaction reliably.

**Continue's rule regex matching.** Continue rules can activate on file content regex, not just glob path — this enables "when a file imports `openai`, load the openai-migration rule" patterns that Momentum currently hand-codes via prompt logic.

**Kilo's explicit rule precedence order.** Kilo documents exact precedence (agent prompts > project config > AGENTS.md > global config > skills) [OFFICIAL: kilo.ai/docs/customize/agents-md]. Momentum's authority-hierarchy rule is similar but less machine-readable. A manifested, enforceable precedence — not just a documented one — would reduce rule conflicts.

**Qwen's subagent lifecycle hooks.** `SubagentStart` and `SubagentStop` events do not exist in Claude Code's documented hook list. Momentum's spawning-patterns rule would benefit from these for audit logging of Fan-Out vs TeamCreate spawn events.

**Codex's `AGENTS.override.md` pattern.** Separating base AGENTS.md from an override file at the same level, loaded preferentially if present, lets a developer temporarily swap the global rule set without editing the canonical file. Useful for experiments and retros.

## Practical conclusions

If Momentum had to migrate off Claude Code today, the tier list is:

1. **Qwen Code** — near-zero porting cost for primitives; lose only workflow-DSL niceties
2. **OpenCode (sst)** — low porting cost; hooks rewrite shell→TS is the main friction
3. **Codex CLI** — medium cost; hook maturity warnings on non-Bash tools; slash-command/skill story still coalescing
4. **Kilo Code** — medium cost; nested AGENTS.md helps; hook absence forces external daemons
5. **Cline** — medium cost; hooks are good; subagent-spawn pattern doesn't map cleanly
6. **Roo Code** — high cost; modes instead of subagents; no hooks
7. **Goose AI** — high cost overall but workflows port *better*; compensate with external hook layer (file watchers) and MCP for tool capabilities
8. **ForgeCode** — high cost; no skills, no hooks; custom agents port but practice layer thin
9. **Continue.dev** — not currently viable as a practice host
10. **Aider** — not a practice host at all

The pattern: Claude Code's primitive set is being commoditized. By April 2026 the SKILL.md format is a cross-tool standard [PRAC: thepromptindex.com/how-to-use-ai-agent-skills-the-complete-guide], AGENTS.md is nearly universal, and hook systems are emerging. The distinctive Claude Code asset that Momentum leans on most heavily — nested CLAUDE.md loading with path-scoped rules and the workflow-fidelity rule over explicit step DSLs — remains the hardest to replicate on competitors. Kilo is the only documented nested loader, and no competitor has the `<check>`/`<action>`/`<critical>` DSL as a parseable structure.

The cross-cutting recommendation: Momentum should (a) adopt SKILL.md frontmatter conventions aggressively so skills stay portable, (b) design new rules to be path-scoped via frontmatter globs (Continue-style), not just placement, (c) move automation that truly depends on hooks (auto-commit, auto-rename) behind a small abstraction that can swap shell hooks → TS plugin → external daemon depending on host, and (d) consider whether the workflow DSL should be promoted to a parseable format (YAML-first, like Goose recipes) so it survives migration to a host without step-tag semantics.

## Sources

- [ForgeCode — Custom Rules (AGENTS.md)](https://forgecode.dev/docs/custom-rules/) [OFFICIAL]
- [ForgeCode — Custom Commands](https://forgecode.dev/docs/custom-commands/) [OFFICIAL]
- [ForgeCode — Agent Definition Guide](https://forgecode.dev/docs/agent-definition-guide/) [OFFICIAL]
- [Goose — Recipes guide](https://block.github.io/goose/docs/guides/recipes/) [OFFICIAL]
- [Goose — Recipe Reference](https://block.github.io/goose/docs/guides/recipes/recipe-reference/) [OFFICIAL]
- [Goose — Session Recipes (goose-docs.ai)](https://goose-docs.ai/docs/guides/recipes/session-recipes/) [OFFICIAL]
- [Goose — Sub-Recipes (Advent of AI Day 15)](https://dev.to/nickytonline/advent-of-ai-2025-day-15-goose-sub-recipes-3mnd) [PRAC]
- [OpenCode — Agents](https://opencode.ai/docs/agents/) [OFFICIAL]
- [OpenCode — Plugins (lifecycle hooks)](https://opencode.ai/docs/plugins/) [OFFICIAL]
- [OpenCode — Rules](https://opencode.ai/docs/rules/) [OFFICIAL]
- [OpenCode — Agent Skills](https://opencode.ai/docs/skills/) [OFFICIAL]
- [Qwen Code — Agent Skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) [OFFICIAL]
- [Qwen Code — Subagents](https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/) [OFFICIAL]
- [Qwen Code — Hooks (docs/users/features/hooks.md)](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/hooks.md) [OFFICIAL]
- [Qwen Code — AGENTS.md](https://github.com/QwenLM/qwen-code/blob/main/AGENTS.md) [OFFICIAL]
- [Kilo Code — AGENTS.md](https://kilo.ai/docs/customize/agents-md) [OFFICIAL]
- [Kilo Code — Custom Modes](https://kilo.ai/docs/customize/custom-modes) [OFFICIAL]
- [Kilo Code — Custom Rules](https://kilo.ai/docs/agent-behavior/custom-rules) [OFFICIAL]
- [Kilo Code — What's New April 2026](https://kilo.ai/docs/code-with-ai/platforms/vscode/whats-new) [OFFICIAL]
- [Aider — Chat modes](https://aider.chat/docs/usage/modes.html) [OFFICIAL]
- [Aider — Coding conventions](https://aider.chat/docs/usage/conventions.html) [OFFICIAL]
- [Aider — YAML config](https://aider.chat/docs/config/aider_conf.html) [OFFICIAL]
- [Cline — Rules docs](https://docs.cline.bot/customization/cline-rules) [OFFICIAL]
- [Cline v3.36 — Hooks blog post](https://cline.bot/blog/cline-v3-36-hooks) [OFFICIAL]
- [Cline — Stop adding rules when you need workflows](https://cline.ghost.io/stop-adding-rules-when-you-need-workflows/) [OFFICIAL]
- [Roo Code — Custom Modes](https://docs.roocode.com/features/custom-modes) [OFFICIAL]
- [Roo Code — Custom Instructions](https://docs.roocode.com/features/custom-instructions) [OFFICIAL]
- [Roo Code — AGENTS.md support issue #5966](https://github.com/RooCodeInc/Roo-Code/issues/5966) [OFFICIAL]
- [Roo Code — Hook enhancement issue #11504](https://github.com/RooCodeInc/Roo-Code/issues/11504) [OFFICIAL]
- [Roo Code — Hook on events issue #12025](https://github.com/RooCodeInc/Roo-Code/issues/12025) [OFFICIAL]
- [Continue.dev — Rules deep dive](https://docs.continue.dev/customize/deep-dives/rules) [OFFICIAL]
- [Continue.dev — Customization overview](https://docs.continue.dev/customize/overview) [OFFICIAL]
- [Continue.dev — AGENTS.md support issue #6716](https://github.com/continuedev/continue/issues/6716) [OFFICIAL]
- [Codex CLI — Slash commands](https://developers.openai.com/codex/cli/slash-commands) [OFFICIAL]
- [Codex CLI — AGENTS.md](https://developers.openai.com/codex/guides/agents-md) [OFFICIAL]
- [Codex CLI — Advanced configuration](https://developers.openai.com/codex/config-advanced) [OFFICIAL]
- [Codex Hooks — community release tracker](https://ai.sulat.com/codex-hooks-just-gave-you-back-complete-control-over-your-code-57d044bcae1b) [PRAC]
- [openai/codex — ApplyPatchHandler hook issue #16732](https://github.com/openai/codex/issues/16732) [OFFICIAL]
- [openai/codex — PreToolUse/PostToolUse issue #14754](https://github.com/openai/codex/issues/14754) [OFFICIAL]
- [hatayama/codex-hooks — reuses Claude Code hook settings](https://github.com/hatayama/codex-hooks) [PRAC]
- [Agentic Skills Frameworks Compared — Ry Walker](https://rywalker.com/research/agentic-skills-frameworks) [UNVERIFIED]
- [Agentic Coding Tools 2026 — 20-Platform Matrix](https://www.digitalapplied.com/blog/agentic-coding-tools-q2-2026-20-platform-matrix) [UNVERIFIED]
- [The Complete Guide to Agent Skills 2026](https://www.thepromptindex.com/how-to-use-ai-agent-skills-the-complete-guide.html) [PRAC]
