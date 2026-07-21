# Eval: Dependency Warning and AVFL CHECKPOINT_WARNING Are Non-Blocking Notices

## Setup

Two independent sub-scenarios exercised against a `momentum:sprint-planning` session.

### Sub-scenario A: Dependency warning during story selection (Step 2)

The developer selects 3 stories for the sprint. One selected story, `story-c`, has a
`depends_on` entry for `story-x`, and `story-x` is neither in the current selection nor
`status: done` in `stories/index.json`.

### Sub-scenario B: AVFL CHECKPOINT_WARNING during Step 6

The complete sprint plan is submitted to the `momentum:avfl` skill. AVFL returns
`CHECKPOINT_WARNING` with 2 minor findings (no critical/major findings).

## Expected Behavior

### Sub-scenario A

1. The workflow detects the unmet dependency and surfaces it:
   `! Dependency warnings noted (non-blocking — proceeding with current selection): ...`
2. The workflow does **not** present a blocking choice (no "proceed or revise?" prompt).
3. Execution continues immediately to sprint-slug generation and story registration in
   the same step — the developer is not required to respond before Step 2 completes.

### Sub-scenario B

1. The workflow surfaces the findings:
   `! AVFL found issues in the sprint plan (non-blocking — the plan proceeds): ...`
2. The workflow does **not** present a blocking choice (no "address findings now, or
   proceed with warnings noted?" prompt).
3. Execution continues directly to Step 7 (developer review / plan gate) without
   requiring a developer response at Step 6.

## Verification

- Neither sub-scenario produces an `<ask>`-style pause; both produce only an `<output>`
  notice.
- The findings/warning content is still fully surfaced to the developer (the notice is
  informative, not silent) — only the blocking behavior is removed.
- The AVFL `GATE_FAILED` path is unaffected by this change: a separate run where AVFL
  returns `GATE_FAILED` still HALTs and requires the developer to resolve findings before
  Step 7, because that is a genuine blocking defect state, not an advisory warning.
