# Containerization & Deployment Workshop
## From Local Development to Kubernetes

---

## Section 1: Introduction & Setup

### What We'll Build Today
- A simple Python Flask web service
- Containerize it with Docker
- Orchestrate with Docker Compose
- Deploy to Kubernetes using Minikube

### Prerequisites
- Python 3.11+ installed
- Docker Desktop installed
- kubectl installed
- Minikube installed (for final section)

---

## Section 2: Building Our Web Service Locally

### Step 1: Understanding the Application

Our Flask application is a simple REST API with three endpoints:

```python
GET /              # Welcome message with API info
GET /api/health    # Health check for monitoring
GET /api/time      # Returns current server time
```

### Step 2: Installing Dependencies

Navigate to the project directory:

```bash
cd colorstackcu-teachin-docker-k8s-deploy
```

Install Python dependencies:

```bash
pip install -r web-service/requirements.txt
```

This installs:
- **Flask**: Web framework for building REST APIs
- **Werkzeug**: WSGI utility library (Flask dependency)

### Step 3: Running Locally

Start the development server:

```bash
python web-service/app.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 4: Testing the Endpoints

Open a new terminal and test:

```bash
# Welcome endpoint
curl http://localhost:5000/

# Health check
curl http://localhost:5000/api/health

# Current time
curl http://localhost:5000/api/time
```

---

## Section 3: Introduction to Docker

### What is a Container?

> A **container** is a lightweight, standalone package that includes everything needed to run an application: code, runtime, system tools, libraries, and settings.

**Key Characteristics:**
- Isolated from the host system
- Portable across different environments
- Shares the host OS kernel (unlike VMs)
- Starts in seconds

### What is Docker?

**Docker** is a platform for developing, shipping, and running applications in containers.

**Core Components:**
1. **Docker Engine**: Runs and manages containers
2. **Docker Image**: Blueprint/template for containers
3. **Docker Container**: Running instance of an image
4. **Dockerfile**: Instructions to build an image

### Why Use Containers?

| Problem | Container Solution |
|---------|-------------------|
| "Works on my machine" | Consistent environment everywhere |
| Complex dependencies | Self-contained with all dependencies |
| Slow deployments | Fast startup and scaling |
| Resource intensive VMs | Lightweight, share host kernel |

### Docker vs. Virtual Machines

```
┌─────────────────────┐  ┌─────────────────────┐
│   Virtual Machine   │  │      Container      │
├─────────────────────┤  ├─────────────────────┤
│   App 1  │  App 2   │  │   App 1  │  App 2   │
│  Bins/Libs          │  │  Bins/Libs          │
│  Guest OS           │  ├─────────────────────┤
├─────────────────────┤  │    Docker Engine    │
│    Hypervisor       │  ├─────────────────────┤
├─────────────────────┤  │      Host OS        │
│      Host OS        │  ├─────────────────────┤
│    Infrastructure   │  │   Infrastructure    │
└─────────────────────┘  └─────────────────────┘

    Gigabytes                  Megabytes
    Minutes to start           Seconds to start
```

---

## Section 4: Building Our Docker Image

### Understanding the Dockerfile

A **Dockerfile** contains instructions to build a Docker image.

Let's examine our [`Dockerfile`](file:///Users/mikey/repos/colorstackcu-teachin-docker-k8s-deploy/Dockerfile):

```dockerfile
# Base image: Python 3.11 slim (smaller size)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY web-service/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY web-service/ .

# Expose port 5000
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["python", "app.py"]
```

### Key Dockerfile Instructions

| Instruction | Purpose |
|------------|---------|
| `FROM` | Base image to build upon |
| `WORKDIR` | Set working directory |
| `COPY` | Copy files from host to image |
| `RUN` | Execute commands during build |
| `EXPOSE` | Document which ports to expose |
| `ENV` | Set environment variables |
| `CMD` | Default command to run container |

### Docker Layer Caching

Docker builds images in **layers**. Each instruction creates a new layer.

**Why copy requirements.txt separately?**

```dockerfile
COPY web-service/requirements.txt .     # Layer 1
RUN pip install -r requirements.txt     # Layer 2 (slow)
COPY web-service/ .                     # Layer 3
```

- If you only change code (not requirements), layers 1-2 are cached
- Pip install doesn't run again → faster builds!

### Building the Image

Build the Docker image:

```bash
docker build -t colorstack-web-service:latest .
```

**Flags explained:**
- `-t`: Tag/name the image
- `.`: Build context (current directory)

Expected output:
```
[+] Building 12.3s (10/10) FINISHED
 => [1/5] FROM python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY web-service/requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY web-service/ .
 => exporting to image
```

### Viewing Images

List all Docker images:

```bash
docker images
```

You should see:
```
REPOSITORY                TAG       SIZE
colorstack-web-service    latest    ~150MB
python                    3.11-slim ~130MB
```

---

## Section 5: Running Docker Containers

### Running Our Container

Start a container from our image:

```bash
docker run -d -p 8080:5000 --name my-web-service colorstack-web-service:latest
```

**Flags explained:**
- `-d`: Detached mode (run in background)
- `-p 8080:5000`: Port mapping (host:container)
- `--name`: Name the container
- `colorstack-web-service:latest`: Image to use

### Port Mapping

```
Your Computer          Container
┌────────────┐        ┌────────────┐
│            │        │            │
│  Port 8080 │◄──────►│  Port 5000 │
│            │        │            │
└────────────┘        └────────────┘
```

Traffic to `localhost:8080` → forwarded to container's port `5000`

### Testing the Containerized App

```bash
# Welcome endpoint
curl http://localhost:8080/

# Health check
curl http://localhost:8080/api/health

# Current time
curl http://localhost:8080/api/time
```

### Useful Docker Commands

```bash
# List running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs my-web-service

# Follow logs in real-time
docker logs -f my-web-service

# Stop container
docker stop my-web-service

# Start stopped container
docker start my-web-service

# Remove container
docker rm my-web-service

# Remove container (force stop if running)
docker rm -f my-web-service
```

---

## Section 6: Docker Compose

### What is Docker Compose?

**Docker Compose** is a tool for defining and running multi-container applications using a YAML configuration file.

**Benefits:**
- Define your entire stack in one file
- Manage multiple containers together
- Easier than long `docker run` commands
- Great for development environments

### Our docker-compose.yml

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

### Key Concepts

- **Services**: Containers to run (we have one: `web-service`)
- **Build**: Build from Dockerfile in current directory
- **Ports**: Same as `-p` flag in docker run
- **Environment**: Set environment variables
- **Restart**: Restart policy if container crashes

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View running services
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Docker Compose vs Docker Run

**Docker Run:**
```bash
docker run -d -p 8080:5000 -e PORT=5000 -e FLASK_ENV=development \
  --restart unless-stopped --name colorstack-web-service colorstack-web-service:latest
```

**Docker Compose:**
```bash
docker-compose up -d
```

Much simpler! Especially with multiple services.

---

## Section 7: Introduction to Kubernetes

### What is Kubernetes (K8s)?

**Kubernetes** is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

**Think of it as:**
- Docker manages individual containers
- Kubernetes manages fleets of containers across multiple machines

### Why Kubernetes?

| Feature | Benefit |
|---------|---------|
| **Auto-scaling** | Scale up/down based on load |
| **Self-healing** | Automatically restart failed containers |
| **Load balancing** | Distribute traffic across containers |
| **Rolling updates** | Zero-downtime deployments |
| **Service discovery** | Containers find each other automatically |

### When to Use Kubernetes?

**Good fit:**
- Microservices architectures
- Applications that need high availability
- Teams running many containers
- Multi-environment deployments (dev, staging, prod)

**Overkill for:**
- Simple single-container apps
- Prototypes or MVPs
- Small teams learning containers

### Kubernetes Architecture

```
┌──────────────────────────────────────────────┐
│             Kubernetes Cluster               │
│  ┌────────────────────────────────────────┐  │
│  │         Control Plane (Master)         │  │
│  │  • API Server                          │  │
│  │  • Scheduler                           │  │
│  │  • Controller Manager                  │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Node 1  │  │  Node 2  │  │  Node 3  │  │
│  │  ┌────┐  │  │  ┌────┐  │  │  ┌────┐  │  │
│  │  │Pod │  │  │  │Pod │  │  │  │Pod │  │  │
│  │  └────┘  │  │  └────┘  │  │  └────┘  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└──────────────────────────────────────────────┘
```

### Key Kubernetes Concepts

**Pod**
- Smallest deployable unit
- Contains one or more containers
- Shares network and storage

**Deployment**
- Manages a set of identical Pods
- Handles scaling and updates
- Ensures desired state

**Service**
- Exposes Pods to network traffic
- Provides load balancing
- Stable IP address and DNS name

**Namespace**
- Virtual cluster within a cluster
- Isolates resources

---

## Section 8: Deploying to Minikube

### What is Minikube?

**Minikube** runs a single-node Kubernetes cluster on your local machine for development and learning.

**Perfect for:**
- Learning Kubernetes
- Local development
- Testing K8s manifests
- CI/CD testing

### Prerequisites Check

Ensure you have:
1. ✅ Docker Desktop running
2. ✅ kubectl installed
3. ✅ Minikube installed

See [`minikube-setup.md`](file:///Users/mikey/repos/colorstackcu-teachin-docker-k8s-deploy/minikube-setup.md) for installation instructions.

### Starting Minikube

```bash
# Start Minikube cluster
minikube start

# Check status
minikube status

# Verify kubectl can connect
kubectl cluster-info
```

### Important: Using Local Docker Images

Minikube runs in its own Docker environment. To use our local image:

```bash
# Point your shell to Minikube's Docker daemon
eval $(minikube docker-env)

# Build the image again (now it's in Minikube's registry)
docker build -t colorstack-web-service:latest .

# Verify the image is available
docker images | grep colorstack
```

### Our Kubernetes Manifests

Our [`deploy.yaml`](file:///Users/mikey/repos/colorstackcu-teachin-docker-k8s-deploy/deploy.yaml) contains two resources:

**1. Deployment** (manages Pods)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-service
spec:
  replicas: 2  # Run 2 copies
  selector:
    matchLabels:
      app: web-service
  template:
    metadata:
      labels:
        app: web-service
    spec:
      containers:
      - name: web-service
        image: colorstack-web-service:latest
        imagePullPolicy: Never  # Use local image
        ports:
        - containerPort: 5000
```

**2. Service** (exposes Pods)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  selector:
    app: web-service  # Routes to Pods with this label
  ports:
  - port: 80
    targetPort: 5000
```

### Deploying to Kubernetes

Apply the manifests:

```bash
kubectl apply -f deploy.yaml
```

Expected output:
```
deployment.apps/web-service created
service/web-service created
```

### Verifying the Deployment

```bash
# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services

# Detailed pod information
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>
```

Expected output:
```
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
web-service   2/2     2            2           30s

NAME          READY   STATUS    RESTARTS   AGE
web-service-xxx   1/1     Running   0          30s
web-service-yyy   1/1     Running   0          30s

NAME          TYPE           EXTERNAL-IP   PORT(S)        AGE
web-service   LoadBalancer   <pending>     80:30123/TCP   30s
```

### Accessing the Service

Get the Minikube service URL:

```bash
minikube service web-service --url
```

This returns something like: `http://192.168.49.2:30123`

Test it:

```bash
# Replace with your actual URL
export SERVICE_URL=$(minikube service web-service --url)

curl $SERVICE_URL/
curl $SERVICE_URL/api/health
curl $SERVICE_URL/api/time
```

### Scaling the Application

One of Kubernetes' superpowers is easy scaling:

```bash
# Scale to 5 replicas
kubectl scale deployment web-service --replicas=5

# Verify
kubectl get pods

# Scale back down
kubectl scale deployment web-service --replicas=2
```

### Updating the Application

Make a change to [`app.py`](file:///Users/mikey/repos/colorstackcu-teachin-docker-k8s-deploy/web-service/app.py), then:

```bash
# Rebuild image (in Minikube's Docker)
eval $(minikube docker-env)
docker build -t colorstack-web-service:latest .

# Restart pods to use new image
kubectl rollout restart deployment web-service

# Watch rollout status
kubectl rollout status deployment web-service
```

### Kubernetes Dashboard

Minikube includes a web UI:

```bash
minikube dashboard
```

This opens a browser with:
- Visual view of all resources
- Pod logs
- Resource usage
- And more!

### Cleanup

When you're done:

```bash
# Delete the deployment and service
kubectl delete -f deploy.yaml

# Stop Minikube
minikube stop

# Delete the cluster (optional)
minikube delete
```

---

## Section 9: Recap & Next Steps

### What We Learned

1. ✅ Built a Python Flask web service
2. ✅ Ran it locally with pip
3. ✅ Understood Docker concepts and benefits
4. ✅ Created a Dockerfile
5. ✅ Built and ran Docker containers
6. ✅ Simplified with Docker Compose
7. ✅ Introduced Kubernetes concepts
8. ✅ Deployed to Minikube
9. ✅ Scaled and updated the application

### The Progression

```
Local Development → Docker Container → Docker Compose → Kubernetes
(Single machine)    (Portable)         (Multi-service)  (Production-ready)
```

### Key Takeaways

**Containers solve:**
- "Works on my machine" problems
- Dependency management
- Consistent environments

**Docker provides:**
- Easy containerization
- Image distribution
- Local development tools

**Kubernetes adds:**
- Auto-scaling
- Self-healing
- Load balancing
- Production-grade orchestration

### Next Steps

**Deepen Your Knowledge:**
1. Add a database (PostgreSQL) to docker-compose
2. Implement persistent storage in Kubernetes
3. Set up CI/CD pipelines
4. Explore Helm (K8s package manager)
5. Learn about Ingress controllers
6. Deploy to a managed Kubernetes service (GKE, EKS, AKS)

**Resources:**
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Play with Docker](https://labs.play-with-docker.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

---

## Questions?

Thank you for participating in this workshop! 🎉

**Contact:**
- GitHub: [colorstackcu-teachin-docker-k8s-deploy](https://github.com/)
- Project files: [`README.md`](file:///Users/mikey/repos/colorstackcu-teachin-docker-k8s-deploy/README.md)
