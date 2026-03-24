# Story 2.4: Completion Signals and Productive Waiting

Status: review

## Story

As a developer,
I want Impetus to surface clear completion signals and maintain dialogue during background tasks,
so that I always know when something is mine to act on and I'm never left in silence.

## Acceptance Criteria

**AC1 — Completion signal format:**
Given a story cycle, workflow, or major workflow step completes,
When Impetus delivers the Completion Signal (UX-DR5),
Then the signal contains: explicit ownership return ("this is yours to review and adjust"), a file list of what was produced with paths, and a "what's next?" question
And the developer is never left unsure whether Impetus is still working

**AC2 — Productive waiting during background tasks:**
Given Impetus dispatches a background subagent (e.g. code-reviewer, VFL),
When the subagent is running (UX-DR12),
Then Impetus maintains dialogue on the same topic — does not context-switch to unrelated subjects
And for tasks taking more than a few seconds, Impetus offers substantive discussion or an acknowledged pause
And silence (dead air) is never the response to a running background task

**AC3 — Subagent result synthesis:**
Given a subagent returns findings,
When Impetus synthesizes the result (UX-DR10),
Then Impetus's voice synthesizes the findings — raw subagent JSON or output is never presented to the developer
And severity indicators are used: `!` for critical findings, `·` for minor findings
And critical findings trigger an explicit flywheel offer when the flywheel skill is available; if Epic 6 is not yet implemented, Impetus notes the finding and logs it for later flywheel processing

**AC4 — Hub-and-spoke contract enforcement:**
Given Impetus is orchestrating any subagent,
When results arrive (UX-DR6),
Then subagent identity is never surfaced to the developer (hub-and-spoke contract maintained)
And the developer interacts only with Impetus — no awareness of which subagent ran is required
And subagents return structured JSON with at minimum `{status, result, question, confidence}` — Impetus synthesizes from this contract, not from free-form prose

**AC5 — Implementation summary at review dispatch:**
Given implementation of a story cycle or workflow step has completed and a review process is being dispatched (FR8),
When the review runs,
Then Impetus provides a human-readable summary of what was built or produced during the implementation phase
And this summary is delivered at the moment review is dispatched — the developer reads it while review runs, not after

**AC6 — Attention-aware checkpoint on findings presentation:**
Given a subagent returns findings or a workflow step completes and presents results for review,
When Impetus synthesizes the result (UX-DR19),
Then the synthesis leads with a micro-summary of key decisions and outcomes
And offers tiered review depth: quick scan (summary only), full review (expand all findings), or trust & continue
And never dumps the full artifact unprompted

**AC7 — Confidence-directed review on findings:**
Given a review finding references a specification section,
When Impetus presents the finding (UX-DR22),
Then Impetus indicates the confidence level of the referenced content (high = derived from upstream spec, medium = inferred, low = needs developer input)

## Tasks / Subtasks

- [x] Task 1: Define the Completion Signal template in `skills/momentum/references/` (AC: 1)
  - [x] 1.1: Create `skills/momentum/references/completion-signals.md` with the canonical completion signal format
  - [x] 1.2: Define the required components: ownership return phrase, artifact file list with paths, "what's next?" prompt
  - [x] 1.3: Define edge cases: workflow with no file output (e.g. configuration changes), partial completion (interrupted before finish), multi-artifact completion
  - [x] 1.4: Include the canonical example from UX spec:
    ```
    ✓  Story 4.2 complete — session journal implementation done

    What was produced:
      · src/ledger.ts — LedgerEntry type + CRUD operations
      · src/ledger.test.ts — 12 passing acceptance tests
      · .claude/rules/ledger-patterns.md — upstream fix from code review

    This is yours to review and adjust. What's next?
    ```

- [x] Task 2: Define the Productive Waiting pattern in `skills/momentum/references/` (AC: 2)
  - [x] 2.1: Add productive waiting instructions to `skills/momentum/references/completion-signals.md` (or a separate `productive-waiting.md` if it exceeds reasonable section length)
  - [x] 2.2: Define the dialogue-maintenance pattern: after dispatching a background agent (`run_in_background: true`), Impetus surfaces implementation summary or offers same-topic discussion
  - [x] 2.3: Define the acknowledged-pause pattern: when no substantive discussion is available, Impetus explicitly acknowledges the wait ("The review is running — I'll have results shortly") rather than going silent
  - [x] 2.4: Specify what "same topic" means: discussion about the work just completed, ACs being verified, architectural context, or what comes next — never unrelated subjects

- [x] Task 3: Define subagent result synthesis rules in Impetus workflow (AC: 3, 4)
  - [x] 3.1: Add synthesis instructions to `skills/momentum/workflow.md` — when subagent results arrive, Impetus reads structured JSON and synthesizes into its own voice
  - [x] 3.2: Define the subagent return contract: `{status: "complete|needs_input|blocked", result: {}, question: null|string, confidence: "high|medium|low"}`
  - [x] 3.3: Define severity indicator rendering: `!` prefix for critical/blocking findings, `·` prefix for minor/informational findings
  - [x] 3.4: Define confidence-directed synthesis: high → synthesize directly; medium → flag explicitly ("inferred — verify"); low → surface as question to user
  - [x] 3.5: Define flywheel integration: if `momentum-upstream-fix` skill exists, offer flywheel trace for critical findings; if not installed, log finding with note "flywheel processing deferred — Epic 6"
  - [x] 3.6: Enforce hub-and-spoke: never mention subagent name, tool name, or "the code reviewer said" — always "the review found" or "I found"
  - [x] 3.7: Define tiered review depth in synthesis instructions (AC: 6) — after micro-summary, offer: quick scan (summary only) / full review (expand all findings) / trust & continue. Never present full finding list as default.
  - [x] 3.8: Define confidence-level indicators on findings (AC: 7) — each finding references content with a confidence tag: high (derived from upstream spec), medium (inferred from patterns), low (needs developer input). Use natural language: "This comes directly from the architecture" vs. "Inferred — worth verifying"

- [x] Task 4: Define implementation summary at review dispatch (AC: 5)
  - [x] 4.1: Add review-dispatch summary pattern to `skills/momentum/references/completion-signals.md`
  - [x] 4.2: Define what the summary contains: files created/modified, key decisions made, how work maps to acceptance criteria, any deviations or open questions
  - [x] 4.3: Specify timing: summary is delivered at the moment the review subagent is dispatched, not after review completes — the developer reads it during the wait

- [x] Task 5: Integrate completion signals into Impetus workflow.md (AC: 1, 2, 5)
  - [x] 5.1: Add workflow step for "workflow completion" that invokes the completion signal template
  - [x] 5.2: Add workflow step for "review dispatch" that provides implementation summary then dispatches review
  - [x] 5.3: Ensure the progress indicator from Story 2.3 transitions correctly at completion: `✓ Built: [all steps]` + `→ Now: review` or final completion with no `◦ Next:` line

- [x] Task 6: Create behavioral evals (AC: 1, 2, 3, 4, 5, 6, 7)
  - [x] 6.1: `eval-completion-signal-format.md` — verify ownership return, file list, "what's next?" present
  - [x] 6.2: `eval-productive-waiting.md` — verify dialogue maintained after background dispatch, no dead air
  - [x] 6.3: `eval-subagent-synthesis.md` — verify raw JSON never shown, severity indicators used, hub-and-spoke contract maintained
  - [x] 6.4: `eval-review-dispatch-summary.md` — verify implementation summary delivered at dispatch time
  - [x] 6.5: `eval-flywheel-offer.md` — verify critical findings trigger flywheel offer (or deferred note if Epic 6 unavailable)
  - [x] 6.6: `eval-tiered-review-depth.md` — verify findings presentation offers tiered depth (quick scan / full review / trust & continue), not full dump (AC: 6)
  - [x] 6.7: `eval-confidence-directed-findings.md` — verify confidence levels indicated on findings (high/medium/low); natural language, not raw labels (AC: 7)

## Dev Notes

### Implementation Type

This is a **skill-instruction (EDD) + reference-document** story — same pattern as Stories 2.1, 2.2, and 2.3. No compiled code. Deliverables are markdown instructions and reference documents that define Impetus behavior.

### Critical Dependency: Story 2.Spike (Background Agent Coordination)

The epics define Story 2.Spike as a prerequisite: "Validate that the SendMessage API reliably supports background agent checkpoint/resume." **The spike has not been completed and no research document exists in `docs/research/`.**

However, the core ACs for this story do NOT require checkpoint/resume. They require:
- **AC2:** Maintain dialogue while background agent runs — achievable by having Impetus talk to the user after calling `Agent` with `run_in_background: true`
- **AC3/4:** Synthesize results when agent completes — the agent returns its result, Impetus processes it

The architecture already confirms: "Background execution (confirmed: Claude Code subagents explicitly support foreground/background modes)." The `run_in_background: true` parameter on the Agent tool is the mechanism.

**Recommendation:** This story can proceed without the spike. The spike's concern (checkpoint/resume mid-task) is relevant to Story 4.3 (full story cycle), not to the completion signal and synthesis patterns defined here. Flag this for the developer: implement using `run_in_background: true` + foreground dialogue, not checkpoint/resume.

### Architecture Compliance

| Requirement | Source | How This Story Complies |
|---|---|---|
| Hub-and-spoke voice contract | Decision 3b | AC4 — subagent identity never surfaces; all synthesis through Impetus voice |
| Subagent structured JSON contract | Decision 3b | AC4 — `{status, result, question, confidence}` enforced |
| Productive waiting | Decision 4c | AC2 — dead air is a failure mode; dialogue maintained on same topic |
| Visual progress format | Decision 4a | Task 5.3 — progress indicator integration at completion |
| Confidence weighting | Decision 3b | Task 3.4 — high/medium/low confidence directs synthesis behavior |
| SKILL.md ≤500 lines | NFR3 | Reference content goes in `references/`, not inline in workflow.md |

### File Structure

**Modify:**
- `skills/momentum/workflow.md` — add completion signal and productive waiting steps (keep under 500-line budget)

**Create:**
- `skills/momentum/references/completion-signals.md` — canonical completion signal format, productive waiting patterns, review dispatch summary
- `skills/momentum/evals/eval-completion-signal-format.md`
- `skills/momentum/evals/eval-productive-waiting.md`
- `skills/momentum/evals/eval-subagent-synthesis.md`
- `skills/momentum/evals/eval-review-dispatch-summary.md`
- `skills/momentum/evals/eval-flywheel-offer.md`
- `skills/momentum/evals/eval-tiered-review-depth.md`
- `skills/momentum/evals/eval-confidence-directed-findings.md`

### Previous Story Intelligence (Story 2.3)

Story 2.3 established:
- **Progress indicator format:** `✓ Built` / `→ Now` / `◦ Next` — this story must use the same format at completion boundaries
- **Symbol vocabulary:** ✓ → ◦ ! ✗ ? — this story adds `·` for minor findings (consistent with UX spec)
- **Response Architecture Pattern:** orientation → substantive → transition → user control — completion signals follow this same pattern
- **Journal integration:** workflow state stored in `journal.json` — completion signals should update journal thread status to closed
- **Evals pattern:** 5 behavioral evals in `skills/momentum/evals/` — this story follows the same pattern

### Anti-Patterns to Prevent

- **Dead air:** Never leave the user with no response while a background task runs. Even "The review is running — I'll surface results shortly" is better than silence.
- **Raw subagent dump:** Never show raw JSON, agent names, or tool names. Always synthesize.
- **Context switching:** During productive waiting, stay on the topic of the work just completed. Don't pivot to unrelated subjects.
- **Ambiguous ownership:** At completion, always say explicitly "this is yours" — the developer must know the ball is in their court.
- **Step count regression:** Never "Step 5/8 complete" — use narrative progress indicator from Story 2.3.
- **Generic praise:** No "Great work!" or "Excellent!" in completion signals — state what was done, not how the agent feels about it.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Epic 2, Story 2.4]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 3b — Hub-and-Spoke Voice Contract]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4c — Productive Waiting]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Completion Signal Component]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Productive Waiting / Long-Running Tasks]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Subagent Return Pattern]
- [Source: _bmad-output/planning-artifacts/prd.md#FR7, FR8, NFR18]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Attention-Aware Checkpoints (UX-DR19)]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Confidence-Directed Review (UX-DR22)]
- [Source: _bmad-output/implementation-artifacts/2-3-visual-progress-tracks-workflow-position.md]

## Acceptance Test Plan

**Story type:** skill-instruction
**Verification method:** EDD — adversarial eval authoring by an independent acceptance tester
**Test artifacts location:** `skills/momentum/evals/`
**Acceptance tester:** unassigned

### Test Scenarios

1. **Eval: completion-signal-format** — Given a story cycle or workflow step completes, Impetus must deliver a completion signal containing: explicit ownership return ("this is yours to review and adjust"), a file list with paths, and a "what's next?" question. Fail if: any of the three components is absent, or the developer is left uncertain whether Impetus is still working.

2. **Eval: productive-waiting** — Given Impetus has dispatched a background subagent, Impetus must maintain dialogue on the topic of the work just completed — not go silent, not switch to unrelated subjects. Fail if: Impetus produces no response after dispatching, or response changes subject.

3. **Eval: subagent-synthesis** — Given a subagent returns a structured JSON result with findings, Impetus must synthesize the findings in its own voice. Fail if: raw JSON appears in the response, a subagent name is mentioned ("the code reviewer said"), or findings appear without `!`/`·` severity indicators.

4. **Eval: review-dispatch-summary** — Given implementation completes and a review subagent is dispatched, Impetus must provide a human-readable summary of what was built at the moment of dispatch — not after the review completes. Fail if: summary is absent at dispatch time, or summary is delivered only after review results arrive.

5. **Eval: flywheel-offer** — Given a subagent returns a critical finding, Impetus must offer flywheel processing when `momentum-upstream-fix` is available. If not available, Impetus must note the finding and log it with "flywheel processing deferred — Epic 6". Fail if: critical finding is surfaced with no flywheel offer or deferral note.

6. **Eval: tiered-review-depth** — Given subagent findings arrive, Impetus must lead with a micro-summary and offer tiered depth: quick scan / full review / trust & continue. Fail if: full finding list is presented as default without offering tiers.

7. **Eval: confidence-directed-findings** — Given a finding references a specification section, Impetus must indicate confidence level in natural language: high ("This comes directly from the architecture"), medium ("Inferred — worth verifying"), low (surfaces as question). Fail if: confidence level is absent, or expressed as raw labels ("high/medium/low") rather than natural language.

### Acceptance Gate

This story passes acceptance when:
- AC1: Completion signal contains ownership return, file list with paths, and "what's next?" question
- AC2: After background dispatch, Impetus maintains on-topic dialogue — no dead air
- AC3: Subagent results synthesized in Impetus voice with severity indicators; no raw JSON or agent names
- AC4: Hub-and-spoke maintained — developer never sees subagent identity
- AC5: Implementation summary delivered at review dispatch time, not after
- AC6: Findings presentation leads with micro-summary and offers tiered review depth
- AC7: Confidence level indicated on findings in natural language

---

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Debug Log References
N/A

### Completion Notes List
- Followed EDD cycle: 7 behavioral evals written first, then reference doc and workflow extensions
- All productive waiting content consolidated in completion-signals.md (single reference doc, not split) — content fits within reasonable section length
- Workflow.md extended with steps 11-14 (completion signal, review dispatch, productive waiting, subagent synthesis) as non-linear invoke-able steps, not part of startup flow
- Workflow.md at 461 lines — within 500-line NFR3 budget
- Subagent return contract defined: `{status, result, question, confidence}` with three status values and three confidence levels
- Flywheel integration handles both available and unavailable states gracefully
- Hub-and-spoke contract enforced in both reference doc and workflow step notes
- Tiered review depth: micro-summary default, three tiers offered as natural language (not coded menu)
- Confidence-directed findings: natural language expressions, varied phrasing to avoid robotic repetition
- Story 2.Spike dependency noted but not blocking — story proceeds with `run_in_background: true` mechanism per dev notes recommendation

### File List
- `skills/momentum/references/completion-signals.md` — canonical reference for completion signals, productive waiting, subagent synthesis, review dispatch summaries, tiered review depth (NEW)
- `skills/momentum/workflow.md` — extended with steps 11-14: completion signal, review dispatch, productive waiting, subagent result synthesis (MODIFIED)
- `skills/momentum/evals/eval-completion-signal-format.md` — AC1 eval (NEW)
- `skills/momentum/evals/eval-productive-waiting.md` — AC2 eval (NEW)
- `skills/momentum/evals/eval-subagent-synthesis.md` — AC3/AC4 eval (NEW)
- `skills/momentum/evals/eval-review-dispatch-summary.md` — AC5 eval (NEW)
- `skills/momentum/evals/eval-flywheel-offer.md` — AC3 flywheel eval (NEW)
- `skills/momentum/evals/eval-tiered-review-depth.md` — AC6 eval (NEW)
- `skills/momentum/evals/eval-confidence-directed-findings.md` — AC7 eval (NEW)
- `_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md` — story file updated (MODIFIED)

### Change Log
- Created `skills/momentum/references/completion-signals.md` with 5 sections: completion signal format, productive waiting, subagent result synthesis, review dispatch summary, tiered review depth
- Extended `skills/momentum/workflow.md` with steps 11-14 covering completion signals, review dispatch, productive waiting, and subagent result synthesis
- Created 7 behavioral evals covering all 7 ACs
- Marked all tasks complete and set story status to review
