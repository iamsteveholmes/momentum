# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal ETL (Extract, Transform, Load) system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. The pipeline uses a staged architecture: Stage 2 completes before Stage 3 begins, enabling data integrity guarantees at each processing boundary.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

API key authentication is used to verify each request before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

Transformation applies exponential backoff retry on transient failures: up to 3 attempts with delays of 1s, 2s, and 4s.

Files exceeding 100MB are handled separately from the primary transformation path via an overflow queue.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache significantly reduces end-to-end latency compared to unbuffered writes by batching warehouse write operations.

Polling for batch completion uses a 5-minute interval. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

See Section 6 — Security Considerations for authentication and access control details.

## Performance Characteristics

Benchmarks show that streaming is 3× faster than batch processing for files under 10MB. For larger payloads, batch processing is preferred.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The pipeline is monitored by the on-call team via the Prometheus dashboard
- Horizontal scaling is supported; add worker instances to increase throughput

## Security Considerations

The pipeline enforces security controls at the ingestion boundary and throughout the processing chain:

- **Authentication:** API key authentication is required for all inbound HTTP POST requests to the ingestion layer. Requests without a valid API key are rejected with a 401 response.
- **Encryption in transit:** All customer data is transmitted over TLS 1.2 or higher between the customer SDK and the ingestion endpoint.
- **Internal service communication:** Internal inter-stage communication occurs within the private network boundary; services are not exposed externally.
- **Access control:** Access to the data warehouse output is restricted to authorized downstream consumers. Credentials are injected via environment variables and not stored in container images.
- **Audit logging:** Authentication failures and rejected events are logged to the dead-letter queue for operational review.

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a real-time streaming pipeline alongside the existing batch pipeline.
