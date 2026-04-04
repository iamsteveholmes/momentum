# Spec Capture Guide for momentum:plan-audit

Reference loaded in Steps 2–3 of the workflow to guide classification, story creation, and spec audit.

---

## 1. Trivial vs. Substantive Classification

| Signal in plan | Classification |
|---|---|
| ONLY read operations: Read, Glob, Grep, WebSearch, WebFetch, git log/diff/status queries | **trivial** |
| Creates or modifies any file (Write, Edit, Bash that touches files) | **substantive** |
| Introduces a new skill, agent, rule, or hook | **substantive** |
| Makes an architectural decision (new pattern, new convention, ADR-worthy) | **substantive** |
| Changes behavior of existing system | **substantive** |
| Adds a new capability to the Momentum module | **substantive** |

**When in doubt: classify as substantive.** The cost of a missed capture is higher than the cost of a spurious process story.

---

## 2. Process Story Convention

### ID Format

```
p{sprint_num}.{n}
```

- `sprint_num`: current sprint number (integer, e.g., 1, 2, 3)
- `n`: next available sequence number within that sprint (e.g., if p1.1 and p1.2 exist, use p1.3)
- Example: `p1.1`, `p1.2`, `p2.1`

### Epic Naming

```
P{sprint_num} — Process Sprint-{sprint_num}
```

- Example: `P1 — Process Sprint-1`, `P2 — Process Sprint-2`

---

## 3. Process Story Frontmatter Schema

```yaml
---
story_id: p{sprint}.{n}
status: ready-for-dev
type: process
epic: P{sprint} — Process Sprint-{sprint}
title: {plan title from first H1}
sprint: {sprint_num}
touches:
  - {paths from plan's Files to Create/Modify table}
depends_on: []
---
```

**Required fields:** `story_id`, `status`, `type`, `epic`, `title`, `sprint`, `touches`, `depends_on`

**Note:** Process stories do not include a `story_file` pointer (they are self-contained, unlike product stories which point to a separate full story file).

---

## 4. Sprint Number Resolution

Determine `sprint_num` in this order:

1. Check `_bmad/bmm/sprint-status.yaml` if it exists — read `current_sprint`
2. Check `_bmad-output/planning-artifacts/epics.md` — find the sprint marked as active or "Sprint N" in the sprint planning section
3. Default to `1` if no sprint assignment is found

---

## 5. Process Story Body Composition

### User Story (from plan Context)

Transform the plan's Context section into a user story:

```
As a Momentum developer,
I want {goal extracted from Context},
So that {rationale extracted from Context}.
```

### Background

Copy the plan's Context section verbatim (or summarize if > 300 words).

### Acceptance Criteria

Derive from the plan's **Verification** section as Given/When/Then:

```
Given {precondition from verification item},
When {trigger},
Then {observable result}.
```

If no Verification section: derive ACs from the plan's execution steps (each step = one AC).

### Definition of Done

Use the plan's Files to Create/Modify table as DoD items:
```
- [ ] {path} — {brief description of what it should contain/do}
```

### Dev Notes

**Change type:** {classify each file group using these signals (from `skills/momentum/skills/create-story/references/change-types.md`):
- `SKILL.md`, `workflow.md`, `references/`, instruction files → `skill-instruction`
- `.sh`, `.py`, `.ts`, `scripts/`, executables → `script-code`
- `.claude/rules/`, `settings.json`, hooks config → `rule-hook`
- JSON config, version files, directory structure → `config-structure`
- `docs/`, `_bmad-output/`, PRD, architecture, research, README → `specification`
}

---

## 6. ADR Amendment Signals

Recommend an architecture.md update when the plan introduces any of:

| Signal | Where to update in architecture.md |
|---|---|
| New hook type or new hook target tool | Hook Infrastructure section |
| New skill pattern or skill lifecycle mechanism | Skills Architecture section |
| New deployment mechanism | Skills Deployment Classification Table |
| New inter-skill dependency pattern | Agent/Skill Composition section |
| New story type (e.g., process stories) | Sprint/Story Management section |
| Change to FR coverage (new functional requirement satisfied) | FR Coverage Map |

---

## 7. Upstream Spec Update Signals

| Plan content | Spec file to update |
|---|---|
| New hook (any type) | architecture.md — Hook Infrastructure |
| New skill category or skill lifecycle change | architecture.md — Skills Architecture |
| New FR satisfied or changed | epics.md — FR Coverage Map |
| New epic or story type | epics.md — Epic list |
| New capability affecting end-user experience | prd.md — relevant feature section |
| New deployment/installation behavior | architecture.md — Deployment section |

**Scope discipline:** Update only the sections that directly apply. Do not rewrite full spec files for a targeted change.

---

## 8. Targeted Spec Section Reading

When auditing specs, read ONLY the sections relevant to the plan's changes:

1. Identify keywords from the plan's Files to Create/Modify table: hook types, skill names, config paths
2. Grep for those keywords in architecture.md and epics.md to find relevant sections
3. Read those sections (not full files)
4. Skip any spec file that has no section touched by the plan

**Example:** Plan adds a PreToolUse hook → read only "Hook Infrastructure" from architecture.md. Skip prd.md entirely if the plan has no user-facing behavioral changes.
