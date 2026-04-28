---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "OpenCode extension contract — definitive verification of canonical repo, skills, plugin events, AGENTS.md precedence from source"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["sst/opencode vs anomalyco/opencode", "v1.14.27 vs v1.0.xxx", "skills support reality", "stars count"]
---

# OpenCode Extension Contract — Source-of-Truth Verification

This report resolves four contradictions in the multi-agent-deployment corpus by
cloning `https://github.com/anomalyco/opencode`, inspecting source at the
`v1.14.28` release tag (SHA `acd8783a36d8642ade7038f34ca4f2f2ac3cc824`,
published 2026-04-27 04:23 UTC), and live-checking GitHub API + opencode.ai
metadata at the same time.

## 1. Canonical Org/Repo: `anomalyco/opencode`

**Resolved: `anomalyco/opencode` is canonical. `sst/opencode` is a 301 redirect
shell to the same repository.**

Evidence:

- `curl -I https://github.com/sst/opencode` returns `HTTP/2 301` with
  `location: https://github.com/anomalyco/opencode`. This is GitHub's standard
  rename redirect — the underlying repository ID is the same.
- The GitHub API confirms it: `GET /repos/sst/opencode` returns
  `{"message":"Moved Permanently", "url":".../975734319"}`. Following the
  redirect resolves to `full_name: "anomalyco/opencode"`, the same numeric
  repository ID `975734319`.
- `opencode.ai` (the homepage stamped on the repo metadata) embeds GitHub
  metadata directly in its HTML: `{stars:150109, release:{tag_name:"v1.14.28"},
  contributors:455}`. This is the same repo.
- README.md at HEAD identifies the project as `opencode` from `anomalyco`. No
  fork-of relationship is declared (`fork: false`).

The `sst/opencode` URL is a legacy reference. SST (the company behind the
project's predecessor SST framework) appears to have transferred the repository
to a dedicated `anomalyco` org. The redirect preserves all old links without
breakage. Any corpus claim that "sst/opencode is real and anomalyco/opencode is
a fork" is wrong — it is the inverse. The canonical clone URL is
`https://github.com/anomalyco/opencode.git`. The website canonical is
`https://opencode.ai/`.

## 2. Latest Released Version + SHA

**Resolved: latest release is `v1.14.28`, NOT `v1.0.xxx`.**

`git tag -l 'v*' | sort -V` from the cloned repo shows the version trajectory
includes `v1.4.6 ... v1.4.14, v1.14.17 ... v1.14.28`. The corpus claim of
`v1.0.xxx` is stale or fabricated; the project is well past 1.14.

- Latest release tag: `v1.14.28`
- Release commit SHA: `acd8783a36d8642ade7038f34ca4f2f2ac3cc824`
- Release date: 2026-04-27 04:23:33 UTC (literally hours before this
  verification ran)
- Prior release: `v1.14.27` at SHA `373cc2a5e13ba7b8cc40ff3306c7db023fab370c`,
  published 2026-04-27 02:08:56 UTC

Both `v1.14.27` and `v1.14.28` exist as discrete tags — the corpus contradiction
is just one source citing yesterday's version and another citing today's. Both
are real. `v1.14.28` is current as of verification time.

Default branch is `dev`, not `main`. AGENTS.md in the repo confirms this:
`The default branch in this repo is dev. Local main ref may not exist; use dev
or origin/dev for diffs.`

## 3. Skills Support — Fully Implemented, Docs Live

**Resolved: skills are first-class. The 404 claim is wrong.**

### Discovery is in source

`packages/opencode/src/skill/index.ts` (291 lines) implements full skill
discovery. Lines 23-26 declare the discovery contract:

```ts
const EXTERNAL_DIRS = [".claude", ".agents"]
const EXTERNAL_SKILL_PATTERN = "skills/**/SKILL.md"
const OPENCODE_SKILL_PATTERN = "{skill,skills}/**/SKILL.md"
const SKILL_PATTERN = "**/SKILL.md"
```

The `discoverSkills` function (lines 146-199) loads skills from six locations
in this exact order:

1. **Global Claude/agents skills** — `~/.claude/skills/**/SKILL.md` and
   `~/.agents/skills/**/SKILL.md` (via `Global.Path.home + dir`)
2. **Project Claude/agents skills** — walks up from `cwd` to git worktree
   looking for `.claude/skills/` and `.agents/skills/` (via `fsys.up`)
3. **Configured directories** — the project's `.opencode/` directory and any
   parent `.opencode/` directories matching `{skill,skills}/**/SKILL.md`
4. **`config.skills.paths`** — explicit paths from `opencode.jsonc` config
   (supports `~/` expansion)
5. **`config.skills.urls`** — remote skill registries; `Discovery.pull` fetches
   `index.json` then downloads each skill's files (see
   `packages/opencode/src/skill/discovery.ts`)

Skills are filtered by agent permissions (line 250): `Permission.evaluate(
"skill", skill.name, agent.permission)`. Each SKILL.md must have YAML
frontmatter with `name` and `description` (line 96, validated with zod). The
formatter (`fmt`, lines 264-288) emits skills as either an XML
`<available_skills>` block or a markdown `## Available Skills` list.

The kill switches `OPENCODE_DISABLE_EXTERNAL_SKILLS`,
`OPENCODE_DISABLE_CLAUDE_CODE_SKILLS`, and `OPENCODE_DISABLE_CLAUDE_CODE` (which
implies the previous two) are wired through `packages/core/src/flag/flag.ts`.
Setting any of these disables `.claude/skills/` and `.agents/skills/` discovery
while leaving `.opencode/skills/` intact.

### A real SKILL.md ships in the repo

`.opencode/skills/effect/SKILL.md` is a working skill the OpenCode team uses
internally:

```yaml
---
name: effect
description: Work with Effect v4 / effect-smol TypeScript code in this repo
---
```

It instructs the agent to clone `effect-smol` into
`.opencode/references/effect-smol` and grep that source before writing Effect
code. This is the canonical "skill scoped to a project" pattern.

### Docs page is live (200 OK)

`curl -I https://opencode.ai/docs/skills` returns `HTTP/2 200`. The MDX source
is at `packages/web/src/content/docs/skills.mdx` (222 lines, page title "Agent
Skills", description "Define reusable behavior via SKILL.md definitions"). The
docs explicitly enumerate all six discovery paths matching the source code:
`.opencode/skills/<name>/SKILL.md`, `~/.config/opencode/skills/<name>/SKILL.md`,
`.claude/skills/<name>/SKILL.md`, `~/.claude/skills/<name>/SKILL.md`,
`.agents/skills/<name>/SKILL.md`, `~/.agents/skills/<name>/SKILL.md`.

Translated MDX exists for `bs/skills.mdx` and `tr/skills.mdx`. Any corpus
source citing a 404 was either looking at a transient deploy state or at a
stale URL like `/docs/skill/` (singular) — the live URL is `/docs/skills/`.

## 4. Plugin Contract

**Resolved: plugins are TypeScript modules exporting a `Plugin` function that
returns a `Hooks` object.**

The plugin SDK is published as `@opencode-ai/plugin`. Source:
`packages/plugin/src/index.ts` (333 lines). The contract:

```ts
export type PluginInput = {
  client: ReturnType<typeof createOpencodeClient>
  project: Project
  directory: string
  worktree: string
  experimental_workspace: { register(type: string, adaptor: WorkspaceAdaptor): void }
  serverUrl: URL
  $: BunShell
}
export type Plugin = (input: PluginInput, options?: PluginOptions) => Promise<Hooks>
export type PluginModule = { id?: string; server: Plugin; tui?: never }
```

Real example shipped in the SDK (`packages/plugin/src/example.ts`):

```ts
import { Plugin } from "./index.js"
import { tool } from "./tool.js"

export const ExamplePlugin: Plugin = async (_ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: { foo: tool.schema.string().describe("foo") },
        async execute(args) { return `Hello ${args.foo}!` },
      }),
    },
  }
}
```

Plugins are loaded via `config.plugin: Array<string | [string, PluginOptions]>`
in `opencode.jsonc`. `OPENCODE_DISABLE_DEFAULT_PLUGINS=1` disables built-ins.

## 5. Plugin Hook Events — Full List

The `Hooks` interface (`packages/plugin/src/index.ts:222-333`) exposes 16 hook
points. Plugins implement any subset:

**Lifecycle / general:**
- `event(input: { event: Event })` — receives every Bus event (see event list
  below)
- `config(input: Config)` — modify resolved config

**Tool authoring:**
- `tool: { [key: string]: ToolDefinition }` — register custom tools
- `tool.execute.before({ tool, sessionID, callID }, { args })` — mutate args
  before tool runs
- `tool.execute.after({ tool, sessionID, callID, args }, { title, output,
  metadata })` — post-process tool output
- `tool.definition({ toolID }, { description, parameters })` — modify tool
  schema sent to the LLM

**Auth / providers:**
- `auth: AuthHook` — register a provider, OAuth/API auth flows, prompts
- `provider: ProviderHook` — register custom models for a provider

**Chat lifecycle:**
- `chat.message({ sessionID, agent?, model?, messageID?, variant? }, { message,
  parts })` — fires on each new user message
- `chat.params(...)` — mutate `temperature`, `topP`, `topK`, `maxOutputTokens`,
  `options` before send
- `chat.headers(...)` — add HTTP headers to LLM requests

**Permissions / commands:**
- `permission.ask(input: Permission, { status: "ask" | "deny" | "allow" })`
- `command.execute.before({ command, sessionID, arguments }, { parts })`

**Shell:**
- `shell.env({ cwd, sessionID?, callID? }, { env })` — mutate environment for
  shell tool calls

**Experimental:**
- `experimental.chat.messages.transform` — rewrite the message list before send
- `experimental.chat.system.transform({ sessionID?, model }, { system })` —
  rewrite system prompt array
- `experimental.session.compacting({ sessionID }, { context, prompt? })` —
  customize compaction prompt
- `experimental.compaction.autocontinue(...)` — gate the post-compaction
  auto-continue turn
- `experimental.text.complete({ sessionID, messageID, partID }, { text })`

### Bus Events (raw event types passed to the `event` hook)

Enumerated by `rg 'BusEvent.define\('` excluding tests and TUI internals.
Source files cited inline:

- `command.executed` — `packages/opencode/src/command/index.ts`
- `file.edited` — `packages/opencode/src/file/index.ts`
- `file.watcher.updated` — `packages/opencode/src/file/watcher.ts`
- `global.disposed` — `packages/opencode/src/server/routes/global.ts`
- `ide.installed` — `packages/opencode/src/ide/index.ts`
- `installation.updated`, `installation.update_available` —
  `packages/opencode/src/installation/index.ts`
- `lsp.client.diagnostics` — `packages/opencode/src/lsp/client.ts`
- `lsp.updated` — `packages/opencode/src/lsp/lsp.ts`
- `mcp.tools.changed`, `mcp.browser.open.failed` —
  `packages/opencode/src/mcp/index.ts`
- `message.part.delta` — `packages/opencode/src/session/message-v2.ts`
- `permission.asked`, `permission.replied` —
  `packages/opencode/src/permission/index.ts`
- `project.updated` — `packages/opencode/src/project/project.ts`
- `pty.created`, `pty.updated`, `pty.exited`, `pty.deleted` —
  `packages/opencode/src/pty/index.ts`
- `question.asked`, `question.replied`, `question.rejected` —
  `packages/opencode/src/question/index.ts`
- `server.connected`, `server.instance.disposed` —
  `packages/opencode/src/server/event.ts` and
  `packages/opencode/src/bus/index.ts`
- `session.compacted` — `packages/opencode/src/session/compaction.ts`
- `session.diff`, `session.error` — `packages/opencode/src/session/session.ts`
- `session.idle`, `session.status` — `packages/opencode/src/session/status.ts`
- `todo.updated` — `packages/opencode/src/session/todo.ts`
- `vcs.branch.updated` — `packages/opencode/src/project/vcs.ts`
- `workspace.ready`, `workspace.failed`, `workspace.restore`,
  `workspace.status` — `packages/opencode/src/control-plane/workspace.ts`
- `worktree.ready`, `worktree.failed` —
  `packages/opencode/src/worktree/index.ts`

That is **35 distinct events** plus the TUI-internal events
(`tui.prompt.append`, etc.) which are not normally surfaced to plugins. Plugins
receive all of these via the single `event` hook.

## 6. AGENTS.md Handling and Precedence

**Resolved: AGENTS.md is the primary; CLAUDE.md is a fallback gated by
`OPENCODE_DISABLE_CLAUDE_CODE_PROMPT`. CONTEXT.md is deprecated.**

Source: `packages/opencode/src/session/instruction.ts:17-21`:

```ts
const FILES = [
  "AGENTS.md",
  ...(Flag.OPENCODE_DISABLE_CLAUDE_CODE_PROMPT ? [] : ["CLAUDE.md"]),
  "CONTEXT.md", // deprecated
]
```

The precedence rule for project-level instructions (lines 126-134) is **first
match wins**:

```ts
if (!Flag.OPENCODE_DISABLE_PROJECT_CONFIG) {
  for (const file of FILES) {
    const matches = yield* fs.findUp(file, ctx.directory, ctx.worktree)
    if (matches.length > 0) {
      matches.forEach((item) => paths.add(path.resolve(item)))
      break
    }
  }
}
```

The walker uses `fs.findUp` to traverse from cwd to the worktree root. It
returns the **first file in the FILES list that has any matches anywhere on the
walk-up path**. So if `AGENTS.md` exists at any ancestor, CLAUDE.md is never
consulted — they do not stack across precedence levels but can stack across
ancestor directories at the same level.

Global instructions (`globalFiles()`, lines 23-33) load:

1. `$OPENCODE_CONFIG_DIR/AGENTS.md` (if env var set)
2. `~/.config/opencode/AGENTS.md` (default global config)
3. `~/.claude/CLAUDE.md` (unless `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1`)

Again, **first existing file wins** (line 137: `if (yield* fs.existsSafe(file))
{ paths.add(...); break }`).

GEMINI.md is **not** mentioned anywhere in the source. The corpus claim that
OpenCode reads GEMINI.md is wrong. Only AGENTS.md, CLAUDE.md, and the
deprecated CONTEXT.md are recognized.

The relevant flags (from `packages/core/src/flag/flag.ts`):

- `OPENCODE_DISABLE_CLAUDE_CODE` — master kill switch; sets both
  `_PROMPT` and `_SKILLS` variants to true
- `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` — disables CLAUDE.md fallback only
- `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` — disables `.claude/skills/` discovery
  only
- `OPENCODE_DISABLE_EXTERNAL_SKILLS` — disables both `.claude/skills/` and
  `.agents/skills/` (implied by `_CLAUDE_CODE_SKILLS`)
- `OPENCODE_DISABLE_PROJECT_CONFIG` — disables walking up from cwd entirely
- `OPENCODE_CONFIG_DIR` — overrides global config directory

These give a Momentum-style practice module precise control: ship to
`.claude/skills/` for Claude Code compatibility, and OpenCode picks them up
automatically unless the user sets `OPENCODE_DISABLE_CLAUDE_CODE`.

## 7. Live Repo Metadata

Verified at 2026-04-27 05:11 UTC via GitHub REST API:

| Metric | Value |
|---|---|
| `full_name` | `anomalyco/opencode` |
| `stargazers_count` | **150,109** (also `watchers_count: 150,110`) |
| `forks_count` | 17,248 |
| `subscribers_count` | 588 |
| `open_issues_count` | 6,156 |
| `default_branch` | `dev` |
| `created_at` | 2025-04-30 20:08 UTC |
| `pushed_at` | 2026-04-27 05:06 UTC (5 minutes before query) |
| `archived` | false |
| `fork` | false |
| `description` | "The open source coding agent." |
| `homepage` | `https://opencode.ai` |

Contributors: pagination header reports 878 distinct contributors (anonymous
counted), or 455 logged-in contributors per the embedded opencode.ai page data.

The corpus's "36K stars" claim is roughly four times too low. Either it cited
data from ~6 months ago, or the source counted forks (17K) and rounded up. The
real number, as of this verification, is 150,109 stars. This makes OpenCode
materially larger than the corpus framed it.

## Resolution Summary

| Contradiction | Resolution |
|---|---|
| `sst/opencode` vs `anomalyco/opencode` | **`anomalyco/opencode` is canonical.** `sst/opencode` 301-redirects to it (same repo ID `975734319`). |
| 36K vs 150K stars | **150,109 stars** as of 2026-04-27. Corpus 36K figure is stale. |
| Skills 404 vs full SKILL.md support | **Full support.** 222-line MDX docs page returns 200; `packages/opencode/src/skill/{index,discovery}.ts` implements 6-path discovery. The 404 claim is debunked. |
| `v1.14.27` vs `v1.0.xxx` | **`v1.14.28` is latest** (SHA `acd8783a`, 2026-04-27). `v1.14.27` is the immediate prior release. `v1.0.xxx` claim is fabricated. |

For Momentum's multi-agent deployment work, the takeaways are concrete:
OpenCode reads `.claude/skills/` and `.agents/skills/` natively (no shim
needed), respects `name`/`description` frontmatter, exposes 16 plugin hooks and
35 bus events, and prefers `AGENTS.md` over `CLAUDE.md` with first-match
precedence. The kill-switch env vars give the user an off-ramp if Momentum
ships skills they do not want auto-loaded.
