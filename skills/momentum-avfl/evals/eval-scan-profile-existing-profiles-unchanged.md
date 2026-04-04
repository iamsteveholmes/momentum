# Eval: Scan Profile — Existing Profiles Unchanged

## Scenario

Given AVFL is invoked with `profile: gate` (or `checkpoint`, or `full`) after the scan profile has been added to the framework:

### Sub-scenario A: gate profile
- `profile: gate`
- `output_to_validate`: a well-formed JSON document

### Sub-scenario B: checkpoint profile
- `profile: checkpoint`
- `output_to_validate`: a draft architecture document with minor issues

### Sub-scenario C: full profile
- `profile: full`
- `output_to_validate`: a final PRD with known issues
- `corpus: true` with multiple files

## Expected Behavior

1. **gate** behaves identically to before scan was added: 1 agent, structural lens only, no fix loop, pass/fail with halt_and_report on failure
2. **checkpoint** behaves identically: 1 agent per active lens (2-3 lenses), 1 fix attempt on failure, continue_with_warning regardless of result
3. **full** behaves identically: 2 agents per lens (dual review), up to 4 fix iterations, pass threshold 95, iterative fix loop with skepticism stepping down to level 2 on iteration 2+
4. No existing profile gains the `output_format` field — `structured_handoff` is scan-only
5. Corpus mode (`corpus: true`) continues to work with gate, checkpoint, and full exactly as before — cross-document dimensions activate, per-file output blocks are produced by fixer, authority_hierarchy is respected

## Anti-Behaviors (must NOT happen)

- Existing profile definitions in framework.json are NOT modified
- No existing profile inherits scan-specific fields (output_format, on_fail: return_findings)
- The scan profile does NOT appear as a fallback or default for any existing profile
- Corpus mode behavior is NOT altered by the presence of the scan profile
