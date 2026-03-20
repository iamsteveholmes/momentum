# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. The pipeline stages are interconnected with explicit dependencies to ensure data consistency.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

Authentication is used to verify each request before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. This sequential dependency ensures data quality. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute sliding window; Redis cache stores event fingerprints for comparison, with expired entries automatically flushed.

Transformation applies the standard retry policy on transient failures.

Large files are handled separately from the primary transformation path via an overflow queue. When input size exceeds configured thresholds, events route to the overflow queue for separate batch processing to prevent memory exhaustion.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache reduces end-to-end latency compared to unbuffered writes.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. The monitoring layer continuously collects performance data and alerts the on-call team to anomalies. Polling for status updates uses a 10-minute interval, balancing operational visibility with system overhead. Key monitored metrics include end-to-end latency, error rates at each stage, and queue saturation points.

## Performance Characteristics

Testing indicates that batch processing typically performs better than streaming for files under 10MB due to reduced I/O overhead. For larger payloads, streaming is preferred.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline and workflow are monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a real-time streaming workflow alongside the existing batch pipeline.
