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

    <check if="any story has status 'blocked' with no resolution path OR {{unsatisfied_external_deps}} is non-empty">
      <output>## Conductor — Cannot Start (H4)

**Guard:** H4 — Stalled state detected.

One or more sprint stories are `blocked` with no available resolution path, or have unsatisfiable dependencies outside this sprint. The Conductor cannot proceed from a stalled state.

**Affected stories:** {{stalled_stories}}

**Resolution:** Resolve the blocked stories or drop them from the sprint, then re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <check if="stories/index.json and sprints/index.json disagree on story membership OR any story's status is an unrecognized value OR the sprint branch sprint/{{sprint_slug}} does not exist">
      <output>## Conductor — Cannot Start (H5)

**Guard:** H5 — Inconsistent state detected.

The sprint and story records are inconsistent. This may mean the sprint index and story index disagree on story membership, a story carries an unrecognized status, or the sprint branch `sprint/{{sprint_slug}}` is missing (sprint planning should have created it).

**Details:** {{inconsistency_details}}

**Resolution:** Repair the inconsistency (re-run sprint planning if the branch is missing, or correct the index entries), then re-invoke the Conductor.</output>
      <action>HALT. Do not dispatch any story.</action>
    </check>

    <note>H1–H5 are the only cannot-start guards. All five have now been evaluated. If execution reaches this point, all guards passed. The build will proceed; H1–H5 are NOT re-evaluated once the build starts.</note>

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
    <note>This is the only ask on the routine path before the end-gate. Once confirmed, the build runs silently through Phase 2, Phase 3, and Phase 4. No developer-facing HALT exists outside this Phase 1, except: (a) the Conductor-facing section-7 freeze guard (internal, developer does not see it) and (b) the developer-facing mid-flight escalation tier for irreversible-and-imminent or build-invalidating findings only (Phase 2, step 2.E). Routine findings are never raised mid-build. There is no resume/cleanup prompt, no per-story confirmation, and no other mid-build questions.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 2: BUILD PHASE — PER-STORY PIPELINES                  -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="2" goal="Build phase — run per-story pipelines for all sprint stories in dependency order">
    <note>No story-count cap. No human gate between stories on the routine path. The mid-flight escalation branch (step 2.E) is the single narrow exception — reserved for irreversible-and-imminent or build-invalidating findings only.</note>

    <action>Build dependency graph from {{sprint_waves}} and story-level `depends_on` arrays in {{story_map}}. A story is unblocked when all its blockers reach `done`.</action>

    <action>Initialize {{build_log}} = [] (accumulates per-story pipeline outcomes for the end-gate report).</action>
    <action>Initialize {{pending_merge_list}} = [] (accumulates stories ready to merge to the sprint branch).</action>
    <action>Initialize {{escalation_queue}} = [] (accumulates any mid-flight escalation findings surfaced during the build — processed at step 2.E).</action>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.A — Per-story pipeline (repeated unit)           -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.A" goal="Per-story pipeline — the repeated build unit for each unblocked story">
      <note>This step executes once per story in dependency order. It is the hollow shell for the per-story pipeline internals delivered by downstream stories (dev agent spawn, auto-fix loop, per-story AVFL, code review). Fill the spawn calls and fix loop when those stories land.</note>

      <action>For each unblocked story (status == `ready-for-dev` AND all depends_on blockers are `done`):

        2.A.1 — Transition to in-progress:
          `momentum-tools sprint status-transition --story {slug} --target in-progress`

        2.A.2 — Spawn dev agent (individual-agent, not TeamCreate):
          Resolve agent via: `momentum-tools agent resolve --touches "{{story.touches | join(',')}}"`
          Spawn the resolved agent with the story file at `.momentum/stories/{slug}.md`.
          Constraint passed to agent: "Do not mutate git. Do not spawn build agents. Produce output only."
          [HOLLOW: per-story pipeline internals — dev spawn, auto-fix loop, per-story AVFL, code review — are delivered by downstream conduct stories.]

        2.A.3 — Receive dev agent output. The Conductor (not the agent) commits:
          - Create or check out story branch: `git checkout -b story/{slug}` (or `git checkout story/{slug}`)
          - Stage files: `git add {touched_files}`
          - Commit: `git commit -m "feat({slug}): [story title]"`

        2.A.4 — Auto-fix loop (HOLLOW — downstream story delivers the loop engine):
          [Placeholder: run per-story AVFL + code review, route routine findings to silent auto-fix,
           route stakes-class findings to {{escalation_queue}} or end-gate-expanded per DEC-036 D1/D2.
           The selection logic (which findings qualify for mid-flight escalation) is delivered by the
           stakes-timing escalation mechanism story. Mark stakes-class findings with their disposition:
           fixed | dismissed (non-empty rationale) | triaged-out | escalated.]

        2.A.5 — Mark story merge-ready. Add to {{pending_merge_list}}.
      </action>

      <check if="{{escalation_queue}} is non-empty">
        <action>Before merging this story, evaluate escalation candidates (step 2.E).</action>
      </check>

      <action>For each story in {{pending_merge_list}}:
        - Rebase story branch onto sprint branch: `git rebase sprint/{{sprint_slug}} story/{slug}`
        - If rebase conflicts: the Conductor resolves them autonomously or fires a fixer subagent, then retries the rebase. Never HALT for developer resolution on a routine merge conflict (per spec decision #9; full conflict-resolution engine delivered by conduct-merge-and-conflict-resolution).
        - Merge to sprint branch: `git checkout sprint/{{sprint_slug}}` then `git merge story/{slug}`
        - Transition story to review: `momentum-tools sprint status-transition --story {slug} --target review`
        - Append to {{build_log}}: { slug, title, status: "merged", findings_summary }
        - Clear {{pending_merge_list}} entry.
      </action>

      <action>Re-evaluate dependency graph. If newly unblocked stories exist, loop back to step 2.A for those stories.</action>

      <check if="all sprint stories are in review or done status">
        <action>Build phase complete. Proceed to Phase 3 (AVFL-on-merge).</action>
      </check>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.E — Mid-flight escalation branch (DEC-036 D1)    -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.E" goal="Mid-flight escalation — pause-ask-resume for narrow, stakes-gated findings">
      <note>STRUCTURAL ACKNOWLEDGMENT ONLY. This branch is present as the defined home for the DEC-036 D1 mid-flight escalation tier. The decision logic that determines which findings qualify (irreversible-and-imminent or build-invalidating, with stakes classes: security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) is delivered by the stakes-timing escalation mechanism story. Do not widen the bar here. Routine findings are never routed to this branch.</note>

      <note>Timing bar (DEC-036 D1, narrow): mid-flight escalation applies only when BOTH conditions hold — (1) the finding is stakes-class (security-auth-isolation, irreversible-destructive, or high-blast-radius-architecture) AND (2) the timing qualifies (irreversible-and-imminent: continuing the build would make the finding unrecoverable; OR build-invalidating: the finding structurally blocks correct build completion). Everything else routes to end-gate-expanded (the default tier) or silent auto-fix.</note>

      <check if="{{escalation_queue}} is non-empty AND escalation decision logic is available">
        <!-- PAUSE — Touchpoint 3 (narrow exception): surface escalation findings to developer -->
        <output>## Mid-flight Escalation — Build Paused

The build has paused for a finding that meets the narrow stakes-and-timing bar (DEC-036 D1).

**Paused at:** story `{{current_story_slug}}`
**Finding type:** {{stakes_class}}
**Reason for mid-flight routing:** {{escalation_reason}} (irreversible-and-imminent | build-invalidating)

**Finding detail:**
{{escalation_finding_detail}}

**Options:**
- **Continue** — apply the recommended resolution and resume the build from this point
- **Halt** — stop the build here for deeper investigation
- **Dismiss** — record a rationale and route this finding to end-gate-expanded; resume build</output>

        <ask>Continue, Halt, or Dismiss?</ask>

        <check if="Continue">
          <!-- RESUME: apply resolution, commit via Conductor (not subagent), clear escalation queue, resume build -->
          <action>Spawn a fix subagent scoped to the finding. Receive output. The Conductor commits the fix.</action>
          <action>Clear {{escalation_queue}}. Record outcome in {{build_log}} with disposition: fixed.</action>
          <action>Resume build from the story that triggered the escalation (return to step 2.A loop).</action>
        </check>

        <check if="Halt">
          <action>HALT. Record build state in {{build_log}} with disposition: escalated (build halted). Surface the finding detail for developer investigation.</action>
        </check>

        <check if="Dismiss">
          <action>Record dismissal with developer-provided rationale in {{build_log}}. Disposition: dismissed (rationale required — must be non-empty). Route finding to end-gate-expanded section of the end-gate report.</action>
          <action>Clear {{escalation_queue}}. Resume build from the story that triggered the escalation (return to step 2.A loop).</action>
        </check>
      </check>

      <check if="{{escalation_queue}} is non-empty AND escalation decision logic is NOT yet available">
        <note>Escalation decision engine not yet delivered (downstream story). Route all candidates to end-gate-expanded as a safe fallback. Do not interrupt the build for this reason.</note>
        <action>Move all {{escalation_queue}} entries to end-gate-expanded section of the report. Clear {{escalation_queue}}. Resume build.</action>
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
    <action>Separate {{avfl_findings}} into routine (route to end-gate report) and stakes-class (route to end-gate-expanded or mid-flight escalation per DEC-036 D1/D2 — escalation logic delivered by downstream story).</action>

    <action>Append AVFL results to {{build_log}}: { phase: "avfl-on-merge", findings_count, stakes_findings_count }.</action>
    <note>No developer ask here. AVFL findings are held for the end-gate. Proceed to Phase 4.</note>
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
