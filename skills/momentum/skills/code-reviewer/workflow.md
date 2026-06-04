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

  <critical>
    The bmad-code-review SKILL.md activation flow (Steps 1–6: resolve_customization.py,
    persistent_facts, config load, user greeting, "WAIT FOR INPUT") is SUPPRESSED entirely.
    This adapter does NOT run resolve_customization.py and does NOT greet the user. Config is
    loaded directly from `config_path` resolved in step 1 of this workflow; no activation
    ceremony precedes it.

    step-01-gather-context from bmad-code-review is likewise BYPASSED in its entirety. The
    adapter does not run the five-tier target-discovery cascade, does not ask "What do you want
    to review?", and does not present the CHECKPOINT summary or wait for user confirmation. All
    of those prompts are suppressed because the diff and spec are already injected by the
    Conductor — step 2 of this workflow is the complete substitute for step-01-gather-context.
  </critical>

  <step n="1" goal="Verify required configuration scaffolding">
    <action>
      Resolve the project's main-worktree root — the canonical checkout where `_bmad/` lives.
      This is NOT necessarily the CWD (git worktrees do not materialize gitignored/untracked
      files). Resolve with:

        `git rev-parse --git-common-dir`

      That returns the path to the `.git` directory of the main worktree (e.g.,
      `/path/to/project/.git`). Strip the `.git` suffix to get `main_root`.

      Then check whether `${main_root}/_bmad/bmm/config.yaml` exists (Read or ls).
    </action>
    <check if="config.yaml is ABSENT from main_root">
      <output>
        ERROR — required configuration scaffolding is missing.

        bmad-code-review requires `_bmad/bmm/config.yaml` (in the main project checkout) to
        load project context. This file does not exist.

        To resolve, create `_bmad/bmm/config.yaml` at the project root with these fields:

        ```yaml
        project_name: YOUR_PROJECT_NAME
        user_skill_level: intermediate
        planning_artifacts: "{project-root}/_bmad-output/planning-artifacts"
        implementation_artifacts: "{project-root}/_bmad-output/implementation-artifacts"
        momentum_state: "{project-root}/.momentum"
        project_knowledge: "{project-root}/docs"
        user_name: YOUR_NAME
        communication_language: English
        document_output_language: English
        output_folder: "{project-root}/_bmad-output"
        ```

        The Conductor cannot proceed with the code-review leg for this story until this file is
        present. This is a setup gap, not a code defect — create the file and re-run.
      </output>
      <note>Halt the adapter run after emitting this error. Do not attempt a partial run.</note>
    </check>
    <check if="config.yaml is PRESENT at main_root">
      <action>
        Set `config_path` to `${main_root}/_bmad/bmm/config.yaml`. Proceed to step 2.
      </action>
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

      1. **Normalize** findings from all layers into a unified list. Each finding at this stage:
         - `id` — sequential integer
         - `review_layer` — `blind` | `edge` | `auditor` | merged (e.g., `blind+edge`)
         - `title` — one-line summary
         - `detail` — full description
         - `location` — file and line reference if available

      2. **Deduplicate.** Merge findings that describe the same issue. Use the most specific
         finding as base; append unique detail from others into `detail`; set `review_layer` to
         the merged label (e.g., `blind+edge`).

      3. **Classify** each finding into exactly one bmad triage bucket:
         - `patch` — fixable without human input (unambiguous correct fix)
         - `defer` — pre-existing issue, not caused by the current change
         - `dismiss` — noise, false positive, or handled elsewhere
         - `decision_needed` — only possible when `review_mode` = "full"; ambiguous choice
           requiring human input. When `review_mode` = "no-spec", reclassify as `patch` (if fix
           is unambiguous) or `defer` (if not).

      4. **Drop all `dismiss`-bucket findings immediately.** The bmad `dismiss` bucket represents
         noise, false positives, or findings handled elsewhere — these are bmad-layer noise and
         MUST NOT flow into the canonical finding stream. Record the dropped count for the header
         summary, but do not emit any dropped finding as a canonical record.

         IMPORTANT — the two "dismiss" concepts are DISTINCT:
         - **bmad `dismiss` bucket** (dropped here) = bmad's own noise filter. A finding in this
           bucket was judged as a false positive or already handled, before any conduct logic runs.
           Dropping it here is correct and required.
         - **conduct fixer `dismissed` disposition** (downstream, not here) = a *fixer-leg* outcome
           where a legitimate-looking finding the fixer chose not to act on is recorded with a
           REQUIRED non-empty rationale and rendered in the end-gate report (per DEC-036). This
           disposition is assigned by the fixer, not by this adapter. The adapter MUST NOT
           pre-emptively suppress any `decision_needed`, `patch`, or `defer` finding on its own
           judgment — doing so would rob the fixer of findings it is supposed to see and
           dismiss-with-rationale, and would silently shrink the report's dismissal ledger.

      The `decision_needed`, `patch`, and `defer` buckets are all legitimate findings and proceed
      to step 4.5 for canonical normalization. Do not filter or suppress any of them.

      This triage runs entirely in-process. It does NOT write to any file.
    </action>
    <note>
      The step-04-present HALTs from bmad-code-review are fully suppressed: no file writes,
      no decision-needed resolution prompts, no patch-handling prompts, no sprint-status sync,
      no next-steps menu. All of that is owned by the Conductor's end-gate.
    </note>
  </step>

  <step n="4.5" goal="Normalize surviving findings to the canonical schema and populate stakes_class">
    <action>
      For each surviving finding (bucket: `decision_needed`, `patch`, or `defer`), emit one
      record in the canonical finding schema defined in
      `skills/momentum/references/finding-schema.md`. Populate fields as follows:

      **Adapter-stamped fields (set by this adapter, not the fixer):**
      - `story_slug` — the story slug from the Conductor's invocation context
      - `source` — always `bmad-code-review` for every finding this adapter emits; no exceptions
      - `verdict` — set to `FAIL` for every finding this adapter emits; all surviving findings
        (patch, defer, decision_needed) represent genuine issues the reviewer flagged, so the
        reviewer's raw verdict is always FAIL. Do NOT write the bmad bucket label into this field
        — the bucket is a triage category, not the reviewer's pass/fail assessment
      - `severity` — infer from the finding's detail prose (e.g., `blocker` if the reviewer
        flagged it as critical/blocking, `major` if significant but non-blocking, `minor` for
        style/low-impact); when inference is ambiguous, use `minor` as the conservative default
      - `type` — infer from the finding's subject: `correctness`, `security`,
        `spec-compliance`, `style`, `test-coverage`, or another appropriate category
      - `location` — copy from the normalized finding's `location` field; use `"unspecified"`
        when unavailable
      - `summary` — copy the normalized finding's `title` (one-line summary)
      - `detail` — copy the normalized finding's `detail` (full explanation)
      - `evidence` — copy any code snippet or diff excerpt the reviewer cited; use `""` if none
      - `ac_id` — set to the acceptance criterion identifier if the Acceptance Auditor cited one;
        otherwise `null`
      - `legitimate` — set to `true` for `patch`, `decision_needed`, and `defer` findings (all
        three buckets represent issues the reviewer judged genuine, not false positives); the
        fixer assigns disposition entirely based on the emitted fields — the adapter does not
        predict or constrain fixer routing
      - `suggested_fix` — copy any fix suggestion from the reviewer's prose; `null` if none

      **Disposition and timing fields** — these are fixer-assigned; the adapter does NOT set
      `disposition` or `timing_tier`. Leave them absent or null. The fixer populates them.

      **`stakes_class` — assigned by consulting the shared rubric (this adapter's core wiring):**

      Read the classification signals in `skills/momentum/references/stakes-classification-rubric.md`.
      For each finding, evaluate the finding's `summary` and `detail` prose against the rubric's
      signal lists in this order:

      1. Does the finding involve authentication, authorization, credential handling, isolation
         boundaries, privilege escalation, or input validation at a security boundary?
         → `security-auth-isolation`
      2. Does the finding involve schema migrations, data deletes, force-pushes, production
         deploys, destructive file operations, or any action whose failure means permanent data
         loss or an unrecoverable state?
         → `irreversible-destructive`
      3. Does the finding involve shared interfaces, cross-cutting contracts, architectural
         patterns, module boundaries, or surfaces whose failure radiates widely across many
         consumers?
         → `high-blast-radius-architecture`
      4. None of the above match → `routine`

      **The adapter MUST NOT re-implement or fork this logic.** The signal lists above are
      extracted from the rubric for in-step reference; the rubric document is the authoritative
      source. If the rubric's signal list and the signals reproduced here ever diverge, the
      rubric wins. The adapter's obligation is emission-wiring only: read the rubric, apply its
      signals, set the field. Do not invent additional classification heuristics here.

      **No-signal default:** bmad-code-review emits no stakes or security signal of its own —
      its triage is bucket-only. When the finding prose provides no signal matching any of the
      three stakes classes, set `stakes_class` to `routine`. Never leave `stakes_class` unset.

      The result of this step is a list of canonical finding records, each with `stakes_class`
      populated and `source` set to `bmad-code-review`. These records are the adapter's output
      to the Conductor. This step does NOT write any file.
    </action>
    <note>
      Ownership boundaries:
      - This adapter owns the WIRING: bucket→schema mapping, `source` stamping, and rubric
        consumption to populate `stakes_class`.
      - The RUBRIC (what counts as each stakes class) is owned by
        `skills/momentum/references/stakes-classification-rubric.md`. The adapter does not
        redefine or duplicate it.
      - The SCHEMA shape (field names, dispositions, timing tiers) is owned by
        `skills/momentum/references/finding-schema.md`. The adapter conforms to it.
      - DISPOSITIONS and TIMING TIERS are fixer-assigned. The adapter emits them absent/null.
    </note>
  </step>

  <step n="5" goal="Return canonical findings to the Conductor">
    <action>
      Emit the findings report in the following structure. This is the adapter's sole output.

      ```
      CODE REVIEW FINDINGS — {{story_slug}}
      ======================================
      Diff scope: {{diff_stats}} (N files, +X -Y lines)
      Review mode: {{review_mode}}
      Layers completed: {{completed_layers}}
      Layers failed: {{failed_layers | "none"}}
      bmad-dismiss dropped (noise): {{bmad_dismiss_count}} (not in canonical stream)

      CANONICAL FINDINGS ({{canonical_count}} total — {{patch_count}} patch,
      {{defer_count}} defer, {{decision_needed_count}} decision-needed):
      All findings carry source=bmad-code-review and a populated stakes_class.

      {{#each canonical_findings}}
      [{{id}}]
        story_slug:    {{story_slug}}
        source:        bmad-code-review
        verdict:       {{verdict}}
        severity:      {{severity}}
        stakes_class:  {{stakes_class}}
        type:          {{type}}
        location:      {{location}}
        summary:       {{summary}}
        detail:        {{detail}}
        evidence:      {{evidence}}
        ac_id:         {{ac_id}}
        legitimate:    {{legitimate}}
        suggested_fix: {{suggested_fix}}
        disposition:   (fixer-assigned)
        timing_tier:   (fixer-assigned)

      {{/each}}

      {{#if no_canonical_findings}}
      FINDINGS: none — clean review across all completed layers ({{bmad_dismiss_count}} bmad-dismiss noise dropped).
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
      Bucket mapping — what flows through and what is dropped:
      - `decision_needed` → canonical finding with source=bmad-code-review (flows to fixer)
      - `patch`          → canonical finding with source=bmad-code-review (flows to fixer)
      - `defer`          → canonical finding with source=bmad-code-review (flows to fixer)
      - `dismiss`        → DROPPED at the bmad layer; count recorded in header but NOT emitted

      The bmad `dismiss` drop and the conduct fixer `dismissed` disposition are DISTINCT:
      the drop here is bmad-layer noise removal; the fixer's `dismissed` disposition is a
      downstream, rationale-required outcome for legitimate-looking findings the fixer waves off.
      This adapter never pre-empts the fixer's dismissal judgment.

      stakes_class guarantee: every canonical finding carries a populated stakes_class. It is
      assigned via the shared rubric (`stakes-classification-rubric.md`), defaulting to `routine`
      when the finding prose matches no stakes-class signal. The adapter does not leave it unset.

      Working-tree safety: byte-for-byte unchanged from before this run. The adapter is read-only.
    </note>
  </step>

</workflow>
