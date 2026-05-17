---
name: agent-builder
description: Per-agent composer for Tier 2 agents. Accepts base_body_path, constitution excerpt, and manifesto inputs (role × domain) to produce a composed agent file and a matching routing entry in momentum/agents.json. Use when building a composed agent for a specific role × domain pair. Called by build-agents once per pair. For change_type:agent stories, sprint-dev routes here. Also user-invocable as momentum:agent-builder.
model: sonnet
effort: medium
user-invocable: true
allowed-tools: Read Grep Glob Bash Edit Write Skill
---

Follow the instructions in ./workflow.md.
