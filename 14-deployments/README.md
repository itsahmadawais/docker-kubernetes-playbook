# 📦 14 — Deployments

## 🎯 Goal

In the previous module, we learned that a ReplicaSet keeps the desired number of Pods running.

But what happens when we need to deploy a new version of our application?

Imagine we have three Pods running version `1.0` of our application. We build version `1.1` and want users to start using it.

One option would be to delete all existing Pods and create new ones.

The problem?

There would be a period where no Pods are available, causing downtime.

Deployments solve this problem by updating Pods gradually while keeping the application available.

---

# 📁 Project Structure

```text
14-deployments/
│
├── deployment.yaml
└── README.md
```

---

# 🧠 ReplicaSet vs Deployment

A ReplicaSet has one responsibility:

> Keep the desired number of Pods running.

```text
ReplicaSet
     │
     ▼
3 Pods
```

A Deployment sits one level above a ReplicaSet.

```text
Deployment
     │
     ▼
ReplicaSet
     │
     ▼
Pods
```

Instead of managing Pods directly, a Deployment manages ReplicaSets.

This allows Kubernetes to safely deploy new versions and recover quickly if something goes wrong.

---

# 📄 Deployment Configuration

`deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: nginx-deployment

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

# 📝 New YAML Field

Compared to a Pod manifest, a Deployment introduces one new concept.

## kind

```yaml
kind: Deployment
```

Instead of creating a ReplicaSet directly, we're creating a Deployment.

The Deployment is responsible for managing ReplicaSets, which in turn manage Pods.

Everything else inside the Pod template should already look familiar from the previous modules.

---

# 🚀 Create the Deployment

Apply the manifest:

```bash
kubectl apply -f deployment.yaml
```

Verify the Deployment:

```bash
kubectl get deployments
```

View the ReplicaSet created by the Deployment:

```bash
kubectl get rs
```

Finally, list the Pods:

```bash
kubectl get pods
```

Notice that we only created a Deployment, yet Kubernetes automatically created a ReplicaSet, which then created the Pods.

```text
Deployment
     │
     ▼
ReplicaSet
     │
     ▼
3 Pods
```

---

# 🔍 Inspect the Deployment

View detailed information:

```bash
kubectl describe deployment nginx-deployment
```

Useful information includes:

- Desired replicas
- Current replicas
- Update strategy
- Pod template
- Old and new ReplicaSets
- Events

---

# 🔄 Rolling Updates

Let's deploy a new version of nginx.

Update the image:

```yaml
image: nginx:1.27
```

Apply the changes:

```bash
kubectl apply -f deployment.yaml
```

Watch the rollout:

```bash
kubectl get pods -w
```

Instead of deleting all Pods at once, Kubernetes creates a new Pod first, waits until it becomes healthy, and only then removes one of the old Pods.

This process continues until every Pod has been replaced.

```text
Old ReplicaSet (3 Pods)

↓

New ReplicaSet (3 Pods)
```

This is called a **Rolling Update**, allowing applications to be updated with little or no downtime.

---

# 📜 Deployment History

Every time the Pod template changes, Kubernetes creates a new Deployment revision.

View the revision history:

```bash
kubectl rollout history deployment nginx-deployment
```

Each revision represents a different version of your application.

---

# ↩️ Why Rollbacks Matter

Imagine your application is running version **1.0**.

Everything is working perfectly.

```text
Users

      │

      ▼

Application v1.0 ✅
```

You release version **1.1** using your Deployment.

A few minutes later, users start reporting problems:

- Login is broken.
- Orders cannot be placed.
- The application crashes unexpectedly.

You know how to fix the bug, but it may take 20–30 minutes to investigate, update the code, build a new Docker image, and deploy it.

Can your users wait that long?

Usually, the answer is **no**.

Instead of keeping the broken version online, Kubernetes allows you to quickly return to the last working version.

```text
Application v1.0

      │

      ▼

Deploy v1.1

      │

      ▼

Problem Found ❌

      │

      ▼

Rollback

      │

      ▼

Application v1.0 ✅
```

The rollback itself is another rolling update. Kubernetes gradually replaces the broken Pods with Pods from the previous ReplicaSet.

Users can continue using the application while your team fixes the issue.

Once the bug has been resolved, you build a new image (for example, **v1.2**) and deploy again.

---

# ↩️ Roll Back a Deployment

Restore the previous version:

```bash
kubectl rollout undo deployment/nginx-deployment
```

Watch the rollback:

```bash
kubectl get pods -w
```

You'll notice the same rolling update behavior, except Kubernetes is now replacing the current Pods with Pods from the previous ReplicaSet.

---

# 🏗️ Typical Deployment Workflow

A typical deployment process looks like this:

```text
Developer writes code
        │
        ▼
Build Docker image
        │
        ▼
Push image to registry
        │
        ▼
Update Deployment
        │
        ▼
kubectl apply
        │
        ▼
Rolling Update
```

If a problem is discovered:

```text
Deploy v1.1
      │
      ▼
Bug Found
      │
      ▼
Rollback to v1.0
      │
      ▼
Fix the bug
      │
      ▼
Build v1.2
      │
      ▼
Deploy Again
```

The rollback is only a temporary safety net. The real solution is to fix the application and release a corrected version.

---

# 🎯 Key Takeaways

After completing this module, we understand:

- A Deployment manages ReplicaSets.
- ReplicaSets manage Pods.
- Deployments perform rolling updates with minimal downtime.
- Every Deployment update creates a new revision.
- Previous revisions can be restored using `kubectl rollout undo`.
- Rollbacks help restore a stable version while developers fix production issues.
- In production, images should be versioned (for example, `1.0.0`, `1.1.0`) instead of using `latest`.

In the next module, we'll learn how applications communicate inside a Kubernetes cluster using **Services**.