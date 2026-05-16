---
id: DEC-020
title: Universal Agent Role Taxonomy — BMAD-Aligned Base Bodies
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines Architecture)
  - DEC-008 (Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy)
  - DEC-013 (Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery)
  - DEC-016 (Agent Taxonomy — Two-Tier Shipped/Customs Model)
architecture_decisions_affected:
  - DEC-016 — partially superseded; Tier A/B taxonomy replaced by nine universal roles
stories_affected:
  - code-reviewer-agent-definition (closed)
  - architect-guard-agent-definition (closed)
  - documenter-agent-definition (closed — rename to retro-synthesizer in workflow if needed)
  - dev-fixer-agent-definition (closed)
  - ux-base-body (new)
  - analyst-base-body (new)
  - researcher-base-body (new)
---

# DEC-020: Universal Agent Role Taxonomy — BMAD-Aligned Base Bodies

## Summary

Nine universal base body roles are established, aligned with BMAD role naming but adapted for orchestrator-spawned (non-interactive) subagent use. These are plugin-shipped markdown files in `skills/momentum/agents/` and define role identity, behavioral constraints, output format contract, and file ownership scope for each named role.

Several previously-planned role definitions are closed as unnecessary. code-reviewer and architect-guard are not separate base bodies — they are the dev and architect roles invoked through a skill with `context:fork` + `allowed-tools: Read` applied at spawn time. The retro synthesizer is an inline spawn, not a typed role. dev-fixer is a behavioral constraint pattern, not a base body. Three new base bodies (ux, analyst, researcher) are created to fill gaps in the taxonomy.

The nine-role taxonomy aligns with BMAD's proven vocabulary and gives every project a consistent foundation for agent composition. The closures reduce the taxonomy surface by eliminating roles that existed solely to express caller-side constraints — a concern that belongs at the call site, not in the role definition.

## Decisions

### D1: Nine universal base bodies — ADOPTED

**Developer framing:** What is the canonical set of agent roles the plugin ships, and how do they align with BMAD's role vocabulary?

**Decision:** Nine roles: architect, pm, ux, analyst, researcher, dev, sm, qa, e2e. These are plugin-shipped markdown files in `skills/momentum/agents/`. Each defines role identity, behavioral constraints, output format contract, and file ownership scope.

**Rationale:** Aligns with BMAD's proven role taxonomy; gives every project a consistent vocabulary for agent composition. The nine roles cover the full practice pipeline from research and analysis through design, development, and verification.

---

### D2: code-reviewer and architect-guard are NOT separate base bodies — ADOPTED

**Developer framing:** Should code-reviewer and architect-guard have their own base body files, or can they be expressed as constrained invocations of existing roles?

**Decision:** These are the dev and architect roles invoked through a skill with `context:fork` + `allowed-tools: Read` applied at spawn time. No separate base body files needed. The skill wrapper provides the permission constraint; the harness enforces it. Closes stories: code-reviewer-agent-definition, architect-guard-agent-definition.

**Rationale:** The constraint is a caller concern, not a role concern. Any role can be invoked read-only. Creating separate base bodies for read-only variants would multiply files without adding meaningful differentiation in role identity or behavioral contract.

---

### D3: Retro synthesizer is an inline spawn, not a typed role — ADOPTED

**Developer framing:** Does the retro synthesizer need its own base body file, or can it be handled inline?

**Decision:** The retro synthesizer receives three findings blocks inline in its prompt and writes the retro document. No plugin agent file needed. Closes story: documenter-agent-definition (rename to retro-synthesizer in the workflow if needed).

**Rationale:** It's a write-with-synthesis pattern, not a reusable role contract. The synthesizer's behavior is fully specified by its inline prompt context; extracting it to a base body adds file overhead without enabling reuse across other workflows.

---

### D4: dev-fixer is a constraint pattern, not a base body — ADOPTED

**Developer framing:** Should dev-fixer have its own base body, or is it better expressed as a constraint applied to another role?

**Decision:** No dev-fixer.md. AVFL findings carry document-type metadata; the fix spawn resolves the routing table to find the document owner and applies a fix-constraint prompt (bounded executor, no scope expansion). Closes story: dev-fixer-agent-definition. See DEC-025 for full fixer routing design.

**Rationale:** The fix constraint is behavioral, applied by the orchestrator; the role identity comes from document ownership. A generic dev-fixer role would lack the domain knowledge needed to fix specialized artifact types correctly.

---

### D5: Three new base bodies needed — ADOPTED

**Developer framing:** Are there gaps in the existing base body set that require new files?

**Decision:** ux-base-body, analyst-base-body, and researcher-base-body stories are created. These roles (UX designer, business analyst, researcher) exist in BMAD and have natural document ownership in the Momentum pipeline.

**Rationale:** The ux, analyst, and researcher roles each own distinct artifact families (UX specs, assessments, research documents) that require role-specific identity, behavioral constraints, and output format contracts. They cannot be subsumed into existing roles without losing the ownership clarity the taxonomy is designed to provide.
