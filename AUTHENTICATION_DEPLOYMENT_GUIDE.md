# Highland Tower Development - Authentication & Deployment Guide

## Authentication System

The Highland Tower gcPanel platform now requires authentication before accessing the dashboard.

### Login Credentials

**Production Team Access:**
- **Administrator**: `admin` / `highland2025`
- **Project Manager**: `manager` / `manager123`
- **Site Engineer**: `engineer` / `engineer123`

### Security Features

- Secure password hashing using SHA-256
- Session state management
- Role-based access control
- Automatic logout functionality
- Login attempt monitoring

## Docker Deployment

### Build and Run Container

```bash
# Build the Docker image
docker build -t gcpanel:latest .

# Run the container
docker run -d \
  --name gcpanel-app \
  -p 5000:5000 \
  -e DATABASE_URL="your_database_url" \
  gcpanel:latest
```

### Docker Features

- Non-root user for security
- Health checks for monitoring
- Optimized layer caching
- Production-ready configuration

## Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Create namespace and resources
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Check deployment status
kubectl get pods -n highland-tower
kubectl get services -n highland-tower
```

### Kubernetes Components

- **Namespace**: `highland-tower` with resource quotas
- **Deployment**: 2 replica pods with health checks
- **Service**: ClusterIP service for internal access
- **Ingress**: HTTPS with SSL termination
- **ConfigMap**: Streamlit configuration
- **PVC**: Persistent storage for data

### Production URLs

- **Internal**: `http://gcpanel-service.highland-tower.svc.cluster.local`
- **External**: `https://gcpanel.highland-tower.com`

## Security Configuration

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=5000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### TLS/SSL Setup

The Kubernetes ingress includes:
- Automatic SSL certificate management
- Force HTTPS redirects
- Secure headers configuration

## Monitoring & Health Checks

### Health Endpoints

- **Liveness**: `/_stcore/health`
- **Readiness**: `/_stcore/health`

### Resource Limits

- **CPU**: 250m requests, 500m limits
- **Memory**: 512Mi requests, 1Gi limits
- **Storage**: 10Gi persistent volume

## Access Control

### User Roles

1. **Administrator**: Full system access
2. **Project Manager**: Project management modules
3. **Site Engineer**: Field operations and reporting

### Session Management

- Automatic session timeout
- Secure logout functionality
- Session state protection

## Deployment Checklist

- [ ] Authentication system tested
- [ ] Docker image built and tagged
- [ ] Kubernetes manifests applied
- [ ] SSL certificates configured
- [ ] Database connection verified
- [ ] Health checks responding
- [ ] User access confirmed

## Support

For technical support or deployment assistance, contact the Highland Tower Development team.

**Project**: $45.5M Mixed-Use Development
**Platform**: gcPanel Enterprise Construction Management
**Status**: Production Ready with Authentication Protection