# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal Extract, Transform, Load (ETL) system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. Pipeline stages execute in sequence: ingestion feeds transformation, which must complete before delivery begins. Monitoring runs continuously alongside all stages.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

API key authentication is used to verify each request before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

Transformation applies the standard retry policy on transient failures: exponential backoff with an initial delay of 5 seconds, doubling on each attempt, up to a maximum of 3 retry attempts.

Files exceeding 100MB are handled separately from the primary transformation path via an overflow queue.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache significantly reduces end-to-end latency compared to unbuffered writes.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

## Security

Authentication for inbound requests is enforced at the ingestion layer using API key authentication. Keys are issued per customer SDK integration and rotated on a 90-day cycle.

All data in transit between pipeline stages is encrypted using TLS 1.2 or higher. Access to the metrics endpoint is restricted to the internal monitoring network.

Authorization for warehouse writes is governed by the service account assigned to the delivery layer; the account has write-only access scoped to the target analytics schema.

## Performance Characteristics

For small, frequent event payloads, streaming offers lower per-event latency. Batch processing provides higher throughput for large payloads by amortizing per-batch overhead; for payloads exceeding 10MB, batch processing is preferred.

Under nominal load, the pipeline maintains sub-second ingestion-to-transformation latency for 95th-percentile events. End-to-end confirmed delivery latency (ingestion through warehouse write acknowledgment) is governed by the Stage 3 batch polling interval of 5 minutes.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a real-time streaming pipeline alongside the existing batch pipeline.
