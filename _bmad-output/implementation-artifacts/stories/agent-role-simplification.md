---
title: Agent Role Simplification — Dev + Prompt Engineer with Directory-Scoped Guidelines
story_key: agent-role-simplification
status: ready-for-dev
epic_slug: agent-team-model
depends_on: []
touches:
  - skills/momentum/agents/dev.md
  - skills/momentum/agents/dev-skills.md
  - skills/momentum/agents/dev-build.md
  - skills/momentum/agents/dev-frontend.md
  - skills/momentum/skills/agent-guidelines/SKILL.md
  - skills/momentum/skills/agent-guidelines/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
change_type: skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Part 4 Architecture Decisions — Decision 37 (Agent role simplification)"
---

# Agent Role Simplification

## Story

The current agent model has four dev-role agent files: `dev.md` (base),
`dev-skills.md`, `dev-build.md`, and `dev-frontend.md`. This was designed under
the assumption that domain specialization belongs in Momentum's agent definition
files. Decision 37 reverses that assumption: domain specialization (Kotlin,
Gradle, Python, frontend frameworks) belongs to the **project** via
directory-scoped `CLAUDE.md` files, not to Momentum.

Momentum should distinguish agents only by **methodology**:

- **dev** -- writes code, follows TDD (red-green-refactor), picks up project
  conventions from directory-scoped CLAUDE.md files at the paths it touches
- **prompt-engineer** (replaces `dev-skills.md`) -- writes skill instructions
  (SKILL.md, workflow.md, agent definitions), follows EDD (eval-driven
  development), knows frontmatter schema and 500-line skill limit

The bridge between Momentum's methodology agents and the project's domain
knowledge is the `momentum:agent-guidelines` skill. It already generates
technology guidelines; this story expands it to also define developer roles
(e.g., "Frontend Developer = dev agent + frontend/CLAUDE.md") and create
directory-scoped CLAUDE.md files with stack-specific conventions.

Sprint planning and sprint-dev workflows are updated to classify stories by
`change_type` (methodology selection) and `touches` (guideline scoping) instead
of by specialist agent file lookup.

## Acceptance Criteria

### AC1: Specialist agent files removed

`dev-build.md` and `dev-frontend.md` are deleted from `skills/momentum/agents/`.
No workflow, skill, or configuration file references them. The only dev-role
agent files remaining are `dev.md` and `prompt-engineer.md`.

### AC2: dev-skills.md renamed to prompt-engineer.md

`dev-skills.md` is renamed to `prompt-engineer.md` with updated identity framing:
the agent is a prompt engineer who writes skill instructions using EDD
methodology. The file retains knowledge of SKILL.md frontmatter schema, workflow
XML structure, 500-line limit, and agent definition conventions. The name, description,
and system prompt reflect "prompt-engineer" identity -- not "dev-skills".

### AC3: dev.md updated with methodology focus

`dev.md` system prompt is updated to emphasize methodology over domain:
- TDD (red-green-refactor) is the primary implementation approach
- The agent reads and follows any directory-scoped CLAUDE.md or `.claude/rules/`
  files it encounters at the paths it touches
- No domain-specific knowledge is baked in -- all domain conventions come from
  the project's guidelines
- Guidelines may be injected via the spawn prompt; the agent applies them as
  project-local overrides

### AC4: agent-guidelines skill enhanced with role definition

The `momentum:agent-guidelines` skill gains a role-definition phase (in addition
to its existing discovery, research, consultation, and generation phases):
- During consultation, the skill asks the developer to define project developer
  roles (e.g., "Frontend Developer", "Backend Developer", "Infra Engineer")
- Each role is a mapping: role name, methodology agent (`dev` or
  `prompt-engineer`), and one or more directory scopes whose CLAUDE.md files
  provide domain context
- The skill writes a role configuration file (e.g.,
  `.claude/momentum/developer-roles.json`) that sprint-planning can consume
- Directory-scoped CLAUDE.md files are created or updated with stack-specific
  conventions for each role's scoped paths

### AC5: Sprint planning classifies by methodology and scoped guidelines

Sprint-planning workflow Step 5 is updated:
- **Methodology selection**: Stories are classified by `change_type` --
  `code` or `script-code` maps to `dev`, `skill-instruction` maps to
  `prompt-engineer`. This replaces the old `touches`-based specialist agent
  selection.
- **Guideline scoping**: `touches` paths are matched against the project's
  role configuration to determine which directory-scoped guidelines to attach.
  When no role configuration exists, no guidelines are attached (base agent
  only).
- The sprint plan output still shows project role names (e.g., "Frontend
  Developer") for readability, but the underlying assignment is methodology
  agent + guidelines path.

### AC6: Sprint-dev spawns methodology agents with injected guidelines

Sprint-dev workflow Phase 2 is updated:
- Stories spawn either `dev` or `prompt-engineer` based on `change_type`
  (replacing the old `subagent_type`/`specialist` field lookup)
- Scoped guidelines are injected into the spawn prompt as context, not as agent
  file selection
- The spawn mechanism is simpler: two agent files instead of N specialist files
- When guidelines are attached, the spawn prompt includes them; when not, the
  base agent runs unaugmented

### AC7: No regressions in non-dev agent roles

QA reviewer (`qa-reviewer.md`), E2E validator (`e2e-validator.md`), architecture
guard, and code reviewer agents are completely unchanged. This story only affects
dev-role agent files and the workflows that spawn them.

### AC8: Supersedes specialist-dev-agents story

The `specialist-dev-agents` story (which introduced `dev-build.md`,
`dev-frontend.md`, and the `specialist` field in sprint records) is superseded
by this story. Any sprint record fields or workflow logic from that story that
conflict with this story's approach are replaced. The `specialist` field in
sprint records is removed or replaced with `methodology` and `guidelines_path`.

## Tasks / Subtasks

- [ ] Task 1 -- Agent file changes (AC1, AC2, AC3)
  - [ ] Delete `skills/momentum/agents/dev-build.md`
  - [ ] Delete `skills/momentum/agents/dev-frontend.md`
  - [ ] Rename `skills/momentum/agents/dev-skills.md` to `prompt-engineer.md`
  - [ ] Rewrite `prompt-engineer.md` identity: prompt engineer, EDD methodology,
        SKILL.md frontmatter schema, workflow XML structure, 500-line limit
  - [ ] Update `dev.md` system prompt: TDD methodology, no baked-in domain
        knowledge, reads directory-scoped CLAUDE.md, accepts injected guidelines
  - [ ] Verify no other files reference `dev-build.md`, `dev-frontend.md`, or
        `dev-skills.md` by name

- [ ] Task 2 -- Enhance agent-guidelines skill (AC4)
  - [ ] Add role-definition consultation phase to `workflow.md`
  - [ ] Define role configuration output schema (role name, methodology agent,
        directory scopes)
  - [ ] Update `SKILL.md` to document the new phase and output
  - [ ] Implement directory-scoped CLAUDE.md creation for each role's scoped
        paths during the generation phase

- [ ] Task 3 -- Update sprint-planning Step 5 (AC5)
  - [ ] Replace specialist agent classification with `change_type`-based
        methodology selection
  - [ ] Add guideline scoping: match `touches` against role configuration
  - [ ] Update team composition output format to show methodology + guidelines
  - [ ] Remove any `specialist` field references from sprint plan output

- [ ] Task 4 -- Update sprint-dev Phase 2 (AC6, AC8)
  - [ ] Replace specialist agent spawning with methodology agent spawning
        (`dev` or `prompt-engineer`)
  - [ ] Inject scoped guidelines via spawn prompt instead of agent file selection
  - [ ] Remove `specialist` field handling from sprint record reads
  - [ ] Add `methodology` and `guidelines_path` to story assignment schema if
        needed

- [ ] Task 5 -- Validate end-to-end and non-regression (AC7)
  - [ ] Verify a `change_type: code` story spawns `dev` agent
  - [ ] Verify a `change_type: skill-instruction` story spawns `prompt-engineer`
  - [ ] Verify directory-scoped guidelines are injected when role config exists
  - [ ] Verify base agent works unaugmented when no role config exists
  - [ ] Verify QA reviewer, E2E validator, architecture guard agents are
        untouched
  - [ ] Verify no dangling references to deleted agent files

## Dev Notes

### What this replaces

The `specialist-dev-agents` story introduced domain-specific agent files and a
`specialist` field in sprint records. That approach baked domain knowledge into
Momentum's agent files. Decision 37 reverses this: Momentum owns methodology,
the project owns domain knowledge. This story supersedes `specialist-dev-agents`.

### The two methodology agents

| Agent | File | Methodology | What it writes |
|-------|------|------------|----------------|
| Dev | `agents/dev.md` | TDD (red-green-refactor) | Code, scripts, tests, config |
| Prompt Engineer | `agents/prompt-engineer.md` | EDD (eval-driven development) | SKILL.md, workflow.md, agent defs |

### How directory-scoped guidelines work

Claude Code already supports directory-scoped `CLAUDE.md` files. When an agent
touches files under `frontend/`, it automatically picks up `frontend/CLAUDE.md`.
No special Momentum machinery is needed -- the guidelines just need to exist.

The `momentum:agent-guidelines` skill is the authoring tool: it discovers the
project's stack, consults with the developer, and creates these `CLAUDE.md`
files. It also writes a role configuration so sprint-planning can display
human-readable role names.

### Sprint record schema change

Before (specialist-dev-agents approach):
```json
{
  "role": "dev",
  "specialist": "dev-skills",
  "guidelines": "path/to/guidelines.md"
}
```

After (this story):
```json
{
  "role": "dev",
  "methodology": "dev",
  "guidelines_path": "frontend/CLAUDE.md"
}
```

Or for skill-instruction stories:
```json
{
  "role": "dev",
  "methodology": "prompt-engineer",
  "guidelines_path": null
}
```

### What NOT to change

- **Non-dev agent roles** (qa-reviewer, e2e-validator, architecture-guard,
  code-reviewer) -- these are review/validation agents, not dev agents
- **The `momentum:dev` skill workflow** -- the skill that orchestrates story
  implementation is unchanged; only the agent it spawns changes
- **bmad-dev-story** -- the BMad story execution skill is unmodified
- **The agent-guidelines skill's existing phases** (discovery, research,
  consultation, generation, validation) -- only a role-definition sub-phase
  is added to the consultation phase

### Key design principle

A "Frontend Developer" in project X is not a Momentum concept. It is a
project-defined role: the `dev` methodology agent + `frontend/CLAUDE.md`
guidelines. Momentum never needs to know what Kotlin or Compose is. The
project's `CLAUDE.md` files carry that knowledge.

## Momentum Implementation Guide

### Change type: skill-instruction -- EDD Approach

All changes in this story are to agent definitions and workflow files (markdown
that instructs agents). Use eval-driven development:

**Behavioral evals should verify:**
- `dev.md` system prompt contains TDD methodology, no domain-specific knowledge,
  and instructions to read directory-scoped guidelines
- `prompt-engineer.md` system prompt contains EDD methodology, SKILL.md schema
  knowledge, and 500-line limit awareness
- `dev-build.md` and `dev-frontend.md` do not exist after implementation
- Sprint-planning Step 5 selects methodology by `change_type`, not by `touches`
  path patterns to specialist agents
- Sprint-dev Phase 2 spawns `dev` or `prompt-engineer`, not specialist agents
- Guidelines injection via spawn prompt works correctly
- No references to deleted agent files remain in any workflow or skill

**DoD items:**
- [ ] All workflow modifications follow existing XML structure and conventions
- [ ] Agent definitions are under 80 lines each
- [ ] No dangling references to removed files
- [ ] AVFL checkpoint on all modified artifacts
- [ ] Changes documented in Dev Agent Record

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
