# 📦 Module 07 — Docker Networking

## Overview

So far, we've learned how to build Docker images, run containers, orchestrate multiple services with Docker Compose, and improve the development experience using bind mounts.

The next question naturally becomes:

> **How do containers communicate with each other?**

In a real application, a backend service rarely works alone. It typically needs to communicate with databases, caches, message brokers, and other services. This module explores how Docker enables that communication without requiring hardcoded IP addresses or manual network configuration.

---

## 🎯 Learning Objectives

After completing this module, you will understand:

* How Docker networks work
* Why containers are isolated by default
* How Docker Compose automatically creates networks
* How service names become hostnames
* How containers discover and communicate with each other
* How to configure applications using environment variables
* How a complete multi-container application works

---

## 🧠 The Problem

Imagine you're building a backend API that needs to connect to:

* PostgreSQL
* Redis
* Another microservice

How should the API connect?

Should you use:

```text
localhost
```

❌ No.

Inside a container, `localhost` always refers to **that container itself**.

Should you use an IP address?

❌ No.

Container IP addresses are dynamic and may change whenever containers are recreated.

There needs to be a better solution.

---

## 💡 Docker's Solution

Docker provides an internal network with built-in DNS.

When multiple containers are connected to the same Docker network, they can communicate using **service names** instead of IP addresses.

For example:

```text
API
 │
 ├── postgres-db
 ├── redis
 └── payment-service
```

Each service name automatically becomes a hostname that other containers can resolve.

---

## 📚 Module Structure

This module is divided into five practical exercises.

### 🧩 01 — No Network (Isolation)

Learn that containers are isolated by default and cannot communicate unless they share a network.

---

### 🧩 02 — Default Docker Compose Network

Understand how Docker Compose automatically creates a network and connects all services to it.

---

### 🧩 03 — Service Name Communication

Learn how Docker's internal DNS resolves service names such as:

```text
postgres-db
redis
```

instead of requiring IP addresses.

---

### 🧩 04 — Complete Microservices Stack

Build a small application consisting of:

* FastAPI
* PostgreSQL
* Redis

and see how all services communicate using Docker networking.
---

## 🧠 Final Mental Model

```text
                    Docker Network

        ┌────────────────────────────────┐
        │                                │
        │   API                          │
        │    │                           │
        │    ├────────► PostgreSQL       │
        │    │                           │
        │    └────────► Redis            │
        │                                │
        └────────────────────────────────┘
```

Instead of communicating using IP addresses, containers simply use service names.

Docker's internal DNS resolves those names to the correct containers.

---

## 🎯 Key Takeaways

After completing this module, you should understand that:

* Containers are isolated by default.
* Docker Compose automatically creates a private network.
* Every service joins that network automatically.
* Service names act as hostnames.
* Applications should use environment variables instead of hardcoded addresses.
* Multi-container applications become much easier to configure and maintain.
