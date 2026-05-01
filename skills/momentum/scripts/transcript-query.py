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
    Use --story-slugs to filter sessions by slug membership (comma-separated).

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
import re
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


def _get_jsonl_columns(con, path: str) -> set[str]:
    """Return the set of top-level column names in a JSONL file's inferred schema."""
    try:
        result = con.sql(
            f"SELECT column_name FROM (DESCRIBE SELECT * FROM read_json('{path}', {READ_JSON_OPTS}))"
        ).fetchall()
        return {row[0] for row in result}
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# Session discovery
# ---------------------------------------------------------------------------

def _encode_project_path(abs_path: str) -> str:
    """Encode an absolute filesystem path to Claude Code's project directory name.

    Claude Code encodes project paths by replacing every '/' with '-'.
    For absolute paths starting with '/', this produces a leading '-'.
    """
    return abs_path.replace("/", "-")


def _resolve_project_dir(abs_path: str, projects_dir: str) -> str | None:
    """Resolve the ~/.claude/projects/ directory for a given absolute project path.

    Tries the canonical encoding first. If that directory doesn't exist, falls back
    to a suffix-match search in projects_dir. Returns the matched path if found, or
    None if no directory exists for the given project path.
    """
    encoded = _encode_project_path(abs_path)
    candidate = os.path.join(projects_dir, encoded)
    if os.path.isdir(candidate):
        return candidate
    # Fallback: search for a directory whose name decodes back to the path suffix
    if os.path.isdir(projects_dir):
        for entry in os.listdir(projects_dir):
            if abs_path.endswith(entry.replace("-", "/")):
                full = os.path.join(projects_dir, entry)
                if os.path.isdir(full):
                    return full
    return None


def _project_base():
    """Infer Claude Code project directory from cwd."""
    cwd = os.getcwd()
    projects_dir = os.path.expanduser("~/.claude/projects")
    resolved = _resolve_project_dir(cwd, projects_dir)
    if resolved:
        return resolved
    # Return best-guess even if not found (caller handles missing dir gracefully)
    encoded = _encode_project_path(cwd)
    return os.path.join(projects_dir, encoded)


def _worktree_bases(cwd: str | None = None) -> list[str]:
    """Discover Claude Code project directories for all git worktrees.

    Shells out to `git worktree list --porcelain` and for each worktree path
    resolves the Claude Code project directory using the same encoding logic as
    _project_base (via _resolve_project_dir). Emits a stderr warning for any
    worktree path whose encoded directory does not exist under ~/.claude/projects/.
    Returns the list of directories that actually exist.
    Falls back to [] when not in a git repo or git is unavailable.
    """
    if cwd is None:
        cwd = os.getcwd()

    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10,
        )
        if result.returncode != 0:
            return []
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return []

    projects_dir = os.path.expanduser("~/.claude/projects")
    bases = []
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            wt_path = line[len("worktree "):].strip()
            resolved = _resolve_project_dir(wt_path, projects_dir)
            if resolved:
                bases.append(resolved)
            else:
                encoded = _encode_project_path(wt_path)
                print(
                    f"_worktree_bases: no Claude Code project directory found for worktree '{wt_path}' "
                    f"(tried encoded name: '{encoded}' under {projects_dir}). "
                    "Sessions from this worktree will be skipped.",
                    file=sys.stderr,
                )
    return bases


def discover_sessions(
    base: str | list[str],
    after: str | None = None,
    before: str | None = None,
) -> list[str]:
    """Return JSONL session file paths, optionally filtered by mtime date range.

    Args:
        base: Claude project directory (or list of directories) to search.
              When a list is provided, all directories are searched and results
              are deduplicated and sorted by mtime then path for stable ordering.
        after: ISO date string YYYY-MM-DD — include sessions modified on or after
               this date (start of UTC day, i.e. YYYY-MM-DDT00:00:00Z, inclusive).
        before: ISO date string YYYY-MM-DD — include sessions modified on or before
                this date (end of UTC day, i.e. YYYY-MM-DDT23:59:59.999999Z, inclusive).
    """
    # Normalise to list
    bases = [base] if isinstance(base, str) else list(base)

    after_dt = datetime.fromisoformat(after).replace(tzinfo=timezone.utc) if after else None
    # Task 2: before_dt must be end-of-day UTC (23:59:59.999999Z) to include the full final day
    before_dt = (
        datetime.fromisoformat(before).replace(
            hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc
        )
        if before
        else None
    )

    seen: set[str] = set()
    paths: list[tuple[float, str]] = []  # (mtime, path) for stable sort

    for b in bases:
        if not os.path.isdir(b):
            continue
        for entry in os.listdir(b):
            if not entry.endswith(".jsonl"):
                continue
            full = os.path.join(b, entry)
            if not os.path.isfile(full):
                continue
            # Deduplicate by realpath
            real = os.path.realpath(full)
            if real in seen:
                continue
            mtime = os.path.getmtime(full)
            mtime_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
            if after_dt and mtime_dt < after_dt:
                continue
            if before_dt and mtime_dt > before_dt:
                continue
            seen.add(real)
            paths.append((mtime, full))

    # Sort by mtime then path for stable ordering
    paths.sort(key=lambda x: (x[0], x[1]))
    return [p for _, p in paths]


def discover_subagent_files(base: str | list[str], sessions: list[str]) -> list[str]:
    """Return all subagent JSONL paths found under session subagent directories.

    Accepts either a single base directory or a list of base directories.
    """
    bases = [base] if isinstance(base, str) else list(base)

    paths = []
    seen: set[str] = set()
    for session_path in sessions:
        session_id = os.path.basename(session_path).replace(".jsonl", "")
        # Check each base for the subagent directory
        for b in bases:
            sa_dir = os.path.join(b, session_id, "subagents")
            if not os.path.isdir(sa_dir):
                continue
            for f in os.listdir(sa_dir):
                if not f.endswith(".jsonl"):
                    continue
                full = os.path.join(sa_dir, f)
                real = os.path.realpath(full)
                if real not in seen:
                    seen.add(real)
                    paths.append(full)
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
# Slug-based session filtering (Task 5)
# ---------------------------------------------------------------------------

_SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$')


def _filter_sessions_by_slugs(con, session_paths: list[str], slugs: list[str]) -> list[str]:
    """Filter sessions to those that mention any of the given slugs.

    For each session file, runs a DuckDB probe query using parameterized LIKE
    conditions to check if any message content contains one of the supplied slugs.
    Returns filtered list.
    Logs pre/post counts to stderr.

    Raises ValueError if any slug fails shape validation (^[a-z0-9][a-z0-9-]*[a-z0-9]$).
    """
    if not slugs or not session_paths:
        return session_paths

    # Validate slug shape at the boundary before any SQL is constructed
    for slug in slugs:
        if not _SLUG_RE.match(slug):
            raise ValueError(
                f"Invalid slug '{slug}': slugs must match ^[a-z0-9][a-z0-9-]*[a-z0-9]$ — "
                "check your --story-slugs argument"
            )

    pre_count = len(session_paths)
    kept = []
    error_count = 0
    for path in session_paths:
        # Build parameterized LIKE conditions: one placeholder per slug
        placeholders = " OR ".join(
            "message.content::VARCHAR LIKE ?" for _ in slugs
        )
        probe_sql = f"""
            SELECT 1
            FROM read_json('{path}', {READ_JSON_OPTS})
            WHERE {placeholders}
            LIMIT 1
        """
        params = [f"%{slug}%" for slug in slugs]
        try:
            row = con.execute(probe_sql, params).fetchone()
            if row is not None:
                kept.append(path)
        except Exception as exc:
            error_count += 1
            print(
                f"Slug filter: probe error for {path} (slugs: {slugs}): {exc}",
                file=sys.stderr,
            )
            # On error, keep the session (err on the side of inclusion)
            kept.append(path)

    if error_count > 0:
        threshold = max(1, pre_count // 4)  # 25% failure threshold
        if error_count >= threshold:
            raise RuntimeError(
                f"Slug filter: {error_count}/{pre_count} probe queries failed "
                f"(threshold: {threshold}). Session filter is unreliable — aborting."
            )

    post_count = len(kept)
    if post_count < pre_count:
        print(
            f"Slug filter: {pre_count} → {post_count} sessions "
            f"(dropped {pre_count - post_count} sessions not mentioning any of: {', '.join(slugs)})",
            file=sys.stderr,
        )
    else:
        print(
            f"Slug filter: {pre_count} sessions kept (all mention at least one slug)",
            file=sys.stderr,
        )
    return kept


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
            columns = _get_jsonl_columns(con, agent["jsonl_path"])
            has_tool_use_result = "toolUseResult" in columns
            has_source_tool = "sourceToolAssistantUUID" in columns

            # Build error detection clause based on available columns
            if has_tool_use_result:
                error_where = """
                          -- Indicator 1: toolUseResult JSON object with success=false
                          (TRY_CAST(toolUseResult AS JSON) IS NOT NULL
                           AND json_extract_string(toolUseResult::VARCHAR, '$.success') = 'false')
                          OR
                          -- Indicator 2: content block with is_error=true flag
                          message.content::VARCHAR LIKE '%"is_error":true%'
                          OR message.content::VARCHAR LIKE '%"is_error": true%'"""
            else:
                error_where = """
                          -- toolUseResult column absent — only check content block errors
                          message.content::VARCHAR LIKE '%"is_error":true%'
                          OR message.content::VARCHAR LIKE '%"is_error": true%'"""

            # Build tool_results count — sourceToolAssistantUUID may be absent
            if has_source_tool:
                tool_results_expr = """COUNT(*) FILTER (
                            WHERE type = 'user' AND sourceToolAssistantUUID IS NOT NULL
                        ) AS tool_results"""
            else:
                tool_results_expr = "0 AS tool_results"

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
                        {tool_results_expr},
                        COUNT(*) AS total_entries
                    FROM entries
                ),
                -- Error detection via actual error indicators (not string matching)
                error_count AS (
                    SELECT COUNT(*) AS errors
                    FROM entries
                    WHERE type = 'user'
                      AND ({error_where}
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
        help="Include sessions modified on or after this date (UTC start-of-day, inclusive)",
    )
    parser.add_argument(
        "--before",
        metavar="YYYY-MM-DD",
        help="Include sessions modified on or before this date (UTC end-of-day, inclusive)",
    )
    parser.add_argument(
        "--story-slugs",
        metavar="SLUG1,SLUG2,...",
        help="Filter sessions to those mentioning any of these story slugs (comma-separated). "
             "Used for same-day sprint disambiguation.",
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

    # Parse story slugs
    story_slugs: list[str] = []
    if getattr(args, "story_slugs", None):
        story_slugs = [s.strip() for s in args.story_slugs.split(",") if s.strip()]

    # Resolve session base directories (primary + worktrees)
    cwd = os.getcwd()
    if args.source:
        primary_base = args.source
        worktree_bases: list[str] = []
    else:
        primary_base = _project_base()
        worktree_bases = _worktree_bases(cwd)

    # Deduplicate: primary_base may already appear in worktree_bases
    all_bases: list[str] = []
    seen_bases: set[str] = set()
    for b in [primary_base] + worktree_bases:
        real = os.path.realpath(b) if os.path.isdir(b) else b
        if real not in seen_bases:
            seen_bases.add(real)
            all_bases.append(b)

    print(
        f"Found {len(all_bases)} base(s): {', '.join(all_bases)}",
        file=sys.stderr,
    )

    sessions = discover_sessions(all_bases, after=args.after, before=args.before)
    pre_filter_count = len(sessions)

    con = duckdb.connect()

    # Apply slug-based filtering when --story-slugs provided
    if story_slugs:
        sessions = _filter_sessions_by_slugs(con, sessions, story_slugs)

    post_filter_count = len(sessions)
    subagents = discover_subagent_files(all_bases, sessions)

    if not sessions and not subagents:
        print(
            f"No session files found across {len(all_bases)} base(s)",
            file=sys.stderr,
        )
        if not args.after and not args.before:
            print("Tip: use --after YYYY-MM-DD to filter by sprint date range", file=sys.stderr)
        sys.exit(1)

    print(
        f"Found {post_filter_count} session(s) (pre-filter: {pre_filter_count}), "
        f"{len(subagents)} subagent file(s)",
        file=sys.stderr,
    )

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
