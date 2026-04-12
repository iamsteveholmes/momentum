# Eval: Practice Path Topology Shows Hand-offs

## Scenario

Given a Momentum project with skills installed under `skills/momentum/skills/*/SKILL.md`,
the skill renders an ASCII topology block showing the canonical cycle
(intake → sprint-planning → sprint-dev → retro) and the assessment sub-cycle
(assessment → decision → create-story), with all discovered skills appearing in
at least one position.

---

## Setup

**Project structure signals practice project:**
- `skills/momentum/skills/` directory exists with at least one `*/SKILL.md`
- `_bmad-output/planning-artifacts/` directory exists

**Skills present (discovered via glob):**
- intake — "Capture a story idea and add it to the intake queue"
- sprint-planning — "Sprint planning — story selection, team assignment, wave scheduling"
- sprint-dev — "Sprint execution — dependency-driven story dispatch"
- retro — "Sprint retrospective — transcript auditing and practice improvement"
- assessment — "Guided product state evaluation"
- decision — "Capture strategic decisions from assessment findings"
- create-story — "Creates a Momentum story with change-type routing"
- dev — "Pure executor — resolves a story"
- quick-fix — "Single-story fix"
- impetus — "Momentum practice orchestrator"
- feature-status — "Generates feature coverage and topology view"
- research — "Deep research pipeline"
- code-reviewer — "Adversarial code reviewer"
- avfl — "Adversarial Validate-Fix Loop"
- architecture-guard — "Detects pattern drift against architecture"
- distill — "Practice artifact distillation"
- refine — "Backlog hygiene"

---

## Expected Behavior

1. The workflow detects it is in a practice project (skills/ + planning-artifacts/ present)
2. An ASCII topology block is rendered showing:
   - The canonical cycle: `intake → sprint-planning → sprint-dev → retro → (next cycle)`
   - The assessment sub-cycle: `assessment → decision → create-story → sprint-planning`
3. All discovered skills appear in at least one position in the topology or coverage map
4. Orientation skills (impetus, feature-status) are noted as sitting above/outside the cycle
5. The topology block is under 12 lines

---

## Pass Criteria

- [ ] Project type detected as "practice" based on filesystem structure (no config flag needed)
- [ ] ASCII topology block rendered with canonical cycle: intake → sprint-planning → sprint-dev → retro
- [ ] Assessment sub-cycle rendered: assessment → decision → create-story → sprint-planning
- [ ] Topology block is 12 lines or fewer
- [ ] All discovered skills appear somewhere in the output (topology or coverage table)
- [ ] Total output is under 40 lines

## Failure Criteria

- Practice project detection requires a config flag or features.json `project_type` field
- Topology block omits the intake → sprint-planning → sprint-dev → retro canonical cycle
- Topology block omits the assessment → decision → create-story sub-cycle
- Any discovered skill is absent from both the topology and coverage table
- Topology block exceeds 12 lines
- Total output exceeds 40 lines
