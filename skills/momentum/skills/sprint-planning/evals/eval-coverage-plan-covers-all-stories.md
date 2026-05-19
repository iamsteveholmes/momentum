# Eval: Coverage Plan Covers All Stories

**ID:** eval-coverage-plan-covers-all-stories
**Change-type:** skill-instruction
**Phase:** coverage plan (Step 3.5 Phase B)

## Scenario

Given a sprint with 4 approved stories:
- `story-a` (skill-instruction) — invokes a skill that also exercises story-b's hook behavior
- `story-b` (rule-hook) — trigger fires during the same integration scenario as story-a
- `story-c` (specification) — standalone document review, no overlap
- `story-d` (script-code) — standalone script execution, no overlap

And contracts have been authored for all 4 stories

When Step 3.5 Phase B runs (coverage plan authoring)

Then `coverage-plan.md` is written to `.momentum/sprints/{sprint-slug}/` and:
1. The file opens with the anti-redundancy principle note: "Never validate in isolation what an integrated scenario already exercises."
2. An integration scenario is defined that covers both `story-a` and `story-b`
3. `story-a` and `story-b` are each listed as "covered-by-composition" under that scenario, with a rationale sentence
4. `story-c` and `story-d` are each listed as "dedicated-run" standalone verification targets
5. Every story in the sprint appears exactly once (no story is both covered-by-composition and dedicated-run)
6. Every scenario in the plan names at least one story it discharges
7. No story is omitted from the plan

## Pass Criteria

- `coverage-plan.md` exists at the sprint directory root
- Anti-redundancy note appears in the header section
- Each of the 4 stories appears exactly once
- Stories with shared integration scenario are marked covered-by-composition
- Isolated stories are marked dedicated-run
- Rationale is present for each covered-by-composition story

## Fail Criteria

- `coverage-plan.md` missing
- Any story appears more than once
- Any story is omitted
- Covered-by-composition stories lack rationale
- Anti-redundancy principle note absent
