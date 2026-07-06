# Eval: Exactly one post-sprint surface is produced for a completed sprint

**Skill under test:** `momentum:retro`
**Workflow:** `skills/momentum/skills/retro/workflow.md`

## Scenario

**Given:** Sprint `sprint-2026-07-01` has completed its build phase (conduct produced
`.momentum/handoffs/sprint-2026-07-01-endgate-report.html` and the sprint was approved
and merged). The retrospective is now running.

**When:** The retrospective completes Phase 4 and 4.5 and produces post-sprint output.

**Then:**

1. Exactly **one** human-facing HTML decision surface exists for this sprint's post-sprint
   review: `sprint-2026-07-01-endgate-report.html`.
2. No second or parallel HTML review surface is created (e.g., no `retro-review.html`,
   no `process-gate.html`, no `sprint-2026-07-01-retro.html`).
3. `retro-transcript-audit.md` exists as a flat findings record — it is a machine/depth-on-demand
   document, not a human decision surface.
4. The retro workflow explicitly states the single-surface invariant: the endgate HTML is
   extended in place; no new parallel decision surface is created.

## Pass Criteria

- Phase 4.5 in the retro workflow writes to the existing endgate HTML path
  (`.momentum/handoffs/{{sprint_slug}}-endgate-report.html`), not to a new file
- The workflow contains an explicit statement of the single-surface invariant
- `retro-transcript-audit.md` is referenced as a depth-on-demand backing document
- A count of HTML decision surfaces produced = 1

## Fail Criteria

- Phase 4.5 creates a new HTML file at a different path for the process findings
- The workflow is silent about whether a second HTML file is acceptable
- Both `endgate-report.html` and a separate `retro-*.html` file are present and treated
  as co-equal review surfaces for the same sprint

## Verification Note

Verified by inspecting the retro workflow Phase 4.5 action: the write target must be
`.momentum/handoffs/{{sprint_slug}}-endgate-report.html` (the same path conduct wrote to).
A `<critical>` or `<note>` in the workflow must assert the single-surface invariant.
Inspection of workflow instructions is sufficient; a live run is not required.
