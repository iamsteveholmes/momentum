# Eval: Triage Delegates to Executors — Never Writes Story Files Directly

## Purpose

Verify that `momentum:triage` delegates ARTIFACT items to `momentum:intake` and never
writes story stub files or stories/index.json entries directly.

## Scenario

A developer invokes `/momentum:triage` with two observations, both classified as ARTIFACT:

1. "Add a `--verbose` flag to the sprint-status command"
2. "Intake should support batch mode for multiple items"

The developer approves both in the batch approval step.

## Expected Behaviors

### B1: Delegation to momentum:intake

For each approved ARTIFACT item, triage spawns `momentum:intake` as a subagent. It does
NOT use Write, Edit, or direct calls to momentum-tools story-add. The intake skill handles
stub file creation and index entry writing.

### B2: Enriched Context Passed to intake

Each intake spawn receives:
- title (derived from item text)
- description (item text expanded)
- feature_slug (from enrichment step)
- story_type (from enrichment step)
- epic_slug (from enrichment step)
- priority (from enrichment step)
- source: "triage — conversation" (or similar source label)

### B3: No Direct File Mutations

The triage skill itself makes zero Write or Edit calls to:
- `_bmad-output/implementation-artifacts/stories/*.md`
- `_bmad-output/implementation-artifacts/stories/index.json`
- Any planning artifact file (prd.md, architecture.md, epics.md)

### B4: Parallel Spawns When Multiple Items

When two or more ARTIFACT items are approved, intake spawns are launched in parallel,
not sequentially. (Exception: DECISION items are always sequential because momentum:decision
is interactive.)

### B5: Summary Reports intake Results

After all intake spawns complete, the summary step reports:
- Each stub slug and path returned by intake
- No "failed to create story" errors (assuming normal conditions)

## Pass Criteria

B1–B5 must all be satisfied. Direct file writes to story files is an automatic failure.
