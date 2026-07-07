# 🧩 02 — Image Layer Optimization

## 🎯 Goal

Understand how the order of Dockerfile instructions affects build caching and why organizing instructions properly leads to faster rebuilds.

---

## 📁 Files

* `app.py`
* `requirements.txt`
* `Dockerfile`

---

## 🧠 The Problem

Imagine your Dockerfile looks like this:

```dockerfile
COPY . .

RUN pip install -r requirements.txt
```

Now suppose you only change:

```python
print("Hello Docker!")
```

Even though your dependencies haven't changed, Docker invalidates the `COPY . .` layer, forcing it to reinstall all Python packages.

This results in slower builds.

---

## ❌ Inefficient Dockerfile

```dockerfile
FROM python:3.14

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

Every source code change invalidates the dependency installation layer.

---

## ✅ Optimized Dockerfile

```dockerfile
FROM python:3.14

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Now Docker installs dependencies only when `requirements.txt` changes.

Changes to your application code reuse the cached dependency layer.

---

## ▶️ Build the Image

```bash
docker build -t cache-demo .
```

---

## ✏️ Try This

1. Build the image.
2. Modify only `app.py`.
3. Build again.

Notice that Docker reuses the cached dependency layer.

Next, modify `requirements.txt` and build once more.

This time Docker reinstalls the dependencies because that layer has changed.

---

## 🎯 Key Takeaway

Arrange Dockerfile instructions from **least frequently changing** to **most frequently changing**.

This allows Docker to maximize layer caching, resulting in:

* Faster rebuilds
* More efficient CI/CD pipelines
* Reduced build times during development
