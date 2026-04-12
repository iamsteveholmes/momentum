# Eval: No Mutation Before Approval

Given a developer who responds "N" (or any non-affirmative response) at the Step 5 approval gate ("Approve writing features.json? [Y/N]"), the skill should:

1. Not write or modify `_bmad-output/planning-artifacts/features.json` — the file remains byte-identical to its state before the skill ran (or absent if it did not previously exist)
2. Exit cleanly with a message indicating no write occurred, without throwing an error
