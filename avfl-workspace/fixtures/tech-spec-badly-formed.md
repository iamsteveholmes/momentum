# DataSync API Integration Specification

## Overview
This document describes the integration specification for the DataSync API.

## Authentication
All requests must include a Bearer token in the Authorization header.

## Endpoints

### POST /sync
Initiates a data synchronization job. Returns a job ID for polling.

See Section 5 for error codes and handling procedures.

## Rate Limits
Standard tier: 100 requests/hour.
