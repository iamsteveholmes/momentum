#!/usr/bin/env bash
# subagent-stop.sh — SubagentStop hook: log subagent lifecycle stop events
# Fires whenever a subagent completes in the main session.
#
# Hook input (via stdin as JSON):
#   {
#     "agent_type": "...",
#     "session_id": "...",
#     "agent_transcript_path": "...",
#     "last_assistant_message": "..."
#   }
#
# Output: JSONL entry appended to sprint log directory
#   {timestamp, agent, story, sprint, event: "subagent-stop", detail}
#
# Resilience:
#   - If sprint slug cannot be determined, logs to _unsorted
#   - Any failure exits silently (exit 0) — never blocks agent work
#   - last_assistant_message truncated to 500 chars max (AC #8)

set -uo pipefail

# --- Project root detection ---
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}"
if [[ -z "$PROJECT_DIR" ]]; then
  exit 0
fi

# Read all stdin upfront (before subshell) to avoid stdin consumption issues
HOOK_STDIN_DATA=""
if read -r -t 2 first_line 2>/dev/null; then
  HOOK_STDIN_DATA="$first_line"
  while IFS= read -r -t 0.1 more_line 2>/dev/null; do
    HOOK_STDIN_DATA="${HOOK_STDIN_DATA}${more_line}"
  done || true
fi

# Wrap everything in a subshell to catch any errors silently
(
  # --- Parse all fields from stdin JSON via Python ---
  # Delegate ALL parsing and logging to Python for reliability
  SPRINTS_INDEX="$PROJECT_DIR/_bmad-output/implementation-artifacts/sprints/index.json"
  LOG_BASE="$PROJECT_DIR/.claude/momentum/sprint-logs"

  HOOK_STDIN_DATA_VAL="$HOOK_STDIN_DATA" \
  SPRINTS_INDEX_VAL="$SPRINTS_INDEX" \
  LOG_BASE_VAL="$LOG_BASE" \
  python3 - <<'PYEOF' 2>/dev/null || true
import json, os
from datetime import datetime

stdin_data = os.environ.get('HOOK_STDIN_DATA_VAL', '')
sprints_index = os.environ.get('SPRINTS_INDEX_VAL', '')
log_base = os.environ.get('LOG_BASE_VAL', '')

# Parse hook input
agent_type = 'unknown-subagent'
session_id = ''
transcript_path = ''
last_message = ''

try:
    if stdin_data:
        d = json.loads(stdin_data)
        agent_type = d.get('agent_type') or 'unknown-subagent'
        session_id = d.get('session_id') or ''
        transcript_path = d.get('agent_transcript_path') or ''
        last_message = d.get('last_assistant_message') or ''
except Exception:
    pass

# Truncate last_message to 500 chars max (AC #8)
if len(last_message) > 500:
    last_message = last_message[:500]

# Determine sprint slug
sprint_slug = '_unsorted'
try:
    if os.path.isfile(sprints_index):
        with open(sprints_index) as f:
            data = json.load(f)
        active = data.get('active') or {}
        slug = active.get('slug', '') or ''
        if slug:
            sprint_slug = slug
except Exception:
    pass

# Set up log directory
log_dir = os.path.join(log_base, sprint_slug)
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'hooks-observability.jsonl')

# Build JSONL entry
entry = {
    'timestamp': datetime.now().isoformat(),
    'agent': agent_type,
    'story': None,
    'sprint': sprint_slug if sprint_slug != '_unsorted' else None,
    'event': 'subagent-stop',
    'detail': json.dumps({
        'session_id': session_id,
        'agent_type': agent_type,
        'transcript_path': transcript_path,
        'last_message': last_message,
    }),
}

with open(log_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(entry) + '\n')
PYEOF
) 2>/dev/null || true

# Always exit 0 — never block agent work
exit 0
