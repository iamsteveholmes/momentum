# Cross-Story Seam Coherence — Matching Heuristics

**Implements:** Step 3.6 (`Cross-story seam coherence check`) of `sprint-planning/workflow.md`.
**Root cause this closes:** nornspun sprint-2026-05-30 — consumer story
`campaign-init-offered-suggestion-list-render-and-routes` depended on producer
`backend-campaign-init-add-offered-suggestion-list-copy` for "the backend payload," but the
producer only edited a system prompt and delivered no payload. Both stories passed their own
gates; the seam between them belonged to no one.

**Extends, does not replace:** Step 2's shallow `depends_on` check (presence/status: is the
producer `done` or in-sprint?) stays as-is. This gate adds the missing semantic half: *does the
producer actually deliver what the consumer names?* One `depends_on` feature, two steps.

---

## 0. Vocabulary (binding)

Call this check **"cross-story seam coherence"** or **"seam coherence"**. A failure is a **"seam
coherence failure"** or **"cross-story coherence mismatch."**

Never use **"contract-freeze," "freeze," or "lock"** to describe this check or its failures —
those words already mean the per-story `frozen_sha256` temporal-integrity check
(`conduct-contract-freeze-check`). This gate is a different, semantic thing: unrelated wording.

---

## 1. Edge model

For every story `S` in `{{selected_stories}}` with a non-empty `depends_on`, and every slug `D`
in `S.depends_on`, create one edge:

```
edge = {
  consumer:   S,
  producer:   D,
  in_sprint:  D ∈ {{selected_stories}}
}
```

Enumerate **every** such edge — in-sprint and out-of-sprint alike. This full list is
`{{coherence_edges}}`. Nothing is filtered out at this stage; even edges with no concrete
named input (see §3) are recorded, just classified as `presence-only`.

---

## 2. Consumer input extraction

Read the consumer story's own file in full — `.momentum/stories/{{consumer_slug}}.md`
(Story/Description, Acceptance Criteria, Dev Notes). This is the human-authored source of what
the consumer expects; read it directly rather than relying only on its frozen contract, since
contract language is Outsider-Test-filtered and may abstract away the exact producer linkage.

For each edge, look for language that names a **concrete thing** the consumer expects the
producer to supply — not bare ordering language ("build after X", "needs X to land first").
Signal phrases (apply judgment; this list is illustrative, not exhaustive):

- "from the backend", "the backend payload/response", "an endpoint", "a schema"
- "a config key/value", "an emitted constant", "a signal from", "a field"
- "sourced from", "delivered by", "supplied by", "provided by", "the API"

If such language is found: set `{{named_input}}` = a short, concrete paraphrase of the thing
named (e.g., "a backend response field carrying the offered-suggestion copy").

If no such language is found — the dependency is purely sequencing, with nothing specific
named — set `{{named_input}} = null`. Classify the edge `presence-only`: it is still counted
in `{{coherence_edges}}` and reported, but is not subject to semantic matching (Step 2's
presence/status check already covers pure ordering deps).

---

## 3. Producer deliverable resolution

For every edge with a non-null `{{named_input}}`, resolve what the producer actually delivers.

### 3a. In-sprint producer (`edge.in_sprint == true`)

Read the producer's frozen contract at
`.momentum/sprints/{{sprint_slug}}/specs/{{producer_slug}}.*` (authored by Step 3.5). Read the
full Part-A header (`how_dev_self_checks` especially) plus the entire Part-B body, extracting
the observable-deliverable text by format:

| Extension | Read |
|---|---|
| `.eval.yaml` | every `scenarios[].then` entry + `pass_criteria` |
| `.trigger.md` | `## Observable Outcome` |
| `.smoke.sh` | the assert/echo lines |
| `.review.md` | `## Required Claims` + `## Required Sections` |
| `.feature` | every `Then` clause |

Store the result as `{{producer_deliverable_text}}`.

### 3b. Out-of-sprint producer (`edge.in_sprint == false`)

1. Look up `{{producer_slug}}` in `.momentum/stories/index.json`. Read its `status`.
   - Status is **not** `done` → the edge is a coherence failure now: reason "producer not
     complete." Skip resolution and go straight to §5 (failure recording).
   - Status **is** `done` → continue.
2. Resolve `{{producer_deliverable_text}}` in this priority order:
   a. Search `.momentum/sprints/index.json` → `completed[]` for the entry whose `stories` list
      contains `{{producer_slug}}`. If that entry has
      `team.story_assignments[{{producer_slug}}].contract.path`, read that file (same
      Part-A/Part-B extraction as §3a — the sprint directory persists on disk after
      completion, so the path resolves).
   b. If no `completed[]` entry carries a `contract` block for this slug (older sprints predate
      the DEC-029/030 contract schema), fall back to reading
      `.momentum/stories/{{producer_slug}}.md` directly — its Acceptance Criteria and
      Description sections stand in as the recorded deliverable text.
3. If neither source resolves any text at all (a `done` story with no recorded deliverable
   anywhere — should be rare): treat as a coherence failure, reason "producer marked done but
   no recorded deliverable found."

---

## 4. Matching

Compare `{{named_input}}` against `{{producer_deliverable_text}}` by semantic judgment, not
string equality. The question: does the producer's own recorded observable deliverable
plausibly provide the concrete thing the consumer names?

- **SATISFIED** — the producer text describes emitting/delivering/exposing something that
  plausibly is the named input (a matching field, endpoint, schema, config value, constant, or
  signal).
- **MISMATCH** — the producer text describes something else entirely (an internal prompt edit,
  unrelated logic, an unrelated surface) with no reasonable reading that it delivers the named
  input.

**Canonical mismatch anchor:** consumer names "the copy sourced from the backend payload."
Producer's deliverable text describes only an Urd system-prompt edit — no payload field, no
endpoint, no schema appears anywhere in it. No reasonable reading satisfies "backend payload"
from a system-prompt-only change → **MISMATCH**.

**Canonical satisfied anchor:** consumer names "the response field carrying the suggestion
copy." Producer's deliverable text states the endpoint's response now includes that field →
**SATISFIED**.

---

## 5. Failure card format

Every `MISMATCH` and every "producer not complete" / "no recorded deliverable" edge becomes one
failure entry:

```
- consumer: {{consumer_slug}}
  producer: {{producer_slug}}
  missing:  <the specific named input the consumer expects but the producer does not deliver —
             quote or closely paraphrase both the consumer's ask and the producer's actual
             deliverable, so the mismatch is self-evident>
  seam:     <one sentence naming the boundary this crosses, e.g. "backend response payload →
             client render">
  resolutions:
    1. Amend {{producer_slug}}'s contract to deliver <missing>
    2. Amend {{consumer_slug}} so it no longer requires <missing>
    3. Add a new story to own <missing> (a wiring story)
```

Store the full list as `{{coherence_failures}}`.

---

## 6. Coherence report file

Write `.momentum/sprints/{{sprint_slug}}/coherence-report.md`:

```markdown
# Cross-Story Seam Coherence Report — {{sprint_slug}}

{{edge_count}} depends_on edge(s) examined ({{in_sprint_count}} in-sprint,
{{out_of_sprint_count}} out-of-sprint).

## Satisfied
- {{consumer}} → {{producer}}: {{named_input}} — satisfied by {{one-line evidence from
  producer_deliverable_text}}
(or, for presence-only edges: "{{consumer}} → {{producer}}: presence-only — no named
deliverable to match, Step 2 covers presence/status")

## Open Coherence Failures
<one failure card per §5, formatted exactly as above>
(or, if none: "None — every edge with a named input resolves to a matching producer
deliverable.")

## Override Decisions
<empty until Step 8 records one — see §7>
```

This file is the durable record read back by Step 7 (fork synthesis) and Step 8 (activation
gate).

---

## 7. Override recording (used by Step 8)

If open failures remain at Step 8's pre-activation gate and the developer explicitly instructs
the run to proceed anyway, append to the `## Override Decisions` section of
`coherence-report.md`:

```markdown
- {{timestamp, UTC}} — overridden by developer.
  Open at override time: {{list of "consumer → producer" pairs still open}}
  Developer note: "{{verbatim override instruction or fork verdict text}}"
```

Write this whether the override came from the Step 7 gate's per-fork verdict text (pasted
decision block) or from an explicit instruction given directly at the Step 8 prompt. This
satisfies the requirement that the override be visible in a durable record after the run —
not merely implied by the sprint having activated.
