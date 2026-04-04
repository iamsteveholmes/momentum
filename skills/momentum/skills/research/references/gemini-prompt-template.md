# Gemini Deep Research Prompt Template

Generate a Gemini Deep Research prompt from the research scope. Substitute all `{{variables}}`.

---

## Template

```
Research Topic: {{topic}}

I need a comprehensive analysis of {{topic}}.

Research Goals: {{goals}}

Key questions to investigate:

1. [First sub-question from scope.md]
2. [Second sub-question from scope.md]
3. [Third sub-question from scope.md]
(expand inline — one numbered entry per sub-question from scope.md)

Desired output: A structured report with findings organized by question, including:
- Specific actionable recommendations where available
- Example patterns or implementations where relevant
- Citations with URLs for every factual claim
- An honest assessment of current limitations and gaps

Date context: Today is {{date}}. Prioritize current and recent sources.
```

## Usage Notes

- Generate this prompt from the scope.md sub-questions
- Write the generated prompt to `raw/gemini-prompt.md` before offering to run
- The `{{#each}}` syntax is illustrative — expand the sub-questions inline as a numbered list
- Gemini Deep Research performs best with specific, bounded questions rather than broad open-ended topics
- If more than 6 sub-questions, consider grouping related ones for the Gemini prompt while keeping them separate for Claude subagents
