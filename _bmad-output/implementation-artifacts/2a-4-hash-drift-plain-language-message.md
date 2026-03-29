# Story 2a.4: Hash Drift Plain-Language Message

Status: in-progress

## Story

As a developer,
I want the hash drift warning to tell me what actually happened in plain English,
so that I don't need to know what "hash drift" or "component groups" mean.

## Acceptance Criteria

1. **Given** a hash mismatch is detected for installed quality rules
   **When** Impetus surfaces the condition
   **Then** the message is: `! Your quality rules were edited after Momentum set them up.`
   **And** the options are: `[R] Restore the originals · [K] Keep your edits`
   **And** no reference to "hash drift", "component group", "stored hash", or step numbers appears

## Tasks / Subtasks

- [x] Task 1: Replace the hash drift warning message in `skills/momentum/workflow.md` Step 10 (AC: 1)
  - [x] 1.1: Locate Step 10 in workflow.md — the `<step n="10" goal="Hash drift detection...">` block
  - [x] 1.2: Replace the current `<output>` block with the exact AC-mandated message: `! Your quality rules were edited after Momentum set them up.` followed by `[R] Restore the originals · [K] Keep your edits`
  - [x] 1.3: Remove all references to internal terms: "hash mismatch", "{{group}} files", "component group", step numbers from the user-facing output
  - [x] 1.4: Preserve the existing `<ask>` and response handling logic — only the output text changes

## Dev Notes

### What This Story Changes

This is a targeted message copy change in a single workflow step. The logic (hash computation, compare, re-apply or keep) is unchanged. Only the text surfaced to the developer changes.

**Current message (workflow.md Step 10, lines ~608–616):**
```
! Rules modified since Momentum installed them.
  {{group}} files have been changed (hash mismatch).

Re-apply from the Momentum package, or keep your edits?
[R] Re-apply · [K] Keep modified
```

**Required replacement message (exact):**
```
! Your quality rules were edited after Momentum set them up.

[R] Restore the originals · [K] Keep your edits
```

### What Must Not Change

- The `<check if="computed hash == stored hash ...">` branch (pass-through to step 7) — untouched
- The `<check if="developer chooses [R]">` re-apply logic — untouched
- The `<check if="developer chooses [K]">` keep-edits logic, including the note that the warning will recur — untouched
- The `<ask>` prompt — the only valid responses remain `[R]` and `[K]`

### Architecture Context

**Hash drift detection mechanism** (`architecture.md` §Decision 5c, lines ~570–577):
- Impetus reads `~/.claude/momentum/global-installed.json` at session start
- Per-component git blob SHA (`git hash-object`) stored at install/upgrade time
- On mismatch: surfaced as a warning, **not a blocker** — developer decides
- "surfaced as a warning, not a blocker" must remain true; this story does not change the flow gate behavior

**State file schema** (`architecture.md` lines ~543–552):
```json
{
  "components": {
    "rules": { "version": "1.0.0", "hash": "<git-blob-sha>" }
  }
}
```
The `hash` field in `global-installed.json.components.{{group}}.hash` is the stored value compared against the computed `git hash-object` result. This story does not touch this schema.

**Step 10 location in workflow**: `skills/momentum/workflow.md`, the `<step n="10">` block. The step runs after all version groups are confirmed current (after step 9 upgrade path) and before step 7 session orientation.

### File to Modify

- `skills/momentum/workflow.md` — single file, single change, in the Step 10 `<output>` block

### Project Structure Notes

- `skills/momentum/workflow.md` is the sole implementation file. No config files, no new files.
- No new variables introduced. No schema changes.
- The `{{group}}` template variable was used in the old message; it must **not** appear in the new message (AC explicitly forbids internal terminology).

### Testing Standard

Per `docs/process/acceptance-testing-standard.md`: verify AC via manual inspection of the modified `<output>` block. Confirm:
1. The phrase `! Your quality rules were edited after Momentum set them up.` appears verbatim
2. The phrase `[R] Restore the originals · [K] Keep your edits` appears verbatim
3. None of the forbidden terms appear in the output block: "hash drift", "component group", "stored hash", step numbers, `{{group}}`

### References

- Story 2a.4 ACs: `_bmad-output/planning-artifacts/epics.md` §Story 2a.4
- Current Step 10 implementation: `skills/momentum/workflow.md` lines ~597–631
- Hash drift architecture: `_bmad-output/planning-artifacts/architecture.md` §Decision 5c (~lines 570–577)
- UX-DRs covered by Epic 2a: UX-DR1, UX-DR2, UX-DR6 (plain-language user-facing messages)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
