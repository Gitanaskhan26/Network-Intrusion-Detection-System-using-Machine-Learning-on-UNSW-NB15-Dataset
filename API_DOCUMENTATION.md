# 📡 API Documentation

## Overview

The Network Intrusion Detection System provides a RESTful API built with FastAPI for making predictions on network traffic data.

**Base URL:** `http://localhost:8080`

**API Version:** v1

---

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Request/Response Formats](#requestresponse-formats)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [Rate Limiting](#rate-limiting)

---

## Authentication

Currently, the API does not require authentication. For production deployment, consider implementing:

- API Keys
- OAuth 2.0
- JWT tokens

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Check if the API is running

**Request:**
```bash
curl -X GET http://localhost:8080/
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Network Security API is running",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### 2. Single Prediction

**Endpoint:** `POST /predict`

**Description:** Predict whether network traffic is malicious or normal based on network flow features

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "features": {
    "having_IP_Address": 1,
    "URL_Length": 54,
    "Shortining_Service": 0,
    "having_At_Symbol": 1,
    "double_slash_redirecting": 0,
    "Prefix_Suffix": -1,
    "having_Sub_Domain": -1,
    "SSLfinal_State": -1,
    "Domain_registeration_length": -1,
    "Favicon": 1,
    "port": 1,
    "HTTPS_token": -1,
    "Request_URL": 1,
    "URL_of_Anchor": -1,
    "Links_in_tags": 1,
    "SFH": -1,
    "Submitting_to_email": -1,
    "Abnormal_URL": -1,
    "Redirect": 0,
    "on_mouseover": 1,
    "RightClick": 1,
    "popUpWidnow": 1,
    "Iframe": 1,
    "age_of_domain": -1,
    "DNSRecord": -1,
    "web_traffic": -1,
    "Page_Rank": -1,
    "Google_Index": 1,
    "Links_pointing_to_page": 1,
    "Statistical_report": -1
  }
}
```

**Response (Success):**
```json
{
  "prediction": "Legitimate",
  "confidence": 0.94,
  "probability": {
    "Legitimate": 0.94,
    "Phishing": 0.06
  },
  "timestamp": "2026-01-15T10:30:45.123456"
}
```

**Response (Phishing Detected):**
```json
{
  "prediction": "Phishing",
  "confidence": 0.89,
  "probability": {
    "Legitimate": 0.11,
    "Phishing": 0.89
  },
  "timestamp": "2026-01-15T10:30:45.123456",
  "alert_level": "high"
}
```

**Status Codes:**
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

### 3. Batch Prediction

**Endpoint:** `POST /predict/batch`

**Description:** Predict multiple website samples at once

**Request Body:**
```json
{
  "samples": [
    {
      "features": { /* feature set 1 */ }
    },
    {
      "features": { /* feature set 2 */ }
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "id": 0,
      "prediction": "Legitimate",
      "confidence": 0.94
    },
    {
      "id": 1,
      "prediction": "Phishing",
      "confidence": 0.89
    }
  ],
  "total": 2,
  "phishing_detected": 1,
  "timestamp": "2026-01-15T10:30:45.123456"
}
```

---

### 4. Upload CSV for Prediction

**Endpoint:** `POST /predict/upload`

**Description:** Upload CSV file with website features for batch prediction

**Request:**
- **Content-Type:** `multipart/form-data`
- **File Parameter:** `file`

**Example:**
```bash
curl -X POST \
  -F "file=@network_traffic.csv" \
  http://localhost:8080/predict/upload
```

**CSV Format:**
```csv
having_IP_Address,URL_Length,Shortining_Service,SSLfinal_State,Google_Index,...
1,54,0,-1,1,...
-1,32,0,1,-1,...
```

**Response:**
```json
{
  "status": "success",
  "total_records": 100,
  "predictions": [
    {
      "row": 0,
      "prediction": "Normal",
      "confidence": 0.92
    },
    // ... more predictions
  ],
  "summary": {
    "legitimate": 85,
    "phishing": 15
  },
  "download_url": "/results/prediction_12345.csv"
}
```

---

### 5. Download Prediction Results

**Endpoint:** `GET /results/{result_id}`

**Description:** Download prediction results as CSV

**Request:**
```bash
curl -X GET http://localhost:8080/results/prediction_12345.csv \
  -o results.csv
```

**Response:**
- **Content-Type:** `text/csv`
- CSV file with predictions

---

### 6. Model Information

**Endpoint:** `GET /model/info`

**Description:** Get information about the deployed model

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "version": "1.0.0",
  "trained_on": "2026-01-10",
  "features": 31,
  "accuracy": 0.91,
  "precision": 0.89,
  "recall": 0.93,
  "f1_score": 0.91,
  "dataset": "Phishing Websites"
}
```

---

### 7. Statistics

**Endpoint:** `GET /stats`

**Description:** Get API usage statistics

**Response:**
```json
{
  "total_predictions": 1523,
  "phishing_detected": 234,
  "legitimate_sites": 1289,
  "uptime": "5 days, 3 hours",
  "last_prediction": "2026-01-15T10:30:45.123456"
}
```

---

## Request/Response Formats

### Feature Schema

The UNSW-NB15 dataset has **49 features**. Here's the complete list:

```json
{
  "dur": "float",           // Flow duration
  "spkts": "int",          // Source to destination packet count
  "dpkts": "int",          // Destination to source packet count
  "sbytes": "int",         // Source to destination bytes
  "dbytes": "int",         // Destination to source bytes
  "rate": "float",         // Packets per second
  "sttl": "int",           // Source to destination time to live
  "dttl": "int",           // Destination to source time to live
  "sload": "float",        // Source bits per second
  "dload": "float",        // Destination bits per second
  "sloss": "int",          // Source packets retransmitted
  "dloss": "int",          // Destination packets retransmitted
  "sinpkt": "float",       // Source inter-packet arrival time (ms)
  "dinpkt": "float",       // Destination inter-packet arrival time (ms)
  "sjit": "float",         // Source jitter (ms)
  "djit": "float",         // Destination jitter (ms)
  "swin": "int",           // Source TCP window advertisement
  "stcpb": "int",          // Source TCP base sequence number
  "dtcpb": "int",          // Destination TCP base sequence number
  "dwin": "int",           // Destination TCP window advertisement
  "tcprtt": "float",       // TCP round trip time
  "synack": "float",       // TCP SYN to SYN-ACK time
  "ackdat": "float",       // TCP SYN-ACK to ACK time
  "smean": "int",          // Mean of packet size (source)
  "dmean": "int",          // Mean of packet size (destination)
  "trans_depth": "int",    // HTTP request/response depth
  "response_body_len": "int", // HTTP response body length
  "ct_srv_src": "int",     // Connection count (service/source)
  "ct_state_ttl": "int",   // Connection count (state/TTL)
  "ct_dst_ltm": "int",     // Connection count (destination/last time)
  "ct_src_dport_ltm": "int", // Connection count (source/dest port/last time)
  "ct_dst_sport_ltm": "int", // Connection count (dest/source port/last time)
  "ct_dst_src_ltm": "int", // Connection count (dest/source/last time)
  "is_ftp_login": "int",   // FTP session (1 = yes, 0 = no)
  "ct_ftp_cmd": "int",     // FTP command count
  "ct_flw_http_mthd": "int", // HTTP method count
  "ct_src_ltm": "int",     // Connection count (source/last time)
  "ct_srv_dst": "int",     // Connection count (service/destination)
  "is_sm_ips_ports": "int" // Same IPs and ports (1 = yes, 0 = no)
  // ... additional features based on full UNSW-NB15 schema
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid feature values",
    "details": {
      "field": "rate",
      "value": -1,
      "constraint": "must be non-negative"
    }
  },
  "timestamp": "2026-01-15T10:30:45.123456"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `MODEL_NOT_FOUND` | 404 | Trained model not available |
| `PREDICTION_ERROR` | 500 | Error during prediction |
| `FILE_UPLOAD_ERROR` | 400 | Invalid file format |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |

---

## Examples

### Python Example

```python
import requests
import json

# API endpoint
url = "http://localhost:8080/predict"

# Sample network traffic data
data = {
    "features": {
        "dur": 0.121478,
        "spkts": 4,
        "dpkts": 2,
        "sbytes": 672,
        "dbytes": 134,
        "rate": 33.19,
        # ... other features
    }
}

# Make prediction request
response = requests.post(url, json=data)

# Parse response
if response.status_code == 200:
    result = response.json()
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### cURL Example

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "dur": 0.121478,
      "spkts": 4,
      "dpkts": 2,
      "sbytes": 672,
      "dbytes": 134,
      "rate": 33.19
    }
  }'
```

### JavaScript Example

```javascript
const predictTraffic = async (features) => {
  const response = await fetch('http://localhost:8080/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ features }),
  });
  
  const result = await response.json();
  return result;
};

// Usage
const features = {
  dur: 0.121478,
  spkts: 4,
  dpkts: 2,
  // ... other features
};

predictTraffic(features)
  .then(result => console.log('Prediction:', result.prediction))
  .catch(error => console.error('Error:', error));
```

---

## Rate Limiting

**Current Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1610710800
```

**Rate Limit Exceeded Response:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
  }
}
```

---

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** `http://localhost:8080/docs`
- **ReDoc:** `http://localhost:8080/redoc`

---

## Webhooks (Future Feature)

Configure webhooks to receive notifications when attacks are detected:

```json
{
  "webhook_url": "https://your-server.com/webhook",
  "events": ["attack_detected"],
  "threshold": 0.8
}
```

---

## SDK Support (Future)

Official SDKs planned for:
- Python
- JavaScript/TypeScript
- Java
- Go

---

## Changelog

### v1.0.0 (2026-01-15)
- Initial API release
- Single and batch prediction endpoints
- CSV upload support
- Model information endpoint

---

## Support

For API issues or questions:
- GitHub Issues: [github.com/yourusername/network_security/issues](https://github.com/yourusername/network_security/issues)
- Email: support@example.com

---

**Last Updated:** January 2026
