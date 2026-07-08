# 📦 10 — Kubernetes Architecture

## 🎯 Goal

Understand how Kubernetes works internally before deploying your first application.

In the previous module, we learned **why Kubernetes exists**. In this module, we'll answer an even more important question:

> **How does Kubernetes actually work?**

By the end of this chapter, you'll understand the major components of a Kubernetes cluster and how they work together to deploy and manage applications.

---

# 🧠 From Docker to Kubernetes

With Docker, if you wanted multiple instances of your application, you had to manage them yourself.

```text
docker run my-api
docker run my-api
docker run my-api
...
```

As applications grow, this quickly becomes difficult.

Instead, Kubernetes lets you describe the **desired state**.

For example:

> I want 10 instances of my Ticket Booking API.

Kubernetes then figures out:

* Which server should run each instance.
* How to distribute the workload.
* How to recover from failures.
* How to maintain the desired number of running instances.

---

# 🏗️ What Is a Kubernetes Cluster?

A **Kubernetes Cluster** is a collection of machines working together.

Those machines are called **Nodes**.

```text
Kubernetes Cluster

├── Node A
├── Node B
└── Node C
```

Each node is simply a server.

It can be:

* A virtual machine
* A physical server
* A cloud instance (AWS, Azure, GCP, etc.)

Together, these nodes provide the computing resources needed to run your applications.

---

# 🧠 Control Plane vs Worker Nodes

Every Kubernetes cluster consists of two major parts.

```text
                 Kubernetes Cluster

        ┌──────────────────────────────┐
        │        Control Plane         │
        │      (Makes Decisions)       │
        └──────────────────────────────┘
                    │
      ───────────────────────────────────
                    │
     ┌──────────────┴──────────────┐
     ▼                             ▼
 Worker Node A               Worker Node B
 (Runs Pods)                 (Runs Pods)
```

The responsibilities are clearly separated.

## Control Plane

The **Control Plane** is the brain of Kubernetes.

It does **not** run your applications.

Instead, it decides:

* Where Pods should run.
* Whether more Pods should be created.
* Whether failed Pods should be replaced.
* Whether the cluster matches the desired state.

---

## Worker Nodes

Worker Nodes perform the actual work.

They are responsible for running your application's Pods.

When Kubernetes creates a new Pod, it is scheduled onto one of these nodes.

---

# 📦 Pods Run on Nodes

Suppose you deploy an application with **10 replicas**.

Kubernetes might distribute them like this:

```text
Node A
├── Pod 1
├── Pod 2
└── Pod 3

Node B
├── Pod 4
├── Pod 5
└── Pod 6

Node C
├── Pod 7
├── Pod 8
├── Pod 9
└── Pod 10
```

Notice that you never tell Kubernetes where each Pod should run.

You simply describe **what you want**, and Kubernetes decides **where it should run**.

---

# ⚙️ Inside the Control Plane

The Control Plane is made up of several components, each with a specific responsibility.

---

## API Server

The **API Server** is the front door of Kubernetes.

When you want to interact with a Kubernetes cluster, you typically use **`kubectl`**, the official Kubernetes command-line interface (CLI).

For example:

```bash
kubectl apply -f deployment.yaml
```

The `kubectl` command does **not** create Pods or make changes directly.

Instead, it sends a request to the **API Server**.

The API Server validates the request and coordinates the appropriate Kubernetes components to carry out the desired operation.

It's important to note that `kubectl` is just one client. Other tools, such as the Kubernetes Dashboard, CI/CD pipelines, and custom applications, also communicate with the cluster through the API Server.

Think of the API Server as the central communication hub of the Kubernetes cluster.

---

## etcd

`etcd` is Kubernetes' database.

It stores the cluster's desired state, including information about:

* Pods
* Deployments
* Services
* ConfigMaps
* Secrets
* Nodes

Whenever you apply a Kubernetes configuration, it is stored in `etcd`.

---

## Scheduler

The Scheduler decides **which worker node should run a Pod**.

It considers factors such as:

* Available CPU
* Available memory
* Node availability
* Scheduling rules

It then selects the most appropriate node for each Pod.

---

## Controller Manager

The Controller Manager continuously compares the desired state with the current state.

For example:

Desired:

```text
5 Pods
```

Current:

```text
4 Pods
```

The Controller Manager notices the difference and creates another Pod until the desired state is restored.

---

# ⚙️ Inside Every Worker Node

Each Worker Node also contains several components.

---

## Kubelet

The Kubelet runs on every worker node.

It receives instructions from the Control Plane and ensures the required Pods are running on that node.

---

## Container Runtime

Kubernetes does not run containers itself.

Instead, it relies on a **container runtime**, such as:

* containerd
* CRI-O

The container runtime is responsible for actually starting and stopping containers.

---

## kube-proxy

`kube-proxy` handles networking on the worker node.

It helps route traffic so applications can communicate reliably within the cluster.

---

# 🔄 How Everything Works Together

When you deploy an application, Kubernetes follows a series of steps.

```text
You
 │
 ▼
kubectl apply
 │
 ▼
API Server
 │
 ▼
etcd stores the desired state
 │
 ▼
Controller Manager detects a new application
 │
 ▼
Scheduler selects a Worker Node
 │
 ▼
Kubelet receives the instruction
 │
 ▼
Container Runtime starts the Pod
 │
 ▼
Application is Running
```

Each component has a single responsibility, and together they automate the deployment and management of your applications.

---

# 🎯 Key Takeaway

A Kubernetes cluster consists of:

* A **Control Plane**, which makes decisions.
* One or more **Worker Nodes**, which run your applications.

You describe the desired state of your application.

The Control Plane decides **what should happen**.

The Worker Nodes execute those decisions.

Understanding this architecture makes it much easier to learn the Kubernetes objects you'll encounter next.

In the next module, we'll deploy our **first Pod** and see how Kubernetes turns a simple YAML file into a running application.
