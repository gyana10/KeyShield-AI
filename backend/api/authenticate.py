import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User, UserProfile, AuthenticationLog
from backend.db.schemas import AuthenticationRequest, AuthenticationResponse
from backend.core.dependencies import get_current_email
from backend.ml.feature_adapter import build_features
from backend.ml.predictor import predict
from backend.ml.profile_similarity import calculate_similarity
from backend.ml.profile_engine.fusion import TriLayerFusionEngine
from backend.ml.profile_engine.updater import ProfileUpdater
from backend.xai.explainer import explain

router = APIRouter(prefix="", tags=["Authentication Engine"])


@router.post("/authenticate", response_model=AuthenticationResponse)
def authenticate(
    data: AuthenticationRequest,
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # 1. Build statistical features from input timing array
    raw_dict = data.model_dump()
    features = build_features(raw_dict)

    # 2. Retrieve user behavioral profile
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()

    # 3. Calculate Profile Similarity
    if profile:
        profile_res = calculate_similarity(profile, features)
    else:
        profile_res = {
            "similarity": 50.0,
            "explanations": []
        }

    # 4. Stacking Ensemble Inference
    ensemble_res = predict(features, profile)

    # 5. Tri-Layer Fusion Evaluation
    fusion_res = TriLayerFusionEngine.evaluate(ensemble_res, profile_res)

    # 6. Tree SHAP Explanations
    shap_res = explain(features, profile)

    # 7. Adaptive Profile Update (if Genuine & High Confidence)
    if profile:
        ProfileUpdater.update_profile(
            profile_model=profile,
            new_features=features,
            confidence_score=fusion_res["confidence_score"],
            decision=fusion_res["decision"]
        )

    # 8. Store Authentication Log
    now = datetime.utcnow()
    auth_log = AuthenticationLog(
        user_id=user.id,
        decision=fusion_res["decision"],
        anomaly_score=fusion_res["anomaly_score"],
        risk=fusion_res["risk"],
        profile_similarity=fusion_res["profile_similarity"],
        probability=fusion_res["probability"],
        confidence_score=fusion_res["confidence_score"],
        model_contributions=json.dumps(fusion_res["model_contributions"]),
        shap_explanation=json.dumps(shap_res),
        created_at=now
    )

    db.add(auth_log)
    db.commit()

    return {
        "user": user.username,
        "decision": fusion_res["decision"],
        "risk": fusion_res["risk"],
        "probability": fusion_res["probability"],
        "anomaly_score": fusion_res["anomaly_score"],
        "profile_similarity": fusion_res["profile_similarity"],
        "confidence_score": fusion_res["confidence_score"],
        "model_contributions": fusion_res["model_contributions"],
        "explanations": fusion_res["explanations"],
        "shap_explanation": shap_res,
        "timestamp": now
    }