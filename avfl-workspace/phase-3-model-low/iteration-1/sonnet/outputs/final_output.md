# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. Pipeline stages execute sequentially; each stage begins after the preceding stage's output is available.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

Requests are authenticated via API key in the Authorization header before processing begins. Schema validation and authentication are independent checks applied to every inbound request.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

On transient failures, transformation retries with exponential backoff: up to 3 attempts with an initial delay of 1 second, doubling on each retry.

Events exceeding 10MB are handled separately from the primary transformation path via an overflow queue.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache reduces write I/O latency by buffering records before committing to the warehouse.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

Access to pipeline infrastructure is restricted to authenticated operators. API keys and service credentials are rotated on a 90-day schedule; all traffic between pipeline components is encrypted in transit via TLS 1.2 or higher.

## Performance Characteristics

Internal benchmarks show that batch processing is 3× faster than streaming for payloads under 10MB under nominal load conditions. For larger payloads, streaming is preferred.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, delivery, and monitoring based on load patterns. Future work includes adding a real-time streaming workflow alongside the existing batch pipeline.
