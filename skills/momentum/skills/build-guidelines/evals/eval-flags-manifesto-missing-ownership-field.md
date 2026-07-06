# Eval: Missing ownership field surfaces a signal, never a silent guess

**Eval ID:** build-guidelines-flags-missing-ownership
**Stakes:** correctness — a missing-field signal is required; silent pass leads to guessed patterns

**Given** a manifesto that omits the `## File Ownership` section entirely (or has an empty `file_ownership: []` list),

**When** build-guidelines Phase 1 (Discover) scans and validates that manifesto,

**Then** the manifesto is marked `valid: false` in `{{manifest_matrix}}` with an explicit reason: `"missing or empty ## File Ownership field — resolver patterns cannot be determined"`. It is surfaced in the Discover output under "Invalid manifests (skipped)" with that reason. Phase 3 does not attempt to build this manifest — it is skipped with the missing-field error, not processed with a guessed `permissions_scope` inferred from prose.

## Verification approach

Read build-guidelines `workflow.md` Phase 1 Discover action. Confirm:

1. The scan loop includes a check for `## File Ownership` section presence AND non-empty `file_ownership` list.
2. A manifesto missing that section (or with empty list) is marked `valid: false` with a descriptive reason that names the missing field.
3. The Discover output template shows invalid manifests with reason — including the ownership-field case.
4. Phase 3 skips or halts on this manifest rather than falling through to prose-based inference.

## Pass criteria

A manifesto missing `## File Ownership` produces an explicit "missing or empty ## File Ownership field — resolver patterns cannot be determined" signal in the Discover phase — the manifest is flagged invalid, not silently processed.

## Fail criteria

A manifesto missing `## File Ownership` passes Phase 1 validation silently, and Phase 3 infers a `permissions_scope` from `## Project Stack` prose or "broad-match defaults" — producing a guessed patterns set with no missing-field signal.
