---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "Goose, ForgeCode, Gemini CLI extension contracts — definitive verification of skills/hooks/AGENTS.md/extensions from source"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["Goose skills cross-tool reads", "Goose hooks existence", "ForgeCode canonical org tailcallhq vs antinomyhq", "ForgeCode hooks", "Gemini CLI hooks v0.26+", "Gemini tool name remapping"]
---

# Verification: Goose, ForgeCode, Gemini CLI

This document resolves three corpus contradictions by reading source at named tags. Bash was unavailable in this session, so all evidence comes from raw GitHub blob URLs at the named release tags. The tag-pinned URLs are stable references — every quoted constant or schema lives at the SHA pinned in each agent section. Where source was inaccessible (e.g. line-numbered ranges in some `blob/` views), evidence falls back to the raw `raw.githubusercontent.com` mirror at the same tag.

---

## 1. Goose (block/goose)

### Version

| Field | Value |
|---|---|
| Latest release tag | `v1.32.0` |
| Release date | 2026-04-23 |
| Commit SHA | `14a8815746e3c6ffad107f4983df50fd631ec2ce` |
| Source | `[OFFICIAL-SOURCE — block/goose/releases/tag/v1.32.0]` |

### Resolution table

| Question | Corpus claim | Verified answer | Evidence |
|---|---|---|---|
| Reads `.claude/skills/`? | Yes (cross-tool) | **YES** (workspace and `~/.claude/skills`) | `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/platform_extensions/skills.rs]` |
| Reads `.codex/skills/`? | Yes | **NO** — not in skill path list | `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/platform_extensions/skills.rs]` |
| Reads `.cursor/skills/`? | Yes | **NO** — not in skill path list | `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/platform_extensions/skills.rs]` |
| Reads `.agents/skills/`? | Yes | **YES** (workspace and `~/.agents/skills`) | `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/platform_extensions/skills.rs]` |
| Has hook system? | NO | **NO** at v1.32.0; **draft PR #8842 in flight** | `[OFFICIAL-SOURCE — block/goose/pull/8842]` |
| Reads AGENTS.md? | Yes | **YES** | `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/hints/load_hints.rs]` |
| Reads `.goosehints`? | Yes | **YES** | same |
| Reads `GOOSE.md`? | (varied) | **NO** — not in hardcoded list | same |

### Skills

The skills system in Goose is implemented as a built-in **platform extension** at `crates/goose/src/agents/platform_extensions/skills.rs`. The original implementation landed via PR #5760 (merged 2025-11-24, commit `6421522acc7992cb1abf98faf996d5e5ed7d5cce`); v1.32.0 ships an expanded path list.

**Workspace-relative skill directories** (resolved against `working_dir`):
- `.goose/skills`
- `.claude/skills`
- `.agents/skills`

**Global skill directories** (resolved against `~`):
- `~/.agents/skills`
- `~/.claude/skills`
- `~/.config/agents/skills`
- `$CONFIG_DIR/skills` (XDG config dir + `/skills`)

Skill identification: each skill is a directory containing a `SKILL.md` file with YAML frontmatter (`name`, `description`). Goose registers a `load_skill` tool; the LLM activates a skill on demand by name (progressive disclosure — skill body and supporting files are not loaded until activation). Path canonicalization rejects traversal outside the resolved skill directory.

Cite: `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/platform_extensions/skills.rs]` and `[OFFICIAL-SOURCE — block/goose/pull/5760]`.

**Verdict on cross-tool reads.** The corpus claim that Goose reads `.codex/skills/` and `.cursor/skills/` is **false**. Goose reads only `.goose/skills`, `.claude/skills`, and `.agents/skills` at the workspace tier. The Claude alias is intentional (compatibility with Claude's existing skill ecosystem); the `.agents` alias is the proposed cross-tool standard (see AGENTS.md ecosystem). There is no Codex or Cursor compatibility shim.

### Hooks

**Goose v1.32.0 has no agent-lifecycle hook system.** A grep against `crates/goose/src/agents/agent.rs` returns no matches for `hook`, `Hook`, `before_tool`, `after_tool`, `pre_tool`, `post_tool`, `on_session_start`, `on_message`, `callback`, or `event_handler`. The agent loop uses direct method calls and `async/await` rather than a hook dispatcher. The `crates/goose/src/agents/` module list confirms there is no `hooks.rs`, `hook.rs`, or `hook_manager.rs`.

The matches that do appear in the repo for "hook" are:
1. **Husky / git pre-commit hooks** in `.husky/` (build-time, not agent runtime).
2. **Open work in flight**: Issue #7411 ("feat: add agent lifecycle hooks (Claude Code-compatible config)", opened 2026-02-21, status `needs_human` + `stale`) and **PR #8842** ("feat: lifecycle hooks system", draft, opened 2026-04-25, head SHA `83c0dcf`) which proposes events `before_tool_call`, `after_tool_call`, `before_reply`, `after_reply`, `on_session_start`, `on_session_end` configured via `config.yaml`.

Cite: `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/agent.rs]` and `[OFFICIAL-SOURCE — block/goose/pull/8842]`.

**Verdict.** Corpus is correct that Goose has no hooks. The corpus would be wrong if it claimed Goose will *never* have hooks — a draft system is in active development as of the v1.32.0 release window.

### Recipes (.yaml format)

Recipe parsing lives in `crates/goose/src/recipe/` with the schema struct in `mod.rs`. Top-level fields:

| Field | Type | Required |
|---|---|---|
| `version` | `String` | Optional (default `"1.0.0"`) |
| `title` | `String` | Required |
| `description` | `String` | Required |
| `instructions` | `String` | Optional* |
| `prompt` | `String` | Optional* |
| `extensions` | `Vec<ExtensionConfig>` | Optional |
| `settings` | `Settings` | Optional |
| `activities` | `Vec<String>` | Optional |
| `author` | `Author` | Optional |
| `parameters` | `Vec<RecipeParameter>` | Optional |
| `response` | `Response` | Optional |
| `sub_recipes` | `Vec<SubRecipe>` | Optional |
| `retry` | `RetryConfig` | Optional |

*Validator requires at least one of `prompt` or `instructions`. There is no `profile` field at v1.32.0 (corpus citations referencing `profile` are stale). Discovery uses `recipe.yaml`/`recipe.json` in CWD plus `~/.config/goose/recipes/` and `.goose/recipes/`, augmented by `GOOSE_RECIPE_PATH`.

Cite: `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/recipe/mod.rs]`.

### Extensions (MCP)

Extension config is an enum in `crates/goose/src/agents/extension.rs`. Variants:

- **Stdio** — `cmd`, `args`, `envs`, `env_keys`, `timeout`, `bundled`, `available_tools`
- **StreamableHttp** — `uri`, `envs`, `env_keys`, `headers`, `timeout`, `socket` (Unix domain), `bundled`, `available_tools`
- **Sse** — *deprecated*, kept for config-file backwards compat only
- **Builtin** — references compiled-in MCP servers (the `goose-mcp` crate)
- **Platform** — references entries in `PLATFORM_EXTENSIONS` registry (skills, todo, summon, etc.)
- **Frontend** — caller-provided tools surfaced to the agent
- **InlinePython** — `code`, `dependencies`, `timeout`

Discovery and load: `crates/goose/src/config/extensions.rs` reads from a config key `extensions` (constant `EXTENSIONS_CONFIG_KEY`) inside Goose's unified config (`~/.config/goose/config.yaml`). `is_extension_available` filters Platform variants against the static `PLATFORM_EXTENSIONS` registry; `resolve_extensions_for_new_session` merges recipe-supplied, override, and globally-enabled extensions.

Cite: `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/agents/extension.rs]` and `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/config/extensions.rs]`.

### AGENTS.md / .goosehints / GOOSE.md handling

`crates/goose/src/hints/load_hints.rs` defines a `CONTEXT_FILE_NAMES` config key with two hardcoded defaults: `".goosehints"` and `"AGENTS.md"`. Loading (`load_hint_files`):

1. Reads the configured filenames from the user's config dir (`Paths::in_config_dir(...)`).
2. Walks ancestors from CWD up to the git root (`.git` marker), reading any matching filename at each level.
3. `build_gitignore` walks the same range collecting `.gitignore` entries to filter the context.

There is no hardcoded path for `GOOSE.md` or `CLAUDE.md`. Tests reference `CLAUDE.md` only as a configurable filename example — it would be loaded only if the user adds it to `CONTEXT_FILE_NAMES`.

Cite: `[OFFICIAL-SOURCE — block/goose/blob/v1.32.0/crates/goose/src/hints/load_hints.rs]`.

The shipped `AGENTS.md` at the repo root contains build/test/lint commands and crate-structure rules — it is consumed by the agent itself when the user runs Goose against the Goose source tree, not a meta document about Goose's AGENTS.md handling.

---

## 2. ForgeCode (canonical org resolution)

### Canonical org

Two orgs claim the project: `tailcallhq/forgecode` and `antinomyhq/forge`. Both serve identical README content, identical star counts (~7,032), and the same default branch (`main`). The disambiguator is the **install pipeline**:

- The site `https://forgecode.dev` (referenced in README install instructions) links its socials and "GitHub Stars" badge directly to `https://github.com/tailcallhq/forgecode`.
- The README's curl install (`curl -fsSL https://forgecode.dev/cli | sh`) and Nix flake (`nix run github:tailcallhq/forgecode`) both point at `tailcallhq/forgecode`.
- The latest release tag `v2.12.9` published 2026-04-26 09:00 UTC at SHA `8a9f3410f460d1618931dcc0a4b222e65eff0f58` exists in `tailcallhq/forgecode`.

**Canonical: `github.com/tailcallhq/forgecode`.** `antinomyhq/forge` appears to be either a maintainer's parallel namespace or a legacy mirror; no install path or marketing routes through it.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/main/README.md]` and `[OFFICIAL-SOURCE — forgecode.dev]`.

### Version

| Field | Value |
|---|---|
| Latest release tag | `v2.12.9` |
| Release date | 2026-04-26 |
| Commit SHA | `8a9f3410f460d1618931dcc0a4b222e65eff0f58` |
| Default branch | `main` |
| Workspace language | Rust 93.8% |

### Resolution table

| Question | Verified answer | Evidence |
|---|---|---|
| Reads `.forge/skills/`? | **YES** — bundled skills directory ships in repo | `[OFFICIAL-SOURCE — tailcallhq/forgecode/tree/v2.12.9/.forge/skills]` |
| Reads `~/forge/skills/`? | Likely (skill registration is path-based) — not directly verified at v2.12.9 | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/skill.rs]` |
| Reads `.claude/skills/`? | **NO** evidence in source | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/skill.rs]` |
| Reads `.agents/skills/`? | **NO** evidence in source | same |
| Has hook system? | **YES** — six lifecycle events, in-process callbacks | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/hook.rs]` |
| Reads AGENTS.md? | **YES** — three precedence tiers | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_services/src/instructions.rs]` |
| Custom commands? | **YES** — markdown files in `.forge/commands/` | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/command.rs]` |
| MCP support? | **YES** — `mcpServers` map (Claude `.mcp.json` compatible) | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/mcp.rs]` |
| `permissions.yaml` schema? | **YES** — policies list, allow/deny/confirm × read/write/command/url | `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_services/src/policy.rs]` |

### Skills

`crates/forge_domain/src/skill.rs` defines:

```rust
pub struct Skill {
    pub name: String,
    pub path: Option<PathBuf>,
    pub command: String,         // prompt body
    pub description: String,
    pub resources: Vec<PathBuf>, // supporting files
}
```

The bundled `.forge/skills/` directory at v2.12.9 contains 11 skill subdirectories: `create-agent`, `create-command`, `create-github-issue`, `create-plan`, `debug-cli`, `github-pr-comments`, `post-forge-feature`, `resolve-conflicts`, `resolve-fixme`, `test-reasoning`, `write-release-notes`. Skill discovery paths are not enumerated as constants in `skill.rs` itself — the struct is path-agnostic; loaders in `forge_services` (likely `agent_registry.rs` or `discovery.rs`) inject paths at runtime. Within `forge_services/src/`, no `.rs` file is named `skills.rs`. Path discovery is therefore likely keyed on the `.forge/` directory containing both `commands/` and `skills/`.

**No evidence in source that ForgeCode reads `.claude/skills/` or `.agents/skills/`.** ForgeCode's skill format is bespoke (the `Skill` struct, not Claude's `SKILL.md` frontmatter format); cross-tool compatibility would require a shim that does not appear at v2.12.9.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/skill.rs]` and `[OFFICIAL-SOURCE — tailcallhq/forgecode/tree/v2.12.9/.forge/skills]`.

### Hooks

**ForgeCode has a real, in-process hook system at v2.12.9** — distinguishing it from Goose. `crates/forge_domain/src/hook.rs`:

```rust
pub struct Hook {
    on_start:          Box<dyn EventHandle<EventData<StartPayload>>>,
    on_end:            Box<dyn EventHandle<EventData<EndPayload>>>,
    on_request:        Box<dyn EventHandle<EventData<RequestPayload>>>,
    on_response:       Box<dyn EventHandle<EventData<ResponsePayload>>>,
    on_toolcall_start: Box<dyn EventHandle<EventData<ToolcallStartPayload>>>,
    on_toolcall_end:   Box<dyn EventHandle<EventData<ToolcallEndPayload>>>,
}
```

Six `LifecycleEvent` variants — `Start`, `End`, `Request` (LLM call), `Response`, `ToolcallStart`, `ToolcallEnd`. Payloads carry typed data (`request_count`, `ChatCompletionMessageFull`, `ToolCallFull`, `ToolResult`).

Critical distinction from Claude Code / Codex / Gemini hooks: these are **in-process Rust callbacks** registered via `EventHandle`, not external shell-command or HTTP hooks driven by config files. There is no `hooks.yaml` schema. They are an internal extension point for the runtime, not a user-facing customization surface. The tool's CLAUDE.md-style customization is `.forge/commands/` (markdown slash commands) and `permissions.yaml` (policy gating), not user-defined lifecycle hooks.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/hook.rs]`.

### AGENTS.md handling

`crates/forge_services/src/instructions.rs` searches three locations, in this order (concatenated, all loaded):

1. `environment.global_agentsmd_path()` — global user config path.
2. `git_root_path.join("AGENTS.md")` — repo root, located via `git rev-parse --show-toplevel`.
3. `environment.local_agentsmd_path()` — current working directory.

The only filename hardcoded is `AGENTS.md`. No `CLAUDE.md`, `FORGE.md`, or `.forgerc` — those are not loaded at v2.12.9.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_services/src/instructions.rs]`.

### MCP

`crates/forge_domain/src/mcp.rs` defines two server configs (camelCase JSON via serde):

```rust
McpStdioServer { command, args, env, timeout, disable }
McpHttpServer  { url, headers, timeout, disable, oauth }
```

The file's doc comment: *"Follows the design specifications of Claude's `.mcp.json`"*. Top-level config key is `mcpServers` — directly compatible with Claude Code's project `.mcp.json` schema, plus `oauth` extension for HTTP servers.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/mcp.rs]`.

### Custom commands

`crates/forge_domain/src/command.rs`:

```rust
pub struct Command {
    pub name: String,
    pub description: String,
    pub prompt: Option<String>,
}
```

Doc comment: *"Commands are discovered from `.md` files in the forge commands directories and made available as slash commands in the UI."* Format: YAML frontmatter (`name`, `description`) plus markdown body (the prompt template). Bundled examples at v2.12.9: `.forge/commands/check.md`, `.forge/commands/fixme.md`, plus `commands/github-pr-description.md` at the repo root.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_domain/src/command.rs]`.

### permissions.yaml schema

`crates/forge_services/src/policy.rs` reads from `environment.permissions_path()`, falling back to the embedded default `permissions.default.yaml` (`include_str!`). Schema (types from `forge_app::domain::PolicyConfig`):

```yaml
policies:
  - permission: allow      # | confirm | deny
    rule:
      read: "docs/**/*"    # OR write: "src/**/*"
                            # OR command: "git *"
                            # OR url: "https://api.github.com/*"
      dir: "/scope/path/*" # optional scope (write/command/url only)
  - permission: deny
    rule:
      all:                 # logical operators: all, any, not
        - command: "rm -rf *"
        - not:
            command: "rm -rf node_modules"
```

**Tool → operation mapping:** `Read`, `FsSearch` → `read`; `Write`, `Patch`, `MultiPatch`, `Remove` → `write`; `Shell` → `command`; `Fetch` → `url`. **MCP tools bypass `permissions.yaml`** — the file governs only built-in tools.

Activation: `permissions.yaml` is enforced only when `restricted` mode is enabled in `.forge.toml`. If absent on first run with restricted mode, ForgeCode generates a default allow-all file.

Cite: `[OFFICIAL-SOURCE — tailcallhq/forgecode/blob/v2.12.9/crates/forge_services/src/policy.rs]` and `[OFFICIAL-SOURCE — forgecode.dev/docs/permissions/]`.

---

## 3. Gemini CLI (google-gemini/gemini-cli)

### Version

| Field | Value |
|---|---|
| Latest release tag | `v0.39.1` |
| Release date | 2026-04-24 |
| Commit SHA | `4d73f3413949ae5c638804c5eac27a9bcd0567ca` |
| Workspace | TypeScript pnpm monorepo (98% TS) |
| Packages | `cli`, `core`, `a2a-server`, `devtools`, `sdk`, `test-utils`, `vscode-ide-companion` |

### Resolution table

| Question | Corpus claim | Verified answer | Evidence |
|---|---|---|---|
| Hooks system in v0.26+? | YES, ~10 events with Before/After naming | **YES** — 11 events confirmed | `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/hooks/reference.md]` |
| AfterModel fires per chunk? | YES | **YES** — *"Fired for every chunk generated by the model"* | same |
| Reads `.gemini/skills/`? | YES | **YES** — workspace and `~/.gemini/skills` | `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/cli/skills.md]` |
| Reads `.agents/skills/`? | YES | **YES** — explicit alias, takes precedence over `.gemini/skills` within tier | same |
| Reads `.claude/skills/`? | (varied) | **NO** — not in skill discovery list | same |
| Tool names use `read_file`, `run_shell_command`? | YES | **YES** — confirmed in source constants | `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/packages/core/src/tools/definitions/base-declarations.ts]` |
| AGENTS.md vs GEMINI.md? | configurable | **`context.fileName` is an array; default is `GEMINI.md`; AGENTS.md is opt-in** | `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/cli/gemini-md.md]` |
| `gemini-extension.json` schema? | yes | full schema verified | `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/extensions/reference.md]` |

### Hooks (confirmed)

`docs/hooks/reference.md` at v0.39.1 documents 11 events. The corpus claim of "~10 events" is accurate; the more specific claim that "AfterModel fires per chunk" is **explicitly correct**.

| Event | Cadence | Use case (verbatim from docs) |
|---|---|---|
| `SessionStart` | Once per session | "Fires on application startup, resuming a session, or after a `/clear` command. Used for loading initial [context]." |
| `SessionEnd` | Once per session | "Fires when the CLI exits or a session is cleared. Used for cleanup or final telemetry." |
| `BeforeAgent` | Per turn | "Fires after a user submits a prompt, but before the agent begins planning. Used for prompt validation." |
| `AfterAgent` | Per turn | "Fires once per turn after the model generates its final response. Primary use case is response validation." |
| `BeforeModel` | Per LLM request | "Fires before sending a request to the LLM. Operates on a stable, SDK-agnostic request format." |
| `AfterModel` | **Per chunk** | "Fired for **every chunk** generated by the model. Modifying the response only affects the current chunk." |
| `BeforeToolSelection` | Pre-decision | "Fires before the LLM decides which tools to call. Used to filter the available toolset or force specific [choices]." |
| `BeforeTool` | Per tool call | "Fires before a tool is invoked. Used for argument validation, security checks, and parameter rewriting." |
| `AfterTool` | Per tool call | "Fires after a tool executes. Used for result auditing, context injection, or hiding sensitive output." |
| `Notification` | Observability | "Fires when the CLI emits a system alert. Used for external logging." |
| `PreCompress` | Pre-compaction | "Fires before the CLI summarizes history to save tokens. Used for logging or state saving." |

Hooks are user-configurable shell commands, HTTP endpoints, or in-process handlers, declared in `~/.gemini/settings.json` or `.gemini/settings.json`. They have been **enabled by default since v0.26.0**.

Cite: `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/hooks/reference.md]`.

### Skills

`docs/cli/skills.md` documents three discovery tiers:

1. **Workspace skills** — `.gemini/skills/` or `.agents/skills/` (committed to VCS).
2. **User skills** — `~/.gemini/skills/` or `~/.agents/skills/` (cross-workspace personal).
3. **Extension skills** — bundled inside installed `gemini-extension.json` extensions.

**Precedence:** Workspace > User > Extension. Within a single tier, **`.agents/skills/` takes precedence over `.gemini/skills/`** when the same skill name appears in both.

`.claude/skills/` is **not** in the discovery list. (This is asymmetric with Goose, which reads `.claude/skills/` but not `.gemini/skills/`.)

The activation mechanism is the `activate_skill` tool (constant `ACTIVATE_SKILL_TOOL_NAME = 'activate_skill'`), confirming progressive disclosure of skill content rather than full preload.

Cite: `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/cli/skills.md]` and `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/packages/core/src/tools/definitions/base-declarations.ts]`.

### Tool name mapping (corpus claim verified)

The corpus claim that "Gemini uses `read_file`, `run_shell_command` etc. (not `Read`, `Bash`)" is **correct**. From `packages/core/src/tools/definitions/base-declarations.ts` at v0.39.1:

```ts
export const READ_FILE_TOOL_NAME       = 'read_file';
export const SHELL_TOOL_NAME           = 'run_shell_command';
export const WRITE_FILE_TOOL_NAME      = 'write_file';
export const EDIT_TOOL_NAME            = 'replace';          // <- not "edit"
export const GREP_TOOL_NAME            = 'grep_search';
export const GLOB_TOOL_NAME            = 'glob';
export const LS_TOOL_NAME              = 'list_directory';
export const WEB_FETCH_TOOL_NAME       = 'web_fetch';
export const WEB_SEARCH_TOOL_NAME      = 'google_web_search';
export const READ_MANY_FILES_TOOL_NAME = 'read_many_files';
export const MEMORY_TOOL_NAME          = 'save_memory';
export const ACTIVATE_SKILL_TOOL_NAME  = 'activate_skill';
export const ASK_USER_TOOL_NAME        = 'ask_user';
export const ENTER_PLAN_MODE_TOOL_NAME = 'enter_plan_mode';
export const EXIT_PLAN_MODE_TOOL_NAME  = 'exit_plan_mode';
export const WRITE_TODOS_TOOL_NAME     = 'write_todos';
```

Two further notes worth flagging:
- The **edit tool is named `replace`**, not `edit_file` or `replace_in_file`. Translation tables that map Claude's `Edit` to a Gemini equivalent must use `replace`.
- The **web search tool is `google_web_search`**, not `web_search`. Provider-coupled.
- `BeforeTool` / `AfterTool` hook matchers must use these snake_case strings, not Claude's PascalCase tool names.

Cite: `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/packages/core/src/tools/definitions/base-declarations.ts]`.

### AGENTS.md vs GEMINI.md

Default context filename is **`GEMINI.md`**. AGENTS.md is **opt-in** via the `context.fileName` array setting in `settings.json`:

```json
{
  "context": {
    "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]
  }
}
```

Loading is **hierarchical and concatenated** (not first-match-wins):
1. Global user context (`~/.gemini/GEMINI.md` or whatever `context.fileName` resolves to in `~`).
2. Workspace context — search current directory and ancestors up to project root (marked by `.git`) or home directory; collect all matches.
3. Just-in-time component context — when a tool reads a file, scan its directory and ancestors up to a trusted root for matching context files.

All discovered files are concatenated and sent with every prompt. Discovery boundaries are configurable; an empty boundary array disables parent traversal. The CLI footer displays the count of loaded context files.

There is **no implicit precedence between AGENTS.md and GEMINI.md** beyond user-specified array order in `context.fileName`. Both — and any other names listed — are loaded and concatenated when present.

Cite: `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/cli/gemini-md.md]`.

### MCP / extensions

`gemini-extension.json` schema (top-level keys, all optional unless noted):

| Key | Type | Notes |
|---|---|---|
| `name` | string (required) | Lowercase, dashes |
| `version` | string (required) | SemVer |
| `description` | string | Shown on geminicli.com/extensions |
| `mcpServers` | object | Same schema as Claude Code's `.mcp.json` server map; supports `${extensionPath}` interpolation |
| `contextFileName` | string | Defaults to `GEMINI.md` if absent and a `GEMINI.md` exists in the extension dir |
| `excludeTools` | string[] | Names from the snake_case tool registry (e.g. `"run_shell_command"`) |
| `migratedTo` | string | URL of new repo if extension has moved |
| `plan` | object | `{ "directory": ".gemini/plans" }` for planning features |
| `settings` | array | User-configurable settings (`name`, `description`, `envVar`, `sensitive`) |
| `themes` | array | Custom theme definitions |

Example:

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "description": "My awesome extension",
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${extensionPath}/my-server.js"],
      "cwd": "${extensionPath}"
    }
  },
  "contextFileName": "GEMINI.md",
  "excludeTools": ["run_shell_command"],
  "plan": { "directory": ".gemini/plans" }
}
```

The `${extensionPath}` substitution is the canonical way to reference bundled assets. MCP servers declared here load on startup identically to those in `~/.gemini/settings.json`.

Cite: `[OFFICIAL-SOURCE — google-gemini/gemini-cli/blob/v0.39.1/docs/extensions/reference.md]`.

---

## Cross-agent summary

| Capability | Goose v1.32.0 | ForgeCode v2.12.9 | Gemini CLI v0.39.1 |
|---|---|---|---|
| Reads `.claude/skills/` | YES (workspace + `~`) | NO | NO |
| Reads `.agents/skills/` | YES (workspace + `~`) | NO | YES (preferred over `.gemini/skills`) |
| Reads own `.X/skills/` | `.goose/skills/` | `.forge/skills/` | `.gemini/skills/` |
| Cross-tool skill standard | `.claude/skills` + `.agents/skills` aliases | none — bespoke `Skill` struct | `.agents/skills` alias |
| User-facing hook system | NO (draft PR #8842) | NO (Rust callbacks only) | YES (11 events, since v0.26) |
| AGENTS.md read by default | YES (hardcoded with `.goosehints`) | YES (3 tiers, hardcoded) | NO (default `GEMINI.md`; opt-in via `context.fileName`) |
| MCP support | YES (Stdio/StreamableHttp/SSE-deprecated) | YES (`.mcp.json` compatible) | YES (via `gemini-extension.json` or settings) |
| Custom commands | Recipes (`recipe.yaml`) and SubRecipes | `.forge/commands/*.md` + frontmatter | Extension-bundled commands |
| Permissions config | n/a | `permissions.yaml` (allow/confirm/deny × read/write/command/url) | n/a |

**Three corrections to corpus.**

1. **Goose does NOT read `.codex/skills/` or `.cursor/skills/`.** It reads only `.goose/skills`, `.claude/skills`, and `.agents/skills` at the workspace tier. Any corpus claim of broader cross-tool reads is wrong.
2. **ForgeCode's canonical org is `tailcallhq/forgecode`**, confirmed by the install pipeline (`forgecode.dev` → `tailcallhq/forgecode`). `antinomyhq/forge` is a parallel/legacy namespace.
3. **Gemini CLI's hooks claim is fully accurate** (11 events at v0.39.1, `AfterModel` per-chunk verified). **Tool name remapping is also accurate** — `read_file`, `run_shell_command`, plus the easy-to-miss `replace` (not `edit_file`) and `google_web_search` (not `web_search`).

The Goose hook gap is closing: PR #8842 is draft and proposes a Claude Code-compatible config schema. Plan for hook-based parity to land in Goose within one or two minor versions of the v1.32 line. ForgeCode's hook system is not exposed to user config and should not be conflated with Claude/Codex/Gemini's user-facing lifecycle hooks; it is an internal Rust extension point only.

Provenance pinning: every quoted struct, constant, and schema in this document lives at the named tag (`v1.32.0`, `v2.12.9`, `v0.39.1`) at the named SHA. Future drift can be verified by re-fetching the same blob URL with a different ref. The most volatile claim is Goose hooks — once PR #8842 merges, that row in the cross-agent summary flips to YES.
