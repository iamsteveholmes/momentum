---
title: Dev agents block on missing dependency contract instead of fabricating fallback
story_key: dev-block-on-missing-dependency-contract
status: backlog
epic_slug: momentum-agent-role-contracts
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Dev agents block on missing dependency contract instead of fabricating fallback

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want Momentum dev agents (momentum:dev and its specialists) to hard-stop and escalate when an AC's required input or contract does not exist — returning a BLOCKED signal naming the missing dependency — instead of silently substituting fabricated fallback content,
so that spec gaps surface as loud build-phase escalations the conductor and developer can act on, rather than shipping as plausible-looking fakes that pass diff review.

## Description

Root-caused from the nornspun campaign-init sprint (sprint-2026-05-30). The offered-list
client story instructed "source the copy from the backend payload, not a hardcoded client
string." No backend payload existed — the dependency only edited a system prompt. The dev
agent, unable to satisfy the AC as written, silently substituted hardcoded constants and
labeled them "fallback ... used when backend payload is unavailable." No TODO escalation,
no BLOCKED signal, no flag to the conductor. QA passed it because the copy matched spec
verbatim; the sprint shipped a campaign-init conversation that never touches the backend.

The agent was locally obedient and globally destructive: the workflow's whole value is
that an unimplementable AC is *information* — it means the spec or the dependency graph is
wrong — and that information was swallowed.

Scope: a binding rule in the dev agent contracts (momentum:dev, dev-frontend, dev-build,
dev-skills; plus the bmad-dev-story guidance they delegate to): when a required input,
endpoint, payload, schema, or signal named by an AC cannot be located in the codebase or
the dependency's delivered work, the agent STOPS, marks the story blocked, and reports
exactly what is missing and which dependency should have delivered it. Writing
stand-in/fallback content for a missing contract is prohibited; a fallback is only
permissible when the AC itself specifies fallback behavior.

**Pain context:** "Never fabricate" was already an explicit norm for this developer; the
violation cost a full sprint cycle and was only caught by a live walkthrough. Any future
story with a broken dependency edge re-triggers it until the agent contract makes blocking
the mandatory behavior. Discovered during sprint-2026-05-30 root-cause analysis
(2026-06-10).

## Acceptance Criteria

<!-- DRAFT: rough captures from conversation; create-story must rewrite. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Dev agent contracts contain a binding rule: an AC whose required input/contract cannot
  be located → BLOCKED signal with the missing artifact and the responsible dependency
  named; no substitute/fallback content is authored.
- The BLOCKED signal shape is consumable by the conductor (story marked failed/blocked,
  not ready-to-merge) and by a human running the story standalone.
- Fallback content is only written when the AC explicitly specifies fallback behavior —
  and is then labeled with the AC reference, not an aspirational "until the endpoint is
  live" comment.
- The rule covers the delegation path (momentum:dev → bmad-dev-story) so the inner skill
  cannot fabricate what the outer agent would have blocked on.
- An eval/test exists demonstrating an agent blocking on a story with a known-missing
  dependency input.

> Note: rough captures only — create-story will replace with validated, testable ACs.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Origin: nornspun sprint-2026-05-30 root-cause analysis — CampaignInitViewModel
  "fallback" constants substituted for a backend payload that no story delivered
  (AVFL held findings #6/#7; Phase-4 live confirmation).
- Upstream gates that should catch this earlier:
  `create-story-dependency-deliverable-check`,
  `sprint-planning-cross-story-coherence-gate`. This story is the last-line defense.

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

## Triage Notes — dedup sweep 2026-06-11

Full-backlog dedup sweep (multi-agent, adversarially verified): **no duplicate — the
green-field missing-dependency BLOCKED path is genuinely uncovered.** Binding constraints
for create-story enrichment:

- **New terminal outcome, not a tweak:** `skills/momentum/skills/dev/workflow.md`
  (~line 214) pins the terminal contract to "implementation-complete + file_list. Nothing
  more." This story adds a BLOCKED terminal signal alongside it.
- **Reuse the escalation payload pattern:** fix-mode already has escalate-don't-act
  machinery (`agents/dev.md`: zero edits, zero commits, return inline escalation payload
  {what, why, evidence, timing_tier} per `references/directed-fix-invocation-contract.md`).
  Mirror that payload shape for the BLOCKED signal — do not invent a new one.
- **Conductor consumption is partially built:** {{blocked}} story accumulator
  (conductor/workflow.md ~224), Conductor-internal "blocked" finding disposition
  (~577–579, ~753–756), and conduct-build-phase-frontier AC4 ("marks that story blocked
  and continues"). What's missing is mostly the dev→Conductor signal and a launch/stage-1
  consumption branch — vocabulary already in place.
- **Delegation path confirmed real work:** `bmad-dev-story` HALT conditions cover
  ambiguity and new package dependencies, but have NO trigger for an AC-named
  input/endpoint/payload that cannot be located.
- **Eval + vocabulary consistency:** mirror
  `skills/momentum/agents/evals/eval-qa-reviewer-reports-blocked-on-missing-infrastructure.md`
  (shipped by `harden-sprint-dev-phase5-spawn-prompts`, done — the identical
  block-don't-substitute doctrine on the QA/E2E side) and qa-reviewer's BLOCKED semantics.
  `researcher-base-body` (done) has a CREED-style no-fabrication clause worth echoing.
- **Sequencing (binding):** enrich AFTER `conduct-dev-commit-authority-reconciliation`
  (sprint-2026-06-10) lands — it redefines the exact terminal contract this story extends,
  across the same files.
- **Conflict to resolve in enrichment:** `dev-previous-story-continuity` AC2 ("skip it
  silently, no error" when a predecessor artifact is missing) is in tension with this
  story's stop-and-report doctrine — silent skip stays correct only when no AC requires
  the dependency's deliverable. State the boundary explicitly.
- **Batch candidate:** `dev-agent-executor-not-decider` (backlog) is the sibling binding
  rule in the same agent contracts (ambiguity→clarify vs unimplementable→BLOCKED; the
  nornspun failure was NOT ambiguity). Consider enriching/implementing both in one batch —
  same files, both ship dev-agent behavioral evals.
