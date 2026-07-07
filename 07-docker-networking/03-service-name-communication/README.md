# 🧩 03 — Service Name Communication

## 🎯 Goal

Use Docker's internal DNS to allow one container to communicate with another using its **service name**.

---

## 🧠 The Problem

Our API needs to connect to PostgreSQL.

Should we write:

```text
localhost
```

❌ No.

Inside the API container, `localhost` refers to the API container itself.

Should we use the PostgreSQL container's IP?

❌ No.

Container IPs can change whenever containers are recreated.

---

## 💡 Solution

Use the **service name** defined in `compose.yaml`.

If the service is named:

```yaml
postgres-db:
```

Then the hostname becomes:

```text
postgres-db
```

Docker automatically resolves it.

---

## 📁 Project Structure

```text
03-service-name-communication/
│
├── app/
│   ├── main.py
│   └── requirements.txt
├── Dockerfile
└── compose.yaml
```

---

## 📄 app/main.py

```python
import os

db_host = os.getenv("DB_HOST", "localhost")

print(f"Connecting to database at: {db_host}")
```

---

## 📄 app/requirements.txt

```text
# No external dependencies required
```

---

## 📄 Dockerfile

```dockerfile
FROM python:3.14

WORKDIR /app

COPY app/ .

CMD ["python", "main.py"]
```

---

## 📄 compose.yaml

```yaml
services:
  api:
    build: .
    environment:
      DB_HOST: postgres-db
    depends_on:
      - postgres-db

  postgres-db:
    image: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: postgres
```

---

## ▶️ Run

```bash
docker compose up --build
```

Expected output:

```text
Connecting to database at: postgres-db
```

---

## 🧠 What's happening?

1. Docker starts both containers.
2. Both join the same Docker network.
3. Docker registers `postgres-db` in its internal DNS.
4. The API reads `DB_HOST=postgres-db`.
5. When the application connects, Docker translates `postgres-db` to the correct container IP.

```text
API Container
      │
      │  DB_HOST=postgres-db
      ▼
Docker Internal DNS
      ▼
PostgreSQL Container
```

---

## 💡 Why use an environment variable?

Instead of hardcoding:

```python
host = "postgres-db"
```

we use:

```python
host = os.getenv("DB_HOST")
```

This makes the application portable.

For example:

| Environment  | DB_HOST                                   |
| ------------ | ----------------------------------------- |
| Local Docker | `postgres-db`                             |
| Kubernetes   | `postgres`                                |
| AWS RDS      | `mydb.abc123.us-east-1.rds.amazonaws.com` |

The code stays the same—only the configuration changes.

---

## 🎯 Key Takeaway

Service names act as hostnames inside a Docker network.

Instead of connecting to an IP address, applications connect using the service name, making the system easier to manage and portable across environments.
