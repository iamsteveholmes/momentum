#!/usr/bin/env python3
"""transcript-query.py — DuckDB-powered Claude Code transcript analyzer.

Reads Claude Code session JSONL files and extracts structured data for
sprint retrospective analysis. Supports pre-built queries and ad-hoc SQL.

Usage:
    python3 transcript-query.py <query> [options]
    python3 transcript-query.py sql "<SQL>" [options]

Pre-built queries:
    user-messages    Human-typed prompts (not tool results)
    agent-summary    Per-subagent digest: prompt, outcome, tool counts
    errors           Tool errors from all 3 encoding locations
    backtracking     Assistant messages with retry/correction signals
    team-messages    Inter-agent SendMessage and teammate-message content
    tool-usage       Tool call frequency by name, optionally per agent
"""

import argparse
import json
import os
import sys
from pathlib import Path

import duckdb

# Default paths
DEFAULT_BASE = os.path.expanduser("~/.claude/projects/-Users-steve-projects-momentum")
DEFAULT_PRIMARY_SESSION = "fe5b6cbc-3255-4ca9-83f2-6edec79f1d25"
ALL_SESSIONS = [
    "fe5b6cbc-3255-4ca9-83f2-6edec79f1d25",
    "ebbba161-f3f2-4664-b187-8d5cb3fe1660",
    "3968acbc-dea7-4f62-8ce0-d58c8c6bd376",
    "57537a81-1f29-4073-a7d2-f3412458ad06",
    "4af96169-44a6-4845-be8b-8406bd1f4f6d",
    "9198cd0d-acd0-4d43-b07a-bc120251df77",
    "a58aeb39-ac82-479c-86a4-a39f79559f10",
    "27af3835-13ba-4d03-8616-116880644042",
]

READ_JSON_OPTS = "format='newline_delimited', ignore_errors=true, maximum_object_size=10485760"


def session_paths(base):
    """Return list of existing session JSONL file paths."""
    paths = []
    for sid in ALL_SESSIONS:
        p = os.path.join(base, f"{sid}.jsonl")
        if os.path.exists(p):
            paths.append(p)
    return paths


def subagent_dir(base, session_id=None):
    """Return subagent directory path for given session."""
    sid = session_id or DEFAULT_PRIMARY_SESSION
    return os.path.join(base, sid, "subagents")


def read_json_call(paths):
    """Build a read_json SQL fragment for a list of file paths."""
    if len(paths) == 1:
        return f"read_json('{paths[0]}', {READ_JSON_OPTS})"
    path_list = ", ".join(f"'{p}'" for p in paths)
    return f"read_json([{path_list}], {READ_JSON_OPTS}, union_by_name=true)"


def query_user_messages(con, base, args):
    """Extract human-typed prompts from all sessions."""
    paths = session_paths(base)
    sql = f"""
        SELECT
            timestamp,
            filename AS session_file,
            CASE
                WHEN message.content::VARCHAR LIKE '[{{%' THEN
                    json_extract_string(json_extract(message.content::VARCHAR, '$[0]'), '$.text')
                ELSE message.content::VARCHAR
            END AS content,
            parentUuid IS NULL AS is_first_message
        FROM {read_json_call(paths)}
        WHERE type = 'user'
          AND (sourceToolAssistantUUID IS NULL)
          AND isSidechain = false
        ORDER BY timestamp
    """
    if args.filter:
        sql = sql.replace("ORDER BY", f"AND ({args.filter})\n        ORDER BY")
    if args.limit:
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def _get_jsonl_columns(con, jsonl_path):
    """Return the set of column names in a JSONL file. Returns empty set on error."""
    try:
        desc = con.sql(
            f"SELECT * FROM read_json('{jsonl_path}', {READ_JSON_OPTS}) LIMIT 0"
        ).description
        return {col[0] for col in desc}
    except Exception:
        return set()


def _build_agent_summary_sql(jsonl_path, has_tool_use_result, has_source_tool_uuid):
    """Build per-agent summary SQL adapted to the file's actual schema.

    Handles three schema variants:
    - Files with toolUseResult + sourceToolAssistantUUID (full schema)
    - Files with toolUseResult but no sourceToolAssistantUUID
    - Files with neither column (lightweight transcripts)

    Error detection uses structural indicators only (no string pattern matching):
    - Location 1: toolUseResult JSON object with success=false
    - Location 2: message.content array element with is_error=true
    - Location 3: toolUseResult JSON-encoded string with "Error: prefix
    """
    if has_tool_use_result:
        error_conditions = """
                    -- Location 1: structured tool result with success=false
                    TRY(TRY_CAST(json_extract_string(toolUseResult::VARCHAR, '$.success') AS BOOLEAN)) = false
                    -- Location 2: content array element with is_error=true
                    OR message.content::VARCHAR LIKE '%"is_error":true%'
                    OR message.content::VARCHAR LIKE '%"is_error": true%'
                    -- Location 3: toolUseResult JSON-encoded string with Error prefix
                    OR toolUseResult::VARCHAR LIKE '"Error:%'"""
    else:
        error_conditions = """
                    -- Location 2 only (no toolUseResult column in this schema)
                    message.content::VARCHAR LIKE '%"is_error":true%'
                    OR message.content::VARCHAR LIKE '%"is_error": true%'"""

    tool_results_col = (
        "COUNT(*) FILTER (WHERE type = 'user' AND sourceToolAssistantUUID IS NOT NULL) as tool_results,"
        if has_source_tool_uuid
        else "0 as tool_results,"
    )

    return f"""
                WITH entries AS (
                    SELECT *, ROW_NUMBER() OVER (ORDER BY timestamp) as rn
                    FROM read_json('{jsonl_path}', {READ_JSON_OPTS})
                ),
                first_user AS (
                    SELECT message.content::VARCHAR as content
                    FROM entries
                    WHERE type = 'user' AND rn = (
                        SELECT MIN(rn) FROM entries WHERE type = 'user'
                    )
                    LIMIT 1
                ),
                last_assistant AS (
                    SELECT message.content::VARCHAR as content
                    FROM entries
                    WHERE type = 'assistant' AND rn = (
                        SELECT MAX(rn) FROM entries WHERE type = 'assistant'
                    )
                    LIMIT 1
                ),
                tool_counts AS (
                    SELECT
                        COUNT(*) FILTER (WHERE type = 'assistant') as assistant_turns,
                        {tool_results_col}
                        COUNT(*) as total_entries
                    FROM entries
                ),
                error_count AS (
                    SELECT COUNT(*) as errors
                    FROM entries
                    WHERE type = 'user'
                      AND ({error_conditions}
                      )
                )
                SELECT
                    tc.assistant_turns,
                    tc.tool_results,
                    tc.total_entries,
                    ec.errors,
                    LEFT(COALESCE(fu.content, ''), 300) as first_prompt,
                    LEFT(COALESCE(la.content, ''), 300) as last_response
                FROM tool_counts tc, error_count ec
                LEFT JOIN first_user fu ON true
                LEFT JOIN last_assistant la ON true
            """


def query_agent_summary(con, base, args):
    """Generate per-subagent summary from primary session subagents."""
    sa_dir = subagent_dir(base)
    if not os.path.isdir(sa_dir):
        print(f"No subagent directory at {sa_dir}", file=sys.stderr)
        return None

    # Build manifest from meta.json files
    manifest = []
    for f in sorted(os.listdir(sa_dir)):
        if f.endswith(".meta.json"):
            agent_id = f.replace(".meta.json", "")
            meta_path = os.path.join(sa_dir, f)
            jsonl_path = os.path.join(sa_dir, f"{agent_id}.jsonl")
            if not os.path.exists(jsonl_path):
                continue
            with open(meta_path) as mf:
                meta = json.load(mf)
            manifest.append({
                "agent_id": agent_id,
                "agent_type": meta.get("agentType", "unknown"),
                "jsonl_path": jsonl_path,
                "size_kb": round(os.path.getsize(jsonl_path) / 1024),
            })

    results = []
    for agent in manifest:
        try:
            cols = _get_jsonl_columns(con, agent["jsonl_path"])
            has_tr = "toolUseResult" in cols
            has_sa = "sourceToolAssistantUUID" in cols
            sql = _build_agent_summary_sql(agent["jsonl_path"], has_tr, has_sa)
            row = con.sql(sql).fetchone()

            results.append({
                "agent_id": agent["agent_id"],
                "agent_type": agent["agent_type"],
                "size_kb": agent["size_kb"],
                "assistant_turns": row[0] if row else 0,
                "tool_results": row[1] if row else 0,
                "total_entries": row[2] if row else 0,
                "errors": row[3] if row else 0,
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

    # Output as JSONL
    output = "\n".join(json.dumps(r) for r in results)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Wrote {len(results)} agent summaries to {args.output}", file=sys.stderr)
    else:
        print(output)
    return None  # Already handled output


def query_errors(con, base, args):
    """Extract tool errors from all sessions and subagents."""
    paths = session_paths(base)
    sa_dir = subagent_dir(base)

    # Add subagent paths
    if os.path.isdir(sa_dir):
        for f in os.listdir(sa_dir):
            if f.endswith(".jsonl"):
                paths.append(os.path.join(sa_dir, f))

    sql = f"""
        SELECT
            timestamp,
            filename AS source_file,
            toolUseResult::VARCHAR AS tool_result,
            LEFT(message.content::VARCHAR, 500) AS content_preview
        FROM {read_json_call(paths)}
        WHERE type = 'user'
          AND (
            -- Location 1: toolUseResult is a JSON object with success=false
            TRY(TRY_CAST(json_extract_string(toolUseResult::VARCHAR, '$.success') AS BOOLEAN)) = false
            -- Location 2: message.content array has an element with is_error=true
            OR message.content::VARCHAR LIKE '%"is_error":true%'
            OR message.content::VARCHAR LIKE '%"is_error": true%'
            -- Location 3: toolUseResult is a JSON-encoded string with Error prefix
            OR toolUseResult::VARCHAR LIKE '"Error:%'
          )
        ORDER BY timestamp
    """
    if args.filter:
        sql = sql.replace("ORDER BY", f"AND ({args.filter})\n        ORDER BY")
    if args.limit:
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_backtracking(con, base, args):
    """Find assistant messages with correction/retry signals."""
    paths = session_paths(base)
    sa_dir = subagent_dir(base)
    if os.path.isdir(sa_dir):
        for f in os.listdir(sa_dir):
            if f.endswith(".jsonl"):
                paths.append(os.path.join(sa_dir, f))

    sql = f"""
        SELECT
            timestamp,
            filename AS source_file,
            LEFT(message.content::VARCHAR, 500) AS content_preview
        FROM {read_json_call(paths)}
        WHERE type = 'assistant'
          AND (message.content::VARCHAR LIKE '%actually%'
               OR message.content::VARCHAR LIKE '%instead%'
               OR message.content::VARCHAR LIKE '%let me try%'
               OR message.content::VARCHAR LIKE '%retry%'
               OR message.content::VARCHAR LIKE '%try again%'
               OR message.content::VARCHAR LIKE '%I was wrong%'
               OR message.content::VARCHAR LIKE '%mistake%')
        ORDER BY timestamp
    """
    if args.filter:
        sql = sql.replace("ORDER BY", f"AND ({args.filter})\n        ORDER BY")
    if args.limit:
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_team_messages(con, base, args):
    """Extract inter-agent communication."""
    sa_dir = subagent_dir(base)
    if not os.path.isdir(sa_dir):
        print(f"No subagent directory at {sa_dir}", file=sys.stderr)
        return None

    paths = [os.path.join(sa_dir, f) for f in os.listdir(sa_dir) if f.endswith(".jsonl")]
    if not paths:
        return None

    sql = f"""
        SELECT
            timestamp,
            filename AS source_file,
            LEFT(message.content::VARCHAR, 800) AS content_preview
        FROM {read_json_call(paths)}
        WHERE type = 'assistant'
          AND (message.content::VARCHAR LIKE '%SendMessage%'
               OR message.content::VARCHAR LIKE '%teammate-message%')
        ORDER BY timestamp
    """
    if args.limit:
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_tool_usage(con, base, args):
    """Aggregate tool call frequency."""
    paths = session_paths(base)
    sa_dir = subagent_dir(base)
    if os.path.isdir(sa_dir):
        for f in os.listdir(sa_dir):
            if f.endswith(".jsonl"):
                paths.append(os.path.join(sa_dir, f))

    # Extract tool names from assistant messages containing tool_use
    sql = f"""
        WITH tool_calls AS (
            SELECT
                timestamp,
                filename,
                json_extract_string(unnested.item, '$.name') as tool_name
            FROM (
                SELECT timestamp, filename, message.content::VARCHAR as content
                FROM {read_json_call(paths)}
                WHERE type = 'assistant'
                  AND message.content::VARCHAR LIKE '%tool_use%'
            ),
            LATERAL (
                SELECT unnest(from_json(content, '["json"]')) as item
            ) unnested
            WHERE json_extract_string(unnested.item, '$.type') = 'tool_use'
        )
        SELECT tool_name, COUNT(*) as call_count
        FROM tool_calls
        WHERE tool_name IS NOT NULL
        GROUP BY tool_name
        ORDER BY call_count DESC
    """
    if args.limit:
        sql += f"\n        LIMIT {args.limit}"
    return con.sql(sql)


def query_sql(con, base, args):
    """Run ad-hoc SQL query."""
    sql = args.sql_query
    # Replace $BASE placeholder
    sql = sql.replace("$BASE", base)
    sql = sql.replace("$SUBAGENTS", subagent_dir(base))
    sql = sql.replace("$READ_OPTS", READ_JSON_OPTS)
    return con.sql(sql)


def main():
    parser = argparse.ArgumentParser(description="Claude Code transcript analyzer")
    parser.add_argument("query", help="Pre-built query name or 'sql'")
    parser.add_argument("sql_query", nargs="?", help="SQL query (when query='sql')")
    parser.add_argument("--source", default=DEFAULT_BASE, help="Base transcript directory")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=["json", "csv", "table"], default="table")
    parser.add_argument("--filter", help="Additional SQL WHERE clause")
    parser.add_argument("--limit", type=int, help="Limit results")
    args = parser.parse_args()

    con = duckdb.connect()

    queries = {
        "user-messages": query_user_messages,
        "agent-summary": query_agent_summary,
        "errors": query_errors,
        "backtracking": query_backtracking,
        "team-messages": query_team_messages,
        "tool-usage": query_tool_usage,
        "sql": query_sql,
    }

    if args.query not in queries:
        print(f"Unknown query: {args.query}", file=sys.stderr)
        print(f"Available: {', '.join(queries.keys())}", file=sys.stderr)
        sys.exit(1)

    result = queries[args.query](con, args.source, args)

    if result is None:
        return  # Query handled its own output (e.g., agent-summary)

    if args.output:
        if args.format == "json":
            rows = result.fetchall()
            cols = [d[0] for d in result.description]
            with open(args.output, "w") as f:
                for row in rows:
                    f.write(json.dumps(dict(zip(cols, [str(v) if v is not None else None for v in row]))) + "\n")
            print(f"Wrote {len(rows)} rows to {args.output}", file=sys.stderr)
        elif args.format == "csv":
            result.write_csv(args.output)
            print(f"Wrote CSV to {args.output}", file=sys.stderr)
        else:
            # Write table format
            with open(args.output, "w") as f:
                f.write(str(result))
            print(f"Wrote table to {args.output}", file=sys.stderr)
    else:
        if args.format == "json":
            rows = result.fetchall()
            cols = [d[0] for d in result.description]
            for row in rows:
                print(json.dumps(dict(zip(cols, [str(v) if v is not None else None for v in row]))))
        else:
            print(result)


if __name__ == "__main__":
    main()
