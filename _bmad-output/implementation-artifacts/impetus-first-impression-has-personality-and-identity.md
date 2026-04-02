# Story 2.8: Impetus First Impression Has Personality and Identity

Status: done

## Story

As a developer invoking `/momentum` for the first time,
I want Impetus to introduce itself with personality and visual identity,
so that my first encounter feels like meeting a practice partner — not reading a configuration script.

## Acceptance Criteria

1. **Given** a developer invokes `/momentum` for the first time (first-install path, Step 2), **When** Impetus presents the consent summary, **Then** the greeting includes a visual identity element (ASCII art, nerdfont icon, or equivalent) and a brief self-introduction that establishes Impetus as a practice partner — not a configuration script
2. **Given** any Impetus greeting (Steps 2, 7, 9), **When** a version number would have appeared, **Then** no version string, variable interpolation (`{{current_version}}`), or machinery is visible. Impetus speaks in its own voice.
3. **Given** the developer has completed setup and reaches the session menu (Step 7, zero-thread path), **When** Impetus presents the menu, **Then** the opening line has voice and personality consistent with the first-encounter greeting — not a flat "You're set up and ready"
4. **Given** the upgrade path (Step 9), **When** Impetus presents the upgrade summary, **Then** the presentation uses Impetus voice, not a mechanical version-diff format

## Tasks / Subtasks

- [x] Task 1: Replace Step 2 first-install consent template with voice-compliant greeting (AC: #1, #2)
  - [x] 1.1: Remove ALL `{{current_version}}` interpolation from Step 2 output templates. Three instances removed.
  - [x] 1.2: Add ASCII art MOMENTUM logo at top of first-install greeting (both branch).
  - [x] 1.3: Add self-introduction: "I'm Impetus — your practice partner. I handle the engineering discipline so you can focus on building."
  - [x] 1.4: Rewrite consent body for all three conditional branches in Impetus guide voice. Factual content preserved, `[Y] Yes · [N] No` and `Set up now?` preserved.
  - [x] 1.5: Replace `Setting up Momentum {{current_version}}...` with `Setting things up...` in Step 3.

- [x] Task 2: Replace Step 7 zero-thread session menu opening with voice-compliant greeting (AC: #3)
  - [x] 2.1: Replace "You're set up and ready." with "Everything's in place — let's build something."
  - [x] 2.2: Menu items and closing question left unchanged.

- [x] Task 3: Replace Step 9 upgrade templates with voice-compliant presentation (AC: #2, #4)
  - [x] 3.1: Removed all 4 `{{version_entry.version}}` from user-facing headers.
  - [x] 3.2: Replaced "Momentum {{version_entry.version}} is available." with "Some things have evolved since your last session." Version numbers preserved in per-group detail lines.
  - [x] 3.3: Replaced progress/completion with "Applying updates..." and "All caught up — latest practice updates are in place."
  - [x] 3.4: Rewritten error output in Impetus voice while preserving version numbers for diagnostics.

## Dev Notes

### Root Cause Analysis

Steps 2, 7, and 9 output templates were written in Story 1.3 (Epic 1) before Epic 2's voice rules existed. The templates use mechanical patterns:

- **`Momentum {{current_version}} — first time here`** — treats Impetus as a product label, surfaces version machinery, has no personality
- **`You're set up and ready.`** — flat orientation with zero voice character
- **`Momentum {{version_entry.version}} is available.`** — changelog-style upgrade header

Voice rules (workflow.md lines 68-77) explicitly prohibit visible machinery and require the guide's register (oriented, substantive, forward-moving). The templates violate all three qualities. Finding F2 is a direct voice rule violation (`{{current_version}}` is backstage machinery). Finding F1 is a deeper UX failure — the first encounter establishes the developer's mental model of what they're working with, and a config dump says "tool" not "partner."

### Architecture Compliance

**Voice Rules (workflow.md, lines 68-77):**
- Never surface internal names: model names, agent names, tool names, or backstage machinery
- Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, ? question — always paired with text

**Agent Voice Register (UX spec, lines 364-367):**
- Orchestrating agent (Impetus): guide's voice — oriented, substantive, forward-moving
- Impetus is the sole user-facing voice (UX spec line 370)

**Response Architecture Pattern (UX-DR15, UX spec lines 341-346):**
- Orientation line -> Substantive content -> Transition signal -> User control (always final element)
- First-install consent must follow this: identity/orientation -> what needs to happen -> consent prompt

**First-Install Design Principles (UX spec, lines 636-641):**
- Impetus never installs without consent
- Each action reported individually
- Setup failure surfaces with specific diagnosis

### File Structure Requirements

**Single file modified:** `skills/momentum/workflow.md`

All changes are to `<output>` template blocks within Steps 2, 3, 7, and 9. No structural changes to step logic, GOTOs, actions, or control flow. The step numbering is unaffected.

**Affected lines:**
- Step 2 output templates: lines 186-219 (three conditional branches)
- Step 3 progress output: line 233
- Step 7 zero-thread menu opening: lines 362-375
- Step 9 upgrade display template: lines 502-516
- Step 9 upgrade progress/completion: lines 536, 547

### Testing Requirements

This is a `skill-instruction` change — use EDD (Eval-Driven Development), not TDD. See Momentum Implementation Guide below.

### Previous Story Intelligence

**From Story 2.6 (most recent spec in Epic 2):**
- Pattern: Evals go in `skills/momentum/evals/` (established by Story 2.3)
- Voice rules: All output must synthesize in Impetus voice, never raw JSON or internal identifiers
- Anti-pattern: "Step N/M regression" — never use step counts in orientation, always narrative

**From Dogfood Findings:**
- F1 (first-install greeting has no personality) — the template `Momentum {{current_version}} — first time here` followed by a bullet list of config actions. No introduction, no visual identity, no sense of meeting a practice partner. Step 2 template was written in Story 1.3 before Epic 2's voice rules existed.
- F2 (`{{current_version}}` surfaces version machinery) — the greeting header `Momentum {{current_version}} — first time here` renders as "Momentum 1.0.0 — first time here." Voice rules say no visible machinery.
- User feedback (memory): "First-install and session greeting need personality — ASCII art, nerdfont icons, identity. Currently a lifeless config dump."

### Git Intelligence

Recent commits show dogfood validation work (ee40034 through 241354c) documenting the exact failures. The workflow.md hasn't been modified since the Epic 2 story merges. No conflicting changes expected. Story 2.6 and 2.7 touch Steps 11-13 and Step 1 respectively — no overlap with Steps 2, 3, 7, 9.

### References

- [Source: skills/momentum/workflow.md#Step 2, lines 186-230] — First-install consent templates with `{{current_version}}`
- [Source: skills/momentum/workflow.md#Step 3, line 233] — Install progress template with `{{current_version}}`
- [Source: skills/momentum/workflow.md#Step 7, lines 358-381] — Session orientation with flat "You're set up and ready"
- [Source: skills/momentum/workflow.md#Step 9, lines 484-553] — Upgrade templates with `{{version_entry.version}}` headers
- [Source: skills/momentum/workflow.md#Voice Rules, lines 68-77] — No visible machinery, guide's register
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Response Architecture Pattern UX-DR15, lines 341-346] — Orientation → Substantive → Transition → User control
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Agent Voice Register, lines 364-367] — Impetus: oriented, substantive, forward-moving
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey 0, lines 596-641] — First-install UX design with consent principles
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey 4, lines 645-695] — Upgrade journey UX design
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F1, lines 42-55] — First-install greeting has no personality
- [Source: _bmad-output/implementation-artifacts/epic-2-dogfood-findings.md#F2, lines 59-67] — Version machinery surfaces in greeting
- [Source: _bmad-output/implementation-artifacts/epic-2-refinement-proposal.md#Story 2.8, lines 126-144] — Refinement proposal with ACs

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 -> skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2-3 behavioral evals in `skills/momentum/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-first-install-personality.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify the workflow.md output templates in Steps 2, 3, 7, and 9 per Task guidance above

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match -> task complete
5. If any eval fails -> diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance note:** This story modifies only `workflow.md`, not SKILL.md. The standard SKILL.md NFR checks (description <=150 chars, model/effort frontmatter, body <=500 lines) do not apply. Verify the existing SKILL.md remains compliant after workflow changes if the overall line count of the skill package shifts.

**Additional DoD items for this story (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically)

---

### What Exists Today (Before/After Guidance)

The developer implementing this story needs to see exactly what mechanical templates exist and understand what voice-compliant replacements should look like. This section quotes the current templates verbatim and describes the transformation.

#### Step 2 — First-Install Consent (lines 186-219)

**Current template (both global + project branch, line 188):**
```
  Momentum {{current_version}} — first time here

  Before we get started, I need to configure a few things:

    · {{global_rules_count}} global rules → ~/.claude/rules/
      ({{list rule names}})
    · Enforcement hooks → .claude/settings.json
```

**Current template (project-only branch, line 197):**
```
  Momentum {{current_version}} — setting up this project

  Global rules are already installed. I just need project config:

    · Enforcement hooks → .claude/settings.json
```

**Current template (global-only branch, line 203):**
```
  Momentum {{current_version}} — setting up global rules

  Project config is already in place. I just need global rules on this machine:

    · {{global_rules_count}} global rules → ~/.claude/rules/
      ({{list rule names}})
```

**What's wrong:** All three branches open with `Momentum {{current_version}}` — a product label with version machinery. No self-introduction, no visual identity, no personality. The body reads like a package manager changelog.

**What voice-compliant looks like:** The first-install (both branch) is the developer's first encounter with Impetus. It should:
- Open with a visual identity element (ASCII art or nerdfont icon block) — something memorable that marks Impetus as a presence, not a script
- Include a one-to-two sentence self-introduction: Impetus names itself and establishes its role ("I'm Impetus — your practice partner for..." or similar)
- Frame the consent as a partner preparing the workspace, not a tool listing its install manifest
- Keep the factual content (what files, where they go) — just reframe the delivery
- No `{{current_version}}` anywhere in user-facing text

The project-only and global-only branches don't need the full visual identity (that's the first-encounter moment) but should still use Impetus voice instead of `Momentum {{current_version}}` headers.

#### Step 3 — Install Progress (line 233)

**Current template:**
```
  Setting up Momentum {{current_version}}...
```

**What's wrong:** `Momentum {{current_version}}` is version machinery.

**What voice-compliant looks like:** Impetus narrates the setup in its own voice. Something like `Setting things up...` or `Getting your workspace ready...` — no product name as header, no version string.

#### Step 7 — Zero-Thread Session Menu (lines 362-375)

**Current template:**
```
You're set up and ready.

Here's what I can help with:

  1. Create a story
  2. Develop a story
  ...

What would you like to work on?
```

**What's wrong:** `You're set up and ready.` is flat, lifeless, has zero personality. Every session starts with this line for the zero-thread path — it sets the daily tone.

**What voice-compliant looks like:** An opening line with Impetus's guide register — forward-moving, warm, brief. Not another visual identity moment (that's first-encounter only), but consistent voice character. The menu items and closing question are fine. Only the opening line needs personality.

#### Step 9 — Upgrade Templates (lines 502-547)

**Current template (upgrade summary, lines 503-516):**
```
  Momentum {{version_entry.version}} is available.

    {{group}} ({{scope}})     {{installed_group_version}} → {{version_entry.version}}
      · {{action description or target}}
    [... one line per action, grouped by component group ...]

  {{version_entry.description}}

  {{restart_notice_or_no_restart}}

  Update now?
  [U] Update · [S] Skip for now
```

**Current template (upgrade progress, line 536):**
```
  Updating to Momentum {{version_entry.version}}...
```

**Current template (upgrade completion, line 547):**
```
  Momentum is now at {{version_entry.version}}.
```

**What's wrong:** `Momentum {{version_entry.version}} is available` is a changelog header. `Updating to Momentum {{version_entry.version}}...` and `Momentum is now at {{version_entry.version}}` surface version strings as identity.

**What voice-compliant looks like:** Impetus frames the upgrade conversationally — "Some things have evolved since last time" or similar. Version numbers can appear in the per-group detail lines as factual context (e.g., `rules 1.0.0 → 1.1.0`) — the prohibition is on `Momentum X.Y.Z` as a header or identity label. Progress and completion messages use Impetus voice. The UX spec (line 649) gives the key framing: "Momentum was updated on your machine. Your project hasn't caught up yet."

---

### Verification (post-AVFL)

Adversarial subagent verification via cmux (Workspace C — isolated from other story verifications).

**Setup:**
1. `cmux new-workspace` → create isolated verification workspace
2. `cmux send --surface <X> "cd ~/projects/nornspun && npx skills update"` → pull latest momentum
3. Delete `installed.json` in nornspun to trigger first-install path
4. `cmux send --surface <X> "claude"` → launch Claude Code

**Test sequence:**
1. `cmux send` → `/momentum`
2. `cmux read-screen --lines 60` → **Assert:** visual identity element (ASCII art / nerdfont) present, self-introduction has personality, NO `{{current_version}}` or version strings
3. `cmux send` → "Y" (accept setup)
4. Wait for setup completion, `cmux read-screen` → **Assert:** Step 3 progress output has no version strings
5. Reach session menu, `cmux read-screen` → **Assert:** opening line has voice and personality, not flat "You're set up and ready"
6. **Adversarial:** Search all captured output for any remaining mechanical/lifeless language patterns, template interpolation artifacts (`{{`), or version machinery across Steps 2, 3, 7, 9

## Dev Agent Record

### Agent Model Used

claude-opus-4-6

### Completion Notes List

- All 3 `{{current_version}}` removed from Step 2 output, replaced with ASCII art identity + self-introduction (both branch) and Impetus voice (project-only and global-only branches)
- Step 3 progress output stripped of version machinery
- Step 7 zero-thread opening line replaced with forward-moving Impetus voice
- All 4 `{{version_entry.version}}` headers removed from Step 9 user-facing output; version numbers preserved only in per-group detail lines
- Error diagnostic at Step 9 rewritten in Impetus voice while retaining version numbers for troubleshooting
- 2 EDD evals written before implementation: first-install personality/identity and session-menu/upgrade voice
- EDD verification: all eval behaviors confirmed by inspection of produced output templates

### File List

- `skills/momentum/workflow.md` — Steps 2, 3, 7, 9 output templates rewritten
- `skills/momentum/evals/eval-first-install-personality-and-identity.md` — EDD eval (new)
- `skills/momentum/evals/eval-session-menu-voice-and-upgrade-voice.md` — EDD eval (new)
