# Sprint Plan: sprint-2026-04-03

**Date:** 2026-04-03
**Sprint slug:** sprint-2026-04-03
**Status:** Planning
**Stories:** 3

---

## Sprint Goal

Deliver the research infrastructure layer: AVFL corpus validation for multi-document quality gates, a full 6-phase research skill with provenance tracking, and project-specific agent guidelines generation. These three stories are independently implementable and enable Epic 8 (Research & Knowledge Management) alongside the Impetus Core agent guidelines capability.

---

## Stories in Sprint

| # | Story Key | Title | Epic | Change Type | Wave |
|---|-----------|-------|------|-------------|------|
| 1 | agent-guidelines-skill | Agent Guidelines Skill — Guided Technology Guidelines Generation | impetus-core | skill-instruction | 1 |
| 2 | 8-1-avfl-corpus-mode | AVFL Corpus Mode — Multi-Document Cross-Validation | research-knowledge-management | skill-instruction | 1 |
| 3 | 8-2-momentum-research-skill | momentum-research Skill — 6-Phase Deep Research Pipeline | research-knowledge-management | skill-instruction | 1 |

---

## Dependency Graph

```
agent-guidelines-skill  ──(independent)──>  Wave 1
8-1-avfl-corpus-mode    ──(independent)──>  Wave 1
8-2-momentum-research-skill ──(soft: Phase 3 needs 8-1)──> Wave 1*

* Story 8-2 Phases 1,2,4,5,6 are fully independent.
  Phase 3 (VERIFY) requires 8-1-avfl-corpus-mode corpus mode.
  Implementation strategy: build all phases except 3, placeholder Phase 3,
  then integrate after 8-1 lands.
```

**Execution waves:** All 3 stories can start concurrently (Wave 1). No hard blocks. The 8-2 → 8-1 dependency is phase-level only and managed by implementing Phase 3 as a placeholder stub initially.

---

## Team Composition

### Generic Momentum Roles (Architecture Decision 26 — Two-Layer Model)

| Role | Skill / Agent | Purpose | Assigned When |
|------|--------------|---------|---------------|
| **Dev** | `momentum-dev` | Implements stories in worktrees, logs decisions via `momentum-tools log` | Every story |
| **QA** | Code reviewer | Reviews code against acceptance criteria | Stories with `script-code` change type |
| **E2E Validator** | Verifier agent | Validates behavior against Gherkin specs (black-box — never sees implementation) | All stories with Gherkin specs |
| **Architect Guard** | `momentum-architecture-guard` | Checks pattern drift against architecture decisions | Stories touching architecture-sensitive paths |

### Role Assignment per Story

| Story | Dev | QA | E2E Validator | Architect Guard |
|-------|:---:|:--:|:-------------:|:---------------:|
| agent-guidelines-skill | Yes | — | Yes (12 scenarios) | — |
| 8-1-avfl-corpus-mode | Yes | — | Yes (12 scenarios) | Yes |
| 8-2-momentum-research-skill | Yes | — | Yes (20 scenarios) | — |

**Why no QA:** All stories are `skill-instruction` (markdown skill files, not compiled code). No `script-code` tasks exist in this sprint.

**Why Architect Guard on 8-1:** Story 8-1 modifies `framework.json` — the core AVFL dimension taxonomy and prompt templates that all validation lenses depend on. The `corpus_only: true` flag and new dimensions must not break existing single-document validation contracts.

### Project-Specific Guidelines (Layer 2)

Momentum is a practice module (markdown + bash, no compiled code). Stack-specific guidelines per role:

| Role | Project Guidelines |
|------|-------------------|
| **Dev** | EDD approach: write behavioral evals BEFORE any skill files. NFR compliance: SKILL.md description ≤150 chars, `model:` and `effort:` frontmatter required, body ≤500 lines (overflow → `references/`). Provenance: all new files include `derives_from` and `content_origin` where applicable. |
| **E2E Validator** | Phase 3 verification is a **developer-confirmation checklist** derived from Gherkin scenarios — full automated verification is deferred (per sprint-dev story AC). Verifier reads specs from `sprints/phase-3-sprint-execution/specs/`, checks each scenario against the merged codebase, and reports pass/fail per scenario. |
| **Architect Guard** | Run `momentum-architecture-guard` on 8-1 changeset. Verify: (1) existing lens dimension assignments unchanged, (2) `corpus_only: true` flag prevents new dimensions from activating in single-doc mode, (3) prompt template variants extend (not replace) existing templates. |

### Test Approach per Story

| Story | Approach | Evals |
|-------|----------|-------|
| agent-guidelines-skill | EDD | Verify discovery accuracy, rule structure, prohibition format, version pinning, AVFL invocation |
| 8-1-avfl-corpus-mode | EDD (3 evals) | `eval-corpus-cross-document-dimensions.md`, `eval-corpus-backward-compatible.md`, `eval-corpus-fixer-authority-resolution.md` |
| 8-2-momentum-research-skill | EDD (3 evals) | `eval-light-profile.md`, `eval-medium-profile.md` (Phase 3 portion deferred until 8-1 lands), `eval-resume-support.md` |

### Execution Sequence

```
Wave 1 (all concurrent):
  ├── agent-guidelines-skill  ──> Dev ──> E2E Validator
  ├── 8-1-avfl-corpus-mode    ──> Dev ──> Architect Guard ──> E2E Validator
  └── 8-2-momentum-research   ──> Dev (Phases 1,2,4,5,6) ──> E2E Validator (light scenarios)

After 8-1 merges:
  └── 8-2-momentum-research   ──> Dev (Phase 3 integration) ──> E2E Validator (medium scenarios)

Post-merge (all stories done):
  └── Sprint-level AVFL pass on full codebase
  └── E2E Verification pass: all 44 Gherkin scenarios
  └── Sprint summary + retro suggestion
```

---

## FR Coverage

| FR | Description | Story |
|----|-------------|-------|
| FR48 | AVFL skill (extended with corpus mode) | 8-1-avfl-corpus-mode |
| FR44 | Multi-model research (partial — CLI, not MCP) | 8-2-momentum-research-skill |
| FR45 | Date-anchoring and primary-source directives | 8-2-momentum-research-skill |
| FR12 | derives_from frontmatter in research output | 8-2-momentum-research-skill |
| FR16 | Claim-level provenance status | 8-2-momentum-research-skill |
| FR17 | Content origin tracking | 8-2-momentum-research-skill |
| FR61a | Two-layer agent model guideline creation | agent-guidelines-skill |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Rate limits during 8-2 testing (multi-agent research) | High | Medium | Use light profile for initial testing; stagger agent launches |
| 8-1 delays block 8-2 Phase 3 integration | Medium | Low | Phase 3 is a placeholder; 5 of 6 phases testable independently |
| AVFL corpus mode prompt size exceeds subagent context | Low | High | Documented limit: 3-15 files recommended; most research corpora are 6-8 files |
| Gemini CLI auth issues during 8-2 testing | Medium | Low | Graceful degradation: prompt written to file, user told to run `! gemini` |

---

## AVFL Validation

Sprint-level AVFL checkpoint was run on all story files as a corpus (3 validators: Structural, Accuracy, Domain). Results:

- **16 findings** identified (6 HIGH, 5 MEDIUM, 5 LOW)
- **11 findings fixed** in fix pass (all HIGH and MEDIUM)
- **5 LOW findings** accepted as known issues
- **Status:** CHECKPOINT_WARNING — stories are ready for dev with known minor issues

Key fixes applied:
- Story 8-1: added `story_key`, structured `derives_from`, `corpus_only: true` flags, exact prompt template names, "Extends" not "Implements" FR48
- Story 8-2: removed hard `depends_on` block (→ soft dependency), added Tasks/Subtasks section, disclosed FR44 CLI deviation, added SUSPECT provenance row, Q&A fallback for placeholder Phase 3

---

## Gherkin Specs

Detailed behavioral specifications for verifier agents:
- `sprints/phase-3-sprint-execution/specs/8-1-avfl-corpus-mode.feature`
- `sprints/phase-3-sprint-execution/specs/8-2-momentum-research-skill.feature`
- `sprints/phase-3-sprint-execution/specs/agent-guidelines-skill.feature` (pre-existing)

---

## Approval

- [ ] Developer reviews sprint plan
- [ ] Developer approves story selection and wave assignments
- [ ] Sprint activated via `momentum-tools sprint activate`
