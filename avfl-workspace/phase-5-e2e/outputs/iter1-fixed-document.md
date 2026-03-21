# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. The pipeline operates in stages with defined sequencing: ingestion feeds into transformation, which must complete before delivery begins. Monitoring runs continuously in parallel with all stages.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Each request is authenticated using HMAC-signed request signatures; unauthenticated requests are rejected before schema validation. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue. Dead-letter events are reviewed by the on-call team via a dedicated DLQ dashboard; events older than 7 days are automatically purged.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

On transient failures, transformation applies an exponential backoff retry policy: up to 5 attempts, with initial delay of 100ms doubling on each attempt, capped at 30 seconds.

Large files (>50MB) are handled separately from the primary transformation path via an overflow queue. Overflow queue events are processed by the same transformation logic but batched at a reduced rate and routed to the same Stage 3 delivery path via a dedicated overflow delivery channel.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache reduces average write latency by approximately 70% compared to unbuffered synchronous writes in benchmark testing (internal benchmark, March 2026, 10K event/sec sustained load on staging infrastructure).

Polling for batch completion uses a 30-second interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. The on-call team monitors the pipeline via the Prometheus dashboard.

Alert thresholds: error rate >1% triggers a P2 alert; queue depth >10,000 events triggers a P1 alert; throughput drop >50% from baseline triggers a P2 alert. SLA targets: 99.5% of events delivered within 60 seconds of ingestion under nominal load. Escalation paths and runbook are maintained in the internal ops wiki at `wiki/pipeline-runbook`.

## Security

Authentication uses HMAC-signed request signatures. Each customer SDK is issued a unique signing key; signatures are validated server-side before schema checking begins. Requests failing authentication are rejected with a 401 response and logged.

All data in transit is encrypted using TLS 1.2 or higher. Data at rest in the data warehouse is encrypted using AES-256. Customer analytics events are treated as potentially containing PII; access to raw event data is restricted to authorized data engineering roles. Data retention policy: raw events are retained for 90 days; aggregated metrics are retained for 2 years. The pipeline operates under SOC 2 Type II compliance requirements.

## Performance Characteristics

Benchmarks conducted on production-equivalent infrastructure (March 2026, 8-core nodes, 32GB RAM, 1Gbps network) show that batch processing achieves 3× higher throughput than record-by-record streaming for payloads under 10MB due to reduced per-record overhead. For larger payloads where memory pressure becomes a factor, streaming mode is preferred to avoid buffering costs.

Under nominal load, the pipeline maintains sub-60-second end-to-end latency for 95th-percentile events from ingestion acknowledgment to data warehouse availability.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a sub-second real-time streaming path for latency-sensitive event categories alongside the existing batch pipeline.
