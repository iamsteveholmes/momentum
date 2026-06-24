---
title: Build Nornspun Agent Constitution (Tier 1 Hot Context)
story_key: nornspun-agent-constitution
status: ready-for-dev
epic_slug: momentum-agent-composition-pipeline
feature_slug: ""
story_type: feature
priority: medium
change_type:
  - specification
verification_method_advisory: document-review
depends_on: []
touches:
  - "/Users/steve/projects/nornspun/.claude/guidelines/constitution.md"
---

# Build Nornspun Agent Constitution (Tier 1 Hot Context)

## Story

As a developer,
I want a tight Tier 1 constitution file for nornspun agents,
so that every agent — whether spawned by sprint planning or invoked ad-hoc — operates with the right project-specific context, routing, and KB access without requiring developer guidance each time.

## Description

The three-tier Codified Context architecture (DEC-008) defines: Tier 1 hot constitution (always loaded), Tier 2 composed specialist files (loaded at spawn), Tier 3 cold KB (on-demand retrieval). The nornspun-agentic-kb vault was built as the Tier 3 cold layer. This story builds the Tier 1 constitution.

The constitution for nornspun is intentionally narrow — ~100-150 lines, not the 660-line reference implementation — because Momentum's sprint planning already handles structured routing. The constitution covers only what planning cannot: ad-hoc invocations and project-specific invariants every agent must honor.

**This is the concrete G1 TEST BED for the agent-composition pipeline.** nornspun is a DIFFERENT project from Momentum — it lives at `~/projects/nornspun` with its own architecture docs, decisions, and a real cold KB at `~/projects/nornspun-agentic-kb`. The constitution authored here is the first real Tier-1 artifact produced for a non-Momentum project, validating the three-tier architecture against a genuine target. (See Concerns / Reconciliation in Dev Notes for how this hand-authored build relates to the constitution-builder orchestrator that will later generate it.)

**Key design decisions from conversation:**
- Sprint planning drives routing for structured work; the constitution handles ad-hoc only
- The routing table maps file patterns / task types to specialist agents as a fallback
- CMUX layout is now hardcoded globally (see `~/.claude/rules/cmux.md`) — the constitution should reference it, not re-define it
- The cold KB lives at `~/projects/nornspun-agentic-kb`; agents need JIT retrieval instructions, not the index pre-loaded

**Pain context:** Without the constitution, ad-hoc agent invocations on nornspun lack context about the project's invariants (async-first, repository pattern, SSE contract, cost caps). Agents reinvent decisions already captured in architecture docs and the KB. The KB exists but agents aren't wired to query it.

**Scope note (per DEC-026 D4):** The constitution carries **project domain knowledge only** — stack facts, conventions, architectural invariants shared by ALL agents, plus the wiki-query interface block as shared infrastructure. It does NOT contain agent-specific routing entries (file-pattern → role mappings); those are agent-specific and belong in each agent's manifesto (the agent-builder's concern). Tier 2 specialist files are out of scope for this story.

## Acceptance Criteria

1. A constitution file exists at `~/projects/nornspun/.claude/guidelines/constitution.md` (the Tier-1 path defined by DEC-008 D1: `.claude/guidelines/constitution.md`). If a path other than `.claude/guidelines/constitution.md` is agreed during implementation, the agreed path is recorded in the Dev Agent Record with rationale.

2. The constitution file body is ≤ 150 lines (intentionally narrow; not the 660-line reference target). Line count is verified by `wc -l` and recorded in the Dev Agent Record.

3. The constitution contains a **Project Invariants** section that documents, at minimum, each of the following invariants — every entry traceable to a nornspun architecture decision or guideline:
   - **async-first** — no blocking calls in async routes; long-running generation runs as `asyncio` tasks via the in-process task registry, not FastAPI `BackgroundTasks` (nornspun Decision 19).
   - **repository / data-layer access** — all storage access goes through the `StorageBackend` protocol / data layer, not ad-hoc direct DB calls (nornspun architecture.md data model).
   - **SSE contract** — the streaming event contract distinguishes conversation events (`message.*`, `tool.*`) from background-task events (`task.background.*`) on a single SSE connection; event types follow the documented prefix convention (nornspun Decision 20).
   - **snake_case wire format** — JSON wire payloads use snake_case field names.
   - **per-session cost cap enforcement** — agents respect the per-session cost-control posture (e.g., silence-mode suppresses Inner Thoughts computation, no separate evaluation LLM calls) per nornspun Decision 21/22.

4. The constitution contains a **Cold KB pointer** section that:
   - names the vault path (`~/projects/nornspun-agentic-kb`),
   - states WHEN to query (unfamiliar API, pattern uncertainty, library-version questions),
   - includes a wiki-query interface block (how to invoke the wiki-query skill or grep the vault) as shared infrastructure available to all agents (per DEC-026 D4: the wiki-query block stays in the constitution). The exact canonical both-mode block (fast index-only + full-body) is extended by the sibling story `nornspun-agent-constitution-wiki-query-block`; this story provides the section and a working pointer, and does not duplicate that story's verbatim-block scope.

5. The constitution does NOT contain agent-specific file-pattern → role routing entries (e.g., `*.kts` → dev-build, `*.kt` in `composeApp/` → dev-frontend). Confirmed by inspection — these belong in the per-agent manifesto (agent-builder's concern), not the constitution (per DEC-026 D4 scope narrowing).

6. The constitution references the global CMUX layout rule (`~/.claude/rules/cmux.md`) rather than re-defining the layout (CMUX is now hardcoded globally).

7. Every invariant and pointer in the constitution is validated against nornspun's authoritative sources before the story is considered done: `~/projects/nornspun/docs/planning-artifacts/architecture.md`, the relevant entries in `~/projects/nornspun/docs/decisions/`, and `~/projects/nornspun/docs/guidelines/`. Any invariant that cannot be traced to a source is removed or corrected. The validation cross-references are recorded in the Dev Agent Record.

8. Out of scope, confirmed by inspection: Tier 2 specialist files (Python backend dev, Kotlin/Compose dev, QA) are NOT created by this story — they are tracked separately. The constitution contains no Tier-2 specialist content.

## Tasks / Subtasks

- [ ] **Task 1 — Extract nornspun invariants from authoritative sources** (AC: 3, 7)
  - Read `~/projects/nornspun/docs/planning-artifacts/architecture.md` and the relevant `~/projects/nornspun/docs/decisions/` files; confirm exact wording for async-first (Decision 19), the SSE event contract (Decision 20), the cost-control / silence posture (Decision 21/22), the repository/StorageBackend data-layer pattern, and snake_case wire format.
  - Record the source citation (file + decision number / section) for each invariant. Drop any invariant that cannot be traced to a source.

- [ ] **Task 2 — Author the constitution file** (AC: 1, 2, 3, 6)
  - Create `~/projects/nornspun/.claude/guidelines/constitution.md` (Tier-1 path per DEC-008 D1). Create the `.claude/guidelines/` directory in the nornspun project if it does not exist.
  - Write the **Project Invariants** section covering each invariant from Task 1, each with its source citation.
  - Add a one-line reference to the global CMUX layout rule (`~/.claude/rules/cmux.md`); do not re-define the layout.
  - Keep the body ≤ 150 lines; verify with `wc -l`.

- [ ] **Task 3 — Author the Cold KB pointer section** (AC: 4)
  - Add the **Cold KB pointer** section: vault path `~/projects/nornspun-agentic-kb`, the WHEN-to-query triggers, and a wiki-query interface block (skill invocation or vault grep) as shared infrastructure.
  - Leave the verbatim canonical both-mode wiki-query block to the sibling story `nornspun-agent-constitution-wiki-query-block`; provide a working pointer/section here that that story extends.

- [ ] **Task 4 — Enforce scope boundaries** (AC: 5, 8)
  - Confirm by inspection that the constitution contains NO agent-specific file-pattern → role routing entries (those move to the manifesto per DEC-026 D4).
  - Confirm the constitution contains no Tier-2 specialist content (those are tracked separately).

- [ ] **Task 5 — Validate against nornspun sources and record cross-references** (AC: 7)
  - Cross-reference every invariant/pointer against architecture.md, the cited decisions, and `docs/guidelines/`. Correct or remove any unsupported claim.
  - Record the validation cross-reference map and the final line count in the Dev Agent Record.

## Dev Notes

### Decision Authority

- **DEC-008 D1** (Three-tier project layout — ADOPTED): defines the canonical Tier-1 path `.claude/guidelines/constitution.md` — "hot, always loaded, critical rules and pointers"; Tier-3 cold layer is a separate `{project}_vault/` repo populated by KB skills and distilled by build-guidelines. This story builds the Tier-1 artifact for nornspun.
- **DEC-026 D4** (constitution-builder rework — domain knowledge only — ADOPTED): the constitution generates ONLY project domain knowledge — stack facts, conventions, and architectural patterns shared by all agents. Routing moves to the per-agent manifesto (agent-builder's concern). The wiki-query interface block (DEC-018) stays in the constitution as shared infrastructure. This story honors that scope: invariants + KB pointer in; agent-specific routing out.
- This story **predates DEC-038** and references DEC-008 / DEC-026 D4. Its intent — a narrow, hand-authored Tier-1 constitution for the nornspun test bed, scoped to domain knowledge only — is preserved as-is. No DEC-038 re-framing is applied here; any reconciliation with the constitution-builder orchestrator is captured in Concerns below, not resolved by this story.

### Current State of Affected Files

- `~/projects/nornspun/.claude/guidelines/constitution.md` — **does not yet exist**. The nornspun project has `~/projects/nornspun/.claude/` with `agents/`, `momentum/`, `rules/`, `skills/`, `settings.json`, and `settings.local.json`, but **no `guidelines/` directory yet**. This story creates `guidelines/constitution.md`.
- `~/projects/nornspun-agentic-kb` — **exists** (the Tier-3 cold KB vault). Agents need JIT retrieval instructions pointing here, not a pre-loaded index.
- `~/projects/nornspun/docs/planning-artifacts/architecture.md` — **exists**; authoritative source for async-first (Decision 19), SSE contract (Decision 20), cost/silence posture (Decision 21/22), data-layer/StorageBackend pattern, snake_case wire format.
- `~/projects/nornspun/docs/decisions/` and `~/projects/nornspun/docs/guidelines/` — **exist**; secondary authoritative sources (the latter holds stack guidelines: compose-ui-patterns, gradle-agp-build, kmp-testing-stack, kotlin-kmp-conventions, ktor-sse-patterns).

### Architecture Compliance

- **Tier-1 hot context only.** Always-loaded, slow-changing content. No Tier-2 specialist material; no Tier-3 index pre-loaded.
- **Domain-knowledge-only scope (DEC-026 D4).** Shared project knowledge, not agent-specific routing. The constitution is identical for every nornspun agent.
- **Path convention (DEC-008 D1).** `.claude/guidelines/constitution.md` is the canonical Tier-1 path. Any deviation must be recorded with rationale.
- **No CMUX re-definition.** Reference the global rule; CMUX is hardcoded globally (`~/.claude/rules/cmux.md`).
- **Narrow by design.** ≤ 150 lines. Momentum's sprint planning already supplies structured routing; the constitution covers only ad-hoc invocation context and project invariants.

### Testing Requirements

- **Change type:** `specification` (a project-domain knowledge document authored under `.claude/guidelines/`).
- **Verification method (advisory):** `document-review` — per the routing table in `skills/momentum/references/rules/verification-standard.md` Section 1 (`specification` → `document-review`). No automated driver; the artifact is verified by inspection and cross-reference.
- **What to verify:**
  - File exists at the Tier-1 path and body is ≤ 150 lines (`wc -l`).
  - Every required invariant (AC 3) and pointer (AC 4) is present.
  - Every invariant traces to a cited nornspun source (architecture.md / decisions / guidelines) — no unsupported claims (AC 7).
  - Scope boundaries hold: no agent-specific routing entries (AC 5); no Tier-2 specialist content (AC 8); CMUX referenced not redefined (AC 6).

### Project Context Reference

- **Target project:** nornspun (`~/projects/nornspun`) — a DIFFERENT project from Momentum. All authoring and validation happen against nornspun's own sources, not Momentum's.
- **Cold KB:** `~/projects/nornspun-agentic-kb` (Tier-3 vault, already built).
- **G1 test bed:** This is the first real Tier-1 constitution produced for a non-Momentum project under the agent-composition pipeline — it validates the three-tier architecture end-to-end against a genuine target.
- **Sibling story:** `nornspun-agent-constitution-wiki-query-block` extends the Cold KB pointer section with the verbatim canonical both-mode wiki-query block (DEC-018). This story provides the section + a working pointer; it does not duplicate that story's verbatim-block scope.

### Concerns / Reconciliation

- **Hand-authored build vs. the constitution-builder orchestrator (G1 framing).** This story manually authors the nornspun Tier-1 constitution. The parent epic `momentum-agent-composition-pipeline` also contains the work to build/rework the `constitution-builder` skill (the orchestrator that GENERATES such constitutions) and `constitutionmd-generation-acceptance-criteria` (the generation ACs). There is a potential overlap/drift risk: the hand-authored nornspun constitution and the auto-generated output must converge on the same shape (domain-knowledge-only per DEC-026 D4, ≤ ~150 lines for narrow projects, wiki-query block as shared infrastructure). Reconciliation guidance for the developer: treat this story's output as the **golden reference artifact** for what constitution-builder should later be able to produce for nornspun — i.e., when constitution-builder is run on nornspun in a future story, its output should be diffable against this hand-authored file. If the generation ACs (`constitutionmd-generation-acceptance-criteria`) diverge from the structure produced here, flag the divergence at that story rather than retro-fitting this one. Do not block this story on the orchestrator existing — the hand-authored test-bed artifact is the point.

### References

- DEC-008: Composable Specialist Agents Architecture — Three-Tier Layout (`_bmad-output/planning-artifacts/decisions/dec-008-composable-agents-architecture-2026-04-22.md`) — D1 defines the Tier-1 constitution path.
- DEC-026: Build Pipeline Redesign (`_bmad-output/planning-artifacts/decisions/dec-026-build-pipeline-redesign-2026-05-16.md`) — D4 narrows constitution scope to domain knowledge only; wiki-query block stays as shared infrastructure.
- Lens B2: Context Engineering Ecosystem (`_bmad-output/research/agent-guidelines-discovery-2026-04-09/raw/lens-b2-context-engineering-ecosystem.md`)
- Cold KB vault: `~/projects/nornspun-agentic-kb`
- nornspun architecture: `~/projects/nornspun/docs/planning-artifacts/architecture.md` (Decision 19 async tasks; Decision 20 SSE event contract; Decision 21/22 Inner Thoughts / Global Silence cost posture)
- nornspun stack guidelines: `~/projects/nornspun/docs/guidelines/` (compose-ui-patterns, gradle-agp-build, kmp-testing-stack, kotlin-kmp-conventions, ktor-sse-patterns)
- CMUX layout rule: `~/.claude/rules/cmux.md`
- Sibling story: `.momentum/stories/nornspun-agent-constitution-wiki-query-block.md`
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–5 → specification (direct authoring with cross-reference verification)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, decision, or parent spec) — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria — here, author `~/projects/nornspun/.claude/guidelines/constitution.md` with the Project Invariants section, the Cold KB pointer section, and the CMUX reference, scoped to domain-knowledge-only per DEC-026 D4.
2. **Verify cross-references:** every invariant and pointer must resolve to a real nornspun source. Confirm each invariant against `~/projects/nornspun/docs/planning-artifacts/architecture.md`, the cited `~/projects/nornspun/docs/decisions/` entries, and `~/projects/nornspun/docs/guidelines/`. Confirm the cold-KB vault path and CMUX rule path exist. Remove or correct anything that does not resolve.
3. **Verify format / scope compliance:** Tier-1 path per DEC-008 D1; body ≤ 150 lines; no agent-specific routing entries; no Tier-2 specialist content; CMUX referenced, not redefined.
4. **Document** in the Dev Agent Record: the final path used, the line count, the invariant → source cross-reference map, and confirmation of the scope boundaries.

**No tests or evals required** for specification changes. AVFL checkpoint (run by momentum:dev) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks (added to standard bmad-dev-story DoD):**
- [ ] All cross-references to nornspun documents, files, decisions, and the cold-KB vault resolve correctly
- [ ] Constitution is at the Tier-1 path (`.claude/guidelines/constitution.md`) per DEC-008 D1 (or agreed path recorded with rationale)
- [ ] Body ≤ 150 lines confirmed via `wc -l`
- [ ] Domain-knowledge-only scope confirmed: no agent-specific routing entries (DEC-026 D4); no Tier-2 specialist content
- [ ] CMUX referenced via `~/.claude/rules/cmux.md`, not re-defined
- [ ] Invariant → source cross-reference map recorded in Dev Agent Record
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

**Frozen verification contract reminder:** A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Before signaling done, Dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Dev does not read the verifier body (Part B: scenarios, assertion scripts) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

_This section is populated by the dev agent during implementation._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
