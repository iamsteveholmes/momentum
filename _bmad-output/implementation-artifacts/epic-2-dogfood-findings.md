# Epic 2 Dogfood Findings

Observed during live testing of `/momentum` in ~/projects/nornspun after Epic 2 merge and global skill install.

Date: 2026-03-23

## Action Items

| # | Finding | Severity | Status | Fix |
|---|---------|----------|--------|-----|
| F1 | First-install greeting has no personality | High | Open | Add ASCII art/nerdfont identity, self-introduction to Steps 2, 7, 9 |
| F2 | "Momentum 1.0.0" surfaces version machinery | Medium | Open | Replace `Momentum {{current_version}}` header with Impetus voice |
| F4 | Natural language input skips confirmation | High | Open | Strengthen confirmation rule or add structural gate before dispatch |
| F5 | Ambiguous input clarification lacks numbered options | Medium | Open | Eval showed correct behavior (one question) but wrong format |
| F6 | Thread ID machinery (T-NNN) surfaced | Medium | Open | Steps 11-13 should use context_summary/story_ref, not thread_id |
| F7 | Dormant thread hygiene didn't fire | High | Open | Root cause: F9 |
| F8 | Multi-tab concurrent detection didn't fire | High | Open | Root cause: F9 |
| F9 | Step 11/12 split causes hygiene to be skipped | Critical | Open | Merge Steps 11+12: threads → hygiene → selection in one response |
| F10 | No-re-offer after decline not persisted | Medium | Open | Extend journal schema with offer/declination tracking |
| F11 | Expertise-adaptive not differentiated on repeat | Medium | Open | Track /momentum invocation count for expertise signal |
| F12 | Natural language confirmation consistently skipped | High | Open | Strengthen confirmation rule or add structural gate |

**Deferred validation — requires Epic 3/4 workflows to exercise:**

| # | Behavior | Story | Trigger |
|---|----------|-------|---------|
| V1 | Completion signal format (ownership return, file list, "what's next?") | 2.4 AC1 | Workflow completes |
| V2 | Productive waiting during background tasks | 2.4 AC2 | Background subagent dispatch |
| V3 | Subagent result synthesis (no raw JSON, severity indicators) | 2.4 AC3 | Subagent returns results |
| V4 | Hub-and-spoke contract (subagent identity hidden) | 2.4 AC4 | Subagent orchestration |
| V5 | Implementation summary at review dispatch | 2.4 AC5 | Review dispatched |
| V6 | Tiered review depth (micro-summary, quick scan, full review) | 2.4 AC6 | Review findings presented |
| V7 | Confidence-directed review | 2.4 AC7 | Review findings with spec references |
| V8 | Config gap detection | 2.5 AC3 | Missing config scenario |
| V9 | Multi-tab concurrent detection | 2.2 AC4 | Two simultaneous sessions |

**Not actionable:**
| F3 | Pre-push install served stale skills | Low | Closed | Operator error — always push before reinstall |

---

## Finding 1: First-install greeting has no personality

**Observed:** Impetus presents "Momentum 1.0.0 — first time here" followed by a bullet list of config actions. No introduction, no visual identity, no sense of meeting a practice partner.

**Expected:** Impetus should make an entrance — ASCII art or nerdfont icons, self-introduction, something memorable. The first encounter sets the tone for the entire practice.

**Root cause:** Step 2 first-install template (workflow.md line ~188) was written in Story 1.3 before Epic 2's voice rules existed. Never updated.

**Affected areas:**
- Step 2 (first-install consent)
- Step 7 (normal session menu — "You're set up and ready" is equally flat)
- Step 9 (upgrade path)

**Severity:** High — UX first impression

---

## Finding 2: "Momentum 1.0.0" surfaces version machinery

**Observed:** The greeting header is `Momentum {{current_version}} — first time here`, which renders as "Momentum 1.0.0 — first time here."

**Expected:** Voice rules (Story 2.1) say no visible machinery. Impetus should speak as itself, not announce a product version string.

**Root cause:** Same as Finding 1 — Step 2 template predates voice rules.

**Severity:** Medium — voice rule violation

---

## Finding 3: Pre-push global install served stale skills

**Observed:** Installing Momentum globally via `npx skills add` before pushing Epic 2 changes resulted in the old pre-Epic-2 workflow being served to other projects. The nornspun session showed `[S] I'll handle it manually` instead of `[Y] Yes · [N] No` because it was running the old code.

**Expected:** Skills should match the latest version. This is a deployment sequencing issue, not a code bug.

**Lesson:** Always push before reinstalling global skills. Consider adding a version check to the install process.

**Severity:** Low — operator sequencing, not a code defect

---

## Finding 4: Natural language input skips confirmation step

**Observed:** Developer typed "I want to create a story" at the menu. Impetus immediately invoked bmad-create-story without confirming intent first.

**Expected:** AC5 (Story 2.1) requires: "natural language intent extracted and confirmed before acting ('Starting story creation — correct?')". Impetus should have confirmed before dispatching.

**Root cause:** The input interpretation rules are behavioral instructions that the LLM may not follow consistently when the intent seems unambiguous. The rule is present in workflow.md but the LLM judged the intent clear enough to skip confirmation.

**Severity:** High — violates AC5, could dispatch wrong workflow

---

## Finding 5: Ambiguous input clarification lacks numbered options

**Observed:** Developer typed "that one" after an interrupt. Impetus asked one clarifying question (correct per AC5) but phrased it as "is that the one, or did you have a different story in mind?" instead of presenting numbered options.

**Expected:** AC5 says "ambiguous input triggers exactly one clarifying question" and the input interpretation rule says "presented as numbered options." Should have been: "Which one — 1. Create a story, 2. Develop a story, 3. ..."

**Root cause:** The behavioral instruction says "numbered options" but the LLM inferred story context from the previous action rather than falling back to the menu items.

**Severity:** Medium — correct behavior (one question) but wrong format (no numbered options)

---

## Finding 6: Thread ID machinery surfaced in responses

**Observed:** Impetus says "T-002 is 4 days dormant" and the progress indicator shows "T-002 WebSocket research." The T-NNN thread ID is internal journal machinery.

**Expected:** Voice rules say no visible machinery — no internal names, no agent names, no tool names. Thread IDs are internal identifiers for the journal system, not user-facing labels.

**Root cause:** The session orientation and progress indicator steps reference thread_id from journal entries without translating to user-friendly labels. The journal schema uses T-NNN IDs for internal tracking, but Impetus should present threads by their context_summary or story_ref, not their ID.

**Severity:** Medium — voice rule violation, consistent across thread display and progress indicator

---

## Finding 7: Dormant thread hygiene didn't fire proactively

**Observed:** T-002 (WebSocket research) is 4 days dormant (>3 day threshold). Step 12 (thread hygiene) should have surfaced it with a one-action closure offer *before* waiting for thread selection. Instead, dormancy was only noted after the developer explicitly selected the thread.

**Expected:** AC5 (Story 2.2): "Impetus surfaces the dormant thread with brief context and offers one-action closure" at session start, before the developer makes a selection.

**Root cause:** The LLM appears to have gone from Step 11 (display threads) directly to waiting for input, skipping Step 12 (hygiene checks). The workflow says "GOTO step 12" after Step 11 but the LLM may have treated the thread display + prompt as a natural stopping point.

**Severity:** High — AC5 behavior not triggered, dormant threads accumulate silently

---

## Finding 8: Multi-tab concurrent detection not tested but T-001 was recent

**Observed:** T-001 was timestamped ~5 minutes ago (within the 30-minute window for AC4 concurrent detection). Impetus did not flag it as potentially active in another tab.

**Expected:** AC4 (Story 2.2): "if the entry was timestamped within the last 30 minutes, Impetus flags it as likely intentional concurrent work."

**Root cause:** Same as Finding 7 — Step 12 hygiene checks appear to have been skipped entirely. The concurrent detection, dormant hygiene, and dependency notification all live in Step 12.

**Severity:** High — AC4 behavior not triggered

---

## Finding 9: Step 11/12 split causes hygiene checks to be skipped entirely

**Observed:** Step 12 (thread hygiene — concurrent detection, dormant closure, dependency notification, unwieldy triage) never fires. The LLM renders Step 11's thread list with the question "Continue (1/2/...) or tell me what you need?" and stops to wait for the developer's response. The developer answers before the LLM reaches Step 12.

**Root cause:** Step 11 contains an `<output>` with an interactive question, then says `GOTO step 12`. But the LLM treats the question as a natural interaction point and waits for input. Step 12 never executes because the developer responds to Step 11's question first.

**Fix:** Merge Steps 11 and 12 so that thread display → hygiene warnings → selection prompt all render in a single Impetus response. The developer should see: threads, then any hygiene alerts (dormant, concurrent, dependency, unwieldy), THEN the selection question. This is the only way to guarantee hygiene checks fire before the developer makes a selection.

**Impact:** This is the root cause of Findings 7 and 8. Fixing this one issue resolves AC4 (concurrent), AC5 (dormant), AC6 (dependency notification), and AC7 (unwieldy triage) simultaneously.

**Severity:** Critical — blocks 4 ACs (AC4, AC5, AC6, AC7)

---

## Finding 10: No-re-offer after decline not persisted across sessions

**Observed:** Declined dormant thread closure in session 2. Re-invoked `/momentum` in session 3. Dormant thread closure was re-offered.

**Expected:** AC5 (Story 2.5): "Record declination in journal thread state... do not re-surface the same offer unless context has materially changed."

**Root cause:** The decline was ephemeral — only in conversation context. The no-re-offer rule requires writing the declination to journal.jsonl, but the workflow didn't write a declination entry. The journal only tracks thread state (open/closed), not offer history.

**Fix:** Either extend the journal schema with an `offers` field to track declined proactive offers per thread, or add a separate declination log that the hygiene step checks.

**Severity:** Medium — AC5 behavior not persistent

---

## Finding 11: Expertise-adaptive abbreviation not clearly differentiated

**Observed:** Second invocation of `/momentum` didn't visibly differ from the first in orientation style. No "Full walkthrough or just the decision points?" offer was made.

**Expected:** AC6 (Story 2.5): "Repeat encounter = abbreviated — present current state and decision points directly. May ask 'Full walkthrough or just the decision points?'"

**Root cause:** The LLM may not have access to cross-session history to know this is a repeat encounter. The journal tracks workflow threads, not `/momentum` invocation history. Without a record of prior completions, the expertise-adaptive check has no signal.

**Fix:** Track `/momentum` invocation count in installed.json or a separate counter, so the expertise-adaptive check has a concrete signal.

**Severity:** Medium — AC6 behavior not differentiated

---

## Finding 12: Natural language confirmation consistently skipped

**Observed:** Second test — "yeah let's pick up the test infra work" went directly to thread 1 resumption without confirming "Resuming d1-1b test infrastructure — correct?" Same behavior as Finding 4.

**Expected:** AC5 (Story 2.1): Natural language intent extracted and confirmed before acting.

**Root cause:** The LLM treats unambiguous intent as not needing confirmation. The input interpretation rule says to confirm, but when intent is clear, the LLM optimizes by skipping. This is a consistent behavioral compliance issue — the rule needs to be stronger or structurally enforced.

**Severity:** High — consistent AC5 violation across multiple tests

---

## Findings from successful validation

The following Epic 2 behaviors were confirmed working:

- **Story 2.1 AC2:** Menu displays with Response Architecture Pattern (orientation → menu → user control)
- **Story 2.1 AC3:** Voice rules followed — no generic praise, no step counts, narrative orientation
- **Story 2.2 AC3:** Empty journal path — skipped thread display, transitioned to menu
- **Story 2.5 AC6:** Expertise-adaptive — detected first encounter, delivered full walkthrough
- **Story 2.1 AC1:** Impetus speaks first — menu presented without developer prompting
- **First-install flow:** Complete execution — rules written, hooks configured, state files created, hash computed
- **Story 2.2 AC2:** Journal display — numbered thread list with phase and elapsed time, ordered by most-recently-active
- **Story 2.2 AC8:** Workflow resumability — re-oriented from journal context, offered "continue or restart?"
- **Story 2.3 AC1:** Progress indicator — 3-line format with ✓/→/◦, collapsed correctly
- **Story 2.3 AC4:** Symbol vocabulary — symbols paired with text
- **Story 2.3 AC7:** On-demand "where am I?" — returned visual progress indicator
- **Story 2.1 AC5 (partial):** Number input selects item without confirmation (worked for thread selection)
- **Hash drift check:** Computed hash matched stored hash, no false alarm
- **Story 2.2 AC5 (partial):** Dormant hygiene fired on second run — offered closure for 4-day dormant thread
- **Story 2.2 AC6:** Dependency notification — surfaced "Thread 2 waiting on Thread 1"
- **Story 2.2 Steps 11+12:** Combined display — threads, hygiene, selection all in one response (second run)
- **Story 2.2 Step 14:** Journal write protocol — append-only closure entry, journal-view.md regenerated
- **Story 2.5 AC1:** JIT spec contextualization — surfaced architecture decision inline with source reference
- **Story 2.5 AC2:** Follow-up as discovery — read 26 tool uses exploring architecture before answering
- **Story 2.5 AC7:** Motivated disclosure — framed why the spec decision matters to the current thread
- **Story 2.5 AC4:** Proactive offer — used ? symbol to offer thread closure based on spec discovery
- **Story 2.1 fuzzy continue:** "yeah let's pick up the test infra work" correctly mapped to thread 1

## Untested behaviors

These require deeper workflow execution (subagent dispatch, background tasks, review cycles) that a dogfood session through `/momentum` orientation alone cannot exercise:

- **Story 2.4 AC1:** Completion signal format (ownership return, file list, "what's next?")
- **Story 2.4 AC2:** Productive waiting during background tasks
- **Story 2.4 AC3:** Subagent result synthesis (no raw JSON, severity indicators)
- **Story 2.4 AC4:** Hub-and-spoke contract (subagent identity hidden)
- **Story 2.4 AC5:** Implementation summary at review dispatch
- **Story 2.4 AC6:** Tiered review depth (micro-summary, quick scan, full review)
- **Story 2.4 AC7:** Confidence-directed review
- **Story 2.5 AC3:** Config gap detection (need missing config scenario)
- **Story 2.2 AC4:** Multi-tab concurrent detection (need two simultaneous sessions)

These will be naturally exercised when Epic 3/4 workflows (story cycles, code review) run through Impetus.
