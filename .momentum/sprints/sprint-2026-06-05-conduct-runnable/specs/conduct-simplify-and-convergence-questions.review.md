# conduct-simplify-and-convergence-questions — Document Review Contract

```yaml
story_slug: conduct-simplify-and-convergence-questions
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-simplify-and-convergence-questions.review.md
how_dev_self_checks: |
  Before you signal done, open the per-story build/conduct workflow document you produced and
  confirm a fresh reader could verify every claim below by reading ONLY that document. Walk the
  checklist: is the optional post-fix cleanup pass now written as a concrete, runnable step that
  triggers the cleanup, captures whatever it produces, and feeds that result back into the build
  — the same kind of executable step as the mid-flight fix step and the re-check step, not inert
  prose beside two concrete steps; does the document state exactly one rule for when the cleanup
  pass runs (a single stated condition — every story, a size/diff threshold, or on demand — not
  several conflicting hints); does it state one single canonical number for how many times a
  retry may be attempted before giving up, with every other mention of a retry/fix-attempt limit
  agreeing with that number rather than contradicting it; does it name who or what is permitted
  to request the deeper / higher-rigor review level and the signal that triggers it; and does it
  state, for a finding that was approved-as-is rather than fixed, exactly which terminal state
  the story lands in, with no named terminal state left unreachable? Finally confirm none of
  these resolutions reopened a human question on the routine build path — when this workflow is
  run, a routine build still reaches the final gate with no mid-run developer question.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/conduct-simplify-and-convergence-questions.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

The per-story build/conduct workflow document this story delivers — the build workflow that
describes, per story, the mid-flight fix step, the optional post-fix cleanup pass, the re-check
step, the retry/give-up bound, the deeper-review opt-in, and the story terminal states. A
reviewer opens that delivered workflow document and confirms every claim below by reading it.
For this document-review contract, reading the delivered workflow document is the sanctioned
verification method.

The single behavioral claim below (routine run reaches the final gate with no mid-run question)
is confirmed by running the delivered workflow against a routine sprint and observing the
absence of any mid-run developer prompt.

## Required Claims

- [ ] The optional post-fix cleanup pass is written as a concrete, runnable step — it contains an instruction that actually triggers the cleanup work, not a sentence merely describing that such a pass could happen.
- [ ] The cleanup pass step captures whatever the cleanup produces and feeds that result back into the build flow.
- [ ] The cleanup pass is the same kind of executable step as the mid-flight fix step and the re-check step — all three are actions that run, not one describing while the others act.
- [ ] Exactly one trigger rule for the cleanup pass is stated (for example: every story, a size/diff threshold, or on demand), and no second, conflicting statement of when the cleanup pass runs appears anywhere else in the document.
- [ ] A single canonical retry bound is stated as the source of truth for how many attempts are allowed before the loop gives up.
- [ ] Every other mention of a retry or fix-attempt limit in the document agrees with that canonical bound rather than naming a different number.
- [ ] The document names who or what is permitted to request the deeper / higher-rigor review level.
- [ ] The document states the signal or condition on which that deeper review level is requested.
- [ ] For a finding approved-as-is rather than fixed, the document states exactly which terminal state the story lands in.
- [ ] No terminal story state named by the document is left unreachable — every named terminal state has a defined path that reaches it.

## Behavioral Claim

- [ ] Running the delivered workflow against a routine sprint (only ordinary, low-stakes findings) reaches the final gate with no mid-run developer prompt — none of the cleanup-pass trigger, retry bound, deeper-review owner, or end-state resolutions inserts a mid-run question. Observable: the run produces only its run-start and end-gate developer touchpoints.

## Required Sections

- [ ] A per-story build flow that presents the mid-flight fix step, the optional post-fix cleanup pass, and the re-check step as three executable steps of the same kind.
- [ ] A stated rule for when the cleanup pass runs (single, non-conflicting).
- [ ] A canonical retry-bound statement that other retry/fix-attempt mentions defer to.
- [ ] A deeper-review opt-in section naming the requesting party and the triggering signal.
- [ ] An enumeration of story terminal states, including the terminal state for the approved-as-is path, with no named terminal state left unreachable.

## Pass Criteria

- All Required Claims checkboxes are confirmable by reading the delivered workflow document alone.
- All Required Sections are present.
- The cleanup pass is an executable, output-capturing, fed-back step on par with the fix and re-check steps, with exactly one stated trigger rule.
- There is one canonical retry bound and no place in the document contradicts it with a different number.
- The deeper-review level has both a named requesting party and a stated triggering signal.
- The approved-as-is path lands in a stated terminal state and no named terminal state is unreachable.
- The behavioral claim holds: a routine run reaches the final gate with only its run-start and end-gate touchpoints.

## Fail Criteria

- Any Required Claim cannot be confirmed from the delivered workflow document alone.
- The cleanup pass is descriptive prose only — it states cleanup may occur but contains no instruction that triggers it, captures nothing, and feeds nothing back, while the fix and re-check steps remain concrete.
- The cleanup-pass placement is left open, or two or more conflicting statements of when it runs coexist.
- Two or more different retry/fix-attempt limits remain with no single reconciling canonical bound.
- The deeper-review level has no named requesting party or no stated trigger.
- The approved-as-is outcome is undefined, or the document names a terminal state that nothing can ever transition into.
- A convergence resolution causes a routine run to pause and ask the developer a question mid-run.
