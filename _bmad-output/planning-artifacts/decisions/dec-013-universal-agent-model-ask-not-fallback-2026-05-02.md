---
id: DEC-013
title: Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery
date: '2026-05-02'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-02'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines — extended: no separate Momentum-internal category)
  - DEC-008 (Composable Agents Architecture — extended: ask/recommend replaces halt, sprint planning adds extensibility)
architecture_decisions_affected:
  - DEC-001 — extended: "Momentum-internal" agents are not a separate category; all agent types follow the same model
  - DEC-008 D4 — refined: no-fallback posture becomes ask/recommend posture; developer always decides
stories_affected:
  - agent-spawn-preflight-check
  - build-guidelines-skill
  - agents-md-manifest-format (new story needed)
  - missing-base-bodies-audit (new story needed)
---

# DEC-013: Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery

## Summary

Three decisions emerged from a conversation about extending the composable agents
architecture beyond dev specialists. D1 eliminates the "Momentum-internal" agent
category — all agent types follow the same model; a project simply chooses which
ones to compose and which to leave at the base body. D2 refines the no-fallback
posture from DEC-008 D4: the skill never silently degrades to a base body, but it
also never halts unilaterally — instead it surfaces the gap and asks the developer
to decide. D3 establishes sprint planning as a runtime discovery mechanism for new
agent types: the catalog of agent types is not fixed at design time, and sprint
planning can identify and name new specialist types as it classifies stories.

---

## Decisions

### D1: No separate Momentum-internal agent category — ADOPTED

**Developer framing:** We explored whether Momentum's workflow agents (retro
auditors, distill enumerator/adversary, feature-grooming discovery agents, etc.)
needed a separate "Momentum-internal" bucket because they work on Momentum artifacts
(sprint transcripts, PRDs, epics) rather than project code.

**Decision:** Reject the distinction. All agent types follow the same model — base
body in the plugin, optional project-composed file in `.claude/guidelines/agents/`.
Whether an agent needs project composition is a per-project decision, not a
categorical one. A project that decides the base retro-auditor is sufficient uses
it as-is. A project that wants specialized auditing runs `build-guidelines` to
compose a customized version. The plugin ships base bodies for all known agent
types; the project decides which to compose.

**Rationale:** The "Momentum-internal" distinction required deciding upfront which
agent types could ever benefit from project conditioning. That's impossible to
know in advance — a complex security project might need specialized retro auditors;
Momentum itself needs dev-skills agents conditioned on SKILL.md format. One model
handles all cases. The base body is the floor; composition is always available.

---

### D2: Ask/recommend on missing agent — not silent fallback, not unilateral halt — ADOPTED

**Developer framing:** DEC-008 D4 said sprint-dev halts when a required composed
specialist is missing. We explored whether all skills should follow the same halt
behavior or whether silent fallback to the base body was acceptable.

**Decision:** Neither. When a skill needs an agent type and no composed file exists,
it surfaces the gap and asks the developer. Example:

> "This sprint has Python backend stories. No `dev-python-fastapi.md` found.
> Base body `dev.md` is available. Run `/momentum:build-guidelines` to compose
> a project-specific agent, or confirm you want to proceed with the base body."

The developer decides. The skill never silently degrades (no automatic fallback),
and it never halts without giving the developer a path forward. The `required`
flag in the `agents.md` manifest controls whether missing composed files trigger
a stronger recommendation — but even for required types the developer gets a
choice, not a unilateral block.

**Rationale:** Silent fallback hides quality gaps. Unilateral halt blocks progress
when the base body is genuinely acceptable. Asking respects developer agency,
surfaces the gap explicitly, and lets the developer make an informed tradeoff.
Consistent with DEC-008 D2's soft-stop posture.

---

### D3: Sprint planning as runtime agent-type discovery mechanism — ADOPTED

**Developer framing:** The `agents.md` manifest in each skill was being designed
as a fixed registry of agent types. We explored whether the catalog of agent types
could be extended at runtime.

**Decision:** Adopt sprint planning as a discovery mechanism for new agent types.
When classifying stories, sprint planning may identify that a story or cluster of
stories would benefit from a specialist type that does not yet exist (no base body,
no composed file). Sprint planning surfaces this:

> "Three stories touch the database migration path. A `db-migration-specialist`
> agent would be appropriate. No base body or composed file exists. Run
> `/momentum:build-guidelines` to define and generate it."

The `agents.md` manifest inside each skill is a **seed list** (minimum known set),
not a closed registry. Sprint planning can grow the project's agent pool. Other
skills (quick-fix, retro) can similarly surface agent type gaps when they encounter
work that a known type handles poorly.

`build-guidelines` handles both: composing known base types with project knowledge,
and defining new agent types from scratch when the project's needs exceed the
plugin's catalog.

**Rationale:** Projects cannot enumerate all specialist types they will ever need
at setup time. Complex projects evolve — new technical domains emerge, new quality
concerns surface. Making the agent type catalog extensible at runtime means the
agent pool grows with the project rather than being fixed at day one. Sprint
planning is the natural discovery point because it classifies every story and has
full visibility into what technical domains the sprint touches.

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|---|---|---|---|
| Gate 1 (D2) | After ask/recommend UX ships in sprint-dev | Is the ask pattern effective in practice? | Developers respond by running build-guidelines or confirming base body, not by disabling the check |
| Gate 2 (D3) | After first sprint where planning discovers a new type | Does runtime type discovery actually happen? | Sprint planning surfaces at least one new agent type that build-guidelines then creates |
