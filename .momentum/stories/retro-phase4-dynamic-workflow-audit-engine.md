---
title: Replace retro Phase 4 auditor team with a dynamic Workflow-tool audit engine
story_key: retro-phase4-dynamic-workflow-audit-engine
status: ready-for-dev
epic_slug: momentum-sprint-retro
story_type: feature
priority: high
depends_on: []
verification_method: EDD eval
---

# Replace retro Phase 4 auditor team with a dynamic Workflow-tool audit engine

## Story

As the Momentum practice maintainer,
I want `/momentum:retro` Phase 4 (the auditor team) to run as a single dynamic **Workflow-tool** call instead of the current hand-rolled foreground-`Agent` fan-out (3 `Agent` spawns in one message, no Workflow tool),
so that the transcript audit scales its subagent count with sprint size, adversarially verifies its findings to kill false positives, and hands the main loop a structured return instead of sentinel-delimited free text — without disturbing any other retro phase or human gate.

> **Terminology:** "fan-out" in the *old* design = the main loop emitting individual `Agent` tool calls (spawning-patterns.md). In the *new* design there is no foreground `Agent` fan-out — Phase 4 is one `Workflow()` call, and concurrency happens **inside** the Workflow via its primitives: `parallel()` (a barrier — runs auditors concurrently, waits for all) and `pipeline()` (no barrier — each finding flows through verification independently). Wherever this story says "parallel auditors," read `parallel()`; wherever it says "per-finding verification," read `pipeline()`.

This is the **first adoption of the Claude Code Workflow tool's dynamic JS orchestration (`pipeline()/parallel()/agent()`) anywhere in Momentum.** It is deliberately scoped to one phase of one skill so the pattern can be proven on a contained, read-mostly surface before it spreads.

## Acceptance Criteria

1. **Phase 4 invokes the Workflow tool exactly once.** At Phase 4, the retro main loop calls the Claude Code **Workflow** tool one time with the audit script (inline `script` or a committed `scriptPath`). No foreground `Agent` fan-out for auditors/synthesizer remains in Phase 4 of `retro/workflow.md`.
2. **The audit Workflow has the three-stage shape:** `Discover` (`parallel()` lens auditors + per-story analysts) → `Verify` (`pipeline(findings, f => parallel([…skeptics]))` — each finding flows through a verify stage whose body spawns the refute panel via `parallel()`) → `Synthesize` (one `agent()` that writes the findings doc and returns structured data).
3. **Synthesize is a structural singleton.** The `Synthesize` stage is a **single `agent()` call**, never placed inside a loop, `parallel()`, or a multi-item `pipeline()` stage. Exactly one agent writes `retro-transcript-audit.md`.
4. **Structured data contract.** The audit Workflow returns JSON of shape `{ priority_action_items[], handoff_candidates[], metrics{}, doc_path }`. Phase 5 reads `priority_action_items` from this return; Phase 5.5 reads `handoff_candidates` from this return. No `*_FINDINGS_START/END` sentinel-block parsing of agent text remains anywhere in the workflow.
5. **All five human gates stay in the main loop.** Sprint pick (P1), incomplete-story F/I disposition (P3), per-stub Y/N (P5), handoff Y/N (P5.5), and the synth-failure continue prompt remain main-loop `<ask>` steps that bracket the Workflow call. The audit Workflow itself performs **no** `<ask>` / human-in-the-loop interaction (it runs in the background and returns once). The synth-failure gate has a concrete trigger from the return contract: it fires when `synthesize_status != "ok"` or `doc_path` is null/absent (see Data contract).
6. **Zero-session HALT precedes the Workflow.** The Phase 2 zero-session guard remains a main-loop HALT evaluated **before** Phase 4. When zero session files are found, the audit Workflow is **never invoked**. (Keeps both `eval-phase2-halts-on-zero-sessions` and `eval-phase2-proceeds-on-nonempty-sessions` green; the Workflow can never run on empty extracts and runs normally on non-empty ones.)
7. **Per-story parallelism scales with the sprint.** Within the Workflow's `Discover` stage, `parallel()` spawns one per-story analyst per sprint story, each scoped via `transcript-query.py sql ... --story-slugs <slug>`, so audit breadth grows with story count rather than being fixed at three auditors. The lens auditors (human, execution, review, efficiency, coordination) also run under `parallel()`. No part of Phase 4 uses the old foreground-`Agent` fan-out.
8. **Findings are adversarially verified.** In `Verify`, each candidate finding is judged by a 2–3 skeptic refute panel; a finding is dropped when a majority refute it. Surviving vs. dropped counts are `log()`-ed so suppression is visible.
9. **`retro-transcript-audit.md` is shape-stable.** The synthesized document is written to the same path (`.momentum/sprints/{slug}/retro-transcript-audit.md`) and still contains all eight sections: Executive Summary, What Worked Well, What Struggled, User Interventions, Story-by-Story Analysis, Cross-Cutting Patterns, Metrics, Priority Action Items.
10. **Untouched phases stay byte-stable.** The change set touches only Phase 4 of `retro/workflow.md`, the Phase 5 findings-ingestion action, and the new audit script file. Phases 0, 1, 2, 3, 5.5, and 6 are unchanged. (Keeps `eval-retro-phase5-routes-all-findings-to-stubs`, `eval-retro-phase5-no-distill-invocation`, `eval-produces-sprint-summary-at-retro-close`, `eval-sprint-summary-word-count-enforcement`, `eval-sprint-summary-omits-features-section-when-no-feature-status`, and `eval-no-behavior-change` green.)
11. **The four Phase-4 mechanism evals are migrated to the Workflow shape** (all four describe the obsolete "documenter" topology; two also assume `TeamCreate` — see Dev Notes "Eval drift" for the exact per-eval split):
    - `eval-phase-4-spawns-exactly-one-documenter` → **new pass condition:** exactly one `Synthesize`-stage `agent()` writes the doc; **no** assertion on total agent count (it now varies per sprint). Rename "documenter" → "synthesizer"; drop the fixed total-of-4 and the SendMessage-era Rationale.
    - `eval-phase-4-no-duplicate-tool-use-id` → retired or rewritten with rationale: under runtime-managed Workflow spawns, agents cannot share a `tool_use_id`, so the historical single-call-replication footgun is structurally impossible.
    - `eval-team-singleton-guard-halts-on-duplicate-documenter` and `eval-team-singleton-guard-passes-on-correct-composition` → reframed to assert the Workflow synth-stage singleton (one `agent()` in `Synthesize`), not a `~/.claude/teams/.../config.json` member tally.
    All eight preserved evals (AC6, AC10 lists) remain green after the change.
12. **Explicit Workflow opt-in is documented.** `retro/SKILL.md` and/or `retro/workflow.md` state that Phase 4 calls the Workflow tool, and the call site is gated to fire only after the zero-session guard passes — making the opt-in point explicit (the Workflow tool requires explicit invocation, never inferred).

## Tasks / Subtasks

- [ ] **Task 1 — Author the audit Workflow script** (AC: 2, 3, 4, 7, 8, 9) — *change type: script-code*
  - [ ] Create the script (`skills/momentum/skills/retro/audit-workflow.js`, or an inline `script` string the workflow passes to the Workflow tool). Begin with the mandatory `export const meta = { name, description, phases }` literal.
  - [ ] **Define the `args` contract** the main loop passes when invoking the Workflow (these replace the prose `{{…}}` template vars and avoid runtime date calls): `{ sprint_slug, sprint_started, sprint_completed, sprint_stories[], audit_dir, transcript_query_path }`. The script reads everything time- or scope-bound from `args` — never from `Date.now()`/`new Date()`.
  - [ ] `Discover` (`parallel()`): ~5 lens auditors (human, execution, review, efficiency, coordination) reading their shard of `audit-extracts/`, plus one per-story analyst per `args.sprint_stories` entry scoped by `transcript-query.py sql --story-slugs`. Each returns candidate findings via a `schema`.
  - [ ] `Verify` (`pipeline(findings, f => parallel([...skeptics]))`): each finding flows through a verify stage whose body spawns a 2–3 skeptic refute panel via `parallel()`; majority-refute drops it; `log()` surviving/dropped counts.
  - [ ] `Synthesize` (single `agent()`): write all 8 sections to `retro-transcript-audit.md`; `return { priority_action_items, handoff_candidates, metrics, doc_path, synthesize_status }` where `synthesize_status` is `"ok"` only if the doc was written (this is the synth-failure gate's trigger).
- [ ] **Task 2 — Rewrite Phase 4 of `retro/workflow.md`** (AC: 1, 5, 6, 12) — *change type: skill-instruction*
  - [ ] Replace the 3-auditor + synthesizer foreground spawn (~lines 250–482) with a single main-loop step that calls the Workflow tool and binds its structured return.
  - [ ] Keep the zero-session HALT in Phase 2 ahead of this call; ensure Phase 4 never runs when extracts are empty.
  - [ ] Note the explicit Workflow opt-in in the step prose and in `SKILL.md`.
- [ ] **Task 3 — Update Phase 5 (and 5.5) ingestion** (AC: 4) — *change type: skill-instruction*
  - [ ] Phase 5 reads `priority_action_items` from the Workflow return (not by re-reading/parsing the doc or sentinel blocks). Phase 5.5 reads `handoff_candidates` from the return. Preserve both gates' Y/N prompts and outputs verbatim.
- [ ] **Task 4 — Migrate the four mechanism evals; verify the preserved eight** (AC: 11) — *change type: skill-instruction (EDD eval migration — the evals are the skill's EDD harness)*
  - [ ] Rewrite `eval-phase-4-spawns-exactly-one-documenter`, retire/rewrite `eval-phase-4-no-duplicate-tool-use-id`, reframe both `eval-team-singleton-guard-*` evals to the synth-stage singleton.
  - [ ] Re-confirm the preserved evals (phase2 zero-session/​nonempty, phase5 routes-all/​no-distill, sprint-summary close/​word-count/​features-conditional, no-behavior-change) still pass against the new Phase 4.
- [ ] **Task 5 — Diff guard** (AC: 9, 10) — *change type: verification (standard DoD, no code artifact)*
  - [ ] Confirm the change set touches only Phase 4, the Phase 5/5.5 ingestion actions, the new script, and the four evals. Confirm Phases 0,1,2,3,6 and the audit-doc path/sections are unchanged.
- [ ] **Task 6 — End-to-end verification** (AC: 1–9) — *change type: verification (execution test, standard DoD)*
  - [ ] Run a real retro (or a fixture-backed dry run) against a completed sprint; confirm the audit Workflow executes, fans out per-story, verifies findings, writes the 8-section doc, and returns the contract the gates consume.

## Dev Notes

### Current state of the file being modified (read before editing — primary failure-prevention)

`skills/momentum/skills/retro/workflow.md` (785 lines, 7 phases). Anchor on the `<!-- PHASE n -->` comment headers, not line numbers (numbers below are illustrative and may drift). **Phase 4 today (the `<!-- PHASE 4 -->` block, ≈lines 250–482) is already "pure fan-out," NOT TeamCreate:** the main loop spawns 3 foreground auditors in one message (`auditor-human` → reads `user-messages.jsonl`; `auditor-execution` → `agent-summaries.jsonl` + `errors.jsonl`; `auditor-review` → `team-messages.jsonl` + reviewer-role summaries). Each returns findings as text wrapped in `HUMAN_FINDINGS_START/END`, `EXECUTION_FINDINGS_START/END`, `REVIEW_FINDINGS_START/END`. The orchestrator extracts those JSON arrays and passes them to **exactly one `synthesizer`** agent that writes `retro-transcript-audit.md`. This story replaces that interior; it does not touch the surrounding phases.

### ⚠ Eval drift already present (important)

All four Phase-4 mechanism evals are **already stale** relative to the shipped `workflow.md` (which has moved to pure fan-out with a `synthesizer` — no `TeamCreate`, no `SendMessage`, no team config file). But they are stale in two different ways — be precise when migrating:

- **`eval-team-singleton-guard-halts-on-duplicate-documenter` and `eval-team-singleton-guard-passes-on-correct-composition`** — these genuinely assume `TeamCreate` "Shape A": they tally members in `~/.claude/teams/{team}/config.json`. Reframe them to assert the Workflow synth-stage singleton; drop the `config.json`/`TeamCreate` machinery entirely.
- **`eval-phase-4-spawns-exactly-one-documenter`** — asserts a fixed spawn count (`total=4`: 1 documenter + 3 auditors). It does **not** reference `TeamCreate`/`config.json`; its staleness is the role name ("documenter"), the fixed total-of-4, and a Rationale that cites SendMessage. Migrate per AC11's new pass condition (one `Synthesize` `agent()`; no total-count assertion).
- **`eval-phase-4-no-duplicate-tool-use-id`** — asserts each spawned agent has a distinct `tool_use_id` (the single-call-replication footgun). No `TeamCreate`/`config.json` reference. Retire or rewrite: under runtime-managed Workflow spawns this is structurally impossible.

Treat "preserve evals" as "preserve the eight behavioral evals; rewrite these four mechanism evals to the new reality." Do not try to keep any `TeamCreate`/`documenter`/`config.json` assertion alive.

### Workflow tool semantics the design depends on (the hard constraints)

- A Workflow is a JS script invoked via the **Workflow tool**. `agent(prompt, {schema,label,phase})` spawns a subagent and returns its final text, or a validated object if `schema` is given. `pipeline(items, ...stages)` runs each item through all stages with **no barrier**. `parallel(thunks)` is a **barrier** (failed thunks → `null`; `.filter(Boolean)`). `log()`, `phase()`.
- **HARD: a Workflow runs in the background and RETURNS ONCE. It cannot ask the developer anything mid-run.** Therefore every retro human gate stays in the main-loop prose workflow; the Workflow is the autonomous analysis island between gates, and the main loop consumes its return (AC4, AC5). This is the documented hybrid pattern (scout inline → Workflow → main-loop gate → optional next Workflow).
- Concurrency cap ≈ `min(16, cores−2)` concurrent agents; lifetime cap 1000; a single `parallel()/pipeline()` call ≤ 4096 items. Per-story fan-out on a large sprint queues under the cap — fine.
- The Workflow tool requires **explicit** invocation (never inferred). The skill's prose is the explicit opt-in (AC12).
- `exactly-one-synthesizer` is preserved structurally by keeping `Synthesize` a single `agent()` call outside any loop/`parallel` (AC3) — this is the Workflow-native replacement for the old team-singleton guard.

### Data engine

`skills/momentum/scripts/transcript-query.py` — queries: `user-messages`, `agent-summary`, `errors`, `team-messages`, `tool-usage`, `sql`. Filters: `--after`/`--before` (UTC; `--before` end-of-day inclusive), `--story-slugs` CSV. `sql` is an arbitrary-SQL escape hatch over the DuckDB view; it is how per-story analysts scope their shard (AC7). Auditors must stream/scope large files (`agent-summaries.jsonl`, `errors.jsonl`) via SQL rather than full-Read.

### Data contract (main loop ↔ Workflow)

**Inputs — the `args` the main loop passes into the Workflow** (these carry the values today's prose holds in `{{…}}`; passing them as `args` also satisfies the no-runtime-date rule):
```json
{ "sprint_slug", "sprint_started", "sprint_completed", "sprint_stories": [], "audit_dir", "transcript_query_path" }
```

**Return — what the Workflow hands back:**
```json
{
  "priority_action_items": [{ "title", "priority", "source_detail", "suggested_ac": [], "epic_slug" }],
  "handoff_candidates":    [{ "title", "slug", "description", "epic_slug?", "failure_diagnosis?", "feature_state_transition?" }],
  "metrics": { "user_msgs", "subagents", "errors", "team_msgs", "struggles", "successes" },
  "doc_path": ".momentum/sprints/{slug}/retro-transcript-audit.md",
  "synthesize_status": "ok"
}
```
Phase 5's stub gate iterates `priority_action_items`; Phase 5.5's handoff gate iterates `handoff_candidates`. The Phase-4 synth-failure `<ask>` fires when `synthesize_status != "ok"` or `doc_path` is null/absent — the contract is the gate's only trigger (the main loop no longer inspects the filesystem for the doc). Both downstream gates and their outputs are otherwise unchanged.

### Sole-writer / authority boundaries to respect

The audit Workflow is **read-mostly**: it reads `audit-extracts/`, runs `transcript-query.py`, and writes exactly one artifact (`retro-transcript-audit.md`). It must **not** mutate `stories/index.json` or `sprints/index.json` (sprint-manager / momentum-tools are sole writers) and must **not** call `momentum-tools` sprint-state transitions — those stay in the main loop (Phases 3, 5, 6). No `isolation:'worktree'` is needed (no parallel conflicting file writes).

**Note on Phase 5's existing `stories/index.json` write:** Phase 5 writes approved stubs directly to `stories/index.json`. That is a **pre-existing, sanctioned exception** — retro's own `<critical>` in `workflow.md` authorizes it ("Write stub entries directly to stories/index.json (no momentum-tools command exists for this operation)"). AC10 keeps Phase 5 byte-stable, so this story neither introduces nor removes that write; it stays in the main loop (never the Workflow). Do not "fix" it as part of this story.

### Files in scope

- `skills/momentum/skills/retro/workflow.md` — Phase 4 rewrite + Phase 5/5.5 ingestion edit.
- `skills/momentum/skills/retro/audit-workflow.js` (new) — the audit Workflow script (or inline in workflow.md).
- `skills/momentum/skills/retro/SKILL.md` — note the Workflow opt-in (and keep the ~500-line / frontmatter conventions per the agent-skill development guide).
- `skills/momentum/skills/retro/evals/` — migrate the four mechanism evals.

### Project Structure Notes

Retro lives at `skills/momentum/skills/retro/`. Stories live in `.momentum/stories/`; sprint state in `.momentum/sprints/`; the practice ledger is written via `momentum-tools.py practice-ledger append` (Phase 5.5, unchanged). The new script is the first Workflow-tool script in the repo — keep it self-contained and JS (not TS); avoid `Date.now()/Math.random()/new Date()` in the script body per Workflow constraints.

### References

- Current retro workflow (the file being modified): `skills/momentum/skills/retro/workflow.md` — locate sections by their `<!-- PHASE 4 -->` / `<!-- PHASE 5 -->` comment headers (line numbers ≈250–482 / ≈484–533 are illustrative only)
- Retro evals (4 to migrate, 8 to preserve): `skills/momentum/skills/retro/evals/`
- Data engine: `skills/momentum/scripts/transcript-query.py` (QUERIES at line 679)
- Practice-ledger CLI (Phase 5.5, unchanged): `skills/momentum/scripts/momentum-tools.py` (`practice-ledger append`)
- Conductor (the DEC-035/036 "autonomous span between human touchpoints" idiom this mirrors): `skills/momentum/skills/conductor/workflow.md`, `.../conductor/SKILL.md`
- Spawning patterns rule: `~/.claude/rules/spawning-patterns.md` (fan-out vs TeamCreate decision)
- Agent/skill development conventions (frontmatter, ~500-line limit): `skills/momentum/references/agent-skill-development-guide.md`
- Epic context: `momentum-sprint-retro` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 2, 3, 4 → `skill-instruction` (EDD)
- Task 1 → `script-code` (TDD / execution test)
- Tasks 5–6 → verification activities (standard bmad-dev-story DoD)

**Verification method (frozen contract):** `EDD eval` **governs** this story — the primary deliverable is the retro skill's audit *behavior*. Per Verification Standard §1 multi-type clause, the `script-code` Task 1 (`audit-workflow.js`) **additionally** requires an **Execution test**: run the audit Workflow against fixture `audit-extracts/` and confirm it (a) returns the `{ priority_action_items, handoff_candidates, metrics, doc_path }` contract and (b) writes the 8-section `retro-transcript-audit.md`. This per-task secondary method is the written justification required by Verification Standard §2.

---

### skill-instruction Tasks (2, 3, 4): Eval-Driven Development (EDD)

**Do NOT use TDD for `workflow.md`/`SKILL.md`** — skill instructions are non-deterministic LLM prompts. Use EDD:

1. **Evals first.** This story is unusual: it **migrates** existing evals rather than only adding new ones. The four mechanism evals in `skills/momentum/skills/retro/evals/` (see Dev Notes "Eval drift") are rewritten to the Workflow shape **before** the Phase 4 rewrite; the eight behavioral evals must stay green. Treat the whole `skills/momentum/skills/retro/evals/` suite as the EDD harness.
2. **Implement.** Rewrite Phase 4 of `retro/workflow.md`, update Phase 5/5.5 ingestion, note the Workflow opt-in in `retro/SKILL.md`.
3. **Verify.** For each eval, spawn a subagent with the eval scenario + the revised skill files as context; confirm behavior matches. Max 3 diagnose→revise cycles, then surface.

**NFR compliance (mandatory for the skill-instruction tasks):**
- `retro/SKILL.md` `description` ≤ 150 characters — count precisely (the current description is long; do not exceed the cap if you edit it).
- `model:` and `effort:` frontmatter present and correct in `retro/SKILL.md`.
- `retro/workflow.md` (and `SKILL.md`) body ≤ 500 lines / 5000 tokens — the Phase 4 rewrite should make workflow.md **shorter**, not longer (the audit script absorbs the 3 verbose auditor prompts). If the inline script would push it over, put the script in `audit-workflow.js` and reference it.
- `momentum:` namespace preserved.

**DoD additions (skill-instruction):**
- [ ] The 4 mechanism evals migrated to the Workflow shape; the 8 behavioral evals re-run and green.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented).
- [ ] `retro/SKILL.md` description ≤150 chars; `model:`/`effort:` present; bodies ≤500 lines.
- [ ] AVFL checkpoint on the changed skill documented (momentum:dev runs this).

### script-code Task (1): Execution test (the audit Workflow script)

The audit Workflow is **JS for the Claude Code Workflow tool** — the first such script in the repo. "Tests" here = an **execution test**, not unit tests over prompt text:

1. **Author** `skills/momentum/skills/retro/audit-workflow.js` (or an inline `script` string). Begin with the mandatory `export const meta = { name, description, phases }` literal. Stages: `Discover` (`parallel()`), `Verify` (`pipeline()`), `Synthesize` (single `agent()`).
2. **Execute** against fixture `audit-extracts/` (reuse a real completed sprint's extracts). Assert: the structured return matches the contract; exactly one agent wrote the doc; the doc has all 8 sections; surviving/dropped finding counts are logged.
3. **Constraints:** self-contained **JS** (not TS); no `Date.now()`/`Math.random()`/`new Date()` in the script body (Workflow resume constraint — stamp timestamps from the caller or via `args`); read-mostly (no `stories/index.json`/`sprints/index.json` writes; no `momentum-tools` sprint transitions).

**DoD additions (script-code):** execution test passes against fixture extracts; no regression in the preserved evals; the script never mutates sprint/story state.

**Gherkin separation (Decision 30):** Any `.feature` specs under `sprints/{sprint-slug}/specs/` are **off-limits** to the dev agent — implement against the plain-English ACs in this story only, never against `.feature` files.

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
