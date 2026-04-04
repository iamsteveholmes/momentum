---
title: momentum-research Skill — 6-Phase Deep Research Pipeline with Provenance
status: ready-for-dev
epic_slug: research-knowledge-management
story_key: 8-2-momentum-research-skill
depends_on: []  # Phases 1,2,4,5,6 are independent. Only Phase 3 (VERIFY) requires 8-1-avfl-corpus-mode — see Dev Notes for sequencing.
touches:
  - skills/momentum-research/SKILL.md
  - skills/momentum-research/workflow.md
  - skills/momentum-research/references/
  - skills/momentum-research/evals/
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/epics.md
    relationship: derives_from
    section: "Epic 8: Research & Knowledge Management"
  - path: ~/.claude/plans/fancy-plotting-beaver.md
    relationship: derives_from
    section: "Story 2: momentum-research Skill"
---

# Story 8-2: momentum-research Skill

## Goal

Create the `momentum-research` skill implementing a 6-phase deep research pipeline:
SCOPE → EXECUTE → VERIFY → Q&A → SYNTHESIZE → COMMIT. The skill produces
validated, provenance-tracked research documents through parallel subagents, optional
Gemini CLI triangulation, AVFL corpus validation, and Momentum provenance patterns.

**User Story:** As a Momentum developer, I want to run structured deep research using
Claude Code so that I get a validated, provenance-tracked research document through a
repeatable pipeline.

## Acceptance Criteria

### AC1: Skill Package Exists

- Skill exists at `~/.agents/skills/momentum-research/` with the following structure:
  ```
  skills/momentum-research/
  ├── SKILL.md                         # model: opus, effort: high
  ├── workflow.md                      # 6-phase pipeline
  ├── references/
  │   ├── profiles.md                  # light/medium/heavy definitions
  │   ├── briefing-template.md         # Subagent prompt template
  │   ├── gemini-prompt-template.md    # Gemini prompt generator
  │   └── output-structure.md         # Default synthesis structure
  └── evals/
      ├── eval-light-profile.md
      ├── eval-medium-profile.md
      └── eval-resume-support.md
  ```

### AC2: Phase 1 — SCOPE (Interactive)

- Elicits research topic from user
- Decomposes topic into 4–8 sub-questions that collectively cover the topic
- Asks user to select profile: light (3 agents, no AVFL, no Q&A), medium (5-6 agents,
  checkpoint AVFL, Q&A), or heavy (6-8 agents, full AVFL, Q&A)
- Creates project directory `{output_folder}/research/{topic-slug}-{YYYY-MM-DD}/`
  with subdirs: `raw/`, `validation/`, `final/`
- Writes `scope.md` into the project root with: topic, goals, decomposed sub-questions,
  selected profile, and date

### AC3: Phase 2 — EXECUTE (Parallel Subagents)

- Spawns N parallel background subagents per profile: light=3, medium=5-6, heavy=6-8
- Each subagent receives a briefing from `references/briefing-template.md` with:
  - The sub-question it is answering
  - Today's date (date-anchoring, FR45)
  - Instruction to use primary sources and cite URLs
  - Evidence notation requirement: `[OFFICIAL]`, `[PRAC]`, `[UNVERIFIED]`
- Each subagent writes its findings to `raw/research-{subtopic}.md` with frontmatter:
  `content_origin: claude-code-subagent`
- Each subagent also returns a 2-3 sentence inline summary to the orchestrator
- **Optional Gemini CLI integration:**
  - Skill checks `which gemini` before offering
  - Asks user to confirm before running `gemini -p`
  - Generates a Gemini prompt using `references/gemini-prompt-template.md`
  - Tells user to run `! gemini` if auth fails
  - If run, writes output to `raw/gemini-output.md` with frontmatter
    `content_origin: gemini-cli`
- **Resume support:** Phase 2 checks which `raw/research-*.md` files already exist.
  Only spawns agents for missing subtopics. Existing files are not overwritten.

### AC4: Phase 3 — VERIFY (AVFL Corpus Validation)

- Light profile: skip Phase 3 entirely, proceed to Phase 5 (SYNTHESIZE)
- Medium profile: invoke `momentum-avfl` with `corpus: true`, `profile=checkpoint`,
  2 lenses (structural + factual). AVFL report written to `validation/avfl-report.md`.
- Heavy profile: invoke `momentum-avfl` with `corpus: true`, `profile=full`,
  4 lenses. AVFL report written to `validation/avfl-report.md`.
- **Note:** Phase 3 on medium/heavy depends on Story 8-1 (avfl-corpus-mode) being
  implemented. Dev must implement and test Phases 1, 2, 4, 5, 6 first, then integrate
  Phase 3 after Story 8-1 lands.

### AC5: Phase 4 — Q&A (Practitioner Notes)

- Light profile: skip Phase 4 entirely
- Medium and Heavy profiles:
  - Presents AVFL-identified uncertainties and gaps as targeted questions to the user
  - Captures user responses interactively
  - Writes all Q&A to `raw/practitioner-notes.md` with frontmatter
    `content_origin: human`
  - When Phase 3 (VERIFY) was skipped or in placeholder state (Story 8-1 not yet landed): skip Q&A (no AVFL findings to present)

### AC6: Phase 5 — SYNTHESIZE (Subagent)

- A single Opus subagent runs in the foreground (not background)
- Subagent receives clean context: reads all `raw/*.md` files, `validation/*.md` files,
  and `scope.md` from disk
- Output structure adapts from Phase 1 scope (the sub-questions drive document sections)
- Falls back to `references/output-structure.md` as default structure template
- Writes synthesized document to `final/{topic-slug}-final-{YYYY-MM-DD}.md`
- Final document frontmatter includes:
  - `content_origin: claude-code-synthesis`
  - `human_verified: true` (if Q&A phase ran; false for light profile)
  - `derives_from` chain (see AC8)

### AC7: Phase 6 — COMMIT

- Proposes git commit to the user with conventional message:
  `docs(research): {topic description}`
- Waits for user confirmation before running commit
- Does not auto-push

### AC8: Provenance Tracking (FR12, FR16, FR17)

- Final document `derives_from` chain in frontmatter:
  ```yaml
  derives_from:
    - path: raw/research-{subtopic-1}.md
      relationship: synthesized_from
    - path: raw/research-{subtopic-2}.md
      relationship: synthesized_from
    # ... one entry per raw file ...
    - path: raw/gemini-output.md          # if present
      relationship: synthesized_from
    - path: validation/avfl-report.md     # if present
      relationship: validated_by
    - path: raw/practitioner-notes.md     # if present
      relationship: informed_by
  ```
- Each `raw/research-*.md` file includes `content_origin: claude-code-subagent`
- `raw/gemini-output.md` includes `content_origin: gemini-cli`
- `raw/practitioner-notes.md` includes `content_origin: human`
- Final doc uses `content_origin: claude-code-synthesis` with `human_verified: true`
  after Q&A; `human_verified: false` for light profile

### AC9: Evidence Notation → Claim-Level Provenance (FR16)

- Evidence notation maps to Momentum provenance:
  - `[OFFICIAL]` → VERIFIED (Anthropic docs, official APIs, primary sources)
  - `[PRAC]` → CITED (practitioner blogs, community reports with URL)
  - `[UNVERIFIED]` → INFERRED (reasonable inference, model knowledge, no source)
  - Claims with no attribution → UNGROUNDED (AVFL should flag these)
  - Claims flagged by AVFL → SUSPECT (claims that failed AVFL corpus validation in Phase 3 — annotated by AVFL fixer, not by subagent authors)

### AC10: Behavioral Evals (EDD)

- Three behavioral evals written **before** any skill files are created:
  - `eval-light-profile.md`: light profile spawns 3 agents, no AVFL, no Q&A,
    final doc produced
  - `eval-medium-profile.md`: medium profile runs AVFL corpus checkpoint, Q&A
    phase presents AVFL-identified uncertainties, final doc produced
  - `eval-resume-support.md`: interrupted mid-EXECUTE (some raw/ files exist),
    re-invoked, only missing subtopics are researched (existing files not overwritten)

## Dev Notes

### Architecture Context

This story originates from a real research session that used 6 parallel subagents,
Gemini Deep Research, and an 8-validator AVFL pass on 7 documents (corpus mode was
hacked together ad hoc). The methodology that worked is being formalized as a skill.

**The problem Phase 3 solves:** Multi-document research generates multiple `raw/*.md`
files that can contradict each other. Standard single-document AVFL can't catch
cross-document inconsistencies. Story 8-1 adds corpus mode to fix this.

### Dependency: Story 8-1 (avfl-corpus-mode)

Phase 3 requires `momentum-avfl` corpus mode (Story 8-1). **Implementation order:**

1. Implement and test Phases 1, 2, 4, 5, 6 first (no dependency on 8-1)
2. Write `workflow.md` with a clear `# Phase 3: VERIFY` placeholder that explains
   the dependency
3. After Story 8-1 lands and is merged, integrate Phase 3 invocation

Light profile works fully without 8-1. Medium/heavy Phase 3 is gated on 8-1.

### File Locations

- **Skill target:** `~/.agents/skills/momentum-research/` (same location as other
  Momentum skills installed via Agent Skills)
- **Research output:** `{output_folder}/research/{topic-slug}-{YYYY-MM-DD}/`
  where `output_folder` comes from `bmad-init` config
- **Evals:** `skills/momentum-research/evals/` — must exist before SKILL.md is written

### Key Design Decisions from Plan

1. **All validators get ALL corpus files** — no distribution. Cross-doc checks need
   full visibility. 6-8 raw files at ~4K tokens each = 24-32K tokens, fits in context.
2. **Gemini CLI** (not MCP): Use the `gemini` CLI with the `-p` flag for Deep Research.
   MCP integration is a growth feature; CLI works today.
3. **Resume support** is Phase 2 only: Check which `raw/research-*.md` files exist.
   Only spawn agents for missing subtopics. This handles rate-limit failures gracefully.
4. **Synthesis is a subagent** — clean 200K context window, reads everything from disk,
   writes final doc to disk. No context pollution from research phase.
5. **Q&A skipped for light** — light profile is optimized for speed.
6. **No continuation across invocations** — each invocation creates a new dated project
   directory. Prior research can be cited as `source_material` in a new SCOPE.

### Briefing Template Requirements (AC3)

The subagent briefing in `references/briefing-template.md` must include:
- Date anchoring: "Today is {date}. Cite sources that are current as of {date}."
- Primary source directive: "Prefer official docs and primary sources over secondary"
- Sub-question assignment: exactly what this agent is answering
- Evidence notation: define `[OFFICIAL]`, `[PRAC]`, `[UNVERIFIED]` with examples
- Output format: frontmatter with `content_origin: claude-code-subagent`, then findings
- Inline summary requirement: "End with a 2-3 sentence summary of your key findings"

### Gemini CLI Integration Notes (AC3)

```bash
# Check availability
which gemini  # if exits non-zero, skip Gemini offer

# Generate prompt from template
# Ask user to confirm before running

# Run Deep Research
gemini -p "{generated prompt}"

# If auth fails
# Tell user: "Run `! gemini` in the terminal to authenticate, then re-invoke the skill"
```

### NFR Compliance

- SKILL.md `description` field must be ≤150 characters (count precisely)
- `model: opus` and `effort: high` frontmatter required
- SKILL.md body ≤500 lines / 5000 tokens; overflow content goes in `references/`
- Skill name `momentum-research` follows `momentum-` prefix convention (NFR12)

### Related Work

- `momentum-avfl` — invoked in Phase 3; corpus mode required for medium/heavy profiles
- `bmad-init` — config loading for `output_folder`
- `momentum-create-story` — structural pattern reference for skill packaging
- `agent-guidelines-skill` story — same skill-instruction change type and EDD approach

### FR Coverage

- FR44 (partial — CLI-based): Multi-model research via parallel Claude subagents + Gemini CLI. FR44 specifies MCP-integrated providers; this implements CLI approximation per plan decision. MCP integration deferred to growth backlog.
- FR45: Date-anchoring and primary-source directives in subagent briefing template
- FR12: `derives_from` chain in final document frontmatter
- FR16: Claim-level provenance via evidence notation mapping
- FR17: `content_origin` tracking in every raw and final file

---

## Tasks / Subtasks

- [ ] **Task 1 — Write 3 behavioral evals (EDD — before any skill files)** (AC: 10)
  - [ ] Create `evals/eval-light-profile.md` — 3 agents, no AVFL, no Q&A, final doc produced
  - [ ] Create `evals/eval-medium-profile.md` — 5-6 agents, AVFL checkpoint, Q&A (Phase 3 portion requires Story 8-1 — mark with dependency note)
  - [ ] Create `evals/eval-resume-support.md` — detects existing raw/ files, only spawns missing subtopic agents

- [ ] **Task 2 — Create SKILL.md** (AC: 1)
  - [ ] Frontmatter: name=momentum-research, model=opus, effort=high, description ≤150 chars
  - [ ] Body: "Follow the instructions in ./workflow.md"

- [ ] **Task 3 — Create workflow.md with all 6 phases** (AC: 2, 3, 4, 5, 6, 7)
  - [ ] Phase 1 (SCOPE): topic elicitation, decomposition, profile selection, project dir creation
  - [ ] Phase 2 (EXECUTE): parallel subagents with briefing template, evidence notation, resume detection, optional Gemini CLI
  - [ ] Phase 3 (VERIFY): AVFL corpus invocation — placeholder stub until Story 8-1 lands, with `corpus: true`, scaled by profile
  - [ ] Phase 4 (Q&A): present AVFL uncertainties, write practitioner-notes.md. Fallback when Phase 3 is placeholder: skip Q&A (no AVFL findings to present)
  - [ ] Phase 5 (SYNTHESIZE): single Opus subagent, reads from disk, writes final doc
  - [ ] Phase 6 (COMMIT): propose conventional commit

- [ ] **Task 4 — Create all references/ files** (AC: 1, 8, 9)
  - [ ] `references/profiles.md` — light/medium/heavy definitions with agent counts, AVFL profiles, token estimates
  - [ ] `references/briefing-template.md` — subagent prompt with evidence notation, output format, word count guidance
  - [ ] `references/gemini-prompt-template.md` — Gemini Deep Research prompt generator with topic/sub-questions
  - [ ] `references/output-structure.md` — default synthesis structure (adaptable per topic), provenance frontmatter template

- [ ] **Task 5 — Run evals, verify behavior** (AC: 10)
  - [ ] Invoke each eval scenario and verify expected behavior
  - [ ] Light profile: end-to-end without AVFL
  - [ ] Resume: interrupt and re-invoke, confirm only missing subtopics re-run

---

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks → skill-instruction (EDD)
  *(All files are inside `skills/momentum-research/` — SKILL.md, workflow.md, references/, evals/)*

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are
non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum-research/evals/` (create `evals/`
   first):
   - One `.md` file per eval, named descriptively
   - Format each eval as: "Given [describe the input and context], the skill should
     [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text
   - Required evals (per AC10):
     - `eval-light-profile.md`
     - `eval-medium-profile.md`
     - `eval-resume-support.md`

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, and reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it:
   (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md
   and workflow.md contents as context. Observe whether the subagent's behavior matches
   the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run
   (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in
  `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills)

**Dependency sequencing:**
- Phases 1, 2, 4, 5, 6 can be implemented and tested without Story 8-1
- Write Phase 3 as a placeholder in `workflow.md` that documents the dependency
  and instructs the dev agent to integrate after 8-1 lands
- Medium/heavy evals that exercise Phase 3 should be written but marked with a
  note: "Phase 3 integration requires Story 8-1 (avfl-corpus-mode) to be done"
- Do not block story completion on Phase 3 integration — the story is done when
  Phases 1, 2, 4, 5, 6 are implemented, all 3 evals pass, and Phase 3 placeholder
  is in place

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3 behavioral evals written in `skills/momentum-research/evals/` BEFORE any
      skill files created
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model: opus` and `effort: high` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] Phase 3 placeholder in `workflow.md` with clear dependency note on Story 8-1
- [ ] `derives_from` chain structure documented in `references/output-structure.md`
      or equivalent reference
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this
      automatically — validates the implemented SKILL.md against story ACs)
