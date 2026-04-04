# Eval: Session Menu and Upgrade Templates Use Impetus Voice

## Scenario A — Session Menu (Zero Threads)

Given a developer reaches Step 7 with no open journal threads:

### Expected Behaviors

1. The opening line has personality and warmth consistent with Impetus's guide register — not the flat "You're set up and ready."
2. The visual identity element (ASCII art) does NOT repeat — that is first-encounter only
3. The numbered menu items and closing question "What would you like to work on?" remain unchanged
4. The tone is forward-moving and oriented, not generic

## Scenario B — Upgrade Path (Step 9)

Given a developer triggers the upgrade path (some component group has a version behind current_version):

### Expected Behaviors

1. No `Momentum {{version_entry.version}}` appears as a header or identity label in the upgrade summary
2. The upgrade summary is framed in Impetus voice — conversational, explaining what evolved and why it matters
3. Version numbers may appear in per-group detail lines (e.g., `rules 1.0.0 → 1.1.0`) as factual context — only prohibited as headers
4. The skip message does not use `{{version_entry.version}}` as a header
5. The progress message ("Updating to...") and completion message ("is now at...") use Impetus voice without version-string-as-identity patterns
6. The error output for unresolvable upgrade paths still contains version numbers (appropriate for diagnostics) but uses Impetus voice framing
7. The `[U] Update · [S] Skip for now` prompt is preserved
