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

### `load_config(service_name: str) -> ServiceConfig`
Loads service configuration from environment variables including `APP_ENV` and `SHUTDOWN_TIMEOUT_SECONDS`.

### `AppError`
Base exception class for application errors. Provides `to_log_fields()` for structured error logging.

### `install_signal_handlers(service_logger_name: str)`
Installs SIGINT/SIGTERM handlers for graceful shutdown with logging.

### `init_correlation_id() -> str`
Initializes a correlation ID from the `CORRELATION_ID` environment variable or generates a UUID4.

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
