# 🚀 Docker & Kubernetes Playbook

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

A hands-on, project-based learning repository for mastering **Docker** and **Kubernetes** through practical engineering exercises.

Rather than memorizing commands or copying configuration files, this playbook focuses on building a strong mental model of how containerized applications work—from writing your first Dockerfile to deploying scalable, production-ready applications with Kubernetes.

Whether you're preparing for technical interviews, transitioning into backend or platform engineering, or simply want to understand how modern applications are built and deployed, this repository is designed to help you learn by building.

---

# 🎯 Why This Repository?

Many Docker and Kubernetes tutorials focus on **what** commands to run.

This repository focuses on **why** those commands exist and how the underlying technologies work.

Every module starts with a real-world problem, walks through a practical solution, and explains the reasoning behind it so you build intuition instead of memorizing syntax.

The goal isn't to memorize Docker or Kubernetes commands.

The goal is to think like an engineer who can confidently design, build, debug, deploy, and operate containerized applications.

---

# 🧠 Learning Philosophy

Each module follows the same learning approach:

1. **Understand the problem**
2. **Build a minimal working example**
3. **Observe the system's behavior**
4. **Explain why it behaves that way**
5. **Extract production-ready best practices**

This approach develops the intuition needed for real-world engineering rather than short-term memorization.

---

# 📚 What You'll Learn

## 🐳 Docker

* Docker images and containers
* Writing Dockerfiles
* Build context
* Image layers and build caching
* `RUN`, `CMD`, and `ENTRYPOINT`
* Container lifecycle
* Bind mounts
* Named volumes
* Docker networking
* Docker Compose
* Production-ready Docker images
* Docker security and best practices

---

## ☸️ Kubernetes

* Why Kubernetes exists
* Kubernetes architecture
* Pods
* ReplicaSets
* Deployments
* Services
* ConfigMaps
* Secrets
* Resource requests and limits
* Health probes
* Persistent Volumes
* StatefulSets
* Jobs and CronJobs
* Ingress
* Horizontal Pod Autoscaler (HPA)
* Helm
* Production best practices

---

# 📂 Repository Structure

Each directory represents a standalone learning module that builds upon the previous one.

```text
01-dockerfile-basics/
02-run-vs-layers-and-caching/
03-entrypoint-vs-cmd/
04-using-dockerignore/
05-bind-mounts/
06-named-volumes/
07-docker-networking/
08-docker-compose/
09-production-ready-docker-images/

10-why-kubernetes/
11-kubernetes-architecture/
12-pods/
13-replicasets/
14-deployments/
15-services/
16-configmaps/
17-secrets/
18-resource-requests-and-limits/
19-health-probes/
20-persistent-volumes/
21-statefulsets/
22-jobs-and-cronjobs/
23-ingress/
24-horizontal-pod-autoscaler/
25-helm/
26-production-best-practices/
```

Every module includes:

* A clear learning objective
* Practical examples
* A detailed README
* Hands-on exercises
* Production insights and best practices

---

# 💻 Technologies Used

* Docker
* Docker Compose
* Kubernetes
* Helm
* Python 3.14
* FastAPI
* PostgreSQL

---

# 🎯 Who Is This Repository For?

This repository is designed for developers who want to understand **how modern containerized applications work in production**, not just how to run a few commands.

It's especially useful for:

* Backend Engineers
* Full-Stack Developers
* DevOps Engineers
* Platform Engineers
* Cloud Engineers
* Software Engineering Students
* Developers preparing for technical interviews

Whether you're learning Docker for the first time or strengthening your Kubernetes knowledge for production systems, you'll find practical, real-world examples throughout this repository.

---

# 🚀 Learning Journey

```text
Docker Fundamentals
        │
        ▼
Docker Compose
        │
        ▼
Production-Ready Docker Images
        │
        ▼
Why Kubernetes?
        │
        ▼
Kubernetes Architecture
        │
        ▼
Core Kubernetes Resources
        │
        ▼
Application Deployment
        │
        ▼
State Management
        │
        ▼
Networking & Ingress
        │
        ▼
Scaling Applications
        │
        ▼
Helm
        │
        ▼
Production Best Practices
```

Each module builds naturally upon the previous one, helping you understand not only *how* things work, but *why* they work that way.

---

# 🧠 A Note on Learning

One of the biggest misconceptions in software engineering is that great engineers memorize commands.

They don't.

Great engineers understand concepts.

It's perfectly normal to maintain a personal cheat sheet, consult documentation, or use AI tools like ChatGPT or Claude to recall specific commands or syntax. What matters most is understanding **what you're trying to accomplish, why you're doing it, and how the underlying technologies work together**.

When you understand the concepts, the commands become easy to find and use. Without that understanding, memorizing commands provides little long-term value.

This playbook is built around that philosophy.

---

# 🤝 Contributing

Found a mistake, spotted an improvement, or have an idea for a new module?

Contributions, discussions, and suggestions are always welcome.

---

# ⭐ Support the Project

If this repository helped you better understand Docker or Kubernetes, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.

Happy learning! 🚀
