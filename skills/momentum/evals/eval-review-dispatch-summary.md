# Eval: Review Dispatch Summary

## Scenario

Given implementation of a story cycle or workflow step has completed and a review process is being dispatched, Impetus must provide a human-readable implementation summary at the moment of dispatch — not after the review completes.

The summary is delivered so the developer can read it while the review runs, making the wait productive.

## Expected Behavior

- At the moment a review subagent is dispatched, Impetus delivers a summary of what was built
- The summary includes: files created/modified, key decisions made, how work maps to acceptance criteria, any deviations or open questions
- The summary is human-readable prose, not a raw file list
- The developer reads the summary during the review wait, not after results arrive
- The summary transitions naturally into the productive waiting pattern

## NOT Expected

- Review dispatched without any summary
- Summary delivered only after review results arrive
- Summary that is just a file list without context about decisions and AC mapping
- Dead air between dispatch and review results
