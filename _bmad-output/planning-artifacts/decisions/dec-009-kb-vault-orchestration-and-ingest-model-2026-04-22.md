---
id: DEC-009
title: Practice Knowledge Base Vault — Orchestration Model, Isolation, Merge Strategy, Research Path
date: '2026-04-22'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-04-22'
prior_decisions_reviewed:
  - DEC-008 (Composable Specialist Agents Architecture — immediate predecessor; this SDR is a follow-on implementation-detail pass for the KB vault established there)
  - DEC-001 (Three-Tier Agent Guidelines — originates the vault concept)
stories_affected:
  - kb-init
  - kb-ingest
  - kb-raw-ingest-spike
  - wiki-page-schema-and-frontmatter-formalization
  - vault-claudemd-navigation-contract-spec
  - vault-indexmd-registry-format-and-update-protocol
  - staleness-detection-mechanism-for-raw-sources
---

# DEC-009: Practice Knowledge Base Vault — Orchestration Model, Isolation, Merge Strategy, Research Path

## Summary

Follow-on to DEC-008 covering four implementation-level decisions about the Tier 3 cold KB vault. During `momentum:feature-breakdown` for `momentum-practice-knowledge-base`, four strategic questions emerged that DEC-008 did not resolve: (D1) whether kb-ingest is invoked from the vault or from the project, (D2) whether vaults are per-project or shared across projects, (D3) how re-ingest interacts with manual edits on derived wiki pages, (D4) where Momentum's own research reports land in the vault. Net direction: **project-centric orchestration (contingent on workspace-invokable skills), one vault per project, git-versioned overwrites instead of protected regions, and research reports treated as ordinary raw sources that the vault re-synthesizes on its own terms.** The unifying principle across all four: favor simplicity and explicit responsibility over clever automation.

---

## Decisions

### D1: Vault-centric vs project-centric orchestration model — ADAPTED

**Developer framing:** Today the developer opens the vault directly in Claude Code and runs synthesis interactively — a vault-centric model by default. The question is whether to automate this into a vault-centric skill (runs inside the vault, project doesn't manage it) or a project-centric skill (runs from the project, which reaches into the vault).

**Decision:** Adapt — target project-centric orchestration, contingent on technical feasibility. The vault must be treated as a workspace (addressable from the project context), and the skill that lives within the vault must be invokable from outside the vault. If those capabilities exist or can be built, project-centric is the model. If they cannot, fall back to vault-centric (the current manual workflow) until they can.

**Rationale:**
Adapt project-centric if possible. So the vault would have to be a workspace and the skill within the vault would have to be invokable.

---

### D2: Multi-project vault naming and isolation — ADOPTED (Option A)

**Developer framing:** Every project gets a dedicated vault, OR projects on the same stack share a vault, OR a hybrid where each project has its own vault but can import shared stack-level vaults.

**Decision:** Adopt Option A — one vault per project. Each project scaffolds a dedicated `{project}_vault/` repo via kb-init. No shared vaults in the initial model. Overlap across projects on the same stack is accepted as a cost.

**Rationale:**
Option A — There will be overlap but even two kotlin-compose projects might be using different patterns, different libraries, etc.

---

### D3: Re-ingest merge strategy for manual edits — ADOPTED (Option A)

**Developer framing:** When kb-ingest re-runs a source that was previously ingested, and the resulting wiki page has since been manually edited, the system must choose between overwrite, append, protected sections, sidecar notes, or conflict-resolution prompts.

**Decision:** Adopt Option A — overwrite. Re-ingest overwrites the derived wiki page unconditionally. No protected regions, no sidecar files, no conflict prompts. The vault is a git repo, so manual edits are recoverable from git history if needed.

**Rationale:**
Overwrite. It can be in git and versioned.

---

### D4: Research-output ingest path — ADOPTED (Option A)

**Developer framing:** Momentum's own research reports (`_bmad-output/research/**/*.md`) are already pre-synthesized. The question is whether they bypass synthesis (land directly in `wiki/`), go through synthesis (land in `raw/` and get re-synthesized like any other source), get a light-touch synthesis pass, or drop into both `raw/` and `wiki/`.

**Decision:** Adopt Option A — research reports are ingested into `raw/` and re-synthesized by the vault's normal kb-ingest pipeline, same as any other source. No bypass path. The vault produces wiki pages on its own terms regardless of whether the source was already synthesized elsewhere.

**Rationale:**
Option A. The vault has a different synthesis concept.

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 (D1) | During kb-ingest spec/design | Is vault-as-workspace + cross-workspace skill invocation feasible in Claude Code? | Project-centric skill can be implemented without manual vault-opening; if feasibility fails, fall back to vault-centric and record that reversal |
| Gate 2 (D3) | After kb-ingest ships and first re-ingest cycle | Is the overwrite + git-history recovery model sufficient in practice? | No reported data loss; manual edits recoverable from git; developer does not report friction reviving wiki content after ingest |
