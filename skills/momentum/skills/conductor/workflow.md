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
        {{contract_integrity_stops}} = []    — Conductor-facing integrity stops (per story, contract fingerprint mismatch; not stakes-class, not escalations)
        {{build_log}}                = []    — per-story pipeline outcomes for the end-gate report
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

        2.1.3 — Spawn dev agent (individual-agent fan-out, NOT TeamCreate — spawned concurrently with all other frontier pipelines):
          Resolve agent via: `momentum-tools agent resolve --touches "{{S.touches | join(',')}}"`
          Spawn the resolved agent with the story file at `.momentum/stories/{S.slug}.md`.
          Constraint passed to agent: "Do not mutate git. Do not spawn build agents. Produce output only."
          [HOLLOW: per-story pipeline internals — dev spawn, auto-fix loop, per-story quality gate — are specified by downstream conduct stories. Fill the spawn calls and fix loop when those stories land.]

        2.1.4 — CONTRACT-FREEZE GATE (hooked at story launch — earliest sound point):
          Invoke step 2.V for story S. If step 2.V records an integrity stop for S (i.e., appends to {{contract_integrity_stops}}),
          skip all further verification actions for S in this pipeline iteration — do NOT dispatch the verifier for S.
          If step 2.V confirms the contract is unchanged, proceed to verification as normal.

          [PLACEMENT NOTE: The freeze gate fires here, at launch, rather than at a later "verification boundary" inside the
          per-story pipeline. This is intentional and correct: the contract file is frozen at planning and is static between
          launch and verification, so a sha256 check at launch guards the same invariant as one at verification-start. The
          per-story pipeline internals (step 2.1.3 HOLLOW) are owned by downstream conduct stories — when those stories land,
          they MUST NOT add a second freeze check at the per-story verification boundary. The gate belongs here, once, at
          launch. Adding it again inside the per-story pipeline would double-gate and create redundant integrity stops.]

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
             {{escalations}} (which is reserved for stakes-class mid-flight records only, per line 226).
          5. Remove S from {{running}} without transitioning it to "review".
             Mark S in Conductor in-memory state as integrity-stopped (not blocked, not failed).
          6. CONTINUE the build phase. Other stories in {{running}} and {{frontier}} are unaffected.
             The mismatch on one story does not halt the rest of the build.
        </action>

        <note>This is the ONE sanctioned non-developer halt in the verification path. It does not raise a stakes-class escalation. It does not enter the silent auto-fix loop. It is not dismissable with a rationale — there is no disposition to dismiss. It is not a mid-flight escalation eligible for the developer-facing pause (step 2.F). It is the Conductor catching its own integrity violation before it can corrupt a verification result, then continuing the build. The developer sees the mismatch in the end-gate report as an informational note (the integrity-stop entry in {{contract_integrity_stops}}), not as a prompt during the build.</note>
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
                      `git merge --abort`). Step 2.F has already removed S from {{running}} and set the
                      story to closed-incomplete. Do NOT stage or commit any resolution for S.
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
            The `escalated` disposition is produced only by the escalation engine (step 2.F / 2.2.M.4.E).
          </note>

          <!-- ── 2.2.M.6 — Successful integration path ───────────────────────────── -->
          <!-- Reached ONLY via the explicit "Proceed to step 2.2.M.6" from a clean merge (line 440)     -->
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
            `momentum-tools sprint status-transition --story {S.slug} --target closed-incomplete`
            Note: "blocked" is Conductor in-memory state ({{blocked}} array). The durable story status is "closed-incomplete" — "blocked" is not a valid state in the tool's state machine. If the intent is only in-memory tracking and no durable state transition is needed, omit this command; if a durable terminal state is required, "dropped" is the alternative valid choice.
            Append to {{build_log}}: { slug: S.slug, title: S.title, outcome: "blocked", reason: S.reason, retry_count: {{retries}}[S.slug] }.
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
          <action>Remove S.slug from {{running}}. Transition story to closed-incomplete:
            `momentum-tools sprint status-transition --story {S.slug} --target closed-incomplete`
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

  <step n="3" goal="AVFL-on-merge — sprint-level quality scan on the full integrated sprint branch">
    <note>AVFL runs once after ALL stories are merged to the sprint branch. It is a read-only scan at this phase — findings are not fixed here; they are held for the end-gate report. This phase runs silently; no developer interaction unless a finding triggers mid-flight escalation criteria (which are delivered by a downstream story).</note>

    <action>Capture sprint diff: identify files changed by all merged stories (union of all `touches` arrays in {{story_map}}).</action>
    <action>Collect acceptance criteria from all sprint story files. Concatenate as {{all_acs}}.</action>

    <action>Spawn `momentum:avfl` (individual-agent, not TeamCreate) with:
      - task_context: "Sprint {{sprint_slug}} — full codebase after {{sprint_stories | length}} stories merged"
      - output_to_validate: {{sprint_diff}}
      - source_material: {{all_acs}}
      - profile: checkpoint
      - stage: final
      Constraint passed to agent: "Do not mutate git. Do not spawn build agents. Return findings only."
    </action>

    <action>Store {{avfl_findings}} = full findings list from AVFL output, tagged with source="avfl" and severity per finding.</action>

    <action>Route AVFL findings through the escalation engine (references/escalation.md):
      For each finding F in {{avfl_findings}}:
        If F.stakes_class == "routine": add to end-gate report as routine finding; no escalation check.
        If F.stakes_class is stakes-class (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture):
          Invoke escalation engine with F.
          If engine returns { outcome: "continue" }: tag F with timing_tier: "end-gate-expanded"; hold for end-gate report.
          If engine returns { outcome: "pause-branch" }: invoke step 2.F pause-ask-resume logic for F.
            Note: AVFL runs post-merge; mid-flight escalations from AVFL are post-merge pauses. The engine evaluates the bar identically regardless of phase.
            Post-merge resolution outcome differences: Proceed = spawn fixer + commit to sprint branch; Change = fixer with alternative + commit to sprint branch. Abort-that-branch does NOT apply post-merge (no in-flight story branch exists); if the developer rejects the finding, open a follow-up backlog story instead.
      ANTI-FIREHOSE: Only findings explicitly flagged irreversible-and-imminent or build-invalidating by AVFL fire a pause-ask. Non-imminent stakes-class findings go to end-gate-expanded.
    </action>

    <action>Append AVFL results to {{build_log}}: { phase: "avfl-on-merge", findings_count, stakes_findings_count, mid_flight_escalations_count }.</action>
    <note>No general developer ask here. AVFL findings are held for the end-gate unless the escalation engine fires a pause-ask for a bar-clearing finding. Proceed to Phase 4.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 4: END-TO-END (E2E) VALIDATION                        -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="4" goal="E2E validation — end-to-end behavioral check on the integrated sprint branch">
    <note>E2E validation runs silently. No developer interaction unless a finding hits the mid-flight escalation bar (downstream story delivers that logic). Results are held for the end-gate report.</note>

    <action>Spawn E2E validator agent (individual-agent, not TeamCreate):
      Resolve agent via: `momentum-tools agent resolve --role e2e-validator`
      Provide: sprint slug, story specs, sprint branch `sprint/{{sprint_slug}}`.
      Constraint passed to agent: "Do not mutate git. Do not spawn build agents. Return validation results only."
    </action>

    <action>Store {{e2e_results}} = structured E2E validation report from agent output.</action>
    <action>Append E2E results to {{build_log}}: { phase: "e2e", scenarios_checked, passed, failed, blocked }.</action>
    <note>No developer ask here. E2E results are held for the end-gate. Proceed to Phase 5.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 5: SINGLE HUMAN END-GATE                              -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="5" goal="Single human end-gate — the one mandatory developer acceptance point for the sprint build">
    <note>This is Touchpoint 2 — the only mandatory human acceptance gate in the entire build. It is unambiguously last: Phase 5 runs after E2E completes, and no second mandatory acceptance gate follows it. The end-gate report organizes findings by user-facing functionality (DEC-035 D6). Stakes-class items appear as expanded decision cards requiring explicit acknowledgment (DEC-036 D4). Dismissed findings appear in a "Dismissed / not-actioned" section with rationale (DEC-036 D3). The Approve control is not pre-checked (DEC-036 D4 anti-rubber-stamp).</note>

    <action>Compile the end-gate report from {{build_log}}, {{avfl_findings}}, and {{e2e_results}}:
      - Organize by user-facing functionality (not by story or implementation detail)
      - Routine findings section: auto-fixed items (what changed + what was dismissed with rationale)
      - Stakes-class section (if any): expanded decision cards — one per finding — requiring explicit developer acknowledgment before Approve enables
      - Dismissed / not-actioned section: findings the auto-fix loop dismissed, each with rationale
      - Mid-flight escalations section (if any): findings that were escalated during the build, with disposition recorded
      - Quarantined stories section (if any): from {{build_log}} entries where outcome == "quarantined";
        surface as informational — the story branch is preserved and the conflict detail is recorded;
        these are stories that exhausted the 3-attempt merge bound and could not be integrated this sprint;
        no developer action is required during the report itself; quarantined stories are surfaced for
        post-sprint follow-up (create backlog stories or manually resolve the conflict)
      - Contract-integrity-stops section (if any): from {{contract_integrity_stops}} directly (a dedicated collection —
        not filtered from {{escalations}}); surface as informational — no developer action required during the report;
        these are stories that need follow-up because their verification contract fingerprint did not match the
        frozen_sha256 recorded at assignment
      - E2E summary: scenarios passed, failed, blocked
    </action>

    <output>## Conductor End-Gate — Sprint `{{sprint_slug}}`

**Stories built:** {{sprint_stories | length}}
**AVFL findings:** {{avfl_findings_count}} ({{routine_count}} routine, {{stakes_count}} stakes-class)
**E2E:** {{e2e_passed}} passed / {{e2e_failed}} failed / {{e2e_blocked}} blocked

---

### What Changed (by user-facing area)
{{build_summary_by_functionality}}

### Auto-fix Loop — What Was Fixed
{{auto_fixed_summary}}

### Auto-fix Loop — Dismissed / Not-Actioned
{{dismissed_summary}}
<!-- Each dismissed item includes: finding, rationale for dismissal, disposition: dismissed -->

{{#if stakes_findings}}
### Stakes-Class Findings — Requires Explicit Acknowledgment
<!-- These findings were held out of silent auto-fix per DEC-036 D2. Each requires acknowledgment before Approve enables. -->
{{#each stakes_findings}}
**[{{stakes_class}}]** {{file}}: {{description}}
  - Evidence: {{evidence}}
  - Recommended action: {{recommended_action}}
  - Acknowledge: [ ] Yes, I have reviewed this finding
{{/each}}
{{/if}}

{{#if mid_flight_escalations}}
### Mid-flight Escalations During Build
{{#each mid_flight_escalations}}
- Story `{{slug}}`: {{finding_summary}} — Disposition: {{disposition}}
{{/each}}
{{/if}}

{{#if quarantined_stories}}
### Quarantined Stories (Informational)
<!-- These stories exhausted the 3-attempt per-story merge bound and could not be integrated this sprint. Their work is preserved on the story branch. No developer action is required during the build — this section informs you that these stories need post-sprint follow-up. -->
{{#each quarantined_stories}}
- Story `{{slug}}` — {{title}}: could not be merged after {{merge_attempts}} attempts. Conflicted files: {{conflict_files}}. Branch `story/{{slug}}` preserved. Recommend: create a backlog follow-up story or manually resolve the conflict.
{{/each}}
{{/if}}

{{#if contract_integrity_stops}}
### Contract-Integrity Stops (Informational)
<!-- These stories were not verified: the contract file on disk did not match the fingerprint frozen at assignment. No verification result was recorded for them. The contract freeze check (spec §7 step 2) caught the drift before it could corrupt a result. No action required from you during the build — this section informs you that these stories need follow-up. -->
{{#each contract_integrity_stops}}
- Story `{{slug}}`: contract fingerprint mismatch. Contract path: `{{contract_path}}`. Frozen sha256: `{{frozen_sha256}}`. Live sha256: `{{live_sha256}}`. Story was not verified; no verification result recorded.
{{/each}}
{{/if}}

### E2E Validation
{{e2e_results_summary}}

---

**Approve:** [ ] I accept this build and authorize merge to main.
<!-- This control is not pre-checked. If stakes-class findings are present above, acknowledge each before approving. -->
</output>

    <ask>Review the end-gate report. Acknowledge any stakes-class findings. Approve the build to merge to main, or request fixes.</ask>

    <check if="developer approves">
      <action>Merge sprint branch to main:
        1. `git checkout main`
        2. `git merge sprint/{{sprint_slug}}`
        3. If conflicts: the Conductor resolves them autonomously or fires a fixer subagent, then retries the merge (per spec §2 and decision #9 — "Conductor resolves conflicts; retry"; conflict-resolution engine delivered by conduct-merge-and-conflict-resolution). Never HALT for developer resolution.
        4. After successful merge: `git branch -d sprint/{{sprint_slug}}`
      </action>
      <action>Transition all sprint stories to done:
        For each story in {{sprint_stories}}:
          `momentum-tools sprint status-transition --story {slug} --target done`
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
