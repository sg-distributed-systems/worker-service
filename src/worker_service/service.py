"""
Background job queue management.

Handles job enqueueing, prioritization, status tracking, and lifecycle management
for asynchronous tasks including email sending, report generation, and data exports.
"""
from datetime import datetime
from uuid import UUID, uuid4

from core_logger import get_logger

from .errors import NotFoundError, ValidationError

logger = get_logger("worker-service", tier="infrastructure")

VALID_JOB_TYPES = {"email_send", "report_generate", "data_export", "image_resize", "cache_invalidate"}
JOB_QUEUE: dict = {}


def enqueue_job(job_type: str, payload: dict, priority: int) -> dict:
    logger.info("job_enqueue_requested", job_type=job_type, priority=priority)

    if job_type not in VALID_JOB_TYPES:
        raise ValidationError("invalid_job_type", details={"allowed": list(VALID_JOB_TYPES)})

    if priority < 1 or priority > 10:
        raise ValidationError("priority_out_of_range", details={"min": 1, "max": 10})

    job_id = uuid4()
    scheduled_at = datetime.utcnow()

    JOB_QUEUE[job_id] = {"type": job_type, "status": "pending", "scheduled_at": scheduled_at}

    logger.info("job_enqueued", job_id=str(job_id), job_type=job_type, priority=priority)
    return {"job_id": job_id, "status": "pending", "scheduled_at": scheduled_at}


def get_job_status(job_id: UUID) -> dict:
    logger.debug("job_status_check", job_id=str(job_id))

    job = JOB_QUEUE.get(job_id)
    if not job:
        raise NotFoundError("job_not_found", details={"job_id": str(job_id)})

    return {"job_id": job_id, "status": job["status"], "scheduled_at": job["scheduled_at"]}


def cancel_job(job_id: UUID) -> dict:
    logger.info("job_cancellation", job_id=str(job_id))

    job = JOB_QUEUE.get(job_id)
    if not job:
        raise NotFoundError("job_not_found")

    if job["status"] != "pending":
        raise ValidationError("cannot_cancel_non_pending_job", details={"current_status": job["status"]})

    job["status"] = "cancelled"
    logger.info("job_cancelled", job_id=str(job_id))
    return {"job_id": job_id, "status": "cancelled", "cancelled_at": datetime.utcnow()}


def purge_completed_jobs(older_than_days: int = 30) -> dict:
    logger.info("job_purge_started", older_than_days=older_than_days)

    if older_than_days < 1:
        raise ValidationError("invalid_retention_period", details={"min_days": 1})

    removed = 0
    logger.info("jobs_purged", removed=removed, older_than_days=older_than_days)
    return {"removed": removed, "purged_at": datetime.utcnow()}
