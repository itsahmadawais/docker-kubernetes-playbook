# 🧩 01 — No Network (Isolation Problem)

## 🎯 Goal

Understand that Docker containers are isolated by default and cannot automatically communicate with each other.

---

## 📁 Files

* `app.py`
* `Dockerfile`

---

## 🧠 Concept

When containers are started independently using `docker run`, Docker does **not** automatically place them on a shared network.

As a result:

* They cannot discover each other
* They do not share DNS
* They cannot communicate using container names

---

## ▶️ Build

```bash
docker build -t network-demo .
```

---

## ▶️ Run Two Containers

```bash
docker run -d --name app1 network-demo
```

```bash
docker run -d --name app2 network-demo
```

Both containers will continue running.

---

## ✏️ Try This

Open a shell inside `app1`:

```bash
docker exec -it app1 bash
```

Now try to reach `app2`:

```bash
ping app2
```

or

```bash
getent hosts app2
```

You'll notice that Docker cannot resolve `app2` because the containers are running independently and are not connected to a shared network.

---

## 🎯 Key Takeaway

Containers started separately are isolated by default. To allow them to communicate, they must be connected to the same Docker network.
