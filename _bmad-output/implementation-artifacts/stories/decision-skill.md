---
title: Decision Skill — Capture Strategic Decisions from Assessments
story_key: decision-skill
status: review
epic_slug: impetus-epic-orchestrator
depends_on:
  - assessment-skill
touches:
  - skills/momentum/skills/decision/SKILL.md
  - skills/momentum/skills/decision/workflow.md
  - skills/momentum/skills/decision/references/sdr-template.md
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

### AC4: SDR Template Exists

- A template exists at `skills/momentum/skills/decision/references/sdr-template.md`
- The template defines the complete SDR structure: frontmatter schema, body sections
  (Summary, individual Decisions with recommendation/decision/rationale, Phased
  Implementation Plan, Decision Gates), and formatting conventions
- The workflow uses this template to produce every SDR document — ensuring consistent
  format across decisions

### AC5: SDR Document Written from Template

- The output follows the SDR template with frontmatter:
  - id: SDR-NNN (auto-incremented from existing decisions)
  - title, date, status (decided/deferred/superseded)
  - source_research: list of source docs with type and date
  - prior_decisions_reviewed: list of ADs or prior SDRs reviewed
  - architecture_decisions_affected: list with outcome notes
  - stories_affected: list of backlog story slugs
- Body contains: Summary, individual Decisions (each with recommendation, decision,
  rationale), Phased Implementation Plan (if applicable), Decision Gates (if any)
- Written to `_bmad-output/planning-artifacts/decisions/`

### AC6: Upstream and Downstream Links Updated

- If the SDR was produced from an ASR, update the ASR's `decisions_produced`
  frontmatter field with the new SDR id
- Update `decisions/index.md` with the new entry

### AC7: Committed

- The SDR document, index update, and any ASR frontmatter update are committed
  together

### AC8: Bridge to Story Creation

- After decisions are captured, the skill offers: "Want to create stories for
  these decisions?"
- If yes, invoke `momentum:create-story` (or `momentum:intake` for lightweight
  capture) for each decision that implies new work

## Tasks / Subtasks

- [x] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-8)
  - [x] Create eval verifying the three input flows and decision capture format

- [x] Task 2 — Create SDR template (AC: 4)
  - [x] Create `skills/momentum/skills/decision/references/sdr-template.md`
  - [x] Include complete frontmatter schema and all body sections
  - [x] Use nornspun SDR-001 as reference for format

- [x] Task 3 — Create SKILL.md (AC: 1)
  - [x] Frontmatter: name: decision, model: claude-sonnet-4-6, effort: high
  - [x] SKILL.md body delegates to ./workflow.md

- [x] Task 4 — Create workflow.md (AC: 2-3, 5-8)
  - [x] Step 1: Determine input flow (A/B/C) and load source material
  - [x] Step 2: Walk through findings/recommendations with developer
  - [x] Step 3: For each finding, capture decision + rationale
  - [x] Step 4: Identify affected stories and architecture decisions
  - [x] Step 5: Write SDR document from template with proper frontmatter
  - [x] Step 6: Update upstream links (ASR decisions_produced if applicable)
  - [x] Step 7: Update decisions/index.md, commit
  - [x] Step 8: Offer bridge to story creation

- [x] Task 5 — Run eval and verify (AC: 1-8)

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

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- Implemented eval-first (EDD): behavioral eval written before any skill files
- sdr-template.md modeled on nornspun SDR-001 reference — includes frontmatter schema with all required fields, decision section format (recommendation/decision/rationale), Phased Implementation Plan and Decision Gates as optional sections, naming convention, auto-increment logic, and registry entry format
- SKILL.md delegates entirely to workflow.md — no inline logic; description is 128 chars (under 150 limit)
- workflow.md implements all three input flows (A: from assessment, B: from research, C: revisit) with flow-specific source loading; walks findings one at a time; captures verdict (adopt/reject/defer/adapt) and rationale; updates ASR decisions_produced for Flow A; commits all artifacts together; bridges to momentum:create-story or momentum:intake
- Step 3 of workflow separates affected stories and architecture decisions as a distinct capture phase before writing the SDR, ensuring full context is collected
- Verified all 8 ACs satisfied against eval criteria

### File List

- skills/momentum/skills/decision/SKILL.md (created)
- skills/momentum/skills/decision/workflow.md (created)
- skills/momentum/skills/decision/references/sdr-template.md (created)
- skills/momentum/skills/decision/evals/eval-three-input-flows-and-decision-capture.md (created)
