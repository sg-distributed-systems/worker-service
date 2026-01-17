from fastapi import APIRouter

from .main import run_job
from .schemas import RunJobRequest, RunJobResponse

router = APIRouter()


@router.post("/worker/run", response_model=RunJobResponse)
def run_job_route(req: RunJobRequest) -> RunJobResponse:
    run_job(req.job_name)
    return RunJobResponse(status="ok")
