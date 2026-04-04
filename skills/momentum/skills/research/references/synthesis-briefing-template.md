# Synthesis Agent Briefing Template

Use this template when spawning the synthesis agent in Phase 5. Substitute all `{{variables}}`.

---

## Briefing

You are synthesizing a research corpus on: **{{topic}}**

Research goals: {{goals}}
Profile: {{profile}}
Date: {{date}}

### Your Task

Read ALL of the following files from disk (do not rely on prior context — start fresh):

**Raw research files:**
{{list each raw/research-*.md file path, one per line}}

**Additional sources (if present):**
- {{project_dir}}/raw/gemini-output.md (Gemini CLI triangulation — if file exists)
- {{project_dir}}/validation/avfl-report.md (AVFL quality findings — if file exists)
- {{project_dir}}/raw/practitioner-notes.md (human Q&A responses — if file exists)
- {{project_dir}}/scope.md (research scope and sub-questions)

### Output Structure

Load `./references/output-structure.md` for the default structure template. Adapt sections to match the sub-questions from scope.md — the sub-questions drive the document sections, not a fixed template.

Write the final document to: `{{project_dir}}/final/{{topic_slug}}-final-{{date}}.md`

### Provenance Frontmatter

The final document MUST begin with this frontmatter (expand inline — do not use template syntax):

```yaml
---
title: "{{topic}} — Research Report"
date: {{date}}
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: {{true if practitioner-notes.md exists, false otherwise}}
derives_from:
  - path: raw/research-subtopic-1.md
    relationship: synthesized_from
  - path: raw/research-subtopic-2.md
    relationship: synthesized_from
  # ... one entry per raw research file ...
  # Add these only if the files exist:
  - path: raw/gemini-output.md
    relationship: synthesized_from
  - path: validation/avfl-report.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---
```

### Evidence Notation Mapping

Apply these mappings when carrying forward claims from raw sources:

| Raw Notation | Final Status | Meaning |
|---|---|---|
| `[OFFICIAL]` | VERIFIED | Official docs, primary sources |
| `[PRAC]` | CITED | Practitioner blogs, community reports with URL |
| `[UNVERIFIED]` | INFERRED | Reasonable inference, no specific source |
| No attribution | UNGROUNDED | Remove or explicitly flag |
| AVFL-flagged | SUSPECT | Claims that failed AVFL verification |

### Writing Guidelines

- Direct, practitioner-focused prose. Active voice. Short sentences.
- Lead with actionable guidance, follow with evidence/sources
- Cite sources inline: `([Source Name](URL))` with evidence notation
- Mark community-reported claims as such: "Practitioners report..."
- No padding or filler. Respect the reader's time.
- Target 5,000-8,000 words for medium/heavy profiles; 2,000-3,000 for light

### Completion

After writing the file, return a 2-3 sentence summary of the final document to the orchestrator.
