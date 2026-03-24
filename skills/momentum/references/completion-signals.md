# Completion Signals Reference

This document defines the canonical formats for completion signals, productive waiting, subagent result synthesis, and review dispatch summaries. Impetus workflow.md references this document — the patterns here are authoritative.

---

## 1. Completion Signal Format

Every story cycle, workflow, or major workflow step completion delivers a signal with three required components.

### Required Components

1. **Status line** — `✓` prefix, what completed, one-line summary
2. **File list** — every file produced or modified, with path and brief description, `·` prefix per line
3. **Ownership return + forward prompt** — explicit handoff ("This is yours to review and adjust") followed by "What's next?"

### Canonical Template

```
✓  [what completed] — [one-line summary]

What was produced:
  · [path/to/file1] — [brief description]
  · [path/to/file2] — [brief description]

This is yours to review and adjust. What's next?
```

### Canonical Example

```
✓  Story 4.2 complete — session journal implementation done

What was produced:
  · src/ledger.ts — LedgerEntry type + CRUD operations
  · src/ledger.test.ts — 12 passing acceptance tests
  · .claude/rules/ledger-patterns.md — upstream fix from code review

This is yours to review and adjust. What's next?
```

### Edge Cases

**Workflow with no file output** (e.g., configuration changes, validation-only steps):
```
✓  Configuration validation complete — all hooks verified active

No files were modified. The validation confirmed existing configuration is correct.

This is yours. What's next?
```

**Partial completion** (interrupted before finish):
```
→  Story 3.1 partially complete — paused at task 4 of 7

What was produced so far:
  · src/parser.ts — token extraction logic (complete)
  · src/parser.test.ts — 6 of 12 tests written

Remaining: tasks 5-7 (transformer, output formatter, integration tests).
Pick up where we left off, or adjust the plan?
```

**Multi-artifact completion** (many files):
```
✓  Epic 2 stories 2.1–2.4 complete — Impetus UX layer implemented

What was produced:
  · skills/momentum/workflow.md — full Impetus workflow with all UX patterns
  · skills/momentum/references/completion-signals.md — signal format reference
  · skills/momentum/references/progress-indicators.md — visual progress reference
  · skills/momentum/evals/eval-*.md — 12 behavioral evals across 4 stories
  ... and 3 more files

This is yours to review and adjust. Want the full file list, or shall we move on?
```

When more than ~6 files are produced, show the most important ones and offer to expand.

### Progress Indicator Integration

At final completion, the progress indicator shows all steps built with no upcoming items:
```
✓ Built: scaffold, types, CRUD, tests, rules
```

No `◦ Next:` line appears — its absence signals finality.

At intermediate completion (workflow step done, more steps remain):
```
✓ Built: scaffold, types
→ Now: CRUD operations
◦ Next: tests, rules
```

---

## 2. Productive Waiting

When Impetus dispatches a background subagent, silence is a failure mode. The developer must always have something to engage with.

### Substantive Discussion Pattern (Preferred)

After dispatching a background agent with `run_in_background: true`, Impetus delivers an implementation summary or offers same-topic discussion:

```
I've dispatched the review. While it runs, here's a summary of what was built:

  · The ledger module implements create, read, update, delete operations
  · We chose append-only writes to match the architecture's immutability requirement
  · All 12 acceptance tests pass — they cover the happy path and 3 edge cases

The review is checking against the story's ACs. Anything you want to revisit before results come in?
```

### Acknowledged Pause Pattern (Fallback)

When no substantive discussion is available, explicitly acknowledge the wait:

```
The review is running — I'll have results shortly.
```

Or with slightly more context:

```
The review is checking the implementation against story 4.2's acceptance criteria. I'll have findings in a moment.
```

### "Same Topic" Definition

During productive waiting, all discussion must relate to:
- The work just completed
- Acceptance criteria being verified
- Architectural context relevant to the current work
- What comes next in the workflow

Never: unrelated subjects, general tips, or tangential information.

### Anti-Patterns

- **Dead air** — no response while background task runs
- **Context switching** — pivoting to unrelated subjects during the wait
- **Filler** — generic commentary unrelated to the work ("While we wait, did you know...")

---

## 3. Subagent Result Synthesis

When a subagent returns results, Impetus synthesizes them into its own voice. The hub-and-spoke contract means the developer never knows which subagent ran.

### Subagent Return Contract

All subagents return structured JSON:

```json
{
  "status": "complete | needs_input | blocked",
  "result": {
    "findings": [...],
    "summary": "..."
  },
  "question": null | "string — surfaced to developer if non-null",
  "confidence": "high | medium | low"
}
```

Impetus synthesizes from this contract. Free-form prose from subagents is not presented directly.

### Severity Indicators

- `!` — Critical or blocking finding. Requires attention before proceeding.
- `·` — Minor or informational finding. Note for awareness, not blocking.

### Synthesis Voice Rules

**Always say:**
- "The review found..."
- "I found..."
- "One issue to address..."

**Never say:**
- "The code reviewer said..."
- "The VFL agent found..."
- "momentum-avfl reported..."
- Any subagent name, tool name, or agent identity

### Confidence-Directed Synthesis

The subagent's `confidence` field directs how Impetus presents findings:

- **High** (derived from upstream spec) — synthesize directly, no hedging
  - "This comes directly from the architecture" / "The PRD specifies this explicitly"
- **Medium** (inferred from patterns) — flag with verification nudge
  - "Inferred from the architecture patterns — worth verifying" / "This follows from the design, though it's not stated explicitly"
- **Low** (needs developer input) — surface as a question, not an assertion
  - "I'm not sure about this one — how do you want to handle it?" / "This needs your input — the specs don't cover it clearly"

Vary the natural language across findings — avoid robotic repetition of the same phrasing.

### Flywheel Integration

When a finding has `!` severity (critical):

1. **If `momentum-upstream-fix` skill is available:** offer flywheel trace
   - "This looks like it could be traced upstream. Want me to run a flywheel trace?"
2. **If `momentum-upstream-fix` is NOT available:** include deferral note
   - Weave naturally: "...noted for flywheel processing when Epic 6 ships"
   - Or as a parenthetical: "(flywheel processing deferred — Epic 6)"

Minor findings (`·`) never trigger flywheel offers.

### Hub-and-Spoke Contract

The developer interacts only with Impetus. Subagent identity is an implementation detail:

- No subagent names in any output
- No "I asked the reviewer to..." or "The analysis tool reported..."
- Results presented as Impetus's own synthesis
- If the developer asks "who found this?" — "I found it during the review" (not "the code-reviewer subagent")

---

## 4. Review Dispatch Summary

When dispatching a review subagent, Impetus provides an implementation summary at the moment of dispatch — the developer reads it during the wait, not after.

### Summary Contents

1. **Files created/modified** — with brief description of each
2. **Key decisions made** — architectural choices, trade-offs, deviations from plan
3. **AC mapping** — how the work maps to acceptance criteria
4. **Open questions** — anything unresolved or needing developer input

### Canonical Template

```
I've kicked off the review. Here's what was built:

  · [file1] — [description]
  · [file2] — [description]

Key decisions:
  · [decision 1 — why this approach]
  · [decision 2 — trade-off made]

This covers AC1 through AC4. AC5 is partially addressed — [detail].

[Any open questions or deviations to flag]

I'll have review findings shortly. Anything you want to flag before they come in?
```

### Timing

The summary is delivered at the moment the review subagent is dispatched. It transitions naturally into the productive waiting pattern — the summary IS the substantive discussion during the wait.

---

## 5. Tiered Review Depth

When presenting findings, Impetus never dumps the full list unprompted. Instead, it leads with a micro-summary and offers depth tiers.

### Micro-Summary

1-3 sentences covering:
- How many findings total (critical vs. minor)
- Key decisions or outcomes
- Overall assessment

### Tier Offer

After the micro-summary, offer three tiers as a natural question:

```
The review found 2 items worth noting — one needs attention, one is minor.
Want me to walk through them, or are you good to continue?
```

The three tiers (expressed naturally, not as a coded menu):
- **Quick scan** — the micro-summary is sufficient, move on
- **Full review** — "Walk me through them" / "Show me the details"
- **Trust & continue** — "Looks good, let's keep going"

### Presentation When Full Review Selected

Expand findings with severity indicators and confidence:

```
! [critical finding] — [description with confidence language]
  [recommendation]

· [minor finding] — [description with confidence language]
```
