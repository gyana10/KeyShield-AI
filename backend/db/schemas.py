from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# User Registration & Auth Schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Enrollment Schemas
class KeystrokeData(BaseModel):
    holdTimes: List[float] = Field(..., min_length=1)
    flightTimes: List[float] = Field(..., min_length=1)
    totalDuration: float = Field(..., gt=0)
    backspaces: int = Field(default=0, ge=0)


class EnrollmentResponse(BaseModel):
    message: str
    user: str
    sample_index: int
    total_samples: int
    enrollment_complete: bool


# Authentication Schemas
class AuthenticationRequest(KeystrokeData):
    pass


class FeatureExplanation(BaseModel):
    feature: str
    description: str
    expected: float
    current: float
    similarity: float


class ModelContribution(BaseModel):
    model_name: str
    probability: float
    weight: float


class ShapExplanation(BaseModel):
    global_importance: Dict[str, float]
    local_contributions: Dict[str, float]
    text_explanation: str


class AuthenticationResponse(BaseModel):
    user: str
    decision: str
    risk: str
    probability: float
    anomaly_score: float
    profile_similarity: float
    confidence_score: float
    model_contributions: Dict[str, Any]
    explanations: List[Dict[str, Any]]
    shap_explanation: Dict[str, Any]
    timestamp: Optional[datetime] = None


# Profile API Schema
class ProfileResponse(BaseModel):
    user_id: int
    username: str
    email: str
    enrollment_complete: bool
    sample_count: int
    drift_score: float
    hold_mean: float
    hold_std: float
    flight_mean: float
    flight_std: float
    total_duration: float
    backspaces: float
    last_updated: datetime


# History API Schema
class LogItem(BaseModel):
    id: int
    decision: str
    risk: str
    anomaly_score: float
    profile_similarity: float
    probability: float
    confidence_score: float
    model_contributions: Optional[Dict[str, Any]] = None
    shap_explanation: Optional[Dict[str, Any]] = None
    created_at: datetime


class HistoryResponse(BaseModel):
    total: int
    logs: List[LogItem]


# Model Info API Schema
class ModelMetrics(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float


class ModelInfoResponse(BaseModel):
    architecture: str
    base_models: List[str]
    meta_learner: str
    features: List[str]
    model_comparison: List[Dict[str, Any]]
    global_feature_importance: Dict[str, float]


# Statistics API Schema
class StatisticsResponse(BaseModel):
    total_authentications: int
    genuine_count: int
    suspicious_count: int
    pass_rate: float
    average_similarity: float
    average_confidence: float
    risk_breakdown: Dict[str, int]
    drift_status: str