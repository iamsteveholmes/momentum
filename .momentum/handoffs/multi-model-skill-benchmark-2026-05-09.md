# Multi-Model Skill Benchmark Handoff

**Date:** 2026-05-09
**Author:** opencode (GLM-5.1 session)
**Status:** Test invalidated — methodology fix required before re-run

---

## What We Tried

Benchmark 6 coding models against a real implementation story (`campaign-init-screen-integration`) to compare quality, cost, and speed. Each model was given the same story spec and told to implement all acceptance criteria, saving outputs to `/tmp/campaign-init-bench/<model>/outputs/`.

### Models Tested

| Model | OpenRouter ID | Cost | Duration | Files Out |
|-------|--------------|------|----------|-----------|
| MiniMax M2.7 | `minimax/minimax-m2.7` | $0.15 | 9m11s | 7 |
| DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` | $0.67 | 14m18s | 26 |
| MiMo V2.5 Pro | `xiaomi/mimo-v2.5-pro` | $0.57 | 20m7s | 7 |
| Sonnet 4 | `anthropic/claude-sonnet-4` | $2.27 | ~5m | 11 |
| GLM-5.1 | `z-ai/glm-5.1` | $2.55 | 14m39s | 8 |
| Qwen 3.6 Plus | `qwen/qwen3.6-plus` | $0.80 | 6m39s | 13 |

### Judge Models

Three top-tier models evaluated the outputs independently:

| Judge | OpenRouter ID |
|-------|--------------|
| Opus 4.7 | `anthropic/claude-opus-4.7` |
| Gemini 3.1 Pro | `google/gemini-3.1-pro-preview` |
| Grok 4.3 | `x-ai/grok-4.3` |

---

## What Went Wrong

### 1. Story Leaked the Answer

The story file (`status: done`) contained a **Dev Agent Record** and **File List** documenting the canonical implementation. When models read the story, they also saw exactly which files implement it. Five of six models recognized this and retrieved/adapted the existing code from `nornspun-client/`. Only Sonnet 4 wrote independently — and it produced buggy code.

**Result:** We tested file-retrieval fidelity, not implementation ability. The top 5 outputs were essentially copies of existing code with varying degrees of trimming and formatting.

### 2. Task Tool Hangs on Some Models

MiMo, MiniMax, and DeepSeek all hung when they spawned `Task` (subagent) tool calls. The parent `opencode run` process would wait indefinitely while the subagent session died silently. Only models that avoided subagents (or were instructed not to use them) completed reliably.

**Fix:** Add `IMPORTANT: Do NOT use the Task tool or spawn subagents. Do all exploration and implementation directly using Read, Glob, Grep, Bash, and Write tools yourself.` to the prompt.

### 3. Model ID Pitfalls

OpenRouter model IDs have quirks:
- `x-ai/grok-4.20-multi-agent` → must be `x-ai/grok-4.20-multi-agent-beta`
- `x-ai/grok-4.20` → doesn't support tool use; use `x-ai/grok-4.3`
- Always verify IDs via `curl -s https://openrouter.ai/api/v1/models | python3 -c "..."`

### 4. Credit Limits

Sonnet 4 died on first run with "This request requires more credits". After adding credits, it ran fine. Pre-fund the account or expect interruptions.

---

## How to Fix the Benchmark

### Scrub the Story

Before re-running, strip the Dev Agent Record and File List from the story file:

```bash
# Copy the story and remove the leaked answer sections
python3 -c "
import re, sys
with open('/Users/steve/projects/nornspun/.momentum/stories/campaign-init-screen-integration.md') as f:
    content = f.read()
# Remove everything from '## Dev Agent Record' onward
content = re.sub(r'\n## Dev Agent Record.*', '', content, flags=re.DOTALL)
# Also change status to in-progress
content = content.replace('status: done', 'status: in-progress')
with open('/tmp/campaign-init-bench/story-scrubbed.md', 'w') as f:
    f.write(content)
"
```

Then reference `/tmp/campaign-init-bench/story-scrubbed.md` in the prompt instead of the original.

### Recommended Value Additions

The original test missed the best value coding models:

| Model | OpenRouter ID | Why |
|-------|--------------|-----|
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | Legendary price/perf for coding |
| DeepSeek V4 Flash | `deepseek/deepseek-v4-flash` | Same family as Pro, much cheaper |
| Qwen 3.6 27B | `qwen/qwen3.6-27b` | Smaller Qwen, still solid |
| Grok 4.1 Fast | `x-ai/grok-4.1-fast` | xAI's fast/cheap variant |

---

## How to Run the Test (cmux + OpenRouter)

### Prerequisites

1. OpenRouter account with credits loaded
2. `opencode` CLI installed and configured with OpenRouter provider
3. `cmux` running (the macOS terminal multiplexer)
4. The frontend-dev skill copied to the target project so subagents can see it:
   ```bash
   cp -r ~/projects/nornspun-client/.claude/skills/frontend-dev \
         ~/projects/nornspun/.claude/skills/frontend-dev
   ```

### Step 1: Identify Your cmux Context

```bash
cmux identify --json
```

Note the `pane_ref` and `window_ref`. You'll split off a new pane for the benchmark tabs.

### Step 2: Create the Right Pane

```bash
# Split the current pane to the right
cmux new-split right --panel pane:<your_pane>
```

This creates a new pane (e.g. `pane:55`). All benchmark tabs will live in this pane.

### Step 3: Create One Tab Per Model

```bash
# For each model, create a new terminal tab in the right pane
cmux new-surface --type terminal --pane pane:55
```

Each `new-surface` returns a surface ID (e.g. `surface:110`, `surface:111`, etc.). Track these.

### Step 4: Launch All Models Concurrently

Send the `opencode run` command to each surface. The key flags:

- **`-m openrouter/<provider>/<model>`** — selects the model
- **`--dangerously-skip-permissions`** — auto-approves tool calls (otherwise writes to `/tmp` get auto-rejected)
- **`--title "benchmark-<name>"`** — labels the session in the DB for later querying
- **`--` at the end** — the prompt follows

The prompt MUST include the anti-subagent instruction and the scrubbed story path:

```bash
PROMPT='You are implementing a feature for the nornspun-client Compose Multiplatform project. Use whatever skills are available to you. IMPORTANT: Do NOT use the Task tool or spawn subagents. Do all exploration and implementation directly using Read, Glob, Grep, Bash, and Write tools yourself.

The story specification is at: /tmp/campaign-init-bench/story-scrubbed.md

Read the story and implement all acceptance criteria.

Save all Kotlin source files to /tmp/campaign-init-bench/<MODEL_NAME>/outputs/ and write an APPROACH.md explaining what skills you used, your methodology, and your choices.'

# For each model, send to its tab:
cmux send --surface surface:<ID> "opencode run -m openrouter/<provider>/<model> --dangerously-skip-permissions --title 'benchmark-<name>' \"$PROMPT\""
cmux send-key --surface surface:<ID> Enter
```

Example for all 6 original models + 4 value models (10 concurrent):

```bash
MODELS=(
  "minimax/minimax-m2.7|minimax-m2.7"
  "deepseek/deepseek-v4-pro|deepseek-v4-pro"
  "xiaomi/mimo-v2.5-pro|mimo-v2.5-pro"
  "anthropic/claude-sonnet-4|sonnet-4"
  "z-ai/glm-5.1|glm-5.1"
  "qwen/qwen3.6-plus|qwen3.6-plus"
  "google/gemini-2.5-flash|gemini-25-flash"
  "deepseek/deepseek-v4-flash|deepseek-v4-flash"
  "qwen/qwen3.6-27b|qwen3.6-27b"
  "x-ai/grok-4.1-fast|grok41-fast"
)

for entry in "${MODELS[@]}"; do
  IFS='|' read -r model_id dir_name <<< "$entry"
  SURFACE=$(cmux new-surface --type terminal --pane pane:55 2>&1 | awk '{print $2}')
  cmux send --surface "$SURFACE" "opencode run -m openrouter/$model_id --dangerously-skip-permissions --title 'benchmark-$dir_name' 'You are implementing a feature for the nornspun-client Compose Multiplatform project. Use whatever skills are available to you. IMPORTANT: Do NOT use the Task tool or spawn subagents. Do all exploration and implementation directly using Read, Glob, Grep, Bash, and Write tools yourself.

The story specification is at: /tmp/campaign-init-bench/story-scrubbed.md

Read the story and implement all acceptance criteria.

Save all Kotlin source files to /tmp/campaign-init-bench/$dir_name/outputs/ and write an APPROACH.md explaining what skills you used, your methodology, and your choices.'"
  cmux send-key --surface "$SURFACE" Enter
  echo "Launched $model_id on $SURFACE"
  sleep 1
done
```

### Step 5: Monitor Progress

```bash
# Quick scan of all tabs
for s in 110 111 112 113 114 115; do
  echo "=== surface:$s ==="
  cmux read-screen --surface surface:$s --lines 3 2>&1 | tail -2
  echo
done
```

Models are done when you see the shell prompt return (e.g. `momentum on ... took XmYs`).

### Step 6: Run Judges (Same Pattern)

Create 3 more tabs, one per judge model. Use the evaluation prompt at `/tmp/campaign-init-bench/judge_prompt.md`:

```bash
JUDGES=(
  "anthropic/claude-opus-4.7|opus47"
  "google/gemini-3.1-pro-preview|gemini31pro"
  "x-ai/grok-4.3|grok43"
)

for entry in "${JUDGES[@]}"; do
  IFS='|' read -r model_id judge_name <<< "$entry"
  SURFACE=$(cmux new-surface --type terminal --pane pane:55 2>&1 | awk '{print $2}')
  cmux send --surface "$SURFACE" "opencode run -m openrouter/$model_id --dangerously-skip-permissions --title 'judge-$judge_name' 'Read the evaluation instructions at /tmp/campaign-init-bench/judge_prompt.md and execute them. Write your evaluation to /tmp/campaign-init-bench/JUDGE_${judge_name}.md'"
  cmux send-key --surface "$SURFACE" Enter
done
```

### Step 7: Extract Costs from DuckDB

```bash
duckdb ~/.local/share/opencode/opencode.db -c "
WITH msgs AS (
  SELECT 
    regexp_extract(m.data::varchar, '\"modelID\":\"([^\"]+)\"', 1) as model,
    CAST(regexp_extract(m.data::varchar, '\"cost\":([0-9.]+)', 1) AS DOUBLE) as cost
  FROM message m
  JOIN session s ON m.session_id = s.id
  WHERE s.title LIKE 'benchmark%'
  AND m.data::varchar LIKE '%assistant%'
  AND m.data::varchar LIKE '%cost%'
)
SELECT model, round(sum(cost), 4) as total_cost, count(*) as steps
FROM msgs
GROUP BY model
ORDER BY total_cost DESC
"
```

### Step 8: Consolidate Judge Evaluations

Read all `JUDGE_*.md` files, compare rankings, and produce a consolidated report noting:
- Where judges agree (strong signal)
- Where judges disagree (needs human review)
- Cost/quality tradeoffs

### Step 9: Teardown

```bash
# Remove the skill copy from nornspun (keeps project clean)
rm -rf ~/projects/nornspun/.claude/skills/frontend-dev

# Optionally clean /tmp outputs
# rm -rf /tmp/campaign-init-bench
```

---

## Key Lessons

1. **Never use a `status: done` story for implementation benchmarks** — it leaks the canonical implementation
2. **Always add anti-subagent instructions** — the Task tool hangs on ~50% of OpenRouter models
3. **Verify model IDs against the live API** — OpenRouter suffix conventions change (`-beta`, `-preview`, etc.)
4. **Pre-fund credits** — high-output models burn through balance fast
5. **Run judges from diverse providers** — reduces provider-specific bias
6. **Cost is queryable from DuckDB** after the fact — no need to track it manually
