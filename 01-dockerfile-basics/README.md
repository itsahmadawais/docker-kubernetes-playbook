# 01 - Dockerfile Basics

## Objective

The goal of this exercise is to understand the fundamental concepts behind Docker images, containers, and Dockerfiles by containerizing a simple Python application.

Instead of memorizing Docker commands, this task focuses on building a mental model of how Docker works.

---

## Project Structure

```text
01-dockerfile-basics/
├── app.py
├── Dockerfile
└── README.md
```

---

## Application

**app.py**

```python
print("Hello from Docker!")
```

---

## Dockerfile

```dockerfile
FROM python:3.14

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

---

## Dockerfile Breakdown

### `FROM python:3.14`

Uses the official Python 3.14 image as the base image.

Docker builds our image on top of this existing image instead of installing Python from scratch.

---

### `WORKDIR /app`

Sets `/app` as the working directory inside the image.

If the directory does not exist, Docker creates it automatically.

All subsequent relative paths are resolved from this directory.

---

### `COPY app.py .`

Copies `app.py` from the **build context** (our local project directory) into the current working directory inside the image (`/app`).

This demonstrates that the left side of `COPY` is the source on the host, while the right side is the destination inside the image.

---

### `CMD ["python", "app.py"]`

Defines the default command executed when a container starts.

It is **not executed during image build**. Instead, Docker stores it as metadata and runs it only when a container is created from the image.

---

## Build the Image

```bash
docker build -t hello-python .
```

### Command Breakdown

* `docker build` → Builds a Docker image.
* `-t hello-python` → Tags the image as `hello-python:latest`.
* `.` → Uses the current directory as the build context.

---

## Run the Container

```bash
docker run hello-python
```

Expected output:

```text
Hello from Docker!
```

---

## Key Concepts Learned

### Image vs Container

An **image** is an immutable blueprint.

A **container** is a running instance of an image.

Multiple containers can be created from the same image.

---

### Build Context

When running:

```bash
docker build .
```

Docker sends the current directory to the Docker Engine as the build context.

The Dockerfile can only access files inside this build context.

---

### Image Layers

Each Dockerfile instruction creates a new image layer.

Docker caches these layers, allowing future builds to reuse unchanged layers and significantly reduce build times.

---

### Working Directory

`WORKDIR` behaves similarly to running `cd` in Linux.

Relative paths used by `COPY`, `RUN`, `CMD`, and other instructions are resolved from this directory.

---

### Container Lifecycle

A container remains running only while its main process is running.

If the main process exits, the container stops.

This explains why:

```python
print("Hello")
```

causes the container to exit immediately, while an infinite loop keeps it running.

---

### Python Output Buffering

During testing, we observed that Python buffered output inside the container.

For production applications, unbuffered logging is recommended so logs are immediately available through Docker.

Common approaches include:

```dockerfile
ENV PYTHONUNBUFFERED=1
```

or

```dockerfile
CMD ["python", "-u", "app.py"]
```

---

## Production Notes

* Use meaningful image tags instead of relying on `latest`.
* Keep the build context as small as possible.
* Organize application files using `WORKDIR`.
* Write logs to `stdout`/`stderr` instead of log files inside the container.
* Version images to enable reliable rollbacks during deployments.

---

## Summary

After completing this exercise, I understand:

* The difference between images and containers.
* How Docker builds images.
* What a build context is.
* How `FROM`, `WORKDIR`, `COPY`, and `CMD` work.
* Why containers stop when their main process exits.
* Why Python output buffering matters in containerized applications.
* Why image tagging is important for versioning and production rollbacks.

This exercise establishes the foundation for the next topic: understanding `RUN`, image layers, Docker build caching, and writing production-ready Dockerfiles.
