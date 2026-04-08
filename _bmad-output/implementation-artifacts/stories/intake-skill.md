---
title: Intake Skill — Lightweight Story Capture from Conversation
story_key: intake-skill
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/intake/SKILL.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/intake/references/stub-template.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/implementation-artifacts/stories/refine-skill.md
    relationship: related_to
    section: "AC4: Priority suggestions require stories to exist in backlog"
---

# Intake Skill — Lightweight Story Capture from Conversation

## Story

As a developer in conversation with Claude,
I want to capture a story idea into the backlog with full context while it's fresh,
so that the intent, pain, scope, and constraints are preserved without running the
heavyweight create-story pipeline.

## Description

Today there are two extremes for getting a story into the backlog:

1. **Manual index stub** — Someone adds a one-line entry to stories/index.json with
   a title and `story_file: false`. Fast, but the conversational context ("this comes
   up every sprint, the workaround is X, the forgetting risk is Y") is lost entirely.

2. **Full create-story** — The heavyweight pipeline: artifact analysis, web research,
   change-type classification, implementation guide injection, AVFL checkpoint. Right
   for dev-ready stories, overkill for "throw this in the backlog."

The gap is a lightweight `/momentum:intake` command that captures a story idea at
conversational fidelity — the why, the scope, rough ACs, pain context — without the
full analysis pipeline. It produces a **stub story file** from a template that clearly
marks all sections as drafts requiring later enrichment, plus an index entry.

The stub template is a key deliverable. It must be visually unambiguous that sections
are NOT finished and require significant updating before development. This prevents a
dev agent from treating a stub as a ready-for-dev spec.

Create-story should later be able to detect an existing stub and enrich it rather than
starting from scratch, but that integration is out of scope for this story.

## Acceptance Criteria (Plain English)

### AC1: Skill Is Independently Invocable

- A skill exists at `skills/momentum/skills/intake/SKILL.md` with valid frontmatter
  (name, description, model, effort)
- `/momentum:intake` works without Impetus running and without an active sprint
- SKILL.md body delegates to `./workflow.md`
- SKILL.md description is under 150 characters

### AC2: Conversational Context Capture

- The skill extracts story information from the current conversation or user-provided
  arguments:
  - Title (required)
  - Description — the "why" and scope as described conversationally
  - User story statement (as a / I want / so that) — derived from context
  - Rough acceptance criteria — captured as-is from conversation, not polished
  - Pain context — recurrence, workaround burden, forgetting risk, any other
    rationale the user provided for why this matters
  - Suggested epic and priority
- The skill does NOT run: artifact analysis, web research, architecture deep-dive,
  change-type classification, AVFL checkpoint, or implementation guide injection

### AC3: Stub Template Produces Clearly Draft Output

- A stub template exists at `skills/momentum/skills/intake/references/stub-template.md`
- The template includes all sections from the full story template
- Every section that has not been fully populated MUST contain an explicit draft
  marker that states this section is a draft and must be rewritten during the
  create-story phase. The marker must be unambiguous — both an HTML comment
  (e.g., `<!-- DRAFT: This section is a stub. It MUST be rewritten by create-story
  before development. -->`) and visible inline text (e.g., `_DRAFT — requires
  rewrite via create-story before this story is dev-ready._`)
- The only sections that are NOT marked as drafts are: story key/slug, title, and
  the initial description/user story captured by intake
- Sections that MUST be marked as draft: Acceptance Criteria (rough ACs from
  conversation are explicitly labeled as draft needing refinement), Dev Notes,
  architecture compliance, testing requirements, implementation guide, Tasks/Subtasks,
  Dev Agent Record
- The status in the stub is set to `backlog` (NOT `ready-for-dev`)
- A create-story agent reading this file should have zero confusion about which
  sections need to be rewritten and which are already finalized

### AC4: Index Entry Written with Epic Assignment

- The skill adds an entry to `stories/index.json` via momentum-tools CLI with:
  - status: `backlog`
  - title: from captured context
  - epic_slug: assigned to an epic (required, not optional)
  - story_file: `true`
  - priority: from suggested priority (or `low` if not provided)
  - depends_on: `[]` (intake doesn't analyze dependencies)
  - touches: `[]` (intake doesn't analyze file scope)
- Epic assignment is part of the intake workflow — the skill must determine which
  epic the story belongs to, either from the user's suggestion or by reading
  the epic list from epics.md/stories/index.json and recommending the best fit
- If the epic cannot be determined, the skill asks the user rather than defaulting
  to a placeholder

### AC5: Slug Generation

- The story slug is derived from the title: lowercased, spaces to hyphens, stripped
  of special characters, truncated to reasonable length
- If the slug already exists in stories/index.json, the skill reports the conflict
  and asks the user for an alternative

### AC6: Minimal Tool Calls

- The skill should complete in a small number of tool calls — it reads
  stories/index.json once (to check for slug conflicts), writes the stub file, and
  runs the CLI to add the index entry
- No subagent spawns, no parallel discovery, no web research

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-6)
  - [ ] Create `skills/momentum/skills/intake/evals/eval-intake-captures-context.md`
    — verifies the skill captures conversational context into a stub file with draft
    markers and writes an index entry

- [ ] Task 2 — Create stub template (AC: 3)
  - [ ] Create `skills/momentum/skills/intake/references/stub-template.md`
  - [ ] Include all sections from full story template
  - [ ] Add visible draft indicators to unpopulated sections
  - [ ] Ensure status defaults to `backlog`
  - [ ] Verify a dev agent would clearly recognize this as not ready for implementation

- [ ] Task 3 — Create SKILL.md (AC: 1)
  - [ ] Create `skills/momentum/skills/intake/SKILL.md` with frontmatter
    (name: intake, model: claude-sonnet-4-6, effort: low)
  - [ ] SKILL.md body delegates to `./workflow.md`
  - [ ] Verify description under 150 characters

- [ ] Task 4 — Create workflow.md (AC: 2, 4, 5, 6)
  - [ ] Step 1: Extract story context from conversation/arguments
  - [ ] Step 2: Generate slug, check for conflicts in stories/index.json
  - [ ] Step 3: Populate stub template with captured context
  - [ ] Step 4: Write stub file and add index entry via momentum-tools CLI
  - [ ] Step 5: Report what was captured and what still needs enrichment

- [ ] Task 5 — Run eval and verify (AC: 1-6)
  - [ ] Run eval via subagent
  - [ ] Confirm skill is independently invocable
  - [ ] Confirm stub file has clear draft indicators
  - [ ] Confirm index entry uses momentum-tools CLI (not direct JSON edit)

## Dev Notes

### Stub Template Design

The stub template must make the draft state impossible to miss. Approach:

```markdown
## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture
     analysis, implementation guide, and technical requirements. -->

_This section is a stub. It requires enrichment before development._
```

Both the HTML comment (visible to agents reading the file) and the italic text
(visible to humans) signal draft state. The frontmatter `status: backlog` is the
machine-readable signal.

### CLI Commands Needed

**Index entry creation:** The skill needs to add an entry to stories/index.json.
Check whether `momentum-tools sprint` has a command for adding a new story entry.
If not, this story may need to add one — but check first, as triage or sprint-planning
may have already created this path.

**No new priority/status commands needed** — intake only uses `backlog` status and
the standard priority levels.

### Relationship to create-story

Intake and create-story are complementary, not competing:

| Aspect | intake | create-story |
|---|---|---|
| When to use | "Throw this in the backlog" | "Spec this for development" |
| Output status | `backlog` | `ready-for-dev` |
| Analysis depth | Conversational capture only | Full artifact + web research |
| Time/cost | Seconds, minimal tool calls | Minutes, subagent spawns |
| Dev Notes | Stub (draft markers) | Fully populated |

Future enhancement (out of scope): create-story detects an existing stub and enriches
it instead of starting from scratch. This would make intake -> create-story a natural
two-phase pipeline.

### Orchestrator Purity

The intake skill is lightweight but still follows orchestrator purity (Decision 3d):
- Reads stories/index.json (to check slug conflicts)
- Writes the stub file (Write tool — this is the one file intake is sole author of)
- Adds index entry via momentum-tools CLI (Bash tool)
- No subagent spawns needed

### What NOT to Change

- `momentum:create-story` — intake is additive, not a replacement
- `momentum:refine` — refine operates on whatever's in the backlog; intake just adds to it
- `stories/index.json` schema — no new fields needed
- `momentum-tools.py` — check if story-add command exists first; if not, add it as a
  subtask but keep it minimal

### Project Structure Notes

- Skill directory: `skills/momentum/skills/intake/`
- Stub template: `skills/momentum/skills/intake/references/stub-template.md`
- Eval directory: `skills/momentum/skills/intake/evals/`
- CLI: `skills/momentum/scripts/momentum-tools.py`

### References

- [Source: skills/momentum/skills/create-story/workflow.md] — heavyweight pipeline this complements
- [Source: .claude/skills/bmad-create-story/template.md] — full story template (stub template derives from this)
- [Source: skills/momentum/scripts/momentum-tools.py] — CLI for index mutations

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
