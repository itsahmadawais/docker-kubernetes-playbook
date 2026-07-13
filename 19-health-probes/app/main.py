from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import time

startup_complete = False
app_ready = False
app_healthy = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    global startup_complete, app_ready

    # Simulate a slow startup
    time.sleep(15)

    startup_complete = True
    app_ready = True

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "Docker Kubernetes Playbook"}


@app.get("/startup")
def startup_probe():
    if startup_complete:
        return PlainTextResponse("OK", status_code=200)
    return PlainTextResponse("Starting", status_code=503)


@app.get("/ready")
def readiness_probe():
    if app_ready:
        return PlainTextResponse("Ready", status_code=200)
    return PlainTextResponse("Not Ready", status_code=503)


@app.get("/health")
def liveness_probe():
    if app_healthy:
        return PlainTextResponse("Healthy", status_code=200)
    return PlainTextResponse("Unhealthy", status_code=500)


@app.post("/break")
def break_app():
    global app_healthy
    app_healthy = False
    return {"message": "Application is now unhealthy"}