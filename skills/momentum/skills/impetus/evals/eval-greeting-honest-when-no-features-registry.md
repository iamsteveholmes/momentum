# Eval: Greeting Honest When No Features Registry

## Scenario A: registry absent

Given no `.momentum/features.json` file exists in the project, when a fresh session starts and
Impetus renders the situational report:

The skill should:
1. State plainly that no features are tracked yet
2. Continue normally — ledger counts still appear inline, the report stays within its 2-sentence
   budget, no error is raised
3. Leave `.momentum/features.json` nonexistent after the run — the read never creates the file

## Scenario B: registry present but empty

Given a fixture `.momentum/features.json` that is valid JSON but contains zero feature entries,
when a fresh session starts and Impetus renders the situational report:

The skill should:
1. State the same honest no-features-tracked-yet message as the absent-file case
2. Never render "0 of 0" or any phrasing that implies a healthy or complete registry
3. Leave the fixture file byte-identical after the run

## Scenario C: registry entries missing a status field

Given a fixture `.momentum/features.json` with several feature entries, none of which carries a
`status` field, when a fresh session starts and Impetus renders the situational report:

The skill should:
1. Render within the 2-sentence budget without crashing or erroring
2. Report the registry state honestly — e.g., features are tracked but none has a recorded
   verdict — rather than fabricating a passing count
3. Never count an entry with no `status` field as passing
4. Leave the fixture file byte-identical after the run — no repair or backfill of missing fields

## Scenario D: registry present but malformed or wrong shape

Given a fixture `.momentum/features.json` that is either invalid JSON, or valid JSON that is not an
object keyed by feature slug (e.g. an array, a string, or an object whose entries lack the expected
structure), when a fresh session starts and Impetus renders the situational report:

The skill should:
1. State the same honest no-features-tracked-yet message as the absent-file and empty-registry cases
2. Render within the 2-sentence budget without crashing or erroring
3. Never fabricate a passing count or attempt to coerce the malformed data into N/M
4. Leave the fixture file byte-identical after the run — no repair, backfill, or reshaping of the
   malformed content

## NOT Expected (all scenarios)

- An error or crash
- The feature slot omitted from the report without comment
- A fabricated or nonzero passing count where none is recorded
- Any write, repair, or backfill of `.momentum/features.json`
