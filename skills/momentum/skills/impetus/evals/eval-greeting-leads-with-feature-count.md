# Eval: Greeting Leads With Feature Count

## Scenario

Given a fixture `.momentum/features.json` holding 8 feature entries — 2 with `status: "passing"`,
5 with `status: "failing"`, 1 with `status: "absent"` — and no pending gate card awaiting the
developer, when a fresh session starts and Impetus renders the situational report:

The skill should:
1. Lead the report with the feature headline "2 of 8 feature acceptance conditions passing" —
   ahead of ledger counts, sprint name, handoff context, or any story number
2. Still surface the honest ledger counts (open entries, this week, older than 30 days, near
   auto-close) and any recurring-pattern signal inline, within the same report
3. Keep the whole report to at most 2 sentences
4. Leave `.momentum/features.json` byte-identical after the run

## NOT Expected

- Any fact (sprint name, handoff context, story count) preceding the feature headline
- The headline stating numbers other than 2 of 8
- Ledger counts or the recurring-pattern signal dropped to make room for the headline
- The report exceeding 2 sentences
- Any write to `.momentum/features.json`
