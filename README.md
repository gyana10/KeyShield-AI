# KeyShield AI 🛡️
### AI Behavioral Biometric Authentication Platform

[![Live Application](https://img.shields.io/badge/Live_App-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://key-shield-ai.vercel.app)
[![API Server](https://img.shields.io/badge/API_Server-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://keyshield-ai-backend.onrender.com)
[![API Docs](https://img.shields.io/badge/API_Docs-OpenAPI-85EA2D?style=for-the-badge&logo=openapi-initiative&logoColor=black)](https://keyshield-ai-backend.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-111111?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0+-20B2AA?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-FF6F00?style=for-the-badge)](https://shap.readthedocs.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)

**KeyShield AI** is an enterprise-grade AI-powered Behavioral Biometric Authentication Platform that continuously verifies user identity based on unique keystroke dynamics (hold times, flight times, press durations, and correction habits).

Designed with an **Apple-inspired UI aesthetic** (`SF Pro` typography, dark mode glassmorphism, pill buttons), KeyShield AI combines a **Stacking Ensemble Machine Learning Pipeline** (Isolation Forest, Random Forest, XGBoost, LightGBM &rarr; Logistic Regression Meta-Learner), a **Z-Score Profile Engine**, and **Tree SHAP Explainability (XAI)**.

---

## 🔗 Live Application Links

- 🌐 **Live Web Application**: [https://key-shield-ai.vercel.app](https://key-shield-ai.vercel.app)
- 👤 **Behavioral Profile Section**: [https://key-shield-ai.vercel.app/profile.html](https://key-shield-ai.vercel.app/profile.html)
- ⚡ **Biometrics Test**: [https://key-shield-ai.vercel.app/authenticate.html](https://key-shield-ai.vercel.app/authenticate.html)
- 📊 **Analytics Dashboard**: [https://key-shield-ai.vercel.app/dashboard.html](https://key-shield-ai.vercel.app/dashboard.html)
- ⚙️ **FastAPI Production Backend**: [https://keyshield-ai-backend.onrender.com](https://keyshield-ai-backend.onrender.com)
- 📖 **Interactive OpenAPI Documentation**: [https://keyshield-ai-backend.onrender.com/docs](https://keyshield-ai-backend.onrender.com/docs)
- 🐙 **GitHub Repository**: [https://github.com/gyana10/KeyShield-AI](https://github.com/gyana10/KeyShield-AI)

---

## 🌟 Key Features

- **🚀 Stacking Ensemble Architecture**: Out-Of-Fold (OOF) cross-validated stacking ensemble combining Isolation Forest, Random Forest, XGBoost, and LightGBM base models with a Logistic Regression meta-learner (**92.09% Accuracy, 0.9302 ROC-AUC**).
- **🔍 Tree SHAP Explainability**: Provides local and global feature attribution using Tree SHAP, explaining *why* an authentication attempt was classified as genuine or suspicious.
- **⚡ Tri-Layer Biometric Fusion**: Combines Stacking Ensemble Probability (50%), Statistical Profile Similarity (35%), and Isolation Forest Anomaly Scores (15%) for robust decision-making.
- **👤 Apple-Styled Behavioral Profile Section**: Dedicated profile section tracking hold/flight timing baseline statistics, correction rates, and real-time behavior drift detection.
- **🛡️ Apple Design System UI**: Sleek dark mode (`SF Pro` font stack, `#000000` / `#161617` canvas, 18px rounded glass cards, pill action buttons, and Chart.js visualizations).
- **🔒 Enterprise Backend Security**: JWT Bearer token authentication, bcrypt password hashing, input validation, and IP-based rate limiting.

---

## 📐 System Architecture

```mermaid
flowchart TD
    subgraph Client["Client Interface (Vercel - Apple UI)"]
        UI["Apple Design System UI\n(Home, Biometrics Test, Profile, Dashboard)"]
        FE["Keystroke Feature Extractor\n(Hold/Flight timings, Totals, Backspaces)"]
        Charts["Chart.js Engine\n(Radar, Gauge, Timeline, SHAP, Model Comparison)"]
    end

    subgraph Backend["FastAPI Backend Services (Render)"]
        Router["REST API Controllers\n(/auth, /enroll, /authenticate, /history, /profile, /model-info, /statistics)"]
        Security["Security Middleware\n(JWT Auth, Rate Limiter, Password Policy, Wildcard CORS)"]

        subgraph ML["Machine Learning Pipeline"]
            SE["Stacking Ensemble\n(IsoForest + RF + XGBoost + LightGBM -> Logistic Regression)"]
            SHAP["Tree SHAP Explainer\n(Feature Contributions & Summary)"]
        end

        subgraph ProfileEngine["Adaptive Profile Engine"]
            SimEngine["Z-Score Profile Similarity"]
            Updater["Adaptive EMA Profile Updater\n& Drift Detector"]
        end
    end

    subgraph Database["PostgreSQL Storage (Neon DB)"]
        DB[(Users, Enrollments, UserProfiles, AuthenticationLogs)]
    end

    UI --> FE
    FE --> Router
    Router --> Security
    Security --> ML
    Security --> ProfileEngine
    ProfileEngine --> DB
    ML --> SHAP
    SHAP --> Router
    Router --> UI
    Charts --> UI
```

---

## 📊 Stacking Ensemble Benchmark Performance

Evaluation on 15,300 benchmark keystroke dynamic samples:

| Model Name | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Equal Error Rate (EER) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Isolation Forest** | 87.29% | 89.39% | 96.16% | 0.9265 | 0.8821 | 18.59% |
| **Random Forest** | 92.39% | 93.11% | 98.12% | 0.9555 | 0.9258 | 14.27% |
| **XGBoost** | 91.90% | 93.30% | 97.25% | 0.9524 | 0.9286 | 14.27% |
| **LightGBM** | 92.06% | 93.41% | 97.33% | 0.9533 | 0.9261 | 14.75% |
| **🏆 Stacking Ensemble** | **92.09%** | **93.29%** | **97.53%** | **0.9536** | **0.9302** | **13.98%** |

---

## 📁 Repository Directory Structure

```
KeyShield_AI/
├── backend/
│   ├── api/                 # REST API Routers (auth, enroll, authenticate, history, profile, model-info, statistics)
│   ├── core/                # Config, JWT Security, Rate Limiter & Dependencies
│   ├── db/                  # SQLAlchemy Database Models, Database Session & Pydantic Schemas
│   ├── ml/                  # Stacking Ensemble Trainer, Predictor & Adaptive Profile Engine
│   ├── xai/                 # Tree SHAP Explainer Module
│   └── main.py              # FastAPI Application Entry Point
├── data/
│   ├── raw/                 # DSL-StrongPasswordData.csv (CMU Keystroke Benchmark)
│   └── processed/           # Processed statistical features dataset
├── frontend/
│   ├── css/                 # Apple Design System styles (SF Pro font, glassmorphism, pill buttons)
│   ├── js/                  # API client, Feature Extractor, Profile & Chart.js Visualizations
│   ├── index.html           # Apple Landing page
│   ├── profile.html         # User Behavioral Profile & Baseline Radar Chart
│   ├── authenticate.html    # Biometric authentication tester
│   └── dashboard.html       # Analytics dashboard
├── tests/                   # Automated pytest test suites (Auth, Stacking, XAI, APIs)
├── .env.example             # Environment variable template
├── render.yaml              # Render deployment configuration
├── vercel.json              # Vercel deployment configuration
└── README.md                # Documentation
```

---

## 🔌 REST API Specifications

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/register` | User Registration with password complexity validation | ❌ |
| `POST` | `/login` | User Login & JWT Access Token issuance | ❌ |
| `POST` | `/enroll` | Multi-sample keystroke profile enrollment (3 samples min) | ✅ |
| `POST` | `/authenticate` | Evaluate biometrics via Stacking Ensemble + SHAP + Profile | ✅ |
| `GET` | `/history` | Paginated user authentication logs & SHAP explanations | ✅ |
| `GET` | `/profile` | User behavioral profile baseline & drift metrics | ✅ |
| `GET` | `/model-info` | Stacking ensemble architecture & benchmark performance | ❌ |
| `GET` | `/statistics` | User and system-level biometrics analytics | ✅ |

---

## 💻 Local Setup & Installation

### 1. Prerequisites
- Python 3.10+
- PostgreSQL (or local SQLite fallback)

### 2. Installation
```bash
git clone https://github.com/gyana10/KeyShield-AI.git
cd KeyShield-AI

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Initialize Database & Train Models
```bash
# Set environment variables
cp .env.example .env

# Initialize database schema
python -m backend.db.init_db

# Train Stacking Ensemble ML models
python -m backend.ml.train
```

### 4. Run Server & Application
```bash
# Start FastAPI backend server
uvicorn backend.main:app --reload --port 8000
```
Open `frontend/index.html` in your browser or serve via Live Server.

### 5. Run Automated Tests
```bash
pytest tests/ -v
```

---

## 🌐 Cloud Deployment Architecture

- **Database**: [Neon.tech](https://neon.tech) (Serverless PostgreSQL)
- **Backend Service**: [Render.com](https://render.com) (FastAPI Python Environment)
- **Frontend App**: [Vercel.com](https://vercel.com) (Global CDN Static Hosting)

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.