# 📦 06 — Bind Mounts, Live Development & Compose Overrides

---

## 🧠 Overview

This module connects everything about **Docker development workflow**:

- Why we needed bind mounts
- How live code syncing works
- Why rebuilds are not always required
- How FastAPI enables live reload
- How Docker Compose supports dev vs prod setups

---

## 🧠 Problem We Started With

When I first learned Docker, I thought:

> “Every code change will require rebuilding the image again.”

So even a small change like:

```python
print("Hello World")
````

required:

```bash id="g6p1"
docker build
docker run
```

again and again.

---

## ❌ The Problem

This caused:

* Slow development cycle
* Constant image rebuilding
* No instant feedback loop
* Frustration during debugging

---

## 💡 The Solution Journey

We solved this step by step:

---

# 🧩 01 — No Mount (Baseline)

We saw that:

```text id="g6p2"
Code → Build Image → Run Container
```

✔ Changes require rebuild
✔ Image is static snapshot

---

# 🧩 02 — Bind Mount Basic

We introduced:

```yaml id="g6p3"
volumes:
  - .:/app
```

Meaning:

```text id="g6p4"
Local folder → /app inside container
```

✔ No rebuild needed
✔ Container uses live files

---

# 🧩 03 — Live Edit Behavior

We learned:

* Files update instantly inside container
* BUT running program does NOT auto-rerun

✔ File sync ≠ process restart

---

# 🧩 04 — FastAPI Live Reload

We built real workflow:

* Bind mounts + FastAPI + Uvicorn `--reload`

```text id="g6p5"
Edit Code → File Sync → Server Reload → Instant Response
```

✔ Real backend development workflow

---

# ⚙️ 05 — Compose Override Concept

We introduced environment separation:

## Base

```yaml id="g6p6"
compose.yaml → shared setup
```

## Dev override

```yaml id="g6p7"
compose.override.yaml → live reload + bind mounts
```

## Prod override

```yaml id="g6p8"
compose.prod.yaml → stable image-based deployment
```

✔ Same project, different environments

---

## 🧠 Final Mental Model

### ❌ Without Bind Mounts

```text id="g6p9"
Code Change → Rebuild Image → Restart Container
```

---

### ✅ With Bind Mounts

```text id="g6p10"
Code Change → Instant File Sync → Container Uses Updated Code
```

---

### 🚀 With FastAPI + Reload

```text id="g6p11"
Code Change → Sync → Auto Server Restart → Live API Update
```

---

## 🎯 Key Takeaways

* Docker images are static snapshots
* Bind mounts enable live file syncing
* Execution and file system are separate concepts
* Dev and prod require different Docker strategies
* Compose override helps manage environments cleanly