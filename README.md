# KeyShield AI - Behavioral Biometrics Verification Engine

KeyShield AI is a commercial-grade behavioral biometrics verification platform that validates user identity through keystroke dynamics. KeyShield AI evaluates raw typing timing patterns against a learned statistical baseline using a **4-layer decision engine** combined with explainable artificial intelligence.

---

## Key Features & Security Architecture

1. **5-Sample Baseline Enrollment & 25-Paragraph Bank**
   - Collects 5 raw typing samples using a randomized 25-paragraph text bank.
   - Computes statistical baseline tolerances (`mean`, `median`, `std`, `min`, `max`) across 17 features.
   - Enforces copy-paste anti-cheat protection by disabling text selection, right-click context menus, and paste events.

2. **Backend Feature Extraction (17 Features)**
   - All feature processing occurs on the backend: `hold_mean`, `hold_std`, `hold_min`, `hold_max`, `hold_median`, `flight_mean`, `flight_std`, `flight_min`, `flight_max`, `flight_median`, `typing_duration`, `backspaces`, `typing_speed`, `pause_count`, `rhythm_score`, `keystroke_variance`, `transition_variance`.

3. **4-Layer Decision Fusion Engine**
   - **Layer 1: Statistical Profile Similarity (45% Weight)** — Feature-by-feature deviation score.
   - **Layer 2: Independent Isolation Forest Anomaly Detection (15% Weight)** — Out-of-distribution anomaly detector.
   - **Layer 3: Stacking Ensemble Machine Learning (40% Weight)** — Random Forest + XGBoost + LightGBM base models fed into a 5-Fold Stratified Out-of-Fold (OOF) Logistic Regression Meta-Learner (**92.09% Accuracy, 0.9302 ROC-AUC**).
   - **Layer 4: Tree SHAP Explainability** — Local feature attributions, contribution percentages, and natural language explanations.

4. **Adaptive Behavioral Profile**
   - Updates baseline via Exponential Moving Average (EMA, $\alpha=0.1$) only when verification decision is genuine with $\ge 95\%$ confidence.

---

## Model Performance & Benchmark

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
│   │   ├── enrollment.py        # 5-sample raw keystroke enrollment endpoint
│   │   ├── authenticate.py      # 4-layer biometric verification endpoint
│   │   └── dashboard.py         # Consolidated profile, history, and model-info endpoints
│   ├── ml/
│   │   ├── feature_engineering.py # 17-feature extraction, profile creation, similarity, EMA update
│   │   ├── train.py               # IsoForest + RF/XGB/LGBM Stacking Ensemble trainer with 5-fold OOF
│   │   ├── predictor.py           # Verification pipeline orchestrator (4-layer weighted decision engine)
│   │   └── explainability.py      # Tree SHAP local/global attributions & natural language generator
│   ├── db/
│   │   ├── database.py          # SQLAlchemy session & engine
│   │   ├── models.py            # Database tables (User, Enrollment, UserProfile, AuthenticationLog)
│   │   └── schemas.py           # Pydantic request and response schemas
│   └── main.py                  # FastAPI application entry point
├── frontend/
│   ├── css/
│   │   └── style.css            # Dark mode cybersecurity SaaS design system
│   ├── js/
│   │   ├── main.js              # API client, 25-paragraph bank & anti-cheat protection
│   │   └── dashboard.js         # Chart.js analytics & dashboard logic
│   ├── index.html               # Landing page
│   ├── enroll.html              # 5-sample paragraph recorder
│   ├── authenticate.html        # Biometric verification tester
│   └── dashboard.html           # Analytics dashboard
└── tests/                       # Automated pytest suite
```

---

## Quick Start (Local Setup)

### 1. Environment Setup
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

## Automated Test Execution
Run the automated Pytest test suite:
```bash
pytest tests/ -v
```

---

## Live Production Deployments
- **Backend API**: Deployed on Render (`https://keyshield-ai-backend.onrender.com`)
- **Frontend App**: Deployed on Vercel (`https://key-shield-ai.vercel.app`)