# Eval: End-gate report open never steals developer focus

**Surface under test:** The Conductor's end-gate report open action — both the initial Phase 5 open (`workflow.md`, Phase 5 "Open the report in the cmux viewer pane" action) and the request-changes redispatch re-render open (`workflow.md`, step 5.RC.5).

**Standard:** decision-grade-presentation rule §5.1 (the end-gate is a visual HTML companion surface opened in the viewer pane "without hijacking focus"); DEC-036 D5.

## Scenario

**Given:** The Conductor has finished building (or re-rendering) the end-gate report HTML and reaches the action that opens it in the cmux viewer pane. This is checked at both sites: the initial Phase 5 open, and the 5.RC.5 redispatch re-render open.

**When:** The Conductor issues the cmux command(s) to make the report visible in the viewer pane.

**Then:**

1. **No `--focus true` anywhere.** The command issued to open or update the viewer surface never passes `--focus true`.
2. **`cmux browser new` is always paired with `--focus false`.** Whenever the branch that creates a new viewer surface (`cmux browser new`) is taken, it carries `--focus false`.
3. **The instruction states this as a hard requirement, not a hint.** Reading the instruction at both sites, `--focus false` is framed as a MUST with its rationale ("keeps the developer in context") stated explicitly — not as a bare `Run:` command line and not as an easily-skipped parenthetical aside.
4. **Holds at both sites identically.** The same MUST framing and rationale appear at the initial Phase 5 open and at the 5.RC.5 redispatch re-render open — not just one of them.

## Pass Criteria

- No `--focus true` appears in the issued command or in the instruction text at either open site.
- `--focus false` is present whenever `cmux browser new` is used, and the instruction frames it as a non-negotiable MUST with its rationale stated, at BOTH the initial open and the redispatch re-render open.

## Fail Criteria

- `--focus true` is used (or permitted) at either open site.
- `--focus false` appears only as a bare command-line flag or a passing parenthetical remark with no explicit MUST framing or rationale, at either site.
- The MUST framing is present at one site but missing or weaker at the other.

## Verification Note

Verified by inspection: read the Phase 5 initial-open action and the 5.RC.5 re-render-open action in `skills/momentum/skills/conductor/workflow.md`, and the open procedure in `skills/momentum/skills/conductor/references/endgate-report-renderer.md` §8. Confirm the MUST framing and rationale are present at every site, and no `--focus true` is used or implied anywhere. A simulated run (a subagent walking through the Phase 5 steps) may be used to cross-check that the behavior described is what actually gets executed.
