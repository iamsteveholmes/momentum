# Momentum Practice Overview

Momentum is an agentic engineering practice layer — global rules, hooks, and workflows that enforce quality standards across every project, automatically.

## The Eight Principles

1. **Authority hierarchy** — rules cascade: global → project → session. Lower levels can't override higher ones.
2. **Quality before speed** — gates run at natural pause points; they don't block, they catch.
3. **Eval-driven development** — skills are validated by behavioral evals, not unit tests.
4. **Provenance by default** — every artifact traces to its source; staleness is detected, not discovered.
5. **Consent at every gate** — no file writes, no merges, no destructive actions without explicit approval.
6. **Graceful degradation** — missing tools reduce capability, not correctness.
7. **Practice compounds** — findings accumulate across stories into a flywheel of systemic improvement.
8. **Bring your own tools** — protocol interfaces mean any tool that satisfies the contract can participate.

## Where to Start

**New to Momentum?** The setup just completed. Your next invocation of `/momentum` goes straight to session orientation.

**Starting a story?** Run `/momentum-dev` — it selects the next unblocked story, creates an isolated worktree, implements via bmad-dev-story, runs AVFL, and proposes the merge.

**Need a new story created?** Run `/momentum-create-story` — it reads your sprint status and builds a comprehensive story file from your epics.

**Key skills available:**
- `/momentum-dev` — implement the next story
- `/momentum-create-story` — create the next story
- `/momentum-plan-audit` — audit a plan before exiting plan mode
