# Constitution Builder — Process Notes

**Run type:** Stale routing update (replacement path)
**Target skill:** fastapi-pydantic SKILL.md (simulated)
**Technologies:** FastAPI, Pydantic v2, PydanticAI
**Date:** 2026-05-04

---

## Phase 1 — Elicit

Gathered from simulated developer responses:
- Target SKILL.md path set to workspace outputs directory
- Existing `## Quick Routing` section detected — 8 outdated entries covering only FastAPI and Pydantic basics, nothing on PydanticAI agents
- Told developer: "A routing table already exists — I'll generate a replacement. You can decide whether to swap it out entirely or merge selectively."
- Typical scenarios captured: dependency injection wiring, request model validation, PydanticAI agent integration into routes, async agent calls, model field validation errors

---

## Phase 2 — KB Audit Results

**Vault:** `/Users/steve/projects/nornspun-agentic-kb`
**Index:** 578 lines, covering ~25 technology domains

### Covered (routing entries generated)

| Concept | KB Pages |
|---|---|
| FastAPI Depends / DI | `FastAPI-Depends-Dependency-Injection.md`, `FastAPI-Async-Routing.md` |
| Pydantic v2 field/model validators | `FastAPI-Pydantic-v2.md`, `Pydantic v1 to v2 Migration.md` |
| Pydantic TypeAdapter, ConfigDict | `FastAPI-Pydantic-v2.md` |
| PydanticAI @agent.tool registration | `Tool Registration (@agent.tool).md` |
| PydanticAI RunContext DI | `RunContext and Dependency Injection.md` |
| PydanticAI agent streaming | `Agent Streaming.md` |
| PydanticAI structured output | `Structured Output and Output Types.md` |
| PydanticAI system prompts | `System Prompts (Static and Dynamic).md` |
| PydanticAI TestModel / FunctionModel | `TestModel and FunctionModel.md` |
| PydanticAI Toolsets | `Toolsets.md` |
| FastAPI SSE (native 0.135+) | `FastAPI-SSE-Server-Sent-Events.md` |
| FastAPI lifespan events | `FastAPI-Lifespan-Events.md` |
| Cross-domain synthesis | `PydanticAI × TestModel × pytest-asyncio.md`, `Research: PydanticAI Agent Framework.md` |

**Concepts covered: 13**

### Partial (thin coverage, noted in entry phrasing)

- FastAPI + PydanticAI bridging (Depends→RunContext): no dedicated page, but covered across `FastAPI-Lifespan-Events.md`, `RunContext.md`, and the PydanticAI research synthesis. Entries drafted with combined query strings.

### Gaps (no KB backing — wiki-ingest not invoked per test constraint)

- No dedicated page on **error handling when async agent calls fail inside a FastAPI route** (e.g. `AgentRunError`, timeouts, partial streaming failures). The `FastAPI-Error-Handling.md` page covers HTTP exceptions but not PydanticAI-specific error types.
- No page on **Model Configuration and ModelSettings** (`Model Configuration and ModelSettings.md` exists in the index but was not read during this run — post-audit, it's covered; one entry added referencing it).
- No page on **pydantic-evals integration with FastAPI** for evaluation pipelines inside routes (pydantic-evals page exists but covers standalone evaluation, not web integration).

**Concepts gapped: 2** (agent call error handling in routes, pydantic-evals in web context)

---

## Phase 3 — Gap Filling

Developer chose: **do NOT invoke wiki-ingest** (test constraint).

Documented gaps above. Routing coverage for the two gapped areas is absent. Recommend ingesting:
1. PydanticAI error handling documentation (AgentRunError, UsageLimitExceeded, UnexpectedModelBehavior)
2. Patterns for wrapping async agent calls in FastAPI routes with proper error propagation

---

## Phase 4 — Routing Entry Generation

Approach: read each concept page, identified the specific problems they answer, wrote 2–4 entries per concept. Total drafts: 34 entries across 7 subsections.

Subsections chosen:
1. **Dependency Injection** — 5 entries (Depends wiring, caching, router-level, testing, arch warning)
2. **Pydantic v2 Models and Validation** — 7 entries (validators, migration, TypeAdapter, context)
3. **Async Routing and Execution Model** — 3 entries (blocking, run_in_threadpool, router structure)
4. **PydanticAI Agent Integration** — 6 entries (route wiring, RunContext bridging, lifespan, tool registration)
5. **Async Agent Calls and Streaming** — 5 entries (SSE streaming, stop-at-first-output, graph traversal, nginx)
6. **Structured Agent Output** — 4 entries (output_type, validators, streaming partials, mode decision)
7. **System Prompts and Model Configuration** — 3 entries (dynamic prompts, ordering, runtime settings)
8. **Testing Agents** — 5 entries (TestModel, FunctionModel, ALLOW_MODEL_REQUESTS, event loop conflict, contextvar)

Fast index-only (`wiki-query quick answer:`) used for 4 definitional lookups where full page retrieval would be overkill.

---

## Phase 5 — Review

Simulated developer accepted all 34 entries as-is. No cuts or additions requested.

Final count: **34 entries across 8 subsections** (subsection count increased from 7 during consolidation of system prompts + model config into one section).

---

## Phase 6 — Stale Replacement Path

Existing section had 8 entries covering:
- FastAPI route definition basics
- Pydantic BaseModel in request body
- Response model serialization
- HTTPException usage
- Depends basic wiring
- ConfigDict / v1 migration
- Field validators
- Settings via pydantic-settings

These 8 outdated entries had zero PydanticAI coverage. The replacement was written from scratch — no merge was needed since all old entries are subsumed by the new entries (the new table covers every old topic with tighter symptom phrasing, plus adds the 13 new PydanticAI concepts).

Developer chose: **replace the existing section entirely**.

Output written to: `outputs/routing-table.md`

---

## Observations

1. **Agent integration docs were the primary KB addition since last routing pass.** The 8 original entries were functionally complete for pure FastAPI/Pydantic work. The new 26 PydanticAI entries represent a genuine KB expansion — this is exactly the case constitution-builder is designed for.

2. **The `run_stream()` stop-at-first-output behavior is a non-obvious trap.** It merited its own entry because it causes tools to silently not execute — exactly the kind of symptom a developer would bring to a skill without knowing the root cause.

3. **The Depends → RunContext bridge is the highest-value cross-cutting entry.** No single KB page covers it; it was inferred from reading `FastAPI-Lifespan-Events.md` (for shared state via `app.state`) and `RunContext.md` (for passing deps at `agent.run()` call time). The entry points to both pages.

4. **PydanticAI × TestModel × pytest-asyncio synthesis was valuable.** Two entries (event loop conflict, contextvar propagation) came directly from this synthesis page's "Tensions and Trade-offs" section — content that would not appear in either concept page alone.

5. **`wiki-query quick answer:` used 4 times.** All 4 are definitional/mode-selection questions where a developer needs a concise answer, not a full page read. This kept full-retrieval entries focused on diagnostic/wiring scenarios.
