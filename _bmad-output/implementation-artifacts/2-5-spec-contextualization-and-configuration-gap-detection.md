# Story 2.5: Spec Contextualization and Configuration Gap Detection

Status: ready-for-dev

## Story

As a developer,
I want Impetus to surface relevant spec context at the moment I need it and guide me through configuration gaps,
so that I never need to manually hunt for specs or figure out how to fix missing configuration.

## Acceptance Criteria

**AC1 — Just-in-time spec contextualization:**
Given a developer is in a workflow step that references an architectural decision, acceptance criterion, or prior choice,
When Impetus presents that step (FR10),
Then it surfaces the relevant spec context inline — file reference and key decision, not the full document
And the developer can act on the step without opening another file

**AC2 — Follow-up questions as discovery opportunities:**
Given a developer asks a follow-up question during any workflow step,
When Impetus receives the question (FR11),
Then Impetus treats it as a discovery opportunity — gathers artifact context before answering
And returns an answer grounded in the current artifact (not generic)
And if the question reveals an ambiguity or gap in the current spec, Impetus flags it explicitly ("This question reveals an ambiguity in the acceptance criteria — worth clarifying before we continue")
And after answering, re-presents the user control so the workflow continues

**AC3 — Configuration gap detection and conversational resolution:**
Given the developer's project is missing required Momentum configuration (e.g. protocol mapping undefined, MCP provider unconfigured, ATDD tool binding undefined — full example list in FR9)
When Impetus detects the gap at session start or when a workflow step encounters it (FR9),
Then Impetus surfaces the gap with a clear description of what's missing and why it matters
And guides the developer through resolution conversationally — never dumps a raw config file
And does not block other workflows while resolution is pending unless the missing config would cause data loss or irreversible action in that workflow
And blocking gaps are defined as: missing MCP server required for the next workflow step, missing write target that would silently skip a required output

**AC4 — Proactive-offer, never-block pattern:**
Given Impetus detects an information gap or a step the developer is about to skip,
When the conversational floor is open (no subagent running, no pending decision) (UX-DR8),
Then Impetus uses proactive-offer framing — offers options without blocking on a response; the developer retains the decision

**AC5 — No-re-offer after explicit decline:**
Given a developer has explicitly declined a proactive offer,
When the same or similar gap recurs (UX-DR8),
Then Impetus does not re-surface the same offer unless context changes materially

**AC6 — Expertise-adaptive orientation depth:**
Given a developer encounters a workflow step for the second or subsequent time,
When Impetus delivers orientation (UX-DR20),
Then guidance depth adapts: first encounter = full walkthrough with context, subsequent = abbreviated decision points, expert mode = minimal cue
And Impetus may ask at workflow start: "Full walkthrough or just the decision points?"

**AC7 — Motivated disclosure for spec context:**
Given Impetus surfaces spec context inline,
When delivering contextualization (UX-DR21),
Then every drill-down is framed with why it matters to the current step, not just what the spec says

## Tasks / Subtasks

- [ ] Task 1: Define spec contextualization instructions in `skills/momentum/references/` (AC: 1, 7)
  - [ ] 1.1: Create `skills/momentum/references/spec-contextualization.md` with the canonical JIT spec surfacing pattern
  - [ ] 1.2: Define the file-reference-and-key-decision format: `[Source: path/to/file.md#Section] — key decision in one sentence`
  - [ ] 1.3: Define what counts as "surfacing context inline" vs. "dumping the document": cite the decision, not the document; quote the one sentence that matters; offer a drill-down if the developer wants more
  - [ ] 1.4: Define Motivated Disclosure framing rule (UX-DR21): every context reference must be preceded by "why it matters to this step" — not just the spec content
  - [ ] 1.5: Define the drill-down pattern: when developer wants more context, Impetus expands with why-it-matters framing before presenting detail (not: "Here's the full architecture section"; but: "Event sourcing here differs from CRUD — affects migration in Story 4.3")

- [ ] Task 2: Define follow-up question handling in `skills/momentum/workflow.md` (AC: 2)
  - [ ] 2.1: Add follow-up question handling pattern: when a question arrives mid-step, Impetus reads relevant artifact before answering (not from memory)
  - [ ] 2.2: Define ambiguity detection trigger: if the question reveals a gap or contradiction in the spec, Impetus flags it explicitly with: "This question reveals an ambiguity in [acceptance criteria / architecture decision] — worth clarifying before we continue"
  - [ ] 2.3: Define re-continuation pattern: after answering a follow-up question, Impetus re-presents the user control [A/P/C or equivalent] so the workflow step does not stall
  - [ ] 2.4: Define discovery opportunity framing: answer with artifact-grounded content; no generic responses ("Generally speaking..."); if no artifact is available, say so explicitly

- [ ] Task 3: Define configuration gap detection in `skills/momentum/references/` (AC: 3, 4, 5)
  - [ ] 3.1: Create `skills/momentum/references/configuration-gap-detection.md` with the canonical gap detection pattern
  - [ ] 3.2: Define the gap inventory: protocol mapping table (FR35), MCP provider config, ATDD tool binding — these are the minimum detectable gaps; extend as FR9 is exercised
  - [ ] 3.3: Define gap surfacing format: description of what's missing + why it matters + conversational resolution offer (never raw config dump)
  - [ ] 3.4: Define blocking vs. non-blocking gap classification:
    - Blocking: missing MCP server required for next workflow step; missing write target that would silently skip a required output
    - Non-blocking: everything else — workflow continues while gap is pending resolution
  - [ ] 3.5: Define resolution conversation pattern: Impetus asks targeted questions to fill the gap (e.g. "What ATDD tool is configured for this project?" → records answer → writes config entry); developer is guided step by step, never handed a config blob
  - [ ] 3.6: Define when gap detection fires: at session start (scan installed.json and protocol mapping); at workflow step entry (detect if required config for this specific step is present)

- [ ] Task 4: Define proactive-offer and expertise-adaptive patterns in `skills/momentum/workflow.md` (AC: 4, 5, 6)
  - [ ] 4.1: Add proactive-offer pattern to workflow instructions: "when the conversational floor is open (no subagent running, no pending decision), if a gap is detected, offer — never block"
  - [ ] 4.2: Define proactive-offer format: use `?` symbol + offer framing ("I notice you're about to implement without an accepted spec. Want me to walk you through quick-spec first? Or continue as planned?")
  - [ ] 4.3: Define no-re-offer rule: if developer declines, Impetus records the declination in journal thread state; does not re-surface the same offer unless `context_changed: true` (e.g. spec was updated, story changed)
  - [ ] 4.4: Define expertise-adaptive orientation: at workflow start, Impetus detects whether this developer+workflow combination is a first encounter (full walkthrough) or repeat (abbreviated). Detection via journal thread history.
  - [ ] 4.5: Define the explicit ask: at repeat-encounter workflow start, Impetus may ask "Full walkthrough or just the decision points?" — one question, one time, not repeated within the session

- [ ] Task 5: Integrate contextualization and gap detection into Impetus workflow.md (AC: 1, 2, 3, 4, 5, 6, 7)
  - [ ] 5.1: Add `load spec-contextualization.md` reference to relevant workflow steps (step entry, step presentation)
  - [ ] 5.2: Add `load configuration-gap-detection.md` reference at session start and workflow step entry
  - [ ] 5.3: Add follow-up question handling as a top-level workflow pattern (not buried in a specific step — applies across all steps)
  - [ ] 5.4: Ensure gap detection at session start integrates with Story 2.2 journal read — both happen in the same orientation phase without duplication

- [ ] Task 6: Create behavioral evals (AC: 1, 2, 3, 4, 5, 6, 7)
  - [ ] 6.1: `eval-jit-spec-contextualization.md` — verify spec context surfaced inline (file ref + key decision), motivated disclosure framing present, developer can act without opening another file
  - [ ] 6.2: `eval-followup-question-as-discovery.md` — verify Impetus reads artifact before answering, ambiguity explicitly flagged when detected, workflow re-presented after answer
  - [ ] 6.3: `eval-config-gap-detection.md` — verify gap surfaced with description + why-it-matters, never raw config dump, blocking vs. non-blocking correctly classified
  - [ ] 6.4: `eval-proactive-offer-never-block.md` — verify offer framing used (not blocking question), developer retains decision, workflow can continue without resolution
  - [ ] 6.5: `eval-no-re-offer-after-decline.md` — verify same offer not re-surfaced after explicit developer decline
  - [ ] 6.6: `eval-expertise-adaptive-orientation.md` — verify first-encounter gets full walkthrough, repeat-encounter gets abbreviated or asks preference, no "Step N/M" framing in any mode

## Dev Notes

### Implementation Type

This is a **skill-instruction (EDD) + reference-document** story — same pattern as Stories 2.1–2.4. No compiled code. Deliverables are markdown instructions and reference documents that define Impetus behavior. Verification is adversarial eval authoring.

### Architecture Compliance

| Requirement | Source | How This Story Complies |
|---|---|---|
| FR9: configuration gap detection | PRD FR9 | AC3 — gap detection at session start and step entry; conversational resolution |
| FR10: just-in-time spec contextualization | PRD FR10 | AC1 — inline file-ref + key decision; no full-doc dumps |
| FR11: follow-up questions as discovery | PRD FR11 | AC2 — artifact-grounded answers; ambiguity flagged explicitly |
| UX-DR8: proactive-offer, never-block | UX spec UX-DR8 | AC4 — offer framing; floor-open gate; developer retains decision |
| UX-DR20: expertise-adaptive orientation | UX spec UX-DR20 | AC6 — first/subsequent/expert mode; "full walkthrough or decision points?" |
| UX-DR21: motivated disclosure | UX spec UX-DR21 | AC7 — every context reference preceded by why-it-matters framing |
| SKILL.md ≤500 lines | NFR3 | Reference content in `references/`, not inline in workflow.md |
| Visual progress format | Decision 4a | Progress indicator unchanged — this story adds references/, not new progress steps |
| Orchestrator purity | Decision 3d | Impetus surfaces context and detects gaps; does not implement or write config files directly — resolution is conversational, developer confirms each action |
| Hub-and-spoke voice | Decision 3b | AC2, AC7 — all surfaced context synthesized by Impetus; subagent outputs (if any) never shown raw |

### Configuration Gap Inventory (FR9)

The minimum gap types Impetus must detect at implementation:
- **Protocol mapping table** (FR35) — if a workflow step references a protocol type (e.g. `code-reviewer:review`) and the protocol is not bound in project config, Impetus detects this before the step executes
- **MCP provider** — if a workflow step requires an MCP server and none is configured in `.mcp.json`, gap is detected and classified blocking
- **ATDD tool binding** — if the ATDD workflow step fires and no test runner is bound, gap is detected non-blocking (unless the specific step would silently skip output)

Blocking gap definition (Decision 5c / FR9 epics):
- Missing MCP server required for the **next** workflow step → blocking
- Missing write target that would **silently skip** a required output → blocking
- All other gaps → non-blocking; workflow continues, resolution offered

### File Structure

**Modify:**
- `skills/momentum/workflow.md` — add follow-up question handling, proactive-offer pattern, expertise-adaptive orientation, gap detection integration at session start and step entry (keep under 500-line budget)

**Create:**
- `skills/momentum/references/spec-contextualization.md` — JIT spec surfacing pattern, motivated disclosure framing, drill-down pattern
- `skills/momentum/references/configuration-gap-detection.md` — gap inventory, blocking/non-blocking classification, resolution conversation pattern, detection timing
- `skills/momentum/evals/eval-jit-spec-contextualization.md`
- `skills/momentum/evals/eval-followup-question-as-discovery.md`
- `skills/momentum/evals/eval-config-gap-detection.md`
- `skills/momentum/evals/eval-proactive-offer-never-block.md`
- `skills/momentum/evals/eval-no-re-offer-after-decline.md`
- `skills/momentum/evals/eval-expertise-adaptive-orientation.md`

### Previous Story Intelligence (Stories 2.1–2.4)

Stories 2.1–2.4 established the patterns this story extends:
- **Story 2.1:** SKILL.md frontmatter, 500-line budget enforced, references/ for overflow content, model routing (sonnet/high for Impetus), named menu + user control as final element, Response Architecture Pattern (orientation → substantive → transition → user control)
- **Story 2.2:** Session journal at `.claude/momentum/journal.jsonl` (JSONL, append-only); journal read at session start; thread state tracked per thread_id; dormant thread detection; gap detection must integrate with journal read — same orientation phase, no duplication
- **Story 2.3:** Progress indicator format ✓/→/◦ (non-negotiable); symbol vocabulary (✓ → ◦ ! ✗ ? · ); orientation line is narrative, never "Step N/M"; workflow step format; evals pattern in `skills/momentum/evals/`
- **Story 2.4:** Completion signals in `references/completion-signals.md`; productive waiting in same file; subagent structured JSON contract `{status, result, question, confidence}`; synthesis in Impetus voice; hub-and-spoke enforced; tiered review depth (quick scan / full review / trust & continue)

**Key patterns to reuse, not reinvent:**
- Reference document pattern: one `references/*.md` file per concern; loaded on demand by `workflow.md`
- Eval pattern: `skills/momentum/evals/eval-[concept].md` — adversarial scenarios with explicit pass/fail criteria
- Journal thread state: use existing thread state fields; do not add new top-level journal fields
- Proactive offer symbol: `?` (already in symbol vocabulary from Story 2.3)

### Anti-Patterns to Prevent

- **Full document dump:** Never respond to a spec context request by loading the entire architecture or UX spec. Cite the one decision that matters to this step.
- **Generic answers:** When a developer asks a follow-up question, never answer from memory with "Generally speaking..." — read the artifact first.
- **Blocking on proactive offer:** If the conversational floor is not open (subagent running, pending decision), do not surface a proactive offer. Do not block workflow to present a gap that is non-blocking.
- **Repeating declined offers:** Once a developer declines a proactive offer, record it in journal thread state. Do not re-offer within the same session or across sessions unless context changes (e.g. the spec that triggered the offer was updated).
- **Raw config dump:** Never respond to a configuration gap by showing a raw JSON or YAML file. Always guide conversationally — ask, receive, record, confirm.
- **Step N/M regression:** Expertise-adaptive orientation must still use narrative progress format. "Just the decision points" means abbreviated content, not step counts.
- **Silent gap bypass:** If a missing config would cause a workflow step to silently skip a required output, this is a blocking gap — do not proceed without resolution.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Epic 2, Story 2.5]
- [Source: _bmad-output/planning-artifacts/epics.md#FR9, FR10, FR11]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 3b — Hub-and-Spoke Voice Contract]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 3d — Orchestrator Purity Principle]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4b — Session Orientation Contract]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UX-DR8 Proactive Orientation]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UX-DR20 Expertise-Adaptive Orientation]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UX-DR21 Motivated Disclosure]
- [Source: _bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md]
- [Source: _bmad-output/implementation-artifacts/2-3-visual-progress-tracks-workflow-position.md]
- [Source: _bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md]

## Acceptance Test Plan

**Story type:** skill-instruction
**Verification method:** EDD — adversarial eval authoring by an independent acceptance tester
**Test artifacts location:** `skills/momentum/evals/`
**Acceptance tester:** unassigned

### Test Scenarios

1. **Eval: jit-spec-contextualization** — Given a developer is at a workflow step that references an architectural decision or AC, Impetus must surface a file reference and key decision inline — not the full document. Must include motivated disclosure framing (why it matters to this step). Fail if: full document is dumped, no file reference is given, or why-it-matters framing is absent.

2. **Eval: followup-question-as-discovery** — Given a developer asks a follow-up question mid-step, Impetus must read the relevant artifact before answering (not answer generically). If the question reveals a spec ambiguity, Impetus must explicitly flag it. After answering, Impetus must re-present the user control. Fail if: answer is generic (no artifact cited), ambiguity not flagged when present, or workflow control not re-presented.

3. **Eval: config-gap-detection** — Given a required Momentum configuration is missing (protocol mapping, MCP provider, or ATDD tool binding), Impetus must surface the gap with a description of what's missing and why it matters. Must guide conversationally — no raw config dump. Must correctly classify blocking vs. non-blocking. Fail if: gap not surfaced, raw config shown, or blocking gap allowed to silently proceed.

4. **Eval: proactive-offer-never-block** — Given Impetus detects an information gap and the conversational floor is open, Impetus must offer using `?` symbol framing without blocking on a response. The developer must be able to decline and continue without Impetus repeating the offer in the same context. Fail if: Impetus blocks workflow on response, or offer fires while a subagent is running or a decision is pending.

5. **Eval: no-re-offer-after-decline** — Given a developer has explicitly declined a proactive offer, when the same gap recurs in the same or a subsequent session, Impetus must not re-surface the offer unless context has materially changed. Fail if: same offer re-surfaced after explicit decline with no context change.

6. **Eval: expertise-adaptive-orientation** — Given a developer enters a workflow for the second or subsequent time, Impetus must deliver abbreviated orientation (decision points, not full walkthrough) or ask "Full walkthrough or just the decision points?" at workflow start. Expert-mode response must use narrative progress format — no "Step N/M". Fail if: full walkthrough always delivered regardless of history, or step counts appear in abbreviated mode.

### Acceptance Gate

This story passes acceptance when:
- AC1: Spec context surfaced inline (file reference + key decision); developer can act without opening another file
- AC2: Follow-up questions receive artifact-grounded answers; spec ambiguities explicitly flagged; workflow control re-presented after answer
- AC3: Config gaps surfaced with description + why-it-matters; conversational resolution; blocking/non-blocking correctly classified
- AC4: Proactive offers use offer framing; only fire when conversational floor is open; developer retains decision
- AC5: Declined offers not re-surfaced without material context change
- AC6: Guidance depth adapts on repeat encounters; "full walkthrough or decision points?" offered; no step counts in any mode
- AC7: Every spec context reference framed with why-it-matters before content

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
