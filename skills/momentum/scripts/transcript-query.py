#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["duckdb"]
# ///
"""transcript-query.py — DuckDB-powered Claude Code transcript analyzer.

Reads Claude Code session JSONL files and extracts structured data for
sprint retrospective analysis. Supports pre-built queries and ad-hoc SQL.

Auto-installs duckdb via pip if not available.

Usage:
    python3 transcript-query.py <query> [options]
    python3 transcript-query.py sql "<SQL>" [options]

Pre-built queries:
    user-messages    Human-typed prompts (not tool results), all sessions
    agent-summary    Per-subagent digest: prompt, outcome, tool counts, errors
    errors           Tool errors using actual error indicators (not string matching)
    team-messages    Inter-agent SendMessage and teammate-message content
    tool-usage       Tool call frequency by name
    sql              Ad-hoc SQL — use $SESSIONS, $SUBAGENTS, $READ_OPTS placeholders

Session discovery:
    By default, discovers sessions from ~/.claude/projects/<project>/
    Use --source to override the base directory.
    Use --after / --before to filter by date range (YYYY-MM-DD).

Error detection (AC #8):
    Errors are detected via actual error indicators:
      1. toolUseResult.success == false  (JSON object with success field)
      2. content[].is_error == true      (content block flag)
      3. type == 'tool_result' with is_error field
    String matching on error words is NOT used in error queries.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure duckdb is available
try:
    import duckdb
except ImportError:
    print("duckdb not found — installing via pip...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb", "-q"])
    import duckdb


READ_JSON_OPTS = "format='newline_delimited', ignore_errors=true, maximum_object_size=10485760"


# ---------------------------------------------------------------------------
# Session discovery
# ---------------------------------------------------------------------------

def _project_base():
    """Infer Claude Code project directory from cwd."""
    cwd = os.getcwd()
    # Claude Code encodes path as hyphen-joined path components
    encoded = cwd.replace("/", "-")
    base = os.path.expanduser(f"~/.claude/projects/{encoded}")
    if os.path.isdir(base):
        return base
    # Fallback: search ~/.claude/projects/ for a directory that matches end of cwd
    projects_dir = os.path.expanduser("~/.claude/projects")
    if os.path.isdir(projects_dir):
        for entry in os.listdir(projects_dir):
            if cwd.endswith(entry.replace("-", "/")):
                candidate = os.path.join(projects_dir, entry)
                if os.path.isdir(candidate):
                    return candidate
    return base  # Return best-guess even if not found


def discover_sessions(base: str, after: str | None = None, before: str | None = None) -> list[str]:
    """Return JSONL session file paths in base, optionally filtered by mtime date range.

    Args:
        base: Claude project directory (e.g. ~/.claude/projects/...)
        after: ISO date string YYYY-MM-DD — include sessions modified on or after this date
        before: ISO date string YYYY-MM-DD — include sessions modified on or before this date
    """
    if not os.path.isdir(base):
        return []

    after_dt = datetime.fromisoformat(after).replace(tzinfo=timezone.utc) if after else None
    before_dt = datetime.fromisoformat(before).replace(tzinfo=timezone.utc) if before else None

    paths = []
    for entry in os.listdir(base):
        if not entry.endswith(".jsonl"):
            continue
        full = os.path.join(base, entry)
        if not os.path.isfile(full):
            continue
        if after_dt or before_dt:
            mtime = datetime.fromtimestamp(os.path.getmtime(full), tz=timezone.utc)
            if after_dt and mtime < after_dt:
                continue
            if before_dt and mtime > before_dt:
                continue
        paths.append(full)
    return sorted(paths)


def discover_subagent_files(base: str, sessions: list[str]) -> list[str]:
    """Return all subagent JSONL paths found under session subagent directories."""
    paths = []
    for session_path in sessions:
        session_id = os.path.basename(session_path).replace(".jsonl", "")
        sa_dir = os.path.join(base, session_id, "subagents")
        if not os.path.isdir(sa_dir):
            continue
        for f in os.listdir(sa_dir):
            if f.endswith(".jsonl"):
                paths.append(os.path.join(sa_dir, f))
    return sorted(paths)


def read_json_fragment(paths: list[str]) -> str:
    """Build SQL fragment to read a list of JSONL files via DuckDB read_json."""
    if not paths:
        raise ValueError("No paths provided to read_json_fragment")
    if len(paths) == 1:
        return f"read_json('{paths[0]}', {READ_JSON_OPTS})"
    path_list = ", ".join(f"'{p}'" for p in paths)
    return f"read_json([{path_list}], {READ_JSON_OPTS}, union_by_name=true)"


# ---------------------------------------------------------------------------
# Pre-built queries
# ---------------------------------------------------------------------------

def query_user_messages(con, sessions: list[str], args) -> object | None:
    """Extract human-typed prompts from all sessions.

    Excludes tool results (sourceToolAssistantUUID IS NULL means human-typed).
    Excludes sidechain messages.
    Returns: timestamp, session_file, content, is_first_message
    """
    if not sessions:
        print("No session files found.", file=sys.stderr)
        return None

    sql = f"""
        SELECT
            timestamp,
            filename AS session_file,
            CASE
                WHEN message.content::VARCHAR LIKE '[{{%'
                THEN json_extract_string(
                    json_extract(message.content::VARCHAR, '$[0]'), '$.text'
                )
                ELSE message.content::VARCHAR
            END AS content,
            (parentUuid IS NULL) AS is_first_message
        FROM {read_json_fragment(sessions)}
        WHERE type = 'user'
          AND sourceToolAssistantUUID IS NULL
          AND isSidechain = false
        ORDER BY timestamp
    """
    if getattr(args, "filter", None):
        sql = sql.replace("ORDER BY", f"AND ({args.filter})\n        ORDER BY")
    if getattr(args, "limit", None):
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_agent_summary(con, sessions: list[str], subagents: list[str], args) -> object | None:
    """Generate per-subagent digest from subagent JSONL files.

    For each subagent: first prompt, outcome snippet, tool counts, error count.
    Error count uses actual error indicators, not string matching.
    Returns JSONL to stdout or --output file.
    """
    # Build manifest from meta.json files co-located with subagent JSONLs
    sa_dirs = set()
    for p in subagents:
        sa_dirs.add(os.path.dirname(p))

    manifest = []
    for sa_dir in sorted(sa_dirs):
        for f in sorted(os.listdir(sa_dir)):
            if not f.endswith(".meta.json"):
                continue
            agent_id = f.replace(".meta.json", "")
            jsonl_path = os.path.join(sa_dir, f"{agent_id}.jsonl")
            if not os.path.exists(jsonl_path):
                continue
            meta_path = os.path.join(sa_dir, f)
            try:
                with open(meta_path) as mf:
                    meta = json.load(mf)
            except Exception:
                meta = {}
            manifest.append({
                "agent_id": agent_id,
                "agent_type": meta.get("agentType", "unknown"),
                "jsonl_path": jsonl_path,
                "size_kb": round(os.path.getsize(jsonl_path) / 1024),
            })

    if not manifest:
        print("No subagent files found.", file=sys.stderr)
        return None

    results = []
    for agent in manifest:
        try:
            row = con.sql(f"""
                WITH entries AS (
                    SELECT *,
                           ROW_NUMBER() OVER (ORDER BY timestamp) AS rn,
                           ROW_NUMBER() OVER (ORDER BY timestamp DESC) AS rn_desc
                    FROM read_json('{agent['jsonl_path']}', {READ_JSON_OPTS})
                ),
                first_user AS (
                    SELECT message.content::VARCHAR AS content
                    FROM entries
                    WHERE type = 'user'
                      AND rn = (SELECT MIN(rn) FROM entries WHERE type = 'user')
                    LIMIT 1
                ),
                last_assistant AS (
                    SELECT message.content::VARCHAR AS content
                    FROM entries
                    WHERE type = 'assistant'
                      AND rn_desc = 1
                    LIMIT 1
                ),
                counts AS (
                    SELECT
                        COUNT(*) FILTER (WHERE type = 'assistant') AS assistant_turns,
                        COUNT(*) FILTER (
                            WHERE type = 'user' AND sourceToolAssistantUUID IS NOT NULL
                        ) AS tool_results,
                        COUNT(*) AS total_entries
                    FROM entries
                ),
                -- Error detection via actual error indicators (not string matching)
                error_count AS (
                    SELECT COUNT(*) AS errors
                    FROM entries
                    WHERE type = 'user'
                      AND (
                          -- Indicator 1: toolUseResult JSON object with success=false
                          (TRY_CAST(toolUseResult AS JSON) IS NOT NULL
                           AND json_extract_string(toolUseResult::VARCHAR, '$.success') = 'false')
                          OR
                          -- Indicator 2: content block with is_error=true flag
                          message.content::VARCHAR LIKE '%"is_error":true%'
                          OR message.content::VARCHAR LIKE '%"is_error": true%'
                      )
                )
                SELECT
                    c.assistant_turns,
                    c.tool_results,
                    c.total_entries,
                    ec.errors,
                    LEFT(fu.content, 400) AS first_prompt,
                    LEFT(la.content, 400) AS last_response
                FROM counts c, error_count ec, first_user fu, last_assistant la
            """).fetchone()

            results.append({
                "agent_id": agent["agent_id"],
                "agent_type": agent["agent_type"],
                "size_kb": agent["size_kb"],
                "assistant_turns": row[0] if row else 0,
                "tool_results": row[1] if row else 0,
                "total_entries": row[2] if row else 0,
                "error_count": row[3] if row else 0,
                "first_prompt": row[4] if row else "",
                "last_response": row[5] if row else "",
            })
        except Exception as e:
            results.append({
                "agent_id": agent["agent_id"],
                "agent_type": agent["agent_type"],
                "size_kb": agent["size_kb"],
                "parse_error": str(e),
            })

    output_text = "\n".join(json.dumps(r) for r in results)
    if getattr(args, "output", None):
        with open(args.output, "w") as f:
            f.write(output_text + "\n")
        print(f"Wrote {len(results)} agent summaries to {args.output}", file=sys.stderr)
    else:
        print(output_text)
    return None  # Handled output directly


def query_errors(con, sessions: list[str], subagents: list[str], args) -> object | None:
    """Extract tool errors using actual error indicators.

    Error detection uses:
      1. toolUseResult JSON object with success=false
      2. content[].is_error == true flag in message content

    Does NOT use string matching on 'error', 'Error', 'FAIL', etc.
    This keeps false-positive rate below 5% (AC #8).
    """
    all_paths = sessions + subagents
    if not all_paths:
        print("No files found.", file=sys.stderr)
        return None

    sql = f"""
        SELECT
            timestamp,
            filename AS source_file,
            toolUseResult::VARCHAR AS tool_result,
            LEFT(message.content::VARCHAR, 600) AS content_preview
        FROM {read_json_fragment(all_paths)}
        WHERE type = 'user'
          AND (
              -- Indicator 1: toolUseResult JSON object with success=false
              (TRY_CAST(toolUseResult AS JSON) IS NOT NULL
               AND json_extract_string(toolUseResult::VARCHAR, '$.success') = 'false')
              OR
              -- Indicator 2: content block is_error flag
              message.content::VARCHAR LIKE '%"is_error":true%'
              OR message.content::VARCHAR LIKE '%"is_error": true%'
          )
        ORDER BY timestamp
    """
    if getattr(args, "filter", None):
        sql = sql.replace("ORDER BY", f"AND ({args.filter})\n        ORDER BY")
    if getattr(args, "limit", None):
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_team_messages(con, subagents: list[str], args) -> object | None:
    """Extract inter-agent SendMessage and teammate-message content from subagent transcripts."""
    if not subagents:
        print("No subagent files found.", file=sys.stderr)
        return None

    sql = f"""
        SELECT
            timestamp,
            filename AS source_file,
            LEFT(message.content::VARCHAR, 1000) AS content_preview
        FROM {read_json_fragment(subagents)}
        WHERE type = 'assistant'
          AND (
              message.content::VARCHAR LIKE '%SendMessage%'
              OR message.content::VARCHAR LIKE '%teammate-message%'
          )
        ORDER BY timestamp
    """
    if getattr(args, "limit", None):
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_tool_usage(con, sessions: list[str], subagents: list[str], args) -> object | None:
    """Aggregate tool call frequency across all sessions and subagents."""
    all_paths = sessions + subagents
    if not all_paths:
        print("No files found.", file=sys.stderr)
        return None

    sql = f"""
        WITH tool_calls AS (
            SELECT
                timestamp,
                filename,
                json_extract_string(item.value, '$.name') AS tool_name
            FROM (
                SELECT timestamp, filename,
                       unnest(from_json(message.content::VARCHAR, '["json"]')) AS item
                FROM {read_json_fragment(all_paths)}
                WHERE type = 'assistant'
                  AND message.content::VARCHAR LIKE '%tool_use%'
            )
            WHERE json_extract_string(item.value, '$.type') = 'tool_use'
        )
        SELECT tool_name, COUNT(*) AS call_count
        FROM tool_calls
        WHERE tool_name IS NOT NULL
        GROUP BY tool_name
        ORDER BY call_count DESC
    """
    if getattr(args, "limit", None):
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_sql(con, sessions: list[str], subagents: list[str], args) -> object | None:
    """Run ad-hoc SQL. Use $SESSIONS, $SUBAGENTS, $ALL, $READ_OPTS as placeholders."""
    sql = args.sql_query

    def _fragment(paths):
        return read_json_fragment(paths) if paths else "VALUES(NULL)"

    sql = sql.replace("$SESSIONS", _fragment(sessions))
    sql = sql.replace("$SUBAGENTS", _fragment(subagents))
    sql = sql.replace("$ALL", _fragment(sessions + subagents))
    sql = sql.replace("$READ_OPTS", READ_JSON_OPTS)
    return con.sql(sql)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def emit_result(result, args):
    """Write query result to output file or stdout."""
    if result is None:
        return
    fmt = getattr(args, "format", "table")
    output_path = getattr(args, "output", None)

    if output_path:
        if fmt == "json":
            rows = result.fetchall()
            cols = [d[0] for d in result.description]
            with open(output_path, "w") as f:
                for row in rows:
                    f.write(json.dumps(
                        {k: (str(v) if v is not None else None)
                         for k, v in zip(cols, row)}
                    ) + "\n")
            print(f"Wrote {len(rows)} rows to {output_path}", file=sys.stderr)
        elif fmt == "csv":
            result.write_csv(output_path)
            print(f"Wrote CSV to {output_path}", file=sys.stderr)
        else:
            with open(output_path, "w") as f:
                f.write(str(result))
            print(f"Wrote table to {output_path}", file=sys.stderr)
    else:
        if fmt == "json":
            rows = result.fetchall()
            cols = [d[0] for d in result.description]
            for row in rows:
                print(json.dumps(
                    {k: (str(v) if v is not None else None)
                     for k, v in zip(cols, row)}
                ))
        else:
            print(result)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

QUERIES = ["user-messages", "agent-summary", "errors", "team-messages", "tool-usage", "sql"]


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code transcript analyzer for sprint retrospectives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "query",
        choices=QUERIES,
        metavar="query",
        help=f"Pre-built query or 'sql'. Choices: {', '.join(QUERIES)}",
    )
    parser.add_argument("sql_query", nargs="?", help="SQL query (only when query='sql')")
    parser.add_argument(
        "--source",
        default=None,
        help="Claude project directory (default: auto-detected from cwd)",
    )
    parser.add_argument(
        "--after",
        metavar="YYYY-MM-DD",
        help="Include sessions modified on or after this date",
    )
    parser.add_argument(
        "--before",
        metavar="YYYY-MM-DD",
        help="Include sessions modified on or before this date",
    )
    parser.add_argument("--output", help="Output file path")
    parser.add_argument(
        "--format",
        choices=["json", "csv", "table"],
        default="json",
        help="Output format (default: json for file output, table for stdout)",
    )
    parser.add_argument("--filter", help="Additional SQL WHERE clause fragment")
    parser.add_argument("--limit", type=int, help="Limit result rows")
    args = parser.parse_args()

    if args.query == "sql" and not args.sql_query:
        parser.error("sql_query argument required when query is 'sql'")

    base = args.source or _project_base()
    if not os.path.isdir(base):
        print(f"Warning: project directory not found: {base}", file=sys.stderr)

    sessions = discover_sessions(base, after=args.after, before=args.before)
    subagents = discover_subagent_files(base, sessions)

    if not sessions and not subagents:
        print(f"No session files found in {base}", file=sys.stderr)
        if not args.after and not args.before:
            print("Tip: use --after YYYY-MM-DD to filter by sprint date range", file=sys.stderr)
        sys.exit(1)

    print(
        f"Found {len(sessions)} session(s), {len(subagents)} subagent file(s)",
        file=sys.stderr,
    )

    con = duckdb.connect()

    dispatch = {
        "user-messages": lambda: query_user_messages(con, sessions, args),
        "agent-summary": lambda: query_agent_summary(con, sessions, subagents, args),
        "errors":        lambda: query_errors(con, sessions, subagents, args),
        "team-messages": lambda: query_team_messages(con, subagents, args),
        "tool-usage":    lambda: query_tool_usage(con, sessions, subagents, args),
        "sql":           lambda: query_sql(con, sessions, subagents, args),
    }

    result = dispatch[args.query]()
    emit_result(result, args)


if __name__ == "__main__":
    main()
