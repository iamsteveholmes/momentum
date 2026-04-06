# Enhancement Opportunities Analysis — Impetus

**Scanner:** DreamBot (Creative Edge-Case & Experience Innovation)
**Target:** `skills/momentum/skills/impetus/`
**Date:** 2026-04-06

---

## Agent Understanding

Impetus is the Momentum practice orchestrator — the single interface a solo developer interacts with for session orientation, sprint dispatch, installation, upgrades, and thread management. It is stateless across sessions (journal.jsonl provides persistence), dispatches all real work to subagent skills, and maintains a strong identity as a "servant-partner in the KITT sense" with dry, confident personality. Key assumptions: the user is a solo developer running agentic engineering practices, the user launches sessions via `/momentum`, and all subagent dispatch follows hub-and-spoke purity (Impetus never does the work directly).

---

## User Journey Narratives

### 1. The First-Timer

**Journey:** Invokes `/momentum` for the first time. Sees ASCII art, "I am Impetus. I hold the line on engineering discipline..." Gets a consent prompt for installing rules and hooks. Likely says [Y]. Sees confirmation ticks, maybe a restart notice, then lands on the session menu.

**Bright spots:**
- The identity introduction is strong and memorable. ASCII art + self-declaration of purpose sets a tone immediately.
- Consent-before-action is respectful. No files are modified without explicit agreement.
- The first-session-ever greeting ("This is the beginning. Let's forge something worth building.") carries genuine emotional weight.

**Friction points:**
- After first install completes (Step 3 → Step 4 → Step 5 → Step 7), the developer hits the session menu. If this is their very first encounter with Momentum as a practice, the menu items ("Plan a sprint", "Refine backlog", "Triage") assume they already know what sprints, backlogs, and triage mean in the Momentum context. The expertise-adaptive check (momentum_completions == 0) triggers full walkthrough mode, but the walkthrough is about the *workflow*, not the *practice*. A first-timer who doesn't know what a Momentum sprint is versus a generic sprint gets no guidance.
- The restart notice ("Restart Claude Code when ready") is a practical dead end. After restart, the developer must re-invoke `/momentum` to continue. There is no breadcrumb or reminder of what they were doing. They return to a cold session that happens to have rules installed but no continuity from the install conversation.

### 2. The Expert

**Journey:** Has used Momentum for 15+ sessions. Invokes `/momentum`, sees abbreviated greeting, selects "Continue the sprint" within 2 seconds.

**Bright spots:**
- The happy path is genuinely fast (2-3 tool calls to first visible output). The preflight consolidation is well-engineered.
- Expertise-adaptive orientation means no re-explanation of what they already know.
- Fuzzy continue ("yes", "go ahead", "yep") bypasses any confirmation friction.

**Friction points:**
- The expert who wants to skip the greeting entirely and go directly to sprint-dev ("just continue where I left off") still sees the full narrative + planning context + menu + closer. For someone who invokes `/momentum` multiple times daily, this greeting ceremony becomes friction. There is no "express mode" that detects "you have one obvious action" and offers a single-key shortcut.
- The expert who wants to invoke a specific sub-skill directly (e.g., "create story 3.2") must wait for the menu, type the request in natural language, get a confirmation gate ("Creating story 3.2 — correct?"), confirm, and only then dispatch. That is three exchanges where the user already knew the answer from the start.

### 3. The Confused User

**Journey:** Typed `/momentum` because they saw it somewhere, or thought it was a different tool. They don't have any sprint context, backlog, or planning artifacts.

**Bright spots:**
- The `first-session-ever` state gracefully handles the "nothing exists yet" case.
- The decline path (Step 6) is clean and non-judgmental: "Understood. Setup is needed... You can invoke `/momentum` again any time."

**Friction points:**
- If a confused user declines setup [N], they land at Step 7 (session orientation — degraded) with no sprint data, no journal, and no planning context. The menu offers "Plan a sprint" / "Refine backlog" / "Triage" — but the user may not even have a project they want to run sprints on. There is no "I'm just exploring" or "Tell me what Momentum is" option. The confused user has no off-ramp that educates without committing.
- If the confused user selects "Triage" they get: "Triage is coming in the next phase." If they select "Refine backlog" without any backlog, the create-story skill may hit a wall. Two out of three menu items may dead-end for a truly new user.

### 4. The Edge-Case User

**Journey:** Has multiple tabs open, partially-completed sprints, dormant threads, and a messy journal.

**Bright spots:**
- Concurrent tab detection (30-minute window) is a genuine safety feature with correct UX: warn, never block.
- Dormant thread hygiene (>3 days) proactively surfaces cleanup without being obnoxious.
- The no-re-offer pattern is sophisticated — it respects prior decisions via context_hash and correctly allows re-offer when context materially changes.

**Friction points:**
- The "more than 5 open threads" triage offer fires at the same time as dormant-thread hygiene, concurrent-tab warnings, and dependency-satisfied notifications. All of these are emitted inline before the selection prompt. For a messy journal, the developer could see 4+ warnings/offers before the thread list, creating an overwhelming wall of text. There is no prioritization — concurrent-tab warning (urgent safety) is displayed at the same visual weight as a dormant thread suggestion (nice-to-have).
- The declined_offers persistence is thread-scoped. If a developer closes a dormant thread and then a *different* thread becomes dormant 3 days later, there is no session-level "I don't care about dormant threads — stop asking" option. The developer must decline per-thread every time.

### 5. The Hostile Environment

**Journey:** Missing files, broken JSON, git not available, no network.

**Bright spots:**
- The preflight script handles JSON decode errors gracefully (falls back to empty dicts).
- Hash drift check handles `git hash-object` failures (timeout, not found) without crashing.
- Missing journal.jsonl is treated as "no open threads" — no error, no warning.

**Friction points:**
- If `momentum-versions.json` is missing or corrupt, `current_version` falls back to `"0.0.0"` and the preflight silently produces `route: "greeting"` with no version actions. The developer gets a normal session with no indication that the skill installation is broken. This is silent data loss — the developer won't know why upgrades aren't offered.
- If `momentum-tools.py` itself fails (Python not installed, script missing, permission denied), the SKILL.md startup has no error handling around the Bash call. The Bash tool will return an error, but there is no graceful degradation path defined. The developer sees a raw error and has no guidance.
- The journal.jsonl POSIX append-safety note is correct for small entries, but there is no protection against concurrent *reads*. Two tabs both reading the journal, computing thread states, and then both appending could produce correct but duplicated hygiene actions (e.g., two "close dormant thread" entries for the same thread).

### 6. The Automator

**Journey:** Another agent or a CI pipeline wants to invoke Impetus headlessly to check sprint status, trigger a sprint-dev session, or get the current greeting state.

**Bright spots:**
- `momentum-tools.py` subcommands (`session greeting-state`, `session startup-preflight`, `sprint activate`) are already CLI-accessible and return structured JSON. An automator could bypass Impetus entirely and call these directly.

**Friction points:**
- Impetus itself has zero headless support. Every path requires interactive input: [Y]/[N] for install, menu selection for greeting, thread selection for journal display. There is no `--headless` flag or input-parameter passthrough.
- The dispatched sub-skills (sprint-dev, sprint-planning) are invoked via Agent tool, which is inherently interactive. A pipeline that wants "run the next story in the sprint" cannot get there without simulating a conversation.

---

## Headless Assessment

**Level: Partially adaptable**

The core routing logic is already in `momentum-tools.py` and returns structured JSON. The greeting state computation, version comparison, hash drift detection, and journal scanning are all headless-ready today — they just happen to be consumed by an interactive skill.

What would be needed:
- A `--action` parameter for startup-preflight that specifies the desired dispatch target (e.g., `--action=sprint-dev`), skipping the greeting ceremony entirely.
- The install/upgrade consent could accept a `--auto-approve` flag for CI environments.
- The thread selection could accept a `--thread=T-001` or `--continue-most-recent` parameter.

What cannot easily go headless:
- First-install consent is fundamentally interactive (it modifies the developer's machine).
- Hash drift resolution (restore vs. keep) requires judgment.
- Dormant thread triage is inherently a human decision.

**Headless invocation contract (if implemented):**
- Input: `momentum:impetus --headless --action=<dispatch-target> [--thread=<id>] [--auto-approve]`
- Output: `{"route": "dispatched", "target": "momentum:sprint-dev", "thread": "T-003"}`

---

## Facilitative Patterns Check

| Pattern | Present? | Assessment |
|---|---|---|
| **Soft Gate Elicitation** | Partially | The proactive-offer pattern uses "? [gap]. [resolution]? Or continue as planned?" which is a soft gate. But the main menu is hard-numbered — no "anything else before we start?" gate after menu display. |
| **Intent-Before-Ingestion** | Yes | Startup preflight gathers state before displaying anything. Journal read happens before thread display. Good. |
| **Capture-Don't-Interrupt** | No | If a developer provides additional context during natural language input (e.g., "I want to continue the sprint but first let me tell you about a bug I found"), the input interpretation gate extracts only the dispatch intent and discards the rest. No mechanism to capture ambient context. |
| **Dual-Output** | Not applicable | Impetus produces no artifacts — it orchestrates. Sub-skills produce the artifacts. |
| **Parallel Review Lenses** | Not applicable | Impetus is not a review tool. |
| **Three-Mode Architecture** | No | There is one mode: interactive HITL. No guided/yolo/autonomous distinction. See headless assessment above. |
| **Graceful Degradation** | Partially | Preflight handles missing files well. But if a dispatched sub-skill fails or is unavailable, there is no fallback behavior defined. The "Triage" and "Run retro" placeholders are technically graceful degradation (acknowledge, don't crash), but they provide no alternative action. |

---

## Key Findings

### Edge Cases

**EC-1: Greeting ceremony friction for power users**
- Severity: `medium-opportunity`
- Area: SKILL.md happy path (greeting route, no threads)
- Observation: A developer with 50+ sessions who always continues their sprint still sees the full narrative + planning context + menu + closer before they can type "1". The ceremony is beautiful on first encounter but becomes drag on the 50th.
- Suggestion: When `momentum_completions >= 10` and there is exactly one obvious action (active sprint in progress, no threads), consider an "express greeting" mode: single-line state + single-key dispatch. Example: `Sprint "sprint-2026-04-06" is underway. Continue? [Y] or menu [M]`. Preserves the full greeting as an opt-in via [M].

**EC-2: No session-level "stop asking about dormant threads" escape hatch**
- Severity: `low-opportunity`
- Area: workflow.md Step 11, dormant thread hygiene
- Observation: No-re-offer is per-thread, per-context-hash. A developer who always declines dormant closure must decline each thread individually, each session, until context changes. There is no "I manage my own threads, stop offering" preference.
- Suggestion: After 3 consecutive dormant-closure declines across any threads, offer a session-level preference: "You've declined dormant cleanup a few times. Want me to stop offering for this project?" Persist as a preference in installed.json.

**EC-3: Hygiene wall-of-text for messy journals**
- Severity: `medium-opportunity`
- Area: workflow.md Step 11, hygiene checks
- Observation: Concurrent-tab warning, dormant thread offers, dependency-satisfied notifications, and unwieldy-triage offer all emit inline before the selection prompt. With 6+ threads, some dormant, some recently active, the output before the actual thread list could be overwhelming.
- Suggestion: Prioritize and batch hygiene signals. Lead with safety (concurrent-tab warning). Then display the thread list. Then, after display but before the selection prompt, surface one hygiene observation — the most impactful one. Offer "more hygiene items?" as a soft gate rather than dumping everything.

**EC-4: No recovery path for broken momentum-tools.py**
- Severity: `medium-opportunity`
- Area: SKILL.md Startup section
- Observation: If the Bash call to `momentum-tools.py session startup-preflight` fails (Python not found, script error, permission issue), SKILL.md has no error handling. The developer sees a raw error with no guidance.
- Suggestion: Wrap the preflight Bash call in a check. If it returns non-zero or invalid JSON, display a brief diagnostic: "Something went wrong during startup. Check that Python 3 is available: `python3 --version`. If this persists, try `/momentum:impetus` again or file an issue." Then offer a degraded session menu with whatever state can be inferred from direct file reads.

**EC-5: Silent failure when momentum-versions.json is missing**
- Severity: `low-opportunity`
- Area: momentum-tools.py startup-preflight, line 589-596
- Observation: If the versions manifest is missing or corrupt, the preflight silently falls back to `current_version = "0.0.0"`, produces no needs_work, and routes to "greeting". The developer has a normal session but will never receive upgrades and has no indication anything is wrong.
- Suggestion: When `current_version == "0.0.0"` (the fallback), include a `warning` field in the preflight response: `"warning": "versions manifest missing or corrupt — upgrades disabled"`. SKILL.md can surface this as a proactive offer: "? Version manifest is missing — upgrades won't be detected. Want me to check the installation?"

### Experience Gaps

**EG-1: No "what is Momentum?" off-ramp for explorers**
- Severity: `medium-opportunity`
- Area: SKILL.md happy path, session-greeting.md menus
- Observation: Every session state's menu assumes the developer knows what they want. There is no "Learn about Momentum", "What can you do?", or "Help" option. The first-session-ever state introduces Impetus's identity but not the practice itself. A developer who found the plugin through marketplace search has no in-context education path.
- Suggestion: Add a natural-language fallback for help-seeking inputs ("what is this?", "help", "what can you do?"). Response: a 3-sentence practice overview + link to the practice plan. Not a menu item (it would dilute the action-oriented menu), but a recognized input class alongside number/fuzzy-continue/natural-language.

**EG-2: Post-restart continuity gap**
- Severity: `medium-opportunity`
- Area: workflow.md Steps 2-3 (first-install), Step 9 (upgrade)
- Observation: When a restart is required (enforcement hooks), the developer is told to restart but has no breadcrumb for what comes after. They return to a cold session. If they had been mid-install, the state files are written, so re-invocation routes to greeting (not re-install). But the developer doesn't know this — they might think they need to redo the install.
- Suggestion: After the restart notice, add a forward-looking line: "When you restart and invoke `/momentum` again, I'll pick up right where we left off — setup is already recorded." This costs zero implementation and eliminates uncertainty.

**EG-3: Thread context_summary quality variance**
- Severity: `low-opportunity`
- Area: journal-schema.md, workflow.md Step 12
- Observation: Thread resumption quality depends entirely on the quality of `context_summary` written by whatever workflow created the thread. The journal schema defines guidelines ("one sentence, specific, actionable") and the progress-indicator reference defines sufficiency criteria, but there is no validation at write time. A workflow that writes "Working on story" produces a thread that is useless for resumption.
- Suggestion: Add a minimum-quality check to Step 13 (journal write). Before appending, verify context_summary is at least 20 characters and contains at least one specific noun (story number, file name, feature name). If it fails, enhance it from available context before writing.

**EG-4: No sprint progress summary in greeting**
- Severity: `high-opportunity`
- Area: SKILL.md happy path greeting, session-greeting.md
- Observation: The greeting narrative says "Sprint X is underway — steady ground" but gives no quantitative signal. How many stories done? How many remain? Any blocked? The developer must select "Continue the sprint" and wait for sprint-dev to load before they know their sprint health. This is the most valuable context for the daily session start, and it is deferred behind a dispatch.
- Suggestion: Include a one-line sprint health summary in the greeting state data from preflight. Example: `Sprint "sprint-2026-04-06" is underway — 2 of 4 stories done, 1 in progress, 1 ready.` This turns the greeting from an identity moment into an orientation moment. The preflight script already reads the sprint and story data — adding a count summary is trivial.

### Delight Opportunities

**DO-1: Sprint streak / session cadence recognition**
- Severity: `low-opportunity`
- Area: session-greeting.md, installed.json session_stats
- Observation: `session_stats` tracks `momentum_completions`, `first_invocation`, and `last_invocation`. This is enough to compute session frequency and detect patterns, but nothing uses it beyond expertise-adaptive orientation.
- Suggestion: At milestone completions (10th session, 50th, 100th) or after a streak of daily sessions, Impetus could drop a brief, in-character acknowledgment: "Twenty sessions in. The discipline holds." Not gamification — recognition. In keeping with the Optimus-meets-KITT voice: earned, understated, rare. Add to session-greeting narrative selection logic with a new `milestone` field in the greeting data.

**DO-2: "What changed since last session?" digest**
- Severity: `medium-opportunity`
- Area: SKILL.md happy path greeting
- Observation: When a developer returns after a day or more, they get the sprint state but no digest of what happened since their last session. If they ran work across multiple tabs, the journal has the history, but it is not surfaced. A developer returning Monday morning after Friday work has to reconstruct context manually.
- Suggestion: When `last_invocation` is more than 12 hours ago and the journal has entries after that timestamp, compute a brief "since you were last here" digest: stories that moved status, threads that were opened/closed, sprint state changes. One paragraph, delivered between the narrative and the menu. This transforms session-start from "where was I?" to "here's what happened."

**DO-3: Natural-language shortcut memory**
- Severity: `low-opportunity`
- Area: Input interpretation behavioral pattern
- Observation: If a developer always types "let's build" instead of selecting menu item 1, the natural language gate fires every time: extract intent, confirm, wait, dispatch. The confirmation is correct UX for ambiguous input, but for a developer who says the same thing every session, it becomes performative.
- Suggestion: Track confirmed natural-language → dispatch mappings in session_stats. After the same natural-language phrase confirms to the same dispatch target 3 times, auto-resolve it (skip confirmation). Surface this as: "I know that one — heading to sprint-dev." Respects the safety of the confirmation gate while rewarding consistent users.

---

## Top Insights

### 1. The greeting is an identity moment but not an orientation moment

The narrative voice is exceptional — "the work is done", "steady ground", "let's face it together" — these carry real emotional weight. But the greeting contains zero quantitative context about sprint health. The developer's most urgent question at session start is "where are things?" not "what does Impetus feel about things?" The fix is additive, not subtractive: keep the narrative voice, add a one-line sprint health summary. The preflight already has all the data.

### 2. Hygiene signals need triage, not just accumulation

The Step 11 hygiene system is impressively thorough — concurrent tab detection, dormant threads, dependency satisfaction, unwieldy journal triage — but it presents everything at once. Real users with messy journals will hit a wall of warnings that dilutes the signal. The highest-impact improvement would be prioritizing hygiene signals (safety first, convenience second) and batching lower-priority items behind a soft gate. This is the difference between a system that detects problems and a system that helps you address them.

### 3. Express mode for high-frequency users is the single highest-leverage UX addition

A developer who invokes `/momentum` 3-5 times daily, always continues their sprint, never needs the menu — this is the power user profile. Today they see the full ceremony every time. An express mode that detects "one obvious action" and offers a single-key shortcut would transform the daily experience from "pleasant but repetitive" to "frictionless." The implementation is straightforward: check `momentum_completions >= N`, check if exactly one sprint action is obvious, and offer the shortcut. The full menu remains one keystroke away.
