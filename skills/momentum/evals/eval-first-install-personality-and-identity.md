# Eval: First-Install Greeting Has Personality and Identity

## Scenario

Given a developer invokes `/momentum` for the first time (both global-installed.json and installed.json are absent), and startup routing dispatches to Step 2 (first-install consent):

## Expected Behaviors

1. The greeting output includes a visual identity element (ASCII art, nerdfont icon, or equivalent) — something memorable that marks Impetus as a presence, not a generic tool
2. The greeting includes a brief self-introduction where Impetus names itself and establishes its role as a practice partner (1-2 sentences, not a feature list)
3. No `{{current_version}}`, `{{version_entry.version}}`, or any rendered version string (e.g., "Momentum 1.0.0") appears as a header or identity label in any user-facing output across Steps 2 and 3
4. The consent body (what will be installed, where) retains its factual content but is framed in Impetus's guide voice — oriented, substantive, forward-moving — not as a mechanical install manifest
5. The `[Y] Yes · [N] No` prompt and `Set up now?` question are preserved
6. Step 3 progress output does not contain version machinery — uses Impetus voice instead
