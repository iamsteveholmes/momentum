---
title: Assessment Skill — Guided Product State Evaluation
story_key: assessment-skill
status: ready-for-dev
epic_slug: impetus-epic-orchestrator
depends_on: []
touches:
  - skills/momentum/skills/assessment/SKILL.md
  - skills/momentum/skills/assessment/workflow.md
  - skills/momentum/skills/assessment/references/asr-template.md
  - _bmad-output/planning-artifacts/assessments/index.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/assessments/index.md
    relationship: derives_from
    section: "Assessment Registry — artifact type definition"
---

# Assessment Skill — Guided Product State Evaluation

## Story

As a developer using Momentum,
I want a skill that guides me through producing a structured assessment of my
product's current state,
so that I have a clear, evidence-based snapshot of where things are, what works,
what's broken, and what decisions need to be made.

## Description

Assessments (ASR) are the missing bridge between research and decisions. Today,
findings from research sessions and codebase audits scatter across conversation
history with no durable artifact. The assessment skill produces a structured,
point-in-time snapshot that captures what was discovered and feeds forward into
decision records.

This is an ANALYSIS PHASE skill — conversational, not autonomous. The developer
drives the scope and validates every major finding. The skill discovers, presents,
and asks "does this match your understanding?" at every checkpoint. Findings are
not written into the ASR until the developer confirms them.

The pipeline this completes:

```
Research (external findings)
        ↘
         Assessment (where are we now?) ← THIS SKILL
        ↗
Codebase state
        ↘
         Decision (what do we do?)
                ↘
                 Stories (how do we do it?)
```

Reference implementation: `/Users/steve/projects/nornspun/_bmad-output/planning-artifacts/assessments/asr-001-community-readiness-2026-04-08.md`

## Acceptance Criteria (Plain English)

### AC1: Skill Is Independently Invocable

- A skill exists at `skills/momentum/skills/assessment/SKILL.md` with valid
  frontmatter (name, description, model, effort)
- `/momentum:assessment` works without Impetus running
- SKILL.md body delegates to `./workflow.md`
- SKILL.md description is under 150 characters

### AC2: Scoping Is Collaborative

- The skill starts by asking the developer what they want to assess (full product
  state? specific epic? a user journey? community readiness? a specific concern?)
- The developer and skill collaboratively determine:
  - What agents to spawn for discovery (backend audit, client audit, journey
    tracing, strategy alignment — whatever fits the scope)
  - What repos or directories to audit
  - What questions the assessment should answer
- The skill does not assume scope — it asks

### AC3: Parallel Discovery Based on Agreed Scope

- The skill spawns parallel discovery agents based on the scoping conversation
- Each agent audits actual codebase/artifact state (not documentation claims)
- Agents return structured findings with evidence (file paths, line counts,
  status assessments)
- The number and type of agents varies by scope — there is no fixed agent roster

### AC4: Findings Are Developer-Validated

- After discovery agents return, the skill presents findings to the developer
  section by section
- After each finding: "Does this match your understanding?" — the developer may
  challenge findings, add context the agents missed, or redirect investigation
- Findings are not written into the ASR until the developer confirms them
- The developer may request deeper investigation on any finding before confirming

### AC5: Recommended Next Steps Are Collaborative

- After all findings are discussed, the skill collaboratively drafts recommended
  next steps with the developer
- Next steps should be concrete and actionable (not vague "consider doing X")
- The developer approves the final next steps list before it's written

### AC6: ASR Template Exists

- A template exists at `skills/momentum/skills/assessment/references/asr-template.md`
- The template defines the complete ASR structure: frontmatter schema, body sections
  (Purpose, Method, Findings, Recommended Next Steps, Raw Data), and formatting
  conventions
- The workflow uses this template to produce every ASR document — ensuring consistent
  format across assessments

### AC7: ASR Document Written from Template

- The output follows the ASR template with frontmatter:
  - id: ASR-NNN (auto-incremented from existing assessments)
  - title, date, status (current), method (describes what agents were spawned)
  - decisions_produced: [] (empty — decisions come later)
  - supersedes: (if this replaces a prior assessment, link it)
- Body contains: Purpose, Method, numbered Findings (each with evidence tables),
  Recommended Next Steps, Raw Data (if applicable)
- Written to `_bmad-output/planning-artifacts/assessments/`

### AC8: Registry Updated and Committed

- `assessments/index.md` is updated with the new entry
- The ASR document and index update are committed together

### AC9: Bridge to Decision Skill

- After the ASR is written, the skill offers: "These findings are ready to feed
  into a decision record. Want to capture decisions now?"
- If yes, invoke `momentum:decision` (or flag for manual invocation if the skill
  doesn't exist yet)

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-9)
  - [ ] Create eval verifying the skill scopes collaboratively and validates
    findings with the developer before writing

- [ ] Task 2 — Create ASR template (AC: 6)
  - [ ] Create `skills/momentum/skills/assessment/references/asr-template.md`
  - [ ] Include complete frontmatter schema and all body sections
  - [ ] Use nornspun ASR-001 as reference for format

- [ ] Task 3 — Create SKILL.md (AC: 1)
  - [ ] Frontmatter: name: assessment, model: claude-sonnet-4-6, effort: high
  - [ ] SKILL.md body delegates to ./workflow.md

- [ ] Task 4 — Create workflow.md (AC: 2-5, 7-9)
  - [ ] Step 1: Scoping conversation — ask what to assess, agree on agent roster
  - [ ] Step 2: Spawn parallel discovery agents per agreed scope
  - [ ] Step 3: Present findings section by section with developer validation
  - [ ] Step 4: Collaboratively draft recommended next steps
  - [ ] Step 5: Write ASR document from template with proper frontmatter
  - [ ] Step 6: Update assessments/index.md, commit
  - [ ] Step 7: Offer bridge to decision skill

- [ ] Task 5 — Run eval and verify (AC: 1-9)

## Dev Notes

### Voice

Impetus voice — dry, factual, forward-moving. Present findings, don't
editorialize. Let the developer draw conclusions. Ask targeted questions to
sharpen the picture.

### ASR Frontmatter Schema

```yaml
id: ASR-NNN
title: descriptive title
date: 'YYYY-MM-DD'
status: current | superseded
method: description of discovery agents spawned
decisions_produced: [] # filled in later by decision skill
supersedes: # optional — path to prior assessment this replaces
```

### Key Constraint

Assessments are COLLABORATIVE. The skill guides and discovers, but the developer
validates. Every major finding gets a checkpoint. This is not an autonomous
report generator — it's a guided investigation.

### Relationship to Other Skills

| Skill | Relationship |
|---|---|
| momentum:decision | Assessment feeds forward — the ASR is source material for SDRs |
| momentum:refine | Refine will review assessments for staleness (Story 3) |
| momentum:research | Research produces external findings; assessment evaluates internal state |
| momentum:create-story | Stories may be created from assessment findings (via decisions) |

### References

- [Source: nornspun assessments/asr-001-community-readiness-2026-04-08.md] — reference implementation
- [Source: _bmad-output/planning-artifacts/assessments/index.md] — registry format

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
