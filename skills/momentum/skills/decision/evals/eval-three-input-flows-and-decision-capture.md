# Eval: Four Input Flows and Decision Capture Format

**Skill:** `momentum:decision`
**AC Coverage:** AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8

---

## Purpose

Verify that the decision skill correctly handles all four input flows, captures
decisions with full context, produces properly structured SDR documents, updates
upstream links, and bridges to story creation.

---

## Eval 1: Flow A — From Assessment

### Input

```
Invocation: momentum:decision
Developer prompt: "I want to capture decisions from our latest assessment"
Context: ASR document exists at _bmad-output/planning-artifacts/assessments/asr-001-backend-readiness-2026-04-08.md
ASR has findings with recommendations:
  - Finding 1: Backend is 60% production-ready. Recommended: implement error handling layer
  - Finding 2: Auth is missing. Recommended: implement OAuth2 or use existing provider
```

### Expected Behavior

1. Skill asks which input flow: assessment, research doc, or revisit prior decision
2. Developer selects "from assessment"
3. Skill prompts for path to ASR document
4. Skill reads the ASR and presents Finding 1's recommendation
5. Skill asks: "What do you want to decide about this recommendation? (adopt / reject / defer / adapt)"
6. Developer says "adopt" with rationale
7. Skill records the decision and moves to Finding 2
8. Process repeats for each finding
9. Skill asks about affected stories and architecture decisions
10. Skill writes SDR to `_bmad-output/planning-artifacts/decisions/sdr-NNN-*.md`
11. Skill updates ASR frontmatter `decisions_produced` field with new SDR id
12. Skill updates `_bmad-output/planning-artifacts/decisions/index.md`
13. Skill commits all changes together
14. Skill asks: "Want to create stories for these decisions?"

### SDR Output Requirements

- Frontmatter includes: id, title, date, status, source_research, prior_decisions_reviewed, architecture_decisions_affected, stories_affected
- Body includes: Summary section, individual Decisions (each with recommendation/decision/rationale), Phased Implementation Plan (if applicable), Decision Gates (if applicable)
- id is auto-incremented (SDR-001 if no prior decisions, SDR-002 if one exists, etc.)
- File named: `sdr-NNN-slug-YYYY-MM-DD.md`

### Pass Criteria

- [ ] Skill identifies it is in Flow A (from assessment) based on developer input
- [ ] Skill reads the ASR and extracts all findings with their recommendations
- [ ] Each finding is presented one at a time with decision options (adopt/reject/defer/adapt)
- [ ] Developer rationale is captured for each decision
- [ ] SDR document written with correct frontmatter schema
- [ ] SDR body has Summary, numbered Decisions, each with recommendation/decision/rationale subsections
- [ ] ASR `decisions_produced` field updated with new SDR id
- [ ] `decisions/index.md` updated with new row
- [ ] Changes committed together in one commit
- [ ] Bridge to story creation offered at end

---

## Eval 2: Flow B — From Research Document

### Input

```
Invocation: momentum:decision
Developer prompt: "I have a research doc I need to make decisions from"
Context: Research document at docs/research/gemini-deep-research-stack-eval.md
Research has 5 recommendations:
  - Adopt GraphQL for API layer
  - Migrate to LangGraph for orchestration
  - Implement prefix caching
  - Use Redis for session state
  - Adopt multi-model routing
```

### Expected Behavior

1. Skill identifies Flow B (from research)
2. Prompts for research document path
3. Reads document and extracts recommendations
4. Presents each recommendation for decision: adopt / reject / defer / adapt
5. Developer decides: adopt GraphQL (with rationale), reject LangGraph, defer Redis, etc.
6. Skill captures all decisions with rationale
7. Produces SDR with all decisions documented

### Pass Criteria

- [ ] Skill identifies Flow B from developer input
- [ ] Skill reads research document and extracts recommendations
- [ ] Each recommendation presented individually (not dumped all at once)
- [ ] Each decision captured with: recommendation text, decision (adopt/reject/defer/adapt), rationale
- [ ] SDR written with source_research pointing to research doc with type: gemini-deep-research or prior-research

---

## Eval 3: Flow C — Revisit Prior Decision

### Input

```
Invocation: momentum:decision
Developer prompt: "I want to revisit SDR-001 — conditions have changed"
Context: SDR-001 exists at _bmad-output/planning-artifacts/decisions/sdr-001-stack-eval-2026-04-07.md
SDR-001 had a decision to defer LangGraph migration.
New context: LangGraph 2.0 released with major stability improvements.
```

### Expected Behavior

1. Skill identifies Flow C (revisit)
2. Prompts for path to existing SDR
3. Reads SDR and presents original decisions
4. For each decision, asks: "Have conditions changed for this decision?"
5. Developer confirms LangGraph decision has changed
6. Skill captures updated decision with new rationale
7. Produces new SDR with status referencing original
8. Original SDR could be updated to status: superseded

### Pass Criteria

- [ ] Skill identifies Flow C from developer input
- [ ] Skill reads existing SDR and presents original decisions
- [ ] For each decision, asks if conditions have changed
- [ ] New SDR produced with updated decisions
- [ ] Prior SDR referenced in new SDR frontmatter (prior_decisions_reviewed)

---

## Eval 4: Decision Context Completeness (AC3)

### Input

Any flow, capturing a single decision.

### Expected Captures

For each decision the SDR must contain:

```markdown
### D1: {{recommendation title}} — {{ADOPTED/REJECTED/DEFERRED/ADAPTED}}

**Research recommended:** {{what the source material said to do}}

**Decision:** {{adopted/rejected/deferred — with any modifications}}

**Rationale:**
{{developer's explanation in their own words}}
```

### Pass Criteria

- [ ] "Research recommended" section present for Flows A/B/C (captures source material recommendation verbatim or summarized) — OR — "Developer framing" section present for Flow D (captures what the developer was aiming for in their own words)
- [ ] "Decision" line clear — one of: adopted, rejected, deferred, adapted
- [ ] "Rationale" captures the developer's reasoning in their words (not paraphrased by skill)
- [ ] Source material links present in frontmatter `source_research`
- [ ] `stories_affected` populated with story slugs (or empty list if none)
- [ ] `architecture_decisions_affected` populated with AD references (or empty list if none)

---

## Eval 5: SDR Template Compliance (AC4, AC5)

### Verification

Read `skills/momentum/skills/decision/references/sdr-template.md` and verify:

- [ ] Template file exists at that path
- [ ] Frontmatter schema section defines all required fields: id, title, date, status, source_research, prior_decisions_reviewed, architecture_decisions_affected, stories_affected
- [ ] Body structure section defines: Summary, individual Decisions (with recommendation/decision/rationale), Phased Implementation Plan, Decision Gates
- [ ] Template includes naming convention (sdr-NNN-slug-YYYY-MM-DD.md)
- [ ] Template includes registry entry format for index.md

---

## Eval 6: Bridge to Story Creation (AC8)

### Expected End-of-Skill Behavior

After SDR is committed, the skill must:

1. Offer: "Want to create stories for these decisions?"
2. If developer says yes, invoke `momentum:create-story` or `momentum:intake` for each decision that implies new work
3. If developer says no, confirm SDR location and end

### Pass Criteria

- [ ] Offer to create stories is presented after commit
- [ ] If yes: `momentum:create-story` or `momentum:intake` is invoked per decision
- [ ] If no: skill completes cleanly with SDR path and index confirmation

---

## Eval 7: Skill Invocability (AC1)

### Verification

Read `skills/momentum/skills/decision/SKILL.md` and verify:

- [ ] Valid frontmatter with name, description, model, effort
- [ ] description is under 150 characters
- [ ] Body delegates to `./workflow.md`
- [ ] No inline workflow logic in SKILL.md body (delegation only)

---

## Eval 8: Flow D — Developer-Originated Decision Capture

### Intent

Verify that momentum:decision correctly handles Flow D (developer-proposed decisions from conversation, not from a source document) with appropriate SDR output.

### Pass Criteria

- [ ] Flow D option is presented in Step 1's ask
- [ ] Developer's verbal decision description is captured into discrete decision items
- [ ] `{{source_research}}` is populated with `[{path: "(conversation)", type: developer-conversation, date: today}]`
- [ ] SDR D-sections for Flow D use `**Developer framing:**` instead of `**Research recommended:**`
- [ ] Walk-through captures rationale per decision the same way as Flows A/B/C
- [ ] SDR is written to the decisions directory using the standard filename convention
- [ ] Index update and commit steps proceed unchanged

### Anti-patterns

- Forcing Flow D into Flow B by asking for a source path
- Leaving `source_research` empty or populating with a fabricated document path
- Using `Research recommended:` for a Flow D SDR — misleading because there is no research source
