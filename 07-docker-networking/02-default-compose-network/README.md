# 🧩 02 — Default Docker Compose Network

## 🎯 Goal

Understand how Docker Compose automatically creates a network and allows services to communicate using their **service names**.

---

## 🧠 The Problem

Imagine you have two containers:

* API
* PostgreSQL

How does the API connect to the database?

Do we use:

```text
192.168.1.15
```

or

```text
localhost
```

❌ Neither.

Container IPs are dynamic and `localhost` inside the API container refers to the API container itself.

---

## 💡 Docker Compose Solution

When you run:

```bash
docker compose up
```

Docker automatically creates a network for the project.

For example, if your folder is named:

```text
02-default-compose-network
```

Docker creates something similar to:

```text
02-default-compose-network_default
```

Every service joins this network automatically.

---

## 📁 Project Structure

```text
02-default-compose-network/
│
├── compose.yaml
└── README.md
```

---

## 📄 compose.yaml

```yaml
services:
  api:
    image: python:3.14
    command: sleep infinity

  postgres-db:
    image: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: postgres
```

Notice that we don't define any networks.

Docker Compose does it for us.

---

## ▶️ Run

```bash
docker compose up -d
```

---

## 🧠 What Docker does

```text
                Docker Network
        ┌─────────────────────────┐
        │                         │
        │   api                   │
        │      │                  │
        │      │                  │
        │      ▼                  │
        │   postgres-db           │
        │                         │
        └─────────────────────────┘
```

Both containers are now on the same private network.

---

## 🔑 Service Name = Hostname

Inside the `api` container, you can connect to PostgreSQL using:

```text
postgres-db
```

For example:

```text
Host: postgres-db
Port: 5432
```

You do **not** need to know the container's IP address.

Docker's internal DNS resolves:

```text
postgres-db
```

to the correct container automatically.

---

## 🧪 Verify

Open a shell inside the API container:

```bash
docker compose exec api bash
```

Then try:

```bash
ping postgres-db
```

or

```bash
getent hosts postgres-db
```

You'll see that Docker resolves the service name to the container's IP address.

---

## 🎯 Key Takeaway

When Docker Compose starts your application:

* It automatically creates a private network.
* Every service joins that network.
* Each service name becomes a hostname.
* Containers communicate using service names instead of IP addresses.

> **Think of Docker Compose as creating a private LAN for your containers, complete with its own DNS server.**
