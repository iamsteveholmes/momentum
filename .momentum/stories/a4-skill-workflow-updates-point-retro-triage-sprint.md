---
title: "A4: Skill workflow updates — point retro/triage/sprint-planning/intake/feature-breakdown at the new practice-ledger CLI"
story_key: a4-skill-workflow-updates-point-retro-triage-sprint
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: practice
change_type:
  - skill-instruction
  - specification
verification_method: skill eval
harness_profile: default
depends_on:
  - a1-practice-ledger-schema-cli-redesign-true-append-only
touches:
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/triage/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/feature-breakdown/workflow.md
  - skills/momentum/skills/triage/evals/eval-triage-queue-items-written-via-cli.md
  - skills/momentum/skills/triage/evals/eval-triage-resurfaces-open-queue-items.md
  - skills/momentum/skills/triage/evals/eval-triage-no-distill-delegation.md
  - skills/momentum/skills/intake/evals/eval-intake-routes-discovered-work-with-discovered-from.md
  - skills/momentum/skills/retro/evals/eval-retro-phase5-no-distill-invocation.md
---

# A4: Skill workflow updates — point retro/triage/sprint-planning/intake/feature-breakdown at the new practice-ledger CLI

## Story

As a Momentum developer,
I want every skill workflow that currently invokes `momentum-tools.py intake-queue …` to invoke the new `momentum-tools.py practice-ledger …` CLI with the renamed schema fields and event-type taxonomy from DEC-033,
So that producer skills stop drifting from A1's redesigned event log, the new CLI surface is the only path skills know, and the cascade closes cleanly without legacy invocations lingering in the practice.

## Description

DEC-033 redesigns the practice ledger as a true append-only event log (A1). A1 ships the new CLI surface (`momentum-tools.py practice-ledger {summary,open,history,since,by-source,close-stale,append}`) plus the new schema (`event_id`, `entity_id`, `ts`, `event_type` from the seven-value enum, `source`, `actor`, `payload`, optional `custom_event_type`). The old `intake-queue` subcommand and its mutable-row schema (kind/status fields, whole-file-rewrite consume) are removed by A1.

This story is the producer-side sweep: it updates every skill workflow that calls the ledger to use the new CLI invocations and the new schema vocabulary, and it updates the affected skill evals so the eval scaffold validates against the new surface rather than the old.

**Affected skill workflows (per AES-003 Findings 6 and 9; confirmed via `grep -rln 'intake-queue' skills/momentum/`):**

1. `skills/momentum/skills/retro/workflow.md` — Phase 5.5 handoff: `intake-queue append --source retro --kind handoff …` → `practice-ledger append --source retro --event_type created …` (kind:handoff becomes a `created` event with `source: retro` and a payload field indicating handoff origin; the `kind` field no longer exists in the new schema). 14 references in this file.
2. `skills/momentum/skills/triage/workflow.md` — Capture path for SHAPING/DEFER/REJECT classes (the three classes that don't delegate to intake/decision) and the resurfacing read path. 25 references — the heaviest-touched file. Both the writer invocations and the classification-table action column ("Write `kind: shape` event to `intake-queue.jsonl`") must update to the new schema where event_type replaces kind.
3. `skills/momentum/skills/sprint-planning/workflow.md` — Handoff queue read for sprint planning input. 6 references.
4. `skills/momentum/skills/intake/workflow.md` — Single reference; ARTIFACT capture path from triage delegation.
5. `skills/momentum/skills/feature-breakdown/workflow.md` — 5 references.

**Affected evals:**

6. `skills/momentum/skills/triage/evals/eval-triage-queue-items-written-via-cli.md` — assertions about the CLI invocation shape; rewrite for `practice-ledger append --event_type …`.
7. `skills/momentum/skills/triage/evals/eval-triage-resurfaces-open-queue-items.md` — assertions about reading "open" items; rewrite for the new derived-state semantics (open = entity whose last event is non-terminal) via `practice-ledger open`.
8. `skills/momentum/skills/triage/evals/eval-triage-no-distill-delegation.md` — single mention; align vocabulary.
9. `skills/momentum/skills/intake/evals/eval-intake-routes-discovered-work-with-discovered-from.md` — 3 references; align vocabulary.
10. `skills/momentum/skills/retro/evals/eval-retro-phase5-no-distill-invocation.md` — single mention; align vocabulary.

**Architecture and PRD:** Out of scope. A1 already updates `architecture.md` (Decisions 52 + 1c + `.momentum/` State Layout + Read/Write Authority table) and `prd.md` (FR114/115/116/117/120). A4 is producer-skill scope only.

**Scope correction vs. stub:** The original intake stub title named seven skills (retro, triage, sprint-planning, intake, decision, assessment, feature-breakdown). A pre-story audit (`grep -rln 'intake-queue' skills/momentum/skills/`) confirmed that the `decision` and `assessment` skill workflows contain zero `intake-queue` references and are therefore excluded from this story's scope. The five workflows enumerated above are the complete producer set; the stub's broader list reflected conversational guessing, not a code audit.

**Pain context:** Multi-skill update sweep per AES-003 Findings 6 and 9. Depends on A1's CLI surface landing. After A4 merges, no Momentum skill workflow can reference the legacy `intake-queue` CLI or the legacy `kind` field.

## Acceptance Criteria

### CLI subcommand rename — writer side

1. Every invocation of `python3 skills/momentum/scripts/momentum-tools.py intake-queue append …` across all five workflow.md files (retro, triage, sprint-planning, intake, feature-breakdown) is replaced with `python3 skills/momentum/scripts/momentum-tools.py practice-ledger append …`. Verified by `grep -l 'intake-queue append' skills/momentum/skills/*/workflow.md` returning zero matches after the story merges.
2. Every flag passed to the renamed `append` invocations is translated to the new schema: `--kind <value>` is removed; `--event_type <value>` is used in its place; the value taxonomy follows DEC-033 D3 (`created`/`updated`/`consumed`/`rejected`/`closed_stale`/`reopened`/`custom`). The old `--kind handoff`/`--kind shape`/`--kind watch`/`--kind rejected`/`--kind capture` etc. flags do not appear anywhere in the five workflow files after the story merges.
3. Where the legacy `kind` value carried semantics that don't map cleanly to one of the seven event types (e.g., `kind: handoff` from retro Phase 5.5), the migration uses `event_type: created` plus a payload field that preserves the original semantic (e.g., `--payload-json '{"intent":"handoff","origin_skill":"retro"}'`). The mapping is documented as a comment at the top of the producing workflow step.

### CLI subcommand rename — reader side

4. Every read-side invocation that previously used `intake-queue list …` is replaced with the appropriate `practice-ledger` reader subcommand from DEC-033 D7: `practice-ledger open` for "currently open entries", `practice-ledger by-source <source>` for source-filtered reads, `practice-ledger history --entity <id>` for full per-entity history, `practice-ledger since <ts>` for change-since queries, `practice-ledger summary` for counts. Verified by `grep -l 'intake-queue list' skills/momentum/skills/*/workflow.md` returning zero matches after the story merges.
5. The retro Phase 5.5 verification step (currently `intake-queue list --source retro --kind handoff --status open` in `retro/workflow.md` line 648 region) is rewritten as `practice-ledger by-source retro` filtered to non-terminal entities (or equivalent that achieves the same observable check — "did the handoff events land?").
6. The triage resurface path (currently reads open queue items) is rewritten using `practice-ledger open`. The output shape consumed by triage is the new derived-state output (entity_id + last event), not the legacy `kind`/`status` row shape.

### Classification-table semantics in triage

7. The Classification Table in `skills/momentum/skills/triage/workflow.md` (the `| Class | Meaning | Downstream action |` table near the top of the file) is updated so the "Downstream action" column references `event_type` values from the new enum instead of `kind:` strings. SHAPING/DEFER/REJECT classes' downstream actions become: SHAPING → `event_type: created` with payload `{"triage_class":"shaping"}`; DEFER → `event_type: created` with payload `{"triage_class":"defer"}`; REJECT → `event_type: rejected` with payload `{"reason":"…"}` populated from triage. (REJECT is the only class that maps to a terminal event type natively; the other two are non-terminal `created` events with classification carried in payload — this keeps "shaping/defer" entities visible via `practice-ledger open`.)
8. Any helper text in triage workflow steps that references `kind: shape` / `kind: watch` / `kind: rejected` strings is updated to the new event_type + payload pattern from AC7. No `kind:` string remains in `triage/workflow.md` after the story merges (verified by grep).

### File-path references

9. Every workflow.md mention of the bare filename `.momentum/intake-queue.jsonl` (in prose, log messages, completion summaries) is updated to `.momentum/practice-ledger.jsonl`. Glob references that should match both files use `practice-ledger*.jsonl`. Verified by `grep -l 'intake-queue\.jsonl' skills/momentum/skills/*/workflow.md` returning zero matches.
10. The retro completion summary (currently "events written to intake-queue.jsonl") and the triage capture-step completion summary are both updated to reference `practice-ledger.jsonl` and the new event_type vocabulary.

### Eval files

11. `eval-triage-queue-items-written-via-cli.md` is rewritten so the assertions exercise the new CLI surface: setup invokes `practice-ledger append --event_type created --source triage --payload-json '{"triage_class":"shaping"}'`; the verification reads via `practice-ledger by-source triage` and asserts the appended event appears with the expected event_type and payload. The eval no longer references `kind` anywhere.
12. `eval-triage-resurfaces-open-queue-items.md` is rewritten so "open" is defined as the new derived-state notion (entity_id whose last event is non-terminal). The eval asserts that `practice-ledger open` surfaces a SHAPING entity written in the setup step, and that the same entity disappears from `practice-ledger open` output after a `--event_type consumed` event is appended for the same entity_id.
13. `eval-triage-no-distill-delegation.md`, `eval-intake-routes-discovered-work-with-discovered-from.md`, and `eval-retro-phase5-no-distill-invocation.md` are each updated to align their CLI references and field-name references with the new schema. Where these evals previously asserted on `kind`/`status` fields, they now assert on `event_type`/derived-state.

### Discipline: no legacy surface remains

14. After the story merges, `grep -rn 'intake-queue' skills/momentum/skills/` returns zero matches in the five workflow files and the five eval files listed in this story's `touches`. (Matches in `skills/momentum/scripts/momentum-tools.py` test fixtures preserving pre-2026-05 archive read are owned by A1 and out of scope here. The underscore variant `intake_queue` does not appear in any source file — verified by pre-story audit — so the grep pattern is the hyphenated form only.)
15. After the story merges, `grep -rnE 'kind:\s*(shape|watch|rejected|handoff)' skills/momentum/skills/` returns zero matches in the five workflow files and five eval files listed in this story's `touches`. (The four enum values listed are the actual legacy `kind` values found in the pre-story audit. References to the literal string "kind" in unrelated prose contexts — e.g., "what kind of work" — are acceptable; the grep target is the structured `kind: <enum-value>` pattern. Note the `-E` flag — ERE syntax is required for the alternation to work correctly.)

### Verification

16. For each of the five updated workflow.md files, at least one eval from that skill's `evals/` directory (or a newly-added eval) demonstrates the new CLI invocation succeeds end-to-end against the A1 ledger and produces the expected derived-state output. The eval list invoked for this story's verification is the five eval files in `touches` plus any newly added evals.
17. A manual smoke pass is documented in the story's completion notes: one retro Phase 5.5 invocation, one triage SHAPING capture, and one sprint-planning handoff queue read are executed against a local practice-ledger.jsonl seeded by A1's `append` CLI, and the resulting derived state matches the AC expectations. Smoke-pass output is captured in the Dev Agent Record.

## Tasks / Subtasks

- [ ] **Task 1 — Audit current ledger surface in producer skills (skill-instruction)**
  - [ ] Run `grep -rn 'intake-queue\|intake_queue' skills/momentum/skills/` and capture the full reference list as the change baseline. Cross-reference against the five workflow files and five eval files in `touches`; flag any newly-discovered file as a scope question for the developer.
  - [ ] For each reference, note whether it is a writer invocation, a reader invocation, a prose mention, or a field-name reference. The mix determines per-step edit strategy.
  - [ ] Re-read DEC-033 §D3 (event_type enum) and §D7 (reader subcommands) to lock the target vocabulary.

- [ ] **Task 2 — Update `skills/momentum/skills/triage/workflow.md` (skill-instruction)**
  - [ ] Update the Classification Table downstream-action column per AC7.
  - [ ] Update every writer invocation in steps that handle SHAPING/DEFER/REJECT to use `practice-ledger append --event_type … --payload-json …`. Use `event_type: created` for non-terminal classes and carry the class label in payload; use `event_type: rejected` for REJECT.
  - [ ] Update the resurface read step to use `practice-ledger open` and consume its derived-state output shape.
  - [ ] Update prose, log messages, and step completion outputs to reference `practice-ledger.jsonl` and event_type vocabulary.
  - [ ] Verify with grep that no `intake-queue`, no `intake_queue`, and no `kind: <enum-value>` patterns remain in this file.

- [ ] **Task 3 — Update `skills/momentum/skills/retro/workflow.md` (skill-instruction)**
  - [ ] Update Phase 5.5 (line 554 region) writer invocations: `--kind handoff` → `--event_type created --payload-json '{"intent":"handoff","origin_skill":"retro"}'`. Apply to both the per-finding loop and any one-shot batch invocations.
  - [ ] Update the post-write verification step (line 648 region) to use `practice-ledger by-source retro` (filter to non-terminal in the workflow step rather than asking the CLI to filter on the legacy `--status open` flag).
  - [ ] Update the Phase 5.5 narrative comment (line 46 region) and the completion summary (line 766 region) to reference `practice-ledger.jsonl` and the new event_type vocabulary.
  - [ ] Verify with grep that no `intake-queue`, no `intake_queue` remain in this file.

- [ ] **Task 4 — Update `skills/momentum/skills/sprint-planning/workflow.md` (skill-instruction)**
  - [ ] Replace the six `intake-queue` references with the appropriate `practice-ledger` invocations. The sprint-planning handoff-queue read is the primary use case — map it to `practice-ledger open` or `practice-ledger by-source retro` depending on whether the workflow wants all open entities or only retro-sourced handoffs.
  - [ ] Update any prose that names the file.

- [ ] **Task 5 — Update `skills/momentum/skills/intake/workflow.md` and `skills/momentum/skills/feature-breakdown/workflow.md` (skill-instruction)**
  - [ ] intake: single reference — convert in place.
  - [ ] feature-breakdown: five references — apply the same writer/reader rename pattern as the larger files.
  - [ ] Verify both files clean under grep.

- [ ] **Task 6 — Update triage evals (specification)**
  - [ ] Rewrite `eval-triage-queue-items-written-via-cli.md` per AC11: setup uses new CLI; assertions exercise `event_type` and payload fields, not `kind`.
  - [ ] Rewrite `eval-triage-resurfaces-open-queue-items.md` per AC12: "open" defined as derived state; assertions read via `practice-ledger open` and verify disappearance on `consumed` event append.
  - [ ] Update `eval-triage-no-distill-delegation.md` vocabulary alignment.

- [ ] **Task 7 — Update intake + retro evals (specification)**
  - [ ] Update `eval-intake-routes-discovered-work-with-discovered-from.md` (3 references): align CLI and field-name references to new schema.
  - [ ] Update `eval-retro-phase5-no-distill-invocation.md` (single reference): align vocabulary.

- [ ] **Task 8 — Run skill evals end-to-end and capture smoke pass (skill-instruction)**
  - [ ] For each of the five updated workflow files, invoke its skill's eval suite against a local practice-ledger seeded by A1's CLI. Confirm each eval passes.
  - [ ] Execute the manual smoke pass from AC17: one retro Phase 5.5, one triage SHAPING capture, one sprint-planning handoff read. Capture output in the Dev Agent Record completion notes.
  - [ ] Run the final discipline-grep (AC14, AC15) against the touched files — both must return zero matches.

- [ ] **Task 9 — Update the story `touches` list if Task 1 surfaced new files (specification)**
  - [ ] If Task 1's grep audit found in-scope `intake-queue` references in files not listed in this story's `touches`, surface that to the developer before editing. Either extend `touches` (preferred — keeps the discipline-grep AC14 honest) or scope-bound the discovery as a follow-up story.

## Dev Notes

### Architecture Compliance

- DEC-033 is the controlling decision. D1 (append-only), D2 (schema), D3 (event_type enum), D7 (reader CLI surface) are the authoritative source for vocabulary and invocation shape.
- A1's index entry (`a1-practice-ledger-schema-cli-redesign-true-append-only`) lists the new CLI surface in its `touches` — A4 is the consumer of the surface A1 produces. If A1's final CLI shape diverges from DEC-033 D7 during implementation (e.g., an additional flag, a renamed subcommand), A4 picks up the divergence here and updates accordingly. A1 is authoritative on CLI shape; A4 mirrors.
- Architecture.md and PRD.md updates are A1's responsibility (per A1's touches). A4 does NOT edit those files. If A4's audit reveals architecture/PRD references that A1 missed, raise as a defect against A1 — do not patch in A4 scope.
- Producer-skill responsibility per DEC-033 D4: every appended event must have a closure path. The new `created` events written from SHAPING/DEFER classes are subject to the 15-day TTL `closed_stale` policy via A1's `close-stale` routine — producers do not need to emit explicit closure events from this story; the TTL handles it.

### Testing Requirements

- Verification method: `skill eval`. For each touched skill, the eval suite invokes the workflow step that calls the ledger and asserts on the CLI surface used and the resulting derived state.
- Per-file evals required:
  - retro Phase 5.5 — `eval-retro-phase5-no-distill-invocation.md` covers the no-distill assertion; a fresh assertion covering "Phase 5.5 invokes `practice-ledger append --event_type created --source retro`" is added inside the existing eval or in a sibling eval as the dev judges cleaner.
  - triage SHAPING capture — `eval-triage-queue-items-written-via-cli.md` (rewritten).
  - triage open-resurface — `eval-triage-resurfaces-open-queue-items.md` (rewritten).
  - intake ARTIFACT capture — `eval-intake-routes-discovered-work-with-discovered-from.md` (rewritten).
- AC14/AC15 discipline-grep is part of the verification checklist. Run grep both before-and-after; capture counts in the Dev Agent Record.
- AC17 smoke pass: execute against a temp `.momentum/practice-ledger.jsonl` (NOT the real one) to avoid polluting the practice. Use a throwaway directory or a worktree.

### Implementation Guide

**Change types in this story:** `skill-instruction` (5 workflow.md files), `specification` (5 eval markdown files).

**Per change-type approach:**

- **skill-instruction edits (workflow.md):** these are agentic-engineering skill files that the dev-skills rule (`.claude/rules/dev-skills.md`) puts under `skills/momentum/references/agent-skill-development-guide.md` authority. Before editing any workflow.md, the dev agent must read that reference guide and follow its conventions for `<step>` / `<action>` / `<critical>` / `<note>` XML semantics, invocation control, and structure rules. Edits are surgical — only the CLI invocations, field names, and prose strings that mention `intake-queue` / `kind:` change. Do not refactor surrounding step logic.
- **specification edits (eval markdown):** eval files describe assertions and setup/teardown for skill evaluation. Their structure is dictated by `skills/momentum/references/skill-evals-guide.md` (or the canonical reference in `references/` if path differs). Read the existing eval files first to mirror their shape — same headings, same assertion format, same setup pattern.

**EDD reminder (skill-instruction discipline):** for each updated workflow.md, the corresponding eval must pass end-to-end before the file is considered done. The eval is the spec; the workflow is the implementation. If an eval is not present for a touched skill step, add one (preferred) or document the gap (acceptable) in the completion notes.

**Decision 30 black-box reminder:** Gherkin specs for this sprint live in `.momentum/sprints/sprint-2026-05-26/specs/` and are off-limits to the dev agent. The dev agent implements against the plain-English ACs in this story file only — never against `.feature` files.

**Vocabulary mapping cheat sheet (DEC-033 D3 + A1 CLI):**

| Legacy (intake-queue) | New (practice-ledger) |
|---|---|
| `intake-queue append --kind handoff --source retro` | `practice-ledger append --event_type created --source retro --payload-json '{"intent":"handoff"}'` |
| `intake-queue append --kind shape --source triage` | `practice-ledger append --event_type created --source triage --payload-json '{"triage_class":"shaping"}'` |
| `intake-queue append --kind watch --source triage` | `practice-ledger append --event_type created --source triage --payload-json '{"triage_class":"defer"}'` |
| `intake-queue append --kind rejected --source triage --reason "…"` | `practice-ledger append --event_type rejected --source triage --payload-json '{"reason":"…"}'` |
| `intake-queue list --status open` | `practice-ledger open` |
| `intake-queue list --source retro --kind handoff --status open` | `practice-ledger by-source retro` (workflow filters to non-terminal) |
| `intake-queue list --status open --limit 5` | drop — Impetus uses `practice-ledger summary` per A3 |

If A1's actual CLI surface diverges from this cheat sheet, A1's surface wins — update this section as a clarification, not as a re-spec.

### Project Structure Notes

- All five workflow.md files live under `skills/momentum/skills/<skill-name>/workflow.md`.
- All five eval files live under `skills/momentum/skills/<skill-name>/evals/<eval-name>.md`.
- No new files are created by this story. No deletions either.
- The dev-skills rule (`.claude/rules/dev-skills.md`) makes `skills/momentum/references/agent-skill-development-guide.md` authoritative for any SKILL.md / workflow.md / agent-definition edits — confirm that file is read before the first workflow.md edit in this story.

### References

- DEC-033 — Practice-Ledger Event-Log Redesign (`_bmad-output/planning-artifacts/decisions/dec-033-practice-ledger-event-log-redesign-2026-05-25.md`)
- AES-003 — Practice-Ledger Defects + Epic Unification (`_bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md`) — Findings 6 and 9 are the producer-skill drift findings this story closes.
- Cascade Plan — `.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md` — A1→A4 dependency edge documented here.
- A1 story — `.momentum/stories/a1-practice-ledger-schema-cli-redesign-true-append-only.md` — the CLI-surface contract A4 consumes.
- Dev-skills authority — `.claude/rules/dev-skills.md` → `skills/momentum/references/agent-skill-development-guide.md`.
- Triage handoff that originated A4 — `.momentum/handoffs/practice-ledger-and-epic-cascade-stories-2026-05-25.md`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
