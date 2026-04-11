---
title: Agent Guidelines Skill — Guided Technology Guidelines Generation for Projects
status: done
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum-agent-guidelines/SKILL.md
  - skills/momentum-agent-guidelines/workflow.md
  - skills/momentum-agent-guidelines/references/detection-heuristics.md
  - skills/momentum-agent-guidelines/references/rule-template.md
  - skills/momentum-agent-guidelines/references/reference-doc-template.md
  - skills/momentum-agent-guidelines/sub-skills/
change_type: skill-instruction
---

# Agent Guidelines Skill

> **Gen-1 implementation — superseded by gen-2 architecture.**
> This skill generates `.claude/rules/` and `docs/guidelines/` artifacts (the correct
> content shape) but does NOT generate the Tier 1 hot constitution or Tier 2 composed
> specialist agent files. See DEC-001 and `build-guidelines-skill` story for gen-2.
> Gen-1 output is directly reusable as cold KB input for `momentum:kb-ingest`.

## Goal

Create the `momentum-agent-guidelines` skill that fills the explicit gap in Decision 26
(Two-Layer Agent Model): Momentum provides generic agent roles, but projects have no
tooling to create the stack-specific guidelines those roles need. This skill discovers a
project's technology stack, researches current state and breaking changes, interactively
consults with the developer on recommendations, and generates a complete set of
path-scoped rules, reference docs, and CLAUDE.md updates.

Implements FR61a. Grounded in the Agent Guidelines Authoring research report
(`_bmad-output/planning-artifacts/research/technical-agent-guidelines-authoring-research-2026-04-03.md`).

## Acceptance Criteria (Plain English)

> Detailed Gherkin specs: `_bmad-output/implementation-artifacts/sprints/phase-3-sprint-execution/specs/agent-guidelines-skill.feature`

### Discovery Phase
- The skill spawns parallel subagents to scan the project for technology stack signals
- Build files are detected: `build.gradle.kts`, `package.json`, `Cargo.toml`,
  `pyproject.toml`, `go.mod`, `pom.xml`, and similar
- Existing `.claude/rules/` files and `CLAUDE.md` are audited for current coverage
- Test configuration files and testing frameworks are detected
- Source patterns are scanned to identify languages, frameworks, and conventions
- Discovery results are presented to the user as a structured technology profile

### Research Phase
- For each detected technology, focused web searches find current versions, breaking
  changes from likely training data, and deprecated patterns
- Research outputs are in prohibition format: "NEVER use X — use Y instead"
- Research stays light (2-3 web searches per technology); user can escalate to full
  research skill if needed
- Research findings are presented to the user with sources

### Consultation Phase
- Interactive back-and-forth covers: technology inventory confirmation, existing
  guidelines audit, testing framework recommendations, validation approach, path scope
  design, and content depth decisions
- Each decision point stops and waits for user input
- User can accept, modify, or skip any recommendation
- User can request deeper research on any specific technology

### Generation Phase
- Path-scoped `.claude/rules/*.md` files are generated with correct `paths:` frontmatter
- Each rules file is 30-80 lines, following the research-backed ordering: version pins
  first, then critical prohibitions, then correct patterns, then setup specifics
- Reference docs are generated in `docs/references/` (100-300 lines) for technologies
  with significant training data gaps
- CLAUDE.md is updated with pointers to generated reference docs
- All generated files include version pins and `Last verified:` date stamps

### Validation Phase
- AVFL checkpoint profile runs on all generated artifacts
- Findings are presented to the user before finalizing
- User can accept or request fixes

## Dev Notes

### What exists today
- Decision 26 and FR61 describe the two-layer model but provide no creation tooling
- FR61a (added in this sprint) defines the requirement for this skill
- The architecture section under "Agent Guidelines Generation" describes the workflow
- The research report provides the complete evidence base for all design decisions
- Existing skills (`momentum-create-story`, `momentum-avfl`) provide structural patterns

### Skill structure

```
skills/momentum-agent-guidelines/
  SKILL.md                              # model: opus, effort: high
  workflow.md                           # 5-phase XML workflow
  references/
    detection-heuristics.md             # build file → technology mapping
    rule-template.md                    # template for generated rules files
    reference-doc-template.md           # template for generated reference docs
  sub-skills/
    build-scanner/SKILL.md              # model: sonnet, effort: medium
    rules-auditor/SKILL.md              # model: sonnet, effort: medium
    test-config-scanner/SKILL.md        # model: sonnet, effort: medium
    source-pattern-scanner/SKILL.md     # model: sonnet, effort: medium
```

### Change type: skill-instruction

**EDD approach** — Behavioral evals should verify:
- Discovery subagents correctly identify technologies from representative build files
- Generated rules files contain valid `paths:` frontmatter with correct glob patterns
- Generated rules follow prohibition format and include version pins
- Generated rules are under 80 lines
- AVFL checkpoint is invoked on generated artifacts

### Key design decisions
1. Opus for orchestration (consultation needs nuance), Sonnet for all subagents
2. Detection heuristics in a reference file, not code — extensible and human-editable
3. Light research by default (web searches), with escalation to full research skill
4. Consultation before generation — don't waste compute on unwanted artifacts
5. Path-scoped rules compose automatically with generic agents via the file system

## File List

- `skills/momentum-agent-guidelines/SKILL.md` — new (orchestrator, opus/high)
- `skills/momentum-agent-guidelines/workflow.md` — new (5-phase workflow)
- `skills/momentum-agent-guidelines/references/detection-heuristics.md` — new (build file → tech mapping, staleness risk)
- `skills/momentum-agent-guidelines/references/rule-template.md` — new (generation template for path-scoped rules)
- `skills/momentum-agent-guidelines/references/reference-doc-template.md` — new (generation template for reference docs)
- `skills/momentum-agent-guidelines/sub-skills/build-scanner/SKILL.md` — new (sonnet/medium)
- `skills/momentum-agent-guidelines/sub-skills/rules-auditor/SKILL.md` — new (sonnet/medium)
- `skills/momentum-agent-guidelines/sub-skills/test-config-scanner/SKILL.md` — new (sonnet/medium)
- `skills/momentum-agent-guidelines/sub-skills/source-pattern-scanner/SKILL.md` — new (sonnet/medium)

## Change Log

- 2026-04-03: Initial implementation — all 9 skill files created. QA passed all ACs, Validator passed 15/17 scenarios (2 edge-case branches added post-review). AVFL checkpoint on sprint plan scored 97/100 post-fix.
