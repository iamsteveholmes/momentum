# Eval: Startup Preflight Performance — Tool Call Budget

## Scenario

Momentum is fully installed. All component groups are at current version. No hash drift. No open journal threads. This is the happy path — the most common startup.

**Given** all components are current, no drift, no open threads
**When** the developer invokes `/momentum`
**Then** first visible output (session greeting + menu) appears within 3-5 tool calls

## Context to Load

Load `skills/momentum/skills/impetus/SKILL.md` as the implementation under test.

Simulate:
- `startup-preflight` returns `route: "greeting"`, `has_open_threads: false`, with greeting state inline
- `session-greeting.md` is available at the expected reference path

## Expected Tool Call Sequence

1. **Bash**: `momentum-tools session startup-preflight` → returns route + greeting state (1 call)
2. **Read**: `session-greeting.md` → template lookup (1 call)
3. **Output**: Rendered greeting + menu ← first visible output

Total: **2-3 tool calls** before first visible output (SKILL.md auto-load is not counted as a tool call — it's the skill entry point).

## Failure Conditions

- More than 5 tool calls before first visible output = FAIL
- Loading workflow.md on the happy path = FAIL (workflow.md is only for non-happy paths)
- Reading momentum-versions.json, installed.json, or global-installed.json as separate Read calls = FAIL (these are consolidated into startup-preflight)
- Any file read that startup-preflight already provides data for = FAIL

## Pass Condition

First visible output (greeting + menu) appears after at most 3 tool calls: 1 Bash (preflight) + 1 Read (session-greeting.md) + rendering. No workflow.md loaded.
