---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Portability across agentic CLIs — Claude Code-exclusive or multi-tool?"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Portability Across Agentic CLIs — ECC vs Momentum

## Inline Summary

ECC is **genuinely cross-tool, not Claude Code-only** — but the portability is uneven and built largely with adapter glue rather than a single unified runtime [OFFICIAL]. The repository ships first-class config trees for Claude Code, Codex, OpenCode, Cursor, and Gemini CLI, plus newer experimental targets (Kiro, Trae, CodeBuddy, Antigravity), with a Node-based selective installer that copies subsets into each target's expected paths [OFFICIAL]. The **AGENTS.md standard is real** — originated by OpenAI in August 2025, donated to the Linux Foundation's new Agentic AI Foundation (AAIF) in December 2025 alongside MCP and goose, and adopted by 60k+ projects and 25+ tools [OFFICIAL]. Verdict on the suspect claim: the prior report's framing of a single "Plugin-Everything architecture that is agnostic to the specific agentic CLI" is **overstated** — the actual mechanism is a per-tool adapter pattern with shared sources, not a runtime-neutral plugin format. Momentum, by comparison, is single-target Claude Code today and would need substantial work to follow ECC's multi-target path.

## ECC Repository Reality Check

The repository at `https://github.com/affaan-m/everything-claude-code` is a 167k-star, MIT-licensed monorepo with a stated mission of being "The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond." [OFFICIAL] It was created 2026-01-18 and pushed as recently as 2026-04-26 (today), so the project is live and actively iterated. Languages by byte volume break down as JavaScript ≈ 2.4 MB, Rust ≈ 1.8 MB, Python ≈ 235 KB, Shell ≈ 163 KB, with smaller TypeScript and PowerShell shares — which is itself the first hint that this is not a pure markdown plugin: there is real cross-platform installer code under `scripts/`. [OFFICIAL]

The top-level layout actually present in the repo includes the following tool-target directories (each shown to exist via the GitHub Contents API today):

- `.claude/` and `.claude-plugin/` — Claude Code home and plugin manifest
- `.codex/` — Codex CLI configuration tree (`config.toml`, `agents/`, `AGENTS.md`)
- `.codex-plugin/` — Codex marketplace plugin metadata
- `.opencode/` — OpenCode plugin (full TypeScript module, `index.ts`, `plugins/`, `prompts/`, `tools/`, `opencode.json`)
- `.cursor/` — Cursor IDE hooks tree (`hooks.json`, `hooks/*.js` adapter)
- `.gemini/` — Gemini CLI baseline (`GEMINI.md` only)
- `.kiro/`, `.trae/`, `.codebuddy/` — newer/experimental targets, mostly install scripts and READMEs
- `.agents/`, `agents/`, `commands/`, `skills/`, `rules/`, `hooks/`, `mcp-configs/`, `manifests/`, `plugins/` — shared sources
- `AGENTS.md` (root) — universal agent instruction file

The presence of these directories alone does not prove parity, so the rest of this report verifies what each target actually receives and how it is wired.

## Direct Support Per CLI

### Claude Code (CC)

Native and primary. `.claude-plugin/plugin.json` is a real Claude Code plugin manifest (`name: everything-claude-code`, `version: 1.10.0`, `skills: ["./skills/"]`, `commands: ["./commands/"]`). [OFFICIAL] Every other target appears to be a derivative of the CC sources — agents and skills authored against Claude Code conventions are then either reused via shared paths or transformed for the destination tool.

### OpenAI Codex CLI

Substantial support. `.codex/config.toml` is annotated as an "ECC Codex Reference Configuration" tied to the Codex schema at `https://developers.openai.com/codex/config-schema.json`. [OFFICIAL] Settings include `approval_policy`, `sandbox_mode`, `web_search`, `persistent_instructions = "Follow project AGENTS.md guidelines..."`, `[mcp_servers.*]` blocks for github/context7/exa/memory/playwright/sequential-thinking, `[features] multi_agent = true`, named profiles (`strict`, `yolo`), and a `[agents]` block referencing `agents/explorer.toml`, `agents/reviewer.toml`, `agents/docs-researcher.toml` — Codex-specific agent definitions that exist in `.codex/agents/`. There is also a separate `.codex-plugin/plugin.json` manifest with `name: ecc`, `version: 1.10.0`, `skills: "./skills/"`, `mcpServers: "./.mcp.json"`, and a Codex marketplace `interface` block. The repo carries a `scripts/sync-ecc-to-codex.sh` that backs up `~/.codex`, merges ECC's `AGENTS.md` into the user's existing one via marker-based merging, generates Codex prompts from `commands/*.md`, and merges MCP servers into `config.toml` via a Node TOML parser. This is real, plumbed-through Codex support.

### OpenCode (sst/opencode)

First-class. `.opencode/opencode.json` is an OpenCode-spec config (`$schema: https://opencode.ai/config.json`) declaring models, an `instructions` array that pulls `AGENTS.md`, `CONTRIBUTING.md`, and 11 skill `SKILL.md` files into the OpenCode instruction context, a `plugin: ["./plugins"]` reference, and an `agent` map that defines `build`, `planner`, `architect`, `code-reviewer`, `security-reviewer`, etc. with per-agent tool gates and prompt-file references (`{file:prompts/agents/planner.txt}`). [OFFICIAL] `.opencode/index.ts` is a published TypeScript plugin module exporting `ECCHooksPlugin` and metadata declaring 13 agents, 31 commands, 37 skills, plus hook events `file.edited`, `tool.execute.before`, `tool.execute.after` (and more). The repo also hosts a `scripts/build-opencode.js` referenced from the script list. So OpenCode gets both a config + a real npm-shippable plugin (`ecc-universal`).

### Cursor IDE

Bridge-layer support via an adapter pattern. `.cursor/hooks.json` is a Cursor-native hooks manifest with 14 hook events including `sessionStart`, `sessionEnd`, `beforeShellExecution`, `afterShellExecution`, `afterFileEdit`, `beforeMCPExecution`, `afterMCPExecution`, `beforeReadFile`, `beforeSubmitPrompt`, `subagentStart`, `subagentStop`, `beforeTabFileRead`, `afterTabFileEdit`, `preCompact`. [OFFICIAL] `.cursor/hooks/adapter.js` is a Cursor-to-Claude-Code adapter that reads Cursor's stdin JSON, transforms it into a Claude-Code-shaped `tool_input`/`tool_output`/`transcript_path` payload, then re-invokes the existing `scripts/hooks/*.js` files. Each per-event Cursor hook (`after-file-edit.js`, `before-shell-execution.js`, etc.) is a thin wrapper. There are also `.cursor/rules/`, `.cursor/skills/`, `.cursor/hooks/` shared. Cursor support is real but is explicitly an adapter that translates between event shapes — not a re-implementation.

### Gemini CLI

Thin. `.gemini/GEMINI.md` is the entire footprint and explicitly says "Gemini support is currently focused on a strong project-local instruction layer via `.gemini/GEMINI.md`, plus the shared MCP catalog and package-manager setup assets shipped by the installer." [OFFICIAL] There is, however, a real adapter: `scripts/gemini-adapt-agents.js` rewrites ECC agent frontmatter to use Gemini's tool names (Read → `read_file`, Write → `write_file`, Edit → `replace`, Bash → `run_shell_command`, Grep → `grep_search`, Glob → `glob`, WebSearch → `google_web_search`, WebFetch → `web_fetch`), and strips unsupported `color:` metadata. So the support exists, but it is more "we'll mechanically transform agents at install time" than "agents work natively as authored."

### Goose, Aider, Cline, ForgeCode

**Not supported by ECC.** The repository contains no `.goose`, `.aider`, `.cline`, or `.forgecode` directories, no skills referencing those harnesses, and no installer adapters for them. [OFFICIAL] The README excerpt fetched does not mention them. This matters because Goose is itself one of the three founding contributions to the Linux Foundation's Agentic AI Foundation, so its absence is conspicuous if ECC truly aspired to "every major harness." Aider is conspicuously listed by the AGENTS.md project as a supported tool, yet ECC does not appear to ship Aider-specific assets either.

### Other targets

`.kiro/`, `.trae/`, and `.codebuddy/` directories exist with READMEs and install/uninstall scripts but no deep config — these are bridgeheads, not full ports. [PRAC] Antigravity and Grok appear in README copy as "supported with manual fallback," not first-class targets.

## Format Compatibility — Are Skill/Agent Markdowns Reusable As-Is?

Mostly yes for skills, with caveats for agents.

**Skills** are markdown files with YAML frontmatter (the same `SKILL.md` convention Anthropic publishes for Claude Code Agent Skills). Both OpenCode and Codex accept skill markdown as input — `.opencode/opencode.json` lists `skills/tdd-workflow/SKILL.md` directly in its `instructions` array, meaning the OpenCode runtime ingests the same source files Claude Code uses. [OFFICIAL] The Codex integration generates prompts from `commands/*.md` rather than from `skills/`, so skill reuse there is partial.

**Agents** are not always portable as-is. The Gemini adapter (`scripts/gemini-adapt-agents.js`) exists precisely because Gemini CLI uses different tool names and frontmatter conventions than Claude Code, so authored agents must be transformed at install time. [OFFICIAL] Codex agents under `.codex/agents/*.toml` are TOML, not markdown — a deliberate format split because Codex multi-agent uses TOML configs. OpenCode agents are defined inside `opencode.json` as JSON entries that point to `prompts/agents/*.txt` files — a third encoding for the same concept.

**Hooks** are categorically not reusable across runtimes (see "Hook Portability" below). They are the least portable piece of the stack.

So the reality is: skill markdown is largely portable because it is just "instructional markdown the model reads"; agent definitions need format conversion because each tool encodes them differently; hooks need outright re-implementation. ECC's strategy is to keep the source content shared (single skills/agents trees) and add adapters per target, rather than to invent a universal format.

## AGENTS.md — Real Standard?

Yes, AGENTS.md is real and well-codified.

- **Origin**: introduced by OpenAI in August 2025 as "a simple, universal standard … that gives AI coding agents a consistent source of project-specific guidance" alongside Codex. [OFFICIAL]
- **Governance**: donated to the Linux Foundation in December 2025 as one of three founding projects of the **Agentic AI Foundation (AAIF)**, alongside Anthropic's Model Context Protocol (MCP) and Block's goose. Press release confirmed by Linux Foundation, OpenAI, Anthropic, and TechCrunch. [OFFICIAL]
- **Adoption**: 60k+ open-source projects, 25+ tools listed as supporting the format including GitHub Copilot Coding Agent, OpenAI Codex, Google Jules, Gemini CLI, Cursor, VS Code, Zed, Aider, Devin, Windsurf, UiPath, JetBrains Junie. [OFFICIAL]
- **Spec**: hosted at `https://agents.md` with an accompanying repo at `https://github.com/openai/agents.md`. The format has no required fields — it is "just standard Markdown" — with common conventions for setup, code style, testing, PR rules, and security. Monorepos may use nested AGENTS.md files where the closest file wins. [OFFICIAL]
- **AAIF members** (2026): Platinum tier includes AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI; Gold tier includes Adyen, Arcade.dev, Cisco, Datadog, Docker, Ericsson, IBM, JetBrains, Okta, Oracle, Salesforce, SAP, Shopify, Snowflake, Temporal, Twilio, others. [OFFICIAL]

So when the prior report alluded to "the AGENTS.md standard" it was correct on the existence of the standard. ECC genuinely uses it: a real `AGENTS.md` lives at the repo root with project rules ("Agent-First", "Test-Driven", "Security-First", "Immutability", "Plan Before Execute", agent table, security guidelines, testing requirements, workflow surface policy), plus a separate `.codex/AGENTS.md` for Codex-specific overlays. [OFFICIAL] OpenCode is configured to read root `AGENTS.md` first via `instructions`. Codex is told to "Follow project AGENTS.md guidelines" via `persistent_instructions`. This is exactly how the standard is intended to be consumed.

The caveat: AGENTS.md is **a content convention, not a runtime**. It does not give you portable hooks, portable plugin manifests, or portable agent definitions. It is the lowest-common-denominator integration: every agentic tool reads markdown, so a markdown file at a known location works everywhere. ECC leans on this pragmatically.

## MCP Portability

MCP itself is portable in principle — that is the whole point of a protocol — and ECC treats it that way. There is a single `mcp-configs/mcp-servers.json` source, a top-level `.mcp.json`, and per-target merge logic.

- **Claude Code**: MCP servers are merged into Claude Code's settings via the installer.
- **Codex**: `.codex/config.toml` carries `[mcp_servers.*]` blocks with TOML syntax. The sync script merges into the user's `~/.codex/config.toml` add-only. [OFFICIAL]
- **OpenCode**: MCP integration goes through OpenCode's own plugin system (the `.opencode/plugins` tree), not direct config injection.
- **Cursor**: MCP is gated by `before-mcp-execution.js` and `after-mcp-execution.js` hooks that audit and log calls.
- **Gemini CLI**: README claims "shared MCP catalog … shipped by the installer" but the only Gemini-specific file is `GEMINI.md`, so the actual mechanism is unclear.

**Client-specific quirks observed**: TOML in Codex vs. JSON in Claude Code's settings vs. JSON in OpenCode's `opencode.json`; different startup-timeout fields; Cursor wrapping MCP calls through hooks rather than direct config; OpenCode preferring its plugin SDK over direct MCP config injection. So while MCP is *protocol*-portable, the **declarations of MCP servers** are not — every tool wants its own format. This is exactly the friction the AAIF was created to address. [PRAC]

## Hook Portability

Hooks are the least portable layer in any agentic stack, and ECC's design accepts that and works around it via the adapter pattern.

- **Claude Code hooks** are JSON in `.claude/settings.json` (or plugin `hooks/hooks.json`) with events `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, etc. Eight events total per ECC's `AGENTS.md`.
- **Cursor hooks** are JSON in `.cursor/hooks.json` with 15 events including `beforeReadFile`, `beforeSubmitPrompt`, `beforeTabFileRead`, `afterTabFileEdit` (Tab refers to Cursor's Tab autocomplete agent). [OFFICIAL]
- **OpenCode hooks** are TypeScript plugin functions in `.opencode/plugins/index.ts` with events `file.edited`, `tool.execute.before`, `tool.execute.after`, etc. — 11+ events. [OFFICIAL]
- **Codex** appears to have no equivalent hook concept in `config.toml` — Codex relies on `persistent_instructions` and `notify` commands instead.
- **Gemini CLI** — no hook concept exposed.

ECC's strategy is the **DRY adapter**: keep the actual hook business logic in `scripts/hooks/*.js` (Node), then write per-tool wrappers that translate the tool's stdin payload into the Claude-Code-shaped payload that the canonical hook scripts expect. The Cursor `adapter.js` quoted earlier is the cleanest example. The repo also exposes runtime gates (`ECC_HOOK_PROFILE`, `ECC_DISABLED_HOOKS` env vars) so a user can toggle hooks without editing files. [OFFICIAL]

What this means in practice: the *behavior* of an ECC hook can be ported because the Node business logic is shared, but the *event surface* — which events fire and what payload they carry — is fundamentally per-tool. There is no portable "hook protocol" today. **Most of ECC's hook portability story is engineering glue, not standard-based interop.**

The fraction of ECC that is portable vs. CC-only is hard to pin precisely, but a defensible estimate from the repo evidence:

- **Highly portable**: skill markdown (most), AGENTS.md content, MCP server *intent*, ~80% of agent prompt content.
- **Adapter-required**: agent frontmatter formats, MCP server *configuration syntax*, hook business logic invocations.
- **Per-tool re-implemented**: hook event manifests, plugin manifests, install scripts, slash-command shims.

So perhaps **60–70% of ECC's value is portable across CC + Codex + OpenCode + Cursor**, with declining portability into Gemini CLI (~30–40%, mostly AGENTS.md and skill text) and into Goose/Aider/Cline (~0%, no integration shipped). [PRAC]

## Plugin Manifests

`plugin.json` is **Claude-Code-specific** as a manifest format. ECC ships a `.claude-plugin/plugin.json` matching Claude Code's plugin schema (`name`, `version`, `skills`, `commands`). [OFFICIAL] But ECC also ships:

- `.codex-plugin/plugin.json` — Codex marketplace manifest with a different schema (`mcpServers`, `interface`, `defaultPrompt`).
- `.opencode/package.json` + `.opencode/index.ts` — npm package + TypeScript plugin entry, OpenCode's plugin model.
- `agent.yaml` (top-level) — yet another manifest, format unverified.
- `manifests/` directory — multiple per-target install manifests.

There is no cross-tool plugin manifest standard. Each agentic CLI defines its own plugin/marketplace format, and ECC writes one per target. The `scripts/install-apply.js` runtime acts as the fan-out: it parses `--target` (`claude` | `cursor` | `antigravity` and others), resolves a profile or module list, and applies the right copy operations into the right destination paths via `lib/install-manifests.js` and `lib/install-executor.js`. This is a real package-manager-shaped installer, not a thin file-copy script.

## Comparison With Momentum's Portability Story

Momentum is **single-target Claude Code** today, by every metric I can find:

- **Plugin manifest**: `/Users/steve/projects/momentum/skills/momentum/.claude-plugin/plugin.json` declares `name: momentum, version: 0.17.0, description: "Agentic engineering practice — rules, agents, quality gates, and workflow automation across projects"` with no cross-tool fields. There is no `.codex-plugin/`, `.opencode/`, `.cursor/`, `.gemini/`, or `AGENTS.md` at the project root. [OFFICIAL]
- **Layout**: `skills/momentum/{agents, commands, hooks, references, scripts, skills}` follows Claude Code's plugin convention exactly.
- **Hooks**: `skills/momentum/hooks/hooks.json` uses Claude Code-specific event names (`PreToolUse`, `PostToolUse`, `Stop`) and the `$CLAUDE_PROJECT_DIR` and `$CLAUDE_TOOL_INPUT_FILE_PATH` environment variables. These are CC-only event names; they would not fire under Codex, OpenCode, or Cursor as written. [OFFICIAL]
- **Skill frontmatter**: Skills like `momentum:research`, `momentum:upstream-fix`, `momentum:architecture-guard`, `momentum:plan-audit` use the `model:`, `effort:`, `context:`, `allowed-tools:` keys that match Claude Code's Agent Skills spec. The `model: claude-opus-4-6` and `model: sonnet` values are Claude-only model handles, not portable to Codex/OpenAI or Gemini. [OFFICIAL]
- **AGENTS.md**: Not present at project root. Project-level guidance lives in `CLAUDE.md`, which is the Claude-Code-specific equivalent.

Should Momentum be cross-tool? Three considerations:

1. **AGENTS.md is the cheap win.** Authoring an `AGENTS.md` at the project root (or symlinking from `CLAUDE.md` via marker-based merge as ECC does) gets Momentum readable by Codex, OpenCode, Cursor, Gemini, GitHub Copilot Coding Agent, Aider, and others that respect the standard — at the cost of keeping the file generic enough not to assume Claude Code idioms. This is hours of work, not weeks.
2. **Skill content is largely portable.** Most Momentum skill markdown is instructional prose for the model — that text is ~85% portable. The frontmatter (`model: claude-opus-4-6`, `allowed-tools: Read, Glob, Grep, Bash`) is CC-specific and would need a per-target adapter, similar to ECC's `gemini-adapt-agents.js`. The `Skill tool`–style invocation pattern (`/momentum:foo`) is Claude-Code-specific and would need slash-command shims for OpenCode or prompt files for Codex.
3. **Hooks and Impetus orchestration are the deep CC dependencies.** The Stop-gate hook, the file-protection PreToolUse hook, and any sub-agent spawning pattern (`Task`, `TeamCreate`, `Agent`) are tied to Claude Code's runtime. Porting these is the same engineering problem ECC solved with the Cursor adapter and OpenCode plugin — significant work, possibly a month-plus of effort per target.

The strategic question for Momentum is whether cross-tool support is a **product** or a **distraction**. ECC's bet is that being "the agent harness performance optimization system" requires a presence in every harness. Momentum's positioning as an "agentic engineering practice" is more methodological and could plausibly stay Claude-Code-native, with AGENTS.md as a courtesy export so that other tools at least see the project's intent. There is also a middle path — keep the runtime CC-only, but ship a minimal `momentum-bridge` package that exports an AGENTS.md, the rules/, and the references/ as a Codex/OpenCode reference — at a fraction of the cost of full ECC-style ports.

## Comparative Verdict

| Dimension | ECC (2026-04-26) | Momentum (0.17.0) |
|---|---|---|
| Claude Code | Native, primary | Native, only target |
| Codex CLI | Full: config.toml, agents, AGENTS.md, sync script | None |
| OpenCode | Full: TypeScript plugin, opencode.json, npm package | None |
| Cursor IDE | Adapter-based: hooks.json + Cursor→CC payload bridge | None |
| Gemini CLI | Thin: GEMINI.md + agent frontmatter rewriter | None |
| Goose | Not supported | Not supported |
| Aider | Not supported | Not supported |
| Cline | Not supported | Not supported |
| ForgeCode | Not supported | Not supported |
| AGENTS.md at root | Yes, used as universal layer | No |
| MCP catalog | Single source, per-tool merge | Not exposed at plugin level |
| Hook portability | Adapter pattern (DRY business logic) | CC-only, $CLAUDE_* env vars |
| Plugin manifests | Per-tool (claude-plugin, codex-plugin, opencode npm) | Single CC manifest |
| Selective installer | Yes (`install-apply.js`, profiles, `--target`) | No |

**Final verdict on the suspect claim** — the prior report's wording of a single "Plugin-Everything architecture agnostic to the specific agentic CLI" is **not how ECC actually works**. ECC is a **multi-target monorepo with a per-target adapter pattern and a smart selective installer** that copies different subsets of shared sources into each tool's expected paths. The shared-sources part is real and substantial. The "agnostic" framing is marketing — under the hood, every target requires its own glue. AGENTS.md is the closest thing to a true cross-tool standard ECC relies on, and the standard is real, OpenAI-originated, and now under Linux Foundation governance. ECC is genuinely cross-tool in a way Momentum is not, and would be a credible reference architecture if Momentum ever decided to expand beyond Claude Code.

## Sources

- ECC repo: [github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — root file/dir listing, README, AGENTS.md, .claude-plugin/plugin.json, .codex/config.toml, .codex-plugin/plugin.json, .opencode/opencode.json, .opencode/index.ts, .cursor/hooks.json, .cursor/hooks/adapter.js, .gemini/GEMINI.md, scripts/install-apply.js, scripts/sync-ecc-to-codex.sh, scripts/gemini-adapt-agents.js — all retrieved 2026-04-26 via `gh api repos/affaan-m/everything-claude-code/contents/...`
- ECC homepage: [ecc.tools](https://ecc.tools)
- AGENTS.md spec site: [agents.md](https://agents.md)
- AGENTS.md GitHub: [github.com/openai/agents.md](https://github.com/openai/agents.md)
- Linux Foundation press release on AAIF: [linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- OpenAI announcement: [openai.com/index/agentic-ai-foundation](https://openai.com/index/agentic-ai-foundation/)
- Anthropic MCP donation post: [anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- TechCrunch coverage: [techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era](https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/)
- AAIF 2026 events program: [linuxfoundation.org/press/agentic-ai-foundation-announces-global-2026-events-program-anchored-by-agntcon-mcpcon-north-america-and-europe](https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-global-2026-events-program-anchored-by-agntcon-mcpcon-north-america-and-europe)
- Codex config schema (referenced from ECC `.codex/config.toml`): [developers.openai.com/codex/config-reference](https://developers.openai.com/codex/config-reference) and [developers.openai.com/codex/multi-agent](https://developers.openai.com/codex/multi-agent)
- OpenCode config schema (referenced from ECC `.opencode/opencode.json`): [opencode.ai/config.json](https://opencode.ai/config.json)
- IntuitionLabs analysis of AAIF: [intuitionlabs.ai/articles/agentic-ai-foundation-open-standards](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards)
- Solo.io commentary on AAIF: [solo.io/blog/aaif-announcement-agentgateway](https://www.solo.io/blog/aaif-announcement-agentgateway)
- Privacy Guides news on AAIF: [privacyguides.org/news/2025/12/24/the-linux-foundation-announces-formation-of-the-agentic-ai-foundation](https://www.privacyguides.org/news/2025/12/24/the-linux-foundation-announces-formation-of-the-agentic-ai-foundation/)
- EdTech Innovation Hub coverage: [edtechinnovationhub.com/news/linux-foundation-creates-agentic-ai-foundation-to-steward-open-standards-for-autonomous-ai-systems](https://www.edtechinnovationhub.com/news/linux-foundation-creates-agentic-ai-foundation-to-steward-open-standards-for-autonomous-ai-systems)
- Momentum local repo: `/Users/steve/projects/momentum/skills/momentum/.claude-plugin/plugin.json`, `/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json`, `/Users/steve/projects/momentum/skills/momentum/skills/*/SKILL.md` — read 2026-04-26
