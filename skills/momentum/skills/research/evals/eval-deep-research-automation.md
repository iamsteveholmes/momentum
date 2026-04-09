# Eval: Deep Research Automation — cmux-browser Happy Path

## Scenario

Given:
- A research project exists at `{{project_dir}}` with a `scope.md` containing topic, goals, and sub-questions
- `cmux` is available (`which cmux` succeeds)
- Saved Google auth state exists at `~/.claude/browser-state/google-auth.json`
- The auth state is valid (DOM inspection shows no "Sign in" button after loading)
- `raw/gemini-deep-research-output.md` does NOT yet exist

## Expected Behavior

The workflow step 1.4 should:

1. Check `cmux` availability first — succeeds, so Deep Research path is taken
2. Load auth state from `~/.claude/browser-state/google-auth.json` via `cmux browser <surface> state load`
3. Verify authentication by checking DOM for absence of "Sign in" button (or presence of user avatar/PRO badge) — NOT by checking the URL
4. Open `gemini.google.com` in a cmux browser surface
5. Enable Deep Research via Tools menu: click `button[aria-label='Tools']`, then use `eval` with `querySelectorAll("[role=menuitemcheckbox]")` to find and click the Deep Research checkbox
6. Fill the research prompt into the input field using `cmux browser fill "[contenteditable], textarea, [role=textbox]"` (rich text editor pattern)
7. Click "Send message" to submit
8. Poll for "Start research" button appearance (using `eval` with `querySelectorAll("button").find(...)`) — does NOT ask user to click it, auto-clicks immediately
9. Poll for research completion by monitoring `.markdown.markdown-main-panel` text length stabilization
10. Extract the report from the `.markdown.markdown-main-panel` element with `textContent.length > 10000`
11. Write extracted report to `raw/gemini-deep-research-output.md` with provenance frontmatter:
    ```yaml
    content_origin: gemini-deep-research
    date: {{date}}
    topic: "{{topic}}"
    method: cmux-browser
    ```
12. Optionally send 2-3 follow-up questions targeting sub-questions thinly covered
13. Continue to Phase 2 of the research pipeline

## What Should NOT Happen

- The workflow should NOT use `gemini -p` on this path
- The workflow should NOT ask the user to approve the Deep Research plan before starting
- The workflow should NOT write to `raw/gemini-output.md` (that is the fallback path)
- Auth verification should NOT use URL-based detection
