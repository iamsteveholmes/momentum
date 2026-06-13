# Triage Disposition: Four Critical Fixes from the campaign-init Root-Cause Handoff

**Responds to:** `campaign-init-root-cause-four-critical-fixes-2026-06-10.md`
**Triaged:** 2026-06-11, via full-backlog multi-agent dedup sweep (5 agents, adversarially
verified) + capture-infrastructure verification.

## Verdict

All four stories are **genuinely new work — zero duplicates** across the full momentum
backlog. All four stay at priority `critical`, status `backlog`. Per-story enrichment
constraints, premise corrections, reuse anchors, and cross-references are appended to each
stub under "Triage Notes — dedup sweep 2026-06-11" — create-story must read them.

The handoff's dedup warning is confirmed: `conduct-qa-reviewer-normalization-adapter`
(sprint-2026-06-10) is field-shape normalization only; it does NOT cover method execution.
They are distinct stories that edit the same conductor stage-2 block.

## Sequencing decision

1. **Sprint-2026-06-10 ships as approved (five seam-fix stories) — the four fixes do NOT
   join it.** Reasons: (a) all four are intake stubs needing create-story enrichment +
   spec freeze, the sprint's five are ready-for-dev with approved frozen contracts;
   (b) `conduct-qa-execute-verification-method` and `dev-block-on-missing-dependency-contract`
   edit the same conductor stage-2 / dev terminal-contract text two sprint stories rewrite —
   adding them mid-sprint creates same-file collisions; (c) nornspun's next conduct run is
   decoupled — its local runbook story `conduct-round-build-smoke-qa-leg` (nornspun repo,
   critical) covers the smoke-QA leg until conduct ships.
2. **After sprint-2026-06-10 merges, enrich in this order:**
   `conduct-qa-execute-verification-method` first (would have caught the incident alone
   even with all upstream gates missed), then `dev-block-on-missing-dependency-contract`
   (batch with `dev-agent-executor-not-decider` — same files, sibling rule), then the two
   planning gates (`sprint-planning-cross-story-coherence-gate`,
   `create-story-dependency-deliverable-check`) — independent, no hard ordering.
3. Both conduct-adjacent enrichments must anchor edits against **post-sprint** workflow
   text (the sprint rewrites the REVIEWER A block and the dev terminal contract).

## Capture verification (handoff "already done" claims)

- Index entries (priority critical), stubs, practice-ledger `created` events (lines
  28–31, commit 3ad28d2), and beads (all 4 live in the dolt DB, IDs in beads-id-map.json)
  — **all verified**.
- Epic slugs all exist in `_bmad-output/planning-artifacts/epics.json`
  (momentum-sprint-orchestration, momentum-sprint-planning-to-ready,
  momentum-agent-role-contracts).
- **One discrepancy:** the handoff claims "beads with discovered-from edges" — `bd dep
  list` shows zero edges on all four beads, and the Discovery Root epic bead has no
  dependents. Minor; re-wire if discovered-from lineage matters for bead queries.

## Byproduct hygiene flags (for momentum:refine — not actioned here)

- Three index entries claim `story_file: true` with **no file on disk**:
  `verification-method-two-column-smoke-ui-model`,
  `re-emit-frozen-app-ui-contracts-via-producer`,
  `conduct-live-run-against-fixture-sprint`.
- Index-vs-frontmatter status drift: `qa-reviewer-rescope-per-story-contract` (index done
  / file ready-for-dev), `conduct-per-story-build-review-dispatch` and
  `conduct-verification-method-enum-alignment` (index done / file backlog),
  `contract-seam-stories-two-sided-review-scope` (index done / file backlog — flagged
  independently by three sweep agents).
- `cross-story-pattern-detection-surfaces-systemic-issues`: index says `story_file: false`
  but a 4-line file exists on disk.
- `avfl-cross-story-integration-lens` stub may be partially stale —
  `avfl/workflow-merge-review.md` already implements much of it.
- `agent-state-verification-hook` (critical, sprint-04 era): refine should assess whether
  its dev/E2E-prompt scope is partially superseded by the conduct pipeline.
