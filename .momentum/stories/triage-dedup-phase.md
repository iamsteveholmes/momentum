---
title: Triage dedup phase — deterministic prefilter + cluster fan-out + per-theme findings
story_key: triage-dedup-phase
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-sprint-orchestration
story_type: practice
harness_profile: defaults
change_type:
  - script-code
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/triage/workflow.md
  - skills/momentum/skills/triage/SKILL.md
verification_method:
  script-code: "Execution test — run triage prefilter with representative inputs; observe that output (shortlists, score breakdowns, intra-batch matrix) matches spec"
  skill-instruction: "EDD eval — adversarial eval scenarios authored by acceptance tester independent of implementation"
---

# Triage dedup phase — deterministic prefilter + cluster fan-out + per-theme findings

## Story

As a developer,
I want to implement the dedup gate in momentum:triage — a deterministic prefilter feeding cluster fan-out subagents that produce per-theme findings against the existing backlog,
so that every triage invocation (regardless of caller) deduplicates new items against the backlog before classification, ending the duplicate sprawl the backlog has been accreting.

## Description

Implements Phases 0–3 and 5 of the triage redesign plan approved 2026-05-24 (`~/.claude/plans/i-want-us-to-delightful-spindle.md`). (Phase 4 — consolidation analysis fan-out — is Story B scope, not implemented here.) Adds the dedup gate to `momentum:triage` as mandated by **DEC-031 D5**. Standalone value — ships backlog-hygiene gate even before consolidation analysis (Story B) lands.

**Scope:**

- **Phase 0 (new)** — `momentum-tools triage prefilter` subcommand. Pure-Python TF-IDF cosine on title + description, `touches`-path Jaccard overlap, epic/feature_slug boost, status filter (skip `done | dropped | closed-incomplete`). Output per item: top-K=10 candidate stories with score breakdowns, plus an intra-batch similarity matrix. Tuning target: recall ≥95% on real duplicates with K=10.
- **Phase 1 (new)** — inline batch clustering using Phase 0 similarity matrix (3–7 items/cluster; batches ≤5 skip clustering, single dedup agent).
- **Phase 2 (new)** — dedup fan-out: one subagent per cluster, parallel single message (mirrors retro Phase 4 pattern, no TeamCreate, no SendMessage). Each agent receives its cluster's items (full text) + prefiltered shortlist (~15–30 candidates) + full metadata for each candidate story. Returns per-theme JSON findings: `{source_item_id, theme, match_type: duplicate|supersedes|extends|unique, matched_story_slug, evidence, recommended_action, consolidation_hint}`.
- **Phase 3 (new)** — inline consolidation-candidate identification: orchestrator groups `consolidation_hint` fields by `target_slug_or_theme`; hint groups with 2+ members become merge candidates flagged for Story B. Also uses Phase 0's intra-batch similarity matrix to surface items that scored as related but weren't in the same cluster. Pure inline, no subagent.
- **Phase 5 (updated)** — approval UX gains three new sections **before** the existing classification block: dedup actions, split candidates (multi-theme items), merge candidates flagged. Existing five-class classification reused for survivors.
- **Unit tests** for prefilter (recall on synthetic duplicates, status filter correctness, edge cases: empty backlog, single-item batch, all-identical batch).

**Pattern reused:** `retro/workflow.md` Phase 4 — pure fan-out (no TeamCreate, no SendMessage), parallel spawn in a single message, structured findings.

**Cost profile (with prefilter):** ~25–80K input tokens per triage run (vs ~200–320K under a full-snapshot design).

**Pain context:** The intake queue currently holds 33 open un-triaged items sitting next to ~250 non-terminal backlog stories. Sprint-planning bypasses the missing dedup gate by allowing raw handoff promotion via `handoff-N`, explicitly named as a defect in sprint-2026-05-17 retro handoff `iq-20260521002551-3a403aee`. Without this gate, every sprint cycle creates new duplicate stubs that compound the backlog hygiene problem; DEC-031 D5 ratified that dedup must become a mandatory triage gate to stop the accretion.

## Acceptance Criteria

1. `momentum-tools triage prefilter` subcommand exists and is invocable from the triage workflow.
2. Given a batch of incoming items and a populated stories index, the prefilter outputs a ranked top-K=10 shortlist per item with score breakdown fields: `tfidf_score`, `jaccard_score`, `epic_boost`, `combined_score`.
3. The prefilter applies a status filter: stories with status `done`, `dropped`, or `closed-incomplete` are excluded from scoring entirely; only `backlog`, `ready-for-dev`, and `in-progress` stories are candidates.
4. The prefilter outputs an intra-batch similarity matrix (NxN, where N = number of incoming items) suitable for Phase 1 clustering.
5. A unit test fixture with ≥5 synthetic duplicate pairs achieves ≥95% recall at K=10 (i.e., the true duplicate appears in the top-10 candidates for ≥95% of pairs).
6. The triage workflow adds Phase 0 (prefilter invocation) before the existing classification step, passing incoming item titles and descriptions to `momentum-tools triage prefilter`.
7. The triage workflow adds Phase 1 inline clustering: batches of ≤5 items skip clustering and use a single dedup agent; larger batches use the intra-batch similarity matrix to form clusters of 3–7 items (greedy threshold).
8. The triage workflow adds Phase 2 dedup fan-out: spawns one subagent per cluster in parallel via single-message fan-out (no TeamCreate, no SendMessage — mirrors retro/workflow.md Phase 4 pattern).
9. Each dedup subagent receives only the prefiltered shortlist for its cluster members (union of top-K candidates, deduped — not the full backlog).
10. Each dedup subagent returns a JSON array of per-theme findings conforming to the schema: `{ "source_item_id": "iq-...", "theme": "string", "match_type": "duplicate | supersedes | extends | unique", "matched_story_slug": "slug | null", "evidence": "1-2 sentence justification", "recommended_action": "consume | merge | replace | continue", "consolidation_hint": { "target_slug_or_theme": "...", "rationale": "..." } | null }`.
11. A multi-theme incoming item (e.g., one covering two distinct concerns) returns two separate findings, surfacing it as a split candidate in the approval UX.
12. The triage workflow adds Phase 3 inline consolidation-candidate grouping: the orchestrator groups `consolidation_hint` fields by `target_slug_or_theme`; groups with 2+ members are flagged as merge candidates (not analyzed further in this story — Story B scope).
13. The Phase 5 approval UX in `triage/workflow.md` gains three new sections before the existing classification section: (a) **Dedup actions** — per-theme findings grouped by `recommended_action`; (b) **Split candidates** — items with 2+ per-theme findings; (c) **Merge candidates** — consolidation groups from Phase 3, shown as display-only with label "flagged for Story B — no action available yet." No executor path for merge candidates exists in Story A.
14. On approval of dedup actions, the executor consumes queue items marked as duplicates and routes survivors to the existing five-class classification flow.
15. Running triage against the 33 open handoffs produces sensible dedup findings: at minimum, item `iq-20260521002617-b66bc747` ('e2e-validator hardcoded service assumptions') is flagged against `e2e-validator-black-box-hardening`, and item `iq-20260521002732-9cde80f6` ('subagent spawn pre-flight context tier check') is flagged against `agent-spawn-preflight-check`.
16. Unit tests cover: prefilter recall on synthetic duplicates, status filter exclusion, empty-backlog edge case (returns empty shortlists, no error), single-item batch edge case (1x1 similarity matrix produced, no error), all-identical batch edge case (all inter-item cosine similarities ≥0.4 in matrix output).
17. `triage/SKILL.md` description is updated to reflect the new dedup gate behavior (≤150 characters, per NFR1).

## Tasks / Subtasks

1. **Add `triage prefilter` subcommand to `momentum-tools.py`**
   - Implement `collections.Counter`-based TF-IDF (no sklearn, no external dependencies)
   - Implement Jaccard coefficient on tokenized `touches` paths
   - Implement epic/feature_slug exact-match boost (+0.1 to combined score)
   - Implement status filter: exclude terminal states before scoring
   - Output top-K=10 candidates per item sorted by combined score, with score breakdowns
   - Output intra-batch similarity matrix (NxN, TF-IDF cosine on item pairs)

2. **Write unit tests for prefilter in `test-momentum-tools.py`**
   - Synthetic duplicate recall fixture (≥5 pairs, assert recall ≥95% at K=10)
   - Status filter test: terminal-status stories excluded from candidates
   - Empty backlog edge case: no candidates returned, no error raised
   - Single-item batch: produces 1x1 similarity matrix (single self-entry)
   - All-identical batch: all inter-item cosine similarities ≥0.4 (verifies matrix values)

3. **Add Phases 0–3 inline orchestration to `triage/workflow.md`** *(Phase 4 — consolidation analysis fan-out — is Story B scope, not in this task)*
   - Phase 0: call `momentum-tools triage prefilter`, capture shortlists and similarity matrix
   - Phase 1: inline cluster logic using similarity matrix (≤5 skip, else greedy threshold clusters of 3–7)
   - Phase 2: fan-out dedup subagent spawns per cluster (single-message parallel, no TeamCreate)
   - Phase 3: inline `consolidation_hint` grouping pass, flag 2+ member groups as merge candidates

4. **Update Phase 5 approval UX in `triage/workflow.md`**
   - Add dedup actions section before existing classification
   - Add split candidates section (items with multiple per-theme findings)
   - Add merge candidates section (flagged groups, no analysis — Story B deferred)
   - Preserve all existing five-class classification sections for survivors

5. **Update `triage/SKILL.md` description**
   - Update the `description` field to reflect the dedup gate addition
   - Confirm description ≤150 characters
   - Confirm `model:` and `effort:` frontmatter fields remain present

## Dev Notes

### Architecture Compliance

This story implements **DEC-031 D5** — dedup and consolidation as mandatory triage gates. The decision's rationale is explicit: *"Making dedup + consolidation mandatory in triage itself ensures every caller gets the same backlog hygiene, which is what stops the backlog accreting duplicates."*

Triage remains standalone and anytime-callable (DEC-031 D5 requirement preserved). This story does not wire caller integration (retro/assessment/decision → triage) — that is Story C scope.

The dedup fan-out pattern (Phase 2) is architecturally identical to the retro Phase 4 auditor fan-out: pure fan-out, no TeamCreate, no SendMessage, parallel in a single message, structured findings collected by the orchestrator. Read `skills/momentum/skills/retro/workflow.md` Step 4 as the canonical pattern reference before implementing.

### Testing Requirements

**Unit tests (script-code tasks):**
- All prefilter tests go in `skills/momentum/scripts/test-momentum-tools.py`
- Run with: `python3 -m pytest skills/momentum/scripts/test-momentum-tools.py -v -k "prefilter"`
- Recall fixture: build ≥5 item/story pairs where the story is a known paraphrase of the item; assert the true story appears in top-K=10 for ≥95% of pairs
- Status filter test: populate a mock index with terminal-status stories; assert none appear as candidates
- Edge case tests: empty index, single-item batch (1x1 matrix output), all-identical batch (clustering path)

**Behavioral verification (skill-instruction tasks):**
- Run triage against the 33 open handoffs as the acceptance fixture
- Expect: item `iq-20260521002617-b66bc747` ('e2e-validator hardcoded service assumptions') flagged against `e2e-validator-black-box-hardening`; item `iq-20260521002732-9cde80f6` ('subagent spawn pre-flight context tier check') flagged against `agent-spawn-preflight-check`
- Run triage on a 1-item batch: confirm single dedup agent spawned (no clustering), correct routing on completion
- Run triage on a synthetic 30-item batch with 3 intentional intra-batch duplicates: confirm per-theme findings surface the overlap and approval UX asks to merge

### Implementation Guide

**Phase 0 — TF-IDF prefilter implementation:**
- Use `collections.Counter` for term frequency. Compute IDF from the stories index at runtime (no cache needed — fast on 250 stories, auto-fresh).
- Tokenize: lowercase, split on whitespace + punctuation, remove stopwords (minimal list: "the", "a", "an", "is", "in", "of", "to", "for", "and", "with", "by").
- Combine scores: `combined = 0.6 * tfidf_cosine + 0.3 * jaccard_touches + (0.1 if epic_match else 0.0)`. `epic_match` is True when both item and story share the same `epic_slug` or `feature_slug`. Maximum combined score is 1.0.
- Status filter: apply before scoring. Read `status` from stories index; skip if status in `{"done", "dropped", "closed-incomplete"}`.
- Output: per item, a sorted list of `{slug, title, tfidf_score, jaccard_score, epic_boost, combined_score}` (top K=10). Also output the NxN intra-batch matrix as `{item_i, item_j, cosine_similarity}` triples.

**Phase 1 — Clustering:**
- Inline orchestrator logic in `workflow.md` — no subagent needed.
- Greedy threshold: sort all (i, j) intra-batch pairs by cosine similarity descending; greedily assign i and j to the same cluster if both are unassigned and similarity ≥ 0.4. Cluster size target: 3–7; if a cluster would exceed 7, start a new one.
- For batches ≤5 items: skip clustering entirely, assign all items to one cluster, spawn one dedup agent.

**Phase 2 — Fan-out:**
- All dedup agent spawns go in a **single message** (parallel foreground agents). This is the critical correctness requirement — sequential spawning violates the pattern.
- Each agent prompt: (1) cluster items with full text, (2) union of prefiltered shortlists for cluster members (deduped by slug), (3) full metadata for each candidate story, (4) instructions to return per-theme JSON findings.
- Agents return their JSON array as their final response. Orchestrator collects all arrays.

**Phase 3 — Consolidation candidate grouping:**
- Inline in workflow.md after collecting Phase 2 findings.
- Group all findings where `consolidation_hint` is non-null by `consolidation_hint.target_slug_or_theme`.
- Groups with 2+ members → merge candidate. Flag for Story B, do not analyze further.
- Also use Phase 0's intra-batch similarity matrix to surface item pairs that scored as related but were not assigned to the same cluster (e.g., similarity ≥ 0.4 but cluster boundary fell between them). Surface these as additional consolidation hints.

**Phase 5 — Approval UX additions:**
- Three new sections added before the existing classification block in the batch approval output.
- Dedup actions section: grouped by `recommended_action` (consume, merge, replace, continue). Each finding shows: theme, match_type, matched_story_slug, evidence, recommended_action.
- Split candidates section: items where ≥2 per-theme findings exist. Show item summary + themes.
- Merge candidates section: consolidation groups. Show group members + rationale. Label as "flagged for Story B — no analysis yet."

### Project Structure Notes

- `momentum-tools.py` — main script at `skills/momentum/scripts/momentum-tools.py`. Create a new `triage` command group — no such group exists yet. Use the `intake-queue` group as the structural pattern. The first subcommand in the new `triage` group is `prefilter`.
- `test-momentum-tools.py` — companion test file at `skills/momentum/scripts/test-momentum-tools.py`. Add new test class `TestTriagePrefilter` following the existing test class conventions.
- `triage/workflow.md` — rewrite target at `skills/momentum/skills/triage/workflow.md`. Phases 0–3 are inserted before the existing Step 2 (context reads); Phase 5 approval UX additions go into the existing Step 4 output block.
- `triage/SKILL.md` — description-only update at `skills/momentum/skills/triage/SKILL.md`.
- No new files or directories needed. Do not create a `triage/references/` directory in this story (Story B may need it for the consolidation schema).

### References

- Authoritative plan: `~/.claude/plans/i-want-us-to-delightful-spindle.md`
- Governing decision: DEC-031 D5 (dedup + consolidation as mandatory triage gates)
- Fan-out pattern: `skills/momentum/skills/retro/workflow.md` Step 4 (Phase 4 auditor fan-out)
- Current triage workflow: `skills/momentum/skills/triage/workflow.md`
- momentum-tools.py structure: `skills/momentum/scripts/momentum-tools.py` (read first 100 lines for command group patterns)
- Change type templates: `skills/momentum/skills/create-story/references/change-types.md`
- Verification standard: `skills/momentum/references/rules/verification-standard.md`

---

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → script-code (TDD)
- Tasks 3, 4, 5 → skill-instruction (EDD)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/skills/[name]/scripts/` or `skills/momentum/scripts/`. Follow the pattern in existing Momentum scripts for language choice and structure.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- Tests written and passing
- No regressions in existing test suite
- Code quality checks pass if configured

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/triage/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-dedup-phase2-fan-out-parallel.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md and SKILL.md

**Then verify:**
3. Run evals: for each eval file, spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**Regression evals (mandatory):** The 5 existing evals in `skills/momentum/skills/triage/evals/` must also pass after implementing workflow changes — run them as regression evals. New dedup-phase evals are additive; do not remove or modify existing evals.

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/triage/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
