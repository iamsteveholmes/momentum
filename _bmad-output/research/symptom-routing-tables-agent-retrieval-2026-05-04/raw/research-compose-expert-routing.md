---
content_origin: claude-code-subagent
date: 2026-05-04
sub_question: "How was the compose-expert plugin's Quick Routing section authored — hand-written vs. generated from a knowledge index?"
topic: "Symptom-based routing tables for agent knowledge retrieval"
---

## Summary Finding

The Quick Routing section in the compose-expert SKILL.md was **hand-authored** by the plugin's maintainer (Adit Lal, `aldefy`). It was introduced in a discrete, documented release (v2.3.0, 2026-05-03) as a deliberate editorial improvement — not generated from a script, index file, or automated tooling. No generation infrastructure exists in the repository.

## Location of the Plugin

The compose-expert skill is not a Momentum-native skill. It is a third-party plugin installed via the Claude Code plugin marketplace: **[OFFICIAL]**

- Marketplace path: `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/`
- SKILL.md: `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/skills/compose-expert/SKILL.md`
- References: `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/skills/compose-expert/references/`

## The Quick Routing Section — Structure and Content

The Quick Routing section (lines 79–153 of SKILL.md) is a signal-to-file dispatch table introduced with this header: **[OFFICIAL]**

> Use this table first. Match the user's signal to one reference file and read it before answering.

It organizes 33 bullet entries across 7 thematic subsections:

1. State, recomposition, side effects (5 entries)
2. Animation and motion (3 entries)
3. Layout, lists, modifiers (3 entries)
4. Navigation (3 entries)
5. Paging (4 entries)
6. Theming and design systems (4 entries)
7. Multiplatform and platform-specific (3 entries)
8. Interop and accessibility (2 entries)
9. Production, review, migration (5 entries)
10. Source-code receipts (1 grouped entry with 6 sub-bullets)

Each bullet maps a **symptom or API mention** to a specific `references/*.md` file. Secondary references are noted with `(secondary: ...)`. The section covers all 23 reference files accessible in the `references/` directory. **[OFFICIAL]**

## Evidence of Hand-Authorship

### Git History — Single Commit Introduction

The local marketplace clone has exactly **one git commit** in its history: **[OFFICIAL]**

```
6c05a4d Merge pull request #13 from aldefy/fix/skill-description-length
```

This commit is a merge of PR #13 and contains the entire initial state of the plugin as a single squashed history. The SKILL.md file was added in this commit (`296 +` lines).

### CHANGELOG — Explicit Editorial Narrative

The CHANGELOG at `CHANGELOG.md` is the most direct evidence. The v2.3.0 entry reads: **[OFFICIAL]**

> **Quick Routing section in `SKILL.md`**. A signal-to-file table at the top of the skill so Claude lands on the right reference in one read instead of scanning the full topic table. Every reference file is reachable from at least one routing entry.

This describes the authoring rationale in editorial terms — "so Claude lands on the right reference in one read" — indicating a deliberate human design decision about agent retrieval ergonomics, not an automated output.

The CHANGELOG documents the full version history back to v1.0.0 (2026-02-28) and shows the Quick Routing section arrived in v2.3.0, separate from the initial 13-reference launch in v1.0.0. **[OFFICIAL]**

### No Generation Tooling Found

The repository's `scripts/` directory contains only three files: **[OFFICIAL]**

- `check-description-length.sh` — validates frontmatter length cap
- `check-versions.sh` — asserts version consistency across manifests
- `validate-plugin-manifest.sh` — validates plugin.json schema

None of these generate or update the Quick Routing section. There is no script that reads the `references/` directory and emits routing table entries. **[OFFICIAL]**

### No Knowledge Index in References

The `references/` directory contains 23 topic-specific markdown files plus a `source-code/` subdirectory with 6 files. There is no `index.md`, `index.json`, or any file that serves as a knowledge index from which a routing table could be automatically derived. **[OFFICIAL]**

## Structural Analysis — Organic vs. Mechanical

The routing table's structure is characteristic of hand-authorship rather than mechanical generation:

- **Non-uniform entry lengths**: Some bullets are terse ("→ `references/animation.md`"), others include nuanced secondary references and parenthetical qualifications ("secondary: `references/modifiers.md` for `graphicsLayer`"). A generator would produce uniform entries. **[PRAC]**
- **Grouped thematic sections**: The subsections follow conceptual groupings (state vs. animation vs. layout) that reflect editorial judgment about how users think, not how files are named. **[PRAC]**
- **Symptom phrasing**: Several entries use natural-language symptom phrasing ("my screen recomposes too often", "choosing between Nav 2 and Nav 3") that would need an explicit prompt to generate. These read as hand-crafted for usability. **[PRAC]**
- **Source-code receipts handled differently**: These get a single grouped entry with sub-bullets rather than individual routing entries, a deliberate editorial choice to de-emphasize them as primary dispatch targets. **[OFFICIAL]** (text: "cite, don't route to")
- **Every reference covered**: The CHANGELOG explicitly notes "every reference file is reachable from at least one routing entry" — this reads as a human quality check, not a generator guarantee. **[PRAC]**

## What Changed at v2.3.0

The v2.3.0 release (same day as the marketplace clone's single commit, 2026-05-03) added Quick Routing alongside three new Paging 3 reference files and a new navigation-migration reference. **[OFFICIAL]** The routing table was evidently authored alongside the new references — as the author added new files, they updated the routing table to include them. This is consistent with hand maintenance rather than a generated artifact.

## Implications for New Skill Authorship

No reusable generation infrastructure exists in the compose-expert plugin that could be repurposed for a new compose+kotest skill. The routing table is maintained manually alongside the reference files. A new skill would need to either:

1. Hand-author a Quick Routing section following the same pattern **[PRAC]**
2. Write a generation script that introspects reference file frontmatter or headings to auto-produce routing entries — but no such tooling exists today and would need to be built **[PRAC]**

## Sources

All paths examined:

- `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/skills/compose-expert/SKILL.md` — primary artifact
- `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/CHANGELOG.md` — version history and authoring intent
- `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/scripts/` — all three scripts reviewed
- `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/skills/compose-expert/references/` — directory listing, no index.md found
- `/Users/steve/.claude/plugins/marketplaces/aldefy-compose-skill/` — git log (`git log --all --oneline`) showing single-commit history
- `/Users/steve/.claude/plugins/cache/aldefy-compose-skill/compose-expert/2.3.1/` — cached version directory structure (no git history present)
- `/Users/steve/projects/momentum/skills/` — confirmed compose-expert is NOT a Momentum-native skill
