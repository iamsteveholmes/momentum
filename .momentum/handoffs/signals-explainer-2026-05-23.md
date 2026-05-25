# Signals — What They Are, Why They Exist, What To Decide

**Date:** 2026-05-23
**Purpose:** Explain the `.momentum/signals/` concept so you can decide whether to ship it, collapse it into practice-ledger, or defer.

---

## What signals/ is supposed to be (per FR120 + architecture)

`.momentum/signals/` is a directory of tiny JSON files. Each file is **one pending work flag** — a small structured marker saying "this kind of thing needs attention."

Two types are defined today:

| Signal type | Written when | Cleared when |
|---|---|---|
| `triage-uncleared` | Triage captured observations but didn't classify/resolve all of them | Developer classifies or rejects them next session |
| `avfl-finding-pending-upstream-fix` | AVFL found an issue that traces to a spec/rule/workflow root cause that hasn't been queued for fixing | The upstream fix story is created or applied |

Schema (each file):

```json
{
  "signal_type": "triage-uncleared",
  "origin": "momentum:triage",
  "created": "2026-05-23T14:30:00Z",
  "payload": { /* signal-specific structured data */ },
  "cleared": null  // ISO timestamp when resolved; null while open
}
```

Filename convention: `{signal_type}-{slug-or-timestamp}.json`.

**Intended writers:** retro, triage, avfl.
**Intended reader:** Impetus session orientation — at session start, scan the directory, surface "you have N pending signals" with their types/origins.

---

## The mental model

| Artifact | What it answers | Size profile |
|---|---|---|
| **practice-ledger.jsonl** (formerly intake-queue) | "What's the full history of what happened?" — event log, persistent, monotonically growing | Hundreds → thousands of entries |
| **signals/** | "What's screaming for my attention RIGHT NOW?" — small set of currently-active flags | Typically 0–5 entries |

Analogy: practice-ledger is your inbox + sent folder. Signals is the notification badge on app icons.

The reason they're separate:
- Practice-ledger answers "show me history, filter by source/kind/status" — a query that returns dozens of entries.
- Signals answer "what's actively blocking or waiting for me right this second" — a binary at-a-glance display, typically empty or a handful of items.

Mixing them means the "currently actionable" query has to filter through hundreds of historical entries every session, and the line between "open and waiting" vs "open but not blocking" gets fuzzy.

---

## Current state (per Agent D's audit)

- Directory exists. Has only a `README.md` documenting the schema.
- **Zero signal files have ever been written.** No actual signals exist.
- **No producer has shipped.** retro, triage, avfl workflows all declare intent but never emit signal writes.
- The architecture acknowledges this gap explicitly as **ARCH-8** ("As of 2026-05-22, no done stories actually implement signal write calls in retro or triage. The signals/ directory and schema contract are established, but the producers are pending — not yet shipped.")
- **Legacy `momentum:impetus` skill IS ready to read signals** — its `orient.md` reference file implements the full read contract (iterate directory, surface pending signals as situational state). There's even a unit eval that verifies graceful empty-directory handling.
- **New experimental `.claude/rules/impetus.md` does NOT reference signals/ at all** — when I wrote that rule earlier, I forgot signals existed.

So: schema is done, reader is done in the legacy skill, but the producers were never shipped and the new rule doesn't know about signals.

---

## The three real options

### Option A — Ship the producers; keep signals/ distinct from practice-ledger

**What it means:** Honor the existing FR120 contract. Write code (in `momentum-tools`) for `signal-write` and `signal-clear`. Update retro, triage, avfl workflows to call those CLI commands when their conditions are met. Add signals/ to the new Impetus rule's session-start scan.

**Pros:**
- Honors a decided architectural pattern.
- Signals stay tiny, queries stay cheap.
- The "what's screaming at me?" surface is honest — only what's actually unresolved appears.

**Cons:**
- More moving parts (two surfaces instead of one).
- Producer-clearer protocol can drift (e.g., triage writes a signal, the issue gets handled by some other path, signal is never cleared, stale flag lingers — same rot pattern as practice-ledger).
- Adds work to this cascade (new CLI subcommands, updates in 3 skill workflows, rule update).

### Option B — Collapse signals/ into practice-ledger with an "attention" query

**What it means:** Don't ship the producers. Instead, the practice-ledger gets a small set of `event_type` values that mark something as actively-pending attention (e.g., `attention_flag`). Add a `momentum-tools practice-ledger attention` query that returns just those entries. Impetus surfaces that result.

**Pros:**
- One artifact. One schema. One CLI. Simpler.
- Doesn't double the producer-clearer drift surface.
- The cascade we already have grows by maybe 20% to add the attention query.

**Cons:**
- The "attention" query has to filter through the full ledger every time. Performance is fine until the ledger has thousands of entries; manageable.
- Mixes ephemeral attention-grabbing flags with persistent history in one file — semantics get muddier.
- Loses the file-per-signal property (which makes git-tracking individual signals visible in commits — minor benefit).

### Option C — Defer the signals/ decision out of this cascade

**What it means:** Park it. Practice-ledger cascade ships. Signals/ stays empty. We come back to it later when the rest of the cascade is settled.

**Pros:**
- Smallest cognitive load right now.
- Keeps the cascade focused on what was originally decided.
- ARCH-8 stays where it is (already known and documented).

**Cons:**
- The new Impetus rule still doesn't know about signals/. If it ships as-is, we're shipping a rule that misses what could be a real attention surface.
- The "do we need this at all?" question stays open. Maybe the answer turns out to be "no, practice-ledger is enough" — in which case we wasted cycles maintaining the FR120 contract.

---

## My honest recommendation

**Option C (defer) is the safest move for THIS cascade.** Reasons:

1. The practice-ledger redesign is already substantial and has its own design subtleties (event log, custom escape, hard cut migration, DuckDB reads). Adding signals/ producer work mid-cascade increases the surface area when the cascade hasn't proven itself yet.
2. Signals' usefulness is hypothetical right now — no producers have ever run, no Impetus has ever read a real signal. We don't have empirical evidence that the "what's screaming at me?" surface is needed beyond what practice-ledger could provide.
3. Deferring it doesn't lose anything — the schema and README stay, the legacy Impetus skill's read contract stays, ARCH-8 stays as the explicit "we know this is pending" marker.
4. Once practice-ledger is live with the new schema, we'll have empirical data on what the developer actually wants to see at session start. We can then make the signals decision with real evidence instead of architectural guess.

The one wrinkle: the new `.claude/rules/impetus.md` needs to either (a) reference signals/ and document them as "future surface, currently no producers" or (b) ignore them entirely until the deferred decision lands. (a) is cleaner.

---

## What I need you to decide

1. **Which option** (A ship, B collapse, C defer)?
2. **For the new Impetus rule** — should it mention signals/ as a future surface (option a above) or ignore until decided (option b above)?
