# 📦 25 — Helm

## 🎯 Goal

In previous modules, we deployed Kubernetes applications by manually creating and applying multiple YAML files.

As applications grow, managing dozens of Kubernetes manifests becomes difficult, especially across multiple environments such as development, staging, and production.

Helm solves this problem by allowing us to package Kubernetes resources into reusable **Charts**, making deployments easier to configure, version, upgrade, and share.

In this module, we'll create our first Helm Chart for a FastAPI application and learn the complete Helm workflow.

---

# 📁 Project Structure

```text
25-helm/
│
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── fastapi-chart/
    ├── Chart.yaml
    ├── values.yaml
    ├── .helmignore
    └── templates/
        ├── _helpers.tpl
        ├── deployment.yaml
        ├── service.yaml
        ├── ingress.yaml
        └── hpa.yaml
```

---

# 🧠 Why Helm?

Imagine a production Kubernetes application.

It may contain resources such as:

* Deployment
* Service
* Ingress
* ConfigMap
* Secret
* PersistentVolumeClaim
* Horizontal Pod Autoscaler
* ServiceAccount
* RBAC
* Network Policies

Managing all of these YAML files manually quickly becomes difficult.

Helm allows us to:

* Write templates once
* Configure deployments using values
* Reuse the same chart across multiple environments
* Upgrade applications easily
* Roll back failed deployments
* Package Kubernetes applications for distribution

---

# 🧠 What is a Helm Chart?

A **Chart** is a package containing Kubernetes templates and configuration.

It consists of:

```text
Chart.yaml
values.yaml
templates/
```

A Helm Chart is similar to a reusable application package.

---

---

# ⚙️ Installing Helm

Helm is not included with Kubernetes and must be installed separately.

Follow the official installation guide:

[https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/)

After installation, verify it is available:

```bash
helm version
```

# 🧠 Chart.yaml

`Chart.yaml` contains metadata about the chart.

Example:

```yaml
apiVersion: v2

name: fastapi-chart

description: A Helm chart for deploying a FastAPI application

type: application

version: 0.1.0

appVersion: "1.0.0"
```

---

# 🧠 values.yaml

`values.yaml` stores configuration that can change between environments.

Example:

```yaml
replicaCount: 1

image:
  repository: fastapi-helm
  tag: latest
```

Instead of modifying Kubernetes manifests directly, we simply change values.

---

# 🧠 Templates

The `templates/` directory contains Kubernetes manifests with Helm template syntax.

Example:

Instead of writing:

```yaml
replicas: 3
```

we write:

```yaml
replicas: {{ .Values.replicaCount }}
```

Helm replaces the template using values from `values.yaml`.

---

# 🧠 Helm Rendering

When we install a chart, Helm performs the following steps:

```text
Read Chart

↓

Read values.yaml

↓

Render Templates

↓

Generate Kubernetes YAML

↓

Send YAML to Kubernetes API

↓

Resources Created
```

Kubernetes never receives Helm templates.

It only receives standard Kubernetes manifests.

---

# 🧠 Releases

Every installation of a Helm Chart is called a **Release**.

For example:

```bash
helm install fastapi .
```

creates a release named:

```text
fastapi
```

The same chart can be installed multiple times with different release names and configurations.

---

# 📄 _helpers.tpl

Helper templates reduce duplication.

Instead of repeating names throughout every template, helper functions generate consistent resource names.

---

# 🚀 Build the Docker Image

```bash
docker build -t fastapi-helm ./app
```

---

# 🚀 Validate the Chart

Before installing, validate the chart.

```bash
helm lint .
```

This checks for template errors and chart issues.

---

# 🚀 Render Templates

Generate Kubernetes YAML without deploying anything.

```bash
helm template .
```

This is useful for verifying the rendered manifests.

---

# 🚀 Install the Chart

Install the application into Kubernetes.

```bash
helm install fastapi .
```

Where:

* `fastapi` → Release name
* `.` → Current chart

---

# 🔍 Verify the Installation

List installed releases.

```bash
helm list
```

Verify Kubernetes resources.

```bash
kubectl get all
```

If enabled:

```bash
kubectl get ingress
```

```bash
kubectl get hpa
```

---

# 🌐 Access the Application

Forward the Service.

```bash
kubectl port-forward service/fastapi-fastapi-chart 8000:80
```

Open:

```text
http://localhost:8000
```

---

# 🔄 Upgrade a Release

Modify `values.yaml`.

Example:

```yaml
replicaCount: 3
```

Upgrade the release.

```bash
helm upgrade fastapi .
```

Helm updates only the necessary Kubernetes resources.

---

# 📜 Release History

View previous revisions.

```bash
helm history fastapi
```

Every upgrade creates a new revision.

---

# ⏪ Rollback

Rollback to an earlier revision.

```bash
helm rollback fastapi 1
```

This restores the application to Revision 1.

---

# 🗑️ Uninstall

Remove every resource created by the chart.

```bash
helm uninstall fastapi
```

Verify:

```bash
kubectl get all
```

---

# 📦 Common Helm Commands

Validate chart:

```bash
helm lint .
```

Render templates:

```bash
helm template .
```

Install:

```bash
helm install fastapi .
```

List releases:

```bash
helm list
```

Upgrade:

```bash
helm upgrade fastapi .
```

History:

```bash
helm history fastapi
```

Rollback:

```bash
helm rollback fastapi 1
```

Uninstall:

```bash
helm uninstall fastapi
```
---

# 🎯 Key Takeaways

After completing this module, we understand:

* Helm is the package manager for Kubernetes.
* A Helm Chart packages Kubernetes resources into reusable templates.
* `Chart.yaml` contains chart metadata.
* `values.yaml` stores configurable values.
* Templates generate Kubernetes manifests dynamically.
* Every installation of a chart creates a Helm Release.
* Helm simplifies installing, upgrading, rolling back, and uninstalling applications.
* The `helm template` command allows inspecting generated manifests before deployment.
* The `helm lint` command validates charts before installation.

---

## Next Module

In the next module, we'll learn **Kubernetes Production Best Practices**. We'll explore the techniques and recommendations for deploying secure, reliable, and production-ready applications on Kubernetes.
