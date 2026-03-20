# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal Extract, Transform, Load (ETL) system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. Ingestion, transformation, and delivery are implemented as discrete sequential stages; Stage 2 must complete before Stage 3 begins.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

API key authentication is used to verify each request before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

Transformation applies a retry policy on transient failures: up to 3 attempts with exponential backoff (initial delay 1s, max delay 30s); after exhausting retries, the event is routed to the dead-letter queue.

Files exceeding 10MB are handled separately from the primary transformation path via an overflow queue.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache significantly reduces write-path latency compared to unbuffered writes.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

Security considerations are covered in the Security section below.

## Performance Characteristics

Benchmarks show that streaming is faster than batch processing for files under 10MB. For larger payloads (files exceeding 10MB), batch processing is preferred.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events.

## Security

Access to the pipeline ingestion endpoint is controlled via API key authentication. Keys are issued per customer SDK integration and rotated on a 90-day schedule. All event data is transmitted over TLS 1.2 or higher. Internal service-to-service communication uses mutual TLS (mTLS).

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a real-time streaming pipeline alongside the existing batch pipeline.
