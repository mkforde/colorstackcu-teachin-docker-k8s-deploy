# Docker & Kubernetes Teaching Demo

A hands-on workshop for learning containerization and deployment, from local development to production-ready Kubernetes deployments.

## 🎯 Workshop Overview

This teaching demo guides you through the complete journey of containerizing and deploying a web application:

1. **Local Development** - Build and run a Python Flask web service
2. **Docker Basics** - Understand containers and create a Dockerfile
3. **Docker Run** - Build and run containers locally
4. **Docker Compose** - Simplify multi-container orchestration
5. **Kubernetes Intro** - Learn core K8s concepts
6. **Minikube Deployment** - Deploy to a local Kubernetes cluster

## 📁 Project Structure

```
colorstackcu-teachin-docker-k8s-deploy/
├── web-service/
│   ├── app.py              # Flask web service
│   └── requirements.txt    # Python dependencies
├── Dockerfile              # Container image definition
├── compose.yml             # Docker Compose configuration
├── deploy.yaml             # Kubernetes manifests
├── .dockerignore           # Docker build exclusions
├── slides.md               # Workshop presentation
├── minikube-setup.md       # Minikube installation guide
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker Desktop
- kubectl (for Kubernetes section)
- Minikube (for Kubernetes section)

### 1. Run Locally

```bash
# Install dependencies
pip install -r web-service/requirements.txt

# Run the application
python web-service/app.py

# Test it
curl http://localhost:5000/
```

### 2. Run with Docker

```bash
# Build the image
docker build -t colorstack-web-service:latest .

# Run the container
docker run -d -p 8080:5000 --name my-web-service colorstack-web-service:latest

# Test it
curl http://localhost:8080/
```

### 3. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# Test it
curl http://localhost:8080/

# Stop services
docker-compose down
```

### 4. Deploy to Kubernetes (Minikube)

See [minikube-setup.md](minikube-setup.md) for detailed setup instructions.

```bash
# Start Minikube
minikube start

# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the image
docker build -t colorstack-web-service:latest .

# Deploy to Kubernetes
kubectl apply -f deploy.yaml

# Get the service URL
minikube service web-service --url

# Test it
curl $(minikube service web-service --url)/
```

## 📚 API Endpoints

The web service provides three endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message with API documentation |
| `/api/health` | GET | Health check for monitoring |
| `/api/time` | GET | Returns current server time |

### Example Responses

```bash
# Welcome
$ curl http://localhost:5000/
{
  "message": "Welcome to the ColorStack Teaching Demo!",
  "endpoints": { ... }
}

# Health check
$ curl http://localhost:5000/api/health
{
  "status": "healthy",
  "service": "web-service",
  "version": "1.0.0"
}

# Server time
$ curl http://localhost:5000/api/time
{
  "server_time": "2025-11-20T19:00:00",
  "timezone": "UTC",
  "timestamp": 1732132800.0
}
```

## 📖 Documentation

- **[slides.md](slides.md)** - Complete workshop slides with detailed explanations
- **[minikube-setup.md](minikube-setup.md)** - Minikube installation and troubleshooting guide

## 🎓 Learning Objectives

By the end of this workshop, you'll understand:

- ✅ How to containerize applications with Docker
- ✅ Dockerfile best practices (layer caching, multi-stage builds)
- ✅ Container networking and port mapping
- ✅ Docker Compose for multi-container apps
- ✅ Core Kubernetes concepts (Pods, Deployments, Services)
- ✅ Deploying to Kubernetes with Minikube
- ✅ Scaling and updating applications in Kubernetes

## 🛠️ Technologies Used

- **Python 3.11** - Application runtime
- **Flask 3.0** - Web framework
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration
- **Kubernetes** - Container orchestration
- **Minikube** - Local Kubernetes cluster

## 🔧 Common Commands

### Docker

```bash
# Build image
docker build -t colorstack-web-service:latest .

# Run container
docker run -d -p 8080:5000 colorstack-web-service:latest

# View logs
docker logs <container-id>

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deploy.yaml

# Get resources
kubectl get pods
kubectl get deployments
kubectl get services

# View logs
kubectl logs <pod-name>

# Scale deployment
kubectl scale deployment web-service --replicas=5

# Delete resources
kubectl delete -f deploy.yaml
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t colorstack-web-service:latest .
```

### Kubernetes Pod Issues

```bash
# Describe pod for detailed info
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>

# Delete and recreate
kubectl delete -f deploy.yaml
kubectl apply -f deploy.yaml
```

See [minikube-setup.md](minikube-setup.md#troubleshooting) for Minikube-specific issues.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Created for the ColorStack CU teaching workshop on containerization and Kubernetes deployment.

## 📬 Questions or Feedback?

Feel free to open an issue or submit a pull request!

---

**Ready to start?** Check out [slides.md](slides.md) for the full workshop presentation! 🚀
