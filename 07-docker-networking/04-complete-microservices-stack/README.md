# 🧩 04 — Complete Microservices Stack

## 🎯 Goal

Build a small application consisting of multiple containers that communicate over Docker's internal network.

This example brings together concepts from previous modules:

- Dockerfiles
- Docker Compose
- Networks
- Service discovery
- Environment variables
- Volumes
- `depends_on`

---

## 📁 Project Structure

```text
04-complete-microservices-stack/
│
├── app/
│   ├── main.py
│   └── requirements.txt
├── Dockerfile
└── compose.yaml
```

---

## 🏗 Architecture

```text
               Docker Network

          ┌─────────────────────┐
          │                     │
          │      FastAPI        │
          │         │           │
          │         │           │
          │         ▼           │
          │    PostgreSQL       │
          │                     │
          │         ▲           │
          │         │           │
          │       Redis         │
          │                     │
          └─────────────────────┘
```

All three containers are connected to the same Docker network and communicate using their service names.

---

## 📄 compose.yaml

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres-db
      - redis
    environment:
      DB_HOST: postgres-db
      DB_USER: postgres
      DB_PASSWORD: pass
      DB_NAME: postgres

      REDIS_HOST: redis

  postgres-db:
    image: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis
    restart: unless-stopped

volumes:
  postgres-data:
```

---

## 🧠 What's Happening?

### API

- Builds our custom Docker image
- Exposes port **8000**
- Connects to PostgreSQL
- Connects to Redis

---

### PostgreSQL

- Uses the official PostgreSQL image
- Stores data in a named Docker volume
- Is reachable as:

```text
postgres-db
```

---

### Redis

Uses the official Redis image.

Other containers connect using:

```text
redis
```

---

## 🔗 Service Discovery

Docker automatically creates DNS entries.

| Service | Hostname |
|---------|----------|
| API | `api` |
| PostgreSQL | `postgres-db` |
| Redis | `redis` |

No IP addresses are needed.

---

## 💾 Persistent Storage

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

The named volume stores PostgreSQL data outside the container.

This means your database survives even if the container is removed and recreated.

---

## ▶️ Run

```bash
docker compose up --build
```

Docker will:

1. Build the API image.
2. Pull PostgreSQL.
3. Pull Redis.
4. Create a Docker network.
5. Create the named volume.
6. Start all containers.

---

## 🧠 What You've Learned

By this point, you understand how to build a multi-container application where:

- Containers communicate using service names.
- Docker provides internal DNS.
- Databases persist data using volumes.
- Environment variables configure connections.
- Docker Compose manages the entire application.

---

## 🎯 Key Takeaway

Docker Compose is much more than a tool for starting containers.

It defines an application's infrastructure, including its services, networking, storage, and configuration, allowing the entire stack to be started with a single command.