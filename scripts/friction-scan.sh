#!/usr/bin/env bash
# friction-scan.sh — Scan past Claude Code sessions for friction signals.
#
# Reads JSONL session transcripts via DuckDB, filters to user-role messages,
# counts occurrences of frustration / correction phrases, and ranks them.
#
# Usage:
#   scripts/friction-scan.sh                  # ranked phrase frequency, last 90d
#   scripts/friction-scan.sh --days 30        # restrict window
#   scripts/friction-scan.sh --examples       # show top 30 raw messages with matches
#   scripts/friction-scan.sh --project PATH   # override project dir (encoded)
#
# Defaults to the current project (~/.claude/projects/<cwd-encoded>).

set -euo pipefail

DAYS=90
MODE=ranked
PROJECT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="$2"; shift 2 ;;
    --examples) MODE=examples; shift ;;
    --project) PROJECT_DIR="$2"; shift 2 ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$PROJECT_DIR" ]]; then
  ENCODED=$(pwd | sed 's|/|-|g')
  PROJECT_DIR="$HOME/.claude/projects/$ENCODED"
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "No session dir at: $PROJECT_DIR" >&2
  exit 1
fi

GLOB="$PROJECT_DIR/*.jsonl"

# Phrase list — case-insensitive substring matches against user message text.
read -r -d '' PHRASES <<'SQL' || true
  ('don''t'), ('do not'), ('stop doing'), ('please stop'), ('never do'), ('quit doing'),
  ('wrong'), ('incorrect'), ('that''s not'), ('not what i'),
  ('i didn''t ask'), ('i didn''t want'), ('i never said'), ('i never asked'),
  ('not like that'), ('not that way'), ('the opposite'),
  ('i told you'), ('i said'), ('as i said'), ('we discussed'), ('we agreed'),
  ('the rule is'), ('how many times'), ('still doing'),
  ('why did you'), ('why are you'), ('why would you'),
  ('wtf'), ('ffs'), ('ugh'), ('argh'), ('seriously?'),
  ('are you kidding'), ('come on'), ('cmon'), ('jfc'),
  ('undo'), ('revert'), ('go back'), ('remove that'), ('delete that'),
  ('put it back'), ('roll back'), ('not what i wanted'),
  ('instead of'), ('rather than'), ('should be'), ('should have'),
  ('supposed to'),
  ('keeps doing'), ('every time'), ('each time'),
  ('you always'), ('you never'), ('you forgot'),
  ('you skipped'), ('you missed'), ('you didn''t'),
  ('where''s the'), ('where is the')
SQL

read -r -d '' SQL_COMMON <<SQL || true
WITH raw AS (
  SELECT json
  FROM read_json_objects('$GLOB',
                         format='newline_delimited',
                         ignore_errors=true,
                         maximum_object_size=33554432)
  WHERE json_extract_string(json, '\$.type') = 'user'
),
extracted AS (
  SELECT
    TRY_CAST(json_extract_string(json, '\$.timestamp') AS TIMESTAMP) AS ts,
    json_extract_string(json, '\$.sessionId') AS session_id,
    json_extract_string(json, '\$.cwd') AS cwd,
    COALESCE(
      json_extract_string(json, '\$.message.content'),
      json_extract_string(json, '\$.message.content[0].text')
    ) AS text
  FROM raw
),
phrases(phrase) AS (
  VALUES
$PHRASES
)
SQL

if [[ "$MODE" == "ranked" ]]; then
  SQL_TAIL="
  SELECT
    phrase,
    COUNT(*) AS hits,
    COUNT(DISTINCT session_id) AS sessions,
    MAX(ts)::DATE AS last_seen
  FROM extracted e
  JOIN phrases p ON LOWER(e.text) LIKE '%' || p.phrase || '%'
  WHERE text IS NOT NULL
    AND ts >= NOW() - INTERVAL '$DAYS days'
  GROUP BY phrase
  HAVING hits > 0
  ORDER BY hits DESC, last_seen DESC;"
else
  SQL_TAIL="
  SELECT
    ts::DATE AS day,
    session_id,
    string_agg(DISTINCT phrase, ', ') AS matched,
    LEFT(text, 220) AS snippet
  FROM extracted e
  JOIN phrases p ON LOWER(e.text) LIKE '%' || p.phrase || '%'
  WHERE text IS NOT NULL
    AND ts >= NOW() - INTERVAL '$DAYS days'
  GROUP BY ts, session_id, text
  ORDER BY ts DESC
  LIMIT 30;"
fi

duckdb -box <<EOF
$SQL_COMMON
$SQL_TAIL
EOF
