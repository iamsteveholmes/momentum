---
id: DEC-022
title: "`momentum/` Pipeline Artifact Directory Structure"
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-009 (Practice Knowledge Base Vault — Orchestration Model, Isolation, Merge Strategy, Research Path)
architecture_decisions_affected:
  - DEC-009 — momentum/ replaces the vault concept for in-project knowledge artifacts
stories_affected:
  - momentum-directory-migration (new — migrates _bmad-output/planning-artifacts/ to momentum/)
---

# DEC-022: `momentum/` Pipeline Artifact Directory Structure

## Summary

A new `momentum/` directory replaces `_bmad-output/planning-artifacts/` as the home for pipeline knowledge artifacts. The BMAD-legacy path is removed in favor of a directory name that reflects the practice producing the artifacts. Subfolders are organized by role ownership, making the routing table computable from directory structure alone.

Operational state remains in `.momentum/` (machine-readable, live-mutating records). The split between `momentum/` and `.momentum/` mirrors the distinction between knowledge artifacts (human-readable, long-lived, produced by role-specific agents) and operational state (machine-readable, ephemeral, managed by the practice harness). Sprint artifacts are split across both directories by type: machine state in `.momentum/sprints/<slug>/`, human outputs in `momentum/sprints/<slug>/`.

## Decisions

### D1: Establish `momentum/` as pipeline knowledge artifact directory — ADOPTED

**Developer framing:** What directory structure should replace `_bmad-output/planning-artifacts/` for pipeline-produced knowledge artifacts?

**Decision:** Establish `momentum/` with these subfolders:
- `momentum/research/` — research documents, synthesis briefings (owner: researcher)
- `momentum/analysis/` — assessment records aes-*.md, analysis docs (owner: analyst)
- `momentum/decisions/` — decision records dec-*.md, index (owner: analyst/architect)
- `momentum/architecture/` — architecture.md, ADRs (owner: architect)
- `momentum/pm/` — prd.md, epics.md, features.json (owner: pm)
- `momentum/ux/` — UX specs, wireframes, design briefs (owner: ux)
- `momentum/sprints/` — sprint summaries, retro outputs, handoffs (human-readable side; owner: sm)

**Rationale:** Removes the BMAD-legacy path (`_bmad-output/`); makes role-based ownership explicit in directory structure; separates knowledge artifacts from operational state. Subfolder naming aligns with role taxonomy from DEC-020 so ownership is visually obvious.

---

### D2: `.momentum/` remains operational state — CONFIRMED

**Developer framing:** Does the `.momentum/` directory structure change with this decision?

**Decision:** No. stories/index.json, sprints/index.json, intake-queue.jsonl, signals/, handoffs/ stay in `.momentum/`. These are machine-readable, live-mutating records — not knowledge artifacts.

**Rationale:** Operational state and knowledge artifacts have different access patterns and retention needs. Operational state is read and written by the practice harness on every workflow step; knowledge artifacts are produced once and revised infrequently by role-specific agents.

---

### D3: Sprint artifact split — ADOPTED

**Developer framing:** Where do sprint artifacts live — `.momentum/` or `momentum/`, or both?

**Decision:** `.momentum/sprints/<slug>/` holds machine-readable state (specs, signals). `momentum/sprints/<slug>/` holds human-readable outputs (retro-transcript-audit.md, sprint-summary.md). Same slug, two homes.

**Rationale:** Clean separation of state vs. output. Machine state needs to be read-writable by the harness with minimal parsing overhead. Human outputs need to be browsable, diffable, and useful as context for the next sprint.

---

### D4: `docs/` remains catch-all — CONFIRMED

**Developer framing:** Does everything in `docs/` need to migrate to `momentum/`?

**Decision:** No. Project-specific non-pipeline docs, analysis that doesn't fit pipeline categories, and reference materials stay in `docs/`. Not everything needs to be categorized; catch-all prevents over-engineering.

**Rationale:** Forcing all documentation into the `momentum/` taxonomy would require classifying documents that are genuinely miscellaneous. A catch-all reduces friction for ad-hoc notes and reference material without polluting the structured artifact directories.
