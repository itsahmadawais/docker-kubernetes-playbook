# 🧩 06 — Production Checklist

## 🎯 Goal

Review the essential practices for building efficient, secure, and maintainable Docker images for production.

This chapter serves as a quick reference to the concepts covered throughout the Docker playbook.

---

## ✅ Use Specific Image Tags

Avoid relying on the `latest` tag.

Instead of:

```dockerfile
FROM python:latest
```

Prefer:

```dockerfile
FROM python:3.14-slim
```

Using specific tags makes builds predictable and reproducible.

---

## ✅ Keep the Build Context Small

Docker sends the build context during every `docker build`.

Use a `.dockerignore` file to exclude unnecessary files such as:

* `.git`
* `node_modules`
* `.env`
* Log files
* Temporary files

A smaller build context leads to faster builds and reduces the risk of including sensitive files.

---

## ✅ Optimize Docker Layers

Arrange Dockerfile instructions from **least frequently changing** to **most frequently changing**.

For example:

1. Copy dependency files.
2. Install dependencies.
3. Copy application source code.

This maximizes Docker's layer caching and speeds up rebuilds.

---

## ✅ Use Multi-Stage Builds

Separate the build environment from the runtime environment.

Only copy the files required to run the application into the final image.

This produces:

* Smaller images
* Cleaner runtime environments
* Improved security

---

## ✅ Run as a Non-Root User

Avoid running applications as the `root` user.

Create a dedicated user and switch to it using the `USER` instruction.

This follows the principle of least privilege and reduces security risks.

---

## ✅ Add Health Checks

Use the `HEALTHCHECK` instruction so Docker can determine whether the application is responding correctly.

A running container does not always indicate a healthy application.

---

## ✅ Write Logs to Standard Output

Applications should write logs to:

* `stdout`
* `stderr`

Docker automatically captures these logs, making them available through:

```bash
docker logs <container-name>
```

Avoid writing application logs to files inside the container.

---

## ✅ Keep Containers Stateless

Containers should not rely on their local filesystem for persistent data.

Store important data using:

* Docker volumes
* External databases
* Object storage

This allows containers to be replaced without losing data.

---

## ✅ Use Environment Variables

Avoid hardcoding configuration values inside the image.

Use environment variables for:

* Database credentials
* API keys
* Connection strings
* Environment-specific settings

---

## 🎯 Final Checklist

Before deploying a Docker image to production, ask yourself:

* ✅ Am I using a specific base image version?
* ✅ Is my build context minimized?
* ✅ Is Docker layer caching optimized?
* ✅ Am I using a multi-stage build where appropriate?
* ✅ Is the application running as a non-root user?
* ✅ Have I configured a health check?
* ✅ Are logs written to `stdout`/`stderr`?
* ✅ Is persistent data stored outside the container?
* ✅ Is configuration provided through environment variables?

If you can confidently answer **Yes** to these questions, your Docker image follows many of the practices commonly used in production environments.

---

## 🚀 What's Next?

So far, you've learned how to:

* Build Docker images
* Run containers
* Manage data with volumes and bind mounts
* Orchestrate services with Docker Compose
* Connect containers using Docker networks
* Apply production-ready Docker practices

The next step is to learn how to deploy and manage these containers at scale using **Kubernetes**.
