---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Hook/automation parity across agents — what each of Claude Code, OpenCode, Codex, Gemini CLI, Goose, ForgeCode offers for automated behavior on events, plus fallback patterns where parity is impossible."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# Hook / Automation Parity Across Six Agents

## Inline Summary

The biggest portability blocker is **PreToolUse blocking semantics**: Claude Code, Codex, OpenCode, and Gemini all have a pre-tool hook that can deny execution, but their JSON contracts differ in field names (`permissionDecision` vs `decision: deny` vs throwing an exception), and Goose / ForgeCode have **no pre-tool gate at all** — only retry-after-the-fact. The second-biggest blocker is **`UserPromptSubmit`**, which Claude Code and Codex support natively, Gemini approximates with `BeforeAgent`, and OpenCode/Goose/ForgeCode lack entirely; the most reliable cross-agent fallback is to **inject context through the static instructions file** (`AGENTS.md`, `GEMINI.md`, `.goosehints`, or `AGENTS.md` for ForgeCode) which is reread on every session start. For post-action enforcement, every agent except ForgeCode can run a post-tool script; the universal fallback is `git` pre-commit hooks plus CI-side validators that fire regardless of which agent produced the diff.

---

## 1. Claude Code — Hook Contract Baseline (April 2026)

Claude Code currently exposes **28 hook events** [OFFICIAL — code.claude.com/docs/en/hooks]. The set has grown substantially from the original 9-event lineup; nearly every state transition in the agentic loop is now interceptable.

### 1.1 Event Catalogue

Categorized by where they fire in the loop [OFFICIAL]:

- **Session lifecycle**: `SessionStart` (matchers: `startup|resume|clear|compact`), `SessionEnd`, `InstructionsLoaded` (fires when CLAUDE.md / `.claude/rules/*.md` are read)
- **User input**: `UserPromptSubmit` (no matcher, can block), `UserPromptExpansion` (fires on slash-command / skill expansion before reaching the model)
- **Tool lifecycle**: `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`
- **Agent loop**: `SubagentStart`, `SubagentStop`, `Stop`, `StopFailure`
- **Team coordination**: `TeammateIdle`, `TaskCreated`, `TaskCompleted`
- **Config / environment**: `ConfigChange`, `CwdChanged`, `FileChanged`
- **Worktree**: `WorktreeCreate` (can block), `WorktreeRemove`
- **Compaction**: `PreCompact`, `PostCompact`
- **MCP elicitation**: `Elicitation`, `ElicitationResult`
- **Notification**: `Notification` (observe-only)

### 1.2 Configuration Schema

Hooks are declared in `settings.json` at four scopes — `~/.claude/settings.json` (user), `.claude/settings.json` (project, committed), `.claude/settings.local.json` (project, gitignored), and managed-policy (org admin) [OFFICIAL]. Plugins can also bundle a `hooks/hooks.json`, and skills/agents can declare hooks in YAML frontmatter with `once: true` semantics.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh",
            "timeout": 600
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint.sh" }
        ]
      }
    ]
  }
}
```

Beyond `type: command`, Claude Code supports `type: http` (POST JSON to a URL, expect 2xx + JSON decision), `type: mcp_tool` (call a registered MCP tool), `type: prompt` (delegate the decision to a model invocation), and `type: agent` (spawn a subagent to verify) [OFFICIAL — code.claude.com/docs/en/hooks].

### 1.3 Inputs / Outputs / Blocking

Every hook receives JSON on stdin including `session_id`, `transcript_path`, `cwd`, `permission_mode`, and `hook_event_name`. Tool events add `tool_name`, `tool_input`, `tool_use_id`; post-events add `tool_response` and `duration_ms`.

Exit codes are the universal kill-switch [OFFICIAL]:
- `0` — success; stdout parsed as JSON if valid, otherwise added as context (for events that accept context injection)
- `1` — non-blocking error (transcript shows first stderr line)
- `2` — **blocking** error; stderr fed back to Claude
- Other — treated like `1`

`PreToolUse` is the only event using `permissionDecision` (`allow|deny|ask|defer`); all other blocking events use `decision: "block"` with a `reason`. Real example — denying `rm -rf` [PRAC — disler/claude-code-hooks-mastery]:

```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command')
if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:"Destructive rm -rf blocked by policy"}}'
fi
exit 0
```

A common post-edit linter [PRAC — affaan-m/everything-claude-code]:

```bash
#!/bin/bash
FILE=$(jq -r '.tool_input.file_path')
case "$FILE" in
  *.ts|*.tsx) bunx eslint --fix "$FILE" ;;
  *.py) ruff check --fix "$FILE" ;;
esac
```

Critical subtlety: **exit 1 does not block** — only exit 2 (or a JSON `permissionDecision: "deny"` for PreToolUse) actually halts the action [OFFICIAL]. Many practitioners get this wrong on first attempt.

---

## 2. OpenCode — Plugin-Based Hooks

OpenCode's extensibility surface is a **TypeScript/JavaScript plugin SDK**, not a JSON config [OFFICIAL — opencode.ai/docs/plugins]. A plugin is a module that exports a `Plugin` function returning a hooks object.

### 2.1 Event Catalogue [OFFICIAL]

- **Tool**: `tool.execute.before`, `tool.execute.after`
- **Session**: `session.created`, `session.compacted`, `session.deleted`, `session.idle`, `session.status`, `session.updated`, `session.error`
- **Message**: `message.part.removed/updated`, `message.removed/updated`
- **Permission**: `permission.asked`, `permission.replied`, `permission.updated`
- **Files**: `file.edited`, `file.watcher.updated`
- **LSP**: `lsp.client.diagnostics`, `lsp.updated`
- **Special**: `stop` (intercept agent termination), `experimental.chat.system.transform` (mutate system prompt), `experimental.session.compacting` (control compaction behavior), `shell.env` (inject env vars into child processes), `command.executed`, `tui.prompt.append`, `installation.updated`

### 2.2 Configuration

`.opencode/opencode.json` lists plugins; the plugin file lives at `.opencode/plugin/*.ts` [OFFICIAL].

```json
{ "$schema": "https://opencode.ai/config.json", "plugin": ["./plugin/security.ts"] }
```

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const Security: Plugin = async ({ client, project, $ }) => ({
  "tool.execute.before": async (input, output) => {
    if (input.tool === "bash" && output.args.command.includes("rm -rf")) {
      throw new Error("Dangerous command blocked")
    }
  },
  "tool.execute.after": async (input) => {
    if (input.tool === "edit" && input.args.filePath.endsWith(".rs")) {
      await $`cargo fmt`
    }
  },
  "experimental.chat.system.transform": async (input, output) => {
    output.system.push("<rules>Always run tests after edits.</rules>")
  }
})
```

### 2.3 Blocking Semantics

Blocking is by **thrown exception**, not exit code or JSON decision [OFFICIAL]. `tool.execute.before` blocks tool execution; `stop` can re-prompt the agent to continue work via `client.session.prompt({...})`.

### 2.4 Gaps vs Claude Code

OpenCode lacks direct equivalents for `UserPromptSubmit`, `PreToolUse` matcher patterns (matching is done in plugin code), `Stop` decision blocking with `decision: "block"` JSON, `SubagentStart/Stop`, `PreCompact` (only `experimental.session.compacting`), `Notification`, and the rich permission-request decision tree [PRAC — gist by zeke comparing the two].

A community compatibility layer, **oh-my-opencode** (`createClaudeCodeHooksHook()`), reads `~/.claude/settings.json` and adapts `PreToolUse → tool.execute.before`, `PostToolUse → tool.execute.after`, etc., though there's an open bug where hooks fail to execute reliably [PRAC — code-yeongyu/oh-my-openagent issue #1707]. There's also an unmerged native-compat issue (#12472) requesting first-class Claude Code hook support [OFFICIAL — anomalyco/opencode#12472].

A documented limitation is that **plugin hooks cannot inject AI-visible messages into conversation context** (only into system prompt via `experimental.chat.system.transform`), making it impossible to build skills that require ongoing behavioral enforcement after each turn [OFFICIAL — anomalyco/opencode#17412].

---

## 3. Codex CLI (OpenAI) — Closest Claude Parity

Codex CLI shipped a hook system in late 2025 that was **stabilized in early 2026** and is now the closest hook contract to Claude Code's by design [OFFICIAL — developers.openai.com/codex/hooks].

### 3.1 Event Catalogue [OFFICIAL]

- `SessionStart` (matchers: `startup|resume|clear`)
- `PreToolUse` (matchers: tool name, regex)
- `PermissionRequest` (matchers: tool name)
- `PostToolUse` (matchers: tool name)
- `UserPromptSubmit` (no matcher)
- `Stop` (no matcher)

That's it — six events. No `SessionEnd`, `SubagentStop`, `PreCompact`, `Notification`, or `InstructionsLoaded`.

### 3.2 Configuration

Hooks are gated behind a feature flag and live in either `hooks.json` or inline `[hooks]` tables in `config.toml`. Both `~/.codex/` (user) and `<repo>/.codex/` (project) layers merge — higher precedence does **not** replace lower [OFFICIAL]. There's also an enterprise `requirements.toml` with `managed_dir` for org-controlled hooks.

```toml
[features]
codex_hooks = true

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "/usr/bin/python3 $(git rev-parse --show-toplevel)/.codex/hooks/block_secrets.py"
statusMessage = "Scanning for secrets"
timeout = 10
```

### 3.3 Inputs / Outputs / Blocking

Codex deliberately mirrors Claude Code's JSON shape, including `hookSpecificOutput.permissionDecision: "deny"` for `PreToolUse` and `decision: "block"` for `PostToolUse` / `UserPromptSubmit` / `Stop` [OFFICIAL]. Exit codes match: `0` success, `2` blocking failure with stderr as reason. Default timeout is 600s.

Real example — secret scanner for Bash commands [OFFICIAL]:

```python
import json, sys, re
hook_input = json.load(sys.stdin)
command = hook_input.get("tool_input", {}).get("command", "")
for pat in [r"sk_live_\w+", r"sk-\w{20,}", r"ghp_\w{36}"]:
  if re.search(pat, command):
    print(json.dumps({"hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Secret detected"}}))
    sys.exit(0)
sys.exit(0)
```

### 3.4 Known Issues

`ApplyPatchHandler` does NOT emit `PreToolUse`/`PostToolUse` — hooks only fire for `Bash` reliably; file-edit interception is a known gap [OFFICIAL — openai/codex#16732]. There's also a 0.124.0 startup crash when `codex_hooks` is enabled with certain config shapes [OFFICIAL — openai/codex#19199].

### 3.5 Gaps vs Claude Code

No `SubagentStart/Stop`, `PreCompact`, `Notification`, `WorktreeCreate`, or matcher patterns for prompt-event sources. No `type: prompt` or `type: agent` hook handlers — only `command`. No skill/agent frontmatter hooks.

---

## 4. Gemini CLI — Hooks v0.26+

Gemini CLI adopted a hook system in v0.26.0 (early 2026) [OFFICIAL — geminicli.com/docs/hooks]. The taxonomy is **slightly different** from Claude/Codex and uses `Before/After` naming.

### 4.1 Event Catalogue [OFFICIAL]

- **Tool**: `BeforeTool`, `AfterTool`
- **Agent**: `BeforeAgent` (after user input, before planning), `AfterAgent` (after final model response)
- **Model**: `BeforeModel`, `BeforeToolSelection`, `AfterModel` (per-chunk!)
- **Lifecycle**: `SessionStart`, `SessionEnd`, `Notification`, `PreCompress`

Notable: `AfterModel` fires on **every response chunk**, enabling streaming redaction. `BeforeAgent` is the closest analogue to `UserPromptSubmit` but fires after planning prep.

### 4.2 Configuration

`settings.json` at project (`.gemini/settings.json`) and user (`~/.gemini/settings.json`) scopes [OFFICIAL].

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "read_.*",
        "sequential": false,
        "hooks": [
          { "type": "command", "command": "validate-file-access.sh", "timeout": 5000 }
        ]
      }
    ],
    "SessionStart": [
      { "matcher": "startup",
        "hooks": [{ "type": "command", "command": "load-context.sh" }]}
    ]
  }
}
```

### 4.3 Inputs / Outputs / Blocking

JSON on stdin; JSON on stdout; stderr for logs. Exit codes: `0` success, `2` system block (stderr is rejection reason), other = warning. Blocking uses `decision: "deny"` (not Claude's `permissionDecision`). Across `BeforeAgent`, `BeforeModel`, `BeforeTool`, `AfterTool`, `AfterModel`, `AfterAgent` — each can return `decision: "deny"` to block its respective stage [OFFICIAL].

### 4.4 Gaps vs Claude Code

No `UserPromptSubmit` (use `BeforeAgent` instead — fires later), no `Stop` decision-block (use `AfterAgent`), no `SubagentStart/Stop`, no `PermissionRequest`, no `WorktreeCreate`, no skill-frontmatter hooks. Field name `decision: "deny"` vs Claude's `permissionDecision: "deny"` makes JSON outputs non-portable.

---

## 5. Goose (AAIF / Linux Foundation) — No Hooks, Recipe Validators Only

Goose has **no hook system** [UNVERIFIED — exhaustive search of goose-docs.ai and block.github.io/goose returned no event/hook documentation]. The closest extension points:

### 5.1 Recipes [OFFICIAL — block/goose recipe-reference]

Recipes are YAML configs that bundle instructions, parameters, extensions (MCP servers), `response` schema validation, sub-recipes, and a `retry` block. The retry block is the closest thing to a post-tool hook:

```yaml
retry:
  max_retries: 3
  checks:
    - type: shell
      command: "test -f output.txt"
    - type: file_exists
      path: "build/output.bin"
    - type: file_content
      path: "report.md"
      pattern: "PASS"
  on_failure: "rm -f temp_files*"
```

Checks are evaluated **after the entire recipe runs**, not per-tool. `on_failure` is a cleanup command between attempts. There is no per-tool gate, no pre-prompt hook, no session-start hook in the Claude Code sense [OFFICIAL — DeepWiki block/goose 4.1.4].

### 5.2 Extensions [OFFICIAL]

Goose extensions are MCP servers. The "lifecycle" of an extension is just MCP server start/stop — there's no callback when the agent uses one of its tools. Custom toolkits can load additional context into the system prompt, but only at extension-load time, not per-event.

### 5.3 .goosehints [OFFICIAL — dev.to/lymah/using-goosehints]

`.goosehints` is the static instruction file. Locations: `~/.config/goose/.goosehints` (user), `~/.goosehints` (home), `<project>/.goosehints` (project). Contents are appended to the system prompt on every request — so it's reread per conversation, not per turn. It is **not** a hook, but the only mechanism for cross-session behavioral enforcement.

### 5.4 Implications

Goose is the most parity-poor agent in this set. To enforce policy you must either (a) wrap tools as MCP servers that self-validate, (b) rely on `retry` checks after the fact, or (c) write extensive instructions into `.goosehints`.

---

## 6. ForgeCode — No Hook System Documented

ForgeCode (antinomyhq/forgecode, the Rust-based "harness") has no documented hook system as of April 2026 [OFFICIAL — forgecode.dev/docs and github.com/antinomyhq/forgecode]. Extension points are entirely declarative:

- **Skills**: `.forge/skills/<name>/SKILL.md` with YAML frontmatter
- **Agents**: `.forge/agents/*.md` with frontmatter (model, tools, system prompt)
- **Commands**: `.forge/commands/*.yaml` (shortcut commands invoked via `:name`)
- **AGENTS.md**: project-root persistent instructions; `~/forge/AGENTS.md` global
- **forge.yaml**: `model`, `temperature`, `max_walker_depth`, `max_tool_failure_per_turn`, `max_requests_per_turn`, `custom_rules`, `commands`

There's no PreToolUse/PostToolUse/SessionStart hook concept exposed to users [OFFICIAL — github.com/antinomyhq/forgecode tree].

(Aside: a separate project named "claude-forge" by sangrokjung does ship 15+ Claude Code hooks bundled as a marketplace plugin, but that's a Claude Code add-on, not a ForgeCode feature [PRAC — github.com/sangrokjung/claude-forge].)

ForgeCode's terminal-bench wins come from harness engineering (parallel walkers, stricter tool budgets), not hooks. There is open community demand — cmux issue #2777 specifically requests "ForgeCode-style agent integration for sidebar metadata + notifications" — implying the integration surface is currently signal-poor [PRAC — manaflow-ai/cmux#2777].

---

## 7. Parity Matrix

Legend: ✅ native, ◐ partial / different shape, ❌ none, 📄 fallback via static instructions only.

| Capability                              | Claude Code | OpenCode | Codex | Gemini CLI | Goose | ForgeCode |
|------------------------------------------|:--:|:--:|:--:|:--:|:--:|:--:|
| **Pre-tool observe**                     | ✅ PreToolUse | ✅ tool.execute.before | ✅ PreToolUse | ✅ BeforeTool | ❌ | ❌ |
| **Pre-tool BLOCK**                       | ✅ permissionDecision | ✅ throw Error | ✅ permissionDecision | ✅ decision:deny | ❌ | ❌ |
| **Post-tool observe**                    | ✅ PostToolUse | ✅ tool.execute.after | ✅ PostToolUse | ✅ AfterTool | ◐ retry-only | ❌ |
| **Post-tool block / re-feedback**        | ✅ decision:block | ◐ no native block | ✅ decision:block | ✅ decision:deny | ❌ | ❌ |
| **UserPromptSubmit BLOCK + inject**      | ✅ | ❌ | ✅ | ◐ BeforeAgent | ❌ | ❌ |
| **SessionStart context injection**       | ✅ stdout→context | ◐ session.created (no inject) | ✅ stdout→context | ✅ stdout→context | 📄 .goosehints | 📄 AGENTS.md |
| **SessionEnd**                           | ✅ | ✅ session.deleted | ❌ | ✅ | ❌ | ❌ |
| **Stop / continue-loop**                 | ✅ | ✅ stop hook | ✅ | ◐ AfterAgent continue:false | ◐ retry-only | ❌ |
| **SubagentStart/Stop**                   | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **PreCompact / compaction control**      | ✅ | ◐ experimental.session.compacting | ❌ | ✅ PreCompress | ❌ | ❌ |
| **Notification observe**                 | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **PermissionRequest / dialog hook**      | ✅ | ✅ permission.asked | ✅ | ❌ | ❌ | ❌ |
| **System-prompt mutation**               | ◐ via SessionStart context | ✅ experimental.chat.system.transform | ❌ | ✅ BeforeModel | 📄 .goosehints | 📄 AGENTS.md |
| **HTTP / MCP-tool hook handlers**        | ✅ command/http/mcp_tool/prompt/agent | ◐ in-plugin only | ◐ command only | ◐ command only | ❌ | ❌ |
| **Frontmatter hooks (skill/agent)**      | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Matcher patterns (regex/glob)**        | ✅ | ◐ in-code if/else | ✅ | ✅ | ❌ | ❌ |
| **Org-managed/policy hooks**             | ✅ managed settings | ❌ | ✅ requirements.toml | ❌ | ❌ | ❌ |

---

## 8. Fallback Patterns When Hooks Are Absent

Real projects on Goose, ForgeCode, and partial-parity OpenCode/Gemini converge on the same handful of fallbacks.

### 8.1 Static-Instruction Context Injection (Replaces SessionStart + UserPromptSubmit)

Every modern coding agent reads a static markdown file on every session start:

| Agent | File(s) | Reload Behavior |
|---|---|---|
| Claude Code | `CLAUDE.md` (project), `~/.claude/CLAUDE.md` (user) | Per-session; `InstructionsLoaded` hook fires |
| OpenCode | `AGENTS.md` (project), `~/.config/opencode/AGENTS.md`; falls back to `CLAUDE.md` | Per-session [OFFICIAL — opencode.ai/docs/rules] |
| Codex | `AGENTS.md`, `AGENTS.override.md`, `TEAM_GUIDE.md`, `.agents.md` (in precedence order; chained directory walk) | **Per-run / per-TUI-launch only** — modifications mid-session are NOT picked up; `/init` or restart required [OFFICIAL — openai/codex#3198, #8547] |
| Gemini CLI | `GEMINI.md` (hierarchical: global / project root / subdirectory) | Per-launch; `/memory refresh` reloads in-session [OFFICIAL] |
| Goose | `.goosehints` (project, home, subdir) | Reread per request — every line ships with every prompt [OFFICIAL] |
| ForgeCode | `AGENTS.md` (project, `~/forge/AGENTS.md` global) | Per-launch [OFFICIAL] |

**Fallback pattern**: Move per-session context injection out of hooks and into `AGENTS.md`. Codex's "rebuild instruction chain on every run" semantics make this reliable for all six agents — at the cost of context-window bloat. The rule of thumb from goose practitioners is "if `.goosehints` is too big, it pushes out important context" [PRAC — dev.to/blockopensource/whats-in-my-goosehints-file]. Same applies to all agents — keep the file lean.

### 8.2 Pre-Commit Git Hooks (Replaces PostToolUse Linter Enforcement)

Where PostToolUse can't run (Goose, ForgeCode, OpenCode without plugin work), projects fall back to `pre-commit` framework or husky:

```yaml
# .pre-commit-config.yaml — runs regardless of which agent edited
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks: [{ id: ruff-format }, { id: ruff }]
  - repo: local
    hooks:
      - id: secret-scan
        name: scan staged for secrets
        entry: ./scripts/scan-secrets.sh
        language: system
```

This is the dominant pattern in Goose-using shops because Goose has zero pre-action interception. It sacrifices "block at edit time" for "block at commit time" but is fully agent-agnostic.

### 8.3 MCP Tool Wrapping (Replaces PreToolUse Validation)

When a target agent has no PreToolUse hook (Goose, ForgeCode), wrap dangerous capabilities as a custom MCP server that performs validation **inside** the tool implementation. Goose explicitly recommends this pattern — "extensions expose their capabilities through Tools and maintain their own state" [OFFICIAL — goose-docs.ai extensions design]. Block engineering's red-team blog post on Goose recommends MCP-side validation as the primary security posture because "the system prompt is the most reliable attack surface" — meaning: don't trust prompt-level rules, enforce in the tool [PRAC — engineering.block.xyz/blog/how-we-red-teamed-our-own-ai-agent].

Concrete pattern: replace direct shell access with `mcp-safe-shell` that validates commands against an allowlist before execution. This is portable across all agents that speak MCP (all six in this matrix do).

### 8.4 Tripwire Tool Definitions (Cross-Agent Pattern)

A community pattern (popularized by Owen Fox's Claude Code guide and replicated in OpenCode/Goose) defines a "honeypot" tool whose mere invocation indicates the agent went off-rails [PRAC — ofox.ai/blog/claude-code-hooks-subagents-skills-complete-guide-2026]. The tool's implementation logs and aborts. Works in any MCP-capable agent. Drawback: relies on the model not calling the tripwire — purely observational.

### 8.5 Polling / Watch Processes

For agents without `FileChanged` (Codex, Gemini, Goose, ForgeCode), real projects run `entr`, `watchexec`, or `chokidar`-based watchers in a side terminal:

```bash
watchexec --exts py,ts -- bash -c './scripts/lint-changed.sh && ./scripts/test-related.sh'
```

This is fully agent-agnostic and is the standard pattern in monorepos that mix Claude Code + Goose + Cursor in one team [PRAC — multiple practitioner blogs].

### 8.6 LSP / IDE-Side Enforcement

Diagnostics-on-edit (the `lsp.client.diagnostics` event in OpenCode, none equivalent elsewhere) can be replaced with LSP itself: configure the language server's `--fix-on-save` and rely on `Edit`/`Write` triggering an in-IDE recompile. Cursor and JetBrains AI use this pattern heavily because their IDEs already host the LSP. Limitation: headless agent runs (Codex CLI, Goose recipes in CI) bypass LSP.

### 8.7 System-Prompt Tripwires (UserPromptSubmit Fallback)

Where `UserPromptSubmit` doesn't exist (OpenCode, Goose, ForgeCode), the fallback is to put strong "if X then Y" instructions in the static instructions file. This is unreliable — depends on model adherence — but it's the only option without writing a wrapper CLI. Common pattern in `.goosehints`:

```
RULE: Before any destructive action (rm, drop table, delete), state the action
in plain English and wait for explicit confirmation. If the user has not
confirmed in this turn, refuse and ask.
```

This is explicitly weaker than a hook because the model can ignore it; Block's red-team paper documents how `.goosehints`-style instructions were bypassed by prompt-injected recipes [PRAC — engineering.block.xyz red-team post].

### 8.8 Wrapper CLI / Proxy Process

For zero-hook agents (ForgeCode, Goose), the most aggressive fallback is to wrap the agent itself in a parent process (`expect`, `tmux pipe-pane`, custom Rust wrapper) that intercepts stdout for tool-call markers and stdin for prompts. Used by tools like `cmux`, `ccmanager`, and `claude-mem` [PRAC — github.com/kbwo/ccmanager, github.com/thedotmack/claude-mem]. High implementation cost, but provides full observability across any agent.

---

## 9. Recommendations for Cross-Agent Practice Modules

For Momentum or any practice module targeting multiple agents:

1. **Treat Claude Code as the only "rich" hook target.** Codex is close but lacks SubagentStop and InstructionsLoaded; assume parity for the six events Codex supports and degrade gracefully for the rest.
2. **Make `AGENTS.md` (or per-agent equivalent) the authoritative session-start mechanism**, not SessionStart hooks. Symlink or generate `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.goosehints` from one source.
3. **For hard policy enforcement, use MCP tool wrapping** — it's the only mechanism portable to Goose and ForgeCode and works for all six agents.
4. **Keep pre-commit hooks as the universal post-action backstop.** Don't rely on agent-specific PostToolUse for anything that must not ship.
5. **Skip `UserPromptSubmit` portability entirely.** The capability is unique enough that targeting it across agents requires a wrapper CLI; treat it as a Claude-Code-only enhancement.
6. **For OpenCode**, write a single TypeScript plugin that maps a Claude-Code-shaped settings.json into plugin hooks (mirror the oh-my-opencode pattern, but ship it in your plugin rather than relying on theirs).

---

## Sources

- [Claude Code Hooks reference (code.claude.com/docs/en/hooks)](https://code.claude.com/docs/en/hooks) [OFFICIAL]
- [Claude Code Hooks guide (code.claude.com/docs/en/hooks-guide)](https://code.claude.com/docs/en/hooks-guide) [OFFICIAL]
- [Claude Code settings.md](https://docs.claude.com/en/docs/claude-code/settings.md) [OFFICIAL]
- [OpenCode Plugins docs](https://opencode.ai/docs/plugins/) [OFFICIAL]
- [OpenCode Permissions docs](https://opencode.ai/docs/permissions/) [OFFICIAL]
- [OpenCode Rules docs](https://opencode.ai/docs/rules/) [OFFICIAL]
- [OpenCode Native Claude Code hooks compatibility issue #12472](https://github.com/anomalyco/opencode/issues/12472) [OFFICIAL]
- [OpenCode plugin AI-visible context limitation issue #17412](https://github.com/anomalyco/opencode/issues/17412) [OFFICIAL]
- [OpenCode ApplyPatchHandler hook gap issue #16732](https://github.com/openai/codex/issues/16732) [OFFICIAL]
- [OpenCode Plugin Development Guide gist (lindquist)](https://gist.github.com/johnlindquist/0adf1032b4e84942f3e1050aba3c5e4a) [PRAC]
- [OpenCode vs Claude Code Hooks comparison gist (zeke)](https://gist.github.com/zeke/1e0ba44eaddb16afa6edc91fec778935) [PRAC]
- [OpenCode plugin development blog (Lushbinary)](https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/) [PRAC]
- [Codex Hooks docs (developers.openai.com/codex/hooks)](https://developers.openai.com/codex/hooks) [OFFICIAL]
- [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) [OFFICIAL]
- [Codex Configuration Reference](https://developers.openai.com/codex/config-reference) [OFFICIAL]
- [Codex AGENTS.md reload issue #3198](https://github.com/openai/codex/issues/3198) [OFFICIAL]
- [Codex AGENTS.md auto-reread issue #8547](https://github.com/openai/codex/issues/8547) [OFFICIAL]
- [Codex hooks startup crash issue #19199](https://github.com/openai/codex/issues/19199) [OFFICIAL]
- [Gemini CLI Hooks reference (geminicli.com/docs/hooks/reference)](https://geminicli.com/docs/hooks/reference/) [OFFICIAL]
- [Gemini CLI Hooks index](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/index.md) [OFFICIAL]
- [Gemini CLI Memory Management tutorial](https://geminicli.com/docs/cli/tutorials/memory-management/) [OFFICIAL]
- [Gemini CLI GEMINI.md reload issue #10702](https://github.com/google-gemini/gemini-cli/issues/10702) [OFFICIAL]
- [Goose recipe-reference (block.github.io)](https://block.github.io/goose/docs/guides/recipes/recipe-reference/) [OFFICIAL]
- [Goose extensions design](https://block.github.io/goose/docs/goose-architecture/extensions-design/) [OFFICIAL]
- [Goose retry/validation deep dive (DeepWiki)](https://deepwiki.com/block/goose/4.1.4-subagents-and-tasks) [OFFICIAL]
- [.goosehints usage (dev.to/lymah)](https://dev.to/lymah/using-goosehints-files-with-goose-304m) [PRAC]
- [Goose .goosehints global-load bug #1765](https://github.com/block/goose/issues/1765) [OFFICIAL]
- [Block red-team Goose post](https://engineering.block.xyz/blog/how-we-red-teamed-our-own-ai-agent-) [PRAC]
- [ForgeCode docs (forgecode.dev)](https://forgecode.dev/) [OFFICIAL]
- [ForgeCode GitHub repository](https://github.com/antinomyhq/forgecode) [OFFICIAL]
- [ForgeCode tool guidelines](https://github.com/antinomyhq/forgecode/blob/main/docs/tool-guidelines.md) [OFFICIAL]
- [cmux integration request for ForgeCode #2777](https://github.com/manaflow-ai/cmux/issues/2777) [PRAC]
- [Claude Code hooks complete guide (claudefa.st)](https://claudefa.st/blog/tools/hooks/hooks-guide) [PRAC]
- [Claude Code hooks/subagents/skills guide (ofox.ai)](https://ofox.ai/blog/claude-code-hooks-subagents-skills-complete-guide-2026/) [PRAC]
- [GitButler Claude Code Hooks](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks) [PRAC]
- [disler/claude-code-hooks-mastery repo](https://github.com/disler/claude-code-hooks-mastery) [PRAC]
- [affaan-m/everything-claude-code hooks](https://github.com/affaan-m/everything-claude-code/tree/main/hooks) [PRAC]
- [oh-my-opencode Claude-Code-compatibility hooks bug #1707](https://github.com/code-yeongyu/oh-my-openagent/issues/1707) [OFFICIAL]
- [agents.md spec](https://agents.md/) [OFFICIAL]
- [DeployHQ AI coding config files guide](https://www.deployhq.com/blog/ai-coding-config-files-guide) [PRAC]
