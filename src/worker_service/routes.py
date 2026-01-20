"""
API route definitions for the service.

Defines FastAPI router endpoints that handle incoming HTTP requests and
delegate to core business logic functions.
"""
from fastapi import APIRouter

from .main import run_job
from .schemas import RunJobRequest, RunJobResponse

router = APIRouter()


@router.post("/worker/run", response_model=RunJobResponse)
def run_job_route(req: RunJobRequest) -> RunJobResponse:
    run_job(req.job_name)
    return RunJobResponse(status="ok")
