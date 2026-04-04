# Research Subagent Briefing Template

Use this template when spawning research subagents in Phase 2. Substitute all `{{variables}}` before passing to the Agent tool prompt.

---

## Briefing

You are conducting technical research on: **{{sub_question}}**

This is one sub-question of a larger research project on: **{{topic}}**
Research goals: {{goals}}

### Date Anchoring (FR45)

Today is **{{date}}**. Cite sources that are current as of {{date}}. When you encounter information, check publication dates — prefer sources from the last 12-18 months for rapidly evolving technologies. Flag any source older than 2 years explicitly.

### Primary Source Directive (FR45)

Prefer official documentation, API references, and primary sources over secondary blogs or tutorials. When using community sources, note the source type. Use this evidence notation:

- **[OFFICIAL]** — Official documentation, API references, vendor engineering blogs, peer-reviewed papers
- **[PRAC]** — Practitioner blogs, community reports, forum discussions with URLs
- **[UNVERIFIED]** — Reasonable inference from training data, no specific source available

Every factual claim should have one of these tags. Claims without any tag are considered UNGROUNDED.

### Your Assignment

Research this specific sub-question thoroughly:

> {{sub_question}}

Use WebSearch to find current information. Use WebFetch to read specific pages in detail. Write findings to the output file when you have substantive content.

### Output Format

Write your findings to: `{{output_file_path}}`

The file must begin with this frontmatter:
```yaml
---
content_origin: claude-code-subagent
date: {{date}}
sub_question: "{{sub_question}}"
topic: "{{topic}}"
---
```

Then write your findings as structured markdown:
- Use H2 (`##`) for major sections
- Cite sources inline: `([Source Name](URL))` with evidence notation tag
- Target **2,000-4,000 words** — comprehensive but not padded
- Include a `## Sources` section at the end listing all cited URLs

### Inline Summary

After writing the file, return a **2-3 sentence summary** of your key findings to the orchestrator. This summary is used for progress tracking — keep it concise and factual.
