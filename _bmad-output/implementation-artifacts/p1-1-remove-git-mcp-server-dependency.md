---
story_id: p1.1
status: ready
type: process
epic: P1 — Process Sprint-1
title: Remove Git MCP Server Dependency
sprint: 1
touches:
  - ".mcp.json"
  - "skills/momentum/references/mcp-config.json"
  - "skills/momentum/workflow.md"
  - "_bmad-output/planning-artifacts/architecture.md"
  - "_bmad-output/planning-artifacts/epics.md"
  - "_bmad-output/planning-artifacts/ux-design-specification.md"
  - "_bmad-output/implementation-artifacts/1-1-repository-structure-established.md"
  - "_bmad-output/implementation-artifacts/1-3-first-momentum-invocation-completes-setup.md"
depends_on: []
---

# Remove Git MCP Server Dependency

## User Story

As a Momentum developer,
I want to remove the `@modelcontextprotocol/server-git` MCP server dependency,
So that the installation is leaner, avoids an unnecessary npx download, frees a tool-ceiling slot, and eliminates a redundant permission surface.

## Background

The architecture (Decision 3c) specified `@modelcontextprotocol/server-git` for provenance tracking — file history, blame, and diff. After architect review, this dependency provides zero capabilities beyond what Claude Code already has via the git CLI and Bash tool. The provenance system (Epic 5) is 100% architecturally designed but 0% implemented, and its own design already uses `git hash-object` via CLI with "zero extra tooling" (Decision 1a) — not via MCP.

The Git MCP adds:
- An npx download dependency (`@modelcontextprotocol/server-git`) on each MCP server activation
- A tool-ceiling slot consumed (Cursor ~40 tool limit)
- A second permission surface with no additional safety benefit

Removal is fully reversible — one config line to re-add if ever needed.

## Acceptance Criteria

```gherkin
Scenario: Git MCP server entry removed from active config
  Given the project .mcp.json file exists
  When I inspect its contents
  Then there is no "git" server entry
  And the findings MCP server entry is preserved

Scenario: Git MCP removed from install template
  Given the Impetus skill template at skills/momentum/references/mcp-config.json
  When I inspect its contents
  Then there is no "git" server entry
  And the findings MCP server entry is preserved

Scenario: Workflow output no longer references Git MCP
  Given the Impetus workflow at skills/momentum/workflow.md
  When I inspect its output messages
  Then no output line mentions "Git MCP"

Scenario: Architecture spec reflects removal decision
  Given the architecture document at _bmad-output/planning-artifacts/architecture.md
  When I read Decision 3c
  Then the Git MCP row is marked as removed or absent
  And the rationale for removal is documented

Scenario: No residual references to Git MCP in active code
  Given the full project codebase
  When I grep for "modelcontextprotocol/server-git" and "Git MCP"
  Then zero matches appear in active code/config files
  And spec artifacts document the removal decision rather than the original reference
```

## Definition of Done

- [ ] `.mcp.json` — git server entry removed, findings server preserved
- [ ] `skills/momentum/references/mcp-config.json` — git server entry removed from template
- [ ] `skills/momentum/workflow.md` — Git MCP output line updated (remove "Git MCP" label)
- [ ] `_bmad-output/planning-artifacts/architecture.md` — Decision 3c updated to reflect removal with rationale
- [ ] `_bmad-output/planning-artifacts/epics.md` — MCP Servers summary (line 170) updated; Story 7.5 Given clause (line 1698) updated to remove "git MCP"
- [ ] `_bmad-output/planning-artifacts/ux-design-specification.md` — Git MCP output example (line 618) updated
- [ ] `_bmad-output/implementation-artifacts/1-1-repository-structure-established.md` — Task 5 Dev Notes embedded JSON schema (lines 230-234) updated to remove git server entry
- [ ] `_bmad-output/implementation-artifacts/1-3-first-momentum-invocation-completes-setup.md` — Git MCP output reference (line 269) updated

## Dev Notes

**Change type:** `config-structure` (primary: JSON config files, workflow output) + `docs` (spec artifact updates)

**Risk:** Minimal. No functionality loss — nothing currently implemented uses the Git MCP. CLI git provides all needed operations. Fully reversible.

**Confirmed no changes needed:** Story 1.4 (`1-4-momentum-detects-and-applies-upgrades.md`) — verified zero Git MCP references.

**Scope guard:** Do NOT modify any provenance architecture design (Epic 5). The provenance system design is sound — only the tooling dependency reference changes. Do NOT remove the findings MCP server entry.
