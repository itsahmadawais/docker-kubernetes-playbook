# 🧩 02 — Bind Mount Basic

## 🎯 Goal

Understand how `.:/app` maps your local folder into a Docker container.

---

## 📁 Files

- app.py
- Dockerfile
- compose.yaml

---

## 🧠 What is happening

In this setup, we use a bind mount:

```yaml
volumes:
  - .:/app
````

### Meaning:

* `.` → your current project folder (on your machine)
* `/app` → folder inside the container

So Docker connects both like this:

```text
Local Folder (.)  →  Container Folder (/app)
```

Anything inside `/app` in the container is actually your local files.

---

## ▶️ Run

```bash
docker compose up --build
```

---

## ✏️ Try this

1. Run the container
2. Change `app.py`
3. Run again or rerun script

👉 Changes are instantly reflected inside the container because it is using your local files.

---

## 🎯 Key Takeaway

`.:/app` means your local project folder is directly mounted inside the container at `/app`, so both share the same files.

