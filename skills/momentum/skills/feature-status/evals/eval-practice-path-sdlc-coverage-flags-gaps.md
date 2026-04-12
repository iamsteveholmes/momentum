# Eval: Practice Path SDLC Coverage Flags Gaps

## Scenario

Given skills covering Discovery, Planning, Specification, Implementation, Review,
Retrospective, and Orientation but no skill mapped to Quality/Validation, the skill's
SDLC coverage table marks Quality/Validation as "gap" and marks covered phases with
the relevant skill names.

---

## Setup

**Project structure signals practice project:**
- `skills/momentum/skills/` directory exists with at least one `*/SKILL.md`
- `_bmad-output/planning-artifacts/` directory exists

**Skills present (minimal set — Quality/Validation is intentionally uncovered):**
- research — "Deep research pipeline with parallel agent dispatch" → Discovery
- assessment — "Guided product state evaluation" → Discovery
- intake — "Capture a story idea from conversation" → Planning
- sprint-planning — "Sprint planning — story selection, team assignment" → Planning
- create-story — "Creates a Momentum story with change-type routing" → Specification
- decision — "Capture strategic decisions from assessment findings" → Specification
- dev — "Pure executor — resolves a story, creates implementation artifacts" → Implementation
- quick-fix — "Single-story fix — define, specify, implement" → Implementation
- code-reviewer — "Adversarial code reviewer with read-only tools" → Review
- retro — "Sprint retrospective — transcript auditing and practice improvement" → Retrospective
- impetus — "Momentum practice orchestrator — start here" → Orientation/Onboarding
- feature-status — "Generates an HTML planning artifact showing feature coverage" → Orientation/Onboarding

**Quality/Validation phase intentionally NOT covered** (no architecture-guard, no avfl skill present)

---

## Expected Behavior

1. The workflow discovers all 12 skills via glob
2. Maps each skill to one or more SDLC phases using name and description heuristics
3. Renders a compact table with 8 rows (one per phase)
4. Phases with covering skills show the skill names in the "Skills" column and "covered" in Status
5. Quality/Validation phase shows empty Skills column and "gap" in Status
6. No extra prose — just the table
7. The Retrospective phase is covered by `retro`
8. The Orientation/Onboarding phase is covered by `impetus` and `feature-status`

---

## Pass Criteria

- [ ] SDLC coverage table contains exactly 8 phase rows: Discovery, Planning, Specification,
      Implementation, Review, Retrospective, Orientation/Onboarding, Quality/Validation
- [ ] Quality/Validation row shows "gap" status (no covering skills)
- [ ] All 7 other phases show "covered" status
- [ ] Skill names appear in the covering column for each covered phase
- [ ] research and assessment both appear in Discovery row
- [ ] dev and quick-fix both appear in Implementation row
- [ ] impetus and feature-status both appear in Orientation/Onboarding row
- [ ] No extra prose in the coverage section

## Failure Criteria

- Quality/Validation is not flagged as "gap" despite no covering skills
- Table has fewer or more than 8 SDLC phase rows
- Covered phases show "gap" incorrectly
- Skill names are hardcoded rather than derived from discovered skills
- Phase rows are missing skill names (shows empty even when skills cover the phase)
