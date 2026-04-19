---
id: S-01
slug: feature-breakdown-skill
story_key: feature-breakdown-skill
title: "Build the /momentum:feature-breakdown Skill — Feature → Gap List → Triage"
epic_slug: ad-hoc
status: ready-for-dev
story_file: true
change_type: skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/feature-breakdown/SKILL.md
  - skills/momentum/skills/feature-breakdown/workflow.md
derives_from: []
---

# Build the /momentum:feature-breakdown Skill — Feature → Gap List → Triage

## User Story

As a Momentum developer, I can invoke `/momentum:feature-breakdown` with a feature slug from
`_bmad-output/planning-artifacts/features.json` and receive a triaged set of new story stubs,
decisions, and distillations that together close the gap between the feature's current story
set and what is required to ship that feature end to end — without the skill ever writing
directly to `features.json`, `stories/index.json`, or any planning artifact itself.

## Background / Context

**The practice gap this skill closes.** No existing skill answers the question "given this
feature, what stories are needed to ship it?"

- `feature-grooming` catalogs features and flags unmapped/understory features, but it does
  not author the missing work.
- `intake` creates one story stub at a time with no feature lens.
- `sprint-planning` assumes the backlog already contains what a feature needs.

Between these three skills there is no step that takes a feature and systematically enumerates
the stories required to ship it. `feature-breakdown` fills that gap.

**Role in the practice.** `feature-breakdown` is a pure orchestrator. It identifies gap
candidates and hands them to `momentum:triage` for classification and routing. It never
decides sufficiency itself and never writes to planning artifacts. Triage then routes items:

- ARTIFACT → `intake` (new story stub)
- DECISION → `decision` (decision document)
- DISTILL → `distill` (practice artifact update)
- SHAPING / DEFER / REJECT → `intake-queue.jsonl`

**Triage already supports this delegation pattern.** `skills/momentum/skills/triage/workflow.md`
Step 1 contains an "invoked from retro or assessment with a pre-enumerated list" branch.
`feature-breakdown` reuses that contract with `source_label = "feature-breakdown:{feature_slug}"`.

## Acceptance Criteria

### AC1 — Skill exists and is invocable
- `skills/momentum/skills/feature-breakdown/SKILL.md` exists with frontmatter fields
  `name: feature-breakdown`, a `description` beginning with a gerund and including a
  triggering phrase equivalent to "Use when the developer wants to enumerate stories
  needed to ship a feature", `model: claude-sonnet-4-6`, and `effort: high`.
- `SKILL.md` body is a single pointer line of the form `Follow the instructions in ./workflow.md`
  consistent with other Momentum skills.
- The skill is invocable as `/momentum:feature-breakdown`.

### AC2 — Workflow file exists and encodes the 7-step flow
- `skills/momentum/skills/feature-breakdown/workflow.md` exists.
- Uses the `<workflow>`, `<step>`, `<action>`, `<check>`, `<ask>`, `<output>`, `<critical>`,
  `<note>` tags consistent with other Momentum orchestrator workflows (e.g., `feature-grooming/workflow.md`,
  `triage/workflow.md`, `distill/workflow.md`, `quick-fix/workflow.md`).
- Encodes the 7-step workflow below:
  1. Load feature context.
  2. Load surrounding context (PRD, epics, architecture, stories index — with offset/limit).
  3. Parallel gap analysis (2 subagents, fan-out).
  4. Synthesize gap list.
  5. Developer review gate.
  6. Delegate to `momentum:triage`.
  7. Report.

### AC3 — Required and optional inputs
- Workflow accepts `feature_slug` as a required input.
- Workflow accepts an optional focus hint (e.g., "ingestion-side only") that narrows the
  gap search.
- Workflow fails fast with a clear, actionable message if `feature_slug` is not a key in
  `features.json` — the message names the missing slug and suggests running
  `/momentum:feature-grooming` to view available slugs.

### AC4 — Feature context load captures the right fields
- Step 1 reads `_bmad-output/planning-artifacts/features.json[feature_slug]` and captures
  at minimum: `acceptance_condition`, `value_analysis` (the full block including any
  "known gaps" paragraph), `system_context`, current `stories` array, and `status`.
- The captured context is passed to both parallel gap-analysis agents in Step 3.

### AC5 — Surrounding context load is scoped
- Step 2 reads relevant sections of `_bmad-output/planning-artifacts/prd.md`, `epics.md`,
  and `architecture.md`. It is not required to read these in full — `offset`/`limit` Read
  calls are used because these files are large.
- Step 2 reads `_bmad-output/implementation-artifacts/stories/index.json` filtered to
  stories in epics the feature touches and stories already on the feature. The filtering
  approach is described in the workflow (e.g., "read full file, filter in-memory by
  epic_slug").

### AC6 — Parallel gap analysis uses fan-out, not TeamCreate
- Step 3 spawns exactly 2 subagents in a single message using individual `Agent` tool
  calls (fan-out pattern per `~/.claude/rules/spawning-patterns.md`). It does NOT use
  `TeamCreate`.
- Agent A's role is "Acceptance-first" — given the `acceptance_condition`, enumerate the
  concrete capabilities required to satisfy it, check each against existing stories on
  the feature and in surrounding epics, and flag what is missing.
- Agent B's role is "Value-gap-first" — given the `value_analysis` "known gaps" paragraph
  (or the full `value_analysis` if no explicit gaps paragraph exists) and the current
  story set, identify implementation work that would close the gaps.
- Each agent returns a structured findings list — each finding has a short title, a
  one-line description, and a suggested class (ARTIFACT / DECISION / SHAPING).

### AC7 — Synthesis produces a deduplicated gap list
- Step 4 merges both agents' findings, deduplicates (same capability under different titles
  maps to one item), and produces a single structured gap list.
- Each item in the final list carries: short title, one-line description, source (Agent A,
  Agent B, or both), and a suggested class (ARTIFACT / DECISION / SHAPING).
- The suggested class is explicitly a suggestion — the workflow documents that triage
  makes the binding classification. `feature-breakdown`'s synthesis only emits ARTIFACT /
  DECISION / SHAPING suggestions; the additional outcomes triage may assign (DISTILL,
  DEFER, REJECT) are triage's own routing decisions and appear only in the final report
  (AC10), never in the gap list handed to triage.

### AC8 — Developer review gate before any delegation
- Step 5 presents the synthesized gap list to the developer and asks "These items will be
  handed to triage. Remove any before we proceed?" using an `<ask>` tag.
- No delegation to triage happens until the developer responds.
- The workflow supports the developer removing items from the list. If every item is
  removed, the workflow exits cleanly with a "no gaps to triage" output and does not
  invoke triage.

### AC9 — Triage delegation with correct source_label
- Step 6 invokes `momentum:triage` using the Skill tool with the approved gap list as a
  pre-enumerated source. The invocation mirrors the input shape triage already accepts
  (see `skills/momentum/skills/triage/workflow.md` Step 1's pre-enumerated-list branch).
- The invocation passes `source_label = "feature-breakdown:{feature_slug}"`.
- The workflow fails fast with a clear message if `momentum:triage` is unavailable — the
  message names the missing dependency.

### AC10 — Final report summarizes outcomes
- Step 7 summarizes after triage returns: feature slug, total gap count, classification
  outcomes (how many became ARTIFACT/DECISION/DISTILL/SHAPING/DEFER/REJECT), and pointers
  (paths) to any new story files, decision documents, or distill outcomes that triage
  reports in its output.
- The report uses concise, dry Momentum voice consistent with other orchestrator outputs.

### AC11 — Orchestrator purity: no direct writes to planning artifacts
- The workflow.md contains NO direct `Write` or `Edit` actions against any of:
  `features.json`, `stories/index.json`, `prd.md`, `epics.md`, `architecture.md`, or any
  file under `_bmad-output/planning-artifacts/` or `_bmad-output/implementation-artifacts/stories/`.
- All writes happen via delegated subagents (i.e., triage, which routes to intake / decision
  / distill which own their respective writes).
- The `<critical>` header of the workflow explicitly documents this boundary.

### AC12 — Skill is auto-discovered by the plugin
- A new skill under `skills/momentum/skills/<slug>/` with a valid SKILL.md is auto-discovered
  by the Momentum plugin; no additional registration is required.
- If the dev agent discovers that additional registration IS required (e.g., a plugin
  manifest entry), it stops and flags the finding to the developer rather than modifying
  unrelated infrastructure.

## Tasks / Subtasks

- [ ] Task 1 — Read reference skills and the development guide (AC1, AC2)
  - [ ] Read `skills/momentum/skills/feature-grooming/SKILL.md` and `workflow.md`
  - [ ] Read `skills/momentum/skills/triage/SKILL.md` and `workflow.md` — especially
        Step 1's pre-enumerated-list branch
  - [ ] Read `skills/momentum/references/agent-skill-development-guide.md` in full
  - [ ] Read `skills/momentum/skills/distill/workflow.md` and
        `skills/momentum/skills/quick-fix/workflow.md` as structural references

- [ ] Task 2 — Create `skills/momentum/skills/feature-breakdown/SKILL.md` (AC1)
  - [ ] Frontmatter: `name: feature-breakdown`; `description` beginning with a gerund and
        containing the triggering phrase from AC1; `model: claude-sonnet-4-6`; `effort: high`
  - [ ] Body: a single pointer line — `Follow the instructions in ./workflow.md`

- [ ] Task 3 — Create `skills/momentum/skills/feature-breakdown/workflow.md` (AC2–AC11)
  - [ ] Goal statement + orchestrator purity `<critical>` block referencing features.json,
        stories/index.json, and other planning artifacts as off-limits
  - [ ] Initialization section — load config from `_bmad/bmm/config.yaml`; resolve
        `planning_artifacts` and `implementation_artifacts` paths
  - [ ] Step 1 — Load feature context (AC3 input validation + AC4 field capture)
  - [ ] Step 2 — Load surrounding context (AC5 scoped reads)
  - [ ] Step 3 — Parallel gap analysis (AC6 fan-out with 2 Agent spawns in one message)
  - [ ] Step 4 — Synthesize gap list (AC7 deduplication + structured output)
  - [ ] Step 5 — Developer review gate (AC8 `<ask>` + remove-all exit path)
  - [ ] Step 6 — Delegate to triage (AC9 Skill invocation + correct source_label +
        fail-fast branch)
  - [ ] Step 7 — Report (AC10 summary format)

- [ ] Task 4 — Verify discoverability (AC12)
  - [ ] After the SKILL.md and workflow.md are written, confirm the skill is listed as
        `/momentum:feature-breakdown` by running `/plugin` or inspecting the plugin
        skill listing (reload if necessary)
  - [ ] If not auto-discovered, stop and flag to the developer — do NOT modify plugin
        infrastructure to force discovery

## Dev Notes

### Frontmatter schema authority

`skills/momentum/references/agent-skill-development-guide.md` is the authoritative source
for the frontmatter schema, description trigger phrasing, system prompt structure, and
invocation control. Read it before authoring SKILL.md.

### Triage input shape

`skills/momentum/skills/triage/workflow.md` Step 1 describes the shape triage expects when
invoked with a pre-enumerated list (retro/assessment branch). Mirror exactly that input
shape — do not invent a new one. Pass the `source_label` field at the top level so triage
can prefix findings-ledger entries correctly.

### Fan-out, not TeamCreate

Per `~/.claude/rules/spawning-patterns.md`: the two gap-analysis agents are independent
(they do not need to talk to each other during execution) so this is fan-out — multiple
`Agent` tool calls in a single message. Do not use `TeamCreate`. The workflow should
state this rationale in a `<note>` or `<critical>` block.

### Comparable skill structure

The closest structural analogue is `skills/momentum/skills/distill/workflow.md` — also an
orchestrator that runs a discovery/enumeration phase and delegates writes. Reuse its phase
pattern and voice. Voice is the Impetus voice: dry, confident, forward-moving. Use the
established symbol vocabulary (check / arrow / circle / bang / cross / dot).

### Large-file reading

`prd.md`, `epics.md`, `architecture.md`, and `stories/index.json` are all large. Always
use `offset`/`limit` on Read calls. For `stories/index.json`, read once and filter
in-memory — do not paginate through attempting to match entries.

### What this skill is NOT responsible for

- Modifying `feature-grooming` so it auto-invokes `feature-breakdown` — separate follow-up.
- Modifying `sprint-planning` to gate on feature coverage — separate follow-up.
- Any changes to `features.json` schema — out of scope.
- Evals for the new skill — separate follow-up.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/feature-breakdown/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-fails-fast-on-missing-feature-slug.md`, `eval-produces-deduplicated-gap-list.md`, `eval-delegates-to-triage-with-correct-source-label.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

> **Scope exception for this story:** The developer has explicitly moved evals to a separate follow-up (see "Out of scope" in the top-level story). Task 1–4 of THIS story do not require evals to be written. The EDD guidance is preserved here because if the dev agent discovers a subtle behavioral gap during implementation, writing a minimal scratch eval is still the right tool — it just doesn't block DoD.

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented SKILL.md against story ACs)

### Gherkin black-box separation (Decision 30)

Gherkin specs for this quick-fix exist in `_bmad-output/implementation-artifacts/sprints/quickfix-feature-breakdown-skill/specs/` but are off-limits to the dev agent. The dev agent implements against the plain English ACs in this story file only, never against `.feature` files.

## Definition of Done

- [ ] `skills/momentum/skills/feature-breakdown/SKILL.md` exists with valid frontmatter
      per `agent-skill-development-guide.md`
- [ ] `skills/momentum/skills/feature-breakdown/workflow.md` exists encoding all 7 steps
- [ ] Skill is discoverable as `/momentum:feature-breakdown`
- [ ] Workflow passes the orchestrator-purity check (no direct writes to planning artifacts
      or the stories index)
- [ ] SKILL.md `description` field is ≤150 characters (count the actual characters)
- [ ] SKILL.md frontmatter includes `model:` and `effort:` fields with correct values
- [ ] SKILL.md body is ≤500 lines / ≤5000 tokens (overflow content belongs in `references/`)
- [ ] AVFL checkpoint passes on the story + workflow file before implementation is
      considered complete
- [ ] Story status transitioned to done
