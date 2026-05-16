---
id: DEC-023
title: Agent Routing Table — Machine-Readable Registry with 1..N Fan-Out
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-008 (Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy)
  - DEC-013 (Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery)
  - DEC-016 (Agent Taxonomy — Two-Tier Shipped/Customs Model)
architecture_decisions_affected:
  - DEC-016 D3 — superseded; agents.md manifest per-skill replaced by project-level routing table
stories_affected:
  - specialist-classify-update-for-gen-2-paths (scope expanded to multi-result)
  - sprint-dev-composed-file-spawn-wiring (routing-table-driven)
  - agents-md-manifest-format (closed — replaced by routing table)
  - routing-table-schema-and-implementation (new)
---

# DEC-023: Agent Routing Table — Machine-Readable Registry with 1..N Fan-Out

## Summary

A machine-readable JSON routing table (`momentum/agents.json`) replaces the implicit agent resolution currently hardcoded in sprint-dev and specialist-classify. The table has a `defaults` section (plugin-provided, one entry per universal role) and a `project` section (written by build-agents, one entry per role × domain combination with file patterns and write permissions).

Every skill that spawns a typed role resolves 1..N agents from the table based on the relevant file list, each scoped to its file domain. This eliminates the single-agent assumption embedded in the current sprint-dev implementation and makes multi-domain stories work correctly without orchestrator-level knowledge of project layout. build-agents writes routing entries as the last step of agent creation, keeping the table in sync automatically.

## Decisions

### D1: `momentum/agents.json` as routing table — ADOPTED

**Developer framing:** How should agent resolution be made explicit, auditable, and consistent across all skills?

**Decision:** Establish `momentum/agents.json` as the routing table with the following format:
```json
{
  "defaults": {
    "dev": "skills/momentum/agents/dev.md",
    "architect": "skills/momentum/agents/architect.md"
  },
  "project": [
    {
      "role": "dev",
      "slug": "dev-cmp",
      "agent": ".claude/guidelines/agents/dev-cmp.md",
      "patterns": ["**/src/**/ui/**", "**/*.kt"],
      "write_permissions": ["src/main/kotlin/**/ui/**"]
    }
  ]
}
```
Defaults are plugin-provided (always present). Project entries are written by build-agents.

**Rationale:** Makes agent resolution explicit, auditable, and consistent across all skills. Any skill can perform the same lookup and get the same result; there is no implicit resolution logic scattered across multiple skill implementations.

---

### D2: 1..N fan-out is the universal spawning pattern — ADOPTED

**Developer framing:** Should every skill that spawns a typed role support multi-domain stories, or only sprint-dev?

**Decision:** Every skill that spawns a typed role (not just sprint-dev) must: (1) collect relevant files (story.touches, git diff, finding.file_path, etc.); (2) look up routing table — group files by matching agent; (3) spawn one agent per group, each scoped to its file domain; (4) apply write_permissions per agent at spawn time (enforced by harness). If no project entry matches, fall back to defaults.

**Rationale:** Eliminates hardcoded single-agent assumptions; makes multi-domain stories work correctly without orchestrator-level knowledge of project layout. Applying the pattern universally prevents new skills from re-introducing the single-agent assumption.

---

### D3: write_permissions enforced at spawn time — ADOPTED

**Developer framing:** How are file write permissions enforced for routed agents?

**Decision:** Each routing table entry carries `write_permissions` (array of Edit() patterns). When spawning that agent, the skill injects these as tool-permission constraints. The harness enforces them — the agent cannot write outside its domain regardless of intent. Read-only invocations (code-review, architecture-guard) pass empty `write_permissions`.

**Rationale:** Permission walls are structural, not behavioral. An agent that intends to respect its domain but makes an error is still constrained. Behavioral constraints (prompt-level) are advisory; structural constraints (harness-enforced) are reliable.

---

### D4: specialist-classify returns N results — ADOPTED

**Developer framing:** Does the current specialist-classify interface need to change to support routing-table-driven fan-out?

**Decision:** Currently returns one string. Must return an array of `{slug, agent_path, file_scope}` tuples. All callers (sprint-dev, quick-fix, code-review) iterate the array and spawn accordingly.

**Rationale:** Single-result API cannot express multi-domain stories. All callers need the same multi-result interface to implement the universal fan-out pattern correctly.

---

### D5: build-agents writes routing entry on agent creation — ADOPTED

**Developer framing:** How is the routing table kept in sync with composed agent files?

**Decision:** The last step of agent-builder (called by build-agents) appends a routing entry to `momentum/agents.json`. The routing table stays in sync with composed agent files automatically. No manual registration step.

**Rationale:** Manual registration is error-prone and creates a class of bugs where an agent file exists but sprint-dev cannot find it. Automatic registration at creation time eliminates this failure mode entirely.
