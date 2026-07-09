# 🧩 03 — Multi-Container Pods

## 🎯 Goal

In the previous modules, every Pod contained a single container.

This raises a natural question:

> **If a Pod can contain multiple containers, why don't we put our entire application inside one Pod?**

In this module, we'll answer that question and learn when multiple containers inside a Pod make sense.

---

# 📁 Project Structure

```text
03-multi-container-pods/
│
├── pod.yaml
└── README.md
```

---

# 🧠 Coming from Docker Compose

In Docker Compose, it's common to run several containers together.

For example:

```text
Docker Compose

├── FastAPI
├── Redis
└── PostgreSQL
```

Although they are started together, they are still independent containers.

If Redis crashes, only Redis is restarted.

If the API needs more capacity, we can run more API containers without creating additional Redis or PostgreSQL containers.

---

# 🤔 Should We Do the Same in Kubernetes?

A common assumption is:

> "Since a Pod can contain multiple containers, let's put FastAPI, Redis, and PostgreSQL into one Pod."

While Kubernetes allows multiple containers inside a Pod, this is **not** how applications are typically designed.

Instead, Kubernetes usually looks like this:

```text
Node

├── Pod
│     └── FastAPI
│
├── Pod
│     └── Redis
│
└── Pod
      └── PostgreSQL
```

Each service gets its own Pod.

This allows Kubernetes to:

* Restart each service independently.
* Scale each service independently.
* Update each service independently.

For example, if your application receives more traffic, you might need:

```text
10 FastAPI Pods
1 Redis Pod
1 PostgreSQL Pod
```

If Redis were inside every API Pod, Kubernetes would create ten Redis instances as well—which is almost never what you want.

---

# 🧠 So When Do We Use Multiple Containers?

The rule is simple:

> **Containers should share a Pod only when they must always live together.**

That means they should:

* Start together.
* Stop together.
* Be scheduled on the same node.
* Share the same network.
* Scale together.

If one container is useless without the other, they are good candidates for the same Pod.

---

# 📦 Example 1 — Database Metrics Exporter

```text
Pod

├── PostgreSQL
└── PostgreSQL Exporter
```

The exporter collects metrics from PostgreSQL and exposes them to **Prometheus** (a monitoring system that collects CPU, memory, request count, database statistics, and other metrics).

Without PostgreSQL, the exporter has nothing to monitor.

These containers naturally belong together.

---

# 📦 Example 2 — Vault Agent

```text
Pod

├── API
└── Vault Agent
```

The Vault Agent retrieves secrets (such as database passwords or API keys) and makes them available to the application.

Without the API, the Vault Agent has no purpose.

---

# 📦 Example 3 — Cloud SQL Proxy

```text
Pod

├── API
└── Cloud SQL Proxy
```

Instead of connecting directly to the database, the API communicates through the proxy.

The proxy exists only to serve that application, so they are deployed together.

---

# 🚀 Practical Example

For this exercise, we'll create a Pod with two containers:

```text
Pod

├── nginx
└── busybox
```

The nginx container serves web traffic.

The BusyBox container simply runs alongside it so we can observe how Kubernetes manages multiple containers inside a single Pod.

Create the Pod:

```bash
kubectl apply -f pod.yaml
```

Check the Pods:

```bash
kubectl get pods
```

Example:

```text
NAME         READY   STATUS    RESTARTS   AGE
multi-pod    2/2     Running   0          10s
```

Notice that Kubernetes reports:

```text
READY

2/2
```

This means the Pod contains **two running containers**.

---

# 🔍 Viewing Logs

Since the Pod contains multiple containers, Kubernetes needs to know which container's logs you want.

For example:

```bash
kubectl logs multi-pod -c nginx
```

or

```bash
kubectl logs multi-pod -c busybox
```

The `-c` flag specifies the container name inside the Pod.

---

# 🧠 One Network, One IP

Containers inside the same Pod share the same network namespace.

That means:

* They share the same IP address.
* They can communicate using `localhost`.
* They can share mounted volumes.

This close relationship is one of the reasons they are placed in the same Pod.

---

# 🎯 Key Takeaways

After completing this module, you understand:

* A Pod can contain one or more containers.
* Most applications use **one container per Pod**.
* Services such as APIs, Redis, and PostgreSQL are typically deployed in separate Pods.
* Multiple containers belong in the same Pod only when they must always run together.
* Containers within a Pod share the same network and can communicate through `localhost`.
* `kubectl logs -c` lets you view logs from a specific container inside a Pod.

In the next module, we'll explore how Pods communicate with each other and why Kubernetes introduces another important concept: **Services**.
