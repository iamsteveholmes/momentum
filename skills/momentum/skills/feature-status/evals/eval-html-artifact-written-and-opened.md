# Eval: HTML Artifact Written and Opened

## Scenario

Given a valid `features.json` and `stories/index.json`, the skill must write a
self-contained HTML file, open it in a cmux browser pane, and write the cache
`.md` file with correct frontmatter.

## Input

### features.json (valid, minimal)
```json
{
  "project_type": "product",
  "features": [
    {
      "id": "feat-onboarding",
      "name": "User Onboarding",
      "type": "flow",
      "status": "partial",
      "acceptance_condition": "A new user can complete onboarding in under 3 minutes with contextual guidance.",
      "stories": ["onboarding-flow", "feed-init"]
    },
    {
      "id": "feat-auth",
      "name": "Authentication",
      "type": "connection",
      "status": "working",
      "acceptance_condition": "A user can sign in with email/password and stay authenticated across sessions.",
      "stories": ["auth-login", "session-persistence"]
    }
  ]
}
```

### stories/index.json (valid, matching)
```json
{
  "stories": {
    "onboarding-flow": {
      "title": "Onboarding flow screens",
      "status": "done",
      "summary": "Implements 4-screen onboarding wizard with contextual tips"
    },
    "feed-init": {
      "title": "Initial feed population",
      "status": "in-progress",
      "summary": "Populates user feed with starter content on first login"
    },
    "auth-login": {
      "title": "Email/password login",
      "status": "done",
      "summary": "Login form with email/password authentication"
    },
    "session-persistence": {
      "title": "Session token persistence",
      "status": "done",
      "summary": "Stores and refreshes JWT tokens across browser sessions"
    }
  }
}
```

## Expected Behavior

1. The skill writes `.claude/momentum/feature-status.html` with:
   - No external CSS/JS dependencies (all inline or CDN ESM for Mermaid)
   - Valid HTML5 structure (`<!DOCTYPE html>`, `<head>`, `<body>`)
   - Works when opened via `file://` protocol (no server required)
   - Page header showing project name and generated date
   - Summary stats bar with total features, counts by status, and gap count
   - Mermaid dependency graph inside a `<details>` block (collapsed by default)
   - Feature tables grouped by type (flow, connection for this input)
   - Footer

2. The skill opens the file in a cmux browser pane:
   ```
   cmux browser open file://{claude_project_dir}/.claude/momentum/feature-status.html
   ```

3. The skill writes `.claude/momentum/feature-status.md` with frontmatter:
   ```yaml
   ---
   input_hash: {sha256 of features_content + ":" + stories_content}
   summary: 2 features: 1 working · 1 partial · 0 not-started · 0 gaps
   generated_at: {ISO 8601 datetime}
   ---
   ```
   Body: same one-line summary as the frontmatter `summary` field.

## Pass Criteria

- [ ] `.claude/momentum/feature-status.html` is written
- [ ] HTML has no broken external resource references (except Mermaid CDN ESM)
- [ ] HTML opens correctly via `file://` (no server-side rendering needed)
- [ ] HTML contains `<details class="dependency-graph">` (collapsed by default)
- [ ] HTML contains `<section class="feature-group" data-type="flow">` and `data-type="connection"`
- [ ] `cmux browser open` command is executed with the correct file path
- [ ] `.claude/momentum/feature-status.md` is written with all three frontmatter fields
- [ ] `input_hash` matches SHA-256 of `features_content + ":" + stories_content`
- [ ] `generated_at` is a valid ISO 8601 datetime

## Failure Criteria

- HTML references external CSS files (only Mermaid ESM CDN import is permitted)
- HTML artifact is not written (skill outputs text dump instead)
- cmux browser open is not called (or path is wrong)
- `.claude/momentum/feature-status.md` is missing or has incorrect frontmatter
- `input_hash` is missing or not a 64-char hex string
