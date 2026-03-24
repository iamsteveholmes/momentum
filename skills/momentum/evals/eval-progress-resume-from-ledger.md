# Eval: Interrupted Workflow Resumption with Progress Indicator

## Scenario

Given a developer was previously working on the BMAD workflow and completed Brief, Research, and PRD phases before the session was interrupted during the UX phase, and `.claude/momentum/journal.json` contains a thread entry with:

```json
{
  "thread_id": "bmad-acme-2026-03-20",
  "workflow": "bmad",
  "current_step": "ux",
  "phase": "active",
  "context_summary": "Acme project — brief captured SaaS dashboard vision, research validated market fit with 3 competitors analyzed, PRD defined 12 functional requirements including real-time analytics and role-based access. UX phase started: established mobile-first constraint and began interaction pattern inventory.",
  "completed_steps": ["brief", "research", "prd"],
  "updated_at": "2026-03-20T14:30:00Z"
}
```

When the developer invokes `/momentum` in a new session, Impetus should reconstruct the workflow position from the journal and present the progress indicator with a resume prompt.

## Expected Behavior

1. Impetus detects the interrupted workflow from `journal.json`
2. Displays the progress indicator showing the correct position:

```
  ✓  Brief · Research · PRD               vision through requirements defined
  →  UX                                   building interaction patterns
  ◦  Architecture · Epics · Stories       3 phases to implementation
```

3. Asks: "continue from here, or restart this step?" (or equivalent phrasing)
4. The developer does NOT need to re-explain their context — the journal's `context_summary` provides sufficient orientation
5. Every symbol in the indicator has adjacent text pairing

## NOT Expected

- Asking the developer "what were you working on?" or requiring re-explanation
- Showing the wrong step as current (e.g., showing Research as current when UX was interrupted)
- Starting from the beginning of the workflow without acknowledging prior progress
- Missing the resume prompt (continue/restart choice)
- A symbol without adjacent descriptive text
- "Step 4/7" or any numeric position format
