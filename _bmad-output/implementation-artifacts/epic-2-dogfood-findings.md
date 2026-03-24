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
