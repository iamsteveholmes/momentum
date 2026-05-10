---
title: "Symptom-based routing tables for agent knowledge retrieval — Research Report"
date: 2026-05-04
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/research-momentum-ecosystem-routing.md
    relationship: synthesized_from
  - path: raw/research-compose-expert-routing.md
    relationship: synthesized_from
  - path: raw/research-community-patterns-dec001.md
    relationship: synthesized_from
---

## Executive Summary

No skill or tool exists — in Momentum, in the compose-expert plugin, or in the broader community — that generates symptom→reference routing tables from a knowledge index. Hand-author the routing table for the new compose+kotest skill, following compose-expert's `## Quick Routing` pattern and DEC-015's prescriptive scenario format.

## Sub-Question 1 — Momentum ecosystem

Momentum has no generator for symptom→reference routing tables. The implemented `agent-guidelines` skill (Gen-1) produces path-scoped rules and reference docs plus a coarse "load this doc for this technology" CLAUDE.md pointer — not symptom-grained routing. (VERIFIED: `skills/momentum/skills/agent-guidelines/workflow.md`)

The planned `build-guidelines` skill (Gen-2) names a Tier 1 "constitution" containing trigger tables, but it sits in backlog with no implementation. (VERIFIED: `.momentum/stories/build-guidelines-skill.md`) Even when shipped, its architecture differs from compose-expert's inline-SKILL.md approach — it generates a separately loaded constitution document.

Grepping Momentum's skills tree for "Quick Routing", "routing table", and "symptom" returns zero hits in SKILL.md context. (VERIFIED)

## Sub-Question 2 — compose-expert authoring

The compose-expert `## Quick Routing` section was hand-authored by maintainer Adit Lal and shipped in v2.3.0 (2026-05-03). The CHANGELOG describes deliberate editorial intent: "so Claude lands on the right reference in one read instead of scanning the full topic table." (VERIFIED: `~/.claude/plugins/marketplaces/aldefy-compose-skill/CHANGELOG.md`)

No generation tooling exists in the repo — the three scripts present validate frontmatter, versions, and manifest schema only. There is no `index.md` in `references/` from which a table could be derived. (VERIFIED) Structural tells of hand-authorship: non-uniform entry lengths, thematic groupings reflecting user mental models, natural-language symptom phrasing, and explicit editorial choices like grouping source-code receipts under one entry. (CITED)

## Sub-Question 3 — Community patterns and DEC-001

DEC-001 prescribes that trigger tables belong in Tier 1 hot constitution but does not specify *how* to author them. (VERIFIED: `dec-001-three-tier-agent-guidelines-2026-04-09.md`) DEC-015 refines this: triggers must be prescriptive named scenarios, not vague permissions, because "the LLM will always prefer using training data." (VERIFIED) DEC-018 adds that triggers must name exact `wiki-query` invocation syntax per scenario. (VERIFIED)

No community tool generates symptom→reference tables from a knowledge index. SkillRouter (arxiv 2603.22455) handles runtime skill routing, not static table generation. (VERIFIED) The `metaskill` repo (xvirobotics) generates routing tables but for agent-to-role dispatch, not symptom-to-reference. (CITED) Anthropic's official skill best practices treat trigger descriptions as hand-authored. (VERIFIED)

## Recommendation

Hand-author the compose+kotest routing table now. Model the structure on compose-expert's `## Quick Routing` (thematic groupings, symptom phrasing, secondary references, every reference reachable). Apply DEC-015's prescriptive language — name scenarios as imperatives, not permissions. File a backlog item to revisit if `build-guidelines` ships and the knowledge index outgrows manual maintenance.
