# Eval: Contract Authored Per Story

**ID:** eval-contract-authored-per-story
**Change-type:** skill-instruction
**Phase:** contract authoring (Step 3.5 Phase A)

## Scenario

Given a sprint with 3 approved stories of different change-types:
- `add-impetus-greeting` (change_type: skill-instruction)
- `hookify-pre-tool-guard` (change_type: rule-hook)
- `research-spike-avfl-perf` (change_type: specification)

And the verification-standard rule is available at `skills/momentum/references/rules/verification-standard.md`

And `momentum/verification-harness.json` is available

When Step 3.5 Phase A runs (contract authoring) after all 3 stories are approved

Then:
1. Three contract files are written to `.momentum/sprints/{sprint-slug}/specs/`:
   - `add-impetus-greeting.eval.yaml`
   - `hookify-pre-tool-guard.trigger.md`
   - `research-spike-avfl-perf.review.md`
2. Each contract file has a non-empty body (not just a header line)
3. Each contract body describes observable behaviors — what the feature does, not how it's implemented
4. No contract body references internal SKILL.md contents, delegation chains, or tool call sequences
5. The `.momentum/sprints/{sprint-slug}/specs/` directory is created if it did not exist

## Pass Criteria

- All three files exist with correct extensions
- Bodies are non-empty (> 10 lines each)
- No clause in any contract reads like: "when sprint-planning delegates to X", "when the hook in settings.json fires", "when the SKILL.md description field is read"

## Fail Criteria

- Any file is missing or has the wrong extension
- Any body is empty or contains only a template header
- Any clause references internal implementation detail
