# 📦 01 - Dockerfile Basics

## Objective

The objective of this exercise is to understand the fundamentals of Docker by containerizing a simple Python application.

Rather than memorizing commands, this task focuses on building a strong mental model of how Docker images, containers, Dockerfiles, image tags, and the build process work together.

---

## Project Structure

```text
01-dockerfile-basics/
├── app.py
├── Dockerfile
└── README.md
```

---

# Experiments

To understand how Docker containers behave, two Python applications were tested.

## Experiment 1 - Short-Lived Process

```python
print("Hello from Docker!")
```

### Observation

* The application printed `Hello from Docker!`.
* The Python process exited immediately.
* Since the main process completed, Docker automatically stopped the container.

This demonstrates an important Docker concept:

> A container remains alive only while its primary process is running.

---

## Experiment 2 - Long-Running Process

```python
import time

while True:
    print("Hello from Docker!")
    time.sleep(5)
```

### Expected Behavior

Since the Python process never exits, the container should continue running indefinitely.

### Observation

Initially, no output appeared while the container was running.

Once the container was stopped, all log messages appeared at once.

This behavior was caused by **Python output buffering**, not Docker.

Python buffers stdout when it detects that it is running in a non-interactive environment.

### Production Solutions

Disable output buffering using one of the following approaches.

Using an environment variable:

```dockerfile
ENV PYTHONUNBUFFERED=1
```

Using Python's unbuffered mode:

```dockerfile
CMD ["python", "-u", "app.py"]
```

Or flushing every print statement:

```python
print("Hello from Docker!", flush=True)
```

Using unbuffered logging is considered a best practice because Docker, Kubernetes, and cloud logging systems collect application logs from **stdout** and **stderr**.

---

# Dockerfile

```dockerfile
FROM python:3.14

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

---

# Dockerfile Breakdown

## `FROM python:3.14`

Uses the official Python 3.14 image as the base image.

Instead of installing Python manually, Docker builds the image on top of an existing Python image.

---

## `WORKDIR /app`

Sets `/app` as the current working directory inside the image.

If the directory does not already exist, Docker creates it automatically.

All relative paths used by subsequent Dockerfile instructions are resolved from this directory.

---

## `COPY app.py .`

Copies `app.py` from the **build context** into the current working directory (`/app`) inside the image.

Important concept:

* Left side → Source from the build context.
* Right side → Destination inside the image.

Example:

```dockerfile
COPY app.py .
```

Results in:

```text
/app/app.py
```

---

## `CMD ["python", "app.py"]`

Defines the default command executed when a container starts.

`CMD` is **not executed during image build**.

Instead, Docker stores it as metadata and executes it whenever a container is created from the image.

---

# Building the Image

```bash
docker build -t hello-python .
```

## Command Breakdown

### `docker build`

Builds a Docker image from a Dockerfile.

---

### `-t`

`-t` stands for **tag**.

It assigns a human-readable name to the image.

Images follow this format:

```text
<image-name>:<tag>
```

Examples:

```text
hello-python:latest
hello-python:v1
hello-python:v2
hello-python:1.0.0
```

If no tag is specified, Docker automatically uses the `latest` tag.

Therefore, these commands are equivalent:

```bash
docker build -t hello-python .
```

```bash
docker build -t hello-python:latest .
```

Using versioned tags is recommended for production because they support reproducible deployments and safe rollbacks.

---

### `.` (Build Context)

The final argument specifies the **build context**.

Docker sends every file inside the build context to the Docker Engine before the image build begins.

The Dockerfile can only access files that are inside the build context.

---

## Using a Different Dockerfile

By default, Docker searches for a file named:

```text
Dockerfile
```

If your Dockerfile has a different name or is located elsewhere, specify it using the `-f` option.

Example:

```bash
docker build -t hello-python:v1 -f Dockerfile.dev .
```

or

```bash
docker build -t backend:v1 -f backend/Dockerfile backend/
```

Here:

* `-f` specifies which Dockerfile should be used.
* The last argument specifies the build context.

These are independent of each other.

---

# Running the Container

```bash
docker run hello-python
```

For **Experiment 1**, the output is:

```text
Hello from Docker!
```

The container exits immediately because the Python process finishes.

For **Experiment 2**, the container continues running because the main Python process never exits.

---

# Key Concepts Learned

## Images vs Containers

An **image** is an immutable blueprint.

A **container** is a running instance of that image.

Multiple containers can be created from a single image.

Deleting a container does not delete the image.

---

## Build Context

Running:

```bash
docker build .
```

does **not** mean "find the Dockerfile in the current directory."

Instead, it means:

> Use the current directory as the build context.

Docker sends the build context to the Docker Engine, and the Dockerfile can only access files contained within it.

---

## Image Layers

Each Dockerfile instruction creates a new image layer.

Docker caches these layers to improve build performance.

If a layer has not changed, Docker reuses it instead of rebuilding it.

This is why ordering Dockerfile instructions correctly can significantly reduce build times.

---

## Working Directory

`WORKDIR` behaves similarly to the Linux `cd` command.

Example:

```dockerfile
WORKDIR /app
WORKDIR src
```

Results in:

```text
/app/src
```

Relative paths are resolved from the current working directory.

---

## Container Lifecycle

A container remains running only while its primary process is running.

If the main process exits, Docker stops the container.

This explains why:

```python
print("Hello")
```

stops immediately, while:

```python
while True:
    ...
```

keeps the container alive.

---

## Python Output Buffering

Python buffers standard output when running in a non-interactive environment.

For production applications, unbuffered output is recommended so logs appear immediately in Docker and orchestration platforms.

---

## Image Tags

Image tags are lightweight labels used to identify different versions of an image.

Examples:

```text
hello-python:v1
hello-python:v2
hello-python:latest
```

Using versioned tags allows applications to be rolled back quickly without rebuilding images.

---

# Production Notes

* Use a dedicated `WORKDIR` instead of relying on the base image's default directory.
* Keep the build context as small as possible.
* Version Docker images instead of relying on the `latest` tag.
* Treat Docker images as immutable artifacts.
* Write logs to `stdout` and `stderr` rather than files inside the container.
* Enable unbuffered logging for Python applications.
* Organize Dockerfile instructions to maximize Docker's build cache.

---

# Summary

After completing this exercise, you should understand:


* The difference between Docker images and containers.
* How Docker builds an image.
* What a build context is and why it matters.
* How `FROM`, `WORKDIR`, `COPY`, and `CMD` work.
* How Docker image tags are used for versioning.
* Why containers stop when their main process exits.
* Why Python output buffering affects Docker logs.
* Why versioned image tags simplify production deployments and rollbacks.

This exercise establishes the foundation for the next topic: understanding `RUN`, Docker image layers, build caching, and writing production-ready Dockerfiles.
