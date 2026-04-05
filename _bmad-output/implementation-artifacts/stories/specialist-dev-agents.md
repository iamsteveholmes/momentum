---
title: Specialist Dev Agents — Domain-Specific Agent Definitions
story_key: specialist-dev-agents
status: ready-for-dev
epic_slug: agent-team-model
depends_on:
  - dev-agent-definition-files
touches:
  - skills/momentum/agents/
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
change_type: config-structure + skill-instruction
---

# Specialist Dev Agents — Domain-Specific Agent Definitions

## Goal

Replace the one-size-fits-all "Dev" role with domain-specialist dev agents. The
current team model assigns every story the same generic dev agent, regardless of
whether the story touches Gradle build files, Kotlin Compose frontend, Python
backend, SKILL.md workflows, or shell scripts. Each domain benefits from an
agent preamble that brings domain-specific expertise: dependency management
conventions for build agents, SKILL.md structure and EDD patterns for skills
agents, idiomatic Compose patterns for frontend agents, etc.

This story adds: (1) domain classification rules in sprint-planning Step 5 that
map `touches` path patterns to specialist types, (2) at least three specialist
agent definition files that extend the base `dev.md` pattern, (3) sprint-dev
Phase 2 modifications to spawn the correct specialist, and (4) sprint record
storage of the specialist assignment per story.

Depends on `dev-agent-definition-files` which establishes the base `agents/dev.md`
and the agent-spawning pattern in sprint-dev.

## Acceptance Criteria (Plain English)

1. Domain classification rules exist in sprint-planning workflow Step 5: `touches`
   path patterns map to specialist types using the mapping table defined in Dev
   Notes below. Multiple pattern matches resolve to the most specific specialist
   (e.g., `*.gradle*` beats the catch-all).
2. At least three specialist agent definition files exist in `skills/momentum/agents/`:
   `dev-skills.md`, `dev-build.md`, and `dev-frontend.md`. Additional specialists
   (e.g., `dev-python.md`, `dev-scripts.md`) may be added if the mapping table
   warrants them.
3. Each specialist agent definition follows the same frontmatter schema as
   `agents/dev.md` (name, description, model, effort, tools) and extends the
   base dev agent pattern with a focused domain-specific system prompt — not a
   full workflow, just a preamble of domain expertise and conventions.
4. Sprint planning Step 5 assigns a specialist type per story based on domain
   classification after role determination. The specialist type is stored in the
   team composition output alongside the role.
5. Sprint-dev Phase 2 reads the specialist type from the sprint record and spawns
   the assigned specialist agent file (e.g., `agents/dev-skills.md`). When no
   specialist matches or the specialist file does not exist, it falls back to
   the base `agents/dev.md`.
6. Each specialist agent accepts optional project guidelines that override or
   extend its built-in domain instructions — the same guidelines mechanism from
   Decision 26 (Two-Layer Agent Model) that the base dev agent uses.
7. The sprint record (`sprints/{slug}.json`) stores the specialist assignment per
   story in `team.story_assignments[slug].specialist` (e.g., `"dev-skills"`,
   `"dev-build"`) rather than the generic `"dev"`.

## Dev Notes

### Path pattern to specialist mapping table

This table lives in sprint-planning Step 5 as inline classification rules.
Order matters — first match wins, so more specific patterns come first.

| Pattern | Specialist | Rationale |
|---------|-----------|-----------|
| `skills/*/SKILL.md`, `skills/*/workflow.md`, `skills/**/sub-skills/` | `dev-skills` | SKILL.md authoring, EDD patterns, workflow XML structure |
| `*.gradle*`, `*.kts`, `buildSrc/`, `gradle/` | `dev-build` | Gradle conventions, dependency catalogs, build configuration |
| `*.kt`, `**/compose/**`, `**/ui/**` | `dev-frontend` | Kotlin Compose/KMP patterns, state management, UI conventions |
| `*.py`, `**/python/**` | `dev-python` | Python conventions, packaging, test patterns |
| `scripts/`, `*.sh`, `hooks/` | `dev-scripts` | Shell scripting, hook conventions, CLI patterns |
| `agents/*.md` | `dev-skills` | Agent definitions follow similar authoring patterns to skills |
| (no match) | `dev` | Base dev agent — generic implementation |

When a story's `touches` array contains paths matching multiple specialist types,
use the majority rule: the specialist with the most matching paths wins. Ties
break to the first specialist in table order (most specific).

### Sprint planning Step 5 modifications

After the existing role determination logic (Dev, QA, E2E Validator, Architect
Guard), add a domain classification pass:

1. For each story, iterate its `touches` paths
2. Match each path against the pattern table above
3. Tally matches per specialist type
4. Assign the majority specialist (or `dev` if no patterns match)
5. Store the specialist assignment in the team composition output

The team composition output changes from:
```
Role: Dev — N stories, guidelines: [project-specific | generic]
```
to:
```
Role: Dev — N stories
  · dev-skills: story-a, story-b (guidelines: project-specific)
  · dev-build: story-c (guidelines: generic)
  · dev: story-d (guidelines: generic)
```

### Sprint-dev Phase 2 modifications

Phase 2 currently spawns `momentum:dev` for every story with a role and
guidelines. After this story:

1. Read `team.story_assignments[slug].specialist` from the sprint record
2. Resolve the agent definition file: `skills/momentum/agents/{specialist}.md`
3. If the file exists, pass it as the agent definition to the spawn
4. If the file does not exist, log a warning and fall back to `agents/dev.md`
5. Pass the same guidelines (from the team composition) regardless of specialist

### Specialist agent definition format

Each specialist is a SHORT agent definition file — a focused system prompt, not
a workflow. The pattern matches `qa-reviewer.md` and `e2e-validator.md`:

```yaml
---
name: dev-skills
description: Specialist dev agent for SKILL.md, workflow, and agent definition authoring.
model: sonnet
effort: high
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

You are a specialist dev agent for Momentum skill and workflow files. You implement
stories that create or modify SKILL.md files, workflow.md files, agent definitions,
and sub-skills.

## Domain Expertise

[15-30 lines of domain-specific knowledge: SKILL.md frontmatter conventions,
workflow XML structure, EDD eval patterns, agent definition schema, etc.]

## Implementation Approach

Implement the story per its spec. Apply your domain expertise to the implementation
decisions. When project guidelines are provided, they override your built-in defaults.
```

Target length: 40-80 lines per specialist. Enough to carry domain knowledge into
the agent's context without bloating the system prompt.

### Specialist agent domain knowledge (brief)

**dev-skills**: SKILL.md frontmatter schema (name, description, model, effort,
tools), workflow.md XML structure (`<workflow>`, `<step>`, `<action>`, `<check>`,
`<ask>`, `<output>`, `<critical>`, `<note>`), EDD patterns for eval files,
agent definition schema, sub-skill organization. Knows that skill markdown IS
code (conventional commits: `feat(skills)` not `docs`).

**dev-build**: Gradle Kotlin DSL conventions, version catalog
(`libs.versions.toml`), dependency management, `buildSrc/` conventions,
composite builds, task configuration avoidance. Knows build files tend to have
cascading effects and require careful dependency ordering.

**dev-frontend**: Kotlin Compose/Compose Multiplatform patterns, MVI state
management, `remember`/`derivedStateOf` patterns, recomposition rules, Navigation
component patterns, Material3 theming. Knows UI code needs preview annotations
and composable test patterns.

### Extensibility

Projects can add their own specialist agents later by:
1. Dropping an agent definition file in `agents/` (e.g., `dev-rust.md`)
2. Adding a row to the pattern mapping table in sprint-planning Step 5

The mapping table is in the workflow file, not hard-coded in a script — human
and agent editable.

### What NOT to change

- **`momentum:dev` skill** (`skills/momentum-dev/` or `skills/momentum/skills/dev/`) —
  the skill workflow is unchanged. Specialist agents are passed TO the dev skill
  as context, not wired into its workflow logic.
- **`bmad-dev-story`** — the BMad story execution skill is unmodified.
- **Agent definitions for non-dev roles** (qa-reviewer, e2e-validator) — these are
  team review agents, not dev agents. Untouched.
- **`momentum:agent-guidelines` skill** — generates project-level guidelines, which
  are orthogonal to agent definitions. Untouched.

### Sprint record schema change

The `team.story_assignments` object in `sprints/{slug}.json` gains a `specialist`
field:

```json
{
  "team": {
    "story_assignments": {
      "plugin-skeleton": {
        "role": "dev",
        "specialist": "dev-skills",
        "guidelines": "path/to/guidelines.md"
      },
      "some-build-story": {
        "role": "dev",
        "specialist": "dev-build",
        "guidelines": null
      }
    }
  }
}
```

### Requirements coverage

- Architecture: Decision 26 (Two-Layer Agent Model) — specialist agents are the
  Momentum layer; project guidelines remain the project layer
- PRD FR62-FR70 (sprint execution): specialist spawning improves implementation
  quality by providing domain-appropriate agent expertise
- Epic: agent-team-model — this is the core story that introduces domain specialization

## Tasks / Subtasks

- [ ] Task 1 — Create specialist agent definition files (AC: 2, 3, 6)
  - [ ] Create `skills/momentum/agents/dev-skills.md` with SKILL.md/workflow domain expertise
  - [ ] Create `skills/momentum/agents/dev-build.md` with Gradle/dependency domain expertise
  - [ ] Create `skills/momentum/agents/dev-frontend.md` with Kotlin Compose/KMP domain expertise
  - [ ] Optionally create `dev-python.md` and `dev-scripts.md` if the mapping table includes them
  - [ ] Verify each agent definition follows frontmatter schema from base `dev.md`
  - [ ] Verify each agent definition is 40-80 lines (focused, not bloated)

- [ ] Task 2 — Add domain classification to sprint-planning Step 5 (AC: 1, 4)
  - [ ] Add the path pattern to specialist mapping table as classification rules
  - [ ] Add classification pass after role determination: iterate `touches`, tally matches, assign majority specialist
  - [ ] Update team composition output format to show specialist breakdown per story
  - [ ] Store specialist assignment in team composition data

- [ ] Task 3 — Modify sprint-dev Phase 2 to spawn specialist agents (AC: 5)
  - [ ] Read `specialist` field from `team.story_assignments[slug]` in sprint record
  - [ ] Resolve agent definition file path: `skills/momentum/agents/{specialist}.md`
  - [ ] Add fallback: if specialist file does not exist, log warning and use `agents/dev.md`
  - [ ] Pass guidelines to specialist agent same as base dev agent

- [ ] Task 4 — Update sprint record schema (AC: 7)
  - [ ] Add `specialist` field to `team.story_assignments` entries in sprint planning Step 8
  - [ ] Verify sprint-dev Phase 2 reads the new field correctly
  - [ ] Verify the sprint review output includes specialist assignment per story

- [ ] Task 5 — Validate end-to-end flow
  - [ ] Verify a story touching `skills/*/SKILL.md` gets classified as `dev-skills`
  - [ ] Verify a story touching `*.gradle*` gets classified as `dev-build`
  - [ ] Verify a story with no pattern matches falls back to base `dev`
  - [ ] Verify sprint record contains specialist assignments
  - [ ] Verify sprint-dev spawns the correct specialist agent file

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → config-structure (agent definition files — markdown with frontmatter)
- Tasks 2, 3, 4 → skill-instruction (workflow modifications in sprint-planning and sprint-dev)
- Task 5 → validation (no implementation, just verification)

---

### config-structure Tasks: Direct Implementation

Agent definition files are markdown with YAML frontmatter. Implement directly:

1. **Write each agent definition file** following the schema from existing agents
   (qa-reviewer.md, e2e-validator.md)
2. **Verify by inspection:**
   - YAML frontmatter parses correctly (name, description, model, effort, tools)
   - System prompt is focused and domain-specific (40-80 lines)
   - No workflow logic — just expertise preamble and implementation instructions
3. **Document** created files in the Dev Agent Record

### skill-instruction Tasks: EDD Approach

Workflow modifications should be verified with behavioral evals:
- Sprint-planning Step 5 correctly classifies stories by domain from `touches` paths
- Sprint-dev Phase 2 resolves and spawns the correct specialist agent
- Fallback to base dev agent works when specialist file is missing
- Sprint record contains specialist assignments in the expected schema location

**DoD items for skill-instruction tasks:**
- [ ] Workflow modifications follow existing XML structure and conventions
- [ ] Classification logic handles edge cases (empty touches, mixed domains, no matches)
- [ ] Fallback behavior is explicit and logged
- [ ] Changes documented in Dev Agent Record

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
