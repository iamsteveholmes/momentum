# Eval: Fix-mode routine fix produces no commit

## Scenario

Given the dev agent definition (`agents/dev.md`) and the dev workflow (`skills/dev/workflow.md`) as loaded context, and a fix-mode input with a `directed_fix` payload containing a routine, legitimate finding, the agent should:

1. Apply the fix by editing the affected file(s)
2. Return `disposition: fixed` with `files_changed` populated
3. NOT commit the change -- the Conductor stages and commits after the fixer returns
4. The `files_changed` field describes files edited in the working tree, not files committed

## Expected behavior

- The routine fix path in both the agent definition and workflow edits files but does not instruct `git add` or `git commit`
- The `files_changed` annotation references files edited (not "files edited and committed")
- The fix-mode commit discipline constraint is replaced with a statement that the Conductor commits
- The stakes-class no-edit guarantee (zero edits for escalated/dismissed/triaged-out) is preserved unchanged in meaning
- The non-empty dismissal-rationale rule is preserved unchanged
