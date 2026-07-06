# 🧩 05 — Docker Compose Override (Dev vs Prod)

## 🎯 Goal

Understand how Docker Compose allows different configurations for development and production using override files.

---

## 🧠 Problem

In real projects, we don’t want the same setup for:

- Development (fast iteration, live reload)
- Production (stable, optimized, no live mounts)

But maintaining separate full files causes duplication.

---

## 💡 Solution: Compose Override

Docker Compose can merge multiple files automatically.

---

## 📁 Files

- compose.yaml (base)
- compose.override.yaml (dev changes)
- compose.prod.yaml (production changes)

---

## 🧠 How it works

### Base file (shared)

```yaml id="ov1"
services:
  app:
    build: .
    ports:
      - "8000:8000"
````

---

### Dev override (automatic)

If `compose.override.yaml` exists, Docker automatically applies it when you run:

```bash id="ov2"
docker compose up
```

Example:

```yaml id="ov3"
services:
  app:
    volumes:
      - .:/app
    command: uvicorn main:app --reload
```

---

### Production override (manual)

Production config is applied manually:

```bash id="ov4"
docker compose -f compose.yaml -f compose.prod.yaml up
```

Example:

```yaml id="ov5"
services:
  app:
    image: my-app:v1.0.0
    volumes: []
```

---

## 🧠 Key idea

Docker Compose merges files:

```text id="ov6"
base + override → final configuration
```

---

## ▶️ Dev Run

```bash id="ov7"
docker compose up
```

Automatically uses:

* compose.yaml
* compose.override.yaml (if present)

---

## ▶️ Prod Run

```bash id="ov8"
docker compose -f compose.yaml -f compose.prod.yaml up
```

---

## 🎯 Key Takeaway

Compose override lets you reuse one base setup and change behavior for dev and prod without duplicating configuration.
