# momentum:dev Workflow

**Goal:** Implement a Momentum story (green-field build mode) or apply a directed fix and return a per-finding disposition map (fix-mode). Mode is determined by input: a `directed_fix` payload selects fix-mode; everything else is green-field build.

**Role:** Pure implementer. In green-field mode, receives a story, delegates all implementation to bmad-dev-story, and reports what was changed. In fix-mode, receives a set of findings from the Conductor, applies the stakes-class branch, and returns dispositions (fixed + files_changed, dismissed + rationale, triaged-out, or escalated + inline payload). The Conductor stages (under the write-scope guard) and commits all in-scope changes.

**Conductor owns everything else.** Worktree creation/lifecycle, lockfile handling, git mutation (merge, rebase, conflict resolution), worktree cleanup, crash recovery, and the mid-flight pause decision are all Conductor responsibilities (spec sections 3 and 6). The dev agent does not touch any of those concerns — adding them back here would break the Conductor's single-owner model and the precondition for mid-flight escalation (DEC-035, DEC-036 D1).

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all green-field implementation to that skill.</critical>
  <critical>The verification contract is a two-part file at `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (the `# === VERIFICATION HEADER` YAML block) as a self-check. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin, etc.) beyond sections explicitly referenced by `how_dev_self_checks`. Dev never writes, edits, appends to, or alters any part of the contract. Dev never chooses the verification method — it is given in Part A. Stakes classification and mid-flight escalation do not change this read surface; dev reads only Part A regardless of any stakes class or disposition active elsewhere in the flow.</critical>
  <critical>If the story does not have a Momentum Implementation Guide section, warn the user: the story was likely created with bmad-create-story directly rather than momentum:create-story. Offer to run the injection step manually before proceeding.</critical>
  <critical>Fix-mode disposition outcomes are mutually exclusive: a finding receives exactly ONE of fixed, dismissed, triaged-out, or escalated — never combined. For stakes-class findings (security-auth-isolation, irreversible-destructive, high-blast-radius-architecture), make zero edits and produce zero commits. Route on legitimate: legitimate:true → escalated (with inline payload); legitimate:false → dismissed (with non-empty rationale). A non-legitimate stakes-class finding is dismissed, never escalated.</critical>
  <critical>Fix-mode dismissed disposition always requires a non-empty dismissal_rationale. An empty or missing rationale is invalid and must not be produced.</critical>
  <critical>Fix-mode does not pause, block, or prompt the human. Emitting the timing_tier flag is the full extent of routing output. The Conductor owns the pause decision.</critical>

  <step n="0" goal="Detect operating mode — fix-mode or green-field build">
    <action>Check: does the input contain a `directed_fix` payload?</action>

    <check if="directed_fix payload is present">
      <action>Store {{mode}} = "fix"</action>
      <action>Store {{findings}} = directed_fix.findings (array of finding objects)</action>
      <action>Store {{story_file}} = directed_fix.story_file</action>
      <action>Store {{sprint_slug}} = directed_fix.sprint_slug</action>
      <output>> Fix-mode selected. Processing {{findings.length}} finding(s) for story `{{story_file}}`.</output>
      <action>Jump to Step 0.5 (fix-mode execution). Skip Steps 1–3 entirely — fix-mode does not invoke bmad-dev-story or perform a green-field build.</action>
    </check>

    <check if="no directed_fix payload">
      <action>Store {{mode}} = "green-field"</action>
      <output>> Green-field build mode selected. Proceeding to story resolution.</output>
      <action>Continue to Step 1 (story resolution for green-field build).</action>
    </check>
  </step>

  <step n="0.5" goal="Fix-mode: apply stakes-class branch to each finding">
    <action>Initialize {{disposition_map}} = empty array to collect per-finding results.</action>
    <action>For each finding in {{findings}}, apply the following branch logic:</action>

    <check if="finding.stakes_class is 'security-auth-isolation', 'irreversible-destructive', or 'high-blast-radius-architecture'">
      <action>STAKES-CLASS PATH: Make NO edits to any file. Produce NO commit.</action>

      <check if="finding.legitimate is true">
        <action>Build the escalation payload inline:
          - **what**: state clearly what issue was detected and where (from finding.summary, finding.detail, and finding.evidence)
          - **why**: explain why this finding is stakes-class and what the consequences of mis-handling are; name the specific stakes_class
          - **evidence**: include the concrete artifact excerpt from finding.evidence that substantiates the finding
          - **timing_tier**: assign `end-gate-expanded` by default; assign `mid-flight` ONLY if the finding is both irreversible-and-imminent (about to execute now, cannot be undone) OR build-invalidating (continuing would compound an invalid build state). Do not widen this bar — urgency alone or stakes class alone is insufficient for mid-flight.
        </action>
        <action>Append to {{disposition_map}}: { finding_id, disposition: "escalated", files_changed: [], dismissal_rationale: null, escalation: { what, why, evidence, timing_tier } }</action>
      </check>

      <check if="finding.legitimate is false">
        <action>DISMISSED PATH (stakes-class false positive): Do not edit any file. Compose a non-empty dismissal_rationale explaining specifically why this finding is not genuine despite its stakes-class label (false positive, misidentified scope, pre-existing known issue, etc.). An empty or missing rationale is invalid — do not produce one.</action>
        <action>Append to {{disposition_map}}: { finding_id, disposition: "dismissed", files_changed: [], dismissal_rationale: "{{non-empty explanation}}", escalation: null }</action>
      </check>

      <note>Escalation requires legitimate:true. A non-legitimate finding is dismissed even when stakes_class is non-routine — schema Rule 3 states non-legitimate findings are never escalated.</note>
    </check>

    <check if="finding.stakes_class is 'routine' AND finding.legitimate is true AND finding is in scope for this story">
      <action>ROUTINE FIX PATH: Apply the fix by editing the affected file(s) per finding.suggested_fix (or derive the fix from finding.summary, finding.detail, and finding.evidence if no suggested_fix is provided).</action>
      <action>Capture {{files_fixed}} = list of files edited in the working tree. Do not stage or commit — the Conductor stages and commits after the fixer returns.</action>
      <action>Append to {{disposition_map}}: { finding_id, disposition: "fixed", files_changed: [{{files_fixed}}], dismissal_rationale: null, escalation: null }</action>
    </check>

    <check if="finding.stakes_class is 'routine' AND finding.legitimate is false">
      <action>DISMISSED PATH: Do not edit any file. Compose a non-empty dismissal_rationale explaining specifically why this finding is not genuine (false positive, misidentified scope, pre-existing known issue, etc.). An empty or missing rationale is invalid — do not produce one.</action>
      <action>Append to {{disposition_map}}: { finding_id, disposition: "dismissed", files_changed: [], dismissal_rationale: "{{non-empty explanation}}", escalation: null }</action>
    </check>

    <check if="finding.stakes_class is 'routine' AND finding.legitimate is true AND finding is out of scope for this story">
      <action>TRIAGED-OUT PATH: Do not edit any file. Record that this finding is legitimate but out of scope. It will be tracked separately via momentum:triage and is not silently dropped.</action>
      <action>Append to {{disposition_map}}: { finding_id, disposition: "triaged-out", files_changed: [], dismissal_rationale: null, escalation: null }</action>
    </check>

    <action>After processing all findings, emit the fix-mode output signal:</action>
    <output>
```
AGENT_OUTPUT_START
{
  "mode": "fix",
  "story_file": "{{story_file}}",
  "dispositions": {{disposition_map}}
}
AGENT_OUTPUT_END
```
Where {{disposition_map}} is the array of per-finding disposition objects built above. Each escalated finding has a fully populated escalation object including timing_tier; each fixed finding has files_changed populated; each dismissed finding has a non-empty dismissal_rationale.
    </output>
    <action>HALT. Fix-mode is complete. The Conductor owns all routing from here — including whether and when to surface mid-flight escalations to the human.</action>

    <note>Fix-mode contract reference: `skills/momentum/references/directed-fix-invocation-contract.md` — see §"Canonical Fixer Output Shape" for the authoritative per-finding object schema. Fix-mode finding schema: `skills/momentum/references/finding-schema.md`. Dispositions vocabulary: fixed | dismissed (non-empty rationale required) | triaged-out | escalated. Timing tiers: end-gate-expanded (default) | mid-flight (narrow: irreversible-and-imminent OR build-invalidating ONLY). The mutual exclusivity invariant: a finding receives exactly one disposition; a fix and an escalation are never both produced for the same finding. Shape invariant: `timing_tier` is ALWAYS nested inside the `escalation` object — never at the top level of the disposition object. `stakes_class` and `summary` are NOT echoed in the disposition object; the Conductor recovers them by joining on `finding_id` to the inbound findings it provided.</note>
  </step>

  <step n="1" goal="Resolve story to develop (green-field only)">
    <action>Check: has the user provided an explicit story file path or story key?</action>

    <check if="explicit story path or key provided">
      <action>If a file path is provided, store {{story_file}} = the provided path</action>
      <action>Read `.momentum/stories/index.json`</action>
      <action>If a story key is provided, look up {{story_key}} in stories/index.json. The story implementation file is at `.momentum/stories/{{story_key}}.md`. If a file path was provided, derive the story key from the filename.</action>
      <action>Store {{story_key}} and {{story_file}}</action>
    </check>

    <check if="no story path or key provided">
      <action>Read `.momentum/stories/index.json`</action>
      <action>Parse all story entries: each entry has slug (the key), status, depends_on, touches</action>
      <action>Filter to candidate stories: `status == "ready-for-dev"` AND every slug in `depends_on` has `status == "done"` in the same index</action>
      <check if="no candidates found">
        <action>Build a status summary: (1) for each story with status `in-progress`, list it as 'in progress in another session'; (2) for each story with status `ready-for-dev` whose `depends_on` includes any key not yet `done`, list: key → blocked on [list of incomplete depends_on keys]. If a depends_on key is `in-progress`, note it as `in-progress (will unblock when done)`.</action>
        <output>## No Unblocked Stories Available

> Resolve blocking stories first, then re-invoke `momentum:dev`.

**Current story status:**
[status summary]</output>
        <action>HALT</action>
      </check>
      <action>From the candidates, select the highest-priority story using this order:
        1. Epic sprint assignment: Day 1 stories first, then Sprint 1, Sprint 2, Growth
        2. Story order within that epic (parse from key: `1-2-...` → epic 1, story 2)
      </action>
      <action>Store {{story_key}} = selected story key</action>
      <action>Store {{story_file}} = `.momentum/stories/{{story_key}}.md`.</action>
      <output>> Selected story `{{story_key}}` (status: `ready-for-dev`, depends_on satisfied). Proceeding to develop.</output>
    </check>

  </step>

  <step n="2" goal="Invoke bmad-dev-story">
    <action>Invoke the `bmad-dev-story` skill. Pass the story file path ({{story_file}}). bmad-dev-story will read the story's Dev Notes — including the Momentum Implementation Guide section — and implement accordingly.</action>

    <action>Wait for bmad-dev-story to complete fully (story status = "review")</action>
    <action>After bmad-dev-story completes, capture:
      - {{story_key}}: the story key
      Then read {{story_file}} and extract:
      - {{file_list}}: from the story's File List section — files created/modified/deleted
      - {{tests_run}}: true if bmad-dev-story ran tests, false otherwise (from the Dev Agent Record or implementation output)
      - {{test_result}}: "pass", "fail", or "not_run" — the outcome of the test run (from the same source; use "not_run" if {{tests_run}} is false)
    </action>

    <note>bmad-dev-story handles: story loading, sprint tracking, review continuation detection, task implementation loop, definition-of-done gate, story transition to review status. The Momentum Implementation Guide in the story tells it to use EDD for skill-instruction tasks rather than TDD.</note>
    <note>Working directory: the Conductor creates the story branch (`story/{slug}` forked from `sprint/{{sprint_slug}}`) and the worktree (`.worktrees/story-{slug}`) at story launch (conductor workflow step 2.1, STAGE-1 DEV SPAWN block) immediately before spawning this agent. The dev agent is spawned already scoped to that worktree and writes within it. The Conductor stages (under the write-scope guard) and commits (conductor/workflow.md stage-1 sequence). The dev agent neither creates nor enters/exits worktrees, and it does not commit.</note>
  </step>

  <step n="2.5" goal="Part-A header self-check">
    <action>Locate the story's verification contract. Derive the sprint slug from context or read `.momentum/sprints/index.json` to find the active sprint. Look up the story's `verification_method` from the sprint assignment record (`.momentum/sprints/index.json` or the assignment JSON); the extension maps 1:1: eval_yaml→.eval.yaml, smoke_sh→.smoke.sh, trigger_md→.trigger.md, review_md→.review.md, gherkin→.feature. If the verification_method is unavailable, glob `.momentum/sprints/{sprint-slug}/specs/{{story_key}}.*` and take the single matching file (expect 0 or 1 result).</action>

    <check if="contract file exists AND contains a Part-A header (line starting with '# === VERIFICATION HEADER')">
      <action>Read the Part-A header block only — the YAML front-matter from `# === VERIFICATION HEADER` through the end of the YAML block. Extract the `how_dev_self_checks` prompt. Note: `how_dev_self_checks` is Part A's plain-language restatement of the observable acceptance target. It may explicitly reference observable clauses in the contract body (e.g., "the scenarios below") — those referenced clauses are Part-A-sanctioned and form part of your acceptance target alongside the prompt itself.</action>
      <action>Self-check: execute the directives in `how_dev_self_checks` against the just-built implementation in the current worktree, including any observable clauses the prompt explicitly references in the contract body. Hold the full acceptance target (prompt + any referenced clauses) alongside the story's plain-English ACs. Do not read beyond the sections explicitly referenced — the verifier body as a whole (scenarios not referenced by the prompt, assertion scripts, Gherkin) remains off-limits.</action>
      <output>**Part-A self-check:** Performed. `how_dev_self_checks` prompt executed; implementation satisfies all Part-A header requirements.</output>
      <action>Store {{part_a_self_check}} = "performed"</action>
    </check>

    <check if="no contract file found OR file has no Part-A header">
      <output>**Part-A self-check:** Skipped — no contract or no Part-A header available. Proceeding on story ACs.</output>
      <action>Store {{part_a_self_check}} = "skipped-no-contract"</action>
    </check>

    <note>Dev reads the Part-A header and any observable clauses explicitly referenced by `how_dev_self_checks`. Never read the verifier body beyond those referenced sections. Never write, edit, or alter any part of the contract. Stakes classification and mid-flight escalation do not change this read surface.</note>
    <note>No EnterWorktree/ExitWorktree is needed — the Conductor already scoped this agent to the story worktree. The self-check inspects the just-built implementation in the current working directory automatically.</note>
  </step>

  <step n="3" goal="Report implementation-complete">
    <output>## Story `{{story_key}}` — Implementation Complete

**Files changed:**
{{file_list}}

Implementation is done. The Conductor handles merge, worktree cleanup, and any recovery from here.
    </output>

    <action>Emit the structured completion signal:
```
AGENT_OUTPUT_START
{
  "status": "complete",
  "story_key": "{{story_key}}",
  "files_changed": [{{file_list}}],
  "part_a_self_check": "{{part_a_self_check}}",
  "test_results": {
    "tests_run": {{tests_run}},
    "outcome": "{{test_result}}"
  }
}
AGENT_OUTPUT_END
```
Where {{file_list}} is the comma-separated list of files from the story's File List section; {{part_a_self_check}} is "performed" or "skipped-no-contract" from Step 2.5; {{tests_run}} is true|false and {{test_result}} is "pass", "fail", or "not_run" — all captured in Step 2 from bmad-dev-story's Dev Agent Record.

If implementation failed (bmad-dev-story did not reach story status "review"), emit the failed variant instead. Populate files_changed with whatever files were changed in the worktree before the failure (check `git status` / `git diff --name-only`); use an empty array only if no files were modified:
```
AGENT_OUTPUT_START
{
  "status": "failed",
  "story_key": "{{story_key}}",
  "error": "{{error_description}}",
  "files_changed": [{{files_changed_before_failure_or_empty}}],
  "part_a_self_check": "{{part_a_self_check}}",
  "test_results": {
    "tests_run": false,
    "outcome": "not_run"
  }
}
AGENT_OUTPUT_END
```
    </action>

    <note>Terminal contract: implementation-complete + file_list. Nothing more. The Conductor owns all git mutation (merge, rebase, conflict resolution), worktree lifecycle, lockfile handling, and crash recovery per spec sections 3 and 6. Relocating those authorities out of dev is the precondition for the Conductor to own the narrow, stakes-gated mid-flight escalation tier (DEC-036 D1).</note>
  </step>

</workflow>
