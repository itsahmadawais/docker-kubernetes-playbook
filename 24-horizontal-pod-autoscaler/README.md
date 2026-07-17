# 📦 24 — Horizontal Pod Autoscaler (HPA)

## 🎯 Goal

In previous modules, we manually scaled Deployments by changing the number of replicas.

While this works, it's not practical for real-world applications because traffic constantly changes throughout the day.

Kubernetes solves this problem using the **Horizontal Pod Autoscaler (HPA)**.

HPA automatically increases or decreases the number of Pods based on resource utilization, allowing applications to handle changing workloads without manual intervention.

In this module, we'll build a simple FastAPI application, generate CPU load, and watch Kubernetes automatically scale our Deployment.

---

# 📁 Project Structure

```text
24-horizontal-pod-autoscaler/
│
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── deployment.yaml
├── service.yaml
├── hpa.yaml
└── README.md
```

---

# 🧠 Why Horizontal Pod Autoscaler?

Imagine an API normally receives 50 requests per minute.

Suddenly, a marketing campaign brings thousands of users.

A single Pod may become overloaded.

Instead of manually increasing replicas, Kubernetes can automatically create additional Pods.

Likewise, when traffic decreases, Kubernetes removes unnecessary Pods to reduce resource usage.

---

# 🧠 Horizontal vs Vertical Scaling

There are two common approaches to scaling.

### Vertical Scaling

Increase the resources assigned to a Pod.

Example:

```text
1 CPU
↓

2 CPUs
```

The number of Pods remains the same.

---

### Horizontal Scaling

Increase the number of Pods.

```text
1 Pod

↓

2 Pods

↓

4 Pods
```

Traffic is distributed across multiple Pods.

This is the approach Kubernetes prefers.

---

# 🧠 How HPA Works

The Horizontal Pod Autoscaler continuously monitors metrics such as CPU or memory utilization.

```text
Pod Metrics

↓

Metrics Server

↓

Horizontal Pod Autoscaler

↓

Deployment

↓

Pods Scaled
```

When utilization exceeds the configured target, HPA increases the number of replicas.

When utilization falls, HPA gradually scales the Deployment back down.

---

# 🧠 CPU Requests Matter

HPA calculates utilization relative to the Pod's **CPU request**, **not** its CPU limit.

Example:

```yaml
resources:
  requests:
    cpu: "100m"

  limits:
    cpu: "500m"
```

If the Pod is currently using **500m CPU**, HPA calculates:

```text
500m ÷ 100m = 500% utilization
```

It does **not** compare usage against the CPU limit.

For this reason, configuring realistic CPU requests is important when using HPA.

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

          image: fastapi-hpa:latest
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8000

          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"

            limits:
              cpu: "500m"
              memory: "256Mi"
```

---

# 📄 Service

`service.yaml`

```yaml
apiVersion: v1
kind: Service

metadata:
  name: fastapi-service

spec:
  selector:
    app: fastapi

  ports:
    - port: 80
      targetPort: 8000

  type: ClusterIP
```

---

# 📄 Horizontal Pod Autoscaler

`hpa.yaml`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler

metadata:
  name: fastapi-hpa

spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-deployment

  minReplicas: 1
  maxReplicas: 5

  metrics:
    - type: Resource

      resource:
        name: cpu

        target:
          type: Utilization
          averageUtilization: 50
```

---

# 📝 YAML Breakdown

## scaleTargetRef

```yaml
scaleTargetRef:
```

Specifies which Deployment HPA should manage.

---

## minReplicas

```yaml
minReplicas: 1
```

The Deployment will never scale below one Pod.

---

## maxReplicas

```yaml
maxReplicas: 5
```

The Deployment will never scale above five Pods, even if CPU utilization remains high.

---

## averageUtilization

```yaml
averageUtilization: 50
```

HPA attempts to keep the average CPU utilization across all Pods near 50%.

---

# 🚀 Build the Docker Image

```bash
docker build -t fastapi-hpa ./app
```

---

# 🚀 Deploy the Application

```bash
kubectl apply -f .
```

---

# 🌐 Access the Application

Forward the Service to your local machine.

```bash
kubectl port-forward service/fastapi-service 8000:80
```

Open:

```text
http://localhost:8000/
```

---

# 🔍 Verify the Deployment

```bash
kubectl get deployments
```

```bash
kubectl get pods
```

Initially:

```text
NAME

fastapi-deployment-xxxxxxxxxx-xxxxx
```

Only one Pod should be running.

---

# 🔍 Watch HPA

```bash
kubectl get hpa -w
```

---

# 🔍 Watch Pods

Open another terminal.

```bash
kubectl get pods -w
```

---

# 🚀 Generate CPU Load

Continuously call the CPU-intensive endpoint.

Example (PowerShell):

```powershell
while ($true) {
    Invoke-WebRequest "http://localhost:8000/cpu" -UseBasicParsing | Out-Null
}
```

or

```powershell
while ($true) {
    curl.exe http://localhost:8000/cpu > $null
}
```

The application intentionally performs CPU-intensive work, causing CPU utilization to increase.

---

# 🔍 Observe Autoscaling

Initially:

```text
1 Pod
```

As CPU utilization increases:

```text
2 Pods

↓

3 Pods

↓

4 Pods

↓

5 Pods
```

If CPU utilization remains above the configured target after reaching five Pods, HPA will stop scaling because the maximum replica count has been reached.

Example:

```text
TARGETS

57% / 50%

REPLICAS

5
```

This means Kubernetes would like to create additional Pods but cannot because `maxReplicas` has been reached.

---

# 🔍 Scale Down

Stop generating traffic.

After a short stabilization period, Kubernetes gradually removes unnecessary Pods.

```text
5 Pods

↓

4 Pods

↓

3 Pods

↓

2 Pods

↓

1 Pod
```

This delay prevents Pods from constantly being created and removed during short traffic spikes.

---

# 🧠 Mental Model

```text
Traffic Increases

↓

CPU Usage Increases

↓

Metrics Server Collects Metrics

↓

Horizontal Pod Autoscaler

↓

CPU Above Target?

↓

Yes

↓

Create More Pods

↓

Reached maxReplicas?

↓

Yes

↓

Stop Scaling
```

---

# ⚠️ Metrics Server Requirement

Horizontal Pod Autoscaler depends on the Kubernetes **Metrics Server**.

Without it:

```bash
kubectl top pods
```

returns:

```text
error: Metrics API not available
```

and HPA reports:

```text
cpu: <unknown>/50%
```

In local Kubernetes environments such as **Kind**, the Metrics Server may also require the following argument to successfully collect metrics:

```text
--kubelet-insecure-tls
```

Managed Kubernetes services such as Amazon EKS, Google GKE, and Azure AKS typically provide a working Metrics Server configuration or documented installation process.

---

# 🎯 Key Takeaways

After completing this module, we understand:

- Horizontal Pod Autoscaler automatically scales Deployments based on resource utilization.
- HPA commonly scales using CPU or memory metrics collected by the Metrics Server.
- CPU utilization is calculated relative to **CPU requests**, not CPU limits.
- `minReplicas` defines the minimum number of Pods.
- `maxReplicas` defines the maximum number of Pods HPA is allowed to create.
- When CPU usage exceeds the configured target, Kubernetes automatically creates additional Pods.
- When demand decreases, Kubernetes gradually scales the Deployment back down.
- HPA requires a functioning Metrics Server to make scaling decisions.

---

In the next module, we'll explore **Helm**, the package manager for Kubernetes. Instead of manually writing and maintaining multiple YAML files, Helm allows us to package Kubernetes resources into reusable **Charts**, making deployments easier to configure, version, and share.