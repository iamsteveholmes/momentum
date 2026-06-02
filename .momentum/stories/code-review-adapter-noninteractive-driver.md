---
title: "Code-review adapter: non-interactive bmad-code-review driver"
story_key: code-review-adapter-noninteractive-driver
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on: []
touches:
  - skills/momentum/skills/code-reviewer/SKILL.md
  - skills/momentum/skills/code-reviewer/workflow.md
---

# Code-review adapter: non-interactive bmad-code-review driver

## Story

As the Conductor (the top-level session orchestrator that owns the conduct build phase),
I want a thin adapter that drives the existing adversarial code review tool in a non-interactive, report-only mode against a single story's diff,
so that the per-story review leg can run autonomously inside the build phase without ever pausing to ask a human for input.

## Description

conduct is the in-session, per-story, autonomous-build, single-end-gate rewrite of the
sprint development workflow. The Conductor runs every story's build and review without
mid-stream human prompts, surfacing a single human end-gate at the end of the flow.

The existing adversarial code review tool was built for an interactive, human-in-the-loop
session: it can pause and HALT for confirmation, and it can be asked to apply fixes. Neither
behavior is compatible with an autonomous per-story leg. The Conductor needs a way to call
that review capability such that it always runs to completion, always returns its findings,
never blocks on a prompt, and never mutates files.

This story delivers a thin transport adapter that:

- Drives the code review tool in report-only, non-interactive mode against a single story diff.
- Suppresses the tool's HALT/confirmation behavior so the run completes without input.
- Does not apply any fixes — the adapter only reports findings (fix application is a separate
  leg owned elsewhere in conduct).
- Verifies that the code review tool's required configuration scaffolding is present before
  running, and surfaces an actionable error if it is missing rather than failing opaquely.

This is the lowest-effort P0 work item for the per-story review leg: it unblocks every
downstream story that depends on having review findings available. It is pure transport —
it carries findings from the review tool to the Conductor and does not interpret, classify,
triage, or act on them.

Pain context: without this adapter the review tool cannot be invoked autonomously at all —
its interactive HALTs would stall the build phase the moment a story is reviewed, and its
fix-application mode would mutate the working tree out from under the Conductor (which owns
all git mutation). The adapter removes both hazards with a single non-interactive,
report-only entry point.

Source decisions: DEC-035 (adopt conduct; one human gate at the end; auto-fix loop must be
legible) and DEC-036 (narrow stakes-gated escalation amends DEC-035). This story is UNCHANGED
by the DEC-036 amendment — it is pure transport and carries no classification, escalation,
disposition, or auto-fix logic. The DEC-036 surface (stakes classes, dispositions, timing
tiers) lands in separate stories that consume this adapter's output, not in the adapter itself.

Governing spec: section 4 (tool decision — the adversarial review tool is the chosen engine
for the per-story review leg) and section 10 (gap map — the config-scaffolding gap this story
closes), plus open question 3 (the required configuration scaffolding and the actionable error
when it is absent).

## Acceptance Criteria

1. Invoking the adapter against a single story's diff runs the adversarial code review tool
   and returns the review's findings, without pausing or waiting for any human input at any
   point during the run.

2. The adapter runs the review tool in report-only mode: it produces findings and makes no
   changes to any tracked file in the working tree. After a run completes, the working tree
   is byte-for-byte unchanged from before the run.

3. The adapter suppresses every interactive HALT, confirmation prompt, or pause that the
   underlying review tool would normally raise in an interactive session, so the run always
   proceeds to completion unattended.

4. When the review tool finds issues, the adapter returns those findings to the caller in full
   (it does not drop, summarize away, or silently swallow findings); when the review tool finds
   nothing, the adapter returns an explicit empty/no-findings result rather than an error.

5. Before driving the review tool, the adapter verifies that the review tool's required
   configuration scaffolding is present. If the scaffolding is present, the adapter proceeds
   to run normally.

6. If the required configuration scaffolding is absent, the adapter does not attempt a
   silent or partial run; instead it surfaces a clear, actionable error message that names
   what is missing and what the operator must provide, so the failure is diagnosable rather
   than opaque.

7. The adapter is scoped to a single story's diff per invocation: the review it drives is
   bounded to the changes for the story under review and does not pull in unrelated changes.

8. The adapter performs transport only — it does not classify findings by stakes, assign
   dispositions, escalate, triage, or apply any fix. (DEC-036 amendment scoping: stakes
   classification, dispositions of fixed / dismissed / triaged-out / escalated, and the
   mid-flight vs. end-gate-expanded timing tiers are explicitly out of scope for this adapter
   and are owned by separate stories that consume this adapter's findings.)

## Tasks / Subtasks

- [ ] Add an adapter entry point in the code-reviewer skill that accepts a single story's diff
      as input and drives the adversarial code review tool against it.
- [ ] Configure the drive to run in report-only mode so the adapter applies no fixes and the
      working tree is left unchanged (AC2, AC8).
- [ ] Configure the drive to run non-interactively: suppress/auto-answer every HALT,
      confirmation, or pause so the run completes without human input (AC1, AC3).
- [ ] Return the review tool's findings to the caller in full, and return an explicit
      no-findings result when the review is clean (AC4).
- [ ] Add a pre-run check that verifies the review tool's required configuration scaffolding is
      present before driving the tool (AC5).
- [ ] On missing configuration scaffolding, emit a clear, actionable error that names what is
      missing and what to provide; do not attempt a partial/silent run (AC6).
- [ ] Confirm or supply the minimal configuration file the review tool expects
      (`_bmad/bmm/config.yaml`) so the pre-run check has a known-good target to verify (AC5, open
      question 3).
- [ ] Bound the adapter's review to the single story's diff per invocation (AC7).
- [ ] Update `skills/momentum/skills/code-reviewer/SKILL.md` and
      `skills/momentum/skills/code-reviewer/workflow.md` to document the non-interactive,
      report-only adapter mode and its pre-run config check.
- [ ] State explicitly in the skill docs that the adapter is pure transport and carries no
      stakes classification, disposition, escalation, or fix-application logic (AC8).

## Dev Notes

This is a `skill-instruction` change: the deliverable is instruction edits to the code-reviewer
skill (`SKILL.md` + `workflow.md`) that define the adapter mode. Verification is `skill-invoke`
— the adapter is exercised by invoking the skill against a story diff and observing its outputs
and side effects (findings returned, working tree unchanged, config-missing error surfaced).

Key technical grounding:

- The underlying engine is the existing adversarial code review tool. The adapter is a thin
  driver over it — it does not reimplement review logic, it constrains how the tool is invoked.
- Report-only / non-interactive are the two invariants. Report-only means no fix application and
  no working-tree mutation (the Conductor owns all git mutation; the adapter must never touch the
  tree). Non-interactive means every HALT/confirmation the tool would raise in a human session is
  suppressed or auto-answered so the run never blocks.
- The review tool expects a configuration file at `_bmad/bmm/config.yaml`. Confirm whether this
  scaffolding is present in the project; if absent, supply a minimal config sufficient for the
  tool to run. The pre-run check (AC5/AC6) verifies this file's presence and, when missing,
  raises an actionable error naming the missing path rather than letting the tool fail opaquely
  deep in its own run. This addresses spec open question 3.
- UNCHANGED by DEC-036: this adapter is pure transport. It carries findings; it does not
  classify them by stakes class (security/auth-isolation; irreversible/destructive;
  high-blast-radius/architecture; routine), does not assign dispositions (fixed / dismissed /
  triaged-out / escalated), does not select a timing tier (end-gate-expanded vs. mid-flight),
  and does not apply fixes. All of that lives in separate stories that consume this adapter's
  output. Keeping this story narrow is deliberate: it is the lowest-effort P0 that unblocks the
  per-story review leg without entangling it with the DEC-036 escalation surface.

Governing spec sections (cite by number):

- Spec section 4 — tool decision: the adversarial code review tool is the chosen engine for the
  per-story review leg; the adapter drives that engine.
- Spec section 10 — gap map: identifies the configuration-scaffolding gap this adapter closes.
- Spec open question 3 — the required configuration scaffolding and the actionable error path
  when it is absent (AC5/AC6).

### References

- Epic: `momentum-sprint-orchestration` — see `_bmad-output/planning-artifacts/epics.json`.
- Decision: DEC-035 — adopt conduct; one human end-gate; legible auto-fix loop. This adapter is
  the non-interactive transport that lets the per-story review leg run inside the
  single-end-gate flow.
- Decision: DEC-036 — narrow, stakes-gated mid-flight escalation amending DEC-035. This story is
  explicitly UNCHANGED by DEC-036 (pure transport; classification/escalation/disposition are
  out of scope and owned by separate stories).
