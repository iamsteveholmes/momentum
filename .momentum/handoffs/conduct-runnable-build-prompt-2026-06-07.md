# Prompt 2 — Build the conduct-runnable sprint AS the conduct engine (in-session, by hand)

> Updated 2026-06-07 after the planning session. Corrections from the original draft are marked **⟳ CHANGED** / **➕ NEW**. The sprint is already *planned* — read "State as of now" first; it changes where you start.

---

## TASK

Build the **conduct-runnable** sprint by **acting as the conduct engine yourself, in-session** — exactly as `sprint-2026-06-02-conduct-core` was run — and produce the SAME single end-gate report. conduct still isn't runnable (that's literally what this sprint builds), so **YOU are the Conductor, by hand**.

You are in **PLAN MODE**: read the sources, then present your plan via `ExitPlanMode` and wait for my approval before activating or building anything. Use **dynamic Workflows** for the parallel build work.

---

## ➕ STATE AS OF NOW (read before anything — the original prompt assumed a blank start; it isn't)

- The sprint is **planned but NOT activated**. `.momentum/sprints/index.json` → `planning` holds: `slug: sprint-2026-06-05-conduct-runnable`, **25 stories**, **6 waves**, `status: planning`, `active: null`.
- **The sprint branch already exists**: `sprint/sprint-2026-06-05-conduct-runnable`, **10 commits ahead of main**, carrying all planning artifacts (25 frozen contracts, coverage plan, the architecture/PRD spec updates, the HTML plan doc). **Do NOT create the branch from main** — check out the existing one.
- **Contracts are FILES**, one per story, at `.momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/<slug>.{eval.yaml,review.md,smoke.sh}` (18 skill-invoke `.eval.yaml`, 5 document-review `.review.md`, 2 bash `.smoke.sh`). They are the **frozen record**. `planning.team.story_assignments[<slug>]` carries only `{role, specialist, guidelines, wave}` — the contract lives in the file, not embedded in the assignment.
- **Scope is 25 stories** (the original 20 + 5 net-new retro findings folded in: `conduct-state-machine-defects-shipped-unfixed`, `tighten-dev-fixer-write-scope-stop-story-spec-edits`, `controlled-enums-and-stable-ledger-schema-finding-cards`, `exercise-conduct-escalation-machinery-end-to-end`, `extract-shared-diff-range-helper-for-per-story-review`).
- **Spec impact is already applied** on the branch (architecture **Decision 59 — Conduct Execution Engine**, plus `FR139`/`FR140`/`NFR22`, committed in `92dbf9c`). **Do NOT re-do spec updates.**
- The branch base carries **2 of my earlier commits** (`cabf9f2`, `b4cff4e` — retro audit + the finding intakes) that are **not on main**. Expected; relevant only at the sprint→main merge.

---

## READ FIRST (start with the report standard + decisions; go deeper as needed)

- **End-gate report standard — BUILD THE FINAL REPORT TO THIS:** `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md`. Worked example to match: `.momentum/handoffs/sprint-2026-06-02-conduct-core-hitl-report.html`. Reference generator: `.momentum/gen-endgate-report.py`.
- **Design spec:** `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` (§3 per-story pipeline, §4 finding schema, §6 git, §8 single end-gate, §9 report).
- **Decisions:** DEC-035, DEC-036 (stakes-and-timing escalation), DEC-037 (standalone `/momentum:conduct`, coexists with sprint-dev — do NOT rewrite sprint-dev).
- **The sprint record:** `.momentum/sprints/index.json` → `planning` (`waves[]`, `team.story_assignments[]`) + the frozen contract files in `specs/`.
- **The plan you're executing:** `.momentum/handoffs/conduct-runnable-sprint-plan-2026-06-06.html` (the planning review doc — §7 deviations, §8 risks, §9 activation are load-bearing for you).

---

## EXECUTION MODEL — act as the conduct engine

- **YOU are the Conductor and own ALL git mutation** (worktree create off the sprint branch, rebase, `merge --no-ff`, conflict resolution, cleanup, the sprint→main merge). Subagents build/review/fix in **isolated worktrees** and return structured output; they **NEVER merge**.
- **Per-story pipeline**, fanned out as **dynamic Workflows**: dev (isolated worktree) → concurrent { QA vs the frozen Part-B contract ; report-only adversarial review using the **bmad-code-review METHODOLOGY** — NOT the interactive skill, which HALTs and writes story files } → directed fixer (`momentum:dev` fix-mode, bounded retry 3) → a re-check stage (re-run the adversarial review on the post-fix diff; one bounded re-fix) → then **YOU** rebase + merge it to the sprint branch.
- **⟳ CHANGED — dependency gating: use the WAVES, not `depends_on`.** Every story's `depends_on` in the index is **empty** (these were intake stubs). The **`planning.waves` order IS the dependency DAG** — I derived it from sequencing hints + story semantics. Treat waves as **binding**, not advisory: launch wave N's stories only once every story in waves 1..N-1 has reached `>= review`. (The original "gate on each story's own `depends_on`, waves advisory" does not apply here — there is no `depends_on` data.)
- **⟳ CHANGED — serialize the `workflow.md`-heavy stories.** ~12 of the 25 stories edit the conductor's single `skills/momentum/skills/conductor/workflow.md`. The index has **no `touches` data**, so overlap can't be auto-detected. Building two `workflow.md` stories in parallel **will** conflict. Within a wave, **serialize** stories that edit `conductor/workflow.md` (build them one at a time, rebasing each onto the prior's merge) and only parallelize stories that touch disjoint files. This is the single biggest build risk — plan for it explicitly.
- **⟳ CHANGED — freeze check: there is NO `frozen_sha256` field.** The hand-authored contracts follow the conduct-core format, which carries no `frozen_sha256` (that field belongs to the not-yet-built producer schema). **Do NOT HALT looking for it.** The **committed contract files in `specs/` ARE the frozen record.** If you want a freeze baseline, compute `sha256` of each contract file at activation and record it yourself — but never block on a field that doesn't exist.
- **⟳ CHANGED — acceptance-criteria source.** The conduct stories have **no `## Acceptance Criteria` heading**; they use **`## What's needed`** (and `## Story` / `## Why`). The contracts' `acceptance_criteria_ref: …#acceptance-criteria` anchor is dangling-by-convention — QA/dev agents must read the **`## What's needed` bullets** as the acceptance source, cross-checked against the contract's Part-B body.
- **➕ Special-case `conduct-state-machine-defects-shipped-unfixed` (critical, Wave 2):** its two transition fixes **already landed** on the branch (approve path `review→verify→done` in `conductor/workflow.md`; terminal→terminal guard in `momentum-tools.py`). **Confirm-then-verify** those (regression), and focus implementation on its genuinely-open work: the **MAJOR-residual → backlog-stub governance guard**. The story carries a `## Status (verified 2026-06-06)` note saying exactly this.
- **DEC-036 escalation, bias NARROW:** every finding is **routine → auto-fix silently and collapse**, UNLESS it is **stakes-class** (security/auth-isolation | irreversible/destructive | high-blast-radius/architecture). Stakes-class → **ESCALATE** (raise), do not silently fix. **Mid-flight pause ONLY** on the narrow bar (irreversible-and-imminent OR build-invalidating); everything else collapses to the end gate. Expect **0–1 mid-flight pauses** across the run.
- **ONE human gate at the END.** No intermediate asks/HALTs. Build, fix, merge autonomously; on persistent failure **quarantine-and-continue** (never HALT mid-build). **Scope discipline:** build agents must NOT edit story spec files or other stories' files — **revert any such scope leak before merging** (this sprint even has a story about it: `tighten-dev-fixer-write-scope-stop-story-spec-edits`).
- **After all merges:** a **post-merge AVFL integration pass** over the 3-dot merged diff (auto-fix bounded; collect leftovers) + an **E2E/verification consolidation** that **honors the coverage plan** (`.momentum/sprints/sprint-2026-06-05-conduct-runnable/coverage-plan.md`: 3 covered-by-composition, 22 dedicated-run — do NOT re-verify in isolation what an integration scenario already discharges).

---

## ⟳ CHANGED — ACTIVATION (first step after plan approval)

1. `export CLAUDE_PROJECT_DIR=/Users/steve/projects/momentum`. Invoke momentum-tools as **`python3 skills/momentum/scripts/momentum-tools.py …`** (it is NOT on PATH — that's literally story #1).
2. **Check out the EXISTING branch** — do NOT create from main: `git checkout sprint/sprint-2026-06-05-conduct-runnable`. The planning artifacts + contracts are already on it.
3. **Record per-story approvals first** — holistic review left `planning.approvals` empty, so a bare `sprint activate` fails its approval guard. Record approval for all 25 (autonomous bookkeeping), then `verify-approvals`, then `sprint activate`:
   ```bash
   MT="python3 skills/momentum/scripts/momentum-tools.py"
   for s in $($MT_LIST); do $MT sprint story-approve --slug "$s" --decision approved; done
   $MT sprint verify-approvals
   $MT sprint activate
   ```
   (Pull the slug list from `planning.stories` — use a `while IFS= read -r` loop or a Python one-liner, NOT `for x in $VAR`; see lessons.)
4. **Freeze baseline (optional):** there is no `frozen_sha256` in the contracts — if you want one, `sha256sum specs/*` now and stash it; do not block on it.

---

## THE END-GATE REPORT — produce it EXACTLY like the conduct-core report (build to the Format & Voice spec)

- **Self-contained HTML** at `.momentum/handoffs/sprint-2026-06-05-conduct-runnable-hitl-report.html`; open it with **`open <file>`** (a cmux browser surface can silently drop — verify it persists).
- **PLAIN LANGUAGE, assume nothing. RISK-organized, NOT a findings catalog:** focus on the high-risk divergences — each a **5-beat narrative** (what the piece does · why its guarantee was written that way · where it diverged · the risk created/removed · why acceptable); **collapse routine fixes to a COUNT**.
- **Sections:** §01 what-shipped (before/after, plain) · §02 per-piece purpose WITH a **"Review this work item"** expand per item (testing-FIRST verification — honest about inspection-vs-execution — then architectural rationale WITH decision references, then the actual color-coded diff) · §03 high-risk divergences · §04 the decision(s) for you · §05 dismissed (with rationale) + routine count · §06 **"How done is this, really?"** (honest live-vs-hollow status) · §07 merge & push · **anti-rubber-stamp GATE** (no pre-checked approve; per-card acknowledgment for stakes items).
- **For any UI-changing item**, lead its review panel with before/after screenshots (capture by running the app) — Format spec §6b. **Note:** this sprint has **no app-ui stories** (all skill-instruction / document-review / bash), so §6b likely won't trigger — keep the rule for generality but don't fabricate screenshots.

---

## GIT

Commit **autonomously** (conventional commits; **no Co-Authored-By trailer**). **NEVER push without my explicit approval.** The sprint→main merge is part of the approve sequence; the **push is a SEPARATE, explicit confirmation** (show me the push list and ask).

---

## PRACTICAL LESSONS (carried from conduct-core + this planning session — these save hours)

- **zsh, not bash:** unquoted `$VAR` does **NOT** word-split — use `while IFS= read -r` loops or literal word lists, never `for x in $VAR`. (Also: `declare -n` namerefs are unsupported; arrays passed unquoted collapse to one token. This bit the planning session.)
- **The Bash tool persists cwd** across calls — anchor every call (`cd` to repo root, or absolute paths + `git -C`).
- **Dynamic Workflow `args` can arrive as a JSON string** — defensively `const x = typeof args === 'string' ? JSON.parse(args) : args`.
- **Workflow `meta` must be a pure literal** — no variables/calls/spreads, and no apostrophes inside single-quoted strings.
- **In the AVFL pass, assert the canonical finding-schema vocabulary** (`stakes_class` / `disposition` / `timing_tier` / the narrow mid-flight bar) is **CONSISTENT across all files that encode it** — that's where cross-story integration drift hides. (`controlled-enums-and-stable-ledger-schema-finding-cards` is a story precisely because conduct-core's ledgers drifted here.)
- **➕ The adversarial Outsider-Test guard is strict** about source-inspection and internal-name clauses. When QA/review reads a contract, remember: `.review.md` (document-review) contracts are verified by reading the **named deliverable artifact** — that's sanctioned, not a violation. `.eval.yaml` contracts must be checked by **observable behavior**, never by counting internal checks or naming which agent the conductor spawns.
- **➕ `planning.slug` / `touches` / `depends_on` have no CLI setters** and the latter two are empty — don't expect to read dependency or file-overlap data from the index; the waves + your own diff inspection are the source of truth.

---

## STOP

STOP at the single end-gate report and wait for me (**request changes** vs **approve**). On **approve**: triage leftovers → backlog stubs, close stories, merge sprint→main, then **SHOW the push list and ASK before pushing**.
