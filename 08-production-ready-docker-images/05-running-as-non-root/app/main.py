import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Running as non-root",
        "uid": os.getuid(),
        "gid": os.getgid(),
    }