# Data Processing Pipeline — Architecture Brief

## Overview

This document describes the architecture for the Meridian Data Processing Pipeline, an internal Extract, Transform, Load (ETL) system that handles batch ingestion, transformation, and delivery of analytics events from customer applications to the data warehouse. Pipeline stages operate sequentially — Stage 1 feeds Stage 2, which must complete before Stage 3 begins — with multiple parallel workers within each stage to maximize throughput.

The pipeline is designed for high-volume event streams and handles approximately 50,000 events per second under peak load.

## Architecture Components

### Stage 1 — Ingestion

The ingestion layer accepts events via HTTP POST from customer SDK agents. Events are validated against a JSON schema on arrival; malformed events are rejected with a 400 response and logged to the dead-letter queue.

HMAC-signed API key authentication is used to verify each request before processing begins.

Accepted events are placed on an internal message queue for downstream processing.

### Stage 2 — Transformation

Stage 2 must complete before Stage 3 begins. The transformation layer normalizes event schemas, enriches records with customer metadata from the reference database, and deduplicates events within a 5-minute window using a Redis cache.

Transformation applies the standard retry policy on transient failures: up to 3 retry attempts with exponential backoff (initial delay 500ms, multiplier 2×, maximum delay 30s).

Files exceeding 50 MB are handled separately from the primary transformation path via an overflow queue.

### Stage 3 — Delivery

The delivery layer writes transformed events to the data warehouse in micro-batches of 500 records. The in-memory delivery cache significantly reduces latency compared to unbuffered writes by absorbing burst load and amortizing write overhead across batches.

Polling for batch completion uses a 5-minute interval for operational monitoring only and is not on the critical delivery path; events are delivered as micro-batches complete. Errors are logged and the batch is requeued for up to 3 retry attempts.

### Stage 4 — Monitoring

The pipeline exposes a metrics endpoint at `/metrics` with standard Prometheus counters for throughput, error rate, and queue depth. Polling for status updates uses a 10-minute interval.

Security considerations are documented in the Security section below.

## Performance Characteristics

Internal testing shows that streaming is typically faster than batch processing for files under 10 MB, where batch overhead is not fully amortized. For larger payloads (above 10 MB), batch processing is preferred due to reduced per-record overhead and more efficient warehouse write patterns.

Under nominal load, the pipeline maintains sub-second end-to-end latency for 95th-percentile events, measured from ingestion acceptance to warehouse write confirmation on the delivery critical path.

## Security

Authentication for inbound requests uses HMAC-signed API keys validated at the ingestion layer. Events are transmitted over TLS 1.2 or higher between all pipeline stages and to the data warehouse. Data at rest in the message queue and Redis cache is encrypted using AES-256. Access to the data warehouse is restricted to service accounts with least-privilege IAM roles. The `/metrics` endpoint is network-access-controlled and not exposed to the public internet.

## Operational Notes

- Deployment is via container image; configuration is injected via environment variables
- The on-call team monitors the pipeline via the Prometheus dashboard; alerting thresholds and escalation procedures are defined in the runbook
- Horizontal scaling is supported; add worker instances to increase throughput

## Conclusions

The Meridian pipeline provides a scalable, fault-tolerant data delivery path. The staged architecture enables independent scaling of ingestion, transformation, and delivery based on load patterns. Future work includes adding a real-time streaming pipeline alongside the existing batch pipeline.
