# 🧩 03 — Multi-Stage Builds

## 🎯 Goal

Understand how multi-stage builds help create smaller, cleaner, and more secure Docker images by separating the build environment from the runtime environment.

---

## 📁 Files

* `app/main.py`
* `app/requirements.txt`
* `Dockerfile.single`
* `Dockerfile.multi`

---

## 🧠 The Problem

A traditional Docker build uses a single stage where everything needed to build the application is also included in the final image.

For example:

* Build dependencies
* Temporary files
* Package caches
* Application code

While this works, the final image often contains files that are only required during the build process.

This leads to:

* Larger Docker images
* Slower deployments
* Increased attack surface
* Unnecessary files in production

---

## ❌ Single-Stage Build

Our first Dockerfile builds and runs the application in a single stage.

Build the image:

```bash id="ms1zkd"
docker build -f Dockerfile.single -t app:single .
```

Run the container:

```bash id="1ev0jk"
docker run -p 8000:8000 app:single
```

The application works correctly, but the entire build environment becomes part of the final image.

---

## ✅ Multi-Stage Build

The second Dockerfile separates the process into two stages:

### Builder Stage

Responsible for:

* Installing dependencies
* Preparing everything required by the application

### Runtime Stage

Responsible for:

* Copying only the required application files and installed dependencies
* Running the application

The runtime image does not include the temporary build environment.

Build the image:

```bash id="7e2wmr"
docker build -f Dockerfile.multi -t app:multi .
```

Run the container:

```bash id="xvjlwm"
docker run -p 8000:8000 app:multi
```

Although both containers behave the same, the multi-stage build produces a cleaner production image.

---

## 🧠 The Key Instruction

The following instruction makes multi-stage builds possible:

```dockerfile id="b7juz0"
COPY --from=builder /install /usr/local
```

It copies only the files produced by the **builder** stage into the final runtime image.

Everything else from the builder stage is discarded.

---

## 🎯 Why Use Multi-Stage Builds?

Multi-stage builds help you:

* Reduce image size
* Remove unnecessary build artifacts
* Improve security by shipping fewer tools
* Create cleaner production images
* Separate build and runtime responsibilities

---

## 🎯 Key Takeaway

A multi-stage build separates **building** an application from **running** it.

Instead of shipping everything used during the build, the final image contains only what is required to run the application, making it a preferred approach for production Docker images.
