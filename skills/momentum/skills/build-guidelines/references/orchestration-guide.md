# build-guidelines Orchestration Guide

This reference covers: the composition formula, manifesto consumption contract, multi-KB architecture, exemplar-shape specification, and agents.json schema.

---

## Composition Formula

Per `momentum-agent-composition-pipeline` epic:

```
composed_agent = base_body + constitution_excerpt + manifesto (diagnostic table + stack facts)
```

- **`base_body`** — from `skills/momentum/agents/{role}.md` (plugin-shipped, role-generic)
- **`constitution_excerpt`** — relevant sections from `.claude/guidelines/constitution.md` (Tier 1, project-wide)
- **`manifesto`** — the `## Diagnostic Table` + `## Project Stack` from `.claude/manifests/{role}-{domain}.md` (Tier 2, per-role×domain, sprint-invariant)

The composed file lives at `.claude/guidelines/agents/{role}-{domain}.md`.

**Why baked in, not injected at spawn time:** CLAUDE.md inheritance for subagents is unreliable (GitHub #29423). Path-scoped rules have a regression (GitHub #16299). The only guaranteed delivery channel is the agent file's system prompt body. Build-guidelines bakes guidelines in before the sprint starts — when sprint-dev spawns the composed file, the guidelines ARE the agent.

---

## Manifesto Consumption Contract

Per `skills/momentum/references/manifesto-format.md` (AC8):

| What build-guidelines reads | Where it lives | What build-guidelines does with it |
|---|---|---|
| `role` | Identity block | Determines base body to merge (`agents/{role}.md`) |
| `domain` | Identity block | Determines output file name (`{role}-{domain}.md`) |
| `project_kb` | Identity block | Scopes `wiki-query` resolution to the correct project KB |
| `## Project Stack` | Stack section | Bakes stack facts into composed agent for disambiguation |
| `## Diagnostic Table` | Diagnostic table section | Injects full symptom→`wiki-query` routing table (verbatim) |

**Sprint invariance (DEC-038 D1):** The manifesto is consumed as-is. The composed agent embeds the diagnostic table verbatim. Any change to the table requires editing the manifesto file — not a per-sprint override. No sprint or story identifier is added.

---

## Composed Agent File Shape (cmp-dev Exemplar Conformance)

Every composed file must match this structure (validated in Phase 6):

```markdown
---
name: {role}-{domain}
model: sonnet
effort: medium
tools: [Read, Glob, Grep, Bash, Edit, Write, Agent, Skill]
---

## Project Guidelines — {Stack} ({Date})

### Critical Rules (always active)
{version pins, hard prohibitions, never/always rules from manifesto stack section}

### Reference Docs (load on demand)
- Antipatterns → .claude/guidelines/refs/{domain}-antipatterns.md
- Testing → .claude/guidelines/refs/{domain}-testing.md
...

### Diagnostic Table
{## Diagnostic Table content from manifesto — verbatim}

---
{full base agent body, unchanged from skills/momentum/agents/{role}.md}
```

**Shape invariants:**
- Frontmatter: `name`, `model`, `tools` required
- Guidelines block (critical rules + diagnostic table) ABOVE the `---` separator
- Full unmodified base body BELOW the `---` separator
- No sprint identifier, no story identifier, anywhere in the file

Reference exemplar: `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`
(Format reference ONLY — a nornspun artifact, never a Momentum agent.)

---

## Multi-KB Architecture (DEC-038 D2)

Each manifesto declares `project_kb` in its identity block. Build-guidelines reads this to scope downstream `wiki-query` operations.

| Project | `project_kb` value |
|---|---|
| Momentum | `momentum-agentic-kb` |
| nornspun | `nornspun-agentic-kb` |
| Other project | `{project-name}-kb` |

**Current state:** `wiki-query` (DEC-018) resolves against the active vault. The multi-KB extension (FR142) routes lookups to a declared `project_kb` — planned but not yet implemented. The `project_kb` field is stored now so the pipeline is ready when FR142 lands.

**In constitution-builder invocations:** pass `project_kb` as context so constitution-builder can scope its wiki-query calls correctly once FR142 lands.

---

## agents.json Schema

Located at `momentum/agents.json` in the project root. Schema (as consumed by `momentum-tools agent resolve`):

```json
{
  "defaults": {
    "dev": "skills/momentum/agents/dev.md",
    "qa-reviewer": "skills/momentum/agents/qa-reviewer.md"
  },
  "project": [
    {
      "role": "dev",
      "domain": "kotlin-compose",
      "slug": "dev-kotlin-compose",
      "agent": ".claude/guidelines/agents/dev-kotlin-compose.md",
      "patterns": ["composeApp/**", "shared/**", "*.kt"],
      "write_permissions": ["composeApp/**", "shared/**", "*.kt"]
    }
  ]
}
```

**Field notes:**
- `slug` = `{role}-{domain}` — unique key, used by `momentum-tools agent resolve`
- `agent` — path to the composed agent file
- `patterns` — file glob patterns this agent owns; **populated at registration time** by agent-builder from the `permissions_scope` build-guidelines supplies. Never empty after registration. Used by `momentum-tools agent resolve --touches` to match the correct composed agent.
- `write_permissions` — mirrors `patterns`; the set of globs the agent is authorised to write. Populated at registration time alongside `patterns`.

**Creation:** if `momentum/agents.json` does not exist, create it with `{"defaults": {}, "project": []}`. Never overwrite the `defaults` block — it may have entries set by other tooling.

---

## Sprint-Dev Detection Contract (AC7)

Sprint-dev and the Conductor resolve the correct composed agent via `momentum-tools agent resolve --touches <touches>`. The tool matches the story's `touches` paths against the populated `patterns` arrays in `momentum/agents.json` and returns the matching composed slug and agent path.

Detection logic (in sprint-dev / Conductor, Phase 2):

```
touches = story's declared file-touch list (e.g., ["composeApp/**", "shared/src/**"])

result = momentum-tools agent resolve --touches <touches>
# → returns: { "slug": "dev-kotlin-compose",
#              "agent": ".claude/guidelines/agents/dev-kotlin-compose.md" }

IF result.agent EXISTS:
  Use result.agent as agent_path (guidelines already baked into system prompt)
ELSE:
  Fall back to generic skills/momentum/agents/{role}.md + guidelines-verification-gate warning
```

**Path naming:** when a composed-agent path must be referenced directly, it is always `.claude/guidelines/agents/{role}-{domain}.md` where `{domain}` is the manifesto's domain id (e.g. `kotlin-compose`). Never construct a path from the story's coarse `specialist` classification — always resolve via `agent resolve --touches`.

Deep spawn-wiring mechanics are owned by story `sprint-dev-composed-file-spawn-wiring`. Build-guidelines establishes the detection/fallback contract only.

---

## Known Limitation: patterns Derivation Is Best-Effort

Build-guidelines derives the `permissions_scope` globs (which become `patterns` in `agents.json`) from the manifesto's `## Project Stack` prose via LLM inference. This is a best-effort derivation — it is reliable for well-structured manifestos but is not fully deterministic.

**Root cause:** the manifesto-format spec (`skills/momentum/references/manifesto-format.md`) does not yet define a normative, machine-readable file-ownership / patterns field. Until it does, there is no structured source for build-guidelines to read globs from.

**Follow-up (cross-artifact — out of scope for this story):** for fully-deterministic G1 resolution, a normative `file_patterns` (or equivalent) field should be added to `manifesto-format.md`. This is owned by the `manifesto-format` story, not build-guidelines. Do not edit `manifesto-format.md` here.

---

## Incompleteness Signal

When a composed agent (at runtime) encounters a situation not covered by any diagnostic-table entry, it must emit an incompleteness signal — not silently fall through to training knowledge:

```
[MANIFESTO INCOMPLETE: no diagnostic-table entry for <situation>]
```

or

```
[MANIFESTO INCOMPLETE: wiki-query '<terms>' returned no usable result for <symptom>]
```

This signal surfaces to the developer, who then updates the manifesto and re-runs build-guidelines. This is the manifesto-completeness feedback loop (DEC-038 D1 Completeness Criterion).

---

## Cross-References

| Reference | Path |
|---|---|
| DEC-038 | `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` |
| DEC-001 | `_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md` |
| Manifesto format | `skills/momentum/references/manifesto-format.md` |
| constitution-builder | `skills/momentum/skills/constitution-builder/SKILL.md` |
| agent-builder | `skills/momentum/skills/agent-builder/workflow.md` |
| cmp-dev exemplar | `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` |
| momentum-tools agent resolve | `skills/momentum/scripts/momentum-tools.py` (~line 1972) |
