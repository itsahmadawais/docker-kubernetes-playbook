#  09 — Why Kubernetes (K8s)?

## 🎯 Goal

Understand the problems Kubernetes solves and why container orchestration becomes essential as applications grow.

This module introduces the motivation behind Kubernetes. We won't write any Kubernetes YAML yet. Instead, we'll build a mental model that will make the upcoming modules much easier to understand.

---

## 🧠 The Problem

Imagine you've built a FastAPI application and packaged it using Docker.

```text
Docker Image
      │
      ▼
Docker Container
```

You deploy it to a server and everything works perfectly.

As your application becomes more popular, you decide to run multiple containers.

```text
Server
│
├── API 1
├── API 2
├── API 3
├── API 4
└── API 5
```

For a while, everything runs smoothly.

Then new challenges begin to appear.

---

## Problem 1 — A Container Crashes

One of your containers unexpectedly stops.

```text
Server
│
├── API 1
├── API 2
├── ❌ API 3
├── API 4
└── API 5
```

Someone has to notice the failure and restart the container.

With Docker alone, that's your responsibility.

---

## Problem 2 — Traffic Increases

Your application suddenly receives ten times more traffic.

Five containers are no longer enough.

You now need twenty.

Someone has to start those additional containers and ensure they're distributed correctly.

Again, that's a manual task.

---

## Problem 3 — One Server Isn't Enough

Eventually a single server runs out of CPU and memory.

You purchase another server.

```text
Server A
├── API
├── API

Server B
├── API
├── API
```

Now you have a new challenge.

Which server should run each container?

How do you balance the workload?

---

## Problem 4 — A Server Fails

Suppose Server A suddenly becomes unavailable.

```text
Server A ❌

Server B
├── API
├── API
```

The containers that were running on Server A disappear.

Someone must recreate them on another healthy server.

---

## Problem 5 — Deploying New Versions

Your application is running Version 1.

You release Version 2.

How do you update dozens of running containers without causing downtime?

Performing rolling updates manually quickly becomes difficult and error-prone.

---

## 💡 The Solution

Docker solves one problem:

> **How do I package and run an application inside a container?**

Kubernetes solves another:

> **How do I manage hundreds or thousands of containers automatically?**

Instead of manually restarting containers, scaling applications, or deciding where they should run, Kubernetes continuously manages your applications for you.

---

## 🧠 The Core Idea: Desired State

The most important concept in Kubernetes is the **desired state**.

Instead of telling Kubernetes **how** to perform each task, you simply describe **what you want**.

For example:

```text
I want:

• 5 application Pods
• Each running image my-api:v1
• Each requiring 512 MiB RAM
• Each requiring 0.5 CPU
```

Kubernetes continuously compares the current state of the cluster with the desired state.

If they don't match, Kubernetes takes action automatically.

---

## Example

Desired state:

```text
5 Pods
```

Current state:

```text
Pod 1 ✅
Pod 2 ✅
Pod 3 ❌
Pod 4 ✅
Pod 5 ✅
```

Kubernetes notices that only four Pods are running.

It automatically creates a replacement until the desired state is restored.

---

## Resource Requirements

When defining an application, you also specify the resources each Pod requires.

For example:

```text
Memory: 512 MiB
CPU: 0.5
```

Kubernetes uses these requirements to determine which server has enough available resources to run the Pod.

If no server has sufficient capacity, the Pod remains in the **Pending** state until resources become available or additional nodes are added to the cluster.

---

## Docker vs Kubernetes

Docker is responsible for packaging and running containers.

Kubernetes is responsible for managing those containers across one or more servers.

```text
Your Code
     │
     ▼
Docker Image
     │
     ▼
Container
     │
     ▼
Kubernetes
 • Schedules containers
 • Restarts failed workloads
 • Scales applications
 • Performs rolling updates
 • Monitors application health
```

Docker and Kubernetes work together—they solve different problems.

---

## 🎯 Key Takeaway

Docker helps you build and run containers.

Kubernetes helps you operate containerized applications reliably at scale.

Rather than manually managing containers, you describe the desired state of your application, and Kubernetes continuously works to make reality match that description.

This declarative approach is the foundation of everything you'll learn in the upcoming Kubernetes modules.