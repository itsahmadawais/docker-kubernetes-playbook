import os

import psycopg
import redis
from fastapi import FastAPI

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")
DB_NAME = os.getenv("DB_NAME", "postgres")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


@app.get("/")
def home():
    db_connected = False
    redis_connected = False

    # Check PostgreSQL
    try:
        conn = psycopg.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
        )
        conn.close()
        db_connected = True
    except Exception:
        pass

    # Check Redis
    try:
        client = redis.Redis(host=REDIS_HOST, port=6379)
        client.ping()
        redis_connected = True
    except Exception:
        pass

    return {
        "message": "Docker Networking Demo",
        "database": "Connected" if db_connected else "Not Connected",
        "redis": "Connected" if redis_connected else "Not Connected",
        "db_host": DB_HOST,
        "redis_host": REDIS_HOST,
    }