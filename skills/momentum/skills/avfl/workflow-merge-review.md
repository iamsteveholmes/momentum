# AVFL Merge Review Workflow

**Goal:** Review the net integrated change of a sprint branch versus main using a full dual-reviewer adversarial validation loop with a declining-skepticism auto-fix loop. Returns a typed `CLEAN | NON_CONVERGENT` result the Conductor consumes directly.

**Inputs (bound by caller before step 1):**
- `{{sprint_branch}}` — e.g. `sprint/sprint-2026-06-05-conduct-runnable`
- `{{base_ref}}` — the main branch reference, e.g. `main`
- `{{merged_stories}}` — array of `{slug, files_touched[]}` from the Conductor's merge log
- `{{story_contracts}}` — map from slug to verification contract path (used by the fixer for cross-story contradiction resolution)

**Constants (hardcoded — merge review is a single fixed config):**
- `LENSES = [structural, accuracy, coherence, domain]`
- `MAX_ITERATIONS = 4`
- `PASS_SCORE = 95`
- `SKEPTICISM = [3, 2, 2, 2]` — declining, floor 2 (per avfl-declining benchmark)

**Authority invariants:**
- This workflow NEVER asks the developer a question. It runs silently to completion and returns the typed result.
- The Conductor is the sole git-mutation authority. This workflow's fixer step produces file content and a commit message; the Conductor commits it.
- No subagent spawned by this workflow spawns further agents.

---

<workflow>

  <critical>This workflow never asks the developer anything. It runs silently to completion and returns a typed result object. No pause, no ask, no HALT.</critical>
  <critical>The Conductor owns all git mutations. The fixer step in this workflow produces corrected file content and a commit message label; it does NOT commit. The Conductor commits after receiving the fixer output.</critical>
  <critical>The typed result is either CLEAN (score >= 95) or NON_CONVERGENT (max iterations reached or oscillation detected). No other status. The Conductor acts on the typed result without re-parsing prose.</critical>
  <critical>Integration code findings (type == "integration", source == "avfl-merge-review") route to the directed fixer (momentum:dev fix-mode). The AVFL internal artifact fixer is NOT used for source-code integration findings. Doc/spec/skill-file findings use the AVFL internal fixer. Classify before dispatching.</critical>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- STEP 1: GATHER MERGE — capture 3-dot diff and context      -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="1" goal="Capture the net integrated change of the sprint branch vs. main">

    <action>Compute the merge base:
      Run: `git merge-base {{base_ref}} {{sprint_branch}}`
      Bind {{merge_base}} = the SHA returned.
    </action>

    <action>Capture the integrated diff (3-dot — net change the developer would ship):
      Run: `git diff {{merge_base}}...{{sprint_branch}}`
      Bind {{merged_diff}} = full diff output.
      Run: `git diff --name-only {{merge_base}}...{{sprint_branch}}`
      Bind {{changed_files}} = list of changed file paths.
    </action>

    <action>Capture the list of --no-ff merge commits that compose the integrated result:
      Run: `git log --merges {{merge_base}}..{{sprint_branch}} --oneline`
      Bind {{merge_commits}} = the list of merge commit lines.
    </action>

    <action>Identify the integration surface — files touched by more than one merged story (highest cross-story risk zone):
      For each file in {{changed_files}}: count how many story slugs in {{merged_stories}} include that file in their `files_touched` array.
      Bind {{integration_surface}} = files touched by more than one story.
    </action>

    <action>Initialize loop state:
      {{iteration}}       = 1
      {{current_diff}}    = {{merged_diff}}    (the content under review; updated by fixer each iteration)
      {{iteration_scores}} = []
      {{fix_log}}         = []
      {{fix_commits}}     = []
      {{prev_score}}      = null
      {{no_fix_last}}     = false
    </action>

  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- STEP 2: VALIDATE — parallel fan-out, 8 agents              -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="2" goal="Parallel dual-reviewer validation over all four lenses">

    <note>This step repeats each iteration. All 8 subagents are launched in a single message turn (fan-out). Each receives the current diff (updated after each fix pass), the merge context, and the current skepticism level. Model and effort per Role Configuration in the AVFL SKILL.md (Enumerator=sonnet/medium, Adversary=opus/high).</note>

    <action>Bind skepticism for this iteration:
      {{skepticism}} = SKEPTICISM[{{iteration}} - 1]
      (SKEPTICISM = [3, 2, 2, 2] — iteration 1 uses 3; iterations 2+ use 2)
    </action>

    <action>Read `references/framework.json` → `prompts` for the exact prompt templates to use for each validator type. Use `prompts.validator_system` and `prompts.validator_task` verbatim. Do not substitute or abbreviate.
    </action>

    <action>Spawn 8 validator subagents CONCURRENTLY (individual-agent fan-out, NOT TeamCreate).
      One Enumerator + one Adversary per lens. All 8 in a single message turn.

      Each validator receives:
        - lens: one of [structural, accuracy, coherence, domain]
        - reviewer_framing: Enumerator (systematic, section-by-section) OR Adversary (holistic, pattern-aware)
        - skepticism: {{skepticism}}
        - content_under_review: {{current_diff}}
        - context: {
            sprint_branch: "{{sprint_branch}}",
            base_ref: "{{base_ref}}",
            merge_commits: {{merge_commits}},
            integration_surface: {{integration_surface}},
            merged_stories: {{merged_stories}}
          }
        - instructions: "You are reviewing the NET INTEGRATED CHANGE of the sprint branch vs. {{base_ref}}.
            This diff spans ALL merged stories combined — you must look for cross-story integration defects
            that no single story review could see. Pay special attention to files in the integration surface
            (touched by >1 story). Each finding must include: id (LENS_ID-NNN), severity (critical|major|minor|low),
            dimension, location (file:section or file:line), description, evidence (quoted text — mandatory),
            suggestion, owning_stories (which story slugs are implicated). Findings without evidence are discarded."
        - domain_expert: "integration reviewer"
        - task_context: "Sprint branch net integrated diff across {{merged_stories | length}} merged stories"

      Constraint: "Do not mutate git. Do not spawn build agents. Return findings only."

      Sub-skill paths per role:
        Enumerator: sub-skills/validator-enum
        Adversary:  sub-skills/validator-adv

      Bind {{all_validator_outputs}} = array of all 8 validator result sets when the fan-out join completes.
    </action>

  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- STEP 3: CONSOLIDATE                                         -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="3" goal="Consolidate, deduplicate, score, and classify findings across all lenses">

    <note>Consolidator runs sequentially after all validators complete. Model: haiku/low. Sub-skill: sub-skills/consolidator. Use `prompts.consolidator` from framework.json verbatim.</note>

    <action>Spawn the consolidator subagent (individual-agent, NOT TeamCreate):
      Model: haiku. Sub-skill: sub-skills/consolidator.
      Inputs:
        - validator_outputs: {{all_validator_outputs}}
        - integration_surface: {{integration_surface}}
        - merged_stories: {{merged_stories}}
        - story_contracts: {{story_contracts}}
      Instructions:
        "1. Tag each finding: both reviewers found it -> HIGH confidence; only one -> MEDIUM.
         2. Merge all findings from all lenses into one list.
         3. Deduplicate: same issue from multiple sources -> keep most specific, highest severity.
         4. Investigate MEDIUM-confidence findings against story contracts. Keep if evidence supports; discard if hallucination.
         5. Remove any finding lacking evidence.
         6. CLASSIFY each surviving finding: INTEGRATION (implicates >1 story OR location is in integration_surface) | LOCAL (single-story).
         7. Populate owning_stories for each finding from the blame index and changed_files.
         8. Score: start 100, apply critical -15, major -8, minor -3, low -1.
         9. Sort: critical first, then location.
         10. Assign grade: >=95 Clean, >=85 Good, >=70 Fair, >=50 Poor, <50 Failing."
      Returns: { findings: [...], score: N, grade: string }
      Constraint: "Do not mutate git. Return consolidated findings only."

      Bind {{consolidated_findings}} = consolidator output findings.
      Bind {{score}} = consolidator output score.
    </action>

    <action>Append {{score}} to {{iteration_scores}}.</action>

  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- STEP 4: EVALUATE — typed exit conditions                    -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="4" goal="Evaluate exit conditions and determine whether to return CLEAN, fix, or return NON_CONVERGENT">

    <note>No developer interaction at this step. All exits are structural. Returns either the final typed result or proceeds to the fix step.</note>

    <check if="{{score}} >= 95">
      <action>Return CLEAN result:
        {
          "status": "CLEAN",
          "final_score": {{score}},
          "iterations": {{iteration}},
          "scores_per_iteration": {{iteration_scores}},
          "fixes_applied": {{fix_log}},
          "leftovers": [],
          "commits": {{fix_commits}}
        }
      </action>
      <note>CLEAN means the merged result meets the quality bar. The Conductor records this and proceeds to Phase 4 (E2E).</note>
    </check>

    <check if="{{score}} < 95 AND {{iteration}} >= MAX_ITERATIONS">
      <action>Return NON_CONVERGENT — max iterations reached:
        {
          "status": "NON_CONVERGENT",
          "reason": "max_iterations",
          "final_score": {{score}},
          "iterations": {{iteration}},
          "scores_per_iteration": {{iteration_scores}},
          "fixes_applied": {{fix_log}},
          "leftovers": {{consolidated_findings}}
            (each leftover carries: id, severity, confidence, classification, owning_stories,
             location, description, evidence, suggestion, why_unresolved: "max_iterations"),
          "commits": {{fix_commits}}
        }
      </action>
    </check>

    <check if="{{score}} < 95 AND {{no_fix_last}} == true AND {{score}} == {{prev_score}}">
      <action>Return NON_CONVERGENT — oscillation guard (no progress last iteration, score unchanged):
        {
          "status": "NON_CONVERGENT",
          "reason": "oscillation",
          "final_score": {{score}},
          "iterations": {{iteration}},
          "scores_per_iteration": {{iteration_scores}},
          "fixes_applied": {{fix_log}},
          "leftovers": {{consolidated_findings}}
            (each leftover carries: id, severity, confidence, classification, owning_stories,
             location, description, evidence, suggestion, why_unresolved: "oscillation"),
          "commits": {{fix_commits}}
        }
      </action>
    </check>

    <check if="{{score}} < 95 AND {{iteration}} < MAX_ITERATIONS AND NOT ({{no_fix_last}} == true AND {{score}} == {{prev_score}})">
      <note>Score below threshold, iterations remaining, no oscillation. Proceed to the fix step.</note>
      <action>Set {{prev_score}} = {{score}}. Proceed to step 5 (FIX).</action>
    </check>

  </step>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- STEP 5: FIX — route integration code vs. doc findings      -->
  <!-- ═══════════════════════════════════════════════════════════ -->

  <step n="5" goal="Apply fixes to the integrated result on the sprint branch, routing code findings to the directed fixer and doc findings to the AVFL artifact fixer">

    <note>The Conductor is the sole git-mutation authority. This step produces corrected file content. The Conductor commits after receiving this output. Fixes are applied to the live sprint branch (not a worktree) — the next validation iteration inspects the result of these fixes.</note>

    <action>Partition {{consolidated_findings}} into two groups:

      Group A — Integration code findings (route to directed fixer momentum:dev fix-mode):
        Criteria: finding.type == "integration" AND the location is a source-code file
          (not a .md, .yaml, .json spec/skill/doc file).

      Group B — Doc/spec/skill/artifact findings (route to AVFL internal artifact fixer):
        Criteria: all findings NOT in Group A — i.e., doc, spec, skill markdown, YAML/JSON schema files,
          or non-integration findings in source-code files.

      Bind {{code_findings}} = Group A.
      Bind {{doc_findings}}  = Group B.
    </action>

    <!-- ── Group A: Integration code findings → directed fixer ── -->

    <check if="{{code_findings}} is non-empty">
      <action>Spawn momentum:dev in fix-mode as a subagent (individual-agent, NOT TeamCreate).

        INVOCATION: Pass a directed_fix wrapper object so momentum:dev selects fix-mode (not green-field).
        The presence of the directed_fix key is the mode-select gate in dev/workflow.md step 0.
        Invocation contract: skills/momentum/references/directed-fix-invocation-contract.md.

        Input payload:
          directed_fix: {
            findings: {{code_findings}} (normalized to canonical finding schema; each finding carries finding_id, stakes_class, legitimate, summary, detail, evidence, suggested_fix),
            story_file: "sprint-integration/{{sprint_branch}}" (integration handle — identifies the context for cross-story scope checks),
            sprint_slug: "{{sprint_slug}}"
          }

        Constraint: "Do not mutate git. Do not spawn build agents. Apply fixes to the sprint branch working tree
          and return per-finding dispositions per the directed-fix-invocation-contract canonical output shape.
          For cross-story contradictions: resolve toward the higher-authority contract if resolvable;
          if both have equal authority or no contract exists for a story, return disposition: triaged-out
          so the Conductor can route a reconciliation note via momentum:triage.
          WRITE-SCOPE: You may only edit files implicated by the code findings. Do not edit story spec files
          or verification contracts."
        Returns: { mode: "fix", story_file: ..., dispositions: [ { finding_id, disposition, files_changed, dismissal_rationale, escalation } ] }

        The Conductor (not the fixer) commits any applied fixes after the fixer returns.
        Commit authority: the Conductor stages and commits the fixer's output per Phase 3 step 3.2.

        For each returned finding disposition D:
          - disposition == "fixed":
              Append to {{fix_log}}: { id: D.finding_id, iteration: {{iteration}}, severity: (look up in {{code_findings}} by finding_id), owning_stories: (look up), change: "applied by directed fixer", rationale: (look up suggested_fix) }
          - disposition == "dismissed":
              Record dismissal with D.dismissal_rationale; exclude from next-iteration findings.
          - disposition == "triaged-out":
              Carry forward to leftover findings; mark why_unresolved: "triaged-out (cross-artifact)" in final leftovers if max_iterations reached.
          - disposition == "escalated":
              Carry forward as a leftover finding; mark why_unresolved: "escalated (stakes-class — held for end-gate)" in final leftovers.
              The Conductor routes the escalation payload (D.escalation) to {{end_gate_escalations}} at Phase 3 step 3.3.
      </action>
    </check>

    <!-- ── Group B: Doc/spec/skill findings → AVFL artifact fixer ── -->

    <check if="{{doc_findings}} is non-empty">
      <action>Spawn the AVFL internal fixer (sub-skills/fixer) as a subagent (individual-agent, NOT TeamCreate):
        Model: sonnet. Sub-skill: sub-skills/fixer.
        Inputs:
          - findings: {{doc_findings}}
          - output_to_validate: {{current_diff}}
          - domain_expert: "integration reviewer"
          - story_contracts: {{story_contracts}}
          - authority_hierarchy: [story contracts in story_contracts by story merge order]
        Use `prompts.fixer` from framework.json verbatim.
        Constraint: "Do not commit. Produce corrected file content only. Return per-finding dispositions."
        Returns: corrected content per file + per-finding dispositions.

        For each returned finding:
          - disposition == "fixed": append to {{fix_log}} with iteration and change.
          - disposition == "dismissed": exclude from next iteration.
          - disposition == "unresolved_contradiction": carry forward per above.
      </action>
    </check>

    <action>Compose the fix commit message for the Conductor:
      Bind {{fix_commit_label}} = "fix(avfl): resolve integration findings — iteration {{iteration}}"
      (The Conductor commits using this label after staging all applied fixes.)
      Bind {{fix_commits_this_iter}} = [{{fix_commit_label}}]  (one commit per iteration).
      Append {{fix_commit_label}} to {{fix_commits}}.
    </action>

    <action>Update {{current_diff}} to reflect the fixed state:
      After the Conductor commits the fixer output to {{sprint_branch}}, recompute:
        Run: `git diff {{merge_base}}...{{sprint_branch}}`
        Bind {{current_diff}} = new diff output.
    </action>

    <action>Check whether any fix was applied this iteration:
      If {{fix_log}} gained no new entries during this fix step: set {{no_fix_last}} = true.
      Else: set {{no_fix_last}} = false.
    </action>

    <action>Increment iteration: {{iteration}} = {{iteration}} + 1.
      Return to step 2 (VALIDATE) for the next iteration.
    </action>

  </step>

</workflow>
