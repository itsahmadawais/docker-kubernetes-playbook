# 📦 18 — Resource Requests and Limits

## 🎯 Goal

In the previous modules, Kubernetes scheduled Pods onto available nodes for us.

But how does Kubernetes decide **which node (server)** has enough capacity to run a Pod?

And what prevents one application from consuming all the CPU or memory on a node?

This is where **Resource Requests and Limits** come in.

They allow us to tell Kubernetes:

* The **minimum** resources our application needs.
* The **maximum** resources our application is allowed to consume.

---

# 📁 Project Structure

```text
18-resource-requests-limits/
│
├── deployment.yaml
└── README.md
```

---

# 🧠 The Problem

Imagine a Kubernetes **node (server)** with limited resources.

```text
Node

CPU:    2 Cores
Memory: 2 GiB
```

Now suppose we deploy several applications.

```text
API

Worker

Redis
```

Without resource limits, one application could gradually consume most of the available CPU or memory.

As a result:

* Other applications become slow.
* Pods may crash.
* The entire node becomes unstable.

Kubernetes solves this by allowing us to define **resource requests** and **resource limits** for every Pod.

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

          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"

            limits:
              cpu: "200m"
              memory: "128Mi"
```

---

# 📝 YAML Breakdown

## requests

```yaml
requests:
  cpu: "100m"
  memory: "64Mi"
```

Requests define the **minimum resources** Kubernetes guarantees for a Pod.

The Kubernetes scheduler uses these values to determine whether a node has enough available CPU and memory to run the Pod.

If no node can satisfy the requested resources, the Pod remains in the **Pending** state.

---

## limits

```yaml
limits:
  cpu: "200m"
  memory: "128Mi"
```

Limits define the **maximum resources** a Pod is allowed to consume.

If the running application exceeds these limits:

* CPU usage is throttled.
* Memory overuse causes the container to be terminated (`OOMKilled`).

---

# 🧠 CPU Units

CPU is measured in **cores**.

Kubernetes allows us to specify CPU as either **whole CPU cores** or **millicores** (`m`).

|   Value | Meaning       |
| ------: | ------------- |
|  `100m` | 0.1 CPU core  |
|  `250m` | 0.25 CPU core |
|  `500m` | 0.5 CPU core  |
| `1000m` | 1 CPU core    |
|     `2` | 2 CPU cores   |
|     `4` | 4 CPU cores   |
|     `8` | 8 CPU cores   |

The `m` stands for **millicores**, where:

```text
1000m = 1 CPU Core
```

Small applications typically use millicores, while larger workloads may request one or more full CPU cores.

---

# 🧠 Memory Units

Memory is commonly specified using binary units.

|   Value | Meaning       |
| ------: | ------------- |
|  `64Mi` | 64 Mebibytes  |
| `128Mi` | 128 Mebibytes |
| `512Mi` | 512 Mebibytes |
|   `1Gi` | 1 Gibibyte    |
|   `2Gi` | 2 Gibibytes   |
|  `16Gi` | 16 Gibibytes  |

---

# 🚀 Deploy the Application

Create the Deployment:

```bash
kubectl apply -f deployment.yaml
```

Verify the Deployment:

```bash
kubectl get deployments
```

List the Pods:

```bash
kubectl get pods
```

Inspect one of the Pods:

```bash
kubectl describe pod <pod-name>
```

The output contains many details. Focus on the **Requests** and **Limits** section:

```text
Requests:
  cpu:     100m
  memory:  64Mi

Limits:
  cpu:     200m
  memory:  128Mi
```

Notice that Kubernetes stores both the requested resources and the maximum allowed resources for every container.

---

# 🧪 Experiment 1 — Insufficient Resources

Let's see how Kubernetes uses **requests** during scheduling.

Update the Deployment:

```yaml
resources:
  requests:
    cpu: "8"
    memory: "16Gi"

  limits:
    cpu: "10"
    memory: "128Gi"
```

Apply the changes:

```bash
kubectl apply -f deployment.yaml
```

Watch the Pods:

```bash
kubectl get pods
```

Example:

```text
NAME                                STATUS

nginx-deployment-546c8cb74c-9wjml   Running
nginx-deployment-546c8cb74c-j9v2w   Running
nginx-deployment-546c8cb74c-lcg4n   Running
nginx-deployment-74c5f94485-97kqp   Pending
```

Inspect the Pending Pod:

```bash
kubectl describe pod <pod-name>
```

Example output:

```text
FailedScheduling

0/1 nodes are available:
1 Insufficient memory
```

Notice that the Pod never reaches the `Running` state.

Since no node has enough available CPU and memory to satisfy the requested resources, Kubernetes leaves the Pod in the **Pending** state until sufficient resources become available.

This demonstrates that **requests are used by the Kubernetes scheduler**.

---

# 🧪 Experiment 2 — Invalid Resource Configuration

Requests must always be **less than or equal to** limits.

For example:

```yaml
resources:
  requests:
    memory: "64Mi"

  limits:
    memory: "18Mi"
```

Apply the Deployment:

```bash
kubectl apply -f deployment.yaml
```

Kubernetes immediately rejects the manifest.

Example:

```text
The Deployment "nginx-deployment" is invalid:

spec.template.spec.containers[0].resources.requests:

Invalid value: "64Mi":
must be less than or equal to memory limit of 18Mi
```

The same validation applies to CPU.

For example:

```yaml
requests:
  cpu: "500m"

limits:
  cpu: "200m"
```

is also invalid.

The rule is simple:

```text
Request ≤ Limit
```

A Pod cannot request more resources than it is allowed to consume.

---

# 🧠 Mental Model

Think of requests and limits as defining the operating range for a Pod.

```text
                    Pod

      Request                    Limit
      ┌───────┐              ┌────────┐
CPU   │100m   │────────────▶ │200m    │
      └───────┘              └────────┘

Memory
      ┌───────┐              ┌────────┐
      │64Mi   │────────────▶ │128Mi   │
      └───────┘              └────────┘
```

* **Request** = Minimum resources Kubernetes guarantees.
* **Limit** = Maximum resources the Pod is allowed to consume.

---

# 🎯 Key Takeaways

After completing this module, we understand:

* Resource **requests** define the minimum CPU and memory Kubernetes guarantees for a Pod.
* The Kubernetes scheduler uses **requests** to decide where a Pod can run.
* Resource **limits** define the maximum CPU and memory a Pod may consume.
* CPU can be specified using **cores** or **millicores** (`1000m = 1 CPU core`).
* Memory is commonly specified using **Mi** and **Gi**.
* If a Pod exceeds its CPU limit, Kubernetes throttles its CPU usage.
* If a Pod exceeds its memory limit, the container is terminated (`OOMKilled`).
* Requests must always be less than or equal to limits.
* If no node has enough resources to satisfy a Pod's requests, the Pod remains in the **Pending** state until resources become available.

In the next module, we'll learn about **Health Probes**, which allow Kubernetes to determine whether an application is healthy, ready to receive traffic, or needs to be restarted.
