from fastapi import FastAPI
import time

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Horizontal Pod Autoscaler Demo",
        "endpoints": ["/", "/cpu"]
    }


@app.get("/cpu")
def cpu_load():
    """
    Simulate CPU-intensive work for about 10 seconds.
    """

    end_time = time.time() + 10

    while time.time() < end_time:
        sum(i * i for i in range(10000))

    return {"message": "CPU load completed."}