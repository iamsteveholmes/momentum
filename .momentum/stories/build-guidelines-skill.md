---
title: Build-Guidelines Skill — Gen-2 Agent Guidelines: Constitution + Composed Specialist Agent Files
story_key: build-guidelines-skill
status: backlog
epic_slug: agent-team-model
depends_on:
  - kb-init
touches:
  - skills/momentum/skills/build-guidelines/SKILL.md
  - skills/momentum/skills/build-guidelines/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
---

# Build-Guidelines Skill — Gen-2 Agent Guidelines

## What This Is

A skill (`/momentum:build-guidelines`) that generates the Tier 1 and Tier 2 artifacts
of the three-tier agent guidelines architecture:

- **Tier 1 (Hot constitution):** `.claude/guidelines/constitution.md` — ~660 lines,
  always loaded. Trigger tables, critical rules, pointers to Tier 3.
- **Tier 2 (Composed specialist agent files):** `.claude/guidelines/agents/{role}-{domain}.md`
  — base agent body + project manifest merged. Guidelines are part of the system prompt,
  not the spawn prompt.

This is the gen-2 replacement for `momentum:agent-guidelines` (gen-1, which only
generates `.claude/rules/` + `docs/references/`).

## Why This Matters

**The fundamental problem:** CLAUDE.md inheritance for subagents is unreliable (GitHub
#29423). Path-scoped rules have a regression (GitHub #16299). The only guaranteed delivery
channel to a subagent is its system prompt body.

**The solution (April 9, 2026 session):** Don't inject guidelines at spawn time — bake
them into the agent file before the sprint starts. `build-guidelines` generates
`dev-kotlin-compose.md` = `dev.md` body + Kotlin Compose project manifest merged.
When `sprint-dev` spawns the agent, it spawns the composed file — the guidelines ARE
the agent.

Steve's exact words (April 9): *"Is there a way we could essentially create specialist
agent files for the TeamCreate? Right now our idea is to use guideline injection
essentially but couldn't we instead bake the manifest into the agent file and create
different specialized agents?"*

## Generated File Structure

```
{project}/
  .claude/
    guidelines/
      constitution.md              ← Tier 1: hot layer (always loaded)
      agents/
        dev-kotlin-compose.md      ← Tier 2: dev.md body + KMP guidelines
        dev-python-fastapi.md      ← Tier 2: dev.md body + Python guidelines
        qa-kotlin-compose.md       ← Tier 2: qa-reviewer.md body + QA guidelines
        e2e-kotlin-compose.md      ← Tier 2: e2e-validator.md body + E2E guidelines
        ...
      refs/
        compose-antipatterns.md    ← JIT reference (pointed to from constitution)
        compose-testing.md
        ...
```

## Composed Agent File Format

```markdown
---
name: dev-kotlin-compose
model: sonnet
effort: medium
tools: [Read, Glob, Grep, Bash, Edit, Write, Agent, Skill]
---

## Project Guidelines — {Stack} ({Date})

### Critical Rules (always active)
{version pins, hard prohibitions, never/always rules}

### Reference Docs (load on demand)
- Antipatterns → .claude/guidelines/refs/{domain}-antipatterns.md
- Testing → .claude/guidelines/refs/{domain}-testing.md
...

---
{full base agent body, unchanged from skills/momentum/agents/dev.md}
```

## Workflow Phases (high level)

1. **Discover** — detect roles needed for this project (from stories/sprint composition),
   detect technology domains (from build files, source patterns, vault index)
2. **Consult** — interactive: confirm role×domain matrix, review existing constitution,
   decide Layer 2 reference doc scope
3. **Distill** — for each role×domain: pull relevant pages from cold KB vault, synthesize
   into hot constitution entries and composed agent body additions
4. **Generate** — write `constitution.md` and all `agents/{role}-{domain}.md` files;
   write `refs/*.md` JIT reference docs
5. **Wire** — update sprint record to reference composed agent files; update sprint-dev
   spawn logic to use `.claude/guidelines/agents/` files when present
6. **Validate** — AVFL checkpoint: verify line counts, check no role bleed, confirm all
   vault citations resolve

## Sprint-Dev Integration

When composed agent files exist in `.claude/guidelines/agents/`, `sprint-dev` uses them
instead of the generic `skills/momentum/agents/*.md` files. Detection:
- Check `.claude/guidelines/agents/` for `{role}-{domain}.md` matching the story's
  specialist classification
- If found: spawn the composed file (guidelines already in system prompt)
- If not found: fall back to generic agent + `guidelines-verification-gate` warning

## Context References

- Decision document: `_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md`
- Assessment document: `_bmad-output/planning-artifacts/assessments/aes-001-agent-guidelines-current-state-2026-04-09.md`
- Gen-1 predecessor: `_bmad-output/implementation-artifacts/stories/agent-guidelines-skill.md` (done)
- Depends on: `kb-init` (vault needed for distill phase to have source material)
- Related: `kb-ingest` (keeps vault current so distill phase has fresh knowledge)
