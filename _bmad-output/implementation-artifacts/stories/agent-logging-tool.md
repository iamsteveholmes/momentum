---
title: Agent Logging Tool — Structured JSONL Event Log for All Agents
status: ready-for-dev
epic_slug: impetus-core
depends_on:
  - momentum-tooling
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
change_type: cli-tool
---

# Agent Logging Tool

## Goal

Add a `log` subcommand to momentum-tools.py so every agent in the system can record
decisions, errors, retries, assumptions, findings, and ambiguities to structured JSONL
files during execution. This creates the observability foundation that all Phase 3
workflows depend on — sprint-dev, momentum-dev, and verifiers all log through this
single deterministic interface.

## Acceptance Criteria (Plain English)

> Detailed Gherkin specs: `sprints/phase-3-sprint-execution/specs/agent-logging-tool.feature`

- The `log` subcommand accepts `--agent`, `--event`, `--detail`, and optionally `--story`
  and `--sprint` arguments. `--agent`, `--event`, and `--detail` are required; `--story`
  and `--sprint` are optional
- When `--story` is provided, log entries are written to `{agent-role}-{story-slug}.jsonl`;
  when omitted, entries go to `{agent-role}.jsonl` (for Impetus's own orchestration log)
- Log files are stored under `.claude/momentum/sprint-logs/{sprint-slug}/`
- The sprint-log directory structure is created automatically on first write
- Each log entry is a single JSON line containing timestamp, agent, story (or null),
  event type, and detail text
- Only valid event types are accepted: decision, error, retry, assumption, finding,
  ambiguity
- The tool is append-only — it never reads, modifies, or truncates existing log entries
- Exit code 0 on success with JSON confirmation on stdout; exit code 1 on failure
  (invalid event type, missing required args)
- Missing `--agent`, `--event`, or `--detail` arguments are rejected with a clear error
- When `--sprint` is omitted, logs go to `.claude/momentum/sprint-logs/_unsorted/` as a
  fallback directory (graceful degradation for standalone invocations)

## Dev Notes

### What exists today
- `momentum-tools.py` has two command groups: `sprint` and `version`
- CLI uses argparse with nested subparsers
- All commands use the `result()` / `error_result()` helpers for JSON output
- `resolve_project_dir()` finds the project root from `CLAUDE_PROJECT_DIR` or git
- `test-momentum-tools.py` uses a `setup_project()` helper that creates temp dirs with
  git init, and `run_tool()` to invoke the script

### What to change
- Add `log` as a new top-level command group in `build_parser()`
- Implement `cmd_log()` that:
  1. Validates event type against the allowed set
  2. Resolves the log directory: `{project_dir}/.claude/momentum/sprint-logs/{sprint-slug}/`
  3. Creates the directory if it doesn't exist (`mkdir -p` equivalent)
  4. Determines filename: `{agent}.jsonl` or `{agent}-{story}.jsonl`
  5. Constructs the JSON entry with ISO 8601 timestamp
  6. Appends the entry as a single line to the file
  7. Outputs JSON confirmation via `result()`
- Add tests to `test-momentum-tools.py`:
  - Log creation creates directory structure
  - Log append adds a valid JSONL line
  - Multiple appends accumulate (file grows)
  - Invalid event type rejected
  - Missing required args rejected
  - Log entry has correct JSON structure (timestamp, agent, story, event, detail)
  - Story-less log uses agent-only filename
  - Story log uses agent-story filename

### What NOT to change
- Do not modify the existing `sprint` or `version` command groups
- Do not add any log-reading or log-querying capability — this is write-only
- Do not change the `result()` / `error_result()` output helpers
- Do not add dependencies beyond the Python standard library

### Interface reference
```
momentum-tools log --agent <role> --story <slug> --sprint <slug> --event <type> --detail "..."
```

### JSONL entry format
```json
{"timestamp": "2026-04-02T14:30:00.123456", "agent": "dev", "story": "agent-logging-tool", "event": "decision", "detail": "Chose worktree-based isolation for concurrent story execution"}
```

### Event type semantics
| Event | When to use |
|---|---|
| `decision` | Agent chose between alternatives — record the choice and why |
| `error` | Something failed — record what and context |
| `retry` | Agent is retrying an operation — record attempt number and reason |
| `assumption` | Agent assumed something not explicitly stated — record what |
| `finding` | Agent discovered something noteworthy — record observation |
| `ambiguity` | Agent encountered unclear input — record what was unclear |

### Requirements Coverage
- FR56: Agent Observability — this story implements the structured JSONL logging tool (`momentum-tools log`) with all required arguments, event types, append-only storage, and per-agent file isolation
- FR57: Graceful Log Failures — exit code behavior and error handling for missing/invalid arguments (graceful degradation in callers is validated by momentum-dev-simplify)
- Architecture: Agent Logging Infrastructure (Decision 24) — implements the `momentum-tools log` CLI, JSONL entry schema, file naming convention, event type vocabulary, and directory auto-creation
- Architecture: Read/Write Authority table, momentum-tools log row — establishes the write-only append authority model for agent log files
- Architecture: Installed Structure, sprint-logs/ directory — creates the runtime directory structure under `.claude/momentum/sprint-logs/{sprint-slug}/`
