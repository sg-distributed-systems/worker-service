from pydantic import BaseModel


class RunJobRequest(BaseModel):
    job_name: str


class RunJobResponse(BaseModel):
    status: str
