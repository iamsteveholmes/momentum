# Sprint-Dev Redesign Spec

**Status:** Draft for developer review — converge, then implement.
**Date:** 2026-05-29
**Scope:** Rewrite of `momentum:sprint-dev` and its dependent agents/skills to a per-story, autonomous-build, single-end-gate model.

---

## 1. Design intent

This redesign collapses the multi-gate, wave-barriered sprint-dev flow into an autonomous build with **exactly one** human-in-the-loop surface at the end. It is grounded in ten binding developer decisions. They are not up for relitigation — every section below designs *to* them.

1. **End-gate is the default HITL surface; a narrow mid-flight escalation tier is the sole exception.** The single human end-gate remains the default and the safety net: AVFL never asks the developer anything, dev agents always retry on failure (no retry/skip/halt prompt), and **routine** findings are *always* auto-fixed silently — there is no per-finding fix/defer prompt for ordinary work. The sole exception is a narrow, high-bar, stakes-gated mid-flight escalation tier: a finding may escalate mid-flight ONLY if it is **irreversible-and-imminent** OR **build-invalidating**. No other condition widens the mid-flight tier. Stakes-class legitimate findings (security/auth-isolation, irreversible/destructive, high-blast-radius/architecture) are **raised** (surfaced as decision cards) rather than silently auto-fixed; findings that do not meet the mid-flight bar are held for end-gate expansion. This amends DEC-035 binding decision #1 — preserving its anti-firehose intent while relaxing its absolutism.
2. **One end gate only (default) + narrow mid-flight exception.** After the report, a **Conductor** waits for the developer to either (a) say *"we need changes"* → run ONE change-workflow that loops over fixes, or (b) *approve* → triage any leftover issues into new stubs, merge to main, push. There is **no Reject**. Stories close one way or another; the only non-closed case is a blocked/never-completed story → spin out a new stub via `momentum:triage`. New work discovered during review → new stubs via triage. The mid-flight escalation tier fires only on the stakes-and-timing bar (irreversible-and-imminent OR build-invalidating); end-gate expansion is the norm and safety net.
3. **One workflow for all fixing.** The change-workflow and the build-fix loop are the **same** workflow type, run any time fixing is required.
4. **Per-story independence.** Each story runs its *own* complete flow: dev → concurrent QA + code-review → fixers → merge its own worktree → done. Prefer per-story independence (a story merges the instant it passes) over global waves. Fall back to waves only when a hard dependency forces it.
5. **Code review tooling.** `momentum:code-reviewer` is a STUB and must not be relied on. Use **`bmad-code-review`** for the adversarial bug hunt; use the built-in **`/simplify`** for optional cleanup. Do not build an in-house reviewer now.
6. **AVFL kept, repositioned.** AVFL runs *after* all worktrees merge — it is the reviewer **of the merge**, inspecting the integrated git result to catch integration issues. Rewrite it as a dynamic **Workflow** (the Workflow tool), not a prose skill.
7. **E2E validation kept.**
8. **HTML report, fully self-sufficient.** The recurring failure to fix: reports omit context the developer needs. Every section MUST contain ALL context needed to decide *in that section* — no terse shorthand, no "see code". The report step is a fully open conversation; the Conductor updates the report and answers questions until the developer gives the go-ahead.
9. **Conductor owns git mutation.** It resolves merge conflicts itself or fires dev subagents to resolve them. Merge failures retry. Worktrees merge after build; AVFL then reviews the merged result. Never HALT.
10. **Verification decided at planning.** *How* each story is verified is decided at **sprint-planning**, not sprint-dev. Sprint-planning emits a per-story verification contract that the build flow consumes.

**State machine (unchanged, terminal states clarified):**
`backlog → ready-for-dev → in-progress → review → verify → done`, with terminals `done`, `dropped`, `closed-incomplete`.

Key structural inversion: the unit of flow is **the story, not the wave**. A story runs its own `pipeline()` (dev → QA+review → fix → merge) and merges itself the moment it passes. The only sprint-wide barriers are the single post-merge AVFL pass, E2E, and the single end-gate report.

---

## 2. End-to-end flow

```
SPRINT-PLANNING  (decision 10)
   └─ emits per-story VERIFICATION CONTRACT (closed-enum method + dev-readable header)
   └─ writes story_assignments[] with contract pointer + frozen_sha256 + can_merge_independently
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ BUILD PHASE — Conductor owns it. Per-story pipelines, concurrent.        │
│ Frontier = stories whose depends_on are all merged (>= review).          │
│                                                                          │
│  For each launch-ready story, concurrently:                              │
│    pipeline(S):                                                          │
│      1. DEV       — worktree off sprint branch; implements vs plain ACs  │
│      2. QA + REVIEW (concurrent fan-out, read-only, this story's diff)   │
│           • qa-reviewer    → verifies the story's verification contract  │
│           • bmad-code-review → adversarial bug hunt                      │
│      3. FIX      — code-fixer applies ALL legitimate findings; re-check; │
│                    /simplify optional cleanup after fixes; bounded retry │
│      4. MERGE    — Conductor rebases+merges S's worktree → sprint branch;│
│                    status → review; worktree+branch removed (per-story). │
│                    Conflict → Conductor resolves or fires fixer; retry.  │
│      → on merge: re-evaluate frontier, launch newly-unblocked stories.   │
│      → exhausted retries: mark blocked, CONTINUE (no halt).              │
└─────────────────────────────────────────────────────────────────────────┘
                              │ all stories merged or blocked
                              ▼
   AVFL-ON-MERGE (decision 6) — Workflow; reviews 3-dot merged diff for
   integration defects; auto-fixes; returns CLEAN | NON_CONVERGENT + leftovers
                              ▼
   E2E VALIDATION (decision 7) — runs against the merged result
                              ▼
   CONDUCTOR END GATE (decisions 2, 8) — single HITL
   └─ render self-sufficient HTML report → open conversation
        ├─ question  → answer, update report in place, stay open
        ├─ "changes" → run CHANGE-WORKFLOW (decision 3) → re-render report → loop
        └─ approve   → APPROVE SEQUENCE:
              triage leftovers/blocked/discovered → stubs (momentum:triage)
              close all stories (done | closed-incomplete)
              merge sprint branch → main (Conductor resolves conflicts; retry)
              show push list → ASK before push → git push
```

There are **two** developer touchpoints in the whole flow: the end-gate conversation (which resolves to *changes* or *approve*), and the push confirmation (folded into approve, mandated by git-discipline). Everything else is autonomous.

---

## 3. Execution model — the per-story pipeline

### Principle: the story is the unit of flow

The old model phased the whole sprint through global barriers — all devs, then one AVFL gate, then all reviews, then all fixes, then one `done` transition for everyone. That is a parallel-barrier topology: throughput is gated by the slowest story in every phase, and nothing reaches `done` until the final batch.

The new model is `pipeline()` per story, fanned out across stories — explicitly **not** `parallel()` barriers. Each story runs its own complete pipeline and merges itself the moment it passes. A fast, independent story merges (integration-clean) while a slow story is still in dev.

Why `pipeline()` over barriers:

- **No head-of-line blocking.** Under barriers, one slow/retrying story stalls every other story at the next gate — making decision 4 ("a story merges as soon as it passes") structurally impossible.
- **No batched HITL.** Barriers force the orchestrator to collect per-story results to present together — exactly what produced the old per-finding prompts and consolidated fix queue. Per-story pipelines fix in place automatically and surface nothing until the end report.
- **Correct dependency semantics.** A barrier keyed on "all wave-(N-1) done" couples stories that share no files. `pipeline()` gates a story on *only its own `depends_on` set*.

### The Conductor

The **Conductor** is the orchestrator role that owns the build phase. It replaces the global wave loop *and* the per-failure ASK gate. It is the only entity that spawns agents and the only entity that mutates git on the sprint branch (decision 9). It writes no code, specs, or fixes itself — it spawns subagents for all of that.

```
Conductor state (in-memory, mirrored to task tracking):
{
  frontier:  [slug, ...],            // unblocked, not yet launched
  running:   { slug: pipeline_handle },
  merged:    [slug, ...],            // status == 'review' on sprint branch
  blocked:   [slug, ...],            // exhausted retries OR unsatisfiable dep
  retries:   { slug: int },          // per-story retry count
}
```

Responsibilities during build:
- Maintain the **ready frontier**: stories whose `depends_on` are all satisfied and not yet launched.
- Launch one **story pipeline** per ready story, concurrently.
- React to each pipeline's terminal signal: `merged`, `blocked`, or `failed`.
- On `merged`: re-evaluate the frontier; launch any story that just became unblocked.
- On `failed`: **always retry automatically** (decision 1). Bounded retry (default 2). If still failing, mark `blocked` and **continue** — never halt.
- On merge conflict: resolve itself or fire a dev subagent, then retry the merge (decision 9). Never halt.
- When the frontier is empty and all pipelines have terminated: hand off to AVFL-on-merge, then E2E, then the end-gate report.

The Conductor never asks the developer anything during build.

### Per-story dependency gating (no global waves)

Dependencies resolve **per story, on its own `depends_on` set only**. `sprint_record.waves` becomes advisory ordering metadata at most; the binding source is each story's `depends_on` array.

A story is **launch-ready** when:

```
story.status == "ready-for-dev"
  AND every slug in story.depends_on has reached its merge gate
      (status >= "review" on the sprint branch)
```

The gate is **`>= review`, not `done`** — this fixes the old unsatisfiable-`done` bug. A blocker is "available to depend on" the instant its code is merged into the sprint branch, because the dependent branches its worktree off the sprint branch and inherits the blocker's code. The blocker need not pass AVFL or be verified (those are sprint-wide, end-of-build) before its dependents can build on it.

Frontier re-evaluation is event-driven:

```
on story S merged (status -> review):
    for each story T not yet launched:
        if T.status == "ready-for-dev"
           and all(dep in merged for dep in T.depends_on):
            frontier.add(T); launch_pipeline(T)
```

Independent stories all start at t=0 in parallel. A chain A→B→C serializes *only that chain* while every unrelated story runs concurrently. If `.beads/` exists, `bd ready --json --claim` may supply the frontier (atomic claim against concurrent Conductors); the wave graph is dropped as a primary source.

### One story, end to end

```
pipeline(story S):

  ── stage 1: DEV ────────────────────────────────────────────
  Conductor spawns dev agent(s) for S (individual-agent; N agents if
  multi-domain per routing-table resolution, each file-scoped).
  Dev agent:
    - branches worktree .worktrees/story-{slug} off sprint/{sprint_slug}
      (NOT off main — inherits all merged blockers' code)
    - status: ready-for-dev -> in-progress
    - implements against plain-English ACs (black-box; never reads the
      verifier contract body)
    - emits "implementation-complete + file_list" — nothing more.
  Dev no longer proposes or awaits a merge (old dev/workflow.md merge step
  REMOVED). Merge authority moves to the Conductor.

  ── stage 2: QA + CODE-REVIEW (concurrent within the story) ──
  Conductor spawns, in ONE turn, against the story worktree (fan-out):
    • qa-reviewer       — verifies the story's VERIFICATION CONTRACT
    • bmad-code-review  — adversarial bug hunt (Blind Hunter, Edge Case
                          Hunter, Acceptance Auditor)
  Both read-only / report-only. Both return normalized findings for THIS
  story only. Neither asks the developer anything.

  ── stage 3: FIX (automatic, in-place) ──────────────────────
  If either reviewer returns legitimate findings:
    Conductor spawns ONE code-fixer subagent (single writer) in the SAME
    worktree. It fixes EVERY legitimate finding automatically (no prompt),
    dismisses with rationale, or emits a triage stub for genuinely
    out-of-scope new work. Commits the fixes.
    Optional: /simplify cleanup pass AFTER the fixer (sequential, never
    concurrent with the fixer — it mutates the tree).
    Re-run only the reviewer(s) that raised findings. Loop until clean or
    retry bound (default 3). Leftover/out-of-scope findings recorded on the
    pipeline result for the end-gate to spin into stubs.
  If no findings: skip to merge.

  ── stage 4: MERGE (terminal — the story merges ITSELF) ─────
  Conductor (owns git mutation):
    git rebase sprint/{sprint_slug} story/{slug}    # onto latest sprint
       conflict -> Conductor resolves, or fires a fixer subagent; retry.
    git checkout sprint/{sprint_slug}
    git merge --no-ff story/{slug}
       conflict/failure -> resolve + retry; persistent -> mark blocked.
    status -> review                                 # the story's merge gate
    git worktree remove --force .worktrees/story-{slug}
    git branch -d story/{slug}                        # cleanup is per-story
  Emit { slug, outcome: merged, leftover_findings: [...] }
```

The story reaches `review` at its own merge and stays there until sprint end. `verify`/`done` transitions happen at sprint completion (after AVFL + E2E + approve) but no longer gate any other story's launch — gating is on `>= review`.

---

## 4. Quality gate — QA + code review + fix (per story, pre-merge)

This is the gate *inside* the per-story flow — distinct from the post-merge AVFL pass (which reviews the integrated result). Two reviewers run concurrently against the story diff; their findings converge on one fixer; the story merges only after a clean re-check.

### Tool decision (decision 5)

| Lane | Tool | Mode | Why |
|---|---|---|---|
| **Bug-hunting review** (PRIMARY) | **`bmad-code-review`** | report-only, scoped to story diff | Only existing real adversarial bug hunter (Blind Hunter + Edge Case Hunter + Acceptance Auditor + structured triage). Returns categorized findings that map onto the normalized schema. Does not apply fixes — correct, because fixing is the code-fixer's job. |
| **AC verification** (concurrent) | **`momentum:qa-reviewer`** (rescoped) | read-only, per-story worktree | Reads the verification contract, runs the test command, classifies each AC VERIFIED/PARTIAL/MISSING/BLOCKED with file:line evidence. |
| **Cleanup** (optional, post-fix) | built-in **`/simplify`** | applies fixes | Purpose-built cleanup (reuse, simplification, efficiency, altitude). NOT a bug hunter. Runs *after* the fixer, sequential — never concurrent (it mutates the tree). Keep out of the always-on leg so it doesn't double-mutate code the fixer just touched. |

**Wire `bmad-code-review` report-only, not via `/code-review --fix`:** two reviewers run concurrently and may both surface fixes (e.g. a MISSING-AC finding is also a fix). Routing **all** findings through one code-fixer gives a single writer per worktree (orchestrator-purity), lets the fixer dedupe overlapping findings, and keeps fix provenance in one commit per story.

**Retire the stub.** Delete `skills/momentum/skills/code-reviewer/SKILL.md` and `commands/code-reviewer.md` (or convert the stub into a thin adapter that invokes `bmad-code-review` and normalizes its triage into the finding schema). Replace every `momentum:code-reviewer` invocation in `sprint-dev/workflow.md` and `quick-fix/workflow.md`. **Do not build an in-house reviewer now** — defer to backlog. For high-risk stories, a story field `review_depth: deep` may opt into `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter` instead of the default.

### Concurrent execution (per story, in-worktree)

```
Story worktree (post-dev, code complete, pre-merge)
│
├─ Phase A: CONCURRENT (fan-out — two parallel Agent spawns; they don't talk)
│   ├─ qa-reviewer (read-only)         → verification_contract → qa_findings[]
│   └─ bmad-code-review (report-only)  → git diff scoped → review_findings[]
│
├─ Phase B: CONVERGE → one code-fixer subagent (single writer)
│      input: qa_findings[] + review_findings[]  (deduped, severity-sorted)
│      action: auto-fix ALL routine legitimate findings (no fix/defer prompt for ordinary work);
│              escalate stakes-class findings (security/auth-isolation, irreversible/destructive,
│              high-blast-radius/architecture) as decision cards — NOT silently fixed;
│              apply timing tier: mid-flight if irreversible-and-imminent OR build-invalidating,
│              otherwise end-gate-expanded (default);
│              dismiss only with non-empty recorded rationale; out-of-scope NEW work
│              → triage stub (momentum:triage), don't fix. Commit.
│
├─ Phase C: /simplify (optional cleanup, applies fixes) — AFTER B, sequential
│
└─ Phase D: RE-CHECK gate (always retry on failure — decision 1)
       re-run qa-reviewer test command + ACs
       ├─ clean   → story passes → Conductor merges its worktree
       └─ remains → loop to Phase B. Bounded retries (3). Still failing →
                    BLOCKED → spin a stub via momentum:triage, leave unmerged.
```

Concurrency rules: Phase A is **fan-out** (two independent reviewers, never communicate — per `spawning-patterns.md`, never TeamCreate). The fixer (B) is the single writer. `/simplify` (C) must be strictly after B. Each story runs A→D independently and merges the moment D is clean.

### Normalized finding schema (reviewer → fixer / Conductor contract)

All reviewers normalize to one shape so the fixer and the report consume them uniformly:

```jsonc
{
  "story_slug": "...",
  "source": "bmad-code-review | qa-reviewer | architecture-guard | avfl | e2e-validator | simplify",
  "verdict": "PASS | FAIL | BLOCKED",
  "severity": "blocker|critical | major|high | minor|medium | low",
  "type": "bug | missing-ac | partial-ac | edge-case | drift | integration | cleanup",
  "location": "path:line",            // a component, never "see code"
  "summary": "one line, plain language",
  "detail": "full context — what's wrong AND why it violates the AC/contract",
  "evidence": "the proof: failing test+assertion, diff hunk, or command output",
  "ac_id": "AC2 | null",
  "legitimate": true,                 // legit -> disposition depends on stakes class + timing tier (see below)
  "stakes_class": "routine | security/auth-isolation | irreversible/destructive | high-blast-radius/architecture",
  "timing_tier": "end-gate-expanded | mid-flight",  // end-gate-expanded is the default
  "suggested_fix": "concrete, actionable — never 'see code'"
}
```

**Stakes classes** — every finding carries exactly one:

| Class | Examples |
|---|---|
| `security/auth-isolation` | XSS, auth bypass, credential exposure, permission escalation |
| `irreversible/destructive` | migration, delete, force-push, prod deploy, data truncation |
| `high-blast-radius/architecture` | cross-cutting pattern change, public API break, structural drift |
| `routine` (default) | everything else — bugs, missing ACs, style, cleanup |

**Timing tiers** — two values only:

| Tier | When it applies |
|---|---|
| `end-gate-expanded` | Default. Finding held for end-gate; appears as a decision card at the human surface. |
| `mid-flight` | Narrow exception. Finding escalates immediately ONLY if it is **irreversible-and-imminent** OR **build-invalidating**. No other condition qualifies. |

**Disposition** — the fixer's outcome per finding:

| Disposition | Meaning | Constraint |
|---|---|---|
| `fixed` | Applied automatically; routine findings always land here | Default for routine class |
| `escalated` | Stakes-class finding raised as a decision card (not silently fixed); routed to end-gate-expanded or mid-flight per timing tier | Stakes class only |
| `dismissed` | Fixer judged finding invalid or out-of-scope | **Non-empty rationale REQUIRED** — empty or missing rationale is invalid |
| `triaged-out` | New out-of-scope work; spun into a backlog stub via `momentum:triage` | — |

There is **no `deferred` disposition** — the defer prompt is removed. Routine findings are always auto-fixed (`fixed`). Stakes-class findings are `escalated`, not silently fixed. There is no per-finding fix/defer prompt for ordinary work.

### What this replaces in `sprint-dev/workflow.md`

- **Delete** Phase 4b's `momentum:code-reviewer` (stub) → `bmad-code-review` inside each story worktree, pre-merge.
- **Delete** Phase 4c (consolidated fix queue + developer fix/defer HITL) — violates decision 1.
- **Move** qa-reviewer earlier: from Phase 5 (post-merge main) to Phase A (per-story worktree diff). Its cross-story integration check migrates to AVFL (decision 6).
- **Keep** qa-reviewer's hard constraints: "Reading source is never a substitute for executing tests," MISSING-vs-BLOCKED distinction, mandatory service startup per `e2e-validation.md` when `requires_services: true`.

---

## 5. AVFL — reviewer of the merge

### Role in the new model

AVFL runs **exactly once per sprint, after every story worktree has merged**. Its job is to catch what per-story QA and code-review structurally cannot see: **integration defects** — contradictions between stories, broken cross-references across files two different dev agents touched, duplicated/conflicting implementations, dangling callers, spec-vs-merged drift. It inspects the **merged result via git**, never individual worktrees.

It honors the binding decisions:
- **Never asks the developer anything** (decision 1) — no GATE_FAILED prompt, no MAX_ITERATIONS prompt, no per-finding fix/defer.
- **Always auto-fixes routine legitimate findings** and loops with declining skepticism until clean or non-convergent. Stakes-class findings (security/auth-isolation, irreversible/destructive, high-blast-radius/architecture) surfaced by AVFL are tagged `escalated` and passed to the Conductor as decision cards for the end-gate, not silently auto-fixed.
- It is **not** the end gate. It produces a result object; the Conductor reads it and folds it into the report. Anything AVFL could not resolve becomes a **leftover** the Conductor routes to `momentum:triage` — AVFL never spins stories itself.

This kills the audited contradiction: sprint-dev currently wraps AVFL as a read-only `checkpoint` stop-gate, then runs a *separate* developer-driven fix/defer queue (Phase 4c/4d). That entire HITL queue is deleted; AVFL's native auto-fix loop *is* the mechanism now.

### Why a Workflow, not a prose skill (decision 6)

The loop and phase logic currently live as narrative prose the orchestrating agent must re-interpret every run — the recurring fragility. A Workflow gives:

1. **The loop is structural, not interpreted** — max-iteration bound, skepticism step-down, convergence exit are engine-enforced control flow.
2. **Fan-out is first-class** — the 8 parallel validators become a declared parallel fan-out with a join barrier before consolidation.
3. **State is explicit** — findings, score, iteration counter, fix log are workflow variables, not context the agent must hold across compaction.
4. **Deterministic exit contract** — returns a typed result object the Conductor consumes, not prose to parse.
5. **Model/effort routing survives as step config** — benchmarked optima (Enumerator=sonnet/medium, Adversary=opus/high, Consolidator=haiku/low, Fixer=sonnet/medium) become per-step declarations.

The dimension taxonomy, finding schema, scoring weights, and the four prompt-template families (`validator_system`, `validator_task`, `consolidator`, `fixer` in `framework.json`) are **retained verbatim** as workflow assets. We rewrite the *orchestration*, not the *validation science*.

### Phase structure (Workflow script sketch)

```
WORKFLOW avfl-merge-review
  INPUTS:
    sprint_branch    : string
    base_ref         : string                       # "main"
    story_contracts  : map<slug, VerificationContract>   # decision 10
    merged_stories   : array<{slug, files_touched[]}>    # from merge log
  CONSTANTS:
    LENSES         = [structural, accuracy, coherence, domain]
    MAX_ITERATIONS = 4
    PASS_SCORE     = 95
    SKEPTICISM     = [3, 2, 2, 2]   # declining; floor 2 (avfl-declining behavior)

  STEP gather_merge:
    merged_diff   = git diff {base_ref}...{sprint_branch}      # 3-dot net change
    changed_files = git diff --name-only {base_ref}...{sprint_branch}
    blame_index   = per changed_file, git log -> attribute hunks to owning story
    integration_surface = files touched by >1 story            # highest-risk zone

  iteration = 1
  LOOP while iteration <= MAX_ITERATIONS:
    skepticism = SKEPTICISM[iteration-1]

    # PHASE 1: VALIDATE (parallel fan-out, 8 agents) ───────────
    PARALLEL FAN-OUT over LENSES:
      Enumerator(lens, model=sonnet, effort=medium, ...payload)
      Adversary (lens, model=opus,   effort=high,   ...payload)
    JOIN BARRIER

    # PHASE 2: CONSOLIDATE / DEDUP ─────────────────────────────
    STEP consolidate (model=haiku, effort=low):
      confidence: both reviewers -> HIGH; one -> MEDIUM
      dedup across lenses; verify MEDIUM against contracts; discard no-evidence
      score = 100 − Σ(crit*15 + high*8 + med*3 + low*1)
      classify: INTEGRATION (spans >1 story / in integration_surface) | LOCAL

    # PHASE 3: EVALUATE (no HITL — structural exit) ────────────
    IF score >= PASS_SCORE:               RETURN result(status=CLEAN, ...)
    IF iteration == MAX_ITERATIONS:       RETURN result(status=NON_CONVERGENT, leftovers=...)
    IF no fix last iteration AND score unchanged:
                                          RETURN result(status=NON_CONVERGENT, ...)  # oscillation guard

    # PHASE 4: FIX (auto, never prompts) ───────────────────────
    STEP fix (model=sonnet, effort=medium, run-as=domain_expert):
      apply fixes in severity order in the MERGED TREE on sprint_branch;
      cross-story contradictions resolved toward higher-authority contract;
      unresolved cross-story conflict -> mark unresolved_contradiction, leave for leftovers
      commit "fix(avfl): resolve integration findings — iteration {n}"
    iteration += 1
```

### Result object (contract handed to the Conductor)

```jsonc
{
  "status": "CLEAN | NON_CONVERGENT",     // never GATE_FAILED/WARNING (those were HITL signals)
  "final_score": 96,
  "iterations": 2,
  "scores_per_iteration": [88, 96],
  "fixes_applied": [
    { "id": "ACCURACY-003", "iteration": 1, "severity": "high",
      "owning_stories": ["auth-token-refresh", "session-store"],
      "change": "...", "rationale": "..." }
  ],
  "leftovers": [                            // only when NON_CONVERGENT
    { "id": "DOMAIN-007", "severity": "medium", "confidence": "HIGH",
      "classification": "INTEGRATION", "owning_stories": ["..."],
      "location": "...", "description": "...", "evidence": "...", "suggestion": "...",
      "why_unresolved": "unresolved_contradiction | oscillation | max_iterations" }
  ],
  "commits": ["<sha>", "<sha>"]            // AVFL's own fix commits on sprint_branch
}
```

The Conductor renders **every leftover with full context** into the report's integration section (each leftover carries description + evidence + owning stories + suggestion inline). On approval, leftovers flow to `momentum:triage` as new stubs.

> **Cross-pillar note on the fixer.** The AVFL `fixer` sub-skill historically fixes *artifacts/docs*. For merge-integration findings that touch source code, AVFL should hand off to the **code-fixer** (Section 4 / Section 8), not its internal artifact fixer. Do not conflate the two.

### Placement

Build `avfl-merge-review` as a **Workflow** under the avfl skill (alongside the retained `framework.json` + prompt templates). Keep the existing prose `momentum:avfl` skill for its other callers (`momentum:research` corpus validation, `create-story`) on the `gate`/`checkpoint`/`scan`/`full` profiles — those are not merge reviews. The merge reviewer is a single fixed config (full dual-reviewer + declining-skepticism auto-fix), so hardcoding it as a Workflow is the right altitude.

---

## 6. Git lifecycle

### Owner: the Conductor

All git mutation in the build phase is owned by the **Conductor** — the only actor that runs `rebase`, `merge`, branch/worktree create/remove, or conflict resolution. Dev subagents write and commit inside their worktrees; they never merge. This replaces five HALT/ask gates from the audit with autonomous Conductor logic. **Zero developer HALT exists anywhere in the git lifecycle.** The only developer interaction is the end-gate push confirmation (mandated by git-discipline), which sits at the very end.

The dev skill's `<critical>` "Never auto-execute git merge... wait for explicit user confirmation" is **deleted**. The dev skill no longer merges or cleans up — its merge step reduces to "commit all work in the worktree, emit completion signal." Merge, conflict resolution, and cleanup move entirely to the Conductor. This resolves the audit's finding that the two skills disagreed on the merge gate: there is now exactly one merge authority.

### Branch / worktree topology

| Artifact | Name | Created by | Removed by |
|---|---|---|---|
| Story branch | `story/{slug}` | Conductor (worktree add) | Conductor, after quality gates pass |
| Story worktree | `.worktrees/story-{slug}` | Conductor | Conductor, after quality gates pass |
| Sprint branch | `sprint/{slug}` | sprint-planning (at activation) | Conductor, after sprint→main merge |
| Harness side-effect branch | `worktree-agent-*` | Agent tool harness (unavoidable) | Conductor, force-delete at final cleanup |

Lock files (`.worktrees/story-{slug}.lock`) are **removed** — they coordinated concurrent human-driven dev sessions; under one Conductor there is no cross-session race. The crash-recovery resume/cleanup ask is deleted (see Reconcile below).

### Per-story merge flow

```
merge_story(slug):
    attempt = 0
    loop:
        attempt += 1
        git rebase sprint/{sprint_slug} story/{slug}
        if rebase conflicts:  resolve_conflicts(slug, mode="rebase")
        git checkout sprint/{sprint_slug}
        git merge --no-ff story/{slug}
        if merge conflicts:   resolve_conflicts(slug, mode="merge"); continue
        break
        if attempt >= MAX_MERGE_ATTEMPTS (3):  quarantine_story(slug); return
    # post-merge, this story only:
    git worktree remove --force .worktrees/story-{slug}
    git branch -d story/{slug}
    status-transition {slug} -> review
    re-evaluate dependency graph; spawn newly-unblocked dev agents
```

Both rebase **and** merge steps are conflict-guarded (the audit found the merge step was unhandled). `--no-ff` gives each story an identifiable merge commit, which AVFL relies on to attribute integration findings.

### Conflict resolution (detect → auto-resolve → fire fixer → retry) — decision 9

```
resolve_conflicts(slug, mode):
  1. DETECT  conflicted = git diff --name-only --diff-filter=U
             classify: trivial (imports, lockfiles, generated, status/index.json,
                       pure-additive) vs semantic (overlapping logic edits)
  2. AUTO-RESOLVE trivial (Conductor, directly):
             lockfiles/generated -> regenerate or take target-side
             status/index.json   -> re-derive from authoritative source (sprint-manager)
             pure-additive       -> union-merge; git add resolved paths
  3. FIRE FIXER if semantic paths remain:
             spawn ONE dev/code-fixer subagent (change_type matched via routing
             table) with: conflicted files (markers in place) + BOTH stories' ACs +
             instruction to resolve preserving both intents, then stage.
  4. FINALIZE rebase --continue | commit --no-edit; verify no markers remain;
             if still dirty -> abort this attempt (--abort) and let merge_story retry.
```

Any unexpected git failure loops `merge_story` up to `MAX_MERGE_ATTEMPTS = 3`. Between attempts the tree is reset to clean via `--abort`, so retries start from a known-good point.

### Quarantine (replaces HALT) — decision 2

If a story cannot merge after 3 attempts, the Conductor does **not** halt:
1. Leave `.worktrees/story-{slug}` and `story/{slug}` intact (work preserved).
2. Record `merge-blocked` with captured conflict detail (files, markers, both intents).
3. Continue merging the other independent stories.
4. At the report, surface the quarantined story in full context (the conflicting hunks + both intents inline, per decision 8).
5. At approve, spin a new stub via `momentum:triage`; transition the original story to `closed-incomplete`.

### AVFL handoff (decision 6)

After all per-story merges, `sprint/{slug}` holds the integrated result. git-lifecycle hands AVFL a clean **3-dot** inspection (fixing the audited boundary-diff issue):

```
merge_base    = git merge-base main sprint/{sprint_slug}
merged_diff   = git diff {merge_base}...sprint/{sprint_slug}     # net integrated change
merge_commits = git log --merges {merge_base}..sprint/{sprint_slug} --oneline
```

AVFL receives `merged_diff` (the thing the developer will actually ship) plus the `--no-ff` merge commits so it can attribute integration issues to specific story merges.

### Sprint → main merge (end gate only)

```
on developer approval at end gate:
    triage leftover AVFL/E2E findings -> stubs (momentum:triage)
    git checkout main
    git merge --no-ff sprint/{sprint_slug}
    if conflicts: resolve_conflicts("sprint", mode="merge"); retry   # SAME flow, no HALT
    git branch -d sprint/{sprint_slug}
    git branch -l 'worktree-agent-*' | xargs -r git branch -D        # harness orphans
    git log @{u}..HEAD --oneline                                     # git-discipline rule
    -> push requires developer's explicit OK (the one retained gate)
```

### Reconcile on start (replaces crash-recovery ask)

Before build, the Conductor reconciles git state non-interactively:
- For each story slug: if `story/{slug}` or `.worktrees/story-{slug}` exists from a prior crashed run, `git worktree remove --force` + `git branch -D` and recreate fresh (no resume prompt — dev re-implements deterministically from the story file).
- `git worktree prune`; force-clean pre-existing `worktree-agent-*` orphans.

---

## 7. Planning → dev handoff: the verification contract (decision 10)

Sprint-planning is the **sole authority** on how each story is verified. It decides the method per story (closed enum, not free text), emits a per-story verification contract, and hands it to the build flow. Dev, QA, and the fixer loop **consume** it and **never decide** verification. This removes the two-signal ambiguity (`verification_method` free-text vs. `change_type` routing).

### Verification method is an enum, decided at planning

`verification_method` becomes a **closed enum keyed to the harness driver-binding keys**, so there is exactly one routing signal:

| `verification_method` | Contract file | `driver_bindings` key | Driver | Source change-types |
|---|---|---|---|---|
| `skill-invoke` | `.eval.yaml` | `skill-invoke` | `Skill` | `skill-instruction`, `agent-definition` |
| `behavioral-trigger` | `.trigger.md` | `behavioral-trigger` | `cmux` | `rule-hook` |
| `bash` | `.smoke.sh` | `bash` | `cmux` | `script-code`, `script-cli`, `backend` |
| `smoke-ui` | `.feature` | `smoke` | `Maestro`/`Playwright` | `app-ui` |
| `curl` | `.smoke.sh` | `curl` | `curl` | `backend` (HTTP) |
| `document-review` | `.review.md` | `document-review` | `null` (human/AI read) | `specification`, `research-spike`, `config-structure` |

**Planning sets it, not create-story.** Sprint-planning computes `verification_method` from the story's `change_type` set using the existing precedence weighting (`app-ui > script-code > script-cli > backend > agent-definition > skill-instruction > rule-hook > config-structure > specification > research-spike`); the winning change-type maps to exactly one enum value. `change_type` is an *input*; `verification_method` is the committed *output*. The `contract-format-guide.md` "Harness driver" column (`shell-executor`, `hook-trigger`, `document-reviewer`) is **stale** and must be rewritten to the real keys (`bash`, `behavioral-trigger`, `document-review`) the live contracts already use.

### The contract: two-part structure

One contract per story, frozen at planning, at `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Every contract gains a mandatory **dev-readable header** so it serves both the verifier and the dev. The old `<critical>` rule ("dev agents never access this path") is **removed**.

**Part A — Dev-Readable Verification Header** (new; identical schema across all formats):

```yaml
# === VERIFICATION HEADER (dev + QA both read this) ===
story_slug: b2-create-story-input-routing-read-epic-context
verification_method: skill-invoke          # the enum — the ONE routing signal
harness_profile: skill-invoke               # == driver_bindings key, == verification_method
contract_path: .momentum/sprints/sprint-2026-05-26/specs/b2-...eval.yaml
how_dev_self_checks: |                       # plain-language; decision 8 "full context"
  Before you signal done, invoke `momentum:create-story` against an epic that
  has context X and confirm the output reflects the epic, not the legacy feature.
  The exact scenarios you must satisfy are in `scenarios:` below. Run them
  yourself; do not delegate the judgment.
coverage_disposition: dedicated-run          # or: covered-by-composition
covered_by_scenario: null                    # integration-scenario id if composition
acceptance_criteria_ref: .momentum/stories/b2-...md#acceptance-criteria
platforms: [host]
```

**Part B — Verifier Contract Body** (existing per-format black-box contract, unchanged in spirit): `scenarios:` for `.eval.yaml`, assertion script for `.smoke.sh`, trigger/outcome for `.trigger.md`, required-claims for `.review.md`, Gherkin for `.feature`. Still black-box / Outsider-Test clean — Part A's `how_dev_self_checks` is the only place insider phrasing ("before you signal done") is allowed.

Both parts in one frozen file is the contract of record. Dev reads Part A; QA/verifier reads Part B (authoritative pass/fail). They cannot diverge because they are the same file.

### Coverage plan

`coverage-plan.md` remains the sprint-wide routing artifact. Its per-story disposition is **denormalized into each contract's `coverage_disposition` / `covered_by_scenario`** so the build flow doesn't parse prose. This tells the flow whether a story gets a dedicated verification run during build, or is discharged later by an integration scenario at AVFL/merge.

### Sprint-record schema: assignment carries the contract pointer

Written by `momentum:sprint-manager` (sole writer of `sprints/index.json`):

```jsonc
"story_assignments": {
  "b2-create-story-input-routing-read-epic-context": {
    "role": "dev",
    "specialist": "dev-skills",
    "guidelines": ".claude/rules/dev-skills.md",
    "change_type": ["skill-instruction"],
    "verification_method": "skill-invoke",     // canonical, top-level, closed enum
    "contract": {
      "path": ".momentum/sprints/sprint-2026-05-26/specs/b2-...eval.yaml",
      "harness_profile": "skill-invoke",        // must == verification_method
      "coverage_disposition": "dedicated-run",
      "covered_by_scenario": null,
      "frozen_sha256": "<hash of the contract file at activation>"
    },
    "can_merge_independently": true
  }
}
```

`frozen_sha256` lets the build flow assert the contract was not mutated between planning and build. `can_merge_independently` supports decision 4 — planning sets it `true` for any story with no hard dependency; it flips `false` with a populated `depends_on` only when a hard dependency forces wave ordering.

### How the per-story flow reads the handoff

No verification decisions are made here:
1. **Resolve assignment** from `story_assignments[slug]`.
2. **Verify freeze:** `sha256(contract.path) == contract.frozen_sha256`. Mismatch → halt and surface to the Conductor (do not silently re-verify against a changed contract).
3. **Dev consumes Part A** — its acceptance target is `how_dev_self_checks` + the contract body's observable clauses. Dev never authors or alters the contract, and never chooses how it is verified.
4. **QA/verifier consumes Part B** — verifier selected purely by `verification_method` → `driver_bindings[method].driver`. If `coverage_disposition: covered-by-composition`, the dedicated run is skipped at build time and discharged later by the named integration scenario at AVFL/merge.
5. **Fixer loop** — on fail, the fixer (decision 1: always auto-fix) gets Part A + the failing Part B clauses and iterates until the frozen contract passes.

### Required changes

- `create-story/workflow.md`: stop writing prose `verification_method`; if retained, it is advisory, not a routing key.
- `sprint-planning/workflow.md`: compute the enum `verification_method` from `change_type` precedence; write the Part A header into every contract; denormalize coverage disposition into each header; write the formalized `story_assignments[]` schema (incl. `contract{}` + `can_merge_independently`).
- Remove the `<critical>` "dev agents never access specs/" rule.
- `contract-format-guide.md`: rewrite the stale "Harness driver" column to real `driver_bindings` keys; add the Part A header schema as mandatory.
- `verification-harness.json`: no schema change — `contract_extensions` and `driver_bindings` keys already align; the enum is defined to equal these keys so the JSON stays the single source of truth.

---

## 8. The single HITL gate — the Conductor end-gate

### Principle

Sprint-dev has **one primary HITL surface: the Conductor end-gate**, which is the default and the safety net. Every intermediate `<ask>`, HALT, and per-finding fix/defer prompt for routine findings is removed. The build phase, AVFL, E2E, and all fix loops run autonomously. The developer is engaged at the end — after merge and all validation — through a single open-ended conversational gate that resolves to **"we need changes"** or **"approve"**. There is no Reject. The only other touchpoint is the push confirmation, folded into approve.

**Mid-flight escalation tier (narrow exception, not the default):** A stakes-class finding may escalate mid-flight — bypassing end-gate deferral — ONLY if it meets the strict bar: **irreversible-and-imminent** OR **build-invalidating**. No other condition widens this tier. The three stakes classes that qualify a finding for consideration: security/auth-isolation, irreversible/destructive (migration, delete, force-push, prod deploy), high-blast-radius/architecture. A finding in one of these classes that does NOT meet the mid-flight timing bar is held for end-gate expansion (the default). End-gate expansion is the norm and safety net; the mid-flight tier is the rare exception. Routine findings are always auto-fixed silently and never surface mid-flight.

### What is removed

| Audit item | Disposition |
|---|---|
| Session resumption ask (Resume/Reset) | **Removed.** Stale in-progress stories auto-reset to `ready-for-dev` and re-dispatched. |
| Dev-agent failure ask (Retry/Skip/Halt) | **Removed.** Auto-retry (bounded); exhausted → `blocked`, build continues; spun to a stub at approve. |
| AVFL acknowledgement wall | **Removed.** Findings flow straight into the autonomous fix loop. |
| Consolidated fix queue (per-finding fix/defer) | **Removed for routine findings.** Routine findings always auto-fixed. Stakes-class findings are escalated (decision cards), not prompted per-finding. |
| Remaining-findings ask (Accept/fix/defer) | **Removed.** The autonomous loop iterates to convergence (bounded). |
| Team-review findings ask | **Removed.** Same loop. |
| Verification checklist ask | **Removed as a gate.** Gherkin results become a read-only report section; `done` is driven by approve. |
| H1–H5 pre-flight HALTs (no sprint / not activated / approvals / stalled) | **Retained as Phase-1 pre-flight HALTs** — "cannot start" guards, fire before any work; not part of the Conductor loop. |
| Story-merge / main-merge conflict HALTs | **Removed.** Conductor resolves (decision 9). |
| Push ask | **Retained, folded into approve.** |
| Retro convenience ask | **Retained** (post-completion convenience, not a gate). |

### The Conductor end-gate

```
state ConductorGate:
  report = render_html_report(sprint_state)
  surface report to developer
  loop:
    dev_input = open conversation (free-form; no menu)
    intent    = classify(dev_input)   # changes | approve | question
    switch intent:
      question:
        answer using sprint state, diffs, findings, story specs.
        UPDATE the report in place if the answer adds needed context (decision 8).
        regenerate affected sections; continue loop
      changes:
        run CHANGE_WORKFLOW(scope = dev_input)
        report = render_html_report(sprint_state)   # full re-render
        surface; continue loop
      approve:
        run APPROVE_SEQUENCE()                        # terminal
        break loop
```

**Two outcomes only.** `changes` loops back through the fix-workflow and re-renders; `approve` is terminal. `question` is the conversational substrate — the gate stays open, answering and updating, until the developer issues `changes` or `approve`. Ambiguous input defaults to `question` (never silently approve or mutate).

### The change-workflow (one workflow — build-fix AND developer-requested changes) — decision 3

```
CHANGE_WORKFLOW(scope):
  # scope: findings (autonomous, build phase) | request (Conductor gate)
  items = resolve_items(scope)
  for each item (parallel where independent):
    spawn code-fixer subagent with: item, target branch, story context
  await all fixers
  re-run only the affected validators (AVFL lens / E2E scenario / review) on changed files
  if residual legitimate findings AND iterations < MAX_FIX_ITERATIONS: recurse
  resolve any merge conflicts (Conductor self-resolve or fixer; retry)
  return change_summary
```

No developer prompt inside the loop. Bounded iteration; on hitting the cap, residual items become report entries and stub candidates at approve. When invoked from the gate (`scope = request`), the natural-language request is parsed into discrete directives, each dispatched as a fixer item exactly like a finding. Conflict resolution lives here, not in a HALT.

### The approve sequence (terminal) — decision 2

```
APPROVE_SEQUENCE():
  # 1. Triage leftovers + discovered work into stubs
  leftovers = blocked/never-completed stories + capped/residual findings
            + unconfirmed scenarios + new work surfaced in conversation
  if leftovers: invoke momentum:triage with the pre-enumerated list
                # triage classifies each (ARTIFACT->intake stub / DECISION / SHAPING /
                # DEFER / REJECT); ARTIFACTs become backlog stubs via momentum:intake

  # 2. Close every story one way or another (no story stays open)
  for each story:
    if completed-and-validated -> done
    if blocked/never-completed  -> closed-incomplete   # replacement stub already created

  # 3. Merge to main and complete
  run sprint complete; merge sprint branch -> main (Conductor resolves conflicts; retry)
  branch cleanup

  # 4. Push (the one retained confirmation)
  show git log @{u}..HEAD --oneline; confirm push; on confirm: git push
```

### Blocked / never-completed and newly-discovered work

A story never blocks closure and never stays open. During build, a dev that exhausts retries marks `blocked` and the build continues. At the report, every blocked story appears in its own section with full context. At approve, it is fed to `momentum:triage` → `momentum:intake` creates a fresh backlog stub (not a story in this sprint); the original transitions to `closed-incomplete`. Newly-discovered work that is *not* a change to existing sprint work is likewise collected and passed to triage at approve — keeping the sprint's scope fixed while capturing discovery as stubs.

---

## 9. The HTML report (HITL surface) — decision 8

The single HITL artifact: a self-contained `.html` written to `.momentum/handoffs/<sprint-slug>-hitl-report.html`, produced after all merges + AVFL + E2E. The developer reads it top to bottom and copies back a `changes` or `approve` prompt.

### CORE MANDATE — total per-section self-sufficiency (the rule the old template lacked)

> Every section must carry **all** context required to make the decision in that section, written for a developer who has **not** been watching the sprint and has **no** access to the code, the spec, or prior report versions. A section is invalid if a competent reader would have to open a file, grep a symbol, recall a prior conversation, or read another section to understand it.

Every finding, decision, scorecard row, and deferred item MUST inline:
1. **What** — plain language (not a code symbol as the headline).
2. **Where** — file + function/line, as supporting detail *after* the plain-language statement.
3. **Why it matters** — the concrete observable consequence ("`history` shows 1 event instead of 2"), not an abstraction ("data integrity issue").
4. **Evidence** — the actual proof (failing test + assertion, diff hunk, command output, AVFL finding text), quoted inline, not linked.
5. **Options + trade-offs** — for anything requiring a decision: each option with cost and benefit (tucked in `<details>` if long, but present).
6. **Recommendation** — the Conductor's pick with a one-line rationale.

The audit's banned failure case — `b1 — stories_remaining counted review status (ad-hoc 14→5)` — becomes a self-contained card:

> **The "stories remaining" count was inflated by stories already in review.** In `momentum-tools.py → count_remaining()`, stories with `status: "review"` were counted as remaining. *Consequence:* the ad-hoc epic reported 14 remaining when only 5 were open — a ~3× overcount. *Evidence:* `test_remaining_excludes_review` failed with `assert 14 == 5`; passes after the fix. *Fix applied:* `review` excluded from the remaining set. *Status:* auto-fixed and re-validated, no decision needed — shown for transparency.

### Authoring discipline — per-item self-sufficiency checklist (Conductor pre-flight, not shipped)

```
PER-ITEM SELF-SUFFICIENCY CHECKLIST (item: __________)
[ ] Plain-language headline (no bare code symbol as the title)
[ ] What it is — for someone who hasn't seen the code
[ ] Where — file + function/line as supporting detail
[ ] Why it matters — as an observable consequence
[ ] Evidence inlined — failing test/assertion, diff, or command output quoted, not linked
[ ] If a decision: every option present, each with cost + benefit
[ ] If a decision: a recommendation with one-line rationale
[ ] No unexplained acronym, ticket id, or symbol left dangling
[ ] No "see code", "see spec", "as discussed", "per above"
VERDICT: [ ] ships  [ ] rewrite
```

### Required sections (fixed order)

```
HERO  Sprint slug · review version (v1/v2/…) · one-line subtitle · status pill ·
      metrics strip (stories merged X/Y · tests passing · defects auto-fixed ·
      decisions for you · leftovers to triage)

01 Sprint summary        What the sprint set out to do + what actually shipped (2–4 sentences).
02 Per-story scorecard    One self-contained row per story: title, what it did, verification
   with evidence          method (from the verification contract), pass/fail per gate, the
                          EVIDENCE (test names/counts, E2E result), independent merge timestamp.
03 Quality-gate findings  Every finding from QA, code-review, AVFL, E2E — each a self-contained
   (full context)         card per the CORE MANDATE. Grouped by gate, severity-sorted. Auto-fixed
                          findings shown with their fix + re-validation ("no decision needed").
03-D Dismissed findings   **[D3 — Required]** Every finding the fixer dismissed, rendered as a
   (legible auto-fix)     self-contained card: what was dismissed, the non-empty rationale, and
                          why it was judged invalid/out-of-scope. The auto-fix loop must be legible
                          about what it dismissed, not only what it changed. Never omit or collapse
                          dismissed items — empty-state renders "Nothing dismissed this cycle."
04 Decisions needing you  Stakes-class findings (security/auth-isolation, irreversible/destructive,
   (fully contextualized)  high-blast-radius/architecture) that were escalated appear here as
                          decision cards, not in the auto-fixed section. Each: background panel +
                          the contradiction/question + options-with-tradeoffs (<details>) +
                          recommendation + a <choices> radio group. Mid-flight escalations that
                          resolved before the end-gate appear with their resolution noted inline.
05 Deferred items         Each with what, why safe to defer, and what triaging later costs.
                          Become triage stubs on approval. Empty-state if none.
06 Blocked / incomplete   Any story that didn't complete; what blocked it + recovery path.
                          On approval these spin out as stubs via momentum:triage. Empty-state if none.
07 Merge & push preview   Commits ahead of main/origin, full test totals, the exact approval
                          sequence, and the explicit note that PUSH IS A SEPARATE CONFIRMATION.
GATE  Single end-gate control (changes vs approve) + copy-decision-as-prompt.
```

### Schemas

**Per-story scorecard row (02):**
```jsonc
{ story_slug, title,
  what_it_did:        "1–2 plain sentences — the change in the world, not the diff",
  verification_method:"From the contract: e.g. 'unit tests on fold logic + manual: run
                       momentum-tools status, confirm open count matches'",
  gates: { dev, qa, code_review, avfl, e2e },   // pass | fail | n/a
  evidence:           "658 unit tests green incl. test_fold_replay; E2E '…' passed",
  defects_found_fixed: N,                         // detailed in section 03
  merged_at:          "ISO timestamp — proves the independent per-story merge" }
```

**Decision card (04) — the only interactive content:**
```jsonc
{ id, title: "Plain-language QUESTION as the headline, not a symbol",
  severity_chip,
  background: "Self-contained panel; define every term; no assumed context",
  the_call:   "The contradiction/fork: what's true now, what the spec says, why they differ",
  blocks_sprint: true|false,
  options: [ { value, label, cost, benefit } ],   // EVERY option, each with both
  recommendation: { value, one_line_why },
  choices_radio_group: value }
```

### Empty-state rule

A section with no items renders an explicit contextualized empty state (never blank, never omitted) — itself decision-relevant context:
```html
<section><h2><span class="num">05</span>Deferred items</h2>
  <div class="panel empty">Nothing was deferred this cycle — every finding was
  either fixed or surfaced as a decision above.</div></section>
```

### The single end-gate control

Reuses the existing template's `.final` pair + `paint()`/`val()`/`buildPrompt()`/`copyPrompt()`/`toggleOut()` JS; the two terminal choices map to decision 2:
- **`✓ Approve & finish`** → on paste-back: triage leftovers → stubs, transition completed stories → done, sprint complete, merge sprint → main, then ask before push.
- **`⟲ Request changes`** → on paste-back: run ONE change-workflow over the developer's specified fixes; re-issue the report as the next version. No merge to main.

No Reject, no Hold-forever. `buildPrompt()` assembles a newline-bulleted natural-language prompt: gate choice as head line, one bullet per decision-card selection; when `changes` is selected, a free-text `<textarea id="changes">` is appended verbatim (the change-workflow's scope). `copyPrompt()` writes to `#out`, copies, flashes "✓ copied — paste it back to me."

**D4 — Anti-rubber-stamp forcing function [Required]:** The end-gate is structured so the human cannot trivially rubber-stamp it when stakes-class items are present. Implementation requirements:
- The `✓ Approve & finish` button is **not pre-checked** and is **disabled** when unresolved stakes-class decision cards are present in section 04.
- Each stakes-class decision card in section 04 requires **explicit per-card acknowledgment** (a radio selection or explicit choice) before the Approve control enables.
- Routine auto-fixed items (section 03) require no per-card action — they collapse and need nothing.
- The `buildPrompt()` function includes each acknowledged card choice in the submitted prompt, creating an audit trail of which stakes items the developer explicitly reviewed.
- If no stakes-class items are present (section 04 is empty), the Approve control enables normally — the forcing function activates only when it has something stakes-class to force attention onto.

### Live conversation + template/data separation

Per decision 8 the report is a **fully open conversation** — the Conductor stays available, answers questions, and **rewrites the report file in place** when asked for more context; the developer reloads. So the report must be cheap to regenerate: it is **data-driven**, not bespoke prose.

- **Data** — one in-memory report object the Conductor assembles from: verification contracts (per-story method), per-story flow results (gates + evidence + merge timestamps), QA/code-review/AVFL/E2E findings, git preview (`git rev-list --count`, test totals).
- **Template** — fixed HTML skeleton + the carried-forward `:root` token block, component CSS (`.hero`, `.metrics`, `.metric`, `.pill`, `.sev.*`, `.panel`, `.decision`, `.item`, `.choices`, `.final`, `.out`, `<details>` caret) and the five JS functions.
- **Self-sufficiency enforced at the data layer** — every finding/decision/row object has required non-empty fields (`what`, `why`, `evidence`; decisions add `options[]` + `recommendation`). An object missing a required field is a *build error*, not a rendered-empty card. This makes "no terse shorthand" a system property, not a hope.

**House style (carried forward verbatim):** self-contained single `.html`, zero external dependencies (inline `<style>` + `<script>`, no CDN/fonts/images, per `anthropics/html-effectiveness`). Anthropic warm palette, three font stacks, radius/border/shadow tokens, numbered sections, severity chips, `<details>` disclosure. Reference: `.momentum/handoffs/sprint-2026-05-26-hitl-report.html`.

### D5 — Decision-grade presentation standard [Required]

The report applies a practice-wide "decision-grade presentation" standard that reconciles two competing mandates: cut irrelevant material (Specification Fatigue source) while guaranteeing sufficient context to decide without leaving the report (self-sufficiency mandate from decision 8). The standard is: **tight on the irrelevant, complete on the decision-relevant.**

**Presentation caps (upper bounds — cut irrelevant material):**
- Per auto-fixed finding (section 03): summary ≤ 3 sentences; evidence quoted inline ≤ 10 lines; longer evidence in a `<details>` block.
- Per dismissed finding (section 03-D): reason ≤ 2 sentences; no reproduction steps unless they constitute the rationale.
- Per decision card (section 04): background panel ≤ 150 words; options list ≤ 3–5 items; each option ≤ 1 cost + 1 benefit sentence. Use `<details>` for anything beyond these caps.
- Sprint summary (section 01): 2–4 sentences; no enumeration of every story name.
- Scorecard row (section 02): `what_it_did` ≤ 2 sentences; evidence ≤ 1 line summarizing test counts + outcome.

**Self-sufficiency floor (lower bounds — decision context must stay inline):**
- Every decision card (section 04) MUST carry `what / why / evidence` inline — the human must never be sent to reference another file, the spec, or a prior conversation to make a call.
- Every dismissed finding (section 03-D) MUST carry the non-empty rationale inline — "see code" or "context-dependent" are not rationales.
- Every blocked/incomplete story (section 06) MUST carry what blocked it and the recovery path inline.
- The self-sufficiency checklist (§ "Authoring discipline" above) is the gate — any item that fails the checklist is a build error, not a rendered-empty card.

**Conflict resolution:** When the cap and the floor conflict (the decision context required exceeds the cap), the self-sufficiency floor wins. The cap cuts *irrelevant* material; it never cuts decision-relevant context.

---

## 10. Agent gap map

Status legend: **REAL** = working body exists · **STUB** = file exists, placeholder body · **MISSING** = no file · **ORPHAN** = real body, nothing spawns it · **PROSE→WF** = exists, must be rewritten as a Workflow.

| Role (redesign needs) | Where today | Status | Blocking? | What to build / fix |
|---|---|---|---|---|
| **conductor** — owns end gate, writes/updates HTML report, answers live, triages leftovers, merges to main, pushes | nothing | **MISSING** | **P0 — hardest block.** Decisions 2/8/9 hang off it. | New `skills/momentum/skills/conductor/` (orchestrator skill + `workflow.md`). Owns the single HITL. Spawns merge-resolver/fixer for conflicts, invokes triage, runs `git push` only with approval. |
| **code-reviewer** — adversarial bug hunt, read-only | `skills/.../code-reviewer/SKILL.md` (stub) | **STUB** | **P0 (decision 5).** | **Do not build in-house.** Wire `bmad-code-review` as the per-story reviewer. Convert the stub into a thin adapter that invokes it against the story diff and normalizes triage into the finding schema. |
| **code-fixer** — applies findings to *merged source code*, always auto-fixes, retries | only `avfl/sub-skills/fixer` (artifacts, not code) | **MISSING (for code)** | **P0.** Decisions 1 + 3 + 4. | New `skills/momentum/agents/code-fixer.md` (write-capable). Consumes `findings[]`, applies every legitimate fix, retries, commits, emits structured output. Reuses dev.md's commit + output blocks. Also the change-workflow worker and the merge-conflict resolver. |
| **dev** — per-story executor in own worktree | `agents/dev.md` (REAL) | **REAL** | scope change | Keep. Remove its merge/cleanup/lock/crash-ask responsibilities (move to Conductor). Add: dev reads the verification contract's Part A header (decision 10). Terminal output = implementation-complete + file_list. |
| **dev-skills** — SKILL.md / workflow / agents specialist | `agents/dev-skills.md` | **REAL** | none | Keep — the only specialist relevant to Momentum's own repo; the likely default specialist here. |
| **dev-build / dev-frontend** (Gradle/Kotlin, Compose) | `agents/dev-build.md`, `agents/dev-frontend.md` | **REAL but stack-coupled** | low | Irrelevant to Momentum's markdown/bash repo. Leave; flag against DEC-026 (generic base + project guidelines). Out of scope this sprint. |
| **qa-reviewer** — AC verification | `agents/qa-reviewer.md` (REAL) | **REAL** | scope change | Keep. Rescope from "post-merge on main, whole sprint" → "single story worktree diff vs that story's verification contract", run concurrently in stage 2. Cross-story integration check migrates to AVFL. |
| **e2e-validator** — behavioral validation | `agents/e2e-validator.md` (REAL) | **REAL** | none | Keep (decision 7). Stays sprint-level, runs against the merged result after AVFL. Harness-driven; the per-story contract populates/extends `verification-harness.json`. |
| **architecture-guard** — drift vs decisions | `skills/.../architecture-guard/SKILL.md` (REAL) | **REAL** | none | Keep. Runs against the merged diff alongside e2e-validator. Read-only PASS/FAIL — feeds the report, never auto-blocks. |
| **avfl** orchestrator — reviewer OF THE MERGE | `skills/.../avfl/SKILL.md` (prose) | **PROSE→WF** | medium | Rewrite as a Workflow (decision 6); retarget from artifact validation to inspecting the merged git result. |
| **avfl lenses** — validator-enum / validator-adv / consolidator / fixer | `avfl/sub-skills/*` (REAL) | **REAL** | none | Keep all four. The AVFL `fixer` fixes *artifacts* — for merge-integration *code* findings, hand off to the new **code-fixer**, do not conflate. |
| **merge-resolver** — resolves worktree→sprint and sprint→main conflicts | nothing | **MISSING** | **P1 (decision 9).** | No new base body. Conductor resolves trivial conflicts inline; for semantic, fires the **code-fixer** as the conflict-resolution worker (it has Edit/Bash/commit). Merge failure → retry. |
| **triage** — leftovers / new work → stubs | `momentum:triage` (REAL) | **REAL** | none | Keep. Conductor invokes it at the approve branch. Accepts a pre-enumerated list from a caller; ARTIFACT → `momentum:intake` stub. No Reject path. |
| **routing roles: architect / pm / sm** | `agents.json` → 3 dead paths | **MISSING bodies** | P2 | `agents.json` maps these to nonexistent files. Create the bodies or delete the dead entries. Not needed for the redesign to run — cleanup. |
| **analyst / researcher / ux** | real bodies | **ORPHAN** | none | Out of sprint-dev scope; nothing spawns them. Leave; note for a separate composition-pipeline effort. |

### Build order (most-blocking first)

1. **code-reviewer adapter → `bmad-code-review`** (P0) — unblocks the per-story review leg; lowest effort (wraps an existing real bug hunter).
2. **code-fixer base body** (P0) — required by the per-story fix step, the change-workflow loop, and (reused) merge-conflict resolution.
3. **conductor skill + HTML report template** (P0) — the single end gate, report-as-conversation, triage/merge/push. Largest new build; everything post-merge depends on it.
4. **Rescope qa-reviewer to per-story worktree + teach dev to read the verification contract** (P1) — small prompt edits to real agents.
5. **AVFL prose → Workflow, retargeted at the merged git result** (P1) — mechanical rewrite; sub-agents reused; integration findings → code-fixer.
6. **merge-resolver wiring** (P1) — Conductor-inline first, escalate to firing code-fixer; no new base body.
7. **Cleanup `agents.json`** dead `architect`/`pm`/`sm` paths (P2) — not required for the redesign to run.

---

## 11. What is removed vs kept (consolidated)

| Old (waves) | New (per-story pipeline) |
|---|---|
| Phase 2↔3 global wave loop | Conductor event-driven frontier |
| Wave barrier on `done` | Per-story gate on own `depends_on >= review` |
| Global AVFL stop-gate after all merge | AVFL kept; runs once post-merge over the integrated branch, as a Workflow |
| Per-story code review as a global Phase 4b | Code review inside each story's stage 2 (`bmad-code-review`) |
| Consolidated fix queue + per-finding fix/defer ASK | Automatic in-place fix inside stage 3; no prompt |
| Deferred global worktree cleanup (Phase 4d) | Per-story cleanup at the story's own merge |
| Per-failure Retry/Skip/Halt ASK | Automatic bounded retry; persistent failure → `blocked` + continue |
| Rebase/merge conflict → HALT | Conductor resolves or fires fixer; retry; never halt |
| `dev` proposes & awaits merge | `dev` returns implementation-complete only; Conductor merges |
| Just-in-time `.feature` discovery in Phase 6 | Verification contract authored at sprint-planning, consumed per story |
| `momentum:code-reviewer` (stub) invoked as real | `bmad-code-review` for bugs; `/simplify` for optional cleanup |
| AVFL fed a `git log` boundary diff | AVFL fed a 3-dot merged diff + merge-commit list |
| 5 `<ask>` + 2 fix-loop asks + push ask + retro ask + 8 HALTs | 1 decision gate (changes/approve) + folded push confirmation + retro offer + Phase-1 pre-flight HALTs only |

---

## 12. Files this redesign touches

| File | Change |
|---|---|
| `skills/momentum/skills/sprint-dev/workflow.md` | Replace the wave loop + global Phases 3–7 with the Conductor build phase + AVFL-on-merge + E2E + end-gate; retain Phase-1 pre-flight HALTs only; switch AVFL capture to 3-dot diff. |
| `skills/momentum/skills/dev/workflow.md` | Strip merge gate, cleanup, lock, crash-ask; reduce to worktree-local commit + completion signal; add Part-A header consumption. |
| `skills/momentum/agents/dev.md` | Remove the `<critical>` no-auto-merge rule; remove merge/cleanup authority. |
| `skills/momentum/skills/conductor/` (new) | New orchestrator skill + `workflow.md` — owns the end gate, report, change-workflow, approve sequence, all git mutation. |
| `skills/momentum/agents/code-fixer.md` (new) | New write-capable fixer base body. |
| `skills/momentum/skills/code-reviewer/SKILL.md` | Convert stub → thin `bmad-code-review` adapter (or delete + repoint callers). |
| `commands/code-reviewer.md` | Delete or repoint. |
| `skills/momentum/agents/qa-reviewer.md` | Rescope to per-story worktree + verification contract. |
| `skills/momentum/agents/e2e-validator.md` | Keep; runs against merged result; consumes harness contract. |
| `skills/momentum/skills/avfl/` | New `avfl-merge-review` Workflow alongside retained `framework.json` + prompt templates; keep prose skill for other callers. |
| `skills/momentum/skills/sprint-planning/workflow.md` | Compute enum `verification_method`; write Part-A headers; denormalize coverage; write formalized `story_assignments[]`. |
| `skills/momentum/skills/create-story/workflow.md` | Stop writing prose `verification_method` as a routing key. |
| `skills/momentum/skills/sprint-manager/` | Write the formalized `story_assignments[]` schema incl. `contract{}` + `can_merge_independently`. |
| `contract-format-guide.md` | Rewrite stale "Harness driver" column to real `driver_bindings` keys; add Part-A header schema. |
| `skills/momentum/skills/quick-fix/workflow.md` | Repoint `momentum:code-reviewer` → `bmad-code-review`. |
| `momentum/agents.json` | Create or delete dead `architect`/`pm`/`sm` paths (P2). |

---

## 13. Open questions for the developer

1. **`/simplify` placement.** It is specified as an *optional* post-fix cleanup pass inside each story's stage 3. Should it run automatically on every story, only on stories above a size/diff threshold, or only when the developer explicitly asks at the end-gate? (It mutates the tree and adds latency/cost per story.)

2. **Retry bounds.** Two bounds are proposed with different defaults: dev/pipeline retry = 2, merge attempts = 3, fix-loop iterations = bounded ("3" in one section, `MAX_FIX_ITERATIONS` unspecified elsewhere). Confirm the canonical numbers, or whether they should be configurable per sprint.

3. **`bmad-code-review` scaffolding.** It expects `_bmad/bmm/config.yaml`. Does that exist in Momentum's repo, or does the adapter need to supply a minimal config? If absent, this is a hidden P0 sub-task on the code-reviewer adapter.

4. **AVFL on a clean merge.** If no per-story pipeline produced *any* integration-surface change (e.g. all stories touched disjoint files), should AVFL still run the full 8-validator loop, or short-circuit to CLEAN when `integration_surface` is empty? (Cost vs. paranoia trade-off.)

5. **`review_depth: deep` authority.** The deep-review opt-in (`bmad-review-adversarial-general` + `bmad-review-edge-case-hunter` instead of `bmad-code-review`) is a story field. Who sets it — sprint-planning (alongside `verification_method`), or the developer at planning time per story? And what heuristic flags a story as high-risk?

6. **Conductor as a skill vs. the top-level session.** The Conductor is specified as a new orchestrator skill. But it must own git mutation, spawn subagents, and hold a long live conversation at the end gate — that is the top-level session's job, and orchestrator-purity rules forbid skills from writing files directly. Confirm: is the Conductor a *skill that sprint-dev's workflow embodies* (i.e. the sprint-dev top-level session *is* the Conductor), or a separately-spawned skill? This affects who legitimately runs `git push`.

7. **Where the `code-fixer` lives.** Proposed as `skills/momentum/agents/code-fixer.md` (a base body) reusing `dev.md`'s commit/output blocks. Should it instead be a *mode* of `momentum:dev` ("fix-mode") to avoid a second body that drifts from dev.md? Two sections phrase it both ways.

8. **E2E ↔ verification-contract overlap.** The verification contract has an `e2e` / `e2e_binding` field *and* E2E is a separate sprint-wide pillar consuming `verification-harness.json`. Confirm the contract's `e2e_binding` is the *only* source the sprint-wide E2E pass reads (single source of truth), vs. the harness JSON being authored independently.

9. **`closed-incomplete` vs `dropped`.** The state machine has both terminal states. Blocked/never-completed stories are routed to `closed-incomplete` (work preserved as a stub). When, if ever, does a story go to `dropped` instead? Is `dropped` reachable from the new flow at all, or only by explicit developer action outside sprint-dev?

10. **Pre-flight HALTs retained — confirm the set.** H1–H5 (no sprint / not activated / missing approvals / stalled) are kept as Phase-1 "cannot start" guards. Confirm these are still desirable as hard HALTs (they are the *only* HALTs left), or whether any should also become autonomous (e.g. auto-activate, auto-reconcile) to match the decision-1 spirit.

---

## 14. Reconciliation note — DEC-035 binding decision #1 × DEC-036

This note maps each spec change in this revision to the source decision it satisfies, mirroring the DEC-036 Reconciliation table structure.

| Spec change | Section(s) revised | DEC-035 binding decision #1 (as written) | DEC-036 decision satisfied |
|---|---|---|---|
| "Zero intermediate gates / one human gate at the end" absolute replaced with "end-gate is the default; narrow mid-flight escalation tier is the sole exception." | §1 (binding decision #1), §8 (Principle) | "Every intermediate approval gate is removed." — relaxed: intermediate gate permitted only when irreversible-and-imminent OR build-invalidating. | D1 — Stakes-and-timing escalation policy adopted. Amendment is intent-preserving: anti-firehose intent preserved, absolutism relaxed. |
| Mid-flight bar stated explicitly and narrowly — a finding may escalate mid-flight ONLY if irreversible-and-imminent OR build-invalidating; no other condition. | §1 (binding decision #1), §8 (mid-flight escalation tier paragraph) | Not addressed in DEC-035. | D1 — The mid-flight bar is the load-bearing definition; must stay narrow. |
| Routine findings stated to be always auto-fixed silently; stakes-class legitimate findings raised (escalated), not silently fixed. | §1 (binding decision #1), §4 (Phase B action text), §8 (Principle) | "Legitimate issues are always fixed automatically — no per-finding fix/defer prompt." — amended: true for routine class only; stakes-class findings are raised as decision cards. | D1 + D2 — Stakes-class findings leave the silent auto-fix path; routine findings remain always auto-fixed. Anti-firehose intent preserved. |
| Finding schema: `legitimate: true` no longer asserts ALWAYS auto-fixed; disposition depends on stakes class + timing tier. | §4 (normalized finding schema inline comment) | "Legitimate issues are always fixed automatically." — relaxed for stakes-class. | D2 — Stakes finding-class added to fixer schema. |
| Three stakes classes documented: security/auth-isolation, irreversible/destructive (migration, delete, force-push, prod deploy), high-blast-radius/architecture; plus default routine class. | §4 (Stakes classes table) | Not enumerated in DEC-035. | D2 — Stakes classes defined as adopted; these are the basis for the escalation routing. |
| Full disposition set documented: `fixed`, `escalated` (new), `dismissed` (non-empty rationale required), `triaged-out`. | §4 (Disposition table) | Disposition set was: fixed, dismissed (with rationale), triaged-out. | D2 — `escalated` disposition is the mechanism by which stakes-class findings are raised rather than silently fixed. |
| Timing-tier marker added to finding schema: `end-gate-expanded` (default) | `mid-flight` (narrow exception). | §4 (finding schema + Timing tiers table) | Not present in DEC-035 schema. | D1 — Timing-tier marker is the implementation of the two-tier routing: end-gate-expanded is the norm; mid-flight fires only on the bar. |
| Non-empty dismissal rationale required — empty or missing rationale is invalid. | §4 (Disposition table, `dismissed` row) | "Dismissed (with rationale)" was in DEC-035 schema but not enforced as a validation gate. | D3 (indirectly) — Legible auto-fix loop requires the rationale to be present for rendering; empty rationale makes the dismissed-rendering section incoherent. |
| §8 documents the narrow mid-flight escalation tier alongside the single human end-gate; restates the narrow bar; makes clear end-gate is default and mid-flight is rare exception. | §8 (Principle, mid-flight paragraph) | "Sprint-dev has exactly one HITL gate." — amended: one primary gate (default) plus a narrow exception. | D1 — The conduct spec must be revised (§8 gate model) to design to the stakes-and-timing exception. |
| Dismissed findings rendered in report (D3 — section 03-D). The auto-fix loop is legible about what it dismissed, not only what it changed. | §9 (Required sections — section 03-D) | DEC-035 D5 mandated surfacing what the fixer changed and dismissed; dismissed rendering was not built (only the "changed" half). | D3 — Builds the unbuilt half of DEC-035 D5; purely additive. |
| Anti-rubber-stamp end-gate forcing function (D4): Approve not pre-checked; stakes-class cards require explicit per-card acknowledgment before Approve enables. | §9 (D4 — Anti-rubber-stamp forcing function) | DEC-035 end-gate had no forcing function; Approve control was pre-checked. | D4 — Forcing function adopted; depends on D1/D2 classification accuracy. |
| Decision-grade presentation caps (upper bounds) + self-sufficiency floor (lower bounds) — tight on irrelevant, complete on decision-relevant. | §9 (D5 — Decision-grade presentation standard) | DEC-035 decision 8 mandated self-sufficiency but had no concision counterweight. | D5 — Adapted with self-sufficiency floor; caps cut irrelevant material, floor preserves decision context inline. |
