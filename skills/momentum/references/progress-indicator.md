# Progress Indicator Reference

Canonical format, rules, symbol vocabulary, and journal integration for the Momentum visual progress indicator.

---

## Canonical 3-Line Format

The progress indicator shows workflow position in a compact, collapsible format. At most 3 lines; at boundaries, 2 lines.

```
  ✓  [completed phases · separated]    [value summary — what exists now]
  →  [current phase]                   [why this step matters]
  ◦  [upcoming phases · separated]     [count or summary of what remains]
```

### Examples

Mid-workflow (4 completed, 1 current, 2 upcoming):
```
  ✓  Brief · Research · PRD · UX      vision through interaction patterns done
  →  Architecture                     making implementation decisions
  ◦  Epics · Stories                  2 phases to implementation
```

First step (0 completed, 1 current, 6 upcoming):
```
  →  Brief                                         capturing the core product idea
  ◦  Research · PRD · UX · Arch · Epics · Stories  6 phases ahead
```

Last step (6 completed, 1 current, 0 upcoming):
```
  ✓  Brief · Research · PRD · UX · Arch · Epics  foundation through planned work
  →  Stories                                      breaking the work into deliverables
```

### Workflow Phases (Ordered)

Brief, Research, PRD, UX, Architecture, Epics, Stories — 7 phases total.

---

## Collapse Rules

1. **Completed phases collapse to a single ✓ line.** List phase names separated by ` · `, followed by a value summary phrase describing what has been accumulated (not what tasks were done).
2. **Upcoming phases collapse to a single ◦ line.** List phase names separated by ` · `, followed by a count or summary of what remains.
3. **The current phase always stands alone on the → line** with a one-phrase description of why it matters to the work.
4. **The indicator never grows** with workflow length — it is always 2 or 3 lines regardless of how many phases exist.

---

## Boundary Rules

- **Workflow start** (no completed phases): Omit the ✓ line entirely. Display 2 lines: → current, ◦ upcoming.
- **Workflow end** (no upcoming phases): Omit the ◦ line entirely. Display 2 lines: ✓ completed, → current.
- **Never display** an empty line, a placeholder line ("✓ nothing yet"), or a line for a category that has zero entries.

---

## Symbol Vocabulary

Single source of truth for all Momentum components (Impetus, hooks, subagent output synthesis).

| Symbol | Meaning              | Paired text example                                          |
|--------|----------------------|--------------------------------------------------------------|
| ✓      | completed / passing  | "✓ Built: vision through requirements done"                  |
| →      | current / active     | "→ Now: building interaction patterns"                       |
| ◦      | upcoming / pending   | "◦ Next: 3 phases to implementation"                         |
| !      | warning / attention  | "! This thread appears active in another tab"                |
| ✗      | failed / blocked     | "✗ lint check failed — missing semicolon at auth.ts:42"      |
| ?      | question / decision  | "? Which authentication provider should we use?"             |

### Text-Pairing Rule

Every symbol MUST have adjacent text on the same line conveying the same meaning. A symbol without paired text is a violation. This ensures meaning is recoverable when Unicode symbols do not render correctly.

Violations:
- ✓ appearing alone on a line
- → used as a bullet without descriptive text
- ◦ ◦ ◦ used decoratively
- Any symbol conveying meaning solely through the glyph

---

## Terminal Rendering Constraints

- **80-character width**: The progress indicator must render cleanly without horizontal scrolling at 80 characters.
- **No color dependency**: Output must be understandable without terminal color support.
- **Terminal-safe characters only**: ✓, →, ◦, !, ✗, ? are the complete set. No box-drawing characters, no emoji, no characters requiring specific font support.

---

## Response Architecture Pattern Integration

Every rendered workflow step follows this 4-element structure:

1. **Narrative orientation line** — preceded by or incorporating the progress indicator. Describes where the developer is and what value has accumulated. Always narrative, never numeric.
2. **Substantive content** — the work of the step: questions, decisions, artifacts, context.
3. **Transition signal** — forward-looking: what happens after this step and what value it unlocks.
4. **Explicit user control** — always the final element. Clear choices: A/P/C or contextual equivalent.

### Anti-Patterns

- "Step 3/7", "Step 3 of 7", "Phase 4/7" — **banned**. All orientation is narrative.
- "Great work!", "Well done!" — no generic praise.
- "Continuing...", "Moving on to..." — no mechanical transitions.
- Ellipsis counts ("...3 more steps...") — no special syntax.

---

## On-Demand Position Query

When a developer asks "where am I?", "what's my current position?", "show me my progress", or any equivalent query:

1. Display the progress indicator for the current workflow position (3-line or 2-line at boundary).
2. All standard rules apply: collapse, boundary, text-pairing, terminal-safe.
3. Answer the question directly — show position, do not re-explain the entire workflow.

---

## Journal Integration for Workflow Resumption

When Impetus detects an interrupted workflow (via `.claude/momentum/journal.json`), it reconstructs the progress indicator from journal state.

### Fields Read from Journal Thread Entries

| Field             | Purpose                                          |
|-------------------|--------------------------------------------------|
| `workflow`        | Identifies which workflow was active              |
| `current_step`    | The phase that was in progress when interrupted   |
| `completed_steps` | Ordered list of phases already completed          |
| `context_summary` | Narrative summary for re-orientation              |
| `phase`           | Thread lifecycle phase (active/interrupted/done)  |

### Resume Behavior

1. Read `journal.json` — find the most recent thread with `phase: "active"` or `phase: "interrupted"`.
2. Reconstruct the indicator: `completed_steps` → ✓ line, `current_step` → → line, remaining phases → ◦ line.
3. Present the indicator with a resume prompt: "continue from here, or restart this step?"
4. The developer should NOT need to re-explain context — the journal's `context_summary` provides sufficient orientation.

### context_summary Sufficiency Criteria

Story 2.2 owns journal write operations. The `context_summary` field in every phase-transition journal write MUST satisfy these criteria for progress indicator reconstruction:

1. **Project identity**: Include the project name or working title so the developer recognizes which project.
2. **Accumulated value per completed phase**: For each completed phase, include a brief clause describing the key output or decision (e.g., "brief captured SaaS dashboard vision", "research validated market fit with 3 competitors analyzed").
3. **Current phase context**: Describe what was in progress when the phase was entered — enough to resume without re-reading upstream artifacts.
4. **No implementation details**: Summarize outcomes and decisions, not process steps taken.
5. **Length guideline**: 1-3 sentences. Enough for re-orientation, not a full recap.

Example of sufficient context_summary:
> "Acme project — brief captured SaaS dashboard vision, research validated market fit with 3 competitors analyzed, PRD defined 12 functional requirements including real-time analytics and role-based access. UX phase started: established mobile-first constraint and began interaction pattern inventory."

Example of insufficient context_summary:
> "Working on UX phase."
