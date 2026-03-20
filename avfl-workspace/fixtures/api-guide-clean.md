# Momentum Analytics API Integration Guide

## Version
v2.1.0 | Updated: 2026-03-15

## Overview
The Momentum Analytics API provides programmatic access to workflow metrics, quality scores, and validation results. This guide covers authentication, available endpoints, request/response formats, and error handling.

## Prerequisites
- A Momentum account with API access enabled
- An API key (generated in Settings → Developer → API Keys)
- HTTP client capable of sending JSON requests

## Authentication
All requests must include your API key in the `X-Momentum-Key` header.

```http
GET /v2/metrics HTTP/1.1
Host: api.momentum.example.com
X-Momentum-Key: mk_live_abc123xyz
```

## Endpoints

### GET /v2/metrics
Returns aggregate quality metrics for your workspace.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start_date | string (ISO 8601) | Yes | Start of reporting period |
| end_date | string (ISO 8601) | Yes | End of reporting period |
| workflow | string | No | Filter by workflow name |

**Response (200 OK):**
```json
{
  "period": { "start": "2026-03-01", "end": "2026-03-15" },
  "total_validations": 142,
  "clean_rate": 0.84,
  "avg_score": 91.3,
  "avg_iterations": 2.1
}
```

**Errors:**

| Code | Meaning |
|------|---------|
| 400 | Invalid date range |
| 401 | Missing or invalid API key |
| 429 | Rate limit exceeded |

### GET /v2/validations/{id}
Returns details for a specific validation run.

**Path parameters:**
- `id` (string, required): Validation run ID

**Response (200 OK):**
```json
{
  "id": "val_abc123",
  "status": "CLEAN",
  "score": 97,
  "iterations": 2,
  "findings_fixed": 3,
  "duration_ms": 14200
}
```

**Errors:**

| Code | Meaning |
|------|---------|
| 401 | Missing or invalid API key |
| 404 | Validation run not found |

## Rate Limits
All tiers: 100 requests/hour. Exceeded requests return HTTP 429 with a `Retry-After` header indicating seconds until the limit resets.

## Error Response Format
All errors use this structure:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "You have exceeded 100 requests per hour.",
    "retry_after": 1823
  }
}
```
