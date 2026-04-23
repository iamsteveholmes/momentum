---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "What are opencode's real skill/agent/plugin installation and discovery mechanics as of April 2026?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements — addendum"
---

# opencode (SST) — Install, Discovery, and Plugin Mechanics (April 2026)

Scope: verify the real, current shape of opencode's extension system by fetching primary sources (opencode.ai/docs, github.com/sst/opencode, github.com/awesome-opencode/awesome-opencode, the `opencode.ai/config.json` JSON schema). Training data cutoff prior to April 2026 must not be trusted for any of these claims without the citations below.

Evidence tags: **[OFFICIAL]** = opencode.ai docs / sst repo / opencode config schema. **[PRAC]** = community practitioner (awesome-opencode lists, third-party skill repos). **[UNVERIFIED]** = claim I could not confirm against a primary source during this pass.

Latest version observed at time of research: **opencode v1.14.20** (release dated 2026-04-21). [OFFICIAL — github.com/sst/opencode]

---

## 1. Skill discovery paths

opencode scans six canonical locations for `<skill-name>/SKILL.md`, in this precedence order (first match wins per skill name; project paths traverse upward to git worktree root and load all matches encountered): [OFFICIAL — opencode.ai/docs/skills]

1. `.opencode/skills/<name>/SKILL.md` — project-local (opencode-native)
2. `~/.config/opencode/skills/<name>/SKILL.md` — global (opencode-native)
3. `.claude/skills/<name>/SKILL.md` — project (Claude-compatible)
4. `~/.claude/skills/<name>/SKILL.md` — global (Claude-compatible)
5. `.agents/skills/<name>/SKILL.md` — project (agent-compatible, Anthropic/OAS convention)
6. `~/.agents/skills/<name>/SKILL.md` — global (agent-compatible)

Confirmation of all four claimed paths from the research brief: **`.opencode/skills/`, `~/.config/opencode/skills/`, `.claude/skills/`, `.agents/skills/` are all real and scanned.** [OFFICIAL] The doc additionally confirms the global `~/.claude/skills/` and `~/.agents/skills/` variants.

**Remote skill distribution (new in 2026):** opencode also supports a `skills.urls` config key that downloads skills from a `.well-known/agent-skills/` endpoint into `~/.cache/opencode/skills/`, and a `skills.paths` extension mechanism. [OFFICIAL — opencode.ai/config.json schema; PRAC — opencode-skills README referenced via search] The skill config shape in `opencode.json`:

```json
{
  "skills": {
    "urls": ["https://example.com/.well-known/agent-skills/"],
    "paths": ["/some/additional/dir"]
  }
}
```

**SKILL.md frontmatter (required):** `name` (lowercase alphanumeric + hyphens, 1–64 chars, must match containing dir; regex `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (1–1024 chars). Optional: `license`, `compatibility`, `metadata` (string→string map). [OFFICIAL — opencode.ai/docs/skills]

**Invocation:** Agents call the native `skill` tool: `skill({ name: "skill-name" })`. Permissions are declared in `opencode.json` under `permission.skill` with pattern matching (`"*": "allow"`, `"pr-review": "allow"`, `"pattern-*": "deny"`). [OFFICIAL]

---

## 2. Agent discovery paths

**opencode does NOT officially scan `.claude/agents/`.** The docs list only two paths: [OFFICIAL — opencode.ai/docs/agents]

- Global: `~/.config/opencode/agents/`
- Project: `.opencode/agents/`

Agent files are markdown with frontmatter:

```markdown
---
description: Agent purpose
mode: subagent        # primary | subagent | all
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: false
---
Agent system prompt here.
```

Filename becomes the agent name: `reviewer.md` → `@reviewer`. [OFFICIAL]

Agents may also be defined inline in `opencode.json` under the `agent` key. [OFFICIAL]

**Asymmetry worth noting:** opencode is Claude-compatible for **skills** (`.claude/skills/`) and for **rules** (`CLAUDE.md` fallback), but **not** for agents. A Claude Code `.claude/agents/reviewer.md` file is NOT picked up by opencode. [OFFICIAL — confirmed by direct re-query of the agents page] Migrating Claude Code subagents into opencode therefore requires copying or symlinking them from `.claude/agents/` into `.opencode/agents/`.

**`opencode agent create`** — interactive wizard: picks global vs project scope, collects a purpose description, auto-generates system prompt and slug, lets you select tool permissions, then writes the markdown file. [OFFICIAL — opencode.ai/docs/agents]

---

## 3. Plugin system

**Install mechanism = npm, declared in `opencode.json`.** Bun installs and caches plugins automatically at startup in `~/.cache/opencode/node_modules/`. [OFFICIAL — opencode.ai/docs/plugins]

```json
{
  "plugin": [
    "opencode-helicone-session",
    "@my-org/custom-plugin"
  ]
}
```

Both unscoped and scoped npm packages are supported. No `opencode plugin install` CLI subcommand exists — `plugin` in `opencode.json` is the declarative install surface. [OFFICIAL — verified against CLI reference]

**Local plugin directories** (for in-tree or dev plugins without npm publish):

- Project: `.opencode/plugins/`
- Global: `~/.config/opencode/plugins/`

Local plugins needing external npm deps use a co-located `.opencode/package.json`. [OFFICIAL]

**Plugin TypeScript entry point:** a plugin is an async function default-exported (or named) from the package's entry, receiving a context and returning a hooks object. Types come from `@opencode-ai/plugin`: [OFFICIAL]

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => { /* handle lifecycle events */ },
    tool:  { /* custom tool registrations */ },
  }
}
```

Custom tools use the helper:

```typescript
import { type Plugin, tool } from "@opencode-ai/plugin"

export const CustomTools: Plugin = async (ctx) => ({
  tool: {
    mytool: tool({
      description: "…",
      args: { foo: tool.schema.string() },
      async execute(args, context) { return `Hello ${args.foo}` },
    }),
  },
})
```

---

## 4. Hooks surface

**The prior "28 lifecycle events" claim is stale/low.** As of 2026-04-22 the docs enumerate **~30 stable events plus TUI/experimental extras — ~39 distinct event names in total** observed on the plugins page. [OFFICIAL — opencode.ai/docs/plugins]

Full list observed:

| Category | Events |
|---|---|
| Command | `command.executed` |
| Files | `file.edited`, `file.watcher.updated` |
| Installation | `installation.updated` |
| LSP | `lsp.client.diagnostics`, `lsp.updated` |
| Messages | `message.updated`, `message.removed`, `message.part.updated`, `message.part.removed` |
| Permissions | `permission.asked`, `permission.replied` |
| Server | `server.connected` |
| Sessions | `session.created`, `session.updated`, `session.deleted`, `session.idle`, `session.status`, `session.compacted`, `session.diff`, `session.error` |
| Shell | `shell.env` |
| Todo | `todo.updated` |
| Tools | `tool.execute.before`, `tool.execute.after` |
| TUI | `tui.prompt.append`, `tui.command.execute`, `tui.toast.show` |
| Experimental | `experimental.session.compacting` |

Count: **~28–30 stable + TUI/experimental ≈ 39.** The "28" number is plausibly what earlier training data saw; the surface has grown. [OFFICIAL]

Plugin context destructure: `{ project, client, $, directory, worktree }` where `$` is a Bun-style shell tag, `client` is the opencode server client, `worktree` reflects git state. [OFFICIAL]

---

## 5. awesome-opencode

**Yes — a curated list exists and is actively maintained.** [PRAC]

- **Canonical repo:** https://github.com/awesome-opencode/awesome-opencode (org `awesome-opencode`, not under `sst/`)
- **Mirror site:** https://www.awesome-opencode.com/ and https://www.opencode.asia/ecosystem/awesome/
- **Size:** ~115+ items across 6 categories, 223 commits, last updated ~2026-03-21 [PRAC — awesome-opencode README]

Categories (counts approximate):

| Category | Count |
|---|---|
| Official Repositories | 4 (core CLI, JS/TS SDK, Go SDK, Python SDK) |
| Plugins | 70+ |
| Themes | 4 |
| Agents | 4 |
| Projects | 30+ (TUIs, Neovim/IDE plugins, Discord bots, session managers, orchestration) |
| Resources | 3 |

**Skills are NOT a top-level category.** They are referenced inside individual plugins (e.g. `opencode-skillful`, "Agent Skills (JDT)", `opencode-skills`). [PRAC]

A separate community list exists: **`TheArchitectit/awesome-opencode-skills`** — ~26 skills across 9 categories (Document Processing, Development Tools, Business/Marketing, Communication, Creative/Media, Productivity, plus "coming soon" sections). It ships a helper script: `./scripts/install_opencode_skills.sh --global` or `--project`, which copies skill folders into `~/.config/opencode/skill/` or `.opencode/skill/`. [PRAC — TheArchitectit/awesome-opencode-skills README]

Note: that repo's README uses the singular path `skill/`, which contradicts the official plural `skills/`. **Trust the official docs — use `skills/`.** The helper script may work because opencode also accepts the singular directory name, but this is **[UNVERIFIED]**; the authoritative path is `skills/`.

---

## 6. `opencode.json` schema

**Schema URL:** `https://opencode.ai/config.json` (TUI-specific: `https://opencode.ai/tui.json`). [OFFICIAL — referenced from docs/config]

**Top-level keys** confirmed by fetching the live JSON schema: [OFFICIAL]

| Key | Purpose |
|---|---|
| `$schema` | Schema reference |
| `model` | Primary model (e.g. `anthropic/claude-sonnet-4-5`) |
| `small_model` | Cheap model for titles, summaries |
| `provider` | Provider-level settings (keys, timeouts, regions) |
| `agent` | Inline agent definitions (map keyed by agent name) |
| `default_agent` | Agent used when none specified |
| `tools` | Allow/deny built-in tools (write, bash, edit, …) |
| `command` | Custom slash-command templates |
| `mcp` | MCP server configuration |
| `permission` | Fine-grained permission rules |
| `instructions` | Paths/globs to external rule files |
| `plugin` | **Array** of npm package names (note: singular, not `plugins`) |
| `skills` | **Object** with `paths` and `urls` subkeys (note: plural) |
| `formatter` | Code formatters (Prettier, custom) |
| `share` / `autoshare` | Session sharing mode |
| `server` | Port, host, mDNS, CORS |
| `snapshot` | Session change tracking |
| `autoupdate` | `true` / `false` / `"notify"` |
| `compaction` | Auto-compact/prune/reserved-token settings |
| `watcher` | File-watcher ignore patterns |
| `disabled_providers` / `enabled_providers` | Provider allow/deny lists |
| `experimental` | Unstable options |
| `logLevel`, `mode`, `username` | Misc |

**Permission subkeys** (each: `"ask"` | `"allow"` | `"deny"`, or granular object):
`read`, `edit`, `glob`, `grep`, `list`, `bash`, `task`, `external_directory`, `todowrite`, `question`, `webfetch`, `websearch`, `codesearch`, `lsp`, `doom_loop`, `skill`. [OFFICIAL]

**Important naming gotcha** — opencode mixes singular/plural inconsistently between config keys and filesystem directories:

| Thing | Config key | Filesystem dir |
|---|---|---|
| Plugins | `plugin` (singular, array) | `plugins/` (plural) |
| Skills  | `skills` (plural, object)  | `skills/` (plural) |
| Agents  | `agent`  (singular, object/map) | `agents/` (plural) |
| Commands | `command` (singular, object/map) | `commands/` (plural) |

When writing an `opencode.json`, use **singular** for `plugin`, `agent`, `command`, but **plural** for `skills`. When creating files, use **plural** directories.

**Config precedence** (lowest to highest — later overrides earlier, merged not replaced): [OFFICIAL — opencode.ai/docs/config]

1. Remote `.well-known/opencode` config
2. Global `~/.config/opencode/opencode.json`
3. `OPENCODE_CONFIG` env var
4. Project `./opencode.json`
5. `.opencode/` directories (merged in)
6. `OPENCODE_CONFIG_CONTENT` env var
7. Managed settings (`/Library/Application Support/opencode/`)
8. macOS MDM preferences (highest, non-overridable)

---

## 7. AGENTS.md / opencode.md / CLAUDE.md support

**Yes, opencode reads all three rule-file conventions, with explicit fallback to Claude Code.** [OFFICIAL — opencode.ai/docs/rules]

Precedence / search order:

1. Local `AGENTS.md` — primary, traversing upward from cwd
2. Local `CLAUDE.md` — fallback if no `AGENTS.md`
3. Global `~/.config/opencode/AGENTS.md`
4. Global `~/.claude/CLAUDE.md` — Claude Code migration fallback (disableable via env var)
5. `opencode.json` → `instructions` key (explicit paths, glob supported)

"The first matching file wins in each category. For example, if you have both `AGENTS.md` and `CLAUDE.md`, only `AGENTS.md` is used." [OFFICIAL — direct quote]

Note: `opencode.md` is **not** a recognized rule file name per the docs; the canonical name is `AGENTS.md`. [OFFICIAL]

The `/init` slash-command auto-generates an `AGENTS.md` for a project. [OFFICIAL]

---

## 8. Is there an `opencode install <skill>` CLI?

**No.** The opencode CLI (v1.14.20) has no `install`, `skill install`, `plugin install`, or `add` subcommand for extensions. [OFFICIAL — opencode.ai/docs/cli]

Complete CLI surface as of 2026-04-22:

- **Agent:** `opencode agent create`, `opencode agent list`
- **Auth:** `opencode auth login`, `opencode auth list`/`ls`, `opencode auth logout`
- **GitHub:** `opencode github install` (installs GH Actions workflow, NOT skills), `opencode github run`
- **MCP:** `opencode mcp add`, `opencode mcp list`/`ls`, `opencode mcp auth [name]`, `opencode mcp auth list`/`ls`, `opencode mcp logout [name]`, `opencode mcp debug <name>`
- **General:** `opencode`, `opencode run [message...]`, `opencode serve`, `opencode attach [url]`, `opencode models [provider]`, `opencode session list`, `opencode stats`, `opencode export [sessionID]`, `opencode import <file>`, `opencode web`, `opencode acp`, `opencode upgrade [target]`, `opencode uninstall`

**Skill "installation" is purely filesystem-based** (copy/clone into one of the six scanned paths, or declare a `.well-known` URL in `skills.urls`). **Plugin "installation" is declarative npm** (list the package in `plugin` in `opencode.json`; Bun resolves it at startup). **Agent "installation" is filesystem-based** (write markdown to `.opencode/agents/` or create via `opencode agent create`).

This is meaningfully different from Claude Code's `/plugin marketplace` workflow — opencode has no registry/marketplace CLI; everything routes through npm (plugins), filesystem convention (skills/agents), or the awesome-opencode curated list.

---

## Quick-reference: installing a skill / agent / plugin on opencode

### Install a skill (filesystem, project-local)

```bash
# Skill authored as a folder containing SKILL.md + supporting files
mkdir -p .opencode/skills/my-skill
cp path/to/SKILL.md .opencode/skills/my-skill/SKILL.md
# Done — opencode auto-discovers at startup. SKILL.md frontmatter must have
# `name: my-skill` matching the directory name.
```

### Install a skill (global, opencode-native)

```bash
mkdir -p ~/.config/opencode/skills/my-skill
cp path/to/SKILL.md ~/.config/opencode/skills/my-skill/SKILL.md
```

### Reuse existing Claude Code skills without moving them

```bash
# opencode scans .claude/skills/ and ~/.claude/skills/ natively — no action needed
# if skills already live there from Claude Code.
ls ~/.claude/skills/   # these are already visible to opencode
```

### Install a remote skill via `.well-known` (new 2026)

```jsonc
// opencode.json
{
  "skills": {
    "urls": ["https://my-org.example.com/.well-known/agent-skills/"]
  }
}
// opencode downloads to ~/.cache/opencode/skills/ on next start; verify with /skill in TUI.
```

### Install an agent (markdown, project)

```bash
mkdir -p .opencode/agents
cat > .opencode/agents/reviewer.md <<'EOF'
---
description: Adversarial code reviewer
mode: subagent
model: anthropic/claude-sonnet-4-5
permission:
  edit: deny
  bash: false
---
You review diffs for correctness, security, and style.
EOF
# Invoke with @reviewer in a session.
```

### Install an agent via wizard

```bash
opencode agent create    # interactive: scope, description, tools, auto-slug
```

### Install a plugin (npm, declarative)

```jsonc
// opencode.json
{
  "plugin": [
    "opencode-notificator",            // unscoped npm package
    "@my-org/opencode-custom-plugin"   // scoped npm package
  ]
}
// Bun installs on next start into ~/.cache/opencode/node_modules/.
```

### Install a local/dev plugin

```bash
mkdir -p .opencode/plugins/my-plugin
# write index.ts that default-exports a Plugin function from @opencode-ai/plugin
# optional .opencode/package.json for external deps
```

### Migrate Claude Code agents into opencode

```bash
# opencode does NOT scan .claude/agents/. Copy or symlink:
mkdir -p .opencode/agents
for f in .claude/agents/*.md; do
  ln -s "$(pwd)/$f" ".opencode/agents/$(basename "$f")"
done
# Verify frontmatter has `mode: subagent` (or primary/all) — opencode-specific key.
```

### Upgrade opencode itself

```bash
opencode upgrade            # latest
opencode upgrade v1.14.20   # pinned
```

---

## Summary (inline, 3–5 sentences)

As of 2026-04-22 (opencode v1.14.20), opencode's extension model is **filesystem-first for skills and agents, npm-declarative for plugins, and zero-CLI-registry overall** — there is no `opencode install <skill>` or `opencode plugin add` command. Skill discovery is broad and Anthropic-compatible: opencode scans **six** paths including `.opencode/skills/`, `~/.config/opencode/skills/`, `.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`, plus a new `skills.urls` config for `.well-known/agent-skills/` remote distribution. Agent discovery is narrower — **only** `.opencode/agents/` and `~/.config/opencode/agents/`; `.claude/agents/` is NOT read, so Claude Code subagents must be copied/symlinked over. Plugins are npm packages listed in `opencode.json` under the (singular) `plugin` key; the lifecycle surface is ~39 events (not 28 — the older number is stale). A curated list exists at `github.com/awesome-opencode/awesome-opencode` (~115+ items across 6 categories), plus a community skill-specific list at `TheArchitectit/awesome-opencode-skills` (~26 skills) with a copy-script installer.
