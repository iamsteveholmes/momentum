---
title: Momentum knowledge base buildout
story_key: momentum-knowledge-base-buildout
status: ready-for-dev
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: feature
priority: medium
depends_on: []
touches:
  - skills/momentum/skills/build-guidelines/workflow.md
  - skills/momentum/skills/build-guidelines/references/orchestration-guide.md
  - skills/momentum/references/manifesto-format.md
  - ~/.obsidian-wiki/config
  - ~/projects/momentum-agentic-kb/
change_type:
  - config-structure
  - specification
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Momentum knowledge base buildout

## Story

As a developer,
I want to stand up Momentum's own knowledge base (KB) — a Momentum-scoped Obsidian vault separate from any other project's KB — and extend `wiki-query` so it resolves the correct per-project KB,
so that a Momentum agent's diagnostic-table manifesto resolves its symptom→`wiki-query` lookups against Momentum-domain knowledge instead of nornspun's (or an empty) knowledge base.

## Description

Momentum needs its OWN Obsidian-style cold KB, distinct from nornspun's, because agents are
project-scoped (DEC-038 D2): a Momentum agent resolves its manifesto's symptom→`wiki-query`
lookups against Momentum-domain knowledge (skills, workflows, agent architecture, conduct,
practice model), not nornspun's. This story stands up the "cold KB" (Tier 3) half that the
diagnostic-table manifesto (DEC-038 D1, PRD FR136) queries, and delivers the multi-KB
`wiki-query` extension (PRD FR142) that routes each lookup to the KB its `project_kb` declares.

The work has two shippable legs (see the split boundary in Tasks):

- **Leg A — Vault init + seed.** Create a Momentum-owned vault under the canonical identifier
  `momentum-agentic-kb` (parallel to `nornspun-agentic-kb`) and seed it with Momentum-domain
  concept pages so the manifesto diagnostic tables have real pages to hit.
- **Leg B — FR142 multi-KB `wiki-query`.** Extend the cold-KB interface (DEC-018) from a single
  global vault to a per-project registry, so `wiki-query` resolves the vault named by the
  invoking agent's `project_kb`, and make the `build-agents` (build-guidelines) pipeline route
  `project_kb` operatively rather than merely storing it "for later."

**Pain context:** Without a Momentum KB there is nothing for a Momentum agent's diagnostic-table
manifesto to query — the recovered prototype's KB (`nornspun-agentic-kb`) is nornspun's, not
Momentum's. The cohort pipeline can compose agents, but their `wiki-query` routing resolves
against the wrong vault (nornspun's) or none until this exists. Every Momentum manifesto
symptom→`wiki-query` entry dangles until the Momentum KB is built and the resolver is
project-scoped.

Source: DEC-038 (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB Architecture,
2026-06-16); PRD FR142. Background: `.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md`.

## Acceptance Criteria

These ACs are observable (Outsider Test): each names an artifact or behavior a person outside
the project can check without reading intent.

**Leg A — Momentum KB vault (init + seed):**

1. A Momentum-owned KB vault exists on disk under the Momentum-scoped identifier
   `momentum-agentic-kb`, at a path parallel to `nornspun-agentic-kb` (distinct from any
   nornspun vault), containing a valid Obsidian vault skeleton — a `.obsidian/` config directory
   and a root `index.md`. Listing the vault path shows it exists and is not the nornspun vault.

2. The vault is seeded with Momentum-domain concept pages covering each of these five domains:
   **skills, workflows, agent architecture, conduct, and the practice model.** Each named domain
   has at least one concept page whose title/frontmatter identifies it, and the vault `index.md`
   lists the seeded pages.

3. For every Momentum agent manifesto present in the repo at implementation time, every
   symptom→`wiki-query` entry resolves to a real page in the Momentum KB — zero dangling queries.
   Running each entry's `wiki-query` terms against the Momentum vault returns at least one
   matching page (DEC-038 D1 completeness criterion). If no Momentum manifesto exists yet, the
   five-domain baseline seed of AC2 stands as the coverage floor.

**Leg B — FR142 multi-KB `wiki-query` extension:**

4. The KB-resolution mechanism supports multiple project KBs: a registry maps each `project_kb`
   identifier to its vault path, and both `momentum-agentic-kb` and `nornspun-agentic-kb` are
   registered with distinct paths. Inspecting the registry shows both entries.

5. `wiki-query` resolves the vault named by the invoking agent's `project_kb`: invoked in a
   `momentum-agentic-kb` context it reads the Momentum vault; invoked in a `nornspun-agentic-kb`
   context it reads the nornspun vault. When no `project_kb` is supplied, resolution falls back to
   the current single-vault behavior (no regression for existing single-KB callers).

6. The `build-agents` pipeline routes `project_kb` **operatively** rather than storing it for
   later: a `build-guidelines` run for a Momentum manifesto scopes its `wiki-query` operations to
   `momentum-agentic-kb`, and the "planned, not yet implemented" current-state notes in
   `build-guidelines/workflow.md`, `build-guidelines/references/orchestration-guide.md`, and
   `references/manifesto-format.md` are updated to describe the now-operative routing.

7. End-to-end resolver proof: a manifesto symptom→`wiki-query` lookup declaring
   `project_kb: momentum-agentic-kb`, run through the extended resolver, returns a Momentum KB
   page — not a nornspun page and not an empty result. Use a real Momentum agent manifesto if one
   exists at implementation time; otherwise prove the resolver with a minimal fixture manifest
   created for this purpose (Task 4). The real *composed-agent* end-to-end proof is discharged
   downstream — by the sibling `manifesto-builder-skill-generate-then-curate` (which authors
   Momentum manifestos) and the sprint's `live-e2e-compose-register-resolve-gen-2-agent` — once
   real Momentum manifestos exist. This story owns the KB + resolver, not manifesto authoring
   (see Architecture Compliance).

## Tasks / Subtasks

> **Split boundary (trimmable):** Tasks 1–2 (Leg A — vault init + seed) and Tasks 3–5 (Leg B —
> FR142 multi-KB) are independently shippable. If this story must be split, Leg B becomes its own
> story; Leg A alone still delivers a queryable Momentum KB. Keep as one story unless trimming is
> required.

### Leg A — Momentum KB vault (init + seed)

- [ ] **Task 1 — Initialize the Momentum KB vault** *(config-structure)* — AC1
  - Invoke the `wiki-setup` skill (or equivalent init path) to create a new Obsidian vault under
    the Momentum-scoped identifier `momentum-agentic-kb`, at a path parallel to
    `nornspun-agentic-kb` (e.g. `~/projects/momentum-agentic-kb/`), distinct from any nornspun vault.
  - Confirm the vault skeleton: a `.obsidian/` config directory and a root `index.md` exist.
  - Verify by inspection: the vault path exists and is not `nornspun-agentic-kb`.

- [ ] **Task 2 — Seed Momentum-domain concept pages** *(specification)* — AC2, AC3
  - Author (or ingest via `wiki-ingest`) concept pages for the five domains: skills, workflows,
    agent architecture, conduct, practice model. Use the nornspun KB page shape as the *format
    exemplar only* (concept pages under `concepts/`, frontmatter title/tags/summary, wikilinks) —
    nornspun content is never copied in.
  - Enumerate the distinct `wiki-query` targets referenced across all Momentum agent manifestos
    present at implementation time; ensure a matching page exists for each (no dangling — AC3).
  - Optional cleanup: absorb/relocate any stray Momentum content currently living under
    `nornspun-agentic-kb/projects/momentum/` (a `momentum.md` and small subtree exist there) into
    the Momentum vault, so Momentum knowledge lives in the Momentum KB.
  - Verify by inspection: `index.md` lists the seeded pages; each of the five domains has ≥1 page.

### Leg B — FR142 multi-KB `wiki-query` extension

- [ ] **Task 3 — Establish the multi-KB registry** *(config-structure)* — AC4
  - Extend the KB config (`~/.obsidian-wiki/config`, currently a single `OBSIDIAN_VAULT_PATH`)
    into a registry mapping each `project_kb` identifier to its vault path (a superset that keeps
    the single-value default working).
  - Register both `momentum-agentic-kb` and `nornspun-agentic-kb` with distinct paths.
  - Verify by inspection: the config parses; both entries present with correct paths; existing
    single-vault resolution still works.

- [ ] **Task 4 — Extend `wiki-query` resolution to honor `project_kb`** *(skill-instruction)* — AC5, AC7
  - Update the `wiki-query` "Before You Start" vault-resolution step so it resolves the vault from
    the invoking agent's declared `project_kb` (via the Task-3 registry) instead of always the
    single global `OBSIDIAN_VAULT_PATH`.
  - Preserve fallback: when no `project_kb` is supplied, resolve to the current default vault
    (no regression for existing single-KB callers).
  - EDD: write behavioral evals asserting Momentum context → Momentum vault, nornspun context →
    nornspun vault, no-context → default vault.
  - Fixture for AC7: if no real Momentum manifesto exists at implementation time (none exists as of
    2026-07-13 — `.claude/manifests/` is absent), create a minimal fixture manifest declaring
    `project_kb: momentum-agentic-kb` with one symptom→`wiki-query` entry targeting a seeded Momentum
    page, and use it to prove the end-to-end resolver round-trip (AC7). The fixture is a test artifact
    for this story only — real Momentum manifestos are authored by the sibling
    `manifesto-builder-skill-generate-then-curate`.
  - Note: the `wiki-query` skill is a shared, project-external artifact (see Project Context
    Reference) — choose the least-invasive integration (config-driven resolution over forking the
    shared skill where possible).

- [ ] **Task 5 — Make `build-agents` multi-KB routing operative** *(skill-instruction)* — AC6
  - Update `build-guidelines` so it passes/resolves `project_kb` operatively (scopes downstream
    `wiki-query` operations to the declared KB), not merely "stored for pipeline readiness."
  - Update the "not yet implemented" current-state notes to describe the now-operative routing —
    in `build-guidelines/workflow.md` (the KB-scope resolution action, ~line 60, "planned, not yet
    implemented"), `build-guidelines/references/orchestration-guide.md` (Multi-KB Architecture section,
    "planned but not yet implemented"), and `references/manifesto-format.md` (KB Scoping section,
    "planned, not yet implemented").
  - EDD: eval asserting a Momentum-manifesto `build-guidelines` run scopes `wiki-query` to
    `momentum-agentic-kb`.

## Dev Notes

### Decision Authority

- **DEC-038 D2 (binding):** Knowledge bases and agents are project-scoped. Momentum needs its own
  KB; nornspun keeps its own; multiple KBs are allowed. The `build-agents` pipeline and the
  `wiki-query` interface (DEC-018) are extended to support multiple per-project KBs. `cmp-dev.md`
  and `nornspun-agentic-kb` are nornspun artifacts — format exemplars only, never Momentum agents.
- **DEC-038 D1 (binding):** The manifesto is the agent's stable per-role×domain *diagnostic table*
  (observable symptom → exact `wiki-query` lookup). **Completeness criterion:** if a manifesto
  entry has no page to hit, the manifesto/KB pair is incomplete — this is the ground for AC3's
  no-dangling requirement.
- **PRD FR142 (binding):** Per-Project Multi-KB Architecture and KB Buildout — the multi-KB
  `wiki-query` extension and the Momentum-KB buildout are one sequenced workstream, tracked by this
  story. `wiki-query` must resolve the correct KB for the invoking project/agent.
- **Canonical KB identifier:** `momentum-agentic-kb` — fixed by the KB Scoping table in
  `references/manifesto-format.md` and by the build-guidelines G1 eval. Do not rename.

### Current State of Affected Files (verified this session, 2026-07-13)

- **No Momentum KB vault exists** anywhere (`~/projects/momentum-agentic-kb`, `~/projects/momentum-kb`,
  `.momentum/kb`, `~/.momentum/kb` all absent). The nornspun vault at `~/projects/nornspun-agentic-kb`
  is real and populated (~168 concept pages: `concepts/`, `entities/`, `references/`, `sources/`,
  `synthesis/`, `index.md`, `hot.md`, `.obsidian/`). It even holds a stray `projects/momentum/momentum.md`
  subtree — Momentum content misplaced in the wrong vault.
- **`~/.obsidian-wiki/config`** is single-vault today: `OBSIDIAN_VAULT_PATH=/Users/steve/projects/nornspun-agentic-kb`
  plus `OBSIDIAN_SOURCES_DIR`, `CLAUDE_HISTORY_PATH`, `OBSIDIAN_LINK_FORMAT`, `OBSIDIAN_MAX_PAGES_PER_INGEST`.
  This is the single-global pointer Leg B replaces with a per-`project_kb` registry.
- **`wiki-query` skill** resolves the vault in its "Before You Start" step: read `~/.obsidian-wiki/config`
  → `OBSIDIAN_VAULT_PATH` → read `$VAULT/hot.md` then `$VAULT/index.md`. This single-vault resolution is
  the exact seam the multi-KB extension changes (Task 4). The skill lives outside the Momentum repo
  (see Project Context Reference).
- **`skills/momentum/skills/build-guidelines/workflow.md`** already reads `project_kb` from each
  manifesto and computes `{{kb_scope}}` single|multi, but its note states: *"wiki-query multi-KB
  extension (FR142) is planned, not yet implemented. Store project_kb for pipeline readiness."* Task 5
  makes this operative and rewrites the note.
- **`skills/momentum/skills/build-guidelines/references/orchestration-guide.md`** (Multi-KB Architecture
  section) and **`skills/momentum/references/manifesto-format.md`** (KB Scoping section) both carry
  equivalent "not yet implemented" current-state language — worded as "planned but not yet implemented"
  in orchestration-guide.md and "planned, not yet implemented" in manifesto-format.md — plus the
  Project→`project_kb` table (Momentum → `momentum-agentic-kb`, nornspun → `nornspun-agentic-kb`).
  Task 5 updates their current-state notes to "operative."

### Architecture Compliance

- Three-tier agent model (architecture.md, Decision 56 / DEC-008 / DEC-038): Tier 3 is the **Cold KB**
  (Obsidian vault, accessed on demand via `wiki-query`). This story builds Momentum's Tier 3 and makes
  its access project-scoped. It does not touch Tier 1 (constitution) or Tier 2 (composed agent/manifesto)
  authoring — those are sibling stories in this epic.
- Multi-KB extends DEC-018 (`wiki-query` cold-KB interface) rather than replacing it; single-KB callers
  must keep working (AC5 fallback).
- No per-agent routing lives in the constitution (DEC-038): routing is the manifesto's diagnostic table.
  This story only ensures those manifesto lookups have a real, correctly-scoped KB to resolve against.

### Testing Requirements

- **skill-instruction tasks (4, 5):** EDD — behavioral evals for resolution routing and operative
  build-guidelines scoping (see Momentum Implementation Guide). No unit tests on the prompts.
- **config-structure tasks (1, 3):** direct implementation + inspection — vault skeleton exists;
  registry parses; both KBs present; single-vault fallback preserved.
- **specification task (2):** direct authoring + cross-reference verification — pages exist per domain;
  every manifesto `wiki-query` target has a matching page (AC3); `index.md` lists them.
- **Primary behavioral proof (verification_method_advisory: `skill-invoke`):** run a
  `project_kb: momentum-agentic-kb` manifesto lookup — a real Momentum manifesto if one exists, else
  the Task-4 fixture manifest — through the extended resolver and observe it reads the Momentum vault
  and returns a Momentum page (AC5, AC7); run the same under `project_kb: nornspun-agentic-kb` and
  observe it reads the nornspun vault. The real composed-agent end-to-end proof is discharged
  downstream once Momentum manifestos exist (AC7).

### Project Context Reference

- **Cross-repo scope (surface at implementation):** the Momentum KB vault (`~/projects/momentum-agentic-kb/`),
  the KB config (`~/.obsidian-wiki/config`), and the `wiki-query` skill are all **external to the Momentum
  git repo** — `wiki-query` ships from the Obsidian-wiki plugin/skill suite (a copy is present at
  `nornspun-client/.claude/skills/wiki-query/SKILL.md`). Prefer a config-driven resolution (registry +
  `project_kb` lookup) over forking the shared skill, so the extension does not diverge the plugin. The
  in-repo touch points are the build-guidelines/manifesto-format notes (Task 5).
- **Format exemplar:** `~/projects/nornspun-agentic-kb/` page shape and `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`
  (verbatim `cmp-dev` diagnostic table). Exemplars only — never copied into the Momentum KB.
- **Init/seed skills:** `wiki-setup` (vault initialization), `wiki-ingest` (distill sources into pages),
  `wiki-status` (coverage check). Use these rather than hand-rolling vault mechanics.

### References

- DEC-038: `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`
  (D1 diagnostic-table definition + completeness criterion; D2 per-project multi-KB; Phase 3 = this KB buildout; G2 authored-vs-generated manifesto is a *separate* story).
- PRD FR142 (Per-Project Multi-KB Architecture and KB Buildout) and FR136 (Gen-2 manifesto diagnostic table): `_bmad-output/planning-artifacts/prd.md`.
- DEC-018 (Obsidian Wiki Skills — `wiki-query` as cold-KB interface), extended here.
- `skills/momentum/references/manifesto-format.md` — KB Scoping section (`project_kb` normative field; Momentum → `momentum-agentic-kb`).
- `skills/momentum/skills/build-guidelines/references/orchestration-guide.md` — Multi-KB Architecture section.
- Background handoff: `.momentum/handoffs/manifesto-cmp-dev-recovery-2026-06-16.md`.
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

### Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → config-structure (direct)
- Task 2 → specification (direct authoring + cross-reference)
- Task 3 → config-structure (direct)
- Tasks 4, 5 → skill-instruction (EDD)

A frozen verification contract for this sprint lives at
`sprints/{sprint-slug}/specs/momentum-knowledge-base-buildout.{ext}`. Dev reads the Part-A header
(`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling
done. Dev never reads the Part-B verifier body (scenarios, assertion scripts, Gherkin) beyond
sections `how_dev_self_checks` explicitly references.

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill change:**
1. Write 2–3 behavioral evals in the affected skill's `evals/` directory (create it if absent).
   For this story the skills modified are `wiki-query` (resolution seam — Task 4) and
   `skills/momentum/skills/build-guidelines/` (operative `project_kb` routing — Task 5):
   - One `.md` file per eval, named descriptively (e.g. `eval-wiki-query-resolves-momentum-kb-from-project-kb.md`,
     `eval-build-guidelines-scopes-wiki-query-to-declared-kb.md`).
   - Format each eval as: "Given [input and context], the skill should [observable behavior]."
   - Test behaviors/decisions, not exact output text (e.g. *which vault was read*, not the answer prose).

**Then implement:**
2. Modify the resolution step (Task 4) and the build-guidelines routing (Task 5).

**Then verify:**
3. Run evals: for each eval, spawn a subagent with (1) the eval's scenario as its task and (2) the
   modified skill loaded as context (or invoke the installed skill). Observe whether behavior matches.
4. All evals match → task complete.
5. Any eval fails → diagnose the gap in the instructions, revise, re-run (max 3 cycles; surface if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- Any SKILL.md `description` field touched must be ≤150 characters (NFR1) — count precisely.
- `model:` and `effort:` frontmatter must be present (model routing per FR23).
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow goes in `references/` (NFR3).
- Skill names use the `momentum:` namespace prefix where applicable (NFR12).

**Additional DoD for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in the affected skill's `evals/`.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented).
- [ ] Any touched SKILL.md description ≤150 characters confirmed.
- [ ] `model:`/`effort:` frontmatter present and correct on any touched SKILL.md.
- [ ] Touched SKILL.md/workflow.md body ≤500 lines / 5000 tokens (overflow in `references/`).
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically).

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Create the vault skeleton (Task 1) / write the registry (Task 3)** per the ACs.
2. **Verify by inspection:**
   - The KB config must parse (e.g. it remains valid key=value / valid JSON if reformatted) — validate with a tool, not by eye.
   - Required fields present: every registry entry maps a `project_kb` id → an existing vault path; both KBs present.
   - Paths: every referenced vault path must exist after creation (the Momentum vault must exist before it is registered).
   - No regression: the single-vault default resolution must still work when no `project_kb` is supplied.
3. **Document** what was created in the Dev Agent Record.

**DoD for config-structure tasks:**
- [ ] KB config parses without error (validated with a tool).
- [ ] Registry maps both `momentum-agentic-kb` and `nornspun-agentic-kb` to distinct, existing paths.
- [ ] Vault skeleton (`.obsidian/`, `index.md`) exists at the Momentum-scoped path.
- [ ] Single-vault fallback preserved.
- [ ] Changes documented in Dev Agent Record.

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Concept-page seeding (Task 2) is validated by inspection and by AVFL against upstream intent — not by tests:

1. **Author/ingest the pages** per the five-domain coverage and the manifesto-demand set (AC2, AC3).
2. **Verify cross-references:** every seeded page referenced by `index.md` resolves; every Momentum
   manifesto `wiki-query` target has a matching page (no dangling).
3. **Verify format compliance:** pages follow the Obsidian concept-page shape (frontmatter
   title/tags/summary, wikilinks) exemplified by the nornspun vault — exemplar only, no copied content.
4. **Document** what was authored in the Dev Agent Record.

**No tests or evals required** for the seeding task. AVFL checkpoint (run by momentum:dev) validates against the ACs.

**Additional DoD for the specification task:**
- [ ] Each of the five domains (skills, workflows, agent architecture, conduct, practice model) has ≥1 page.
- [ ] Every Momentum manifesto `wiki-query` target resolves to a real page (no dangling) — or the five-domain baseline stands if no manifesto exists yet.
- [ ] `index.md` lists the seeded pages; wikilinks resolve.
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically).

## Dev Agent Record

_This section is populated only during and after development._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
