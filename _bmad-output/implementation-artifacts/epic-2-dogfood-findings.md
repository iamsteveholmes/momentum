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

## Findings from successful validation

The following Epic 2 behaviors were confirmed working:

- **Story 2.1 AC2:** Menu displays with Response Architecture Pattern (orientation → menu → user control)
- **Story 2.1 AC3:** Voice rules followed — no generic praise, no step counts, narrative orientation
- **Story 2.2 AC3:** Empty journal path — skipped thread display, transitioned to menu
- **Story 2.5 AC6:** Expertise-adaptive — detected first encounter, delivered full walkthrough
- **Story 2.1 AC1:** Impetus speaks first — menu presented without developer prompting
- **First-install flow:** Complete execution — rules written, hooks configured, state files created, hash computed
