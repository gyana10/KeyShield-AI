import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.api.auth import router as auth_router
from backend.api.enrollment import router as enroll_router
from backend.api.authenticate import router as authenticate_router
from backend.api.history import router as history_router
from backend.api.profile import router as profile_router
from backend.api.model_info import router as model_info_router
from backend.api.statistics import router as statistics_router

load_dotenv()

app = FastAPI(
    title="KeyShield AI - Behavioral Biometrics Platform",
    description="AI Behavioral Biometric Authentication System powered by Stacking Ensemble & Tree SHAP Explainability",
    version="1.0.0"
)

# Configurable CORS origins
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:8000,http://localhost:8000")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(enroll_router)
app.include_router(authenticate_router)
app.include_router(history_router)
app.include_router(profile_router)
app.include_router(model_info_router)
app.include_router(statistics_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "KeyShield AI Biometrics Platform 🛡️",
        "version": "1.0.0",
        "docs": "/docs"
    }