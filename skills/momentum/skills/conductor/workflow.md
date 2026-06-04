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

  <step n="1" goal="Pre-flight — validate sprint readiness before the build begins">
    <note>This is Touchpoint 1: the only developer interaction before the end-gate on the routine path. Present the sprint plan and confirm the build should begin.</note>

    <action>Read the active sprint record from `.momentum/sprints/index.json` — bind {{sprint_record}} to its `active` block.</action>

    <check if="{{sprint_record}} is null OR {{sprint_record}}.status != 'active'">
      <output>No active sprint found. Run sprint planning and activate a sprint before invoking Conductor.</output>
      <action>HALT.</action>
    </check>

    <action>Bind:
      {{sprint_slug}} = {{sprint_record}}.slug
      {{sprint_stories}} = {{sprint_record}}.stories (array of story slugs)
      {{sprint_waves}} = {{sprint_record}}.waves
    </action>

    <action>For each story slug in {{sprint_stories}}, read its entry from `.momentum/stories/index.json` to collect: title, status, depends_on, touches. Store as {{story_map}}.</action>

    <action>Verify all stories are in `ready-for-dev` status (or already `done` from a prior partial run). Flag any stories in unexpected states.</action>

    <action>Confirm the sprint branch `sprint/{{sprint_slug}}` exists. If it does not exist, HALT — sprint planning should have created it.</action>

    <output>## Conductor — Pre-flight Complete

**Sprint:** `{{sprint_slug}}`
**Stories:** {{sprint_stories | length}} (listed in wave order)
{{#each sprint_stories}}
- `{{slug}}` — {{title}}
{{/each}}

**Phase sequence:** Pre-flight → Build (per-story pipelines) → AVFL-on-merge → E2E → End-gate

The build will proceed silently through all stories. The next human touchpoint is the end-gate after E2E completes, unless a narrow stakes-and-timing escalation surfaces during the build.

Ready to begin?</output>

    <ask>Confirm to start the build.</ask>
    <note>This is the only ask on the routine path before the end-gate. Once confirmed, the build runs silently through Phase 2, Phase 3, and Phase 4.</note>
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
        {{retries}}     = {}    — { slug: int } per-story retry counter
        {{escalations}} = []    — mid-flight escalation records (stakes-class, strict bar only)
        {{build_log}}   = []    — per-story pipeline outcomes for the end-gate report
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

        Store pipeline_handle in {{running}}[S.slug].
      </action>

      <note>After launching the full frontier, the Conductor enters the heartbeat (step 2.2): it waits for terminal signals from running pipelines and reacts to each as it arrives. It does not advance manually — the event drives the next action.</note>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.2 — Heartbeat: react to each terminal signal     -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.2" goal="Heartbeat — react to per-story terminal signals without requiring human input to advance">

      <note>This step is the event-driven loop of the build phase. The Conductor receives terminal signals from running pipelines. Each signal triggers a specific reaction. No human input is needed to advance between stories on the routine path — the loop runs autonomously until the frontier is exhausted and all pipelines have terminated.</note>

      <note>Terminal signals: a per-story pipeline emits exactly one of: { slug, outcome: "merged", leftover_findings: [...], escalations: [...] } OR { slug, outcome: "failed", reason: "...", retry_count: int }. The Conductor reacts to each signal as it arrives from any running pipeline.</note>

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
          <note>After the pause is resolved (developer responds via step 2.F), the hook returns a resolution outcome. Continue with the merge and frontier re-evaluation for S using that resolution.</note>
        </check>

        <check if="hook returns 'continue' OR hook resolution completes">
          <action>Complete the merge for story S:
            2.2.M.1 — Rebase story branch onto sprint branch:
              `git rebase sprint/{{sprint_slug}} story/{S.slug}`
              Conflict → Conductor resolves autonomously or fires a fixer subagent; retry rebase.
              Never HALT for developer resolution on a routine merge conflict.
              (Full conflict-resolution engine delivered by conduct-merge-and-conflict-resolution.)

            2.2.M.2 — Merge to sprint branch:
              `git checkout sprint/{{sprint_slug}}`
              `git merge --no-ff story/{S.slug}`
              Conflict/failure → resolve + retry; persistent failure → mark S blocked (see 'failed' signal).

            2.2.M.3 — Transition story to review:
              `momentum-tools sprint status-transition --story {S.slug} --target review`

            2.2.M.4 — Remove worktree and branch (per-story cleanup):
              `git worktree remove --force .worktrees/story-{S.slug}`
              `git branch -d story/{S.slug}`

            2.2.M.5 — Record outcome:
              Add S.slug to {{merged}}.
              Remove S.slug from {{running}}.
              Append to {{build_log}}: { slug: S.slug, title: S.title, outcome: "merged", findings_summary: S.leftover_findings }.
              Append any escalation records from the hook to {{escalations}}.
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
            `momentum-tools sprint status-transition --story {S.slug} --target blocked` (or nearest available state).
            Append to {{build_log}}: { slug: S.slug, title: S.title, outcome: "blocked", reason: S.reason, retry_count: {{retries}}[S.slug] }.
            CONTINUE. Do not halt the build phase. Other stories in {{running}} and {{frontier}} are unaffected.
          </action>
          <note>A blocked story does not propagate to its dependents automatically — dependents whose depends_on includes S.slug can never satisfy the >= review gate for S. They will also be marked blocked when the frontier finds them unsatisfiable at build end.</note>
        </check>
      </check>

      <!-- ── Build-phase completion check ─────────────────────── -->
      <check if="{{running}} is empty AND {{frontier}} is empty">
        <action>All pipelines have terminated. Build phase heartbeat ends.
          For any remaining stories in {{story_map}} that are still in "ready-for-dev" state with unsatisfiable depends_on:
            Mark them blocked; append to {{build_log}} with outcome: "blocked", reason: "dependency never reached >= review".
          Proceed to Phase 3 (AVFL-on-merge).
        </action>
      </check>
    </step>

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.F — Mid-flight escalation consumption hook       -->
    <!-- (DEC-036 D1 — invoked from step 2.2, between terminal   -->
    <!--  signal and the "continue" action)                      -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.F" goal="Mid-flight escalation consumption hook — pause-branch vs. continue, deferred to the escalation mechanism">

      <note>CONSUMPTION HOOK. This step is inserted between a per-story pipeline's terminal signal and the "continue" (merge + frontier re-evaluation) action in step 2.2. Its job is to consume the outcome of the escalation mechanism — not to detect or classify findings itself. The Conductor defers detection and classification entirely to the escalation mechanism (delivered by the stakes-timing escalation mechanism story). The frontier's role is: observe the pipeline signal, invoke the mechanism, and act on the mechanism's outcome (pause-branch or continue).</note>

      <note>Narrow mid-flight bar (DEC-036 D1, must not be widened): the escalation mechanism may signal "pause-branch" ONLY when a finding is BOTH (1) stakes-class (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) AND (2) meets the timing qualifier (irreversible-and-imminent: continuing would make the finding unrecoverable; OR build-invalidating: the finding structurally blocks correct build completion). Nothing else qualifies for mid-flight escalation. Stakes-class findings that do NOT meet the timing qualifier are NOT routed here — they are held for end-gate-expanded. The mid-flight tier is the exception; end-gate-expanded is the norm and safety net. Do not widen this bar.</note>

      <note>Routine findings (the default class) NEVER enter this hook. Routine findings stay on the always-auto-fix path inside the per-story pipeline. The hook is not invoked for them, and no mid-flight pause occurs. The anti-firehose intent of DEC-035 is fully preserved: the build flow is not flooded with mid-flight pauses for ordinary work.</note>

      <!-- ── Hook entry point ─────────────────────────────────── -->
      <action>Receive S.escalations from the pipeline's terminal signal.
        Invoke the escalation mechanism with S.escalations.
        The mechanism returns one of:
          { outcome: "continue" }  — no mid-flight bar finding; proceed normally
          { outcome: "pause-branch", finding: {...}, stakes_class, escalation_reason }  — bar is met
        The Conductor does not itself inspect or classify S.escalations; it only acts on the mechanism's returned outcome.
      </action>

      <!-- ── Outcome: continue ─────────────────────────────────── -->
      <check if="mechanism returns outcome == 'continue'">
        <action>No mid-flight escalation. All S.escalations are either routine (stayed on auto-fix path inside the pipeline) or stakes-class findings that do not meet the mid-flight bar (held for end-gate-expanded). Return "continue" to step 2.2. Record any end-gate-expanded findings in {{build_log}} for the end-gate report.</action>
      </check>

      <!-- ── Outcome: pause-branch ─────────────────────────────── -->
      <check if="mechanism returns outcome == 'pause-branch'">
        <note>This is Touchpoint 3 (narrow exception). The build pauses THIS branch — not the entire build phase. Other stories in {{running}} and newly-unblocked stories in {{frontier}} continue unaffected. Pausing one branch does not halt the rest of the build.</note>

        <!-- PAUSE — Surface to developer -->
        <output>## Mid-flight Escalation — Branch Paused

The build has paused story `{{S.slug}}` for a finding that meets the narrow stakes-and-timing bar (DEC-036 D1). Other stories continue building.

**Paused story:** `{{S.slug}}` — {{S.title}}
**Finding class:** {{stakes_class}}
**Mid-flight qualifier:** {{escalation_reason}} (irreversible-and-imminent | build-invalidating)

**Finding detail:**
{{finding.summary}}

Evidence: {{finding.evidence}}
Recommended action: {{finding.suggested_fix}}

**Options:**
- **Continue** — apply the recommended resolution and resume this branch
- **Halt** — stop the entire build here for deeper investigation
- **Dismiss** — record a rationale; route to end-gate-expanded; resume this branch</output>

        <ask>Continue, Halt, or Dismiss this finding?</ask>

        <check if="Continue">
          <action>Spawn a fix subagent scoped to the finding (individual-agent, not TeamCreate). The subagent produces output only. The Conductor (not the subagent) commits the fix.</action>
          <action>Record outcome in {{build_log}}: { slug: S.slug, event: "mid-flight-escalation", disposition: "fixed", finding_summary: {{finding.summary}} }.</action>
          <action>Append record to {{escalations}}: { slug: S.slug, stakes_class, escalation_reason, disposition: "fixed" }.</action>
          <action>Return "continue" to step 2.2 (the merge and frontier re-evaluation for S proceed).</action>
        </check>

        <check if="Halt">
          <action>Record outcome in {{build_log}}: { slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", finding_summary: {{finding.summary}}, build_state: "halted" }.</action>
          <action>HALT. Surface the finding detail and build state for developer investigation. The build does not proceed.</action>
        </check>

        <check if="Dismiss">
          <action>Require non-empty developer-provided rationale. An empty or missing rationale is invalid — re-ask until rationale is provided.</action>
          <action>Record outcome in {{build_log}}: { slug: S.slug, event: "mid-flight-escalation", disposition: "dismissed", rationale: {{developer_rationale}}, finding_summary: {{finding.summary}} }.</action>
          <action>Append record to {{escalations}}: { slug: S.slug, stakes_class, escalation_reason, disposition: "dismissed", rationale: {{developer_rationale}} }. Route finding to end-gate-expanded section of the end-gate report.</action>
          <action>Return "continue" to step 2.2 (the merge and frontier re-evaluation for S proceed).</action>
        </check>
      </check>

      <!-- ── Fallback: mechanism not yet delivered ────────────── -->
      <check if="escalation mechanism is NOT yet delivered">
        <note>The stakes-timing escalation mechanism (delivered by a downstream story) is not yet available. Safe fallback: route all entries in S.escalations to end-gate-expanded. Do not interrupt the build. Return "continue" to step 2.2.</note>
        <action>For each entry in S.escalations: add to {{build_log}} with timing_tier: "end-gate-expanded" and note: "mechanism not yet delivered — routed to end-gate as fallback".</action>
        <action>Return "continue" to step 2.2.</action>
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
