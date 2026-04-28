---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "Claude Code hook contract — definitive enumeration of events, handler types, blocking semantics, settings.json schema as of 2026-04-26"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["8 events vs 28 events", "permissionDecision JSON shape", "handler types"]
---

## Resolution

**Both corpus claims are wrong, but the 28-event claim is closer to current truth.** As of 2026-04-26 the canonical Claude Code hooks reference enumerates **28 hook events** in its `## Hook events` section and a 28-row `Hook lifecycle` summary table. The legacy "8 events" figure reflects the early 2025 hook contract (roughly v1.0.x) and has been superseded by ~20 additions over Claude Code v1.0 → v2.1.119. The correct answer for "today" is **28 events as documented**, with one additional (`Setup`) shipped in CHANGELOG v2.1.10 but not currently surfaced as a section header on the live reference page.

The corpus's "command|http|mcp_tool|prompt|agent" handler-type set is **fully correct**. The corpus's `permissionDecision: "deny"` claim is **correct as a value**, but only inside `hookSpecificOutput` and only for `PreToolUse` (and analogous structure for `PermissionRequest`/`PermissionDenied`/`Elicitation*`). It is not a top-level field.

## Canonical doc URL (with HTTP fetch confirmation)

- Original `https://docs.claude.com/en/docs/claude-code/hooks` — `301 Moved Permanently` → `https://code.claude.com/docs/en/hooks`
- Original `https://docs.claude.com/en/docs/claude-code/hooks-reference` — `301 Moved Permanently` → `https://code.claude.com/docs/en/hooks-reference` (now **404** — the reference page was consolidated into `/docs/en/hooks`)
- Authoritative reference: **`https://code.claude.com/docs/en/hooks`** (page title: "Hooks reference"; subtitle confirms this page covers schema, JSON I/O, exit codes, async, HTTP hooks, prompt hooks, MCP tool hooks)
- Quickstart companion: `https://code.claude.com/docs/en/hooks-guide` ("Automate workflows with hooks")
- Release notes: `https://docs.claude.com/en/release-notes/claude-code` → `307 Temporary Redirect` → `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md` (3,285 lines, v1.0.x through v2.1.119)
- Markdown variant fetched directly: `https://code.claude.com/docs/en/hooks.md` (155,864 bytes, 2,549 lines)

The previous corpus citation `code.claude.com/docs/en/hooks` is correct; the cited counts disagreed because they reflect different points in time.

## Total event count (resolved)

The live `## Hook events` section contains 28 `###` event subsections, in this lifecycle order:

`SessionStart`, `InstructionsLoaded`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `PermissionDenied`, `Notification`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `SessionEnd`, `Elicitation`, `ElicitationResult`.

The `Hook lifecycle` summary table (lines 27–56 of the markdown source) lists the same 28 events with one-line "When it fires" descriptions. A 29th event, `Setup`, was added in CHANGELOG entry v2.1.10 ("Added new `Setup` hook event that can be triggered via `--init`, `--init-only`, or `--maintenance` CLI flags") but does not appear as a section header on the current reference page — likely an experimental/maintenance-mode event omitted from the main lifecycle docs.

Any answer that says "8 events" is referring to v1.0-era hooks: at v1.0.0 the contract was approximately `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`, `UserPromptSubmit`, plus `SessionStart`/`SessionEnd` as those were added — the count crossed 8 within v1.0.x and has roughly tripled since.

## Per-event reference table

The live page consolidates trigger and blocking semantics in a single matrix. The key columns: **fires when**, **can block?**, **decision pattern**, **key fields**.

| # | Event | Fires when | Can block? | Decision pattern |
|---|---|---|---|---|
| 1 | `SessionStart` | session begins or resumes | No | none (stdout = injected context) |
| 2 | `InstructionsLoaded` | CLAUDE.md / `.claude/rules/*.md` loaded into context | No | exit code ignored |
| 3 | `UserPromptSubmit` | user submits prompt, before Claude processes | Yes | top-level `decision: "block"` |
| 4 | `UserPromptExpansion` | typed command expands into prompt | Yes | top-level `decision: "block"` |
| 5 | `PreToolUse` | before tool call | Yes | `hookSpecificOutput.permissionDecision` (allow/deny/ask/defer) |
| 6 | `PermissionRequest` | permission dialog appears | Yes (denies permission on exit 2) | `hookSpecificOutput.decision.behavior` (allow/deny) |
| 7 | `PostToolUse` | tool call succeeds | No (shows stderr to Claude) | top-level `decision: "block"` |
| 8 | `PostToolUseFailure` | tool call fails | No | top-level `decision: "block"` |
| 9 | `PostToolBatch` | full batch of parallel tool calls resolves | Yes (stops loop before next model call) | top-level `decision: "block"` |
| 10 | `PermissionDenied` | auto-mode classifier denies tool call | No (denial already happened) | `hookSpecificOutput.retry: true` |
| 11 | `Notification` | Claude Code emits notification | No | none |
| 12 | `SubagentStart` | subagent spawned | No | none |
| 13 | `SubagentStop` | subagent finishes | Yes (prevents stop) | top-level `decision: "block"` |
| 14 | `TaskCreated` | `TaskCreate` is invoked | Yes (rolls back creation) | exit 2 or `continue: false` |
| 15 | `TaskCompleted` | task is being marked completed | Yes | exit 2 or `continue: false` |
| 16 | `Stop` | Claude finishes responding | Yes (prevents stop) | top-level `decision: "block"` |
| 17 | `StopFailure` | turn ends due to API error | No (output ignored) | none |
| 18 | `TeammateIdle` | agent-team teammate about to go idle | Yes | exit 2 or `continue: false` |
| 19 | `ConfigChange` | configuration file changes during session | Yes (except `policy_settings`) | top-level `decision: "block"` |
| 20 | `CwdChanged` | working dir changes (e.g., `cd`) | No | none (designed for direnv) |
| 21 | `FileChanged` | watched file changes on disk | No | none (matcher = filenames) |
| 22 | `WorktreeCreate` | worktree being created (`--worktree` / `isolation: "worktree"`) | Yes (any non-zero exit aborts) | command prints path on stdout; HTTP returns `hookSpecificOutput.worktreePath` |
| 23 | `WorktreeRemove` | worktree being removed | No (failures debug-only) | none |
| 24 | `PreCompact` | before compaction | Yes | top-level `decision: "block"` |
| 25 | `PostCompact` | after compaction completes | No | none |
| 26 | `Elicitation` | MCP server requests user input mid-tool-call | Yes (denies elicitation) | `hookSpecificOutput.action` (accept/decline/cancel) + `content` |
| 27 | `ElicitationResult` | after user responds to MCP elicitation, before sending back | Yes (becomes decline) | `hookSpecificOutput.action` + `content` |
| 28 | `SessionEnd` | session terminates | No | none |

(Plus `Setup` from CHANGELOG v2.1.10, not yet a section in the reference page.)

## Handler types

Verbatim from `### Hook handler fields → Common fields` (lines 283–287):

- `type: "command"` — runs a shell command; stdin = JSON, stdout/stderr/exit-code communicate result.
- `type: "http"` — POSTs JSON to a URL; response body uses the same JSON output schema as command hooks.
- `type: "mcp_tool"` — calls a tool on a connected MCP server; tool's text output treated as command-hook stdout.
- `type: "prompt"` — sends prompt to a Claude model for single-turn yes/no evaluation. Returns JSON.
- `type: "agent"` — spawns a subagent that can use Read/Grep/Glob to verify conditions before deciding. Marked **experimental** in the docs.

The corpus's "command|http|mcp_tool|prompt|agent" string is exactly correct. Note that not all events accept all handler types — `SessionStart` is documented as supporting only `command` and `mcp_tool` (line 731: "Only `type: "command"` and `type: "mcp_tool"` hooks are supported").

settings.json schema (canonical shape, from live docs):

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<string|regex|*>",
        "hooks": [
          {
            "type": "command|http|mcp_tool|prompt|agent",
            "if": "<permission-rule-syntax>",
            "command": "<shell command>",
            "timeout": 600,
            "once": true
          }
        ]
      }
    ]
  },
  "disableAllHooks": true
}
```

The `if` field uses permission-rule syntax (e.g., `Bash(git *)`) and was added in CHANGELOG v2.1.85. `once: true` was added in v2.1.0. `disableAllHooks` was added at CHANGELOG line 2778 (v1.0-era).

## Blocking semantics

Two paths are mutually exclusive — pick one per hook handler:

**Path A: exit codes only.**

- `exit 0` — success. For `UserPromptSubmit`, `UserPromptExpansion`, and `SessionStart`, stdout is added as model-visible context. For all other events, stdout goes to the debug log only.
- `exit 2` — blocking error. stderr is fed back to Claude as feedback. The effect is event-specific (table at lines 584–613 of the markdown).
- Any other exit code — non-blocking error; transcript shows `<hook> hook error` + first line of stderr; execution continues.
- **Exception:** `WorktreeCreate` treats *any* non-zero exit as abort.

**Path B: exit 0 + JSON on stdout.**

Universal fields:

- `continue` (default `true`) — `false` stops Claude entirely after the hook, takes precedence over event-specific decisions.
- `stopReason` — message shown to user when `continue: false`.
- `suppressOutput` — omits stdout from debug log.
- `systemMessage` — warning shown to user.

Event-specific decision shape (from the `Decision control` table, lines 662–672):

| Pattern | Events | Field shape |
|---|---|---|
| top-level `decision` | UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | `{ "decision": "block", "reason": "..." }` (only valid value: `"block"`) |
| exit-or-continue | TeammateIdle, TaskCreated, TaskCompleted | exit 2 OR `{"continue": false, "stopReason": "..."}` |
| `hookSpecificOutput.permissionDecision` | PreToolUse | values `allow`, `deny`, `ask`, `defer`; plus `permissionDecisionReason` and optional `updatedInput` |
| `hookSpecificOutput.decision.behavior` | PermissionRequest | `allow` or `deny`; can include `updatedInput` and permission update entries |
| `hookSpecificOutput.retry` | PermissionDenied | `retry: true` tells the model it may retry the denied tool call |
| path return | WorktreeCreate | command hook prints path; HTTP returns `hookSpecificOutput.worktreePath` |
| `hookSpecificOutput.action` + `content` | Elicitation, ElicitationResult | `action` ∈ {accept, decline, cancel} |
| no decision | WorktreeRemove, Notification, SessionEnd, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged | side-effect-only |

The corpus claim of `permissionDecision: "deny"` is therefore **correct only inside the `hookSpecificOutput` envelope and only for `PreToolUse`**. Verbatim from the canonical example (lines 88–95):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

HTTP-handler blocking is via response body only — non-2xx and connection failures are non-blocking. To deny via HTTP, return `2xx` with the JSON decision.

## Version history (when count grew)

Mapping CHANGELOG entries to the version that introduced each event:

| Event | Introduced in | Notes |
|---|---|---|
| `PreCompact` | v1.0.48 | "Added a PreCompact hook" |
| `UserPromptSubmit` | v1.0.54 | also added `cwd` to common input |
| `SessionStart` | v1.0.62 | "for new session initialization" |
| `SessionEnd` | v1.0.85 | systemMessage support added v1.0.112 |
| `Stop` / `SubagentStop` (split) | early v1.0.x | (line 2919: "Split Stop hook triggering into Stop and SubagentStop") |
| Prompt-based stop hooks | v2.0.30 | Added |
| `SubagentStart` | v2.0.43 | Added |
| `PermissionRequest` | v2.0.45 | "automatically approve or deny tool permission requests" |
| Plugin system + plugin hooks | v2.0.x (line 2517) | "Plugin System Released" |
| `prompt` and `agent` handler types | v2.1.0 | "from plugins (previously only command hooks were supported)"; `once: true` also v2.1.0; agent/skill frontmatter hooks added same release |
| `Setup` event | v2.1.10 | `--init`/`--maintenance` modes |
| `TeammateIdle`, `TaskCompleted` | v2.1.33 | "for multi-agent workflows" |
| `ConfigChange` | v2.1.49 | "fires when configuration files change during a session" |
| `WorktreeCreate`, `WorktreeRemove` | v2.1.50 | "custom VCS setup and teardown" |
| HTTP handler type | v2.1.63 | "POST JSON to a URL and receive JSON" |
| `InstructionsLoaded` | v2.1.69 | CLAUDE.md / rules loading |
| `Elicitation`, `ElicitationResult` | v2.1.76 | MCP user-input interception |
| `PostCompact` | v2.1.76 | Added |
| `StopFailure` | v2.1.78 | "fires when the turn ends due to an API error" |
| `CwdChanged`, `FileChanged` | v2.1.83 | "for reactive environment management (e.g., direnv)" |
| `TaskCreated` | v2.1.84 | "fires when a task is created via `TaskCreate`" |
| `if` conditional field | v2.1.85 | permission-rule-syntax filter |
| `PermissionDenied` | v2.1.89 | auto-mode-denial post-hook with `{retry: true}` |
| `PreToolUse` `defer` decision | v2.1.89 | fourth permissionDecision value |
| `mcp_tool` handler type | (CHANGELOG line 62, recent v2.1.x) | "Hooks can now invoke MCP tools directly via `type: "mcp_tool"`" |

So the timeline is: ~7 events at v1.0 launch → ~9 by v1.0.85 (`SessionEnd`) → ~12 by v2.0.45 (`PermissionRequest`) → 18 by v2.1.50 (worktree events) → 28 by v2.1.84–v2.1.89 (`TaskCreated` + `PermissionDenied`). The hook contract has been the single most-iterated surface in the Claude Code product over the last twelve months.

## Resolution against corpus contradictions

1. **"8 events vs 28 events" — both with `[OFFICIAL — code.claude.com/docs/en/hooks]` citation.** Resolved: **28 is current as of 2026-04-26**, matching the live `## Hook events` section header count and lifecycle table. The 8-event figure is an obsolete snapshot from early v1.0 and should be retired from the corpus or annotated with a date stamp. Recommended corpus correction: replace the contested fact with "28 hook events documented at code.claude.com/docs/en/hooks (v2.1.119, accessed 2026-04-26); the contract has grown roughly fourfold since v1.0 and continues to add events most minor releases."

2. **`permissionDecision: "deny"` JSON shape.** Resolved: the value is correct, but the field lives at `hookSpecificOutput.permissionDecision`, not at the top level. Valid values are `allow`, `deny`, `ask`, `defer` — the `defer` value is the most recent addition (v2.1.89). Sibling fields are `hookEventName: "PreToolUse"` (required) and `permissionDecisionReason` (optional human-readable reason injected into stderr feedback). `PermissionRequest` uses a *different* shape: `hookSpecificOutput.decision.behavior` with values `allow`/`deny`. Mixing the two shapes is a common bug — the `if` filter and the JSON envelope should both be specified per-event.

3. **Handler types `command|http|mcp_tool|prompt|agent`.** Resolved: **all five are correct and documented as canonical**. They appear in the `Common fields` bullets and in the live JSON examples. `prompt` and `agent` are LLM-evaluated (used for "judgment rather than deterministic rules" — verbatim from line 11 of the guide). `agent` is flagged experimental. `prompt` and `agent` were originally restricted to plugin hooks and were generalized in v2.1.0.

## Sources

- `https://code.claude.com/docs/en/hooks` (canonical reference; markdown variant `https://code.claude.com/docs/en/hooks.md`, 155,864 bytes, 2,549 lines, fetched 2026-04-26)
- `https://code.claude.com/docs/en/hooks-guide` (companion quickstart)
- `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md` (3,285 lines spanning v1.0.x through v2.1.119, fetched 2026-04-26 via raw.githubusercontent.com)
- `https://docs.claude.com/en/docs/claude-code/hooks` and `/hooks-reference` — both confirmed as 301 redirects, latter now 404 (consolidated into `/docs/en/hooks`)
