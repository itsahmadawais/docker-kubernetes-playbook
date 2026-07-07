# 🧩 05 — Running as a Non-Root User

## 🎯 Goal

Understand why running applications as the **root** user inside a container is discouraged and how to run them as a dedicated non-root user instead.

---

## 📁 Files

* `app/main.py`
* `app/requirements.txt`
* `Dockerfile.root`
* `Dockerfile.non-root`

---

## 🧠 The Problem

By default, most Docker containers run as the **root** user.

This means the application inside the container has elevated privileges.

Although containers provide isolation, running as root is considered a security risk because a compromised application has more permissions than it typically needs.

Following the **principle of least privilege**, applications should run with only the permissions required to perform their tasks.

---

## 💡 The Solution

Instead of running the application as `root`, we:

1. Create a dedicated user.
2. Give the application ownership of its files.
3. Switch to that user before starting the application.

This limits the permissions available to the application and improves container security.

---

## 🧠 Understanding the Dockerfile

Our non-root Dockerfile contains the following instructions:

```dockerfile
RUN useradd --create-home appuser

USER appuser

COPY --chown=appuser:appuser app/ .
```

Let's understand each instruction.

---

### `RUN useradd --create-home appuser`

Creates a new Linux user named `appuser`.

The `--create-home` flag also creates a home directory for the user.

---

### `USER appuser`

Changes the default user for all subsequent Dockerfile instructions and for the application when the container starts.

Instead of running as `root`, the application now runs as `appuser`.

---

### `COPY --chown=appuser:appuser app/ .`

Copies the application files into the image and assigns ownership to `appuser`.

Without this step, the files would typically be owned by `root`, which could prevent the non-root user from accessing or modifying them when required.

---

## ▶️ Build the Images

Build the image that runs as **root**:

```bash
docker build -f Dockerfile.root -t app-root .
```

Build the image that runs as a **non-root** user:

```bash
docker build -f Dockerfile.non-root -t app-non-root .
```

---

## ▶️ Run the Containers

Run the root version:

```bash
docker run -p 8000:8000 --name root-container app-root
```

Open:

```text
http://localhost:8000
```

The application returns something similar to:

```json
{
  "message": "Running as non-root",
  "uid": 0,
  "gid": 0
}
```

A UID of `0` indicates the application is running as the **root** user.

---

Run the non-root version:

```bash
docker run -p 8001:8000 --name non-root-container app-non-root
```

Open:

```text
http://localhost:8001
```

Now you'll see something similar to:

```json
{
  "message": "Running as non-root",
  "uid": 1000,
  "gid": 1000
}
```

The exact UID and GID may differ depending on the image, but they will no longer be `0`, indicating the application is running as a regular user.

---

## 🎯 Why Run as a Non-Root User?

Running containers as a non-root user:

* Reduces security risks
* Limits the impact of a compromised application
* Follows the principle of least privilege
* Aligns with container security best practices

---

## 🎯 Key Takeaway

Containers run as the **root** user by default, but production applications should avoid unnecessary privileges.

Creating a dedicated user and running the application as that user is a simple yet effective way to improve the security of your Docker images.
