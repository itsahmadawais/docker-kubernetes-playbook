# 📦 02 - RUN vs Layers & Docker Build Cache

## Objective

The goal of this exercise is to understand how Docker executes `RUN` instructions during image build, how image layers are created, and how Docker build cache improves performance.

This module focuses on one of the most important Docker concepts used in production: **layer caching and build optimization**.

---

## Dockerfile Used

```dockerfile id="dockerfile1"
FROM python:3.14

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

---

## Application

```python id="app1"
print("Hello from Docker + RUN lesson")
```

---

## Key Concepts Learned

---

### 1. RUN Executes During Image Build

`RUN` instructions are executed **while the image is being built**, not when the container starts.

Example:

```dockerfile id="run1"
RUN apt-get update
RUN apt-get install -y curl
```

These commands:

* Modify the image filesystem
* Create new image layers
* Do NOT run when `docker run` is executed

---

### 2. Image Layers

Each Dockerfile instruction creates a **layer** in the final image.

Conceptually:

```text id="layers1"
Base Image (python:3.14)
        ↓
RUN apt-get update
        ↓
RUN apt-get install curl
        ↓
WORKDIR /app
        ↓
COPY app.py
        ↓
CMD metadata
```

Docker reuses unchanged layers instead of rebuilding them.

---

### 3. Docker Build Cache

When rebuilding the image, Docker checks each step:

* If nothing changed → reuse cached layer
* If something changed → rebuild from that step onward

Example behavior:

```text id="cache1"
Step 1: FROM python:3.14        → cached
Step 2: RUN apt-get update      → cached
Step 3: RUN apt-get install     → cached
Step 4: COPY app.py             → rebuilt if file changes
```

---

### 4. Cache Invalidation Rule

> If a layer changes, all layers after it are invalidated.

This is critical for performance optimization.

---

### 5. Importance of Instruction Order

Bad Dockerfile pattern:

```dockerfile id="bad1"
COPY . .
RUN pip install -r requirements.txt
```

Problem:

* Any code change invalidates dependency installation
* Leads to slow builds

---

Good Dockerfile pattern:

```dockerfile id="good1"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Benefit:

* Dependencies are cached
* Only application code changes trigger rebuilds

---

### 6. WORKDIR Usage

```dockerfile id="workdir1"
WORKDIR /app
```

* Sets working directory inside container
* Automatically creates directory if it does not exist
* Makes paths cleaner and more predictable
* Avoids hardcoding absolute paths

---

## Build Command

```bash id="build1"
docker build -t run-demo .
```

---

## Observations

* First build runs all steps.
* Subsequent builds reuse cached layers.
* Changing only `app.py` invalidates only the `COPY` layer and below.
* Dependency layers remain cached, improving build speed.

---

## Production Insights

* Docker caching significantly reduces CI/CD build times.
* Layer ordering is a key optimization skill in real-world systems.
* Dependency installation should be separated from application code.
* Images should be treated as immutable artifacts.

---

## Summary

After completing this exercise, you should understand:

* How `RUN` differs from `CMD`
* How Docker builds images layer by layer
* How Docker cache improves build performance
* Why instruction ordering matters in Dockerfiles
* How to structure Dockerfiles for production efficiency

This forms the foundation for advanced Docker topics such as multi-stage builds, image optimization, and CI/CD pipelines.
