---
title: Constitution-Builder Write-Mode Parameterization — In-Place SKILL vs Composed Agent File vs Standalone Constitution
story_key: constitution-builder-write-mode-parameterization
status: ready-for-dev
epic_slug: momentum-agent-composition-pipeline
feature_slug: momentum-composable-specialist-agents
story_type: feature
priority: medium
depends_on:
  - wiki-query-interface-block-for-hot-constitution
  - constitutionmd-generation-acceptance-criteria
touches:
  - skills/momentum/skills/constitution-builder/SKILL.md
  - skills/momentum/skills/constitution-builder/workflow.md
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Constitution-Builder Write-Mode Parameterization

## Story

As a developer,
I want `momentum:constitution-builder` to accept a `write_mode` parameter that selects between writing the constitution block into an existing SKILL.md, writing it as a standalone composed agent file at a target path, or writing the universal Tier 1 constitution,
so that the same KB-synthesis logic powers both direct-invoke skills (frontend-dev style) and sprint-dev subagents (composed agent file style) without duplicating implementation.

## Description

Per **DEC-026 D4**, `momentum:constitution-builder` is reworked to generate **domain knowledge only**: project-specific embedded facts (stack, conventions, architectural patterns) and KB-sourced context (wiki lookups via DEC-018 wiki-query interface). It no longer generates Permissions, Standing Rules, or Quick Routing — those responsibilities move to `agent-builder-skill` (see story `agent-builder-skill`).

The constitution's output is scoped to:
- **Embedded facts** — stack identity, key conventions, architectural constraints that every agent in this project needs
- **KB-sourced context** — wiki-query lookups that surface project-specific knowledge at agent spawn time
- **Wiki-query interface block** (DEC-018) — shared infrastructure available to all agents; stays in constitution as a cross-cutting concern

**What moves out of constitution-builder:**
- `## Quick Routing` — moves to `agent-builder-skill` (agent-specific routing per role × domain)
- Agent-specific `## Permissions` — moves to `agent-builder-skill`
- Agent-specific `## Standing Rules` — moves to `agent-builder-skill`

Cross-cutting permissions and standing rules that apply to every agent (e.g., "never commit secrets", "always use conventional commits") remain in the constitution.

The `write_mode` parameter still governs where the output is written (`in_place_skill`, `composed_agent_file`, `standalone_constitution`), but the content written is now domain knowledge only rather than the full agent configuration.

**Pain context:** Per DEC-026 D5, the canonical pipeline is constitution-builder (Tier 1, once) → agent-builder × N (Tier 2, per role × domain). Constitution-builder must be narrowed to domain knowledge so it stays stable and slow-changing; per-agent routing is fast-changing and belongs in agent-builder.

> **Scope note:** Routing generation moves to `agent-builder-skill` (story: `agent-builder-skill`). That story must be activated before or alongside this one.

## DEC-038 Alignment

**DEC-038** ratifies that an agent's per-role×domain routing is its **manifesto** — a *stable diagnostic table* mapping observable developer symptoms to the exact `wiki-query` lookup for each. That table is owned **per agent**, at the manifesto/`agent-builder` layer. This sharpens the constitution-vs-routing split this story already encodes:

- **The shared constitution must NOT own per-agent routing.** A project-shared `## Quick Routing` table is meaningless for a `pm` or `architect` — a shared Compose/Kotest routing table only makes sense for a frontend specialist. Per-agent routing (the diagnostic table) belongs in the per-agent manifesto / composed-agent layer, not in any write mode that emits shared, project-wide content.
- **Write modes must respect the split.** Whatever a write mode emits for the shared constitution carries only project-wide, agent-agnostic content (embedded facts, KB-sourced context, the shared wiki-query interface). The per-agent diagnostic table is layered on by the manifesto/`agent-builder` step, not by constitution-builder.
- **`## Quick Routing` ownership is reconciled here**, consistent with the sibling story `constitutionmd-generation-acceptance-criteria`: shared content stays project-wide; per-agent routing is per-agent (the manifesto). Per DEC-038, `wiki-query` (DEC-018) is also extended to address multiple per-project KBs, and agents are project-scoped — so the KB-sourced context a constitution emits is scoped to *this* project's KB(s).

## Acceptance Criteria

ACs reflect DEC-026 D4 scope (domain knowledge only). Prior ACs assuming Permissions + Standing Rules + Quick Routing generation are superseded.

### write_mode parameter

1. `momentum:constitution-builder` accepts a `write_mode` argument that takes exactly one of three values: `in_place_skill`, `composed_agent_file`, `standalone_constitution`. Invoking the skill with any other value for `write_mode` is rejected with a message naming the three valid values.
2. The write-target path is supplied to the skill as an explicit argument; the skill does not infer the target path from the `write_mode` value alone (exception: `standalone_constitution`, which has a fixed canonical path per AC 11).
3. When `write_mode` is `in_place_skill` or `composed_agent_file` and no target path was supplied, the Elicit phase asks the developer "where should this constitution be written?" before any content is generated. When the path is already supplied, the skill does not re-ask.

### Domain-knowledge output (all write modes)

4. The constitution output contains an **embedded-facts** section covering stack identity, key conventions, and architectural constraints for the project.
5. The constitution output contains a **KB-sourced context** section populated via `wiki-query` lookups (DEC-018 interface) performed at generation time.
6. The constitution output includes the **wiki-query interface block** (DEC-018) as shared infrastructure available to all agents.
7. The constitution output contains **no `## Quick Routing` section** — routing tables are not generated by constitution-builder under any write mode.
8. The constitution output contains **no agent-specific `## Permissions` section** — agent-specific permissions are not generated by constitution-builder.
9. The constitution output contains **no agent-specific `## Standing Rules` section** — agent-specific standing rules are not generated by constitution-builder.
10. Cross-cutting permissions and standing rules that apply to *every* agent in the project (e.g., "never commit secrets", "always use conventional commits") MAY appear in the constitution output; only *agent-specific* permissions/rules/routing are excluded.
11. Per DEC-038 (multi-KB, project-scoped agents): the KB-sourced context is scoped to *this* project's KB(s) — `wiki-query` lookups address the invoking project's own knowledge base(s), not another project's.

### write_mode behavior

12. `in_place_skill` mode writes the domain-knowledge sections into an **existing** `SKILL.md` at the supplied path, preserving the file's other content.
13. `composed_agent_file` mode writes the domain-knowledge sections into a **standalone agent file** at the supplied path. Agent-specific configuration (routing, per-agent permissions) is supplied separately by `agent-builder-skill`, not by this mode.
14. `standalone_constitution` mode writes the universal Tier 1 constitution to the canonical path `.claude/guidelines/constitution.md`.

### Routing delegation

15. The skill workflow contains **no phase** that generates routing tables or agent-specific routing entries — any such phase present in the current implementation is removed.
16. The skill workflow explicitly states (in a note or comment) that routing-table / per-agent-routing generation is the responsibility of `agent-builder-skill` (the manifesto/diagnostic-table layer), per DEC-038.

### Skill-document NFR compliance

17. The SKILL.md `description` field is ≤150 characters and accurately reflects the narrowed (domain-knowledge-only) behavior — it no longer advertises generating `## Permissions` + `## Standing Rules` + `## Quick Routing` as the skill's purpose.
18. `model:` and `effort:` frontmatter fields remain present in SKILL.md; the skill body stays ≤500 lines / 5000 tokens (overflow, if any, moves to `references/` with a load instruction).

## Tasks / Subtasks

- [ ] **Task 1 — Add the `write_mode` parameter and Elicit-phase path handling** (AC 1, 2, 3)
  - [ ] Define the `write_mode` argument with the closed value set `{in_place_skill, composed_agent_file, standalone_constitution}` and reject any other value with a message naming the three valid values (AC 1)
  - [ ] Accept the write-target path as an explicit argument; do not derive it from `write_mode` for `in_place_skill`/`composed_agent_file` (AC 2)
  - [ ] In the Elicit phase, ask for the target path only when it was not supplied and the mode requires one (AC 3)

- [ ] **Task 2 — Narrow generated content to domain knowledge only** (AC 4, 5, 6, 7, 8, 9, 10, 11)
  - [ ] Replace the `## Permissions` / `## Standing Rules` / `## Quick Routing` generation with embedded-facts + KB-sourced-context + wiki-query-interface generation (AC 4, 5, 6)
  - [ ] Remove agent-specific Permissions, Standing Rules, and Quick Routing generation; ensure none appears in output (AC 7, 8, 9)
  - [ ] Permit only project-universal cross-cutting permissions/rules in output (AC 10)
  - [ ] Scope `wiki-query` lookups to the invoking project's KB(s) per DEC-038 multi-KB / project-scoped model (AC 11)

- [ ] **Task 3 — Implement the three write-mode behaviors** (AC 12, 13, 14)
  - [ ] `in_place_skill`: insert/replace domain-knowledge sections in an existing SKILL.md at the supplied path, preserving other content (AC 12)
  - [ ] `composed_agent_file`: write domain-knowledge sections to a standalone agent file at the supplied path (AC 13)
  - [ ] `standalone_constitution`: write the universal Tier 1 constitution to `.claude/guidelines/constitution.md` (AC 14)

- [ ] **Task 4 — Remove routing-generation phase and document the delegation** (AC 15, 16)
  - [ ] Delete the routing-entry-generation phase (current SKILL.md Phase 6 "Generate Routing Entries" and the Quick Routing parts of Phases 1, 7, 8) (AC 15)
  - [ ] Add a note/comment stating routing/diagnostic-table generation is owned by `agent-builder-skill` per DEC-038 (AC 16)

- [ ] **Task 5 — Bring SKILL.md into NFR compliance and update its self-description** (AC 17, 18)
  - [ ] Rewrite the `description` frontmatter to ≤150 chars describing the narrowed domain-knowledge-only behavior and the `write_mode` parameter (AC 17)
  - [ ] Confirm `model:`/`effort:` present and body ≤500 lines / 5000 tokens; move overflow to `references/` if needed (AC 18)

- [ ] **Task 6 — EDD: author and run behavioral evals** (covers AC 1, 7, 12–16)
  - [ ] Write 2–3 behavioral evals under `skills/momentum/skills/constitution-builder/evals/` exercising: write_mode value rejection, no-`## Quick Routing`-in-output, and per-mode target-path behavior
  - [ ] Run the EDD cycle and confirm eval behaviors (or document failures)

## Dev Notes

### Decision Authority

- **DEC-026 D4** is the authoritative scope source: constitution-builder generates **domain knowledge only** (embedded facts + KB-sourced context + wiki-query interface). Permissions, Standing Rules, and Quick Routing are explicitly out of scope for this skill.
- **DEC-026 D5** establishes the pipeline ordering: constitution-builder (Tier 1, once) → agent-builder × N (Tier 2, per role × domain). Constitution must stay stable/slow-changing; per-agent routing is fast-changing and lives in agent-builder.
- **DEC-038** ratifies the manifesto as the per-agent **diagnostic table** (observable symptom → exact `wiki-query`), owned at the manifesto/agent-builder layer — **never** in the shared constitution. It also extends `wiki-query` (DEC-018) to multiple per-project KBs and declares agents project-scoped.
- **DEC-018** defines `wiki-query` as the Tier 3 cold-KB interface (extended by DEC-038 to multiple per-project KBs).
- Architecture Decision 56 (DEC-026 D3/D5) and the "Routing ownership — per-agent, not shared constitution (DEC-038)" block in `architecture.md` name **this story** and its sibling `constitutionmd-generation-acceptance-criteria` as the owners of the `## Quick Routing` reconciliation. Architecture also notes: `constitution-builder writes only constitution.md` / `agent-builder is the sole authorized writer to momentum/agents.json project block` — constitution-builder must not write routing into agents.json.

### Current State of Affected Files

- **`skills/momentum/skills/constitution-builder/SKILL.md`** (exists, ~245 lines, ~9.6 KB). The workflow is currently **inline in SKILL.md** as Phases 1–8 — there is no separate `workflow.md` file in the skill directory (verified: directory contains only `SKILL.md` and `evals/`). Current behavior is the *pre-narrowing* design — it generates exactly the three sections this story removes:
  - Phase 2 "Permission Scoping" generates `## Permissions` (plus a `settings.json` snippet) — **to be removed / narrowed to project-universal only**.
  - Phase 3 "Generate Standing Rules" generates `## Standing Rules` — **to be removed / narrowed to project-universal only**.
  - Phases 4–7 (Audit KB, Fill Gaps, Generate Routing Entries, Review) build and write `## Quick Routing` — **routing generation to be removed entirely** (Task 4).
  - There is **no `write_mode` parameter today** — the skill always writes into a single target SKILL.md path via Phase 8.
  - The frontmatter `description` is ~600 characters and explicitly advertises `## Permissions + ## Standing Rules + ## Quick Routing` — it violates NFR1 (≤150 chars) and is now inaccurate; Task 5 rewrites it.
- **`skills/momentum/skills/constitution-builder/workflow.md`** — **does not exist on disk.** The story `touches` lists it because the canonical skill shape separates SKILL.md (frontmatter + body) from workflow.md (procedural steps). Dev decision required (see Concerns): either (a) keep the workflow inline in SKILL.md and refactor it there, or (b) split the procedural workflow out into a new `workflow.md`. Either approach must satisfy the ACs; the `touches` path is retained so the index reflects the intended file surface.
- **`skills/momentum/skills/constitution-builder/evals/`** — exists; Task 6 adds behavioral evals here.

### Architecture Compliance

- Three-tier model (DEC-001 / DEC-008 D1, restated in architecture Decision 56): Tier 1 Hot Constitution (project-wide, this skill) → Tier 2 Composed Agent File (per-agent, agent-builder) → Tier 3 Cold KB (wiki vault via `wiki-query`). This story keeps constitution-builder firmly in Tier 1 and strips anything per-agent.
- `wiki-query` is the only sanctioned cold-KB access path (DEC-018); KB-sourced context must be produced through it, not by direct vault reads embedded as static content beyond what `wiki-query` returns at generation time.
- Writer-authority constraint (architecture Decision 56): constitution-builder writes only constitution content (SKILL.md / agent file / `constitution.md`) — it must not write routing entries into `momentum/agents.json` (that is agent-builder's sole authority).
- FR136/FR138/FR142 cross-reference: the constitution is layer (2) of the three-layer composition; this story enforces that the constitution layer carries no manifesto (diagnostic-table) content.

### Testing Requirements

- This is a `skill-instruction` change → **EDD (Eval-Driven Development)**, not TDD. Skill instructions are non-deterministic LLM prompts; unit tests do not apply.
- Verification method (advisory): `skill-invoke` (per the routing table in `skills/momentum/references/rules/verification-standard.md` Section 1: `skill-instruction` → `skill-invoke`). The verifier invokes the skill and observes routing/response/halt behavior; it does not read implementation internals (anti-insider-knowledge guard, Section 4).
- Author evals before implementing (Task 6). Suggested behavioral evals:
  - Given an unrecognized `write_mode` value, the skill rejects it and names the three valid values (AC 1).
  - Given any valid `write_mode`, the generated/written output contains no `## Quick Routing` section (AC 7).
  - Given `standalone_constitution`, the skill targets `.claude/guidelines/constitution.md`; given `in_place_skill`/`composed_agent_file` without a path, it elicits the path (AC 3, 14).
- A frozen verification contract for this sprint will exist at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done; Dev does not read the Part-B verifier body (scenarios/assertions/Gherkin) beyond sections `how_dev_self_checks` explicitly references.

### Project Context Reference

- Sibling/coordinating stories in epic `momentum-agent-composition-pipeline`:
  - `constitutionmd-generation-acceptance-criteria` (shares the `## Quick Routing` ownership reconciliation per DEC-038 — keep the two stories' ACs consistent).
  - `agent-builder-skill` / `manifesto-builder-skill-generate-then-curate` (receive the routing + per-agent permissions this story removes — must be activated before or alongside this story so routing is not orphaned).
  - `build-guidelines-skill` (orchestrator; primary consumer of the new write modes).
  - `wiki-query-interface-block-for-hot-constitution` (defines what `standalone_constitution` mode must include).
- Per-project KB scoping (DEC-038 / FR142): Momentum maintains its own KB; the nornspun `cmp-dev.md` is a format exemplar only (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`).

### References

- `momentum:constitution-builder` SKILL.md and workflow.md (current behavior to be narrowed)
- `agent-builder-skill` story (receives routing + agent-specific permissions; must coordinate with this story)
- `build-guidelines-skill` story (primary consumer of new write modes)
- `constitutionmd-generation-acceptance-criteria` story (sibling — shares the `## Quick Routing` ownership reconciliation per DEC-038)
- `wiki-query-interface-block-for-hot-constitution` (defines what `standalone_constitution` mode must include)
- DEC-038 — manifesto = per-agent diagnostic table; per-agent routing owned at the manifesto/agent-builder layer, NOT the shared constitution; per-project multi-KB, project-scoped agents (reconciles `## Quick Routing` ownership for this story)
- DEC-026 D4 — constitution-builder rework, domain knowledge only (authoritative scope source)
- DEC-026 D5 — three-skill pipeline: constitution-builder → agent-builder × N → routing table
- DEC-018 — wiki-query as Tier 3 cold KB interface (extended by DEC-038 to multiple per-project KBs)
- DEC-013 — universal agent model
- DEC-001 — three-tier agent guidelines architecture
- architecture.md — Decision 56 (DEC-026 D3/D5) and "Routing ownership — per-agent, not shared constitution (DEC-038)" block; writer-authority constraint (constitution-builder writes only constitution.md)
- prd.md — FR136 (Gen-2 composition model), FR138 (agent-builder pipeline), FR142 (per-project multi-KB + KB buildout)
- `skills/momentum/references/rules/verification-standard.md` — Section 1 method routing (`skill-instruction` → `skill-invoke`)
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/constitution-builder/evals/` (the dir already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-rejects-unknown-write-mode.md`, `eval-output-has-no-quick-routing.md`, `eval-standalone-mode-targets-canonical-path.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify the SKILL.md (and/or split out a `workflow.md` — see the open decision in Dev Notes → Current State) to add `write_mode`, narrow content to domain knowledge, and remove routing generation.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md (and workflow.md if split) contents as context, or invoke the skill via its Agent Skills name if installed. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely. The current description (~600 chars) MUST be rewritten (AC 17).
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23) — both are currently present; preserve them.
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3).
- Skill name uses the `momentum:` namespace (NFR12) — already satisfied (`constitution-builder`).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/constitution-builder/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented SKILL.md against story ACs)

**Frozen verification contract reminder:** A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Before signaling done, read only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Do not read the Part-B verifier body (scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

_This section is populated by the dev agent during implementation._
