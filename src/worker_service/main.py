"""
Service entrypoint with lifecycle management.

Initializes configuration, correlation ID, and signal handlers before running
the main service logic. Provides structured error handling for all exceptions.
"""
from core_logger import get_logger

from worker_service.config import load_config
from worker_service.errors import AppError
from worker_service.lifecycle import install_signal_handlers
from worker_service.observability import init_correlation_id

logger = get_logger("worker-service")


def run_job(job_name: str) -> None:
    logger.info("job_started", job_name=job_name)
    logger.info("job_completed", job_name=job_name)


def run() -> None:
    cfg = load_config("worker-service")
    cid = init_correlation_id()
    install_signal_handlers("worker-service")

    logger.info("service_starting", env=cfg.env, correlation_id=cid)

    try:
        run_job("daily_cleanup")
        logger.info("service_completed")
    except AppError as e:
        logger.warning("app_error", **e.to_log_fields())
        raise
    except Exception as e:
        logger.exception("unhandled_exception", exc=e)
        raise


def main() -> None:
    run()


if __name__ == "__main__":
    main()
