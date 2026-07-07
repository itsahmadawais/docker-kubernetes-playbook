# 🧩 01 — Using `.dockerignore`

## 🎯 Goal

Understand what the **build context** is and how `.dockerignore` helps reduce unnecessary files sent during a Docker build.

---

## 📁 Files

* `app.py`
* `Dockerfile`
* `.dockerignore`

---

## 🧠 The Problem

When you run:

```bash
docker build .
```

Docker sends the **entire build context** (the current directory) to the Docker Engine (Docker Daemon).

In a real project, this may include files that are not needed to build your image, such as:

* `.git`
* `node_modules`
* `.env`
* Log files
* Temporary files

Sending these files increases build time, image size, and may even expose sensitive information.

---

## ▶️ Build Without `.dockerignore`

First, build the image without creating a `.dockerignore` file.

```bash
docker build -t dockerignore-demo .
```

Notice the build output:

```text
=> transferring context: XX MB
```

Docker transfers every file in the build context.

---

## ✏️ Add `.dockerignore`

Create a `.dockerignore` file:

```text
.git
node_modules
.env
*.log
notes.txt
```

These files and directories will now be excluded from the build context.

---

## ▶️ Build Again

Run the build again:

```bash
docker build -t dockerignore-demo .
```

You'll notice the transferred build context is significantly smaller because Docker ignores the excluded files.

---

## 🎯 Key Takeaway

A `.dockerignore` file prevents unnecessary files from being sent during a Docker build, resulting in:

* Faster builds
* Smaller build context
* Reduced risk of exposing sensitive files
* Cleaner and more efficient Docker images
