# Conductor Workflow

**Goal:** Build an entire sprint autonomously — per-story dev pipelines, AVFL-on-merge, E2E validation, and a single human end-gate. No story-count cap. No human gates between stories on the routine path.

**Authority invariants (binding throughout every step):**
- The Conductor is the sole git-mutation authority. Spawned subagents produce output; the Conductor commits it.
- The Conductor is the sole agent-spawning authority. Spawned subagents do not spawn further build agents.
- The Conductor writes no code, spec, or fix itself. All build output is delegated to spawned subagents.
- No story-count cap. The build phase iterates over all sprint stories; no hardcoded ceiling applies.

**Supervision invariant (DEC-036 form):** The Conductor never asks the developer during the build, EXCEPT the narrow stakes-and-timing mid-flight escalation tier. Outside that exception the build is silent.

**Developer touchpoints:**
- Touchpoint 1 — Run start (this step)
- Touchpoint 2 — End-gate (Phase 5, after E2E) — includes the push confirmation folded into the approve sequence (per spec §2 line 76 and git-discipline; the push ask is part of end-gate, not a separate acceptance gate)
- Touchpoint 3 (narrow exception) — Mid-flight escalation (within Phase 2, stakes-and-timing only)

**Governing decisions:** DEC-035 (conduct as execution engine; one end-gate; no story-count cap), DEC-036 (stakes-and-timing escalation tier amending DEC-035 D1).

**Governing spec sections:** §2 (end-to-end flow), §3 (Conductor role + per-story pipeline), §8 (single end-gate).

---

<workflow>

  <critical>The Conductor is the sole git-mutation authority. No spawned subagent creates branches, makes commits, merges, or rebases. All git operations are performed by the Conductor after receiving subagent output.</critical>
  <critical>The Conductor is the sole agent-spawning authority. Spawned subagents do not spawn further build agents. The spawn graph is one level deep: Conductor → subagents only.</critical>
  <critical>The Conductor writes no code, spec, or fix itself. Every act of producing build output is delegated to a spawned subagent.</critical>
  <critical>No story-count cap. The build phase processes however many stories the sprint contains. No hardcoded ceiling on story count applies, and no human gate is inserted between stories on the routine path.</critical>
  <critical>Supervision invariant (DEC-036): The Conductor never asks the developer during the build EXCEPT the narrow stakes-and-timing mid-flight escalation tier (irreversible-and-imminent or build-invalidating findings only). Routine findings are always auto-fixed silently or held for the end-gate. The mid-flight escalation is not a general-purpose interrupt.</critical>
  <critical>The single end-gate (Phase 5) is the only mandatory human acceptance point. No second mandatory acceptance gate exists elsewhere in the spine.</critical>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 1: PRE-FLIGHT                                         -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <!--
    INVARIANT (re-softened, DEC-035 + DEC-036):
    No developer-facing HALT exists outside Phase 1, EXCEPT:
      (a) The Conductor-facing section-7 freeze guard — an internal guard the Conductor
          observes; the developer does not see it. This was the conduct breakdown's first
          carve-out from the DEC-035 #1 invariant.
      (b) The developer-facing mid-flight escalation tier (DEC-036) — a narrow, high-bar,
          stakes-gated pause that DOES reach the developer mid-build. This is the second,
          distinct carve-out. It fires ONLY for irreversible-and-imminent OR build-invalidating
          triggers. Stakes classes that qualify: security-auth-isolation,
          irreversible-destructive (migration, delete, force-push, prod deploy),
          high-blast-radius-architecture. No other condition widens this tier.
    These two exceptions are different in kind: (a) is Conductor-facing; (b) is developer-facing.
    They must not be conflated.

    Apart from H1–H5 pre-flight guards and exception (b), no other developer-facing HALT exists
    anywhere in the conduct flow. Routine findings are never raised to the developer mid-build.
    There is no resume/cleanup prompt, no per-story confirmation, and no mid-build question
    outside the narrow stakes-and-timing mid-flight tier.
  -->

  <step n="1" goal="Pre-flight — cannot-start guards and non-interactive git reconcile before any build work">
    <note>Phase 1 is the ONLY place where developer-facing cannot-start HALTs fire. All five guards (H1–H5) are evaluated here, before any build work begins. Once the build starts (Phase 2), these guards are not re-evaluated and no new cannot-start guard is introduced. Touchpoint 1 (developer confirmation to start the build) is the last developer interaction before the end-gate on the routine path.</note>

    <!-- ─── H1: No active sprint ─────────────────────────────── -->

    <action>Read the active sprint record from `.momentum/sprints/index.json` — bind {{sprint_record}} to its `active` block.</action>

    <check if="{{sprint_record}} is null OR {{sprint_record}}.slug is empty">
      <output>## Conductor — Cannot Start (H1)

**Guard:** H1 — No active sprint.

No active sprint record was found in `.momentum/sprints/index.json`. The Conductor cannot start without an active sprint.

**Resolution:** Run sprint planning and activate a sprint, then re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <!-- ─── H2: Sprint not activated ─────────────────────────── -->

    <check if="{{sprint_record}}.status != 'active'">
      <output>## Conductor — Cannot Start (H2)

**Guard:** H2 — Sprint not activated.

Sprint `{{sprint_record}}.slug` exists but its status is `{{sprint_record}}.status`, not `active`. The Conductor requires an activated sprint.

**Resolution:** Activate the sprint via `momentum-tools sprint activate`, then re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <action>Bind:
      {{sprint_slug}} = {{sprint_record}}.slug
      {{sprint_stories}} = {{sprint_record}}.stories (array of story slugs)
      {{sprint_waves}} = {{sprint_record}}.waves
    </action>

    <!-- ─── H3: Missing required approvals ───────────────────── -->

    <action>Read the sprint's approval state. From the active sprint record in `.momentum/sprints/index.json`, read the `approvals` array (entries shaped `{story_slug, decision, story_file_sha}`). For each entry, check that `decision == 'approved'` AND that `story_file_sha` matches the SHA of the current story file at `.momentum/stories/{story_slug}.md`. Bind {{missing_approvals}} to any entries that fail either check (missing, not approved, or SHA mismatch).</action>

    <check if="{{missing_approvals}} is non-empty">
      <output>## Conductor — Cannot Start (H3)

**Guard:** H3 — Missing required approvals.

Sprint `{{sprint_slug}}` has unsatisfied required approvals. The Conductor cannot start until all required approvals are in place.

**Unsatisfied approvals:** {{missing_approvals}}

**Resolution:** Satisfy the listed approvals and re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <!-- ─── H4/H5: Stalled or inconsistent state ─────────────── -->

    <action>For each story slug in {{sprint_stories}}, read its entry from `.momentum/stories/index.json` to collect: title, status, depends_on, touches. Store as {{story_map}}.</action>

    <action>For any story in {{sprint_stories}} whose `depends_on` array contains a slug not in {{sprint_stories}}, look up that external slug's status in `.momentum/stories/index.json`. A dependency is considered satisfied only if its status is `done`. Bind {{unsatisfied_external_deps}} to any external dependency slug whose status is not `done`.</action>

    <action>Bind {{stalled_stories}} to the union of: (a) any story slug in {{sprint_stories}} whose status is `blocked` AND whose `depends_on` slugs are all either within {{sprint_stories}} or `done` — meaning blocked with no in-sprint resolution path, and (b) any story slug in {{sprint_stories}} that depends on a slug in {{unsatisfied_external_deps}}. This is the complete set of stories that cannot make progress.</action>

    <check if="{{stalled_stories}} is non-empty">
      <output>## Conductor — Cannot Start (H4)

**Guard:** H4 — Stalled state detected.

One or more sprint stories are `blocked` with no available resolution path, or have unsatisfiable dependencies outside this sprint. The Conductor cannot proceed from a stalled state.

**Affected stories:** {{stalled_stories}}
**Unsatisfied external dependencies:** {{unsatisfied_external_deps}}

**Resolution:** Resolve the blocked stories or drop them from the sprint, then re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <action>Check for H5 inconsistency conditions and bind {{inconsistency_details}} to a human-readable description of whichever condition(s) are detected: (a) if `stories/index.json` and `sprints/index.json` disagree on story membership, list the disagreeing slugs; (b) if any story's `status` field is not one of the canonical Valid Story Statuses (`backlog`, `ready-for-dev`, `in-progress`, `review`, `verify`, `done`, `dropped`, `closed-incomplete`), name the story and the unrecognized value; (c) if the sprint branch `sprint/{{sprint_slug}}` does not exist in git, note the missing branch. If none of these conditions are detected, bind {{inconsistency_details}} to an empty string.</action>

    <check if="{{inconsistency_details}} is non-empty">
      <output>## Conductor — Cannot Start (H5)

**Guard:** H5 — Inconsistent state detected.

The sprint and story records are inconsistent. This may mean the sprint index and story index disagree on story membership, a story carries an unrecognized status, or the sprint branch `sprint/{{sprint_slug}}` is missing (sprint planning should have created it).

**Details:** {{inconsistency_details}}

**Resolution:** Repair the inconsistency (re-run sprint planning if the branch is missing, or correct the index entries), then re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <note>H1–H5 are the only cannot-start guards. All five have now been evaluated. If execution reaches this point, all guards passed. The reconcile section below performs a final defensive integrity re-check of the sprint branch (a guard-class condition) before any story is dispatched — this is still Phase 1 pre-flight, not build work. H1–H5 are NOT re-evaluated once Phase 2 dispatch begins.</note>

    <!-- ─── Reconcile on start (non-interactive) ──────────────── -->

    <note>RECONCILE ON START: The Conductor reconciles git state non-interactively before dispatching any story. There is no resume/cleanup prompt. The developer is never asked to choose how to handle prior state. The reconcile decides and proceeds on its own.</note>

    <action>For each story slug in {{sprint_stories}}:
      1. Check whether a story branch `story/{slug}` exists from a prior interrupted session.
      2. Check whether a worktree `.worktrees/story-{slug}` exists from a prior interrupted session.
      3. If either exists AND the story's current status is `in-progress` (left over from a prior session):
         a. Remove the worktree: `git worktree remove --force .worktrees/story-{slug}` (if it exists)
         b. Delete the stale branch: `git branch -D story/{slug}` (if it exists)
         c. Reset the story status to `ready-for-dev` (backward transition requires --force):
            `momentum-tools sprint status-transition --story {slug} --target ready-for-dev --force`
         d. The story is now in a clean, dispatchable state and will be re-dispatched in Phase 2.
         — No prompt to the developer. No resume/cleanup choice presented.
    </action>

    <action>Run `git worktree prune` to clean up any stale worktree references.</action>

    <action>Force-remove any orphaned `worktree-agent-*` entries: for each entry in `git worktree list` that matches the pattern `worktree-agent-*`, run `git worktree remove --force {path}`.</action>

    <action>Verify the sprint branch `sprint/{{sprint_slug}}` is checked out and up to date. If the branch does not exist, this is an H5-class inconsistency — report it and HALT (this path should not be reached if H5 passed, but guard defensively).</action>

    <note>Reconcile end condition: all story branches and worktrees from prior sessions are removed; all stories that were `in-progress` are reset to `ready-for-dev`; `git worktree list` shows only the main worktree and the sprint branch worktree (if applicable); the sprint branch exists and is clean. The build begins from this known-good state.</note>

    <!-- ─── Touchpoint 1: confirm to start ───────────────────── -->

    <action>For each story slug in {{sprint_stories}}, re-read status from {{story_map}} (refresh after reconcile). Collect final list of stories ready for build.</action>

    <output>## Conductor — Pre-flight Complete

**Sprint:** `{{sprint_slug}}`
**Stories:** {{sprint_stories | length}} (listed in wave order)
{{#each sprint_stories}}
- `{{slug}}` — {{title}} — status: {{status}}
{{/each}}

**Pre-flight guards:** H1 No active sprint — PASS · H2 Sprint not activated — PASS · H3 Missing approvals — PASS · H4 Stalled state — PASS · H5 Inconsistent state — PASS

**Reconcile on start:** Complete. Any stale in-progress stories from prior sessions have been auto-reset to ready-for-dev and will be re-dispatched. No resume/cleanup prompt was shown.

**Phase sequence:** Pre-flight → Build (per-story pipelines) → AVFL-on-merge → E2E → End-gate

The build will proceed silently through all stories. The next human touchpoint is the end-gate after E2E completes, unless a narrow stakes-and-timing escalation surfaces during the build (irreversible-and-imminent or build-invalidating only).

Ready to begin?</output>

    <ask>Confirm to start the build.</ask>
    <note>This is the only ask on the routine path before the end-gate. Once confirmed, the build runs silently through Phase 2, Phase 3, and Phase 4. No developer-facing HALT exists outside this Phase 1, except: (a) the Conductor-facing section-7 freeze guard (internal, developer does not see it) and (b) the developer-facing mid-flight escalation tier for irreversible-and-imminent or build-invalidating findings only (Phase 2, step 2.F). Routine findings are never raised mid-build. There is no resume/cleanup prompt, no per-story confirmation, and no other mid-build questions.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 2: BUILD PHASE — DEPENDENCY FRONTIER + PIPELINES      -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="2" goal="Build phase — event-driven dependency frontier: launch all unblocked stories concurrently, react to terminal signals, apply the mid-flight consumption hook">

    <note>This is the engine of the autonomous build. It is event-driven: the Conductor reacts to per-story terminal signals (merged | failed) rather than advancing a sequential queue. No story-count cap applies. No human gate separates stories on the routine path. The sole exception is the narrow mid-flight escalation consumption hook (step 2.F), which fires only when the escalation mechanism surfaces a finding meeting the strict stakes-and-timing bar.</note>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.0 — Initialize frontier state                    -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.0" goal="Initialize Conductor state for the dependency frontier">

      <action>Build the dependency graph from each story's `depends_on` array in {{story_map}}.
        Ignore {{sprint_waves}} as a binding source — the `depends_on` array per story is the authoritative gate.
        {{sprint_waves}} is advisory ordering metadata only.
      </action>

      <action>Initialize Conductor state:
        {{frontier}}    = []    — unblocked stories not yet launched
        {{running}}     = {}    — { slug: pipeline_handle } for in-flight stories
        {{merged}}      = []    — stories that have reached status >= review on the sprint branch
        {{blocked}}     = []    — stories that exhausted retries or have an unsatisfiable dependency
        {{retries}}     = {}    — { slug: int } per-story retry counter (pipeline-level; distinct from merge_attempts)
        {{merge_attempts}}           = {}    — { slug: int } per-story rebase-then-merge attempt counter (bound: 3); owned by step 2.2.M
        {{escalations}}              = []    — mid-flight escalation records (stakes-class, strict bar only)
        {{end_gate_escalations}}     = []    — Conductor-scoped accumulator for end-gate-expanded stakes findings across ALL stories; populated by step 2.2 signal handler from each story's S.escalations (end-gate-expanded subset); consumed by step 5 Source 1 to build decision cards. Each entry: { finding_id, stakes_class, timing_tier:"end-gate-expanded", summary, evidence, suggested_fix, story_slug }.
        {{contract_integrity_stops}}  = []    — Conductor-facing integrity stops (per story, contract fingerprint mismatch; not stakes-class, not escalations)
        {{build_log}}                 = []    — per-story pipeline outcomes for the end-gate report
        {{coverage_discharge_results}} = {}  — { slug: { outcome, scenario_id, evidence } } — populated by Phase 3 step 3.D; outcome is "verified-by-composition" for discharged deferrals
      </action>

      <action>Seed {{merged}} from current story statuses to support partial-run resume:
        For each story S in {{story_map}}:
          if S.status is "review" OR S.status is "done":
            add S.slug to {{merged}}
        This ensures dependents of already-merged blockers can satisfy the >= review gate on resume.
        Note: on a fresh run {{merged}} starts empty (no stories yet at review/done), which is correct.
      </action>

      <action>Reconcile in-progress stories from a crashed or aborted prior partial run:
        For each story S in {{story_map}} where S.status == "in-progress":
          Option A (clean worktree): if S's worktree is clean or abandonable, reset S's status to "ready-for-dev"
            via `momentum-tools sprint status-transition --story {S.slug} --target ready-for-dev --force`
            (--force is required: in-progress -> ready-for-dev is a backward transition; intentional for crash-recovery)
            and admit S to the frontier on the pass below.
          Option B (dirty worktree): record S in {{build_log}} with outcome: "stranded",
            reason: "in-progress on resume — worktree not clean" and note dependency on
            spec §6 reconcile-on-start (owned by conduct-merge-and-conflict-resolution).
            Do NOT add S to {{frontier}}; it must be handled by the reconcile-on-start handler.
        Note: stories at in-progress from a prior run must not be silently abandoned — they need
        an explicit reconcile decision, not a silent fall-through.
      </action>

      <action>Compute initial frontier: for each story S in {{story_map}}:
        if S.status == "ready-for-dev"
           AND every slug in S.depends_on is in {{merged}} (status >= review):
          add S to {{frontier}}

        Note: stories with empty depends_on are launch-ready immediately.
        Note: independent stories all enter the frontier at t=0.
      </action>

      <check if="{{frontier}} is empty AND {{running}} is empty">
        <note>All stories were either already at review/done (prior partial run) or have unsatisfiable dependencies. Build phase is already complete.</note>
        <action>Proceed to Phase 3 (AVFL-on-merge).</action>
      </check>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.1 — Launch the full frontier concurrently        -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.1" goal="Launch every story in the frontier concurrently — no story-count cap">

      <note>All stories currently in {{frontier}} are launched as concurrent per-story pipelines in a single turn. There is NO story-count cap: if 10 stories are unblocked at once, all 10 are launched. None are deferred solely because of how many are ready. This invariant is absolute — it derives from DEC-035 D4 and the no-cap critical above.</note>

      <action>For each story S in {{frontier}} (launch ALL simultaneously, not sequentially):

        2.1.1 — Remove S from {{frontier}}. Add S to {{running}}.

        2.1.2 — Transition to in-progress:
          `momentum-tools sprint status-transition --story {S.slug} --target in-progress`

        2.1.4 — CONTRACT-FREEZE GATE (fires at story launch, before any pipeline stages):
          Invoke step 2.V for story S. If step 2.V records an integrity stop for S (i.e., appends to {{contract_integrity_stops}}),
          skip all further verification actions for S in this pipeline iteration — do NOT dispatch the verifier for S.
          If step 2.V confirms the contract is unchanged, proceed to 2.1.5.

          [PLACEMENT NOTE: The freeze gate fires here, at launch, before stage-1 dev spawn and before any
          verification dispatch. This is intentional and correct: the contract file is frozen at planning and
          is static between launch and verification, so a sha256 check at launch guards the same invariant as
          one at verification-start. The per-story pipeline stages MUST NOT add a second freeze check at any
          later point. The gate belongs here, once, at launch. Adding it again inside the pipeline would
          double-gate and create redundant integrity stops.]

        2.1.5 — COVERAGE-DISPOSITION BRANCH (fires after contract-freeze check, before stage-1 dev spawn):
          INTEGRITY-STOP GUARD: If step 2.V recorded an integrity stop for S (i.e., S is in {{contract_integrity_stops}}),
          skip this step entirely — do NOT invoke step 2.C and do NOT dispatch any verifier for S. The integrity-stop
          semantics from 2.1.4 take precedence: no further verification actions are performed for S in this pipeline
          iteration. Only proceed when 2.1.4 confirmed the contract is unchanged.

          When the contract is confirmed unchanged: Invoke step 2.C for story S. Step 2.C reads S's frozen
          `coverage_disposition` from the assignment and returns one of two routing outcomes:
            { outcome: "dedicated-run" }         — perform the dedicated QA verification run during this build phase
            { outcome: "covered-by-composition", integration_scenario: "<scenario-id>" }
                                                 — skip the dedicated build-time run; record the deferral
          Bind {{coverage_disposition}}[S.slug] = the outcome string returned by step 2.C.
          Act on the routing outcome as specified in step 2.C. Do NOT dispatch the verifier at build time
          for a story whose coverage_disposition is "covered-by-composition".

        2.1.3 — STAGE-1 → STAGE-2 → STAGE-3 PIPELINE: Fire asynchronously after 2.1.4/2.1.5 resolve.
          Each story's pipeline runs independently and concurrently with other stories' pipelines.
          The pipeline emits a single terminal signal when complete; step 2.2 consumes that signal.
          The launch loop does NOT block on any stage — all per-story pipelines run concurrently.

          ── STAGE-1: DEV SPAWN ──────────────────────────────────────────────────────────────
          Resolve agent: `momentum-tools agent resolve --touches "{{S.touches | join(',')}}"`
          Bind {{dev_agent}} = the resolved agent name (e.g., "dev", "dev-build", "dev-frontend", "dev-skills").
          Bind {{writable_files}} = the explicit set of files this story is expected to create or modify.
            Derivation rule (in priority order):
              1. If the story spec contains an explicit `## What's needed` or `## Deliverables` section
                 that enumerates file paths, use those paths.
              2. Otherwise (absent or non-enumerated section), derive deterministically:
                 (a) Any file path literally named in the story spec body (e.g. in backticks or code fences).
                 (b) Any file matching the story's `touches` globs from `.momentum/stories/index.json`.
                 (c) Minus: all `.momentum/stories/` paths and all `.momentum/sprints/` paths (always forbidden).
              The fallback MUST produce an enumerable list — an empty or undefined writable_files is
              not a valid result. If steps 1-2 yield no paths, bind {{writable_files}} = [] and log a
              warning; the per-story FORBIDDEN clauses below still apply regardless.
          Spawn {{dev_agent}} as an individual agent (fan-out, NOT TeamCreate) with:
            - story_file: `.momentum/stories/{S.slug}.md`
            - sprint_slug: {{sprint_slug}}
            - worktree_path: `.worktrees/story-{S.slug}` (the story's isolated git worktree)
            - contract_part_a: path to `.momentum/sprints/{{sprint_slug}}/specs/{S.slug}.*` (Part A only)
            - writable_files: {{writable_files}} (enumerated list; agent must write ONLY these files)
          Constraint passed to agent: "Do not mutate git. Do not spawn build agents. Produce output only.
            WRITE-SCOPE: You may ONLY create or modify files listed in writable_files for this story.
            FORBIDDEN: Do NOT edit `.momentum/stories/{S.slug}.md` (this story's own spec file) — it is read-only input.
            FORBIDDEN: Do NOT edit any other story's spec file under `.momentum/stories/` or its verification contract under `.momentum/sprints/`.
            FORBIDDEN: Do NOT edit any file outside the declared writable_files set.
            CROSS-ARTIFACT RULE: If during implementation you identify a problem that belongs to a DIFFERENT artifact (e.g., another story's spec, a shared reference file not in your writable set), do NOT edit that artifact. Instead, record it as a reconciliation note in your completion signal so the Conductor can route it to the owning story via momentum:triage or create-story."
          This spawn fires concurrently with all other frontier story spawns (no story-count cap).

          When {{dev_agent}} returns its implementation-complete signal:
          Bind {{stage1_output}} = the agent's return value (implementation-complete + file_list).
          Bind {{stage1_cross_artifact_notes}} = {{stage1_output}}.cross_artifact_notes (default []).

          WRITE-SCOPE COMMIT GUARD: Before committing, verify that every file staged by `git add -u`
            falls within {{writable_files}} for story S. To enforce this:
            — Run `git -C .worktrees/story-{S.slug} diff --name-only --cached` after staging to
              obtain the actual staged file list.
            — For each staged path P: confirm P is in {{writable_files}}.
              If P is NOT in {{writable_files}} AND P is not `.momentum/stories/{S.slug}.md` (always forbidden),
              log a warning in {{build_log}} and UNSTAGE P (`git -C .worktrees/story-{S.slug} restore --staged P`)
              before committing. Do NOT commit out-of-scope edits.
          The Conductor (sole git-mutation authority) commits the produced output:
            `git -C .worktrees/story-{S.slug} add -u`
            (apply write-scope guard above before proceeding)
            `git -C .worktrees/story-{S.slug} commit -m "feat({S.slug}): implement {{S.title}}"`

          CROSS-ARTIFACT ROUTING: If {{stage1_cross_artifact_notes}} is non-empty, accumulate each
            entry into {{build_cross_artifact_notes}} with the story slug attached:
              { slug: S.slug, artifact: entry.artifact, note: entry.note }
            These are deferred — do NOT invoke momentum:triage inline here. The full batch is
            routed to momentum:triage at build-phase completion (step 2.2 / Phase 2 wrap-up),
            mirroring the triaged-out path for fix-mode findings.

          Then advance this story's pipeline to stage-2.

          ── STAGE-2: CONCURRENT QA + CODE-REVIEW FAN-OUT ───────────────────────────────────
          Stage 2 fires AFTER the stage-1 commit, BEFORE the merge at step 2.2.M (pre-merge review).
          Apply coverage routing established at 2.1.5:
            - If {{coverage_disposition}}[S.slug] == "covered-by-composition": skip stage-2 entirely;
              bind {{stage2_findings}} = [] and advance directly to stage-3 with an empty findings list.
            - If {{coverage_disposition}}[S.slug] == "dedicated-run" (default): dispatch the fan-out below.

          DIFF RANGE (Scenario A — Pre-Merge Review, per references/per-story-review-diff-range.md):
          Compute the per-story diff at review time — do NOT capture a SHA; do NOT wait for the merge:
            {{story_diff}} = output of:
              `git -C .worktrees/story-{S.slug} diff \
                $(git -C .worktrees/story-{S.slug} \
                  merge-base sprint/{{sprint_slug}} story/{{S.slug}}) \
                ..story/{{S.slug}}`
          Pass the materialized diff (not the range expression) to both reviewers.
          DO NOT use over-scoped ranges (main...HEAD) or two-dot sprint-tip forms.
          Authoritative pattern and rationale: references/per-story-review-diff-range.md.

          Spawn the following two agents CONCURRENTLY (individual-agent fan-out, NOT TeamCreate):

            REVIEWER A — qa-reviewer agent:
              Inputs:
                - story_slug: S.slug
                - worktree_path: `.worktrees/story-{S.slug}`
                - verification_contract: `.momentum/sprints/{{sprint_slug}}/specs/{S.slug}.*`
                - story_diff: {{story_diff}}
              Constraint: "Read-only. Do not modify code. Do not mutate git. Produce findings only."
              Returns: per-AC classification (VERIFIED / PARTIAL / MISSING / BLOCKED) with stakes_class
                on each finding, normalized to the canonical finding schema (finding-schema.md).
                Source field: `qa-reviewer`.

            REVIEWER B — momentum:code-reviewer skill (bmad-code-review adapter):
              Inputs:
                - story_slug: S.slug
                - story_diff: {{story_diff}}
                - worktree_path: `.worktrees/story-{S.slug}`
              Constraint: "Report-only mode. Do not modify code. Do not mutate git. Produce findings only."
              Returns: normalized finding records per canonical finding schema (finding-schema.md),
                stakes_class populated on every record. Source field: `bmad-code-review`.

          When BOTH reviewers have returned:
          Bind {{qa_findings}} = findings array from REVIEWER A.
          Bind {{cr_findings}} = findings array from REVIEWER B.
          Merge into {{stage2_findings}}: deduplicated union of {{qa_findings}} and {{cr_findings}},
            severity-sorted (critical → major → minor → low).
          Deduplication: if a qa-reviewer finding and a bmad-code-review finding describe the same
            location and issue, keep the higher-severity record; annotate source as
            "qa-reviewer+bmad-code-review".
          Each finding in {{stage2_findings}} carries the canonical base fields of finding-schema.md,
            including: story_slug, source, stakes_class, severity, verdict, type, location, summary,
            detail, evidence, legitimate, ac_id (where applicable), and suggested_fix (when provided).
          Then advance this story's pipeline to stage-3.

          ── STAGE-3 FIX LOOP ───────────────────────────────────────────────────────────────
          Invoke step 2.S3 for story S, passing {{stage2_findings}} as input.
          Step 2.S3 (live) runs the directed fix-loop (Phase B→C→D, retry-bound-3, escalation routing).
          When step 2.S3 emits its terminal signal, this story's pipeline emits its own terminal signal
            to step 2.2 — either { slug, outcome: "merged", ... } or { slug, outcome: "failed", ... } —
            per the outcome and quarantine rules in step 2.S3.

        Store pipeline_handle in {{running}}[S.slug].
      </action>

      <note>After launching the full frontier, the Conductor enters the heartbeat (step 2.2): it waits for terminal signals from running pipelines and reacts to each as it arrives. It does not advance manually — the event drives the next action.</note>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.V — Contract-freeze check (per story, first      -->
    <!-- step of verification — spec §7 step 2)                  -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.V" goal="Contract-freeze check — Conductor asserts sha256(contract) == frozen_sha256 before per-story verification; Conductor-facing integrity stop on mismatch">

      <note>CONDUCTOR-FACING INTEGRITY GATE. This step is the first thing the Conductor does before running verification for each story. It is executed per story — once per story, for that story's contract. It is NOT a developer-facing HALT and NOT a stakes-class escalation. It is the Conductor checking its own inputs before trusting a verification result. The developer is never paused, prompted, or shown this check. Spec reference: §7 step 2 (the first carve-out from the DEC-035 #1 "no developer-facing HALT outside pre-flight" invariant). The second carve-out is the developer-facing mid-flight escalation tier (step 2.F); these two carve-outs are different in kind and must not be conflated.</note>

      <note>This step is not a finding disposition. It produces no disposition of fixed | dismissed | triaged-out | escalated. A fingerprint mismatch is not a stakes-class finding and does not enter the silent auto-fix path. It is a structural integrity assertion the Conductor makes about its own inputs: "is the contract under verification the same contract that was frozen at assignment?" If not, the Conductor stops before producing any verification result for that story and surfaces the mismatch to itself — not to the developer.</note>

      <note>Vocabulary invariant (do not widen): stakes classes (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine) apply only to build findings. The freeze check belongs to none of these classes. Timing tiers (end-gate-expanded | mid-flight) apply only to finding routing. The freeze check uses neither tier. Dispositions (fixed | dismissed | triaged-out | escalated) apply only to findings in the auto-fix loop or mid-flight escalation. The freeze check produces none of these.</note>

      <!-- ── Per-story invocation ────────────────────────────── -->
      <action>For each story S that is about to enter verification:
        1. Resolve S's assignment from `story_assignments[S.slug]` in the sprint record (`.momentum/sprints/index.json`).
           Bind:
             {{contract_path}}   = assignment.contract.path
             {{frozen_sha256}}   = assignment.contract.frozen_sha256
        2. Compute the current fingerprint of the contract file on disk:
             {{live_sha256}} = sha256( file-contents at {{contract_path}} )
           Use a SHA-256 digest of the exact file bytes. (Shell reference: `sha256sum {{contract_path}}` or `shasum -a 256 {{contract_path}}`.)
        3. Compare {{live_sha256}} to {{frozen_sha256}}.
      </action>

      <!-- ── Match path — proceed ───────────────────────────── -->
      <check if="{{live_sha256}} == {{frozen_sha256}}">
        <note>Contract unchanged. The contract file on disk is identical to what was frozen at assignment. Verification integrity is confirmed. Proceed to per-story verification without interruption.</note>
        <action>Allow per-story verification to proceed for story S. The build is not interrupted.</action>
      </check>

      <!-- ── Mismatch path — Conductor-facing integrity stop ── -->
      <check if="{{live_sha256}} != {{frozen_sha256}}">
        <note>Contract has drifted since it was frozen at assignment. The Conductor must NOT silently re-verify story S against the changed contract. Doing so would mean the verification result rests on a contract that was never assigned — the end-gate would inherit a corrupted result. The mismatch surfaces to the Conductor only. The developer is not paused, prompted, or shown this stop.</note>

        <action>Integrity stop — Conductor-facing only:
          1. Do NOT dispatch the per-story verifier for story S.
          2. Do NOT produce a verification result for story S (no VERIFIED / PARTIAL / MISSING / BLOCKED disposition is recorded from a drifted contract).
          3. Record the integrity stop in {{build_log}}:
             { slug: S.slug, title: S.title, outcome: "contract-integrity-stop",
               reason: "contract fingerprint mismatch — live sha256 does not equal frozen_sha256",
               contract_path: {{contract_path}},
               frozen_sha256: {{frozen_sha256}},
               live_sha256: {{live_sha256}} }
          4. Record an entry in {{contract_integrity_stops}} that identifies story S as integrity-stopped,
             so the end-gate report can surface it to the developer as an informational item:
             { slug: S.slug, contract_path: {{contract_path}}, frozen_sha256: {{frozen_sha256}}, live_sha256: {{live_sha256}} }
             Note: {{contract_integrity_stops}} is a dedicated collection initialized at step 2.0 — it is separate from
             {{escalations}} (which is reserved for stakes-class mid-flight records only, per its initialization in step 2.0).
          5. Remove S from {{running}} without transitioning it to "review".
             Mark S in Conductor in-memory state as integrity-stopped (not blocked, not failed).
          6. CONTINUE the build phase. Other stories in {{running}} and {{frontier}} are unaffected.
             The mismatch on one story does not halt the rest of the build.
        </action>

        <note>This is the ONE sanctioned non-developer halt in the verification path. It does not raise a stakes-class escalation. It does not enter the silent auto-fix loop. It is not dismissable with a rationale — there is no disposition to dismiss. It is not a mid-flight escalation eligible for the developer-facing pause (step 2.F). It is the Conductor catching its own integrity violation before it can corrupt a verification result, then continuing the build. The developer sees the mismatch in the end-gate report as an informational note (the integrity-stop entry in {{contract_integrity_stops}}), not as a prompt during the build.</note>
      </check>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.S3 — Stage-3 fix loop (Phase B–D, per story)     -->
    <!-- Invoked after stage-2 (QA + code-review) returns        -->
    <!-- findings for story S. Governs: spec §3 Phase B–D + §4.  -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.S3" goal="Stage-3 per-story fix loop — directed fixer with retry-bound-3, escalation routing (DEC-036 D1/D2)">

      <note>INVOCATION CONTEXT. Step 2.S3 runs after stage-2 (QA reviewer + code-review) has returned findings for story S. It is the Phase B→C→D loop per spec §3 and §4: apply fixes via the directed fixer, optionally run /simplify, re-check, and repeat — bounded at 3 attempts per finding. The Conductor invokes this step with the merged findings list from stage-2. The Conductor remains the sole git-mutation authority; the directed fixer (subagent) produces output only and never commits itself.

      Stage-2 callers (QA reviewer + code-review adapter) and Phase D re-check callers must derive the per-story diff using the canonical pre-merge merge-base pattern (Scenario A). Canonical pattern: references/per-story-review-diff-range.md.</note>

      <note>ROUTINE-PATH GUARANTEE (DEC-035 D1, always-on default). Routine findings (stakes_class == routine) are ALWAYS auto-fixed inside this loop with no human gate. The always-auto-fix behavior for routine findings is UNCHANGED and PRESERVED. This is the anti-firehose baseline: the vast majority of findings complete Phase B→D autonomously without any escalation or human contact.</note>

      <note>ESCALATION-PATH GUARD (DEC-036 D2 amendment). A stakes-class finding (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) is NEVER silently auto-fixed inside this loop. Such a finding is immediately routed to the escalation channel (end-gate-expanded tier by default; mid-flight tier only on the narrow irreversible-and-imminent OR build-invalidating bar). This is the stage-3 leg of the three-place absolute — the guard must be honored here even though the other two legs (schema comment, dev executor) are threaded by their own stories.</note>

      <note>ISOLATION INVARIANT. An escalated finding for one item does NOT stop routine findings on other items from completing their normal fix → re-check → bound-3 cycle. The escalation path is non-destructive to the routine path. Within a single story's findings list, escalated findings exit the retry loop; routine findings continue their fix/re-check cycle to completion regardless.</note>

      <!-- ── Entry: bind findings, initialize per-finding retry state ─── -->

      <action>Bind {{stage2_findings}} = merged findings array from stage-2 (qa-reviewer + bmad-code-review output for story S),
        deduplicated and severity-sorted (highest severity first).
        Bind {{fix_attempts}} = {} — per-finding retry counter keyed by finding ID.
        Bind {{finding_dispositions}} = [] — per-finding outcome records (fixed | dismissed | triaged-out | escalated | blocked).
          [NOTE: "blocked" is Conductor-internal-only, used when retry budget is exhausted. It is NOT in the canonical four-value disposition set (fixed | dismissed | triaged-out | escalated) defined by finding-schema.md. Before blocked findings reach the end-gate report or any schema consumer, they are treated as escalated findings (the canonical catch-all for findings that cannot be fixed, dismissed, or triaged-out per finding-schema.md §73). The triage spin-out path for blocked findings serves the same routing purpose as the escalated path.]
        Bind {{end_gate_escalations}} = [] — escalated findings routed to end-gate-expanded tier (held for Phase 5).
          [WIRED: {{end_gate_escalations}} is written here, emitted in the pipeline signal payload, and consumed by the end-gate report at step 5. Step 5 merges these per-story escalations with AVFL and E2E escalation leftovers into {{stakes_findings}} — the decision-card section of the HTML report. Each entry must carry: finding_id, stakes_class, summary, evidence, suggested_fix. These fields populate the decision cards. See references/endgate-report-renderer.md for the full data contract and rendering spec.]
        Bind {{mid_flight_escalations}} = [] — escalated findings accumulated for single dispatch to step 2.F (the shared-primitive escalation hook).
      </action>

      <check if="{{stage2_findings}} is empty">
        <note>No findings from stage-2. Skip the fix loop entirely and proceed to stage-4 (merge). This is the clean path — the story merges immediately after stage-2.</note>
        <action>Proceed to stage-4 (merge) for story S. Do not invoke the directed fixer.</action>
      </check>

      <!-- ── Phase B: CONVERGE — directed fixer invocation ──────────── -->

      <action>PHASE B — Invoke the directed fixer (momentum:dev in fix mode) as a subagent (individual-agent, NOT TeamCreate):
        Input: {{stage2_findings}} (or the subset of findings still unresolved in the current loop iteration).
        Pass {{writable_files}} (the same set passed to the stage-1 dev spawn for story S) to the fixer.
        Constraint passed to fixer subagent: "Do not mutate git. Do not spawn build agents. Apply fixes and return per-finding dispositions. Produce output only.
          WRITE-SCOPE: You may ONLY create or modify files listed in writable_files for this story.
          FORBIDDEN: Do NOT edit `.momentum/stories/{S.slug}.md` (this story's own spec file) — it is read-only input.
          FORBIDDEN: Do NOT edit any other story's spec file under `.momentum/stories/` or its verification contract under `.momentum/sprints/`.
          FORBIDDEN: Do NOT edit any file outside the declared writable_files set.
          CROSS-ARTIFACT RULE: If a finding points to a problem that belongs to a DIFFERENT artifact outside this story's writable_files set, do NOT edit that artifact in-tree. Return disposition `triaged-out` for that finding so the Conductor can route a reconciliation note to the owning story."
        Invocation contract: skills/momentum/references/directed-fix-invocation-contract.md.
        The fixer applies every routine legitimate finding automatically (no prompt), returns escalated disposition for stakes-class findings (not silently fixed), dismissed with non-empty rationale for non-genuine findings, or triaged-out for out-of-scope new work.
        The Conductor (not the fixer) commits any applied fixes after the fixer returns.
      </action>

      <!-- ── Route each finding by disposition returned by fixer ───── -->

      <action>For each finding F in the fixer's returned dispositions:

        CASE disposition == "fixed":
          — Stakes-class guard: VERIFY that F.stakes_class == "routine". If the fixer returns "fixed" for a stakes-class finding (non-routine), treat it as an implementation error — do NOT commit the fix. Log a warning in {{build_log}} and re-classify F as escalated (see escalated path below).
            When re-classifying: look up the inbound finding for F.finding_id in {{stage2_findings}} to recover stakes_class, summary, evidence, and suggested_fix (the fixer's "fixed" disposition object does not carry these fields). Default timing_tier to "end-gate-expanded" (the conservative default per finding-schema.md) since the fixer never sets timing_tier on a "fixed" disposition.
          — Commit the applied fix to the story worktree .worktrees/story-{S.slug}: `git -C .worktrees/story-{S.slug} add -u && git -C .worktrees/story-{S.slug} commit -m "fix({S.slug}): auto-fix {F.summary}"`
          — Record F in {{finding_dispositions}}: { finding_id: F.id, disposition: "fixed", summary: F.summary, stakes_class: "routine" }

        CASE disposition == "dismissed":
          — Validate non-empty rationale: if F.dismissal_rationale is empty or missing, treat as invalid — log error in {{build_log}} and re-present F to the fixer in the next iteration (do not record as dismissed until a rationale is supplied).
          — Record F in {{finding_dispositions}}: { finding_id: F.id, disposition: "dismissed", summary: F.summary, dismissal_rationale: F.dismissal_rationale }

        CASE disposition == "triaged-out":
          — Look up the inbound finding I for F.finding_id in {{stage2_findings}} to recover summary, detail, location, and suggested_fix (the fixer's triaged-out disposition object carries only finding_id and disposition; the descriptive fields live on the inbound finding).
          — Record F in {{finding_dispositions}}: { finding_id: F.finding_id, disposition: "triaged-out", summary: I.summary, detail: I.detail, location: I.location, suggested_fix: I.suggested_fix }
          — The Conductor will route triaged-out findings to momentum:triage at build-phase completion (not inline here — triage is deferred to avoid blocking the fix loop). The recovered descriptive fields ensure the triage stub has actionable content.

        CASE disposition == "escalated":
          — Look up the inbound finding I for F.finding_id in {{stage2_findings}} to recover stakes_class, summary, evidence, and suggested_fix (the fixer's escalated disposition object carries these in the nested escalation object and does not echo them at the top level; join by finding_id). Canonical shape defined in directed-fix-invocation-contract.md §"Canonical Fixer Output Shape".
            Resolve fields: stakes_class = I.stakes_class; timing_tier = F.escalation.timing_tier (NESTED — read from inside the escalation object, NOT from F.timing_tier; default "end-gate-expanded" if absent); summary = I.summary; evidence = F.escalation.evidence (inline from fixer) or I.evidence; suggested_fix = I.suggested_fix.
          — Record in {{finding_dispositions}}: { finding_id: F.finding_id, disposition: "escalated", stakes_class: stakes_class, timing_tier: timing_tier, summary: summary, evidence: evidence, suggested_fix: suggested_fix }
          — F is removed from the retry-bound-3 loop IMMEDIATELY. No further fix/re-check attempts will be run against F inside this loop.
          — Route by timing tier:
              IF timing_tier == "mid-flight":
                — The finding is irreversible-and-imminent OR build-invalidating (per skills/momentum/references/directed-fix-invocation-contract.md narrow bar).
                — Append to {{mid_flight_escalations}} (accumulated for dispatch to step 2.F after all findings are processed).
              ELSE (timing_tier == "end-gate-expanded" OR timing_tier not set):
                — The finding is stakes-class but does NOT meet the mid-flight bar. Route to end-gate-expanded tier (the default and safety net).
                — Append to {{end_gate_escalations}}: { finding_id: F.finding_id, stakes_class: stakes_class, timing_tier: "end-gate-expanded", summary: summary, evidence: evidence, suggested_fix: suggested_fix }
                — Record in {{build_log}}: { slug: S.slug, event: "stage3-escalation", disposition: "escalated", timing_tier: "end-gate-expanded", finding_summary: summary }
                — Continue the fix loop. This escalation does NOT pause the build or stop other findings from completing.
      </action>

      <!-- ── Optional Phase C: /simplify cleanup pass ─────────────── -->

      <note>PHASE C (/simplify) is an optional post-fixer cleanup pass. It runs AFTER the fixer (Phase B), NEVER concurrently — it mutates the tree and must not double-mutate code the fixer just touched. /simplify is NOT a bug hunter; it applies cleanup only. Its findings, if any, feed back into the next Phase B iteration as routine cleanup findings.</note>

      <!-- ── Mid-flight dispatch for bar-clearing escalations ───────── -->

      <check if="{{mid_flight_escalations}} is non-empty">
        <note>One or more findings in the current iteration were classified mid-flight by the fixer. Per the SHARED-PRIMITIVE CONTRACT (step 2.F / references/escalation.md), the Conductor does NOT pre-classify or loop over candidates itself. It passes the full {{mid_flight_escalations}} array to the escalation engine (step 2.F) in a single invocation — the engine owns bar evaluation and the pause/continue decision. Other routine findings continue their fix/re-check cycle unaffected.</note>
        <action>Invoke step 2.F (the mid-flight escalation consumption hook) once with the full {{mid_flight_escalations}} array as the findings input.
          The escalation engine evaluates the bar for each finding and returns "pause-branch" or "continue" per its contract (references/escalation.md).
          Record outcome in {{build_log}}: { slug: S.slug, event: "stage3-mid-flight-escalation", disposition: "escalated", timing_tier: "mid-flight", finding_count: length({{mid_flight_escalations}}) }
          Append each finding to {{escalations}}: { slug: S.slug, stakes_class: F.stakes_class, timing_tier: "mid-flight", disposition: "escalated" }
        </action>
      </check>

      <!-- ── Phase D: RE-CHECK gate — loop control ─────────────────── -->

      <action>PHASE D — RE-CHECK: Re-run only the reviewer(s) that originally raised unresolved routine findings.
        Collect {{remaining_findings}} = findings not yet resolved (status not fixed | dismissed | triaged-out | escalated).
        Note: escalated findings (both end-gate-expanded and mid-flight) are ALREADY removed from {{remaining_findings}} — they exit the retry loop at escalation time and are never re-checked inside the loop.
        DIFF RANGE FOR RE-CHECK: Use the same canonical pre-merge merge-base pattern as stage 2. The story branch is still pre-merge at this point. Canonical pattern: references/per-story-review-diff-range.md (Scenario A — Pre-Merge Review).
      </action>

      <check if="{{remaining_findings}} is empty">
        <note>All findings are resolved (fixed, dismissed, triaged-out, or escalated). The fix loop is clean. Proceed to stage-4 (merge).</note>
        <action>Proceed to stage-4 (merge) for story S.
          Emit partial pipeline signal payload (for eventual terminal signal from stage-4):
            leftover_findings: [] (none remaining)
            escalations: {{end_gate_escalations}} (held for Phase 5 end-gate; mid-flight escalations already dispatched)
        </action>
      </check>

      <check if="{{remaining_findings}} is non-empty">

        <!-- ── Retry-bound-3 enforcement ──────────────────────── -->

        <action>For each finding F in {{remaining_findings}}:
          Increment {{fix_attempts}}[F.id] (initialize to 0 if absent).
        </action>

        <check if="any F in {{remaining_findings}} has {{fix_attempts}}[F.id] less than 3">
          <note>Retry budget available for at least one remaining finding. Loop back to Phase B with the unresolved findings.</note>
          <action>Return to Phase B (CONVERGE): invoke the directed fixer again with {{remaining_findings}} (the subset still unresolved).
            Do not pass already-fixed, dismissed, triaged-out, or escalated findings back to the fixer — pass only the genuinely unresolved ones.
          </action>
        </check>

        <check if="all F in {{remaining_findings}} have {{fix_attempts}}[F.id] >= 3">
          <note>Retry budget exhausted for all remaining findings. Mark each exhausted finding BLOCKED. Continue to the next story — do NOT halt the whole build.</note>
          <action>For each finding F in {{remaining_findings}} (where {{fix_attempts}}[F.id] >= 3):
            Record F in {{finding_dispositions}}: { finding_id: F.id, disposition: "blocked", summary: F.summary, attempts: {{fix_attempts}}[F.id] }
            Append to {{build_log}}: { slug: S.slug, event: "stage3-finding-blocked", finding_id: F.id, finding_summary: F.summary, attempts: {{fix_attempts}}[F.id] }
          </action>
          <action>Emit partial pipeline signal payload:
            leftover_findings: blocked findings list (for end-gate report and triage spin-out)
            escalations: {{end_gate_escalations}} (held for Phase 5 end-gate)
            Note: mid-flight escalations were already dispatched inline; they do not appear in leftover_findings.
          </action>
          <note>BLOCKED-then-continue: the whole-build is NOT halted. However, per spec §3 stage-3 ('BLOCKED -> spin a stub via momentum:triage, leave unmerged'), story S is NOT merged. The Conductor removes S from {{running}} WITHOUT transitioning it to stage-4, spins a triage stub for the blocked findings, and continues building other stories in {{running}} and {{frontier}} unaffected. The story remains unmerged; dependents whose >= gate requires S's merge become unsatisfiable, which is the intended consequence of an unmergeable story.</note>
          <action>Mark story S as BLOCKED (do NOT invoke stage-4 merge for S).
            Remove S from {{running}}.
            Note: do NOT transition S to a terminal status here — the story remains at its current non-terminal status. The terminal transition (closed-incomplete) is deferred to Phase 5 approve, which performs the single terminal transition for all stranded/blocked stories (quarantine convention, per spec §6/§8). "blocked" is Conductor in-memory state only (tracked via leftover_findings and build_log).
            Spin a triage stub for the blocked findings: invoke momentum:triage with the blocked findings list for S, so they are queued into the backlog.
            Record in {{build_log}}: { slug: S.slug, event: "stage3-story-blocked", leftover_count: length(blocked findings), stranded: true, note: "story left unmerged per spec §3; terminal status transition deferred to Phase 5 approve" }
            Continue building remaining stories in {{running}} and {{frontier}}.
          </action>
        </check>

      </check>

    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.C — Coverage-disposition branch (per story)     -->
    <!-- Reads frozen coverage_disposition; routes dedicated-run -->
    <!-- vs. covered-by-composition. Does not classify findings. -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.C" goal="Coverage-disposition branch — read frozen coverage_disposition from the assignment and route: dedicated-run (perform QA at build time) vs. covered-by-composition (skip build-time QA; record deferral to named integration scenario at AVFL/merge)">

      <note>READS, DOES NOT DECIDE. This step is purely mechanical. The Conductor reads the frozen `coverage_disposition` value from the assignment record it was handed at planning. It does not compute, infer, choose, or override the disposition — the disposition was set upstream (planning/contract freeze) and is immutable at build time. The only judgment-shaped behavior allowed is the safe default for a missing or unrecognized value, and that default is conservative (`dedicated-run`; do not skip verification). Spec reference: §7 step 4 (build-time verifier dispatch gated on coverage_disposition).</note>

      <note>TIMING-AND-VENUE ONLY — DEC-036 does NOT change this branch. DEC-036's amendments (narrow stakes-gated mid-flight escalation; legible dispositions fixed | dismissed | triaged-out | escalated with required non-empty rationale for dismissals; end-gate-expanded vs. mid-flight timing tiers; anti-rubber-stamp end-gate) concern HOW findings are classified and WHEN stakes-class findings leave the silent auto-fix path. This branch concerns only WHEN the verification run happens (build vs. AVFL/merge) and WHERE it runs. Choosing `covered-by-composition` changes only the timing and venue of the QA run; it never demotes, hides, silences, or auto-resolves any finding — including any stakes-class finding. A stakes-class finding (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) that surfaces when the deferred verification is discharged at AVFL/merge is still routed out of the silent auto-fix path and rendered in the report by the finding schema and report — NOT by this branch. The deferral does not weaken that routing. This boundary must remain clear: a future reader must not mistake `covered-by-composition` for a way to bypass stakes handling.</note>

      <note>NON-GOALS — guardrails this branch must never violate:
        (1) This branch must not change how any finding is classified. Finding classification (stakes classes, dispositions, timing tiers) belongs to the finding schema and the auto-fix / escalation machinery — not to coverage routing.
        (2) This branch must not demote, hide, silence, or auto-resolve any finding, including a stakes-class finding. The deferral records the timing/venue change only.
        (3) This branch must not widen build-time verification beyond what the disposition specifies (no adding extra verification runs for a `dedicated-run` story beyond its one run).
        (4) This branch must not produce a second dedicated verification run for a story already marked `covered-by-composition`.
        (5) This branch must not re-derive or substitute its own judgment for the frozen `coverage_disposition` value.
      </note>

      <!-- ── Per-story invocation ────────────────────────────── -->
      <action>For each story S entering the coverage-disposition check:
        1. Resolve S's assignment from `story_assignments[S.slug]` in the sprint record (`.momentum/sprints/index.json`).
        2. Read the frozen coverage fields from the assignment's contract block:
             {{coverage_disposition}}   = assignment.contract.coverage_disposition
             {{covered_by_scenario}}    = assignment.contract.covered_by_scenario  (may be null)
        3. Evaluate {{coverage_disposition}} against the two recognized values:
             "dedicated-run"           — recognized; route to dedicated-run path below
             "covered-by-composition"  — recognized; route to covered-by-composition path below
             any other value (including null, missing, empty string, or unrecognized string):
                                       — treat as "dedicated-run" (safe default; see safe-default check below)
      </action>

      <!-- ── Safe default: missing or unrecognized ────────────── -->
      <check if="{{coverage_disposition}} is null OR missing OR not in {'dedicated-run', 'covered-by-composition'}">
        <note>Missing or unrecognized `coverage_disposition`. The safe default is `dedicated-run` — treat this story as requiring a dedicated verification run at build time. Do NOT silently skip verification when the disposition is absent or unrecognized. The conservative choice is always to run the dedicated check. This prevents silent coverage gaps from malformed or missing assignment data.</note>
        <action>Log a warning in {{build_log}} for story S: { slug: S.slug, event: "coverage-disposition-default", reason: "coverage_disposition was missing or unrecognized — defaulted to dedicated-run", observed_value: {{coverage_disposition}} }.
          Treat S as `dedicated-run` for all purposes in this build phase. Proceed to the dedicated-run path below.
        </action>
      </check>

      <!-- ── Path A: dedicated-run ─────────────────────────────── -->
      <check if="{{coverage_disposition}} == 'dedicated-run' (or defaulted to dedicated-run)">
        <note>This story gets a dedicated QA verification run during the build phase. The verifier is dispatched for this story as normal. No deferral is recorded. The dedicated run is the standard build-time path.</note>
        <action>Return routing outcome to step 2.1.5: { outcome: "dedicated-run" }.
          Proceed to verifier dispatch for story S in the build phase. Exactly one dedicated verification run is performed.
        </action>
      </check>

      <!-- ── Path B guard: covered-by-composition with no named scenario ── -->
      <check if="{{coverage_disposition}} == 'covered-by-composition' AND ({{covered_by_scenario}} is null OR missing OR empty string)">
        <note>AC 3 requires that for a covered-by-composition story the Conductor names the specific integration scenario that will discharge the story's verification. A null/missing/empty covered_by_scenario means there is no named downstream owner — skipping the dedicated run would create a silent coverage gap. The safe default is dedicated-run, mirroring the AC 5 treatment already applied to a missing coverage_disposition.</note>
        <action>Log a warning in {{build_log}} for story S:
            { slug: S.slug, event: "coverage-disposition-incomplete",
              reason: "coverage_disposition is 'covered-by-composition' but covered_by_scenario is null/missing/empty — cannot defer without a named integration scenario; defaulted to dedicated-run",
              observed_coverage_disposition: "covered-by-composition",
              observed_covered_by_scenario: {{covered_by_scenario}} }
          Treat S as `dedicated-run` for all purposes in this build phase. Proceed to the dedicated-run path (Path A) below.
        </action>
      </check>

      <!-- ── Path B: covered-by-composition ───────────────────── -->
      <check if="{{coverage_disposition}} == 'covered-by-composition' AND {{covered_by_scenario}} is present AND non-empty">
        <note>This story's verification is deferred to a named integration scenario at AVFL/merge. No dedicated QA verification run is performed for this story at build time. The Conductor records the deferral explicitly — it does not silently drop the verification. The named integration scenario ({{covered_by_scenario}}) is the downstream discharge point at AVFL/merge (Phase 3). The deferral record is informational: it states THAT the run was skipped and WHICH scenario owns the discharge. Nothing in this record changes how findings from that scenario are classified, escalated, or reported.</note>
        <note>PRECONDITION — a named scenario is required. This path is reached only when covered_by_scenario is present and non-empty. When it is null/missing/empty, the guard above fires first and routes to dedicated-run instead. This ensures AC 3's naming requirement is a hard precondition for skipping the dedicated build-time run.</note>
        <action>Skip the dedicated QA verification run for story S at build time. Do NOT dispatch the per-story verifier for S during this build phase.
          Record the deferral in {{build_log}}:
            { slug: S.slug, title: S.title, event: "coverage-disposition-deferred",
              coverage_disposition: "covered-by-composition",
              covered_by_scenario: {{covered_by_scenario}},
              note: "Dedicated build-time QA run skipped. Verification debt discharged at AVFL/merge by the named integration scenario." }
          Return routing outcome to step 2.1.5: { outcome: "covered-by-composition", integration_scenario: {{covered_by_scenario}} }.
          Do not produce a VERIFIED / PARTIAL / MISSING / BLOCKED verification disposition for story S from this build-phase step — the verification result belongs to the integration scenario at AVFL/merge.
        </action>
        <note>GUARDRAIL — no second run. Once this routing outcome is returned and the deferral is recorded, the Conductor must NOT perform an additional dedicated verification run for S during the build phase. The deferral is a one-way routing decision for the build phase; it does not prevent the integration scenario from running at AVFL/merge — it ensures the dedicated build-time run does not also run. Double-running wastes effort and can produce contradictory signals.</note>
        <note>STAKES-CLASS BOUNDARY — deferral does not weaken routing. If the integration scenario at AVFL/merge surfaces a stakes-class finding (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture), that finding is still routed out of the silent auto-fix path and rendered in the report by the finding schema and report. The deferral from this build-phase branch does not weaken, suppress, or narrow that routing. The timing/venue changed; the routing rules did not.</note>
        <note>DOWNSTREAM DISCHARGE — wired in Phase 3 step 3.D. The `coverage-disposition-deferred` build_log record and the `covered_by_scenario` field drive the discharge consumer at AVFL/merge (Phase 3 step 3.D). Step 3.D reads all deferred records, runs each named integration scenario, records the outcome as `verified-by-composition` on pass, and surfaces any undischarged deferral as a leftover finding at the end-gate. The discharge loop is closed — the deferral is not silently assumed satisfied.</note>
      </check>

    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.2 — Heartbeat: react to each terminal signal     -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.2" goal="Heartbeat — react to per-story terminal signals without requiring human input to advance">

      <note>This step is the event-driven loop of the build phase. The Conductor receives terminal signals from running pipelines. Each signal triggers a specific reaction. No human input is needed to advance between stories on the routine path — the loop runs autonomously until the frontier is exhausted and all pipelines have terminated.</note>

      <note>Terminal signals: a per-story pipeline emits exactly one of: { slug, outcome: "merged", leftover_findings: [...], escalations: [...] } OR { slug, outcome: "failed", reason: "...", retry_count: int, escalations: [...] }. The Conductor reacts to each signal as it arrives from any running pipeline.

Note on signal vocabulary: spec §3 lists three reactions — merged, blocked, failed. "blocked" is NOT a pipeline-emitted signal; it is a Conductor-assigned categorization applied after retries are exhausted or a dependency becomes unsatisfiable (see exhausted-retries and completion-sweep branches below). The two-signal model here is intentionally reconciled with spec §3's three-term list: pipelines emit only merged or failed; the Conductor derives blocked from failed exhaustion and dep-unsatisfiable outcomes.</note>

      <!-- ── Signal: merged ──────────────────────────────────── -->
      <check if="terminal signal received with outcome == 'merged' for story S">

        <!-- Consumption hook: inserted BETWEEN the terminal signal and the "continue" action -->
        <!-- See step 2.F for the full hook definition. Execute it before re-evaluating the frontier. -->
        <action>Invoke consumption hook (step 2.F) with S's escalations array from the terminal signal.
          The hook determines whether any finding in S.escalations meets the narrow mid-flight bar.
          The hook defers detection and classification to the escalation mechanism — the frontier does not classify.
          Outcome: hook returns "pause-branch" or "continue".
        </action>

        <check if="hook returns 'pause-branch'">
          <action>Execute mid-flight escalation pause for story S (step 2.F handles the pause-ask-resume).
            While S's branch is paused: other stories in {{running}} and any newly-unblocked stories continue unaffected.
            Pausing one branch does NOT halt the rest of the build phase.
          </action>
          <note>After the pause is resolved (developer responds via step 2.F with Proceed, Change, or Abort-that-branch), the hook returns "continue" to step 2.2 for all three outcomes. Proceed and Change resume the branch (merge and frontier re-evaluation for S proceed normally). Abort-that-branch abandons S's branch only — the rest of the build continues unaffected; the build is NOT terminated globally. There is no run-terminating outcome.</note>
        </check>

        <check if="hook returns 'continue' OR hook resolution completes">
          <!-- ── Accumulate end-gate-expanded escalations into Conductor scope ──── -->
          <action>Accumulate end-gate-expanded findings from this story into the Conductor-scoped accumulator:
            For each entry E in S.escalations where E.timing_tier == "end-gate-expanded":
              Append { finding_id: E.finding_id, stakes_class: E.stakes_class, timing_tier: "end-gate-expanded",
                       summary: E.summary, evidence: E.evidence, suggested_fix: E.suggested_fix,
                       story_slug: S.slug }
              to {{end_gate_escalations}}.
            This is the consumer-side aggregation that closes the seam between the per-story
            {{end_gate_escalations}} (reset each story in step 2.S3) and the Conductor-scoped
            {{end_gate_escalations}} that step 5 Source 1 reads to build decision cards.
          </action>

          <!-- ═══════════════════════════════════════════════════════════════════════ -->
          <!-- STEP 2.2.M — PER-STORY INTEGRATION: REBASE → MERGE → CONFLICT PATH    -->
          <!-- Conductor is the sole git-mutation authority for all operations below. -->
          <!-- The directed fixer produces content only; the Conductor commits it.    -->
          <!-- Terminal sprint→main merge is NOT handled here — it belongs in Phase 5 -->
          <!-- and is already gated by the developer-approved end-gate APPROVE seq.   -->
          <!-- ═══════════════════════════════════════════════════════════════════════ -->

          <!-- ── 2.2.M.0 — Initialize per-story attempt counter ──────────────────── -->
          <action>Initialize {{merge_attempts}}[S.slug] = 0 (if absent). This counter tracks the total number
            of rebase-then-merge attempts for story S and is bounded at 3.
          </action>

          <!-- ── 2.2.M.1 — Rebase step (conflict-guarded) ────────────────────────── -->
          <action>2.2.M.1 — REBASE: Increment {{merge_attempts}}[S.slug].
            Rebase the story branch `story/{S.slug}` onto the sprint integration branch `sprint/{{sprint_slug}}`:
              `git rebase sprint/{{sprint_slug}} story/{S.slug}`
            This step is conflict-guarded: any conflict surfacing during the rebase is detected here and enters
            the conflict-classification path (step 2.2.M.3). The Conductor is the sole git writer for this op.
          </action>

          <check if="rebase completes cleanly (no conflicts)">
            <action>Proceed to the merge step (2.2.M.2).</action>
          </check>

          <check if="rebase produces conflicts">
            <action>Leave the rebase in-progress (do NOT abort).
              Bind {{conflict_files}} to the list of conflicted files (from `git diff --name-only --diff-filter=U`).
              Bind {{conflict_op}} to "rebase".
              Proceed to conflict classification (step 2.2.M.3).
            </action>
          </check>

          <!-- ── 2.2.M.2 — Merge step (conflict-guarded) ─────────────────────────── -->
          <action>2.2.M.2 — MERGE: Merge the rebased story branch into the sprint integration branch:
              `git checkout sprint/{{sprint_slug}}`
              `git merge --no-ff story/{S.slug}`
            This step is conflict-guarded: any conflict surfacing during the merge is detected here and enters
            the conflict-classification path (step 2.2.M.3). The Conductor is the sole git writer for this op.
          </action>

          <check if="merge completes cleanly (no conflicts)">
            <action>Proceed to the successful-integration path (step 2.2.M.6).</action>
          </check>

          <check if="merge produces conflicts">
            <action>Leave the merge in-progress (do NOT abort).
              Bind {{conflict_files}} to the list of conflicted files (from `git diff --name-only --diff-filter=U`).
              Bind {{conflict_op}} to "merge".
              Proceed to conflict classification (step 2.2.M.3).
            </action>
          </check>

          <!-- ── 2.2.M.3 — Conflict classification: trivial vs. semantic ──────────── -->
          <note>CONFLICT CLASSIFICATION. A conflict is either trivial (mechanically resolvable) or semantic
            (requires understanding intent). The classification determines whether the Conductor auto-resolves
            or fires a directed fixer. Only the Conductor performs the actual git operations — the fixer
            produces resolution content; the Conductor commits it.

            Trivial conflict (auto-resolve, no human involvement):
              - Non-overlapping hunks — the conflicted regions edit different constructs in the same area
              - Additive-only collisions — both sides add content (imports, entries) with no removal
              - Generated index or lockfile churn the Conductor can reconcile deterministically
                (e.g., package-lock.json, yarn.lock, go.sum, Gemfile.lock)
              In these cases the resolution is deterministic and requires no intent-understanding.

            Semantic conflict (requires directed fixer):
              - Overlapping logic — both sides modify the same function, method, or control-flow construct
              - Contradictory edits to the same named construct (variable, class, schema field, config key)
              - Any case where choosing one side's edit over the other requires knowing the intended behavior
              In these cases the Conductor fires a directed fixer to produce a correct resolution.
          </note>

          <check if="conflict is trivial">
            <action>AUTO-RESOLVE (trivial):
              Apply the deterministic resolution without invoking a fixer. The Conductor resolves the conflict
              directly (non-overlapping hunks: accept both; additive-only: merge both additions; lockfile churn:
              regenerate deterministically).
              Stage the resolved files: `git add &lt;resolved-files&gt;`
              Continue the in-progress operation (the operation was NOT aborted):
                If {{conflict_op}} == "rebase": `git rebase --continue`
                If {{conflict_op}} == "merge":  `git merge --continue` (or `git commit` to finalize)
              If the continue succeeds with no further conflicts:
                If {{conflict_op}} == "rebase": proceed to the merge step (2.2.M.2).
                If {{conflict_op}} == "merge":  proceed to the successful-integration path (2.2.M.6).
              If the continue surfaces another conflict: bind {{conflict_files}} to the new set,
                increment {{merge_attempts}}[S.slug], and return to step 2.2.M.3.
              No human involvement. No escalation. Proceed to step 2.2.M.4 (attempt accounting) only
              when the continue itself fails (i.e., cannot be continued cleanly after resolution).
            </action>
          </check>

          <check if="conflict is semantic">
            <action>SEMANTIC RESOLUTION via directed fixer:
              Spawn a directed fixer subagent (individual-agent, NOT TeamCreate) with:
                - The conflicted file(s) and their conflict markers (the operation is still in-progress)
                - The story's intent (S.title, S.acceptance_criteria from the story spec)
                - The sprint integration branch context
              Constraint passed to fixer: "Produce resolution content only. Do not mutate git."
              The fixer returns resolved file content AND annotates the finding with `stakes_class` and
              `timing_tier` (per directed-fix-finding-schema). Before staging the resolutions, proceed to
              step 2.2.M.4.E (escalation hook). The hook determines whether to escalate or continue.
              Only after the hook returns "continue" does the Conductor:
                1. Write the fixer's resolved content into the conflicted files.
                2. Stage the resolved files: `git add &lt;resolved-files&gt;`
                3. Continue the in-progress operation:
                     If {{conflict_op}} == "rebase": `git rebase --continue`
                     If {{conflict_op}} == "merge":  `git merge --continue` (or `git commit` to finalize)
                4. If the continue succeeds with no further conflicts:
                     If {{conflict_op}} == "rebase": proceed to the merge step (2.2.M.2).
                     If {{conflict_op}} == "merge":  proceed to the successful-integration path (2.2.M.6).
                5. If the continue surfaces another conflict: bind {{conflict_files}} to the new set,
                     increment {{merge_attempts}}[S.slug], and return to step 2.2.M.3.
                6. If the continue itself fails (cannot be completed even after resolution):
                     abort the operation (`git rebase --abort` or `git merge --abort`) and proceed to
                     step 2.2.M.4 (attempt accounting) to decide whether to retry or quarantine.
            </action>
          </check>

          <!-- ── 2.2.M.4 — Attempt accounting and bounded-retry gate ───────────────── -->
          <note>BOUNDED RETRY. This gate is reached ONLY when `--continue` itself fails after a resolution
            attempt (i.e., the operation could not be resumed even after staging the resolved files). Successful
            resolutions — those where `--continue` completes cleanly — route directly to 2.2.M.2 (if the rebase
            leg resolved) or to 2.2.M.6 (if the merge leg resolved) without passing through this gate.

            The abort-and-restart-from-scratch path (entered here) is capped at 3 total attempts per story.
            A story that exhausts the cap is quarantined (step 2.2.M.5) — it is never retried indefinitely.
          </note>

          <action>2.2.M.4 — ABORT the failed operation before retrying from scratch:
            If {{conflict_op}} == "rebase": `git rebase --abort`
            If {{conflict_op}} == "merge":  `git merge --abort`
            Increment {{merge_attempts}}[S.slug].
          </action>

          <check if="{{merge_attempts}}[S.slug] less than 3">
            <action>Retry is allowed. Return to step 2.2.M.1 to retry the full rebase-then-merge sequence
              for story S ({{merge_attempts}}[S.slug] has already been incremented).
            </action>
          </check>

          <check if="{{merge_attempts}}[S.slug] >= 3">
            <action>Retry bound exhausted. Proceed to quarantine (step 2.2.M.5).</action>
          </check>

          <!-- ── 2.2.M.4.E — Escalation hook for semantic resolutions ─────────────── -->
          <action>2.2.M.4.E — ESCALATION HOOK (spec §6, DEC-036 D1). Called from the semantic resolution
            path (step 2.2.M.3) BEFORE the resolution is staged or committed. The merge leg calls the engine;
            the engine decides the bar. The Conductor never classifies stakes or timing itself here.

            Inputs: the fixer-annotated finding with `stakes_class` and `timing_tier`.

            NARROW BAR — must never widen:
              Escalate when the resolution is build-invalidating OR stakes-class-touching
              (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture).
              Routine semantic resolutions (stakes_class == routine AND not build-invalidating) are
              auto-continued silently — no escalation, no pause, no developer involvement.
              The escalation engine (references/escalation.md) determines whether timing_tier qualifies
              for mid-flight pause or end-gate-expanded tagging; the Conductor delegates that decision
              entirely to the engine (step 2.F) and does not re-evaluate it here.

            Execution:

              Step 1: Evaluate the bar.
                If stakes_class == routine AND resolution is NOT build-invalidating:
                  CONTINUE — skip steps 2–4; return to 2.2.M.3 to stage the resolved files and
                  continue the in-progress operation (`git rebase --continue` / `git merge --continue`).
                If stakes_class != routine OR resolution is build-invalidating:
                  Proceed to step 2.

              Step 2: Invoke the escalation engine.
                Pass the fixer-annotated finding to step 2.F (escalation engine).
                Step 2.F evaluates timing_tier and returns one of: pause-branch | continue.

              Step 3: Act on the engine's response.
                If engine returns "continue":
                  Proceed back to step 2.2.M.3 to stage the resolved files and continue the in-progress
                  operation (`git rebase --continue` / `git merge --continue`). On success route per
                  the continue-success rules in 2.2.M.3 (rebase success → 2.2.M.2; merge success → 2.2.M.6).
                  If the continue itself fails, proceed to step 2.2.M.4 (abort-and-bounded-retry gate).
                If engine returns "pause-branch":
                  Surface the mid-flight escalation to the developer (step 2.F manages the pause-ask).
                  While S's branch is paused, other stories in {{running}} continue unaffected.
                  Wait for the developer's resolution choice:
                    - Proceed or Change: stage the resolved files, continue the in-progress operation,
                      and on success route per 2.2.M.3 continue-success rules.
                    - Abort-that-branch: abort the in-progress operation (`git rebase --abort` /
                      `git merge --abort`). Step 2.F has already removed S from {{running}} and added
                      S to {{blocked}} (terminal transition deferred to Phase 5 approve per quarantine
                      convention). Do NOT stage or commit any resolution for S.
                      Fall through directly to frontier re-evaluation (step 2.2's frontier block),
                      bypassing step 2.2.M.4 and 2.2.M.6 entirely for this story.

            TERMINAL SPRINT→MAIN MERGE SCOPE-OUT:
              This hook applies ONLY to per-story merge operations (story/* → sprint/*).
              The terminal sprint→main merge in Phase 5 is inside the developer-gated end-gate APPROVE
              sequence and is NOT a mid-flight trigger. Do not invoke this hook for the terminal merge.

            DISPOSITION: Any finding raised through this hook is recorded with disposition `escalated`
              (distinct from `fixed`, `dismissed`, and `triaged-out`). See step 2.2.M.6.
          </action>

          <!-- ── 2.2.M.5 — Quarantine (after 3 failed attempts) ───────────────────── -->
          <note>QUARANTINE-NOT-HALT. A story that cannot be merged after 3 attempts is quarantined. Quarantine
            means: work is preserved (never discarded), conflict detail is recorded, and the rest of the sprint
            continues. Quarantine is NEVER a HALT. It never pulls the developer in mid-flight. The sprint does
            not stop. The quarantined story is surfaced at the end-gate.
          </note>

          <action>2.2.M.5 — QUARANTINE story S:
            1. Preserve the story branch: `story/{S.slug}` is kept as-is (do NOT delete it).
               The branch remains accessible for post-sprint inspection or manual resolution.
            2. Record conflict detail in {{build_log}}:
               { slug: S.slug, title: S.title, outcome: "quarantined",
                 reason: "conflict unresolved after 3 attempts",
                 conflict_files: {{conflict_files}},
                 merge_attempts: {{merge_attempts}}[S.slug] }
            3. Remove S.slug from {{running}}. Do NOT transition to a terminal story status here —
               the story remains at its current status; the quarantine record in {{build_log}} is the
               durable signal. The end-gate report surfaces the quarantine to the developer.
            4. TERMINATE this story's integration. Do not halt the build phase. Other stories in
               {{running}} and {{frontier}} are entirely unaffected. A quarantined story is NOT treated
               as merged — its slug is NOT added to {{merged}} — so any stories that depend_on S will
               never satisfy the >= review gate for S and will be swept into blocked at build-phase
               completion. Step 2.2.M.6 (successful integration) does NOT apply to a quarantined story;
               jump directly to the frontier re-evaluation block below.
          </action>

          <note>Quarantine records and escalation records ({{escalations}}) are separate collections.
            A quarantined story produces a quarantine entry in {{build_log}}, not an `escalated` disposition.
            The `escalated` disposition is assigned by the fixer (dev fix-mode) per the canonical finding schema;
            the mid-flight pause primitive is owned only by the escalation engine (step 2.F / 2.2.M.4.E).
          </note>

          <!-- ── 2.2.M.6 — Successful integration path ───────────────────────────── -->
          <!-- Reached ONLY via the explicit "Proceed to step 2.2.M.6" from a clean merge (the merge-clean branch at step 2.2.M.2) -->
          <!-- or from a successful retry after conflict resolution. Never reached from quarantine (2.2.M.5). -->
          <action>2.2.M.6 — SUCCESSFUL INTEGRATION (reached after a clean rebase-then-merge, with or without
            prior conflict resolution):

            Worktree and branch cleanup:
              Remove the story worktree: `git worktree remove --force .worktrees/story-{S.slug}`
              Delete the story branch: `git branch -d story/{S.slug}`

            2.2.M.6.1 — Transition story to review after successful merge:
              `momentum-tools sprint status-transition --story {S.slug} --target review`

            2.2.M.6.2 — Record outcome:
              Add S.slug to {{merged}}.
              Remove S.slug from {{running}}.
              Append to {{build_log}}: { slug: S.slug, title: S.title, outcome: "merged",
                findings_summary: S.leftover_findings,
                escalations: (any escalation records produced during this story's merge path) }.
              For any escalations produced during the merge path (step 2.2.M.4.E), append each to
              {{escalations}} with disposition: "escalated".
          </action>

          <!-- Frontier re-evaluation: event-driven, triggered by the merge -->
          <action>Re-evaluate the dependency frontier: for each story T not yet launched and not in {{blocked}}:
            if T.status == "ready-for-dev"
               AND every slug in T.depends_on is in {{merged}} (status >= review):
              add T to {{frontier}}

            Note: the readiness gate is >= review (status on the sprint branch), NOT done.
            A blocker is available to depend on the instant its code is merged, before AVFL or E2E.
          </action>

          <check if="{{frontier}} is non-empty">
            <action>Launch all newly-unblocked stories concurrently (return to step 2.1 for the new frontier batch). No story is deferred because of how many others are running.</action>
          </check>
        </check>
      </check>

      <!-- ── Signal: failed ──────────────────────────────────── -->
      <check if="terminal signal received with outcome == 'failed' for story S">

        <note>Bounded retry: default retry bound is 2 (the pipeline may retry internally; this is the Conductor-level retry on top). On retry, the Conductor re-launches the pipeline for S. On exhausted retries, the Conductor marks S blocked and CONTINUES — it never halts the build phase for a single story's failure. The rest of the frontier and all running pipelines are unaffected.</note>

        <!-- Consumption hook on failed: invoked BEFORE the retry/block decision -->
        <!-- A build-invalidating finding is the class most likely to surface via a failed outcome. -->
        <!-- Without this hook invocation, build-invalidating escalations would bypass mid-flight escalation entirely. -->
        <action>If S.escalations is non-empty: invoke consumption hook (step 2.F) with S.escalations before the retry/block decision.
          The hook's pause-branch vs. continue outcome takes effect here identically to the merged path:
          — "pause-branch": pause this branch and surface the mid-flight escalation to the developer before retrying or marking blocked.
          — "continue": proceed to the retry/block decision below.
          If S.escalations is empty: skip the hook and proceed directly to the retry/block decision.
        </action>

        <action>Increment {{retries}}[S.slug] (initialize to 0 if absent).</action>

        <check if="{{retries}}[S.slug] less than 2">
          <action>Retry: re-launch S's pipeline (return to step 2.1 for S alone).
            Record the retry attempt in {{build_log}}: { slug: S.slug, event: "retry", attempt: {{retries}}[S.slug] }.
          </action>
        </check>

        <check if="{{retries}}[S.slug] >= 2">
          <action>Exhausted retries. Mark S blocked:
            Add S.slug to {{blocked}}.
            Remove S.slug from {{running}}.
            Note: do NOT transition S to a terminal status here — the story remains at its current non-terminal status. The terminal transition (closed-incomplete) is deferred to Phase 5 approve, which performs the single terminal transition for all stranded/blocked stories (quarantine convention, per spec §6/§8). "blocked" is Conductor in-memory state ({{blocked}} array); "blocked" is not a valid state in the tool's state machine.
            Append to {{build_log}}: { slug: S.slug, title: S.title, outcome: "blocked", reason: S.reason, retry_count: {{retries}}[S.slug], stranded: true, note: "terminal status transition deferred to Phase 5 approve" }.
            CONTINUE. Do not halt the build phase. Other stories in {{running}} and {{frontier}} are unaffected.
          </action>
          <note>A blocked story does not propagate to its dependents automatically. Dependents whose depends_on includes S.slug remain in "ready-for-dev" — they can never satisfy the >= review gate for S, so they are never added to the frontier and never launched. At build end, the completion check (below) sweeps all remaining ready-for-dev stories with unsatisfiable depends_on and marks them blocked. The end-of-build sweep is the single mechanism that marks stranded dependents blocked.</note>
        </check>
      </check>

      <!-- ── Build-phase completion check ─────────────────────── -->
      <check if="{{running}} is empty AND {{frontier}} is empty">
        <action>All pipelines have terminated. Build phase heartbeat ends.
          For any remaining stories in {{story_map}} that are still in "ready-for-dev" state with unsatisfiable depends_on:
            Add to {{blocked}}; transition to "closed-incomplete" via `momentum-tools sprint status-transition --story {slug} --target closed-incomplete`; append to {{build_log}} with outcome: "blocked", reason: "dependency never reached >= review".
          For any story in {{story_map}} still in "in-progress" not handled by step 2.0 reconcile:
            Record in {{build_log}} with outcome: "stranded"; defer to spec §6 reconcile-on-start handler.
          Proceed to Phase 3 (AVFL-on-merge).
        </action>
      </check>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.F — Mid-flight escalation consumption hook       -->
    <!-- (DEC-036 D1 — invoked from step 2.2, between terminal   -->
    <!--  signal and the "continue" action)                      -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.F" goal="Mid-flight escalation consumption hook — pause-branch vs. continue, routed through the escalation engine (references/escalation.md)">

      <note>CONSUMPTION HOOK. This step is inserted between a per-story pipeline's terminal signal and the "continue" (merge + frontier re-evaluation) action in step 2.2. Its job is to consume the outcome of the escalation engine — not to detect or classify findings itself. The Conductor defers detection and classification entirely to the escalation engine (behavioral spec: references/escalation.md). The frontier's role: observe the pipeline signal, invoke the engine, act on the engine's outcome (pause-branch or continue).</note>

      <note>Narrow mid-flight bar (DEC-036 D1, must not be widened): the escalation engine fires "pause-branch" ONLY when a finding is BOTH (1) stakes-class (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) AND (2) meets the timing qualifier: irreversible-and-imminent (continuing would make the finding unrecoverable) OR build-invalidating (the finding structurally blocks correct build completion). Nothing else qualifies for mid-flight escalation. Stakes-class findings that do NOT meet the timing qualifier stay on the autonomous path and are held for end-gate-expanded. The mid-flight tier is the exception; end-gate-expanded is the norm and safety net. Do not widen this bar.</note>

      <note>ANTI-FIREHOSE GUARD: Routine findings NEVER enter this hook. Routine findings stay on the always-auto-fix path inside the per-story pipeline. Across a representative build with many routine and non-imminent findings and only a small number of true bar-clearing findings, the number of mid-flight pauses must equal the number of bar-clearing findings and no more. The anti-firehose intent of DEC-035 binding decision #1 is fully preserved: the build flow is not flooded with mid-flight pauses for ordinary work. Everything that does not clear the bar flows to the end-gate-expanded tier.</note>

      <note>SHARED-PRIMITIVE CONTRACT: This engine is the single detection-and-pause primitive for mid-flight escalation. Both the build-phase frontier (step 2.2) and the merge/conflict-resolution leg (step 2.2.M) route mid-flight escalation through this step. Neither leg independently decides the bar or owns its own pause primitive. See references/escalation.md for the authoritative contract.</note>

      <!-- ── Hook entry point ─────────────────────────────────── -->
      <action>Receive S.escalations from the pipeline's terminal signal.
        Invoke the escalation engine (references/escalation.md) with S.escalations.
        The engine evaluates bar: stakes_class in {security-auth-isolation, irreversible-destructive, high-blast-radius-architecture} AND timing_tier == mid-flight.
        (timing_tier == mid-flight encodes that the finding is irreversible-and-imminent or build-invalidating — per the upstream directed-fix-finding-schema ACs 9–10. No separate escalation_reason field is consulted.)
        Engine returns one of:
          { outcome: "continue" }  — no mid-flight bar finding; proceed normally
          { outcome: "pause-branch", finding: {...}, stakes_class, timing_tier }  — bar is met
        The Conductor does not itself inspect or classify S.escalations; it only acts on the engine's returned outcome.
      </action>

      <!-- ── Outcome: continue ─────────────────────────────────── -->
      <check if="engine returns outcome == 'continue'">
        <action>No mid-flight escalation. All S.escalations are either routine (stayed on auto-fix path inside the pipeline) or stakes-class findings that do not meet the mid-flight bar (held for end-gate-expanded). Return "continue" to step 2.2. Record any end-gate-expanded findings in {{build_log}} with timing_tier: "end-gate-expanded" for the end-gate report.</action>
      </check>

      <!-- ── Outcome: pause-branch ─────────────────────────────── -->
      <check if="engine returns outcome == 'pause-branch'">
        <note>This is Touchpoint 3 (narrow exception). The build pauses THIS branch — not the entire build phase. Other stories in {{running}} and newly-unblocked stories in {{frontier}} continue unaffected. Pausing one branch does not halt the rest of the build.</note>

        <!-- PAUSE — Surface to developer (DEC-036 D5 self-sufficiency floor: what / why / evidence inline) -->
        <output>## Mid-flight Escalation — Branch Paused

The build has paused story `{{S.slug}}` for a finding that meets the narrow stakes-and-timing bar (DEC-036 D1). Other stories continue building.

**Paused story:** `{{S.slug}}` — {{S.title}}
**Finding class:** {{stakes_class}}
**Timing tier:** mid-flight (irreversible-and-imminent or build-invalidating)

**What is at stake:**
{{finding.summary}}

**Why this qualifies (evidence):**
{{finding.evidence}}

**Recommended action:** {{finding.suggested_fix}}

**Options:**
- **Proceed** — apply the recommended resolution and resume this branch
- **Change** — alter the planned action (describe what you want instead)
- **Abort-that-branch** — stop this line of work; mark branch as abandoned; build continues for other stories</output>

        <ask>Proceed, Change, or Abort-that-branch?</ask>

        <check if="Proceed">
          <action>Spawn a fix subagent scoped to the finding (individual-agent, not TeamCreate). The subagent produces output only. The Conductor (not the subagent) commits the fix.</action>
          <action>Record outcome in {{build_log}}: { slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", resolution: "fix-applied", finding_summary: {{finding.summary}} }.
            Note: disposition is "escalated" (not "fixed") — this finding was raised mid-flight to the developer; it is stakes-class and was not silently auto-fixed. The "escalated" disposition is distinct from "fixed" (routine auto-fix), "dismissed" (waved off with rationale), and "triaged-out" (outside scope). "resolution: fix-applied" records how the escalated finding was resolved.
          </action>
          <action>Append record to {{escalations}}: { slug: S.slug, stakes_class, timing_tier: "mid-flight", disposition: "escalated", resolution: "fix-applied" }.</action>
          <action>Return "continue" to step 2.2 (the merge and frontier re-evaluation for S proceed). No further mid-flight pause is raised for this resolved finding.</action>
        </check>

        <check if="Change">
          <action>Receive the developer's alternative instruction (what to do differently). Spawn a fix subagent with the developer's alternative instruction (individual-agent, not TeamCreate). The subagent produces output only. The Conductor commits the changed action.</action>
          <action>Record outcome in {{build_log}}: { slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", resolution: "changed-action", developer_instruction: {{developer_instruction}}, finding_summary: {{finding.summary}} }.</action>
          <action>Append record to {{escalations}}: { slug: S.slug, stakes_class, timing_tier: "mid-flight", disposition: "escalated", resolution: "changed-action", developer_instruction: {{developer_instruction}} }.</action>
          <action>Return "continue" to step 2.2 (the merge and frontier re-evaluation for S proceed). No further mid-flight pause is raised for this resolved finding.</action>
        </check>

        <check if="Abort-that-branch">
          <action>Abandon this branch only. Do NOT halt the entire build phase — other stories in {{running}} and {{frontier}} continue unaffected.</action>
          <action>Remove S.slug from {{running}}.
            Note: do NOT transition S to a terminal status here — the story remains at its current non-terminal status. The terminal transition (closed-incomplete) is deferred to Phase 5 approve, which performs the single terminal transition for all stranded/blocked stories (quarantine convention, per spec §6/§8).
            Add S.slug to {{blocked}} so Phase 5 approve can identify it for the closed-incomplete transition.
          </action>
          <action>Record outcome in {{build_log}}: { slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", resolution: "branch-aborted", finding_summary: {{finding.summary}} }.</action>
          <action>Append record to {{escalations}}: { slug: S.slug, stakes_class, timing_tier: "mid-flight", disposition: "escalated", resolution: "branch-aborted" }.</action>
          <note>The build continues for all other stories. The frontier re-evaluation in step 2.2 is NOT triggered for S (the branch is abandoned, not merged). Dependents of S.slug can never satisfy the >= review gate and will be swept into blocked at build-phase completion.</note>
        </check>
      </check>
    </step>

  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 3: AVFL-ON-MERGE                                      -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="3" goal="AVFL-on-merge — run avfl-merge-review Workflow over the precise integrated sprint-vs-main diff">

    <note>AVFL-on-merge runs once after ALL stories are merged to the sprint branch. It uses the avfl-merge-review Workflow (skills/momentum/skills/avfl/workflow-merge-review.md), which inspects the 3-dot merge-base diff of the sprint branch versus main — the net integrated change the developer would actually ship. This phase runs silently; no developer interaction. The workflow returns a typed CLEAN | NON_CONVERGENT result the Conductor consumes directly.</note>

    <!-- ── 3.1 — Assemble inputs for the merge-review Workflow ── -->

    <action>Build the {{merged_stories}} input for the merge-review Workflow:
      For each story slug S in {{merged}} (stories that reached status >= review):
        Resolve the files this story touched from the story spec (the `touches` array in {{story_map}}[S]).
      Bind {{merged_stories}} = array of { slug: S.slug, files_touched: S.touches }
        for each S in {{merged}}.
    </action>

    <action>Build the {{story_contracts}} map for the merge-review Workflow:
      For each story S in {{merged}}:
        Resolve S's contract path from `story_assignments[S.slug].contract.path` in the sprint record.
      Bind {{story_contracts}} = map from slug to contract path
        (used by the fixer for cross-story contradiction resolution — higher-authority contract wins).
    </action>

    <!-- ── 3.2 — Invoke the avfl-merge-review Workflow ─────────── -->

    <note>The avfl-merge-review Workflow owns the 3-dot diff capture, the dual-reviewer parallel fan-out, the declining-skepticism fix loop, and the typed result. The Conductor does NOT spawn momentum:avfl here — it invokes the avfl-merge-review Workflow, which handles its own subagent spawning. The Conductor remains the sole git-mutation authority: the workflow's fixer produces file content and a commit message label; the Conductor commits after each fix iteration.</note>

    <action>Invoke the avfl-merge-review Workflow (skills/momentum/skills/avfl/workflow-merge-review.md) with:
      - sprint_branch: "sprint/{{sprint_slug}}"
      - base_ref: "main"
      - merged_stories: {{merged_stories}}
      - story_contracts: {{story_contracts}}
      Constraint: "Do not ask the developer anything. Do not commit. Return the typed result when done."
      The workflow runs through its validate → consolidate → evaluate → fix loop autonomously.
      For each fix iteration where the workflow's fixer produces corrected file content:
        The Conductor stages and commits the output:
          `git checkout sprint/{{sprint_slug}}`
          `git add -u && git commit -m "fix(avfl): resolve integration findings — iteration {N}"`
        The workflow then re-captures the updated diff and continues its loop.
      Bind {{merge_review_result}} = the typed result object returned by the Workflow.
    </action>

    <!-- ── 3.3 — Consume the typed result ──────────────────────── -->

    <action>Extract findings from the merge-review result to populate {{avfl_findings}}:
      Bind {{avfl_findings}} = array built from {{merge_review_result}} as follows:

      From fixes_applied (findings that were fixed during the review loop):
        For each fix F: emit { source: "avfl-merge-review", finding_id: F.id, severity: F.severity,
          summary: F.change, disposition: "fixed", story_slug: F.owning_stories[0] or "sprint-integration",
          stakes_class: "routine" }

      From leftovers (only present when status == NON_CONVERGENT):
        For each leftover L: emit { source: "avfl-merge-review", finding_id: L.id,
          severity: L.severity, confidence: L.confidence, classification: L.classification,
          summary: L.description, evidence: L.evidence, suggestion: L.suggestion,
          why_unresolved: L.why_unresolved,
          story_slug: L.owning_stories[0] or "sprint-integration",
          location: L.location, owning_stories: L.owning_stories,
          disposition: "residual", stakes_class: "routine",
          type: "integration" }

      Tag all entries: source = "avfl-merge-review".
    </action>

    <!-- ── 3.4 — Route residual leftovers through escalation ─── -->

    <action>Route remaining (non-fixed) AVFL findings through the escalation engine (references/escalation.md):
      For each finding F in {{avfl_findings}} where F.disposition == "residual":
        If F.stakes_class == "routine": hold for end-gate report as routine finding; no escalation check.
        If F.stakes_class is stakes-class (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture):
          Invoke escalation engine with F.
          If engine returns { outcome: "continue" }: tag F with timing_tier: "end-gate-expanded"; hold for end-gate report.
          If engine returns { outcome: "pause-branch" }: invoke step 2.F pause-ask-resume logic for F.
            Note: AVFL runs post-merge; post-merge resolution: Proceed = spawn fixer + commit to sprint branch;
            Change = fixer with alternative + commit; Abort-that-branch does NOT apply (no in-flight story branch
            exists) — open a follow-up backlog story instead.
      ANTI-FIREHOSE: Only findings explicitly flagged irreversible-and-imminent or build-invalidating fire a pause-ask. Non-imminent stakes-class findings go to end-gate-expanded.
    </action>

    <!-- ── 3.5 — Record result and proceed ─────────────────────── -->

    <action>Append AVFL-on-merge results to {{build_log}}:
      { phase: "avfl-on-merge",
        result_status: {{merge_review_result}}.status,
        final_score: {{merge_review_result}}.final_score,
        iterations: {{merge_review_result}}.iterations,
        scores_per_iteration: {{merge_review_result}}.scores_per_iteration,
        fixes_applied_count: length({{merge_review_result}}.fixes_applied),
        leftovers_count: length({{merge_review_result}}.leftovers or []),
        fix_commits: {{merge_review_result}}.commits,
        findings_count: length({{avfl_findings}}),
        stakes_findings_count: count of F in {{avfl_findings}} where F.stakes_class != "routine",
        mid_flight_escalations_count: count of F in {{avfl_findings}} where F.timing_tier == "mid-flight" }
    </action>

    <check if="{{merge_review_result}}.status == 'NON_CONVERGENT'">
      <note>The merge review could not fully converge. Leftovers carry full context (what/where/evidence/suggestion/why_unresolved). These are already in {{avfl_findings}} with disposition="residual" and will appear as decision cards or residual items in the end-gate report. The build is NOT halted — proceed to Phase 4 (E2E) with the known leftovers. The end-gate report surfaces them to the developer for acknowledgment.</note>
      <action>Continue to Phase 4. Do not halt or ask the developer. The NON_CONVERGENT result is surfaced at the end-gate.</action>
    </check>

    <note>No developer ask here on the routine path. The avfl-merge-review Workflow ran over the precise 3-dot integrated diff. AVFL findings are held for the end-gate unless the escalation engine fires a pause-ask for a bar-clearing finding. Proceed to step 3.D.</note>

    <!-- ── 3.D — Coverage-disposition discharge consumer ──────── -->
    <!--
      Discharge all coverage-composition deferrals that were recorded in Phase 2.
      Step 2.C wrote, for each covered-by-composition story S:
        { slug, title, event: "coverage-disposition-deferred",
          covered_by_scenario: <scenario-id>,
          coverage_disposition: "covered-by-composition" }
      This step is the mandatory consumer: it actually runs the named scenario,
      verifies the deferred story's acceptance behavior is observed, and records
      whether the debt is discharged.  A deferral is NEVER silently assumed satisfied.
    -->

    <step n="3.D" goal="Coverage-disposition discharge consumer — run each named integration scenario for deferred stories; record verified-by-composition on pass; surface undischarged deferrals as end-gate leftovers on fail or missing">

      <note>CONSUMER INVARIANT. This step runs after the AVFL merge-review loop (steps 3.1–3.5) because the integration scenario runs on the fully-integrated sprint branch — the same surface AVFL reviewed. The scenario must observe the deferred story's acceptance behavior in the integrated state, not in a per-story worktree. Running before AVFL would mean running against a partially-integrated surface, which would not satisfy the discharge contract.</note>

      <note>SILENT-GAP PREVENTION. A coverage-composition deferral records a DEBT. That debt is discharged only when the named scenario (a) is found, (b) is run, and (c) observes the deferred story's required behavior. If any of these three conditions fails, the debt is NOT silently closed — it is surfaced as an undischarged-coverage-deferral leftover at the end-gate. The developer sees it as an unverified item. Nothing in this step auto-resolves the deferral based on assumption or proximity to passing work.</note>

      <!-- ── 3.D.1 — Collect all deferred records ─────────────── -->

      <action>Collect {{deferred_records}} from {{build_log}}:
        Filter {{build_log}} to all entries where event == "coverage-disposition-deferred".
        Each entry has shape: { slug, title, covered_by_scenario, coverage_disposition }.
        Bind {{deferred_records}} = the filtered list.
      </action>

      <check if="{{deferred_records}} is empty">
        <note>No covered-by-composition deferrals were recorded in this build. Nothing to discharge. This step is a no-op for builds where all stories ran dedicated verification. Proceed to Phase 4.</note>
        <action>Skip 3.D.2 and 3.D.3. Proceed to Phase 4 (E2E).</action>
      </check>

      <!-- ── 3.D.2 — Run each named integration scenario ───────── -->

      <action>For each deferred record R in {{deferred_records}} (process concurrently if multiple):

        Bind {{scenario_id}} = R.covered_by_scenario.

        LOCATE THE SCENARIO:
          Attempt to resolve {{scenario_id}} against the known integration scenario registry for
          this sprint (e.g., contract files under `.momentum/sprints/{{sprint_slug}}/specs/`,
          or any file whose scenario `name` field matches {{scenario_id}}).
          Bind {{scenario_found}} = true if the scenario is located; false otherwise.

        CHECK if {{scenario_found}} == false:
          — The named scenario cannot be located. The deferral CANNOT be discharged.
          — Record in {{build_log}}:
              { slug: R.slug, title: R.title,
                event: "coverage-deferral-undischarged",
                covered_by_scenario: {{scenario_id}},
                outcome: "scenario-not-found",
                note: "Named integration scenario could not be located; deferral remains open." }
          — Append an undischarged-deferral leftover to {{avfl_findings}}:
              { source: "coverage-discharge-consumer",
                finding_id: "undischarged-deferral-{{R.slug}}",
                severity: "major",
                type: "coverage-gap",
                stakes_class: "routine",
                disposition: "residual",
                story_slug: R.slug,
                location: R.slug,
                summary: "Coverage deferral for `{{R.slug}}` is undischarged — named scenario `{{scenario_id}}` not found.",
                detail: "Story `{{R.slug}}` was deferred from build-time QA with the expectation that integration scenario `{{scenario_id}}` would verify its acceptance behavior at AVFL/merge. The scenario cannot be located. The verification debt is unresolved.",
                evidence: "coverage-disposition-deferred record: slug={{R.slug}}, covered_by_scenario={{scenario_id}}; scenario file not found under `.momentum/sprints/{{sprint_slug}}/specs/`.",
                suggestion: "Locate or create the named integration scenario `{{scenario_id}}`, run it against the sprint branch, and confirm it observes `{{R.slug}}`'s required behavior. Alternatively, re-run story `{{R.slug}}` with `coverage_disposition: dedicated-run`." }
          — Skip to the next deferred record. Do NOT proceed to the run step.

        RUN THE SCENARIO (when {{scenario_found}} == true):
          Spawn an integration-scenario executor agent (individual-agent, NOT TeamCreate) with:
            - scenario_id: {{scenario_id}}
            - scenario_path: the resolved path to the scenario file
            - sprint_branch: "sprint/{{sprint_slug}}"
            - deferred_story_slug: R.slug
            - deferred_story_title: R.title
            - story_spec: ".momentum/stories/{{R.slug}}.md"
            - contract_path: the path to R.slug's verification contract (from `story_assignments[R.slug].contract.path` in the sprint record)
          Constraint passed to agent: "Run the named integration scenario against the integrated sprint branch. Verify that the scenario observes the deferred story's required acceptance behavior. Return a structured result: { scenario_id, ran: bool, passed: bool, deferred_story_observed: bool, evidence: string }. Do not mutate git. Do not spawn build agents."
          Bind {{scenario_result}} = the agent's returned result for this record.

        EVALUATE DISCHARGE:
          A deferral is DISCHARGED only when ALL three conditions hold:
            (1) {{scenario_result}}.ran == true          — the scenario was actually executed
            (2) {{scenario_result}}.passed == true       — the scenario passed
            (3) {{scenario_result}}.deferred_story_observed == true  — the deferred story's
                  acceptance behavior was observed by the scenario (not merely that the scenario
                  passed on its own — the scenario must provide positive evidence that it covers
                  R.slug's required behavior)
          If ANY condition is false: the deferral is NOT discharged.
      </action>

      <!-- ── 3.D.3 — Record outcomes ─────────────────────────────── -->

      <action>For each deferred record R and its {{scenario_result}}:

        CASE: all three discharge conditions hold (ran AND passed AND deferred_story_observed):
          — Record discharge in {{build_log}}:
              { slug: R.slug, title: R.title,
                event: "coverage-deferral-discharged",
                covered_by_scenario: {{scenario_id}},
                outcome: "verified-by-composition",
                evidence: {{scenario_result}}.evidence,
                note: "Deferred story's acceptance behavior was observed by the named integration scenario. Verification debt discharged." }
          — Tag the story as verified-by-composition in the Conductor's in-memory state:
              {{coverage_discharge_results}}[R.slug] = { outcome: "verified-by-composition", scenario_id: {{scenario_id}}, evidence: {{scenario_result}}.evidence }
          — No leftover is appended to {{avfl_findings}} for this record.

        CASE: any discharge condition fails (scenario ran but did not pass, OR ran and passed but deferred story's behavior was not observed, OR scenario could not run):
          — Determine the failure mode for evidence:
              If {{scenario_result}}.ran == false: failure_mode = "scenario-did-not-run"
              Else if {{scenario_result}}.passed == false: failure_mode = "scenario-failed"
              Else: failure_mode = "deferred-story-behavior-not-observed"
          — Record in {{build_log}}:
              { slug: R.slug, title: R.title,
                event: "coverage-deferral-undischarged",
                covered_by_scenario: {{scenario_id}},
                outcome: failure_mode,
                evidence: {{scenario_result}}.evidence,
                note: "Deferral is not discharged; see leftover finding in end-gate report." }
          — Append an undischarged-deferral leftover to {{avfl_findings}}:
              { source: "coverage-discharge-consumer",
                finding_id: "undischarged-deferral-{{R.slug}}",
                severity: "major",
                type: "coverage-gap",
                stakes_class: "routine",
                disposition: "residual",
                story_slug: R.slug,
                location: R.slug,
                summary: "Coverage deferral for `{{R.slug}}` is undischarged — {{failure_mode}} for scenario `{{scenario_id}}`.",
                detail: "Story `{{R.slug}}` was deferred from build-time QA. Its named integration scenario `{{scenario_id}}` was expected to observe its acceptance behavior at AVFL/merge. The discharge failed: {{failure_mode}}. The verification debt is unresolved.",
                evidence: {{scenario_result}}.evidence,
                suggestion: "Investigate why scenario `{{scenario_id}}` did not discharge the deferral ({{failure_mode}}). Ensure the scenario explicitly covers story `{{R.slug}}`'s acceptance criteria. Re-run Phase 3 after fixing the scenario, or re-run story `{{R.slug}}` with `coverage_disposition: dedicated-run`." }
      </action>

      <action>Append coverage-discharge summary to {{build_log}}:
        { phase: "avfl-on-merge",
          event: "coverage-discharge-consumer-complete",
          deferred_count: length({{deferred_records}}),
          discharged_count: count of entries in {{coverage_discharge_results}} where outcome == "verified-by-composition",
          undischarged_count: count of entries in {{build_log}} where event == "coverage-deferral-undischarged" }
      </action>

      <note>STAKES-ROUTING NOTE. Undischarged-deferral leftovers are injected into {{avfl_findings}} with stakes_class:"routine" and disposition:"residual". Phase 3 step 3.4 (AVFL residual routing) and Phase 5 (end-gate assembly) will pick them up via the standard residual path — no special-casing needed. If a deferred story's acceptance behavior itself covers a stakes-class concern (e.g., security-auth-isolation), the operator who set coverage_disposition must ensure the integration scenario is stakes-aware. The discharge consumer does not re-classify stakes; it records the discharge outcome as evidence. Stakes routing at the end-gate is driven by the finding schema and report, not by this step.</note>

      <note>Proceed to Phase 4 (E2E).</note>
    </step>

  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 4: END-TO-END (E2E) VALIDATION                        -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="4" goal="E2E validation — end-to-end behavioral check on the integrated sprint branch, with normalization and escalation routing">

    <note>E2E validation runs silently. No developer interaction unless a finding hits the narrow mid-flight escalation bar (irreversible-and-imminent or build-invalidating). All other findings — including non-urgent stakes-class E2E findings — are held for the end-gate as decision cards. The E2E findings follow the SAME normalization and escalation-routing path as build findings. They are not stored only as a raw count.</note>

    <!-- ── 4.1 — Spawn E2E validator ─────────────────────────── -->

    <action>Spawn E2E validator agent (individual-agent, not TeamCreate):
      Resolve agent via: `momentum-tools agent resolve --role e2e-validator`
      Provide: sprint slug, story specs, sprint branch `sprint/{{sprint_slug}}`.
      Constraint passed to agent: "Do not mutate git. Do not spawn build agents. Return validation results only."
    </action>

    <action>Store {{e2e_results}} = structured E2E validation report from agent output.</action>

    <!-- ── 4.2 — Normalize each E2E failure to canonical finding schema ── -->

    <action>NORMALIZE E2E FINDINGS. For each FAIL or ERROR scenario in {{e2e_results}}:

      Extract the following from the e2e-validator's report structure:
        - story_slug: the story key from the scenario's "[story]:[AC]" label; if no story key, use "e2e-integration" as a sentinel slug indicating a sprint-level integration failure not tied to a single story
        - location: "[story]:[AC]" label from the validator output, or "sprint-integration" for sprint-level failures
        - summary: one-sentence plain-English description — use the validator's "Expected: ... Actual: ..." pair as the source material; rephrase as a declarative statement of what is wrong
        - detail: full explanation of what failed, why it matters as an observable consequence (not just a count), and what the expected vs. actual behavior was
        - evidence: the concrete artifact excerpt quoted from the validator output — the command run, the actual output observed, or the error message; NEVER substitute a count ("1 failure") for inline evidence
        - verdict: "FAIL" for behavior-divergence findings; "ERROR" for execution failures
        - severity: derive from the AC's character:
            - If the failed AC is a core user-visible behavior or a build-blocking scenario: "major"
            - If the failure is a non-critical edge case: "minor"
            - If execution cannot proceed at all (ERROR, environment broken): "critical"
            - If the failure is a style or presentation detail: "low"
            Default to "major" when the character is unclear — err toward attention.
        - type: derive from the failure character:
            - Behavior diverges from spec: "spec-compliance"
            - Integration seam between two components is broken: "integration"
            - Required behavior is entirely absent: "completeness"
            - Security or auth-isolation observable failure: "security"
            - Other bug: "bug"
        - stakes_class: apply the stakes-classification rubric (references/stakes-classification-rubric.md):
            - If the failing scenario touches auth, security, or isolation boundaries: "security-auth-isolation"
            - If the scenario validates an irreversible/destructive action (migration, data-delete, force-push, prod-deploy): "irreversible-destructive"
            - If the failure reveals a cross-cutting architectural contract break: "high-blast-radius-architecture"
            - Otherwise: "routine"
        - source: "e2e-validator"
        - ac_id: the AC identifier from the scenario label, or null if not present
        - legitimate: true for all FAIL/ERROR findings from the validator (the validator is the verifier of record for E2E; its FAIL verdict is taken as legitimate)
        - suggested_fix: the validator's suggested remediation if any; null otherwise
        - timing_tier: default "end-gate-expanded"; override to "mid-flight" only if the finding is BOTH stakes-class AND (irreversible-and-imminent OR build-invalidating) — apply the narrow bar from references/stakes-classification-rubric.md

      Produce {{e2e_findings}} = array of normalized finding records in the canonical shape above.
      PASS and SKIP scenarios from the validator do NOT produce findings — they produce no entry in {{e2e_findings}}.
      MANUAL scenarios from the validator produce a finding only if the manual review revealed a failure; otherwise no entry.

      EVIDENCE INVARIANT: Every finding in {{e2e_findings}} must carry non-empty `evidence` quoting inline from the validator's output. A finding with evidence == "" or evidence reduced to a count is malformed and must be rejected before proceeding.
    </action>

    <!-- ── 4.3 — Route E2E findings through the escalation engine ─── -->

    <action>ROUTE E2E FINDINGS. For each finding F in {{e2e_findings}}:

      CASE F.stakes_class == "routine":
        — Routine E2E findings are handled on the transparent auto-fix path (parallel to routine build findings).
        — The Conductor spawns a directed fixer (individual-agent) scoped to F: fix the integration defect.
          The fixer returns a disposition: fixed | dismissed (with non-empty rationale) | triaged-out.
          The Conductor commits any fix applied by the fixer:
            `git checkout sprint/{{sprint_slug}}`
            `git add -u && git commit -m "fix(e2e): auto-fix {F.summary}"`
          Record the disposition in {{e2e_findings}}:
            F.disposition = the fixer's returned value ("fixed" | "dismissed" | "triaged-out").
            If "dismissed": also set F.dismissal_rationale = fixer-returned rationale (non-empty required).
            If "triaged-out": invoke momentum:triage to spin a backlog stub for F (per finding-schema Rule 4 — triaged-out findings are not silently dropped). Record stub slug in F.triage_stub_slug.
          Append to {{build_log}}: { phase: "e2e", event: "e2e-finding-auto-fixed", story_slug: F.story_slug, summary: F.summary, disposition: F.disposition }

      CASE F.stakes_class != "routine" (stakes-class finding):
        — Stakes-class E2E findings are NEVER silently auto-fixed. Route to escalation.
        — Set F.disposition = "escalated".
        — Set F.timing_tier = F.timing_tier (already set in normalization step; default "end-gate-expanded").
        — Route by timing tier:
            IF F.timing_tier == "mid-flight":
              — Finding is irreversible-and-imminent OR build-invalidating.
              — Invoke step 2.F (mid-flight escalation consumption hook) with F as a single-finding escalations array.
              — The engine evaluates the bar and returns "pause-branch" or "continue".
              — Record in {{build_log}}: { phase: "e2e", event: "e2e-mid-flight-escalation", story_slug: F.story_slug, stakes_class: F.stakes_class, summary: F.summary }
            ELSE (timing_tier == "end-gate-expanded" OR not set):
              — Finding is stakes-class but does NOT meet the mid-flight bar. Hold for end-gate.
              — Append to {{end_gate_escalations}}: { finding_id: generated-id, story_slug: F.story_slug, source: "e2e-validator", stakes_class: F.stakes_class, timing_tier: "end-gate-expanded", severity: F.severity, type: F.type, location: F.location, summary: F.summary, detail: F.detail, evidence: F.evidence, suggested_fix: F.suggested_fix, ac_id: F.ac_id, legitimate: true, disposition: "escalated" }
              — Record in {{build_log}}: { phase: "e2e", event: "e2e-stakes-escalation", story_slug: F.story_slug, stakes_class: F.stakes_class, timing_tier: "end-gate-expanded", summary: F.summary }
    </action>

    <!-- ── 4.4 — Build log and phase completion ──────────────────── -->

    <action>Append E2E phase summary to {{build_log}}:
      { phase: "e2e",
        scenarios_checked: (count of all scenarios in validator output),
        passed: (count of PASS scenarios),
        failed: (count of FAIL scenarios),
        blocked: (count of ERROR/BLOCKED scenarios),
        e2e_findings_count: length({{e2e_findings}}),
        routine_auto_fixed: (count of findings where disposition == "fixed"),
        routine_dismissed: (count of findings where disposition == "dismissed"),
        stakes_escalated_end_gate: (count of findings with stakes_class != routine AND timing_tier == "end-gate-expanded"),
        stakes_escalated_mid_flight: (count of findings with stakes_class != routine AND timing_tier == "mid-flight") }
    </action>

    <note>No developer ask here on the routine path. Routine E2E findings are auto-fixed silently. Stakes-class E2E findings with timing_tier == "end-gate-expanded" are held for the end-gate as decision cards. Only timing_tier == "mid-flight" findings trigger the narrow mid-flight pause (step 2.F). Proceed to Phase 5.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 5: SINGLE HUMAN END-GATE                              -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="5" goal="Single human end-gate — the one mandatory developer acceptance point for the sprint build">
    <note>This is Touchpoint 2 — the only mandatory human acceptance gate in the entire build. It is unambiguously last: Phase 5 runs after E2E completes, and no second mandatory acceptance gate follows it. The end-gate report is a self-contained HTML file that organizes findings by user-facing functionality (DEC-035 D6). Stakes-class items appear as expanded decision cards requiring explicit acknowledgment (DEC-036 D4). Dismissed findings appear in a "Waved off" section with rationale (DEC-036 D3). The Approve control is not pre-checked (DEC-036 D4 anti-rubber-stamp). Full rendering spec: references/endgate-report-renderer.md.</note>

    <!-- ── Assemble {{stakes_findings}} from all three escalation sources ── -->

    <action>Assemble {{stakes_findings}} — the full set of escalated decisions requiring human acknowledgment:
      Source 1 — Per-story fix-loop escalations (step 2.S3):
        Collect ALL entries from {{end_gate_escalations}} (written by every story's fix loop, accumulated at Conductor scope in step 2.2).
        Each entry carries: finding_id, stakes_class, timing_tier:"end-gate-expanded", summary, evidence, suggested_fix, story_slug.
      Source 2 — Post-merge AVFL escalations (Phase 3):
        From {{avfl_findings}}: filter to entries where stakes_class != "routine" AND disposition == "residual".
        (AVFL-on-merge leftovers carry disposition "residual" — they never carry "escalated". The directed fixer
        inside the AVFL loop emits "fixed", "dismissed", "triaged-out", or "escalated" per the canonical vocabulary,
        but the Conductor's Phase 3 step 3.3 normalizes unfixed leftovers to disposition "residual" when
        assembling {{avfl_findings}}. No AVFL entry in {{avfl_findings}} carries "escalated".)
        For each, carry: finding_id (or generate one), stakes_class, summary, evidence, suggested_fix (from recommended_action if present), source:"avfl".
      Source 3 — E2E failed/stakes scenarios (Phase 4):
        From the normalized {{e2e_findings}} (Phase 4) and {{e2e_results}}.failed_scenarios: include E2E findings whose stakes_class != "routine" (and any failed scenario whose failure_reason indicates a stakes-class behavioral gap).
        For each, carry: finding_id (the normalized "e2e-{scenario_name}"), stakes_class, summary (the scenario name in plain language), evidence (failure_reason), suggested_fix, source:"e2e-validator".
      Bind {{stakes_findings}} = concat(Source 1, Source 2, Source 3), deduplicated by finding_id (Source 1 already carries E2E stakes findings appended by Phase 4; the dedup prevents double-counting with Source 3).
      If {{stakes_findings}} is empty: the build is clean; the gate can be approved without any decision cards.
    </action>

    <action>Assemble supporting report variables:
      {{routine_auto_fixed_count}} = count of findings with disposition == "fixed" across {{avfl_findings}} and all per-story {{finding_dispositions}} records in {{build_log}}.
      {{dismissed_findings}}       = entries with disposition == "dismissed" (must each carry dismissal_rationale; reject any without one and surface as a Conductor warning in {{build_log}}).
      {{stories_built_count}}      = count of entries in {{merged}}.
      {{blocked_stories}}          = stories never added to {{merged}} (quarantined, integrity-stopped, fix-budget-exhausted, or mid-flight-aborted); derive from {{build_log}} events.
      {{quarantined_stories}}      = subset of {{blocked_stories}} where outcome == "quarantined" in {{build_log}}.
      {{contract_integrity_stops}} = from Conductor in-memory state (step 2.2 integrity-check path).
      {{mid_flight_escalations}}   = escalations already raised to the developer during the build (informational only in the end-gate report).
      {{high_risk_divergences}}    = per-story finding records from {{build_log}} where disposition was initially "fixed" (auto-fixed after review) AND severity in { blocker, critical, major } — these are the consequential divergences that were caught and resolved; they populate §03 of the report.
    </action>

    <!-- ── Build the self-contained HTML end-gate report ── -->

    <action>BUILD THE END-GATE REPORT as a self-contained HTML file at `.momentum/handoffs/{{sprint_slug}}-endgate-report.html`.

      Rendering authority: references/endgate-report-renderer.md (full data contract, CSS tokens, section spec, decision-card markup, gate JavaScript, and voice rules).
      Voice authority: _bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md (the canonical Format & Voice spec).
      Bar: .momentum/handoffs/sprint-2026-06-02-conduct-core-hitl-report.html (the worked example; reproduce its structure and voice, not its sprint-specific content).

      The report MUST contain all eight sections in fixed order:
        HERO    — metrics strip: stories built · high-risk divergences caught · decisions-for-you count · auto-fixed count · waved-off count · blocked/broken count.
        §01     — What shipped: before/after plain terms, concrete new capabilities, one-line completeness caveat linking to §06.
        §02     — What each piece is for: one plain paragraph per story (job + guarantee + what breaks without it); each carries a "Review this work item" expand containing: (1) verification first — what had to be true + how it was checked + honest inspection-vs-execution note + result; (2) architectural rationale with named decision/spec references + files changed; (3) actual diff in a collapsed <pre class="diff">; (4) visual evidence for any UI item (data-URI screenshots, or explicit gap note).
        §03     — Where it diverged: {{high_risk_divergences}} told as 5-beat risk narratives (per renderer §7), scariest-first, collapsible <details class="risk"> cards; routine excluded entirely.
        §04     — The decision(s) for you: one <div class="decision"> card per entry in {{stakes_findings}}; if {{stakes_findings}} is empty, render "No decisions required — this build raised no stakes-class items." No card is blank; each states in plain language: what the decision is about, what is at stake, options with trade-offs, and a recommendation. No option pre-selected. No acknowledge checkbox pre-checked.
        §05     — Waved off & routine: {{dismissed_findings}} as a table (what flagged | why safe to leave); {{routine_auto_fixed_count}} as a single count sentence — NOT itemized.
        §06     — How done is this, really? Two tables: live-vs-hollow. Explicit "what approving actually does" callout. If the sprint is a partial slice, state it plainly.
        §07     — Merge & push preview: commits/diffstat; exact approve sequence; "push is a separate confirmation."
        GATE    — Single control: Approve / Request Changes; copy-decision-as-prompt textarea; approve <button> disabled until every §04 card has been acknowledged AND has a selection (per renderer §6 paint() logic); if {{stakes_findings}} is empty, approve enables after gate choice is made (no forcing function for a clean build).

      Informational-only sections (render if non-empty, no developer action required):
        Mid-flight escalations: {{mid_flight_escalations}} — findings already raised during the build, with their recorded disposition.
        Quarantined stories: {{quarantined_stories}} — branches not merged; preserved; post-sprint follow-up.
        Contract-integrity stops: {{contract_integrity_stops}} — stories not verified due to fingerprint mismatch.

      HTML requirements:
        - Inline <style> and <script> only; zero external dependencies; no CDN links; no remote fonts.
        - CSS tokens per renderer §3 (ivory/slate/clay/olive palette, --fs-scale:1.28 variable).
        - Single --fs-scale CSS variable for global font scaling.
        - All diffs HTML-escaped inside <pre> tags.
        - File must open correctly in a browser with no network access.
    </action>

    <action>Open the report in the cmux Browser viewer pane as a new tab (right pane; does not create a new structural pane):
      Run: cmux browser new "file:///$(pwd)/.momentum/handoffs/{{sprint_slug}}-endgate-report.html" --workspace "$CMUX_WORKSPACE_ID" --focus false
      Verify the surface opens: cmux browser {surface} wait --load-state complete --timeout-ms 15000
    </action>

    <ask>The end-gate report is open in the viewer. Review each section. Acknowledge any decision cards in §04. Then approve to merge to main, or request changes.</ask>

    <check if="developer approves">
      <action>Merge sprint branch to main:
        1. `git checkout main`
        2. `git merge sprint/{{sprint_slug}}`
        3. If conflicts: the Conductor resolves them autonomously or fires a fixer subagent, then retries the merge (per spec §2 and decision #9 — "Conductor resolves conflicts; retry"; conflict-resolution engine delivered by conduct-merge-and-conflict-resolution). Never HALT for developer resolution.
        4. After successful merge: `git branch -d sprint/{{sprint_slug}}`
      </action>
      <action>Transition sprint stories to their correct terminal status (per spec §8):
        For each story in {{sprint_stories}}:
          IF slug is in {{merged}} (story completed-and-validated, work integrated):
            Step 1: `momentum-tools sprint status-transition --story {slug} --target verify`
            Step 2: `momentum-tools sprint status-transition --story {slug} --target done`
            Note: the state machine requires adjacent transitions — review -> verify -> done (two steps). A direct review -> done skip is invalid. Both steps are performed here in sequence before moving to the next story.
          ELSE (story is quarantined, integrity-stopped, or blocked/never-merged — not in {{merged}}):
            `momentum-tools sprint status-transition --story {slug} --target closed-incomplete`
            Note: quarantined stories (never added to {{merged}} per step 2.2.M.5), integrity-stopped stories (removed from {{running}} without a terminal transition), and blocked/aborted stories (retry-exhausted, mid-flight aborted, or stage-3 blocked — all deferred here per the quarantine convention adopted at steps 2.S3, 2.2, and 2.F) all go to closed-incomplete, not done. These stories are at a non-terminal status when they arrive here; this is the single terminal transition for stranded stories. Spinning replacement stubs via momentum:triage for these is handled at build-phase completion (step 2.2 exhausted-retries path); any not yet stubbed should be spun here before push.
      </action>
      <action>MAJOR-RESIDUAL GOVERNANCE GUARD — ensure no MAJOR-severity residual leaves the sprint without a linked backlog stub.
        Sources of residual findings to scan:
          (a) {{avfl_findings}} — AVFL post-merge findings (Phase 3); each has severity and disposition fields (normalized at L1078: fixed | dismissed | escalated | residual).
          (b) {{build_log}} entries with event == "stage3-finding-blocked" — per-story pipeline findings that exhausted the fix retry budget; each carries disposition: "blocked".
          (c) {{e2e_findings}} — E2E findings (Phase 4); each has severity and disposition fields (normalized at Phase 4 step 4.3: fixed | dismissed | triaged-out | escalated). Findings where disposition != "fixed" AND disposition != "dismissed" are residuals.
        Combine all three sources into {{all_build_findings}}.

        Collect {{major_residuals}} = all findings F in {{all_build_findings}} where:
          - F.severity is in {blocker, critical, major}  — the upper severity tier
          - F.disposition is NOT "fixed" AND NOT "dismissed" — finding was not resolved; it is a residual
        Note: "fixed" and "dismissed" findings are fully resolved and need no stub.
        Note: "blocked" findings (step 2.S3 retry-exhausted path) and "escalated" and "residual" AVFL findings all satisfy the NOT-fixed/NOT-dismissed condition and are included.
        Note: "blocked" findings already had a triage stub spun at block time (step 2.S3). momentum:triage's own dedup gate prevents duplicate stubs if the guard re-invokes it for the same finding.

        Initialize {{triage_stubs_created}} = [].

        For each finding F in {{major_residuals}}:
            Invoke momentum:triage with F's descriptive fields (summary, detail, evidence, location, story_slug, severity, stakes_class) to create a backlog stub for this residual finding.
            Append F.finding_id to {{triage_stubs_created}}.
            Append to {{build_log}}: { event: "major-residual-stub-created", finding_id: F.finding_id, severity: F.severity, summary: F.summary, story_slug: F.story_slug }

        Bind {{stubs_created_this_pass}} = count of stubs created in the loop above.
        If {{stubs_created_this_pass}} > 0: surface a note in the push summary output: "{{stubs_created_this_pass}} MAJOR-severity residual(s) from this build now have linked backlog stubs — review via momentum:refine before next sprint."

        INVARIANT: When this action completes, every finding in {{major_residuals}} has a corresponding backlog stub. No MAJOR-severity residual may leave this sprint without one.
      </action>
      <action>Show push summary: `git log @{u}..HEAD --oneline`</action>
      <ask>Push to origin/main?</ask>
      <check if="developer confirms push">
        <action>Run: `git push`</action>
      </check>
      <output>Sprint `{{sprint_slug}}` complete. All stories merged to main.</output>
    </check>

    <check if="developer requests fixes">
      <note>Developer-requested fixes at the end-gate are out of scope for this scaffold story. The end-gate fix flow (spawning targeted fix agents from end-gate findings) is delivered by downstream conduct stories. At this stage: acknowledge the request, record the findings for follow-up, and surface them as backlog candidates.</note>
      <action>For each finding the developer wants fixed: offer to create a follow-up backlog story with title, AC, and source reference.</action>
    </check>
  </step>

</workflow>
