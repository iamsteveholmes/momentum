# Eval: Product Path Unaffected by Practice Extension

## Scenario

Given a product project directory with no `skills/` directory containing SKILL.md files,
the skill renders feature type groups (flow/connection/quality) with status and gap analysis.
No topology block or SDLC coverage table appears in the output.

---

## Setup

**Project does NOT have practice project signals:**
- No `skills/` directory (or it exists but contains no `*/SKILL.md` files)
- `_bmad-output/planning-artifacts/` may or may not exist

**features.json present with product structure:**
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
      "acceptance_condition": "A user can sign in and stay authenticated across sessions.",
      "stories": ["auth-login", "session-persistence"]
    },
    {
      "id": "feat-perf",
      "name": "Sub-2s Page Load",
      "type": "quality",
      "status": "not-started",
      "acceptance_condition": "All key pages load in under 2 seconds on a standard 4G connection.",
      "stories": []
    }
  ]
}
```

---

## Expected Behavior

1. Practice project detection check finds no `skills/*/SKILL.md` files → falls through to product path
2. Product path renders as normal: feature type groups (flow, connection, quality)
3. HTML output contains `<section class="feature-group" data-type="flow">`,
   `data-type="connection"`, `data-type="quality"` sections
4. No ASCII topology block appears anywhere in the output
5. No SDLC coverage table appears in the output
6. No skill inventory is built or rendered
7. Gap analysis runs on feature acceptance conditions vs. assigned stories

---

## Pass Criteria

- [ ] Product path executes (not practice path) when no `skills/*/SKILL.md` present
- [ ] HTML contains three type groups: flow, connection, quality
- [ ] HTML contains `<section class="feature-group" data-type="flow">` element
- [ ] HTML contains `<section class="feature-group" data-type="connection">` element
- [ ] HTML contains `<section class="feature-group" data-type="quality">` element
- [ ] No ASCII topology block in output
- [ ] No SDLC coverage table in output
- [ ] `feat-perf` (no stories, not-started) receives a gap flag
- [ ] Gap analysis still runs on acceptance conditions vs. story coverage

## Failure Criteria

- Practice path triggers on a product project (topology block or SDLC table appears)
- Product type groups (flow/connection/quality) are replaced or missing
- Gap analysis is skipped on product features
- The practice path detection changes how product gap analysis works in any way
- HTML structure differs from pre-practice-extension behavior
