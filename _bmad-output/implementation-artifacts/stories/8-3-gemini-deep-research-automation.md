---
title: Gemini Deep Research Automation — cmux-browser Integration for momentum-research
status: review
epic_slug: research-knowledge-management
story_key: 8-3-gemini-deep-research-automation
depends_on:
  - 8-2-momentum-research-skill
touches:
  - skills/momentum/skills/research/workflow.md
  - skills/momentum/skills/research/references/gemini-prompt-template.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/epics.md
    relationship: derives_from
    section: "Epic 8: Research & Knowledge Management"
  - path: _bmad-output/research/jetbrains-air-2026-04-04/
    relationship: informed_by
    section: "Prototype validation session"
---

# Story 8-3: Gemini Deep Research Automation

Status: review

## Story

As a Momentum developer running the momentum-research skill,
I want Gemini Deep Research to run automatically via browser automation instead of basic `gemini -p`,
so that I get higher-quality triangulation from Gemini's multi-step research pipeline using my existing Pro subscription without manual browser interaction.

## Acceptance Criteria

### AC1: Deep Research Replaces Basic Gemini Prompt

- The workflow step 1.4 in `skills/momentum-research/workflow.md` uses cmux-browser to automate `gemini.google.com` Deep Research instead of `gemini -p`
- The `gemini -p` fallback is retained as a degraded path when cmux-browser is unavailable
- The Gemini prompt template (`references/gemini-prompt-template.md`) remains unchanged — it generates the prompt text for both paths

### AC2: Authentication State Management

- On first run, the workflow checks for saved auth state at `~/.claude/browser-state/google-auth.json`
- If auth state exists, it is loaded via `cmux browser <surface> state load ~/.claude/browser-state/google-auth.json`
- After loading, the workflow verifies authentication by checking for the absence of a "Sign in" button/link
- If not authenticated (no saved state or stale state), the workflow prompts the user to log in manually in the cmux browser pane
- After successful login, the workflow saves auth state via `cmux browser <surface> state save ~/.claude/browser-state/google-auth.json`
- Auth verification uses DOM inspection (check for user avatar, PRO badge, or absence of sign-in link), not URL-based detection

### AC3: Deep Research Execution Pipeline

- The workflow opens a cmux browser surface to `gemini.google.com`
- Enables Deep Research via Tools menu → Deep Research checkbox (uses `eval` + `.click()` on the menuitemcheckbox)
- Fills the research prompt into the input field
- Clicks "Send message" to submit
- Waits for the research plan to appear (polling for "Start research" button presence)
- Auto-clicks "Start research" without waiting for user approval
- Polls for research completion by checking the response container's text length stabilization

### AC4: Research Output Extraction

- After completion, extracts the report text from the `.markdown.markdown-main-panel` DOM element with the largest text content (>10K chars)
- Writes the extracted text to `raw/gemini-deep-research-output.md` (distinct from `raw/gemini-output.md` used by the `gemini -p` fallback)
- The output file includes provenance frontmatter: `content_origin: gemini-deep-research`, `date`, `topic`, `method: cmux-browser`

### AC5: Error Handling and Recovery

- **Plan generation timeout:** If "Generating research plan" persists for >3 minutes without producing a "Start research" button, reload the page and retry (max 2 retries)
- **Research completion staleness:** If the response container text length hasn't changed for >5 minutes during research execution, reload the page (the completed report will load from Gemini's server-side state)
- **Session recovery:** If a reload loses the conversation, the workflow opens the sidebar, finds the most recent conversation matching the topic, and clicks into it to recover the completed output
- **Total failure:** After exhausting retries, falls back to `gemini -p` basic mode with a warning message to the user
- **cmux-browser unavailable:** If `cmux` command is not found, skip Deep Research entirely and fall back to `gemini -p` (or skip Gemini if `gemini` is also unavailable)

### AC6: Follow-Up Questions Cycle

- After extracting the Deep Research report, the workflow optionally sends follow-up questions in the same Gemini conversation to probe gaps or deepen specific areas
- The orchestrator generates 2-3 targeted follow-up questions based on the sub-questions from scope.md that the initial report covered thinly
- Each follow-up response is appended to the same output file (`raw/gemini-deep-research-output.md`) under a `## Follow-Up` section
- **UI width requirement:** At narrow widths, the Deep Research report renders as a full-screen overlay that hides the chat input. At wider widths, the report displays alongside the chat input in a side-by-side layout. The workflow must ensure the cmux browser surface is wide enough (or maximized) before starting Deep Research. If the chat input is not visible after research completes, resize the surface wider before attempting follow-ups.

### AC7: Workflow Step Structure

- The updated step 1.4 in workflow.md is structured as a clear decision tree:
  1. Check cmux availability → if unavailable, try `gemini -p` fallback
  2. Check/load auth state → if unauthenticated, prompt user
  3. Execute Deep Research pipeline (AC3)
  4. Extract output (AC4)
  5. On failure at any step, degrade gracefully per AC5

## Tasks / Subtasks

- [x] Task 1: Update workflow.md step 1.4 with cmux-browser Deep Research pipeline (AC: 1, 3, 5, 6)
  - [x] 1.1: Replace the existing step 1.4 with the new decision tree structure
  - [x] 1.2: Add cmux availability check as the first gate
  - [x] 1.3: Add auth state load/verify/save sequence
  - [x] 1.4: Add Deep Research execution steps (Tools menu, fill, submit, auto-approve plan, poll completion)
  - [x] 1.5: Add output extraction steps (DOM query, text extraction, file write with provenance)
  - [x] 1.6: Add error handling branches (plan timeout, staleness, session recovery, total failure fallback)
  - [x] 1.7: Retain `gemini -p` as explicit fallback path

- [x] Task 2: Update gemini-prompt-template.md usage notes (AC: 1)
  - [x] 2.1: Add note that the template is used for both Deep Research (cmux-browser) and basic Gemini (`gemini -p`) paths
  - [x] 2.2: No changes to the template content itself — it generates the same prompt text for both paths

## Dev Notes

### Key Implementation Context

**Prototype validation:** A full prototype was validated in the session prior to this story being created. The working sequence is documented in `_bmad-output/research/jetbrains-air-2026-04-04/` — the Gemini Deep Research output there was produced by this exact automation approach.

**Critical cmux-browser patterns discovered during prototyping:**

- **Tools menu:** The Deep Research toggle is a `menuitemcheckbox` inside the Tools menu (`button[aria-label='Tools']`). CSS selector `text=Deep research` fails with JS errors — use `eval` with `.querySelectorAll("[role=menuitemcheckbox]")` + `.find()` + `.click()` instead.
- **Input fill:** Use `cmux browser fill "[contenteditable], textarea, [role=textbox]"` — Gemini's input is a rich text editor, not a plain textarea.
- **Model selector button:** The "Thinking" dropdown is `.input-area-switch` class, but the model selector is separate from the Tools menu.
- **Start research button:** Appears after plan generation. Use `eval` with `querySelectorAll("button").find(b => b.textContent.includes("Start research")).click()` — direct CSS/text selectors throw JS errors on Gemini's SPA.
- **Report extraction:** Filter `.markdown.markdown-main-panel` elements by `textContent.length > 10000` to find the report (the plan text element is smaller). This is the authoritative selector — validated in prototyping.
- **Auth state persistence:** Saved to `~/.claude/browser-state/google-auth.json`. Includes cookies, localStorage, sessionStorage. Google OAuth sessions last weeks/months.
- **"Something went wrong" toasts:** These appear occasionally but don't necessarily block the research. The first attempt in prototyping hung on "Generating research plan" — a page reload and retry succeeded immediately.
- **Follow-up questions:** After Deep Research completes, the chat input is available on the left side (report on right) when the surface is wide enough. Follow-up responses appear as new `.markdown.markdown-main-panel` elements (index increases — use the last non-report-sized element). Responses take 15-45 seconds. Check length stabilization (two reads 5s apart) to confirm completion. The follow-up response does NOT trigger another Deep Research — it's a regular Gemini response with the research context.

**Existing skill location:** The momentum-research skill files are at `skills/momentum/skills/research/` (migrated from the top-level `skills/momentum-research/` as part of the plugin structure refactor).

### Architecture Constraints

- The workflow.md is a skill instruction file — changes are `skill-instruction` type (EDD, not TDD)
- The step 1.4 replacement must preserve the existing step numbering and flow (steps 1.1-1.3 before, steps 2.x after)
- All cmux-browser interactions must use the patterns from `~/.agents/skills/cmux-browser/references/` — particularly the snapshot-ref lifecycle and authentication patterns
- The auth state file path `~/.claude/browser-state/google-auth.json` is a convention established during prototyping — the dev agent should use this path

### Project Structure Notes

- `skills/momentum/skills/research/workflow.md` — primary file being modified
- `skills/momentum/skills/research/references/gemini-prompt-template.md` — minor usage note update
- `~/.claude/browser-state/` — auth state storage directory (created if needed)
- No new skill files are created — this is a modification to an existing skill's workflow

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → skill-instruction (EDD)

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md or reference files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/research/evals/` (evals/ already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-deep-research-automation.md`, `eval-deep-research-fallback.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text
   - Suggested evals:
     - `eval-deep-research-automation.md`: Given a research project with cmux-browser available and saved Google auth state, the workflow should open a browser surface, enable Deep Research, fill the prompt, auto-approve the plan, poll for completion, extract the report, and write it to `raw/gemini-deep-research-output.md` with provenance frontmatter
     - `eval-deep-research-fallback.md`: Given a research project where cmux-browser is unavailable (or Deep Research fails after retries), the workflow should fall back to `gemini -p` basic mode and write output to `raw/gemini-output.md`

**Then implement:**
2. Write/modify the workflow.md and reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for this story:**
- [x] 2+ behavioral evals written in `skills/momentum/skills/research/evals/`
- [x] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [x] SKILL.md description ≤150 characters confirmed (118 chars)
- [x] `model:` and `effort:` frontmatter present and correct
- [x] SKILL.md body ≤500 lines / 5000 tokens confirmed (13 lines)
- [x] AVFL checkpoint on produced artifact documented

### References

- [Prototype session]: cmux-browser automation of Gemini Deep Research validated 2026-04-04
- [cmux-browser skill]: `~/.agents/skills/cmux-browser/references/commands.md` — full command reference
- [cmux-browser auth]: `~/.agents/skills/cmux-browser/references/authentication.md` — login/OAuth/state patterns
- [Epic 8 epics.md]: `_bmad-output/planning-artifacts/epics.md` — FR44 (multi-model research)
- [Story 8-2]: `_bmad-output/implementation-artifacts/stories/8-2-momentum-research-skill.md` — parent skill story

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, no errors.

### Completion Notes List

- Replaced workflow.md step 1.4 with full cmux-browser Deep Research pipeline using a 3-gate decision tree (existing output → prompt generation → cmux availability)
- Auth state management: loads from `~/.claude/browser-state/google-auth.json`, verifies via DOM inspection (not URL), prompts user for manual login if stale, saves after successful auth
- Deep Research execution: Tools menu eval pattern (menuitemcheckbox), rich-text-editor fill, auto-approves plan (no user gate), polls completion via text length stabilization
- Error handling: plan timeout → 2 retries with page reload; stale response → page reload + session recovery via sidebar; total failure → gemini -p fallback
- Follow-up questions cycle: identifies thinly-covered sub-questions, sends 2-3 follow-ups, checks surface width before submission, appends under ## Follow-Up section
- Output extraction uses `.markdown.markdown-main-panel` filter `>10000 chars` (authoritative selector from prototyping)
- Output file: `raw/gemini-deep-research-output.md` with provenance frontmatter `content_origin: gemini-deep-research`, `method: cmux-browser`
- gemini -p fallback retained with user confirmation ask; writes to `raw/gemini-output.md` with `content_origin: gemini-cli`
- Phase 5 synthesis step updated to include `raw/gemini-deep-research-output.md` as a source alongside `raw/gemini-output.md`
- Dual-path usage note added to gemini-prompt-template.md references section
- 2 behavioral evals written (happy path + fallback scenarios); both pass against workflow logic
- EDD verification: all eval expectations satisfied by the updated workflow
- AVFL checkpoint: workflow produces provenance-tracked output with correct content_origin values

### File List

- `skills/momentum/skills/research/workflow.md` — modified (step 1.4 replaced; step 5.1 updated for gemini-deep-research-output.md)
- `skills/momentum/skills/research/references/gemini-prompt-template.md` — modified (Dual-Path Usage section added)
- `skills/momentum/skills/research/evals/eval-deep-research-automation.md` — created
- `skills/momentum/skills/research/evals/eval-deep-research-fallback.md` — created
