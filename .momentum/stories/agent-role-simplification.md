# Agent Role Simplification — Dev + Prompt Engineer with Directory-Scoped Guidelines

Status: backlog
Epic: agent-team-model

## What This Is

Consolidate the four specialist dev agent files (dev.md, dev-skills.md, dev-build.md, dev-frontend.md) into two methodology-based agents: **dev** (TDD) and **prompt-engineer** (EDD). Domain specialization moves from Momentum's agent files to the project's directory-scoped CLAUDE.md files.

## Why It Matters

The current model bakes domain knowledge (Kotlin, Gradle, Python) into Momentum's agent definitions. This breaks in multi-stack projects — a "build specialist" needs Gradle knowledge for the frontend repo and Poetry knowledge for the backend repo, but they're the same agent file. The real distinction isn't domain — it's methodology: code developers follow TDD, skill authors follow EDD. Everything else is project context.

## Design Decisions (Decision 37)

**Two methodology agents:**
- **dev** — writes code, TDD, picks up project conventions from directory CLAUDE.md
- **prompt-engineer** (replaces dev-skills) — writes skill instructions, EDD, knows frontmatter schema and 500-line limit

**Project defines its own roles:** A "Frontend Developer" is a project concept, not a Momentum concept. It's a dev agent + frontend/CLAUDE.md guidelines. Momentum never needs to know what Kotlin or Compose is.

**Directory-scoped CLAUDE.md is the mechanism:** Claude Code already supports this natively. Put conventions where the code lives:
- `frontend/CLAUDE.md` → Kotlin, Compose, Gradle conventions
- `backend/CLAUDE.md` → Python, FastAPI, Poetry conventions

**agent-guidelines skill is the bridge:** Enhanced to define project roles (role name + methodology agent + directory scopes) and create directory-scoped CLAUDE.md files with stack-specific conventions.

**Sprint planning classifies by change_type, not touches:** `code`/`script-code` → dev, `skill-instruction` → prompt-engineer. Touches paths match against project role scopes for guideline attachment.

## Rough Scope

- Delete `dev-build.md`, `dev-frontend.md`
- Rename `dev-skills.md` → `prompt-engineer.md` with updated framing
- Update `dev.md` to emphasize methodology over domain
- Add role-definition phase to `momentum:agent-guidelines` workflow
- Update sprint-planning Step 5 (methodology selection + guideline scoping)
- Update sprint-dev Phase 2 (spawn dev or prompt-engineer with injected guidelines)
- QA, E2E, architecture-guard agents unchanged

## Context References

- [Decision 37]: `docs/planning-artifacts/momentum-master-plan.md` — full rationale
- [specialist-dev-agents story]: superseded by this change
- [agent-guidelines skill]: `skills/momentum/skills/agent-guidelines/` — enhanced, not replaced
