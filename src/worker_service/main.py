from core_logger import get_logger

logger = get_logger("worker-service")


def run_job(job_name: str) -> None:
    logger.info("job_started", job_name=job_name)
    logger.info("job_completed", job_name=job_name)


def main() -> None:
    run_job("daily_cleanup")


if __name__ == "__main__":
    main()
