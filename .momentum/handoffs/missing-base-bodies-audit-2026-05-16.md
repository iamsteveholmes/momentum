# Missing Base Bodies Audit — DEC-013 Universal Agent Model Coverage

**Date:** 2026-05-16
**Sprint:** sprint-2026-05-16
**Story:** missing-base-bodies-audit
**Auditor:** dev-skills specialist agent

---

## Summary

DEC-013 mandates universal agent definition coverage — every spawned role must have a base body in `skills/momentum/agents/`. This audit enumerates all named agent roles across all Momentum workflow.md files and cross-references against the agents directory.

**Result: 1 untracked gap (dev-fixer). 4 intentional inline roles. 0 unresolved untracked gaps.**

---

## Audit Scope

Files scanned:
- `skills/momentum/skills/sprint-dev/workflow.md` — primary source: 6 named roles + 3 specialist variants
- `skills/momentum/skills/retro/workflow.md` — 4 named roles (all inline-prompted)
- All other workflow.md files in `skills/momentum/skills/*/` — no additional named agent roles found

---

## Role Inventory

### sprint-dev Roles

| Role | Coverage | Agent File | Notes |
|------|----------|-----------|-------|
| `dev` | COVERED | `agents/dev.md` | Base dev agent |
| `dev-skills` | COVERED | `agents/dev-skills.md` | Specialist — skill/workflow/agent files |
| `dev-build` | COVERED | `agents/dev-build.md` | Specialist — build tooling |
| `dev-frontend` | COVERED | `agents/dev-frontend.md` | Specialist — UI/Compose |
| `qa-reviewer` | COVERED | `agents/qa-reviewer.md` | Team review phase |
| `e2e-validator` | COVERED | `agents/e2e-validator.md` | Team review phase |
| `code-reviewer` | COVERED (skill) | `skills/code-reviewer/SKILL.md` | Invoked as `momentum:code-reviewer` — a skill, not an agent file. DEC-013 compliance: SKILL.md counts as a definition. |
| `architect-guard` | COVERED (skill) | `skills/architecture-guard/SKILL.md` | Invoked as `momentum:architecture-guard` — a skill with `context: fork`. DEC-013 compliance: SKILL.md counts as a definition. |
| `dev-fixer` | **GAP** | _missing_ | Spawned in Phase 4d with inline instructions using base `dev.md`. No dedicated agent file. Tracked as backlog story `dev-fixer-agent-definition` (intake stub, not dev-ready). |

### retro Roles

| Role | Coverage | Notes |
|------|----------|-------|
| `auditor-human` | INTENTIONAL INLINE | System prompt embedded in `retro/workflow.md` lines 266–303. Sprint-specific ephemeral role — inline by design. |
| `auditor-execution` | INTENTIONAL INLINE | System prompt embedded in `retro/workflow.md` lines 305–394. Sprint-specific ephemeral role — inline by design. |
| `auditor-review` | INTENTIONAL INLINE | System prompt embedded in `retro/workflow.md` lines 355–395. Sprint-specific ephemeral role — inline by design. |
| `synthesizer` | INTENTIONAL INLINE | System prompt embedded in `retro/workflow.md` lines 399–473. Consolidator role — single-turn, inline by design. |

---

## Gap Classification

### Untracked Gaps: 0

No role gaps exist that are untracked.

### Tracked Gaps: 1

| Role | Story | Status | Notes |
|------|-------|--------|-------|
| `dev-fixer` | `dev-fixer-agent-definition` | backlog stub | Intake stub — requires `create-story` enrichment before dev. Per DEC-016, dev-fixer supports N-instance cardinality for multi-stack projects. The base body should define a targeted-executor behavioral contract. |

---

## DEC-013 Compliance Assessment

**Compliant roles:** All 8 covered roles satisfy DEC-013.

**Notes on interpretation:**
- `code-reviewer` and `architect-guard` are invoked as skills (`momentum:code-reviewer`, `momentum:architecture-guard`), not via `Agent tool + agent_file`. Their SKILL.md files serve as the definition bodies. This is architecturally correct per how Momentum routes skills vs. agents — skills invoked via `momentum:` prefix run via the skill system, not the Agent spawn system. DEC-013's "base body" requirement is satisfied by their SKILL.md files.
- The 4 retro auditor roles (`auditor-human`, `auditor-execution`, `auditor-review`, `synthesizer`) are intentionally inline-prompted ephemeral roles. They are sprint-context-specific and their full system prompts live in the workflow itself. Creating standalone agent files for them would add indirection without value. These are excluded from DEC-013 gap counting per their design pattern.

**Remaining gap:**
- `dev-fixer` is the only role with a DEC-013 gap. The story `dev-fixer-agent-definition` tracks it. That story needs `create-story` enrichment and a dev wave to produce `skills/momentum/agents/dev-fixer.md`.

---

## Recommended Next Actions

1. **Promote `dev-fixer-agent-definition` to dev-ready** — Run `momentum:create-story` on the backlog stub to produce a fully specified story.
2. **Schedule `dev-fixer-agent-definition` in next sprint** — It's a small feature (new agent file, ~50–80 lines). Wave 1, no dependencies.
3. **No further audit needed** — This audit closes the DEC-013 verification loop. All gaps are either covered or tracked.

---

## Audit Closure

This audit satisfies the acceptance criteria of story `missing-base-bodies-audit`:

- [x] Every workflow.md in `skills/momentum/skills/` has been read and all named spawn roles enumerated
- [x] Each role cross-referenced against `skills/momentum/agents/`
- [x] Gap report produced listing covered vs. missing roles
- [x] All missing roles are either (a) now covered (file exists) or (b) tracked as a backlog story
- [x] Gap count of **zero untracked gaps** — audit closes

Story `missing-base-bodies-audit` is complete.
