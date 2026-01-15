# 🏗️ System Architecture

## Overview

This document provides a detailed technical architecture of the Network Intrusion Detection System.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Data Sources                         │
│                  (MongoDB / Local CSV)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Ingestion Layer                      │
│  • Load UNSW-NB15 dataset                                    │
│  • Train/Test split                                          │
│  • Artifact storage                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  Data Validation Layer                       │
│  • Schema validation                                         │
│  • Data drift detection                                      │
│  • Quality checks                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                Data Transformation Layer                     │
│  • Feature scaling                                           │
│  • Encoding                                                  │
│  • Missing value imputation                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   Model Training Layer                       │
│  • Algorithm selection                                       │
│  • Hyperparameter tuning                                     │
│  • Model evaluation                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Model Deployment                          │
│  • FastAPI REST API                                          │
│  • Docker container                                          │
│  • Prediction endpoint                                       │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Ingestion Component

**Location:** `networksecurity/components/data_ingestion.py`

**Responsibilities:**
- Connect to MongoDB or read from local CSV
- Split data into training and testing sets
- Save processed data to artifact directory
- Generate data ingestion artifact metadata

**Configuration:** `DataIngestionConfig`

**Output:** `DataIngestionArtifact`

**Key Classes:**
```python
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig)
    def initiate_data_ingestion() -> DataIngestionArtifact
```

### 2. Data Validation Component

**Location:** `networksecurity/components/data_validation.py`

**Responsibilities:**
- Validate schema against predefined schema (YAML)
- Detect data drift using statistical tests
- Check for missing values
- Validate data types and ranges
- Generate validation report

**Configuration:** `DataValidationConfig`

**Input:** `DataIngestionArtifact`

**Output:** `DataValidationArtifact`

**Key Features:**
- Schema validation from `data_schema/schema.yaml`
- Statistical drift detection
- Generates `report.yaml`

### 3. Data Transformation Component

**Location:** `networksecurity/components/data_transformation.py`

**Responsibilities:**
- Handle missing values (SimpleImputer)
- Scale numerical features (StandardScaler)
- Encode categorical features
- Create preprocessing pipeline
- Transform data to NumPy arrays
- Save preprocessing object

**Configuration:** `DataTransformationConfig`

**Input:** `DataValidationArtifact`

**Output:** `DataTransformationArtifact`

**Pipeline:**
```python
preprocessor = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
    ('scaler', StandardScaler())
])
```

### 4. Model Training Component

**Location:** `networksecurity/components/model_trainer.py`

**Responsibilities:**
- Load transformed data
- Train classification model
- Evaluate model performance
- Calculate metrics (accuracy, precision, recall, F1)
- Save trained model
- Generate classification report

**Configuration:** `ModelTrainerConfig`

**Input:** `DataTransformationArtifact`

**Output:** `ModelTrainerArtifact`

**Supported Models:**
- Random Forest Classifier
- XGBoost
- Gradient Boosting
- (Configurable)

### 5. Prediction Pipeline

**Location:** `networksecurity/pipeline/batch_prediction.py`

**Responsibilities:**
- Load preprocessing pipeline
- Load trained model
- Accept new network traffic data
- Transform input features
- Make predictions
- Return classification results

**API Endpoint:** `/predict` (POST)

## Entity Classes

### Config Entities

**Location:** `networksecurity/entity/config_entity.py`

```python
@dataclass
class TrainingPipelineConfig:
    pipeline_name: str
    artifact_dir: str
    timestamp: str

@dataclass
class DataIngestionConfig:
    ...

@dataclass
class DataValidationConfig:
    ...

@dataclass
class DataTransformationConfig:
    ...

@dataclass
class ModelTrainerConfig:
    ...
```

### Artifact Entities

**Location:** `networksecurity/entity/artifact_entity.py`

```python
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
```

## Utilities

### Main Utils

**Location:** `networksecurity/utils/main_utils/utils.py`

**Functions:**
- `read_yaml_file()` - Read YAML configurations
- `write_yaml_file()` - Write YAML reports
- `save_numpy_array_data()` - Save NumPy arrays
- `load_numpy_array_data()` - Load NumPy arrays
- `save_object()` - Serialize Python objects
- `load_object()` - Deserialize Python objects

### ML Utils

**Location:** `networksecurity/utils/ml_utils/`

**Metric Module:**
- `get_classification_score()` - Calculate all metrics
- `ClassificationMetricArtifact` - Store metric results

**Model Module:**
- `NetworkModel` - Custom estimator wrapper
- Model persistence utilities

## Logging & Exception Handling

### Logging

**Location:** `networksecurity/logging/logger.py`

**Features:**
- Timestamp-based log files
- Structured logging format
- Multiple log levels (INFO, DEBUG, ERROR)
- Saved to `logs/` directory

### Exception Handling

**Location:** `networksecurity/exception/exception.py`

**Custom Exception:**
```python
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail: sys)
```

**Features:**
- Detailed error messages
- Line number tracking
- File path in error output
- Stack trace preservation

## Deployment Architecture

### Docker Container

```
┌──────────────────────────────────────┐
│        Docker Container              │
│  ┌────────────────────────────┐      │
│  │     FastAPI Application    │      │
│  │  • /predict endpoint       │      │
│  │  • Model loading           │      │
│  │  • Request validation      │      │
│  └────────────────────────────┘      │
│                                      │
│  ┌────────────────────────────┐      │
│  │   Trained Model Files      │      │
│  │  • model.pkl               │      │
│  │  • preprocessing.pkl       │      │
│  └────────────────────────────┘      │
│                                      │
│  Port: 8080                          │
└──────────────────────────────────────┘
```

### CI/CD Flow

```
Git Push → GitHub Actions → Build Docker → Push to ECR → Deploy to EC2
```

**Stages:**
1. **Integration:** Lint & Test
2. **Build:** Docker image creation
3. **Push:** Upload to AWS ECR
4. **Deploy:** Pull and run on EC2

## Data Flow

```
Raw CSV → MongoDB → Data Ingestion → Validation → Transformation → 
Model Training → Saved Model → API → Predictions
```

## Security Considerations

- Environment variables for sensitive data
- MongoDB connection string in `.env`
- AWS credentials in GitHub Secrets
- Input validation in API
- Error handling without exposing internals

## Scalability

- **Horizontal Scaling:** Multiple API containers behind load balancer
- **Batch Prediction:** Process large datasets efficiently
- **Model Versioning:** Timestamp-based artifact storage
- **Cloud Storage:** S3 integration for large datasets

## Monitoring & Observability

- Application logs in `logs/` directory
- API request/response logging
- Model performance tracking
- Data drift monitoring
- Error rate tracking

---

**Last Updated:** January 2026
