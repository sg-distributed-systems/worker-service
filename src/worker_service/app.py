"""
FastAPI application factory with health check endpoints.

Creates the FastAPI app instance, includes API routes, and provides /healthz
and /readyz endpoints for Kubernetes-style health and readiness probes.
"""
from uuid import uuid4

from core_logger import set_correlation_id
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .routes import router

SERVICE_NAME = "worker-service"
app = FastAPI(title=SERVICE_NAME)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
        set_correlation_id(correlation_id)
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


app.add_middleware(CorrelationIdMiddleware)
app.include_router(router)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": SERVICE_NAME}


@app.get("/readyz")
def readyz():
    return {"status": "ok", "service": SERVICE_NAME}
