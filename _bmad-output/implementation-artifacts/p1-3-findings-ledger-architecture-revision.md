---
story_id: p1.3
status: review
type: process
epic: P1 — Process Sprint-1
title: Findings Ledger Architecture Revision
sprint: 1
touches:
  - ".mcp.json"
  - ".claude/settings.local.json"
  - "skills/momentum/references/mcp-config.json"
  - "skills/momentum/references/momentum-versions.json"
  - "skills/momentum/workflow.md"
  - "mcp/findings-server/README.md"
  - "_bmad-output/planning-artifacts/architecture.md"
  - "_bmad-output/planning-artifacts/epics.md"
depends_on:
  - p1.1
---

# Findings Ledger Architecture Revision

## User Story

As a Momentum developer,
I want to revise the findings ledger architecture to use a global JSONL file and clarify the MCP server's role,
So that the findings ledger can detect cross-project patterns, concurrent sessions can safely append without file corruption, and the placeholder MCP config stops failing on every session start.

## Background

The momentum-findings MCP server is configured in `.mcp.json` and enabled in `settings.local.json`, but the actual server (`mcp/findings-server/index.js`) doesn't exist — it's an Epic 6 placeholder. This causes a "Failed to reconnect to momentum-findings" error on every Claude Code session start.

Beyond the immediate fix, architectural analysis determined the ledger should be global JSONL at `~/.claude/momentum/findings-ledger.jsonl` (cross-project pattern detection), the MCP server should be an optional query interface (not a concurrency solution), and the schema needs a `project` field with timestamp-based IDs. See plan for full rationale.

## Acceptance Criteria

```gherkin
Scenario: No MCP failure on session start
  Given a new Claude Code session is started in the momentum project
  When the session initializes
  Then no "Failed to reconnect to momentum-findings" error appears

Scenario: MCP config is empty
  Given the project .mcp.json file exists
  When I inspect its contents
  Then the mcpServers object is empty

Scenario: Install template has no MCP entries
  Given the Impetus install template at skills/momentum/references/mcp-config.json
  When I inspect its contents
  Then the mcpServers object is empty

Scenario: Version manifest has no MCP action
  Given the version manifest at skills/momentum/references/momentum-versions.json
  When I inspect the 1.0.0 actions array
  Then there is no write_config action for .mcp.json

Scenario: Workflow has no MCP references in install flow
  Given the Impetus workflow at skills/momentum/workflow.md
  When I inspect the install flow
  Then no output mentions MCP servers or .mcp.json

Scenario: Architecture Decision 1c specifies global JSONL
  Given the architecture document at _bmad-output/planning-artifacts/architecture.md
  When I read Decision 1c
  Then the findings ledger location is ~/.claude/momentum/findings-ledger.jsonl
  And the format is JSONL (one JSON object per line, append-only)
  And the schema includes a "project" field
  And the id format is timestamp-based (F-{unix_ms}-{random_4hex})

Scenario: Architecture Decision 3c clarifies MCP role
  Given the architecture document
  When I read Decision 3c
  Then the findings MCP server phase is "Deferred (Epic 6)" (not MVP)
  And the description clarifies MCP is an optional query layer
  And the description notes MCP is per-session and cannot serialize writes

Scenario: Epic 6 stories reflect global JSONL architecture
  Given the epics document at _bmad-output/planning-artifacts/epics.md
  When I read Stories 6.1-6.5
  Then Story 6.1 specifies ~/.claude/momentum/findings-ledger.jsonl as init path
  And Story 6.2 specifies cross-project pattern detection
  And Story 6.3 specifies JSONL append with timestamp-ID supersession semantics
  And Story 6.5 specifies global practice health metric with per-project breakdown

Scenario: No stale references to per-project findings-ledger.json
  When I run grep -rP "findings-ledger\.json[^l]" _bmad-output/ skills/ mcp/
  Then zero matches are found (all changed to .jsonl or removed)

Scenario: All findings-ledger references use global path
  When I run grep -r "\.claude/momentum/findings-ledger" _bmad-output/ skills/ mcp/
  Then all matches use the ~/.claude/ global prefix
  And no matches use a project-relative .claude/ path
```

## Definition of Done

- [ ] `.mcp.json` — empty mcpServers object
- [ ] `skills/momentum/references/mcp-config.json` — empty mcpServers object
- [ ] `skills/momentum/references/momentum-versions.json` — no mcp-config.json action
- [ ] `skills/momentum/workflow.md` — no MCP references in install flow; `"mcp"` key removed from installed.json template
- [ ] `mcp/findings-server/README.md` — updated placeholder noting global JSONL architecture
- [ ] `_bmad-output/planning-artifacts/architecture.md` — Decisions 1c, 2a, 3c updated; schema updated; structure diagrams updated
- [ ] `_bmad-output/planning-artifacts/epics.md` — Stories 6.1-6.5 updated for global JSONL
- [ ] `.claude/settings.local.json` — `enabledMcpjsonServers` removed entirely (local, not committed)

## Dev Notes

**Change types:**
- `config-structure`: `.mcp.json`, `mcp-config.json`, `momentum-versions.json`, `settings.local.json`
- `skill-instruction`: `workflow.md`
- `docs`: `architecture.md`, `epics.md`, `README.md`

**Overlap with p1.1:** Story p1.1 removes the git MCP server. This story (p1.3) removes the findings MCP placeholder and revises the architecture. Both touch `.mcp.json`, `mcp-config.json`, and `workflow.md`. p1.3 depends on p1.1 — run p1.1 first.
