# Docker & Kubernetes Playbook

A hands-on learning repository focused on mastering Docker and Kubernetes through real-world backend engineering exercises.

This project is designed to move beyond theory and build a **production-level mental model** of how containerized systems work in modern backend architectures.

---

# 🎯 Purpose of This Repository

The goal of this repository is to build deep, practical understanding of:

* Docker fundamentals
* Container lifecycle and runtime behavior
* Image layering and build optimization
* Container networking and service communication
* Multi-container backend systems
* Production-ready container design patterns

Each module is structured as a **progressive engineering exercise**, not just a tutorial.

---

# 🧠 Learning Approach

Instead of memorizing commands, this repository focuses on:

> Understanding how and why Docker behaves the way it does.

Each task follows this pattern:

1. Identify a real-world problem
2. Build a minimal working example
3. Observe container behavior
4. Extract production-level insights
5. Document findings like an engineering system

---

# 📦 Module Structure

## 01 - Dockerfile Basics

* Images vs containers
* Build context
* Dockerfile instructions (FROM, WORKDIR, COPY, CMD)
* Python container lifecycle
* Output buffering behavior

---

## 02 - RUN vs Layers & Caching

* Image layers
* Docker build cache
* Why build order matters
* Performance optimization
* Dependency installation strategies

---

## 03 - ENTRYPOINT vs CMD

* Container runtime behavior
* Command construction model
* Argument passing in containers
* Production CLI patterns
* Service container design

---

## 04 - Docker Networking Basics

* Container isolation model
* Docker bridge networking
* Container-to-container communication
* Internal DNS resolution
* FastAPI + PostgreSQL integration

---

## 05 - Docker Compose (Upcoming)

* Multi-container orchestration
* Service definitions
* Environment configuration
* Network automation
* Production-like local environments

---

## 🚀 Tech Stack Used

* Python 3.14
* FastAPI
* PostgreSQL
* Docker
* Docker CLI
* (Upcoming) Docker Compose
* (Upcoming) Kubernetes fundamentals

---

# 🧱 Key Concepts Covered

* Container lifecycle management
* Image layering and caching
* Process execution model in containers
* Network isolation and service discovery
* Environment-based configuration
* Production-ready Dockerfile design

---

# 🧠 What This Repository Demonstrates

This repository is not just about Docker usage.

It demonstrates:

* Backend system design thinking
* Production-level containerization skills
* Debugging real container behavior
* Understanding distributed systems basics
* Preparing for Kubernetes architecture

---

# 📈 Progression Path

This repository is designed as a learning ladder:

```text id="flow1"
Docker Basics
    ↓
Image Optimization
    ↓
Runtime Behavior
    ↓
Networking
    ↓
Compose
    ↓
Kubernetes
```

---

# 🎯 Target Audience

This repository is intended for:

* Backend engineers (junior → senior transition)
* Developers learning Docker seriously
* Engineers preparing for DevOps / platform roles
* Anyone building production backend systems

---

# 💡 Philosophy

> You don’t learn Docker by memorizing commands.
> You learn Docker by understanding system behavior.

---

# 🚀 Next Steps

The next module introduces:

## Docker Compose

Where we evolve from:

```bash
docker run ...
docker run ...
docker run ...
```

to:

```bash
docker compose up
```

and define entire backend systems declaratively.

---

# 📌 Status

* [x] Dockerfile Basics
* [x] RUN vs Layers & Caching
* [x] ENTRYPOINT vs CMD
* [x] Docker Networking Basics
* [ ] Docker Compose (in progress)
* [ ] Kubernetes Fundamentals (planned)
