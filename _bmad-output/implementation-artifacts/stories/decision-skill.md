---
title: Decision Skill — Capture Strategic Decisions from Assessments
story_key: decision-skill
status: ready-for-dev
epic_slug: impetus-epic-orchestrator
depends_on:
  - assessment-skill
touches:
  - skills/momentum/skills/decision/SKILL.md
  - skills/momentum/skills/decision/workflow.md
  - _bmad-output/planning-artifacts/decisions/index.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/decisions/index.md
    relationship: derives_from
    section: "Decision Registry — artifact type definition"
---

# Decision Skill — Capture Strategic Decisions from Assessments

## Story

As a developer using Momentum,
I want a skill that captures strategic decisions in a structured format linked
to their source material,
so that the reasoning behind significant choices is preserved and traceable
to the stories that implement them.

## Description

Decisions (SDR) capture what was decided based on assessments and research. They
are the bridge between "we learned something" and "we're building something."
Without them, decisions fall through the cracks between research sessions and
sprint planning.

The skill supports three input flows:
- **From assessment:** Walk through an ASR's findings, decide what to do about each
- **From research:** Extract recommendations from a research doc, decide what to
  adopt/reject/defer
- **Revisit:** Re-evaluate a prior decision when conditions have changed

The skill captures decisions, it doesn't deliberate them. The deliberation already
happened in conversation or during the assessment.

Reference implementation: `/Users/steve/projects/nornspun/_bmad-output/planning-artifacts/decisions/sdr-001-agentic-ui-stack-eval.md`

## Acceptance Criteria (Plain English)

### AC1: Skill Is Independently Invocable

- A skill exists at `skills/momentum/skills/decision/SKILL.md` with valid
  frontmatter (name, description, model, effort)
- `/momentum:decision` works without Impetus running
- SKILL.md body delegates to `./workflow.md`
- SKILL.md description is under 150 characters

### AC2: Three Input Flows Supported

- **(A) From assessment:** The skill reads a specific ASR document, walks through
  its findings, and asks the developer what they want to decide about each
  gap/finding. Decisions may be: adopt a recommendation, reject with rationale,
  defer with conditions, or split into phased implementation.
- **(B) From research:** The skill reads a research document, extracts
  recommendations, and asks the developer what to adopt/reject/defer for each.
- **(C) Revisit:** The skill reads an existing SDR, checks whether conditions
  have changed (decision gates met, new research available, assessment findings
  that contradict the original rationale), and walks the developer through
  re-evaluation.

### AC3: Decisions Capture Full Context

- Each decision captures:
  - What was recommended (from source material)
  - What was decided (adopted/rejected/deferred/adapted)
  - The rationale (why this choice, in the developer's words)
  - Source material links (ASR or research doc path)
  - Affected stories (existing backlog stories impacted by the decision)
  - Affected architecture decisions (if any AD in architecture.md changes)

### AC4: SDR Document Written with Proper Format

- The output follows the SDR format with frontmatter:
  - id: SDR-NNN (auto-incremented from existing decisions)
  - title, date, status (decided/deferred/superseded)
  - source_research: list of source docs with type and date
  - prior_decisions_reviewed: list of ADs or prior SDRs reviewed
  - architecture_decisions_affected: list with outcome notes
  - stories_affected: list of backlog story slugs
- Body contains: Summary, individual Decisions (each with recommendation, decision,
  rationale), Phased Implementation Plan (if applicable), Decision Gates (if any)
- Written to `_bmad-output/planning-artifacts/decisions/`

### AC5: Upstream and Downstream Links Updated

- If the SDR was produced from an ASR, update the ASR's `decisions_produced`
  frontmatter field with the new SDR id
- Update `decisions/index.md` with the new entry

### AC6: Committed

- The SDR document, index update, and any ASR frontmatter update are committed
  together

### AC7: Bridge to Story Creation

- After decisions are captured, the skill offers: "Want to create stories for
  these decisions?"
- If yes, invoke `momentum:create-story` (or `momentum:intake` for lightweight
  capture) for each decision that implies new work

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-7)
  - [ ] Create eval verifying the three input flows and decision capture format

- [ ] Task 2 — Create SKILL.md (AC: 1)
  - [ ] Frontmatter: name: decision, model: claude-sonnet-4-6, effort: high
  - [ ] SKILL.md body delegates to ./workflow.md

- [ ] Task 3 — Create workflow.md (AC: 2-7)
  - [ ] Step 1: Determine input flow (A/B/C) and load source material
  - [ ] Step 2: Walk through findings/recommendations with developer
  - [ ] Step 3: For each finding, capture decision + rationale
  - [ ] Step 4: Identify affected stories and architecture decisions
  - [ ] Step 5: Write SDR document with proper frontmatter
  - [ ] Step 6: Update upstream links (ASR decisions_produced if applicable)
  - [ ] Step 7: Update decisions/index.md, commit
  - [ ] Step 8: Offer bridge to story creation

- [ ] Task 4 — Run eval and verify (AC: 1-7)

## Dev Notes

### Voice

Impetus voice. The skill captures decisions, it doesn't deliberate them. The
deliberation already happened in conversation or during the assessment. Present
options clearly, record what the developer decides, move on.

### SDR Frontmatter Schema

```yaml
id: SDR-NNN
title: descriptive title
date: 'YYYY-MM-DD'
status: decided | deferred | superseded
source_research:
  - path: relative/path/to/source.md
    type: assessment | gemini-deep-research | prior-research | architecture-analysis
    date: 'YYYY-MM-DD'
prior_decisions_reviewed:
  - AD-N (description)
architecture_decisions_affected:
  - AD-N outcome description
stories_affected:
  - story-slug-1
  - story-slug-2
```

### Key Constraint

The decision skill is a recorder, not a deliberator. It presents what was
recommended, captures what was decided, and links everything together. The
developer makes the actual decisions.

### Relationship to Other Skills

| Skill | Relationship |
|---|---|
| momentum:assessment | Upstream — ASRs are primary input for decisions |
| momentum:research | Upstream — research docs are alternative input |
| momentum:create-story | Downstream — decisions produce stories |
| momentum:intake | Downstream — lightweight story capture from decisions |
| momentum:refine | Reviews decisions for gate conditions and missing stories |

### References

- [Source: nornspun decisions/sdr-001-agentic-ui-stack-eval.md] — reference implementation
- [Source: _bmad-output/planning-artifacts/decisions/index.md] — registry format

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
