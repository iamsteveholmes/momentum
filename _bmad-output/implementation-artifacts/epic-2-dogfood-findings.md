# Epic 2 Dogfood Findings

Observed during live testing of `/momentum` in ~/projects/nornspun after Epic 2 merge and global skill install.

Date: 2026-03-23

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
