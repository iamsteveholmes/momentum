---
title: Impetus session greeting leads with N-of-M feature conditions passing
story_key: impetus-session-greeting-leads-with-n-of-m-feature
status: ready-for-dev
epic_slug: momentum-impetus-session-orientation
feature_slug:
story_type: practice
priority: medium
change_type:
  - rule-hook
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on:
  - momentum-tools-feature-verify-human-verdict-recorder-and
touches:
  - .claude/rules/impetus.md
  - skills/momentum/skills/impetus/SKILL.md
  - skills/momentum/skills/impetus/references/orient.md
  - skills/momentum/references/rules/decision-grade-presentation.md
  - skills/momentum/skills/impetus/evals/
---

# Impetus session greeting leads with N-of-M feature conditions passing

## Story

As a developer,
I want the Impetus session greeting to lead with the practice's headline number — N of M feature acceptance conditions passing, read from `.momentum/features.json` — alongside the existing honest ledger counts,
so that story counts no longer mislead about actual delivered capability.

## Description

The Impetus session-start situational report leads with the practice's headline number: **N of M
feature acceptance conditions passing**, read from `.momentum/features.json`, alongside the honest
ledger counts it already carries. Story counts stop leading any report surface — they may survive as
supporting detail, never as the headline.

This is **integration seam 3 of DEC-040 D1** — the third and last of the three seams features are
permitted to touch (1: sprint planning declares `goal_conditions`; 2: sprint closure records a human
PASS/FAIL verdict; 3: Impetus reports N passing). No other seam is opened by this story.

**Consumer seam — read-only, single writer upstream.** This story is the *consumer* side of a
producer/consumer pair:

- **Producer:** `momentum-tools-feature-verify-human-verdict-recorder-and` — the
  `momentum-tools feature verify` command, which is the **sole writer** of `.momentum/features.json`
  (DEC-040 D1: "Sole writer: the `momentum-tools feature verify` command recording a human verdict").
- **Consumer:** this story — the Impetus greeting, which **reads the registry and never writes it**.
  No Impetus surface may create, repair, backfill, or otherwise mutate `.momentum/features.json`,
  including when the file is absent.

The registry's status model is **failing-by-default** (`absent | failing | passing`). N counts only
features whose status is `passing`; M is every feature in the registry. A feature with no recorded
human verdict is never counted as delivered.

**Budget discipline.** The situational report's cap is ≤ 2 sentences (Decision-Grade Presentation
Standard §2.2 row 1). The N-of-M signal **joins** that budget — it never widens it. Under the
caps-vs-floor rule, the N-of-M number becomes a floor element alongside the honest ledger counts and
the recurring-pattern signal: it may not be trimmed to hit the sentence cap. Other wording (voice
framing, sprint narration) gets trimmed instead.

**Pain context:** Nornspun delivery discovery — story throughput rose 3→9 per sprint while 0 of 15
features ever passed. Story counts actively misled; the only number that should greet the developer
is verified user capability.

**Source:** DEC-040 D1, integration seam 3
(`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`).

## Acceptance Criteria

1. **The greeting reads the registry and computes the two numbers.** At session start, Impetus reads
   `.momentum/features.json` and derives N (features whose status is `passing`) and M (total features
   in the registry).

2. **N of M leads the situational report.** The N-of-M feature number is the first fact the developer
   reads — ahead of ledger counts, sprint name, handoff context, and any story number. The single
   exception is a pending gate card: when one exists, the pending question leads and the N-of-M
   headline follows it immediately (DEC-040 D5 — Impetus leads the session with the card as the
   agenda). Absent a pending card, N-of-M is first.

3. **The existing floor survives inside the same budget.** The honest ledger counts (open / this week
   / older than 30 days / near auto-close) and any recurring-pattern signal still appear inline, and
   the whole report still fits its ≤ 2-sentence budget. The N-of-M signal joins that budget rather
   than widening it.

4. **Story counts never lead.** No Impetus report surface leads with a story count. Where story
   numbers still appear, they appear after the feature number as supporting detail.

5. **Absent or empty registry degrades honestly, not silently.** When `.momentum/features.json` does
   not exist, or exists with zero features, the greeting states plainly that no features are tracked
   yet and continues normally. It does not error, does not omit the slot without comment, and does
   not render an empty registry as a health signal.

6. **Failing-by-default is preserved in the count.** Only features with status `passing` count toward
   N. Features with status `failing` or `absent` count toward M but not N. A feature with no recorded
   verdict is never counted as passing.

7. **The greeting is read-only against the registry.** No Impetus surface writes, creates, repairs, or
   backfills `.momentum/features.json` under any condition, including when the file is missing.

8. **The floor is written down where it binds.** The Impetus presentation-standard floor names the
   N-of-M feature signal as a required element of the situational report, so a future editor cannot
   trim it to satisfy the sentence cap.

## Tasks / Subtasks

- [ ] **Task 1 — Update the always-on Impetus rule to read and lead with N of M.** (AC1, AC2, AC5,
      AC6, AC7)
  - [ ] In `.claude/rules/impetus.md` § "Session-start behavior", add the features-registry read to
        the existing **single** Bash call that gathers cheap state — do not add a second call.
  - [ ] Specify the derivation: N = count of features with `status == "passing"`; M = total feature
        entries. State that `absent` and `failing` both count toward M only.
  - [ ] Specify the absent/empty behavior: report "no features tracked yet" (honest empty state),
        never an error and never an implied-healthy `0 of 0`.
  - [ ] State explicitly that the read is read-only — Impetus never writes `.momentum/features.json`;
        `momentum-tools feature verify` is the sole writer.
  - [ ] Rewrite the situational-report instruction so the N-of-M number leads, ahead of ledger counts
        and sprint state.
  - [ ] Add a `.momentum/features.json` row to the § "Where state lives" table
        ("How much of the product verifiably works").

- [ ] **Task 2 — Update the Impetus skill's Presentation Standard floor.** (AC3, AC8)
  - [ ] In `skills/momentum/skills/impetus/SKILL.md` § "Presentation Standard", add the N-of-M feature
        signal to the non-negotiable floor beside the honest ledger counts and recurring-pattern
        signal.
  - [ ] Restate caps-vs-floor for this surface: the ≤ 2-sentence cap governs length; it does not
        license dropping the feature number. Trim voice framing first.
  - [ ] Confirm NFR compliance is untouched: `description` ≤ 150 chars, `model:`/`effort:` present,
        body ≤ 500 lines.

- [ ] **Task 3 — Update the orientation reference so the legacy skill path reports the same number.**
      (AC1, AC2, AC4, AC5)
  - [ ] In `skills/momentum/skills/impetus/references/orient.md` § "State Sources", add
        `.momentum/features.json` as a silently-read source with the same honest-missing rule already
        applied to other sources.
  - [ ] In § "Situational States", make the feature number the lead-with value across states — story
        and sprint detail follows it.
  - [ ] In § "Delivery Principles", add the demotion rule: story counts never lead; they are
        supporting detail only.

- [ ] **Task 4 — Name the feature signal in the shared presentation-standard floor.** (AC8)
  - [ ] In `skills/momentum/references/rules/decision-grade-presentation.md`, amend the
        **Situational report** row of the per-surface budget table (§2.2 row 1) so its floor clause
        names the N-of-M feature signal alongside the honest ledger counts and recurring-pattern
        signal.
  - [ ] Keep the edit surgical — one row's floor clause. Do not restructure the table or alter any
        other surface's budget. Project scope may tighten a cap, never loosen one.

- [ ] **Task 5 — Write behavioral evals for the greeting.** (AC1–AC7)
  - [ ] Add evals under `skills/momentum/skills/impetus/evals/`, following the existing
        `eval-<behavior>.md` naming and "Given … the skill should …" format:
    - [ ] `eval-greeting-leads-with-feature-count.md` — populated registry with a mix of passing and
          failing features: the greeting leads with N of M and the ledger counts still appear inline.
    - [ ] `eval-greeting-honest-when-no-features-registry.md` — `.momentum/features.json` absent: the
          greeting reports no features tracked yet, does not error, and writes nothing.
    - [ ] `eval-greeting-story-counts-never-lead.md` — active sprint with several done stories: the
          story count does not lead; the feature number does.
  - [ ] Run the EDD cycle: spawn a subagent per eval, observe behavior, revise the instructions on
        mismatch (max 3 cycles).

## Dev Notes

### Decision Authority

**DEC-040 D1 is the source of truth for this story.** Where this story file and DEC-040 D1 disagree,
D1 wins.

Binding constraints carried from D1:

- Features integrate at **exactly three seams and no others**. This story is seam 3 (Impetus reports
  N passing). Do not add a fourth seam — no epic-facing skill, no story-facing skill, and no other
  report surface gains a features read as part of this story.
- **Sole writer:** `momentum-tools feature verify`. This story's surfaces are strictly read-only.
- **Failing-by-default** status model: `absent | failing | passing`.
- Registry location is **`.momentum/features.json`** (per-project).

**Read path — resolved default (no new CLI surface).** The greeting reads `.momentum/features.json`
directly inside the existing single session-start Bash call. A `momentum-tools feature <read>`
subcommand was considered and rejected for this story: the sibling producer story owns the `feature`
command group in `skills/momentum/scripts/momentum-tools.py` this sprint, and a second story editing
that file invites a merge collision for no behavioral gain. The consumer needs two integers; a direct
read of a small JSON file is the minimal seam.

**Verification method — `behavioral-trigger` (advisory).** This story classifies as both `rule-hook`
and `skill-instruction`, which route to `behavioral-trigger` and `skill-invoke` respectively. The
primary deliverable is the always-on rule at `.claude/rules/impetus.md` — the surface that actually
renders today's greeting — and the observable outcome is "start a session with a known registry
fixture in place, observe what the greeting leads with." That is a trigger-and-observe test, so
`behavioral-trigger` governs. The skill-instruction tasks are verified by their EDD evals (Task 5)
within the same pass.

### Current State of Affected Files

| File | Current state | What this story changes | Must be preserved |
|---|---|---|---|
| `.claude/rules/impetus.md` | § "Session-start behavior" specifies **one** Bash call gathering sprint summary, `momentum-tools practice-ledger summary` counts, the idempotent `close-stale` safety net, and the 3 most recent handoffs. Surfaces a 1–2 sentence situational report, then yields. | Adds the `.momentum/features.json` read to that same call; makes N-of-M the lead of the report; adds a features row to "Where state lives". | The single-call discipline, the ledger counts + recurring-pattern signal, the close-stale safety net, the yield-then-wait behavior, and the "do not dump menus / do not narrate the read" boundaries. |
| `skills/momentum/skills/impetus/SKILL.md` | 80 lines. § "Presentation Standard" declares the ≤ 2-sentence situational-report cap and a floor of honest ledger counts + recurring-pattern signal, plus the caps-vs-floor note. `model: sonnet`, `effort: low`. | Adds the N-of-M feature signal to the floor and to the caps-vs-floor note. | The cap value (≤ 2 sentences), the existing floor elements, `effort: low` and the note that low effort does not reduce completeness, and NFR limits (description ≤ 150 chars, body ≤ 500 lines). |
| `skills/momentum/skills/impetus/references/orient.md` | 60 lines. § "State Sources" lists sprints index, stories index, and `.momentum/signals/`, with an explicit honest-missing rule and no fallback to `_bmad-output/implementation-artifacts/`. § "Situational States" table has a "Lead with" column that is currently sprint/story-shaped. | Adds the features registry as a silent source; makes the feature number the lead-with value; adds the story-counts-never-lead principle. | The silent-read rule and its single sanctioned exception (plugin-cache staleness warning), the honest-missing-source rule, the 2–3 suggestion maximum, and BOND.md memory integration. |
| `skills/momentum/references/rules/decision-grade-presentation.md` | Line 51 is the **Situational report** row: cap ≤ 2 sentences, floor clause naming honest ledger counts + recurring-pattern signal, with "floor wins on the signal — do not drop it to hit the sentence count; trim other wording instead". | Adds the N-of-M feature signal to that row's floor clause. | Every other row's budget, the caps-vs-floor resolution rule, and the cascade note that project scope may tighten but never loosen a cap. |
| `skills/momentum/skills/impetus/evals/` | 74 existing `eval-*.md` behavioral evals in "Given … the skill should …" form. | Adds 3 new evals for the feature-number greeting. | Existing evals and their naming convention. |

**Registry state at story time:** `.momentum/features.json` does **not** exist yet, and **nothing in
this sprint creates its content.** The producer story ships only the `momentum-tools feature verify`
write command and explicitly disclaims authoring registry content; populated registry data arrives
via the DEC-040 Phase 3 design reconciliation. Every verification in this story — and every eval in
Task 5 — therefore runs against a **fixture** registry and must not depend on real project state.

**Path collision warning:** `skills/momentum/scripts/momentum-tools.py` contains legacy code
referencing `_bmad-output/planning-artifacts/features.json` (the deprecated feature-status cache,
superseded by `momentum:canvas`). That is **not** this registry. Read `.momentum/features.json` and
nothing else; do not "fix" or consult the legacy path.

### Architecture Compliance

- **Decision-Grade Presentation Standard** (`skills/momentum/references/rules/decision-grade-presentation.md`)
  governs this surface end to end. §2.2 row 1 sets the ≤ 2-sentence cap; §3 defines the
  self-sufficiency floor; §4 resolves cap-vs-floor conflicts in the floor's favor. This story adds a
  floor element and changes no cap.
- **Exec-summary-first** (§2.1) is the rule that makes AC2 architectural rather than cosmetic: the
  first content element must be the decision-relevant headline. The headline is verified capability,
  not activity.
- **Authority hierarchy** — the global rule at `~/.claude/rules/decision-grade-presentation.md` is
  the parent of the in-repo copy. Project scope may **tighten** a cap, never loosen it. Adding a
  required floor element is a tightening and is permitted; do not touch the cap value.
- **DEC-040 D1 three-seam constraint** is an architectural boundary, not a style preference. DEC-034
  was amended precisely because making features a peer of epics inside every skill was the prior
  failure. Widening the read surface beyond Impetus re-creates that failure.
- **Impetus boundaries** (`.claude/rules/impetus.md` § Boundaries) — Impetus orchestrates; it does not
  write practice state. The read-only constraint in AC7 is this boundary applied to the registry.

### Cross-Story Coordination

`conduct-resume-card-impetus-pending-gate-agenda-session` (DEC-040 D5) modifies the **same** Impetus
session-start surface in this sprint, adding the pending-gate agenda. The division of ownership:

- **This story** owns the headline number — N of M feature conditions passing.
- **The resume-card story** owns the pending-gate agenda item and the card read.

**Ordering (agreed with the sibling story, per DEC-040 D5):** when a **pending gate card exists, it
leads** and the N-of-M headline follows it. **Absent a pending card, N-of-M leads.** The sibling
story's AC7 states the same rule from its side ("the pending question is the first thing in the
situational report"); the two stories must not diverge on this.

Both additions land in the same section of `.claude/rules/impetus.md` and
`skills/momentum/skills/impetus/SKILL.md`, and both must fit the same ≤ 2-sentence budget; neither
may widen it. Whichever lands second **preserves** the other's addition rather than overwriting the
section. No `depends_on` edge is declared between the two — this is a merge-sequencing note for the
Conductor, not a build-order constraint.

### Testing Requirements

Verification is behavioral: create the trigger condition, observe the greeting.

- **Populated registry** — write a fixture `.momentum/features.json` with a known mix (e.g., 2
  `passing`, 5 `failing`, 1 `absent`). Start a fresh session. Observe: the greeting leads with "2 of
  8", the ledger counts and any recurring-pattern signal appear inline, and the whole report is ≤ 2
  sentences.
- **Absent registry** — remove/rename the fixture. Start a fresh session. Observe: the greeting says
  no features are tracked yet, does not error, and the file is still absent afterward (proving the
  read-only constraint).
- **Empty registry** — a registry with zero feature entries. Observe: the same honest empty state, not
  a `0 of 0` that reads as healthy.
- **Story-count demotion** — with an active sprint carrying several done stories, confirm no story
  count leads the report.
- **Read-only proof** — after each run, confirm `.momentum/features.json` is byte-identical (or still
  absent). Any write is an AC7 failure.
- **EDD evals** (Task 5) cover the skill-instruction surfaces per the change-type guidance below.

Restore any fixture state after verification — do not leave a synthetic registry behind.

### Project Context Reference

- Registry: `.momentum/features.json` (created by the producer story; per-project; failing-by-default).
- Producer command: `momentum-tools feature verify <feature-slug> --verdict pass|fail --evidence <text> --build <backendSha>:<clientSha>`.
- Existing greeting data source: `momentum-tools practice-ledger summary` — returns open-entry counts
  (this week / older than 30 days / near auto-close) plus recurring-pattern signals.
- Sprint: `sprint-2026-08-03` — DEC-040 implementation. Sprint goal: *"A sprint can no longer claim
  done without a human seeing it work."*

### References

- `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (D1 integration seam 3; D5 for the resume-card overlap)
- `skills/momentum/references/rules/decision-grade-presentation.md` §2.2 row 1, §3, §4
- `skills/momentum/references/rules/verification-standard.md` §1 (change-type → method routing), §2 (method override justification)
- `docs/research/nornspun-delivery-discovery-2026-08-02/` (pain context: 0 of 15 features passing across 10 sprints)
- Producer story: `.momentum/stories/momentum-tools-feature-verify-human-verdict-recorder-and.md`
- Overlapping consumer story: `.momentum/stories/conduct-resume-card-impetus-pending-gate-agenda-session.md`
- Epic context: `momentum-impetus-session-orientation` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → `rule-hook` (functional verification)
- Tasks 2, 3, 4, 5 → `skill-instruction` (EDD)

---

### rule-hook Tasks: Functional Verification

Rules are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule change** per the established format in `.claude/rules/impetus.md`. Keep the
   session-start behavior a single Bash call; the features read joins it.
2. **State the expected behavior** as a testable condition in the Dev Agent Record: "Given a session
   starts with `.momentum/features.json` present, the greeting leads with N of M feature conditions
   passing, within the ≤ 2-sentence budget, with ledger counts intact."
3. **Verify functionally:** create each registry fixture state (populated, empty, absent), trigger a
   fresh session start, and record what the greeting actually led with in each case. Confirm the
   registry file is unmodified after every run.
4. **Document** the verification result and the observed greeting text for each fixture state in the
   Dev Agent Record.

**Format requirements:**
- The rule file follows the established markdown format of the other `.claude/rules/` files.
- The rule stays internally consistent: the "Where state lives" table and the "Session-start
  behavior" section must agree on the registry path and on read-only status.

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as a testable condition (in Dev Agent Record)
- [ ] Functional verification performed across all three registry states and result documented
- [ ] Format matches established patterns
- [ ] Read-only constraint proven — registry unmodified after each session-start run

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md, workflow.md, or reference files.** Skill instructions are
non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line:**
1. Write the behavioral evals in `skills/momentum/skills/impetus/evals/` (the directory exists — match
   its `eval-<behavior>.md` naming):
   - Format each eval as: "Given [input and context], the skill should [observable behavior]"
   - Test behaviors and decisions, not exact output text — assert that the feature number *leads*,
     not that a specific sentence is produced.

**Then implement:**
2. Modify `skills/momentum/skills/impetus/SKILL.md`, `references/orient.md`, and the
   `decision-grade-presentation.md` situational-report row.

**Then verify:**
3. Run the evals: for each eval file, spawn a subagent with the eval's scenario as its task and the
   modified SKILL.md / orient.md contents as context. Observe whether behavior matches.
4. All evals match → tasks complete.
5. Any eval fails → diagnose the instruction gap, revise, re-run (max 3 cycles; surface to the
   developer if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- `SKILL.md` `description` field ≤ 150 characters (NFR1) — count precisely; this story does not change
  it, so confirm it is still within budget after editing.
- `model:` and `effort:` frontmatter present (`model: sonnet`, `effort: low` today — preserve both).
- `SKILL.md` body under 500 lines / 5000 tokens (NFR3); currently 80 lines, so overflow is not a risk,
  but keep the Presentation Standard edit tight.
- Skill name keeps the `momentum:` namespace (NFR12).

**Additional DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written in `skills/momentum/skills/impetus/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] `SKILL.md` description ≤ 150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and unchanged
- [ ] `SKILL.md` body ≤ 500 lines confirmed
- [ ] AVFL checkpoint on the produced artifact documented (`momentum:dev` runs this automatically)

---

### Story-Wide DoD Additions

- [ ] The situational report still fits ≤ 2 sentences with the N-of-M signal included — measured, not
      assumed.
- [ ] Honest ledger counts and recurring-pattern signal still appear inline (floor preserved).
- [ ] No Impetus surface writes `.momentum/features.json` under any registry state.
- [ ] No fourth features seam introduced — only Impetus surfaces read the registry.
- [ ] Fixture registries removed after verification.

---

### Frozen Verification Contract

A frozen verification contract exists for this sprint at
`.momentum/sprints/sprint-2026-08-03/specs/impetus-session-greeting-leads-with-n-of-m-feature.eval.yaml`.
Read the Part-A header (`verification_method`, `harness_profile`, `how_dev_self_checks`) as the
pre-done self-check; the Part-B body is for verifier agents only.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
