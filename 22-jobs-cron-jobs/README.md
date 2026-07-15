# 📦 22 — Jobs and CronJobs

## 🎯 Goal

So far, we've used Kubernetes controllers that keep applications running continuously.

- **Deployment** keeps a specified number of Pods running.
- **StatefulSet** keeps stateful Pods running with stable identities.

However, not every workload is a long-running application.

Many tasks only need to run once and then exit successfully.

Examples include:

- Database migrations
- Importing CSV files
- Sending emails
- Generating reports
- Creating database backups
- Cleaning temporary files

These are known as **batch workloads**.

Kubernetes provides **Jobs** and **CronJobs** to run these workloads reliably.

In this module, we'll learn the difference between Jobs and CronJobs by using a simple BusyBox container.

---

# 📁 Project Structure

```text
22-jobs-cronjobs/
│
├── job.yaml
├── cronjob.yaml
└── README.md
```

---

# 🧠 Why Deployments Aren't Suitable

Deployments are designed for applications that should keep running.

Consider a Deployment that runs a script.

```text
Run Script

↓

Script Finishes

↓

Container Exits

↓

Deployment Creates Another Pod

↓

Script Runs Again
```

This continues forever.

For one-time tasks, this isn't the behavior we want.

---

# 🧠 What is a Job?

A **Job** tells Kubernetes:

> Run this task until it completes successfully.

The Job creates a Pod.

The Pod runs the task.

When the task finishes successfully, the Pod stops and the Job is marked as **Completed**.

```text
Create Job

↓

Create Pod

↓

Run Task

↓

Task Completes

↓

Completed
```

If the task fails, Kubernetes automatically creates another Pod and retries until the Job succeeds (subject to the Job's retry configuration).

---

# 🧠 What is a CronJob?

A **CronJob** runs Jobs on a schedule.

Instead of creating one Job, Kubernetes automatically creates new Jobs based on a cron schedule.

For example:

```text
Every Day at 2 AM

↓

Create Job

↓

Run Task

↓

Completed

↓

Wait

↓

Next Scheduled Time

↓

Create Another Job
```

A CronJob does **not** execute your application directly.

It creates a **Job**, and that Job creates a Pod to run the task.

---

# 🧠 Job vs CronJob

| Job | CronJob |
|------|----------|
| Runs once | Runs on a schedule |
| Creates one Job | Creates multiple Jobs over time |
| Used for one-time tasks | Used for recurring tasks |

---

# 🧠 Mental Model

```text
Deployment

Start

↓

Run Forever

────────────────────────

Job

Start

↓

Run Once

↓

Completed

────────────────────────

CronJob

Schedule

↓

Create Job

↓

Run Once

↓

Completed

↓

Wait

↓

Repeat
```

---

# 💡 Running Your Own Scripts

In this module, we'll use a lightweight BusyBox container to keep the examples simple.

In real-world applications, Jobs and CronJobs typically execute your own application packaged as a Docker image.

For example:

```text
report-generator/
├── app.py
├── requirements.txt
└── Dockerfile
```

Build the image:

```bash
docker build -t report-generator:latest .
```

Then reference it in your Job:

```yaml
containers:
  - name: report-generator
    image: report-generator:latest
```

When the Pod starts, Kubernetes runs the container's default command defined in the Dockerfile.

Once the application finishes successfully, the Job is marked as **Completed**.

---

# 📄 Job Configuration

`job.yaml`

```yaml
apiVersion: batch/v1
kind: Job

metadata:
  name: hello-job

spec:
  template:
    spec:
      restartPolicy: Never

      containers:
        - name: hello
          image: busybox:latest

          command:
            - sh
            - -c
            - |
              echo "Starting Job..."
              sleep 10
              echo "Job completed successfully!"
```

---

# 📝 YAML Breakdown

## restartPolicy

```yaml
restartPolicy: Never
```

The container should not restart inside the same Pod.

If the Job fails, Kubernetes creates a new Pod instead.

---

## command

```yaml
command:
```

Specifies the command executed when the container starts.

In this example, BusyBox prints two messages with a short delay between them.

---

# 🚀 Run the Job

```bash
kubectl apply -f job.yaml
```

---

# 🔍 Watch the Pod

```bash
kubectl get pods -w
```

You'll observe something similar to:

```text
READY   STATUS

0/1     ContainerCreating

1/1     Running

0/1     Completed
```

Notice that the Pod finishes successfully instead of running forever.

---

# 🔍 Inspect the Job

```bash
kubectl get jobs
```

Example output:

```text
NAME        COMPLETIONS   DURATION

hello-job   1/1           12s
```

Notice that the Job has successfully completed.

---

# 🔍 View the Logs

```bash
kubectl logs job/hello-job
```

Example output:

```text
Starting Job...

Job completed successfully!
```

---

# 📄 CronJob Configuration

`cronjob.yaml`

```yaml
apiVersion: batch/v1
kind: CronJob

metadata:
  name: hello-cronjob

spec:
  schedule: "*/1 * * * *"

  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never

          containers:
            - name: hello
              image: busybox:latest

              command:
                - sh
                - -c
                - |
                  echo "CronJob started..."
                  date
                  sleep 10
                  echo "CronJob finished!"
```

---

# 📝 YAML Breakdown

## schedule

```yaml
schedule: "*/1 * * * *"
```

Defines when Kubernetes should create a new Job.

This example creates a Job every minute.

Cron expressions can schedule tasks every minute, hour, day, week, or month.

---

## jobTemplate

```yaml
jobTemplate:
```

Defines the Job that the CronJob creates at every scheduled execution.

---

# 🚀 Run the CronJob

```bash
kubectl apply -f cronjob.yaml
```

---

# 🔍 Inspect the CronJob

```bash
kubectl get cronjobs
```

Example output:

```text
NAME              SCHEDULE

hello-cronjob     */1 * * * *
```

---

# 🔍 Watch Jobs Being Created

```bash
kubectl get jobs -w
```

Every minute, Kubernetes creates a new Job.

Example output:

```text
hello-cronjob-29238145

hello-cronjob-29238146

hello-cronjob-29238147
```

Notice that each execution creates a brand-new Job.

---

# 🔍 Watch the Pods

```bash
kubectl get pods -w
```

Every scheduled execution creates a new Pod.

```text
Running

↓

Completed
```

The Pod finishes, and Kubernetes waits until the next scheduled execution.

---

# 🔍 View the Logs

Choose one of the created Jobs.

```bash
kubectl logs job/<job-name>
```

Example output:

```text
CronJob started...

Mon Jul 14 12:00:00 UTC 2026

CronJob finished!
```

---

# 🧹 Cleanup

Delete the CronJob:

```bash
kubectl delete cronjob hello-cronjob
```

Delete all completed Jobs:

```bash
kubectl delete jobs --all
```

---

# 🎯 Key Takeaways

After completing this module, we understand:

- Deployments keep applications running continuously.
- Jobs execute tasks once until they complete successfully.
- CronJobs create Jobs on a schedule.
- Jobs create Pods to execute workloads.
- CronJobs create Jobs, which in turn create Pods.
- Completed Jobs do not continue running indefinitely.
- Production Jobs typically execute custom Docker images containing application code or scripts.
- Jobs and CronJobs are commonly used for batch processing, scheduled maintenance, backups, migrations, and report generation.

In the next module, we'll learn about **Ingress**, which allows external users to access applications running inside a Kubernetes cluster through HTTP and HTTPS.