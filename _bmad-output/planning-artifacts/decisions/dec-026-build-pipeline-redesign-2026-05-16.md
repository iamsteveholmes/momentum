---
id: DEC-026
title: Build Pipeline Redesign — build-agents, agent-builder, constitution-builder Rework
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines Architecture)
  - DEC-008 (Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy)
  - DEC-015 (KB Cold-Context Delivery — Workflow Steps, Prescriptive Constitution Triggers, Skills Audit)
  - DEC-018 (Obsidian Wiki Skills Replace Planned KB Stories — wiki-query as Cold KB Interface)
architecture_decisions_affected:
  - DEC-008 D1 — partially superseded; build-guidelines renamed to build-agents, constitution scope narrowed to domain knowledge only
stories_affected:
  - build-guidelines-skill (closed — rename + scope change covers this)
  - agent-guidelines (closed — retirement story needed)
  - constitution-builder-write-mode-parameterization (update — ACs must reflect domain-knowledge-only scope)
  - build-guidelines-invocation-surface-in-sprint-planning (update — rename to build-agents)
  - agent-builder-skill (new)
---

# DEC-026: Build Pipeline Redesign — build-agents, agent-builder, constitution-builder Rework

## Summary

The agent-building pipeline is renamed and restructured into a clean three-skill sequence. build-guidelines becomes build-agents (project-setup orchestrator). A new agent-builder skill handles per-agent composition (base body + manifesto + permissions → composed file + routing entry). constitution-builder is reworked to generate domain knowledge only — routing and agent-specific configuration moves to agent-builder. agent-guidelines (Gen-1) is retired.

The three-skill pipeline is: constitution-builder (Tier 1, run once per project) → agent-builder × N (Tier 2, run once per role × domain) → routing table complete. build-agents orchestrates both tiers. The separation between shared project knowledge (constitution) and agent-specific routing (manifesto) prevents the constitution from becoming a kitchen-sink document that grows unbounded as projects add agents.

## Decisions

### D1: agent-guidelines retired — ADOPTED

**Developer framing:** Is the Gen-1 stack-rule generator (agent-guidelines skill) still needed after the Gen-2 pipeline?

**Decision:** agent-guidelines is superseded by the constitution-builder + agent-builder pipeline. Its 4 scanner sub-skills (build-scanner, rules-auditor, test-config-scanner, source-pattern-scanner) may survive as standalone discovery primitives if needed, but the generation step is replaced. Story needed: retire agent-guidelines skill, evaluate scanner sub-skill reuse.

**Rationale:** The Gen-1 generator produces undifferentiated stack rules that are not scoped to roles or domains. The Gen-2 pipeline produces role-specific composed files with explicit ownership and routing. The Gen-1 output is a strict subset of what Gen-2 produces, and maintaining both creates confusion about which pipeline to use.

---

### D2: build-guidelines renamed to build-agents — ADOPTED

**Developer framing:** Does the build-guidelines name still reflect what the skill does after these changes?

**Decision:** build-guidelines → build-agents. It is the project-setup orchestrator: calls constitution-builder once (Tier 1) and agent-builder N times (once per role × domain), then ensures routing table is complete. Developer runs `/momentum:build-agents` when starting a project or adding a new stack.

**Rationale:** The name reflects the output (built agents), not the intermediate artifact (guidelines). The developer's mental model is "I need agents for this project" not "I need guidelines files."

---

### D3: New agent-builder skill — ADOPTED

**Developer framing:** What skill handles per-agent composition in the Gen-2 pipeline?

**Decision:** agent-builder is a new skill that produces one composed agent file. Inputs: base body (from plugin), constitution excerpt (from `momentum/architecture/constitution.md`), manifesto inputs (role × domain specifics from story spec). Output: `.claude/guidelines/agents/{role}-{domain}.md` + routing entry in `momentum/agents.json`. Wraps skill-creator with an agent-specific starting template. See DEC-027 for how skill-creator is used in execution.

**Rationale:** A dedicated agent-builder skill provides a consistent interface for producing composed agent files. Without it, the composition logic would be scattered across build-agents (too high-level) or skill-creator (too generic).

---

### D4: constitution-builder rework — domain knowledge only — ADOPTED

**Developer framing:** What should the constitution contain after routing and agent-specific configuration moves to agent-builder?

**Decision:** constitution-builder generates ONLY project domain knowledge after rework: stack facts, conventions, and architectural patterns shared by all agents. Routing moves to agent-builder (agent-specific routing per role × domain). The wiki-query interface block (DEC-018) stays in the constitution as shared infrastructure available to all agents.

**Rationale:** Separates shared project knowledge (constitution) from agent-specific routing (manifesto); prevents the constitution from becoming a kitchen-sink document. The constitution should be stable and slow-changing; routing is agent-specific and changes as project domains evolve.

---

### D5: Three-skill pipeline — ADOPTED

**Developer framing:** What is the canonical sequence for building agents in a project?

**Decision:** constitution-builder (Tier 1, once) → agent-builder × N (Tier 2, per role × domain) → routing table complete. build-agents orchestrates both. Replaces the single build-guidelines skill with ambiguous scope.

**Rationale:** The three-skill pipeline has clear separation of concerns: shared knowledge (Tier 1), per-agent composition (Tier 2), registration (automatic via agent-builder). Each tier can be re-run independently when its inputs change — re-run constitution-builder when the stack changes; re-run agent-builder for a specific role when that domain changes.
