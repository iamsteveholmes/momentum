# Story 2.1: Impetus Skill Created with Correct Persona and Input Handling

Status: ready-for-dev

## Story

As a developer,
I want Impetus available as a skill with Impetus's consistent voice and clear menu,
so that I have a single, reliable orchestrating agent for every Momentum workflow.

## Acceptance Criteria

**AC1 — Skill configuration:**
Given the Momentum skills are installed,
When Claude Code starts,
Then `momentum/SKILL.md` exists with a description ≤150 characters (NFR1)
And the skill name is `momentum` (entry-point, no prefix) — all other Momentum skills are prefixed `momentum-` (NFR12)
And the skill's `model:` is set to a current Sonnet-tier model and `effort:` is `high` per the model routing guide (FR23); the specific model string is read from `references/model-routing-guide.md`, not hard-coded
And skill instructions stay under 500 lines / 5000 tokens; overflow content is in `references/` (NFR3)
And when tested by invoking `/momentum` manually alongside 68+ BMAD skills, the correct Momentum skill matches on first attempt — spot-checked during dogfooding (NFR2, NFR16)

**AC2 — Menu and Response Architecture:**
Given a developer invokes `/momentum`,
When Impetus presents its first response,
Then a numbered menu lists all available practice workflows and entry points
And the response follows the Response Architecture Pattern (UX-DR15): orientation line → substantive content → transition signal → user control
And the orientation line is narrative (never "step N/M")
And user control is always the final element and always visible

**AC3 — Impetus voice:**
Given Impetus is responding to any user action,
When formulating the response,
Then Impetus's voice is used: oriented, substantive, forward-moving (UX-DR18)
And no generic praise appears ("Great!", "Excellent!", "Sure!")
And no step counts appear ("Step 3/8")
And no agent machinery is visible — no internal names, no model references
And subagent findings are synthesized by Impetus before presenting (never raw output)
And when Impetus is uncertain, it acknowledges uncertainty explicitly rather than fabricating confidence

**AC5 — Orchestrator purity constraint:**
Given the Impetus skill implementation in `skills/momentum/workflow.md`,
When an architect or developer inspects the workflow,
Then `workflow.md` contains no code writing, test execution, eval running, code review, or findings generation logic
And all implementation work is dispatched to purpose-specific subagents (bmad-dev-story for implementation, AVFL for validation, momentum-code-reviewer for review)
And this constraint is traceable to Architecture Decision 3d (Orchestrator Purity Principle)

**AC4 — Input interpretation:**
Given a developer enters a number, letter, or natural language phrase,
When Impetus interprets input (UX-DR16),
Then a number selects the corresponding journal item or menu item
And a letter command is case-insensitive
And "continue" / "yes" / "go ahead" / "proceed" all map to C
And natural language intent is extracted and confirmed before acting ("Starting the story cycle for Story 4.2 — correct?")
And ambiguous input triggers exactly one clarifying question (never two)

## Tasks / Subtasks

- [ ] Task 1: Update `skills/momentum/SKILL.md` — correct frontmatter for persona and model routing (AC: 1)
  - [ ] 1.1: Update `model:` to `claude-sonnet-4-6` (Sonnet-tier, per model routing guide direction)
  - [ ] 1.2: Update `effort:` to `high` (Impetus = orchestrator producing outputs without automated validation — elevated effort per FR23)
  - [ ] 1.3: Create `skills/momentum/references/model-routing-guide.md` as a stub (Story 3.5 fills it out; this stub documents the current decision: Sonnet + high for Impetus)
  - [ ] 1.4: Verify description is ≤150 characters — count precisely

- [ ] Task 2: Implement the Impetus menu in `skills/momentum/workflow.md` — normal session path (AC: 2)
  - [ ] 2.1: Add the normal-session step (after install/upgrade routing passes): display numbered menu of all practice workflows
  - [ ] 2.2: Apply Response Architecture Pattern: orientation line → menu (substantive content) → transition signal → user control
  - [ ] 2.3: Menu items must cover all currently available workflows: install setup, story creation, story development, plan audit, VFL validation (stubs for later epics get placeholder entries)
  - [ ] 2.4: Ensure first response is immediate — Impetus speaks first, never waits for the user to ask

- [ ] Task 3: Implement Impetus voice rules in `skills/momentum/workflow.md` (AC: 3)
  - [ ] 3.1: Add explicit instructions banning: "Great!", "Excellent!", "Sure!", "Step N/M", raw subagent output, model/agent names
  - [ ] 3.2: Add instruction: when uncertain, surface the gap explicitly — never fabricate confidence
  - [ ] 3.3: Add instruction: synthesize subagent output into Impetus's voice before presenting (hub-and-spoke contract)

- [ ] Task 4: Implement input interpretation in `skills/momentum/workflow.md` (AC: 4)
  - [ ] 4.1: Implement number → select item (no confirmation needed)
  - [ ] 4.2: Implement letter command case-insensitivity
  - [ ] 4.3: Implement fuzzy match: "continue" / "yes" / "go ahead" / "proceed" → C
  - [ ] 4.4: Implement natural language: extract intent, confirm before acting ("Starting X — correct?")
  - [ ] 4.5: Implement ambiguous input: exactly one clarifying question (never two), presented as numbered options

## Dev Notes

### What Already Exists (Do Not Recreate)

Stories 1.1, 1.3, and 1.4 have already established:
- `skills/momentum/SKILL.md` — exists with `model: claude-opus-4-6`, `effort: normal`, description stub
- `skills/momentum/workflow.md` — exists with:
  - Step 1: startup routing (first-install → Journey 0; version mismatch → Journey 4; match → normal session)
  - Steps covering the first-install flow (Journey 0) and upgrade flow (Journey 4)
  - `references/momentum-versions.json`, `hooks-config.json`, `mcp-config.json`, `practice-overview.md`

**This story adds:** the "normal session" step to workflow.md (what happens when versions match and setup is already done), the numbered menu, the voice rules, and the input interpretation logic. It also updates the SKILL.md frontmatter.

### Task 1: Model and Effort Correction

The stub SKILL.md (from Story 1.1) set `model: claude-opus-4-6` and `effort: normal`. The AC specifies Sonnet-tier + high.

**Why Sonnet-tier (not Opus)?** The model routing guide (Story 3.5) will formally document this. The reasoning: Impetus is an orchestrator that routes to other skills and synthesizes results — it doesn't itself perform the high-stakes reasoning that triggers the cognitive hazard rule. Opus is reserved for verifier subagents (code-reviewer, architecture-guard) and VFL runs. Impetus as router/synthesizer = Sonnet is sufficient.

**Why `effort: high`?** Impetus produces outputs without automated validation (the developer is the downstream consumer). Per FR23, this qualifies for elevated effort at the Sonnet tier.

**Model routing guide stub** (`references/model-routing-guide.md`):
```markdown
# Momentum Model Routing Guide

## Current Assignments

| Skill | Model | Effort | Rationale |
|---|---|---|---|
| momentum (Impetus) | claude-sonnet-4-6 | high | Orchestrator; elevated effort for unvalidated outputs |
| momentum-vfl | claude-opus-4-6 | high | Complex parallel validation orchestration |
| momentum-code-reviewer | claude-opus-4-6 | high | Cognitive hazard rule — verifier |
| momentum-architecture-guard | claude-opus-4-6 | high | Cognitive hazard rule — verifier |
| momentum-upstream-fix | claude-opus-4-6 | high | High-stakes root cause analysis |
| momentum-create-story | claude-sonnet-4-6 | medium | Story authoring — well-validated by downstream AVFL |
| momentum-dev | claude-sonnet-4-6 | medium | Story orchestration — validated by AVFL gate |
| momentum-plan-audit | claude-sonnet-4-6 | medium | Plan classification + story creation |

Story 3.5 will elaborate this guide with the full decision framework.
```

This stub serves as the `references/model-routing-guide.md` document the AC requires. Story 3.5 fills it out fully.

[Source: epics.md#Story 2.1 AC1 note, architecture.md#Structural Patterns, FR23]

### Task 2: Normal Session Step and Menu

The normal session step is the one that runs when setup is complete and versions match. Add it as the final routing destination in workflow.md Step 1:

```
Check installed.json → exists → versions match → NORMAL SESSION (this step)
```

**Menu format (UX-DR15 Response Architecture Pattern):**

```
You're set up and ready.

Here's what I can help with:

  1. Create a story
  2. Develop a story
  3. Review a plan
  4. Run VFL validation
  5. Audit spec provenance
  6. Show session threads

What would you like to work on?
```

Design rules:
- Orientation line first: "You're set up and ready." — narrative, not "Step 1/6" or "Welcome to Momentum"
- Substantive content: the numbered menu
- Transition signal: implicit in the question ("What would you like to work on?")
- User control: always last and always visible — the question invites selection

**First response is immediate.** Impetus speaks first. The developer should never need to type a first message to get the menu.

[Source: ux-design-specification.md#Response Architecture Pattern; epics.md Story 2.1 AC2; architecture.md#Decision 4b]

### Task 3: Voice Rules Implementation

The voice rules live in the workflow.md SKILL instructions (not just metadata — they must be behavioral directives the agent follows). Example implementation language for the workflow:

```
VOICE RULES — non-negotiable for every response:
- Never: "Great!", "Excellent!", "Sure!", "Of course!", "Absolutely!" — these are filler
- Never: "Step N/M" or any numeric progress indicator — always narrative orientation
- Never: surface internal names (Claude, Sonnet, AVFL agents, VFL reviewers) to the user
- Always: synthesize subagent output before presenting — the user sees Impetus's view, not raw agent output
- Always: return agency explicitly at completion ("That's done — here's what was produced. What's next?")
- When uncertain: surface the gap ("I don't have the journal context I need here — should I assume X or ask you first?")
```

**Subagent synthesis rule (Decision 3b — Hub-and-Spoke):**
Impetus is the only agent that speaks to the user. When any subagent (VFL, code-reviewer) completes, Impetus reads the structured JSON result and reformulates it in Impetus's voice before presenting. The user never sees JSON, reviewer names, or raw agent output.

[Source: architecture.md#Decision 3b; ux-design-specification.md UX-DR18, UX-DR10]

### Task 4: Input Interpretation Rules

These rules apply throughout all Impetus interactions (not just the menu step). Implement as a standing behavioral directive in the workflow:

| Input | Behavior |
|---|---|
| `2` (number) | Select item 2 from current list — no confirmation |
| `C` or `c` | Continue — case-insensitive |
| `"continue"`, `"yes"`, `"go ahead"`, `"proceed"` | Treated as C |
| `"let's do the story"` | Extract intent → confirm: "Starting story creation — correct?" |
| `"that one"` | Ambiguous → exactly ONE clarifying question: "Which one — 1 or 3?" |
| Follow-up question | Answer the question, then return to the active step |

**Critical rule:** Ambiguous input → exactly **one** clarifying question. Never two sequential clarifying questions. If the first clarifying question is itself ambiguous, make a reasonable assumption and flag it.

[Source: ux-design-specification.md#Input Interpretation; epics.md Story 2.1 AC4; ux-design-specification.md UX-DR16]

### Symbol Vocabulary (UX-DR9)

Used throughout all Impetus responses — must be consistent:

| Symbol | Meaning |
|---|---|
| ✓ | Completed / passing |
| → | Current / active |
| ◦ | Upcoming / pending |
| ! | Warning / attention |
| ✗ | Failed / blocked |
| ? | Question / decision needed |

Symbols are always paired with text — meaning must survive any rendering context (terminal, web, export).

### NFR Compliance for SKILL.md

After Task 1 updates:
- Description ≤150 characters: must be recounted precisely after any edits
- `model: claude-sonnet-4-6`: Sonnet-tier per model routing guide
- `effort: high`: elevated effort per FR23
- Name `momentum`: bare entry-point exception (all others `momentum-[concept]`)
- workflow.md body ≤500 lines: this story adds significant content to the already-substantial workflow from Stories 1.3/1.4 — check total line count; use `references/` for overflow

### Project Structure Notes

Files modified by this story:
```
skills/momentum/
├── SKILL.md           ← UPDATE: model + effort + verify description
├── workflow.md        ← EXTEND: add normal-session menu, voice rules, input interpretation
└── references/
    └── model-routing-guide.md  ← NEW: stub (Story 3.5 fills out)
```

### Spec Fatigue Patterns

Spec fatigue mitigation patterns (UX-DR19–22) apply to all Impetus responses but are primarily exercised in Stories 2.4 (attention-aware checkpoints, confidence-directed review), 2.5 (expertise-adaptive orientation, motivated disclosure), and Epic 4 (code review findings presentation). Story 2.1 establishes the voice foundation — Impetus's narrative, synthesis-first communication style is the vehicle through which these patterns are delivered downstream. No additional ACs or tasks required here.

### References

- [Source: epics.md#Story 2.1 — Acceptance Criteria]
- [Source: epics.md#FR6, FR23 — Orchestrating Agent, Model Routing]
- [Source: epics.md#NFR1, NFR2, NFR3, NFR12 — Context/token budget, skill matching, naming]
- [Source: ux-design-specification.md#Response Architecture Pattern (UX-DR15)]
- [Source: ux-design-specification.md#Input Interpretation (UX-DR16)]
- [Source: ux-design-specification.md UX-DR18 — Impetus voice register]
- [Source: ux-design-specification.md UX-DR10 — Hub-and-Spoke Voice Contract]
- [Source: architecture.md#Decision 3b — Hub-and-Spoke Voice Contract]
- [Source: architecture.md#Decision 4b — Session Orientation Contract]
- [Source: architecture.md#Implementation Patterns — Communication Patterns, symbol vocabulary]

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD) — updating SKILL.md and extending workflow.md
- Task 1.3 → config-structure (direct) — creating `references/model-routing-guide.md` stub (reference file, not executable skill instruction)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md.** Use EDD:

**Write evals first** in `skills/momentum/evals/`:
- `eval-menu-first-response.md` — Given Impetus is invoked with no prior context, it should immediately present a numbered menu without waiting for user input; the response should follow orientation → menu → "What would you like to work on?" structure; no "Step N/M", no "Great!", no agent names
- `eval-voice-no-generic-praise.md` — Given a developer says "Thanks, that worked!", Impetus should respond without generic praise; response should be forward-moving ("What's next?" or acknowledge and offer the next step) without "Great!" or "Excellent!"
- `eval-input-fuzzy-match.md` — Given a developer types "yeah let's keep going", Impetus should interpret this as C (continue) without asking for clarification
- `eval-input-natural-language-confirm.md` — Given a developer types "I want to work on story 2.3", Impetus should extract the intent and confirm ("Starting development of Story 2.3 — correct?") before acting
- `eval-ambiguous-one-question.md` — Given a developer types "that one", Impetus should ask exactly one clarifying question with numbered options; should never ask a follow-up clarifying question

**Then implement:** update SKILL.md, extend workflow.md

**Then verify:** spawn subagent per eval, observe behavior. Max 3 fix cycles per eval.

**NFR compliance:**
- SKILL.md description ≤150 characters — recount after edits
- `model: claude-sonnet-4-6` and `effort: high` present
- workflow.md body ≤500 lines (check combined length with Stories 1.3/1.4 content; if over, extract reference content)
- Skill name `momentum` (bare exception)

**Additional DoD items:**
- [ ] 5 behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all 5 eval behaviors confirmed
- [ ] SKILL.md description ≤150 characters confirmed (count actual characters)
- [ ] `model: claude-sonnet-4-6` and `effort: high` present
- [ ] workflow.md ≤500 lines confirmed (or overflow in references/)
- [ ] `references/model-routing-guide.md` stub created
- [ ] AVFL checkpoint documented

---

### config-structure Tasks: Direct Implementation

For Task 1.3 (`model-routing-guide.md` stub):
- Write the file per the schema in Dev Notes Task 1
- This is a markdown reference file, not JSON — verify it is well-formed markdown
- No special validation needed beyond visual inspection

---

## Acceptance Test Plan

**Story type:** skill-instruction
**Verification method:** EDD — adversarial eval authoring by an independent acceptance tester
**Test artifacts location:** `skills/momentum/evals/`
**Acceptance tester:** unassigned

### Test Scenarios

The following adversarial eval scenarios are authored to attempt to demonstrate failure. The acceptance tester writes and runs these in a separate session from the developer, after implementation is complete.

1. **Eval: menu-first-response** — Given Impetus is invoked with no prior context, trigger `/momentum`. The skill must immediately present a numbered menu without waiting for user input. Response must follow orientation → menu → "What would you like to work on?" structure. Fail if: response contains "Step N/M", contains "Great!" or "Excellent!", surfaces an agent name, or waits for user to speak first.

2. **Eval: voice-no-generic-praise** — Given a developer says "Thanks, that worked!", Impetus must respond without generic praise. Response must be forward-moving. Fail if: contains "Great!", "Excellent!", "Sure!", "Of course!", or "Absolutely!".

3. **Eval: input-fuzzy-match** — Given a developer types "yeah let's keep going", Impetus must interpret this as C (continue) without asking for clarification. Fail if: asks what the user means, treats as ambiguous, or fails to continue.

4. **Eval: input-natural-language-confirm** — Given a developer types "I want to work on story 2.3", Impetus must extract intent and confirm before acting ("Starting development of Story 2.3 — correct?"). Fail if: proceeds without confirmation, or asks more than one clarifying question.

5. **Eval: ambiguous-one-question** — Given a developer types "that one", Impetus must ask exactly one clarifying question with numbered options. Fail if: asks two sequential clarifying questions, or resolves ambiguity without asking.

### Acceptance Gate

This story passes acceptance when:
- AC1: `/momentum` skill exists with description ≤150 characters, `model: claude-sonnet-4-6`, `effort: high`, name `momentum`
- AC2: First response presents numbered menu following orientation → content → transition → user control
- AC3: All 5 voice-rule evals pass (no generic praise, no step counts, no agent names)
- AC4: All input interpretation evals pass (fuzzy match, confirm before act, exactly one clarifying question)

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

### File List
