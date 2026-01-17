# worker-service

Runs background jobs and scheduled tasks.

## Why this repo exists

Background processing is isolated from request-handling services to prevent long-running tasks from impacting API latency and availability.

## Core Components

### `run_job(job_name: str)`
Executes a named background job.

**Logs:**
- `job_started` — Logged when a job begins execution
- `job_completed` — Logged when a job finishes successfully

## HTTP Interface

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/healthz` | GET | Liveness probe |
| `/readyz` | GET | Readiness probe |
| `/worker/run` | POST | Runs a background job |

### Running the service

```bash
uvicorn src.worker_service.app:app --host 0.0.0.0 --port 8009
```
