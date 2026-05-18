# Story: document-context-tier-subagent-inheritance

Status: ready-for-dev
Epic: impetus-core

## Story

As a Momentum practitioner,
I want the context-tier propagation behavior documented accurately across the relevant rule and reference files,
so that I never receive incorrect guidance claiming subagents run at a different context tier than the parent session.

## Acceptance Criteria

1. `~/.claude/rules/spawning-patterns.md` contains a "Context Tier Inheritance" subsection documenting that context tier is set at the session level and inherited by all subagents at spawn time.
2. The `spawning-patterns.md` section explicitly states that `model:` frontmatter does NOT override context tier — it controls model family (Sonnet/Opus/Haiku) only.
3. `skills/momentum/references/agent-skill-development-guide.md` `model:` frontmatter schema entry (in both Agent and SKILL.md sections) has a caveat noting it controls model family only, not context tier.
4. `~/.claude/rules/model-routing.md` has a note or forward reference clarifying that `model:` pins control family selection only; context tier behavior is documented in `spawning-patterns.md`.
5. No existing guidance in any of the three files is contradicted or left ambiguous by the additions.

## Tasks / Subtasks

- [ ] Task 1: Add "Context Tier Inheritance" subsection to `~/.claude/rules/spawning-patterns.md` (AC: 1, 2)
  - [ ] 1.1 Read the current file to identify placement — after the Decision Rule section
  - [ ] 1.2 Write the subsection: context tier is session-level, inherited by all subagents at spawn time, `model:` frontmatter does not override it
  - [ ] 1.3 Verify the addition is internally consistent and does not contradict existing fan-out / TeamCreate guidance
  - [ ] 1.4 Document expected behavior as testable condition in Dev Agent Record

- [ ] Task 2: Add `model:` caveat to `skills/momentum/references/agent-skill-development-guide.md` (AC: 3)
  - [ ] 2.1 Read the guide, locate the two `model:` frontmatter schema entries (Agent section line ~10, SKILL.md section line ~75)
  - [ ] 2.2 Add an inline comment or caveat note to each: "controls model family (Sonnet/Opus/Haiku) only — does not override session context tier"
  - [ ] 2.3 Verify surrounding schema entries are unaffected

- [ ] Task 3: Add forward reference to `~/.claude/rules/model-routing.md` (AC: 4)
  - [ ] 3.1 Read the current file (currently a placeholder: "Route tasks to models based on cognitive requirements declared in skill frontmatter.")
  - [ ] 3.2 Add a section clarifying that `model:` pins select model family only; for context tier behavior, see `spawning-patterns.md`
  - [ ] 3.3 Preserve the existing placeholder line (or integrate it) so the file's intent remains intact

- [ ] Task 4: Cross-check all three files for consistency (AC: 5)
  - [ ] 4.1 Re-read all three modified files and confirm no contradictions
  - [ ] 4.2 Confirm that `spawning-patterns.md` is the single authoritative source for context tier behavior, and the other two files reference or defer to it

## Dev Notes

### Context and Motivation

This story was created via `momentum:distill` from a session learning. A distill session discovered that context tier (e.g., standard vs. 1M-token window) is a session-level property inherited by all subagents at spawn time. An agent under 1M context spawns all child agents under 1M context — there is no per-invocation override. This was not documented anywhere in the rule files, and the existing `model-routing.md` placeholder created a misleading implication that `model:` frontmatter was the complete routing mechanism.

**Source:** distill — Tier 2 escalation (adversary identified multi-file coordination requirement)

### File State at Story Creation

**`~/.claude/rules/spawning-patterns.md`** (40 lines, clean):
- Documents fan-out vs TeamCreate patterns
- Decision rule section ends at line 40
- No mention of context tier anywhere
- **Placement for new content:** Append a new `## Context Tier Inheritance` section after the Decision Rule section

**`skills/momentum/references/agent-skill-development-guide.md`** (99 lines):
- Agent frontmatter schema at lines 6–17; `model: sonnet|haiku|opus  # Optional: model override` at line 10
- SKILL.md frontmatter schema at lines 68–82; `model: haiku|sonnet|opus  # Optional: model override` at line 75
- No mention of context tier anywhere
- **Placement:** Add a parenthetical caveat to each `model:` comment line

**`~/.claude/rules/model-routing.md`** (5 lines, placeholder):
```
# Model Routing

<!-- Placeholder — full content implemented in Story 3.5 -->

Route tasks to models based on cognitive requirements declared in skill frontmatter.
```
- **Placement:** Add a substantive section below the existing line, or replace the placeholder comment with real content that includes the family/tier distinction and a cross-reference to spawning-patterns.md

### Architecture Constraints

These are all **rule files or reference files** — no compiled code, no tests required beyond functional verification. Changes must be:
- Declarative and prose-form (consistent with existing `.claude/rules/` style)
- Non-contradictory across files
- `spawning-patterns.md` is the single authoritative home for context tier behavior

### Project Structure Notes

- Global user rules live in `~/.claude/rules/` (outside this project directory) — the dev agent must edit these absolute paths directly
- Momentum references live at `skills/momentum/references/` (within this project at `/Users/steve/projects/momentum/skills/momentum/references/`)
- Do NOT create new files — all three changes are additions to existing files

### References

- [Source: ~/.claude/rules/spawning-patterns.md] — Fan-out vs TeamCreate decision rule
- [Source: skills/momentum/references/agent-skill-development-guide.md#Frontmatter-Schema] — `model:` schema entries (lines 10 and 75)
- [Source: ~/.claude/rules/model-routing.md] — Current placeholder content
- [Source: distill session] — Learning: context tier propagates from parent session; `model:` does not override it

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 3 → rule-hook (functional verification)
- Task 2 → skill-instruction (reference doc modification; EDD waiver: no SKILL.md or workflow.md created — NFR checks for ≤150-char description, model: frontmatter, ≤500 lines are N/A; one behavioral eval scenario provided below; AVFL checkpoint validates)
- Task 4 → unclassified (No Momentum-specific guidance for this task — standard bmad-dev-story DoD applies)

---

### rule-hook Tasks: Functional Verification

Rules files are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule** per the established format in existing `.claude/rules/` files
2. **State the expected behavior** as a testable condition: "Given a developer reads about context tier behavior in spawning-patterns.md, they will find an accurate, authoritative subsection explaining session-level inheritance and that `model:` does not override it"
3. **Verify functionally:**
   - For rules files: confirm all required sections are present and the rule is internally consistent
   - Confirm `spawning-patterns.md` does not contradict fan-out / TeamCreate guidance already present
   - Confirm `model-routing.md` forward reference does not create a circular or ambiguous pointer
4. **Document** the verification result and expected behavior in the Dev Agent Record

**Format requirements:**
- Rules files in `.claude/rules/` must follow the established markdown format (heading, body prose, no frontmatter)
- No duplicate entries (add once, cleanly)

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed and result documented
- [ ] Format matches established patterns

---

### skill-instruction Tasks: Reference Doc Modification

`agent-skill-development-guide.md` is classified as `skill-instruction` (files inside `skills/*/references/` per change-types.md detection rules). However, this task is a documentation addition (adding a caveat comment) to an existing reference file, not a new skill or behavioral instruction.

**EDD waiver authority:** change-types.md requires EDD for skill-instruction tasks, but the standard NFR checks (SKILL.md ≤150-char description, model: frontmatter presence, ≤500-line limit) are N/A here because no SKILL.md or workflow.md is being created — only a reference doc receives inline caveat additions. The waiver is self-justified by the task scope.

**Behavioral eval scenario (minimal, satisfies DoD):** Given a developer reads the `agent-skill-development-guide.md` `model:` schema entry (either Agent or SKILL.md section), they will find a caveat making clear the field controls model family only and does not override session context tier. The AVFL checkpoint run by `momentum:dev` validates the addition against the story ACs.

**Implementation approach:**
1. Read the file to locate the two `model:` schema entries
2. Add the caveat inline: append `— controls model family only, not context tier` (or equivalent phrasing) to the existing comment on each `model:` line
3. Verify surrounding schema entries are unaffected
4. Document in Dev Agent Record

**Additional DoD items for this task:**
- [ ] Both `model:` schema entries (Agent section and SKILL.md section) updated
- [ ] No surrounding schema entries modified
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

---

### Gherkin Specs Note

Gherkin `.feature` files for this sprint live in `sprints/{sprint-slug}/specs/`. Per Decision 30 (black-box separation), the dev agent implements against plain English ACs in this story file only — never against `.feature` files directly.

## Dev Agent Record

### Agent Model Used

(to be filled at implementation time)

### Debug Log References

### Completion Notes List

### File List

- `~/.claude/rules/spawning-patterns.md` — added `## Context Tier Inheritance` section
- `skills/momentum/references/agent-skill-development-guide.md` — added `model:` caveat to both frontmatter schema entries
- `~/.claude/rules/model-routing.md` — added family/tier distinction and cross-reference to spawning-patterns.md
