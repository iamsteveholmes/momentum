---
title: Transcript Query Calibration — Fix Error False Positives and Schema Variants
story_key: transcript-query-calibration
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - _bmad-output/implementation-artifacts/sprints/sprint-2026-04-06/audit-extracts/transcript-query.py
change_type: code
priority: medium
---

# Transcript Query Calibration — Fix Error False Positives and Schema Variants

## Problem

The `transcript-query.py` error detection has a **65% false-positive rate**: 529 of 806 flagged errors were not actual errors. Additionally, 18 subagent transcripts were unparseable due to JSONL schema variations the tool doesn't handle.

The root cause is string-pattern matching on words like "error", "Error", "FAIL", and "failed" in the raw `toolUseResult` and `message.content` fields. These strings appear constantly in normal tool output — stack traces being discussed, error-handling code being written, log messages being read, filenames containing "error", etc. The current approach cannot distinguish "this tool call failed" from "this tool call returned content that mentions the word error."

## Error Location Reference

Errors in Claude Code JSONL transcripts appear in exactly 3 locations. All three must be checked; none should use string matching.

### Location 1: `toolUseResult` as structured object with `.success` field

When a tool result is returned as a JSON object, it may contain an explicit success indicator:

```json
{
  "toolUseResult": {
    "success": false,
    "output": "Command failed with exit code 1: ..."
  }
}
```

**Detection:** `toolUseResult.success = false` (boolean check, not string match).

### Location 2: `content[].is_error` flag in message content array

Tool results returned via the Anthropic API content block format use an `is_error` boolean:

```json
{
  "message": {
    "content": [
      {
        "type": "tool_result",
        "tool_use_id": "...",
        "is_error": true,
        "content": "Error: file not found"
      }
    ]
  }
}
```

**Detection:** Parse `message.content` as JSON array, check for any element where `is_error = true` (boolean, not string match on `"is_error":true`).

### Location 3: `toolUseResult` as string with error prefix

Some tool results are stored as plain strings. Actual errors use a specific prefix pattern (e.g., `"tool_use_error: ..."` or similar structured prefix), not arbitrary mentions of the word "error" in the output body.

**Detection:** Check whether the string value of `toolUseResult` starts with an error-indicator prefix, not whether it contains "error" anywhere.

## Unparseable Agent Transcripts

18 agents could not be parsed because the JSONL entries use schema variations the tool doesn't anticipate:

- Some entries lack the `toolUseResult` field entirely (agent-to-agent messages, system prompts)
- Some entries use different content encodings (string vs. array vs. nested object)
- Some entries have `message.content` as a plain string rather than a JSON array

The tool must handle all entry shapes gracefully — missing fields should be treated as "no error," not cause a parse failure.

## Acceptance Criteria

1. Error queries (`errors` command and `error_count` in `agent-summary`) use structural error indicators (`toolUseResult.success = false`, `content[].is_error = true`, `toolUseResult` string error prefix) instead of string pattern matching on "error"/"Error"/"FAIL"/"failed".

2. False-positive rate on error detection drops below 5% when re-run against the sprint-2026-04-06 session transcripts (the same corpus that produced the 65% false-positive rate).

3. All subagent JSONL files that exist in the subagents directory are parseable — the tool does not skip or crash on schema variations. Entries with missing or differently-shaped fields are handled gracefully (treated as non-errors, not parse failures).

4. The `agent-summary` command's `error_count` CTE uses the same corrected detection logic as the standalone `errors` query — no divergence between the two code paths.

5. The tool continues to detect actual errors that were correctly flagged by the old heuristic — true-positive recall does not regress.

## Dev Notes

### Current flawed detection (both `query_errors` and `query_agent_summary`)

```python
# Lines 156-160 (agent-summary error_count CTE)
WHERE type = 'user'
  AND (toolUseResult::VARCHAR LIKE '%error%'
       OR toolUseResult::VARCHAR LIKE '%Error%'
       OR toolUseResult::VARCHAR LIKE '%FAIL%'
       OR message.content::VARCHAR LIKE '%"is_error":true%'
       OR message.content::VARCHAR LIKE '%"is_error": true%')

# Lines 221-226 (errors query)
WHERE type = 'user'
  AND (toolUseResult::VARCHAR LIKE '%error%'
       OR toolUseResult::VARCHAR LIKE '%Error%'
       OR toolUseResult::VARCHAR LIKE '%FAIL%'
       OR toolUseResult::VARCHAR LIKE '%failed%'
       OR message.content::VARCHAR LIKE '%"is_error":true%'
       OR message.content::VARCHAR LIKE '%"is_error": true%')
```

### What to replace it with

Use DuckDB's JSON extraction functions to check the actual structural indicators:

```sql
WHERE type = 'user'
  AND (
    -- Location 1: structured toolUseResult with success=false
    TRY_CAST(json_extract(toolUseResult::VARCHAR, '$.success') AS BOOLEAN) = false

    -- Location 2: content array element with is_error=true
    OR EXISTS (
      SELECT 1 FROM (
        SELECT unnest(from_json(message.content::VARCHAR, '["json"]')) as item
      ) WHERE TRY_CAST(json_extract_string(item, '$.is_error') AS BOOLEAN) = true
    )

    -- Location 3: toolUseResult string with error prefix
    OR (
      json_extract(toolUseResult::VARCHAR, '$.success') IS NULL
      AND toolUseResult::VARCHAR NOT LIKE '{%'
      AND toolUseResult::VARCHAR LIKE 'tool_use_error:%'
    )
  )
```

The exact SQL will need tuning against real data — the above is a starting point, not copy-paste-ready. The implementer should:

1. Sample actual error entries from the sprint corpus to identify the real prefix patterns
2. Verify the DuckDB JSON functions work on the actual field shapes
3. Compare old vs. new result sets to confirm true positives are retained

### Schema robustness

Wrap field access in `TRY_CAST` or null checks. Use `ignore_errors=true` (already present in `READ_JSON_OPTS`) and `union_by_name=true` for multi-file reads. Fields that don't exist in some entries should evaluate to NULL, not cause query failure.

## Tasks

1. **Audit the corpus** — Sample 20-30 entries from the current error results to catalog the actual false-positive patterns (e.g., "error" in stack traces, code snippets, filenames). Sample 10-15 known actual errors to identify their structural markers.

2. **Fix `query_errors`** — Replace string-matching WHERE clause (lines 221-226) with structural checks against the 3 error locations. Validate against the sprint corpus.

3. **Fix `query_agent_summary` error CTE** — Replace string-matching WHERE clause (lines 156-160) with the same structural checks. Ensure both code paths use identical logic.

4. **Handle schema variations** — Ensure all JSONL entries are parseable regardless of shape. Test against the 18 previously-unparseable agent files. Entries with missing fields should not cause parse errors.

5. **Validate false-positive rate** — Re-run `errors` query against the full sprint-2026-04-06 corpus. Manually verify a sample of flagged errors. Confirm false-positive rate < 5% and no true-positive regression.
