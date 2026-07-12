# 📦 16 — ConfigMaps

## 🎯 Goal

So far, we've learned how to package applications with Docker and deploy them using Kubernetes.

But there's still one question:

**Where should application configuration live?**

Imagine we have a FastAPI application that connects to a database.

```python
DATABASE_HOST = "postgres"
DATABASE_PORT = 5432
LOG_LEVEL = "INFO"
```

Everything works in development.

Later, we deploy the same application to production.

Now the database host changes.

```text
prod-db.company.com
```

The logging level should also change.

```text
WARNING
```

Should we edit the code?

Should we rebuild the Docker image?

Not really.

The application is exactly the same. Only the configuration has changed.

This is the problem that **ConfigMaps** solve.

---

# 📁 Project Structure

```text
16-configmaps/
│
├── configmap.yaml
├── deployment.yaml
└── README.md
```

---

# 🧠 How Docker Solved This

We've already seen this concept in Docker.

Instead of hardcoding configuration into the image, we passed environment variables when starting the container.

```bash
docker run \
-e DATABASE_HOST=postgres \
-e LOG_LEVEL=INFO \
my-app
```

Or by using a `.env` file.

The important idea was:

> **The Docker image stays the same. Only the configuration changes.**

---

# ☸️ How Kubernetes Solves It

Kubernetes follows the same principle.

Instead of passing environment variables every time we start a container, Kubernetes stores configuration in a dedicated object called a **ConfigMap**.

Applications can then read that configuration when they start.

```text
          ConfigMap
               │
               ▼
         Deployment
               │
               ▼
             Pods
```

This allows the same container image to be deployed to development, staging, and production using different configuration.

---

# 📄 ConfigMap Configuration

`configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap

metadata:
  name: app-config

data:
  APP_NAME: Docker Kubernetes Playbook
  ENVIRONMENT: Development
  LOG_LEVEL: INFO
```

The `data` section contains simple key-value pairs that our application can use.

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

          envFrom:
            - configMapRef:
                name: app-config
```

The new section is:

```yaml
envFrom:
  - configMapRef:
      name: app-config
```

This tells Kubernetes:

> Load every key-value pair from the `app-config` ConfigMap and expose them as environment variables inside the container.

---

# 📝 YAML Breakdown

## kind

```yaml
kind: ConfigMap
```

Creates a Kubernetes ConfigMap resource that stores application configuration.

---

## data

```yaml
data:
  LOG_LEVEL: INFO
```

Contains the configuration values.

Each key becomes an environment variable inside the container.

---

## envFrom

```yaml
envFrom:
  - configMapRef:
      name: app-config
```

References an existing ConfigMap.

When the Pod starts, Kubernetes injects those values as environment variables.

---

# 🚀 Create the Resources

Create the ConfigMap:

```bash
kubectl apply -f configmap.yaml
```

Deploy the application:

```bash
kubectl apply -f deployment.yaml
```

---

# 🔍 Verify the ConfigMap

List ConfigMaps:

```bash
kubectl get configmaps
```

Describe the ConfigMap:

```bash
kubectl describe configmap app-config
```

---

# 🔍 Verify the Environment Variables

Find a Pod:

```bash
kubectl get pods
```

Open a shell inside one of them:

```bash
kubectl exec -it <pod-name> -- sh
```

Display all environment variables:

```bash
env
```

Since the container also contains many system environment variables, it's often easier to filter the ones we added.

```bash
env | grep APP
env | grep ENVIRONMENT
env | grep LOG
```

Example output:

```text
APP_NAME=Docker Kubernetes Playbook
ENVIRONMENT=Development
LOG_LEVEL=INFO
```

These values were injected into the container directly from the ConfigMap.

---

# 🧠 Mental Model

Think of a ConfigMap as a configuration file managed by Kubernetes.

Instead of storing configuration inside your application image, you store it separately.

```text
Docker Image
      │
Application Code
      │
      ▼
Deployment
      │
      ▼
Reads Configuration
      │
      ▼
ConfigMap
```

The same Docker image can now be deployed to multiple environments simply by using different ConfigMaps.

---

# 🎯 Key Takeaways

After completing this module, we understand:

* Configuration should be separated from application code.
* Docker passes configuration using environment variables.
* Kubernetes stores configuration in ConfigMaps.
* A ConfigMap contains key-value pairs.
* Deployments can reference ConfigMaps using `envFrom`.
* The same container image can be reused across different environments by changing only the ConfigMap.

In the next module, we'll learn about **Secrets**, which are designed for storing sensitive configuration such as passwords, API keys, and access tokens.
