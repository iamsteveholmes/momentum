---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Cross-agent installation architectures (case studies beyond BMAD/ECC) — concrete projects that ship to multiple AI coding agents: file layouts, install scripts, format adapters, version pinning, update mechanism."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# Cross-Agent Installation Architectures — Case Studies (April 2026)

## Inline Summary

Across the projects surveyed, three repeatable architectural patterns dominate as of April 2026: (1) **a registry of "Integration"/"Agent" objects that each declare a target directory + filename + format**, with a single-source-of-truth Markdown corpus translated at install time (Spec Kit, ai-rulez, rulebook-ai, rules.so); (2) **a "universal store" pattern** in which `SKILL.md` is the canonical unit, copied or symlinked into per-agent `skills/` directories detected at runtime (Vercel `skills`, OpenSkills, SkillKit, Skillz, Skills-Supply); and (3) **an in-place guideline-injection pattern** where the tool writes/refreshes a managed `<!-- MARKER START/END -->` block inside whatever instruction file each agent reads (Backlog.md, partly OpenSkills `sync`). Version pinning is overwhelmingly handled by tool-level semver releases plus per-package git refs in a lockfile (`agents.toml`, `skills-lock.json`, `.sync-state.json`), not by content-level versioning.

---

## Survey Notes

EXCLUSIONS: BMAD-method and `affaan-m/everything-claude-code` are covered by sibling agents and not re-covered here. All starred counts and dates verified via `gh` CLI on 2026-04-26.

---

## github/spec-kit — registry-of-integrations + skills layout

**Repo / activity** [OFFICIAL]: `github/spec-kit`, ~91K stars, last release `v0.8.1` on 2026-04-24, last push 2026-04-24 (very active; multiple commits same day).

**Target agents supported** [OFFICIAL]: 28 in the registry as of 2026-04-26, enumerated in `src/specify_cli/integrations/__init__.py::_register_builtins` — Agy, Amp, Auggie, Bob, Claude, Codebuddy, Codex, Copilot, Cursor-Agent, Forge, Gemini, Generic, Goose, Iflow, Junie, Kilocode, Kimi, Kiro-CLI, OpenCode, Pi, Qodercli, Qwen, Roo, Shai, Tabnine, Trae, Vibe, Windsurf.

**File layout (key paths)** [OFFICIAL]:

```
spec-kit/
├── src/specify_cli/
│   ├── agents.py            # CommandRegistrar — translates one Markdown command file into N agent-specific files
│   ├── integrations/
│   │   ├── __init__.py      # INTEGRATION_REGISTRY + _register_builtins()
│   │   ├── base.py          # IntegrationBase / MarkdownIntegration / TomlIntegration / SkillsIntegration
│   │   ├── manifest.py
│   │   ├── claude/__init__.py   # ClaudeIntegration  -> .claude/skills/*/SKILL.md
│   │   ├── codex/__init__.py
│   │   ├── cursor_agent/, opencode/, gemini/, ... (28 dirs)
│   └── workflows/, presets.py, extensions.py
├── templates/
│   ├── commands/            # CANONICAL Markdown command templates (specify, plan, tasks, implement, ...)
│   ├── spec-template.md, plan-template.md, tasks-template.md, constitution-template.md
└── pyproject.toml           # ships `specify` CLI (uvx-installable)
```

**Single source of truth** [OFFICIAL]: `templates/commands/*.md` — Markdown with YAML frontmatter (description, scripts, etc.). Each integration class translates these to its native shape.

**Compilation step** [OFFICIAL]: `CommandRegistrar` in `src/specify_cli/agents.py` parses the frontmatter, runs `rewrite_project_relative_paths` (mapping `../../scripts/` → `.specify/scripts/`, etc.), then renders Markdown or TOML output per integration. Each integration declares its destination via class attrs:

```python
class ClaudeIntegration(SkillsIntegration):
    key = "claude"
    config = {"folder": ".claude/", "commands_subdir": "skills"}
    registrar_config = {"dir": ".claude/skills",
                        "format": "markdown",
                        "args": "$ARGUMENTS",
                        "extension": "/SKILL.md"}
    context_file = "CLAUDE.md"
```

`SkillsIntegration` further wraps each command into a `speckit-<name>/SKILL.md` folder (Anthropic-style). `TomlIntegration` (used by Gemini, Tabnine) re-emits TOML. Argument placeholders differ per agent (`$ARGUMENTS`, `{{args}}`, etc.) — enforced by `registrar_config["args"]`.

**Install script** [OFFICIAL]: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`, then `specify init <project> --integration claude` (or `--integration cursor`, etc.). The CLI is a Python entry point, not a bash one-liner. The `--integration` flag is the deprecated-but-still-active `--ai` flag (per commit `171b65a` 2026-04-24, the project is renaming).

**Version pinning / updates** [OFFICIAL]: semver git tags (`v0.8.1`); `specify update` re-templates from the tag pinned in the user's project. Templates ship inside the `specify_cli` Python package, so `uv tool upgrade` is the upgrade path.

**Portable vs. agent-specific** [OFFICIAL]: portable = the slash-command body, the spec/plan/tasks artifacts, the `.specify/` scripts. Agent-specific = filename + frontmatter shape + argument placeholder + invocation separator (`speckit.plan` vs `/speckit-plan`). The `_HOOK_COMMAND_NOTE` in `claude/__init__.py` shows that some agents' renderers inject extra prose to handle quirks ("replace dots with hyphens").

---

## ai-rulez (Goldziher/ai-rulez) — single YAML compiled by templates per agent

**Repo / activity** [OFFICIAL]: ~111 stars, latest release `v4.0.6` on 2026-04-25, last push 2026-04-26. Go binary distributed via npm (`npx ai-rulez`) and PyPI.

**Target agents supported** [OFFICIAL]: 19+ (Claude, Cursor, Copilot, Windsurf, Cline, Roo, Kilo, Codex, Gemini, AMP, Continue, …). Two distinct registries: one for **rule output** (per-agent file conventions) under `internal/templates/`, and one for **runtime invocation** at `internal/agents/agents.go`, which only lists 6 agents that have a CLI binary to shell out to.

**File layout** [OFFICIAL]:

```
ai-rulez/
├── ai-rulez.yml                # CANONICAL — user authors this once
├── cmd/                        # Cobra subcommands (init, generate, validate, etc.)
├── internal/
│   ├── agents/agents.go        # runtime invocation (claude/codex/cursor-agent/cn/gemini/amp)
│   ├── generator/              # per-agent file emission
│   ├── parser/, scanner/, importer/
│   ├── templates/              # Go text/template per-agent output shapes
│   └── builtins/               # built-in rule packs
└── skills/                     # ai-rulez-the-tool's own skills
```

**Single source of truth** [OFFICIAL]: a single `ai-rulez.yml` that the user writes; it composes "rules", "context", "skills", "agents", "commands" into one declarative tree. `ai-rulez generate` walks targets and emits CLAUDE.md, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, etc.

**Compilation step** [OFFICIAL]: Go templates in `internal/templates/` plus per-agent generators in `internal/generator/`. The generator both writes files and (uniquely in this survey) **invokes the agent's local CLI** at generate-time to ask it to validate or rewrite — `agents.go` literally `exec.LookPath("cursor-agent")` and `exec.CommandContext(ctx, "claude", "--print", "--permission-mode", "bypassPermissions", prompt)`. So "compilation" can include a live agent loop.

**Install script** [OFFICIAL]: `npx ai-rulez@latest init && npx ai-rulez@latest generate`. Also installable via `pip install ai-rulez` or via Goreleaser binary releases (`.goreleaser.yaml` is in repo root).

**Version pinning / updates** [OFFICIAL]: GitHub releases (`v4.0.6`); the `ai-rulez.yml` doesn't pin rule packs by version per se but `community_packs` references upstream slugs. Updates are `npx ai-rulez@latest` rerun.

**Portable vs. agent-specific** [OFFICIAL]: portable = rule prose; agent-specific = frontmatter (`.mdc` for Cursor needs a specific YAML shape with `globs`/`alwaysApply`), filename, single-file vs many-file emission. ai-rulez treats rules vs skills vs commands as separate concept buckets, each with its own per-agent target table.

---

## botingw/rulebook-ai — declarative AssistantSpec table

**Repo / activity** [OFFICIAL]: ~594 stars, last push 2025-10-03 (older — flag: 6+ months stale). Python tool. Worth surveying for its very clean separation.

**Target agents supported** [OFFICIAL]: 10 in `src/rulebook_ai/assistants.py` — Cursor, Windsurf, Cline, Roo, Kilo, Warp, Copilot, Claude Code, Codex CLI, Gemini CLI.

**Single source of truth + compilation** [OFFICIAL]: One frozen dataclass per assistant declares `rule_path`, `is_multi_file`, `filename` (single-file case), `file_extension` (multi-file case), `clean_path`, `has_modes`, `supports_subdirectories`. Generator code reads this table and decides whether to concatenate to a single file (`CLAUDE.md`, `AGENTS.md`, `WARP.md`) or fan-out to a directory (`.cursor/rules/*.mdc`, `.windsurf/rules/*.md`). This is the **smallest** "registry" abstraction in the survey — one ~20-line dataclass per agent.

**File layout** [OFFICIAL]:

```
rulebook-ai/
├── src/rulebook_ai/
│   ├── assistants.py           # SUPPORTED_ASSISTANTS list + ASSISTANT_MAP
│   ├── core.py, cli.py, packs/, community/
├── memory/, prompts/, rule_sets/
└── pyproject.toml              # console_scripts entry "rulebook"
```

**Install / updates** [OFFICIAL]: `pip install rulebook-ai`; `rulebook install --assistants cursor,claude-code,roo`. Updates are tool re-installs; rule pack versions tracked via git.

**Portable vs. agent-specific** [OFFICIAL]: portable = rule prose in `rule_sets/`; agent-specific = file path + extension + concatenation vs split. `clean_path` is a thoughtful detail — it's the path the tool nukes on `clean`, scoped narrowly so it doesn't blow away unrelated user files (e.g. Copilot's `.github/copilot-instructions.md` rather than `.github`).

---

## continuedev/rules ("rules.so") — per-format renderers, registry-published

**Repo / activity** [OFFICIAL]: 53 stars, last release `v1.2.3` on 2025-06-25 (flag: ~10 months since last release), repo last push 2026-03-05. Go-based CLI.

**Target agents supported** [OFFICIAL]: continue, cursor (`.cursor/rules/*.mdc`), windsurf (`.windsurf/rules/*.md`), claude (`CLAUDE.md`), copilot (`.github/instructions/*.instructions.md`), codex (`AGENT.md`), cline (`.clinerules/*.md`), cody (`.sourcegraph/*.rule.md`), amp (`AGENT.md`).

**File layout** [OFFICIAL]:

```
continuedev/rules/
├── main.go, bin.js, build.js
├── cmd/                         # Cobra commands: init, add, publish, render
├── internal/                    # per-format renderers, registry client
├── rules.json                   # local manifest pinning installed rules
└── docs-main/, spec/, scripts/
```

**Single source of truth** [PRAC]: rules authored as Markdown + YAML frontmatter in a private repo or registry; `rules publish` uploads them to the rules.so registry. Consumers run `rules add <slug>` and the renderer writes per-target files.

**Install / updates** [PRAC]: `npm install -g @continuedev/rules` (binary wrapped), then `rules init` → `rules add owner/slug --target cursor claude windsurf`. Versions pinned in `rules.json` per project.

**Portable vs. agent-specific** [OFFICIAL]: same prose; Cursor needs `.mdc` with `globs/alwaysApply`; Copilot needs `.instructions.md` glob-frontmatter; Continue's own format is `.continue/rules/*.md`.

---

## MrLesk/Backlog.md — guideline injection between markers, MCP for runtime

**Repo / activity** [OFFICIAL]: ~5.4K stars, latest release `v1.44.0` on 2026-03-21, last push 2026-04-26. TypeScript / Bun. Distinct architecture: Backlog.md doesn't ship skills/commands — it ships **instruction blocks** that teach an agent how to use its own CLI.

**Target agents supported** [OFFICIAL]: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`, `README.md`. Plus an MCP server path for any MCP-capable agent.

**File layout** [OFFICIAL]:

```
Backlog.md/
├── src/agent-instructions.ts            # writes/refreshes guideline blocks
├── src/guidelines/
│   ├── agent-guidelines.md              # canonical AGENTS.md text
│   ├── project-manager-backlog.md
│   ├── index.ts
│   └── mcp/                             # MCP-flavored variants
├── src/mcp/                             # MCP server impl
└── package.json (`bin: backlog`)
```

**Single source of truth** [OFFICIAL]: `src/guidelines/agent-guidelines.md` (and the few sibling MD files) — embedded in the bundle. `src/agent-instructions.ts` exports per-target constants (`CLAUDE_GUIDELINES`, `GEMINI_GUIDELINES`, `COPILOT_GUIDELINES`).

**Compilation step** [OFFICIAL]: not really compilation — **idempotent injection**. `addAgentInstructions()` reads the existing target file (or creates it), strips any prior block delimited by `<!-- BACKLOG.MD GUIDELINES START -->` / `<!-- BACKLOG.MD GUIDELINES END -->` (special-cased to `# === BACKLOG.MD GUIDELINES START ===` for `.cursorrules` since that file doesn't support HTML comments), then re-appends the current version. This is the cleanest implementation of the "managed-block" pattern in the survey.

**Install** [OFFICIAL]: `bun i -g backlog.md` / `npm i -g backlog.md` / `brew install backlog-md`. `backlog init` runs an interactive wizard that prompts the user which target files to write and whether to register an MCP server with Claude Code, Codex, Gemini CLI, Cursor, or Kiro.

**Version pinning / updates** [OFFICIAL]: tool-level semver. The injected block is rewritten on every `backlog init` so updates flow through tool upgrades; the MCP path means runtime behavior tracks the installed CLI version, not the on-disk markdown.

**Portable vs. agent-specific** [OFFICIAL]: the prose is essentially the same; the marker syntax is the only divergence (HTML comment vs `#`-comment for `.cursorrules`). MCP integration replaces the markdown for agents that support it.

---

## vercel-labs/skills — single store, per-agent symlinks, lockfile

**Repo / activity** [OFFICIAL]: ~16K stars, latest release `v1.5.1` on 2026-04-17, last push 2026-04-22. Distributed by `npx skills` (no global install required).

**Target agents supported** [OFFICIAL]: 43+ enumerated in `src/agents.ts`. Snippet:

```ts
'claude-code': {skillsDir: '.claude/skills',     globalSkillsDir: join(claudeHome, 'skills')}
codex:         {skillsDir: '.agents/skills',     globalSkillsDir: join(codexHome, 'skills')}
cursor:        {skillsDir: '.agents/skills',     globalSkillsDir: join(home,'.cursor/skills')}
amp:           {skillsDir: '.agents/skills',     globalSkillsDir: join(configHome,'agents/skills')}
antigravity:   {skillsDir: '.agents/skills',     globalSkillsDir: join(home,'.gemini/antigravity/skills')}
augment:       {skillsDir: '.augment/skills'}
continue:      {skillsDir: '.continue/skills'}
windsurf, cline, codebuddy, command-code, cortex, crush, deepagents, droid, ...
```

The crucial design: **most agents share `.agents/skills/`** (the proposed cross-tool universal directory); a handful (Claude Code, Augment, Continue, Codebuddy, Cortex, Crush) keep their own. Each agent has a `detectInstalled()` predicate that probes for `~/.claude`, `~/.gemini/antigravity`, `~/.codex`, etc., to decide if it should be auto-targeted.

**File layout** [OFFICIAL]:

```
vercel-labs/skills/
├── src/agents.ts              # AGENT REGISTRY (the heart)
├── src/install.ts, installer.ts, find.ts, list.ts
├── src/local-lock.ts          # ./skills-lock.json writer
├── src/plugin-manifest.ts     # Anthropic-compat plugin manifest
├── src/providers/             # GitHub, GitLab, well-known endpoints
├── skills/                    # this repo's own skill content
└── package.json (`bin: skills`)
```

**Single source of truth** [OFFICIAL]: `SKILL.md` with YAML frontmatter (`name`, `description`) inside any directory the user installs from (`anthropics/skills`, `obra/superpowers`, etc.). The skill content is the canonical artifact; the CLI does not transform body content, only places.

**Compilation step** [OFFICIAL]: minimal. For non-universal agents, the CLI **symlinks** from a canonical store to the per-agent skills dir — content lives once on disk. For universal `.agents/skills/`-using agents, files land directly there.

**Install** [OFFICIAL]: `npx skills add anthropics/skills@official` or `npx skills add github:owner/repo`. Two scopes: global (`~/.agents/.skill-lock.json`) and project (`./skills-lock.json`).

**Version pinning / updates** [OFFICIAL]: `skills-lock.json` records source URL, ref (commit SHA), and resolved metadata per skill. `npx skills update` re-resolves refs. Skill content versioning is delegated to the source repo.

**Portable vs. agent-specific** [OFFICIAL]: SKILL.md format is universal; the only adapter is the destination path. There is no per-agent re-rendering. This is the cleanest "store + symlink" architecture.

---

## numman-ali/openskills — npm package with sync-AGENTS.md command

**Repo / activity** [OFFICIAL]: ~9.9K stars, latest release `v1.5.0` on 2026-01-17, last push 2026-01-18 (flag: 3+ months without commits — not stale, but the field has moved fast since).

**Target agents supported** [OFFICIAL]: Claude Code, Cursor, Windsurf, Aider, Codex, "anything that reads AGENTS.md" — fewer than vercel-labs/skills. Default install path is `./.claude/skills`; with `--universal` flag, `./.agent/skills` (note: singular `.agent`, distinct from vercel's `.agents`).

**File layout** [OFFICIAL]:

```
openskills/
├── src/cli.ts                # commander.js entry: list/install/read/update/sync/manage/remove
├── src/commands/             # one file per command
├── examples/, tests/
└── package.json              # ships `openskills` bin
```

**Compilation / install** [OFFICIAL]: `npx openskills install <gh-source>` clones, finds SKILL.md folders, copies to target dir. The notable command is **`openskills sync`** — it walks installed skills and rewrites `AGENTS.md` (or any output path) to enumerate them, so agents that only read AGENTS.md (rather than scan `skills/`) still know what's available. This is the second example in the survey of an injection-style step.

**Version pinning / updates** [PRAC]: source-pinned by git ref; `openskills update` re-pulls. No per-skill semver.

**Portable vs. agent-specific** [OFFICIAL]: SKILL.md portable; the agent-specific bit is which directory you install to, controlled by flags rather than auto-detected.

---

## 803/skills-supply (`sk`) — agents.toml manifest + cross-agent reconciliation

**Repo / activity** [OFFICIAL]: 31 stars (smaller; included for the spec), latest release `sk@0.2.4` on 2026-01-12, last push 2026-01-17. TypeScript monorepo. Most rigorous "Result-type, no-throw" code style of any tool surveyed.

**Target agents supported** [OFFICIAL]: Claude Code, Codex, OpenCode, with a typed `ResolvedAgent` registry for adding more.

**File layout** [OFFICIAL]:

```
skills-supply/
├── packages/
│   ├── core/                  # core types (Result, ValidatedDeclaration, AgentId, MANIFEST_FILENAME="agents.toml")
│   ├── sk/
│   │   ├── cli.ts
│   │   ├── agents/            # install.ts, reconcile.ts, registry.ts, state.ts
│   │   ├── manifest/          # parse.ts, transform.ts, write.ts, fs.ts, discover.ts
│   │   ├── sync/              # sync.ts (entry), marketplace.ts, repo.ts, validate.ts
│   │   ├── packages/          # extract.ts, fetch.ts, resolve.ts, types.ts
│   │   └── io/, env.ts, credentials/
│   └── api/, database/, web/, discovery/
├── packages/SPEC.md
└── AGENTS.md (the project's own)
```

**Single source of truth** [OFFICIAL]: per-project `agents.toml` (constant `MANIFEST_FILENAME`). It declares `[package]`, dependencies, and `[agents]` enable/disable. `sk sync` walks up the tree to find it (npm-style).

**Compilation step** [OFFICIAL]: `runSync()` in `packages/sk/sync/sync.ts` resolves manifest packages, fetches their contents (GitHub/Git/local) into a temp dir, extracts skills, then for each enabled agent calls `planAgentInstall` and `applyAgentInstall`. `reconcileAgentSkills` removes anything previously installed but no longer in the manifest — the **"npm prune" pattern**. Per-agent state is persisted via `buildAgentState`/`writeAgentState`, giving the tool true bidirectional sync awareness rather than blind copying.

**Install / updates** [OFFICIAL]: `sk pkg add gh obra/superpowers`, `sk sync`. Updates are `sk sync` after changing the manifest or after upstream changes.

**Version pinning / updates** [OFFICIAL]: `agents.toml` declarations carry git refs; `sk` resolves these into a typed `ValidatedDeclaration`. Reconciliation tracks per-agent state files so removals are explicit.

**Portable vs. agent-specific** [OFFICIAL]: SKILL.md is portable. Agent-specific = path + state file location + reconciliation rules.

---

## rohitg00/skillkit — three-tier monorepo with mesh/memory layers

**Repo / activity** [OFFICIAL]: 890 stars, latest release `v1.24.0` on 2026-04-21, last push 2026-04-21 (very active). Most ambitious scope of any tool here.

**Target agents supported** [OFFICIAL]: 44+ — claims "ship to 46 agents at once"; supports Claude Code, Cursor, Codex, Windsurf, Copilot, Gemini CLI, etc.

**File layout** [OFFICIAL]:

```
skillkit/
├── src/                       # primary source
├── packages/
│   ├── agents/, api/, cli/, core/, extension/
│   ├── mcp/, mcp-memory/, memory/, mesh/, messaging/
│   ├── resources/, tui/
├── apps/, clients/, registry/, marketplace/
├── schemas/                   # JSON schemas for skill manifest
├── skills/, skills-lock.json
└── tsup.config.ts, turbo.json (Turbo monorepo with tsup builds)
```

**Single source of truth** [OFFICIAL]: SKILL.md + JSON-schema-validated manifest in `schemas/`.

**Compilation step** [PRAC]: `@skillkit/agents` package contains the 44+ adapters; translation between formats happens here. The `@skillkit/mesh` package adds **P2P multi-machine distribution** — unique among the surveyed tools — so a skill installed on one workstation can propagate across a team's machines. Memory layer (`@skillkit/memory`) persists session learnings with semantic embeddings.

**Install** [OFFICIAL]: `npm i -g skillkit` or `npx skillkit`. CLI commands include install / translate / share / `skillkit memory compress` / `skillkit memory search`.

**Version pinning / updates** [OFFICIAL]: `skills-lock.json` (same pattern as Vercel's `skills`). Tool releases on a fast cadence (1.24.0 in April 2026).

**Portable vs. agent-specific** [PRAC]: cross-agent translation is the marquee feature — claims to convert between Cursor `.mdc`, Continue `.md`, Anthropic `SKILL.md`, etc. Adapter logic lives in `packages/agents/`.

---

## jkitchin/skillz — small Python CLI with YAML platform table

**Repo / activity** [OFFICIAL]: 28 stars, no releases yet, last push 2026-04-27 (active small project; included to show the smallest viable architecture).

**Target agents supported** [OFFICIAL]: Claude, OpenCode, Codex, Gemini — declared in `example-config.yaml`:

```yaml
default_platform: claude
platforms:
  claude:   {skills_dir: ~/.claude/skills,         commands_dir: ~/.claude/commands}
  opencode: {skills_dir: ~/.config/opencode/skills, commands_dir: ~/.config/opencode/command}
  codex:    {skills_dir: ~/.codex/skills,           commands_dir: ~/.codex/commands}
  gemini:   {skills_dir: ~/.config/gemini/skills,   commands_dir: ~/.config/gemini/commands}
```

**File layout** [OFFICIAL]:

```
skillz/
├── cli/                      # Python entry: __main__, commands/, config.py, validator.py
├── skills/, agents/, commands/, hooks/, templates/
├── example-config.yaml
└── pyproject.toml
```

**Compilation step** [OFFICIAL]: copy + validate. `cli/validator.py` enforces SKILL.md frontmatter rules. No per-agent body rewriting — the YAML platform table just maps to a destination path. Closest in spirit to vercel-labs/skills, but config-file-driven rather than runtime-detected.

**Install** [OFFICIAL]: `uv pip install -e .` (or `pip`). Configure via `~/.config/skillz/config.yaml`. Run `python -m cli.main install <skill-name> --platform codex`.

**Version pinning / updates** [PRAC]: not formalized — git-clone-based.

---

## numman-ali/n-skills — curated marketplace synced from upstreams

**Repo / activity** [OFFICIAL]: 976 stars, latest release `v1.3.2` on 2026-01-17, last push 2026-03-22. Distinct role: this is a **marketplace repo**, not a tool. It packages skills authored elsewhere and republishes them under one umbrella.

**File layout** [OFFICIAL]:

```
n-skills/
├── .claude-plugin/marketplace.json    # Anthropic plugin manifest
├── sources.yaml                       # SOURCES (per-skill upstream pointers)
├── scripts/sync-external.mjs          # sync engine
├── skills/automation/, skills/tools/, skills/workflow/
└── package.json
```

**Single source of truth** [OFFICIAL]: `sources.yaml` — each entry declares `name`, `source.repo`, `source.path`, `target.path`, `author`, `license`. `native: true` marks skills maintained in-repo.

**Compilation / sync step** [OFFICIAL]: `scripts/sync-external.mjs` runs daily (GitHub Actions), clones each upstream, computes `hashDirectory()` over content, writes a `.sync-state.json` with the hash, and commits changes only if the directory hash changed. Content-level diffing rather than commit-SHA tracking — handles upstream squash-rebases gracefully.

**Install** [OFFICIAL]: as a Claude Code plugin marketplace via `.claude-plugin/marketplace.json`; or via `openskills install numman-ali/n-skills`; or `npx openskills install numman-ali/n-skills`. Designed to be agent-agnostic since the underlying skills are SKILL.md folders.

**Version pinning** [OFFICIAL]: `.sync-state.json` records hashes per skill. Marketplace consumers pin to a git SHA of n-skills itself.

**Portable vs. agent-specific** [OFFICIAL]: no agent-specific output — n-skills is purely a curation/aggregation layer.

---

## Cross-Cutting Observations

**Three architectural patterns** [UNVERIFIED synthesis]:

1. **Registry-of-integrations + per-agent renderer** — Spec Kit, ai-rulez, rulebook-ai, rules.so. Each defines a typed object per agent (path, filename, format flags). Generation walks the canonical Markdown corpus and emits N native files. Best for projects that ship slash commands or rules where each agent has subtly different frontmatter expectations.

2. **Universal SKILL.md store + per-agent path adapter** — Vercel `skills`, OpenSkills, SkillKit, Skillz, n-skills, skills-supply. Anthropic's SKILL.md is treated as a contract; the only translation needed is "where does it land". Symlinking (Vercel) and reconciliation state files (skills-supply) are sophisticated extensions. This is winning because of the Anthropic Skills standard's gravitational pull.

3. **In-place guideline injection between markers** — Backlog.md (cleanest), Continue's `<!-- markers -->` Spec Kit context-marker pattern, OpenSkills `sync`. Used when the goal is teaching the agent how to use an external tool rather than installing reusable capabilities. Idempotent rewrite is the key trick.

**Universal directory convergence** [OFFICIAL via vercel-labs/skills source]: many agents now read `.agents/skills/` (plural; vercel-labs' choice) or `.agent/skills/` (singular; openskills' `--universal` flag). Codex, Cursor, Windsurf, Cline, Amp, Antigravity all use `.agents/skills/` according to vercel-labs' `agents.ts`. Claude Code, Continue, Augment, Crush keep their own. This is a real fork in the standard.

**AGENTS.md continues to win** [PRAC]: Codex CLI, GitHub Copilot, Cursor, Windsurf, Amp, Devin all read AGENTS.md natively as of April 2026. Claude Code does not (Anthropic uses CLAUDE.md). The recommended workaround across multiple sources is `ln -s AGENTS.md CLAUDE.md`.

**Version-pinning is overwhelmingly tool-level + lockfile** [OFFICIAL]: every tool surveyed pins through tool semver releases; per-skill versioning is delegated to source git refs (`skills-lock.json`, `agents.toml`, `.sync-state.json`, `rules.json`). No tool surveyed implements true package-manager semver-range resolution per skill.

**Update mechanisms** [OFFICIAL]: range from "rerun the tool" (most) to "scheduled GitHub Actions sync" (n-skills) to "P2P mesh propagation" (SkillKit). The reconcile-and-prune approach (skills-supply, partly Vercel's lockfile) is the most production-shaped.

**Portability ceiling** [UNVERIFIED]: the body of a Markdown rule/skill is always portable. Frontmatter is always agent-specific. Argument placeholders, subdirectory mode-folders (Roo/Kilo `has_modes`), and skill-vs-rule-vs-command type distinctions are the three biggest sources of per-agent divergence.

---

## Sources

- github/spec-kit — https://github.com/github/spec-kit (verified via `gh api` 2026-04-26; latest release v0.8.1 2026-04-24) [OFFICIAL]
- spec-kit integrations dir — https://github.com/github/spec-kit/tree/main/src/specify_cli/integrations [OFFICIAL]
- spec-kit AGENTS.md — https://github.com/github/spec-kit/blob/main/AGENTS.md [OFFICIAL]
- spec-kit installation guide — https://github.github.com/spec-kit/installation.html [OFFICIAL]
- MrLesk/Backlog.md — https://github.com/MrLesk/Backlog.md (v1.44.0 2026-03-21) [OFFICIAL]
- Backlog.md agent-instructions.ts — https://github.com/MrLesk/Backlog.md/blob/main/src/agent-instructions.ts [OFFICIAL]
- Goldziher/ai-rulez — https://github.com/Goldziher/ai-rulez (v4.0.6 2026-04-25) [OFFICIAL]
- ai-rulez agents.go — https://github.com/Goldziher/ai-rulez/blob/main/internal/agents/agents.go [OFFICIAL]
- ai-rulez PyPI — https://pypi.org/project/ai-rulez/ [OFFICIAL]
- botingw/rulebook-ai — https://github.com/botingw/rulebook-ai (last push 2025-10-03; flag: 6+ months stale) [OFFICIAL]
- rulebook-ai assistants.py — https://github.com/botingw/rulebook-ai/blob/main/src/rulebook_ai/assistants.py [OFFICIAL]
- continuedev/rules — https://github.com/continuedev/rules (v1.2.3 2025-06-25; flag: 10 months) [OFFICIAL]
- rules.so docs — https://rules.so [OFFICIAL]
- vercel-labs/skills — https://github.com/vercel-labs/skills (v1.5.1 2026-04-17) [OFFICIAL]
- vercel-labs/skills agents.ts — https://github.com/vercel-labs/skills/blob/main/src/agents.ts [OFFICIAL]
- Vercel skills changelog — https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem [OFFICIAL]
- numman-ali/openskills — https://github.com/numman-ali/openskills (v1.5.0 2026-01-17) [OFFICIAL]
- 803/skills-supply — https://github.com/803/skills-supply (sk@0.2.4 2026-01-12) [OFFICIAL]
- skills-supply sync.ts — https://github.com/803/skills-supply/blob/main/packages/sk/sync/sync.ts [OFFICIAL]
- rohitg00/skillkit — https://github.com/rohitg00/skillkit (v1.24.0 2026-04-21) [OFFICIAL]
- SkillKit docs — https://www.skillkit.sh/docs/commands [OFFICIAL]
- jkitchin/skillz — https://github.com/jkitchin/skillz (last push 2026-04-27) [OFFICIAL]
- skillz example-config.yaml — https://github.com/jkitchin/skillz/blob/main/example-config.yaml [OFFICIAL]
- numman-ali/n-skills — https://github.com/numman-ali/n-skills (v1.3.2 2026-01-17) [OFFICIAL]
- n-skills sources.yaml — https://github.com/numman-ali/n-skills/blob/main/sources.yaml [OFFICIAL]
- n-skills sync-external.mjs — https://github.com/numman-ali/n-skills/blob/main/scripts/sync-external.mjs [OFFICIAL]
- AGENTS.md spec — https://agents.md/ [OFFICIAL]
- AGENTS.md guide (Augment) — https://www.augmentcode.com/guides/how-to-build-agents-md [PRAC]
- DeployHQ AGENTS.md/CLAUDE.md guide — https://www.deployhq.com/blog/ai-coding-config-files-guide [PRAC]
- OpenCode skills docs — https://opencode.ai/docs/skills/ [OFFICIAL]
- Codex Agent Skills — https://developers.openai.com/codex/skills [OFFICIAL]
- Continue rules deep-dive — https://docs.continue.dev/customize/deep-dives/rules [OFFICIAL]
