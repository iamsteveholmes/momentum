# Story 2.7: Natural Language Input Confirmed Before Workflow Dispatch

Status: ready-for-dev

## Story

As a developer using Momentum,
I want Impetus to always confirm my intent before dispatching a workflow when I type natural language (instead of a number or letter command),
so that I am never sent into the wrong workflow because the LLM inferred an intent I did not mean, and ambiguous input gives me numbered options to choose from.

## Acceptance Criteria

1. **Given** a developer types natural language at any menu or thread selection prompt, **When** Impetus interprets the input as a workflow dispatch intent, **Then** Impetus presents a confirmation with the extracted intent and waits for explicit yes/no before dispatching (e.g., "Starting development of Story 2.3 — correct?")
2. **Given** the developer has confirmed intent, **When** confirmation is received, **Then** Impetus dispatches to the identified workflow. The confirmation is exactly one exchange, not a multi-turn dialog.
3. **Given** a developer types ambiguous input at any prompt, **When** Impetus cannot resolve to a single action, **Then** Impetus presents exactly ONE clarifying question with numbered options (not open-ended phrasing)
4. **Given** the confirmation and clarification rules in the BEHAVIORAL PATTERNS section, **Then** the rules include explicit MUST language and a structural gate pattern (e.g., "before any GOTO to a workflow step, MUST confirm if input was natural language")

## Tasks / Subtasks

- [ ] Task 1: Strengthen the Input Interpretation behavioral pattern with MUST language and a structural gate (AC: #1, #4)
  - [ ] 1.1: In the BEHAVIORAL PATTERNS section (workflow.md line 79-88), replace the current line 85 (`- **Natural language intent:** extract intent and confirm before acting.`) with MUST-level enforcement language. New text must include: (a) the word "MUST", (b) an explicit structural gate pattern — "Before executing any GOTO or workflow dispatch triggered by natural language input, MUST first present a one-line confirmation and wait for yes/no", (c) the existing example preserved ("Starting development of Story 2.3 — correct?")
  - [ ] 1.2: Add a new rule immediately after the natural language intent rule: "**Structural gate — natural language dispatch:** When a developer's input is natural language (not a number, letter command, or fuzzy continue), the following sequence is mandatory: (1) Extract the most likely intent, (2) Present confirmation: '[extracted intent] — correct?', (3) Wait for yes/no, (4) Only on 'yes' execute the GOTO. If 'no', ask what they meant with numbered options. This gate applies at every prompt where input leads to a workflow dispatch: Step 7 menu, Step 12 thread selection, and any future interactive prompt."
  - [ ] 1.3: Strengthen the ambiguous input rule (line 86) to include MUST language and explicit numbered-options format requirement: "MUST present exactly ONE clarifying question with numbered options (e.g., '1. Create a story, 2. Develop a story, 3. Something else'). Never open-ended phrasing."
- [ ] Task 2: Add structural gate enforcement at dispatch points in workflow steps (AC: #1, #2)
  - [ ] 2.1: In Step 7 (line 358-381), after the menu `<output>` block and before/around the checks that handle developer input, add a `<note>` reinforcing the natural language gate: "If developer input is natural language (not a menu number), apply the Input Interpretation structural gate — confirm extracted intent before dispatching to any workflow."
  - [ ] 2.2: In Step 12 (Thread hygiene step, input handling at lines 440-448), after `Wait for developer input`, add a `<note>` reinforcing the gate: "If developer input is natural language (not a thread number, 'continue', or hygiene response), apply the Input Interpretation structural gate — confirm extracted intent before dispatching."
  - [ ] 2.3: Verify the gate pattern covers the "no" path — when the developer says "no" to the confirmation, Impetus must ask what they meant with numbered options (same as ambiguous input handling). This should be specified in the structural gate rule added in Task 1.2.
- [ ] Task 3: Ensure the confirmation is exactly one exchange (AC: #2)
  - [ ] 3.1: In the structural gate rule (Task 1.2), add explicit anti-pattern: "The confirmation is exactly one exchange. Do NOT ask follow-up questions after 'yes' — dispatch immediately. Do NOT ask 'are you sure?' — one confirmation is enough."
  - [ ] 3.2: Verify the existing fuzzy continue rule (line 84) is NOT affected — "yes", "go ahead", "proceed" in response to a confirmation MUST still work as confirmation (not re-trigger the gate). Add a note: "When 'yes'/'go ahead'/'proceed' is a response to a natural language confirmation prompt, it confirms the action — it does not re-trigger the gate."

## Dev Notes

### Root Cause Analysis

The defect is in the Input Interpretation behavioral pattern at workflow.md line 85:

```
- **Natural language intent:** extract intent and confirm before acting. Example: "I want to work on story 2.3" → "Starting development of Story 2.3 — correct?"
```

(Note: the full line includes the example shown above — Task 1.1 requires preserving this example during the rewrite.)

This is a behavioral instruction — it tells the LLM what to do but provides no structural enforcement. When the developer types something like "I want to create a story" or "yeah let's pick up the test infra work", the LLM judges the intent as unambiguous and optimizes away the confirmation step. This was observed consistently across multiple dogfood tests (F4 and F12).

The fix requires two layers:
1. **Stronger language:** Replace "confirm before acting" with "MUST confirm before acting" and add explicit prohibition against skipping
2. **Structural gate pattern:** Add a named, referenceable gate that dispatch steps can invoke — making the confirmation a structural part of the workflow rather than a suggestion. The gate is placed both in the behavioral pattern (global) and reinforced at each dispatch point (local).

This dual-layer approach (global rule + local reinforcement) mirrors the pattern used successfully in Voice Rules, where rules are stated once globally and reinforced at specific steps where the LLM is most likely to violate them.

### Architecture Compliance

**Input Interpretation (UX Design Specification, lines 967-978):**
- Number input: no confirmation needed (select directly)
- Letter command: no confirmation needed
- Fuzzy continue: treated as C, no confirmation needed
- Natural language: extract intent, confirm before acting
- Ambiguous: one clarifying question with numbered options

**Response Architecture Pattern (UX-DR15, UX spec lines 341-346):**
- Orientation line -> Substantive content -> Transition signal -> User control
- The confirmation prompt follows this: orientation (extracted intent) -> confirmation question (user control)

**Voice Rules (workflow.md lines 68-77):**
- Confirmation must follow Impetus voice — no generic praise, no "Sure!", just the intent and question

### File Structure Requirements

**Single file modified:** `skills/momentum/workflow.md`

The changes are confined to:
- Lines 79-88: Input Interpretation behavioral pattern (BEHAVIORAL PATTERNS section)
- Lines 358-381: Step 7 menu dispatch (add gate reinforcement note)
- Lines 440-447: Step 12 thread selection dispatch (add gate reinforcement note)

No step renumbering needed. No GOTO chain changes. This is purely additive — strengthening existing rules and adding enforcement notes at dispatch points.

### Testing Requirements

This is a `skill-instruction` change — use EDD (Eval-Driven Development), not TDD. See Momentum Implementation Guide below.

### Previous Story Intelligence

**From Story 2.6 (previous in Epic 2):**
- Pattern: Behavioral rules that the LLM can optimize away need structural enforcement — Story 2.6 solved the same class of problem (GOTO after interactive output) by merging steps
- Pattern: Evals go in `skills/momentum/evals/` (established by Story 2.3)
- Pattern: Local reinforcement at the step level works alongside global rules — Story 2.6 added voice rule reinforcement in the merged step even though the rule was already global
- Anti-pattern: Behavioral instructions without MUST language are treated as suggestions by the LLM

**From Dogfood Findings:**
- F4: "I want to create a story" -> immediately dispatched without confirmation
- F12: "yeah let's pick up the test infra work" -> immediately resumed thread without confirmation. Same pattern as F4. Consistent behavioral compliance failure.
- F5: Ambiguous input got one clarifying question (correct) but phrased as open-ended ("is that the one, or did you have a different story in mind?") instead of numbered options

### Git Intelligence

Recent commits show dogfood validation work (241354c and earlier) documenting the exact failures. The workflow.md was last modified during Epic 2 story merges. No conflicting changes expected. Story 2.6 (step merge) may touch nearby lines (Steps 11-12) — if 2.6 lands first, the step numbers and line references for Task 2.2 will shift. The behavioral pattern changes (Task 1) and Step 7 gate (Task 2.1) are independent of 2.6.

### References

- [Source: skills/momentum/workflow.md#Input Interpretation, lines 79-88] — Current behavioral pattern with weak enforcement
- [Source: skills/momentum/workflow.md#Step 7, lines 334-381] — Session orientation menu dispatch point
- [Source: skills/momentum/workflow.md#Step 12 input handling, lines 440-448] — Thread selection input handling at end of hygiene step
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Input Interpretation, lines 967-978] — UX design specification for input handling
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Uncertainty Recovery, lines 980-992] — Numbered options format for ambiguous input
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F4, lines 83-92] — Natural language input skips confirmation
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F5, lines 95-103] — Ambiguous input lacks numbered options
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F12, lines 185-193] — Confirmation consistently skipped
- [Source: _bmad-output/implementation-artifacts/epic-2-refinement-proposal.md#Story 2.7, lines 102-123] — Refinement proposal

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 -> skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2-3 behavioral evals in `skills/momentum/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-nl-confirmation-before-dispatch.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md changes (strengthen Input Interpretation rules, add structural gate, reinforce at dispatch steps)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match -> task complete
5. If any eval fails -> diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance note:** This story modifies only `workflow.md`, not SKILL.md. The standard SKILL.md NFR checks (description <= 150 chars, model/effort frontmatter, body <= 500 lines) do not apply. Verify the existing SKILL.md remains compliant after workflow changes if the overall line count of the skill package shifts.

**Additional DoD items for this story (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically)

---

### Verification (post-AVFL)

Adversarial subagent verification via cmux. Subagent invokes `/momentum` through cmux and tests input handling adversarially:
1. Types natural language intent ("yeah let's pick up the test infra work") — must get confirmation before dispatch
2. Types ambiguous input ("that one") — must get numbered options
3. Types a number ("2") — must select directly without confirmation
4. Tries edge cases: very confident NL ("start story 2.6 now"), fuzzy continue phrases ("sure", "go ahead"), mixed input ("do number 3")
5. Subagent actively tries to bypass the confirmation gate — phrasing intent as a command, using imperative voice, embedding numbers in NL

## Dev Agent Record

### Agent Model Used

### Completion Notes List

### File List
