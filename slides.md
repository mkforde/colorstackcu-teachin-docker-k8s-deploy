---
marp: true
theme: default
paginate: true
size: 16:9
---

# Containerization & Deployment Workshop
## From Local Development to Kubernetes

**ColorStack CU Teaching Demo**

---

# What We'll Build Today

- ✅ A simple Python Flask web service
- ✅ Containerize it with Docker
- ✅ Orchestrate with Docker Compose
- ✅ Deploy to Kubernetes using Minikube

---

# Prerequisites

- Python 3.11+ installed
- Docker Desktop installed
- kubectl installed
- Minikube installed (for final section)

---

<!-- _class: lead -->
# Section 1
## Building Our Web Service Locally

---

# Our Flask Application

Three simple REST API endpoints:

```python
GET /              # Welcome message with API info
GET /api/health    # Health check for monitoring
GET /api/time      # Returns current server time
```

Simple, easy to understand, perfect for learning!

---

# Installing Dependencies

```bash
# Navigate to the project
cd colorstackcu-teachin-docker-k8s-deploy

# Install Python dependencies
pip install -r web-service/requirements.txt
```

**Installs:**
- Flask 3.0 - Web framework
- Werkzeug - WSGI utility library

---

# Running Locally

```bash
# Start the development server
python web-service/app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

# Testing the Endpoints

```bash
# Welcome endpoint
curl http://localhost:5000/

# Health check
curl http://localhost:5000/api/health

# Current time
curl http://localhost:5000/api/time
```

✅ Everything should return JSON responses

---

<!-- _class: lead -->
# Section 2
## Introduction to Docker

---

# What is a Container?

> A **container** is a lightweight, standalone package that includes everything needed to run an application

**Includes:**
- Code
- Runtime
- System tools
- Libraries
- Settings

---

# Key Container Characteristics

✅ **Isolated** from the host system
✅ **Portable** across different environments
✅ **Shares** the host OS kernel (unlike VMs)
✅ **Starts** in seconds

---

# What is Docker?

**Docker** is a platform for developing, shipping, and running applications in containers.

**Core Components:**
1. **Docker Engine** - Runs and manages containers
2. **Docker Image** - Blueprint/template for containers
3. **Docker Container** - Running instance of an image
4. **Dockerfile** - Instructions to build an image

---

# Why Use Containers?

| Problem | Container Solution |
|---------|-------------------|
| "Works on my machine" | ✅ Consistent everywhere |
| Complex dependencies | ✅ Self-contained |
| Slow deployments | ✅ Fast startup |
| Resource intensive VMs | ✅ Lightweight |

---

# Docker vs Virtual Machines

**Virtual Machine:**
- Entire guest OS included
- Gigabytes in size
- Minutes to start

**Container:**
- Shares host OS kernel
- Megabytes in size
- Seconds to start

---

<!-- _class: lead -->
# Section 3
## Building Our Docker Image

---

# Understanding the Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY web-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY web-service/ .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
```

---

# Key Dockerfile Instructions

| Instruction | Purpose |
|------------|---------|
| `FROM` | Base image to build upon |
| `WORKDIR` | Set working directory |
| `COPY` | Copy files from host to image |
| `RUN` | Execute commands during build |
| `EXPOSE` | Document which ports to expose |
| `ENV` | Set environment variables |
| `CMD` | Default command to run |

---

# Docker Layer Caching

**Why copy requirements.txt separately?**

```dockerfile
COPY web-service/requirements.txt .     # Layer 1
RUN pip install -r requirements.txt     # Layer 2 (slow)
COPY web-service/ .                     # Layer 3
```

- If only code changes → layers 1-2 are cached
- Pip install doesn't run again
- ⚡ **Much faster builds!**

---

# Building the Image

```bash
docker build -t colorstack-web-service:latest .
```

**Flags:**
- `-t` → Tag/name the image
- `.` → Build context (current directory)

**Result:** ~165MB image created

---

# Viewing Images

```bash
docker images
```

**You should see:**
```
REPOSITORY                TAG       SIZE
colorstack-web-service    latest    ~165MB
python                    3.11-slim ~130MB
```

---

<!-- _class: lead -->
# Section 4
## Running Docker Containers

---

# Running Our Container

```bash
docker run -d -p 8080:5000 \
  --name my-web-service \
  colorstack-web-service:latest
```

**Flags:**
- `-d` → Detached mode (background)
- `-p 8080:5000` → Port mapping (host:container)
- `--name` → Name the container

---

# Port Mapping Explained

```
Your Computer          Container
┌────────────┐        ┌────────────┐
│            │        │            │
│  Port 8080 │◄──────►│  Port 5000 │
│            │        │            │
└────────────┘        └────────────┘
```

Traffic to `localhost:8080` → forwarded to container's port `5000`

---

# Testing the Container

```bash
# Welcome endpoint
curl http://localhost:8080/

# Health check
curl http://localhost:8080/api/health

# Current time
curl http://localhost:8080/api/time
```

✅ Same app, now containerized!

---

# Useful Docker Commands

```bash
docker ps                    # List running containers
docker ps -a                 # All containers
docker logs my-web-service   # View logs
docker logs -f my-web-service # Follow logs
docker stop my-web-service   # Stop container
docker start my-web-service  # Start stopped container
docker rm my-web-service     # Remove container
```

---

<!-- _class: lead -->
# Section 5
## Docker Compose

---

# What is Docker Compose?

**Tool for defining and running multi-container applications using YAML**

**Benefits:**
✅ Define entire stack in one file
✅ Manage multiple containers together
✅ Easier than long `docker run` commands
✅ Great for development

---

# Our compose.yml

```yaml
version: '3.8'
services:
  web-service:
    build: .
    container_name: colorstack-web-service
    ports:
      - "8080:5000"
    environment:
      - PORT=5000
      - FLASK_ENV=development
    restart: unless-stopped
```

---

# Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View running services
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

# Docker Compose vs Docker Run

**Docker Run:**
```bash
docker run -d -p 8080:5000 -e PORT=5000 \
  -e FLASK_ENV=development \
  --restart unless-stopped \
  --name colorstack-web-service \
  colorstack-web-service:latest
```

**Docker Compose:**
```bash
docker-compose up -d
```

**Much simpler!** Especially with multiple services.

---

<!-- _class: lead -->
# Section 6
## Introduction to Kubernetes

---

# What is Kubernetes (K8s)?

**Open-source container orchestration platform**

**Manages:**
- Deployment automation
- Scaling
- Management of containerized applications

**Think of it:** Docker manages containers, Kubernetes manages fleets of containers across machines

---

# Why Kubernetes?

| Feature | Benefit |
|---------|---------|
| Auto-scaling | Scale up/down based on load |
| Self-healing | Restart failed containers |
| Load balancing | Distribute traffic |
| Rolling updates | Zero-downtime deployments |
| Service discovery | Containers find each other |

---

# When to Use Kubernetes?

**✅ Good fit:**
- Microservices architectures
- High availability needs
- Many containers
- Multi-environment deployments

**❌ Overkill for:**
- Simple single-container apps
- Prototypes/MVPs
- Small teams learning containers

---

# Key Kubernetes Concepts

**Pod**
- Smallest deployable unit
- Contains one or more containers

**Deployment**
- Manages a set of identical Pods
- Handles scaling and updates

**Service**
- Exposes Pods to network traffic
- Provides load balancing

---

<!-- _class: lead -->
# Section 7
## Deploying to Minikube

---

# What is Minikube?

**Runs a single-node Kubernetes cluster locally**

**Perfect for:**
✅ Learning Kubernetes
✅ Local development
✅ Testing K8s manifests
✅ CI/CD testing

---

# Starting Minikube

```bash
# Start Minikube cluster
minikube start

# Check status
minikube status

# Verify kubectl can connect
kubectl cluster-info
```

---

# Using Local Docker Images

Minikube runs in its own Docker environment.

**To use our local image:**

```bash
# Point shell to Minikube's Docker daemon
eval $(minikube docker-env)

# Build the image (now in Minikube's registry)
docker build -t colorstack-web-service:latest .
```

---

# Our Kubernetes Manifests

**deploy.yaml contains:**

1. **Deployment** - Manages 2 Pod replicas
2. **Service** - Exposes Pods via LoadBalancer

Both are well-commented for teaching!

---

# Deploying to Kubernetes

```bash
# Apply the manifests
kubectl apply -f deploy.yaml

# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services
```

---

# Accessing the Service

```bash
# Get the service URL
minikube service web-service --url

# Test it
export SERVICE_URL=$(minikube service web-service --url)
curl $SERVICE_URL/
curl $SERVICE_URL/api/health
```

---

# Scaling the Application

**One of Kubernetes' superpowers:**

```bash
# Scale to 5 replicas
kubectl scale deployment web-service --replicas=5

# Verify
kubectl get pods

# Scale back down
kubectl scale deployment web-service --replicas=2
```

⚡ **Instant scaling!**

---

# Kubernetes Dashboard

```bash
minikube dashboard
```

**Opens web UI with:**
- Visual view of all resources
- Pod logs
- Resource usage
- Easy troubleshooting

---

<!-- _class: lead -->
# Recap & Next Steps

---

# What We Learned

✅ Built a Python Flask web service
✅ Ran it locally with pip
✅ Understood Docker concepts
✅ Created a Dockerfile
✅ Built and ran Docker containers
✅ Simplified with Docker Compose
✅ Learned Kubernetes concepts
✅ Deployed to Minikube
✅ Scaled applications

---

# The Progression

```
Local Development
    ↓
Docker Container (Portable)
    ↓
Docker Compose (Multi-service)
    ↓
Kubernetes (Production-ready)
```

---

# Key Takeaways

**Containers solve:**
- "Works on my machine" ✅
- Dependency management ✅
- Consistent environments ✅

**Kubernetes adds:**
- Auto-scaling ✅
- Self-healing ✅
- Production-grade orchestration ✅

---

# Next Steps

1. Add database to docker-compose
2. Implement persistent storage in K8s
3. Set up CI/CD pipelines
4. Explore Helm charts
5. Deploy to managed K8s (GKE, EKS, AKS)

---

# Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Play with Docker](https://labs.play-with-docker.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

---

<!-- _class: lead -->
# Questions?

## Thank you! 🎉

**Check out the full resources in the repo**
