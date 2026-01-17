from fastapi import FastAPI

from .routes import router

SERVICE_NAME = "worker-service"
app = FastAPI(title=SERVICE_NAME)
app.include_router(router)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": SERVICE_NAME}


@app.get("/readyz")
def readyz():
    return {"status": "ok", "service": SERVICE_NAME}
