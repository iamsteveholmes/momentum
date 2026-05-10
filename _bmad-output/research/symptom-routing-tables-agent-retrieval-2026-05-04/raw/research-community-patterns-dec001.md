---
content_origin: claude-code-subagent
date: 2026-05-04
sub_question: "Is there a known community pattern, meta-skill, or tool for generating symptom→reference routing tables from a knowledge index? What does DEC-001 prescribe about hot constitution trigger tables?"
topic: "Symptom-based routing tables for agent knowledge retrieval"
---

# Community Patterns and DEC-001 Prescriptions for Symptom→Reference Routing Tables

## What DEC-001 Prescribes About Trigger Tables

DEC-001 (`_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md`) establishes the three-tier architecture and **names trigger tables as a Tier 1 (hot constitution) artifact** — not a Tier 2 or Tier 3 concern. Specifically, the constitution (`~660 lines, always in context`) is defined as containing: **"Trigger tables (domain → reference doc pointer)"**, critical cross-cutting rules, and pointers to Tier 3 cold KB for on-demand retrieval. [OFFICIAL]

**What DEC-001 prescribes about authoring trigger tables:**

DEC-001 does not prescribe *how* trigger tables should be authored — it only prescribes *that* they must exist in Tier 1. The authoring method is left to the `build-guidelines` skill (gen-2), which is planned but not yet implemented. The `build-guidelines` workflow (`.momentum/stories/build-guidelines-skill.md`) describes a **Distill phase** where the skill pulls relevant pages from the cold KB vault and synthesizes them into hot constitution entries, implying trigger tables are generated from KB content — not hand-authored — but no generation algorithm is specified yet. [OFFICIAL]

**DEC-015 and DEC-018 refine the prescription:**

DEC-015 (`dec-015-kb-cold-context-workflow-steps-constitution-audit-2026-05-02.md`) adapts the hot constitution trigger language from permissive to **prescriptive**: rather than "if you need domain knowledge, consult the KB," the constitution must name specific scenarios — "when classifying a story's domain," "when selecting a test pattern for a new library." DEC-015 D3 explicitly rejects vague permission language because "the LLM will always prefer using training data." [OFFICIAL]

DEC-018 (`dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`) further specifies that constitution triggers must name **exact `wiki-query` invocation syntax** for each scenario, not generic KB lookup language. This is Phase 2 of DEC-018's phased implementation. The backlog story `wiki-query-interface-block-for-hot-constitution.md` captures this as a dev-ready requirement — trigger scenarios must be written as **imperatives**, not suggestions. [OFFICIAL]

**Summary of local prescription:** DEC-001 says trigger tables belong in Tier 1 hot context. DEC-015 says they must be prescriptive (named scenarios, not permissions). DEC-018 says they must name exact `wiki-query` syntax per scenario. None of these decisions specify a generation algorithm — the `build-guidelines` skill is the planned generator, but it is backlog, not implemented.

---

## Community Patterns: Symptom→Reference Routing Table Generation

### The SkillRouter Research Direction (arxiv 2603.22455)

The closest published research to symptom→reference routing is **SkillRouter** ([SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale](https://arxiv.org/abs/2603.22455), March 2026). SkillRouter addresses routing *from a task description* to *the correct skill* at inference time using a 1.2B retrieve-and-rerank pipeline achieving 74.0% Hit@1. Its key finding: the **skill body** (full implementation text) is the decisive routing signal — removing it causes 29–44 percentage point degradation. This is a runtime routing system, not a table generation tool. [OFFICIAL]

A related framework, [skill-semantic-router](https://github.com/zhuang-HE/skill-semantic-router), implements multi-layer semantic retrieval for intelligent skill dispatch, again at runtime. Neither SkillRouter nor skill-semantic-router produces a static symptom→reference routing table; they route dynamically. [PRAC]

### Metaskill: Nearest Meta-Skill Analog

**[metaskill](https://github.com/xvirobotics/metaskill)** (xvirobotics) is a meta-skill that generates CLAUDE.md files containing routing tables and orchestration protocols for multi-agent teams. Its BUILD phase produces a routing table as a core artifact. However, it generates *agent-to-role* routing tables (which agent handles which file pattern or task type), not *symptom-to-reference-doc* routing tables for knowledge retrieval. The concept is directly analogous — a meta-skill that generates routing tables — but the routing target differs. [PRAC]

### Skill Authoring Best Practices: Triggers Are Hand-Authored

Anthropic's official [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) and the [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) community guide both treat trigger descriptions as **hand-authored** metadata. The agent Skills progressive disclosure model (L1 metadata → L2 instructions → L3 resources) uses the skill description/trigger as a routing signal, but these are written by the skill author, not generated. SkillReducer research ([arxiv 2603.29919](https://arxiv.org/html/2603.29919v1)) found that 26.4% of publicly available skills lack routing descriptions entirely, confirming that generation is not the norm — human authorship is. [OFFICIAL] [PRAC]

### No Known Tool for Generating Symptom→Reference Tables from a Knowledge Index

Web search across "meta-skill generate routing table knowledge index," "agent skill routing table generation," and community repositories (including [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) with 1,000+ skills and [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) with 232+ skills) found **no tool, skill, or established community pattern** for generating symptom→reference routing tables specifically from a knowledge index. The community treats trigger/routing table authorship as a human-curated task. [UNVERIFIED]

The closest analog in academic literature is [Skill Retrieval Augmentation for Agentic AI](https://arxiv.org/html/2604.24594) (April 2026), which treats retrieval of relevant reference material as a runtime RAG problem — not a table generation problem. Static trigger tables of the type DEC-001 prescribes (baked into the hot constitution before agent invocation) have no published generation tooling as of 2026-05-04. [OFFICIAL]

---

## Synthesis: Implications for the Compose+Kotest Skill

Given the above:

1. **No off-the-shelf tool exists** for generating symptom→reference routing tables from a knowledge index. The `build-guidelines` skill (planned in Momentum) is the intended generator, but it is not yet implemented.
2. **Hand-authoring is the community norm** for trigger/routing table content in SKILL.md files and hot constitutions.
3. **DEC-001 + DEC-015 + DEC-018 together prescribe the format**: prescriptive named scenarios (not permissions), imperative language, exact `wiki-query` invocation syntax per scenario, placed in Tier 1 hot context.
4. **Metaskill** (xvirobotics) is the nearest structural analog — a meta-skill that generates routing tables — but targets agent-to-role routing, not symptom-to-reference routing. Its BUILD-phase pattern (generate a structured routing artifact as output) could be adapted.

For a new compose+kotest skill, the current best path is **hand-authoring the symptom→reference trigger table** following DEC-015's prescriptive scenario format, and tracking a future `build-guidelines`-style generation skill as a backlog item if the knowledge index grows large enough to warrant it.

---

## Sources

- `_bmad-output/planning-artifacts/decisions/dec-001-three-tier-agent-guidelines-2026-04-09.md` — DEC-001, three-tier architecture, trigger table prescription
- `_bmad-output/planning-artifacts/decisions/dec-015-kb-cold-context-workflow-steps-constitution-audit-2026-05-02.md` — DEC-015, prescriptive vs. permissive trigger language
- `_bmad-output/planning-artifacts/decisions/dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md` — DEC-018, wiki-query syntax in constitution triggers
- `.momentum/stories/build-guidelines-skill.md` — planned trigger table generator (backlog)
- `.momentum/stories/wiki-query-interface-block-for-hot-constitution.md` — backlog story for imperative trigger language
- [SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale](https://arxiv.org/abs/2603.22455) — runtime skill routing, March 2026
- [SkillRouter HTML](https://arxiv.org/html/2603.22455v1) — full paper
- [skill-semantic-router (GitHub)](https://github.com/zhuang-HE/skill-semantic-router) — semantic routing framework
- [metaskill (GitHub)](https://github.com/xvirobotics/metaskill) — meta-skill generating routing tables
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — official trigger/description authoring guidance
- [mgechev/skills-best-practices (GitHub)](https://github.com/mgechev/skills-best-practices) — community skill authoring guide
- [SkillReducer: Optimizing LLM Agent Skills for Token Efficiency](https://arxiv.org/html/2603.29919v1) — skill description coverage statistics
- [Skill Retrieval Augmentation for Agentic AI](https://arxiv.org/html/2604.24594) — runtime retrieval augmentation, April 2026
- [VoltAgent/awesome-agent-skills (GitHub)](https://github.com/VoltAgent/awesome-agent-skills) — community skill library, 1000+
- [alirezarezvani/claude-skills (GitHub)](https://github.com/alirezarezvani/claude-skills) — Claude-specific skill library, 232+
