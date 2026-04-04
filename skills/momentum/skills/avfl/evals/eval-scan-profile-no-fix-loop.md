# Eval: Scan Profile — No Fix Loop

## Scenario

Given AVFL is invoked with:
- `profile: scan`
- `output_to_validate`: a markdown file with known structural and accuracy issues
- `source_material`: the original ground truth document
- `domain_expert`: "technical writer"
- `task_context`: "architecture decision record"

## Expected Behavior

1. The skill spawns dual reviewers (Enumerator + Adversary) on ALL four lenses — structural, accuracy, coherence, and domain — for a total of up to 8 parallel validator subagents
2. Validators run at skepticism level 3 (high) because scan executes a single pass only, and iteration 1 always uses level 3 per pipeline logic
3. The consolidator merges, deduplicates, and scores findings with cross-check confidence tagging (HIGH when both reviewers agree, MEDIUM when only one found it)
4. After consolidation (Phase 3 EVALUATE), the pipeline exits and returns the consolidated findings list as the final output
5. **No fixer subagent is spawned.** Phase 4 (FIX) is never reached because `fix_loop: false`
6. The output is a structured findings list, not a corrected document

## Anti-Behaviors (must NOT happen)

- The fixer is NOT invoked under any circumstances
- The pipeline does NOT loop back to Phase 1 for a second iteration
- The skill does NOT attempt to produce corrected output
- The skill does NOT reduce skepticism to level 2 (there is no iteration 2)
