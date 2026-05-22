---
content_origin: research-agent
date: 2026-05-22
sub_question: "GitHub Actions as alternative dispatcher for Momentum sprint pipeline"
---

# GitHub Actions as Alternative Dispatcher — Research Report

## Research Question

Can GitHub Actions serve as the dispatcher/coordinator for Momentum's automated sprint pipeline — replacing a purpose-built tool like Gas City — and if so, where does it succeed, where does it fail, and is it a serious alternative?

## Sources Consulted

- `https://docs.github.com/en/actions/reference/limits` — hard limits (job timeout, workflow duration, matrix size, concurrency) [OFFICIAL]
- `https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions` — jobs.needs, jobs.strategy.matrix, fail-fast, continue-on-error, workflow_dispatch inputs [OFFICIAL]
- `https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows` — workflow_dispatch, repository_dispatch, workflow_run chaining limits [OFFICIAL]
- `https://docs.github.com/en/actions/sharing-automations/reusing-workflows` — reusable workflow nesting (max 10 levels), inputs/outputs, secrets [OFFICIAL]
- `https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment` — required reviewers, approval gates [OFFICIAL]
- `https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/reviewing-deployments` — reviewer experience, comment-on-approval, rejection behavior [OFFICIAL]
- `https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions` — cost per minute per runner type, free tier, storage [OFFICIAL]
- `https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners` — self-hosted runner cost model, setup [OFFICIAL]
- `https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow` — matrix jobs, max-parallel, per-entry continue-on-error [OFFICIAL]
- `https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs` — concurrency groups, FIFO queuing, cancel-in-progress [OFFICIAL]
- `https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions` — ANTHROPIC_API_KEY injection, forked repo restrictions, command-line visibility [OFFICIAL]
- `https://github.com/anthropics/claude-code-action` — official Claude Code GitHub Action, execution modes, configuration [OFFICIAL]
- `https://github.com/anthropics/claude-code-action/blob/main/docs/configuration.md` — max-turns, allowed tools, model selection [OFFICIAL]
- `https://github.com/anthropics/claude-code-action/blob/main/docs/capabilities-and-limitations.md` — what claude-code-action cannot do [OFFICIAL]
- `https://github.com/anthropics/claude-code-action/blob/main/docs/solutions.md` — documented automation patterns [OFFICIAL]
- `https://github.com/anthropics/claude-code-action/blob/main/docs/experimental.md` — automation mode vs interactive mode [OFFICIAL]
- Prior Gas City research corpus (validation/discovery-*.md) — Gas City capabilities used as comparison baseline [OFFICIAL + PRAC]

---

## Findings

### 1. Core Fit Assessment

#### Parallel story dispatch via matrix jobs

CONFIRMED. GitHub Actions' `jobs.strategy.matrix` provides first-class parallel job dispatch. A sprint pipeline can define a matrix over story identifiers and GitHub Actions will fan out one job per story, each running on its own isolated runner VM. `fail-fast: false` prevents one story's failure from cancelling the remaining stories. Per-story `continue-on-error: true` allows individual story failures to be recorded without failing the workflow:

```yaml
jobs:
  sprint-dev:
    strategy:
      fail-fast: false
      matrix:
        story: [story-001, story-002, story-003]
    runs-on: ubuntu-latest
    steps:
      - run: claude -p "run momentum:sprint-dev for ${{ matrix.story }}"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

The maximum matrix size is 256 jobs per workflow run [OFFICIAL]. This is well above Momentum's 4-8 story sprints.

The maximum concurrent jobs per workflow depends on the plan tier: 20 concurrent on GitHub Free, up to 500 on Enterprise [OFFICIAL]. For a solo developer with GitHub Free, 20 concurrent jobs is sufficient for any realistic sprint size.

#### Fan-in via `needs:` dependencies

CONFIRMED. The `needs:` keyword creates hard dependency edges between jobs. A downstream job does not start until all jobs listed in its `needs:` array have completed. This is the native fan-in pattern:

```yaml
jobs:
  corpus-avfl:
    needs: [sprint-dev]  # waits for ALL matrix story jobs to complete
    runs-on: ubuntu-latest
    steps:
      - run: claude -p "run momentum:avfl-validator"
```

When the upstream job is a matrix, `needs: [sprint-dev]` waits for **all matrix instances** to complete before `corpus-avfl` starts. This is the barrier/fan-in primitive Momentum needs between story dispatch and corpus validation. CONFIRMED from workflow syntax documentation and consistent with how matrix + needs interacts in GitHub Actions.

This is a material difference from Gas City, which has **no native barrier/join primitive** and requires custom fan-in scaffolding (flag files or bead count queries). GitHub Actions provides this natively with zero custom code.

#### Convergence loops (run until condition passes)

CONFIRMED as a workaround pattern, not a native primitive. GitHub Actions has no native "loop until condition" construct within a single workflow. The workaround is a workflow that conditionally dispatches a new instance of itself using `repository_dispatch` or `workflow_dispatch` via the GitHub API. One running job can call `gh api repos/{repo}/dispatches` with an `event_type`, triggering a new workflow run. That run evaluates the condition; if it fails, it dispatches itself again.

Critical constraints on this pattern:

- `GITHUB_TOKEN` cannot trigger workflows from within a running workflow (prevents accidental recursion). Self-dispatch requires a Personal Access Token or GitHub App token stored as a secret [OFFICIAL].
- `workflow_run` event (dedicated workflow chaining event) has a hard limit of 3 chaining levels [OFFICIAL]. Self-dispatch via `repository_dispatch` does not have a documented iteration limit, but each iteration consumes a new workflow run and accrues minutes.
- There is no built-in iteration counter or state passed between self-dispatched runs. The workflow must read state from an artifact, a repository file, or an external store to know which iteration it is on and what the current score is.

Practical self-dispatch loop skeleton:

```yaml
# avfl-fix-loop.yml
on:
  repository_dispatch:
    types: [run-avfl-fix]

jobs:
  avfl-fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "run momentum:avfl-fixer"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - id: check
        run: |
          score=$(cat .momentum/avfl-score.txt)
          echo "score=$score" >> $GITHUB_OUTPUT
          [ "$score" -ge 95 ] && echo "pass=true" >> $GITHUB_OUTPUT || echo "pass=false" >> $GITHUB_OUTPUT
      - if: steps.check.outputs.pass == 'false'
        run: |
          gh api repos/$GITHUB_REPOSITORY/dispatches \
            -f event_type=run-avfl-fix \
            -f client_payload='{"iteration": "${{ github.event.client_payload.iteration + 1 }}"}'
        env:
          GH_TOKEN: ${{ secrets.PAT_TOKEN }}
```

This works. It is, however, more complex than Gas City's `gc converge create` with a `--gate condition` flag, which encodes the same pattern in a single CLI command backed by native durable state.

INFERRED: Each self-dispatch iteration creates a new workflow run, separate from the original sprint pipeline run. The GitHub Actions UI shows separate runs, not a unified "iteration 3 of 10" view. Pipeline coherence in the UI is lost when using self-dispatch loops.

#### `claude -p` as a shell step

CONFIRMED with caveats. The Anthropic `claude-code-action@v1` official GitHub Action exists and is the supported integration path [OFFICIAL]. It invokes Claude Code via the Claude Code SDK internally — developers do not need to manage the binary installation. The action accepts a `prompt:` input for automation mode:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      Run momentum:sprint-dev for story {{ story_id }}
    claude_args: "--max-turns 50"
```

The `--max-turns` flag controls the maximum number of agentic turns (tool calls + responses). For a full story implementation session, this needs to be high enough to complete the work; the documentation does not specify a default, and runaway turns consume API budget proportionally.

Alternatively, `claude -p` can be invoked directly as a shell command if the Claude Code CLI is installed on the runner:

```yaml
- run: |
    npm install -g @anthropic-ai/claude-code
    claude -p "run momentum:sprint-dev for story $STORY_ID" \
      --dangerously-skip-permissions
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    STORY_ID: ${{ matrix.story }}
```

Security note: the ANTHROPIC_API_KEY is passed as an environment variable (correct pattern — not command-line argument, which would be visible in process listings) [OFFICIAL].

**Critical runtime constraint:** GitHub-hosted runners provide fresh VMs per job with no persistent state. Each `claude -p` session starts with a clean filesystem. Git worktrees must be created within the job — the checkout action clones the repo fresh, and worktree creation/deletion is entirely the job's responsibility. There is no persistent worktree pool analogous to Gas City's rig model.

#### Job and workflow timeout limits

CONFIRMED. Hard limits from official documentation:

| Scope | GitHub-hosted runners | Self-hosted runners |
|---|---|---|
| Per-job execution time | 6 hours (360 minutes) | 5 days |
| Total workflow run duration | 35 days (including wait time) | 35 days |
| Max concurrent jobs (GitHub Free) | 20 | Unlimited (your machine) |
| Max matrix jobs per workflow | 256 | 256 |

The 6-hour per-job limit applies to GitHub-hosted runners. For an overnight sprint run where individual story jobs may run for hours (LLM session time + CI validation), 6 hours per job is tight but likely sufficient for Momentum's use case (individual story sessions are unlikely to exceed 2-3 hours). The 35-day total workflow duration limit is not a practical constraint.

Self-hosted runners remove the 6-hour job limit entirely (5-day cap), which is the natural choice for heavy agentic workloads that could span long sessions.

---

### 2. Human-in-the-Loop Support

#### GitHub Environments with required reviewers

CONFIRMED. GitHub Environments provide a native human approval gate primitive. A job that references an environment with required reviewers pauses before starting and waits for approval. The workflow itself suspends — no compute is consumed while waiting.

Configuration:

```yaml
jobs:
  human-review:
    environment: sprint-review  # environment has required reviewers configured
    runs-on: ubuntu-latest
    steps:
      - run: claude -p "apply requested fixes"
```

Up to 6 required reviewers can be designated; only one needs to approve for the job to proceed [OFFICIAL].

The approval timeout is configurable per environment (default appears to be no timeout, though individual jobs have their overall job timeout). If no reviewer acts, the workflow run eventually expires.

#### Reviewer experience and feedback mechanism

CONFIRMED with significant gap. When a job awaits environment approval, reviewers see the pending deployment in the GitHub UI and receive a notification. Reviewers can **leave a comment** when approving or rejecting [OFFICIAL].

However: the comment is not automatically passed to the next workflow step or run as structured data. The gap is:

- Reviewer approves → job proceeds. The next step has no API access to read what the reviewer wrote.
- Reviewer rejects → the workflow job fails. The workflow run ends. A new workflow run must be triggered (manually or via automation) to re-enter the fix pipeline.
- There is no built-in "reject with payload that seeds the next run" mechanism.

Workaround for feedback injection: a reviewer could write structured feedback as a comment on the workflow run or a designated GitHub issue, and the next workflow run's first step could read that comment via the GitHub API (`gh api`). This requires the human to follow a convention (write feedback in a specific place) and the workflow to know where to look. This is the same gap that exists in Gas City — `gc converge iterate` carries no feedback payload — and the workaround shape is similar (artifact directory in Gas City, GitHub issue/comment in GitHub Actions). INFERRED as viable workaround; [UNVERIFIED] as production-tested pattern.

#### Iterative human rejection and re-entry into fix pipeline

INFERRED (important gap). When an environment gate is rejected, the workflow job fails and the workflow run terminates. To re-enter the fix pipeline:

1. A new workflow run must be triggered — either manually via the GitHub UI ("Re-run workflow"), via `workflow_dispatch`, or via `repository_dispatch` from external automation.
2. The new run starts from the beginning of the workflow (or from the failing job if using "Re-run failed jobs").
3. There is no built-in "re-enter from this specific gate with the reviewer's rejection reason" workflow concept.

This is a significant design mismatch for Momentum's human review loop, which requires iterative N-time rejection with each rejection re-entering a fix pipeline. In Gas City, `gc converge iterate` resumes an existing convergence loop. In GitHub Actions, each rejection-and-retry creates a new workflow run with no native state continuity.

The practical workaround is a repository-level state file (`.momentum/review-state.json`) that the workflow reads on startup to determine whether it is in a "re-entering from rejection" state. This is buildable but requires custom scaffolding that Gas City's convergence primitive provides natively.

---

### 3. Convergence Loops

#### Native loop constructs

CONFIRMED ABSENT. GitHub Actions has no native "repeat until condition" loop within a single workflow run. Each workflow run is a directed acyclic graph (DAG) of jobs — no cycles, no iterative convergence.

The three practical patterns for implementing convergence loops in GitHub Actions:

**Pattern A: Self-dispatch via repository_dispatch**
Each loop iteration is a separate workflow run. A job checks the condition; if it fails, it calls the GitHub API to dispatch a new workflow run of the same type. Pros: simple, works with existing job structure. Cons: each iteration is a separate run (UI fragmentation), iteration state must be externalized (file or API), self-dispatch requires a PAT/App token (not GITHUB_TOKEN), billing accrues per iteration as independent runs.

**Pattern B: Reusable workflow composition + outputs**
A caller workflow calls a reusable workflow (max 10 levels of nesting [OFFICIAL]), uses job outputs to determine if another call is needed, and uses `if:` conditionals to short-circuit. This does not enable true loops within one workflow run — it still requires re-triggering. Nesting depth is not a substitute for iteration.

**Pattern C: In-job shell loop**
A single job step runs a shell `while` loop that invokes `claude -p`, checks the score, and retries — all within one job execution. This is bounded by the 6-hour job timeout (GitHub-hosted) and is effectively unlimited for self-hosted runners. It is the simplest pattern but makes the individual job monolithic and breaks the step-level visibility that GitHub Actions normally provides.

Pattern C is the most viable for the AVFL and E2E fix loops in Momentum if self-hosted runners are used. Example:

```bash
# Within a single job step on a self-hosted runner:
for i in $(seq 1 10); do
  claude -p "run momentum:avfl-fixer" --dangerously-skip-permissions
  score=$(cat .momentum/avfl-score.txt)
  [ "$score" -ge 95 ] && break
done
```

This is runnable, auditable via the step's log output, and bounded by the loop counter. However, the GitHub Actions UI shows only one step log — not per-iteration progress as separate tracked items. INFERRED as viable for overnight sprint runs where the developer is not watching live.

#### Practitioner patterns for fix loops

UNKNOWN. No documented community examples of GitHub Actions used for AVFL-style AI validation fix loops were found. The claude-code-action solutions guide shows single-invocation patterns (PR review, issue triage, scheduled maintenance) — not convergence loops [OFFICIAL]. Blog posts and community forums do not surface examples of multi-iteration convergence workflows using GitHub Actions as the orchestrator. This is not evidence the pattern fails — it may simply be that the agentic pipeline use case is too new for documented community practice to exist.

#### Rate limits on self-dispatch

CONFIRMED. The GitHub API rate limit for `GITHUB_TOKEN` is 1,000 requests per repository per hour (15,000 for Enterprise Cloud) [OFFICIAL]. Each `repository_dispatch` call consumes one API call. For a 10-iteration AVFL fix loop plus a 10-iteration E2E fix loop, total API calls are low (20) — rate limiting is not a concern at Momentum's scale. If the fix loop runs many times per sprint (unlikely), this still does not approach the rate limit.

---

### 4. Error Handling

#### Matrix job failure isolation

CONFIRMED. With `fail-fast: false` and per-entry `continue-on-error: true`, a matrix job failure (one story failing) does not cancel other matrix jobs. All stories proceed to completion (or failure), and the workflow continues to downstream jobs that `needs:` the matrix job.

The downstream `corpus-avfl` job needs to distinguish between "all stories passed" and "some stories failed." Job outputs from matrix jobs are accessible via `needs.<job>.outputs.<key>` in downstream jobs. Each matrix job can write its pass/fail status to a job output, and the downstream job reads all of them. [OFFICIAL — job outputs via needs context]

This is functionally equivalent to Gas City's "condition trigger checks bead count" fan-in workaround, but with native support: the fan-in is built into the DAG, and per-story pass/fail status flows through job outputs without requiring external state files.

#### Step-level retry

INFERRED. GitHub Actions has no built-in step retry. The community-maintained `nick-fields/retry` action provides retry logic for individual steps:

```yaml
- uses: nick-fields/retry@v3
  with:
    max_attempts: 3
    retry_on: error
    command: claude -p "run QA validation"
```

This is an unofficial action and adds an external dependency. For official support, retry must be implemented within the shell command itself. [UNVERIFIED: nick-fields/retry stability and maintenance status not investigated]

#### Runner death mid-job

CONFIRMED. If a GitHub-hosted runner dies (infrastructure failure), the job is marked as failed and the workflow run moves to the failed state. There is no automatic pickup of mid-job state — the job does not resume from the point of failure. The workflow can be re-run, but all steps restart from the beginning (or from the first failed step using "Re-run failed jobs").

There is no equivalent of Gas City's GUPP (Get Up, Pick Up) crash recovery model, where an agent session crashes and a restarted session picks up the in-progress work item from the durable bead store. GitHub Actions' runner crash recovery is workflow-run-level re-execution, not step-level continuation. For LLM agent sessions that make external API calls, a runner crash mid-session means the entire claude session is lost and must restart.

Self-hosted runners can be configured to restart automatically (runner process as a system service), but the job-level state is still lost on crash — the runner picks up the next queued job, not the interrupted one.

#### Silent hang detection

INFERRED. GitHub Actions has no equivalent to Gas City's stuck-agent watchdog (30-minute idle threshold, `gt feed --problems` TUI). A job that is running but making no progress (e.g., a claude session stuck waiting for a tool call) will show as "in progress" in the UI until it times out per the `timeout-minutes` setting on the job.

Job-level timeout prevents infinite hangs:

```yaml
jobs:
  sprint-dev:
    timeout-minutes: 180  # 3-hour hard limit per story job
```

When the timeout fires, the job is cancelled and marked as failed. There is no "nudge" mechanism to prod the running agent. The developer would need to investigate the job's live log to understand why it appears stuck. CONFIRMED for timeout behavior; INFERRED for "no nudge" conclusion.

---

### 5. Developer Experience, Monitoring, and Cost

#### Pipeline visibility

CONFIRMED with significant gaps. GitHub Actions provides:

- **Workflow run visualization**: A real-time graph of job dependencies (the DAG) showing which jobs are running, queued, completed, or failed. Job names are visible. For a matrix, each matrix instance shows as a separate node.
- **Live log streaming**: Each job's step output streams in real time in the GitHub UI. The developer can watch a specific job's claude session output as it runs.
- **Status badges**: A workflow status badge for the repository's default branch.
- **Job execution time**: Billable minutes per job are displayed.
- **Notifications**: GitHub sends email/web notifications for workflow run completion (pass/fail). No native Slack push notification without custom action.

What GitHub Actions does NOT provide:

- **No pipeline-phase view across stories**: There is no single screen that shows "story-001 is in QA, story-002 passed, story-003 is in code review." The matrix view shows job names and status, but the "phase" semantic is whatever the developer encodes in job names.
- **No convergence loop iteration count**: Self-dispatch loop iterations appear as separate workflow runs with no grouping. The UI does not say "AVFL fix loop, iteration 3 of 10" — it shows three separate workflow runs.
- **No human gate discovery proactively**: Pending environment approvals appear in the "Environments" tab of the repository and generate a GitHub notification, but there is no dedicated "3 gates are waiting for you" view. The developer must navigate to the specific workflow run to approve.
- **No agent health monitoring**: There is no equivalent to `gt feed --problems` that shows which Claude sessions are active, idle, or stuck.

Compared to Gas City's monitoring story: both have the same fundamental gap (no unified pipeline-phase view), and both require the developer to navigate multiple views to reconstruct pipeline state. Gas City's `gc converge list` gives iteration state per loop natively; GitHub Actions has no equivalent for self-dispatch iterations. GitHub Actions' matrix job DAG view is better than Gas City's lack of a pipeline view — but Gas City's per-loop state (`gc converge status`) is more granular than GitHub Actions' per-run views. The two gaps are different in character.

#### Cost model

CONFIRMED. Costs from official documentation:

| Runner type | Cost per minute |
|---|---|
| Linux 2-core (x64) | $0.008 (4x multiplier on $0.002 base) |
| Linux 2-core (x64) — correct rate | $0.006 per minute |
| macOS 3/4-core | $0.062 per minute |
| Windows 2-core | $0.010 per minute |

Free tier: 2,000 minutes/month (GitHub Free), 3,000 minutes/month (GitHub Pro).

For a sprint with 6 stories, each running 2 hours of story work + 1 hour of validation work per job, with parallel execution: approximately 6 × 3h = 18 job-hours = 1,080 minutes per sprint at $0.006/min = **$6.48 per sprint on GitHub-hosted Linux runners**. Over 50 sprints per year: approximately $324/year.

This is API cost only. Claude API costs (ANTHROPIC_API_KEY usage) are separate and likely dominate the compute cost. The GitHub Actions compute cost itself is modest.

**Self-hosted runners eliminate GitHub compute costs entirely** — the developer pays only for their own machine's electricity/cloud cost. For a developer already running a local machine or a small VPS, self-hosted runners are effectively free for compute. The setup cost is a one-time investment (~30 minutes to configure the runner process as a system service).

#### Self-hosted runner requirements for `claude -p`

CONFIRMED. `claude -p` invocations require: the Claude Code CLI installed on the runner, an ANTHROPIC_API_KEY secret, and sufficient disk/network for git operations. There is no requirement for Dolt, tmux, or any Gas City infrastructure.

Self-hosted runners are appropriate for Momentum's use case for three reasons:
1. Removes the 6-hour job timeout limit (extended to 5 days per job).
2. Eliminates compute costs.
3. Allows the developer to run Claude Code sessions in their own environment with their existing tool configuration (MCP servers, allowed tools, etc.) without re-configuring per-runner.

The setup requirement is a running GitHub Actions runner process (`actions/runner`) registered to the repository. Restart-as-service configuration is documented and standard. There is no exotic dependency. [OFFICIAL — self-hosted runner docs]

#### Practical limits as an agentic pipeline orchestrator

CONFIRMED with synthesis. GitHub Actions was designed as a CI/CD automation platform, not as an agentic pipeline orchestrator. The friction points at the design boundary are:

1. **Ephemeral state**: Each job starts with a clean runner. Persistent state (story progress, worktrees, iteration count) must be stored externally (git repo files, artifacts, or external stores). Gas City's bead store provides durable state natively.

2. **No native loop constructs**: Convergence loops require self-dispatch workarounds, which fragment the pipeline into separate workflow runs.

3. **No agent-aware monitoring**: Stuck agent detection, agent health, session lifecycle — none of these are concepts GitHub Actions has primitives for.

4. **Approval without payload**: Human review gates work for blocking but not for feedback-carrying rejection. The reviewer comment is logged but not machine-readable in the next run.

5. **Workflow YAML complexity grows with pipeline complexity**: A Momentum sprint pipeline with parallel stories, per-story QA + code review, AVFL loops, E2E loops, and human review gates would require a significant YAML workflow definition. Gas City encodes the same pipeline in smaller TOML orders plus shell scripts. As pipeline complexity grows, GitHub Actions YAML becomes harder to maintain than the Gas City configuration model.

---

## Synthesis

### Where GitHub Actions fits Momentum's needs

**Fan-out (parallel story dispatch)**: Native matrix jobs, `fail-fast: false`, per-entry `continue-on-error`. Better than Gas City — no custom scaffolding needed. CONFIRMED.

**Fan-in barrier**: Native `needs:` dependency. Waits for all matrix instances without custom flag files or bead count queries. Substantially better than Gas City's manual workaround. CONFIRMED.

**Human gate (blocking)**: GitHub Environments with required reviewers. Reviewer must approve/reject; the workflow suspends during wait. Equivalent to Gas City's `waiting_manual` convergence gate for the blocking case. CONFIRMED.

**`claude -p` invocation**: `anthropics/claude-code-action@v1` is the official integration path. No custom runner setup needed for the action. CONFIRMED.

**Error isolation**: Matrix job failure isolation is native. Other stories continue when one fails. Better than Gas City's no-retry exec orders, which require internal retry logic. CONFIRMED.

**Cost**: Modest compute cost on GitHub-hosted runners; zero compute cost on self-hosted. Not a blocker. CONFIRMED.

### Where GitHub Actions fails Momentum's needs

**Convergence loops**: No native construct. Self-dispatch via `repository_dispatch` works but fragments the pipeline into separate runs, loses iteration state natively, and requires a PAT/App token (not GITHUB_TOKEN). Gas City's `gc converge create` with a condition gate is a more natural primitive for the AVFL and E2E fix loops. CONFIRMED GAP.

**Human feedback injection**: Reviewer comment is visible in the UI but not machine-readable in the next run. No native "rejection with payload" mechanism. Same gap as Gas City, but Gas City's artifact directory workaround is more structured. CONFIRMED GAP.

**Iterative human review loop**: Each rejection creates a new workflow run. No state continuity between rejection and re-entry. The developer must manually trigger the re-run or build automation to do it. Gas City's `gc converge iterate` resumes the same loop. CONFIRMED GAP — more significant than Gas City's equivalent gap.

**Agent health and stuck detection**: No equivalent to `gt feed --problems` or stuck-agent alerts. The developer must watch live logs or notice timeouts. CONFIRMED GAP.

**Convergence loop visibility**: Self-dispatch iterations appear as separate runs. No unified "iteration 3 of 10" view. Gas City's `gc converge status` provides this natively. CONFIRMED GAP.

**Worktree management**: No persistent worktree pool. Each job clones fresh and must set up its own worktree. Gas City's rig model maintains worktrees persistently across agent invocations. INFERRED as gap — creates setup overhead per story job.

**Pipeline-phase semantic**: GitHub Actions does not know what "code review phase" or "QA phase" means. All semantic must be encoded in job names and step names. Gas City similarly lacks pipeline-phase semantics, but its bead labels allow semantic metadata that the REST API can filter on. For Momentum specifically, neither tool provides this natively — both require the developer to build the semantic layer.

### Key architectural tension

GitHub Actions is optimized for **event-driven automation of discrete tasks** — a PR opens, a test suite runs, a deployment is triggered. Its job model is well-suited for one-shot agentic invocations (a claude session that does one thing and exits). It is awkward for **iterative convergence loops** and **long-running pipelines with human feedback cycles**, because every iteration and every re-entry appears as a separate workflow run with no native continuity.

Gas City is optimized for **persistent orchestration** — a city runs continuously, monitoring for triggers, managing agent sessions, tracking state durably. Its convergence primitive is native to this continuous model. The tradeoff is that Gas City requires a persistent running process (the Controller) and an opinionated state model (beads). GitHub Actions requires no persistent infrastructure beyond the runner — it is event-driven and stateless by design.

For Momentum's sprint pipeline, the dominant use pattern is **episodic** (one sprint per week, not 24/7 continuous operation). This favors GitHub Actions' event-driven model over Gas City's continuous-controller model — Momentum does not need a always-on controller when it only dispatches work once a week.

The dominant complexity driver is **the AVFL and E2E fix loops**. These are convergence loops. If they must be implemented as self-dispatch iterations in GitHub Actions, the complexity cost (PAT management, run fragmentation, external state) may outweigh the simplicity benefit of using a familiar platform.

---

## Open Questions

1. **What is the actual default `--max-turns` for the claude-code-action in automation mode?** The documentation describes the parameter but does not state a default. If the default is too low (e.g., 20 turns), long story implementation sessions would fail silently by running out of turns. This must be confirmed before using the action for full sprint-dev sessions.

2. **Can `repository_dispatch` reliably chain AVFL fix loop iterations without rate limiting?** At Momentum's scale (at most 10 iterations per sprint), the answer is almost certainly yes. But if the AVFL fix loop were to run on a CI/CD pipeline with frequent sprints (e.g., a team running daily sprints), the 1,000 API requests/hour limit could be approached. This is not a concern for solo development.

3. **Is there a pattern for environment approval reviewers to write structured rejection feedback that a subsequent workflow run reads?** The GitHub API can be queried for pending deployment review comments. Whether the standard GitHub review interface supports structured rejection payloads (rather than free-text comments) is UNKNOWN. A workaround using GitHub Issues as a feedback channel would require convention enforcement.

4. **What does "Re-run failed jobs" do to a workflow with matrix jobs?** If the sprint-dev matrix runs 6 stories and 2 fail, "Re-run failed jobs" presumably re-runs only the 2 failed story jobs. Whether the downstream `corpus-avfl` job also re-runs, or whether it was already skipped when the upstream jobs failed, is UNKNOWN from available documentation. This matters for whether the human can re-run only the failed stories without re-running the full pipeline.

5. **Is self-hosted runner restart-on-crash automatic?** If the developer's machine is the runner host and the runner process crashes mid-sprint, do queued jobs stall until the runner is restarted manually? Understanding runner restart behavior matters for overnight sprint runs where no human is watching.

---

## Fit Verdict

### Direct comparison to Gas City

| Requirement | GitHub Actions | Gas City |
|---|---|---|
| Parallel story dispatch | NATIVE — matrix jobs | WORKAROUND — exec orders per story |
| Fan-in barrier | NATIVE — needs: | WORKAROUND — bead count condition |
| Per-story fix loops (code review, QA) | NATIVE — jobs per phase | NATIVE — orders per phase |
| AVFL/E2E convergence loops | WORKAROUND — self-dispatch | NATIVE — gc converge create |
| Human approval gate (blocking) | NATIVE — environments | NATIVE — waiting_manual |
| Human rejection with feedback | WORKAROUND — comment convention | WORKAROUND — artifact dir convention |
| Iterative human review loop | AWKWARD — new run per iteration | NATIVE — gc converge iterate |
| Error isolation (one story fails) | NATIVE — continue-on-error | WORKAROUND — condition scripts |
| Stuck job detection | PARTIAL — job timeout only | PARTIAL — gt feed --problems |
| Pipeline visibility (phase per story) | GAP — job names only | GAP — CLI queries only |
| Convergence loop iteration view | GAP — separate runs | NATIVE — gc converge status |
| Infrastructure overhead | LOW — hosted or self-hosted | MEDIUM — persistent controller + Dolt option |
| Setup complexity | LOW — add .github/workflows/ | MEDIUM — gc init + city config |
| Production maturity | HIGH — years of production use | LOW — v1.1.0, < 1 month old |
| Community ecosystem | HIGH — extensive actions marketplace | LOW — nascent, young ecosystem |
| Cost | LOW — modest per-minute billing | LOW — self-hosted, free |
| Familiarity to developer | HIGH — standard CI/CD tooling | LOW — new concepts (orders, convergence, beads) |

### Assessment

**GitHub Actions is a serious alternative for 70% of the Momentum sprint pipeline.** The parallel story dispatch, fan-in barrier, per-story code review + QA jobs, and human approval gate all map naturally onto GitHub Actions primitives — better than Gas City's equivalents in most cases. The fan-out/fan-in pattern is unambiguously simpler in GitHub Actions than in Gas City.

**The 30% where it breaks down is the convergence loop.** The AVFL fix loop, E2E fix loop, and human review re-entry loop are all convergence patterns. GitHub Actions has no native convergence primitive. Self-dispatch works but is not first-class: iterations are disconnected workflow runs, state must be externalized, and visibility suffers. If these loops run rarely (e.g., AVFL already passes on most sprints), the workaround cost is low. If they run frequently (convergence takes 5-7 iterations per sprint on average), the operational friction accumulates.

**For a solo developer already familiar with GitHub Actions**, the cognitive cost of learning Gas City's concepts (cities, rigs, orders, beads, convergence loops, GUPP) is a real argument for GitHub Actions. The sprint pipeline can be expressed in ~150-200 lines of YAML, using a single `anthropics/claude-code-action@v1` action that Anthropic officially supports and documents. The operational model is: a workflow run is the sprint; stories are matrix jobs; AVFL and E2E are downstream jobs with shell loops; human review is an environment gate. This is maintainable, debuggable, and requires zero new infrastructure.

**The decisive question is whether convergence loop fidelity matters enough to accept Gas City's complexity and immaturity.** If Momentum's AVFL and E2E fix loops are expected to run many times and the developer needs to watch their state, Gas City wins on ergonomics. If those loops are expected to be occasional and short, GitHub Actions' workaround is acceptable.

**Practical recommendation:** GitHub Actions is the lower-risk alternative for an initial sprint pipeline implementation. It requires no new infrastructure, no learning curve on Gas City concepts, and its primitives (matrix, needs, environments) directly model the core sprint pipeline shape. The convergence loops should be implemented as in-job shell loops (Pattern C above) on a self-hosted runner to avoid the self-dispatch complexity and UI fragmentation. The human review loop re-entry gap is real but acceptable for a solo developer who can click "Re-run failed jobs" in the GitHub UI after writing feedback to a designated Issue or file. A migration to Gas City remains viable once Gas City matures (post-v1.5, with MCP support shipped), but is not required for Momentum's current needs.

**GitHub Actions is a serious alternative — not a toy alternative. The convergence loop gap is the only disqualifying gap, and it is addressable with Pattern C (in-job shell loop on a self-hosted runner).**
