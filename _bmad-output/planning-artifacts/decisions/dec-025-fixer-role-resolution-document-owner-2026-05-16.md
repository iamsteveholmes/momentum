---
id: DEC-025
title: Fixer Role Resolution — Document Owner + Fix Constraint, No dev-fixer Base Body
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-008 (Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy)
  - DEC-020 (Universal Agent Role Taxonomy — BMAD-Aligned Base Bodies)
  - DEC-023 (Agent Routing Table — Machine-Readable Registry with 1..N Fan-Out)
architecture_decisions_affected:
  - DEC-020 D4 — implements the fixer routing described in D4 of the taxonomy decision
stories_affected:
  - dev-fixer-agent-definition (closed)
  - avfl fixer phase spawn logic (update — implement routing-table resolution)
---

# DEC-025: Fixer Role Resolution — Document Owner + Fix Constraint, No dev-fixer Base Body

## Summary

AVFL's fix phase resolves the document owner from the routing table rather than spawning a generic dev-fixer. Findings carry document-type metadata (file path of the affected artifact). The fix-constraint (bounded executor, no scope expansion, escalate if ambiguous) is a prompt injected by the orchestrator at spawn time, not a separate role definition.

This closes the dev-fixer-agent-definition story. The fix role has no independent identity — it is always "document owner + fix constraint." The fixer selection is automatic and correct because the routing table already knows which agent owns each file pattern; no orchestrator-level routing logic is needed.

## Decisions

### D1: No dev-fixer base body — ADOPTED

**Developer framing:** Should AVFL's fix phase use a dedicated dev-fixer agent, or can it resolve the correct fixer from existing roles?

**Decision:** No dev-fixer.md. dev-fixer-agent-definition story is closed. The fix role is a behavioral constraint (fix only what's in the finding, no scope expansion, no additions) applied to whatever agent owns the document being fixed.

**Rationale:** The role identity is "document owner"; the fix constraint is orthogonal to role identity. A generic dev-fixer role would lack the domain knowledge needed to fix specialized artifact types correctly. For example, a finding in architecture.md requires an architect to fix it; a finding in a Compose UI file requires the dev-cmp agent.

---

### D2: AVFL findings carry document-type metadata — ADOPTED

**Developer framing:** How does the AVFL fix phase know which agent to spawn for a given finding?

**Decision:** Each AVFL finding includes the file path of the affected artifact. The fix phase groups findings by file path, resolves the routing table for each group, and spawns the appropriate owner agent with the fix-constraint prompt. A story touching Compose files gets dev-cmp + fix-constraint; a finding in architecture.md gets architect + fix-constraint.

**Rationale:** Makes fixer selection automatic and correct; eliminates mismatches between finding type and fixing agent. The file path is the natural join key between findings and the routing table — no additional metadata classification is needed.

---

### D3: Fix-constraint prompt is orchestrator-injected — ADOPTED

**Developer framing:** Where should the fix-constraint ("implement only this specific finding, no additions, no interpretation, escalate if ambiguous") live — in a base body or injected at spawn time?

**Decision:** The fix-constraint is injected by the AVFL orchestrator at spawn time, not baked into any base body.

**Rationale:** The constraint is context-specific (this finding, this file, this iteration of the fix loop). Baking it into a base body would make the base body unusable outside the AVFL fix phase context, or require the base body to carry conditional logic about whether it's running in fix mode. The injection pattern keeps base bodies clean and single-purpose.
