"""
API route definitions for the service.

Defines FastAPI router endpoints that handle incoming HTTP requests and
delegate to core business logic functions.
"""
from fastapi import APIRouter

from .schemas import (
    CancelJobRequest,
    CancelJobResponse,
    EnqueueJobRequest,
    EnqueueJobResponse,
    GetJobStatusRequest,
    GetJobStatusResponse,
)
from .service import cancel_job, enqueue_job, get_job_status

router = APIRouter()


@router.post("/worker/enqueue", response_model=EnqueueJobResponse, status_code=200)
def enqueue_job_route(req: EnqueueJobRequest) -> EnqueueJobResponse:
    result = enqueue_job(
        job_type=req.job_type,
        payload=req.payload,
        priority=req.priority,
    )
    return EnqueueJobResponse(
        job_id=result["job_id"],
        status=result["status"],
        scheduled_at=result["scheduled_at"],
    )


@router.post("/worker/status", response_model=GetJobStatusResponse, status_code=200)
def get_job_status_route(req: GetJobStatusRequest) -> GetJobStatusResponse:
    result = get_job_status(job_id=req.job_id)
    return GetJobStatusResponse(
        job_id=result["job_id"],
        status=result["status"],
        scheduled_at=result["scheduled_at"],
    )


@router.post("/worker/cancel", response_model=CancelJobResponse, status_code=200)
def cancel_job_route(req: CancelJobRequest) -> CancelJobResponse:
    result = cancel_job(job_id=req.job_id)
    return CancelJobResponse(
        job_id=result["job_id"],
        status=result["status"],
        cancelled_at=result["cancelled_at"],
    )
