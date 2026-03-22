# Story 1.5: Enforcement Degrades Gracefully Across Tool Tiers

Status: ready-for-dev

## Story

As a developer,
I want Momentum's enforcement tiers to be explicitly defined and behave as documented at each tier,
so that teams using any tool can adopt Momentum at the level their environment supports.

## Acceptance Criteria

**AC1 — Tier 2 (Cursor/other tools):**
Given Momentum skills installed in Cursor via `npx skills add`,
When a developer invokes a Momentum skill,
Then skill instructions execute at advisory level — guidance is provided but not enforced
And `context: fork` frontmatter is silently ignored (Claude Code-exclusive per skills compatibility table)
And the developer is not required to take any additional action for skills to function

**AC2 — Tier 1 (Claude Code):**
Given Momentum installed in Claude Code (Tier 1),
When a developer uses any Momentum workflow,
Then Tier 1 full deterministic enforcement is active: hooks fire automatically, rules auto-load, subagents enforce quality
And this is explicitly documented in the README as Tier 1

**AC3 — Tier 3 (no tooling):**
Given no tooling at all (Tier 3),
When a developer reads the Momentum README,
Then all three enforcement tiers are defined: Tier 1 (Claude Code — full deterministic), Tier 2 (Cursor/other tools with skills — advisory), Tier 3 (no tooling — philosophy/documentation only)
And each tier lists what works and what does not
And instructions for adopting at each tier are present

## Tasks / Subtasks

- [ ] Task 1: Write the Momentum README with enforcement tier documentation (AC: 2, 3)
  - [ ] 1.1: Write the Tier 1 section: what Claude Code provides (hooks, rules, subagents, model routing); how to install; what "full deterministic enforcement" means
  - [ ] 1.2: Write the Tier 2 section: what other tools provide (skill instructions only, advisory); what is NOT available (hooks, rules, context:fork isolation); how `context: fork` and `model:` frontmatter are silently ignored
  - [ ] 1.3: Write the Tier 3 section: philosophy/documentation only; how to adopt Momentum principles without any tooling; point to practice-overview.md and the eight principles
  - [ ] 1.4: Write install instructions for each tier: Tier 1 (`npx skills add momentum/momentum -a claude-code` + `/momentum`), Tier 2 (`npx skills add momentum/momentum -a cursor`), Tier 3 (read the docs)

- [ ] Task 2: Verify Tier 2 behavior — Agent Skills standard compliance (AC: 1)
  - [ ] 2.1: Confirm all SKILL.md files have only standard-required frontmatter fields (`name`, `description`) plus additive Claude Code fields — no required non-standard fields that would break parsing
  - [ ] 2.2: Confirm `context: fork` is only in frontmatter (not in instructions body) so tools that ignore it don't get confused
  - [ ] 2.3: Document verification result in Dev Agent Record

- [ ] Task 3: Verify Tier 3 documentation is actionable without tooling (AC: 3)
  - [ ] 3.1: Confirm README Tier 3 section is self-contained: a developer can read it and understand the eight Momentum principles without installing anything
  - [ ] 3.2: Confirm `skills/momentum/references/practice-overview.md` (from Story 1.3) exists and is referenced from the README for detailed principle documentation

## Dev Notes

### This Story is Primarily Documentation

Unlike Stories 1.1–1.4 which create code/config, Story 1.5 is about **writing the README** and **verifying** that the existing packaging decisions (from Stories 1.1–1.2) deliver the correct tier behavior. The graceful degradation is architecturally guaranteed by the Agent Skills standard:

> "Extra YAML frontmatter fields are silently ignored by tools that don't understand them. A single SKILL.md can be both spec-compliant and tool-optimized." [Source: research/technical-agent-skills-deployment-research-2026-03-15.md#Layer 1]

No new enforcement code is needed — the tiers are a natural consequence of how the packaging works:
- **Tier 1 (Claude Code):** Impetus writes hooks + rules + MCP on first run (Story 1.3). Hooks fire deterministically. Rules auto-load from `~/.claude/rules/`. Context:fork skills spawn isolated subagents.
- **Tier 2 (Cursor/other):** Same SKILL.md files install via `npx skills add -a cursor`. Instructions execute as advisory. Extra frontmatter ignored. No hooks, no rules, no subagent isolation.
- **Tier 3 (none):** Read the README + practice-overview.md. Apply principles manually.

### README Structure

The README should cover (at minimum):

```markdown
# Momentum

[One-paragraph description]

## Quick Start

[Install command + first invocation]

## Enforcement Tiers

### Tier 1: Full Deterministic (Claude Code)
[What you get, how it works, how to install]

### Tier 2: Advisory (Cursor & Other Tools)
[What you get, what's NOT available, how to install]

### Tier 3: Philosophy Only (No Tooling)
[How to adopt principles without installing anything]

## The Eight Principles

[Brief list with pointers to practice-overview.md]
```

### NFR7 Compliance

NFR7 requires:
- Each tier explicitly tested
- Tier 3 validated by: (1) verifying the README documents all three tiers, (2) confirming practice principles are documented in a form actionable without tooling

**Tier 3 validation method (from NFR7):** "verifying the README documents all three enforcement tiers and their respective capabilities and limitations; confirming that the practice principles are documented in a form that is actionable without any tooling installation."

This means the README Tier 3 section must be standalone — a developer who reads only the README (no install, no tools) must be able to understand and apply Momentum's principles.

[Source: epics.md#NFR7]

### What Already Exists

- `README.md` at repo root exists — it's a basic project readme, not the product README this story creates
- `skills/momentum/references/practice-overview.md` — created in Story 1.3, contains the eight principles for orientation

### References

- [Source: epics.md#Story 1.5 — Acceptance Criteria]
- [Source: epics.md#NFR5-NFR8 — Portability & Graceful Degradation]
- [Source: epics.md#NFR7 — Tier 3 validation method]
- [Source: _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md#Layer 1 — Agent Skills standard portability]
- [Source: architecture.md#Deployment Structure — Skills Deployment Classification]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → unclassified (README documentation and verification — no Momentum-specific EDD/TDD guidance applies; standard bmad-dev-story DoD applies)

No skill-instruction, script-code, rule-hook, or config-structure tasks. Standard bmad-dev-story DoD is sufficient.

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
