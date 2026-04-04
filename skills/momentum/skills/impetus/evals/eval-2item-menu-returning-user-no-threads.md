# Eval: 2-Item Menu — Returning User, No Threads

## Story

2a-3: Session-Open Menu Redesign

## Setup

- `momentum_completions = 3` (returning user)
- `journal.jsonl` absent or contains zero open threads
- Momentum fully installed, version matches

## Expected Behavior

1. Session menu renders with exactly 2 items:
   - `/create` — Write a story
   - `/develop` — Build the next story
2. Items 3–6 from the old menu (Review a plan, Run quality validation, Audit spec provenance, Show session threads) do NOT appear
3. Number alias `1` dispatches identically to `/create` → momentum:create-story workflow
4. Number alias `2` dispatches identically to `/develop` → momentum:dev workflow
5. Slash command `/create` dispatches to momentum:create-story workflow
6. Slash command `/develop` dispatches to momentum:dev workflow

## Fail Conditions

- Any of the old items 3–6 appear in the menu
- Number aliases (1, 2) are not recognized
- `/create` dispatches to wrong workflow
- `/develop` dispatches to wrong workflow
- Menu has more than 2 items
- Menu has fewer than 2 items
- Stats write (deferred) blocks or delays menu rendering
