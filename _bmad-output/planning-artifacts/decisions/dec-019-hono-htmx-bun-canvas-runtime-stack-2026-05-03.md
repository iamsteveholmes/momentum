---
id: DEC-019
title: Momentum Canvas Runtime Stack — Hono+HTMX+Bun Supersedes DEC-011 Vite Approach
date: '2026-05-03'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-03'
prior_decisions_reviewed:
  - DEC-011 (Project Canvas Implementation Foundations — D2 Vite build superseded by this decision)
stories_affected:
  - momentum-cycle-dashboard-shell-hono-bun-server
  - momentum-cycle-features-lens
  - momentum-cycle-cycle-timeline-lens
  - momentum-cycle-sprint-lens-sprint-detail-drill-down
  - momentum-cycle-feature-l2-drill-down-reading-mode
  - momentum-cycle-story-l3-drill-down-reading-mode
---

# DEC-019: Momentum Canvas Runtime Stack — Hono+HTMX+Bun Supersedes DEC-011 Vite Approach

## Summary

DEC-011 D2 adopted a Vite + `vite-plugin-singlefile` build for the canvas because the developer preferred a static `file://` artifact with no in-browser transpile cost. That decision was made before Pass 10 of the Claude Design prototype session locked the navigation model: a breadcrumb-as-nav system requiring three addressable screens (dashboard / feature L2 / sprint detail / story L3) with live data polling. A static file cannot serve navigable routes or push live data fragments, making DEC-011 D2 unimplementable against the final design. The replacement stack — Hono + HTMX + Bun — is strictly simpler: one server process, no build step, polling is two HTMX attributes, drill-down navigation maps directly to Hono routes returning HTML fragments. DEC-011 D2 is superseded. DEC-011 D1 (rename to momentum:canvas) and D3 (state source paths under `.momentum/`) remain in force.

---

## Decisions

### D1: Canvas Runtime Stack — Hono+HTMX+Bun — ADOPTED (supersedes DEC-011 D2)

**Developer framing:** DEC-011 D2 adopted Vite + `vite-plugin-singlefile` to produce a static `file://` artifact. That decision was correct given what was known at the time (the design was at Pass 4, navigation model not yet settled). Pass 10 of the 10-pass Claude Design prototype session locked a breadcrumb navigation model requiring three navigable screens with live data polling. A static file cannot do this. The developer requested Hono+HTMX+Bun explicitly in the design review conversation and confirmed the single-file server approach.

**Decision:** Adopt Hono+HTMX+Bun as the runtime stack for momentum-canvas. Implementation:
- `server.tsx` runs on port 3456 via `bun --hot server.tsx` (no compile step, hot-reload in dev)
- Hono handles routing and server-renders JSX fragments using the design tokens from Momentum Cycle - Final.html
- HTMX handles live data: `hx-get="/lenses/features" hx-trigger="every 2s"` on each lens section
- HTMX handles navigation: `hx-push-url="/features/{slug}"` on drill-down links; browser history maintained
- Breadcrumb: `hx-swap-oob="true"` on breadcrumb element, updated with each navigation response
- Polarity flip (dark dashboard → warm light reading): CSS class swap on `.pane-inner`, 140ms CSS transition
- Single file architecture: entire server lives in `skills/momentum/skills/canvas/server.tsx`
- Skill invoker (replacing feature-status): port-check → cmux respawn-pane `bun --hot server.tsx` in services pane → cmux browser open `http://localhost:3456` in viewer pane

This decision supersedes DEC-011 D2 (Vite + vite-plugin-singlefile + `__DATA__` injection) entirely. The shape item `iq-20260426162939-11e0ea57` (__DATA__ injection contract) is consumed — no contract needed.

**Rationale:**
The navigation model (drill-down between dashboard / sprint / feature / story) makes a static file impossible. Pass 10 locked breadcrumb-as-nav which requires a server to handle URL routing. Hono+HTMX+Bun is strictly simpler than the Vite approach: one runtime process, no build step, polling is two HTMX attributes, navigation maps cleanly to Hono routes with HTML fragment responses. DEC-011 D2's "I vastly prefer a static to dynamic page" was written before the navigation requirement was settled in Pass 10. The navigation requirement changes the calculus — the server IS the static build.

---

## Phased Implementation Plan

| Phase | Focus | Key Stories |
|-------|-------|-------------|
| 1 | Server shell + cmux wiring | momentum-cycle-dashboard-shell-hono-bun-server |
| 2 | Live lenses (Features + Cycle timeline) | momentum-cycle-features-lens, momentum-cycle-cycle-timeline-lens |
| 3 | Sprint lens + sprint detail | momentum-cycle-sprint-lens-sprint-detail-drill-down |
| 4 | Feature L2 drill-down | momentum-cycle-feature-l2-drill-down-reading-mode |
| 5 | Story L3 drill-down | momentum-cycle-story-l3-drill-down-reading-mode |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | Phase 1 done | Does the server open cleanly in the cmux viewer pane and handle hot-reload? | `bun --hot server.tsx` starts, port-check idempotent, cmux opens `http://localhost:3456` |
| Gate 2 | Phase 2 done | Does live polling feel right at 2s interval? | Features lens updates within 2s of a features.json write; no flicker on re-render |
