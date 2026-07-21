# Eval: End-gate report open reuses an existing viewer surface instead of churning panes

**Surface under test:** The Conductor's end-gate report open action — the initial Phase 5 open, the 5.RC.5 redispatch re-render open, and the corresponding open procedure in `references/endgate-report-renderer.md` (§8 and the §13 fused re-render path).

**Standard:** Verified cmux behavior — `cmux browser new` ALWAYS returns `placement=split` and creates a new structural pane; it never reuses an existing viewer surface. Project memory: `reference_cmux_browser_new_always_splits`.

## Scenario

**Given:** Two cases, both checked:
- (a) A viewer browser surface already exists in the workspace (e.g. showing a prior plan-gate report, or an earlier end-gate render that this open supersedes).
- (b) No viewer browser surface exists yet this session.

**When:** The Conductor opens (or re-opens) the end-gate report.

**Then:**

1. **Query before acting.** The instruction directs the Conductor to check for an existing viewer surface first (e.g. `cmux list-panes` / `cmux list-pane-surfaces`) before deciding how to open the report.
2. **Case (a) — reuse via `goto`.** When a viewer surface already exists, the Conductor navigates it in place with `cmux browser <surface> goto <url>` and does NOT run `cmux browser new`.
3. **Case (b) — `browser new` only when absent.** When no viewer surface exists yet, the Conductor uses `cmux browser new ... --focus false` to create the first one.
4. **No stale reuse claim remains.** Neither `workflow.md` nor `endgate-report-renderer.md` (including its §8 open procedure, the §140-area viewer-open reference, and the §13 fused re-render step) asserts that `cmux browser new` "adds a tab" or "does not create a new structural pane." The corrected text instead states that `cmux browser new` always creates a new structural pane, and that reuse requires `goto`.

## Pass Criteria

- Both open sites in `workflow.md` (initial Phase 5 open, 5.RC.5 redispatch open) and the renderer's open procedure describe the query-then-branch pattern: reuse via `goto` when a surface exists, `browser new` only when none exists.
- A before/after check of viewer-pane count shows no growth when a viewer surface already existed.
- No text anywhere in the two touched files claims `cmux browser new` reuses, tabs into, or avoids creating a new structural pane.

## Fail Criteria

- Any open site issues `cmux browser new` unconditionally, without first checking for an existing viewer surface.
- Any remaining sentence in either file asserts that `cmux browser new` adds a tab to an existing pane or does not create a new structural pane.
- A second viewer pane appears when one already existed before the open.

## Verification Note

Verified by inspection: read the initial Phase 5 open action, the 5.RC.5 redispatch re-render open action, and `endgate-report-renderer.md` §8 (file output / open procedure) and §13 (fused re-render path, step 6). Confirm the query-then-branch structure is present at all sites and that the stale "reuse"/"tab" claims have been fully removed, not just partially edited. A simulated run with a pre-existing viewer surface can cross-check that no second pane is created.
