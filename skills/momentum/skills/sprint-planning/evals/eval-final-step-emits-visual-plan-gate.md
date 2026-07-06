# Eval: Final Step Emits Visual Plan Gate

**ID:** eval-final-step-emits-visual-plan-gate
**Change-type:** skill-instruction
**Phase:** developer review (Step 7)

## Scenario

Given a sprint plan that has completed Steps 1–6 with:
- 4 stories selected and approved: `story-a` (Wave 1, HIGH stakes), `story-b` (Wave 1, low stakes),
  `story-c` (Wave 2, depends on `story-a`, medium stakes), `story-d` (Wave 2, depends on `story-b`, low stakes)
- Verification contracts authored for all 4 stories in `.momentum/sprints/sprint-2026-07-06/specs/`
- AVFL result: CLEAN

When Step 7 (developer review of complete sprint plan) runs

Then:
1. A self-contained HTML file is written to `.momentum/handoffs/sprint-2026-07-06-plan-gate.html`
   before any ask/prompt is presented to the developer
2. The file is opened in the viewer via `cmux browser new … --focus false`
   (adds a tab to the existing viewer pane; does NOT create a new structural split)
3. The developer is presented with a sign-off prompt that references the plan gate, NOT a flat-text
   concatenation of story specs or a bare A/M/R text block
4. The HTML file is self-contained: no external CSS or JS links, no `<link rel="stylesheet">`, no `<script src=`

## Pass Criteria

- `.momentum/handoffs/sprint-2026-07-06-plan-gate.html` exists after Step 7 runs
- `cmux browser new` is called with the `file://` URL of the plan gate
- Developer prompt refers to the gate (not a raw plan dump)
- HTML file opens standalone in a browser without network requests

## Fail Criteria

- No HTML file is produced; developer sees only prose or a markdown-formatted plan
- HTML file is produced but NOT opened in the viewer
- A new structural pane is created instead of a tab in the existing viewer pane
- The HTML file has external `<link>` or `<script src>` dependencies
