# 📦 12 — Pods

## 🎯 Learning Objectives

By the end of this module, you'll understand:

* What a Pod is
* Why Kubernetes uses Pods instead of containers
* How to create and inspect Pods
* The Pod lifecycle
* Why Pods are considered ephemeral
* How multiple containers can share a single Pod
* When to use Init Containers

This module introduces the most fundamental Kubernetes object: the **Pod**.

---

# 📖 Why Pods?

Throughout the previous modules, we've talked about running applications in Kubernetes.

However, Kubernetes does **not** deploy containers directly.

Instead, it deploys **Pods**.

A Pod is the smallest deployable unit in Kubernetes.

For most applications, a Pod contains a single application container, which is why it often feels similar to running a Docker container.

As you'll discover later in this module, a Pod can also contain multiple containers that work together.

---

# 🧠 From Docker to Kubernetes

With Docker, the basic unit is a **Container**.

```text id="h9m12c"
Docker

Image
   │
   ▼
Container
```

With Kubernetes, the basic unit is a **Pod**.

```text id="6td8sa"
Docker Image
      │
      ▼
Pod
      │
      ▼
Container
```

Rather than managing containers directly, Kubernetes manages Pods.

---

# 📂 Module Structure

```text id="3mq8g0"
11-pods/
│
├── 01-first-pod/
├── 02-pod-lifecycle/
├── 03-multi-container-pods/
├── 04-init-containers/
└── README.md
```

Each submodule focuses on one important concept, building your understanding step by step.

---

# 📚 What You'll Learn

## 01 — First Pod

Create your first Kubernetes Pod.

You'll learn:

* Pod structure
* Creating a Pod
* Inspecting a Pod
* Viewing logs
* Deleting a Pod

This exercise introduces the basic Kubernetes workflow using `kubectl`.

---

## 02 — Pod Lifecycle

Pods don't remain in the same state forever.

You'll explore common Pod states such as:

* Pending
* Running
* Succeeded
* Failed
* CrashLoopBackOff
* ImagePullBackOff

Understanding these states is essential for debugging Kubernetes applications.

---

## 03 — Multi-Container Pods

Although most Pods contain a single application container, Kubernetes also allows multiple containers to share a Pod.

You'll learn:

* Why multiple containers may share a Pod
* Sidecar containers
* Shared networking
* Shared storage

---

## 04 — Init Containers

Some tasks must complete before an application starts.

Init Containers provide a clean way to perform setup tasks such as:

* Waiting for dependencies
* Downloading configuration
* Running database migrations

Only after all Init Containers finish successfully does the application container start.

---

# 🧠 Mental Model

Think of a Pod as a wrapper around one or more containers.

```text id="g4yw6d"
Pod
│
├── Application Container
├── (Optional) Sidecar Container
└── Shared Network & Storage
```

Kubernetes schedules, monitors, and replaces Pods—not individual containers.

---

# 🚀 Why It Matters

Pods are the foundation of Kubernetes.

Every higher-level Kubernetes object ultimately manages Pods.

For example:

```text id="tmf0z8"
Deployment
      │
      ▼
ReplicaSet
      │
      ▼
Pods
```

Understanding Pods first makes concepts like Deployments, Services, Autoscaling, and Rolling Updates much easier to learn.

---

# 🎯 Key Takeaway

A Pod is the smallest deployable unit in Kubernetes.

Although a Pod often contains a single container, it is much more than just a container. It provides shared networking, shared storage, and a lifecycle that Kubernetes can manage.

In the next exercises, you'll create your first Pod, inspect its behavior, and learn why Pods are the building block of every Kubernetes application.
