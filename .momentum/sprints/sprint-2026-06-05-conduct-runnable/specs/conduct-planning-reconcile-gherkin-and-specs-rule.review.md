# conduct-planning-reconcile-gherkin-and-specs-rule — Document Review Contract

```yaml
story_slug: conduct-planning-reconcile-gherkin-and-specs-rule
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-planning-reconcile-gherkin-and-specs-rule.review.md
how_dev_self_checks: |
  Before you signal done, open the delivered planning guidance documents you produced — the
  sprint-planning workflow document and the story-creation injected-guidance document — and
  confirm a fresh reader could verify the document claims below by reading ONLY those documents.
  Walk the checklist: search the text of both documents for any wording that forbids the
  developer role from reading or accessing the contract specs path, and confirm none remains;
  confirm the documents state the one-contract-of-record rule — exactly one contract file per
  non-app story, with no standalone Gherkin .feature file written alongside another contract for
  the same slug. Then confirm the behavioral claim: run sprint planning against a small set of
  non-app stories (no user-interface stories among them), let it activate a sprint, and glob the
  sprint's specs/ directory per story slug — each planned non-app story resolves to exactly one
  contract file, never a .feature file alongside a .eval.yaml / .smoke.sh / .review.md for the
  same slug.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/conduct-planning-reconcile-gherkin-and-specs-rule.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

The delivered planning-guidance documents this story corrects: the sprint-planning workflow
document and the story-creation injected-guidance document. A reviewer opens those delivered
documents and confirms the document claims below by reading them. For this document-review
contract, reading the delivered planning-guidance documents is the sanctioned verification
method.

The behavioral claim below (one contract file per non-app story after planning) is confirmed by
running sprint planning against non-app stories, activating the sprint, and globbing the
resulting specs/ directory — an observable filesystem outcome.

## Required Claims

- [ ] The delivered sprint-planning workflow document contains no wording that forbids the developer role from reading or accessing the contract specs path.
- [ ] The delivered story-creation injected-guidance document (the guidance carried into created stories) contains no wording that forbids the developer role from reading or accessing the contract specs path.
- [ ] The delivered planning guidance states the one-contract-of-record rule: each planned non-app story has exactly one contract file of record, with no standalone Gherkin .feature file produced alongside another contract for the same slug.

## Behavioral Claim

- [ ] Running sprint planning against a set of non-app stories (no user-interface story among them) and activating the sprint produces, for each planned non-app story, exactly one contract file in the sprint's specs/ directory: a glob of specs/ on a single story's slug returns exactly one file — never zero for a planned story, never two, and never a .feature file alongside a .eval.yaml / .smoke.sh / .review.md for the same slug.

## Required Sections

- [ ] In the sprint-planning workflow document, contract-generation guidance that yields a single contract of record per non-app story (no standalone .feature emitted alongside another contract for the same slug).
- [ ] In both the sprint-planning workflow document and the story-creation injected-guidance document, the absence of any standing prohibition on the developer role accessing the specs path.

## Pass Criteria

- Both delivered planning-guidance documents are free of any wording forbidding the developer role from accessing the specs path.
- The one-contract-of-record-per-non-app-story rule is stated in the delivered planning guidance.
- The behavioral claim holds: after planning, every planned non-app story resolves to exactly one contract file in specs/, with no duplicate .feature alongside another contract for the same slug.

## Fail Criteria

- A standing instruction forbidding the developer role from accessing the specs path remains in the delivered sprint-planning workflow document or in the story-creation injected guidance.
- The one-contract-of-record-per-non-app-story rule is not stated in the delivered planning guidance.
- After planning, any planned non-app story has two or more contract files for its slug — for example a .feature file alongside a .eval.yaml / .smoke.sh / .review.md — or a glob of specs/ on a planned story's slug returns zero files.
