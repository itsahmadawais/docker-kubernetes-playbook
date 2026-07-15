# 📦 21 — StatefulSets

## 🎯 Goal

In the previous module, we learned how **Persistent Volumes** allow data to survive Pod recreation.

However, some applications require more than persistent storage.

Distributed systems such as PostgreSQL clusters, MongoDB replica sets, Kafka, and ZooKeeper require each Pod to have a **stable identity**.

A Pod named `database-0` shouldn't suddenly become `database-x7h9k` after being recreated.

To solve this problem, Kubernetes provides **StatefulSets**.

In this module, we'll compare Deployments and StatefulSets to understand when StatefulSets should be used and why stable identities matter.

---

# 📁 Project Structure

```text
21-statefulsets/
│
├── deployment.yaml
├── service.yaml
├── statefulset.yaml
└── README.md
```

---

# 🧠 Why Deployments Aren't Enough

Deployments are designed for **stateless applications**.

Examples include:

* FastAPI
* Django
* Spring Boot
* Node.js
* React
* Nginx

These applications don't care which Pod serves a request.

Consider a Deployment with three Pods.

```text
nginx-deployment-7d8cb7dc8-abc12
nginx-deployment-7d8cb7dc8-def34
nginx-deployment-7d8cb7dc8-ghi56
```

Delete one Pod.

Kubernetes creates another Pod to maintain the desired number of replicas.

```text
nginx-deployment-7d8cb7dc8-xyz89
```

Notice that the replacement Pod has a completely new identity.

For stateless applications, this behavior is perfectly acceptable.

---

# 🧠 Why StatefulSets Exist

Some applications require each Pod to keep its own identity.

Examples include:

* PostgreSQL clusters
* MySQL replication
* MongoDB replica sets
* Kafka
* ZooKeeper
* Elasticsearch

These systems depend on stable Pod names because every instance has a specific role within the cluster.

Instead of creating anonymous Pods, StatefulSets create Pods with predictable names.

```text
nginx-0
nginx-1
nginx-2
```

If `nginx-1` is deleted, Kubernetes recreates:

```text
nginx-1
```

instead of creating a randomly named Pod.

---

# 🧠 Deployment vs StatefulSet

| Deployment                                      | StatefulSet                                    |
| ----------------------------------------------- | ---------------------------------------------- |
| Designed for stateless applications             | Designed for stateful applications             |
| Pods are interchangeable                        | Every Pod has its own identity                 |
| Random Pod names                                | Stable Pod names                               |
| Suitable for web APIs and frontend applications | Suitable for databases and distributed systems |
| Creates a ReplicaSet                            | Manages Pods directly                          |

---

# 🧠 Stable Identity

The biggest advantage of StatefulSets is that every Pod has a permanent identity.

```text
nginx-0

nginx-1

nginx-2
```

Deleting a Pod doesn't change its identity.

```text
Delete nginx-1

↓

Kubernetes creates nginx-1
```

This predictable naming allows distributed systems to reliably communicate with one another.

---

# 🧠 Ordered Deployment

Deployments create Pods whenever resources are available.

StatefulSets create Pods in order.

```text
nginx-0

↓

nginx-1

↓

nginx-2
```

Likewise, Pods are terminated in reverse order.

```text
nginx-2

↓

nginx-1

↓

nginx-0
```

This ordered behavior is important for many distributed applications.

---

# 🧠 Headless Service

Unlike Deployments, StatefulSets require a **Headless Service**.

```yaml
clusterIP: None
```

Instead of load balancing requests, a Headless Service gives every Pod a stable network identity.

For example:

```text
nginx-0.nginx

nginx-1.nginx

nginx-2.nginx
```

This allows Pods to consistently communicate with one another.

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

# 📄 Headless Service

`service.yaml`

```yaml
apiVersion: v1
kind: Service

metadata:
  name: nginx

spec:
  clusterIP: None

  selector:
    app: nginx

  ports:
    - port: 80
      targetPort: 80
```

---

# 📄 StatefulSet Configuration

`statefulset.yaml`

```yaml
apiVersion: apps/v1
kind: StatefulSet

metadata:
  name: nginx

spec:
  serviceName: nginx

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

# 📝 YAML Breakdown

## serviceName

```yaml
serviceName: nginx
```

Associates the StatefulSet with its Headless Service.

This allows every Pod to receive a stable DNS name.

---

## replicas

```yaml
replicas: 3
```

Creates three Pods.

Unlike a Deployment, every Pod receives its own predictable identity.

---

## Headless Service

```yaml
clusterIP: None
```

Disables load balancing and enables stable DNS names for each Pod.

---

# 🚀 Deploy the Deployment

```bash
kubectl apply -f deployment.yaml
```

View the Pods.

```bash
kubectl get pods
```

Example output:

```text
nginx-deployment-7d8cb7dc8-abc12
nginx-deployment-7d8cb7dc8-def34
nginx-deployment-7d8cb7dc8-ghi56
```

Delete one Pod.

```bash
kubectl delete pod <pod-name>
```

A replacement Pod is automatically created with a different random name.

---

# 🚀 Remove the Deployment

```bash
kubectl delete deployment nginx-deployment
```

---

# 🚀 Deploy the StatefulSet

```bash
kubectl apply -f service.yaml

kubectl apply -f statefulset.yaml
```

View the Pods.

```bash
kubectl get pods
```

Example output:

```text
nginx-0
nginx-1
nginx-2
```

Notice that every Pod has a predictable name.

---

# 🔍 Delete a Pod

Delete:

```bash
kubectl delete pod nginx-1
```

Watch the Pods.

```bash
kubectl get pods -w
```

Example output:

```text
nginx-1   Terminating

↓

nginx-1   ContainerCreating

↓

nginx-1   Running
```

Notice that Kubernetes recreated **`nginx-1`**, preserving its identity.

---

# 🔍 Ordered Scaling

Increase the number of replicas.

```bash
kubectl scale statefulset nginx --replicas=5
```

Observe the Pods.

```text
nginx-0
nginx-1
nginx-2
nginx-3
nginx-4
```

Now scale the StatefulSet back down.

```bash
kubectl scale statefulset nginx --replicas=2
```

Notice that Pods are removed in reverse order.

```text
nginx-4

↓

nginx-3

↓

nginx-2
```

This ordered behavior is unique to StatefulSets.

---

# 🧠 Mental Model

Think of the two controllers like this.

**Deployment**

```text
Pod A

Pod B

Pod C

All Pods are identical.
```

**StatefulSet**

```text
nginx-0

nginx-1

nginx-2

Every Pod has its own identity.
```

---

# 🎯 Key Takeaways

After completing this module, we understand:

* Deployments and StatefulSets are different Kubernetes workload controllers.
* Deployments are designed for stateless applications.
* StatefulSets are designed for stateful applications.
* StatefulSets provide stable Pod names and identities.
* StatefulSets recreate Pods with the same identity.
* StatefulSets create Pods in order and terminate them in reverse order.
* StatefulSets require a Headless Service to provide stable network identities.
* Most web applications use Deployments, while databases and distributed systems commonly use StatefulSets.

In the next module, we'll explore **Jobs and CronJobs**, which are designed to run tasks that execute once or on a schedule.
