# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse.

The pipeline is designed as a sequential handoff between stages: Stage 1 feeds Stage 2 which feeds Stage 3, with Stage 4 operating independently for monitoring. Within each stage, processing is parallelized across multiple worker instances to maximize throughput. The pipeline handles approximately 50,000 events per second under peak load.

## Component Inventory

| Component | Role | Stages Served |
|---|---|---|
| HTTP Ingestion Endpoint | Accepts events from customer SDK agents | Stage 1 |
| Message Queue | Buffers accepted events for downstream processing | Stage 1 → Stage 2 |
| Dead-Letter Queue (DLQ) | Holds rejected or undeliverable events for inspection | Stage 1, Stage 3 |
| Transformation Workers | Normalize, enrich, and deduplicate events | Stage 2 |
| Redis Cache | Event deduplication within 5-minute window | Stage 2 |
| Reference Database | Customer metadata for event enrichment | Stage 2 |
| Overflow Queue | Handles large-payload events on degraded path | Stage 2 → Stage 3 |
| Data Warehouse | Final destination for transformed analytics events | Stage 3 |
| Metrics Endpoint | Prometheus-compatible metrics for pipeline observability | Stage 4 |

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

Authentication uses API keys passed via the `Authorization` header with HMAC-SHA256 request signing. Each request is verified before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

**Dead-letter queue handling:** When events are sent to the DLQ, an alert fires when the queue depth exceeds 100 events. The on-call team has a 24-hour inspection window. Manual retry is available via the ops tooling (`pipeline-ops dlq retry`). Events are retained for 7 days, then purged.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

The 5-minute deduplication window is chosen to cover typical network retry delays and upstream clock skew; it is configurable via the `DEDUP_WINDOW_SECONDS` environment variable.

**Retry policy:** On transient failures (5xx responses from downstream services and network timeouts), the transformation stage retries with exponential backoff: attempt 1 after 1 second, attempt 2 after 2 seconds, attempt 3 after 4 seconds. After 3 failed attempts, the event batch is routed to the DLQ and the on-call team is alerted.

Large files (payloads exceeding 50MB) are handled separately from the primary transformation path via an overflow queue. This path delivers to Stage 3 with degraded latency (best-effort; not subject to the sub-second SLA). For payloads above 50MB, streaming decomposition is preferred because memory pressure and parallelism decomposition characteristics favor streaming at that scale.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. Batch size of 500 is chosen to balance warehouse write efficiency against delivery latency; it is configurable via `BATCH_SIZE`.

The in-memory delivery cache reduces end-to-end delivery latency significantly compared to unbuffered writes; the exact improvement depends on payload size and warehouse write throughput.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts (exponential backoff matching Stage 2 policy). After all retries are exhausted, the batch is routed to the DLQ and the on-call team is alerted for manual intervention.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

## Delivery Semantics

The pipeline provides **at-least-once delivery** with effective deduplication within the 5-minute window. Events may be processed more than once upstream (due to retries), but the Stage 2 Redis deduplication layer removes duplicates seen within the window. This yields effectively-once semantics for events arriving within 5 minutes of each other.

Events outside the deduplication window (e.g., delayed retries arriving after 5 minutes) may result in duplicates in the data warehouse. Downstream consumers should be aware of this boundary condition.

## Security

Authentication is via API key with HMAC-SHA256 request signing (see Stage 1). Authorization is enforced at the ingestion endpoint — each API key is scoped to a customer tenant; cross-tenant access is rejected.

All data in transit is encrypted via TLS 1.2+. Data at rest in the data warehouse is encrypted using AES-256. Redis cache data is not persisted to disk; cache contents are ephemeral.

Customer data is isolated by tenant ID at the transformation layer; event enrichment uses only the originating tenant's reference data.

## Performance Characteristics

Benchmarks show that batch processing is 3× faster than streaming for payloads under 10MB. For larger payloads (>10MB), streaming decomposition is preferred because memory pressure and parallelism characteristics at that scale favor streaming over batch buffering.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events. This latency measures the time from event ingestion (Stage 1 acceptance) through transformation (Stage 2) to delivery queue submission (Stage 3 write initiation). It does not include batch completion polling time (which operates on a separate 5-minute interval for delivery confirmation).

**Capacity sizing at 50,000 events/sec peak:**
- Redis: sized for 10M keys (covers 5-minute dedup window at peak load)
- Message queue: capacity 1M events (approximately 20 seconds of peak burst)
- Data warehouse write path: sustains 100K records/sec write throughput

## Availability and SLA

Target pipeline availability: **99.9%** (approximately 8.7 hours downtime per year).

- Recovery Point Objective (RPO): 1 hour (events in the DLQ are retained for 7 days; upstream retry covers shorter windows)
- Recovery Time Objective (RTO): 4 hours

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput at Stage 2 and Stage 3

## Future State

Future work includes adding a real-time streaming workflow alongside the existing batch pipeline, enabling sub-100ms delivery for latency-sensitive event types.

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path with 99.9% availability SLA. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. At-least-once delivery with bounded deduplication provides effectively-once semantics for the common case.
