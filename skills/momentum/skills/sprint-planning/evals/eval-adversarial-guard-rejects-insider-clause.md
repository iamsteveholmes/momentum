# Eval: Adversarial Guard Rejects Insider Clause

**ID:** eval-adversarial-guard-rejects-insider-clause
**Change-type:** skill-instruction
**Phase:** adversarial guard (Step 3.5 Phase C)

## Scenario

Given a contract for story `add-impetus-greeting` (skill-instruction) that contains the clause:
> "When sprint-planning delegates to bmad-create-story, the story file is written to .momentum/stories/"

And a second clause that is black-box clean:
> "When the developer invokes momentum:sprint-planning with a story selection, a story file appears at .momentum/stories/{slug}.md"

When Step 3.5 Phase C runs (adversarial guard) with a decorrelated adversarial agent (not the same agent that authored the contract)

Then:
1. The adversarial agent produces a structured findings list
2. The first clause ("delegates to bmad-create-story") is flagged as failing the Outsider Test
3. The flagged clause identifies: the story slug, the clause text, and a one-sentence reason why it fails
4. The second clean clause is NOT flagged
5. The sprint-planning workflow rewrites the flagged clause to describe observable outcomes
6. The adversarial agent is re-run on the revised contract
7. The revised clause passes the re-run (no findings on the second pass)

## Pass Criteria

- Findings list produced with at least 1 entry for the insider clause
- Entry includes: story slug, clause text, failure reason
- Failure reason mentions insider knowledge (delegation chain, internal mechanism)
- Clean clause not flagged
- Rewrite cycle runs before proceeding
- Re-run produces no findings for the rewritten clause

## Fail Criteria

- Adversarial agent flags zero clauses (missed the insider reference)
- Adversarial agent flags the clean clause (false positive)
- No rewrite cycle runs after findings
- Same agent that authored the contract performs the review (not decorrelated)
- Sprint proceeds to team composition with unresolved insider clause
