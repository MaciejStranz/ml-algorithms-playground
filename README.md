# ML Algorithms Playground

ML Algorithms Playground is an interactive platform that allows users to run machine learning experiments through a web interface.

The project consists of three main layers:

- **ml_core** – computational engine responsible for training, hyperparameter validation, dataset handling, and metrics computation  
- **Django + Django REST Framework** – backend API managing experiments, metadata, datasets, and algorithms  
- **React** – frontend UI for configuring, running, and visualizing experiments *(in progress)*

This project demonstrates backend engineering, ML engineering, API design, and full-stack development.

---

## 🚀 Features

### **Supported Algorithms**

#### Classical (scikit-learn / XGBoost):
- Support Vector Machine (SVC / SVR)
- Random Forest (Classifier / Regressor)
- XGBoost (Classifier / Regressor)
- Logistic Regression / Linear Regression

#### Deep Learning (PyTorch):
- MLPClassifier / MLPRegressor with customizable architecture

---

### **Available Datasets**

- Iris — multiclass classification  
- Wine — multiclass classification  
- Breast Cancer — binary classification  
- Diabetes — regression  
- Synthetic Sinus Function — regression

### Synchronization with Django
All metadata of datasets and algorithms is stored in **ml_core module**, in order to automatically feed Django database with this data 2 sync commends were prepared:
```
python manage.py sync_datasets
python manage.py sync_algorithms
```

## 📦 Experiment System

Each experiment stores:

- Selected dataset  
- Selected algorithm  
- Hyperparameters  
- Train/test split parameters  
- Metrics  
- (Optional) predictions and probabilities  

### Returned results include:
- `y_true`, `y_pred`, `y_proba`
- metrics summary
- dataset & algorithm metadata

---

## 🧩 REST API (Django REST Framework)

### Available endpoints:
```
GET /api/datasets/
GET /api/algorithms/
GET /api/experiments/
POST /api/experiments/
GET /api/experiments/<id>/
```
Experiment status values:
- `running`
- `finished`
- `failed`

In subsequent stages of the project, it is planned to use background jobs (Celery) to conduct training.
In this case, the experiment will have the status “in progress.” Currently, everything is carried out synchronously.

---

## 📤 Example API Request
```
POST /api/experiments/
{
"dataset": 1,
"algorithm": 2,
"hyperparameters": {"C": 1.0, "kernel": "rbf"},
"test_size": 0.3,
"random_state": 42,
"include_predictions": true,
"include_probabilities": true
}
```

## 🛠 Technology Stack

### Machine Learning
- Python, NumPy  
- scikit-learn  
- XGBoost  
- PyTorch  

### Backend
- Django  
- Django REST Framework  
- PostgreSQL or SQLite  

### Frontend (planned)
- React + TypeScript  


