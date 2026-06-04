<workflow>

  <critical>
    This adapter is PURE TRANSPORT. It carries findings from bmad-code-review to the Conductor.
    It NEVER mutates any tracked file in the working tree. It NEVER applies fixes. It NEVER
    writes to the story file, deferred-work.md, or any other project file. The Conductor owns
    all git mutation; the adapter owns none.
  </critical>

  <critical>
    This adapter NEVER pauses for human input. Every HALT, confirmation prompt, and "wait for
    user" instruction in the underlying bmad-code-review step files is suppressed. The run
    proceeds from start to finish unattended. If a step in the underlying tool would normally
    HALT, the adapter auto-resolves it using the inputs already provided and continues.
  </critical>

  <critical>
    The adapter is scoped to ONE story's diff per invocation. The diff is provided at invocation
    time (via Conductor context). The adapter does not scan git state to discover a review target
    — the diff is the input, full stop.
  </critical>

  <step n="1" goal="Verify required configuration scaffolding">
    <action>
      Check whether `_bmad/bmm/config.yaml` exists in the project root.

      Run: `ls _bmad/bmm/config.yaml` (or equivalent existence check via Read).
    </action>
    <check if="config.yaml is ABSENT">
      <output>
        ERROR — required configuration scaffolding is missing.

        bmad-code-review requires `_bmad/bmm/config.yaml` to load project context. This file
        does not exist in the current project.

        To resolve, create `_bmad/bmm/config.yaml` with at minimum these fields:

        ```yaml
        project_name: &lt;your-project-name&gt;
        planning_artifacts: "{project-root}/docs/planning-artifacts"
        implementation_artifacts: "{project-root}/docs/implementation-artifacts"
        user_name: &lt;your-name&gt;
        communication_language: English
        document_output_language: English
        ```

        The Conductor cannot proceed with the code-review leg for this story until this file is
        present. This is a setup gap, not a code defect — create the file and re-run.
      </output>
      <note>Halt the adapter run after emitting this error. Do not attempt a partial run.</note>
    </check>
    <check if="config.yaml is PRESENT">
      <action>Proceed to step 2.</action>
    </check>
  </step>

  <step n="2" goal="Receive and validate the story diff">
    <action>
      The diff for the story under review is provided in the Conductor's invocation context.
      Extract it. The diff is bounded to the single story's changes (the Conductor supplies
      a `git diff` scoped to the story worktree — do not expand scope).

      Validate that the diff is non-empty. A diff is the unified output of `git diff` for the
      story's committed changes.
    </action>
    <check if="diff is empty or absent">
      <output>
        FINDINGS: none

        The diff provided for story `{{story_slug}}` is empty — there are no changes to review.
        Returning explicit no-findings result to the Conductor.
      </output>
      <note>Return the no-findings result and exit cleanly. This is not an error.</note>
    </check>
    <check if="diff is present and non-empty">
      <action>
        Set `diff_output` to the provided diff content.

        If a story spec file path was supplied in the invocation context, set `spec_file` to that
        path and `review_mode` to "full". If no spec file was supplied, set `review_mode` to
        "no-spec".

        Do NOT ask the user for any of this information — it is injected by the Conductor.
        Do NOT present a context summary or wait for confirmation. Proceed directly to step 3.
      </action>
    </check>
  </step>

  <step n="3" goal="Run adversarial review layers (report-only)">
    <action>
      Drive the three adversarial review layers from bmad-code-review step-02-review, adapted
      for non-interactive, report-only execution:

      **Suppression rule:** Step 2 of bmad-code-review contains a fallback: "If subagents are
      not available, generate prompt files … and HALT." That HALT is SUPPRESSED. If subagents
      are unavailable, generate the review inline (same model, same prompts) without generating
      files and without halting.

      Launch these layers:

      1. **Blind Hunter** — receives `{{diff_output}}` only. No spec, no context docs, no
         project access. Invoke via the `bmad-review-adversarial-general` skill, or inline if
         subagents are unavailable. Returns a markdown list of findings.

      2. **Edge Case Hunter** — receives `{{diff_output}}` and read access to the project.
         Invoke via the `bmad-review-edge-case-hunter` skill, or inline if unavailable.
         Returns a JSON array of findings.

      3. **Acceptance Auditor** (only when `review_mode` = "full") — receives `{{diff_output}}`,
         the content of the file at `{{spec_file}}`, and any context docs referenced in the
         spec's frontmatter `context` field. Prompt:
         > You are an Acceptance Auditor. Review this diff against the spec and context docs.
         > Check for: violations of acceptance criteria, deviations from spec intent, missing
         > implementation of specified behavior, contradictions between spec constraints and
         > actual code. Output findings as a Markdown list. Each finding: one-line title, which
         > AC/constraint it violates, and evidence from the diff.
         Returns a markdown list.

      When `review_mode` = "no-spec", skip the Acceptance Auditor entirely without prompting.

      Layers run concurrently where possible. If a layer fails or returns empty, record it in
      `failed_layers` and continue with findings from the remaining layers.
    </action>
    <note>
      These layers are read-only. They produce findings text. They do not write any file.
      The adapter collects their output and proceeds to step 4 without pausing.
    </note>
  </step>

  <step n="4" goal="Triage findings (in-process, no file writes)">
    <action>
      Run the triage logic from bmad-code-review step-03-triage inline, adapted for
      non-interactive execution. No HALT, no user interaction.

      1. **Normalize** findings from all layers into a unified list. Each finding:
         - `id` — sequential integer
         - `source` — `blind` | `edge` | `auditor` | merged (e.g., `blind+edge`)
         - `title` — one-line summary
         - `detail` — full description
         - `location` — file and line reference if available

      2. **Deduplicate.** Merge findings that describe the same issue. Use the most specific
         finding as base; append unique detail from others into `detail`; set `source` to merged.

      3. **Classify** each finding into exactly one bucket:
         - `patch` — fixable without human input (unambiguous correct fix)
         - `defer` — pre-existing issue, not caused by the current change
         - `dismiss` — noise, false positive, or handled elsewhere
         - `decision_needed` — only possible when `review_mode` = "full"; ambiguous choice
           requiring human input. When `review_mode` = "no-spec", reclassify as `patch` (if fix
           is unambiguous) or `defer` (if not).

      4. **Drop** all `dismiss` findings. Record dismiss count.

      This triage runs entirely in-process. It does NOT write to any file.
    </action>
    <note>
      The step-04-present HALTs from bmad-code-review are fully suppressed: no file writes,
      no decision-needed resolution prompts, no patch-handling prompts, no sprint-status sync,
      no next-steps menu. All of that is owned by the Conductor's end-gate.
    </note>
  </step>

  <step n="5" goal="Return structured findings to the Conductor">
    <action>
      Emit the findings report in the following structure. This is the adapter's sole output.

      ```
      CODE REVIEW FINDINGS — {{story_slug}}
      ======================================
      Diff scope: {{diff_stats}} (N files, +X -Y lines)
      Review mode: {{review_mode}}
      Layers completed: {{completed_layers}}
      Layers failed: {{failed_layers | "none"}}

      FINDINGS ({{total_count}} total — {{patch_count}} patch, {{defer_count}} defer,
      {{decision_needed_count}} decision-needed, {{dismiss_count}} dismissed):

      {{#each findings}}
      [{{id}}] {{source}} | {{classification}} | {{title}}
        Location: {{location | "unspecified"}}
        Detail: {{detail}}

      {{/each}}

      {{#if no_findings}}
      FINDINGS: none — clean review across all completed layers.
      {{/if}}

      {{#if failed_layers}}
      WARNING: The following review layers failed or returned empty: {{failed_layers}}.
      The review may be incomplete. The Conductor should note this in the end-gate report.
      {{/if}}
      ```

      This output is returned to the Conductor as text. The adapter makes no further action.
      It does not apply patches. It does not write to any file. It does not prompt for next steps.
    </action>
    <note>
      AC4 compliance: when findings exist, all are returned in full (no summarizing away).
      When no findings exist, an explicit "none" result is returned rather than an error.
      AC2 compliance: working tree is byte-for-byte unchanged from before this run.
      AC8 compliance: no stakes classification, no disposition assignment, no escalation,
      no fix application — pure transport.
    </note>
  </step>

</workflow>
