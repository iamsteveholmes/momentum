---
content_origin: claude-code-subagent
date: 2026-05-04
sub_question: "Does the momentum skill ecosystem have a skill or established pattern that generates or maintains symptom→reference routing tables?"
topic: "Symptom-based routing tables for agent knowledge retrieval"
---

## Summary Finding

The momentum skill ecosystem does **not** have a skill that generates or maintains symptom→reference routing tables. The pattern exists in the wild (compose-expert's `## Quick Routing` section is a working example), and a future generation of the agent-guidelines system (`build-guidelines`) is designed but not yet implemented. Currently, routing tables are hand-authored per skill, with no generator tooling in place.

---

## What Was Searched

All files under `/Users/steve/projects/momentum/skills/momentum/` were searched for "routing", "symptom", "decision tree", "constitution", "hot layer", "hot-layer", "Quick Routing", "routing table", "→.*\.md", and "maps to". The agent-guidelines skill, its sub-skills, and all references were read in full. The build-guidelines story was read in full. The compose-expert SKILL.md (an installed plugin, not a momentum skill) was read for pattern comparison.

---

## agent-guidelines Skill (Gen-1) — What It Does

**[OFFICIAL]** The `agent-guidelines` skill exists at `skills/momentum/skills/agent-guidelines/SKILL.md` and is an implemented, working skill. Its workflow (`workflow.md`) is a 5-phase pipeline:

1. Discover — spawns 4 parallel sub-skills: `build-scanner`, `rules-auditor`, `test-config-scanner`, `source-pattern-scanner`
2. Research — web-searches for breaking changes per detected technology
3. Consult — interactive developer approval loop
4. Generate — produces path-scoped `.claude/rules/*.md` files (Layer 1) and `docs/references/*.md` files (Layer 2)
5. Validate — AVFL checkpoint

**[OFFICIAL]** The generated artifacts are path-scoped rules files (30–80 lines, ordered: version pins → prohibitions → conventions → setup) and reference docs (100–300 lines, worked code examples). The detection-heuristics reference maps build files and dependency patterns to technology stack components — this is a build-signal→technology mapping, not a symptom→reference routing table.

**[OFFICIAL]** The generated CLAUDE.md update pattern is a pointer section:
```
## Technology References
When working with [technology], read `docs/references/{technology}-patterns.md` for current patterns.
```
This is a coarse "load this doc for this technology" pointer, not a symptom-grained routing table.

**Conclusion:** agent-guidelines generates technology-scoped rule files and reference docs. It does not generate symptom→reference routing tables inside those SKILL.md files, and it has no sub-skill dedicated to routing table creation. **[OFFICIAL]**

---

## build-guidelines Skill (Gen-2) — Designed But Not Implemented

**[OFFICIAL]** The story file at `.momentum/stories/build-guidelines-skill.md` describes a gen-2 replacement for agent-guidelines. Key architectural concepts:

- **Tier 1 (Hot constitution):** `.claude/guidelines/constitution.md` — ~660 lines, always loaded
- **Tier 2 (Composed specialist agent files):** `.claude/guidelines/agents/{role}-{domain}.md` — base agent body + project manifest merged

The constitution concept is the closest analogue to a "hot layer" in momentum's vocabulary. However, `build-guidelines` is a **backlog story with status: `backlog`** — the skill does not exist in `skills/momentum/skills/`. The file `skills/momentum/skills/build-guidelines/` does not exist. **[OFFICIAL]**

**[OFFICIAL]** The story references a `constitution.md` that would contain "trigger tables, critical rules, pointers to Tier 3." This is the closest planned artifact to a symptom→reference routing table — a section of the constitution with trigger conditions mapping to reference docs. But this is a planned design, not a current implementation.

---

## The compose-expert Pattern (External Reference)

**[OFFICIAL]** The installed `compose-expert` plugin (`~/.claude/plugins/cache/aldefy-compose-skill/compose-expert/2.3.1/skills/compose-expert/SKILL.md`) uses an explicit `## Quick Routing` section — a hand-authored table mapping user-signal symptoms (API names, error descriptions, casual phrases) to specific `references/*.md` files:

```
- **`remember`, `rememberSaveable`, `mutableStateOf` vs `mutableIntStateOf`, state hoisting** → `references/state-management.md`
- **`LaunchedEffect`, `SideEffect`, `DisposableEffect`** → `references/side-effects.md`
```

This is the exact pattern described in the research question. **[OFFICIAL]** It is hand-authored inside the SKILL.md file. There is no generator that produced it — the compose-expert maintainer wrote it manually. Momentum has no tool that reads a knowledge index and emits a routing table like this.

---

## No Generator Tooling Exists

**[OFFICIAL]** Grepping the entire momentum skills tree for "Quick Routing", "routing table", "symptom", and "→.*SKILL" returns zero hits within momentum's own skill files. The only hit for "routing" in a SKILL.md context is the `eval-no-routing-narration.md` eval (which tests that Impetus doesn't narrate routing decisions aloud — a UX rule, not a routing table).

**[PRAC]** The agent-guidelines workflow's `references/rule-template.md` and `references/reference-doc-template.md` define structure for rules and reference docs respectively, but neither template includes a routing table section. There is no template for generating a SKILL.md with a Quick Routing section.

**[PRAC]** The planned `build-guidelines` constitution concept (Tier 1 "trigger tables") would partially fill this gap — but only as a generated file that the agent loads, not as an inlined routing section inside a SKILL.md. The architecture is different from compose-expert's approach.

---

## Conclusion

No skill or established pattern in the momentum ecosystem generates or maintains symptom→reference routing tables. The compose-expert plugin demonstrates the pattern works well in practice, but it is hand-authored. The planned `build-guidelines` skill (backlog, not implemented) will generate a "constitution" with trigger tables — adjacent but architecturally distinct (a loaded document rather than an inlined SKILL.md section). For a new compose+kotest skill, the routing table must be hand-authored, following compose-expert's `## Quick Routing` convention as the only existing reference implementation.

---

## Sources

| Path | Role |
|---|---|
| `skills/momentum/skills/agent-guidelines/SKILL.md` | Gen-1 agent-guidelines skill definition |
| `skills/momentum/skills/agent-guidelines/workflow.md` | Full workflow — all 5 phases |
| `skills/momentum/skills/agent-guidelines/references/detection-heuristics.md` | Build-signal→technology mapping table |
| `skills/momentum/skills/agent-guidelines/references/rule-template.md` | Layer 1 rules file template |
| `skills/momentum/skills/agent-guidelines/references/reference-doc-template.md` | Layer 2 reference doc template |
| `skills/momentum/skills/agent-guidelines/sub-skills/source-pattern-scanner/SKILL.md` | Source-code pattern analysis sub-skill |
| `.momentum/stories/build-guidelines-skill.md` | Gen-2 design story (backlog) |
| `~/.claude/plugins/cache/aldefy-compose-skill/compose-expert/2.3.1/skills/compose-expert/SKILL.md` | compose-expert Quick Routing pattern (external reference) |
| `skills/momentum/skills/impetus/SKILL.md` | Impetus routing (checked for table patterns — none found) |
| `skills/momentum/skills/impetus/evals/eval-no-routing-narration.md` | Routing narration eval (UX rule, not routing table) |
