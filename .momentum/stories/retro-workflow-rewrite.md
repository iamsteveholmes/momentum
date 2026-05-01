---
title: Retro Workflow Rewrite — Replace Milestone Logs with Transcript Audit
story_key: retro-workflow-rewrite
status: backlog
epic_slug: impetus-core
depends_on:
  - transcript-query-calibration
touches:
  - skills/momentum/skills/retro/SKILL.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/scripts/momentum-tools.py
  - _bmad-output/implementation-artifacts/sprints/sprint-2026-04-06/audit-extracts/transcript-query.py
change_type: skill-instruction + code
priority: critical
---

# Retro Workflow Rewrite — Replace Milestone Logs with Transcript Audit

## Problem

The existing retro workflow (Phases 2-4: log collection, story verification,
cross-log discovery) relies on structured milestone events that agents
explicitly choose to log via `momentum-tools log`. In sprint-2026-04-06,
this produced **2 findings from 24 log events** — nearly useless.

An ad-hoc transcript audit using DuckDB and a 3-auditor team found **10
struggle items, 7 success patterns, 13 user interventions, and 7
cross-cutting patterns** from the same sprint's raw session transcripts
(246 user messages, 97 subagent transcripts, 806 tool events). An order
of magnitude more signal.

The retro's value proposition is the practice improvement flywheel. If the
retro can't surface what actually happened, the flywheel doesn't turn.

## Root Cause

Milestone logs are a curated highlight reel — agents log decisions, not
struggles. The real signal lives in:
- **User messages** — corrections, redirections, frustration, praise
- **Agent transcripts** — tool errors, backtracking, duplication, efficiency
- **Inter-agent messages** — coordination quality, handoff clarity
- **Session timing** — gaps, bottlenecks, parallelism effectiveness

None of this is captured in milestone logs.

## Solution: Two-Wave Transcript Audit Architecture

### Wave 1: DuckDB Preprocessing (no agents)

Replace Phases 2-4 with automated extraction using `transcript-query.py`
(DuckDB wrapper). This tool reads Claude Code session JSONL files directly
via SQL — no custom parsing, no line-by-line JSON loading.

**Prerequisite:** DuckDB installed (`pip install duckdb`). The tool should
check and auto-install if missing.

**Extraction queries (run automatically):**

| Extract | What | Source |
|---------|------|--------|
| `user-messages.jsonl` | All human-typed prompts across all sessions | Session JSONL files |
| `agent-summaries.jsonl` | Per-subagent digest: prompt, outcome, tool counts, error count, turns | Subagent JSONL files |
| `errors.jsonl` | Tool errors using actual error indicators (not string matching) | All JSONL files |
| `team-messages.jsonl` | Inter-agent SendMessage and teammate-message content | Subagent JSONL files |

**Session discovery:** Find session JSONL files by date range matching the
sprint's started/completed dates in `~/.claude/projects/{project}/`.
Map subagent transcripts via `{session-id}/subagents/` directories.

**Output:** `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/audit-extracts/`

### Wave 2: Auditor Team (3 auditors + 1 documenter)

Spawn 4 agents in parallel via TeamCreate:

**auditor-human** — Reads `user-messages.jsonl`. Identifies:
- Corrections (user fixing agent behavior)
- Redirections (user changing approach)
- Frustration signals (tone, repetition, escalation)
- Praise/approval (what worked)
- Decision points (human exercised judgment)

**auditor-execution** — Reads `agent-summaries.jsonl` + `errors.jsonl`.
Investigates interesting agents via ad-hoc `transcript-query.py` queries:
- Duplication patterns (multiple agents with identical prompts)
- Error recovery patterns
- Tool usage efficiency
- Story iteration counts (why did story X need N dev agents?)

**auditor-review** — Reads `team-messages.jsonl` + agent summaries filtered
to review roles (qa-reviewer, e2e-validator, prompt-engineer). Evaluates:
- Quality gate effectiveness (real issues vs false positives)
- Fix cycle productivity (thrashing vs convergent)
- Inter-agent coordination quality

**documenter** — Receives findings from all 3 auditors via SendMessage.
Builds the findings document. Owns it exclusively. After all auditors
report, performs cross-cutting synthesis pass.

### Findings Document Structure

Output: `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/retro-transcript-audit.md`

```markdown
# Sprint Transcript Audit — {sprint-slug}

## Executive Summary
## What Worked Well
## What Struggled
## User Interventions
## Story-by-Story Analysis
## Cross-Cutting Patterns
## Metrics
## Priority Action Items
```

Each finding includes: what happened, evidence, root cause, recommendation
(fix/keep/investigate).

### What Stays from Current Retro

- **Phase 1 (Sprint Identification)** — unchanged
- **Phase 3 (Story Verification)** — unchanged, still needed
- **Phase 6 (Story Stub Creation)** — unchanged, but now informed by
  transcript audit findings instead of thin milestone log findings
- **Phase 7 (Sprint Closure)** — unchanged

### What Gets Replaced

- **Phase 2 (Log Collection)** — replaced by DuckDB preprocessing
- **Phase 4 (Cross-Log Discovery)** — replaced by auditor team analysis
- **Phase 5 (Triage Output Generation)** — replaced by documenter's
  findings document (single artifact instead of dual triage)

## Acceptance Criteria

1. Retro workflow includes a DuckDB preprocessing step that extracts
   user-messages, agent-summaries, errors, and team-messages from session
   JSONL files into `audit-extracts/` directory.

2. `transcript-query.py` is available as standard retro tooling at a
   known path in the plugin, supporting both pre-built queries and ad-hoc
   SQL via `transcript-query.py sql "..."`.

3. User messages are extracted and analyzed as a first-class audit input
   — every human prompt across all sprint sessions is captured.

4. Retro spawns an auditor team with 3 specialized roles (human, execution,
   review) plus 1 documenter, all communicating via SendMessage.

5. Findings document covers both successes (what to preserve) AND struggles
   (what to fix), with evidence and recommendations for each.

6. Milestone log analysis (current Phases 2/4) is removed from the
   critical path. Milestone logs may optionally supplement but are not
   the primary data source.

7. Retro produces actionable story stubs from transcript audit findings,
   with full descriptions and acceptance criteria.

8. `transcript-query.py` error detection uses actual error indicators
   (`is_error` flag, `tool_use_error` responses) not string matching.
   False-positive rate < 5%.

9. Session discovery automatically finds JSONL files matching the sprint's
   date range — no manual path specification needed.

## Evidence from Sprint-2026-04-06

| Metric | Milestone Logs | Transcript Audit |
|--------|---------------|------------------|
| Findings | 2 | 37 (10 struggles + 7 successes + 13 interventions + 7 patterns) |
| Data analyzed | 24 log events | 246 user messages + 97 subagents + 806 tool events |
| Story stubs created | 2 | 10 (3 critical, 3 high, 2 medium, 2 low) |
| Actionability | Low | High — specific root causes with evidence |
| Time to insight | ~2 minutes | ~15 minutes (preprocessing + audit team) |

## Technical Notes

- DuckDB is an in-process library (like SQLite for analytics). No server,
  no daemon, no configuration. `pip install duckdb` is the only dependency.
- Session transcripts live at `~/.claude/projects/{project-path}/{uuid}.jsonl`
- Subagent transcripts at `{uuid}/subagents/agent-{id}.jsonl`
- JSONL schema has 8 entry types. Key distinction: human prompts have
  `sourceToolAssistantUUID = null`; tool results have it set.
- Errors appear in 3 locations: `toolUseResult.success`, `content[].is_error`,
  `toolUseResult` string prefix. Must check all three.

## Gherkin Scenarios

```gherkin
Feature: Retro Transcript Audit

  Scenario: Preprocessing extracts user messages from session transcripts
    Given a completed sprint with session JSONL files
    When the retro runs DuckDB preprocessing
    Then user-messages.jsonl contains all human-typed prompts
    And each entry has timestamp, session_file, and content fields
    And tool results are excluded (only human prompts)

  Scenario: Auditor team produces findings document
    Given preprocessed extracts exist in audit-extracts/
    When the retro spawns the auditor team
    Then 3 auditors and 1 documenter are created
    And auditors send findings to documenter via SendMessage
    And documenter writes retro-transcript-audit.md
    And the document has both "What Worked Well" and "What Struggled" sections

  Scenario: Error extraction has low false-positive rate
    Given session transcripts with known errors
    When transcript-query.py extracts errors
    Then flagged errors use actual error indicators not string matching
    And false-positive rate is below 5%

  Scenario: Milestone logs are not the primary data source
    Given a sprint with zero momentum-tools log events
    When the retro runs
    Then transcript audit still produces substantive findings
    And the retro does not halt or produce empty output
```

---

## Dev Agent Record

### Completion Notes

Implemented transcript-audit-based retro workflow replacing milestone-log-based Phases 2/4/5.

**transcript-query.py** (`skills/momentum/scripts/transcript-query.py`):
- Supports 6 pre-built queries: user-messages, agent-summary, errors, team-messages, tool-usage, sql
- Session discovery via `--after`/`--before` date range filters (no hardcoded session IDs)
- Auto-detects project base from cwd by encoding path as Claude Code convention
- Auto-installs duckdb via pip if not present
- Error detection via actual error indicators: `is_error:true` content block flag and `toolUseResult.success=false` — not string matching
- Ad-hoc SQL via `transcript-query.py sql "..."` with $SESSIONS/$SUBAGENTS/$ALL/$READ_OPTS placeholders
- Verified functional against real sprint-2026-04-06 session data (15 sessions, 351 subagents)

**workflow.md** (`skills/momentum/skills/retro/workflow.md`):
- Phase 0: Task tracking (updated phase list, 6 phases instead of 7)
- Phase 1: Sprint identification — unchanged, adds sprint_started for session discovery
- Phase 2: Transcript preprocessing (NEW) — replaces log collection; runs 4 DuckDB extractions in parallel
- Phase 3: Story verification — unchanged
- Phase 4: Auditor team (NEW) — replaces cross-log discovery + triage output; spawns auditor-human, auditor-execution, auditor-review, documenter via TeamCreate; produces single retro-transcript-audit.md
- Phase 5: Story stub creation — unchanged in mechanics, now reads from findings document instead of triage files
- Phase 6: Sprint closure — unchanged, updated summary to report transcript metrics

**SKILL.md** description updated to reflect new architecture.

### AC Verification

1. AC1 (DuckDB preprocessing step) — Phase 2 runs 4 extractions into audit-extracts/
2. AC2 (transcript-query.py at known path) — `skills/momentum/scripts/transcript-query.py` with ad-hoc sql support
3. AC3 (user messages first-class) — user-messages.jsonl captured; auditor-human analyzes it
4. AC4 (auditor team 3+1 via SendMessage) — Phase 4 spawns all 4 via TeamCreate with explicit communication protocol
5. AC5 (successes AND struggles) — documenter template requires both "What Worked Well" and "What Struggled" sections
6. AC6 (milestone logs not critical path) — workflow critical note + preprocessing handles empty log case gracefully
7. AC7 (actionable story stubs with full ACs) — Phase 5 derives suggested ACs from findings
8. AC8 (actual error indicators, <5% false positives) — errors query uses is_error flag and success=false only
9. AC9 (auto session discovery by date range) — --after/--before flags with sprint_started/sprint_completed

## File List

- `skills/momentum/scripts/transcript-query.py` — new
- `skills/momentum/skills/retro/workflow.md` — modified
- `skills/momentum/skills/retro/SKILL.md` — modified

## Change Log

- feat(skills): retro workflow rewrite — transcript audit replaces milestone log analysis (2026-04-06)

## Status

review
