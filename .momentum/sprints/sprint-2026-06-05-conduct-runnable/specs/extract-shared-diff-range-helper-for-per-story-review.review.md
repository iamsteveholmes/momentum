# extract-shared-diff-range-helper-for-per-story-review — Document Review Contract

```yaml
story_slug: extract-shared-diff-range-helper-for-per-story-review
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/extract-shared-diff-range-helper-for-per-story-review.review.md
how_dev_self_checks: |
  Before you signal done, open the diff-range pattern document you produced and confirm a fresh reader
  could verify each claim below by reading only that document and the places that cite it. Walk the
  checklist. First: is there exactly ONE documented diff-range pattern — one canonical way to compute
  the range of changes for a per-story review — rather than several competing recipes? Second: does
  that one pattern say to capture the pre-merge commit identifier at the point of merge, and then take
  the diff as a two-dot range from that captured pre-merge point up to the story's branch (the
  pre-merge point .. the story branch)? Third: does the pattern document declare itself the single
  named source-of-record for the per-story review diff range — the one canonical place a reviewer is
  meant to consult, rather than one recipe among several? Fourth: confirm the document validates the
  pattern against the build's actual merge mechanics (rebase, then fast-forward), not an abstract idea
  of how git merges. Fifth — behavioral: run a per-story review over a merged story and read its output;
  confirm it produces a correct, non-empty scoped diff for a story that genuinely changed files (no
  empty three-dot diff). If exactly one pattern exists, it uses the captured-pre-merge two-dot range,
  the document declares itself canonical, it is checked against the real rebase-then-fast-forward
  mechanics, and a per-story review run yields a correct non-empty scoped diff, the work is done.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/extract-shared-diff-range-helper-for-per-story-review.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

The diff-range pattern deliverable that documents the single vetted way to compute a per-story review diff range, declaring itself the canonical source-of-record for that range. All document-review claims below are confirmed by reading the pattern document alone — no source code access required. One behavioral claim is confirmed by running a per-story review over a merged story and reading its output.

## Required Claims

- [ ] Exactly one diff-range pattern is documented — a single canonical recipe for computing a per-story review's diff range, with no competing alternative recipes presented as equally valid.
- [ ] The pattern instructs capturing the pre-merge commit identifier at the merge point.
- [ ] The pattern takes the diff as a two-dot range from that captured pre-merge point up to the story branch (the captured pre-merge point `..` the story branch), not a three-dot range.
- [ ] The pattern document declares itself the single named source-of-record for the per-story review diff range — the one canonical place a reviewer consults for that range.
- [ ] Running a per-story review over a merged story produces a correct, non-empty scoped diff — no empty three-dot diff — observable by running the review and reading its output.
- [ ] The pattern is validated against the build's concrete merge mechanics (rebase, then fast-forward), not against an abstract git merge model.
- [ ] Following the pattern does not produce an empty diff for a story that genuinely changed files (the known empty-three-dot-diff failure is explicitly avoided).

## Required Sections

- [ ] A statement of the single canonical diff-range pattern.
- [ ] The capture step for the pre-merge commit identifier at the merge point.
- [ ] The two-dot range expression from the captured pre-merge point to the story branch.
- [ ] A note that the pattern is validated against rebase-then-fast-forward merge mechanics.
- [ ] A self-declaration that this document is the canonical source-of-record for the per-story review diff range.

## Pass Criteria

- All document-review Required Claims are confirmable by reading the pattern document alone; the behavioral claim is confirmable by running a per-story review and reading its output.
- All Required Sections are present.
- Exactly one diff-range pattern exists, using the captured-pre-merge two-dot range.
- The document declares itself the single canonical source-of-record for the per-story review diff range.
- The pattern is explicitly validated against rebase-then-fast-forward mechanics, and a per-story review run over a merged story yields a correct, non-empty scoped diff for a story that changed files.

## Fail Criteria

- More than one diff-range recipe is documented, or no single canonical pattern is established.
- The pattern uses a three-dot range, or fails to capture the pre-merge identifier at the merge point.
- The document does not declare itself the canonical source-of-record for the per-story review diff range.
- The pattern is justified only against an abstract git model, or a per-story review run over a merged story produces an empty diff for a story that genuinely changed files.
