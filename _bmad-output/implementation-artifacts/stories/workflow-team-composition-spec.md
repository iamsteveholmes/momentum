---
title: Workflow Team Composition Spec — Codify Required Roles and Spawning Modes
story_key: workflow-team-composition-spec
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/avfl/SKILL.md
  - skills/momentum/skills/sprint-planning/workflow.md
change_type: skill-instruction
---

# Workflow Team Composition Spec — Codify Required Roles and Spawning Modes

## Description

Sprint-2026-04-06 retro revealed that 6 of 10 user corrections were about
team composition and spawning. Specific failures:

- **Missing dev/fixer agent:** AVFL team was composed without a dev/fixer
  agent twice. The user had to ask "Where is the dev agent?"
- **Wrong spawning mode:** Wave agents were spawned as TeamCreate groups
  when they should have been individual Agent spawns. User had to correct:
  "Why are wave agents coming as teams? Absolutely should not be."
- **Role ambiguity:** No workflow explicitly declares which roles are
  required vs. optional for a given phase, so Impetus improvised — badly.

The root cause is that team composition rules are implicit. The sprint
record carries a `team` object, but workflows don't declare what roles
they need, how agents should be spawned (individual Agent tool vs.
TeamCreate), or concurrency expectations. When Impetus has to infer
these from context, it gets it wrong 60% of the time.

This story adds explicit team composition sections to each workflow that
spawns agents, codifying required roles, spawning mode, and concurrency
constraints so there is zero ambiguity.

## Acceptance Criteria (Plain English)

1. The sprint-dev workflow (`skills/momentum/skills/sprint-dev/workflow.md`)
   contains a `<team-composition>` section (or equivalent structural
   element) at the top of the workflow that declares:
   - Required roles for each phase that spawns agents (Phase 2 dev wave,
     Phase 4 AVFL fix agents, Phase 5 team review)
   - Spawning mode per role: `individual` (Agent tool, one agent per
     spawn) or `team` (TeamCreate, grouped spawn) — with the default
     being `individual` unless explicitly overridden
   - Concurrency expectation: `parallel` (all agents in one turn) or
     `sequential` (one at a time, dependency-ordered)

2. The AVFL skill (`skills/momentum/skills/avfl/SKILL.md`) contains a
   similar composition declaration that codifies:
   - Validator agents are always spawned as individual agents (never as
     a team)
   - Consolidator runs sequentially after validators
   - Fixer runs sequentially after consolidator
   - Model and effort per role (already present in the Role Configuration
     table — this declaration references it, not duplicates it)

3. Sprint-dev Phase 2 (dev wave) explicitly states that each dev agent
   is spawned as an individual Agent tool call, never via TeamCreate.
   The spawning mode is declared alongside the existing agent resolution
   logic (steps 2.1–2.5).

4. Sprint-dev Phase 5 (team review) explicitly states that QA, E2E
   Validator, and Architect Guard are spawned as three individual Agent
   tool calls in parallel in a single message — not as a TeamCreate
   group.

5. Sprint-dev Phase 4 (AVFL fix agents) explicitly states that fix
   agents are spawned as individual Agent tool calls on the sprint
   branch.

6. Sprint planning workflow includes a team composition planning step
   that validates the planned `team` object against the workflow's
   declared required roles before activating the sprint. If a required
   role is missing from the plan, sprint planning must surface the gap
   before activation.

7. Every team composition declaration includes a "spawning mode" field
   that is one of: `individual-agent` (default), `team-create`. The
   field is mandatory — no spawning without an explicit mode declaration.

8. No existing behavior changes — this story adds declarations that
   codify what the workflows already intend. If a workflow currently
   spawns agents individually, the declaration says `individual-agent`.
   This is documentation-as-code, not a behavior change.

## Dev Notes

### Where to add declarations

The primary change is adding structured metadata to existing workflow
files. Two approaches, in order of preference:

**Option A — XML elements in workflow.md** (preferred for sprint-dev):
```xml
<team-composition phase="dev-wave">
  <role name="dev" specialist="true" spawning="individual-agent" concurrency="parallel">
    Agent definition: skills/momentum/agents/{specialist}.md
    Fallback: skills/momentum/agents/dev.md
    One agent per unblocked story.
  </role>
</team-composition>
```

**Option B — Structured section in SKILL.md** (preferred for AVFL):
Add a "## Team Composition" section after the existing "## Pipeline
Execution" section, using the same table format AVFL already uses for
Role Configuration.

### Sprint-dev workflow changes

Phase 2 (step n="2") already contains the agent resolution logic at
lines 113–149. The team composition declaration should be placed just
before this step or as a `<critical>` rule at the top of the workflow.
Key points to codify:

- Dev agents: `individual-agent`, parallel within a wave, one per story
- Never use TeamCreate for dev agents — each story gets its own
  isolated agent with its own worktree
- The specialist resolution logic (steps 2.3a–2.3d) remains unchanged

Phase 5 (step n="5") at lines 271–332 spawns three agents. Codify:
- QA Agent: `individual-agent`, parallel with peers
- E2E Validator: `individual-agent`, parallel with peers
- Architect Guard: `individual-agent`, parallel with peers
- All three in a single message (three Agent tool calls), never TeamCreate

Phase 4 (step n="4") at lines 225–265 may spawn fix agents. Codify:
- Fix agents: `individual-agent`, sequential (one per critical finding)
- No worktrees — direct on sprint branch

### AVFL SKILL.md changes

The Role Configuration table (lines 166–176) already declares
model/effort per role. Add a "Spawning Mode" column or a dedicated
subsection that states:
- All validators: `individual-agent`, parallel (all in one turn)
- Consolidator: `individual-agent`, sequential (after all validators)
- Fixer: `individual-agent`, sequential (after consolidator)
- Never use TeamCreate in AVFL — each subagent is an individual spawn

### Sprint planning validation

The sprint-planning workflow builds the `team` object. Add a validation
step that checks:
- Every phase that declares required roles has at least one agent
  assigned to fill each required role
- Story assignments reference valid specialist agent definitions
  (file exists at `skills/momentum/agents/{specialist}.md`)
- No story is left unassigned

### What NOT to change

- Do not modify the agent definition files themselves (dev.md, etc.)
- Do not change the sprint record schema — the `team` object format
  is fine, the problem is that workflows don't declare what they need
- Do not add runtime validation — this is compile-time (workflow parse
  time) documentation that Impetus reads before spawning

### Files

- `skills/momentum/skills/sprint-dev/workflow.md` — add team composition
  declarations to phases 2, 4, and 5
- `skills/momentum/skills/avfl/SKILL.md` — add spawning mode to Role
  Configuration section
- `skills/momentum/skills/sprint-planning/workflow.md` — add team
  validation step
