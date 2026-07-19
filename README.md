# KeyShield AI - Behavioral Biometrics Verification Engine

KeyShield AI is a commercial-grade continuous behavioral biometrics verification system that validates user identity based on keystroke dynamics. Rather than relying on simple single-model classification, KeyShield AI implements a **4-layer decision engine** that evaluates timing patterns against learned behavioral baselines.

---

## 4-Layer Verification Architecture

1. **Layer 1: Statistical Profile Similarity (45% Weight)**
   - Extracts 17 statistical feature dimensions (`hold_mean`, `hold_std`, `hold_min`, `hold_max`, `hold_median`, `flight_mean`, `flight_std`, `flight_min`, `flight_max`, `flight_median`, `typing_duration`, `backspaces`, `typing_speed`, `pause_count`, `rhythm_score`, `keystroke_variance`, `transition_variance`).
   - Computes feature-by-feature deviation against the enrolled baseline profile created from 5 enrollment samples.

2. **Layer 2: Independent Isolation Forest Anomaly Detection (15% Weight)**
   - Operates as an independent anomaly detector trained exclusively on genuine timing distributions to identify out-of-distribution typing samples.

3. **Layer 3: Stacking Ensemble Machine Learning (40% Weight)**
   - Integrates Random Forest, XGBoost, and LightGBM base classifiers.
   - Outputs out-of-fold (OOF) probability vectors fed into a Logistic Regression Meta-Learner trained via 5-Fold Stratified Cross-Validation (**92.09% Accuracy, 0.9302 ROC-AUC**).

4. **Layer 4: Tree SHAP Explainability & Natural Language Generator**
   - Calculates local feature attributions and contribution percentages for every verification attempt, producing human-readable explanations.

---

## Model Benchmark & Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Isolation Forest** | 87.29% | 0.8810 | 0.8650 | 0.8729 | 0.8821 |
| **Random Forest** | 92.39% | 0.9250 | 0.9220 | 0.9235 | 0.9258 |
| **XGBoost** | 91.90% | 0.9200 | 0.9180 | 0.9190 | 0.9286 |
| **LightGBM** | 92.06% | 0.9210 | 0.9200 | 0.9205 | 0.9261 |
| **Stacking Ensemble** | **92.09%** | **0.9225** | **0.9200** | **0.9212** | **0.9302** |

---

## Project Structure

```text
KeyShield_AI/
├── backend/
│   ├── api/
│   │   ├── enrollment.py        # 5-sample fixed paragraph enrollment workflow
│   │   ├── authenticate.py      # 4-layer biometric verification endpoint
│   │   └── dashboard.py         # Consolidated metrics, history, and model-info endpoints
│   ├── ml/
│   │   ├── feature_engineering.py # 17-feature extraction, profile generation, similarity, EMA update
│   │   ├── train.py               # IsoForest + RF/XGB/LGBM Stacking Ensemble trainer with 5-fold OOF
│   │   ├── predictor.py           # Verification pipeline orchestrator (4-layer weighted decision engine)
│   │   └── explainability.py      # Tree SHAP local/global attributions & natural language generator
│   ├── db/
│   │   ├── database.py          # SQLAlchemy session & database engine
│   │   ├── models.py            # Database tables (User, Enrollment, UserProfile, AuthenticationLog)
│   │   └── schemas.py           # Pydantic request and response schemas
│   └── main.py                  # FastAPI application entry point
├── frontend/
│   ├── css/
│   │   └── style.css            # Dark mode cybersecurity SaaS design system
│   ├── js/
│   │   ├── main.js              # API client & raw keystroke event recorder
│   │   └── dashboard.js         # Chart.js analytics & dashboard logic
│   ├── index.html               # Landing page
│   ├── enroll.html              # 5-sample fixed paragraph enrollment recorder
│   ├── authenticate.html        # Biometric verification tester
│   └── dashboard.html           # Analytics dashboard
└── tests/                       # Automated pytest suite
```

---

## Quick Start (Local Setup)

### 1. Environment Setup & Dependencies
```bash
git clone https://github.com/gyana10/KeyShield-AI.git
cd KeyShield-AI
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Database & Model Initialization
```bash
python -m backend.db.init_db
python -m backend.ml.train
```

### 3. Launch Backend API Server
```bash
uvicorn backend.main:app --reload --port 8000
```

### 4. Open Frontend Application
Open `frontend/index.html` in your web browser.

---

## Automated Testing
Run the automated test suite:
```bash
pytest tests/ -v
```

---

## Production Deployment
- **Backend API**: Deployed on Render (`https://keyshield-ai-backend.onrender.com`)
- **Frontend App**: Deployed on Vercel (`https://key-shield-ai.vercel.app`)