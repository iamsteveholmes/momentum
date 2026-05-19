# Eval: Activation Blocked Without Contracts

**ID:** eval-activation-blocked-without-contracts
**Change-type:** skill-instruction
**Phase:** activation gate (Step 8)

## Scenario

Given a sprint with 3 stories where:
- `story-a` has a contract file at `.momentum/sprints/{sprint-slug}/specs/story-a.eval.yaml`
- `story-b` does NOT have a contract file (specs/ exists but no story-b.* file)
- `story-c` has a contract file at `.momentum/sprints/{sprint-slug}/specs/story-c.trigger.md`

And `coverage-plan.md` EXISTS at `.momentum/sprints/{sprint-slug}/coverage-plan.md`

When Step 8 (Activate the sprint) runs and the activation gate check executes

Then:
1. The gate detects that `story-b` is missing a contract file
2. The activation gate surfaces an error message identifying `story-b` as missing its contract
3. `momentum-tools sprint activate` is NOT called
4. The developer is informed of the specific missing contract
5. Planning halts until the missing contract is remedied

## Scenario B: Missing coverage-plan.md

Given all 3 stories have contracts in specs/

But `coverage-plan.md` does NOT exist at `.momentum/sprints/{sprint-slug}/coverage-plan.md`

When Step 8 activation gate check executes

Then:
1. The gate detects missing coverage-plan.md
2. An error message surfaces identifying the missing coverage plan
3. `momentum-tools sprint activate` is NOT called

## Pass Criteria

- Activation gate checks both: (a) contract file per story, (b) coverage-plan.md
- Gate blocks activation when either is missing
- Error message names the specific missing artifact
- `momentum-tools sprint activate` never called when gate fails

## Fail Criteria

- `momentum-tools sprint activate` called despite missing contracts
- `momentum-tools sprint activate` called despite missing coverage-plan.md
- Gate fails silently without surfacing error
- Gate only checks one of the two required artifacts
