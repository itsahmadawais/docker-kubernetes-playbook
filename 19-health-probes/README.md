# 📦 19 — Health Probes

## 🎯 Goal

In the previous module, we learned how **Resource Requests and Limits** help Kubernetes decide where Pods should run and how much CPU and memory they are allowed to use.

However, even if a Pod is running, that doesn't necessarily mean the application inside it is ready to serve requests or is still functioning correctly.

Docker provides a basic `HEALTHCHECK` instruction to determine whether a container is healthy. Kubernetes takes this concept much further by introducing **Health Probes**. 

A **Health Probe** is simply a periodic diagnostic check performed by Kubernetes directly on your container. It allows the cluster to understand:
* Has the application finished starting?
* Is the application ready to receive traffic?
* Is the application still healthy, or should it be restarted?

In this module, we'll use a small FastAPI application to simulate realistic application behavior and observe how Kubernetes uses Health Probes to manage an application's lifecycle automatically.

---

# 📁 Project Structure

```text
19-health-probes/
│
├── app/
│   ├── main.py
│   └── requirements.txt
│
├── Dockerfile
├── deployment.yaml
└── README.md

```

---

# 🧠 Why Docker HEALTHCHECK Isn't Enough

Docker supports a single health check using the `HEALTHCHECK` instruction. While useful, Docker only answers one basic question:

> "Is this container healthy?"

Kubernetes needs more information to manage real-world apps.

Consider a web application that takes 20 seconds to initialize. During startup:

* The container is running.
* The application isn't ready yet.
* Restarting the container would only make things worse.

Likewise, an application might be running but temporarily unable to serve requests because it is still connecting to a database.

To solve this, Kubernetes separates these concerns into **three different probes**.

---

# 🧠 The Three Health Probes

### 🚀 Startup Probe

Determines whether the application has finished starting. While the Startup Probe is failing, Kubernetes waits patiently and does **not** run liveness or readiness checks. This prevents slow-starting apps from being killed prematurely.

### 🚦 Readiness Probe

Determines whether the application is ready to receive traffic. If the Readiness Probe fails, Kubernetes stops sending requests to the Pod, but keeps the Pod running.

### 🩺 Liveness Probe

Determines whether the application is still functioning correctly. If the Liveness Probe fails repeatedly, Kubernetes assumes the app is stuck or crashed and automatically restarts the container.

---

# 🧠 Mental Model

```text
Container Starts
        │
        ▼
Startup Probe
        │
        ▼
Application Started?
        │
       Yes
        │
        ▼
Readiness Probe ◄────────────────┐
        │                        │
        ▼                        │
Ready to receive traffic?        │
        │                        │
       Yes                       │
        │                        │
        ▼                        │
Traffic reaches Pod              │
        │                        │
        ▼                        │
Liveness Probe                   │
        │                        │
        ▼                        │
Application Healthy?             │
        │                        │
       Yes ──────────────────────┘
        │
        No
        │
        ▼
Restart Container

```

---

# 🔍 Probe Types

Kubernetes supports multiple ways to check your application's health.

### 🌐 HTTP Probe

Kubernetes sends an HTTP request to the application. Any response code between 200 and 399 indicates success.

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000

```

*This is the most common approach for web applications and REST APIs.*

### 🔌 TCP Probe

Kubernetes simply checks whether it can establish a raw network connection to a port.

```yaml
livenessProbe:
  tcpSocket:
    port: 5432

```

*This is commonly used for databases, caches, and message brokers.*

### 💻 Exec Probe

Kubernetes executes a specific command inside the container. An exit code of `0` indicates success.

```yaml
livenessProbe:
  exec:
    command:
      - cat
      - /tmp/healthy

```

### Which Probe Type Should I Use?

| Probe Type | Typical Use Cases |
| --- | --- |
| **HTTP** | Web applications and REST APIs |
| **TCP** | Databases, caches, message brokers |
| **Exec** | Custom applications requiring internal validation scripts |

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
          image: fastapi-health:latest

          ports:
            - containerPort: 8000

          # Allows Kubernetes to wait for slow-starting applications
          startupProbe:
            httpGet:
              path: /startup
              port: 8000
            periodSeconds: 5
            failureThreshold: 6

          # Controls whether the Pod receives user traffic
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 3
            periodSeconds: 5

          # Continuously checks whether the application needs a restart
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5

```

---

# 🚀 Build and Deploy the Application

### 1. Build the Docker Image

```bash
docker build -t fastapi-health:latest .

```

### 2. Deploy to Kubernetes

```bash
kubectl apply -f deployment.yaml

```

### 3. Watch the Pod Status

```bash
kubectl get pods -w

```

Initially, you will notice:

```text
READY    STATUS
0/1      Running

```

The container is already running, but the application hasn't passed its Startup and Readiness probes yet.

After the application finishes starting, it transitions to:

```text
READY    STATUS
1/1      Running

```

> ⚠️ **Key Takeaway:** A Pod being **Running** does not necessarily mean it is **Ready** to receive traffic.

---

# 🌐 Access the Application

Because the FastAPI application runs inside the isolated Kubernetes cluster, it isn't directly accessible from your local machine. We will temporarily forward a local port to the Pod to interact with it.

### 1. Get your Pod's name:

```bash
kubectl get pods

```

### 2. Forward your local port to the Pod:

```bash
kubectl port-forward pod/<pod-name> 8000:8000

```

You can now access the application endpoints locally in your browser or via `curl`:

* `http://localhost:8000/`
* `http://localhost:8000/startup`
* `http://localhost:8000/ready`
* `http://localhost:8000/health`

> 💡 *Note: We're using `kubectl port-forward` for local testing simplicity. In production, applications are accessed securely through a Kubernetes Service.*

---

# 🔬 Probes in Action

### 1. Startup Probe in Action

Our FastAPI application intentionally waits a bit before completing its startup. During this time, the Startup Probe will fail a few times.

If you run `kubectl describe pod <pod-name>`, you will see these events at the bottom:

```text
Warning  Unhealthy  ...  Startup probe failed: connect: connection refused

```

Despite these initial failures, notice that the **Restart Count** remains `0`. Kubernetes understands that the application is still initializing and lets it finish booting up instead of aggressively restarting it.

### 2. Liveness Probe in Action (Self-Healing)

Our application exposes a special endpoint designed to simulate a broken app. To intentionally break the application, run:

```bash
curl -X POST http://localhost:8000/break

```

Once called, the `/health` endpoint starts returning a server error. Watch your pods now:

```bash
kubectl get pods -w

```

After a few failed health checks, Kubernetes automatically steps in and restarts the container. You will see the change live:

```text
NAME                                  READY   STATUS    RESTARTS   AGE
fastapi-deployment-7f49c5b4d-xxxxx   1/1     Running   1          90s

```

Notice that the **Restart Count** increased to `1`. This demonstrates Kubernetes' built-in self-healing capability.

---

# 🎯 Key Takeaways

* Docker provides a single binary check, while Kubernetes offers three specialized health probes.
* **Startup Probes** allow slow-starting applications to initialize without getting caught in a restart loop.
* **Readiness Probes** safely remove broken or busy Pods from receiving traffic without deleting them.
* **Liveness Probes** act as an automatic system administrator, restarting frozen or crashed containers.
* A Pod can be actively **Running** but not yet **Ready** to handle traffic.

In the next module, we'll explore **Persistent Volumes**, which allow applications to save data beyond the lifetime of individual Pods.