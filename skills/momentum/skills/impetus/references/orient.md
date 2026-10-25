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
- `{project-root}/.momentum/features.json` — feature registry (DEC-040 D1), read-only. A JSON
  object keyed by feature slug; derive N (entries with `status == "passing"`) and M (total entries).
  `failing`, `absent`, and no-status entries all count toward M, never toward N. Absent file, zero
  entries, or a malformed/unexpected-shape file (invalid JSON, not an object, entries missing the
  expected structure) is the same honest "no features tracked yet" state, reported the same way as
  any other missing source below — never an error, never a fabricated count. This source is never written by Impetus;
  `momentum-tools feature register` is the sole creator of entries and `momentum-tools feature verify` the sole writer of status/last_verified.
- `{project-root}/.momentum/sprints/*/resume-card.json` (DEC-040 D5) — pending build-gate cards,
  scanned across every sprint directory regardless of which sprint (if any) is `active`. Keep only
  cards whose `status` reads `"pending"`; a card whose shape fails the check (missing or renamed
  `status`, `question`, or any of `question.text`/`question.gates`/`question.options`) is named in
  the report rather than treated as "no card". On every surfacing of a still-pending card, increment
  its `resurface_count` by 1 and leave `waited_since` unchanged — this is the one narrow shared-write
  exception to this source's otherwise read-only status; only the leading, fully-rendered card is
  "surfaced" and increments — when several cards are pending, those named only in the count line
  are not surfaced and are not rewritten; no other field is ever touched, and no card
  is ever created, repaired, or backfilled by Impetus. Full field shape, correlation key, and write
  semantics are the seam contract at `skills/momentum/skills/conductor/references/resume-card.md` —
  cite it rather than restating field names. This source and its leading-report precedence mirror
  `.claude/rules/impetus.md`'s Session-start behavior section; that rule is authoritative if the two
  ever diverge.

There is no fallback to `_bmad-output/implementation-artifacts/`. If a source is missing, report state honestly (e.g., "no sprints recorded") rather than substituting old paths.

## Situational States

Derive which state the project is in and orient accordingly. In every state below, the **feature
headline (N of M feature acceptance conditions passing, or the honest no-features-tracked-yet
statement) leads** — every "Lead with" cell in this table is supporting context that comes
**after** the feature headline, with two exceptions, in precedence order: a pending resume card,
then a `leading`-tier tasting nudge (which itself yields to a pending card). Per DEC-040 D5 and
`.claude/rules/impetus.md`, a pending resume card leads the whole report ahead of the feature
headline whenever one exists; absent a pending card, a `leading`-tier tasting nudge becomes the
report's first sentence, ahead of the feature headline, per `.claude/rules/impetus.md`;
absent both, the feature headline is first as stated below.

| State | Signal | Lead with |
|---|---|---|
| Pending build gate | A `resume-card.json` with `status: "pending"` exists in any sprint directory | **Leads the whole report, ahead of the feature headline** — the card's question and options, phrased using its `phase` and `question.gates` so the sentence is self-sufficient; count lines only for merged/blocked work; the feature headline (N of M) follows it (behind a `leading` tasting nudge's fallback placement, if one is also due) |
| Active sprint | `sprints.active` is non-null | *After the feature headline:* sprint name, stories in-progress, what's near done |
| Sprint planning ready | `sprints.planning` is non-null | *After the feature headline:* what's been selected, invite to activate |
| Between sprints | Both null, last sprint has `completed` date | *After the feature headline:* when last sprint closed, retro status, suggest next move |
| Clean slate | No sprints at all | *After the feature headline:* fresh start — suggest sprint planning |
| Stories in-progress, no sprint | `stories/index.json` has `in-progress` items | *After the feature headline:* surface the active work, note the gap |
| Pending signals present | `.momentum/signals/` has uncleared `*.json` files | *After the feature headline:* surface the outstanding signals alongside sprint/story state |

## Delivery Principles

- One grounded situation statement, then suggestions — not the other way around
- The feature headline (N of M) leads the situation statement, except when a pending resume card
  exists — that leads instead, with N-of-M following it (behind a `leading` nudge's fallback placement, if one is also due) — or, absent a card, when a
  `leading`-tier tasting nudge opens the report ahead of it (see Situational States
  above and `.claude/rules/impetus.md`). Story counts never lead. Where a story count still
  appears, it appears after the feature number as supporting detail.
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
