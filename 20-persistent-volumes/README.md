# 📦 20 — Persistent Volumes

## 🎯 Goal

In the Docker section of this playbook, we learned that **Volumes** allow data to survive container recreation.

Kubernetes solves the same problem for **Pods**.

By default, every Pod has its own writable filesystem. If the Pod is deleted, everything written inside that filesystem is lost.

In this module, we'll learn how **Persistent Volumes (PVs)** and **Persistent Volume Claims (PVCs)** allow applications to store data outside the Pod so it remains available even after the Pod is recreated.

We'll use a simple FastAPI application that writes and reads a text file to demonstrate data persistence.

---

# 📁 Project Structure

```text
20-persistent-volumes/
│
├── app/
│   ├── main.py
│   └── requirements.txt
│
├── Dockerfile
├── persistent-volume.yaml
├── persistent-volume-claim.yaml
├── deployment.yaml
└── README.md
```

---

# 🧠 Why Docker Volumes Aren't Enough

Docker Volumes solve the problem of preserving data when a **container** is recreated.

Kubernetes faces the same challenge with **Pods**.

Consider a simple application that writes a file.

```text
/data/message.txt
```

Initially:

```text
Pod

└── /data/message.txt
```

If the Pod is deleted:

```text
Pod ❌

↓

New Pod
```

The new Pod starts with a fresh filesystem, so the file is gone.

Applications that need to preserve data require storage that exists independently of individual Pods.

---

# 🧠 Persistent Volumes

Kubernetes solves this by separating storage from Pods.

Instead of storing files inside the Pod, applications write to a **Persistent Volume**.

```text
Pod

↓

Persistent Volume

↓

Disk
```

If the Pod is recreated:

```text
Old Pod ❌

↓

New Pod

↓

Same Persistent Volume
```

The application continues using the same storage, so previously written data remains available.

---

# 🧠 Persistent Volume vs Persistent Volume Claim

Kubernetes separates storage into two resources.

## Persistent Volume (PV)

A Persistent Volume represents the actual storage available to the cluster.

Examples include:

* Local disk
* AWS EBS
* Azure Disk
* Google Persistent Disk
* NFS

Think of a Persistent Volume as the storage itself.

---

## Persistent Volume Claim (PVC)

Applications don't use a Persistent Volume directly.

Instead, they create a **Persistent Volume Claim**, requesting storage from Kubernetes.

Kubernetes automatically binds the claim to a suitable Persistent Volume.

Think of a Persistent Volume Claim as a storage request.

---

# 🧠 Mental Model

```text
Pod
 │
 ▼
Persistent Volume Claim
 │
 ▼
Persistent Volume
 │
 ▼
Storage
```

The Pod doesn't care where the storage comes from.

It simply mounts the Persistent Volume Claim and uses it like a normal directory.

---

# 📄 Persistent Volume

`persistent-volume.yaml`

```yaml
apiVersion: v1
kind: PersistentVolume

metadata:
  name: fastapi-pv

spec:
  capacity:
    storage: 1Gi

  accessModes:
    - ReadWriteOnce

  hostPath:
    path: /tmp/k8s-data
```

---

# 📄 Persistent Volume Claim

`persistent-volume-claim.yaml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: fastapi-pvc

spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 1Gi
```

---

# 📄 Deployment Configuration

`deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: fastapi-deployment

spec:
  replicas: 1

  selector:
    matchLabels:
      app: fastapi

  template:
    metadata:
      labels:
        app: fastapi

    spec:
      containers:
        - name: fastapi
          image: fastapi-pv:latest

          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8000

          volumeMounts:
            - name: app-storage
              mountPath: /data

      volumes:
        - name: app-storage
          persistentVolumeClaim:
            claimName: fastapi-pvc
```

---

# 📝 YAML Breakdown

## Persistent Volume

```yaml
kind: PersistentVolume
```

Creates storage that can be used by applications.

For this module, we use a local `hostPath` to keep the example simple.

---

## Persistent Volume Claim

```yaml
kind: PersistentVolumeClaim
```

Requests storage from Kubernetes.

The claim is automatically bound to a matching Persistent Volume.

---

## volumeMounts

```yaml
volumeMounts:
```

Mounts the Persistent Volume inside the container.

Our FastAPI application writes files to:

```text
/data
```

---

## volumes

```yaml
volumes:
```

Connects the Pod to the Persistent Volume Claim.

This allows the application to access persistent storage.

---

# 🚀 Build the Docker Image

```bash
docker build -t fastapi-pv:latest .
```

---

# 🚀 Create the Persistent Volume

```bash
kubectl apply -f persistent-volume.yaml
```

Verify:

```bash
kubectl get pv
```

Example output:

```text
NAME         CAPACITY   ACCESS MODES   STATUS
fastapi-pv   1Gi        RWO            Available
```

---

# 🚀 Create the Persistent Volume Claim

```bash
kubectl apply -f persistent-volume-claim.yaml
```

Verify:

```bash
kubectl get pvc
```

Example output:

```text
NAME          STATUS   VOLUME
fastapi-pvc   Bound    fastapi-pv
```

Notice that the claim is now **Bound** to the Persistent Volume.

---

# 🚀 Deploy the Application

```bash
kubectl apply -f deployment.yaml
```

Verify the Pod is running:

```bash
kubectl get pods
```

---

# 🌐 Access the Application

Forward a local port to the Pod.

```bash
kubectl port-forward pod/<pod-name> 8000:8000
```

Open:

```text
http://localhost:8000/docs
```

---

# ✍️ Write Data

Call:

```http
POST /write
```

Example request body:

```json
{
  "message": "Hello Kubernetes!"
}
```

---

# 📖 Read the Data

Call:

```http
GET /read
```

Example response:

```json
{
  "message": "Hello Kubernetes!"
}
```

At this point, the message has been written to the mounted Persistent Volume.

---

# 🗑️ Delete the Pod

Delete the running Pod.

```bash
kubectl delete pod <pod-name>
```

Because the application is managed by a Deployment, Kubernetes automatically creates a replacement Pod.

Watch the new Pod appear:

```bash
kubectl get pods -w
```

---

# 🔍 Verify Data Persistence

Forward the port to the new Pod.

```bash
kubectl port-forward pod/<new-pod-name> 8000:8000
```

Call:

```http
GET /read
```

Example response:

```json
{
  "message": "Hello Kubernetes!"
}
```

Although the original Pod no longer exists, the file is still available because it was stored on the Persistent Volume rather than inside the Pod.

---

# 🧠 Mental Model

Think of the process like this.

```text
Old Pod
    │
    ▼
Persistent Volume
    ▲
    │
New Pod
```

The Pod changes.

The storage doesn't.

The new Pod simply mounts the same Persistent Volume and continues using the existing data.

---

# 🎯 Key Takeaways

After completing this module, we understand:

* Pods have ephemeral filesystems by default.
* Persistent Volumes provide storage that survives Pod recreation.
* Persistent Volume Claims allow applications to request storage without depending on a specific disk.
* Applications access Persistent Volumes through normal filesystem paths.
* Deleting a Pod does not delete data stored on a Persistent Volume.
* Persistent storage is essential for applications that need to preserve data beyond the lifetime of individual Pods.

In the next module, we'll explore **StatefulSets**, which build upon Persistent Volumes to run stateful applications such as databases and distributed systems.
