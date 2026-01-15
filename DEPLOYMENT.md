# 🚀 Deployment Guide

This guide covers various deployment strategies for the Network Intrusion Detection System.

## Table of Contents

- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [AWS Deployment](#aws-deployment)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

---

## Local Deployment

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- 4GB+ RAM recommended

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/network_security.git
   cd network_security
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   
   Create `.env` file:
   ```env
   MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   ```

5. **Push data to MongoDB (optional)**
   ```bash
   python push_data.py
   ```

6. **Train the model**
   ```bash
   python main.py
   ```

7. **Start the API server**
   ```bash
   python app.py
   ```

8. **Access the application**
   
   Open browser: `http://localhost:8080`

---

## Docker Deployment

### Build Docker Image

```bash
docker build -t network-intrusion-detection:latest .
```

### Run Container

```bash
docker run -d \
  -p 8080:8080 \
  --name network-ids \
  -e MONGO_DB_URL="your_mongodb_connection_string" \
  network-intrusion-detection:latest
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MONGO_DB_URL=${MONGO_DB_URL}
    volumes:
      - ./Artifacts:/app/Artifacts
      - ./logs:/app/logs
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Check Logs

```bash
docker logs network-ids
```

### Stop Container

```bash
docker stop network-ids
docker rm network-ids
```

---

## AWS Deployment

### Option 1: EC2 Deployment

#### Prerequisites

- AWS Account
- EC2 instance (t2.medium or larger recommended)
- Security group with port 8080 open

#### Steps

1. **Connect to EC2**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```

2. **Install Docker**
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   ```

3. **Pull Docker image** (if using ECR)
   ```bash
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin your-ecr-uri
   
   docker pull your-ecr-uri/network-security:latest
   ```

4. **Run container**
   ```bash
   docker run -d \
     -p 8080:8080 \
     --name network-ids \
     -e MONGO_DB_URL="your_mongodb_connection_string" \
     your-ecr-uri/network-security:latest
   ```

5. **Access application**
   
   `http://your-ec2-public-ip:8080`

### Option 2: AWS ECR + GitHub Actions (Automated)

This is already configured in `.github/workflows/main.yml`

#### Required GitHub Secrets

Set these in your GitHub repository settings:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REPOSITORY_NAME`
- `AWS_ECR_LOGIN_URI`

#### How It Works

1. **Push to main branch** triggers workflow
2. **Integration tests** run
3. **Docker image** is built
4. **Image pushed** to AWS ECR
5. **EC2 instance** (self-hosted runner) pulls and runs new image

### Option 3: AWS ECS/Fargate

1. **Create ECS Cluster**
   ```bash
   aws ecs create-cluster --cluster-name network-ids-cluster
   ```

2. **Create Task Definition**
   
   Use the Docker image from ECR

3. **Create Service**
   ```bash
   aws ecs create-service \
     --cluster network-ids-cluster \
     --service-name network-ids-service \
     --task-definition network-ids-task \
     --desired-count 1 \
     --launch-type FARGATE
   ```

### Option 4: AWS Lambda + API Gateway (Serverless)

For serverless deployment, you'll need to:

1. Modify the FastAPI app for Lambda compatibility
2. Use AWS Lambda Layers for dependencies
3. Configure API Gateway
4. Use S3 for model storage

---

## Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_DB_URL` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `AWS_ACCESS_KEY_ID` | AWS access key (optional) | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (optional) | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_REGION` | AWS region (optional) | `us-east-1` |

### Optional Configuration

Create `.env` file in project root:

```env
# MongoDB
MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/

# AWS (Optional)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Application
APP_HOST=0.0.0.0
APP_PORT=8080
LOG_LEVEL=INFO

# Model Configuration
MODEL_THRESHOLD=0.5
BATCH_SIZE=32
```

---

## Performance Optimization

### For Production

1. **Use production WSGI server**
   
   Instead of Uvicorn development server:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
   ```

2. **Enable caching**
   
   Cache model in memory to avoid reloading

3. **Load balancing**
   
   Use AWS ELB or Nginx for multiple instances

4. **Resource limits**
   ```bash
   docker run -d \
     -p 8080:8080 \
     --memory="2g" \
     --cpus="2" \
     network-intrusion-detection:latest
   ```

---

## Monitoring & Logging

### Application Logs

Logs are stored in `logs/` directory with timestamp-based filenames.

### Docker Logs

```bash
# View logs
docker logs -f network-ids

# Save logs to file
docker logs network-ids > app.log 2>&1
```

### CloudWatch (AWS)

Configure CloudWatch agent for EC2/ECS:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json \
  -s
```

---

## Scaling Strategies

### Horizontal Scaling

1. **Multiple EC2 instances** behind Application Load Balancer
2. **ECS Service** with desired count > 1
3. **Auto Scaling Group** based on CPU/memory metrics

### Vertical Scaling

- Increase instance size (t2.medium → t2.large)
- Allocate more Docker resources

---

## Security Best Practices

1. **Never commit `.env` file**
   
   Already in `.gitignore`

2. **Use IAM roles** instead of access keys on EC2

3. **Enable HTTPS**
   
   Use AWS Certificate Manager + ALB

4. **Restrict security groups**
   
   Only allow necessary ports

5. **Regular updates**
   ```bash
   docker pull latest-image
   docker restart network-ids
   ```

6. **Secrets management**
   
   Use AWS Secrets Manager or Parameter Store

---

## Health Checks

### API Health Check

```bash
curl http://localhost:8080/
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Network Security API is running"
}
```

### Docker Health Check

Add to Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1
```

---

## Backup & Recovery

### Backup Artifacts

```bash
# Backup trained models
aws s3 sync ./Artifacts/ s3://your-bucket/network-ids/artifacts/

# Backup database
mongodump --uri="mongodb+srv://..." --out=./backup/
```

### Restore

```bash
# Restore artifacts
aws s3 sync s3://your-bucket/network-ids/artifacts/ ./Artifacts/

# Restore database
mongorestore --uri="mongodb+srv://..." ./backup/
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>
```

#### 2. MongoDB Connection Error

- Check connection string format
- Verify network access in MongoDB Atlas
- Ensure IP is whitelisted

#### 3. Model Not Found

```bash
# Retrain model
python main.py
```

#### 4. Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t network-intrusion-detection .
```

#### 5. Out of Memory

- Increase Docker memory limit
- Use larger EC2 instance
- Optimize batch processing

### Debug Mode

Run application in debug mode:

```bash
# Add to .env
DEBUG=True

# Or export
export DEBUG=True
python app.py
```

---

## CI/CD Pipeline

The project includes automated CI/CD via GitHub Actions.

### Workflow Stages

1. **Continuous Integration**
   - Linting
   - Unit tests
   - Code quality checks

2. **Continuous Delivery**
   - Build Docker image
   - Push to AWS ECR

3. **Continuous Deployment**
   - Pull image on EC2
   - Restart container
   - Clean up old images

### Manual Trigger

```bash
# Push to main branch
git push origin main
```

---

## Cost Optimization

### AWS Cost Reduction

1. **Use Reserved Instances** for predictable workloads
2. **Stop EC2 instances** when not needed
3. **Use Spot Instances** for non-critical workloads
4. **Enable S3 lifecycle policies**
5. **Monitor with AWS Cost Explorer**

### Free Tier Options

- **EC2:** t2.micro (750 hours/month)
- **ECR:** 500 MB storage
- **CloudWatch:** 5 GB logs
- **Lambda:** 1M requests/month

---

## Production Checklist

Before deploying to production:

- [ ] Environment variables configured
- [ ] Model trained and validated
- [ ] Docker image tested locally
- [ ] Security groups configured
- [ ] HTTPS enabled
- [ ] Monitoring/logging set up
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Error handling verified

---

## Support

For deployment issues:
- Check [Troubleshooting](#troubleshooting) section
- Review application logs
- Open GitHub issue with details

---

**Last Updated:** January 2026
