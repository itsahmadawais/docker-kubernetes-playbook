# 🧩 03 — Bind Mount Live Edit

## 🎯 Goal

Understand the difference between file syncing and application execution.

---

## 📁 Files

- app.py
- Dockerfile
- compose.yaml

---

## 🧠 What happens here

We use a bind mount:

```yaml
volumes:
  - .:/app
````

This means:

* Your local files are synced into the container instantly
* The container always sees the latest version of your code

---

## ⚠️ Important concept

Bind mounts only sync files — they do NOT restart your program.

So even if the file changes inside the container, the running process will not automatically rerun.

---

## ▶️ Run

```bash
docker compose up
```

---

## ✏️ Try this

1. Run the container
2. Keep it running
3. Edit `app.py`

👉 You will see:

* File is updated inside container
* But running program does NOT automatically restart

---

## 🧠 Why this happens

Because Docker handles files, not running processes.

A running script must be restarted manually unless the application supports hot reload.

---

## 🎯 Key Takeaway

Bind mounts update files instantly, but they do not automatically restart or re-execute your application.
