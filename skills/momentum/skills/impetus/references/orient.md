---
name: Orient
code: orient
description: Read project state silently and deliver a grounded situational report with specific next-step suggestions.
---

# Orient

## What Success Looks Like

After a silent read of sprint state and story status, the owner receives a clear situational report in plain language — where the work stands, what's active, what's pending — and 2-3 specific next-step suggestions grounded in what the data actually shows. The owner should feel oriented within the first exchange, not after three questions.

## State Sources

Read these silently at session open. No narration. The owner sees only the synthesis.

- `{project-root}/.momentum/sprints/index.json` — sprint lifecycle: check `active`, `planning`, `completed` (last entry), and `quickfixes`
- `{project-root}/.momentum/stories/index.json` — story status across the backlog: in-progress, ready-for-dev, done
- `{project-root}/.momentum/signals/` — pending work flags (retro-derived). Iterate the directory; if empty or absent, no narration. For each `*.json` signal file, read `signal_type`, `origin`, `payload` and surface as part of orientation context.

There is no fallback to `_bmad-output/implementation-artifacts/`. If a source is missing, report state honestly (e.g., "no sprints recorded") rather than substituting old paths.

## Situational States

Derive which state the project is in and orient accordingly:

| State | Signal | Lead with |
|---|---|---|
| Active sprint | `sprints.active` is non-null | Sprint name, stories in-progress, what's near done |
| Sprint planning ready | `sprints.planning` is non-null | What's been selected, invite to activate |
| Between sprints | Both null, last sprint has `completed` date | When last sprint closed, retro status, suggest next move |
| Clean slate | No sprints at all | Fresh start — suggest sprint planning |
| Stories in-progress, no sprint | `stories/index.json` has `in-progress` items | Surface the active work, note the gap |
| Pending signals present | `.momentum/signals/` has uncleared `*.json` files | Surface the outstanding signals alongside sprint/story state |

## Delivery Principles

- One grounded situation statement, then suggestions — not the other way around
- Suggestions must follow from data: "Sprint closed April 15, retro done, no active sprint — ready to plan the next push?" not "Things are looking good!"
- If genuinely nothing is outstanding: "Clean slate — no active sprint, backlog is healthy. Want to explore what's next?"
- 2-3 suggestions maximum — more is noise
- Never narrate the reads. Ever.

**One explicit exception to the silent-read rule:** the plugin cache staleness warning. When
`session plugin-cache-check` returns `status: "skew-cache-behind"` or `"skew-cache-ahead"`,
Impetus surfaces the warning from `references/staleness-warning.md` **before** the orientation
greeting. This is a deliberate, sanctioned exception — not a narration of a read, but a
protective action taken on behalf of the developer. All other reads remain silent. The staleness
check is the safety net for operator-discipline lapses; the operator-discipline rule
(`feedback_fresh_session_before_major_workflows`) remains the primary mitigation.

## Memory Integration

Before speaking, check BOND.md:
- **Working mode:** Does your owner prefer a full situation report, or do they usually know what they want? Calibrate depth.
- **Decision style:** Single recommendation or options? Lead accordingly.

## After the Session

Note in the session log whether the orientation felt well-calibrated. If the owner had a different read of the situation than what the files showed, that's worth a note in MEMORY.md — it may indicate a state file that's behind, or a preference for how situations are framed.
