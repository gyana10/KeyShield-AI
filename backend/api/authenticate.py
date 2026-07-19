import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import UserProfile, AuthenticationLog
from backend.db.schemas import VerificationRequest, VerificationResponse
from backend.ml.predictor import predictor_engine
from backend.ml.feature_engineering import create_behavioral_profile

router = APIRouter(tags=["Authentication"])


@router.post("/authenticate", response_model=VerificationResponse)
def authenticate_sample(request: VerificationRequest, db: Session = Depends(get_db)):
    """
    Evaluates verification sample through 4-Layer Verification Engine:
    Stage 1: Statistical Profile Similarity
    Stage 2: Independent Isolation Forest Anomaly Detection
    Stage 3: 5-Fold OOF Stacking Ensemble Classification
    Stage 4: Configurable Weighted Decision Engine
    Stage 5: Tree SHAP Explainability & Natural Language Explanation
    """
    raw_events = [e.dict() for e in request.events]

    # Fetch User Behavioral Profile from Database
    profile_record = db.query(UserProfile).filter(UserProfile.user_id == 1).first()

    if profile_record and profile_record.model_blob:
        try:
            behavioral_profile = json.loads(profile_record.model_blob)
        except Exception:
            behavioral_profile = {}
    else:
        # Fallback default baseline if enrollment hasn't been completed yet
        default_features = [predictor_engine.evaluate_verification(raw_events, {})["verification_features"]] * 5
        behavioral_profile = create_behavioral_profile(default_features)

    # Execute 4-Layer Verification Pipeline in predictor_engine
    result = predictor_engine.evaluate_verification(raw_events, behavioral_profile)

    # Log Authentication Record into Database
    auth_log = AuthenticationLog(
        user_id=1,
        decision=result["decision"],
        risk=result["risk"],
        confidence_score=result["confidence"],
        anomaly_score=result["isolation_forest_score"],
        profile_similarity=result["profile_similarity"],
        probability=result["probability_genuine"],
        model_contributions=json.dumps({
            "rf_probability": result["rf_probability"],
            "xgb_probability": result["xgb_probability"],
            "lgb_probability": result["lgb_probability"],
            "stacking_probability": result["stacking_probability"],
            "isolation_forest_result": result["isolation_forest_result"]
        }),
        shap_explanation=json.dumps({
            "top_contributing_features": result["top_contributing_features"],
            "local_contributions": result["shap_explanation"],
            "text_explanation": result["text_explanation"]
        })
    )
    db.add(auth_log)

    # Update Profile via EMA if genuine & high confidence
    if result.get("profile_updated") and result.get("new_profile") and profile_record:
        profile_record.model_blob = json.dumps(result["new_profile"])
        profile_record.last_updated = datetime.utcnow()

    db.commit()

    return {
        "decision": result["decision"],
        "risk": result["risk"],
        "confidence": result["confidence"],
        "probability_genuine": result["probability_genuine"],
        "probability_suspicious": result["probability_suspicious"],
        "profile_similarity": result["profile_similarity"],
        "isolation_forest_score": result["isolation_forest_score"],
        "isolation_forest_result": result["isolation_forest_result"],
        "rf_probability": result["rf_probability"],
        "xgb_probability": result["xgb_probability"],
        "lgb_probability": result["lgb_probability"],
        "stacking_probability": result["stacking_probability"],
        "top_contributing_features": result["top_contributing_features"],
        "shap_explanation": result["shap_explanation"],
        "text_explanation": result["text_explanation"],
        "feature_breakdown": result["feature_breakdown"],
        "profile_updated": result["profile_updated"],
        "timestamp": datetime.utcnow()
    }