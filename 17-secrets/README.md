# 📦 17 — Secrets

## 🎯 Goal

In the previous module, we learned how to use **ConfigMaps** to separate configuration from our application.

For example, values such as:

```text
APP_NAME=Docker Kubernetes Playbook
LOG_LEVEL=INFO
DATABASE_HOST=postgres
```

don't belong inside our Docker image because they can change between environments.

However, not all configuration is safe to expose.

Consider the following values:

```text
DATABASE_PASSWORD=myPassword123
JWT_SECRET=...
API_KEY=...
```

These are sensitive and should be handled differently.

This is the problem that **Secrets** solve.

---

# 📁 Project Structure

```text
17-secrets/
│
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
└── README.md
```

---

# 🧠 Why Not Store Everything in a ConfigMap?

Technically, Kubernetes allows you to store passwords inside a ConfigMap.

However, this is not recommended.

Configuration generally falls into two categories:

**Non-sensitive configuration**

* Application name
* Log level
* Feature flags
* Database host
* Environment

**Sensitive configuration**

* Database passwords
* API keys
* Access tokens
* JWT secrets
* Certificates

Kubernetes separates these into two different resources:

```text
Application Configuration
        │
        ├──────────────┐
        ▼              ▼
   ConfigMap         Secret
```

This makes the intent clear and allows production environments to apply different security policies to Secrets.

---

# 🧠 ConfigMaps vs Secrets

From the application's perspective, there is almost no difference.

The application simply reads environment variables.

```python
os.getenv("DATABASE_HOST")
os.getenv("DATABASE_PASSWORD")
```

It doesn't know whether the values came from a ConfigMap or a Secret.

The separation exists for developers, operators, and production infrastructure.

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
  LOG_LEVEL: INFO
  DATABASE_HOST: postgres
```

---

# 📄 Secret Configuration

`secret.yaml`

```yaml
apiVersion: v1
kind: Secret

metadata:
  name: app-secret

type: Opaque

stringData:
  DATABASE_PASSWORD: mypassword123
  API_KEY: abc123
```

The important additions are:

```yaml
kind: Secret
type: Opaque
```

and

```yaml
stringData:
```

`stringData` allows us to provide plain text values.

Kubernetes automatically converts them into the format it stores internally.

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

            - secretRef:
                name: app-secret
```

Notice that the Deployment can consume both ConfigMaps and Secrets simultaneously.

Inside the container, all values become environment variables.

---

# 🚀 Create the Resources

Create the ConfigMap:

```bash
kubectl apply -f configmap.yaml
```

Create the Secret:

```bash
kubectl apply -f secret.yaml
```

Deploy the application:

```bash
kubectl apply -f deployment.yaml
```

---

# 🔍 Verify the Resources

List ConfigMaps:

```bash
kubectl get configmaps
```

List Secrets:

```bash
kubectl get secrets
```

Describe the Secret:

```bash
kubectl describe secret app-secret
```

Notice that Kubernetes does not display the actual values.

Instead, you'll see something similar to:

```text
Data
====
API_KEY:              6 bytes
DATABASE_PASSWORD:   13 bytes
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

Display the environment variables:

```bash
env
```

Since the container contains many system environment variables, it's easier to filter the ones we added.

```bash
env | grep APP
env | grep LOG
env | grep DATABASE
env | grep API
```

Example output:

```text
APP_NAME=Docker Kubernetes Playbook
LOG_LEVEL=INFO
DATABASE_HOST=postgres
DATABASE_PASSWORD=mypassword123
API_KEY=abc123
```

Notice that the application receives values from both the ConfigMap and the Secret in exactly the same way.

---

# 🧠 Are Secrets Encrypted?

A common misconception is that Kubernetes Secrets are encrypted.

By default, they are **Base64 encoded**, not encrypted.

You can verify this yourself.

```bash
kubectl get secret app-secret -o yaml
```

You'll see output similar to:

```yaml
data:
  API_KEY: YWJjMTIz
  DATABASE_PASSWORD: bXlwYXNzd29yZDEyMw==
```

Production Kubernetes clusters typically enable encryption at rest and use access controls to better protect Secrets.

---

# 🧠 Mental Model

Think of ConfigMaps and Secrets as two containers for different kinds of configuration.

```text
                    Deployment
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     ConfigMap                     Secret
 (Non-sensitive)               (Sensitive)
          │                             │
          └──────────────┬──────────────┘
                         ▼
                        Pod
```

The application simply reads environment variables, while Kubernetes manages where those values come from.

---

# 🎯 Key Takeaways

After completing this module, we understand:

* ConfigMaps store non-sensitive configuration.
* Secrets store sensitive configuration.
* Deployments can consume ConfigMaps and Secrets at the same time.
* The application accesses both in exactly the same way.
* Kubernetes hides Secret values when describing the resource.
* By default, Kubernetes Secrets are Base64 encoded, not encrypted.

In the next module, we'll learn about **Resource Requests and Limits**, which allow Kubernetes to allocate CPU and memory efficiently while protecting applications from resource contention.
