# 📦 03 - ENTRYPOINT vs CMD

## Objective

The objective of this exercise is to understand how Docker determines what runs inside a container using `ENTRYPOINT` and `CMD`, and how both work together to define runtime behavior.

This module builds a mental model of container execution rather than just command syntax.

---

## Project Structure

```text id="s1"
03-entrypoint-vs-cmd/
├── app.py
├── other.py
├── Dockerfile
└── README.md
```

---

## Applications

### app.py

```python id="s2"
print("Docker ENTRYPOINT vs CMD lesson")
```

### other.py

```python id="s3"
print("Hello from other.py")
```

---

## Dockerfile

```dockerfile id="s4"
FROM python:3.14

WORKDIR /app

COPY . .

ENTRYPOINT ["python"]
CMD ["app.py"]
```

---

## Build the Image

```bash id="s5"
docker build -t entrypoint-demo:v1 .
```

---

## Key Concept

This exercise demonstrates how Docker constructs the final runtime command by combining:

```text id="s6"
ENTRYPOINT + CMD
```

---

# ENTRYPOINT vs CMD

## ENTRYPOINT

```dockerfile id="s7"
ENTRYPOINT ["python"]
```

Defines the **fixed executable** for the container.

In this case:

> The container will always run Python.

---

## CMD

```dockerfile id="s8"
CMD ["app.py"]
```

Defines the **default argument** passed to the ENTRYPOINT.

If no runtime arguments are provided, Docker uses this value.

---

## How Docker combines them

When running:

```bash id="s9"
docker run entrypoint-demo:v1
```

Docker executes:

```text id="s10"
python app.py
```

Because:

* ENTRYPOINT → `python`
* CMD → `app.py`

---

## Overriding CMD at runtime

You can override the default argument:

```bash id="s11"
docker run entrypoint-demo:v1 other.py
```

This executes:

```text id="s12"
python other.py
```

---

## Observations

### Case 1 - Default execution

```bash id="s13"
docker run entrypoint-demo:v1
```

Output:

```text id="s14"
Docker ENTRYPOINT vs CMD lesson
```

---

### Case 2 - Overriding CMD

```bash id="s15"
docker run entrypoint-demo:v1 other.py
```

Output:

```text id="s16"
Hello from other.py
```

---

# Key Learnings

## 1. ENTRYPOINT defines the executable

* It defines what the container *is*
* It is not easily overridden
* It acts as the fixed runtime process

---

## 2. CMD defines default arguments

* It provides default behavior
* It can be overridden at runtime
* It works together with ENTRYPOINT

---

## 3. Final command construction

Docker builds the final command like this:

```text id="s17"
ENTRYPOINT + CMD
```

Example:

```text id="s18"
python + app.py
```

---

# Production Usage Patterns

## Pattern 1 - Simple scripts

```dockerfile id="s19"
CMD ["python", "app.py"]
```

---

## Pattern 2 - Controlled runtime (recommended for CLI-style containers)

```dockerfile id="s20"
ENTRYPOINT ["python"]
CMD ["app.py"]
```

---

## Pattern 3 - Backend services

```dockerfile id="s21"
ENTRYPOINT ["uvicorn"]
CMD ["app:app", "--host", "0.0.0.0"]
```

---

# Why this matters

Understanding ENTRYPOINT and CMD is essential because:

* It defines how containers behave at runtime
* It controls how arguments are passed into containers
* It is heavily used in production systems and Kubernetes deployments

---

# Summary

After completing this exercise, you should understand:

* The difference between ENTRYPOINT and CMD
* How Docker constructs the final execution command
* How to override CMD at runtime
* Why ENTRYPOINT defines container identity
* How both work together in real-world containerized applications

This forms a core foundation for understanding container runtime behavior in production environments.
