---
title: UX Base Body — Universal Agent Role Contract for UX Designer
story_key: ux-base-body
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: feature
change_type: agent
depends_on: []
touches:
  - skills/momentum/agents/ux.md
---

# UX Base Body — Universal Agent Role Contract for UX Designer

## Story

As a sprint-dev orchestrator spawning agents for UX work,
I want an `agents/ux.md` base body file that defines the UX agent role contract,
so that orchestrators can spawn a consistent, unconditioned UX agent that the
agent-composition-pipeline can layer project-specific context onto.

## Description

DEC-020 established nine universal base bodies that ship in the Momentum plugin
(Decision D1). Three of those nine were missing at the time of the decision —
ux, analyst, and researcher — identified in Decision D5. This story delivers
`skills/momentum/agents/ux.md`, one of those three.

The base body is an unconditioned agent definition: it declares the UX role
identity, behavioral constraints, output format contract, and document ownership
scope, but contains no project-specific context. The agent-composition-pipeline
layers project knowledge on top when assembling a composed agent for a specific
project.

BMAD role alignment: the Momentum UX base body corresponds to the `bmad-agent-ux-designer`
role (Sally). The base body strips the interactive persona mechanics (activation
steps, menu, icon prefix) and replaces them with orchestrator-friendly spawning
semantics — purpose-driven rather than conversation-driven.

Without this file, the agent-composition-pipeline cannot assemble a UX agent for
any project, blocking orchestrator-driven UX work (sprint-dev UX story execution,
retro synthesis of UX findings, design review phases).

## Acceptance Criteria (Plain English)

### AC1: File Exists at the Correct Path

`skills/momentum/agents/ux.md` exists in the Momentum plugin. No other location
is acceptable — base bodies must be co-located with the existing agents (dev.md,
qa-reviewer.md, e2e-validator.md) so the agent-composition-pipeline can discover
them by convention.

### AC2: Frontmatter Is Complete and Valid

The file includes YAML frontmatter with at minimum:
- `name: ux`
- `description:` — action-oriented trigger description, under 250 characters,
  front-loads the use case (spawning context: sprint UX story execution, design
  review, UX findings synthesis)
- `model:` — set to `sonnet`
- `effort:` — set to `medium`
- `tools:` — includes Read, Glob, Grep, Bash, Edit, Write (UX agent needs write
  access to produce UX specs and design documents)

### AC3: Role Identity Is Declared

The system prompt body opens with a clear "You are..." role statement that:
- Names the role as UX designer / UX agent in Momentum's practice
- Distinguishes this from an interactive persona — this agent is spawned by an
  orchestrator, not invoked by a user in conversation
- States the agent's primary purpose: produce UX deliverables from story specs

### AC4: Behavioral Constraints Are Explicit

The file includes a "Critical Constraints" section (matching the pattern in
dev.md and qa-reviewer.md) covering:
- Scope: this agent is scoped to a single story or design task per spawn
- Write authority: the agent produces UX artifacts but does NOT modify non-UX
  files (no touching story indexes, sprint records, or architecture docs)
- Commit behavior: the agent commits completed UX artifacts with a conventional
  commit message, staging only UX-relevant files
- Structured output: the agent emits a structured `AGENT_OUTPUT_START/END` block
  so the orchestrator can parse results

### AC5: Document Ownership Scope Is Declared

The file declares the artifact families owned by the UX role:
- UX specifications (ux-design-specification.md, ux-spec-*.md)
- Wireframe descriptions and interaction design documents
- Design requirement documents
- UX findings in retro/review contexts

This ownership declaration is what allows the agent-composition-pipeline and
the AVFL fixer routing table (DEC-025) to resolve "who fixes this artifact?"
for UX-owned files.

### AC6: Output Format Contract Is Defined

The file specifies the structured output block the agent emits on completion,
using the same AGENT_OUTPUT_START/END envelope as dev.md:
- `status`: complete | failed
- `story_key`: the story being implemented
- `files_changed`: list of created/modified UX artifact paths
- `ux_artifacts`: list of artifact types produced (spec, wireframe, requirements)

### AC7: Large File Handling Section Is Present

The file includes the standard `## Large File Handling` section (required
convention per agent-skill-development-guide.md). The section is under 20 lines
and covers: offset/limit usage, search-before-read pattern, named large files,
and error recovery.

### AC8: The Two Behavioral Evals Pass

Both evals written in Task 1 pass when run against the completed `ux.md`:
- Eval 1: structural completeness — all required sections present, frontmatter
  valid, Large File Handling section present and correctly sized
- Eval 2: role identity and behavioral constraints — role statement is
  orchestrator-appropriate (not interactive persona), document ownership is
  declared, write authority is scoped to UX artifacts only

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before implementation) (AC: 8)
  - [ ] Create `skills/momentum/agents/evals/eval-ux-base-body-structure.md`
    — verifies structural completeness: file exists, frontmatter has required
    fields (name, description, model, effort, tools), all required sections
    present (role statement, Critical Constraints, document ownership, output
    format, Large File Handling), Large File Handling section is under 20 lines
  - [ ] Create `skills/momentum/agents/evals/eval-ux-base-body-role-contract.md`
    — verifies role contract correctness: "You are..." opens the body, agent
    is framed as orchestrator-spawned (not interactive persona), document
    ownership names at least ux specs and design docs, write authority is scoped
    to UX artifacts, AGENT_OUTPUT_START/END envelope is present with required
    fields (status, story_key, files_changed)

- [ ] Task 2 — Implement `skills/momentum/agents/ux.md` (AC: 1–7)
  - [ ] Write frontmatter: name, description, model=sonnet, effort=medium, tools
  - [ ] Write role statement: orchestrator-spawned UX agent, not interactive
  - [ ] Write Critical Constraints section: story scope, write authority, commit
    behavior, structured output requirement
  - [ ] Write Input section: what the agent receives when spawned (story_file,
    sprint_slug, role, guidelines)
  - [ ] Write Process section: read story → produce UX artifacts → commit → emit
    structured output
  - [ ] Declare document ownership: ux specs, wireframes, design docs, UX requirements
  - [ ] Write Output Format section: AGENT_OUTPUT_START/END block with ux_artifacts field
  - [ ] Add standard Large File Handling section (copy from dev.md as baseline,
    adapt if UX-specific large files differ)

- [ ] Task 3 — Validate evals pass (AC: 8)
  - [ ] Run eval-ux-base-body-structure.md against the completed ux.md
  - [ ] Run eval-ux-base-body-role-contract.md against the completed ux.md
  - [ ] Confirm both evals produce no failures
  - [ ] Commit: `feat(agents): add ux.md base body — DEC-020 universal role contract`

## Dev Notes

### Role Identity

The UX agent is an orchestrator-spawned executor, not an interactive persona.
The BMAD Sally persona (activation steps, menu, icon prefix, persistent facts)
is deliberately absent — those mechanics serve interactive conversation sessions.
This agent receives a spawn prompt from sprint-dev or another orchestrator,
produces UX artifacts, and returns structured output.

The opening role statement should follow the same pattern as dev.md and qa-reviewer.md:
```
You are a UX agent in Momentum's sprint execution. You produce UX design artifacts
from story specs.
```

Not:
```
You are Sally, the UX Designer. [persona mechanics]
```

### Behavioral Constraints

Model after the "Critical Constraints" pattern in dev.md. Key constraints for the UX agent:

**You are scoped to one story.** The orchestrator delivers a story file; the UX agent
designs for that story only. It does not select stories or manage sprint state.

**Write authority is scoped to UX artifacts.** The agent writes to UX spec files,
wireframe descriptions, and design documents. It does not write to story indexes
(`stories/index.json`), sprint records, architecture docs, or code files.

**Commit when done.** After artifacts are produced, commit with a conventional commit
message. Stage only UX artifact files — never `git add -A`.

**Return structured output.** The AGENT_OUTPUT_START/END block allows sprint-dev to
parse completion status. Include a `ux_artifacts` field listing what was produced.

### Output Format Contract

Extend the standard AGENT_OUTPUT_START/END envelope (from dev.md) with a UX-specific
field:

```json
{
  "status": "complete",
  "story_key": "{story_key}",
  "files_changed": ["{list of ux artifact files created or modified}"],
  "ux_artifacts": ["ux-spec", "wireframe", "design-requirements"]
}
```

The `ux_artifacts` field uses a controlled vocabulary:
- `ux-spec` — UX specification document
- `wireframe` — wireframe description or interaction diagram
- `design-requirements` — design requirement document
- `ux-findings` — UX-focused findings in retro or review context

### Document Ownership Scope

Per DEC-020 D5, the UX role owns:
- UX specifications (`ux-design-specification.md`, `ux-spec-*.md`)
- Wireframe descriptions and interaction design documents
- Design requirement documents
- UX findings in retro and review artifacts

This ownership is what the AVFL fixer routing table (DEC-025) consults when a
finding is attributed to a UX-owned file — it resolves to the UX base body as
the fix executor.

### Process Section Shape

Follow the same four-step pattern as dev.md:
1. Read the story (extract ACs, dev notes, file list, change_type, touches)
2. Produce UX artifacts (the core design work — read guidelines if provided)
3. Commit changes (stage only UX-relevant files)
4. Return structured output (AGENT_OUTPUT_START/END block)

Unlike dev.md, the UX agent does NOT delegate to bmad-dev-story. It performs its
own artifact production directly.

### Tool Set Rationale

Read, Glob, Grep — for reading story specs, architecture docs, existing design context.
Bash — for git operations (commit), file existence checks.
Edit, Write — for creating and modifying UX specification documents.

The UX agent does NOT need Agent or Skill tools — it does not spawn subagents or
invoke skills. If the scope grows to require delegation, that decision belongs in a
new story.

### Large File Handling Placement

Insert the standard Large File Handling section after the Process section and before
the Output Format section (same placement as qa-reviewer.md and e2e-validator.md).
Copy the standard text from dev.md — no UX-specific adaptation is needed since the
UX agent reads the same types of large files (architecture.md, prd.md, story index).

### Eval Verification Strategy

**Eval 1 (structural completeness)** — purely mechanical. Grep checks:
- File exists at `skills/momentum/agents/ux.md`
- Frontmatter contains `name: ux`, `model:`, `effort:`, `tools:`
- Body contains `## Critical Constraints`, `## Large File Handling`, `## Output Format`
  (or equivalents)
- Large File Handling section is ≤ 20 lines (count lines between heading and next `##`)

**Eval 2 (role contract correctness)** — semantic checks:
- First non-frontmatter line of body contains "You are" and "UX"
- Body does NOT contain "Sally" or "persona" or "menu" or "icon" (interactive
  persona markers absent)
- Body contains at least two of: "ux spec", "wireframe", "design", "ux-design"
  (document ownership evidence)
- Body contains "AGENT_OUTPUT_START" (structured output envelope present)
- Body contains `"status"`, `"story_key"`, `"files_changed"` (required output fields)

### Project Structure Notes

- Output file: `skills/momentum/agents/ux.md`
- Eval files: `skills/momentum/agents/evals/eval-ux-base-body-structure.md`
  and `skills/momentum/agents/evals/eval-ux-base-body-role-contract.md`
- Reference agents: `skills/momentum/agents/dev.md` (process and output format),
  `skills/momentum/agents/qa-reviewer.md` (constraints and Large File Handling placement)
- Development guide: `skills/momentum/references/agent-skill-development-guide.md`

### References

- DEC-020 D1: Nine universal base bodies (architect, pm, ux, analyst, researcher, dev, sm, qa, e2e)
- DEC-020 D5: UX, analyst, researcher identified as missing — stories created
- DEC-025: AVFL fixer routing table (document ownership drives fix executor selection)
- Source: handoff agent-architecture-triage-2026-05-16.md

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
