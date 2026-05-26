# Triage Handoff — Practice-Ledger + Epic-Layer Cascade Stories

**Date:** 2026-05-25
**For:** `momentum:triage`
**Source decisions:** DEC-033 (Practice-Ledger Event-Log Redesign), DEC-034 (Epic-Layer Consolidation)
**Source assessment:** AES-003
**Plan reference:** `~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md`
**Process story:** `practice-ledger-features-epics-cascade-sequenced-plan` (status: in-progress)

---

## Triage Instructions

This handoff contains **8 observations** that should all classify as **ARTIFACT** (concrete stories to be created). They derive from two formally-decided architectural decisions (DEC-033 + DEC-034) — the deliberation is done; triage's job is classification + enrichment + delegation to `momentum:intake` for stub creation.

**Default for all 8:**
- Classification: `ARTIFACT`
- Source: `decision` (both DEC-033 and DEC-034 are upstream)
- Epic: `ad-hoc` (per the existing convention for cascade-originated work; can be re-homed later via epic-grooming once DEC-034's epic-layer consolidation lands)
- Priority: see per-story below
- Story type: see per-story below
- Change type: see per-story below — note that some are software engineering (need dev pipeline) and some are context engineering (would benefit from a lighter execution path; per the developer, that routing distinction is a future create-story enhancement, not in scope for this batch)
- Dependencies: see per-story below

**Cross-cutting dependencies:**
- A1 BLOCKS A2, A3, A4 (they consume the new CLI or the renamed file)
- B1 BLOCKS B2, B3, B4 (they depend on epics.json being the new source of truth)
- Cascade A and Cascade B are mutually independent — interleave or run in parallel

**Concurrency constraint (already in the plan):** create-story sessions run in pairs of 2 max (serialized index registration). Quick-fix sessions run in pairs of 2 max (serialized register/complete; only 1 touching architecture.md at a time).

**Doc updates folded into each story** (per developer choice during planning) — architecture.md, prd.md, epics.md updates land with the implementation story that drove them, not as a separate final doc-cleanup story.

---

## Observation 1 — A1: Ledger schema + CLI redesign

**Title:** A1: Practice-ledger schema + CLI redesign — true append-only event log

**Description:** Implement DEC-033 D1–D8 + D10. Rename `.momentum/intake-queue.jsonl` to `.momentum/practice-ledger.jsonl`. Rewrite the schema: `event_id` (immutable per row, unique), `entity_id` (repeats per logical thing), `ts`, `event_type` enum (`created`/`updated`/`consumed`/`rejected`/`closed_stale`/`reopened`/`custom`), `custom_event_type` (when custom), `source`, `actor`, `payload`. Implement append-only writer (`open('a')`, O_APPEND) for all writes — no whole-file rewrites. Implement DuckDB-backed reader CLI subcommands: `summary`, `open`, `history --entity`, `since`, `by-source`. Implement `close-stale --age-days <N>` CLI command for the TTL closure path. Set up Claude Code Routine (via CronCreate) to invoke close-stale daily. Hard-cut migration: freeze existing 88 entries as `.momentum/practice-ledger-pre-2026-05.jsonl`; new file starts empty under new schema. Update architecture.md (Decision 52 rewrite, Decision 1c amendment with pointer to DEC-033, State Layout, Read/Write Authority table). Update prd.md (FR115 rewrite; FR114/116/117 reference updates).

**Source:** decision (DEC-033)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** practice
**Suggested change_type:** script-code (Python CLI), specification (architecture.md + prd.md updates), config-structure (data migration)
**Suggested priority:** high
**Dependencies:** none (foundation story; blocks A2, A3, A4)
**Effort estimate:** 6–10 hours (biggest implementation lift in the cascade)
**Verification approach (per DEC-029):** EDD eval for the CLI subcommands + Execution test for the migration; harness_profile: default

---

## Observation 2 — A2: Ledger hygiene cleanup

**Title:** A2: Practice-ledger hygiene cleanup — close 12 stale entries

**Description:** Implement the one-time hygiene pass referenced in AES-003 Finding 3. Using the new CLI from A1, append `consumed` events for the 10 entries with "superseded by DEC-..." in titles (outcome_ref: `"superseded:<dec-id>"`), the 3 entries with "Test:" prefix or "Old triage-inbox.md approach" (outcome_ref: `"test-leftover"`). Verify post-cleanup that `momentum-tools practice-ledger open` returns the expected reduced count. This may be implementable as a shell script or just a sequence of CLI invocations — the work is data hygiene, not new code.

**Source:** decision (DEC-033, AES-003 Finding 3)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** maintenance
**Suggested change_type:** config-structure (data operation; minimal/no code)
**Suggested priority:** medium
**Dependencies:** A1 (requires the new CLI)
**Effort estimate:** 1–2 hours
**Verification approach:** Smoke test (run the CLI calls, confirm count drops); harness_profile: default

---

## Observation 3 — A3: Impetus rule update for new ledger + retired signals/

**Title:** A3: Impetus rule update — honest counts, new ledger, retired signals

**Description:** Implement DEC-033 D9 in the experimental `.claude/rules/impetus.md`. Drop the "last 5" instruction (currently surfaces 80% test scaffolding per AES-003 Finding 4). Replace with honest count surfacing: "N open entries (X this week, Y older than 30 days, Z near auto-close)" plus recurring patterns from history. Use the new `momentum-tools practice-ledger summary` CLI. Update the "where state lives" table to point at `practice-ledger.jsonl` (not intake-queue.jsonl). Remove any references to `.momentum/signals/` (retired per DEC-033 D6). Document the subagent guard remains.

**Source:** decision (DEC-033, AES-003 Findings 4 and 10)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** practice
**Suggested change_type:** rule-hook (the rule file IS the implementation)
**Suggested priority:** high
**Dependencies:** A1 (requires the new CLI's `summary` subcommand)
**Effort estimate:** 1–2 hours
**Verification approach:** Behavioral trigger test (open a fresh session, observe Impetus's session-start output matches the new pattern); harness_profile: default

---

## Observation 4 — A4: Skill workflow updates for new ledger CLI

**Title:** A4: Skill workflow updates — point retro/triage/sprint-planning/intake/decision/assessment/feature-breakdown at the new CLI

**Description:** Update the workflow.md files for skills that invoke the intake-queue CLI to use the new practice-ledger CLI subcommand names. Affected skills (per AES-003 Agent E touchpoint audit): retro, triage, sprint-planning, intake, decision, assessment, feature-breakdown. Also update related evals (`eval-triage-queue-items-written-via-cli.md`, `eval-triage-resurfaces-open-queue-items.md`) for the schema changes (field renames where applicable). Update architecture.md Read/Write Authority rows to reflect the new CLI surface.

**Source:** decision (DEC-033, AES-003 Findings 6 and 9)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** practice
**Suggested change_type:** skill-instruction (multiple workflow.md files)
**Suggested priority:** medium
**Dependencies:** A1 (requires the new CLI)
**Effort estimate:** 3–4 hours
**Verification approach:** EDD eval per affected skill workflow (verify the new CLI invocations work); harness_profile: default

---

## Observation 5 — B1: Epic schema migration

**Title:** B1: Epic schema migration — define epics.json, migrate features and categorical epics, re-home unhomed stories

**Description:** Implement DEC-034 D1–D5. Define new `epics.json` schema at `_bmad-output/planning-artifacts/epics.json` with the unified epic shape: `epic_slug`, `name`, `description`, `lifecycle: finite-lived | long-lived`, `audience: user | internal`, plus carried-forward feature fields (`value_analysis`, `system_context`, `acceptance_conditions`, `stories[]`, `stories_done`, `stories_remaining`, `last_verified`, `notes`). Migrate the 23 current features into the new shape (default `finite-lived` + `user`). Evaluate the 18 categorical epics one by one with the developer: dissolve into finite-lived epics where possible (re-home their stories accordingly) or convert to `long-lived` where genuinely warranted (e.g., `ad-hoc`). Best-effort re-home the 269 unhomed stories from `stories/index.json` into appropriate epics; `ad-hoc` accepts residue. Freeze `features.json` as `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json`. Update architecture.md (Decisions 44–49 → historical; Read/Write Authority + Skills Deployment Classification). Update prd.md (FR102–FR113 superseded). Restructure `epics.md` (likely retire as narrative; the canvas becomes the human view).

**Source:** decision (DEC-034)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** practice
**Suggested change_type:** specification (heavy schema + doc work), config-structure (data migration), possibly script-code (small migration script)
**Suggested priority:** high
**Dependencies:** none (foundation story; blocks B2, B3, B4)
**Effort estimate:** 6–10 hours (heaviest cascade B lift; includes the 269-story re-homing pass)
**Verification approach:** Document review (developer + AVFL on the new schema + migrated data); harness_profile: default

---

## Observation 6 — B2: create-story input-routing update

**Title:** B2: create-story input-routing — read epic context instead of feature context

**Description:** Update `momentum:create-story` to read epic context (from new `epics.json`) instead of feature context (from retired `features.json`). The skill's input-routing logic for upstream context — currently looks up the story's feature_slug to find feature value_analysis/system_context/acceptance_conditions — needs to change to look up the story's epic_slug. The change_type-aware context injection that pulls from decisions/architecture/PRD for the right story type remains the same. Update SKILL.md + workflow.md.

**Source:** decision (DEC-034 D6)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** practice
**Suggested change_type:** skill-instruction (SKILL.md + workflow.md updates)
**Suggested priority:** medium
**Dependencies:** B1 (requires epics.json to exist as the new source)
**Effort estimate:** 2–3 hours
**Verification approach:** EDD eval (run create-story against an epic-homed story stub; verify epic context is injected); harness_profile: default

---

## Observation 7 — B3: Canvas update — features lens becomes epics lens

**Title:** B3: Canvas update — render epics instead of features

**Description:** Update `skills/momentum/skills/canvas/server.tsx` (TypeScript) to render epics. Per AES-003 Finding 9, this is a "hidden blocker" the original plan missed. Replace `readFeaturesJson()` + `readFeatureBySlug()` with `readEpicsJson()` + `readEpicBySlug()`. Update the `/lenses/features` route to `/lenses/epics`. Update the L2 detail view to render epic shape (lifecycle, audience, etc.). Sprint lens and cycle timeline lens unaffected. Practice-rendering path may need rework — verify against DEC-048 (practice project detection).

**Source:** decision (DEC-034, AES-003 Finding 9)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** feature (user-visible canvas behavior)
**Suggested change_type:** script-code (TypeScript implementation), skill-instruction (canvas SKILL.md + workflow.md updates)
**Suggested priority:** medium
**Dependencies:** B1 (requires epics.json to exist)
**Effort estimate:** 4–6 hours
**Verification approach:** Smoke test (run canvas server, visit /lenses/epics, confirm rendering) + Manual review for visual correctness; harness_profile: default

---

## Observation 8 — B4: feature-grooming/feature-breakdown restructure

**Title:** B4: feature-grooming + feature-breakdown → epic-grooming + epic-breakdown restructure

**Description:** Per DEC-034 D6: rename `momentum:feature-grooming` to `momentum:epic-grooming` (taking over the unified epic taxonomy maintenance role; the existing categorical `epic-grooming` retires — its work absorbs here). Rename `momentum:feature-breakdown` to `momentum:epic-breakdown`. Update each skill's SKILL.md frontmatter (name, description), workflow.md (references to features.json → epics.json; six-signal scan now applies to unified epics), and evals (rename + update assertions). Move skill directories. Update architecture.md Skills Deployment Classification rows. Update any references to old skill names in other skills' workflows (sprint-planning, etc.).

**Source:** decision (DEC-034 D6)
**Suggested classification:** ARTIFACT
**Suggested epic:** ad-hoc
**Suggested story_type:** practice
**Suggested change_type:** skill-instruction (skill renames + workflow updates; directory moves)
**Suggested priority:** medium
**Dependencies:** B1 (requires epics.json to exist; otherwise the renamed skills have no data source)
**Effort estimate:** 3–5 hours
**Verification approach:** EDD eval per renamed skill; harness_profile: default

---

## Triage Execution Plan

1. **Run momentum:triage** with this handoff as the input.
2. **Confirm classification** — all 8 should land as ARTIFACT (this handoff already pre-classifies; triage's batch-approval UX validates).
3. **Triage delegates each to momentum:intake** for story stub creation. Stubs land at `.momentum/stories/{slug}.md` with the enrichment fields populated.
4. **Stubs go into `.momentum/stories/index.json`** with status `backlog`. They become create-story candidates.
5. **Run momentum:create-story** for each story (in pairs of 2 max, per cascade plan concurrency constraints) to flesh out the full spec.
6. **Cascade execution** follows via quick-fix in dependency order (A1 then A2/A3/A4 in pairs; B1 then B2/B3/B4 in pairs).
7. **Post-cascade batch AVFL** scan-profile pass on integrated final state (per `feedback_avfl_post_merge_strategy.md`).
8. **Close cascade process story** `practice-ledger-features-epics-cascade-sequenced-plan`: in-progress → review → done.

---

## Suggested triage observation file

If your `momentum:triage` workflow expects observations as discrete entries to classify, this handoff document IS the observation file — each of the 8 observations above maps to one triage classification decision. Pre-classified suggestions provided per observation; triage can override.

If your triage workflow instead expects to read from `.momentum/intake-queue.jsonl` for observations, this handoff can be loaded as 8 separate `source: handoff` entries (one per observation) — but that introduces the very `intake-queue.jsonl` we're about to retire as part of DEC-033. Recommendation: read this handoff document directly during the triage session rather than round-tripping through the queue that's about to be redesigned.
