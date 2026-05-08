---
source: web research synthesis
fetched: 2026-04-26
confidence: high
---

# Raw: A2A Protocol and SDK Landscape

## A2A (Agent-to-Agent) Protocol

- Created by Google, now under Linux Foundation
- v1.0 released March 2026
- 23.4k GitHub stars
- Transport: JSON-RPC 2.0 over HTTP(S), plus REST & gRPC in v1.0
- Official SDKs: Python, JS/TS, Go, Java, .NET
- Inspector: web-based debug tool at github.com/a2aproject/a2a-inspector

## Rust A2A Options

### ra2a (community, 164 stars)
- GitHub: github.com/qntx/ra2a
- crates.io: published
- Full v1.0 spec: JSON-RPC, REST, gRPC, SSE streaming, push notifications, SQL storage, interceptors
- All 12 A2A v1.0 operations
- Client + server

### a2a-rs (official, 19 stars)
- GitHub: github.com/a2aproject/a2a-rs
- Very early, less complete than ra2a

## Go A2A CLI

- `a2a-go` ships a CLI: `a2a discover`, `a2a send`, `a2a serve`
- Proves there's demand for command-line A2A interaction
