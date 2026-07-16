# 📦 23 — Ingress

## 🎯 Goal

In previous modules, we learned that a **Service** provides a stable endpoint for Pods inside the Kubernetes cluster.

However, Services are primarily intended for **internal cluster communication**.

If users need to access an application from outside the cluster, Kubernetes requires another component.

This is where **Ingress** comes in.

Ingress provides a single entry point for external HTTP and HTTPS traffic and routes requests to the appropriate Services based on rules such as URL paths or hostnames.

In this module, we'll deploy a simple frontend and a FastAPI backend, then configure an Ingress to route requests to the correct application.

---

# 📁 Project Structure

```text
23-ingress/
│
├── api/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   └── Dockerfile
│
├── api-deployment.yaml
├── api-service.yaml
├── frontend-deployment.yaml
├── frontend-service.yaml
├── ingress.yaml
└── README.md
```

---

# 🧠 Why Do We Need Ingress?

Suppose we have two applications:

- Frontend
- REST API

Without Ingress, each Service would need its own external endpoint.

```text
Frontend Service
        │
        ▼
External Endpoint

API Service
        │
        ▼
External Endpoint
```

As applications grow, managing multiple external endpoints becomes difficult.

Ingress solves this by providing a **single entry point**.

```text
Internet
        │
        ▼
Ingress
        │
 ┌──────┴──────┐
 │             │
 ▼             ▼
Frontend     API
Service      Service
```

---

# 🧠 Kubernetes Networking Flow

```text
Browser
      │
      ▼
Ingress Controller
      │
      ▼
Ingress
      │
      ▼
Service
      │
      ▼
Pods
```

Each component has a specific responsibility.

| Component | Responsibility |
| ---------- | -------------- |
| Pod | Runs the application |
| Service | Provides a stable endpoint for Pods |
| Ingress | Defines routing rules |
| Ingress Controller | Implements those routing rules |

---

# 🧠 Service vs Ingress

| Service | Ingress |
| -------- | -------- |
| Exposes Pods | Exposes Services |
| Used for internal cluster networking | Used for external HTTP/HTTPS access |
| Load balances traffic across Pods | Routes requests to different Services |
| One Service per application | One Ingress can expose many Services |

---

# 📄 Ingress Configuration

`ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress

metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2

spec:
  ingressClassName: nginx

  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80

          - path: /api(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

---

# 📝 YAML Breakdown

## `ingressClassName`

```yaml
ingressClassName: nginx
```

Specifies that this Ingress should be managed by the NGINX Ingress Controller.

---

## `rewrite-target`

```yaml
annotations:
  nginx.ingress.kubernetes.io/rewrite-target: /$2
```

Rewrites the incoming request path before forwarding it to the backend Service.

For example:

```text
Incoming Request

/api/users

        │

        ▼

After Rewrite

/users
```

This allows the FastAPI application to define routes such as:

```text
/
```

and

```text
/users
```

instead of:

```text
/api
/api/users
```

---

## Frontend Route

```yaml
path: /
```

Routes requests for the frontend application.

```text
http://localhost/
        │
        ▼
frontend-service
```

---

## API Route

```yaml
path: /api(/|$)(.*)
```

Routes requests beginning with `/api` to the FastAPI Service.

Combined with the rewrite annotation:

```text
/api
        │
        ▼
/

/api/users
        │
        ▼
/users
```

This allows Ingress to expose the API under `/api` while keeping the backend application unaware of that prefix.

---

# 🚀 Build Docker Images

```bash
docker build -t fastapi-ingress ./api

docker build -t frontend-ingress ./frontend
```

---

# 🚀 Deploy Everything

Apply all Kubernetes resources:

```bash
kubectl apply -f .
```

---

# 🔍 Verify Resources

Verify that the Pods are running:

```bash
kubectl get pods
```

Verify the Services:

```bash
kubectl get services
```

Verify the Ingress:

```bash
kubectl get ingress
```

You should see an Ingress similar to:

```text
NAME          CLASS   ADDRESS

app-ingress   nginx   <address>
```

---

# 🌐 Access the Application

An Ingress resource only defines routing rules.

To make those rules functional, the cluster must have an **Ingress Controller** installed.

For this module, we use the **NGINX Ingress Controller**.

In our local environment, we'll temporarily expose the Ingress Controller using port forwarding.

```bash
kubectl port-forward \
    -n ingress-nginx \
    service/ingress-nginx-controller \
    8080:80
```

Now open:

Frontend

```text
http://localhost:8080/
```

FastAPI

```text
http://localhost:8080/api
```

Notice that both applications are accessed through a **single entry point**, while Ingress automatically routes each request to the correct Service.

> **Note**
>
> In production environments, the Ingress Controller is typically exposed through a LoadBalancer or another external endpoint, so `kubectl port-forward` is not required.

---

# 🧠 Mental Model

```text
Browser
      │
      ▼
Ingress Controller
      │
      ▼
Ingress Rules
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Frontend   API
Service    Service
 │          │
 ▼          ▼
Pods      Pods
```

---

# 🎯 Key Takeaways

After completing this module, we understand:

- Services expose Pods inside the Kubernetes cluster.
- Ingress exposes Services to external users through a single entry point.
- Ingress routes traffic based on paths or hostnames.
- An Ingress Controller is required to implement Ingress rules.
- URL rewriting allows backend applications to remain independent of external URL structures.
- Multiple applications can share a single external endpoint.
- In production, Ingress Controllers are typically exposed through a LoadBalancer or another external endpoint.

In the next module, we'll explore **Horizontal Pod Autoscaler (HPA)**, which automatically scales the number of Pods based on resource utilization such as CPU or memory, allowing applications to handle changing workloads efficiently.