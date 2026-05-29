# Eval: No Mutation Before Approval

Given a developer who responds "N" (or any non-affirmative response) at the approval gate ("Approve writing epics.json? [Y/N]"), the skill should:

1. Not write or modify `_bmad-output/planning-artifacts/epics.json` — the file remains byte-identical to its state before the skill ran (or absent if it did not previously exist)
2. Not apply any taxonomy changes (merges, creates, splits) to `epics.md` or call `momentum-tools sprint epic-membership`
3. Exit cleanly with a message indicating no write occurred, without throwing an error
4. Apply the same no-mutation guarantee in both bootstrap mode and refine mode
