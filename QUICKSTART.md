# 🚀 Quick Start Guide

Get the Network Intrusion Detection System up and running in 5 minutes!

---

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8 or higher
- ✅ pip package manager
- ✅ Git
- ✅ (Optional) Docker
- ✅ (Optional) MongoDB account

---

## Option 1: Quick Local Setup (Recommended for Testing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/network_security.git
cd network_security
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add this content:
```env
MONGO_DB_URL=mongodb+srv://your-username:your-password@cluster.mongodb.net/
```

> 💡 **Tip:** Get a free MongoDB cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### Step 5: Load Data (Optional)

If you have the UNSW-NB15 dataset:

```bash
# Place your CSV in Network_Data/ folder
cp /path/to/UNSW-NB15_1.csv Network_Data/

# Push to MongoDB (optional)
python push_data.py
```

### Step 6: Train the Model

```bash
python main.py
```

Expected output:
```
INFO: Data Ingestion Started
INFO: Data Ingestion Completed
INFO: Data Validation Started
INFO: Data Validation Completed
INFO: Data Transformation Started
INFO: Data Transformation Completed
INFO: Model Training Started
INFO: Model Training Completed
```

### Step 7: Start the API

```bash
python app.py
```

You should see:
```
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8080
```

### Step 8: Test the API

Open your browser and visit:
- **API Docs:** http://localhost:8080/docs
- **ReDoc:** http://localhost:8080/redoc
- **Health Check:** http://localhost:8080/

Or test with curl:
```bash
curl http://localhost:8080/
```

---

## Option 2: Docker Setup (Recommended for Production)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/network_security.git
cd network_security
```

### Step 2: Create .env File

```bash
echo "MONGO_DB_URL=your_mongodb_connection_string" > .env
```

### Step 3: Build Docker Image

```bash
docker build -t network-ids:latest .
```

### Step 4: Run Container

```bash
docker run -d \
  -p 8080:8080 \
  --name network-ids \
  --env-file .env \
  network-ids:latest
```

### Step 5: Verify

```bash
# Check if container is running
docker ps

# View logs
docker logs network-ids

# Test API
curl http://localhost:8080/
```

---

## Option 3: Using Pre-trained Model

If you have a pre-trained model:

### Step 1: Clone and Setup

```bash
git clone https://github.com/yourusername/network_security.git
cd network_security
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Place Model Files

Copy your trained model files to `final_model/`:
```bash
cp /path/to/model.pkl final_model/
cp /path/to/preprocessing.pkl final_model/
```

### Step 3: Start API

```bash
python app.py
```

---

## Making Your First Prediction

### Using the Interactive Docs

1. Go to http://localhost:8080/docs
2. Click on `POST /predict`
3. Click "Try it out"
4. Enter sample data:

```json
{
  "features": {
    "dur": 0.121478,
    "spkts": 4,
    "dpkts": 2,
    "sbytes": 672,
    "dbytes": 134,
    "rate": 33.19,
    "sttl": 252,
    "dttl": 252,
    "sload": 1234.5,
    "dload": 234.6,
    "sloss": 0,
    "dloss": 0,
    "sinpkt": 30.369,
    "dinpkt": 60.738,
    "sjit": 0,
    "djit": 0,
    "swin": 255,
    "stcpb": 0,
    "dtcpb": 0,
    "dwin": 255,
    "tcprtt": 0,
    "synack": 0,
    "ackdat": 0,
    "smean": 168,
    "dmean": 67,
    "trans_depth": 0,
    "response_body_len": 0,
    "ct_srv_src": 2,
    "ct_state_ttl": 2,
    "ct_dst_ltm": 1,
    "ct_src_dport_ltm": 1,
    "ct_dst_sport_ltm": 1,
    "ct_dst_src_ltm": 1,
    "is_ftp_login": 0,
    "ct_ftp_cmd": 0,
    "ct_flw_http_mthd": 0,
    "ct_src_ltm": 2,
    "ct_srv_dst": 1,
    "is_sm_ips_ports": 0
  }
}
```

5. Click "Execute"
6. View the response!

### Using Python

```python
import requests

url = "http://localhost:8080/predict"
data = {
    "features": {
        "dur": 0.121478,
        "spkts": 4,
        "dpkts": 2,
        # ... add all 49 features
    }
}

response = requests.post(url, json=data)
print(response.json())
```

### Using cURL

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "dur": 0.121478,
      "spkts": 4,
      "dpkts": 2
    }
  }'
```

---

## Project Structure Overview

```
network_security/
├── app.py                  # FastAPI application
├── main.py                 # Training pipeline
├── requirements.txt        # Dependencies
├── Dockerfile             # Docker configuration
├── networksecurity/       # Main package
│   ├── components/        # Pipeline components
│   ├── pipeline/          # Orchestration
│   └── utils/            # Utilities
└── Artifacts/            # Training outputs
```

---

## Common Commands

### Training

```bash
# Full training pipeline
python main.py

# Check logs
tail -f logs/$(ls -t logs/ | head -1)
```

### API

```bash
# Start API
python app.py

# Start with specific port
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t network-ids .

# Run container
docker run -d -p 8080:8080 network-ids

# View logs
docker logs -f network-ids

# Stop container
docker stop network-ids

# Remove container
docker rm network-ids
```

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
pip install -r requirements.txt
# or
pip install -e .
```

### Issue: MongoDB Connection Error

**Solution:**
- Check `.env` file exists
- Verify MongoDB connection string
- Ensure IP is whitelisted in MongoDB Atlas
- Test connection:
  ```bash
  python -c "from pymongo import MongoClient; client = MongoClient('your_connection_string'); print(client.list_database_names())"
  ```

### Issue: Port 8080 Already in Use

**Solution:**
```bash
# Find process
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 8000
```

### Issue: Model Not Found

**Solution:**
```bash
# Train model first
python main.py

# Check artifacts
ls -la Artifacts/
```

---

## Next Steps

Now that you're up and running:

1. 📚 **Read the Documentation**
   - [README.md](README.md) - Project overview
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference

2. 🧪 **Experiment**
   - Try different models
   - Tune hyperparameters
   - Add new features

3. 🚀 **Deploy**
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)
   - Set up CI/CD
   - Deploy to cloud

4. 🤝 **Contribute**
   - Check [CONTRIBUTING.md](CONTRIBUTING.md)
   - Open issues
   - Submit pull requests

---

## Getting Help

- 📖 **Documentation:** Check all .md files in root directory
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/network_security/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/network_security/discussions)
- 📧 **Email:** your.email@example.com

---

## Quick Links

- [Full Documentation](README.md)
- [API Docs](http://localhost:8080/docs) (when running)
- [System Architecture](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)

---

**Happy Coding! 🎉**

---

**Last Updated:** January 15, 2026
