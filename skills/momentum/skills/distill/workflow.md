# Distill Workflow

**Goal:** Immediately capture a session learning and apply it to the appropriate practice artifact —
rules, references, or skill prompts — without sprint activation or backlog ceremony.

**The practice gap distill closes:** Small, obvious practice improvements should land in minutes,
not weeks. Distill is the practice-artifact analogue of `/momentum:quick-fix`.

**Invoked by:** Developer directly (`/momentum:distill`) or from retro Phase 5 for Tier 1 findings.

---

<workflow>
  <critical>Orchestrator purity (Decision 3d): This workflow MUST NOT write files directly. Every file change goes through a spawned write subagent. The orchestrator reads, routes, presents, and delegates — it never contains direct Edit/Write actions on practice files.</critical>
  <critical>Discovery before write: Enumerator and Adversary agents MUST complete before any write subagent is spawned. Path classification and Tier determination happen in discovery, not post-hoc.</critical>
  <critical>No direct-invocation workarounds: Distill ALWAYS spawns subagents. The orchestrator does not perform the write itself, even for trivial single-line additions.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: DISCOVER                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Discover — spawn Enumerator and Adversary in parallel to classify scope and tier">

    <action>If invoked directly (not from retro Phase 5), ask the developer to describe the learning:
      - What did you observe or learn in this session?
      - Which practice artifact do you think needs updating (rule file, reference, skill prompt)?
      - Do you have a draft of the change, or should the agents derive it?

    Store {{learning_description}} and {{candidate_artifact}} from the developer's response.
    If invoked from retro Phase 5, {{learning_description}} and {{candidate_artifact}} are passed in
    from the retro finding — do not ask again.
    </action>

    <action>Determine the current working directory and the Momentum project path:
      - Run `git rev-parse --show-toplevel` to get {{project_root}}
      - Check if {{project_root}} contains `skills/momentum/.claude-plugin/plugin.json`
        → If yes: this IS the Momentum project → store {{is_momentum_project}} = true
        → If no: this is an external project → store {{is_momentum_project}} = false
      - If {{is_momentum_project}} = false, note the Momentum install path:
        check `~/.claude/plugins/momentum/` or similar standard paths for Momentum's own files
    </action>

    <action>Spawn two parallel discovery agents (model: claude-sonnet-4-6, effort: medium):

      **Enumerator agent** — system prompt:
      ```
      You are the Enumerator for a practice artifact distillation discovery pass.

      Learning to distill: {{learning_description}}
      Candidate artifact: {{candidate_artifact}}
      Project root: {{project_root}}
      Is Momentum project: {{is_momentum_project}}

      Your job:
      1. Read the candidate artifact (and neighboring artifacts if relevant) to map existing content.
      2. Identify WHERE specifically the learning would land — which section, after which entry,
         in what format (rule sentence, reference entry, prompt addition, etc.).
      3. Draft the proposed change: the exact text to add or modify.
      4. Classify the fix PATH:
         - Path A: learning applies to a project-local artifact (.claude/rules/, project references)
         - Path B: learning applies to Momentum's own practice files AND we are IN the Momentum project
         - Path C: learning applies to Momentum's own practice files AND we are in an EXTERNAL project
      5. Classify the fix TIER:
         - Tier 1: small, immediately applicable — single rule sentence, reference entry update,
           or prompt clarification. One file, minimal change.
         - Tier 2: structural — multi-file change, new skill, workflow redesign, or anything
           requiring spec-level deliberation.

      Return structured output:
      {
        "proposed_change": "<exact text to add/modify>",
        "target_file": "<absolute path to the file>",
        "target_section": "<section heading or location description>",
        "insertion_context": "<the text BEFORE the insertion point, for exact placement>",
        "path": "A" | "B" | "C",
        "tier": 1 | 2,
        "rationale": "<why this location and tier>"
      }
      ```

      **Adversary agent** — system prompt:
      ```
      You are the Adversary for a practice artifact distillation discovery pass.

      Learning to distill: {{learning_description}}
      Candidate artifact: {{candidate_artifact}}
      Project root: {{project_root}}
      Is Momentum project: {{is_momentum_project}}

      Your job — challenge the proposed distillation for three failure modes:
      1. REDUNDANCY: Is this learning already stated elsewhere? Search broadly — rules files,
         reference documents, skill prompts, workflow steps. Quote the existing text if found.
      2. CONFLICT: Does this learning contradict or create ambiguity with existing guidance?
         Identify the specific conflict and its scope.
      3. SCOPE FIT: Is the right artifact targeted? Would this learning be better placed in a
         different rule file, a different reference, or as a workflow step change?

      Also confirm or challenge the Tier classification:
      - Tier 1 requires: single-file, single-section, single-sentence-ish addition.
        If the change ripples to multiple files or requires cross-artifact consistency work → Tier 2.
      - Tier 2 heuristics: multi-file coordination, new skill needed, workflow step modification,
        or the change is load-bearing for other guidance that must also be updated.

      Return structured output:
      {
        "redundancy": { "found": true|false, "evidence": "<quote or null>" },
        "conflict": { "found": true|false, "description": "<description or null>" },
        "scope_fit": { "correct": true|false, "alternative": "<better target or null>" },
        "tier_challenge": { "upholds_tier_1": true|false, "reason": "<reason if challenging>" },
        "overall_verdict": "proceed" | "revise" | "block",
        "verdict_rationale": "<why>"
      }
      ```
    </action>

    <action>Wait for both agents to return. Store:
      {{enumerator_output}} = Enumerator's structured output
      {{adversary_output}} = Adversary's structured output
    </action>

    <action>Reconcile outputs:
      - If adversary verdict is "block": present findings to developer and HALT unless developer overrides.
      - If adversary verdict is "revise": incorporate scope/target correction into {{enumerator_output}}.
      - If adversary tier_challenge.upholds_tier_1 = false: escalate to Tier 2 regardless of Enumerator classification.
      - Final {{path}} = enumerator_output.path (or scope_fit.alternative if adversary corrected it)
      - Final {{tier}} = min(enumerator tier, adversary challenge outcome)
      - Final {{target_file}} = enumerator_output.target_file
      - Final {{proposed_change}} = enumerator_output.proposed_change
    </action>

    <output>Discovery complete.

Learning: {{learning_description}}
Proposed change: {{proposed_change}}
Target file: {{target_file}}
Target section: {{enumerator_output.target_section}}
Path: {{path}} ({{path_label}})
Tier: {{tier}}

Adversary findings:
  Redundancy: {{adversary_output.redundancy.found}} {{#if adversary_output.redundancy.evidence}}— "{{adversary_output.redundancy.evidence}}"{{/if}}
  Conflict: {{adversary_output.conflict.found}} {{#if adversary_output.conflict.description}}— {{adversary_output.conflict.description}}{{/if}}
  Scope fit: {{adversary_output.scope_fit.correct}} {{#if adversary_output.scope_fit.alternative}}→ better target: {{adversary_output.scope_fit.alternative}}{{/if}}
  Verdict: {{adversary_output.overall_verdict}}

Proceed with this change?</output>

    <ask>Approve (A), revise description (R), or cancel (C)?</ask>

    <check if="developer cancels">
      <action>HALT — no changes made. Optionally write ledger entry with disposition: cancelled.</action>
    </check>

    <check if="developer requests revision">
      <action>Update {{learning_description}} with developer's revision. Re-run Phase 1 discovery.</action>
    </check>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: ROUTE                                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Route — branch on Path A / B / C and Tier 1 / Tier 2">

    <check if="tier == 2">
      <output>Tier 2 classification: this change requires a story stub rather than direct application.

Reason: {{adversary_output.tier_challenge.reason | default: enumerator_output.rationale}}

A story stub will be created in `_bmad-output/implementation-artifacts/stories/` for sprint
activation. No practice files will be modified in this session.</output>
      <action>Proceed directly to Phase 3 (Tier 2 path — create story stub).</action>
    </check>

    <check if="tier == 1 and path == 'C'">
      <output>Path C: this learning applies to Momentum's practice files, but the current project
is NOT the Momentum project.

Distill cannot modify Momentum files from an external project. Choose:
  D — Defer to retro: record in findings-ledger for next retro cycle
  G — Generate remote prompt: produce a self-contained prompt to paste into a Momentum session</output>
      <ask>Choose D or G:</ask>
      <action>Store {{path_c_choice}} = developer's choice (D or G)</action>
      <action>Route to appropriate Phase 3 sub-path for Path C.</action>
    </check>

    <check if="tier == 1 and path == 'A'">
      <output>Path A: project-local change — {{target_file}}
Applying immediately via write subagent. Continuing to Phase 3.</output>
    </check>

    <check if="tier == 1 and path == 'B'">
      <output>Path B: Momentum-level change in the Momentum project — {{target_file}}
Will bump plugin patch version after applying. Continuing to Phase 3.</output>
    </check>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: APPLY                                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Apply — spawn write subagent (Tier 1) or create-story subagent (Tier 2)">

    <check if="tier == 2">
      <action>Spawn `momentum:create-story` (model: sonnet, effort: medium) with:
        - Title: derived from {{learning_description}} (kebab-case slug, descriptive)
        - epic_slug: "impetus-core" for Momentum/practice findings, or appropriate project epic
        - change_type: determined from the nature of the change (skill-instruction, script-code, etc.)
        - Description: {{learning_description}}
        - Acceptance criteria: derived from Enumerator's proposed_change and rationale
        - Source: "distill — Tier 2 escalation"
        - touches: [{{target_file}}] plus any additional files Adversary identified
      </action>
      <action>Store {{story_file}} from create-story output</action>
      <output>Story stub created: {{story_file}}
The finding has been captured as a backlog story for sprint activation.
Proceeding to Phase 6 (Ledger).</output>
      <action>Skip to Phase 6 — no AVFL or commit for Tier 2 path.</action>
    </check>

    <check if="tier == 1 and path == 'C' and path_c_choice == 'D'">
      <output>Deferring to retro — writing findings-ledger entry with origin: distill.
No Momentum files modified in this session.</output>
      <action>Skip to Phase 6 — ledger-only entry for Path C defer.</action>
    </check>

    <check if="tier == 1 and path == 'C' and path_c_choice == 'G'">
      <output>Generating remote prompt for Momentum session application.

---
## Remote Distill Prompt

**Copy and paste the following into a `/momentum:distill` session in the Momentum project:**

---
Learning to distill: {{learning_description}}

Target file: {{target_file}}
Target section: {{enumerator_output.target_section}}

Proposed change:
{{proposed_change}}

Instructions: Apply this learning directly using `/momentum:distill`. The Enumerator and
Adversary discovery pass has already been run — the proposed change is ready for application
as a Tier 1 Path B distillation.
---

Findings-ledger entry will be written with disposition: remote-prompt-generated.</output>
      <action>Skip to Phase 6 — ledger-only entry for Path C generate.</action>
    </check>

    <check if="tier == 1 and (path == 'A' or path == 'B')">
      <action>Spawn a write subagent (model: claude-sonnet-4-6, effort: medium) with:

        System prompt:
        ```
        You are a precision write agent for practice artifact distillation.

        Your job: apply exactly ONE change to exactly ONE file. Do not explore,
        do not make adjacent improvements, do not modify anything not specified.

        File to modify: {{target_file}}
        Section: {{enumerator_output.target_section}}
        Insertion context (text BEFORE insertion point): {{enumerator_output.insertion_context}}
        Change to apply: {{proposed_change}}

        Steps:
        1. Read {{target_file}} to confirm insertion context exists.
        2. Apply the change at the exact location specified.
        3. Write the updated file.
        4. Confirm: output the exact diff of what changed (before/after lines).

        Do not add explanatory comments. Do not modify surrounding content.
        Do not fix unrelated issues you notice. Apply exactly the specified change.
        ```
      </action>

      <action>Wait for write subagent to complete. Verify {{target_file}} was modified.</action>
      <output>Change applied to {{target_file}}.</output>
    </check>

    <check if="path == 'B'">
      <action>Bump the plugin patch version:
        1. Read `skills/momentum/.claude-plugin/plugin.json`
        2. Parse the current version (e.g., "0.4.2")
        3. Increment patch: "0.4.2" → "0.4.3"
        4. Spawn a write subagent to update the version field in plugin.json
      </action>
      <output>Plugin version bumped to {{new_version}}.</output>
    </check>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: VALIDATE                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Validate — invoke momentum:avfl with distill profile on changed files (Tier 1 only)">

    <check if="tier == 2 or (path == 'C')">
      <action>Skip Phase 4 — AVFL validation only runs for applied changes (Tier 1, Path A or B).</action>
    </check>

    <check if="tier == 1 and (path == 'A' or path == 'B')">
      <action>Invoke `momentum:avfl` with:
        - profile: distill
        - output_to_validate: content of {{target_file}} (the modified file only)
        - source_material: {{learning_description}} + {{proposed_change}}
        - domain_expert: "practice artifact reviewer"
        - task_context: "Distill validation — {{target_file}}"
        - stage: final
      </action>

      <check if="AVFL returns findings">
        <output>AVFL distill validation found issues in {{target_file}}:

{{avfl_findings}}

Choose:
  C — Correct: apply suggested corrections, then commit
  K — Keep as-is: commit without corrections (document findings as known)</output>
        <ask>Correct or keep?</ask>

        <check if="developer chooses correct">
          <action>Spawn a write subagent to apply AVFL corrections to {{target_file}}</action>
          <output>Corrections applied. Proceeding to commit.</output>
        </check>

        <check if="developer chooses keep">
          <output>Proceeding to commit without corrections. Findings noted.</output>
        </check>
      </check>

      <check if="AVFL returns clean">
        <output>AVFL distill validation clean. Proceeding to commit.</output>
      </check>
    </check>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: COMMIT                                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Commit changes and present push summary">

    <check if="tier == 2">
      <action>Commit the story stub file:
        `git add {{story_file}}`
        `git commit -m "docs(stories): distill — {{story_slug}} [Tier 2]"`
      </action>
      <output>Story stub committed. No practice files modified.</output>
    </check>

    <check if="tier == 1 and path == 'A'">
      <action>Commit the practice artifact change:
        `git add {{target_file}}`

        Derive commit type from file type:
          - `.claude/rules/*.md` → `feat(rules): distill — {{one_line_summary}}`
          - `skills/*/references/*.md` or `skills/*/references/*.json` → `feat(references): distill — {{one_line_summary}}`
          - `skills/*/SKILL.md` or `skills/*/workflow.md` → `feat(skills): distill — {{one_line_summary}}`
          - Default → `feat(practice): distill — {{one_line_summary}}`

        `git commit -m "{{commit_type}}: distill — {{one_line_summary}}"`
      </action>
      <output>Practice artifact committed (Path A).</output>
    </check>

    <check if="tier == 1 and path == 'B'">
      <action>Commit both the practice artifact change and the version bump:
        `git add {{target_file}} skills/momentum/.claude-plugin/plugin.json`

        Derive commit type as per Path A rules above.

        `git commit -m "{{commit_type}}: distill — {{one_line_summary}}

- feat(skills): apply distill change to {{target_file}}
- chore(plugin): bump version to {{new_version}}"`
      </action>

      <action>Present push summary:
        `git log @{u}..HEAD --oneline`
      </action>

      <output>Practice artifact committed (Path B — Momentum-level change).

Commits ready to push:
{{push_summary}}

Push to remote?</output>

      <ask>Push (Y/N)?</ask>

      <check if="developer confirms push">
        <action>Run: `git push`</action>
        <output>Pushed.</output>
      </check>

      <check if="developer declines push">
        <output>Commits held locally. Push when ready.</output>
      </check>
    </check>

    <check if="path == 'C'">
      <output>No files committed — Path C does not modify project files.</output>
    </check>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: LEDGER                                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Write findings-ledger entry with origin: distill">

    <action>Determine ledger path: `~/.claude/momentum/findings-ledger.jsonl`
    If the file does not exist, it will be created on first write.
    </action>

    <action>Determine disposition and artifact for ledger entry:
      - Tier 1, Path A or B, applied: artifact = {{target_file}}, disposition = "applied"
      - Tier 1, Path C, defer: artifact = null (Momentum target not in this project), disposition = "deferred"
      - Tier 1, Path C, remote prompt: artifact = null, disposition = "remote-prompt-generated"
      - Tier 2: artifact = {{story_file}}, disposition = "stubbed"
    </action>

    <action>Spawn a write subagent to append the ledger entry:

      System prompt:
      ```
      You are a ledger write agent. Append exactly one JSON line to a JSONL file.

      Ledger file: ~/.claude/momentum/findings-ledger.jsonl
      If the file does not exist, create it.

      Entry to append (write as a single minified JSON line, no trailing comma):
      {
        "timestamp": "{{iso_8601_now}}",
        "origin": "distill",
        "artifact": {{artifact_json}},
        "learning": "{{learning_description}}",
        "tier": {{tier}},
        "path": "{{path}}",
        "disposition": "{{disposition}}"
      }

      Do not modify any existing lines. Append only.
      ```
    </action>

    <output>Distill complete.

Summary:
  Learning: {{learning_description}}
  Artifact: {{artifact_or_story_or_null}}
  Path: {{path}} | Tier: {{tier}} | Disposition: {{disposition}}
  Ledger: ~/.claude/momentum/findings-ledger.jsonl updated

{{#if disposition == 'applied'}}Practice updated and committed.{{/if}}
{{#if disposition == 'stubbed'}}Story stub created: {{story_file}}{{/if}}
{{#if disposition == 'deferred'}}Finding deferred — will surface at next retro.{{/if}}
{{#if disposition == 'remote-prompt-generated'}}Remote prompt generated above — paste into a Momentum session to apply.{{/if}}
</output>

  </step>

</workflow>
