---
title: Daily tasting reminder + expected-vs-reality brief generator
story_key: daily-tasting-reminder-expected-vs-reality-brief-generator
status: ready-for-dev
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
priority: high
change_type:
  - script-cli
  - rule-hook
verification_method_advisory: bash
depends_on: [momentum-tools-feature-verify-human-verdict-recorder-and]
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - .claude/rules/impetus.md
---

# Daily tasting reminder + expected-vs-reality brief generator

## Story

As a developer,
I want a daily reminder for my ≥10-minute tasting session, paired with a generated brief that lays out what the practice claims works today, what changed since I last looked, and 2–3 specific probes,
so that the model's expectations about the product's behavior get tested against reality instead of going unverified.

## Description

Two deliverables, both hanging off the feature registry:

1. **The reminder.** A tasting-due signal — how many days since the developer last recorded a
   human verdict against a feature — surfaced by Impetus at session start with prominence that
   rises as the gap widens. It never fails, blocks, or errors anything; escalation is
   re-surfacing only (DEC-040 D5 replaced expiry-FAIL with session-start re-surfacing precisely
   because this practice serves a nights-and-weekends developer, for whom a time-based automatic
   failure is a punishment for having a day job).

2. **The brief.** A generated document that contrasts **what the practice claims** against
   **what the developer has actually seen work**: the features the registry currently marks
   `passing` (the claim), what merged since the last walkthrough (the change), and 2–3 specific
   probes the developer performs in the running app (the test). Findings from the walkthrough
   route to intake under the owner-priority rule (DEC-040 D6) carrying the feature slug of the
   probe that surfaced them.

**The consumer seam (explicit).** `.momentum/features.json` has exactly one writer and this
story is not it.

- **Producer:** `momentum-tools feature verify` — the sole writer of `.momentum/features.json`,
  built by the sibling story `momentum-tools-feature-verify-human-verdict-recorder-and` in this
  same sprint. It records the human PASS/FAIL verdict and stamps `last_verified {date, build
  SHAs, verdict}`.
- **Consumer:** this story's `momentum-tools tasting` commands — **read-only**. They open the
  registry, derive the walkthrough window from the newest `last_verified.date` — an accepted
  proxy for the last walkthrough, since verdicts are recorded at sprint closure, not at every
  daily walkthrough; a walkthrough that records no verdict does not advance it, so the window
  is clamped to the bounded default maximum (14 days) rather than growing without limit — and never write
  a byte back to it under any code path. The architecture Read/Write Authority table already
  names the "daily tasting-brief generator (DEC-040 D4)" as a read-only consumer of that file;
  this story implements that row as written.

That direction is the whole point of the design: the registry is failing-by-default and only a
human verdict flips a condition to `passing`. If the brief generator could write to it, the
practice could once again claim delivery without a human ever having seen the thing work — the
exact failure DEC-040 exists to close.

**Source of truth:** DEC-040 D4 —
`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`.
Schema authority for `.momentum/features.json` is DEC-040 D1 (same document).

**Pain context:** Steve, verbatim: "no less than 10 min daily, and that means I need Claude
Code to remind me AND prepare a document for what we would expect today. Let's see if the
model's expectations stand up to reality." Discovery receipt: 5–6 app-launch days in 54; every
one of those walkthroughs found a top-tier defect within minutes; the dev database after four
months held zero real user data.

## Acceptance Criteria

1. `momentum-tools tasting brief` exists as an invocable subcommand. It writes a brief to
   `.momentum/tasting/brief-<YYYY-MM-DD>.md` and, with `--json`, also prints a machine-readable
   summary of the same content to stdout.

2. Both `tasting` subcommands treat `.momentum/features.json` as read-only. No code path in
   this story opens the registry for writing, creates it, or modifies any field in it —
   including `last_verified`.

3. The brief's "What should work today" section names the features the registry currently
   marks `passing` — up to 7, quoting each feature's acceptance condition verbatim so the
   developer can see the exact claim they are being asked to test. When more than 7 are
   passing, the 7 most recently verified appear and the remainder collapse to a single
   count line, per the decision-grade collapse convention.

4. The brief's "What changed" section lists what merged since the last recorded verdict — the
   newest `last_verified.date` in the registry, used as an accepted proxy for the last
   walkthrough. The window never exceeds the bounded default maximum of 14 days: when the
   registry holds no recorded verdict at all, or the newest verdict is older than that bound,
   the command falls back to the 14-day default window. The brief states in plain language which window
   it used and why.

5. The brief generates 2–3 probes, never more and never zero when there is at least one claim
   to test. Each probe names one feature slug, states the claim under test, and gives a
   concrete action the developer performs in the running app — not an instruction to read code,
   inspect a file, or run a test suite.

6. When `.momentum/features.json` is absent, empty, or unparseable, the command still produces
   a brief, states plainly that there are no recorded claims to test, emits zero probes rather
   than inventing any, and exits with status 0.

7. The brief closes with routing instructions for findings: anything the developer observes
   during the walkthrough enters intake at critical priority with a mandatory feature link,
   carrying the feature slug of the probe that surfaced it (DEC-040 D6).

8. The brief is short enough to read before the walkthrough rather than instead of it: it
   opens with its purpose in plain language, holds each list to at most 7 items, and stays
   within AC 5's probe cap. A wall of text on this surface is a defect, not a style
   preference.

9. `momentum-tools tasting status --json` reports whether a tasting session is due (due when
   a full day or more has passed since the last recorded walkthrough, and always when the
   registry holds no verdict at all), the days-since count, and a prominence tier that rises
   with it: `quiet` at 1–3 days, `insistent` at 4–7, `leading` at 8 or more — the last
   threshold set against the discovery's 7–18-day withdrawal gaps.

10. The tasting-due signal never fails, blocks, exits non-zero, or errors a session under any
    input — including a missing registry, a malformed registry, or a repository with no git
    history. Escalation is re-surfacing at higher prominence and nothing else.

11. `.claude/rules/impetus.md` gains a section instructing Impetus to include the tasting nudge
    in the session-start situational report when a session is due, within that report's
    two-sentence budget and at the prominence the tier indicates: `quiet` appends the nudge
    inside the report's second sentence, `insistent` opens the second sentence with it, and
    `leading` makes it the report's first sentence. When no session is due, no nudge appears
    at all.

12. Running `momentum-tools tasting brief` twice on the same day is safe: the second run
    regenerates the same day's brief file in place rather than erroring, appending, or creating
    a duplicate.

## Tasks / Subtasks

- [ ] **Task 1 — Add the `tasting` command group to the CLI.** Register a `tasting` subparser in
      `build_parser()` in `skills/momentum/scripts/momentum-tools.py`, following the existing
      command-group pattern (`sprint`, `session`, `practice-ledger`), with `brief` and `status`
      subcommands. (AC 1, AC 9)

- [ ] **Task 2 — Implement the registry reader and window derivation.** Read
      `.momentum/features.json` read-only; tolerate absent, empty, and unparseable files without
      raising. Derive the walkthrough window start from the newest `last_verified.date` across
      all features (accepted proxy for the last walkthrough), clamping to the 14-day bounded
      default window when no verdict exists or the newest verdict predates the bound.
      (AC 2, AC 4, AC 6)

- [ ] **Task 3 — Implement `tasting status`.** Compute days since the last recorded walkthrough,
      the due flag, and the prominence tier per AC 9's thresholds (`quiet` 1–3, `insistent`
      4–7, `leading` 8+). Guarantee a zero exit and a well-formed payload on every input,
      including a repository with no git history. (AC 9, AC 10)

- [ ] **Task 4 — Implement `tasting brief`.** Assemble the three sections — the registry's
      current `passing` claims with their acceptance conditions quoted, what merged in the
      window, and 2–3 probes — plus the D6 findings-routing footer. Write to
      `.momentum/tasting/brief-<YYYY-MM-DD>.md`, regenerating in place on a same-day rerun, and
      support `--json`. (AC 1, AC 3, AC 4, AC 5, AC 7, AC 12)

- [ ] **Task 5 — Enforce the presentation caps in the generator.** Cap each list at 7 items and
      probes at 3; lead the document with its plain-language purpose. (AC 8)

- [ ] **Task 6 — Fixture-based tests for both subcommands.** Cover: a populated registry with
      mixed `passing`/`failing`/`absent` statuses; a registry with no `last_verified` anywhere;
      an absent registry; a malformed (unparseable) registry; a same-day rerun. Assert the
      registry file is byte-identical before and after every run. (AC 2, AC 4, AC 5, AC 6,
      AC 12)

- [ ] **Task 7 — Add the tasting-nudge section to `.claude/rules/impetus.md`.** Specify when the
      nudge appears, its two-sentence budget inside the situational report, and how prominence
      rises with the tier (the AC 11 placement mapping). State the expected behavior as a
      testable condition and verify it functionally. (AC 11)

## Dev Notes

### Decision Authority

DEC-040 is the source of truth for this story. Four of its decisions bind directly:

- **D4 (Daily tasting)** — the story itself: no less than 10 minutes daily; Claude Code both
  reminds and prepares a brief generated from `features.json` plus whatever merged since the
  last walkthrough; what should work today, what changed, 2–3 specific probes.
- **D1 (features.json registry)** — schema authority. Fields: `slug`, `name`,
  `acceptance_condition`, `status` (`absent | failing | passing`, failing-by-default),
  `last_verified {date, build SHAs, verdict}`, optional informational `epic_slugs` and
  `design_ref`. Sole writer: `momentum-tools feature verify`. Features integrate at exactly
  three seams and no others — do not add a fourth by making anything here write to the registry.
- **D5 (Resume cards / re-surfacing)** — governs the reminder's escalation model. A gate or
  nudge never silently hangs and never greets the developer with a wall of text; escalation is
  re-surfacing at every session start with rising prominence, never automatic failure.
- **D6 (Intake owner-priority)** — governs the brief's findings-routing footer. Owner-sourced
  app observations enter intake at critical priority with a mandatory feature link, verified on
  the surface where the owner met the behavior. The validator that enforces this is a separate
  sibling story; this story's job is to emit findings already carrying the feature slug so that
  validator has something to enforce against.

### Current State of Affected Files

**`skills/momentum/scripts/momentum-tools.py`** (~3,091 lines). A single-file argparse CLI.
`build_parser()` at the bottom registers command groups (`sprint`, `session`, `triage`,
`practice-ledger`, `version`, `story`, `feature-status-hash`), each with its own subparser and
`set_defaults(func=...)`. Handlers are module-level `cmd_*` functions taking
`argparse.Namespace`. Shared helpers already exist and should be reused rather than
re-implemented: `resolve_project_dir()`, `read_json()`, `write_json()`, `result()`, and
`error_result()`. There is currently **no** `tasting` command group and **no** command that
reads `.momentum/features.json`.

Note a naming trap in this file: `_compute_feature_status()` and `cmd_feature_status_hash()`
read a *different, legacy* `features.json` at `_bmad-output/planning-artifacts/features.json` —
the pre-DEC-034 planning artifact, superseded by `epics.json` for work tracking. That file is
not this story's registry and must not be confused with it. The DEC-040 registry is
`.momentum/features.json`, a different path with a different purpose.

**`.momentum/features.json`** — does not exist yet. It is created by the sibling story
`momentum-tools-feature-verify-human-verdict-recorder-and` in this same sprint. Every code path
here must therefore behave correctly against an absent registry, and the fixture suite must
cover that case explicitly rather than assuming the sibling has landed.

**`.claude/rules/impetus.md`** — the always-on Impetus persona rule. Its "Session-start
behavior" section already specifies one Bash call gathering cheap state (sprint summary,
practice-ledger counts, auto-close safety net, recent handoffs) and a situational report of 1–2
sentences. The tasting nudge belongs inside that existing budget as an added section — not as a
rewrite of the greeting, and not as an extra tool call on the happy path.

**Coordination note:** two sibling stories in this sprint also touch Impetus session-start
surfacing — `impetus-session-greeting-leads-with-n-of-m-feature` (the N-of-M headline) and
`conduct-resume-card-impetus-pending-gate-agenda-session` (the pending-gate agenda). Keep this
story's edit to a self-contained new section so the three compose rather than collide.

### Architecture Compliance

`_bmad-output/planning-artifacts/architecture.md` already carries the DEC-040 amendments this
story implements. The Read/Write Authority table names `momentum-tools feature verify` as
**sole writer** of `.momentum/features.json` and lists its read-only consumers as sprint-planning
(`goal_conditions`), Impetus (N-passing headline), and the **daily tasting-brief generator
(DEC-040 D4)** — this story. No architecture change is required; this story makes an existing
architectural row real.

The `.momentum/` State Layout section governs the new `.momentum/tasting/` directory: `.momentum/`
holds everything the practice produces and consumes during normal operation, which is exactly
what a generated daily brief is. Planning artifacts stay under `_bmad-output/planning-artifacts/`;
a tasting brief is not a planning artifact and does not go there.

The Decision-Grade Presentation Standard governs both output surfaces. The brief is a
developer-facing document under the caps (purpose first, ≤7 bullets per list, ≤3 probes). The
nudge is part of the situational report, whose budget is ≤2 sentences. DEC-040 D5 states the
enforcement plainly: massive walls of text on any gate surface are a defect.

### Testing Requirements

Verification is CLI-executable and fixture-based — no running product is required to verify this
story, even though the brief it generates points the developer *at* a running product.

Fixture registries to build under a temporary project directory:

- **Populated** — several features with mixed `passing` / `failing` / `absent` statuses and
  varied `last_verified` dates, to exercise claim selection and window derivation.
- **No verdicts** — features present, no `last_verified` anywhere, to exercise the default
  window fallback and its plain-language explanation.
- **Absent** — no `.momentum/features.json` at all, to exercise the honest-degradation path.
- **Malformed** — a file that is not valid JSON, to confirm it degrades rather than raising.

The read-only guarantee gets its own assertion, not just a code review: hash or byte-compare
`.momentum/features.json` before and after every `tasting brief` and `tasting status` invocation
across all fixtures, and assert it is unchanged.

Idempotence gets an assertion too: run `tasting brief` twice in the same day against the same
fixture and confirm one file exists, regenerated rather than appended or duplicated.

The rule change (Task 7) is declarative and has no unit test. Verify it functionally: state the
expected behavior as a testable condition and confirm the rule's sections are present,
internally consistent, and consistent with the prominence tiers the CLI actually emits.

### Project Context Reference

This story sits in the DEC-040 implementation sprint (`sprint-2026-08-03`), whose goal is: *a
sprint can no longer claim done without a human seeing it work.* This story is the half of that
goal aimed at the human's attention rather than the machinery's refusal — the closure-refusal
and merge-gate stories make the practice unable to lie; this story makes it likely the developer
actually looks. Both halves are needed: refusal without a tasting habit produces sprints that
correctly refuse to close and then stay open forever.

Per DEC-040's phased plan, this story is in phase 2 (Momentum skill/tooling changes), listed
last in that phase's enumeration — it depends on the registry writer existing but not on the
other phase-2 items.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 6 → `script-cli` (TDD, CLI-surface verification)
- Task 7 → `rule-hook` (functional verification)

---

### script-cli Tasks: TDD with CLI-Surface Verification

`script-cli` has no dedicated injection template in `change-types.md`; the `script-code` TDD
approach applies, with the CLI surface itself as the verification target (per
`verification-standard.md`, `script-cli` routes to the `bash` method — run the command with
representative inputs and observe that output matches spec).

1. **Red:** Write the failing fixture tests first — populated, no-verdicts, absent, and
   malformed registries, plus the read-only byte-comparison and the same-day rerun. Confirm
   they fail before implementing.
2. **Green:** Implement the minimum code to make them pass. Reuse the existing module helpers
   (`resolve_project_dir`, `read_json`, `result`, `error_result`) rather than adding parallel
   implementations.
3. **Refactor:** Improve structure while keeping tests green.

**Placement:** the new command group goes in `skills/momentum/scripts/momentum-tools.py`
alongside the existing groups — do not create a new script for it. Follow the established
`cmd_*` handler + `add_parser` + `set_defaults(func=...)` pattern exactly.

**DoD additions for these tasks:**
- [ ] `.momentum/features.json` verified byte-identical before and after every command run
- [ ] All four registry fixture states covered and passing
- [ ] Both subcommands exit 0 on every fixture, including malformed and absent
- [ ] Same-day rerun produces exactly one brief file
- [ ] No regressions in the existing momentum-tools test suite

### rule-hook Tasks: Functional Verification

Rules are declarative and have no unit tests. Verify functionally:

1. **Write the rule section** per the established format of the surrounding
   `.claude/rules/impetus.md` sections.
2. **State the expected behavior** as a testable condition: "When a session start finds
   `momentum-tools tasting status` reporting due with tier X, the situational report must
   include the tasting nudge at prominence X, within its two-sentence budget."
3. **Verify functionally** — confirm the section is present, internally consistent, and that
   the prominence tiers it names match the tiers the CLI emits.
4. **Document** the verification result and expected behavior in the Dev Agent Record.

**DoD additions for this task:**
- [ ] Expected behavior stated as a testable condition in the Dev Agent Record
- [ ] Functional verification performed and result documented
- [ ] Prominence tiers in the rule match the tiers `tasting status` emits
- [ ] Format matches the surrounding sections of `.claude/rules/impetus.md`

### Frozen Verification Contract

A frozen verification contract exists for this sprint at
`.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Read the **Part-A header only**
(`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before
signaling done. Do **not** read the verifier body (Part B: scenarios, assertion scripts,
Gherkin) beyond the sections `how_dev_self_checks` explicitly references.

### Project Structure Notes

- CLI implementation: `skills/momentum/scripts/momentum-tools.py` (existing file, extend)
- Fixture tests: `skills/momentum/scripts/test-momentum-tools.py` (existing suite, extend)
- CLI entry point: `skills/momentum/bin/momentum-tools` (existing wrapper, no change expected)
- Generated briefs: `.momentum/tasting/brief-<YYYY-MM-DD>.md` (new directory)
- Registry read (read-only): `.momentum/features.json` (write path owned by the sibling
  story's CLI; registry content arrives via DEC-040 Phase 3 design reconciliation — tests
  here run against fixture registries)
- Rule edit: `.claude/rules/impetus.md` (existing file, add one section)

### References

- Decision source: DEC-040 D4 (daily tasting), D1 (features.json schema authority), D5
  (re-surfacing escalation, no expiry-FAIL), D6 (intake owner-priority routing) —
  `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`
- Architecture Read/Write Authority table — names this story's generator as a read-only consumer
  of `.momentum/features.json`; `_bmad-output/planning-artifacts/architecture.md`
- `.momentum/` State Layout section — governs placement of `.momentum/tasting/`;
  `_bmad-output/planning-artifacts/architecture.md`
- Verification standard (change-type → method routing; `script-cli` → `bash`) —
  `skills/momentum/references/rules/verification-standard.md`
- Producer of the registry this story consumes: story
  `momentum-tools-feature-verify-human-verdict-recorder-and` (sole writer of
  `.momentum/features.json`)
- Owner-priority validator that consumes this story's findings: story
  `intake-owner-priority-validator-owner-sourced-app`
- Discovery receipts (5–6 app-launch days in 54; every walkthrough found a top-tier defect) —
  `docs/research/nornspun-delivery-discovery-2026-08-02/`
- Epic context: `momentum-impetus-experience` (from _bmad-output/planning-artifacts/epics.json)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
