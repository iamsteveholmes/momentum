---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "Codex CLI extension contract — definitive verification of hooks, skills, AGENTS.md, MCP, sandbox modes from openai/codex source"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["no hooks vs 6-event hooks", "skills directory discovery order", "Rust % composition", "AGENTS.md precedence"]
---

# Codex CLI Extension Contract — Source Verification

## Version under inspection

- Repo: `https://github.com/openai/codex`
- Tag: `rust-v0.125.0` (latest non-alpha as of 2026-04-26; the next four tags `rust-v0.126.0-alpha.1..4` are pre-release)
- Commit SHA: `637f7dd6d737f3961e6bf32fbb3861c4953269c5`
- Workspace: Cargo workspace under `codex-rs/` plus a thin `codex-cli/` Node wrapper

## 1. Hooks — RESOLVED: full first-class system

The "no first-class hook system" claim is **wrong as of v0.125.0**. The corpus citation matching reality is "6-event hook system mirroring Claude Code's JSON shape." There is a dedicated crate `codex-rs/hooks/` containing engine, schema, types, registry, dispatcher, and per-event modules.

### Six events

`codex-rs/hooks/src/events/mod.rs` declares exactly six event modules:

```rust
pub(crate) mod common;
pub mod permission_request;
pub mod post_tool_use;
pub mod pre_tool_use;
pub mod session_start;
pub mod stop;
pub mod user_prompt_submit;
```

The wire schema in `codex-rs/hooks/src/schema.rs` (lines 70-84) names them in the Claude-compatible PascalCase:

```rust
pub(crate) enum HookEventNameWire {
    #[serde(rename = "PreToolUse")] PreToolUse,
    #[serde(rename = "PermissionRequest")] PermissionRequest,
    #[serde(rename = "PostToolUse")] PostToolUse,
    #[serde(rename = "SessionStart")] SessionStart,
    #[serde(rename = "UserPromptSubmit")] UserPromptSubmit,
    #[serde(rename = "Stop")] Stop,
}
```

This is five Claude Code events plus a Codex-original `PermissionRequest` event (sandbox/approval gate, not in Claude Code).

### Schema mirrors Claude Code's JSON shape

Each event has both an input and an output schema generated via `schemars` and stored as fixtures under `codex-rs/hooks/schema/generated/*.command.{input,output}.schema.json`. Field names, casing, and semantics mirror Claude Code's hooks contract:

- Universal output fields (`schema.rs:59-68`): `continue` (default `true`), `stopReason`, `suppressOutput`, `systemMessage` — identical to Claude Code's universal hook output.
- `PreToolUse` output supports `decision: "approve" | "block"` (legacy) plus the newer `hookSpecificOutput.permissionDecision: "allow" | "deny" | "ask"` with `permissionDecisionReason` and `updatedInput` — direct parity with Claude Code.
- `PostToolUse` output supports `decision: "block"` and `hookSpecificOutput.additionalContext` plus an `updatedMCPToolOutput` field.
- `Stop` output: `decision: "block"` + `reason` (Claude requires reason when blocking).

A test in `schema.rs:678-721` explicitly notes the **single Codex divergence** from Claude — a `turn_id` field added to all turn-scoped event inputs:

> // Codex intentionally diverges from Claude's public hook docs here so
> // internal hook consumers can key off the active turn.

### Blocking semantics

`codex-rs/hooks/src/types.rs:16-25` defines a three-valued result:

```rust
pub enum HookResult {
    Success,
    /// FailedContinue: hook failed, but other subsequent hooks should still execute and the
    /// operation should continue.
    FailedContinue(Box<dyn std::error::Error + Send + Sync + 'static>),
    /// FailedAbort: hook failed, other subsequent hooks should not execute, and the operation
    /// should be aborted.
    FailedAbort(Box<dyn std::error::Error + Send + Sync + 'static>),
}
```

`PreToolUse` denial blocks the tool call; `PostToolUse` `block` injects a feedback message; `Stop` block can prevent session termination. This matches Claude Code's behavioral contract.

### Registration mechanism

Hooks register via either `hooks.json` (JSON form) or a `[hooks]` table in `config.toml` (TOML form). From `codex-rs/hooks/src/engine/discovery.rs:178-219`:

```rust
fn load_hooks_json(config_folder: Option<&Path>, ...) -> Option<...> {
    let source_path = config_folder?.join("hooks.json");
    ...
    let parsed: HooksFile = match serde_json::from_str(&contents) { ... };
}

fn load_toml_hooks_from_layer(layer: &ConfigLayerEntry, ...) -> Option<...> {
    let hook_value = layer.config.get("hooks")?.clone();
    let parsed = match HookEventsToml::deserialize(hook_value) { ... };
}
```

Both forms accept the same `HookEventsToml` shape (`codex-rs/config/src/hook_config.rs:15-29`):

```rust
pub struct HookEventsToml {
    #[serde(rename = "PreToolUse",        default)] pub pre_tool_use:        Vec<MatcherGroup>,
    #[serde(rename = "PermissionRequest", default)] pub permission_request:  Vec<MatcherGroup>,
    #[serde(rename = "PostToolUse",       default)] pub post_tool_use:       Vec<MatcherGroup>,
    #[serde(rename = "SessionStart",      default)] pub session_start:       Vec<MatcherGroup>,
    #[serde(rename = "UserPromptSubmit",  default)] pub user_prompt_submit:  Vec<MatcherGroup>,
    #[serde(rename = "Stop",              default)] pub stop:                Vec<MatcherGroup>,
}
```

Each `MatcherGroup` has an optional regex `matcher` (e.g. `"Edit|Write"`, `"^Bash$"`, `"*"`) and a list of `HookHandlerConfig` entries. Three handler kinds are declared (`hook_config.rs:92-109`): `command` (shell command — fully implemented), `prompt` (declared but emits "not supported yet" warning during discovery — `discovery.rs:364-367`), and `agent` (also "not supported yet" — `discovery.rs:368-371`). Today, only the `command` form runs; the prompt/agent variants are reserved.

### Configuration layering

`codex-rs/hooks/src/engine/discovery.rs:54-101` walks a `ConfigLayerStack` covering: `System` (`/etc/codex/...`), `User` (`$CODEX_HOME/...`, default `~/.codex`), `Project` (`<repo>/.codex/...`), `Mdm` (managed-policy), `SessionFlags`, and legacy managed-config layers — emitting warnings if both `hooks.json` and `config.toml` `[hooks]` are populated in the same layer. Hook source is tagged with a `HookSource` enum (`System`, `User`, `Project`, `Mdm`, `SessionFlags`, etc.), preserving Claude Code's "where did this come from" lineage.

**Verdict: 6-event hook system mirroring Claude Code's JSON shape, with one Codex extension (`turn_id`) and one Codex-original event (`PermissionRequest`). Registration via `hooks.json` or TOML in System/User/Project/Mdm layers.**

## 2. AGENTS.md handling — RESOLVED

`codex-rs/core/src/agents_md.rs:1-43` documents the canonical algorithm in a top-of-file block comment:

```rust
//! AGENTS.md discovery and user instruction assembly.
//!
//! 1. Determine the project root by walking upwards from the current working
//!    directory until a configured `project_root_markers` entry is found.
//!    When `project_root_markers` is unset, the default marker list is used
//!    (`.git`). If no marker is found, only the current working directory is
//!    considered. An empty marker list disables parent traversal.
//! 2. Collect every `AGENTS.md` found from the project root down to the
//!    current working directory (inclusive) and concatenate their contents in
//!    that order.
//! 3. We do **not** walk past the project root.

pub const DEFAULT_AGENTS_MD_FILENAME: &str = "AGENTS.md";
pub const LOCAL_AGENTS_MD_FILENAME: &str = "AGENTS.override.md";
```

Two distinct discovery passes:

- **Global instructions** (`AgentsMdManager::load_global_instructions`, `agents_md.rs:96-113`) — checks `$CODEX_HOME/AGENTS.override.md` first, then `$CODEX_HOME/AGENTS.md`. The `.override.md` file wins per the iteration order `[LOCAL_AGENTS_MD_FILENAME, DEFAULT_AGENTS_MD_FILENAME]`.
- **Project chain** (`agents_md.rs:255-...`) — walks `cwd` upward to the project root marker (defaulting to `.git`), then concatenates every `AGENTS.md` from project-root → cwd inclusive, separated by `\n\n`. Bounded by `project_doc_max_bytes` (truncates if exceeded).

User-supplied `Config::user_instructions` is concatenated with AGENTS.md content via the literal separator `"\n\n--- project-doc ---\n\n"` (`agents_md.rs:43`). A `child_agents_md` feature flag (`agents_md.rs:157-162`) appends a hierarchical-agents helper message.

**Precedence: User config-level `instructions` first, then AGENTS.md chain (project-root → cwd, in that order). Within a directory, `AGENTS.override.md` beats `AGENTS.md`. Global `$CODEX_HOME/AGENTS.{override,}.md` is loaded as a separate "instruction source" alongside the in-tree chain.**

## 3. Skills support — RESOLVED: native, multi-root

Codex v0.125.0 has a first-class skills system (`codex-rs/skills/` for system skills, `codex-rs/core-skills/` for loading/rendering, `codex-rs/core/src/skills.rs` for session integration). Discovery is in `codex-rs/core-skills/src/loader.rs`.

Constants (`loader.rs:106-109`):

```rust
const AGENTS_DIR_NAME: &str = ".agents";
const SKILLS_DIR_NAME: &str = "skills";
```

The `skill_roots_with_home_dir` function walks the config-layer stack and adds these roots (`loader.rs:243-311`):

| Layer | Path | Scope |
|---|---|---|
| Project | `<repo>/.codex/skills` | `SkillScope::Repo` |
| User (config layer) | `$CODEX_HOME/skills` (deprecated, kept for back-compat) | `SkillScope::User` |
| User (home) | `$HOME/.agents/skills` | `SkillScope::User` |
| User (cached) | `$CODEX_HOME/skills/.system` (embedded shipped skills) | `SkillScope::System` |
| System | `/etc/codex/skills` | `SkillScope::Admin` |
| Plugin | `<plugin_root>/skills` (per loaded plugin) | `SkillScope::User` |
| Repo (ancestral) | every directory between `cwd` and project root: `<dir>/.agents/skills` | `SkillScope::Repo` |

```rust
ConfigLayerSource::User { .. } => {
    // Deprecated user skills location (`$CODEX_HOME/skills`), kept for backward
    // compatibility.
    roots.push(SkillRoot { path: config_folder.join(SKILLS_DIR_NAME), scope: SkillScope::User, ... });

    // `$HOME/.agents/skills` (user-installed skills).
    if let Some(home_dir) = home_dir {
        roots.push(SkillRoot { path: home_dir.join(AGENTS_DIR_NAME).join(SKILLS_DIR_NAME),
                               scope: SkillScope::User, ... });
    }

    // Embedded system skills are cached under `$CODEX_HOME/skills/.system` and are a
    // special case (not a config layer).
    roots.push(SkillRoot { path: system_cache_root_dir(&config_folder),
                           scope: SkillScope::System, ... });
}
```

Iteration is `HighestPrecedenceFirst` over the layer stack (`loader.rs:251`), and roots are deduplicated by path (`dedupe_skill_roots_by_path`).

System skills are embedded into the binary via `include_dir!` and unpacked on startup into `$CODEX_HOME/skills/.system`, gated by a fingerprint marker file (`codex-rs/skills/src/lib.rs:32-56`). The shipped sample is `skill-creator` (`lib.rs:159-166` test asserts `skill-creator/SKILL.md` is present).

**No `.claude/skills` discovery anywhere in the source.** Codex reads `.codex/skills/` (project), `.agents/skills` (project ancestors and `$HOME/.agents/skills`), the deprecated `$CODEX_HOME/skills/`, and `/etc/codex/skills/`. Cross-agent compatibility with Claude Code skills lives in the `.agents/skills` convention, not the Claude-namespaced path.

## 4. Custom prompts — DEPRECATED / NOT PRESENT

A grep across the entire `codex-rs/` workspace for prompt-directory loading returns no matches:

- `rg "PROMPTS_DIR|prompts_dir|custom_prompt|user_prompt_dir|\.codex/prompts|join.*prompts" --type rust` → 0 hits beyond the `include_str!("prompts/...")` calls that embed *built-in* prompt strings into the binary (`codex-rs/core/src/context/permissions_instructions.rs`, `codex-rs/protocol/src/models.rs:841`).
- `codex-rs/tui/src/slash_command.rs` enumerates a fixed `enum SlashCommand` (Model, Approvals, Skills, Memories, Mcp, Plugins, Personality, Realtime, etc.) — there is no plugin/user-supplied slash-command loader.

User-extensible behaviour has migrated to **skills**. The earlier `~/.codex/prompts/` directory referenced in older blogs is not loaded by v0.125.0 source. If documentation references it, it is stale.

## 5. MCP — RESOLVED: per-server config in TOML, two transports

`codex-rs/config/src/config_toml.rs:177-178`:

```rust
#[schemars(schema_with = "crate::schema::mcp_servers_schema")]
pub mcp_servers: HashMap<String, McpServerConfig>,
```

`McpServerConfig` (`codex-rs/config/src/mcp_types.rs:118-...`) flattens a transport plus per-server policy fields:

```rust
pub struct McpServerConfig {
    #[serde(flatten)] pub transport: McpServerTransportConfig,
    pub experimental_environment: Option<String>,
    pub enabled: bool,                                // default true
    pub required: bool,                               // exec-mode hard fail
    pub supports_parallel_tool_calls: bool,
    pub startup_timeout_sec: Option<Duration>,
    pub tool_timeout_sec: Option<Duration>,
    pub default_tools_approval_mode: Option<AppToolApproval>,  // Auto | Prompt | Approve
    pub enabled_tools: Option<Vec<String>>,           // allow-list
    pub disabled_tools: Option<Vec<String>>,          // deny-list
    pub scopes: Option<Vec<String>>,                  // OAuth
    pub oauth_resource: Option<String>,               // RFC 8707
    pub tools: HashMap<String, McpServerToolConfig>,  // per-tool approval
}
```

Two transports (`mcp_types.rs:362-392`):

```rust
#[serde(untagged, deny_unknown_fields, rename_all = "snake_case")]
pub enum McpServerTransportConfig {
    Stdio { command: String, args: Vec<String>, env: Option<HashMap<String,String>>,
            env_vars: Vec<McpServerEnvVar>, cwd: Option<PathBuf> },
    StreamableHttp { url: String, bearer_token_env_var: Option<String>,
                     http_headers: Option<HashMap<String,String>>,
                     env_http_headers: Option<HashMap<String,String>> },
}
```

So Codex supports both stdio MCP and the 2025-06-18 streamable-HTTP transport, with bearer-token-from-env-var, OAuth scopes/resource, per-server enable/disable, allow/deny lists, per-tool approval gates, and timeouts. Configured under `[mcp_servers.<name>]` in `config.toml` (TOML inline), reusable across the same config-layer stack as hooks.

## 6. Sandbox modes — RESOLVED

`codex-rs/protocol/src/config_types.rs:61-76`:

```rust
#[derive(Deserialize, Debug, Clone, Copy, PartialEq, Default, Serialize, Display, JsonSchema, TS)]
#[serde(rename_all = "kebab-case")]
#[strum(serialize_all = "kebab-case")]
pub enum SandboxMode {
    #[serde(rename = "read-only")]          #[default] ReadOnly,
    #[serde(rename = "workspace-write")]               WorkspaceWrite,
    #[serde(rename = "danger-full-access")]            DangerFullAccess,
}
```

Three modes, default `read-only`. `workspace-write` permits writes inside the project root (and configured read-roots); `danger-full-access` removes the sandbox entirely. The hook payload reflects this — `codex-rs/hooks/src/types.rs:99,125-138` carries `sandbox_policy` strings like `"danger-full-access"` and a `SandboxPermissions` enum.

A separate `WindowsSandboxLevel` (`config_types.rs:131-136`: `Disabled | RestrictedToken | Elevated`) controls the Windows-specific sandbox backend.

## 7. Repository language composition — RESOLVED

Neither `tokei` nor `cloc` is installed in this environment, so the percentages were computed with `wc -l` over all tracked source files at `rust-v0.125.0`, excluding `target/`, `node_modules/`, and `.git/`:

| Language | Files | Lines |
|---|---:|---:|
| Rust (`.rs`) | 1,637 | 740,681 |
| Python (`.py`) | 85 | 24,274 |
| TypeScript (`.ts`) | 511 | 8,103 |
| Markdown (`.md`) | 162 | 15,827 |
| TOML (`.toml`) | 120 | 4,551 |
| JavaScript (`.js`) | 6 | 2,333 |

Computing a Linguist-style percentage that excludes docs/config but includes all real source languages (Rust + Python + TypeScript + JavaScript): **Rust = 95.52%**. Excluding the small `js` slice: **95.81%**. Including markdown brings Rust down to 93.89%.

The corpus claims of "94.9%" and "96.3%" both fall within plausible Linguist boundaries depending on which paths/extensions the sampler swept (e.g. excluding the SDK `sdk/python/` and `sdk/typescript/` directories, or excluding test fixtures, drives the ratio higher; including them drives it lower). **The most defensible single number for v0.125.0 is "Rust ≈ 95–96% by line count, with the remainder dominated by Python (SDK + scripts) and TypeScript (SDK)."** Treat any precise figure to one decimal as commit-dependent — the repo is still actively shifting code (v0.126 alpha series in flight).

## Summary table

| Verification target | Resolution |
|---|---|
| Hook system | **Yes — full first-class.** 6 events (`PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart`, `UserPromptSubmit`, `Stop`), Claude-shaped JSON, blocking semantics, `hooks.json` or TOML `[hooks]` registration across System/User/Project/Mdm layers. Single divergence: `turn_id` extension. |
| Skills discovery order | `<repo>/.codex/skills` → `<ancestor>/.agents/skills` → `$CODEX_HOME/skills` (deprecated) → `$HOME/.agents/skills` → `$CODEX_HOME/skills/.system` (bundled) → `/etc/codex/skills` → plugin roots. **No `.claude/skills`.** |
| AGENTS.md precedence | Global `$CODEX_HOME/AGENTS.override.md` > `$CODEX_HOME/AGENTS.md`; in-tree chain walks project-root → cwd, concatenating every `AGENTS.md`; `AGENTS.override.md` beats `AGENTS.md` per directory. Default project-root marker is `.git`. |
| MCP | Per-server TOML under `[mcp_servers.<name>]`; transports `stdio` and `streamable_http`; OAuth scopes/resource; per-tool approval; allow/deny lists; bearer-token-from-env. |
| Sandbox modes | `read-only` (default), `workspace-write`, `danger-full-access`; plus Windows `Disabled | RestrictedToken | Elevated`. |
| Custom prompts directory | **Not present in v0.125.0 source.** No loader for `~/.codex/prompts/`. Slash commands are a fixed enum. User extensibility goes through skills. |
| Rust % | ≈95.5–95.8% by source-line count at `rust-v0.125.0`; both 94.9% and 96.3% are within sampler-dependent variance. |

The corpus's "no first-class hook system" claim should be treated as out of date relative to v0.125.0 — Codex now ships a Claude-Code-shaped hook contract end-to-end.
