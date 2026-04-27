---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "everything-claude-code (ECC) as exemplar — repo structure, install/update flow, distributable assets, Claude-Code-specific bits, portability analysis."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# everything-claude-code (ECC) as Exemplar — Technical Deep Dive

## Inline Summary

The most reusable parts of ECC for a multi-agent practice module are (a) its **manifest-driven selective installer** (`install-profiles.json` × `install-modules.json` × `install-apply.js`) which decouples logical bundles ("security profile", "research profile") from physical per-target file layouts, (b) its **shared-source / per-target adapter pattern** (single `skills/`, `agents/`, `commands/`, `hooks/`, `mcp-configs/` trees fanned out to `.claude/`, `.codex/`, `.opencode/`, `.cursor/`, `.gemini/` via Node mutators), and (c) its acceptance that **AGENTS.md is the only true cross-tool content layer** — everything else (hook event surface, plugin manifest, agent encoding) requires per-agent glue [OFFICIAL]. ECC is **not** a runtime-neutral plugin; it is a monorepo of canonical sources plus an installer that knows how each target wants to receive them. That architectural separation is the lift Momentum can copy without copying ECC's surface area.

## Canonical Repo

- **Source:** `https://github.com/affaan-m/everything-claude-code` ([repo](https://github.com/affaan-m/everything-claude-code)) — MIT, branch `main`, created 2026-01-18, last push 2026-04-26 [OFFICIAL].
- **Live numbers (GitHub REST API, 2026-04-26):** 167,488 stars / 25,969 forks / 159 contributors / 12 releases / ~1,465 commits; version `1.10.0` synchronized across `VERSION`, `package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `agent.yaml` [OFFICIAL].
- **Homepage:** `https://ecc.tools`.
- **Naming:** three non-interchangeable identifiers — GitHub `affaan-m/everything-claude-code`, Claude plugin `everything-claude-code@everything-claude-code`, npm `ecc-universal`. README calls the trifurcation intentional ([README.md](https://github.com/affaan-m/everything-claude-code/blob/main/README.md)) [OFFICIAL].

## Repository Structure (Top 3 Levels)

Verified live via `gh api .../contents/` and the recursive git tree (2,662 entries, not truncated) [OFFICIAL]:

```
everything-claude-code/
├── .claude-plugin/        plugin.json + marketplace.json (canonical Claude manifest)
├── .claude/               Claude Code staging (commands/, rules/, skills/, team/)
├── .codex/                AGENTS.md, agents/*.toml (3), config.toml
├── .codex-plugin/         plugin.json (Codex marketplace)
├── .cursor/               hooks.json (14 events), hooks/adapter.js, rules/, skills/
├── .gemini/               GEMINI.md only (token surface)
├── .opencode/             opencode.json, index.ts, plugins/, prompts/agents/, tools/, commands/, package.json
├── .agents/, .kiro/, .trae/, .codebuddy/   bridgeheads
├── agents/                48 canonical agent .md (shared source)
├── commands/              79 slash-command .md (shared source)
├── skills/                183 skill dirs each w/ SKILL.md (shared source)
├── rules/                 89 .md across 15 lang/common subdirs (shared source)
├── hooks/                 hooks.json + README only
├── mcp-configs/           mcp-servers.json (24+ templates)
├── manifests/             install-{profiles,modules,components}.json
├── schemas/               JSON schemas
├── scripts/
│   ├── install-apply.js, install-plan.js, uninstall.js, repair.js, doctor.js, ecc.js
│   ├── gemini-adapt-agents.js, sync-ecc-to-codex.sh, build-opencode.js
│   ├── ci/                validators (validate-skills.js, ...)
│   ├── codex/             merge-codex-config.js, merge-mcp-config.js
│   └── hooks/             40 hook scripts
├── ecc2/                  Rust 2.0 alpha (Cargo + src/)
├── tests/                 ~102 test files
├── ecc_dashboard.py       39 KB Tkinter desktop GUI
├── install.sh, install.ps1, package.json (ecc-universal@1.10.0), agent.yaml
├── AGENTS.md, CLAUDE.md, SOUL.md, RULES.md, the-*-guide.md
└── README.md (~69 KB)
```

The deliberate split: top-level `agents/`, `commands/`, `skills/`, `rules/`, `hooks/`, `mcp-configs/` are **canonical sources**; dot-prefixed directories (`.claude/`, `.codex/`, `.opencode/`, `.cursor/`, `.gemini/`) are **per-target staging** the installer copies into or merges with user home/project paths [OFFICIAL].

## Plugin Packaging

### Claude Code: `.claude-plugin/plugin.json`

The canonical Claude plugin manifest is intentionally minimal ([plugin.json](https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/plugin.json)) [OFFICIAL]:

```json
{
  "name": "everything-claude-code",
  "version": "1.10.0",
  "description": "Battle-tested Claude Code plugin for engineering teams — 38 agents, 156 skills, 72 legacy command shims, production-ready hooks, and selective install workflows evolved through continuous real-world use",
  "author": { "name": "Affaan Mustafa", "url": "https://x.com/affaanmustafa" },
  "homepage": "https://ecc.tools",
  "repository": "https://github.com/affaan-m/everything-claude-code",
  "license": "MIT",
  "skills": ["./skills/"],
  "commands": ["./commands/"]
}
```

Two relative-path fields, `skills` and `commands`, point Claude Code at the canonical directories. **Note what is missing**: no explicit `agents`, no `hooks`, no `mcp` — those load from convention-discovered locations or are deferred to manual install (rules) or to a sibling plugin runtime. The README explicitly states "Claude Code plugins cannot distribute `rules` automatically" — so rules are the single artifact class that requires user-side `cp -R` regardless of plugin install [OFFICIAL].

### Marketplace: `.claude-plugin/marketplace.json`

The marketplace file is a single-plugin entry: top-level `name`, `owner`, `metadata.description`, then a `plugins[]` array containing one object with `name`, `source: "./"` (the repo itself acts as both marketplace and the plugin's source root), `version`, `author`, `homepage`, `repository`, `license`, `keywords[]`, `category: "workflow"`, `tags[]`, and `strict: false` (permitting non-strict matching during install) [OFFICIAL].

### Per-Harness Manifests

ECC ships **parallel manifests** for non-Claude harnesses with deliberately different schemas:

- **`.codex-plugin/plugin.json`** — `name: ecc`, version `1.10.0`, declares `skills: "./skills/"` and `mcpServers: "./.mcp.json"`, plus a Codex-specific `interface` block (`defaultPrompt`, `category`) [OFFICIAL].
- **`agent.yaml`** — top-level gitagent manifest (`spec_version: "0.1.0"`) with `model.preferred: claude-opus-4-6`, `fallback: [claude-sonnet-4-6]`, explicit lists of ~135 skills and ~80 commands [OFFICIAL].
- **`package.json`** — npm package `ecc-universal@1.10.0` exposing binaries `ecc` (`scripts/ecc.js`) and `ecc-install` (`scripts/install-apply.js`); `engines.node: >=18`; deps `@iarna/toml`, `ajv`, `sql.js` [OFFICIAL].
- **`.opencode/index.ts`** — npm-shippable TypeScript module exporting `ECCHooksPlugin`, with metadata declaring 13 agents, 31 commands, 37 skills, hook events `file.edited`, `tool.execute.before/after`, `session.created/idle/deleted`, `file.watcher.updated`, `permission.ask`, `todo.updated`, `shell.env`, `experimental.session.compacting`, and custom tools `run-tests`, `check-coverage`, `security-audit`, `format-code`, `lint-check`, `git-summary`, `changed-files` [OFFICIAL].

The metadata counts **diverge from the canonical sources on purpose** — OpenCode gets a curated subset, not the full 183-skill catalog. The selective installer makes that divergence cheap to maintain.

## Install / Update Flow

### Three Install Paths Coexist

README documents three paths in preference order [OFFICIAL]: (1) **Claude marketplace** — `/plugin marketplace add https://github.com/affaan-m/everything-claude-code` then `/plugin install everything-claude-code@everything-claude-code` — loads skills, commands, hooks; does *not* load rules (platform limit); (2) **OSS shell installer** — `git clone && npm install && ./install.sh --profile full` — selective, also works for non-Claude targets; (3) **npm direct** — `npx ecc-install --profile full`. README explicitly warns that running the OSS installer *after* a plugin install creates duplicate skills and double-fires hooks — unusual operational signage.

### The Installer Pipeline

`install.sh` is a POSIX wrapper that auto-installs Node deps and `exec node scripts/install-apply.js "$@"` ([install.sh](https://github.com/affaan-m/everything-claude-code/blob/main/install.sh)) [OFFICIAL]; `install.ps1` mirrors it on Windows.

The Node entrypoint `scripts/install-apply.js` (~150 lines + `lib/` modules) ([install-apply.js](https://github.com/affaan-m/everything-claude-code/blob/main/scripts/install-apply.js)) [OFFICIAL] parses `--target <claude|cursor|antigravity|codex|gemini|opencode|codebuddy>`, `--profile <name>`, `--modules <ids>`, `--with`/`--without <component>`, `--config <path>`, `--dry-run`, `--json`. It resolves through `lib/install/request.js`, optionally loads `ecc-install.json`, builds a plan via `lib/install/runtime.js` (with `projectRoot`, `homeDir`, `claudeRulesDir`), and executes via `lib/install-executor.js`. The plan object exposes `mode`, `target`, `adapter.id`, `installRoot`, `installStatePath`, `operations[]` (each `sourceRelativePath` → `destinationPath`), `selectedModuleIds`, `excludedModuleIds`, `skippedModuleIds`, `warnings`. `--dry-run --json` emits a machine-readable plan before any file is touched.

This is a real package-manager-shaped pipeline — planning, dry-run, JSON output, install-state tracking, per-target adapter dispatch — not a glorified `cp -R`.

### Manifest-Driven Selection

The selective install architecture is ECC's single most reusable piece. It rests on three JSON manifests under `manifests/`:

**`install-profiles.json`** ([profiles](https://github.com/affaan-m/everything-claude-code/blob/main/manifests/install-profiles.json)) [OFFICIAL] declares 5 profiles (`core`, `developer`, `security`, `research`, `full`), each just a list of module IDs.

**`install-modules.json`** ([modules](https://github.com/affaan-m/everything-claude-code/blob/main/manifests/install-modules.json)) [OFFICIAL] is the heart — 20 modules, each declaring `id`, `kind` (rules/agents/commands/hooks/platform/skills), `paths[]` (relative to repo root), `targets[]` (which harnesses can receive this module), `dependencies[]` (other module IDs), `defaultInstall`, `cost`, `stability`. Example: `platform-configs` declares `paths: [".claude-plugin",".codex",".cursor",".gemini",".opencode","mcp-configs","scripts/setup-package-manager.js"]` and `targets: ["claude","cursor","antigravity","codex","gemini","opencode","codebuddy"]`. `framework-language` lists 39 skill paths and depends on `rules-core`, `agents-core`, `commands-core`, `platform-configs`.

Three properties: (1) module `paths` reference canonical sources only — per-target shape changes happen in the install adapter, not the manifest; (2) `targets[]` is a whitelist — `agents-core` deliberately omits `opencode` and `gemini` because they receive agents through other channels (OpenCode's `opencode.json` agent map; Gemini's rewriter); (3) `dependencies[]` resolves a transitive closure (`security` pulls `workflow-quality` pulls `platform-configs`).

**`install-components.json`** is the user-facing toggle layer. So the install equation is: **profile → modules (with deps) → paths × target adapter → file operations**. This is the abstraction Momentum currently lacks entirely.

### Update Mechanism

ECC has **three** update paths and the README is explicit that they don't compose [OFFICIAL]:

1. **Claude marketplace update**: `/plugin marketplace update everything-claude-code` then `/plugin install everything-claude-code@everything-claude-code` (re-install picks up new version).
2. **Git pull + re-run installer**: `git pull && ./install.sh --profile <same-profile>`. The installer is idempotent against `installStatePath` (a state file that records what was placed where) — a re-run reconciles deltas.
3. **npm**: `npm install -g ecc-universal@latest` then `ecc-install --profile <same-profile>`.

ECC ships `scripts/repair.js`, `scripts/doctor.js`, and `scripts/list-installed.js` to diagnose and recover from drift between expected and actual install state — recognition that long-running installs go out of sync.

## What ECC Distributes

Verified against the live tree 2026-04-26:

| Asset | Count | Location | Per-target encoding |
|---|---|---|---|
| Agents | 48 `.md` (frontmatter `name`/`description`/`tools`/`model`) | `agents/` | Claude `.md` native; Codex `.toml` (3 ship); OpenCode JSON map → `prompts/agents/*.txt`; Gemini rewritten frontmatter |
| Skills | 183 dirs (`SKILL.md` w/ `name`/`description`/`origin`) | `skills/<name>/` | Markdown reusable; OpenCode lists 13 in `instructions[]` |
| Slash commands | 79 `.md` | `commands/` | Claude native; Codex `generate_prompt_file()`; OpenCode 34 in `.opencode/commands/` |
| Hook scripts | 40 `.js` | `scripts/hooks/` | Shared Node business logic; per-tool wrappers in `.cursor/hooks/`, `.opencode/plugins/` |
| Hook config | 1 `hooks.json` | `hooks/` | Claude `PreToolUse/PostToolUse/Stop/PreCompact/SessionStart` |
| Rules | 89 `.md` across 15 dirs | `rules/{common,cpp,csharp,...,zh}/` | Manual `cp -R` per README |
| MCP servers | 6 default + 24+ catalog | `.mcp.json` + `mcp-configs/mcp-servers.json` | Per-target merge: Claude settings, Codex TOML `[mcp_servers.*]`, OpenCode plugin |
| Output styles / status lines | 0 | — | Not a discrete category |
| Plugin manifests | 4 | `.claude-plugin/`, `.codex-plugin/`, `package.json`+`.opencode/index.ts` | Per-tool by definition |
| Install manifests | 3 (profiles, modules, components) | `manifests/` | Tool-agnostic (selection layer) |

Counts disagree across ECC's own self-descriptions (live 48/183/79; plugin manifest 38/156/72; SOUL.md 30/135/60; agent.yaml ~135/~80). The v1.10.0 "synced counts to the live OSS surface" claim in `CHANGELOG.md` was already stale on report date [OFFICIAL].

### Examples of Non-Trivial Behavior

**Hook with substantive logic.** The Claude `hooks.json` `PreToolUse` matcher for `Bash` is a single ~30-line `node -e` expression that probes six possible plugin install paths (`~/.claude`, `~/.claude/plugins/ecc`, `~/.claude/plugins/ecc@ecc`, `marketplace/ecc`, `everything-claude-code`, `everything-claude-code@everything-claude-code`, plus `cache/<name>/<version>` glob), settles on `CLAUDE_PLUGIN_ROOT`, then `require()`s `scripts/hooks/plugin-hook-bootstrap.js` ([hooks/hooks.json](https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json)) [OFFICIAL]. The defensive probing reveals chronic Claude plugin path resolution drift in production.

**Skill — `tdd-workflow`.** Frontmatter `name`/`description`/`origin: ECC`. Body declares "Git Checkpoints" (compile-time RED acceptable as proxy for runtime RED), a Step 1/2/3 RED-GREEN-REFACTOR template with TypeScript Jest examples, and an 80% coverage gate ([SKILL.md](https://github.com/affaan-m/everything-claude-code/blob/main/skills/tdd-workflow/SKILL.md)) [OFFICIAL].

**Multi-target agent — `code-reviewer`.** Same content lives at `agents/code-reviewer.md` (Claude frontmatter `tools: ["Read","Grep","Glob","Bash"]`, `model: sonnet`), as a JSON entry in `.opencode/opencode.json` with `prompt: "{file:prompts/agents/code-reviewer.txt}"` and `tools: { read: true, bash: true, write: false, edit: false }`, and (after Gemini adapter) with `tools: [read_file, grep_search, glob, run_shell_command]` [OFFICIAL].

## Claude-Code-Specific Bits

The following ECC artifacts have **no equivalent** outside Claude Code and would have to be re-implemented or dropped on a port:

- **`.claude-plugin/plugin.json` schema and the `/plugin marketplace` mechanic.** Anthropic-defined; not used by any other harness [OFFICIAL].
- **Hook event names `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`, `SessionStart` and matchers like `Bash`, `Edit|Write`.** Every other harness uses different event vocabularies (Cursor: `beforeShellExecution`, `afterFileEdit`, `beforeMCPExecution`, `subagentStart`, etc.; OpenCode: `tool.execute.before`, `file.edited`, `session.created`, `permission.ask`, etc.) [OFFICIAL].
- **`CLAUDE_PLUGIN_ROOT` / `$CLAUDE_PROJECT_DIR` / `$CLAUDE_TOOL_INPUT_FILE_PATH` env vars** referenced throughout `scripts/hooks/`. Not present in Codex, OpenCode, Gemini, Cursor [OFFICIAL].
- **Sub-agent invocation contract via `Task` / agent frontmatter `tools:` `model:` keys.** The frontmatter shape is Anthropic's; Codex multi-agent uses TOML (`[agents.*]` blocks), OpenCode uses an `agent` map in `opencode.json`, Gemini uses different tool names altogether [OFFICIAL].
- **Plugin path resolution heuristics in `hooks.json`.** The 30-line probe expression exists *because* of Claude marketplace cache layout — irrelevant on any other harness.
- **The "rules cannot be distributed via plugin" limitation** itself is a Claude-Code-specific platform constraint that drives ECC's "Step 2: Install Rules (Required)" manual `cp -R` ritual [OFFICIAL].

## Things That Translate Readily to Other Agents

- **`SKILL.md` markdown content** — instructional prose for the model is ~85% portable verbatim. OpenCode literally reads `skills/tdd-workflow/SKILL.md`, `skills/security-review/SKILL.md`, etc. directly via its `instructions[]` array in `opencode.json` ([opencode.json](https://github.com/affaan-m/everything-claude-code/blob/main/.opencode/opencode.json)) [OFFICIAL].
- **`AGENTS.md`** at the repo root — readable by Codex, OpenCode (via `instructions[]`), Cursor, Gemini, GitHub Copilot Coding Agent, Aider, JetBrains Junie, and ~25 other tools per the agents.md spec [OFFICIAL].
- **MCP server *intent*** — every harness understands the MCP protocol, but each wants its own *declaration syntax* (Claude JSON, Codex TOML, OpenCode JSON-via-plugin, Cursor wrapped through hooks). ECC keeps a single source `mcp-configs/mcp-servers.json` and per-target merge scripts (`scripts/codex/merge-mcp-config.js`, `scripts/codex/merge-codex-config.js`) [OFFICIAL].
- **Agent prompt body text** — the long-form English instructions in an agent file carry over verbatim; only the frontmatter encoding changes.
- **Slash command body text** — same: the prose is portable; what changes is *how* it gets invoked (Claude `/plugin list`, OpenCode `prompts/`, Codex generated prompt files).

## Per-Target Adaptation — Concrete Code

ECC's portability rests on three concrete adaptation patterns.

### Pattern A: Sync Script (Codex)

`scripts/sync-ecc-to-codex.sh` ([sync-ecc-to-codex.sh](https://github.com/affaan-m/everything-claude-code/blob/main/scripts/sync-ecc-to-codex.sh)) [OFFICIAL] is a 400-line bash script that: (1) backs up `~/.codex/config.toml` and `AGENTS.md` to `$CODEX_HOME/backups/ecc-$STAMP/`; (2) **marker-based merges** ECC AGENTS.md content into the user's via `<!-- BEGIN ECC -->` / `<!-- END ECC -->` so user content survives re-sync; (3) generates Codex prompt files from `commands/*.md` (strips frontmatter, prepends `# ECC Command Prompt: /<name>`); (4) copies `.codex/agents/*.toml` to `$CODEX_HOME/agents/`; (5) installs global git hooks; (6) merges MCP servers into `~/.codex/config.toml` via `scripts/codex/merge-mcp-config.js` (Node `@iarna/toml` round-trip, add-only, never overwrites); (7) runs a post-sync regression check; (8) supports `--dry-run` and `--update-mcp`. The script `require_path`s every input at the top and fails fast — production-grade plumbing.

### Pattern B: Adapter Wrapper (Cursor)

`.cursor/hooks/adapter.js` ([adapter.js](https://github.com/affaan-m/everything-claude-code/blob/main/.cursor/hooks/adapter.js)) [OFFICIAL] is the cleanest DRY-business-logic example. A `transformToClaude(cursorInput)` function maps Cursor's stdin payload (`cursorInput.command`, `.path`, `.output`, `.transcript_path`) into a Claude-shaped `{tool_input, tool_output, transcript_path, _cursor}` object, then `runExistingHook(scriptName, stdinData)` `execFileSync`s `node scripts/hooks/<name>` with the transformed JSON on stdin (15s timeout). Each Cursor event (`after-file-edit.js`, `before-shell-execution.js`, `before-mcp-execution.js`, etc.) is a thin file that calls `transformToClaude()` then `runExistingHook('post-edit-format.js', payload)`. The 40 canonical hook scripts under `scripts/hooks/` never need to know they are being driven by Cursor. An `ECC_HOOK_PROFILE` (`minimal|standard|strict`) and `ECC_DISABLED_HOOKS` env-var layer adds runtime control.

### Pattern C: Frontmatter Rewriter (Gemini)

`scripts/gemini-adapt-agents.js` ([gemini-adapt-agents.js](https://github.com/affaan-m/everything-claude-code/blob/main/scripts/gemini-adapt-agents.js)) [OFFICIAL] mechanically transforms agent frontmatter at install time:

```javascript
const TOOL_NAME_MAP = new Map([
  ['Read', 'read_file'], ['Write', 'write_file'], ['Edit', 'replace'],
  ['Bash', 'run_shell_command'], ['Grep', 'grep_search'], ['Glob', 'glob'],
  ['WebSearch', 'google_web_search'], ['WebFetch', 'web_fetch'],
]);
```

It walks `.gemini/agents/*.md`, parses the frontmatter, rewrites `tools: [...]` array entries through the map, strips unsupported `color:` keys, and writes back. MCP tool names (`mcp__server__tool`) are normalized into snake-case via a regex pipeline. This is the lightest-weight adaptation pattern — zero runtime cost, just a one-shot transform during install.

## Portability Analysis (Per Asset Class)

| Asset class | To OpenCode | To Codex CLI | To Cursor | To Gemini CLI | To Goose / ForgeCode |
|---|---|---|---|---|---|
| AGENTS.md | Reused via `instructions[]` | Reused via `persistent_instructions` | Read by Cursor | Reused | Reused (Goose), unsupported (ForgeCode) |
| Skill `SKILL.md` body | Verbatim ingest into `instructions[]` | Wrapped into prompt files | Copied to `.cursor/skills/` | Read as token surface | No integration — would need new adapter |
| Agent frontmatter | Rewritten as JSON `agent` map entries pointing to `prompts/agents/*.txt` | Rewritten as TOML `[agents.*]` files (3 only ship today) | Adapter-driven through hooks | Rewritten by `gemini-adapt-agents.js` | None |
| Slash commands | 34 ported into `.opencode/commands/` | Generated as prompt files | Copied to `.cursor/` | Not supported | None |
| Hooks (event surface) | TS plugin `ECCHooksPlugin` — totally different events | No hook concept; uses `notify` + `persistent_instructions` | JS adapter to Cursor's 14 events | No hook concept | Not supported |
| Hook business logic | Reused via OpenCode plugin or via wrapper-call patterns | Mostly N/A | Reused verbatim via adapter | N/A | N/A |
| MCP servers | Through `.opencode/plugins/` plugin SDK | TOML merge into `~/.codex/config.toml` | Wrapped through Cursor MCP hooks | Catalog reference only | Goose has its own MCP impl; ForgeCode uses MCP |
| Plugin manifest | Per-tool TS module + `package.json` | `.codex-plugin/plugin.json` (different schema) | Cursor `hooks.json` only | None | Each agent defines its own |
| Rules | Subset bundled into `.opencode/instructions/` | Manual `cp -R` to `~/.codex/` | Copied to `.cursor/rules/` | Read inline via `GEMINI.md` | Not supported |

**Single-source-of-truth candidates** (worth templating once, fanning out via codegen at install time):

- All skill `SKILL.md` markdown bodies.
- AGENTS.md (root) and any `CLAUDE.md`-style overlays (treat the latter as a generated artifact).
- Agent prompt **bodies** (frontmatter is per-target, body is shared).
- MCP server logical declarations (canonical JSON in `mcp-configs/`, mechanically converted to JSON/TOML at install time).
- Slash command bodies (frontmatter and invocation glue are per-target).

**Per-target rewrite required** (no single-source feasible):

- Plugin/marketplace manifests (each harness defines its own schema).
- Hook event manifests and per-event wrappers (event vocabularies do not align).
- Frontmatter encodings for agents and skills.
- Per-target install state files (each adapter manages its own state).

**What ECC genuinely does NOT support today:**

- **Goose** — no `.goose/` directory, no skills referencing Goose, no installer adapter. Conspicuous given Goose is one of three founding contributions to the Linux Foundation's Agentic AI Foundation alongside MCP and AGENTS.md [OFFICIAL].
- **Aider** — listed as supported by the agents.md project; ECC ships nothing Aider-specific.
- **Cline / ForgeCode** — no integration.
- **Antigravity / Grok** — README says "supported with manual fallback" but the install manifests do reference an `antigravity` target in module `targets[]` arrays (e.g., `agents-core` includes `antigravity`), so partial support exists at install-plan level even if no `.antigravity/` directory ships.

## What Would Have to Change for ECC to Ship Standalone to OpenCode or Codex

ECC already ships *to* OpenCode and Codex; the question is what additional work would publish ECC as a first-class plugin in those tools' own marketplaces.

**OpenCode standalone:** the `.opencode/` directory is already shaped (`package.json`, `index.ts` exporting `ECCHooksPlugin`, `plugins/`, `tools/`, `prompts/`, `commands/`, `opencode.json`); `scripts/build-opencode.js` exists. Remaining lift: (a) extract `.opencode/` into its own publishable package boundary, (b) bundle skill markdown as data, (c) reconcile metadata counts against actual `prompts/agents/` content, (d) fold rules into `instructions[]` (OpenCode has no native rule format), (e) repackage the canonical Node hook scripts under `scripts/hooks/` as in-process functions inside `ECCHooksPlugin` rather than `execFileSync` calls.

**Codex standalone:** `.codex-plugin/plugin.json` exists with `interface`, `defaultPrompt`, `mcpServers`. Three `.codex/agents/*.toml` files exist. Remaining lift: scale from 3 to ~48 agents by writing a generator that converts `agents/*.md` (Anthropic frontmatter) to `.codex/agents/*.toml` (Codex schema), analogous to `gemini-adapt-agents.js`. Slash commands are already handled by `sync-ecc-to-codex.sh`'s `generate_prompt_file()`. Hooks are unsolved (Codex has no hook concept; `persistent_instructions` is the substitute).

**Cursor standalone:** Cursor has no extensions marketplace for hook bundles. The current `.cursor/hooks.json` + `adapter.js` pattern *is* the deployment mechanism; users install via `./install.sh --target cursor --profile core`.

Pattern across all three: ECC is already structured to ship to each as a distinct deliverable; the lift is finishing the per-target build outputs (curated TS plugin for OpenCode, TOML-agent generator for Codex) and resolving the platform mismatches (rules in OpenCode, hooks in Codex).

## What Momentum Can Steal Without Copying ECC's Surface Area

1. **Manifest-driven selective install (`profiles → modules → paths × targets`).** Replace any monolithic install with three small JSONs: profiles, modules, components. Each module declares paths, targets, dependencies, kind, cost, stability. The installer is a Node script that resolves a profile to a module set, runs deps closure, then dispatches to per-target adapters.
2. **Shared-source / dot-prefix-target layout.** Keep canonical `skills/`, `agents/`, `commands/`, `rules/`, `hooks/`, `mcp-configs/` at the top level. Use `.claude/`, `.codex/`, `.opencode/`, `.cursor/`, `.gemini/` as per-target staging that the installer either copies or merges. Every per-target file is either symlinked to or generated from a canonical source.
3. **The three adaptation patterns** (sync script for Codex, adapter wrapper for Cursor, frontmatter rewriter for Gemini) — each addresses a different category of mismatch. Pick the cheapest per asset class.
4. **Marker-based AGENTS.md merge** with `<!-- BEGIN ECC -->` / `<!-- END ECC -->` so user content survives re-installs. This is the single non-obvious ergonomic in ECC's installer.
5. **`installStatePath` + `repair.js` + `doctor.js`** — long-running installs go out of sync; bake recovery commands into the installer from day one rather than discovering the need later.
6. **Skip the ecc2 Rust rewrite as a model.** It is in-tree, builds, but is "alpha, not GA" per the `v1.10.0` CHANGELOG — adoption energy is on the existing JS installer, not the Rust prototype [OFFICIAL].

## Sources

- [ECC repo root](https://github.com/affaan-m/everything-claude-code) — top-level layout, README, CHANGELOG, manifests
- [README.md](https://github.com/affaan-m/everything-claude-code/blob/main/README.md) — install flow, three install paths, naming/migration note, multi-model setup warnings
- [CHANGELOG.md](https://github.com/affaan-m/everything-claude-code/blob/main/CHANGELOG.md) — v1.10.0 surface refresh, ecc2 alpha status
- [.claude-plugin/plugin.json](https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/plugin.json) — canonical Claude plugin manifest
- [.claude-plugin/marketplace.json](https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/marketplace.json) — single-plugin marketplace entry
- [.codex-plugin/plugin.json](https://github.com/affaan-m/everything-claude-code/blob/main/.codex-plugin/plugin.json) — Codex marketplace manifest
- [.codex/config.toml](https://github.com/affaan-m/everything-claude-code/blob/main/.codex/config.toml) — Codex reference config with persistent_instructions, MCP servers, profiles
- [.opencode/opencode.json](https://github.com/affaan-m/everything-claude-code/blob/main/.opencode/opencode.json) — OpenCode native config with instructions[] and agent map
- [.opencode/index.ts](https://github.com/affaan-m/everything-claude-code/blob/main/.opencode/index.ts) — exported npm plugin module + metadata
- [.cursor/hooks/adapter.js](https://github.com/affaan-m/everything-claude-code/blob/main/.cursor/hooks/adapter.js) — Cursor→Claude hook payload transformer
- [hooks/hooks.json](https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json) — canonical Claude hook settings with PluginRoot probe
- [scripts/hooks/](https://github.com/affaan-m/everything-claude-code/tree/main/scripts/hooks) — 40 hook scripts directory
- [install.sh](https://github.com/affaan-m/everything-claude-code/blob/main/install.sh) — POSIX shell wrapper around install-apply.js
- [scripts/install-apply.js](https://github.com/affaan-m/everything-claude-code/blob/main/scripts/install-apply.js) — Node installer entrypoint with --profile, --modules, --target, --dry-run, --json
- [scripts/sync-ecc-to-codex.sh](https://github.com/affaan-m/everything-claude-code/blob/main/scripts/sync-ecc-to-codex.sh) — Codex sync with marker-based AGENTS.md merge and MCP TOML merger
- [scripts/gemini-adapt-agents.js](https://github.com/affaan-m/everything-claude-code/blob/main/scripts/gemini-adapt-agents.js) — frontmatter rewriter (Read→read_file, Bash→run_shell_command, etc.)
- [manifests/install-profiles.json](https://github.com/affaan-m/everything-claude-code/blob/main/manifests/install-profiles.json) — 5 profiles → module sets
- [manifests/install-modules.json](https://github.com/affaan-m/everything-claude-code/blob/main/manifests/install-modules.json) — 20 modules with paths/targets/dependencies
- [agents/code-reviewer.md](https://github.com/affaan-m/everything-claude-code/blob/main/agents/code-reviewer.md) — sample agent (Anthropic frontmatter)
- [skills/tdd-workflow/SKILL.md](https://github.com/affaan-m/everything-claude-code/blob/main/skills/tdd-workflow/SKILL.md) — sample skill body
- [GitHub repo metadata API](https://api.github.com/repos/affaan-m/everything-claude-code) — verified live counts on 2026-04-26
- [GitHub releases](https://github.com/affaan-m/everything-claude-code/releases) — 12 releases v1.0.0–v1.10.0
- [agents.md spec site](https://agents.md) — AGENTS.md format documentation
- [Linux Foundation AAIF press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) — MCP + AGENTS.md + goose donation
