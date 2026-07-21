---
name: manifesto-builder
description: Drafts an agent's diagnostic-table manifesto from the project KB, then requires human curation of symptom wording before writing it to disk.
model: sonnet
effort: medium
user-invocable: true
allowed-tools: Read Grep Glob Bash Write Skill
---

# momentum:manifesto-builder

Produces the **manifesto** — the agent's per-role×domain diagnostic table (observable symptom →
exact `wiki-query`), scoped by stack facts, with a normative `## File Ownership` glob list — at the
canonical path `.claude/manifests/{role}-{domain}.md`. This is the producer that `momentum:build-guidelines`
Phase 1 (Discover) expects to find on disk and that `momentum:agent-builder` composes into a runnable
agent. Before this skill existed, nothing authored these files — build-guidelines could discover but
never receive one.

## Two Committed Design Stances

This skill's shape is not incidental — it resolves two open questions from DEC-038, recorded here so a
future reader sees why the skill exists and how it decides:

1. **Standalone producer, not folded into `agent-builder`.** `momentum:manifesto-builder` is its own
   skill. `build-guidelines/workflow.md` is discover-only — it scans `.claude/manifests/` and invokes
   `agent-builder` to compose, but never authors a manifesto itself. This skill runs **before**
   build-guidelines in the composition sequence: `manifesto-builder` (author) → `build-guidelines`
   (discover + compose) → sprint-dev/conduct (spawn composed agents). It is developer-invoked — the
   curate step is inherently interactive — never called by build-guidelines.

2. **Generate-THEN-curate (DEC-038 Gate G2), not hand-authored, not silently auto-finalized.** The
   skill auto-**drafts** symptom→`wiki-query` entries by reusing `constitution-builder`'s Phase 3
   KB-lookup method, then routes the draft to the developer to **curate** the symptom phrasing (and the
   File Ownership globs) before anything is written. Rationale (DEC-038 D1): the recovered `cmp-dev`
   prototype proved that specific, observable, diagnostic symptom phrasing is the expensive,
   human-designed part of a manifesto — generation seeds it, curation perfects it. The skill never
   treats a fresh draft as finished.

**Output authority:** `skills/momentum/references/manifesto-format.md` (v1.0) — every section, field, and
normative rule this skill produces traces to that document. Read it before drafting.
**Decision authority:** DEC-038 (`_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`),
Gates G1 and G2.

## What This Skill Is Not

- Not a per-sprint or per-story generator — the manifesto is stable across every sprint (DEC-038 D1).
  Never inject a sprint slug, story slug, or "overlay" language into the output.
- Not the composer — it does not merge a base body, does not write `momentum/agents.json`, and does
  not produce the runnable composed agent file. That is `momentum:agent-builder`, orchestrated by
  `momentum:build-guidelines`.
- Not a copy of the reference exemplar (`docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md`). The
  exemplar predates the `## File Ownership` field and is a diagnostic-table *shape* reference only —
  never a Momentum agent, never a source to lift File Ownership globs from.

## Inputs

| Input | Required | Notes |
|---|---|---|
| `role` | yes | Agent role: `dev`, `qa`, `e2e`, `architect`, `pm`, or a future role. Elicited if not supplied. |
| `domain` | yes | Technology domain, e.g. `kotlin-compose`. Elicited if not supplied. |
| `project_kb` | yes | The project KB `wiki-query` resolves against. Derived from `~/.obsidian-wiki/config` when unambiguous; elicited otherwise. |

## Output

`.claude/manifests/{role}-{domain}.md` — conformant to `manifesto-format.md`'s Manifesto File Template:
identity block → `## Project Stack` → `## File Ownership` → `## Diagnostic Table`.

Load and follow `./workflow.md` — it is the binding execution protocol; the mandatory curate gate
lives there and must not be skipped.
