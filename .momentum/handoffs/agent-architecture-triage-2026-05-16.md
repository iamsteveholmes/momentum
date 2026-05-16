# Handoff: Agent Architecture Triage — 2026-05-16

## Context

A full agent architecture redesign was completed in session 2026-05-16. Eight decision documents were written (DEC-020 through DEC-027, committed beb2416). These decisions obsolete several existing backlog stories, change the scope of others, and surface new work that needs to enter the backlog. This handoff is for a `momentum:triage` pass to process that delta.

**Do not re-litigate the decisions. They are adopted and committed. Triage only.**

---

## The Architecture in Brief (context for triage decisions)

**Nine universal base bodies** ship in the plugin: `architect`, `pm`, `ux`, `analyst`, `researcher`, `dev`, `sm`, `qa`, `e2e`. Aligned with BMAD role names; interaction model is orchestrator-spawned subagent, not interactive.

**Document ownership** is explicit: architect owns `architecture.md`; pm owns `prd.md`, `epics.md`, `features.json`; ux owns design/UX docs; analyst owns assessments and analysis; researcher owns research docs; dev owns code (project-defined variants via routing table).

**`momentum/` directory** replaces `_bmad-output/planning-artifacts/` for pipeline knowledge artifacts. Subfolders: `research/`, `analysis/`, `decisions/`, `ux/`, `architecture/`, `pm/`, `sprints/`. `.momentum/` stays operational state.

**`momentum/agents.json` routing table** is machine-readable. Maps file patterns → agent slug + agent path + write_permissions. Defaults (plugin base bodies) + project entries (written by build-agents). Every skill resolves 1..N agents from this table based on relevant files — not hardcoded agent names.

**Read-only = skill constraint, not a role.** `code-review` skill invokes `dev` with `context:fork + allowed-tools: Read`. `architecture-guard` skill invokes `architect` same way. No separate base body files for read-only variants.

**Fixer = document owner + fix constraint.** AVFL findings carry file-path metadata. Fix spawn resolves routing table → owner agent + fix-constraint prompt injected by orchestrator. No `dev-fixer` base body.

**Build pipeline:** `agent-guidelines` retired. `build-guidelines` → `build-agents` (orchestrator). New `agent-builder` skill (per-agent composer: base_body + manifesto → composed file + routing entry). `constitution-builder` reworked: domain knowledge only (routing moves to agent-builder).

**change_type routing in sprint-dev:** `skill`/`agent` stories → skill-building subagent → skill-creator autonomous mode + approval gate. `feature`/`bug` → normal path. `rule`/`hook` → direct edit + commit. `dev-skills` agent retired.

Full details: DEC-020 through DEC-027 in `_bmad-output/planning-artifacts/decisions/`.

---

## Triage Items

### CLOSE — Stories no longer needed

These stories describe work that is either superseded by the new architecture or explicitly eliminated by a decision. Triage action: mark as `rejected` or `superseded`, add a note citing the relevant DEC.

| Story slug | Reason | Decision |
|---|---|---|
| `code-reviewer-agent-definition` | Not a base body — skill-applied constraint | DEC-020 D2, DEC-024 |
| `architect-guard-agent-definition` | Not a base body — skill-applied constraint | DEC-020 D2, DEC-024 |
| `documenter-agent-definition` | Retro synthesizer is an inline spawn, not a typed role | DEC-020 D3 |
| `dev-fixer-agent-definition` | Fixer is a constraint pattern, not a base body | DEC-020 D4, DEC-025 |
| `agents-md-manifest-format` | Replaced by `momentum/agents.json` routing table | DEC-023 |
| `build-guidelines-skill` | Superseded: renamed to build-agents, scope redesigned | DEC-026 D2 |

---

### CREATE — New stories needed

These stories represent work surfaced by the new architecture that has no existing story. Triage action: promote each to a backlog story stub, assign to the appropriate feature, then run `momentum:create-story` to enrich.

**Feature: `momentum-agent-role-contracts`**

| Story slug (proposed) | What it covers |
|---|---|
| `ux-base-body` | Create `agents/ux.md` base body — owns UX specs, design docs, wireframes |
| `analyst-base-body` | Create `agents/analyst.md` base body — owns assessment records, analysis docs |
| `researcher-base-body` | Create `agents/researcher.md` base body — owns research docs, synthesis briefings |

**Feature: `momentum-agent-composition-pipeline`**

| Story slug (proposed) | What it covers |
|---|---|
| `agent-builder-skill` | New skill: per-agent composer (base_body + manifesto + permissions → composed agent file + routing table entry). Wraps skill-creator with agent-specific template. |
| `routing-table-schema-and-implementation` | Define and implement `momentum/agents.json` schema — defaults block, project entries with patterns and write_permissions, resolution algorithm |
| `specialist-classify-multi-result` | Rework `momentum-tools specialist-classify` to return array of `{slug, agent_path, file_scope}` instead of single string |
| `momentum-directory-migration` | Migrate `_bmad-output/planning-artifacts/` to `momentum/` — all subfolders, update all skill references |

**Feature: `momentum-sprint-orchestration`**

| Story slug (proposed) | What it covers |
|---|---|
| `change-type-routing-in-sprint-dev` | Sprint-dev Phase 2 reads `change_type`; routes skill/agent to skill-building subagent, rule/hook to direct edit, docs to writer agent |
| `skill-agent-story-spec-mig-template` | Add MIG injection for `change_type: skill` and `change_type: agent` in `create-story` — distills constitution context into spec so skill-creator is pre-briefed |

---

### UPDATE — Stories with changed scope

These stories already exist but their scope or acceptance criteria are now incorrect. Triage action: update story file to reflect new scope, do not start dev until updated.

| Story slug | What changed | Decision |
|---|---|---|
| `constitution-builder-write-mode-parameterization` | ACs currently assume constitution generates Permissions + Standing Rules + Quick Routing. New scope: domain knowledge only. Routing moves to agent-builder. | DEC-026 D4 |
| `build-guidelines-invocation-surface-in-sprint-planning` | References `build-guidelines` — rename to `build-agents` throughout | DEC-026 D2 |
| `sprint-dev-composed-file-spawn-wiring` | Must implement routing-table-driven resolution (not hardcoded agent paths) and handle `change_type` routing | DEC-023, DEC-027 D3 |
| `sprint-planning-composed-file-preference-update` | References `build-guidelines` — update to `build-agents` | DEC-026 D2 |
| `nornspun-agent-constitution` | Constitution scope narrows to domain knowledge only; wiki-query block and routing stay, but routing is now agent-builder's concern | DEC-026 D4 |

---

## Feature Membership Notes

After triage, update `features.json` entries:
- `momentum-agent-role-contracts`: add ux-base-body, analyst-base-body, researcher-base-body; remove the 4 closed stories
- `momentum-agent-composition-pipeline`: add agent-builder-skill, routing-table-schema-and-implementation, specialist-classify-multi-result, momentum-directory-migration; remove build-guidelines-skill; update build-guidelines-invocation story slug reference
- `momentum-sprint-orchestration`: add change-type-routing-in-sprint-dev, skill-agent-story-spec-mig-template

---

## What to Run

```
/momentum:triage
```

Feed this handoff as the source. Classify each item above as ARTIFACT (new story stub → intake) or DISTILL (scope update → apply to existing story file). The CLOSE items are DECISION-class — record the rejection with the DEC citation.
