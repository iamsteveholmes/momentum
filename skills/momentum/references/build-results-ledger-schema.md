# Build-Results Ledger Schema

**Version:** 1.0 — stable schema established 2026-06-07

The build-results ledger records the outcome of each story's conduct pipeline run. One row per story per run. Every row uses the **same stable schema** defined here — no field drift across rounds, no prose rows mixed with structured rows.

---

## Canonical Join Key

`slug` is the **canonical join key** for the build-results ledger. Every row carries a `slug` value that is a real story slug — no prose labels, no non-story keys. The same `slug` value ties each build-results row to the corresponding finding cards in the finding-cards ledger via `story_slug`. A join of the two ledgers on this key must lose no stories.

---

## Row Schema

Every build-results row carries the following fields. Fields marked *optional* may be absent when not applicable; all other fields are required for every row.

| Field | Type | Required | Meaning |
|---|---|---|---|
| `slug` | string | yes | Story slug — the canonical join key. Must be a real story slug; no prose labels. |
| `round` | integer | yes | The conduct build round in which this story was processed (1-based). |
| `title` | string | yes | Human-readable story title for display. |
| `verification_method` | string | yes | How the story was verified: `document-review`, `skill-invoke`, `e2e`, or other named method from the contract. |
| `qa_verdict` | string | yes | QA verdict: `PASS` or `FAIL`. |
| `freeze` | string | yes | Freeze-check result: `MATCH` (implementation matches frozen contract) or `DRIFT` (diverged from frozen contract). |
| `findings_total` | integer | yes | Total number of findings produced by all reviewers for this story. |
| `legitimate` | integer | yes | Count of findings judged legitimate (`legitimate: true`). |
| `fixed` | integer | yes | Count of findings with `disposition: fixed`. |
| `dismissed` | integer | yes | Count of findings with `disposition: dismissed`. |
| `escalated` | integer | yes | Count of findings with `disposition: escalated`. |
| `fix_summary` | string | yes | One-sentence summary of what the fix loop changed. Empty string when `findings_total` is 0. |
| `merged` | boolean | yes | Whether the story's worktree was merged to the sprint branch. |
| `merged_at` | string (ISO 8601) | yes | Timestamp of merge. Present when `merged` is true; null or absent when `merged` is false. |
| `blocked` | boolean | yes | Whether the story was blocked (a dependency was unmet or a conduct stop condition fired). |
| `diverged` | boolean | yes | Whether the worktree had diverged from the sprint branch base at merge time (true = needed a rebase or merge commit). |
| `recheck` | string | optional | Present when a recheck pass was run after an initial fix attempt: `CLEAN` (no new findings), `REFIXED` (additional fixes applied), or `STILL-FAILING`. |
| `deliverables` | string[] | optional | List of file paths changed by this story. Present when the story produced trackable file-level deliverables. |
| `note` | string | optional | Informational annotation — for context that does not fit the structured fields. Never used as a substitute for a structured field. |
| `gates` | object | optional | Structured sub-verdict for each conduct gate. When present, carries `dev`, `qa`, and `code_review` keys, each with value `pass`, `fail`, or `pass-after-fix`. Omitted when gate detail is not separately tracked. |

### gates sub-object (when present)

| Key | Values |
|---|---|
| `dev` | `pass` \| `fail` |
| `qa` | `pass` \| `fail` |
| `code_review` | `pass` \| `pass-after-fix` \| `fail` |

---

## One Shape, All Rounds

Every row in the ledger uses the schema above regardless of round number. The distinction between "structured gates rows" and "prose key rows" that appeared in conduct-core's build-results JSONL is not valid under this schema. The `key` field used in rounds 3–6 of that run is replaced by `fix_summary`, which carries the same content in a stable named field.

**`key` is not a valid field name in this schema.** Any producer emitting a `key` field must rename it to `fix_summary`.

---

## Example Row

```jsonl
{
  "slug": "example-story-slug",
  "round": 3,
  "title": "Example Story Title",
  "verification_method": "document-review",
  "qa_verdict": "PASS",
  "freeze": "MATCH",
  "findings_total": 4,
  "legitimate": 4,
  "fixed": 3,
  "dismissed": 1,
  "escalated": 0,
  "fix_summary": "Fixed three spec-compliance issues; dismissed one false-positive style note",
  "merged": true,
  "merged_at": "2026-06-07T12:00:00Z",
  "blocked": false,
  "diverged": false,
  "recheck": "CLEAN",
  "deliverables": ["skills/momentum/references/example.md"],
  "gates": {"dev": "pass", "qa": "pass", "code_review": "pass-after-fix"}
}
```

---

## Join: Finding-Cards ↔ Build-Results

The two conduct ledgers join on a single canonical key:

| Ledger | Key field |
|---|---|
| Finding-cards ledger | `story_slug` |
| Build-results ledger | `slug` |

A consumer joining on this key must find a corresponding entry in each ledger for every story that participated in the build. An intentional absence is valid — for example, a story that produced zero findings will have no finding cards but will have a build-results row with `findings_total: 0`. The converse (a story with finding cards but no build-results row) is a schema violation.

No entry in either ledger may be keyed to a value that is not a real story slug.

---

## Companion Schema: Event-Level Build Ledger

The story-level build-results row defined here and the event-level build ledger (`skills/momentum/skills/conductor/references/build-ledger.md`) are companion schemas at different granularities. A build-results row is derivable by folding a story's event-level ledger rows (collecting terminal outcome, finding counts, disposition counts, merge status). The two schemas join on the story slug: `slug` in build-results, `story_slug` in the event ledger.

---

## Source Decisions

- **DEC-035** — Adopt conduct; one human end-gate; no story-count cap; legible auto-fix loop.
- **Retro finding (sprint-2026-06-02-conduct-core)** — Build-results schema drifted mid-build: 3 structured gates rows vs 18 prose key rows. Two real story slugs had no card key; two non-story prose keys existed. This schema eliminates that drift by defining one stable row shape and requiring a canonical join key on every entry.
