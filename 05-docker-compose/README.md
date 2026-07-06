# 📦 Module 05 — Docker Compose

## 🎯 Learning Objective

In the previous modules, we learned how to build Docker images, run containers, optimize Dockerfiles, and connect containers using Docker networks.

Those skills are enough for running a single container or even a couple of containers manually.

However, real-world applications rarely consist of just one container.

In this module, you'll learn how **Docker Compose** allows us to define and manage an entire multi-container application using a single configuration file.

By the end of this exercise, you'll understand how to build, configure, network, and run multiple services with a single command.

---

# 🚧 The Problem

Imagine you're building an e-commerce platform.

Instead of one application, your project consists of multiple services:

* 🌐 API
* 🗄️ PostgreSQL Database
* ⚡ Redis Cache

Without Docker Compose, setting up the application requires several manual steps.

You need to:

* Build the API image.
* Pull the PostgreSQL image.
* Pull the Redis image.
* Create a Docker network.
* Create Docker volumes for persistent storage.
* Start the PostgreSQL container.
* Start the Redis container.
* Start the API container.
* Pass environment variables.
* Ensure services communicate correctly.

For a small project this might be manageable.

Now imagine an application with:

* Authentication Service
* Product Service
* Order Service
* Payment Service
* Notification Service
* PostgreSQL
* Redis
* RabbitMQ

Managing every container manually quickly becomes repetitive and error-prone.

Another challenge is data persistence.

Suppose your PostgreSQL database stores thousands of customer records.

If the database container is removed, you don't want your customer data to disappear with it.

You need a storage mechanism that exists **outside the container** so data survives container recreation.

As applications grow, managing containers, networks, environment variables, startup order, and persistent storage manually becomes increasingly difficult.

---

# 💡 The Solution

Docker Compose solves this problem by allowing you to describe your entire application inside a single file named:

```text
compose.yaml
```

Instead of executing numerous Docker commands, you simply run:

```bash
docker compose up
```

Docker Compose automatically:

* Builds application images.
* Pulls official images.
* Creates Docker networks.
* Creates Docker volumes.
* Starts containers.
* Connects services together.
* Passes environment variables.
* Manages the application's lifecycle.

Instead of managing individual containers, you begin managing the application as a whole.

---

# 📂 Project Structure

```text
05-docker-compose/
│
├── app/
│   ├── main.py
│   └── requirements.txt
│
├── Dockerfile
└── compose.yaml
```

---

# 🧠 Dockerfile vs Docker Compose

One of the most common questions beginners ask is:

> **Do I still need a Dockerfile if I'm using Docker Compose?**

The answer is **Yes**.

Both serve different purposes.

### Dockerfile

A Dockerfile defines **how to build a single service**.

It specifies:

* Base image
* Dependencies
* Files to copy
* Startup command

Think of it as the recipe for creating one Docker image.

---

### Docker Compose

Docker Compose defines **how multiple services work together**.

It describes:

* Which services exist
* Which images should be built
* Which images should be pulled
* Environment variables
* Networks
* Volumes
* Port mappings
* Startup dependencies

Think of Docker Compose as the blueprint for the entire application.

---

# 📚 What You'll Learn

After completing this module, you'll understand:

* Why Docker Compose exists.
* The relationship between Dockerfiles and Docker Compose.
* How to define multiple services.
* The difference between `build` and `image`.
* How port mapping works.
* How containers communicate using Docker's internal DNS.
* How environment variables configure applications.
* The purpose and limitation of `depends_on`.
* Why Docker volumes are needed.
* How Docker Compose automatically creates networks.
* How to manage an entire application using a single command.

---

# 📖 Core Concepts

## Services

Each application component is defined as a **service**.

For this module we have:

* API
* PostgreSQL
* Redis

Each service becomes its own Docker container.

---

## `build`

The `build` instruction tells Docker Compose to build an image using a Dockerfile.

Example:

```yaml
build: .
```

Docker Compose internally performs a Docker image build before creating the container.

When working with microservices, each service typically has its own Dockerfile.

Example:

```yaml
services:
  auth:
    build: ./auth

  products:
    build: ./products

  orders:
    build: ./orders
```

Each service is built independently.

---

## `image`

The `image` instruction specifies which image should be used.

Example:

```yaml
image: my-api:v1.0
```

Here:

* `my-api` is the image name.
* `v1.0` is the image tag.

If no tag is provided, Docker automatically uses the `latest` tag.

---

## `ports`

Port mapping allows applications running inside containers to be accessed from outside Docker.

Example:

```yaml
ports:
  - "5000:8000"
```

Meaning:

```text
Host Machine        Container
------------        ----------
5000      ─────▶    8000
```

Users access the application using port **5000**, while the application itself continues listening on **8000** inside the container.

Not every service needs exposed ports.

For example, PostgreSQL and Redis can communicate internally with other containers without exposing their ports to the host machine.

---

## `environment`

Environment variables provide configuration without changing application code.

Example:

```yaml
environment:
  DB_HOST: postgres-db
  DB_USER: postgres
```

Applications read these values using:

```python
os.getenv(...)
```

This makes the same application portable across development, testing, and production environments.

---

## `depends_on`

The `depends_on` instruction defines startup order.

Example:

```yaml
depends_on:
  - postgres-db
```

This tells Docker Compose:

> Start the PostgreSQL container before starting the API container.

**Important**

This **does not** guarantee that PostgreSQL is ready to accept database connections.

Production applications should implement retry logic or health checks to handle startup delays gracefully.

---

## Volumes

Containers are designed to be ephemeral.

If a container is deleted, its writable layer is deleted as well.

For databases, this would mean losing all stored data.

Docker Volumes solve this problem by storing data outside the container.

Example:

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

Left side:

```text
postgres-data
```

A Docker-managed named volume.

Right side:

```text
/var/lib/postgresql/data
```

The directory inside the PostgreSQL container where database files are stored.

The correct container path is determined by the application's documentation or the official Docker image documentation.

Deleting the PostgreSQL container does **not** delete the Docker volume.

This allows a newly created container to reuse the existing database.

---

## Automatic Networking

Docker Compose automatically creates a dedicated network for every project.

All services join this network automatically.

Instead of communicating using IP addresses, services communicate using their service names.

Example:

```text
postgres-db
redis
```

A FastAPI application can connect to PostgreSQL using:

```python
host = "postgres-db"
```

Docker automatically resolves the service name using its internal DNS.

This means your application never needs to know container IP addresses.

---

# 🚀 Common Commands

Start all services:

```bash
docker compose up
```

Build images before starting:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

Stop the application:

```bash
docker compose down
```

Stop the application and remove Docker volumes:

```bash
docker compose down -v
```

---

# 💡 Key Takeaways

After completing this module, you should understand:

* Docker Compose manages an entire application instead of individual containers.
* Dockerfiles build individual services, while Docker Compose orchestrates multiple services.
* Services communicate using Docker's internal DNS.
* Environment variables separate configuration from application code.
* Volumes provide persistent storage outside containers.
* `depends_on` controls startup order but does not guarantee service readiness.
* Docker Compose automatically creates networks and volumes.
* Multi-container applications can be started with a single command.

---

# 🎯 Summary

Docker Compose represents an important shift in how containerized applications are managed.

Instead of thinking about individual containers, you begin thinking in terms of complete systems composed of multiple services working together.

By describing an application's architecture in a single `compose.yaml` file, Docker Compose automates image building, networking, configuration, storage, and service orchestration.

This approach greatly simplifies local development and provides the conceptual foundation for container orchestration platforms such as Kubernetes, where many of these same ideas are applied across clusters of machines.
