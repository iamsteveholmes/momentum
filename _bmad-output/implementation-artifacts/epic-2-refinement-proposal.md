# Epic 2 Refinement — Triage and Story Proposal

**Source:** Epic 2 dogfood validation (12 findings), AVFL integration action items (5 candidates), Epic 1 retrospective (7 items)
**Convention:** "Epic N Refinement" replaces the "Nb" suffix pattern (e.g., "Epic 1b" → "Epic 2 Refinement")
**Gate:** All stories must complete before Epic 3 implementation begins (hardens Epic 2 foundation)

---

## Triage Table

### Epic 2 Dogfood Findings (F1–F12)

| ID | Finding | Sev | Classification | Story | Reasoning |
|---|---|---|---|---|---|
| F1 | First-install greeting has no personality | High | **Refinement** | 2.8 | Voice violation — Steps 2/7/9 lack identity |
| F2 | `{{current_version}}` surfaces version machinery | Med | **Refinement** | 2.8 | Same root — mechanical templates, no voice |
| F3 | Pre-push install served stale skills | Low | **Done** | — | Operator error (closed in findings doc) |
| F4 | Natural language input skips confirmation | High | **Refinement** | 2.7 | Behavioral rule not structurally enforced |
| F5 | Ambiguous input lacks numbered options | Med | **Refinement** | 2.7 | Format compliance — same pattern as F4 |
| F6 | Thread ID machinery (T-NNN) surfaced | Med | **Refinement** | 2.6 | Output template uses `thread_id` not `context_summary` |
| F7 | Dormant thread hygiene didn't fire | High | **Refinement** | 2.6 | Root cause: F9 |
| F8 | Multi-tab concurrent detection didn't fire | High | **Refinement** | 2.6 | Root cause: F9 |
| F9 | Step 11/12 split skips hygiene | **Crit** | **Refinement** | 2.6 | Step 11 output asks for input → LLM stops → Step 12 never runs |
| F10 | No-re-offer after decline not persisted | Med | **Refinement** | 2.9 | Journal lacks offer/declination tracking |
| F11 | Expertise-adaptive not differentiated | Med | **Refinement** | 2.9 | No invocation counter for repeat detection |
| F12 | NL confirmation consistently skipped | High | **Refinement** | 2.7 | Same root cause as F4 |

### Deferred Validations (V1–V9)

| ID | Behavior | Source AC | Classification | Target |
|---|---|---|---|---|
| V1 | Completion signal format | 2.4 AC1 | **Deferred** | Epic 4 dogfood — requires workflow completion |
| V2 | Productive waiting | 2.4 AC2 | **Deferred** | Epic 4 dogfood — requires background subagent |
| V3 | Subagent result synthesis | 2.4 AC3 | **Deferred** | Epic 4 dogfood — requires subagent returns |
| V4 | Hub-and-spoke contract | 2.4 AC4 | **Deferred** | Epic 4 dogfood — requires subagent orchestration |
| V5 | Implementation summary at review | 2.4 AC5 | **Deferred** | Epic 4 dogfood — requires review dispatched |
| V6 | Tiered review depth | 2.4 AC6 | **Deferred** | Epic 4 dogfood — requires review findings |
| V7 | Confidence-directed review | 2.4 AC7 | **Deferred** | Epic 4 dogfood — requires spec references |
| V8 | Config gap detection | 2.5 AC3 | **Deferred** | Epic 3/4 dogfood — needs missing config scenario |
| V9 | Multi-tab concurrent detection | 2.2 AC4 | **Deferred** | Post-2.6 manual validation — root cause fixed by 2.6; validate then |

### AVFL Integration Candidates (AI-1–AI-5)

| ID | Item | Classification | Target |
|---|---|---|---|
| AI-1 | Spec validation at story creation | **Deferred** | Epic 4 (AVFL skill exists) |
| AI-2 | Research validation | **Deferred** | Epic 8 (Story 8.1) |
| AI-3 | Spec cascade validation | **Deferred** | Epic 5 (provenance + AVFL) |
| AI-4 | Upgrade validation | **Deferred** | Post-Epic 4 (Epic 1 enhancement) |
| AI-5 | Retrospective validation | **Deferred** | Epic 6 (Story 6.5) |

### Epic 1 Retro Items (#1–#7)

| ID | Item | Classification | Evidence |
|---|---|---|---|
| #1 | Fix `npx skills add` | **Done** | Story 1.6 completed in Epic 1b |
| #2 | Acceptance testing process | **Done** | Story 1.7 completed in Epic 1b |
| #3 | Acceptance testing standard | **Done** | Part of Story 1.7 in Epic 1b |
| #4 | Re-evaluate ATDD priority | **Done** | FR39 split documented |
| #5 | journal.json → JSONL | **Done** | Story 1.9 completed in Epic 1b |
| #6 | Run Spike 2.Spike | **Refinement** → Story 2.10 | Never executed — architecture gate (Decision 4c) violated. Must complete before Epic 4. |
| #7 | Orchestrator Purity Principle | **Done** | Story 1.8 completed in Epic 1b |

### Triage Summary

| Classification | Count | Items |
|---|---|---|
| **Refinement** | 12 | F1, F2, F4, F5, F6, F7, F8, F9, F10, F11, F12, Retro #6 |
| **Done** | 7 | F3, Retro #1–#5, Retro #7 |
| **Deferred** | 14 | V1–V9, AI-1–AI-5 |
| **Won't Fix** | 0 | — |
| **Total** | 33 | All items classified |

---

## Proposed Stories

### Story 2.6: Session Thread Display Fires Hygiene Checks Before Developer Input

**Change type:** `skill-instruction` (EDD)
**Findings addressed:** F9 (critical), F7, F8, F6
**Priority:** 1 — Critical blocker
**Dependencies:** None

Merge Steps 11 and 12 in `workflow.md` so thread display + all hygiene checks + selection prompt render in a single response. Replace `thread_id` references with `context_summary`/`story_ref` in output templates.

**Root cause:** Step 11 (line 385) outputs "Continue (1/2/...) or tell me what you need?" then GOTOs Step 12. The LLM renders the question and waits for developer input — Step 12's hygiene checks never execute.

**Acceptance Criteria:**

- **Given** open threads exist in journal.jsonl, **When** Impetus displays the session journal, **Then** thread list, hygiene warnings (concurrent/dormant/dependency/unwieldy), and selection prompt all appear in ONE response before developer input
- **Given** any thread was active within the last 30 minutes, **Then** concurrent-work warning appears inline before selection prompt (Story 2.2 AC4)
- **Given** any thread exceeds the 3-day dormancy threshold, **Then** dormant-thread closure offer appears inline before selection prompt (Story 2.2 AC5)
- **Given** any thread is displayed in output, **Then** identified by `context_summary` or `story_ref` — never by `thread_id` (T-NNN). Internal identifiers do not appear in any user-facing output.

**Verification (post-AVFL):** Adversarial subagent verification via cmux. Subagent sets up journal.jsonl with ≥2 open threads (one dormant >3d, one active <30min), invokes `/momentum` through cmux, and adversarially validates: (1) all hygiene warnings render in a single response before input prompt, (2) no T-NNN identifiers visible anywhere in output, (3) selection prompt appears after warnings not before. Subagent attempts to trigger the original failure mode (Step 11 stopping before hygiene).

**Touches:** `skills/momentum/workflow.md` Steps 11, 12, 13

---

### Story 2.7: Natural Language Input Confirmed Before Workflow Dispatch

**Change type:** `skill-instruction` (EDD)
**Findings addressed:** F4, F12, F5
**Priority:** 2 — High severity
**Dependencies:** None (independent of 2.6)

Strengthen the Input Interpretation behavioral pattern in `workflow.md` so that natural language intent triggers a mandatory confirmation step with a structural gate before any workflow dispatch. Ensure ambiguous input clarification uses numbered options per existing rule.

**Root cause:** Line 85 states "extract intent and confirm before acting" but this behavioral instruction is optimized away by the LLM when intent seems clear. Needs structural enforcement (explicit MUST language + gate pattern).

**Acceptance Criteria:**

- **Given** a developer types natural language at any menu or thread selection prompt, **When** Impetus interprets the input as a workflow dispatch intent, **Then** Impetus presents a confirmation with the extracted intent and waits for explicit yes/no before dispatching (e.g., "Starting development of Story 2.3 — correct?")
- **Given** the developer has confirmed intent, **When** confirmation is received, **Then** Impetus dispatches to the identified workflow. The confirmation is exactly one exchange, not a multi-turn dialog.
- **Given** a developer types ambiguous input at any prompt, **When** Impetus cannot resolve to a single action, **Then** Impetus presents exactly ONE clarifying question with numbered options (not open-ended phrasing)
- **Given** the confirmation and clarification rules in the BEHAVIORAL PATTERNS section, **Then** the rules include explicit MUST language and a structural gate pattern (e.g., "before any GOTO to a workflow step, MUST confirm if input was natural language")

**Verification (post-AVFL):** Adversarial subagent verification via cmux. Subagent invokes `/momentum` through cmux and tests input handling adversarially: (1) types natural language intent ("yeah let's pick up the test infra work") — must get confirmation before dispatch, (2) types ambiguous input — must get numbered options, (3) types a number — must select directly without confirmation, (4) tries edge cases: very confident NL ("start story 2.6 now"), fuzzy continue phrases, mixed input. Subagent actively tries to bypass the confirmation gate.

**Touches:** `skills/momentum/workflow.md` Input Interpretation behavioral pattern + dispatch steps

---

### Story 2.8: Impetus First Impression Has Personality and Identity

**Change type:** `skill-instruction` (EDD)
**Findings addressed:** F1, F2
**Priority:** 3 — High (UX polish, no downstream deps)
**Dependencies:** None (independent)

Replace mechanical first-install templates (Steps 2, 7, 9) with voice-compliant greetings that give Impetus personality and visual identity. Remove `{{current_version}}` from user-facing headers. Add ASCII art or nerdfont-based identity element to the first-encounter path.

**Acceptance Criteria:**

- **Given** a developer invokes `/momentum` for the first time (first-install path, Step 2), **When** Impetus presents the consent summary, **Then** the greeting includes a visual identity element (ASCII art, nerdfont icon, or equivalent) and a brief self-introduction that establishes Impetus as a practice partner — not a configuration script
- **Given** any Impetus greeting (Steps 2, 7, 9), **When** a version number would have appeared, **Then** no version string, variable interpolation (`{{current_version}}`), or machinery is visible. Impetus speaks in its own voice.
- **Given** the developer has completed setup and reaches the session menu (Step 7, zero-thread path), **When** Impetus presents the menu, **Then** the opening line has voice and personality consistent with the first-encounter greeting — not a flat "You're set up and ready"
- **Given** the upgrade path (Step 9), **When** Impetus presents the upgrade summary, **Then** the presentation uses Impetus voice, not a mechanical version-diff format

**Verification (post-AVFL):** Adversarial subagent verification via cmux. Subagent deletes `installed.json`, invokes `/momentum` fresh through cmux, and adversarially checks: (1) visual identity element present in first-install, (2) self-introduction has personality (not a config script), (3) no `{{current_version}}`, version strings, or template interpolation artifacts visible, (4) zero-thread menu has voice. Subagent specifically looks for any remaining mechanical/lifeless language patterns.

**Touches:** `skills/momentum/workflow.md` Steps 2, 7, 9 output templates

---

### Story 2.9: Behavioral Persistence Across Sessions for Offers and Expertise

**Change type:** `config-structure` + `skill-instruction`
**Findings addressed:** F10, F11
**Priority:** 4 — Medium severity
**Dependencies:** Hard dependency on Story 2.6 (needs merged hygiene step to exist before adding offer tracking)

Extend the journal schema with an `offers` field to track declined proactive offers per thread, so the no-re-offer rule (UX-DR8) persists across sessions. Add an invocation counter so the expertise-adaptive pattern (UX-DR20) can distinguish first encounters from repeat encounters.

**Acceptance Criteria:**

- **Given** the developer explicitly declines a proactive offer (e.g., dormant thread closure), **When** the declination occurs, **Then** a journal entry is appended recording: what was offered, that it was declined, and the context at time of decline
- **Given** a previously declined offer exists in the journal, **When** Impetus runs hygiene checks on the next session, **Then** the same offer is not re-surfaced unless context has materially changed (spec updated, story changed, new workflow aspect)
- **Given** the developer has invoked `/momentum` in a prior session, **When** Impetus starts, **Then** a persistent counter of prior `/momentum` completions is available (in `installed.json` or journal metadata)
- **Given** the expertise counter shows ≥1 prior completion, **When** Impetus delivers session orientation, **Then** orientation is abbreviated per UX-DR20 — current state and decision points, skipping explanatory walkthrough

**Verification (post-AVFL):** Adversarial subagent verification via cmux. Subagent runs a multi-session test through cmux: (1) invokes `/momentum`, declines a proactive offer, ends session, (2) invokes `/momentum` again, verifies declined offer is NOT re-surfaced, (3) verifies orientation is abbreviated on repeat invocation, (4) adversarially tests edge cases: does the offer reappear if context changes? Does the counter persist across sessions? Subagent tries to trigger re-offer and non-adaptive behavior.

**Touches:** `skills/momentum/references/journal-schema.md` (new `offers` field), `skills/momentum/workflow.md` (merged hygiene step, Step 7 expertise-adaptive)

---

### Story 2.10: Background Agent Coordination Mechanism Validated and Documented

**Change type:** `specification` (research spike → standard story)
**Findings addressed:** Epic 1 Retro #6, Architecture Decision 4c gate
**Priority:** 5 — Blocks Epic 4 Story 4.3
**Dependencies:** None (independent of other refinement stories)

Execute the technical spike validating whether the SendMessage API supports checkpoint/resume for background agents. Capture results as a standard research document. This was defined as Story 2.Spike but **never executed** — the architecture gate in Decision 4c was bypassed when Stories 2.4/2.5 proceeded (safely, since they don't need checkpoint/resume — Story 2.4 dev notes explain the rationale).

**Process note:** Per user feedback, spikes are now treated as standard stories so results are always captured as committed artifacts. Story 2.10 is the first spike-as-story.

**Acceptance Criteria:**

- **Given** the need for background agent communication in Story 4.3, **When** this story completes, **Then** a research document exists at `docs/research/background-agent-coordination.md` documenting: (1) whether SendMessage supports checkpoint/resume, (2) reliability/latency/context constraints if yes, (3) alternative pattern if no
- **Given** Architecture Decision 4c's implementation note ("do not implement productive waiting or background VFL execution until spike result is documented"), **When** spike results are documented, **Then** Decision 4c is updated with actual mechanism or revised approach
- **Given** Story 2.4 dev notes acknowledge the gate was not satisfied, **When** this story completes, **Then** the dev notes reference the research document

**Verification (post-AVFL):** Adversarial subagent verification — manual review (cmux not applicable for research artifact). Subagent reviews the research document adversarially: (1) checks `docs/research/background-agent-coordination.md` exists with actionable findings (not vague), (2) verifies Decision 4c in architecture.md is updated and consistent with research, (3) checks Story 2.4 dev notes cross-reference, (4) adversarially challenges: are the findings reproducible? Does the document cover failure modes? Would a developer have enough info to implement Story 4.3?

**Touches:** `docs/research/background-agent-coordination.md` (new), `_bmad-output/planning-artifacts/architecture.md` (Decision 4c update), `_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md` (cross-reference)

---

## Deferred Items → Future Epic Mapping

| Item | Target | Rationale |
|---|---|---|
| V1–V7 | Epic 4 dogfood | Require subagent dispatch, review cycles, completion signals — only exercisable during story cycles |
| V8 | Epic 3/4 dogfood | Requires a missing-config scenario naturally arising from hook/protocol setup |
| V9 | Post-Story-2.6 manual validation | Root cause fixed by 2.6; validate manually after fix, no story needed unless defect found |
| AI-1 | Epic 4 (enhance momentum-create-story) | AVFL gate profile on new story files; requires AVFL skill (Story 4.6) |
| AI-2 | Epic 8 (Story 8.1) | Research validation via AVFL; requires multi-model research workflow |
| AI-3 | Epic 5 (provenance + AVFL) | Cascade validation on SUSPECT documents; requires provenance infrastructure |
| AI-4 | Post-Epic 4 (Epic 1 enhancement) | Upgrade safety net via AVFL gate; requires AVFL skill to exist |
| AI-5 | Epic 6 (Story 6.5) | Retrospective claim validation; requires retrospective workflow |

---

## Dependency Graph

```
Story 2.6 (F9/F7/F8/F6) ──── critical path
  │
  └──▶ Story 2.9 (F10/F11) ── hard dependency on merged hygiene step

Story 2.7 (F4/F12/F5) ─────── independent
Story 2.8 (F1/F2) ──────────── independent
Story 2.10 (Retro #6) ──────── independent (blocks Epic 4, not other 2.x stories)
```

- Stories 2.6, 2.7, 2.8, 2.10 can be created and developed in parallel
- Story 2.9 has a **hard dependency** on Story 2.6 (needs merged step structure to exist)
- Stories 2.6–2.9 must complete before Epic 3 implementation begins
- Story 2.10 must complete before Epic 4 Story 4.3 begins

---

## Recommended Story Creation Order

1. **Story 2.6** — Critical blocker, unblocks 2.9
2. **Story 2.7** — High severity, independent
3. **Story 2.8** — High severity, independent (could swap with 2.7)
4. **Story 2.9** — Medium severity, hard dependency on 2.6
5. **Story 2.10** — Blocks Epic 4; independent of other refinement stories

---

## Spec Amendments Needed

| Spec | Amendment | Scope |
|---|---|---|
| `epics.md` | Add Epic 2 Refinement section + 5 stories | Additive |
| `sprint-status.yaml` | Add story entries 2-6 through 2-10 | Additive |
| `journal-schema.md` | Add `offers` field, invocation counter | Additive (Story 2.9) |
| `architecture.md` | Decision 4c update with spike results | Substantive — mechanism decision (Story 2.10) |
| `ux-design-specification.md` | None — behaviors already specified, findings are impl gaps | — |

**Note:** No existing UX design or architecture amendments needed for Stories 2.6–2.9. The dogfood findings are implementation gaps against already-specified behaviors, not spec gaps.

---

## Process Changes

1. **Spikes as standard stories:** Spikes are now treated as standard stories with committed research artifacts. Story 2.10 is the first spike-as-story. No more informal experiments that may go uncaptured.
2. **Refinement epic naming:** "Epic N Refinement" replaces the "Nb" suffix pattern for clarity.

---

## Next Steps

After user approval of this proposal:
1. Invoke `/momentum-create-story` for each story in creation order
2. Update `epics.md` with Epic 2 Refinement section
3. Update `sprint-status.yaml` with story entries 2-6 through 2-10
