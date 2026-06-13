# Eval: No dev variant instructs a commit

## Scenario

Given the full set of dev agent variants (`agents/dev.md`, `agents/dev-build.md`, `agents/dev-frontend.md`, `agents/dev-skills.md`), the dev workflow (`skills/dev/workflow.md`), and the directed-fix contract (`references/directed-fix-invocation-contract.md`), grep for all occurrences of "commit" across these files.

## Expected behavior

Every remaining occurrence of the word "commit" in these files must either:
1. Attribute commit authority to the Conductor (e.g., "the Conductor stages and commits")
2. Describe the no-edit/no-commit guarantee for escalated/dismissed/triaged-out dispositions
3. Describe what does NOT happen (e.g., "no fix commit is produced" in escalation context)
4. Reference conventional commit message format as documentation for the Conductor's benefit (not as an instruction for the dev agent to author commits)

No occurrence should instruct the dev agent (in any mode or variant) to run `git add`, `git commit`, or produce a commit.
