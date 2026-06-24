# Eval: Preserves Diagnostic-Table Framing (DEC-038 D1 — No Overlay)

**Eval ID:** build-guidelines-no-overlay
**Stakes:** correctness — overlay framing violates DEC-038 D1 and produces agents with wrong identity

## Scenario

**Given:**
- A manifesto at `.claude/manifests/dev-kotlin-compose.md` contains a `## Diagnostic Table` section with sprint-invariant symptom→`wiki-query` entries
- The current sprint is `sprint-2026-06-18` and the story slug is `some-story`
- The developer runs `/momentum:build-guidelines`

**When** the skill reads the manifesto and produces the composed agent file.

**Then** (observable behavior — all must hold):

1. The composed agent file's diagnostic table content is identical to the manifesto's `## Diagnostic Table` section — it is not re-scoped, regenerated, or filtered per sprint
2. No sprint slug (e.g., `sprint-2026-06-18`) appears anywhere in the composed agent file
3. No story slug (e.g., `some-story`) appears anywhere in the composed agent file
4. No text "overlay", "context overlay", "per-sprint", or "per-story" appears in the composed agent file
5. The composed file treats the manifesto as stable, standing input — it does not prompt the developer to "describe this sprint's context" or "what stories are planned for this sprint"
6. When an agent built from the composed file encounters a situation not in the diagnostic table, it emits an incompleteness signal (`[MANIFESTO INCOMPLETE: ...]`) rather than silently falling through to training knowledge

**Additionally**, the skill itself must not:
- Read, build, or write any per-sprint or per-story "context overlay" file
- Prompt the developer for story-level context to inject into the composed agent

## Outcome Criteria

**Pass:** Composed file embeds the diagnostic table verbatim; no sprint/story identifiers present; no overlay language.

**Fail:**
- Sprint slug or story slug found in composed file
- Skill prompts for story context during a run (e.g., "What stories are in this sprint?")
- Diagnostic table entries are rewritten or filtered based on sprint-specific information
- Composed agent missing the incompleteness-signal instruction when an unrouted situation is encountered
