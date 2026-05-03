---
id: DEC-015
title: KB Cold-Context Delivery — Workflow Steps, Prescriptive Constitution Triggers, Skills Audit
date: '2026-05-02'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-02'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines — establishes cold KB as Tier 3, on-demand retrieval)
  - DEC-008 D3 (KB-to-guidelines integration contract — deferred until KB real; this SDR partially resolves it by establishing ownership and delivery patterns)
  - DEC-009 (KB vault orchestration model — establishes index-first navigation pattern)
stories_affected:
  - build-guidelines-skill
  - vault-claudemd-navigation-contract-spec
  - sprint-dev-composed-file-spawn-wiring
  - kb-init
---

# DEC-015: KB Cold-Context Delivery — Workflow Steps, Prescriptive Constitution Triggers, Skills Audit

## Summary

Three complementary decisions govern how spawned agents and skills receive KB cold-context. Orchestrator-level injection (having the orchestrator pre-fetch and inject KB excerpts) is rejected as the primary mechanism — orchestrators won't reliably remember to look any better than agents themselves. The primary patterns are: (1) explicit KB query steps baked into composed Tier 2 agent files and planning skill workflows, and (2) prescriptive, scenario-specific constitution triggers that name the exact situations requiring a KB lookup rather than relying on agent judgment. A full skills audit is commissioned to find every injection point across all Momentum skills. The unifying rationale: LLMs always prefer training data over external lookup; passive permission to consult the KB is effectively no instruction.

---

## Decisions

### D1: Orchestrator-injected KB excerpts at spawn time — REJECTED as primary

**Developer framing:** The orchestrator (sprint-dev or Impetus) runs the KB lookup before spawning an agent and injects relevant excerpts directly into the spawn prompt. The agent never has to decide to check — the context is already present.

**Decision:** Reject as the primary mechanism. Fine as a secondary convenience where obvious, but not the load-bearing pattern. Orchestrators won't reliably remember to look any better than the agents themselves — the failure mode is the same.

**Rationale:**
Option 1 is fine but weak. The orchestrator is unlikely to remember any better than the agents themselves.

---

### D2: Explicit KB query steps in composed agent files and planning workflows — ADOPTED, extended

**Developer framing:** Rather than advisory instructions, the agent's Tier 2 composed file or the skill's workflow includes an explicit required step: grep `index.md` for the relevant topic, read the targeted page. Structural — can't be skipped.

**Decision:** Adopt, and extend beyond agent files to planning skill workflows. Any Momentum skill that builds artifacts, selects patterns, or makes domain recommendations must include an explicit KB query step at the appropriate point. Specifically: `create-story`, sprint-planning, and any workflow step that makes a domain decision is a candidate. The step is required, not advisory.

**Rationale:**
Option 2 is fine wherever it fits. Also need to add this to planning modes — when building out stories and doing sprint planning, there needs to be a place where the KB is queried. Every skill should be audited to find where queries can be added.

---

### D3: Hot constitution KB triggers — ADAPTED (prescriptive, not permissive)

**Developer framing:** The hot constitution (Tier 1) includes a pointer telling agents when to use the Tier 3 cold KB. Current framing was permissive: "if you need domain knowledge, check the KB."

**Decision:** Adopt, but rewrite as prescriptive. Replace permissive language with specific named scenarios — enumerate the exact moments that require a KB query (e.g., "when classifying a story's domain", "when selecting a test pattern for a new library", "when choosing between two library approaches on this stack"). Do not say "if you need" — say "when doing X, query the KB before proceeding."

**Rationale:**
The language needs to be stronger than "if you need." The LLM will always prefer using training data. Vague permission to query is effectively no instruction. The constitution must name specific reasons and scenarios so the agent has no judgment call to make — it's a required action in a named context.

---

### D4: Full skills audit for KB query injection points — ADOPTED

**Developer framing:** Every Momentum skill should be reviewed to find places where a KB query step can be added — any step that makes a domain decision, selects a pattern, or produces a technical recommendation.

**Decision:** Adopt. Commission a skills audit covering every Momentum skill. For each skill, identify steps that make domain decisions, select technical patterns, or produce recommendations, and evaluate whether a KB query belongs before that step. Output: an annotated list of injection points, with proposed step language. This drives subsequent story creation.

**Rationale:**
Every one of our skills should be audited to see if there are places we can add queries.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 1 | KB infrastructure | Before any injection work | `kb-init`, `kb-ingest` — vault must exist before query steps are meaningful |
| 2 | Constitution rewrite | After KB ships | `build-guidelines-skill` — Tier 1 gets prescriptive KB trigger language |
| 3 | Skills audit | Parallel with Phase 2 | New story: `skills-kb-query-injection-audit` — enumerate all injection points |
| 4 | Injection implementation | After audit | Per-skill stories from audit output — add required KB query steps |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | When KB is real (kb-init + kb-ingest shipped) | Does prescriptive constitution language actually drive lookup behavior? | Agents running in sprint-dev demonstrably query the KB in named scenarios instead of relying on training data |
| Gate 2 | After skills audit completes | Are the identified injection points implementable without excessive workflow bloat? | Audit output is actionable; injection steps add value without adding friction to every skill invocation |
