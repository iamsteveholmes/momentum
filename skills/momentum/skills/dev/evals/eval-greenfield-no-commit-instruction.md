# Eval: Green-field dev produces no commit

## Scenario

Given the dev agent definition (`agents/dev.md`) and the dev workflow (`skills/dev/workflow.md`) as loaded context, and a green-field story input (no `directed_fix` payload), the agent should:

1. Implement the story by delegating to bmad-dev-story
2. Leave all changes uncommitted in the worktree (no `git add`, no `git commit`)
3. Emit the standard `AGENT_OUTPUT_START` / `AGENT_OUTPUT_END` structured output with `status: "complete"`, `story_key`, `files_changed`, `part_a_self_check`, `test_results`, and `cross_artifact_notes`
4. NOT contain any instruction to commit, stage, or run `git add`/`git commit` in its green-field process steps

## Expected behavior

- The agent definition contains no green-field commit step (no "### 4 (Green-field). Commit Changes" or equivalent)
- The "What NOT to Do" section includes a prohibition on committing in either mode
- The structured output schema is unchanged (field names, AGENT_OUTPUT framing, disposition vocabulary)
- The workflow contains no commit action in the green-field path (Steps 1-3)
