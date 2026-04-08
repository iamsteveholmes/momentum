---
title: Agent Prompt Large-File Guidance — Standard Instructions for Context-Exceeding Files
story_key: agent-prompt-large-file-guidance
status: ready-for-dev
epic_slug: agent-team-model
depends_on: []
touches:
  - skills/momentum/agents/dev.md
  - skills/momentum/agents/dev-skills.md
  - skills/momentum/agents/dev-build.md
  - skills/momentum/agents/dev-frontend.md
  - skills/momentum/agents/qa-reviewer.md
  - skills/momentum/agents/e2e-validator.md
  - skills/momentum/references/agent-skill-development-guide.md
change_type: config-structure
derives_from:
  - path: _bmad-output/implementation-artifacts/sprints/sprint-2026-04-06-2/retro-transcript-audit-teamcreate.md
    relationship: retro_finding
    section: "S5. file_too_large errors dominate the error population (33.6%)"
---

# Agent Prompt Large-File Guidance — Standard Instructions for Context-Exceeding Files

## Story

As a sprint-dev orchestrator spawning agents for story implementation and review,
I want all agent definitions to include standard guidance for handling files that
exceed the Read tool's token limit,
so that agents use offset/limit parameters and targeted search instead of failing
or hallucinating when encountering large files.

## Description

Sprint retro audit of sprint-2026-04-06-2 revealed that 196 of 584 tool errors
(33.6%) were `file_too_large` errors — agents attempting to read entire architecture
docs, PRDs, JSONL extracts, and other large files without using offset/limit
parameters. This was the single most common error type in the sprint and is entirely
preventable.

The root cause is simple: agent definitions and spawn prompts contain no guidance on
handling large files. Agents default to reading entire files, hit the Read tool's
token limit (10,000 tokens per read), fail, then retry or work around — adding 1-3
wasted turns per occurrence. Across 196 occurrences, this represents ~300-600 wasted
turns of compute.

The fix is a standard "Large File Handling" section added to every agent definition
in `skills/momentum/agents/`. The section teaches agents to:

1. **Anticipate large files** — architecture.md, prd.md, epics.md, JSONL extracts,
   and index.json files routinely exceed 10K tokens
2. **Use offset/limit** — read specific portions of files when the full file is not
   needed
3. **Search before reading** — use Grep to find relevant sections, then read only
   those sections with offset/limit
4. **Handle the error gracefully** — when a Read fails with a token-limit error,
   fall back to Grep + targeted Read rather than retrying the same full-file read

This guidance should also be added to the agent-skill-development-guide.md reference
so that future agent definitions inherit the pattern by convention.

## Acceptance Criteria (Plain English)

### AC1: Standard Large-File Handling Section Exists in All Agent Definitions

- Every agent definition file in `skills/momentum/agents/*.md` includes a
  "Large File Handling" section (or equivalent) in its system prompt body
- The section covers: known large files, offset/limit usage, search-before-read
  strategy, and error recovery
- The section is concise — under 20 lines per agent definition — so it does not
  bloat agent system prompts

### AC2: Guidance Is Actionable and Specific

- The guidance names specific files that commonly exceed limits (architecture.md,
  prd.md, epics.md, index.json, JSONL extracts)
- The guidance includes concrete examples of offset/limit usage (not just "use
  offset/limit" but "Read with offset=0, limit=100 to get the first 100 lines")
- The guidance prescribes the search-then-read pattern: Grep for the relevant
  section heading or keyword, note the line number, then Read with offset/limit
  targeting that area

### AC3: Agent-Skill Development Guide Updated

- `skills/momentum/references/agent-skill-development-guide.md` includes a section
  on large file handling as a standard convention for all agent definitions
- Future agent definitions created from this guide will include large-file guidance
  by default

### AC4: No Agent Behavior Regression

- Existing agent behaviors (dev delegation to bmad-dev-story, qa-reviewer read-only
  constraint, e2e-validator behavioral focus, etc.) are unchanged
- The only change to each agent file is the addition of the large-file handling
  section — no other sections are modified
- All agents retain their existing frontmatter, tools, and process steps

### AC5: Guidance Works for Both Read-Only and Read-Write Agents

- The large-file section is appropriate for both read-only agents (qa-reviewer,
  e2e-validator) and read-write agents (dev, dev-skills, dev-build, dev-frontend)
- The guidance does not reference tools that a read-only agent does not have

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-5)
  - [ ] Create `skills/momentum/agents/evals/eval-large-file-guidance-present.md`
    — verifies every agent definition in agents/*.md includes a large-file handling
    section with offset/limit guidance, named large files, and search-before-read
    pattern

- [ ] Task 2 — Draft the standard large-file handling section (AC: 1, 2, 5)
  - [ ] Write the reusable section content covering: known large files,
    offset/limit mechanics, search-before-read pattern, error recovery
  - [ ] Keep it under 20 lines
  - [ ] Ensure it references only tools available to all agents (Read, Grep —
    both are in every agent's tool list)

- [ ] Task 3 — Add section to all agent definitions (AC: 1, 4)
  - [ ] Add to `skills/momentum/agents/dev.md`
  - [ ] Add to `skills/momentum/agents/dev-skills.md`
  - [ ] Add to `skills/momentum/agents/dev-build.md`
  - [ ] Add to `skills/momentum/agents/dev-frontend.md`
  - [ ] Add to `skills/momentum/agents/qa-reviewer.md`
  - [ ] Add to `skills/momentum/agents/e2e-validator.md`
  - [ ] Verify no existing sections are modified — addition only

- [ ] Task 4 — Update agent-skill-development-guide.md (AC: 3)
  - [ ] Add a "Large File Handling" subsection under the Agent Definition Files
    section of `skills/momentum/references/agent-skill-development-guide.md`
  - [ ] Document this as a standard convention for all agent definitions

- [ ] Task 5 — Run eval and verify non-regression (AC: 1-5)
  - [ ] Run eval via subagent
  - [ ] Confirm all 6 agent definitions have the section
  - [ ] Confirm no other sections in any agent file were modified (diff check)
  - [ ] Confirm agent-skill-development-guide.md has the convention

## Dev Notes

### Known Large Files in Momentum

These files routinely exceed the Read tool's 10,000-token limit:

| File | Typical Size | Why Agents Read It |
|---|---|---|
| `_bmad-output/planning-artifacts/architecture.md` | ~42K tokens | Architecture decisions, story context |
| `_bmad-output/planning-artifacts/prd.md` | ~30K+ tokens | FR references, requirement context |
| `_bmad-output/planning-artifacts/epics.md` | ~15K tokens | Epic membership, story mapping |
| `_bmad-output/implementation-artifacts/stories/index.json` | ~20K tokens | Story lookup, dependency checking |
| `_bmad-output/implementation-artifacts/sprints/*/audit-extracts/*.jsonl` | Variable, often large | Retro transcript analysis |

### Standard Section Content (Draft)

The section added to each agent should follow this pattern:

```markdown
## Large File Handling

Some project files exceed the Read tool's token limit (10,000 tokens). When you
encounter a file-too-large error or need to read a file known to be large, use
these strategies:

1. **Search before reading** — Use Grep to find the specific section, heading, or
   keyword you need. Note the line number from Grep output, then Read with offset
   and limit targeting that area.
2. **Read in chunks** — Use `offset` and `limit` parameters: `offset=0, limit=200`
   for the first 200 lines, then adjust as needed.
3. **Known large files** — These commonly exceed limits: architecture.md, prd.md,
   epics.md, stories/index.json, and JSONL audit extracts. Never attempt a full
   read of these files.
4. **On error, narrow scope** — If a Read fails with a token-limit error, do not
   retry the same read. Instead, Grep for what you need and read only that section.
```

This is approximately 12 lines of instruction — well within the 20-line budget.
The exact wording may vary slightly per agent if role-specific nuance is needed
(e.g., qa-reviewer reads story files + implementation files, dev reads story files +
architecture), but the core pattern is identical.

### Placement Within Agent Files

Insert the section after the agent's existing process/behavior sections but before
the output format section. For agents that end with an output format (dev.md,
qa-reviewer.md, e2e-validator.md), place it before the output section. For agents
that end with an implementation approach paragraph (dev-skills.md, dev-build.md,
dev-frontend.md), place it before that paragraph.

Placement per file:
- `dev.md` — after "What NOT to Do", before end of file
- `dev-skills.md` — after "Conventional Commits", before "Implementation Approach"
- `dev-build.md` — after "Common Pitfalls", before "Implementation Approach"
- `dev-frontend.md` — after "Common Pitfalls", before "Implementation Approach"
- `qa-reviewer.md` — after "Cross-Story Integration Check" (step 4), before
  "Output Format"
- `e2e-validator.md` — after "Cross-Scenario Consistency" (step 4), before
  "Output Format"

### What NOT to Change

- **Agent frontmatter** — no changes to name, description, model, effort, or tools
- **Existing process steps** — the large-file section is additive, not a replacement
  for any existing instruction
- **Sprint-dev workflow** — this story does not modify how agents are spawned
- **SKILL.md files** — skills are not affected; this is agent-definitions only
- **bmad-dev-story** — the dev agent's delegation target is unchanged

### Requirements Coverage

- Retro finding S5: "Add standard instruction to agent definitions: When reading
  files that may be large, use offset/limit parameters or search for specific
  content"
- Retro Pattern 3: "Error patterns that could be eliminated by better prompts" —
  file_too_large accounts for 33.6% of all tool errors
- Architecture Decision 26: Two-Layer Agent Model — agent definitions carry practice
  knowledge; this adds large-file practice knowledge to the agent layer

### Project Structure Notes

- Agent definitions: `skills/momentum/agents/*.md` (6 files)
- Development guide: `skills/momentum/references/agent-skill-development-guide.md`
- Eval directory: `skills/momentum/agents/evals/`

### References

- [Source: _bmad-output/implementation-artifacts/sprints/sprint-2026-04-06-2/retro-transcript-audit-teamcreate.md] — retro finding S5
- [Source: skills/momentum/references/agent-skill-development-guide.md] — agent definition conventions

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
