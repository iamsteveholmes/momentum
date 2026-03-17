# WB Prompt: Prep-Session Workflow VFL Transformation

**For:** Workflow Builder (BMB) in game-prep project
**Target:** `_bmad/_config/custom/nornspun/workflows/prep-session/`
**Action:** Convert from legacy format + transform to orchestrator pattern with VFL validation

---

## Prompt to Give the WB

Paste this when the WB asks what you want to edit. The WB will detect the workflow as non-compliant (workflow.yaml + instructions.md, no step folders) and offer to convert. Say YES to convert, and provide this as the scope for the conversion + transformation:

---

### Begin Prompt

I want to convert and transform Verdandi's prep-session workflow (`_bmad/_config/custom/nornspun/workflows/prep-session/`). This is a two-part transformation:

**Part 1: Convert** from legacy format (workflow.yaml + instructions.md) to BMAD step-file architecture. The existing instructions.md has 6 inline steps — each should become its own step file.

**Part 2: Transform** the converted workflow from a monolith (Verdandi does everything in one context) to an **orchestrator pattern** where Verdandi dispatches work to sub-agents and validates between steps using the validate-fix-loop (VFL) framework.

Here is the full specification for the transformation:

#### Architecture Change

**Before:** Verdandi generates all content in a single context (recap, analysis, scene flow, secrets) and calls the accuracy-reviewer sub-agent once at the end.

**After:** Verdandi is the orchestrator. She:
1. Dispatches each content generation step to a sub-agent
2. Runs VFL validation between steps (gate, checkpoint, or full depending on the step)
3. Handles the fix loop if validation finds issues (sends findings back to the generating sub-agent)
4. Presents the final assembled document to the Spinner

Verdandi does NOT generate content herself. She coordinates, validates, and communicates.

#### Step-by-Step Specification

**Step 1: Context Loading** (currently instructions.md step 1)
- **Sub-agent:** Haiku, effort low — extracts structured data from tracker.json, loads chapter, loads NPC profiles. Returns a structured context object (campaign summary, last session events, upcoming chapter content, NPCs, encounters).
- **VFL validation after:** Gate profile — structural check. Do all referenced files exist? Are required fields present in tracker? Is the chapter loaded? This is deterministic — Haiku can validate it.
- **Verdandi's role:** Greet the Spinner (in character), present the context summary, ask if ready to proceed. She reads the sub-agent's structured output and presents it warmly.

**Step 2: Recap Generation** (currently instructions.md step 2)
- **Sub-agent:** Sonnet, effort high — generates the "When Last Our Heroes Met..." read-aloud recap. Receives: last session events from the context object + flavor.md for tone guidance. Persona: dramatic storyteller voice (not Verdandi's voice — this is player-facing narration).
- **VFL validation after:** Checkpoint profile — this is the FIRST INTERPRETATION step. Source material (session capture) is first transformed into derived creative content. 73% error propagation risk starts here.
  - **Factual Accuracy lens:** Do the events in the recap match session[-1] from tracker.json? No fabricated events?
  - **Domain lens (Player Knowledge — CRITICAL):** Does the recap contain ONLY information the party knows? No GM secrets leaked? This is category D from the accuracy-reviewer — the most dangerous error type for session preps.
  - **Validator model:** Sonnet, medium effort. Source material = tracker.json session[-1] + chapter (to check what's secret vs known).
  - **If checkpoint fails:** Send findings back to the Sonnet recap sub-agent for one fix attempt. If still failing, present findings to Spinner for manual review.

**Step 3: Content Analysis** (currently instructions.md step 3)
- **Sub-agent:** Sonnet, effort medium — analyzes the current chapter and identifies all content types (NPCs, combat encounters, social encounters, exploration, puzzles, subsystem mechanics). Assesses session scope and pacing. Returns a structured analysis.
- **VFL validation after:** Gate profile — structural completeness check. Are all content types from the chapter accounted for? Is anything quietly omitted from the analysis?
  - **Validator model:** Haiku, low effort. Check the analysis against the chapter file to verify nothing was missed.

**Step 4: Scene Flow Generation** (currently instructions.md step 4)
- **Sub-agent:** Sonnet, effort high — generates the scene-by-scene flow with NPC tables, challenges, PC integration, likely outcomes, GM notes. This is the most complex content generation step. Receives: context from step 1, analysis from step 3, NPC profiles, chapter content.
- **VFL validation after:** Checkpoint profile — this is the PENULTIMATE step. Late-stage errors are 3.5x more damaging.
  - **Factual Accuracy lens:** NPC attributes match profiles? Character names/classes/levels correct?
  - **Domain Fitness lens (PF2e rules):** Game math correct? DCs level-appropriate? Encounter XP budgets right? Action economy works? Creature abilities match stat blocks?
  - **Domain Fitness lens (Campaign):** Temporal coherence — no events from future chapters? NPC relationships accurate per tracker?
  - **Validator model:** Sonnet, medium effort. Source material = NPC profiles + creature JSONs + chapter + tracker.
  - **If checkpoint fails:** Send findings back to the Sonnet scene generator for one fix attempt.

**Step 5: Floating Secrets & GM Notes** (currently instructions.md step 5)
- **Sub-agent:** Sonnet, effort medium — compiles floating secrets, foreshadowing, PC-specific opportunities, and GM notes. Receives: context, chapter, character profiles.
- **VFL validation after:** Gate profile — cross-reference integrity check. Do all secrets reference real entities? Do PC names match the party? Do referenced scenes exist in step 4 output?
  - **Validator model:** Haiku, low effort. Structural cross-reference check.

**Step 6: Assembly, Final Validation & Output** (currently instructions.md step 6)
- **Verdandi assembles** the outputs from steps 2, 4, and 5 into the session prep template.
- **VFL validation:** Full profile — dual-reviewer on the assembled document.
  - **Reviewer 1 (Enumerator framing):** The existing `nornspun-accuracy-reviewer` sub-agent. It already uses read-only tools (Read, Grep, Glob) and systematically checks categories A-J. This IS the Enumerator — keep it exactly as it is.
  - **Reviewer 2 (Adversary framing):** A new reviewer — same domain expertise but intuitive/holistic framing. Reads the full prep as a GM would. Looks for what feels off, what's suspiciously convenient, what would trip up a GM at the table. Catches things the systematic reviewer misses (narrative inconsistencies, tonal shifts, pacing problems, "would this actually work in play?").
  - **Consolidation:** Verdandi consolidates findings. Both found it → HIGH confidence (must fix). Only one found it → MEDIUM confidence (Verdandi investigates).
  - **Fix loop:** If score < 95, send findings to the original step's sub-agent for fixing. Re-validate. Up to 4 iterations.
  - **Validator model:** Sonnet, medium effort for both reviewers. Opus for consolidation if Verdandi is orchestrating at Opus; otherwise Sonnet.
- **On pass:** Verdandi presents the completed prep to the Spinner (in character).

#### Model Routing Summary

| Role | Model | Effort |
|---|---|---|
| Verdandi (orchestrator) | Sonnet | medium |
| Step 1 sub-agent (data extraction) | Haiku | low |
| Step 2 sub-agent (recap writing) | Sonnet | high |
| Step 3 sub-agent (content analysis) | Sonnet | medium |
| Step 4 sub-agent (scene flow) | Sonnet | high |
| Step 5 sub-agent (secrets compilation) | Sonnet | medium |
| Gate validators (steps 1, 3, 5) | Haiku | low |
| Checkpoint validators (steps 2, 4) | Sonnet | medium |
| Full reviewer 1 — accuracy-reviewer (step 6) | Sonnet | medium |
| Full reviewer 2 — adversary craft reviewer (step 6) | Sonnet | medium |
| Consolidator (step 6) | Sonnet or Opus | high |

#### Source Material Passthrough

**Critical principle from VFL:** Always pass original source material alongside derived data through the entire pipeline. Every validator at every stage should check against original ground truth, not just the previous step's output.

For this workflow, the source material is:
- `tracker.json` — session history, world state, open threads
- Current chapter markdown — what's coming
- NPC profiles — canonical NPC data
- Character profiles — canonical PC data
- `flavor.md` — campaign tone
- Creature/subsystem JSONs — canonical game mechanics

These should be available to every validator, not compressed into intermediate summaries.

#### Existing Sub-Agent to Integrate

The `nornspun-accuracy-reviewer` already exists at `.claude/agents/nornspun/accuracy-reviewer.md`. It:
- Has read-only tools (Read, Grep, Glob)
- Covers 10 verification categories (A-J)
- Uses adversarial framing ("Assume errors exist. Hunt for them relentlessly.")
- Produces structured findings reports

For the full VFL at step 6, this reviewer becomes **Reviewer 1 (Enumerator framing)** — it's already systematic and exhaustive. A second reviewer with **Adversary framing** (holistic, intuitive, "does this feel right for a GM?") should be created as a companion sub-agent.

#### New Sub-Agent Needed

**PF2e Rules Reviewer** — for the Domain Fitness lens at step 4 checkpoint. Focuses exclusively on:
- Game math (DCs, XP budgets, ability modifiers)
- Action economy (3-action system, reaction timing)
- Creature stat block accuracy against building tables
- Subsystem mechanics (TP/IP thresholds, influence rules)
- Level-appropriateness of encounters

This could be a separate sub-agent at `.claude/agents/nornspun/pf2e-rules-reviewer.md` or it could be a validation focus parameter passed to the accuracy-reviewer. The WB should decide the cleaner architecture.

#### VFL Validation in the Edit Workflow Itself

Since we're eating our dog food: as the WB makes changes to this workflow during the edit process, apply appropriate VFL validation at the end of each step that modifies the document:
- After converting to step-file architecture → gate check (structural validity)
- After adding sub-agent dispatch patterns → checkpoint (do the sub-agent invocations reference real agents? are model/effort values valid?)
- After the full transformation is complete → the WB's own step-e-06 validation

#### What NOT to Change

- Verdandi's personality and communication style — she still greets the Spinner warmly, still presents results in character, still closes with personalized wisdom
- The session prep template structure — the output format stays the same
- The accuracy-reviewer's protocol — it works; we're promoting it to Reviewer 1, not rewriting it
- The campaign data model — tracker.json, chapter files, NPC profiles all stay as they are

### End Prompt

---

## Notes for Steve

1. The WB will first assess and detect non-compliance, then offer conversion. Accept the conversion path.
2. During discovery (step E-02), the WB will ask what you want to change. That's when you provide the detailed specification above (the "Step-by-Step Specification" section is the key content).
3. The WB will work through changes one at a time with your approval. The spec above tells it WHAT to build; the WB's own process handles HOW.
4. The new adversary craft reviewer sub-agent will need to be created — the WB may defer this to a separate BMB agent-builder session, or handle it inline.
5. The PF2e rules reviewer is a design decision for the WB — it might recommend folding it into the accuracy-reviewer with a validation_focus parameter rather than creating a separate agent.
