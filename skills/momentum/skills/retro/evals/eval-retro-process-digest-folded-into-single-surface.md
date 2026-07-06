# Eval: Retro process digest is folded into the fused gate, not a separate surface

**Skill under test:** `momentum:retro` (Phases 4–4.5)
**Workflow:** `skills/momentum/skills/retro/workflow.md`

## Scenario

**Given:** Sprint `sprint-2026-07-01` has completed its build phase (conduct produced
`.momentum/handoffs/sprint-2026-07-01-endgate-report.html`). The retro's audit Workflow
(Phase 4) returns 9 findings: 4 actionable process findings (2 Stop, 1 Change, 1 Keep)
and 5 routine observations. `retro-transcript-audit.md` is written by the audit Workflow.

**When:** The retro completes Phase 4 and produces its post-sprint output.

**Then:**

1. The 4 process findings are folded into **`sprint-2026-07-01-endgate-report.html`** —
   the same file conduct produced — not into a new separate HTML document.
2. A "Process review (Keep / Stop / Change)" section appears **beneath** the results
   sections in that file.
3. At most 7 findings are surfaced; here 4 (all actionable) with the routine 5 collapsed
   to a single count line ("5 routine observations not surfaced").
4. Each of the 4 surfaced findings carries **what / why-it-matters / evidence** inline.
5. `retro-transcript-audit.md` exists as the depth-on-demand flat record; the fused gate
   **links to it** — it does not paste its contents inline.
6. No separate review HTML document is produced for this sprint's process findings.

## Pass Criteria

- Process findings appear in `{{sprint_slug}}-endgate-report.html`, not in a new file
- The Process review section is positioned beneath the results sections
- ≤7 findings surfaced; routine findings collapsed to a count line
- Each surfaced finding carries what/why/evidence inline
- `retro-transcript-audit.md` is linked, not inlined

## Fail Criteria

- A separate HTML file is emitted alongside the endgate HTML for process findings
- The Process review section appears before the results sections
- More than 7 findings surfaced without collapsing routines
- A surfaced finding is missing what, why, or evidence
- Full contents of `retro-transcript-audit.md` are pasted into the HTML

## Verification Note

Verified by inspecting: (1) the retro workflow — Phase 4 must bind `{{process_findings}}`
and Phase 4.5 must write to the existing endgate HTML path; (2) the renderer spec §3 spine —
the Process review section must follow the results sections; (3) the fused gate HTML — a link
to `retro-transcript-audit.md` must exist rather than its full text. Inspection of workflow
instructions is sufficient; a live run is not required.
