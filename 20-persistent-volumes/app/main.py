from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DATA_DIR = Path("/data")
DATA_FILE = DATA_DIR / "message.txt"


class Message(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "Persistent Volumes Demo"}


@app.post("/write")
def write_message(payload: Message):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    DATA_FILE.write_text(payload.message)

    return {
        "message": "Data written successfully.",
        "file": str(DATA_FILE),
    }


@app.get("/read")
def read_message():
    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="No message found."
        )

    return {
        "message": DATA_FILE.read_text()
    }