---
title: Agent Observability System — Hook-Based Logging for Retro Flywheel
story_key: agent-observability-system
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/hooks/hooks.json
  - skills/momentum/scripts/momentum-tools.py
change_type: rule-hook + code
priority: high
---

# Agent Observability System — Hook-Based Logging for Retro Flywheel

## Description

The retro flywheel depends on agent logs to discover patterns, errors, and
process gaps. Today, retro reads curated milestone logs — typically ~24 events
per sprint — hand-written by Impetus via `momentum-tools log`. Meanwhile,
actual session data shows 246 user messages, 97 subagent invocations, and
806 tool events per sprint. The curated log captures less than 3% of what
happened.

Claude Code provides `SubagentStop` and `SubagentStart` lifecycle hooks that
fire in the main session whenever a subagent is spawned or completes.
`SubagentStop` exposes `agent_transcript_path`, `last_assistant_message`,
`agent_type`, and `session_id`. These hooks can automatically capture every
subagent lifecycle event without any agent needing to remember to log.

This story adds hook-based observability that captures subagent start/stop
events into structured JSONL logs, enriches the existing `momentum-tools log`
command to support the new event types, and wires the hooks into
`hooks.json`. The retro skill's cross-log discovery phase then has 30-50x
more signal to work with.

## Acceptance Criteria (Plain English)

1. A `SubagentStart` hook is registered in `skills/momentum/hooks/hooks.json`
   that fires whenever a subagent is spawned. The hook captures the subagent's
   name/type, the session ID, and the timestamp, and writes a structured JSONL
   entry to the sprint log directory.

2. A `SubagentStop` hook is registered in `skills/momentum/hooks/hooks.json`
   that fires whenever a subagent completes. The hook captures the subagent's
   name/type, session ID, `agent_transcript_path`, `last_assistant_message`
   (truncated to a reasonable length for log storage), duration (if
   calculable from start/stop timestamps), and writes a structured JSONL entry
   to the sprint log directory.

3. Hook scripts are resilient: if the sprint slug cannot be determined (no
   active sprint), events are written to the `_unsorted` log directory. If
   the script fails for any reason, it exits silently (exit code 0) so it
   never blocks agent work.

4. The JSONL entries produced by the hooks use the same schema as existing
   `momentum-tools log` entries: `{timestamp, agent, story, sprint, event,
   detail}`. The `event` field uses new types: `subagent-start` and
   `subagent-stop`. The `agent` field contains the subagent type/name. The
   `detail` field contains a JSON-encoded object with hook-provided metadata
   (session_id, transcript_path, last_message_summary).

5. The `momentum-tools log` command's `VALID_EVENT_TYPES` set is expanded to
   include `subagent-start` and `subagent-stop` so that these events can also
   be written programmatically (not only by hooks).

6. Log files produced by hooks follow the existing naming convention:
   `{agent-name}.jsonl` within `.claude/momentum/sprint-logs/{sprint-slug}/`.
   A dedicated file like `hooks-observability.jsonl` may be used if the
   subagent name cannot be reliably determined at hook time.

7. The hook scripts are fast. Each hook must complete within the configured
   timeout (5 seconds is appropriate). They do not read large files, make
   network calls, or invoke Python with heavy imports.

8. The `last_assistant_message` captured by SubagentStop is truncated to
   500 characters maximum to keep log files manageable. The full transcript
   remains available at `agent_transcript_path` for deeper analysis.

9. The retro skill's existing log collection phase (Phase 2) can read these
   new event types without modification — they use the same JSONL schema and
   appear in the same log directory. No changes to the retro workflow are
   required for basic ingestion.

10. The hook registration in `hooks.json` uses the standard format already
    established by PostToolUse, PreToolUse, and Stop hooks.

## Dev Notes

### Hook environment variables

Claude Code exposes these environment variables to hook scripts:

**SubagentStart:**
- `CLAUDE_SESSION_ID` — session ID of the main (parent) session
- Standard project env vars (`CLAUDE_PROJECT_DIR`, etc.)
- Subagent metadata via hook input (agent name/type)

**SubagentStop:**
- `agent_transcript_path` — path to the subagent's JSONL transcript file
- `last_assistant_message` — final assistant message from the subagent
- `agent_type` — the type/name of the subagent
- `session_id` — the subagent's session ID
- Standard project env vars

Verify exact variable names against current Claude Code docs before
implementation — the hooks API is evolving.

### Implementation approach

**Option A (recommended): Shell scripts**
Two lightweight bash scripts:
- `skills/momentum/hooks/subagent-start.sh`
- `skills/momentum/hooks/subagent-stop.sh`

Each script:
1. Determines the active sprint slug (read `sprints/index.json` with a
   simple `jq` or `python3 -c` one-liner, fallback to `_unsorted`)
2. Constructs the JSONL entry
3. Appends to the log file

Shell is preferred over Python for hook scripts because:
- No import overhead (Python startup + json/pathlib imports add ~200ms)
- Hooks have a 5-second timeout; shell + jq finishes in <100ms
- Matches the existing hook scripts (lint-format.sh, file-protection.sh,
  stop-gate.sh)

**Option B: Python via momentum-tools.py**
Add a `hook-log` subcommand to momentum-tools.py that accepts hook
environment variables and writes the JSONL entry. Hooks call
`python3 momentum-tools.py hook-log --event subagent-start ...`.

Downside: Python startup time (~300ms) on every subagent start/stop.
Acceptable if jq is not available, but shell is faster.

### Sprint slug detection

The hook script needs to determine which sprint to log to. Strategy:
1. Read `_bmad-output/implementation-artifacts/sprints/index.json`
2. If `active` is non-null, use `active.slug`
3. Else fallback to `_unsorted`

This is the same detection pattern used by `momentum-tools log --sprint`.

### hooks.json changes

Add two new hook entries:

```json
{
  "SubagentStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/subagent-start.sh",
          "timeout": 5
        }
      ]
    }
  ],
  "SubagentStop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/subagent-stop.sh",
          "timeout": 5
        }
      ]
    }
  ]
}
```

### JSONL schema examples

**subagent-start event:**
```json
{
  "timestamp": "2026-04-06T11:45:18.818688",
  "agent": "dev-agent",
  "story": null,
  "sprint": "sprint-2026-04-06",
  "event": "subagent-start",
  "detail": "{\"session_id\": \"abc-123\", \"agent_type\": \"dev-agent\"}"
}
```

**subagent-stop event:**
```json
{
  "timestamp": "2026-04-06T12:15:42.123456",
  "agent": "dev-agent",
  "story": null,
  "sprint": "sprint-2026-04-06",
  "event": "subagent-stop",
  "detail": "{\"session_id\": \"abc-123\", \"agent_type\": \"dev-agent\", \"transcript_path\": \"/path/to/transcript.jsonl\", \"last_message\": \"Story complete. All tests passing.\"}"
}
```

### Tasks breakdown

1. **Verify hook API** — Confirm exact environment variables and input
   format for SubagentStart and SubagentStop hooks in current Claude Code
   version. Check if hook receives data via env vars, stdin, or arguments.

2. **Write subagent-start.sh** — Shell script that reads sprint slug from
   sprints/index.json, constructs JSONL entry from hook-provided metadata,
   appends to log file. Include error handling (silent failure, fallback to
   `_unsorted`).

3. **Write subagent-stop.sh** — Shell script that captures transcript path,
   last message (truncated), session ID, and agent type. Appends JSONL entry.
   Same resilience requirements as start script.

4. **Update hooks.json** — Add SubagentStart and SubagentStop entries
   alongside existing PostToolUse, PreToolUse, and Stop hooks.

5. **Update momentum-tools.py VALID_EVENT_TYPES** — Add `subagent-start`
   and `subagent-stop` to the set so programmatic logging of these event
   types is also supported.

6. **Manual verification** — Run a sprint or invoke a subagent manually,
   confirm JSONL entries appear in the correct sprint log directory with
   the expected schema. Verify retro's Phase 2 reads them without error.

### Risks

- **Hook API instability** — SubagentStart/SubagentStop hooks are documented
  but the exact input format may differ from documentation. Task 1 mitigates
  this by verifying before coding.

- **jq availability** — Shell scripts that parse JSON need `jq` or a Python
  fallback. The script should check for `jq` and fall back to
  `python3 -c "import json..."` if unavailable.

- **Log volume** — A sprint with 50+ subagent invocations will produce 100+
  hook-generated events. This is a feature, not a bug — retro needs this
  data. But log file sizes should be monitored. The 500-char truncation on
  `last_assistant_message` keeps individual entries bounded.
