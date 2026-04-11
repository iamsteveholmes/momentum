---
id: S-01
slug: implement-momentum-distill-skill
story_key: implement-momentum-distill-skill
title: "Implement /momentum:distill — Practice Artifact Distillation Skill"
epic_slug: ad-hoc
status: backlog
story_file: true
change_type: skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/distill/SKILL.md
  - skills/momentum/skills/distill/workflow.md
  - skills/momentum/skills/avfl/references/framework.json
  - skills/momentum/skills/retro/workflow.md
---

# Implement /momentum:distill — Practice Artifact Distillation Skill

## User Story

As a Momentum developer, I can invoke `/momentum:distill` at any point during a session or
from retro Phase 5 to immediately capture a session learning and apply it to the appropriate
practice artifact, so that learnings are distilled in minutes rather than waiting weeks for
sprint cycle processing.

## Background / Context

**The practice gap distill closes:** All Momentum findings currently must survive sprint
planning before landing in rules files, references, or skill prompts. Even a small, obvious
rule addition — the kind that takes one sentence to express — must wait for the next sprint
cycle to be captured. This multi-week lag means learnings are lost, deferred, or forgotten
before they reach the practice layer. Retro findings sit as story stubs that may never be
activated.

**FR97 (Practice Artifact Distillation):** The developer can invoke `/momentum:distill` to
capture a session learning or retro finding and immediately apply it to the appropriate
practice artifact, without sprint activation or backlog management. The skill is the
practice-artifact analogue of `/momentum:quick-fix`: where quick-fix handles code stories,
distill handles practice artifacts (rules, references, skill prompts, spec additions).

**FR96 (Retro Signal Classification):** Each retro finding carries a causal signal type
(`Context | Instruction | Workflow | Failure`) that determines which practice artifact
needs updating. In retro Phase 5, Tier 1 findings (small, immediately applicable) route to
`/momentum:distill` instead of creating story stubs. Tier 2 findings (structural changes)
continue through Phase 5's existing stub creation path.

**Decision 42 (Distill Execution Path and AVFL Profile):** Distill is the fourth execution
path alongside epic orchestration, sprint orchestration, and quick-fix. The discovery phase
runs two parallel agents (Enumerator maps existing content; Adversary challenges redundancy
and conflicts) before any changes are written. Fix scope is classified during discovery into
one of three paths: project-local, Momentum-level in the Momentum project, or Momentum-level
in an external project. The AVFL post-change pass uses a lightweight distill profile:
two subagents, single pass, Sonnet at medium-low effort, no fix iterations.

**Motivating research:** `_bmad-output/research/momentum-vs-fowler-feedback-flywheel-2026-04-10/final/`
documents the structural gap between Momentum's current feedback latency and Fowler's
feedback flywheel model. Key finding: Momentum lacks a mechanism for immediate artifact
updates from session learnings.

## Acceptance Criteria

### AC1 — Skill is invocable
- `skills/momentum/skills/distill/SKILL.md` exists with `name: distill`, model: sonnet,
  effort: medium, and points to `workflow.md`
- `skills/momentum/skills/distill/workflow.md` exists and is a complete, executable workflow
- The skill is invocable as `/momentum:distill` from any session context

### AC2 — Discovery phase: two parallel agents before any writes
- When distill is invoked, a discovery phase runs before any files are modified
- Two parallel agents execute in the discovery phase:
  - **Enumerator:** maps existing content in the candidate practice artifact(s) — rules,
    references, skill prompts — and identifies where the learning would land
  - **Adversary:** challenges the proposed change for redundancy (is this already stated
    elsewhere?), conflict (does this contradict an existing rule?), and scope fit (is the
    right artifact targeted?)
- Discovery completes before any write subagent is spawned
- Orchestrator purity is maintained: the distill workflow never writes files directly

### AC3 — Fix scope classification determines execution path
- During discovery, the skill classifies the fix scope into one of three paths:
  - **Path A — Project-local:** the learning applies to a rule or reference scoped to the
    current project (`.claude/rules/`, project-local references)
  - **Path B — Momentum-level, in Momentum project:** the learning applies to Momentum's own
    practice files, and the current working directory IS the Momentum project
  - **Path C — Momentum-level, in external project:** the learning applies to Momentum's own
    practice files, but the current working directory is NOT the Momentum project
- Classification is determined during discovery, not as a post-hoc step after writing

### AC4 — Path A: applies change to project-local artifact and commits
- When fix scope is Path A, distill writes the change to the appropriate project-local
  practice file (via a write subagent — not the orchestrator directly)
- Commits the change with a conventional commit message

### AC5 — Path B: applies change to Momentum files, bumps plugin version, commits and pushes
- When fix scope is Path B (Momentum-level, in Momentum project), distill writes the change
  to the appropriate Momentum practice file (via a write subagent)
- Bumps the plugin patch version in `skills/momentum/.claude-plugin/plugin.json`
- Commits and presents a push summary for developer approval before pushing

### AC6 — Path C: presents defer-to-retro OR generate-remote-prompt options
- When fix scope is Path C (Momentum-level, in external project), distill does NOT attempt
  to modify Momentum files in another project
- Presents two options to the developer:
  1. **Defer to retro:** records the finding in the findings-ledger with `origin: distill`
     for retro Phase 5 processing
  2. **Generate remote prompt:** produces a self-contained prompt the developer can paste
     into a Momentum session to apply the change

### AC7 — Two-tier model: Tier 1 commits immediately, Tier 2 creates story stub
- **Tier 1 (small, immediately applicable):** rule addition, reference entry, prompt
  clarification — distill applies the change, runs AVFL, and commits
- **Tier 2 (structural changes):** changes requiring multi-file refactoring, new skill
  creation, or workflow redesign — distill creates a story stub in
  `_bmad-output/implementation-artifacts/stories/` instead of writing changes directly
- The Tier classification is determined during discovery, informed by Adversary output

### AC8 — Post-change AVFL using distill profile
- After writing changes (Tier 1 only), distill invokes `momentum:avfl` with the distill
  profile:
  - `profile: distill`
  - `output_to_validate`: only the changed file(s)
  - Model: sonnet, effort: medium-low
  - Single pass, two subagents (Enumerator + Adversary framings)
  - No fix iterations — AVFL output informs a developer-prompted correction or a clean commit
- If AVFL returns findings, they are presented to the developer with a correction-or-commit
  choice

### AC9 — Audit trail: findings-ledger entry with `origin: distill`
- Every distill invocation writes a findings-ledger entry to
  `~/.claude/momentum/findings-ledger.jsonl`
- The entry includes `origin: distill`, the artifact path modified (or targeted for Path C),
  the learning description, Tier classification, and path taken (A/B/C)
- This enables FR33 ratio tracking to count distillation-origin fixes separately from
  code-review-origin fixes

### AC10 — Retro Phase 5 integration
- `skills/momentum/skills/retro/workflow.md` Phase 5 is modified to add a classification
  check before stub creation
- For each priority action item in the retro audit, if `signal_type` is set AND the finding
  is Tier 1 (immediately applicable, small rule/reference change), distill is invoked
  instead of creating a stub
- Tier 2 retro findings continue through the existing stub creation path unchanged
- The Phase 5 step documents the Tier classification logic used to route each finding

### AC11 — Distill AVFL profile added to framework.json
- `skills/momentum/skills/avfl/references/framework.json` contains a `distill` profile entry
- Profile specifies: two subagents (Enumerator + Adversary), single pass (no multi-lens
  parallelism), model sonnet at medium-low effort, no fix iterations
- Profile is named `distill` and is a peer of existing profiles (`gate`, `checkpoint`,
  `full`, `scan`)

## Tasks / Subtasks

- [ ] Task 1 — Create `skills/momentum/skills/distill/SKILL.md` (AC1)
  - [ ] Frontmatter: `name: distill`, `model: claude-sonnet-4-6`, `effort: medium`,
        `description` front-loaded to trigger for session learnings and retro Phase 5 Tier 1
  - [ ] Body: "Follow the instructions in ./workflow.md"

- [ ] Task 2 — Create `skills/momentum/skills/distill/workflow.md` (AC1–AC10)
  - [ ] `<critical>` elements: orchestrator purity, discovery-before-write invariant,
        no direct file writes from orchestrator
  - [ ] Phase 1 (Discover): spawn Enumerator + Adversary in parallel; receive scope
        classification and Tier determination from their output
  - [ ] Phase 2 (Route): branch on Path A / B / C and Tier 1 / Tier 2
  - [ ] Phase 3 (Apply): Tier 1 — spawn write subagent for appropriate path;
        Tier 2 — spawn create-story subagent for stub
  - [ ] Phase 4 (Validate): invoke `momentum:avfl` with `profile: distill` on changed files
        (Tier 1 only)
  - [ ] Phase 5 (Commit): commit changes, bump plugin version for Path B, present push
        summary
  - [ ] Phase 6 (Ledger): write findings-ledger entry with `origin: distill`

- [ ] Task 3 — Add `distill` profile to `framework.json` (AC11)
  - [ ] Add `distill` entry to `validation_profiles` section
  - [ ] Specify: 2 subagents (enumerator + adversary framings), single-pass, Sonnet
        medium-low, no fix iterations, scope limited to changed files only

- [ ] Task 4 — Modify `skills/momentum/skills/retro/workflow.md` Phase 5 (AC10)
  - [ ] Add Tier classification logic before stub creation loop
  - [ ] For Tier 1 findings with `signal_type` set: invoke `momentum:distill` instead of
        writing stub
  - [ ] For Tier 2 findings: continue existing stub creation path unchanged
  - [ ] Document which findings went to distill vs. stub in Phase 5 output

## Dev Notes

### Distill AVFL profile in framework.json

The distill profile is structurally distinct from existing profiles:
- **No multi-lens parallelism:** existing profiles run validators across structural,
  accuracy, and coherence lenses. Distill runs a single pass — one Enumerator framing, one
  Adversary framing, no lens differentiation.
- **No fix iterations:** AVFL's fixer is not invoked. Findings go to the developer for a
  manual correction-or-commit decision.
- **Scope: changed files only.** The `output_to_validate` passed to the distill AVFL is the
  specific file(s) modified by the change — not the full document or skill corpus.
- Model: Sonnet, effort at the lower end of medium (equivalent to `effort: low-medium` —
  express in framework.json as whatever token-budget tier maps to ~10k output tokens).

### Retro Phase 5 integration — read the existing step carefully

The current Phase 5 loop creates story stubs for ALL priority action items. The integration
adds a pre-loop classification step:

```
For each priority action item:
  1. Check if signal_type is set on the finding (from Phase 4 classification)
  2. If signal_type set AND finding is Tier 1 (small rule/reference/prompt change):
     → Invoke momentum:distill with the finding as input
     → Record that this finding was distilled (not stubbed)
  3. If signal_type not set OR finding is Tier 2:
     → Continue with existing stub creation path
```

The Tier 1 vs. Tier 2 determination in retro Phase 5 follows the same heuristics as
distill's own discovery phase: Tier 1 = single-sentence rule addition, reference entry
update, or prompt clarification. Tier 2 = multi-file change, new skill, or workflow redesign.

### Three-path routing: determined in discovery, not post-hoc

The Enumerator and Adversary agents receive the current working directory context and the
Momentum project path (if different). They classify fix scope as part of their discovery
output. The orchestrator does NOT re-classify after the fact — it reads the path
determination from the discovery output and routes accordingly.

### Orchestrator purity

Decision 3d applies: the distill workflow must not write files directly. Every file change
happens through a spawned write subagent. The Adversary and Enumerator agents are read-only.
The write subagent is spawned only after discovery completes and the developer sees the
proposed change and confirms.

### Path C: generating a remote prompt

For Path C (Momentum-level fix from an external project), the "generate remote prompt" option
produces a self-contained markdown block with:
- The finding description
- The specific file to modify in the Momentum project
- The proposed change (the exact text addition/modification)
- Instructions for applying via `/momentum:distill` in a Momentum session

### Reference: comparable skill structure

`skills/momentum/skills/quick-fix/workflow.md` is the closest structural analogue. Key
differences in distill:
- No worktree: distill operates directly on the working tree (practice files, not code)
- No Gherkin/spec impact phase: distill is intentionally lean
- No E2E validation: AVFL distill profile replaces the full validation team
- Discovery phase is new: quick-fix starts with a developer description; distill starts with
  two agents reading existing content before proposing changes

## Definition of Done

- [ ] `skills/momentum/skills/distill/SKILL.md` exists and is valid per agent-skill-development-guide.md
- [ ] `skills/momentum/skills/distill/workflow.md` exists with all 6 phases implemented
- [ ] `distill` profile added to `skills/momentum/skills/avfl/references/framework.json`
- [ ] `skills/momentum/skills/retro/workflow.md` Phase 5 updated with Tier routing
- [ ] AVFL distill profile validates clean against its own spec in framework.json
- [ ] Story status transitioned to done
