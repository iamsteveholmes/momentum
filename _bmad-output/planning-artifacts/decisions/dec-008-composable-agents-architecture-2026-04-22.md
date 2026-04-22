---
id: DEC-008
title: Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy
date: '2026-04-22'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-04-22'
prior_decisions_reviewed:
  - DEC-001 (Three-Tier Agent Guidelines — confirmed and extended with no-fallback posture)
architecture_decisions_affected:
  - DEC-001 — confirmed; D4 adds no-fallback posture (sprint-dev halts when composed file missing rather than falling back)
  - architecture.md Decision 26 (Two-Layer Agent Model) — superseded by collapsed-base-body model; canonical-lookup table to remove pre-shipped specialists (dev-skills.md, dev-build.md, dev-frontend.md). Story `architecture-decision-26-update-for-base-body-collapse` covers the doc update.
stories_affected:
  - base-body-collapse-rollback
  - rename-base-body-files-to-canonical-naming
  - architecture-decision-26-update-for-base-body-collapse
  - project-manifest-format-specification
  - constitutionmd-generation-acceptance-criteria
  - sprint-dev-composed-file-spawn-wiring
  - sprint-planning-composed-file-preference-update
  - specialist-classify-update-for-gen-2-paths
  - build-guidelines-invocation-surface-in-sprint-planning
  - architect-base-body
  - sm-base-body
  - pm-base-body
  - build-guidelines-skill
---

# DEC-008: Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy

## Summary

During `momentum:feature-grooming` and `momentum:feature-breakdown` for the new `momentum-composable-specialist-agents` feature, five strategic decisions emerged from conversation. This SDR captures: (D1) confirmation of the three-tier agent-guidelines layout originally decided in DEC-001; (D2) KB-init as a soft stop the developer must handle before `build-guidelines` runs, rejecting silent kb-less fallback; (D3) deferral of the KB-to-guidelines integration contract until KB is real; (D4) rejection of a fallback path when composed specialist files are missing — sprint-dev halts and the developer is expected to run `build-guidelines` to produce them; (D5) confirmation that the SM base body carries lightweight technical literacy with the explicit clarification that this includes enough proficiency to *design* stories via `create-story`, not merely run the workflow. Net direction: composable-agents architecture is settled and concrete enough to drive 12 backlog stories; KB and missing-file behaviors favor explicit developer responsibility over silent degradation.

---

## Decisions

### D1: Three-tier project layout — ADOPTED

**Developer framing:** Formalize the canonical project structure for composable specialist agents — Tier 1 hot constitution, Tier 2 composed specialist files, Tier 3 in-project references plus a separate cold KB vault — with specific file paths and the KB vault layout.

**Decision:** Adopt three-tier layout. In-project: `.claude/guidelines/constitution.md` (Tier 1 — hot, always loaded, ~660-line target, critical rules and pointers); `.claude/guidelines/agents/{role}-{domain}.md` (Tier 2 — composed specialists loaded at spawn); `.claude/guidelines/refs/*.md` (Tier 3 in-project JIT references). Tier 3 cold layer is a separate `{project}_vault/` repo with `raw/`, `wiki/`, `index.md`, `log.md`, `CLAUDE.md` — populated by `kb-init`/`kb-ingest`, distilled by `build-guidelines`.

**Rationale:**
Based on our research this is the best way to create a KB for agents.

---

### D2: KB-init dependency sequencing — ADAPTED

**Developer framing:** Determine whether `momentum-composable-specialist-agents` gates on KB shipping, or whether `build-guidelines` operates kb-less when no vault exists.

**Decision:** Adapt the kb-less recommendation to a **soft stop**. `build-guidelines` does not silently fall back to kb-less mode when no vault exists. Under most normal circumstances, KB setup is something the developer must handle before `build-guidelines` runs. The skill surfaces the gap and waits for the developer rather than degrading silently into stack-detection-only mode.

**Rationale:**
No, it should be a soft stop, under most normal circumstances this is something the dev must handle before it comes into play.

---

### D3: KB-to-guidelines integration contract — ADOPTED (deferred)

**Developer framing:** Defer detailed design of the KB → `build-guidelines` distill handoff (interface format, trigger point, ownership) until KB exists in concrete form.

**Decision:** Adopt the deferral. The contract is not designed in this SDR. Re-open when `kb-init` and `kb-ingest` are real artifacts and we can see the actual shape of vault content the distill phase consumes.

**Rationale:**
Let's see what it looks like before we design the contract.

---

### D4: Fallback behavior when composed file missing — REJECTED

**Developer framing:** When sprint-dev cannot find `.claude/guidelines/agents/{role}-{domain}.md` for a story's classified specialist, decide whether to fall back to a generic base body, emit a warning, block the sprint, or proceed silently.

**Decision:** Reject the fallback recommendation. No fallback. The composed file should be created. Sprint-dev halts when the expected composed specialist is missing; the developer is expected to run `/momentum:build-guidelines` to produce it. This makes the missing-prerequisite condition visible and actionable rather than silently degrading specialist quality. Consistent with D2's soft-stop posture.

**Rationale:**
No fallback. It should be created.

---

### D5: SM technical proficiency scope — ADOPTED (clarified)

**Developer framing:** Determine what technical knowledge belongs in the SM base body versus what must escalate to the developer or a specialist dev.

**Decision:** Adopt the lightweight-literacy scope: story-quality judgment (testability, completeness), backlog reasoning (priorities, duplicates, dependencies), change-type literacy (novel+load-bearing vs well-understood+reversible), touches-path shape-knowledge. Hard limit: SM does not design implementations, debug code, or hold stack-specific conventions; technical design questions escalate to developer or specialist dev. **Clarification:** SM has enough literacy to *design* the stories — `create-story` is a competent design activity, not just a workflow execution. The SM judges story quality and shape, not just process compliance.

**Rationale:**
Adopt, but he has enough literacy to design the stories (create-story).

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 (D2) | When kb-init ships | Is the soft-stop friction acceptable in practice? | Developers running `build-guidelines` on a fresh project understand the KB prerequisite and can act on it without confusion |
| Gate 2 (D3) | When kb-init and kb-ingest are both real | Re-evaluate the KB-to-guidelines integration contract | Concrete vault content exists; distill phase can be designed against actual data shape |
| Gate 3 (D4) | After `sprint-dev-composed-file-spawn-wiring` ships | Does halting on missing composed file actually drive correct behavior? | Developers respond to the halt by running `build-guidelines`, not by editing sprint-dev to add their own fallback |
