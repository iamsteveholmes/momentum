Research Topic: Comparative analysis of `affaan-m/everything-claude-code` (https://github.com/affaan-m/everything-claude-code) vs Momentum (an agentic engineering practice module for Claude Code)

I need a comprehensive analysis of how `affaan-m/everything-claude-code` compares to Momentum.

Research Goals: Identify parallels, where everything-claude-code is superior, where Momentum is superior, community traction, portability across agentic CLIs, philosophy comparison, and integration assessment. The findings will inform whether Momentum should adopt patterns from this project, integrate parts of it, or remain on its current trajectory.

Context on Momentum (the comparator):
- Momentum is a Claude Code plugin that ships skills (sprint-planning, sprint-dev, retro, avfl, create-story, intake, research, decision, feature-grooming, epic-grooming, assessment, quick-fix, impetus orchestrator).
- AVFL (Adversarial Validate-Fix Loop) — multi-agent enumerator+adversary lens validation.
- Gherkin/ATDD acceptance specs.
- Sprint discipline with state-machine transitions on stories/index.json and sprints/index.json.
- Persistent file-based memory at `~/.claude/projects/.../memory/`.
- Settings.json hooks enforce behavior (commit checkpoints, plan-audit gates).
- Plugin distribution via Claude Code plugin marketplace.
- Decision documents, intake queue (intake-queue.jsonl), feature/epic grooming taxonomy.

Key questions to investigate:

1. **Architecture & capabilities of `affaan-m/everything-claude-code`** — What does the repository ship at the code level? Browse the repo structure. Enumerate commands, hooks, agents, skills, MCP servers, output styles, settings, statuslines. Read actual source files (not just the README). What is the directory layout? What programming/scripting languages? What does each major folder contain?

2. **Maturity & community signals** — Release cadence and version history (check tags, releases, commits). Contributor velocity (number of contributors, recent activity). Issue/PR throughput (open vs closed, response time). Code health (presence of tests, CI workflows, structure quality, dependency hygiene). Star growth and forks. Ecosystem mentions (blog posts, Reddit, Hacker News, Twitter/X, YouTube). Is this a polished, production-grade project or a hot README riding the Claude Code hype curve?

3. **Direct feature parallels with Momentum** — Map features in `everything-claude-code` to Momentum equivalents. Where do they overlap? Sprint planning? Story-driven development? Multi-agent orchestration? Validation loops (anything like AVFL)? Retrospectives? Plugin/distribution model? Memory systems? Hooks-driven enforcement? List specific commands/skills/agents in `everything-claude-code` and the closest Momentum analogue (or "no analogue").

4. **Where `everything-claude-code` is superior or has features Momentum lacks** — Look for patterns, ergonomics, ideas that Momentum doesn't have. UX wins, novel workflows, clever hook usage, distribution polish, onboarding, documentation patterns, community-driven contribution model, pre-built integrations.

5. **Where Momentum is superior** — Conceptual or implementation depth not present in `everything-claude-code`: AVFL-style adversarial validation, Gherkin/ATDD behavioral specs, structured sprint state machines, change-type classification on stories, intake-queue event log, decision document capture, epic/feature taxonomy grooming, plan-audit hook gates, persistent multi-conversation memory.

6. **Portability across agentic CLIs** — Is `everything-claude-code` Claude Code-exclusive, or does it support / target / abstract over OpenCode, Goose, ForgeCode, Codex, Aider, or other agentic CLIs? Are commands, hooks, agents, MCP configs portable to other tools? Is there an explicit cross-tool design? What is its multi-agent or multi-tool story?

7. **Philosophy comparison** — How does the project's design philosophy compare to Momentum's? Governance model (single maintainer vs community vs opinionated team?). Opinionatedness (does it teach a practice or hand you a toolkit?). Target user (solo dev, team, hobbyist, enterprise?). Pedagogy (does it explain WHY things are done a certain way, or just provide tools?). How does it treat AI agents — as peers, tools, orchestrators, replaceable workers? Conventions vs flexibility.

8. **Integration assessment** — Would integrating `everything-claude-code` (or specific pieces of it) into Momentum be useful? What is portable to Momentum? What would conflict architecturally or philosophically? What is the migration cost vs benefit? Concrete recommendations: adopt-as-is, adopt-with-modification, watch-and-learn, ignore, or fork.

Desired output: A structured report with findings organized by question, including:
- Specific actionable recommendations where available
- Example patterns or implementations where relevant — quote actual file paths and code snippets from the `everything-claude-code` repo
- Citations with URLs for every factual claim (GitHub file links, blog URLs, social media links, release notes)
- An honest assessment of current limitations and gaps in `everything-claude-code` — do not give it the benefit of the doubt
- Direct side-by-side comparisons with Momentum where possible

Date context: Today is 2026-04-26. Prioritize current and recent sources (2025-2026). The Claude Code ecosystem evolves rapidly, so older sources may be obsolete.
