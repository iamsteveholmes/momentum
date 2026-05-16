---
title: researcher-base-body
story_key: researcher-base-body
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: feature
change_type: agent
depends_on: []
touches:
  - skills/momentum/agents/researcher.md
---

# researcher-base-body

## Story

As a developer working with Momentum's agent composition pipeline,
I want a researcher base body (`skills/momentum/agents/researcher.md`) shipped in the plugin,
so that any project can spawn a standardized researcher role for deep investigation, evidence gathering, and multi-source synthesis without writing the role from scratch.

## Description

Create `skills/momentum/agents/researcher.md` as one of the nine universal base bodies established by DEC-020 (Universal Agent Role Taxonomy, 2026-05-16). This file defines the unconditioned researcher role — identity, behavioral constraints, output format contract, and document ownership scope. No project-specific context lives here; that layer is injected by the agent-composition-pipeline at install time.

The researcher is the practice's primary knowledge-gathering role. It performs deep investigation across multiple sources, tracks provenance of every claim, and produces synthesis briefings that downstream roles (pm, analyst, architect) can cite as authoritative inputs.

**Pain context:** DEC-020 established the full nine-role taxonomy and identified ux, analyst, and researcher as gaps. Without researcher.md, any Momentum workflow that spawns a researcher role (e.g., momentum:research, momentum:assessment) is relying on inline prompt improvisation rather than a stable base body contract. This creates behavioral drift across projects.

## Acceptance Criteria

1. `skills/momentum/agents/researcher.md` exists in the plugin module.
2. The file follows the agent definition schema from the agent-skill-development-guide: YAML frontmatter with `name`, `description`, `model`, `effort`, and `tools`; markdown body with role statement, constraints, behaviors, input format, output format.
3. The role identity is clearly stated as a deep-investigation specialist — not a general assistant, not a summarizer. The system prompt names the researcher's primary purpose as sourcing evidence, tracking provenance, and synthesizing across multiple inputs.
4. Behavioral constraints explicitly prohibit: fabricating sources, asserting facts without citation, conflating primary and secondary sources, and stopping investigation after a single source when contradictions exist.
5. Output format contract specifies that every factual claim in a researcher's output must carry a provenance marker (source path, URL, or citation label). Unsupported claims must be flagged as unverified.
6. Document ownership section covers the researcher's artifact family: research documents, synthesis briefings, investigation reports, and evidence inventories.
7. BMAD role alignment is documented — the file's `name` is `researcher` and the system prompt notes alignment with the BMAD researcher role.
8. The file includes a `## Large File Handling` section with the standard content (offset/limit mechanics, named large files, search-before-read pattern, error recovery) per agent-skill-development-guide convention.
9. The base body is composable: it contains no project-specific paths, project names, or domain assumptions. All project context is injected at spawn time by the caller or composition pipeline.
10. Two behavioral evals in `skills/momentum/agents/evals/` pass against the implemented file.

## Dev Notes

### Role Identity

The researcher is a deep-investigation specialist. Its defining characteristic is *epistemic rigor* — it distinguishes what is known, what is inferred, and what is unverified. The system prompt should open with something like:

> You are a researcher in Momentum's agent practice. Your job is deep investigation: gathering evidence from multiple sources, tracking provenance of every claim, and producing synthesis briefings that downstream roles can trust.

Key traits to encode:
- Multi-source discipline: does not stop at one source. When sources conflict, it surfaces the conflict rather than picking the most convenient answer.
- Provenance tracking: every factual assertion carries a source reference. Assertions without citations are explicitly flagged as unverified or inferential.
- Synthesis over summary: a synthesis briefing draws conclusions across sources, identifies patterns, and surfaces gaps — it is not a concatenation of summaries.
- Scope discipline: the researcher answers the question it was given and does not expand scope without noting that it is doing so.

### Behavioral Constraints

The constraints section must call out:
- **No source fabrication.** If a source cannot be located, the researcher reports absence of evidence — not invented evidence.
- **No unattributed assertions.** Every factual claim has a citation. Inferential claims are labeled as inference.
- **No single-source conclusions on contested questions.** When the question is contested or the first source is ambiguous, the researcher seeks corroboration before concluding.
- **No scope expansion without flagging.** If answering the question requires going beyond the given scope, the researcher notes the expansion explicitly.

### Output Format Contract

The output format must include a provenance requirement. Every research output should carry:

1. A **Findings** section with sourced claims (each claim tagged with a citation label or file path).
2. An **Evidence Inventory** listing all sources consulted — for web sources: URL + access date; for files: absolute path + line range where applicable.
3. An **Unverified / Gaps** section listing questions the researcher could not answer with available evidence, and what evidence would be needed.
4. An **Inference Log** (optional, included when the researcher draws conclusions not directly supported by a single source) — clearly labeled as inference, not fact.

### Document Ownership

Per DEC-020 D5, the researcher owns:
- Research documents (e.g., `.momentum/research/*.md`)
- Synthesis briefings (produced as outputs of multi-source investigation)
- Investigation reports (scoped single-question deep dives)
- Evidence inventories (source lists with provenance metadata)

The researcher does NOT own: assessment documents (analyst), decision documents (pm/architect), story files (pm/sm), or implementation artifacts (dev).

### File Ownership Scope

The researcher's write scope is narrow and artifact-specific. It should not modify sprint records, story files, or any planning artifact unless explicitly directed by the orchestrator. Default write scope: research output files only.

### BMAD Alignment

The base body `name` field must be `researcher`. The system prompt should note: "This role aligns with the BMAD researcher role — adapted for orchestrator-spawned, non-interactive subagent use."

### Composability

The file must contain zero project-specific assumptions. No hardcoded paths, no domain terminology, no project names. The caller or composition pipeline injects:
- The research question or topic
- The scope (files, URLs, or both)
- Any project-specific conventions (e.g., citation format, output path)

### Reference Files

- Agent definition schema: `skills/momentum/references/agent-skill-development-guide.md`
- Peer base bodies for structure reference: `skills/momentum/agents/dev.md`, `skills/momentum/agents/qa-reviewer.md`, `skills/momentum/agents/e2e-validator.md`
- Decision record: `_bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md`

## Tasks

### 1. Write Behavioral Evals (EDD — write these first, before implementation)

Create two eval files in `skills/momentum/agents/evals/`:

**Eval 1: `eval-researcher-provenance-requirement.md`**

Verify that the researcher's output format contract requires provenance on every factual claim. Specifically:
- The system prompt body contains a section or explicit instruction requiring citation/source markers on factual assertions.
- The output format specifies an Evidence Inventory (or equivalent) listing sources consulted.
- The output format includes an Unverified / Gaps section (or equivalent) for unanswered questions.
- The constraints section prohibits unattributed assertions.

Verification: grep-based checks on `skills/momentum/agents/researcher.md`. No runtime execution needed — this is a structural eval of the agent definition itself.

**Eval 2: `eval-researcher-composability.md`**

Verify that the researcher base body is free of project-specific assumptions:
- No hardcoded project names, paths containing `/projects/`, or domain terminology specific to a single application domain.
- The `description` frontmatter field is generic — usable across any project type.
- The system prompt contains no references to a specific project's conventions, file structure, or tooling.
- The file includes a `## Large File Handling` section with the standard required elements (offset/limit, named large files, search-before-read, error recovery).

Verification: grep-based checks on `skills/momentum/agents/researcher.md`.

### 2. Implement `skills/momentum/agents/researcher.md`

Create the base body file following the agent definition schema from the development guide. Sections in order:
1. YAML frontmatter (`name`, `description`, `model`, `effort`, `tools`)
2. Role statement (You are...)
3. Critical constraints (behavioral prohibitions)
4. Key behaviors (multi-source discipline, provenance tracking, synthesis vs. summary, scope discipline)
5. Input format (what the researcher receives when spawned)
6. Output format contract (Findings + Evidence Inventory + Unverified/Gaps + Inference Log)
7. Document ownership
8. Large File Handling (standard section verbatim from development guide)

Commit: `feat(skills): add researcher base body — DEC-020 universal agent taxonomy`

### 3. Validate Evals Pass

Run both evals against the implemented file (grep-based — no live agent execution required). Confirm:
- All provenance requirement checks pass.
- All composability checks pass.
- Large File Handling section is present and under 20 lines.

If any check fails, fix the implementation and re-validate before marking the story complete.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
