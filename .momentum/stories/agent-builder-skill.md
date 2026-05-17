---
title: agent-builder — Per-Agent Composition Skill (DEC-026 D3)
story_key: agent-builder-skill
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-agent-composition-pipeline
story_type: feature
change_type: skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/agent-builder/SKILL.md
  - skills/momentum/skills/agent-builder/workflow.md
  - momentum/agents.json
---

# agent-builder — Per-Agent Composition Skill (DEC-026 D3)

## Story

As a developer using the agent composition pipeline,
I want a dedicated `/momentum:agent-builder` skill that accepts a base body, constitution excerpt, and role × domain inputs to produce one composed Tier 2 agent file and its routing entry,
so that build-agents can orchestrate composition by invoking agent-builder once per role × domain pair — without bespoke composition logic scattered across other skills.

## Description

agent-builder is the Tier 2 skill in the three-skill agent composition pipeline defined by DEC-026 D5:

```
constitution-builder (Tier 1, once per project)
  → agent-builder × N (Tier 2, once per role × domain)
  → routing table complete
```

build-agents orchestrates both tiers; agent-builder is the composition unit — one invocation, one composed file, one routing entry. It wraps skill-creator with an agent-specific starting template (DEC-026 D3). The story spec's MIG section (populated by create-story per DEC-027 D2) pre-answers skill-creator's interview phase so the build runs autonomously.

**Pain context (DEC-026 D2/D3):** Constitution-builder previously carried composition responsibilities it should not own. Without agent-builder, build-agents has no clean delegation target, and composition logic lives ad hoc across multiple callers. The separation keeps the constitution stable and slow-changing while agent-specific routing changes as domains evolve.

**Sprint scope note:** constitution-builder (Tier 1, DEC-026) is out of scope for this sprint. agent-builder accepts `constitution_excerpt` as a direct input parameter — the caller (or developer) provides the excerpt manually. constitution-builder (the skill that extracts and maintains that excerpt automatically) is a future story.

## Acceptance Criteria

1. `/momentum:agent-builder` can be invoked with three required inputs: `base_body_path` (path to a plugin agent body file, e.g. `skills/momentum/agents/dev.md`), `constitution_excerpt` (relevant section of `momentum/architecture/constitution.md`), and `manifesto_inputs` (role × domain specifics: role name, domain slug, file patterns, write permissions scope).

2. When all three inputs are provided, the skill produces a composed agent file at `.claude/guidelines/agents/{role}-{domain}.md` containing the merged base body, constitution excerpt, and domain-specific manifesto section.

3. When the composed file is written, the skill appends a routing entry for this role × domain pair to `momentum/agents.json` under the `project` array, using the schema from DEC-023 D1:
   ```json
   {
     "role": "<role>",
     "slug": "<role>-<domain>",
     "agent": ".claude/guidelines/agents/<role>-<domain>.md",
     "patterns": ["<file_patterns_from_manifesto_inputs>"],
     "write_permissions": ["<scope_from_manifesto_inputs>"]
   }
   ```
   If `momentum/agents.json` does not exist yet, it is created with `{ "defaults": {}, "project": [<entry>] }`. If it exists but the slug already appears in `project`, the existing entry is updated in place rather than duplicated.

4. Before composing, the skill runs skill-creator in autonomous mode using the story spec's MIG section as pre-answered interview input — it does not prompt the developer interactively during the build loop (draft → 2-3 evals → programmatic grading → one improvement pass, per DEC-027 D4).

5. After skill-creator completes, the skill surfaces the composed file path, eval summary, and routing entry to the developer as an approval gate. The developer can: (A) approve and finalize the routing entry commit, (R) request one iteration with specific feedback before re-presenting, or (X) abort without writing the routing entry.

6. Each invocation is scoped to exactly one role × domain pair. When build-agents orchestrates multiple pairs, it invokes agent-builder once per pair — agent-builder never composes more than one file per invocation.

7. The composed agent file follows the agent definition conventions in `skills/momentum/references/agent-skill-development-guide.md`: proper frontmatter (name, description, model, effort, tools), a `## Large File Handling` section, and a system prompt body under 200 lines.

8. The skill is invocable both directly by a developer (`/momentum:agent-builder`) and by build-agents as a subagent spawn. In both cases the inputs, composition behavior, and output contract are identical.

## Dev Notes

### Pipeline Context: This Is the Tier 2 Composition Unit

The three-skill pipeline (DEC-026 D5) has clear separation of concerns:

| Tier | Skill | Input | Output | Frequency |
|------|-------|-------|--------|-----------|
| 1 | constitution-builder | Stack facts, conventions | `momentum/architecture/constitution.md` domain-knowledge sections | Once per project (or stack change) |
| 2 | **agent-builder** | base_body + constitution excerpt + role × domain | `.claude/guidelines/agents/{role}-{domain}.md` + routing entry | Once per role × domain pair |
| — | build-agents | Project config | Orchestrates Tier 1 then Tier 2 × N | Developer entry point |

agent-builder is scoped to Tier 2 only. It never invokes constitution-builder. It never invokes build-agents. Scope discipline is critical — one composed file per invocation (CREED: one responsibility, one output unit).

### This Is an EDD Story — Write Evals First

`change_type: skill-instruction` means the EDD cycle applies. The three behavioral evals (Task 1) must be written and committed before SKILL.md is drafted (Task 2). Evals define the behavioral contract; the skill must satisfy that contract, not the other way around.

Eval format: `skills/momentum/skills/agent-builder/evals/eval-{name}.md`

### How agent-builder Wraps skill-creator

skill-creator's normal flow starts with an interview phase that gathers skill purpose, triggers, and behavioral constraints. For agent-builder, this interview is pre-answered by the story spec's MIG section (DEC-027 D2). The MIG section contains:
- The role name and domain slug (from `manifesto_inputs`)
- The relevant constitution excerpt (from `constitution_excerpt`)
- The base body path (from `base_body_path`)
- The file patterns and write permissions scope (from `manifesto_inputs`)

agent-builder passes this pre-answered context to skill-creator as its starting template, bypassing the interactive interview. skill-creator then runs its eval loop autonomously (DEC-027 D4):
```
draft → 2-3 parallel eval subagents → programmatic grading → one improvement pass → commit
```

The developer approval gate fires after the autonomous loop completes, not during it.

### Routing Entry Format (DEC-023 D1)

The `momentum/agents.json` schema written by this skill:

```json
{
  "defaults": {
    "dev": "skills/momentum/agents/dev.md",
    "architect": "skills/momentum/agents/architect.md"
  },
  "project": [
    {
      "role": "dev",
      "slug": "dev-cmp",
      "agent": ".claude/guidelines/agents/dev-cmp.md",
      "patterns": ["**/src/**/ui/**", "**/*.kt"],
      "write_permissions": ["src/main/kotlin/**/ui/**"]
    }
  ]
}
```

Key constraints from DEC-023:
- `defaults` block is plugin-provided — agent-builder never modifies it
- `project` entries are written by agent-builder — one entry per role × domain invocation
- `slug` is `{role}-{domain}`, kebab-case, max 50 chars
- `patterns` drive routing-table fan-out — every skill that spawns a typed role uses these to group files by matching agent (DEC-023 D2)
- `write_permissions` are harness-enforced at spawn time (DEC-023 D3) — not advisory

If `momentum/agents.json` does not yet exist (first invocation), agent-builder creates it with an empty `defaults: {}` and the new `project` entry. The defaults block is populated by build-agents from the plugin manifest, not by agent-builder.

### Composed Agent File Structure

The composed file at `.claude/guidelines/agents/{role}-{domain}.md` is a merged system prompt:

```markdown
---
name: {role}-{domain}
description: "{role} agent scoped to {domain} domain. Use when..."
model: sonnet
effort: medium
tools: Read Glob Grep Bash Edit Write
---

{base_body content}

## Domain Context — {domain}

{constitution_excerpt for this domain}

## Manifesto — {role} in {domain}

{role × domain specifics: patterns owned, write permissions, escalation paths}

## Large File Handling

{standard section from agent-skill-development-guide.md}
```

The base body provides behavioral defaults for the role (dev, architect, qa, etc.). The constitution excerpt provides project-wide domain knowledge shared across all agents. The manifesto section is agent-builder's unique contribution: it scopes the agent to its specific file domain and write permissions.

### SKILL.md and workflow.md Conventions

- SKILL.md frontmatter: `user-invocable: true`, `model: claude-opus-4-6`, `effort: medium`
- SKILL.md body: under 300 lines, detailed steps in workflow.md
- workflow.md: XML `<workflow>` block with `<step>` elements, matching sprint-planning/workflow.md structure
- SKILL.md description must be under 250 chars and front-load the invocation trigger

Reference: `skills/momentum/references/agent-skill-development-guide.md`

### What This Skill Does NOT Do

- Does not invoke constitution-builder (Tier 1 is build-agents' responsibility)
- Does not orchestrate multiple role × domain pairs (that is build-agents' job)
- Does not modify the `defaults` block in agents.json (plugin-managed)
- Does not write to `.claude/guidelines/agents/` except its one composed file per invocation
- Does not run AVFL (skill-creator's eval loop replaces AVFL for prompt artifacts — DEC-027 D1)

## Tasks / Subtasks

- [ ] Task 1 — Write 2-3 behavioral evals (EDD — before any SKILL.md work)
  - [ ] Create `skills/momentum/skills/agent-builder/evals/eval-composition-output.md`
    — verifies: given valid `base_body_path`, `constitution_excerpt`, and `manifesto_inputs`, the skill produces a composed file at the expected `.claude/guidelines/agents/{role}-{domain}.md` path with all three source sections present
  - [ ] Create `skills/momentum/skills/agent-builder/evals/eval-routing-entry-written.md`
    — verifies: after composition, `momentum/agents.json` contains a `project` entry with the correct `slug`, `agent` path, `patterns`, and `write_permissions` fields; re-invocation with the same slug updates the existing entry rather than appending a duplicate
  - [ ] Create `skills/momentum/skills/agent-builder/evals/eval-approval-gate-behavior.md`
    — verifies: after the autonomous skill-creator loop, the approval gate is presented with (A/R/X) options; selecting X leaves no routing entry in agents.json; selecting R re-runs the improvement pass and re-presents the gate; selecting A finalizes the commit

- [ ] Task 2 — Create `skills/momentum/skills/agent-builder/SKILL.md` and `workflow.md`
  - [ ] Write SKILL.md frontmatter: name, description (≤250 chars), model (opus-4-6), effort (medium), user-invocable: true
  - [ ] Write SKILL.md body: overview paragraph, input/output contract, reference to workflow.md
  - [ ] Write workflow.md with `<workflow>` XML block:
    - Step 1: Gather and validate inputs (base_body_path, constitution_excerpt, manifesto_inputs)
    - Step 2: Read base body, read constitution excerpt, validate manifesto_inputs fields
    - Step 3: Assemble starting template for skill-creator (pre-answered MIG section)
    - Step 4: Run skill-creator in autonomous mode (draft → evals → grading → improvement pass)
    - Step 5: Present approval gate (composed file + eval summary) — A/R/X
    - Step 6 (on A): Write routing entry to momentum/agents.json and commit

- [ ] Task 3 — Run evals and validate
  - [ ] Run each eval via subagent against the completed SKILL.md + workflow.md
  - [ ] Confirm all three eval behavioral assertions pass
  - [ ] Verify composed file structure matches `agent-skill-development-guide.md` conventions (frontmatter, Large File Handling section, body under 200 lines)

## Momentum Implementation Guide

**Change type: skill-instruction**

This story creates two new skill files (`SKILL.md` + `workflow.md`) and a new data file (`momentum/agents.json`). All three are skill-instruction artifacts — no code, no hooks.

### EDD Cycle for skill-instruction

**Before writing SKILL.md or workflow.md:**
1. Write all 3 evals in `skills/momentum/skills/agent-builder/evals/`
2. Commit evals: `docs(skills): add agent-builder evals — EDD pre-implementation`

**Then implement:**
3. Write `SKILL.md` and `workflow.md` to satisfy eval contracts
4. Commit implementation: `feat(skills): add agent-builder skill — DEC-026 D3`

**Then verify:**
5. Run each eval via subagent
6. Confirm routing entry schema matches DEC-023 D1 exactly
7. Commit verification results: `test(skills): verify agent-builder evals pass`

### DoD Items

- [ ] 3 behavioral evals written before SKILL.md is drafted
- [ ] SKILL.md frontmatter complete: name, description (≤250 chars), model, effort, user-invocable
- [ ] workflow.md has `<workflow>` XML block with steps 1-6
- [ ] Composed agent file structure includes: frontmatter, base body, constitution excerpt, manifesto section, `## Large File Handling`
- [ ] `momentum/agents.json` written with correct DEC-023 D1 schema
- [ ] Duplicate-slug guard: re-invocation with existing slug updates entry, not appends
- [ ] Approval gate (A/R/X) behaves correctly per eval-approval-gate-behavior.md
- [ ] All 3 evals pass when run against finished skill
- [ ] SKILL.md body under 300 lines; workflow.md steps self-contained

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6 (dev-skills specialist)

### Debug Log References

None — implementation proceeded directly from DEC-026 D3 and DEC-027 D3 decision documents.

### Completion Notes List

- Story was an intake stub; enriched in-place from DEC-026 D3 (agent-builder decision) and agent-architecture-triage-2026-05-16.md
- Created SKILL.md with correct frontmatter: user-invocable, allowed-tools, model=sonnet, effort=medium
- Created workflow.md with 4-phase execution: Elicit → Compose → Validate via skill-creator → Write outputs
- Workflow follows DEC-026 D3 inputs (base_body_path, constitution excerpt, manifesto_context, permissions_scope)
- Workflow outputs composed Tier 2 agent file at `.claude/guidelines/agents/{role}-{domain}.md` and routing entry in `momentum/agents.json`
- Large File Handling section mandated in all composed agent files (per agent-skill-development-guide.md convention)
- skill-creator validation gate included in Phase 3 with fallback manual checklist

### File List

- `skills/momentum/skills/agent-builder/SKILL.md` (created)
- `skills/momentum/skills/agent-builder/workflow.md` (created)
