---
topic: "everything-claude-code vs Momentum — comparative analysis"
goals: "Identify parallels, where everything-claude-code is superior, where Momentum is superior, community traction, portability across agentic CLIs, philosophy comparison, and integration assessment"
profile: heavy
date: 2026-04-26
sub_questions:
  - "Architecture & capabilities — what does affaan-m/everything-claude-code ship at the code level (commands, hooks, agents, skills, MCP servers, output styles, settings, statuslines)? Read the source, not just the README."
  - "Maturity & community signals — release cadence, version history, contributor velocity, issue/PR throughput, code health (tests, CI, structure), star growth, ecosystem mentions. How polished is this project?"
  - "Direct feature parallels with Momentum — sprint planning, story-driven dev, multi-agent orchestration, validation loops, retrospectives, plugin distribution, memory systems, hooks-driven enforcement."
  - "Where is everything-claude-code superior or has features Momentum lacks — patterns, ergonomics, ideas worth borrowing."
  - "Where is Momentum superior — AVFL, Gherkin/ATDD, structured artifacts (intake-queue, stories/index, decision documents), sprint discipline, change-type classification, epic grooming, feature taxonomy."
  - "Portability across agentic CLIs — Claude Code-exclusive, or designed for OpenCode/Goose/ForgeCode/Codex/Aider? Is there an abstraction layer? What is the multi-agent story?"
  - "Philosophy comparison — design philosophy, governance model, opinionatedness, target user (solo dev vs team vs hobbyist), pedagogy (does it teach a practice or just ship tools?), how it treats AI agents, conventions vs flexibility."
  - "Integration assessment — would integrating it (or specific pieces) into Momentum be useful? What is portable, what is incompatible, what would conflict, what is the migration cost vs benefit?"
---

# Research Scope: everything-claude-code vs Momentum — comparative analysis

**Date:** 2026-04-26
**Profile:** heavy
**Goals:** Identify parallels, where everything-claude-code is superior, where Momentum is superior, community traction, portability across agentic CLIs, philosophy comparison, and integration assessment.

## Repository Under Study

`https://github.com/affaan-m/everything-claude-code`

## Sub-Questions

1. **Architecture & capabilities** — What does `affaan-m/everything-claude-code` ship at the code level? Commands, hooks, agents, skills, MCP servers, output styles, settings, statuslines. Read the actual source, not just the README.

2. **Maturity & community signals** — Release cadence, version history, contributor velocity, issue/PR throughput, code health (tests, CI, structure), star growth, ecosystem mentions. Is this a polished project or a hot README?

3. **Direct feature parallels with Momentum** — Where the two solve the same problem: sprint planning, story-driven dev, multi-agent orchestration, validation loops, retrospectives, plugin distribution, memory systems, hooks-driven enforcement.

4. **Where everything-claude-code is superior / has features Momentum lacks** — Patterns, ergonomics, ideas worth borrowing.

5. **Where Momentum is superior** — AVFL, Gherkin/ATDD, structured artifacts (intake-queue, stories/index, decision documents), sprint discipline, change-type classification, epic grooming, feature taxonomy.

6. **Portability across agentic CLIs** — Claude Code-exclusive, or designed for OpenCode / Goose / ForgeCode / Codex / Aider? Is there an abstraction layer? What is the multi-agent story?

7. **Philosophy comparison** — Design philosophy, governance model, opinionatedness, target user (solo dev vs team vs hobbyist), pedagogy (does it teach a practice or just ship tools?), how it treats AI agents (peers, tools, orchestrators), conventions vs flexibility.

8. **Integration assessment** — Would integrating it (or specific pieces) into Momentum be useful? What is portable, what is incompatible, what would conflict, what is the migration cost vs benefit?

## Momentum Context (for comparators)

Momentum is the agentic engineering practice module in this repository. Key Momentum concepts that researchers should reference when answering Q3, Q4, Q5, Q7, Q8:

- **Skills** — reusable instruction packages (e.g., `momentum:sprint-planning`, `momentum:sprint-dev`, `momentum:retro`, `momentum:avfl`, `momentum:create-story`, `momentum:intake`, `momentum:research`, `momentum:decision`, `momentum:feature-grooming`, `momentum:epic-grooming`, `momentum:assessment`, `momentum:quick-fix`).
- **AVFL** — Adversarial Validate-Fix Loop, multi-agent enumerator+adversary lens validation.
- **Gherkin/ATDD** — behavioral acceptance specs.
- **Sprint discipline** — sprint-manager owns stories/index.json and sprints/index.json with state-machine transitions.
- **Memory** — persistent file-based memory at `~/.claude/projects/.../memory/`.
- **Hooks** — settings.json hooks enforcing behavior (e.g., commit checkpoints, plan-audit gate).
- **Plugin distribution** — packaged as a Claude Code plugin under `skills/momentum/`.
- **Decision documents** — captured strategic decisions as standalone artifacts.
- **Intake queue** — `intake-queue.jsonl` event log for backlog ideas.
- **Feature/epic grooming** — taxonomy maintenance for features and epics.

Researchers should browse this repository's `.claude/`, `_bmad-output/`, and `skills/momentum/` directories when comparing concepts.
