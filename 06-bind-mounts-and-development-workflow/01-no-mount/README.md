# 🧩 01 — No Mount (Baseline)

## 🎯 Goal

Understand how Docker behaves without bind mounts.

---

## 📁 Files

- app.py
- Dockerfile

---

## 🧠 What happens here

In this setup, your code is copied into the Docker image at build time.

So the container runs a **fixed snapshot** of your code.

---

## ▶️ Run

```bash
docker build -t no-mount .
docker run no-mount
````

---

## ✏️ Try this

1. Change `app.py`
2. Run container again

👉 You will NOT see changes unless you rebuild the image.

---

## 🎯 Key Takeaway

Without bind mounts, code changes require rebuilding the Docker image.

