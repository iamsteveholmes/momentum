---
title: Build the qa-reviewer → canonical finding schema normalization adapter the Conductor already consumes
story_key: conduct-qa-reviewer-normalization-adapter
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
  - agent-definition
verification_method_advisory: skill-invoke
depends_on:
  - directed-fix-finding-schema
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/agents/qa-reviewer.md
  - skills/momentum/skills/conductor/evals/
---

# Build the qa-reviewer → canonical finding schema normalization adapter the Conductor already consumes

Status: ready-for-dev

## Story

As the Conductor orchestrating stage-2 of a conduct build,
I want qa-reviewer producer-format findings deterministically normalized to the canonical finding schema before they merge into `{{stage2_findings}}`,
so that the directed fix loop's input contract holds on every story — no finding enters Phase B missing `severity`, `legitimate`, `type`, `suggested_fix`, or `story_slug`.

## Description

The Conductor consumes a qa-reviewer output format the agent explicitly does not emit, and the adapter both sides point to was never built. This is a confirmed finding from the 2026-06-09 conductor effectiveness review (adversarially verified, high confidence).

**Conductor side:** `skills/momentum/skills/conductor/workflow.md` stage-2 (REVIEWER A block, ~lines 400–402) claims REVIEWER A "Returns: per-AC classification (VERIFIED / PARTIAL / MISSING / BLOCKED) with stakes_class on each finding, normalized to the canonical finding schema (finding-schema.md)." The merge step (~lines 419–426) then asserts every finding in the merged `{{stage2_findings}}` carries the canonical base fields: `story_slug`, `source`, `stakes_class`, `severity`, `verdict`, `type`, `location`, `summary`, `detail`, `evidence`, `legitimate`, `ac_id`, `suggested_fix`.

**Agent side:** `skills/momentum/agents/qa-reviewer.md` line 173 says verbatim that the agent's output shape "is not the canonical normalized finding shape… An external normalization adapter (owned by the `directed-fix-finding-schema` story) maps qa-reviewer findings into the full canonical shape — adding `source: qa-reviewer`, `legitimate`, `severity`, `type`, `suggested_fix`, and `story_slug`." The agent's Output Format (~lines 139–171) genuinely contains no `severity`, `legitimate`, `type`, or `suggested_fix` fields — its findings carry only AC, Verdict, stakes_class, Location, Summary, Detail, Evidence.

**The adapter does not exist.** Repo-wide grep finds "normalization adapter" only at qa-reviewer.md:173. The story `directed-fix-finding-schema` (per `.momentum/stories/index.json`, status: done) scoped ONLY the schema document — its 14 ACs and 11 tasks all target `skills/momentum/references/finding-schema.md`; an adapter was never in its scope. Contrast REVIEWER B: its normalization is real, implemented in `skills/momentum/skills/code-reviewer/workflow.md` step 4.5 ("Normalize surviving findings to the canonical schema and populate stakes_class"). REVIEWER A has no equivalent.

**Consequence:** the Conductor passes `{{stage2_findings}}` straight to the Phase B fixer (step 2.S3, workflow.md ~line 430 and ~574), so the fix loop's input contract is broken at this seam on every story that produces qa-reviewer findings. The fixer's disposition rules key on `legitimate` and `stakes_class`; downstream lookups (workflow.md lines ~614, ~619, ~637, ~642) recover `summary`, `evidence`, `suggested_fix`, `stakes_class` from `{{stage2_findings}}` records — fields qa-reviewer findings never carried.

**Chosen venue (binding for this story):** implement the normalization as an explicit Conductor-side action in stage-2 of `conductor/workflow.md`, immediately after REVIEWER A returns and before the merge/dedup with REVIEWER B findings. Do NOT extend qa-reviewer.md's Output Format to emit canonical-shape findings. Rationale: (a) this mirrors the existing REVIEWER B architecture, where normalization lives in the consuming/adapter layer (code-reviewer workflow.md step 4.5), keeping producer formats clean; (b) qa-reviewer.md:173 already states "No change to this output template is required here" — the producer contract is stable and downstream of a deliberate design; (c) the fields to be added (`legitimate: true`, `source`, `story_slug`) are facts the Conductor knows authoritatively, not judgments the reviewer should re-make. The qa-reviewer.md schema note is then corrected to name the Conductor's stage-2 normalization as the owner, so both artifacts agree and no dangling adapter reference remains.

## Acceptance Criteria

1. `skills/momentum/skills/conductor/workflow.md` stage-2 contains an explicit normalization action that runs immediately after REVIEWER A returns and before the merge/dedup with REVIEWER B findings, converting each finding in qa-reviewer's producer-format report (the `### Findings` entries of the QA Review Report) into a canonical finding record per `skills/momentum/references/finding-schema.md`.

2. The normalization action specifies a deterministic, total field mapping that populates every canonical base field on every normalized record: `story_slug`, `source`, `verdict`, `severity`, `stakes_class`, `type`, `location`, `summary`, `detail`, `evidence`, `ac_id`, `legitimate`, `suggested_fix` — with no field left to inference at run time.

3. The severity mapping is explicit and total over the three finding-bearing per-AC classifications, and emits only the closed-enum values of finding-schema.md's Severity Enum: `BLOCKED` → `critical`, `MISSING` → `major`, `PARTIAL` → `minor`. No other severity values are producible, and the mapping does not consult `stakes_class` (severity and stakes class are independent axes per finding-schema.md).

4. The mapping sets `source: "qa-reviewer"`, sets `legitimate: true` (qa-reviewer is the verifier of record — it does not emit findings it judges to be false positives), sets `story_slug` from the pipeline's story context (S.slug), carries `ac_id` and `stakes_class` through from the producer finding, carries `verdict` as the producer finding's per-AC classification string, and sets `suggested_fix` to `null` (the qa-reviewer producer format has no explicit fix field; Detail describes expected state, not remediation steps).

5. The `type` field is assigned deterministically from the closed Type Enum: `security` when the finding's `stakes_class` is `security-auth-isolation`, otherwise `spec-compliance` (qa-reviewer findings are by definition AC-verification findings).

6. The normalization handles the empty case: a qa-reviewer report with zero findings (all ACs VERIFIED) normalizes to an empty array, and the merge proceeds with REVIEWER B findings alone — no error, no fabricated records.

7. The REVIEWER A "Returns:" description in conductor/workflow.md (~lines 400–402) is corrected to state that the agent returns its producer-format QA Review Report (per-AC classification with stakes_class) and that the Conductor normalizes it to the canonical schema in the stage-2 normalization action — it no longer claims the agent itself returns canonical-shape findings.

8. The merge step in conductor/workflow.md (~lines 419–426) binds `{{qa_findings}}` to the output of the new normalization action (not to REVIEWER A's raw report), so its stated guarantee — every `{{stage2_findings}}` record carries the canonical base fields — holds by construction for both reviewer streams.

9. The schema note in `skills/momentum/agents/qa-reviewer.md` (~line 173) is updated to name the Conductor's stage-2 normalization action in `conductor/workflow.md` as the owner of the producer→canonical mapping; the dangling claim that the adapter is "owned by the `directed-fix-finding-schema` story" is removed. The agent's Output Format template itself is unchanged.

10. Both artifacts agree after the change: a search across `skills/momentum/` for "normalization adapter" (and equivalent phrasing) resolves only to the implemented Conductor-side normalization — no text in either touched file references an adapter that does not exist, and conductor/workflow.md and qa-reviewer.md describe the same producer/consumer contract. (Story/planning documents under `.momentum/` and `docs/` are out of scope for this check.)

## Tasks / Subtasks

- [ ] Task 1: Add the stage-2 normalization action to `skills/momentum/skills/conductor/workflow.md` (AC: 1, 2, 3, 4, 5, 6)
  - [ ] Insert the action between "When BOTH reviewers have returned:" and the `{{qa_findings}}` binding (anchor on the text "Bind {{qa_findings}} = findings array from REVIEWER A", currently ~line 417 — anchor by text, not line number)
  - [ ] Spec the full deterministic mapping table (producer field → canonical field), including the fixed values (`source`, `legitimate`), the pipeline-supplied value (`story_slug` = S.slug), the verdict→severity table, the stakes_class→type rule, and the suggested_fix-or-null rule
  - [ ] Spec the empty-findings case (zero producer findings → empty normalized array)
  - [ ] Follow the field-mapping presentation style of `skills/momentum/skills/code-reviewer/workflow.md` step 4.5 for consistency
- [ ] Task 2: Correct the REVIEWER A "Returns:" block in `conductor/workflow.md` (AC: 7)
  - [ ] Rewrite ~lines 400–402 so the stated return shape is the producer-format QA Review Report and the normalization responsibility is explicitly the Conductor's stage-2 action
- [ ] Task 3: Update the merge step in `conductor/workflow.md` to consume the normalized result (AC: 8)
  - [ ] Bind `{{qa_findings}}` = the normalized canonical records produced by Task 1's action
  - [ ] Confirm the merge step's canonical-base-fields guarantee text (~lines 424–426) now holds by construction; adjust wording only if it still implies the agent did the normalizing
- [ ] Task 4: Update the qa-reviewer.md schema note to point at the implemented venue (AC: 9, 10)
  - [ ] Edit the blockquote at `skills/momentum/agents/qa-reviewer.md:173`: replace "owned by the `directed-fix-finding-schema` story" with the Conductor's stage-2 normalization action in `skills/momentum/skills/conductor/workflow.md`; keep the "No change to this output template is required here" producer-stability statement
  - [ ] Leave the Output Format template (~lines 139–171) untouched
  - [ ] Cross-artifact consistency check: grep both touched files (and repo-wide for "normalization adapter") and verify every reference resolves to the implemented Conductor-side action (AC 10)
- [ ] Task 5: EDD evals for the changed instructions (AC: 1–8; per Momentum Implementation Guide below)
  - [ ] Write behavioral evals exercising the normalization action: a producer report with PARTIAL/MISSING/BLOCKED findings normalizes to complete canonical records; an all-VERIFIED report normalizes to an empty array; a `security-auth-isolation` finding gets `type: security`
  - [ ] Run the evals via subagent and document outcomes in the Dev Agent Record

## Dev Notes

### Current state of the artifacts being modified (read these before editing)

**`skills/momentum/skills/conductor/workflow.md` (2,136 lines — large; use Grep + offset reads, never a full read).** Stage-2 lives inside step 2.1's per-story pipeline (block "── STAGE-2: CONCURRENT QA + CODE-REVIEW FAN-OUT ──", ~lines 373–427). Today it: computes the per-story diff (per `references/per-story-review-diff-range.md`), spawns REVIEWER A (qa-reviewer agent) and REVIEWER B (momentum:code-reviewer skill) concurrently as individual-agent fan-out, then on both returning binds `{{qa_findings}}`/`{{cr_findings}}`, merges into `{{stage2_findings}}` (dedup + severity-sort critical → major → minor → low), and advances to stage-3 which passes `{{stage2_findings}}` to step 2.S3 (the directed fix loop). What this story changes: the REVIEWER A "Returns:" text, a new normalization action before the `{{qa_findings}}` binding, and the binding itself. What must be preserved: the concurrent fan-out structure, the coverage-routing skip path (~line 376 — "covered-by-composition" binds `{{stage2_findings}} = []` and skips stage-2 entirely; the normalization action must sit inside the dispatched fan-out path, not on the skip path), the dedup/severity-sort rules, the "qa-reviewer+bmad-code-review" dedup annotation, the stage-3 handoff, and the DEEPER-REVIEW OPT-IN routing for REVIEWER B (~lines 509–523). Downstream consumers that rely on canonical fields being present on `{{stage2_findings}}` records: lines ~574, ~586, ~594, ~614, ~619, ~637, ~642 (fix-loop lookups by finding_id recovering stakes_class/summary/evidence/suggested_fix). Line numbers throughout are current as of story creation — they WILL drift; anchor every edit by quoted text, not line number.

**`skills/momentum/agents/qa-reviewer.md` (197 lines).** Producer Output Format at ~139–171: QA Review Report with Test Results, per-AC table (AC# / Description / Status / Evidence / Stakes Class), and Findings entries carrying exactly: AC, Verdict (PARTIAL | MISSING | BLOCKED), stakes_class, Location, Summary, Detail ("what is wrong, why it matters, what was expected"), Evidence. The stakes-class assignment rubric (lines ~110–126) makes the agent the stakes producer — that responsibility stays with the agent. What this story changes: ONLY the schema-note blockquote at line 173. What must be preserved: the entire Output Format template, the stakes rubric, Verdict Rules, the SendMessage return protocol, and the Out of Scope section.

**`skills/momentum/references/finding-schema.md` (219 lines, v1.1).** Read in full before implementing — it is the target shape. Key constraints the mapping must honor: `severity` is a closed ordered enum (`critical`/`major`/`minor`/`low`); `type` is a closed enum (use `spec-compliance` for AC-divergence findings, `security` for findings meeting the security-auth-isolation bar); `severity` and `stakes_class` are explicitly independent axes (§"Severity and Stakes Class Are Independent Axes") — do NOT inflate severity from stakes; `legitimate` drives the fixer's disposition rules (Rule 1/2: legitimate+routine → auto-fixed, legitimate+stakes → escalated); `suggested_fix` is string-or-null; `ac_id` is string-or-null. Fixer-assigned fields (`disposition`, `dismissal_rationale`, `timing_tier`) are NOT set by this normalization — they belong to the fix loop.

### The reuse anchor — do not reinvent

`skills/momentum/skills/code-reviewer/workflow.md` step 4.5 is the existing, working normalization precedent for REVIEWER B (bmad-code-review → canonical). It demonstrates the expected specification style: one bullet per canonical field, explicit fallback values (e.g., `location` → `"unspecified"` when absent), explicit `legitimate` policy per bucket, and a closing guarantee statement ("every canonical finding carries a populated stakes_class"). Mirror that style for the qa-reviewer mapping inside conductor/workflow.md stage-2. Do NOT create a new standalone adapter skill (the code-reviewer skill exists because bmad-code-review is an interactive skill needing a non-interactive wrapper; qa-reviewer is already a Conductor-spawned agent — the Conductor's own workflow text is the right venue).

### The complete field mapping (authoritative for Task 1)

| Canonical field | Source | Rule |
|---|---|---|
| `story_slug` | pipeline | `S.slug` from the per-story pipeline context |
| `source` | fixed | `"qa-reviewer"` |
| `verdict` | producer `Verdict` | carry the per-AC classification string (`PARTIAL` \| `MISSING` \| `BLOCKED`) |
| `severity` | derived | `BLOCKED` → `critical`; `MISSING` → `major`; `PARTIAL` → `minor` (total; closed enum; never consults stakes_class) |
| `stakes_class` | producer `stakes_class` | carry through unchanged (agent is the stakes producer per its rubric) |
| `type` | derived | `security` if `stakes_class == security-auth-isolation`, else `spec-compliance` |
| `location` | producer `Location` | carry through; `"unspecified"` if absent (mirrors code-reviewer step 4.5) |
| `summary` | producer `Summary` | carry through |
| `detail` | producer `Detail` | carry through |
| `evidence` | producer `Evidence` | carry through |
| `ac_id` | producer `AC` | carry through |
| `legitimate` | fixed | `true` — qa-reviewer is the verifier of record and emits only findings it judges genuine |
| `suggested_fix` | fixed | `null` — the qa-reviewer producer format has no explicit fix field (Detail describes expected state, not remediation steps) |

Severity-derivation note (recorded interpretation): the source finding said "derive severity from per-AC classification + stakes." finding-schema.md declares severity and stakes_class independent axes, and the fixer routes escalation on `stakes_class` alone — so stakes participation in severity would double-count the signal and violate the schema's orthogonality statement. The mapping therefore derives severity from the per-AC classification only; stakes is honored on its own axis (`stakes_class` carried through, and it alone drives Rule-2 escalation). If the developer believes a stakes-aware severity bump is required, that is a schema change and belongs in a separate story against finding-schema.md — do not improvise it here.

### Venue decision (binding)

This story implements Option A from the source finding: Conductor-side normalization in stage-2 of conductor/workflow.md. Option B (extend qa-reviewer.md's output contract to emit canonical-shape findings directly) is explicitly rejected for this story — do not implement both, and do not leave the qa-reviewer.md schema note pointing at a nonexistent owner. After this story, the two artifacts must describe the same contract: agent emits producer format; Conductor stage-2 normalizes; merge consumes normalized records.

### Conventions and guardrails

- Follow `skills/momentum/references/agent-skill-development-guide.md` for any edit to workflow.md or agent definition files (per `.claude/rules/dev-skills.md`).
- conductor/workflow.md is instruction text for an LLM orchestrator, not executable code: the "adapter" is a precisely specified workflow action (a mapping table + rules the Conductor applies at run time), exactly like code-reviewer step 4.5. There is no script to write; `script-code`/TDD does not apply.
- Anchor all edits by quoted text. The cited line numbers (400–402, 417–426, 173) are creation-time references and will drift.
- Do not touch `finding-schema.md` (owned by directed-fix-finding-schema, done), `code-reviewer/workflow.md` step 4.5 (REVIEWER B's path is correct), or the conductor's E2E normalization path (Phase 4, ~line 1654 — separate, already specified).
- Keep the stage-2 skip path intact: when coverage routing binds `{{stage2_findings}} = []`, no reviewers run and no normalization fires.
- A frozen verification contract will exist for this story in its sprint (`.momentum/sprints/{sprint-slug}/specs/conduct-qa-reviewer-normalization-adapter.*`). Dev reads only the Part-A header (how_dev_self_checks, verification_method, harness_profile) as a self-check before signaling done; never read the verifier body (Part B) beyond sections how_dev_self_checks explicitly references.

### Previous story intelligence

- `directed-fix-finding-schema` (done per `.momentum/stories/index.json`) delivered finding-schema.md v1.0; v1.1 (2026-06-07) tightened `type` and `severity` to closed enums and named `story_slug` the canonical join key. Its dev notes called the schema "the keystone the whole escalation chain stands on" — this story closes the last unfinished consumer seam of that keystone.
- The conduct-runnable sprint (merged to main at bc4ec4d, 25 stories) assembled the conductor; commit 351b36c ("fix(conduct): post-merge AVFL integration pass — reconcile 9 cross-story drifts") shows cross-story seam drift in conductor/workflow.md is a known failure mode — which is exactly what this story repairs at the REVIEWER A seam. Expect the file to have been edited recently; re-grep anchors before editing.

### Web research

Not applicable — all deliverables are internal Momentum instruction files (markdown). No external libraries, frameworks, or APIs are involved.

### Project Structure Notes

- `skills/momentum/skills/conductor/workflow.md` — Conductor build orchestration (edit: stage-2 block only)
- `skills/momentum/agents/qa-reviewer.md` — REVIEWER A agent definition (edit: schema-note blockquote only)
- `skills/momentum/references/finding-schema.md` — canonical schema (read-only for this story)
- `skills/momentum/skills/code-reviewer/workflow.md` — REVIEWER B adapter, step 4.5 (read-only; style precedent)
- `skills/momentum/skills/conductor/references/per-story-review-diff-range.md` — diff-range rationale (read-only context)
- Evals for conductor changes live under `skills/momentum/skills/conductor/evals/` (create if absent, per EDD guidance)

### References

- [Source: skills/momentum/skills/conductor/workflow.md — STAGE-2 block ~lines 373–427; fix-loop consumers ~574–642]
- [Source: skills/momentum/agents/qa-reviewer.md — Output Format ~139–171; schema note line 173; stakes rubric ~110–126]
- [Source: skills/momentum/references/finding-schema.md — v1.1; Base Fields, Severity Enum, Type Enum, Stakes Class, Disposition Rules]
- [Source: skills/momentum/skills/code-reviewer/workflow.md — step 4.5 normalization precedent]
- [Source: .momentum/stories/directed-fix-finding-schema.md — prior story; schema-only scope, ACs 1–14]
- [Source: 2026-06-09 conductor effectiveness review — confirmed finding (adversarially verified, high confidence)]
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 5 → skill-instruction (EDD)
- Task 4 → agent-definition (EDD — same approach as skill-instruction; agent definitions are LLM prompt files, verified by skill-invoke)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-normalizes-qa-findings-to-canonical-shape.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text
   - For this story, the eval scenarios in Task 5 are the required set: producer report with PARTIAL/MISSING/BLOCKED findings → complete canonical records; all-VERIFIED report → empty array; `security-auth-isolation` finding → `type: security`

**Then implement:**
2. Modify the conductor workflow.md stage-2 block (Tasks 1–3) and the qa-reviewer.md schema note (Task 4)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) the relevant workflow.md stage-2 excerpt as context. Observe whether the subagent's normalization behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- This story modifies `workflow.md` and an agent file, not a SKILL.md — no description-length change applies, but confirm `skills/momentum/skills/conductor/SKILL.md` is untouched (description ≤150 chars, `model:`/`effort:` frontmatter remain intact)
- workflow.md overflow guidance: if the normalization mapping table would bloat stage-2, the established overflow venue is `skills/momentum/skills/conductor/references/` with a clear load instruction (mirror how `per-story-review-diff-range.md` is referenced) — keep stage-2 inline if the addition stays compact
- Skill names retain the `momentum:` namespace prefix (NFR12)

### agent-definition Task (Task 4): EDD with cross-artifact verification

`change-types.md` defines no dedicated agent-definition template; per the verification-standard routing table, agent-definition verifies by `skill-invoke` — the same method as skill-instruction. Apply the EDD approach above, with the verification focus on cross-artifact agreement: after editing the qa-reviewer.md schema note, run the AC-10 consistency grep across `skills/momentum/` and confirm the note names the Conductor's stage-2 normalization as the owner. Follow `skills/momentum/references/agent-skill-development-guide.md` for agent-definition file conventions.

**Additional DoD items for this story's change types (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] `skills/momentum/skills/conductor/SKILL.md` untouched; frontmatter (`model:`, `effort:`) and description length unchanged
- [ ] workflow.md stage-2 edits anchored by quoted text, not line numbers
- [ ] qa-reviewer.md Output Format template byte-identical except the line-173 schema-note blockquote
- [ ] AC-10 consistency grep across `skills/momentum/` documented in Dev Agent Record
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically)

**Frozen verification contract reminder:** a frozen verification contract exists for this sprint at `.momentum/sprints/{sprint-slug}/specs/conduct-qa-reviewer-normalization-adapter.{ext}`. Dev reads the Part-A header (how_dev_self_checks, verification_method, harness_profile) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by how_dev_self_checks.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
