from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/users")
def users():
    return [
        {
            "id": 1,
            "name": "Alice"
        },
        {
            "id": 2,
            "name": "Bob"
        }
    ]