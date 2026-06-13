---
title: Conductor staging must see new files, and the ledger append must be shell-safe
story_key: conduct-conductor-staging-and-ledger-append-safety
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
priority: high
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/build-ledger.md
---

# Conductor staging must see new files, and the ledger append must be shell-safe

## Story

As the maintainer of the conduct build engine,
I want the Conductor's commit step to stage newly-created files and its ledger append to be safe against arbitrary prose,
so that green-field stories (the common case) cannot silently lose new files at commit, and the build journal cannot be corrupted by an apostrophe or a crash mid-write.

## Why this exists (two stakes-class escalations from sprint-2026-06-10, end-gate D1 + D2)

These were raised by the build's own stakes-class escalation path and held for the developer; both confirmed real and accepted as fix-next.

**D1 (critical, irreversible-destructive) — `git add -u` is blind to untracked files.** Now that dev agents never commit (DEC-035), the Conductor's `git add -u` is the only staging path — but it ignores brand-new files. A green-field story whose deliverable is a new file (a new skill, reference, or test — the most common shape) would have that file silently dropped at commit and destroyed at worktree cleanup. **Empirically hit during sprint-2026-06-10:** the Conductor compensated by staging new eval/reference files by explicit path. Sites: `conductor/workflow.md:581, 1739, 2105, 2479`.

**D2 (security-auth-isolation) — the ledger append uses a shell-unsafe `printf`.** `build-ledger.md:23` prescribes `printf '%s\n' '{…json…}' >> ledger` with the row JSON in shell single-quotes. Row fields carry free prose (finding summaries, dismissal rationales, developer change-request text); any apostrophe terminates the quoting early (corruption + injection-shaped hazard, since summaries can echo reviewed repo content), and an embedded newline splits one logical row across lines. The rehydration parser is told only to "parse each line as JSON" with no rule for the partial final line a crash-mid-append leaves — the exact moment the journal must survive. (sprint-2026-06-10 sidestepped this by writing the ledger via a JSON serializer — the safe pattern to codify.)

## Acceptance Criteria

1. The four `git add -u` staging sites in `conductor/workflow.md` enumerate the change set with `git status --porcelain` (which includes untracked files), stage in-scope paths explicitly, and discard out-of-scope **untracked** files with `git clean -f` (tracked ones with `git checkout -- P`). The write-scope guard operates over the enumerated set, not over `add -u`'s tracked-only view.
2. A green-field story whose output is a new file has that file staged and committed by the Conductor (verified by an eval or a walked scenario).
3. `build-ledger.md` mandates single-quote-safe row construction — JSON-escape and newline-flatten free-prose fields before interpolation, or compose via a quoted heredoc / serializer — so an apostrophe or newline in any field cannot corrupt the row or the JSONL contract.
4. The step 2.0 rehydration rule handles an unparseable line (including the partial final line from a crash-mid-append): skip it, log a `conductor-warning` ledger row, and continue rehydration — never abort.

## Tasks / Subtasks
- [ ] Replace `git add -u` with porcelain-enumerated explicit staging + `git clean -f` for untracked discards at all four sites; route the write-scope guard over the enumerated set. (AC 1, 2)
- [ ] Codify shell-safe ledger append (escape/flatten or serializer) in build-ledger.md and the standing-rule append instruction. (AC 3)
- [ ] Add the malformed/partial-line skip-and-warn rule to step 2.0 rehydration. (AC 4)

## Dev Notes
- Both are pre-existing conductor surfaces that this sprint's no-commit change (D1) and new-ledger feature (D2) made newly consequential; the dev-commit-authority story (AC7) was correctly forbidden from touching conductor staging, which is why they remained open.
- Recommend doing this as the first conduct quick-fix after sprint-2026-06-10 (developer's stated disposition).

## Dev Agent Record
