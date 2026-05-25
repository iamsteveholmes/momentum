---
id: AES-003
title: Practice-Ledger Defects + Epic-Layer Consolidation — State Audit and Cascade Capture
date: '2026-05-25'
status: current
method: 5 parallel discovery agents (arch+code, data+hygiene, features↔epics state, signals/ infrastructure, skill ecosystem touchpoints) + extensive developer-driven planning conversation across two sessions (2026-05-23 + 2026-05-25) + AVFL checkpoint validation against architecture.md/prd.md/epics.md
decisions_produced: []
supersedes: []
---

# AES-003: Practice-Ledger Defects + Epic-Layer Consolidation

## Purpose

Capture the current state of Momentum's practice-ledger infrastructure (currently `.momentum/intake-queue.jsonl`) and the parallel features-vs-epics layering, document the defects and gaps that have emerged in operation, and articulate the design direction that two upcoming decisions will ratify.

**Questions this assessment answers:**

1. What is the actual current state of the practice-ledger, and where does it diverge from its documented architecture?
2. What concurrency, hygiene, and surfacing defects have we accumulated?
3. What is the actual current state of the features/epics dual-layer organization, and is the cost of maintaining two parallel grouping concepts worth the value they provide?
4. What is the state of the `.momentum/signals/` infrastructure, and how does it relate to the practice-ledger going forward?
5. What direction should two upcoming decisions (practice-ledger redesign; epic-layer consolidation) take?

**Decisions this assessment informs:**

- **Decision 1 — Practice-Ledger Event-Log Redesign** (pending — will be authored next)
- **Decision 2 — Epic-Layer Consolidation** (pending — will be authored next)

## Method

Five discovery agents were spawned in parallel on 2026-05-23 against the working repository at `/Users/steve/projects/momentum`. Each agent audited a specific slice of actual codebase/artifact state, producing structured findings with evidence tables.

| Agent | Scope |
|---|---|
| **A — Practice-Ledger arch+code audit** | architecture.md Decisions 1c + 52; momentum-tools.py intake-queue functions (lines 1992–2139); search for findings-ledger code |
| **B — Practice-Ledger data+hygiene audit** | `.momentum/intake-queue.jsonl` entry analysis (88 entries; counts by status/source/kind); `.claude/rules/impetus.md` session-start rule |
| **C — Features↔Epics state audit** | `features.json` (23 entries) + `epics.md` (18 entries); cross-reference with stories/index.json (410 entries); DEC-031 D2 status; `epic-feature-collapse-closeable-grouping` story state |
| **D — Signals/ infrastructure audit** | `.momentum/signals/` directory; PRD FR120 contract; search for signal producers/readers; ARCH-8 reference |
| **E — Skill ecosystem touchpoint audit** | All readers and writers of intake-queue.jsonl + features.json across momentum-tools.py, skill workflows, agent definitions, rules, docs |

Developer scope context: this assessment captures findings that surfaced across two extensive planning sessions where each finding was investigated to its evidence and the design implications were discussed in conversation. The discovery agents re-verified the empirical claims and surfaced 4 new findings beyond the original 7-finding scope. The developer validated each finding and adjusted framing where the original assessment was wrong (notably on features↔epics direction and signals/ disposition).

---

## Findings

### Finding 1: Practice-Ledger Architecture-vs-Code Drift

| Component | Status | Evidence |
|---|---|---|
| Architecture claim (DEC-007) | Real | `_bmad-output/planning-artifacts/architecture.md:2864` — "append-only JSONL event log" with "Entries are never deleted — `status` flips from `open` to `consumed`" |
| Architecture claim (DEC-1c) | Real | `_bmad-output/planning-artifacts/architecture.md:466–476` — Findings Ledger declared "append-only JSONL ... POSIX atomic append" |
| Implementation reality | Broken | `skills/momentum/scripts/momentum-tools.py:2097–2135` — `cmd_intake_queue_consume()` performs whole-file read-modify-write: `lines = queue_path.read_text(...).splitlines()` → mutates entry in memory → `queue_path.write_text(...)` rewrites the entire file. Architecture's "append-only" promise is contradicted. |

The architecture mandates append-only semantics specifically to preserve history and enable concurrent writes without locking. The implementation honors append-only for `cmd_intake_queue_append` (uses POSIX `open('a')`) but violates it on `cmd_intake_queue_consume` — closure operations rewrite the whole file in place. The architecture-vs-code drift is not partial; the consume code path actively contradicts what the architecture promises.

### Finding 2: Lost-Update Concurrency Unsafety in Practice-Ledger

| Component | Status | Evidence |
|---|---|---|
| Append operation | Safe | `momentum-tools.py:2050` uses POSIX `open(path, "a")` — atomic for lines under PIPE_BUF (~4096 bytes), enabling concurrent appends from multiple sessions without locking |
| Consume operation | Broken | `momentum-tools.py:2097–2135` performs unprotected read-modify-write with zero advisory locking (no `fcntl.flock`, no `portalocker`, no atomic write-then-rename). Two concurrent consume calls can lose updates. An interleaved append-and-consume can lose the appended entry. A crash mid-write can corrupt the file. |
| Risk profile | Real | Sprint-dev spawns subagents that may emit ledger events concurrently. Multiple Claude Code sessions running in parallel worktrees can also trigger races. The defect is silent — lost entries don't produce visible failures. |

JSONL's concurrent-write safety promise comes entirely from POSIX atomic-append on small lines — and that safety evaporates the moment any path does whole-file rewrites. The consume path eliminates the very property that justified choosing JSONL in the first place.

### Finding 3: Practice-Ledger Backlog Rot

| Component | Status | Evidence |
|---|---|---|
| Total entries | Real | `.momentum/intake-queue.jsonl` — 88 entries (52 open, 36 consumed) |
| Status distribution | Concerning | 59% of entries are `open` — the open-list grows monotonically with no mechanism to clean it |
| Stale entries (open but superseded) | Broken | **12 stale entries:** 8 with "superseded by DEC-..." in title (work explicitly overridden by a later decision), 4 with "Test:" prefix (leftover from spike validation), 1 "Old triage-inbox.md approach" (pre-DEC-007) |
| Closure mechanism | Missing | No workflow auto-closes superseded entries. `cmd_intake_queue_consume` requires explicit `--id` per entry. No batch close, no garbage collection, no triage pass. Entries grow until manually cleaned. |

12 entries (23% of open) should be closed but aren't, because the practice has no closure discipline beyond "the developer manually runs `consume`." The lack of a closure mechanism means the open-list will continue to grow indefinitely.

### Finding 4: Impetus "Last 5" Rule Inverts Relevance

| Component | Status | Evidence |
|---|---|---|
| Current Impetus rule | Real (recently authored) | `.claude/rules/impetus.md:23` — instructs Impetus to read "open ledger entries from `.momentum/intake-queue.jsonl` (filter `status: "open"`, last 5)" |
| Coverage at current state | Broken | Surfaces 5 entries; hides 47 of 52 open entries (90.4% hidden). Counts pass; rot is invisible to session-start. |
| Quality of surfaced entries | Inverted | 4 of the newest 5 are TEST SCAFFOLDING (`Test: REJECT item`, `Old triage-inbox.md approach`, `Test: SHAPING item`, `Test: DEFER item`). The "last 5" pattern surfaces 80% junk and buries the substantive DEC-031/DEC-032 work that's actually queued. Newest ≠ most relevant. |

The "last 5" instruction was a tidiness shortcut that produced exactly the failure mode it was meant to avoid: it makes the ledger look clean while hiding both the rot AND the actionable work. The honest fix is closure discipline, not better filtering.

### Finding 5: Features vs. Epics — A Layering Cost That Will Be Resolved

| Component | Status | Evidence |
|---|---|---|
| Features layer (`features.json`) | Real | 23 features; mature 14-field schema with `value_analysis`, `system_context`, `acceptance_conditions`; sole writer is `momentum:feature-grooming` |
| Epics layer (`epics.md`) | Real | 18 epic headers; narrative-only descriptions; no per-epic `value_analysis`/`system_context`/`acceptance_conditions` fields |
| Story coverage gap | Real | 410 stories total; 141 stories in both features and epics; **269 stories in epics with no feature home**; 2 stories in features but not in epics; 3 stories cross-cut multiple features |
| DEC-031 D2 readiness | Stub | `epic-feature-collapse-closeable-grouping` story exists as backlog INTAKE STUB (never went through create-story). Neither `feature-grooming` nor `feature-breakdown` skills have been updated to support the new M:N model. |
| Categorical vs. finite-lived epic semantics | Latent confusion | The 18 epics in `epics.md` are categorical (long-lived themes — "Stay Oriented with Impetus") while features are finite-lived (closeable deliverables). Two parallel grouping concepts with different lifecycles, different schemas, different write surfaces. Maintaining both adds coordination cost. |

The dual-layer organization was historically motivated: categorical epics carried theme-based grouping, features carried value-delivery semantics with closure conditions. In practice the dual layer creates coordination overhead and conceptual ambiguity ("is this a feature or an epic?"), and the 269 unhomed stories show that features.json doesn't cover the work that's actually being done. The developer's direction (validated 2026-05-25) is to unify into a single epic concept that can be either finite-lived or long-lived, with `audience: user | internal` as a property — eliminating the dual-layer cost without forcing every categorical theme to dissolve.

### Finding 6: Signals/ Infrastructure — Schema Without Producers

| Component | Status | Evidence |
|---|---|---|
| `.momentum/signals/` directory | Real (empty) | Exists with only `README.md` (2,865 bytes). Zero signal files have ever been written. |
| PRD FR120 contract | Real | Defines schema (`signal_type`, `origin`, `created`, `payload`, optional `cleared`), recognized types (`triage-uncleared`, `avfl-finding-pending-upstream-fix`), intended writers (retro, triage, avfl), intended reader (Impetus session orientation) |
| Producer status | Missing | Architecture's ARCH-8 explicitly states: "As of 2026-05-22, no done stories actually implement signal write calls in retro or triage. The signals/ directory and schema contract are established, but the producers ... are pending — not yet shipped." Verified by grep: zero `signals/` writes in retro, triage, or avfl workflows. |
| Reader status | Asymmetric | Legacy `momentum:impetus` skill's `references/orient.md` implements the full read contract (iterate directory, surface pending signals as situational state). The new experimental `.claude/rules/impetus.md` does NOT reference signals/ at all. |

The signals/ infrastructure was designed as a complementary surface to the practice-ledger — a small, ephemeral set of attention-flags distinct from the persistent event log. Producers were never shipped, so the question "is the distinct surface actually needed?" stayed theoretical. The developer's direction (validated 2026-05-25) is to absorb signals into the practice-ledger entirely: every open entry in the ledger IS the attention surface; closure discipline replaces the need for a separate attention-flag mechanism.

### Finding 7: Latent Findings-Ledger Defect (Decision 1c)

| Component | Status | Evidence |
|---|---|---|
| Architecture intent (DEC-1c) | Real | `architecture.md:466–476` — Findings Ledger declared at `~/.claude/momentum/findings-ledger.jsonl` with append-only JSONL semantics; intended for cross-project pattern detection by the flywheel workflow |
| Implementation | Missing | Zero references to `findings_ledger` or `findings-ledger` in `momentum-tools.py`. No code, no CLI subcommands, no workflow integration. Grep across entire repo returns only architectural/planning artifacts — no production code. |
| Defect status | Latent (design-only) | The same JSONL-rewrite pattern that broke intake-queue would inherit into findings-ledger if it's implemented naively. The defect lives in the design, not in shipped code. |

The Findings Ledger is unbuilt — there is no Epic 6 flywheel implementation. This is good news because the defect hasn't shipped, and bad news because the architecture as written would produce the same lost-update problem on day one of implementation. Decision 1's redesign should pre-empt this by establishing the correct event-log pattern for the practice's ledger artifacts broadly.

### Finding 8: Story Coverage Gap — 269 Stories Without Feature Home

| Component | Status | Evidence |
|---|---|---|
| Stories in `stories/index.json` | Real | 410 stories total |
| Stories referenced in any `features.json` entry | Real | 146 unique story slugs across all `stories` arrays |
| Overlap | Real | 141 stories appear in both features and stories index (97% of features stories are also in index — features tracking is accurate for what it covers) |
| Stories NOT homed in any feature | Real | **269 stories** exist in stories/index.json but are not referenced by any feature's `stories` array |

The 269 unhomed stories are not a bug in feature-grooming — they reflect that features.json was introduced after much of the backlog was created and never retroactively classified everything. They also include quick-fix-originated work (`ad-hoc` epic) that doesn't fit the feature shape. In the post-cascade unified epic model, these stories need to be re-homed; best-effort categorization during cascade B, with `ad-hoc` accepting the residue.

### Finding 9: Hidden Touchpoints Not in Original Cascade Scope

| Component | Status | Evidence |
|---|---|---|
| `canvas/server.tsx readFeaturesJson()` + `readFeatureBySlug()` | Hidden blocker | The canvas live dashboard reads `features.json` directly via these functions. Not listed in the original cascade plan's "Critical files" section. Cascade B must either retarget these to the new epic store or break the canvas's features lens. |
| Triage evals (`eval-triage-queue-items-written-via-cli.md`, `eval-triage-resurfaces-open-queue-items.md`) | Hidden touchpoint | Both evals directly validate the intake-queue schema (`kind` field). Not in the original cascade plan's Critical files. Will fail after the schema change unless updated. |
| Cascade effort estimate | Larger than initially scoped | Agent E estimated 24–46 hours for the original "retire features.json" framing. With the unified-epic direction and these hidden touchpoints, the actual scope is plausibly 60–100 hours of focused work. |

The original plan's touchpoint list was incomplete in two specific places — the canvas server and the triage evals — and the effort estimate was optimistic because the cascade B framing was wrong. The unified-epic direction also adds work (re-homing 269 stories, migrating 18 categorical epics) that wasn't in the original plan.

### Finding 10: Impetus Rule Asymmetry — Signals Reader Inconsistency

| Component | Status | Evidence |
|---|---|---|
| Legacy `momentum:impetus` skill | Reads signals | `skills/momentum/skills/impetus/references/orient.md` + `evals/eval-impetus-handles-empty-signals.md` implement the signals/ read contract and validate empty-directory handling |
| New experimental `.claude/rules/impetus.md` | Does NOT read signals | The rule's session-start behavior reads `intake-queue.jsonl` (with the "last 5" defect) and `handoffs/`, but never mentions signals |
| Impact | Inconsistency until signals decision | Once signals/ is absorbed into practice-ledger (per Finding 6), both reader paths converge on practice-ledger and the asymmetry resolves. The new rule needs an update during cascade A3 to handle the post-absorption state. |

The asymmetry is incidental — the new rule was written before signals/ was understood — but it signals (heh) that the rule's design hasn't been validated against the full Momentum state-surface yet. Cascade A3 (Impetus rule update) should be scoped to handle this.

---

## Design Direction Captured (Pre-Decision)

The developer validated the following directions during this assessment. These will be formalized as Decision 1 (practice-ledger redesign) and Decision 2 (epic-layer consolidation) immediately after this assessment lands.

### Practice-Ledger Redesign

- **True append-only event log.** Records are immutable. Status transitions are new events appended with the same `entity_id` as the original. Whole-file rewrites are eliminated.
- **Schema:** `event_id` (immutable per row, unique), `entity_id` (identifies the logical thing; repeats across rows), `ts`, `event_type` (enum), `custom_event_type` (when event_type=custom), `source`, `actor`, `payload`.
- **Event types:** `created`, `updated`, `consumed`, `rejected`, `closed_stale`, `reopened`, `custom`. Seven total. `closed_stale` is first-class (distinct from consumed/rejected) to make attention-debt patterns queryable.
- **Closure discipline:** EVERY record has a closure condition. Time-based default: **15-day TTL**. If unresolved, auto-emit `closed_stale` event for that entity. Other closure conditions can be defined per event_type.
- **Auto-close mechanism:** `momentum-tools practice-ledger close-stale --age-days 15` invoked via Claude Code **Routines** (daily schedule) as primary, with Impetus session-start running it as defense-in-depth if the routine missed a day. Idempotent.
- **Reopen pattern:** Same `entity_id`, new `reopened` event. Preserves full attention/inattention history. Explicit human decision at triage time when duplicates are detected.
- **Signals/ absorption:** Retire `.momentum/signals/` entirely. The two signal use cases (`triage-uncleared`, `avfl-finding-pending-upstream-fix`) become entries in practice-ledger with `source: triage` / `source: avfl` and appropriate payload. Every open entry in the ledger IS the attention surface.
- **DuckDB-backed reader.** CLI subcommands: `summary`, `open`, `history --entity`, `since`, `by-source`. State queries fold events by `entity_id` to derive current status.
- **Hard-cut migration.** Existing 88 entries freeze as `practice-ledger-pre-2026-05.jsonl`. New file starts empty with the new schema. Glob-ready reader paths from day one for future rotation.
- **Impetus surfacing:** Honest counts only — "N open entries (X this week, Y older than 30 days, Z near auto-close)" + recurring patterns ("'X' has been closed_stale 4 times in 60 days"). No inline enumeration. Developer drills in via CLI when curious.

### Epic-Layer Consolidation

- **Unify the epic concept.** Drop the parallel-layer model. Single concept going forward: epic = a grouping of stories with a defined audience and lifecycle.
- **Lifecycle is a property of the epic, not a separate layer.** An epic can be **finite-lived** (deliverable with closure conditions — most current "features") or **long-lived** (ongoing thematic concern — `ad-hoc`, possibly "Stay Oriented with Impetus"). Both shapes coexist; the property is named on each epic.
- **Audience is a property:** `audience: user | internal`. Some epics ship user-visible capability; others are internal/infrastructure deliverables. The current flow/connection/quality taxonomy may survive for the user-visible ones.
- **Schema:** `epics.json` (replacing/absorbing `features.json`). LLM- and app-readable structured data. Human review/reading happens via canvas, not raw JSON.
- **Migration:** 23 current features → 23 epics in the new shape; 18 current categorical epics → some dissolve, some survive as long-lived; 269 unhomed stories → best-effort re-homing during cascade, `ad-hoc` for residue.
- **Skill restructure:** `feature-grooming` → `epic-grooming` (taking over the role of maintaining the unified epic taxonomy). `feature-breakdown` → `epic-breakdown`. Current categorical `epic-grooming` retires. Canvas updates to render epics instead of features.

---

## Recommended Next Steps

1. **Author Decision 1 — Practice-Ledger Event-Log Redesign.** Capture the schema, event types, closure discipline (15-day TTL + Routine-driven close-stale), signals/ absorption, reader CLI, hard-cut migration, and Impetus surfacing model as a ratifiable decision document. Use `momentum:decision`. Source from this assessment.
2. **Author Decision 2 — Epic-Layer Consolidation.** Capture the unification, lifecycle-as-property, audience-as-property, JSON schema, migration plan, and skill rename direction as a ratifiable decision document. Use `momentum:decision`. Source from this assessment.
3. **Create story A1 — Ledger schema + CLI redesign.** Implements the new event-log schema, CLI subcommands, DuckDB reader, hard-cut migration, Routine setup, architecture.md/PRD updates. Blocks A2, A3, A4. Use `momentum:create-story`.
4. **Create story B1 — Epic schema migration.** Establishes `epics.json`, migrates 23 features + dissolves/retains 18 categorical epics + re-homes 269 unhomed stories + retires `features.json`. Updates architecture.md/PRD/canvas references. Blocks B2, B3, B4. Use `momentum:create-story`.
5. **Create remaining stories A2/A3/A4 and B2/B3/B4 in pairs** — A2: ledger hygiene cleanup. A3: Impetus rule update for new ledger + retired signals/. A4: skill workflow updates (retro, triage, sprint-planning, etc.) to use new CLI. B2: create-story input-routing update. B3: canvas update to render epics. B4: feature-grooming/feature-breakdown → epic-grooming/epic-breakdown restructure. Run create-story in pairs of 2 per the plan's serialized-index-write constraint.
6. **Execute Cascade A in dependency order.** A1 first (in a worktree). Then A2, A3, A4 in pairs, respecting the architecture.md sole-writer constraint (only one quick-fix touching architecture.md at a time).
7. **Execute Cascade B in dependency order.** B1 first. Then B2, B3, B4 in pairs with the same constraints.
8. **Run post-cascade batch AVFL.** Single scan-profile pass on the integrated final state after all leaf stories merge, per the AVFL post-merge convention (`feedback_avfl_post_merge_strategy.md`). Worktrees stay alive until clean; bulk-remove after clean signal.

---

## Raw Data

### Agent A — Practice-Ledger arch+code audit (5 findings)

Confirmed the doc-vs-code drift in Decision 52 and Decision 1c. Located the consume code path at `momentum-tools.py:2097–2135` and documented the read-modify-write pattern with line-by-line evidence. Verified that no `findings_ledger` code exists in the codebase (zero grep matches outside research/planning artifacts), making Decision 1c's defect purely latent.

### Agent B — Practice-Ledger data+hygiene audit (4 findings)

Quantified the ledger state: 88 entries, 52 open, 36 consumed. Stale count: 12 (8 superseded + 4 test scaffolding). Newest-5 inversion: 4 of 5 are test scaffolding. Calculated the Impetus rule coverage at 9.6% (5/52 open entries surfaced). Recommended consume/reject pass and rule restructure.

### Agent C — Features↔Epics state audit (5 findings)

Schema-mapped features.json (23 features, 14 fields) and epics.md (18 epics, narrative-only). Cross-referenced with stories/index.json (410 stories) to find the 269-story coverage gap. Located DEC-031 D2's `epic-feature-collapse-closeable-grouping` story as a backlog intake stub. Confirmed both `feature-grooming` and `feature-breakdown` skills exist and operate, but neither has been updated for the M:N model DEC-031 D2 implies.

### Agent D — Signals/ infrastructure audit (6 findings)

Verified `.momentum/signals/` contains only README.md (no signal files ever written). Read FR120's contract verbatim. Grep across momentum-tools.py, retro, triage, avfl workflows confirmed zero producer code. ARCH-8 explicitly documents the producer gap. Legacy `momentum:impetus` skill's `orient.md` implements the read contract; new `.claude/rules/impetus.md` does not. Originally recommended keeping signals distinct from practice-ledger (different purposes); developer direction overrode this in favor of absorption (Finding 6 above).

### Agent E — Skill ecosystem touchpoint audit (cross-cutting)

Mapped 15 touchpoints for intake-queue.jsonl (CLI functions, skill workflows, evals, rules, docs) — classified as rename / shape-aware / reference. Mapped 11 touchpoints for features.json — classified including retire-or-restructure for feature-grooming. Identified two hidden touchpoints not in the original plan's Critical files: `canvas/server.tsx readFeaturesJson()` (high-priority dashboard blocker) and the triage evals. Estimated effort: 24–46 hours for original framing; substantially more given the unified-epic direction.
