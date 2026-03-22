# Momentum Findings Ledger MCP Server

This is the Momentum findings ledger MCP server, to be implemented in Epic 6.

The server will provide a structured query interface over `~/.claude/momentum/findings-ledger.jsonl` (global, JSONL format). It is not the write path — the flywheel writes directly via JSONL append. The MCP server enables filtered queries (by project, pattern_tag, severity, date range) for pattern detection.

The server will not be configured until Epic 6 delivers a working implementation.

**Status:** Placeholder — implementation in Epic 6 (Story 6.1+).
