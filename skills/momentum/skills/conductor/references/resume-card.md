# Resume Card — Session-Death-Proof Gate Agenda (DEC-040 D5)

**Purpose:** A conduct build's mandatory human gate (Phase 5) — and, before that, the build itself
— can be interrupted by session death at any point. Without a durable pointer back to "where we
were and what's pending," the developer returns to a wall of text or a decision they have to
reconstruct from scratch. The resume card is that durable pointer: a small JSON file, sibling to
the build ledger, that always states where the run got to and the single question currently
waiting on a human.

This is a **seam contract**: the Conductor (producer) and Impetus (consumer) are two independently
edited surfaces. Both cite this document as their source of shape instead of restating field names,
so the two halves cannot drift apart the way `escalation.timing_tier` (nested) vs. `F.timing_tier`
(flat) once did on `directed-fix-invocation-contract`.

---

## File Location

```
.momentum/sprints/{{sprint_slug}}/resume-card.json
```

One card per sprint. Sibling to `build-ledger.jsonl` — same directory, same survival guarantee.
Unlike the ledger, this file is **overwritten in place** on every refresh (it is a single current
snapshot, not an append-only event log). Created on first write; no pre-creation step.

**Correlation key:** `sprint_slug`. Assigned by: the Conductor, at sprint-plan time (the same value
already used for the sprint directory and the build ledger). Uniqueness scope: one card file per
sprint directory — the path itself is the uniqueness boundary. Lifetime: for the life of the sprint
directory. The Conductor never deletes a card; a resolved sprint's card simply stops being pending.

---

## Canonical Output Shape

```json
{
  "sprint_slug": "sprint-2026-08-03",
  "status": "pending",
  "phase": "end-gate",
  "merged": {
    "count": 3,
    "slugs": ["story-a", "story-b", "story-c"]
  },
  "blocked": {
    "count": 1,
    "slugs": ["story-d"]
  },
  "question": {
    "text": "Approve merge to main and push to origin, or request changes?",
    "gates": "the tier-1 merge gate — merging this sprint's work to main and pushing to origin",
    "options": ["Approve", "Request changes"],
    "report_path": ".momentum/handoffs/sprint-2026-08-03-endgate-report.html"
  },
  "waited_since": "2026-08-24T18:04:11Z",
  "resurface_count": 2,
  "resolved_at": null,
  "resolution": null
}
```

A resolved card carries the same shape with `status: "resolved"`, `resolved_at` set, and
`resolution` set (e.g. `"approved"`, `"changes-requested"`, `"closed"`) — every other field is left
as it stood at resolution, a historical record of the last pending state.

---

## Field Definitions

| Field | Type | Writer | Set/updated when |
|---|---|---|---|
| `sprint_slug` | string | Conductor | Written once, at first card creation. Never changes. |
| `status` | `"pending"` \| `"resolved"` | Conductor only | `"pending"` on every emit/refresh while a question is open. `"resolved"` only when the developer actually resolves the currently-open question (see Resolution below). **No other value exists — see Anti-Expiry Invariant.** |
| `phase` | string | Conductor only | Refreshed on every emit — the phase the run has reached (`"build"`, `"avfl-on-merge"`, `"e2e"`, `"end-gate"`, `"closure"`, ...). Free text naming the Conductor step, not a controlled enum — new phase names may be added without a contract change. Impetus reads this to phrase its lead-in contextually; it is never separately enumerated as its own line in the greeting (see Presentation Budget). |
| `merged.count`, `merged.slugs` | int, array of string | Conductor only | Refreshed on every emit from the build ledger's `{{merged}}` set (the authoritative source — never an in-context accumulator). `slugs` exists for depth-on-demand; the greeting renders `count` only. |
| `blocked.count`, `blocked.slugs` | int, array of string | Conductor only | Same rule as `merged`, sourced from the ledger's blocked/failed story set. |
| `question.text` | string | Conductor only | The single pending question, in plain language. Exactly one question ever exists on the card — never an array, never two questions bundled into one string. |
| `question.gates` | string | Conductor only | What the question's answer controls — e.g. "the tier-1 merge gate," "whether the build continues to the next story," "the sprint's tier-2 closure verdict." Required — a question without a stated "what it gates" is a defect (AC 2). |
| `question.options` | array of string | Conductor only | The concrete answers available (e.g. `["Approve", "Request changes"]`, `["Resume the build"]`). |
| `question.report_path` | string \| null | Conductor only | Path to the end-gate report (or other depth artifact) for the developer to open for full detail. `null` when no such report exists yet (e.g. the mid-build resume-the-build question, before Phase 5 has ever rendered a report). |
| `waited_since` | string (ISO 8601) | **Shared-write** — see below | Anchors "how long has this decision been waiting." |
| `resurface_count` | integer | **Shared-write** — see below | Counts how many session greetings have surfaced this still-pending card. |
| `resolved_at` | string (ISO 8601) \| null | Conductor only | Set once, at resolution. `null` while pending. |
| `resolution` | string \| null | Conductor only | Set once, at resolution — the resolution kind (`"approved"`, `"changes-requested"`, `"closed"`, or another Conductor-defined value). `null` while pending. |

### The two shared-write fields — write semantics (Task 2 declaration)

`waited_since` and `resurface_count` are the **only** fields either side may write outside its own
role. Every other field above is exclusively Conductor-written (Impetus is read-only on them) or
exclusively Impetus-written. This narrow exception exists because both halves have a legitimate
claim on "how stale is this decision":

- **`resurface_count`** — the Conductor emits it at `0` when a question first begins waiting.
  **Impetus increments it by exactly 1** each time it surfaces this still-pending card in a session
  greeting (read-modify-write the file). The Conductor never increments it and never resets it
  except by starting a brand-new question (see below).
- **`waited_since`** — the Conductor sets it to `NOW()` whenever it writes a question that is **new**
  relative to the card's current `question.text` (first emission of a question, or a change in
  which question is pending — e.g. build-resume question → merge-gate-approval question →
  closure-verdict question). The Conductor **leaves the existing value unchanged** when it refreshes
  the card for the **same still-pending question** (e.g. a phase-checkpoint refresh during the
  build, or the redispatched ask after a request-changes pass — both keep the clock running on the
  same decision). Impetus never changes this value, but every file write Impetus performs to
  increment `resurface_count` necessarily rewrites the whole object — `waited_since` is carried
  forward unchanged in that same write. This is what makes it "shared-write" rather than
  Conductor-exclusive: an Impetus rewrite that includes this field unchanged is not a violation:
  an Impetus rewrite that *changes its value* would be.

No other field may be written by both sides. A field written by both without this explicit
declaration is a Task 7 finding.

---

## Anti-Expiry Invariant (AC 10 — contract-level rule, not an implementation note)

`status` has **exactly two values**: `pending` and `resolved`. **No time-based transition between
them exists, anywhere in this contract.** Neither elapsed wall-clock time, nor `resurface_count`,
nor session count, nor any other measure of staleness may ever change `status` away from `pending`
on its own. The only thing that resolves a card is a recorded developer decision (see Resolution
below). A card may be re-surfaced across dozens of sessions and weeks of elapsed time and must
still read `pending` throughout — rising `resurface_count` and an aging `waited_since` are the
**entire** mechanism for rising prominence (AC 9); there is no escalation path that ends in a
failed/expired/auto-resolved status. (DEC-040 D5 explicitly rejected the researched 48-hour
expiry-to-FAIL design — do not reintroduce it here or anywhere downstream of this contract.)

---

## Resolution

The Conductor sets `status: "resolved"` (with `resolved_at` and `resolution`) at exactly these
points, and nowhere else:

1. **Approve, merge verified.** The developer approves the end-gate and the merge-gate outcome is
   confirmed `"merged"` (the full execute-and-verify sequence passed). `resolution: "approved"`.
2. **Request-changes cycle begins.** The developer answers the end-gate ask with a change request.
   The *current* pending question ("approve or request changes") is answered the instant the
   developer chooses that path — `resolution: "changes-requested"`. A **new** pending card (new
   `question`, fresh `waited_since`) is written moments later at the redispatched ask, once the
   autonomous fix pass completes and the report is re-rendered. The developer is never shown a gap
   between these two states within one live session; the resolve-then-re-pend pair exists so an
   interrupted session between them still leaves an accurate durable record of what was answered
   and what is newly waiting.
3. **Tier-2 closure succeeds.** `momentum-tools sprint complete` succeeds (fresh close or the
   idempotent no-op). `resolution: "closed"`.

**Idempotency:** resolving an already-resolved card is a no-op — check `status` before writing; if
already `"resolved"`, do not write again. This guarantees a resumed session can never double-write
or regress a resolved card back to `pending`.

Once resolved, Impetus stops surfacing the card from the next session onward (AC 11) — the read
side filters on `status == "pending"` only.

---

## Presentation Budget (shared definition of "compact" — AC 8)

Both sides share this definition so neither drifts toward a wall of text:

- **Lead:** at most two sentences.
- **Merged/blocked:** rendered as `merged.count` and `blocked.count` only — never the `slugs`
  arrays enumerated inline.
- **Question:** exactly one, with its `options` — never more than one question, never omitted.
- **Depth:** `question.report_path` is linked, never inlined.
- **Repetition:** `resurface_count` and the age of `waited_since` add exactly one line on
  re-surfacing (AC 9) — the rest of the card's rendered length does not grow with repetition.

A rendered surface that violates any bullet above is a defect under the Decision-Grade
Presentation Standard, independent of this contract.

---

## Producer — Who Writes, and When

The Conductor (`skills/momentum/skills/conductor/workflow.md`) is the sole writer of every field
except the two shared-write fields' updates from Impetus. Emit/refresh sites (all cite this
contract instead of restating field shape):

- Phase 2 build loop, on each `story-terminal` row with `outcome: "merged"` — refreshes
  `merged`/`blocked`/`phase`, question stays "resume the build."
- The `avfl-on-merge-complete` and `e2e-phase-complete` phase checkpoints — same refresh, question
  unchanged.
- Phase 5, immediately before the end-gate report is opened (both the initial open and every
  redispatch after a request-changes pass) — inside the RENDER-THEN-ASK atomic block, so no turn
  boundary can separate gate render from card durability.
- The tier-2 sprint closure gate, when closure is refused/pending — the question becomes the
  closure verdict question.

Card contents are always sourced from the build ledger (the authoritative source), never from
in-context accumulators — an interrupted-then-resumed run must produce the same card an
uninterrupted run would have at that point.

## Consumer — Who Reads, and When

Impetus (`.claude/rules/impetus.md`) reads every `resume-card.json` across `.momentum/sprints/*/`
as part of its single session-start Bash call — independent of which sprint is marked active, since
a gate can be pending on a sprint that never closed. It keeps only cards with `status == "pending"`.
If more than one is pending, the one with the most recent `waited_since` leads; the rest are named
in a single count line. Impetus never writes any field except the two shared-write updates
described above, and never creates, repairs, or backfills a card.

### Malformed card handling

A card file that exists but is missing or renames `status` or `question` (the two fields the
consumer cannot safely default) is not silently treated as "no card." Impetus names the offending
file path and states that a resume card was found but its shape is unreadable — because a broken
card may be hiding a genuinely pending gate, silently skipping it is the exact wall-of-silence
failure mode this contract exists to prevent. This is a shape-incompatibility signal, not a normal
"no pending work" state.

---

## Source Decisions

- **DEC-040 D5** — the resume card and pending-gate agenda this contract implements; rejects the
  researched 48-hour expiry-to-FAIL design.
- **`contract-seam-stories-two-sided-review-scope`** — the seam-contract convention this document
  follows (Canonical Output Shape, correlation-key declaration, two-sided review scope).
- **`references/build-ledger.md`** — the authoritative source this card's contents are derived
  from; the sibling durable-state convention this file follows for path and survival guarantees.
