---
name: build-guidelines
description: "Builds gen-2 composed specialist agent files (base body + manifesto) and Tier 1 constitution. Run before sprint to bake guidelines in."
model: claude-sonnet-4-6
effort: medium
---

# momentum:build-guidelines

Orchestrates the three-tier agent guidelines architecture for a project. Produces:

- **Tier 1 (Hot Constitution):** `.claude/guidelines/constitution.md` — project-wide, always loaded.
- **Tier 2 (Composed Agent Files):** `.claude/guidelines/agents/{role}-{domain}.md` — base body + manifesto merged per role × domain pair.

This skill is an **orchestrator over `momentum:agent-builder`** (Tier 2 composer) and optionally `momentum:constitution-builder` (domain-knowledge synthesis). It contains no KB-synthesis logic of its own. It loops the agent manifesto's role × domain matrix, invokes `agent-builder` for each pair (which assembles the full composed file AND writes `momentum/agents.json` with non-empty `patterns[]`), and validates that the resulting agents are resolvable via `momentum-tools agent resolve --touches`.

**DEC-038 G1 gate:** At least one composed agent file must be written to disk AND registered in `momentum/agents.json`. This is the key observable.

**The manifesto is sprint-invariant.** The skill reads per-role×domain diagnostic tables as stable, standing input. It does NOT read, build, or write any per-sprint/per-story context overlay. No sprint or story identifier flows into any composed output.

See `workflow.md` for the full six-phase execution spine.
See `references/orchestration-guide.md` for the composition formula, multi-KB contract, and exemplar-shape reference.

## Dependency Check

Before invoking this skill, verify:

```
constitution-builder write_mode parameter available:
  momentum:constitution-builder supports composed_agent_file and standalone_constitution write modes
  (dependency: constitution-builder-write-mode-parameterization story)
```

If `constitution-builder` does not support these write modes, HALT with:

> "build-guidelines requires constitution-builder with composed_agent_file / standalone_constitution write modes (story: constitution-builder-write-mode-parameterization). Please complete that dependency first."

## Inputs

This skill accepts optional invocation arguments:

| Argument | Description | Default |
|---|---|---|
| `manifests_dir` | Directory containing manifesto files | `.claude/manifests/` |
| `output_dir` | Directory for composed agent files | `.claude/guidelines/agents/` |
| `constitution_path` | Path for Tier 1 constitution output | `.claude/guidelines/constitution.md` |
| `dry_run` | If true, preview plan but do not write files | `false` |

If arguments are absent, the skill uses defaults and elicits project context interactively.

## Output

After a successful run, the skill produces:

```
Build-Guidelines Run Complete
─────────────────────────────────
Tier 1 constitution: .claude/guidelines/constitution.md
Composed agents:
  ✓ dev-kotlin-compose  → .claude/guidelines/agents/dev-kotlin-compose.md
  ✓ qa-kotlin-compose   → .claude/guidelines/agents/qa-kotlin-compose.md
  ...

agents.json: momentum/agents.json updated — N project[] entries

G1 Gate: PASSED (≥1 composed agent on disk + registered)
```

If G1 is not met (no composed agent written + registered), the skill emits a clear failure:

```
G1 Gate: FAILED
  No composed agent file was written AND registered in momentum/agents.json.
  Check: manifests_dir contains ≥1 conformant manifesto, constitution-builder write modes available.
```
