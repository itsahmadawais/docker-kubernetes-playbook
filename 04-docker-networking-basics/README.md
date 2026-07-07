# 04 - Docker Networking Basics

## Objective

The objective of this exercise is to understand how containers communicate with each other using Docker networks.

This module demonstrates:

* Why `localhost` does not work between containers
* How Docker networking enables service-to-service communication
* How container names act as DNS hostnames
* How real backend systems (FastAPI + PostgreSQL) interact in Docker

---

## System Architecture

```text id="arch1"
FastAPI Container  ───────►  PostgreSQL Container
        (API)                 (Database)
         │
         └── Connected via Docker network (app-network)
```

---

## Key Concept

Each container runs in complete isolation, including its own network stack.

This means:

> `localhost` inside a container refers only to itself, not other containers.

---

## Why localhost fails

If FastAPI tries to connect like this:

```text id="fail1"
host = "localhost"
```

It fails because:

* `localhost` = current container only
* PostgreSQL is running in a separate container

---

## Solution: Docker Network

We create a shared network:

```bash id="net1"
docker network create app-network
```

Containers inside this network can communicate using **container names as DNS names**.

---

## PostgreSQL Container

```bash id="pg1"
docker run -d \
  --name postgres-db \
  --network app-network \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=postgres \
  postgres
```

---

## FastAPI Application

### app/main.py

```python id="api1"
from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres-db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.get("/")
def root():
    return {"message": "FastAPI running inside Docker network"}


@app.get("/db-check")
def db_check():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    conn.close()

    return {"postgres_version": version}
```

---

## Requirements

```text id="req1"
fastapi
uvicorn
psycopg2-binary
```

---

## Dockerfile (FastAPI Service)

```dockerfile id="df1"
FROM python:3.14

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Build FastAPI Image

```bash id="build1"
docker build -t fastapi-network:v1 .
```

---

## Run PostgreSQL Container

```bash id="runpg1"
docker run -d \
  --name postgres-db \
  --network app-network \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=postgres \
  postgres
```

---

## Run FastAPI Container

```bash id="runapi1"
docker run -d \
  --name fastapi-app \
  --network app-network \
  -p 8000:8000 \
  -e DB_HOST=postgres-db \
  -e DB_USER=postgres \
  -e DB_PASSWORD=pass \
  -e DB_NAME=postgres \
  fastapi-network:v1
```

---

## Key Behavior

### 1. Containers communicate using names

Instead of:

```text id="wrong1"
localhost:5432 ❌
```

We use:

```text id="correct1"
postgres-db ✅
```

---

### 2. Docker provides internal DNS

Docker automatically resolves:

```text id="dns1"
postgres-db → internal container IP
```

So services communicate using names instead of IPs.

---

### 3. Shared network enables connectivity

Only containers inside the same Docker network can communicate.

---

## Testing the Setup

### Root endpoint

```text id="test1"
http://localhost:8000/
```

### Database check

```text id="test2"
http://localhost:8000/db-check
```

Expected response:

```json id="test3"
{
  "postgres_version": "PostgreSQL ..."
}
```

---

## Key Learnings

* Containers are isolated environments
* `localhost` refers only to the current container
* Docker networks enable inter-container communication
* Container names act as DNS hostnames
* Backend services communicate via service discovery, not IPs

---

## Production Insight

In real-world systems:

* Docker networking is the foundation of microservices communication
* Kubernetes extends this using Services + CoreDNS
* Hardcoded IPs are never used in production
* Service names become stable network identities

---

## Summary

After completing this exercise, you should understand:

* How containers communicate via Docker networks
* Why `localhost` fails in multi-container systems
* How Docker DNS resolves container names
* How FastAPI and PostgreSQL interact in a containerized system

This module forms the foundation for multi-service backend systems and prepares you for Docker Compose and Kubernetes networking.
