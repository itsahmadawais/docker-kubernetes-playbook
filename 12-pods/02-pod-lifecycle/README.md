# 🧩 02 — Pod Lifecycle

## 🎯 Goal

In the Docker modules, we learned an important concept:

> **A container lives only while its main process is running.**

For example:

```bash
docker run nginx
```

The nginx server keeps running, so the container stays alive.

```text
Container
     │
     ▼
nginx process
     │
     ▼
Container keeps running
```

Now consider another example:

```bash
docker run busybox echo "Hello Docker"
```

Output:

```text
Hello Docker
```

Once the command finishes, the main process exits and Docker stops the container.

This behavior doesn't change in Kubernetes.

A Pod still runs one or more containers, so the Pod's lifecycle depends on what happens inside those containers.

The difference is that Kubernetes continuously watches the Pod and decides whether it should restart the container or report an error.

In this module, we'll intentionally create different scenarios and observe how Kubernetes responds.

---

# 📁 Project Structure

```text
02-pod-lifecycle/
│
├── pod-running.yaml
├── pod-completed.yaml
├── pod-image-pull-error.yaml
└── README.md
```

---

# 🧠 From Docker to Kubernetes

In Docker, we manually start a container:

```text
Docker Image
      │
      ▼
 Docker Container
```

In Kubernetes, we create a Pod that contains the container.

```text
Pod
 │
 └── Container
       │
       └── Main Process
```

The Pod's state is determined by what happens to the container's main process.

---

# 🚀 Experiment 1 — Long Running Application

Create the nginx Pod:

```bash
kubectl apply -f pod-running.yaml
```

Watch it:

```bash
kubectl get pods -w
```

Example:

```text
NAME        READY   STATUS              RESTARTS   AGE
nginx-pod   0/1     ContainerCreating   0          2s
nginx-pod   1/1     Running             0          5s
```

## What happened?

Just like Docker, nginx is a web server that continuously waits for incoming requests.

Since its main process never exits, Kubernetes keeps the Pod in the **Running** state.

```text
Pod

└── nginx

      │
      ▼

Waiting for requests...

      │
      ▼

Running
```

---

# 🚀 Experiment 2 — Completed Pod

Create the BusyBox Pod:

```bash
kubectl apply -f pod-completed.yaml
```

Check the status:

```bash
kubectl get pods
```

Example:

```text
NAME          READY   STATUS      RESTARTS   AGE
busybox-pod   0/1     Completed   0          5s
```

## What happened?

The container executes:

```text
echo "Hello Kubernetes"
```

prints the message and exits successfully.

This is exactly the same behavior we observed in Docker.

The difference is that we configured:

```yaml
restartPolicy: Never
```

so Kubernetes knows this is expected and does not restart the container.

This pattern is commonly used for:

* Database migrations
* Data imports
* Backups
* Report generation
* One-time scripts

---

# 🚀 Experiment 3 — Image Pull Failure

Create the Pod:

```bash
kubectl apply -f pod-image-pull-error.yaml
```

Check the status:

```bash
kubectl get pods
```

Example:

```text
NAME        READY   STATUS         RESTARTS   AGE
nginx-pod   0/1     ErrImagePull   0          4s
```

A few seconds later:

```text
ImagePullBackOff
```

Inspect the Pod:

```bash
kubectl describe pod nginx-pod
```

## What happened?

Just like Docker, Kubernetes needs the correct image name and tag.

When Kubernetes asks the container runtime to download:

```text
nginx:this-image-does-not-exist
```

the registry replies:

> Image not found.

Kubernetes retries several times before waiting longer between attempts.

This is why the status changes from:

```text
ErrImagePull
```

to

```text
ImagePullBackOff
```

---

# 🧪 Bonus Experiment — CrashLoopBackOff

Open `pod-completed.yaml`.

Replace:

```yaml
command:
  - echo
  - Hello Kubernetes
```

with:

```yaml
command:
  - sh
  - -c
  - exit 1
```

Delete the old Pod:

```bash
kubectl delete pod busybox-pod
```

Create it again:

```bash
kubectl apply -f pod-completed.yaml
```

Watch:

```bash
kubectl get pods -w
```

Eventually you'll see:

```text
CrashLoopBackOff
```

## What happened?

In Docker, when an application crashes, the container simply stops.

Kubernetes behaves differently.

By default, every Pod uses:

```yaml
restartPolicy: Always
```

Kubernetes assumes your application should always be running.

When the container exits with an error, Kubernetes restarts it.

If it keeps failing, Kubernetes waits longer between restart attempts.

This behavior is reported as:

```text
CrashLoopBackOff
```

---

# 🔍 Inspect a Pod

Whenever a Pod doesn't behave as expected, inspect it:

```bash
kubectl describe pod <pod-name>
```

This command shows:

* Scheduling information
* Container state
* Events
* Restart history
* Image pull errors
* Failure reasons

It is one of the most useful debugging commands in Kubernetes.

---

# 🧠 Pod Lifecycle

During these experiments, we observed how a Pod moves through different states.

```text
                  kubectl apply
                        │
                        ▼
                    Pending
                        │
                        ▼
               ContainerCreating
                        │
                        ▼
                     Running
                ┌───────┼─────────┐
                │       │         │
                ▼       ▼         ▼
          Completed  CrashLoop  Terminating
                         │
                         ▼
                 CrashLoopBackOff

Or, if the image cannot be downloaded:

Pending
   │
   ▼
ErrImagePull
   │
   ▼
ImagePullBackOff
```

The important idea is that Kubernetes continuously observes the Pod and reacts based on what happens to the application's main process.

---

# 🎯 Key Takeaways

After completing this module, you understand:

* Containers behave the same way in Kubernetes as they do in Docker.
* A Pod's lifecycle depends on the lifecycle of its containers.
* Long-running applications remain in the **Running** state.
* One-time tasks finish with the **Completed** state.
* Invalid image names lead to **ErrImagePull** and **ImagePullBackOff**.
* Applications that repeatedly fail enter **CrashLoopBackOff**.
* `restartPolicy` determines whether Kubernetes should restart a finished container.
* `kubectl describe pod` is one of the most important commands for troubleshooting Pods.

In the next module, we'll learn why a Pod can contain multiple containers and when that design is useful.
