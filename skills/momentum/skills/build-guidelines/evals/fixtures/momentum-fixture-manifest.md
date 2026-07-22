---
role: dev
domain: kb-fixture
project_kb: momentum-agentic-kb
---

# dev-kb-fixture — Minimal fixture manifest for multi-KB resolver proof

**Test artifact only — not a real Momentum agent.** Created for the
`momentum-knowledge-base-buildout` story (Task 4) to prove the end-to-end resolver round-trip
(AC7) because no real Momentum agent manifesto exists in `.claude/manifests/` as of 2026-07-13.
Real Momentum manifestos are authored by the sibling story
`manifesto-builder-skill-generate-then-curate`; this fixture is not one of them and must not be
treated as a template for authoring real manifestos beyond its format conformance.

---

## Project Stack

Momentum practice-layer fixture — no application stack. Used only to exercise the multi-KB
`wiki-query` resolver against the seeded Momentum KB.

- **Purpose:** resolver round-trip proof only.
- **KB:** `momentum-agentic-kb` (see `~/projects/momentum-agentic-kb/`)

Tech: **n/a (fixture)**

---

## File Ownership

file_ownership:
  - "skills/momentum/skills/build-guidelines/evals/fixtures/**"

---

## Diagnostic Table

### Momentum Agent Architecture

- **Need to recall which tier owns the manifesto vs. the composed agent file vs. the cold KB** → `wiki-query Momentum three-tier agent architecture manifesto diagnostic table`
