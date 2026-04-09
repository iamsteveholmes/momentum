# Eval: Deep Research Fallback — cmux Unavailable or Failure

## Scenario A: cmux Not Available

Given:
- A research project exists at `{{project_dir}}` with `scope.md`
- `cmux` is NOT installed (`which cmux` returns no output / exits non-zero)
- `gemini` CLI IS available

## Expected Behavior (Scenario A)

The workflow step 1.4 should:

1. Check `cmux` availability — fails, so Deep Research is skipped entirely
2. Fall immediately through to the `gemini -p` basic path
3. Ask the user whether to generate a Gemini prompt for external triangulation
4. If user confirms, run `gemini -p "$(cat {{project_dir}}/raw/gemini-prompt.md)"` and write output to `raw/gemini-output.md` with `content_origin: gemini-cli`
5. Continue to Phase 2

## What Should NOT Happen (Scenario A)

- The workflow should NOT attempt any cmux browser operations
- The workflow should NOT halt or error — graceful degradation only

---

## Scenario B: Deep Research Fails After Retries

Given:
- `cmux` IS available
- Auth state loads successfully
- Deep Research pipeline is initiated, but "Generating research plan" persists for >3 minutes without producing a "Start research" button (plan generation timeout)
- Two retry attempts (page reload + retry) also fail

## Expected Behavior (Scenario B)

The workflow step 1.4 should:

1. Attempt plan generation — timeout after ~3 minutes
2. Reload page and retry (up to 2 retries)
3. After exhausting retries, display a warning to the user about the failure
4. Fall back to `gemini -p` basic mode (if `gemini` CLI is available)
5. Write output to `raw/gemini-output.md` with `content_origin: gemini-cli` on the fallback path
6. Continue to Phase 2

## What Should NOT Happen (Scenario B)

- The workflow should NOT halt permanently after a timeout — it must attempt retries and then fall back
- The workflow should NOT write to `raw/gemini-deep-research-output.md` when falling back to basic mode

---

## Scenario C: Both cmux and gemini Unavailable

Given:
- `cmux` is NOT available
- `gemini` CLI is also NOT available

## Expected Behavior (Scenario C)

The workflow step 1.4 should:

1. Check `cmux` — unavailable
2. Check `gemini` — unavailable
3. Skip Gemini step entirely with an informational note
4. Continue to Phase 2 without any Gemini output
