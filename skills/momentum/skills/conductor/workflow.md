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

    <note>Reconcile end condition: all story branches and worktrees belonging to `in-progress` stories from prior sessions are removed; all stories that were `in-progress` are reset to `ready-for-dev`; `git worktree list` shows only the main worktree, the sprint branch worktree (if applicable), and any leftover entries for non-`in-progress` stories; the sprint branch exists and is clean. Stories that were not `in-progress` (e.g., `ready-for-dev`, `blocked`) may still have leftover branches or worktree directories from other circumstances — these are handled by the launch-time idempotent collision handling in step 2.1 STAGE-1 when those stories are dispatched. The build begins from this known-good state.</note>

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

    <critical>LEDGER-APPEND STANDING RULE (applies to every {{build_log}} append in Phases 2–5): Every instruction that appends a row to {{build_log}} ALSO appends the same row to the build ledger at {{ledger_path}} — per references/build-ledger.md. The append is a single-line Bash printf: `printf '%s\n' '&lt;row-json&gt;' >> {{ledger_path}}`. The row carries an `event` field from the controlled event-type set (references/build-ledger.md), a `story_slug` field (real story slug; exceptions enumerated in the reference), and a `ts` field (ISO 8601 timestamp). Terminal rows use `event: "story-terminal"` with `outcome` as a payload field. KEY VOCABULARY: all rows use `story_slug:` as the canonical join key (per finding-schema.md). Do NOT use `slug:` as a key name in any new or updated {{build_log}} or ledger row — `story_slug:` is the single, uniform field name for identifying a story. This standing rule eliminates the need to repeat "AND append to the ledger" at each of the ~30 build_log sites — every build_log append is implicitly also a ledger append. The ledger is the durable copy; the in-context {{build_log}} is the volatile write-through cache. REHYDRATION EXEMPTION: the rehydration replay loop in step 2.0 (which reads ledger rows and appends them back into {{build_log}}) is a REBUILD operation only — these replay appends do NOT trigger a second ledger append. The standing rule applies to new live-event appends only, not to rows being replayed from the ledger during resume. Failure to honor this exemption doubles the ledger on every resume.</critical>

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
        {{contract_integrity_stops}} = []    — Conductor-facing integrity stops (per story, contract fingerprint mismatch; not stakes-class, not escalations)
        {{build_log}}                = []    — per-story pipeline outcomes for the end-gate report
        {{conductor_reverted_fixes}} = []    — findings whose fix commit was reverted by scope discipline (write-scope guard in stage-3 or stage-1); each entry: { finding_id, story_slug, summary, reverted_files: [], reroute_stub_slug: null }. Consumed at end-gate scorecard assembly to exclude from {{routine_auto_fixed_count}}.
        {{coverage_discharge_results}} = {}  — { slug: { outcome, scenario_id, evidence } } — populated by Phase 3 step 3.D; outcome is "verified-by-composition" for discharged deferrals. Consumed at the build_log discharge summary (~step 3.5); NOT consumed at the end-gate scorecard.
      </action>

      <!-- ── BUILD LEDGER: init + rehydration ──────────────────── -->

      <action>Bind {{ledger_path}} = ".momentum/sprints/{{sprint_slug}}/build-ledger.jsonl".
        The build ledger is the durable, append-only record of every state-bearing event in this build.
        Behavioral spec: references/build-ledger.md (event-type set, row shape, append-only rules, enum vocabulary by reference).
        The ledger file is created on first append (no pre-creation step). All appends use:
          `printf '%s\n' '&lt;row-json&gt;' >> {{ledger_path}}`
      </action>

      <check if="file exists at {{ledger_path}} (a prior session wrote events for this sprint)">
        <note>REHYDRATION. A build ledger from a prior session exists. Replay its rows to rebuild all Conductor-scoped accumulators before the status-based {{merged}} seed and in-progress reconcile run. This ensures findings, dispositions, escalations, quarantine records, integrity stops, reverted fixes, coverage deferrals/discharges, and build-log events from a prior session are recovered — not just the story membership that the status-based seed provides.</note>

        <action>Read all lines from {{ledger_path}}. Parse each line as a JSON object. For each row R, rebuild accumulators:

          Event-type routing (keyed on R.event):

            "story-launched", "stage-transition", "stage3-simplify-pass",
            "coverage-disposition-deferred", "coverage-disposition-default", "coverage-disposition-incomplete",
            "coverage-deferral-undischarged", "coverage-discharge-consumer-complete",
            "avfl-on-merge-complete", "avfl-finding",
            "e2e-finding-auto-fixed", "e2e-mid-flight-escalation",
            "e2e-stakes-escalation", "e2e-phase-complete",
            "endgate-change-request-parsed",
            "endgate-change-workflow-pass", "endgate-change-escalated", "endgate-fix-budget-exhausted",
            "endgate-report-re-rendered", "major-residual-stub-created",
            "conductor-warning":
              → Append R to {{build_log}}.

            "finding-disposition":
              → Append R to {{build_log}}.
              → This is the durable store that closes the phantom store defect.
                Per-story {{finding_dispositions}} transients no longer need to survive across stories —
                the ledger is the authoritative source at Phase 5 assembly.

            "stage3-escalation":
              → Append R to {{build_log}}.
              → If R.timing_tier == "end-gate-expanded": append { finding_id: R.finding_id, stakes_class: R.stakes_class,
                  timing_tier: "end-gate-expanded", summary: R.finding_summary, story_slug: R.story_slug }
                  to {{end_gate_escalations}}.

            "stage3-mid-flight-escalation", "mid-flight-escalation":
              → Append R to {{build_log}}.
              → Append { story_slug: R.story_slug, stakes_class: R.stakes_class, timing_tier: "mid-flight",
                  disposition: "escalated", resolution: R.resolution,
                  finding_count: R.finding_count } to {{escalations}}.

            "stage3-fix-scope-reverted":
              → Append R to {{build_log}}.
              → Append { finding_id: R.finding_id, story_slug: R.story_slug, summary: R.finding_summary,
                  reverted_files: R.reverted_files, reroute_stub_slug: R.reroute_stub_slug } to {{conductor_reverted_fixes}}.
              Note: R.reroute_stub_slug is set by the inline triage call at stage-3 time and is recorded
              in the ledger row; rehydration recovers the stub link from the durable row rather than
              hardcoding null, so the end-gate link between a reverted fix and its backlog stub survives resume.

            "stage3-finding-blocked":
              → Append R to {{build_log}}.

            "stage3-story-blocked":
              → Append R to {{build_log}}.
              → If R.story_slug is not in {{blocked}}: add R.story_slug to {{blocked}}.

            "contract-integrity-stop":
              → Append R to {{build_log}}.
              → Append { story_slug: R.story_slug, contract_path: R.contract_path,
                  frozen_sha256: R.frozen_sha256, live_sha256: R.live_sha256 } to {{contract_integrity_stops}}.

            "story-terminal":
              → Append R to {{build_log}}.
              → If R.outcome == "merged": add R.story_slug to {{merged}} (if not already present).
              → If R.outcome in {"blocked", "quarantined", "stranded", "contract-integrity-stop"}: add R.story_slug to {{blocked}} (if not already present).
              → If R.outcome == "quarantined": note the quarantine record for end-gate report.
              → If R.merge_attempts is present (quarantine rows carry it): set {{merge_attempts}}[R.story_slug] = R.merge_attempts.

            "retry":
              → Append R to {{build_log}}.
              → Set {{retries}}[R.story_slug] = max(existing value or 0, R.attempt) — rebuilds per-story retry counter.

            "scorecard-revert-reconciliation":
              → Append R to {{build_log}}.

            "coverage-deferral-discharged":
              → Append R to {{build_log}}.
              → Also populate {{coverage_discharge_results}}[R.story_slug] = { outcome: "verified-by-composition",
                  scenario_id: R.covered_by_scenario, evidence: R.evidence }.

          Track seen events: build a set of (story_slug, event, finding_id) tuples from all rows.
          Bind {{ledger_seen_events}} = this set, used for duplicate-prevention on resume.

          PHASE CHECKPOINT RULE (resume): After rehydrating, check which phases have already produced
          their phase-completion summary rows in the ledger, and skip those phases if their completion
          event is present:
            — If a row with event == "avfl-on-merge-complete" exists: skip Phase 3 (AVFL-on-merge) on resume.
            — If a row with event == "e2e-phase-complete" exists: skip Phase 4 (E2E) on resume.
          For step 3.D counts: scope the deferred/discharged/undischarged counts to rows with
          ts >= the latest "avfl-on-merge-complete" row's ts (i.e., from the current consumer run
          only) when re-running; if "coverage-discharge-consumer-complete" exists from a prior run,
          skip step 3.D entirely on resume.
          This prevents AVFL and E2E from re-executing wholesale after an interrupt, which would
          append duplicate summary rows and inflate Phase 5 counts.
        </action>

        <note>After rehydration: in-context accumulators ({{build_log}}, {{escalations}}, {{end_gate_escalations}}, {{contract_integrity_stops}}, {{conductor_reverted_fixes}}, {{coverage_discharge_results}}, {{merged}}, {{blocked}}, {{retries}}, {{merge_attempts}}) are populated from the durable ledger. The status-based {{merged}} seed below cross-checks and supplements this — the ledger provides the richer record (findings, dispositions, escalations, retry counts) while story statuses provide the authoritative membership check.</note>
      </check>

      <check if="file does NOT exist at {{ledger_path}}">
        <note>Fresh build — no prior ledger. Initialize {{ledger_seen_events}} = empty set. All accumulators start empty (their defaults from the init block above). The ledger file will be created on the first append.</note>
        <action>Bind {{ledger_seen_events}} = {} (empty set).</action>
      </check>

      <note>DUPLICATE-PREVENTION USE OF {{ledger_seen_events}}: Before appending a `finding-disposition` or `stage3-escalation` row to the ledger during a live build, check whether the tuple (story_slug, event, finding_id) is already in {{ledger_seen_events}}. If it is, skip the append — the event was already recorded in a prior session for a story that is not being re-run. Add each newly appended tuple to {{ledger_seen_events}} so the check is current throughout the build. This prevents duplicate rows for the same finding when a story's events survive from a prior session into the current session's ledger. The per-story re-run convention (step 2.0 reconcile resets in-progress stories) determines which stories produce new events; events for stories NOT re-run must not be re-appended even if they enter the event-processing path again.</note>

      <action>Seed {{merged}} from current story statuses to support partial-run resume:
        For each story S in {{story_map}}:
          if S.status is "review" OR S.status is "done":
            add S.slug to {{merged}}
        This ensures dependents of already-merged blockers can satisfy the >= review gate on resume.
        Note: on a fresh run {{merged}} starts empty (no stories yet at review/done), which is correct.
      </action>

      <action>Reconcile in-progress stories from a crashed or aborted prior partial run:
        For each story S in {{story_map}} where S.status == "in-progress":
          Option A (clean worktree): if S's worktree is clean or abandonable AND S.slug is NOT in {{blocked}}, reset S's status to "ready-for-dev"
            via `momentum-tools sprint status-transition --story {S.slug} --target ready-for-dev --force`
            (--force is required: in-progress -> ready-for-dev is a backward transition; intentional for crash-recovery)
            and admit S to the frontier on the pass below.
            If S.slug IS in {{blocked}} (rehydrated from a prior session): do NOT reset or re-launch S — it was already blocked; leave it blocked and defer to Phase 5 approve.
          Option B (dirty worktree): if no prior "story-terminal" row for S.slug already exists in
            the ledger (check {{ledger_seen_events}} — skip if (S.slug, "story-terminal", null) is present),
            record in {{build_log}} (and the build ledger per standing rule):
            { event: "story-terminal", story_slug: S.slug, outcome: "stranded",
              reason: "in-progress on resume — worktree not clean",
              note: "dependency on spec §6 reconcile-on-start (owned by conduct-merge-and-conflict-resolution)",
              ts: NOW() }.
            If a prior stranded row already exists for S.slug, skip the re-append — it was recorded in the prior session.
            Do NOT add S to {{frontier}}; it must be handled by the reconcile-on-start handler.
        Note: stories at in-progress from a prior run must not be silently abandoned — they need
        an explicit reconcile decision, not a silent fall-through.
      </action>

      <action>Compute initial frontier: for each story S in {{story_map}}:
        if S.status == "ready-for-dev"
           AND S.slug is NOT in {{blocked}}
           AND every slug in S.depends_on is in {{merged}} (status >= review):
          add S to {{frontier}}

        Note: stories with empty depends_on are launch-ready immediately.
        Note: independent stories all enter the frontier at t=0.
        Note: the {{blocked}} guard is required on resume — a story rehydrated into {{blocked}} from
        a prior session must not be re-launched even if its status is still "ready-for-dev" (status
        transitions for blocked stories are deferred to Phase 5 approve per the quarantine convention).
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

        2.1.2a — LEDGER: story launch event (state-bearing — not currently in {{build_log}}):
          Append to {{build_log}} AND the build ledger at {{ledger_path}} per the standing rule:
            { event: "story-launched", story_slug: S.slug, title: S.title, ts: NOW() }

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
          Act on the routing outcome as specified in step 2.C. Do NOT dispatch the dedicated QA
          verification run (REVIEWER A / qa-reviewer) at build time for a story whose
          coverage_disposition is "covered-by-composition". Stage-2's adversarial code review
          (REVIEWER B / momentum:code-reviewer) is unaffected by the coverage disposition and
          still runs on the per-story diff at build time.

        2.1.3 — STAGE-1 → STAGE-2 → STAGE-3 PIPELINE: Fire asynchronously after 2.1.4/2.1.5 resolve,
          and ONLY IF S is NOT in {{contract_integrity_stops}}. An integrity-stopped story skips 2.1.3
          entirely — no branch, no worktree, no dev spawn, no pipeline stages are executed for it.
          Each story's pipeline runs independently and concurrently with other stories' pipelines.
          The pipeline emits a single terminal signal when complete; step 2.2 consumes that signal.
          The launch loop does NOT block on any stage — all per-story pipelines run concurrently.

          ── STAGE-1: DEV SPAWN ──────────────────────────────────────────────────────────────

          CREATE STORY BRANCH AND WORKTREE (Conductor-executed, before dev spawn, Conductor-serial):
            Placement: deliberately first action of STAGE-1, after 2.1.4/2.1.5 gates resolve and only
            when S is NOT in {{contract_integrity_stops}}, so a gate-stopped story never acquires an
            orphan worktree. This placement is intentional and must not be moved later in the pipeline.

            Rationale: forking from the sprint tip keeps the merge-base diff exactly story-scoped
            (references/per-story-review-diff-range.md Scenario A — pre-merge review isolates only
            the story's own commits when the branch diverged from sprint/{{sprint_slug}}).

            CWD anchor: all relative paths below resolve from repo root. The Conductor normalizes
            CWD via `git rev-parse --show-toplevel` before executing any git mutations in this block.

            Note on concurrency: the Conductor performs branch and worktree creation for each story
            serially (one story at a time) to prevent `.git` lock contention. Concurrency applies to
            the dev agents that run afterward — not to the Conductor's git mutations.

            Idempotent collision handling (same removal ordering as the RECONCILE ON START
            action in Phase 1 — worktree first, then branch — extended with prune and an
            unregistered-path fallback):
              1. `git worktree prune` — clear any stale worktree registrations first.
              2. Check `git worktree list` for any entry whose path matches `.worktrees/story-{S.slug}`.
                 If found: `git worktree remove --force --force .worktrees/story-{S.slug}`
                 If remove fails (e.g., unregistered path): `rm -rf .worktrees/story-{S.slug}` then
                 `git worktree prune` again.
              3. Check whether branch `story/{S.slug}` exists. Before deleting, check `git worktree list`
                 for any entry currently on `story/{S.slug}` and force-remove that worktree first.
                 Then: `git branch -D story/{S.slug}`

            Create branch and worktree:
              `git branch story/{S.slug} sprint/{{sprint_slug}}`
              `git worktree add .worktrees/story-{S.slug} story/{S.slug}`

            The branch base is explicit — `sprint/{{sprint_slug}}` — never main, never an unspecified
            default. The sprint branch is verified to exist by the H5 guard and reconcile (Phase 1);
            this action does not re-verify.

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
              append { event: "conductor-warning", story_slug: S.slug, reason: "staged file outside writable_files — unstaged: " + P, ts: NOW() } to {{build_log}} and the build ledger, then UNSTAGE P (`git -C .worktrees/story-{S.slug} restore --staged P`)
              before committing. Do NOT commit out-of-scope edits.
          The Conductor (sole git-mutation authority) commits the produced output:
            `git -C .worktrees/story-{S.slug} add -u`
            (apply write-scope guard above before proceeding)
            `git -C .worktrees/story-{S.slug} commit -m "feat({S.slug}): implement {{S.title}}"`

          CROSS-ARTIFACT ROUTING: If {{stage1_cross_artifact_notes}} is non-empty, accumulate each
            entry into {{build_cross_artifact_notes}} with the story slug attached:
              { story_slug: S.slug, artifact: entry.artifact, note: entry.note }
            These are deferred — do NOT invoke momentum:triage inline here. The full batch is
            routed to momentum:triage at build-phase completion (step 2.2 / Phase 2 wrap-up),
            mirroring the triaged-out path for fix-mode findings.

          Then advance this story's pipeline to stage-2.
          LEDGER: stage transition event (state-bearing — not currently in {{build_log}}):
            Append per standing rule: { event: "stage-transition", story_slug: S.slug, from_stage: "stage-1", to_stage: "stage-2", ts: NOW() }

          ── STAGE-2: CODE REVIEW + CONDITIONAL QA FAN-OUT ──────────────────────────────────
          Stage 2 fires AFTER the stage-1 commit, BEFORE the merge at step 2.2.M (pre-merge review).

          DIFF RANGE (Scenario A — Pre-Merge Review, per references/per-story-review-diff-range.md):
          Compute the per-story diff at review time — do NOT capture a SHA; do NOT wait for the merge:
            {{story_diff}} = output of:
              `git -C .worktrees/story-{S.slug} diff \
                $(git -C .worktrees/story-{S.slug} \
                  merge-base sprint/{{sprint_slug}} story/{{S.slug}}) \
                ..story/{{S.slug}}`
          Pass the materialized diff (not the range expression) to reviewers.
          DO NOT use over-scoped ranges (main...HEAD) or two-dot sprint-tip forms.
          Authoritative pattern and rationale: references/per-story-review-diff-range.md.
          [NOTE: {{story_diff}} is always computed, regardless of coverage disposition. Both
          dedicated-run and covered-by-composition stories need the per-story diff for code review.]

          Apply coverage routing established at 2.1.5 to determine reviewer dispatch:

            ── FALLBACK: unbound or unrecognized disposition ──
            If {{coverage_disposition}}[S.slug] is null, missing, or does not match either recognized
            value ("dedicated-run" or "covered-by-composition"), treat as "dedicated-run" (safe default).
            This mirrors the safe-default rule in step 2.C: never skip or defer verification when the
            disposition is absent or unrecognized.

            ── dedicated-run (default) ──
            If {{coverage_disposition}}[S.slug] == "dedicated-run":
            Spawn the following two agents CONCURRENTLY (individual-agent fan-out, NOT TeamCreate):

              REVIEWER A — qa-reviewer agent:
                Inputs:
                  - story_slug: S.slug
                  - worktree_path: `.worktrees/story-{S.slug}`
                  - verification_contract: `.momentum/sprints/{{sprint_slug}}/specs/{S.slug}.*`
                  - story_diff: {{story_diff}}
                Constraint: "Read-only. Do not modify code. Do not mutate git. Produce findings only."
                Returns: the producer-format QA Review Report — per-AC classification
                  (VERIFIED / PARTIAL / MISSING / BLOCKED) with stakes_class on each finding.
                  This is the agent's native output shape, NOT the canonical finding schema.
                  The Conductor normalizes it to the canonical schema in the stage-2
                  normalization action below (before the {{qa_findings}} binding).

              REVIEWER B — momentum:code-reviewer skill (bmad-code-review adapter):
                Inputs:
                  - story_slug: S.slug
                  - story_diff: {{story_diff}}
                  - worktree_path: `.worktrees/story-{S.slug}`
                  - review_depth: S.review_depth if set in the story spec (see DEEPER-REVIEW OPT-IN above);
                      omit this field (or pass null) when the story spec does not set it, which triggers
                      standard-depth review. Passing "deep" triggers the higher-rigor pass.
                Constraint: "Report-only mode. Do not modify code. Do not mutate git. Produce findings only."
                Returns: normalized finding records per canonical finding schema (finding-schema.md),
                  stakes_class populated on every record. Source field: `bmad-code-review`.

            When BOTH reviewers have returned:

            REVIEWER A RETURN VALIDATION: Before normalization, confirm that REVIEWER A
            returned a parseable QA Review Report containing a recognizable `### Findings`
            section (or an explicit `(none)` marker). If REVIEWER A's return is absent,
            is an error string, or is prose that cannot be parsed as a QA Review Report
            (i.e. there is no `## QA Review Report` header and no `### Findings` section),
            treat this as a REVIEWER A failure — invoke the pipeline-retry path for
            REVIEWER A exactly as if REVIEWER A had returned an explicit `failed` signal.
            Do NOT fall through to the Empty case; an unparseable return is a reviewer
            failure, not a clean zero-findings report.

            ── NORMALIZE REVIEWER A (qa-reviewer) → CANONICAL FINDING SCHEMA ──────────────
            Authoritative predicate: a finding is any entry in the `### Findings` section
            of the QA Review Report whose Verdict is `PARTIAL`, `MISSING`, or `BLOCKED`.
            These two selection criteria are equivalent and must agree — a `### Findings`
            entry whose Verdict is not one of those three values is malformed (reviewer
            failure), and a finding with Verdict PARTIAL/MISSING/BLOCKED that does not
            appear in `### Findings` is also malformed. If the table's non-VERIFIED rows
            and the `### Findings` section diverge (different set of findings), treat the
            report as malformed and invoke the REVIEWER A failure path rather than
            silently producing a partial result. Entries with Verdict VERIFIED carry no
            finding and are not normalized.

            For each finding in the qa-reviewer report's `### Findings` section, emit one
            canonical record with every base field populated:

            - `story_slug` — S.slug from the per-story pipeline context
            - `source` — `"qa-reviewer"`
            - `verdict` — the producer finding's per-AC classification string
                (`PARTIAL` | `MISSING` | `BLOCKED`)
            - `severity` — derived from verdict only (never consults stakes_class):
                `BLOCKED` → `critical`; `MISSING` → `major`; `PARTIAL` → `minor`
            - `stakes_class` — carry through from the producer finding unchanged
                (the agent is the stakes producer per its rubric)
            - `type` — `security` if `stakes_class == security-auth-isolation`,
                else `spec-compliance` (qa-reviewer findings are AC-verification findings)
            - `location` — carry through from the producer finding's Location field;
                `"unspecified"` if absent
            - `summary` — carry through from the producer finding's Summary field;
                `""` (empty string) if absent
            - `detail` — carry through from the producer finding's Detail field;
                `""` (empty string) if absent
            - `evidence` — carry through from the producer finding's Evidence field;
                `""` (empty string) if absent (BLOCKED findings definitionally may carry
                no evidence — this is not a data error)
            - `ac_id` — carry through from the producer finding's AC field;
                `null` if absent
            - `legitimate` — `true` (qa-reviewer is the verifier of record; it emits
                only findings it judges genuine)
            - `suggested_fix` — `null` (the qa-reviewer producer format has no explicit
                fix field; Detail describes expected state, not remediation steps)

            BLOCKED routing note: a finding with `verdict: BLOCKED` and `severity: critical`
            reflects that test execution was prevented (missing infrastructure, unreachable
            service, absent harness) — it is an environment condition, not a code defect.
            The fixer cannot resolve environment gaps; if a BLOCKED finding exhausts the
            fix budget without resolution, the blocked-then-continue path applies
            (budget-exhausted → mark BLOCKED, spin triage stub, story remains unmerged).
            This routing note does not alter the AC-mandated severity mapping
            (BLOCKED → critical stays).

            Empty case: when the qa-reviewer report contains zero findings (all ACs
            VERIFIED), the normalization produces an empty array. No error, no fabricated
            records.

            Disposition and timing fields (`disposition`, `dismissal_rationale`,
            `timing_tier`) are fixer-assigned — the normalization does NOT set them.
            ──────────────────────────────────────────────────────────────────────────────────

            Bind {{qa_findings}} = the normalized canonical records produced by the
              normalization action above (not REVIEWER A's raw producer-format report).
            Bind {{cr_findings}} = findings array from REVIEWER B.
            Merge into {{stage2_findings}}: deduplicated union of {{qa_findings}} and {{cr_findings}},
              severity-sorted (critical → major → minor → low).
            Deduplication: if a qa-reviewer finding and a bmad-code-review finding describe the same
              location and issue, keep the higher-severity record; annotate source as
              "qa-reviewer+bmad-code-review".

            ── covered-by-composition ──
            If {{coverage_disposition}}[S.slug] == "covered-by-composition":
            Spawn REVIEWER B ONLY as an individual agent (fan-out, NOT TeamCreate):

              REVIEWER B — momentum:code-reviewer skill (bmad-code-review adapter):
                Dispatch with Inputs, Constraint, and Returns IDENTICAL to the REVIEWER B block in the
                dedicated-run branch above — that block is the single canonical REVIEWER B specification
                (story_slug, story_diff: {{story_diff}}, worktree_path, review_depth per DEEPER-REVIEW
                OPT-IN; report-only constraint; returns normalized finding-schema.md records with
                stakes_class populated on every record, source field `bmad-code-review`).

            REVIEWER A (qa-reviewer) is NOT dispatched — the dedicated QA verification run is deferred
            to the named integration scenario at AVFL/merge (per step 2.C Path B). This is not a code
            review — it is a QA verification run, and its deferral is the sole effect of the
            covered-by-composition disposition.

            REVIEWER B FAILURE HANDLING: If REVIEWER B errors, fails to return, or returns
            output that does not conform to the canonical finding schema (finding-schema.md), treat
            this as a stage-2 failure — do NOT bind [] and do NOT silently advance to stage-3.
            Re-dispatch REVIEWER B once (single retry). If the retry also fails, emit the pipeline
            failed terminal signal for story S: { slug: S.slug, outcome: "failed",
            reason: "stage-2 REVIEWER B non-return or schema-invalid output after retry" }.
            Do NOT ask the developer. Do NOT bind [] as a fallback.

            When REVIEWER B has returned (with valid schema-conforming output):
            Bind {{cr_findings}} = findings array from REVIEWER B.
            Bind {{stage2_findings}} = {{cr_findings}}, severity-sorted (critical → major → minor → low).
            [NOTE: No merge/dedup is needed — only one reviewer produced findings. The dedup rule
            applies only to the dedicated-run path where both reviewers return findings.]

          Each finding in {{stage2_findings}} carries the canonical base fields of finding-schema.md,
            including: story_slug, source, stakes_class, severity, verdict, type, location, summary,
            detail, evidence, legitimate, ac_id (where applicable), and suggested_fix (when provided).
          Then advance this story's pipeline to stage-3.
          LEDGER: stage transition event (state-bearing — not currently in {{build_log}}):
            Append per standing rule: { event: "stage-transition", story_slug: S.slug, from_stage: "stage-2", to_stage: "stage-3", ts: NOW() }

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
          3. Record the integrity stop in {{build_log}} (and the build ledger per standing rule):
             { event: "contract-integrity-stop", story_slug: S.slug, title: S.title,
               reason: "contract fingerprint mismatch — live sha256 does not equal frozen_sha256",
               contract_path: {{contract_path}},
               frozen_sha256: {{frozen_sha256}},
               live_sha256: {{live_sha256}},
               ts: NOW() }
          4. Record an entry in {{contract_integrity_stops}} that identifies story S as integrity-stopped,
             so the end-gate report can surface it to the developer as an informational item:
             { story_slug: S.slug, contract_path: {{contract_path}}, frozen_sha256: {{frozen_sha256}}, live_sha256: {{live_sha256}} }
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
    <!-- DEEPER-REVIEW OPT-IN (review_depth:deep)                -->
    <!-- Names the requesting party and triggering signal.        -->
    <!-- ─────────────────────────────────────────────────────── -->

    <!--
      REVIEW DEPTH GOVERNANCE:

      Standard depth (default): REVIEWER B (momentum:code-reviewer) runs at its default
      rigor level on every story in every build. No explicit parameter is required.

      Deeper review (review_depth:deep): a higher-rigor code-review pass. It is dispatched
      as REVIEWER B with the additional input `review_depth: "deep"` passed to the skill.

      REQUESTING PARTY: The developer is the ONLY party permitted to request review_depth:deep.
      The Conductor never upgrades to deep review on its own authority.

      TRIGGERING SIGNAL: The developer sets `review_depth: "deep"` in the story's spec file
      (`.momentum/stories/{slug}.md`) under the story's build-options block (or equivalent
      top-level field). When the Conductor reads the story spec at launch (step 2.1 STAGE-1),
      it checks for this field and passes it to REVIEWER B if present.

      ROUTINE PATH: On a routine build the developer does not set this field. REVIEWER B
      runs at standard depth. The deeper-review opt-in is NOT triggered automatically and
      does NOT insert any mid-run developer question. It is a planning-time decision by
      the developer, recorded in the story spec before the build starts.

      BEHAVIORAL INVARIANT: review_depth:deep never reopens a human question on the
      routine build path. Setting it is a planning action (pre-flight), not a mid-run
      escalation.
    -->

    <!-- ─────────────────────────────────────────────────────── -->
    <!-- STEP 2.S3 — Stage-3 fix loop (Phase B–D, per story)     -->
    <!-- Invoked after stage-2 returns findings for story S.     -->
    <!-- Governs: spec §3 Phase B–D + §4.                        -->
    <!-- ─────────────────────────────────────────────────────── -->

    <step n="2.S3" goal="Stage-3 per-story fix loop — directed fixer with retry-bound-3, escalation routing (DEC-036 D1/D2)">

      <note>INVOCATION CONTEXT. Step 2.S3 runs after stage-2 has returned findings for story S (from the QA reviewer + code-review adapter on the dedicated-run path, or from the code-review adapter only on the covered-by-composition path). It is the Phase B→C→D loop per spec §3 and §4: apply fixes via the directed fixer, run /simplify (every story, once per iteration, after Phase B), re-check, and repeat — bounded at 3 attempts per finding. The Conductor invokes this step with the stage-2 findings list for story S. The Conductor remains the sole git-mutation authority; the directed fixer (subagent) produces output only and never commits itself.

      Stage-2 callers and Phase D re-check callers must derive the per-story diff using the canonical pre-merge merge-base pattern (Scenario A). Canonical pattern: references/per-story-review-diff-range.md.</note>

      <note>ROUTINE-PATH GUARANTEE (DEC-035 D1, always-on default). Routine findings (stakes_class == routine) are ALWAYS auto-fixed inside this loop with no human gate. The always-auto-fix behavior for routine findings is UNCHANGED and PRESERVED. This is the anti-firehose baseline: the vast majority of findings complete Phase B→D autonomously without any escalation or human contact.</note>

      <note>ESCALATION-PATH GUARD (DEC-036 D2 amendment). A stakes-class finding (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) is NEVER silently auto-fixed inside this loop. Such a finding is immediately routed to the escalation channel (end-gate-expanded tier by default; mid-flight tier only on the narrow irreversible-and-imminent OR build-invalidating bar). This is the stage-3 leg of the three-place absolute — the guard must be honored here even though the other two legs (schema comment, dev executor) are threaded by their own stories.</note>

      <note>ISOLATION INVARIANT. An escalated finding for one item does NOT stop routine findings on other items from completing their normal fix → re-check → bound-3 cycle. The escalation path is non-destructive to the routine path. Within a single story's findings list, escalated findings exit the retry loop; routine findings continue their fix/re-check cycle to completion regardless.</note>

      <!-- ── CANONICAL RETRY BOUNDS (declared once; all per-loop mentions defer to these) ───── -->
      <!--                                                                                        -->
      <!-- FIX-LOOP BOUND ({{MAX_FIX_ATTEMPTS}}): governs Phase B→D iterations per finding.      -->
      <!--   Canonical value: 3. Every Phase D check that tests {{fix_attempts}} against a        -->
      <!--   numeric limit MUST reference {{MAX_FIX_ATTEMPTS}}, not a hardcoded literal.          -->
      <!--   If the retry budget is ever changed, it is changed here and only here.               -->
      <!--                                                                                        -->
      <!-- MERGE-ATTEMPT BOUND: governs rebase-then-merge attempts per story.                    -->
      <!--   Canonical value: 3. Declared at step 2.0 init ({{merge_attempts}} bound: 3)          -->
      <!--   and enforced in step 2.2.M.4. Each mention in 2.2.M refers to that step 2.0         -->
      <!--   declaration; no merge-attempt mention may state a different number.                  -->
      <!--                                                                                        -->
      <!-- PIPELINE-RETRY BOUND: governs Conductor-level story-pipeline retries on failure.      -->
      <!--   Canonical value: 2. Declared at the step 2.2 failed-signal handler note             -->
      <!--   ("default retry bound is 2"); all checks in that handler defer to that statement.   -->
      <!--   Pipeline retries are a distinct loop from the fix-loop and merge-attempt loop.       -->
      <!--   The three loops are separate; each has its own canonical bound declared once.        -->

      <!-- ── Entry: bind findings, initialize per-finding retry state ─── -->

      <action>Bind {{MAX_FIX_ATTEMPTS}} = 3 — the canonical fix-loop bound for this step. Every Phase D check
        that tests {{fix_attempts}} against a retry limit uses {{MAX_FIX_ATTEMPTS}}. Declared once here;
        never hardcoded elsewhere in 2.S3.
        Bind {{stage2_findings}} = findings array from stage-2 for story S (qa-reviewer + bmad-code-review output on the
        dedicated-run path; bmad-code-review output only on the covered-by-composition path),
        deduplicated where applicable and severity-sorted (highest severity first).
        Bind {{fix_attempts}} = {} — per-finding retry counter keyed by finding ID.
        Bind {{finding_dispositions}} = [] — per-finding outcome records (fixed | dismissed | triaged-out | escalated | blocked | scope-reverted).
          [NOTE: "blocked" and "scope-reverted" are Conductor-internal-only values. They are NOT in the canonical four-value disposition set (fixed | dismissed | triaged-out | escalated) defined by finding-schema.md.
            "blocked" — used when retry budget is exhausted; treated as escalated for schema consumers.
            "scope-reverted" — used when the write-scope guard fully discards a fix (stage-3 SCOPE-REVERT PATH case a or case b with insufficient in-scope portion). The scope-reverted disposition has its own inline reroute path (momentum:triage called immediately, not deferred) and MUST NOT be picked up by the build-phase-completion deferred triaged-out router, which would create a duplicate stub. For schema consumers, scope-reverted maps to triaged-out.]
        Bind {{story_end_gate_escalations}} = [] — per-story accumulator for escalated findings routed to end-gate-expanded tier within this story's pipeline. Reset at the start of each story. Emitted in the pipeline signal payload; consumed by step 2.2's accumulation action which appends entries into the Conductor-scoped {{end_gate_escalations}} accumulator.
          [WIRED: {{story_end_gate_escalations}} is written here, emitted in the pipeline signal payload, and consumed by step 2.2 to populate the Conductor-scoped {{end_gate_escalations}}. Step 5 reads {{end_gate_escalations}} (Conductor-scoped) to build decision cards. Each entry must carry: finding_id, stakes_class, summary, evidence, suggested_fix. These fields populate the decision cards. See references/endgate-report-renderer.md for the full data contract and rendering spec.]
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
        RESET per-finding locals: {{fix_reverted_files}} = [] — must be cleared at the top of each iteration so a prior finding's discarded paths cannot bleed into the current finding's scope-revert check.

        CASE disposition == "fixed":
          — Stakes-class guard: VERIFY that F.stakes_class == "routine". If the fixer returns "fixed" for a stakes-class finding (non-routine), treat it as an implementation error — do NOT commit the fix. Append { event: "conductor-warning", story_slug: S.slug, reason: "fixer returned 'fixed' for stakes-class finding " + F.finding_id + " — re-classifying as escalated", ts: NOW() } to {{build_log}} and the build ledger; then re-classify F as escalated (see escalated path below).
            When re-classifying: look up the inbound finding for F.finding_id in {{stage2_findings}} to recover stakes_class, summary, evidence, and suggested_fix (the fixer's "fixed" disposition object does not carry these fields). Default timing_tier to "end-gate-expanded" (the conservative default per finding-schema.md) since the fixer never sets timing_tier on a "fixed" disposition.
          — WRITE-SCOPE COMMIT GUARD (fix loop): Before staging the fix, run `git -C .worktrees/story-{S.slug} diff --name-only` to enumerate the files the fixer modified. For each modified file P: if P is NOT in {{writable_files}} for story S, it is out of scope. UNSTAGE and DISCARD the out-of-scope edit (`git -C .worktrees/story-{S.slug} checkout -- P`) before committing. Collect the discarded paths into {{fix_reverted_files}}.
            SCOPE-REVERT PATH (fires when {{fix_reverted_files}} is non-empty after discarding):
              a. If ALL files the fixer modified were out of scope (the fix produced ONLY out-of-scope edits — nothing was committed), the fix was entirely reverted:
                 — Do NOT commit. The finding's "fixed" disposition is INVALID — the fix never landed.
                 — Look up the inbound finding I for F.finding_id in {{stage2_findings}} to recover summary, detail, location, suggested_fix, severity, stakes_class (mirroring the triaged-out and escalated cases at lines 575/580; these descriptive fields are needed for the triage stub below).
                 — Re-classify F: change disposition from "fixed" to "scope-reverted" in {{finding_dispositions}}.
                   [NOTE: "scope-reverted" is Conductor-internal (parallel to "blocked" at line 521). It is NOT in the canonical four-value set (fixed | dismissed | triaged-out | escalated). Before any schema consumer sees this record it maps to "triaged-out". Using a distinct value prevents the build-phase-completion deferred-triage router (CASE disposition == "triaged-out") from picking up this record a second time and creating a duplicate stub — the inline reroute below is the sole routing owner for scope-reverted findings.]
                 — LEDGER (phantom-store closure): append per standing rule: { event: "finding-disposition", story_slug: S.slug, finding_id: F.id, disposition: "scope-reverted", summary: I.summary, severity: I.severity, ts: NOW() }
                 — Append to {{conductor_reverted_fixes}}: { finding_id: F.id, story_slug: S.slug, summary: I.summary, reverted_files: {{fix_reverted_files}}, reroute_stub_slug: null }.
                 — RE-ROUTE for follow-up (defect must not be silently dropped): invoke momentum:triage with the inbound finding I's descriptive fields (finding_id: F.id, summary: I.summary, detail: I.detail, location: I.location, suggested_fix: I.suggested_fix, story_slug: S.slug, severity: I.severity, stakes_class: I.stakes_class) to create a backlog stub so the defect remains on record. This triage call is inline because the scope-reverted disposition does NOT enter the deferred-triage router. Bind the returned stub slug into {{reroute_stub_slug}}.
                 — Bind {{conductor_reverted_fixes}}[last].reroute_stub_slug = {{reroute_stub_slug}}.
                 — Log in {{build_log}} (and the build ledger per standing rule): { story_slug: S.slug, event: "stage3-fix-scope-reverted", finding_id: F.id, finding_summary: I.summary, reverted_files: {{fix_reverted_files}}, reroute_stub_slug: {{reroute_stub_slug}}, note: "fix entirely discarded by write-scope guard — disposition reclassified from fixed to scope-reverted; defect re-routed inline for follow-up" }.
                 Note: reroute_stub_slug is now recorded in the ledger row so that rehydration at step 2.0 recovers the stub link from the durable event rather than defaulting to null.
                 — Do NOT pass F to the fixer again in the next iteration — the defect is out-of-scope for this story's deliverables and will be addressed through the stub.
              b. If ONLY SOME files were out of scope (the fix contained both in-scope and out-of-scope edits), the partial fix is committed without the out-of-scope files. The finding remains disposition "fixed" only if the in-scope portion of the fix is sufficient to address the finding. If the in-scope portion alone does not address the finding (the core fix was in the discarded file), apply the same full-revert path above (re-classify to "scope-reverted", append to {{conductor_reverted_fixes}}, re-route inline). If the in-scope portion is sufficient: commit and record disposition "fixed" normally; log the partial discard in {{build_log}} as a warning.
          — Commit the applied fix (in-scope edits only, after the guard above):
              `git -C .worktrees/story-{S.slug} add -u && git -C .worktrees/story-{S.slug} commit -m "fix({S.slug}): auto-fix {F.summary}"`
          — Record F in {{finding_dispositions}}: { finding_id: F.id, disposition: "fixed", summary: F.summary, stakes_class: "routine" }
            (Only reached when the write-scope guard did NOT reclassify F — i.e., the fix landed in-scope and is valid.)
          — LEDGER (phantom-store closure): append per standing rule: { event: "finding-disposition", story_slug: S.slug, finding_id: F.id, disposition: "fixed", summary: F.summary, stakes_class: "routine", severity: I.severity, ts: NOW() }
            Note: I.severity is recovered from the inbound finding I for F.finding_id in {{stage2_findings}} — the same lookup used above to validate stakes_class.

        CASE disposition == "dismissed":
          — Validate non-empty rationale: if F.dismissal_rationale is empty or missing, treat as invalid — log error in {{build_log}} and re-present F to the fixer in the next iteration (do not record as dismissed until a rationale is supplied).
          — Record F in {{finding_dispositions}}: { finding_id: F.id, disposition: "dismissed", summary: F.summary, dismissal_rationale: F.dismissal_rationale }
          — Look up the inbound finding I for F.finding_id in {{stage2_findings}} to recover severity.
          — LEDGER (phantom-store closure): append per standing rule: { event: "finding-disposition", story_slug: S.slug, finding_id: F.id, disposition: "dismissed", summary: F.summary, dismissal_rationale: F.dismissal_rationale, severity: I.severity, ts: NOW() }

        CASE disposition == "triaged-out":
          — Look up the inbound finding I for F.finding_id in {{stage2_findings}} to recover summary, detail, location, and suggested_fix (the fixer's triaged-out disposition object carries only finding_id and disposition; the descriptive fields live on the inbound finding).
          — Record F in {{finding_dispositions}}: { finding_id: F.finding_id, disposition: "triaged-out", summary: I.summary, detail: I.detail, location: I.location, suggested_fix: I.suggested_fix }
          — LEDGER (phantom-store closure): append per standing rule: { event: "finding-disposition", story_slug: S.slug, finding_id: F.finding_id, disposition: "triaged-out", summary: I.summary, severity: I.severity, ts: NOW() }
          — The Conductor will route triaged-out findings to momentum:triage at build-phase completion (not inline here — triage is deferred to avoid blocking the fix loop). The recovered descriptive fields ensure the triage stub has actionable content.

        CASE disposition == "escalated":
          — Look up the inbound finding I for F.finding_id in {{stage2_findings}} to recover stakes_class, summary, evidence, and suggested_fix (the fixer's escalated disposition object carries these in the nested escalation object and does not echo them at the top level; join by finding_id). Canonical shape defined in directed-fix-invocation-contract.md §"Canonical Fixer Output Shape".
            Resolve fields: stakes_class = I.stakes_class; timing_tier = F.escalation.timing_tier (NESTED — read from inside the escalation object, NOT from F.timing_tier; default "end-gate-expanded" if absent); summary = I.summary; evidence = F.escalation.evidence (inline from fixer) or I.evidence; suggested_fix = I.suggested_fix.
          — Record in {{finding_dispositions}}: { finding_id: F.finding_id, disposition: "escalated", stakes_class: stakes_class, timing_tier: timing_tier, summary: summary, evidence: evidence, suggested_fix: suggested_fix }
          — LEDGER (phantom-store closure): append per standing rule: { event: "finding-disposition", story_slug: S.slug, finding_id: F.finding_id, disposition: "escalated", stakes_class: stakes_class, timing_tier: timing_tier, summary: summary, severity: I.severity, ts: NOW() }
          — F is removed from the retry-bound-3 loop IMMEDIATELY. No further fix/re-check attempts will be run against F inside this loop.
          — Route by timing tier:
              IF timing_tier == "mid-flight":
                — The finding is irreversible-and-imminent OR build-invalidating (per skills/momentum/references/directed-fix-invocation-contract.md narrow bar).
                — Append to {{mid_flight_escalations}} (accumulated for dispatch to step 2.F after all findings are processed).
              ELSE (timing_tier == "end-gate-expanded" OR timing_tier not set):
                — The finding is stakes-class but does NOT meet the mid-flight bar. Route to end-gate-expanded tier (the default and safety net).
                — Append to {{story_end_gate_escalations}}: { finding_id: F.finding_id, stakes_class: stakes_class, timing_tier: "end-gate-expanded", summary: summary, evidence: evidence, suggested_fix: suggested_fix }
                — Record in {{build_log}}: { story_slug: S.slug, event: "stage3-escalation", disposition: "escalated", timing_tier: "end-gate-expanded", finding_summary: summary }
                — Continue the fix loop. This escalation does NOT pause the build or stop other findings from completing.
      </action>

      <!-- ── Phase C: /simplify cleanup pass ──────────────────────── -->
      <!--                                                               -->
      <!-- TRIGGER RULE (single, non-conflicting): the /simplify pass   -->
      <!-- runs on EVERY story, once per fix-loop iteration, immediately -->
      <!-- after Phase B returns. No size/diff threshold. No on-demand  -->
      <!-- opt-in. No second condition elsewhere in this step overrides  -->
      <!-- this rule. The pass is always executed when Phase B applies   -->
      <!-- at least one fix; when Phase B finds nothing to fix (empty    -->
      <!-- stage2_findings) the fix loop exits at the empty-findings     -->
      <!-- check above and this action is never reached.                 -->

      <action>PHASE C — SIMPLIFY CLEANUP: Spawn the /simplify skill as a subagent (individual-agent, NOT TeamCreate):
        Input:
          - worktree_path: `.worktrees/story-{S.slug}` (the story's worktree after Phase B fixes have been committed)
          - writable_files: {{writable_files}} (same scope constraint as the Phase B fixer)
        Constraint passed to subagent: "Apply code simplification and cleanup only. Do not introduce new logic,
          fix bugs, or expand scope. Do not mutate git. Return a findings list of cleanup changes applied
          (each entry: { finding_id, type: 'cleanup', severity: 'low', summary, location, suggested_fix }).
          If nothing warrants cleanup, return an empty list."
        Bind {{simplify_findings}} = the subagent's returned findings list (may be empty).
      </action>

      <action>PHASE C — CAPTURE AND COMMIT: If {{simplify_findings}} is non-empty:
        Verify that every file modified by the /simplify subagent is in {{writable_files}}. Apply the same
        write-scope guard used in Phase B: unstage and discard any out-of-scope edits before committing.
        The Conductor (sole git-mutation authority) commits the cleanup output:
          `git -C .worktrees/story-{S.slug} add -u`
          (apply write-scope guard before proceeding)
          `git -C .worktrees/story-{S.slug} commit -m "refactor({S.slug}): simplify cleanup pass"`
        Record in {{build_log}}: { story_slug: S.slug, event: "stage3-simplify-pass", findings_count: length({{simplify_findings}}), committed: true }
        If {{simplify_findings}} is empty: record in {{build_log}}: { story_slug: S.slug, event: "stage3-simplify-pass", findings_count: 0, committed: false }
        Do NOT invoke momentum:triage for simplify findings — they are cleanup-only, not defects.
      </action>

      <action>PHASE C — FEED BACK: Merge {{simplify_findings}} into the unresolved findings list for the next
        Phase B iteration. Each entry in {{simplify_findings}} is tagged stakes_class: "routine" and
        disposition: null (unresolved). Append to {{remaining_findings}} so they are presented to the Phase B
        fixer in the next iteration as routine cleanup candidates.
        Note: this feedback is ONLY meaningful when the loop is about to re-enter Phase B (i.e., when
        {{remaining_findings}} from Phase D is non-empty or {{simplify_findings}} itself is non-empty and the
        loop has iterations remaining). If all other findings are resolved AND {{simplify_findings}} is empty,
        Phase D will find {{remaining_findings}} empty and the loop exits cleanly — no re-entry to Phase B.
        If {{simplify_findings}} is non-empty but all fix-attempt budgets are at {{MAX_FIX_ATTEMPTS}}: the
        simplify findings do NOT extend the fix budget beyond {{MAX_FIX_ATTEMPTS}} — they are treated
        as iteration-zero findings ({{fix_attempts}}[F.id] initialized to 0) and are subject to the same
        per-finding retry bound.
      </action>

      <!-- ── Mid-flight dispatch for bar-clearing escalations ───────── -->

      <check if="{{mid_flight_escalations}} is non-empty">
        <note>One or more findings in the current iteration were classified mid-flight by the fixer. Per the SHARED-PRIMITIVE CONTRACT (step 2.F / references/escalation.md), the Conductor does NOT pre-classify or loop over candidates itself. It passes the full {{mid_flight_escalations}} array to the escalation engine (step 2.F) in a single invocation — the engine owns bar evaluation and the pause/continue decision. Other routine findings continue their fix/re-check cycle unaffected.</note>
        <action>Invoke step 2.F (the mid-flight escalation consumption hook) once with the full {{mid_flight_escalations}} array as the findings input.
          The escalation engine evaluates the bar for each finding and returns "pause-branch" or "continue" per its contract (references/escalation.md).
          Record outcome in {{build_log}}: { story_slug: S.slug, event: "stage3-mid-flight-escalation", disposition: "escalated", timing_tier: "mid-flight", finding_count: length({{mid_flight_escalations}}) }
          Append each finding to {{escalations}}: { story_slug: S.slug, stakes_class: F.stakes_class, timing_tier: "mid-flight", disposition: "escalated" }
        </action>
      </check>

      <!-- ── Phase D: RE-CHECK gate — loop control ─────────────────── -->

      <action>PHASE D — RE-CHECK: Re-run only the reviewer(s) that originally raised unresolved routine findings.
        RE-CHECK NORMALIZATION: qa-reviewer output from a Phase D re-check passes through
        the same stage-2 normalization mapping (above) before resolution matching — the
        re-check producer format is identical to the original. Do not attempt resolution
        matching against producer-format re-check output; normalize first, then match
        against {{remaining_findings}} by location and summary.
        Collect {{remaining_findings}} = UNION of:
          (a) findings not yet resolved (status not fixed | dismissed | triaged-out | escalated | scope-reverted | blocked), AND
          (b) any entries in {{simplify_findings}} with disposition: null that are not already present in set (a).
        This additive collect ensures simplify findings appended by Phase C FEED BACK survive into the next Phase B
        iteration — they carry disposition: null and were never in stage2_findings, so a status-only filter would drop them.
        Note: escalated findings (both end-gate-expanded and mid-flight) are ALREADY removed from {{remaining_findings}} — they exit the retry loop at escalation time and are never re-checked inside the loop. Scope-reverted findings are also removed — they were fully discarded by the write-scope guard and re-routed inline; re-presenting them to the fixer would be incorrect (the defect is out-of-scope for this story). Blocked findings are also excluded — their fix budget is exhausted and they are handled by the blocked-then-continue path below.
        DIFF RANGE FOR RE-CHECK: Use the same canonical pre-merge merge-base pattern as stage 2. The story branch is still pre-merge at this point. Canonical pattern: references/per-story-review-diff-range.md (Scenario A — Pre-Merge Review).
      </action>

      <check if="{{remaining_findings}} is empty">
        <note>All findings are resolved (fixed, dismissed, triaged-out, escalated, scope-reverted, or blocked). The fix loop is clean. Proceed to stage-4 (merge).</note>
        <action>Proceed to stage-4 (merge) for story S.
          Emit partial pipeline signal payload (for eventual terminal signal from stage-4):
            leftover_findings: [] (none remaining)
            escalations: {{story_end_gate_escalations}} (per-story accumulator; consumed by step 2.2 accumulation action into Conductor-scoped {{end_gate_escalations}}; mid-flight escalations already dispatched)
        </action>
      </check>

      <check if="{{remaining_findings}} is non-empty">

        <!-- ── Retry-bound-3 enforcement ──────────────────────── -->

        <action>For each finding F in {{remaining_findings}}:
          Increment {{fix_attempts}}[F.id] (initialize to 0 if absent).
        </action>

        <check if="any F in {{remaining_findings}} has {{fix_attempts}}[F.id] less than {{MAX_FIX_ATTEMPTS}}">
          <note>Retry budget available for at least one remaining finding. Loop back to Phase B with the unresolved findings.</note>
          <action>Return to Phase B (CONVERGE): invoke the directed fixer again with {{remaining_findings}} (the subset still unresolved).
            Do not pass already-fixed, dismissed, triaged-out, escalated, or scope-reverted findings back to the fixer — pass only the genuinely unresolved ones.
          </action>
        </check>

        <check if="all F in {{remaining_findings}} have {{fix_attempts}}[F.id] >= {{MAX_FIX_ATTEMPTS}}">
          <note>Retry budget exhausted for all remaining findings ({{MAX_FIX_ATTEMPTS}} attempts reached). Mark each exhausted finding BLOCKED. Continue to the next story — do NOT halt the whole build.</note>
          <action>For each finding F in {{remaining_findings}} (where {{fix_attempts}}[F.id] >= {{MAX_FIX_ATTEMPTS}}):
            Record F in {{finding_dispositions}}: { finding_id: F.id, disposition: "blocked", summary: F.summary, attempts: {{fix_attempts}}[F.id] }
            Look up the inbound finding I for F.id in {{stage2_findings}} to recover severity.
            LEDGER (phantom-store closure): append per standing rule: { event: "finding-disposition", story_slug: S.slug, finding_id: F.id, disposition: "blocked", summary: F.summary, severity: I.severity, attempts: {{fix_attempts}}[F.id], ts: NOW() }
            Append to {{build_log}}: { story_slug: S.slug, event: "stage3-finding-blocked", finding_id: F.id, finding_summary: F.summary, attempts: {{fix_attempts}}[F.id] }
          </action>
          <action>Emit partial pipeline signal payload:
            leftover_findings: blocked findings list (for end-gate report and triage spin-out)
            escalations: {{story_end_gate_escalations}} (per-story accumulator; consumed by step 2.2 accumulation action into Conductor-scoped {{end_gate_escalations}})
            Note: mid-flight escalations were already dispatched inline; they do not appear in leftover_findings.
          </action>
          <note>BLOCKED-then-continue: the whole-build is NOT halted. However, per spec §3 stage-3 ('BLOCKED -> spin a stub via momentum:triage, leave unmerged'), story S is NOT merged. The Conductor removes S from {{running}} WITHOUT transitioning it to stage-4, spins a triage stub for the blocked findings, and continues building other stories in {{running}} and {{frontier}} unaffected. The story remains unmerged; dependents whose >= gate requires S's merge become unsatisfiable, which is the intended consequence of an unmergeable story.</note>
          <action>Mark story S as BLOCKED (do NOT invoke stage-4 merge for S).
            Remove S from {{running}}.
            Note: do NOT transition S to a terminal status here — the story remains at its current non-terminal status. The terminal transition (closed-incomplete) is deferred to Phase 5 approve, which performs the single terminal transition for all stranded/blocked stories (quarantine convention, per spec §6/§8). "blocked" is Conductor in-memory state only (tracked via leftover_findings and build_log).
            Spin a triage stub for the blocked findings: invoke momentum:triage with the blocked findings list for S, so they are queued into the backlog.
            Record in {{build_log}} (and the build ledger per standing rule): { event: "stage3-story-blocked", story_slug: S.slug, leftover_count: length(blocked findings), stranded: true, note: "story left unmerged per spec §3; terminal status transition deferred to Phase 5 approve", ts: NOW() }
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

      <note>TIMING-AND-VENUE ONLY — DEC-036 does NOT change this branch. DEC-036's amendments (narrow stakes-gated mid-flight escalation; legible dispositions fixed | dismissed | triaged-out | escalated with required non-empty rationale for dismissals; end-gate-expanded vs. mid-flight timing tiers; anti-rubber-stamp end-gate) concern HOW findings are classified and WHEN stakes-class findings leave the silent auto-fix path. This branch concerns only WHEN the dedicated QA verification run happens (build vs. AVFL/merge) and WHERE it runs. Choosing `covered-by-composition` changes only the timing and venue of the dedicated QA verification run (REVIEWER A / qa-reviewer); it never demotes, hides, silences, or auto-resolves any finding — including any stakes-class finding. Adversarial code review (REVIEWER B / momentum:code-reviewer) still runs at build time on the per-story diff for every story whose pipeline reaches stage-2 (i.e., stories that were not halted by the integrity-stop guard at 2.1.4) regardless of coverage disposition — the code review is not a QA verification run and is never deferred by this branch. A stakes-class finding (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture) that surfaces from the code review at build time or from the deferred QA verification at AVFL/merge is still routed out of the silent auto-fix path and rendered in the report by the finding schema and report — NOT by this branch. The deferral does not weaken that routing. This boundary must remain clear: a future reader must not mistake `covered-by-composition` for a way to bypass stakes handling or skip code review.</note>

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
        <action>Log a warning in {{build_log}} for story S: { story_slug: S.slug, event: "coverage-disposition-default", reason: "coverage_disposition was missing or unrecognized — defaulted to dedicated-run", observed_value: {{coverage_disposition}} }.
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
            { story_slug: S.slug, event: "coverage-disposition-incomplete",
              reason: "coverage_disposition is 'covered-by-composition' but covered_by_scenario is null/missing/empty — cannot defer without a named integration scenario; defaulted to dedicated-run",
              observed_coverage_disposition: "covered-by-composition",
              observed_covered_by_scenario: {{covered_by_scenario}} }
          Treat S as `dedicated-run` for all purposes in this build phase. Proceed to the dedicated-run path (Path A) below.
        </action>
      </check>

      <!-- ── Path B: covered-by-composition ───────────────────── -->
      <check if="{{coverage_disposition}} == 'covered-by-composition' AND {{covered_by_scenario}} is present AND non-empty">
        <note>This story's dedicated QA verification run is deferred to a named integration scenario at AVFL/merge. No dedicated QA verification run (REVIEWER A / qa-reviewer) is performed for this story at build time. Adversarial code review (REVIEWER B / momentum:code-reviewer) still runs at build time on the per-story diff — coverage disposition does not defer, skip, or weaken code review. The Conductor records the deferral explicitly — it does not silently drop the QA verification. The named integration scenario ({{covered_by_scenario}}) is the downstream discharge point at AVFL/merge (Phase 3). The deferral record is informational: it states THAT the dedicated QA run was skipped and WHICH scenario owns the discharge, and notes that code review still runs at build time. Nothing in this record changes how findings from either the code review or the integration scenario are classified, escalated, or reported.</note>
        <note>PRECONDITION — a named scenario is required. This path is reached only when covered_by_scenario is present and non-empty. When it is null/missing/empty, the guard above fires first and routes to dedicated-run instead. This ensures AC 3's naming requirement is a hard precondition for skipping the dedicated build-time run.</note>
        <action>Skip the dedicated QA verification run for story S at build time. Do NOT dispatch REVIEWER A (qa-reviewer) for S during this build phase. Stage-2 still dispatches REVIEWER B (momentum:code-reviewer) on the per-story diff — coverage disposition defers only the QA verification run, not the code review.
          Record the deferral in {{build_log}}:
            { story_slug: S.slug, title: S.title, event: "coverage-disposition-deferred",
              coverage_disposition: "covered-by-composition",
              covered_by_scenario: {{covered_by_scenario}},
              note: "Dedicated build-time QA run (REVIEWER A) skipped. Adversarial code review (REVIEWER B) still runs at build time on the per-story diff (stage-2). QA verification debt to be discharged at AVFL/merge by the named integration scenario." }
          Return routing outcome to step 2.1.5: { outcome: "covered-by-composition", integration_scenario: {{covered_by_scenario}} }.
          Do not produce a VERIFIED / PARTIAL / MISSING / BLOCKED verification disposition for story S from this build-phase step — the verification result belongs to the integration scenario at AVFL/merge.
        </action>
        <note>GUARDRAIL — no second QA run. Once this routing outcome is returned and the deferral is recorded, the Conductor must NOT perform an additional dedicated QA verification run (REVIEWER A / qa-reviewer) for S during the build phase. The deferral is a one-way routing decision for the build phase; it does not prevent the integration scenario from running at AVFL/merge — it ensures the dedicated build-time QA run does not also run. Double-running wastes effort and can produce contradictory signals. REVIEWER B's code-review dispatch on the per-story diff is NOT a QA verification run and does not violate this guardrail — it is adversarial bug-hunting, not acceptance verification.</note>
        <note>STAKES-CLASS BOUNDARY — deferral does not weaken routing. If the integration scenario at AVFL/merge surfaces a stakes-class finding (security-auth-isolation | irreversible-destructive | high-blast-radius-architecture), that finding is still routed out of the silent auto-fix path and rendered in the report by the finding schema and report. The deferral from this build-phase branch does not weaken, suppress, or narrow that routing. The timing/venue changed; the routing rules did not.</note>
        <note>DOWNSTREAM DISCHARGE — wired in Phase 3 step 3.D. The `coverage-disposition-deferred` build_log record and the `covered_by_scenario` field drive the discharge consumer at AVFL/merge (Phase 3 step 3.D). Step 3.D reads all deferred records, runs each named integration scenario, records the outcome as `verified-by-composition` on pass, and surfaces any undischarged deferral as a leftover finding at the end-gate. The discharge loop is closed — the deferral is not silently assumed satisfied. Step 3.D discharges the deferred QA verification debt only — it does not perform or replace code review, which runs at build time via stage-2 REVIEWER B.</note>
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
            {{story_end_gate_escalations}} (reset each story in step 2.S3; emitted as S.escalations
            in the pipeline signal payload) and the Conductor-scoped {{end_gate_escalations}}
            that step 5 Source 1 reads to build decision cards.
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
            2. Record conflict detail in {{build_log}} (and the build ledger per standing rule):
               { event: "story-terminal", story_slug: S.slug, title: S.title, outcome: "quarantined",
                 reason: "conflict unresolved after 3 attempts",
                 conflict_files: {{conflict_files}},
                 merge_attempts: {{merge_attempts}}[S.slug],
                 ts: NOW() }
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
              Append to {{build_log}} (and the build ledger per standing rule): { event: "story-terminal", story_slug: S.slug, title: S.title, outcome: "merged",
                findings_summary: S.leftover_findings,
                escalations: (any escalation records produced during this story's merge path),
                ts: NOW() }.
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
            Record the retry attempt in {{build_log}}: { story_slug: S.slug, event: "retry", attempt: {{retries}}[S.slug] }.
          </action>
        </check>

        <check if="{{retries}}[S.slug] >= 2">
          <action>Exhausted retries. Mark S blocked:
            Add S.slug to {{blocked}}.
            Remove S.slug from {{running}}.
            Note: do NOT transition S to a terminal status here — the story remains at its current non-terminal status. The terminal transition (closed-incomplete) is deferred to Phase 5 approve, which performs the single terminal transition for all stranded/blocked stories (quarantine convention, per spec §6/§8). "blocked" is Conductor in-memory state ({{blocked}} array); "blocked" is not a valid state in the tool's state machine.
            Append to {{build_log}} (and the build ledger per standing rule): { event: "story-terminal", story_slug: S.slug, title: S.title, outcome: "blocked", reason: S.reason, retry_count: {{retries}}[S.slug], stranded: true, note: "terminal status transition deferred to Phase 5 approve", ts: NOW() }.
            CONTINUE. Do not halt the build phase. Other stories in {{running}} and {{frontier}} are unaffected.
          </action>
          <note>A blocked story does not propagate to its dependents automatically. Dependents whose depends_on includes S.slug remain in "ready-for-dev" — they can never satisfy the >= review gate for S, so they are never added to the frontier and never launched. At build end, the completion check (below) sweeps all remaining ready-for-dev stories with unsatisfiable depends_on and marks them blocked. The end-of-build sweep is the single mechanism that marks stranded dependents blocked.</note>
        </check>
      </check>

      <!-- ── Build-phase completion check ─────────────────────── -->
      <check if="{{running}} is empty AND {{frontier}} is empty">
        <action>All pipelines have terminated. Build phase heartbeat ends.
          For any remaining stories in {{story_map}} that are still in "ready-for-dev" state with unsatisfiable depends_on:
            Add to {{blocked}}; transition to "closed-incomplete" via `momentum-tools sprint status-transition --story {slug} --target closed-incomplete`; append to {{build_log}} (and the build ledger per standing rule): { event: "story-terminal", story_slug: slug, outcome: "blocked", reason: "dependency never reached >= review", ts: NOW() }.
          For any story in {{story_map}} still in "in-progress" not handled by step 2.0 reconcile:
            Record in {{build_log}} (and the build ledger per standing rule): { event: "story-terminal", story_slug: slug, outcome: "stranded", note: "defer to spec §6 reconcile-on-start handler", ts: NOW() }.
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
          <action>Record outcome in {{build_log}}: { story_slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", resolution: "fix-applied", finding_summary: {{finding.summary}} }.
            Note: disposition is "escalated" (not "fixed") — this finding was raised mid-flight to the developer; it is stakes-class and was not silently auto-fixed. The "escalated" disposition is distinct from "fixed" (routine auto-fix), "dismissed" (waved off with rationale), and "triaged-out" (outside scope). "resolution: fix-applied" records how the escalated finding was resolved.
          </action>
          <action>Append record to {{escalations}}: { story_slug: S.slug, stakes_class, timing_tier: "mid-flight", disposition: "escalated", resolution: "fix-applied" }.</action>
          <action>Return "continue" to step 2.2 (the merge and frontier re-evaluation for S proceed). No further mid-flight pause is raised for this resolved finding.</action>
        </check>

        <check if="Change">
          <action>Receive the developer's alternative instruction (what to do differently). Spawn a fix subagent with the developer's alternative instruction (individual-agent, not TeamCreate). The subagent produces output only. The Conductor commits the changed action.</action>
          <action>Record outcome in {{build_log}}: { story_slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", resolution: "changed-action", developer_instruction: {{developer_instruction}}, finding_summary: {{finding.summary}} }.</action>
          <action>Append record to {{escalations}}: { story_slug: S.slug, stakes_class, timing_tier: "mid-flight", disposition: "escalated", resolution: "changed-action", developer_instruction: {{developer_instruction}} }.</action>
          <action>Return "continue" to step 2.2 (the merge and frontier re-evaluation for S proceed). No further mid-flight pause is raised for this resolved finding.</action>
        </check>

        <check if="Abort-that-branch">
          <action>Abandon this branch only. Do NOT halt the entire build phase — other stories in {{running}} and {{frontier}} continue unaffected.</action>
          <action>Remove S.slug from {{running}}.
            Note: do NOT transition S to a terminal status here — the story remains at its current non-terminal status. The terminal transition (closed-incomplete) is deferred to Phase 5 approve, which performs the single terminal transition for all stranded/blocked stories (quarantine convention, per spec §6/§8).
            Add S.slug to {{blocked}} so Phase 5 approve can identify it for the closed-incomplete transition.
          </action>
          <action>Record outcome in {{build_log}}: { story_slug: S.slug, event: "mid-flight-escalation", disposition: "escalated", resolution: "branch-aborted", finding_summary: {{finding.summary}} }.</action>
          <action>Append record to {{escalations}}: { story_slug: S.slug, stakes_class, timing_tier: "mid-flight", disposition: "escalated", resolution: "branch-aborted" }.</action>
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
          summary: L.description, evidence: L.evidence, suggested_fix: L.suggestion,
          why_unresolved: L.why_unresolved,
          story_slug: L.owning_stories[0] or "sprint-integration",
          location: L.location, owning_stories: L.owning_stories,
          disposition: "residual", stakes_class: L.stakes_class or "routine",
          type: "integration" }
        Note: stakes_class is carried from L.stakes_class (populated by the merge-review leftover schema).
        Default to "routine" only when L.stakes_class is absent. This preserves non-routine stakes
        classifications so Source 2 at step 5 can correctly surface them as decision cards.

      Tag all entries: source = "avfl-merge-review".

      LEDGER — Per-finding AVFL events: For each entry in {{avfl_findings}}, append to {{build_log}} and the build ledger:
        { event: "avfl-finding", story_slug: (F.story_slug or "sprint-integration"), finding_id: F.finding_id,
          disposition: F.disposition, severity: F.severity, stakes_class: F.stakes_class,
          summary: F.summary, evidence: F.evidence, suggested_fix: F.suggested_fix,
          source: "avfl-merge-review", ts: NOW() }
      This makes AVFL finding-level data durable — Phase 5 Sources 2-3 can reconstruct {{avfl_findings}} from the ledger on resume.

      From Group-A fixer escalations (findings the directed fixer returned with disposition "escalated"
        during the merge-review inner fix loop — tracked via workflow-merge-review.md step 5 Group-A
        handling at ~line 280-282, where escalated dispositions are carried forward as leftovers with
        why_unresolved: "escalated (stakes-class — held for end-gate)"):
        For each leftover L where L.why_unresolved starts with "escalated":
          Append to {{end_gate_escalations}}: { finding_id: L.id,
            stakes_class: L.stakes_class or "routine",
            timing_tier: "end-gate-expanded",
            summary: L.description, evidence: L.evidence, suggested_fix: L.suggestion,
            story_slug: L.owning_stories[0] or "sprint-integration",
            source: "avfl-merge-review" }
          Append to {{build_log}} (and the build ledger per standing rule — REQUIRED so this escalation survives session death):
            { event: "stage3-escalation", story_slug: (L.owning_stories[0] or "sprint-integration"),
              finding_id: L.id, stakes_class: L.stakes_class or "routine",
              timing_tier: "end-gate-expanded", finding_summary: L.description, ts: NOW() }
          Tag the corresponding {{avfl_findings}} entry with timing_tier: "end-gate-expanded" and
          disposition: "escalated" (overriding "residual") so Source 2 de-dup at step 5 correctly
          identifies these as already escalated and avoids double-counting.
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

    <action>Append AVFL-on-merge results to {{build_log}} (and the build ledger per standing rule):
      { event: "avfl-on-merge-complete", phase: "avfl-on-merge",
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
        Each entry has shape: { story_slug, title, covered_by_scenario, coverage_disposition }.
        Bind {{deferred_records}} = the filtered list.
        Note: entries use story_slug (not slug) as the canonical join key per the key vocabulary rule in the standing rule.
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
              { story_slug: R.story_slug, title: R.title,
                event: "coverage-deferral-undischarged",
                covered_by_scenario: {{scenario_id}},
                outcome: "scenario-not-found",
                note: "Named integration scenario could not be located; deferral remains open." }
          — Append an undischarged-deferral leftover to {{avfl_findings}}:
              { source: "coverage-discharge-consumer",
                finding_id: "undischarged-deferral-{{R.story_slug}}",
                severity: "major",
                type: "coverage-gap",
                stakes_class: "routine",
                disposition: "residual",
                story_slug: R.story_slug,
                location: R.story_slug,
                summary: "Coverage deferral for `{{R.story_slug}}` is undischarged — named scenario `{{scenario_id}}` not found.",
                detail: "Story `{{R.story_slug}}` was deferred from build-time QA with the expectation that integration scenario `{{scenario_id}}` would verify its acceptance behavior at AVFL/merge. The scenario cannot be located. The verification debt is unresolved.",
                evidence: "coverage-disposition-deferred record: slug={{R.story_slug}}, covered_by_scenario={{scenario_id}}; scenario file not found under `.momentum/sprints/{{sprint_slug}}/specs/`.",
                suggestion: "Locate or create the named integration scenario `{{scenario_id}}`, run it against the sprint branch, and confirm it observes `{{R.story_slug}}`'s required behavior. Alternatively, re-run story `{{R.story_slug}}` with `coverage_disposition: dedicated-run`." }
          — Skip to the next deferred record. Do NOT proceed to the run step.

        RUN THE SCENARIO (when {{scenario_found}} == true):
          Spawn an integration-scenario executor agent (individual-agent, NOT TeamCreate) with:
            - scenario_id: {{scenario_id}}
            - scenario_path: the resolved path to the scenario file
            - sprint_branch: "sprint/{{sprint_slug}}"
            - deferred_story_slug: R.story_slug
            - deferred_story_title: R.title
            - story_spec: ".momentum/stories/{{R.story_slug}}.md"
            - contract_path: the path to R.story_slug's verification contract (from `story_assignments[R.story_slug].contract.path` in the sprint record)
          Constraint passed to agent: "Run the named integration scenario against the integrated sprint branch. Verify that the scenario observes the deferred story's required acceptance behavior. Return a structured result: { scenario_id, ran: bool, passed: bool, deferred_story_observed: bool, evidence: string, stakes_findings: array }. The `stakes_findings` array contains any non-routine stakes-class concerns you observe while running the scenario — each entry has shape: { stakes_class: string, summary: string, location: string, evidence: string, suggested_fix: string }. Include only findings whose stakes_class is one of: security-auth-isolation | irreversible-destructive | high-blast-radius-architecture. Routine findings are not included in this array. The array may be empty. Do not mutate git. Do not spawn build agents."
          Bind {{scenario_result}} = the agent's returned result for this record.

        EVALUATE DISCHARGE:
          A deferral is DISCHARGED only when ALL three conditions hold:
            (1) {{scenario_result}}.ran == true          — the scenario was actually executed
            (2) {{scenario_result}}.passed == true       — the scenario passed
            (3) {{scenario_result}}.deferred_story_observed == true  — the deferred story's
                  acceptance behavior was observed by the scenario (not merely that the scenario
                  passed on its own — the scenario must provide positive evidence that it covers
                  R.story_slug's required behavior)
          If ANY condition is false: the deferral is NOT discharged.
      </action>

      <!-- ── 3.D.3 — Record outcomes ─────────────────────────────── -->

      <action>For each deferred record R and its {{scenario_result}}:

        CASE: all three discharge conditions hold (ran AND passed AND deferred_story_observed):
          — Record discharge in {{build_log}}:
              { story_slug: R.story_slug, title: R.title,
                event: "coverage-deferral-discharged",
                covered_by_scenario: {{scenario_id}},
                outcome: "verified-by-composition",
                evidence: {{scenario_result}}.evidence,
                note: "Deferred story's acceptance behavior was observed by the named integration scenario. Verification debt discharged." }
          — Tag the story as verified-by-composition in the Conductor's in-memory state:
              {{coverage_discharge_results}}[R.story_slug] = { outcome: "verified-by-composition", scenario_id: {{scenario_id}}, evidence: {{scenario_result}}.evidence }
          — No undischarged-deferral leftover is appended to {{avfl_findings}} for this record.
          — STAKES-FINDINGS PASS-THROUGH: Even when a deferral is discharged, the executor may have observed non-routine stakes-class concerns while running the scenario. These must not be silently dropped.
            For each entry SF in {{scenario_result}}.stakes_findings (may be empty):
              If SF.stakes_class is one of { security-auth-isolation, irreversible-destructive, high-blast-radius-architecture }:
                Append to {{avfl_findings}}:
                  { source: "coverage-discharge-consumer",
                    finding_id: "discharge-stakes-{{R.story_slug}}-{{loop_index}}",
                    severity: "major",
                    type: "stakes-finding",
                    stakes_class: SF.stakes_class,
                    disposition: "residual",
                    story_slug: R.story_slug,
                    location: SF.location,
                    summary: SF.summary,
                    detail: "Stakes-class concern observed by the discharge executor while running scenario `{{scenario_id}}` for deferred story `{{R.story_slug}}`. The deferral itself was discharged (scenario passed), but this concern requires a human decision — it is not on the routine auto-fix path.",
                    evidence: SF.evidence,
                    suggestion: SF.suggested_fix }
                (Routine findings from the executor are NOT added here — they are out of scope for this path.)

        CASE: any discharge condition fails (scenario ran but did not pass, OR ran and passed but deferred story's behavior was not observed, OR scenario could not run):
          — Determine the failure mode for evidence:
              If {{scenario_result}}.ran == false: failure_mode = "scenario-did-not-run"
              Else if {{scenario_result}}.passed == false: failure_mode = "scenario-failed"
              Else: failure_mode = "deferred-story-behavior-not-observed"
          — Record in {{build_log}}:
              { story_slug: R.story_slug, title: R.title,
                event: "coverage-deferral-undischarged",
                covered_by_scenario: {{scenario_id}},
                outcome: failure_mode,
                evidence: {{scenario_result}}.evidence,
                note: "Deferral is not discharged; see leftover finding in end-gate report." }
          — Append an undischarged-deferral leftover to {{avfl_findings}}:
              { source: "coverage-discharge-consumer",
                finding_id: "undischarged-deferral-{{R.story_slug}}",
                severity: "major",
                type: "coverage-gap",
                stakes_class: "routine",
                disposition: "residual",
                story_slug: R.story_slug,
                location: R.story_slug,
                summary: "Coverage deferral for `{{R.story_slug}}` is undischarged — {{failure_mode}} for scenario `{{scenario_id}}`.",
                detail: "Story `{{R.story_slug}}` was deferred from build-time QA. Its named integration scenario `{{scenario_id}}` was expected to observe its acceptance behavior at AVFL/merge. The discharge failed: {{failure_mode}}. The verification debt is unresolved.",
                evidence: {{scenario_result}}.evidence,
                suggestion: "Investigate why scenario `{{scenario_id}}` did not discharge the deferral ({{failure_mode}}). Ensure the scenario explicitly covers story `{{R.story_slug}}`'s acceptance criteria. Re-run Phase 3 after fixing the scenario, or re-run story `{{R.story_slug}}` with `coverage_disposition: dedicated-run`." }
      </action>

      <action>Append coverage-discharge summary to {{build_log}} (and the build ledger per standing rule):
        { phase: "avfl-on-merge",
          event: "coverage-discharge-consumer-complete",
          deferred_count: length({{deferred_records}}),
          discharged_count: count of entries in {{coverage_discharge_results}} where outcome == "verified-by-composition",
          undischarged_count: count of entries in {{build_log}} where event == "coverage-deferral-undischarged" }
      </action>

      <note>STAKES-ROUTING NOTE. Two categories of findings flow out of this step:
        (1) Undischarged-deferral leftovers — injected into {{avfl_findings}} with stakes_class:"routine" and disposition:"residual". Because they are routine, Phase 3 step 3.4 holds them (no escalation check) and Phase 5 Source 2 excludes them from {{stakes_findings}} (which filters to non-routine residuals only). They surface to the developer via the {{undischarged_deferrals}} variable computed in Phase 5's supporting-variables step and rendered in §05 of the end-gate report — not via the §04 decision-card path.
        (2) Stakes-class findings returned by the discharge executor — injected into {{avfl_findings}} with the executor-reported stakes_class (non-routine) and disposition:"residual", source:"coverage-discharge-consumer". Because their stakes_class is non-routine, Phase 5 Source 2 picks them up for {{stakes_findings}} and they render as decision cards in §04 of the end-gate report. This holds EVEN WHEN the deferral itself was discharged (scenario passed). A passing scenario does not suppress a stakes-class concern the executor observed during the run. This routing closes the gap identified at step 2.C's STAKES-CLASS BOUNDARY: a deferral does not weaken stakes routing — it only defers the venue, never the path.</note>

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

    <action>Append E2E phase summary to {{build_log}} (and the build ledger per standing rule):
      { event: "e2e-phase-complete", phase: "e2e",
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
  <!-- STORY TERMINAL STATES — COMPLETE ENUMERATION                -->
  <!-- Every named terminal state has exactly one defined path     -->
  <!-- that reaches it. No named terminal state is unreachable.    -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <!--
    TERMINAL STATES AND THEIR REACHABLE PATHS:

    done
      PATH: Story merged to sprint branch (step 2.2.M.6 → status "review") → developer approves
        at end-gate (Phase 5) → Conductor transitions review → verify → done (two-step, Phase 5
        approve action). This is the success path for every story that completes the build pipeline.
      FINDING APPROVED-AS-IS (stakes-class finding acknowledged at end-gate without a code fix):
        The story itself still lands in "done". Acknowledging a decision card at the end-gate
        means the developer has reviewed the stakes-class finding and accepted the current state.
        The finding's own disposition remains "escalated" in the build record — it is NOT marked
        "fixed" — but the story status transitions to done regardless. The stakes-class finding
        is preserved in the build log and may produce a follow-up backlog stub via the
        MAJOR-RESIDUAL GOVERNANCE GUARD (Phase 5 approve action).

    closed-incomplete
      PATH: Story did NOT merge successfully. Any of the following produces closed-incomplete:
        (a) Retry-exhausted at pipeline level ({{retries}} >= PIPELINE_RETRY_BOUND=2, step 2.2
            failed-signal handler). Terminal transition deferred to Phase 5 approve.
        (b) Stage-3 finding budget exhausted (all {{fix_attempts}} >= {{MAX_FIX_ATTEMPTS}}=3,
            step 2.S3). Story left unmerged. Terminal transition deferred to Phase 5 approve.
        (c) Merge-attempts exhausted ({{merge_attempts}} >= 3, step 2.2.M.5 quarantine).
            Terminal transition deferred to Phase 5 approve.
        (d) Mid-flight Abort-that-branch choice by developer (step 2.F). Terminal transition
            deferred to Phase 5 approve.
        (e) Build-phase completion sweep: story still in ready-for-dev with unsatisfiable
            depends_on (step 2.2 completion check). Transitioned to closed-incomplete inline.
        In all cases the Conductor performs the transition via:
          `momentum-tools sprint status-transition --story {slug} --target closed-incomplete`

    dropped
      PATH: A story is transitioned to "dropped" when the DEVELOPER explicitly removes it from
        the sprint scope before or during the build — outside the automated pipeline. Specifically:
        the developer invokes `momentum-tools sprint status-transition --story {slug} --target dropped`
        directly (a manual operation, not performed by the Conductor). The Conductor observes
        "dropped" during H5 inconsistency check (line 134: "dropped" is in the canonical valid-
        status set). If the Conductor encounters a story in "dropped" status when seeding {{merged}}
        at step 2.0, it treats it as a non-blocking story (not added to {{frontier}}, not expected
        to merge). The Conductor NEVER transitions a story to "dropped" itself — that is a developer
        act. Stories the Conductor cannot merge go to closed-incomplete, not dropped.
      NOTE: "dropped" is reachable only via direct developer action outside the automated build.
        It is in the valid-status set (H5 check) because the Conductor must tolerate it as input
        state, not because the Conductor produces it as output.

    INVARIANT: No named terminal state is unreachable. Every terminal state listed in the
    canonical valid-status set has a defined path above. The Conductor produces "done" and
    "closed-incomplete"; "dropped" is produced by direct developer action and tolerated as input.
  -->

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PHASE 5: SINGLE HUMAN END-GATE                              -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="5" goal="Single human end-gate — the one mandatory developer acceptance point for the sprint build">
    <note>This is Touchpoint 2 — the only mandatory human acceptance gate in the entire build. It is unambiguously last: Phase 5 runs after E2E completes, and no second mandatory acceptance gate follows it. The end-gate report is a self-contained HTML file that organizes findings by user-facing functionality (DEC-035 D6). Stakes-class items appear as expanded decision cards requiring explicit acknowledgment (DEC-036 D4). Dismissed findings appear in a "Waved off" section with rationale (DEC-036 D3). The Approve control is not pre-checked (DEC-036 D4 anti-rubber-stamp). Full rendering spec: references/endgate-report-renderer.md.</note>

    <!-- ── Assemble {{stakes_findings}} from all three escalation sources ── -->

    <note>AUTHORITATIVE SOURCE: The build ledger at {{ledger_path}} is the authoritative source for all Phase 5 end-gate assembly. In-context accumulators ({{build_log}}, {{end_gate_escalations}}, {{escalations}}, etc.) are write-through caches populated during the build and rehydrated from the ledger on resume. At end-gate assembly time, the Conductor reads the ledger to assemble all report variables. This ensures an interrupted-then-resumed build produces the same end-gate as an uninterrupted run — the ledger survives session death; in-context variables do not.</note>

    <note>SUPERSESSION RULE (re-run stories): When the Conductor re-runs a story (resets in-progress → ready-for-dev at step 2.0 reconcile), the ledger will contain event rows from both the prior attempt and the current attempt for that story_slug. At Phase 5 assembly time, apply supersession when deriving per-story state from `finding-disposition` and `story-terminal` rows: for a given (story_slug, event, finding_id) tuple, the latest row by `ts` wins. This prevents prior-session rows from a re-run story from inflating counts (double-counting a finding) or placing the same story in both {{merged}} and {{blocked}}. The raw ledger timeline is preserved (prior rows not deleted), but Phase 5 reads only the superseding latest row per key tuple.</note>

    <action>Assemble {{stakes_findings}} — the full set of escalated decisions requiring human acknowledgment:

      LEDGER SOURCE: Read all rows from the build ledger at {{ledger_path}}.

      Source 1 — Per-story fix-loop escalations (step 2.S3):
        From the ledger only: collect all rows where event == "stage3-escalation" AND timing_tier == "end-gate-expanded".
        Under the write-through standing rule, every end-gate-expanded escalation is appended to the ledger at the time it is recorded in step 2.S3 — there are no unflushed events. The {{end_gate_escalations}} in-context accumulator is the write-through cache; the ledger is the authoritative source. Do not also collect from {{end_gate_escalations}} — the ledger already contains every entry that accumulator holds.
        Each entry carries: finding_id, stakes_class, timing_tier:"end-gate-expanded", summary, evidence, suggested_fix, story_slug.
      Source 2 — Post-merge AVFL escalations (Phase 3):
        From the ledger: collect rows where event == "avfl-finding" AND stakes_class != "routine" AND disposition in {"residual", "escalated"}.
        (Most AVFL-on-merge leftovers carry disposition "residual". Group-A fixer escalations carry disposition
        "escalated". The dedup at Bind {{stakes_findings}} below handles any overlap between Source 1 and Source 2.)
        For each, carry: finding_id, stakes_class, summary, evidence, suggested_fix, source:"avfl-merge-review".
        Note: do NOT read from {{avfl_findings}} in-context accumulator — it is a volatile cache that does not survive session death. The durable ledger rows (event == "avfl-finding") are the authoritative source.
      Source 3 — E2E failed/stakes scenarios (Phase 4):
        From the ledger: collect rows where event == "e2e-stakes-escalation" AND stakes_class != "routine".
        For each, carry: finding_id (generated at append time or "e2e-{story_slug}"), stakes_class, summary, evidence (from the row), suggested_fix, source:"e2e-validator".
        Note: do NOT read from {{e2e_findings}} in-context accumulator — it is a volatile cache. The durable ledger rows (event == "e2e-stakes-escalation") are the authoritative source.
      Bind {{stakes_findings}} = concat(Source 1, Source 2, Source 3), deduplicated by finding_id (Source 1 already carries E2E stakes findings appended by Phase 4; the dedup prevents double-counting with Source 3).
      If {{stakes_findings}} is empty: the build is clean; the gate can be approved without any decision cards.
    </action>

    <action>Assemble supporting report variables from the build ledger at {{ledger_path}}:

      CONDUCTOR-REVERT RECONCILIATION (must run BEFORE computing {{routine_auto_fixed_count}}):
        Collect {{reverted_fix_ids}} = { finding_id : entry } for every entry in {{conductor_reverted_fixes}} (rehydrated from ledger rows with event == "stage3-fix-scope-reverted" at step 2.0).
        Scan all ledger rows where event == "finding-disposition". For each record R where:
          R.disposition == "fixed" AND R.finding_id is in {{reverted_fix_ids}}:
          — Override R.disposition to "scope-reverted" in the assembled report data (do NOT mutate the raw ledger or {{build_log}}; apply the override only to the variables assembled here for the end-gate report).
          — IDEMPOTENCY GUARD: Before appending an override row, check whether a row with event == "scorecard-revert-reconciliation" AND finding_id == R.finding_id already exists in the ledger. If such a row already exists (e.g., from a prior Phase 5 re-assembly or resume), skip the append — the override was already recorded. Only append when no prior override row exists for this finding_id.
          — If no prior override row exists: Append an override row to the build ledger (append-only corrections per references/build-ledger.md):
            { event: "scorecard-revert-reconciliation", story_slug: R.story_slug, finding_id: R.finding_id, note: "disposition overridden from fixed to scope-reverted — fix was discarded by write-scope guard; reroute_stub_slug: {{reverted_fix_ids}}[R.finding_id].reroute_stub_slug", ts: NOW() }
          — Also append the same row to {{build_log}} for in-context consistency.
        Bind {{reconciled_finding_dispositions}} = the per-story disposition records with the overrides applied.
        Note: this reconciliation ensures the scorecard counts ONLY findings whose fixes actually reached the merged result. A fix that was reverted by scope discipline (write-scope guard discarded it) cannot be counted as fixed — the underlying defect was re-routed to a backlog stub via {{conductor_reverted_fixes}} at stage-3 time, but the overstate risk arises if the raw "fixed" disposition is used without cross-checking.
        SCOPE CLARIFICATION — this cross-check is load-bearing only for the partial-revert case (b) where the fix partially landed and disposition remains "fixed" in the raw record but the in-scope portion was insufficient (or as an end-gate safety net for any other edge case where a "fixed" record survived into the raw log while the fix was actually reverted). Full-revert case (a) findings are already written with disposition "scope-reverted" at stage-3 time — they never carry "fixed" in the raw record and so never satisfy the predicate above. Those entries are therefore already excluded from {{routine_auto_fixed_count}} without this cross-check. The reconciliation correctly handles both cases: full-reverts are excluded at source; partial-revert stragglers are caught here.

      {{routine_auto_fixed_count}} = count the set of finding_ids where: (a) the ledger has a finding-disposition row with disposition == "fixed" for that finding_id, OR the ledger has an avfl-finding row with disposition == "fixed" for that finding_id; AND (b) that finding_id is NOT in {{reverted_fix_ids}}. Use set semantics (cardinality of the set), not arithmetic subtraction — MINUS means "exclude from the set", not "subtract a count". This prevents over-subtraction when a finding_id in {{reverted_fix_ids}} was never counted as fixed in the first place (full-revert case where the raw record was written as scope-reverted, not fixed).
      {{dismissed_findings}}       = ledger rows where event == "finding-disposition" AND disposition == "dismissed" (must each carry non-empty dismissal_rationale; reject any without one and append { event: "conductor-warning", story_slug: R.story_slug, reason: "dismissed finding " + R.finding_id + " has empty or missing dismissal_rationale — excluded from dismissed_findings", ts: NOW() } to {{build_log}} and the build ledger).
      {{stories_built_count}}      = count of entries in {{merged}} (cross-checked against ledger rows where event == "story-terminal" AND outcome == "merged").
      {{blocked_stories}}          = stories never added to {{merged}} (quarantined, integrity-stopped, fix-budget-exhausted, or mid-flight-aborted); derive from the union of:
        (a) ledger rows where event == "story-terminal" AND outcome in {"blocked", "quarantined", "stranded"},
        (b) ledger rows where event == "contract-integrity-stop" (integrity-stopped stories never produce a story-terminal row),
        (c) ledger rows where event == "stage3-story-blocked",
        (d) ledger rows where event == "mid-flight-escalation" AND resolution == "branch-aborted".
        Apply supersession (latest row wins per story_slug) before computing this set.
        Exclude stories in {{merged}} from this set.
      {{quarantined_stories}}      = subset of {{blocked_stories}} sourced from ledger rows where event == "story-terminal" AND outcome == "quarantined".
      {{contract_integrity_stops}} = from ledger rows where event == "contract-integrity-stop" (cross-checked against Conductor in-memory state).
      {{mid_flight_escalations}}   = {{escalations}} — the Conductor-scoped accumulator (rehydrated from ledger rows with event in {"stage3-mid-flight-escalation", "mid-flight-escalation"} at step 2.0). This is the durable record of all mid-flight escalations raised during the build. Do NOT source from the per-story transient {{mid_flight_escalations}} reset in step 2.S3 — that variable is a within-story accumulator that resets each story and under-reports at Phase 5.
      {{high_risk_divergences}}    = ledger rows where event == "finding-disposition" AND disposition == "fixed" (post-reconciliation, NOT scope-reverted) AND severity in { critical, major } — these are the consequential divergences that were caught and resolved; they populate §03 of the report. Scope-reverted "fixes" are excluded from this set — they were NOT resolved, they were re-routed. Note: severity is carried on the finding-disposition row itself (written at append time from I.severity); the filter is now directly executable. "blocker" is not a valid severity value — the closed severity enum is critical | major | minor | low per finding-schema.md.
      {{undischarged_deferrals}}   = ledger rows where event == "coverage-deferral-undischarged" — these are deferred stories whose named integration scenario could not be found or did not pass; they are routine findings excluded from {{stakes_findings}} and must be surfaced explicitly in §05 so the developer can see them at the gate. Note: do NOT read from {{avfl_findings}} — use the durable ledger rows instead so undischarged deferrals survive session death. Non-routine stakes-class concerns from the discharge executor are recorded with event "avfl-finding" and are captured by Source 2 above — they are NOT included here to avoid double-rendering.
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
        §05     — Waved off & routine: {{dismissed_findings}} as a table (what flagged | why safe to leave); {{routine_auto_fixed_count}} as a single count sentence — NOT itemized. If {{undischarged_deferrals}} is non-empty, render a "Unresolved coverage deferrals" subsection: one row per entry showing story slug, named scenario, and failure reason — clearly flagged as unverified acceptance behavior requiring follow-up. This is the primary visibility surface for routine undischarged deferrals (excluded from §04 because they are routine, not stakes-class).
        §06     — How done is this, really? Two tables: live-vs-hollow. Explicit "what approving actually does" callout. If the sprint is a partial slice, state it plainly.
        §07     — Merge & push preview: commits/diffstat; exact approve sequence; "push is a separate confirmation."
        GATE    — Single control: Approve / Request Changes; copy-decision-as-prompt textarea; approve <button> disabled until every §04 card has been acknowledged AND has a selection (per renderer §6 paint() logic); if {{stakes_findings}} is empty, approve enables after gate choice is made (no forcing function for a clean build).

      Informational-only sections (render if non-empty, no developer action required):
        Mid-flight escalations: {{escalations}} — findings already raised during the build (sourced from the Conductor-scoped {{escalations}} accumulator, not the per-story transient), with their recorded disposition.
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
          (a) {{avfl_findings}} — AVFL post-merge findings (Phase 3); each has severity and disposition fields (normalized in step 3.3 (avfl_findings): fixed | residual | escalated).
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

    <check if="developer requests changes">

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- END-GATE CHANGE-WORKFLOW (REQUEST-CHANGES REDISPATCH LOOP)  -->
      <!-- One bounded pass over developer-specified fixer items;      -->
      <!-- no developer prompt inside the loop; re-render then return  -->
      <!-- to the same end-gate <ask> above.                           -->
      <!-- ═══════════════════════════════════════════════════════════ -->

      <note>REQUEST-CHANGES PATH. The developer has declined to approve and has submitted a change request. The Conductor now parses that request into discrete fixer items, runs one bounded autonomous pass over them using the directed-fixer machinery (momentum:dev fix-mode via the directed-fix-invocation-contract), re-renders the end-gate report, and returns control to the same end-gate ask above. The developer is never asked a follow-up question while the pass is running — they give the request once and the pass runs to completion. This is an autonomous loop with the Conductor as sole agent-spawning and git-mutation authority throughout.</note>

      <note>LOOP BOUND. The attempt bound for the change-workflow pass is {{MAX_FIX_ATTEMPTS}} (canonical value: 3, declared at step 2.S3). No additional canonical bound is declared here — all mentions of the retry limit in this section defer to the step 2.S3 declaration of {{MAX_FIX_ATTEMPTS}}. After {{MAX_FIX_ATTEMPTS}} fix attempts on a given item, remaining unresolved items are held as residuals and surfaced in the re-rendered report, then the loop returns to the gate without further looping. The Conductor does not loop indefinitely.</note>

      <note>GATE INVARIANT. This change-workflow path does NOT add a second mandatory human acceptance gate. It re-presents the SAME end-gate (the single mandatory human gate in Phase 5). The redispatch loop is: request received → parse → autonomous pass → re-render report → return to the Phase 5 <ask> above. The developer sees the gate again at the top of this same Phase 5 step. No new step is inserted.</note>

      <!-- ── 5.RC.1 — Parse change request into discrete fixer items ── -->

      <action>5.RC.1 — PARSE CHANGE REQUEST into discrete fixer items:
        Read the developer's full change-request text (the text they submitted at the gate).
        Parse it into a list {{endgate_fixer_items}} of discrete, independently addressable items:
          — Each item is a self-contained instruction or finding referencing a specific story, section,
            code location, report section, or acceptance concern.
          — Items separated by conjunctions ("and also"), numbered lists, bullet points, or commas
            each become a distinct entry.
          — Do NOT collapse the full request into a single monolithic entry; every separately named
            change must be its own item. Example: "fix the auth check in conductor.md and clean up
            the Phase 3 note" → two items.
          — If the request is a single non-separable instruction, {{endgate_fixer_items}} is a
            single-element list.
          — Bind {{endgate_fixer_items}} = the parsed list (minimum 1 entry).
        Assign each item a fixer_id: "endgate-fix-{N}" (N = 1-based index).
        Initialize {{endgate_fix_attempts}} = {} — per-item retry counter keyed by fixer_id.
        Initialize {{endgate_fix_dispositions}} = [] — per-item outcome records.
        Initialize {{endgate_fix_pass_count}} = 0 — total pass iterations in this change-workflow.
        Append to {{build_log}} and the build ledger at {{ledger_path}} per the standing rule:
        { event: "endgate-change-request-parsed", item_count: length({{endgate_fixer_items}}),
          items: {{endgate_fixer_items}}, ts: NOW() }.
      </action>

      <!-- ── 5.RC.2 — Autonomous change-workflow pass (bounded) ──────── -->

      <action>5.RC.2 — AUTONOMOUS CHANGE-WORKFLOW PASS:
        GIT WORKING CONTEXT INVARIANT: The end-gate runs post-merge in the MAIN session on the
        already-checked-out sprint branch (`sprint/{{sprint_slug}}`). There is no per-story worktree
        at end-gate time. All fixer edits, write-scope guard operations, and commit commands in this
        step operate directly in the main worktree on `sprint/{{sprint_slug}}`. This is a single
        declared invariant — never reasserted mid-loop with a git checkout call.

        Collect {{unresolved_endgate_items}} = all items in {{endgate_fixer_items}} not yet resolved
          (not yet in {{endgate_fix_dispositions}} with outcome "fixed" or "dismissed" or "triaged-out" or "residual").
        On the first pass: {{unresolved_endgate_items}} = {{endgate_fixer_items}} (all items).

        For each item I in {{unresolved_endgate_items}} (process as fan-out individual-agent spawns
        where items are independent; do NOT use TeamCreate):

          Determine {{endgate_item_writable_files}} for item I:
            — If I references a specific named story slug S: use {{writable_files}} as established for
              S at build time (the story's declared writable file set from step 2.1 STAGE-1). Enforce
              all write-scope constraints from the directed-fix-invocation-contract.
            — If I references a sprint-level artifact (e.g., Phase 5 report, AVFL findings,
              integration-level issue): use the sprint branch's touched files as the scope (files
              modified since the sprint branch diverged from main).
            — If scope cannot be determined from the item text: record I as disposition "triaged-out"
              with rationale "scope could not be determined from change request — item added to backlog
              for follow-up". Invoke momentum:triage with I's text as the stub. Skip the fixer spawn
              for this item; it is resolved without a fix attempt.

          Determine {{endgate_item_stakes_class}} for item I:
            COMMON CASE (routine-by-authorization): an ordinary change the developer requested and
            authorized at the gate is treated as routine and auto-applied autonomously. This is the
            default path and covers the vast majority of requested changes.
            STAKES-CLASS OVERRIDE: if the item text explicitly references a security, auth, isolation,
            irreversible, destructive, or high-blast-radius operation (e.g., "delete all", "drop table",
            "remove auth check", "force-push", "production deploy"), classify as the matching
            stakes_class ("security-auth-isolation", "irreversible-destructive", or
            "high-blast-radius-architecture"). Otherwise: "routine".
            Bind {{endgate_item_stakes_class}} = classified value.

          Spawn momentum:dev in fix-mode (individual-agent, NOT TeamCreate) for item I:
            Input:
              — directed_fix: {
                    findings: [
                      { finding_id: I.fixer_id,
                        summary: I.text,
                        stakes_class: {{endgate_item_stakes_class}},
                        legitimate: true,
                        severity: "major",
                        source: "developer-endgate-request",
                        location: (referenced story slug or file path if identifiable, else "sprint-level"),
                        detail: I.text }
                    ],
                    story_file: (referenced story slug or file path if identifiable, else "sprint-level"),
                    sprint_slug: "{{sprint_slug}}"
                  }
              — writable_files: {{endgate_item_writable_files}} (Conductor-side scope guard; not read by fixer from payload)
            Constraint passed to fixer: "Do not mutate git. Do not spawn build agents. Apply the
              requested change and return a per-finding disposition. Produce output only.
              WRITE-SCOPE: You may ONLY create or modify files listed in writable_files.
              FORBIDDEN: Do NOT edit any story's own spec file under .momentum/stories/ or its
              verification contract under .momentum/sprints/.
              FORBIDDEN: Do NOT edit any file outside the declared writable_files set.
              CROSS-ARTIFACT RULE: If the change targets a file outside writable_files, return
              disposition triaged-out so the Conductor can route a reconciliation stub."
            Invocation contract: skills/momentum/references/directed-fix-invocation-contract.md.
            MODE NOTE: The directed_fix wrapper is required — its presence is the mode-select gate in dev/workflow.md step 0. Without it, momentum:dev defaults to green-field build mode and ignores the finding.

          When the fixer returns its disposition for item I:

            CASE disposition == "fixed":
              — WRITE-SCOPE COMMIT GUARD (mirrors step 2.S3 Phase B guard exactly):
                Run `git diff --name-only` on the affected file set. For each modified file P not
                in {{endgate_item_writable_files}}: unstage and discard the edit
                (`git checkout -- P`) before committing.
                (All git commands operate in the main worktree on the already-checked-out
                `sprint/{{sprint_slug}}` branch — per the GIT WORKING CONTEXT INVARIANT above.)
              — Commit the applied fix (in-scope edits only):
                  `git add -u && git commit -m "fix(endgate): apply requested change — {I.text | truncate 60}"`
              — Record in {{endgate_fix_dispositions}}: { fixer_id: I.fixer_id, outcome: "fixed",
                  summary: I.text, commit: <sha> }
              — Remove I from {{unresolved_endgate_items}}.

            CASE disposition == "dismissed":
              — Validate non-empty rationale; if missing: re-present I on the next pass.
              — Record in {{endgate_fix_dispositions}}: { fixer_id: I.fixer_id, outcome: "dismissed",
                  summary: I.text, dismissal_rationale: <fixer's rationale> }
              — Remove I from {{unresolved_endgate_items}}.

            CASE disposition == "triaged-out":
              — Invoke momentum:triage with I's text and any context to create a backlog stub.
              — Record in {{endgate_fix_dispositions}}: { fixer_id: I.fixer_id, outcome: "triaged-out",
                  summary: I.text, triage_stub_slug: <returned slug> }
              — Remove I from {{unresolved_endgate_items}}.

            CASE disposition == "escalated":
              — This fires when the synthetic finding was classified as a non-routine stakes_class
                (security-auth-isolation, irreversible-destructive, or high-blast-radius-architecture).
                The fixer correctly declined to auto-apply it.
              — Route to {{end_gate_escalations}}: append { finding_id: I.fixer_id, stakes_class: {{endgate_item_stakes_class}},
                  timing_tier: (fixer's escalation.timing_tier, default "end-gate-expanded"),
                  summary: I.text, evidence: (fixer's escalation.evidence), suggested_fix: I.text }
                This entry will surface as a §04 decision card on the re-rendered end-gate report.
              — Record in {{endgate_fix_dispositions}}: { fixer_id: I.fixer_id, outcome: "escalated",
                  summary: I.text, stakes_class: {{endgate_item_stakes_class}} }
              — Remove I from {{unresolved_endgate_items}}.
              — Append to {{build_log}} and the build ledger at {{ledger_path}} per the standing rule:
                { event: "endgate-change-escalated", fixer_id: I.fixer_id, stakes_class: {{endgate_item_stakes_class}}, summary: I.text, ts: NOW() }

        Increment {{endgate_fix_pass_count}}.
        Append to {{build_log}} and the build ledger at {{ledger_path}} per the standing rule:
        { event: "endgate-change-workflow-pass", pass: {{endgate_fix_pass_count}},
          items_resolved_this_pass: (count of items removed from unresolved),
          items_remaining: length({{unresolved_endgate_items}}), ts: NOW() }.
      </action>

      <!-- ── 5.RC.3 — Retry gate (bounded) ───────────────────────────── -->

      <check if="{{unresolved_endgate_items}} is non-empty">
        <action>For each unresolved item I in {{unresolved_endgate_items}}:
          Increment {{endgate_fix_attempts}}[I.fixer_id].
        </action>

        <check if="any item in {{unresolved_endgate_items}} has {{endgate_fix_attempts}}[I.fixer_id] less than {{MAX_FIX_ATTEMPTS}}">
          <note>At least one item still has budget. Re-enter the pass (5.RC.2) with the unresolved items only. Do NOT re-present already-resolved items. The Conductor does not ask the developer anything during this re-entry — the loop is autonomous.</note>
          <action>Return to 5.RC.2 with {{unresolved_endgate_items}} (items whose budget is not yet exhausted).
            Do not re-include items that are already in {{endgate_fix_dispositions}}.
          </action>
        </check>

        <check if="all items in {{unresolved_endgate_items}} have {{endgate_fix_attempts}}[I.fixer_id] >= {{MAX_FIX_ATTEMPTS}}">
          <note>Fix budget exhausted for all remaining items. Mark each as residual — do NOT loop further. The unresolved items will appear in the re-rendered report as residual end-gate items requiring follow-up. This terminates the autonomous loop; control passes to the re-render step.</note>
          <action>For each item I in {{unresolved_endgate_items}}:
            Record in {{endgate_fix_dispositions}}: { fixer_id: I.fixer_id, outcome: "residual",
              summary: I.text, attempts: {{endgate_fix_attempts}}[I.fixer_id],
              note: "fix-budget exhausted — item carried forward as residual in re-rendered report" }
            Invoke momentum:triage with I's text to create a backlog stub so the item is not silently dropped.
            Append to {{build_log}} and the build ledger at {{ledger_path}} per the standing rule:
            { event: "endgate-fix-budget-exhausted", fixer_id: I.fixer_id, attempts: {{endgate_fix_attempts}}[I.fixer_id], summary: I.text, ts: NOW() }
          </action>
        </check>
      </check>

      <!-- ── 5.RC.4 — Commit change-workflow summary and re-render report ── -->

      <action>5.RC.4 — RE-RENDER THE END-GATE REPORT:
        Rendering authority: references/endgate-report-renderer.md — identical to the initial build.
        The re-render reproduces the same eight-section fixed-order contract, decision-card markup,
        and gate JS as the initial BUILD action, only ADDING the informational "Changes applied this pass"
        section described below.
        Re-assemble all end-gate report variables using the same logic as the initial report-build
        action above (the "BUILD THE END-GATE REPORT" action in Phase 5). Re-read from live state:
          — Re-assemble {{stakes_findings}} from {{end_gate_escalations}}, {{avfl_findings}},
            and {{e2e_findings}} (these are unchanged by the change-workflow pass; the pass
            targeted story-level or sprint-level code changes, not finding metadata).
          — Re-assemble supporting variables ({{routine_auto_fixed_count}}, {{dismissed_findings}},
            {{stories_built_count}}, {{blocked_stories}}, etc.) from live Conductor state.
          — Append a "Changes applied this pass" section to the report body: a summary table
            listing each item from {{endgate_fix_dispositions}}:
              columns: item # | change requested | outcome | commit (if fixed) | note (if residual or triaged-out)
            This section is informational. It shows the developer what the autonomous pass did.
          — If any items in {{endgate_fix_dispositions}} have outcome == "residual": add a
            "Residual change-request items" note in the report's §05 area listing the unresolved
            items with their triage stub slugs.
        Overwrite the same HTML file at `.momentum/handoffs/{{sprint_slug}}-endgate-report.html`
          (same path as the initial report; re-render in place).
        Append to {{build_log}} and the build ledger at {{ledger_path}} per the standing rule:
        { event: "endgate-report-re-rendered", pass: {{endgate_fix_pass_count}},
               items_fixed: count of "fixed" in {{endgate_fix_dispositions}},
               items_triaged_out: count of "triaged-out" in {{endgate_fix_dispositions}},
               items_residual: count of "residual" in {{endgate_fix_dispositions}} }
      </action>

      <action>5.RC.5 — OPEN THE RE-RENDERED REPORT in the viewer:
        Run: cmux browser new "file:///$(pwd)/.momentum/handoffs/{{sprint_slug}}-endgate-report.html" --workspace "$CMUX_WORKSPACE_ID" --focus false
        (The `--focus false` flag keeps the developer in context; the tab is available in the viewer pane.)
      </action>

      <!-- ── 5.RC.6 — Return to the end-gate ask (redispatch) ─────────── -->

      <note>REDISPATCH. The autonomous pass is complete and the report is re-rendered. The Conductor now returns control to the same end-gate ask above (the single Phase 5 ask: "approve or request changes"). This is not a new gate — it is the same gate re-presented with the updated report. The developer may now: (a) approve (proceeds to the approve branch above), or (b) submit another change request (re-enters this request-changes path for another bounded pass). There is no limit on how many times the developer may cycle through this gate, but each pass is bounded by {{MAX_FIX_ATTEMPTS}} per item internally.</note>

      <output>The requested changes have been applied (or carried forward as residuals where the fix budget was exhausted). The end-gate report has been re-rendered and is open in the viewer.

**Change pass summary:**
- Items fixed: {{count of "fixed" in endgate_fix_dispositions}}
- Items dismissed: {{count of "dismissed" in endgate_fix_dispositions}}
- Items triaged to backlog: {{count of "triaged-out" in endgate_fix_dispositions}}
- Items carried forward as residuals: {{count of "residual" in endgate_fix_dispositions}}

Review the updated report, acknowledge any decision cards in §04, then approve to merge to main, or request further changes.</output>

      <ask>The end-gate report is open in the viewer. Review each section. Acknowledge any decision cards in §04. Then approve to merge to main, or request changes.</ask>

    </check>
  </step>

</workflow>
