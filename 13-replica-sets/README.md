# 📦 13 — ReplicaSets

## 🎯 Goal

In the previous module, we learned how to create a Pod.

A Pod is great for running an application, but it has one major limitation:

**It doesn't guarantee that your application stays running.**

In this module, we'll understand how ReplicaSets solve that problem by ensuring the desired number of Pods are always running.

---

# 📁 Project Structure

```text
13-replica-sets/
│
├── replicaset.yaml
└── README.md
```

---

# 🧠 The Problem

Suppose you've deployed your application as a single Pod.

```text
Pod

└── Nginx Container
```

Everything works perfectly.

Now imagine someone accidentally deletes the Pod.

```bash
kubectl delete pod nginx-pod
```

Or perhaps the Pod crashes because of a node failure.

What happens?

Nothing.

Your application simply disappears because Kubernetes only created the Pod you asked for—it doesn't automatically recreate it.

For production applications, this is unacceptable.

---

# 💡 The Solution

Instead of creating Pods directly, Kubernetes provides **ReplicaSets**.

A ReplicaSet lets you define how many identical Pods should always be running.

For example:

```text
Desired Pods = 3
```

Kubernetes continuously compares the desired state with the current state.

```text
Desired: 3 Pods

Current: 3 Pods
```

Everything is healthy.

Now suppose one Pod disappears.

```text
Desired: 3 Pods

Current: 2 Pods
```

The ReplicaSet immediately notices the difference and creates a replacement Pod.

A few moments later:

```text
Desired: 3 Pods

Current: 3 Pods
```

Your application is healthy again.

This automatic recovery is called **self-healing**.

---

# 🧠 Mental Model

Think of a ReplicaSet as a manager.

```text
ReplicaSet

"I always want 3 Pods running."

        │
        ▼

Current: 2 Pods

        │
        ▼

Create one more Pod
```

ReplicaSets don't run containers themselves.

Instead, they continuously ensure that the desired number of Pods exists.

---

# 📄 ReplicaSet Configuration

`replicaset.yaml`

```yaml
apiVersion: apps/v1
kind: ReplicaSet

metadata:
  name: nginx-replicaset

spec:
  replicas: 3

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
```

---

# YAML Breakdown

## apiVersion

```yaml
apiVersion: apps/v1
```

Specifies which Kubernetes API manages ReplicaSets.

Unlike Pods (`v1`), ReplicaSets belong to the `apps/v1` API group.

---

## kind

```yaml
kind: ReplicaSet
```

Tells Kubernetes to create a ReplicaSet instead of a Pod.

---

## metadata

```yaml
metadata:
  name: nginx-replicaset
```

The name of the ReplicaSet resource.

---

## replicas

```yaml
replicas: 3
```

The desired number of Pods.

If fewer Pods are running, Kubernetes creates more.

If more Pods exist, Kubernetes removes the extras.

---

## selector

```yaml
selector:
  matchLabels:
    app: nginx
```

Defines which Pods belong to this ReplicaSet.

The ReplicaSet manages every Pod whose label matches:

```text
app=nginx
```

---

## template

```yaml
template:
```

This is the blueprint used whenever Kubernetes needs to create a new Pod.

Think of it as a reusable Pod definition.

---

## template.metadata.labels

```yaml
labels:
  app: nginx
```

Every Pod created by this ReplicaSet receives this label.

The ReplicaSet uses these labels to identify the Pods it owns.

---

## template.spec.containers

```yaml
containers:
  - name: nginx
    image: nginx:latest
```

Defines the container that runs inside every Pod created by the ReplicaSet.

---

# 🚀 Create the ReplicaSet

Apply the configuration:

```bash
kubectl apply -f replicaset.yaml
```

Verify it was created:

```bash
kubectl get rs
```

Example:

```text
NAME                DESIRED   CURRENT   READY
nginx-replicaset    3         3         3
```

Meaning:

* **DESIRED** → Number of Pods you requested.
* **CURRENT** → Number of Pods Kubernetes has created.
* **READY** → Number of healthy Pods ready to serve traffic.

---

# 🔍 View the Pods

```bash
kubectl get pods
```

Example:

```text
NAME                      READY   STATUS
nginx-replicaset-abc12    1/1     Running
nginx-replicaset-def34    1/1     Running
nginx-replicaset-ghi56    1/1     Running
```

Notice that the ReplicaSet automatically generates unique Pod names.

---

# 🧪 Experiment 1 — Self-Healing

Delete one of the Pods.

```bash
kubectl delete pod <pod-name>
```

Now watch the Pods:

```bash
kubectl get pods -w
```

You'll notice that Kubernetes immediately creates a replacement Pod.

Although one Pod was deleted, the ReplicaSet restores the desired number of running Pods.

---

# 🧪 Experiment 2 — Scaling

Open `replicaset.yaml` and change:

```yaml
replicas: 3
```

to

```yaml
replicas: 5
```

Apply the changes again:

```bash
kubectl apply -f replicaset.yaml
```

Run:

```bash
kubectl get pods
```

You'll now see five running Pods.

Next, change:

```yaml
replicas: 2
```

Apply the configuration again.

Kubernetes automatically removes the extra Pods until only two remain.

---

# 🔎 Inspect the ReplicaSet

View detailed information:

```bash
kubectl describe rs nginx-replicaset
```

Useful information includes:

* Desired replicas
* Current replicas
* Pod selector
* Pod template
* Events showing Pods being created or deleted

---

# 🗑️ Delete the ReplicaSet

```bash
kubectl delete rs nginx-replicaset
```

Deleting the ReplicaSet also removes the Pods it manages.

---

# 🎯 Key Takeaways

After completing this module, you understand:

* A Pod alone does not guarantee your application stays running.
* A ReplicaSet ensures a specified number of Pods always exist.
* ReplicaSets automatically recreate failed or deleted Pods (self-healing).
* Changing the `replicas` value scales your application up or down.
* ReplicaSets manage Pods using **labels** and **selectors**.
* The Pod **template** acts as a blueprint for creating new Pods.

In the next module, you'll learn about **Deployments**, which build on ReplicaSets and provide safe application updates, rolling deployments, and rollbacks.
