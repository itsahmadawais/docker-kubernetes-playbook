# 🧩 01 — First Pod

## 🎯 Goal

In the Docker modules, we learned how to package applications into images and run them as containers.

For example:

```text
Docker Image
      |
      v
Docker Container
```

Docker solved an important problem:

> "How do we package and run applications consistently?"

But when applications grow, running containers manually becomes difficult.

Imagine a production system:

```text
Server

├── API Container
├── Worker Container
├── Payment Container
├── Notification Container
└── Database Container
```

Now we need answers to new questions:

* What happens if a container crashes?
* How do we run multiple copies of our application?
* Which server should run each container?
* How do we update applications without downtime?

This is where Kubernetes comes in.

---

# 🧠 From Docker Containers to Kubernetes Pods

Docker manages containers.

Kubernetes manages containerized applications.

However, Kubernetes does not directly create containers.

Instead, Kubernetes works with a higher-level concept called a **Pod**.

```text
Kubernetes

     |
     v

    Pod

     |
     v

 Container
```

A Pod is the smallest unit Kubernetes deploys and manages.

---

# 🧩 What is a Pod?

A Pod is a wrapper around one or more containers.

For most backend applications, a Pod contains one main application container.

Example:

```text
Pod

└── FastAPI Container
```

Or:

```text
Pod

└── Nginx Container
```

The Pod provides the environment where the container runs.

Kubernetes manages the Pod lifecycle instead of directly managing the container.

---

# 📁 Project Structure

```text
01-first-pod/
  │
  ├── pod.yaml
  └── README.md
```

---

# 📄 Our First Kubernetes Configuration

We will create a simple Nginx Pod.

`pod.yaml`

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: nginx-pod

spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80
```

This configuration tells Kubernetes:

> "Create a Pod named nginx-pod and run the nginx container inside it."

---

# YAML Breakdown

## apiVersion

```yaml
apiVersion: v1
```

Defines which Kubernetes API version should handle this resource.

Pods use the core Kubernetes API:

```text
v1
```

---

## kind

```yaml
kind: Pod
```

Defines the type of resource we want Kubernetes to create.

Here:

```text
Create a Pod
```

Other Kubernetes resources include:

```text
Deployment
Service
ConfigMap
Secret
```

---

## metadata

```yaml
metadata:
  name: nginx-pod
```

Contains information about the resource.

Here we define the Pod name:

```text
nginx-pod
```

---

## spec

```yaml
spec:
```

Defines the desired state.

It describes what we want Kubernetes to create.

---

## containers

```yaml
containers:
  - name: nginx
    image: nginx:latest
```

Defines the container that should run inside the Pod.

Kubernetes will:

1. Find a suitable node.
2. Schedule the Pod.
3. Ask kubelet to start the container.
4. Pull the image if needed.
5. Run the application.

---

# 🚀 Create the Pod

Apply the configuration:

```bash
kubectl apply -f pod.yaml
```

Output:

```text
pod/nginx-pod created
```

Kubernetes now tries to make the cluster match our desired state.

---

# 🔍 Verify the Pod

Check running Pods:

```bash
kubectl get pods
```

Example:

```text
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          20s
```

The Pod is now running.

---

# 🔎 Inspect What Kubernetes Created

To understand what happened:

```bash
kubectl describe pod nginx-pod
```

This shows:

* Which node runs the Pod.
* Container details.
* Image information.
* Events.
* Errors.

This command becomes extremely important when debugging Kubernetes applications.

---

# 🌐 Access the Application

The Pod is running inside the Kubernetes network.

It is not directly accessible from your browser.

For testing, we create a temporary connection:

```bash
kubectl port-forward pod/nginx-pod 8080:80
```

Traffic flow:

```text
Browser

localhost:8080

      |
      v

kubectl port-forward

      |
      v

nginx Pod

Container Port: 80
```

Open:

```text
http://localhost:8080
```

You should see the nginx welcome page.

---

# 🗑️ Delete the Pod

Remove the Pod:

```bash
kubectl delete pod nginx-pod
```

Kubernetes removes the resource.

---

# 🎯 Key Takeaways

After this module, we understand:

* A Pod is Kubernetes' smallest deployable unit.
* Kubernetes YAML describes the desired state.
* `kubectl apply` creates Kubernetes resources.
* A Pod runs one or more containers.
* Pods are internal and need networking components for production access.

Next, we will explore the **Pod lifecycle** and understand how Kubernetes handles container failures and restarts.
