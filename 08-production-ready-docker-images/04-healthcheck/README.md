# 🧩 04 — Health Checks

## 🎯 Goal

Understand how Docker determines whether an application inside a container is healthy, not just running.

---

## 📁 Files

* `app/main.py`
* `app/requirements.txt`
* `Dockerfile`

---

## 🧠 The Problem

When a container starts, Docker only knows whether its main process is running.

For example, your web server may still be running, but the application itself could be unresponsive due to an internal error.

Without a health check, Docker reports the container as:

```text
Up 30 seconds
```

even if the application is no longer responding to requests.

---

## 💡 The Solution

Docker provides the `HEALTHCHECK` instruction.

It periodically executes a command inside the container to verify that the application is responding correctly.

If the command succeeds, Docker marks the container as:

```text
healthy
```

If the command continues to fail, Docker marks the container as:

```text
unhealthy
```

---

## 🧠 Understanding `HEALTHCHECK`

Our Dockerfile contains the following instruction:

```dockerfile
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"
```

Let's understand each part.

---

### `--interval=30s`

Runs the health check every **30 seconds**.

```text
0s ───► 30s ───► 60s ───► 90s
          ▲         ▲         ▲
      Health     Health    Health
       Check      Check     Check
```

---

### `--timeout=5s`

Docker waits up to **5 seconds** for the health check command to complete.

If the command does not finish within 5 seconds, that health check is considered a failure.

---

### `--retries=3`

Docker does not mark the container as unhealthy after a single failed check.

Instead, it waits for **three consecutive failures** before changing the container status to:

```text
unhealthy
```

This helps prevent temporary network delays or startup latency from incorrectly marking the container as unhealthy.

---

### `CMD`

This is the command Docker executes during every health check.

```dockerfile
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"
```

The command sends an HTTP request to:

```text
http://localhost:8000/
```

Here, `localhost` refers to the **container itself**, not your local machine.

If the application responds successfully, Docker considers the container healthy.

---

## ▶️ Build the Image

Build the Docker image:

```bash
docker build -t health-demo .
```

Here:

* `health-demo` is the image name.

---

## ▶️ Run the Container

Create and start a container from the image:

```bash
docker run -d -p 8000:8000 --name health-api health-demo
```

Command breakdown:

* `-d` → Run the container in detached mode.
* `-p 8000:8000` → Map port **8000** on your machine to port **8000** inside the container.
* `--name health-api` → Assign the container the name `health-api`.
* `health-demo` → Create the container from the `health-demo` image.

> **Note:** The port mapping is not required for the health check itself. The health check runs inside the container. We expose the port so we can access the application from our browser.

---

## 🔍 Verify

Check the running container:

```bash
docker ps
```

After a few moments, you'll see something similar to:

```text
CONTAINER ID   IMAGE         STATUS
a1b2c3d4e5f6   health-demo   Up 30 seconds (healthy)
```

The `(healthy)` status indicates that Docker's health check is succeeding.

---

## 🎯 Why Use Health Checks?

Health checks allow Docker to determine whether:

* The application is accepting requests
* The application is functioning correctly
* The container should be considered healthy

This becomes especially important in production environments where container orchestration platforms monitor application health and take action when services become unhealthy.

---

## 🎯 Key Takeaway

A running container does not always mean a healthy application.

The `HEALTHCHECK` instruction allows Docker to periodically verify that the application is responding correctly and accurately report its health status.
