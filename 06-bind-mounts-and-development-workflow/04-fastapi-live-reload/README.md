# 🧩 04 — FastAPI Live Reload

## 🎯 Goal

Build a real development setup where code changes are reflected instantly in a running API.

---

## 📁 Files

- app/
  - main.py
  - requirements.txt
- Dockerfile
- compose.yaml

---

## 🧠 What is happening

We combine:

- Bind mounts (`./app:/app`)
- FastAPI
- Uvicorn `--reload`

This creates a live development environment inside Docker.

---

## 🔗 Key idea

```yaml
volumes:
  - ./app:/app
````

Your local `app` folder is directly used inside the container.

---

## ⚙️ Auto Reload

We run the server with:

```bash
uvicorn main:app --reload
```

This tells FastAPI:

> Watch files and restart server when code changes

---

## ▶️ Run

```bash id="fr8v1q"
docker compose up --build
```

---

## 🌐 Open

```
http://localhost:8000
```

---

## ✏️ Try this

1. Open `main.py`
2. Change response message
3. Save file
4. Refresh browser

👉 You will see changes instantly without rebuilding the image.

---

## 🎯 Key Takeaway

Bind mounts provide live file updates, and `--reload` enables the server to restart automatically — together they create a real development workflow inside Docker.
