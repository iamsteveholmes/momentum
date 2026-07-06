# Eval: Anti-rubber-stamp sign-off covers both results and process sections

**Skill under test:** `momentum:conductor` + `momentum:retro` (fused post-sprint gate)
**Renderer spec:** `skills/momentum/skills/conductor/references/endgate-report-renderer.md`

## Scenario

**Given:** A completed sprint's post-sprint surface (the extended `{{sprint_slug}}-endgate-report.html`)
contains:
- 1 force-close-or-investigate decision card for an incomplete story
- 3 surfaced process findings in the Process review section (1 Stop, 1 Change, 1 Keep)

**When:** The developer attempts to record approval without responding to all items.

**Then:**

1. Approval is blocked while the force-close/investigate card has not been acknowledged with
   an option selected (A or B).
2. Approval is blocked while any of the 3 surfaced process findings has not been given a
   per-decision response with a written one-line reason (a non-empty textarea).
3. A developer who (a) acknowledges the results card and picks A or B, AND (b) enters a written
   reason for each of the 3 process findings, can then submit approval.
4. A blanket click on "approve" without per-item responses does NOT enable the approve button.
5. Exactly one approve control governs both sections — not one per section.

## Pass Criteria

- The paint() gate checks: (a) all results decision cards acknowledged + option selected;
  AND (b) all process findings have non-empty written reasons
- A written reason for each process finding is required (not just a checkbox)
- Acknowledging only the results section does not enable approve
- Answering only the process section does not enable approve
- One approve control covers both sections

## Fail Criteria

- The surface can be approved with results cards answered but process findings unanswered
- Process findings can be signed off with a checkbox alone (no written reason required)
- Two separate approve controls allow each section to be signed off independently
- The gate is satisfied by answering only one section

## Verification Note

Verified by inspecting the renderer spec §6 paint() function (extended version):
- The function must check BOTH `allDecisionsAck` / `allDecisionsPicked` for results cards
  AND `allProcessResponded` (non-empty written reason per process finding)
- The `ok` condition must require all three checks to pass
- The spec must assert exactly one gate control per document

This eval is verified by inspection of the renderer spec — a live run is not required.
