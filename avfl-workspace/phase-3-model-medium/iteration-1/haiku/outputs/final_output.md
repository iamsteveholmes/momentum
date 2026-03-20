# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse.

### Execution Model

The pipeline uses a hybrid execution model:

```
Continuous: Ingestion <---> Monitoring (parallel, independent)
                          |
                          v
Sequential: Transformation --> Delivery (Transformation must complete before Delivery begins)
```

In plain terms:
- **Ingestion** accepts events continuously from SDK agents
- **Monitoring** operates in parallel, collecting metrics and status
- **Transformation** processes the ingested events and must complete before Delivery
- **Delivery** writes transformed events to the warehouse

This hybrid approach maximizes throughput (independent ingestion/monitoring) while ensuring consistency (ordered transformation-to-delivery).

### Performance and Capacity

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. The processing sequence is:

1. **Authentication**: Each HTTP request is authenticated before any processing begins
2. **Validation**: Authenticated events are validated against a JSON schema; malformed events are rejected with a 400 HTTP response code
3. **Queuing**: Accepted events are placed on an internal message queue for downstream processing

Rejected events are logged to the dead-letter queue for analysis and replay.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins, ensuring all records are enriched and deduplicated before delivery. The transformation layer:

- Normalizes event schemas to a canonical format (defined as: a JSON structure with required fields: timestamp, user_id, event_type, properties, and metadata; see Schema specification document for full details)
- Enriches records with customer metadata from the reference database
- Deduplicates events within a 5-minute window using a Redis cache
- Applies exponential backoff retry policy on transient failures (max 3 retry attempts)

Large files are handled separately from the primary transformation path via an overflow queue to prevent blocking normal-sized payloads.

### Stage 3 — Delivery

The delivery layer writes transformed records to the data warehouse in micro-batches of 500 records. The processing flow:

- In-memory delivery cache buffers records between transformations and warehouse writes
- Polling for batch completion uses a 5-minute interval (configurable; baseline derived from micro-batch size and network throughput)
- Errors are logged to the pipeline monitoring system
- Failed batches are requeued for up to 3 retry attempts before escalation

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters:
- Throughput (events/sec)
- Error rate (errors/sec)
- Queue depth (pending records by stage)

Polling for status updates uses a 10-minute interval (slower than Stage 3 because system health is less time-critical than delivery completion). Monitoring runs in parallel with Ingestion to provide real-time visibility.

Security considerations are documented in Section 5 below.

## Security

The pipeline implements the following security controls:

- **Authentication**: All inbound HTTP requests require valid API credentials; authentication occurs before validation
- **Encryption**: Events are encrypted in transit (TLS 1.2+) and at rest in the message queue
- **Access Control**: Role-based access control limits who can configure, deploy, and monitor the pipeline
- **Audit Logging**: All administrative actions and anomalies are logged to a secure audit trail
- **Data Retention**: Event records are retained according to compliance requirements (see operational runbook for retention policy details). Current practice: records are retained for a configurable period after warehouse delivery, then purged.

## Performance Characteristics

Performance testing shows:

- **Batch vs. Streaming**: For payloads under 10MB, the current batch architecture processes at approximately 3x throughput compared to streaming. This improvement comes from reduced per-event processing overhead: batch mode amortizes validation, authentication, and metadata lookup costs across multiple events, whereas streaming processes these steps individually. Streaming is preferred for real-time requirements with payloads >10MB.
- **End-to-End Latency**: Under nominal load (50% peak capacity), the pipeline maintains sub-second end-to-end latency for the 95th percentile of events. Typical latency: 200-500ms per event.
- **Cache Impact**: The in-memory delivery cache reduces queue wait time by approximately 15-20% compared to direct warehouse writes, improving perceived latency from micro-batch timeout perspective.

**Note**: All benchmarks assume standard AWS instance sizing (c5.2xlarge compute, io1 storage) and typical JSON event sizes (2-5KB). Performance varies with hardware configuration and event size. For different hardware or event sizes, contact the platform team for updated benchmarks.

## Operational Notes

- **Deployment**: The pipeline is deployed via container image; configuration is injected via environment variables
- **Monitoring**: The pipeline and workflow are monitored by the on-call team via the Prometheus dashboard at `/metrics`
- **Scaling**: Horizontal scaling is supported by adding worker instances. Scaling recommendations:
  - Add workers when per-stage queue depth exceeds 10% of configured batch window
  - Typical performance observed: 8-12 workers per stage provide optimal throughput-to-cost ratio; scaling beyond this range has shown diminishing returns due to increased contention (use caution when scaling to >12 workers)
  - Monitor CPU and network utilization; scale to maintain <70% utilization
- **Troubleshooting**: Common issues, resolution steps, and performance tuning guidance are documented in the operational runbook (maintained separately; contact platform team for access)

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns.

The current implementation prioritizes batch throughput and consistency guarantees. Future enhancements under consideration include:
- Adding a parallel real-time streaming path for low-latency events (analysis phase only; not scheduled)
- Replacing Redis deduplication with a distributed cache for multi-region deployments
- Implementing adaptive batch sizing based on load patterns
