# Research Prompts Are Date Anchored with Primary Source Directives

Status: backlog
Epic: research-knowledge

## Description

Research agent prompts in the momentum:research skill must enforce citation hygiene beyond source-type labeling. Two gaps exist in the current briefing-template.md:

1. **Deadlink filter** — agents cite URLs without verifying liveness. Broken links degrade corpus quality silently.
2. **Gameable-metrics prohibition** — agents use GitHub stars as a proxy for AI project maturity. Stars are gameable and unreliable; commits, contributor distribution, and download counts are more durable signals.

This story adds explicit directives to the research subagent briefing template (and any other research prompt templates that cite sources) to close both gaps.

**Implementation targets:**
- `skills/momentum/skills/research/references/briefing-template.md` (primary)
- `skills/momentum/skills/research/references/gemini-prompt-template.md` (verify URL guidance applies)
- `skills/momentum/skills/research/references/synthesis-briefing-template.md` (verify gameable-metrics flagging applies at synthesis stage)

**Source:** sprint-2026-04-27 retro + feedback memory: feedback_github_stars_unreliable.md

## Acceptance Criteria

- **AC-1 (Deadlink filter):** The research subagent briefing template includes an explicit instruction to verify URL liveness before citing any source — agents must confirm a URL returns a non-404 response before including it in findings or the Sources section.

- **AC-2 (Gameable-metrics prohibition):** The research subagent briefing template explicitly prohibits GitHub stars (and equivalent vanity metrics such as forks-without-commits and social media follower counts) as maturity signals for AI projects. The directive requires substituting: commit frequency, contributor distribution (bus factor), and download/install counts as the required maturity proxies.

- **AC-3 (Gameable-metrics flagging in output):** Research output (raw files and final synthesis) must flag any gameable metric that appears in source material with a `[GAMEABLE-METRIC]` notation, alongside the preferred substitute signal if available, rather than silently carrying the metric forward as evidence.
