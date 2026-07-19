import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User, UserProfile, AuthenticationLog
from backend.db.schemas import StatisticsResponse
from backend.core.dependencies import get_current_email

router = APIRouter(prefix="", tags=["Biometrics Statistics"])


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(
    email: str = Depends(get_current_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    logs = db.query(AuthenticationLog).filter(
        AuthenticationLog.user_id == user.id
    ).all()

    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    total_attempts = len(logs)
    if total_attempts == 0:
        return {
            "total_authentications": 0,
            "genuine_count": 0,
            "suspicious_count": 0,
            "pass_rate": 0.0,
            "average_similarity": 0.0,
            "average_confidence": 0.0,
            "risk_breakdown": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "drift_status": "NO_PROFILE" if not profile else ("NORMAL" if (profile.drift_score or 0) < 0.5 else "BEHAVIOR_DRIFT_DETECTED")
        }

    genuine_count = sum(1 for l in logs if l.decision == "GENUINE")
    suspicious_count = total_attempts - genuine_count
    pass_rate = round((genuine_count / total_attempts) * 100.0, 2)

    similarities = [l.profile_similarity for l in logs if l.profile_similarity is not None]
    confidences = [l.confidence_score for l in logs if l.confidence_score is not None]

    avg_sim = round(float(np.mean(similarities)), 2) if similarities else 0.0
    avg_conf = round(float(np.mean(confidences)), 2) if confidences else 0.0

    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for l in logs:
        if l.risk in risk_counts:
            risk_counts[l.risk] += 1

    drift_val = profile.drift_score if profile else 0.0
    if drift_val > 0.6:
        drift_status = "SIGNIFICANT_DRIFT"
    elif drift_val > 0.3:
        drift_status = "MODERATE_DRIFT"
    else:
        drift_status = "STABLE"

    return {
        "total_authentications": total_attempts,
        "genuine_count": genuine_count,
        "suspicious_count": suspicious_count,
        "pass_rate": pass_rate,
        "average_similarity": avg_sim,
        "average_confidence": avg_conf,
        "risk_breakdown": risk_counts,
        "drift_status": drift_status
    }
