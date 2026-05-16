---
id: DEC-027
title: Skill/Agent Development — Skill-Creator Pipeline + Change-Type Routing in Sprint-Dev
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-008 (Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy)
  - DEC-013 (Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery)
  - DEC-020 (Universal Agent Role Taxonomy — BMAD-Aligned Base Bodies)
  - DEC-026 (Build Pipeline Redesign — build-agents, agent-builder, constitution-builder Rework)
architecture_decisions_affected:
  - DEC-008 D1 — extends the three-tier layout with change_type-specific routing in sprint execution
stories_affected:
  - dev-skills implied retirement (handled in base-body-collapse-rollback)
  - change-type-routing-in-sprint-dev (new — sprint-dev Phase 2 routing logic)
  - skill-agent-story-spec-mig-template (new — create-story MIG injection for change_type: skill/agent)
  - sprint-dev-composed-file-spawn-wiring (update — must handle change_type routing)
---

# DEC-027: Skill/Agent Development — Skill-Creator Pipeline + Change-Type Routing in Sprint-Dev

## Summary

skill-creator is used for building both skills and agent definitions. Agent base bodies and composed agent files are markdown system prompts; skill-creator's eval loop (draft → parallel test runs → grader → iteration) applies equally well to agent definitions. No separate "agent eval" tooling is needed.

create-story serves as the context bridge for skill and agent stories, distilling constitution knowledge into the story spec's MIG section. skill-creator starts from this spec — the interview phase is pre-answered by create-story. The constitution is not injected directly into skill-creator.

sprint-dev routes based on `change_type`: skill and agent stories bypass bmad-dev-story and route to a skill-building subagent. The subagent runs skill-creator in autonomous mode with a developer approval gate after completion. dev-skills is retired as its only purpose (building SKILL.md files) is now handled by skill-creator.

## Decisions

### D1: skill-creator used for both skills and agents — ADOPTED

**Developer framing:** Does agent definition development require its own eval tooling, or can skill-creator handle it?

**Decision:** skill-creator is used for both skills and agent definitions. The eval loop (draft → parallel test runs → grader → iteration) works for agent definitions just as well as skills. No separate "agent eval" tooling needed.

**Rationale:** Agent base bodies and composed agent files are markdown system prompts — the same artifact type as skills. skill-creator's testing model is simpler and better-suited than AVFL for prompt artifacts. Reusing skill-creator eliminates the need to build, maintain, and learn a separate evaluation pipeline.

---

### D2: create-story is the context bridge — ADOPTED

**Developer framing:** How does skill-creator receive project-specific context (stack, conventions, architectural patterns) for skill and agent stories without being tightly coupled to constitution.md?

**Decision:** For `change_type: skill` or `agent`, create-story reads `constitution.md`, `architecture.md`, and project patterns, then distills relevant knowledge into the story spec's MIG section. skill-creator starts from this spec — the interview phase is pre-answered. The constitution is NOT injected directly into skill-creator.

**Rationale:** create-story already reads these documents as part of its normal story creation flow. Embedding context in the spec makes it explicit and reviewable before skill-creator runs. Direct constitution injection into skill-creator would couple the two tools in a way that's hard to debug when context is incorrect or stale.

---

### D3: change_type routing in sprint-dev — ADOPTED

**Developer framing:** How does sprint-dev route execution differently for skill/agent stories versus feature/bug stories?

**Decision:** sprint-dev Phase 2 reads `change_type` before spawning. Routing table:

| change_type | Path |
|---|---|
| feature/bug | bmad-dev-story + worktree + AVFL + team review |
| skill | skill-building subagent → skill-creator autonomous mode |
| agent | skill-building subagent → agent-builder (wraps skill-creator) |
| rule/hook | direct edit + commit (no spawn) |
| docs | role-appropriate writer agent + lightweight AVFL checkpoint |

**Rationale:** Skill/agent stories don't need worktrees, merge gates, or AVFL spec validation; they need behavioral eval + human review. Feature/bug stories need the full development and verification pipeline. Routing at the change_type boundary prevents over-engineering simple changes (rule/hook) and under-engineering complex ones (feature).

---

### D4: Autonomous skill-creator mode with approval gate — ADOPTED

**Developer framing:** Should skill development within sprint-dev require interactive developer feedback during the build loop, or can it run autonomously?

**Decision:** sprint-dev spawns a skill-building subagent with skill-creator available. The subagent runs skill-creator in autonomous mode: draft → 2-3 evals (parallel subagents) → programmatic grading → one improvement pass → commit. No browser viewer, no interactive feedback loop. sprint-dev then presents the built artifact + eval summary to the developer as an approval gate before moving on. Developer can approve or flag for iteration.

**Rationale:** Removes the human-in-the-loop inner loop from the sprint while preserving human judgment at the gate. The autonomous loop is fast and produces a concrete artifact with eval evidence; the approval gate gives the developer visibility and control at the right level of abstraction.

---

### D5: dev-skills agent retired — ADOPTED

**Developer framing:** Is the dev-skills agent still needed after skill-creator covers skill and agent development?

**Decision:** agents/dev-skills.md is removed as part of base-body-collapse-rollback. skill-creator replaces the need for a specialist agent that builds skills.

**Rationale:** dev-skills' only purpose was to build/edit SKILL.md files; skill-creator does this better with a built-in eval system. Maintaining a separate specialist agent for a task that skill-creator handles more rigorously creates confusion about which path to use and adds file inventory overhead without capability benefit.
