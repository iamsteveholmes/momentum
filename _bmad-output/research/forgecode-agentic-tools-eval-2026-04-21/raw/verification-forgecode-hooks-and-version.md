---
content_origin: claude-code-subagent
date: 2026-04-21
sub_question: "Primary-source verification of ForgeCode hooks presence and current version — AVFL dispute resolution"
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

# ForgeCode — Direct Repo Verification

## Dispute 1: Hooks / Lifecycle Events

### Finding

**Partial — hooks exist in source, but NOT as a user-configurable extension system.** ForgeCode has a fully realized lifecycle-event framework in Rust with six event types (`Start`, `End`, `Request`, `Response`, `ToolcallStart`, `ToolcallEnd`) and five concrete handlers (`CompactionHandler`, `DoomLoopDetector`, `PendingTodosHandler`, `TitleGenerationHandler`, `TracingHandler`). However, these hooks are **compiled into the binary and wired in `app.rs`** — they are not a Claude Code-style user-extensibility surface where a developer drops a shell script or declares `PreToolUse`/`PostToolUse` handlers in YAML/JSON config.

The only user-facing toggle over hook behavior is the boolean config flag `verify_todos` (default `false`), which conditionally adds the `PendingTodosHandler` to the `on_end` hook chain. That is the sum total of external hook configurability.

**Both the AVFL dispute sides are partially correct:**
- Gemini's claim of "native hook systems for validation and logging" is **technically true of the internal architecture** but misleading — a user cannot configure their own hooks without recompiling Forge.
- The four subagent files that said hooks are "absent" were correct **from a user-surface perspective** — there is no equivalent to Claude Code's `~/.claude/settings.json` hooks array.

### Evidence

**Source code: `crates/forge_domain/src/hook.rs`** `[OFFICIAL]` — defines the `LifecycleEvent` enum and `Hook` struct:

```rust
pub enum LifecycleEvent {
    Start(EventData<StartPayload>),
    End(EventData<EndPayload>),
    Request(EventData<RequestPayload>),
    Response(EventData<ResponsePayload>),
    ToolcallStart(EventData<ToolcallStartPayload>),
    ToolcallEnd(EventData<ToolcallEndPayload>),
}

pub struct Hook {
    on_start: Box<dyn EventHandle<EventData<StartPayload>>>,
    on_end: Box<dyn EventHandle<EventData<EndPayload>>>,
    on_request: Box<dyn EventHandle<EventData<RequestPayload>>>,
    on_response: Box<dyn EventHandle<EventData<ResponsePayload>>>,
    on_toolcall_start: Box<dyn EventHandle<EventData<ToolcallStartPayload>>>,
    on_toolcall_end: Box<dyn EventHandle<EventData<ToolcallEndPayload>>>,
}
```
URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/hook.rs

**Source code: `crates/forge_app/src/hooks/mod.rs`** `[OFFICIAL]` — declares the five built-in handlers:

```rust
mod compaction;
mod doom_loop;
mod pending_todos;
mod title_generation;
mod tracing;

pub use compaction::CompactionHandler;
pub use doom_loop::DoomLoopDetector;
pub use pending_todos::PendingTodosHandler;
pub use title_generation::TitleGenerationHandler;
pub use tracing::TracingHandler;
```
URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/mod.rs

**Source code: `crates/forge_app/src/app.rs`** `[OFFICIAL]` — shows hooks are wired in Rust code, not configuration:

```rust
let on_end_hook = if forge_config.verify_todos {
    tracing_handler.clone().and(title_handler.clone())
        .and(PendingTodosHandler::new())
} else {
    tracing_handler.clone().and(title_handler.clone())
};

let hook = Hook::default()
    .on_start(tracing_handler.clone().and(title_handler))
    .on_request(tracing_handler.clone().and(DoomLoopDetector::default()))
    .on_response(
        tracing_handler.clone()
            .and(CompactionHandler::new(agent.clone(), environment.clone())),
    )
    .on_toolcall_start(tracing_handler.clone())
    .on_toolcall_end(tracing_handler)
    .on_end(on_end_hook);
```
URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/app.rs

**Config schema: `forge.schema.json`** `[OFFICIAL]` — the only hook-related user-facing configuration:

- `verify_todos: boolean` (default false): "Enables the pending todos hook that checks for incomplete todo items when a task ends and reminds the LLM about them."
- No `hooks`, `on_tool_use`, `PreToolUse`, `lifecycle`, or any similar user-configurable hook keys exist anywhere in the root schema properties (verified via full schema inspection).

URL: https://github.com/tailcallhq/forgecode/blob/main/forge.schema.json

**GitHub code search confirms absence of user-facing hook config:**
- `repo:tailcallhq/forgecode hook` → 21 results, all internal Rust source files and doc-level mentions.
- `repo:tailcallhq/forgecode lifecycle` → 9 results, all internal implementation references.
- No `hooks:` key appears in `forge.yaml` / `forge.toml` config surfaces.

**Gemini's "Tool-Call Correction Layer" and "Semantic Entry-Point Discovery" components are HALLUCINATIONS** `[OFFICIAL]`:
- `repo:tailcallhq/forgecode "Tool-Call Correction"` → **0 results**
- `repo:tailcallhq/forgecode "Semantic Entry-Point"` → **0 results**

These named components do not exist in the codebase under those names.

### Determinism Mechanism

Forge achieves workflow determinism through a layered set of mechanisms, none of which are called "hooks" at the user surface:

1. **Three-mode agent separation (Forge / Muse / Sage)** `[OFFICIAL]` — Each built-in agent is a `.md` file with YAML frontmatter declaring `tools:`, `reasoning:`, and a system prompt. The tools list is a hard allowlist enforced at the orchestrator level, not a prompt suggestion.
   - **Forge** agent has: `task, sem_search, fs_search, read, write, undo, remove, patch, multi_patch, shell, fetch, skill, todo_write, todo_read, mcp_*` — it is the only agent that can modify files.
   - **Muse** agent has: `sem_search, sage, search, read, fetch, plan, mcp_*` — it has a `plan` tool but no `write`/`patch`/`shell`, so it is structurally incapable of modifying code.
   - **Sage** agent has: `sem_search, search, read, fetch` — pure read-only research.
   - URLs: https://github.com/tailcallhq/forgecode/tree/main/crates/forge_repo/src/agents

2. **Built-in `DoomLoopDetector` hook** `[OFFICIAL]` — fires on every `Request` event. Detects two loop patterns from conversation history: (a) consecutive identical `(tool_name, arguments)` pairs exceeding threshold 3, and (b) repeating `[A,B,C][A,B,C][A,B,C]` sequences. When detected, it injects a warning message into the conversation context to break the loop. This is the closest thing to a Claude Code `PreToolUse` hook, but it is not user-configurable — it fires always, at a fixed threshold.
   - URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/doom_loop.rs

3. **Built-in `PendingTodosHandler` hook** `[OFFICIAL]` — fires on the `End` event (only when `verify_todos: true`). If the LLM signals "done" but the conversation's todo list still has `pending` or `in_progress` items, the handler injects a reminder listing outstanding todos, preventing premature termination. This is the main user-toggleable determinism mechanism.
   - URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/pending_todos.rs

4. **`todo_write` / `todo_read` tools** `[OFFICIAL]` — the `forge` agent's system prompt instructs it to "Use this tool VERY frequently to ensure that you are tracking your tasks." Combined with `PendingTodosHandler`, this creates a planning-cycle enforcement loop. Each `todo_write` call sends only changed items (server-side merges by `content` key).
   - URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/tools/descriptions/todo_write.md

5. **`plan` tool + `plans/` directory** `[OFFICIAL]` — the Muse agent writes plan markdown files to a `plans/` directory; the `execute-plan` skill then runs them. This is Forge's plan-approval pattern: the plan is materialized as a file the user can review before execution, rather than an inline "plan mode" toggle. There is **no formal plan-approval gate** in the code — the user-review step is conventional, enforced by agent separation rather than a runtime check.

6. **`task` tool (subagents)** `[OFFICIAL]` — gated by the `subagents: boolean` config flag (default `false`). When enabled, the forge agent gets a `task` tool that launches specialized sub-agents as subprocesses with their own tool allowlists. Note that `subagents: true` also **removes** the `sage` research tool from the forge agent — they are mutually exclusive. Subagents support `session_id` resumption for multi-turn delegation.
   - URL: https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/tools/descriptions/task.md

7. **`CompactionHandler` on `Response` events** `[OFFICIAL]` — auto-compacts conversation context when token budget is exceeded. Not strictly a determinism mechanism but prevents the agent from dropping work due to context overflow.

8. **`restricted` shell mode** `[OFFICIAL]` — a `restricted: boolean` config flag (README: "Restricted shell mode limits file system access and prevents unintended changes"). Safety, not determinism, but relevant to controlled execution.

9. **`max_tool_failure_per_turn` and `max_requests_per_turn`** `[OFFICIAL]` — root-level schema config flags that cap retries and LLM calls per turn, providing bounded execution guarantees.

**Summary of the determinism story:** Forge trades Claude Code's user-extensible hook system for a **curated set of hardcoded determinism primitives** (doom-loop detection, todo-reminder, context compaction, tool-allowlist-per-agent, plan-file workflow). A user cannot add a custom `post_edit_lint` hook without modifying Rust source — but they also get working determinism out of the box without configuring one.

## Dispute 2: Current Version

### Finding

**Current version: v2.12.0, published 2026-04-21T06:52:07Z (today).** The subagent claim of v2.12.0 is correct; Gemini's v0.106.0 claim was accurate for the date it names (Aug 2025) but is ~8 months stale relative to today's date.

### Evidence

**Latest release on GitHub Releases API** `[OFFICIAL]`:

```
Tag: v2.12.0
Name: v2.12.0
Published: 2026-04-21T06:52:07Z
Prerelease: False
URL: https://github.com/tailcallhq/forgecode/releases/tag/v2.12.0
```
Release notes include `feat(rprompt): display reasoning effort next to model in zsh rprompt (#3087)` and several provider fixes. URL: https://github.com/tailcallhq/forgecode/releases/tag/v2.12.0

**Version trajectory from release list** `[OFFICIAL]`:
- v0.106.0 published 2025-08-12 (matches Gemini's "August 2025" claim exactly — so Gemini was citing real but outdated data)
- v1.0.0 published 2025-10-25
- v2.0.0 published 2026-03-14
- v2.12.0 published 2026-04-21 (today)

Total tags in repo: **340**. Total v2.x releases: **36**. Total v1.x releases: **40** (v1.0.0 → v1.32.1).

**Cargo.toml workspace version:** The top-level `[workspace.package]` in `Cargo.toml` reads `version = "0.1.0"` — this is a placeholder and does not reflect the release tag. Release versioning is driven by git tags + GitHub Actions release-drafter, not the Cargo manifest. URL: https://github.com/tailcallhq/forgecode/blob/main/Cargo.toml

### Repo Canonicality

**`tailcallhq/forgecode` is the canonical repo. `antinomyhq/forge` is a 301 redirect to it.** `[OFFICIAL]`

Direct evidence:
```
$ curl -sI https://github.com/antinomyhq/forge | head -5
HTTP/2 301
location: https://github.com/tailcallhq/forgecode
```

Confirmation: GitHub's rename-redirect behavior — the org `antinomyhq` is the former org name, `tailcallhq` is the current owner. Both URLs resolve to the same repo (id `900461318`).

**Repo stats as of 2026-04-21 (pulled from `gh api repos/tailcallhq/forgecode`)** `[OFFICIAL]`:
- Stars: **6,794**
- Forks: **1,374**
- Open issues: **132**
- Subscribers: **23**
- Default branch: `main`
- Language: **Rust**
- License: Apache-2.0
- Created: 2024-12-08
- Last push: 2026-04-21T19:52:13Z (today)
- Topics include: `ai-pair-programming`, `claude-4-sonnet`, `cli-assistant`, `open-source-claude-code`, `openai`, `qwen`, `shell`

The `open-source-claude-code` topic tag suggests the authors explicitly position Forge as a Claude Code competitor/alternative.

## Summary

**Dispute 1:** Both sides were partially right. Forge has a full internal lifecycle-hook architecture (6 event types, 5 handlers) but exposes **zero user-configurable hook surface** — the only relevant user toggle is `verify_todos: boolean`. The "native hook systems for validation and logging" phrasing from Gemini is technically true but misleading for a developer expecting Claude Code-style `.claude/settings.json` hook files. Gemini's "Tool-Call Correction Layer" and "Semantic Entry-Point Discovery" components **do not exist** in the codebase under those names — those are hallucinations. Determinism is achieved via hardcoded handlers (`DoomLoopDetector`, `PendingTodosHandler`, `CompactionHandler`), strict per-agent tool allowlists (Forge/Muse/Sage), the `todo_write`-`verify_todos` enforcement loop, the file-materialized plan workflow (`plan` tool → `plans/` → `execute-plan` skill), and bounded-turn config flags (`max_tool_failure_per_turn`, `max_requests_per_turn`, `restricted` shell).

**Dispute 2:** Current version is **v2.12.0, published today (2026-04-21T06:52:07Z)**. The subagents were correct. Gemini's v0.106.0 cite is real-but-stale — that release shipped 2025-08-12, eight months before the research date. Forge crossed v1.0.0 on 2025-10-25 and v2.0.0 on 2026-03-14, so the major-version jumps happened well after Gemini's training window. The canonical repo is **`tailcallhq/forgecode`** (6,794 stars, 1,374 forks, 340 tags, 132 open issues, Apache-2.0, Rust); `antinomyhq/forge` is an HTTP 301 redirect.

## Sources

- [tailcallhq/forgecode README](https://github.com/tailcallhq/forgecode/blob/main/README.md) `[OFFICIAL]`
- [tailcallhq/forgecode v2.12.0 release](https://github.com/tailcallhq/forgecode/releases/tag/v2.12.0) `[OFFICIAL]`
- [tailcallhq/forgecode v0.106.0 release (Gemini's cited version)](https://github.com/tailcallhq/forgecode/releases/tag/v0.106.0) `[OFFICIAL]`
- [crates/forge_domain/src/hook.rs — LifecycleEvent and Hook definitions](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/hook.rs) `[OFFICIAL]`
- [crates/forge_app/src/hooks/mod.rs — handler exports](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/mod.rs) `[OFFICIAL]`
- [crates/forge_app/src/hooks/doom_loop.rs — loop-detection handler](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/doom_loop.rs) `[OFFICIAL]`
- [crates/forge_app/src/hooks/pending_todos.rs — todo reminder handler](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/pending_todos.rs) `[OFFICIAL]`
- [crates/forge_app/src/app.rs — hook wiring in orchestrator setup](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/app.rs) `[OFFICIAL]`
- [forge.schema.json — root config schema, verify_todos and subagents flags](https://github.com/tailcallhq/forgecode/blob/main/forge.schema.json) `[OFFICIAL]`
- [crates/forge_repo/src/agents/forge.md — implementation agent with task management prompt](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_repo/src/agents/forge.md) `[OFFICIAL]`
- [crates/forge_repo/src/agents/muse.md — planning-only agent definition](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_repo/src/agents/muse.md) `[OFFICIAL]`
- [crates/forge_repo/src/agents/sage.md — research-only agent definition](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_repo/src/agents/sage.md) `[OFFICIAL]`
- [crates/forge_domain/src/tools/descriptions/todo_write.md — todo_write tool description](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/tools/descriptions/todo_write.md) `[OFFICIAL]`
- [crates/forge_domain/src/tools/descriptions/task.md — subagent task tool description](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/tools/descriptions/task.md) `[OFFICIAL]`
- [GitHub API response confirming antinomyhq/forge → tailcallhq/forgecode redirect (HTTP 301)](https://github.com/tailcallhq/forgecode) `[OFFICIAL]`
