---
title: "Manifesto format: normative file-pattern / ownership field for deterministic agent resolution"
story_key: manifesto-format-normative-file-pattern-ownership-field
status: ready-for-dev
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: maintenance
priority: high
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/references/manifesto-format.md
  - skills/momentum/skills/build-guidelines/workflow.md
  - skills/momentum/skills/build-guidelines/SKILL.md
  - skills/momentum/skills/build-guidelines/references/orchestration-guide.md
  - skills/momentum/skills/build-guidelines/evals/
---

# Manifesto format: normative file-pattern / ownership field for deterministic agent resolution

## Story

As a developer,
I want the manifesto format to declare a normative, machine-readable file-pattern / ownership field that build-guidelines reads deterministically,
so that each composed agent's `agents.json` `patterns` resolve reliably and the agent is always reachable instead of silently falling back to the generic `dev` agent.

## Description

build-guidelines (shipped in sprint-2026-06-18) derives each composed agent's `agents.json` `patterns` (the file globs the `momentum-tools agent resolve --touches` resolver matches on) by best-effort LLM inference from the manifesto's `## Project Stack` prose — because the manifesto format (`skills/momentum/references/manifesto-format.md`) declares no normative machine-readable file-pattern / ownership field. Concretely, build-guidelines workflow Phase 3 (the agent-builder invocation step, `<step n="3">`, in its `permissions_scope` action) instructs the orchestrator to "derive [permissions_scope] from manifesto's `## Project Stack` 'Shared UI' / 'Shared logic' paths, or from any 'File ownership' section in the manifesto … default to broad-match patterns." That inferred `permissions_scope` is handed to `agent-builder`, which writes it verbatim into the `agents.json` project entry as `"patterns"`. The resolver matches a touched file path against those `patterns`; when they are vague, wrong, or empty, no entry matches and the resolver returns the generic `dev` fallback — the composed agent is functionally dead.

This is the single G1-determinism residual that stands between "agent cohort works in practice" and "works deterministically." build-guidelines already enforces a G1 gate (non-empty `patterns[]` + `--touches` resolves the composed slug, not the generic fallback), but G1 currently depends on an LLM guess being good enough.

**Fix:** add a normative, machine-readable file-pattern / ownership field to the manifesto format, and have build-guidelines read that field verbatim as the source of `permissions_scope` — no LLM inference for the resolver-critical globs. A manifesto missing the field must produce a detectable signal, not a silent inference.

**Pain context:** Surfaced at the sprint-2026-06-18 conduct end-gate as a "still hollow" gap. It gates the reliability of the sprint's flagship capability (agent composition) — the cohort is not production-trustworthy until resolution is deterministic. Priority: HIGH. This is a real backlog item, NOT a quick-fix.

## Acceptance Criteria

1. **Normative ownership field in the manifesto format.** `skills/momentum/references/manifesto-format.md` declares a new **Required** section (e.g. `## File Ownership`) that specifies a machine-readable file-pattern / ownership field: its field name, its value shape (a YAML/list of glob strings such as `skills/**/*.md`), its placement in the file, the normative rules governing it, and at least one worked example. The section is added to the format's required-section set, not buried as optional prose.

2. **Template + consumption-contract reflect the field.** The "Manifesto File Template" block and the "Build-Guidelines Consumption Contract (AC8)" table in `manifesto-format.md` are updated to include the new ownership field. The consumption-contract table states explicitly that build-guidelines reads this field to populate the composed agent's `agents.json` `patterns[]` (the `permissions_scope` it passes to agent-builder) — replacing the current reliance on `## Project Stack` prose for resolver-critical globs.

3. **Field is mandatory; absence is incomplete.** The format states that the ownership field is mandatory — a manifesto without it is **incomplete** (consistent with the existing Completeness Criterion's treatment of incompleteness). The rule is written so a consumer can mechanically detect the missing field rather than guess.

4. **build-guidelines reads the field deterministically.** build-guidelines (`workflow.md` Phase 3 — the `<step n="3">` agent-builder invocation, `permissions_scope` action — plus any matching SKILL.md / orchestration-guide.md description) reads the manifesto ownership field **verbatim** as the source of `permissions_scope` passed to agent-builder. The best-effort LLM inference from `## Project Stack` "Shared UI" / "Shared logic" prose is removed for resolver-critical globs. Observable: for a manifesto whose ownership field is `["skills/**/*.md", "skills/**/*.sh"]`, the resulting `momentum/agents.json` project entry's `patterns` equals exactly `["skills/**/*.md", "skills/**/*.sh"]` — no added, dropped, or reworded globs.

5. **Missing field surfaces a signal, never a silent guess.** When build-guidelines processes a manifesto that lacks the ownership field, it surfaces a detectable signal (flags the manifesto invalid in the Discover phase matrix, or HALTs/warns) instead of silently inferring patterns from prose. Observable: running build-guidelines against a manifesto with no ownership field produces an explicit "missing ownership field" signal rather than a populated-but-guessed `patterns` set.

6. **End-to-end deterministic resolution (G1 residual closed).** A composed agent built from a manifesto with a populated ownership field resolves via `momentum-tools agent resolve --touches <path-matching-a-declared-glob>` to the **composed** slug (`{role}-{domain}`), not the generic `dev` fallback. The resolution is driven by the declared field, not by an inference.

## Tasks / Subtasks

- [ ] **Task 1 — Add the normative ownership section to the manifesto format.** (AC1, AC3)
  In `skills/momentum/references/manifesto-format.md`, add a Required `## File Ownership` section after the `## Project Stack` section. Define: the field name and shape (a list of glob strings), placement, normative authoring rules (globs must be concrete enough to match the agent's touched paths; no empty list), the mandatory-field rule (absence ⇒ incomplete, tied to the Completeness Criterion), and a worked example mapping a stack to its owned globs (e.g. `dev × skills → ["skills/**/*.md", "skills/**/*.sh", "skills/**/*.yaml"]`).

- [ ] **Task 2 — Update template + consumption contract.** (AC2)
  In the same file, add the ownership field to the "Manifesto File Template" code block and add a row to the "Build-Guidelines Consumption Contract (AC8)" table: *What build-guidelines reads = the File Ownership field → What it does with it = populates the composed agent's `agents.json` `patterns[]` (`permissions_scope`) deterministically.* Adjust the existing `## Project Stack` table row so it no longer implies it is the source of resolver patterns.

- [ ] **Task 3 — Make build-guidelines read the field verbatim.** (AC4)
  Rewrite build-guidelines `workflow.md` Phase 3 (the `<step n="3">` agent-builder invocation) `permissions_scope` derivation: read the manifesto's File Ownership field and pass it through unchanged as `permissions_scope`. Remove the "derive from `## Project Stack` 'Shared UI'/'Shared logic' paths … default to broad-match patterns" LLM-inference instruction for resolver-critical globs. Update `SKILL.md` AND `references/orchestration-guide.md` — the latter's `## Known Limitation: patterns Derivation Is Best-Effort` section (lines ~155–161, including its line-157 statement "Build-guidelines derives the `permissions_scope` globs … via LLM inference") documents exactly the gap this story closes; rewrite that section to describe the deterministic field-read and remove its now-obsolete "Follow-up (cross-artifact — out of scope for this story)" note that points at this very story. Preserve the orchestrator-purity contract — build-guidelines still does not self-write `agents.json`; agent-builder continues to write `patterns = permissions_scope`.

- [ ] **Task 4 — Gap handling for a missing field.** (AC5)
  In build-guidelines Phase 1 (Discover) manifest-validation, treat a manifesto with no File Ownership field (or an empty field) as invalid/incomplete: surface it in the manifest matrix with a reason, and do not infer patterns from prose. Confirm the existing G1 gate (Phase 5/6) still fails loudly rather than passing on a guessed pattern.

- [ ] **Task 5 — EDD evals + skill-invoke verification.** (AC4, AC6)
  Write/extend behavioral evals under `skills/momentum/skills/build-guidelines/evals/` asserting: (a) a populated ownership field flows verbatim to `agents.json` `patterns`; (b) `momentum-tools agent resolve --touches` on a matching path returns the composed slug, not `dev`; (c) a manifesto missing the field is flagged, not inferred. Run the skill-invoke verification on a representative manifesto and record the result.

## Dev Notes

### Decision Authority

- **DEC-038 D1/D2** and **architecture.md Decision 56** govern the manifesto: it is the agent's stable, sprint-invariant **diagnostic table**, per-project KB-scoped. This story ADDS a machine-readable ownership field; it must not reframe the manifesto as a per-sprint/per-story overlay, and must not touch the diagnostic-table semantics.
- **build-guidelines G1 gate** (workflow.md `<critical>`): a run is valid only if at least one composed agent is registered with non-empty `patterns[]` AND `momentum-tools agent resolve --touches` returns the composed slug (not the generic fallback). This story makes G1 deterministic by sourcing `patterns` from a declared field instead of an inference — it does not relax G1.
- The ownership field is the new authoritative source for `permissions_scope`/`patterns`. The existing AC8 consumption contract in `manifesto-format.md` is the contract to extend.

### Current State of Affected Files

- `skills/momentum/references/manifesto-format.md` — required sections today: identity block (`role`, `domain`, `project_kb`), `## Project Stack`, `## Diagnostic Table`, KB Scoping, Completeness Criterion, File Template, and the "Build-Guidelines Consumption Contract (AC8)" table. **No file-pattern / ownership field exists.** The AC8 table lists `## Project Stack` as what build-guidelines bakes in "for disambiguation" — today that prose is also the de facto (LLM-inferred) source of resolver patterns.
- `skills/momentum/skills/build-guidelines/workflow.md` — Phase 3 (the `<step n="3">` agent-builder invocation) derives `permissions_scope` by best-effort inference from `## Project Stack` paths and hands it to `agent-builder`. Phases 5/6 verify registration and run the `--touches` resolver as the G1 gate.
- `skills/momentum/skills/build-guidelines/SKILL.md` — describes build-guidelines as an orchestrator over agent-builder (Tier 2) that validates resolvability via `--touches`.
- `skills/momentum/skills/build-guidelines/references/orchestration-guide.md` — its `## Known Limitation: patterns Derivation Is Best-Effort` section (lines ~155–161) already documents this exact gap, restates the LLM-inference at line 157, and names this story as the fix owner ("a normative `file_patterns` … field should be added to `manifesto-format.md`"). That section becomes obsolete once this story lands and must be rewritten to the deterministic field-read.
- `agent-builder` (`skills/momentum/skills/agent-builder/workflow.md`, **not modified by this story**) — receives `permissions_scope` and writes the `agents.json` project entry with `"patterns": {{permissions_scope}}` and `"write_permissions": {{permissions_scope}}`. Because it already passes `permissions_scope` through verbatim, no agent-builder change is needed: fixing the upstream source (build-guidelines → the manifesto field) is sufficient.
- `momentum/agents.json` — `project[]` is currently empty; `defaults` lists the generic base agents (including `dev`). The resolver matches a touched path against each project entry's `patterns`; an empty/non-matching `patterns` yields the generic-`dev` fallback this story eliminates.

### Architecture Compliance

- **Orchestrator purity (preserved):** build-guidelines must remain an orchestrator — it reads a field and passes it through; it must NOT self-write `agents.json` and must NOT reintroduce KB-synthesis or pattern-inference logic. agent-builder remains the sole writer of the `patterns` entry.
- **Sprint invariance (preserved):** the ownership field is standing, per-role×domain data — no sprint/story identifier may flow into it or into any composed output (DEC-038 D1).
- **Determinism over inference:** resolver-critical globs are read, not inferred. This is the whole point of the story; any residual "default to broad-match patterns" inference path defeats it and must be removed from the resolver-critical path.

### Testing Requirements

- **Verification method: `skill-invoke`** (per `skills/momentum/references/rules/verification-standard.md` §1 — `skill-instruction` → `skill-invoke`). Selection was unambiguous: every task is `skill-instruction` (a `references/` doc inside `skills/` and the build-guidelines skill files), yielding a single routing method with no escalation.
- **EDD, not TDD**, for the skill/reference changes (these are LLM-prompt artifacts). Behavioral evals live in `skills/momentum/skills/build-guidelines/evals/`.
- **Functional observability:** the decisive checks are (a) `agents.json` `patterns` equals the declared field verbatim, and (b) `momentum-tools agent resolve --touches <matching path>` returns the composed `{role}-{domain}` slug rather than `dev`. These are ordinary-user-observable (no insider knowledge) and satisfy the anti-insider-knowledge guard (verification-standard §4).
- A harness-profile reference for the `skill-invoke` driver should be declared per verification-standard §3 at sprint-planning contract-freeze time.

### Project Context Reference

This story closes the deterministic-resolution residual for the agent composition pipeline. The reachability contract it hardens is build-guidelines' G1 gate; the artifact it amends is the manifesto format's AC8 consumption contract.

### References

- `skills/momentum/references/manifesto-format.md` — the format spec to extend (identity block, `## Project Stack`, AC8 Build-Guidelines Consumption Contract, File Template).
- `skills/momentum/skills/build-guidelines/workflow.md` — Phase 3 / `<step n="3">` (`permissions_scope` derivation), Phases 5–6 (G1 `--touches` gate).
- `skills/momentum/skills/build-guidelines/SKILL.md` — orchestrator description / G1 key observable.
- `skills/momentum/skills/build-guidelines/references/orchestration-guide.md` — `## Known Limitation: patterns Derivation Is Best-Effort` (lines ~155–161): restates the inference (line 157) and names this story as the fix owner; rewrite when the fix lands.
- `skills/momentum/skills/agent-builder/workflow.md` — downstream consumer; writes `agents.json` `patterns = permissions_scope` (lines ~197–198). Not modified, but the contract this story relies on.
- `momentum/agents.json` — resolver target; `project[]` `patterns` matched by `momentum-tools agent resolve --touches`.
- `skills/momentum/references/rules/verification-standard.md` §1 — change-type → verification-method routing (`skill-instruction` → `skill-invoke`).
- DEC-038 D1/D2 — `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` (manifesto = diagnostic table; per-project multi-KB).
- architecture.md Decision 56 — manifesto canonical definition + manifesto-format subsection.
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md, workflow.md, or `references/` format-spec files.** These are non-deterministic LLM prompts / specifications — unit tests do not apply. Use EDD:

**Before writing the changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/build-guidelines/evals/` (the dir already exists for this skill):
   - One `.md` file per eval, named descriptively (e.g., `eval-reads-ownership-field-verbatim-into-patterns.md`, `eval-flags-manifesto-missing-ownership-field.md`, `eval-touches-resolves-composed-slug-not-dev.md`).
   - Format each as: "Given [a manifesto with / without the ownership field], build-guidelines should [observable behavior — patterns equal the field verbatim / the manifest is flagged invalid / `--touches` returns the composed slug]."
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Edit `manifesto-format.md` (Tasks 1–2) and the build-guidelines skill files (Tasks 3–4).

**Then verify:**
3. Run evals: for each eval, spawn a subagent, give it the eval scenario, and load the changed `manifesto-format.md` + build-guidelines `workflow.md`/`SKILL.md` as context (or invoke build-guidelines on a representative manifesto). Observe whether behavior matches.
4. All evals match → tasks complete. Any eval fails → diagnose, revise, re-run (max 3 cycles; surface to developer if still failing).

**NFR compliance (for any SKILL.md edited):**
- `description` ≤ 150 characters (NFR1) — build-guidelines' current description is within budget; keep it so if edited.
- `model:` and `effort:` frontmatter present (they are).
- SKILL.md body ≤ 500 lines / 5000 tokens; push overflow to `references/` (NFR3).
- `momentum:` namespace prefix preserved (NFR12).

**Additional DoD items (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/build-guidelines/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] If SKILL.md edited: description ≤ 150 chars confirmed; `model:`/`effort:` present; body ≤ 500 lines confirmed
- [ ] `momentum/agents.json` `patterns` verified equal to the declared field verbatim (AC4)
- [ ] `references/orchestration-guide.md` inference language updated — `## Known Limitation` section rewritten to the deterministic field-read; obsolete Follow-up note removed (AC4)
- [ ] `momentum-tools agent resolve --touches <matching path>` returns the composed slug, not `dev` (AC6)
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically)

**Frozen verification contract:** a frozen contract exists per sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signalling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts) beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
