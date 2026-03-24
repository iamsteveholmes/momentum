# Eval: Subagent Result Synthesis

## Scenario

Given a subagent returns a structured JSON result with findings, Impetus must synthesize the findings in its own voice. The hub-and-spoke contract must be maintained: the developer never learns which subagent produced the findings.

Subagents return structured JSON conforming to the contract:
```json
{
  "status": "complete|needs_input|blocked",
  "result": { ... },
  "question": null | "string",
  "confidence": "high|medium|low"
}
```

Impetus synthesizes from this contract — never from free-form prose.

## Expected Behavior

- Raw JSON never appears in the response to the developer
- Subagent identity is never surfaced — no "the code reviewer said", "the VFL found", or tool/agent names
- Findings use Impetus's voice: "the review found" or "I found", not third-party attribution
- Severity indicators are used: `!` prefix for critical/blocking findings, `·` prefix for minor/informational findings
- Critical findings (`!`) trigger a flywheel offer when `momentum-upstream-fix` is available
- If flywheel skill is not installed, critical findings include a deferral note: "flywheel processing deferred — Epic 6"
- Confidence directs synthesis: high → synthesize directly; medium → flag explicitly ("inferred — verify"); low → surface as question to the developer

## NOT Expected

- Raw JSON or structured data shown to the developer
- Subagent names mentioned (e.g., "the code reviewer", "momentum-avfl", "the VFL agent")
- Findings without severity indicators (`!` or `·`)
- Critical findings presented without flywheel offer or deferral note
- All findings treated the same regardless of confidence level
