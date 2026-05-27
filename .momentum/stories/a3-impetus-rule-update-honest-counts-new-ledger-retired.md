---
title: "A3: Impetus rule update — honest counts, new ledger, retired signals"
story_key: a3-impetus-rule-update-honest-counts-new-ledger-retired
status: ready-for-dev
epic_slug: ad-hoc
feature_slug: ""
story_type: practice
change_type:
  - rule-hook
verification_method: behavioral trigger test
harness_profile: default
depends_on:
  - a1-practice-ledger-schema-cli-redesign-true-append-only
touches:
  - .claude/rules/impetus.md
priority: medium
---

# A3: Impetus rule update — honest counts, new ledger, retired signals

## Story

As a developer,
I want the experimental Impetus rule updated to surface honest practice-ledger counts via the new `momentum-tools practice-ledger summary` CLI and drop retired signal references,
so that session-start orientation reflects real practice state instead of test scaffolding noise.

## Description

Implement **DEC-033 D9** (and absorb D5 + D6 surface effects) in the experimental `.claude/rules/impetus.md`. Three concrete changes:

1. **Replace the "last 5" anti-pattern.** The current Session-start behavior reads "last 5" entries from `.momentum/intake-queue.jsonl`. Per AES-003 Finding 4, this surfaces ~80% test scaffolding and hides 90% of open entries. Replace with honest, structured counts delivered by the new CLI from A1:
   - "N open entries (X this week, Y older than 30 days, Z near auto-close)"
   - Recurring patterns surfaced from history (e.g., "'X' has been `closed_stale` 4 times in 60 days")
   - No inline enumeration of entries; drill-down happens via CLI on developer request.

2. **Point at the new ledger filename and CLI.** Rename every reference from `.momentum/intake-queue.jsonl` to `.momentum/practice-ledger.jsonl`, including the "Where state lives" table row. Remove the "renaming to" parenthetical (the rename has happened). Use `momentum-tools practice-ledger summary` for session-start state gathering.

3. **Retire `.momentum/signals/` mentions entirely.** Per DEC-033 D6, the signals directory is absorbed into the unified ledger — every open ledger entry IS the attention surface. The current Impetus rule references the ledger only (no `signals/` mention in `impetus.md` today, but verify and remove any that surface). Confirm no surviving references.

A fourth implicit change: per **DEC-033 D5**, Impetus session-start is the safety-net invoker for `momentum-tools practice-ledger close-stale --age-days 15` when the last close-stale run is older than 24h. Add this to the session-start preflight (single Bash call, idempotent — the CLI itself handles the "did we run today?" check).

The Subagent guard section remains unchanged — Impetus must not adopt its identity when running as a subagent.

**Pain context:** AES-003 Findings 4 and 10 — the "last 5" rule was authored in the same evening as the assessment that revealed it lies about state. Closes that loop.

**Source:** triage — handoff `practice-ledger-and-epic-cascade-stories-2026-05-25`.

## Acceptance Criteria

1. **No "last 5" instruction.** The Session-start behavior section of `.claude/rules/impetus.md` contains no instruction to read "last 5" entries, no count-bounded enumeration of ledger rows, and no inline enumeration of entries.

2. **Honest counts via new CLI.** Session-start behavior instructs Impetus to gather state via `momentum-tools practice-ledger summary` (the CLI delivered by A1). The output shape Impetus surfaces matches DEC-033 D9:
   - "N open entries (X this week, Y older than 30 days, Z near auto-close)"
   - Recurring patterns from history when present (e.g., closed_stale recurrence)
   - At most 1–2 sentences in Impetus voice; no menus, no fill bars.

3. **Filename migration complete.** Every occurrence of `intake-queue.jsonl` in `.claude/rules/impetus.md` is replaced with `practice-ledger.jsonl`. The "Where state lives" table row for "What needs attention" points at `.momentum/practice-ledger.jsonl` and no longer carries the "renaming to" parenthetical.

4. **No `signals/` references.** `.claude/rules/impetus.md` contains zero occurrences of `.momentum/signals/`, `signals directory`, or `pending signals` surfacing instructions.

5. **Auto-close safety net wired.** Session-start behavior instructs Impetus to invoke `momentum-tools practice-ledger close-stale --age-days 15` as part of the single preflight Bash call. The instruction notes the CLI is idempotent (no harm if Routine already ran today).

6. **Subagent guard preserved.** The Subagent guard section is present and unchanged in intent — Impetus does not adopt its identity when running as a subagent.

7. **Boundaries preserved.** The Identity section, the Boundaries section ("does not write code…", "does not run legacy `/momentum:impetus`…", "does not prefix with structured menus…"), and the Status: Experimental note remain present and intact.

8. **Behavioral trigger test passes.** A fresh Claude Code session opened at the project root surfaces a session-start situational report in Impetus voice that:
   - Uses the new CLI (verifiable from the Bash call audit trail)
   - Surfaces honest counts in the structure described in AC 2
   - Does not enumerate entries inline
   - Yields to the developer after the situational report
   - Behaves as a no-op for the safety-net invocation when close-stale has already run within 24h (no visible disruption).

9. **Format compliance.** The rule file remains a single `.md` document under `.claude/rules/` with no new structural sections introduced; existing section ordering is preserved (Identity → Session-start behavior → Where state lives → Boundaries → Subagent guard).

## Tasks / Subtasks

- [ ] **Task 1 — Read the current rule and confirm scope.** Re-read `.claude/rules/impetus.md` and verify (a) the "last 5" instruction lives in the Session-start behavior section, (b) the "Where state lives" table contains the `intake-queue.jsonl` reference, (c) no `signals/` references exist (per current file inspection). Note any surprises before editing.

- [ ] **Task 2 — Rewrite Session-start behavior section.** Replace the "Open ledger entries from `.momentum/intake-queue.jsonl` (filter `status: "open"`, last 5)…" bullet with:
  - A bullet instructing the single preflight Bash call to invoke `momentum-tools practice-ledger summary` (returns honest counts + recurring patterns)
  - A bullet instructing the same Bash call to invoke `momentum-tools practice-ledger close-stale --age-days 15` as the session-start safety net (idempotent — CLI itself checks last-run timestamp)
  - Update the surfacing instruction so Impetus delivers 1–2 sentences in voice that include "N open entries (X this week, Y older than 30 days, Z near auto-close)" and any recurring-pattern signal returned by `summary`.
  - Preserve "Surface a brief situational report — 1–2 sentences in Impetus voice — then stop." and "Do not dump menus / narrate the read / run heavy orientation workflows."

- [ ] **Task 3 — Update "Where state lives" table.** Replace the "What needs attention" row's path with `.momentum/practice-ledger.jsonl` and drop the "renaming to `practice-ledger.jsonl`" parenthetical. No other table rows change.

- [ ] **Task 4 — Audit for `signals/` and stale references.** Run a grep across the file for `signals`, `intake-queue`, and `last 5`. Confirm zero remaining occurrences after edits. Remove anything missed.

- [ ] **Task 5 — Preserve Identity, Boundaries, Subagent guard.** Diff-check that the Identity section, Boundaries section, and Subagent guard section are byte-identical to pre-edit (or only changed for cross-reference consistency with the rewritten Session-start behavior).

- [ ] **Task 6 — Behavioral trigger test.** State the expected behavior as a testable condition: "Given a fresh Claude Code session opened at the project root, when Impetus runs the session-start preflight, then the situational report surfaces honest counts via `momentum-tools practice-ledger summary` (no 'last 5' enumeration) and the close-stale safety net is invoked idempotently." Open a fresh session in this project. Capture the actual session-start output. Confirm it matches AC 2, AC 5, and AC 8. Document the observed output + Bash call in the Dev Agent Record.

- [ ] **Task 7 — Document verification result.** Record in the Dev Agent Record: (a) the exact rewritten Session-start behavior section, (b) the diff summary, (c) the behavioral-trigger test result, (d) any deviation from spec and rationale.

## Dev Notes

### Architecture Compliance

This story implements **DEC-033 D9** with surface effects from **D5** (session-start safety-net invocation of close-stale) and **D6** (no surviving `signals/` references). Per DEC-033, Architecture Decision 52 is superseded — `.momentum/intake-queue.jsonl` is renamed to `.momentum/practice-ledger.jsonl` and the read path moves to a derived-state SQL query (DuckDB-backed) via `momentum-tools practice-ledger summary`. Architecture Decision 1c is amended to inherit the same event-log shape (forward pointer; no code impact here).

A1 delivers the new CLI subcommands (`summary`, `open`, `history`, `since`, `by-source`, `close-stale`) and the renamed ledger file. This story consumes that CLI from the rule layer. **A3 must not begin before A1 lands** — the `summary` CLI must exist for the rewritten session-start preflight to function.

Verification method routing per `skills/momentum/references/rules/verification-standard.md` Section 1: `change_type: rule-hook` → **behavioral trigger test**. The trigger is "fresh Claude Code session opened in this project"; the observable behavior is the Impetus session-start situational report.

The Impetus rule file (`.claude/rules/impetus.md`) is project-scoped (per `~/.claude/rules/authority-hierarchy.md`); this edit does not affect the global Impetus skill at `skills/momentum/skills/impetus/` (which is the legacy skill kept coexisting per the rule file's Status: Experimental note).

### Testing Requirements

Per the `rule-hook` template in `skills/momentum/skills/create-story/references/change-types.md`:

1. **Stated testable condition** (recorded in Dev Agent Record per template DoD): "Given a fresh Claude Code session opened at the project root, the Impetus session-start preflight surfaces honest counts via `momentum-tools practice-ledger summary` and invokes `close-stale --age-days 15` idempotently — without enumerating ledger entries inline and without surfacing pending-signals language."

2. **Functional verification** (the behavioral trigger test in Task 6):
   - Open a fresh Claude Code session at the project root
   - Observe Impetus's first response — confirm voice match, count structure, no inline enumeration
   - Inspect the audit trail of the preflight Bash call — confirm it invokes `momentum-tools practice-ledger summary` and `momentum-tools practice-ledger close-stale --age-days 15`
   - Open a second fresh session within 24h; confirm close-stale is still invoked but produces no visible effect (idempotency)

3. **Format compliance** (per template):
   - File remains valid markdown under `.claude/rules/`
   - Existing section ordering preserved
   - No duplicate sections introduced

No unit tests apply (rules are declarative). No EDD evals required (this is a rule edit, not a skill-instruction edit).

### Implementation Guide

#### Momentum Implementation Guide

**Change Types in This Story:**
- All tasks → `rule-hook` (functional verification)

---

#### rule-hook Tasks: Functional Verification

Rules and hook configurations are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule** per the established format in existing `.claude/rules/` files. The current `.claude/rules/impetus.md` is the format reference; preserve heading levels, list styles, and the table format already in use.

2. **State the expected behavior** as a testable condition (see Testing Requirements section 1 above).

3. **Verify functionally:**
   - For this rules file, the trigger is "fresh Claude Code session opened in this project."
   - Confirm all required sections are present and the rule is internally consistent (Identity, Session-start behavior, Where state lives, Boundaries, Subagent guard).
   - Confirm cross-references resolve: the CLI subcommand names (`summary`, `close-stale`) must match what A1 ships.
   - Confirm the rule does not reference any retired surface (`intake-queue.jsonl`, `.momentum/signals/`, "last 5", "pending signals").

4. **Document** the verification result and expected behavior in the Dev Agent Record.

**Format requirements:**
- Rule file remains a single `.md` document under `.claude/rules/`
- No duplicate sections; no new structural sections introduced
- Heading levels and table format preserved

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed and result documented (behavioral trigger test from Task 6)
- [ ] Format matches established patterns
- [ ] AVFL checkpoint on produced rule file documented (run by post-merge sprint AVFL, not per-story)

### Project Structure Notes

- **Single file touched:** `.claude/rules/impetus.md`. No other files require modification in this story. (Skill workflows that consume the ledger CLI are A4's scope, not A3's.)
- **Authority hierarchy:** Project-scoped rule under `.claude/rules/`. Cannot override global rules. Cascades to session-level behavior automatically.
- **CLI dependency on A1:** The rewritten session-start preflight references `momentum-tools practice-ledger summary` and `momentum-tools practice-ledger close-stale --age-days 15`. These subcommands MUST exist when A3 lands. A1 is the blocking dependency — do not begin A3 implementation until A1 is merged.
- **No downstream coupling within A3:** The Impetus rule does not import or compose other rules; this edit is self-contained.
- **Worktree note:** Per developer convention (intake stub commit `a5a1eb7`), this story is implemented in-place on `sprint/sprint-2026-05-26` — no worktree isolation required.

### References

- **Decision:** `_bmad-output/planning-artifacts/decisions/dec-033-practice-ledger-event-log-redesign-2026-05-25.md`
  - D5 — Routine-driven auto-close with session-start safety net
  - D6 — Signals/ absorbed entirely into practice-ledger
  - D9 — Impetus surfacing: honest counts, no inline enumeration
- **Assessment:** `_bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md` (Findings 4 and 10)
- **Cascade plan:** `.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md`
- **Blocking dependency:** `.momentum/stories/a1-practice-ledger-schema-cli-redesign-true-append-only.md`
- **Verification routing:** `skills/momentum/references/rules/verification-standard.md` (Section 1: `rule-hook` → behavioral trigger test)
- **Change-type template:** `skills/momentum/skills/create-story/references/change-types.md` (rule-hook section)
- **Current rule:** `.claude/rules/impetus.md`
- **Authority cascade:** `~/.claude/rules/authority-hierarchy.md`

## Dev Agent Record

### Agent Model Used

_To be populated by dev agent._

### Debug Log References

_To be populated by dev agent._

### Completion Notes List

_To be populated by dev agent._

### File List

_To be populated by dev agent._
