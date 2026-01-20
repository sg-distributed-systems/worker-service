"""
Pydantic models for API request and response validation.

Defines data transfer objects used for request parsing and response
serialization in the API layer.
"""
from datetime import datetime
from typing import Dict
from uuid import UUID

from pydantic import BaseModel, Field


class EnqueueJobRequest(BaseModel):
    job_id: UUID
    job_type: str
    payload: Dict = Field(default_factory=dict)
    priority: int = Field(ge=1, le=10, default=5)


class EnqueueJobResponse(BaseModel):
    job_id: UUID
    status: str
    scheduled_at: datetime


class GetJobStatusRequest(BaseModel):
    job_id: UUID


class GetJobStatusResponse(BaseModel):
    job_id: UUID
    status: str
    scheduled_at: datetime


class CancelJobRequest(BaseModel):
    job_id: UUID


class CancelJobResponse(BaseModel):
    job_id: UUID
    status: str
    cancelled_at: datetime
