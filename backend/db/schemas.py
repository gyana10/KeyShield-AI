from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# Raw Keystroke Timing Event Schema
class RawKeystrokeEvent(BaseModel):
    key: str
    type: str  # "keydown" or "keyup"
    time: float


# 5-Sample Enrollment Request Schema
class EnrollmentRequest(BaseModel):
    samples: List[List[RawKeystrokeEvent]] = Field(..., min_length=5, max_length=5)


class EnrollmentResponse(BaseModel):
    message: str
    enrollment_complete: bool
    total_samples: int
    profile_summary: Dict[str, Any]


# Raw Keystroke Verification Request Schema
class VerificationRequest(BaseModel):
    events: List[RawKeystrokeEvent] = Field(..., min_length=2)


# 4-Layer Verification Response Payload
class VerificationResponse(BaseModel):
    decision: str
    risk: str
    confidence: float
    probability_genuine: float
    probability_suspicious: float
    profile_similarity: float
    isolation_forest_score: float
    isolation_forest_result: str
    rf_probability: float
    xgb_probability: float
    lgb_probability: float
    stacking_probability: float
    top_contributing_features: List[Dict[str, Any]]
    shap_explanation: Dict[str, float]
    text_explanation: str
    feature_breakdown: Dict[str, Any]
    profile_updated: bool
    timestamp: Optional[datetime] = None


# Dashboard Combined Schemas
class DashboardResponse(BaseModel):
    profile: Dict[str, Any]
    history: List[Dict[str, Any]]
    statistics: Dict[str, Any]
    model_info: Dict[str, Any]