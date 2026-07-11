# 📦 15 — Services

## 🎯 Goal

In the previous module, we learned how Deployments keep our application running by creating and replacing Pods.

However, there's still a problem.

Pods are **ephemeral**—they can be created, deleted, and recreated at any time. When this happens, their IP addresses change.

If another application communicates directly with a Pod's IP, that connection will eventually break.

A **Service** solves this problem by providing a **stable IP address and DNS name** that always route traffic to the correct Pods, even as Pods come and go.

---

# 📁 Project Structure

```text
15-services/
│
├── deployment.yaml
├── service.yaml
└── README.md
```

---

# 🧠 The Problem

Imagine we deploy three Pods.

```text
Deployment
      │
      ▼
Pod A (10.244.0.17)

Pod B (10.244.0.18)

Pod C (10.244.0.19)
```

Each Pod has its own IP address.

If Pod A crashes, Kubernetes creates a replacement.

```text
Pod A ❌

↓

Pod D (10.244.0.25)
```

The IP changed.

Any application using the old IP now fails.

Instead of connecting to Pods directly, Kubernetes encourages applications to communicate through a **Service**.

---

# 🧠 How a Service Works

A Service sits in front of one or more Pods.

```text
                Service
          (Stable IP / DNS)
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
     Pod A      Pod B     Pod C
```

Applications communicate with the Service instead of talking directly to individual Pods.

The Service discovers Pods using **label selectors** and automatically **load-balances** incoming requests across the healthy Pods.

If a Pod is deleted and Kubernetes creates a replacement, the Service automatically updates its list of available endpoints without requiring any changes from the client.

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

# 📄 Service Configuration

`service.yaml`

```yaml
apiVersion: v1
kind: Service

metadata:
  name: nginx-service

spec:
  selector:
    app: nginx

  ports:
    - port: 80
      targetPort: 80

  type: ClusterIP
```

---

# 📝 YAML Breakdown for `service.yaml`

## selector

```yaml
selector:
  app: nginx
```

The Service searches for Pods whose labels match:

```yaml
labels:
  app: nginx
```

Only those Pods become Service endpoints.

---

## ports

```yaml
ports:
  - port: 80
    targetPort: 80
```

There are two ports involved:

- **port** – The port clients use when communicating with the Service.
- **targetPort** – The port the application is listening on inside the container.

In this example, nginx listens on port `80`, so both values are the same.

For a FastAPI application, it might look like:

```yaml
ports:
  - port: 80
    targetPort: 8000
```

Clients connect to the Service on port `80`, while the Service forwards traffic to port `8000` inside the container.

---

## type

```yaml
type: ClusterIP
```

`ClusterIP` is the default Service type.

It creates an internal Service that can only be accessed from within the Kubernetes cluster.

Kubernetes also supports other Service types such as `NodePort` and `LoadBalancer` for exposing applications outside the cluster, but `ClusterIP` is the most common choice for communication between applications running inside Kubernetes.

---

# 🚀 Create the Resources

Deploy the application:

```bash
kubectl apply -f deployment.yaml
```

Create the Service:

```bash
kubectl apply -f service.yaml
```

---

# 🔍 Verify Everything

Check the Deployment:

```bash
kubectl get deployments
```

Check the Pods:

```bash
kubectl get pods
```

Check the Service:

```bash
kubectl get svc
```

Example:

```text
NAME            TYPE        CLUSTER-IP      PORT(S)
nginx-service   ClusterIP   10.96.162.197   80/TCP
```

---

# 📍 View Service Endpoints

A Service doesn't create Pods—it discovers existing Pods using its selector.

View the endpoints:

```bash
kubectl get endpoints
```

Example:

```text
NAME            ENDPOINTS
nginx-service   10.244.0.17:80,10.244.0.18:80,10.244.0.19:80
```

Each endpoint represents one healthy Pod behind the Service.

Kubernetes manages this list automatically as Pods are created, deleted, or replaced.

---

# 🌐 Access the Service

Since `ClusterIP` is only accessible inside the cluster, we can temporarily forward a local port to the Service:

```bash
kubectl port-forward service/nginx-service 8080:80
```

Open:

```text
http://localhost:8080
```

Traffic flows like this:

```text
Browser
      │
localhost:8080
      │
kubectl port-forward
      │
nginx-service
      │
One of the nginx Pods
```

---

# 🧠 Mental Model

Think of a Service as a receptionist.

Applications don't need to know where each Pod is running.

Instead, they simply send requests to the Service.

```text
           Client
              │
              ▼
        nginx-service
              │
      ┌───────┴────────┐
      ▼       ▼        ▼
    Pod A   Pod B    Pod C
```

As Pods are created, deleted, or replaced, the Service continues routing requests to healthy Pods without requiring clients to update any IP addresses.

---

# 🎯 Key Takeaways

After completing this module, we understand:

- Pods have temporary IP addresses.
- A Service provides a stable IP address and DNS name for accessing Pods.
- Services discover Pods using label selectors.
- Services automatically load-balance requests across healthy Pods.
- `port` is the Service's port, while `targetPort` is the container's listening port.
- `ClusterIP` creates an internal Service that is accessible only within the Kubernetes cluster.
- A Service does **not** create Pods—it discovers and routes traffic to existing Pods.
- Applications should communicate through Services rather than directly with Pod IP addresses.

In the next module, we'll learn how **ConfigMaps** allow applications to separate configuration from container images.