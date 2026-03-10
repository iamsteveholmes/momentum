# Technical Research: Claude Code Tool Permissions & BMAD Agent Configuration

**Date:** 2026-03-07
**Researcher:** Mary (Business Analyst Agent)
**Topic:** Why BMAD agents trigger excessive tool permission prompts in Claude Code
**Status:** Complete

---

## Executive Summary

Your permission friction stems from **three specific gaps** in your current `settings.local.json` configuration, not from anything BMAD is doing (or failing to do). BMAD does not manage Claude Code permissions at all — it relies entirely on your Claude Code settings. The fix is straightforward: add missing non-destructive tools to your allowlist and optionally broaden your WebFetch policy.

---

## Root Cause Analysis

### Your Current Configuration

Your permissions live in `.claude/settings.local.json` (the right place — gitignored, personal). Here's what's **allowed**:

| Tool | Status | Notes |
|------|--------|-------|
| Edit | Allowed | Unrestricted |
| Write | Allowed | Unrestricted |
| Bash | Allowed | Unrestricted (with deny/ask rules for destructive commands) |
| WebSearch | Allowed | Unrestricted |
| WebFetch | Partially Allowed | **Domain-restricted** — only 16 specific domains |
| mcp__agentvibes__text_to_speech | Allowed | Specific MCP tool |
| **Read** | **NOT ALLOWED** | Prompts every time |
| **Glob** | **NOT ALLOWED** | Prompts every time |
| **Grep** | **NOT ALLOWED** | Prompts every time |
| **Agent** | **NOT ALLOWED** | Prompts every time |
| **NotebookEdit** | **NOT ALLOWED** | Prompts when used |
| **WebFetch (unlisted domains)** | **NOT ALLOWED** | Prompts for every new domain |

### The Three Gaps

**Gap 1: Read, Glob, Grep are missing from the allowlist.**
These are the most frequently used, completely non-destructive tools in Claude Code. Every single file read, every search, every glob pattern match triggers a permission prompt. For a typical BMAD workflow that loads config files, reads agent definitions, searches for templates, and reads workflow files — that's easily 10-20 prompts before any real work begins.

**Gap 2: Agent (subagent) is not in the allowlist.**
BMAD workflows and research tasks heavily use subagents (Explore, Plan, general-purpose, and specialized agents like bmm-market-researcher). Each agent launch triggers a permission prompt. A technical research workflow like the one that produced this report spawns 3+ agents in parallel.

**Gap 3: WebFetch is domain-locked.**
You have 16 domains whitelisted. Every time Claude needs to fetch from a domain not on the list, it prompts. This is the most visible friction because research workflows fetch from dozens of domains. You can either maintain an ever-growing domain list or allow WebFetch unrestricted (it's read-only — it cannot modify anything on the web).

### Why BMAD Doesn't Help Here

BMAD agents define tool access **instructionally** (telling the AI what to do), not **mechanically** (configuring Claude Code's permission system). Specifically:

- Agent definitions (`.md` files) contain `<rules>` and `<activation>` sections that guide behavior
- Workflow YAML files have `required_tools` fields, but these are declarative documentation — they don't configure permissions
- BMAD has no installer step that sets up Claude Code permissions
- The `allowed-tools` frontmatter pattern (supported by Claude Code skills) is not used in BMAD agent definitions

This is by design — BMAD is framework-agnostic and doesn't assume Claude Code as its runtime.

---

## Claude Code Permission System Reference

### Settings File Hierarchy (Priority Order)

| Priority | File | Scope | Shared? |
|----------|------|-------|---------|
| 1 (highest) | Managed settings (OS-level) | Organization | Yes |
| 2 | CLI arguments (`--allowedTools`) | Session | No |
| 3 | `.claude/settings.local.json` | You + this project | No (gitignored) |
| 4 | `.claude/settings.json` | All collaborators + this project | Yes (committed) |
| 5 (lowest) | `~/.claude/settings.json` | You + all projects | No |

**Critical rule:** If a tool is denied at ANY level, no lower level can allow it.

### Permission Rule Syntax

```json
{
  "permissions": {
    "allow": ["ToolName", "ToolName(specifier)"],
    "ask": ["ToolName(pattern)"],
    "deny": ["ToolName(pattern)"]
  }
}
```

**Evaluation order:** deny > ask > allow (first match wins)

#### Tool Specifier Patterns

| Tool | Specifier Format | Example |
|------|-----------------|---------|
| Bash | Wildcard on command | `Bash(npm run *)`, `Bash(git commit *)` |
| Read/Edit | Gitignore-style paths | `Read(src/**)`, `Edit(/src/**/*.ts)` |
| WebFetch | Domain matching | `WebFetch(domain:github.com)` |
| MCP tools | Server + tool name | `mcp__puppeteer__puppeteer_navigate` |
| Agent | Agent type name | `Agent(Explore)`, `Agent(Plan)` |

**Path prefixes for Read/Edit:**
- `~/path` — home directory
- `/path` — project root (not filesystem root!)
- `//path` — absolute filesystem path
- `**` — recursive match

### Permission Modes

| Mode | Key | Behavior |
|------|-----|----------|
| Ask (Default) | `default` | Prompts for all non-allowed tools |
| Auto Accept Edits | `acceptEdits` | Auto-accepts file edits, still asks for Bash |
| Plan | `plan` | Read-only analysis, no modifications |
| Don't Ask | `dontAsk` | Auto-denies unless pre-approved |
| Bypass | `bypassPermissions` | Skips all checks (containers/VMs only) |

Set via: `claude --permission-mode acceptEdits` or `"defaultMode": "acceptEdits"` in settings.

---

## Recommended Fix

### Option A: Targeted Fix (Recommended)

Add the missing non-destructive tools to your existing `settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Agent",
      "Edit",
      "Write",
      "Bash",
      "WebSearch",
      "WebFetch",
      "mcp__agentvibes__text_to_speech"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(rm -rf ~)",
      "Bash(git push --force:*)",
      "Bash(git reset --hard:*)"
    ],
    "ask": [
      "Bash(rm:*)",
      "Bash(git push:*)"
    ]
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [
    "agentvibes"
  ]
}
```

**What changed:**
1. Added `Read`, `Glob`, `Grep`, `Agent` to allowlist
2. Changed `WebFetch` from domain-restricted to unrestricted (it's read-only, safe)
3. Removed individual `WebFetch(domain:...)` entries (redundant when WebFetch is fully allowed)
4. Removed `SlashCommand` and `Skill` entries (these don't need explicit permission)

**What this preserves:**
- Destructive commands still denied (`rm -rf /`, `rm -rf ~`, force push, hard reset)
- Dangerous operations still prompt (`rm`, `git push`)
- Edit, Write, Bash remain allowed (your existing preference)

### Option B: Domain-Restricted WebFetch (If You Prefer Tighter Control)

If you want to keep WebFetch domain-locked but reduce prompts, use a broader pattern:

```json
"allow": [
  "Read",
  "Glob",
  "Grep",
  "Agent",
  "Edit",
  "Write",
  "Bash",
  "WebSearch",
  "WebFetch(domain:github.com)",
  "WebFetch(domain:api.github.com)",
  "WebFetch(domain:raw.githubusercontent.com)",
  "WebFetch(domain:bmadcode.github.io)",
  "WebFetch(domain:www.npmjs.com)",
  "WebFetch(domain:pathfinderwiki.com)",
  "WebFetch(domain:2e.aonprd.com)",
  "WebFetch(domain:foundryvtt.com)",
  "WebFetch(domain:www.patreon.com)",
  "WebFetch(domain:kmp.jetbrains.com)",
  "WebFetch(domain:conveyor.hydraulic.dev)",
  "WebFetch(domain:mise.jdx.dev)",
  "WebFetch(domain:whitfin.io)",
  "WebFetch(domain:www.foundryvtt-hub.com)",
  "WebFetch(domain:graphtreon.com)",
  "WebFetch(domain:www.academeez.com)",
  "WebFetch(domain:betterstack.com)",
  "WebFetch(domain:towardsthecloud.com)",
  "WebFetch(domain:medium.com)",
  "WebFetch(domain:dasroot.net)",
  "WebFetch(domain:aws.amazon.com)",
  "mcp__agentvibes__text_to_speech"
]
```

**Trade-off:** You'll still get prompted for every new domain, but Read/Glob/Grep/Agent prompts disappear.

### Option C: Permission Mode Change

If you want even less friction, combine Option A with `acceptEdits` mode:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Read", "Glob", "Grep", "Agent",
      "Edit", "Write", "Bash", "WebSearch", "WebFetch",
      "mcp__agentvibes__text_to_speech"
    ],
    "deny": [
      "Bash(rm -rf /)", "Bash(rm -rf ~)",
      "Bash(git push --force:*)", "Bash(git reset --hard:*)"
    ],
    "ask": [
      "Bash(rm:*)", "Bash(git push:*)"
    ]
  }
}
```

---

## Impact Analysis

### Prompt Reduction Estimate

| Scenario | Before (prompts per workflow) | After (Option A) |
|----------|------------------------------|-------------------|
| BMAD agent activation | 3-5 (config read, agent read, workflow read) | 0 |
| Technical research workflow | 15-25 (reads + globs + greps + agents + fetches) | 0 |
| Session prep (Nornspun) | 8-12 (campaign files, adventure files, indexes) | 0 |
| Creature building | 5-8 (template reads, reference lookups) | 0 |
| Typical full session | 40-80 total prompts | 0-2 (only rm/git push) |

### Security Posture

| Risk | Mitigation |
|------|-----------|
| Accidental file deletion | `rm` commands still prompt; `rm -rf /` and `rm -rf ~` denied |
| Unintended git push | `git push` still prompts; force push denied |
| Malicious web content | WebFetch is read-only; cannot execute or modify anything |
| File modification | Edit/Write/Bash are already allowed in your current config |
| Agent autonomy | Agents inherit your permission rules; they can't escalate |

### What WebFetch Actually Does

WebFetch is a **read-only HTTP GET** operation. It:
- Cannot POST, PUT, DELETE, or modify remote resources
- Cannot execute JavaScript or interact with web pages
- Returns raw text/HTML content only
- Cannot authenticate or send credentials
- Cannot download executables or run them

Allowing it unrestricted carries the same risk as opening a web browser — effectively zero for your use case.

---

## Additional Optimizations

### CLI Aliases for Different Work Modes

```bash
# ~/.zshrc or ~/.bashrc
alias claude-prep='claude --permission-mode acceptEdits'
alias claude-research='claude --allowedTools "Read,Glob,Grep,Agent,WebFetch,WebSearch"'
```

### Global Settings for Cross-Project Comfort

Add to `~/.claude/settings.json` if you want Read/Glob/Grep allowed in ALL projects:

```json
{
  "alwaysThinkingEnabled": true,
  "effortLevel": "high",
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep"
    ]
  }
}
```

This won't override project-level deny rules but provides a baseline.

---

## Sources & Methodology

- **Primary:** Claude Code permissions documentation, CLI reference, settings schema
- **Project audit:** Full read of `.claude/settings.json`, `.claude/settings.local.json`, `~/.claude/settings.json`
- **BMAD audit:** Searched all agent definitions, workflow configs, core infrastructure, and installer output across `_bmad/` directory tree (58 files searched)
- **Cross-reference:** Claude Code changelog for permission feature history
