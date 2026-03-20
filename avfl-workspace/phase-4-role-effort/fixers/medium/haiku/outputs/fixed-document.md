# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL (Extract, Transform, Load) system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. Ingestion and transformation stages operate sequentially; delivery begins only after transformation is complete.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

API key authentication is used to verify each request before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

Transformation applies an exponential backoff retry policy (up to 3 attempts, doubling delay on each transient failure) on transient failures.

Files exceeding 100MB are handled separately from the primary transformation path via an overflow queue.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache significantly reduces end-to-end write latency compared to unbuffered writes.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

Security considerations are documented in the Security Considerations section below.

## Performance Characteristics

Internal benchmarks show that streaming is 3× faster than batch for files under 10MB. For larger payloads, batch processing is preferred.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Security Considerations

Authentication is enforced at the ingestion layer via API key validation on every inbound request. All data in transit is encrypted using TLS. Data at rest in the warehouse is encrypted at the storage layer. Access to pipeline configuration and metrics endpoints is restricted to authorized internal services and on-call personnel.

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a real-time streaming capability alongside the existing batch pipeline.
