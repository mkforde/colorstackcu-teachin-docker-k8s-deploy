# Minikube Setup Guide

This guide will help you set up Minikube on your local machine for the Kubernetes section of the workshop.

## Prerequisites

Before installing Minikube, ensure you have:
- ✅ **Docker Desktop** installed and running
- ✅ At least **2 CPUs** available
- ✅ At least **2GB of free memory**
- ✅ At least **20GB of free disk space**

## Installation

### macOS

**Option 1: Using Homebrew (Recommended)**

```bash
# Install kubectl
brew install kubectl

# Install Minikube
brew install minikube
```

**Option 2: Direct Download**

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

### Linux

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Windows

**Using Chocolatey:**

```powershell
# Install kubectl
choco install kubernetes-cli

# Install Minikube
choco install minikube
```

**Using Windows Package Manager:**

```powershell
winget install Kubernetes.kubectl
winget install Kubernetes.minikube
```

## Verify Installation

Check that both tools are installed correctly:

```bash
# Check kubectl version
kubectl version --client

# Check Minikube version
minikube version
```

Expected output:
```
Client Version: v1.28.x
minikube version: v1.32.x
```

## Starting Minikube

### Start the Cluster

```bash
# Start Minikube with Docker driver
minikube start --driver=docker

# This will take 2-5 minutes on first run
```

Expected output:
```
😄  minikube v1.32.0 on Darwin 14.0
✨  Using the docker driver based on user configuration
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster
```

### Verify the Cluster

```bash
# Check cluster status
minikube status

# Check cluster info
kubectl cluster-info

# Verify nodes
kubectl get nodes
```

Expected output:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   30s   v1.28.3
```

## Using Local Docker Images with Minikube

Minikube runs in its own Docker environment. To use locally built Docker images:

### Option 1: Use Minikube's Docker Daemon

```bash
# Point your shell to Minikube's Docker daemon
eval $(minikube docker-env)

# Now build your image
docker build -t colorstack-web-service:latest .

# The image is now available to Minikube
```

> **Note:** Run `eval $(minikube docker-env)` in each new terminal session where you want to build images for Minikube.

### Option 2: Load Images into Minikube

```bash
# Build image normally
docker build -t colorstack-web-service:latest .

# Load it into Minikube
minikube image load colorstack-web-service:latest
```

### Verify Images

```bash
# List images in Minikube
minikube image ls | grep colorstack
```

## Deploying the Web Service

### Step 1: Build the Image

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the image
docker build -t colorstack-web-service:latest .
```

### Step 2: Apply Kubernetes Manifests

```bash
# Deploy the application
kubectl apply -f deploy.yaml
```

Expected output:
```
deployment.apps/web-service created
service/web-service created
```

### Step 3: Verify Deployment

```bash
# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services
```

Wait until all pods show `STATUS: Running` and `READY: 1/1`.

### Step 4: Access the Service

Get the service URL:

```bash
minikube service web-service --url
```

This returns something like: `http://192.168.49.2:30123`

Test it:

```bash
# Store the URL
export SERVICE_URL=$(minikube service web-service --url)

# Test endpoints
curl $SERVICE_URL/
curl $SERVICE_URL/api/health
curl $SERVICE_URL/api/time
```

### Step 5: Open in Browser

```bash
# This automatically opens the service in your browser
minikube service web-service
```

## Useful Minikube Commands

### Cluster Management

```bash
# Start the cluster
minikube start

# Stop the cluster
minikube stop

# Delete the cluster
minikube delete

# Pause the cluster (saves resources)
minikube pause

# Unpause the cluster
minikube unpause

# Check cluster status
minikube status
```

### Dashboard

```bash
# Open Kubernetes dashboard in browser
minikube dashboard

# Get dashboard URL without opening browser
minikube dashboard --url
```

### Accessing Services

```bash
# Get service URL
minikube service <service-name> --url

# Open service in browser
minikube service <service-name>

# List all services
minikube service list
```

### Logs and Debugging

```bash
# View Minikube logs
minikube logs

# SSH into the Minikube VM
minikube ssh

# View events
kubectl get events --sort-by='.lastTimestamp'
```

### Add-ons

```bash
# List available add-ons
minikube addons list

# Enable an add-on (e.g., metrics-server)
minikube addons enable metrics-server

# Disable an add-on
minikube addons disable metrics-server
```

## Troubleshooting

### Issue: Minikube won't start

**Solution 1: Check Docker is running**
```bash
docker ps
```

**Solution 2: Delete and recreate cluster**
```bash
minikube delete
minikube start
```

**Solution 3: Specify more resources**
```bash
minikube start --cpus=4 --memory=4096
```

### Issue: Pods are in "ImagePullBackOff" status

This means Kubernetes can't find the Docker image.

**Solution: Build image in Minikube's Docker**
```bash
eval $(minikube docker-env)
docker build -t colorstack-web-service:latest .
kubectl rollout restart deployment web-service
```

**Verify imagePullPolicy is set to "Never"** in `deploy.yaml`:
```yaml
imagePullPolicy: Never
```

### Issue: Can't access the service

**Solution 1: Use minikube service command**
```bash
minikube service web-service --url
```

**Solution 2: Use port forwarding**
```bash
kubectl port-forward service/web-service 8080:80
# Then access at http://localhost:8080
```

### Issue: Pods are not running

**Check pod status:**
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Common causes:**
- Image not found (see ImagePullBackOff solution above)
- Insufficient resources
- Application crashes on startup

### Issue: "Connection refused" when accessing service

**Check if pods are ready:**
```bash
kubectl get pods
```

Wait until `READY` shows `1/1` and `STATUS` shows `Running`.

### Issue: Minikube uses too much CPU/Memory

**Solution: Stop when not in use**
```bash
minikube stop
```

**Or pause instead:**
```bash
minikube pause
```

## Cleaning Up

After the workshop:

```bash
# Delete the deployment and service
kubectl delete -f deploy.yaml

# Stop Minikube
minikube stop

# (Optional) Delete the cluster entirely
minikube delete
```

## Additional Resources

- [Official Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Tutorials](https://kubernetes.io/docs/tutorials/)
- [Minikube GitHub](https://github.com/kubernetes/minikube)

## Next Steps

Once you're comfortable with Minikube:
1. Try deploying multi-service applications
2. Experiment with persistent volumes
3. Set up Ingress for routing
4. Explore Helm for package management
5. Consider managed Kubernetes services (GKE, EKS, AKS) for production
